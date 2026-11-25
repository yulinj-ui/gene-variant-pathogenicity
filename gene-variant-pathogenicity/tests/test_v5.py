import copy,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from pvs1_review import evaluate,PATHS,GATES
from test_v3 import review
from test_v2 import case
from render_report import render
from score import score

# Explicit scenario fixtures derived from the documented source paths, not engine-generated routes.
CASES={
'N01':{'nmd':True},'N02':{'nmd':True,'exon_present':False},
'N03':{'nmd':False,'region':'critical'},'N04':{'nmd':False,'lof_common':True},
'N05':{'nmd':False,'removed_aa':11},'N06':{'nmd':False,'removed_aa':9},
'S01':{'consequence':'out_of_frame_nmd'},'S02':{'consequence':'out_of_frame_nmd','exon_present':False},
'S03':{'consequence':'out_of_frame_no_nmd','region':'critical'},'S04':{'consequence':'out_of_frame_no_nmd','lof_common':True},
'S05':{'consequence':'out_of_frame_no_nmd','removed_aa':11},'S06':{'consequence':'out_of_frame_no_nmd','removed_aa':9},
'S07':{'consequence':'in_frame','lof_common':True},'S08':{'consequence':'in_frame','removed_aa':11},
'S09':{'consequence':'in_frame','removed_aa':9},'S10':{'consequence':'in_frame','region':'critical'},
'D01':{'consequence':'whole_gene'},'D02':{'consequence':'out_of_frame_nmd'},'D03':{'consequence':'out_of_frame_nmd','exon_present':False},
'D04':{'consequence':'out_of_frame_no_nmd','region':'critical'},'D05':{'consequence':'out_of_frame_no_nmd','lof_common':True},
'D06':{'consequence':'out_of_frame_no_nmd','removed_aa':11},'D07':{'consequence':'out_of_frame_no_nmd','removed_aa':9},
'D08':{'consequence':'in_frame','lof_common':True},'D09':{'consequence':'in_frame','removed_aa':11},'D10':{'consequence':'in_frame','removed_aa':9},'D11':{'consequence':'in_frame','region':'critical'},
'U01':{'tandem':'confirmed','effect':'no_effect'},'U02':{'tandem':'confirmed','effect':'disrupts_frame_and_nmd'},
'U03':{'tandem':'presumed','effect':'assessed_unknown'},'U04':{'tandem':'presumed','effect':'disrupts_frame_and_nmd'},'U05':{'tandem':'non_tandem'},
'I01':{'alternative_start':False,'upstream_pathogenic':True},'I02':{'alternative_start':False,'upstream_pathogenic':False},'I03':{'alternative_start':True}}
KIND={'N':'nonsense_frameshift','S':'canonical_splice','D':'deletion','U':'duplication','I':'initiation'}
def fixture(path='N01'):
    kind=KIND[path[0]]
    f={'exon_present':True,'lof_common':False}
    if path[0] in 'NSD':f.update(region='assessed_unknown',removed_aa=11,protein_length=100)
    if path[0]=='U':f.update(length_known=True,whole_gene=False,external_insertion=False)
    f.update(CASES[path])
    d=dict(kind=kind,identity=dict(variant_id='synthetic-v1',build='GRCh38',genomic_change='synthetic-only',transcript='NM_TEST.1',gene='SYNTHETIC',disease='synthetic disease',inheritance='AD'),
       review=review(*GATES),source_version='AbouTayoun_2018_generic',vcep_policy='reviewed_generic_applicable',basis_ids=['synthetic-pvs1-basis'],
       facts_review={k:dict(source='synthetic example, not patient evidence',location='synthetic fact record',rationale='engineering test only') for k in ['nmd_or_frame','exon_relevance','population_tolerance','critical_region_or_start','mechanism']},
       mechanism=dict(lof_mechanism='established',association='definitive',independent_pathogenic_lof_count=3,phenotype_lof_count=3,phenotype_total_count=10,associated_lof_count=3,multiple_exons=True,single_exon_gene=False,null_mouse=False),
       scenarios=[dict(id='scenario1',facts=f)])
    if path[0]=='S':d['splice_review']=dict(canonical_gt_ag_plusminus_1_2=True,cryptic_sites_within_20nt_reviewed=True,scenarios_complete=True,later_splicing_guidance_reviewed=True,rna_data_present=False)
    return d
