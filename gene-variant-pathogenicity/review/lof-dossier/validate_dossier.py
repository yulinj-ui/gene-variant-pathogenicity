"""Offline completeness/provenance audit only. Never emits a clinical input or score."""
import json,hashlib,sys,importlib,unittest,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parent
COUNTS={'independent_pathogenic_lof_count','phenotype_lof_count','phenotype_total_count','associated_lof_count'}
BOOLS={'multiple_exons','single_exon_gene','null_mouse'}
FIELDS=COUNTS|BOOLS|{'lof_mechanism','association'}
def audit(d,sources):
    blockers=[];known={s['id'] for s in sources}
    for k in sorted(FIELDS):
        f=d.get('fields',{}).get(k,{})
        v=f.get('value')
        if v is None: blockers.append(k+':unknown');continue
        if k in COUNTS and (type(v)!=int or v<0):blockers.append(k+':invalid_type')
        if k in BOOLS and type(v)!=bool:blockers.append(k+':invalid_type')
        if k=='association' and v not in ['limited','moderate','strong','definitive']:blockers.append(k+':invalid_value')
        if k=='lof_mechanism' and v not in ['established','absent']:blockers.append(k+':invalid_value')
        if not f.get('source_ids') or set(f['source_ids'])-known:blockers.append(k+':invalid_source')
        if not f.get('location') or not f.get('rationale'):blockers.append(k+':missing_trace')
        if f.get('status')!='approved' or not f.get('reviewer') or not f.get('reviewed_at'):blockers.append(k+':not_signed_off')
    den=d.get('denominator',{})
    if not den.get('complete') or any(not den.get(k) for k in ['definition','inclusion','exclusion','deduplication','cutoff','variant_ids']):blockers.append('denominator:incomplete')
    if d.get('vcep',{}).get('generic_applicable') is not True:blockers.append('vcep:generic_not_approved')
    if not d.get('signoff',{}).get('approved'):blockers.append('dossier:not_signed_off')
    ids=[v.get('id') for v in d.get('variants',[])]
    if len(ids)!=len(set(ids)):blockers.append('variants:duplicate_id')
    return dict(status='blocked' if blockers else 'requires_semantic_review',blockers=blockers,automatic_score_import=False,program_input=None,evidence_code=None,classification=None)
def main():
    p=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parents[1]/'scripts'
    sys.path.insert(0,str(p));engine=importlib.import_module('pvs1_review')
    d=json.loads((ROOT/'MSH2_Lynch机制档案.json').read_text());s=json.loads((ROOT/'来源登记.json').read_text())
    result=audit(d,s)
    m={k:f['value'] for k,f in d['fields'].items()}
    try: legacy=engine.mechanism(m)
    except engine.Pending as e:legacy={'status':'blocked','reason':str(e)}
    class Tests(unittest.TestCase):
        def test_real_dossier_blocked(self):self.assertEqual(result['status'],'blocked')
        def test_no_export(self):self.assertIsNone(result['program_input'])
        def test_no_classification(self):self.assertIsNone(result['classification']);self.assertFalse(result['automatic_score_import'])
        def test_legacy_missing_count(self):self.assertEqual(legacy['status'],'blocked');self.assertIn('independent_pathogenic_lof_count',legacy['reason'])
        def test_original_variants(self):self.assertEqual(len(d['variants']),9);self.assertEqual(d['count_discrepancy']['summary_unique_variants'],8)
        def test_no_independent_P_assumed(self):self.assertTrue(all(v['independent_pathogenic_without_pvs1'] is None for v in d['variants']))
        def test_transcript_difference(self):self.assertEqual(d['variants'][0]['original_transcript'],'NM_000251.2');self.assertTrue(d['variants'][0]['reported_hgvs'].startswith('NM_000251.3:'))
        def test_unknown_not_false(self):self.assertIsNone(m['null_mouse']);self.assertIsNone(m['multiple_exons'])
        def test_vcep_block(self):self.assertIn('vcep:generic_not_approved',result['blockers'])
        def test_bad_source(self):
            x=copy.deepcopy(d);x['fields']['association']['source_ids']=['FAKE'];self.assertIn('association:invalid_source',audit(x,s)['blockers'])
        def test_bool_is_not_count(self):
            x=copy.deepcopy(d);x['fields']['associated_lof_count']['value']=True;self.assertIn('associated_lof_count:invalid_type',audit(x,s)['blockers'])
        def test_duplicate(self):
            x=copy.deepcopy(d);x['variants'].append(x['variants'][0]);self.assertIn('variants:duplicate_id',audit(x,s)['blockers'])
        def test_source_hashes(self):
            for e in s:
                if e['snapshot']:self.assertEqual(hashlib.sha256((ROOT/e['snapshot']).read_bytes()).hexdigest(),e['sha256'])
    with (ROOT/'离线测试报告.txt').open('w') as log:
        run=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
    result['existing_v5_mechanism_call']=legacy
    result['tests']={'run':run.testsRun,'failures':len(run.failures),'errors':len(run.errors)}
    (ROOT/'输入核验结果.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result['tests']));return 0 if run.wasSuccessful() else 1
if __name__=='__main__':raise SystemExit(main())
