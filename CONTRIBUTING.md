# Contributing to wawoo-skills

Thanks for taking the time to contribute. This guide explains where each kind of contribution belongs and what we expect, so we both save time.

wawoo-skills is a **public, programming-focused kit** of reusable skills, agents, workflows, and an MCP server for AI coding agents. It is generated from an internal source; this repository is the published surface.

## Philosophy

- **Lean, opinionated core.** The core stays small and predictable. Specialized workflows and one-off integrations belong in your own project or a separate skill, not in core.
- **Programming only.** Writing, marketing, SEO, and copywriting skills are maintained in the internal source, not here.
- **The core evolves through shared improvements.** Reusable capabilities that benefit many workflows are more valuable than a control for one task.

Read the [README](README.md) for what the kit does and how it is organized.

## Where changes belong

| Location | Role | Who reads it |
|---|---|---|
| Internal source (`workspace/skills`) | **Source of truth**: all skills / agents / workflows | Your local MCP (`WAWOO_SKILLS_ROOT`) |
| This repository | **Published output**: programming-focused assets only | GitHub and readers |
| `~/.config/kilo/` | Global install mirror (`install_global.py`) | Kilo |

- Do **not** add writing / marketing / SEO / proofreading skills here.
- Change the internal source first, then publish; do not grow the public repo directly.

## Report bugs

Open a GitHub issue and use the **bug report** template. Include:

- What you did, what you expected, and what happened.
- Reproduction steps, the kit version (`VERSION`), and your platform.
- Relevant logs, screenshots, or a recording.

If an agent investigated, include the evidence and reproduction steps it collected. An explanation of the cause still needs verification.

## Discuss before proposing features

Product discussions, including feature requests, belong in **GitHub Discussions**. Feature requests opened as issues will be closed.

Explain:

- What are you trying to do?
- How do you do it today?
- Where does the kit get in the way?
- What would a better workflow look like?

There is no feature-request backlog or commitment to implement. A discussion may be read and learned from without a reply.

## Pull requests

**Focused fixes for reproducible bugs are welcome.** For features, open a discussion first. A PR without a linked issue or discussion may be closed.

**PRs are reviewed on a best-effort basis.** Submitting one only makes sense if you are comfortable with it being closed without a detailed review.

### What we look for

- **Demonstrated demand.** Link an issue or discussion with concrete examples.
- **Value across workflows.** Prefer reusable improvements over isolated controls.
- **A coherent design.** Shared capabilities should work across clients and providers; do not reshape a shared abstraction around one client.
- **A finished experience.** Follow the existing structure and style; incomplete or rushed changes will be closed.

### Keep the scope small

Submit one focused change. Very large PRs (roughly **3,000+ lines of production code**) are unlikely to be accepted. Prefer the smallest complete improvement that can be tested and understood on its own.

### QA evidence

Run the changed behavior yourself and include evidence:

- The commands you ran and their output.
- Tests that exercise the changed behavior. A bug fix needs a regression test that fails on the broken version.
- For interactive UI or client changes: before/after screenshots or a recording.
- The clients and platforms you tested, and any you could not test.

PRs without verification and evidence will be closed, whether they fix a bug or add a feature.

Using an agent is welcome. Submitting its output without trying the result yourself does not meet this bar.

### Local checks (required)

Run these before opening a PR and paste the results:

```bash
python3 scripts/validate_assets.py    # asset checks (name=dir, refs, duplicates, JSON)
python3 scripts/gen_capabilities.py   # regenerate the catalog (do not hand-edit it)
python3 scripts/e2e_flows.py          # MCP contract / E2E smoke
python3 scripts/check_public_boundary.py   # programming-only boundary
```

- If `gen_capabilities.py` changes `.kilo/CAPABILITIES.md`, commit it with your change.
- If you added a third-party asset, update `.kilo/skills/ATTRIBUTION.md` and `LICENSES/`; unverified-license assets are not accepted.
- Bump `VERSION` and update `CHANGELOG.md` only when asked.

## Security

Do not open public issues for security problems. Follow [`SECURITY.md`](SECURITY.md).

## License

By contributing, you agree that your contribution is licensed under the repository's **MIT** license (see `LICENSE`). Keep third-party copyright and NOTICE notices intact.
