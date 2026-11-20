# Change: Multi-Model Joint Forward Evaluation Gate for Major Portable Behavior Changes

Author: elvis. Revision: draft-v2. Status: proposal-only (awaiting explicit `迭代优化skill：已批准 add-multi-model-eval-gate`; no implementation, runtime sync, or Git mutation authorized).

## Why

1. **Empirical cross-model overfitting risk (`arXiv:2611.18856v1` §4.3.3 Table 2)**:
   - When one agent harness serves multiple model families (Grok 4.20 Reasoning, Claude Opus 5.5, and Gemini 3.8 Flash), edits evolved on a single model family degraded sibling models (`66.84–72.24` mean held-out score), whereas unified multi-model feedback matched per-model specialized harnesses (`75.24` vs `75.20`) and outperformed the shared seed (`73.28`).
2. **Current Self-Evolution gap across four shared CLI runtimes**:
   - `openspec-superpower-change` synchronizes one shared portable skill surface across `codex`, `pi`, `antigravity-cli`, and `grok-cli` spanning distinct model families.
   - `S11` (`61d22ff`) closed the **rule-retirement** half (`validate_sim_retirement_record` requiring `>= 2` distinct normalized runtimes or model families for `cross-model-internalized`), but **adding or modifying** Major portable behavior rules (triggers, routing, OpenSpec/Superpowers boundaries, evidence/completion gates) still has no structured multi-model forward-evaluation gate or deterministic validator. A rule change validated only on one model family can silently over-trigger, loop, or weaken guards on sibling runtimes.
3. **Proportionate friction requirement**:
   - Patch/Minor slices and purely mechanical script/test-only edits must stay fast and exempt; only Major Self-Evolution changes touching portable behavioral prose need multi-model joint forward evaluation, with a fail-closed, user-owned waiver path when a second runtime/model family is genuinely unavailable.

## What Changes

- **M1 — Multi-Model Joint Forward Evaluation Gate (`references/self-evolution-rule.md`, `references/skill-iteration-loop.md`)**:
  - Add `## Multi-Model Joint Forward Evaluation Gate` to `references/self-evolution-rule.md` scoping the gate strictly to **Major Self-Evolution changes that modify portable behavioral prose** (`SKILL.md`, `references/*.md`, or `templates/*.md` declared in `references/cross-cli-portable-manifest.json`). Patch/Minor slices, business projects, and non-behavioral script/test-only edits are exempt; zero everyday hot-path token cost.
  - Define two strict closure statuses recorded as an append-only dual-YAML block (`record_kind: sim-multi-model-eval`) in `docs/iteration/BACKLOG.md` (reusing existing state, no new state file):
    1. `dual-covered` (default): `>= 2` isolated forward evaluations spanning **at least 2 distinct normalized `runtime` values or 2 distinct normalized `model_family` values** (reusing `S11` open-world normalization with no closed model allowlist, respecting `CCG-009` and `SKILL.md:145`), where **every** evaluation covers the full declared `scenarios` set and achieves `verdict: PASS` (no averaging or majority voting over a failing model).
    2. `single-model-waived` (fail-closed emergency escape hatch): allowed **only** when a second runtime/model family is demonstrably unavailable and the **user** explicitly signs off (`waiver_owner: user`, non-empty `waiver_reason`, relative `waiver_record_ref`, explicit `followup_recheck_condition`, plus `>= 1` full-scenario `PASS` evaluation); agents can never self-approve a waiver, and the final report must honestly disclose single-model waiver scope rather than claiming dual-model verification.
  - Link this gate in `references/skill-iteration-loop.md` Step 6 (`## One-round sequence`) without weakening existing `## Authorization` or `## Reading budget for one round` boundaries.
- **M2 — Production-Wired Deterministic Validator & Regressions (`scripts/validate_core_gates.py`, `tests/test_workflow_rules.py`)**:
  - Reuse `S11`'s `_normalize_relative_path`, `_normalize_runtime_name`, and `_normalize_model_family` to implement `validate_multi_model_eval_record(record: dict, label: str)` and `validate_multi_model_eval_guard(self_rule, loop)`, and add `"references/self-evolution-rule.md#multi-model-joint-forward-evaluation-gate"` to `S11`'s `NON_RETIRABLE_SECTIONS` so this new locked governance section cannot be retired via `sim-retirement`.
  - Wire `validate_multi_model_eval_guard` and `_validate_backlog_sim_multi_model_evals(root)` into `scripts/validate_core_gates.py:main(...)`, scanning fenced YAML blocks in `docs/iteration/BACKLOG.md` (when present) whose top-level mapping has `record_kind == "sim-multi-model-eval"` or key `coverage_status` identically under both `PyYAML` and `simple_yaml_load`.
  - Add RED->GREEN unit tests and adversarial counterexamples in `tests/test_workflow_rules.py` verified under both parsers.

## Scope and Non-Goals

- **Phase A in-scope files (current proposal-only gate)**:
  - `openspec/changes/add-multi-model-eval-gate/{proposal,design,tasks}.md`
  - `openspec/changes/add-multi-model-eval-gate/specs/skill-workflow-governance/spec.md`
  - `docs/review/2026-11-20-S12-multi-model-eval-gate-draft.md`
  - `docs/iteration/BACKLOG.md` (append `S12` proposal-only entry) and `docs/iteration/CURRENT.md` (record `S12` awaiting-approval state)
- **Phase B in-scope files (strictly after `迭代优化skill：已批准 add-multi-model-eval-gate`)**:
  - `references/self-evolution-rule.md`
  - `references/skill-iteration-loop.md`
  - `scripts/validate_core_gates.py`
  - `tests/test_workflow_rules.py`
  - `distribution/codex-plugin` (regenerated via `scripts/build_codex_plugin.py .`)
  - `openspec/specs/skill-workflow-governance/spec.md` (on archive)
  - `CHANGELOG.md`, `docs/iteration/{BACKLOG,CURRENT,LOG}.md`
- **Explicit Non-Goals**:
  - Does NOT apply to Patch/Minor Self-Evolution or ordinary business-project development.
  - Does NOT add a new state file, modify `SKILL.md` / `references/shared-global-governance.md` (v6) / `templates/learning-candidate-template.md`, or introduce automated multi-account concurrent CLI dispatch.
  - Does NOT touch any of the 6 legacy dirty working-tree file groups.
