# Skills (95)

Agent Skill format (`<name>/SKILL.md`). Shared by Kilo / Cursor. **Origins and licenses: [`ATTRIBUTION.md`](./ATTRIBUTION.md)**.

## Breakdown

| Collection | Count | License | Main use |
|---|---|---|---|
| **Skills For Real Engineers** | 25 | MIT | Development process (`to-spec` → `to-tickets` → `implement` / `implement-spec` → `tdd` → `code-review` → `retro`, `ask-matt`) |
| **Kilo built-in** | 16 | MIT (frontmatter) | Quality, design, safety (`architecture-decision`, `engineering-quality`, `test-engineering`, `security-review`, ...) |
| **OpenDesign** | 10 | Apache-2.0 | **Web/app design** (`design-brief`, `reference-design-contract`, `design-md`, `frontend-design`, `web-design-guidelines`, `design-review`, ...) |
| **This repository** | 16 | MIT | `deployment`, `compliance-legal`, `privacy-review`, `changelog`, `memory`, `slides`, `screenshots-marketing`, `plan-md`, `language-policy`, `publication-boundary`, `science-writing`, `viral-hooks`, `fal-gen`, `context-compression`, `data-egress-guard`, `content-guardrail` |
| **pstack** (Lauren Tan / Poteto) | 28 | MIT | `principle-*` engineering-principle skills (design, debugging, verification, context, concurrency) |

## By category

- **Development**: Skills For Real Engineers (`code-review`, `tdd`, `diagnosing-bugs`, `domain-modeling`, `prototype`, ...)
- **Design / UI**: `web-experience-design`, `accessibility-audit`, `design-brief`, `reference-design-contract`, `design-md`, `frontend-design`, `web-design-guidelines`, `design-review`
- **Market / business**: `marketing-psychology`, `brand-guidelines`, `slides`
- **Research**: `research`, `research-decision-room`, `product-discovery`
- **Security / legal**: `security-review`, `compliance-legal`, `privacy-review`, `release-readiness`, `data-egress-guard`, `content-guardrail`
- **Operations**: `deployment`, `incident-debugging`, `dependency-upgrade`, `database-change-safety`, `pdca-cycle`
- **Memory / versioning**: `memory`, `changelog`
- **Context / RAG**: `context-compression` (offline, deterministic context cleaning)
- **Engineering principles**: `principle-*` (24) — apply-before rules for design, debugging, verification, context, and concurrency
- **Verification / audit trail**: `blast-radius`, `create-verification-skill`, `maintain-verification-skill`, `show-me-your-work`
- **Planning**: `plan-md`

## Representative workflows

- Development: `setup-matt-pocock-skills` → `to-spec` → `to-tickets` → `implement` / `implement-spec` (`tdd`) → `code-review` → `retro`
- Design: `design-brief` → `reference-design-contract` → `frontend-design` → `design-review` → `web-design-guidelines` → `accessibility-audit`
- Market: `research` → `research-decision-room` → `product-discovery` → `marketing-psychology` → `plan-md`
- Legal / security: `compliance-legal` → `privacy-review` → `security-review` → `release-readiness`

## Cautions

- **Do not harvest en masse** (read only what you need).
- **Excluded from publication**: Marketplace business (3, `NOASSERTION`) / `fal-gen` (license unclear).
- `imagegen-frontend-mobile` is **prompt guidance** only (no image-generation tool is bundled).
