from cnv_manual_review import blank

def reviewed(d):
    r=blank(d);r.update(reviewer='SYNTHETIC TEST ONLY',reviewed_at='2026-09-27')
    for key,s in r['sections'].items():
        s.update(status='reviewed',conclusion='Synthetic engineering fixture, not a clinical review',source='synthetic fixture',location='test')
        s['checks']={x:'Synthetic reviewed fixture only' for x in s['checks']}
        if key=='section2':s['evidence_ids']=['cnv-section2']
        elif key in ['section1','section3','section4','section5']:s['evidence_ids']=[x['id'] for x in d['scoring']['evidence'] if x['code'].startswith(key[-1])]
    d['manual_review']=r
    return d
