#!/usr/bin/env python3
"""Gemini 2.5 → Qwen 3 の二段監査（公開 repo の説明ドキュメント）。"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://openrouter.ai/api/v1/chat/completions"
GEMINI = os.environ.get("OPENROUTER_DOC_MODEL", "google/gemini-2.5-flash")
QWEN = os.environ.get("OPENROUTER_QWEN_MODEL", "qwen/qwen3-30b-a3b")


def load_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if key:
        return key
    for p in (Path("/home/git/zen-router/.env"), Path("/home/git/zen-workflow/.env")):
        if not p.is_file():
            continue
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("OPENROUTER_API_KEY=") and not line.startswith("#"):
                v = line.split("=", 1)[1].strip().strip('"')
                if v:
                    return v
    return ""


def chat(key: str, model: str, system: str, user: str) -> str:
    body = json.dumps(
        {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.3,
            "max_tokens": 20000,
        }
    ).encode()
    req = urllib.request.Request(
        API,
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/parkwoo/wawoo-skills",
            "X-Title": "wawoo-skills-doc-dual-audit",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]


def doc_bundle() -> str:
    globs = [
        "docs/GUIDES*.md",
        "docs/PRODUCT-OVERVIEW*.md",
        "docs/MEMORY-CLIENT-GUIDE*.md",
        "docs/CLIENT-INTEGRATION-GUIDE*.md",
        "docs/COPY-WRITING-GUIDE*.md",
        "README*.md",
    ]
    parts = []
    for pattern in globs:
        for p in sorted(ROOT.glob(pattern)):
            if "internal" in str(p):
                continue
            parts.append(f"=== {p.relative_to(ROOT)} ===\n{p.read_text(encoding='utf-8')[:12000]}")
    cap = (ROOT / ".kilo/CAPABILITIES.md").read_text(encoding="utf-8")[:2500]
    return f"CAPABILITIES excerpt:\n{cap}\n\n" + "\n".join(parts)


SYSTEM = """You audit wawoo-skills PUBLIC docs (github.com/parkwoo/wawoo-skills).

Facts: 97 skills, 21 agents, 12 workflows. Product-neutral. MCP = Model Context Protocol.
Paseo-style language bar on every user doc: [English](x.md) · [简体中文](x.zh-CN.md) · [日本語](x.ja.md) · [한국어](x.ko.md)
Public kit has NO /writing, /market-plan, no viral-hooks/marketing-psychology — COPY guide must only list skills that exist.

Checklist gaps to fix in your output:
- Memory: standalone MEMORY-CLIENT-GUIDE clear for first-time users (0 vs 1, install flags, verify)
- Missing cross-links between GUIDES, USAGE, memory
- Copy/docs: writing-for-agents, documentation-localization, docs-specialist, /research — readable tables
- SEO comments and plain-language leads

Return ONLY JSON:
{
  "auditor": "<model id>",
  "issues": [{"id","severity","file","problem","fix"}],
  "files": {"docs/RELATIVE_PATH.md": "full new markdown content", ...}
}
Only include files that need rewrite. English files in English; *.ja.md Japanese; *.zh-CN.md Simplified Chinese; *.ko.md Korean.
Do not invent skills not in CAPABILITIES."""


def parse_json(raw: str) -> dict:
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if "```" in text:
            text = text.rsplit("```", 1)[0]
    return json.loads(text.strip())


def main() -> int:
    key = load_key()
    if not key:
        print("no OPENROUTER_API_KEY", file=sys.stderr)
        return 1
    bundle = doc_bundle()
    out_dir = ROOT / "docs/evidence"
    out_dir.mkdir(parents=True, exist_ok=True)
    merged: dict = {"issues": [], "files": {}}

    for model in (GEMINI, QWEN):
        print("auditing with", model, flush=True)
        user = f"Second pass after prior edits.\n\n{bundle}"
        if merged["files"]:
            user += "\n\nPrior patches keys: " + ", ".join(merged["files"].keys())
        try:
            raw = chat(key, model, SYSTEM, user)
            data = parse_json(raw)
        except (urllib.error.HTTPError, json.JSONDecodeError) as e:
            (out_dir / f"audit-fail-{model.replace('/', '_')}.txt").write_text(str(e), encoding="utf-8")
            print("fail", model, e, file=sys.stderr)
            continue
        data["auditor"] = model
        (out_dir / f"audit-{model.replace('/', '_')}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        merged["issues"].extend(data.get("issues", []))
        for path, content in (data.get("files") or {}).items():
            if not path.startswith("docs/") and not path.startswith("README"):
                continue
            merged["files"][path] = content

    (out_dir / "audit-merged.json").write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    print("merged files:", len(merged["files"]), "issues:", len(merged["issues"]))

    for rel, content in merged["files"].items():
        dest = ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        print("wrote", rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())