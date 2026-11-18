#!/usr/bin/env python3
"""README の版表示を VERSION（正本）と揃える。validate_assets からも参照される。"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 各 README の「現在版」行（semver のみ置換）
README_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("README.md", re.compile(r"(Current:\s*\*\*)([0-9]+\.[0-9]+\.[0-9]+)(\*\*)")),
    ("README.ja.md", re.compile(r"(現在:\s*\*\*)([0-9]+\.[0-9]+\.[0-9]+)(\*\*)")),
    ("README.ko.md", re.compile(r"(현재:\s*\*\*)([0-9]+\.[0-9]+\.[0-9]+)(\*\*)")),
    ("README.zh-CN.md", re.compile(r"(当前版本：\*\*)([0-9]+\.[0-9]+\.[0-9]+)(\*\*)")),
)


def ssot_version() -> str:
    path = ROOT / "VERSION"
    if not path.is_file():
        raise FileNotFoundError(f"missing VERSION: {path}")
    v = path.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", v):
        raise ValueError(f"invalid VERSION: {v!r}")
    return v


def readme_version_issues() -> list[str]:
    """README 版表示が VERSION と一致しない場合のメッセージ。"""
    try:
        expected = ssot_version()
    except (FileNotFoundError, ValueError) as exc:
        return [str(exc)]

    issues: list[str] = []
    for name, pattern in README_PATTERNS:
        path = ROOT / name
        if not path.is_file():
            issues.append(f"missing README for version sync: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        m = pattern.search(text)
        if not m:
            issues.append(f"{name}: version line not found (run sync_readme_version.py)")
            continue
        found = m.group(2)
        if found != expected:
            issues.append(f"{name}: README has {found} but VERSION is {expected}")
    return issues


def sync_readmes(*, dry_run: bool = False) -> int:
    """VERSION を README 4 種へ反映。変更があれば 0、変更なしでも 0。"""
    expected = ssot_version()
    changed = 0
    for name, pattern in README_PATTERNS:
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        m = pattern.search(text)
        if not m:
            print(f"SKIP {name}: version line not found", file=sys.stderr)
            return 1
        if m.group(2) == expected:
            continue
        new_text = pattern.sub(rf"\g<1>{expected}\g<3>", text, count=1)
        changed += 1
        if dry_run:
            print(f"would update {name}: {m.group(2)} -> {expected}")
        else:
            path.write_text(new_text, encoding="utf-8")
            print(f"updated {name}: {m.group(2)} -> {expected}")
    if changed == 0:
        print(f"OK: READMEs already match VERSION ({expected})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync README version lines from VERSION")
    parser.add_argument("--check", action="store_true", help="exit 1 if out of sync")
    parser.add_argument("--dry-run", action="store_true", help="with default sync, print only")
    args = parser.parse_args()
    if args.check:
        issues = readme_version_issues()
        if issues:
            for line in issues:
                print(line, file=sys.stderr)
            return 1
        print(f"OK: READMEs match VERSION ({ssot_version()})")
        return 0
    return sync_readmes(dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())