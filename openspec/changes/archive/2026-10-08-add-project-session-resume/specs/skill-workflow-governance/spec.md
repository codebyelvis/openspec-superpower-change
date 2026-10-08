## ADDED Requirements

### Requirement: Project implementation checkpoint persistence

Authorized unfinished local implementation and external collaboration SHALL
reuse `docs/agent-collab/<change-id>/status.md` as the canonical mutable recovery
record. Before intentional pause, advancing implementation-turn end or window
handoff, the workflow SHALL persist current state, completed references, exactly
one nonterminal `next_action`, blockers and `resume_condition`. Terminal state
SHALL have no pending next action. It SHALL NOT create a second task ledger,
global index, session-start hook or conversation checkpoint system.

OpenSpec work SHALL use its actual change-id. Direct Change SHALL reuse its
scoped ID or record a stable `direct-<slug>` directory identifier only when
pending cross-window work needs a checkpoint; it SHALL NOT fabricate OpenSpec
approval. Completed compact single-turn changes need no checkpoint artifact.

#### Scenario: Local window closes with pending work

- **GIVEN** authorized implementation has completed one step and has pending work
- **WHEN** its advancing turn ends or the agent intentionally pauses
- **THEN** the canonical status records the actual phase, completed references
  and exactly one safe next action with required owner/permission/evidence
- **AND** the next window does not need the prior conversation

#### Scenario: External execution remains outstanding

- **GIVEN** a full Handoff's canonical hash is bound to an outstanding Brief
- **WHEN** the control-plane window ends without new progress
- **THEN** the already-persisted wait action remains canonical
- **AND** the workflow does not invalidate that hash by rewriting progress

### Requirement: Explicit schema-6 local resume subset

Local recovery governance SHALL be an explicitly discriminated schema-6 subset
with the exact fields and existing meanings specified in design draft-v1.
External recovery SHALL reference its same-file complete Handoff governance;
it SHALL NOT copy governance fields into another mutable mapping. Progress
fields SHALL be separate from Handoff governance and remain in that same file.

The explicit resume validation interface SHALL reject duplicate, mixed,
unparsable, contradictory or unsafe state. The existing external `--status`
interface SHALL retain its exact full schema-6 requirements and SHALL NOT accept
a local subset or automatically downgrade after an error. Active schema-4/5
SHALL NOT be migrated or resumed by this feature.

#### Scenario: Valid local checkpoint

- **GIVEN** a record explicitly declares local resume and has the approved subset
- **WHEN** the local resume validator checks it
- **THEN** it validates the local ownership, phase, progress and evidence rules
- **AND** it does not treat that record as an external Handoff or signing proof

#### Scenario: Missing external fields cannot downgrade

- **GIVEN** an external contract is missing required schema-6 fields
- **WHEN** either external validation or recovery is attempted
- **THEN** the result is BLOCKED
- **AND** no missing-field fallback, relabeling or marker removal enables resume

### Requirement: Verified persisted revision is the best checkpoint

The best checkpoint SHALL be the latest required-verification PASS that has
been persisted with its revision, scoped source-input fingerprint, actual
command results and bound evidence references. No latest edit, reply, timestamp
or bare Git HEAD SHALL substitute for it. Changed verified inputs SHALL
invalidate current PASS while preserving the historical checkpoint and edits.
The workflow SHALL NOT automatically roll back to the prior checkpoint.

#### Scenario: Later unverified edit

- **GIVEN** revision R has persisted verification PASS
- **WHEN** an authorized source/config/test input changes after R
- **THEN** recovery identifies the mismatch and selects verification or fix
- **AND** R remains historical evidence without certifying the changed tree

#### Scenario: Unsafe or unresolved evidence path

- **WHEN** a checkpoint reference escapes the bound project root, traverses a
  symlink, lacks required evidence or conflicts with its scope fingerprint
- **THEN** the verified claim and advancing recovery are BLOCKED

### Requirement: Bounded recovery from persisted project state

After compaction, window/agent/model switch or `继续` / `继续闭环` / `闭环推进`,
the workflow SHALL recover the selected persisted status and referenced
contract/plan/evidence, validate them, and perform its unique authorized next
action without re-asking unchanged approved steps. Multiple unfinished changes
SHALL require user selection and SHALL NOT be selected automatically.

Continuation SHALL NOT grant OpenSpec approval, Git push, production writes,
owner transfer, signing or completion authority. Any loaded agent MAY read the
state; mutation and decisions SHALL require existing bound identity/assignment.
Different models in the same valid instance SHALL NOT change authority. An
unassigned new instance SHALL report the existing reassignment boundary and
SHALL NOT impersonate the prior controller. Invalid state SHALL fail closed,
not fall back to a last chat message or auto-create a replacement record.

#### Scenario: Valid assigned new-window recovery

- **GIVEN** one unfinished selected record, valid existing assignment and scope
- **WHEN** the agent receives `继续闭环` without prior chat
- **THEN** it validates and continues the persisted next action
- **AND** it does not ask again for approval already recorded for that action

#### Scenario: New instance has no assignment

- **WHEN** a new instance can read the checkpoint but lacks its required role
- **THEN** it reports recovered state and the ownership blocker/resume condition
- **AND** it cannot rebind itself, sign evidence or claim completion

#### Scenario: Two unfinished changes

- **WHEN** recovery finds more than one unfinished change
- **THEN** it asks the user to select one before implementation
- **AND** it does not choose by recency, priority or the latest reply

### Requirement: Resume preserves existing completion transitions

Checkpoint creation and recovery SHALL preserve existing risk, approval,
verification, Review, ownership and completion rules. Local transitions SHALL
use existing lifecycle values and risk-applicable gates. External complete
SHALL still require separately persisted final verification, final Review and
actual previous-status proof. A best checkpoint or batch PASS SHALL NOT become
whole-task completion. Completed records SHALL remain terminal.

#### Scenario: Best checkpoint with pending final gates

- **GIVEN** implementation tests have passed and a verified checkpoint exists
- **WHEN** required final Review or closeout evidence remains pending
- **THEN** status remains at the applicable nonterminal gate with one next action
- **AND** the workflow cannot mark complete

#### Scenario: External atomic final completion is rejected

- **WHEN** resume attempts to combine pending final verification, final Review
  and complete in one external status update
- **THEN** existing transition validation rejects it
- **AND** the local resume feature cannot bypass that rejection
