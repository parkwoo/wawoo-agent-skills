#!/usr/bin/env python3
"""Register wawoo-skills MCP in a Cursor workspace (monorepo-friendly, idempotent).

Usage:
  python3 scripts/install_cursor_workspace.py
  python3 scripts/install_cursor_workspace.py --workspace /home/git
  python3 scripts/install_cursor_workspace.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "mcp" / "server.py"
PY = sys.executable or "python3"


def mcp_payload(skills_root: Path, server_arg: str, memory_readonly: bool) -> dict:
    return {
        "mcpServers": {
            "wawoo-skills": {
                "command": PY,
                "args": [server_arg],
                "env": {
                    "WAWOO_SKILLS_ROOT": str(skills_root),
                    "WAWOO_MEMORY_READONLY": "0" if not memory_readonly else "1",
                },
            }
        }
    }


def resolve_server_arg(workspace: Path, skills_root: Path) -> str:
    try:
        rel = SERVER.relative_to(workspace)
        return str(rel).replace("\\", "/")
    except ValueError:
        return str(SERVER)


def main() -> int:
    ap = argparse.ArgumentParser(description="Install wawoo-skills MCP into .cursor/mcp.json")
    ap.add_argument("--workspace", type=Path, default=Path.cwd(), help="Cursor workspace root")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--memory-writable", action="store_true", help="allow memory_save from other repos")
    args = ap.parse_args()

    ws = args.workspace.resolve()
    skills_root = ROOT.resolve()
    if not SERVER.is_file():
        print(f"ERROR: missing {SERVER}", file=sys.stderr)
        return 1

    cursor_dir = ws / ".cursor"
    mcp_path = cursor_dir / "mcp.json"
    server_arg = resolve_server_arg(ws, skills_root)
    payload = mcp_payload(skills_root, server_arg, memory_readonly=not args.memory_writable)

    print(f"workspace     : {ws}")
    print(f"skills root   : {skills_root}")
    print(f"server arg    : {server_arg}")
    print(f"write target  : {mcp_path}")

    if args.dry_run:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    cursor_dir.mkdir(parents=True, exist_ok=True)
    mcp_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("OK: wrote", mcp_path)
    print("Next: Cursor Reload Window → Settings → MCP → enable wawoo-skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
