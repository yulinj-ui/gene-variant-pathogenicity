import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_helpers import pm3, pp1pp4, functional
from test_v2 import case
from score import score
from render_report import render


def review(*keys):
    return dict({k:True for k in keys},reviewer='synthetic reviewer',reviewed_at='2026-09-27',
                source='synthetic fixture',rationale='synthetic calculation test; not a patient')


def pmdata(phase='trans',partner='P',count=1):
    return {'review':review('recessive_disease','disease_applicability','frequency_threshold_validated','case_independence_reviewed','vcep_checked'),
        'cases':[{'id':f'case{i}','family_id':f'family{i}','phase':phase,'partner_class':partner,
          'partner_variant_id':f'variant{i}','source_ids':['synthetic'],
          'review':review('affected','target_rare','partner_rare','independent_partner_classification','phase_or_homozygosity_reviewed')} for i in range(count)]}


def ppdata(n):
    return {'joint_points':n,'review':review('applicability_reviewed','phase_reviewed','penetrance_reviewed',
        'independence_reviewed','probability_allocation_reviewed','cap_reviewed')}


def fdata(n):
    return {'odds_path':n,'review':review('mechanism_matched','assay_validated',
        'controls_independently_classified','replicates_reviewed','calibration_reviewed','vcep_checked')}


