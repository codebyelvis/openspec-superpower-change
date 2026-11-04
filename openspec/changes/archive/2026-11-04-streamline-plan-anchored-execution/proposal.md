# Change: Streamline plan-anchored execution and coarse-grained batches

## Why

As underlying coding agents become stronger at long-context reasoning, single-pass implementation, and native test execution, legacy ceremony designed to police weak models has become counterproductive:

1. **Duplicate planning artifacts**: Requiring a standalone Superpowers implementation plan and separate JSON Preflight artifacts even when an approved OpenSpec (`proposal.md` + `design.md` + `tasks.md`) already specifies exact files, cohesive slices, and verification commands slows down entry without adding safety.
2. **Overly fine-grained slicing and micro-step ceremony**: Breaking cohesive work into micro-steps with standalone intermediate JSON artifacts (`red-green.json`, `native-green.json`, `approval-provenance.json`) restricts model autonomy and multiplies round-trips.
3. **Manual SHA-256 ledger friction**: Eagerly creating `docs/agent-collab/<change-id>/status.md` for single-session work and including non-code metadata (`CHANGELOG.md`, task ledgers, prior Review/Evidence reports) in `verified_revision.inputs` causes self-hash invalidation loops during closeout.
4. **Cold-path context bloat**: `references/approved-implementation-workflow.md` mixes everyday execution rules with ~260 lines of rare session-recovery and control-plane rebind/return protocols.

The desired workflow is **Anchor-at-Ends, Free-in-Middle**: a high-capability model defines a clear, four-anchor Plan at the start and performs a rigorous complete-diff + regression Review at the end, while any capable executor model implements the cohesive batch freely in the middle guarded by real regression tests.

## What Changes

- **Four-anchor OpenSpec/Plan unification**: Allow an approved OpenSpec (`design.md` + `tasks.md`) that already specifies the four execution anchors—(1) allowed/forbidden file scope, (2) target interfaces and `path:line` code facts, (3) coarse-grained cohesive batches, and (4) exact regression test commands and assertions—to serve directly as the executable Plan without generating a duplicate Superpowers Plan or standalone local Preflight JSON files.
- **Coarse-grained cohesive execution & inline RED/GREEN**: Default implementation to one cohesive business batch (or 2–3 milestone batches for large cross-subsystem changes) rather than micro-steps. Preserve executor freedom inside the approved scope and verify behavior via real regression tests, recording concise inline RED-to-GREEN evidence (failing test name, non-zero exit code, and one-line failure summary -> passing exit code) in the final report instead of standalone intermediate JSON files.
- **Bounded bugfix Direct Change**: Allow localized bugfixes restoring intended behavior to use Direct Change without requiring a pre-existing approved spec path in Gate 0 when three hard conditions hold: (1) a failing-then-passing regression test proves the fix, (2) no external API/schema/permission/lifecycle contract changes, and (3) blast radius is bounded by the local diff.
- **Lazy `status.md` creation & clean `verified_revision.inputs`**: Keep `status.md` lazy for `compact` and `standard` local work (persisted only before an intentional stop, compaction, or window handoff). For `strict` and `self-evolution`, create `status.md` once at approval and refresh only at review/completion boundaries. Restrict `verified_revision.inputs` strictly to verified source, rule, and test files—excluding `CHANGELOG.md`, task ledgers, and Review/Evidence reports to prevent closeout hash-cycle invalidation.
- **In-place hot/cold path partitioning**: Partition `references/approved-implementation-workflow.md` into an upfront hot-path trunk (read for everyday implementation) and a clearly marked cold-path reference section (`Project Session Resume` and control-plane rebind/return, read only on session recovery or rebind), avoiding new file creation or manifest churn.
- **Remove deprecated `grok-cc` references**: Remove obsolete `grok-cc` examples and consultation paragraphs from active workflow references (`references/approved-implementation-workflow.md`, `references/confirmation-lease.md`, `references/local-instruction-checkpoint.md`, `docs/engineering-invariants.md`, and `openspec/specs/skill-workflow-governance/spec.md`) while keeping generic delegated advisory review support intact.

## Scope

- `SKILL.md`
- `references/approved-implementation-workflow.md`
- `references/confirmation-lease.md`
- `references/local-instruction-checkpoint.md`
- `references/direct-change-rule.md`
- `references/step-evidence-gate.md`
- `references/completion-contract.md`
- `docs/engineering-invariants.md`
- `openspec/specs/skill-workflow-governance/spec.md`
- `tests/test_workflow_rules.py`
- Generated/runtime mirrors synced via existing tools (`skills/openspec-superpower-change/SKILL.md`, `distribution/`)

No new schema, lifecycle state, runner, or manifest file is added. Existing dirty workspace files (`scripts/validate_core_gates.py`, `scripts/validate_cross_cli_sync.py`, `references/jev/`, etc.) remain untouched.

## Approval Status

- Change-id: `streamline-plan-anchored-execution`
- Status: `approved_for_implementation`
- User approval: Explicitly approved via “批准按 streamline-plan-anchored-execution 闭环推进” on 2026-11-04 after reviewing the independent agent review and converged 4-item design draft.
