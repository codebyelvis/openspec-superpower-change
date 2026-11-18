# Design: fuse-harness-pstack-guardrails

Author: elvis

## Context

This change is classified as **Major Self-Evolution** under `references/self-evolution-rule.md` because it modifies deterministic verification vetoes, failure classification/receipt fields, conditional high-risk review escalation, repair-loop stopping rules, and learning-closeout promotion guidance in `openspec-superpower-change`.

Repository baseline is local `main` @ `7829572` (1 commit ahead of `origin/main` `b8876b8`, 503 unit tests green). The primary checkout also contains 6 pre-existing unstaged/untracked paths from an earlier session (`allow-one-external-grok-control-plane`), treated strictly as `OUT_OF_SCOPE_PREEXISTING_DEBT` and never staged, reverted, or modified. Both preliminary design reviews (`FULL_PREFLIGHT` B1–B7 / S1–S9 and `FOCUSED_RECHECK` R1–R9 in `docs/design/2026-11-18-harness-pstack-fusion-plan-review.md`) have been resolved and empirically verified on macOS `/usr/bin/python3` (Python 3.9.6).

## Goals / Non-Goals

### Goals

- Preserve caller `PATH` across `launchd` boundaries, kill timed-out verification process groups cleanly without orphan `mvn`/`pytest` processes, and short-circuit deterministic verification failures before launching the read-only reviewer CLI.
- Provide non-collapsing `failure_signature` hashes (distinguishing distinct failing test cases that share identical summary footers) and leak-free `verify_error_excerpt` redaction (handling `@` inside URL passwords and quoted JSON keys).
- Catch zero-test false-PASS runs (`v_code == 0` with zero positive test counts across the full output, and `v_code == 5` pytest zero-selected/deselected exits) without penalizing multi-module runs where some modules have 0 tests and others pass `>= 1` test.
- Add a focused 5th conditional hunt lens (`diagnosability_context`) and automatically escalate `fast` reviews touching high-risk SQL/migration/auth/security/permission business files using `git.changed_files.txt` as the single source of truth.
- Codify `Attack the Premise` + identical-signature early stop in `/autoloop` repair loops and a 4-tier mechanical enforcement hierarchy in `project-learning-closeout.md` without touching `SKILL.md` or `approved-implementation-workflow.md`.

### Non-Goals

- Introducing `.harness/` repository state files, `NO_PROGRESS` state-machine enums in `approved-implementation-workflow.md`, or `.publication-retained/` storage directories.
- Modifying `SKILL.md`, `references/approved-implementation-workflow.md`, `scripts/validate_core_gates.py`, `scripts/validate_cross_cli_sync.py`, or any `OUT_OF_SCOPE_PREEXISTING_DEBT` path.
- Archiving the OpenSpec change before 4-target cross-CLI sync, independent Final Review, and explicit user Git authorization.

## Four Hard Anchors

1. **Anchor 1 — Allowed Scope**:
   - Phase A: `openspec/changes/fuse-harness-pstack-guardrails/{proposal.md,design.md,tasks.md,specs/skill-workflow-governance/spec.md}` only.
   - Phase B (after `迭代优化skill：已批准 fuse-harness-pstack-guardrails`): `scripts/{autoloop_ctl.py,gov_runner.py}`, `references/{autoloop-review-hunt.md,autoloop-req-acceptance.md,project-learning-closeout.md}`, `CHANGELOG.md`, generated `distribution/codex-plugin/**`, `tests/{test_gov_runner_git_capture.py,test_workflow_rules.py}`, and—only after explicit Git authorization—OpenSpec reconciliation/archive files.
2. **Anchor 2 — Forbidden Scope**:
   - `SKILL.md`, `references/approved-implementation-workflow.md`, `scripts/validate_core_gates.py`, `scripts/validate_cross_cli_sync.py`, historical `openspec/changes/integrate-governed-cli-autoloop/**`, and all 6 `OUT_OF_SCOPE_PREEXISTING_DEBT` paths.
