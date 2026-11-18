#!/usr/bin/env python3
"""Fail if writing/marketing assets appear in the public programming-only kit.

The marker `.public-programming-only` at the repo root enables this check.
The internal source (workspace/skills) legitimately has these assets; without
the marker this script simply skips.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = ROOT / ".public-programming-only"

DENY_SKILLS = {
    "marketing-psychology",
    "viral-hooks",
    "science-writing",
    "screenshots-marketing",
    "slides",
    "brand-guidelines",
    "writing-fragments",
    "writing-beats",
    "writing-shape",
    "seo-writing",
    "proofreading",
}
DENY_COMMANDS = {
    "writing",
    "market-plan",
    "deck",
    "content-delivery-lite",
    "content-build",
    "content-audit",
}
DENY_AGENTS = {"market-researcher.md"}


def main() -> int:
    if not MARKER.exists():
        print("skip: not the public programming-only repo")
        return 0

    bad: list[str] = []
    for name in sorted(DENY_SKILLS):
        if (ROOT / ".kilo" / "skills" / name).exists():
            bad.append(f".kilo/skills/{name}")
    for name in sorted(DENY_COMMANDS):
        if (ROOT / ".kilo" / "commands" / f"{name}.md").exists():
            bad.append(f".kilo/commands/{name}.md")
    for name in sorted(DENY_AGENTS):
        if (ROOT / ".kilo" / "agents" / name).exists():
            bad.append(f".kilo/agents/{name}")

    if bad:
        print(
            "FAIL: writing/marketing assets found in the public programming-only kit:",
            file=sys.stderr,
        )
        for item in bad:
            print(f"  - {item}", file=sys.stderr)
        print(
            "Move them to the internal source (workspace/skills). See CONTRIBUTING.md.",
            file=sys.stderr,
        )
        return 1

    print("OK: public kit contains programming assets only")
    return 0


if __name__ == "__main__":
    sys.exit(main())
