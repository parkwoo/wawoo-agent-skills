#!/usr/bin/env python3
"""Skill 收录：GitHub parkwoo/wawoo-agent-skills の CAPABILITIES.md → docs/skills-catalog + JSON。

正本（厳守）: https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/CAPABILITIES.md  
（构建时 raw 拉取，不读 workspace/skills 或本机 clone，除非 KIT_CATALOG_SOURCE=local）

中文说明: website/content/guides.i18n.json（英文来自 GitHub CAPABILITIES）。

执行: WAWOO_SKILLS_GIT_REF=master python3 scripts/gen_site_capabilities_json.py
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
import oss_root  # noqa: E402
import wawoo_capabilities_github as gh  # noqa: E402

KIT_ROOT = Path(__file__).resolve().parents[1]
WEB = KIT_ROOT / "website"
OUT_JSON = WEB / "content" / "capabilities.catalog.json"
METRICS = WEB / "content" / "site-metrics.json"
I18N_JSON = WEB / "content" / "guides.i18n.json"
PAGE_JSON = WEB / "content" / "skills-catalog.page.json"
BUCKETS_JSON = WEB / "content" / "catalog-skill-buckets.json"
DOCS_DIR = KIT_ROOT / "docs"

# workspace 専用 skill（公開 kit に載せたら即失敗）
_FORBIDDEN_PUBLIC_NAMES = frozenset(
    {
        "paseo-orchestration",
        "kiun-report-corpus",
        "kiun-corpus-auditor",
        "kiun-corpus-wave",
        "nextwave-catalog-bridge",
        "wawoo-tools-stg-dagu-test",
        "git-identity",
    }
)


def _wawoo_skills_root() -> Path:
    """仅 KIT_CATALOG_SOURCE=local 时使用。"""
    env = os.environ.get("WAWOO_SKILLS_ROOT", "").strip()
    if env:
        root = Path(env).expanduser().resolve()
    else:
        root = oss_root.kit_oss_clone_root()
    if not (root / ".kilo").is_dir():
        raise SystemExit(f"WAWOO_KIT_OSS_ROOT 无效: {root}")
    return root


def _load_gen_capabilities(wawoo_root: Path):
    path = wawoo_root / "scripts" / "gen_capabilities.py"
    if not path.is_file():
        raise SystemExit(f"wawoo-skills に gen_capabilities.py がありません: {path}")
    spec = importlib.util.spec_from_file_location("gen_capabilities", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("gen_capabilities.py を読み込めません")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.ROOT = wawoo_root
    mod.KILO = wawoo_root / ".kilo"
    mod.READINESS = wawoo_root / "scripts" / "readiness.json"
    return mod


def _load_page_copy(locale: str) -> dict:
    if not PAGE_JSON.is_file():
        return {}
    data = json.loads(PAGE_JSON.read_text(encoding="utf-8"))
    block = data.get(locale)
    return block if isinstance(block, dict) else {}


def _page_sub(text: str, catalog: dict) -> str:
    c = catalog["counts"]
    return (
        text.replace("{{skills}}", str(c["skills"]))
        .replace("{{agents}}", str(c["agents"]))
        .replace("{{workflows}}", str(c["workflows"]))
        .replace("{{generated_at}}", catalog.get("generated_at", ""))
        .replace("{{capabilities_url}}", catalog.get("capabilities_md", ""))
    )


def _load_guides_i18n() -> dict[str, dict]:
    if not I18N_JSON.is_file():
        return {}
    try:
        data = json.loads(I18N_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"guides.i18n.json が壊れています: {e}") from e
    items = data.get("items")
    return items if isinstance(items, dict) else {}


def _item_i18n_key(name: str) -> str:
    return name.lstrip("/")


def _description_for_locale(name: str, default: str, locale: str, i18n: dict[str, dict]) -> str:
    entry = i18n.get(_item_i18n_key(name)) or i18n.get(name)
    if entry:
        localized = entry.get(locale)
        if isinstance(localized, str) and localized.strip():
            return localized.strip()
    if locale == "en":
        return default
    # zh/ja/ko：CAPABILITIES 仅英文，应由 guides.i18n.json 提供译文
    return default


def _load_skill_buckets() -> dict:
    if not BUCKETS_JSON.is_file():
        raise SystemExit(
            f"缺少 {BUCKETS_JSON.relative_to(KIT_ROOT)}。"
            "请先运行: WAWOO_SKILLS_ROOT=… python3 scripts/gen_catalog_skill_buckets.py"
        )
    data = json.loads(BUCKETS_JSON.read_text(encoding="utf-8"))
    return data


# 収録ページは Workflow / Agent / Skill の 3 層のみ（細分 bucket は TOC を汚すので載せない）
CATALOG_TIERS: dict[str, dict[str, tuple[str, str]]] = {
    "zh": {
        "workflows": (
            "工作流",
            "以 <code>/</code> 开头的入口命令；在客户端用自然语言触发 <code>workflow_get</code>。",
        ),
        "agents": (
            "Agent 角色",
            "工作流或 MCP 指定的执行视角；通常不必逐个打开。",
        ),
        "skills": (
            "Skill 技能",
            "工作流正文点名后再 <code>skill_get</code>；按名称字母序。",
        ),
    },
    "en": {
        "workflows": (
            "Workflows",
            "Entry commands (<code>/…</code>). Trigger with <code>workflow_get</code>.",
        ),
        "agents": (
            "Agent roles",
            "Personas chosen by workflows or MCP.",
        ),
        "skills": (
            "Skills",
            "<code>skill_get</code> when named; sorted A–Z.",
        ),
    },
    "ja": {
        "workflows": ("Workflow", "<code>workflow_get</code> で起動する <code>/</code> 入口。"),
        "agents": ("Agent", "ワークフローが指す実行視点。"),
        "skills": ("Skill", "指されたときだけ <code>skill_get</code>。"),
    },
    "ko": {
        "workflows": ("Workflow", "<code>workflow_get</code> 진입 명령."),
        "agents": ("Agent", "Workflow가 지정하는 역할."),
        "skills": ("Skill", "지명 시 <code>skill_get</code>."),
    },
}

BUCKET_LEADS: dict[str, dict[str, str]] = {
    "zh": {
        "engineering": "写功能、补缺陷、做规格与实现验证。",
        "quality": "合并前评审、测试策略与改动手递。",
        "ui": "界面实现、设计审稿、可访问性与视觉资产。",
        "research": "调研、市场叙事、长文与创意写作。",
        "security": "安全/隐私/合规审查与外发内容守门。",
        "ops": "部署、依赖、数据库与线上故障。",
        "docs": "计划文档、changelog 与本地化。",
        "memory": "跨会话记忆、上下文压缩与会话交接。",
        "principles": "按需加载的短纪律 skill（principle-*）。",
        "platform": "套件路由、边界、桥接与协作辅助。",
    },
    "en": {
        "engineering": "Specs, implementation, defects, and verification.",
        "quality": "Review, testing, and handoff before merge.",
        "ui": "UI implementation, design review, and a11y.",
        "research": "Research, copy, and creative writing.",
        "security": "Security, privacy, compliance, and egress guards.",
        "ops": "Deploy, dependencies, data, and incidents.",
        "docs": "Plans, changelogs, and documentation.",
        "memory": "Memory, context compression, handoffs.",
        "principles": "Short discipline skills (principle-*).",
        "platform": "Kit routing, boundaries, and bridges.",
    },
}


def _catalog_tiers(locale: str) -> dict[str, tuple[str, str]]:
    return CATALOG_TIERS.get(locale) or CATALOG_TIERS["en"]


def _render_tier_guide(page: dict, locale: str) -> list[str]:
    body = page.get("tier_guide")
    if not body:
        body = {
            "zh": (
                "| 类型 | 是什么 | 何时用 |\n| --- | --- | --- |\n"
                "| **Workflow** | 固定步骤的流程入口（<code>/delivery-lite</code> 等） | 先对齐「我在做哪类事」 |\n"
                "| **Agent** | 角色视角（审代码、做 UI…） | 一般由工作流或 MCP 指定 |\n"
                "| **Skill** | 单份 SKILL.md 操作说明 | 正文点名后再 <code>skill_get</code> |"
            ),
            "en": (
                "| Kind | What | When |\n| --- | --- | --- |\n"
                "| **Workflow** | Process entry (<code>/…</code>) | Pick task shape first |\n"
                "| **Agent** | Persona | Usually from the flow |\n"
                "| **Skill** | One playbook | <code>skill_get</code> when named |"
            ),
        }.get(locale, "")
    title = page.get("tier_guide_title") or {
        "zh": "三类能力怎么区分",
        "en": "Workflow vs Agent vs Skill",
        "ja": "3 種類の見分け方",
        "ko": "3가지 구분",
    }.get(locale, "")
    if not body:
        return []
    summary = {"zh": "展开对照表", "en": "Show comparison", "ja": "一覧を開く", "ko": "표 펼치기"}.get(locale, "…")
    return [
        '<details class="kit-catalog-tier-details">',
        f"<summary>{_esc(title)}（{summary}）</summary>",
        "",
        '<div class="kit-catalog-tier-guide" markdown="1">',
        "",
        body,
        "",
        "</div>",
        "",
        "</details>",
        "",
    ]


def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _one_line(s: str, n: int = 80) -> str:
    s = re.sub(r"\s+", " ", (s or "").strip())
    return s if len(s) <= n else s[: n - 1] + "…"


def _strip_md_bold(text: str) -> str:
    return re.sub(r"\*\*([^*]+)\*\*", r"\1", text or "")


def _inline_md_links_to_html(text: str) -> str:
    """`<p>` 内では Markdown が効かないため、[text](url) を <a> に変換する。"""
    def _link(m: re.Match[str]) -> str:
        label = _esc(m.group(1))
        href = _esc(m.group(2))
        return f'<a href="{href}" target="_blank" rel="noopener noreferrer">{label}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link, text)


def _guard_public_only(skills: list, agents: list, workflows: list) -> None:
    names = {s["name"] for s in skills} | {a["name"] for a in agents} | {w["id"] for w in workflows}
    leaked = sorted(names & _FORBIDDEN_PUBLIC_NAMES)
    if leaked:
        raise SystemExit(
            "公開 kit に workspace 専用 skill が含まれています。"
            f" WAWOO_SKILLS_ROOT を公開 wawoo-skills にしてください: {', '.join(leaked)}"
        )


def _build_catalog_local() -> tuple[list[dict], list[dict], list[dict]]:
    wawoo_root = _wawoo_skills_root()
    gen = _load_gen_capabilities(wawoo_root)
    needs = gen.load_readiness()
    skills_raw = gen.collect("skills/*/SKILL.md", needs)
    agents_raw = gen.collect("agents/*.md", needs)
    workflows_raw = gen.collect("commands/*.md", needs)

    ref = gh.git_ref()
    skills = []
    for n, r, note, desc, p in skills_raw:
        skills.append(
            {
                "name": n,
                "ready": bool(r),
                "ready_label": "✅" if r else f"⚠️ {note}",
                "size_kb": None,
                "description": desc,
                "path": p,
                "url": gh.github_blob_href(p, ref),
            }
        )
    agents = [
        {"name": n, "description": d, "path": p, "url": gh.github_blob_href(p, ref)}
        for n, _r, _n, d, p in agents_raw
    ]
    workflows = []
    for n, _r, _note, desc, p in workflows_raw:
        cmd = n if n.startswith("/") else f"/{n}"
        workflows.append(
            {
                "name": cmd,
                "id": n,
                "description": desc,
                "path": p,
                "url": gh.github_blob_href(p, ref),
            }
        )
    return skills, agents, workflows


def build_catalog() -> dict:
    source = (os.environ.get("KIT_CATALOG_SOURCE") or "github").strip().lower()
    ref = gh.git_ref()

    if source == "local":
        skills, agents, workflows = _build_catalog_local()
        source_root = str(_wawoo_skills_root())
        capabilities_url = gh.capabilities_blob_url(ref)
        raw_url = gh.capabilities_raw_url(ref)
    else:
        text, raw_url = gh.fetch_capabilities_md(ref)
        skills, agents, workflows = gh.parse_capabilities_md(text, ref=ref)
        source_root = f"https://github.com/{gh.GITHUB_REPO}/tree/{ref}"
        capabilities_url = gh.capabilities_blob_url(ref)

    if not skills:
        raise SystemExit(f"GitHub CAPABILITIES 解析失败（skills=0）: {raw_url}")

    _guard_public_only(skills, agents, workflows)

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    counts = {"skills": len(skills), "agents": len(agents), "workflows": len(workflows)}

    return {
        "generated_at": now,
        "source": source,
        "git_ref": ref,
        "source_root": source_root,
        "capabilities_raw": raw_url,
        "capabilities_md": capabilities_url,
        "counts": counts,
        "skills": skills,
        "agents": agents,
        "workflows": workflows,
    }


LOCALES = {
    "zh": {
        "suffix": "",
        "doc_prefix": "/cn/docs/skills-catalog/",
        "title": "Skill 收录 — 全量能力与 CAPABILITIES 同步",
        "description": "全部 Skill、Agent、Workflow，与 CAPABILITIES.md 一致。",
        "hero": "Skill 收录",
        "hero_lead": "与[使用说明](usage.md)相同文档版式；数量与 [GitHub CAPABILITIES.md](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/CAPABILITIES.md) 一致。共 {{skills}} Skills · {{agents}} Agents · {{workflows}} Workflows。",
        "info": "先选 **Workflow**，点到再 `skill_get`。说明列：英文正本在 CAPABILITIES，**简体中文见 guides.i18n.json**（构建时写入本页）。",
        "table_name": "名称",
        "table_desc": "说明（简体中文）",
        "built": "生成时间",
        "lang_links": (
            '<a href="/en/docs/skills-catalog/">English</a>\n'
            '  <span aria-hidden="true">·</span>\n'
            '  <a href="/ja/docs/skills-catalog/">日本語</a>\n'
            '  <span aria-hidden="true">·</span>\n'
            '  <a href="/ko/docs/skills-catalog/">한국어</a>\n'
            '  <span aria-hidden="true">·</span>\n'
            "  <strong>简体中文</strong>"
        ),
    },
    "en": {
        "suffix": ".en",
        "doc_prefix": "/en/docs/skills-catalog/",
        "title": "Skills catalog — synced with CAPABILITIES.md",
        "description": "Full Skills, Agents, and Workflows index.",
        "hero": "Skills catalog",
        "hero_lead": "Same layout as the [usage manual](usage.md); counts match [GitHub CAPABILITIES.md](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/CAPABILITIES.md). {{skills}} skills · {{agents}} agents · {{workflows}} workflows.",
        "info": "Choose a **Workflow** first; `skill_get` only what the flow names.",
        "table_name": "Name",
        "table_desc": "Description (wawoo-skills frontmatter / CAPABILITIES)",
        "built": "Generated",
        "lang_links": (
            '<a href="/cn/docs/skills-catalog/">简体中文</a>\n'
            '  <span aria-hidden="true">·</span>\n'
            '  <strong>English</strong>\n'
            '  <span aria-hidden="true">·</span>\n'
            '  <a href="/ja/docs/skills-catalog/">日本語</a>\n'
            '  <span aria-hidden="true">·</span>\n'
            '  <a href="/ko/docs/skills-catalog/">한국어</a>'
        ),
    },
    "ja": {
        "suffix": ".ja",
        "doc_prefix": "/ja/docs/skills-catalog/",
        "title": "Skill 収録 — CAPABILITIES と同期",
        "description": "Skill・Agent・Workflow の全一覧。",
        "hero": "Skill 収録",
        "hero_lead": "[利用ガイド](usage.md)と同じ版式（[GitHub CAPABILITIES](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/CAPABILITIES.md) と同期）。{{skills}} Skills · {{agents}} Agents · {{workflows}} Workflows。",
        "info": "先に **Workflow** を選び、本文で指された skill だけ skill_get。",
        "table_name": "名前",
        "table_desc": "説明",
        "built": "生成",
        "lang_links": (
            '<a href="/cn/docs/skills-catalog/">简体中文</a>\n'
            '  <span aria-hidden="true">·</span>\n'
            '  <a href="/en/docs/skills-catalog/">English</a>\n'
            '  <span aria-hidden="true">·</span>\n'
            '  <strong>日本語</strong>\n'
            '  <span aria-hidden="true">·</span>\n'
            '  <a href="/ko/docs/skills-catalog/">한국어</a>'
        ),
    },
    "ko": {
        "suffix": ".ko",
        "doc_prefix": "/ko/docs/skills-catalog/",
        "title": "Skill 수록 — CAPABILITIES 동기화",
        "description": "Skill·Agent·Workflow 전체 목록.",
        "hero": "Skill 수록",
        "hero_lead": "[사용 설명](usage.md)과 같은 문서 형식 ([GitHub CAPABILITIES](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/CAPABILITIES.md) 동기화). {{skills}} Skills · {{agents}} Agents · {{workflows}} Workflows.",
        "info": "먼저 **Workflow**를 고르고, flow에서 지정한 skill만 skill_get.",
        "table_name": "이름",
        "table_desc": "설명",
        "built": "생성 시각",
        "lang_links": (
            '<a href="/cn/docs/skills-catalog/">简体中文</a>\n'
            '  <span aria-hidden="true">·</span>\n'
            '  <a href="/en/docs/skills-catalog/">English</a>\n'
            '  <span aria-hidden="true">·</span>\n'
            '  <a href="/ja/docs/skills-catalog/">日本語</a>\n'
            '  <span aria-hidden="true">·</span>\n'
            '  <strong>한국어</strong>'
        ),
    },
}


def _md_cell(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ")


def _md_table_rows(
    items: list[dict],
    t_name: str,
    t_desc: str,
    *,
    show_skill_size: bool = False,
) -> list[str]:
    rows = [
        f'<div class="kit-catalog-table" markdown="1">\n\n',
        f"| {t_name} | {t_desc} |",
        "| --- | --- |",
    ]
    for it in sorted(items, key=lambda x: x["name"].lower()):
        name = it["name"]
        extra = ""
        if it.get("ready") is False:
            extra = " ⚠️"
        if show_skill_size:
            skb = it.get("size_kb")
            if skb is not None and "/skills/" in str(it.get("path", "")):
                extra = f" · {skb}KB{extra}"
        link = f"[`{name}`]({it['url']})"
        desc = _md_cell(_one_line(it.get("description", ""), 220)) + extra
        rows.append(f"| {link} | {desc} |")
    rows.append("\n</div>\n")
    return rows


def _render_highlights(page: dict) -> list[str]:
    title = page.get("highlights_title") or ""
    cards = page.get("highlights") or []
    if not cards:
        return []
    out = [
        f'<p class="kit-catalog-subhead"><strong>{_esc(title)}</strong></p>',
        "",
        '<div class="kit-catalog-highlights" markdown="1">',
        "",
    ]
    for card in cards:
        name = _esc(str(card.get("name", "")))
        body = re.sub(r"`([^`]+)`", r"<code>\1</code>", str(card.get("body", "")))
        out.append(f'<article class="kit-catalog-highlight"><strong>{name}</strong><p>{body}</p></article>')
        out.append("")
    out.append("</div>")
    out.append("")
    return out


def _render_quickref(page: dict, locale: str) -> list[str]:
    title = page.get("quickref_title") or ""
    rows = page.get("quickref") or []
    if not rows:
        return []
    cols = page.get("quickref_columns")
    if not isinstance(cols, list) or len(cols) != 3:
        cols = {
            "zh": ["场景", "工作流", "可复制的一句"],
            "en": ["Task", "Workflow", "Try saying"],
            "ja": ["シーン", "Workflow", "コピー用"],
            "ko": ["상황", "Workflow", "복사 문장"],
        }[locale]
    out = [
        f'<p class="kit-catalog-subhead"><strong>{_esc(title)}</strong></p>',
        "",
        '<div class="kit-catalog-quickref" markdown="1">',
        "",
        f"| {cols[0]} | {cols[1]} | {cols[2]} |",
        "| --- | --- | --- |",
    ]
    for row in rows:
        task = _md_cell(str(row.get("task", "")))
        wf = str(row.get("workflow", ""))
        copy = _esc(str(row.get("copy", "")))
        out.append(
            f"| {task} | `{wf}` | "
            f'<code class="kit-catalog-copy" data-kit-copy-cmd="{copy}">{copy}</code> |'
        )
    out.append("")
    out.append("</div>")
    out.append("")
    return out


def _with_locale_descriptions(items: list[dict], locale: str, i18n: dict[str, dict]) -> list[dict]:
    out: list[dict] = []
    for it in items:
        row = dict(it)
        row["description"] = _description_for_locale(
            it["name"], it.get("description", ""), locale, i18n
        )
        out.append(row)
    return out


def build_catalog_markdown(catalog: dict, locale: str, i18n: dict[str, dict]) -> str:
    meta = LOCALES[locale]
    page = _load_page_copy(locale)
    c = catalog["counts"]
    tiers = _catalog_tiers(locale)
    cap = catalog["capabilities_md"]

    title = _page_sub(page.get("title") or meta["title"], catalog)
    description = _page_sub(page.get("description") or meta["description"], catalog)
    hero_title = page.get("hero_title") or meta["hero"]
    hero_line1 = _strip_md_bold(page.get("hero_line1") or meta["info"])
    hero_line2 = page.get("hero_line2") or ""
    hero_example = page.get("hero_example") or ""
    hero_counts_raw = _page_sub(
        page.get("hero_counts")
        or meta["hero_lead"]
        .replace("{{skills}}", str(c["skills"]))
        .replace("{{agents}}", str(c["agents"]))
        .replace("{{workflows}}", str(c["workflows"])),
        catalog,
    )
    hero_counts = _inline_md_links_to_html(hero_counts_raw)

    parts = [
        "---",
        f"title: {title}",
        f"description: {description}",
        "hide:",
        "  - title",
        "  - navigation",
        "---",
        "",
        '<div class="kit-catalog-root" markdown="1">',
        "",
        '<div class="kit-catalog-hero" markdown="0">',
        "",
        f'<p class="kit-catalog-title">{_esc(hero_title)}</p>',
        f'<p class="kit-catalog-lead">{_esc(hero_line1)}</p>',
    ]
    if hero_line2:
        parts.append(f'<p class="kit-catalog-usage">{hero_line2}</p>')
    if hero_example:
        parts.append(f'<p class="kit-catalog-example">{_inline_md_links_to_html(hero_example)}</p>')
    parts.extend(
        [
            f'<p class="kit-catalog-hero-counts">{hero_counts}</p>',
            '<div class="kit-catalog-hero-meta">',
            '<div class="kit-doc-langs">',
            meta["lang_links"],
            "</div>",
            "</div>",
            "</div>",
            "",
        ]
    )
    wf = _with_locale_descriptions(catalog["workflows"], locale, i18n)
    ag = _with_locale_descriptions(catalog["agents"], locale, i18n)
    sk = _with_locale_descriptions(catalog["skills"], locale, i18n)

    tier_ids = ("workflows", "agents", "skills")
    slug = {"workflows": "cat-workflows", "agents": "cat-agents", "skills": "cat-skills"}

    for tier_id in tier_ids:
        items = wf if tier_id == "workflows" else ag if tier_id == "agents" else sk
        if not items:
            continue
        title_sec, lead = tiers[tier_id]
        parts.append(
            f'<h2 class="kit-catalog-tier" id="{slug[tier_id]}">{_esc(title_sec)}（{len(items)}）</h2>'
        )
        parts.append("")
        if lead:
            parts.append(f'<p class="kit-catalog-tier-lead">{lead}</p>')
            parts.append("")
        parts.extend(_md_table_rows(items, meta["table_name"], meta["table_desc"]))
        parts.append("")

    parts.extend(_render_quickref(page, locale))
    parts.extend(_render_tier_guide(page, locale))
    parts.extend(_render_highlights(page))

    footer_meta = _page_sub(page.get("footer_meta") or f"_{meta['built']}: {{generated_at}}_", catalog)
    footer_links = _page_sub(page.get("footer_links") or "", catalog)
    parts.extend(
        [
            '<p class="kit-catalog-footer">',
            footer_meta,
            footer_links,
            "</p>",
            "",
            "</div>",
            "",
        ]
    )

    return "\n".join(parts).strip() + "\n"


def write_skills_catalog_docs(catalog: dict, i18n: dict[str, dict]) -> None:
    for loc, meta in LOCALES.items():
        fname = f"skills-catalog{meta['suffix']}.md"
        path = DOCS_DIR / fname
        path.write_text(build_catalog_markdown(catalog, loc, i18n), encoding="utf-8")


def write_guides_redirect() -> None:
    for loc, meta in LOCALES.items():
        target = meta["doc_prefix"]
        rel = WEB / "guides" / "index.html" if loc == "zh" else WEB / loc / "guides" / "index.html"
        rel.parent.mkdir(parents=True, exist_ok=True)
        rel.write_text(
            f"""<!DOCTYPE html>
