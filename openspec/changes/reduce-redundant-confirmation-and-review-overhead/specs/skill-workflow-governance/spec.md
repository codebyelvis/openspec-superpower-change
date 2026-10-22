## MODIFIED Requirements

### Requirement: Authorized execution continuity

During an already authorized implementation, the workflow SHALL continue the
next approved pending task while no missing authority or material user decision
prevents that action. Completing one subtask, summarizing progress, or naming a
next step SHALL NOT be a stop condition. An advancing turn with executable
pending work SHALL perform at least one task-related action.

Before requesting confirmation, the Router SHALL compare the proposed action,
exact target, scope, conditions and current actor assignment with existing
explicit authorization. A protected action category alone SHALL NOT require
another confirmation when the exact action remains authorized. Closed-loop
wording alone SHALL NOT grant protected-action or Major implementation authority.

The workflow SHALL recover goal, current task, pending work, blockers,
acceptance, verification and existing user decisions from the canonical Plan,
Status, Handoff or equivalent state after compaction, recovery, model/agent
switch or `继续`. It SHALL separately validate actor assignment, SHALL NOT infer
the next task or ownership from the last chat response, and SHALL NOT create a
second task-state system. Existing Acceptance, Test, Build, Verification,
Evidence, Review and Completion mechanisms remain the only Done criteria.

#### Scenario: Pending task without blocker

- **GIVEN** implementation is authorized and an approved pending task needs no
  new material decision or authority
- **WHEN** one subtask finishes
- **THEN** execution proceeds without asking whether it should continue

#### Scenario: Advancing turn requires action

- **GIVEN** executable approved work remains pending
- **WHEN** the agent takes an advancing implementation turn
- **THEN** it performs an authorized task-related action
- **AND** a summary or future plan alone is not treated as progress

#### Scenario: Explicit Review and publication authorization remains valid

- **GIVEN** the user authorized one scoped external Review and ordinary push to
  an exact repository/branch, and all applicable gates and actor checks pass
- **WHEN** the workflow reaches those actions without a target or scope change
- **THEN** it reuses that authorization without asking for the same permission
- **AND** another repository, force-push, release or new side effect remains
  outside that authorization

#### Scenario: Canonical resume

- **GIVEN** a continuation recovers the same approved task and valid assignment
- **WHEN** the workflow resumes
- **THEN** it executes the next authorized incomplete action without re-asking
- **AND** it does not create a second task manager or authorization registry

#### Scenario: New instance has no signing assignment

- **GIVEN** the approved design and user decisions remain valid
- **WHEN** a new instance lacks the required assignment
- **THEN** it preserves those decisions and reports the exact identity blocker
- **AND** it neither impersonates the original controller nor asks to approve
  the same design again merely because the instance changed

#### Scenario: Legal stop condition

- **WHEN** an action lacks applicable authority, requires a material decision,
  exceeds scope, lacks required evidence/resources, would bypass a blocked gate,
  or the user pauses or cancels
- **THEN** the action stops and records its actual blocker owner and condition
- **AND** an already authorized independent correction may continue without
  crossing the blocked transition
- **AND** platform permission or a chat summary cannot bypass that condition

#### Scenario: A new Major contract is not approved

- **GIVEN** the user asked generally to optimize, continue and push
- **WHEN** a new concrete Major contract has not been approved
- **THEN** authorized preparation continues but Major implementation waits for
  that exact contract's approval

#### Scenario: Code has been written but evidence is incomplete

- **WHEN** implementation is written but required evidence or Review is missing
- **THEN** the task remains in progress and is not reported complete

## ADDED Requirements

### Requirement: Authorization binding is separate from evidence freshness

The workflow SHALL identify the approved authorization artifact as the subject
of a Confirmation Lease revision/hash. It SHALL preserve exact binding checks.
Implementation, Report, test-result and progress changes SHALL refresh affected
evidence without automatically invalidating an unchanged authorization contract.
Historical bindings SHALL NOT be silently reinterpreted or migrated.

