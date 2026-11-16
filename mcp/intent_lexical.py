"""Local lexical intent router — zero-model, deterministic pre-LLM layer.

Scores the input against per-workflow utterance examples (``intent_routes.json``)
with tf-idf cosine, then gates on an absolute cosine threshold and the margin over the runner-up.
It **abstains** (returns None) when confidence is low or the top two routes are
too close, so the existing upstream LLM scoring is used only when the local layer
is unsure.

Tunable via env (no model, no network):
  WAWOO_INTENT_LEXICAL=0            disable
  WAWOO_INTENT_LEXICAL_THRESHOLD    min share (default 0.55)
  WAWOO_INTENT_LEXICAL_MARGIN       min cosine gap between top-2 (default 0.05)
  WAWOO_INTENT_LEXICAL_MIN_TOKENS   min input tokens (default 3)
"""
from __future__ import annotations

import json
import math
import os
import re
from dataclasses import dataclass
from pathlib import Path

ROUTES_FILE = Path(__file__).resolve().parent / "intent_routes.json"
_TOK = re.compile(r"[A-Za-z0-9_']+|[\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7a3]")

_cache: tuple[dict[str, float], dict[str, dict[str, float]]] | None = None


def _tokenize(text: str) -> list[str]:
    return _TOK.findall((text or "").lower())


@dataclass
class LexicalRoute:
    workflow: str
    score: float  # winner cosine in [0,1] (confidence)
    cosine: float  # raw tf-idf cosine of the winner
    margin: float  # cosine gap vs runner-up
    runner_up: str = ""


def _load() -> tuple[dict[str, float], dict[str, dict[str, float]]]:
    global _cache
    if _cache is not None:
        return _cache
    raw = json.loads(ROUTES_FILE.read_text(encoding="utf-8"))
    docs: dict[str, list[str]] = {}
    for wf, utts in raw.items():
        if wf.startswith("_") or not isinstance(utts, list):
            continue
        docs[wf] = _tokenize(" ".join(str(u) for u in utts) + " " + wf.replace("-", " "))
    df: dict[str, int] = {}
    for toks in docs.values():
        for t in set(toks):
            df[t] = df.get(t, 0) + 1
    n = max(len(docs), 1)
    idf = {t: math.log((n + 1) / (c + 1)) + 1.0 for t, c in df.items()}

    def vec(toks: list[str]) -> dict[str, float]:
        tf: dict[str, int] = {}
        for t in toks:
            tf[t] = tf.get(t, 0) + 1
        return {t: (1.0 + math.log(c)) * idf.get(t, 1.0) for t, c in tf.items()}

    _cache = (idf, {wf: vec(toks) for wf, toks in docs.items()})
    return _cache


def _cos(a: dict[str, float], b: dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    dot = sum(v * b.get(t, 0.0) for t, v in a.items())
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def local_lexical_route(
    text: str,
    *,
    threshold: float | None = None,
    margin: float | None = None,
    min_tokens: int | None = None,
) -> LexicalRoute | None:
    idf, docvecs = _load()
    toks = _tokenize(text)
    mt = int(min_tokens if min_tokens is not None else os.environ.get("WAWOO_INTENT_LEXICAL_MIN_TOKENS", "3"))
    if len(toks) < mt:
        return None
    tf: dict[str, int] = {}
    for t in toks:
        tf[t] = tf.get(t, 0) + 1
    q = {t: (1.0 + math.log(c)) * idf[t] for t, c in tf.items() if t in idf}
    if not q:
        return None

    scored = sorted(((wf, _cos(q, v)) for wf, v in docvecs.items()), key=lambda x: x[1], reverse=True)
    top, s1 = scored[0]
    runner, s2 = scored[1] if len(scored) > 1 else ("", 0.0)
    if s1 <= 0.0:
        return None

    th = float(threshold if threshold is not None else os.environ.get("WAWOO_INTENT_LEXICAL_THRESHOLD", "0.30"))
    mg = float(margin if margin is not None else os.environ.get("WAWOO_INTENT_LEXICAL_MARGIN", "0.05"))
    if s1 < th or (s1 - s2) < mg:
        return None
    return LexicalRoute(workflow=top, score=round(s1, 4), cosine=round(s1, 4), margin=round(s1 - s2, 4), runner_up=runner)


def selftest() -> int:
    cases = {
        "run a retrospective and improve our process": "self-improve",
        "review my changes and fix what the review finds": "self-review",
        "prepare a pitch deck for the client": "deck",
        "market research and pricing strategy": "market-plan",
        "this screen's design needs a review": "design-review",
    }
    for text, want in cases.items():
        got = local_lexical_route(text)
        assert got is not None, f"no route for: {text}"
        assert got.workflow == want, f"{text!r} -> {got.workflow} (want {want})"
    assert local_lexical_route("ok") is None, "short input must abstain"
    print("selftest OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(selftest())
