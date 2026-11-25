#!/usr/bin/env python3
"""Offline-first annotation adapter. No implicit Worker or credential forwarding."""
import argparse
import base64
import concurrent.futures
import datetime
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

VV_BASE = 'https://rest.variantvalidator.org/VariantValidator/variantvalidator'
GENEBE = 'https://api.genebe.net/cloud/api-public/v1/variant'


from source_http import get_json, FetchError
import copy
import hashlib


def payload_hash(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def request_receipt(url, data):
    return {'url': url, 'payload_sha256': payload_hash(data), 'transport_status': 'ok',
            'retrieved_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}


def checked_request(context, data):
    if not isinstance(context, dict) or context.get('transport_status') != 'ok' or context.get('payload_sha256') != payload_hash(data):
        raise ValueError('complete request receipt bound to this payload required')
    u = urllib.parse.urlparse(context.get('url', ''))
    if u.scheme != 'https' or not u.hostname or u.username or u.password or u.fragment:
        raise ValueError('invalid request receipt URL')
    q = urllib.parse.parse_qs(u.query)
    if any(len(v) != 1 for v in q.values()):
        raise ValueError('ambiguous request query')
    return u, {k: v[0] for k,v in q.items()}


def valid_hgvs(hgvs):
    if not re.fullmatch(r'N[MR]_\d+\.\d+:c\.[^\s]+', hgvs):
        # Synthetic test IDs are accepted only by direct pure function tests, not live CLI.
        raise ValueError('versioned RefSeq transcript:cDNA required; other inputs need external normalization')


def coordinate(c):
    if not isinstance(c, dict):
        raise ValueError('coordinate missing')
    chrom = str(c.get('chr', '')).removeprefix('chr')
    pos = c.get('pos')
    if isinstance(pos, bool) or not str(pos).isdigit() or int(pos) < 1:
        raise ValueError('invalid position')
    if chrom not in [str(i) for i in range(1, 23)] + ['X', 'Y', 'MT', 'M']:
        raise ValueError('invalid chromosome')
    ref, alt = c.get('ref'), c.get('alt')
    if not all(isinstance(x, str) and re.fullmatch('[ACGT]+', x) for x in (ref, alt)) or ref == alt:
        raise ValueError('invalid ref/alt')
    return {'chr': chrom, 'pos': int(pos), 'ref': ref, 'alt': alt}


def protein(p):
    if not isinstance(p, str) or not p:
        return None
    q = p.split(':')[-1].replace('(', '').replace(')', '').replace('*', 'Ter')
    if not q.startswith('p.') or '?' in q:
        return None
    # Conservatively leave one-letter and three-letter notation distinct.
    return q


def src_variantvalidator(d, hgvs):
    vals = [v for v in d.values() if isinstance(v, dict) and v.get('hgvs_transcript_variant') == hgvs]
    if len(vals) != 1:
        raise ValueError('exact requested HGVS not uniquely returned; normalization needs review')
    val = vals[0]
    if val.get('validation_warnings'):
        raise ValueError('VariantValidator warnings require review')
    loci = val.get('primary_assembly_loci') or {}
    def vcf(build):
        c = (loci.get(build) or {}).get('vcf')
        if isinstance(c, str) and c.count('-') == 3:
            ch, po, re_, al = c.split('-'); c = {'chr': ch, 'pos': po, 'ref': re_, 'alt': al}
        return coordinate(c) if c else None
    p = val.get('hgvs_predicted_protein_consequence') or {}
    hg38 = vcf('grch38')
    if not hg38:
        raise ValueError('GRCh38 coordinate missing')
    return {'transcript': hgvs.split(':')[0], 'hgvs_c': hgvs, 'hgvs_p': p.get('tlr') or p.get('slr'),
            'hg38': hg38, 'hg19': vcf('grch37'),
            'hg38_hgvsg': (loci.get('grch38') or {}).get('hgvs_genomic_description')}


def src_genebe(d, coord, transcript, context=None):
    variants = d.get('variants', [d])
    if not isinstance(variants, list) or len(variants) != 1:
        raise ValueError('nonunique variant response')
    v = variants[0]
    if coordinate(v) != coordinate(coord):
        raise ValueError('GeneBe allele mismatch')
    build = v.get('genome')
    if build is not None and build not in ('hg38', 'GRCh38'):
        raise ValueError('GeneBe build mismatched')
    if context is not None or build is None:
        u, q = checked_request(context, d)
        endpoint = urllib.parse.urlparse(GENEBE)
        if (u.netloc, u.path) != (endpoint.netloc, endpoint.path) or q.get('genome') not in ('hg38', 'GRCh38') or coordinate(q) != coordinate(coord):
            raise ValueError('GeneBe request identity/build mismatch')
    cons = v.get('consequences') or []
    matches = [c for c in cons if (c.get('transcript') or c.get('feature')) == transcript]
    if len(matches) != 1:
        raise ValueError('exact transcript missing or ambiguous; no fallback')
    pick = matches[0]
    return {'hgvs_p': pick.get('hgvs_p'), 'transcript': transcript,
            'dbsnp': v.get('dbsnp'), 'acmg_class': v.get('acmg_classification'),
            'acmg_criteria': v.get('acmg_criteria'), 'acmg_score': v.get('acmg_score'),
            'clinvar_class': v.get('clinvar_classification'), 'clinvar_stars': v.get('clinvar_review_status'),
            'clinvar_subs': v.get('clinvar_submissions_summary'), 'clinvar_disease': v.get('clinvar_disease'),
            'alphamissense': v.get('alphamissense_score'), 'bayesdel_noaf': v.get('bayesdelnoaf_score')}


def src_worker(d, coord, hgvs, context=None, hgvsg=None):
    modern = 'query' in d
    if modern:
        u, q = checked_request(context, d)
        query = d.get('query')
        if not isinstance(query, dict) or query.get('hgvs') != hgvs or query.get('dataset') != 'gnomad_r4':
            raise ValueError('Worker query echo mismatch')
        if not u.path.endswith('/annotate') or q.get('hgvs') != hgvs or q.get('dataset') != 'gnomad_r4':
            raise ValueError('Worker request mismatch')
        # Dataset alone cannot prove assembly: require the VV assembly-specific RefSeq accession and HGVS.
        if not hgvsg or (d.get('coord') or {}).get('hgvsg') != hgvsg:
            raise ValueError('Worker GRCh38 RefSeq genomic identity not confirmed')
        if ('build' in d and d['build'] not in ('hg38', 'GRCh38')) or ('input' in d and d['input'] != hgvs):
            raise ValueError('Worker conflicting identity fields')
    elif d.get('input') != hgvs or d.get('build') not in ('hg38', 'GRCh38'):
        raise ValueError('Worker must echo input and build')
    if coordinate(d.get('coord')) != coordinate(coord):
        raise ValueError('Worker allele mismatch')
    out = copy.deepcopy(d)
    statuses = d.get('sources')
    if modern and not isinstance(statuses, dict):
        raise ValueError('Worker upstream statuses missing')
    if statuses is not None:
        if not isinstance(statuses, dict):
            raise ValueError('Worker malformed upstream statuses')
        fields = {'gnomad': 'gnomad_variant', 'constraint': 'gnomad_gene', 'codon_landscape': 'clinvar_codon'}
        out['_field_status'] = {}
        for field, source in fields.items():
            ok = statuses.get(source) == 'ok'
            out['_field_status'][field] = 'available' if ok and d.get(field) is not None else 'unavailable'
            if not ok:
                out[field] = None
        rows = out.get('merged_predictors')
        if isinstance(rows, list):
            source_keys = {'gnomAD':'gnomad_variant', 'dbNSFP':'myvariant', 'VEP':'vep'}
            out['merged_predictors'] = [r for r in rows if isinstance(r,dict) and statuses.get(source_keys.get(r.get('source'))) == 'ok']
        out['_partial'] = any(v != 'ok' for v in statuses.values()) or any(v != 'available' for v in out['_field_status'].values())
    return out


def number(n, label, minimum=0, maximum=None, integral=False):
    import math
    if n is None:
        return None
    if isinstance(n, bool) or not isinstance(n, (int, float)) or not math.isfinite(n):
        raise ValueError('invalid ' + label)
    if n < minimum or (maximum is not None and n > maximum) or (integral and int(n) != n):
        raise ValueError('out of range ' + label)
    return n


def frequency(g, prefix):
    af = number(g.get(prefix + '_af'), 'AF', maximum=1)
    ac = number(g.get(prefix + '_ac'), 'AC', integral=True)
    an = number(g.get(prefix + '_an'), 'AN', integral=True)
    if ac is not None and an is not None:
        if ac > an or (an == 0 and af is not None):
            raise ValueError('invalid AC/AN')
        if af is not None and an and abs(af - ac / an) > 1e-6:
            raise ValueError('inconsistent AF/AC/AN')
    return {'af': af, 'ac': ac, 'an': an}


DBNSFP54_DEFAULT = os.environ.get(
    'DBNSFP54_TABIX', '/Volumes/T9/genomics/refs/annot/dbNSFP/5.4a/dbNSFP5.4a_grch38.gz')
_DB54_FIELDS = ['REVEL_score', 'AlphaMissense_score', 'AlphaMissense_pred', 'CADD_phred', 'CADD_raw',
                'BayesDel_noAF_score', 'BayesDel_addAF_score', 'MetaRNN_score', 'MetaRNN_pred',
                'PrimateAI_score', 'SIFT_score', 'SIFT_pred', 'Polyphen2_HDIV_score', 'Polyphen2_HDIV_pred',
                'Polyphen2_HVAR_score', 'Polyphen2_HVAR_pred', 'VARITY_R_score', 'ESM1b_score', 'ESM1b_pred',
                'gnomAD4.1_joint_AF', 'gnomAD4.1_joint_AC', 'gnomAD4.1_joint_AN', 'gnomAD4.1_joint_POPMAX_AF']
_DB54_MIN = {'SIFT_score'}                 # 越小越有害；其余数值取最大（最不利于良性的一端）
_DB54_OVERLAY = {'REVEL': 'REVEL_score', 'ALPHAMISSENSE': 'AlphaMissense_score',
                 'BAYESDEL_NOAF': 'BayesDel_noAF_score', 'METARNN': 'MetaRNN_score',
                 'PRIMATEAI': 'PrimateAI_score', 'VARITY_R': 'VARITY_R_score',
                 'ESM1B': 'ESM1b_score', 'CADD_PHRED': 'CADD_phred'}
_DB54_BOUNDED = {'REVEL', 'ALPHAMISSENSE'}


def _find_tabix():
    import shutil
    for c in (os.environ.get('TABIX_BIN'), shutil.which('tabix'),
              os.path.expanduser('~/miniforge3/envs/trio/bin/tabix'),
              '/opt/homebrew/bin/tabix', '/usr/local/bin/tabix'):
        if c and os.path.exists(c):
            return c
    return None


def src_dbnsfp54(c):
    """本地 dbNSFP 5.4a 查询（无外发）。不可用时 raise，由调用方记录状态并回落在线值。"""
    import subprocess
    path = os.environ.get('DBNSFP54_TABIX', DBNSFP54_DEFAULT)
    tabix = _find_tabix()
    if not (os.path.exists(path) and os.path.exists(path + '.tbi')):
        raise RuntimeError('dbNSFP 5.4a 不可用（T9 未挂载？）: ' + path)
    if not tabix:
        raise RuntimeError('找不到 tabix（设 TABIX_BIN 或加入 PATH）')
    chrom = str(c['chr']).removeprefix('chr')
    pos = int(c['pos'])                     # 5.4a contig 无 chr 前缀
    hdr = subprocess.run([tabix, '-H', path], capture_output=True, text=True, timeout=120)
    if hdr.returncode != 0 or not hdr.stdout.strip():
        raise RuntimeError('tabix 表头失败: ' + hdr.stderr.strip()[:100])
    col = {n: i for i, n in enumerate(hdr.stdout.splitlines()[0].lstrip('#').split('\t'))}
    out = subprocess.run([tabix, path, f'{chrom}:{pos}-{pos}'], capture_output=True, text=True, timeout=300)
    if out.returncode != 0:
        raise RuntimeError('tabix 查询失败: ' + out.stderr.strip()[:100])
    rows = [r.split('\t') for r in out.stdout.splitlines() if r.strip()]
    rows = [r for r in rows if len(r) > max(col.values()) and r[col['ref']] == c['ref'] and r[col['alt']] == c['alt']]
    if not rows:
        return {'found': False, 'path': path,
                'note': '5.4a 无此等位记录（indel/非 SNV 不在库内，不得解读为预测良性）'}
    values, raw = {}, {}
    for f in _DB54_FIELDS:
        vals = [v for r in rows for v in r[col[f]].split(';') if v not in ('.', '')]
        raw[f] = vals
        if not vals:
            continue
        try:
            nums = [float(v) for v in vals]
        except ValueError:
            values[f] = vals[0] if len(set(vals)) == 1 else ';'.join(sorted(set(vals)))
            continue
        values[f] = min(nums) if f in _DB54_MIN else max(nums)
    values['version'] = '5.4a'
    values['rows'] = len(rows)
    return {'found': True, 'path': path, 'values': values, 'raw': raw}


def to_evidence(hgvs, responses, request_metadata=None, dbnsfp54=False):
    request_metadata = request_metadata or {}
    states, warnings, parsed = {}, [], {}
    def parse(name, fn):
        value = responses.get(name)
        if value is None:
            states[name] = {'status': 'unavailable', 'reason': 'response not supplied'}
            return {}
        try:
            if not isinstance(value, dict) or not value or value.get('error') or value.get('errors'):
                raise ValueError('empty/error response')
            out = fn(value)
            states[name] = {'status': 'validated', 'reason': 'identity validated; field completeness checked separately'}
            parsed[name] = out
            return out
        except (ValueError, TypeError, KeyError, AttributeError) as e:
            states[name] = {'status': 'unavailable', 'reason': str(e)}
            return {}
    vv = parse('variantvalidator', lambda d: src_variantvalidator(d, hgvs))
    gb, wk = {}, {}
    if vv.get('hg38'):
        gb = parse('genebe', lambda d: src_genebe(d, vv['hg38'], vv['transcript'], request_metadata.get('genebe')))
        wk = parse('worker', lambda d: src_worker(d, vv['hg38'], hgvs, request_metadata.get('worker'), vv.get('hg38_hgvsg')))
    else:
        for name in ('genebe', 'worker'):
            states[name] = {'status': 'blocked', 'reason': 'no validated coordinate/transcript anchor'}
    if wk.get('_partial'):
        states['worker'] = {'status': 'partial', 'reason': 'identity validated; one or more upstream fields unavailable'}
    if wk.get('warnings'):
        warnings.append('Worker reported upstream warnings; see raw response and field statuses')
    p1, p2 = protein(vv.get('hgvs_p')), protein(gb.get('hgvs_p'))
    state = 'verified' if p1 and p2 and p1 == p2 else 'conflict' if p1 and p2 else 'single_source' if p1 or p2 else 'unresolved'
    if state == 'conflict':
        warnings.append('Protein consequences conflict; do not assign consequence-dependent evidence')
    fq = {'global': {'af': None, 'ac': None, 'an': None}, 'eas': {'af': None, 'ac': None, 'an': None}}
    try:
        gnomad = wk.get('gnomad') or {}
        if not isinstance(gnomad, dict):
            raise ValueError('invalid frequency payload')
        for group in ('global', 'eas'):
            fq[group] = frequency(gnomad, group)
    except ValueError as e:
        fq = {'global': {'af': None, 'ac': None, 'an': None}, 'eas': {'af': None, 'ac': None, 'an': None}}
        warnings.append(str(e)); states['worker'] = {'status': 'partial', 'reason': 'frequency rejected'}
    preds = {}
    predictor_rows = wk.get('merged_predictors') or []
    if not isinstance(predictor_rows, list):
        warnings.append('invalid predictor payload'); predictor_rows = []
    for pr in predictor_rows:
        if not isinstance(pr, dict) or not isinstance(pr.get('id'), str) or not pr.get('id'):
            warnings.append('invalid predictor row'); continue
        key = pr['id']
        try:
            bounded = key.upper() in ('REVEL', 'REVEL_MAX', 'SPLICEAI', 'SPLICEAI_DS_MAX', 'ALPHAMISSENSE', 'SIFT', 'SIFT_MAX', 'POLYPHEN', 'POLYPHEN_MAX')
            raw = pr.get('value')
            if isinstance(raw, str) and re.fullmatch(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?', raw):
                raw = float(raw)
            value = number(raw, 'predictor ' + key, minimum=0 if bounded else -1e300, maximum=1 if bounded else None)
        except ValueError:
            warnings.append('invalid predictor ' + key); continue
        if key in preds and (preds[key]['status'] == 'conflict' or preds[key]['value'] != value):
            preds[key] = {'value': None, 'source': None, 'status': 'conflict'}
        else:
            preds[key] = {'value': value, 'source': pr.get('source'), 'status': 'available' if value is not None else 'unavailable'}
    for key, field in [('ALPHAMISSENSE', 'alphamissense'), ('BAYESDEL_NOAF', 'bayesdel_noaf')]:
        value = gb.get(field)
        if value is not None:
            try:
                value = number(value, key, minimum=0 if key == 'ALPHAMISSENSE' else -1e300,
                               maximum=1 if key == 'ALPHAMISSENSE' else None)
                if key in preds and (preds[key]['status'] == 'conflict' or preds[key]['value'] != value):
                    preds[key] = {'value': None, 'source': None, 'status': 'conflict'}
                else:
                    preds[key] = {'value': value, 'source': 'GeneBe', 'status': 'available'}
            except ValueError:
                warnings.append('invalid predictor ' + key)
    db54 = None
    if vv.get('hg38'):
        if dbnsfp54:
            try:
                db54 = src_dbnsfp54(vv['hg38'])
                states['dbnsfp54_local'] = {'status': 'ok', 'reason': 'local dbNSFP 5.4a tabix; no outbound request'}
                if not db54.get('found'):
                    warnings.append('dbNSFP 5.4a 无此等位（indel/非 SNV 不覆盖）；不得当作预测良性')
            except (RuntimeError, OSError, ValueError, IndexError) as e:
                states['dbnsfp54_local'] = {'status': 'unavailable', 'reason': str(e)[:160]}
        else:
            states['dbnsfp54_local'] = {'status': 'disabled', 'reason': 'local dbNSFP query not requested'}
    else:
        states['dbnsfp54_local'] = {'status': 'blocked', 'reason': 'no validated hg38 coordinate'}
    if db54 and db54.get('found'):
        for key, field in _DB54_OVERLAY.items():
            raw = db54['values'].get(field)
            if not isinstance(raw, (int, float)):
                continue
            try:
                value = number(raw, key, minimum=0 if key in _DB54_BOUNDED else -1e300,
                               maximum=1 if key in _DB54_BOUNDED else None)
            except ValueError:
                warnings.append('invalid local dbNSFP value ' + key)
                continue
            preds[key] = {'value': value, 'source': 'dbNSFP5.4a(local)', 'status': 'available'}
        if any(p.get('source') == 'dbNSFP5.4a(local)' for p in preds.values()):
            warnings.append('REVEL/AlphaMissense/BayesDel/MetaRNN/PrimateAI/VARITY_R/ESM1b/CADD 已用本地 dbNSFP 5.4a 覆盖在线值；SIFT/PolyPhen 仍用 VEP/在线规范转录本值')
    return {'schema_version': '0.4', 'input': hgvs,
            'protein_gate': {'status': state, 'passed': state == 'verified',
                             'usable_for_consequence_review': bool(vv.get('hg38')) and state in ('verified','single_source'),
                             'identity_status': 'validated' if vv.get('hg38') else 'unresolved',
                             'crosscheck_status': 'agreed' if state == 'verified' else 'conflict' if state == 'conflict' else 'not_completed', 'transcript': vv.get('transcript'),
                             'hgvs_c': vv.get('hgvs_c'), 'hgvs_p': vv.get('hgvs_p'), 'hgvs_p_genebe': gb.get('hgvs_p'),
                             'source': [name for name, p in [('VariantValidator', p1), ('GeneBe', p2)] if p]},
            'coords': {'hg38': vv.get('hg38'), 'hg19': vv.get('hg19'), 'rsid': gb.get('dbsnp')},
            'clinvar': {k: gb.get(v) for k, v in [('classification', 'clinvar_class'), ('stars', 'clinvar_stars'), ('submissions', 'clinvar_subs'), ('disease', 'clinvar_disease')]},
            'frequency': fq, 'predictors': preds,
            'dbnsfp54': None if not db54 else {'version': '5.4a', 'found': db54.get('found'),
                                               'note': db54.get('note'), **db54.get('values', {})},
            'constraint': wk.get('constraint'),
            'codon_landscape': wk.get('codon_landscape'),
            'acmg_benchmark': {'tool': 'GeneBe', 'classification': gb.get('acmg_class'), 'criteria': gb.get('acmg_criteria'), 'score': gb.get('acmg_score'), 'use': 'benchmark_only'},
            '_sources': states, '_warnings': warnings,
            '_upstream_status': wk.get('sources', {}), '_field_status': wk.get('_field_status', {}),
            '_request_metadata': request_metadata,
            '_needs_manual': ['frequency coverage/filters/dataset/FAF', 'current VCEP and source rules', 'field-level provenance', 'CNV uses separate workflow'],
            'classification': None, 'report_status': 'evidence_collection_only'}


def annotate(hgvs, worker_url=None, genebe_auth=None, dbnsfp54=True):
    valid_hgvs(hgvs)
    enc = urllib.parse.quote(hgvs, safe='')
    responses, status, requests, receipts = {}, {}, {}, {}
    def fetch(name, url, auth=None):
        requests[name] = url
        try:
            responses[name] = get_json(url, auth=auth)
            receipts[name] = request_receipt(url, responses[name])
            status[name] = {'status': 'ok'}
        except FetchError as e:
            status[name] = e.record()
        except (ValueError, TypeError):
            status[name] = {'status': 'invalid_response'}
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        jobs = [pool.submit(fetch, 'variantvalidator', f'{VV_BASE}/GRCh38/{enc}/all')]
        if worker_url:
            u = urllib.parse.urlparse(worker_url)
            if u.scheme != 'https' or u.username or u.password or u.query or u.fragment:
                raise ValueError('Worker must be a credential-free HTTPS base URL')
            jobs.append(pool.submit(fetch, 'worker', worker_url.rstrip('/').removesuffix('/annotate') + '/annotate?' + urllib.parse.urlencode({'hgvs': hgvs, 'dataset': 'gnomad_r4'})))
        else:
            status['worker'] = 'not_configured'
        for job in jobs:
            job.result()
    try:
        vv = src_variantvalidator(responses.get('variantvalidator', {}), hgvs)
        params = dict(vv['hg38'], genome='hg38', useEnsembl='False')
        fetch('genebe', GENEBE + '?' + urllib.parse.urlencode(params), genebe_auth)
    except (ValueError, TypeError):
        status['genebe'] = 'blocked; validated anchor unavailable'
    ev = to_evidence(hgvs, responses, receipts, dbnsfp54=dbnsfp54)
    ev['_fetch_status'] = status
    ev['_provenance'] = {'retrieved_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'request_urls': requests,
                         'adapter_status': 'request_bound_v0.6.3; per-source and per-field status required'}
    return ev, responses


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('hgvs')
    source = ap.add_mutually_exclusive_group()
    source.add_argument('--fixture', type=Path)
    source.add_argument('--online', action='store_true')
    ap.add_argument('--worker', help='Explicit trusted HTTPS base URL; no default')
    ap.add_argument('--raw', action='store_true')
    ap.add_argument('--card', action='store_true')
    ap.add_argument('--no-dbnsfp54', action='store_true', help='Skip the local dbNSFP 5.4a tabix query')
    ap.add_argument('--dbnsfp54', metavar='PATH', help='Override the local dbNSFP 5.4a .gz path for this run')
    args = ap.parse_args()
    try:
        if args.fixture:
            responses = json.loads(args.fixture.read_text())
            metadata = responses.get('request_metadata') or responses.get('evidence', {}).get('_request_metadata', {})
            responses = responses.get('responses', responses)
            ev = to_evidence(args.hgvs, responses, metadata, dbnsfp54=bool(args.dbnsfp54))
            ev['_provenance'] = {'mode': 'offline_fixture', 'source_file': str(args.fixture)}
        elif args.online:
            key = os.environ.get('GENEBE_KEY')
            email = os.environ.get('GENEBE_EMAIL')
            auth = (email + ':' + key) if email and key else key
            if auth and ':' not in auth:
                raise ValueError('GENEBE_EMAIL plus GENEBE_KEY required (or legacy email:key)')
            if args.dbnsfp54:
                os.environ['DBNSFP54_TABIX'] = args.dbnsfp54
            ev, responses = annotate(args.hgvs, args.worker, auth, dbnsfp54=not args.no_dbnsfp54)
        else:
            responses = {}; ev = to_evidence(args.hgvs, {})
            ev['_fetch_status'] = {'all': 'offline; supply --fixture or explicitly --online'}
        if args.raw:
            result = {'evidence': ev, 'responses': responses}
        elif args.card:
            print('变异证据卡（测试版）')
            print('Input: ' + args.hgvs)
            print('Protein gate: ' + ev['protein_gate']['status'])
            print('HGVSp: ' + str(ev['protein_gate']['hgvs_p']))
            print('Coordinates: ' + json.dumps(ev['coords'], ensure_ascii=False))
            print('Frequency: ' + json.dumps(ev['frequency'], ensure_ascii=False))
            print('Predictors: ' + json.dumps(ev['predictors'], ensure_ascii=False))
            if ev.get('dbnsfp54'):
                print('dbNSFP 5.4a: ' + json.dumps({k: v for k, v in ev['dbnsfp54'].items() if k != 'raw'}, ensure_ascii=False))
            print('Sources: ' + json.dumps(ev['_sources'], ensure_ascii=False))
            print('Classification: 未完成正式评级')
            return
        else:
            result = ev
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    except (ValueError, TypeError, KeyError) as e:
        ap.error(str(e))


if __name__ == '__main__':
    main()
