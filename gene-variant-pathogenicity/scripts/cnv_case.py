"""Admit one reviewed Section2 contribution to the independent CNV score.
Other sections still require explicit reviewed evidence. No SNV point conversion.
"""
import argparse,copy,json
from pathlib import Path
from cnv_section2 import evaluate
from case_pipeline import signed
from score import score
from cnv_manual_review import validate as validate_manual_review

def run(d):
    if set(d)-{'identity','scoring','section2_input','integration_review','manual_review','review_mode'}:raise ValueError('unknown CNV case fields')
    s=copy.deepcopy(d['scoring']);inp=d['section2_input'];identity=d['identity']
    if identity!=inp.get('identity'):raise ValueError('CNV case identity mismatch')
    framework='CNV_'+inp['cnv_type']
    if s.get('framework')!=framework:raise ValueError('CNV loss/gain framework mismatch')
    if any(r.get('code','').startswith('2') or r.get('admitted_from') for r in s.get('evidence',[])):raise ValueError('one Section2 contribution only; do not stack or submit preassembled Section2 rows')
    b=validate_manual_review(d);approval=d.get('integration_review',{})
    if not signed(approval):b.append('CNV_integration_review_missing')
    for k in ['all_targets_and_transcripts_reviewed','uncertain_breakpoints_reviewed','other_sections_reviewed','section4_skip_rule_reviewed','independence_and_caps_reviewed','dosage_date_reviewed','clinical_context_reviewed']:
        if approval.get(k) is not True:b.append('CNV_integration_unreviewed:'+k)
    r=evaluate(inp)
    if r['status']!='reviewed_section2_candidate':b+=['section2:'+x for x in r['blockers']]
    seen={basis for row in s.get('evidence',[]) for basis in row.get('basis_ids',[])}
    if seen & set(inp.get('basis_ids',[])):b.append('section2_underlying_evidence_reused')
    if not b:
        rid='cnv-section2-source-rule'
        if rid in s.get('rules',{}):raise ValueError('reserved rule id')
        review=inp['review'];code=r['code'];points=r['assigned_points']
        s.setdefault('rules',{})[rid]=dict(code=code,framework=framework,status='reviewed',
            source='Riggs2020 Supplemental Material1 and official CNV calculator',version='Riggs2020; checked 2026-09-27',
            location='Section2 '+code,reviewer=review['reviewer'],reviewed_at=review['reviewed_at'],
            applicability=review['rationale'],allowed_points=[points])
        s.setdefault('evidence',[]).append(dict(id='cnv-section2',code=code,framework=framework,rule_id=rid,
            status='reviewed',gate='passed',points=points,source_ids=[review['source']],basis_ids=inp['basis_ids'],
            rationale=review['rationale'],admitted_from='cnv_section2'))
    calculated=score(s);b+=calculated['blockers']
    return dict(status='blocked' if b else 'reviewed_candidate_only',classification=None,
        authoritative_candidate=None if b else calculated['point_candidate'],authoritative_framework='Riggs_2020',
        score_comparison=calculated,blockers=b,assembled_scoring=s,admission_audit=[r],
        routing=dict(framework=framework,integration_review=approval,manual_review=d.get('manual_review')),ba1_exception_check=None,
        limitations=['One reviewed Section2 contribution, not automated whole-CNV classification','No automatic transcript/coordinate/NMD annotation','Other CNV sections, conflicts and caps remain under documented review'])

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args()
    print(json.dumps(run(json.loads(Path(a.input).read_text())),ensure_ascii=False,indent=2))
