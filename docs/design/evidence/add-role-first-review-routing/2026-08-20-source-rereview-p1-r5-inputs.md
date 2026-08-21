# Candidate Source High Re-review Inputs — P1 R5

## Assignment and authority

- reviewer product: `codex`
- reviewer role: `independent-reviewer`
- reviewer profile: `control-plane-high`
- reviewer implementation: fresh no-history `gpt-5.6-luna` with `max`
  reasoning, distinct from all authors, executors, prior reviewers, and the
  bound decision owner
- purpose: independently decide whether the fifth-corrected candidate source
  satisfies the approved change and may return to read-only four-target
  runtime planning
- result authority: governed implementation Review evidence only; the reviewer
  cannot mutate source/runtime, accept its own result, update canonical state,
  or claim completion

The original control plane accepts only an explicit `PASS`, `FAIL`, or
`BLOCKED`. Any actionable finding blocks runtime planning and returns the
candidate to correction, complete fresh verification/delta, and another Review
revision.

## Required read set and bindings

Read both project `AGENTS.md` and `SKILL.md` files completely, then the approved
OpenSpec change and Plan, engineering invariants, project-learning closeout,
synchronization contracts, complete source verification, all prior source
Reviews, the runtime Sync-plan FAIL Review, complete current Router and
Companion trees, every changed/added record, production code, and tests. Do not
rely on this record instead of the actual files.

Primary mode-`0644` inputs:

| Input | SHA-256 |
|---|---|
| `docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md` | `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| `openspec/changes/add-role-first-review-routing/proposal.md` | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| `openspec/changes/add-role-first-review-routing/design.md` | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| `openspec/changes/add-role-first-review-routing/specs/skill-workflow-governance/spec.md` | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| `openspec/changes/add-role-first-review-routing/tasks.md` | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| `docs/design/evidence/add-role-first-review-routing/2026-08-10-source-verification.md` | `52bca43ed01b18f959f3afe6bca22016d98cf584737a0ef88d0107cc3cc6050b` |
| `docs/design/evidence/add-role-first-review-routing/2026-08-20-source-delta-p1-r5-summary.json` | `8dfb1971406017fa388ee96eb8c309fef39c33089069703e468e9f8e3afdadac` |
| first source FAIL `docs/design/reviews/2026-08-10-add-role-first-review-routing-source-review.md` | `35050b3e8766b055f11d3a55018d4a34c1aca87893f574b477bbfe28a9cf6ef1` |
| P1 R1 source FAIL | `44138637110b7643585d244721cf710f1f08a899dca874fd81df6ab1898d9719` |
| P1 R2 source FAIL | `5991be2198f4387bb0e860733352fb98e063e22bfcd694eacd3f4704932429b3` |
| P1 R3 source FAIL | `c451abf26592caa0630f8d3b2d272e740ddde40d959cccc79f5d672d4b379c47` |
| P1 R4 source PASS `docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r4.md` | `579c4486fadd8574af24ae112e81519b87d266cdecb0621c30b7c176ec0dce70` |
| runtime Sync-plan FAIL `docs/design/reviews/2026-08-20-add-role-first-review-routing-runtime-sync-plan-review.md` | `8562b0ed1d4ef17dc34f100e783e72b02ae40138f8888b7516ef2566ecb255a8` |
| corrected `scripts/validate_cross_cli_sync.py` | `332de6171495faa12b3acd6c7c39e8ee35972a9c87eebe216d9581cc3b520044` |
| corrected `tests/test_cross_cli_sync.py` | `97d46aec7247ab9e0f93d60b2c017248e22e4b54d2c53f3f01eaa83d0c9b1ed2` |
| Router `tests/test_workflow_rules.py` | `9e8f1d6904b0eb3e397eafb305f0e1743a77dcd9d9c715ac05e510f4e3aa2dc7` |
| Router `README.md` | `44314b9c0f128ddcac90154ac5f36f167f70a66ab93aca61a4b46a86646f08ff` |
| Router `README_cn.md` | `b973047e8092a9b7550ab62db5e795c6a7a0ba30e51304a2541953d4379fb987` |
| Companion `README.md` | `f260de8c1e97ca5ce282e39c432278ebed4699745d0cd6c650dc82ece9ffe0b5` |
| Companion `README_cn.md` | `d6180a9a0f54fc0d87934bd24efe320d5f9c7b45cb816292f86db5d1ba2b601c` |
| Companion `tests/test_workflow_rules.py` | `65f8e4f2de06dfd050ef74310c94a84d76cec2b54c1955a1fdb66372d5f0b12c` |

Private read-only reproduction inputs:

| Input | Mode / SHA-256 |
|---|---|
| `/private/tmp/add-role-first-review-routing-p1r5-20260820-WeKcZW/source-delta-r5.json` | `0600` / `9c094d37cc8a3d9994b0b255a2b2e8ff94a3440c306eb13690846d2a37da57a0` |
| `/private/tmp/add-role-first-review-routing-p1r5-20260820-WeKcZW/source-compare-r5` | `0700` |
| `/private/tmp/add-role-first-review-routing-p1r5-20260820-WeKcZW/preflight-source-bindings-r5.json` | `0600` / `8bdf40b33323b4d8c3f197946935d2e9d958fe7b418fa8e06393657c914cc9e6` |
| `/private/tmp/add-role-first-review-routing-p1r5-20260820-WeKcZW/source-delta-allowlist-r5.txt` | `0600` / `6f4c8b5b8fcd02edadc3eafcd74bf80930c4f83a5988525634152ba53b74a005` |
| `/private/tmp/add-role-first-review-routing-p1r5-20260820-WeKcZW/role-first-forward-summary-r5.json` | `0600` / `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |
| R5 backup root | `0700` |
| `validate_cross_cli_sync.py.before` | `0600` / `8d8a18a4c6d9a7639fe963e08c1a799b0c5a531129fd6195c8cd9fd8c4315f1e` |
| `test_cross_cli_sync.py.before` | `0600` / `15f787aa7f0e23fd60611d3d0c5639b1541aba7b760fd88d93efe635f8a37aa3` |
| `source-verification.md.before` | `0600` / `bbcf2cc726876409aae30b7cac577a198e8341593c04b74f5f4084caeab84f95` |

