# Authorized Continuation Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans for this cohesive
> rule update. The bound Codex controller implements; distinct Codex instances
> provide Preflight, Implementation and Final Review evidence.

**Goal:** Remove redundant confirmation and advisory ceremony without changing
approval, identity, evidence freshness or completion authority.

**Architecture:** Clarify existing Router predicates and representation rules;
retain validators, lifecycle schemas and exact immutable bindings. Validate an
isolated release candidate independently of the dirty integration source, then
apply only the reviewed owned delta and use existing scoped runtime sync.

**Tech Stack:** Markdown, OpenSpec, Python standard-library unittest; PyYAML and
dependency-free parser paths; existing grok-cc and cross-CLI sync helpers.

**Spec:** `openspec/changes/reduce-redundant-confirmation-and-review-overhead/`
(`proposal.md`, `design.md`, spec delta and `approval.md`). Draft-v2 is approved.

## Global Constraints

- Router-only source/publication; no grok-cc or Companion implementation edits.
- Preserve all Non-negotiables, exact lease comparisons, historical bindings,
  schema-6 assignments and existing Preflight convergence limits.
- Evidence profile: strict (authority/routing); one cohesive business slice;
  separate independent Preflight, Implementation and Final Reviews.
- Existing scoped commit/push authority targets verified `origin/main` only;
  no force-push, unrelated commits, release or new external destination.
- Existing source dirty work and runtime drift remain user-owned and unchanged.
- Cloud CC is advisory only. Complete, integrity-checked report is required;
  accepted input or an idle terminal is not a completed opinion or formal PASS.

## Review Focus

1. Source changes versus approval bytes: test real lease reuse plus rejection of
   stale implementation fingerprints and changed authorization bindings.
2. Protected category with/without explicit action coverage: real validator
   positive/negative pair; agent probe for exact push target and no force-push.
3. Fixable BLOCKED versus prohibited advancement: agent probe keeps Preflight
   closed while correcting its command, preserves the terminal recheck ceiling.
4. Recovery identity versus existing user choice: agent probe retains decisions
   without inheriting a controller assignment.
5. Compact evidence and advisory routing: agent probes accept complete inline
   facts, preserve missing-evidence rejection, keep CC outside formal PASS.

## Isolation, Baselines And Ownership

Source base: `1242605fc4bb52c5644027697d71587e4a9dcc74`.
Companion verification base: `74c14369bad1f985d95e83a9f11a699d4db310a6`.
Use project-external isolated source snapshots under the already-created private
temporary execution directory. Export both bases with `git archive` into sibling
directories; this creates no branch/worktree metadata and does not implement on
the dirty main checkout. Source/runtime preimages already exist in a separate
private backup directory; refresh selected preimages before integration/sync.

Keep a second untouched Router archive as `release-baseline` for no-index diff
checks. Before named OpenSpec validation in the candidate, copy only this
unchanged approved change directory (including its approval receipt), this Plan
and this round's scoped evidence into their original relative paths. These
governance artifacts are untracked at the base and are not supplied by archive.

Behavioral comparison uses separate `instruction-before` and `instruction-after`
fixtures containing the identical integration preimage of `SKILL.md`, `AGENTS.md`
and `references/`. The before hashes must match the recorded five-sample control;
apply only the reviewed owned rule delta to after. Keep unrelated rebind/return
bytes identical. The clean release candidate is a separate verification scope,
not the after arm of a mixed-instruction causal comparison.

Perform implementation in the isolated candidate. Validate that clean candidate
without any native-consumer/rebind/JEV dirty files. Apply its reviewed delta to
the integration source only after Implementation Review; reject conflicting
hunks rather than overwrite user changes. Runtime sync uses the integration
source with preserved existing parity, not the clean release tree. State both
evidence scopes explicitly. No claim of whole-runtime equality to release HEAD.

## Task 1: Baselines, Cloud Opinion And Readiness

**Files:** approved change directory; this Plan; scoped `docs/review/` evidence.
**Consumes:** approved draft-v2; actual private packet and current binding.
**Produces:** bounded cloud opinion, behavior baseline, independent Preflight.

- [ ] Collect the one requested CC advisory through its existing binding and
  packet/hash check; manually restrict output to the requested report file.
- [ ] Evaluate each finding against local evidence; correct only Plan details
  within approval. A changed protected boundary requires its actual approval.
