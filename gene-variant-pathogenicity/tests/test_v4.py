import copy
import sys
import unittest
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from locus_review import calculate, table2, exact, TABLE2, COMMON_GATES, PP4_GATES, JOINT_GATES
from test_v3 import review
from test_v2 import case
from score import score
from render_report import render

def fixture(y='0.958',n=2,mode='pp4_equal'):
    p=dict(packet_id='demo-packet',subject_id='synthetic-subject',allele_id='paternal',
       variant_ids=['demo-v'+str(i) for i in range(n)],basis_ids=['synthetic-observation'],mode=mode,
       source=dict(kind='published',url='https://pmc.ncbi.nlm.nih.gov/articles/PMC10806742/',version='2024',
          location='Figure 2; synthetic fixture, not a patient',gene='CTNS',disease='synthetic cystinosis scenario',
          phenotype_definition='synthetic matched phenotype',testing_method='synthetic matched method'),
       review=review(*(COMMON_GATES+(PP4_GATES if mode=='pp4_equal' else JOINT_GATES))))
    if mode=='pp4_equal':p.update(diagnostic_yield=y,inheritance='AR',locus_model='homogeneous',allocation='equal',segregation_present=False)
    else:p['joint_points']=y
    return {'packets':[p]}

def report_case():
    return dict(variant_id='demo-v0',subject_id='synthetic-subject',scoring=case([('PM2_Supporting',1)]),
                review_calculations={'locus_review':fixture()})

