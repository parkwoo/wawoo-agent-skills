---
title: wawoo-skills 카탈로그（98 Skills / 12 Workflows）
description: 공개 Agent Skills 및 MCP 워크플로 인덱스.
hide:
  - title
  - navigation
---

<div class="kit-catalog-root" markdown="1">

<div class="kit-catalog-hero" markdown="0">

<p class="kit-catalog-title">스킬·워크플로 목록</p>
<p class="kit-catalog-lead">오픈소스 워크플로 엔진: 증거 기반 단계.</p>
<p class="kit-catalog-usage">먼저 **workflow_get**, flow가 가리키는 skill만 **skill_get**.</p>
<p class="kit-catalog-hero-counts"><a href="https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/CAPABILITIES.md" target="_blank" rel="noopener noreferrer">GitHub CAPABILITIES</a> · 98 Skills · 21 Agents · 12 Workflows</p>
<div class="kit-catalog-hero-meta">
<div class="kit-doc-langs">
<a href="/cn/docs/skills-catalog/">简体中文</a>
  <span aria-hidden="true">·</span>
  <a href="/en/docs/skills-catalog/">English</a>
  <span aria-hidden="true">·</span>
  <a href="/ja/docs/skills-catalog/">日本語</a>
  <span aria-hidden="true">·</span>
  <strong>한국어</strong>
</div>
</div>
</div>

<h2 class="kit-catalog-tier" id="cat-workflows">Workflow（12）</h2>

<p class="kit-catalog-tier-lead"><code>workflow_get</code> 진입 명령.</p>

<div class="kit-catalog-table" markdown="1">


| 이름 | 설명 |
| --- | --- |
| [`/compliance-review`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/compliance-review.md) | Legal / privacy / security gate (compliance-legal → privacy-review → security-review → release-readiness) |
| [`/delivery-lite`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/delivery-lite.md) | Lightweight delivery — SSOT plan file state machine, minimal ceremony (L0–L1). Default for single-feature requests without full f… |
| [`/design-review`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/design-review.md) | UI design review (design-review → web-design-guidelines → accessibility-audit) |
| [`/feature-delivery`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/feature-delivery.md) | Deliver a feature through discovery, design, implementation, testing, review, and approval gates. |
| [`/incident-response`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/incident-response.md) | Investigate and safely resolve an incident or urgent regression with evidence and follow-up. |
| [`/release-review`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/release-review.md) | Prepare a release-review package with legal/compliance, privacy, version, security, test, artifact, remote, and rollback evidence… |
| [`/research`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/research.md) | Research → decision (research → product-discovery → to-spec/to-tickets) |
| [`/self-improve`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/self-improve.md) | Self-improvement (retro → pdca-cycle → self-review → plan-md) |
| [`/self-review`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/self-review.md) | Self-correction (code-review → code-skeptic → diagnosing-bugs/tdd → fix → verify) |
| [`/sprint-plan`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/sprint-plan.md) | Sprint planning L2 (wayfinder → to-tickets → priority/estimate/capacity → plan-md) |
| [`/status-report`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/status-report.md) | Progress / status report (ACTIVE or triage/to-tickets → progress/risk → plan-md) |
| [`/ui-delivery`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/ui-delivery.md) | Design, implement, and audit a web UI change across responsive and accessibility states. |

</div>


<h2 class="kit-catalog-tier" id="cat-agents">Agent（21）</h2>

<p class="kit-catalog-tier-lead">Workflow가 지정하는 역할.</p>

<div class="kit-catalog-table" markdown="1">


