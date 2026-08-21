# Source Verification Evidence

## Revision and authority

- change: `add-role-first-review-routing`
- phase: Task 6 source verification
- authority: source verification only
- baseline exclusions: real Pi, runtime sync/apply/restore, Git, canonical
  transition, archive, publication, Envelope, and completion
- dependency boundary: dependency installation and interpreter substitution were
  initially excluded; the later R7 amendment authorized only the exact isolated
  Conda environment and interpreter recorded below

## Attempt 1 — BLOCKED

- observed date: `2026-08-11`, Asia/Shanghai
- command:
  `python3 /Users/elvis/.codex-account-a/skills/.system/skill-creator/scripts/quick_validate.py /Users/elvis/file/develop/opensource/openspec-superpower-change`
- exit: `1`
- sanitized failure: the default interpreter raised
  `ModuleNotFoundError: No module named 'yaml'` while importing the validator's
  required PyYAML dependency.
- classification: execution-environment dependency blocker; this result does
  not show a Router implementation or test regression.
- stop applied: yes. The remaining seven Task 6 validation commands, static
  checks, natural forward run, and source-delta command were not started in
  this attempt.

The approved Plan explicitly requires `BLOCKED` when the default `python3`
lacks PyYAML and forbids installing packages or substituting an unbound
interpreter in this Plan revision. No workaround was attempted.

## Attempt 2 — authorized standard installation refused

- observed date: `2026-08-11`, Asia/Shanghai
- one-time user authority: install PyYAML only into the default `python3` user
  environment for the approved `quick_validate`; stop if the standard install
  is refused, and do not use `--break-system-packages`.
- command: `python3 -m pip install --user PyYAML`
- exit: `1`
- sanitized failure category: PEP 668
  `externally-managed-environment`; pip refused the requested user install.
- installation result: no successful PyYAML installation occurred.
- prohibited override used: no; `--break-system-packages` was not used.
- stop applied: yes. No alternate installer, environment, interpreter, or
  dependency route was attempted, and Task 6 validation was not rerun.

## Historical blocker after Attempt 2

At that point Task 6 was `BLOCKED` by the default interpreter dependency and
could resume only after a separately approved and governed route became
available. R7 later supplied that route by binding a specific isolated
environment/interpreter and dependency procedure, refreshing immutable inputs,
and obtaining a fresh independent Plan Preflight PASS.

## Attempt 3 — isolated Conda environment and initial validation PASS

- observed date: `2026-08-11`, Asia/Shanghai
- governing Plan SHA-256:
  `3a6169b892151a29d7cfa1ce96798e15c659327c6db34fc1e054d65c6ed39a80`
- R7 independent Preflight Review artifact:
  `docs/design/reviews/2026-08-11-add-role-first-review-routing-conda-plan-amendment-r7-review.md`
- R7 Review SHA-256:
  `67bf414d43da1678809d1c40892ab0d1fbf16868247dc2584f88c10d3fd0faaa`
- R7 Review verdict: `PASS`

### Step 2 — environment creation

- exact subshell exit: `0`
- Conda executable: `/opt/anaconda3/bin/conda`
- Conda executable SHA-256:
  `a543f4db6623ff7316d0549c2e5241196499a0d0b3e8d212772eeb2df084c8a3`
- isolated environment:
  `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-quick-validate-r1`
- isolated HOME/package-cache/TMPDIR: created only at the three reviewed paths
  under the mode-`0700` transaction root
- final assertion:
  `conda-verification-python: pass; python=3.11; pyyaml-major=6`
- channel/solver: explicit `defaults` / classic solver
- base update performed: `no`; the informational newer-Conda warning was not
  acted upon
- environment activated: `no`
- pip invoked: `no`
- fallback, interpreter substitution, or automatic cleanup: `no`

### Step 3 — quick/project/unit/OpenSpec validation

The exact reviewed fail-fast subshell exited `0`:

| Validation | Result |
|---|---|
| Router `quick_validate.py` with bound Conda Python | `PASS` — `Skill is valid!` |
| Router dependency-free project validator | `PASS` — `Core gates valid` |
| Router default-`python3` unittest suite | `PASS` — 184 tests, `OK` |
| Companion `quick_validate.py` with bound Conda Python | `PASS` — `Skill is valid!` |
| Companion dependency-free project validator | `PASS` — validation succeeded |
| Companion default-`python3` unittest suite | `PASS` — 85 tests, `OK` |
| `openspec validate add-role-first-review-routing --strict` | `PASS` — change valid |
| `openspec validate --all --strict --no-interactive` | `PASS` — 3 passed, 0 failed |

## Current state and next boundary

- The default-interpreter/PyYAML blocker is cleared only for the two
  `quick_validate` commands through the reviewed isolated Conda interpreter.
- Task 6.1 is not complete: Step 4 static/cross-skill checks, Step 5 isolated
  forward verification, and Step 6 source-delta evidence have not run.
- No source correctness/PASS, Candidate source High Review, real Pi, runtime,
  Git, canonical transition, archive, publication, completion, or cleanup is
  claimed or authorized by this record.
- The Conda environment is retained for reproducibility until the governed
  Task 11 cleanup boundary.

## Attempt 3 continuation — static checks PASS, forward verification BLOCKED

### Step 4 — static and cross-skill checks

All exact reviewed commands exited `0`:

- both negated searches emitted no unallowlisted line;
- the Router and Companion Handoff contracts were byte-identical;
- both shared Handoff/validator-core identity tests passed;
- the path-only audit ended with `0 sensitive categories found`.

### Step 5 — isolated GREEN forward tests

- sanitized summary path:
  `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/role-first-forward-summary.json`
- private summary mode: `0600`
- private summary SHA-256:
  `4243215d6a089a11b31b4e45a66063da42a7a6b4de1cee89813d44cc2f6659f1`
- durable eight-field-per-case copy:
  `docs/design/evidence/add-role-first-review-routing/2026-08-10-role-first-forward-summary.json`
- case count: `6`
- oracle matches: `2`
- oracle mismatches: `4`
- transient runner root after completion: absent; no raw model/process output was retained.

Sanitized mismatch classification:

| Case | Result | Observed mismatch against the approved oracle |
|---|---|---|
| `generic_review_destination` | `FAIL` | profile was `cohesive-medium`, expected `control-plane-high` |
| `user_selected_pi` | `FAIL` | role/profile/authority were `independent-reviewer` / `cohesive-medium` / `governed-review-evidence`, expected `advisory-reviewer` / `control-plane-high` / `advisory-input` |
| `new_window_codex` | `PASS` | none |
| `advisory_review` | `FAIL` | profile was `cohesive-medium`, expected `control-plane-high` |
| `same_pi_session` | `PASS` | none |
| `required_reviewer_unavailable` | `FAIL` | blocker owner was `control-plane`, expected `user` |

The command runner writes the sanitized summary and returns nonzero whenever
any case mismatches. The launching tool yielded while the runner was active and
did not retain the terminal numeric status in its immediate result, but the
runner source contract and the four persisted `FAIL` records mechanically map
this run to `forward: "blocked"` / exit `1`; no rerun or replacement output was
attempted.

### Stop boundary

- Task 6 Step 6 `source-delta` was not started.
- `source-compare-r7` and `source-delta-r7.json` remain absent.
- Task 6.1 remains incomplete.
- No Candidate source High Review prompt/verdict, runtime planning, real Pi,
  runtime mutation, Git, canonical transition, archive, publication,
  completion, fallback, or cleanup is authorized or claimed.

Resume only through a governed source-slice diagnosis/fix and a fresh complete
Task 6 verification run. The failed forward evidence must remain durable and
must not be rewritten as PASS.

## Governed source-slice diagnosis and TDD correction

The blocked summary above remains the durable record of the first natural
forward run. The three private sanitized attempt artifacts were also retained
without raw model or process output:

| Forward attempt | Result | Sanitized SHA-256 | Durable interpretation |
|---|---:|---|---|
| 1 | `2/6`, BLOCKED | `4243215d6a089a11b31b4e45a66063da42a7a6b4de1cee89813d44cc2f6659f1` | Full eight-field mismatch table is preserved above. |
| 2 | `1/6`, BLOCKED | `a8af620b1c727f6f52c1ea92eca31c48b9d6b358b7866bcfdaefa36dc134456f` | Documentation-only change did not affect the runner because the copied Skill bytes were not exposed to the no-tool model prompt. |
| 3 | `3/6`, BLOCKED | `e88ad074384d8e7760ba49d48fcfb6722d172c3d4ed124829a1c3d958c75ef7e` | Source-bound classification fixed role/profile selection, but actionable future instance assignment was still misclassified as unavailable. |

The narrowest confirmed causes were:

- four runtime-facing documents did not contain one exact review-kind
  classification matrix;
- the forward runner copied those Skill files but prohibited tool reads, so the
  model could not observe their content;
- the original oracle over-constrained fields that the approved contract leaves
  selectable or owner-equivalent; and
- the runtime guidance did not distinguish an actionable recommendation for a
  future distinct instance from an explicitly unavailable required reviewer.

TDD evidence was captured before each correction:

- the shared classification-matrix tests failed against all four runtime-facing
  documents, then passed after one identical managed block was added;
- the forward-runner source-binding tests failed before the runner extracted and
  injected that reviewed block, then passed after the minimal implementation;
- boundary tests for actionable assignment versus explicit unavailability failed
  before the final guidance lines were added, then passed afterward;
- the runner keeps oracle alternatives private and rejects oracle text in model
  prompts, summaries, and retained temporary output.

Changed source surfaces were limited to the approved allowlist:

- Router `SKILL.md`, `references/agent-capability-routing.md`, and
  `references/response-patterns.md`;
- Companion `SKILL.md`;
- Router/Companion workflow tests;
- Router forward fixtures and runner.

## Final Task 6 re-verification — PASS through Step 5

The complete reviewed Step 3 subshell was rerun after the final correction and
exited `0`:

| Validation | Fresh result |
|---|---|
| Router `quick_validate.py` with bound Conda Python | `PASS` |
| Router dependency-free project validator | `PASS` |
| Router default-`python3` unittest suite | `PASS` — 186 tests, `OK` |
| Companion `quick_validate.py` with bound Conda Python | `PASS` |
| Companion dependency-free project validator | `PASS` |
| Companion default-`python3` unittest suite | `PASS` — 86 tests, `OK` |
| change OpenSpec strict validation | `PASS` |
| all OpenSpec strict validation | `PASS` — 3 passed, 0 failed |

The exact Step 4 static/cross-skill block also exited `0`: both negative
searches were empty, the shared Handoff and validator-core checks passed, and
the path-only audit ended with `0 sensitive categories found`.

The final isolated six-case natural forward run exited `0`:

- stdout result: `forward: "pass"`, `case_count: 6`;
- private summary mode: `0600`;
- private and durable summary SHA-256:
  `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b`;
- durable current summary:
  `docs/design/evidence/add-role-first-review-routing/2026-08-10-role-first-forward-summary.json`;
- all six result rows are `PASS` and retain exactly the approved eight fields;
- transient runner root after completion: absent.

The durable JSON now represents the current fresh PASS state; the earlier
BLOCKED state is not erased because its exact SHA, complete mismatch table,
diagnosis, and stop boundary remain in this evidence record.

## Current boundary

- Task 6 Step 6 complete no-Git source-delta has not yet run.
- Candidate source High Review has not yet been requested or accepted.
- No real Pi, runtime plan/apply/restore, Git, canonical transition, archive,
  publication, Envelope, completion, or cleanup is authorized or claimed.

## Step 6 source-delta attempts — BLOCKED

### Attempt 1 — preflight inventory schema mismatch

- exact source-delta command exit: `1`;
- sanitized error: `source inventory fields are invalid`;
- compare root: created mode `0700`, retained as
  `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/source-compare-r7-attempt1-blocked`;
- delta JSON: not created.

The source-start inventories correctly use the strict three-field inventory
schema. The R4 preflight inventories correctly add their reviewed
`excluded_paths`, but the production source-delta validator incorrectly sent
that four-field value through the source-start validator. The existing unit
fixture repeated the wrong three-field shape and therefore concealed the
failure.

A realistic four-field preflight fixture first reproduced the exact production
failure. The minimal implementation then added a preflight-only validator that
requires the exact binding fields, exact exclusion list, safe unique relative
paths, and no overlap between exclusions and recorded paths. The source-start
validator remains unchanged and strict. The focused RED became GREEN.

### Attempt 2 — exact allowlist rejection

- exact source-delta command exit: `1`;
- sanitized error: `source delta contains paths outside the exact allowlist`;
- compare root: created mode `0700`, retained as
  `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/source-compare-r7-attempt2-blocked`;
- delta JSON: not created.

A path/status/SHA-only diagnostic initially found four parent-directory size
changes plus one changed generated cache file. A nested allowed-file RED proved
that directory entry size changes caused by allowed children were incorrectly
treated as source changes. The comparator now ignores only the `size` field of
an existing directory when every other directory field is identical; directory
addition, deletion, type, mode, and all file/symlink changes remain governed.
The focused RED became GREEN.

