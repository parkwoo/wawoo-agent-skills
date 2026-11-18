---
description: Design, implement, and audit a web UI change across responsive and accessibility states.
agent: web-designer
replay: safe
---

# UI Delivery

**L1 SSOT**: `docs/plans/ACTIVE.md` (tasks) + `DESIGN.md` (`design-md`) if needed. Update ACTIVE at the exit and pass `python3 scripts/plan_active.py`.

1. Read `docs/plans/ACTIVE.md` and inspect the current UI, design tokens, primary user task, target viewports, and existing states.
1b. **Skill routing**: open `frontend-guides-hub` and load **one** downstream skill at a time (avoid reading the full catalog). Use `modern-web-guidance-bridge` only when native Web APIs / Baseline patterns are needed.
2. Use `web-experience-design` to define hierarchy, content, interaction, desktop/mobile behavior, and non-goals.
3. **Only if images are needed**, generate **just what you need** with `fal-gen` (requires `FAL_KEY`; hero / illustration / background / texture / mobile screens). If unset, proceed with a **placeholder + source**. Save outputs under `docs/.../assets/` and confirm whether they should be committed.
4. Implement the smallest consistent UI change; retain semantic HTML and keyboard behavior.
5. Use `test-engineering`, `accessibility-audit`, and `performance-audit` as applicable.
5b. **Uplift evidence (verify, required)** — Let `<ui-root>` be the changed UI tree; use `<compose-dir>` when compose/images changed. Stamp UTC as `TS` (e.g. `20261118T120000Z`), write JSON under `docs/evidence/skill-uplift/`, and link paths in ACTIVE evidence.

```bash
TS=$(date -u +%Y%m%dT%H%M%SZ)
python3 scripts/skill_uplift_check.py web-design-guidelines --path <ui-root> \
  > docs/evidence/skill-uplift/ui-delivery-web-design-${TS}.json
python3 scripts/skill_uplift_check.py accessibility-audit --path <ui-root> \
  > docs/evidence/skill-uplift/ui-delivery-a11y-${TS}.json
# Only when compose / image tags changed:
python3 scripts/skill_uplift_check.py deployment --path <compose-dir> \
  > docs/evidence/skill-uplift/ui-delivery-deploy-${TS}.json
```

6. Inspect rendered desktop/mobile states. Report evidence and explicitly list unavailable browsers, devices, states, or data.
7. Run `change-readiness` before handoff. Update ACTIVE (evidence = screenshots, audit results, PR). Do not replace brand assets, alter tracking, or publish without approval.

## Privacy / security / context

- Before any external LLM/API call or returning output: `guard_content` (policy gate) → `mask_pii` / `redact_infra` (redact) — see `data-egress-guard`.
- Never echo internal IPs, hosts, URLs, ports, or credentials in errors or logs.
- When context is long or repetitive: `context-compression` (MCP `compress_context`) + `principle-guard-the-context-window`.
- Security/privacy review: `security-review` / `privacy-review` (audit phase).
