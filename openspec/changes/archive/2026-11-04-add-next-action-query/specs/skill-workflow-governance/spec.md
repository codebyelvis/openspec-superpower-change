## ADDED Requirements

### Requirement: Deterministic read-only next-action query

The workflow SHALL expose a read-only query that, given canonical schema-6
`status.md` content, reports the legal next state transition without writing
any state. The query SHALL first run the full structural validation; on
validation failure it SHALL report `BLOCKED` with the reason and produce no
next-action suggestion. On success it SHALL report: the current
lifecycle state and result tuple; each legal next state; the evidence roles
required for that transition bound to executor/reviewer/control-plane
identity; the allowed `next_owner`; the lease state; and, when the current
state is `blocked`, the `blocker_owner` and `resume_condition` verbatim.

The query SHALL reuse the existing transition and owner tables in
`scripts/validate_core_gates.py`; it SHALL NOT copy or duplicate the
transition rules into a second authority. The query output SHALL be
explicitly advisory, SHALL NOT write or generate a proposed status file,
SHALL NOT enter `status.md`, and SHALL NOT act as evidence or substitute
for Router or governor judgment.

#### Scenario: Valid status yields legal next transitions

- **GIVEN** canonical `status.md` passes structural validation
- **WHEN** the read-only next-action query runs
- **THEN** it lists each legal next state with its evidence roles, allowed `next_owner`, and lease state
- **AND** it writes no file and changes no canonical state

#### Scenario: Blocked status returns resume context

- **GIVEN** a strict blocked canonical status with `blocker_owner` and `resume_condition` set
- **WHEN** the read-only next-action query runs
- **THEN** it produces zero automatic transitions and echoes `blocker_owner` and `resume_condition` verbatim
- **AND** it does not suggest a next action

#### Scenario: Invalid status fails closed

- **GIVEN** canonical status content fails structural validation
- **WHEN** the read-only next-action query runs
- **THEN** it reports `BLOCKED` with the validation reason
- **AND** it produces no next-action suggestion

#### Scenario: Advisory output is not authoritative

- **GIVEN** the read-only next-action query reports a next state
- **WHEN** a Router or governor decision differs
- **THEN** the Router/governor decision governs
- **AND** the query output is not recorded as evidence and not written to `status.md`