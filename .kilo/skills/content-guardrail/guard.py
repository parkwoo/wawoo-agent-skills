#!/usr/bin/env python3
"""content-guardrail: policy-as-data content gate (deterministic, no model).

Checks text against a JSON policy before it is sent outbound (or before output is
returned). Returns a verdict plus the violations with short snippets.

Policy shape:
  {
    "deny": ["competitor name", "internal codename"],     # case-insensitive substring
    "regex": [{"name": "ssn", "pattern": "\\b\\d{3}-\\d{2}-\\d{4}\\b"}],
    "secrets": true,        # built-in credential patterns
    "infra": true,          # private IPs / internal hostnames
    "fail_closed": true     # a policy error => unsafe (default: fail-open)
  }

CLI:
  python3 guard.py --input text.txt --policy policy.example.json
  echo "..." | python3 guard.py --policy policy.example.json --json
  python3 guard.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_SECRETS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    "github_token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "aws_key": re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    "api_key": re.compile(r"\b(?:sk-[A-Za-z0-9]{16,}|AIza[0-9A-Za-z_-]{20,})\b"),
    "bearer": re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{12,}"),
}
_INTERNAL_HOST = re.compile(r"\b(?:[a-z0-9-]+\.)+(?:local|internal|lan|corp|intranet|localdomain)\b", re.I)
_IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def _private_ipv4(value: str) -> bool:
    try:
        a, b, _, _ = (int(x) for x in value.split("."))
    except ValueError:
        return False
    return a in (0, 10, 127) or (a == 172 and 16 <= b <= 31) or (a == 192 and b == 168) or (a == 169 and b == 254)


def _snippet(text: str, start: int, end: int, pad: int = 24) -> str:
    lo = max(0, start - pad)
    hi = min(len(text), end + pad)
    return text[lo:hi].replace("\n", " ")


def load_policy(source: dict | str | Path | None) -> dict:
    if source is None:
        return {}
    if isinstance(source, dict):
        return source
    return json.loads(Path(source).read_text(encoding="utf-8"))


def guard(text: str, policy: dict | str | Path | None = None) -> dict:
    policy = load_policy(policy)
    violations: list[dict] = []
    errors: list[str] = []
    lowered = text.lower()

    for term in policy.get("deny") or []:
        term = str(term)
        if not term:
            continue
        idx = lowered.find(term.lower())
        if idx >= 0:
            violations.append({"rule": "deny", "kind": "term", "match": _snippet(text, idx, idx + len(term))})

    for spec in policy.get("regex") or []:
        if isinstance(spec, str):
            spec = {"name": spec, "pattern": spec}
        name = str(spec.get("name") or "regex")
        try:
            m = re.search(str(spec.get("pattern", "")), text, re.IGNORECASE if spec.get("ignore_case") else 0)
        except re.error as exc:
            errors.append(f"{name}: {exc}")
            continue
        if m:
            violations.append({"rule": name, "kind": "regex", "match": _snippet(text, m.start(), m.end())})

    if policy.get("secrets"):
        for name, rx in _SECRETS.items():
            m = rx.search(text)
            if m:
                violations.append({"rule": name, "kind": "secret", "match": _snippet(text, m.start(), m.end())})

    if policy.get("infra"):
        for m in _IPV4.finditer(text):
            if _private_ipv4(m.group(0)):
                violations.append({"rule": "private_ip", "kind": "infra", "match": m.group(0)})
                break
        hm = _INTERNAL_HOST.search(text)
        if hm:
            violations.append({"rule": "internal_host", "kind": "infra", "match": hm.group(0)})

    fail_closed = bool(policy.get("fail_closed"))
    safe = not violations and not (fail_closed and errors)
    return {"safe": safe, "violations": violations, "policy_errors": errors, "fail_closed": fail_closed}


def selftest() -> int:
    pol = {"deny": ["AcmeCorp"], "regex": [{"name": "ssn", "pattern": r"\b\d{3}-\d{2}-\d{4}\b"}], "secrets": True, "infra": True, "fail_closed": True}
    assert guard("please mention AcmeCorp", pol)["violations"], "deny term not caught"
    assert guard("id 123-45-6789", pol)["violations"], "regex not caught"
    assert guard("key AKIAABCDEFGHIJKLMNOP", pol)["violations"], "secret not caught"
    assert guard("db at 10.2.3.4", pol)["violations"], "private ip not caught"
    assert guard("all clear here", pol)["safe"], "false positive"
    # fail-closed policy error
    bad = {"regex": [{"name": "bad", "pattern": "("}], "fail_closed": True}
    assert guard("x", bad)["safe"] is False
    open_pol = {"regex": [{"name": "bad", "pattern": "("}], "fail_closed": False}
    assert guard("x", open_pol)["safe"] is True
    print("selftest OK")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Policy-as-data content gate (no model).")
    ap.add_argument("--input", help="text file (default: stdin)")
    ap.add_argument("--policy", help="policy JSON file")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    text = Path(args.input).read_text(encoding="utf-8") if args.input else sys.stdin.read()
    res = guard(text, args.policy)
    print(json.dumps(res, ensure_ascii=False, indent=2 if args.json else None))
    return 0 if res["safe"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
