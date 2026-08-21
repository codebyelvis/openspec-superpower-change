## ADDED Requirements

### Requirement: Explicit role-first reviewer assignment

Every Review request, recommendation, prompt, and governed assignment SHALL
resolve a non-blank Review purpose, one concrete reviewer product, reviewer role,
capability profile, instance-independence requirement, and result authority
before the Review is treated as actionable. The workflow SHALL NOT accept a
missing or blank purpose or use an unresolved “other agent”, “independent agent”,
“another model”, or equivalent label as the sole Review destination.

#### Scenario: User asks another agent to Review
- **WHEN** the user asks for “another agent” to Review without selecting a product
- **THEN** the control plane SHALL recommend one concrete eligible reviewer product
- **AND** it SHALL state the Review purpose, role, capability profile,
  instance-independence requirement, and whether the result is advisory,
  governed evidence, or a canonical control-plane decision

#### Scenario: Review purpose is missing or blank
- **WHEN** a Review request, recommendation, prompt, Handoff, or governed
  assignment omits its Review purpose or supplies only blank text
- **THEN** validation or Preflight Review SHALL reject the assignment
- **AND** the Review SHALL NOT be treated as actionable or satisfy a gate

#### Scenario: User selects Pi as reviewer
- **WHEN** the user explicitly selects Pi for a Review that Pi is eligible to perform
- **THEN** the Reviewer Assignment Contract SHALL preserve product `pi`
- **AND** the workflow SHALL NOT silently substitute Codex, Antigravity CLI, or
  Grok CLI

#### Scenario: Same implementation instance is proposed as reviewer
- **WHEN** the proposed reviewer instance is the executor or otherwise
  participated in the implementation being independently reviewed
- **THEN** governed independent Review SHALL be rejected
- **AND** the workflow SHALL require a distinct eligible instance or return
  `BLOCKED`

#### Scenario: Advisory Review is requested
- **WHEN** a standalone Review does not decide a governed gate or final completion
- **THEN** its concise assignment SHALL still name the concrete product and role
- **AND** its result authority SHALL be labeled advisory rather than canonical

#### Scenario: Required reviewer is unavailable
- **WHEN** no eligible product instance satisfies a required standard or strict
  independent Review assignment
- **THEN** the Review gate SHALL return `BLOCKED` with an owner and resume condition
- **AND** it SHALL NOT downgrade the work or emit an unresolved generic destination

### Requirement: Schema-6 governed Reviewer Assignment Contract

New Handoff-backed external work SHALL use schema 6 and SHALL contain exactly one
always-present immutable `reviewer_assignment`. That mapping SHALL contain
exactly structured `review_purpose`, `agent_product`, `agent_instance_id`,
`agent_role`, `capability_profile`, structured `independence_requirement`, and
`result_authority`. Review purpose SHALL contain exactly non-blank `object` and
`decision` strings. Independence SHALL contain exactly
`kind: distinct-contract-instance` and a duplicate-free `distinct_from` list of
canonical assignment names. Governed result authority SHALL be exactly
`governed-review-evidence`.

The schema-6 top-level required set SHALL be exactly the frozen schema-5 set
minus `independent_reviewer_assignment`, plus `reviewer_assignment`, with
`schema_version: 6`. Its exact immutable set SHALL apply the same replacement to
the frozen schema-5 `readonly_fields`; all other lifecycle fields and values
remain unchanged unless this requirement overrides them. `schema_version` SHALL
be the sole structural discriminator and no optional compatibility discriminator
SHALL be accepted.

Schema-6 `readonly_fields` SHALL include the complete `reviewer_assignment` and
every existing immutable routing field. Schema-2 Review evidence SHALL match the
assignment product, instance, role, and profile; its earlier canonical revision
and SHA-256 SHALL bind the complete immutable purpose, independence requirement,
and result authority. No Review result SHALL self-authorize a canonical
transition or final completion.

#### Scenario: Standard or strict independent Review is assigned
- **WHEN** a schema-6 standard or strict Handoff is created
- **THEN** `reviewer_assignment` SHALL bind role `independent-reviewer`, profile
  `control-plane-high`, and `distinct_from` exactly to `control_plane_owner` and
  `executor_assignment`
- **AND** its instance ID SHALL differ from both resolved assignment instances
- **AND** `independent_review_not_applicable_reason` SHALL be `null`

#### Scenario: Compact control-plane Review is assigned
- **WHEN** a schema-6 compact Handoff uses control-plane inline Review
- **THEN** reviewer product, instance, role, and profile SHALL exactly match
  `control_plane_owner`
