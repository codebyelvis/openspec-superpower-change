## ADDED Requirements

### Requirement: Deterministic verification environment passthrough, process-group timeout isolation, pre-reviewer failure short-circuit, and redacted non-collapsing failure evidence

`scripts/autoloop_ctl.py run` SHALL pass the caller's `PATH` environment string
(`verify_env_path`) in the batch payload without serializing unrelated caller
environment variables, and `scripts/gov_runner.py` SHALL apply a non-empty
`verify_env_path` to the verification subprocess `PATH`. `scripts/gov_runner.py`
SHALL execute `verify_command` in a dedicated process session
(`start_new_session=True`); when `verify_timeout` expires, `gov_runner.py` SHALL
terminate the entire process group via `os.killpg(..., SIGKILL)`, record exit
code `124`, classify `failure_kind` as `"timeout"`, and write structured failure
artifacts instead of crashing or leaving orphan child processes running.

Whenever `verify_command` exits with non-zero `v_code` (or triggers a
deterministic zero-test execution veto on `v_code == 0`), `scripts/gov_runner.py`
SHALL short-circuit before launching the read-only reviewer CLI (`cli_launched:
false`), classify `failure_kind` deterministically as `"timeout"` (`v_code ==
124`), `"setup_or_env_error"` (strictly `v_code` in `(126, 127)` or shell-level
`command not found`, keeping Python/runtime `ImportError` or `ModuleNotFoundError`
at exit `1` as `"verification_failed"`), `"empty_test_execution"` (`v_code == 0`
zero-test veto, or `v_code == 5` matching zero-collected or `-k` deselected test
output), or `"verification_failed"`, mask credentials in `verify_error_excerpt`
(including `@`-containing URL passwords and quoted JSON secret/bearer fields),
and compute a deterministic 16-hex `failure_signature` over sorted unique failed
test identifiers plus the first non-footer error line normalized for volatile
timestamps, durations, memory addresses, and temporary paths.

#### Scenario: Missing binary or shell command fails fast as setup_or_env_error without launching reviewer

- **WHEN** `verify_command` invokes an absent executable returning exit code `127` (or `126` / shell `command not found`)
- **THEN** `gov_runner.py` SHALL settle deterministically as `FAIL` with `cli_launched: false` and `failure_kind: "setup_or_env_error"`
- **AND** Python `ModuleNotFoundError` exiting with code `1` SHALL instead record `failure_kind: "verification_failed"`

#### Scenario: Verification timeout kills grandchild processes and records structured timeout receipt

- **WHEN** `verify_command` spawns a background or child process that exceeds `verify_timeout`
- **THEN** `gov_runner.py` SHALL kill the entire verification process group via `os.killpg`, record `verify_exit_code: 124` and `failure_kind: "timeout"`, and skip launching the reviewer CLI
- **AND** no grandchild process from that verification session SHALL remain alive after `_run_verify_command` returns

#### Scenario: Distinct failing unit tests do not collapse to the same failure_signature and secrets are fully masked

- **WHEN** two consecutive runs fail on different test cases (such as `FAIL: test_a` vs `FAIL: test_b`) that share an identical trailing summary footer (`FAILED (failures=1)`), or failure output contains `postgres://admin:p@ss@host/db` and JSON `{"Authorization": "Bearer sk-secret"}`
- **THEN** `gov_runner.py` SHALL produce strictly unequal `failure_signature` values for `test_a` vs `test_b` while producing identical `failure_signature` values for repeated runs of `test_a` across different durations or `/tmp` paths
- **AND** neither `report.md` nor `receipt.json` SHALL contain any raw substring of the password or token (`p@ss`, `ss@`, or `sk-secret`)

### Requirement: Aggregate positive-count-exempted zero-test execution veto

When `verify_command` exits with code `0`, `scripts/gov_runner.py` SHALL inspect
the combined verification output across the entire command invocation: if no
positive executed test count (such as `Ran [1-9]\d* tests`, `Tests run: [1-9]\d*`,
or `[1-9]\d* passed`) appears anywhere in the combined output AND a zero-test
execution marker (`Ran 0 tests`, `collected 0 items`, `Tests run: 0,`, `no tests
ran`, or `There are no tests to run`) is present, `gov_runner.py` SHALL
deterministically veto `PASS` before launching the read-only reviewer CLI with
`failure_kind: "empty_test_execution"`. When at least one test suite or module in
a chained/multi-module verification run reports a positive executed test count,
an earlier or sibling module reporting `0` tests SHALL NOT trigger the zero-test
veto.

#### Scenario: Single-suite zero-test command with exit code 0 is vetoed before reviewer launch

- **WHEN** `verify_command` exits `0` with output `Ran 0 tests in 0.000s` and no positive test count anywhere in stdout/stderr
- **THEN** `gov_runner.py` SHALL deterministically settle as `FAIL` with `failure_kind: "empty_test_execution"` and `cli_launched: false`
- **AND** `autoloop_ctl.py` SHALL NOT stamp `status: passed`

#### Scenario: Multi-module run with both zero-test and positive-test modules is exempted

