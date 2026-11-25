import copy
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from evidence_lookup import ps1pm5, pm4, ps4, bs2, pp1_lod, ba1_threshold
from cnv_section2 import evaluate
from case_pipeline import run
from compare_frameworks import decode
from score import score as score_run
from test_v2 import case
from test_v5r1 import sign, add_rule, assess


def review(*keys):
    return dict({k: True for k in keys}, reviewer='synthetic reviewer', reviewed_at='2026-09-29',
                source='synthetic fixture', rationale='engineering test only; not a patient')


def ps1(review_keys, **extra):
    d = dict(review=review(*review_keys), relationship='same_amino_acid', reference_class='P')
    d.update(extra)
    return d


def pm5(review_keys, **extra):
    d = dict(review=review(*review_keys), relationship='same_residue_diff_aa', reference_class='P', grantham_not_less=True)
    d.update(extra)
    return d


class PS1PM5Tests(unittest.TestCase):
    GATES = ['reference_independently_classified', 'phenotype_matched', 'reference_no_splice_effect', 'vcep_checked']

    def test_ps1_P(self):
        r = ps1pm5(ps1(self.GATES)); self.assertEqual(r['code'], 'PS1'); self.assertEqual(r['strength'], 'Strong'); self.assertEqual(r['bayesian_weight'], 4)
    def test_ps1_LP(self):
        r = ps1pm5(ps1(self.GATES, reference_class='LP')); self.assertEqual(r['code'], 'PS1_Moderate'); self.assertEqual(r['bayesian_weight'], 2)
    def test_pm5_P_grantham_not_less(self):
        r = ps1pm5(pm5(self.GATES)); self.assertEqual(r['code'], 'PM5'); self.assertEqual(r['strength'], 'Moderate'); self.assertEqual(r['bayesian_weight'], 2)
    def test_pm5_P_grantham_less(self):
        r = ps1pm5(pm5(self.GATES, grantham_not_less=False)); self.assertEqual(r['code'], 'PM5_Supporting'); self.assertEqual(r['bayesian_weight'], 1)
    def test_pm5_LP(self):
        r = ps1pm5(pm5(self.GATES, reference_class='LP')); self.assertEqual(r['code'], 'PM5_Supporting'); self.assertEqual(r['bayesian_weight'], 1)
    def test_pm5_missing_grantham_blocks(self):
        r = ps1pm5(ps1(self.GATES, relationship='same_residue_diff_aa', grantham_not_less=None)); self.assertEqual(r['status'], 'blocked')
    def test_pm5_strong_requires_P(self):
        r = ps1pm5(pm5(self.GATES, reference_class='LP', pm5_strong=True)); self.assertEqual(r['status'], 'blocked')
    def test_pm5_strong_P(self):
        r = ps1pm5(pm5(self.GATES, pm5_strong=True)); self.assertEqual(r['code'], 'PM5_Strong'); self.assertEqual(r['bayesian_weight'], 4)
    def test_missing_review_blocks(self):
        r = ps1pm5(dict(review=review(), relationship='same_amino_acid', reference_class='P')); self.assertEqual(r['status'], 'blocked')
    def test_invalid_relationship(self):
        with self.assertRaises(ValueError): ps1pm5(ps1(self.GATES, relationship='same_codon_any'))
    def test_circular_reference_gate(self):
        d = ps1(self.GATES); d['review']['reference_independently_classified'] = False
        self.assertEqual(ps1pm5(d)['status'], 'blocked')


