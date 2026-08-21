# Completion Contract

For schema 6 Review routing, carry all six concepts without abbreviation:
Review purpose, reviewer product, role, capability, independence, and authority.
The normative assignment and product/instance boundary live in
`references/agent-capability-routing.md`; this reference does not create a
second authority.

This is the Router-owned normative contract for a whole-task completion claim.
Batch, slice, and route references may add local evidence rules, but they do not
define a second completion checklist.

## Success

A task is complete only when the approved scope and acceptance criteria are
satisfied, every required verification has fresh final evidence produced after
the last implementation or learning change, and the final Review PASS covers
the complete diff and claims at the required risk profile. No unresolved
`FAIL` or `BLOCKED` result may remain.

An external batch `PASS` is not task completion. It returns the work as
`awaiting-final-verification`; the Router alone evaluates this contract and
records any whole-task completion transition.

## Evidence

Evidence must identify the command or probe, result, relevant artifact or inline
record, and freshness boundary. External execution additionally retains
runtime-validated hashed attempt Report, batch Review, final verification, and
final Review artifacts. A label, stale result, executor assertion, or metadata
claim cannot replace evidence.

For a Handoff-backed path, run fresh `final_critical` once and persist its hashed
evidence manifest in a new `awaiting-final-verification` revision. Persist final
Review evidence, then allow `complete` only when attempt Report, batch Review,
final verification, and final Review artifacts are present and
runtime-validated against the actual prior canonical status with
`--previous-status`. Later state-changing edits invalidate affected evidence.

The final Review PASS must inspect actual files and the complete diff; review
scope, tests/logs, documentation and contract consistency, sensitive
information, temporary files, and unrelated changes; and include the
risk-appropriate adversarial or business-chain probe. Invoke
`superpowers:verification-before-completion` before any success claim.

## Stop conditions

Any verification or Review `FAIL` returns to the same scope for correction,
fresh verification, and Review. Any `BLOCKED` result records the blocker owner
and resume condition and stops completion. Scope expansion, invalid approval,
missing required evidence, unresolved sensitive-data concerns, or an
incompatible active lifecycle also stop the claim.

## Learning and reconciliation

Run Project Learning Closeout after implementation Review PASS and before fresh
final verification or OpenSpec reconciliation/archive. The audit may determine
that no durable promotion is required, but mandatory project-local promotion or
an explicit user request to archive and distill blocks completion until durable
artifacts and any mechanically enforceable regression test or validator pass
focused verification and Review. A chat-only summary is not durable promotion.

For OpenSpec-backed work, complete OpenSpec task reconciliation: Reconcile
`tasks.md` with no unexplained required item and Update project-required
design/closeout documentation. Archive only when repository semantics permit
it, then run strict validation after archive. If deployment, release, or another
required lifecycle remains outstanding, keep the change active and record its
owner and resume condition. Any closeout validation or Review finding returns
to correction, fresh verification, and Review.

## Cross-CLI sync

When portable workflow files or managed governance change, synchronize validated
source to every declared required runtime and verify parity, discovery, and
target validators. Any required Codex, Pi, Antigravity CLI, or Grok CLI target
drift blocks completion; repository-only documentation/history changes do not
create that gate.

## Git and publication authority

OpenSpec approval, a plan, a Handoff, implementation success, and this contract
do not grant Git or publication authority. `git add`, commit, push, PR creation,
destructive Git, release, deployment, or other external publication requires
the applicable explicit user authorization. An unrequested commit or push is
not a completion requirement.

## Residual risk

Report accepted non-blocking residual risk with its evidence, impact, owner or
decision, and follow-up condition. A residual that contradicts approved
acceptance, safety, evidence integrity, or required runtime parity is blocking
and must be handled under the stop conditions instead of being waived by prose.
