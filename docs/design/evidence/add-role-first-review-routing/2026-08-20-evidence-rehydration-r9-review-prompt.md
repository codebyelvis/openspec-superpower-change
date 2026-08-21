# Independent R9 Evidence-Rehydration Preflight

You are a fresh Codex instance acting only as the independent reviewer for the
`add-role-first-review-routing` Task 6 R9 recovery amendment.

## Reviewer Assignment

- purpose: decide whether the original Codex control plane may execute only
  Task 6 Step 5A, then Step 6 after Step 5A exits `0`
- reviewer product: `codex`
- reviewer role: `independent-reviewer`
- capability profile: `control-plane-high`
- independence: distinct from the Plan/amendment author, evidence preparer,
  failed-attempt investigator, and future cache/source-delta executor
- result authority: governed R9 Plan Preflight evidence only

Your verdict does not mutate source or runtime, accept itself, complete the
OpenSpec change, archive, publish, or replace the original control plane.

## Bound primary inputs

Read every primary input completely:

1. `/Users/elvis/file/develop/opensource/openspec-superpower-change/docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md`
   - expected SHA-256:
     `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229`
2. `/Users/elvis/file/develop/opensource/openspec-superpower-change/docs/design/evidence/add-role-first-review-routing/2026-08-20-evidence-rehydration-r9-inputs.md`
   - expected SHA-256:
     `dcc8658bb014a0e7140a5a4e0eda733f921544c2911422e0bc2d8fef183d2903`
3. `/Users/elvis/file/develop/opensource/openspec-superpower-change/docs/design/evidence/add-role-first-review-routing/2026-08-10-plan-preflight-inputs.md`
4. `/Users/elvis/file/develop/opensource/openspec-superpower-change/docs/design/evidence/add-role-first-review-routing/2026-08-12-source-delta-recovery-r8-r2-inputs.md`
5. `/Users/elvis/file/develop/opensource/openspec-superpower-change/docs/design/reviews/2026-08-11-add-role-first-review-routing-source-delta-recovery-r8-review.md`
6. `/Users/elvis/file/develop/opensource/openspec-superpower-change/docs/design/evidence/add-role-first-review-routing/2026-08-10-source-verification.md`

Read and verify these private R9-r2 artifacts without modifying them:

- root:
  `/private/tmp/add-role-first-review-routing-r9-r2-20260820-4hEfNB`
- preparation script `prepare-r9-r2.py`, expected SHA
  `60a6ef3d951f84b54957d6ccc52b2171d07fad73d1b46b01f32f95ae71a0d83a`
- preparation manifest `preparation-manifest-r9.json`, expected SHA
  `e84741b7c94f30bd0bdefed845fc991819ea1474d7431705f09bcdc2e8b14edf`
- bindings `preflight-source-bindings-r9.json`, expected SHA
  `5462cf683a8eb92439e7364100d2f6f467c7e3bd06e7fc4581445aea80aa3b7a`
- compatibility receipt `preflight-input-compatibility-r9.json`, expected SHA
  `13898312f910b9a07f4804989eae7be04e758dd472172a6612beb22109a2501b`
- continuity receipt `continuity-r9.json`, expected SHA
  `11c0f63eb5248974baffac7561eecdd6edc2f677b66cb3c8ea56298936bc220a`
- exact allowlist and both reconstructed/preflight inventories
- both 36-file preimage archives and their safe member lists
- both original pre-R9 and fresh pre-r2 current-tree backup archives; list
  members only, never extract or restore them

The target Review artifact must still be absent when you begin:

`/Users/elvis/file/develop/opensource/openspec-superpower-change/docs/design/reviews/2026-08-20-add-role-first-review-routing-evidence-rehydration-r9-review.md`

## Required review questions

1. Do the 36 recovered files match every durable R4 path/SHA pair, with no
   native file contents or authority silently substituted?
2. Are the ten bounded `git cat-file blob` reads narrow, reproducible, and
   non-mutating, and is the earlier no-Git process deviation disclosed rather
   than rewritten as compliant history?
3. Do the R8-r2 continuity projections mechanically reach the exact persisted
   Router and Companion snapshot hashes and record counts?
4. Is the reconstructed-baseline meaning honest and sufficient: candidate
   source bytes roll back to hash-proven preimages; only the three documented
   absent files and old generated-cache record are projected; R9 freezes rather
   than fabricates Plan/OpenSpec/evidence history?
5. Are archives, modes, counts, baselines, Preflight snapshots, allowlist and
   bindings structurally compatible with the current source-delta validator?
6. Is the 43-entry allowlist exact, unique, wildcard-free, and limited to the
   governed source/evidence paths required before Step 6?
7. Does the Step 5A transaction still bind exactly one cache path, current
   bytes and filesystem identity, create durable backup/evidence before an
   exclusive same-filesystem move, stop on ambiguity, and avoid unlink,
   overwrite, recursive cleanup, or broad restore?
8. Do the failed preparation/compatibility attempts remain preserved and
   non-authorizing, without contaminating revision-2 inputs?
9. Does R9 leave OpenSpec, Handoff, independent Review, PASS/FAIL/BLOCKED,
   Completion, control-plane authority, executor/reviewer isolation, runtime,
   Pi, archive and publication semantics unchanged?
10. Is there any P0/P1 issue that makes Step 5A or Step 6 unsafe or
    non-reproducible?

## Tool and mutation boundary

Use only read-only filesystem commands needed to read, hash, stat, list archive
members, and inspect JSON/text. Do not run Git, extract archives, create files,
write the Review artifact, execute the preparation script, run Step 5A or
source-delta, move/delete the cache, edit either repository/runtime, invoke Pi,
clean temporary roots, update OpenSpec/canonical state, archive, publish, or
claim completion.

## Required output

Return one self-contained review with:

- `Verdict: PASS | FAIL | BLOCKED`
- `Decision scope`: exactly R9 Plan Preflight for Task 6 Steps 5A–6
- `Input verification`: hashes/modes/counts checked and any residual
- `Findings`: ordered by severity; each has ID, severity, evidence location,
  problem, impact, and exact required correction; write `none` only if none
- `Governance invariants`: explicit result for authority, isolation,
  PASS/FAIL/BLOCKED, Completion, Git/runtime/Pi/archive/publication boundaries
- `Authorized next action`: for PASS, only original control-plane acceptance
  and Step 5A, then Step 6 after Step 5A exit `0`; otherwise the precise blocker

Do not broaden a PASS into source correctness, runtime readiness, whole-task
completion, archive, publication, or cleanup authority.