3. **Anchor 3 — Execution Sequence (R3 & R4 Compliant)**:
   - Phase A (`openspec validate fuse-harness-pstack-guardrails --strict` + independent Phase A review + stop) $\rightarrow$ User explicit `迭代优化skill：已批准 fuse-harness-pstack-guardrails` $\rightarrow$ Step B1 Backup $\rightarrow$ Step B2 RED-to-GREEN + `build_codex_plugin.py` $\rightarrow$ Step B3 Python 3.9 `py_compile` + clean-snapshot-tree full suite + isolated Forward-Tests $\rightarrow$ Step B4 Independent Implementation Review (`antigravity-cli` / `agy-readonly-review`) $\rightarrow$ Step B5 Project Learning Closeout audit $\rightarrow$ Step B6 Fresh Final Verification $\rightarrow$ Step B7 4-Target Cross-CLI Sync (`plan` -> `verify-prestate` -> per-target `apply/verify/verify-discovery/commit-target` -> `verify-all`) $\rightarrow$ Step B8 Independent Final Review (`antigravity-cli` / `agy-readonly-review`) $\rightarrow$ Step B9 Explicit Git Authorization Gate (keep change active if unauthorized; once authorized, commit implementation -> clean `git worktree` verification -> OpenSpec archive + `openspec validate --strict` + focused archive Review & commit -> `git push origin main` -> cleanup backups).
4. **Anchor 4 — Acceptance & Evidence Oracle**:
   - Zero syntax errors under `/usr/bin/python3 -m py_compile`; zero errors in `quick_validate.py`, `validate_core_gates.py`, `validate_distribution.py`, full stdlib `unittest discover -s tests -v` on clean snapshot tree, 2 isolated forward-tests, `validate_cross_cli_sync.py verify-all`, and `PASS` verdicts from distinct `agy-readonly-review` instances (`same_instance=false`).

## Decisions

### Decision 1: Caller `PATH` Passthrough, Process-Group Timeout Kill, Pre-CLI `v_code != 0` Short-Circuit, Redaction & Non-Collapsing Signature (`F1` + `B4/B5/S6/R1/R2/R5/R8`)

- **Caller `PATH` passthrough (`S6`)**: `autoloop_ctl.py run` writes `"verify_env_path": os.environ.get("PATH", "")` into `batch_payload` (capturing `PATH` only, never dumping full caller environment secrets). `_run_verify_command()` in `gov_runner.py` overrides `env["PATH"]` when `verify_env_path` is non-empty.
- **Process-group timeout isolation (`R5`)**: `_run_verify_command()` spawns `subprocess.Popen(..., start_new_session=True)`. On `subprocess.TimeoutExpired`, it sends `os.killpg(proc.pid, signal.SIGKILL)` (ignoring `ProcessLookupError`), reaps `proc.wait()`, and returns `(124, True)`.
- **Pre-CLI short-circuit and 4-way `failure_kind` (`B4`, `B5`, `R8`)**:
  - When `v_code != 0`, `gov_runner.py` writes `verify.exit`, captures Git snapshot metadata if requested, skips launching the read-only reviewer CLI (`cli_launched = False`), and settles deterministically as `FAIL`:
    1. `timed_out` (`v_code == 124`) $\rightarrow$ `failure_kind = "timeout"`;
    2. `v_code in (126, 127)` or `SHELL_CMD_MISSING_RE` in combined stdout/stderr $\rightarrow$ `failure_kind = "setup_or_env_error"` (`ImportError` / `ModuleNotFoundError` exit `1` remains `"verification_failed"`);
    3. `v_code == 5` and (`ZERO_TEST_EXEC_RE` or `PYTEST_DESELECTED_EXIT5_RE` matching `0 selected` / `\d+ deselected`) $\rightarrow$ `failure_kind = "empty_test_execution"`;
    4. Otherwise $\rightarrow$ `failure_kind = "verification_failed"`.
  - When `v_code == 0`, `evaluate_deterministic_vetoes(batch, snap_meta, raw)` (retaining its 3-parameter signature and reading `raw / "verify.exit"`) checks combined `verify.stdout` + `verify.stderr`: if `not POSITIVE_TEST_COUNT_RE.search(combined)` and `ZERO_TEST_EXEC_RE.search(combined)`, it appends a deterministic zero-test execution veto (`failure_kind = "empty_test_execution"`, `cli_launched = False`).
