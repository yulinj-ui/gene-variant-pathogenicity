"""Match the published July 2018 BA1 exclusions. A negative match never proves BA1."""
import json,argparse
from pathlib import Path
TABLE=json.loads((Path(__file__).resolve().parents[1]/'references/ba1-exceptions-2018.json').read_text())
def match(data):
    found=set(); channels=[]; unknown=[]
    for key in ('allele_registry_id','clinvar_variation_id','hgvs','coordinate'):
        if key not in data:continue
        v=data[key]
        if key=='coordinate':
            if not isinstance(v,dict) or set(v)!={'build','chrom','pos','ref','alt'}:raise ValueError('exact normalized coordinate record required')
            if v['build']!='GRCh37':unknown.append('build_not_supported');continue
            if type(v['pos']) is not int or v['pos']<1:raise ValueError('positive integer coordinate required')
        hits={r['id'] for r in TABLE['variants'] if r[key]==v}
        channels.append(hits);found|=hits
    if not channels:unknown.append('no_supported_identity')
    # A known identifier plus a different/unmatched supplied alias must not be silently accepted.
    if found and (len(found)>1 or any(x!=found for x in channels)):unknown.append('identity_conflict')
    status='identity_unresolved' if unknown else 'exception_match' if found else 'not_in_snapshot'
    return dict(status=status,matched_ids=sorted(found),blockers=unknown,snapshot=TABLE['version'],
        clinical_classification=None,BA1_eligible=None,
        note='Historical exclusion matching only; negative result requires current-list, gene/disease/VCEP and population review')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args()
    print(json.dumps(match(json.loads(Path(a.input).read_text())),ensure_ascii=False,indent=2))
