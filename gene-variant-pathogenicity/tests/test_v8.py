"""v0.8.0 regression: upstream frequency gates, local dbNSFP wiring, offline behaviour."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import freq_evidence as fe
import genebe_fields as gv


class LocalDbnsfpTests(unittest.TestCase):
    def test_overlay_scope(self):
        self.assertEqual(set(gv._DB54_OVERLAY),
                         {'REVEL', 'ALPHAMISSENSE', 'BAYESDEL_NOAF', 'METARNN',
                          'PRIMATEAI', 'VARITY_R', 'ESM1B', 'CADD_PHRED'})
        self.assertNotIn('SIFT', gv._DB54_OVERLAY)
        self.assertNotIn('POLYPHEN', gv._DB54_OVERLAY)

    def test_missing_anchor_reports_blocked(self):
        ev = gv.to_evidence('NM_TEST.1:c.28C>T', {})
        self.assertEqual(ev['_sources']['dbnsfp54_local']['status'], 'blocked')
        self.assertIsNone(ev['dbnsfp54'])
        self.assertEqual(ev['schema_version'], '0.4')

    def test_fixture_mode_never_queries_library(self):
        ev = gv.to_evidence('NM_TEST.1:c.28C>T', {}, dbnsfp54=False)
        self.assertIn(ev['_sources']['dbnsfp54_local']['status'], ('blocked', 'disabled'))


class FrequencyGateTests(unittest.TestCase):
    def test_not_queried_withholds(self):
        out = fe.gates({'state': 'NOT_QUERIED'}, 'AD', None, 'LDLR', 'NM_000527.5:c.1183G>A', None)
        for code in ('PM2', 'BA1', 'BS1', 'BS2'):
            self.assertIn('扣留', out[code])

    def test_absent_confirmed_allows_pm2(self):
        out = fe.gates({'state': 'ABSENT_CONFIRMED'}, 'AD', None, 'LDLR', 'c.1A>G', None)
        self.assertTrue(out['PM2'].startswith('✅'))
        self.assertEqual(out['BA1'], '不满足')

    def test_ba1_threshold_and_an_floor(self):
        g = {'state': 'FOUND', 'ac': 700, 'an': 10000, 'hom': 0, 'hemi': 0,
             'faf95_grpmax': 0.07, 'faf95_grpmax_pop': 'eas',
             'pops': {'eas': {'ac': 700, 'an': 10000}, 'jpn': {'ac': 500, 'an': 3000}}}
        out = fe.gates(g, 'AD', None, 'GENE', 'c.1A>G', None)
        self.assertIn('BA1', out['BA1'])
        self.assertIn('eas', out['BA1'])
        self.assertNotIn('jpn', out['BA1'])       # non-continental / small subpopulation

    def test_ad_requires_ac_zero(self):
        g = {'state': 'FOUND', 'ac': 3, 'an': 1000000, 'hom': 0, 'hemi': 0,
             'faf95_grpmax': 3e-6, 'faf95_grpmax_pop': 'eas',
             'pops': {'eas': {'ac': 3, 'an': 1000000}}}
        out = fe.gates(g, 'AD', 1e-4, 'GENE', 'c.1A>G', None)
        self.assertTrue(out['PM2'].startswith('⛔'))

    def test_max_credible_af(self):
        self.assertAlmostEqual(fe.max_credible_af('AD', 1 / 250, 0.05, 1.0, 0.8), 0.000125, places=9)
        self.assertAlmostEqual(fe.max_credible_af('AR', 1 / 2500, 0.05, 1.0, 1.0), 0.001, places=9)

    def test_vcep_overrides_generic_ad_pm2(self):
        g = {'state': 'FOUND', 'ac': 1, 'an': 1613310, 'hom': 0, 'hemi': 0,
             'faf95_grpmax': 8.5e-07, 'faf95_grpmax_pop': 'nfe',
             'pops': {'nfe': {'ac': 1, 'an': 1179766}}}
        out = fe.gates(g, 'AD', 1e-4, 'LDLR', 'c.1183G>A', {'state': 'FOUND'})
        self.assertIn('VCEP', out['PM2'])
        self.assertNotIn('两条都不赋', out['PM2'])

    def test_ba1_exemption_snapshot(self):
        self.assertIn(('GJB2', 'c.109G>A'), fe.BA1_EXCEPTIONS)
        self.assertEqual(len(fe.BA1_EXCEPTIONS), 9)


if __name__ == '__main__':
    unittest.main()
