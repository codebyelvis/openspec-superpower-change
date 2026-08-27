# skill-workflow-governance Specification

## Purpose
Define deterministic ownership, approval, evidence, review, correction, and
completion rules for the `openspec-superpower-change` and
`codex-brief-antigravity-review` skill pair.
## Requirements
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

### Requirement: Non-duplicated OpenSpec and Superpowers ownership
The workflow SHALL use OpenSpec as the single approved design contract and SHALL
map applicable Superpowers discovery, planning, TDD, Review, and verification
discipline onto that contract without creating a duplicate design approval or
granting Git permission.

#### Scenario: OpenSpec-backed brainstorming
- **WHEN** brainstorming applies to an OpenSpec-required change
- **THEN** its decisions are recorded in the OpenSpec proposal/design
- **AND** the same decision does not require a second `docs/superpowers/specs/`
  artifact or approval

#### Scenario: Plan contains Git steps
- **GIVEN** the current user has not explicitly authorized Git mutation
- **WHEN** a Superpowers plan is prepared for execution
- **THEN** `git add`, `git commit`, and `git push` steps are removed or blocked
- **AND** the plan itself does not count as authorization

### Requirement: Mandatory review correction loop
Every implementation path SHALL complete a current-revision Preflight Review,
verification, and post-implementation Review before completion. Every actionable
finding SHALL restart the corresponding correction and Review loop.

#### Scenario: Preflight finding
- **WHEN** a Plan or external Brief has an executable gap, placeholder, scope
  conflict, missing command, or unauthorized Git step
- **THEN** implementation or dispatch does not start
- **AND** the artifact is revised and reviewed again

#### Scenario: Non-actionable observation
- **WHEN** Review records an observation that requires no change
- **THEN** it is explicitly classified as an accepted residual risk with an owner
  or decision
- **AND** it is not represented as an unresolved actionable finding

### Requirement: Canonical auditable handoff state
Handoff-backed external execution SHALL use schema version 3 with exactly one
canonical state block, non-empty critical checks, safe evidence references,
sequential final-gate persistence, and attempt history.

#### Scenario: Empty verification contract
- **WHEN** any external Handoff has an empty or blank `step_critical` or
  `final_critical` entry
- **THEN** both validators reject the contract

#### Scenario: Final verification passes before final Review
- **WHEN** final verification passes with non-empty evidence artifacts
- **THEN** canonical status persists that PASS while final Review remains pending
- **AND** completion is still forbidden

#### Scenario: Complete without evidence
- **WHEN** lifecycle claims `complete` without attempt Report, batch Review, final
  verification, and final Review hashed artifact references
- **THEN** both validators reject the contract

#### Scenario: Stale or mislabeled evidence
- **WHEN** an artifact manifest has the wrong role, result, batch, attempt, or
  source revision for the claimed state
- **THEN** runtime validation rejects it
- **AND** Preflight/timeout evidence cannot substitute for batch Review PASS

#### Scenario: Complete without previous canonical state
- **WHEN** runtime validation receives a `complete` snapshot without the actual
  immediately preceding canonical status
- **THEN** it rejects the completion claim
- **AND** the project still keeps exactly one canonical marker block

#### Scenario: Blank blocker or unsafe artifact
- **WHEN** blocker details are blank or an artifact path is absolute or traverses
  outside the project
- **THEN** both validators reject the contract

### Requirement: Executable validation without optional YAML dependency
Project validators SHALL enforce schema-3 semantics with and without PyYAML,
reject Python booleans as positive integers, and keep single-repository tests
independent of an absent sibling clone.

#### Scenario: Standalone repository clone
- **GIVEN** the companion repository is not checked out beside the project
- **WHEN** the default unittest suite runs
- **THEN** local workflow tests still execute and pass
- **AND** only explicit cross-repository parity checks are skipped

### Requirement: OpenSpec completion reconciliation
An OpenSpec-backed task SHALL reconcile contract tasks and repository closeout
state before it is called closed.

#### Scenario: Repository implementation is complete
- **WHEN** all implementation, verification, and Review gates pass
- **THEN** `tasks.md` is reconciled with no unexplained open task
- **AND** required design/closeout documentation is updated
- **AND** the change is archived when repository completion semantics allow it
- **AND** strict validation passes after archive

#### Scenario: Deployment or release remains
- **WHEN** repository policy requires deployment or release before archival
- **THEN** the change remains active with an explicit owner and resume condition
- **AND** the workflow does not claim the contract is closed

### Requirement: Codex-primary auxiliary-agent collaboration

The workflow SHALL keep Codex as the single owner of routing, approval,
canonical state transitions, evidence acceptance, final verification, and final
completion while allowing Antigravity CLI and Grok CLI to serve as explicitly
assigned batch executors or independent reviewers.

External collaboration SHALL use schema version 4 to bind immutable
`executor_agent`, `independent_reviewer_agent`, and `decision_owner` identities;
Report and Review evidence SHALL bind the producing agent identity and role.
Canonical agent identities SHALL be exactly `codex`, `antigravity-cli`, or
`grok-cli`, and `decision_owner` SHALL be `codex`.