- **AND** independence SHALL name only `executor_assignment`, the resolved
  instances SHALL differ, and `independent_review_not_applicable_reason` SHALL be non-blank
- **AND** the Review result SHALL remain governed evidence rather than canonical completion

#### Scenario: Reviewer Assignment shape is incomplete or extended
- **WHEN** a schema-6 assignment has a missing, extra, blank, malformed, or
  duplicated purpose/identity/independence/authority field
- **THEN** Router and Companion validation SHALL reject the Handoff
- **AND** no Brief, execution, Review, evidence acceptance, or transition SHALL proceed

#### Scenario: Immutable Reviewer Assignment changes during a transition
- **WHEN** a proposed schema-6 transition changes Review purpose, reviewer
  identity, independence requirement, or result authority
- **THEN** previous-status validation SHALL reject the transition
- **AND** a new approval-bound contract SHALL be required instead of mutating the assignment

#### Scenario: Review evidence is bound to a different purpose or assignment
- **WHEN** Review evidence identity differs from `reviewer_assignment` or its
  canonical source revision/SHA-256 does not bind the reviewed immutable assignment
- **THEN** evidence validation SHALL reject the artifact
- **AND** the Handoff SHALL NOT advance

#### Scenario: Old-shape current Handoff is supplied after cutover
- **WHEN** a current or resumable governed Handoff uses schema 4, schema 5, a
  missing discriminator, or the old four-field reviewer shape after schema-6 deployment
- **THEN** current-workflow validation SHALL reject it
- **AND** file path, timestamp, mtime, prose, missing fields, or product value
  SHALL NOT grandfather it into transition authority

#### Scenario: Legacy audit is mistaken for current validation
- **WHEN** a caller supplies schema 4 or schema 5 to a current creation,
  validation, evidence, transition, resume, or completion entry point
- **THEN** the current entry point SHALL reject it regardless of structural legacy validity
- **AND** a separate read-only legacy inventory/audit MAY report only path,
  schema, lifecycle, immutable fingerprint, and drain status
- **AND** that audit result SHALL NOT be reusable as current-contract PASS or authority

## MODIFIED Requirements

### Requirement: Codex-primary auxiliary-agent collaboration

The workflow SHALL keep Codex as the single owner of routing, approval,
canonical state transitions, evidence acceptance, final verification, and final
completion while allowing Codex, Pi, Antigravity CLI, and Grok CLI instances to
serve as explicitly assigned schema-6 batch executors or independent reviewers.

External collaboration SHALL bind immutable executor, independent-reviewer,
and decision-owner product/instance/role/profile identities; Report and Review
evidence SHALL bind the producing agent identity and role. Canonical agent
schema-6 products SHALL be exactly `codex`, `pi`, `antigravity-cli`, or `grok-cli`, and
the control-plane decision owner SHALL be the bound product `codex`, role
`control-plane`, profile `control-plane-high`, instance, and governing contract.
No product name by itself SHALL grant authority. All four products SHALL have
equal eligibility for executor and independent-reviewer roles under their bound
role/profile/instance/contract.

#### Scenario: Implementation and Review are separated
- **GIVEN** at least two eligible instances are available for a standard or
  strict external batch
- **WHEN** one assigned instance implements the batch
- **THEN** another assigned instance SHALL independently review its diff,
  Report, contract, and evidence
- **AND** the bound Codex control plane SHALL audit both outputs before recording
  the authoritative transition

#### Scenario: Second reviewer is unavailable
- **GIVEN** a standard or strict external batch has an assigned executor
- **WHEN** no distinct eligible instance can perform the independent Review
- **THEN** the batch SHALL be `BLOCKED`
- **AND** the existing standard or strict contract SHALL NOT be downgraded by waiver

#### Scenario: Same agent instance attempts independent self-review
- **WHEN** executor and independent-reviewer instance identities are equal, or
  evidence product/instance/role/profile does not match the canonical assignment
- **THEN** validation SHALL reject the Report or Review
- **AND** the batch SHALL NOT advance

#### Scenario: Unknown identity or non-Codex decision owner
- **WHEN** a contract uses a product outside the canonical enum or binds a
  non-Codex product as control-plane decision owner
- **THEN** validation SHALL reject the contract
- **AND** no evidence or state transition SHALL be accepted

#### Scenario: Product name is presented as authority
- **WHEN** an assignment or result claims canonical authority from product name
  alone without the bound Codex control-plane role, profile, instance, and contract
