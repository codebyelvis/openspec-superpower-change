# Change: Fuse Deterministic Verification Guardrails, Diagnosability Hunt Lens, and Learning Enforcement Hierarchy

Author: elvis. Revision: draft-v2. Status: approved (`迭代优化skill：已批准 fuse-harness-pstack-guardrails`).

## Why

Empirical runs of `/autoloop` and independent comparative reviews of `yezhwi/superpowers-engineering-harness` (`v0.3.2`) and `cursor/plugins/pstack` exposed five concrete gaps in `openspec-superpower-change` (on baseline `main` @ `7829572`):

1. **Daemon `PATH` shadowing, orphan timeout children, unshort-circuited verify failures, and collapsible/unredacted failure evidence (`scripts/autoloop_ctl.py`, `scripts/gov_runner.py`)**:
   - `agent-autoloop` runs under `launchd` with minimal `PATH=/usr/bin:/bin`, causing bare `python3` or `npm` verification commands to resolve to `/usr/bin/python3` (missing `PyYAML`) or fail with `127` even when the caller shell had a working toolchain.
   - `subprocess.run(..., shell=True, timeout=...)` neither isolates child process groups (leaving `mvn`/`pytest` grandchildren alive on timeout) nor catches `TimeoutExpired` into a structured receipt (`failure_kind = "timeout"`).
   - When `v_code != 0`, `gov_runner.py` still launches the read-only reviewer CLI, burning minutes of model quota on deterministic command failures, without classifying environment errors (`126`/`127`/`command not found`) vs code/test failures, redacting URL/JSON credentials in `verify_error_excerpt`, or computing a non-collapsing `failure_signature`.
2. **Zero-test false-PASS blind spot (`scripts/gov_runner.py`)**: A broken test selector (`Ran 0 tests`, `collected 0 items`, `Tests run: 0`, or pytest `-k` `deselected` exit `5`) either passes with `v_code == 0` when no positive test count ran across the full run, or falls into generic failure instead of `empty_test_execution`.
3. **Missing external/exception diagnosability hunt lens (`references/autoloop-review-hunt.md`)**: Conditional read-only hunt reviews lack a dedicated lens for swallowed root-cause exceptions, missing in-scope triage identifiers/status codes on external I/O failures, and raw credential logging—while merging such checks into Lens 4 would falsely trigger log nitpicks on pure in-memory branch changes.
4. **Unescalated high-risk business paths in `fast` mode (`scripts/gov_runner.py`, `scripts/autoloop_ctl.py`)**: Zero-argument `fast` runs modifying `db/migration/*.sql`, `auth*`, `security*`, or `permission*` business files stay at `-medium` without mounting `references/autoloop-review-hunt.md`.
5. **Missing repair convergence and mechanical learning hierarchy (`references/autoloop-req-acceptance.md`, `references/project-learning-closeout.md`)**: Auto-repair loops lack explicit `Attack the Premise` and identical-`failure_signature` early-stop rules, and learning closeout lacks an explicit 4-tier mechanical enforcement order under existing dual-signal and Major Self-Evolution prose guards.

## What Changes

- **F1 — Verification execution hardening (`scripts/autoloop_ctl.py`, `scripts/gov_runner.py`)**:
  - Pass caller `os.environ.get("PATH", "")` via `batch_payload["verify_env_path"]` into `gov_runner.py`'s verification subprocess environment.
  - Run verification in a new session (`subprocess.Popen(..., start_new_session=True)`), terminate the entire process group via `os.killpg(proc.pid, signal.SIGKILL)` on timeout (`v_code = 124`, `failure_kind = "timeout"`), and short-circuit before launching the read-only reviewer CLI (`cli_launched = False`) whenever `v_code != 0`.
  - Classify `failure_kind` deterministically into `"timeout"`, `"setup_or_env_error"` (strictly exit `126`/`127` or shell `command not found`, keeping `ImportError`/`ModuleNotFoundError` as `"verification_failed"`), `"empty_test_execution"` (including `v_code == 5` zero-collected or `-k` deselected runs), or `"verification_failed"`.
  - Redact sensitive values via greedy URL credential masking (`admin:p@ss@host` -> `admin:***@host`) and quote-aware key/value masking (covering JSON `"Authorization": "Bearer ..."` and `api_key`/`token`/`secret`/`password`) before writing `verify_error_excerpt`, and compute a 16-hex `failure_signature` from sorted unique failed test IDs (unittest/pytest/Maven Surefire) plus the first non-footer error line.
  - Enforce an aggregate positive-count-exempted zero-test execution veto when `v_code == 0` so multi-module runs with at least one positive test count pass while total zero-test runs fail closed before launching the reviewer CLI.
- **F2 — Fifth conditional hunt lens `diagnosability_context` (`references/autoloop-review-hunt.md`, `scripts/autoloop_ctl.py`)**:
  - Update `references/autoloop-review-hunt.md` header/scope for `pre-mr` and risk-escalated `fast` reviews, and add a 5th conditional lens (`diagnosability_context`) activated exclusively when a diff adds or alters external I/O calls or `catch`/`except` blocks (`hunt: n/a` otherwise).
