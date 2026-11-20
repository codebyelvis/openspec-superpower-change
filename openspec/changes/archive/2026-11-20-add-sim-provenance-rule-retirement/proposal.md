# Change: Provenance-Gated Rule Retirement with SIM Append-Only Tombstones

Author: elvis. Revision: draft-v2. Status: proposal-only (awaiting explicit `迭代优化skill：已批准 add-sim-provenance-rule-retirement`; no implementation, runtime sync, or Git mutation authorized).

## Why

1. **Empirical model-generation and cross-model harness drag (`arXiv:2611.18856v1`)**:
   - In continual recursive self-improvement across Gemini generations (§4.3.2 Table 1), inherited harness patches helped earlier jumps (`+3.5` on 3.5 Flash, `+1.6` on 3.8 Flash) but trailed a fresh seed optimization on stronger Gemini 4 Argon (`94.8` vs `95.6`, `-0.8`). Accumulated patches built for weaker/older models become overhead once frontier models internalize those behaviors.
   - Across shared multi-model harnesses (§4.3.3 Table 2, Grok 4.20 / Opus 5.5 / Gemini 3.8 Flash), single-model patches degraded other models (`66.84–72.24` vs unified multi-model synthesis `75.24`), proving that retiring or revising a shared rule based on a single model's pass can break sibling runtimes.
2. **Governance gap between existing prose lock and S10 SIM memory**:
   - `references/project-learning-closeout.md` (and `openspec/specs/skill-workflow-governance/spec.md`) already require Major Self-Evolution approval before condensing or retiring governed skill/workflow prose and forbid removing `Non-Negotiables` or validator-locked phrases.
   - Slice `S10` (`b344a26`) added append-only `root_cause` / `attempts` (`provenance`, `change`, `predicted`, `observed`) optimizer memory in `templates/learning-candidate-template.md`, `references/skill-iteration-loop.md`, and `docs/iteration/BACKLOG.md`.
   - However, there is currently **no operational contract or deterministic validator** specifying: (a) which concrete repository files and sections are permanently non-retirable, (b) what structured provenance and dual-path retirement proof (higher-layer mechanical replacement OR multi-runtime/cross-model isolated internalization proof) is required before proposing retirement, and (c) how retired rules leave an append-only SIM tombstone in `BACKLOG.md` validated automatically by `scripts/validate_core_gates.py`.

## What Changes

- **R1 — Permanent Non-Retirable Boundary & Provenance-Gated Retirement Contract (`references/self-evolution-rule.md`)**:
  - Add a `## Provenance-Gated Rule Retirement` section formalizing four mandatory prerequisites for retiring governed skill/workflow prose (all remain strictly **Major Self-Evolution**, never downgraded to Minor):
    1. **Hard Exclusion**: Permanently forbid retiring protected governance files (`SKILL.md`, `references/shared-global-governance.md`, `references/completion-contract.md`, `references/step-evidence-gate.md`, `references/handoff-contract.md`, `references/confirmation-lease.md`, `references/agent-capability-routing.md`, `references/openspec-decision-rule.md`), locked governance sections (such as `references/self-evolution-rule.md#hard-prohibitions`, `references/skill-iteration-loop.md#authorization`, `references/skill-iteration-loop.md#reading-budget-for-one-round`, `references/project-learning-closeout.md#triggers`, `references/project-learning-closeout.md#enforcement-and-review`), and any `Non-Negotiables` / `CCG-*` / validator-locked phrase.
    2. **SIM Provenance Anchoring**: Require a verifiable `origin_anchor` (BACKLOG SIM entry, Git commit, archived OpenSpec change, or `CHANGELOG.md` entry) naming the model/runtime and original failure mode the rule targeted. Rules without provenance cannot be retired as "redundant prose".
    3. **Structured Bidirectional Retirement Proof (`retirement_basis` + `retirement_evidence`)**:
       - `mechanical-superseded`: at least 1 structured entry naming the deterministic higher-layer `validator_or_test` path and `negative_case` proving the prior failure mode is rejected mechanically; OR
       - `cross-model-internalized`: at least 2 structured entries (`runtime`, `model_family`, `probe_ref`) providing isolated, unhinted forward-test evidence across **at least 2 distinct normalized runtimes or 2 distinct normalized model families** (without a closed model allowlist) showing non-recurrence after prose removal.
    4. **Major Approval + Append-Only Tombstone**: Require explicit Major OpenSpec approval (`已批准 <change-id>`), independent Implementation Review, and independent Final Review after cross-CLI sync; record retirement in `docs/iteration/BACKLOG.md` via `record_kind: sim-retirement` (never `status: promoted`) with an append-only `observed: retired - ...` attempt and explicit `reopen_condition` (no new state file).
