---
name: research-decision-room
description: Synthesize qualitative research into one HTML decision room (ledger, themes, opportunities, memo). Use in /research, /market-plan, /deck — not a replacement workflow.
triggers:
  - "research decision room"
  - "user research synthesis"
  - "research synthesis dashboard"
  - "evidence-backed product decision"
  - "interview synthesis"
  - "opportunity solution tree"
  - "usability findings dashboard"
  - "qualitative research board"
od:
  mode: prototype
  platform: desktop
  scenario: research
  preview:
    type: html
    entry: index.html
    reload: debounce-100
  design_system:
    requires: true
    sections: [color, typography, layout, components]
  craft:
    requires: [typography, color, accessibility-baseline, anti-ai-slop]
  inputs:
    - name: research_material
      type: string
      required: true
      description: "Interview notes, tickets, survey excerpts, analytics notes, or a product decision brief"
    - name: decision_scope
      type: string
      required: false
      description: "The product/design decision the team needs to make"
  outputs:
    primary: index.html
  example_prompt: "Synthesize 8 interview notes, 24 support tickets, and recent activation metrics into a research decision room for whether a project-management app should add an onboarding checklist or contextual inline tips."
  capabilities_required:
    - file_write
---

# Research Decision Room

Single-page HTML decision artifact: evidence, themes, confidence, tradeoffs, and experiments visible together — not a decorative deck.

**In workflows**: invoked from `/research`, `/market-plan`, or `/deck`. This skill is the **synthesis procedure**; workflow gates stay in each `commands/*.md`.

## Resource map

```text
research-decision-room/
├── SKILL.md
├── example.html
└── references/
    ├── checklist.md
    ├── evidence-model.md
    └── synthesis-workflow.md
```

Read `references/evidence-model.md` before synthesis. Full steps: `references/synthesis-workflow.md`. Before emit: `references/checklist.md`.

## When to use

- Mixed research material (interviews, support, surveys, analytics, product context).
- A decision that needs evidence ("Should we build X?", onboarding path, drop-off why).
- Stakeholders who will not read a long research report.

Do not use for pure visual inspiration, campaign ideation, or brand moodboards only.

## Workflow (summary)

1. Decision frame
2. Evidence ledger (`evidence-model.md`)
3. Themes and tensions
4. Opportunity matrix
5. Decision memo
6. Self-contained `index.html`
7. Checklist → emit `<artifact>`

Step-by-step detail: **`references/synthesis-workflow.md`**.