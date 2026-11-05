## MODIFIED Requirements

### Requirement: Deterministic skill routing

`openspec-superpower-change` SHALL load only when the user explicitly requests
OpenSpec, change gating, or routing, says 「迭代优化skill」, or explicitly requests
archive/distillation. Ordinary
implementation, typo correction, formatting, comments, non-contractual
documentation, already-authorized same-scope continuation, and standalone
read-only Review SHALL NOT automatically load this skill. Generic file or
behavior changes alone SHALL NOT be matching triggers.

This change SHALL preserve approval, evidence, completion, schema-6,
control-plane ownership, production, credential, and destructive Git
boundaries after entry. Not loading the skill SHALL NOT grant another actor
canonical authority or waive an existing authorization or evidence requirement.
Valid Handoff-backed batch governance SHALL remain available in the Companion
under its existing contract; batch evidence SHALL NOT authorize final completion.

The Router implementation target SHALL be
`/Users/elvis/file/develop/opensource/openspec-superpower-change/SKILL.md`.

#### Scenario: Explicit entry

- **WHEN** the user explicitly asks for OpenSpec, change gating, routing, says 「迭代优化skill」, or explicitly requests archive/distillation
- **THEN** the Router SHALL load
- **AND** existing governance boundaries SHALL remain in force

#### Scenario: Ordinary typo request

- **WHEN** the user asks to fix a typo without an explicit entry request
- **THEN** `openspec-superpower-change` SHALL NOT automatically load

#### Scenario: Other excluded requests

- **WHEN** the user requests ordinary implementation, formatting, comments, non-contractual documentation, already-authorized same-scope continuation, or standalone read-only Review without an explicit entry request
- **THEN** the Router SHALL NOT automatically load based on that request alone
- **AND** this exclusion SHALL NOT grant Git, production, credential, destructive-operation, or canonical-completion authority

#### Scenario: Other architecture Review

- **WHEN** the user asks for standalone architecture Review without an explicit Router entry request
- **THEN** the Router SHALL NOT automatically load
- **AND** this change SHALL NOT add an automatic backend specialist trigger

#### Scenario: Explicit backend architecture bounded exception

- **WHEN** the user explicitly requests backend architecture Review from an existing bounded specialty perspective
- **THEN** `backend-architecture-review` MAY still provide read-only specialist evidence
- **AND** that evidence SHALL NOT transfer canonical governance or completion authority
- **AND** the Router SHALL load only on an explicit entry request

#### Scenario: Explicit backend architecture Review and fix

- **WHEN** backend architecture Review is combined with a request to fix files without an explicit Router entry request
- **THEN** that wording alone SHALL NOT automatically load the Router
- **AND** specialist evidence SHALL remain read-only and SHALL NOT authorize implementation

#### Scenario: Ambiguous review-and-fix wording

- **WHEN** a request combines Review and fixing without an explicit Router entry request
- **THEN** the Router SHALL NOT automatically load merely because files may change
- **AND** the request SHALL NOT be handled as standalone lightweight read-only Review

#### Scenario: Final completion evidence

- **WHEN** a governed whole-task completion decision is requested
- **THEN** existing control-plane ownership and completion evidence requirements SHALL remain unchanged
- **AND** the Companion SHALL NOT authorize final completion
- **AND** this authority boundary SHALL NOT broaden the explicit autoload triggers

### Requirement: Diagnosis checkpoint before a single-hypothesis fix

When the user's current request both identifies the defect and requests its
repair, the workflow SHALL treat that one slice as confirmed and proceed from
diagnosis directly to its single-hypothesis fix within existing authorization.
It SHALL NOT require a separate report-and-stop or repeat confirmation for
that same slice. A diagnose-only request SHALL still end with a checkpoint
report and stop without implementation. A request that has not authorized the
identified fix slice SHALL also stop before implementing it.

The two-failure, scope-expansion, new-root-cause, Git, production, and destructive
operation stop conditions SHALL remain unchanged. This continuation SHALL NOT
bypass missing approval, evidence, or any other existing protected boundary.

#### Scenario: Current request names the defect and asks for repair

- **GIVEN** the current request names one defect and requests its repair, and applicable implementation authorization is satisfied
- **WHEN** diagnosis confirms that same slice
- **THEN** the agent SHALL proceed directly to the single-hypothesis fix
- **AND** it SHALL NOT stop merely to obtain the same confirmation again

