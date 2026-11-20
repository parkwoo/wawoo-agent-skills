#!/usr/bin/env python3
"""GitHub 公開倉の CAPABILITIES.md を収録正本として取得する。"""
from __future__ import annotations

import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
import oss_root  # noqa: E402

GITHUB_REPO = oss_root.PUBLIC_GITHUB_REPO
DEFAULT_REF = "master"
USER_AGENT = "wawoo-kit-catalog/1.0"


def git_ref() -> str:
    return (os.environ.get("WAWOO_SKILLS_GIT_REF") or DEFAULT_REF).strip()


def capabilities_raw_url(ref: str | None = None) -> str:
    r = ref or git_ref()
    return f"https://raw.githubusercontent.com/{GITHUB_REPO}/{r}/.kilo/CAPABILITIES.md"


def capabilities_blob_url(ref: str | None = None) -> str:
    r = ref or git_ref()
    return f"https://github.com/{GITHUB_REPO}/blob/{r}/.kilo/CAPABILITIES.md"


def github_blob_href(rel_path: str, ref: str | None = None) -> str:
    r = ref or git_ref()
    return f"https://github.com/{GITHUB_REPO}/blob/{r}/" + rel_path.replace("\\", "/")


def fetch_capabilities_md(ref: str | None = None) -> tuple[str, str]:
    url = capabilities_raw_url(ref)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            text = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        raise SystemExit(f"无法从 GitHub 读取 CAPABILITIES: {url} ({e.code})") from e
    except urllib.error.URLError as e:
        raise SystemExit(f"网络错误，无法拉取 GitHub CAPABILITIES: {url} ({e})") from e
    return text, url


_HEADER_COUNTS = re.compile(r"^## (Skills|Agents|Workflows)（(\d+)）", re.MULTILINE)


def parse_section_header_counts(text: str) -> dict[str, int]:
    """CAPABILITIES 見出しの件数（## Skills（98））を読む。"""
    out: dict[str, int] = {}
    for m in _HEADER_COUNTS.finditer(text):
        out[m.group(1).lower()] = int(m.group(2))
    return out


def assert_parsed_matches_headers(text: str, skills: list, agents: list, workflows: list) -> None:
    """表の行数が見出し件数と一致することを検証（114/23/22 などのズレを即検出）。"""
    hdr = parse_section_header_counts(text)
    expected = {
        "skills": len(skills),
        "agents": len(agents),
        "workflows": len(workflows),
    }
    for key, got in expected.items():
        want = hdr.get(key)
        if want is None:
            raise ValueError(f"CAPABILITIES に ## {key.title()}（N）見出しがありません")
        if want != got:
            raise ValueError(
                f"CAPABILITIES 件数不一致: {key} 見出し={want} 表行数={got} "
                f"（workspace の .kilo を kit に流していないか確認）"
            )


def _section(text: str, heading: str) -> str:
    m = re.search(
        rf"^## {re.escape(heading)}.*?\n(.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return m.group(1) if m else ""


def _parse_size_kb(cell: str) -> float | None:
    m = re.search(r"([\d.]+)\s*KB", cell, re.I)
    return round(float(m.group(1)), 1) if m else None


def parse_capabilities_md(text: str, *, ref: str | None = None) -> tuple[list[dict], list[dict], list[dict]]:
    r = ref or git_ref()
    skills: list[dict] = []
    skill_row = re.compile(
        r"^\| `([^`]+)` \| ([^|]+) \| ([^|]+) \| ([^|]+) \| `([^`]+)` \|",
        re.MULTILINE,
    )
    for m in skill_row.finditer(_section(text, "Skills")):
        name, ready_cell, size_cell, desc, path = (x.strip() for x in m.groups())
        ready = "✅" in ready_cell and "⚠️" not in ready_cell[:3]
        skills.append(
            {
                "name": name,
                "ready": ready,
                "ready_label": ready_cell.strip(),
                "size_kb": _parse_size_kb(size_cell),
                "description": re.sub(r"\s+", " ", desc).strip(),
                "path": path,
                "url": github_blob_href(path, r),
            }
        )

    agents: list[dict] = []
    agent_row = re.compile(r"^\| `([^`]+)` \| ([^|]+) \| `([^`]+)` \|", re.MULTILINE)
    for m in agent_row.finditer(_section(text, "Agents")):
        name, desc, path = (x.strip() for x in m.groups())
        agents.append(
            {
                "name": name,
                "description": re.sub(r"\s+", " ", desc).strip(),
                "path": path,
                "url": github_blob_href(path, r),
            }
        )

    workflows: list[dict] = []
    wf_row = re.compile(r"^\| `/([^`]+)` \| ([^|]+) \| `([^`]+)` \|", re.MULTILINE)
    for m in wf_row.finditer(_section(text, "Workflows")):
        wid, desc, path = (x.strip() for x in m.groups())
        cmd = f"/{wid}"
        workflows.append(
            {
                "name": cmd,
                "id": wid,
                "description": re.sub(r"\s+", " ", desc).strip(),
                "path": path,
                "url": github_blob_href(path, r),
            }
        )
    assert_parsed_matches_headers(text, skills, agents, workflows)
    return skills, agents, workflows