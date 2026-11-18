# web-design-guidelines — expectations (uplift pilot)

Rule ids match `ACTIVE_STATIC_RULES` in `scripts/uplift_pilot.py`. Checks are **per-file heuristics** (false positives possible).

## Images and accessibility

- `[img-alt]` `img` has `alt` (decorative: `alt=""`)

## Focus and input

- `[tabindex-positive]` Avoid positive `tabindex`
- `[outline-none]` When `outline: none|0`, provide a focus substitute in the same file

## Motion

- `[reduced-motion]` Animations without `prefers-reduced-motion` in-file → review (global CSS not traced)

## Interaction

- `[clickable-div]` `onclick` on `div`/`span` without `role="button"` (or similar)

## Check

```bash
python3 scripts/skill_uplift_check.py web-design-guidelines --path <ui-root>
```