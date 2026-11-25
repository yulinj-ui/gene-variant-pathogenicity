#!/usr/bin/env python3
"""Offline, gated review calculations; never issue evidence or final classification."""
import argparse
import json
from decimal import Decimal
from pathlib import Path
from score import decimal

SOURCES = {
 'pm3': 'https://www.clinicalgenome.org/site/assets/files/3717/svi_proposal_for_pm3_criterion_-_version_1.pdf',
 'pp1pp4': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10806742/',
 'functional': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6938631/'}


def result(kind, blockers, **values):
    return dict(tool=kind, source=SOURCES[kind], status='blocked' if blockers else 'test_calculation_only',
                blockers=blockers, evidence_code=None, classification=None, **values)


def reviewed_gate(gate, fields):
    if not isinstance(gate, dict): return ['review_record_missing']
    missing = [k for k in fields if gate.get(k) is not True]
    missing += [k for k in ('reviewer', 'reviewed_at', 'source', 'rationale')
                if not isinstance(gate.get(k), str) or not gate[k].strip()]
    return ['unreviewed:'+k for k in missing]


def pm3(data):
    """SVI 2019 Table 1/2. Family independence/phase must be reviewed upstream."""
    blockers = reviewed_gate(data.get('review'), ['recessive_disease', 'disease_applicability',
        'frequency_threshold_validated', 'case_independence_reviewed', 'vcep_checked'])
    rows = data.get('cases')
    if not isinstance(rows, list): raise ValueError('cases must be a list')
    seen, families, audit = set(), set(), []
    sums = {k:Decimal(0) for k in ('plp','homozygous','vus')}
    for row in rows:
        if not isinstance(row, dict): raise ValueError('case must be an object')
        identity, family = row.get('id'), row.get('family_id')
        if not isinstance(identity,str) or not identity.strip() or identity in seen:
            raise ValueError('missing/duplicate case id')
        if not isinstance(family,str) or not family.strip() or family in families:
            raise ValueError('missing/duplicate family id; family aggregation requires review')
        seen.add(identity); families.add(family)
        failures = reviewed_gate(row.get('review'), ['affected', 'target_rare', 'partner_rare',
            'independent_partner_classification', 'phase_or_homozygosity_reviewed'])
        if not isinstance(row.get('source_ids'),list) or not row['source_ids'] or not all(isinstance(x,str) and x.strip() for x in row['source_ids']):
            failures.append('source_ids_missing')
        phase, partner = row.get('phase'), row.get('partner_class')
        if phase not in ('trans','unknown','homozygous'): raise ValueError('unsupported phase')
        if phase == 'homozygous': category, points = 'homozygous',Decimal('.5')
        else:
            if partner not in ('P','LP','VUS'): raise ValueError('unsupported partner classification')
            if not isinstance(row.get('partner_variant_id'),str) or not row['partner_variant_id'].strip():
                failures.append('partner_variant_id_missing')
            category = 'vus' if partner == 'VUS' else 'plp'
            points = {'P':Decimal(1),'LP':Decimal('.5'),'VUS':Decimal('.25')}[partner] if phase == 'trans' else {'P':Decimal('.5'),'LP':Decimal('.25'),'VUS':Decimal(0)}[partner]
        blockers.extend(identity+':'+x for x in failures)
        if not failures: sums[category] += points
        audit.append({'id':identity,'category':category,'case_points':str(points) if not failures else None,'blockers':failures})
    if not rows: blockers.append('no_cases')
    total = sums['plp'] + min(sums['homozygous'],Decimal(1)) + min(sums['vus'],Decimal('.5'))
    strength = next((s for cutoff,s in [(4,'VeryStrong'),(2,'Strong'),(1,'Moderate'),(Decimal('.5'),'Supporting')] if total>=cutoff),None)
    return result('pm3',blockers,case_audit=audit,uncapped_subtotals={k:str(v) for k,v in sums.items()},
                  case_points=None if blockers else str(total), strength=None if blockers else strength,
                  bayesian_weight=None if blockers or strength is None else {'Supporting':1,'Moderate':2,'Strong':4,'VeryStrong':8}[strength])


def pp1pp4(data):
    """Table 4 lookup ONLY; no pedigree, probability apportionment, or code selection."""
    blockers = reviewed_gate(data.get('review'), ['applicability_reviewed','phase_reviewed',
       'penetrance_reviewed','independence_reviewed','probability_allocation_reviewed','cap_reviewed'])
    n=decimal(data.get('joint_points'))
    if n<0 or n>5: raise ValueError('only reviewed, apportioned, capped points in [0,5] accepted')
    if n*10 != (n*10).to_integral_value(): raise ValueError('Table 4 input must use at most one decimal place; rounding is not automated')
    options=[[],[['PP1_Supporting'],['PP4_Supporting']],
       [['PP1_Moderate'],['PP4_Moderate'],['PP1_Supporting','PP4_Supporting']],
       [['PP1_Supporting','PP4_Moderate'],['PP4_Supporting','PP1_Moderate']],
       [['PP1_Strong'],['PP4_Strong'],['PP1_Moderate','PP4_Moderate']],
       [['PP1_Strong','PP4_Supporting'],['PP4_Strong','PP1_Supporting']]][int(n)]
    return result('pp1pp4',blockers,reviewed_joint_points=str(n),
        maximum_code_options=None if blockers else options, selected_codes=None,
        automatic_score_import=False, note='Code choice and complete 2024 workflow remain disabled; never add raw points and converted weights together')


def functional(data):
    """Brnich Table 3 lookup only, after assay review; controls do not assign strength."""
    blockers=reviewed_gate(data.get('review'), ['mechanism_matched','assay_validated',
       'controls_independently_classified','replicates_reviewed','calibration_reviewed','vcep_checked'])
    if data.get('odds_path') is None:
        return result('functional',blockers+['calibrated_OddsPath_missing'],band=None)
    n=decimal(data['odds_path'])
    if n<=0: raise ValueError('OddsPath must be positive and finite')
    # Retain the printed strict inequalities: equality falls to the next weaker band.
    if n>350: band='PS3_VeryStrong'
    elif n>Decimal('18.7'): band='PS3_Strong'
    elif n>Decimal('4.3'): band='PS3_Moderate'
    elif n>Decimal('2.1'): band='PS3_Supporting'
    elif n<Decimal('.053'): band='BS3_Strong'
    elif n<Decimal('.23'): band='BS3_Moderate'
    elif n<Decimal('.48'): band='BS3_Supporting'
    else: band='Indeterminate'
    return result('functional',blockers,band=None if blockers else band,odds_path=str(n))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('mode',choices=list(SOURCES));ap.add_argument('input_json');a=ap.parse_args()
    try:
        d=json.loads(Path(a.input_json).read_text())
        print(json.dumps({'pm3':pm3,'pp1pp4':pp1pp4,'functional':functional}[a.mode](d),ensure_ascii=False,indent=2))
    except (ValueError,TypeError,KeyError) as e: ap.error(str(e))