#### Scenario: Auxiliary implementation and Review are separated
- **GIVEN** both auxiliary CLIs are available for a standard or strict external batch
- **WHEN** one auxiliary agent implements the batch
- **THEN** the other assigned auxiliary agent SHALL independently review its diff, Report,
  contract, and evidence
- **AND** Codex audits both outputs before recording the authoritative transition

#### Scenario: Second auxiliary reviewer is unavailable
- **GIVEN** a standard or strict external batch has an auxiliary executor
- **WHEN** the other auxiliary CLI cannot Review
- **THEN** Codex performs the distinct Review pass
- **AND** the batch is `BLOCKED` if no distinct reviewer is available
- **AND** the existing standard or strict contract is not downgraded by waiver

#### Scenario: Same auxiliary agent attempts independent self-review
- **WHEN** executor and independent reviewer identities are equal, or evidence
  identity/role does not match the canonical assignment
- **THEN** validation rejects the Report or Review
- **AND** the batch does not advance

#### Scenario: Unknown identity or non-Codex decision owner
- **WHEN** a contract uses an identity outside the canonical enum or sets
  `decision_owner` to a value other than `codex`
- **THEN** validation rejects the contract
- **AND** no evidence or state transition is accepted

#### Scenario: Auxiliary reviewer claims completion
- **WHEN** an auxiliary reviewer reports `PASS` or claims the whole task complete
- **THEN** its result remains advisory evidence
- **AND** canonical state and final completion do not advance until Codex runs the
  required verification and records its own Review decision

#### Scenario: Review finding requires correction
- **WHEN** either auxiliary Review or Codex Review contains an actionable finding
- **THEN** the same scope returns to correction and verification
- **AND** a fresh Review is required before promotion or completion

#### Scenario: Active schema-3 contract exists during upgrade
- **WHEN** pre-deployment inventory finds an active schema-3 canonical status
- **THEN** schema-4 deployment is `BLOCKED` until the v3 workflow reaches its
  existing `complete` terminal state
- **AND** immutable v3 state is not rewritten or silently migrated
- **AND** an ignore list or chat-only abandonment cannot bypass the block

### Requirement: Post-optimization cross-CLI synchronization gate

The workflow SHALL, after either core workflow skill or its shared governance
rules change, synchronize every declared required runtime target and verify
source parity or discovery before claiming the global skill optimization
complete.

#### Scenario: All three runtimes are required
- **GIVEN** Codex, Antigravity CLI, and Grok CLI are declared required targets
- **WHEN** source validation and Review pass
- **THEN** both core skills are synchronized to all three runtime roots
- **AND** each target passes its compatible validator or discovery check
- **AND** final completion remains blocked until cross-runtime parity passes

#### Scenario: A target is unavailable
- **WHEN** a required runtime is missing, stale, undiscoverable, or fails validation
- **THEN** synchronization status is `BLOCKED`
- **AND** the workflow records the target, reason, owner, and resume condition
- **AND** it does not claim global skill optimization complete

#### Scenario: Target is explicitly not applicable
- **WHEN** an uninstalled, unsupported, or user-excluded target is declared
  `not-applicable` before synchronization
- **THEN** the decision includes owner, evidence, non-blank reason, and resume condition
- **AND** completion may proceed without that target only if all remaining
  required targets pass

#### Scenario: Failure is mislabeled not applicable
- **WHEN** an installed required target is stale, undiscoverable, or fails validation
- **THEN** the target remains `BLOCKED` rather than `not-applicable`
- **AND** global skill optimization cannot be called complete

#### Scenario: Repository-only documentation changes
- **WHEN** only README, changelog, tests, design history, or archived OpenSpec files change
- **THEN** no runtime synchronization is required
- **AND** the ordinary repository validation and Review rules still apply

### Requirement: Safe semantic global-rule alignment

The workflow SHALL keep one versioned, stable-ID governance invariant block
aligned across Codex, Antigravity CLI, and Grok CLI while preserving native
overlays and excluding sensitive or runtime-owned configuration from synchronization.

#### Scenario: Global rule files use different native formats
- **WHEN** the three CLIs use different filenames, precedence rules, or tool syntax
- **THEN** the shared governance invariants remain equivalent
- **AND** only a single begin/end marker block is replaced
- **AND** CLI-specific bytes outside that block remain unchanged

#### Scenario: Portable skill parity
- **WHEN** a portable skill file is synchronized
- **THEN** its relative path and SHA-256 match the canonical source manifest
- **AND** drift blocks the sync gate

#### Scenario: Sensitive category enters a sync manifest
- **WHEN** a proposed sync includes credentials, auth/token files, sessions,
  history, logs, caches, model settings, hooks, MCP secrets, or CLI binaries
- **THEN** validation rejects the manifest
- **AND** no sensitive category is copied to another runtime

#### Scenario: Unsafe source or destination path
- **WHEN** a manifest path is absolute, traverses its declared root, resolves
  through a symlink outside that root, or is not a regular file
- **THEN** validation rejects the synchronization before any target replacement
- **AND** diagnostics identify only the path/category without printing sensitive content

### Requirement: Capability-profile routing and bounded authority

The workflow SHALL route agent work using stable capability profiles rather
than concrete model names and SHALL enforce each profile's decision-authority
ceiling.

