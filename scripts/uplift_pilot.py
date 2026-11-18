"""Uplift pilot SSOT — shared by validate_assets and skill_uplift_check."""

from __future__ import annotations

# Skills that must ship expectations.md (validate_assets).
UPLIFT_PILOT_SKILLS: frozenset[str] = frozenset(
    {
        "web-design-guidelines",
        "accessibility-audit",
        "deployment",
    }
)

# Static rules enabled per skill (must match rule ids in expectations.md / checker).
ACTIVE_STATIC_RULES: dict[str, frozenset[str]] = {
    "web-design-guidelines": frozenset(
        {
            "img-alt",
            "tabindex-positive",
            "outline-none",
            "clickable-div",
            "reduced-motion",
        }
    ),
    "accessibility-audit": frozenset(
        {
            "a11y-html-lang",
            "a11y-page-h1",
            "a11y-input-label",
            "a11y-button-type",
            "a11y-skip-link",
        }
    ),
    "deployment": frozenset(
        {
            "deploy-no-latest-tag",
            "deploy-plain-secret-env",
            "deploy-missing-healthcheck",
        }
    ),
}

# File extensions scanned per skill (deployment uses compose/yml only).
SKILL_SCAN_EXTENSIONS: dict[str, frozenset[str]] = {
    "web-design-guidelines": frozenset({".html", ".htm", ".tsx", ".jsx", ".vue", ".php", ".css", ".scss"}),
    "accessibility-audit": frozenset({".html", ".htm", ".tsx", ".jsx", ".vue", ".php"}),
    "deployment": frozenset({".yml", ".yaml"}),
}

DEPLOY_COMPOSE_NAMES = frozenset(
    {
        "docker-compose.yml",
        "docker-compose.yaml",
        "compose.yml",
        "compose.yaml",
    }
)