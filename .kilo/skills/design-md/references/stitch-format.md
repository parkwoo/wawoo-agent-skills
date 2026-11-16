# DESIGN.md — Google Stitch format (notes)

`DESIGN.md` is a plain-text design-system document introduced by **Google Stitch**. Agents read it to generate UI that matches a project's visual language. It is to design what `AGENTS.md` is to engineering: one Markdown file in the repo root, no schema, no tooling.

Source: [Stitch DESIGN.md spec](https://stitch.withgoogle.com/docs/design-md/specification) · [overview](https://stitch.withgoogle.com/docs/design-md/overview) · [Google Labs announcement](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/).

> We absorb the **format/spec only**. Do **not** redistribute `DESIGN.md` files extracted from third-party brand websites (trademark / trade-dress / uncertain license). Generate original documents for the project's own brand.

## Sections (what each must contain)

1. **Visual Theme & Atmosphere** — mood words, density, reference feelings; what it is *not*.
2. **Color Palette & Roles** — table: role (surface/text/accent/state) + hex; contrast notes.
3. **Typography** — families, fallbacks, type scale table (size/weight/line-height/letter-spacing).
4. **Components** — buttons/cards/inputs/nav/tables; default + hover + focus + disabled.
5. **Layout & Spacing** — spacing scale (e.g. 4/8/12/16/24/32), grid, max-width, whitespace intent.
6. **Depth & Elevation** — surface layers and shadow/elevation tokens.
7. **Do's and Don'ts** — non-negotiable guardrails and anti-patterns.
8. **Responsive Behavior** — breakpoints, touch target minimums, collapse/stack rules.
9. **Agent Prompt Guide** — quick color/type reference and copy-paste prompts for agents.

## Rules of thumb

- Concrete over abstract: hex, px/rem, weights — not "nice", "premium".
- One coherent stance; competing directions are named and one is chosen.
- Keep the file context-sized; move long rationale to `references/`.
- Preserve the project's own identity; never clone a brand's assets or exact layout.