class PM4Tests(unittest.TestCase):
    GATES = ['mechanism_matched', 'not_redundant_with_pvs1', 'not_redundant_with_ps1_pm5', 'vcep_checked']

    def d(self, vt, **facts):
        x = dict(review=review(*self.GATES), variant_type=vt)
        x.update(facts)
        return x

    def test_in_frame_indel(self):
        r = pm4(self.d('in_frame_indel', in_repeat_region=False, single_aa_noncritical=False)); self.assertEqual(r['strength'], 'Moderate'); self.assertEqual(r['bayesian_weight'], 2)
    def test_in_frame_single_aa_noncritical(self):
        r = pm4(self.d('in_frame_indel', in_repeat_region=False, single_aa_noncritical=True)); self.assertEqual(r['strength'], 'Supporting')
    def test_repeat_region_is_BP3(self):
        r = pm4(self.d('in_frame_indel', in_repeat_region=True, single_aa_noncritical=False)); self.assertEqual(r['status'], 'blocked'); self.assertIn('BP3', r['blockers'][0])
    def test_stop_loss_no_nsd(self):
        r = pm4(self.d('stop_loss', nsd_present=False)); self.assertEqual(r['strength'], 'Moderate')
    def test_stop_loss_with_nsd_is_PVS1(self):
        r = pm4(self.d('stop_loss', nsd_present=True)); self.assertEqual(r['status'], 'blocked'); self.assertIn('PVS1', r['blockers'][0])
    def test_last_exon_gof(self):
        r = pm4(self.d('last_exon_truncation_gof', gof_mechanism_established=True)); self.assertEqual(r['strength'], 'Moderate')
    def test_last_exon_gof_unestablished(self):
        r = pm4(self.d('last_exon_truncation_gof', gof_mechanism_established=False)); self.assertEqual(r['status'], 'blocked')
    def test_invalid_variant_type(self):
        with self.assertRaises(ValueError): pm4(self.d('missense'))
    def test_missing_bool(self):
        with self.assertRaises(ValueError): pm4(self.d('in_frame_indel'))


class PS4Tests(unittest.TestCase):
    GATES = ['cohort_definitions_reviewed', 'population_matched', 'genotyping_reviewed', 'vcep_checked']

    def lr(self, v):
        return dict(review=review(*self.GATES), mode='likelihood_ratio', lr=v)

    def test_lr_pathogenic_bands(self):
        for lr, band, w in [('350.4', 'VeryStrong', 8), ('18.72', 'Strong', 4), ('4.33', 'Moderate', 2), ('2.08', 'Supporting', 1)]:
            r = ps4(self.lr(lr)); self.assertEqual(r['band'], band); self.assertEqual(r['bayesian_weight'], w)
    def test_lr_indeterminate(self):
        r = ps4(self.lr('0.5')); self.assertEqual(r['band'], 'Indeterminate'); self.assertIsNone(r['bayesian_weight'])
    def test_lr_benign_bands(self):
        for lr, band in [('0.47', 'Supporting'), ('0.22', 'Moderate'), ('0.052', 'Strong'), ('0.002', 'VeryStrong')]:
            r = ps4(self.lr(lr)); self.assertEqual(r['band'], band); self.assertEqual(r['direction'], 'benign')
    def test_lr_invalid(self):
        with self.assertRaises(ValueError): ps4(self.lr('0'))
    def test_count_AD(self):
        gates = ['phenotype_consistent', 'case_independence_reviewed', 'deduplication_reviewed', 'vcep_checked']
        for n, s in [(15, 'Strong'), (6, 'Moderate'), (2, 'Supporting')]:
            r = ps4(dict(review=review(*gates), mode='proband_count', inheritance='AD', pm2_met=True, unrelated_probands=n))
            self.assertEqual(r['strength'], s)
    def test_count_insufficient(self):
        gates = ['phenotype_consistent', 'case_independence_reviewed', 'deduplication_reviewed', 'vcep_checked']
        r = ps4(dict(review=review(*gates), mode='proband_count', inheritance='AD', pm2_met=True, unrelated_probands=1))
        self.assertEqual(r['status'], 'blocked')
    def test_count_requires_pm2(self):
        gates = ['phenotype_consistent', 'case_independence_reviewed', 'deduplication_reviewed', 'vcep_checked']
        r = ps4(dict(review=review(*gates), mode='proband_count', inheritance='AD', pm2_met=False, unrelated_probands=20))
        self.assertEqual(r['status'], 'blocked')
    def test_count_AR_rejected(self):
        gates = ['phenotype_consistent', 'case_independence_reviewed', 'deduplication_reviewed', 'vcep_checked']
        with self.assertRaises(ValueError):
            ps4(dict(review=review(*gates), mode='proband_count', inheritance='AR', pm2_met=True, unrelated_probands=20))