class V3Tests(unittest.TestCase):
    def test_report_recomputes_helpers_separately(self):
        d={'scoring':case([('PM2_Supporting',1)]),'review_calculations':{'pm3':pmdata(count=2)}}
        out=render(d)
        self.assertIn('- 积分：1',out);self.assertIn('未导入主积分',out)
        self.assertIn('\"bayesian_weight\": 4',out);self.assertEqual(out.count('## 模块 '),10)
    def test_report_rejects_unknown_helper(self):
        with self.assertRaises(ValueError):render({'scoring':case([]),'review_calculations':{'ba1':{}}})
    def test_pvs1_pm4_all_strengths_both_orders(self):
        for code,n in [('PVS1',8),('PVS1_Strong',4),('PVS1_Moderate',2),('PVS1_Supporting',1)]:
            for codes in [[(code,n),('PM4',2)],[('PM4',2),(code,n)]]:
                r=score(case(codes));self.assertIn('PVS1_PM4_double_counting',r['blockers']);self.assertIsNone(r['point_candidate'])
    def test_pm4_independent_still_allowed(self):
        self.assertEqual(score(case([('PM4',2),('PS3',4)]))['point_candidate'],'LP')
    def test_profile_not_silently_ignored(self):
        d=case([('PVS1',8)]);d['points_profile']='ACGS_2024'
        with self.assertRaises(ValueError):score(d)
    def test_helper_not_imported(self):
        d=case([('PVS1',8)]);d['helper_results']={'pm3':{'points':4}}
        with self.assertRaises(ValueError):score(d)
    def test_tavtigian_benign_boundary_retained(self):
        self.assertEqual(score(case([('BS1',-4),('BP1',-1),('BP4',-1)]))['point_candidate'],'LB')
        self.assertEqual(score(case([('BS1',-4),('BP1',-1),('BP4',-1),('BP7',-1)]))['point_candidate'],'B')
    def test_pm3_case_vs_bayesian_points(self):
        r=pm3(pmdata(count=2));self.assertEqual(r['case_points'],'2');self.assertEqual(r['bayesian_weight'],4)
        self.assertIsNone(r['evidence_code']);self.assertIsNone(r['classification'])
    def test_pm3_phase_unknown_P_vs_LP(self):
        self.assertEqual(pm3(pmdata('unknown','P',2))['strength'],'Moderate')
        self.assertEqual(pm3(pmdata('unknown','LP',2))['strength'],'Supporting')
    def test_pm3_trans_LP_is_half_point(self):
        # SVI PM3 v1.0: confirmed-in-trans P=1.0, LP=0.5 (not 1.0).
        self.assertEqual(pm3(pmdata('trans','LP',1))['case_points'],'0.5')
        self.assertEqual(pm3(pmdata('trans','LP',2))['strength'],'Moderate')
        self.assertEqual(pm3(pmdata('trans','LP',4))['strength'],'Strong')
        self.assertEqual(pm3(pmdata('trans','P',1))['case_points'],'1')
        self.assertEqual(pm3(pmdata('trans','P',2))['case_points'],'2')
    def test_pm3_all_strength_thresholds(self):
        for count,strength in [(1,None),(2,'Supporting'),(4,'Moderate'),(8,'Strong'),(16,'VeryStrong')]:
            self.assertEqual(pm3(pmdata('unknown','LP',count))['strength'],strength)
    def test_pm3_homo_cap(self):
        r=pm3(pmdata('homozygous',count=8));self.assertEqual(r['case_points'],'1');self.assertEqual(r['strength'],'Moderate')
    def test_pm3_vus_cap_and_unknown(self):
        self.assertEqual(pm3(pmdata('trans','VUS',8))['case_points'],'0.5')
        self.assertIsNone(pm3(pmdata('unknown','VUS',8))['strength'])
    def test_pm3_missing_prerequisite_no_partial_candidate(self):
        d=pmdata(count=2);d['cases'][1]['review']['affected']=False
        r=pm3(d);self.assertIsNone(r['case_points']);self.assertIsNone(r['strength']);self.assertEqual(r['status'],'blocked')
    def test_pm3_no_truthy_string(self):
        d=pmdata();d['review']['vcep_checked']='true';self.assertEqual(pm3(d)['status'],'blocked')
    def test_pm3_duplicate_cases_and_families(self):
        for field in ['id','family_id']:
            d=pmdata(count=2);d['cases'][1][field]=d['cases'][0][field]
            with self.assertRaises(ValueError):pm3(d)
    def test_pm3_invalid_partner_phase(self):
        for phase,partner in [('cis','P'),('trans','B')]:
            with self.assertRaises(ValueError):pm3(pmdata(phase,partner))
    def test_pm3_missing_sources_and_review(self):
        d=pmdata();d['cases'][0]['source_ids']=[];self.assertEqual(pm3(d)['status'],'blocked')
        d=pmdata();d['review'].pop('reviewer');self.assertEqual(pm3(d)['status'],'blocked')
    def test_pm3_empty(self):
        self.assertEqual(pm3(pmdata(count=0))['status'],'blocked')
    def test_pp1_table4_all_intervals(self):
        expected=[[],[['PP1_Supporting'],['PP4_Supporting']],
          [['PP1_Moderate'],['PP4_Moderate'],['PP1_Supporting','PP4_Supporting']],
          [['PP1_Supporting','PP4_Moderate'],['PP4_Supporting','PP1_Moderate']],
          [['PP1_Strong'],['PP4_Strong'],['PP1_Moderate','PP4_Moderate']],
          [['PP1_Strong','PP4_Supporting'],['PP4_Strong','PP1_Supporting']]]
        for n in ['0','.9','1','1.9','2','2.9','3','3.9','4','4.9','5']:
            self.assertEqual(pp1pp4(ppdata(n))['maximum_code_options'],expected[int(float(n))])
    def test_pp1_no_automatic_code_choice(self):
        r=pp1pp4(ppdata('3.4'));self.assertIsNone(r['selected_codes']);self.assertFalse(r['automatic_score_import'])
    def test_pp1_no_silent_round_or_cap(self):
        for n in ['3.99','5.1','-1','NaN',True]:
            with self.assertRaises(ValueError):pp1pp4(ppdata(n))
    def test_pp1_all_gates_required(self):
        d=ppdata(4);d['review']['probability_allocation_reviewed']=False
        self.assertIsNone(pp1pp4(d)['maximum_code_options'])
    def test_functional_strict_boundaries(self):
        pairs=[('.0529','BS3_Strong'),('.053','BS3_Moderate'),('.2299','BS3_Moderate'),('.23','BS3_Supporting'),
            ('.4799','BS3_Supporting'),('.48','Indeterminate'),('2.1','Indeterminate'),('2.1001','PS3_Supporting'),
            ('4.3','PS3_Supporting'),('4.3001','PS3_Moderate'),('18.7','PS3_Moderate'),('18.7001','PS3_Strong'),
            ('350','PS3_Strong'),('350.001','PS3_VeryStrong')]
        for n,b in pairs:self.assertEqual(functional(fdata(n))['band'],b)
    def test_functional_count_or_species_cannot_assign(self):
        d=fdata(None);d.update(validation_controls=100,species='mouse')
        self.assertIsNone(functional(d)['band'])
    def test_functional_validation_required(self):
        d=fdata(400);d['review']['assay_validated']=False;self.assertIsNone(functional(d)['band'])
    def test_functional_invalid_odds(self):
        for n in ['NaN','Infinity',0,-1,True]:
            with self.assertRaises(ValueError):functional(fdata(n))

if __name__=='__main__':unittest.main()
