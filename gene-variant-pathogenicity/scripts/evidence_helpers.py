"""Source-checked test calculations, never direct evidence or clinical classification."""
from decimal import Decimal
from score import decimal


def de_novo_strength(case_points, heterogeneity_points='0'):
    """Input subtotals have already been reviewed. No inference of parentage or phenotype.

    Other inheritance/mosaicism adjustments are NOT performed by this helper.
    High heterogeneity subtotal is separately capped; never add it twice.
    """
    ordinary, hetero = decimal(case_points), decimal(heterogeneity_points)
    if ordinary < 0 or hetero < 0: raise ValueError('negative de novo subtotal')
    if (ordinary*4) % 1 or (hetero*4) % 1: raise ValueError('subtotals must use quarter-point increments')
    total = ordinary + min(hetero,Decimal(1))
    strength = next((s for cutoff,s in [(4,'VeryStrong'),(2,'Strong'),(1,'Moderate'),(Decimal('.5'),'Supporting')] if total>=cutoff), None)
    return {'case_points':str(total), 'uncapped_heterogeneity_points':str(hetero),
            'strength_before_inheritance_adjustments':strength,'evidence_code':None,
            'classification':None,'status':'test_calculation_only',
            'requires':['case deduplication','parental relationship assessment','parental variant testing',
                        'phenotype category review','AR/X-linked/mosaicism exceptions','case-specific rule review']}


def revel_band(value, *, missense=False, identity_validated=False, calibration_selected=False):
    """Table 2 band only. No gene-specific applicability, no automatic evidence creation."""
    if value is None: return {'status':'unavailable','band':None,'evidence_code':None}
    n=decimal(value)
    if n<0 or n>1: raise ValueError('REVEL outside [0,1]')
    if not all(x is True for x in (missense,identity_validated,calibration_selected)):
        return {'status':'prerequisites_unreviewed','band':None,'evidence_code':None}
    if n<=Decimal('.003'): band='BP4_VeryStrong'
    elif n<=Decimal('.016'): band='BP4_Strong'
    elif n<=Decimal('.183'): band='BP4_Moderate'
    elif n<=Decimal('.290'): band='BP4_Supporting'
    elif n<Decimal('.644'): band='Indeterminate'
    elif n<Decimal('.773'): band='PP3_Supporting'
    elif n<Decimal('.932'): band='PP3_Moderate'
    else: band='PP3_Strong'
    return {'status':'test_calibration_band_only','band':band,'evidence_code':None,
            'requires':'gene/disease applicability, preselected tool/version, strength ceiling and combination review'}
