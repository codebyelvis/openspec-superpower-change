# Project Session Resume — draft-v1

Status: draft-v1 approved for scoped implementation on 2026-10-08, user reply
“批准” to the concrete proposal/approval report. Author: elvis.

## Context And Goals

S7 extends existing canonical recovery rather than replacing it. A fresh
loaded agent must locate the goal, current state, completed work, next action,
blockers, resume condition and latest verified checkpoint without old chat.
Persistence does not confer approval, instance identity, evidence authority or
completion. Existing lifecycle/risk/Review gates continue to decide completion.

Non-goals: autosaving a conversation or process, replaying tools, automatic
rollback, a second ledger/index/schema family, a session-start hook, manifest or
companion changes, rewriting active external contracts, and S8 document moves.

## Proposed Decisions And Alternatives

### 1. One canonical file, explicit validation interface

Use `docs/agent-collab/<change-id>/status.md`. Existing OpenSpec work uses its
real change-id. Unfinished Direct Change reuses its established scoped ID or,
if none exists, records a stable `direct-<slug>` ID when a cross-window checkpoint
is first needed; this is a directory identifier, not an approved OpenSpec change.
An already finished compact single-turn change needs no checkpoint ceremony.
No generic continuation message alone creates a Handoff or OpenSpec change.

Add exactly one `Session Resume` section with a fenced data record, explicitly
discriminated by `record_kind: local` or `record_kind: external`. Keep this
discriminator outside schema-6 governance fields. Reject duplicate sections,
unknown kinds and ambiguous/mixed governance sources.

Bind record kind to the scoped contract/plan and preserve it across validated
previous-status transitions. An external assignment or retained external
artifact reference cannot be relabeled local; a kind change requires a newly
approved scoped transition, outside this proposal. Deleting the marker is not
a recovery strategy. As with existing Handoff validation, wholesale forgery of
the prior state and every bound contract/evidence file is outside this
lightweight validator's threat model; no journal or signature system is added.

For **local**, a `governance` mapping contains exactly this schema-6 subset:
`schema_version`, `change_id`, `mode`, `approval_status`, `risk_profile`,
`contract_revision`, `lifecycle_state`, `control_plane_owner`, `blocked_reason`,
`blocker_owner`, `resume_condition`, `next_owner`, `readonly_fields`. Field
meaning, enums and identity shapes remain those of schema 6; immutable fields
are the applicable existing immutable-field subset. Do not invent external
executor/reviewer assignments or batch evidence for a local change.

For **external**, omit the local governance mapping and reference the same
file's existing full Handoff and `contract_revision`; the full Handoff remains
the only source of governance fields. Its exact required field set and the
companion's current Handoff API remain unchanged. Progress is not inserted in
the Handoff marker, copied into Briefs, or used as external Report/Review proof.

The proposed `--resume-status` interface validates this explicit record. Existing
`--status` remains full external Handoff validation and rejects a local subset.
Invalid full external state cannot become valid by changing the discriminator,
omitting the marker, or falling back after a parser error. A local record cannot
coexist with an external marker in the same status file. Legacy 4/5 stay on the
existing immutable audit path, with no automatic migration or resume.

Alternatives: forcing full Handoff onto inline work invents external ceremony;
relaxing existing `--status` admits invalid external contracts; another status
file duplicates authority. The proposed explicit local interface avoids those
effects, but adds a small validator branch that requires approval and tests.

### 2. Progress is a checkpoint, not another task list

The same section has `progress` containing: goal and contract/plan references,
completed work/evidence references, one `next_action`, and `verified_revision`.
Reuse existing OpenSpec tasks/Plan for steps; do not mirror their mutable
checkboxes. References to approval identify existing authorization and never
manufacture it. Nonterminal `next_action` names one concrete action, its existing
owner, required permission/evidence and inputs. A blocked action is an explicit
wait for its persisted resume condition. Terminal completion uses `null`.

Before voluntarily stopping or ending an advancing implementation turn, persist
the actual state and progress together. Do not require a checkpoint for every
TDD micro-step. If an external execution is outstanding, its already-persisted
wait action is sufficient: do not rewrite a status hash bound to a live Brief.
Update progress before the governor captures execution revision/SHA-256, or
after ownership returns using the existing validated transition.

Unexpected process termination is outside a voluntary persistence guarantee;
on recovery, detect changed scope inputs and require verification. No promise
that unpersisted edits or background processes were checkpointed.

### 3. Verified revision and current edits are distinct

`verified_revision` is null until actual required verification succeeds and its
result is persisted. Once present, it binds the status revision, relevant
regular project-relative source/config/test inputs and their hash-or-absence,
the aggregate fingerprint, command results and existing evidence references.
Do not require a Git commit to checkpoint. Exclude the checkpoint itself and
its newly written evidence outputs from the source fingerprint to avoid a
self-hash cycle; preserve evidence path/hash checks separately.

