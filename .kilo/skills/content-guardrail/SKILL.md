---
name: content-guardrail
description: Deterministic policy-as-data content gate (no model, no network) — checks text against deny terms, named regexes, built-in secret and private-infra detectors, and returns a verdict with violations; optional fail-closed. Use before sending text to an external LLM/API, before returning agent output to a user, or as a release/security gate.
---

# content-guardrail — policy-as-data content gate

Check text against a small JSON policy **before** it leaves the boundary. Pure
Python, deterministic; no model. Complements `data-egress-guard` (which *masks*)
by *deciding* whether the content is allowed to go out at all.

Bundled: [`guard.py`](./guard.py), [`policy.example.json`](./policy.example.json).

## Policy shape

```json
{
  "deny": ["CONFIDENTIAL-INTERNAL", "Project Bluebird"],
  "regex": [{ "name": "ssn", "pattern": "\\b\\d{3}-\\d{2}-\\d{4}\\b" }],
  "secrets": true,
  "infra": true,
  "fail_closed": false
}
```

- `deny` — case-insensitive substring terms (codewords, competitor names).
- `regex` — named patterns (use `ignore_case: true` per entry).
- `secrets` — built-in credential detectors (private key, JWT, GitHub/AWS/API token, Bearer).
- `infra` — private IPs and internal hostnames (`*.local/.internal/.lan/.corp`).
- `fail_closed` — a bad regex makes the verdict **unsafe** (default: fail-open, skip and continue).

Returns `{ "safe": bool, "violations": [{rule, kind, match}], "policy_errors": [...], "fail_closed": bool }`.

## Usage

MCP tool (Kilo / Cursor / OpenCode):

```json
{ "text": "...", "policy_path": ".kilo/skills/content-guardrail/policy.example.json" }
```
or pass `policy` inline. Returns the verdict; `safe:false` means block or redact first.

CLI / library:

```bash
python3 guard.py --input text.txt --policy policy.example.json --json
echo "..." | python3 guard.py --policy policy.example.json
python3 guard.py --selftest
```
```python
from guard import guard
res = guard(text, "policy.example.json")   # or a dict
```

## When to use

- Input guard before an external call (block/deny) and output guard before returning to a user.
- A release/security checklist step (no secrets or internal infra in artifacts/logs).
- Pair with `data-egress-guard`: **guard** (allow/block) → **mask** (redact) → send.

## Limits

- Rule/pattern based only (no semantic moderation, no model). Keep policies short and reviewable.
- `deny` is substring matching (fast, predictable); use `regex` for structured data.