After that correction, the complete read-only comparison reports exactly one
remaining unexpected path and no Companion unexpected path:

| Repository/path | Status | Source-start SHA-256 | Current SHA-256 |
|---|---|---|---|
| `router/scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc` | modified | `425e7753b96e7cca2ad645d9a5385e52532e83dd19540ecb7d11ba3adb768c66` | `5b7cd72df71d308929c08fb6ae047403b4374e1824a13f479e5034f468dfff49` |

The cache file was born/modified at `2026-08-11T15:12:26+0800`, after the
source-start inventory at `2026-08-11T13:34:05+0800`. It is not in the bound R7
allowlist or source backup. No deletion, replacement, allowlist expansion,
cleanup, or reverse copy was performed. Current authority does not permit any
of those actions.

### Current stop boundary

- Task 6 Step 6 remains `BLOCKED`; Tasks 6.1 and 6.2 are not reconciled as
  complete.
- A fresh full Step 3/4 run passed after the preflight-schema correction, and a
  fresh final-source forward run again passed `6/6`; the later directory-only
  comparator correction has a focused GREEN test but does not release Step 6.
- Candidate source High Review cannot begin until a separately authorized,
  mechanically bound disposition of the unexpected cache path is completed and
  the complete Task 6 verification/source-delta chain is rerun.

## R9 evidence recovery and final Step 6 source-delta — PASS

On 2026-08-20 the original control plane accepted the independent R9
evidence-rehydration Preflight `PASS` at
`docs/design/reviews/2026-08-20-add-role-first-review-routing-evidence-rehydration-r9-review.md`
(SHA-256
`f533c3b99029e88adc304aa7eb95b17cb8200a375154df1ec5b383c1e595a9c4`).
The Review authorized only Task 6 Step 5A and, after its exit `0`, Step 6.

### Step 5A — exact single-cache transaction PASS

- exact reviewed command exit: `0`;
- stdout: `source_cache_recovery: "pass"`, `source_absent: true`;
- source path:
  `scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc`;
- current-byte backup and moved original SHA-256:
  `5b7cd72df71d308929c08fb6ae047403b4374e1824a13f479e5034f468dfff49`;
- recovery root:
  `/private/tmp/add-role-first-review-routing-r9-r2-20260820-4hEfNB/source-delta-recovery-r9`,
  real mode `0700`;
- `backup.pyc`, `original-object.pyc`, `prepared.json`, and `verified.json`:
  regular non-symlink mode `0600` files;
- source cache after the exclusive same-filesystem move: absent.

The old source-start cache SHA remained historical evidence only. No unlink,
overwrite, recursive cleanup, restore, other cache operation, Git, source edit,
Pi, or runtime operation occurred.

### Step 6 — complete no-Git source-delta PASS

- exact reviewed command exit: `0`;
- private output:
  `/private/tmp/add-role-first-review-routing-r9-r2-20260820-4hEfNB/source-delta-r9.json`;
- private output mode/SHA-256:
  `0600` /
  `ffca933661288aab3df0f5d6f7476339bd7624353798442f8d9191982c8307d2`;
- compare root: real mode `0700`;
- result: `source_delta: "pass"`;
- actual changed paths: `42`;
- bound allowlist entries: `43`;
- unexpected paths: `[]`;
- both 22/14 member preimage archives were safely extracted to the private
  compare root and matched their reconstructed baseline records.

The durable path/status/SHA/mode-only copy is
`docs/design/evidence/add-role-first-review-routing/2026-08-20-source-delta-r9-summary.json`
with SHA-256
`55625e1b0c6a5832520e00975e61d1eeba758bd7c15e482a688dd8b4b41da57e`.
It contains no native source bytes, raw agent output, credentials, sessions, or
runtime settings.

### New boundary

Task 6 source verification is now eligible for candidate source High Review.
This source-delta PASS does not itself establish candidate correctness, runtime
readiness, Pi readiness, OpenSpec completion, canonical transition, archive,
publication, cleanup, or whole-task completion. The cache recovery evidence and
all R9 roots remain retained.

## Candidate source High Review FAIL and P1 correction

The first independent Candidate source High Review was persisted without
rewriting its verdict:

- artifact:
  `docs/design/reviews/2026-08-10-add-role-first-review-routing-source-review.md`;
- artifact SHA-256:
  `35050b3e8766b055f11d3a55018d4a34c1aca87893f574b477bbfe28a9cf6ef1`;
- verdict: `FAIL`;
- actionable finding: P1 destination TOCTOU in runtime apply/restore. The
  implementation checked a destination prestate and then performed an
  unconditional namespace replacement/removal, so external drift inserted
  after the check could be overwritten or deleted.

No runtime planning or mutation began. Before correction, the exact affected
source/test/evidence files were copied to the private mode-`0700` backup root
`/private/tmp/add-role-first-review-routing-p1-toctou-20260820-VueWBG`.
The three backup files are regular mode-`0600` files with SHA-256 values:

- `router/validate_cross_cli_sync.py`:
  `42cb47739b81646eadc303dbdfb59821ed75f21a6a12815600a3b51b7555ed98`;
- `router/test_cross_cli_sync.py`:
  `dc88f721f646752f4969ca3e3a36d3cd1f82f6a611e886d2b250a7937039de97`;
- `router/source-verification.md`:
  `a2bd60a67c4fef9e7840ee1b12f75d6386def07218397dfb311755d92c8d8c56`.

### Root cause and TDD boundary

The confirmed root cause was the separation between reviewed-prestate
validation and namespace mutation. The transaction lock serializes only this
tool and cannot exclude an external writer. The correction reuses the existing
macOS `renameatx_np` primitives:

- existing destinations use atomic `RENAME_SWAP`, then validate the actual
  displaced object and roll back on mismatch;
- absent destinations use `RENAME_EXCL`, so a concurrent creation blocks the
  install without being unlinked;
- restore-to-absent atomically moves the destination into a unique quarantine,
  validates the moved object, and rolls back on mismatch;
- ambiguous rollback preserves the displaced/quarantined object and reports a
  manual-disposition path instead of continuing.

Six focused tests were written before production changes. The RED run produced
six expected failures and no error; the same six tests then passed GREEN:

- existing-file drift after the apply guard;
- absent-file creation at the exclusive apply boundary;
- symlink substitution at the apply swap boundary;
- candidate-write failure never unlinks a concurrent destination;
- existing-file drift at the restore swap boundary;
- absent-file drift at the restore removal boundary.

The full cross-CLI module then passed `69` tests. Current corrected hashes are:

- `scripts/validate_cross_cli_sync.py`:
  `9f1cd9092cd0d98c18197437d7afc6911d63eda864eb5c4b73c391d67e759669`;
- `tests/test_cross_cli_sync.py`:
  `6b905e56fcb6d94eb01f4861b52ba9a063b2ad4c8a5e2191b6f924fcda6121f4`.

### Fresh post-correction verification

The original bound temporary Conda environment could not be replayed because
its real `bin/python3.11` object was externally absent while the `python` and
`python3` symlinks remained. The failed replay stopped at that first command;
it is not represented as a test regression or rewritten as a PASS. The current
project-level verification used `/opt/anaconda3/bin/python` for the two
PyYAML-dependent quick validators, matching the interpreter accepted by the
first High Review, while all dependency-free commands remained on default
`python3`.

Fresh results after the P1 correction:

- Router quick/project validation: `PASS`;
- Router unit suite: `192` tests, `OK`;
- Companion quick/project validation: `PASS`;
- Companion unit suite: `86` tests, `OK`;
- change/all OpenSpec strict validation: `PASS`, `3 passed / 0 failed`;
- both negative searches: no unallowlisted line;
- shared Handoff/validator-core byte checks: `PASS`;
- path-only sensitive audit: `0 sensitive categories found`;
- isolated natural forward run: `forward: "pass"`, `case_count: 6`;
- forward summary: mode `0600`, SHA-256
  `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b`;
- transient forward root after completion: absent.

### Fresh complete source delta

The first P1 delta binding correctly failed closed because the already durable
R9 summary was missing from the expanded allowlist. That failed compare root is
retained and no PASS output was produced. The R2 binding added only that exact
evidence-only path and then passed:

- private delta:
  `/private/tmp/add-role-first-review-routing-p1-toctou-20260820-VueWBG/source-delta-p1-r2.json`;
- private delta mode/SHA-256: `0600` /
  `c0e04d2c838f8694a0f78cd31263713119415225a13c71fcffd4c66df15b0f6d`;
- compare root mode: `0700`;
- binding SHA-256:
  `a47a40f3878f7b34cb7fe73d36635e495b60c28b00eac57848ae2ba4f4293b71`;
- allowlist: `49` entries, SHA-256
  `5bcf0351ab9e0f5ef750b7d0034405ab215d3fb1156ac731df1026108fe7b2b3`;
- actual changed paths: `45`;
- result: `source_delta: "pass"`, `unexpected_paths: []`;
- both preimage archives again matched their bound reconstructed baselines.

The durable path/status/SHA/mode-only copy is
`docs/design/evidence/add-role-first-review-routing/2026-08-20-source-delta-p1-r1-summary.json`
with SHA-256
`8c45a79406b09e5f7fafe0c5230c7ccac6ebcb2ca39dcbdbcb03c22a742f8adf`.
This evidence record and the durable summary were written after the private
delta and are explicitly evidence-only post-delta mutations for the next
independent Review. They do not change implementation bytes and do not
authorize runtime planning until a new Candidate source High Review returns
`PASS` and the control plane accepts it.

## Candidate source High Re-review P1 R1 FAIL and second correction

The fresh independent P1 R1 re-review was persisted without changing its
verdict:

- artifact:
  `docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r1.md`;
- artifact SHA-256:
  `44138637110b7643585d244721cf710f1f08a899dca874fd81df6ab1898d9719`;
- verdict: `FAIL`;
- P1 findings: the mutation boundary did not bind the complete destination
  parent chain, and receipt advancement could discard a concurrently changed
  receipt after exchange;
- P2 finding: the Router and Companion public English/Chinese READMEs still
  described schema-4/schema-1 evidence as current.

No runtime destination was inspected or changed and no runtime plan, Git, or
Pi operation began. Before correction, the nine affected source, test, and
evidence files were copied to
`/private/tmp/add-role-first-review-routing-p1r2-20260820-bSA2SA`, a private
mode-`0700` root. Every direct backup is a regular mode-`0600` file. Their
SHA-256 values are:

| Backup | SHA-256 |
|---|---|
| `router/validate_cross_cli_sync.py` | `9f1cd9092cd0d98c18197437d7afc6911d63eda864eb5c4b73c391d67e759669` |
| `router/test_cross_cli_sync.py` | `6b905e56fcb6d94eb01f4861b52ba9a063b2ad4c8a5e2191b6f924fcda6121f4` |
| `router/test_workflow_rules.py` | `7842c87506320c99d677ddc7a97c1549e686c43824ede00f3b81ee291b65831f` |
| `router/README.md` | `dc8c2f1137f5da7eadde99770139f37fa995e2208dc36a6150c82c1945db49d6` |
| `router/README_cn.md` | `d2e65513d48d20f2dc1b61937a31a500f5c37ce09799b53f3b572e3d21524c68` |
| `router/source-verification.md` | `aaeb40bece860114b48327e6b67b5968c2832dfcb66c71ff6fd56ea7c13103d5` |
| `companion/README.md` | `b6d9465d2a09404b1b354fdcc0e2bc096756832b42d4dd4c01ced97b5a6458c9` |
| `companion/README_cn.md` | `0a16570d60ab2c596a6c313fbb76dbb98e62b634470981a9e49256d9af3dcf1f` |
| `companion/test_workflow_rules.py` | `1a94e6af2d44cbf5b3392ddf6f2f6688c45bb6497bbbc328d8f8dc9982b26793` |

### Root cause, containment, and TDD boundary

The second correction binds the resolved destination parent chain by
directory identity, keeps a no-follow directory descriptor through candidate
creation and namespace mutation, and rechecks that binding around the
mutation. Final operations are performed relative to the verified descriptor,
so a parent mapping, link, type, or ancestor identity change fails closed.

Receipt transitions now use the same guarded exchange discipline. The
displaced live receipt must match the exact expected prestate. Drift triggers
an atomic rollback; ambiguous rollback preserves the displaced state as
mode-`0600` recovery evidence and blocks later targets. History collision or
installation failure also restores the prior live receipt or stops with
retained manual-disposition evidence. No unverified displaced receipt is
unconditionally deleted.

Seven focused cross-CLI tests and two public-documentation tests were written
before the production/documentation correction. The RED runs produced nine
expected failures with no fixture error. The same nine cases then passed
GREEN, covering:

- existing and absent destination parent mapping changes;
- parent symlink substitution and restore-to-absent parent drift;
- receipt drift rollback;
- rollback-blocked receipt retention and later-target exclusion;
- receipt-history collision rollback;
- Router and Companion current schema-6/schema-2 public guidance with frozen
  schema-4/schema-5 legacy audit isolation.

