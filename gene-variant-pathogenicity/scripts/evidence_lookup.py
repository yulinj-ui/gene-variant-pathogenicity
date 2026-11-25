#!/usr/bin/env python3
"""Reviewed-input lookup helpers for evidence items not yet in the primary score.

PS1/PM5, PM4, PS4 (likelihood-ratio and proband-count), BS2, PP1 LOD, and
BA1 threshold. Every helper is test_calculation_only: it never issues an
evidence code or a final classification and never auto-imports into the
primary score. Inputs are caller-reviewed facts; the tool only validates
structure and performs the source-bound table lookup.
"""
import argparse
import json
from pathlib import Path
from review_helpers import reviewed_gate
from score import decimal

SOURCES = {
    'ps1pm5': 'ACMG/AMP 2015; ACGS 2024 v1.2 strength matrix',
    'pm4': 'ACMG/AMP 2015; ACGS 2024 v1.2',
    'ps4': 'ACMG/AMP 2015 (OR>5); Tavtigian 2020 LR/EP; Oza 2018 PMID:30311386',
    'bs2': 'ACGS 2024 v1.2',
    'pp1_lod': 'Jarvik & Browning 2016 PMID:27236918',
    'ba1_threshold': 'Ghosh 2018 PMC6188666; ClinGen SVI 2018',
}

BAYES = {'Supporting': 1, 'Moderate': 2, 'Strong': 4, 'VeryStrong': 8}


def result(kind, blockers, **values):
    return dict(tool=kind, source=SOURCES[kind], status='blocked' if blockers else 'test_calculation_only',
                blockers=blockers, evidence_code=None, classification=None, automatic_score_import=False,
                **values)


def _bool(d, k):
    v = d.get(k)
    if v is None:
        raise ValueError('missing boolean: ' + k)
    if type(v) is not bool:
        raise ValueError('strict boolean required: ' + k)
    return v


def _int(d, k, lo=0):
    v = d.get(k)
    if v is None:
        raise ValueError('missing integer: ' + k)
    if type(v) is not int or v < lo:
        raise ValueError('nonnegative integer required: ' + k)
    return v


def ps1pm5(data):
    """PS1 (same amino acid change) / PM5 (same residue, different amino acid)."""
    blockers = reviewed_gate(data.get('review'), [
        'reference_independently_classified', 'phenotype_matched',
        'reference_no_splice_effect', 'vcep_checked'])
    rel = data.get('relationship')
    if rel not in ('same_amino_acid', 'same_residue_diff_aa'):
        raise ValueError('relationship must be same_amino_acid or same_residue_diff_aa')
    ref = data.get('reference_class')
    if ref not in ('P', 'LP'):
        raise ValueError('reference_class must be P or LP')
    strength = code = None
    if rel == 'same_amino_acid':
        code, strength = ('PS1', 'Strong') if ref == 'P' else ('PS1_Moderate', 'Moderate')
    else:
        if data.get('pm5_strong') is True:
            # PM5_Strong: >=2 distinct pathogenic missense at the same codon,
            # requires VCEP/SVI support and independence from PM1 (manual review).
            if ref != 'P':
                blockers.append('pm5_strong_requires_P_reference')
            else:
                code, strength = 'PM5_Strong', 'Strong'
        else:
            g = data.get('grantham_not_less')
            if ref == 'P' and g is True:
                code, strength = 'PM5', 'Moderate'
            elif ref == 'LP' or g is False:
                code, strength = 'PM5_Supporting', 'Supporting'
            else:
                blockers.append('grantham_not_less_missing_for_P_reference')
    weight = None if blockers or strength is None else BAYES[strength]
    return result('ps1pm5', blockers, code=None if blockers else code,
                  strength=None if blockers else strength, bayesian_weight=weight,
                  note='PM5_Strong requires VCEP/SVI support and PM1-independence review')


def pm4(data):
    """PM4: protein length change (in-frame indel, stop-loss, GOF last-exon truncation)."""
    blockers = reviewed_gate(data.get('review'), [
        'mechanism_matched', 'not_redundant_with_pvs1', 'not_redundant_with_ps1_pm5', 'vcep_checked'])
    vt = data.get('variant_type')
    if vt not in ('in_frame_indel', 'stop_loss', 'last_exon_truncation_gof'):
        raise ValueError('variant_type must be in_frame_indel, stop_loss or last_exon_truncation_gof')
    strength = None
    if vt == 'in_frame_indel':
        if _bool(data, 'in_repeat_region'):
            blockers.append('repeat_region_in_frame_indel_is_BP3_not_PM4')
        else:
            strength = 'Supporting' if _bool(data, 'single_aa_noncritical') else 'Moderate'
    elif vt == 'stop_loss':
        if _bool(data, 'nsd_present'):
            blockers.append('stop_loss_with_NSD_is_PVS1_not_PM4')
        else:
            strength = 'Moderate'
    else:  # last_exon_truncation_gof
        if not _bool(data, 'gof_mechanism_established'):
            blockers.append('last_exon_truncation_requires_established_GOF')
        else:
            strength = 'Moderate'
    weight = None if blockers or strength is None else BAYES[strength]
    return result('pm4', blockers, strength=None if blockers else strength, bayesian_weight=weight,
                  note='Mutex with PVS1/PS1/PM5/PP2/PP3 is enforced by the caller, not this lookup')


