"""Table-5 comparison on already reviewed evidence; never a clinical classifier."""
import re
from collections import Counter
from decimal import Decimal

DEFAULTS = {'PVS1': 8, **{f'PS{i}': 4 for i in range(1,5)},
            **{f'PM{i}': 2 for i in range(1,7)}, **{f'PP{i}': 1 for i in range(1,6)},
            **{f'BS{i}': -4 for i in range(1,5)}, **{f'BP{i}': -1 for i in range(1,8)}}
STRENGTH = {'Supporting':1, 'Moderate':2, 'Strong':4, 'VeryStrong':8}


def decode(code):
    if code == 'BA1':
        return code, None
    m = re.fullmatch(r'(PVS1|PS[1-4]|PM[1-6]|PP[1-5]|BS[1-4]|BP[1-7])(?:_(Supporting|Moderate|Strong|VeryStrong))?', code)
    if not m:
        raise ValueError('unsupported evidence code: ' + code)
    base, strength = m.groups()
    points = DEFAULTS[base] if strength is None else STRENGTH[strength] * (-1 if base.startswith('B') else 1)
    return base, points


def compare(rows):
    """Apply Table 5 structure to supplied strengths, not original strength assignment.

    Extensions lacking a Table-5 bin are unavailable, never rounded or discarded.
    BA1 is intentionally not automated until exception evaluation is implemented.
    """
    reasons, seen, counts = [], set(), Counter()
    for row in rows:
        try:
            base, expected = decode(row['code'])
        except ValueError as e:
            reasons.append(str(e)); continue
        if base in seen:
            reasons.append('duplicate_code_family:' + base)
        seen.add(base)
        if expected is None:
            reasons.append('BA1_exception_workflow_not_implemented'); continue
        actual = Decimal(str(row['points']))
        if actual != expected:
            reasons.append('code_points_mismatch:' + row['code']); continue
        if expected in (-2, -8):
            reasons.append('benign_strength_absent_from_2015_table:' + row['code']); continue
        counts[expected] += 1
    result = {'framework':'ACMG_2015_Table5_on_reviewed_strengths', 'candidate':None,
              'matched_rules':[], 'status':'unavailable' if reasons or not rows else 'test_only',
              'reasons': reasons or ([] if rows else ['no_accepted_evidence']),
              'note':'2015 combining structure on supplied strengths; no automatic strength restoration or later combination amendments'}
    if result['status'] == 'unavailable': return result
    vs, st, mo, su, bs, bp = (counts[x] for x in (8,4,2,1,-4,-1))
    checks = {
        'P': [('P1a',vs>=1 and st>=1), ('P1b',vs>=1 and mo>=2),
              ('P1c',vs>=1 and mo>=1 and su>=1), ('P1d',vs>=1 and su>=2),
              ('P2',st>=2), ('P3a',st>=1 and mo>=3),
              ('P3b',st>=1 and mo>=2 and su>=2), ('P3c',st>=1 and mo>=1 and su>=4)],
        'LP':[('LP1',vs>=1 and mo>=1), ('LP2',st>=1 and mo>=1),
              ('LP3',st>=1 and su>=2), ('LP4',mo>=3),
              ('LP5',mo>=2 and su>=2), ('LP6',mo>=1 and su>=4)],
        'B':[('B2',bs>=2)], 'LB':[('LB1',bs>=1 and bp>=1),('LB2',bp>=2)]}
    hits = {k:[name for name,ok in v if ok] for k,v in checks.items()}
    result['matched_rules'] = [name for names in hits.values() for name in names]
    # Contradictory directions require review; Table 5 footnote, conservative display.
    if (vs+st+mo+su) and (bs+bp):
        result.update(candidate='VUS', reasons=['opposing_evidence_requires_review'])
    else:
        result['candidate'] = next((k for k in ('P','LP','B','LB') if hits[k]), 'VUS')
    return result