The complete cross-CLI module then passed `76` tests. Corrected current hashes
are:

| Current file | SHA-256 |
|---|---|
| `scripts/validate_cross_cli_sync.py` | `cef9fca193364a8ccda204fb80a351a656ac5e22c2919c96ecbf28fc7203f4ff` |
| `tests/test_cross_cli_sync.py` | `95797ae3a2db091661f094c742a9247d098789ff1e453388580f61241e3ac1c8` |
| `tests/test_workflow_rules.py` | `9e8f1d6904b0eb3e397eafb305f0e1743a77dcd9d9c715ac05e510f4e3aa2dc7` |
| `README.md` | `44314b9c0f128ddcac90154ac5f36f167f70a66ab93aca61a4b46a86646f08ff` |
| `README_cn.md` | `b973047e8092a9b7550ab62db5e795c6a7a0ba30e51304a2541953d4379fb987` |
| Companion `README.md` | `f260de8c1e97ca5ce282e39c432278ebed4699745d0cd6c650dc82ece9ffe0b5` |
| Companion `README_cn.md` | `d6180a9a0f54fc0d87934bd24efe320d5f9c7b45cb816292f86db5d1ba2b601c` |
| Companion `tests/test_workflow_rules.py` | `65f8e4f2de06dfd050ef74310c94a84d76cec2b54c1955a1fdb66372d5f0b12c` |

### Fresh second-correction verification

Fresh results after the second correction:

- Router quick/project validation: `PASS`;
- Router unit suite: `200` tests, `OK`;
- Companion quick/project validation: `PASS`;
- Companion unit suite: `87` tests, `OK`;
- change/all OpenSpec strict validation: `PASS`, `3 passed / 0 failed`;
- both exact Task 6 negative searches: empty;
- shared Handoff/validator-core byte checks: `PASS`;
- path-only sensitive audit: `0 sensitive categories found`;
- isolated natural forward run: `forward: "pass"`, `case_count: 6`;
- private forward summary mode/SHA-256: `0600` /
  `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b`;
- transient forward root after completion: absent.

### Fresh complete source delta after the second correction

The exact new source-delta transaction passed:

- private delta:
  `/private/tmp/add-role-first-review-routing-p1r2-20260820-bSA2SA/source-delta-r2.json`;
- private delta mode/SHA-256: `0600` /
  `0e2efdc63378c35f9ff31b36e4471c79e9ffec28fbbfd54293e7cadd68ced6dd`;
- compare root mode: `0700`;
- binding mode/SHA-256: `0600` /
  `599616e5aacf064f4ef3c40eb51b7cb49fd8ff9362eac6ca30954f4dae7e3029`;
- allowlist: `52` entries, mode `0600`, SHA-256
  `deb257062c43f18b22a79b97121f1c39991d43ca920289df7842ee6044184a50`;
- actual changed paths: `48`;
- result: `source_delta: "pass"`, `unexpected_paths: []`.

The durable path/status/SHA/mode-only copy is
`docs/design/evidence/add-role-first-review-routing/2026-08-20-source-delta-p1-r2-summary.json`
with SHA-256
`7c96f9f5b53ae1ed33e791a126442a261f83d1315d3dd6c8825509e6334a74fa`.
This appended evidence record, the durable summary, and the new P1 R2 review
input are evidence-only post-delta records. They do not change the candidate
implementation and do not authorize runtime planning. A fresh independent
Candidate source High Review must still return `PASS` and be accepted by the
original control plane before Task 8 may begin.

## Pi adversarial Review attempt 01 BLOCKED and sixth correction

After the P1 R5 Candidate Source and runtime-plan Reviews both returned `PASS`,
the control plane applied and verified the reviewed plan sequentially for
Codex, Pi, Antigravity CLI, and Grok CLI. All four plan-bound receipts reached
`verified`, and `verify-all` returned the exact four-target order. The first
isolated Pi adversarial Review then returned sanitized `BLOCKED` evidence,
without a business verdict, because the production sandbox allowed the
declared Pi wrapper and its shebang but not the wrapper's bound second-stage
Node executable. No raw Pi output, help/version fallback, native Pi state, or
network access was used.

Before correction, the implementation, tests, prompt, and source-verification
record were copied to
`/private/tmp/add-role-first-review-routing-p1r6-20260820-LAJf5S`, a private
mode-`0700` root. The direct mode-`0600` backups are:

| Backup | SHA-256 |
|---|---|
| `validate_cross_cli_sync.py.before` | `332de6171495faa12b3acd6c7c39e8ee35972a9c87eebe216d9581cc3b520044` |
| `test_cross_cli_sync.py.before` | `97d46aec7247ab9e0f93d60b2c017248e22e4b54d2c53f3f01eaa83d0c9b1ed2` |
| `source-verification.md.before` | `52bca43ed01b18f959f3afe6bca22016d98cf584737a0ef88d0107cc3cc6050b` |
| `pi-adversarial-review-prompt.md.before` | `9cba75f75a714110d5efa3a9ff21112f51367a6626e3fdaea596b16544ff04c1` |

### Root cause, fail-closed launcher binding, and TDD boundary

The Pi executable is a small `/bin/sh` wrapper that executes an absolute Node
runtime and an absolute package entrypoint. `_probe_exec_chain` previously
stopped at the shebang, so the sandbox denied the actual Node `process-exec`.
Allowing the wrapper alone was insufficient; macOS `/bin/sh` also consults a
dynamic shell variant, which would require a wider and mutable shell execution
surface.

Three tests were written before the production correction. Their RED run
produced six expected failures and zero errors: the bound second-stage runtime,
entrypoint, and package subtree were absent; four ambiguous launchers were
accepted; and the real two-stage sandbox path could not return valid evidence.
The correction now:

- reads a bounded UTF-8 shell launcher and accepts either an empty shell stub
  used only for pure contract tests or exactly one `exec` command;
- requires an absolute executable runtime, an absolute regular non-symlink
  package entrypoint, and exact `"$@"` forwarding, while rejecting extra
  commands, relative paths, missing forwarding, and linked entrypoints;
- binds the nearest valid named `package.json`, the resolved runtime and
  entrypoint, and only the required package/runtime read roots;
- executes the validated resolved runtime and entrypoint directly, eliminating
  the wrapper/shell variant from the live process-exec surface;
- retains the fresh temporary `HOME`/`PI_CODING_AGENT_DIR`, read-root
  allowlist, native-root read/write denial, network denial, schema-only output,
  and sanitized fail-closed result.

The same three tests plus both existing Pi probe tests passed GREEN. A pure
production-contract check against the actual launcher resolved the first two
argv entries to the bound Homebrew Node binary and Pi package CLI, found both
in the generated profile, and retained native-root and network denial. It did
not launch Pi.

Current corrected hashes are:

- `scripts/validate_cross_cli_sync.py`:
  `98b759b3f47057006e1128a9e671f55c51ad08a274db43fa4504d4b035cc411d`;
- `tests/test_cross_cli_sync.py`:
  `f3f290f44c440adcbd78e75364e093382d075c86c7f81b2f50440c007f27eb8c`.

### Fresh sixth-correction verification

- Router quick/project validation: `PASS`;
- cross-CLI module: `94` tests, `OK`;
- Router full suite: `218` tests, `OK`;
- Companion quick/project validation: `PASS`;
- Companion full suite: `87` tests, `OK`;
- change/all OpenSpec strict validation: `PASS`, `3 passed / 0 failed`;
- both exact policy-negative searches: empty;
- shared Handoff/validator-core byte checks: `PASS`;
- path-only sensitive audit: `0 sensitive categories found`;
- isolated natural forward run: `forward: "pass"`, six result rows all
  `PASS`, transient root absent;
- private forward summary mode/SHA-256: `0600` /
  `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b`.

One earlier parallel-validation artifact was found by the complete delta as an
unexpected project-root `antigravity-cli/skills` transaction tree. Its birth
time preceded this correction and it contained only generated test/probe
placeholders. It was moved intact, rather than deleted, to the private R6
backup root as `unexpected-test-artifact-r6`. Fresh per-test cross-CLI replay
did not reproduce it, the project-root path is absent, and it was not added to
the allowlist.

### Fresh complete source delta after the sixth correction

The first R6 source-delta invocation correctly stopped before writing an
output because the unexpected generated transaction tree was outside the
allowlist. It created only the new private mode-`0700` compare root
`source-compare-r6`. After the recoverable move above, a retry with new output
and compare paths passed:

- private delta: `source-delta-r6-retry1.json`, mode `0600`, SHA-256
  `6e89942768da96045c14645dfb196d2fe89e4877c963acaa676152e0c66c32ae`;
- successful compare root: `source-compare-r6-retry1`, mode `0700`;
- binding: `preflight-source-bindings-r6.json`, mode `0600`, SHA-256
  `08af96bf93646d8a5f04cd25a5fe342c7237633172755b41c24128c4ae9950f3`;
- allowlist: `70` entries, mode `0600`, SHA-256
  `7e9bc9e8ecd2cff5a9a1d35be32596533e7a4ed5340e3c25a9978a9eb37f454d`;
- actual changed paths: `66` (`52` Router, `14` Companion);
- result: `source_delta: "pass"`, `unexpected_paths: []`.

The durable path/status/SHA/mode-only copy is
`docs/design/evidence/add-role-first-review-routing/2026-08-20-source-delta-p1-r6-summary.json`
with SHA-256
`23485e9b237e218fc2bdbcfab305f41e5e62c5b400d533f24fd9a94a58b104a3`.
This append, the durable summary, and the P1 R6 Review input are evidence-only
post-delta records. Because the source changed after runtime deployment, all
existing runtime plans and receipts are stale for further apply. A fresh
independent Candidate Source High Review must return explicit `PASS` before a
new read-only plan and Sync-plan Review may authorize re-synchronization.

## Sixth-review timeouts, byte-drift finding, and seventh correction

Three fresh Luna Max Candidate Source Review attempts were started read-only
against the bound P1 R6 input. Each was interrupted only after prolonged tool
silence and produced no Review result. No timeout was accepted as `PASS`,
`FAIL`, or `BLOCKED`, and no R6 Review artifact was created. Runtime planning
remained forbidden.

The control plane then independently reproduced a P1 production defect in a
temporary root: after `build_pi_probe` validated the package entrypoint but
before `execute_pi_probe` called `subprocess.run`, an adversarial interleave
replaced the entrypoint's valid `BLOCKED` program with a valid `PASS` program.
Production returned `success=True` and accepted `PASS`. The R6 correction bound
paths and permissions, but not the bytes actually executed after build.

Before correction, the R6 implementation, tests, verification, and Review
input were copied to
`/private/tmp/add-role-first-review-routing-p1r7-20260820-kvklRO`, a private
mode-`0700` root. The mode-`0600` preimages are:

| Backup | SHA-256 |
|---|---|
| `validate_cross_cli_sync.py.before` | `98b759b3f47057006e1128a9e671f55c51ad08a274db43fa4504d4b035cc411d` |
| `test_cross_cli_sync.py.before` | `f3f290f44c440adcbd78e75364e093382d075c86c7f81b2f50440c007f27eb8c` |
| `source-verification.md.before` | `55c1c272e51664acaaa8b38cb19dff6c3754f1c333ddab27da1c3b4a11e8e62b` |
| `source-rereview-p1-r6-inputs.md.before` | `19028bc40ec123ce5ed89a0cd76c219b3957db1e05a61289a71577a7bdb60231` |

### Private snapshot correction and TDD

Five focused cases first failed RED: the contract had no snapshot descriptor;
the original package remained live-readable; an escaping package symlink was
accepted; persistent source drift changed the accepted verdict; and snapshot
drift was not detected. The correction now:

- inventories every package directory, regular-file SHA/executable bit, and
  internal relative symlink, rejecting special files, absolute links, broken
  links, and links escaping the package;
- binds the named package's semantic inventory SHA before execution;
- copies the complete package with symlinks un-followed into a fresh private
  temporary snapshot, requires source-before/source-after/snapshot digests to
  agree, and converts snapshot directories/files to exact read-only modes;
- executes the resolved runtime against the snapshot entrypoint, removes the
  original package from live sandbox read rules, and explicitly denies writes
  to the snapshot below the otherwise writable temporary root;
- rechecks runtime bytes, snapshot bytes/types/links/modes, and every reviewed
  source-root digest after the process; any drift overrides otherwise valid
  stdout with sanitized `BLOCKED` evidence.

The five RED cases and both earlier probe integration cases passed GREEN. A
real-package materialization check, without launching Pi, bound the current
131 MB package in about nine seconds, executed from the temporary snapshot
path, excluded the original package from live read rules, and verified mode
`0555` at the snapshot root.

Corrected hashes:

- `scripts/validate_cross_cli_sync.py`:
  `1c373f5eb6ade5eaa8c0c4750e09a7f0726f25b87dc574775d6408edf73ec642`;
