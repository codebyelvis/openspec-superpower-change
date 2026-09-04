# Skill distribution requirements

## ADDED Requirements

### Requirement: Preserve one canonical skill source

The distribution implementation MUST keep the repository root `SKILL.md` and
its existing portable references as the only authoring source for the skill.
Generated community/client artifacts MUST be derived from that source or from
the existing portable manifest and MUST NOT introduce competing workflow
instructions.

#### Scenario: Standard skill discovery sees one root skill

- **WHEN** a standards-based skill scanner examines the repository root
- **THEN** it finds the existing root `SKILL.md` as the canonical skill
- **AND** it does not need to discover a second root-level copy created for a
  community adapter

#### Scenario: Generated adapter is regenerated

- **WHEN** the distribution builder runs
- **THEN** it projects the portable manifest into the Codex plugin adapter
- **AND** the validator can prove every generated file corresponds to the
  current canonical source

### Requirement: Expose a valid Pi/npm package

The repository MUST provide root package metadata that Pi can recognize and
npm can package without relying on implicit repository contents.

#### Scenario: Pi recognizes the package

- **WHEN** a client reads the root `package.json`
- **THEN** the package has a stable name and semantic version
- **AND** its keywords include `pi-package`
- **AND** its `pi.skills` entry points to the canonical root `SKILL.md`

#### Scenario: Package contents are bounded

- **WHEN** `npm pack --dry-run` is executed
- **THEN** the resulting file list contains the documented public skill,
  references, scripts, templates, documentation, changelog, and license
- **AND** it excludes tests, OpenSpec change records, local agent instructions,
  caches, generated Codex output, and unrelated repository material

### Requirement: Provide standards-based community discovery guidance

The public documentation MUST explain how to discover or install the skill
through skills.sh and SkillsMP using the public GitHub repository, without
claiming that either index certifies the skill or performing an automated
upload that the service does not support.

#### Scenario: User installs from skills.sh

- **WHEN** a user follows the documented skills.sh command
- **THEN** the command targets the public GitHub repository
- **AND** the documentation identifies source review and permission risk as
  part of the installation decision

#### Scenario: User finds the skill in SkillsMP

- **WHEN** a user searches SkillsMP for the public repository
- **THEN** the documentation explains that SkillsMP is an index of public
  `SKILL.md` sources
- **AND** the user is directed to the repository's installation instructions
  rather than a fabricated upload/API flow

### Requirement: Provide a valid skill-only Codex plugin artifact

The project MUST be able to generate and validate a Codex plugin adapter with
the required `.codex-plugin/plugin.json` manifest and a skill directory whose
content is traceable to the canonical portable manifest.

#### Scenario: Plugin manifest is structurally valid

- **WHEN** the generated adapter is inspected
- **THEN** `.codex-plugin/plugin.json` contains a stable name, version,
  description, license, non-empty author, required interface metadata, and
  `skills` path
- **AND** `interface.defaultPrompt` is an array containing one to three
  non-empty strings of at most 128 characters
- **AND** all manifest paths are relative and point inside the adapter

#### Scenario: Plugin source parity is checked

- **WHEN** the validator compares the generated plugin with the portable
  manifest
- **THEN** every required source file exists with matching content
- **AND** unexpected skill files or symlinks cause validation failure

### Requirement: Keep publication and license boundaries explicit

The release documentation and validation MUST distinguish local release
readiness from external publication. The project MUST NOT silently publish to
an external registry or community service, and MUST NOT advertise a ClawHub
publication path under the repository's MIT license.

#### Scenario: Maintainer performs a release dry run

- **WHEN** the documented release checks run
- **THEN** they inspect package and plugin artifacts locally
- **AND** they do not call `npm publish`, a plugin submission endpoint, or a
  community upload endpoint

#### Scenario: License-sensitive community is considered

- **WHEN** a maintainer reviews the supported community list
- **THEN** ClawHub is marked out of scope because its current publication
  contract requires MIT-0
- **AND** no documentation implies that the MIT-licensed skill is published
  there
