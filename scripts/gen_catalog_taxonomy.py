#!/usr/bin/env python3
"""生成 kit Skill 收录分类 SSOT：website/content/catalog-taxonomy.zh.json

分类与 docs/PRODUCT-OVERVIEW.zh-CN.md「Skill 地图」对齐；skills 名单来自公开 wawoo-skills。
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parents[1]
OUT = KIT_ROOT / "website" / "content" / "catalog-taxonomy.zh.json"
_SCRIPTS = KIT_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
import oss_root  # noqa: E402


def _wawoo_root() -> Path:
    env = os.environ.get("WAWOO_SKILLS_ROOT", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    return oss_root.kit_oss_clone_root()


def _skill_names(wawoo: Path) -> list[str]:
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "gen_capabilities", wawoo / "scripts" / "gen_capabilities.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    mod.ROOT = wawoo
    mod.KILO = wawoo / ".kilo"
    mod.READINESS = wawoo / "scripts" / "readiness.json"
    needs = mod.load_readiness()
    return [x[0] for x in mod.collect("skills/*/SKILL.md", needs)]


def assign(name: str) -> str:
    if name.startswith("principle-"):
        return "principles"

    quality = {
        "code-review",
        "change-readiness",
        "code-skeptic",
        "test-engineering",
    }
    ui = {
        "accessibility-audit",
        "brand-guidelines",
        "design-brief",
        "design-md",
        "design-review",
        "fal-gen",
        "frontend-design",
        "frontend-guides-hub",
        "imagegen-frontend-mobile",
        "prototype",
        "reference-design-contract",
        "screenshots-marketing",
        "slides",
        "web-design-guidelines",
        "web-experience-design",
    }
    research = {
        "research",
        "research-decision-room",
        "product-discovery",
        "marketing-psychology",
        "viral-hooks",
        "writing-beats",
        "writing-fragments",
        "writing-shape",
        "science-writing",
        "copy-editing",
        "proofreading",
        "seo-writing",
    }
    security = {
        "security-review",
        "privacy-review",
        "compliance-legal",
        "content-guardrail",
        "data-egress-guard",
        "release-readiness",
    }
    ops = {
        "deployment",
        "incident-debugging",
        "performance-audit",
        "database-change-safety",
        "dependency-upgrade",
    }
    memory = {"memory", "context-compression"}
    planning = {
        "plan-md",
        "pdca-cycle",
        "architecture-decision",
        "domain-modeling",
        "grilling",
        "grill-with-docs",
        "handoff",
    }
    kit = {
        "language-policy",
        "documentation-localization",
        "writing-for-agents",
        "wawoo-oss-boundary",
        "publication-boundary",
        "modern-web-guidance-bridge",
        "legacy-web-scan",
        "git-identity",
        "openrouter-gen",
        "ask-matt",
        "wayfinder",
        "setup-matt-pocock-skills",
        "triage",
        "to-tickets",
        "to-spec",
    }
    engineering = {
        "tdd",
        "implement",
        "implement-spec",
        "diagnosing-bugs",
        "engineering-quality",
        "api-contract-design",
        "codebase-design",
        "create-verification-skill",
        "maintain-verification-skill",
        "benchmark-checklist",
        "blast-radius",
        "figure-it-out",
        "pr",
        "retro",
        "changelog",
        "how",
        "why",
        "recall",
        "reflect",
        "show-me-your-work",
        "swarm",
        "teach",
        "sharpen",
        "in-your-own-words",
    }

    for bucket, names in (
        ("quality", quality),
        ("ui", ui),
        ("research", research),
        ("security", security),
        ("ops", ops),
        ("memory", memory),
        ("planning", planning),
        ("kit", kit),
        ("engineering", engineering),
    ):
        if name in names:
            return bucket
    return "engineering"


def main() -> None:
    wawoo = _wawoo_root()
    names = sorted(_skill_names(wawoo))
    buckets: dict[str, list[str]] = {
        "engineering": [],
        "quality": [],
        "ui": [],
        "research": [],
        "security": [],
        "ops": [],
        "planning": [],
        "memory": [],
        "principles": [],
        "kit": [],
    }
    for n in names:
        buckets[assign(n)].append(n)

    meta = {
        "_note": "Skill 收录分组 SSOT。与 docs/PRODUCT-OVERVIEW.zh-CN.md 地图一致；名单来自公开 wawoo-skills。",
        "order": [
            "engineering",
            "quality",
            "ui",
            "research",
            "security",
            "ops",
            "planning",
            "memory",
            "principles",
            "kit",
        ],
        "sections": {
            "engineering": {
                "title": "工程实现",
                "title_en": "Engineering",
                "lead": "写功能、修缺陷、做规格与可验证交付（常配合 /delivery-lite、/feature-delivery）。",
            },
            "quality": {
                "title": "质量评审",
                "title_en": "Quality review",
                "lead": "合并前与设计阶段的证据化评审（常配合 /self-review）。",
            },
            "ui": {
                "title": "UI · 前端 · 设计",
                "title_en": "UI & design",
                "lead": "界面实现、设计审稿与可访问性（常配合 /ui-delivery、/design-review）。",
            },
            "research": {
                "title": "调研 · 文案 · 市场",
                "title_en": "Research & copy",
                "lead": "调研决策、文章与市场叙事（常配合 /research、/market-plan、/writing）。",
            },
            "security": {
                "title": "安全 · 隐私 · 合规",
                "title_en": "Security & compliance",
                "lead": "发布前与外发内容的门禁（常配合 /compliance-review、/release-review）。",
            },
            "ops": {
                "title": "运维 · 发布 · 性能",
                "title_en": "Ops & release",
                "lead": "部署、依赖升级、性能与线上事故（常配合 /incident-response）。",
            },
            "planning": {
                "title": "规划 · 架构 · 文档",
                "title_en": "Planning & architecture",
                "lead": "计划落盘、架构决策与需求澄清。",
            },
            "memory": {
                "title": "记忆 · 上下文",
                "title_en": "Memory & context",
                "lead": "跨会话记忆与长上下文压缩（各 workflow 入口常用）。",
            },
            "principles": {
                "title": "工程原则（principle-*）",
                "title_en": "principle-*",
                "lead": "短纪律 skill，按需每次只开 1～2 个，勿整族灌进上下文。",
            },
            "kit": {
                "title": "套件基座",
                "title_en": "Kit platform",
                "lead": "路由、边界、桥接与维护本技能库的 meta skill。",
            },
        },
        "assignments": buckets,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(KIT_ROOT)} ({len(names)} skills)")


if __name__ == "__main__":
    main()