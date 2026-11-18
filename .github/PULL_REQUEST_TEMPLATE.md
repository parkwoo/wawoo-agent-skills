## Summary

<!-- What does this change, and why? Link the issue or discussion. -->

Closes #

## Scope

- [ ] One focused change
- [ ] No writing / marketing / SEO skills added (this repository is programming-only)

## QA evidence

Commands run and their output:

```bash
python3 scripts/validate_assets.py
python3 scripts/gen_capabilities.py
python3 scripts/e2e_flows.py
python3 scripts/check_public_boundary.py
```

- [ ] `validate_assets` OK
- [ ] `e2e_flows` passed, 0 failed
- [ ] `check_public_boundary` OK
- [ ] Before/after screenshots or a recording for UI or client changes (if applicable)

## Checklist

- [ ] Linked an issue or discussion
- [ ] Added/updated a regression test (for bug fixes)
- [ ] Updated `ATTRIBUTION.md` / `LICENSES/` for third-party assets (if any)
- [ ] Removed secrets and personal data
