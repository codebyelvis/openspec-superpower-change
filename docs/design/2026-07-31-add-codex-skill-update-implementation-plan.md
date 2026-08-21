# Implementable Plan: add-codex-skill-update (change-id: add-codex-skill-update)

Date: 2026-07-31
Mode: standard implementation (strict)
Risk profile: high (runtime control, deployment, rollback, recovery, scheduled mutation)
Precondition: `2.1` and `2.2` are PASS with exact approved artifact bytes still frozen.

## Scope

Implement all slices under tasks `3.1`→`3.6`, `4.1`→`4.5`, and `5.1`→`5.7` from
the approved OpenSpec contract. No scope expansion.

## Hard "do not do" constraints

1. No `git add/commit/reset/clean/clone/push/pull` as a mutation primitive during
   implementation slices.
2. No mutation outside:
   - current repository candidate files (`openspec/changes/add-codex-skill-update/**`,
     `tests/**`, `references/**`, `scripts/**`, root `README*`, changelog),
   - target sibling source and sibling source build payload, and runtime targets
     listed in task 6.
3. Do not use `git` as a mutation path inside candidate update logic except through the
   approved `bootstrap-apply`/`apply` bounded flows.
4. Candidate Skill body must remain read-only for `audit/plan/verify`; all mutation
   routes must return to Router-owned transactions only.
5. No publish/push without explicit user approval.

## Step 0 — Preflight-aligned bootstrap

No implementation change before this plan is accepted by the distinct Preflight Review.

Allowed files (read/write once plan starts):
- `openspec/changes/add-codex-skill-update/tasks.md` (mark milestones only)
- `openspec/changes/add-codex-skill-update/approvals/**` (frozen until re-approval)