class V5Tests(unittest.TestCase):
    def test_all_source_paths_have_fixtures(self):self.assertEqual(set(CASES),set(PATHS))
    def test_no_mechanism(self):
        d=fixture();d['mechanism']['lof_mechanism']='absent';r=evaluate(d);self.assertEqual(r['status'],'not_applicable');self.assertIsNone(r['adjusted_strength'])
    def test_g1_not_cumulatively_downgraded(self):
        d=fixture();d['mechanism']['null_mouse']=True;self.assertEqual(evaluate(d)['adjusted_strength'],'VeryStrong')
    def test_g2(self):
        d=fixture();d['mechanism'].update(association='moderate',null_mouse=True);r=evaluate(d);self.assertEqual(r['mechanism_tier'],'G2');self.assertEqual(r['adjusted_strength'],'Strong')
    def test_g3_human_only(self):
        d=fixture();d['mechanism']['association']='moderate';self.assertEqual(evaluate(d)['adjusted_strength'],'Moderate')
    def test_g3_mouse_only(self):
        d=fixture();d['mechanism'].update(association='moderate',independent_pathogenic_lof_count=0,associated_lof_count=0,null_mouse=True);self.assertEqual(evaluate(d)['adjusted_strength'],'Moderate')
    def test_below_supporting_pending(self):
        d=fixture('I02');d['mechanism'].update(association='moderate',null_mouse=True);r=evaluate(d);self.assertEqual(r['status'],'blocked');self.assertIsNone(r['adjusted_strength'])
    def test_exact_mechanism_ten_percent(self):
        d=fixture();d['mechanism']['phenotype_total_count']=30;self.assertIn('Table1_exactly_10_percent_conflicts_with_prose',evaluate(d)['blockers'])
    def test_single_exon_exception(self):
        d=fixture();d['mechanism'].update(single_exon_gene=True,multiple_exons=False);self.assertEqual(evaluate(d)['adjusted_strength'],'VeryStrong')
    def test_no_tier(self):
        d=fixture();d['mechanism'].update(association='limited');self.assertEqual(evaluate(d)['status'],'blocked')
    def test_exact_protein_ten_percent(self):
        d=fixture('N05');d['scenarios'][0]['facts']['removed_aa']=10;self.assertEqual(evaluate(d)['status'],'blocked')
    def test_precise_ratio(self):
        for lost,expected in [(100000000000000001,'N05'),(99999999999999999,'N06')]:
            d=fixture('N05');d['scenarios'][0]['facts'].update(removed_aa=lost,protein_length=1000000000000000000)
            self.assertEqual(evaluate(d)['path_results'][0]['path_id'],expected)
    def test_unknown_nmd_not_false(self):
        d=fixture();d['scenarios'][0]['facts']['nmd']='unknown';r=evaluate(d);self.assertEqual(r['status'],'blocked');self.assertIsNone(r['adjusted_strength'])
    def test_missing_population_blocks_positive_nmd(self):
        d=fixture();d['scenarios'][0]['facts'].pop('lof_common');self.assertEqual(evaluate(d)['status'],'blocked')
    def test_global_population_exclusion_on_nmd(self):
        d=fixture();d['scenarios'][0]['facts']['lof_common']=True;r=evaluate(d);self.assertEqual(r['path_results'][0]['path_id'],'N01');self.assertEqual(r['status'],'not_applicable')
    def test_critical_region_does_not_override_transcript_exclusion(self):
        d=fixture('N03');d['scenarios'][0]['facts']['exon_present']=False;self.assertEqual(evaluate(d)['status'],'not_applicable')
    def test_known_noncritical_not_unknown(self):
        d=fixture('N05');d['scenarios'][0]['facts']['region']='proven_noncritical';self.assertEqual(evaluate(d)['status'],'blocked')
    def test_unknown_length(self):
        d=fixture('U02');d['scenarios'][0]['facts']['length_known']=False;self.assertEqual(evaluate(d)['status'],'blocked')
    def test_whole_gene_duplication(self):
        d=fixture('U02');d['scenarios'][0]['facts']['whole_gene']=True;self.assertEqual(evaluate(d)['status'],'not_applicable')
    def test_external_insertion(self):
        d=fixture('U02');d['scenarios'][0]['facts']['external_insertion']=True;self.assertEqual(evaluate(d)['status'],'not_applicable')
    def test_splice_weakest(self):
        d=fixture('S01');d['scenarios'].append(dict(id='second',facts=fixture('S09')['scenarios'][0]['facts']));self.assertEqual(evaluate(d)['adjusted_strength'],'Moderate')
    def test_splice_no_applicable_dominates(self):
        d=fixture('S01');d['scenarios'].append(dict(id='second',facts=fixture('S02')['scenarios'][0]['facts']));self.assertEqual(evaluate(d)['status'],'not_applicable')
    def test_incomplete_scenario_blocks_all(self):
        d=fixture('S01');d['scenarios'].append(dict(id='second',facts={}));self.assertEqual(evaluate(d)['status'],'blocked');self.assertIsNone(evaluate(d)['adjusted_strength'])
    def test_splice_gates(self):
        for k in fixture('S01')['splice_review']:
            d=fixture('S01');d['splice_review'].pop(k);self.assertEqual(evaluate(d)['status'],'blocked')
    def test_rna_not_automated(self):
        d=fixture('S01');d['splice_review']['rna_data_present']=True;self.assertEqual(evaluate(d)['status'],'blocked')
    def test_review_each_field(self):
        for k in GATES+['reviewer','reviewed_at','source','rationale']:
            d=fixture();d['review'].pop(k);self.assertEqual(evaluate(d)['status'],'blocked')
    def test_facts_provenance(self):
        d=fixture();d['facts_review'].pop('mechanism');self.assertEqual(evaluate(d)['status'],'blocked')
    def test_vcep_override_blocked(self):
        d=fixture();d['vcep_policy']='gene_specific';self.assertEqual(evaluate(d)['status'],'blocked')
    def test_transcript_version_required(self):
        d=fixture();d['identity']['transcript']='NM_TEST';self.assertEqual(evaluate(d)['status'],'blocked')
    def test_identity_each_field(self):
        for k in fixture()['identity']:
            d=fixture();d['identity'].pop(k);self.assertEqual(evaluate(d)['status'],'blocked')
    def test_source_injection_rejected(self):
        d=fixture();d['path_id']='N01'
        with self.assertRaises(ValueError):evaluate(d)
    def test_strict_boolean(self):
        d=fixture();d['scenarios'][0]['facts']['nmd']='true'
        with self.assertRaises(ValueError):evaluate(d)
    def test_duplicate_scenario(self):
        d=fixture('S01');d['scenarios']*=2
        with self.assertRaises(ValueError):evaluate(d)
    def test_no_classification(self):
        r=evaluate(fixture('D01'));self.assertIsNone(r['classification']);self.assertIsNone(r['evidence_code']);self.assertFalse(r['automatic_score_import'])

