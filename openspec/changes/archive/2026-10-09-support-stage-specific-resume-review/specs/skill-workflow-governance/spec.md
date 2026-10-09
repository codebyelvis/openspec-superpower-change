## ADDED Requirements

### Requirement: Strict local phase-specific reviewer binding

A local strict Resume Context SHALL accept either its existing full seven-field
reviewer_assignment or an exact phase mapping under that same field, containing
only implementation-review and final-review. Each entry SHALL be a complete
eligible existing seven-field assignment. The mapping SHALL validate both
entries on every load and SHALL require distinct reviewer instances from each
other and the bound controller/local executor. Implementation independence SHALL
retain the two existing targets; Final SHALL additionally name
implementation_reviewer. No external executor SHALL be invented for local work.

Evidence SHALL retain one assignment and identity. Its evidence_role SHALL select
the exact approved mapping entry, including purpose, product, instance, role,
profile, independence and governed authority. Mixed, incomplete, duplicate,
unknown or malformed forms SHALL fail closed without fallback. The nine context
outer fields, schema-6 governance/progress fields and state path SHALL remain.

#### Scenario: Approved distinct local reviewers

- **GIVEN** a strict local context binds independent Implementation and Final instances
- **WHEN** each stage's actual Review is validated
- **THEN** its complete assignment and identity match that exact stage entry
- **AND** the original implementation/final gates and controller authority remain

#### Scenario: Wrong stage or reused instance

- **WHEN** evidence substitutes the other stage's assignment or the mapping reuses an instance
- **THEN** validation rejects it before a canonical transition
- **AND** eligibility or a model name cannot substitute for assignment

#### Scenario: Malformed phase map

- **WHEN** a stage is missing/null, an unknown key is added or the forms are mixed
- **THEN** validation fails without selecting another form or lowering the profile

### Requirement: Stage-bound recovery preserves persisted completion

Strict stage-form local entry to awaiting-final-verification SHALL validate
Implementation Review against actual prior revision/SHA and verified scoped
inputs. Recovery SHALL revalidate retained applicable stage evidence. Complete
SHALL require actual previous awaiting-final-verification, unchanged already
persisted final verification and distinct Final Review bound to that prior
snapshot. Read-only recorded-complete recovery SHALL check both stage assignments
and checkpoint consistency without issuing new signoff or claiming reconstructed
previous bytes. Atomic verify/review/complete and stale evidence SHALL fail.

#### Scenario: New window before final gate

- **GIVEN** a persisted stage-form checkpoint with valid Implementation Review
- **WHEN** a new window reads it
- **THEN** it validates that Review and unchanged inputs, exposing the pending gate
- **AND** an unassigned reader does not acquire control-plane or completion authority

#### Scenario: Separate final verification and Final Review

- **GIVEN** actual final verification was persisted in awaiting-final-verification
- **WHEN** the bound controller proposes complete with the assigned distinct Final Review
- **THEN** validation checks actual previous bytes and the unchanged checkpoint
- **AND** it returns factual consistency with authority_granted=false

#### Scenario: Atomic or stale completion

- **WHEN** verification/review/complete are collapsed or a bound input/prior snapshot changed
- **THEN** validation rejects completion and preserves the historical checkpoint

### Requirement: Specifically approved blocked reviewer-context amendment

Ordinary local context references SHALL remain immutable. An explicit hashed
approving-contract input MAY enable only the draft-v1 design's bounded amendment.
The approval record SHALL own exactly one Resume Amendment Authorization with
amendment_kind, change_id, previous_contract, next_contract_path and the exact
reviewer_assignment map. Its own context SHALL be specifically approved strict
Self-Evolution, same-controller and explicitly scoped for amend-review-binding.
Real user approval SHALL be recorded before action; validator consistency SHALL
NOT create approval, authentication, ownership, execution or completion rights.

The validator SHALL load actual previous canonical/context bytes and a proposed
context through existing safe hash/parsing rules. Both states SHALL be approved,
local strict, blocked, unverified, and otherwise identical except the new hashed
contract reference and one revision increment. All context facts except the
reviewer assignment SHALL remain identical, and the Implementation entry SHALL
retain the exact previous single assignment. Approval scope/hashes and target
mapping/path SHALL match in full. Old approved bytes/evidence SHALL be preserved.

The explicit CLI input SHALL require resume-status/artifact-root/previous-status
and SHALL NOT apply to full external status, normal recovery or automatic migration.
The already-bound controller SHALL check actual prior bytes still match before
atomic replacement. Amendment SHALL preserve wait/blockers and SHALL NOT advance
readiness. A later normal transition retains all existing readiness/Review gates.

#### Scenario: Explicit approved metadata-only conversion

- **GIVEN** a specifically approved reviewer amendment and actual blocked unverified prior state
- **WHEN** only the contract ref and required revision increment change as authorized
- **THEN** validation accepts the guarded blocked-to-blocked conversion
- **AND** original contract/history remain and no implementation/readiness PASS is issued

#### Scenario: Ordinary context swap or unapproved opt-in

- **WHEN** context changes without the explicit correctly hashed scoped approval
- **THEN** validation rejects the swap and does not rewrite canonical state

#### Scenario: Amendment tries to change authority or evidence

- **WHEN** the owner/actions/commands/approval/risk, retained history, wait/blocker or verification changes
- **THEN** the amendment fails before canonical replacement

#### Scenario: Wrong lifecycle or previous bytes

- **WHEN** either state is external/non-strict/non-blocked/verified, or actual prior bytes drift
- **THEN** the amendment fails with old context and canonical bytes retained

### Requirement: Single scoped S8 binding repair retains compatibility

This change SHALL authorize only the post-gate S8 amendment specified in design:
original approval.md with SHA-256
233d318470241a5eb22eea9186bb372d72db6b65bf9556f6ffa818318e924873 remains
unchanged; the new context is add-project-document-ownership/resume-contract-v2.md;
its Implementation assignment remains s8-review-01 and its complete approved Final
assignment is s8-final-01 as specified. Actual canonical state remains at the
existing S8 path. Original S8 contract, acceptance, strict profile and distinct
Final SHALL remain. S9 SHALL NOT implement S8 or sign its pending readiness.

Old full single assignments, local standard/compact, complete external Handoff,
legacy schema-4/schema-5 history, evidence interfaces and completion authority
SHALL retain their existing semantics. A needed excluded change SHALL require a
new specific scope approval. Source proof SHALL be followed by the existing
four-target scoped sync of only the two changed portable files before closure.

#### Scenario: S8 context representation repaired

- **GIVEN** S9 is specifically approved and source proof, Implementation Review and sync pass
- **WHEN** the sole authorized S8 context amendment is persisted
- **THEN** S8 remains blocked with original contracts and its distinct Final binding intact
- **AND** S9 final verification/Final Review cover the actual amended diff before S9 closure
- **AND** fresh S8 readiness is required in a new changed-binding lineage

#### Scenario: Legacy or external record

- **WHEN** an existing single-assignment or complete external context is read
- **THEN** the existing rule applies without a stage-map fallback or historical migration

#### Scenario: No current implementation approval

- **GIVEN** only generic continue/edit instructions and this unapproved proposal
- **WHEN** the round concludes
- **THEN** it leaves reviewable artifacts and S8 blocked, with no source/runtime/Git change