#### Scenario: Low executor encounters ambiguity
- **GIVEN** a `mechanical-low` executor receives a bounded task
- **WHEN** it encounters an unexpected failure, contract ambiguity, security
  field, forbidden file, or required design decision
- **THEN** it returns `BLOCKED` to the control plane
- **AND** it does not expand scope or choose an architecture

#### Scenario: Medium executor reaches an authority boundary
- **GIVEN** a `cohesive-medium` executor implements an approved slice
- **WHEN** the work would change OpenSpec scope, risk, acceptance, production
  authority, or completion state
- **THEN** it stops and escalates to `control-plane-high`
- **AND** the existing approval is not silently broadened

#### Scenario: Model metadata changes
- **WHEN** the concrete model or vendor used for a profile changes
- **THEN** authorization and evidence identity remain unchanged
- **AND** model metadata does not grant decision authority

### Requirement: Schema-5 product, instance, and role identity

New governed external contracts SHALL use schema 5 to separate agent product,
instance, role, capability profile, and control-plane ownership.

#### Scenario: Same product uses separate instances
- **GIVEN** two Codex instances serve as executor and independent reviewer
- **WHEN** schema-5 evidence is validated
- **THEN** their `agent_instance_id` values differ and match their assigned roles
- **AND** product equality does not permit executor self-review

#### Scenario: Instance or role impersonation
- **WHEN** Report or Review evidence has the wrong product, instance, role, or
  capability profile for the canonical assignment
- **THEN** validation rejects the evidence
- **AND** canonical state does not advance

#### Scenario: Active schema-4 contract exists
- **WHEN** deployment inventory finds an active schema-4 Handoff
- **THEN** schema-5 deployment is `BLOCKED` until that contract reaches its
  existing terminal state
- **AND** the v4 contract is not rewritten, ignored, or silently migrated

### Requirement: Layered authorization and Confirmation Leases

The workflow SHALL distinguish tool/platform, scope/workflow, and
business/production authorization and SHALL reuse only a valid scope-bound
Confirmation Lease.

#### Scenario: Platform command permission already exists
- **GIVEN** the platform already permits a safe test command
- **WHEN** the same approved artifact revision and scope reruns that command
- **THEN** the workflow does not request a duplicate chat confirmation
- **AND** it still records the verification result

#### Scenario: Platform permission meets production deletion
- **GIVEN** a shell prefix can execute a deletion command
- **WHEN** the task would delete production data or perform another human-only
  business action
- **THEN** the workflow requires explicit business/production authorization
- **AND** platform permission cannot satisfy that gate

#### Scenario: Confirmation Lease remains valid
- **WHEN** read-only checks, tests, diff review, or the same finding's
  fix/verify/Review loop stay within the bound revision, scope, and risk
- **THEN** the lease is reused without repeated confirmation

#### Scenario: Confirmation Lease is invalidated
- **WHEN** scope, acceptance, risk, production impact, credentials, external
  side effects, destructive Git, evidence assumptions, or the user's decision changes
- **THEN** the lease expires
- **AND** the affected higher-level authorization is requested again

### Requirement: Decision provenance and governed learning candidates

Material decisions SHALL retain an allowed provenance value, and corrections
SHALL enter a Learning Candidate Pipeline before any global Skill evolution.

#### Scenario: User accepts an AI recommendation
- **WHEN** the control plane proposes an option and the user approves it
- **THEN** provenance is `ai-proposed/user-approved`
- **AND** it is not recorded as `user-originated`

#### Scenario: One low-risk correction occurs
- **WHEN** the user corrects task-local wording once
- **THEN** the workflow creates or updates a task-local Candidate Card
- **AND** it does not automatically modify a global Skill

#### Scenario: Global candidate meets evidence threshold
- **WHEN** an invariant has two independent reproductions or one high-severity
  security, integrity, or false-PASS event
- **THEN** the workflow may create a Self-Evolution proposal candidate
- **AND** implementation still requires explicit OpenSpec approval, TDD,
  forward-tests, Review, and runtime synchronization

#### Scenario: Decision is deferred or revoked
- **WHEN** the user defers or revokes a prior decision
- **THEN** provenance and lease status record that transition
- **AND** stale approval cannot authorize later work

### Requirement: Governed manual external execution

State-changing standard or strict work SHALL use the governed Handoff lifecycle
even when a Brief is manually copied to another CLI.

#### Scenario: User manually copies a standard Brief
- **WHEN** an external agent receives the Brief through copy/paste rather than a
  dispatch tool
- **THEN** the Brief still binds canonical status, instance, profile, allowed
  files, abort conditions, evidence, and Report path
- **AND** the work is not downgraded to standalone mode

#### Scenario: Executor reports DONE or PASS
- **WHEN** an executor claims its batch or the whole task is complete
- **THEN** the claim remains non-authoritative Report evidence
- **AND** only the control plane may record promotion or final completion after Review

### Requirement: High independent Review and claim-to-mechanism evidence

For standard and strict work, the control plane SHALL perform or consume a
distinct High Review that examines actual implementation mechanisms rather than
only replaying executor commands.

#### Scenario: Executor tests pass but a copied field is lost
- **WHEN** the executor Report says PASS and focused tests pass
- **THEN** High Review traces the copy/transform/wiring chain
- **AND** it returns `FAIL` if the actual diff loses a required field

