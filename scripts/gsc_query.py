#!/usr/bin/env python3
import argparse
import base64
import json
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path


SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"
API_BASE = "https://searchconsole.googleapis.com/webmasters/v3"


def resolve_cred_path() -> Path:
    candidates = [
        Path.home() / ".openclaw" / "credentials" / "gsc" / "service-account.json",
        Path("/opt/openclaw/state/credentials/gsc/service-account.json"),
        Path(__file__).with_name("service-account.json"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def sign_rs256(data: bytes, private_key: str) -> bytes:
    with tempfile.NamedTemporaryFile("w", delete=True) as tmp:
        tmp.write(private_key)
        tmp.flush()
        proc = subprocess.run(
            ["openssl", "dgst", "-sha256", "-sign", tmp.name],
            input=data,
            capture_output=True,
            check=True,
        )
    return proc.stdout


def get_access_token(cred_path: Path) -> str:
    creds = json.loads(cred_path.read_text())
    now = int(time.time())
    header = {"alg": "RS256", "typ": "JWT"}
    claim = {
        "iss": creds["client_email"],
        "scope": SCOPE,
        "aud": creds["token_uri"],
        "iat": now,
        "exp": now + 3600,
    }
    header_json = json.dumps(header, separators=(",", ":")).encode()
    claim_json = json.dumps(claim, separators=(",", ":")).encode()
    signing_input = f"{b64url(header_json)}.{b64url(claim_json)}".encode()
    signature = b64url(sign_rs256(signing_input, creds["private_key"]))
    assertion = signing_input.decode() + "." + signature
    body = urllib.parse.urlencode(
        {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": assertion,
        }
    ).encode()
    req = urllib.request.Request(creds["token_uri"], data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode())
    return payload["access_token"]


def api_request(path: str, token: str, method: str = "GET", payload=None):
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
    req = urllib.request.Request(API_BASE + path, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def cmd_list_sites(token: str) -> None:
    print(json.dumps(api_request("/sites", token), ensure_ascii=False, indent=2))


def cmd_query(
    token: str,
    site: str,
    days: int,
    dimensions: list[str],
    limit: int,
    search_type: str,
) -> None:
    end_date = time.strftime("%Y-%m-%d", time.gmtime())
    start_ts = time.time() - days * 86400
    start_date = time.strftime("%Y-%m-%d", time.gmtime(start_ts))
    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": dimensions,
        "rowLimit": limit,
        "searchType": search_type,
    }
    encoded_site = urllib.parse.quote(site, safe="")
    path = f"/sites/{encoded_site}/searchAnalytics/query"
    print(json.dumps(api_request(path, token, method="POST", payload=payload), ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list-sites")
    query = sub.add_parser("query")
    query.add_argument("--site", required=True)
    query.add_argument("--days", type=int, default=28)
    query.add_argument("--dimensions", default="query")
    query.add_argument("--limit", type=int, default=20)
    query.add_argument("--search-type", default="web")
    args = parser.parse_args()

    token = get_access_token(resolve_cred_path())
    if args.cmd == "list-sites":
        cmd_list_sites(token)
    elif args.cmd == "query":
        dims = [part.strip() for part in args.dimensions.split(",") if part.strip()]
        cmd_query(token, args.site, args.days, dims or ["query"], args.limit, args.search_type)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        sys.exit(1)