- **THEN** validation or control-plane audit SHALL reject the authority claim
- **AND** executor or reviewer eligibility SHALL remain equal across all four products

#### Scenario: Assigned reviewer claims completion
- **WHEN** a Pi, Codex, Antigravity CLI, or Grok CLI independent reviewer reports
  `PASS` or claims the whole task complete
- **THEN** its result SHALL remain Review evidence
- **AND** canonical state and final completion SHALL NOT advance until the bound
  Codex control plane runs required verification and records its decision

#### Scenario: Review finding requires correction
- **WHEN** an assigned Review or Codex control-plane Review contains an
  actionable finding
- **THEN** the same scope SHALL return to correction and verification
- **AND** a fresh Review SHALL be required before promotion or completion

#### Scenario: Active legacy contract exists during upgrade
- **WHEN** pre-deployment inventory finds any active schema-4 or schema-5 contract
- **THEN** deployment SHALL be `BLOCKED` until that workflow reaches its existing
  `complete` state under the pre-upgrade runtime and schema
- **AND** immutable historical state SHALL NOT be rewritten, ignored, or silently migrated

### Requirement: Post-optimization cross-CLI synchronization gate

The workflow SHALL, after either core workflow Skill or its shared governance
rules change, synchronize every declared required runtime target and verify
source parity, validation, and discovery before claiming the global Skill
optimization complete.

#### Scenario: All four runtimes are required
- **GIVEN** Codex, Pi, Antigravity CLI, and Grok CLI are declared required targets
- **WHEN** source validation and Review pass
- **THEN** both core Skills and the managed governance block SHALL be
  synchronized to all four runtime roots
- **AND** each target SHALL pass its compatible validator and discovery check
- **AND** final completion SHALL remain blocked until four-target parity passes

#### Scenario: Pi executable capability is probed
- **WHEN** implementation checks Pi version/help surfaces or runs an optional
  prompt probe
- **THEN** `HOME` and `PI_CODING_AGENT_DIR` SHALL resolve inside a fresh temporary
  root and enforceable isolation SHALL deny access to the native Pi agent root
- **AND** inherited sessions, context, and Skills SHALL be disabled; a prompt
  probe SHALL additionally use no-session/no-context/no-skills, read-only tools,
  and network denial
- **AND** direct native-root Pi CLI probing or unproven isolation SHALL be rejected

#### Scenario: A target is unavailable
- **WHEN** a required runtime is missing, stale, undiscoverable, or fails validation
- **THEN** synchronization status SHALL be `BLOCKED`
- **AND** the workflow SHALL record the target, reason, owner, and resume condition
- **AND** it SHALL NOT claim global Skill optimization complete

#### Scenario: Target is explicitly not applicable
- **WHEN** an uninstalled, unsupported, or user-excluded target is declared
  `not-applicable` before synchronization
- **THEN** the decision SHALL include owner, evidence, non-blank reason, and
  resume condition
- **AND** completion MAY proceed without that target only if all remaining
  required targets pass

#### Scenario: Failure is mislabeled not applicable
- **WHEN** an installed required target is stale, undiscoverable, or fails validation
- **THEN** the target SHALL remain `BLOCKED` rather than `not-applicable`
- **AND** global Skill optimization SHALL NOT be called complete

#### Scenario: Repository-only documentation changes
- **WHEN** only README, changelog, tests, design history, or archived OpenSpec files change
- **THEN** no runtime synchronization SHALL be required
- **AND** the ordinary repository validation and Review rules SHALL still apply

### Requirement: Safe semantic global-rule alignment

The workflow SHALL keep one versioned, stable-ID governance invariant block
aligned across Codex, Pi, Antigravity CLI, and Grok CLI while preserving native
overlays and excluding sensitive or runtime-owned configuration from synchronization.

Managed version 6 SHALL revise `CCG-001`, `CCG-002`, and `CCG-010` to bind canonical
authority to the assigned Codex control-plane role/profile/instance/contract and
equal schema-6 executor/reviewer eligibility to all four products, define the
schema-4/schema-5 drain and immutable-history boundary, and SHALL add `CCG-016`
with the complete Reviewer Assignment Contract including Review purpose.
Validation SHALL bind these semantics rather than only marker version, ID count,
or hash presence.

#### Scenario: Global rule files use different native formats
- **WHEN** the four coding-agent runtimes use different filenames, precedence
  rules, or tool syntax
- **THEN** the shared governance invariants SHALL remain equivalent
- **AND** exactly one managed begin/end marker block SHALL be inserted or replaced
- **AND** runtime-specific bytes outside that block SHALL remain unchanged

