#!/usr/bin/env python3
"""Limited Biesecker 2024 audit calculations, never clinical evidence or score import."""
import argparse
import json
import re
from decimal import Decimal
from fractions import Fraction
from review_helpers import reviewed_gate, pp1pp4

SOURCE='https://pmc.ncbi.nlm.nih.gov/articles/PMC10806742/'
TABLE2=[('19.1','1'),('25.4','1.5'),('33.0','2'),('41.5','2.5'),('50.6','3'),
 ('59.6','3.5'),('68.0','4'),('75.4','4.5'),('81.6','5'),('86.4','5.5'),
 ('90.2','6'),('93.0','6.5'),('95.0','7'),('96.5','7.5'),('97.5','8'),
 ('98.3','8.5'),('98.8','9'),('99.2','9.5'),('99.4','10'),('99.6','10.5'),
 ('99.7','11'),('99.8','11.5'),('99.9','12')]
BASE_FIELDS={'packet_id','subject_id','allele_id','variant_ids','basis_ids','review','mode','source'}
COMMON_GATES=['applicability_reviewed','phase_reviewed','penetrance_reviewed','vcep_checked','basis_independence_reviewed']
PP4_GATES=['phenotype_matched','testing_method_matched','yield_source_verified','equal_plausibility_reviewed','single_locus_model_reviewed']
JOINT_GATES=['joint_points_reviewed','allocation_already_completed','joint_independence_reviewed','cap_applicable']

def exact(value):
    # Explicit decimal strings preserve caller precision; booleans, floats, exponent notation rejected.
    if not isinstance(value,str) or not re.fullmatch(r'(?:0|[1-9][0-9]*)(?:\.[0-9]+)?',value):
        raise ValueError('use an unsigned exact decimal string; no floats, exponent or implicit rounding')
    return Fraction(Decimal(value))

def decimal_text(value):
    value=Fraction(value);den=value.denominator
    for factor in (2,5):
        while den%factor==0:den//=factor
    if den!=1:raise ValueError('non-terminating decimal not supported')
    # Fraction arithmetic is exact; long division never uses Decimal context rounding.
    sign='-' if value<0 else '';a,b=abs(value.numerator),value.denominator
    whole,rem=divmod(a,b);digits=[]
    while rem:
        q,rem=divmod(rem*10,b);digits.append(str(q))
    return sign+str(whole)+('.'+''.join(digits) if digits else '')

def table2(probability):
    if not 0<=probability<=1:raise ValueError('probability outside [0,1]')
    # Printed table only. Outside its explicit range remains unmapped, never benign evidence.
    if probability<exact('0.191') or probability>exact('0.999'):return None
    eligible=[Fraction(Decimal(n)) for pct,n in TABLE2 if probability>=Fraction(Decimal(pct))/100]
    return max(eligible) if eligible else None

def ids(value,name):
    if not isinstance(value,list) or not value or any(not isinstance(v,str) or not v.strip() for v in value):
        raise ValueError(name+' must be a nonempty string list')
    if len(value)!=len(set(value)):raise ValueError('duplicate '+name)
    return value

