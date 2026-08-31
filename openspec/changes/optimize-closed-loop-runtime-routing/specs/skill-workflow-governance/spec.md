## MODIFIED Requirements

### Requirement: Capability-profile routing and bounded authority

The workflow SHALL route authority through the existing capability profiles,
not concrete model names. It MAY provide non-authoritative model/reasoning
advice, but that advice SHALL NOT alter `agent_product`, control-plane,
executor, reviewer, capability/evidence profile, approval, authority, or PASS.
`Luna Max` SHALL NOT be written into schema-6 `agent_product`.

#### Scenario: Default runtime recommendation

- **WHEN** runtime advice is useful
- **THEN** ordinary OpenSpec/writing-plans/read-only Review recommends Codex
  high; complex security/Preflight/final gate Review recommends Codex xhigh;
  closed-scope cohesive implementation recommends Luna Max; and a small
  mechanical edit may use the current sufficient lower-cost mode
- **AND** the recommendation grants no authority

#### Scenario: Actual switch

- **WHEN** an approved task genuinely requires a different model or reasoning
  environment
- **THEN** the user receives one notice naming target Session, model, reasoning
  strength, reason, copyable prompt, and return model/reasoning target
- **AND** no switch produces no notice

### Requirement: Authorized execution continuity

During authorized implementation, the workflow SHALL continue the next safe
approved task while no blocker or new human decision exists. “闭环推进”,
“继续闭环”, “按推荐方案推进”, and “完成后统一 Review” SHALL mean bounded
continuation only; they SHALL NOT expand scope or grant database, production,
external-effect, release, deployment, destructive, or Git authority.

After option A or an obvious implementation-detail recommendation is accepted,
the workflow SHALL NOT confirm A or ask whether to start the next safe step
again. Only a choice that materially changes business/product semantics,
architecture, security, compatibility, acceptance, risk, or production
authority SHALL enter brainstorming/grill and ask one focused question. A
closed solution SHALL NOT re-enter grill merely because the task is long.

Status reporting SHALL be non-confirmation progress and execution SHALL continue
after the report when safe work remains. After compaction, a new window, an
agent/model switch, or “继续”, the workflow SHALL recover from canonical
Plan/Status/Handoff rather than re-asking completed or approved work.

#### Scenario: Accepted recommendation continues

- **GIVEN** option A is approved and remaining work is safe and in scope
- **WHEN** the user requests closed-loop progress
- **THEN** the workflow performs the next task without another confirmation

#### Scenario: Material choice asks once

- **WHEN** a choice materially changes business, architecture, security,
  compatibility, acceptance, risk, or production authority
- **THEN** the workflow asks one focused question
- **AND** after selection it does not reopen the same choice unless scope or
  risk changes

#### Scenario: Status report is progress

- **GIVEN** safe approved work remains
- **WHEN** the workflow reports status
- **THEN** the report is not phrased as a confirmation request
- **AND** execution continues to the next safe task

#### Scenario: Forbidden boundary

- **WHEN** the next step requires scope expansion, database/production writes,
  external sending, release/deployment, destructive action, or Git authority
- **THEN** the workflow stops and requests the applicable new authorization

#### Scenario: Canonical resume

- **WHEN** context is compacted, a window/model/agent changes, or the user says
  “继续”
- **THEN** the workflow resumes from canonical state without re-asking approved
  or completed work

### Requirement: Profile-weighted workflow remains proportionate

The workflow SHALL use the smallest design, artifact set, and verification
effort adequate for the approved behavior and actual risk. It SHALL reuse
existing rules, templates, validators, fixtures, and test locations before
creating a new abstraction. It SHALL NOT add a state machine, registry, schema
family, runner, fixture framework, task ledger, or dispatch framework when
direct edits and existing verification are sufficient.

TDD and verification SHALL remain relevant to the current task. Focused
RED/GREEN SHALL cover changed acceptance scenarios, changed contracts, and
credible regressions. The workflow SHALL NOT create or run unrelated test
matrices for ceremony. A broader suite SHALL run only when an existing gate or
demonstrated blast radius makes it relevant. Proportionality SHALL NOT skip a
relevant safety, compatibility, validator, Review, or completion gate.

#### Scenario: Simple change uses existing mechanisms

- **WHEN** a workflow correction can be expressed in existing files and proved
  by direct assertions
- **THEN** the workflow reuses those files and assertions
- **AND** it does not create a new schema, registry, runner, or ledger

#### Scenario: Focused TDD

- **WHEN** a task changes a bounded behavior
- **THEN** RED/GREEN exercises that behavior and credible regressions
- **AND** unrelated test suites are not added or run without a gate or
  demonstrated blast-radius reason

#### Scenario: Shared-file blast radius

- **WHEN** a changed global Skill/template is consumed by an existing project
  validator or workflow test file
- **THEN** that validator or test file is relevant final verification
- **AND** unrelated subsystem suites remain out of scope

#### Scenario: Support machinery exceeds the change

- **WHEN** proposed test or design infrastructure is more complex than the
  behavior it proves
- **THEN** the workflow stops and simplifies to the smallest adequate mechanism

## ADDED Requirements

### Requirement: Optional runtime environment advice is non-authoritative

Router and Companion guidance SHALL support one optional human-readable
`运行环境建议` block when an actual model/reasoning switch is needed, containing:

- target Session;
- recommended model;
- reasoning strength;
- switch reason;
- copyable task prompt; and
- return model/reasoning target.

The block SHALL be omitted when no actual switch occurs. Downstream
Brief/dispatch surfaces SHALL copy an existing block verbatim rather than
regenerate it. The block SHALL remain outside the machine-readable schema-6
Handoff marker and canonical `status.md`, and SHALL NOT participate in schema
validation, canonical SHA, lifecycle, permission, authority, or PASS.

#### Scenario: Old schema-6 Handoff

- **GIVEN** a valid schema-6 Handoff contains no runtime-advice block
- **WHEN** it is validated or resumed
- **THEN** it remains valid

#### Scenario: Runtime advice stays non-canonical

- **WHEN** an actual switch notice is included in human-readable guidance
- **THEN** it appears outside the Handoff marker and canonical status
- **AND** no schema field, state, profile, authority, or hash contract changes
