# Change: Streamline simple-change gates

## Why

The current workflow can turn a bounded change into several overlapping
artifacts and Review passes: Brief, Plan, repeated Preflight, separate test
specification and test-quality Reviews, Implementation Review, and Final
Review. This adds latency without improving evidence when the contract, risk,
and implementation slice are already clear.

## What Changes

- Give low-risk Direct Change an inline fast path: no standalone Brief, Plan, or
  Preflight artifact; retain scoped readiness, focused verification, and Review.
- Use one short executable Plan for a single OpenSpec-backed or standard slice;
  do not create a duplicate Brief for inline execution.
- Bound one unchanged-contract Preflight lineage to one `FULL_PREFLIGHT` and at
  most one terminal `FOCUSED_RECHECK`. A second blocked result stops for
  control-plane/user boundary resolution; no third automatic Preflight occurs.
- Require the first Preflight to consolidate all reasonably discoverable
  findings. Same-scope implementation findings return directly to Fix ->
  focused Verify -> implementation Review and do not reopen Preflight.
- Treat test-specification and test-quality inspection as concerns inside the
  implementation/final Review, not mandatory standalone gates.
- Keep TDD proportional: one focused regression per distinct changed behavior
  or credible failure class is sufficient unless another case exercises a
  genuinely different mechanism or risk.
- Permit one post-implementation Review, run after fresh final verification, to
  satisfy both implementation and final Review for compact or standard
  single-slice inline work when it covers the complete diff and no later change
  occurs.
- Preserve full independent Preflight/Review separation for strict effects,
  external Handoffs, multi-slice work, and protected-boundary changes.

## Scope

- `SKILL.md`
- `references/approved-implementation-workflow.md`
- `references/direct-change-rule.md`
- `references/request-modes.md`
- `references/step-evidence-gate.md`
- `references/completion-contract.md`
- `references/self-evolution-rule.md`
- `docs/engineering-invariants.md`
- `tests/test_workflow_rules.py`

No new evidence profile, lifecycle state, schema, registry, runner, task ledger,
or external tool is introduced. Git writes and publication remain separately
authorized.

## Acceptance

1. A compact, reversible Direct Change proceeds from inline readiness to edit,
   focused verification, and concise Review without standalone Brief/Plan/
   Preflight artifacts.
2. A single-slice standard or OpenSpec-backed change uses at most one short Plan
   and one initial Preflight.
3. A blocked Preflight receives one consolidated correction and at most one
   terminal recheck; another blocked result stops rather than starting R3+.
4. Same-scope implementation Review findings do not trigger a new Preflight.
5. Test-spec and test-quality concerns are checked in one implementation/final
   Review unless risk or a concrete failure requires a specialist pass.
6. TDD and verification cover changed behavior and demonstrated blast radius,
   without multiplying equivalent cases or running unrelated suites.
7. Strict, external, multi-slice, security, persistence/write, migration,
   recovery, deployment, destructive, and production-authority work keeps its
   existing full gates.
8. Model identity never weakens a gate; stronger models only make inline
   execution the preferred implementation location when the risk profile
   already permits it.

## Approval Status

- Change-id: `streamline-simple-change-gates`
- Status: `approved_for_implementation`
- User approval: “批准 闭环推进” on 2026-09-04, after the exact change-id
  and scoped contract were presented.
