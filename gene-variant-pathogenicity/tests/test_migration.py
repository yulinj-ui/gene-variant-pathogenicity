import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import genebe_fields as g
import cnv_interval as c
import score as s

HGVS = 'NM_000001.1:c.28C>T'
CO = {'chr': '1', 'pos': 101, 'ref': 'C', 'alt': 'T'}

def sources():
    return {'variantvalidator': {HGVS: {'hgvs_transcript_variant': HGVS,
            'primary_assembly_loci': {'grch38': {'vcf': CO}},
            'hgvs_predicted_protein_consequence': {'tlr': 'NP_000001.1:p.(Arg10Trp)'}}},
            'genebe': {'variants': [dict(CO, genome='hg38', consequences=[{'transcript': 'NM_000001.1', 'hgvs_p': 'NP_000001.1:p.Arg10Trp'}])]},
            'worker': {'input': HGVS, 'build': 'GRCh38', 'coord': CO, 'gnomad': {'global_af': 0, 'global_ac': 0, 'global_an': 2000}}}

def scored(points='1', framework='SNV'):
    return {'framework': framework, 'rules': {'test-rule': {'code': 'TEST', 'status': 'reviewed', 'framework': framework,
            'source': 'synthetic fixture; NOT a medical authority', 'version': 'test-1', 'location': 'fixture',
            'reviewer': 'test-harness', 'reviewed_at': '2026-09-26', 'applicability': 'synthetic arithmetic only', 'allowed_points': [points]}},
            'evidence': [{'id': 'ev1', 'code': 'TEST', 'framework': framework, 'rule_id': 'test-rule',
                          'status': 'reviewed', 'gate': 'passed', 'points': points, 'source_ids': ['fixture'], 'basis_ids': ['observation1'], 'rationale': 'synthetic test'}],
            'combination_policy': {'framework': framework, 'status': 'reviewed', 'source': 'synthetic', 'version': 'test', 'reviewer': 'test-harness', 'reviewed_at': '2026-09-26', 'mutually_exclusive': [], 'caps': []}}

