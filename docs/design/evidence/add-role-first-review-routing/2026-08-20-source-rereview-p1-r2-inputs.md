# Candidate Source High Re-review Inputs — P1 R2

## Assignment and authority

- reviewer product: `codex`
- reviewer role: `independent-reviewer`
- reviewer profile: `control-plane-high`
- reviewer instance: a fresh no-history instance distinct from all authors,
  executors, prior reviewers, and the bound decision owner
- purpose: independently decide whether the twice-corrected candidate source
  satisfies the approved change and may proceed to read-only four-target
  runtime planning
- result authority: governed implementation Review evidence only; the reviewer
  cannot mutate source/runtime, accept its own result, update canonical state,
  or claim completion

The original control plane accepts only an explicit `PASS`, `FAIL`, or
`BLOCKED`. Any actionable finding blocks runtime planning and returns the
candidate to correction, complete fresh verification/delta, and a new Review
revision.

## Required read set

Read the complete current Router and Companion trees, including each local
instruction and Skill, the approved OpenSpec change and Plan, engineering
invariants, project-learning closeout contract, synchronization contracts,
source verification, both prior FAIL Reviews, the complete current delta, and
every changed or added record. Do not rely on this input record instead of the
actual source, tests, documentation, and evidence.

Primary bound inputs:

| Input | SHA-256 |
|---|---|
| `docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md` | `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| `openspec/changes/add-role-first-review-routing/proposal.md` | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| `openspec/changes/add-role-first-review-routing/design.md` | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| `openspec/changes/add-role-first-review-routing/specs/skill-workflow-governance/spec.md` | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| `openspec/changes/add-role-first-review-routing/tasks.md` | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| `docs/design/evidence/add-role-first-review-routing/2026-08-10-source-verification.md` | `92a0593203886fe8919d7c7ee8b7ab3313d4e9fa92a81382af0089b876c0e546` |
| `docs/design/evidence/add-role-first-review-routing/2026-08-20-source-delta-p1-r2-summary.json` | `7c96f9f5b53ae1ed33e791a126442a261f83d1315d3dd6c8825509e6334a74fa` |
| first FAIL `docs/design/reviews/2026-08-10-add-role-first-review-routing-source-review.md` | `35050b3e8766b055f11d3a55018d4a34c1aca87893f574b477bbfe28a9cf6ef1` |
| second FAIL `docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r1.md` | `44138637110b7643585d244721cf710f1f08a899dca874fd81df6ab1898d9719` |
| corrected `scripts/validate_cross_cli_sync.py` | `cef9fca193364a8ccda204fb80a351a656ac5e22c2919c96ecbf28fc7203f4ff` |
| corrected `tests/test_cross_cli_sync.py` | `95797ae3a2db091661f094c742a9247d098789ff1e453388580f61241e3ac1c8` |
| Router `tests/test_workflow_rules.py` | `9e8f1d6904b0eb3e397eafb305f0e1743a77dcd9d9c715ac05e510f4e3aa2dc7` |
| Router `README.md` | `44314b9c0f128ddcac90154ac5f36f167f70a66ab93aca61a4b46a86646f08ff` |
| Router `README_cn.md` | `b973047e8092a9b7550ab62db5e795c6a7a0ba30e51304a2541953d4379fb987` |
| Companion `README.md` | `f260de8c1e97ca5ce282e39c432278ebed4699745d0cd6c650dc82ece9ffe0b5` |
| Companion `README_cn.md` | `d6180a9a0f54fc0d87934bd24efe320d5f9c7b45cb816292f86db5d1ba2b601c` |
| Companion `tests/test_workflow_rules.py` | `65f8e4f2de06dfd050ef74310c94a84d76cec2b54c1955a1fdb66372d5f0b12c` |

Private read-only reproduction inputs:

| Input | Mode / SHA-256 |
|---|---|
| `/private/tmp/add-role-first-review-routing-p1r2-20260820-bSA2SA/source-delta-r2.json` | `0600` / `0e2efdc63378c35f9ff31b36e4471c79e9ffec28fbbfd54293e7cadd68ced6dd` |
| `/private/tmp/add-role-first-review-routing-p1r2-20260820-bSA2SA/source-compare-r2` | `0700` |
| `/private/tmp/add-role-first-review-routing-p1r2-20260820-bSA2SA/preflight-source-bindings-r2.json` | `0600` / `599616e5aacf064f4ef3c40eb51b7cb49fd8ff9362eac6ca30954f4dae7e3029` |
| `/private/tmp/add-role-first-review-routing-p1r2-20260820-bSA2SA/source-delta-allowlist-r2.txt` | `0600` / `deb257062c43f18b22a79b97121f1c39991d43ca920289df7842ee6044184a50` |
| `/private/tmp/add-role-first-review-routing-p1r2-20260820-bSA2SA/role-first-forward-summary-r2.json` | `0600` / `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |

The complete delta reports `48` actual path changes, `52` exact allowlist
entries, and `unexpected_paths: []`. The durable summary, appended source
verification, and this R2 input record were written after the private delta and
are evidence-only post-delta records. Bind and classify them explicitly; they
are not candidate implementation bytes.

## Prior findings and required integrity proof

The first High Review found that apply/restore checked a destination and later
performed an unconditional namespace replacement or removal. The P1 R1
correction added leaf-object exchange, exclusive creation, displaced-object
validation, rollback, quarantine, and focused tests.

The P1 R1 re-review then found three remaining issues:

1. parent-directory identity was not retained through the mutation boundary;
2. receipt advancement could detect receipt drift after exchange but discard
   the displaced receipt and leave a stale locally revised live receipt;
3. public Router/Companion documentation still described legacy evidence
   schema as current.

The P1 R2 candidate claims:

- the resolved complete parent chain is bound by directory identity and
  rechecked while a no-follow directory descriptor anchors candidate creation,
  exchange, exclusive install, restore, quarantine, and cleanup;
- receipt advancement validates the exact displaced receipt, rolls back drift
  atomically when unambiguous, and otherwise preserves recovery evidence and
  blocks later targets; history collision follows the same restore-or-preserve
  rule;
- Router and Companion public English/Chinese documentation now describes
  schema 6 with schema-2 evidence as current and limits schema 4/5 to the
  separate frozen legacy inventory interface.

Trace these claims through actual production path:line mechanisms and tests.
Independently exercise temporary, isolated integrity checks against the
production functions for existing/absent targets, parent mapping/link/type or
ancestor identity changes, descriptor-relative containment, receipt exchange
drift, receipt-history collision, ambiguous rollback preservation, and
later-target exclusion. Decide whether any path can still affect unreviewed
state or falsely report verified apply/restore/recovery.

Also re-evaluate all previously passing areas: role-first routing, concrete
assignment, schema-6/schema-2 evidence identity, current/legacy isolation,
four-target manifest/plan semantics, sensitive exclusions, deterministic
discovery, public docs, shared-byte parity, and the complete changed-record
set.

## Fresh verification evidence

- focused second-correction tests: RED `9` expected failures / `0` fixture
  errors, then GREEN `9/9`;
- full cross-CLI module: `76` tests, `OK`;
- Router full suite: `200` tests, `OK`;
- Companion full suite: `87` tests, `OK`;
- both quick/project validators: `PASS`;
- OpenSpec strict/all: `PASS`, `3 passed / 0 failed`;
- both exact static negative searches: empty;
- shared Handoff and validator-core byte checks: `PASS`;
- sensitive audit: `0 sensitive categories found`;
- forward model cases: `6/6`, `forward: "pass"`;
- complete source delta: `PASS`, `48` actual, `52` allowlisted,
  `unexpected_paths: []`.

The original isolated Conda interpreter remains unavailable because its real
`bin/python3.11` object is externally absent while its symlinks remain. Current
quick validators used `/opt/anaconda3/bin/python`, previously accepted for this
gate; dependency-free validators/tests used default `python3`. Do not present
this as an exact replay of the missing old environment.

## Required output

Return one complete Review artifact with:

1. reviewer assignment and independence statement;
2. start/end hash and mode checks for every bound primary/private input;
3. complete-delta coverage and post-delta evidence-only classification;
4. requirement-to-production-mechanism-to-test traces with path:line evidence;
5. explicit integrity analysis of both prior P1 boundaries and all recovery
   branches;
6. fresh validation commands/results plus sensitive/shared-byte checks;
7. findings ordered by severity with exact correction/resume conditions;
8. one final verdict: `PASS`, `FAIL`, or `BLOCKED`;
9. an explicit statement whether read-only runtime planning may begin.

Do not modify any file, run Git, run Pi, inspect or mutate runtime
destinations, create a runtime plan, accept your own verdict, or claim
completion.
