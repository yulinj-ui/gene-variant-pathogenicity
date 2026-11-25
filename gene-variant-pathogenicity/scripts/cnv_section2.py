"""Riggs Section 2 review on sourced facts. Not a coordinate annotation engine.
One target/scenario per call; candidate only, never final CNV classification.
"""
import argparse,json,re
from pathlib import Path
from decimal import Decimal
from case_pipeline import signed
from pvs1_review import evaluate as pvs1

TABLE=json.loads((Path(__file__).resolve().parents[1]/'references/cnv-section2-rules.json').read_text())
class Pending(Exception):pass
def fact(d,k,allowed):
    v=d.get(k)
    if v is None or v=='unknown':raise Pending('missing_or_unknown:'+k)
    if allowed==(True,False) and type(v) is not bool:raise ValueError('strict bool required:'+k)
    if v not in allowed:raise ValueError('invalid '+k)
    return v
def num(v):
    if not isinstance(v,str):raise ValueError('decimal string required')
    n=Decimal(v)
    if not n.is_finite():raise ValueError('finite decimal required')
    return n
def established(d,axis):
    dosage=d.get('dosage',{})
    if dosage.get('axis')!=axis or type(dosage.get('score')) is not int or dosage['score']!=3:raise Pending('established_'+axis+'_score3_required')
    if not all(dosage.get(k) for k in ['source','record_id','evaluated_at','current_evidence_review']):raise Pending('dosage_provenance_missing')
def benign(d):
    dosage=d.get('dosage',{})
    if dosage.get('assessment')!='dosage_sensitivity_unlikely':raise Pending('established_benign_assessment_required_not_frequency')
    if 'score' in dosage and (type(dosage['score']) is not int or dosage['score']!=40):raise Pending('benign_assessment_conflicts_with_numeric_score')
    if dosage.get('axis')!=('HI' if d['cnv_type']=='LOSS' else 'TS'):raise Pending('benign_dosage_axis_mismatch')
    if not all(dosage.get(k) for k in ['source','record_id','evaluated_at','current_evidence_review']):raise Pending('benign_provenance_missing')

