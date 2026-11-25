"""Reviewed helper admission, mandatory case-specific rule routing, candidate audit.
No automatic clinical signoff. Run input.json; all calculations recomputed locally.
"""
import argparse,copy,json,re
from pathlib import Path
from score import score
from compare_frameworks import decode
from pvs1_review import evaluate as pvs1
from review_helpers import pm3,functional,pp1pp4
from locus_review import calculate as locus
from ba1_review import match as ba1_match
from evidence_lookup import ps1pm5,pm4,ps4,bs2,pp1_lod,ba1_threshold

def strings(v):return isinstance(v,list) and bool(v) and all(isinstance(x,str) and x.strip() for x in v) and len(v)==len(set(v))
def signed(r):
    return isinstance(r,dict) and r.get('approved') is True and all(isinstance(r.get(k),str) and r[k].strip() for k in ('reviewer','reviewed_at','source','location','rationale'))

def routing(identity,r):
    b=[]
    for k in ('variant_id','gene','disease','inheritance'):
        if not isinstance(identity.get(k),str) or not identity[k].strip():b.append('identity_missing:'+k)
        if r.get('identity',{}).get(k)!=identity.get(k):b.append('route_identity_mismatch:'+k)
    if not signed(r.get('review')):b.append('route_review_missing')
    searches=r.get('searches',[])
    if not searches or any(not all(x.get(k) for k in ('url','query','accessed_at','result')) for x in searches):b.append('VCEP_search_record_missing')
    if r.get('search_completed') is not True:b.append('VCEP_search_incomplete')
    status=r.get('outcome')
    if status not in ('applicable','none_found','not_applicable'):b.append('VCEP_status_unresolved')
    if status=='not_applicable' and (not r.get('excluded_candidates') or any(not all(x.get(k) for k in ('url','version','reason')) for x in r['excluded_candidates'])):b.append('VCEP_exclusion_reasons_missing')
    if status=='applicable':
        spec=r.get('specification',{})
        for k in ('url','version','gene','disease','inheritance','combining_rule_location'):
            if not spec.get(k):b.append('specification_missing:'+k)
        if spec.get('gene')!=identity.get('gene') or spec.get('disease')!=identity.get('disease') or spec.get('inheritance')!=identity.get('inheritance'):b.append('VCEP_scope_mismatch')
        if spec.get('release_status')!='released':b.append('VCEP_not_released')
        if spec.get('variant_scope_reviewed') is not True:b.append('VCEP_variant_scope_unreviewed')
        if spec.get('required_materials_complete') is not True:b.append('VCEP_full_materials_incomplete')
        docs=spec.get('documents',[])
        if not docs or any(not all(d.get(k) for k in ('url','version','location')) or d.get('full_text_reviewed') is not True or not re.fullmatch('[0-9a-f]{64}',str(d.get('sha256',''))) for d in docs):b.append('VCEP_full_text_provenance_missing')
    return b

ASSESSMENTS={
 'functional':['mechanism','assay_class','sample_system','controls','replicates','calibration','variant_readout','coverage_of_normal_result','conflict_resolution'],
 'pedigree':['pedigree','phenotypes_and_ages','genotypes_and_phase','inheritance','penetrance','phenocopies','ascertainment','independent_meioses','alternative_causes','method_and_source','probability_allocation','code_conversion'],
 'rna':['tissue_and_transcript','assay_design','controls','allelic_origin','nmd_inhibition','transcript_quantification','lof_consequences','rescue_transcripts','code_and_strength','overlap_with_predictions']}

def assessment(a,kind):
    b=[]
    if not signed(a.get('review')):b.append(kind+':review_missing')
    for k in ASSESSMENTS[kind]:
        x=a.get(k,{})
        if not all(isinstance(x.get(t),str) and x[t].strip() for t in ('finding','source','location','conclusion')):b.append(kind+':missing_'+k)
    if kind=='functional':
        if a.get('readout_kind')=='rna_splicing':b.append('RNA_must_use_splicing_workflow')
        if a.get('readout_kind') not in ('protein_function','cellular_function','organism_function'):b.append('functional_readout_unresolved')
        if a.get('conflict_status') not in ('none','resolved_by_better_validated_assay'):b.append('functional_conflict_unresolved')
        if a.get('variant_result') not in ('normal','abnormal'):b.append('functional_intermediate_requires_specialist_review')
    if kind=='pedigree' and a.get('complexity') not in ('simple_reviewed','specialist_model_reviewed'):b.append('pedigree_model_unreviewed')
    return b

