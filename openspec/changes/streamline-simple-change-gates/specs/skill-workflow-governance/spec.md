## MODIFIED Requirements

### Requirement: Mandatory review correction loop

Every implementation path SHALL complete risk-appropriate readiness,
verification, and Review before completion. Compact low-risk Direct Change MAY
record readiness inline without a standalone Plan, Brief, or Preflight artifact.
Single-slice standard or OpenSpec-backed work SHALL use no more than one short
execution Plan and one initial Preflight unless that Preflight is blocked.

For an unchanged approved contract, Preflight SHALL be bounded to one
`FULL_PREFLIGHT` plus at most one terminal `FOCUSED_RECHECK`. The full Review
SHALL report all reasonably discoverable findings together. A blocked terminal
recheck SHALL stop for control-plane or user boundary resolution and SHALL NOT
start a third automatic Preflight. Same-scope implementation Review findings
SHALL return directly to Fix -> focused Verify -> implementation Review and
SHALL NOT reopen Preflight unless scope, risk, authority, acceptance, or another
protected boundary changes.

#### Scenario: Compact Direct Change needs no standalone Preflight

- **WHEN** a local reversible Direct Change has no material choice, external
  dispatch, protected-boundary change, or strict effect
- **THEN** readiness is recorded inline and implementation proceeds without a
  standalone Brief, Plan, or Preflight artifact
- **AND** focused verification and complete-diff Review remain required

#### Scenario: Preflight converges in at most two passes

- **GIVEN** one `FULL_PREFLIGHT` reports a consolidated blocking finding set
- **WHEN** the declared corrections are complete and protected boundaries are
  unchanged
- **THEN** the same reviewer performs at most one terminal
  `FOCUSED_RECHECK`
- **AND** another blocked result stops instead of opening R3 or later rounds

#### Scenario: Implementation finding does not reopen Preflight

- **WHEN** implementation Review finds a same-scope defect without a protected
  boundary change
- **THEN** the workflow fixes it, runs focused verification, and repeats the
  implementation Review
- **AND** it does not create another Plan/Brief Preflight lineage

### Requirement: Profile-weighted workflow remains proportionate

The workflow SHALL use the smallest artifact, TDD, verification, and Review set
that proves the changed acceptance and demonstrated blast radius. One focused
regression per distinct behavior or credible failure class SHALL be sufficient
unless another case exercises a different mechanism or risk. Equivalent
variants SHALL NOT be multiplied for ceremony, and unrelated suites SHALL NOT
run without an existing gate or demonstrated blast radius.

Test-specification and test-quality concerns SHALL be inspected within the
implementation/final Review by default; separate specialist passes SHALL be
optional and triggered only by concrete risk or failure. Compact and standard
single-slice inline work MAY use one distinct complete-diff Review after fresh
final verification as both Implementation Review and Final Review when no later
change occurs. Strict, external, multi-slice, and protected-boundary work SHALL
retain their existing separate gates.

#### Scenario: One failure class gets one focused regression

- **WHEN** one regression deterministically proves a changed behavior or Review
  finding
- **THEN** the workflow does not add equivalent parameter, platform, race, or
  wording variants without a distinct mechanism or risk

#### Scenario: Single-slice Review is consolidated

- **GIVEN** compact or standard inline work has one cohesive slice
- **WHEN** fresh final verification passes and a distinct reviewer inspects the
  actual files, complete diff, claims, scope, and residual risk
- **THEN** that Review MAY satisfy implementation and final Review together
- **AND** any later source change invalidates it

#### Scenario: Strict work keeps full gates

- **WHEN** work changes security, authorization, persistence/write semantics,
  migration, recovery, deployment, deletion, destructive effects, external
  execution, or production authority
- **THEN** full planning, Preflight, real evidence, independent Review, final
  verification, and completion gates remain required

### Requirement: Phase-aware Superpowers activation

The workflow SHALL not activate planning, TDD, or Review sub-skills as separate
ceremonial phases when one proportional execution path can satisfy the same
contract. Compact Direct Change SHALL remain inline. Single-slice standard or
OpenSpec-backed inline work SHALL use one Plan when required and SHALL NOT also
create a Brief. Multi-slice, strict, or external work SHALL retain the
applicable full workflow.

#### Scenario: Strong model handles a simple task

- **WHEN** a strong reasoning model executes a compact or single-slice task
- **THEN** the proportional inline path is preferred when task risk permits it
- **AND** model identity does not waive any gate required by changed effects

