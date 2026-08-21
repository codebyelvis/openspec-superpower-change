# add-role-first-review-routing Conda Plan Amendment R6 Inputs

## Boundary

- observed_at: `2026-08-11`, Asia/Shanghai
- mode: approved implementation / same-finding Plan correction only
- finding addressed: `F-R5-001`
- source implementation before correction: Tasks 1–5 recorded complete; Task 6
  remains `BLOCKED`
- Conda environment created: `no`
- Git/Pi/runtime/canonical/archive/publication/completion mutation: `no`
- result authority: revision-6 Preflight input binding only

## Historical chain

The revision-4 Plan Preflight, source-start inventories, backups, revision-5
inputs/prompt/snapshots, and revision-5 `BLOCKED` Review remain unchanged and
retain their historical meaning. This record does not rewrite or relabel them.

| Artifact | SHA-256 | Meaning |
|---|---|---|
| initial R4 Preflight inputs | `13a2e1a5e1f11517c39bb9fe00e140c6e61884dedc4bf21f1ede6c3cea048f75` | initial source boundary |
| initial R4 Preflight Review | `9fc3aa76e44bd722d8c7fb57f37d2c2e042b244963fc04b4d736fadbd5f8f030` | historical source-execution PASS |
| Router source-start | `7805c4c70512d28b690241073fb134e9f9b7b93ddc0c3f51ea8d320c81ed0151` | 323-record baseline |
| Companion source-start | `737f700486279fd3d007ba8a9d6e7c96bfff18273eed41d443b6b44b355d068b` | 29-record baseline |
| R5 amendment inputs | `fe5c8ef2186b81257be389e30ce297cf5ed3f0d06f93dec5676a91077a79c381` | historical R5 input |
| R5 amendment prompt | `b151534cd424493699539608e9e9f2c49abb198d5acb83ce110e0033eb06ace6` | historical R5 assignment |
| R5 BLOCKED Review | `64eadbe090dc3f50c2201348703c111088358eaf9677a56f3b444e3238a6b1f1` | `F-R5-001` evidence |
| source blocker evidence | `04857f7fd625b5f6a9b17ff8a9fc2d873eccf95de40fb290e47b44fc75317a88` | default Python/PyYAML blocker |

## Finding evaluation and exact correction

`F-R5-001` was accepted as technically valid. In revision 5, a failed hash,
path, version, `conda create`, or post-create assertion could be followed by
later commands because the exact shell block had no fail-fast boundary.

Revision 6 changes only the implementation Plan:

1. Task 6 Step 2 is one closed subshell beginning with
   `set -euo pipefail`.
2. Each of the four absent/non-symlink guards is split into two independent
   top-level `test` commands.
3. Hash, path, directory creation, isolated version check, `conda create`, mode,
   executable, Python, and PyYAML checks stop at their first nonzero result.
4. Task 6 Step 3 is also one `set -euo pipefail` subshell, so its eight
   verification commands stop at the first nonzero result.
5. Failure authorizes no fallback or automatic cleanup.

Supporting parse/shape evidence ran without executing the blocks:

- `/bin/zsh -n` accepted both extracted subshells;
- both blocks begin with `(` then `set -euo pipefail` and end with `)`;
- all four absent/symlink guard pairs are separate commands.

## Approved contract and progress

The approved contract is unchanged:

| Artifact | Approved/current SHA-256 |
|---|---|
| Proposal | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| Design | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| Spec delta | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| Current task progress | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |

Tasks remain `24 checked / 17 unchecked`; Tasks 6.1–8.7 remain incomplete.

## Revised Plan and Conda binding

| Item | Binding |
|---|---|
| revised Plan SHA-256 | `341a0e7320c436c734b4b29d7992287a70c50bef627607d0dd18fe1a313a66d6` |
| Conda executable | `/opt/anaconda3/bin/conda` |
| Conda executable SHA-256 | `a543f4db6623ff7316d0549c2e5241196499a0d0b3e8d212772eeb2df084c8a3` |
| reviewed version | `conda 24.4.0` |
| environment prefix | `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-quick-validate-r1` |
| isolated HOME | `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-home-r1` |
| isolated package cache | `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-pkgs-r1` |
| isolated TMPDIR | `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-tmp-r1` |

All four Conda paths remain absent and non-symlinks. Their parent transaction
root remains a real mode-`0700` directory. No environment has been created.

The create contract remains: isolated HOME/package cache/TMPDIR, plugins
disabled, classic solver, `--override-channels --channel defaults`,
`--no-default-packages`, Python 3.11, PyYAML 6.x, no activation/init/config/base
modification/pip/fallback.

## Recovery and R6 source-delta bindings

Original recovery artifacts remain unchanged:

| Artifact | Mode/count | SHA-256 |
|---|---|---|
| Router source backup R4 | `0600` / 27 | `a0b7a36e0964fe8e6b93bbcb24a2454bab1c3376159f7cd55f710054d464c491` |
| Companion source backup | `0600` / 14 | `3deab7e813efca3de22ff7d583a5ae089eec079c63842239d9adb85191fb4acc` |
| Router preflight tree R4 | `0600` / 320 | `f5506db159dd77fe5b9401a20a77d9796183f5515c0e20abb466147f8dc3f859` |
| Companion preflight tree R4 | `0600` / 29 | `cf4924df7707cf665d41de48300eb59ce8097f0ee0dd298fd7039e5db625b064` |

R6 adds exactly three new evidence/Review paths to the complete R5 allowlist:

| Artifact | Mode/count | SHA-256 |
|---|---|---|
| `source-delta-allowlist-r6.txt` | `0600` / 52 | `02bb64585bdc8da44c360307fae28e3a8575b37c93096cd0c5e3ce653ae2c16a` |
| `preflight-source-bindings-r6.json` | `0600` / schema 1 | `14cc54cf0a8c9a8a60347006b55627c65011fda631b6a99e161c00b19f5600e3` |

The bindings retain the R4 backups/preflight baselines and bind the revised
Plan and 52-entry R6 allowlist. They grant no restore authority.

## Current partial-source snapshot

Fresh review-only mode-`0600` inventories were captured after the revised Plan
and persisted R5 Review. The Router snapshot excludes only this R6 input record
and the R6 Review prompt, which are finalized afterward. Companion has no
exclusions.

| Inventory | Records | SHA-256 |
|---|---:|---|
| `router-tree-conda-amendment-r6.json` | 331 | `3d2b018faa70839c8cb32f4f8c44b8709d4b8581b8e8dbe9ea105159ead60a4d` |
| `companion-tree-conda-amendment-r6.json` | 29 | `f4eb4af4c836242eb6cc11311aac4bc89ebf68fb2957ccd515770a4317c31bf9` |

These are partial-source Review evidence, not replacement source-start
baselines or restore inputs.

## Stop conditions

- Any R4/R5 historical input, revised Plan, R6 input/binding/allowlist/snapshot,
  Conda executable, backup, or source-start hash drift.
- Any Conda path becomes occupied or linked.
- Either Task 6 subshell lacks exact fail-fast shape or fails parse review.
- Conda requires a fallback, automatic cleanup, new channel/package,
  interpreter substitution, base/config/user-state mutation, or external write.
- Any required validator or fresh independent Review returns `BLOCKED`/`FAIL`.
- Any attempt to treat this amendment as source correctness/Review, runtime,
  Pi, Git, canonical, archive, publication, completion, or cleanup authority.
