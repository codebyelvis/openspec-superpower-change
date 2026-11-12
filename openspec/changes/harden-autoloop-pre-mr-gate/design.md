# Design: harden-autoloop-pre-mr-gate

Author: elvis

## Context

This change is classified as **Major Self-Evolution** under `references/self-evolution-rule.md` because it tightens evidence capture, deterministic signoff vetoes, and `status: passed` completion claims in `scripts/gov_runner.py` and `scripts/autoloop_ctl.py`.

Verified repository baseline on `origin/main` is `534aa5851e34c1f5e98c85039d10f3f1ae852b88` (which already matches the active `~/.codex/skills/openspec-superpower-change` runtime byte-for-byte, including `_is_ai_app_repo` worktree routing and `HEAD` inclusion in `git_fingerprint()`). Because the primary checkout currently sits at `38d9bee` with unrelated archive edits from another session, approved implementation MUST execute in an isolated git worktree created from `origin/main` (`534aa58`) and copy the untracked `openspec/changes/harden-autoloop-pre-mr-gate/` directory from the primary checkout into that isolated worktree without disturbing the primary working tree.

## Goals / Non-Goals

### Goals

- Capture accurate branch net diffs (`<base>...HEAD`), working-tree diffs, changed-file manifests, and full commit logs using only local Git refs (zero `git fetch`, zero target-branch guessing).
- Enforce deterministic Python fail-closed vetoes before/overriding Pi so empty diffs, unresolved `pre-mr` baselines, truncated patches (`> 2,000,000` bytes), or invalid commit messages never settle as `PASS`.
- Keep zero-argument `fast` `/autoloop` lightweight (`medium` reasoning, short prompt) while adding an opt-in/auto-escalated `pre-mr` profile (`high` reasoning, conditional hunt checklist with explicit `hunt: n/a` anti-bloat protection).
- Decouple portable commit checks (`scripts/check_commit_text.py`) from optional external policy JSON (`--commit-policy` + `--commit-profile`).

### Non-Goals

- Modifying `git_fingerprint()` to include `merge-base..HEAD` (which would falsely `BLOCK` read-only reviews if upstream refs move).
- Editing historical `openspec/changes/integrate-governed-cli-autoloop/adapter/**` or `~/.agent-autoloop/app/**`.
- Embedding personal/internal rules (e.g., 150-280 char counts, four-section Chinese headers, RFC1918 scans, or internal GitLab webhook semantics) as hardcoded defaults in open-source files.

## Decisions

### Decision 1: Three-Tier Local-Only Baseline Resolution & Structured Snapshot (`scripts/gov_runner.py`)

- **Decision**: Replace heuristic ref-looping (`origin/HEAD`, `origin/main`, `HEAD~1..HEAD`) and `[:200_000]` slicing with `capture_git_snapshot(work_cwd: str, raw: Path, base_ref: str = "", review_profile: str = "fast") -> dict`:
  0. **`pre-mr` explicit-base guard (`review_profile == "pre-mr"` and `not base_ref.strip()`)**: Immediately record `base_status = "missing_base_ref"` with empty `git.branch_diff.patch` / `git.log.txt` (do NOT enter Tier 2 `@{upstream}` / `Created from` or Tier 3 detached reflog, preventing `@{upstream}` on `origin/<short_branch>` from masking target-branch net diffs).
  1. **Tier 1 (`base_ref` provided)**: Verify `git rev-parse --verify <base_ref>^{commit}`. If verification fails, return `base_status = "invalid_base_ref"` (fail closed before Pi). Otherwise compute `merge_base = git merge-base <base_commit> HEAD`; branch net diff uses three-dot `git diff --find-renames <base_commit>...HEAD` (equivalent to `merge_base..HEAD`, excluding target-only commits), and commit log uses `git log --format=full <merge_base>..HEAD`.
  2. **Tier 2 (`fast` only; `base_ref` omitted, attached branch via `git symbolic-ref -q --short HEAD`)**:
     - First check `@{upstream}`: if `git rev-parse --verify @{upstream}^{commit}` succeeds and `merge_base = git merge-base HEAD @{upstream}` differs from `HEAD`, use `<merge_base>..HEAD` (unpushed commits on current branch).
     - Otherwise scan `git reflog show --format=%gs <branch>` from oldest creation entry (`branch: Created from <ref>`): pick the first entry whose `<ref>^{commit}` resolves locally, whose `merge_base = git merge-base HEAD <ref>` is an ancestor with `merge_base != HEAD`, and where `git rev-list --count <merge_base>..HEAD <= 50`.
  3. **Tier 3 (`fast` only; `base_ref` omitted, detached `HEAD`)**:
     - Scan `git log -g --format=%gs HEAD` for the latest `checkout: moving from <ref> to ...` or `reset: moving to <ref>` where `<ref>^{commit}` resolves locally, `<ref> != HEAD`, `git merge-base --is-ancestor <ref> HEAD` holds, and `git rev-list --count <ref>..HEAD <= 50`; use `<ref>..HEAD`.
  4. **Unresolved fallback (`fast` only)**: Never guess `origin/HEAD`, `origin/main`, `origin/feature/*`, or `HEAD~1..HEAD`. Record `base_status = "unresolved"` and write empty `git.branch_diff.patch` / `git.log.txt`.
