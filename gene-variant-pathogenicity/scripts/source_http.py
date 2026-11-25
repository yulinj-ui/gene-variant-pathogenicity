#!/usr/bin/env python3
"""Bounded, credential-safe retrieval; validated bytes are published atomically."""
import argparse
import base64
import datetime
import email.utils
import gzip
import hashlib
import http.client
import io
import json
import os
from pathlib import Path
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
import zlib


class FetchError(RuntimeError):
    def __init__(self, code, http_status=None, retry_after=None):
        self.code, self.http_status, self.retry_after = code, http_status, retry_after
        super().__init__('network unavailable' if code == 'network_error' else code)

    def record(self):
        return dict(status=self.code, http_status=self.http_status, retry_after_seconds=self.retry_after)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def retry_seconds(value):
    if not value:
        return None
    try:
        return max(0, int(value))
    except (ValueError, TypeError):
        try:
            return max(0, (email.utils.parsedate_to_datetime(value) - datetime.datetime.now(datetime.timezone.utc)).total_seconds())
        except (ValueError, TypeError, OverflowError):
            return None


def validate_body(body, kind):
    prefix = body[:32768].lower()
    html = prefix.lstrip().startswith((b'<!doctype html', b'<html')) or b'<html' in prefix
    if html and any(s in prefix for s in (b'recaptcha', b'hcaptcha', b'cf-chl-', b'checking your browser', b'just a moment')):
        raise FetchError('challenge_page')
    if html and kind != 'html':
        raise FetchError('unexpected_html')
    if not body:
        raise FetchError('empty_response')
    try:
        if kind == 'json':
            def invalid_constant(_):
                raise ValueError('nonfinite')
            data = json.loads(body, parse_constant=invalid_constant)
            if isinstance(data, dict) and (data.get('error') or data.get('errors')):
                raise FetchError('api_error')
            return data
        if kind == 'xml':
            ET.fromstring(body)
        elif kind == 'gzip':
            with gzip.GzipFile(fileobj=io.BytesIO(body)) as gz:
                if len(gz.read(256 * 1024 * 1024 + 1)) > 256 * 1024 * 1024:
                    raise FetchError('file_too_large')
        elif kind == 'zip':
            with zipfile.ZipFile(io.BytesIO(body)) as z:
                if sum(x.file_size for x in z.infolist()) > 256 * 1024 * 1024:
                    raise FetchError('file_too_large')
                if z.testzip():
                    raise FetchError('invalid_document')
        elif kind == 'pdf':
            if not body.startswith(b'%PDF-') or b'%%EOF' not in body[-2048:]:
                raise FetchError('invalid_document')
        elif kind in ('text', 'html'):
            body.decode('utf-8-sig')
    except FetchError:
        raise
    except (ValueError, UnicodeError, ET.ParseError, OSError, EOFError, zipfile.BadZipFile, zlib.error, RuntimeError):
        raise FetchError('invalid_document') from None
    return None




def ssl_context():
    """Prefer an explicit CA bundle: framework Pythons often ship without one."""
    import ssl
    candidates = [os.environ.get('SSL_CERT_FILE')]
    try:
        import certifi
        candidates.append(certifi.where())
    except (ImportError, OSError):
        pass
    candidates += ['/etc/ssl/cert.pem', '/usr/local/etc/openssl/cert.pem',
                   '/opt/homebrew/etc/openssl@3/cert.pem']
    for path in candidates:
        if path and os.path.exists(path):
            try:
                return ssl.create_default_context(cafile=path)
            except (ssl.SSLError, OSError):
                continue
    return ssl.create_default_context()


