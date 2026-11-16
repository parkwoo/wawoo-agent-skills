#!/usr/bin/env python3
"""Install wawoo-skills into a Cursor *workspace* (monorepo-friendly, idempotent).

Writes into <workspace>/.cursor:
  - mcp.json : register `wawoo-skills` (json `command`/`args`, relative server path when inside the workspace)
  - rules/   : copy .cursor/rules/*.mdc (relative `@.kilo/` rewritten to the kit's absolute path)
  - agents/  : .kilo/agents/<name>.md -> <workspace>/.cursor/agents/<name>.md (Cursor project subagents)
  - skills/  : symlink .kilo/skills/<name> -> <workspace>/.cursor/skills/<name>

Project-level rules/skills/agents are read by the Cursor app, **CLI, and cloud agents**.

Usage:
  python3 scripts/install_cursor_workspace.py
  python3 scripts/install_cursor_workspace.py --workspace /home/git
  python3 scripts/install_cursor_workspace.py --dry-run
  python3 scripts/install_cursor_workspace.py --mcp-only     # legacy: only write mcp.json
  python3 scripts/install_cursor_workspace.py --memory-writable
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from adapters import ROOT, cursor_agent_markdown, rewrite_rule_paths, sync_skills  # noqa: E402

SERVER = ROOT / "mcp" / "server.py"
PY = sys.executable or "python3"


def log(ok: bool, msg: str) -> None:
    print(f"{'OK  ' if ok else 'WARN'} {msg}")


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


def write_mcp(cursor_dir: Path, ws: Path, memory_readonly: bool, dry: bool) -> str:
    mcp_path = cursor_dir / "mcp.json"
    server_arg = resolve_server_arg(ws, ROOT.resolve())
    payload = mcp_payload(ROOT.resolve(), server_arg, memory_readonly)
    if dry:
        return f"would write {mcp_path} (server arg: {server_arg})"
    cursor_dir.mkdir(parents=True, exist_ok=True)
    mcp_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return f"wrote {mcp_path} (server arg: {server_arg})"


def install_assets(cursor_dir: Path, dry: bool, mirror: bool) -> None:
    rules_dst = cursor_dir / "rules"
    for f in sorted((ROOT / ".cursor" / "rules").glob("*.mdc")):
        text = rewrite_rule_paths(f.read_text(encoding="utf-8"))
        if dry:
            log(True, f"would write {rules_dst / f.name}")
        else:
            rules_dst.mkdir(parents=True, exist_ok=True)
            (rules_dst / f.name).write_text(text, encoding="utf-8")
    agents_dst = cursor_dir / "agents"
    for f in sorted((ROOT / ".kilo" / "agents").glob("*.md")):
        text = cursor_agent_markdown(f)
        if dry:
            log(True, f"would write {agents_dst / f.name}")
        else:
            agents_dst.mkdir(parents=True, exist_ok=True)
            (agents_dst / f.name).write_text(text, encoding="utf-8")
    linked = sync_skills(ROOT / ".kilo" / "skills", cursor_dir / "skills", mirror=mirror, dry=dry, log=log)
    log(True, f"skills: {linked} link(s)")


def main() -> int:
    ap = argparse.ArgumentParser(description="Install wawoo-skills into a Cursor workspace (.cursor)")
    ap.add_argument("--workspace", type=Path, default=Path.cwd(), help="Cursor workspace root")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--mcp-only", action="store_true", help="only write .cursor/mcp.json (legacy behaviour)")
    ap.add_argument("--no-delete", action="store_true", help="keep extra files in skills/")
    ap.add_argument("--memory-writable", action="store_true", help="allow memory_save from other repos")
    args = ap.parse_args()

    ws = args.workspace.resolve()
    if not SERVER.is_file():
        log(False, f"missing MCP server: {SERVER}")
        return 1

    cursor_dir = ws / ".cursor"
    print(f"workspace     : {ws}")
    print(f"skills root   : {ROOT.resolve()}")
    print(f"write target  : {cursor_dir}")
    print("---")

    log(True, f"mcp: {write_mcp(cursor_dir, ws, memory_readonly=not args.memory_writable, dry=args.dry_run)}")
    if args.mcp_only:
        return 0
    if ws == ROOT.resolve():
        log(True, "workspace is the kit itself; rules/agents/skills already ship here — skipping")
        return 0
    install_assets(cursor_dir, args.dry_run, mirror=not args.no_delete)
    if args.dry_run:
        return 0
    print("---")
    print("RESULT: OK")
    print("Next: Cursor Reload Window -> Settings -> MCP -> enable wawoo-skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
