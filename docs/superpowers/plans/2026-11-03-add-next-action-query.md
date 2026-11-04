# Authorized Continuation Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans for this cohesive
> rule update. The active executor (`pi`) implements; a distinct `antigravity-cli`
> (`agy`) headless session provides Preflight, Implementation and Final Review
> evidence (`independent-reviewer` / `control-plane-high` /
> `governed-review-evidence`).

**Goal:** Add a deterministic read-only next-action query for canonical schema-6
status, eliminating main-thread LLM re-derivation of "what is the legal next
step", without adding a state system, runner, or framework.

**Architecture:** Add a sibling read-only script `scripts/next_action.py` that
imports the existing transition/owner/result tables from
`scripts/validate_core_gates.py` (single source of truth). Run full structural
validation first; on failure emit `BLOCKED` and no suggestion; on success emit
legal next states, required evidence roles bound to identity, allowed
`next_owner`, lease state, and blocked resume context. Output is advisory only:
no status writes, no proposed-status generation, no evidence promotion.

**Tech Stack:** Python standard-library; reuses existing
`validate_core_gates.py` functions and unittest suite. No new runtime deps.

**Spec:** `openspec/changes/add-next-action-query/` (`proposal.md`, spec delta,
`tasks.md`). User approved change-id `add-next-action-query` for implementation.

## Global Constraints

- `scripts/` is portable content per `cross-cli-portable-manifest.json`;
  the new sibling script and any validator refactor must pass four-target
  cross-CLI sync after verified review.
- Minimal refactor of `validate_core_gates.py`: only add a module-level
  `EXPECTED_OWNERS` constant and reference it in the existing
  `_validate_schema4_handoff_contract` owner check (and mirror the identical
  constant/reference in `codex-brief-antigravity-review/scripts/validate_templates.py`
  so `test_shared_validator_core_is_byte_identical_when_companion_exists` stays
  green). No behavior change; existing tests must pass unchanged.
- Read-only: the new script never writes `status.md`, never writes a proposed
  status file, never generates evidence, never promotes state, never transfers
  authority.
- Risk profile: standard. Separate independent Preflight, Implementation and
  Final Reviews; no combined shortcut (`completion-contract` false-PASS rule).
- No new state system, runner, or framework. No Orca dependency in this change.
- `add-next-action-query` is the only reviewed change for staging. Existing
  dirty user work remains user-owned and unchanged.

## Review Focus

1. Reuse vs. duplication: the sibling script must import transition tables from
   `validate_core_gates.py`; assert no copied transition rule body.
2. Fail-closed: invalid or unparsable status emits `BLOCKED` with reason and no
   next-action suggestion.
3. Advisory-only: assert no write of status/proposed status/evidence; output
   flagged advisory and not promotable.
4. Blocked resume: strict blocked fixture echoes `blocker_owner` and
   `resume_condition` verbatim, zero automatic transitions.
5. Cross-CLI: new sibling script listed in `cross-cli-portable-manifest.json`
   and sync passes for all four targets.

## Isolation, Baselines And Ownership

Source base: current `main` HEAD `57b824d`.
Workspace: implement in-place with surgical edits only on the owned
`add-next-action-query` files (`scripts/validate_core_gates.py`,
`scripts/next_action.py`, `tests/test_next_action.py`,
`references/cross-cli-portable-manifest.json`, and companion shared validator
core `codex-brief-antigravity-review/scripts/validate_templates.py`). Preserve
all existing dirty files untouched; run zero destructive Git commands.

No external cloud execution required. grok-cc (bound Claude Code) is advisory
only and its earlier analysis (round-3, `STATUS: SUFFICIENT`) already scoped the
design; no further cloud dispatch needed to implement.

## Task 1: Baseline And Preflight

**Files:** `scripts/validate_core_gates.py`, `tests/`, this Plan, spec delta.
**Consumes:** approved `add-next-action-query`; validator function bodies.
**Produces:** baseline, independent Preflight PASS.

- [ ] Record baseline: run `scripts/validate_core_gates.py --help` and the
  full unittest suite; confirm green pre-change.
- [ ] Read `validate_handoff_contract` owner block (lines ~446-451) and
  `STATE_TUPLES` / `ALLOWED_TRANSITIONS` / `NEXT_OWNERS` module constants.
- [ ] Obtain one independent FULL_PREFLIGHT over this Plan and the spec delta;
  record whole-file Plan hash. Fix findings to PASS before implementation.

## Task 2: Minimal Validator Refactor (no behavior change)

**Modify:** `scripts/validate_core_gates.py`.
**Produces:** module-level `EXPECTED_OWNERS` constant reused by the existing
owner check; existing tests stay green.

- [ ] Add module-level `EXPECTED_OWNERS` mapping (identical to the inline
  `expected_owners` dict) near the other tables.
- [ ] Replace the inline dict in `validate_handoff_contract` with a reference
  to the module constant.
- [ ] Run full unittest suite; assert zero behavior change.

## Task 3: Read-Only Next-Action Script

**Add:** `scripts/next_action.py`.
**Produces:** `--status <path>` CLI that prints advisory next-action JSON/YAML
or `BLOCKED`+reason.

- [ ] Import `extract_handoff_contract`, `read`, `validate_handoff_contract`,
  `ALLOWED_TRANSITIONS`, `STATE_TUPLES`, `NEXT_OWNERS`, `EXPECTED_OWNERS`,
  `ARTIFACT_FIELDS` from `validate_core_gates`.
- [ ] Run structural validation; on `AssertionError` print `BLOCKED` + reason
  and exit non-zero with no suggestion.
- [ ] On success print: current state + result tuple; each legal next state
  (`ALLOWED_TRANSITIONS[state]`); for each, required evidence role(s) mapped to
  identity (executor/reviewer/control-plane) from artifact semantics and owner
  table; allowed `next_owner`; `confirmation_lease_status`; if `blocked`, echo
  `blocker_owner` + `resume_condition` verbatim; mark final-state needing
  `--previous-status`.
- [ ] Flag output as advisory, non-promotable, non-authoritative.

## Task 4: RED/GREEN Tests

**Modify:** add `tests/test_next_action.py`.
**Produces:** per-lifecycle-state RED/GREEN, strict blocked fixture, invalid
status fixture, advisory-only assertions.

- [ ] Every lifecycle state in `LIFECYCLE_STATES` has a green case.
- [ ] Strict blocked fixture (r5-like): zero automatic transitions, echoes
  resume context.
- [ ] Invalid/unparsable status fixture: `BLOCKED`, no suggestion.
- [ ] Advisory-only: no file write, no status mutation, output not evidence.

## Task 5: Verification, Review, Sync, Completion

- [ ] Run full unittest suite + `validate_core_gates.py` on a clean candidate.
- [ ] Independent Implementation Review; fix, re-verify, re-review findings.
- [ ] Separate Final Review (no combined shortcut).
- [ ] Add `scripts/next_action.py` to `cross-cli-portable-manifest.json`;
  run `scripts/validate_cross_cli_sync.py` for all four targets.
- [ ] Persist final verification and final Review evidence.
- [ ] Reconcile tasks, archive `add-next-action-query`, validate after archive.
- [ ] Record residual risks and update completion report.

## Rollback

- Remove `scripts/next_action.py` and its manifest entry; revert the
  `EXPECTED_OWNERS` refactor (behavior-neutral); re-run full suite and
  four-target sync.