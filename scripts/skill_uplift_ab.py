#!/usr/bin/env python3
"""Playwright A/B uplift runner — unguided vs guided fixture pass rates."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AB_ROOT = ROOT / "internal" / "skill-uplift-ab"
SCENARIOS = frozenset({"accessible-dialog"})


def _npm_ready() -> bool:
    return (AB_ROOT / "node_modules" / "@playwright" / "test").is_dir()


def run_playwright(scenario: str, fixture: str) -> dict:
    out_dir = AB_ROOT / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / f"report-{scenario}-{fixture}.json"
    env = {
        **os.environ,
        "UPLIFT_SCENARIO": scenario,
        "UPLIFT_FIXTURE": fixture,
    }
    cmd = [
        "npx",
        "playwright",
        "test",
        f"--config={AB_ROOT / 'playwright.config.mjs'}",
        "--reporter=json",
    ]
    proc = subprocess.run(
        cmd,
        cwd=str(AB_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    raw = proc.stdout.strip() or proc.stderr.strip()
    stats = {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
    if raw:
        try:
            data = json.loads(raw)
            top = data.get("stats") or {}
            if top:
                stats["passed"] = int(top.get("expected", 0))
                stats["failed"] = int(top.get("unexpected", 0))
                stats["skipped"] = int(top.get("skipped", 0))
                stats["total"] = stats["passed"] + stats["failed"] + stats["skipped"] + int(top.get("flaky", 0))
            else:
                suites = data.get("suites") or []
                for suite in suites:
                    for spec in suite.get("specs") or []:
                        for test in spec.get("tests") or []:
                            stats["total"] += 1
                            for r in test.get("results") or []:
                                status = r.get("status", "failed")
                                if status == "passed":
                                    stats["passed"] += 1
                                elif status == "skipped":
                                    stats["skipped"] += 1
                                else:
                                    stats["failed"] += 1
                                break
        except json.JSONDecodeError:
            stats["parse_error"] = raw[:500]
    report_path.write_text(json.dumps({"exit": proc.returncode, "stats": stats, "raw_len": len(raw)}, indent=2), encoding="utf-8")
    rate = stats["passed"] / stats["total"] if stats["total"] else 0.0
    return {
        "fixture": fixture,
        "exit_code": proc.returncode,
        "pass_rate": round(rate, 4),
        "stats": stats,
    }


def run_ab(scenario: str, unguided_dir: Path | None, guided_dir: Path | None) -> dict:
    if scenario not in SCENARIOS:
        return {"ok": False, "error": f"unknown scenario: {scenario}"}
    if not _npm_ready():
        return {
            "ok": False,
            "error": "Playwright not installed. Run: cd internal/skill-uplift-ab && npm install && npx playwright install chromium",
        }
    modes: list[tuple[str, str]] = []
    if unguided_dir and guided_dir:
        # Future: copy custom artifact dirs into temp fixtures — for now only bundled fixtures
        pass
    modes = [("unguided", "unguided"), ("guided", "guided")]
    results = [run_playwright(scenario, name) for _, name in modes]
    by = {r["fixture"]: r for r in results}
    u = by["unguided"]["pass_rate"]
    g = by["guided"]["pass_rate"]
    return {
        "ok": True,
        "scenario": scenario,
        "ts": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "unguided": by["unguided"],
        "guided": by["guided"],
        "uplift": round(g - u, 4),
        "opportunity": round(1.0 - u, 4),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Skill uplift Playwright A/B")
    ap.add_argument("--scenario", default="accessible-dialog")
    ap.add_argument("--unguided", type=Path, help="optional artifact dir (reserved)")
    ap.add_argument("--guided", type=Path, help="optional artifact dir (reserved)")
    ap.add_argument("--out", type=Path, help="write JSON evidence path")
    args = ap.parse_args()
    res = run_ab(args.scenario, args.unguided, args.guided)
    text = json.dumps(res, ensure_ascii=False, indent=2)
    print(text)
    if args.out:
        path = args.out if args.out.is_absolute() else ROOT / args.out
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n", encoding="utf-8")
    if not res.get("ok"):
        return 2
    # exit 1 if guided does not beat unguided (calibration / regression)
    if res.get("uplift", 0) <= 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())