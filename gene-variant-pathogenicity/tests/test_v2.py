import copy
import json
import sys
import unittest
from decimal import Decimal
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from compare_frameworks import compare
from evidence_helpers import revel_band, de_novo_strength
from report_audit import citation_coverage, sample_qc, search_statement
from render_report import render
from test_migration import sources, HGVS, scored
import score
import genebe_fields


def case(codes):
    d=scored();d['rules']={};d['evidence']=[]
    for i,(code,pts) in enumerate(codes):
        key=f'r{i}'; r=scored(str(pts))
        d['rules'][key]=dict(r['rules']['test-rule'],code=code)
        d['evidence'].append(dict(r['evidence'][0],id=f'e{i}',code=code,rule_id=key,basis_ids=[f'b{i}']))
    return d

class ComparisonTests(unittest.TestCase):
    def test_strong_pair_disagreement(self):
        r=score.score(case([('PS1',4),('PS3',4)]))
        self.assertEqual(r['point_candidate'],'LP')
        self.assertEqual(r['acmg_2015_comparison']['candidate'],'P')
        self.assertTrue(r['framework_disagreement']);self.assertIsNone(r['classification'])
    def test_pm2_supporting_does_not_restore_moderate(self):
        r=score.score(case([('PVS1',8),('PM2_Supporting',1)]))
        self.assertEqual(r['point_candidate'],'LP');self.assertEqual(r['acmg_2015_comparison']['candidate'],'VUS')
    def test_all_table5_pathogenic_routes(self):
        routes=[([('PVS1',8),('PS1',4)],'P1a'),([('PVS1',8),('PM1',2),('PM2',2)],'P1b'),
                ([('PVS1',8),('PM1',2),('PP1',1)],'P1c'),([('PVS1',8),('PP1',1),('PP2',1)],'P1d'),
                ([('PS1',4),('PS3',4)],'P2'),([('PS1',4),('PM1',2),('PM2',2),('PM3',2)],'P3a'),
                ([('PS1',4),('PM1',2),('PM2',2),('PP1',1),('PP2',1)],'P3b'),
                ([('PS1',4),('PM1',2),('PP1',1),('PP2',1),('PP3',1),('PP4',1)],'P3c')]
        for codes,route in routes:
            with self.subTest(route=route):
                r=compare(case(codes)['evidence']);self.assertEqual(r['candidate'],'P');self.assertIn(route,r['matched_rules'])
    def test_all_table5_likely_pathogenic_routes(self):
        routes=[([('PVS1',8),('PM1',2)],'LP1'),([('PS1',4),('PM1',2)],'LP2'),
                ([('PS1',4),('PP1',1),('PP2',1)],'LP3'),([('PM1',2),('PM2',2),('PM3',2)],'LP4'),
                ([('PM1',2),('PM2',2),('PP1',1),('PP2',1)],'LP5'),
                ([('PM1',2),('PP1',1),('PP2',1),('PP3',1),('PP4',1)],'LP6')]
        for codes,route in routes:
            with self.subTest(route=route):
                r=compare(case(codes)['evidence']);self.assertEqual(r['candidate'],'LP');self.assertIn(route,r['matched_rules'])
    def test_benign_and_likely_benign(self):
        for codes,expected in [([('BS1',-4),('BS3',-4)],'B'),([('BS1',-4),('BP1',-1)],'LB'),([('BP1',-1),('BP4',-1)],'LB')]:
            self.assertEqual(compare(case(codes)['evidence'])['candidate'],expected)
    def test_opposing_directions(self):
        r=score.score(case([('PVS1',8),('PM2',2),('BS1',-4)]))
        self.assertEqual(r['acmg_2015_comparison']['candidate'],'VUS');self.assertTrue(r['framework_disagreement'])
    def test_unsupported_benign_strength_not_rounded(self):
        r=score.score(case([('BP4_Moderate',-2)]))
        self.assertEqual(r['point_candidate'],'LB');self.assertIsNone(r['acmg_2015_comparison']['candidate'])
    def test_unknown_codes_blocked(self):
        for code in ['PS99','PP3_Strng','PVS2']:
            r=score.score(case([(code,10)]));self.assertIsNone(r['point_candidate'])
            self.assertEqual(r['excluded'][0]['reason'],'unsupported_evidence_code')
    def test_snv_codes_not_accepted_as_cnv(self):
        d=case([('PVS1',8)]);d['framework']='CNV_GAIN';d['combination_policy']['framework']='CNV_GAIN'
        for r in d['rules'].values():r['framework']='CNV_GAIN'
        for r in d['evidence']:r['framework']='CNV_GAIN'
        self.assertIsNone(score.score(d)['point_candidate'])
    def test_cnv_unconverted_points_blocked(self):
        d=scored('8','CNV_GAIN');d['rules']['test-rule']['code']='2I';d['evidence'][0]['code']='2I'
        self.assertEqual(score.score(d)['excluded'][0]['reason'],'CNV_item_points_outside_supported_range')
    def test_ba1_disabled(self):
        r=score.score(case([('BA1',-8)]));self.assertIsNone(r['point_candidate'])
    def test_duplicate_code_family(self):
        r=score.score(case([('PP3',1),('PP3_Strong',4)]));self.assertEqual(r['excluded'][0]['reason'],'duplicate_code_family')
    def test_strength_mismatch(self):
        r=score.score(case([('PM2_Supporting',2)]));self.assertEqual(r['excluded'][0]['reason'],'code_points_mismatch')
    def test_de_novo_not_double_counted(self):
        self.assertIsNone(score.score(case([('PS2',4),('PM6',2)]))['point_candidate'])
    def test_pm1_pp3_cap(self):
        r=score.score(case([('PM1',2),('PP3_Strong',4)]));self.assertIn('PM1_PP3_combined_strength_exceeds_Strong',r['blockers'])
        self.assertEqual(score.score(case([('PM1',2),('PP3_Moderate',2)]))['point_candidate'],'VUS')
    def test_splice_prediction_overlap(self):
        r=score.score(case([('PVS1',8),('PP3',1)]));self.assertIsNone(r['point_candidate'])
    def test_fractional_snv_disabled(self):
        d=scored('2.5');self.assertIsNone(score.score(d)['point_candidate'])
    def test_cnv_not_subject_to_snv_comparator(self):
        r=score.score(scored('-.60','CNV_LOSS'));self.assertEqual(r['point_candidate'],'VUS');self.assertEqual(r['acmg_2015_comparison']['status'],'not_applicable')
    def test_cnv_single_item(self):
        self.assertEqual(score.score(scored('1','CNV_GAIN'))['point_candidate'],'P')