class BS2Tests(unittest.TestCase):
    GATES = ['disease_applicability', 'early_onset_full_penetrant', 'phenotype_assessed', 'vcep_checked']

    def test_met(self):
        for inh in ['AD', 'AR', 'XL']:
            r = bs2(dict(review=review(*self.GATES), inheritance=inh, healthy_carrier_count=2)); self.assertTrue(r['bs2_met'])
    def test_not_met(self):
        r = bs2(dict(review=review(*self.GATES), inheritance='AD', healthy_carrier_count=1)); self.assertFalse(r['bs2_met'])
    def test_invalid_inheritance(self):
        with self.assertRaises(ValueError): bs2(dict(review=review(*self.GATES), inheritance='mt', healthy_carrier_count=2))


class PP1LODTests(unittest.TestCase):
    GATES = ['phase_reviewed', 'penetrance_reviewed', 'counted_by_meiosis', 'vcep_checked']

    def d(self, n):
        return dict(review=review(*self.GATES), meiosis_count=n)

    def test_scale(self):
        for n, s in [(3, 'Supporting'), (4, 'Supporting'), (5, 'Moderate'), (6, 'Moderate'), (7, 'Strong')]:
            r = pp1_lod(self.d(n)); self.assertEqual(r['strength'], s)
    def test_insufficient(self):
        r = pp1_lod(self.d(2)); self.assertEqual(r['status'], 'blocked')


class BA1ThresholdTests(unittest.TestCase):
    GATES = ['population_verified', 'denominator_verified', 'quality_filter_verified',
             'gene_disease_inheritance_reviewed', 'vcep_checked', 'exception_list_current']

    def d(self, af, ac, **extra):
        x = dict(review=review(*self.GATES), af=af, allele_count=ac)
        x.update(extra)
        return x

    def test_applies(self):
        self.assertTrue(ba1_threshold(self.d('0.06', 2000))['ba1_applies'])
    def test_not_applies_af(self):
        self.assertFalse(ba1_threshold(self.d('0.05', 2000))['ba1_applies'])
    def test_not_applies_alleles(self):
        self.assertFalse(ba1_threshold(self.d('0.06', 1999))['ba1_applies'])
    def test_exception_blocks(self):
        self.assertEqual(ba1_threshold(self.d('0.06', 2000, exception_matched_ids=['CA123']))['status'], 'blocked')
    def test_af_range(self):
        with self.assertRaises(ValueError): ba1_threshold(self.d('1.2', 2000))