#### Scenario: Managed v6 keeps old product-level authority wording
- **WHEN** a candidate v6 block retains product-name-only authority in `CCG-001`,
  omits any of the four products from equal executor/reviewer eligibility in
  `CCG-002`, omits the schema-6/old-schema drain boundary from `CCG-010`, or
  omits Review purpose from `CCG-016`
- **THEN** semantic regression validation SHALL reject the block
- **AND** matching IDs, count, version, or aggregate body hash SHALL NOT override
  the semantic failure

#### Scenario: Portable Skill parity
- **WHEN** a portable Skill file is synchronized
- **THEN** its relative path and SHA-256 SHALL match the canonical source manifest
- **AND** drift SHALL block the sync gate

#### Scenario: Sensitive category enters a sync manifest
- **WHEN** a proposed sync includes credentials, auth/token files, sessions,
  history, logs, caches, model settings, extensions, hooks, MCP secrets, or CLI binaries
- **THEN** validation SHALL reject the manifest
- **AND** no sensitive category SHALL be copied to another runtime

#### Scenario: Unsafe source or destination path
- **WHEN** a manifest path is absolute, traverses its declared root, resolves
  through a symlink outside that root, or is not a regular file
- **THEN** validation SHALL reject synchronization before any target replacement
- **AND** diagnostics SHALL identify only the path/category without printing
  sensitive content

### Requirement: Schema-5 product, instance, and role identity

Existing schema-5 contracts SHALL retain the exact pre-change three-product
enum—`codex`, `antigravity-cli`, and `grok-cli`—and the exact pre-change
four-field assignment, schema-2 evidence, transition, and authority semantics.
Schema 5 SHALL NOT admit Pi or any partial schema-6 Reviewer Assignment fields.
Before schema-6 runtime deployment, every active schema-4 or schema-5 contract
SHALL reach `complete` under its existing runtime. After cutover, older complete
contracts/evidence SHALL remain byte-immutable audit history and SHALL NOT
authorize a current transition. New governed external contracts SHALL use
schema 6.

#### Scenario: Active schema-5 contract exists before deployment
- **WHEN** the fresh pre-deployment inventory finds a schema-5 Handoff whose
  lifecycle is not `complete`
- **THEN** schema-6 runtime deployment SHALL be `BLOCKED`
- **AND** that Handoff SHALL finish under the pre-upgrade schema-5 validator or
  remain blocked; it SHALL NOT be migrated, abandoned, or resumed after cutover

#### Scenario: Pi is supplied to schema 5
- **WHEN** a schema-5 contract or its parent-context schema-2 evidence uses `pi`
- **THEN** the frozen schema-5 validator SHALL reject it
- **AND** only schema 6 MAY assign Pi a governed executor or reviewer role

#### Scenario: Pi identity is supplied to schema 4 or schema 1
- **WHEN** a schema-4 executor or reviewer identity or schema-1 evidence identity
  uses `pi`
- **THEN** validation SHALL apply the frozen pre-change legacy product set and
  reject the artifact
- **AND** the schema-6 enum SHALL NOT reinterpret, migrate, or authorize older state

#### Scenario: Complete old-schema history is inspected after cutover
- **WHEN** a complete schema-4/schema-5 contract or schema-1/schema-2 evidence
  artifact is retained for audit after schema-6 deployment
- **THEN** its bytes SHALL remain unchanged and it SHALL be classified as
  non-current immutable history
- **AND** it SHALL NOT satisfy creation, transition, Review, or completion
  authority for a schema-6 Handoff

#### Scenario: Requested product is substituted
- **WHEN** a canonical assignment or explicit user decision selects one eligible
  reviewer product and generated Review instructions name a different product
- **THEN** validation or Preflight Review SHALL reject the substitution
- **AND** the original assignment SHALL remain authoritative until explicitly revised

#### Scenario: Schema-6 instance or role impersonation
- **WHEN** Report or Review evidence has the wrong product, instance, role, or
  capability profile for the canonical assignment
- **THEN** validation SHALL reject the evidence
- **AND** canonical state SHALL NOT advance

#### Scenario: No active old schema is confirmed
- **WHEN** the source Review has passed and runtime synchronization is about to begin
- **THEN** inventory SHALL prove no active schema-4 or schema-5 canonical Handoff
  exists in every known root
- **AND** the same inventory SHALL be repeated immediately before the first apply
- **AND** missing roots, ambiguous state, or any active old schema SHALL return `BLOCKED`
