# Change: Support Stage-Specific Resume Review

Author: elvis. Date: 2026-10-09. Revision: draft-v1.
Status: proposal only; recommended design is awaiting specific approval.

## Why

S8's approved contract requires different Implementation and Final reviewers.
Its existing local Resume Context has one immutable reviewer assignment. Two
independent diagnostic sources show that the current validator accepts either
reviewer's own stage and rejects the other; an ordinary context swap is also
rejected. S8 therefore remains blocked before implementation. Changing its
reviewer/continuity rules is an excluded Major prerequisite, not an S8 plan fix.

## What Changes

- Add a strict-local alternative inside the existing reviewer_assignment field:
  exact implementation-review and final-review mappings, each a complete
  existing seven-field assignment, with separate independent instances.
- Select and validate the approved assignment by evidence phase on entry,
  recovery and completion; retain previous revision/SHA and verified checkpoint
  requirements. Preserve old single assignments and other record/profile rules.
- Add one explicit approved context-amendment validation path. It accepts only
  a strict-local, unverified blocked-to-blocked conversion changing the hashed
  contract reference and revision increment; ordinary context changes still fail.
- Apply that path only to S8's old binding after source proof, Implementation Review and sync pass.
  Create a new S8 resume contract, retain its original approval and contract bytes,
  and preserve the blocked state. Fresh S8 readiness remains a later required gate.

## Impact And Allowed Implementation Files

Capability: skill-workflow-governance, ADDED requirements only.

Future approved implementation may change:

- references/approved-implementation-workflow.md: sole policy owner in Project
  Session Resume; no copied mutable rule in SKILL or another reference.
- scripts/validate_core_gates.py: existing local context, Review, transition and
  explicit CLI validation; no new runner, ledger, schema family or signer.
- tests/test_workflow_rules.py: actual-file stage/compatibility/amendment tests.
- CHANGELOG.md; S9 contract, approval, Plan, review and sanitized proof artifacts;
  existing CURRENT/BACKLOG/LOG bookkeeping and S9 canonical status if needed.
- Exactly one other-change addition: new
  openspec/changes/add-project-document-ownership/resume-contract-v2.md, plus the
  validated S8 canonical status update at its existing path. Old S8 approval,
  proposal/design/spec/tasks and source implementation stay unchanged in S9.

The portable workflow reference and validator already exist in the manifest.
Future sync selects only those two changed files across the existing four targets;
no manifest, shared governance, companion or target-list edits.

Excluded: SKILL trigger/routing, OpenSpec requirement boundaries, Superpowers
selection, full external Handoff/schema-2 evidence, standard/compact behavior,
legacy/historical or main-spec edits, AGENTS/CONTEXT, generated distribution,
other business documents, production/dependencies, other repositories and Git
history rewriting. A needed excluded edit stops for a new specific scope decision.

## Current Phase And Approval Decision

This is Major Self-Evolution, strict after approval. General continue/closed-loop
and local edit authorization permit this reviewable proposal, not implementation.
No S9 approval, implementation, runtime synchronization, Git or production action
is claimed. S8 approval remains valid for its original scope, with F1 blocking it.

Approval of this exact draft accepts the recommended strict-local format,
legacy compatibility and narrowly guarded context amendment, including the
explicit S8 target and reviewer bindings in design.md. It supplies no external
handoff, completion, publication or production authority. The fixed iteration
contract's single-round sync/source Git lease applies only after an actual
specific approved command and all required gates. It does not silently start S8
implementation as part of the S9 slice.

Review draft: [S9 review draft](../../../../docs/review/2026-10-09-S9-stage-review-binding-draft.md).
Detailed acceptance and alternatives are in design.md and the spec delta.
