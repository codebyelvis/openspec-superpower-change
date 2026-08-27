## ADDED Requirements

### Requirement: Scope-bound cross-CLI synchronization plans

The workflow SHALL support an explicitly selected cross-runtime mutation set
without replacing unselected portable files or an unselected managed global
rule. A scoped plan SHALL bind the normalized selection, canonical source
hashes, destination prestates, and complete manifest verification closure into
the reviewed plan hash and durable target receipts.

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
