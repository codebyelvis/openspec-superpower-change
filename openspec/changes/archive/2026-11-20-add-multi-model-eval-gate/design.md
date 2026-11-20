# Design: Multi-Model Joint Forward Evaluation Gate (S12)

Author: elvis. Revision: draft-v2. Status: proposal-only (awaiting explicit approval of `add-multi-model-eval-gate`).

## 1. Architectural Options Considered

| Option | Summary | Assessment |
|---|---|---|
| **Option 1 (Recommended)** | Gate **only Major Self-Evolution changes modifying portable behavioral prose**, reuse `docs/iteration/BACKLOG.md` (`record_kind: sim-multi-model-eval`) and `S11` open-world normalization helpers in `scripts/validate_core_gates.py:main(...)`, requiring `dual-covered` (`>= 2` distinct normalized runtimes or model families, all declared scenarios `PASS`) or explicit user-owned `single-model-waived`. | Zero new state files; zero everyday hot-path token cost; zero friction on Patch/Minor; prevents single-model harness overfitting (`arXiv:2611.18856v1` §4.3.3) while avoiding deadlock when a second runtime/model is unavailable; honors `CCG-009` (no closed model allowlist) and single-account execution. |
| **Option 2 (Rejected)** | Mandate multi-model forward evaluation on every Minor and Patch slice. | Severe everyday friction; violates anti-bloat principles and stalls low-risk fixes with little cross-model risk. |
| **Option 3 (Rejected)** | Require hard `dual-covered` with no waiver path, or allow majority-vote/average PASS across models. | Hard-only deadlocks when a second provider/CLI has an outage; majority-vote hides regressions on a sibling runtime that must stay safe. |

## 2. Activation Boundary

The gate activates **if and only if** a Self-Evolution slice meets **both** conditions:
1. Change level is **Major** (touching trigger scope, request routing, OpenSpec/Superpowers boundaries, Step Evidence Gate signoff, completion-claim rules, or governed prose retirement/eval gates); **AND**
2. The approved change modifies at least one portable behavioral prose file (`SKILL.md`, `references/*.md`, or `templates/*.md` listed in `references/cross-cli-portable-manifest.json`).

Explicitly **exempt**:
- All Patch and Minor Self-Evolution slices;
- Pure script/validator/test/doc changes that do not alter portable behavioral prose;
- Ordinary business-project changes.

## 3. Dual-YAML Record Contract (`record_kind: sim-multi-model-eval`)

Records live in `docs/iteration/BACKLOG.md` under the slice's details using pure nested mappings and scalar lists compatible with both `PyYAML` (`yaml.safe_load`) and `scripts/validate_core_gates.py:simple_yaml_load` (no list-of-dicts, no inline `#` comments, no unquoted `: ` in scalars).

### 3.1 `dual-covered` Shape (Default)

```yaml
record_kind: sim-multi-model-eval
slice: S12
change_id: add-multi-model-eval-gate
coverage_status: dual-covered
scenarios:
  scenario_1:
    kind: fast-path
    summary: Minor slice exempt from multi-model gate proceeds without deadlock
  scenario_2:
    kind: strict-safety
    summary: Major portable prose edit without second model blocks unless user waiver recorded
evaluations:
  eval_1:
    runtime: antigravity-cli
    model_family: gemini-4-neon
    scenario_ids:
      - scenario_1
      - scenario_2
    verdict: PASS
    evidence_ref: docs/review/2026-11-20-S12-eval-gemini.md
  eval_2:
    runtime: antigravity-cli
    model_family: claude-opus-5.5
    scenario_ids:
      - scenario_1
      - scenario_2
    verdict: PASS
    evidence_ref: docs/review/2026-11-20-S12-eval-claude.md
```

### 3.2 `single-model-waived` Shape (User-Signed Outage Fallback)

