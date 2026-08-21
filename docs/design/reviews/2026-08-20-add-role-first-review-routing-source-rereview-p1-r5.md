# Candidate Source High Re-review — P1 R5

## Assignment and authority

- Reviewer: fresh no-history `codex / independent-reviewer / control-plane-high`.
- Scope: Router and Companion source candidate for `add-role-first-review-routing`.
- This is evidence only. It does not update canonical state, accept the candidate, create a Review artifact, generate a runtime plan, inspect runtime destinations, run Git/Pi, or claim task completion.

## Binding and delta

- Input mode: `0644`.
- Input SHA-256: `9f95e38b666b862f2c954ec8e7d3b91f2528ec4756c508ae06c158a681ef4766`.
- Bound primary Plan, OpenSpec artifacts, source/tests, Reviews, and runtime Sync-plan Review hashes matched the input.
- R5 summary SHA-256: `8dfb1971406017fa388ee96eb8c309fef39c33089069703e468e9f8e3afdadac`.
- Private delta input: mode `0600`, SHA-256 `9c094d37cc8a3d9994b0b255a2b2e8ff94a3440c306eb13690846d2a37da57a0`.
- Compare root: mode `0700`.
- Bound delta: `60` source records (`46` Router, `14` Companion), `64` allowlist entries, `unexpected_paths: []`.
- Fresh no-Git classification: `62` actual paths; unchanged `CONTEXT.md` and the absent intended R5 Review are the two non-actual allowlist entries.
- `source-verification.md` differs from the private delta-after hash only because of the disclosed evidence-only post-delta append; its current bound hash is `52bca43ed01b18f959f3afe6bca22016d98cf584737a0ef88d0107cc3cc6050b`.
- Intended Review artifact remained absent at both boundaries. Governed `cpython-314.pyc` also remained absent.

All changed records were covered:

- Router public surfaces: `CHANGELOG.md`, `README.md`, `README_cn.md`, `SKILL.md`.
- Router evidence/history: all R9, R1–R4, runtime Sync-plan inputs/summaries/prompts and source-verification records.
- Router Reviews: original source Review, R1–R4 source Reviews, evidence-rehydration Review, runtime Sync-plan Review.
- Router governance: all 13 changed routing, contract, synchronization, manifest, completion, and Superpowers references.
- Router implementation/tests: `validate_core_gates.py`, `validate_cross_cli_sync.py`, fixtures, forward runner, both test modules, and deleted governed bytecode.
- Companion public surfaces, `agents/openai.yaml`, all seven execution/review templates, validator, and workflow tests.

## P1 R5 mechanism trace

| Requirement | Production mechanism | Evidence |
|---|---|---|
| Reject private roots equal to or nested under any discovery root | Shared `_assert_runtime_root_outside_discovery()` resolves the candidate and compares against all four `TARGET_ORDER` discovery roots (`scripts/validate_cross_cli_sync.py:1204-1234`). | Equality, nested, other-target, relative-normalized, and symlink-ancestor probes all rejected. |
| Lock cannot bypass guard | `_target_transaction_lock()` invokes the shared guard before `_ensure_private_directory`, lock creation, or fsync (`:1285-1310`). | Direct lock-entry probes rejected before transaction side effects. |
| Direct backup helper cannot bypass guard | `_prepare_target_backup()` invokes the guard before private-root creation, target backup, objects, or manifest (`:1716-1772`). | Direct helper probes rejected before backup side effects. |
| Apply fails before any side effect | `apply_target()` validates both backup and transaction roots before lock, backup, receipt, or destination mutation (`:1871-1901`). | Receipt, backup, transaction, safe roots, and destination snapshots remained unchanged. |
| Restore/recovery/verification/commit/verify-all cannot bypass guard | Public restore and recovery guard both roots (`:2360-2389`, `:2589-2663`); verification and commit acquire the guarded lock (`:2473-2586`); verify-all guards before private-root use (`:2666-2691`). | All corresponding direct entry probes rejected before side effects. |
| Existing symlink ancestors are rejected | Root resolution detects symlink redirection into discovery; `_ensure_private_directory()` additionally rejects symlink private-directory ancestry and enforces `0700` (`:1182-1201`). | Existing symlink ancestor into discovery rejected; existing backup-root symlink redirect regression passed. |
| Existing recovery guarantees remain intact | Durable receipts, created-parent binding/cleanup, recovery-blocked state, receipt-history blockers, later-target exclusion, and four-target ordering remain in the corrected paths. | Focused recovery and full cross-CLI suites passed. |

## Adversarial production probes

The corrected isolated probe matrix covered:

- discovery-root equality;
- nested private roots;
- another target’s discovery root;
- relative and normalized paths;
- existing symlink ancestor resolving into discovery;
- backup root and transaction root independently;
- `apply_target`;
- direct `_prepare_target_backup`;
- direct `_target_transaction_lock`;
- `restore_target`;
- `recover_pending`;
- content verification;
- discovery verification;
- `commit_target`;
- `verify_all_receipts`.

Result: `45/45` entry combinations rejected with no unsafe root, receipt, backup, lock, safe-root, or destination side effect.

Safe external roots retained the existing lifecycle: isolated round-trip, crash recovery, recovery-blocked/manual disposition, restore drift handling, and four-target verified ordering all passed. An initial private probe setup error was corrected; it affected only the temporary fixture and no project/runtime bytes.

## Correction history

- Initial source Review: destination namespace/leaf TOCTOU.
- R1: existing-parent identity and receipt displacement.
- R2: initially absent parents, restore cleanup, and post-history receipt rollback ambiguity.
- R3: created-parent logical/path/chain semantic binding.
- R4: those correction branches independently passed.
- Runtime Sync-plan Review: backup and transaction roots were not excluded from Skill discovery roots.
- R5: shared four-root containment guard added and independently exercised above.

The complete prior branches remain coherent: destination and parent identity, missing-parent creation, exact cleanup and rollback ambiguity, receipt history, recovery-blocked handling, later-target isolation, four-target ordering, role-first routing, schema-6/schema-2 identity, legacy isolation, discovery, exclusions, documentation, and shared Router/Companion bytes.

## Fresh validation

- Router quick validator: `Skill is valid!`
- Companion quick validator: `Skill is valid!`
- Router core gates: `Core gates valid`
- Companion template validator: passed
- Router full suite: `215` tests, `OK`
- Companion full suite: `87` tests, `OK`
- Cross-CLI suite: `91` tests, `OK`
- OpenSpec strict change validation: passed
- OpenSpec strict all validation: `3 passed / 0 failed`
- Exact negative searches: clean
- Shared Handoff byte comparison: passed
- Shared validator-core identity tests: `2/2`, passed
- Sensitive path-only audit: `0 sensitive categories found`
- Bound forward routing evidence: `6/6` cases passed
- No project/runtime files were modified.

## Findings

- P0: none.
- P1: none.
- P2: none.
- The source-verification hash difference is an explicitly bound evidence-only append, not a candidate implementation finding.

## Final Verdict

**PASS**

Read-only four-target runtime planning may resume after the bound control-plane accepts and persists this evidence. A fresh plan must be generated before any future apply; the existing reviewed plan is stale after the R5 source change. This Review does not authorize runtime inspection, mutation, promotion, publication, or completion.
