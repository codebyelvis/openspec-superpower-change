## MODIFIED Requirements

### Requirement: Deterministic skill routing

The skill pair SHALL route state-changing development work, review-and-fix,
workflow/template edits, OpenSpec authorization, and final completion decisions
through `openspec-superpower-change`. Ordinary architecture Review SHALL also
remain on the Router's Review-only route. It SHALL reserve standalone
`codex-brief-antigravity-review` use for non-state-changing prompt/brief/checklist
generation and ordinary read-only artifact review, plus Handoff-backed external
batch governance after a valid handoff.

A bounded exception SHALL route only an explicit backend architecture Review of
a proposal/design from architecture/design, performance/stability,
service/module boundaries, API/call-chain/transaction boundaries, or
over-design perspectives to independent `backend-architecture-review`. The
specialist SHALL return read-only bounded evidence only; it SHALL NOT modify
files, implement fixes, create or mutate OpenSpec/Handoff state, replace
ordinary Review, or authorize Router canonical transitions. Review-and-fix SHALL
remain state-changing Router work even when backend architecture intent is
present.

#### Scenario: Other architecture Review

- **WHEN** the user asks for architecture Review without explicit backend
  architecture specialty intent
- **THEN** `openspec-superpower-change` remains the primary Review-only route
- **AND** `backend-architecture-review` is not automatically loaded or invoked

#### Scenario: Explicit backend architecture bounded exception

- **WHEN** the user explicitly requests backend architecture Review from one of
  the bounded specialty perspectives
- **THEN** `backend-architecture-review` may provide read-only specialist
  evidence
- **AND** the Router retains all gate, OpenSpec, Handoff, Evidence, verdict,
  Completion, and authority decisions

#### Scenario: Explicit backend architecture Review and fix

- **WHEN** a request combines explicit backend architecture Review intent with a
  request to modify files or implement the fix
- **THEN** `openspec-superpower-change` remains the primary state-changing route
- **AND** any specialist result remains read-only bounded evidence only

#### Scenario: Ambiguous review-and-fix wording

- **WHEN** a request includes both Review language and file modification or fixing
- **THEN** `openspec-superpower-change` is the primary skill
- **AND** the request is not handled as standalone lightweight Review

#### Scenario: Final completion evidence

- **WHEN** the user asks whether the whole implementation is complete
- **THEN** `openspec-superpower-change` owns the decision
- **AND** the brief skill may provide batch evidence but cannot authorize completion

### Requirement: Evidence-bounded Router selection of Superpowers methods

The Router SHALL own the normative selection of zero or more Superpowers
methods for governed work. It SHALL NOT require the user to name each selected
method, and it SHALL NOT make a Router-required child explicit-only unless a
supported Codex runtime proves native Router-to-child loading. User-explicit
method requests SHALL remain subordinate to workflow, Git, and completion
authority.

#### Scenario: Native nested loading is unsupported

- **GIVEN** an isolated supported-runtime probe shows user-explicit child
  activation succeeds but Router-to-explicit-only-child activation is blocked
- **WHEN** the Codex invocation policy is implemented
- **THEN** Router-required child Skills remain eligible for native implicit
  matching as defense in depth
- **AND** the workflow does not claim mechanical suppression or complete Router
  loading of those children

#### Scenario: Future nested-loading policy is proposed

- **WHEN** a later change proposes making a Router-required child explicit-only
- **THEN** repeatable evidence identifies the loaded Router and complete child by
  path or hash without shell/filesystem fallback or user `$child` input
- **AND** it proves an unselected child remains absent and missing or duplicate
  Router state fails closed
- **AND** the new policy receives its own approved scope before implementation

#### Scenario: User explicitly requests a state-changing sub-skill

- **GIVEN** the user explicitly invokes a `$superpowers:*` method for work that
  may change files or behavior, mutate Git, or decide whole-task completion
- **WHEN** the method request is evaluated
- **THEN** the Router completes Gate 0 before the method runs
- **AND** the method request grants no independent workflow, Git, business, or
  completion authority

#### Scenario: Required Router is missing or ambiguous

- **WHEN** state-changing, Git, or completion work cannot load exactly one
  applicable Router contract
- **THEN** the governed work is `BLOCKED`
- **AND** no child Skill continues on implicit or user-explicit activation alone

#### Scenario: Portable explicit-method precedence is synchronized

- **WHEN** the strengthened explicit-method authority rule is implemented
- **THEN** versioned `CCG-014` covers both broad metadata and user-explicit
  `$superpowers:*` requests on every declared required runtime
- **AND** managed-rule version 5 retains invariant IDs `CCG-001` through
  `CCG-015` and passes cross-target parity validation

#### Scenario: Diagnose-only work discovers a fix

- **GIVEN** the request is explicitly diagnose-only
- **WHEN** read-only domain inspection or `systematic-debugging` identifies a
  candidate fix
