"""Workflow ledger used by intent interpretation (to avoid circular imports)."""

from __future__ import annotations

from dataclasses import dataclass

# Tool names exposed by MCP server.py (the allow-set per workflow)
_MWG_TOOLS: frozenset[str] = frozenset(
    {
        "mwg_search",
        "mwg_retrieve",
        "mwg_legacy_scan",
    }
)

MCP_TOOL_NAMES: frozenset[str] = frozenset(
    {
        "capabilities",
        "skill_search",
        "skill_get",
        "workflow_get",
        "agent_get",
        "memory_recall",
        "memory_save",
        "evidence_check",
        "interpret_intent",
        "route_task",
        "compress_context",
        "mask_pii",
        "redact_infra",
        "guard_content",
    }
) | _MWG_TOOLS

_MCP_READ: frozenset[str] = frozenset(
    {
        "capabilities",
        "skill_search",
        "skill_get",
        "workflow_get",
        "agent_get",
        "memory_recall",
        "interpret_intent",
        "route_task",
        "compress_context",
        "mask_pii",
        "redact_infra",
        "guard_content",
    }
) | _MWG_TOOLS

_MCP_FULL: frozenset[str] = MCP_TOOL_NAMES

_MCP_AUDIT: frozenset[str] = frozenset(
    {
        "capabilities",
        "skill_search",
        "skill_get",
        "workflow_get",
        "agent_get",
        "memory_recall",
        "evidence_check",
        "interpret_intent",
        "route_task",
        "compress_context",
        "mask_pii",
        "redact_infra",
        "guard_content",
    }
)


@dataclass(frozen=True)
class WorkflowSpec:
    agent: str
    description: str
    mcp_tools: frozenset[str]
    # L3: post-start delegation is done by the host IDE/agent (equivalent to an OpenCode subagent)
    delegation: str = "upstream-subagent"
    # P1: decomposed phases (attached later by phases_for())
    phases: tuple[Phase, ...] = ()


WORKFLOWS: dict[str, WorkflowSpec] = {
    "delivery-lite": WorkflowSpec(
        "implementer",
        "Lightweight delivery. Single-feature implementation and progress tracking via ACTIVE.md. Default path for clear, small changes.",
        _MCP_FULL,
    ),
    "feature-delivery": WorkflowSpec(
        "delivery-lead",
        "Cross-cutting feature delivery. Full delivery that bundles design and implementation across multiple components.",
        _MCP_FULL,
    ),
    "ui-delivery": WorkflowSpec(
        "web-designer",
        "UI/UX implementation. Frontend delivery of screens and components per the design charter.",
        _MCP_FULL,
    ),
    "design-review": WorkflowSpec(
        "web-designer",
        "Design/UI review. The main goal is evaluation, findings, and improvement suggestions rather than implementation changes.",
        _MCP_READ,
    ),
    "research": WorkflowSpec(
        "product-owner",
        "Research and decisions. From research on technology, market, and specs to the spec/ticket decision.",
        _MCP_READ,
    ),
    "compliance-review": WorkflowSpec(
        "compliance-reviewer",
        "Compliance / policy-fit review (automatic writes to memory are restricted).",
        _MCP_AUDIT,
    ),
    "release-review": WorkflowSpec(
        "release-manager",
        "Pre-release check. Confirm change scope, risks, and gates.",
        _MCP_AUDIT,
    ),
    "incident-response": WorkflowSpec(
        "sre-operator",
        "Production incident response. Diagnosis, recovery, and recording are the main goals.",
        _MCP_FULL,
    ),
    "sprint-plan": WorkflowSpec(
        "project-manager",
        "Sprint planning. Backlog grooming, estimation, and scope agreement.",
        _MCP_READ,
    ),
    "status-report": WorkflowSpec(
        "project-manager",
        "Status report. Organize progress, blockers, and next actions.",
        _MCP_READ,
    ),
    "self-review": WorkflowSpec(
        "code-reviewer",
        "Self-review. Check change quality, tests, and design consistency.",
        _MCP_AUDIT,
    ),
    "self-improve": WorkflowSpec(
        "delivery-lead",
        "Improve the kit and process themselves. Update skills, procedures, and templates.",
        _MCP_FULL,
    ),
}

