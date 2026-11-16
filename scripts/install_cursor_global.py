#!/usr/bin/env python3
"""Install wawoo-skills into the user-level Cursor config (idempotent, re-runnable).

Target: $CURSOR_HOME_DIR (default ~/.cursor)

  - rules : copy .cursor/rules/*.mdc -> <dir>/rules/  (relative `@.kilo/` rewritten to `@<ROOT>/.kilo/`)
  - skills: symlink .kilo/skills/<name> -> <dir>/skills/<name>   (the kit stays the single source)
  - agents: .kilo/agents/<name>.md -> <dir>/agents/<name>.md     (name + description + role body)
  - mcp   : merge `wawoo-skills` into <dir>/mcp.json             (existing servers preserved)

Cursor reads user-level **rules** and **skills** in the desktop app, CLI, and
cloud agents. User-level **agents** are read by the desktop app only; the CLI /
ACP reads project `.cursor/agents/` — use `install_cursor_workspace.py` there.

Usage:
  python3 scripts/install_cursor_global.py
  python3 scripts/install_cursor_global.py --dry-run
  python3 scripts/install_cursor_global.py --no-delete
  python3 scripts/install_cursor_global.py --memory-writable
  CURSOR_HOME_DIR=/path/to/.cursor python3 scripts/install_cursor_global.py
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from adapters import ROOT, cursor_agent_markdown, rewrite_rule_paths, sync_skills  # noqa: E402

SERVER = ROOT / "mcp" / "server.py"
ENV_DIR = os.environ.get("CURSOR_HOME_DIR", "")
CURSOR_DIR = Path(ENV_DIR).expanduser() if ENV_DIR else Path.home() / ".cursor"


def log(ok: bool, msg: str) -> None:
    print(f"{'OK  ' if ok else 'WARN'} {msg}")


def sync_rules(dry: bool) -> int:
    src = ROOT / ".cursor" / "rules"
    dst = CURSOR_DIR / "rules"
    n = 0
    for f in sorted(src.glob("*.mdc")):
        text = rewrite_rule_paths(f.read_text(encoding="utf-8"))
        if dry:
            log(True, f"would write {dst / f.name}")
        else:
            dst.mkdir(parents=True, exist_ok=True)
            (dst / f.name).write_text(text, encoding="utf-8")
        n += 1
    return n


def sync_agents(dry: bool) -> int:
    src = ROOT / ".kilo" / "agents"
    dst = CURSOR_DIR / "agents"
    n = 0
    for f in sorted(src.glob("*.md")):
        text = cursor_agent_markdown(f)
        if dry:
            log(True, f"would write {dst / f.name}")
        else:
            dst.mkdir(parents=True, exist_ok=True)
            (dst / f.name).write_text(text, encoding="utf-8")
        n += 1
    return n


def ensure_mcp(dry: bool, memory_readonly: bool) -> str:
    path = CURSOR_DIR / "mcp.json"
    cfg: dict = {}
    if path.exists():
        try:
            cfg = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return f"ERROR: invalid JSON at {path}, left unchanged"
    servers = cfg.setdefault("mcpServers", {})
    servers["wawoo-skills"] = {
        "command": sys.executable or "python3",
        "args": [str(SERVER)],
        "env": {
            "WAWOO_SKILLS_ROOT": str(ROOT),
            "WAWOO_MEMORY_READONLY": "1" if memory_readonly else "0",
        },
    }
    if dry:
        return f"would write {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
    path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return f"wrote {path}"


def main() -> int:
    ap = argparse.ArgumentParser(description="Install wawoo-skills into the user-level Cursor config (idempotent).")
    ap.add_argument("--dry-run", action="store_true", help="show actions without writing")
    ap.add_argument("--no-delete", action="store_true", help="keep extra files in skills/ (default: replace symlinks)")
    ap.add_argument("--memory-writable", action="store_true", help="register MCP with memory_save enabled")
    args = ap.parse_args()

    if not SERVER.exists():
        log(False, f"missing MCP server: {SERVER}")
        return 1

    print(f"repo root : {ROOT}")
    print(f"target    : {CURSOR_DIR}")
    print("---")
    log(True, f"rules: {sync_rules(args.dry_run)} file(s)")
    log(True, f"agents: {sync_agents(args.dry_run)} file(s)")
    linked = sync_skills(ROOT / ".kilo" / "skills", CURSOR_DIR / "skills", mirror=not args.no_delete, dry=args.dry_run, log=log)
    log(True, f"skills: {linked} link(s)")
    log(True, f"mcp: {ensure_mcp(args.dry_run, memory_readonly=not args.memory_writable)}")
    if args.dry_run:
        return 0
    print("---")
    print("RESULT: OK")
    print("Restart / Reload Cursor for changes to take effect.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