- `tests/test_cross_cli_sync.py`:
  `be2c1016a22c1f4e4db8a091e5550a784fe0415b18542a805075891ef75820e0`.

### Fresh seventh-correction verification and delta

- Router quick/core/full: `PASS`, `220` tests `OK`;
- Companion quick/templates/full: `PASS`, `87` tests `OK`;
- OpenSpec strict/all: `PASS`, `3 passed / 0 failed`;
- exact negative searches, shared-byte tests, and sensitive audit: `PASS`;
- forward cases: `6/6 PASS`, transient root absent; summary mode/SHA `0600` /
  `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b`;
- complete source delta: `68` actual paths (`54` Router, `14` Companion),
  `73` allowlisted, `unexpected_paths: []`;
- private delta: `source-delta-r7.json`, mode `0600`, SHA-256
  `2f59d1d5ee658869be9afada9e1b510dfcedf6ccc1b47cbababb87c8fcc8d161`;
- binding: mode `0600`, SHA-256
  `6679c9f7ff3520b894445dcfac3ee33bcbd6362f6fe891c2fb24c15b6ece5243`;
- allowlist: mode `0600`, SHA-256
  `f4f513c5012524c418b92418e732be6550e45e074c6d8b5bfc9adfb25c274f1a`;
- compare root: mode `0700`.

The durable R7 summary is
`docs/design/evidence/add-role-first-review-routing/2026-08-20-source-delta-p1-r7-summary.json`,
SHA-256
`74c04c0e28052f3165ebab5f86469099f925ac10e153caea780f559660b27016`.
This append, the durable summary, and the R7 Review input are evidence-only
post-delta records. A fresh independent Candidate Source High Review must
return explicit `PASS` before any runtime planning or deployment may resume.

## Runtime Sync-plan High Review FAIL and fifth correction

The fresh Luna Max runtime Sync-plan High Review was persisted without changing
its decision:

- artifact:
  `docs/design/reviews/2026-08-20-add-role-first-review-routing-runtime-sync-plan-review.md`;
- artifact mode/SHA-256: `0644` /
  `8562b0ed1d4ef17dc34f100e783e72b02ae40138f8888b7516ef2566ecb255a8`;
- verdict: `FAIL`;
- P1 finding: caller-supplied runtime backup and transaction roots were checked
  for private modes, but not mechanically rejected when resolved inside any
  declared Skill discovery root.

The Review confirmed that no actual runtime mutation, Git, or Pi operation had
begun. Before correction, the affected implementation, test, and evidence files
were copied to
`/private/tmp/add-role-first-review-routing-p1r5-20260820-WeKcZW`, a private
mode-`0700` root. The direct backups are regular mode-`0600` files:

| Backup | SHA-256 |
|---|---|
| `validate_cross_cli_sync.py.before` | `8d8a18a4c6d9a7639fe963e08c1a799b0c5a531129fd6195c8cd9fd8c4315f1e` |
| `test_cross_cli_sync.py.before` | `15f787aa7f0e23fd60611d3d0c5639b1541aba7b760fd88d93efe635f8a37aa3` |
| `source-verification.md.before` | `bbcf2cc726876409aae30b7cac577a198e8341593c04b74f5f4084caeab84f95` |

### Root cause, containment correction, and TDD boundary

`apply_target` previously created or opened the transaction root before any
discovery-root containment check, and `_prepare_target_backup` created the
backup root after validating only its private-directory properties. Restore,
recovery, verification, discovery, commit, and verify-all paths used the same
unbound transaction-root assumption.

Two production-path tests were written before the correction. Across the four
declared target discovery roots they produced eight expected RED failures: both
an in-discovery backup root and an in-discovery transaction root were accepted
instead of rejected before mutation.

The correction adds one shared resolved-containment guard. It checks a proposed
backup or transaction root against every plan-bound `skills_root`, including
existing symlink resolution, before any private root, lock, backup, receipt, or
destination is created or changed. `apply_target`, `_prepare_target_backup`,
the transaction lock, restore, recovery, verification, discovery, commit, and
verify-all reuse this guard. The same two tests then passed GREEN for all eight
subcases and prove that the unsafe roots, receipts, backups, and destination
changes remain absent.

The complete cross-CLI module passed `91` tests. The Router full suite passed
`215` tests. Current corrected hashes are:

- `scripts/validate_cross_cli_sync.py`:
  `332de6171495faa12b3acd6c7c39e8ee35972a9c87eebe216d9581cc3b520044`;
- `tests/test_cross_cli_sync.py`:
  `97d46aec7247ab9e0f93d60b2c017248e22e4b54d2c53f3f01eaa83d0c9b1ed2`.

### Fresh fifth-correction verification

- Router quick/project validation: `PASS`;
- Router unit suite: `215` tests, `OK`;
- Companion quick/project validation: `PASS`;
- Companion unit suite: `87` tests, `OK`;
- change/all OpenSpec strict validation: `PASS`, `3 passed / 0 failed`;
- both exact policy-negative searches: empty;
- shared Handoff/validator-core byte checks: `PASS`;
- path-only sensitive audit: `0 sensitive categories found`;
- isolated natural forward run: `forward: "pass"`, six result rows all
  `PASS`;
- private forward summary mode/SHA-256: `0600` /
  `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b`;
- transient forward root after completion: absent.

The historical reviewed Conda interpreter remains unavailable. The quick
validators used the previously accepted `/opt/anaconda3/bin/python`; project
validators and tests used dependency-free default `python3`. This is not
represented as an exact replay of the unavailable interpreter.

### Fresh complete source delta after the fifth correction

The exact new source-delta transaction passed:

- private delta:
  `/private/tmp/add-role-first-review-routing-p1r5-20260820-WeKcZW/source-delta-r5.json`;
- private delta mode/SHA-256: `0600` /
  `9c094d37cc8a3d9994b0b255a2b2e8ff94a3440c306eb13690846d2a37da57a0`;
- compare root mode: `0700`;
- binding mode/SHA-256: `0600` /
  `8bdf40b33323b4d8c3f197946935d2e9d958fe7b418fa8e06393657c914cc9e6`;
- allowlist: `64` entries, mode `0600`, SHA-256
  `6f4c8b5b8fcd02edadc3eafcd74bf80930c4f83a5988525634152ba53b74a005`;
- actual changed paths: `60` (`46` Router, `14` Companion);
- result: `source_delta: "pass"`, `unexpected_paths: []`.

The durable path/status/SHA/mode-only copy is
`docs/design/evidence/add-role-first-review-routing/2026-08-20-source-delta-p1-r5-summary.json`
with SHA-256
`8dfb1971406017fa388ee96eb8c309fef39c33089069703e468e9f8e3afdadac`.
This source-verification append, the durable summary, and the P1 R5 Review
input are evidence-only post-delta records. Runtime apply remains forbidden
until a fresh independent Candidate Source High re-review returns explicit
`PASS`, the control plane accepts it, a new runtime plan is generated, and a
fresh independent Sync-plan High Review returns explicit `PASS`.

## P1 R3 Review FAIL and fourth correction

The fresh independent Candidate Source High Re-review P1 R3 returned `FAIL`
with one P1 finding and was persisted verbatim at
`docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r3.md`.
Its SHA-256 is
`c451abf26592caa0630f8d3b2d272e740ddde40d959cccc79f5d672d4b379c47`.
The Review confirmed the first three correction generations except for the
restore-time binding of transaction-created parent evidence: a planned
`logical_path` could be paired with a different internally valid `path` and
directory `chain`, allowing unrelated cleanup and a false `restored` receipt.
Runtime planning remained blocked.

Before the fourth correction, the implementation, cross-CLI tests, and this
source-verification record were backed up under
`/private/tmp/add-role-first-review-routing-p1r4-20260820-7X9r4J`.
The backup directory is mode `0700`; its three direct backup files are mode
`0600` and preserve the pre-correction SHA-256 values
`a6420e3ee88a606a0ccf963fe04d7725d53e995526d76abb07a8bef8ca307202`,
`fbb702da40475a442c6abe6ea98ce4e337f8d6751a405853fd38f7abc64a2f95`,
and `fba7622846aecde308a7289958056b54aee0781b3af4a99ab2d2f4fe6a038f4a`.

The fourth correction used TDD. The focused RED run had three expected
failures and zero errors: semantic logical-path/path/chain substitution,
record reordering, and truncated chain provenance were all incorrectly
accepted. The missing/extra-record case already failed closed. After the
production correction, all focused cases passed, together with real crash
recovery and Pi target-local failure isolation.

The production correction now:

- derives the deterministic, de-duplicated transaction-created-parent order
  from the bound backup manifest and validates every per-entry hierarchy;
- requires `prepared` receipts to have no records,
  `applied-uncommitted` receipts to contain the exact full planned sequence,
  and `mutation-intent` recovery to contain only the exact deterministic
  created prefix while rejecting any present unrecorded planned directory;
- resolves every recorded logical path before any restore mutation and
  requires its resolved absolute path to equal the recorded path;
- recaptures the complete root-to-directory chain and requires exact equality
  with the recorded chain, including device, inode, mode, owner, and group;
- rejects duplicate final directory identities, reordered records,
  hierarchy/path substitutions, truncated provenance, missing/extra records,
  and empty or non-empty unrelated directories before changing target bytes;
- retains the existing recovery-blocked and later-target exclusion semantics
  on any rejection.

The expanded cross-CLI module passed `89` tests. Current corrected hashes are:

- `scripts/validate_cross_cli_sync.py`:
  `8d8a18a4c6d9a7639fe963e08c1a799b0c5a531129fd6195c8cd9fd8c4315f1e`;
- `tests/test_cross_cli_sync.py`:
  `15f787aa7f0e23fd60611d3d0c5639b1541aba7b760fd88d93efe635f8a37aa3`.

The governed `scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc`
path remains absent.

### Fresh fourth-correction verification

Fresh results after the fourth correction:

- Router quick/project validation: `PASS`;
- Router unit suite: `213` tests, `OK`;
- Companion quick/project validation: `PASS`;
- Companion unit suite: `87` tests, `OK`;
- change/all OpenSpec strict validation: `PASS`, `3 passed / 0 failed`;
- both exact Task 6 negative searches: empty;
- shared Handoff/validator-core byte checks: `PASS`;
- path-only sensitive audit: `0 sensitive categories found`;
- isolated natural forward run: `forward: "pass"`, six result rows all
  `PASS`;
- private forward summary mode/SHA-256: `0600` /
  `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b`;
- transient forward root after completion: absent.

### Fresh complete source delta after the fourth correction

The first fourth-correction source-delta invocation used the bound preflight
inventory files as the source-start baseline arguments and failed before
writing an output JSON with `source inventory fields are invalid`. It created
only the new private mode-`0700` compare root
`/private/tmp/add-role-first-review-routing-p1r4-20260820-7X9r4J/source-compare-r4`.
That failure is retained. No source, baseline, backup, or existing evidence was
changed.

The diagnosed cause was an argument-shape mismatch: preflight inventories
include `excluded_paths`, while source-start baselines use the three-field
inventory schema. The retry used the bound reconstructed source-start
baselines and wrote new paths. It passed:

- private delta:
  `/private/tmp/add-role-first-review-routing-p1r4-20260820-7X9r4J/source-delta-r4-retry1.json`;
- private delta mode/SHA-256: `0600` /
  `235a4a44eb344f6f0ea96137546c26d7b3d0a7b2f250bc3ab17e7ad1c43834ec`;
- successful compare root mode: `0700`;
- binding mode/SHA-256: `0600` /
  `dc6034f8c151d53857b0d78e5417fbff2e5dd8d66e710a2ec6f9f731a20059ae`;
- allowlist: `58` entries, mode `0600`, SHA-256
  `c170a3530a13c7aee65ec28b2c64ff16d545fa804ef8569ed9cc3eda5f235ff5`;
- actual changed paths: `54` (`40` Router, `14` Companion);
- result: `source_delta: "pass"`, `unexpected_paths: []`.

The durable path/status/SHA/mode-only copy is
`docs/design/evidence/add-role-first-review-routing/2026-08-20-source-delta-p1-r4-summary.json`
with SHA-256
`6028f0c3b1d457b516226374fc942adc4e160ac8771d7eb72ce8827c27692127`.
This appended source-verification section, the durable summary, and the new P1
R4 Review input are evidence-only post-delta records. They do not authorize
runtime planning. A fresh independent Candidate Source High Re-review must
return explicit `PASS` and be accepted by the original control plane before
Task 8 may begin.

## Candidate source High Re-review P1 R2 FAIL and third correction

The fresh independent P1 R2 re-review was persisted without changing its
decision:

- artifact:
  `docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r2.md`;
- artifact SHA-256:
  `5991be2198f4387bb0e860733352fb98e063e22bfcd694eacd3f4704932429b3`;
- verdict: `FAIL`;
- P1 findings: initially absent parents were created before descriptor binding;
  restore cleanup used unbound path-string `rmdir`; and a failed rollback after
  receipt-history installation could leave a live `verified` revision without
  a blocker recognized by later-target gates.