#### Scenario: Diagnosis only

- **WHEN** the current request asks only for diagnosis, even if it names a defect
- **THEN** the agent SHALL report its findings and stop
- **AND** it SHALL NOT implement a fix

#### Scenario: Diagnosis finishes without a named fix slice

- **WHEN** diagnosis completes and the current request has not authorized the identified fix slice
- **THEN** the agent SHALL present a checkpoint report and stop before implementation

#### Scenario: The same slice fails twice

- **WHEN** the user has confirmed one fix slice and that slice's fix has failed twice
- **THEN** the agent SHALL stop and report
- **AND** it SHALL NOT start a third attempt or a second hypothesis in that round

#### Scenario: Existing stops still apply

- **WHEN** the same slice fails twice, scope expands, a new root cause triggers an existing stop, or a Git, production, or destructive operation reaches its existing authorization boundary
- **THEN** the workflow SHALL enforce the same stop and report behavior as before this change
- **AND** a named repair request SHALL NOT authorize a third attempt, another hypothesis, or a protected operation outside its authority

### Requirement: Evidence-gated Companion route isolation

`codex-brief-antigravity-review` SHALL keep Standalone Lightweight and
Handed-off External Execution mutually exclusive. Its complete role assignment
section and `ROLE_FIRST_REVIEW_CLASSIFICATION` body SHALL reside in a reference
read only for Handed-off External Execution. The main `SKILL.md` SHALL NOT inject
that body into Standalone Lightweight context. Standalone Lightweight Review
output SHALL contain only scope, findings, `PASS/FAIL/BLOCKED`, and next action;
scope SHALL identify the evidence actually inspected. Its verdict SHALL remain
advisory and SHALL NOT constitute batch promotion or final completion.

With a valid Handoff Contract, the complete existing lifecycle, role assignment,
schema-6, identity, independence, evidence, correction, transition, control-plane
ownership, and final-return requirements SHALL remain mandatory and unchanged.
Moving text SHALL NOT delete or weaken any Handoff governance requirement.

The Companion repository has no `openspec/`; this delta SHALL govern these targets:

- `/Users/elvis/file/develop/opensource/codex-brief-antigravity-review/SKILL.md`
- `/Users/elvis/file/develop/opensource/codex-brief-antigravity-review/references/handed-off-external-execution.md`

#### Scenario: Standalone wording or read-only Review

- **GIVEN** the user requests standalone read-only Review and no valid Handoff route is active
- **WHEN** the Companion is selected
- **THEN** it SHALL NOT load the Handed-off role assignment or ROLE_FIRST classification reference
- **AND** it SHALL output only scope, findings, `PASS/FAIL/BLOCKED`, and next action
- **AND** its verdict SHALL NOT authorize implementation or canonical state changes

#### Scenario: Valid Handoff route is selected

- **GIVEN** a valid canonical Handoff Contract exists
- **WHEN** dispatch, audit, retry, recovery, or batch promotion selects Handed-off External Execution
- **THEN** the complete Handed-off reference, including role assignment and ROLE_FIRST classification, SHALL be read
- **AND** all existing Handoff governance SHALL remain enforced without omission

#### Scenario: Runtime supports lazy reference loading

- **WHEN** reproducible runtime evidence proves inactive Companion references are not loaded
- **THEN** the thin entry and Handed-off-only reference SHALL preserve both route contracts
- **AND** parity checks SHALL cover both routes without changing Handoff authority

#### Scenario: Runtime injects the whole activated body

- **WHEN** a runtime injects the complete activated main SKILL.md body
- **THEN** role assignment and ROLE_FIRST classification SHALL be absent from that main body and reside in the Handed-off-only reference
- **AND** if the runtime also injects inactive references, context isolation SHALL remain unverified rather than be claimed successful
- **AND** this change SHALL NOT authorize a split into new skill entrypoints

#### Scenario: Runtime loading is unobservable

- **WHEN** a required runtime exposes no reproducible Skill/reference loading evidence
- **THEN** its loading result SHALL remain `UNKNOWN`
- **AND** file size alone SHALL NOT establish context isolation or token savings

#### Scenario: Text inspection is not runtime evidence

- **WHEN** only entry text and reference placement have been inspected
- **THEN** the result SHALL establish only textual contract conformance
- **AND** it SHALL NOT claim observed runtime loading behavior, measured token savings, or whole-task completion
