---
description: Legal / privacy / security gate (compliance-legal → privacy-review → security-review → release-readiness)
agent: compliance-reviewer
replay: safe
---

# Compliance Review (legal / privacy / security)

> **A human makes the legal call.** This workflow assembles **evidence and checklists** and requires **human approval**.

2. **`compliance-legal`**:
   - OSS licenses (MIT/Apache-2.0 LICENSE and NOTICE attribution) and an **SBOM**.
   - Checklists for ToS, privacy policy, DPA, and AI usage policy.
3. **`privacy-review`**: PII flows, minimization, retention, masking, cross-border.
4. **`security-review`**: boundaries (auth, SSRF, secrets, tenant isolation).
5. **`release-readiness`**: version, legal files, CHANGELOG, rollback.
6. Output: **applicable / not applicable / needs confirmation**, evidence (path/version/source), residual risk, and **required human approval**.
7. Do **not** publish, contract, change terms, or ship to production **without approval**.

## Platform overlay (co-taro-bz v2 — BR-009)

When billing **gateway token arbitrage** (DEC-15):

1. Confirm **Logical Input Tokens** (baseline) in ToS/customer docs (`TARO-PLATFORM-REQUIREMENTS-v2` BR-009).
2. Confirm disclosure of **`GET /v1/savings`** and response `platform.tokens_saved` (BR-008).
3. No silent SSE `usage` rewrite without `platform` metadata (BR-008).

See `@.kilo/commands/platform-ops.md` §4.

## Known cautions

- This project uses MIT/Apache-2.0 assets (`.kilo/skills/ATTRIBUTION.md`). **Marketplace "business" items come from a third-party source with unverified licenses.**
- Design PII stance: `docs/design/60-SECURITY-OPS.md` §7.4 (do not store bodies by default).
