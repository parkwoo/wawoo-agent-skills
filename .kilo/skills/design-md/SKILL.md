---
name: design-md
description: |
  Create and maintain a DESIGN.md — a plain-text design-system document (Google Stitch format) that design and coding agents read to generate consistent UI. Covers theme, color roles, typography, components, layout, depth, do/don't, responsive, and an agent prompt guide.
triggers:
  - "design.md"
  - "design doc"
  - "design tokens doc"
  - "visual rules doc"
  - "design system document"
od:
  mode: design-system
  category: design-systems
  upstream: "https://github.com/google-labs-code/skills"
---

# design-md — DESIGN.md (design-system document)

> Format: **Google Stitch DESIGN.md** (<https://stitch.withgoogle.com/docs/design-md/specification>). Curated from Google Labs.

`DESIGN.md` does for **look & feel** what `AGENTS.md` does for **how to build**: one Markdown file in the project root that design/coding agents (Stitch, Claude, Cursor, Kilo, OpenCode) read to keep UI consistent. No JSON, no special tooling.

## When to use

- Starting a UI/product with a real visual direction.
- Onboarding an agent to an existing design system.
- Turning taste/references into a durable spec (pair with `reference-design-contract` for evidence + implementation handoff).

## Format (9 sections)

1. **Visual Theme & Atmosphere** — mood, density, design philosophy.
2. **Color Palette & Roles** — semantic name + hex + functional role.
3. **Typography** — families + full hierarchy table (size/weight/line-height).
4. **Components** — buttons, cards, inputs, nav, with states.
5. **Layout & Spacing** — spacing scale, grid, whitespace rules.
6. **Depth & Elevation** — surface hierarchy, shadows.
7. **Do's and Don'ts** — guardrails and anti-patterns.
8. **Responsive Behavior** — breakpoints, touch targets, collapse strategy.
9. **Agent Prompt Guide** — quick color/type reference + ready-to-use prompts.

## Workflow

1. Gather evidence (existing `DESIGN.md`, brand docs, screenshots, URLs). Do not invent brand facts.
2. Pick **one** coherent stance; don't mix unrelated moodboards.
3. Fill `templates/DESIGN.template.md` — all 9 sections, **concrete values > adjectives**.
4. Place at the project root as `DESIGN.md`; keep it in version control.
5. Maintain: update on token/component changes; keep colors as hex + role.

## Tips

- Prefer constraints ("one warm accent; no purple/blue glow") over "premium"/"modern".
- Every color, type, and spacing value must be concrete and reusable.
- **Do not copy a brand's proprietary assets, logo, or exact layout** — capture controllable qualities only (see `reference-design-contract`).
- Keep it short enough to fit context; long detail can live in `references/`.

## References

- `references/stitch-format.md` — section-by-section notes + official links.
- `templates/DESIGN.template.md` — 9-section skeleton.
- Pair: `reference-design-contract` (evidence → DESIGN.md + handoff), `design-review`, `web-design-guidelines`, `accessibility-audit`.
