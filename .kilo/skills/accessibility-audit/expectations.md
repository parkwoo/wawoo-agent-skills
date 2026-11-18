# accessibility-audit — expectations (uplift pilot)

Static heuristics. Rule ids must match `ACTIVE_STATIC_RULES` in `scripts/uplift_pilot.py`.

## Structure and forms

- `[a11y-html-lang]` Root `html` has `lang`
- `[a11y-page-h1]` Page has an `h1` (per-file scope)
- `[a11y-input-label]` `input`/`select`/`textarea` has `id`+`label[for]` or `aria-label` / `aria-labelledby`
- `[a11y-button-type]` `button` in forms has explicit `type` (avoid accidental submit)
- `[a11y-skip-link]` Skip link near top (e.g. `#main`) — heuristic for landing HTML

## Limits

Fragments may false-positive on `h1` / skip-link. Scan directories and triage findings.

## Check

```bash
python3 scripts/skill_uplift_check.py accessibility-audit --path <ui-root>
```