- **F3 — Snapshot-sourced high-risk business path escalation (`scripts/gov_runner.py`, `scripts/autoloop_ctl.py`)**:
  - Scan `git.changed_files.txt` (single source of truth matching the reviewer's snapshot) excluding `docs`/`doc`/`test`/`tests`/`__tests__`/`fixtures` segments and root `*.md`; when `.sql`, high-risk directory segments, or filename stems starting with `("auth", "security", "permission", "migration")` match in `fast` mode, keep `review_profile == "fast"` (avoiding `--base-ref` errors), upgrade default model to `-high` when `--model` was not explicitly passed, mount `HUNT_REF.parent` via `--add-dir`, append `FAST_HUNT_ESCALATION_ADDENDUM`, and record `risk_escalated_paths` in `receipt.json`.
- **F4 — Repair convergence discipline (`references/autoloop-req-acceptance.md`)**:
  - Update the `FAIL` handling rule in `references/autoloop-req-acceptance.md` to fix environment setup on `setup_or_env_error`, stop immediately on two consecutive identical `failure_signature` values, require a one-sentence `Attack the Premise` check before a second code-repair attempt, and forbid dismissing same-scope `FAIL` findings that cite an exact diff `path:line` and concrete trigger path as "not reproduced locally".
- **F5 — Threshold-gated 4-tier learning enforcement hierarchy (`references/project-learning-closeout.md`)**:
  - Add a concise paragraph ordering durable promotions that already pass `## Triggers` and `references/learning-candidate-pipeline.md` as: (1) single-source-of-truth / dead-code removal, (2) pointer-bearing static validators/types, (3) observable behavior regression tests, and (4) prose guidance last, while preserving Major Self-Evolution approval and `Non-Negotiables` / validator-locked phrase protections.

## Scope and Non-Goals

- **Phase A in-scope files (current proposal & validation gate only)**:
  - `openspec/changes/fuse-harness-pstack-guardrails/proposal.md`
  - `openspec/changes/fuse-harness-pstack-guardrails/design.md`
  - `openspec/changes/fuse-harness-pstack-guardrails/tasks.md`
  - `openspec/changes/fuse-harness-pstack-guardrails/specs/skill-workflow-governance/spec.md`
- **Phase B in-scope files (strictly after `迭代优化skill：已批准 fuse-harness-pstack-guardrails`)**:
  - `scripts/autoloop_ctl.py`
  - `scripts/gov_runner.py`
  - `references/autoloop-review-hunt.md`
  - `references/autoloop-req-acceptance.md`
  - `references/project-learning-closeout.md`
  - `CHANGELOG.md`
  - `distribution/codex-plugin/**` (regenerated via `scripts/build_codex_plugin.py .`)
  - `tests/test_gov_runner_git_capture.py`
  - `tests/test_workflow_rules.py`
  - Post-sync, post-Final-Review, Git-authorized OpenSpec archive artifacts (`openspec/changes/archive/<date>-fuse-harness-pstack-guardrails/**` and `openspec/specs/skill-workflow-governance/spec.md`)
- **Non-goals & Forbidden Touches**:
  - Do NOT modify `SKILL.md`, `references/approved-implementation-workflow.md`, `scripts/validate_core_gates.py`, or `scripts/validate_cross_cli_sync.py`.
  - Do NOT adopt `.harness/*.yaml` state machines, `.publication-retained/` storage engines, blanket full-suite test bans, or Cursor-only `pstack` plugins.
  - Do NOT touch any of the 6 pre-existing unstaged/untracked repository paths (`OUT_OF_SCOPE_PREEXISTING_DEBT`: `docs/engineering-invariants.md`, `tests/test_external_grok_control_plane.py`, `openspec/changes/allow-one-external-grok-control-plane/**`, `docs/learning-candidates/2026-11-11-external-grok-control-plane-and-companion-closure.md`, `openspec/changes/archive/2026-11-11-allow-one-external-grok-control-plane/**`, `openspec/specs/external-grok-control-plane/**`).
  - Do NOT infer `git commit`, `git push`, or OpenSpec archive authority from `已批准 fuse-harness-pstack-guardrails` alone; Git and archive publication remain gated behind explicit user Git authorization after 4-target sync and Final Review.

## Impact

- **Affected specs**: `skill-workflow-governance`
- **Affected runtime targets (after Phase B validation & review)**: `codex`, `pi`, `antigravity-cli`, `grok-cli` via `scripts/validate_cross_cli_sync.py` (7 declared portable files on branch `main` vs `origin/main`), plus local `~/.agent-autoloop/plugins/govpi/gov_runner.py` on `autoloop_ctl.py ensure`
- **Compatibility**: `scripts/gov_runner.py` and `scripts/autoloop_ctl.py` remain Python 3.9.6 (`/usr/bin/python3`) compatible (`from __future__ import annotations`, stdlib-only, no Python 3.12 f-string backslash expressions)

## Approval Status

- Change-id presented to user: `fuse-harness-pstack-guardrails`
- Strict validation result: passed (`openspec validate fuse-harness-pstack-guardrails --strict`)
- [x] Proposal drafted with Major Self-Evolution review contract (`B1–B7`, `S1–S9`, and `R1–R9` embedded)
- [x] Phase A OpenSpec artifacts passed independent read-only review (`PASS`, Claude Opus 5.5)
- [x] This specific scoped change-id approved for implementation (`迭代优化skill：已批准 fuse-harness-pstack-guardrails`, with explicit user Git authorization granted for Step 3.6)
