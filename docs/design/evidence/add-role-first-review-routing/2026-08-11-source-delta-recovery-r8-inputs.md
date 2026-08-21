# Source-delta Recovery R8 Preflight Inputs

## Authority and decision boundary

- change: `add-role-first-review-routing`
- phase: Task 6 source-delta recovery amendment R8
- observed date: `2026-08-11`, Asia/Shanghai
- user authorization:
  `批准创建 R8 source-delta recovery amendment：仅将该 pycache 路径纳入精确 allowlist，备份当前字节后删除这一 generated cache；完成独立 Preflight PASS 后方可执行。不得扩展至其他清理、Git、Pi 或 runtime。`
- authority now: create and independently Review the R8 Plan amendment and its
  immutable bindings only
- execution authority before accepted independent `PASS`: none
- execution authority after accepted independent `PASS`: back up and remove
  only the exact cache object through Plan Task 6 Step 5A, then rerun the exact
  Task 6 Step 6 source-delta gate
- explicitly excluded: any other cache/generated cleanup, wildcard or recursive
  deletion, restore, source behavior edit, Git, Pi, runtime sync/apply/restore,
  canonical transition, archive, Envelope, publication, completion, or backup
  cleanup

## Reason for the amendment

Task 6 Steps 3–5 reached fresh PASS on the final source revision. Source-delta
attempt 1 then exposed a preflight-only inventory-schema defect; a realistic
RED and minimal validator fix closed it. Attempt 2 exposed false-positive
directory size changes; a nested allowed-file RED and minimal comparator fix
closed that issue. Both blocked compare roots remain mode `0700`, and neither
attempt created a delta JSON.

After those fixes, the complete comparison reports exactly one unexpected
Router path and zero Companion paths:

`scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc`

The object is generated Python bytecode, but R7 correctly rejected it because
it was outside the exact allowlist. No deletion, replacement, cleanup, reverse
copy, or source-start restore occurred.

## Exact cache binding

| Field | Current reviewed value |
|---|---|
| absolute path | `/Users/elvis/file/develop/opensource/openspec-superpower-change/scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc` |
| kind | regular file; not a symlink |
| current SHA-256 | `5b7cd72df71d308929c08fb6ae047403b4374e1824a13f479e5034f468dfff49` |
| current size | `168579` bytes |
| current mode | `0644` |
| current device | `16777233` |
| current inode | `170846033` |
| current link count | `1` |
| owner/group | `501/20` |
| current mtime/ctime/birth | `2026-08-11T15:12:26+0800` |
| source-start SHA-256 | `425e7753b96e7cca2ad645d9a5385e52532e83dd19540ecb7d11ba3adb768c66` |
| source-start size | `64486` bytes |
| source-start mode | `0644` |

The source-start bytes are historical comparison evidence only. They are not
an authorized restore target. R8 must preserve the exact current SHA before
removing the path.

The source parent and transaction root are on device `16777233`; therefore the
reviewed macOS `renameatx_np(..., RENAME_EXCL)` operation is a same-filesystem
exclusive rename. The source parent is a real mode-`0755` directory. The
transaction root is a real mode-`0700` directory owned by `elvis`.

## R8 transaction contract

The revised Plan Task 6 Step 5A is the only proposed mutation command. It must:

1. wait until the complete R8 Review is persisted and accepted as `PASS`;
2. validate the exact source SHA, size, mode, type, path identity and same-device
   recovery root;
3. create only
   `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/source-delta-recovery-r8`
   as mode `0700`;
4. copy the current source bytes to an exclusive no-follow mode-`0600`
   `backup.pyc`, verify the exact current SHA, and `fsync` the file and directory;
5. persist and `fsync` an exact mode-`0600` `prepared.json` before removal;
6. move only the exact source object to an exclusive `original-object.pyc` with
   `renameatx_np(..., RENAME_EXCL)`, then `fsync` both parent directories;
7. retain both byte copies as mode `0600`, verify source absence, and persist an
   exact mode-`0600` `verified.json`;
8. allow interruption resume only from exact validated transaction states;
   any ambiguity stays preserved and returns `BLOCKED` for a new disposition.

The command has no `unlink`, `remove`, `rmtree`, wildcard, recursive cleanup,
overwrite, cross-target restore, fallback, or automatic cleanup path. Moving
the source object is the only operation that removes it from the source tree.

Before Review and again at this record's final binding, all of the following
remain absent and are not symlinks:

- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/source-delta-recovery-r8`
- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/source-compare-r8`
- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/source-delta-r8.json`
- `docs/design/reviews/2026-08-11-add-role-first-review-routing-source-delta-recovery-r8-review.md`

## Immutable contract and progress bindings

| Artifact | SHA-256 |
|---|---|
| revised Plan R8 | `a761b09cda72a9ca01e9e73c2fab861edb293d57c28b37ab0d90329ecdb42aaa` |
| Proposal | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| Design | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| current Tasks | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| spec delta | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| source verification evidence | `5b014fd0178a7c66a3b328657e1ed3d1d681c73272eb3efee22797ff982f96ad` |
| current durable forward summary | `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |

Tasks remain `24 checked / 17 unchecked / 41 total`. Tasks 6.1 and 6.2
remain incomplete; this amendment does not claim source PASS or authorize the
candidate source High Review.

## Original recovery continuity

