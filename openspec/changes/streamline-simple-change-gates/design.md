# Design: Streamline simple-change gates

## Principles

- Risk and changed effects decide workflow weight; model names do not.
- One concern has one owner and one gate. Do not split planning or Review merely
  to create more checkpoints.
- Safety, authorization, verification-before-completion, and user control remain
  non-negotiable.

## Routing

### Compact inline fast path

Use when work is local, reversible, cohesive, has no material choice, external
dispatch, protected-boundary change, or strict effect. Record Gate 0/1 inline,
edit directly, run focused verification, then perform one concise complete-diff
Review. Do not create a Brief, Plan, Handoff, or standalone Preflight artifact.

### Single-slice standard or OpenSpec work

Use one short executable Plan when planning is required. Inline execution does
not also create a Brief. Run one Preflight before implementation. A blocked
result receives one consolidated correction bundle and at most one terminal
focused recheck by the same reviewer. If it remains blocked, stop for a boundary
decision; do not open a third Review round.

### Strict, external, or multi-slice work

Retain the existing full planning, Preflight, evidence, independent Review,
final verification, and completion rules. A protected-boundary revision starts
a new lineage only after the required approval; it is not an automatic retry.

## TDD and Review budget

- Add the smallest focused RED that proves each distinct changed behavior or
  demonstrated failure class.
- Equivalent parameter, platform, race, and wording variants do not each need a
  separate test unless they exercise a different mechanism or risk.
- A direct deterministic probe or existing validator may reproduce a Review
  finding; a new permanent test is not mandatory when it adds no regression
  value.
- Test specification and quality are inspected inside the single
  implementation/final Review by default. Specialist passes are optional and
  risk-triggered, not automatic gates.
- For compact and standard single-slice inline work, a distinct Review after
  fresh final verification may satisfy implementation and final Review together
  if it covers actual files, complete diff, tests, claims, scope, and residual
  risk, and no file changes afterward.

## Preflight convergence

```text
FULL_PREFLIGHT
  PASS -> implement
  BLOCKED -> one consolidated correction -> terminal FOCUSED_RECHECK
terminal FOCUSED_RECHECK
  PASS -> implement
  BLOCKED -> stop for control-plane/user boundary decision
```

No R3/R4/R5 automatic loop is valid for an unchanged contract. The first
reviewer must report all reasonably discoverable findings together. A focused
recheck cannot add an ordinary finding that was already discoverable in the
root revision; such a completeness breach stops the lineage.

## Compatibility and rollback

No Handoff schema, evidence profile, lifecycle value, Git authority, or
publication boundary changes. Rollback restores the backed-up source files.

