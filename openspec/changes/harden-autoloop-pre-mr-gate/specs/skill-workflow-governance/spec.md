## ADDED Requirements

### Requirement: Deterministic local-ref baseline capture and fail-closed diff signoff in Autoloop runner

`scripts/gov_runner.py` SHALL resolve branch diff baselines exclusively from
local Git refs without invoking `git fetch` or guessing integration branch names
such as `origin/HEAD`, `origin/main`, `origin/feature/*`, or `HEAD~1..HEAD`.
When `review_profile` is `pre-mr` and `--base-ref` is empty, `gov_runner.py`
SHALL record `base_status` as `missing_base_ref` and deterministically settle as
`FAIL` before launching the read-only reviewer CLI. Otherwise, baseline
resolution SHALL follow a deterministic three-tier order: (1) an explicit
`--base-ref` verified as `<ref>^{commit}`, computing net branch changes via
three-dot `git diff --find-renames <base>...HEAD` and commit history via
`git log --format=full <merge-base>..HEAD`; (2) in `fast` mode only, when
`--base-ref` is omitted on an attached branch, `@{upstream}` when ahead of
upstream, otherwise the branch's resolvable `Created from <ref>` reflog entry
within a bounded 50-commit window; (3) in `fast` mode only, when `--base-ref` is
omitted on a detached `HEAD`, the latest resolvable ancestor from `HEAD`
checkout/reset reflog within a bounded 50-commit window; otherwise `base_status`
SHALL be recorded as `unresolved`.

All snapshot artifacts (`git.meta.json`, `git.status.txt`,
`git.changed_files.txt`, `git.branch_diff.patch`, `git.working_diff.patch`,
compatibility `git.diff.patch`, and `git.log.txt`) SHALL be written strictly
under the run's external `evidence_dir` and SHALL NOT mutate the target
repository. `git_fingerprint()` SHALL remain a read-only workspace seal over
`HEAD`, working-tree status/diff, and untracked files, and SHALL NOT incorporate
target-branch advancement. Each patch artifact SHALL enforce a `2,000,000`-byte
ceiling; exceeding that ceiling SHALL mark `truncated: true` and deterministically
veto `PASS` instead of silently truncating. A `missing_base_ref` in `pre-mr`
mode, an invalid `--base-ref`, a truncated patch, an `unresolved` baseline in
`pre-mr` mode, or a clean working tree with zero visible branch diff SHALL
deterministically settle as non-`PASS` regardless of model output text.

#### Scenario: Committed branch slice with clean working tree

- **WHEN** a developer commits changes on a local branch and runs Autoloop with a clean working tree and a resolvable baseline
- **THEN** `gov_runner.py` SHALL write the three-dot branch net diff to `git.branch_diff.patch`, full commit messages to `git.log.txt`, and the union changed-file manifest to `git.changed_files.txt`
- **AND** target-branch-only commits after the merge-base SHALL NOT appear in `git.branch_diff.patch`

#### Scenario: Unresolved detached worktree or empty clean diff cannot false-PASS

- **WHEN** `fast` mode runs on a detached `HEAD` without `--base-ref` or resolvable ancestor reflog, or the working tree is clean with zero visible branch diff
- **THEN** `gov_runner.py` SHALL record the deterministic failure reason and veto `PASS`
- **AND** `autoloop_ctl.py` SHALL NOT mark the requirement contract `status: passed`

#### Scenario: Pre-MR mode without explicit base-ref fails before reviewer launch

- **WHEN** `review_profile` is `pre-mr` and `--base-ref` is omitted or empty
- **THEN** `gov_runner.py` SHALL record `base_status` as `missing_base_ref` without falling back to Tier 2 `@{upstream}` / `Created from` or Tier 3 detached reflog
- **AND** the run SHALL deterministically settle as `FAIL` before launching the read-only reviewer CLI

#### Scenario: Oversized patch fails closed instead of silent truncation

- **WHEN** `git.branch_diff.patch` or `git.working_diff.patch` exceeds `2,000,000` bytes
- **THEN** `git.meta.json` SHALL record `truncated: true`
- **AND** the run SHALL deterministically fail closed without accepting a model `PASS` on a partial diff

### Requirement: Two-tier Autoloop review profiles and portable commit hygiene gate

`scripts/autoloop_ctl.py run` SHALL support `fast` (default) and `pre-mr` review
profiles, automatically selecting `pre-mr` when `--commit-msg-file` is supplied.
`fast` mode SHALL preserve the lightweight review prompt for routine loops while
enforcing non-empty/non-truncated diff preconditions. `pre-mr` mode SHALL invoke
portable commit checks via `scripts/check_commit_text.py` before launching the
read-only reviewer CLI when commit text is present, and SHALL reference
`references/autoloop-review-hunt.md` so stateful Safety, pagination/budget
Liveness, consumer symmetry, and target counterfactual checks apply only when
matching mechanisms exist in the diff (`hunt: n/a` otherwise, without style or
speculative-defense false positives).

Built-in checks in `scripts/check_commit_text.py` SHALL enforce only portable
hygiene (Conventional Commits header with non-empty scope, non-empty body, no
literal `\n` escapes, no `Co-authored-by:` trailer, and no private-key or
secret-token markers in commit text or added diff lines). Project- or
user-specific length bounds, required section headings, and private network
address patterns SHALL be loaded exclusively from an optional `--commit-policy`
JSON file paired with `--commit-profile`, and SHALL be skipped when no policy
file is present.

#### Scenario: Malformed commit fails before launching read-only reviewer

- **WHEN** `autoloop_ctl.py run` executes in `pre-mr` mode with a commit message containing literal `\n`, `Co-authored-by:`, or missing Conventional Commits scope/body
- **THEN** `check_commit_text.py` SHALL fail deterministically before launching the read-only reviewer CLI
- **AND** no model invocation SHALL override that failure into `PASS`

#### Scenario: Portable default without external commit policy file

- **WHEN** `check_commit_text.py` runs without `--commit-policy` or the specified policy path is absent
- **THEN** generic Conventional Commits and secret-hygiene rules SHALL still run
- **AND** personal character-count or four-section rules SHALL NOT cause a valid concise commit message to fail