def route(d):
    typ=d['cnv_type'];rel=d['relation'];f=d.get('facts',{});obj=d.get('target_kind')
    if obj not in ('gene','region'):raise ValueError('target_kind must be gene or region')
    if rel=='full_cover':
        established(d,'HI' if typ=='LOSS' else 'TS');return '2A',None
    if rel=='partial_region':
        if obj!='region':raise ValueError('partial_region requires region')
        established(d,'HI' if typ=='LOSS' else 'TS')
        inclusion=fact(f,'critical_region_status',('not_included','uncertain','not_established','fully_included'))
        if inclusion=='fully_included':raise Pending('reidentify_fully_contained_critical_target_before_2A')
        return '2B',None
    if rel.startswith('benign_'):
        benign(d)
        if typ=='LOSS':
            if rel=='benign_contained':return '2F',None
            if rel=='benign_extra_material':return '2G',None
        else:
            if rel=='benign_identical_content':return '2C',None
            if rel=='benign_smaller':return ('2E' if fact(f,'coding_gene_interrupted',(True,False)) else '2D'),None
            if rel=='benign_larger_no_extra_coding':return '2F',None
            if rel=='benign_extra_material':return '2G',None
        raise ValueError('benign relation not valid for event type')
    if rel=='predicted_hi':
        if typ!='LOSS':raise ValueError('HI prediction is only LOSS 2H')
        if obj!='gene':raise ValueError('2H predictor values must refer to the same candidate gene')
        if d.get('target_clinical_significance')!='uncertain':raise Pending('2H_only_uncertain_genes')
        if d.get('dosage',{}).get('axis')=='HI' and d.get('dosage',{}).get('score')==3:raise Pending('2H_cannot_replace_established_HI')
        if d.get('applied_hi_categories') is None:raise Pending('2H_prior_categories_missing')
        if not isinstance(d['applied_hi_categories'],list) or any(not isinstance(c,str) for c in d['applied_hi_categories']):raise ValueError('applied_hi_categories must be a list of code strings')
        if any(c in ['2A','2B','2C-1','2C-2','2D-1','2D-2','2D-3','2D-4','2E'] for c in d['applied_hi_categories']):raise Pending('2H_not_additive_to_established_HI_evidence')
        profile=f.get('predictor_profile')
        if profile not in ('Riggs2020_original','ClinGen_current_v4'):raise Pending('predictor_profile_unsupported')
        if not all(f.get(k) for k in ('gnomad_source_version','decipher_source_version','metric_equivalence_review')):raise Pending('predictor_versions_or_metric_mapping_missing')
        pli=num(f.get('pli'))
        if not (0<=pli<=1):raise ValueError('invalid pLI range')
        if profile=='Riggs2020_original':
            oe=num(f.get('oe_upper'));hi=num(f.get('decipher_hi_percent'))
            if not (oe>=0 and 0<=hi<=100):raise ValueError('invalid predictor range')
            if not (pli>=Decimal('.9') and oe<Decimal('.35') and hi<=10):raise Pending('2H_threshold_not_met_no_evidence')
        else:
            loeuf=num(f.get('loeuf'));phaplo=num(f.get('phaplo'))
            if not (0<=loeuf<=1 and 0<=phaplo<=1):raise ValueError('invalid predictor range')
            if not (pli>=Decimal('.9') and loeuf<Decimal('.6') and phaplo>=Decimal('.86')):raise Pending('2H_threshold_not_met_no_evidence')
        return '2H',None
    if rel=='intragenic':
        if obj!='gene':raise ValueError('intragenic requires gene')
        established(d,'HI')
        if typ=='GAIN' and fact(f,'terminal_coding_exon_involved',(True,False)):
            if not signed(d.get('terminal_duplication_review')):raise Pending('terminal_duplication_structure_review_required_not_automatically_benign')
        raw=d.get('pvs1_input')
        if not isinstance(raw,dict):raise Pending('pvs1_raw_input_missing')
        if raw.get('mechanism',{}).get('lof_mechanism')!='established':raise Pending('intragenic_LoF_mechanism_not_established')
        if raw.get('kind')!=('deletion' if typ=='LOSS' else 'duplication'):raise ValueError('PVS1_kind_mismatch')
        identity=d.get('identity',{})
        for k in ['variant_id','gene','disease','inheritance','build']:
            if raw.get('identity',{}).get(k)!=identity.get(k):raise ValueError('PVS1_identity_mismatch:'+k)
        if set(raw.get('basis_ids',[]))!=set(d.get('basis_ids',[])):raise ValueError('PVS1_basis_mismatch')
        if f.get('frame_status')=='unknown':
            if typ!='LOSS' or d.get('uncertainty_strategy')!='conservative_in_frame' or not signed(d.get('assumption_review')):raise Pending('frame_unknown_requires_reviewed_conservative_scenario')
            if any(s.get('facts',{}).get('consequence')!='in_frame' for s in raw.get('scenarios',[])):raise ValueError('unknown_frame_cannot_use_out_of_frame_scenario')
        elif f.get('frame_status') not in ('in_frame','out_of_frame','not_applicable'):raise Pending('frame_status_missing')
        elif typ=='LOSS':
            consequences=[s.get('facts',{}).get('consequence') for s in raw.get('scenarios',[])]
            if f['frame_status']=='in_frame' and any(c!='in_frame' for c in consequences):raise ValueError('known_frame_consequence_mismatch')
            if f['frame_status']=='out_of_frame' and any(c not in ('out_of_frame_nmd','out_of_frame_no_nmd') for c in consequences):raise ValueError('known_frame_consequence_mismatch')
        result=pvs1(raw)
        if result['status']=='blocked':raise Pending('PVS1_blocked:'+','.join(result['blockers']))
        strength=result.get('adjusted_strength') if result['status']=='test_calculation_only' else 'NA'
        if strength not in TABLE[typ]['2E' if typ=='LOSS' else '2I']['mapping']:raise Pending('PVS1_strength_not_mapped_in_CNV_table')
        return ('2E' if typ=='LOSS' else '2I'),dict(strength=strength,pvs1=result)
    if typ=='LOSS':
        established(d,'HI')
        if obj!='gene':raise ValueError('partial_gene requires gene')
        if rel in ('five_prime','three_prime'):
            if d.get('platform_resolution_sufficient') is not True:raise Pending('2C_2D_platform_resolution_insufficient')
            if not re.search(r'\.\d+$',str(d.get('transcript_version',''))) or not d.get('transcript_choice_rationale'):raise Pending('transcript_version_or_choice_missing')
        if rel=='five_prime':
            coding=fact(f,'coding_sequence_involved',(True,False))
            if coding:
                fact(f,'alternative_start',(True,False));fact(f,'spared_functional_isoform',(True,False))
                return '2C-1',None
            return '2C-2',None
        if rel=='three_prime':
            if fact(f,'utr_only',(True,False)):return '2D-1',None
            if fact(f,'last_exon_only',(True,False)):
                if fact(f,'last_exon_critical',(True,False)):return '2D-2',None
                if f.get('critical_evidence_search_complete') is not True:raise Pending('absence_of_last_exon_evidence_not_reviewed')
                return '2D-3',None
            if f.get('last_and_other_exons') is not True or f.get('nmd_expected') is not True:raise Pending('2D4_requires_other_exons_and_NMD')
            return '2D-4',None
    else:
        if rel=='full_hi_gene':
            if obj!='gene':raise ValueError('full_hi_gene requires gene')
            established(d,'HI');return '2H',None
        if rel=='one_breakpoint_hi':
            if obj!='gene':raise ValueError('one_breakpoint_hi requires gene')
            established(d,'HI')
            phenotype=fact(f,'phenotype',('highly_specific_consistent','inconsistent','unknown_phenotype','consistent_nonspecific'))
            if phenotype=='consistent_nonspecific':raise Pending('2J_2K_intermediate_phenotype_requires_review')
            return ('2K' if phenotype=='highly_specific_consistent' else '2J'),None
        if rel=='breakpoint_uncertain_gene':
            if obj!='gene':raise ValueError('2L requires gene')
            if d.get('target_clinical_significance')!='uncertain':raise Pending('2L_requires_uncertain_gene')
            if d.get('dosage',{}).get('score')==3:raise Pending('2L_conflicts_with_established_dosage')
            return '2L',None
    raise ValueError('relation not supported for event type')