| 이름 | 설명 |
| --- | --- |
| [`accessibility-reviewer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/accessibility-reviewer.md) | Performs read-only accessibility review of user flows, semantic structure, keyboard operation, and responsive UI. |
| [`architect`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/architect.md) | Evaluates architecture alternatives, interfaces, dependencies, migration risk, and decision records. |
| [`Code Reviewer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/code-reviewer.md) | Senior software engineer conducting thorough code reviews |
| [`Code Simplifier`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/code-simplifier.md) | For simplifying/refactoring features of codebase |
| [`Code Skeptic`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/code-skeptic.md) | For when you need your code criticized like nobody's business |
| [`compliance-reviewer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/compliance-reviewer.md) | Legal, compliance, and privacy review gate for a change or release. Collects evidence and checklists; final legal judgment requir… |
| [`Data`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/data.md) | Run notebook-first data analysis by appending and executing cells for each request. |
| [`delivery-lead`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/delivery-lead.md) | Coordinates evidence-based delivery from scope through review without bypassing approvals. |
| [`docs-localization-reviewer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/docs-localization-reviewer.md) | Maintains factual technical documentation and equivalent localized content. |
| [`Documentation Specialist`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/docs-specialist.md) | Focus on writing documentation, markdown files, and other text-based files |
| [`Frontend Specialist`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/frontend-specialist.md) | Frontend developer expert in React, TypeScript, and modern CSS |
| [`implementer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/implementer.md) | Implements scoped software changes with project conventions, focused tests, and evidence-based reporting. |
| [`performance-reviewer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/performance-reviewer.md) | Reviews performance bottlenecks, measurement design, budgets, and regression safeguards. |
| [`product-owner`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/product-owner.md) | Clarifies user outcomes, priorities, scope, and acceptance criteria without inventing business decisions. |
| [`project-manager`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/project-manager.md) | Agile project and progress management for this project — sprint planning, status reporting, risk tracking, and delivery coordinat… |
| [`qa-engineer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/qa-engineer.md) | Designs test strategy, reproduces defects, evaluates verification evidence, and identifies coverage gaps. |
| [`release-manager`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/release-manager.md) | Prepares releases with version, legal, artifact, compatibility, rollback, and remote-verification checks. |
| [`security-reviewer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/security-reviewer.md) | Performs read-only security review of code, configuration, dependencies, and delivery changes. |
| [`sre-operator`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/sre-operator.md) | Performs cautious read-first operations analysis for logs, monitoring, incidents, and cloud environments. |
| [`wawoo-auto`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/wawoo-auto.md) | Default entry agent. Routes non-trivial requests to a wawoo workflow via MCP before any other tool, then executes that workflow. … |
| [`web-designer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/web-designer.md) | Designs and implements accessible responsive web interfaces, then audits rendered behavior before handoff. |

</div>


<h2 class="kit-catalog-tier" id="cat-skills">Skill（98）</h2>

<p class="kit-catalog-tier-lead">지명 시 <code>skill_get</code>.</p>

<div class="kit-catalog-table" markdown="1">


| 이름 | 설명 |
| --- | --- |
| [`accessibility-audit`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/accessibility-audit/SKILL.md) | Audit and improve web accessibility for semantic structure, keyboard operation, forms, focus, contrast, motion, assistive technol… |
| [`api-contract-design`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/api-contract-design/SKILL.md) | Design or review HTTP, RPC, event, or internal API contracts for clear inputs, outputs, errors, authentication, compatibility, an… |
| [`architecture-decision`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/architecture-decision/SKILL.md) | Evaluate software architecture choices, dependencies, interfaces, constraints, and tradeoffs, then produce a concise decision rec… |
| [`ask-matt`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/ask-matt/SKILL.md) | Ask which skill or flow fits your situation. A router over the skills in this repo. |
| [`benchmark-checklist`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/benchmark-checklist/SKILL.md) | "Vet a perf measurement (limiter, tuning, limits, errors, repeatability, relevance, and whether the work happened) before you rep… |
| [`blast-radius`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/blast-radius/SKILL.md) | "Find what a change could break somewhere else before it ships, beyond the diff, and prove the one fact it's safe because of by r… |
| [`change-readiness`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/change-readiness/SKILL.md) | Perform an evidence-based pre-handoff review of a non-trivial software change before requesting human or external audit. Use afte… |
| [`changelog`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/changelog/SKILL.md) | Generate and maintain user-facing changelog/release notes from git history (Conventional Commits) and keep version/tags consisten… |
| [`code-review`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/code-review/SKILL.md) | "Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this… |
| [`codebase-design`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/codebase-design/SKILL.md) | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening o… |
| [`compliance-legal`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/compliance-legal/SKILL.md) | Review OSS license obligations (MIT/Apache-2.0 attribution, NOTICE), SBOM, and product/service legal checklists (terms, privacy, … |
| [`content-guardrail`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/content-guardrail/SKILL.md) | Deterministic policy-as-data content gate (no model, no network) — checks text against deny terms, named regexes, built-in secret… |
| [`context-compression`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/context-compression/SKILL.md) | Deterministically compress and clean multi-turn conversation context with pure Python (no LLM, no network) — drop stale turns, de… |
| [`create-verification-skill`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/create-verification-skill/SKILL.md) | "Generate a project-local verification skill that drives your app the way a user does — any language, framework, or platform. Use… |
| [`data-egress-guard`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/data-egress-guard/SKILL.md) | Deterministically mask PII and secrets before sending text to an external LLM/API (no model, no network) — replaces spans with nu… |
| [`database-change-safety`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/database-change-safety/SKILL.md) | Plan, implement, and review schema changes, data migrations, backfills, and cleanup with integrity, availability, observability, … |
| [`dependency-upgrade`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/dependency-upgrade/SKILL.md) | Safely evaluate, apply, and verify software dependency, runtime, container-image, or toolchain upgrades with compatibility, secur… |
| [`deployment`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/deployment/SKILL.md) | Plan, execute, and verify a deployment or release (Docker Compose, image tagging, environment, migrations, health checks, rollbac… |
| [`design-brief`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/design-brief/SKILL.md) | Parse a structured design brief written in I-Lang protocol format into a concrete design spec. Eliminates ambiguity from vague re… |
| [`design-md`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/design-md/SKILL.md) | Create and maintain a DESIGN.md — a plain-text design-system document (Google Stitch format) that design and coding agents read t… |
| [`design-review`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/design-review/SKILL.md) | Designer Who Codes: visual audit then fixes with atomic commits and before/after screenshots. Useful for tightening shipped UI be… |
| [`diagnosing-bugs`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/diagnosing-bugs/SKILL.md) | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something br… |
| [`documentation-localization`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/documentation-localization/SKILL.md) | Write, review, and synchronize technical documentation and localized content for factual accuracy, usable instructions, links, me… |
| [`domain-modeling`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/domain-modeling/SKILL.md) | Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or record… |
| [`engineering-quality`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/engineering-quality/SKILL.md) | Plan and implement software changes with explicit scope, evidence-based verification, safe migrations, and rollback readiness. Us… |
| [`fal-gen`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/fal-gen/SKILL.md) | Batch-generate design images (avatars / illustrations / backgrounds / textures) with fal.ai. Use when a task needs generated or f… |
| [`figure-it-out`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/figure-it-out/SKILL.md) | "Design an auditable playbook when no narrower one fits: a large migration, an ambitious multi-part change, or work a human revie… |
| [`frontend-design`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/frontend-design/SKILL.md) | Create distinctive, production-grade frontend interfaces with strong visual direction, polished typography, considered layout, an… |
| [`frontend-guides-hub`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/frontend-guides-hub/SKILL.md) | Frontend/UI skill ラッター — /ui-delivery 向けに既存 skill へ段階的にルートする（110 個平铺を避ける）。 |
| [`grill-with-docs`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/grill-with-docs/SKILL.md) | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. |
| [`grilling`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/grilling/SKILL.md) | Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any '… |
| [`handoff`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/handoff/SKILL.md) | Compact the current conversation into a handoff document for another agent to pick up. |
| [`how`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/how/SKILL.md) | "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"wher… |
| [`imagegen-frontend-mobile`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/imagegen-frontend-mobile/SKILL.md) | A skill for high-quality image concepts for mobile apps. Provides prompts and visual direction for iOS/Android screens and flows … |
| [`implement`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/implement/SKILL.md) | "Implement a piece of work based on a spec or set of tickets." |
| [`implement-spec`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/implement-spec/SKILL.md) | "Implement the result of /to-spec and /to-tickets in code." |
| [`in-your-own-words`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/in-your-own-words/SKILL.md) | "Restate in your own words what you think the user's goals are and what problem they're trying to solve. Use for /in-your-own-wor… |
| [`incident-debugging`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/incident-debugging/SKILL.md) | Diagnose a software incident or high-impact defect through reproduction, evidence collection, fault isolation, mitigation, verifi… |
| [`language-policy`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/language-policy/SKILL.md) | Decide and enforce the writing language for code, engineering records, and explanatory docs via a three-tier policy (code = Engli… |
| [`legacy-web-scan`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/legacy-web-scan/SKILL.md) | Legacy Web パターン掃引 — MWG legacy-scan と社内ルールで modernization 候補を plan-md へ。 |
| [`maintain-verification-skill`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/maintain-verification-skill/SKILL.md) | "Periodic pass that keeps a project's verification skill and feature map honest: parallel source readers per feature, one live se… |
| [`memory`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/memory/SKILL.md) | Persist and recall durable project knowledge (decisions, constraints, gotchas, recurring fixes) across sessions. Use before start… |
| [`modern-web-guidance-bridge`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/modern-web-guidance-bridge/SKILL.md) | On-demand Modern Web Guidance via npx (search/retrieve/legacy-scan). External OSS bridge — do not fork guides into this kit. |
| [`openrouter-gen`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/openrouter-gen/SKILL.md) | Batch-generate design images via OpenRouter image models (default google/gemini-2.5-flash-image). Use for generated design assets… |
| [`pdca-cycle`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/pdca-cycle/SKILL.md) | Run a lightweight Plan-Do-Check-Act cycle for product, engineering, quality, or process improvements. Use when a request needs me… |
| [`performance-audit`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/performance-audit/SKILL.md) | Measure and improve application or web performance using representative workloads, bottleneck evidence, and regression safeguards… |
| [`plan-md`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/plan-md/SKILL.md) | Always save planning deliverables (fix plans, implementation plans, design direction, review responses) as a Markdown file. Use f… |
| [`pr`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/pr/SKILL.md) | "Use when writing a PR body." |
| [`principle-attack-the-premise`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-attack-the-premise/SKILL.md) | "Apply when two or more fixes that share one premise have failed the same gate. Write the premise down and test it directly befor… |
| [`principle-boundary-discipline`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-boundary-discipline/SKILL.md) | "Apply when wiring validation, error handling, or framework adapters. Concentrate guards at system boundaries (CLI, config, netwo… |
| [`principle-build-the-lever`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-build-the-lever/SKILL.md) | "Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, checks. Build the tool that does it or proves it… |
| [`principle-encode-lessons-in-structure`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-encode-lessons-in-structure/SKILL.md) | "Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. Encode the rule as a… |
| [`principle-exhaust-the-design-space`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-exhaust-the-design-space/SKILL.md) | "Apply when facing a novel UI interaction or architectural decision with no precedent in the codebase. Build 2-3 competing protot… |
| [`principle-experience-first`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-experience-first/SKILL.md) | "Apply when product, UX, or feature-scope tradeoffs come up. Choose user delight over implementation convenience; ship fewer poli… |
| [`principle-explain-the-number`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-explain-the-number/SKILL.md) | "Apply before you measure, and before you trust, report, or act on a number you measured: a speedup, a regression, a throughput, … |
| [`principle-fix-root-causes`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-fix-root-causes/SKILL.md) | "Apply when debugging. Trace each symptom back to the first place the system went wrong and fix it there. A guard is a fix only w… |
| [`principle-foundational-thinking`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-foundational-thinking/SKILL.md) | "Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent… |
| [`principle-guard-the-context-window`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-guard-the-context-window/SKILL.md) | "Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep sum… |
| [`principle-laziness-protocol`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-laziness-protocol/SKILL.md) | "Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading. Bias toward deletion … |
| [`principle-make-operations-idempotent`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-make-operations-idempotent/SKILL.md) | "Apply when designing commands, lifecycle steps, or processing loops that run amid crashes, restarts, and retries. Converge to th… |
| [`principle-migrate-callers-then-delete-legacy-apis`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md) | "Apply when introducing a new internal API while old callers still exist. Migrate callers and delete the old API in the same wave… |
| [`principle-minimize-reader-load`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-minimize-reader-load/SKILL.md) | "Apply when reviewing or shaping code that's hard to trace. Count layers between question and answer, and hidden state in the rea… |
| [`principle-model-the-domain`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-model-the-domain/SKILL.md) | "Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files." |
| [`principle-never-block-on-the-human`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-never-block-on-the-human/SKILL.md) | "Apply when tempted to ask 'should I do X?' on reversible work." |
| [`principle-outcome-oriented-execution`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-outcome-oriented-execution/SKILL.md) | "Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture; don't preserve… |
| [`principle-prove-it-works`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-prove-it-works/SKILL.md) | "Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, … |
| [`principle-redesign-from-first-principles`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-redesign-from-first-principles/SKILL.md) | "Apply when integrating a new requirement into an existing design." |
| [`principle-separate-before-serializing-shared-state`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-separate-before-serializing-shared-state/SKILL.md) | "Apply when concurrent actors might write to the same file, branch, key, or state object. Eliminate the sharing first; serialize … |
| [`principle-sequence-verifiable-units`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-sequence-verifiable-units/SKILL.md) | "Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break work into small… |
| [`principle-subtract-before-you-add`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-subtract-before-you-add/SKILL.md) | "Apply when sequencing an addition, refactor, or rewrite. Remove dead code, redundant validators, and stub references first, then… |
| [`principle-test-behavior-not-implementation`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-test-behavior-not-implementation/SKILL.md) | "Apply when you write, change, or keep a test. Assert what the code's users can observe, so that the test fails when that behavio… |
| [`principle-type-system-discipline`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-type-system-discipline/SKILL.md) | "Apply when designing types, reviewing a function signature, or writing code in any statically-typed language. Make illegal state… |
| [`privacy-review`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/privacy-review/SKILL.md) | Review personal data (PII) flows, minimization, retention, masking, logging, and cross-border handling for a feature or service. … |
| [`product-discovery`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/product-discovery/SKILL.md) | Turn an ambiguous product or feature request into a scoped problem statement, user outcome, acceptance criteria, priorities, risk… |
| [`prototype`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/prototype/SKILL.md) | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic f… |
| [`publication-boundary`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/publication-boundary/SKILL.md) | Keep internal development materials out of the public tree of an open-source repo. Use when adding docs or scripts, or auditing w… |
| [`recall`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/recall/SKILL.md) | "Reconstruct your recent working context from your own chat history, live state, and the shared record (user reports, prior fixes… |
| [`reference-design-contract`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/reference-design-contract/SKILL.md) | Turn vague taste, screenshots, URLs, product notes, or "make it feel like this" references into a grounded DESIGN.md plus an impl… |
| [`reflect`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/reflect/SKILL.md) | Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an exis… |
| [`release-readiness`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/release-readiness/SKILL.md) | Prepare and review a software release for versioning, legal files, changelog accuracy, tags, release notes, deployment checks, an… |
| [`research`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/research/SKILL.md) | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the u… |
| [`retro`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/retro/SKILL.md) | "Conduct a retrospective on a coding session." |
| [`security-review`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/security-review/SKILL.md) | Perform a read-first security review of application code, configuration, dependencies, and delivery changes. Use for requested se… |
| [`setup-matt-pocock-skills`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/setup-matt-pocock-skills/SKILL.md) | "Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run on… |
| [`sharpen`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/sharpen/SKILL.md) | "Make a task deeper, not bigger, then rewrite the prompt. Use for /sharpen." |
| [`show-me-your-work`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/show-me-your-work/SKILL.md) | "Keep a reviewable decision trail for long-running or unattended work: a TSV log with one row per decision (what, why, evidence, … |
| [`swarm`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/swarm/SKILL.md) | "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntl… |
| [`tdd`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/tdd/SKILL.md) | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or want… |
| [`teach`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/teach/SKILL.md) | Teach the user a new skill or concept, within this workspace. |
| [`test-engineering`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/test-engineering/SKILL.md) | Design, implement, diagnose, and review software tests with evidence-focused coverage across unit, integration, and end-to-end la… |
| [`to-spec`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/to-spec/SKILL.md) | "Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you'… ⚠️ |
| [`to-tickets`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/to-tickets/SKILL.md) | Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published… ⚠️ |
| [`triage`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/triage/SKILL.md) | Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready … ⚠️ |
| [`wayfinder`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/wayfinder/SKILL.md) | Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and r… |
| [`web-design-guidelines`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/web-design-guidelines/SKILL.md) | Review UI code for Web Interface Guidelines compliance by the Vercel engineering team. Covers layout, typography, color, motion, … |
| [`web-experience-design`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/web-experience-design/SKILL.md) | Design, implement, audit, and hand off web interfaces with evidence for user tasks, visual hierarchy, responsive behavior, access… |
| [`why`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/why/SKILL.md) | "Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds. Di… |
| [`writing-for-agents`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/writing-for-agents/SKILL.md) | Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md. |

</div>


<p class="kit-catalog-subhead"><strong>작업 → 워크플로</strong></p>

<div class="kit-catalog-quickref" markdown="1">

| 상황 | Workflow | 복사 문장 |
| --- | --- | --- |
| 소규모 | `/delivery-lite` | <code class="kit-catalog-copy" data-kit-copy-cmd="/delivery-lite">/delivery-lite</code> |
| 기능 전체 | `/feature-delivery` | <code class="kit-catalog-copy" data-kit-copy-cmd="/feature-delivery">/feature-delivery</code> |
| 장애 | `/incident-response` | <code class="kit-catalog-copy" data-kit-copy-cmd="/incident-response">/incident-response</code> |
| Web UI | `/ui-delivery` | <code class="kit-catalog-copy" data-kit-copy-cmd="/ui-delivery">/ui-delivery</code> |

</div>

<p class="kit-catalog-subhead"><strong>하이라이트</strong></p>

<div class="kit-catalog-highlights" markdown="1">

<article class="kit-catalog-highlight"><strong>워크플로</strong><p><code>/delivery-lite</code> 등 상태 기계.</p></article>

<article class="kit-catalog-highlight"><strong>context-compression</strong><p>LLM 없는 컨텍스트 압축.</p></article>

<article class="kit-catalog-highlight"><strong>data-egress-guard</strong><p>PII/비밀 마스킹.</p></article>

<article class="kit-catalog-highlight"><strong>code-review</strong><p>합입 전 리뷰.</p></article>

</div>

<p class="kit-catalog-footer">
생성 2026-11-20T14:08:23Z · [CAPABILITIES](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/CAPABILITIES.md)
 [사용 설명](usage.md) · [다운로드](/ko/download/)
</p>

</div>