class CNV2HDualProfileTests(unittest.TestCase):
    def prediction(self, profile, **facts):
        from test_v5r1 import sign
        d = dict(cnv_type='LOSS',
                 identity=dict(variant_id='synthetic-cnv', gene='SYNTHETIC', build='GRCh38', disease='synthetic', inheritance='AD'),
                 target_id='t', target_kind='gene', relation='predicted_hi',
                 review=sign(), basis_ids=['b1'],
                 dosage=dict(axis='HI', score=0, source='s', record_id='r', evaluated_at='2020-01-01', current_evidence_review='s'),
                 target_clinical_significance='uncertain', applied_hi_categories=[],
                 fact_sources={k: dict(source='s', location='fixture', rationale='engineering only') for k in
                               ['interval_and_breakpoints', 'target_geometry', 'dosage', 'transcript_and_function', 'platform']},
                 facts=dict(predictor_profile=profile, pli='0.9',
                            gnomad_source_version='verified', decipher_source_version='verified', metric_equivalence_review='synthetic'))
        d['facts'].update(facts)
        return d

    def test_riggs_profile_pass(self):
        r = evaluate(self.prediction('Riggs2020_original', oe_upper='0.349999', decipher_hi_percent='10'))
        self.assertEqual(r['status'], 'reviewed_section2_candidate'); self.assertEqual(r['code'], '2H')
    def test_riggs_profile_boundary_fail(self):
        r = evaluate(self.prediction('Riggs2020_original', oe_upper='0.35', decipher_hi_percent='10'))
        self.assertEqual(r['status'], 'blocked')
    def test_v4_profile_pass(self):
        r = evaluate(self.prediction('ClinGen_current_v4', loeuf='0.599', phaplo='0.86'))
        self.assertEqual(r['status'], 'reviewed_section2_candidate'); self.assertEqual(r['code'], '2H')
    def test_v4_profile_boundary_fail(self):
        r = evaluate(self.prediction('ClinGen_current_v4', loeuf='0.6', phaplo='0.86'))
        self.assertEqual(r['status'], 'blocked')
    def test_v4_profile_phaplo_fail(self):
        r = evaluate(self.prediction('ClinGen_current_v4', loeuf='0.5', phaplo='0.85'))
        self.assertEqual(r['status'], 'blocked')
    def test_unknown_profile_blocked(self):
        r = evaluate(self.prediction('gnomad_v4_0.6', loeuf='0.5', phaplo='0.9'))
        self.assertEqual(r['status'], 'blocked')


def make_case(kind, raw, codes, assessment=None, basis='b-new', inheritance='AD'):
    identity = dict(variant_id='SYNTHETIC', gene='SYNTHETIC', disease='synthetic', inheritance=inheritance)
    rule = dict(code='PM2_Supporting', framework='SNV', status='reviewed', source='synthetic', version='test',
                location='fixture', reviewer='synthetic', reviewed_at='2026-09-29', applicability='synthetic', allowed_points=[1])
    row = dict(id='e0', code='PM2_Supporting', framework='SNV', rule_id='r0', status='reviewed', gate='passed',
               points=1, source_ids=['source'], basis_ids=['unique'], rationale='synthetic')
    d = dict(identity=copy.deepcopy(identity),
             scoring=dict(framework='SNV', rules={'r0': rule}, evidence=[row],
                          combination_policy=dict(status='reviewed', framework='SNV', source='synthetic', version='test',
                                                 reviewer='synthetic', reviewed_at='2026-09-29', mutually_exclusive=[], caps=[])),
             routing=dict(identity=copy.deepcopy(identity), review=sign(), search_completed=True, outcome='none_found',
                          searches=[dict(url='synthetic', query='SYNTHETIC', accessed_at='2026-09-29', result='none')]),
             admissions=[])
    a = dict(id='a1', kind=kind, identity=copy.deepcopy(identity), approval=sign(), source_ids=['fixture'],
             basis_ids=[basis], selected_codes=codes, rule_ids={}, input=raw)
    if assessment is not None:
        a['assessment'] = assessment
    for code in codes:
        add_rule(d, code)
        a['rule_ids'][code] = code
    d['admissions'] = [a]
    return d


G_PS1 = ['reference_independently_classified', 'phenotype_matched', 'reference_no_splice_effect', 'vcep_checked']
G_PM4 = ['mechanism_matched', 'not_redundant_with_pvs1', 'not_redundant_with_ps1_pm5', 'vcep_checked']
G_PS4_LR = ['cohort_definitions_reviewed', 'population_matched', 'genotyping_reviewed', 'vcep_checked']
G_PS4_CNT = ['phenotype_consistent', 'case_independence_reviewed', 'deduplication_reviewed', 'vcep_checked']
G_BS2 = ['disease_applicability', 'early_onset_full_penetrant', 'phenotype_assessed', 'vcep_checked']
G_PP1 = ['phase_reviewed', 'penetrance_reviewed', 'counted_by_meiosis', 'vcep_checked']