| Artifact | SHA-256 | Mode/count |
|---|---|---|
| Router source-start inventory | `7805c4c70512d28b690241073fb134e9f9b7b93ddc0c3f51ea8d320c81ed0151` | `0600`, 323 records |
| Companion source-start inventory | `737f700486279fd3d007ba8a9d6e7c96bfff18273eed41d443b6b44b355d068b` | `0600`, 29 records |
| Router R4 preflight tree | `f5506db159dd77fe5b9401a20a77d9796183f5515c0e20abb466147f8dc3f859` | `0600`, 320 records |
| Companion R4 preflight tree | `cf4924df7707cf665d41de48300eb59ce8097f0ee0dd298fd7039e5db625b064` | `0600`, 29 records |
| Router source backup | `a0b7a36e0964fe8e6b93bbcb24a2454bab1c3376159f7cd55f710054d464c491` | `0600`, 27 members |
| Companion source backup | `3deab7e813efca3de22ff7d583a5ae089eec079c63842239d9adb85191fb4acc` | `0600`, 14 members |

The archives were only listed with `tar -tf`; they were not extracted. They
remain recovery evidence and grant no restore authority.

## R4–R7 Review-history continuity

| Stage | Inputs/prompt/Review SHA-256 | Historical result |
|---|---|---|
| R4 Plan Preflight | `13a2e1a5e1f11517c39bb9fe00e140c6e61884dedc4bf21f1ede6c3cea048f75` / not rebound here / `9fc3aa76e44bd722d8c7fb57f37d2c2e042b244963fc04b4d736fadbd5f8f030` | `PASS` |
| R5 Conda amendment | `fe5c8ef2186b81257be389e30ce297cf5ed3f0d06f93dec5676a91077a79c381` / `b151534cd424493699539608e9e9f2c49abb198d5acb83ce110e0033eb06ace6` / `64eadbe090dc3f50c2201348703c111088358eaf9677a56f3b444e3238a6b1f1` | `BLOCKED` |
| R6 Conda amendment | `a2444d79f6b20841ea55ec71faa481e0cf1b811cf24111e522734eb6b0ea5b23` / `dc3d755b695242d524e0a746911a995f3cdb0232b114ba1b86b1a52d790d28d6` / `b6d41aa854ad8561ca94341408b1d513f43d2fd3ea7b1786d33da4df04339104` | `BLOCKED` |
| R7 Conda amendment | `f565ac3e637c41286a083ad78f9417fe0384e97fae99534ead92e35ac258867c` / `3092db504ca909a69df245229aaef826706832f36bc6e0a4223190c51a5615d5` / `67bf414d43da1678809d1c40892ab0d1fbf16868247dc2584f88c10d3fd0faaa` | `PASS` |

No prior artifact was rewritten or reclassified.

## R8 no-Git allowlist and machine bindings

- allowlist:
  `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/source-delta-allowlist-r8.txt`
- allowlist SHA-256:
  `2fa0f66b563f000eaf4ff933b0e2cecd22706f4906e0b1a70e0593b8dcc0666d`
- mode/count: `0600`, 59 exact unique entries, no wildcard
- R7 preservation: all 55 R7 entries are byte-for-byte present
- exact four additions:
  - `router scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc`
  - `router docs/design/evidence/add-role-first-review-routing/2026-08-11-source-delta-recovery-r8-inputs.md`
  - `router docs/design/evidence/add-role-first-review-routing/2026-08-11-source-delta-recovery-r8-review-prompt.md`
  - `router docs/design/reviews/2026-08-11-add-role-first-review-routing-source-delta-recovery-r8-review.md`
- bindings:
  `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/preflight-source-bindings-r8.json`
- bindings SHA-256:
  `01d92465d4e15fe0174905fceca49b3c2d49a1aba4f6d3dfc9ee78b1d6fcf096`
- bindings mode/schema: `0600` / `1`
- bindings include the exact revised Plan, unchanged R4 backups/preflight
  trees, and 59-entry R8 allowlist; they do not grant restore authority

## R8 partial-source snapshots

The bound snapshots were captured after the final Plan and binding revision.
They exclude the inputs and Review-prompt paths so those two subsequently
created artifacts do not make the immutable snapshot self-referential:

| Repository | Path | SHA-256 | Mode/count/exclusions |
|---|---|---|---|
| Router | `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/router-tree-source-delta-recovery-r8-dispatch.json` | `5de292fd29d5d1edb9cfa099148686f080176a756bbe6c146dac69f966b3ee8b` | `0600`, 338 records; excludes exactly the R8 inputs and prompt paths |
| Companion | `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/companion-tree-source-delta-recovery-r8-dispatch.json` | `c9e67d141f875877da6d0922281d8a65aa4fcb2a9aa1afab32fa5dc3bb4baecf` | `0600`, 29 records; no exclusions |

The earlier R8 preparation, `-final`, `-bound`, `-review`, and `-preflight` snapshots were captured before the
final pre-mutation cache guard was added to the Plan. They remain untouched as
non-authoritative preparation traces and must not be used as Review, restore,
source-start, or final source-delta evidence.

## Independent Review assignment

- review purpose object: revised complete R8 Plan; exact cache identity and
  current-byte backup; exclusive same-filesystem removal; interruption states;
  R8 allowlist/bindings/snapshots; prior evidence continuity; strict authority
  boundary
- review purpose decision: only whether the original bound Codex control plane
  may run Task 6 Step 5A and, only after its exit `0`, rerun Step 6
- reviewer product: `codex`
- reviewer role: `independent-reviewer`
- capability profile: `control-plane-high`
- independence: a new user-opened Codex window, distinct from the R8 amendment
  author, evidence preparer, prior R7 reviewer, and future recovery executor
- result authority: governed R8 source-delta recovery Plan Preflight evidence
  only

The reviewer must not back up, move, delete, restore, clean, or execute the
cache transaction; run source verification/source-delta; or use Git, Pi,
runtime, canonical, archive, publication, Envelope, or completion authority.
