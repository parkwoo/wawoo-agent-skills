# Skill Uplift Pilot (lightweight MWG-style loop)

## One-liner

Track whether skills improve agent output via **expectations.md**, **static checks**, and optional guided/unguided notes; **prune** items models already satisfy.

## Roadmap (shipped)

| Phase | Scope | Artifacts |
|-------|--------|-----------|
| P0 | MWG bridge | `modern-web-guidance-bridge`, `scripts/mwg_bridge.py`, MCP `mwg_*` |
| P1 | Expectations pilot | `web-design-guidelines/expectations.md`, `scripts/skill_uplift_check.py` |
| P1.1 | a11y + deploy pilot | `accessibility-audit` / `deployment` `expectations.md`, checker extension, `ui-delivery` step **5b** evidence paths |
| P1b | Playwright A/B | `internal/skill-uplift-ab/`, `scripts/skill_uplift_ab.py` |
| P1.5 | Frontend hub | `frontend-guides-hub` |
| P2 | Uplift/prune rules | This doc + `USAGE.md` §6.2 |
| P3 | Legacy scan | `legacy-web-scan`, `scripts/legacy_web_scan.py` + MWG CLI |

## §6.2 Uplift / prune rules

1. **~90% pass without the skill** → shorten entry `SKILL.md` or move detail to `references/`.
2. **Low uplift** → fix the **guide/skill**, not the workflow.
3. **High uplift** → extend `expectations.md` and `skill_uplift_check.py`.
4. Store runs under `docs/evidence/skill-uplift/` (no secrets).

## P1 / P1.1 examples

```bash
TS=$(date -u +%Y%m%dT%H%M%SZ)
python3 scripts/skill_uplift_check.py web-design-guidelines --path /path/to/ui-root \
  > docs/evidence/skill-uplift/web-design-guidelines-${TS}.json
python3 scripts/skill_uplift_check.py accessibility-audit --path /path/to/ui-root \
  > docs/evidence/skill-uplift/accessibility-audit-${TS}.json
python3 scripts/skill_uplift_check.py deployment --path /path/to/compose-dir \
  > docs/evidence/skill-uplift/deployment-${TS}.json
```

**P1.1 static rules (summary)**

| skill | rule ids (excerpt) |
|-------|---------------------|
| `accessibility-audit` | `a11y-html-lang`, `a11y-page-h1`, `a11y-input-label`, `a11y-button-type`, `a11y-skip-link` |
| `deployment` | `deploy-no-latest-tag`, `deploy-plain-secret-env`, `deploy-missing-healthcheck` |

Wiring: `.kilo/commands/ui-delivery.md` step **5b**; `.kilo/agents/web-designer.md` “Skill routing” (3 lines).

## Playwright A/B (optional calibration)

```bash
cd internal/skill-uplift-ab && npm install && npx playwright install chromium
cd ../..
python3 scripts/skill_uplift_ab.py --out docs/evidence/skill-uplift/ab-accessible-dialog.json
```

## MCP (P0)

Tools: `mwg_search`, `mwg_retrieve`, `mwg_legacy_scan`. Disable with `WAWOO_MWG_DISABLE=1`.

Rule SSOT: `scripts/uplift_pilot.py` (`UPLIFT_PILOT_SKILLS`, `ACTIVE_STATIC_RULES`) — must match `[rule-id]` in `expectations.md`.

See `docs/USAGE.md` §6.1–6.2 and [modern-web-guidance-src](https://github.com/GoogleChrome/modern-web-guidance-src).