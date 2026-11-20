# Copy, ads & long-form — workflow map

[English](COPY-MARKETING-GUIDE.md) · [日本語](COPY-MARKETING-GUIDE.ja.md) · [简体中文](COPY-MARKETING-GUIDE.zh-CN.md) · [한국어](COPY-MARKETING-GUIDE.ko.md)

## One-liner

For **non-code writing**, pick a **workflow** by goal; load **one skill per phase** via `skill_get` — never read the full catalog.

## 1. Which entry?

| Goal | Command | SSOT | Main skills |
|------|---------|------|-------------|
| Blog, essay, column, script draft | `/writing` | optional `CONTENT.md` | `writing-fragments` → `writing-beats` → `writing-shape` |
| Strong title / hook | `/writing` (viral) | same | + `viral-hooks` → `marketing-psychology` |
| Popular science / explainers | `/writing` (science) | same | + `science-writing` |
| Book / long report chapters | `/content-delivery-lite` | `CONTENT.md` | `writing-for-agents`, … |
| Market → pricing framing | `/market-plan` | `ACTIVE.md` | `research` → … → `marketing-psychology` |
| Slides | `/deck` | `ACTIVE.md` | `slides` + research chain |
| LP / marketing shots | skills only | evidence paths | `screenshots-marketing`, `fal-gen` |
| Docs / README | `/delivery-lite` or edit | `ACTIVE.md` | `writing-for-agents` |

**Memory:** `memory_recall` before work; `memory_save` after decisions — [MEMORY-CLIENT-GUIDE.md](MEMORY-CLIENT-GUIDE.md).

## 2. `/writing` three phases

| Phase | Skill | Do | Don't |
|-------|-------|-----|--------|
| Explore | `writing-fragments` | Save fragments to one `.md` | Outline or polish |
| Structure | `writing-beats` | Order beats; ground terms first | Full draft |
| Draft | `writing-shape` | Final copy in **new** output | Edit fragment file |

**Viral add-on:** `viral-hooks` (title/opening) → `marketing-psychology` (price/CTA **framing only** — facts unchanged).

## 3. `viral-hooks` vs `marketing-psychology`

| | `viral-hooks` | `marketing-psychology` |
|--|---------------|-------------------------|
| Focus | Title, lead, article shape | Price, plans, CTA order |
| Output | 3 titles + 1 lead | before/after framing |
| Avoid | Clickbait, fake stats | False scarcity |

Procedure: `marketing-psychology/references/framing-principles.md`

## 4. Agents

| Agent | Use for |
|-------|---------|
| `docs-specialist` | `/writing`, `/content-delivery-lite` |
| `market-researcher` | `/market-plan` — **humans decide price/contracts** |

Route: `interpret_intent` → `workflow_get`.

## 5. Doc map

| Topic | SSOT |
|-------|------|
| Client install | [CLIENT-INTEGRATION-GUIDE.md](CLIENT-INTEGRATION-GUIDE.md) |
| Memory | [MEMORY-CLIENT-GUIDE.md](MEMORY-CLIENT-GUIDE.md) |
| All guides | [GUIDES.md](GUIDES.md) |

## 6. Quality gates

1. Separate fact vs inference.  
2. Title promise = body delivery.  
3. External publish after approval (`guard_content`, `mask_pii`).  
4. Label unverified numbers.

**Index:** [GUIDES.md](GUIDES.md)