## ADDED Requirements

### Requirement: Plan-anchored cohesive execution and lazy state

For OpenSpec-backed work, when the approved OpenSpec `design.md` and `tasks.md`
already define the Four Hard Anchors—(1) allowed and forbidden file scope,
(2) target interfaces and `path:line` code facts, (3) coarse-grained cohesive
batches, and (4) exact regression test commands and assertions—those approved
OpenSpec artifacts SHALL serve directly as the executable Plan without requiring
a duplicate Superpowers `implementation-plan.md` or standalone local Preflight
JSON artifacts before local execution. A separate Plan is required only when
the approved OpenSpec artifacts omit those executable anchors or when
multi-slice/external coordination requires a distinct execution breakdown.

Execution SHALL default to coarse-grained cohesive business batches rather than
per-file or micro-step gates. Inside an approved batch, the executor MAY iterate
freely on implementation and tests without standalone intermediate JSON files
(`red-green.json`, `native-green.json`), recording a concise inline RED-to-GREEN
proof (failing test name, non-zero exit code, and one-line failure summary
before the fix, followed by passing command and exit code `0`) in the final
verification or Review report.

Localized bugfixes restoring intended behavior MAY use Direct Change without a
pre-existing approved spec path in Gate 0 when three conditions hold:
(1) a failing-then-passing regression test proves the restoration,
(2) no external API, schema, permission, compatibility, or lifecycle contract
changes, and (3) the change is bounded by the localized diff.

For local `compact` and `standard` work, `docs/agent-collab/<change-id>/status.md`
and `## Resume Context` SHALL be created lazily only before an intentional stop,
context compaction, or cross-window/external handoff. Local `strict` and
`self-evolution` work SHALL create `status.md` at approval and refresh it at
review and completion boundaries rather than every micro-step. In all Session
Resume records, `verified_revision.inputs` SHALL include only verified source,
rule, configuration, and test files, and SHALL exclude `CHANGELOG.md`, task
ledgers, and historical Review or Evidence reports so closeout updates do not
invalidate the verified source fingerprint.

`references/approved-implementation-workflow.md` SHALL partition its everyday
execution trunk from its cold-path recovery sections (`Project Session Resume`,
blocked-context amendment, and control-plane rebind/return) via an explicit
cold-path marker so routine single-window execution does not preload recovery
rules.

#### Scenario: Four-anchor OpenSpec serves directly as executable Plan

- **GIVEN** an approved OpenSpec change defines allowed/forbidden file scope,
  `path:line` code facts, cohesive batches, and exact regression commands in
  `design.md` and `tasks.md`
- **WHEN** local implementation begins on a clean baseline
- **THEN** the workflow uses the approved OpenSpec artifacts directly as the Plan
- **AND** does not require a duplicate Superpowers `implementation-plan.md` or
  standalone local Preflight JSON files

#### Scenario: Cohesive batch uses inline RED-to-GREEN proof without intermediate JSON bloat

- **GIVEN** an approved cohesive implementation batch
- **WHEN** the executor runs TDD and verification commands
- **THEN** the executor iterates freely within the approved file scope without
  writing standalone `red-green.json` or `native-green.json` files
- **AND** records the failing test name, non-zero exit code, one-line failure
  summary, and post-fix passing exit code `0` inline in the verification/review
  evidence

#### Scenario: Localized bugfix uses three-condition Direct Change

- **GIVEN** a localized bugfix restores intended behavior without a pre-existing
  spec file path
- **WHEN** it is backed by a failing-then-passing regression test, changes no
  external API/schema/permission/lifecycle contract, and stays within the
  localized diff scope
- **THEN** it proceeds via Direct Change without requiring OpenSpec proposal
  artifacts

#### Scenario: Lazy status creation and clean verified_revision inputs

- **GIVEN** a local `compact` or `standard` change completes within one session
- **WHEN** no intentional pause, compaction, or cross-window handoff occurs
- **THEN** no `docs/agent-collab/<change-id>/status.md` checkpoint is required
- **AND** when `status.md` is used, `verified_revision.inputs` excludes
  `CHANGELOG.md`, task ledgers, and Review/Evidence reports so closeout updates
  do not trigger self-hash invalidation
