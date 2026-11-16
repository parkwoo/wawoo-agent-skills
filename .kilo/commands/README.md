# Workflows (commands) — owner of the process

This project is **workflow-driven**. Commands own the process and **embed Skills For Real Engineers thinking and solutions into each step**. Because agents may skip skills, the workflow calls them **explicitly**.

## List (12)

**Source of truth**: the "main skill chain" below is a summary. The procedure SSOT is each `commands/<name>.md` body.

| command | purpose | main skill chain |
|---|---|---|
| `/delivery-lite` | **L1 code** — lightweight delivery via the ACTIVE.md state machine | `plan-md` (optional) → `implement` → `engineering-quality` → verify |
| `/ui-delivery` | UI delivery (ACTIVE + DESIGN) | `web-experience-design` → implement → audit |
| `/feature-delivery` | Beyond L1, gate-heavy — discovery→design→implement→test→review | the body's skill chain (body wins over this table) |
| `/design-review` | UI design review | `design-review` → `web-design-guidelines` → `accessibility-audit` |
| `/research` | Research → decision | `research` → `product-discovery` → `to-spec`/`plan-md` |
| `/compliance-review` | Legal / privacy / security gate | `compliance-legal` → `privacy-review` → `security-review` → `release-readiness` |
| `/release-review` | Pre-release check | `release-readiness` → `compliance-legal`/`privacy-review` → `security-review` → `documentation-localization` |
| `/incident-response` | Incident response | `incident-debugging` → `engineering-quality` → `retro` |
| `/sprint-plan` | Sprint planning | `wayfinder` → `to-tickets` → priority/estimate/capacity → `plan-md` |
| `/status-report` | Progress / status report | `triage`/`to-tickets` → progress/risk → `plan-md` |
| `/self-review` | Self-correction | `code-review` → `code-skeptic` → `diagnosing-bugs`/`tdd` → fix → verify → `memory` |
| `/self-improve` | Self-improvement (PDCA) | `retro` → `pdca-cycle` → `self-review`/`code-simplifier` → `plan-md` → `memory` |

## Gates (required)

- **Approval**: stop and get approval for destructive changes, production, deletions, external transmission, and contracts/terms.
- **Evidence**: commands run, results, screenshots/diff. Distinguish measured from unverified.
- **Observed failure**: follow the Skills For Real Engineers principle — base work on failures that actually happened, not inference.
- **Legal**: humans make legal calls (`compliance-legal` gathers evidence and checklists only).
