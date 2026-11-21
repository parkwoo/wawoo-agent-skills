#!/usr/bin/env python3
"""docs/*.md → eleventy/content/{locale}/docs/{slug}.md（MkDocs 互換レイアウト front matter）。"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT = ROOT / "eleventy" / "content"

PAGES = ["usage", "download", "guides", "skills-catalog", "changelog"]

LOCALE_FILES = {
    "cn": {"usage": "usage.md", "download": "download.md", "guides": "guides.md", "skills-catalog": "skills-catalog.md", "changelog": "changelog.md"},
    "en": {"usage": "usage.en.md", "download": "download.en.md", "guides": "guides.en.md", "skills-catalog": "skills-catalog.en.md", "changelog": "changelog.en.md"},
    "ja": {"usage": "usage.ja.md", "download": None, "guides": None, "skills-catalog": "skills-catalog.ja.md", "changelog": "changelog.ja.md"},
    "ko": {"usage": None, "download": None, "guides": None, "skills-catalog": "skills-catalog.ko.md", "changelog": None},
}


def _prepare_usage() -> None:
    prep = ROOT / "scripts" / "prepare_usage_mkdocs.py"
    if not prep.is_file():
        return
    subprocess.run([sys.executable, str(prep)], check=False, cwd=str(ROOT))


def _strip_fm(text: str) -> str:
    if not text.startswith("---"):
        return text
    m = re.match(r"^---\s*\n.*?\n---\s*\n", text, re.DOTALL)
    return text[m.end() :] if m else text


def _title_from(text: str, fallback: str) -> str:
    m = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else fallback


def _expand_changelog(body: str) -> str:
    if "{%" in body or "include-markdown" in body:
        cl = ROOT / "CHANGELOG.md"
        if cl.is_file():
            return f"# 更新日志\n\n{cl.read_text(encoding='utf-8')}"
    return body


def main() -> int:
    _prepare_usage()
    if OUT.is_dir():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    for loc, slugs in LOCALE_FILES.items():
        for slug, src_name in slugs.items():
            if not src_name:
                continue
            src = DOCS / src_name
            if not src.is_file():
                print(f"skip missing {src_name}", file=sys.stderr)
                continue
            raw = src.read_text(encoding="utf-8")
            title = _title_from(raw, slug)
            body = _strip_fm(raw)
            if slug == "changelog":
                body = _expand_changelog(body)
            dest_dir = OUT / loc / "docs" / slug
            dest_dir.mkdir(parents=True, exist_ok=True)
            fm = f"""---
layout: doc.njk
locale: {loc}
title: {title}
permalink: /{loc}/docs/{slug}/
---
"""
            (dest_dir / "index.md").write_text(fm + body, encoding="utf-8")
            print(f"staged /{loc}/docs/{slug}/")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())