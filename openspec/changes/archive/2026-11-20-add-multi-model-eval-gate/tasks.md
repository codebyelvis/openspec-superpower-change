# Tasks: add-multi-model-eval-gate (S12)

Author: elvis. Revision: draft-v2. Status: completed (approved via `迭代优化skill：已批准 add-multi-model-eval-gate`, archived and verified via independent Final Review `f4815960`).

## Phase A — Proposal Draft & Strict Validation (Current Gate Only)

- [x] Draft `openspec/changes/add-multi-model-eval-gate/proposal.md` (draft-v2)
- [x] Draft `openspec/changes/add-multi-model-eval-gate/design.md` (draft-v2: activation scope, dual-YAML `dual-covered` / `single-model-waived` schemas, key-parity & key-presence fail-closed rules, `NON_RETIRABLE_SECTIONS` protection for the new gate section, `main(...)` wiring, and Review-before-closeout ordering)
- [x] Draft `openspec/changes/add-multi-model-eval-gate/tasks.md` (draft-v2)
- [x] Draft `openspec/changes/add-multi-model-eval-gate/specs/skill-workflow-governance/spec.md` (draft-v2)
- [x] Draft Major Self-Evolution review plan `docs/review/2026-11-20-S12-multi-model-eval-gate-draft.md` (draft-v2)
- [x] Record `S12` awaiting-approval status in `docs/iteration/BACKLOG.md` and `docs/iteration/CURRENT.md` without modifying source rules, scripts, tests, generated artifacts, or runtimes
- [x] Run `/opt/homebrew/bin/openspec validate add-multi-model-eval-gate --strict`, dual-YAML schema checks on both `design.md` YAML blocks, and existing `quick_validate.py` + dual-parser `validate_core_gates.py` (`/opt/homebrew/bin/python3` & `/opt/anaconda3/bin/python3`) + `validate_distribution.py`
- [x] Pass independent read-only `FOCUSED_RECHECK` of draft-v2 and stop awaiting explicit user approval (`迭代优化skill：已批准 add-multi-model-eval-gate`)

## Phase B — Approved Implementation & Closure (DO NOT EXECUTE BEFORE APPROVAL)

- [x] Record explicit approval SHA-256 table in `docs/review/2026-11-20-S12-multi-model-eval-gate-draft.md` and create structured backup under `/private/tmp/osc-backup-<timestamp>`
- [x] Write RED regression tests in `tests/test_workflow_rules.py` for `validate_multi_model_eval_guard`, `NON_RETIRABLE_SECTIONS` blocking retirement of `references/self-evolution-rule.md#multi-model-joint-forward-evaluation-gate`, `validate_multi_model_eval_record` (valid `dual-covered` & `single-model-waived`, open-world `deepseek-v4`, canonical key-parity rejecting numeric/YAML-literal keys, alias/tier collapse, partial/duplicate/phantom `scenario_ids`, unanimous `PASS` enforcement, strict `waiver_owner: user`, key-presence mixed-waiver rejection including empty/null values, unconditional `status: promoted` ban, and `main(...)` `BACKLOG.md` scanning with uppercase/spaced fence, inline comments, and nested-key non-false-positive), and verify RED failure
- [x] Implement `## Multi-Model Joint Forward Evaluation Gate` in `references/self-evolution-rule.md` and update Step 6 in `references/skill-iteration-loop.md`
- [x] Implement `"references/self-evolution-rule.md#multi-model-joint-forward-evaluation-gate"` in `NON_RETIRABLE_SECTIONS`, plus `validate_multi_model_eval_record`, `validate_multi_model_eval_guard`, and `_validate_backlog_sim_multi_model_evals` wired into `scripts/validate_core_gates.py:main(...)`, and verify GREEN
- [x] Regenerate `distribution/codex-plugin` via `/opt/homebrew/bin/python3 scripts/build_codex_plugin.py .`
- [x] Run full verification suite:
  - `/usr/bin/python3 -m py_compile scripts/*.py`
  - `/opt/anaconda3/bin/python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .`
  - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_core_gates.py .` (no-PyYAML fallback)
  - `PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 scripts/validate_core_gates.py .` (PyYAML)
  - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_distribution.py .`
  - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 -m unittest discover -s tests -v` (main repo + clean-tree no-PyYAML fallback)
  - `PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 -m unittest discover -s tests -p test_workflow_rules.py -v` (PyYAML)
- [x] Run isolated read-only 2-scenario forward-test (Minor exempt vs Major portable prose gating), dogfooding `dual-covered` sequentially across two distinct model families/runtimes (or explicit user-approved `single-model-waived` if unavailable), **persist S12's own `record_kind: sim-multi-model-eval` block (with real `evidence_ref` / `waiver_record_ref`) into `docs/iteration/BACKLOG.md`, and re-run dual-parser `validate_core_gates.py .` (`/opt/homebrew/bin/python3` and `/opt/anaconda3/bin/python3`) to confirm production pass before Implementation Review**
- [x] Pass independent read-only Implementation Review (`readonly-reviewer`, `same_instance=false`, inspecting code, tests, and the persisted S12 `sim-multi-model-eval` record + `evidence_ref`)
- [x] Execute 4-target (`codex`, `pi`, `antigravity-cli`, `grok-cli` with `grok inspect --json --consume`) schema-v2 scoped sync via `scripts/validate_cross_cli_sync.py` + `verify-all` (3 selected portable files, governance v6 unchanged)
- [x] Archive `add-multi-model-eval-gate` via `openspec archive` + `openspec validate --specs --strict`, update `CHANGELOG.md` and `docs/iteration/{BACKLOG,CURRENT,LOG}.md` (`CURRENT` set to `awaiting-final-review`), and re-run fresh dual-parser `validate_core_gates.py .` + `validate_distribution.py .`
- [x] Pass independent Final Review (`same_instance=false`, distinct from executor & Implementation Reviewer, inspecting merged main spec, complete final diff including `BACKLOG.md` `sim-multi-model-eval` + `CHANGELOG.md`, fresh verification counts, and four-target `verify-all` evidence per `CCG-007` & `CCG-016`)
- [x] Perform pure status closeout (`BACKLOG` `done`, `CURRENT` `idle`, archived `tasks.md` final checkboxes), run `scripts/check_commit_text.py`, commit & push only S12 files on `main` (excluding the 6 legacy dirty groups), and clean `/private/tmp/osc-*`
