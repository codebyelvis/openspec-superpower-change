# add-role-first-review-routing Conda Plan Amendment R7 Inputs

## Boundary

- observed_at: `2026-08-11`, Asia/Shanghai
- mode: approved implementation / same-finding Plan correction only
- findings addressed: `F-R6-001`, with a fresh clean Review required to release
  reviewer-side `F-R6-002`
- source implementation before correction: Tasks 1–5 recorded complete; Task 6
  remains `BLOCKED`
- Conda environment created: `no`
- Git/Pi/runtime/canonical/archive/publication/completion mutation: `no`
- result authority: revision-7 Preflight input binding only

## Historical chain

The revision-4 Plan Preflight, source-start inventories, backups, revision-5
and revision-6 inputs/prompts/snapshots/Reviews remain unchanged and retain
their historical meaning. This record does not rewrite or relabel them.

| Artifact | SHA-256 | Meaning |
|---|---|---|
| initial R4 Preflight inputs | `13a2e1a5e1f11517c39bb9fe00e140c6e61884dedc4bf21f1ede6c3cea048f75` | initial source boundary |
| initial R4 Preflight Review | `9fc3aa76e44bd722d8c7fb57f37d2c2e042b244963fc04b4d736fadbd5f8f030` | historical source-execution PASS |
| Router source-start | `7805c4c70512d28b690241073fb134e9f9b7b93ddc0c3f51ea8d320c81ed0151` | 323-record baseline |
| Companion source-start | `737f700486279fd3d007ba8a9d6e7c96bfff18273eed41d443b6b44b355d068b` | 29-record baseline |
| R5 amendment inputs | `fe5c8ef2186b81257be389e30ce297cf5ed3f0d06f93dec5676a91077a79c381` | historical R5 input |
| R5 amendment prompt | `b151534cd424493699539608e9e9f2c49abb198d5acb83ce110e0033eb06ace6` | historical R5 assignment |
| R5 BLOCKED Review | `64eadbe090dc3f50c2201348703c111088358eaf9677a56f3b444e3238a6b1f1` | `F-R5-001` evidence |
| R6 amendment inputs | `a2444d79f6b20841ea55ec71faa481e0cf1b811cf24111e522734eb6b0ea5b23` | historical R6 input |
| R6 amendment prompt | `dc3d755b695242d524e0a746911a995f3cdb0232b114ba1b86b1a52d790d28d6` | historical R6 assignment |
| R6 BLOCKED Review | `b6d41aa854ad8561ca94341408b1d513f43d2fd3ea7b1786d33da4df04339104` | `F-R6-001` and `F-R6-002` evidence |
| source blocker evidence | `04857f7fd625b5f6a9b17ff8a9fc2d873eccf95de40fb290e47b44fc75317a88` | default Python/PyYAML blocker |

## Finding evaluation and exact correction

`F-R6-001` was accepted as technically valid. A command substitution inside
`test "$(producer)" = expected` does not make the producer a top-level required
simple command. If the producer emits expected text and then returns nonzero,
the outer `test` may still return zero and mask that failure.

Revision 7 changes only the implementation Plan and its derived bindings:

1. The SHA pipeline is captured by the assignment-only command
   `ROLE_CONDA_SHA="$(...)"`, followed by a separate `test`.
2. The Conda version is captured by the assignment-only command
   `ROLE_CONDA_VERSION="$(...)"`, followed by a separate `test`.
3. Each of the HOME/package-cache/TMPDIR modes is captured by its own
   assignment-only command, followed by a separate `test`.
4. The existing closed `set -euo pipefail` subshell, eight separate path guards,
   `conda create`, Step 3 command order, isolation rules, and no-fallback/
   no-automatic-cleanup boundary remain unchanged.
5. R7 source-delta paths bind the R7 Plan and R7 allowlist; no source behavior
   is added or changed.

Supporting evidence ran without executing the Plan's Conda or verification
commands:

