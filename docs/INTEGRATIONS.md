# Integrations: Paseo, Google, pstack

[English](INTEGRATIONS.md) · [简体中文](INTEGRATIONS.zh-CN.md) · [日本語](INTEGRATIONS.ja.md) · [한국어](INTEGRATIONS.ko.md)

This page explains **third-party stacks the public kit wires up to**—not product-specific private skills.

## Paseo

[**Paseo**](https://github.com/getpaseo/paseo) ships **OpenCode** as a built-in agent surface. wawoo-skills targets the **same OpenCode config** as the terminal CLI.

| What | How |
|------|-----|
| Config file | `~/.config/opencode/opencode.json` |
| Install | `python3 scripts/install_opencode.py` (add `--memory-writable` for `memory_save`) |
| After env changes | `paseo daemon stop && paseo daemon start` |
| Skills root | `WAWOO_SKILLS_ROOT` → your clone of this repo |
| MCP | Same `wawoo-skills` server as Kilo / Cursor |

**Guides:** [CLIENT-INTEGRATION-GUIDE.md](CLIENT-INTEGRATION-GUIDE.md) · [MEMORY-CLIENT-GUIDE.md](MEMORY-CLIENT-GUIDE.md)

Paseo plugin skills (`npx skills add getpaseo/paseo`) are **separate** from this kit; both can run if MCP and daemon are configured.

## Google (Modern Web Guidance & design docs)

The kit **does not fork** Google’s guide corpus. It bridges on demand:

| Piece | Role |
|-------|------|
| **`modern-web-guidance-bridge`** skill | When to call MWG; no local copy of 262 guides |
| **MCP** `mwg_search` / `mwg_retrieve` / `mwg_legacy_scan` | Search & fetch via `npx modern-web-guidance@latest` (network). Off with `WAWOO_MWG_DISABLE=1` |
| **`scripts/mwg_bridge.py`** | CLI helper used by MCP |
| **`frontend-guides-hub`** / **`legacy-web-scan`** | Route UI work to MWG or legacy-scan |
| **`design-md`** skill | [Stitch DESIGN.md](https://stitch.withgoogle.com/docs/design-md/specification) format (Google Labs lineage; Apache-2.0 in skill dir) |

Upstream OSS: [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance).  
UI workflow: `/ui-delivery` · evidence: [SKILL-UPLIFT-PILOT.md](SKILL-UPLIFT-PILOT.md).

**Intent routing** (`interpret_intent`) may use your **client’s upstream LLM** (OpenRouter, etc.)—that is configured in the **IDE/agent**, not bundled as “Google Gemini inside wawoo-skills.”

## pstack (engineering principles & verification)

**pstack** ([Lauren Tan / Poteto](https://github.com/poteto)) contributes **MIT** skills absorbed into this repo—mostly **`principle-*`** plus verification/thinking helpers.

| Examples | Use |
|----------|-----|
| `principle-*` (24 in catalog) | Optional judgment support—load **1–2 per phase**, not all at once |
| `blast-radius`, `benchmark-checklist`, `sharpen`, `swarm`, … | Deeper verification when a workflow names them |

**License:** `LICENSES/pstack-MIT.txt` · full table: [`.kilo/skills/ATTRIBUTION.md`](../.kilo/skills/ATTRIBUTION.md)

Selection hint: skill **`ask-matt`** routes toward pstack/principle skills when appropriate.

## Quick map

| You use… | Read first |
|----------|------------|
| Paseo desktop / mobile | [CLIENT-INTEGRATION-GUIDE.md](CLIENT-INTEGRATION-GUIDE.md) |
| Baseline / modern CSS & APIs | `modern-web-guidance-bridge` + `/ui-delivery` |
| Stitch-style design tokens | `design-md` |
| Strict engineering habits | `principle-*` / pstack skills via workflow or `ask-matt` |

**Index:** [GUIDES.md](GUIDES.md)