```yaml
record_kind: sim-multi-model-eval
slice: S12
change_id: add-multi-model-eval-gate
coverage_status: single-model-waived
waiver_owner: user
waiver_reason: second model family temporarily unavailable due to provider quota exhaustion
waiver_record_ref: docs/review/2026-11-20-S12-multi-model-eval-gate-draft.md
followup_recheck_condition: re-run scenario_1 and scenario_2 on a second model family once quota recovers
scenarios:
  scenario_1:
    kind: fast-path
    summary: Minor slice exempt from multi-model gate proceeds without deadlock
  scenario_2:
    kind: strict-safety
    summary: Major portable prose edit without second model blocks unless user waiver recorded
evaluations:
  eval_1:
    runtime: antigravity-cli
    model_family: gemini-4-neon
    scenario_ids:
      - scenario_1
      - scenario_2
    verdict: PASS
    evidence_ref: docs/review/2026-11-20-S12-eval-gemini.md
```

### 3.3 Deterministic Fail-Closed Rules (`validate_multi_model_eval_record`)

`scripts/validate_core_gates.py` SHALL expose `validate_multi_model_eval_record(record: dict, label: str = "sim-multi-model-eval") -> None`, directly reusing `_normalize_relative_path`, `_normalize_runtime_name`, and `_normalize_model_family` from `S11`:

1. **Unconditional Ban on `status: promoted`**: Reject unconditionally (raising `AssertionError`) if `record.get("status")` is a string whose trimmed lowercase equals `"promoted"`, regardless of `decision_owner`. Any non-`str` scalar where a string is required MUST explicitly raise `AssertionError`.
2. **Header & Enum Integrity**:
   - `record_kind` MUST equal `"sim-multi-model-eval"`.
   - `slice` MUST be a non-empty `str`; `change_id` MUST be a `str` matching `^[a-z0-9][a-z0-9-]{1,80}$`.
   - `coverage_status` MUST be strictly `"dual-covered"` or `"single-model-waived"`.
3. **Declared `scenarios` Integrity (Dual-YAML Key Parity)**:
   - `scenarios` MUST be a non-empty mapping (`len(scenarios) >= 1`). Every key `k` in `scenarios` (and in `evaluations`) MUST satisfy `isinstance(k, str)`, match `^[a-z][a-z0-9_-]*$`, and NOT be a YAML 1.1 boolean/null literal (`true`, `false`, `null`, `yes`, `no`, `on`, `off`), guaranteeing identical key types across `PyYAML` and `simple_yaml_load`.
   - Each scenario entry MUST be a mapping with `kind` in `{"fast-path", "strict-safety", "adversarial"}` and non-empty string `summary`.
4. **Evaluations Full-Coverage & Zero-Tolerance `PASS` Enforcement**:
   - `evaluations` MUST be a non-empty mapping (`dict`) with valid string keys as defined in rule 3.
   - Every entry `ev` MUST be a mapping containing:
     - `runtime`: validated via `_normalize_runtime_name` (single value, collapses `[-_]+`, maps `agy`/`antigravity` -> `antigravity-cli`, `grok` -> `grok-cli`);
     - `model_family`: validated via `_normalize_model_family` (single value, open-world suffix stripping, rejects empty stem like `v4-high`, no closed model allowlist);
     - `scenario_ids`: non-empty `list` of strings with **no duplicates** (`len(ids) == len(set(ids))`) and **exact full coverage** (`set(ids) == set(scenarios.keys())`); partial or phantom scenario coverage fails closed;
     - `verdict`: MUST be strictly `"PASS"` (any `"FAIL"`, `"BLOCKED"`, non-`str`, or other value fails closed; majority vote or averaging is forbidden);
     - `evidence_ref`: clean project-relative path validated via `_normalize_relative_path`.
5. **Mode-Specific Closure Rules**:
   - If `coverage_status == "dual-covered"`:
     - Require `len(evaluations) >= 2` AND `(len(unique_normalized_runtimes) >= 2 or len(unique_normalized_model_families) >= 2)`.
     - Reject by key presence (`key in record`, not truthiness) if any waiver field (`waiver_owner`, `waiver_reason`, `waiver_record_ref`, `followup_recheck_condition`) appears, even with empty or `null` values.
   - If `coverage_status == "single-model-waived"`:
     - Require `len(evaluations) >= 1`.
     - Require `waiver_owner` to be a `str` whose trimmed lowercase equals strictly `"user"` (reject any agent/model/CLI self-waiver such as `codex`, `agy`, `claude`, `gemini`, `control-plane`).
     - Require non-empty `str` `waiver_reason`, clean relative path `waiver_record_ref` (via `_normalize_relative_path`), and non-empty `str` `followup_recheck_condition`.