- **WHEN** `verify_command` exits `0` on a multi-module build outputting both `Tests run: 0, Failures: 0` and `Tests run: 4, Failures: 0`
- **THEN** `gov_runner.py` SHALL NOT trigger the `empty_test_execution` veto

#### Scenario: Pytest exit code 5 from zero collection or -k deselection is classified as empty_test_execution

- **WHEN** `verify_command` exits with code `5` and outputs `collected 0 items`, `0 selected`, or `5 deselected`
- **THEN** `gov_runner.py` SHALL record `failure_kind: "empty_test_execution"` and `cli_launched: false`

### Requirement: Snapshot-sourced high-risk business path escalation in fast mode and fifth diagnosability hunt lens

`references/autoloop-review-hunt.md` SHALL apply to `pre-mr` reviews and
risk-escalated `fast` reviews, adding a fifth conditional lens
(`diagnosability_context`) that activates exclusively when the diff adds or
alters external I/O calls or `catch`/`except` error-handling blocks (`hunt: n/a`
otherwise) to check against swallowed root-cause exceptions, missing in-scope
triage identifiers/error codes on external failures, and raw credential logging.

In `fast` mode, `scripts/gov_runner.py` SHALL scan `git.changed_files.txt`
(excluding `docs`, `doc`, `test`, `tests`, `__tests__`, `fixtures` path segments
and root-level `*.md` files) for `.sql` files, high-risk directory segments
(`migration`, `migrations`, `changelog`, `auth`, `authn`, `authz`, `oauth`,
`security`, `permission`, `permissions`), or filename stems starting with
`auth`, `security`, `permission`, or `migration`. When matched, `gov_runner.py`
SHALL keep `review_profile` as `fast` (requiring no `--base-ref`), upgrade the
default reviewer model tier to `-high` when `--model` was not explicitly
specified by the caller, mount the `references/` directory containing
`autoloop-review-hunt.md` via `--add-dir`, append `FAST_HUNT_ESCALATION_ADDENDUM`
to the reviewer prompt, and record `risk_escalated_paths` in `receipt.json`.

#### Scenario: Committed SQL migration or auth module in zero-arg fast mode escalates reviewer to high with hunt lens

- **WHEN** `autoloop_ctl.py run` executes in default `fast` mode without `--base-ref` or `--model` on a branch whose `git.changed_files.txt` includes `db/migration/V1__init.sql`, `src/auth.py`, or `src/SecurityConfig.java`
- **THEN** `gov_runner.py` SHALL record the matched path in `risk_escalated_paths`, upgrade the reviewer CLI model to `-high`, mount `references/` via `--add-dir`, and append `FAST_HUNT_ESCALATION_ADDENDUM`
- **AND** `gov_runner.py` SHALL NOT fail with `missing_base_ref`

#### Scenario: Documentation or test-only SQL fixture in fast mode does not escalate

- **WHEN** `git.changed_files.txt` in `fast` mode contains only `docs/architecture.md` or `src/test/resources/seed.sql`
- **THEN** `risk_escalated_paths` SHALL be empty and `fast` mode SHALL retain its default `-medium` model and lightweight prompt

### Requirement: Premise-checking auto-repair convergence and threshold-gated mechanical learning hierarchy

`references/autoloop-req-acceptance.md` SHALL require `/autoloop` repair loops on
`FAIL` to inspect `failure_kind` and `failure_signature`, repair environment/PATH
configuration rather than product code on `setup_or_env_error`, stop immediately
when two consecutive runs emit the identical `failure_signature`, state and verify
the shared premise (`Attack the Premise`) in one sentence before a second code
repair attempt, and never dismiss a same-scope `FAIL` finding citing an exact
diff `path:line` and concrete trigger path as "not reproduced locally".

`references/project-learning-closeout.md` SHALL specify that once an item meets
its mandatory `## Triggers` threshold and passes
`references/learning-candidate-pipeline.md` scope classification, durable
promotion SHALL prefer (1) single-source-of-truth or dead-code removal, (2)
static validators/types naming the canonical replacement, (3) observable behavior
regression tests, and (4) prose guidance last, while keeping any condensation or
retirement of governed skill/workflow prose under Major Self-Evolution approval
and preserving `Non-Negotiables` and validator-locked phrases.

#### Scenario: Consecutive identical failure signatures halt auto-repair loop

- **WHEN** two consecutive `/autoloop` verification runs return `"verdict": "FAIL"` with the identical `failure_signature`
- **THEN** the agent SHALL stop auto-repairing immediately and report the diagnostic evidence rather than attempting blind code mutations

#### Scenario: Learning promotion prioritizes mechanical layers without weakening Major prose locks

- **WHEN** a Project Learning Closeout item qualifies under `## Triggers` and `learning-candidate-pipeline.md`
- **THEN** the closeout workflow SHALL evaluate architectural single-source-of-truth, pointer-bearing static validators, and behavior regression tests before adding prose rules
- **AND** governed skill/workflow prose SHALL NOT be condensed or removed without Major Self-Evolution approval or in violation of validator-locked phrases
