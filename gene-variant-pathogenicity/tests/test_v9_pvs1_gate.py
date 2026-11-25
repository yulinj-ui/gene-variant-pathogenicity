"""v9: PVS1 provenance gate regression tests (FRYL c.8547_8560del case and contract rules)."""
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from pvs1_review import evaluate
from score import score
from report_audit import pvs1_provenance, framework_reaudit
from test_v2 import case
from test_v5 import fixture as pvs1_fixture
from test_v5r1 import fixture as pipeline_fixture
from case_pipeline import run as pipeline_run


def lof_row(i, cls='LP', dependent=True, criteria=('PVS1', 'PS2', 'PM2')):
    return {'variant': 'v%d' % i, 'classification': cls,
            'criteria': list(criteria), 'pvs1_dependent': dependent}


def fryl_input(rows=None, mouse=None, manual_independent=0):
    d = pvs1_fixture('N01')
    d['identity'].update(variant_id='FRYL:NM_015030.2:c.8547_8560del', gene='FRYL',
                         disease='Pan-Chung-Bellen syndrome', inheritance='AD',
                         genomic_change='chr4:48501654 TTGATAAGTTTACAG>T')
    d['mechanism'].pop('lof_evidence', None)
    d['mechanism'].update(association='definitive', phenotype_lof_count=9,
                          phenotype_total_count=14, associated_lof_count=9,
                          independent_pathogenic_lof_count=manual_independent,
                          multiple_exons=True, single_exon_gene=False)
    if mouse is not None:
        d['mechanism']['null_mouse'] = mouse
    if rows is not None:
        d['mechanism']['lof_evidence'] = rows
    return d


FRYL_ROWS = [lof_row(i) for i in range(9)]


class FrylPvs1Tests(unittest.TestCase):
    def test_fryl_g3_moderate(self):
        mouse = {'model': 'Fryl-/- gene trap', 'pmid': '29409347',
                 'phenotype': 'perinatal lethality, growth retardation, hydronephrosis',
                 'heterozygous_phenotype': 'not reported',
                 'recapitulates': 'no'}
        r = evaluate(fryl_input(FRYL_ROWS, mouse=mouse))
        self.assertEqual(r['status'], 'test_calculation_only')
        self.assertEqual(r['mechanism_tier'], 'G3')
        self.assertEqual(r['adjusted_strength'], 'Moderate')
        self.assertTrue(r['counts_audited'])
        self.assertEqual(r['lof_evidence_audit']['computed_independent'], 0)

    def test_fryl_manual_count_claim_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(fryl_input(FRYL_ROWS, manual_independent=9))

    def test_manual_counts_without_evidence_not_audited(self):
        r = evaluate(fryl_input(None, manual_independent=3))
        self.assertEqual(r['mechanism_tier'], 'G1')
        self.assertEqual(r['adjusted_strength'], 'VeryStrong')
        self.assertFalse(r['counts_audited'])

    def test_mouse_partial_is_false(self):
        mouse = {'model': 'Fryl-/- gene trap', 'pmid': '29409347',
                 'phenotype': 'growth retardation', 'heterozygous_phenotype': 'unknown',
                 'recapitulates': 'partial'}
        r = evaluate(fryl_input(FRYL_ROWS, mouse=mouse))
        self.assertEqual(r['mechanism_tier'], 'G3')
        self.assertEqual(r['adjusted_strength'], 'Moderate')

    def test_evidence_validation(self):
        bad = copy.deepcopy(FRYL_ROWS)
        bad.append(lof_row(0))
        with self.assertRaises(ValueError):
            evaluate(fryl_input(bad))
        bad = copy.deepcopy(FRYL_ROWS)
        bad[0]['classification'] = 'UNKNOWN'
        with self.assertRaises(ValueError):
            evaluate(fryl_input(bad))


