# Independent Conda Plan Amendment Preflight Review — Revision 6

## 1. Reviewer identity

| Field | Value |
|---|---|
| reviewer product | `codex` |
| reviewer role | `independent-reviewer` |
| capability profile | `control-plane-high` |
| instance/thread ID | `unavailable` |
| independence basis | `user_opened_separate_window` |
| distinct from | R5 reviewer、Plan/amendment author、evidence preparer、source executor、未来 Conda/environment executor |
| review date | `2026-08-11 Asia/Shanghai` |
| review mode | complete、read-only、fail-closed |
| result authority | `governed Conda Plan amendment revision-6 Preflight evidence only` |

使用了 `codex-brief-antigravity-review` 的 standalone read-only Review 路由；它将本次工作限制为 findings/evidence 输出，未修改或推进任何状态。

## 2. Reviewer Assignment Contract

| Contract field | Accepted assignment |
|---|---|
| `review_purpose.object` | revised complete Plan；R5 BLOCKED 与 `F-R5-001` closure；Task 6 Step 2/3 fail-fast；Conda executable/dependency/channel/path/write boundary；R4/R5/R6 continuity；R6 allowlist/bindings；Git/Pi/runtime/canonical/archive/publication/completion authority |
| `review_purpose.decision` | 仅决定原 bound Codex control-plane 能否执行 revised Task 6 Step 2 exact subshell，并在成功后执行 Step 3 |
| `reviewer_product` | `codex` |
| `reviewer_role` | `independent-reviewer` |
| `capability_profile` | `control-plane-high` |
| `independence_requirement` | `user_opened_separate_window`；instance ID `unavailable` |
| `result_authority` | revision-6 Conda Plan amendment Preflight evidence only |
| explicit non-authorizations | Tasks 1–5 重执行/改写、source correctness/PASS/High Review、真实 Pi、runtime、Git、canonical、archive、Envelope、publication、completion、cleanup |

## 3. Scope、complete reads、SHA 与只读命令

### Complete reads

已完整读取用户要求的全部内容：

- Router：`AGENTS.md`、`SKILL.md`、`CONTEXT.md`、`openspec/project.md`、Proposal、Design、Tasks、delta/current specs、完整 R6 Plan、R4 inputs/PASS Review、RED、source blocker、R5 inputs/prompt/BLOCKED Review、R6 inputs、7 个指定 references、`scripts/validate_cross_cli_sync.py`。
- Companion：`AGENTS.md`、`SKILL.md`、`scripts/validate_templates.py`。
- T：R6 bindings、R6 allowlist、Router/Companion source-start、Router/Companion R6 snapshot。
- Backups：仅使用 `tar -tf`，未提取；Router 27 项，Companion 14 项。

### Start/end immutable SHA

所有值在 Review 开始和 verdict 前一致，无 drift：

| Artifact | Start = End SHA-256 |
|---|---|
| Revised Plan R6 | `341a0e7320c436c734b4b29d7992287a70c50bef627607d0dd18fe1a313a66d6` |
| R6 inputs | `a2444d79f6b20841ea55ec71faa481e0cf1b811cf24111e522734eb6b0ea5b23` |
| Proposal | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| Design | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| Tasks | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| Spec delta | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| R4 inputs | `13a2e1a5e1f11517c39bb9fe00e140c6e61884dedc4bf21f1ede6c3cea048f75` |
| R4 PASS Review | `9fc3aa76e44bd722d8c7fb57f37d2c2e042b244963fc04b4d736fadbd5f8f030` |
| RED evidence | `4c3c74eaac76e01fd7a1536a32785b2fd33ae555b4ca1b6f505969fb6375c3ef` |
| Source blocker | `04857f7fd625b5f6a9b17ff8a9fc2d873eccf95de40fb290e47b44fc75317a88` |
| R5 inputs | `fe5c8ef2186b81257be389e30ce297cf5ed3f0d06f93dec5676a91077a79c381` |
| R5 prompt | `b151534cd424493699539608e9e9f2c49abb198d5acb83ce110e0033eb06ace6` |
| R5 BLOCKED Review | `64eadbe090dc3f50c2201348703c111088358eaf9677a56f3b444e3238a6b1f1` |
| Conda executable | `a543f4db6623ff7316d0549c2e5241196499a0d0b3e8d212772eeb2df084c8a3` |
| R6 allowlist | `02bb64585bdc8da44c360307fae28e3a8575b37c93096cd0c5e3ce653ae2c16a` |
| R6 bindings | `14cc54cf0a8c9a8a60347006b55627c65011fda631b6a99e161c00b19f5600e3` |
| Router source-start | `7805c4c70512d28b690241073fb134e9f9b7b93ddc0c3f51ea8d320c81ed0151` |
| Companion source-start | `737f700486279fd3d007ba8a9d6e7c96bfff18273eed41d443b6b44b355d068b` |
| Router R6 snapshot | `3d2b018faa70839c8cb32f4f8c44b8709d4b8581b8e8dbe9ea105159ead60a4d` |
| Companion R6 snapshot | `f4eb4af4c836242eb6cc11311aac4bc89ebf68fb2957ccd515770a4317c31bf9` |
| Router backup | `a0b7a36e0964fe8e6b93bbcb24a2454bab1c3376159f7cd55f710054d464c491` |
| Companion backup | `3deab7e813efca3de22ff7d583a5ae089eec079c63842239d9adb85191fb4acc` |