- `/bin/zsh -n` accepted the exact extracted Step 2 and Step 3 blocks;
- static shape check found exactly five assignment-only producers and five
  separate comparisons, with no remaining `test "$(shasum...)"`,
  `test "$(... --version)"`, or `test "$(stat...)"` form;
- an in-memory `/bin/zsh` adversarial probe made a producer output the expected
  value and then exit `7`; both a single producer and a `pipefail` pipeline
  terminated at the assignment with exit `7` and never reached the comparison
  or later command.

`F-R6-002` requires no artifact correction. It is released only by a new
independent Review instance that uses the exact R7 command allowlist and does
not invoke `jq` or another unlisted command.

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
| revised Plan SHA-256 | `3a6169b892151a29d7cfa1ce96798e15c659327c6db34fc1e054d65c6ed39a80` |
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

## Recovery and R7 source-delta bindings

Original recovery artifacts remain unchanged:

| Artifact | Mode/count | SHA-256 |
|---|---|---|
| Router source backup R4 | `0600` / 27 | `a0b7a36e0964fe8e6b93bbcb24a2454bab1c3376159f7cd55f710054d464c491` |
| Companion source backup | `0600` / 14 | `3deab7e813efca3de22ff7d583a5ae089eec079c63842239d9adb85191fb4acc` |
| Router preflight tree R4 | `0600` / 320 | `f5506db159dd77fe5b9401a20a77d9796183f5515c0e20abb466147f8dc3f859` |
| Companion preflight tree R4 | `0600` / 29 | `cf4924df7707cf665d41de48300eb59ce8097f0ee0dd298fd7039e5db625b064` |

R7 adds exactly three new evidence/Review paths to the complete R6 allowlist:

| Artifact | Mode/count | SHA-256 |
|---|---|---|
| `source-delta-allowlist-r7.txt` | `0600` / 55 | `6a0b0f27bcc61af2249e4d219fa8afb75f01ba67b8259c3c6cac32628acd61f0` |
| `preflight-source-bindings-r7.json` | `0600` / schema 1 | `9d740c6a594de2f0b431ea815d870038b09be16b06506f10fd5ee5d5f95a3f0b` |

The bindings retain the R4 backups/preflight baselines and bind the revised
Plan and 55-entry R7 allowlist. They grant no restore authority.

## Current partial-source snapshot

Fresh review-only mode-`0600` inventories were captured after the revised Plan
and persisted R6 Review. The Router snapshot excludes only this R7 input record
and the R7 Review prompt, which are finalized afterward. Companion has no
exclusions.

| Inventory | Records | SHA-256 |
|---|---:|---|
| `router-tree-conda-amendment-r7.json` | 334 | `db498b0b1cbb0d9bd4daffee77a25acf8a3b572a63238be18bc40835a037a857` |
| `companion-tree-conda-amendment-r7.json` | 29 | `f4eb4af4c836242eb6cc11311aac4bc89ebf68fb2957ccd515770a4317c31bf9` |

These are partial-source Review evidence, not replacement source-start
baselines or restore inputs.

## Stop conditions

- Any R4/R5/R6 historical input, revised Plan, R7 input/binding/allowlist/
  snapshot, Conda executable, backup, or source-start hash drift.
- Any Conda path becomes occupied or linked.
- Either Task 6 subshell lacks exact fail-fast shape, fails parse review, or a
  producer nonzero can be hidden by its comparison.
- The new reviewer invokes `jq`, Conda, pip, quick validation, unit tests,
  forward probes, source-delta, Git, Pi, runtime, cleanup, or another command
  outside the exact Review allowlist.
- Conda requires a fallback, automatic cleanup, new channel/package,
  interpreter substitution, base/config/user-state mutation, or external write.
- Any required validator or fresh independent Review returns `BLOCKED`/`FAIL`.
- Any attempt to treat this amendment as source correctness/Review, runtime,
  Pi, Git, canonical, archive, publication, completion, or cleanup authority.
