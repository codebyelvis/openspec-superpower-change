# Tasks: Close anti-drift hanging states, completion deadlocks, and uninterrupted closed-loop execution

Change-ID: `close-anti-drift-and-completion-deadlocks`

## Phase 1: Proposal and Preflight
- [x] Create structured temporary backup with SHA256SUMS.
- [x] Author `proposal.md` and `design.md`.
- [x] Author delta `spec.md` in change directory.
- [x] Author prepared diffs in `diffs/`.
- [x] Run `validate_core_gates.py` on proposal structure.
- [x] Explicit user approval of change-id `close-anti-drift-and-completion-deadlocks` on 2026-11-03.

## Phase 2: Implementation
- [x] Update `SKILL.md` (Gate 0 task type, round budget fallback, and delegated review continuity).
- [x] Update `references/step-evidence-gate.md` (Gate 0 template).
- [x] Update `references/completion-contract.md` (pre-existing debt BLOCKED and loop bounds).
- [x] Update `references/confirmation-lease.md` (delegated review continuity).
- [x] Update `references/approved-implementation-workflow.md` (uninterrupted closed-loop continuation).
- [x] Update `openspec/specs/skill-workflow-governance/spec.md`.
- [x] Add deterministic regression tests in `tests/test_workflow_rules.py`.

## Phase 3: Verification and Closure (Current)
- [x] Run `scripts/validate_core_gates.py`.
- [x] Run `python3 /Users/elvis/.codex/skills/.system/skill-creator/scripts/quick_validate.py .`.
- [x] Run unit tests and regression tests in `tests/test_workflow_rules.py`.
- [x] Produce `evidence/phase-b.md`.
- [ ] Present completion summary and wait for user review.
