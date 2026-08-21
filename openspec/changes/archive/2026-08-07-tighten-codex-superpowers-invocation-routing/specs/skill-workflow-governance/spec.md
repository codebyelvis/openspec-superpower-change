## ADDED Requirements

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

- **WHEN** the user requests ordinary diff, Report, or evidence Review without
  fixes or final-completion authority
- **THEN** the Companion standalone route applies
- **AND** architecture, OpenSpec, authorization, and whole-task completion
  Review remain Router Review-only work

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