class ScoreGateTests(unittest.TestCase):
    def review(self, rows=None, mouse=None, manual=3):
        return evaluate(fryl_input(rows, mouse=mouse, manual_independent=manual))

    def test_very_strong_without_g1_blocked(self):
        r = self.review(FRYL_ROWS, manual=0)
        s = score(case([('PVS1_VeryStrong', 8), ('PM2_Supporting', 1)]),
                  pvs1_review=r, enforce_pvs1_provenance=True)
        self.assertIn('pvs1_very_strong_requires_G1', s['blockers'])
        self.assertIsNone(s['point_candidate'])

    def test_very_strong_with_unaudited_counts_blocked(self):
        r = self.review(None, manual=3)
        s = score(case([('PVS1_VeryStrong', 8), ('PM2_Supporting', 1)]),
                  pvs1_review=r, enforce_pvs1_provenance=True)
        self.assertIn('pvs1_independent_lof_counts_not_audited', s['blockers'])

    def test_missing_review_blocked(self):
        s = score(case([('PVS1_VeryStrong', 8), ('PM2_Supporting', 1)]),
                  enforce_pvs1_provenance=True)
        self.assertIn('pvs1_mechanism_review_missing', s['blockers'])

    def test_strength_mismatch_blocked(self):
        r = self.review(FRYL_ROWS, manual=0)  # Moderate
        s = score(case([('PVS1_VeryStrong', 8), ('PM2_Supporting', 1)]),
                  pvs1_review=r, enforce_pvs1_provenance=True)
        self.assertIn('pvs1_strength_mismatch:VeryStrong->Moderate', s['blockers'])

    def test_moderate_accepted_and_scores_vus(self):
        r = self.review(FRYL_ROWS, manual=0)  # Moderate
        s = score(case([('PVS1_Moderate', 2), ('PM2_Supporting', 1)]),
                  pvs1_review=r, enforce_pvs1_provenance=True)
        self.assertEqual(s['blockers'], [])
        self.assertEqual(s['net_points'], '3')
        self.assertEqual(s['point_candidate'], 'VUS')
        self.assertEqual(s['acmg_2015_comparison']['candidate'], 'VUS')

    def test_g1_audited_very_strong_accepted(self):
        r = evaluate(fryl_input(FRYL_ROWS, manual_independent=0))  # G3, not G1
        self.assertEqual(r['adjusted_strength'], 'Moderate')
        audited = pvs1_fixture('N01')  # manual 3, no list -> not audited
        self.assertFalse(evaluate(audited)['counts_audited'])
        # A G1 review backed by an audited list is accepted.
        g1 = pvs1_fixture('N01')
        g1['mechanism']['lof_evidence'] = [
            lof_row(0, cls='P', dependent=False), lof_row(1, cls='P', dependent=False),
            lof_row(2, cls='LP', dependent=False)]
        g1['mechanism']['phenotype_lof_count'] = 3
        g1['mechanism']['phenotype_total_count'] = 10
        g1['mechanism']['associated_lof_count'] = 3
        g1['mechanism']['independent_pathogenic_lof_count'] = 3
        rev = evaluate(g1)
        self.assertTrue(rev['counts_audited'])
        sc = score(case([('PVS1_VeryStrong', 8), ('PM2_Supporting', 1)]),
                   pvs1_review=rev, enforce_pvs1_provenance=True)
        self.assertEqual(sc['blockers'], [])
        self.assertEqual(sc['net_points'], '9')


class AuditFlagTests(unittest.TestCase):
    def test_reaudit_flag_on_pvs1(self):
        s = score(case([('PVS1_VeryStrong', 8), ('PM2_Supporting', 1)]))
        self.assertTrue(s['framework_disagreement'])
        self.assertEqual(s['reaudit_required']['code'], 'PVS1_VeryStrong')

    def test_no_reaudit_when_frameworks_agree(self):
        s = score(case([('PVS1_Moderate', 2), ('PM2_Supporting', 1)]))
        self.assertFalse(s['framework_disagreement'])
        self.assertIsNone(s['reaudit_required'])

    def test_provenance_direct(self):
        g = pvs1_provenance([{'code': 'PVS1_Strong', 'points': 4}], None)
        self.assertIn('pvs1_mechanism_review_missing', g['blockers'])
        self.assertIn('pvs1_very_strong_requires_G1',
                      pvs1_provenance([{'code': 'PVS1_VeryStrong', 'points': 8}],
                                      {'status': 'test_calculation_only',
                                       'mechanism_tier': 'G3',
                                       'adjusted_strength': 'VeryStrong',
                                       'counts_audited': True})['blockers'])
        self.assertIsNone(framework_reaudit([{'code': 'PM2_Supporting', 'points': 1}], True))


class PipelineGateTests(unittest.TestCase):
    def test_pipeline_blocks_unaudited_very_strong(self):
        d = pipeline_fixture()
        d['admissions'][0]['input']['mechanism'].pop('lof_evidence')
        r = pipeline_run(d)
        self.assertIsNone(r['authoritative_candidate'])
        self.assertIn('pvs1_independent_lof_counts_not_audited', r['blockers'])

    def test_pipeline_accepts_audited_very_strong(self):
        r = pipeline_run(pipeline_fixture())
        self.assertEqual(r['status'], 'reviewed_candidate_only')
        self.assertEqual(r['authoritative_candidate'], 'LP')


if __name__ == '__main__':
    unittest.main()