- **Sensitive excerpt redaction (`R2`) & non-collapsing signature (`R1`)**:
  - `_redact_sensitive_text()` applies greedy `URL_CRED_REDACT_RE` (matching up to the `@` immediately preceding the host so `admin:p@ss@127.0.0.1` masks cleanly to `admin:***@127.0.0.1`) and quote-aware `SECRET_REDACT_RE` (covering JSON `"Authorization": "Bearer ..."` and `api_key`/`token`/`secret`/`password`/`passwd`) before slicing to 1200 chars.
  - `_compute_failure_signature()` extracts sorted unique failing test identifiers across unittest (`FAIL:`/`ERROR:`), pytest (`FAILED`), and Maven Surefire (`[ERROR] Class#method` / `Class:line`) plus the **first** non-footer error line (skipping `SUMMARY_FOOTER_RE`), normalizes timestamps, durations, hex addresses, and `/tmp` or `/var/folders` paths, and hashes `f"{failure_kind}|{v_code}|{joined_ids}|{norm}"` with SHA-256 (`[:16]`).

### Decision 2: Separate 5th Hunt Lens & Snapshot-Sourced `fast` High-Risk Escalation (`F2` + `F3` + `B6/S1/S5/R6/R7`)

- **Separate 5th lens (`F2`, confirmed in `FOCUSED_RECHECK` §6.2)**: Keep `diagnosability_context` as Lens 5 in `references/autoloop-review-hunt.md` rather than merging into Lens 4, because Lens 4 activates on any conditional branch/bugfix whereas Lens 5 activates strictly on external I/O (`HTTP/RPC/DB/MQ/CLI`) or `catch`/`except` blocks.
- **Snapshot-sourced `fast` escalation (`F3` + `B6/S5/R6/R7`)**:
  - In `gov_runner.py`, after `capture_git_snapshot()` writes `raw / "git.changed_files.txt"` and deterministic pre-CLI vetoes pass, when `review_profile == "fast"`, `_detect_escalated_paths_from_changed_file(raw / "git.changed_files.txt")` inspects the exact changed-file union seen by the reviewer.
  - Paths containing `NON_BUSINESS_SEGMENTS` (`docs`, `doc`, `test`, `tests`, `__tests__`, `fixtures`) or root-level `*.md` are excluded. Remaining paths escalate when ending in `.sql`, containing any `HIGH_RISK_SEGMENTS` directory/file segment (`migration`, `migrations`, `changelog`, `auth`, `authn`, `authz`, `oauth`, `security`, `permission`, `permissions`), or having `Path(norm_rel).stem.lower().startswith(("auth", "security", "permission", "migration"))`.
  - On non-empty `risk_escalated_paths`: keep `review_profile == "fast"` (no `--base-ref` failure), upgrade default reviewer model to `-high` when `not batch.get("model_explicit")` (rewriting `-medium` -> `-high` on `--model` in `pi_cmd`, or `--thinking medium` -> `high` for legacy `pi`), append `batch.get("hunt_dir")` to `extra_read_dirs` for `--add-dir`, append `FAST_HUNT_ESCALATION_ADDENDUM` (formatted with `batch.get("hunt_ref")`) to `prompt`, and persist `risk_escalated_paths` in `receipt.json`.

### Decision 3: Scoped Prose Refinements Only (`F4` + `F5` + `S2/S3/S4`)

- Leave `references/approved-implementation-workflow.md` and `SKILL.md` completely untouched (`S2`).
- Update line 55 of `references/autoloop-req-acceptance.md` (`S3`) and append one threshold-gated paragraph after line 136 of `references/project-learning-closeout.md` (`S4`) without deleting any validator-locked text in `scripts/validate_core_gates.py:2491-2510` or `tests/test_workflow_rules.py`.

## Exact Rule & Code Snippets

### 1. `references/autoloop-review-hunt.md`