No runtime destination was inspected or changed and no runtime plan, Git, or
Pi operation began. Before correction, the affected implementation, test, and
evidence files were copied to
`/private/tmp/add-role-first-review-routing-p1r3-20260820-3nND1z`, a private
mode-`0700` root. The direct backups are regular mode-`0600` files:

| Backup | SHA-256 |
|---|---|
| `router/validate_cross_cli_sync.py` | `cef9fca193364a8ccda204fb80a351a656ac5e22c2919c96ecbf28fc7203f4ff` |
| `router/test_cross_cli_sync.py` | `95797ae3a2db091661f094c742a9247d098789ff1e453388580f61241e3ac1c8` |
| `router/source-verification.md` | `92a0593203886fe8919d7c7ee8b7ab3313d4e9fa92a81382af0089b876c0e546` |

### Root cause, transaction correction, and TDD boundary

The third correction makes initially absent directory creation part of the
same descriptor-bound transaction as leaf installation:

- creation starts from a verified existing ancestor descriptor;
- each missing component is created exclusively relative to that descriptor,
  opened no-follow, and bound by device, inode, mode, UID, GID, and complete
  canonical directory chain;
- `created_parent_records` are durably appended to the mode-`0600` transaction
  receipt while it remains `mutation-intent`, before candidate leaf install;
- every later leaf install reopens and rechecks those recorded identities and
  retains the final parent descriptor through exclusive installation;
- unrecorded but present planned parents make recovery fail closed.

Restore now validates the exact durable parent records, removes directories in
reverse depth order by descriptor-relative exclusive quarantine, validates the
actual quarantined directory identity, and removes only the exact empty object.
Identity/type/mapping drift or non-empty state is rolled back when unambiguous;
otherwise the quarantine is preserved and recovery becomes blocked. Final
absence is rechecked from the recorded top-level anchor chain. Path-string
`rmdir` and ignored cleanup errors are no longer used.

Receipt history transitions now install a durable mode-`0600`
`manual-disposition` blocker before moving the displaced receipt into history.
The blocker is removed only after the history move, directory durability, and
parent identities are proven, or after an exact successful rollback. A failed
or ambiguous rollback retains the blocker; apply, restore, verification,
commit, recovery, later-target, and verify-all gates reject such transaction
evidence even if the live receipt bytes serialize state `verified`.

Five focused tests were written before production correction. The correctly
targeted RED run produced five expected failures and zero errors, then the same
five passed GREEN. An earlier command typo named a nonexistent unittest class
and produced five loader errors without executing a project test; it was
corrected immediately and is not counted as RED evidence. Three additional
GREEN cases cover parent type substitution, non-empty parent preservation, and
successful post-history rollback cleanup. The eight new cases cover:

- missing multilevel-parent mapping, link, and type changes before install;
- durable identity records for every transaction-created parent;
- mapped replacement and non-empty created-parent restore branches;
- failed post-history rollback with durable later-target exclusion;
- successful post-history rollback with exact blocker cleanup.

The full cross-CLI module passed `84` tests. Current corrected hashes are:

- `scripts/validate_cross_cli_sync.py`:
  `a6420e3ee88a606a0ccf963fe04d7725d53e995526d76abb07a8bef8ca307202`;
- `tests/test_cross_cli_sync.py`:
  `fbb702da40475a442c6abe6ea98ce4e337f8d6751a405853fd38f7abc64a2f95`.

A local syntax-only check unintentionally generated exactly
`scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc`. Its creation time
and exact path were verified, then only that newly created cache file was
removed. The historical `cpython-311.pyc` file was not changed. The fresh
complete source delta below confirms the governed `cpython-314.pyc` path is
absent and reports no additional cache path.

### Fresh third-correction verification

Fresh results after the third correction:

- Router quick/project validation: `PASS`;
- Router unit suite: `208` tests, `OK`;
- Companion quick/project validation: `PASS`;
- Companion unit suite: `87` tests, `OK`;
- change/all OpenSpec strict validation: `PASS`, `3 passed / 0 failed`;
- both exact Task 6 negative searches: empty;
- shared Handoff/validator-core byte checks: `PASS`;
- path-only sensitive audit: `0 sensitive categories found`;
- isolated natural forward run: six result rows, all `PASS`;
- private forward summary mode/SHA-256: `0600` /
  `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b`;
- transient forward root after completion: absent.

### Fresh complete source delta after the third correction

The exact new source-delta transaction passed:

- private delta:
  `/private/tmp/add-role-first-review-routing-p1r3-20260820-3nND1z/source-delta-r3.json`;
- private delta mode/SHA-256: `0600` /
  `8a60ac663085bc765e49a30e47a1a19d10bbf3c19a78a574c6a0aa116fe027d8`;
- compare root mode: `0700`;
- binding mode/SHA-256: `0600` /
  `bdbfa99b93bd17ff86c61a2f119b1c07a74785fb868519d80e1f5ed9f5060d6f`;
- allowlist: `55` entries, mode `0600`, SHA-256
  `cfa09d50b6c83e13d252ddd4f9bdbbced55dcc86503ee6bbccad8b50c95eb847`;
- actual changed paths: `51`;
- result: `source_delta: "pass"`, `unexpected_paths: []`.

The durable path/status/SHA/mode-only copy is
`docs/design/evidence/add-role-first-review-routing/2026-08-20-source-delta-p1-r3-summary.json`
with SHA-256
`6b02a2a5a97155b80d0cff2a02efcdcfd73537719645b5e35a2c9f9095ea447c`.
This appended evidence record, the durable summary, and the new P1 R3 review
input are evidence-only post-delta records. They do not change the candidate
implementation and do not authorize runtime planning. A fresh independent
Candidate source High Review must still return `PASS` and be accepted by the
original control plane before Task 8 may begin.

## Candidate Source High Re-review P1 R7 FAIL and eighth correction

The fresh no-history Luna Max P1 R7 Review was persisted without changing its
decision:

- artifact:
  `docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r7.md`;
- artifact mode/SHA-256: `0644` /
  `399bff18097231d069bf597edcef9e0ebacd358e7e636e40974006fdab784e44`;
- verdict: `FAIL`;
- P1 finding 1: a shell launcher whose resolved runtime remained inside the
  original package could execute that unsnapshotted runtime while the
  entrypoint alone came from the private snapshot;
- P1 finding 2: setup, snapshot, read-root, and subprocess-launch exceptions
  occurred before the sanitized result boundary, so the CLI could expose raw
  exception paths and omit the mode-`0600` Review evidence artifact.

No runtime destination, Git, or Pi operation was started. Before correction,
the affected source, tests, source-verification evidence, R7 input, and R7
Review were copied to the private mode-`0700` root
`/private/tmp/add-role-first-review-routing-p1r8-20260820-9yiUoW`; every direct
backup is a regular mode-`0600` file.

### Runtime binding and sanitized-failure correction

The eighth correction rejects a resolved launcher runtime that is contained by
the entrypoint package before any snapshot or process contract can be accepted.
The real supported launcher shape keeps its runtime outside the package and
continues to execute the read-only snapshot entrypoint.

Pi execution is now split into an exception-producing internal operation and a
single public fail-closed boundary. Any setup, snapshot, read-root, launch, or
result-persistence exception becomes the same fixed-schema `BLOCKED` result.
When the declared output path is usable, the boundary creates it exclusively,
fsyncs it, and enforces mode `0600`. The `probe-pi` CLI exception path prints
only the static blocked schema and never interpolates the raw exception.

Three focused regressions were written before production correction. The
package-contained-runtime case first failed because no exception was raised.
The setup/launch pair then produced one expected failure and one expected error:
the CLI exposed its missing path and wrote no artifact, while the direct launch
exception escaped. After correction all three passed GREEN. The full
cross-CLI module passed `99` tests.

Corrected hashes:

- `scripts/validate_cross_cli_sync.py`:
  `92c8c13889dd6613fa8d224b0fcddd63db841be8720a63e5a00c08ff4fd4581a`;
- `tests/test_cross_cli_sync.py`:
  `3a5c08f805df17764c641f93123187eb95200717eb4654c4de208e4c988a5556`.

### Fresh eighth-correction verification and delta

- Router quick/core/full: `PASS`, `223` tests `OK`;
- cross-CLI module: `PASS`, `99` tests `OK`;
- Companion quick/templates/full: `PASS`, `87` tests `OK`;
- OpenSpec strict/all: `PASS`, `3 passed / 0 failed`;
- both exact policy-negative searches, shared Handoff/validator-core byte
  checks, and path-only sensitive audit: `PASS`;
- isolated forward cases: `6/6 PASS`, transient root absent; private summary
  mode/SHA-256 `0600` /
  `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b`;
- complete no-Git source delta: `71` actual paths (`57` Router, `14`
  Companion), `76` allowlisted, `unexpected_paths: []`;
- private delta mode/SHA-256: `0600` /
  `382b9b5b5b4802b24f012df449177a5bce6837948762110642d061e19e6ca700`;
- private bindings mode/SHA-256: `0600` /
  `ad7152453735b7eebdde1a9e30667cc048850f16581f47516436b14720e86c0a`;
- private allowlist mode/SHA-256: `0600` /
  `4f36ff2a983b801bbc12c9612b92d36217e268520a250a7d352e5b964c0cd018`;
- compare root: mode `0700`.

The durable path/status/SHA/mode-only copy is
`docs/design/evidence/add-role-first-review-routing/2026-08-20-source-delta-p1-r8-summary.json`,
SHA-256
`e237004079db66d11364547d1702cc374e024e6d635abe6115d849c2a03fdcd8`.
This source-verification append, the durable summary, and the P1 R8 Review
input are evidence-only post-delta records. They do not authorize runtime
planning. A fresh independent Candidate Source High Re-review must return
explicit `PASS` before runtime planning or deployment may resume.

## Candidate Source High Re-review P1 R8 FAIL and ninth correction

The fresh no-history Luna Max P1 R8 Review was persisted without changing its
decision:

- artifact:
  `docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r8.md`;
- artifact mode/SHA-256: `0644` /
  `c99d1206f7666d8dbd67c8bc480649b0c1cadabaf75e6a4395e8f1138f31f5ad`;
- verdict: `FAIL`;
- P1 finding 1: a package file hard-linked to an outside launcher runtime
  satisfied the path-containment rule while sharing the same mutable inode;
- P1 finding 2: the reviewed-tree digest represented every symlink by a
  constant marker and therefore did not bind the link target;
- P1 finding 3: a directory-fsync failure after Review artifact installation
  returned `BLOCKED` but could leave a live mode-`0600` `PASS` artifact.

No runtime destination, Git, or Pi operation was started. Before correction,
the affected source, tests, source-verification evidence, R8 input, and R8
Review were copied to the private mode-`0700` root
`/private/tmp/add-role-first-review-routing-p1r9-20260820-4TSC3a`; every direct
backup is a regular mode-`0600` file.

### Identity, reviewed-tree, and evidence-transaction correction

The ninth correction binds the resolved launcher runtime by device and inode
and rejects any regular file in the package inventory that aliases that
identity. The comparison is enforced during the same inventory used for the
private snapshot, so an alias present before or during inventory cannot enter
the reviewed execution package.

The reviewed-tree digest now rejects every symlink before launch. This removes
the retargetable object from the supported reviewed-root contract instead of
claiming that a constant link marker proves immutable reviewed bytes.

Pi result persistence now uses a verified output parent, a private same-directory
candidate, exclusive rename, directory fsync, and exact-prestate guarded cleanup.
If any post-install durability step fails, the public operation remains
`BLOCKED` and removes only the exact artifact it installed; candidate cleanup is
also bounded to the exact hidden file. Collision and parent-drift paths fail
closed without overwriting an existing artifact.

Three focused regressions were written before production correction. The RED
run produced three expected failures: the hard-linked runtime alias was
accepted, the reviewed symlink was accepted, and fsync failure left the output
artifact. The same three passed GREEN after correction. The full cross-CLI
module passed `102` tests.

Corrected hashes:

- `scripts/validate_cross_cli_sync.py`:
  `e847f1c7cc73cd2c4b3fc4cf3ee3bfb8369fd431feb1bdf632f6654ff16d280f`;
- `tests/test_cross_cli_sync.py`:
  `d77e19b190a4887b30e954f7c284d43ae3f66d13b3755707fce7986229010c5d`.

### Fresh ninth-correction verification and delta

- Router quick/core/full: `PASS`, `226` tests `OK`;
- cross-CLI module: `PASS`, `102` tests `OK`;
- Companion quick/templates/full: `PASS`, `87` tests `OK`;
- OpenSpec strict/all: `PASS`, `3 passed / 0 failed`;
- both exact policy-negative searches, shared Handoff/validator-core byte
  checks, and path-only sensitive audit: `PASS`;
- isolated forward cases: `6/6 PASS`, transient root absent; private summary
  mode/SHA-256 `0600` /
  `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b`.

