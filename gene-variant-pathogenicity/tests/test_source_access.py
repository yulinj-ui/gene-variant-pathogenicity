import copy
import datetime
import email.utils
import gzip
import hashlib
import http.client
import io
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import Mock, patch
import urllib.error
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import genebe_fields as g
import source_http as h
HGVS='NM_017780.4:c.2831G>A'


def fixture():
    return json.loads((ROOT/'tests/fixtures/public-chd7-live-20260927.json').read_text())


class AdapterTests(unittest.TestCase):
    def run_case(self, edit=None, bind=False):
        f=fixture()
        if edit: edit(f)
        if bind:
            for name,data in f['responses'].items():
                f['request_metadata'][name]=g.request_receipt(f['request_metadata'][name]['url'],data)
        return g.to_evidence(HGVS,f['responses'],f['request_metadata'])

    def test_real_partial_response(self):
        r=self.run_case();self.assertTrue(r['protein_gate']['passed']);self.assertEqual(r['frequency']['eas']['ac'],278)
        self.assertEqual(r['_sources']['worker']['status'],'partial');self.assertIsNone(r['codon_landscape'])
        self.assertEqual(r['predictors']['CADD']['value'],22.9);self.assertIsNone(r['classification'])

    def test_missing_receipt_fails_closed(self):
        f=fixture();r=g.to_evidence(HGVS,f['responses'])
        self.assertEqual(r['_sources']['genebe']['status'],'unavailable');self.assertEqual(r['_sources']['worker']['status'],'unavailable')

    def test_modified_response_invalidates_receipt(self):
        r=self.run_case(lambda f:f['responses']['genebe']['variants'][0].update(alt='T'))
        self.assertEqual(r['_sources']['genebe']['status'],'unavailable')

    def test_wrong_request_build(self):
        r=self.run_case(lambda f:f['request_metadata']['genebe'].update(url=f['request_metadata']['genebe']['url'].replace('hg38','hg19')))
        self.assertEqual(r['_sources']['genebe']['status'],'unavailable')

    def test_wrong_request_allele(self):
        r=self.run_case(lambda f:f['request_metadata']['genebe'].update(url=f['request_metadata']['genebe']['url'].replace('alt=A','alt=T')))
        self.assertEqual(r['_sources']['genebe']['status'],'unavailable')

    def test_duplicate_request_build(self):
        r=self.run_case(lambda f:f['request_metadata']['genebe'].update(url=f['request_metadata']['genebe']['url']+'&genome=hg19'))
        self.assertEqual(r['_sources']['genebe']['status'],'unavailable')

    def test_conflicting_response_build(self):
        r=self.run_case(lambda f:f['responses']['genebe']['variants'][0].update(genome='hg19'),True)
        self.assertEqual(r['_sources']['genebe']['status'],'unavailable')

    def test_worker_wrong_refseq_assembly(self):
        r=self.run_case(lambda f:f['responses']['worker']['coord'].update(hgvsg='NC_000008.10:g.60821923G>A'),True)
        self.assertEqual(r['_sources']['worker']['status'],'unavailable')

    def test_worker_wrong_hgvs(self):
        r=self.run_case(lambda f:f['responses']['worker']['query'].update(hgvs='NM_017780.4:c.2831G>T'),True)
        self.assertEqual(r['_sources']['worker']['status'],'unavailable')

    def test_failed_frequency_source_masks_data(self):
        r=self.run_case(lambda f:f['responses']['worker']['sources'].update(gnomad_variant='error'),True)
        self.assertIsNone(r['frequency']['global']['ac']);self.assertNotIn('CADD',r['predictors'])
        self.assertIn('REVEL',r['predictors'])

    def test_missing_constraint_source_masks_data(self):
        r=self.run_case(lambda f:f['responses']['worker']['sources'].pop('gnomad_gene'),True)
        self.assertIsNone(r['constraint'])

    def test_worker_unknown_predictor_source_ignored(self):
        r=self.run_case(lambda f:f['responses']['worker']['merged_predictors'].append({'id':'REVEL','value':0.9,'source':'unknown'}),True)
        self.assertEqual(r['predictors']['REVEL']['value'],0.521)

    def test_string_predictor_bounds(self):
        r=self.run_case(lambda f:f['responses']['worker']['merged_predictors'].append({'id':'REVEL_MAX','value':'1.1','source':'gnomAD'}),True)
        self.assertEqual(r['predictors']['REVEL_MAX']['value'],0.521);self.assertIn('invalid predictor REVEL_MAX',r['_warnings'])

    def test_nonfinite_predictor_rejected(self):
        r=self.run_case(lambda f:f['responses']['worker']['merged_predictors'].append({'id':'TEST','value':'NaN','source':'VEP'}),True)
        self.assertNotIn('TEST',r['predictors'])

    def test_raw_export_replay_cli(self):
        f=fixture()
        export={'responses':f['responses'],'evidence':{'_request_metadata':f['request_metadata']}}
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'raw.json';path.write_text(json.dumps(export))
            proc=subprocess.run([sys.executable,str(ROOT/'scripts/genebe_fields.py'),HGVS,'--fixture',str(path)],capture_output=True,text=True,check=True)
            result=json.loads(proc.stdout)
            self.assertTrue(result['protein_gate']['passed'])
            self.assertEqual(result['frequency']['global']['ac'],381)

    def test_worker_endpoint_suffix_and_typed_failure(self):
        f=fixture();urls=[]
        def fetch(url,auth=None):
            urls.append(url)
            if 'VariantValidator/' in url:return f['responses']['variantvalidator']
            if 'api.genebe.net' in url:return f['responses']['genebe']
            raise h.FetchError('rate_limited',429,120)
        with patch.object(g,'get_json',side_effect=fetch):
            r,_=g.annotate(HGVS,'https://example.org/annotate')
        self.assertFalse(any('/annotate/annotate' in u for u in urls))
        self.assertEqual(r['_fetch_status']['worker']['status'],'rate_limited')
        self.assertIsNone(r['frequency']['global']['af'])