class CasePipelineAdmissionTests(unittest.TestCase):
    def test_ps1_admitted(self):
        raw = dict(review=review(*G_PS1), relationship='same_amino_acid', reference_class='P')
        r = run(make_case('ps1pm5', raw, ['PS1']))
        self.assertEqual(r['status'], 'reviewed_candidate_only')
        self.assertEqual(r['score_comparison']['net_points'], '5')  # PS1(4) + PM2_Supporting(1)
    def test_ps1_strength_override_blocked(self):
        raw = dict(review=review(*G_PS1), relationship='same_amino_acid', reference_class='LP')
        r = run(make_case('ps1pm5', raw, ['PS1']))
        self.assertIsNone(r['authoritative_candidate'])
        self.assertTrue(any('selected_codes_not_supported_by_recalculation' in b for b in r['blockers']))
    def test_pm4_admitted(self):
        raw = dict(review=review(*G_PM4), variant_type='in_frame_indel', in_repeat_region=False, single_aa_noncritical=False)
        r = run(make_case('pm4', raw, ['PM4']))
        self.assertEqual(r['score_comparison']['net_points'], '3')  # PM4(2) + PM2(1)
    def test_pm4_repeat_region_blocked(self):
        raw = dict(review=review(*G_PM4), variant_type='in_frame_indel', in_repeat_region=True, single_aa_noncritical=False)
        r = run(make_case('pm4', raw, ['PM4']))
        self.assertIsNone(r['authoritative_candidate'])
    def test_ps4_lr_admitted(self):
        raw = dict(review=review(*G_PS4_LR), mode='likelihood_ratio', lr='18.72')
        r = run(make_case('ps4', raw, ['PS4']))
        self.assertEqual(r['score_comparison']['net_points'], '5')
    def test_ps4_count_admitted(self):
        raw = dict(review=review(*G_PS4_CNT), mode='proband_count', inheritance='AD', pm2_met=True, unrelated_probands=15)
        r = run(make_case('ps4', raw, ['PS4']))
        self.assertEqual(r['score_comparison']['net_points'], '5')
    def test_ps4_benign_lr_blocked(self):
        raw = dict(review=review(*G_PS4_LR), mode='likelihood_ratio', lr='0.47')
        r = run(make_case('ps4', raw, ['BS4']))
        self.assertIsNone(r['authoritative_candidate'])
        self.assertTrue(any('PS4_benign_LR_has_no_standard_code' in b for b in r['blockers']))
    def test_bs2_admitted(self):
        raw = dict(review=review(*G_BS2), inheritance='AD', healthy_carrier_count=2)
        r = run(make_case('bs2', raw, ['BS2']))
        self.assertEqual(r['score_comparison']['net_points'], '-3')  # BS2(-4) + PM2_Supporting(1)
    def test_bs2_not_met_blocked(self):
        raw = dict(review=review(*G_BS2), inheritance='AD', healthy_carrier_count=1)
        r = run(make_case('bs2', raw, ['BS2']))
        self.assertIsNone(r['authoritative_candidate'])
    def test_pp1_lod_admitted(self):
        raw = dict(review=review(*G_PP1), meiosis_count=6)
        r = run(make_case('pp1_lod', raw, ['PP1_Moderate'], assessment=assess('pedigree')))
        self.assertEqual(r['score_comparison']['net_points'], '3')  # PP1_Moderate(2) + PM2(1)
    def test_pp1_lod_requires_pedigree(self):
        raw = dict(review=review(*G_PP1), meiosis_count=6)
        r = run(make_case('pp1_lod', raw, ['PP1_Moderate']))
        self.assertIsNone(r['authoritative_candidate'])
    def test_shared_basis_blocked(self):
        raw = dict(review=review(*G_PS1), relationship='same_amino_acid', reference_class='P')
        r = run(make_case('ps1pm5', raw, ['PS1'], basis='unique'))
        self.assertIsNone(r['authoritative_candidate'])
        self.assertTrue(any('underlying_evidence_already_used' in b for b in r['blockers']))
    def test_no_approval_blocked(self):
        raw = dict(review=review(*G_PS1), relationship='same_amino_acid', reference_class='P')
        d = make_case('ps1pm5', raw, ['PS1'])
        d['admissions'][0]['approval']['approved'] = False
        self.assertIsNone(run(d)['authoritative_candidate'])
    def test_ba1_threshold_check_present(self):
        d = make_case('ps1pm5', dict(review=review(*G_PS1), relationship='same_amino_acid', reference_class='P'), ['PS1'])
        d['ba1_threshold'] = dict(review=review('population_verified', 'denominator_verified', 'quality_filter_verified',
                                                'gene_disease_inheritance_reviewed', 'vcep_checked', 'exception_list_current'),
                                  af='0.06', allele_count=2000)
        r = run(d)
        self.assertTrue(r['ba1_threshold_check']['ba1_applies'])
        # BA1 check is informational: it never auto-issues a Benign classification.
        self.assertEqual(r['authoritative_candidate'], 'VUS')
        self.assertIsNone(r['classification'])


