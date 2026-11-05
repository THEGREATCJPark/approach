#!/usr/bin/env python3
"""PREP-only public link checks. Requires explicit --online; never accesses models or uploads."""
import argparse
import datetime
import ipaddress
import json
import re
import socket
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def public_url(url):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in ['http', 'https'] or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('only credential-free HTTP(S) URLs')
    addresses = socket.getaddrinfo(parsed.hostname, parsed.port or (443 if parsed.scheme == 'https' else 80))
    if any(not ipaddress.ip_address(info[4][0]).is_global for info in addresses):
        raise ValueError('private, loopback or reserved address blocked')


class PublicRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        public_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def check(url, timeout=12):
    result = {'url': url, 'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        public_url(url)
        request = urllib.request.Request(url, headers={'User-Agent': 'approach-reference-check/1.0'}, method='GET')
        with urllib.request.build_opener(PublicRedirect()).open(request, timeout=timeout) as response:
            result.update(status='reachable', http_status=response.status, final_url=response.url, redirected=response.url != url)
            response.read(1024)  # Existence check only, not a document/licence content audit.
    except urllib.error.HTTPError as exc:
        status = 'missing' if exc.code in [404, 410] else 'rate_limited' if exc.code == 429 else 'access_restricted' if exc.code in [401, 403] else 'http_error'
        result.update(status=status, http_status=exc.code)
    except (TimeoutError, socket.timeout):
        result.update(status='timeout')
    except socket.gaierror as exc:
        result.update(status='local_dns_unavailable', detail=str(exc), limitation='No HTTP request completed; this does not establish whether the URL exists.')
    except (urllib.error.URLError, OSError) as exc:
        result.update(status='network_error', detail=str(exc))
    except ValueError as exc:
        result.update(status='blocked_url', detail=str(exc))
    return result


def discover(root):
    urls = set()
    for path in list(root.rglob('*.md')) + list((root / 'catalog').glob('*.json')):
        if '.git' in path.parts:
            continue
        for url in re.findall(r'https?://[^\s<>"\x27`)]+', path.read_text(encoding='utf-8')):
            urls.add(url.rstrip(').,;]'))
    return sorted(urls)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('urls', nargs='*', help='explicit public URLs; otherwise discover repository references')
    parser.add_argument('--online', action='store_true', help='explicit PREP permission to send GET requests')
    parser.add_argument('--timeout', type=float, default=12)
    args = parser.parse_args()
    urls = args.urls or discover(ROOT)
    if not args.online:
        print(json.dumps({'status': 'not_run', 'reason': 'Use --online only in permitted preparation environment.', 'urls': urls}, ensure_ascii=False, indent=2))
        return
    results = [check(url, args.timeout) for url in urls]
    print(json.dumps({'results': results, 'scope': 'Reachability only. Licence and content require separate inspection.'}, ensure_ascii=False, indent=2))
    raise SystemExit(any(r['status'] != 'reachable' for r in results))

if __name__ == '__main__':
    main()