### Commands and missing evidence

使用了 `wc -l`、`nl -ba`、`sed -n`、`rg`、`rg --files`、`stat`、`readlink`、`shasum -a 256`、`tar -tf`、`command -v`、`/bin/zsh -n`、OpenSpec strict validation 和两个获准 project validators。

未运行 Conda CLI、pip、quick_validate、implementation unittest、forward probe、source-delta、Git、Pi、runtime、cleanup；未创建或修改文件/environment。

存在一次 reviewer-side deviation：尝试对 Router R6 snapshot 使用未列入 allowlist 的 `jq`。表达式因类型错误退出，没有 artifact 内容输出、没有写入，但仍构成 finding `F-R6-002`。

实质 artifact 未缺失；由于该 deviation，缺少一次完全遵守命令 allowlist 的干净独立 Review run。

## 4. Revision-6 summary

R6 的变更范围符合声明：

- OpenSpec Proposal、Design、Tasks、spec delta 哈希未变，Tasks 1–5 未被重写。
- R4/R5 历史未重标或回写，见 `R6 inputs:14`。
- Step 2/3 被包装为 `set -euo pipefail` closed subshell；四组 path guards 已拆成独立顶层 tests，见 `Plan:1005`。
- R6 更新了 Plan hash、52-entry allowlist、bindings 和 partial-source snapshots。
- 但是 R6 对 producer failure propagation 的声明不成立，因此 `F-R5-001` 只部分关闭。

## 5. Findings

### P0

None.

### P1 — `F-R6-001`: command-substitution producer failures仍可被外层 `test` 掩盖

- 状态：actionable/open。
- Exact locations：
  - hash pipeline：`Plan:1020`
  - version command：`Plan:1031`
  - 三个 mode producers：`Plan:1046`
  - immediate-stop claim：`Plan:1067`
  - R6 closure claim：`R6 inputs:43`
- Observed fact：`pipefail` 决定命令替换内部 pipeline 的状态，但 `test "$(producer)" = expected` 这个有命令名的 simple command 最终状态由 `test` 决定。若 producer 输出 expected text 后以 nonzero 退出，外层 `test` 仍可返回 `0`。
- Violated contract：任一 hash/version/mode producer nonzero 必须立即终止，不能被后续成功掩盖。
- Impact：
  - `shasum | awk` nonzero status 可被比较成功掩盖；
  - `conda --version` nonzero status 可被相同版本文本掩盖；
  - 三个 `stat` producer 存在同类状态传播缺口；
  - Step 2 仍不具备“任一 nonzero 立即停止”的机械保证。
- Minimum correction：
  - 将 hash pipeline 先放入独立 assignment-only simple command，再单独 `test`；
  - version 同样先独立捕获，再单独 `test`；
  - 三个 mode 值也分别独立捕获，再比较；
  - 保留当前 subshell、path guards、create 和无 fallback/cleanup 规则。
- Owner：Plan amendment author / bound control-plane。
- Release condition：修正 Plan，刷新全部派生 hashes、allowlist、bindings、snapshots、inputs/prompt，并通过新的独立 Preflight。
- Re-review：required。

