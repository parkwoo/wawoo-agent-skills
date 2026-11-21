#!/usr/bin/env python3
"""生成公开 wawoo-skills 的 Skill 分类表（对齐 docs/PRODUCT-OVERVIEW.zh-CN.md 地图）。

输出: website/content/catalog-skill-buckets.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = KIT_ROOT / "scripts"
sys.path.insert(0, str(_SCRIPTS))
import wawoo_capabilities_github as gh  # noqa: E402
OUT = KIT_ROOT / "website" / "content" / "catalog-skill-buckets.json"

# 与 PRODUCT-OVERVIEW.zh-CN「Skill 地图」一致
BUCKET_NAMES = {
    "engineering": "工程实现",
    "quality": "质量评审",
    "ui": "UI / 前端",
    "research": "调研与文案",
    "security": "安全与法务",
    "ops": "运维与发布",
    "docs": "文档与计划",
    "memory": "记忆与上下文",
    "principles": "工程原则（principle-*）",
    "platform": "套件基座",
}

# 显式归属（其余 principle-* 自动归入 principles）
EXPLICIT: dict[str, set[str]] = {
    "engineering": {
        "to-spec",
        "to-tickets",
        "tdd",
        "implement",
        "implement-spec",
        "diagnosing-bugs",
        "engineering-quality",
        "codebase-design",
        "domain-modeling",
        "api-contract-design",
        "create-verification-skill",
        "maintain-verification-skill",
        "figure-it-out",
        "wayfinder",
        "setup-matt-pocock-skills",
        "architecture-decision",
        "benchmark-checklist",
        "blast-radius",
        "prototype",
    },
    "quality": {
        "code-review",
        "change-readiness",
        "test-engineering",
        "pr",
        "retro",
        "triage",
    },
    "ui": {
        "web-experience-design",
        "accessibility-audit",
        "frontend-design",
        "design-brief",
        "design-md",
        "design-review",
        "reference-design-contract",
        "brand-guidelines",
        "frontend-guides-hub",
        "fal-gen",
        "openrouter-gen",
        "imagegen-frontend-mobile",
        "screenshots-marketing",
        "web-design-guidelines",
    },
    "research": {
        "research",
        "research-decision-room",
        "product-discovery",
        "marketing-psychology",
        "viral-hooks",
        "science-writing",
        "writing-beats",
        "writing-fragments",
        "writing-shape",
        "slides",
        "grilling",
        "grill-with-docs",
    },
    "security": {
        "security-review",
        "privacy-review",
        "compliance-legal",
        "content-guardrail",
        "data-egress-guard",
        "release-readiness",
    },
    "ops": {
        "deployment",
        "incident-debugging",
        "performance-audit",
        "database-change-safety",
        "dependency-upgrade",
    },
    "docs": {
        "plan-md",
        "writing-for-agents",
        "documentation-localization",
        "changelog",
        "pdca-cycle",
    },
    "memory": {
        "memory",
        "context-compression",
        "handoff",
        "recall",
        "reflect",
    },
    "platform": {
        "language-policy",
        "wawoo-oss-boundary",
        "git-identity",
        "modern-web-guidance-bridge",
        "legacy-web-scan",
        "publication-boundary",
        "ask-matt",
        "how",
        "why",
        "teach",
        "sharpen",
        "swarm",
        "show-me-your-work",
        "in-your-own-words",
    },
}


def _all_skill_names() -> list[str]:
    text, _url = gh.fetch_capabilities_md()
    skills, _a, _w = gh.parse_capabilities_md(text)
    return [s["name"] for s in skills]


def main() -> None:
    names = _all_skill_names()
    reverse: dict[str, str] = {}
    for bucket, members in EXPLICIT.items():
        for n in members:
            reverse[n] = bucket

    mapping: dict[str, str] = {}
    unassigned: list[str] = []
    for n in names:
        if n.startswith("principle-"):
            mapping[n] = "principles"
            continue
        b = reverse.get(n)
        if b:
            mapping[n] = b
        else:
            unassigned.append(n)

    if unassigned:
        import os

        msg = "未分配（请补 EXPLICIT）: " + ", ".join(sorted(unassigned))
        if os.environ.get("KIT_BUCKETS_LENIENT", "").strip() in ("1", "true", "yes"):
            print("WARN:", msg, "→ platform に仮置き（KIT_BUCKETS_LENIENT）", file=sys.stderr)
            for n in unassigned:
                mapping[n] = "platform"
        else:
            print(msg, file=sys.stderr)
            sys.exit(1)

    payload = {
        "_note": "公开 wawoo-skills Skill 分类 SSOT，对齐 PRODUCT-OVERVIEW.zh-CN。由 gen_catalog_skill_buckets.py 生成。",
        "bucket_labels_zh": BUCKET_NAMES,
        "skill_order": [
            "workflows",
            "agents",
            "engineering",
            "quality",
            "ui",
            "research",
            "security",
            "ops",
            "docs",
            "memory",
            "principles",
            "platform",
        ],
        "skills": mapping,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(KIT_ROOT)} ({len(mapping)} skills)")


if __name__ == "__main__":
    main()