- [ ] Run identical fresh-agent before/after decision scenarios. Use five fresh
  samples per wording variant, one case per distinct mechanism; manually score
  every result. Preserve exact observed decisions in sanitized evidence. Do not
  invent a RED when old guidance already yields the expected behavior.
- [ ] Create isolated clean snapshots and run baseline core/full suite, including
  the sibling Companion dependency. Classify any failure by acceptance relevance.
- [ ] Self-review this Plan for spec coverage, executable commands, proportion,
  boundaries and rollback; obtain one independent FULL_PREFLIGHT with complete
  findings and whole-file Plan hash before implementation.

## Task 2: Minimal Rule Clarifications And Regression Proof

**Modify:** `SKILL.md`, `references/approved-implementation-workflow.md`,
`references/confirmation-lease.md`, `references/step-evidence-gate.md`,
`references/local-instruction-checkpoint.md`, `tests/test_workflow_rules.py`.
`references/completion-contract.md` changes only if needed to eliminate a real
contradiction. `scripts/validate_core_gates.py` is not planned for change: retain
its shared core and exact comparisons. `CHANGELOG.md` records the outcome.

**Consumes:** unchanged existing validator APIs and approved normative wording.
**Produces:** scoped rule delta and behavior evidence; no new state or runner.

Cloud-advisory disposition is recorded in
`docs/review/2026-10-22-authorized-continuation-grok-cc-disposition.md`.
Its corrections refine the approved predicates, not the immutable draft-v2:
the Router entry applies authorization coverage before stop/confirmation in
every route, including Direct Change; no new edit target is introduced. New
lease documentation names its immutable approval source in `approved_scope`
(keep the existing `decision_source` enum), not a mutable execution Plan/Brief.
Changed approved evidence assumptions remain invalidating; stale results alone
require refreshed verification. Compact presentation retains its existing
risk/contract eligibility. Recheck verifies the complete protected-boundary
matrix. Future grok-cc protocol suggestions are not approved implementation or
promoted invariants. Grok CLI runtime sync does not install grok-cc.

- [ ] Add actual `validate_confirmation_lease` coverage: `external-message`
  reuses with explicit business authority, rejects without it or absent action;
  independently mutate exact revision/hash/scope/risk, invalidation flags and
  revoked/deferred status to verify rejection.
- [ ] Extend the existing stale-input fixture: change actual implementation
  bytes while the contract SHA stays fixed; lease reuse remains valid while
  `validate_resume_record` rejects stale implementation fingerprints. These are
  safety regressions and may be GREEN on the baseline, not fabricated RED.
- [ ] Run affected tests before rule changes; document the agent baseline failure
  for each changed behavior or mark the case as non-reproduced safety coverage.
- [ ] Apply minimal predicate-based wording from approved design: authorization
  coverage before asking, immutable authorization versus mutable evidence,
  owner-aware remediation with closed gates, separate recovery decisions,
  compact inline facts and bounded CC advisory routing.
- [ ] Run the same fresh-agent scenarios against the matched instruction-after
  fixture; bind consumed hashes and unchanged unrelated bytes. Include absent
  Major approval, missing evidence, different publication target, unknown send
  and unassigned owner counterexamples. No prompt supplies the expected answer.
  Include the already-authorized Direct Change publication path in the existing
  authorization case, and Plan-byte changes versus approval-byte changes in
  the binding case. Preserve the same original seven-case comparison separately
  from these advisory-driven probes; do not relabel added probes as matched RED.
- [ ] Inspect frontmatter, discovery, conditional wording, linked references,
  absence of duplicate state/ceremony and preserved Non-negotiables. Address
  observed new ambiguity only; do not add speculative universal rules.
- [ ] Run required quick/core/full tests in both parser modes and OpenSpec strict
  validation; independent Implementation Review inspects actual complete delta
  and performs an adversarial probe, not merely a metadata/keyword review.

## Task 3: Sync, Final Gates And Scoped Publication

**Files:** approved change progress and scoped review/learning evidence; runtime
changes only to Task 2 portable files through reviewed schema-v2 sync.
**Consumes:** validated owned delta and independent Implementation Review PASS.
**Produces:** four-target verification, Final Review, scoped publication receipt.

- [ ] Apply owned delta to integration source preserving its dirty preimage;
  run core/full verification there. Audit learning under existing rules; promote
  only required approved-scope knowledge, with mechanical enforcement where
  feasible. Rerun affected checks after any learning edits.