def fetch_bytes(url, *, kind='json', auth=None, attempts=2, timeout=30, max_bytes=32*1024*1024,
                max_retry_wait=10, expected_size=None, expected_sha256=None):
    u = urllib.parse.urlparse(url)
    if u.scheme != 'https' or not u.hostname or u.username or u.password or u.fragment:
        raise ValueError('credential-free HTTPS URL required')
    if attempts not in (1, 2, 3) or timeout <= 0 or max_bytes <= 0 or not 0 <= max_retry_wait <= 30:
        raise ValueError('invalid retrieval limits')
    headers = {'Accept': 'application/json' if kind == 'json' else '*/*', 'Accept-Encoding': 'identity'}
    if auth:
        headers['Authorization'] = 'Basic ' + base64.b64encode(auth.encode()).decode()
    client = urllib.request.build_opener(NoRedirect, urllib.request.HTTPSHandler(context=ssl_context()))
    for attempt in range(attempts):
        body = bytearray()
        try:
            start = time.monotonic()
            with client.open(urllib.request.Request(url, headers=headers), timeout=timeout) as r:
                status = getattr(r, 'status', 200)
                if status != 200:
                    raise FetchError('incomplete_download' if status == 206 else 'http_error', status)
                rh = getattr(r, 'headers', {})
                declared = rh.get('Content-Length')
                try:
                    declared = int(declared) if declared is not None else None
                    if declared is not None and declared < 0:
                        raise ValueError()
                except (ValueError, TypeError):
                    raise FetchError('invalid_content_length') from None
                if declared is not None and declared > max_bytes:
                    raise FetchError('file_too_large')
                while True:
                    chunk = r.read(min(65536, max_bytes + 1 - len(body)))
                    if isinstance(chunk, str):
                        chunk = chunk.encode('utf-8')  # file-like test doubles
                    if not chunk:
                        break
                    body.extend(chunk)
                    if len(body) > max_bytes:
                        raise FetchError('file_too_large')
                    if time.monotonic() - start > timeout:
                        raise FetchError('incomplete_download')
                if declared is not None and len(body) != declared:
                    raise FetchError('incomplete_download')
                if rh.get('Content-Encoding', 'identity').lower() not in ('identity', ''):
                    raise FetchError('unsupported_content_encoding')
            data = bytes(body)
            if expected_size is not None and len(data) != expected_size:
                raise FetchError('incomplete_download')
            digest = hashlib.sha256(data).hexdigest()
            if expected_sha256 is not None and digest != expected_sha256.lower():
                raise FetchError('checksum_mismatch')
            validate_body(data, kind)
            return data, {'status': 'ok', 'http_status': 200, 'bytes': len(data), 'sha256': digest,
                          'content_length': declared, 'attempts': attempt + 1,
                          'integrity': 'expected_hash_verified' if expected_sha256 else 'transport_and_format_checked',
                          'retrieved_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}
        except urllib.error.HTTPError as e:
            after = retry_seconds(e.headers.get('Retry-After') if e.headers else None)
            code = ('rate_limited' if e.code == 429 else 'access_denied' if e.code in (401,403)
                    else 'redirect_blocked' if 300 <= e.code < 400 else 'not_found' if e.code == 404 else 'http_error')
            err = FetchError(code, e.code, after)
            retry = e.code in (429,500,502,503,504)
            e.close()
        except (http.client.IncompleteRead, http.client.RemoteDisconnected):
            err, retry = FetchError('incomplete_download'), True
        except (urllib.error.URLError, TimeoutError, OSError):
            err, retry = FetchError('incomplete_download' if body else 'network_error'), True
        except FetchError as e:
            err, retry = e, e.code == 'incomplete_download'
        delay = err.retry_after if err.retry_after is not None else attempt + 1
        if not retry or attempt + 1 == attempts or delay > max_retry_wait:
            raise err from None
        time.sleep(delay)
    raise FetchError('network_error')


def get_json(url, auth=None, attempts=2, timeout=30):
    body, _ = fetch_bytes(url, auth=auth, attempts=attempts, timeout=timeout)
    data = json.loads(body)
    if not isinstance(data, dict) or not data:
        raise FetchError('invalid_response_shape')
    return data


def download(url, output, *, kind, **kwargs):
    body, record = fetch_bytes(url, kind=kind, **kwargs)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, delete=False) as f:
            tmp = Path(f.name)
            f.write(body)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, output)
    finally:
        if tmp is not None and tmp.exists():
            tmp.unlink()
    return record


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('url'); p.add_argument('--output', required=True)
    p.add_argument('--format', required=True, choices=['json','xml','pdf','gzip','zip','text','html'])
    p.add_argument('--timeout', type=float, default=30)
    p.add_argument('--max-bytes', type=int, default=32*1024*1024)
    p.add_argument('--expected-size', type=int); p.add_argument('--expected-sha256')
    args = p.parse_args()
    try:
        print(json.dumps(download(args.url,args.output,kind=args.format,timeout=args.timeout,max_bytes=args.max_bytes,expected_size=args.expected_size,
                                  expected_sha256=args.expected_sha256)))
    except FetchError as e:
        print(json.dumps(e.record())); raise SystemExit(2)


if __name__ == '__main__':
    main()