class ScoreMutexTests(unittest.TestCase):
    def blocked(self, codes):
        return score_run(case(codes))['blockers']

    def test_ps1_pm5_mutex(self):
        self.assertIn('mutually_exclusive:PM5/PS1', self.blocked([('PS1', 4), ('PM5', 2)]))
    def test_pm4_ps1_mutex(self):
        self.assertIn('mutually_exclusive:PM4/PS1', self.blocked([('PM4', 2), ('PS1', 4)]))
    def test_pm4_pm5_mutex(self):
        self.assertIn('mutually_exclusive:PM4/PM5', self.blocked([('PM4', 2), ('PM5', 2)]))
    def test_pm4_pp3_mutex(self):
        self.assertIn('mutually_exclusive:PM4/PP3', self.blocked([('PM4', 2), ('PP3', 1)]))
    def test_bs2_bp2_mutex(self):
        self.assertIn('mutually_exclusive:BP2/BS2', self.blocked([('BS2', -4), ('BP2', -1)]))
    def test_ps4_ps2_mutex(self):
        self.assertIn('mutually_exclusive:PS2/PS4', self.blocked([('PS4', 4), ('PS2', 4)]))
    def test_pm4_ps3_not_mutex(self):
        self.assertNotIn('mutually_exclusive', ' '.join(self.blocked([('PM4', 2), ('PS3', 4)])))


class PipelineFixtureTests(unittest.TestCase):
    def load(self, name):
        import json
        return json.loads((ROOT / 'tests/fixtures' / name).read_text())

    def test_ps1pm5_fixture(self):
        r = run(self.load('pipeline-ps1pm5-v7.json'))
        self.assertEqual(r['status'], 'reviewed_candidate_only')
        self.assertEqual(r['score_comparison']['net_points'], '5')
        self.assertIn('PS1', [x['code'] for x in r['score_comparison']['accepted']])
    def test_pm4_fixture(self):
        r = run(self.load('pipeline-pm4-v7.json'))
        self.assertEqual(r['score_comparison']['net_points'], '3')
        self.assertIn('PM4', [x['code'] for x in r['score_comparison']['accepted']])
    def test_ps4_fixture(self):
        r = run(self.load('pipeline-ps4-v7.json'))
        self.assertEqual(r['score_comparison']['net_points'], '5')
        self.assertIn('PS4', [x['code'] for x in r['score_comparison']['accepted']])
    def test_bs2_fixture(self):
        r = run(self.load('pipeline-bs2-v7.json'))
        self.assertEqual(r['score_comparison']['net_points'], '-3')
        self.assertIn('BS2', [x['code'] for x in r['score_comparison']['accepted']])
    def test_pp1_lod_fixture(self):
        r = run(self.load('pipeline-pp1-lod-v7.json'))
        self.assertEqual(r['score_comparison']['net_points'], '3')
        self.assertIn('PP1_Moderate', [x['code'] for x in r['score_comparison']['accepted']])


if __name__ == '__main__':
    unittest.main()
