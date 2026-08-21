# Source High Review — P1 R10

## Decision

- Verdict: **FAIL**
- P0: none
- P1: two new persistence findings; R9 persistence finding remains open
- P2: none
- Read-only runtime planning may resume: **NO**

Review performed as fresh no-history `codex / independent-reviewer / control-plane-high`, source-evidence authority only. Router and Companion `AGENTS.md`/`SKILL.md` and the complete R10 input were read. No project files, runtime destinations, Git, Pi process, plan, or target Review artifact were written. All private probe roots were cleaned.

## Binding verification

All required start/end bindings remained unchanged and matched:

- R10 input: `0644 / bbe790f6b6c5a2666bd3f6fad2afeefa0e168976acf119783d50905736254705`
- Approved Plan: `0644 / dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229`
- Prior R5 PASS: `0644 / 073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4`
- Prior R9 FAIL: `0644 / 9d563300e93c63f55cfce321c90712e1e329c0ada45e38270a7ffaa856377fcf`
- Source verification: `0644 / ddd8fad9f32760fa0de02281a191cf31ec606f73adc8474297bd2c47997453be`
- Durable R10 summary: `0644 / c95079e11be22f0f6c6e965ea4984f9c90d703e9e951c0f2144f78d8d0c2bc8c`
- Corrected script: `0644 / 8b9d21ed256b7a2a11dfd40043b2af1e938d9ed50e8b0185a5a174eb5120f77e`
- Corrected tests: `0644 / 146bed95e60c28144095470c1a639f619caa04c8ca14d28d08a245fbf39b8318`
- Pi prompt: `0644 / 9cba75f75a714110d5efa3a9ff21112f51367a6626e3fdaea596b16544ff04c1`
- Sanitized Pi attempt: `0600 / 2cc4d107db175acce6b66d9439ea8bab191d271695d4f75df4b1302dfa2c255b`

The intended R10 Review artifact was absent at start and remains absent.

## Delta classification

The authoritative retry2 delta is:

- SHA-256: `0600 / f6e05c35c620fe2c50e24346d23b76c672ef73703017aaf339bf41071b19c271`
- Compare root: mode `0700`
- `source_delta: "pass"`
- 78 actual changed paths: 64 Router, 14 Companion
- 82 allowlisted paths
- `unexpected_paths: []`
- governed `scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc` deleted relative to baseline

The durable summary’s `source_changes` exactly match the authoritative retry2 record. Evidence-only post-delta artifacts retain their separately bound final hashes.

Retained record classification:

- Initial failed-baseline attempt: rejected before output; compare root retained mode `0700`, empty; non-authoritative.
- Pre-hardening `source-delta-r10.json`: pass structurally, 77 paths, SHA `cab67e501d7f3a524549fb568545759b246c3e878d1a711d5164671674c85371`; non-authoritative.
- Retry1 `source-delta-r10-retry1.json`: pass structurally, 78 paths, SHA `db634968ea2ac0441491aaa921379ceb92342fa25d0e1d172e77cc1a2a540f76`; non-authoritative pre-hardening record.
- Corrected retained first R9 delta independently reproduced exactly: `0600 / 64aca2527cf0f1e513054ac29ab406958cd1de81cc6206e4176396ddacf73dc4`.

## Mechanism and probe trace

