# Tasks: add-sim-provenance-rule-retirement (S11)

Author: elvis. Revision: draft-v2. Status: proposal-only (Phase B strictly blocked until explicit `迭代优化skill：已批准 add-sim-provenance-rule-retirement`).

## Phase A — Proposal Draft & Strict Validation (Current Gate Only)

- [x] Draft `openspec/changes/add-sim-provenance-rule-retirement/proposal.md` (draft-v2)
- [x] Draft `openspec/changes/add-sim-provenance-rule-retirement/design.md` (draft-v2: repository-anchored exclusions, structured dual-YAML evidence schema, open-world runtime/model normalization, `main(...)` `BACKLOG.md` wiring, and Final Review closure)
- [x] Draft `openspec/changes/add-sim-provenance-rule-retirement/tasks.md` (draft-v2)
- [x] Draft `openspec/changes/add-sim-provenance-rule-retirement/specs/skill-workflow-governance/spec.md` (draft-v2)
- [x] Draft Major Self-Evolution review plan `docs/review/2026-11-20-S11-sim-provenance-rule-retirement-draft.md` (draft-v2)
- [x] Record `S11` awaiting-approval status in `docs/iteration/BACKLOG.md` and `docs/iteration/CURRENT.md` without modifying source rules, tests, generated artifacts, or runtimes
- [x] Run `/opt/homebrew/bin/openspec validate add-sim-provenance-rule-retirement --strict`, dual-YAML schema checks, and existing `quick_validate.py` + dual-parser `validate_core_gates.py` + `validate_distribution.py`
- [x] Pass independent read-only `FOCUSED_RECHECK` of draft-v2 and stop awaiting explicit user approval (`迭代优化skill：已批准 add-sim-provenance-rule-retirement`)

## Phase B — Approved Implementation & Closure (DO NOT EXECUTE BEFORE APPROVAL)

- [x] Record explicit approval SHA-256 table in `docs/review/2026-11-20-S11-sim-provenance-rule-retirement-draft.md` and create structured backup under `/private/tmp/osc-backup-<timestamp>`
- [x] Write RED regression tests in `tests/test_workflow_rules.py` for `validate_sim_rule_retirement_guard`, `validate_sim_retirement_record` (including alias/tier collapse, open-world model acceptance, real protected file/section & `#L` line-anchor rejection, unconditional `status: promoted` ban, and `main(...)` `BACKLOG.md` scan), and verify RED failure
- [x] Implement `## Provenance-Gated Rule Retirement` in `references/self-evolution-rule.md`, update Step 3 (`4 条准则` -> `5 条准则` + non-resurrection rule) in `references/skill-iteration-loop.md`, and update `## Rules` (`reverted` / `retired`) in `templates/learning-candidate-template.md`
- [x] Implement `NON_RETIRABLE_FILES`, `NON_RETIRABLE_SECTIONS`, `NON_RETIRABLE_SLUG_TOKENS`, `validate_sim_retirement_record`, and `validate_sim_rule_retirement_guard` wired into `scripts/validate_core_gates.py:main(...)` (including conditional `docs/iteration/BACKLOG.md` retirement-block scanning) and verify GREEN
- [x] Regenerate `distribution/codex-plugin` via `/opt/homebrew/bin/python3 scripts/build_codex_plugin.py .`
- [x] Run full verification suite:
  - `/usr/bin/python3 -m py_compile scripts/*.py`
  - `/opt/anaconda3/bin/python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .`
  - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_core_gates.py .` (no-PyYAML fallback)
  - `PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 scripts/validate_core_gates.py .` (PyYAML)
  - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_distribution.py .`
  - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 -m unittest discover -s tests -v` (main repo + clean-tree no-PyYAML fallback)
- [x] Run isolated read-only forward-test (2 scenarios: reject retirement of protected/single-model rule; respect `retired` tombstone without silent resurrection)
- [x] Pass independent read-only Implementation Review (`readonly-reviewer`, `same_instance=false`)
- [x] Execute 4-target (`codex`, `pi`, `antigravity-cli`, `grok-cli` with `grok inspect --json --consume`) schema-v2 scoped sync via `scripts/validate_cross_cli_sync.py` + `verify-all` (4 selected portable files, governance v6 unchanged)
- [x] Pass independent Final Review (`same_instance=false`, distinct from executor, inspecting final diff, fresh verification counts, and four-target `verify-all` evidence per `CCG-007` & `CCG-016`)
- [x] Update `CHANGELOG.md`, `docs/iteration/{BACKLOG,CURRENT,LOG}.md`, archive `add-sim-provenance-rule-retirement` with strict validation, run `scripts/check_commit_text.py`, commit & push only S11 files on `main` (excluding the 6 legacy dirty groups), and clean `/private/tmp/osc-*`
