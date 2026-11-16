#!/usr/bin/env python3
"""context-compression — deterministic, pure-Python context cleaning & compression.

No LLM, no network, no external model. Heuristic filters + fuzzy dedup +
information-density scoring, all local (milliseconds). Standard library only.

Use it as a library (`ContextCompressionEngine`) or from the CLI:

  python3 compress.py --input turns.json [--budget-tokens 2000] [--json]
  python3 compress.py --input turns.json --max-age-turns 20 --jaccard 0.85
  cat turns.json | python3 compress.py
  python3 compress.py --selftest

Input: a JSON array of turns, each {"role": "...", "text": "...", "ts": <number?>}.
Output: JSON {"turns": [...kept...], "stats": {...}} (kept turns stay chronological).
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass, field
from typing import Iterable, Sequence

_TOK_RE = re.compile(r"[A-Za-z0-9_']+|[\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7a3]")
_WS_RE = re.compile(r"\s+")
_ACK_RE = re.compile(
    r"^(ok(ay)?|sure|got it|gotcha|thanks?|thank you|understood|sounds good|"
    r"yes|yeah|yep|no|nope|done|cool|great|nice|np|no problem|明白|了解|okです)[.!。 ]*$",
    re.IGNORECASE,
)

# Small, deterministic English stopword set (kept inline: no downloads, no version drift).
_STOPWORDS = frozenset(
    "a an the and or but if then else of to in on at by for with from as is are was were be been "
    "being do does did doing have has had having i you he she it we they me him her us them this "
    "that these those my your his its our their so than too very can will just should now".split()
)


def tokenize(text: str) -> list[str]:
    """Lowercase, split latin into words and CJK into characters (deterministic)."""
    return _TOK_RE.findall(text.lower())


def normalize(text: str) -> str:
    """NFKC-ish whitespace normalization (stdlib, deterministic)."""
    import unicodedata

    text = unicodedata.normalize("NFKC", text or "")
    return _WS_RE.sub(" ", text).strip()


@dataclass
class Turn:
    role: str
    text: str
    ts: float | None = None
    idx: int = 0
    norm: str = ""
    tokens: list[str] = field(default_factory=list)
    density: float = 0.0

    @classmethod
    def from_raw(cls, idx: int, raw: dict) -> "Turn":
        text = normalize(str(raw.get("text", "")))
        turn = cls(role=str(raw.get("role", "")), text=text, ts=raw.get("ts"), idx=idx)
        turn.norm = " ".join(tokenize(text))
        turn.tokens = tokenize(text)
        return turn


class ContextCompressionEngine:
    """Deterministic context cleaner/compressor. No model, no I/O beyond stdout when run as CLI."""

    def __init__(
        self,
        *,
        budget_tokens: int = 2000,
        max_age_turns: int | None = None,
        jaccard: float = 0.85,
        seq_ratio: float = 0.9,
        min_tokens: int = 2,
        drop_acks: bool = True,
        keep_system: bool = False,
        half_life: float = 10.0,
        w_len: float = 0.3,
        w_uniq: float = 0.3,
        w_rec: float = 0.25,
        w_kw: float = 0.15,
        keywords: Iterable[str] = (),
    ) -> None:
        self.budget_tokens = budget_tokens
        self.max_age_turns = max_age_turns
        self.jaccard = jaccard
        self.seq_ratio = seq_ratio
        self.min_tokens = min_tokens
        self.drop_acks = drop_acks
        self.keep_system = keep_system
        self.half_life = half_life
        self.w_len, self.w_uniq, self.w_rec, self.w_kw = w_len, w_uniq, w_rec, w_kw
        self.keywords = {k.lower() for k in keywords}

    # --- scoring ---------------------------------------------------------
    def _density(self, turn: Turn, n: int) -> float:
        toks = turn.tokens
        if not toks:
            return 0.0
        length_term = min(len(toks), 200) / 200.0
        uniq = len(set(toks)) / len(toks)
        recency = 0.5 ** ((n - 1 - turn.idx) / self.half_life) if self.half_life > 0 else 1.0
        content = [w for w in toks if w not in _STOPWORDS]
        kw = (sum(1 for w in content if w in self.keywords) / len(content)) if self.keywords and content else 0.0
        return self.w_len * length_term + self.w_uniq * uniq + self.w_rec * recency + self.w_kw * kw

    # --- similarity ------------------------------------------------------
    def _near_dup(self, a: Turn, b: Turn) -> bool:
        if a.norm == b.norm:
            return True
        sa, sb = set(a.tokens), set(b.tokens)
        if not sa or not sb:
            return False
        jac = len(sa & sb) / len(sa | sb)
        if jac < self.jaccard:
            return False
        return _ratio(a.norm, b.norm) >= self.seq_ratio

    # --- main ------------------------------------------------------------
    def compress(self, raw_turns: Sequence[dict]) -> dict:
        turns = [Turn.from_raw(i, r) for i, r in enumerate(raw_turns)]
        n = len(turns)
        dropped = {"blank": 0, "ack": 0, "system": 0, "short": 0, "stale": 0, "dup": 0}

        # 1) heuristic filters
        kept: list[Turn] = []
        for t in turns:
            if not t.norm:
                dropped["blank"] += 1
                continue
            if t.role == "system" and not self.keep_system:
                dropped["system"] += 1
                continue
            if self.drop_acks and t.role == "assistant" and _ACK_RE.match(t.text):
                dropped["ack"] += 1
                continue
            if len(t.tokens) < self.min_tokens:
                dropped["short"] += 1
                continue
            kept.append(t)

        # 2) stale-window drop (superseded by later turns)
        if self.max_age_turns is not None and len(kept) > self.max_age_turns:
            cutoff = len(kept) - self.max_age_turns
            fresh = kept[cutoff:]
            dropped["stale"] += cutoff
            kept = fresh

        # 3) fuzzy dedup — keep the densest (tie: latest) of each near-dup cluster
        for t in kept:
            t.density = self._density(t, n)
        survivors: list[Turn] = []
        for t in kept:
            dup_of = None
            for s in survivors:
                if self._near_dup(t, s):
                    dup_of = s
                    break
            if dup_of is None:
                survivors.append(t)
            else:
                dropped["dup"] += 1
                if t.density > dup_of.density or (t.density == dup_of.density and t.idx > dup_of.idx):
                    survivors[survivors.index(dup_of)] = t

        # 4) information-density budget — greedy by score, then chronological
        chosen = sorted(survivors, key=lambda t: (-t.density, t.idx))
        out: list[Turn] = []
        used = 0
        for t in chosen:
            cost = len(t.tokens)
            if used + cost > self.budget_tokens and out:
                continue
            out.append(t)
            used += cost
        out.sort(key=lambda t: t.idx)

        return {
            "turns": [{"role": t.role, "text": t.text, **({"ts": t.ts} if t.ts is not None else {})} for t in out],
            "stats": {
                "input_turns": n,
                "kept_turns": len(out),
                "dropped": dropped,
                "tokens_in": sum(len(t.tokens) for t in turns),
                "tokens_out": used,
                "ratio": round(len(out) / n, 4) if n else 0.0,
            },
        }


def _ratio(a: str, b: str) -> float:
    import difflib

    return difflib.SequenceMatcher(None, a, b).ratio()


def selftest() -> int:
    raw = [
        {"role": "system", "text": "You are a helpful assistant."},
        {"role": "user", "text": "How do I reset the cache?"},
        {"role": "assistant", "text": "Sure"},
        {"role": "assistant", "text": "Run `cache-cli reset --all` then restart the service."},
        {"role": "user", "text": "how do i reset the cache ?"},  # near-dup question
        {"role": "assistant", "text": "Run cache-cli reset --all, then restart the service."},
        {"role": "user", "text": "ok"},
        {"role": "user", "text": "What about the migration step for the new schema and its rollback plan?"},
        {"role": "user", "text": ""},
    ]
    eng = ContextCompressionEngine(budget_tokens=1000, max_age_turns=None)
    res = eng.compress(raw)
    stats = res["stats"]
    kept = [t["text"] for t in res["turns"]]
    assert stats["dropped"]["system"] == 1, stats
    assert stats["dropped"]["ack"] >= 1, stats
    assert stats["dropped"]["dup"] >= 1, stats
    assert stats["dropped"]["blank"] == 1, stats
    assert any("cache-cli reset" in t for t in kept), kept
    assert any("migration" in t for t in kept), kept
    assert stats["ratio"] < 1.0
    # determinism: same input -> identical output
    assert eng.compress(raw) == res
    print("selftest OK:", json.dumps(stats))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Deterministic, pure-Python context cleaning & compression (no LLM).")
    ap.add_argument("--input", help="JSON file with a list of turns (default: stdin)")
    ap.add_argument("--budget-tokens", type=int, default=2000)
    ap.add_argument("--max-age-turns", type=int, default=None, help="drop turns older than the last N (superseded)")
    ap.add_argument("--jaccard", type=float, default=0.85)
    ap.add_argument("--seq-ratio", type=float, default=0.9)
    ap.add_argument("--min-tokens", type=int, default=2)
    ap.add_argument("--keep-system", action="store_true")
    ap.add_argument("--keywords", default="", help="comma-separated domain terms to weight")
    ap.add_argument("--json", action="store_true", help="pretty JSON output")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    text = open(args.input, encoding="utf-8").read() if args.input else sys.stdin.read()
    raw = json.loads(text)
    eng = ContextCompressionEngine(
        budget_tokens=args.budget_tokens,
        max_age_turns=args.max_age_turns,
        jaccard=args.jaccard,
        seq_ratio=args.seq_ratio,
        min_tokens=args.min_tokens,
        keep_system=args.keep_system,
        keywords=[k.strip() for k in args.keywords.split(",") if k.strip()],
    )
    res = eng.compress(raw)
    print(json.dumps(res, ensure_ascii=False, indent=2 if args.json else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
