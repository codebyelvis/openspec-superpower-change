# Change: Add scope-bound cross-CLI sync plans

## Why

`add-backend-architecture-review-continuity` is source-Review PASS but cannot
synchronize its two approved Router files. The current planner always emits the
entire portable manifest plus the managed global rule for every runtime: 29
Router files, 10 Companion files, and one global-rule operation per target.
Applying that plan would exceed the approved two-path mutation set.

Manual copies or a separate low-level sync tool would bypass the existing
prestate, durable receipt, rollback, ordered-target, verification, discovery,
and recovery mechanisms. The smallest safe repair is a scoped mode in the
existing sync planner that keeps those mechanisms and makes operation selection
explicit and plan-hash-bound.

## What Changes

- Add optional explicit portable-file selectors and an explicit managed-rule
  selector to the existing `plan` command.
- Emit a scoped plan schema that partitions every manifest file into selected
  operations and read-only assertions. Selected operations are the only
  mutation candidates; assertions retain full-manifest parity and prestate
  checks without rewriting unchanged files.
- Preserve legacy no-selector full-manifest plan behavior and existing durable
  apply/verify/discovery/commit/restore/recovery sequencing.
- Reject empty, duplicate, unknown, unsafe, non-v6, or target-incomplete scoped
  selections before plan creation.
- Keep managed global-rule mutation opt-in in scoped mode. An unselected rule is
  still parity-checked and prestate-bound but is never backed up or replaced.
- Bootstrap safely from an isolated temporary candidate tree: use the reviewed
  candidate to unblock the predecessor's exact two-file sync before promoting
  the candidate into canonical source. Then synchronize only this change's
  three portable source files.
- Add TDD coverage for operation closure, tamper resistance, prestate drift,
  unselected-byte preservation, durable rollback/recovery, full verification,
  and legacy compatibility.

## Non-Goals

- Inferring scope automatically from Git status or Diff.
- Changing the portable manifest, managed governance body, routing, OpenSpec,
  Completion, or target authority.
- Introducing a second state machine, another sync script, third-party
  dependency, low-level manual copy path, or Engineering Harness.
- Allowing scope to hide stale unselected files, global-rule drift, sensitive
  paths, unavailable targets, active legacy Handoffs, or failed discovery.
- Applying runtime changes, archiving either change, committing, pushing, or
  publishing before the required approval and Reviews.

## Impact

- Affected spec: `skill-workflow-governance`.
- Execute through a fresh direct Pi session switched to Luna Max after exact
  approval. Active OpenSpec `tasks.md` remains canonical progress; no external
  batch or Handoff state is created. A later external dispatch would require a
  separate schema-6 Handoff Plan and cannot reuse this inline assignment.
- Canonical source files after approval:
  - `scripts/validate_cross_cli_sync.py`
  - `tests/test_cross_cli_sync.py`
  - `references/cross-cli-sync.md`
  - `references/sync-checklist.md`
- Portable files introduced by this change's implementation: the script and two
  references above. Tests and OpenSpec/Plan artifacts are repository-only.
- Predecessor dependency:
  `add-backend-architecture-review-continuity` remains
  `BLOCKED_TARGETED_TOOLING` until the reviewed isolated candidate produces and
  executes an exact two-file plan.
- Change level: Major Self-Evolution because runtime mutation/evidence signoff
  behavior changes.

## Approval Status

- Change-id: `add-scoped-cross-cli-sync-plans`.
- The user authorized closed-loop analysis and creation of a Luna Max
  implementation Plan, not implementation, runtime apply, archive, or external
  dispatch.
- Implementation requires explicit approval of this exact change-id and scoped
  contract after Plan Preflight PASS.
- Git staging, commit, branch/worktree mutation, push, publication, runtime
  apply, archive, and destructive cleanup remain unauthorized until their
  existing gates are satisfied.
- Exact user approval: “批准 OpenSpec change-id add-scoped-cross-cli-sync-plans，按 docs/superpowers/plans/2026-08-26-scoped-cross-cli-sync-plans.md，由 Pi / openai-codex/gpt-5.6-luna / max 直接内联实施；授权 Plan 声明的四个 canonical files、Batch A/B runtime mutation sets 和动态 archive；不授权额外范围、Git commit/push 或发布。”
- [x] This exact change-id and scoped contract are approved for implementation.