| Area | Evidence | Result |
|---|---|---|
| Runtime descriptor binding | `_regular_file_binding` binds device, inode, mode, UID, GID, size, mtime, and content through an `O_NOFOLLOW` descriptor; inventory, snapshot, pre-launch, and post-return checks are present | PASS |
| Preexisting/during-inventory runtime hard-link aliases | Focused tests `test_build_pi_probe_rejects_hard_linked_package_runtime_alias` and `test_build_pi_probe_rejects_runtime_alias_created_during_inventory` | PASS |
| Snapshot runtime substitution | Private probe replaced runtime with a same-content hard-link after package copy; `_materialize_probe_package_snapshot` rejected identity drift | PASS |
| Post-launch runtime substitution | Private probe replaced runtime with a same-content hard-link during mocked launch; result `BLOCKED`, success `False` | PASS |
| Supported launcher/private snapshot | `test_probe_pi_wrapper_allows_its_bound_second_stage`, snapshot/source-drift tests | PASS |
| Raw top-level/nested symlinks | `_absolute_without_symlink_resolution` plus no-follow tree digest; `test_probe_pi_rejects_top_level_reviewed_root_symlink` and nested-symlink test | PASS |
| Root/directory/file mapping, identity, mode, content | Private probes changed root inode/mode, nested-directory inode/mode, file content, and same-content file inode; every result was `BLOCKED` | PASS |
| Native-root and network isolation | Direct profile probe confirmed simultaneous native read deny, native write deny, no corresponding allow, and `(deny network*)`; focused sandbox tests also pass | PASS |
| Existing persistence rollback | Directory-fsync failure and rollback-unlink failure tests; accepted output is removed or rewritten to fixed `BLOCKED` | PASS on covered post-install path |
| Rename collision and persistent candidate cleanup | Focused collision test plus independent quarantine probe; only visible `*.persistence-blocked.*` mode-`0600` BLOCKED evidence survived | PASS on covered post-candidate path |
| Native target verification | `test_native_target_verification_never_invokes_pi_probe` | PASS |
| Sanitized exceptions/output | Setup, launch, and fake isolated-process tests | PASS |
| Test suites | Focused R10 class 23/23; transaction/source-delta tests 33/33; full Router cross-CLI 107/107; Companion 87/87 | PASS |

## Findings

### P1-01 — Candidate-creation failure can leave hidden accepted PASS bytes

Locations:

- `_write_guarded_entry`: `scripts/validate_cross_cli_sync.py:820-838`
- `_write_same_directory_candidate`: `:879-898`
- `_persist_pi_probe_result`: `:3963-4024`

If candidate file `fsync` fails, or the candidate parent guard fails, `_write_guarded_entry` attempts `_guarded_unlink`. When that unlink also fails, the exception escapes before `_write_same_directory_candidate` returns. Therefore `_persist_pi_probe_result` never reaches its candidate cleanup/quarantine `finally` block.

Independent production-function probes injected:

- candidate file `fsync` failure + candidate unlink failure;
- candidate parent-guard failure + candidate unlink failure.

Both returned `BLOCKED`/`False` while leaving a hidden `.cross-cli-sync.<uuid>` mode-`0600` file containing the original `PASS` JSON. This violates the requirement that candidate-creation failure leave neither accepted PASS bytes nor a hidden candidate.

### P1-02 — Output prestate does not bind exact inode; same-content replacement can delete unrelated state

Locations:

- `_capture_guarded_prestate`: `scripts/validate_cross_cli_sync.py:783-801`
- rollback handling in `_persist_pi_probe_result`: `:3988-4006`

The prestate records only `kind`, content SHA-256, and mode. It does not record device/inode. A private probe replaced the installed output with a different inode containing identical PASS bytes before the directory-fsync failure. The persistence code accepted the replacement as equal expected state and unlinked it.

Observed result:

- returned `BLOCKED`, success `False`;
- expected output path absent;
- a hard-link alias to the replacement inode remained with PASS bytes.

This violates the exact-candidate and no-unrelated-state requirement.

## R9 finding disposition

- Runtime identity after inventory: **closed** by descriptor binding and boundary checks.
- Raw top-level reviewed-root symlink: **closed**.
- Reviewed regular-file mode drift: **closed**.
- Persistence cleanup failure: **not closed**; post-install paths are hardened, but P1-01 and P1-02 remain.
- Corrected retained R9 delta hash: **closed**, exact SHA reproduced.

## R7–R9 and Task 10

R7–R9 package alias rejection, raw symlink rejection, snapshot/source drift detection, sanitized output, native-target no-Pi behavior, and native/network isolation remain intact in the reviewed tests and probes.

Task 10 remains an approved limitation: a network-backed model requiring native credentials cannot complete until an approved isolated offline/local or temporary non-native route exists. The sanitized Pi attempt is correctly `BLOCKED`; the sandbox must not be relaxed.

## Resume conditions

Read-only runtime planning must remain blocked until:

1. Candidate-creation exceptions with cleanup failure can leave only explicit visible mode-`0600` fixed-schema `BLOCKED` quarantine, never hidden PASS bytes.
2. Persistence prestate binds exact device/inode and refuses unlink/rewrite when the target inode has changed.
3. RED/GREEN tests cover candidate file/parent failures, unlink failures, same-content inode substitution, rename collision, fsync failures, and quarantine behavior.
4. A regenerated authoritative source delta and bound post-delta evidence pass independently.
5. A fresh independent Source High Review returns explicit `PASS`.
