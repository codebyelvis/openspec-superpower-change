# Source-delta Recovery R8 Revision-2 Preflight Inputs

## Authority and revision purpose

- change: `add-role-first-review-routing`
- phase: Task 6 source-delta recovery R8 revision 2
- observed date: `2026-08-12`, Asia/Shanghai
- original user authorization:
  `批准创建 R8 source-delta recovery amendment：仅将该 pycache 路径纳入精确 allowlist，备份当前字节后删除这一 generated cache；完成独立 Preflight PASS 后方可执行。不得扩展至其他清理、Git、Pi 或 runtime。`
- revision-1 Review verdict: `BLOCKED`
- revision-1 Review artifact:
  `docs/design/reviews/2026-08-11-add-role-first-review-routing-source-delta-recovery-r8-review.md`
- revision-1 Review SHA-256:
  `792e64a77a75ea87a4d2c726a5ca88421194fbcb3146609f4b2daca7c767359e`
- revision-2 purpose: close only `R8-P1-01` and `R8-P1-02`, refresh their
  mechanical probe/bindings, and obtain a new independent Preflight verdict
- execution authority before accepted revision-2 `PASS`: none
- unchanged exclusions: other cleanup, wildcard/recursive deletion, restore,
  source behavior edit, Git, Pi, runtime, canonical transition, archive,
  Envelope, publication, completion, or backup cleanup

## Finding closure design

### R8-P1-01 — source parent identity and mode

The Plan now binds the source parent to:

| Field | Expected value |
|---|---|
| path | `/Users/elvis/file/develop/opensource/openspec-superpower-change/scripts/__pycache__` |
| kind | real directory; no symlink |
| mode | `0755` |
| device | `16777233` |
| inode | `163934412` |
| uid/gid | `501/20` |

Before any recovery-root creation, the transaction opens that directory using
`O_DIRECTORY|O_NOFOLLOW`, compares `fstat(fd)` and `lstat(path)` to the exact
binding, and retains the fd through the transaction. Immediately before the
move it revalidates the same fd/path binding. `renameatx_np(RENAME_EXCL)` uses
the retained source-parent fd and the retained recovery-root fd rather than
`AT_FDCWD` or mutable absolute-path resolution.

Any source-parent type/mode/device/inode/owner/path-fd drift is `BLOCKED`
before rename. The exact cache remains separately bound by SHA/size/mode/
device/inode/nlink/uid/gid.

### R8-P1-02 — durable resumed prepared evidence

`require_exact_payload(..., durable=True)` now:

1. opens the existing evidence file with `O_RDWR|O_NOFOLLOW`;
2. requires regular mode `0600` and exact path/fd device+inode identity;
3. reads and compares the exact payload;
4. calls `os.fsync(fd)` while the validated fd is still open;
5. rechecks fd/path identity and file size/mtime stability before closing.

The existing-prepared branch calls that durable path, then `os.fsync()` on the
retained recovery directory fd, strictly before the namespace-consistency check
and `rename_exclusive`. Existing verified evidence uses the same durable helper.
Fresh prepared evidence keeps the original exclusive write/file-fsync/
directory-fsync order.

## Exact cache and namespace pre-state

The exact source cache remains unchanged from revision 1:

| Field | Value |
|---|---|
| path | `/Users/elvis/file/develop/opensource/openspec-superpower-change/scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc` |
| kind/mode | regular, non-symlink, `0644` |
| SHA-256 | `5b7cd72df71d308929c08fb6ae047403b4374e1824a13f479e5034f468dfff49` |
| size | `168579` |
| device/inode/nlink | `16777233 / 170846033 / 1` |
| uid/gid | `501/20` |
| mtime/ctime/birth | `2026-08-11T15:12:26+0800` |

Source-start cache evidence remains SHA
`425e7753b96e7cca2ad645d9a5385e52532e83dd19540ecb7d11ba3adb768c66`,
size `64486`, mode `0644`; it is not a restore target.

At this revision's binding point these remain absent and non-symlink:

- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/source-delta-recovery-r8`
- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/source-compare-r8`
- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/source-delta-r8.json`
- `docs/design/reviews/2026-08-12-add-role-first-review-routing-source-delta-recovery-r8-r2-review.md`

The revision-1 Review path now exists as the exact immutable `BLOCKED` artifact
above; its occupation is expected history, not execution evidence.

## Contract and evidence hashes

| Artifact | SHA-256 |
|---|---|
| revised Plan R8-r2 | `24c17f8d9170f48c201bbbdf0b8624e0d282f47c35f2c61baac53f01b3c4b1f0` |
| Proposal | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| Design | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| current Tasks | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| spec delta | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| source verification | `5b014fd0178a7c66a3b328657e1ed3d1d681c73272eb3efee22797ff982f96ad` |
| durable forward summary | `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |
| R8 revision-1 inputs | `c682a913f0ab2ba098c36913588a8a2c74e4da2408a0588760ebeb1cdbe322cb` |
| R8 revision-1 prompt | `4385533d80174a6e6d657e12e5b30f7c166c06727e1bfa35e4a3ac3fe9a1d89b` |
| R8 revision-1 BLOCKED Review | `792e64a77a75ea87a4d2c726a5ca88421194fbcb3146609f4b2daca7c767359e` |

