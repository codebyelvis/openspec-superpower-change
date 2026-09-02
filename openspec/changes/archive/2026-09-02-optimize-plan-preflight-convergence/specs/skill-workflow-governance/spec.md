## MODIFIED Requirements

### Requirement: Mandatory review correction loop

Every implementation path SHALL complete a current-revision Preflight Review,
verification, and post-implementation Review before completion. Gate-bearing
Preflight SHALL retain exactly `PASS` and `BLOCKED` results.
`FULL_PREFLIGHT` and `FOCUSED_RECHECK` are Review modes;
`CONTROL_PLANE_ADJUDICATION` is an existing-control-plane convergence route
outside Preflight Review, not a Review mode or canonical state.

The first review in a lineage SHALL be `FULL_PREFLIGHT`, cover the complete
prescribed matrix and an independent adversarial probe, and attest that all
findings reasonably discoverable from supplied evidence were reported. Every
blocking finding SHALL prevent execution.

A revised artifact MAY use `FOCUSED_RECHECK` only when mechanical self-check
passes; the same independent reviewer instance continues; scope, contract/spec,
acceptance, risk/evidence profile, authority, assignments, allowed/forbidden
files, branch/worktree, database/production, and Git/publication/deployment
boundaries are each verified unchanged; and the diff is limited to declared
finding corrections plus necessary adjacent edits.

The existing Preflight Review artifact SHALL record mode; safe project-relative
root/current artifact paths and whole-file SHA-256 values; safe project-relative
parent Review path and whole-file SHA-256; attempt; exact reviewer product,
contract-local instance ID, role, and capability profile; a same-reviewer value
derived from immutable parent identity; an explicit protected-boundary checklist;
declared finding IDs and section anchors;
mechanical evidence; completeness; blocking findings; and recommendations. SHA
values SHALL cover whole regular-file bytes exactly as stored without newline
normalization. Root/current paths SHALL be identical logical paths; path drift
and same-hash substitution at another path are invalid. Current SHA SHALL match
the current regular non-symlink file. At full root, root/current SHA values SHALL
match; after correction, the verified immutable parent Review SHALL anchor the
historical root SHA and reviewer identity without requiring historical bytes at
the mutated path. Every evidence reference SHALL resolve to a regular non-symlink
file within project root. Missing legacy fields SHALL select full review.
Invalid revision/parent binding, replacement reviewer, reviewer identity reused
from author/executor, changed boundary, or undeclared diff SHALL prevent focused
eligibility. This Review
evidence SHALL NOT become a schema, Handoff field, task ledger, or canonical
state.

After two blocked Review results in one lineage, reviewer conflict, expanding
correction scope, an unauthorized protected-boundary change, or a late ordinary
finding that should have been detected during full review, the workflow SHALL
route to `CONTROL_PLANE_ADJUDICATION`. An already-authorized boundary change
SHALL start a new lineage at full review; an unauthorized change SHALL remain
`BLOCKED` until adjudicated and then, if authorized, start a new full lineage.
Adjudication MAY permit one terminal focused recheck after one consolidated
correction bundle; terminal failure SHALL not reopen an unlimited loop.

A non-blocking recommendation SHALL be optional and SHALL NOT contradict
acceptance, safety, authority, evidence integrity, or deterministic execution.
A non-actionable observation with actual residual risk SHALL remain separately
classified as accepted residual risk with impact and owner or decision; it SHALL
NOT be relabeled as a recommendation or unresolved actionable finding. P0/P1,
security, integrity/data-loss, authority, scope, contract, risk, acceptance,
forbidden-effect, false-evidence, and non-executable-plan findings SHALL remain
blocking in every mode.

#### Scenario: First review is complete

- **WHEN** a Plan or Brief enters its first Preflight in a lineage
- **THEN** `FULL_PREFLIGHT` covers the complete matrix and adversarial probe
- **AND** reports all reasonably discoverable findings with completeness true

#### Scenario: Same-scope mechanical correction

- **GIVEN** a full review reported a bounded finding set
- **AND** the same reviewer and every protected boundary remain unchanged
- **WHEN** mechanical self-check passes and the diff only closes those findings
- **THEN** the next Review uses `FOCUSED_RECHECK`
- **AND** unaffected full-review work is not replayed

#### Scenario: Protected boundary changes

- **WHEN** any protected boundary or reviewer instance changes
- **THEN** focused eligibility ends
- **AND** an authorized revision starts a new full lineage while an unauthorized
  revision remains blocked for adjudication

#### Scenario: Legacy Review lacks convergence fields

- **WHEN** historical Preflight Review evidence lacks the new record fields
- **THEN** it remains historical evidence
- **AND** the next Review uses `FULL_PREFLIGHT`

