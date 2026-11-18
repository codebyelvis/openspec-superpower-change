# Tasks: fuse-harness-pstack-guardrails

Author: elvis

## 1. Phase A: Proposal and Strict Validation

- [x] 1.1 Distill `superpowers-engineering-harness` (`v0.3.2`) and `cursor/plugins/pstack` against `openspec-superpower-change` (`main` @ `7829572`), complete independent `FULL_PREFLIGHT` (`B1–B7`, `S1–S9`) and `FOCUSED_RECHECK` (`R1–R9`) design revisions, and verify Python 3.9 regex/helper compatibility
- [x] 1.2 Draft `proposal.md`, `design.md`, `tasks.md`, and `specs/skill-workflow-governance/spec.md` under `openspec/changes/fuse-harness-pstack-guardrails/` and pass `openspec validate fuse-harness-pstack-guardrails --strict`
- [x] 1.3 Run independent read-only review on Phase A OpenSpec artifacts and halt awaiting explicit user approval (`迭代优化skill：已批准 fuse-harness-pstack-guardrails`) before any Phase B edits

## 2. Phase B: Approved Implementation (Pending `迭代优化skill：已批准 fuse-harness-pstack-guardrails`)

- [x] 2.1 Verify/refresh structured temporary 4-target backup under `/tmp/osc-self-evo-backup-<ts>` (outside skill discovery directories) while leaving all 6 `OUT_OF_SCOPE_PREEXISTING_DEBT` paths untouched
- [x] 2.2 Write RED unit tests in `tests/test_gov_runner_git_capture.py` and `tests/test_workflow_rules.py` covering `B4/R5` (`127` vs `ModuleNotFoundError` vs `killpg` timeout `124` + `cli_launched=False`), `B5/R8` (`Ran 0 tests` veto, multi-module positive-count exemption, pytest `v_code == 5` `collected 0 items` & `deselected`), `R1` (distinct unittest failure signatures despite `FAILED (failures=1)` footer), `R2` (zero residual substring leak for `admin:p@ss@host` and JSON `"Authorization": "Bearer ..."`), `B6/S5/R6/R7` (snapshot-sourced escalation for `.sql`, high-risk segments, and `auth/security/permission/migration` filename stems), `S6` (`verify_env_path`), and `F2/F4/F5` reference rules
- [x] 2.3 Implement `F1` and `F3` in `scripts/gov_runner.py` and `scripts/autoloop_ctl.py` following the exact Python 3.9-compatible snippets in `design.md`
- [x] 2.4 Update `references/autoloop-review-hunt.md` (`F2`), `references/autoloop-req-acceptance.md` (`F4`, zero changes to `approved-implementation-workflow.md`), `references/project-learning-closeout.md` (`F5`), and `CHANGELOG.md`, then regenerate `distribution/codex-plugin` via `python3 scripts/build_codex_plugin.py .`
- [x] 2.5 Run `/usr/bin/python3 -m py_compile scripts/gov_runner.py scripts/autoloop_ctl.py scripts/check_commit_text.py`, construct clean snapshot tree `/tmp/osc-clean-verify-<ts>` (`git archive HEAD` + allowed Phase B files), and pass `quick_validate.py`, `validate_core_gates.py`, `validate_distribution.py`, and full `unittest discover -s tests -v`
- [x] 2.6 Execute the 2 isolated Forward-Test probes in `/tmp/osc-forward-test-<ts>` (zero-test false-PASS veto + clean-branch `db/migration/*.sql` `fast` escalation) and explicit `--req openspec/changes/fuse-harness-pstack-guardrails/proposal.md --cmd "<validation-cmd>"` self-check

## 3. Independent Reviews, Cross-CLI Sync, and Git-Authorized Archive Closeout (`R3` / `R4` Order)

- [x] 3.1 Run independent Implementation Review uniquely bound to `agent_product: antigravity-cli` (`/Users/elvis/.gemini/antigravity-cli/bin/agy-readonly-review --model gemini-4-carbon-high --output-format stream-json --disable-slash-commands --add-dir /private/tmp`), recording executor session ID and distinct reviewer `conversation_id` (`same_instance=false`) until `PASS`
- [x] 3.2 Complete Project Learning Closeout audit against `docs/engineering-invariants.md` (read-only; do NOT modify unstaged dirty `docs/engineering-invariants.md`) and `references/project-learning-closeout.md`
- [x] 3.3 Run Fresh Final Verification across `quick_validate.py`, `validate_core_gates.py`, `validate_distribution.py`, and full `unittest discover -s tests -v` on a fresh clean snapshot tree
- [x] 3.4 Execute 4-target Cross-CLI Sync (`scripts/validate_cross_cli_sync.py plan` with `--manifest references/cross-cli-portable-manifest.json` and the 7 declared changed portable files in `--select-file` -> `verify-prestate --target all` -> inspect plan/snapshots -> per-target `apply`, `verify`, `verify-discovery`, `commit-target` across `codex`, `pi`, `antigravity-cli`, `grok-cli` -> `verify-all`)
- [x] 3.5 Run independent Final Review uniquely bound to `agent_product: antigravity-cli` (`agy-readonly-review --model gemini-4-carbon-high`, fresh distinct `conversation_id`, `same_instance=false`) over full net diff, Fresh Final Verification evidence, and `verify-all` sync receipts until `PASS`
- [x] 3.6 Enforce Explicit Git Authorization & Archive Gate (`R3`): if explicit user Git authorization is not yet granted, keep `fuse-harness-pstack-guardrails` active with `owner: user` and `resume_condition: explicit git commit and push authorization`; once explicitly authorized, run exact-path `git add` -> `check_commit_text.py` -> `git commit` -> clean `git worktree add` verification -> reconcile & archive `fuse-harness-pstack-guardrails` into `openspec/changes/archive/` and `openspec/specs/skill-workflow-governance/spec.md` -> post-archive `openspec validate --strict` + focused independent Review & commit -> `git push origin main` -> clean up `/tmp` backups and scratch directories