6. **Honest Static-vs-Runtime Boundary**: `validate_multi_model_eval_record` enforces schema, open-world independence, full-scenario parity, unanimous `PASS`, and user-owned waiver hygiene; verifying that `evidence_ref` reflects genuine unhinted execution remains the responsibility of independent Implementation and Final Review.

### 3.4 Production Wiring in `scripts/validate_core_gates.py:main(...)`

- Add `"references/self-evolution-rule.md#multi-model-joint-forward-evaluation-gate"` to `NON_RETIRABLE_SECTIONS` so S11's `validate_sim_retirement_record` statically blocks any retirement tombstone targeting S12's new locked governance section.
- Add `validate_multi_model_eval_guard(self_rule, loop)` invoked in `main(...)`:
  - On `_markdown_visible_content(_markdown_owned_section(self_rule, "## Multi-Model Joint Forward Evaluation Gate", ...))`, require minimal locked phrases: `"Major Self-Evolution"`, `"cross-cli-portable-manifest.json"`, `"sim-multi-model-eval"`, `"dual-covered"`, `"single-model-waived"`, `"waiver_owner: user"`, `"verdict: PASS"`, and `"status: promoted"`.
  - On `_markdown_visible_content(_markdown_owned_section(loop, "## One-round sequence", ...))`, require: `"Multi-Model Joint Forward Evaluation Gate"`, `"dual-covered"`, `"single-model-waived"`, `"sim-multi-model-eval"`, and `"Patch/Minor"`.
- Add `_validate_backlog_sim_multi_model_evals(root)` invoked in `main(...)` alongside `_validate_backlog_sim_retirements(root)` (skipping cleanly when `docs/iteration/BACKLOG.md` is absent in distribution/runtime roots):
  - Same hardened fence regex `r"^[ \t]*```yaml[ \t]*\r?\n(.*?)\r?\n[ \t]*```[ \t]*$"` (`re.S | re.M | re.I`).
  - Zero-indentation top-level hint regex: `^record_kind\s*:\s*['\"]?sim-multi-model-eval['\"]?(?:\s+#.*|\s*)$` or `^coverage_status\s*:`.
  - Wraps parse errors on matching blocks as `AssertionError`, ignores nested `coverage_status:` in non-eval records, and validates every matching block via `validate_multi_model_eval_record`.

## 4. Target Files, Cohesive Batch, and Exact Verification Anchors (Phase B Only)

### Batch 1 (Single Cohesive Implementation Batch after Approval)

- **Target files**:
  1. `references/self-evolution-rule.md`: add `## Multi-Model Joint Forward Evaluation Gate`.
  2. `references/skill-iteration-loop.md`: update Step 6 in `## One-round sequence` to bind Major portable behavioral prose changes to the gate while exempting Patch/Minor and non-behavioral script/test edits.
  3. `scripts/validate_core_gates.py`: add `"references/self-evolution-rule.md#multi-model-joint-forward-evaluation-gate"` to `NON_RETIRABLE_SECTIONS`, add `validate_multi_model_eval_record`, `validate_multi_model_eval_guard`, and `_validate_backlog_sim_multi_model_evals`, and wire them into `main(...)`.
  4. `tests/test_workflow_rules.py`: add RED->GREEN unit tests and negative counterexamples under both PyYAML and `simple_yaml_load` fallback (valid `dual-covered` across runtimes & across model families including open-world `deepseek-v4`; valid `single-model-waived`; reject retiring `references/self-evolution-rule.md#multi-model-joint-forward-evaluation-gate`; reject non-canonical/YAML-literal keys like `1` or `true` in `scenarios`/`evaluations`; reject same-runtime alias + same-family tier collapse; reject partial/duplicate/phantom `scenario_ids`; reject single failing `verdict: FAIL` hidden beside a `PASS`; reject non-user `waiver_owner`; reject any waiver key presence including empty/null in `dual-covered`; reject `status: promoted`; reject malformed/uppercase-fence/inline-comment `BACKLOG.md` blocks in `main(...)`; confirm nested `coverage_status` in non-eval records does not false-positive; confirm owned visible section guard rejects mutations).
  5. `distribution/codex-plugin` (regenerated via `/opt/homebrew/bin/python3 scripts/build_codex_plugin.py .`).
  6. `CHANGELOG.md`, `docs/iteration/{BACKLOG,CURRENT,LOG}.md` (and `openspec/specs/skill-workflow-governance/spec.md` on archive).