def evaluate(d):
    allowed={'cnv_type','identity','target_id','target_kind','relation','facts','dosage','review','fact_sources','basis_ids','target_clinical_significance','applied_hi_categories','platform_resolution_sufficient','transcript_version','transcript_choice_rationale','pvs1_input','uncertainty_strategy','assumption_review','assigned_points','adjustment_review','terminal_duplication_review'}
    if not isinstance(d,dict) or set(d)-allowed:raise ValueError('unknown Section2 input fields')
    if d.get('cnv_type') not in ('LOSS','GAIN'):raise ValueError('LOSS or GAIN required')
    b=[]
    if not signed(d.get('review')):b.append('section2_review_missing')
    for k in ['variant_id','build','disease','inheritance']:
        if not d.get('identity',{}).get(k):b.append('identity_missing:'+k)
    if d.get('identity',{}).get('build') not in ('GRCh37','GRCh38'):b.append('unsupported_build')
    if not d.get('target_id'):b.append('target_id_missing')
    if d.get('target_kind')=='gene' and not d.get('identity',{}).get('gene'):b.append('target_gene_identity_missing')
    if not isinstance(d.get('basis_ids'),list) or not d['basis_ids'] or any(not isinstance(x,str) or not x for x in d['basis_ids']) or len(set(d['basis_ids']))!=len(d['basis_ids']):b.append('invalid_basis_ids')
    for k in ['interval_and_breakpoints','target_geometry','dosage','transcript_and_function','platform']:
        src=d.get('fact_sources',{}).get(k,{})
        if not all(src.get(t) for t in ('source','location','rationale')):b.append('fact_source_missing:'+k)
    out=dict(status='blocked',blockers=b,code=None,default_points=None,allowed_range=None,assigned_points=None,classification=None,automatic_score_import=False)
    try:
        code,detail=route(d);rule=TABLE[d['cnv_type']][code]
        if detail:rule=rule['mapping'][detail['strength']]
        out.update(code=code,default_points=rule['default'],allowed_range=[rule['min'],rule['max']],pvs1_audit=detail)
        chosen=d.get('assigned_points',rule['default']);value=num(chosen)
        if not num(rule['min'])<=value<=num(rule['max']):b.append('assigned_points_outside_source_range')
        requires_review=value!=num(rule['default'])
        if code=='2C-1' and d['cnv_type']=='LOSS' and (d['facts'].get('alternative_start') is True or d['facts'].get('spared_functional_isoform') is True):requires_review=True
        if requires_review and not signed(d.get('adjustment_review')):b.append('score_adjustment_review_required')
        if code=='2C-2' and d['cnv_type']=='LOSS' and value>0 and not (d['facts'].get('promoter_characterized_and_deleted') is True or d['facts'].get('utr_pathogenic_evidence') is True):b.append('2C2_upgrade_evidence_missing')
        if not b:out.update(status='reviewed_section2_candidate',assigned_points=str(value))
    except Pending as e:b.append(str(e))
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args()
    print(json.dumps(evaluate(json.loads(Path(a.input).read_text())),ensure_ascii=False,indent=2))
