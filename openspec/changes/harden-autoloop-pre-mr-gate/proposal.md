# Change: Harden Autoloop Git Baseline Capture, Deterministic Commit Veto, and Pre-MR Review Profile

Author: elvis. Revision: draft-v1. Status: proposed, pending `已批准 harden-autoloop-pre-mr-gate`.

## Why

`scripts/gov_runner.py` and `scripts/autoloop_ctl.py` currently allow false-PASS signoff and incomplete diff visibility before Merge Request creation:

1. **Heuristic baseline drift and empty-diff PASS (`scripts/gov_runner.py` on `origin/main` `534aa58`)**: `capture_git_snapshot()` loops `@{upstream}`, `origin/HEAD`, `origin/main`, and `origin/master` picking the minimum commit count `1 <= n <= 200`, or falls back to `HEAD~1..HEAD` when `git diff HEAD` is empty, and truncates patches silently at `200_000` bytes. On integration branches other than `main`, `origin/main` sweeps unrelated target-branch history into `git.diff.patch`; on already-pushed branches or clean target checkouts, `@{upstream}..HEAD` is empty and `HEAD~1..HEAD` inspects an upstream commit rather than the branch's net diff; in detached worktrees without upstream, baseline resolution is undefined. Worse, `launch()` marks `passed = (v_code == 0) and ("AUTOLOOP_VERDICT: PASS" in first_line ...)` solely from model text, allowing `autoloop_ctl.py` to stamp `status: passed` even on an empty, unresolved, or silently truncated diff.
2. **Undifferentiated review prompt (`scripts/autoloop_ctl.py`)**: A single generic prompt runs for both routine local loops and pre-MR signoff. Embedding heavy stateful/pagination/commit rules directly into the default prompt risks speculative false-FAILs on simple changes while still delegating deterministic commit-format checks to an LLM.
3. **Coupled commit rules**: Generic Conventional Commits / secret-leak hygiene and project- or user-specific length/section/network-address policies have no clean separation, preventing portable open-source reuse.

## What Changes

- Replace heuristic Git snapshot logic in `scripts/gov_runner.py` with a deterministic, local-ref-only baseline resolver (`pre-mr` requires explicit `--base-ref` and records `base_status=missing_base_ref` + pre-Pi deterministic `FAIL` when omitted; Tier 2 attached `@{upstream}` / `Created from` reflog and Tier 3 detached `HEAD` checkout/reset reflog apply exclusively to `fast`), emitting structured `git.meta.json`, `git.changed_files.txt`, `git.branch_diff.patch` (`<base>...HEAD`), `git.working_diff.patch`, backward-compatible `git.diff.patch`, and `git.log.txt` (`--format=full`), while enforcing a `2_000_000`-byte per-patch ceiling with `truncated=true` fail-closed veto instead of silent `200_000`-byte slicing.
- Preserve `git_fingerprint()` strictly as a read-only workspace mutation seal (`HEAD`, `git status --porcelain -z`, `git diff HEAD`, and untracked files) without mixing `merge-base..HEAD` or running `git fetch`.
- Add deterministic pre-Pi and post-Pi fail-closed vetoes in `scripts/gov_runner.py` so unresolved baselines (in `pre-mr` or clean-worktree `fast` runs), truncated patches, empty total diffs on clean worktrees, or failed commit checks settle as `FAIL` without trusting LLM `PASS` text.
- Add portable `scripts/check_commit_text.py` enforcing generic commit hygiene (Conventional Commits with non-empty scope, non-empty body, no literal `\n`, no `Co-authored-by:`, and no private-key / token-prefix leaks in commit text or added diff lines) plus optional `--commit-policy <json>` / `--commit-profile <name>` hooks for external length, section, and custom regex policies.
- Split `scripts/autoloop_ctl.py run` into `fast` (default `medium`, concise prompt, zero-arg compatible) and `pre-mr` (auto-selected when `--commit-msg-file` is supplied or `--review-profile pre-mr` is passed, defaulting to `high` reasoning and referencing `references/autoloop-review-hunt.md` with strict `hunt: n/a` anti-bloat guards).
- Register `scripts/check_commit_text.py` and `references/autoloop-review-hunt.md` in `references/cross-cli-portable-manifest.json`, update `references/autoloop-req-acceptance.md`, add stdlib unit tests in `tests/test_gov_runner_git_capture.py`, regenerate `distribution/codex-plugin`, and synchronize declared Codex, Pi, Antigravity CLI, and Grok CLI targets after approval.

## Scope and Non-Goals

- **In scope (`openspec-superpower-change`)**:
  - `scripts/gov_runner.py`
  - `scripts/autoloop_ctl.py`
  - `scripts/check_commit_text.py` (new)
  - `references/autoloop-req-acceptance.md`
  - `references/autoloop-review-hunt.md` (new)
  - `references/cross-cli-portable-manifest.json`
  - `tests/test_gov_runner_git_capture.py` (new)
  - Generated `distribution/codex-plugin/**` via `scripts/build_codex_plugin.py .`
- **Non-goals**:
  - Do not modify `CROSS_CLI_GOVERNANCE` version=6 managed block or `SKILL.md` autoload triggers.
  - Do not modify historical change fixture `openspec/changes/integrate-governed-cli-autoloop/adapter/gov_runner.py` or `~/.agent-autoloop/app/**`.
  - Do not hardcode personal word counts, four-section templates, internal webhook rules, or private IP patterns as default failures inside open-source scripts/prompts.
  - Do not touch unrelated dirty files in the primary repository checkout (`allow-one-external-grok-control-plane`); approved implementation runs in an isolated worktree branched from verified `origin/main` (`534aa5851e34c1f5e98c85039d10f3f1ae852b88`), carrying over the untracked `openspec/changes/harden-autoloop-pre-mr-gate/` directory from the primary checkout.

## Impact

- **Affected specs**: `skill-workflow-governance`
- **Affected code**: `scripts/{gov_runner.py,autoloop_ctl.py,check_commit_text.py}`, `references/{autoloop-req-acceptance.md,autoloop-review-hunt.md,cross-cli-portable-manifest.json}`, `tests/test_gov_runner_git_capture.py`, `distribution/codex-plugin/**`
- **Risks**: Over-strict baseline checks could block detached or dirty local `fast` runs if dirty-worktree fallback is omitted; mitigated by allowing dirty-worktree `git diff HEAD` in `fast` mode while failing closed on `pre-mr` or clean-worktree invisible diffs.

## Approval Status

- Change-id presented to user: `harden-autoloop-pre-mr-gate`
- Strict validation result: passed (`openspec validate harden-autoloop-pre-mr-gate --strict`)
- [x] Proposal drafted with Major Self-Evolution review contract
- [x] This specific scoped change-id approved for implementation (`已批准 harden-autoloop-pre-mr-gate`)