- **R2 — Iteration Loop & Template Alignment (`references/skill-iteration-loop.md`, `templates/learning-candidate-template.md`)**:
  - Update `references/skill-iteration-loop.md` Step 3 from 4 to 5 optimizer-memory guidelines by adding the non-resurrection rule (a `retired` rule is only reconsidered when fresh failure evidence triggers its `reopen_condition`, and retirement itself remains Major), keeping SIM memory non-gating and out of everyday hot paths.
  - Extend `templates/learning-candidate-template.md` `## Rules` to note `retired` alongside `reverted` as a valid `observed` outcome prefix for append-only SIM records (preserving existing required fields, Codex-only `status: promoted`, and dual-YAML compatibility).
- **R3 — Production-Wired Deterministic Validator & Negative Regression Suite (`scripts/validate_core_gates.py`, `tests/test_workflow_rules.py`)**:
  - Add `NON_RETIRABLE_FILES`, `NON_RETIRABLE_SECTIONS`, `NON_RETIRABLE_SLUG_TOKENS`, `validate_sim_retirement_record(record: dict)`, and `validate_sim_rule_retirement_guard(self_rule, loop, template)` wired directly into `scripts/validate_core_gates.py:main(...)`.
  - In `main(...)`, when `(root / "docs" / "iteration" / "BACKLOG.md").is_file()`, automatically scan all fenced YAML blocks whose parsed mapping has `record_kind == "sim-retirement"` or contains `retirement_basis`, and validate each block with `validate_sim_retirement_record` (compatible with distribution/runtime roots that omit `docs/iteration/`).
  - Add RED->GREEN unit tests and negative counterexamples in `tests/test_workflow_rules.py` verified under both PyYAML and `simple_yaml_load` fallback.

## Scope and Non-Goals

- **Phase A in-scope files (current proposal-only gate)**:
  - `openspec/changes/add-sim-provenance-rule-retirement/{proposal,design,tasks}.md`
  - `openspec/changes/add-sim-provenance-rule-retirement/specs/skill-workflow-governance/spec.md`
  - `docs/review/2026-11-20-S11-sim-provenance-rule-retirement-draft.md`
  - `docs/iteration/BACKLOG.md` (append `S11` proposal-only entry) and `docs/iteration/CURRENT.md` (record `S11` awaiting-approval state)
- **Phase B in-scope files (strictly after `迭代优化skill：已批准 add-sim-provenance-rule-retirement`)**:
  - `references/self-evolution-rule.md`
  - `references/skill-iteration-loop.md`
  - `templates/learning-candidate-template.md`
  - `scripts/validate_core_gates.py`
  - `tests/test_workflow_rules.py`
  - `distribution/codex-plugin` (regenerated via `scripts/build_codex_plugin.py .`)
  - `openspec/specs/skill-workflow-governance/spec.md` (on archive)
  - `CHANGELOG.md`, `docs/iteration/{BACKLOG,CURRENT,LOG}.md`
- **Explicit Non-Goals**:
  - Does NOT retire any concrete existing rule in this change (establishes the retirement contract, tombstone schema, and production-wired validator only).
  - Does NOT create a new durable state file (`SIM.md` or `RETIRED.md`).
  - Does NOT modify `SKILL.md`, `references/shared-global-governance.md` (governance v6), `references/project-learning-closeout.md`, or any of the 6 untouched legacy dirty file groups.
  - Does NOT downgrade rule retirement from Major to Minor or automate prose deletion.
