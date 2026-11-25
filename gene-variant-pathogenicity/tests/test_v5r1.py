import unittest,json,copy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from case_pipeline import run,ASSESSMENTS,assessment
from ba1_review import match,TABLE
from render_report import render
from compare_frameworks import decode

def load(n):return json.loads((ROOT/'tests/fixtures'/n).read_text())
def sign():return dict(approved=True,reviewer='synthetic reviewer',reviewed_at='2026-09-27',source='synthetic test NOT medical evidence',location='fixture',rationale='synthetic test only')
def assess(kind):
    a={k:dict(finding='synthetic',source='fixture',location='fixture',conclusion='synthetic reviewed') for k in ASSESSMENTS[kind]}
    a['review']=sign();a.update(readout_kind='protein_function',variant_result='abnormal',conflict_status='none',complexity='simple_reviewed');return a
def add_rule(d,code):
    r=copy.deepcopy(d['scoring']['rules']['r0']);r.update(code=code,allowed_points=[decode(code)[1]])
    d['scoring']['rules'][code]=r
def fixture(kind='pvs1'):
    c=load('case-v5.json');p=c['review_calculations']['pvs1']
    identity={k:p['identity'][k] for k in ['variant_id','gene','disease','inheritance']};identity['subject_id']='synthetic-subject'
    d=dict(identity=identity,scoring=c['scoring'],routing=dict(identity=copy.deepcopy(identity),review=sign(),search_completed=True,outcome='none_found',searches=[dict(url='https://cspec.genome.network',query='SYNTHETIC',accessed_at='2026-09-27',result='synthetic negative; not an actual search')]),admissions=[])
    a=dict(id='a1',kind=kind,identity=copy.deepcopy(identity),approval=sign(),source_ids=['fixture'],basis_ids=['b-new'],selected_codes=[],rule_ids={})
    if kind=='pvs1':a.update(input=p,basis_ids=p['basis_ids'],selected_codes=['PVS1_VeryStrong'],mechanism='lof')
    if kind=='functional':a.update(input=load('helper-functional-v3.json'),selected_codes=['PS3_Strong'],assessment=assess('functional'))
    if kind=='pm3':
        identity['inheritance']='AR';d['routing']['identity']['inheritance']='AR';a['identity']=copy.deepcopy(identity)
        a.update(input=load('helper-pm3-v3.json'),selected_codes=['PM3_Supporting'])
    if kind=='locus':
        x=load('locus-joint-v4.json');q=x['packets'][0];q['variant_ids']=[identity['variant_id']];q['source'].update(gene=identity['gene'],disease=identity['disease'])
        a.update(input=x,basis_ids=q['basis_ids'],selected_codes=['PP1_Strong','PP4_Supporting'],assessment=assess('pedigree'))
    for code in a['selected_codes']:add_rule(d,code);a['rule_ids'][code]=code
    d['admissions']=[a];return d

