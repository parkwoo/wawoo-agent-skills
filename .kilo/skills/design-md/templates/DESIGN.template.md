# DESIGN.md — <Project / Brand>

> One coherent visual direction. Concrete values, not adjectives. Replace every `<...>`.

## 1. Visual Theme & Atmosphere

- Mood: <e.g. editorial, calm, tactile, serious>
- Density: <airy | balanced | dense>
- Feels like: <3 references / adjectives>
- Not: <explicit non-goals, e.g. "not playful, no neon">

## 2. Color Palette & Roles

| Role | Hex | Usage |
|---|---|---|
| surface-0 | `#______` | page background |
| surface-1 | `#______` | cards / raised |
| foreground | `#______` | primary text |
| foreground-muted | `#______` | secondary text |
| accent | `#______` | primary action |
| accent-foreground | `#______` | text on accent |
| success / warning / danger | `#______` | states |

Contrast: body text ≥ 4.5:1, large text ≥ 3:1.

## 3. Typography

| Token | Family | Size / Line | Weight | Tracking |
|---|---|---|---|---|
| display | `<family>` | `<40/48>` | `<card>` | `<...>` |
| h1 | | | | |
| h2 | | | | |
| body | | `<16/24>` | `<400>` | `<normal>` |
| mono | | | | |

## 4. Components

- **Button (primary):** `<bg, text, radius, padding, hover, focus, disabled>`
- **Card:** `<surface, radius, shadow, padding>`
- **Input:** `<border, radius, focus ring, error>`
- **Nav:** `<height, items, active state>`
- States: default / hover / focus-visible / active / disabled.

## 5. Layout & Spacing

- Spacing scale: `<4, 8, 12, 16, 24, 32, 48>`
- Grid / max-width: `<...>`
- Whitespace intent: `<...>`

## 6. Depth & Elevation

- surfaces: `<0..n>` · shadows: `<tokens>`

## 7. Do's and Don'ts

- Do: `<...>`
- Don't: `<...>`

## 8. Responsive Behavior

- Breakpoints: `<sm/md/lg>`
- Touch target ≥ `<44px>`
- Collapse/stack: `<...>`

## 9. Agent Prompt Guide

- Quick colors: surface `#____`, text `#____`, accent `#____`
- Prompt: "Build <screen> using this DESIGN.md. Editorial, calm, tactile; one warm accent; no purple/blue glow."