#### Scenario: Safety finding appears during focused review

- **WHEN** focused review identifies P0/P1, security, integrity/data-loss, or
  authority risk
- **THEN** Preflight is `BLOCKED`
- **AND** completeness and retry limits do not suppress the finding

#### Scenario: Reviewer serially adds earlier-discoverable finding

- **GIVEN** full review attested completeness
- **WHEN** focused review adds an ordinary finding already discoverable in the
  root revision and not caused by correction
- **THEN** it records a completeness breach
- **AND** routes to adjudication instead of another serial Review loop

#### Scenario: Two blocked rounds do not converge

- **GIVEN** one full Review and one focused recheck are both blocked
- **WHEN** another retry would begin
- **THEN** control-plane adjudication consolidates the decision
- **AND** at most one terminal focused recheck may follow

#### Scenario: Non-blocking recommendation

- **WHEN** optional improvement affects no acceptance, safety, authority,
  evidence-integrity, or execution requirement
- **THEN** Review records impact and owner/decision
- **AND** recommendation alone does not change `PASS` to `BLOCKED`

#### Scenario: Non-actionable residual risk remains distinct

- **WHEN** Review observes actual residual risk that requires no current change
- **THEN** it records accepted residual risk with impact and owner or decision
- **AND** it is neither an optional recommendation nor unresolved finding

#### Scenario: Later Reviews remain mandatory

- **WHEN** Plan Preflight passes
- **THEN** profile-appropriate verification and Implementation Review remain
  mandatory
- **AND** completion still requires fresh final verification, Final Review, and
  Completion Contract

### Requirement: Profile-weighted workflow remains proportionate

The workflow SHALL preserve compact, standard, and strict evidence weight while
enforcing the same approval and completion invariants. Compact low-risk
mechanical work MAY remain inline with focused verification and concise Review
and SHALL NOT create an unnecessary canonical lease. Standard multi-step work
SHALL retain distinct Review and its required critical evidence. Strict real
evidence and explicit human business gates SHALL remain mandatory for its
triggering effects; mocks or platform permission SHALL NOT replace them.

The workflow SHALL use the smallest design, Plan detail, artifact set, and
verification effort adequate for approved behavior and actual changed effects.
It SHALL reuse existing rules, templates, validators, fixtures, and tests before
creating new machinery.

For OpenSpec-backed work, Plan completeness SHALL mean no unresolved material
choice and no non-executable step. Each business slice SHALL identify exact
files/responsibilities, interfaces or signatures, contract/acceptance references,
RED/GREEN intent, exact critical commands, rollback, and stop conditions. It
SHALL NOT require complete implementation bodies when those items make execution
deterministic; complete bodies remain required when omission leaves a material
choice unresolved.

Risk SHALL follow changed effects rather than mere substrate usage. Reading
persistence through an existing private read-only boundary SHALL NOT alone mean
persistence semantics change. Strict SHALL remain mandatory for changes to
security/auth, public API/schema, persistence semantics, migrations, write paths,
deployment/rollback, deletion/recovery, cross-tenant behavior, or production
authority. Any profile change SHALL end focused eligibility and require full
review.

#### Scenario: Compact mechanical task

- **WHEN** a low-risk deterministic task has no open architecture, security,
  persistence-semantics, production, or public-contract decision
- **THEN** it may remain inline with focused verification and concise Review
- **AND** no unnecessary canonical lease artifact is created

#### Scenario: Standard multi-step task

- **WHEN** a multi-step change has no strict trigger
- **THEN** standard critical evidence and distinct Review remain required
- **AND** Plan proportionality does not downgrade the Review gate

#### Scenario: Strict authorization-sensitive task

- **WHEN** work changes real credentials, authorization, production, migration,
  deletion, release, rollback, recovery, or another strict effect
- **THEN** strict real evidence and explicit human business gates apply
- **AND** mocks or platform permissions cannot replace them

#### Scenario: Executable slice does not duplicate implementation

- **GIVEN** a slice contains exact boundaries, interfaces, acceptance, TDD
  commands, rollback, and stop conditions
- **WHEN** no material implementation decision remains
- **THEN** the Plan may reference approved contract text instead of reproducing
  complete source bodies
- **AND** placeholder validation still rejects unresolved work

#### Scenario: Private read-only persistence consumer

- **GIVEN** a change uses an existing private read-only persistence boundary
- **AND** changes no strict-triggering effect
- **WHEN** evidence profile is classified
- **THEN** substrate usage alone does not force strict
- **AND** required real read-only probes remain mandatory

#### Scenario: Existing strict lineage cannot be downgraded silently

- **GIVEN** an approved lineage is strict
- **WHEN** correction proposes a lower profile
- **THEN** focused recheck is forbidden
- **AND** full control-plane review is required
