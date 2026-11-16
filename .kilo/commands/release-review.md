---
description: Prepare a release-review package with legal/compliance, privacy, version, security, test, artifact, remote, and rollback evidence before publication approval.
agent: release-manager
replay: safe
---

# Release Review

1. Use `release-readiness` to inspect working tree, version, compatibility, LICENSE, README, changelog/release notes, manifests, tests, and rollback.
2. **Legal/compliance gate**: use `compliance-legal` (OSS license/NOTICE/SBOM; terms/privacy/DPA checks) and `privacy-review` (PII, retention, masking). **Legal decisions require human approval**.
3. Use `security-review` for security boundaries and `documentation-localization` for public/multilingual release documentation.
   - **Delegation efficiency**: when delegating an audit to `security-reviewer` etc. via `Task`, inline the key points of the needed skills in the task text and do not let the child re-fetch the same skill with `skill_get`. The child is read-only (shell is a read-only subset) and restricts `read` to line ranges.
4. Run `change-readiness` and provide verified versus unverified remote state.
5. Present the release package for explicit approval. Do not push, tag, publish, deploy, or create a GitHub Release before that approval.

## Privacy / security / context

- Before any external LLM/API call or returning output: `guard_content` (policy gate) → `mask_pii` / `redact_infra` (redact) — see `data-egress-guard`.
- Never echo internal IPs, hosts, URLs, ports, or credentials in errors or logs.
- When context is long or repetitive: `context-compression` (MCP `compress_context`) + `principle-guard-the-context-window`.
- Security/privacy review: `security-review` / `privacy-review` (audit phase).
