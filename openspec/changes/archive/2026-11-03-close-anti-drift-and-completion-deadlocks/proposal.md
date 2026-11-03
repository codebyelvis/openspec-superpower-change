# Change: Close anti-drift hanging states, completion deadlocks, and uninterrupted closed-loop execution

Change-ID: `close-anti-drift-and-completion-deadlocks`
Author: elvis
Status: APPROVED BY USER. In implementation.

## Gate 0

- Mode: Self-Evolution, implementation.
- Task: FIX
- References read: `SKILL.md`; `references/self-evolution-rule.md`; `references/step-evidence-gate.md`; `references/completion-contract.md`; `references/confirmation-lease.md`; `references/approved-implementation-workflow.md`; `references/openspec-decision-rule.md`.
- OpenSpec decision: Required. Gate 0 schema expansion, stop condition fallbacks, completion contract transitions, and delegated review continuity are workflow behavior. Change level: Major. Approved by user on 2026-11-03.
- Required Superpowers methods: implementation discipline with TDD / deterministic regression tests.
- Risk/evidence profile: strict.
- User confirmation required: granted.
- Next action: apply code edits, add deterministic tests, run validation and full test suite, verify clean state.

## Why

1. **Hanging references and unrecorded task type (F1)**:
   - `SKILL.md:111-112` stops on "a task-type change" and "reaching the round budget".
   - Gate 0 never recorded task type (`VERIFY`, `DIAGNOSE`, `FIX`, or `REVIEW`), making "task-type change" subjective and ungrounded.
   - The numeric round budget lives exclusively in private instructions (`~/.codex/AGENTS.md`) and is barred from repository sync. In public, distributed (npm, skills.sh), or multi-agent runtimes lacking private instructions, "reaching the round budget" is a hanging condition.
2. **Deadlock between pre-existing debt and completion loops (F2)**:
   - `SKILL.md:107-109` strictly prohibits repairing pre-existing failures found during verification.
   - `references/completion-contract.md:16-20, 59-60` requires fresh PASS for every required verification and unconditionally routes any FAIL back to the same scope for repair.
   - There was no explicit bridge converting an unrepairable pre-existing debt into a `BLOCKED` stop.
   - Completion contract lacked an upper attempt bound, overriding `SKILL.md`'s two-failure stop upon task closure.
3. **Friction in long-task continuity and delegated review (User explicit addendum)**:
   - When the user explicitly requests "闭环推进" (closed-loop execution) or delegates intermediate approvals/reviews to an advisory reviewer (such as grok-cc advisory review), the agent should not repeatedly pause for polite, redundant human confirmations between intermediate stages.
   - The agent must advance continuously once intermediate review PASS evidence is established, halting only for genuine blockers, breaker conditions (e.g. 2 failures, boundary escape), or user-reserved Git/production actions.

## What Changes

1. **Gate 0 task type recording**:
   - `SKILL.md` & `references/step-evidence-gate.md`: explicitly require recording `task: VERIFY|DIAGNOSE|FIX|REVIEW` in Gate 0.
2. **Numeric round budget fallback**:
   - `SKILL.md`: add fallback rule when local instructions define no numeric budget.
3. **Pre-existing failure handling & BLOCKED transition**:
   - `references/completion-contract.md`: specify that pre-existing debt (`OUT_OF_SCOPE_PREEXISTING_DEBT`) transitions to `BLOCKED`, `blocker_owner: user`, without entering self-repair.
4. **Completion loop bound & operational definitions**:
   - `references/completion-contract.md`: specify that `SKILL.md`'s two-failure and round-budget stops bound every loop. Define attempt and named slice.
5. **Uninterrupted closed-loop execution upon delegated review or closed-loop instruction**:
   - `SKILL.md`, `references/confirmation-lease.md`, and `references/approved-implementation-workflow.md`:
     When the user explicitly instructs closed-loop execution or delegates intermediate signoff to an advisory reviewer (e.g. grok-cc advisory review), intermediate transitions (Preflight PASS, slice verification, test fixes) proceed automatically without intermediate human pause. Pauses are reserved strictly for genuine `BLOCKED` issues, breaker fires (two failures, boundary violation), or explicit Git/release gates.
6. **Specification and regression tests**:
   - Update `openspec/specs/skill-workflow-governance/spec.md`.
   - Add deterministic unit tests in `tests/test_workflow_rules.py`.

## Canonical Paths and Hashes

- Repository root: `/Users/elvis/file/develop/opensource/openspec-superpower-change`
- Backup directory: `/Users/elvis/.codex/self-evolution-backups/20261103T103940-close-anti-drift-and-completion-deadlocks`
