import unittest,copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from cnv_section2 import evaluate,TABLE
from cnv_case import run
from cnv_interval import envelope
from test_v5r1 import sign
from test_v5 import fixture as pvs_fixture
from render_report import render

def fixture(typ='LOSS',relation='full_cover'):
    return dict(cnv_type=typ,identity=dict(variant_id='synthetic-cnv',gene='SYNTHETIC',build='GRCh38',disease='synthetic disease',inheritance='AD'),target_id='synthetic-target',target_kind='gene',relation=relation,
        review=sign(),basis_ids=['synthetic-cnv-basis'],
        dosage=dict(axis='HI' if typ=='LOSS' else 'TS',score=3,source='synthetic source NOT clinical evidence',record_id='synthetic',evaluated_at='2020-01-01',current_evidence_review='synthetic review'),
        fact_sources={k:dict(source='synthetic',location='fixture',rationale='engineering test only') for k in ['interval_and_breakpoints','target_geometry','dosage','transcript_and_function','platform']},facts={})
def partial(rel,f):
    d=fixture(relation=rel);d.update(platform_resolution_sufficient=True,transcript_version='NM_TEST.1',transcript_choice_rationale='synthetic');d['facts']=f;return d
def intragenic(path):
    raw=pvs_fixture(path);d=fixture('LOSS' if path.startswith('D') else 'GAIN','intragenic');d['dosage']['axis']='HI';d['identity']={k:raw['identity'][k] for k in ['variant_id','gene','build','disease','inheritance']};d['basis_ids']=raw['basis_ids'];d['pvs1_input']=raw
    con=raw['scenarios'][0]['facts'].get('consequence','not_applicable');d['facts']['frame_status']='in_frame' if con=='in_frame' else 'out_of_frame' if con.startswith('out_of_frame') else 'not_applicable'
    if path.startswith('U'):d['facts']['terminal_coding_exon_involved']=False
    return d
from manual_fixture import reviewed

def case(d=None):
    d=d or fixture();a=sign();a.update({k:True for k in ['all_targets_and_transcripts_reviewed','uncertain_breakpoints_reviewed','other_sections_reviewed','section4_skip_rule_reviewed','independence_and_caps_reviewed','dosage_date_reviewed','clinical_context_reviewed']})
    return reviewed(dict(identity=d['identity'],section2_input=d,integration_review=a,scoring=dict(framework='CNV_'+d['cnv_type'],rules={},evidence=[],combination_policy=dict(status='reviewed',framework='CNV_'+d['cnv_type'],source='synthetic',version='test',reviewer='synthetic',reviewed_at='2026-09-27',mutually_exclusive=[],caps=[]))))

