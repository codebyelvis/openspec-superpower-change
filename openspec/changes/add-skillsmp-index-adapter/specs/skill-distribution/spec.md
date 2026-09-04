# Skill distribution requirements

## ADDED Requirements

### Requirement: Provide a generated GitHub catalog index adapter

The distribution implementation MUST provide
`skills/openspec-superpower-change/SKILL.md` as a generated regular-file
adapter for catalogs that require nested skill directories. The repository
root `SKILL.md` MUST remain the only authoring source and the adapter MUST be
byte-identical to it.

#### Scenario: Distribution generation creates the index adapter

- **WHEN** the distribution builder runs against a valid repository
- **THEN** it writes a regular file at the exact nested adapter path
- **AND** the adapter bytes equal the canonical root `SKILL.md`

#### Scenario: Adapter drift is rejected

- **WHEN** the adapter is missing, stale, linked, non-regular, or appears at an
  unexpected path
- **THEN** distribution validation fails closed
- **AND** it identifies the adapter boundary that is invalid

#### Scenario: Adapter generation encounters unsafe existing state

- **WHEN** `skills/`, the skill-name directory, or its target entry is linked
  or special, or the reserved adapter directory contains an unexpected entry
- **THEN** generation fails before writing through that path
- **AND** no external target or unrelated repository entry is modified

#### Scenario: Adapter replacement fails after staging

- **WHEN** installation fails after the prior generated adapter is captured
- **THEN** the builder restores and verifies the prior adapter state
- **AND** an unprovable restoration leaves visible recovery evidence and fails
  closed instead of deleting that evidence

#### Scenario: Parent binding changes at the mutation boundary

- **WHEN** a repository or `skills/` pathname is rebound after validation but
  before install, restore, or cleanup
- **THEN** all mutations remain relative to the retained no-follow directory
  descriptors
- **AND** no external or concurrently substituted object is moved, overwritten,
  or deleted

#### Scenario: Source or transaction state changes during generation

- **WHEN** the canonical source is replaced or modified in place, an adapter
  target is hard-linked, or unknown stage/recovery residue appears during the
  transaction
- **THEN** generation does not report success
- **AND** the prior generated state is compensated or retained as visible
  recovery evidence
- **AND** every check that can reject the transaction completes before verified
  recovery evidence is deleted as the commit point

#### Scenario: Required no-follow primitives are unavailable

- **WHEN** the host lacks the required no-follow and descriptor-relative
  filesystem primitives, including descriptor listing or no-follow stat support
- **THEN** generation fails before mutation with a deterministic portability
  diagnostic

#### Scenario: Recovery evidence is reported after pathname rebinding

- **WHEN** compensation leaves recovery evidence and the live `skills/`
  pathname no longer names the retained directory
- **THEN** the diagnostic identifies the retained parent device/inode and
  recovery entry name
- **AND** it marks any lexical live path as untrusted rather than presenting an
  unrelated pathname as authoritative
- **AND** a cleanup failure does not replace the primary transaction error

### Requirement: Preserve existing package and discovery boundaries

The compatibility adapter MUST NOT change the Pi/npm entry point or npm package
contents, and supported local Agent Skills discovery MUST expose one logical
`openspec-superpower-change` skill.

#### Scenario: npm package remains root-only

- **WHEN** `npm pack --dry-run --json` inspects the package
- **THEN** `SKILL.md` is present as the Pi/npm entry point
- **AND** no path under `skills/` is included

#### Scenario: Local discovery examines the repository

- **WHEN** the supported `skills` CLI lists skills from the repository
- **THEN** exactly one logical skill named `openspec-superpower-change` is
  reported

### Requirement: Describe asynchronous catalog indexing accurately

Public distribution documentation MUST distinguish the repository-side nested
adapter prerequisite from third-party crawl, audit, ranking, and refresh
latency. It MUST NOT claim that creating the adapter guarantees immediate
SkillsMP, skills.sh, or Pi gallery search visibility.

#### Scenario: Maintainer verifies source readiness

- **WHEN** the adapter and repository validators pass
- **THEN** documentation permits a claim that the repository-side catalog
  prerequisite is ready
- **AND** it keeps third-party index appearance as externally observed evidence
  rather than a source-code completion claim