# backward compatibility
WORKFLOW_AGENTS: dict[str, str] = {wid: spec.agent for wid, spec in WORKFLOWS.items()}


def workflow_spec(workflow_id: str) -> WorkflowSpec | None:
    return WORKFLOWS.get(workflow_id)


def mcp_tools_allow(workflow_id: str) -> list[str]:
    spec = workflow_spec(workflow_id)
    if spec is None:
        return sorted(MCP_TOOL_NAMES)
    return sorted(spec.mcp_tools)


def catalog_for_upstream(max_desc: int = 72) -> list[dict[str, str]]:
    """A compact list for upstream scoring."""
    rows: list[dict[str, str]] = []
    for wid in sorted(WORKFLOWS):
        spec = WORKFLOWS[wid]
        desc = spec.description
        if len(desc) > max_desc:
            desc = desc[: max_desc - 1] + "…"
        rows.append({"id": wid, "description": desc})
    return rows


# --- workflow phases (P1: decomposition, P2: per-phase tooling) -------------------


@dataclass(frozen=True)
class Phase:
    id: str
    goal: str
    agent: str
    skills: tuple[str, ...] = ()
    tools: frozenset[str] = _MCP_READ
    exit_criteria: tuple[str, ...] = ()
    parallel_group: str = ""


BASE_PHASES: dict[str, Phase] = {
    "discover": Phase("discover", "Fix the outcome, acceptance criteria, and scope", "product-owner", ("product-discovery", "in-your-own-words", "principle-attack-the-premise"), _MCP_READ, ("outcome and acceptance criteria are stated",)),
    "understand": Phase("understand", "Understand intent and runtime before changing", "architect", ("recall", "why", "how"), _MCP_READ, ("goal restated / intent evidence / runtime model stated",)),
    "design": Phase("design", "Decide design and tradeoffs", "architect", ("architecture-decision", "principle-exhaust-the-design-space", "principle-redesign-from-first-principles"), _MCP_READ, ("decision, alternatives, and rejection reasons are recorded",)),
    "plan": Phase("plan", "Break down the work and document the plan", "project-manager", ("plan-md", "recall", "figure-it-out", "principle-sequence-verifiable-units", "context-compression"), _MCP_READ, ("the plan is saved in docs and has an id",)),
    "implement": Phase("implement", "Implement the smallest change", "implementer", ("engineering-quality", "how", "principle-foundational-thinking", "principle-model-the-domain", "principle-subtract-before-you-add", "principle-guard-the-context-window"), _MCP_FULL, ("change is scoped / tests added / no secrets",)),
    "verify": Phase("verify", "Check tests and evidence", "qa-engineer", ("test-engineering", "principle-test-behavior-not-implementation", "principle-prove-it-works", "principle-build-the-lever", "create-verification-skill", "data-egress-guard", "content-guardrail"), _MCP_FULL, ("0 unconverged FAILED / 0 leftover containers / commands recorded",), "readonly-parallel"),
    "audit": Phase("audit", "Read-only review", "security-reviewer", ("security-review", "privacy-review", "blast-radius", "principle-fix-root-causes"), _MCP_READ, ("findings and evidence (with severity)",), "readonly-parallel"),
    "research": Phase("research", "Research primary sources", "product-owner", ("research", "why", "how"), _MCP_READ, ("fact and inference recorded separately",), "readonly-parallel"),
    "release": Phase("release", "Decide release readiness", "release-manager", ("release-readiness", "principle-make-operations-idempotent"), _MCP_AUDIT, ("version/tag/rollback/unverified stated",)),
    "report": Phase("report", "Report with evidence", "delivery-lead", ("change-readiness", "show-me-your-work", "data-egress-guard", "content-guardrail"), _MCP_AUDIT, ("evidence, unverified, risk, next actions",)),
}