- [ ] Inventory known canonical legacy statuses before sync. Generate existing
  schema-v2 plan with one `--select-file openspec-superpower-change:<path>` per
  changed portable file; do not select managed rules or unmodified files. Require
  complete unselected parity, exact prestates and independent plan Review.
- [ ] Apply/verify/commit each target in declared order Codex, Pi, Antigravity CLI,
  Grok CLI; run existing verify-all. No manual copy, native config change or drift
  adoption. A failed target restores only itself and blocks later targets.
- [ ] Run fresh final checks; separate independent Final Review covers the whole
  owned diff, actual evidence, sync, secrets, temporary artifacts and acceptance.
- [ ] Reconcile this change's tasks/specs; archive only when repository semantics
  permit and after applicable gates. No other active change is reconciled.
- [ ] Build the exact clean release tree from base plus owned delta; rerun its
  required checks after closeout. With original index still empty, use a checked
  scoped cached patch, verify index tree equals that tested tree, and commit.
  Check parent/base, actual remote main and absence of unrelated ahead commits;
  push only this commit to `origin/main`, without force. Recheck remote hash.
- [ ] Finish the idle known CC task, retaining its binding. Remove only identified
  owned temporary artifacts after all gates/publication; report retained recovery
  evidence if blocked. Give concise result, test counts and commit hash.

## Exact Verification Commands

Run the core/full/quick commands below in the clean candidate and integration
source. The unchanged base uses core/full/quick only, not validation of a change
absent from that base. Logs remain private and durable reports contain only
sanitized results/hashes. Default `python3` has no PyYAML. For the
PyYAML path, prefix with
`PYTHONPATH=/Users/elvis/.cache/uv/archive-v0/ayESLOK8mFHijrq9bOrjF` (verified 6.0.3).
Quick validator is the installed system skill's `scripts/quick_validate.py`.

```text
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONPATH=/Users/elvis/.cache/uv/archive-v0/ayESLOK8mFHijrq9bOrjF PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .
PYTHONPATH=/Users/elvis/.cache/uv/archive-v0/ayESLOK8mFHijrq9bOrjF PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONPATH=/Users/elvis/.cache/uv/archive-v0/ayESLOK8mFHijrq9bOrjF PYTHONDONTWRITEBYTECODE=1 python3 /Users/elvis/.codex-account-wb/skills/.system/skill-creator/scripts/quick_validate.py .
openspec validate reduce-redundant-confirmation-and-review-overhead --strict
```

Named OpenSpec validation runs only in integration or the prepared candidate
containing the approved change. After archive, use the archived change's actual
repository-supported validation command. In the actual integration Git checkout
run `git diff --check`; for the metadata-free candidate use:

```text
git diff --no-index --check -- /private/tmp/osc-approved-execution-NvaGBN/release-baseline /private/tmp/osc-approved-execution-NvaGBN/openspec-superpower-change
```

For this no-index comparison, exit 0 means identical and exit 1 can mean an
ordinary difference. Accept only exit 0 or 1 with empty diagnostic output;
nonempty whitespace/error diagnostics or exit greater than 1 fail the check.
Capture both output and exit code, rather than reporting exit 1 alone as PASS.

The sync checklist additionally requires the following unchanged Companion
checks in its source and installed Codex runtime root, without editing either:

```text
PYTHONPATH=/Users/elvis/.cache/uv/archive-v0/ayESLOK8mFHijrq9bOrjF PYTHONDONTWRITEBYTECODE=1 python3 /Users/elvis/.codex-account-wb/skills/.system/skill-creator/scripts/quick_validate.py .
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_templates.py .
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Target verification uses existing `validate_cross_cli_sync.py` subcommands and
their reviewed exact plan; Grok discovery uses `grok inspect --json` without
reading config. No Pi native process probe is needed.

## Rollback And Stop Conditions

Before integration, discard only owned candidate edits; source/runtime unchanged.
After integration, reverse only this round's reviewed delta against unchanged
prestates; reject later concurrent changes. Runtime rollback uses the existing
transaction receipt and exact preimage. No reset, history rewrite or unreviewed
copy. Keep private backups until gates and publication resolve.

Stop the affected action for absent/changed authority, unknown transport outcome,
incomplete cloud report, identity mismatch, unselected drift, failed required
evidence or unresolved Review findings. Continue authorized independent work and
same-scope remediation without a new courtesy confirmation. Do not advance a
blocked gate or create a third unchanged-contract Preflight.
