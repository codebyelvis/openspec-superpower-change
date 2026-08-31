# Optimize Closed-Loop Runtime Routing v1.15

**Goal:** Ship the two workflow behavior fixes and the proportional
design/current-task-test rule with the smallest maintainable source and evidence
set.

**Change:** `optimize-closed-loop-runtime-routing` revision `v1.15`

## Boundaries

- Source scope: the implementation and cleanup-only files listed in the v1.15
  proposal.
- Runtime scope: nine changed Skill/reference selectors across Codex, Pi,
  Antigravity CLI, and Grok CLI through the existing portable manifest.
- No Git writes, business/database/production actions, external sending,
  deployment, release, or transaction-residue cleanup.
- Keep the existing private preimage backup and rollback material until final
  verification and runtime parity pass.
- Do not modify sync code or run sync-classifier TDD.

## Step 1: Remove v1.14-only machinery and create focused RED

Delete only these files created by this change:

- Router:
  - `tests/fixtures/closed-loop-runtime-routing-cases.json`
  - `tests/fixtures/closed-loop-runtime-routing-cases.schema.json`
  - `tests/fixtures/closed-loop-runtime-routing-output.schema.json`
  - `tests/fixtures/legacy-approved-roots.json`
  - `tests/fixtures/legacy-reconciliation.schema.json`
  - `tests/run_closed_loop_runtime_forward_tests.py`
  - `tests/reconcile_legacy_statuses.py`
- Companion:
  - `tests/fixtures/closed-loop-runtime-routing-cases.json`
  - `tests/fixtures/closed-loop-runtime-routing-cases.schema.json`

Remove only the v1.14 appended classifier helpers/classes from Router
`tests/test_cross_cli_sync.py` and prove that cleanup-only path has zero final
diff. Restore Companion `references/handed-off-external-execution.md` and its
fixed-hash test to their exact preimages; runtime advice remains in the
Companion Skill, Brief, dispatch, and Handoff references. Rewrite the two new
`ClosedLoopRuntimeRoutingTests` classes as three direct tests per repository.
The tests inspect existing source files and collectively cover the eleven v1.15
acceptance scenarios. They must not import a custom runner or fixture.

Run only those six focused tests for RED. The proportionality/current-task-test
assertions must fail before their source rule is added; setup/import errors do
not count as RED.

## Step 2: Complete minimal source behavior

Keep the already-implemented continuation and runtime-advice wording. Add one
concise owner section to Router
`references/approved-implementation-workflow.md`:

- smallest adequate design/artifact set;
- reuse existing rules/templates/validators/tests first;
- no new framework/schema/registry/runner/ledger when direct mechanisms work;
- TDD covers changed acceptance, changed contracts, and credible regressions;
- no unrelated test creation/execution without an existing gate or demonstrated
  blast radius;
- broader relevant gates remain mandatory.

Add only a short pointer in Router `SKILL.md`. Do not duplicate the full rule
in Companion or another reference.

Run the same six focused tests for GREEN.

## Step 3: Relevant source verification

Run the six focused tests during RED/GREEN. At the final source gate, run each
repository's complete existing unittest suite exactly once because the changed
global files have repository-wide consumers:

- `(cd /Users/elvis/file/develop/opensource/openspec-superpower-change &&
  PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 -m unittest discover -s
  tests -v)`;
- `(cd /Users/elvis/file/develop/opensource/codex-brief-antigravity-review &&
  PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 -m unittest discover -s
  tests -v)`;
- Router `scripts/validate_core_gates.py .`;
- Companion `scripts/validate_templates.py .`;
- both existing `quick_validate.py` checks;
- `openspec validate optimize-closed-loop-runtime-routing --strict
  --no-interactive`;
- byte parity for the two Handoff references and byte equality of the
  machine-readable marker against its preimage;
- forbidden scans for Luna in `agent_product`, new state/profile/ledger/
  registry terms, and runtime advice inside canonical marker material;
- source-scope audit and read-only `git diff --check`.

`test_cross_cli_sync.py` is not part of focused TDD; after exact preimage
restoration it runs only through the one required full-suite completion gate.

## Step 4: One Review, sync, and final verification

Generate one scoped portable plan for the nine changed Skill/reference files.
Before apply, the control plane Reviews its exact source/destination paths,
hashes, selected operations, and target snapshots.
Use the unchanged existing transaction to apply/verify Codex, Pi, Antigravity
CLI, and Grok CLI in manifest order. Stop on an existing transaction gate; do
not invent recovery behavior.

After all four targets pass, rerun the focused tests, validators, strict
validation, Handoff marker/parity, source/runtime hash parity, and read-only
`git diff --check`. Then use one fresh independent gate-bearing reviewer to
inspect the final source/runtime diff and evidence. Fix only actionable
in-scope findings and rerun relevant checks. Reconcile OpenSpec tasks and clean
only temporary material created by this change when rollback is no longer
required.
