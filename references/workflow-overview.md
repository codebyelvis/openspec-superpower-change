# Workflow Overview

## Purpose

`openspec-superpower-change` is the project-level change gate for explicitly requested OpenSpec, change-gating, routing, skill self-evolution, and archive/distillation work. Ordinary questions, standalone read-only reviews, and everyday unconstrained edits do not auto-load this router.

When loaded, it decides:

- whether the request is review-only, discovery, proposal, approved implementation, `/autoloop` requirement verification, or direct change;
- whether OpenSpec approval is required;
- which Superpowers methods (if any) apply to the current phase;
- which Step Evidence Gate profile (`compact`, `standard`, `strict`) governs verification and review;
- when the bound control plane is allowed to claim whole-task completion.

## Four proportional lanes

```text
read applicable local instructions & task-relevant code/docs
-> record Gate 0 before state-changing action (one line for obvious local reversible work)
-> route into the matching proportional lane:

  1. Compact Direct Change (`references/direct-change-rule.md`)
     -> minimum edit -> relevant required checks -> focused inline diff/self-review (no standalone Plan, Preflight, or status.md)

  2. Requirement Closed-Loop (`docs/req/*.md` + `/autoloop`, `references/autoloop-req-acceptance.md`)
     -> auto-match or session-distill `docs/req/*.md` -> minimal implementation & local fast check
     -> `scripts/autoloop_ctl.py run` (governed background verification + isolated read-only AGY review, <= 2 repair rounds)

  3. OpenSpec-Backed Implementation (`references/proposal-workflow.md` -> `references/approved-implementation-workflow.md`)
     -> clarify domain language when needed (`grill-with-docs` / `brainstorming`)
     -> draft & `openspec validate <change-id> --strict` -> stop for explicit user approval
     -> execute directly when OpenSpec `design.md` + `tasks.md` define the Four Hard Anchors; otherwise create a Superpowers plan and run bounded Preflight (`FULL_PREFLIGHT` + at most one `FOCUSED_RECHECK`)
     -> execute cohesive business slices -> verify -> distinct Review -> Project Learning Closeout when triggered
     -> fresh final verification & Final Review (or single consolidated post-verification Review on eligible single-slice standard work)
     -> reconcile `tasks.md`, archive when appropriate, and strict-validate after archive

  4. External Handoff / Cross-Window Session Resume (`references/handoff-contract.md` + `status.md`)
     -> lazy `docs/agent-collab/<change-id>/status.md` checkpoint on pause/compaction/handoff (schema-6 Handoff + schema-2 hashed evidence manifests)
```

## Orchestration model

```text
grill-with-docs / brainstorming when domain language or material boundaries are unclear
  -> OpenSpec as the single approved design contract when protected boundaries change
  -> Four Hard Anchors (or Superpowers plan + bounded Preflight) + `/autoloop` / Step Evidence Gate for disciplined execution and verification
```

## Artifact boundaries

For OpenSpec-backed and governed external work:

- OpenSpec artifacts: `openspec/changes/<change-id>/proposal.md`, `tasks.md`, optional `design.md`, and spec deltas (serving directly as the executable plan when the Four Hard Anchors are present).
- Separate Superpowers plan (`docs/superpowers/plans/YYYY-MM-DD-<change-id>.md`): required only when OpenSpec execution anchors are absent or multi-step non-anchored planning is needed.
- Canonical collaboration / resume ledger: `docs/agent-collab/<change-id>/status.md` (created lazily on pause/compaction/handoff for compact/standard local work; created at approval for strict/self-evolution and schema-6 external handoff).
- For external or `autoloop` work: schema-6 Handoff Contract and schema-2 `COOP_EVIDENCE_MANIFEST` hashed attempt/review/final evidence artifacts.

Optional discovery artifacts:

- `CONTEXT.md` glossary entries.
- `docs/adr/NNNN-slug.md` only for decisions that are hard to reverse, surprising without context, and based on a real trade-off.

## Governance boundaries

- OpenSpec defines what changes, why it changes, and what acceptance scenarios must hold.
- Superpowers and `/autoloop` provide proportional planning, TDD, debugging, verification, and independent read-only review discipline.
- Step Evidence Gate (`references/step-evidence-gate.md`) defines slice-level progress evidence and signoff conditions.
- Completion Contract (`references/completion-contract.md`) owns whole-task completion claims.

## Companion Skill Boundary

`codex-brief-antigravity-review` works standalone for task prompts, briefs, checklists, and read-only diff/evidence review, and consumes the schema-6 Handoff Contract when governing external execution. Daily feature slices without protected OpenSpec contract changes can also enter `/autoloop` directly while escalating to this router whenever unapproved Major or protected boundaries are touched.