Replace lines 1–10 with:
```markdown
# Conditional Read-Only Hunt Reference (`pre-mr` & Risk-Escalated `fast`)

Author: elvis

Use this reference in `pre-mr` read-only reviews and in `fast` reviews escalated by high-risk business paths. Keep strict Scope Lock and Anti-Bloat discipline:

1. **Changed-Hunk Attribution Only**: Every `FAIL` finding MUST anchor to an exact `path:line` modified in `git.branch_diff.patch` or `git.working_diff.patch`, and prove a concrete failure path that did not exist on the target baseline before this change.
2. **Conditional Activation (`hunt: n/a`)**: Evaluate each lens below **only** when the diff actually touches that mechanism. When a lens does not apply to the diff, record `hunt: n/a` for that lens. Never fail a change for "missing defensive guards" without a real in-repo caller or reachable runtime trigger, never emit naming/formatting/style nitpicks, and never report untouched pre-existing issues on the target branch.

## Five Conditional Hunt Lenses
```

Append after line 35:
```markdown

5. **External & Exception Diagnosability (`diagnosability_context`)**
   - **Activate when**: Diff adds or alters external I/O calls (HTTP/RPC/DB/MQ/CLI) or `catch`/`except` error-handling blocks.
   - **Check**:
     - Error paths must not silently swallow root-cause exceptions or log external/state failures without an available in-scope business identifier or error status/code needed for production triage;
     - Logs and error payloads must never output raw credentials, tokens, secrets, or connection passwords.
```

### 2. `references/autoloop-req-acceptance.md` (replace line 55)

```markdown
- On `"verdict": "FAIL"`, inspect `failure_kind`, `failure_signature`, and `report_path`: if `failure_kind == "setup_or_env_error"`, fix the command/PATH environment rather than mutating product code; stop immediately if two consecutive runs produce the identical `failure_signature`; before a second code-repair attempt, state in one sentence and directly check the shared premise assumed by the first failed fix (`Attack the Premise`). Never dismiss a same-scope `FAIL` finding that cites an exact diff `path:line` and concrete trigger path merely as "not reproduced locally" (at most 2 auto-repair rounds before stopping to report).
```

### 3. `references/project-learning-closeout.md` (append after line 136, zero deletions)

```markdown

When an item already meets the mandatory `## Triggers` threshold above and passes `references/learning-candidate-pipeline.md` scope classification, prefer the highest feasible enforcement layer: (1) architectural single-source-of-truth or dead-code removal so agents cannot copy obsolete patterns, (2) static validators or types whose error message names the canonical replacement, (3) observable behavior regression tests, and (4) prose guidance last for judgment-only boundaries. Any condensation or retirement of governed skill/workflow prose remains subject to Major Self-Evolution approval and must never remove `Non-Negotiables` or validator-locked phrases.
```

### 4. `scripts/autoloop_ctl.py` Additions

```python
# cmd_run() pre-mr prompt final bullet:
"- 每个 `FAIL` 发现必须同时给出本次 Diff 内的准确 `path:line`，以及仓库内真实消费者或可达的重试/分页/崩溃重入/异常黑盒触发路径。"

# batch_payload additions:
"verify_env_path": os.environ.get("PATH", ""),
"model_explicit": bool((args.model or "").strip()),
"hunt_ref": str(HUNT_REF.resolve()),
"hunt_dir": str(HUNT_REF.parent.resolve()) if HUNT_REF.parent.is_dir() else "",

