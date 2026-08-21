# Candidate Source High Re-review Inputs — P1 R4

## Assignment and authority

- reviewer product: `codex`
- reviewer role: `independent-reviewer`
- reviewer profile: `control-plane-high`
- reviewer instance: a fresh no-history instance distinct from all authors,
  executors, prior reviewers, and the bound decision owner
- purpose: independently decide whether the four-times-corrected candidate
  source satisfies the approved change and may proceed to read-only
  four-target runtime planning
- result authority: governed implementation Review evidence only; the reviewer
  cannot mutate source/runtime, accept its own result, update canonical state,
  or claim completion

The original control plane accepts only an explicit `PASS`, `FAIL`, or
`BLOCKED`. Any actionable finding blocks runtime planning and returns the
candidate to correction, complete fresh verification/delta, and another Review
revision.

## Required read set

Read the complete current Router and Companion trees, including each local
instruction and Skill, the approved OpenSpec change and Plan, engineering
invariants, project-learning closeout contract, synchronization contracts,
source verification, all four prior FAIL Reviews, the complete current delta,
and every changed or added record. Do not rely on this input record instead of
the actual source, tests, documentation, and evidence.

Primary bound inputs:

| Input | SHA-256 |
|---|---|
| `docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md` | `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| `openspec/changes/add-role-first-review-routing/proposal.md` | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| `openspec/changes/add-role-first-review-routing/design.md` | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| `openspec/changes/add-role-first-review-routing/specs/skill-workflow-governance/spec.md` | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| `openspec/changes/add-role-first-review-routing/tasks.md` | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| `docs/design/evidence/add-role-first-review-routing/2026-08-10-source-verification.md` | `bbcf2cc726876409aae30b7cac577a198e8341593c04b74f5f4084caeab84f95` |
| `docs/design/evidence/add-role-first-review-routing/2026-08-20-source-delta-p1-r4-summary.json` | `6028f0c3b1d457b516226374fc942adc4e160ac8771d7eb72ce8827c27692127` |
| first FAIL `docs/design/reviews/2026-08-10-add-role-first-review-routing-source-review.md` | `35050b3e8766b055f11d3a55018d4a34c1aca87893f574b477bbfe28a9cf6ef1` |
| P1 R1 FAIL `docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r1.md` | `44138637110b7643585d244721cf710f1f08a899dca874fd81df6ab1898d9719` |
| P1 R2 FAIL `docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r2.md` | `5991be2198f4387bb0e860733352fb98e063e22bfcd694eacd3f4704932429b3` |
| P1 R3 FAIL `docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r3.md` | `c451abf26592caa0630f8d3b2d272e740ddde40d959cccc79f5d672d4b379c47` |
| corrected `scripts/validate_cross_cli_sync.py` | `8d8a18a4c6d9a7639fe963e08c1a799b0c5a531129fd6195c8cd9fd8c4315f1e` |
| corrected `tests/test_cross_cli_sync.py` | `15f787aa7f0e23fd60611d3d0c5639b1541aba7b760fd88d93efe635f8a37aa3` |
| Router `tests/test_workflow_rules.py` | `9e8f1d6904b0eb3e397eafb305f0e1743a77dcd9d9c715ac05e510f4e3aa2dc7` |
| Router `README.md` | `44314b9c0f128ddcac90154ac5f36f167f70a66ab93aca61a4b46a86646f08ff` |
| Router `README_cn.md` | `b973047e8092a9b7550ab62db5e795c6a7a0ba30e51304a2541953d4379fb987` |
| Companion `README.md` | `f260de8c1e97ca5ce282e39c432278ebed4699745d0cd6c650dc82ece9ffe0b5` |
| Companion `README_cn.md` | `d6180a9a0f54fc0d87934bd24efe320d5f9c7b45cb816292f86db5d1ba2b601c` |
| Companion `tests/test_workflow_rules.py` | `65f8e4f2de06dfd050ef74310c94a84d76cec2b54c1955a1fdb66372d5f0b12c` |

Private read-only reproduction inputs:

| Input | Mode / SHA-256 |
|---|---|
| `/private/tmp/add-role-first-review-routing-p1r4-20260820-7X9r4J/source-delta-r4-retry1.json` | `0600` / `235a4a44eb344f6f0ea96137546c26d7b3d0a7b2f250bc3ab17e7ad1c43834ec` |
| `/private/tmp/add-role-first-review-routing-p1r4-20260820-7X9r4J/source-compare-r4-retry1` | `0700` |
| retained failed-attempt `/private/tmp/add-role-first-review-routing-p1r4-20260820-7X9r4J/source-compare-r4` | `0700` |
| `/private/tmp/add-role-first-review-routing-p1r4-20260820-7X9r4J/preflight-source-bindings-r4.json` | `0600` / `dc6034f8c151d53857b0d78e5417fbff2e5dd8d66e710a2ec6f9f731a20059ae` |
| `/private/tmp/add-role-first-review-routing-p1r4-20260820-7X9r4J/source-delta-allowlist-r4.txt` | `0600` / `c170a3530a13c7aee65ec28b2c64ff16d545fa804ef8569ed9cc3eda5f235ff5` |
| `/private/tmp/add-role-first-review-routing-p1r4-20260820-7X9r4J/role-first-forward-summary-r4.json` | `0600` / `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |

