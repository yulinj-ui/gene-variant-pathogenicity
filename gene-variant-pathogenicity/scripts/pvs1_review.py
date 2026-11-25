#!/usr/bin/env python3
"""2018 generic PVS1 decision tree audit. Reviewed biological facts are inputs.
No annotation, VCEP overrides, RNA interpretation, clinical code or score import.
"""
import argparse,json
from fractions import Fraction
from pathlib import Path
from review_helpers import reviewed_gate
INVENTORY=json.loads((Path(__file__).resolve().parents[1]/'references/pvs1-inventory.json').read_text())
PATHS={p['id']:p for p in INVENTORY['paths']}
STRENGTHS=['Supporting','Moderate','Strong','VeryStrong']
KINDS={'nonsense_frameshift':'N','canonical_splice':'S','deletion':'D','duplication':'U','initiation':'I'}
FACTS={'nonsense_frameshift':{'nmd','exon_present','lof_common','region','removed_aa','protein_length'},
 'canonical_splice':{'consequence','exon_present','lof_common','region','removed_aa','protein_length'},
 'deletion':{'consequence','exon_present','lof_common','region','removed_aa','protein_length'},
 'duplication':{'tandem','effect','length_known','whole_gene','external_insertion','exon_present','lof_common'},
 'initiation':{'alternative_start','upstream_pathogenic','exon_present','lof_common'}}
GATES=['identity_reviewed','disease_mechanism_reviewed','transcript_reviewed','exon_population_reviewed','vcep_reviewed','technical_quality_reviewed']
class Pending(Exception):pass

def val(f,k,allowed):
    x=f.get(k)
    if x is None or x=='unknown':raise Pending('missing_or_unknown:'+k)
    if isinstance(x,bool):
        if allowed != (True,False):raise ValueError('invalid '+k)
    elif allowed==(True,False):raise ValueError('strict boolean required:'+k)
    if x not in allowed:raise ValueError('invalid '+k)
    return x

def integer(d,k):
    n=d.get(k)
    if n is None:raise Pending('missing:'+k)
    if type(n) is not int or n<0:raise ValueError('nonnegative integer required:'+k)
    return n

def tail(f,critical,excluded,large,small):
    region=val(f,'region',('critical','assessed_unknown','proven_noncritical'))
    if region=='critical':return critical
    if region=='proven_noncritical':raise Pending('source_has_no_proven_noncritical_branch')
    present=val(f,'exon_present',(True,False));common=val(f,'lof_common',(True,False))
    if not present or common:return excluded
    lost=integer(f,'removed_aa');total=integer(f,'protein_length')
    if total<=0 or lost>total:raise ValueError('invalid protein lengths')
    fraction=Fraction(lost,total)
    if fraction==Fraction(1,10):raise Pending('exactly_10_percent_protein_loss_undefined')
    return large if fraction>Fraction(1,10) else small

def route(kind,f):
    if not isinstance(f,dict) or set(f)-FACTS[kind]:raise ValueError('unknown or inappropriate fact fields')
    if kind=='nonsense_frameshift':
        nmd=val(f,'nmd',(True,False))
        if nmd:return 'N01' if val(f,'exon_present',(True,False)) else 'N02'
        return tail(f,'N03','N04','N05','N06')
    if kind in ('canonical_splice','deletion'):
        con=val(f,'consequence',('out_of_frame_nmd','out_of_frame_no_nmd','in_frame','whole_gene'))
        if con=='whole_gene':
            if kind!='deletion':raise ValueError('whole_gene not a splice consequence')
            return 'D01'
        if con=='out_of_frame_nmd':
            present=val(f,'exon_present',(True,False))
            return ('S01' if present else 'S02') if kind=='canonical_splice' else ('D02' if present else 'D03')
        if kind=='canonical_splice':return tail(f,*(['S03','S04','S05','S06'] if con=='out_of_frame_no_nmd' else ['S10','S07','S08','S09']))
        return tail(f,*(['D04','D05','D06','D07'] if con=='out_of_frame_no_nmd' else ['D11','D08','D09','D10']))
    if kind=='duplication':
        tandem=val(f,'tandem',('confirmed','presumed','non_tandem'))
        if tandem=='non_tandem':return 'U05'
        # Unknown is an explicit assessed value here only, as printed in the source tree.
        effect=f.get('effect')
        if effect not in ('disrupts_frame_and_nmd','no_effect','assessed_unknown'):raise Pending('duplication_effect_not_assessed')
        if effect!='disrupts_frame_and_nmd':return 'U01' if tandem=='confirmed' else 'U03'
        return 'U02' if tandem=='confirmed' else 'U04'
    alt=val(f,'alternative_start',(True,False))
    if alt:return 'I03'
    return 'I01' if val(f,'upstream_pathogenic',(True,False)) else 'I02'

