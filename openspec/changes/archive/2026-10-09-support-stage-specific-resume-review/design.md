# Stage-Specific Resume Review — draft-v1

Author: elvis. Status: proposal only; all recommendations await scoped approval.

## Intent And Evidence

Solve the specific S8 conflict without turning continuation into authority or
rewriting immutable contracts. Independent sources are the S8 FULL_PREFLIGHT F1
and the control-plane complete-transition diagnostic. The latter demonstrates
that distinct Final is rejected, same-instance Final is accepted by the old
validator, and a normal context swap is rejected. These are diagnostic fixtures,
not new execution, verification or gate-bearing PASS.

User constraints: preserve S1–S8 scope/priority, original S8 distinct Final,
OpenSpec approval, schema-6 ownership, evidence and completion gates, four CLI
targets and local source/workspace contracts. Proceed through authorized routine
steps autonomously. Material compatibility/lifecycle decisions below are
recommendations for the one concrete OpenSpec approval, not accepted assumptions.

## Alternatives And Recommended Boundary

1. Recommended: strict-local stage mapping plus an explicit approved amendment
   limited to blocked unverified checkpoints. This fixes both the representation
   and S8's already-bound old context while preserving an audit trail.
2. Mapping for new contexts only: smaller implementation, but cannot resolve S8's
   existing immutable binding. S8 stays blocked pending another lifecycle change.
3. Select Final from mutable Plan/Review output, reuse Implementation Reviewer,
   silently replace context or avoid persistence: fails S8 approval/independence
   or existing continuity rules and is not an acceptable fallback.

No new global approval system, signer, state index, autosave hook or executable
migration utility. Extend the existing explicit read-only validator only; the
already-bound Router performs an authorized atomic status replacement afterward.

## 1. Two Exact Shapes In One Existing Field

Keep the nine Resume Context outer fields, the local governance/progress fields
and schema version 6 unchanged. The existing reviewer_assignment value retains
its original seven-field assignment meaning everywhere it already applies.
Only local strict contexts may opt into this alternative exact value shape:

    reviewer_assignment:
      implementation-review: <complete existing seven-field assignment>
      final-review: <complete existing seven-field assignment>

Classify by the exact key set before validating. A malformed seven-field value
must not fall back to the stage form; a malformed stage form must not fall back
to single assignment. Reject mixed/unknown/missing keys, null stages, duplicates,
unsafe refs and malformed values using existing fail-closed parsing/path rules.

Validate both entries on every load, including early/blocked states. Each is an
eligible existing product, independent-reviewer/control-plane-high with full
nonblank review_purpose and governed-review-evidence authority. Implementation
independence retains distinct-contract-instance with exactly
control_plane_owner and executor_assignment as targets. Final adds exactly
implementation_reviewer to those targets. Enforce different contract instance
IDs between both reviewers and the bound controller/local executor. Do not invent
an external executor assignment for local execution.

New evidence still carries one full seven-field reviewer_assignment and its
agent_identity, not the mapping. Its evidence_role selects exactly the approved
stage entry. Do not choose by current lifecycle alone or accept any eligible
unassigned reviewer. Match purpose, identity, role, profile, independence and
authority in full. Existing fingerprint/revision/canonical-SHA gates remain.

The old full assignment remains accepted with its original behavior, including
its separate implementation/final gate use. Local standard, compact/null and
external/full Handoff accept only their existing shapes; external malformed
records cannot select local or stage behavior. Frozen history is not migrated.
This proposal does not retrofit distinct Final onto every legacy strict record.

## 2. Recovery And Completion Keep Their Gates

Entering awaiting-final-verification requires the stage-bound Implementation
Review against actual prior canonical bytes. Standalone recovery rechecks it;
phase entry alone cannot prove a recovered checkpoint valid. Persist actual
critical-command results and verified inputs before Final Review. Completing
requires actual previous awaiting-final-verification, unchanged persisted
verification, and the distinct stage-bound Final Review against that snapshot.

For a recorded-complete stage-form local record, read-only recovery checks both
retained Review assignments and verified input/evidence consistency; it never
signs again. The actual previous-byte requirement is still enforced at the
original complete transition. No new claim of recovered previous bytes is made.
Atomic verify/review/complete, stale inputs, stage substitution and reviewer
self-authorization remain rejected. Separate gates cannot become a combined
shortcut for this protected slice. Model names confer no authority.

