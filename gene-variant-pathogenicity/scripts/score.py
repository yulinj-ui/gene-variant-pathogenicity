#!/usr/bin/env python3
"""Audit explicit evidence points. Sandbox partitions are not clinical classifications."""
import argparse
import json
import re
from decimal import Decimal, InvalidOperation
from compare_frameworks import compare, decode
from report_audit import pvs1_provenance, framework_reaudit


def decimal(x):
    if isinstance(x, bool) or not isinstance(x, (str, int, float)):
        raise ValueError('numeric point required')
    try:
        v = Decimal(str(x))
    except InvalidOperation:
        raise ValueError('invalid points') from None
    if not v.is_finite():
        raise ValueError('nonfinite points')
    return v


def partition(total, framework):
    if framework == 'SNV':
        if total >= 10: return 'P_range'
        if total >= 6: return 'LP_range'
        if total >= 0: return 'VUS_range'
        if total > -7: return 'LB_range'
        return 'B_range'
    if total >= Decimal('.99'): return 'P_range'
    if total >= Decimal('.90'): return 'LP_range'
    if total > Decimal('-.90'): return 'VUS_range'
    if total > Decimal('-.99'): return 'LB_range'
    return 'B_range'


def score(data, pvs1_review=None, enforce_pvs1_provenance=False):
    framework = data.get('framework')
    if framework not in ('SNV', 'CNV_LOSS', 'CNV_GAIN'):
        raise ValueError('framework must be SNV/CNV_LOSS/CNV_GAIN')
    if data.get('points_profile', 'Tavtigian_2020') != 'Tavtigian_2020':
        raise ValueError('unsupported points profile; ACGS and local profiles remain disabled')
    if data.get('helper_results') is not None:
        raise ValueError('helper results cannot be imported as scoring evidence')
    if any(k in data for k in ('locus_packets','locus_results','fractional_points','review_calculations','pvs1_results','pvs1_review')):
        raise ValueError('locus/fractional review data cannot be imported into the primary score')
    rules = data.get('rules', {})
    if not isinstance(rules, dict):
        raise ValueError('rules must be a dictionary')
    evidence = data.get('evidence', [])
    if not isinstance(evidence, list):
        raise ValueError('evidence must be a list')
    accepted, rejected, seen_ids, seen_basis = [], [], set(), set()
    seen_codes = set()
    for row in evidence:
        if not isinstance(row, dict): raise ValueError('evidence row must be an object')
        identity = row.get('id')
        if not identity or identity in seen_ids:
            raise ValueError('missing/duplicate evidence id')
        seen_ids.add(identity)
        reason = None
        rule = rules.get(row.get('rule_id'), {})
        if row.get('framework') != framework:
            reason = 'framework_mismatch'
        elif row.get('status') != 'reviewed' or rule.get('status') != 'reviewed':
            reason = 'pending_review'
        elif rule.get('framework') != framework:
            reason = 'rule_framework_mismatch'
        elif not isinstance(row.get('code'), str) or not row.get('code') or rule.get('code') != row.get('code'):
            reason = 'rule_code_mismatch'
        elif not all(rule.get(k) for k in ('source', 'version', 'location', 'reviewer', 'reviewed_at', 'applicability')):
            reason = 'rule_provenance_missing'
        elif not row.get('source_ids') or not row.get('basis_ids') or not row.get('rationale'):
            reason = 'evidence_provenance_missing'
        elif any(not isinstance(row[k], list) or not all(isinstance(x, str) and x for x in row[k]) for k in ('basis_ids', 'source_ids')):
            reason = 'invalid_basis_ids'
        elif set(row['basis_ids']) & seen_basis:
            reason = 'duplicate_underlying_evidence'
        elif row.get('gate') != 'passed':
            reason = 'prerequisite_not_passed'
        else:
            pts = decimal(row.get('points'))
            allowed = [decimal(x) for x in rule.get('allowed_points', [])]
            if pts not in allowed:
                reason = 'points_not_approved'
            elif framework == 'SNV' and pts != pts.to_integral_value():
                reason = 'fractional_SNV_points_not_supported'
        if not reason and framework == 'SNV':
            try:
                base, expected = decode(row['code'])
            except ValueError:
                base, expected = row['code'], None
                if not re.fullmatch(r'TEST(?:_[A-Z0-9]+)?', base) or 'synthetic' not in rule.get('applicability','').lower():
                    reason = 'unsupported_evidence_code'
            if base in seen_codes:
                reason = 'duplicate_code_family'
            elif base in ('BA1', 'PP5', 'BP6'):
                reason = 'code_requires_unimplemented_or_deprecated_workflow'
            elif expected is not None and pts != expected:
                reason = 'code_points_mismatch'
        if not reason and framework != 'SNV':
            code = row['code']
            synthetic = bool(re.fullmatch(r'TEST(?:_[A-Z0-9]+)?', code)) and 'synthetic' in rule.get('applicability','').lower()
            if not synthetic and not re.fullmatch(r'[1-5][A-Z](?:-[1-9])?', code):
                reason = 'invalid_CNV_rubric_code'
            elif not synthetic and abs(pts) > 1:
                reason = 'CNV_item_points_outside_supported_range'
        if reason:
            rejected.append({'id': identity, 'reason': reason})
        else:
            accepted.append(dict(row, points=str(pts)))
            seen_basis.update(row['basis_ids'])
            if framework == 'SNV': seen_codes.add(base)
    blockers = []
    codes = {r.get('code') for r in accepted}
    # PVS1 provenance gate: strength must match a reviewed mechanism-tier calculation.
    # The review's points are not imported; only its tier/strength are cross-checked.
    pvs1_gate = pvs1_provenance(accepted, pvs1_review)
    if pvs1_review is not None or enforce_pvs1_provenance:
        blockers.extend(pvs1_gate['blockers'])
    # Only apply caller-supplied reviewed combination policy. No archival pair table is active.
    policy = data.get('combination_policy', {})
    if not all(policy.get(k) for k in ('source', 'version', 'reviewer', 'reviewed_at')) or policy.get('status') != 'reviewed':
        blockers.append('combination_policy_unreviewed')
    else:
        if policy.get('framework') != framework:
            blockers.append('combination_policy_framework_mismatch')
        for pair in policy.get('mutually_exclusive', []):
            if len(pair) != 2: raise ValueError('mutual exclusion must be a pair')
            if set(pair) <= codes: blockers.append('mutually_exclusive:' + '/'.join(pair))
        for cap in policy.get('caps', []):
            rows = [r for r in accepted if r.get('code') in cap['codes']]
            subtotal = sum((abs(decimal(r['points'])) for r in rows), Decimal(0))
            if subtotal > decimal(cap['max_abs_points']): blockers.append('cap_exceeded:' + '/'.join(cap['codes']))
    if framework == 'SNV':
        if {'PVS1', 'PM4'} <= seen_codes:
            blockers.append('PVS1_PM4_double_counting')
        # Hard mutual-exclusion pairs for the newly-admitted evidence kinds
        # (ACMG/AMP + ACGS/CanVIG "禁止" combinations). Pre-existing-code pairs that
        # the 2015 Table-5 structure still legitimately combines are left to the
        # caller's combination_policy, not hard-blocked here.
        hard_mutex = [
            ('PS1','PM5'),
            ('PM4','PS1'), ('PM4','PM5'), ('PM4','PP2'), ('PM4','PP3'),
            ('PM1','PM5'),
            ('PP2','PM5'),
            ('PS4','PS2'), ('PS4','PM6'),
            ('BS2','BP2'),
        ]
        for x, y in hard_mutex:
            if {x, y} <= seen_codes:
                blockers.append('mutually_exclusive:' + '/'.join(sorted([x, y])))
        pm1pp3 = [r for r in accepted if r['code'].split('_')[0] in ('PM1','PP3')]
        if {'PM1','PP3'} <= seen_codes and sum(decimal(r['points']) for r in pm1pp3) > 4:
            blockers.append('PM1_PP3_combined_strength_exceeds_Strong')
        if {'PS2', 'PM6'} <= seen_codes:
            blockers.append('de_novo_codes_must_be_aggregated')
        for a in accepted:
            for b in accepted:
                if a['code'].split('_')[0] == 'PVS1' and b['code'].split('_')[0] == 'PP3':
                    if not a.get('mechanism') or not b.get('mechanism') or a['mechanism'] == b['mechanism']:
                        blockers.append('PVS1_PP3_mechanism_overlap_or_unknown')
    if rejected: blockers.append('some_evidence_excluded')
    if not accepted: blockers.append('no_accepted_evidence')
    total = sum((decimal(r['points']) for r in accepted), Decimal(0))
    comparator = compare(accepted) if framework == 'SNV' and not blockers else {
        'candidate':None, 'status':'not_applicable' if framework != 'SNV' else 'blocked', 'reasons':blockers}
    point_candidate = partition(total, framework).replace('_range','') if accepted and not blockers else None
    difference = point_candidate != comparator.get('candidate') if point_candidate and comparator.get('candidate') else None
    reaudit = framework_reaudit(accepted, difference)
    return {'primary_framework': 'Tavtigian_2020_points' if framework == 'SNV' else 'Riggs_2020',
            'point_candidate': point_candidate, 'acmg_2015_comparison': comparator,
            'framework_disagreement': difference,
            'reaudit_required': reaudit,
            'difference_note': 'Compare strengths and framework versions; do not select the higher category; re-audit the strongest evidence when reaudit_required is set' if difference else None,
            'framework': framework, 'accepted': accepted, 'excluded': rejected, 'net_points': str(total),
            'sandbox_partition': partition(total, framework) if accepted and not blockers else None,
            'pvs1_gate': pvs1_gate,
            'classification': None, 'status': 'test_only_not_clinically_validated', 'blockers': blockers,
            'limitations': ['source-checked arithmetic is not clinical validation; classification stays null',
                            'Table 5 comparison uses supplied strengths; BA1 exceptions, VCEP and fractional SNV framework are not automated',
                            'PVS1_VeryStrong requires a matching mechanism-tier review with audited independent LoF counts']}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument('json_file'); args = ap.parse_args()
    try:
        with open(args.json_file) as f: result = score(json.load(f))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, TypeError, KeyError) as e:
        ap.error(str(e))