def mechanism(m):
    if not isinstance(m,dict):raise Pending('mechanism_missing')
    allowed={'lof_mechanism','association','independent_pathogenic_lof_count','phenotype_lof_count','phenotype_total_count','associated_lof_count','multiple_exons','single_exon_gene','null_mouse','lof_evidence'}
    if set(m)-allowed:raise ValueError('unknown mechanism fields')
    lof=val(m,'lof_mechanism',('established','absent'))
    if lof=='absent':return dict(tier='G0',downgrade=None,counts_audited=False,lof_evidence_audit=None,counts=None)
    assoc=val(m,'association',('limited','moderate','strong','definitive'))
    if assoc=='limited':raise Pending('Table1_association_below_Moderate')
    audit,computed=audit_lof_evidence(m.get('lof_evidence'))
    independent=count_value(m,'independent_pathogenic_lof_count',computed['independent'])
    human=count_value(m,'associated_lof_count',computed['associated'])
    audit['manual_independent']=m.get('independent_pathogenic_lof_count')
    audit['manual_associated']=m.get('associated_lof_count')
    if audit['provided']:
        audit['consistent']=(audit['manual_independent'] in (None,independent) and audit['manual_associated'] in (None,human))
    n=integer(m,'phenotype_lof_count');total=integer(m,'phenotype_total_count')
    if not total or n>total or independent>human or independent>n:raise ValueError('inconsistent mechanism counts')
    span=val(m,'multiple_exons',(True,False));single=val(m,'single_exon_gene',(True,False))
    if single and span:raise ValueError('single exon cannot span multiple exons')
    mouse=mouse_flag(m.get('null_mouse'));span=span or single
    fraction=Fraction(n,total)
    if assoc in ('strong','definitive') and independent>=3 and span:
        if fraction==Fraction(1,10):raise Pending('Table1_exactly_10_percent_conflicts_with_prose')
        if fraction>Fraction(1,10):
            return dict(tier='G1',downgrade=0,counts_audited=audit['provided'],lof_evidence_audit=audit,counts=dict(independent=independent,associated=human,phenotype_lof=n,phenotype_total=total))
    h=human>=2 and span
    tier=None
    if h and mouse:tier,downgrade='G2',1
    elif h or mouse:tier,downgrade='G3',2
    if tier:return dict(tier=tier,downgrade=downgrade,counts_audited=audit['provided'],lof_evidence_audit=audit,counts=dict(independent=independent,associated=human,phenotype_lof=n,phenotype_total=total))
    raise Pending('LoF_established_but_no_Table1_tier_satisfied')