- **Evidence files written to `raw` (`evidence_dir/run-<id>/attempt-<n>/`, never `work_cwd`)**:
  - `git.status.txt`: `git status -sb`
  - `git.changed_files.txt`: sorted union of `--name-status --find-renames` from `<base>...HEAD` (when resolved), `git diff --name-status HEAD`, and `git ls-files --others --exclude-standard` (prefixed `?\t<path>`)
  - `git.branch_diff.patch`: `git diff --find-renames <base>...HEAD`
  - `git.working_diff.patch` and `git.diff.patch` (retained as working-tree compatibility view): `git diff --find-renames HEAD`
  - `git.log.txt`: `git log --format=full <merge_base>..HEAD`
  - `git.meta.json`: `{base_status, requested_base_ref, resolved_base_sha, merge_base_sha, head_sha, detached, branch_commit_count, working_dirty, untracked_count, changed_file_count, branch_diff_bytes, working_diff_bytes, truncated}`
- **Patch ceiling**: `MAX_PATCH_BYTES = 2_000_000` per patch. Exceeding `2_000_000` bytes on either `branch_diff` or `working_diff` sets `truncated = True` in `git.meta.json`, writes at most `2_000_000` bytes for inspection, and triggers a deterministic fail-closed veto.

### Decision 2: Deterministic Pre-Pi and Post-Pi Signoff Vetoes (`scripts/gov_runner.py`)

- **Decision**: Evaluate deterministic snapshot & commit gates before launching Pi (and enforce them again when computing `passed`):
  1. `review_profile == "pre-mr"` and `--base-ref` is empty (`base_status == "missing_base_ref"`) -> deterministically settle as `FAIL` before launching Pi (`report.md` + `receipt.json` `verdict: "FAIL"`, skip Pi; Tier 2 `@{upstream}` / `Created from` and Tier 3 detached reflog apply exclusively to `fast`).
  2. `base_status == "invalid_base_ref"` -> deterministically fail closed before launching Pi (skip Pi).
  3. `truncated is True` -> deterministically fail closed before launching Pi (skip Pi).
  4. `review_profile == "pre-mr"` and `base_status != "resolved"` -> deterministically fail closed before launching Pi (skip Pi).
  5. Clean working tree (`not working_dirty and untracked_count == 0`) AND (`base_status != "resolved"` or `branch_diff_bytes == 0`) -> fail closed so empty or invisible commits can never be stamped `PASS` in either `fast` or `pre-mr`.
  6. `review_profile == "pre-mr"` with `commit_msg_file` or non-empty `git.log.txt` -> run `check_commit_text.py`; non-zero exit writes deterministic failure `report.md` and `receipt.json` (`verdict: "FAIL"`, `cli_launched: False`) without launching Pi.

### Decision 3: Portable Commit Checker + Optional Policy JSON (`scripts/check_commit_text.py`)

- **Decision**: Implement standalone stdlib CLI & importable module `scripts/check_commit_text.py`:
  - **Built-in generic checks (always active)**:
    - Header matches `^(feat|fix|refactor|perf|docs|test|build|chore)\(([^()\r\n]+)\):\s+\S+`;
    - Blank line after header followed by non-empty body;
    - Reject literal `\n` escape sequences in subject/body;
    - Reject `Co-authored-by:` trailers (case-insensitive);
    - Reject PEM private key headers and high-confidence secret token prefixes in commit message text and added diff lines (`+` lines excluding `+++`).
  - **External policy extension (`--commit-policy <path>` + `--commit-profile <profile>`)**:
    - If `--commit-policy` is omitted or the path does not exist, skip policy-specific checks (preserving zero-config open-source portability).
    - When the JSON file exists, validate optional `profiles.<profile>` (`min_body_chars`, `max_body_chars`, `required_headings`, `max_bullet_chars`) and `forbidden_added_line_patterns` (e.g., RFC1918 private address literals in user/workbench policy).

### Decision 4: `fast` vs `pre-mr` Split & Conditional Hunt Reference (`scripts/autoloop_ctl.py` + `references/autoloop-review-hunt.md`)

