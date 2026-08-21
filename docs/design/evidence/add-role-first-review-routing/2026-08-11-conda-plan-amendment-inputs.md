# add-role-first-review-routing Conda Plan Amendment Inputs

## Boundary

- observed_at: `2026-08-11T15:31:59+0800`, Asia/Shanghai
- mode: approved implementation / mid-execution Plan amendment only
- reason: Task 6 `quick_validate` requires PyYAML; default Python 3.14 lacks it
- source implementation before amendment: Tasks 1–5 recorded complete; Task 6
  remains `BLOCKED`
- conda environment created: `no`
- git command performed: `no`
- Pi command performed: `no`
- runtime/canonical/archive/publication/completion mutation: `no`
- result_authority: amendment input binding only; this record is not Plan
  Preflight PASS, source Review, runtime authorization, or completion evidence

## User decision and blocker history

The user first authorized only a standard user-environment PyYAML installation
for the default `python3`, with an explicit stop condition if the environment
refused it and an explicit prohibition on `--break-system-packages`.

`python3 -m pip install --user PyYAML` returned exit `1` with PEP 668
`externally-managed-environment`. No successful installation occurred,
`--break-system-packages` was not used, and no alternate installer/interpreter
was attempted in that revision. The durable evidence is:

| Artifact | SHA-256 |
|---|---|
| `docs/design/evidence/add-role-first-review-routing/2026-08-10-source-verification.md` | `04857f7fd625b5f6a9b17ff8a9fc2d873eccf95de40fb290e47b44fc75317a88` |

The user then instructed: `python 用我的conda创建`. This amendment interprets
that decision narrowly: create one isolated Conda prefix for the two approved
`quick_validate` commands, while keeping project validators/tests on default
`python3`. It does not authorize use of Conda base, pip, environment activation,
`conda init`, configuration changes, unrelated packages, another channel, or
another interpreter.

## Approved OpenSpec and progress binding

The approved contract is unchanged:

| Artifact | Approved SHA-256 | Current SHA-256 |
|---|---|---|
| `proposal.md` | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` | same |
| `design.md` | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` | same |
| `tasks.md` | `764a5401f7f5ec86348f3bfcabb854b196b26793b1b842b236f3731eafa7ffea` | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| spec delta | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` | same |

The current task ledger has `24` checked and `17` unchecked items. Its changes
are evidence-backed progress only; no contract-bearing task text changed.
Tasks 6.1–8.7 remain unchecked.

## Initial Preflight and source-start continuity

The accepted revision-4 artifacts remain historical and unchanged:

| Artifact | SHA-256 |
|---|---|
| initial Plan Preflight inputs | `13a2e1a5e1f11517c39bb9fe00e140c6e61884dedc4bf21f1ede6c3cea048f75` |
| independent revision-4 Plan Preflight `PASS` | `9fc3aa76e44bd722d8c7fb57f37d2c2e042b244963fc04b4d736fadbd5f8f030` |
| accepted schema-6 RED evidence | `4c3c74eaac76e01fd7a1536a32785b2fd33ae555b4ca1b6f505969fb6375c3ef` |
| Router source-start inventory | `7805c4c70512d28b690241073fb134e9f9b7b93ddc0c3f51ea8d320c81ed0151` |
| Companion source-start inventory | `737f700486279fd3d007ba8a9d6e7c96bfff18273eed41d443b6b44b355d068b` |

Router source-start contains `323` records; Companion contains `29`. Both are
mode `0600`. The Conda amendment does not recapture or relabel the original
pre-implementation boundary.

## Revised Plan binding

| Path | SHA-256 |
|---|---|
| `docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md` | `c7158746403282c1d1800fb98c4cf042677e390aaf6c8aabb9ac46e078308fb2` |

The revision changes only Task 6 verification-environment instructions and the
source-delta binding revision. It adds an exact Conda create command, isolated
paths, permitted package/channel bounds, expected results, and stop conditions.
It leaves schema/runtime/source behavior, the approved OpenSpec contract, and
Tasks 1–5 implementation requirements unchanged.

## Conda binding and absent paths

| Field | Observed value |
|---|---|
| executable | `/opt/anaconda3/bin/conda` |
| kind/mode | regular file / `0755` |
| version | `conda 24.4.0` |
| SHA-256 | `a543f4db6623ff7316d0549c2e5241196499a0d0b3e8d212772eeb2df084c8a3` |
| base | `/opt/anaconda3` |
| environment prefix | `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-quick-validate-r1` |
| isolated HOME | `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-home-r1` |
| isolated package cache | `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-pkgs-r1` |
| isolated temporary root | `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-tmp-r1` |

All four amendment paths were absent and non-symlinks at the observation
boundary. Their parent transaction root is the existing mode-`0700` directory.
No Conda environment has been created. The reviewed create operation must stop
if any path becomes occupied, the executable hash/version drifts, the standard
Conda solve/create fails, or a requested package/channel constraint cannot be
satisfied.

## Recovery inputs and revised source-delta binding

The initial recovery archives and preflight tree baselines remain unchanged:

| Artifact | Mode | Count | SHA-256 |
|---|---:|---:|---|
| Router source backup R4 | `0600` | `27` | `a0b7a36e0964fe8e6b93bbcb24a2454bab1c3376159f7cd55f710054d464c491` |
| Companion source backup | `0600` | `14` | `3deab7e813efca3de22ff7d583a5ae089eec079c63842239d9adb85191fb4acc` |
| Router preflight tree R4 | `0600` | `320` | `f5506db159dd77fe5b9401a20a77d9796183f5515c0e20abb466147f8dc3f859` |
| Companion preflight tree R4 | `0600` | `29` | `cf4924df7707cf665d41de48300eb59ce8097f0ee0dd298fd7039e5db625b064` |

The revised allowlist adds only the implementation Plan and the three exact
Conda-amendment evidence/Review paths needed to keep the later complete no-Git
delta auditable:

| Artifact | Mode | Count | SHA-256 |
|---|---:|---:|---|
| `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/source-delta-allowlist-r5.txt` | `0600` | `49` | `99238be04ccb2f8951a1c7430688bad4d17dd1c1739744794ac3f6f66632e3d9` |
| `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/preflight-source-bindings-r5.json` | `0600` | schema `1` | `c53f714bf9aa6df8147f8ec01f6d41a5e47c4617b39a289130a39d56987ed731` |

The bindings retain the original source backups/preflight baselines and bind
the revised Plan/allowlist. Neither artifact grants restore or source-change
authority.

## Current partial-source snapshot

Fresh mode-`0600` inventories were captured after the final Plan revision. The
Router snapshot explicitly excludes only this amendment input record and its
independent Review prompt because both are finalized after the snapshot; the
Companion snapshot has no exclusions:

| Inventory | Records | SHA-256 |
|---|---:|---|
| `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/router-tree-conda-amendment-r5.json` | `328` | `dc8d1d4ca4d410f5e5bd0d2f7f8d817d3a2d50d8c81d729e564eb357afe04a4e` |
| `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/companion-tree-conda-amendment-r5.json` | `29` | `f4eb4af4c836242eb6cc11311aac4bc89ebf68fb2957ccd515770a4317c31bf9` |

These inventories include hidden files and always exclude each root `.git`
entry. The two explicit Router exclusions are bound individually by the
independent Review prompt. The snapshot is review evidence only, not a
replacement source-start baseline or restore input.

## Amendment stop conditions

- Any revised Plan, amendment input, Conda executable, original recovery input,
  source-start/current snapshot, R5 allowlist, or R5 bindings drift.
- Any reviewed Conda prefix/home/cache/temporary path becomes occupied or linked.
- Conda would write outside the declared prefix, isolated HOME/package cache/
  temporary root,
  or its normal read-only installation files, except for network retrieval from
  the explicit `defaults` channel.
- Conda requires base modification, environment activation, configuration
  changes, pip, `--break-system-packages`, a different channel, another
  executable/interpreter, or an unreviewed package.
- Any amendment Review finding or validator returns `BLOCKED`/`FAIL`.
- Any attempt to use this amendment as source Review, runtime/Pi/Git/canonical/
  archive/publication/completion authority.