#### Scenario: Unit tests miss an adversarial input
- **WHEN** existing tests pass but an independent bounded-input probe reproduces
  a crash or contract violation
- **THEN** High Review blocks promotion
- **AND** correction, verification, and a fresh Review are required

#### Scenario: Metadata claim lacks a mechanism
- **WHEN** a Report claims concurrency, restart, recovery, or another behavior
  based only on labels or metadata
- **THEN** Review traces the claim to the runner or production mechanism
- **AND** unsupported claims cannot pass

### Requirement: Profile-weighted workflow remains proportionate

The workflow SHALL preserve compact, standard, and strict evidence weight while
enforcing the same approval and completion invariants.

#### Scenario: Compact mechanical task
- **WHEN** a low-risk deterministic task has no open architecture, security,
  persistence, production, or public-contract decision
- **THEN** it may remain inline with focused verification and concise Review
- **AND** no unnecessary canonical lease artifact is created

#### Scenario: Strict authorization-sensitive task
- **WHEN** work affects real credentials, authorization, production, migration,
  deletion, release, rollback, or recovery
- **THEN** strict real evidence and explicit human business gates apply
- **AND** mocks or platform permissions cannot replace them

### Requirement: Phase-aware Superpowers activation

The workflow SHALL select Superpowers sub-skills from the current task phase,
unresolved material decisions, and implementation risk. Generic creation or
modification wording alone SHALL NOT activate a sub-skill.

#### Scenario: Broad skill metadata also matches

- **GIVEN** a state-changing request matches both the change gate and broad Superpowers metadata
- **WHEN** skill routing begins
- **THEN** the shared managed governance rule routes the request through change-gate phase classification first
- **AND** only the Superpowers sub-skills selected by that classification apply to the current phase
- **AND** a selected sub-skill retains its complete rules and HARD-GATE behavior

#### Scenario: Fully specified proposal-only change

- **GIVEN** the user requests only OpenSpec proposal/spec/design/tasks artifacts
- **AND** repository facts plus the request define a testable contract without a material unresolved decision
- **WHEN** Gate 0 classifies the current phase
- **THEN** it records no implementation Superpowers sub-skill for proposal drafting
- **AND** the workflow creates and strictly validates the OpenSpec artifacts
- **AND** it stops for approval of the exact change-id before implementation

#### Scenario: Material proposal ambiguity remains

- **GIVEN** repository inspection cannot resolve a choice that changes scope, security, compatibility, data lifecycle, production authority, or testable acceptance
- **WHEN** the proposal contract would otherwise choose that behavior for the user
- **THEN** the workflow invokes `superpowers:brainstorming`
- **AND** preserves its HARD-GATE after invocation
- **AND** records the accepted decision in the single OpenSpec design/spec contract

#### Scenario: Bounded proposal assumption

- **GIVEN** a missing proposal detail is reversible at approval time
- **AND** it is visible in the proposal/design
- **AND** it does not decide security, compatibility, destructive migration, data lifecycle, production authority, or testable acceptance
- **WHEN** the proposal is drafted
- **THEN** the workflow MAY record that detail as an explicit bounded assumption
- **AND** SHALL NOT invoke brainstorming solely because that assumption exists

#### Scenario: Approved implementation begins

- **GIVEN** the user has approved the exact OpenSpec change-id and scoped contract
- **WHEN** the task transitions from proposal-only to implementation
- **THEN** Gate 0 is refreshed for the implementation phase
- **AND** multi-slice, strict, or external work retains its required planning, TDD, Preflight, Review, evidence, and verification discipline

### Requirement: Model-independent workflow weight

The workflow SHALL NOT use a concrete model, vendor, or version name as a reason
to bypass or require approval, evidence, Review, verification, or a Superpowers
sub-skill. Workflow weight SHALL follow task facts and stable capability/risk
profiles.

#### Scenario: Strong model is selected

- **WHEN** a stronger or newer model executes a proposal-only or implementation task
- **THEN** phase-aware routing applies without adding ceremony solely because the model changed
- **AND** the model identity does not remove any gate required by the task's contract or risk

### Requirement: Request-scoped brief OpenSpec Review

Standalone `codex-brief-antigravity-review` SHALL run only for the current
explicit wording or read-only Review request. It SHALL default to a concise,
findings-first OpenSpec artifact Review and SHALL NOT auto-chain after change
generation.

#### Scenario: Change generated without a Review request

- **GIVEN** OpenSpec artifacts have been produced and validated
- **WHEN** the current user request does not ask for standalone Review
- **THEN** the companion skill is not invoked automatically
- **AND** no duplicate Review ceremony or Handoff artifact is created

#### Scenario: Explicit standalone OpenSpec Review

- **WHEN** the user explicitly requests a read-only Review of proposal, spec, design, and tasks
- **THEN** the companion inspects proposal scope, spec scenarios, design decisions and risks, task traceability, and cross-artifact consistency
- **AND** reports scope/evidence, actionable findings, verdict, and next action in brief form
- **AND** omits governance narration that does not change the result or next action
- **AND** creates no Handoff and makes no implementation or final-completion decision