The bound delta reports `60` actual paths (`46` Router, `14` Companion), `64`
exact allowlist entries, and `unexpected_paths: []`. The durable R5 summary,
source-verification append, and this input are evidence-only post-delta records.
A fresh no-Git reconstruction should therefore report `62` actual paths, with
unchanged `CONTEXT.md` and the still-absent intended P1 R5 Review artifact as
the two non-actual allowlist entries. Bind and classify this explicitly.

## P1 R5 integrity proof

The Sync-plan Review found that runtime backup and transaction roots could be
accepted inside any declared Skill discovery root. The R5 candidate claims:

- one shared guard resolves a proposed private root and compares it to all four
  plan-bound `skills_root` values;
- equal or nested backup/transaction roots, including existing symlink
  resolution into discovery, are rejected;
- apply rejects both roots before creating a transaction directory/lock,
  target backup/manifest, initial receipt, or destination mutation;
- `_prepare_target_backup` and the transaction lock also enforce the guard, and
  restore, recover-pending, content/discovery verification, commit, and
  verify-all cannot bypass it;
- safe roots outside every discovery root retain the existing durable backup,
  receipt, rollback, recovery-blocked, and later-target behavior;
- tests exercise both private-root kinds against every declared discovery root
  and prove no unsafe root, receipt, backup, or destination side effect occurs.

Trace every claim through actual path:line production mechanisms and tests.
Use only isolated temporary probes against production functions. Adversarially
cover equality, nested roots, another target's discovery root, relative and
normalized paths, existing symlink ancestors, fail-before-side-effect ordering,
direct helper entry, restore/recovery entry, and safe outside roots. Re-evaluate
the complete earlier correction history: leaf/parent identity, missing-parent
creation, parent-record semantic binding, exact cleanup, receipt-history
ambiguity, later-target exclusion, four-target ordering, role-first routing,
schema-6/schema-2 identity, legacy isolation, discovery, exclusions, docs,
shared bytes, and complete changed records.

## Fresh verification evidence

- P1 R5 focused RED: eight expected subcase failures, then GREEN;
- cross-CLI module: `91` tests, `OK`;
- Router full suite: `215` tests, `OK`;
- Companion full suite: `87` tests, `OK`;
- both quick/project validators: `PASS`;
- OpenSpec strict/all: `PASS`, `3 passed / 0 failed`;
- exact static negative searches: empty;
- shared Handoff and validator-core byte checks: `PASS`;
- sensitive audit: `0 sensitive categories found`;
- forward model cases: `6/6`, all result rows `PASS`, transient root absent;
- source delta: `PASS`, `60` actual, `64` allowlisted, `unexpected=[]`.

The original reviewed Conda interpreter remains unavailable. Quick validators
used the previously accepted `/opt/anaconda3/bin/python`; dependency-free
validators/tests used default `python3`. Do not present this as exact replay of
the missing interpreter.

The governed `scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc`
path is absent. The historical `cpython-311.pyc` was not changed.

## Required output

Return one complete neutral Markdown Review with assignment/independence,
start/end bindings, complete-delta classification, requirement→mechanism→test
traces, adversarial production-path probes, all correction generations and
recovery branches, fresh validation evidence, findings by severity with exact
resume conditions, one final `PASS`/`FAIL`/`BLOCKED`, and an explicit statement
whether read-only four-target runtime planning may resume.

Do not modify any file, run Git or Pi, inspect or mutate runtime destinations,
create a runtime plan, accept your own verdict, or claim completion. The
existing reviewed plan is stale after the R5 source change and must not be used
for apply even if this source Review passes.