class CNVTests(unittest.TestCase):
    def assertBranch(self,d,code,points):
        r=evaluate(d);self.assertEqual(r['status'],'reviewed_section2_candidate',r);self.assertEqual(r['code'],code);self.assertEqual(r['assigned_points'],points);self.assertIsNone(r['classification'])
    def test_loss_2A(self):self.assertBranch(fixture(),'2A','1.00')
    def test_gain_2A_TS(self):self.assertBranch(fixture('GAIN'),'2A','1.00')
    def test_HI2_not_established(self):
        d=fixture();d['dosage']['score']=2;self.assertEqual(evaluate(d)['status'],'blocked')
    def test_HI_not_TS(self):
        d=fixture('GAIN');d['dosage']['axis']='HI';self.assertEqual(evaluate(d)['status'],'blocked')
    def test_dosage_date_required(self):
        d=fixture();del d['dosage']['evaluated_at'];self.assertEqual(evaluate(d)['status'],'blocked')
    def test_2B_all_conditions(self):
        for typ in ['LOSS','GAIN']:
            for f in ['not_included','uncertain','not_established']:
                d=fixture(typ,'partial_region');d['target_kind']='region';d['facts']['critical_region_status']=f;self.assertBranch(d,'2B','0')
    def test_2B_fully_contained_critical_reidentify(self):
        d=fixture(relation='partial_region');d['target_kind']='region';d['facts']['critical_region_status']='fully_included';self.assertEqual(evaluate(d)['status'],'blocked')
    def test_2C1_default(self):self.assertBranch(partial('five_prime',dict(coding_sequence_involved=True,alternative_start=False,spared_functional_isoform=False)),'2C-1','0.90')
    def test_2C1_rescue_requires_adjustment_review(self):
        d=partial('five_prime',dict(coding_sequence_involved=True,alternative_start=True,spared_functional_isoform=False));self.assertEqual(evaluate(d)['status'],'blocked');d.update(assigned_points='0.45',adjustment_review=sign());self.assertBranch(d,'2C-1','0.45')
    def test_2C2_default(self):self.assertBranch(partial('five_prime',dict(coding_sequence_involved=False)),'2C-2','0')
    def test_2C2_upgrade_needs_evidence(self):
        d=partial('five_prime',dict(coding_sequence_involved=False));d.update(assigned_points='0.45',adjustment_review=sign());self.assertEqual(evaluate(d)['status'],'blocked');d['facts']['promoter_characterized_and_deleted']=True;self.assertBranch(d,'2C-2','0.45')
    def test_platform_insufficient(self):
        d=partial('five_prime',dict(coding_sequence_involved=False));d['platform_resolution_sufficient']=False;self.assertEqual(evaluate(d)['status'],'blocked')
    def test_2D1(self):self.assertBranch(partial('three_prime',dict(utr_only=True)),'2D-1','0')
    def test_2D2(self):self.assertBranch(partial('three_prime',dict(utr_only=False,last_exon_only=True,last_exon_critical=True)),'2D-2','0.90')
    def test_2D3(self):self.assertBranch(partial('three_prime',dict(utr_only=False,last_exon_only=True,last_exon_critical=False,critical_evidence_search_complete=True)),'2D-3','0.30')
    def test_unknown_last_exon_not_negative(self):
        d=partial('three_prime',dict(utr_only=False,last_exon_only=True,last_exon_critical='unknown'));self.assertEqual(evaluate(d)['status'],'blocked')
    def test_2D4(self):self.assertBranch(partial('three_prime',dict(utr_only=False,last_exon_only=False,last_and_other_exons=True,nmd_expected=True)),'2D-4','0.90')
    def test_2D4_no_nmd_no_default(self):
        d=partial('three_prime',dict(utr_only=False,last_exon_only=False,last_and_other_exons=True,nmd_expected=False));self.assertEqual(evaluate(d)['status'],'blocked')
    def test_2E_mappings(self):
        for path,pt in [('D02','0.90'),('D04','0.45'),('D07','0.30'),('D03','0')]:self.assertBranch(intragenic(path),'2E',pt)
    def test_2E_supporting(self):
        d=intragenic('D07');d['pvs1_input']['mechanism'].update(association='moderate',null_mouse=True);self.assertBranch(d,'2E','0.15')
    def test_AR_HI30_not_promoted(self):
        d=intragenic('D02');d['dosage']['score']=30;self.assertEqual(evaluate(d)['status'],'blocked')
    def test_unknown_frame_conservative_is_recorded(self):
        d=intragenic('D10');d['facts']['frame_status']='unknown';self.assertEqual(evaluate(d)['status'],'blocked');d.update(uncertainty_strategy='conservative_in_frame',assumption_review=sign());self.assertBranch(d,'2E','0.30');self.assertEqual(d['facts']['frame_status'],'unknown')
    def test_unknown_frame_no_nmd_assumption(self):
        d=intragenic('D02');d['facts']['frame_status']='unknown';d.update(uncertainty_strategy='conservative_in_frame',assumption_review=sign())
        with self.assertRaises(ValueError):evaluate(d)
    def test_PVS1_block_not_zero(self):
        d=intragenic('D02');d['pvs1_input']['mechanism']['independent_pathogenic_lof_count']=None;self.assertIsNone(evaluate(d)['assigned_points'])
    def test_loss_2F_not_frequency(self):
        d=fixture(relation='benign_contained');d['dosage']={'population_frequency':'0.1'};self.assertEqual(evaluate(d)['status'],'blocked')
    def test_benign_axis_not_interchangeable(self):
        d=fixture('GAIN','benign_identical_content');d['dosage'].update(axis='HI',score=40,assessment='dosage_sensitivity_unlikely');self.assertEqual(evaluate(d)['status'],'blocked')
    def test_partial_transcript_must_be_versioned(self):
        d=partial('five_prime',dict(coding_sequence_involved=False));d['transcript_version']='NM_TEST';self.assertEqual(evaluate(d)['status'],'blocked')
    def test_benign_relations(self):
        for typ,rel,code,pt,f in [('LOSS','benign_contained','2F','-1.00',{}),('LOSS','benign_extra_material','2G','0',{}),('GAIN','benign_identical_content','2C','-1.00',{}),('GAIN','benign_smaller','2D','-1.00',{'coding_gene_interrupted':False}),('GAIN','benign_smaller','2E','0',{'coding_gene_interrupted':True}),('GAIN','benign_larger_no_extra_coding','2F','-0.90',{}),('GAIN','benign_extra_material','2G','0',{})]:
            d=fixture(typ,rel);d['dosage'].update(assessment='dosage_sensitivity_unlikely',score=40);d['facts']=f;self.assertBranch(d,code,pt)
    def prediction(self):
        d=fixture(relation='predicted_hi');d['dosage']['score']=0;d.update(target_clinical_significance='uncertain',applied_hi_categories=[]);d['facts']=dict(predictor_profile='Riggs2020_original',pli='0.9',oe_upper='0.349999',decipher_hi_percent='10',gnomad_source_version='historical metric verified',decipher_source_version='HI index verified',metric_equivalence_review='synthetic');return d
    def test_2H_boundary_pass(self):self.assertBranch(self.prediction(),'2H','0.15')
    def test_2H_oe_equal_fails(self):
        d=self.prediction();d['facts']['oe_upper']='0.35';self.assertEqual(evaluate(d)['status'],'blocked')
    def test_2H_local_profile_disabled(self):
        d=self.prediction();d['facts']['predictor_profile']='gnomad_v4_0.6';self.assertEqual(evaluate(d)['status'],'blocked')
    def test_2H_not_additive(self):
        d=self.prediction();d['applied_hi_categories']=['2A'];self.assertEqual(evaluate(d)['status'],'blocked')
        d['applied_hi_categories']='2A'
        with self.assertRaises(ValueError):evaluate(d)
    def test_gain_2H(self):
        d=fixture('GAIN','full_hi_gene');d['dosage']['axis']='HI';self.assertBranch(d,'2H','0')
    def test_gain_2I(self):
        for path,pt in [('U02','0.90'),('U04','0.45'),('U05','0')]:self.assertBranch(intragenic(path),'2I',pt)
    def test_terminal_dup_not_automatically_pathogenic_or_benign(self):
        d=intragenic('U02');d['facts']['terminal_coding_exon_involved']=True;self.assertEqual(evaluate(d)['status'],'blocked');self.assertIsNone(evaluate(d)['assigned_points'])
    def test_gain_unmapped_strength_block(self):
        d=intragenic('U04');d['pvs1_input']['mechanism'].update(association='moderate',null_mouse=True);self.assertEqual(evaluate(d)['status'],'blocked')
    def test_gain_2J_2K(self):
        for phenotype,code,pt in [('unknown_phenotype','2J','0'),('inconsistent','2J','0'),('highly_specific_consistent','2K','0.45')]:
            d=fixture('GAIN','one_breakpoint_hi');d['dosage']['axis']='HI';d['facts']['phenotype']=phenotype;self.assertBranch(d,code,pt)
    def test_gain_unspecific_not_high(self):
        d=fixture('GAIN','one_breakpoint_hi');d['dosage']['axis']='HI';d['facts']['phenotype']='consistent_nonspecific';self.assertEqual(evaluate(d)['status'],'blocked')
    def test_gain_2L(self):
        d=fixture('GAIN','breakpoint_uncertain_gene');d['dosage']['score']=0;d['target_clinical_significance']='uncertain';self.assertBranch(d,'2L','0')
    def test_predictor_cannot_override_HI3(self):
        d=self.prediction();d['dosage']['score']=3;self.assertEqual(evaluate(d)['status'],'blocked')
    def test_gain_2F_default_is_LB_not_B(self):
        d=fixture('GAIN','benign_larger_no_extra_coding');d['dosage']['assessment']='dosage_sensitivity_unlikely';d['dosage']['score']=40
        self.assertEqual(run(case(d))['authoritative_candidate'],'LB')
    def test_out_of_range_adjustment(self):
        d=fixture();d.update(assigned_points='1.1',adjustment_review=sign());self.assertEqual(evaluate(d)['status'],'blocked')
    def test_case_independent_CNV_score(self):
        r=run(case());self.assertEqual(r['authoritative_candidate'],'P');self.assertEqual(r['score_comparison']['net_points'],'1.00');self.assertIsNone(r['classification'])
    def test_case_cannot_stack_section2(self):
        d=case();d['scoring']['evidence']=[{'code':'2H'}]
        with self.assertRaises(ValueError):run(d)
    def test_case_no_unreviewed_whole_CNV(self):
        d=case();d['integration_review']['other_sections_reviewed']=False;self.assertIsNone(run(d)['authoritative_candidate'])
    def test_case_loss_gain_mismatch(self):
        d=case();d['scoring']['framework']='CNV_GAIN'
        with self.assertRaises(ValueError):run(d)
    def test_CNV_report(self):
        d=case();out=render(dict(variant_id=d['identity']['variant_id'],cnv_pipeline=d));self.assertEqual(out.count('## 模块'),10);self.assertIn('CNV五段式',out)
    def test_geometry_envelope(self):
        def interval(a,b):return dict(build='GRCh38',system='one_based_closed',chr='1',start=a,end=b)
        r=envelope(interval(110,190),interval(90,210),interval(100,200));self.assertEqual(r['geometry_state'],'boundary_dependent_or_partial');self.assertIsNone(r['clinical_code'])
    def test_geometry_bad_envelope(self):
        def interval(a,b):return dict(build='GRCh38',system='one_based_closed',chr='1',start=a,end=b)
        with self.assertRaises(ValueError):envelope(interval(90,210),interval(100,200),interval(100,200))

if __name__=='__main__':unittest.main()