class Response(io.BytesIO):
    def __init__(self,data,status=200,headers=None):
        super().__init__(data);self.status=status;self.headers=headers or {}


class HttpTests(unittest.TestCase):
    def fetch(self,responses,**kwargs):
        opener=Mock();opener.open.side_effect=responses
        with patch.object(h.urllib.request,'build_opener',return_value=opener),patch.object(h.time,'sleep') as sleep:
            result=h.fetch_bytes('https://example.org/data',**kwargs)
        return result,opener,sleep

    def test_429_retry_after(self):
        err=urllib.error.HTTPError('https://example.org',429,'',{'Retry-After':'4'},None)
        (_,r),opener,sleep=self.fetch([err,Response(b'{"ok":true}')])
        self.assertEqual(r['attempts'],2);sleep.assert_called_once_with(4)

    def test_long_retry_after_does_not_retry_early(self):
        opener=Mock();opener.open.side_effect=urllib.error.HTTPError('https://example.org',429,'',{'Retry-After':'120'},None)
        with patch.object(h.urllib.request,'build_opener',return_value=opener),patch.object(h.time,'sleep') as sl:
            with self.assertRaises(h.FetchError) as ctx:h.fetch_bytes('https://example.org')
        self.assertEqual(ctx.exception.code,'rate_limited');self.assertEqual(ctx.exception.retry_after,120)
        self.assertEqual(opener.open.call_count,1);sl.assert_not_called()

    def test_retry_after_date(self):
        date=email.utils.format_datetime(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=120))
        self.assertGreater(h.retry_seconds(date),115)

    def test_challenge_200(self):
        with self.assertRaises(h.FetchError) as c:self.fetch([Response(b'<html>reCAPTCHA</html>')])
        self.assertEqual(c.exception.code,'challenge_page')

    def test_login_html_not_json(self):
        with self.assertRaises(h.FetchError) as c:self.fetch([Response(b'<!doctype html><html>Log in</html>')])
        self.assertEqual(c.exception.code,'unexpected_html')

    def test_graphql_200_errors(self):
        with self.assertRaises(h.FetchError) as c:self.fetch([Response(b'{"errors":[{"message":"Variant not found"}],"data":{"variant":null}}')])
        self.assertEqual(c.exception.code,'api_error')

    def test_content_length_mismatch(self):
        with self.assertRaises(h.FetchError) as c:self.fetch([Response(b'{}',headers={'Content-Length':'50'})],attempts=1)
        self.assertEqual(c.exception.code,'incomplete_download')

    def test_partial_http_status(self):
        with self.assertRaises(h.FetchError) as c:self.fetch([Response(b'{}',status=206)],attempts=1)
        self.assertEqual(c.exception.code,'incomplete_download')

    def test_incomplete_read(self):
        with self.assertRaises(h.FetchError) as c:self.fetch([http.client.IncompleteRead(b'{',20)],attempts=1)
        self.assertEqual(c.exception.code,'incomplete_download')

    def test_hash_mismatch(self):
        with self.assertRaises(h.FetchError) as c:self.fetch([Response(b'{}')],expected_sha256='0'*64)
        self.assertEqual(c.exception.code,'checksum_mismatch')

    def test_limit(self):
        with self.assertRaises(h.FetchError) as c:self.fetch([Response(b'{}')],max_bytes=1)
        self.assertEqual(c.exception.code,'file_too_large')

    def test_invalid_json(self):
        with self.assertRaises(h.FetchError):self.fetch([Response(b'{')])

    def test_nonfinite_json(self):
        with self.assertRaises(h.FetchError):self.fetch([Response(b'{"af":NaN}')])

    def test_gzip_crc(self):
        data=gzip.compress(b'valid table\n')
        with self.assertRaises(h.FetchError):self.fetch([Response(data[:-4])],kind='gzip')
        (body,_),_,_=self.fetch([Response(data)],kind='gzip');self.assertEqual(body,data)

    def test_pdf_truncated(self):
        with self.assertRaises(h.FetchError):self.fetch([Response(b'%PDF-1.7\nno trailer')],kind='pdf')

    def test_download_failure_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as td:
            dest=Path(td)/'scores.csv';dest.write_bytes(b'previous complete file')
            opener=Mock();opener.open.side_effect=TimeoutError('SECRET')
            with patch.object(h.urllib.request,'build_opener',return_value=opener):
                with self.assertRaises(h.FetchError) as ctx:h.download('https://example.org',dest,kind='text',attempts=1)
            self.assertEqual(dest.read_bytes(),b'previous complete file');self.assertEqual(len(list(Path(td).iterdir())),1)
            self.assertNotIn('SECRET',str(ctx.exception))

    def test_successful_atomic_download(self):
        with tempfile.TemporaryDirectory() as td:
            dest=Path(td)/'result.json';opener=Mock();opener.open.return_value=Response(b'{}')
            with patch.object(h.urllib.request,'build_opener',return_value=opener):
                r=h.download('https://example.org',dest,kind='json',expected_sha256=hashlib.sha256(b'{}').hexdigest())
            self.assertEqual(dest.read_bytes(),b'{}');self.assertEqual(r['integrity'],'expected_hash_verified')

    def test_redirect_not_retried(self):
        with self.assertRaises(h.FetchError) as c:self.fetch([urllib.error.HTTPError('https://example.org',302,'',{'Location':'https://other.org'},None)])
        self.assertEqual(c.exception.code,'redirect_blocked')

    def test_url_credentials_rejected(self):
        with self.assertRaises(ValueError):h.fetch_bytes('https://user:secret@example.org')


if __name__=='__main__':unittest.main()
