## ADDED Requirements

### Requirement: Explicit Gate 0 task type recording and numeric round budget fallback

Gate 0 SHALL record the task type explicitly (`VERIFY`, `DIAGNOSE`, `FIX`, or `REVIEW`) to provide an objective baseline for task-type change stops. If local instructions define no numeric round budget, numeric threshold stops SHALL be skipped, while boundary, new root cause, advisor-repeat, and two-failure stops SHALL remain fully binding.

#### Scenario: Gate 0 records task type
- **WHEN** recording Gate 0 facts before action
- **THEN** the record SHALL include the current task classification (`VERIFY`, `DIAGNOSE`, `FIX`, or `REVIEW`)
- **AND** any subsequent transition to a different task type SHALL trigger the task-type change stop

#### Scenario: Missing local numeric round budget
- **WHEN** the runtime environment or local instructions define no numeric round budget values
- **THEN** the workflow SHALL skip numeric tool call, duration, or test count limits
- **AND** the workflow SHALL NOT halt on an undefined numeric threshold
- **AND** all non-numeric safety stops (physical boundary, two-failure, advisor-repeat) SHALL remain active

### Requirement: Pre-existing failure BLOCKED transition and bounded completion loops

A required-check failure classified as pre-existing debt (`OUT_OF_SCOPE_PREEXISTING_DEBT`) SHALL NOT enter self-repair and SHALL transition to `BLOCKED` with `blocker_owner: user`. The two-failure stop in `SKILL.md` SHALL bound every `fix -> verify -> Review` loop in `completion-contract.md`.

#### Scenario: Pre-existing failure halts without repair loop
- **WHEN** a required verification check fails during task completion due to an out-of-scope pre-existing defect
- **THEN** the workflow SHALL NOT route the failure to self-repair
- **AND** the workflow SHALL record a `BLOCKED` status with `blocker_owner: user`
- **AND** the completion claim SHALL pause until the user confirms a separate fix slice or approves a baseline exception

#### Scenario: Completion loop respects two-failure stop
- **WHEN** an in-scope fix slice fails verification twice during completion verification
- **THEN** the workflow SHALL halt completion as `BLOCKED`
- **AND** the agent SHALL NOT attempt a third edit or alternate hypothesis in that round

### Requirement: Delegated review and uninterrupted closed-loop execution

When the user specifies closed-loop execution or delegates intermediate checks/approvals to an advisory reviewer (such as grok-cc advisory review), the workflow SHALL proceed through intermediate stages without pausing for conversational human confirmation once review/verification PASS evidence is established. The workflow SHALL stop only for genuine blockers, breaker limits, or user-reserved Git and production boundaries.

#### Scenario: Delegated review allows continuous slice progression
- **WHEN** the user instructs closed-loop execution or delegates intermediate signoff to an advisory reviewer
- **AND** intermediate verification and review PASS evidence is established for the current slice
- **THEN** the workflow SHALL advance directly to the next authorized slice
- **AND** the workflow SHALL NOT halt solely to ask the user whether to continue