def run(data):
    identity=data.get('identity',{});route=data.get('routing',{})
    blockers=routing(identity,route)
    scoring=copy.deepcopy(data.get('scoring',{}))
    if scoring.get('framework')!='SNV':raise ValueError('this bridge is SNV/Indel only; CNV stays independent')
    evidence=scoring.setdefault('evidence',[]);rules=scoring.get('rules',{})
    if any(r.get('admitted_from') or r.get('joint_allocation_id') for r in evidence):raise ValueError('preassembled admissions forbidden; supply original helper inputs')
    audits=[];seen={b for row in evidence for b in row.get('basis_ids',[])}
    admission_ids=set();assessment_map=copy.deepcopy(data.get('assessments',{}));pvs1_results=[]
    if not isinstance(assessment_map,dict):raise ValueError('assessments must be an object')
    for a in data.get('admissions',[]):
        aid=a.get('id');kind=a.get('kind');raw=a.get('input',{});codes=a.get('selected_codes')
        if not isinstance(aid,str) or not aid or aid in admission_ids:raise ValueError('missing/duplicate admission id')
        admission_ids.add(aid);ab=[]
        if a.get('identity')!=identity:ab.append('admission_identity_mismatch')
        if not signed(a.get('approval')):ab.append('admission_approval_missing')
        if not strings(codes):ab.append('selected_codes_missing')
        basis=a.get('basis_ids');src=a.get('source_ids')
        if not strings(basis) or not strings(src):ab.append('admission_provenance_missing')
        elif seen & set(basis):ab.append('underlying_evidence_already_used')
        if route.get('outcome')=='applicable' and not signed(a.get('vcep_adoption_review')):ab.append('generic_helper_not_approved_under_VCEP')
        result={};options=[]
        if kind=='pvs1':
            result=pvs1(raw);pvs1_results.append(result)
            if raw.get('identity',{}).get('variant_id')!=identity.get('variant_id') or raw.get('identity',{}).get('gene')!=identity.get('gene') or raw.get('identity',{}).get('disease')!=identity.get('disease') or raw.get('identity',{}).get('inheritance')!=identity.get('inheritance'):ab.append('PVS1_identity_mismatch')
            if set(raw.get('basis_ids',[]))!=set(basis or []):ab.append('PVS1_basis_mismatch')
            strength=result.get('adjusted_strength')
            if strength:options=[['PVS1_'+strength]]
        elif kind=='pm3':
            result=pm3(raw)
            if identity.get('inheritance')!='AR':ab.append('PM3_requires_AR_scope_in_this_bridge')
            if result.get('strength'):options=[['PM3_'+result['strength']]]
        elif kind=='functional':
            result=functional(raw);band=result.get('band')
            if band and band!='Indeterminate':options=[[band]]
        elif kind=='locus':
            result=locus(raw)
            packets=result.get('packets',[])
            if len(packets)!=1:ab.append('one_locus_packet_per_admission_required')
            else:
                p=packets[0]
                if p.get('mode')=='pp4_equal' and identity.get('inheritance')!='AR':ab.append('PP4_equal_requires_AR_scope')
                if p.get('subject_id')!=identity.get('subject_id'):ab.append('locus_subject_mismatch')
                if p.get('source',{}).get('gene')!=identity.get('gene') or p.get('source',{}).get('disease')!=identity.get('disease'):ab.append('locus_disease_mismatch')
                if set(p.get('basis_ids',[]))!=set(basis or []):ab.append('locus_basis_mismatch')
                selected=[v for v in p.get('results',[]) if v['variant_id']==identity.get('variant_id')]
                if len(selected)!=1:ab.append('locus_variant_mismatch')
                else:
                    gate={k:True for k in ['applicability_reviewed','phase_reviewed','penetrance_reviewed','independence_reviewed','probability_allocation_reviewed','cap_reviewed']}
                    gate.update(reviewer='computed-lookup',reviewed_at='source-version',source='Biesecker2024 Table4',rationale='lookup after existing packet review')
                    options=pp1pp4({'joint_points':selected[0]['review_points'],'review':gate})['maximum_code_options']
                    if p['mode']=='pp4_equal':options=[x for x in options if all(c.startswith('PP4_') for c in x)]
        elif kind=='ps1pm5':
            result=ps1pm5(raw)
            if result.get('code'):options=[[result['code']]]
        elif kind=='pm4':
            result=pm4(raw)
            if result.get('strength'):options=[['PM4' if result['strength']=='Moderate' else 'PM4_Supporting']]
        elif kind=='ps4':
            result=ps4(raw)
            if raw.get('mode')=='likelihood_ratio':
                if result.get('direction')=='benign':ab.append('PS4_benign_LR_has_no_standard_code')
                elif result.get('band'):options=[['PS4' if result['band']=='Strong' else 'PS4_'+result['band']]]
            elif raw.get('mode')=='proband_count':
                if result.get('strength'):options=[['PS4' if result['strength']=='Strong' else 'PS4_'+result['strength']]]
            else:ab.append('PS4_mode_unresolved')
        elif kind=='bs2':
            result=bs2(raw)
            if result.get('bs2_met'):options=[['BS2']]
        elif kind=='pp1_lod':
            result=pp1_lod(raw)
            if result.get('strength'):options=[['PP1_'+result['strength']]]
        else:raise ValueError('unsupported admission kind')
        if result.get('status')!='test_calculation_only':ab.append('helper_not_ready')
        if codes not in options:ab.append('selected_codes_not_supported_by_recalculation')
        if kind in ('functional','locus','pp1_lod'):
            ak='functional' if kind=='functional' else 'pedigree'
            ab+=assessment(a.get('assessment',{}),ak)
            if kind=='functional' and codes:
                expected='normal' if codes[0].startswith('BS3') else 'abnormal'
                if a.get('assessment',{}).get('variant_result')!=expected:ab.append('functional_direction_mismatch')
        audit=dict(id=aid,kind=kind,recomputed=result,selected_codes=codes,blockers=ab,basis_ids=basis,source_ids=src)
        audits.append(audit)
        if ab:blockers.extend(aid+':'+x for x in ab);continue
        seen.update(basis)
        for index,code in enumerate(codes):
            rid=a.get('rule_ids',{}).get(code)
            if rid not in rules or rules[rid].get('code')!=code:blockers.append(aid+':approved_scoring_rule_missing');continue
            eid='admitted:'+aid+':'+str(index)
            # Table4 two-code options are one bounded joint allocation, never two independent raw sums.
            derived=basis if len(codes)==1 else ['joint-allocation:'+aid+':'+code]
            evidence.append(dict(id=eid,framework='SNV',rule_id=rid,code=code,points=decode(code)[1],
                status='reviewed',gate='passed',source_ids=src,basis_ids=derived,
                underlying_basis_ids=basis,joint_allocation_id=aid if len(codes)>1 else None,
                mechanism=a.get('mechanism'),rationale=a['approval']['rationale'],admitted_from=aid))
            if kind in ('functional','locus','pp1_lod'):assessment_map[eid]=a['assessment']
    for row in evidence:
        base=row.get('code','').split('_')[0];rid=row.get('rule_id');rule=rules.get(rid,{})
        if route.get('outcome')=='applicable':
            spec=route.get('specification',{})
            if rule.get('specification_version')!=spec.get('version') or rule.get('specification_url')!=spec.get('url'):blockers.append(row['id']+':rule_not_bound_to_selected_VCEP')
        kind='functional' if base in ('PS3','BS3') else 'pedigree' if base in ('PP1','PP4','BS4') else 'rna' if row.get('mechanism')=='rna_splicing' and base in ('PVS1','BP7') else None
        if kind:
            a=assessment_map.get(row['id'],{})
            blockers += [row['id']+':'+b for b in assessment(a,kind)]
            if kind=='functional' and a.get('variant_result')!=('normal' if base=='BS3' else 'abnormal'):blockers.append(row['id']+':functional_direction_mismatch')
    if len(pvs1_results)>1:blockers.append('multiple_PVS1_admissions_require_single_mechanism_review')
    result=score(scoring, pvs1_review=(pvs1_results[0] if len(pvs1_results)==1 else None), enforce_pvs1_provenance=True)
    blockers+=result['blockers']
    families={r.get('code','').split('_')[0] for r in evidence}
    if {'PP1','BS4'} <= families:blockers.append('PP1_BS4_requires_unified_specialist_model_not_parallel_codes')
    if {'PS3','BS3'} <= families:blockers.append('PS3_BS3_conflicting_directions_not_stackable')
    if any(r.get('mechanism')=='rna_splicing' and r.get('code','').split('_')[0] in ('PVS1','BP7') for r in evidence):
        for row in evidence:
            if row.get('code','').split('_')[0] in ('PP3','BP4') and row.get('mechanism')!='independent_protein_effect':blockers.append('RNA_prediction_overlap_or_unknown')
    ba=ba1_match(data['ba1_identity']) if 'ba1_identity' in data else None
    ba_thr=ba1_threshold(data['ba1_threshold']) if 'ba1_threshold' in data else None
    authoritative=None
    if route.get('outcome')=='applicable':
        decision=data.get('vcep_combination_review',{})
        if not signed(decision) or decision.get('candidate') not in ('P','LP','VUS','LB','B') or not decision.get('matched_rules') or sorted(decision.get('evidence_ids',[]))!=sorted(r['id'] for r in result['accepted']):blockers.append('VCEP_combination_review_missing_or_mismatched')
        else:authoritative=decision['candidate']
    elif not blockers:authoritative=result['point_candidate']
    if blockers:authoritative=None
    return dict(status='blocked' if blockers else 'reviewed_candidate_only',classification=None,
        authoritative_candidate=authoritative,authoritative_framework='VCEP_reviewed_combination' if route.get('outcome')=='applicable' else 'Tavtigian_2020_points',
        routing=route,score_comparison=result,admission_audit=audits,ba1_exception_check=ba,ba1_threshold_check=ba_thr,
        blockers=blockers,assembled_scoring=scoring,limitations=['Review attestations are not authentication or clinical validation','VCEP combination candidate is manually reviewed, not universally computed','BA1 matcher does not issue a benign classification','BA1 threshold check does not auto-issue a benign classification'])
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args()
    print(json.dumps(run(json.loads(Path(a.input).read_text())),ensure_ascii=False,indent=2))