def packet(data):
    if not isinstance(data,dict):raise ValueError('packet must be an object')
    mode=data.get('mode')
    fields={'pp4_equal':{'diagnostic_yield','inheritance','locus_model','allocation','segregation_present'},
            'reviewed_joint_cap':{'joint_points'}}
    if mode not in fields:raise ValueError('unsupported mode; unequal allocation, pedigree and BS4 engines remain disabled')
    if set(data)-(BASE_FIELDS|fields[mode]):raise ValueError('unknown packet fields; unsupported evidence cannot be ignored')
    for key in ['packet_id','subject_id','allele_id']:
        if not isinstance(data.get(key),str) or not data[key].strip():raise ValueError(key+' required')
    variants=ids(data.get('variant_ids'),'variant_ids');basis=ids(data.get('basis_ids'),'basis_ids')
    blockers=reviewed_gate(data.get('review'),COMMON_GATES+(PP4_GATES if mode=='pp4_equal' else JOINT_GATES))
    src=data.get('source')
    required=['url','version','location','gene','disease']+(['phenotype_definition','testing_method'] if mode=='pp4_equal' else [])
    if not isinstance(src,dict):blockers.append('source_record_missing')
    else:
        blockers += ['source_missing:'+k for k in required if not isinstance(src.get(k),str) or not src[k].strip()]
        if src.get('kind')!='published':blockers.append('unverified_or_local_parameter_source_disabled')
    if mode=='pp4_equal':
        y=exact(data.get('diagnostic_yield'))
        if not 0<=y<=1:raise ValueError('diagnostic_yield must be a fraction in [0,1], not percent')
        if data.get('inheritance')!='AR' or data.get('locus_model')!='homogeneous':blockers.append('outside_Figure2_AR_homogeneous_scope')
        if data.get('segregation_present') is not False:blockers.append('segregation_combination_not_supported')
        if data.get('allocation')!='equal':blockers.append('unequal_allocation_disabled')
        if len(variants) not in (1,2):blockers.append('only_one_or_two_cis_candidates_validated')
    else:
        y=exact(data.get('joint_points'))
        if (y*10).denominator!=1:raise ValueError('reviewed joint points must already have at most one decimal; no rounding')
        if len(variants)!=1:blockers.append('joint_mode_requires_single_already_allocated_variant')
    out=dict(packet_id=data['packet_id'],subject_id=data['subject_id'],allele_id=data['allele_id'],
        variant_ids=variants,basis_ids=basis,mode=mode,source=src,status='blocked' if blockers else 'test_calculation_only',
        blockers=blockers,results=[],automatic_score_import=False,evidence_code=None,classification=None)
    if blockers:return out
    if mode=='pp4_equal':
        share=y/len(variants)
        before=table2(share)
        if before is None:
            out.update(status='unmapped',blockers=['allocated_probability_outside_printed_Table2'],
                       allocation=dict(input_probability=decimal_text(y),per_variant_probability=decimal_text(share)))
            return out
        for variant in variants:
            out['results'].append(dict(variant_id=variant,allocated_probability=decimal_text(share),
                table2_points_before_cap=decimal_text(before),review_points=decimal_text(min(before,Fraction(5))),
                table4_maximum_options=None,evidence_code=None,classification=None))
        out['allocation']=dict(input_probability=decimal_text(y),allocated_sum=decimal_text(share*len(variants)),
                               method='probability_first_equal_split_then_Table2_floor_then_per_variant_cap')
    else:
        capped=min(y,Fraction(5))
        # Table 4 offers options only; externally reviewed joint subtotal is NOT derived here.
        gate=dict(data['review'],**{k:True for k in ['independence_reviewed','probability_allocation_reviewed','cap_reviewed']})
        mapped=pp1pp4({'joint_points':decimal_text(capped),'review':gate})
        out['results']=[dict(variant_id=variants[0],reviewed_joint_points_before_cap=decimal_text(y),
                            review_points=decimal_text(capped),table4_maximum_options=mapped['maximum_code_options'],
                            selected_codes=None,evidence_code=None,classification=None)]
    return out

def calculate(data):
    if not isinstance(data,dict) or set(data)!={'packets'} or not isinstance(data['packets'],list) or not data['packets']:
        raise ValueError('input must contain only a nonempty packets list')
    outputs=[];seen_packets=set();seen_variants=set();seen_basis={}
    for raw in data['packets']:
        p=packet(raw)
        if p['packet_id'] in seen_packets:raise ValueError('duplicate packet id')
        seen_packets.add(p['packet_id'])
        if seen_variants & set(p['variant_ids']):raise ValueError('repeated variant packets; cross-family and repeated-allele aggregation disabled')
        seen_variants.update(p['variant_ids'])
        for basis in p['basis_ids']:
            if basis in seen_basis:raise ValueError('repeated underlying evidence across packets; use one packet for cis candidates')
            seen_basis[basis]=p['packet_id']
        outputs.append(p)
    blocked=any(p['status']!='test_calculation_only' for p in outputs)
    return dict(tool='locus_review',rule_source=SOURCE,status='blocked' if blocked else 'test_calculation_only',
        packets=outputs,automatic_score_import=False,evidence_code=None,classification=None,
        limitations=['No automated pedigree counts, BS4, unequal allocation or main-score import',
                     'Printed Table2 bounds only; no formula extrapolation or invented zero/benign evidence',
                     'Review flags are caller attestations, not authentication or independent medical verification'])

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('input_json');args=ap.parse_args()
    try:print(json.dumps(calculate(json.loads(open(args.input_json).read())),ensure_ascii=False,indent=2))
    except (ValueError,TypeError,KeyError) as e:ap.error(str(e))
