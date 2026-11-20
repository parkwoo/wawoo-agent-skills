#!/usr/bin/env python3
"""公開 OSS clone・GitHub 倉・公式サイト URL の SSOT（命名移行用）。"""
from __future__ import annotations

import os
from pathlib import Path

PUBLIC_GITHUB_REPO = "parkwoo/wawoo-agent-skills"
PUBLIC_GITHUB_URL = f"https://github.com/{PUBLIC_GITHUB_REPO}"
PUBLIC_GITHUB_BLOB = f"github.com/{PUBLIC_GITHUB_REPO}"

SITE_CANONICAL_ORIGIN = "https://skills.wawoo.jp"

_DEFAULT_CLONE = Path("/home/git/wawoo-agent-skills")


def kit_oss_clone_root() -> Path:
    """本機の公開 wawoo-agent-skills clone（gen local / USAGE 同期用）。"""
    env = (os.environ.get("WAWOO_KIT_OSS_ROOT") or os.environ.get("WAWOO_OSS_CLONE") or "").strip()
    if env:
        root = Path(env).expanduser().resolve()
    else:
        root = _DEFAULT_CLONE if _DEFAULT_CLONE.is_dir() else Path("/home/git/wawoo-skills")
    return root


def github_blob_href(rel_path: str, ref: str = "master") -> str:
    rel = rel_path.lstrip("/")
    return f"{PUBLIC_GITHUB_URL}/blob/{ref}/{rel}"


def github_raw_href(rel_path: str, ref: str = "master") -> str:
    rel = rel_path.lstrip("/")
    return f"https://raw.githubusercontent.com/{PUBLIC_GITHUB_REPO}/{ref}/{rel}"