# P5: reuse common phases (avoid duplicate definitions)
WORKFLOW_PHASES: dict[str, tuple[str, ...]] = {
    "delivery-lite": ("plan", "implement", "verify", "report"),
    "feature-delivery": ("understand", "discover", "design", "implement", "verify", "report"),
    "ui-delivery": ("design", "implement", "verify", "report"),
    "design-review": ("audit", "report"),
    "research": ("research", "report"),
    "compliance-review": ("audit", "report"),
    "release-review": ("audit", "release", "report"),
    "incident-response": ("understand", "audit", "implement", "verify", "report"),
    "sprint-plan": ("plan", "report"),
    "status-report": ("report",),
    "self-review": ("audit", "verify", "report"),
    "self-improve": ("plan", "implement", "verify", "report"),
}

# Override agent/skills only for a specific workflow's phase
PHASE_OVERRIDES: dict[tuple[str, str], dict[str, object]] = {
    ("ui-delivery", "implement"): {"agent": "web-designer", "skills": ("web-experience-design", "frontend-design")},
    ("ui-delivery", "verify"): {"skills": ("web-design-guidelines", "accessibility-audit")},
    ("design-review", "audit"): {"agent": "web-designer", "skills": ("design-review", "web-design-guidelines", "accessibility-audit")},
    ("compliance-review", "audit"): {"agent": "compliance-reviewer", "skills": ("compliance-legal", "privacy-review")},
    ("release-review", "audit"): {"skills": ("compliance-legal", "privacy-review", "security-review")},
    ("incident-response", "audit"): {"agent": "sre-operator", "skills": ("incident-debugging", "why", "how", "principle-fix-root-causes")},
    ("incident-response", "implement"): {"agent": "sre-operator", "skills": ("incident-debugging", "deployment", "why", "how")},
    ("self-review", "audit"): {"agent": "code-reviewer", "skills": ("code-review", "codebase-design", "blast-radius", "principle-test-behavior-not-implementation")},
    ("sprint-plan", "plan"): {"agent": "project-manager", "skills": ("wayfinder", "to-tickets", "figure-it-out", "swarm")},
    ("self-improve", "implement"): {"skills": ("engineering-quality", "reflect", "principle-encode-lessons-in-structure", "maintain-verification-skill")},
    ("status-report", "report"): {"agent": "project-manager", "skills": ("plan-md",)},
}


def phases_for(workflow_id: str) -> tuple[Phase, ...]:
    base = BASE_PHASES
    out: list[Phase] = []
    for pid in WORKFLOW_PHASES.get(workflow_id, ()):
        phase = base.get(pid)
        if phase is None:
            continue
        ov = PHASE_OVERRIDES.get((workflow_id, pid))
        if ov:
            import dataclasses

            # Overrides are ADDITIVE: keep the base phase skills (privacy/security/
            # context/engineering) and append the workflow-specific ones.
            if "skills" in ov:
                merged = tuple(dict.fromkeys(tuple(phase.skills) + tuple(ov["skills"])))
                ov = {**ov, "skills": merged}
            phase = dataclasses.replace(phase, **ov)  # type: ignore[arg-type]
        out.append(phase)
    return tuple(out)


def phase_spec(workflow_id: str, phase_id: str) -> Phase | None:
    for p in phases_for(workflow_id):
        if p.id == phase_id:
            return p
    return None


def phase_dicts(workflow_id: str) -> list[dict[str, object]]:
    return [
        {
            "id": p.id,
            "goal": p.goal,
            "agent": p.agent,
            "skills": list(p.skills),
            "mcp_tools_allow": sorted(p.tools),
            "exit_criteria": list(p.exit_criteria),
            "parallel_group": p.parallel_group,
        }
        for p in phases_for(workflow_id)
    ]


def mcp_tools_allow_for_phase(workflow_id: str, phase_id: str) -> list[str]:
    p = phase_spec(workflow_id, phase_id)
    if p is None:
        return mcp_tools_allow(workflow_id)
    return sorted(p.tools)


def implement_allowed(workflow_id: str) -> bool:
    """Whether this workflow has an implement phase (if not, implementation requires a workflow switch)."""
    return any(p.id == "implement" for p in phases_for(workflow_id))


# Attach phases to WorkflowSpec (replace, since it is frozen)
import dataclasses as _dc  # noqa: E402

WORKFLOWS = {wid: _dc.replace(spec, phases=phases_for(wid)) for wid, spec in WORKFLOWS.items()}
WORKFLOW_AGENTS = {wid: spec.agent for wid, spec in WORKFLOWS.items()}


