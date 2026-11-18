---
name: writing-for-agents
description: Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md.
---
# Writing for Agents

How to write **human-readable** docs agents actually follow (skills, `AGENTS.md`, guides).

**User-facing map (public kit):** `docs/COPY-WRITING-GUIDE.md` (EN · 简体中文 · 日本語 · 한국어).

## Context budget

- Entry: this `SKILL.md`.
- Detail & mechanics: [`references/writing-guide.md`](references/writing-guide.md), [`SKILL-MECHANICS.md`](../SKILL-MECHANICS.md).

## Plain rules

1. One file, one job (link out instead of duplicating USAGE or guides).
2. Lead with **who it is for** and **what to do first** (tables beat jargon).
3. Paseo-style language bar: English · 简体中文 · 日本語 · 한국어 on every user guide.
4. No secrets in examples; counts match `gen_capabilities.py` (public: **97 / 21 / 12**).

## Gates

- Do not include secrets or personal data in examples.
- One document, one purpose (do not break the SSOT).