Verification commands:
- `openspec validate add-codex-skill-update --strict`
- `"${PYTHON_BIN:-python3}" "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" .`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`

Stop condition:
- If any required command fails, revision plan text; rerun until PASS.

## Step 1 — Sibling Skill skeleton and bilingual docs

Goal: satisfy task 3.1 by creating minimal candidate package, metadata, references, and docs.

Exact files to add in sibling source:
- `AGENTS.md`
- `SKILL.md`
- `agents/openai.yaml`
- `references/runtime-manifest.json`
- `references/update-contract.md`
- `references/installation-modes.md`
- `references/version-ledger.md`
- `scripts/codex_skill_update.py`
- `scripts/validate_update_contract.py`
- `templates/registry.example.json`
- `templates/com.openai.codex.skill-update-audit.plist`
- `tests/test_skill_contract.py`
- `tests/test_update_engine.py`
- `tests/fixtures/forward-cases.json`
- `README.md`
- `README_cn.md`

Allowed source files outside sibling source for same slice:
- `openspec/changes/add-codex-skill-update/tasks.md` (checklist updates only)
- `openspec/changes/add-codex-skill-update/approvals/artifacts/**` (no change in file set)
- `docs/design/2026-07-30-governed-skill-update-review-draft.md` (archival snapshot for context only, no edits)

Additions:
- deterministic manifest schema and command parsing
- fixed non-mutating `audit`, `plan`, `verify` output fields
- closed adapter contracts and notification redaction

Rollback:
- remove the entire untracked sibling source directory from temp workspace
- restore edited source files from working tree baseline

Step Evidence Gate:
- Before implementation: evidence and rollback paths recorded
- After this slice: run tests in 5.3 and 5.5 for contract-level and forward-case parsing

## Step 2 — Contract tests and RED baseline

Goal: satisfy tasks 3.2 and 3.3 by building negative and boundary coverage that must fail on current revision.

Exact files to add/update:
- `tests/fixtures/forward-cases.json`
- `tests/test_skill_contract.py`
- `tests/test_update_engine.py`
- any required `tests/fixtures/` minimal helper fixtures

Required tests to add before GREEN:
- non-mutating parser behavior for `allow_implicit_invocation`
- mutation-path must return Router handoff contract in public flow
- adapter command whitelist/argv schema rejection
- unknown/absent reason and transaction fields
- dirty/ahead worktree and repo/Git binary prestate hard failures
- source-worktree and root-lock mismatch failures
- candidate tamper, checksum, recovery, and restart paths

Verification commands:
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`

Roll back:
- remove test additions and any partial engine scaffold if a hard fail prevents GREEN coverage

Step Evidence Gate:
- `2.1` RED evidence must be preserved in design/evidence report before this slice moves green.

## Step 3 — Contract and engine core implementation

Goal: implement source-side controller and registry model per tasks `3.4` and `3.5`, with immutable candidate handling.

Exact files to add/update (Router repo):
- `scripts/validate_update_contract.py`
- `tests/test_workflow_rules.py` (if shared governance checks extend to add-codex)
- `openspec/specs/skill-update-governance/spec.md` (contract text already approved)
- `references/agent-capability-routing.md`, `references/step-evidence-gate.md` (only if boundary changed by implementation)
- any engine utility modules added under sibling source `scripts/` (as above)

Implementation checkpoints:
- enforce immutable registry binding + separate registry-replace path
- build global managed-root ownership graph validation
- add explicit reason/result precedence and after-fingerprint checks
- implement `MUTATION_INTENT`, pre-check journal, operation lock, revocation lock
- implement post-success rollback and explicit receipt writing

Verification:
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`
- `python3 -m unittest discover -s tests/forward`

Rollback:
- restore engine modules and test harness to post-Step 2 state while preserving approved untracked artifacts.

Stop condition:
- no action can proceed past this slice without explicit Step Evidence Gate checkpoint and passing local verification.

## Step 4 — Runtime release and first bootstrap authority root

Goal: satisfy task `4.1` by creating immutable release and controlled bootstrap authority root.

Exact files/state to mutate:
- `~/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update/...` (workspace)
- `${CODEX_HOME}/openspec-superpower-change/bootstrap-control/codex-skill-update/` (manifest-bound workspace)
- `${CODEX_HOME}/skill-releases/codex-skill-update/<payload-sha256>/payload/`
- `${CODEX_HOME}/skill-releases/codex-skill-update/<payload-sha256>/runtime-lock.json`
- `openspec/changes/add-codex-skill-update/approvals/<manifest-sha256>.json`

Command class:
- plan-bound `bootstrap-apply` plan generation (Router-only)
- plan-bound `bootstrap-apply` approval and validation
- staged release-lock generation from reviewed manifest allowlist only
- immutable payload materialization and atomic symlink/candidate operations

Rollback:
- restore governance workspace to prior manifest-specific workspace
- keep one prior verified release for rollback
- if `bootstrap-apply` is not fully complete, keep `MUTATION_INTENT` and recover path active, block all new slice advances

Verification:
- `openspec validate add-codex-skill-update --strict`
- targeted bootstrap-invariant checks from `tests/test_update_engine.py`

Step Evidence Gate:
- mark as one complete risk milestone (closeout snapshot now records:
  exact workspace hash, manifest hash, runtime lock closure, and parent chain)

## Step 5 — Schedule transaction, install, and audit readiness

Goal: satisfy tasks `4.2`→`4.3` and route execution prep for task `6.x`.

Exact files/state to mutate:
- `templates/com.openai.codex.skill-update-audit.plist`
- `${CODEX_HOME}/skill-update/state.json` (or equivalent configured state root)
- schedule-specific state records under bootstrap workspace and task-specific plan store

Execution flow:
1. generate `schedule-install` plan
2. obtain scope-bound approval
3. perform exact replacement (install/replace, never uninstall-first mutation)
4. verify launchd binding:
   - label/domain
   - payload digest + runtime-lock hash
   - loaded-config fingerprint
   - Weekday=1 Hour=10 Minute=0

Rollback:
- plan-bound schedule-remove candidate with receipt-bound cleanup
- preserve existing schedule if replacement proof cannot be established
- no rollback that mutates controller while approval expired/revoked

Verification:
- run one scheduled job once in isolated test root
- assert only scheduled read-only paths changed

## Step 6 — Green stabilization and package/runtime sync evidence

Goal: satisfy tasks `6.1`→`6.4`, `4.3`→`4.5`, `5.1`→`5.5`.

Exact files:
- current repo `README.md` / `README_cn.md`
- `tests/test_workflow_rules.py` (cross-target parity and migration assertions)
- `openspec/changes/add-codex-skill-update/specs/skill-update-governance/spec.md` (alignment checks)
- root `README.md` / `README_cn.md` updates and changelog entries

Verification commands:
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`
- `python3 scripts/validate_core_gates.py .`
- `openspec validate add-codex-skill-update --strict`
- sibling release verification for runtime lock payload parity
- run the 7 forward scenarios (answer-free) in same identity set and preserve each output artifact

Rollback:
- no runtime claim if any invariant fails;
- restore changed README/changelog and keep controlled workspace intact until all pass

## Step 7 — Closeout risk milestone

Goal: satisfy tasks `5.6`→`5.7`, `6.5`→`6.7` and pre-closeout invariant.

Exact files:
- `openspec/changes/add-codex-skill-update/tasks.md`
- `docs/design/reviews/2026-07-30-governed-skill-update-review-draft.md` (if updated)
- `docs/design/2026-07-20-final-verification.md` and `docs/design/evidence/**` (runtime/sync/final forward evidence)
- `docs/design/evidence/**` and `docs/design/reviews/**` generated in this change
- `openspec/changes/archive/...` (post-closeout archive if required)

Requirements:
- no further source/runtime claims after risk milestone unless explicit new approval
- preserve raw-trace deletion receipts
- final pre-verification and final verification run from clean checkpoints

Rollback:
- if residual risk remains, stop on final milestone, fix residual, rerun evidence and only then unpause execution.

## Review and stop conditions by milestone

1. Milestone-1 (`3.1` complete): plan-bound RED-to-first-GREEN proof; no runtime bytes written.
2. Milestone-2 (`3.5` complete): contract engine can produce stable plan/receipt/reason output.
3. Milestone-3 (`4.1` complete): bootstrap authority workspace and first manifest-bound release are intact and verifiable.
4. Milestone-4 (`4.3` complete): schedule replace/install is deterministic and idempotent; no schedule drift unhandled.
5. Milestone-5 (`6.2` complete): first installed runtime returns no mutation output and known diverged state remains blocked.
6. Milestone-6 (`closeout snapshot`): no unresolved residual risk blocks final-Verification gate.

Each milestone requires: code fact table, positive checks, negative searches, step verification commands, and explicit residual-risk owner before continuing.
