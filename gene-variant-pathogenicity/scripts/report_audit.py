"""Pure report helpers: preserve unknowns, separate claims and metadata verification."""
from decimal import Decimal

def citation_coverage(citations):
    ids = [r.get('id') for r in citations]
    if any(not isinstance(x,str) or not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError('unique citation IDs required')
    total = len(citations)
    meta = sum(r.get('metadata_verified') is True for r in citations)
    claims = sum(r.get('claim_verified') is True for r in citations)
    both = sum(r.get('metadata_verified') is True and r.get('claim_verified') is True for r in citations)
    return {'total':total,'metadata_verified':meta,'claim_verified':claims,'fully_verified':both,
            'coverage_percent': str(Decimal(both)*100/total) if total else None,
            'status':'available' if total else 'not_applicable'}

def search_statement(date, scopes, status):
    if status != 'success': return '检索未完成；不能据此判断有无既往记录。'
    if not date or not scopes: raise ValueError('date and search scope required')
    return f'截至{date}，在所列数据库与文献范围内未发现既往记录：' + '、'.join(scopes)

def sample_qc(sample):
    # Local SOPs are not provided; no field values can activate this policy.
    return {'status':'not_evaluated','automatic_acceptance':False,
            'mcc':sample.get('mcc'), 'vaf':sample.get('vaf'), 'depth':sample.get('depth'),
            'mosaicism':None,'validated_lod':None,'gonadal_risk_upper_bound':None,
            'reason':'local assay validation and SOP absent; values retained for manual review'}


STRENGTHS = ['Supporting', 'Moderate', 'Strong', 'VeryStrong']


def pvs1_strength(code):
    """Return the PVS1 strength encoded in a code, or None for non-PVS1 codes."""
    if not isinstance(code, str):
        return None
    base, _, suffix = code.partition('_')
    if base != 'PVS1':
        return None
    return suffix or 'VeryStrong'


def pvs1_provenance(evidence_rows, review):
    """Gate PVS1 evidence against its reviewed mechanism-tier calculation.

    A PVS1 row is only acceptable when the review exists, is not blocked, and its
    adjusted strength equals the row strength.  PVS1_VeryStrong additionally needs
    mechanism tier G1 and counts audited against a per-variant lof_evidence list
    (SVI 2018 Table 1: >=3 independent pathogenic LoF AND >10% LoF fraction).
    The review's points are never imported into the score.
    """
    rows = [r for r in evidence_rows if pvs1_strength(r.get('code'))]
    result = {'applicable': bool(rows), 'blockers': [], 'tier': None,
              'adjusted_strength': None, 'counts_audited': None, 'strengths': []}
    if not rows:
        return result
    result['strengths'] = [pvs1_strength(r.get('code')) for r in rows]
    if not isinstance(review, dict):
        result['blockers'].append('pvs1_mechanism_review_missing')
        return result
    tier = review.get('mechanism_tier')
    adjusted = review.get('adjusted_strength')
    status = review.get('status')
    result.update(tier=tier, adjusted_strength=adjusted,
                  counts_audited=review.get('counts_audited'))
    if status != 'test_calculation_only' or adjusted not in STRENGTHS:
        result['blockers'].append('pvs1_review_blocked')
        return result
    for strength in result['strengths']:
        if strength != adjusted:
            result['blockers'].append('pvs1_strength_mismatch:%s->%s' % (strength, adjusted))
        if strength == 'VeryStrong':
            if tier != 'G1':
                result['blockers'].append('pvs1_very_strong_requires_G1')
            if review.get('counts_audited') is not True:
                result['blockers'].append('pvs1_independent_lof_counts_not_audited')
    return result


def framework_reaudit(evidence_rows, disagreement):
    """When points and 2015 structure disagree, require re-audit of the strongest rule.

    The caller still decides the classification; this flag prevents closing the
    discrepancy as a pure 'version difference' without re-checking the rule that
    carries the most points (typically PVS1/PS2/PS3).
    """
    if not disagreement:
        return None
    scored = []
    for row in evidence_rows:
        try:
            pts = abs(float(row.get('points')))
        except (TypeError, ValueError):
            continue
        scored.append((pts, row))
    if not scored:
        return None
    _, strongest = max(scored, key=lambda x: x[0])
    base = str(strongest.get('code', '')).split('_')[0]
    if base not in ('PVS1', 'PS2', 'PS3'):
        return None
    return {'code': strongest.get('code'), 'base': base,
            'reason': 'framework_disagreement_requires_reaudit_of_strongest_evidence'}
