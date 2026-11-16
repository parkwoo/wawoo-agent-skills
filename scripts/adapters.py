#!/usr/bin/env python3
"""Shared helpers: turn the kit's `.kilo` assets into another tool's native files.

Used by `install_cursor_workspace.py` and `install_cursor_global.py` (and any
future adapter). Standard library only.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return (frontmatter dict, body). Single-line scalar values only (sufficient for the kit)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    meta: dict[str, str] = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            value = m.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            meta[m.group(1)] = value
    return meta, text[end + 4:].lstrip("\n")


def cursor_agent_markdown(agent_path: Path) -> str:
    """A Cursor project/user subagent: `name` + `description` frontmatter, body = the role prompt."""
    meta, body = read_frontmatter(agent_path.read_text(encoding="utf-8"))
    name = agent_path.stem
    description = meta.get("description") or f"wawoo {name} agent"
    return f"---\nname: {name}\ndescription: {description}\n---\n\n{body}\n"


def rewrite_rule_paths(text: str, root: Path = ROOT) -> str:
    """Rewrite relative `@.kilo/` references to absolute `@<root>/.kilo/` (for user-level rules)."""
    return text.replace("@.kilo/", f"@{root.as_posix()}/.kilo/")


def sync_skills(src_skills: Path, dst_skills: Path, mirror: bool, dry: bool, log=print) -> int:
    """Symlink each `.kilo/skills/<name>` into `dst_skills/<name>` (the kit stays the single source)."""
    dst_skills.mkdir(parents=True, exist_ok=True)
    linked = 0
    for d in sorted(src_skills.glob("*/")):
        if not (d / "SKILL.md").is_file():
            continue
        link = dst_skills / d.name
        if link.is_symlink():
            if dry:
                log(True, f"would relink {link}")
                continue
            link.unlink()
        elif link.exists():
            if not mirror:
                log(True, f"keep existing {link}")
                continue
            if dry:
                log(True, f"would replace {link}")
                continue
            shutil.rmtree(link)
        if dry:
            log(True, f"would link {link} -> {d}")
        else:
            link.symlink_to(d.resolve())
        linked += 1
    return linked
