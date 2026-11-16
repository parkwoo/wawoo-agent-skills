"""Calibrate the local lexical router (threshold + margin) on a labelled set.

Deterministic grid search over ``intent_eval.json``. Reports precision (accuracy
among routed items), recall over positives, and the abstain rate, then recommends
the threshold/margin that maximizes precision while keeping abstain under a cap.
Set the recommendation with ``WAWOO_INTENT_LEXICAL_THRESHOLD`` / ``_MARGIN``.

CLI:
  python3 intent_calibrate.py                # recommendation + table
  python3 intent_calibrate.py --json
  python3 intent_calibrate.py --max-abstain 0.3
  python3 intent_calibrate.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from intent_lexical import local_lexical_route

EVAL = Path(__file__).resolve().parent / "intent_eval.json"
THRESHOLDS = (0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50)
MARGINS = (0.00, 0.03, 0.05, 0.08, 0.10, 0.15)


def _items() -> list[dict]:
    return json.loads(EVAL.read_text(encoding="utf-8"))["items"]


def evaluate(threshold: float, margin: float, items: list[dict] | None = None) -> dict:
    items = items if items is not None else _items()
    positives = sum(1 for it in items if it.get("workflow"))
    routed = correct = false_route = 0
    for it in items:
        r = local_lexical_route(str(it.get("text", "")), threshold=threshold, margin=margin)
        if not r:
            continue
        routed += 1
        want = it.get("workflow")
        if want and r.workflow == want:
            correct += 1
        elif not want:
            false_route += 1
    total = len(items)
    return {
        "threshold": threshold,
        "margin": margin,
        "routed": routed,
        "correct": correct,
        "false_route": false_route,
        "total": total,
        "precision": round(correct / routed, 4) if routed else 0.0,
        "recall": round(correct / positives, 4) if positives else 0.0,
        "abstain_rate": round(1 - routed / total, 4) if total else 1.0,
    }


def calibrate(max_abstain: float = 0.5) -> dict:
    items = _items()
    rows = [evaluate(t, m, items) for t in THRESHOLDS for m in MARGINS]
    eligible = [r for r in rows if r["abstain_rate"] <= max_abstain and r["routed"] > 0]
    pool = eligible or rows
    best = max(pool, key=lambda r: (r["precision"], -r["abstain_rate"], r["routed"]))
    return {"best": best, "table": rows, "max_abstain": max_abstain}


def selftest() -> int:
    res = calibrate()
    best = res["best"]
    assert best["precision"] >= 0.5, best
    assert best["threshold"] > 0
    assert res["table"], "empty table"
    print("selftest OK:", json.dumps(best))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Calibrate the local lexical router.")
    ap.add_argument("--max-abstain", type=float, default=float(os.environ.get("WAWOO_INTENT_MAX_ABSTAIN", "0.5")))
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    res = calibrate(args.max_abstain)
    if args.json:
        print(json.dumps(res, indent=2))
        return 0
    best = res["best"]
    print(f"best: threshold={best['threshold']} margin={best['margin']} "
          f"precision={best['precision']} recall={best['recall']} abstain={best['abstain_rate']}")
    print(f"export WAWOO_INTENT_LEXICAL_THRESHOLD={best['threshold']}")
    print(f"export WAWOO_INTENT_LEXICAL_MARGIN={best['margin']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
