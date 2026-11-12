# Tasks: harden-autoloop-pre-mr-gate

Author: elvis

## 1. Proposal and Contract

- [x] 1.1 Inspect `origin/main` (`534aa5851e34c1f5e98c85039d10f3f1ae852b88`), `openspec/specs/skill-workflow-governance/spec.md`, `references/self-evolution-rule.md`, and `references/cross-cli-portable-manifest.json`
- [x] 1.2 Draft `proposal.md`, `design.md`, `tasks.md`, and `specs/skill-workflow-governance/spec.md` under `openspec/changes/harden-autoloop-pre-mr-gate/`
- [x] 1.3 Run `openspec validate harden-autoloop-pre-mr-gate --strict` and halt before implementation awaiting explicit `已批准 harden-autoloop-pre-mr-gate`

## 2. Approved Implementation (Isolated Worktree from `origin/main` `534aa58`)

- [x] 2.1 Create isolated temporary structured backup (`/tmp/osc-backup-<ts>`) and isolated git worktree branched from `origin/main` (`534aa58`), copying the untracked `openspec/changes/harden-autoloop-pre-mr-gate/` directory from the primary checkout into the isolated worktree without touching primary checkout dirty files or historical `openspec/changes/integrate-governed-cli-autoloop/adapter/**`
- [x] 2.2 Write RED unit tests in `tests/test_gov_runner_git_capture.py` (5 core cases: clean committed branch diff + `git.log.txt`; detached unresolved baseline fail-closed; three-dot `<base>...HEAD` excluding target-only commits + union manifest; `> 2,000,000`-byte patch truncation fail-closed; generic `check_commit_text.py` hygiene + optional policy JSON decoupling)
- [x] 2.3 Implement `scripts/check_commit_text.py` and `references/autoloop-review-hunt.md`, and update `references/cross-cli-portable-manifest.json` + `references/autoloop-req-acceptance.md`
- [x] 2.4 Implement 3-tier local-ref baseline capture, `2_000_000`-byte ceiling, and deterministic pre/post-Pi fail-closed vetoes in `scripts/gov_runner.py`, plus `fast` / `pre-mr` flags and prompt routing in `scripts/autoloop_ctl.py`
- [x] 2.5 Rebuild generated `distribution/codex-plugin` via `python3 scripts/build_codex_plugin.py .`

## 3. Verification, Cross-CLI Sync, and Companion Local Rollout

- [x] 3.1 Run `quick_validate.py`, `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .`, `python3 -m unittest tests.test_gov_runner_git_capture`, `python3 -m unittest tests.test_workflow_rules`, `python3 scripts/validate_distribution.py`, plus 2 isolated forward probes (`fast` clean branch diff + `pre-mr` pre-Pi commit veto)
- [x] 3.2 Synchronize declared portable targets (`codex`, `pi`, `antigravity-cli`, `grok-cli`) and verify parity with `python3 scripts/validate_cross_cli_sync.py`; run independent read-only Implementation & Final Review
- [x] 3.3 Apply companion local user configurations outside open-source repo: workbench `commit-policy.json` + `个人负责项目Git提交与MR评审规范.md` (`v2.3`), `~/.codex/AGENTS.md` `ELVIS_USER_GLOBAL_SYNC` 4-line addition (`sync_user_global.py --apply --converge-skills && sync_user_global.py --check`), and `~/.codex/skills/autoloop/SKILL.md` alignment; clean up temporary backups
