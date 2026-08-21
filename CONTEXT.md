# Project Context Glossary

## Change Gate

The project-level entry point that classifies state-changing work, protects
approval boundaries, selects evidence weight, and owns final completion.

## Router

`openspec-superpower-change`, acting as the Change Gate and authoritative
control plane for the two-skill workflow.

## Companion

`codex-brief-antigravity-review`, serving either a request-scoped standalone
wording/read-only Review route or an already-authorized Handoff route.

## Prompt Contract

The task-facing statement of goal, scope, authority, success, stop, evidence,
verification, and output obligations. It defines the required result without
unnecessarily prescribing intermediate reasoning.

## Reviewer Assignment Contract

The explicit binding from a Review purpose to one concrete agent product,
role, capability profile, instance-independence condition, and result authority.
It prevents generic destinations such as “another agent” from obscuring who may
perform the Review and whether that result is advisory or governed evidence.

## Canonical Agent Product

A mechanically admitted coding-agent runtime product that may be assigned a
governed executor or independent-reviewer role. Product eligibility does not
grant control-plane authority; role, instance, capability profile, and the
bound contract determine the authority ceiling.

## Completion Contract

The single canonical definition of evidence and state required before the
Router may claim a whole task complete.

## Handoff Governor

The Companion responsibility that validates and advances an authorized external
batch through its canonical Handoff state and evidence lifecycle.

## Prompt Collision

A case where simultaneously applicable workflow instructions prescribe
incompatible triggers, permissions, artifacts, state transitions, or outcomes.

## Prompt-load Evidence

Measured evidence of which Skill bodies and references a supported runtime
actually loads for a scenario. File size alone is not prompt-load evidence.

## Skill Update Controller

An independently maintained maintenance Skill that audits, plans, applies,
verifies, and rolls back updates for explicitly registered Codex Skill
packages. It does not replace the Change Gate and cannot authorize its own
state-changing operations.

## Managed Skill Registry

The explicit inventory of updateable packages and the discovered Skill entries
they expose. It records package source/installation mode, dependency group,
version evidence, validation contract, runtime location, and the mapping from
each Skill name/path to one package. Discovery without a mapping is reported as
unmanaged rather than silently assumed current.

## Skill Update Plan

An immutable, hash-bound proposal for moving one registered package and its
discovered Skill entries from an observed current state to a fixed candidate
state. Creating a plan grants no authority to apply it.

## Skill Update Receipt

The durable, non-sensitive evidence for one approved update or rollback,
including bound plan identity, before/after fingerprints, validation result, and
rollback reference.

## Runtime Payload Lock

The canonical, content-addressed inventory for one immutable updater runtime
release. It records every allowed regular file's normalized relative path,
mode, and content hash; exact closure is required, so missing, extra, linked,
or altered payload entries block installation and discovery.

## Schedule Change Plan

An immutable, hash-bound proposal to install, remove, or replace the updater's
single user LaunchAgent. It binds the action, label, launch domain, exact plist
path and bytes, program arguments, cadence, observed pre-state, allowed paths,
rollback strategy, and expiry. Creating it grants no schedule-mutation
authority.

## Schedule Receipt

The durable, non-sensitive evidence for one approved schedule transaction. It
binds the schedule plan and approval hashes to the before/after plist and loaded
state, exact content-addressed controller payload/runtime lock/active discovery,
verification result, and rollback availability.

## Major Authorization Binding

The exact OpenSpec decision evidence required before a Major Skill update may
become eligible. Its immutable manifest binds the change-id, approved raw
proposal/design/spec/tasks SHA-256 set, a canonical contract-projection digest,
decision provenance, and decision time into the update plan and action approval.
The projection normalizes only existing checklist markers. The complete
approved source-bootstrap material inventory remains byte-frozen until exact worktree
materialization; only afterward do progress ticks avoid rewriting the approved
contract. Any contract-bearing text change requires a new exact approval. A
direction choice or approval of another revision cannot substitute for it.

## Source-Bootstrap Parent-Link Phases

The one-time source bootstrap treats reviewed parent-directory `nlink` values as
pre-decision baselines. On its bound APFS volume, validation admits only a closed
phase table: the immutable manifest at `approval-recorded`; that manifest plus
the held lock and no-replace journal at `journal-ready`; and those entries plus
the final ref, reflog, worktree-admin directory, and replacement worktree at
`post-bootstrap`. The same table governs lexical and retained-descriptor checks;
any unlisted delta or unknown phase fails closed and requires reapproval.

## Managed Root Ownership Graph

The global, registry-derived ownership map for every package source, runtime,
release, discovery, projection, candidate, state, backup, and managed target
root. Except for an exact declared projection, roots from different ownership
domains may not overlap, contain, or alias one another. A manager/OS-owned
container such as the controller state root, OS temporary root, common
discovery directory, or common release store is a graph anchor rather than a
package-owned root. Its reviewed schema may assign distinct exact child
entries/subtrees to controller roles, transactions, or packages; no package may
claim or mutate the whole container.

