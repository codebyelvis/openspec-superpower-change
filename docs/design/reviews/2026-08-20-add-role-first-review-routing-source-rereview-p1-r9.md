# Source High Review — P1 R9

## Decision

- Verdict: **FAIL**
- P0: none
- P1: five findings
- P2: none
- Read-only runtime planning may resume: **NO**

Review was performed as fresh no-history `codex / independent-reviewer / control-plane-high`, source-evidence authority only. Router and Companion `AGENTS.md`/`SKILL.md` and the complete bound R9 input were read. No project files, runtime destinations, Git, Pi process, plan, or target Review artifact were written. Temporary probe directories were cleaned.

## Binding verification

- R9 input: `0644 / f0d1866ddf9b6b0126166d556f4d96b81e3f63bbe413505342e678d9ef06baa0`
- Approved Plan: `0644 / dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229`
- Prior R5 PASS: `0644 / 073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4`
- Prior R8 FAIL: `0644 / c99d1206f7666d8dbd67c8bc480649b0c1cadabaf75e6a4395e8f1138f31f5ad`
- Current source verification: `0644 / 2e651b24eccfc472ab0cbcd67e2fff2298858c275f5ea3c251bf9223f11ee0f1`
- Durable R9 summary: `0644 / 479ec0c6677195aa1174f60495a398daaf170974aa80e482ac5f74f40fc91ec6`
- Corrected script: `0644 / e847f1c7cc73cd2c4b3fc4cf3ee3bfb8369fd431feb1bdf632f6654ff16d280f`
- Corrected tests: `0644 / d77e19b190a4887b30e954f7c284d43ae3f66d13b3755707fce7986229010c5d`
- Pi prompt: `0644 / 9cba75f75a714110d5efa3a9ff21112f51367a6626e3fdaea596b16544ff04c1`
- Sanitized Pi attempt: `0600 / 2cc4d107db175acce6b66d9439ea8bab191d271695d4f75df4b1302dfa2c255b`
- Authoritative retry delta: `0600 / a16ef355cd8ecfb59fed2dfbfd46e370557c9c3b44373d220744f2b02e62237e`
- R9 bindings: `0600 / a3b48b4cb204204cf0641997b923be5f619080885e06676ca7aec2035a1ddc9d`
- R9 allowlist: `0600 / cceb69b843e569f7c99189346e8ced845862fc8e4421c2c8b46c135e86196fc9`
- Forward summary: `0600 / 1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b`

The intended R9 Review artifact was absent at the start and remains absent. The governed source cache path is also absent.

## Delta classification

The authoritative retry reports `source_delta: pass`, 74 actual paths (`60` Router, `14` Companion), 79 allowlisted paths, and `unexpected_paths: []`. The governed `cpython-314` cache path is deleted relative to baseline. This retry is the valid source candidate.

The first retained delta is non-authoritative and is used only to explain the regenerated cache. However, its declared SHA-256 is `64aca252ecec2b8665a498b2b11d579011c2d4577a69ae786a047567b0336f37`, while the retained file actually hashes to `64aca2527cf0f1e513054ac29ab406958cd1de81cc6206e4176396ddacf73dc4`. This evidence-binding mismatch is recorded as P1 below. The current source-verification hash differs from the retry’s expected pre-append hash by the explicitly permitted evidence-only post-delta append.

## Mechanism and probe trace