<html lang="{loc}">
<head>
<meta charset="utf-8" />
<meta http-equiv="refresh" content="0;url={target}" />
<link rel="canonical" href="https://skills.wawoo.jp{target}" />
<script>location.replace("{target}");</script>
<title>Redirect</title>
</head>
<body><p><a href="{target}">Skills catalog</a></p></body>
</html>
""",
            encoding="utf-8",
        )


def sync_site_metrics(counts: dict[str, int]) -> None:
    if not METRICS.is_file():
        return
    data = json.loads(METRICS.read_text(encoding="utf-8"))
    c = data.setdefault("counts", {})
    c["skills"] = counts["skills"]
    c["agent_roles"] = counts["agents"]
    c["workflows"] = counts["workflows"]
    METRICS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _catalog_item_keys(catalog: dict) -> list[str]:
    keys: list[str] = []
    for s in catalog["skills"]:
        keys.append(s["name"])
    for a in catalog["agents"]:
        keys.append(a["name"])
    for w in catalog["workflows"]:
        keys.append(w["name"])
    return keys


def _ensure_zh_translations(catalog: dict, i18n: dict[str, dict]) -> None:
    if os.environ.get("KIT_CATALOG_SKIP_ZH_CHECK") == "1":
        return
    missing: list[str] = []
    for key in _catalog_item_keys(catalog):
        entry = i18n.get(key) or i18n.get(_item_i18n_key(key))
        zh = (entry or {}).get("zh") if isinstance(entry, dict) else None
        if not (isinstance(zh, str) and zh.strip()):
            missing.append(key)
    if missing:
        raise SystemExit(
            "简体中文说明未齐：CAPABILITIES 只有英文，须先翻译到 guides.i18n.json。\n"
            "  WAWOO_SKILLS_ROOT=/path/to/wawoo-skills "
            "GUIDES_I18N_PROVIDER=mymemory python3 scripts/guides_i18n_sync_zh.py\n"
            f"  缺失 {len(missing)} 条，例如: {', '.join(missing[:8])}"
        )


def main() -> None:
    catalog = build_catalog()
    i18n = _load_guides_i18n()
    _ensure_zh_translations(catalog, i18n)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sync_site_metrics(catalog["counts"])
    write_skills_catalog_docs(catalog, i18n)
    write_guides_redirect()
    print(
        f"wrote docs/skills-catalog*.md + redirects "
        f"(source={catalog.get('source_root')}): "
        f"skills={catalog['counts']['skills']} agents={catalog['counts']['agents']} "
        f"workflows={catalog['counts']['workflows']} "
        f"i18n_items={len(i18n)}"
    )


if __name__ == "__main__":
    main()