#### Scenario: Same-scope fix changes code

- **GIVEN** a valid unchanged approved contract permits the correction
- **WHEN** the correction changes code and invalidates relevant test evidence
- **THEN** the workflow refreshes that evidence and Review without renewed scope
  approval

#### Scenario: Bound approval changes

- **WHEN** approved artifact bytes, scope, acceptance, risk, target or authority
  change, or authorization is revoked
- **THEN** the old lease cannot authorize the changed action
- **AND** the applicable existing approval/amendment path remains required

### Requirement: Blocker remediation preserves the closed gate

The assigned controller SHALL distinguish an already authorized correction from
the blocked transition. It SHALL perform scoped remediation and required recheck
without renewed user approval when no material decision is missing. It SHALL
retain existing transition validation, evidence freshness and convergence limits.

#### Scenario: Repairable Preflight defect

- **GIVEN** a Plan has an incorrect test command and the correction is within
  the existing authorized scope and current convergence allowance
- **WHEN** Preflight returns BLOCKED
- **THEN** the Plan is corrected and rechecked without asking whether to fix it
- **AND** implementation does not start before required Preflight PASS

#### Scenario: Blocker requires new authority

- **WHEN** remediation needs a new production effect, broader scope, different
  identity/target or material business choice
- **THEN** the workflow identifies the missing authority or decision and asks
  only for that delta
- **AND** unknown create/send outcomes cannot be resolved by approval alone

### Requirement: Compact signoff permits inline factual evidence

Compact signoff SHALL retain the applicable facts, source references, positive
and negative checks, regression evidence, scope checks and Review. It MAY express
those facts inline instead of a separate code-fact table or full twelve-part
output. Existing strict and protected-boundary evidence requirements SHALL remain.

#### Scenario: Complete compact evidence

- **GIVEN** a compact local correction has adequate inline source/diff references,
  relevant regression results, scope checks and focused Review
- **WHEN** the slice is evaluated
- **THEN** the absence of a separately formatted fact table is not a blocker

#### Scenario: Missing evidence is not a formatting exception

- **WHEN** relevant regression or required real acceptance evidence is absent
- **THEN** compact formatting does not permit signoff

### Requirement: Cloud consultation preserves advisory routing and authorization

The Router SHALL distinguish advisory consultation from delegated implementation.
A standalone advisory request SHALL NOT by itself create an external execution
Handoff or extra formal Review gates. It SHALL reuse the explicit unchanged
dispatch authorization while enforcing the actual transport's binding, target,
integrity, recovery and user-owned action rules. Claude Code output SHALL remain
advisory and SHALL NOT acquire a schema-6 product or formal PASS. Required formal
Review and local verification SHALL remain applicable.

#### Scenario: Already authorized bounded consultation

- **GIVEN** the user authorized the scoped Review and a valid same-target binding
  and reviewed payload satisfy the transport's existing checks
- **WHEN** the Router dispatches and collects that consultation
- **THEN** it does not ask permission again for the same action
- **AND** it does not create an implementation Handoff solely for the consultation
- **AND** it verifies the returned output under the actual supported protocol

#### Scenario: New binding or implementation delegation

- **WHEN** a new target/binding is required or the task changes to implementation
- **THEN** the applicable existing binding or implementation approval path applies
- **AND** advisory permission is not used to infer that new authority

#### Scenario: Report contains no actionable finding

- **GIVEN** a complete report was obtained through the currently supported
  transport and states its actual coverage and unverified items
- **WHEN** the Router evaluates the advice
- **THEN** it may record no actionable advisory findings without inventing issues
- **AND** it does not claim that advice satisfies an independent formal gate

#### Scenario: Required cloud review is unavailable

- **WHEN** the requested cloud reviewer cannot be reached or lacks a required
  authorized binding
- **THEN** the workflow reports that no cloud opinion was obtained
- **AND** continues only independent already-authorized preparation
- **AND** does not substitute local tests or another product as that cloud Review