class AnnotationTests(unittest.TestCase):
    def test_agreement(self):
        ev = g.to_evidence(HGVS, sources())
        self.assertTrue(ev['protein_gate']['passed'])
        self.assertEqual(ev['frequency']['global']['af'], 0)
        self.assertIsNone(ev['classification'])

    def test_protein_conflict(self):
        d = sources(); d['genebe']['variants'][0]['consequences'][0]['hgvs_p'] = 'p.Arg10Ter'
        ev = g.to_evidence(HGVS, d)
        self.assertFalse(ev['protein_gate']['passed']); self.assertEqual(ev['protein_gate']['status'], 'conflict')

    def test_vv_missing_never_claims_crosscheck(self):
        d=sources();d['variantvalidator']=None
        ev=g.to_evidence(HGVS,d)
        self.assertFalse(ev['protein_gate']['passed']);self.assertEqual(ev['protein_gate']['source'], [])
        self.assertIsNone(ev['coords']['hg38'])

    def test_wrong_transcript_no_fallback(self):
        d=sources(); d['genebe']['variants'][0]['consequences'][0]['transcript']='NM_000002.1'
        ev=g.to_evidence(HGVS,d)
        self.assertIsNone(ev['protein_gate']['hgvs_p_genebe']);self.assertFalse(ev['protein_gate']['passed'])

    def test_version_mismatch(self):
        d=sources();d['genebe']['variants'][0]['consequences'][0]['transcript']='NM_000001.2'
        self.assertEqual(g.to_evidence(HGVS,d)['_sources']['genebe']['status'],'unavailable')

    def test_coordinate_mismatch(self):
        d=sources();d['worker']['coord']=dict(CO,pos=102)
        ev=g.to_evidence(HGVS,d);self.assertEqual(ev['_sources']['worker']['status'],'unavailable')
        self.assertIsNone(ev['frequency']['global']['af'])

    def test_build_mismatch(self):
        d=sources();d['genebe']['variants'][0]['genome']='hg19'
        self.assertFalse(g.to_evidence(HGVS,d)['protein_gate']['passed'])

    def test_missing_is_not_zero(self):
        ev=g.to_evidence(HGVS,{})
        self.assertIsNone(ev['frequency']['global']['af']);self.assertIsNone(ev['classification'])

    def test_unresolved_protein_not_passed(self):
        d=sources();d['variantvalidator'][HGVS]['hgvs_predicted_protein_consequence']['tlr']='p.?'
        d['genebe']['variants'][0]['consequences'][0]['hgvs_p']='p.?'
        self.assertEqual(g.to_evidence(HGVS,d)['protein_gate']['status'],'unresolved')

    def test_vv_warnings_block(self):
        d=sources();d['variantvalidator'][HGVS]['validation_warnings']=['reference mismatch']
        self.assertIsNone(g.to_evidence(HGVS,d)['coords']['hg38'])

    def test_invalid_frequency(self):
        for freq in [{'global_af':1.1},{'global_af':float('nan')},{'global_ac':2,'global_an':1},{'global_af':0.1,'global_ac':0,'global_an':2000}]:
            with self.subTest(freq=freq):
                d=sources();d['worker']['gnomad']=freq
                ev=g.to_evidence(HGVS,d);self.assertIsNone(ev['frequency']['global']['af']);self.assertTrue(ev['_warnings'])

    def test_error_object_not_success(self):
        d=sources();d['worker']={'error':'429'}
        self.assertEqual(g.to_evidence(HGVS,d)['_sources']['worker']['status'],'unavailable')

    def test_predictor_conflict(self):
        d=sources();d['worker']['merged_predictors']=[{'id':'REVEL','value':0.1},{'id':'REVEL','value':0.9}]
        self.assertIsNone(g.to_evidence(HGVS,d)['predictors']['REVEL']['value'])

    def test_offline_cli_from_other_cwd(self):
        with patch.object(g,'get_json',side_effect=AssertionError('network forbidden')):
            ev=g.to_evidence(HGVS,sources());self.assertTrue(ev['protein_gate']['passed'])
        result=subprocess.run([sys.executable,str(ROOT/'scripts/genebe_fields.py'),HGVS],cwd='/tmp',capture_output=True,text=True,check=True)
        self.assertIn('offline',json.loads(result.stdout)['_fetch_status']['all'])

    def test_online_mock_has_no_default_worker_or_key_forward(self):
        d=sources(); urls=[]
        def fake(url,auth=None):
            urls.append(url)
            return d['variantvalidator'] if 'VariantValidator/' in url else d['genebe']
        with patch.object(g,'get_json',side_effect=fake),patch.dict('os.environ',{'NCBI_KEY':'SECRET','WORKER_URL':'https://unexpected.invalid'}):
            ev,_=g.annotate(HGVS)
        self.assertEqual(len(urls),2);self.assertFalse(any('SECRET' in u or 'unexpected' in u for u in urls))
        self.assertEqual(ev['_fetch_status']['worker'],'not_configured')

    def test_malformed_frequency_and_predictor_payload(self):
        d=sources();d['worker']['gnomad']=['bad'];d['worker']['merged_predictors']={'bad':'shape'}
        ev=g.to_evidence(HGVS,d)
        self.assertIsNone(ev['frequency']['global']['af']);self.assertEqual(ev['predictors'],{})

    def test_predictor_conflict_stays_conflict(self):
        d=sources();d['worker']['merged_predictors']=[{'id':'REVEL','value':0.1},{'id':'REVEL','value':0.9},{'id':'REVEL','value':None}]
        self.assertEqual(g.to_evidence(HGVS,d)['predictors']['REVEL']['status'],'conflict')

    def test_bounded_predictor(self):
        d=sources();d['worker']['merged_predictors']=[{'id':'REVEL','value':5}]
        self.assertNotIn('REVEL',g.to_evidence(HGVS,d)['predictors'])

    def test_http_429_retry(self):
        import io, urllib.error
        opener=unittest.mock.Mock()
        opener.open.side_effect=[urllib.error.HTTPError('https://example.invalid',429,'limit',{},None),io.StringIO('{"ok":true}')]
        with patch.object(g.urllib.request,'build_opener',return_value=opener),patch.object(g.time,'sleep'):
            self.assertEqual(g.get_json('https://example.invalid'),{'ok':True})
        self.assertEqual(opener.open.call_count,2)

    def test_http_auth_error_not_retried(self):
        import urllib.error
        opener=unittest.mock.Mock()
        opener.open.side_effect=urllib.error.HTTPError('https://example.invalid',401,'auth',{},None)
        with patch.object(g.urllib.request,'build_opener',return_value=opener),self.assertRaises(RuntimeError):
            g.get_json('https://example.invalid')
        self.assertEqual(opener.open.call_count,1)

    def test_timeout_exhausted(self):
        opener=unittest.mock.Mock();opener.open.side_effect=TimeoutError('sensitive detail')
        with patch.object(g.urllib.request,'build_opener',return_value=opener),patch.object(g.time,'sleep'),self.assertRaisesRegex(RuntimeError,'network unavailable'):
            g.get_json('https://example.invalid')
        self.assertEqual(opener.open.call_count,2)