#### Scenario: Valid Handoff exists

- **GIVEN** a valid canonical Handoff Contract exists
- **WHEN** the request dispatches, audits, retries, recovers, or promotes that external batch
- **THEN** the complete handed-off lifecycle remains in force
- **AND** standalone brevity does not remove required artifacts, evidence, or state transitions

### Requirement: Conditional project context discovery

The workflow SHALL run a Domain Context Check before material-choice and
implementation routing whenever affected domain terms, actors, boundaries,
states, or lifecycle may change. It SHALL invoke `grill-with-docs` only when
repository inspection leaves domain language unclear or conflicting, and SHALL
use equivalent built-in Discovery First rules when that skill is unavailable.

#### Scenario: Clear localized task

- **GIVEN** repository context defines the affected language and boundaries
- **AND** the task introduces no new or conflicting domain concept
- **WHEN** Gate 0 classifies the request
- **THEN** the workflow records the scoped context result
- **AND** does not invoke `grill-with-docs` solely because files will change

#### Scenario: Domain language remains ambiguous

- **GIVEN** repository inspection cannot resolve a term, actor, boundary, state,
  or lifecycle meaning that affects the contract
- **WHEN** the workflow reaches the Domain Context Check
- **THEN** it invokes `grill-with-docs` when installed
- **AND** otherwise follows the complete portable Discovery First procedure
- **AND** stabilizes domain language before choosing material solution behavior

#### Scenario: Canonical context is intentionally ignored

- **GIVEN** a Git repository designates `CONTEXT.md` as shared project knowledge
- **WHEN** ignore rules exclude that file from the repository change surface
- **THEN** the context checkpoint reports a project-knowledge finding
- **AND** the ignored local copy cannot by itself satisfy durable promotion
- **AND** no staging, commit, or push occurs without separate user authorization

### Requirement: Governed project-local learning promotion

Corrections and Review findings SHALL enter a project learning audit. The
workflow SHALL require project-local promotion after two independent
correction/Review signals establish the same generalized invariant, or after one
high-severity security, integrity, data-loss, or false-PASS event establishes
it. A user request to archive and distill the session SHALL always run Project
Learning Closeout and SHALL promote every confirmed project-local key point.

#### Scenario: Repeated correction and independent Review find a foundation issue

- **GIVEN** one or more human corrections expose an agent's wrong assumption
- **AND** a distinct Review observation independently confirms the same
  foundational, easy-to-miss project invariant
- **WHEN** the Candidate Card classifies the evidence
- **THEN** the project-local promotion threshold is met
- **AND** final completion remains blocked until promotion and enforcement pass

#### Scenario: One high-severity event occurs

- **WHEN** a single correction or Review finding establishes a security,
  integrity, data-loss, or false-PASS invariant
- **THEN** project-local promotion is mandatory without waiting for recurrence
- **AND** the high-severity evidence does not automatically authorize a global
  Skill change

#### Scenario: One low-risk task-local correction occurs

- **WHEN** a single low-risk correction affects only the current task and does
  not establish a project-local invariant
- **THEN** it remains in the current Plan, Review, or session summary
- **AND** it does not force permanent project documentation or block completion

#### Scenario: User requests session archive and distillation

- **GIVEN** implementation and Review have produced correction history
- **WHEN** the user asks the current session to archive and distill its bug-fix
  experience
- **THEN** the workflow runs Project Learning Closeout before final completion
- **AND** promotes every confirmed project-local key point through the project's
  normal change path even if the automatic threshold was not reached
- **AND** a chat-only archive summary cannot substitute for repository promotion

### Requirement: Layered durable knowledge and executable enforcement

The workflow SHALL classify promoted knowledge by responsibility. It SHALL keep
domain semantics in `CONTEXT.md`, engineering or agent-operating invariants in
project guidance, qualifying hard-to-reverse trade-offs in ADRs, and
mechanically enforceable behavior in deterministic regression tests or
validators. Candidate evidence SHALL be summarized without persisting sensitive
conversation content.

#### Scenario: One lesson contains semantic and implementation knowledge

- **GIVEN** a corrected bug reveals both a project-specific semantic truth and
  an easy-to-miss implementation mechanism
- **WHEN** the lesson is promoted
- **THEN** `CONTEXT.md` receives only the term, meaning, relationship, or resolved
  ambiguity
- **AND** engineering guidance receives the generalized implementation invariant
- **AND** neither artifact duplicates the full incident chronology

#### Scenario: The invariant is mechanically enforceable

- **WHEN** a prior wrong assumption can be represented by a deterministic input,
  state transition, schema, or validator condition
- **THEN** promotion includes a regression test or validator that rejects it
- **AND** prose-only documentation cannot satisfy the completion gate

#### Scenario: Mechanical enforcement is impossible

- **WHEN** the Candidate Card demonstrates that deterministic enforcement is not
  practical
- **THEN** it records a non-empty reason and an explicit adversarial Review
  scenario
- **AND** the promotion still requires focused verification and Review PASS

### Requirement: Learning-aware completion and archive order

The workflow SHALL complete required Project Learning Closeout before fresh
final verification, final Review, OpenSpec task reconciliation/archive, and the
session archive summary. Learning artifacts added during closeout SHALL enter
the changed-file inventory and ordinary verification/Review loop.

