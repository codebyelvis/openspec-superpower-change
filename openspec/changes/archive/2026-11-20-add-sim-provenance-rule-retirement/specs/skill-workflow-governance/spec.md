## ADDED Requirements

### Requirement: Provenance-gated rule retirement with repository-anchored exclusions, production validation, and append-only SIM tombstones

`references/self-evolution-rule.md`, `references/skill-iteration-loop.md`,
`templates/learning-candidate-template.md`, and `scripts/validate_core_gates.py`
SHALL enforce a provenance-gated contract for retiring governed skill or
workflow prose rules without introducing a new iteration state file or moving
retirement memory into everyday hot paths.

Every proposed retirement of governed skill or workflow prose SHALL remain
classified as **Major Self-Evolution** requiring an approved OpenSpec change
(`已批准 <change-id>`), independent Implementation Review, four-target portable
sync verification when applicable, and independent Final Review, and SHALL
satisfy four mandatory conditions:

1. **Repository-anchored non-retirable exclusion**: `target_surface` SHALL use
   canonical `<project-relative-path>#<section-slug>` format (rejecting
   pathless aliases, traversal/absolute paths, or pure line anchors such as
   `#L171`). Protected governance files (`SKILL.md`,
   `references/shared-global-governance.md`, `references/completion-contract.md`,
   `references/step-evidence-gate.md`, `references/handoff-contract.md`,
   `references/confirmation-lease.md`, `references/agent-capability-routing.md`,
   `references/openspec-decision-rule.md`), locked governance sections
   (`references/self-evolution-rule.md#hard-prohibitions`,
   `references/self-evolution-rule.md#change-levels`,
   `references/self-evolution-rule.md#provenance-gated-rule-retirement`,
   `references/skill-iteration-loop.md#authorization`,
   `references/skill-iteration-loop.md#reading-budget-for-one-round`,
   `references/project-learning-closeout.md#triggers`,
   `references/project-learning-closeout.md#enforcement-and-review`), and any
   slug matching `non-negotiables`, `ccg-`, or `validator-locked` SHALL NEVER
   be eligible for retirement regardless of model capability gains. Static
   record validation enforces `target_surface` exclusions, while running
   `scripts/validate_core_gates.py` remains the final mechanical defense
   verifying no validator-locked phrase was deleted from any file.
2. **SIM provenance anchoring**: The retirement record SHALL cite a verifiable
   `origin_anchor` (BACKLOG SIM entry, Git commit, archived OpenSpec change, or
   CHANGELOG reference) explaining which prior model/runtime failure mode
   motivated the rule.
3. **Structured bidirectional retirement proof (`retirement_basis` and `retirement_evidence`)**:
   `retirement_evidence` SHALL be a dual-YAML compatible nested mapping:
   - When `retirement_basis` is `"mechanical-superseded"`: require at least 1
     entry specifying non-empty relative `validator_or_test` and `negative_case`
     proving higher-layer deterministic enforcement rejects the original failure
     mode.
   - When `retirement_basis` is `"cross-model-internalized"`: require at least 2
     entries each specifying single-value `runtime`, `model_family`, and
     `probe_ref` (rejecting multi-value delimiters). Using open-world
     deterministic normalization (mapping runtime aliases such as `agy` ->
     `antigravity-cli`, `grok` -> `grok-cli`, and stripping trailing model
     tier/version suffixes without a closed model allowlist), the evidence set
     SHALL contain at least 2 distinct normalized runtimes or at least 2
     distinct normalized model families.
4. **Append-only SIM tombstone and non-resurrection**: Approved retirements
   SHALL be recorded in `docs/iteration/BACKLOG.md` using
   `record_kind: sim-retirement` (unconditionally forbidding `status: promoted`
   regardless of `decision_owner`), a dual-YAML compatible `attempts` entry
   whose `observed` begins with `retired`, and an explicit `reopen_condition`.
   Future optimizers SHALL NOT silently reinstate a retired rule unless fresh
   failure evidence triggers `reopen_condition`, and retirement records SHALL
   remain non-gating optimizer memory outside everyday hot paths.

`scripts/validate_core_gates.py:main(...)` SHALL execute
`validate_sim_rule_retirement_guard` on every validated root and, whenever
`(root / "docs" / "iteration" / "BACKLOG.md").is_file()`, SHALL scan all fenced
YAML blocks with `record_kind == "sim-retirement"` or key `retirement_basis`
through `validate_sim_retirement_record` identically under both `PyYAML` and
the dependency-free `simple_yaml_load` fallback.

#### Scenario: Retiring a real protected file, locked section, or line-number anchor fails closed

- **WHEN** a retirement record sets `target_surface` to `SKILL.md#routing-boundary`, `SKILL.md#L171`, `references/completion-contract.md#evidence`, `references/skill-iteration-loop.md#authorization`, or a slug containing `ccg-` or `non-negotiables`
- **THEN** `validate_sim_retirement_record` SHALL reject the record fail-closed regardless of `retirement_evidence`

#### Scenario: Same-runtime alias or same-family tier variants cannot satisfy cross-model internalization

- **WHEN** a `"cross-model-internalized"` record cites `runtime: agy` + `model_family: gemini-4-carbon` in `evidence_1` and `runtime: antigravity-cli` + `model_family: gemini-4-argon` in `evidence_2` (or packs two models into one value like `gemini/claude`)
- **THEN** `validate_sim_retirement_record` SHALL reject the record fail-closed because normalized distinct runtimes and model families are both fewer than 2 (or multi-value syntax is disallowed)
- **AND** new model families such as `deepseek-v4` paired with `gemini-4-neon` SHALL pass without requiring a hardcoded model allowlist

#### Scenario: Production validation rejects a malformed or status-promoted retirement tombstone in BACKLOG.md

- **WHEN** `docs/iteration/BACKLOG.md` contains a fenced YAML block with `record_kind: sim-retirement` (or key `retirement_basis`) that sets `status: promoted` (even with `decision_owner: codex`) or lacks `origin_anchor`/`reopen_condition`
- **THEN** `scripts/validate_core_gates.py:main(...)` SHALL fail closed under both `PyYAML` and `simple_yaml_load`
- **AND** roots without `docs/iteration/BACKLOG.md` (such as generated plugin or runtime skill directories) SHALL continue to pass `validate_core_gates.py`

#### Scenario: Valid dual-YAML retirement tombstones pass and prevent silent resurrection

- **WHEN** a non-protected rule has a valid `<path>#<section-slug>` `target_surface`, `origin_anchor`, valid `mechanical-superseded` (>=1 entry) or `cross-model-internalized` (>=2 distinct normalized runtime/model-family entries), explicit `reopen_condition`, `record_kind: sim-retirement`, and an `attempts` entry starting with `retired`
- **THEN** `validate_sim_retirement_record` SHALL accept the record identically under both `PyYAML` and `simple_yaml_load`
- **AND** a fresh Self-Evolution session reading that tombstone without fresh `reopen_condition` failure evidence SHALL NOT silently reinstate the retired prose rule
