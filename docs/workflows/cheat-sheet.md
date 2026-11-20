# Workflow cheat sheet

Workflow files: `.kilo/commands/<name>.md`. Start from MCP **`interpret_intent`** when unsure.

| You want to… | Start with |
|--------------|------------|
| Small fix / one feature | `delivery-lite` |
| Full feature with gates | `feature-delivery` |
| UI change | `ui-delivery` |
| Research → decision | `research` |
| Bug / quality self-check | `self-review` |
| Incident | `incident-response` |
| Pre-release | `release-review` |
| Legal / security read-only audit | `compliance-review` |
| Docs / article | `content-build` or `writing` |
| Status report | `status-report` |

## Default entry

Agent **`wawoo-auto`** and MCP **`interpret_intent`** route into one of **20** workflows.

## In Cursor (no slash)

Open `@.kilo/commands/delivery-lite.md` (or the workflow name) and follow steps; use MCP `skill_get` for each phase skill.

Catalog: `.kilo/CAPABILITIES.md` (generated — do not hand-edit).

More: [INTENT-ROUTING](../INTENT-ROUTING.md) · [GUIDES](../GUIDES.md)