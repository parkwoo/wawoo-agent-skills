#!/usr/bin/env python3
"""website/kit-header.fragment.html・kit-footer.fragment.html を静的 HTML と MkDocs フッターへ反映する。"""

from __future__ import annotations

import json
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "website"
DOCS_FOOTER = ROOT / "docs/overrides/partials/kit-site-footer.html"
LANG_JSON = WEB / "content/kit-lang-by-page.json"

HEADER_PATH = WEB / "kit-header.fragment.html"
FOOTER_PATH = WEB / "kit-footer.fragment.html"
LANG_PLACEHOLDER = "<!-- @kit-lang@ -->"

STATIC_PAGES = (
    "index.html",
    "download/index.html",
    "changelog/index.html",
    "guides/index.shell.html",
)

HEADER_RE = re.compile(r"<header\s+class=\"site-header\">[\s\S]*?</header>", re.MULTILINE)
FOOTER_RE = re.compile(r"<footer\s+class=\"site-footer\"[^>]*>[\s\S]*?</footer>", re.MULTILINE)
LANG_RE = re.compile(r"<select\s+class=\"kit-lang-select\"[\s\S]*?</select>", re.MULTILINE)


def _strip_leading_comment(text: str) -> str:
    text = text.strip()
    if text.startswith("<!--"):
        end = text.find("-->")
        if end != -1:
            text = text[end + 3 :].lstrip()
    return text


def load_header_fragment() -> str:
    return _strip_leading_comment(HEADER_PATH.read_text(encoding="utf-8"))


def load_footer_fragment() -> str:
    return _strip_leading_comment(FOOTER_PATH.read_text(encoding="utf-8"))


def _indent_lang_block(select_html: str) -> str:
    """nav 内と同じ 4 スペースインデントに揃える。"""
    lines = [ln.strip() for ln in select_html.strip().splitlines() if ln.strip()]
    return "\n".join(f"    {ln}" for ln in lines)


def lang_select_for_page(rel: str, page_html: str) -> str:
    if LANG_JSON.is_file():
        data = json.loads(LANG_JSON.read_text(encoding="utf-8"))
        raw = data.get(rel)
        if isinstance(raw, str) and raw.strip():
            return _indent_lang_block(raw)
    page_lang = LANG_RE.search(page_html)
    if page_lang:
        return _indent_lang_block(page_lang.group(0))
    return _indent_lang_block(
        textwrap.dedent(
            """
            <select class="kit-lang-select" data-kit-lang-select data-current="zh"
              aria-label="选择语言（当前：简体中文）">
              <option value="zh" data-href="/" selected>简体中文</option>
              <option value="ja" data-href="/ja/" disabled>日本語</option>
              <option value="en" data-href="/index.en.html">English</option>
              <option value="ko" data-href="/ko/" disabled>한국어</option>
            </select>
            """
        ).strip()
    )


def build_header(fragment: str, rel: str, page_html: str) -> str:
    lang = lang_select_for_page(rel, page_html)
    if LANG_PLACEHOLDER not in fragment:
        raise RuntimeError("kit-header.fragment.html に <!-- @kit-lang@ --> がありません")
    return fragment.replace(LANG_PLACEHOLDER, lang)


def patch_page(html: str, header_frag: str, footer_frag: str, rel: str) -> str:
    if HEADER_RE.search(html):
        header = build_header(header_frag, rel, html)
        html = HEADER_RE.sub(header, html, count=1)
    else:
        print("  警告: <header class=\"site-header\"> が見つかりません", file=sys.stderr)
    if FOOTER_RE.search(html):
        html = FOOTER_RE.sub(footer_frag, html, count=1)
    return html


def footer_inner(footer_frag: str) -> str:
    m = re.search(r"<footer[^>]*>([\s\S]*)</footer>", footer_frag)
    if not m:
        raise RuntimeError("kit-footer.fragment.html の形式が不正です")
    return m.group(1).strip()


def write_docs_footer(footer_frag: str) -> None:
    inner = footer_inner(footer_frag)
    body = f"""{{#- website/kit-footer.fragment.html から生成（install_kit_chrome.py）-#}}
<footer class="site-footer kit-docs-footer">
  <div class="shell">
{inner}
  </div>
</footer>
"""
    DOCS_FOOTER.write_text(body, encoding="utf-8")


def main() -> int:
    if not HEADER_PATH.is_file() or not FOOTER_PATH.is_file():
        print("fragment が見つかりません", file=sys.stderr)
        return 1

    header_frag = load_header_fragment()
    footer_frag = load_footer_fragment()

    for rel in STATIC_PAGES:
        path = WEB / rel
        if not path.is_file():
            continue
        original = path.read_text(encoding="utf-8")
        patched = patch_page(original, header_frag, footer_frag, rel)
        path.write_text(patched, encoding="utf-8")
        print(f"chrome OK: website/{rel}")

    write_docs_footer(footer_frag)
    print(f"chrome OK: {DOCS_FOOTER.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())