Tasks remain `24 checked / 17 unchecked / 41 total`; source-delta and candidate
source High Review remain unreleased.

## Recovery and source-start continuity

| Artifact | SHA-256 | Mode/count |
|---|---|---|
| Router source-start | `7805c4c70512d28b690241073fb134e9f9b7b93ddc0c3f51ea8d320c81ed0151` | `0600`, 323 records |
| Companion source-start | `737f700486279fd3d007ba8a9d6e7c96bfff18273eed41d443b6b44b355d068b` | `0600`, 29 records |
| Router R4 preflight tree | `f5506db159dd77fe5b9401a20a77d9796183f5515c0e20abb466147f8dc3f859` | `0600`, 320 records |
| Companion R4 preflight tree | `cf4924df7707cf665d41de48300eb59ce8097f0ee0dd298fd7039e5db625b064` | `0600`, 29 records |
| Router source backup | `a0b7a36e0964fe8e6b93bbcb24a2454bab1c3376159f7cd55f710054d464c491` | `0600`, 27 members |
| Companion source backup | `3deab7e813efca3de22ff7d583a5ae089eec079c63842239d9adb85191fb4acc` | `0600`, 14 members |

The archives were listed only with `tar -tf`; no extraction or restore occurred.

## Revision-2 allowlist and bindings

- R8 revision-1 allowlist: 59 entries, SHA
  `2fa0f66b563f000eaf4ff933b0e2cecd22706f4906e0b1a70e0593b8dcc0666d`
- R8 revision-2 allowlist:
  `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/source-delta-allowlist-r8-r2.txt`
- revision-2 allowlist SHA/count/mode:
  `a53c1d2b8a46f6e4ca8e9b99e8ec6a90f4a27415ef3341760744a7f0e2dc8b26`,
  62 exact unique entries, `0600`, no wildcard
- revision-1 preservation: all 59 entries retained exactly
- exact three additions:
  - `router docs/design/evidence/add-role-first-review-routing/2026-08-12-source-delta-recovery-r8-r2-inputs.md`
  - `router docs/design/evidence/add-role-first-review-routing/2026-08-12-source-delta-recovery-r8-r2-review-prompt.md`
  - `router docs/design/reviews/2026-08-12-add-role-first-review-routing-source-delta-recovery-r8-r2-review.md`
- bindings:
  `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/preflight-source-bindings-r8-r2.json`
- bindings SHA/mode/schema:
  `e6e423c30dee8c3b678e94f74aea67667bb61d6c79b60c099a58632f2cefeba3`,
  `0600`, schema `1`

The bindings point to the revised Plan, unchanged R4 backups/preflight trees,
and the 62-entry allowlist. They grant no restore or cleanup authority.

## Revision-2 partial-source snapshots

| Repository | Path | SHA-256 | Mode/count/exclusions |
|---|---|---|---|
| Router | `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/router-tree-source-delta-recovery-r8-r2-dispatch.json` | `929958fbde3d78ff66282ceb3bdee3b301fae68f400875cf02a8b869d3bb678d` | `0600`, 341 records; excludes exactly revision-2 inputs/prompt |
| Companion | `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/companion-tree-source-delta-recovery-r8-r2-dispatch.json` | `c9e67d141f875877da6d0922281d8a65aa4fcb2a9aa1afab32fa5dc3bb4baecf` | `0600`, 29 records; no exclusions |

The snapshots are read-only partial-source Preflight evidence, not source-start,
restore, source PASS, or final source-delta evidence. All prior R8 preparation
snapshots remain untouched and non-authoritative.

## Independent Review assignment

- purpose object: complete revised R8-r2 Plan, the two revision-1 findings and
  their mechanical closure, exact cache/source-parent identity, durable
  prepared evidence, dirfd-exclusive rename, revised allowlist/bindings/
  snapshots, history continuity and authority boundary
- purpose decision: only whether the original bound Codex control plane may
  execute Task 6 Step 5A, and only after its exit `0`, Task 6 Step 6
- reviewer product: `codex`
- reviewer role: `independent-reviewer`
- capability profile: `control-plane-high`
- independence: a new user-opened Codex window distinct from the amendment
  author, revision-1 reviewer, evidence preparer and future recovery executor
- result authority: governed R8 revision-2 Plan Preflight evidence only

The reviewer must not execute the cache transaction, create its backup, move or
delete the cache, run source-delta, or use cleanup/Git/Pi/runtime/canonical/
archive/publication/completion authority.