## 3. Explicit Approved Context Amendment

Ordinary validate_resume_record transitions retain exact contract-ref immutability.
Add an opt-in keyword/CLI input representing a safe hashed approval reference:
--resume-amendment-approval '<hashed-reference JSON>'. It is valid only with
--resume-status, --artifact-root and --previous-status, never external --status.
Like existing validation it checks facts and returns authority_granted=false;
it neither authenticates an actor nor establishes real user approval itself.
The Router must first record actual specific approval of this scoped S9 contract.

The approving contract owns exactly one Resume Amendment Authorization JSON
section with these exact fields:

- amendment_kind: strict-local-reviewer-binding;
- change_id: target local change;
- previous_contract: exact safe hashed old approved context reference;
- next_contract_path: safe new approved context path, different from the old one;
- reviewer_assignment: the exact approved strict stage mapping.

The approving contract's own Resume Context must be approved/self-evolution/
strict, retain its explicit amend-review-binding/local-edit action, and bind the
same actual control-plane owner as both target states. Its own workflow may use
the unchanged old single assignment. The concrete user decision and exact S9
contract hashes remain in that existing approval record; there is no validator
inference of approval from bare prose or a successful consistency check.

With this explicit input, require all of the following before accepting:

1. Load/validate the actual previous canonical state, its old context and every
   retained hash, and validate the new proposed state/context using the same
   descriptor-bound, duplicate-safe, project-relative regular-file rules.
2. Both records are local, strict, approved, blocked, with null verified_revision;
   the old context uses a full single assignment. Both retain the same controller.
3. The approval reference/hash and its exact authorization section match the
   target change, original contract ref, new path and full proposed stage map.
   The implementation entry must be byte-equivalent as data to the old assignment.
4. All context facts except reviewer_assignment remain exactly equal: change,
   kind, mode, approval, risk, owner, actions/permissions and critical commands.
5. All canonical fields remain equal except progress.contract and the required
   governance.contract_revision increment by exactly one. In particular preserve
   blocked reasons/owners/condition, wait action, goal, Plan, completed history,
   null verification and immutable fields. No new PASS, evidence rewrite or
   execution transition is allowed in this amendment.
6. Preserve the old approved contract bytes. The controller validates using the
   actual canonical prior bytes, checks they still match before atomic replacement,
   and retains their immutable historical snapshot in S9 evidence. Concurrent
   drift, stale approval/hash, missing old bytes or any unauthorized diff blocks.

A separately approved normal same-context transition may later resolve the
blocker after fresh readiness. Amendment never grants readiness, final signoff,
production/Git authority or ownership transfer. Omitting the opt-in, malformed
approval or unknown fields cannot relax the ordinary immutable-context path.
The protocol can validate a specifically scoped amendment; this S9 authorization
permits only the actual S8 target below, not a migration of other projects/history.

## 4. The Only Authorized S8 Amendment After S9 Approval

Original target contract, retained without edits:
openspec/changes/add-project-document-ownership/approval.md,
SHA-256 233d318470241a5eb22eea9186bb372d72db6b65bf9556f6ffa818318e924873.
New context path:
openspec/changes/add-project-document-ownership/resume-contract-v2.md.
Canonical status retains docs/agent-collab/add-project-document-ownership/status.md.

Copy the old nine-field Resume Context unchanged except reviewer_assignment.
implementation-review is the exact original s8-review-01 seven-field assignment.
final-review has these complete approved-by-this-draft proposed facts:

    review_purpose:
      object: S8 final verification and closure
      decision: decide pass, fail or blocked for the independent final gate
    agent_product: codex
    agent_instance_id: s8-final-01
    agent_role: independent-reviewer
    capability_profile: control-plane-high
    independence_requirement:
      kind: distinct-contract-instance
      distinct_from:
        - control_plane_owner
        - executor_assignment
        - implementation_reviewer
    result_authority: governed-review-evidence

Bind the actual latest S8 canonical snapshot after S9 checks, not today's stale
revision/hash. Preserve the original S8 four-artifact approved hashes, approval
record, scope, acceptance, strict risk and independent Final requirement. S9
records the new approved context and bounded conversion only after source proof,
independent Implementation Review and required four-target sync succeed; it then
includes that actual metadata change in fresh final verification and Final Review.
A failed amendment retains S8 blocked and the old context/canonical bytes.

