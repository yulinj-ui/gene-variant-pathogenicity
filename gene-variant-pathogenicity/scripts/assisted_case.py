"""Autonomous evidence disposition for external-report assistance, without human impersonation.
Medical applicability is reasoned by the agent from cited sources; this gate validates records.
"""
import copy,json,argparse
from pathlib import Path
from case_pipeline import run as snv_run
from cnv_case import run as cnv_run

def text(x):return isinstance(x,str) and bool(x.strip())

def run(d):
    case=copy.deepcopy(d['case']);framework=d.get('framework');a=d.get('assessment',{});blocks=[]
    if framework not in ('SNV','CNV'):raise ValueError('framework must be SNV or CNV')
    if a.get('performed_by')!='DeepSeek Harness' or a.get('review_type')!='autonomous_assist':blocks.append('assessment_actor_missing')
    if a.get('identity')!=case.get('identity'):blocks.append('assessment_identity_mismatch')
    for k in ['variant_identity','disease_mechanism','phenotype_fit','rule_search','pathogenic_evidence_search','benign_evidence_search','independence','external_report_comparison','limitations']:
        row=a.get(k,{})
        if not isinstance(row,dict) or not all(text(row.get(x)) for x in ['finding','source','rationale']):blocks.append('assessment_missing:'+k)
    # Only genuine critical problems stop the overall assessment. Individual unavailable codes are omitted.
    if not isinstance(a.get('critical_issues'),list):blocks.append('critical_issues_inventory_missing')
    else:blocks.extend('critical:'+str(x) for x in a['critical_issues'])
    decisions=a.get('decisions',[])
    if not isinstance(decisions,list):raise ValueError('decisions must be list')
    selected=[];ids=set()
    for row in decisions:
        rid=row.get('id')
        if not text(rid) or rid in ids:raise ValueError('decision ID missing or duplicated')
        ids.add(rid)
        if row.get('disposition') not in ('include','exclude','unavailable','not_applicable'):blocks.append('invalid_disposition:'+rid)
        if not all(text(row.get(k)) for k in ['code','finding','source','rationale']):blocks.append('decision_provenance_missing:'+rid)
        if row.get('origin') not in ('public_primary','external_report_explicit','user_history','unverified_assumption','external_classification'):blocks.append('invalid_origin:'+rid)
        if row.get('disposition')=='include':
            selected.append(rid)
            if row.get('origin') in ('unverified_assumption','external_classification'):blocks.append('unsupported_evidence_origin:'+rid)
            if not text(row.get('applicability')):blocks.append('evidence_applicability_missing:'+rid)
    # The caller constructs transparent agent reviews in the ordinary pipeline. No fabricated human signature.
    scoring=case.get('scoring',{})
    assembled_ids=[r.get('id') for r in scoring.get('evidence',[])]+[r.get('id') for r in case.get('admissions',[])]
    if framework=='CNV':assembled_ids+=['cnv-section2']
    if set(selected)!=set(assembled_ids):blocks.append('decision_scoring_coverage_mismatch')
    main_codes={r.get('id'):r.get('code') for r in scoring.get('evidence',[])}
    for row in decisions:
        if row.get('disposition')=='include' and row.get('id') in main_codes and row.get('code')!=main_codes[row['id']]:blocks.append('decision_code_mismatch:'+row['id'])
    for review in [case.get('routing',{}).get('review'),case.get('integration_review'),case.get('vcep_combination_review')]+[x.get('approval') for x in case.get('admissions',[])]:
        if review is not None and review.get('reviewer')!='DeepSeek Harness (autonomous evidence review)':blocks.append('misleading_reviewer_identity')
    if framework=='CNV':
        case['review_mode']='autonomous_assist'
        mr=case.get('manual_review',{})
        if mr.get('reviewer_role')!='deepseek_harness_assistant' or mr.get('reviewer')!='DeepSeek Harness (autonomous evidence review)':blocks.append('CNV_agent_review_identity')
    result=snv_run(case) if framework=='SNV' else cnv_run(case)
    blocks+=result['blockers']
    grade=None if blocks else result['authoritative_candidate']
    return dict(status='assessment_incomplete' if blocks else 'independent_assisted_assessment',
        independent_classification=grade,clinical_signoff=None,
        evidence_points=None if blocks else result['score_comparison']['net_points'],
        acmg_2015_comparison=result['score_comparison']['acmg_2015_comparison'],
        authoritative_framework=result['authoritative_framework'],
        assessment=a,pipeline=result,blockers=blocks,
        limitations=['Agent assessment is not a laboratory signoff','Public evidence review cannot authenticate external sample quality','Unscored evidence is not benign evidence; no forced grade for missing critical facts'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('input');a=p.parse_args();print(json.dumps(run(json.loads(Path(a.input).read_text())),ensure_ascii=False,indent=2))