class V4Tests(unittest.TestCase):
    def test_equal_published_case(self):
        r=calculate(fixture())['packets'][0]
        self.assertEqual([v['allocated_probability'] for v in r['results']],['0.479']*2)
        self.assertEqual([v['review_points'] for v in r['results']],['2.5']*2)
        self.assertEqual(r['allocation']['allocated_sum'],'0.958')
    def test_single_cap(self):
        r=calculate(fixture(n=1))['packets'][0]['results'][0]
        self.assertEqual(r['table2_points_before_cap'],'7');self.assertEqual(r['review_points'],'5')
    def test_table_all_thresholds_and_just_below(self):
        for i,(pct,pt) in enumerate(TABLE2):
            p=Fraction(pct)/100;self.assertEqual(table2(p),Fraction(pt))
            self.assertEqual(table2(p-Fraction(1,10**12)),None if i==0 else Fraction(TABLE2[i-1][1]))
    def test_source_table_transcription(self):
        import json
        rows=json.loads((Path(__file__).resolve().parents[1]/'references/table2-source-v4.json').read_text())['rows']
        self.assertEqual(TABLE2,[tuple(x) for x in rows])
    def test_precise_allocation_not_rounded(self):
        r=calculate(fixture('0.829999999999999999999999999999999999'))['packets'][0]['results'][0]
        self.assertEqual(r['review_points'],'2')
        self.assertEqual(r['allocated_probability'],'0.4149999999999999999999999999999999995')
    def test_outside_table_is_unmapped(self):
        for y in ['0','0.1','0.190999','1']:
            r=calculate(fixture(y,n=1));self.assertEqual(r['status'],'blocked');self.assertEqual(r['packets'][0]['results'],[])
    def test_bad_numeric(self):
        for y in [True,.958,'NaN','Infinity','-1','1e-2','95.8']:
            with self.assertRaises(ValueError):calculate(fixture(y))
    def test_each_review_required(self):
        for k in COMMON_GATES+PP4_GATES+['reviewer','reviewed_at','source','rationale']:
            d=fixture();d['packets'][0]['review'].pop(k)
            r=calculate(d);self.assertEqual(r['status'],'blocked');self.assertEqual(r['packets'][0]['results'],[])
    def test_truthy_review_rejected(self):
        d=fixture();d['packets'][0]['review']['phase_reviewed']='true';self.assertEqual(calculate(d)['status'],'blocked')
    def test_unverified_local_disabled(self):
        d=fixture();d['packets'][0]['source']['kind']='local';self.assertEqual(calculate(d)['status'],'blocked')
    def test_missing_yield_source_details(self):
        for k in ['url','version','location','gene','disease','phenotype_definition','testing_method']:
            d=fixture();d['packets'][0]['source'].pop(k);self.assertEqual(calculate(d)['status'],'blocked')
    def test_disabled_scopes(self):
        for k,v in [('allocation','unequal'),('inheritance','AD'),('locus_model','heterogeneous'),('segregation_present',True)]:
            d=fixture();d['packets'][0][k]=v;self.assertEqual(calculate(d)['status'],'blocked')
        self.assertEqual(calculate(fixture(n=3))['status'],'blocked')
    def test_unknown_fields_not_ignored(self):
        d=fixture();d['packets'][0]['bs4_points']='-4'
        with self.assertRaises(ValueError):calculate(d)
    def test_duplicate_variants_in_packet(self):
        d=fixture();d['packets'][0]['variant_ids']=['v','v']
        with self.assertRaises(ValueError):calculate(d)
    def test_duplicate_basis_in_packet(self):
        d=fixture();d['packets'][0]['basis_ids']=['b','b']
        with self.assertRaises(ValueError):calculate(d)
    def test_repeated_packet_and_variant_and_basis(self):
        for field in ['packet_id','variant_ids','basis_ids']:
            d=fixture(n=1);p=copy.deepcopy(d['packets'][0]);p.update(packet_id='other',variant_ids=['other'],basis_ids=['other'])
            p[field]=d['packets'][0][field];d['packets'].append(p)
            with self.assertRaises(ValueError):calculate(d)
    def test_joint_cap_and_table4(self):
        r=calculate(fixture('6.5',1,'reviewed_joint_cap'))['packets'][0]['results'][0]
        self.assertEqual(r['review_points'],'5');self.assertEqual(len(r['table4_maximum_options']),2)
        self.assertIsNone(r['selected_codes'])
    def test_joint_retains_fraction(self):
        r=calculate(fixture('2.5',1,'reviewed_joint_cap'))['packets'][0]['results'][0]
        self.assertEqual(r['review_points'],'2.5');self.assertEqual(len(r['table4_maximum_options']),3)
    def test_joint_no_rounding(self):
        with self.assertRaises(ValueError):calculate(fixture('2.59',1,'reviewed_joint_cap'))
    def test_joint_no_allocation(self):self.assertEqual(calculate(fixture('5',2,'reviewed_joint_cap'))['status'],'blocked')
    def test_joint_all_gates(self):
        for k in COMMON_GATES+JOINT_GATES:
            d=fixture('5',1,'reviewed_joint_cap');d['packets'][0]['review'].pop(k);self.assertEqual(calculate(d)['status'],'blocked')
    def test_never_outputs_clinical_decision(self):
        r=calculate(fixture());self.assertFalse(r['automatic_score_import']);self.assertIsNone(r['classification']);self.assertIsNone(r['evidence_code'])
    def test_report_ten_modules_separate_score(self):
        t=render(report_case());self.assertEqual(t.count('## 模块 '),10);self.assertIn('- 积分：1',t);self.assertIn('2.5',t);self.assertIn('未导入主积分',t)
    def test_report_overlap_blocks(self):
        d=report_case();d['scoring']['evidence'][0]['basis_ids']=['synthetic-observation']
        with self.assertRaises(ValueError):render(d)
    def test_report_locus_main_codes_block_even_with_new_basis(self):
        d=report_case();d['scoring']=case([('PP4',1)])
        with self.assertRaises(ValueError):render(d)
    def test_report_subject_and_variant_match(self):
        for k,v in [('variant_id','other'),('subject_id','other'),('variant_id',None)]:
            d=report_case();d[k]=v
            with self.assertRaises(ValueError):render(d)
    def test_report_legacy_helper_rejected(self):
        from test_v3 import ppdata
        d=report_case();d['review_calculations']['pp1pp4']=ppdata('2.5')
        with self.assertRaises(ValueError):render(d)
    def test_primary_rejects_injection(self):
        for key in ['locus_packets','locus_results','fractional_points','review_calculations']:
            d=case([('PM2_Supporting',1)]);d[key]={}
            with self.assertRaises(ValueError):score(d)
    def test_fractional_main_score_still_disabled(self):
        d=case([('PP4',1)]);d['evidence'][0]['points']='2.5'
        for r in d['rules'].values():r['allowed_points']=['2.5']
        self.assertIn('some_evidence_excluded',score(d)['blockers'])
