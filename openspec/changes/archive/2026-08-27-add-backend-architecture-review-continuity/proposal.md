# Change: Add backend architecture Review and execution continuity

## Why

The Router currently owns architecture Review as a broad Review-only route, but
it has no narrow, reusable backend-architecture judgment Skill. Reusing the
full Router for every specialist check would mix domain judgment with change
governance, while routing ordinary Review into an architecture specialist would
make simple work slower.

Approved long implementations also lack one explicit continuity rule tying
pending work, legal stop conditions, resume behavior, and proof of progress to
existing canonical state. The missing rule can cause an agent to stop after a
subtask or return only a plan even though authorized work remains.

The existing Review `FAIL -> Fix -> Verify -> Review` loop also lacks an
explicit convergence boundary. Repeated findings, regressions, reviewer conflict,
or growing fix complexity can otherwise turn a small approved need into a broad
redesign. A conditional minimal-implementation check and an existing-mechanism
escalation close that gap without burdening ordinary Bugfix work.

## What Changes

- Create independent sibling Skill source `backend-architecture-review` with
  four minimal files and its own local Git repository.
- Install that source locally as one discovery symlink in each required Codex,
  Pi, Antigravity CLI, and Grok CLI Skill root; keep the sibling repository as
  the single source and verify every resolved target before Router sync.
- Distill only backend architecture judgment: boundaries, contracts, call
  chains, data/transactions, performance/reliability, evolution/complexity, and
  project consistency.
- Make the Skill explicit-intent-only, read-only, findings-first, lightweight,
  and usable without the Router.
- Route only explicit backend architecture Review requests from the Router to
  the specialist and return its result as bounded evidence; keep all existing
  gates, verdict authority, ordinary Review, Handoff, Evidence, and Completion
  semantics with the Router.
- Add one authorized-execution continuity section that reuses existing
  canonical Plan/Status/Handoff or equivalent state, continues pending work
  while no legal stop applies, requires an actual task action per advancing
  turn, and keeps existing acceptance/evidence as the only Done standard.
- Add a conditional minimal-implementation checkpoint only when a proposed
  solution or Review fix would materially add abstraction, component, layer,
  dependency, or scope. Prefer existing repository/platform capabilities and a
  small local implementation before a new abstraction.
- Preserve the existing Review/Fix loop, but stop non-converging retries through
  existing `BLOCKED` and `control-plane-high` mechanisms before complexity or
  scope keeps expanding.
- Add deterministic trigger/non-trigger, continuity, proportionality, and
  convergence regressions plus the
  required Skill and project validation. A private `/private/tmp` real-agent
  forward runner, not a Router repository fixture, covers canonical Plan/Status
  recovery, actual pending-task action, clean ordinary non-trigger routing,
  trace guards, and legal-stop enforcement.

## Non-Goals

- Architecture implementation, code modification, OpenSpec creation, TDD,
  Handoff, multi-agent orchestration, task-state ownership, or Completion inside
  the new Skill.
- Routing ordinary Diff, Bugfix, acceptance, generic Plan, or generic Review
  requests to the new Skill.
- Adding a planner, task manager, Agent Harness, second state machine, automatic
  secondary Review, remote publication, or adding the sibling Skill to the
  Router's portable manifest. Local discovery symlinks are installation only.
- Making the minimal-implementation sequence mandatory for every ordinary
  Bugfix, creating an `ESCALATED` state, Finding lifecycle, Quality Gate, Task
  Contract, requirements/invariants state system, or new multi-agent flow.
- Changing existing Router Gate, OpenSpec, Handoff, Evidence, PASS/FAIL/BLOCKED,
  Completion, Git, or publication authority.

## Impact

- Affected spec: `skill-workflow-governance`.
- New sibling source: `../backend-architecture-review/{SKILL.md,README.md,references/review-dimensions.md,tests-or-examples/trigger-cases.md}` plus its local `.git/` metadata.
- Local discovery targets: `backend-architecture-review` symlinks under the
  four required runtime Skill roots, each resolving to that sibling source.
- Router source files: `SKILL.md`,
  `references/approved-implementation-workflow.md`, focused regression tests,
  and the active OpenSpec change/Plan artifacts. No additional reference is
  required.
- Private evidence only: the real-agent forward runner, isolated canonical
  fixtures, raw JSONL, and final messages live under `/private/tmp`; no runner,
  fixture, or evidence file is added to the Router repository.
- Portable Router runtime files: the two changed Router instruction files.
  Runtime apply must prove an exact two-path mutation set per target; the current
  full-manifest transaction is not eligible if it would rewrite unchanged
  Router, Companion, or managed-rule files. Missing targeted tooling is recorded
  as `BLOCKED`, not repaired by expanding this change.
- Risk: standard Major Self-Evolution because explicit routing and approved
  execution lifecycle behavior change.

## Approval Status

- Change-id: `add-backend-architecture-review-continuity`.
- The user supplied the exact trigger, scope, exclusions, continuity rules,
  validation scenarios, local Git authorization, and final acceptance in the
  implementation request, and explicitly stated that this task is authorized
  for implementation without another continue prompt.
- The user's current instruction explicitly binds the conditional
  minimal-implementation and non-converging Review/Fix rules to this same
  change-id, requires minimal changes, and forbids a Harness or new governance
  layer. No unresolved design choice remains.
- That authorization is bound only to this scoped change-id; staging, commit,
  push, publication, destructive cleanup, and scope expansion remain
  unauthorized.
- [x] This exact revised change-id and scoped contract are approved for implementation.