#### Scenario: Required learning remains only in conversation

- **GIVEN** a mandatory or explicitly requested project-local promotion exists
- **WHEN** the generalized invariant remains only in chat, Report, or Review
  output
- **THEN** final completion is `BLOCKED`
- **AND** the workflow does not reconcile/archive the change as complete

#### Scenario: Learning closeout adds project artifacts

- **WHEN** Project Learning Closeout updates context, engineering guidance,
  Candidate Cards, tests, or validators
- **THEN** focused verification and Review cover those changes
- **AND** fresh final verification and final Review occur after that PASS
- **AND** the final session summary references the durable result rather than
  becoming its only storage location

#### Scenario: External reviewer identifies the candidate

- **WHEN** an external reviewer reports a potential project-local invariant
- **THEN** its finding remains an evidence input
- **AND** the Codex control plane classifies, promotes, and verifies the candidate
- **AND** the reviewer cannot self-authorize promotion or completion

### Requirement: Unambiguous branch-completion worktree policy

The workflow SHALL define one consistent worktree outcome for every
`finishing-a-development-branch` option. Option 2 SHALL preserve the feature
worktree after push/PR creation, and automatic worktree cleanup SHALL apply only
to Options 1 and 4. These rules SHALL NOT grant Git, publication, deletion, or
cleanup authority that the user has not explicitly provided.

#### Scenario: Option 2 creates a pull request

- **GIVEN** tests pass and the user explicitly selects and authorizes Option 2
- **WHEN** the branch is pushed and a pull request is created
- **THEN** the feature worktree is preserved
- **AND** no branch or worktree cleanup runs automatically

#### Scenario: Contradictory cleanup guidance returns

- **WHEN** any active Option 2 instruction says to clean up its worktree while
  another active instruction says to preserve it
- **THEN** deterministic validation or regression testing fails
- **AND** the workflow cannot claim the Superpowers contract synchronized

#### Scenario: Worktree cleanup lacks authority

- **WHEN** a plan or branch-finishing route includes worktree removal without
  the required selected option and user authority
- **THEN** Preflight is `BLOCKED`
- **AND** platform permission or skill text does not authorize the removal

### Requirement: Canonical result-oriented Completion Contract

The Router SHALL own one canonical whole-task Completion Contract. It SHALL
define the successful terminal result, fresh evidence, final Review, correction,
Project Learning, OpenSpec reconciliation/archive, runtime synchronization,
Git/publication, stop, and residual-risk obligations. Other workflow artifacts
MAY retain route-specific batch evidence and concise safety reminders, but SHALL
reference rather than independently redefine the normative whole-task checklist.

#### Scenario: Whole-task completion is evaluated

- **WHEN** the control plane decides whether the task is complete
- **THEN** it evaluates the canonical Completion Contract
- **AND** requires fresh final evidence, final Review PASS, no unresolved
  actionable finding, required learning promotion, OpenSpec reconciliation, and
  required runtime synchronization

#### Scenario: External batch Review passes

- **WHEN** the final external batch receives Review PASS
- **THEN** the Companion returns `awaiting-final-verification`
- **AND** batch PASS does not satisfy the Router-owned Completion Contract

#### Scenario: A secondary artifact diverges

- **WHEN** a secondary workflow artifact defines a conflicting whole-task
  completion condition or loses its canonical pointer
- **THEN** deterministic validation fails
- **AND** neither definition may be used to claim completion

#### Scenario: Entry discovery remains available

- **WHEN** a fresh session selects the Router for a completion decision
- **THEN** Router metadata/body identifies its final-completion ownership and
  the canonical Completion Contract
- **AND** moving detailed obligations to a reference does not hide the trigger

### Requirement: Evidence-gated Companion route isolation

The Companion SHALL expose mutually exclusive standalone and valid-Handoff
routes through a thin entry contract. Complete Handoff lifecycle instructions
SHALL be required only for the Handoff route. The workflow SHALL choose a
thin-reference or split-Skill structure from observed supported-runtime loading
evidence without changing authority, state, evidence, or completion semantics.

#### Scenario: Standalone wording or read-only Review

- **GIVEN** the user requests only standalone wording or ordinary read-only Review
- **AND** no valid Handoff route is active
- **WHEN** the Companion is selected
- **THEN** it applies the standalone result contract
- **AND** does not require Handoff state transitions, manifests, hashes, or batch
  promotion procedure

#### Scenario: Valid Handoff route is selected

- **GIVEN** a valid canonical Handoff Contract exists
- **WHEN** dispatch, audit, retry, recovery, or batch promotion is requested
- **THEN** the complete Handoff Governor contract is loaded and enforced
- **AND** route isolation does not omit any identity, evidence, transition,
  Review, or final-return requirement

#### Scenario: Runtime supports lazy reference loading

- **WHEN** reproducible runtime evidence proves inactive Companion references are
  not loaded
- **THEN** one thin Skill plus route-specific references MAY be used
- **AND** parity tests cover both routes

#### Scenario: Runtime injects the whole activated body

- **WHEN** reproducible runtime evidence proves the inactive Handoff body cannot
  be isolated through references