The successful private delta reports `54` actual path changes, `58` exact
allowlist entries, and `unexpected_paths: []`. The durable summary, appended
source verification, and this R4 input record were written after the private
delta and are evidence-only. A fresh no-Git reconstruction should therefore
classify `56` actual paths, with unchanged `CONTEXT.md` and the still-absent R4
Review artifact as the two non-actual allowlist entries. Bind and classify
these explicitly; they are not candidate implementation bytes.

The first R4 delta attempt passed preflight inventories where source-start
inventories were required. It failed with `source inventory fields are
invalid`, created only the retained failed-attempt compare directory, and did
not write `source-delta-r4.json`. The successful retry used the bound
reconstructed source-start baselines and new output/compare paths. Verify this
classification; do not represent the first invocation as a product defect or
the retry as the same transaction.

## Prior findings and required integrity proof

The first three correction generations addressed final-leaf identity,
existing parent chains, direct receipt rollback, public contracts, missing
parent descriptor-relative creation, exact directory quarantine cleanup, and
durable post-history blockers. The P1 R3 Review accepted those corrected areas
but found that restore trusted a planned `logical_path` paired with an
independently supplied, internally valid `path` and `chain`.

The P1 R4 candidate claims:

- the bound backup manifest produces one deterministic de-duplicated ordered
  created-parent plan and rejects malformed per-entry hierarchies;
- `prepared` accepts no records, `applied-uncommitted` requires the exact full
  planned sequence, and `mutation-intent` recovery accepts only the exact
  deterministic created prefix while rejecting any present unrecorded planned
  directory;
- before any restore mutation, every logical path must be a directory, resolve
  to the recorded absolute path, and reproduce the exact full root-to-leaf
  device/inode/mode/owner/group chain;
- duplicate identities, reordered records, logical/path/chain substitution,
  truncated provenance, missing/extra records, hierarchy changes, and empty or
  non-empty unrelated directories all block before target content changes;
- rejection moves the pending receipt to `recovery-blocked`, preserves all
  unrelated and actual created-parent state, and prevents later-target and
  recovery progress.

Trace these claims through actual production path:line mechanisms and tests.
Use only isolated temporary software-correctness checks against production
functions. Cover full and prefix receipt states, logical-path/path mismatch,
valid-chain substitution, mapping/link/type changes, truncated root
provenance, missing/extra/reordered records, wrong depth/hierarchy, duplicate
identity, empty/non-empty unrelated directories, exact actual cleanup, crash
recovery, no pre-rejection leaf mutation, durable blocked state, and every
later gate.

Also re-evaluate all previously passing areas: role-first routing, concrete
assignment, schema-6/schema-2 evidence identity, current/legacy isolation,
four-target manifest/plan semantics, sensitive exclusions, deterministic
discovery, public docs, shared-byte parity, all earlier correction branches,
and the complete changed-record set.

## Fresh verification evidence

- focused fourth-correction tests: RED `3` expected failures / `0` errors,
  then GREEN, including empty/non-empty substitution, hierarchy, identity,
  missing/extra/reordered, and truncated-provenance cases;
- full cross-CLI module: `89` tests, `OK`;
- Router full suite: `213` tests, `OK`;
- Companion full suite: `87` tests, `OK`;
- both quick/project validators: `PASS`;
- OpenSpec strict/all: `PASS`, `3 passed / 0 failed`;
- both exact static negative searches: empty;
- shared Handoff and validator-core byte checks: `PASS`;
- sensitive audit: `0 sensitive categories found`;
- forward model cases: `6/6`, all result rows `PASS`;
- complete source delta retry: `PASS`, `54` actual, `58` allowlisted,
  `unexpected_paths: []`.

The original isolated Conda interpreter remains unavailable because its real
`bin/python3.11` object is externally absent while its symlinks remain. Current
quick validators used `/opt/anaconda3/bin/python`, previously accepted for this
gate; dependency-free validators/tests used default `python3`. Do not present
this as an exact replay of the missing old environment.

The governed `scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc`
path remains absent. The historical `cpython-311.pyc` was not touched.

## Required output

Return one complete Review artifact with:

1. reviewer assignment and independence statement;
2. start/end hash and mode checks for every bound primary/private input;
3. complete-delta coverage and post-delta evidence-only classification;
4. requirement-to-production-mechanism-to-test traces with path:line evidence;
5. explicit software-integrity analysis of all correction generations and
   every recovery branch;
6. fresh validation commands/results plus sensitive/shared-byte checks;
7. findings ordered by severity with exact correction/resume conditions;
8. one final verdict: `PASS`, `FAIL`, or `BLOCKED`;
9. an explicit statement whether read-only runtime planning may begin.

Do not modify any file, run Git, run Pi, inspect or mutate runtime
destinations, create a runtime plan, accept your own verdict, or claim
completion. Use neutral software-correctness language and do not include
executable misuse examples.