class BridgeTests(unittest.TestCase):
    def vcep(self):
        d=fixture();d['admissions']=[];r=d['routing'];r['outcome']='applicable'
        r['specification']=dict(url='https://example.org/synthetic-spec',version='test',gene=d['identity']['gene'],disease=d['identity']['disease'],inheritance=d['identity']['inheritance'],combining_rule_location='synthetic table',release_status='released',required_materials_complete=True,documents=[dict(url='https://example.org/synthetic-spec',version='test',location='table',full_text_reviewed=True,sha256='a'*64)])
        r['specification']['variant_scope_reviewed']=True
        d['scoring']['rules']['r0'].update(specification_url=r['specification']['url'],specification_version='test')
        d['vcep_combination_review']=dict(sign(),candidate='VUS',matched_rules=['synthetic table rule'],evidence_ids=['e0']);return d
    def test_VCEP_reviewed_candidate(self):
        r=run(self.vcep());self.assertEqual(r['authoritative_candidate'],'VUS');self.assertEqual(r['authoritative_framework'],'VCEP_reviewed_combination')
    def test_VCEP_material_missing_blocks(self):
        d=self.vcep();d['routing']['specification']['required_materials_complete']=False;self.assertIsNone(run(d)['authoritative_candidate'])
    def test_VCEP_version_mismatch_blocks(self):
        d=self.vcep();d['scoring']['rules']['r0']['specification_version']='old';self.assertIsNone(run(d)['authoritative_candidate'])
    def test_VCEP_decision_evidence_mismatch(self):
        d=self.vcep();d['vcep_combination_review']['evidence_ids']=[];self.assertIsNone(run(d)['authoritative_candidate'])
    def test_preassembled_admission_rejected(self):
        d=fixture();d['scoring']['evidence'][0]['admitted_from']='forged'
        with self.assertRaises(ValueError):run(d)
    def test_pvs1_recomputed_and_admitted(self):
        r=run(fixture());self.assertEqual(r['status'],'reviewed_candidate_only');self.assertEqual(r['score_comparison']['net_points'],'9');self.assertEqual(r['authoritative_candidate'],'LP');self.assertIsNone(r['classification'])
    def test_pm3_supporting_admitted(self):
        r=run(fixture('pm3'));self.assertEqual(r['status'],'reviewed_candidate_only');self.assertEqual(r['score_comparison']['net_points'],'2')
    def test_pm3_AD_blocked(self):
        d=fixture('pm3');d['identity']['inheritance']='AD';d['routing']['identity']['inheritance']='AD';d['admissions'][0]['identity']['inheritance']='AD';self.assertIsNone(run(d)['authoritative_candidate'])
    def test_missing_search(self):
        d=fixture();d['routing']['searches']=[];self.assertIsNone(run(d)['authoritative_candidate'])
    def test_search_failure_not_fallback(self):
        d=fixture();d['routing']['outcome']='unavailable';self.assertIn('VCEP_status_unresolved',run(d)['blockers'])
    def test_not_applicable_requires_reason(self):
        d=fixture();d['routing']['outcome']='not_applicable';self.assertIn('VCEP_exclusion_reasons_missing',run(d)['blockers'])
    def test_scope_mismatch(self):
        d=fixture();d['routing']['identity']['inheritance']='AR';self.assertIsNone(run(d)['authoritative_candidate'])
    def test_no_approval_no_bridge(self):
        d=fixture();d['admissions'][0]['approval']['approved']=False;self.assertEqual(len(run(d)['score_comparison']['accepted']),1)
    def test_raw_helper_block(self):
        d=fixture();d['admissions'][0]['input']['mechanism']['independent_pathogenic_lof_count']=None;self.assertIsNone(run(d)['authoritative_candidate'])
    def test_strength_cannot_be_overridden(self):
        d=fixture();d['admissions'][0]['selected_codes']=['PVS1_Strong'];self.assertIsNone(run(d)['authoritative_candidate'])
    def test_shared_basis_block(self):
        d=fixture();d['scoring']['evidence'][0]['basis_ids']=d['admissions'][0]['basis_ids'];self.assertIsNone(run(d)['authoritative_candidate'])
    def test_functional_admission(self):
        r=run(fixture('functional'));self.assertEqual(r['status'],'reviewed_candidate_only');self.assertEqual(r['score_comparison']['net_points'],'5')
    def test_functional_missing_controls(self):
        d=fixture('functional');del d['admissions'][0]['assessment']['controls'];self.assertIsNone(run(d)['authoritative_candidate'])
    def test_functional_conflict(self):
        d=fixture('functional');d['admissions'][0]['assessment']['conflict_status']='unresolved';self.assertIsNone(run(d)['authoritative_candidate'])
    def test_functional_intermediate(self):
        d=fixture('functional');d['admissions'][0]['assessment']['variant_result']='intermediate';self.assertIsNone(run(d)['authoritative_candidate'])
    def test_splice_is_not_ps3(self):
        d=fixture('functional');d['admissions'][0]['assessment']['readout_kind']='rna_splicing';self.assertIsNone(run(d)['authoritative_candidate'])
    def test_indeterminate_odds_no_code(self):
        d=fixture('functional');d['admissions'][0]['input']['odds_path']='0.49';self.assertIsNone(run(d)['authoritative_candidate'])
    def test_locus_joint_cap_once(self):
        r=run(fixture('locus'));self.assertEqual(r['status'],'reviewed_candidate_only');self.assertEqual(r['score_comparison']['net_points'],'6');self.assertEqual(len(r['score_comparison']['accepted']),3)
    def test_locus_fractional_conversion(self):
        d=fixture('locus');a=d['admissions'][0];a['input']['packets'][0]['joint_points']='2.5';a['selected_codes']=['PP1_Moderate'];add_rule(d,'PP1_Moderate');a['rule_ids']['PP1_Moderate']='PP1_Moderate';self.assertEqual(run(d)['score_comparison']['net_points'],'3')
    def test_locus_subject(self):
        d=fixture('locus');d['admissions'][0]['input']['packets'][0]['subject_id']='other';self.assertIsNone(run(d)['authoritative_candidate'])
    def test_locus_disease(self):
        d=fixture('locus');d['admissions'][0]['input']['packets'][0]['source']['disease']='other';self.assertIsNone(run(d)['authoritative_candidate'])
    def test_locus_duplicate_raw_main(self):
        d=fixture('locus');d['scoring']['evidence'][0]['basis_ids']=d['admissions'][0]['basis_ids'];self.assertIsNone(run(d)['authoritative_candidate'])
    def test_rna_missing_nmd(self):
        a=assess('rna');del a['nmd_inhibition'];self.assertIn('rna:missing_nmd_inhibition',assessment(a,'rna'))
    def test_manual_functional_requires_worksheet(self):
        d=fixture();d['admissions']=[];row=d['scoring']['evidence'][0];row.update(code='PS3_Strong',points=4,rule_id='PS3_Strong');add_rule(d,'PS3_Strong');self.assertIsNone(run(d)['authoritative_candidate'])
    def test_cnv_rejected_by_snv_bridge(self):
        d=fixture();d['scoring']['framework']='CNV_LOSS'
        with self.assertRaises(ValueError):run(d)
    def test_report_10_modules(self):
        d=fixture();t=render(dict(variant_id=d['identity']['variant_id'],case_pipeline=d));self.assertEqual(t.count('## 模块'),10);self.assertIn('PVS1_VeryStrong',t)
    def test_report_mixed_inputs_reject(self):
        with self.assertRaises(ValueError):render(dict(case_pipeline=fixture(),scoring={}))
    def test_VCEP_cannot_use_generic_by_default(self):
        d=fixture();d['routing']['outcome']='applicable';r=run(d);self.assertIsNone(r['authoritative_candidate']);self.assertIn('VCEP_full_materials_incomplete',r['blockers'])
    def test_BA1_all_nine_exact_ids(self):
        for v in TABLE['variants']:
            for key in ('allele_registry_id','clinvar_variation_id','hgvs','coordinate'):self.assertEqual(match({key:v[key]})['status'],'exception_match')
    def test_BA1_conflicting_aliases(self):self.assertEqual(match(dict(allele_registry_id='CA172210',clinvar_variation_id='9'))['status'],'identity_unresolved')
    def test_BA1_other_build(self):
        c=copy.deepcopy(TABLE['variants'][1]['coordinate']);c['build']='GRCh38';self.assertEqual(match(dict(coordinate=c))['status'],'identity_unresolved')
    def test_BA1_negative_never_benign(self):
        r=match(dict(allele_registry_id='CA_NOT_LISTED'));self.assertEqual(r['status'],'not_in_snapshot');self.assertIsNone(r['BA1_eligible'])
    def test_BA1_missing_identity(self):self.assertEqual(match({})['status'],'identity_unresolved')
    def test_BA1_version_not_silently_stripped(self):self.assertEqual(match(dict(hgvs='NM_004004.6:c.109G>A'))['status'],'not_in_snapshot')

if __name__=='__main__':unittest.main()
