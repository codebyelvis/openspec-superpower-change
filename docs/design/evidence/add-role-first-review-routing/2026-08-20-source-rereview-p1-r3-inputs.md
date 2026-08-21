# Candidate Source High Re-review Inputs — P1 R3

## Assignment and authority

- reviewer product: `codex`
- reviewer role: `independent-reviewer`
- reviewer profile: `control-plane-high`
- reviewer instance: a fresh no-history instance distinct from all authors,
  executors, prior reviewers, and the bound decision owner
- purpose: independently decide whether the thrice-corrected candidate source
  satisfies the approved change and may proceed to read-only four-target
  runtime planning
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
source verification, all three prior FAIL Reviews, the complete current delta,
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
| `docs/design/evidence/add-role-first-review-routing/2026-08-10-source-verification.md` | `fba7622846aecde308a7289958056b54aee0781b3af4a99ab2d2f4fe6a038f4a` |
| `docs/design/evidence/add-role-first-review-routing/2026-08-20-source-delta-p1-r3-summary.json` | `6b02a2a5a97155b80d0cff2a02efcdcfd73537719645b5e35a2c9f9095ea447c` |
| first FAIL `docs/design/reviews/2026-08-10-add-role-first-review-routing-source-review.md` | `35050b3e8766b055f11d3a55018d4a34c1aca87893f574b477bbfe28a9cf6ef1` |
| P1 R1 FAIL `docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r1.md` | `44138637110b7643585d244721cf710f1f08a899dca874fd81df6ab1898d9719` |
| P1 R2 FAIL `docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r2.md` | `5991be2198f4387bb0e860733352fb98e063e22bfcd694eacd3f4704932429b3` |
| corrected `scripts/validate_cross_cli_sync.py` | `a6420e3ee88a606a0ccf963fe04d7725d53e995526d76abb07a8bef8ca307202` |
| corrected `tests/test_cross_cli_sync.py` | `fbb702da40475a442c6abe6ea98ce4e337f8d6751a405853fd38f7abc64a2f95` |
| Router `tests/test_workflow_rules.py` | `9e8f1d6904b0eb3e397eafb305f0e1743a77dcd9d9c715ac05e510f4e3aa2dc7` |
| Router `README.md` | `44314b9c0f128ddcac90154ac5f36f167f70a66ab93aca61a4b46a86646f08ff` |
| Router `README_cn.md` | `b973047e8092a9b7550ab62db5e795c6a7a0ba30e51304a2541953d4379fb987` |
| Companion `README.md` | `f260de8c1e97ca5ce282e39c432278ebed4699745d0cd6c650dc82ece9ffe0b5` |
| Companion `README_cn.md` | `d6180a9a0f54fc0d87934bd24efe320d5f9c7b45cb816292f86db5d1ba2b601c` |
| Companion `tests/test_workflow_rules.py` | `65f8e4f2de06dfd050ef74310c94a84d76cec2b54c1955a1fdb66372d5f0b12c` |

Private read-only reproduction inputs:

| Input | Mode / SHA-256 |
|---|---|
| `/private/tmp/add-role-first-review-routing-p1r3-20260820-3nND1z/source-delta-r3.json` | `0600` / `8a60ac663085bc765e49a30e47a1a19d10bbf3c19a78a574c6a0aa116fe027d8` |
| `/private/tmp/add-role-first-review-routing-p1r3-20260820-3nND1z/source-compare-r3` | `0700` |
| `/private/tmp/add-role-first-review-routing-p1r3-20260820-3nND1z/preflight-source-bindings-r3.json` | `0600` / `bdbfa99b93bd17ff86c61a2f119b1c07a74785fb868519d80e1f5ed9f5060d6f` |
| `/private/tmp/add-role-first-review-routing-p1r3-20260820-3nND1z/source-delta-allowlist-r3.txt` | `0600` / `cfa09d50b6c83e13d252ddd4f9bdbbced55dcc86503ee6bbccad8b50c95eb847` |
| `/private/tmp/add-role-first-review-routing-p1r3-20260820-3nND1z/role-first-forward-summary-r3.json` | `0600` / `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |

The complete delta reports `51` actual path changes, `55` exact allowlist
entries, and `unexpected_paths: []`. The durable summary, appended source
verification, and this R3 input record were written after the private delta and
are evidence-only post-delta records. Bind and classify them explicitly; they
are not candidate implementation bytes.

## Prior findings and required integrity proof

The first Review found leaf replacement/removal that was not bound to the
actual displaced object. P1 R1 added exchange, exclusive install, displaced
object validation, rollback, and quarantine. P1 R1 re-review then found
unbound existing-parent mappings, receipt-displacement loss, and stale public
schema guidance. P1 R2 bound existing parent chains, repaired direct receipt
rollback, and corrected public docs.

The P1 R2 Review found three remaining branches:

1. initially absent parents were created by path before a descriptor guard;
2. restore removed recorded directories by path and suppressed cleanup errors;
3. failure after history installation and failed receipt rollback could leave
   a live `verified` revision without a blocker recognized by later targets.

The P1 R3 candidate claims:

- every missing component is created exclusively from a verified ancestor
  descriptor, opened no-follow, bound by full identity/chain, recorded durably
  in the transaction receipt before leaf installation, and rechecked while the
  final descriptor remains open through install;
- restore accepts only recorded exact created-parent identities and removes
  them in reverse depth order through descriptor-relative exclusive quarantine,
  restoring or preserving any non-empty/mismatched object and blocking instead
  of reporting success;
- every receipt-history transition has a durable manual-disposition marker
  before the history move, removes it only after proven success or exact
  rollback, and all verification/commit/recovery/later-target/verify-all gates
  reject retained markers.

Trace these claims through actual production path:line mechanisms and tests.
Use only isolated temporary correctness/interleaving checks against production
functions. Cover missing multilevel parent mapping/link/type/ancestor changes,
crash or failure between directory creation and receipt persistence, malformed
or incomplete parent identity records, non-empty directory cleanup, cleanup
rollback ambiguity, history move/durability/parent-check failures, successful
and failed rollback, blocker durability, and every later gate.

Also re-evaluate all previously passing areas: role-first routing, concrete
assignment, schema-6/schema-2 evidence identity, current/legacy isolation,
four-target manifest/plan semantics, sensitive exclusions, deterministic
discovery, public docs, shared-byte parity, and the complete changed-record
set.

## Fresh verification evidence

- focused third-correction tests: RED `5` expected failures / `0` errors, then
  GREEN `5/5`, plus `3` additional GREEN integrity cases;
- full cross-CLI module: `84` tests, `OK`;
- Router full suite: `208` tests, `OK`;
- Companion full suite: `87` tests, `OK`;
- both quick/project validators: `PASS`;
- OpenSpec strict/all: `PASS`, `3 passed / 0 failed`;
- both exact static negative searches: empty;
- shared Handoff and validator-core byte checks: `PASS`;
- sensitive audit: `0 sensitive categories found`;
- forward model cases: `6/6`, all result rows `PASS`;
- complete source delta: `PASS`, `51` actual, `55` allowlisted,
  `unexpected_paths: []`.

The original isolated Conda interpreter remains unavailable because its real
`bin/python3.11` object is externally absent while its symlinks remain. Current
quick validators used `/opt/anaconda3/bin/python`, previously accepted for this
gate; dependency-free validators/tests used default `python3`. Do not present
this as an exact replay of the missing old environment.

The evidence openly records one syntax-check-generated
`validate_cross_cli_sync.cpython-314.pyc`; only that exact newly created cache
file was removed after its identity and creation time were verified. The
historical `cpython-311.pyc` was not touched, and the complete delta proves the
governed `cpython-314.pyc` path absent with no unexpected cache path.

## Required output

Return one complete Review artifact with:

1. reviewer assignment and independence statement;
2. start/end hash and mode checks for every bound primary/private input;
3. complete-delta coverage and post-delta evidence-only classification;
4. requirement-to-production-mechanism-to-test traces with path:line evidence;
5. explicit software-integrity analysis of all three correction generations
   and every recovery branch;
6. fresh validation commands/results plus sensitive/shared-byte checks;
7. findings ordered by severity with exact correction/resume conditions;
8. one final verdict: `PASS`, `FAIL`, or `BLOCKED`;
9. an explicit statement whether read-only runtime planning may begin.

Do not modify any file, run Git, run Pi, inspect or mutate runtime
destinations, create a runtime plan, accept your own verdict, or claim
completion. Use neutral software-correctness language and do not include
executable misuse examples.
