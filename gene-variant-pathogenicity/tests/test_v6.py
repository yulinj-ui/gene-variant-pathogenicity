import copy,unittest
from assisted_case import run
from render_report import render
ACTOR='DeepSeek Harness (autonomous evidence review)'
def fixture():
 i=dict(variant_id='SYNTHETIC',gene='SYNTHETIC',disease='synthetic',inheritance='AD')
 rev=dict(approved=True,reviewer=ACTOR,reviewed_at='2026-09-27',source='synthetic',location='fixture',rationale='engineering only')
 rule=dict(code='PM2_Supporting',framework='SNV',status='reviewed',source='synthetic',version='test',location='fixture',reviewer=ACTOR,reviewed_at='2026-09-27',applicability='synthetic',allowed_points=[1])
 row=dict(id='e1',code='PM2_Supporting',framework='SNV',rule_id='r',status='reviewed',gate='passed',points=1,source_ids=['source'],basis_ids=['unique'],rationale='synthetic')
 c=dict(identity=i,routing=dict(identity=i,review=rev,searches=[dict(url='synthetic',query='gene',accessed_at='2026-09-27',result='none')],search_completed=True,outcome='none_found'),scoring=dict(framework='SNV',rules={'r':rule},evidence=[row],combination_policy=dict(status='reviewed',framework='SNV',source='synthetic',version='test',reviewer=ACTOR,reviewed_at='2026-09-27',mutually_exclusive=[],caps=[])),admissions=[])
 a=dict(identity=i,performed_by='DeepSeek Harness',review_type='autonomous_assist',critical_issues=[],decisions=[dict(id='e1',code='PM2_Supporting',disposition='include',finding='synthetic',source='synthetic',rationale='synthetic',origin='public_primary',applicability='synthetic')])
 for k in ['variant_identity','disease_mechanism','phenotype_fit','rule_search','pathogenic_evidence_search','benign_evidence_search','independence','external_report_comparison','limitations']:a[k]=dict(finding='synthetic',source='synthetic',rationale='synthetic')
 return dict(framework='SNV',case=c,assessment=a)
class AutonomousTests(unittest.TestCase):
 def test_no_human_signature_required(self):self.assertEqual(run(fixture())['independent_classification'],'VUS')
 def test_unknown_quality_not_global_blocker(self):
  d=fixture();d['assessment']['limitations']['finding']='External BAM and MCC unavailable';self.assertEqual(run(d)['independent_classification'],'VUS')
 def test_unavailable_code_not_blocker(self):
  d=fixture();d['assessment']['decisions'].append(dict(id='pvs1',code='PVS1',disposition='unavailable',finding='mechanism unresolved',source='synthetic',rationale='not enough',origin='user_history'));self.assertEqual(run(d)['independent_classification'],'VUS')
 def test_critical_identity_issue_blocks(self):
  d=fixture();d['assessment']['critical_issues']=['ambiguous allele'];self.assertIsNone(run(d)['independent_classification'])
 def test_no_fabricated_human(self):
  d=fixture();d['case']['routing']['review']['reviewer']='Human not consulted';self.assertIn('misleading_reviewer_identity',run(d)['blockers'])
 def test_external_classification_not_evidence(self):
  d=fixture();d['assessment']['decisions'][0]['origin']='external_classification';self.assertIsNone(run(d)['independent_classification'])
 def test_unverified_assumption_not_primary(self):
  d=fixture();d['assessment']['decisions'][0]['origin']='unverified_assumption';self.assertIsNone(run(d)['independent_classification'])
 def test_explicit_report_fact_with_applicability(self):
  d=fixture();d['assessment']['decisions'][0]['origin']='external_report_explicit';self.assertEqual(run(d)['independent_classification'],'VUS')
 def test_no_evidence_not_forced_VUS(self):
  d=fixture();d['case']['scoring']['evidence']=[];d['assessment']['decisions']=[];self.assertIsNone(run(d)['independent_classification'])
 def test_search_failure_does_not_mean_none(self):
  d=fixture();d['case']['routing']['search_completed']=False;self.assertIsNone(run(d)['independent_classification'])
 def test_decision_inventory(self):
  d=fixture();d['assessment']['decisions']=[];self.assertIsNone(run(d)['independent_classification'])
 def test_no_clinical_signoff(self):self.assertIsNone(run(fixture())['clinical_signoff'])
 def test_report_ten_sections(self):
  d=fixture();s=render(dict(variant_id='SYNTHETIC',assisted_case=d));self.assertEqual(s.count('## 模块'),10);self.assertIn('本次独立辅助评级：VUS',s)
 def test_report_blocked(self):
  d=fixture();d['assessment']['critical_issues']=['unclear'];s=render(dict(variant_id='SYNTHETIC',assisted_case=d));self.assertNotIn('本次独立辅助评级：VUS',s)
 def test_benign_search_required(self):
  d=fixture();del d['assessment']['benign_evidence_search'];self.assertIsNone(run(d)['independent_classification'])
 def test_cnv_autonomous_review(self):
  from test_v5r2 import case
  from cnv_manual_review import digest
  c=case();c['review_mode']='autonomous_assist';c['integration_review']['reviewer']=ACTOR
  c['manual_review'].update(reviewer=ACTOR,reviewer_role='deepseek_harness_assistant');c['manual_review']['input_sha256']=digest(c)
  d=fixture();d.update(framework='CNV',case=c);d['assessment']['identity']=c['identity'];d['assessment']['decisions'][0].update(id='cnv-section2',code='2A')
  self.assertEqual(run(d)['independent_classification'],'P')
 def test_decision_code_binding(self):
  d=fixture();d['assessment']['decisions'][0]['code']='PS2';self.assertIsNone(run(d)['independent_classification'])
 def test_blocked_comparison_not_published(self):
  d=fixture();d['assessment']['critical_issues']=['identity'];s=render(dict(variant_id='SYNTHETIC',assisted_case=d));self.assertIn('2015组合对照：未提供/未评估',s)
