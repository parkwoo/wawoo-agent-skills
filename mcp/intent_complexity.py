"""Deterministic complexity estimate → model tier (no model).

Crude but stable: token count plus a few structural signals. Used to suggest a
``model_tier`` (``fast`` for simple/medium, ``reasoning`` for complex) so callers
can route mechanical work to a cheap model and hard work to a stronger one.
"""
from __future__ import annotations

import re

_TOK = re.compile(r"[A-Za-z0-9_']+|[\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7a3]")
_COMPLEX_SIGNALS = (
    "end to end",
    "end-to-end",
    "architecture",
    "migrate",
    "migration",
    "refactor",
    "redesign",
    "multi",
    "across",
    "integrate",
    "pipeline",
    "schema",
    "rollback",
    "security",
    "compliance",
    "distributed",
    "concurrency",
)


def estimate_complexity(text: str) -> tuple[str, int, str]:
    """Return (complexity, tokens, model_tier). complexity ∈ simple|medium|complex."""
    low = (text or "").lower()
    tokens = len(_TOK.findall(low))
    hits = sum(1 for s in _COMPLEX_SIGNALS if s in low)
    if tokens >= 120 or hits >= 3:
        complexity = "complex"
    elif tokens >= 40 or hits >= 1:
        complexity = "medium"
    else:
        complexity = "simple"
    return complexity, tokens, model_tier_for(complexity)


def model_tier_for(complexity: str) -> str:
    return "reasoning" if complexity == "complex" else "fast"


def selftest() -> int:
    assert estimate_complexity("fix the typo")[0] == "simple"
    assert estimate_complexity("refactor the architecture across services with a migration")[0] in ("medium", "complex")
    assert estimate_complexity("x " * 130)[0] == "complex"
    assert model_tier_for("complex") == "reasoning"
    assert model_tier_for("simple") == "fast"
    print("selftest OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(selftest())