One unguarded local Python probe regenerated exactly the governed
`scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc` after the R9
backup. The event was detected by the first delta, and only that exact generated
file was recoverably moved to the private backup root as
`generated-validate_cross_cli_sync.cpython-314.pyc` (mode/SHA-256 `0600` /
`0d5a538b7d5729a1dc19177b6a50566b82a13d0e088f54e514a194ef12b6ce18`).
The source cache path is absent. The retained first delta is classified
non-authoritative evidence (mode/SHA-256 `0600` /
`64aca2527cf0f1e513054ac29ab406958cd1de81cc6206e4176396ddacf73dc4`).

The bytecode-disabled authoritative retry passed:

- private delta:
  `/private/tmp/add-role-first-review-routing-p1r9-20260820-4TSC3a/source-delta-r9-retry1.json`;
- private delta mode/SHA-256: `0600` /
  `a16ef355cd8ecfb59fed2dfbfd46e370557c9c3b44373d220744f2b02e62237e`;
- compare root mode: `0700`;
- binding mode/SHA-256: `0600` /
  `a3b48b4cb204204cf0641997b923be5f619080885e06676ca7aec2035a1ddc9d`;
- allowlist: `79` entries, mode `0600`, SHA-256
  `cceb69b843e569f7c99189346e8ced845862fc8e4421c2c8b46c135e86196fc9`;
- actual changed paths: `74` (`60` Router, `14` Companion);
- result: `source_delta: "pass"`, `unexpected_paths: []`.

The durable path/status/SHA/mode-only copy is
`docs/design/evidence/add-role-first-review-routing/2026-08-20-source-delta-p1-r9-summary.json`,
SHA-256
`479ec0c6677195aa1174f60495a398daaf170974aa80e482ac5f74f40fc91ec6`.
This source-verification append, the durable summary, and the P1 R9 Review
input are evidence-only post-delta records. They do not authorize runtime
planning. A fresh independent Candidate Source High Re-review must return
explicit `PASS` before runtime planning or deployment may resume.

## Candidate Source High Re-review P1 R9 FAIL and tenth correction

The fresh no-history Luna Max P1 R9 Review was persisted without changing its
decision:

- artifact:
  `docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r9.md`;
- artifact mode/SHA-256: `0644` /
  `9d563300e93c63f55cfce321c90712e1e329c0ada45e38270a7ffaa856377fcf`;
- verdict: `FAIL`;
- P1 findings: runtime identity was not revalidated after package inventory;
  resolving a raw reviewed root hid a top-level symlink; regular-file mode was
  omitted from the reviewed digest; rollback/candidate cleanup failures could
  retain accepted `PASS` or hidden candidate bytes; and the retained first R9
  delta hash was recorded incorrectly.

No runtime destination, Git, or Pi operation was started. Before correction,
the affected source, tests, source-verification evidence, R9 input, R9 Review,
and R9 durable summary were copied to the private mode-`0700` root
`/private/tmp/add-role-first-review-routing-p1r10-20260820-Bun7oJ`; every
direct backup is a regular mode-`0600` file.

### Runtime, reviewed-tree, and persistence correction

Runtime binding now opens the exact file no-follow, hashes it through the open
descriptor, and binds device, inode, mode, UID, GID, size, modification time,
and content before and after the descriptor read. Package inventory is run
twice with the forbidden runtime identity and the runtime binding is rechecked
after each pass. The resulting binding is carried into the private launcher
snapshot contract and rechecked before snapshotting, after snapshotting,
immediately before process launch, and after process return. A runtime path
changed during or after inventory therefore cannot become the accepted
launcher.

The raw reviewed-root path is digested before any resolution. A top-level
symlink is rejected, as is every nested symlink. Root, directory, and regular
file identities and modes are included in the digest; regular files are read
through no-follow descriptors with before/after identity checks. The original
logical root is retained for the post-process digest, so root mapping, file
identity, mode, or content drift changes the bound result to `BLOCKED`.

Pi evidence persistence still uses a verified parent, private same-directory
candidate, exclusive rename, directory fsync, and exact-prestate rollback. If
unlinking an installed `PASS` artifact fails, the exact bound inode is
descriptor-rewritten and fsynced as the fixed `BLOCKED` schema. If a hidden
candidate cannot be unlinked, its exact bytes are first neutralized to
`BLOCKED`, then exclusively renamed to a visible persistence-blocked quarantine
and deleted when possible. Persistent unlink failure may retain only the
explicit mode-`0600` blocked quarantine; it cannot retain accepted `PASS` bytes
or a `.cross-cli-sync.*` candidate.

Five focused regressions reproduced all technical findings against the R9
preimage: runtime alias creation during inventory, top-level reviewed-root
symlink, regular-file mode drift, rollback unlink failure, and persistent
candidate unlink failure. The first runtime test initially failed to trigger
because macOS canonicalized `/var` to `/private/var`; the path comparison was
corrected, then the R9 preimage produced the expected RED failure. The complete
five-case RED boundary and the same five GREEN cases are preserved. The full
cross-CLI module passed `107` tests.

The retained first R9 delta is now bound to its actual reproducible mode/SHA:
`0600` /
`64aca2527cf0f1e513054ac29ab406958cd1de81cc6206e4176396ddacf73dc4`.
The earlier wrong text value was corrected in the preceding R9 evidence
section; the authoritative R9 retry remains unchanged.

Corrected hashes:

- `scripts/validate_cross_cli_sync.py`:
  `8b9d21ed256b7a2a11dfd40043b2af1e938d9ed50e8b0185a5a174eb5120f77e`;
- `tests/test_cross_cli_sync.py`:
  `146bed95e60c28144095470c1a639f619caa04c8ca14d28d08a245fbf39b8318`.

### Fresh tenth-correction verification and delta

- Router quick/core/full: `PASS`, `231` tests `OK`;
- cross-CLI module: `PASS`, `107` tests `OK`;
- Companion quick/templates/full: `PASS`, `87` tests `OK`;
- OpenSpec strict/all: `PASS`, `3 passed / 0 failed`;
- both exact policy-negative searches, shared Handoff/validator-core byte
  checks, and path-only sensitive audit: `PASS`;
- final isolated forward cases: `6/6 PASS`, transient root absent; private
  summary mode/SHA-256 `0600` /
  `6fe31cbfde08855d035ac52caf139d42d5e96ac995380c09017b156281bc79ef`.

The first R10 source-delta call used the preflight inventory in the
source-start argument and was rejected before an output was created. Its
private mode-`0700` partial compare root was retained as
`source-compare-r10-failed-baseline-binding`. The later
`source-delta-r10.json` (`cab67e501d7f3a524549fb568545759b246c3e878d1a711d5164671674c85371`)
and `source-delta-r10-retry1.json`
(`db634968ea2ac0441491aaa921379ceb92342fa25d0e1d172e77cc1a2a540f76`)
are retained non-authoritative pre-hardening records. No project path was
changed by those attempts.

The final bytecode-disabled authoritative retry passed:

- private delta:
  `/private/tmp/add-role-first-review-routing-p1r10-20260820-Bun7oJ/source-delta-r10-retry2.json`;
- private delta mode/SHA-256: `0600` /
  `f6e05c35c620fe2c50e24346d23b76c672ef73703017aaf339bf41071b19c271`;
- compare root mode: `0700`;
- binding mode/SHA-256: `0600` /
  `1a27b71a8cb59b1ca1f542a6c1e78f8b0e488ae05adb8ffeb1d0a3c1deebc762`;
- allowlist: `82` entries, mode `0600`, SHA-256
  `3adc35f24774fb5942df74047f2da2b3db9d0c1a51d7c2a1bbbf453317779998`;
- actual changed paths: `78` (`64` Router, `14` Companion);
- result: `source_delta: "pass"`, `unexpected_paths: []`;
- governed `scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc`:
  absent.

The durable path/status/SHA/mode-only copy is
`docs/design/evidence/add-role-first-review-routing/2026-08-20-source-delta-p1-r10-summary.json`,
SHA-256
`c95079e11be22f0f6c6e965ea4984f9c90d703e9e951c0f2144f78d8d0c2bc8c`.
This source-verification append, the durable summary, and the P1 R10 Review
input are evidence-only post-delta records. They do not authorize runtime
planning. A fresh independent Candidate Source High Re-review must return
explicit `PASS` before runtime planning or deployment may resume.

## P1 R11 exact-candidate persistence correction and verification — PASS

The independent P1 R10 Source High Review was persisted at
`docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r10.md`
with mode/SHA-256 `0644` /
`3543495d547ef12982e59b36968ca90087d85967590e4eb5535a3414e9aa5c06`.
It returned `FAIL` for two persistence P1 findings: candidate-creation failure
could leave a hidden accepted `PASS`, and installed-output rollback could
delete a same-content replacement inode.

Before correction, the exact R10 script, tests, source verification, R10 input,
R10 Review, and durable R10 summary were copied as regular mode-`0600` files
under the private mode-`0700` root
`/private/tmp/add-role-first-review-routing-p1r11-20260820-kth4IL`.

The R11 correction keeps generic atomic candidate behavior unchanged and adds
a Pi-evidence-only writer. It owns the candidate by device/inode from its open
no-follow descriptor. Candidate write/fsync or parent-guard failure first
rewrites and verifies that owned descriptor as the fixed `BLOCKED` schema,
then exposes only a visible mode-`0600` persistence-blocked quarantine when
cleanup cannot remove it. Installed-output rollback no longer unlinks by path:
it opens the output no-follow, binds device/inode/mode/content on one descriptor,
and rewrites only the exact owned inode to fixed `BLOCKED`; a changed inode is
left untouched and the public result remains blocked.

Four focused regressions were RED against the R10 preimage: candidate file
fsync plus unlink failure, candidate parent-guard plus unlink failure,
same-content/mode replacement-inode substitution, and substitution at the old
check-to-unlink boundary. Their GREEN forms prove no hidden accepted candidate,
only fixed-schema private quarantine where retained, no installed-output path
unlink, and preservation of unrelated replacement inode/content. The focused
persistence set passed `7/7`; the complete cross-CLI module passed `111/111`.

Corrected hashes:

- `scripts/validate_cross_cli_sync.py`: mode `0644`, SHA-256
  `301f4ba2ad3121e1e6799a34184540839715602e3c88608892a23439ae3c0aab`;
- `tests/test_cross_cli_sync.py`: mode `0644`, SHA-256
  `c061b5a02d5b601ee5ea3c521556a2dcbeaed318af5b0399c3f5c184bbfdb1c6`.

Fresh R11 validation passed:

- Router quick/core/full: `PASS`, `235` tests `OK`;
- Companion quick/templates/full: `PASS`, `87` tests `OK`;
- OpenSpec strict/all: `PASS`, `3 passed / 0 failed`;
- both exact policy-negative searches, shared Handoff/validator-core byte
  checks, and path-only sensitive audit: `PASS`;
- isolated forward cases: `6/6 PASS`, transient root absent; private summary
  mode/SHA-256 `0600` /
  `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b`;
- governed `scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc`:
  absent.

The bytecode-disabled authoritative no-Git source delta passed:

- private delta:
  `/private/tmp/add-role-first-review-routing-p1r11-20260820-kth4IL/source-delta-r11.json`;
- delta mode/SHA-256: `0600` /
  `11c7608e5fe7b0c9d0d43b22e474777f40fa6e5d999f223009f573555b49c8c5`;
- compare root mode: `0700`;
- bindings mode/SHA-256: `0600` /
  `525f418a2b137eaa0f963e9b189070ee3d67f5f9e839a0de58e3d9c26474c85e`;
- allowlist: `85` entries, mode/SHA-256 `0600` /
  `20a4b3be6516b55c7df40b63309d34f1f28a72498ff8c5ebccd107fb764cc3de`;
- actual changed paths: `80` (`66` Router, `14` Companion), with `37`
  modified, `42` added, and `1` deleted;
- result: `source_delta: "pass"`, `unexpected_paths: []`.

The source-delta command itself completed and persisted the valid artifact. A
subsequent read-only reporting helper used the wrong field name (`change`
instead of `status`) and exited nonzero; the artifact was then independently
parsed, schema-checked, and compared to its durable copy without rerunning or
replacing it.

The durable path/status/SHA/mode-only copy is
`docs/design/evidence/add-role-first-review-routing/2026-08-21-source-delta-p1-r11-summary.json`,
mode/SHA-256 `0644` /
`a3fbe1074cea7c163c507de02e79ba7dcec0c941b4c7b6bf52ca944ba7d02462`.
This verification append, the durable summary, and the P1 R11 Review input are
evidence-only post-delta records. They do not authorize runtime planning. A
fresh independent Candidate Source High Re-review must return explicit `PASS`.

## P1 R13 persistence-boundary correction — implementation evidence

The independent P1 R12 Source High Review returned `FAIL` with five
reproducible P1 findings: one-sided generic exchange rollback, generic/Pi
check-to-unlink deletion, Pi rename-then-raise leaving official `PASS`
evidence, malformed blocked-recovery evidence after a rename exception, and
Pi rollback collision leaving unrelated official output bytes.