### P2 — `F-R6-002`: reviewer command allowlist deviation

- 状态：actionable/open。
- Exact location：本次 reviewer command log；对 `T/router-tree-conda-amendment-r6.json` 的一次 `jq -r ...` 尝试。
- Observed fact：命令因类型错误退出；无 artifact 内容输出、无写入，但 `jq` 不在显式允许命令清单。
- Violated contract：strict read-only review 的 command allowlist。
- Impact：本次 run 不能成为可授权执行的干净 `PASS` evidence。
- Minimum correction：修正 Plan 后，由新的独立窗口仅使用获准命令重新执行完整 Preflight。
- Owner：independent reviewer / bound control-plane。
- Release condition：新的 compliant independent Review 完成。
- Re-review：required。

除 `F-R6-002` 外无其他 P2。

### Observations

- `OBS-R6-001`：四项 project/OpenSpec validation 全部成功，但不检查 shell 状态传播，也不证明 Conda create、quick/unit/source/runtime。Non-blocking reason：它本身没有失败，只是证明范围有限。Owner：control-plane。Release condition：只能在新的 Plan Preflight PASS 后，按 Task 6 Step 2/3 产生真实执行证据。
- `OBS-R6-002`：instance/thread ID 为 `unavailable`。Non-blocking reason：assignment 明确允许与 `user_opened_separate_window` 配对。Owner：user/control-plane。Release condition：若平台以后暴露 ID，则在后续 Review 绑定；当前不是单独 blocker。

## 6. `F-R5-001` closure matrix

| Requirement | R6 result | Evidence |
|---|---|---|
| Step 2 closed subshell | PASS | Plan 1011、1057 |
| First two lines `(` / `set -euo pipefail` | PASS | Plan 1011–1012 |
| Four independent `! -e` / `! -L` guard pairs | PASS | Plan 1022–1029 |
| No `&&`/`||` guard-list exemption | PASS | Plan 1022–1029 |
| `mkdir` standalone/fail-fast | PASS | Plan 1030 |
| `conda create` standalone/fail-fast | PASS | Plan 1035–1043 |
| Python/PyYAML assertion standalone | PASS | Plan 1049–1056 |
| Hash producer nonzero always propagates | FAIL | Plan 1020–1021 |
| Version producer nonzero always propagates | FAIL | Plan 1031–1033 |
| Mode producer nonzero always propagates | FAIL | Plan 1046–1048 |
| Step 3 closed fail-fast subshell | PASS | Plan 1078–1088 |
| No fallback/automatic cleanup | PASS | Plan 1067–1071 |
| Overall closure | **OPEN** | `F-R6-001` |

## 7. Task 6 Step 2/3 fail-fast command matrix

| Command/group | Top-level required command | First nonzero guaranteed to stop? | Result |
|---|---:|---:|---|
| `umask 077` | yes | yes | PASS |
| hash `shasum \| awk` inside `test "$(…)"` | producer no | no, producer status can be swallowed | FAIL |
| 8 path tests | yes | yes | PASS |
| `mkdir -m 0700` | yes | yes | PASS |
| `conda --version` inside `test "$(…)"` | producer no | no, producer status can be swallowed | FAIL |
| `conda create` | yes | yes | PASS |
| executable assertion | yes | yes | PASS |
| 3 `stat` calls inside `test "$(…)"` | producers no | not mechanically for every producer nonzero | FAIL |
| Python/PyYAML here-doc assertion | yes | yes | PASS |
| Step 2 fallback/automatic cleanup | absent | — | PASS |
| Step 3 commands 1–8 | all yes | yes, ordered stop at first nonzero | PASS |
| Step 3 implicit recreate/substitution | absent | — | PASS |

因此仍存在早期 producer failure 被后续成功掩盖的路径。

## 8. Conda isolation matrix