- **THEN** diagnosis stops before any state change
- **AND** the fix is reclassified through the Router before implementation

#### Scenario: Read-only Review is classified

- **WHEN** the user requests ordinary diff, Report, evidence, or non-backend-
  specialty architecture Review without fixes or final-completion authority
- **THEN** ordinary diff, Report, and evidence Review use the Companion
  standalone route, while non-backend-specialty architecture, OpenSpec,
  authorization, and whole-task completion Review remain Router Review-only work
- **AND** only explicit backend architecture specialty intent may use
  `backend-architecture-review` as the bounded read-only exception defined by
  this change

#### Scenario: Proposal-only route is fully specified

- **GIVEN** a proposal-only request has no material unresolved decision
- **WHEN** Gate 0 classifies it
- **THEN** the Router records Superpowers `none`, creates and validates only the
  OpenSpec artifacts, and stops for exact approval
- **AND** implementation planning, TDD, or execution does not begin

#### Scenario: Sub-skill requests another phase

- **WHEN** a selected child requests a later Superpowers phase
- **THEN** control returns to Router classification
- **AND** each phase and Skill is selected at most once for the bounded route
- **AND** unresolved or cyclic selection is `BLOCKED`

#### Scenario: Whole-task completion is requested

- **WHEN** a child Skill supplies verification or Review evidence
- **THEN** the Router-owned Completion Contract evaluates the whole task
- **AND** child evidence alone cannot authorize completion

## ADDED Requirements

### Requirement: Explicit lightweight backend architecture Review

The workflow SHALL provide an independent, read-only
`backend-architecture-review` Skill for explicit backend architecture Review
intent. It SHALL evaluate actual project evidence across responsibility
boundaries, interfaces/contracts, dependencies/call chains, data/transactions,
performance/reliability, evolution/complexity, and project consistency. It SHALL
return concise findings-first specialist evidence and prefer the smallest
project-consistent adjustment. It SHALL emit at most three material top-level
bullets total, embed each minimum adjustment in its finding, and omit any
separate or repeated recommendation list.

The Skill SHALL NOT implement, modify files, create OpenSpec or Handoff state,
run TDD or multi-agent orchestration, own task or Completion state, replace
ordinary Review, or authorize Router canonical transitions. Reasonable simple
solutions SHALL pass without invented architecture work. Local installation
SHALL keep the independent sibling repository as the single source and make it
discoverable from every required runtime before the Router route is deployed.

#### Scenario: Explicit backend architecture intent

- **WHEN** the user explicitly asks to Review a backend proposal from
  architecture, design, performance, stability, service/module boundary,
  API/call-chain/transaction, or over-design perspectives
- **THEN** `backend-architecture-review` performs the read-only specialty Review
- **AND** any later Router decision treats its result as bounded evidence only

#### Scenario: Required runtime discovers the specialist

- **GIVEN** the Router runtime contains the explicit specialist route
- **WHEN** that runtime resolves `backend-architecture-review`
- **THEN** its discovery entry resolves exactly to the independent sibling source
- **AND** no copied Router file, second source history, or remote publication is
  introduced

#### Scenario: Ordinary Review wording

- **WHEN** the user asks only to Review a Bugfix Diff, inspect a generic change,
  accept work, or Review the current Plan
- **THEN** the ordinary existing Review route remains selected
- **AND** `backend-architecture-review` is not automatically loaded or invoked

#### Scenario: Simple project-consistent design

- **GIVEN** a small interface design follows the project's existing boundaries
  and has no material contract, transaction, performance, reliability, or
  evolution defect
- **WHEN** the specialist reviews it
- **THEN** it returns `Verdict: PASS` concisely
- **AND** it does not require new services, layers, components, or abstractions

#### Scenario: Material architecture defect

- **GIVEN** a proposal places remote calls in a long transaction, repeats remote
  I/O, confuses responsibilities, or creates an evidenced performance risk
- **WHEN** the specialist reviews it
- **THEN** it reports the material finding before suggestions
- **AND** recommends the smallest correction supported by project evidence

### Requirement: Authorized execution continuity

During an already authorized implementation, the workflow SHALL continue the
next approved pending task while no blocker or new human decision exists.
Completing one subtask, summarizing progress, or naming a next step SHALL NOT be
a stop condition. An advancing turn with executable pending work SHALL perform
at least one task-related action.

The workflow SHALL recover goal, current task, pending work, blockers,
acceptance, and verification from the existing canonical Plan, Status, Handoff,
or equivalent state after context compaction, session recovery, model/agent
switch, or a user message of `继续`. It SHALL NOT infer the next task from the
last chat response or create a second task-state system. Existing Acceptance,
Test, Build, Verification, Evidence, Review, and Completion mechanisms remain
the only Done criteria.

#### Scenario: Pending task without blocker

