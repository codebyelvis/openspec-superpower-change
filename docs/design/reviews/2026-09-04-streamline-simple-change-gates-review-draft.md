# streamline-simple-change-gates Review Draft

## Classification

- Mode: Self-Evolution
- Level: Major
- Change-id: `streamline-simple-change-gates`
- Approval state: explicitly approved by the user on 2026-09-04

## Observed failure

A bounded single-slice change can accumulate duplicate Brief/Plan artifacts,
multiple Preflight rounds, separate test-spec and test-quality gates, and
separate implementation/final Reviews. The support process can exceed the
change and delay delivery.

## Desired behavior

- Compact Direct Change: inline readiness -> edit -> focused verify -> Review.
- Single-slice standard/OpenSpec: one short Plan, one initial Preflight.
- Unchanged-contract Preflight: one full pass plus at most one terminal focused
  recheck; never R3+ automatically.
- Same-scope implementation findings do not reopen Preflight.
- Test concerns are reviewed once with the implementation by default.
- Strict/external/multi-slice/protected-boundary work remains unchanged.

## Files and exact rule changes

The approved source scope is exactly the nine files listed in the proposal.
Rules will add the compact inline fast path, two-pass Preflight ceiling,
single-slice combined Review, and focused TDD budget. They will remove only
contradictory universal wording that mandates standalone Preflight or duplicate
Review for every path.

## Validation and forward test

- Existing `tests/test_workflow_rules.py`: add only direct assertions for the
  compact path, two-pass ceiling, no Preflight reopen, combined Review, and
  strict preservation.
- Run the focused test class/methods, quick validator, core gates, and the full
  project unittest suite once after source stabilization.
- Run exactly these two isolated static contract scenarios:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_workflow_rules.WorkflowRulesTest.test_compact_direct_change_uses_inline_fast_path -v
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_workflow_rules.WorkflowRulesTest.test_strict_security_recovery_preserves_full_gates -v
  ```

- This Major protected-boundary change retains a separate independent
  Implementation Review before runtime sync and a separate independent Final
  Review after fresh verification. Same-scope findings return to focused
  verification and the same Review stage, not to Preflight.
- Runtime sync is schema-v2 scoped to the seven manifest-declared changed files
  and uses the exact four-target
  plan/apply/verify/verify-discovery/commit/verify-all sequence and per-target
  pre-commit restore commands in the implementation Plan. Grok discovery is
  bound to a mode-0600 `grok inspect --json` artifact and consuming validation.
  Post-commit abandonment uses a newly reviewed reverse sync plan from the
  validated source backup; a verified receipt is never passed to
  `restore-target`. Runtime roots are
  `/Users/elvis/.codex/skills`, `/Users/elvis/.pi/agent/skills`,
  `/Users/elvis/.gemini/antigravity-cli/skills`, and
  `/Users/elvis/.grok/skills`.

## Worktree boundary

Execute in
`/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-skillsmp-index-adapter`
on branch `add-skillsmp-index-adapter`, base
`272e37467f2ec8b29a72daac61c873bc612d12d2`. Preserve the coexisting
`add-skillsmp-index-adapter` diff; this Review covers only the approved
governance paths and their change evidence.

## Rollback

Restore the nine source files from
`/tmp/openspec-review-flow-backup.7cZ0C2`; do not use destructive Git.