Before correction, the exact R12 script and tests plus the required governance
inputs were copied as regular mode-`0600` files beneath the private
mode-`0700` root
`/private/tmp/add-role-first-review-routing-p1r13-20260821-luna`.

R13 now requires both retained ownership sides for generic exchange rollback
and fails closed as `transaction-unsafe` on a one-sided match. Generic and Pi
cleanup rebind the retained entry no-follow immediately before unlink and
preserve explicit recovery state on mismatch. Pi persistence inspects both
names after rename side effects, clears any accepted-looking official
`PASS`, revalidates pending/blocked identity and content after namespace
mutation, and leaves only durable `BLOCKED`/`persistence-unsafe` or
`persistence-pending` residue on collision or uncertainty.

R13 focused production probes and regressions cover all five R12 findings,
including namespace mutation followed by an exception, malformed blocked
recovery substitution, cleanup replacement immediately before unlink, and
rollback collision. The implementation agent reported focused P1 classes
`102/102`, cross-CLI `140/140`, Router full `264/264`, core validator
`PASS`, and quick validation `Skill is valid!`. These are implementation
evidence only; an independent Source High Re-review remains required.

Corrected hashes:

- `scripts/validate_cross_cli_sync.py`: mode `0644`, SHA-256
  `fd8a05c2d8126d1202847a60d574ab65edcee238d3c00c722797db69224e3295`;
- `tests/test_cross_cli_sync.py`: mode `0644`, SHA-256
  `419774194a4254f6a8b253c7505c2722ad5e6509d1979a4acd0533f3df0ab689`.

The bytecode-disabled authoritative R13 no-Git source delta passed:

- private delta:
  `/private/tmp/add-role-first-review-routing-p1r13-20260821-luna/evidence/source-delta-r13.json`;
- delta mode/SHA-256: `0600` /
  `d6c959d118e5f7bcf9f691131c1126be637c683bc03cd10fdb14ea4935113d48`;
- compare root mode: `0700`;
- bindings mode/SHA-256: `0600` /
  `fded0c8cc1f93e9591926118cac6c9d4ff838c980da7eedf79c9c0aadb46fa37`;
- allowlist: `93` entries, mode/SHA-256 `0600` /
  `3531c68cbbb41b4de9e271adb51dbfc22367555565faeaabd4d064125e78ed98`;
- actual changed paths: `89` (`75` Router, `14` Companion), with
  `37` modified, `49` added, and `3` generated-cache deletions;
- result: `source_delta: "pass"`, `unexpected_paths: []`.

The durable path/status/SHA/mode-only copy is
`docs/design/evidence/add-role-first-review-routing/2026-08-21-source-delta-p1-r13-summary.json`,
mode/SHA-256 `0644` /
`2ebfc39e4225adbbb6327925ae7bd0e4d0fdbbe907c750bb055611e4a47bc9ab`.
This verification append, the durable summary, and the R13 Review input are
evidence-only post-delta records. The input was normalized after delta
generation without implementation or runtime changes. They do not authorize
runtime planning. A fresh independent Candidate Source High Re-review must
return explicit `PASS`.

## P1 R12 retained-candidate and persistence-boundary correction — PASS

The independent P1 R11 Source High Review was persisted at
`docs/design/reviews/2026-08-21-add-role-first-review-routing-source-rereview-p1-r11.md`
with mode/SHA-256 `0644` /
`0d89c219a344f9943d9f324d4f36fc0cbb4ec503fc0bce0eb0ceb91912981d62`.
It returned `FAIL` with four persistence P1 findings: candidate-name
substitution before generic and Pi installation, same-inode content mutation,
unverified quarantine rename boundaries, and hidden or ambiguous cleanup
residue.

Before correction, the exact R11 script, tests, source verification, R11
input, R11 Review, and durable R11 summary were copied as regular mode-`0600`
files beneath the private mode-`0700` root
`/private/tmp/add-role-first-review-routing-p1r12-20260821-ww37dU`.

R12 retains no-follow descriptors through candidate installation and cleanup,
binds device, inode, type, mode, UID, GID, link count, size, mtime, ctime, and
two content hashes, and distinguishes full pre-namespace identity checks from
the ctime-only relaxation required after a reviewed rename. Generic create and
swap paths revalidate exact candidates and displaced objects after namespace
mutation, restore or preserve substitutions, close retained descriptors on
candidate-write failure, and use visible transaction recovery names instead of
hidden candidates.

Pi persistence no longer rewrites an installed or candidate `PASS` inode in
place. Uncertain objects move through descriptor-bound visible
`persistence-unsafe` recovery names. Fixed mode-`0600` `BLOCKED` evidence is
written first under a non-evidence `persistence-pending` name, double-bound and
file-fsynced, then exclusively renamed to `persistence-blocked`, directory-
fsynced, and revalidated after the rename. Candidate, output, blocked-recovery,
quarantine, parent-mapping, same-inode, and cleanup substitutions therefore
cannot be accepted as evidence or silently overwrite or delete the substituted
object.

Twenty-three focused tests were RED against the R11 preimage and GREEN after
correction. They cover all four R11 findings plus ctime-only drift, the final
stable-check race, candidate binding failure, destination descriptor cleanup,
the former check-to-unlink boundary, and blocked-recovery crash consistency.
The complete cross-CLI module now passes `134/134`.

Corrected hashes:

- `scripts/validate_cross_cli_sync.py`: mode `0644`, SHA-256
  `36b7c55a5688d455192ff850825eb5807e606141129782df8dc4152f34e2ff54`;
- `tests/test_cross_cli_sync.py`: mode `0644`, SHA-256
  `2aeb37aa97bfbf7f542d9f6e67d64f4500f99c3d0e20d6ae8a67fa70e21524b7`.

Fresh R12 validation passed:

- Router quick/core/full: `PASS`, `258` tests `OK`;
- Companion quick/templates/full: `PASS`, `87` tests `OK`;
- OpenSpec strict/all: `PASS`, `3 passed / 0 failed`;
- both exact policy-negative searches, shared Handoff/validator-core byte
  checks, and path-only sensitive audit: `PASS`;
- isolated forward cases: `6/6 PASS`, transient root absent; private summary
  mode/SHA-256 `0600` /
  `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b`.

The first R12 source-delta attempt used an `88`-entry bound allowlist and was
correctly rejected before output creation because two generated CPython 3.14
cache deletions were not listed. Its mode-`0700` partial compare root,
mode-`0600` bindings (`bb4aead50139702371159922429be24d271ba0a230164fe61283ea7775ce8ec5`),
and mode-`0600` allowlist
(`07691397dada7f2fb4081730d2627a24fbe701c632abf27450c47e729a278638`)
remain unchanged as process evidence; `source-delta-r12.json` remains absent.

The bytecode-disabled authoritative retry passed:

- private delta:
  `/private/tmp/add-role-first-review-routing-p1r12-20260821-ww37dU/source-delta-r12-retry1.json`;
- delta mode/SHA-256: `0600` /
  `3e98e4015b8b461958172c538ea07798de4239d89a2ae0771a9eba1ec84c8e50`;
- compare root mode: `0700`;
- bindings mode/SHA-256: `0600` /
  `b3c52f8cd141e70ab3f61d0366734c888513c5af59da4e6f089979fe24c7fd09`;
- allowlist: `90` entries, mode/SHA-256 `0600` /
  `2f60dd69f0ff969f5c0f937a7665c5087b8316fcecfc47330ca720954a0ae34f`;
- actual changed paths: `85` (`71` Router, `14` Companion), with `37`
  modified, `45` added, and `3` generated-cache deletions;
- result: `source_delta: "pass"`, `unexpected_paths: []`.

The durable path/status/SHA/mode-only copy is
`docs/design/evidence/add-role-first-review-routing/2026-08-21-source-delta-p1-r12-summary.json`,
mode/SHA-256 `0644` /
`aa68cddb16622de36a3d08cb1012c9084f9dfa6a1fe9c5b2f324829ecb0e26d6`.
This verification append, the durable summary, and the P1 R12 Review input are
evidence-only post-delta records. They do not authorize runtime planning. A
fresh independent Candidate Source High Re-review must return explicit `PASS`.

## P1 R13 independent Source High Re-review — FAIL

The fresh no-history Luna Max reviewer was bound to the R13 input and delta,
reran the production-path probes, and returned `FAIL`. It confirmed the
R13 rollback, blocked-evidence, and collision corrections, but reproduced one
remaining P1 in both generic and Pi cleanup:

- after `_rebind_before_unlink()` validates the retained descriptor,
  the reviewed inode can be renamed aside while an unrelated inode replaces
  the cleanup name;
- because the retained descriptor remains linked and ctime is excluded at
  this boundary, validation passes;
- the subsequent name-based `os.unlink()` deletes the unrelated inode
  without error or recovery residue.

The Review artifact is
`docs/design/reviews/2026-08-21-add-role-first-review-routing-source-rereview-p1-r13.md`,
mode `0644`, SHA-256
`5b7ffc4fb35a1072454145f3f1e104a21c4fa2bad28f9d7cab7ae82f5a823b17`.
Read-only runtime verification remains blocked. R14 must replace the
post-check name-based unlink with ownership-preserving atomic quarantine/no-
replace semantics, add the retained-inode-moved/unrelated-replacement
regressions, rebind the complete delta, and obtain a fresh independent Review.

## P1 R14 ownership-preserving cleanup correction — pending independent Review

R14 corrected the remaining R13 cleanup boundary in both generic and Pi
production paths. After descriptor-bound revalidation, cleanup now uses
Darwin `renameatx_np(..., RENAME_EXCL)` to quarantine the exact retained inode
without replacing a name occupied by an unrelated inode. The quarantined
descriptor is revalidated as the retained owner before unlink; collisions,
identity drift, and quarantine/revalidation failures leave explicit recovery
evidence and fail closed. The R14 tests add the retained-inode-moved plus
unrelated-replacement adversarial regressions for both paths.

R14 implementation hashes are:

- `scripts/validate_cross_cli_sync.py`: mode `0644`, SHA-256
  `939dc80effdd605fea745291c02dd1079b9f0ebdfa72e8a467942c92775502d0`;
- `tests/test_cross_cli_sync.py`: mode `0644`, SHA-256
  `6a25c1cbf6eecbf12cec695d29fda09488786017b76d821047f90ccfb69328a7`.

The R14 private source-delta binding is:

- delta:
  `/private/tmp/add-role-first-review-routing-p1r14-20260821-luna/evidence/source-delta-r14.json`,
  mode/SHA-256 `0600` /
  `efce4e61a90ff14b9893cb852e2f09468e3af9be0e9c3857116587290c063e2f`;
- compare root mode: `0700`;
- bindings:
  `/private/tmp/add-role-first-review-routing-p1r14-20260821-luna/evidence/preflight-source-bindings-r14.json`,
  mode/SHA-256 `0600` /
  `8877e931ef9d12f5e093ced04f15ef3517f3fead4cfe1e9f43055b8db56ee42e`;
- allowlist: `96` entries, mode/SHA-256 `0600` /
  `03fd6da52bd02345c595b370af0eebc47dce41dbd9e5046b8b0af2f0730c898d`.

The bytecode-disabled authoritative R14 no-Git source delta passed with
`unexpected_paths: []`: `92` actual paths (`78` Router, `14` Companion),
including `23` Router modifications, `52` Router additions, `3` generated
cache deletions, and `14` Companion modifications. The durable
path/status/SHA/mode-only copy is
`docs/design/evidence/add-role-first-review-routing/2026-08-21-source-delta-p1-r14-summary.json`,
mode/SHA-256 `0644` /
`bf7b42c48e582723c76c739be1188de13e3a7cc453e8c8c793c162308de3f692`.

The R14 input is
`docs/design/evidence/add-role-first-review-routing/2026-08-21-source-rereview-p1-r14-inputs.md`,
mode `0644`; its final SHA-256 is bound in the R14 input record after this
evidence append.
The input and this verification append are evidence-only records after the
authoritative delta; they do not authorize runtime planning. A fresh
independent Candidate Source High Re-review must return explicit `PASS` before
local skill synchronization or runtime verification.

## P1 R15 fail-closed deletion correction — pending independent Review

R15 addressed the R14 final quarantine unlink boundary. Darwin/POSIX
`unlinkat(dir_fd, name)` was independently confirmed to remain name-based and
to provide no inode-CAS or unlink-by-retained-descriptor primitive. The bound
cleanup path therefore no longer falls back to ordinary `os.unlink` or claims
that `unlinkat` is exact-owner deletion: when no exact-owner primitive exists,
it raises a visible cleanup blocker, preserves the quarantined/recovery object,
and fails closed. Pi retained PASS-shaped objects are rewritten through their
validated descriptor into BLOCKED evidence before recovery publication.

R15 added final-bind replacement and post-delete-uncertainty regressions for
both Generic and Pi. The RED R14-preimage probes failed `2/2`; the corrected
focused P1 probes pass `6/6`. R15 implementation hashes are:

