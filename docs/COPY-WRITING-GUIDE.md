# Docs, README, and product copy (public kit)

[English](COPY-WRITING-GUIDE.md) · [简体中文](COPY-WRITING-GUIDE.zh-CN.md) · [日本語](COPY-WRITING-GUIDE.ja.md) · [한국어](COPY-WRITING-GUIDE.ko.md)

<!-- SEO: wawoo-skills documentation writing AGENTS.md skills technical writing -->

## One line

This **open-source** kit ships **engineering-first** writing skills—not a full ads/LP stack. Use the table below to pick **workflow → skill → agent** without reading all 97 skills.

## What exists in this repo

| Goal | Start here | Skills | Agent role |
|------|------------|--------|------------|
| README, `AGENTS.md`, skills | `/delivery-lite` or direct `skill_get` | `writing-for-agents` | `docs-specialist` |
| Multi-language docs | same | `documentation-localization`, `language-policy` | `docs-localization-reviewer` |
| PR description | same | `pr` | `docs-specialist` |
| Plan / status markdown | `/status-report`, `/sprint-plan` | `plan-md` | `project-manager` |
| Research → spec (not ad copy) | `/research` | `research` → `product-discovery` → `to-spec` | `product-owner` |

**Not in this public tree:** `/writing`, `/market-plan`, `viral-hooks`, `marketing-psychology` (those live in extended workspaces only). Do not document them here.

## Readable workflow: improve a README

1. MCP **`interpret_intent`** or pick **`/delivery-lite`**
2. **`memory_recall`** — [MEMORY-CLIENT-GUIDE.md](MEMORY-CLIENT-GUIDE.md)
3. Open **`writing-for-agents`** only (one skill at a time)
4. Draft in plain language; facts in tables; link [GUIDES.md](GUIDES.md)
5. Agent viewpoint **`docs-specialist`** for structure, human reviews facts
6. **`memory_save`** after decisions (if `WAWOO_MEMORY_READONLY=0`)

## `writing-for-agents` in plain words

- **One doc, one job** (skill vs `USAGE` vs guide — no duplicates)
- **Short entry** `SKILL.md`; long detail in `references/`
- **Gates:** no secrets in examples; consistent with `AGENTS.md`

Skill file: `.kilo/skills/writing-for-agents/SKILL.md`

## Agents (copy-related)

| Agent | Use when |
|-------|----------|
| `docs-specialist` | Markdown, README, skill text |
| `docs-localization-reviewer` | JA/EN/ZH/KO factual sync |
## Quality before publish

1. Separate **fact** vs **opinion**  
2. Numbers match `gen_capabilities.py` (**97 / 21 / 12**)  
3. External post: run policy skills if enabled (`content-guardrail`, `mask_pii`)  
4. User-facing docs: [language-policy](.kilo/skills/language-policy/SKILL.md) tiers  

**Index:** [GUIDES.md](GUIDES.md)