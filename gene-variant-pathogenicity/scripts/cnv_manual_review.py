"""Local workflow completeness gate, not a new medical rule or reviewer authentication."""
import hashlib,json
TOPICS={
 'scope':['constitutional_scope','clinical_question','applicable_rules'],
 'coordinates':['assembly_and_convention','interval_and_uncertainty','assay_quality'],
 'annotation':['genes_and_regions','transcripts_exons_utr','functional_consequences'],
 'dosage':['hi_ts_axis','assessment_date_and_new_evidence','benign_evidence'],
 'section1':['content','selected_and_rejected_items'],
 'section2':['all_targets','opposing_evidence','single_contribution_rationale'],
 'section3':['coding_gene_count','counting_method_and_exceptions'],
 'section4':['search_scope_and_results','case_comparability','phenotype_match','case_deduplication','population_4O','skip_conditions'],
 'section5':['parental_testing','phenotype_and_pedigree','inheritance_certainty','overlap_with_section4'],
 'integration':['mutual_exclusions','caps','evidence_independence','conflicts'],
 'limitations':['missing_information','service_failures','impact_on_conclusion','follow_up'],
 'report':['five_sections_accounted','variant_vs_patient_relevance','candidate_and_limitations']}

def digest(d):
    payload={k:v for k,v in d.items() if k!='manual_review'}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def blank(d):
    return dict(schema_version='1',input_sha256=digest(d),identity=d['identity'],reviewer='',reviewer_role='human_professional',reviewed_at='',
        sections={k:dict(status='pending',conclusion='',source='',location='',checks={c:'' for c in checks},evidence_ids=[],exclusions=[],unresolved_issues=[]) for k,checks in TOPICS.items()})

def nonempty(x):return isinstance(x,str) and bool(x.strip())

def validate(d):
    r=d.get('manual_review');b=[]
    if not isinstance(r,dict):return ['manual_review_missing']
    if r.get('schema_version')!='1':b.append('manual_review_schema')
    if r.get('input_sha256')!=digest(d):b.append('manual_review_stale_input')
    if r.get('identity')!=d.get('identity'):b.append('manual_review_identity')
    expected_role='deepseek_harness_assistant' if d.get('review_mode')=='autonomous_assist' else 'human_professional'
    if r.get('reviewer_role')!=expected_role or not all(nonempty(r.get(k)) for k in ['reviewer','reviewed_at']):b.append('manual_review_human_signoff_missing')
    sections=r.get('sections',{})
    if not isinstance(sections,dict):return b+['manual_review_sections_invalid']
    if set(sections)!=set(TOPICS):b.append('manual_review_section_inventory')
    for key,checks in TOPICS.items():
        s=sections.get(key,{})
        if not isinstance(s,dict):b.append('manual_review_invalid:'+key);continue
        if s.get('status') not in ['reviewed','not_applicable']:b.append('manual_review_incomplete:'+key)
        if not all(nonempty(s.get(k)) for k in ['conclusion','source','location']):b.append('manual_review_provenance:'+key)
        c=s.get('checks',{})
        if not isinstance(c,dict) or any(not nonempty(c.get(x)) for x in checks):b.append('manual_review_checks:'+key)
        if s.get('status')=='not_applicable' and not all(nonempty(s.get(k)) for k in ['applicability_rule','applicability_location']):b.append('manual_review_na_rule:'+key)
        if s.get('unresolved_issues')!=[]:b.append('manual_review_unresolved:'+key)
        exclusions=s.get('exclusions')
        if not isinstance(exclusions,list) or any(not isinstance(x,dict) or not all(nonempty(x.get(k)) for k in ['item','reason','source','location']) for x in exclusions):b.append('manual_review_exclusions:'+key)
        ids=s.get('evidence_ids')
        if not isinstance(ids,list) or any(not nonempty(x) for x in ids) or len(ids)!=len(set(ids)):b.append('manual_review_evidence_ids:'+key);continue
        if key in ['section1','section3','section4','section5']:
            n=key[-1];expected=[row.get('id') for row in d['scoring'].get('evidence',[]) if str(row.get('code','')).startswith(n)]
            if set(ids)!=set(expected):b.append('manual_review_evidence_coverage:'+key)
        elif key=='section2' and ids!=['cnv-section2']:b.append('manual_review_evidence_coverage:section2')
        if s.get('status')=='not_applicable' and ids:b.append('manual_review_na_has_evidence:'+key)
    return b

if __name__=='__main__':
    import argparse
    from pathlib import Path
    p=argparse.ArgumentParser();p.add_argument('case');p.add_argument('--template',required=True);a=p.parse_args()
    d=json.loads(Path(a.case).read_text());Path(a.template).write_text(json.dumps(blank(d),ensure_ascii=False,indent=2)+'\n')