def ps4(data):
    """PS4: case-control (likelihood ratio) or proband-count strength lookup."""
    mode = data.get('mode')
    if mode == 'likelihood_ratio':
        blockers = reviewed_gate(data.get('review'), [
            'cohort_definitions_reviewed', 'population_matched',
            'genotyping_reviewed', 'vcep_checked'])
        lr = decimal(data.get('lr'))
        if lr <= 0:
            raise ValueError('LR must be positive and finite')
        direction = band = ep = None
        if lr >= decimal('350.4'):
            direction, band, ep = 'pathogenic', 'VeryStrong', '>=8'
        elif lr >= decimal('18.72'):
            direction, band, ep = 'pathogenic', 'Strong', '4-8'
        elif lr >= decimal('4.33'):
            direction, band, ep = 'pathogenic', 'Moderate', '2-4'
        elif lr >= decimal('2.08'):
            direction, band, ep = 'pathogenic', 'Supporting', '1-2'
        elif lr < decimal('0.00285'):
            direction, band, ep = 'benign', 'VeryStrong', '<=-8'
        elif lr < decimal('0.053'):
            direction, band, ep = 'benign', 'Strong', '-8..-4'
        elif lr < decimal('0.23'):
            direction, band, ep = 'benign', 'Moderate', '-4..-2'
        elif lr < decimal('0.48'):
            direction, band, ep = 'benign', 'Supporting', '-2..-1'
        else:
            direction, band, ep = None, 'Indeterminate', None
        weight = None if blockers or band in (None, 'Indeterminate') else BAYES[band]
        return result('ps4', blockers, mode=mode, direction=None if blockers else direction,
                      band=None if blockers else band, evidence_points=ep,
                      bayesian_weight=weight, note='Code selection (PS4 vs BS4) remains a caller decision')
    if mode == 'proband_count':
        blockers = reviewed_gate(data.get('review'), [
            'phenotype_consistent', 'case_independence_reviewed', 'deduplication_reviewed', 'vcep_checked'])
        inh = data.get('inheritance')
        if inh not in ('AD', 'XL'):
            raise ValueError('proband-count PS4 requires AD or XL inheritance')
        if not _bool(data, 'pm2_met'):
            blockers.append('proband_count_requires_PM2')
        n = _int(data, 'unrelated_probands')
        strength = None
        if n >= 15:
            strength = 'Strong'
        elif n >= 6:
            strength = 'Moderate'
        elif n >= 2:
            strength = 'Supporting'
        else:
            blockers.append('insufficient_probands')
        weight = None if blockers or strength is None else BAYES[strength]
        return result('ps4', blockers, mode=mode, inheritance=inh,
                      unrelated_probands=n, strength=None if blockers else strength,
                      bayesian_weight=weight,
                      note='AR disorders use PM3, not PS4 proband counting; same-family=1, cross-paper dedup required')
    raise ValueError('mode must be likelihood_ratio or proband_count')


def bs2(data):
    """BS2: healthy individuals with the variant in early-onset, fully-penetrant disease."""
    blockers = reviewed_gate(data.get('review'), [
        'disease_applicability', 'early_onset_full_penetrant', 'phenotype_assessed', 'vcep_checked'])
    inh = data.get('inheritance')
    if inh not in ('AD', 'AR', 'XL'):
        raise ValueError('inheritance must be AD, AR or XL')
    n = _int(data, 'healthy_carrier_count')
    met = n >= 2
    return result('bs2', blockers, inheritance=inh, healthy_carrier_count=n,
                  bs2_met=None if blockers else met,
                  note='AD=healthy heterozygotes, AR=healthy homozygotes, XL=healthy hemizygotes; '
                       'reduced-penetrance or imprinting/sex-limited carriers do not count')


def pp1_lod(data):
    """PP1: cosegregation strength from the number of informative meioses (Jarvik scale)."""
    blockers = reviewed_gate(data.get('review'), [
        'phase_reviewed', 'penetrance_reviewed', 'counted_by_meiosis', 'vcep_checked'])
    n = _int(data, 'meiosis_count')
    strength = None
    if n >= 7:
        strength = 'Strong'
    elif n >= 5:
        strength = 'Moderate'
    elif n >= 3:
        strength = 'Supporting'
    else:
        blockers.append('insufficient_informative_meioses')
    weight = None if blockers or strength is None else BAYES[strength]
    return result('pp1_lod', blockers, meiosis_count=n,
                  strength=None if blockers else strength, bayesian_weight=weight,
                  note='Jarvik 2016 scale; VCEP may override. 3-4=Supporting, 5-6=Moderate, >=7=Strong')


def ba1_threshold(data):
    """BA1: allele frequency >5% and >=2000 observed alleles in a continental population,
    outside the published exception list, as a stand-alone benign criterion."""
    blockers = reviewed_gate(data.get('review'), [
        'population_verified', 'denominator_verified', 'quality_filter_verified',
        'gene_disease_inheritance_reviewed', 'vcep_checked', 'exception_list_current'])
    if data.get('exception_matched_ids'):
        blockers.append('in_BA1_exception_list')
    af = decimal(data.get('af'))
    ac = _int(data, 'allele_count')
    if not (0 <= af <= 1):
        raise ValueError('AF must be within [0,1]')
    applies = af > decimal('0.05') and ac >= 2000
    return result('ba1_threshold', blockers, af=str(af), allele_count=ac,
                  ba1_applies=None if blockers else applies,
                  note='Stand-alone benign logic; not converted to -8 points. Exception matching runs separately via ba1_review.py')


def run(mode, data):
    return {'ps1pm5': ps1pm5, 'pm4': pm4, 'ps4': ps4, 'bs2': bs2,
            'pp1_lod': pp1_lod, 'ba1_threshold': ba1_threshold}[mode](data)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('mode', choices=list(SOURCES))
    ap.add_argument('input_json')
    a = ap.parse_args()
    try:
        d = json.loads(Path(a.input_json).read_text())
        print(json.dumps(run(a.mode, d), ensure_ascii=False, indent=2))
    except (ValueError, TypeError, KeyError) as e:
        ap.error(str(e))