| Boundary | Result | Evidence |
|---|---|---|
| Executable | PASS | `/opt/anaconda3/bin/conda`, regular file, mode `0755`, size `515` |
| Executable SHA | PASS | `a543f4db...c8a3` |
| Version binding | PARTIAL | expected `conda 24.4.0`，但 producer status propagation FAIL |
| Prefix | PASS | verdict 前 absent/non-symlink |
| Isolated HOME | PASS | verdict 前 absent/non-symlink |
| Package cache | PASS | verdict 前 absent/non-symlink |
| TMPDIR | PASS | verdict 前 absent/non-symlink |
| Transaction root | PASS | real directory、mode `0700` |
| Plugins | PASS | `CONDA_NO_PLUGINS=true` |
| Solver | PASS | `--solver classic` |
| Channels | PASS | `--override-channels --channel defaults` |
| Default packages | PASS | `--no-default-packages` |
| Python | PASS | create contract `python=3.11`，post-check exact 3.11 |
| PyYAML | PASS | `pyyaml>=6,<7`，post-check major 6 |
| Declared writes | PASS | prefix、isolated HOME、package cache、TMPDIR |
| Activation/init/config/base/pip | PASS | explicitly forbidden |
| Fallback/automatic cleanup | PASS | explicitly forbidden |

## 9. R4/R5/R6 continuity matrix

| Item | Result |
|---|---|
| R4 inputs/PASS Review | hashes unchanged；historical meaning preserved |
| Router/Companion source-start | `323/29` records；hashes unchanged |
| Router backup | mode `0600`、27 entries、hash unchanged；仅 `tar -tf` |
| Companion backup | mode `0600`、14 entries、hash unchanged；仅 `tar -tf` |
| R5 BLOCKED Review | immutable hash unchanged；`F-R5-001` history retained |
| R6 allowlist | mode `0600`；52 lines；unique；无 wildcard |
| R5 preservation | original 49 entries preserved |
| R6 additions | only R6 inputs、R6 prompt、R6 Review 三项 |
| R6 bindings | schema `1`；绑定 current Plan SHA、52-entry allowlist、R4 backups/baselines |
| Router R6 snapshot | mode `0600`、331 records、hash unchanged；仅排除 R6 inputs/prompt |
| Companion R6 snapshot | mode `0600`、29 records、无 exclusions |
| Snapshot meaning | partial-source Review evidence；不是 source-start 或 restore input |
| Restore authority | none |
| Historical rewrite/recovery extraction | none |

## 10. Authority matrix

| Action | Authority from this Review |
|---|---|
| Task 6 Step 2 exact subshell | **not authorized** |
| Task 6 Step 3 | **not authorized** |
| Tasks 1–5 rerun/rewrite | none |
| Source PASS/High Review | none |
| Pi/runtime | none |
| Git/canonical transition | none |
| Archive/Envelope/publication | none |
| Completion | none |
| Cleanup/environment deletion | none |
| Persist this Review as BLOCKED evidence | original bound control-plane only |

## 11. Validation/parse results

| Validation | Exit/result |
|---|---|
| Step 2 exact lines 1011–1057 → `/bin/zsh -n` | exit `0` |
| Step 3 exact lines 1078–1088 → `/bin/zsh -n` | exit `0` |
| `openspec validate add-role-first-review-routing --strict` | exit `0`；valid |
| `openspec validate --all --strict --no-interactive` | exit `0`；`3 passed, 0 failed` |
| Router `validate_core_gates.py .` | exit `0`；Core gates valid |
| Companion `validate_templates.py .` | exit `0`；Validation succeeded |
| Conda create/quick/unit/source/runtime | not run；not proven |

## 12. Verdict

`BLOCKED`

## 13. Exact next action

把本完整 Review 返回原 bound Codex control-plane；不得运行 Task 6 Step 2 或创建 environment。

最小 correction set：

1. 在 Plan 1020–1021、1031–1033、1046–1048 将 producer 与比较拆开：先用独立 assignment-only command 捕获 SHA/version/mode，再用独立 `test` 比较，使 producer nonzero 在 `set -euo pipefail` 下直接终止。
2. 不改 Tasks 1–5、OpenSpec contract、source behavior、Step 3 顺序或既有 isolation/fallback/cleanup 边界。
3. 保持 R4/R5/R6 历史 immutable，创建下一 revision 的 inputs、prompt、allowlist、bindings 和 partial-source snapshots。
4. 用户再开一个独立 Codex 窗口，仅使用明确允许的命令执行完整 Preflight。
5. 只有新的独立 Review 返回 `PASS` 后，原 control-plane 才可先运行修订 Plan Task 6 Step 2 exact subshell；成功后再运行 Step 3 exact subshell。