| Area | Evidence | Result |
|---|---|---|
| Existing hard-link runtime alias | Focused R9 unit test | PASS: rejected |
| Runtime alias introduced during inventory | Temporary probe swapped runtime to a package hard-link after inventory began | **FAIL: returned PASS; `samefile()` true** |
| Supported real launcher | Private snapshot materialization probe | PASS: private entrypoint snapshot created, mode `0555`, digest matched |
| Nested reviewed-root symlink | Focused R9 unit test/direct probe | PASS: rejected |
| Top-level reviewed-root symlink | `_execute_pi_probe` resolves `raw_root` before digesting | **FAIL: returned PASS** |
| Reviewed content drift | Temporary subprocess-mutation probe | PASS: returned BLOCKED |
| Reviewed regular-file mode drift | Temporary chmod-mutation probe | **FAIL: returned PASS** |
| Collision, rename collision, file/dir fsync, parent drift | Temporary transaction probes | PASS: fail closed, no unrelated overwrite |
| Rollback unlink failure | Public `execute_pi_probe` fault injection | **FAIL: returned BLOCKED but retained PASS artifact** |
| Hidden-candidate cleanup failure | Public persistence fault injection | **FAIL: returned BLOCKED but retained hidden candidate** |
| Native target verification | Focused unit test and source inspection | PASS: no Pi/subprocess call |
| Native-root/network isolation | Sandbox profile inspection | PASS: explicit native read/write denial and `(deny network*)` |
| Sanitized Pi attempt | Bound evidence artifact | BLOCKED, consistent with approved Task-10 limitation |

## Findings

### P1-01 — Runtime identity is not revalidated after inventory

`_probe_exec_contract` captures `runtime_metadata` before `_probe_package_inventory` (`scripts/validate_cross_cli_sync.py:3329-3355`). The inventory checks the old device/inode tuple (`3147-3183`) but does not re-stat the runtime after inventory.

A temporary production-function probe replaced the runtime path with a hard-link to a package file during inventory. `_execute_pi_probe` accepted `PASS`, while the runtime and package file were the same inode. The preexisting-alias regression passes, but the required inventory-timing adversary remains open.

### P1-02 — Top-level reviewed-root symlink bypasses rejection

`_execute_pi_probe` resolves each raw read root at line `3657` before calling `_reviewed_tree_digest`. Consequently, `_reviewed_tree_digest`’s root symlink guard (`3575-3578`) never sees a symlink supplied as the reviewed root itself. A top-level symlink probe returned `PASS`.

### P1-03 — Reviewed-tree digest omits regular-file mode

`_reviewed_tree_digest` records file path and content SHA only (`3589-3592`); file mode is not bound. A temporary probe changed a reviewed file from `0644` to `0600` during the mocked subprocess. The post-run digest matched and the result remained `PASS`.

### P1-04 — Persistence cleanup failures can leave accepted evidence

Normal collision, fsync, parent-drift, and rollback paths clean up correctly. However, `_persist_pi_probe_result` and its public boundary (`3782-3846`) do not guarantee cleanup if guarded unlink itself fails.

Fault injection demonstrated:

- output-directory fsync failure + rollback unlink failure: public result became `BLOCKED`, but the mode-`0600` artifact still contained `PASS`;
- rename collision + hidden-candidate unlink failure: public result became `BLOCKED`, but `.cross-cli-sync.*` remained.

This violates the required no-residual-PASS/no-hidden-candidate transaction guarantee.

### P1-05 — Retained cache-incident delta hash is not reproducible

The retained non-authoritative first delta’s declared SHA does not match the actual retained file SHA. Although the authoritative retry is structurally valid and the cache path is absent now, the retained incident evidence cannot be independently bound exactly as declared.

## R7/R8 and Task 10

The R8 preexisting hard-link, nested symlink, and directory-fsync regressions pass. Package snapshotting, content-drift detection, fixed-schema mode-`0600` persistence on usable paths, native-target no-Pi behavior, and native/network denial rules remain intact in focused checks.

Task 10 remains an approved limitation: a network-backed Pi model requiring native credentials cannot complete until an approved isolated offline/local or temporary non-native route exists. The sandbox must not be relaxed. The sanitized Pi result is correctly `BLOCKED` and is not evidence of a successful adversarial Review.

## Resume conditions

Read-only runtime planning remains blocked until all P1s are corrected, with focused RED/GREEN evidence covering:

1. runtime identity changes before and during inventory;
2. raw top-level reviewed-root symlinks and regular-file mode drift;
3. rollback and hidden-candidate cleanup failures themselves;
4. exact regenerated authoritative delta and retained cache-incident hash bindings;
5. a fresh independent Source High Review returning explicit `PASS`.