- **THEN** the implementation MAY use two mutually exclusive Skill entrypoints
- **AND** Router ownership and route selection remain deterministic

#### Scenario: Runtime loading is unobservable

- **WHEN** a required runtime exposes no reproducible Skill/reference loading evidence
- **THEN** its result is `UNKNOWN`
- **AND** file size alone does not authorize a split or a token-savings claim

### Requirement: Measured prompt-load and prompt-collision evidence

Prompt-load optimization SHALL distinguish observed runtime loads, exact-text
tokenizer measurements, and static file-size estimates. Prompt-collision
forward-tests SHALL verify observable routing, Git authority, and selected
Superpowers HARD-GATE behavior without asserting hidden reasoning.

#### Scenario: Token reduction is claimed

- **WHEN** implementation claims a prompt-token reduction
- **THEN** evidence identifies the exact loaded text or runtime trace, input
  hashes, tokenizer/encoding when used, scenario, and uncertainty
- **AND** byte or word counts alone are labelled estimates rather than token facts

#### Scenario: Proposal-only wording matches broad metadata

- **GIVEN** a fully specified proposal-only request also matches broad
  Superpowers metadata
- **WHEN** an isolated routing forward-test runs
- **THEN** Gate 0 selects no implementation sub-skill for proposal drafting
- **AND** the test does not infer that unrelated sub-skills loaded from metadata
  matching alone

#### Scenario: Material decision requires brainstorming

- **GIVEN** repository facts leave a material scope, security, compatibility,
  data-lifecycle, production-authority, or acceptance choice unresolved
- **WHEN** the routing forward-test runs
- **THEN** brainstorming is selected
- **AND** its complete HARD-GATE remains observable in the resulting behavior

#### Scenario: Plan contains unauthorized Git mutation

- **GIVEN** the current user has not authorized Git mutation
- **WHEN** a plan contains `git add`, commit, push, reset, clean, branch deletion,
  or worktree removal
- **THEN** Preflight removes or blocks the step before implementation
- **AND** a paired authorized scenario is not falsely rejected solely because
  the command text exists

#### Scenario: Prompt-load evidence is unavailable

- **WHEN** no supported mechanism can observe the loaded Skill/reference content
- **THEN** the workflow records the limitation and residual risk
- **AND** it does not report a measured optimization PASS

### Requirement: Governed Caveman Lite output profile

The Router SHALL provide an opt-in `governed-caveman-lite` presentation profile
that can be activated with the canonical conversational phrase
`OpenSpec 精简模式`. The profile SHALL use concise professional full sentences,
SHALL remain active only for the current conversation until disabled with
`OpenSpec 正常模式`, and SHALL work without a separately installed Caveman
skill.

The profile SHALL NOT alter request routing, OpenSpec approval, Superpowers
selection, evidence profiles, Handoff state, Review, verification, completion,
Git authority, or publication authority. Protected governance artifacts and
safety-critical text SHALL remain structurally complete.

#### Scenario: User enables the profile with the task

- **WHEN** the user sends `OpenSpec 精简模式：<任务>`
- **THEN** the Router handles the task under its normal governance route
- **AND** ordinary chat uses concise professional full sentences
- **AND** no separate Caveman skill is required

#### Scenario: User enables the profile before the task

- **WHEN** the user sends `OpenSpec 精简模式` before a later task
- **THEN** the profile applies to later ordinary responses in the same conversation
- **AND** the mode creates no workflow state or evidence artifact

#### Scenario: User disables the profile

- **GIVEN** the profile is active
- **WHEN** the user sends `OpenSpec 正常模式`
- **THEN** later responses return to normal output style
- **AND** this latest explicit user instruction controls Router prose even if a
  Caveman-style instruction was previously active
- **AND** routing, approval, evidence, and task state remain unchanged

#### Scenario: Conversation ends

- **GIVEN** the profile is active
- **WHEN** a new conversation begins
- **THEN** the Router starts in normal output mode
- **AND** no account, repository, or runtime preference is inferred

#### Scenario: Protected governance content is produced

- **GIVEN** the profile is active
- **WHEN** the Router produces Gate 0, a mandatory governance-step or approval
  field, an OpenSpec artifact, implementation plan, Handoff contract, evidence
  artifact, state transition, final verification, final Review, critical
  command, rollback instruction, security warning, or destructive confirmation
- **THEN** every required field and ordering constraint remains present
- **AND** governance clarity and safety override output compression

#### Scenario: Default Router request omits the phrase

- **WHEN** a normal Router request does not explicitly enable the profile
- **THEN** the new profile is not forced on
- **AND** existing output behavior remains compatible

### Requirement: Codex-specific Superpowers meta-entry boundary

The Codex installation SHALL make `superpowers:using-superpowers` unavailable
for implicit invocation through product-specific metadata while preserving
user-explicit invocation. This host-specific policy SHALL NOT alter the shared
`using-superpowers/SKILL.md` contract or another host's bootstrap behavior.

#### Scenario: Ordinary fresh-session question

- **GIVEN** a fresh Codex session receives an ordinary question that requires no
  state-changing governance or matching domain Skill
- **WHEN** Codex performs native Skill discovery
- **THEN** product metadata and its fixture show
  `superpowers:using-superpowers` is unavailable for implicit invocation
