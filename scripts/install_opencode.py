#!/usr/bin/env python3
"""Install wawoo-skills into the global OpenCode config (idempotent, re-runnable).

Target: $OPENCODE_GLOBAL_DIR (default ~/.config/opencode)

  - Mirror .kilo/agents  -> <dir>/agent   and .kilo/commands -> <dir>/command
    (the `name:` / `id:` keys are stripped from agent frontmatter so the agent
     key equals the file name — which is what command `agent:` references and
     what the kit expects; OpenCode otherwise keys an agent by `name:`)
  - Idempotently register in opencode.json (or opencode.jsonc):
      mcp.wawoo-skills      (local, absolute python + server, WAWOO_SKILLS_ROOT / WAWOO_MEMORY_READONLY)
      instructions          = [<ROOT>/AGENTS.md]            (absolute; relative paths are not injected)
      skills.paths          = [<ROOT>/.kilo/skills]         (native skill discovery)
      default_agent         = wawoo-auto                    (unless --no-default-agent)
  - Finally run validate_assets and the MCP smoke.

Usage:
  python3 scripts/install_opencode.py                    # mirror (full replace)
  python3 scripts/install_opencode.py --no-delete        # keep extras
  python3 scripts/install_opencode.py --dry-run          # preview changes only
  python3 scripts/install_opencode.py --memory-writable  # enable memory_save (default recall-only)
  python3 scripts/install_opencode.py --no-default-agent # do not set default_agent
  OPENCODE_GLOBAL_DIR=/path/to/config python3 scripts/install_opencode.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "mcp" / "server.py"
ENV_DIR = os.environ.get("OPENCODE_GLOBAL_DIR", "")
GLOBAL_DIR = Path(ENV_DIR).expanduser() if ENV_DIR else Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "opencode"
ASSET_DIRS = {
    "agent": ROOT / ".kilo" / "agents",
    "command": ROOT / ".kilo" / "commands",
}


def log(ok: bool, msg: str) -> None:
    print(f"{'OK  ' if ok else 'WARN'} {msg}")


def strip_jsonc(text: str) -> str:
    text = re.sub(r"^\s*//.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r",(\s*[}\]])", r"\1", text)
    return text


def config_path() -> Path:
    for name in ("opencode.json", "opencode.jsonc"):
        p = GLOBAL_DIR / name
        if p.exists():
            return p
    return GLOBAL_DIR / "opencode.json"


def load_config(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(strip_jsonc(path.read_text(encoding="utf-8")))
    except Exception:
        return {}


def write_config(path: Path, cfg: dict, dry: bool) -> None:
    if dry:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))
    path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sync_assets(dry: bool, mirror: bool) -> None:
    for name, src in ASSET_DIRS.items():
        dst = GLOBAL_DIR / name
        if dry:
            log(True, f"would sync {src} -> {dst} (mirror={mirror})")
            continue
        if dst.exists() and mirror:
            shutil.rmtree(dst)
        dst.mkdir(parents=True, exist_ok=True)
        for f in sorted(src.glob("*.md")):
            if f.name == "README.md":
                continue
            text = f.read_text(encoding="utf-8")
            if name == "agent":
                text = strip_agent_keys(text)
            (dst / f.name).write_text(text, encoding="utf-8")
        log(True, f"synced {src} -> {dst} (mirror={mirror})")


def strip_agent_keys(text: str) -> str:
    """Remove the `name:` / `id:` lines from the leading frontmatter so the agent key is the file name."""
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
    if not m:
        return text
    kept = [line for line in m.group(1).splitlines() if not re.match(r"^(name|id):\s", line)]
    return "---\n" + "\n".join(kept) + "\n---\n" + text[m.end():]


def mcp_entry(memory_readonly: bool) -> dict:
    py = sys.executable or "/usr/bin/python3"
    return {
        "type": "local",
        "command": [py, str(SERVER)],
        "enabled": True,
        "environment": {
            "WAWOO_SKILLS_ROOT": str(ROOT),
            "WAWOO_MEMORY_READONLY": "1" if memory_readonly else "0",
        },
    }


def ensure_config(dry: bool, memory_readonly: bool, default_agent: str | None) -> str:
    path = config_path()
    cfg = load_config(path)
    cfg.setdefault("$schema", "https://opencode.ai/config.json")

    mcp = cfg.setdefault("mcp", {})
    mcp["wawoo-skills"] = mcp_entry(memory_readonly)

    cfg["instructions"] = [str(ROOT / "AGENTS.md")]

    skills = cfg.setdefault("skills", {})
    paths = [p for p in (skills.get("paths") or []) if p != str(ROOT / ".kilo" / "skills")]
    paths.append(str(ROOT / ".kilo" / "skills"))
    skills["paths"] = paths

    if default_agent:
        cfg["default_agent"] = default_agent

    if dry:
        return f"would write {path} (mcp + instructions + skills.paths + default_agent)"
    write_config(path, cfg, dry=False)
    return f"wrote {path} (mcp + instructions + skills.paths + default_agent)"


def verify() -> bool:
    ok = True
    try:
        v = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_assets.py")],
            cwd=str(ROOT), capture_output=True, text=True, timeout=120,
        )
        tail = (v.stdout + v.stderr).strip().splitlines()[-1:] or [""]
        log(v.returncode == 0, f"validate_assets: {tail[0]}")
        ok = ok and v.returncode == 0
    except Exception as exc:
        log(False, f"validate_assets failed to run: {exc}")
        ok = False
    smoke = ROOT / "internal" / "tests" / "test_server.py"
    if smoke.is_file():
        try:
            s = subprocess.run(
                [sys.executable, str(smoke)],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120,
            )
            tail = (s.stdout + s.stderr).strip().splitlines()[-1:] or [""]
            log(s.returncode == 0, f"mcp smoke: {tail[0]}")
            ok = ok and s.returncode == 0
        except Exception as exc:
            log(False, f"mcp smoke failed to run: {exc}")
            ok = False
    else:
        log(True, "mcp smoke: skipped (internal/tests not present)")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description="Install wawoo-skills into the global OpenCode config (idempotent).")
    ap.add_argument("--no-delete", action="store_true", help="keep extra files in target asset dirs (default: mirror)")
    ap.add_argument("--dry-run", action="store_true", help="show actions without writing")
    ap.add_argument("--default-agent", default="wawoo-auto", help="default_agent to register (default: wawoo-auto)")
    ap.add_argument("--no-default-agent", action="store_true", help="do not touch default_agent")
    ap.add_argument(
        "--memory-writable",
        action="store_true",
        help="register MCP with memory_save enabled (WAWOO_MEMORY_READONLY=0). Default keeps recall-only.",
    )
    args = ap.parse_args()

    if not SERVER.exists():
        log(False, f"missing MCP server: {SERVER}")
        return 1

    print(f"repo root : {ROOT}")
    print(f"target    : {GLOBAL_DIR}")
    print(f"mirror    : {not args.no_delete}")
    print("---")
    sync_assets(args.dry_run, not args.no_delete)
    default_agent = None if args.no_default_agent else args.default_agent
    log(True, f"config: {ensure_config(args.dry_run, memory_readonly=not args.memory_writable, default_agent=default_agent)}")
    if args.dry_run:
        return 0
    print("---")
    ok = verify()
    print("---")
    print("RESULT:", "OK" if ok else "FAILED")
    print("Restart OpenCode for changes to take effect (config is loaded once at startup).")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