- **GIVEN** implementation is authorized, approved tasks remain pending, no
  blocker exists, and no new human decision is needed
- **WHEN** one subtask finishes
- **THEN** execution proceeds to the next approved pending task
- **AND** the agent does not ask whether it should continue

#### Scenario: Advancing turn requires action

- **GIVEN** executable approved work remains pending without a blocker
- **WHEN** the agent takes a normal implementation turn
- **THEN** it reads/searches required code, edits, tests/builds, verifies,
  collects evidence, or updates existing canonical state
- **AND** a summary, recommendation, or future plan alone is not progress

#### Scenario: Canonical resume

- **GIVEN** context was compacted, a session or agent changed, or the user says
  `继续`
- **WHEN** execution resumes
- **THEN** the agent recovers the next approved incomplete task from existing
  canonical state and executes it without expanding scope
- **AND** it does not create `.agent/goal.md`, another Task Manager, or a second
  state machine

#### Scenario: Legal stop condition

- **WHEN** approved tasks are complete, state is `BLOCKED`, a new product,
  business, or architecture decision is required, permission/credentials/
  resources are missing, an operation is high-risk/irreversible/out of scope, or
  the user pauses or cancels
- **THEN** execution stops and records the applicable blocker or completion state
- **AND** no platform permission or chat summary bypasses that condition

#### Scenario: Code has been written but evidence is incomplete

- **WHEN** code or instruction text is written but existing Acceptance, Test,
  Build, Verification, or Evidence obligations remain unsatisfied
- **THEN** the task remains in progress
- **AND** it is not marked Done or complete

### Requirement: Conditional minimal implementation

The workflow SHALL apply a lightweight proportionality judgment only when a
proposed implementation or Review fix would materially add abstraction,
component, layer, dependency, or scope. It SHALL select the first adequate option
in this order: Need, Repository Reuse, Stdlib, Platform Native, Existing
Dependency, Small Local Implementation, New Abstraction. A new abstraction or
dependency SHALL NOT be chosen when an earlier project-consistent option
satisfies the approved need.

The judgment SHALL NOT become a mandatory checklist, artifact, gate, or output
for every ordinary Bugfix. It SHALL NOT automatically invoke
`backend-architecture-review`; that Skill remains available only for explicit
backend architecture Review intent.

#### Scenario: Ordinary localized Bugfix

- **GIVEN** an ordinary same-scope Bugfix is adequately solved by an existing
  repository pattern or a small local implementation
- **WHEN** implementation proceeds
- **THEN** no mandatory proportionality ceremony or specialist Review is added
- **AND** the minimal project-consistent fix remains eligible

#### Scenario: Proposed new complexity

- **GIVEN** a proposed solution or Review fix would add a new abstraction,
  component, layer, dependency, or materially wider scope
- **WHEN** an earlier option in the ordered judgment satisfies the approved need
- **THEN** the workflow selects that earlier option
- **AND** it does not add the later complexity for conceptual completeness

### Requirement: Review/Fix convergence boundary

The workflow SHALL retain `Review FAIL -> Fix -> Verify -> Review`. Before
another retry, it SHALL stop mechanically widening fixes when evidence shows the
same finding recurring, fix-induced repeated regression, multiple Review rounds
without convergence, materially conflicting reviewers on the core approach,
probable architecture or requirements-boundary error, expanding fix scope, or
accumulating abstractions, layers, or dependencies for a small need.

The stop SHALL use existing `BLOCKED`, blocker owner/resume condition,
`control-plane-high`, and Review/control-plane mechanisms for one boundary
judgment. It SHALL NOT create `ESCALATED`, a new Finding lifecycle, Quality Gate,
Task Contract, state system, multi-agent flow, or final authority. Ordinary
first-pass findings SHALL continue through the existing same-scope loop.

#### Scenario: Ordinary Review failure remains same-scope

- **GIVEN** a Review returns one actionable same-scope finding without a
  convergence signal
- **WHEN** the finding is accepted
- **THEN** the workflow fixes, verifies, and Reviews it again under the existing
  loop
- **AND** it adds no escalation ceremony or automatic architecture specialist

#### Scenario: Repeated fixes do not converge

- **GIVEN** the same finding or regression has recurred across verified fixes
- **AND** the proposed next fix would keep expanding scope or complexity
- **WHEN** another Review/Fix retry would begin
- **THEN** implementation stops before the widening change and returns
  `BLOCKED` to `control-plane-high` for a boundary judgment
- **AND** no new escalation state or governance layer is created

#### Scenario: Core reviewers conflict

- **GIVEN** reviewers materially disagree on the core architecture or requirement
  boundary
- **WHEN** the executor cannot resolve the conflict from the approved contract
  and repository evidence
- **THEN** it stops same-scope mechanical fixes and records the blocker owner and
  resume decision needed through existing control-plane handling
- **AND** neither reviewer output self-authorizes a broader implementation