- **AND** the question is answered without exhibiting the Router or Superpowers
  meta-workflow
- **AND** actual prompt-load absence is claimed only from supported path/hash
  evidence; otherwise load state is `UNKNOWN`

#### Scenario: User explicitly requests the meta-entry

- **WHEN** the user explicitly invokes `$superpowers:using-superpowers`
- **THEN** Codex loads the complete `using-superpowers` Skill
- **AND** explicit-only metadata does not make the Skill unavailable

#### Scenario: Codex-only metadata is applied

- **GIVEN** the source-managed Superpowers checkout is also the symlink-discovered
  Codex runtime target
- **WHEN** the invocation boundary is implemented or synchronized
- **THEN** only `skills/using-superpowers/agents/openai.yaml`,
  `docs/README.codex.md`, and
  `tests/codex/using-superpowers-invocation-policy.test.js` change for this
  boundary
- **AND** the shared `using-superpowers/SKILL.md` bytes and non-Codex
  Superpowers discovery or invocation metadata remain unchanged

#### Scenario: Superpowers delta is prepared before live application

- **WHEN** RED/GREEN implementation and source validation run
- **THEN** they use a non-discoverable structured copy of the exact live
  Superpowers pre-state without Git mutation
- **AND** the reviewed three-path delta is applied once to the combined
  source/runtime target only after live path/hash preconditions and backups pass

#### Scenario: Invocation-boundary rollback is required

- **WHEN** source validation, fresh-session behavior, or runtime verification
  fails after the Codex metadata is applied
- **THEN** the exact pre-change source and runtime metadata state is restored
- **AND** no fetch, merge, reset, clean, commit, push, or unrelated checkout
  mutation is used as the rollback mechanism

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

### Requirement: Scope-bound cross-CLI synchronization plans

The workflow SHALL support an explicitly selected cross-runtime mutation set
without replacing unselected portable files or an unselected managed global
rule. A scoped plan SHALL bind the normalized selection, canonical source
hashes, destination prestates, and complete manifest verification closure into
the reviewed plan hash and durable target receipts. For schema-v2, the managed
rule destination SHALL be derived from the target-specific canonical runtime
layout of its absolute `skills_root`: the parent runtime root for Codex, Pi, and
Grok, and the grandparent `.gemini` root for Antigravity. A serialized
managed-rule destination SHALL NOT redefine that binding.

Scoped synchronization SHALL reuse the existing ordered target, secure backup,
atomic apply, restore, recovery, content verification, discovery, and commit
mechanisms. It SHALL NOT infer scope from Git state, create a parallel
transaction lifecycle, or treat a scoped selection as permission to ignore
unselected parity, unavailable targets, sensitive content, active legacy
contracts, or final Review.

#### Scenario: Exact portable-file scope is selected

- **GIVEN** an approved change names an exact set of manifest-declared portable
  files for all required schema-6 runtimes
- **WHEN** a scoped sync plan is generated
- **THEN** only those files appear as mutation operations for each applicable
  target
- **AND** every unselected file appears only in the read-only verification
  closure
- **AND** the managed global rule is not a mutation operation unless explicitly
  selected

#### Scenario: Unselected runtime content is stale

- **WHEN** an unselected manifest file or managed global rule does not match its
  canonical source or reviewed prestate
- **THEN** scoped planning or apply is `BLOCKED`
- **AND** the stale object is not silently ignored, replaced, or relabeled
  `not-applicable`

#### Scenario: Scoped plan is expanded after Review

- **WHEN** a file is moved from the assertion closure into operations, a path is
  added, or managed-rule selection changes after Sync-plan Review
- **THEN** plan validation or receipt hash binding rejects the transaction
- **AND** runtime apply does not begin under the prior Review

#### Scenario: Scoped target fails

- **GIVEN** one target has applied an exact scoped operation set under a durable
  receipt
- **WHEN** content, discovery, or commit verification fails
- **THEN** rollback restores only objects selected and mutated for that target
- **AND** later targets remain blocked until the existing recovery contract is
  satisfied

#### Scenario: Scoped verification completes

- **WHEN** all selected operations have applied to every required target
- **THEN** content parity and discovery verify the complete selected-plus-
  asserted portable closure and managed rule
- **AND** final completion remains blocked until every target and independent
  final Review pass

#### Scenario: Legacy full-manifest plan is requested

- **WHEN** no scoped selector is supplied
- **THEN** the existing full-manifest plan and durable transaction behavior
  remain available and validation-compatible
- **AND** scoped mode does not weaken existing full-plan safety or recovery
  tests

#### Scenario: Invalid scoped selection is supplied

- **WHEN** selection is empty, duplicate, unknown, unsafe, sensitive,
  target-incomplete, or incompatible with the schema-6 target set
- **THEN** plan creation fails before an output plan or runtime backup exists
- **AND** diagnostics expose only safe path/category information

#### Scenario: Managed-rule destination is coherently retargeted

- **WHEN** a schema-v2 plan changes a target's managed-rule destination and
  matching pre-state to another regular file
- **THEN** plan generation or loading rejects the plan against the canonical
  target runtime binding
- **AND** candidate, backup, and apply do not touch the replacement file

