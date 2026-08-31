# Change: Optimize closed-loop runtime routing

Revision: `v1.15`

## Why

The workflow needs two small global behavior corrections:

1. make an actual model/reasoning switch explicit to the user; and
2. continue safe, reversible, already-authorized work after the user requests
   closed-loop progress, without repeatedly asking whether to continue.

The v1.14 implementation attempt also exposed a maintainability problem: a
documentation-level workflow correction grew into a custom 35-checker runner,
multiple schemas, a legacy adapter, and unrelated sync-failure commands. That
test and design machinery exceeded the behavior being changed, slowed delivery,
and would make later Skill maintenance harder.

## What Changes

- Define “闭环推进”, “继续闭环”, “按推荐方案推进”, and “完成后统一 Review”
  as bounded continuation intent inside the existing authorization.
- Continue safe, reversible, in-scope reads, edits, tests, verification,
  same-scope Review/Fix, and existing-state updates without repeated
  confirmation. Preserve every existing scope, risk, production, database,
  external-effect, destructive, Git, Review, and completion gate.
- Centralize short, non-authoritative model/reasoning recommendations in
  `agent-capability-routing.md`. Emit the six-field `运行环境建议` block only
  for an actual switch; omit it when the current runtime is sufficient.
- Keep runtime advice outside the schema-6 Handoff marker and canonical
  `status.md`; old schema-6 Handoffs without the block remain valid.
- Add a global proportionality rule: use the smallest design and artifact set
  that proves the approved behavior. Do not add a framework, state, registry,
  schema, fixture system, runner, or ledger when direct edits and existing
  validators are sufficient.
- Bound TDD and verification to the current task. RED/GREEN tests must exercise
  the changed behavior and credible regressions only. Do not create or run
  unrelated test matrices merely because they are available. Broader suites
  run only when an existing gate or the actual blast radius makes them relevant.
- Replace v1.14's custom fixture/runner/adapter/classifier work with a few direct
  assertions in the two existing workflow test files.

## Scope

### Source repositories

- `/Users/elvis/file/develop/opensource/openspec-superpower-change`
- `/Users/elvis/file/develop/opensource/codex-brief-antigravity-review`

The independent change-id remains
`optimize-closed-loop-runtime-routing`. No business change, including
`build-industry-stock-selection-v2`, is part of this work.

### Source files

Router:

- `SKILL.md`
- `references/approved-implementation-workflow.md`
- `references/confirmation-lease.md`
- `references/agent-capability-routing.md`
- `references/handoff-contract.md`
- `tests/test_workflow_rules.py`

Companion:

- `SKILL.md`
- `references/brief-template.md`
- `references/agy-dispatch-template.md`
- `references/handoff-contract.md`
- `tests/test_workflow_rules.py`

Cleanup-only path:

- Router `tests/test_cross_cli_sync.py` may be edited only to remove the
  v1.14 additions and restore its exact preimage. It must have zero final diff,
  is not implementation scope, and is not a runtime selector.
- Companion `references/handed-off-external-execution.md` may be restored to
  its exact preimage to preserve the existing governor hash contract. It must
  have zero final diff and is not a runtime selector.

The two Handoff references remain byte-identical. Existing portable-manifest
tooling synchronizes only the nine changed Skill/reference files to Codex, Pi,
Antigravity CLI, and Grok CLI.

### Removed from v1.15 scope

- the custom closed-loop JSON fixtures, schemas, checker registry, sensitivity
  runner, and forward-output format;
- the legacy reconciliation adapter and its fixtures;
- any final change to `tests/test_cross_cli_sync.py` or
  `references/handed-off-external-execution.md`, and any change to
  `scripts/validate_cross_cli_sync.py`, `references/cross-cli-sync.md`, or
  `references/sync-checklist.md`;
- any new lifecycle state, capability/evidence profile, task ledger, model
  registry, confirmation state machine, dispatch framework, or test framework.

## Acceptance Scenarios

1. A safe task with recommended option A proceeds without confirming A again.
2. A material business/architecture/security choice is asked once; after A is
   selected, safe approved work continues.
3. “按 A 闭环推进” continues later safe in-scope steps.
4. Closed-loop wording stops for database writes, production, release,
   destructive Git, external sending, or scope expansion.
5. An actual model switch states target Session, model, reasoning strength,
   reason, copyable prompt, and return target once.
6. No actual switch emits no runtime-advice block.
7. An old schema-6 Handoff without runtime advice remains valid.
8. A compact one- or two-file Direct Change remains lightweight.
9. Compaction/new-window/“继续” resumes from canonical state without re-asking.
10. A straightforward workflow edit uses existing files and validators rather
    than creating a new runner, schema family, registry, or ledger.
11. TDD runs focused tests for changed behavior; unrelated tests are not added
    or run unless an existing gate or demonstrated blast radius requires them.

## Evidence and Safety

This remains Major Self-Evolution because it changes global workflow behavior,
but evidence is proportional:

- retain the existing private preimage backup and rollback material;
- run focused RED/GREEN tests in the two existing workflow test files;
- run focused RED/GREEN during implementation, then run each repository's
  existing complete unittest suite once at the final source gate because the
  changed global files have repository-wide consumers;
- run the existing Router/Companion validators, quick validation, strict
  OpenSpec validation, Handoff byte/marker compatibility, a pre-apply
  path/hash-plan and target-snapshot Review, and one independent final Review
  after runtime synchronization;
- use the existing portable sync transaction and verify all four targets;
- do not run unrelated sync-classifier TDD or build another test harness.

No Git write, business-code edit, database/production operation, release,
deployment, external message, or cleanup of existing
`.transaction-blocked.*` / `.transaction-unsafe.*` files is authorized.

## Approval Status

- Change-id: `optimize-closed-loop-runtime-routing`
- Revision: `v1.15`
- Status: `approved_for_implementation_after_revision_review`
- User approval: the user explicitly replied “按 v1.15 精简闭环” and required
  the proportional-design/current-task-test rule to be global. This is the
  single approval for the exact reduced scope above; no repeated step approval
  is required while scope and risk remain unchanged.
