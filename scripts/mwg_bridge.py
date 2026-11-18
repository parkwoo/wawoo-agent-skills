#!/usr/bin/env python3
"""Thin wrapper for Google Chrome Modern Web Guidance CLI (npx, network required)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import Any


def _run(argv: list[str], timeout: int = 120) -> tuple[int, str, str]:
    if os.environ.get("WAWOO_MWG_DISABLE", "").strip().lower() in {"1", "true", "yes"}:
        return 1, "", "MWG disabled (WAWOO_MWG_DISABLE)"
    cmd = ["npx", "--yes", "modern-web-guidance@latest", *argv]
    try:
        p = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        return 127, "", "npx not found; install Node.js"
    except subprocess.TimeoutExpired:
        return 124, "", f"timeout after {timeout}s"
    return p.returncode, p.stdout, p.stderr


def search(query: str) -> dict[str, Any]:
    code, out, err = _run(["search", query])
    if code != 0:
        return {"ok": False, "error": err.strip() or out.strip() or f"exit {code}"}
    try:
        hits = json.loads(out)
    except json.JSONDecodeError:
        hits = out.strip()
    return {"ok": True, "query": query, "results": hits}


def retrieve(guide_id: str) -> dict[str, Any]:
    code, out, err = _run(["retrieve", guide_id])
    if code != 0:
        return {"ok": False, "error": err.strip() or out.strip() or f"exit {code}"}
    return {"ok": True, "id": guide_id, "content": out}


def legacy_scan(path: str) -> dict[str, Any]:
    code, out, err = _run(["legacy-scan", path], timeout=300)
    if code != 0:
        return {"ok": False, "error": err.strip() or out.strip() or f"exit {code}"}
    return {"ok": True, "path": path, "report": out}


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: mwg_bridge.py search <query> | retrieve <id> | legacy-scan <path>", file=sys.stderr)
        return 2
    op = sys.argv[1]
    if op == "search" and len(sys.argv) >= 3:
        print(json.dumps(search(" ".join(sys.argv[2:])), ensure_ascii=False, indent=2))
        return 0
    if op == "retrieve" and len(sys.argv) >= 3:
        print(json.dumps(retrieve(sys.argv[2]), ensure_ascii=False)[:500000])
        return 0
    if op == "legacy-scan" and len(sys.argv) >= 3:
        res = legacy_scan(sys.argv[2])
        print(json.dumps({"ok": res["ok"], "path": res.get("path"), "error": res.get("error")}, ensure_ascii=False))
        if res.get("ok"):
            print(res.get("report", ""))
        return 0 if res.get("ok") else 1
    print(f"unknown op: {op}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())