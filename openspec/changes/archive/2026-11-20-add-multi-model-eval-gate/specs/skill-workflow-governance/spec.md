## ADDED Requirements

### Requirement: Multi-model joint forward evaluation gate for Major portable behavior changes

`references/self-evolution-rule.md`, `references/skill-iteration-loop.md`, and
`scripts/validate_core_gates.py` SHALL enforce a proportionate multi-model joint
forward evaluation gate exclusively for **Major Self-Evolution changes that
modify portable behavioral prose** (`SKILL.md`, `references/*.md`, or
`templates/*.md` declared in `references/cross-cli-portable-manifest.json`),
without adding a new state file, modifying everyday hot paths, or slowing Patch,
Minor, or non-behavioral script/test-only edits.

Every qualifying Major portable prose change SHALL record an append-only,
dual-YAML compatible evaluation block (`record_kind: sim-multi-model-eval`) in
`docs/iteration/BACKLOG.md` satisfying one of two strict closure modes:

1. **`dual-covered` (default)**: `evaluations` SHALL contain at least 2 entries
   spanning at least 2 distinct normalized `runtime` values or at least 2
   distinct normalized `model_family` values (reusing open-world deterministic
   normalization without a closed model allowlist, honoring `CCG-009` and
   `SKILL.md` model-independence). Every evaluation SHALL cover the exact full
   set of declared `scenarios` (no missing, duplicate, or undeclared scenario
   IDs), cite a clean relative `evidence_ref`, and record `verdict: PASS`
   (majority voting or averaging over a `FAIL`/`BLOCKED` model is forbidden).
   Waiver fields SHALL NOT appear in a `dual-covered` record.
2. **`single-model-waived` (fail-closed unavailability fallback)**: Allowed only
   when a second runtime or model family is genuinely unavailable and explicitly
   waived by the user. The record SHALL retain at least 1 full-scenario `PASS`
   evaluation and MUST include `waiver_owner: user` (rejecting any agent, model,
   or CLI self-waiver), non-empty `waiver_reason`, clean relative
   `waiver_record_ref`, and non-empty `followup_recheck_condition`. Final
   reporting SHALL disclose single-model waiver scope rather than claiming
   dual-model verification.

In both modes, `record_kind: sim-multi-model-eval` records SHALL unconditionally
forbid `status: promoted` regardless of `decision_owner`, SHALL enforce
canonical string keys in `scenarios` and `evaluations` (`^[a-z][a-z0-9_-]*$`
excluding YAML 1.1 boolean/null literals) for dual-YAML parity, and SHALL
reject waiver keys in `dual-covered` records by key presence (even when empty
or `null`).

`scripts/validate_core_gates.py` SHALL also add
`references/self-evolution-rule.md#multi-model-joint-forward-evaluation-gate`
to `NON_RETIRABLE_SECTIONS` so S11's `validate_sim_retirement_record`
statically blocks retiring this locked governance section.

`scripts/validate_core_gates.py:main(...)` SHALL execute
`validate_multi_model_eval_guard` on owned visible sections of
`references/self-evolution-rule.md` and `references/skill-iteration-loop.md`,
and whenever `(root / "docs" / "iteration" / "BACKLOG.md").is_file()`, SHALL
scan all fenced YAML blocks with `record_kind == "sim-multi-model-eval"` or
top-level key `coverage_status` through `validate_multi_model_eval_record`
identically under both `PyYAML` and `simple_yaml_load` fallback.

#### Scenario: Dual-covered evaluation passes across distinct runtimes or open-world model families with full scenario parity

- **WHEN** a `record_kind: sim-multi-model-eval` record sets `coverage_status: dual-covered` with two evaluations covering the exact declared `scenarios` set, both recording `verdict: PASS`, and spanning at least two distinct normalized runtimes or two distinct normalized model families (including open-world families such as `deepseek-v4`)
- **THEN** `validate_multi_model_eval_record` SHALL accept the record identically under both `PyYAML` and `simple_yaml_load`

#### Scenario: Partial scenario coverage, same-family alias collapse, or one failing model fails closed

- **WHEN** a `dual-covered` record omits a declared scenario in one evaluation, pairs same-runtime alias and same-family tier variants (`agy` + `gemini-4-carbon` vs `antigravity_-cli` + `gemini-4-argon`), or records `verdict: FAIL` or `BLOCKED` on any evaluation alongside another `PASS`
- **THEN** `validate_multi_model_eval_record` SHALL reject the record fail-closed

#### Scenario: Single-model waiver requires explicit user ownership and cannot be self-approved by an agent

- **WHEN** a `single-model-waived` record sets `waiver_owner` to `codex`, `agy`, or any value other than `user`, omits `waiver_reason` / `waiver_record_ref` / `followup_recheck_condition`, or sets `status: promoted`
- **THEN** `validate_multi_model_eval_record` SHALL reject the record fail-closed
- **AND** a `single-model-waived` record with `waiver_owner: user`, valid relative `waiver_record_ref`, non-empty `waiver_reason` and `followup_recheck_condition`, and full-scenario `PASS` evaluation SHALL pass dual-YAML validation

#### Scenario: Production BACKLOG scanning enforces validity while exempting Patch/Minor and non-eval records

- **WHEN** `docs/iteration/BACKLOG.md` contains a malformed `record_kind: sim-multi-model-eval` block (including uppercase/trailing-space YAML fences or inline comments)
- **THEN** `scripts/validate_core_gates.py:main(...)` SHALL fail closed with `AssertionError` under both `PyYAML` and `simple_yaml_load`
- **AND** non-eval `BACKLOG.md` records containing nested `coverage_status` keys and runtime/distribution roots without `docs/iteration/BACKLOG.md` SHALL continue passing `validate_core_gates.py`