# collect_result() receipt projections:
"cli_launched": rc.get("cli_launched", True),
"failure_kind": rc.get("failure_kind"),
"failure_signature": rc.get("failure_signature"),
"veto_errors": rc.get("veto_errors") or [],
"verify_error_excerpt": rc.get("verify_error_excerpt", ""),
"risk_escalated_paths": rc.get("risk_escalated_paths") or [],
```

### 5. `scripts/gov_runner.py` Core Helpers & Constants (Python 3.9 Verified)

```python
POSITIVE_TEST_COUNT_RE = re.compile(
    r"(?:\bRan\s+[1-9]\d*\s+tests?\b|\bTests\s+run:\s*[1-9]\d*\b|\b[1-9]\d*\s+passed\b)"
)
ZERO_TEST_EXEC_RE = re.compile(
    r"(?:\bRan\s+0\s+tests?\s+in\b|\bcollected\s+0\s+items\b|\bTests\s+run:\s*0\s*,|"
    r"===\s*no\s+tests\s+ran\b|\bNO\s+TESTS\s+RAN\b|\bThere\s+are\s+no\s+tests\s+to\s+run\b)",
    re.I,
)
PYTEST_DESELECTED_EXIT5_RE = re.compile(r"(?:\b0\s+selected\b|\b\d+\s+deselected\b)", re.I)
SHELL_CMD_MISSING_RE = re.compile(
    r"(?:command\s+not\s+found|not\s+recognized\s+as\s+an\s+internal\s+or\s+external\s+command)",
    re.I,
)
QUOTED_SECRET_REDACT_RE = re.compile(
    r"(?i)(\b(?:token|secret|password|passwd|authorization|api[_-]?key)\b[\"\']?\s*[:=]\s*)([\"\'])(?:Bearer\s+)?([^\"\'\r\n]+)(\2)"
)
SECRET_REDACT_RE = re.compile(
    r"(?i)(\b(?:token|secret|password|passwd|authorization|api[_-]?key)\b[\"\']?\s*[:=]\s*(?:Bearer\s+)?)([^\s\"\',;}\r\n]+)"
)
URL_CRED_REDACT_RE = re.compile(r"(://[^/\s:@]+:)([^\s/]+)(@[^@\s/]+)")
FAILED_ID_PATTERNS = (
    re.compile(r"^(?:FAIL|ERROR):\s+(\S+(?:\s+\([^)]+\))?)", re.M),
    re.compile(r"^FAILED\s+(\S+)", re.M),
    re.compile(r"^\[ERROR\]\s+([A-Za-z0-9_.$]+(?:#\S+|\(\S+\)|:\d+))", re.M),
)
SUMMARY_FOOTER_RE = re.compile(
    r"^(?:FAILED\s+\(|=+\s+.*failed|\[ERROR\]\s+BUILD\s+FAILURE\b)", re.I
)
HIGH_RISK_SEGMENTS = frozenset(
    {"migration", "migrations", "changelog", "auth", "authn", "authz", "oauth", "security", "permission", "permissions"}
)
# Conservative prefix trade-off: e.g. author_profile.py may also escalate to -high (safe extra compute, zero false-PASS risk).
HIGH_RISK_STEM_PREFIXES = ("auth", "security", "permission", "migration")
NON_BUSINESS_SEGMENTS = frozenset({"docs", "doc", "test", "tests", "__tests__", "fixtures"})

FAST_HUNT_ESCALATION_ADDENDUM = (
    "\n\n补充材料（高敏业务路径自动升档核查）：\n"
    "5. 条件猎杀清单：`{HUNT_REF}`\n"
    "升档附加规则：\n"
    "- 第 2 行起除 Findings First 外，必须附带 `hunt:` 适用性摘要；严格按条件猎杀清单核查本次变更触及的路径，未触及的类别记录 `hunt: n/a`，严禁因“未加无依据防御代码”、命名/格式偏好或目标分支未触碰旧问题判 `FAIL`。\n"
    "- 每个 `FAIL` 发现必须同时给出本次 Diff 内的准确 `path:line`，以及仓库内真实消费者或可达的重试/分页/崩溃重入/异常黑盒触发路径。"
)


def _redact_sensitive_text(text: str, limit: int = 1200) -> str:
    masked = URL_CRED_REDACT_RE.sub(r"\1***\3", text or "")
    masked = QUOTED_SECRET_REDACT_RE.sub(r"\1\2***\4", masked)
    masked = SECRET_REDACT_RE.sub(r"\1***", masked)
    return masked[-limit:] if len(masked) > limit else masked


def _compute_failure_signature(failure_kind: str, v_code: int, raw_output: str) -> str:
    failed_ids = sorted(
        {m.strip() for pat in FAILED_ID_PATTERNS for m in pat.findall(raw_output or "")}
    )
    key_line = ""
    for ln in (x.strip() for x in (raw_output or "").splitlines() if x.strip()):
        if SUMMARY_FOOTER_RE.match(ln):
            continue
        if any(tok in ln for tok in ("AssertionError", "Error", "Exception", "FAILED", "ERROR", "command not found", "exit")):
            key_line = ln
            break
    if not key_line and raw_output:
        non_footer = [
            x.strip()
            for x in raw_output.splitlines()
            if x.strip() and not SUMMARY_FOOTER_RE.match(x.strip())
        ]
        key_line = non_footer[0] if non_footer else ""
    norm = re.sub(r"\b\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?\b", "<ts>", key_line)
    norm = re.sub(r"\b\d+\.\d+s\b", "<dur>", norm)
    norm = re.sub(r"0x[0-9a-fA-F]+", "<addr>", norm)
    norm = re.sub(r"(?:/private)?/(?:tmp|var/folders)/\S+", "<tmp>", norm)
    joined_ids = ";".join(failed_ids)
    return hashlib.sha256(f"{failure_kind}|{v_code}|{joined_ids}|{norm}".encode("utf-8")).hexdigest()[:16]