## Update Transaction Journal

The durable, fsync-backed record written before an approved update crosses its
first mutation boundary. It binds the plan, approval, pre-state, compensation
material, allowed paths, and transaction phase so a restarted controller must
finish verified compensation or stop for manual recovery before doing new work.

## Compensation Lease

The durable, single-use restoration authority prepared while the original
action approval is current and activated only by a fsynced
`MUTATION_INTENT` transition that rechecks that approval. It binds only the
exact transaction pre-state, restoration paths, and compensation hashes.
Approval expiry or Router-recorded revocation stops forward progress but cannot
expand the lease; recovery may only restore/verify that pre-state, after which
the lease is consumed.

## Bootstrap Control Root

The restrictive Router-owned governance root at
`${CODEX_HOME}/openspec-superpower-change/bootstrap-control/codex-skill-update/`.
It is created under the exact Major source-implementation authorization, remains
outside every updater runtime/state/release/discovery/schedule destination, and
has a stable marker bound only to its path, package, schema, and Router control
plane. Each Major authorization gets an immutable manifest-hash child workspace
that holds exact manifest/raw-snapshot copies, bootstrap plan, action approval,
authority channel, compensation lease, journal, receipt, and closeout evidence.
Reapproval never rewrites or invalidates an older workspace. Missing fixed
parent containers are created one component at a time as manager-owned graph
anchors; the final stable root is atomically promoted from a same-filesystem
candidate. This initializer is the only pre-operation-lock path and can create
only the fixed anchors/root; the promoted root already contains its verified
operation lock. After locking, every declared workspace is closure/journal
checked; an unfinished older transaction must recover or block before a new
workspace can do work.

## Authority Revocation Channel

The Router-owned append-only approval/revocation plane, independent of the
long-held controller operation lock. A short authority lock linearizes
canonical no-overwrite revocation records with each forward mutation boundary;
the transaction holds it from the revocation recheck through durable intent,
the atomic mutation, fsync, and boundary result. A revocation ordered before a
boundary stops it, while one ordered after a started boundary stops the next
forward boundary and leaves only compensation-lease restoration authority.

## Source Worktree Bootstrap

The one-time, exact-approved creation of the current repository's isolated
implementation branch/worktree. It binds the repository/common-Git-dir and Git
executable identities, base commit/tree, complete ref/worktree/local-config
prestate digest, every repo/ref/log/admin/worktree-parent descriptor identity,
target absence, sandbox profile, and every approved untracked material hash.
Creation holds an exclusive lock, atomically reserves the target, and is
non-forced/no-checkout inside a write-allowlisted sandbox; raw tree blobs are
materialized through closed plumbing so ambient hooks, filters, helpers,
prompts, or network cannot run. All approved material paths remain byte-frozen until
successful materialization; checklist-only progress begins afterward. Any
prestate/parent drift or partial residue blocks rather than being adopted,
forced, reset, or deleted.

## Source Worktree Quarantine

A failed or incompletely evidenced Source Worktree Bootstrap that is preserved
as read-only recovery evidence. Its ref, worktree, admin path, observed
manifest/snapshot closure, missing evidence, HEAD/tree, and no-mutation policy
are bound into the next exact bootstrap pre-state. Reapproval may name a new
absent ref/worktree/admin target, but it never repairs, reuses, deletes, cleans,
or silently adopts the quarantined attempt. Any quarantine drift blocks the
replacement bootstrap before Git runs.

## Final Evidence Chain

The immutable closeout chain under the current Major authorization workspace:
canonical task-6.7 runtime-Review and task-7.1 Project-Learning prerequisite
records, a child eligibility record that validates their exact PASS parent
chain, a canonical preliminary final-verification record whose parent is that
eligibility record, a child PASS seal that binds verified raw-trace absence and
unchanged governed fingerprints, and a later independent High Review record
whose parent is that PASS. The preliminary/PASS also bind an exact predicted
OpenSpec archive projection; after Review, only that projection may update main
specs/move the change, followed by a strict-validated archive receipt whose
parent is the Review. Each record is content-addressed,
no-follow/no-overwrite, fsynced, and schema-validated. Governed state drift
invalidates the chain; append-only evidence and normalized checklist progress
do not.

## Conditional Final-Child Mutation

A platform-proven protocol anchored to the verified parent: create uses atomic
no-replace; replacement uses atomic exchange that preserves and verifies the
displaced object; removal exchanges the child with a unique tombstone, verifies
the displaced object, then exclusively relocates and verifies that tombstone so
the destination becomes absent. A mismatch is restored where unambiguous and
otherwise enters recovery; no identity-mismatched object is unlinked. An
adapter without every required primitive cannot mutate that final child.

## Schedule Execution Binding

The immutable scope a scheduled audit must recheck before package, network, or
notification activity. It binds the exact content-addressed controller payload,
runtime lock/closure, active discovery target, controller state-root identity,
registry revision/hash, dependency-group identity, adapter identities, and
complete package/entry/projection closure to the approved LaunchAgent plan.