This resolves representation only. S8's original Preflight is still BLOCKED;
its changed protected binding permits a genuinely new Plan/Preflight lineage,
with original ordinary F2/F3 corrections retained, after S9 closure. S9 does not
edit S8 implementation, tasks or Plan, sign S8 readiness, run S8 behavior tests,
or mark S8 done. CURRENT retains S8 as unfinished and documents S9 as its
prerequisite, with no second mutable S8 ledger.

## 5. Bootstrap, Verification And Reviews After Approval

S9 implementation uses an approved old-format strict Resume Context and the
same eligible reviewer assignment for two separate gates where needed. Its
reviewer is distinct from author/executor. This follows the current rule and
avoids requiring unimplemented stage-form admission before implementing it.
Once available, new stage-form behavior is proven in isolated projects; S9 does
not rewrite its own context in place or borrow S8's contract-specific exception.

First RED the old validator with stage-form admission/transition and explicit
amendment acceptance counterexamples. Then implement only the owned reference,
validator and tests. GREEN tests use real temporary regular files, hashes and
separate persisted revisions; synthetic Review values test consistency only.
Actual independent review output remains required for workflow signoff.

Use isolated actual-file forward scenarios with gpt-6.1-sol/high:

- Distinct phase binding: perform scoped edits, actual critical-command
  verification, Implementation Review, persisted final verification and separate
  Final Review; close one window, recover the actual files in another instance
  read-only, then let only the existing bound controller advance.
- Amendment: create a blocked old-format strict fixture, actual scoped approving
  contract and proposed new context; validate/atomically persist the guarded
  blocked-to-blocked transition, verify old bytes/history stay unchanged, and
  reject an unauthorized amendment without canonical mutation.
- Compatibility/adversarial checks: preserve old strict/standard/compact and full
  external semantics; check swapped/reused/unknown instances, missing phase,
  wrong purpose/profile/authority/independence, stale checkpoint/Review/previous,
  invalid hashes/symlinks/duplicate keys and external/local downgrade attempts.

Audit native tools and actual file/command effects; answer-only classifier output
is not behavior proof. Keep raw traces privately while needed and persist only
sanitized process results, identities, revision/file hashes and linkable artifacts.
No new runtime framework or production data dependency is needed.

Required checks: quick_validate with PyYAML; core and full existing unittest suite
with both PyYAML and dependency-free fallback; strict new-change validation;
RED/GREEN and native actual-file proof; artifact scope/hash/link checks.
Independent Plan Preflight, Implementation Review and Final Review remain separate,
with gpt-6.1-sol/high. Reuse unaffected prior evidence but never count S8's blocked
or root-authored diagnostic as S9 independent PASS.

## 6. Sync, Closure And Rollback

After approved source proof, plan/review/apply/verify-all through the existing
four-runtime transaction. Scope contains only the two already-listed portable
files; tests/CHANGELOG/state are source-only. Keep managed governance, manifest,
targets and companion fixed. Any stale required target or missing authority is
BLOCKED. Source tests do not establish runtime or whole-task completion.

After Implementation Review and sync, perform the required learning audit and
guarded S8 metadata amendment with its read-only consistency checks. Then fresh
final verification and independent Final Review cover the entire actual final
diff, including that amendment, under the existing Completion Contract. Later
bookkeeping/evidence changes retain fresh affected checks; no earlier Review is
claimed to cover a future mutation. Reconcile/archive only S9 via the existing
owned path; do not rewrite the currently dirty main spec or historical changes.
Use the approved iteration lease only for S9 scoped add/commit/current-branch push;
exclude all S8 previously uncommitted work except exact approved amendment/state
files, and exclude 44 unrelated dirty files. Do not push another repository.

Proposal backup and scope inventory are in the review draft. Keep them until
approval/rollback decisions complete. Before implementation make a fresh source/
runtime backup and bind sync destination pre-state. Runtime rollback follows its
existing receipt/restore transaction. A persisted context amendment has no
automatic inverse: preserve audit/context and stop for an explicit rollback
scope decision; do not revive stale previous revisions or old verification.
