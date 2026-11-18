#!/usr/bin/env python3
"""Lightweight static checks for skill expectations.md (uplift pilot; stdlib only)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KILO = ROOT / ".kilo" / "skills"
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from uplift_pilot import (  # noqa: E402
    ACTIVE_STATIC_RULES,
    DEPLOY_COMPOSE_NAMES,
    SKILL_SCAN_EXTENSIONS,
    UPLIFT_PILOT_SKILLS,
)


@dataclass
class Finding:
    rule: str
    path: str
    line: int
    detail: str


def iter_files(root: Path, exts: frozenset[str]) -> list[Path]:
    if root.is_file():
        if root.name in DEPLOY_COMPOSE_NAMES or root.suffix.lower() in exts:
            return [root]
        return []
    out: list[Path] = []
    skip = {"node_modules", ".git", "vendor", "dist", "build", "__pycache__"}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in skip for part in p.parts):
            continue
        if p.name in DEPLOY_COMPOSE_NAMES or p.suffix.lower() in exts:
            out.append(p)
    return out


def check_img_alt(path: Path, text: str) -> list[Finding]:
    out: list[Finding] = []
    for m in re.finditer(r"<img\b[^>]*>", text, re.I | re.S):
        tag = m.group(0)
        if not re.search(r"\balt\s*=", tag, re.I):
            line = text[: m.start()].count("\n") + 1
            out.append(Finding("img-alt", str(path), line, "img without alt"))
    return out


def check_web_design_guidelines(path: Path, text: str, active: frozenset[str]) -> list[Finding]:
    findings: list[Finding] = []
    lines = text.splitlines()
    if "img-alt" in active:
        findings.extend(check_img_alt(path, text))
    for i, line in enumerate(lines, 1):
        if "tabindex-positive" in active and re.search(r"tabindex\s*=\s*[\"']?[1-9]", line, re.I):
            findings.append(Finding("tabindex-positive", str(path), i, "positive tabindex"))
        if "outline-none" in active and re.search(r"outline\s*:\s*(none|0)\b", line, re.I):
            findings.append(
                Finding("outline-none", str(path), i, "outline removed — verify focus substitute in file/CSS")
            )
        if "clickable-div" in active and re.search(
            r"<(div|span)\b[^>]*\bonclick\s*=", line, re.I
        ) and not re.search(r"role\s*=\s*[\"']button", line, re.I):
            findings.append(Finding("clickable-div", str(path), i, "onclick on div/span without role=button"))
    if "reduced-motion" in active:
        if "@media" not in text and "prefers-reduced-motion" not in text:
            if re.search(r"animation\s*:|@keyframes|transition\s*:", text):
                findings.append(
                    Finding(
                        "reduced-motion",
                        str(path),
                        0,
                        "animations present but no prefers-reduced-motion in this file",
                    )
                )
    return findings


def check_accessibility_audit(path: Path, text: str, active: frozenset[str]) -> list[Finding]:
    findings: list[Finding] = []
    if path.suffix.lower() not in {".html", ".htm", ".php", ".tsx", ".jsx", ".vue"}:
        return findings
    if "a11y-html-lang" in active and not re.search(r"<html[^>]*\blang\s*=", text, re.I):
        findings.append(Finding("a11y-html-lang", str(path), 1, "missing html lang"))
    if "a11y-page-h1" in active and not re.search(r"<h1\b", text, re.I):
        findings.append(Finding("a11y-page-h1", str(path), 0, "no h1 in file"))
    if "a11y-skip-link" in active:
        if not re.search(r"skip|#main|href=\"#content\"", text, re.I):
            findings.append(Finding("a11y-skip-link", str(path), 0, "no skip-link pattern near top"))
    for i, line in enumerate(text.splitlines(), 1):
        if "a11y-button-type" in active and re.search(r"<button\b(?![^>]*\btype\s*=)", line, re.I):
            findings.append(Finding("a11y-button-type", str(path), i, "button without explicit type"))
        if "a11y-input-label" not in active:
            continue
        for m in re.finditer(r"<(input|select|textarea)\b([^>]*)>", line, re.I):
            attrs = m.group(2)
            if re.search(r"\btype\s*=\s*[\"']?hidden", attrs, re.I):
                continue
            has_label = bool(re.search(r"\b(aria-label|aria-labelledby)\s*=", attrs, re.I))
            has_id = re.search(r"\bid\s*=\s*[\"']([^\"']+)", attrs, re.I)
            if not has_label and not has_id:
                findings.append(Finding("a11y-input-label", str(path), i, "control without label hook"))
    return findings


def check_deployment(path: Path, text: str, active: frozenset[str]) -> list[Finding]:
    findings: list[Finding] = []
    lines = text.splitlines()
    in_service = False
    service_has_ports = False
    service_has_healthcheck = False
    service_line = 0

    def flush_service():
        nonlocal in_service, service_has_ports, service_has_healthcheck
        if in_service and service_has_ports and not service_has_healthcheck:
            if "deploy-missing-healthcheck" in active:
                findings.append(
                    Finding(
                        "deploy-missing-healthcheck",
                        str(path),
                        service_line,
                        "service exposes ports but has no healthcheck",
                    )
                )
        in_service = False
        service_has_ports = False
        service_has_healthcheck = False

    for i, line in enumerate(lines, 1):
        if "deploy-no-latest-tag" in active and re.search(r"image\s*:\s*[^\s#]+:latest\b", line, re.I):
            findings.append(Finding("deploy-no-latest-tag", str(path), i, "image uses :latest"))
        if "deploy-plain-secret-env" in active:
            if re.search(r"(?i)(password|secret|api_key|token)\s*[:=]\s*['\"][^$\\{][^'\"]+", line):
                findings.append(Finding("deploy-plain-secret-env", str(path), i, "possible plaintext secret in compose"))
        if re.match(r"^\s{2}\w[\w-]*:\s*$", line) and "services" not in line:
            flush_service()
            in_service = True
            service_line = i
            continue
        if in_service:
            if re.search(r"^\s{4}ports\s*:", line):
                service_has_ports = True
            if re.search(r"^\s{4}healthcheck\s*:", line):
                service_has_healthcheck = True
            if re.match(r"^\s{2}\w", line) and not line.startswith("    "):
                flush_service()
    flush_service()
    return findings


CHECKERS = {
    "web-design-guidelines": check_web_design_guidelines,
    "accessibility-audit": check_accessibility_audit,
    "deployment": check_deployment,
}


def run(skill: str, target: Path) -> dict:
    if skill not in UPLIFT_PILOT_SKILLS:
        return {"ok": False, "error": f"skill not in pilot: {skill}"}
    exp = KILO / skill / "expectations.md"
    if not exp.is_file():
        return {"ok": False, "error": f"missing {exp}"}
    checker = CHECKERS.get(skill)
    if not checker:
        return {"ok": False, "error": f"no checker for {skill}"}
    active = ACTIVE_STATIC_RULES.get(skill, frozenset())
    exts = SKILL_SCAN_EXTENSIONS.get(skill, frozenset())
    all_findings: list[dict] = []
    files = iter_files(target, exts)
    if not files:
        return {"ok": False, "error": f"no scannable files under {target}"}
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            all_findings.append({"rule": "read-error", "path": str(f), "line": 0, "detail": str(exc)})
            continue
        for finding in checker(f, text, active):
            all_findings.append(
                {"rule": finding.rule, "path": finding.path, "line": finding.line, "detail": finding.detail}
            )
    return {
        "ok": True,
        "skill": skill,
        "target": str(target),
        "active_rules": sorted(active),
        "files_scanned": len(files),
        "finding_count": len(all_findings),
        "findings": all_findings,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Run skill expectations static checks")
    ap.add_argument("skill", help="skill name (e.g. web-design-guidelines)")
    ap.add_argument("--path", type=Path, required=True, help="file or directory to scan")
    ap.add_argument("--json", action="store_true", help="alias for JSON stdout (default)")
    args = ap.parse_args()
    res = run(args.skill, args.path.resolve())
    print(json.dumps(res, ensure_ascii=False, indent=2))
    if not res.get("ok"):
        return 2
    return 1 if res.get("finding_count") else 0


if __name__ == "__main__":
    raise SystemExit(main())