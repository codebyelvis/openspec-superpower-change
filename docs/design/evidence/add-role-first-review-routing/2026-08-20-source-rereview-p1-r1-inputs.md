# Candidate Source High Re-review Inputs — P1 R1

## Assignment and authority

- reviewer product: `codex`
- reviewer role: `independent-reviewer`
- reviewer profile: `control-plane-high`
- reviewer instance: a fresh no-history instance distinct from every author,
  executor, prior reviewer, and the bound decision owner
- purpose: adversarially decide whether the corrected candidate source may
  proceed to read-only four-target runtime planning
- result authority: implementation-evidence-only; the reviewer cannot mutate
  source/runtime, accept its own result, update canonical state, or claim
  completion

The original control plane accepts only an explicit `PASS`, `FAIL`, or
`BLOCKED`. Any actionable finding blocks runtime planning and returns the
candidate to correction plus fresh full verification and a new Review revision.

## Required read set

Read the complete current Router and Companion trees, including local
instructions, the approved OpenSpec change, Plan, source verification, complete
delta summary, and prior FAIL Review. Do not rely on this summary instead of
inspecting the actual implementation/tests and every changed or added record.

Primary bound inputs:

| Input | SHA-256 |
|---|---|
| `docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md` | `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| `openspec/changes/add-role-first-review-routing/proposal.md` | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| `openspec/changes/add-role-first-review-routing/design.md` | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| `openspec/changes/add-role-first-review-routing/specs/skill-workflow-governance/spec.md` | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| `openspec/changes/add-role-first-review-routing/tasks.md` | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| `docs/design/evidence/add-role-first-review-routing/2026-08-10-source-verification.md` | `aaeb40bece860114b48327e6b67b5968c2832dfcb66c71ff6fd56ea7c13103d5` |
| `docs/design/evidence/add-role-first-review-routing/2026-08-20-source-delta-p1-r1-summary.json` | `8c45a79406b09e5f7fafe0c5230c7ccac6ebcb2ca39dcbdbcb03c22a742f8adf` |
| prior `docs/design/reviews/2026-08-10-add-role-first-review-routing-source-review.md` | `35050b3e8766b055f11d3a55018d4a34c1aca87893f574b477bbfe28a9cf6ef1` |
| corrected `scripts/validate_cross_cli_sync.py` | `9f1cd9092cd0d98c18197437d7afc6911d63eda864eb5c4b73c391d67e759669` |
| corrected `tests/test_cross_cli_sync.py` | `6b905e56fcb6d94eb01f4861b52ba9a063b2ad4c8a5e2191b6f924fcda6121f4` |

Private read-only reproduction inputs:

| Input | Mode / SHA-256 |
|---|---|
| `/private/tmp/add-role-first-review-routing-p1-toctou-20260820-VueWBG/source-delta-p1-r2.json` | `0600` / `c0e04d2c838f8694a0f78cd31263713119415225a13c71fcffd4c66df15b0f6d` |
| `/private/tmp/add-role-first-review-routing-p1-toctou-20260820-VueWBG/source-compare-p1-r2` | `0700` |
| `/private/tmp/add-role-first-review-routing-p1-toctou-20260820-VueWBG/preflight-source-bindings-p1-r2.json` | `0600` / `a47a40f3878f7b34cb7fe73d36635e495b60c28b00eac57848ae2ba4f4293b71` |
| `/private/tmp/add-role-first-review-routing-p1-toctou-20260820-VueWBG/source-delta-allowlist-p1-r2.txt` | `0600` / `5bcf0351ab9e0f5ef750b7d0034405ab215d3fb1156ac731df1026108fe7b2b3` |
| `/private/tmp/add-role-first-review-routing-p1-toctou-20260820-VueWBG/role-first-forward-summary-p1-r1.json` | `0600` / `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |

The complete delta reports `45` actual path changes, `49` exact allowlist
entries, and `unexpected_paths: []`. The durable summary and this input record
were written after the private delta and are classified as evidence-only
post-delta additions. The source-verification bytes after the private delta are
bound above. They are not candidate implementation bytes.

## Prior finding and required adversarial proof

The prior High Review returned `FAIL` with one P1: apply and restore checked a
destination before mutation and then unconditionally replaced or removed it.
The candidate claims the correction binds the actual displaced object at the
namespace mutation boundary:

- existing install/restore destinations: `RENAME_SWAP`, validate displaced
  object, rollback mismatch;
- absent install destinations: `RENAME_EXCL`, fail closed on concurrent create;
- restore-to-absent: exclusive move into unique quarantine, validate moved
  object, rollback mismatch;
- ambiguous rollback: preserve recovery evidence and require manual
  disposition.

Trace these claims through production path:line mechanisms and tests. At a
minimum, adversarially evaluate post-check drift for existing files, absent
files, symlinks, type changes, create-write failure, apply rollback, restore
rollback, and an external writer that races the rollback itself. Decide whether
any path can still overwrite/delete unreviewed destination state or falsely
report a verified restore.

Also re-evaluate all previously PASS areas: role-first routing, concrete
assignment, schema-6 and schema-2 evidence identity, current/legacy isolation,
four-target manifest/plan semantics, sensitive exclusions, deterministic
discovery, receipt durability/recovery, public docs, shared-byte parity, and
the full changed-record set.

## Fresh verification evidence

- focused new race tests: RED `6` failures / `0` errors, then GREEN `6/6`;
- full cross-CLI module: `69` tests, `OK`;
- Router full suite: `192` tests, `OK`;
- Companion full suite: `86` tests, `OK`;
- both quick/project validators: `PASS`;
- OpenSpec strict/all: `PASS`, `3 passed / 0 failed`;
- both static negative searches: empty;
- shared Handoff and validator-core byte checks: `PASS`;
- sensitive audit: `0 sensitive categories found`;
- forward model cases: `6/6`, `forward: "pass"`;
- complete source delta: `PASS`, `45` actual, `49` allowlisted,
  `unexpected_paths: []`.

The exact Task 6 isolated Conda interpreter cannot be replayed because its real
`bin/python3.11` object is externally absent while its symlinks remain. The
failed replay stopped before tests. Current quick validators used
`/opt/anaconda3/bin/python`, as accepted by the prior High Review; all fallback
validators/tests used default `python3`. Treat this openly recorded evidence
drift according to the approved contract rather than silently substituting a
claim that the old environment was replayed.

## Required output

Return one complete Review artifact with:

1. reviewer assignment and independence statement;
2. start/end hash and mode checks for every bound primary/private input;
3. complete-delta coverage and evidence-only classification;
4. requirement-to-production-mechanism-to-test traces with path:line evidence;
5. explicit adversarial analysis of the prior P1 and rollback-race boundaries;
6. fresh validation commands/results and sensitive/shared-byte checks;
7. findings ordered by severity with exact correction/resume conditions;
8. one final verdict: `PASS`, `FAIL`, or `BLOCKED`;
9. an explicit statement whether read-only runtime planning may begin.

Do not modify any file, run Git, run Pi, access or mutate runtime destinations,
create a runtime plan, accept your own verdict, or claim completion.