def audit_lof_evidence(rows):
    """Validate the per-variant LoF list and recompute the two mechanism counts.

    Each row is {variant, classification, criteria, pvs1_dependent}.  A variant may
    only be counted as an independent pathogenic LoF if its classification is P/LP
    and that classification did NOT use PVS1 (SVI 2018 anti-circularity rule).
    """
    if rows is None:return dict(provided=False,computed_independent=None,computed_associated=None,manual_independent=None,manual_associated=None,consistent=None),dict(independent=None,associated=None)
    if not isinstance(rows,list) or not rows:raise ValueError('lof_evidence must be a non-empty list')
    okcls={'P','LP','VUS','LB','B'}
    seen=set();independent=0
    for i,row in enumerate(rows):
        if not isinstance(row,dict):raise ValueError('lof_evidence row must be an object')
        allowed={'variant','classification','criteria','pvs1_dependent','clinvar_id','note'}
        if set(row)-allowed:raise ValueError('unknown lof_evidence fields')
        v=row.get('variant')
        if not isinstance(v,str) or not v.strip():raise ValueError('lof_evidence variant required')
        if v in seen:raise ValueError('duplicate lof_evidence variant')
        seen.add(v)
        cls=row.get('classification')
        if not isinstance(cls,str) or cls.strip().upper() not in okcls:raise ValueError('lof_evidence classification must be P/LP/VUS/LB/B')
        cls=cls.strip().upper()
        criteria=row.get('criteria')
        if not isinstance(criteria,list) or not criteria or any(not isinstance(c,str) or not c.strip() for c in criteria):raise ValueError('lof_evidence criteria required')
        dep=row.get('pvs1_dependent')
        if not isinstance(dep,bool):raise ValueError('pvs1_dependent must be boolean')
        if cls in ('P','LP') and not dep:independent+=1
    return dict(provided=True,computed_independent=independent,computed_associated=len(rows),manual_independent=None,manual_associated=None,consistent=True),dict(independent=independent,associated=len(rows))

def count_value(m,key,computed):
    """Manual counts are optional when lof_evidence is supplied; when both exist they must agree."""
    if key in m and m.get(key) is None:raise Pending('missing:'+key)
    manual=m.get(key)
    if computed is None:
        if manual is None:raise Pending('missing:'+key)
        return integer(m,key)
    if manual is None:return computed
    if type(manual) is not int or manual<0:raise ValueError('nonnegative integer required:'+key)
    if manual!=computed:raise ValueError('lof_evidence_count_mismatch:'+key)
    return computed

def mouse_flag(x):
    if x is None:raise Pending('missing:null_mouse')
    if isinstance(x,bool):return x
    if not isinstance(x,dict):raise ValueError('null_mouse must be boolean or object')
    allowed={'model','pmid','phenotype','heterozygous_phenotype','recapitulates'}
    if set(x)-allowed:raise ValueError('unknown null_mouse fields')
    if x.get('recapitulates') not in ('yes','no','partial'):raise Pending('null_mouse_recapitulates_unresolved')
    for k in ('model','pmid','phenotype'):
        if not isinstance(x.get(k),str) or not x[k].strip():raise Pending('null_mouse_evidence_missing:'+k)
    return x['recapitulates']=='yes'

