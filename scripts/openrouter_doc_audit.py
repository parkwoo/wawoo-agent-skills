#!/usr/bin/env python3
"""OpenRouter で公開 kit ドキュメントを監査（キーは環境変数のみ）。"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = os.environ.get("OPENROUTER_DOC_MODEL", "google/gemini-2.5-flash")
API_URL = "https://openrouter.ai/api/v1/chat/completions"


def load_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if key:
        return key
    for candidate in (
        Path("/home/git/zen-router/.env"),
        Path("/home/git/zen-workflow/.env"),
    ):
        if not candidate.is_file():
            continue
        for line in candidate.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("OPENROUTER_API_KEY=") and not line.strip().startswith("#"):
                val = line.split("=", 1)[1].strip().strip('"')
                if val:
                    return val
    return ""


def chat(api_key: str, system: str, user: str, model: str) -> str:
    body = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.35,
            "max_tokens": 16000,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/parkwoo/wawoo-skills",
            "X-Title": "wawoo-skills-public-doc-audit",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=240) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def main() -> int:
    api_key = load_key()
    if not api_key:
        print("OPENROUTER_API_KEY not set", file=sys.stderr)
        return 1

    caps = (ROOT / ".kilo/CAPABILITIES.md").read_text(encoding="utf-8").splitlines()[:8]
    inventory = "\n".join(caps)

    paths = [
        ROOT / "docs/PRODUCT-OVERVIEW.md",
        ROOT / "docs/PRODUCT-OVERVIEW.ja.md",
        ROOT / "README.md",
        ROOT / "README.ja.md",
        ROOT / "docs/GUIDES.md",
        ROOT / "docs/GUIDES.ja.md",
        ROOT / "docs/USAGE.md",
        ROOT / "docs/USAGE.ja.md",
    ]
    chunks = []
    for p in paths:
        if p.is_file():
            chunks.append(f"=== {p.relative_to(ROOT)} ===\n{p.read_text(encoding='utf-8')}")

    system = """You audit PUBLIC open-source docs for github.com/parkwoo/wawoo-skills.

HARD FACTS (never change):
- Product-neutral kit only. NO project-specific or private skills (no kiun, paseo, nextwave, platform-ops).
- Inventory: skills=97, agents=21, workflows=12 (from gen_capabilities.py / CAPABILITIES.md).
- MCP means Model Context Protocol (NOT "Managed Capability Provider").
- Workflows are exactly the 12 in CAPABILITIES.md Workflows section.

Goals: (1) non-engineers understand in 60s what the product is, (2) engineers see MCP/workflows accurately, (3) GitHub/README SEO with natural keywords (AI coding agent, MCP, Cursor, Kilo, skills, workflows, intent routing).

Output ONLY valid JSON (no markdown fence) with keys:
- audit_issues: [{id, severity, file, problem, fix}]
- seo_keywords_en: string[8-12]
- seo_keywords_ja: string[8-12]
- revised_product_overview_en: full PRODUCT-OVERVIEW.md — lead with one concrete before/after example; ## Who this is for (3 bullets); FAQ; all 12 workflows; SEO <!-- --> comment ≤155 chars
- revised_product_overview_ja: full PRODUCT-OVERVIEW.ja.md (Japanese only in body; same sections)
- revised_guides_en: full GUIDES.md (table with one-line plain descriptions)
- revised_guides_ja: full GUIDES.ja.md
- readme_patch_en: {replace_after_tagline: markdown block through FAQ, max 12 lines plus link to PRODUCT-OVERVIEW — no duplicate long FAQ}
- readme_patch_ja: same for README.ja.md
- seo_title_en, seo_title_ja: GitHub About (~120 chars)
"""

    user = f"""CAPABILITIES header:
{inventory}

Documents:
{''.join(chunks)}
"""

    out = ROOT / "docs/evidence/product-overview-gemini-audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        raw = chat(api_key, system, user, DEFAULT_MODEL)
    except urllib.error.HTTPError as e:
        print(e.read().decode("utf-8", errors="replace")[:2500], file=sys.stderr)
        return 2

    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if "```" in text:
            text = text.rsplit("```", 1)[0].strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        (out.parent / "product-overview-gemini-audit.raw.txt").write_text(raw, encoding="utf-8")
        print("JSON parse failed; raw saved", file=sys.stderr)
        return 3

    out.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out)
    print("issues:", len(parsed.get("audit_issues", [])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())