## ADDED Requirements

### Requirement: Literal current goal and verification handback

After classification and authorization, the current goal SHALL be only the deliverable the user literally requested in the current turn. The workflow SHALL NOT infer a broader goal from prior context and SHALL NOT upgrade verification into a fix. `VERIFY` SHALL deliver a fact report. A failure found during `VERIFY` SHALL be the delivered conclusion and SHALL NOT authorize a fix, profiling, a business-code edit, a new test, or an advisor call in that round. Other independent checks MAY finish, and the round SHALL then stop.

#### Scenario: Verification finds one timeout

- **WHEN** the user asks to verify five regression checks and one check times out
- **THEN** the agent SHALL report the failed item, evidence path, pass and fail counts, and the observed timeout
- **AND** the agent SHALL NOT edit business code, create a Git commit, add a test, profile the failure, or call an advisor in that round

#### Scenario: Verification finds a pre-existing failure

- **WHEN** a verification check fails because of a pre-existing issue that this change did not introduce
- **THEN** the workflow SHALL NOT treat that failure as a failure introduced by this change
- **AND** the workflow SHALL NOT start a fix from that result alone

### Requirement: Diagnosis checkpoint before a single-hypothesis fix

When reproduction or diagnosis is complete, the workflow SHALL emit a user-visible checkpoint report and stop. It SHALL enter one single-hypothesis fix only after the user confirms that slice. A slice the user already named in the current literal request SHALL count as confirmed, and the workflow SHALL NOT ask again for that same slice. If the same slice's fix fails twice, the workflow SHALL stop and report.

#### Scenario: Diagnosis finishes without a named fix slice

- **WHEN** reproduction or diagnosis completes and the current literal request did not name the fix slice
- **THEN** the agent SHALL present the checkpoint report and stop
- **AND** the agent SHALL NOT start a fix in that round

#### Scenario: The same slice fails twice

- **WHEN** the user has confirmed one fix slice and that slice's fix has failed twice
- **THEN** the agent SHALL stop and report
- **AND** the agent SHALL NOT start a third fix attempt or a second hypothesis in that round

### Requirement: Added closure stop conditions

The workflow SHALL stop the affected action when the task type changes, a new root cause is outside the original slice, the round budget is reached, an advisor is consulted more than once for the same slice, or a suggested fix exceeds the files or modules recorded at Gate 0. These conditions add to the existing scope, approval, contract, and evidence stops. They SHALL NOT remove those existing stops.

#### Scenario: Suggested fix leaves the Gate 0 file list

- **WHEN** a suggested fix touches a file or module that Gate 0 did not record
- **THEN** the agent SHALL stop the affected action and ask the user
- **AND** the agent SHALL NOT edit that file under the current slice

#### Scenario: Making the next step concrete

- **WHEN** the user has not yet approved the next slice and the agent needs to make that next step concrete
- **THEN** the agent SHALL produce a report plus one suggested slice
- **AND** the agent SHALL NOT implement that slice as part of making the step concrete