- **Exact verification & closure sequence (Phase B)**:
  1. `/usr/bin/python3 -m py_compile scripts/*.py`
  2. `/opt/anaconda3/bin/python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .`
  3. `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_core_gates.py .` (no-PyYAML fallback)
  4. `PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 scripts/validate_core_gates.py .` (PyYAML)
  5. `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_distribution.py .`
  6. `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 -m unittest discover -s tests -v` (main repo + clean-tree no-PyYAML fallback under `/private/tmp/<parent>/openspec-superpower-change` with sibling symlink `codex-brief-antigravity-review`)
  7. `PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 -m unittest discover -s tests -p test_workflow_rules.py -v` (PyYAML)
  8. Isolated 2-scenario read-only forward-test (dogfooding S12 sequentially across 2 distinct model families/runtimes, or explicit user-signed `single-model-waived` if unavailable) -> **persist S12's own `record_kind: sim-multi-model-eval` block (with real `evidence_ref` / `waiver_record_ref`) into `docs/iteration/BACKLOG.md` and re-run dual-parser `validate_core_gates.py .` BEFORE Implementation Review**.
  9. Independent Implementation Review (`readonly-reviewer`, `same_instance=false`, inspecting code, tests, AND the persisted S12 `sim-multi-model-eval` record + `evidence_ref`) -> `PASS`.
  10. Four-target (`codex`, `pi`, `antigravity-cli`, `grok-cli` with `grok inspect --json --consume`) schema-v2 scoped sync for the 3 modified portable files (`references/self-evolution-rule.md`, `references/skill-iteration-loop.md`, `scripts/validate_core_gates.py`) via `scripts/validate_cross_cli_sync.py` + `verify-all` (managed rule v6 untouched).
  11. OpenSpec archive (`openspec archive add-multi-model-eval-gate --yes` + `openspec validate --specs --strict`), update `CHANGELOG.md` and `docs/iteration/{BACKLOG,CURRENT,LOG}.md` (recording `awaiting-final-review`), and re-run dual-parser `validate_core_gates.py .` + `validate_distribution.py .`.
  12. Independent Final Review (`same_instance=false`, distinct from executor & Implementation Reviewer, inspecting merged main spec, complete final diff including `BACKLOG.md` `sim-multi-model-eval` + `CHANGELOG.md`, fresh verification counts, and four-target `verify-all` evidence per `CCG-007` & `CCG-016`) -> `PASS`.
  13. Pure status closeout (`BACKLOG` `done`, `CURRENT` `idle`, archived `tasks.md` final checkboxes), `scripts/check_commit_text.py`, exact commit & push on `main` (excluding 6 legacy dirty groups), and `/private/tmp/osc-*` cleanup.

## 5. Compatibility & Rollback

- **Backward compatibility**: All existing `S1`–`S11` records, `sim-backfill`, `sim-slice-record`, and `sim-retirement` records remain valid unchanged. `SKILL.md`, `templates/learning-candidate-template.md`, `references/shared-global-governance.md` (v6), and `references/project-learning-closeout.md` are untouched.
- **Proposal-only rollback (Phase A)**: Remove `openspec/changes/add-multi-model-eval-gate/` and `docs/review/2026-11-20-S12-multi-model-eval-gate-draft.md`, and restore `docs/iteration/{BACKLOG,CURRENT}.md` to pre-proposal lines.
- **Post-approval rollback (Phase B)**: Restore from `/private/tmp/osc-backup-<timestamp>` prior to push, or `git revert <commit>` plus transactional reverse scoped sync via `scripts/validate_cross_cli_sync.py`.