def _detect_escalated_paths_from_changed_file(changed_txt: Path) -> list[str]:
    if not changed_txt.is_file():
        return []
    matched: list[str] = []
    for raw_line in changed_txt.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = raw_line.split("\t")
        rel = (parts[-1] if parts else "").strip()
        if not rel or ("/" not in rel and rel.lower().endswith(".md")):
            continue
        norm_rel = rel.replace("\\", "/")
        segs = [s.lower() for s in norm_rel.split("/") if s]
        if any(s in NON_BUSINESS_SEGMENTS for s in segs):
            continue
        stem = Path(norm_rel).stem.lower()
        if (
            norm_rel.lower().endswith(".sql")
            or any(s in HIGH_RISK_SEGMENTS for s in segs)
            or stem.startswith(HIGH_RISK_STEM_PREFIXES)
        ):
            matched.append(rel)
    return sorted(set(matched))


def _run_verify_command(v_cmd, work_cwd: str, timeout_sec: int, verify_env_path: str, v_out, v_err) -> tuple[int, bool]:
    env = dict(os.environ)
    if (verify_env_path or "").strip():
        env["PATH"] = verify_env_path.strip()
    proc = subprocess.Popen(
        v_cmd,
        shell=isinstance(v_cmd, str),
        cwd=work_cwd,
        env=env,
        stdout=v_out,
        stderr=v_err,
        text=True,
        start_new_session=True,
    )
    prev_sigterm = signal.getsignal(signal.SIGTERM)

    def _forward_sigterm(signum, _frame):
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGTERM, _forward_sigterm)
    try:
        return proc.wait(timeout=timeout_sec), False
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.wait()
        return 124, True
    finally:
        signal.signal(signal.SIGTERM, prev_sigterm)