def evaluate(data):
    if not isinstance(data,dict):raise ValueError('object required')
    allowed={'kind','identity','review','mechanism','scenarios','splice_review','basis_ids','facts_review','vcep_policy','source_version'}
    if set(data)-allowed:raise ValueError('unknown top-level field; no caller-selected path or strength')
    kind=data.get('kind')
    if kind not in KINDS:raise ValueError('unsupported variant kind')
    out=dict(tool='pvs1_review',source='https://pmc.ncbi.nlm.nih.gov/articles/PMC6185798/',
      status='blocked',blockers=[],path_results=[],tree_strength=None,adjusted_strength=None,
      mechanism_tier=None,counts_audited=None,lof_evidence_audit=None,mechanism_counts=None,
      automatic_score_import=False,evidence_code=None,classification=None)
    blockers=out['blockers'];blockers.extend(reviewed_gate(data.get('review'),GATES))
    identity=data.get('identity',{})
    for k in ['variant_id','build','genomic_change','transcript','gene','disease','inheritance']:
        if not isinstance(identity,dict) or not isinstance(identity.get(k),str) or not identity[k].strip():blockers.append('identity_missing:'+k)
    if isinstance(identity,dict) and not __import__('re').search(r'\.\d+$',str(identity.get('transcript',''))):blockers.append('transcript_version_required')
    if data.get('source_version')!='AbouTayoun_2018_generic':blockers.append('unsupported_source_version')
    if data.get('vcep_policy')!='reviewed_generic_applicable':blockers.append('gene_specific_override_requires_separate_engine')
    basis=data.get('basis_ids')
    if not isinstance(basis,list) or not basis or any(not isinstance(x,str) or not x.strip() for x in basis) or len(set(basis))!=len(basis):blockers.append('invalid_basis_ids')
    # Biological predicates must have review provenance; no automated annotation is implied.
    facts_review=data.get('facts_review')
    if not isinstance(facts_review,dict):blockers.append('facts_provenance_missing')
    else:
        for k in ['nmd_or_frame','exon_relevance','population_tolerance','critical_region_or_start','mechanism']:
            rec=facts_review.get(k,{})
            if not isinstance(rec,dict) or any(not isinstance(rec.get(x),str) or not rec[x].strip() for x in ['source','location','rationale']):blockers.append('fact_provenance_missing:'+k)
    scenarios=data.get('scenarios')
    if not isinstance(scenarios,list) or not scenarios:raise ValueError('nonempty scenarios required')
    if kind!='canonical_splice' and len(scenarios)!=1:blockers.append('multiple_transcripts_or_consequences_require_review')
    if kind=='canonical_splice':
        s=data.get('splice_review',{})
        if not isinstance(s,dict):s={}
        for k in ['canonical_gt_ag_plusminus_1_2','cryptic_sites_within_20nt_reviewed','scenarios_complete','later_splicing_guidance_reviewed']:
            if s.get(k) is not True:blockers.append('splice_gate:'+k)
        if s.get('rna_data_present') is not False:blockers.append('RNA_specific_workflow_not_implemented')
    elif data.get('splice_review') is not None:raise ValueError('splice_review only for splice variants')
    if blockers:return out
    try:mech=mechanism(data.get('mechanism'))
    except Pending as e:blockers.append(str(e));return out
    out['mechanism_tier']=mech['tier']
    out['counts_audited']=mech.get('counts_audited')
    out['lof_evidence_audit']=mech.get('lof_evidence_audit')
    out['mechanism_counts']=mech.get('counts')
    if mech['tier']=='G0':out['status']='not_applicable';out['reason']='no_LoF_disease_mechanism';return out
    seen=set();effective=[]
    for scenario in scenarios:
        if not isinstance(scenario,dict) or set(scenario)!={'id','facts'}:raise ValueError('scenario requires id and facts only')
        sid=scenario['id']
        if not isinstance(sid,str) or not sid.strip() or sid in seen:raise ValueError('missing/duplicate scenario id')
        seen.add(sid);f=scenario['facts']
        try:
            path_id=route(kind,f);p=PATHS[path_id];raw=p['tree_output']
            strength=None if raw=='不适用PVS1' else 'VeryStrong' if raw.startswith('PVS1（') or raw=='PVS1' else raw.split('_')[1]
            record=dict(scenario_id=sid,path_id=path_id,nodes=p['nodes'],source_tree_output=raw,tree_strength=strength,global_exclusions=[])
            out['path_results'].append(record)
            if kind=='duplication':
                if val(f,'whole_gene',(True,False)) or val(f,'external_insertion',(True,False)):record['global_exclusions'].append('duplication_outside_intragenic_LoF_scope')
                if not val(f,'length_known',(True,False)):raise Pending('duplication_length_unknown')
            # Whole gene deletion has no exon relevance predicate; clinical footnote is never automated.
            if not (kind=='deletion' and f.get('consequence')=='whole_gene'):
                present=val(f,'exon_present',(True,False));common=val(f,'lof_common',(True,False))
                if not present or common:record['global_exclusions'].append('exon_tolerance_or_relevant_transcript_exclusion')
            if record['global_exclusions']:strength=None
            effective.append(strength)
        except Pending as e:blockers.append(sid+':'+str(e))
    if blockers:return out
    weakest=None if None in effective else min(effective,key=STRENGTHS.index)
    out['tree_strength']=weakest
    if weakest is None:out['status']='not_applicable';out['reason']='source_leaf_or_global_exclusion';return out
    level=STRENGTHS.index(weakest)-mech['downgrade']
    if level<0:blockers.append('Table1_downgrade_below_Supporting_undefined');return out
    out.update(status='test_calculation_only',adjusted_strength=STRENGTHS[level])
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('input_json');args=ap.parse_args()
    try:print(json.dumps(evaluate(json.loads(Path(args.input_json).read_text())),ensure_ascii=False,indent=2))
    except (ValueError,TypeError,KeyError) as e:ap.error(str(e))
