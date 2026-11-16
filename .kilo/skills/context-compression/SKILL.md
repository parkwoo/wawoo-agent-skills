---
name: context-compression
description: Deterministically compress and clean multi-turn conversation context with pure Python (no LLM, no network) — drop stale turns, deduplicate repeated Q&A, and keep the highest information-density content locally in milliseconds. Use before a RAG/LLM call, as a post-retrieval filter, or when trimming a long chat history at zero API cost.
---

# context-compression — deterministic, offline context cleaning

Shrink a conversation/context window **without any model or network call**. The
engine runs locally (standard library only) and is fully **deterministic**: the
same input always yields the same output. Good for latency-critical backends and
for RAG post-processing where you must not pay for or wait on an LLM.

The reference implementation is bundled: [`compress.py`](./compress.py).

## What it does

1. **Heuristic filters** — normalize (NFKC + whitespace), drop blank turns, drop
   `system` turns (unless kept), drop assistant acknowledgements ("ok"/"sure"/
   "thanks"), drop below a minimum token count.
2. **Stale-window drop** — optionally keep only the last `N` turns (older rounds
   that were superseded are removed).
3. **Fuzzy dedup** — collapse near-duplicate turns (exact-normalized match, then
   token-set Jaccard, then sequence ratio); the **densest** (tie: latest) survives.
4. **Information-density budget** — score each turn (length, unique-token ratio,
   recency half-life, optional domain-keyword weight), keep the highest-scoring
   turns until a token budget is reached, then restore chronological order.

Output is the kept turns (chronological) plus `stats` (dropped counts, tokens
in/out, ratio).

## When to use

- Before sending context to an LLM/RAG pipeline (cheap, deterministic pre-trim).
- Post-retrieval cleanup: remove duplicated chunks/re-asked questions.
- Multi-turn chat trimming where an API round-trip is unacceptable.

Do **not** use it where semantic summarization is required (that needs a model);
this is lossy-but-deterministic selection, not abstractive summarization.

## Usage

CLI (JSON array of `{"role","text","ts?"}` in → JSON out):

```bash
python3 compress.py --input turns.json --budget-tokens 2000 --json
cat turns.json | python3 compress.py --max-age-turns 20 --jaccard 0.85
python3 compress.py --selftest          # deterministic self-check
```

Library:

```python
from compress import ContextCompressionEngine
eng = ContextCompressionEngine(budget_tokens=2000, max_age_turns=20, keywords=["schema", "rollback"])
result = eng.compress([{"role": "user", "text": "..."}, ...])   # -> {"turns": [...], "stats": {...}}
```

## MCP tool

The kit exposes it as the MCP tool **`compress_context`** (available in Kilo / Cursor / OpenCode):

```json
{ "turns": [ {"role": "user", "text": "..."}, ... ], "budget_tokens": 2000, "max_age_turns": 20 }
```

Returns `{ "turns": [...], "stats": {...} }`. Also accepts `input` = path to a JSON file of turns.

**Automatic mode (OpenCode)**: run it on every model call via a plugin on the `experimental.chat.messages.transform` hook (conservative, fail-open).

## Tuning

| Flag | Default | Effect |
|---|---|---|
| `--budget-tokens` | `2000` | final token ceiling (greedy by density) |
| `--max-age-turns` | off | keep only the last N turns (superseded rounds) |
| `--jaccard` / `--seq-ratio` | `0.85` / `0.9` | fuzzy-dedup strictness (higher = stricter) |
| `--min-tokens` | `2` | drop ultra-short turns |
| `--keep-system` | off | retain `system` turns |
| `--keywords` | empty | comma-separated domain terms weighted up in the score |

## Guarantees & limits

- **Offline & free**: standard library only, no network, no API, no model.
- **Deterministic**: stable ordering and scoring; safe to cache/test (`--selftest`).
- Tokenization is heuristic (latin words + CJK characters); it is **not** a real
  tokenizer, so `--budget-tokens` is an approximation, not an exact model count.
- Dedup is lexical/fuzzy, not semantic; paraphrases that share no tokens are kept.