- `scripts/validate_cross_cli_sync.py`: mode `0644`, SHA-256
  `f4759f7e4f73576cfd6db3a8398ad43944a6ad7f9b6db968964c0444c03a881`;
- `tests/test_cross_cli_sync.py`: mode `0644`, SHA-256
  `5557cb2cdea3d95ae2cbf09a1c5420bb7faa4729829d81c8f0ca9859b7e9b063`.

The bytecode-disabled authoritative R15 no-Git source delta passed with
`unexpected_paths: []`:

- private delta:
  `/private/tmp/add-role-first-review-routing-p1r15-20260821-luna/evidence/source-delta-r15.json`,
  mode/SHA-256 `0600` /
  `5898349948ca8ade6cece1460f15367f3b0767d1057ae913de55ee52197576f9`;
- compare root mode: `0700`;
- bindings:
  `/private/tmp/add-role-first-review-routing-p1r15-20260821-luna/evidence/preflight-source-bindings-r15.json`,
  mode/SHA-256 `0600` /
  `abbe2e5f5f0bd3871d8fc23834519ae993e7e5053b0cc4e4a27f75377ac6c923`;
- allowlist: `99` entries, mode/SHA-256 `0600` /
  `5ad2294d2a6d9d1cd3e5662ac4d237a27dfe83da3409b79fb20a4691842e6f40`;
- actual changed paths: `95` (`81` Router, `14` Companion), with `23`
  Router modifications, `55` Router additions, `3` generated-cache deletions,
  and `14` Companion modifications.

The durable path/status/SHA/mode-only copy is
`docs/design/evidence/add-role-first-review-routing/2026-08-21-source-delta-p1-r15-summary.json`,
mode/SHA-256 `0644` /
`0e117004c83b30a68d4b76d86dcc52cf80ba0be9436f78ff78fb2fdf6c58413c`.
The R15 input and this verification append are evidence-only records around
the authoritative delta; their final bindings are recorded in the R15 input
and a fresh independent Review must verify them. Runtime planning remains
blocked until explicit `PASS`.

## P1 R14 independent Source High Review — FAIL

The fresh no-history Luna Max reviewer was bound to the finalized R14 input,
the complete R14 delta, and the corrected generic/Pi implementation. It
returned `FAIL` and confirmed the R14 pre-quarantine race correction, but
reproduced one remaining P1 after the final quarantine ownership check:

- `_unlink_bound_quarantined_entry()` revalidates the quarantine name and
  retained inode at `scripts/validate_cross_cli_sync.py:1138-1145`;
- an unrelated inode can replace that name before the ordinary
  `os.unlink(quarantine_name, dir_fd=guard["fd"])` at `:1146`;
- isolated generic and Pi production-path probes both deleted the unrelated
  inode without recovery residue, and Pi cleanup returned without preserving
  the object.

The Review artifact is
`docs/design/reviews/2026-08-21-add-role-first-review-routing-source-rereview-p1-r14.md`,
mode/SHA-256 `0644` /
`21c8af525ada608343c9498697020d9dbd28a763bf461b4218ff4451a8b77cc5`.
Runtime verification remains blocked. R15 must replace the final name-based
unlink with ownership-preserving deletion semantics, add post-final-check
generic/Pi replacement and post-delete uncertainty regressions, rebind the
complete delta, and obtain a fresh independent Review with explicit `PASS`.

## P1 R15 independent Source High Review — FAIL

The fresh no-history Luna Max reviewer was bound to the finalized R15 input,
the complete R15 delta, and the fail-closed deletion correction. It returned
`FAIL`: generic cleanup is fail-closed and does not delete an unrelated
replacement, but the Pi recovery path can still leave a visible valid
`verdict: PASS` object when the retained inode is moved aside and the
quarantine name is replaced after the final bind.

The remaining P1 is at
`scripts/validate_cross_cli_sync.py:1133-1155`, `:1290-1317`,
`:1201-1229`, with the recovery caller at `:5558-5626`. The recovery branch
only rewrites the retained object when `_retained_binding_matches_name()`
still matches the quarantine name. After namespace replacement that check is
false, so the rewrite is skipped; the already-validated descriptor is closed
and the uncertainty is swallowed. A fresh production probe left the retained
valid canonical Pi JSON with `"verdict": "PASS"` and mode `0600` visible
alongside the blocked evidence.

The R15 regression used arbitrary `b"original-pass\\n"` bytes and checked
residue existence, so it did not assert the semantic no-PASS invariant. The
required R16 correction is to rewrite the retained object through its already
validated descriptor (or otherwise guarantee no PASS-shaped residue), add a
valid canonical JSON PASS replacement probe, preserve the generic unrelated
inode guarantee, and rerun the complete fresh validation/delta/review matrix.

The Review artifact is
`docs/design/reviews/2026-08-21-add-role-first-review-routing-source-rereview-p1-r15.md`,
mode/SHA-256 `0644` /
`c77d7a284867063abdcaccb941844cc673550aeaf18228fecfd3f383ff29f3fc`.
Runtime verification and local skill synchronization remain blocked until an
independent R16 Source High Review returns explicit `PASS`.

## P1 R16 independent Source High Review — PASS

The fresh no-history Luna Max reviewer verified the final R16 input at both
Review boundaries, rechecked the complete no-Git delta and all prior
corrections, and returned `PASS`. R16 closes the R15 Pi retained canonical
`verdict: PASS` residue boundary without weakening Generic fail-closed cleanup.

The exact-owner seam remains fail-closed because Darwin/POSIX provides no
inode-CAS or unlink-by-retained-descriptor primitive. Generic replacement and
post-delete uncertainty probes preserved unrelated inodes and emitted visible
mode-`0600` recovery/blocker evidence. Pi now rewrites the retained object
through its already validated writable descriptor, even after the quarantine
namespace is replaced; the valid canonical-PASS adversarial probe produced a
canonical BLOCKED retained-aside and `pi_pass_residue: []`. The read-only
ownership upgrade path revalidated identity and prestate, and the impossible
upgrade branch retained only explicit unsafe recovery plus BLOCKED evidence.

Fresh validation was green: Router core/quick, workflow `124/124`, cross-CLI
`149/149`, full discovery `273/273`; Companion quick/templates/full `87/87`;
OpenSpec strict/all `3/0`; static/sensitive/shared checks clean; and the six
forward cases all PASS. No P0/P1/P2 finding remains. Runtime verification may
resume only under the separately approved runtime gate and existing plan;
Task 10 remains an approved external limitation.

The R16 Review artifact is
`docs/design/reviews/2026-08-21-add-role-first-review-routing-source-rereview-p1-r16.md`,
mode/SHA-256 `0644` /
`dab79a6a8b03a80b9a453c0dbc79a5af9de406835e43670cc26c6de9e113acb4`.
The durable R16 delta summary is mode/SHA-256 `0644` /
`f409f302910303daa421c0e5c265cd34bf1fbd06145864d55dc859376362dfdc`; the
private delta remains `98` actual records, `102` allowlisted entries, and
`unexpected_paths: []`. Source-level promotion is permitted.

After the Review artifact and this source-verification append were persisted, a
fresh read-only no-Git delta rebind against the same R9 baselines produced the
expected post-review evidence state: `100` records (`86` Router, `14`
Companion), `23` Router modifications, `60` Router additions, `3` expected
generated-cache deletions, `14` Companion modifications, and
`unexpected_paths: []`. The final private rebind is
`/private/tmp/add-role-first-review-routing-p1r16-20260821-luna/evidence/source-delta-r16-final.json`,
mode/SHA-256 `0600` /
`78c4e91b07d768ec58d52941547cddeb7b62edec66651d8ded68109c057fa48b`, with
mode-`0700` compare root
`/private/tmp/add-role-first-review-routing-p1r16-20260821-luna/source-compare-r16-final`.
The two additional post-delta records are the durable R16 summary and Review;
the implementation remains unchanged.

## Project Learning Closeout — promoted high-severity cleanup invariant

The R14/R15 independent findings and the R16 independent PASS establish a
generalized project-local integrity invariant: final cleanup binds an object
identity, not a pathname; when exact-owner deletion is unavailable, cleanup
must fail closed, preserve visible mode-`0600` recovery/blocker evidence, keep
unrelated replacement inodes untouched, and neutralize retained Pi PASS-shaped
evidence through the validated writable descriptor. The durable promotion is:

- `docs/learning-candidates/2026-08-21-bound-cleanup-object-identity.md`,
  mode `0644`, SHA-256 `a7e8e15e9c2912160e689878580e7977fd907d6ada54a89370950b993badcc91`;
- `docs/engineering-invariants.md`, mode `0644`, SHA-256
  `af71b060aea50a37e1a2923101ab2ed3b4bc75eec3da262f872cb9204bea333c`.

The deterministic enforcement is the descriptor-bound production seam and
the final-bind replacement regressions at
`tests/test_cross_cli_sync.py:1241-1299` and `:2540-2621`; focused evidence
remains R16 P1 `7/7 PASS`, cross-CLI `149/149 PASS`, and no canonical JSON PASS
residue. The candidate contains only summarized project-relative provenance and
no private prompt, credential, token, or transcript content.

The learning-closeout no-Git delta was freshly rebound against the same R9
baselines with `102` records (`87` Router, `14` Companion), `24` Router
modifications, `61` Router additions, `3` expected generated-cache deletions,
`14` Companion modifications, and `unexpected_paths: []`:

- private delta:
  `/private/tmp/add-role-first-review-routing-p1r16-20260821-luna/evidence/source-delta-learning-final.json`,
  mode/SHA-256 `0600` /
  `6447c8400213f3fe1af0e15f08738d7c7f1704cbca11ba73abd38d91c9bc63d0`;
- private bindings:
  `/private/tmp/add-role-first-review-routing-p1r16-20260821-luna/evidence/preflight-source-bindings-learning-final.json`,
  mode/SHA-256 `0600` /
  `0eede306e9a32166f3d9919c1ac9faec957212f7acdce88aa8b1667d4bacd584`;
- allowlist: `104` entries, mode/SHA-256 `0600` /
  `051380c9ff07cbc6380ef60235cf74a132ef5da5c141665c907b2d335de8534b`;
- compare root: mode `0700`,
  `/private/tmp/add-role-first-review-routing-p1r16-20260821-luna/source-compare-learning-final`.

This closeout append is evidence-only after the learning delta; a final
read-only rebind must verify the resulting source state before publication.

The required final learning rebind was completed read-only against the same
R9 baselines. It produced `102` records (`87` Router, `14` Companion),
`24` Router modifications, `61` Router additions, `3` expected generated-cache
deletions, `14` Companion modifications, and `unexpected_paths: []`:

- final recheck delta:
  `/private/tmp/add-role-first-review-routing-p1r16-20260821-luna/evidence/source-delta-learning-final-recheck.json`,
  mode/SHA-256 `0600` /
  `fb7ed8eb1dee977843f3540f5a1ddc9fd650cec1e7b79b0f37aafa23c420d7ab`;
- final recheck compare root: mode `0700`,
  `/private/tmp/add-role-first-review-routing-p1r16-20260821-luna/source-compare-learning-final-recheck`;
- learning Review:
  `docs/design/reviews/2026-08-21-bound-cleanup-object-identity-learning-review.md`,
  mode/SHA-256 `0644` /
  `23cf3c3a59f9297fe16a21bda20541bc010eccec68c95864ce6f553d13b3f3b6`,
  verdict `PASS` with no P0/P1/P2 findings.

The source-verification hash changed only because these final evidence records
were appended; implementation and test bindings remain unchanged.

After the task-ledger reconciliation and Learning Review artifact were added,
the final publication rebind was rerun against the same reconstructed R9
baselines. It produced `104` records (`90` Router, `14` Companion, including
the expected three Router cache deletions), specifically `25` Router
modifications, `62` Router additions, `3` expected generated-cache deletions,
and `14` Companion modifications, with `unexpected_paths: []`:

- final publication delta:
  `/private/tmp/add-role-first-review-routing-p1r16-20260821-luna/evidence/source-delta-final-publication.json`,
  mode/SHA-256 `0600` /
  `98599b44c9d51d44e07a7805934bfc110064f67f228aac4d315f10c8812b725d`;
- final publication bindings:
  `/private/tmp/add-role-first-review-routing-p1r16-20260821-luna/evidence/preflight-source-bindings-final-publication.json`,
  mode/SHA-256 `0600` /
  `e2ba464a549a1be12190c85e9a5d8fdbc62898ea4473970bcdc78cb72176e028`;
- final allowlist: `106` entries, mode/SHA-256 `0600` /
  `46b0a177e8dfe0df4954dc753b7f64c14b9fb0a1e6f822c12d283d9153824176`;
- compare root: mode `0700`,
  `/private/tmp/add-role-first-review-routing-p1r16-20260821-luna/source-compare-final-publication`.

The two newly bound source records are the Learning Review artifact and the
reconciled OpenSpec task ledger; the two allowlist-only historical records
remain unchanged and no unallowlisted path exists.
