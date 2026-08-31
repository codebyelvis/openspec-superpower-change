# Tasks: optimize-closed-loop-runtime-routing

Artifact revision: `v1.15`

## 1. Revision and approval

- [x] 1.1 Restore the independent change boundary and inspect current Router,
  Companion, runtime, backup, transaction-residue, and dirty-worktree state.
- [x] 1.2 Reduce v1.14 to the exact v1.15 behavior, file, evidence, and removal
  scope approved by the user.
- [x] 1.3 Run strict OpenSpec validation for v1.15 (PASS).
- [x] 1.4 Complete one independent v1.15 revision Review. Reviewer
  `01a055e7-c281-7083-8409-70513e348a4a` returned PASS after the three
  bounded findings were corrected.
- [x] 1.5 Record the user's centralized approval: “按 v1.15 精简闭环”.

## 2. Safety and short plan

- [x] 2.1 Retain the existing private 77-entry preimage backup, rollback
  helpers, and transaction-marker non-cleanup boundary.
- [x] 2.2 Replace the v1.14 implementation plan with a short v1.15 plan that
  contains only removal, focused GREEN, relevant validation, Review, sync, and
  cleanup steps.
- [x] 2.3 Review and bind the short plan before the next source edit. Reviewed
  plan SHA-256:
  `967dd87d032abad83d0566b6b1e335123a026a4db4b307acf00048eaeb252706`.

## 3. Remove over-designed test infrastructure

- [x] 3.1 Remove only the v1.14 closed-loop fixture/schema/runner and legacy
  adapter files created by this change.
- [x] 3.2 Remove only the v1.14 classifier-test additions from
  `tests/test_cross_cli_sync.py`, require zero final diff for that cleanup-only
  path, and leave sync production code/references unchanged.
- [x] 3.3 Rewrite the two new workflow-test classes as direct focused
  assertions in the existing test files.
- [x] 3.4 Run focused RED before the proportionality rule is complete.

## 4. Minimal implementation

- [x] 4.1 Finalize the bounded continuation rule and proportional
  design/current-task-test budget in Router workflow guidance.
- [x] 4.2 Finalize centralized non-authoritative runtime advice and conditional
  six-field switch notice.
- [x] 4.3 Finalize Companion Brief/dispatch/Handoff presentation while keeping
  both Handoff references byte-identical and schema-6-marker compatible.
- [x] 4.4 Run focused GREEN for all eleven acceptance scenarios.

## 5. Relevant verification and Review

- [x] 5.1 Run each repository's existing complete unittest suite once, plus
  Router/Companion validators, both quick validators, strict validation,
  Handoff byte/marker checks, forbidden scans, source-scope audit, and read-only
  `git diff --check`.
- [x] 5.2 Fix the two actionable source-gate findings (Router missing `stat`
  import and Companion cleanup-only hash drift), then rerun the affected gates.

## 6. Runtime synchronization and closeout

- [x] 6.1 Generate a scoped portable plan for the nine changed Skill/reference
  files using the existing manifest and unchanged sync validator, then Review
  the path/hash plan and target snapshots before apply.
- [x] 6.2 Apply and verify Codex, Pi, Antigravity CLI, and Grok CLI in existing
  manifest order; stop on any existing transaction gate.
- [x] 6.3 Repeat focused and critical final verification against source and all
  four runtime targets, then obtain one independent gate-bearing final Review.
  Reviewer `01a05603-f080-7471-84bb-526b540b24e6` returned PASS on attempt 2
  after fresh mode-0600 gate evidence closed the single evidence-binding finding.
- [x] 6.4 Reconcile this task ledger, report residual risk and rollback, and
  move only this change's nine verified temporary backup/evidence/sync/
  isolated-forward-test
  directories to the system Trash without touching transaction residue.
- [x] 6.5 Do not execute Git writes during implementation or without separate
  publication authority. The user subsequently authorized same-scope source
  commits and pushes; business/database/production operations, external
  sending, deployment, destructive Git, and cleanup of existing transaction
  residue remain forbidden.
