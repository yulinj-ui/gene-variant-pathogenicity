#!/usr/bin/env python3
"""Interval geometry only. Never assigns dosage or clinical evidence."""
import argparse
import json


def normalize(d):
    if d.get('build') not in ('GRCh37', 'GRCh38') or d.get('system') not in ('one_based_closed', 'zero_based_half_open'):
        raise ValueError('explicit build and coordinate system required')
    start, end = d.get('start'), d.get('end')
    if any(isinstance(x, bool) or not isinstance(x, int) for x in (start, end)):
        raise ValueError('integer bounds required')
    if d['system'] == 'one_based_closed':
        start -= 1
    if start < 0 or end <= start:
        raise ValueError('invalid interval')
    chrom = str(d.get('chr', '')).removeprefix('chr')
    if chrom not in [str(i) for i in range(1, 23)] + ['X', 'Y', 'MT']:
        raise ValueError('invalid chromosome')
    return {'build': d['build'], 'chr': chrom, 'start': start, 'end': end}


def overlap(query, region):
    a, b = normalize(query), normalize(region)
    if a['build'] != b['build']:
        raise ValueError('build mismatch; no implicit liftover')
    length = max(0, min(a['end'], b['end']) - max(a['start'], b['start'])) if a['chr'] == b['chr'] else 0
    return {'overlap_bp': length, 'region_fraction': length / (b['end'] - b['start']),
            'query_fraction': length / (a['end'] - a['start']),
            'fully_covers_region': length == b['end'] - b['start'], 'evidence_code': None}


def envelope(minimum, maximum, target):
    """Operational uncertainty audit, not a new medical scoring rule."""
    lo,hi=normalize(minimum),normalize(maximum)
    if (lo['build'],lo['chr'])!=(hi['build'],hi['chr']) or not hi['start']<=lo['start']<lo['end']<=hi['end']:
        raise ValueError('minimum must be contained within maximum on the same assembly/chromosome')
    a,b=overlap(minimum,target),overlap(maximum,target)
    state='stable_full_cover' if a['fully_covers_region'] else 'no_overlap' if b['overlap_bp']==0 else 'boundary_dependent_or_partial'
    return dict(minimum=a,maximum=b,geometry_state=state,clinical_code=None,classification=None,
        note='Min/max scenario comparison is an operational aid; no automatic scoring or least-numeric-score selection')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('json_file'); args = ap.parse_args()
    with open(args.json_file) as f:
        data = json.load(f)
    print(json.dumps(overlap(data['query'], data['region']), indent=2))