def make_path_test(path):
    def run(self):
        r=evaluate(fixture(path));self.assertEqual(r['path_results'][0]['path_id'],path)
        self.assertEqual(r['path_results'][0]['source_tree_output'],PATHS[path]['tree_output'])
        expected=None if PATHS[path]['tree_output']=='不适用PVS1' else ('VeryStrong' if PATHS[path]['tree_output'] in ['PVS1','PVS1（脚注d）'] else PATHS[path]['tree_output'].split('_')[1])
        self.assertEqual(r['adjusted_strength'],expected)
        self.assertEqual(r['status'],'not_applicable' if expected is None else 'test_calculation_only')
    return run
for path in CASES:setattr(V5Tests,'test_path_'+path,make_path_test(path))

class V5IntegrationTests(unittest.TestCase):
    def report(self):return dict(variant_id='synthetic-v1',scoring=case([('PM2_Supporting',1)]),review_calculations={'pvs1':fixture()})
    def test_report_separate(self):
        text=render(self.report());self.assertEqual(text.count('## 模块 '),10);self.assertIn('- 积分：1',text);self.assertIn('VeryStrong',text);self.assertIn('未导入主积分',text)
    def test_report_identity(self):
        d=self.report();d['variant_id']='wrong'
        with self.assertRaises(ValueError):render(d)
    def test_report_overlap(self):
        d=self.report();d['scoring']['evidence'][0]['basis_ids']=['synthetic-pvs1-basis']
        with self.assertRaises(ValueError):render(d)
    def test_no_code_double_count(self):
        for code,n in [('PVS1',8),('PM4',2),('PP3',1)]:
            d=self.report();d['scoring']=case([(code,n)])
            with self.assertRaises(ValueError):render(d)
    def test_primary_reject_import(self):
        for key in ['pvs1_results','pvs1_review']:
            d=case([('PM2_Supporting',1)]);d[key]=evaluate(fixture())
            with self.assertRaises(ValueError):score(d)
    def test_cnv_remains_separate(self):
        d=self.report();d['scoring']['framework']='CNV_LOSS'
        with self.assertRaises(ValueError):render(d)