class ScoreTests(unittest.TestCase):
    def test_pending_not_scored(self):
        d=scored();d['rules']['test-rule']['status']='pending'
        r=s.score(d);self.assertEqual(r['net_points'],'0');self.assertIsNone(r['sandbox_partition'])

    def test_points_cannot_override_rule(self):
        d=scored();d['evidence'][0]['points']='8'
        self.assertEqual(s.score(d)['excluded'][0]['reason'],'points_not_approved')

    def test_no_clinical_classification(self):
        r=s.score(scored('10'));self.assertEqual(r['sandbox_partition'],'P_range');self.assertIsNone(r['classification'])

    def test_duplicate_patient_different_sources(self):
        d=scored();extra=dict(d['evidence'][0],id='ev2',source_ids=['another website']);d['evidence'].append(extra)
        r=s.score(d);self.assertEqual(r['net_points'],'1');self.assertEqual(r['excluded'][0]['reason'],'duplicate_underlying_evidence')

    def test_wrong_framework(self):
        d=scored(framework='CNV_LOSS');d['evidence'][0]['framework']='CNV_GAIN'
        self.assertEqual(s.score(d)['net_points'],'0')

    def test_mutual_exclusion(self):
        d=scored();d['evidence'].append(dict(d['evidence'][0],id='ev2',code='TEST_OTHER',basis_ids=['other']))
        d['rules']['other-rule']=dict(d['rules']['test-rule'],code='TEST_OTHER')
        d['evidence'][1]['rule_id']='other-rule'
        d['combination_policy']['mutually_exclusive']=[['TEST','TEST_OTHER']]
        self.assertIsNone(s.score(d)['sandbox_partition'])

    def test_cap(self):
        d=scored('4');d['combination_policy']['caps']=[{'codes':['TEST'],'max_abs_points':2}]
        self.assertIn('cap_exceeded:TEST',s.score(d)['blockers'])

    def test_source_required(self):
        d=scored();d['rules']['test-rule'].pop('source')
        self.assertEqual(s.score(d)['net_points'],'0')

    def test_snv_boundaries(self):
        for pts,expected in [('10','P_range'),('9','LP_range'),('6','LP_range'),('5','VUS_range'),('0','VUS_range'),('-1','LB_range'),('-6','LB_range'),('-7','B_range')]:
            with self.subTest(pts=pts):self.assertEqual(s.score(scored(pts))['sandbox_partition'],expected)

    def test_cnv_boundaries(self):
        for f in ['CNV_LOSS','CNV_GAIN']:
            for pts,expected in [('.99','P_range'),('.98','LP_range'),('.90','LP_range'),('.89','VUS_range'),('-.89','VUS_range'),('-.90','LB_range'),('-.98','LB_range'),('-.99','B_range')]:
                with self.subTest(f=f,pts=pts):self.assertEqual(s.score(scored(pts,f))['sandbox_partition'],expected)

    def test_nan_rejected(self):
        with self.assertRaises(ValueError):s.score(scored('NaN'))

    def test_no_evidence_not_vus(self):
        d=scored();d['evidence']=[];self.assertIsNone(s.score(d)['sandbox_partition'])

    def test_rule_cannot_approve_different_code(self):
        d=scored();d['evidence'][0]['code']='PVS1'
        self.assertEqual(s.score(d)['excluded'][0]['reason'],'rule_code_mismatch')

    def test_string_source_ids_rejected(self):
        d=scored();d['evidence'][0]['source_ids']='not-a-list'
        self.assertEqual(s.score(d)['net_points'],'0')

class IntervalTests(unittest.TestCase):
    def setUp(self):
        self.region={'build':'GRCh38','chr':'1','start':101,'end':200,'system':'one_based_closed'}
    def test_coordinate_conventions(self):
        q=dict(self.region,start=100,system='zero_based_half_open')
        self.assertEqual(c.overlap(q,self.region)['overlap_bp'],100)
    def test_partial_not_complete(self):
        q=dict(self.region,start=102)
        self.assertFalse(c.overlap(q,self.region)['fully_covers_region'])
    def test_touching_not_overlap(self):
        q=dict(self.region,start=201,end=300)
        self.assertEqual(c.overlap(q,self.region)['overlap_bp'],0)
    def test_build_mismatch(self):
        with self.assertRaises(ValueError):c.overlap(dict(self.region,build='GRCh37'),self.region)
    def test_invalid_bounds(self):
        for start,end in [(0,100),(100,99),(True,100)]:
            with self.subTest(start=start,end=end),self.assertRaises(ValueError):c.normalize(dict(self.region,start=start,end=end))
    def test_geometry_never_assigns_code(self):
        self.assertIsNone(c.overlap(self.region,self.region)['evidence_code'])

class ArchiveTests(unittest.TestCase):
    def test_original_hashes(self):
        for item in json.loads((ROOT/'review/source-manifest.json').read_text()):
            self.assertEqual(hashlib.sha256((ROOT/item['file']).read_bytes()).hexdigest(),item['sha256'])
    def test_every_nonblank_line_mapped_exactly_once(self):
        entries=json.loads((ROOT/'review/feature-map.json').read_text());actual={(x['original_file'],x['line']) for x in entries}
        self.assertEqual(len(entries),len(actual))
        expected=set()
        for item in json.loads((ROOT/'review/source-manifest.json').read_text()):
            for n,line in enumerate((ROOT/item['file']).read_text().splitlines(),1):
                if line.strip():expected.add((item['file'],n))
        self.assertEqual(actual,expected)
        for x in entries:self.assertEqual((ROOT/x['original_file']).read_text().splitlines()[x['line']-1],x['original_text'])
    def test_single_discoverable_skill(self):
        self.assertEqual(list(ROOT.rglob('SKILL.md')),[ROOT/'SKILL.md'])

if __name__=='__main__':unittest.main()