class HelpersTests(unittest.TestCase):
    def test_single_source_allowed_but_not_crosschecked(self):
        d=sources();d['genebe']=None;r=genebe_fields.to_evidence(HGVS,d)
        self.assertTrue(r['protein_gate']['usable_for_consequence_review']);self.assertFalse(r['protein_gate']['passed'])
    def test_conflict_not_usable(self):
        d=sources();d['genebe']['variants'][0]['consequences'][0]['hgvs_p']='p.Arg10Ter'
        self.assertFalse(genebe_fields.to_evidence(HGVS,d)['protein_gate']['usable_for_consequence_review'])
    def test_identity_missing_not_usable(self):
        self.assertFalse(genebe_fields.to_evidence(HGVS,{})['protein_gate']['usable_for_consequence_review'])
    def test_revel_edges(self):
        for n,band in [('0','BP4_VeryStrong'),('.003','BP4_VeryStrong'),('.0031','BP4_Strong'),('.016','BP4_Strong'),('.0161','BP4_Moderate'),('.183','BP4_Moderate'),('.1831','BP4_Supporting'),('.290','BP4_Supporting'),('.2901','Indeterminate'),('.6439','Indeterminate'),('.644','PP3_Supporting'),('.773','PP3_Moderate'),('.932','PP3_Strong'),('1','PP3_Strong')]:
            with self.subTest(n=n):
                r=revel_band(n,missense=True,identity_validated=True,calibration_selected=True)
                self.assertEqual(r['band'],band);self.assertIsNone(r['evidence_code'])
    def test_revel_missing_or_unreviewed(self):
        self.assertIsNone(revel_band(None)['band']);self.assertIsNone(revel_band('.99')['band'])
        self.assertIsNone(revel_band('.99',missense='true',identity_validated=True,calibration_selected=True)['band'])
    def test_revel_invalid(self):
        for n in ['NaN',2,-1,True]:
            with self.assertRaises(ValueError):revel_band(n)
    def test_de_novo_no_gaps(self):
        for n,s in [('.25',None),('.5','Supporting'),('.75','Supporting'),('1','Moderate'),('1.75','Moderate'),('2','Strong'),('3.75','Strong'),('4','VeryStrong')]:
            self.assertEqual(de_novo_strength(n)['strength_before_inheritance_adjustments'],s)
    def test_de_novo_heterogeneity_cap(self):
        r=de_novo_strength('0','4');self.assertEqual(r['case_points'],'1');self.assertEqual(r['strength_before_inheritance_adjustments'],'Moderate')
    def test_de_novo_subtotals_separate(self):
        self.assertEqual(de_novo_strength('2','4')['case_points'],'3')
    def test_citation_actual_coverage(self):
        rows=[{'id':'a','metadata_verified':True,'claim_verified':True},{'id':'b','metadata_verified':True,'claim_verified':False}]
        self.assertEqual(citation_coverage(rows)['coverage_percent'],'50')
        self.assertIsNone(citation_coverage([])['coverage_percent'])
        with self.assertRaises(ValueError):citation_coverage(rows+rows)
    def test_qc_values_do_not_activate_unvalidated_policy(self):
        for v in [.3,.5,.99]:
            r=sample_qc({'vaf':v,'depth':10000,'mcc':0,'validated':True})
            self.assertFalse(r['automatic_acceptance']);self.assertIsNone(r['mosaicism']);self.assertIsNone(r['validated_lod']);self.assertIsNone(r['gonadal_risk_upper_bound'])
    def test_failed_search_never_novel(self):
        self.assertIn('检索未完成',search_statement(None,[],'failed'))
        self.assertIn('所列',search_statement('2026-09-26',['ClinVar'],'success'))
    def test_render_same_score_source(self):
        data={'scoring':case([('PS1',4),('PS3',4)]),'citations':[]}
        text=render(data)
        self.assertIn('测试候选分区：LP',text);self.assertIn('2015组合对照：P',text)
        self.assertEqual(text.count('## 模块 '),10)
        self.assertIn('"coverage_percent": null',text)
        self.assertIn('正式分类：未完成',text)
        self.assertIn('| 证据ID | 代码 | 分值 | 原因 |\n|---|---|---|---|\n| e0',text)

if __name__=='__main__':unittest.main()
