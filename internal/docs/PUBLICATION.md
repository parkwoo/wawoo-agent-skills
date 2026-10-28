# Publication scope (external) and internal assets

> Japanese version: [PUBLICATION.ja.md](PUBLICATION.ja.md)

## External (git-managed, included in clones)

Consumer-facing kit assets:

- `README.md`, `AGENTS.md`, `docs/USAGE.md`, `docs/INTENT-ROUTING.md`, `docs/VERSIONING.md`, `SECURITY.md`, `CHANGELOG.md` (**Japanese project record**), `VERSION`, `docs/memory/TEMPLATE.md` · `MEMORY-TOOLS.md` · `INDEX.example.md`, `docs/plans/README.md` · `*.example.md` — explanatory docs also have a `*.ja.md` counterpart
- `.kilo/` (skills / agents / commands), `.cursor/rules`, `mcp/`
- `scripts/validate_assets.py`, `scripts/gen_capabilities.py`
- `.github/workflows/` (asset / MCP smoke)
- `LICENSE`, `LICENSES/`, `.kilo/skills/ATTRIBUTION.md`

## Internal (outside git)

For maintainers, audits, and measurement. **Not included in public clones.**

| Location (local) | Content |
|---|---|
| `internal/docs/MAINTAINER.md` | Maintainer runbook |
| `internal/docs/audit/` | Audit records, E2E procedure |
| `internal/docs/design/` | **Research / analysis notes** (e.g. tool comparisons, absorption analysis, `*-AUDIT.md`) |
| `internal/docs/plans/` | **Development-process materials** (`RETRO-*`, `self-improve-*`, E2E depth table) |
| `internal/docs/blog/` | **Publishing / series drafts** (Qiita / Kindle outlines) |
| `docs/plans/ACTIVE.md` (local only) | **The kit's own progress SSOT** (public template: `docs/plans/ACTIVE.example.md`) |
| `docs/memory/*.md` (local only) | **The kit's own memory** (public templates: `TEMPLATE.md`, `MEMORY-TOOLS.md`, `INDEX.example.md`) |
| `internal/scripts/e2e/` | Smoke / CLI measurement scripts |
| `internal/docker/e2e/` | Docker measurement |
| `internal/scripts/audit_*.py` | Audit generation |

### Internal dev materials (not published)

The following are **maintainer development-process materials** and are not included in public clones (keep them under `internal/`).

- Research / analysis notes (tool comparisons, absorption analysis, etc.)
- Audit records (`*-AUDIT.md`, etc.)
- Retros and self-improvement (`RETRO-*.md`, `self-improve-*.md`)
- E2E run logs (`docs/plans/evidence/`, gitignored) and the E2E depth table
- Publishing / series drafts (`docs/blog/` equivalent)

> **Migrated (2026-10-28)**: the following were moved into `internal/` and removed from the public tree (note: they remain in history).
> - `docs/design/INTENT-RECEIVER-AUDIT.md` → `internal/docs/design/`
> - `docs/plans/RETRO-20261028-log-optimization.md`, `self-improve-20261028-log-optimization.md`, `E2E-WORKFLOW-COVERAGE.md` → `internal/docs/plans/`
> - `docs/blog/*` → `internal/docs/blog/`
>
> **Decision to keep public: reverted (2026-10-28)**. The **real files** of `docs/plans/ACTIVE.md` (the kit's own progress) and `docs/memory/` are **not published**. Public clones carry only the templates (`ACTIVE.example.md`, `INDEX.example.md`, `TEMPLATE.md`, `MEMORY-TOOLS.md`); each project creates its own real files. CI (`scripts/e2e_flows.py`) does not depend on the real files (it uses templates / isolated memory).
>
> **Migrated (2026-10-29)**: design/process docs were moved out of the public tree (EN+JA) to shrink the public reading surface to `README.md`, `docs/USAGE.md`, `docs/INTENT-ROUTING.md`. Moved: `docs/METHODOLOGY.md`, `docs/PROCESS-PHILOSOPHY.md`, `docs/PUBLICATION.md`, `docs/README.md`, `docs/design/INTENT-RECEIVER.md` → `internal/docs/design/` and `internal/docs/`. Public references were retargeted to `AGENTS.md` §3 / `mcp/README.md`; `scripts/e2e_flows.py` skips the METHODOLOGY checks when `internal/` is absent.

> **Source-of-truth split (2026-10-29)**: **this repo (`wawoo-skills-internal`, private) is the source of truth** — it tracks the kit *and* `internal/`. The **public** kit is `parkwoo/wawoo-skills`, **generated** by `.github/workflows/publish-public.yml` (tag-triggered) from `.publish-allowlist`. Publishing uses an SSH deploy key (secret `PUBLIC_DEPLOY_KEY`). The public repo runs the heavy CI (free); this repo runs only the publish job (tags only, minimal minutes). Local guard: this clone's `origin` push URL is disabled (`DISABLED_DO_NOT_PUSH`) so internal content cannot be pushed to the public repo.

Initial setup:

```bash
./scripts/bootstrap-internal.sh
./internal/scripts/e2e/smoke.sh
```

Templates are **`internal.example/`** only (git-managed). The working copy is `internal/`.

## Secrets

`.env` remains gitignored (`.env.example` lists key names only).

## Memory (`docs/memory/`)

| Usage | Recommended |
|----------|------|
| **This kit** (wawoo-skills) | The real files (`INDEX.md`, `kit.md`, `general.md`, `deployment.md`, etc.) are **non-public** (`.gitignore`). Only `TEMPLATE.md`, `MEMORY-TOOLS.md`, `INDEX.example.md` are published |
| **Consuming projects** (copy the kit to build another product) | Create `INDEX.md` from `INDEX.example.md`; **commit** decisions shared by the team. For personal notes only, add `docs/memory/local/` to `.gitignore` (`local/` is optional, not bundled) |
| **Secrets** | Do not write to memory (`validate_assets.py` pattern-checks) |

Tool priority: `docs/memory/MEMORY-TOOLS.md`.