Use bound-root/no-symlink reads and the existing path/hash conventions. Scope
inputs must cover verification-relevant files of the authorized slice, not
unrelated historical documents or the whole repository. Missing/contradictory
declared coverage blocks a verified claim. Scope is reviewed against the actual
verification commands; the validator does not promise automatic discovery of
all transitive runtime dependencies. An edit affecting those inputs invalidates
current PASS; retain the previous checkpoint as a historical reference, keep
the new edits, and select verification/fix as next action. A newer chat message
or modification time cannot advance the verified revision. Neither a best
checkpoint nor a test PASS implies completion.

### 4. Recovery and authority

On `继续`, `继续闭环`, compaction, or a window/model/agent switch, inspect the
existing project status location. More than one unfinished change requires
selection; do not pick newest/highest-priority automatically. A selected record
must parse, resolve beneath the project root, agree with its contract/plan and
approval, and pass evidence/fingerprint checks before advancing.

Every loaded agent can read the recovery state. Reuse approval and the unique
safe action when the acting identity has the existing required assignment.
A model change in the same bound instance does not alter authority. A new
unassigned instance cannot declare itself the old control plane; it may perform
authorized read-only recovery, then report the existing assignment/rebinding
boundary. This proposal adds no automatic owner transfer. Preserving this
boundary means fully transparent write/signoff recovery cannot be promised for
an arbitrary new identity; that is an explicit limitation for approval.

## Proposed State Transition Table

Local states are a subset of the existing lifecycle enum; no new lifecycle is
introduced. External transitions remain governed by the existing full contract.

| Persisted state | Event and required evidence | Next persisted state / one action |
|---|---|---|
| No record, authorized pending implementation | First intentional handoff/pause | Existing ready state; persist goal, completed references and next approved action |
| `ready-for-execution` | Work attempted; required step evidence retained | `ready-for-review` when distinct Review is required; otherwise existing local verification path |
| `ready-for-review` | Governed Review FAIL | `needs-fix`; one scoped fix, finding and owner |
| `needs-fix` | Authorized fix may proceed | `ready-for-execution`; invalidate affected current PASS |
| Nonterminal ready/fix state | Intentional pause, no new progress/evidence | Preserve phase/revision evidence; persist current unique action; pause is not a new state |
| Nonterminal state | Missing authority, ambiguous/invalid state or other blocker | `blocked`; reason, owner and resume condition; one wait action |
| `blocked` | Resume condition actually met; existing authority/evidence rechecked | Existing eligible phase; never skip the blocked gate |
| Verified checkpoint plus later edited inputs | Fingerprint mismatch | Existing needs-verification/fix path; retain historical checkpoint, do not roll back |
| Required implementation/Review accepted | Completion gates still pending | `awaiting-final-verification`; one pending gate action |
| `awaiting-final-verification` | Fresh required verification persisted | Preserve state; final Review remains next where required |
| `awaiting-final-verification` | Required final Review PASS and all existing closeout conditions satisfied | `complete`; previous-status proof required; `next_action: null` |
| `complete` | New window/continue | Read-only terminal result; do not restart work |

“Needs verification” above describes a pending action, not a new enum value.
For compact local work, Review applicability stays under its existing risk
profile; no synthetic external Report/Review is created. External complete still
requires separately persisted final verification and final Review, actual
previous status, bound evidence and the current sole completion owner.

## Validation And Review

Follow the review draft and tasks. Use existing test infrastructure and native
isolated forward probes: one positive recovery mechanism and strict regressions
for stale inputs, missing/duplicate next action, external downgrade, wrong owner,
multiple changes and invalid final completion. Audit native events and retain
only sanitized results; no fabricated independent Review or persistence PASS.

After approval: quick/core/full existing unittest in both parser modes; strict
OpenSpec validation; profile-required independent implementation Review;
reviewed scoped four-target sync and verify-all; fresh post-sync verification
and distinct-instance final Review. No new manifest selector or target is needed
for the proposed existing portable file edits.

## Migration, Rollback And Open Approval Decision

There is no bulk migration. A new local record is created only for authorized
unfinished work requiring a checkpoint. External progress is added by its bound
owner at a legal hash/transition boundary. Reject incompatible legacy/partial
records instead of mutating them. Restore source from the implementation-round
private backup and runtime with that round's reviewed transaction, then verify.
Never delete a business checkpoint or user edits to simulate rollback.

The approval accepts draft-v1's interface/subset, Direct Change ID,
fingerprint coverage and new-instance limitation. If a change to full Handoff,
companion or ownership/completion authority is required, revise and approve that
scope first. Design acceptance does not certify implementation or Review.
