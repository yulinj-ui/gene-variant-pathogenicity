import copy,unittest
from test_v5r2 import case
from cnv_case import run
from cnv_manual_review import TOPICS,digest,blank
from render_report import render
class MandatoryReviewTests(unittest.TestCase):
    def blocked(self,d):
        r=run(d);self.assertIsNone(r['authoritative_candidate']);self.assertTrue(r['blockers']);self.assertIsNone(r['classification'])
    def test_reviewed_candidate(self):self.assertEqual(run(case())['authoritative_candidate'],'P')
    def test_missing_review(self):
        d=case();del d['manual_review'];self.blocked(d)
    def test_blank_template(self):
        d=case();d['manual_review']=blank(d);self.blocked(d)
    def test_every_section_required(self):
        for k in TOPICS:
            with self.subTest(section=k):
                d=case();del d['manual_review']['sections'][k];self.blocked(d)
    def test_every_check_required(self):
        for k,checks in TOPICS.items():
            for c in checks:
                with self.subTest(section=k,check=c):
                    d=case();d['manual_review']['sections'][k]['checks'][c]='';self.blocked(d)
    def test_pending_unavailable_conflict(self):
        for status in ['pending','unavailable','conflict']:
            d=case();d['manual_review']['sections']['section4']['status']=status;self.blocked(d)
    def test_na_needs_rule(self):
        d=case();d['manual_review']['sections']['section4']['status']='not_applicable';self.blocked(d)
    def test_documented_skip(self):
        d=case();d['manual_review']['sections']['section4'].update(status='not_applicable',applicability_rule='synthetic rule',applicability_location='test');self.assertEqual(run(d)['authoritative_candidate'],'P')
    def test_unresolved_conflict(self):
        d=case();d['manual_review']['sections']['integration']['unresolved_issues']=['conflicting evidence'];self.blocked(d)
    def test_stale_input(self):
        for key in ['identity','scoring','integration_review','section2_input']:
            d=case();d[key]['changed']='test';self.blocked(d) if key not in ['identity','section2_input'] else self.assertNotEqual(digest(d),d['manual_review']['input_sha256'])
    def test_ai_signoff_forbidden(self):
        d=case();d['manual_review']['reviewer_role']='assistant';self.blocked(d)
    def test_missing_signer(self):
        d=case();d['manual_review']['reviewer']='';self.blocked(d)
    def test_source_required(self):
        d=case();d['manual_review']['sections']['section1']['source']='';self.blocked(d)
    def test_evidence_coverage(self):
        d=case();d['manual_review']['sections']['section3']['evidence_ids']=['nonexistent'];self.blocked(d)
    def test_exclusion_reason_required(self):
        d=case();d['manual_review']['sections']['section4']['exclusions']=[{'item':'test'}];self.blocked(d)
    def test_raw_report_cannot_bypass(self):
        d=case();s=render({'scoring':d['scoring']});self.assertIn('CNV_manual_review_pipeline_required',s);self.assertIn('测试候选分区：未提供/未评估',s)
    def test_blocked_report_audit(self):
        d=case();d['manual_review']=blank(d);s=render({'variant_id':d['identity']['variant_id'],'cnv_pipeline':d});self.assertEqual(s.count('## 模块'),10);self.assertIn('manual_review',s);self.assertIn('测试候选分区：未提供/未评估',s)