- **Decision**:
  - Extend `autoloop_ctl.py run` CLI with `--base-ref ""`, `--commit-msg-file ""`, `--commit-policy ""`, `--commit-profile "initial"`, and `--review-profile` (`""` -> `"pre-mr"` when `--commit-msg-file` is set, else `"fast"`).
  - **`fast` profile**: Keeps `antigravity/gemini-4-carbon:medium` default and short prompt pointing to `{RAW}/git.meta.json`, `{RAW}/git.changed_files.txt`, `{RAW}/git.branch_diff.patch`, `{RAW}/git.working_diff.patch`, and `{RAW}/git.log.txt`, adding only the non-negotiable rule that truncated/unresolved/empty diffs cannot `PASS`.
  - **`pre-mr` profile**: Upgrades default model thinking to `high` (`antigravity/gemini-4-carbon:high` when `--model` is not explicitly overridden) and instructs the read-only reviewer to apply `{SKILL_ROOT}/references/autoloop-review-hunt.md`.
  - **`references/autoloop-review-hunt.md` anti-bloat contract**:
    - Evaluates 4 conditional lenses (**Consumer Symmetry**, **Durable Side-Effect / Re-entry Idempotency**, **Pagination / Bounded-Budget Liveness**, **Target Baseline Counterfactual**) **only** when the diff touches matching code paths.
    - Requires outputting `hunt: n/a` for untouched categories; forbids failing for missing speculative guards, naming/style preferences, or pre-existing target-branch defects outside changed hunks.
    - Every `FAIL` finding must cite an exact `path:line` inside the current diff plus a concrete in-repo consumer or reachable retry/pagination/crash-reentry path.

## Exact Rule & Contract Snippets

- `references/cross-cli-portable-manifest.json` additions under `openspec-superpower-change.files`:
  - `{"path": "references/autoloop-review-hunt.md", "targets": ["codex", "pi", "antigravity-cli", "grok-cli"]}`
  - `{"path": "scripts/check_commit_text.py", "targets": ["codex", "pi", "antigravity-cli", "grok-cli"]}`
- `batch_payload` additions in `scripts/autoloop_ctl.py`:
  - `"review_profile": review_profile` (`"fast"` | `"pre-mr"`)
  - `"base_ref": args.base_ref.strip()`
  - `"commit_msg_file": str(Path(args.commit_msg_file).resolve()) if args.commit_msg_file else ""`
  - `"commit_policy": str(Path(args.commit_policy).expanduser().resolve()) if args.commit_policy else ""`
  - `"commit_profile": args.commit_profile.strip()`

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| `cmd_run` triggers `ensure_installed()` which copies `gov_runner.py` to `~/.agent-autoloop` and runs `launchctl kickstart -k` | Unit tests in `tests/test_gov_runner_git_capture.py` call `capture_git_snapshot`, `check_commit_text`, and isolated `gov_runner.py --batch` subprocesses directly in `tempfile` git repos without invoking `ensure_installed()` or real `launchd`. |
| New portable files missing from `distribution/codex-plugin` or runtime targets | Update `references/cross-cli-portable-manifest.json`, run `scripts/build_codex_plugin.py .`, `scripts/validate_distribution.py`, and `scripts/validate_cross_cli_sync.py`. |
| Detached `/tmp` worktrees in pre-MR workflows lack `Created from` reflog | Document and enforce passing `--base-ref origin/<target_branch>` for `pre-mr` runs while preserving Tier-3 checkout/reset reflog and dirty-worktree fallback for `fast` runs. |

## Validation & Forward-Test Plan

1. `python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py <worktree>`
2. `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .`
3. `python3 -m unittest tests.test_gov_runner_git_capture` (5 focused tests: committed clean-tree branch diff + `git.log.txt`; detached unresolved baseline fail-closed; three-dot `<base>...HEAD` excluding target-only commits + union manifest; `> 2,000,000` byte patch truncation fail-closed; generic commit check passing valid message, rejecting literal `\n` and `Co-authored-by:`, and not enforcing 150-char threshold when policy file is absent)
4. Two isolated forward probes (`stub` / isolated batch runner):
   - Fast-path: clean committed branch slice resolves baseline and exposes `git.branch_diff.patch` + `git.log.txt` to reviewer.
   - Strict-path: `pre-mr` with malformed commit message fails deterministically before launching Pi (`cli.argv.json` absent / `cli_launched: False`).
5. `python3 scripts/build_codex_plugin.py . && python3 scripts/validate_distribution.py && python3 scripts/validate_cross_cli_sync.py`

## Migration / Rollback

1. Create timestamped temporary structured backup of `~/.codex/skills/openspec-superpower-change` (outside `~/.codex/skills/` discovery path, e.g., `/tmp/osc-backup-<ts>`) before syncing runtime targets.
2. If any validation, forward-test, or independent review fails, restore runtime targets from `/tmp/osc-backup-<ts>` and discard the isolated implementation worktree; remove temporary backups only after all checks and sync verifications pass.
