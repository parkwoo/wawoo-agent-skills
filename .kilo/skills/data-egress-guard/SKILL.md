---
name: data-egress-guard
description: Deterministically mask PII and secrets before sending text to an external LLM/API (no model, no network) — replaces spans with numbered placeholders and returns a reversible mapping, with locale rules and a fail-closed default. Use when user or private data leaves the boundary, when redacting logs/errors, or as an egress guard before external calls.
---

# data-egress-guard — mask PII/secrets at the boundary

Redact personally identifiable information and credentials **before** text leaves
your boundary (external LLM, API, log sink) with pure Python. Deterministic and
offline; no model.

The reference implementation is bundled: [`mask_pii.py`](./mask_pii.py).

## What it does

- Detects spans (email, phone, URL, IP, MAC, credit card, IBAN, JWT, AWS/GitHub/
  API tokens, `Bearer`, PEM private keys, JP MyNumber / corporate number / phone /
  postal) and replaces each with a **numbered placeholder** like `{{EMAIL_1}}`.
- Returns a reversible `mapping` (`placeholder -> original`); `unmask` restores a
  provider response so the caller still sees the real values.
- **Fail-closed by default**: mask on format match even if a checksum fails (a
  missed mask leaks; an extra mask only over-redacts). `--strict` requires
  checksums (Luhn / IBAN mod-97 / JP checks) to cut false positives.
- Same original → same placeholder (dedup), so repeated values stay consistent.

## Usage

MCP tool (Kilo / Cursor / OpenCode):

```json
{ "text": "mail alice@example.com, card 4111 1111 1111 1111", "locale": "generic,jp" }
```
Returns `{ "text": "mail {{EMAIL_1}}, card {{CARD_1}}", "mapping": {...}, "counts": {...} }`.
Pass `{ "texts": [...] }` for batches, and `{ "unmask": true, "mapping": {...} }` to restore.

CLI / library:

```bash
python3 mask_pii.py --input text.txt --locale generic,jp --json
echo "a@b.com 4111111111111111" | python3 mask_pii.py
python3 mask_pii.py --selftest
```
```python
from mask_pii import PiiMasker
m = PiiMasker(locales=["generic", "jp"])
res = m.mask(text)                 # {"text","mapping","counts"}
m.unmask(res["text"], res["mapping"])
```

## When to use

- Before an external LLM/API call with user data (redact, call, then rehydrate).
- Redacting logs, error messages, and telemetry (also strip internal IPs/URLs/hosts).
- A last gate in a RAG/agent pipeline that sends retrieved text outbound.

Do **not** treat this as a compliance certification; it is a deterministic
defense-in-depth filter. Context-dependent PII (names in free prose) is not caught
by regex — add rules or a human/NER step if you need that.

## Tuning

| Option | Meaning |
|---|---|
| `locale` | `generic` (default) and/or `jp` (adds JP identifiers) |
| `rules` | allow-list of rule names/placeholders (e.g. `EMAIL,CARD,AWS_KEY`) |
| `strict` | require checksums; invalid formats are left unmasked (fewer false positives) |

## Limits

- Regex/checksum only; not a semantic NER model (the kit stays model-free).
- Placeholders can shift token counts slightly; keep the mapping in-process only
  when possible (it contains the original sensitive values).