```

## Independent Review Routing Contract (`CCG-016` / `R4`)

Both **Implementation Review** (Step B4) and **Final Review** (Step B8)—plus the post-archive focused diff Review in Step B9—are bound to **one concrete reviewer product**:

- `agent_product`: `antigravity-cli` (`pi` is unavailable on this workstation and MUST NOT be listed as a fallback)
- `entrypoint`: `/Users/elvis/.gemini/antigravity-cli/bin/agy-readonly-review --model gemini-4-carbon-high --output-format stream-json --disable-slash-commands --add-dir /private/tmp`
- `agent_role`: `independent-reviewer`
- `capability_profile`: `control-plane-high`
- `independence`: `distinct-contract-instance` (`same_instance=false`, verified by recording both the executor conversation ID `82aad109-d4a7-4334-8981-9758596ff9a7` and each spawned reviewer's distinct `conversation_id` from `stream-json` `init`/`result` events)
- `result_authority`: `governed-review-evidence`

## Cross-CLI Sync Contract (`B7` & Manifest Verification)

`references/cross-cli-portable-manifest.json` and `references/workflow-overview.md` are NOT self-declared inside `manifest["skills"][0]["files"]` (passing them to `--select-file` raises `ValueError` in `scripts/validate_cross_cli_sync.py:6053-6054`). Step B7 therefore passes `--manifest references/cross-cli-portable-manifest.json` and passes `--select-file` exclusively for the 7 declared portable files modified across local `main` (`7829572` + Phase B) relative to `origin/main`:

1. `references/approved-implementation-workflow.md` (from `7829572`)
2. `references/autoloop-req-acceptance.md`
3. `references/autoloop-review-hunt.md`
4. `references/project-learning-closeout.md`
5. `references/resume-context-amendments.md` (from `7829572`)
6. `scripts/autoloop_ctl.py`
7. `scripts/gov_runner.py`

## Validation & Forward-Test Plan

1. **Python 3.9 Compatibility Gate**:
   - `/usr/bin/python3 -m py_compile scripts/gov_runner.py scripts/autoloop_ctl.py scripts/check_commit_text.py`
2. **Clean Snapshot Tree Full Gate Suite** (constructed via `git archive HEAD` + overlaying Phase B allowed files into `/tmp/osc-clean-verify-<ts>`, isolating pre-existing dirty files):
   - `/opt/anaconda3/bin/python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py <clean_tree>`
   - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_core_gates.py <clean_tree>`
   - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_distribution.py <clean_tree>`
   - `PYTHONPATH=<clean_tree> PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 -m unittest discover -s <clean_tree>/tests -v`
3. **Focused Unit Tests (`tests/test_gov_runner_git_capture.py` & `tests/test_workflow_rules.py`)**:
   - Exit `127` (`setup_or_env_error`) vs `ModuleNotFoundError` exit `1` (`verification_failed`) vs process-group timeout exit `124` (`timeout` with zero surviving background `sleep` grandchildren), all setting `cli_launched is False`;
   - Single-module `Ran 0 tests` (`v_code == 0`) vetoed as `empty_test_execution`, multi-module `Tests run: 0` + `Tests run: 4` (`v_code == 0`) exempted by positive count, and pytest `collected 0 items` / `5 deselected` (`v_code == 5`) classified as `empty_test_execution`;
   - Non-collapsing `failure_signature` across two distinct `unittest` failures ending in `FAILED (failures=1)` and identical signature across repeated runs of the same failing test with varying durations/temp paths;
   - Zero residual secret substrings (`p@ss`, `ss@`, `sk-abc`, `k1_sec`) in `report.md` and `receipt.json` for inputs combining `postgres://admin:p@ss@127.0.0.1:5432/db` and JSON `{"Authorization": "Bearer sk-abc123", "api_key":"k1_sec"}`;
   - Snapshot-sourced escalation for committed `db/migration/V1__init.sql`, `src/auth.py`, and `src/SecurityConfig.java` on a clean worktree without `--base-ref` (`-high`, `HUNT_REF.parent` mounted, `FAST_HUNT_ESCALATION_ADDENDUM` injected) vs non-escalation for `docs/note.md` and `src/test/resources/seed.sql`, plus `verify_env_path` `PATH` passthrough.
4. **Two Isolated Forward-Test Probes (`/tmp/osc-forward-test-<ts>`)**:
   - Probe 1 (Zero-Test False-PASS Veto): Temporary Git repo whose verify command prints `Ran 0 tests in 0.000s` with exit `0` settles deterministically as `FAIL` (`failure_kind == "empty_test_execution"`, `cli_launched == False`).
   - Probe 2 (Clean-Branch High-Risk `fast` Escalation): Temporary Git repo with committed `db/migration/V2__add_idx.sql` on a feature branch in `fast` mode without `--base-ref` records `risk_escalated_paths: ["db/migration/V2__add_idx.sql"]`, upgrades `--model` to `-high`, mounts `references/`, and injects `FAST_HUNT_ESCALATION_ADDENDUM`.

## Migration / Rollback (`R9` Explicit Approval Guard)

1. **Cross-CLI Runtime Rollback**: Run `scripts/validate_cross_cli_sync.py restore-target` or copy from `/tmp/osc-self-evo-backup-<ts>/{codex,pi,antigravity,grok}/openspec-superpower-change` and re-run `quick_validate.py` + `validate_core_gates.py`.
2. **Local `agent-autoloop` Runner Rollback**: Restore `scripts/gov_runner.py` from backup and run `python3 scripts/autoloop_ctl.py ensure`.
3. **Repository Working-Tree Rollback (`R9`)**: NEVER run `git reset` or `git clean`. Discarding uncommitted edits on tracked Phase B files via `git checkout HEAD -- <allowed-files>` **requires explicit user approval first** (`SKILL.md:210`), and MUST copy all modified files to `/tmp/osc-rollback-stash-<ts>/` before restoring only the Phase B file list while leaving all 6 `OUT_OF_SCOPE_PREEXISTING_DEBT` paths untouched.
