#!/usr/bin/env python3
"""Repo-local legacy front-end pattern scan (stdlib; complements MWG legacy-scan)."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RULES: list[tuple[str, re.Pattern[str]]] = [
    ("jquery", re.compile(r"\bjquery(\.min)?\.js\b|\$\(\s*['\"]", re.I)),
    ("bootstrap3-js", re.compile(r"bootstrap[/\-]3|bootstrap@3", re.I)),
    ("legacy-modal-lib", re.compile(r"\b(micromodal|sweetalert|swal)\b", re.I)),
    ("document-write", re.compile(r"\bdocument\.write\s*\(", re.I)),
    ("inline-onclick-heavy", re.compile(r"\bonclick\s*=\s*['\"]", re.I)),
    ("bare-innerHTML-assign", re.compile(r"\.innerHTML\s*=\s*[^;]+(?:user|input|param)", re.I)),
]


def iter_files(root: Path) -> list[Path]:
    exts = {".html", ".htm", ".js", ".ts", ".tsx", ".jsx", ".vue", ".php", ".phtml"}
    skip_dirs = {"node_modules", ".git", "vendor", "dist", "build", "__pycache__"}
    if root.is_file():
        return [root] if root.suffix.lower() in exts else []
    out: list[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in skip_dirs for part in p.parts):
            continue
        if ".min." in p.name:
            continue
        if p.suffix.lower() in exts:
            out.append(p)
    return out


def scan(path: Path) -> dict:
    hits: list[dict] = []
    files = iter_files(path)
    for f in files:
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            for rule_id, pat in RULES:
                if pat.search(line):
                    hits.append({"rule": rule_id, "path": str(f), "line": i, "excerpt": line.strip()[:120]})
    return {"ok": True, "root": str(path), "files": len(files), "hit_count": len(hits), "hits": hits}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", type=Path, nargs="?", default=Path.cwd())
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    res = scan(args.path.resolve())
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res["hit_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())