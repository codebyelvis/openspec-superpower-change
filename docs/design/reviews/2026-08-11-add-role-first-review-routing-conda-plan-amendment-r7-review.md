# Independent Conda Plan Amendment Preflight Review — Revision 7

结论：**PASS**。F-R6-001 与 F-R6-002 均已关闭；本结论只释放原 bound Codex control-plane 对 Task 6 Step 2 exact subshell 的执行，Step 2 成功后才可执行 Step 3。

## 1. Reviewer identity

- `reviewer_product`: `codex`
- `reviewer_role`: `independent-reviewer`
- `capability_profile`: `control-plane-high`
- `instance/thread ID`: `unavailable`
- `independence_basis`: `user_opened_separate_window`
- 独立性声明：本 reviewer 不是 R5/R6 reviewer、Plan/amendment author、evidence preparer、source executor，也不担任后续 Conda/environment executor。
- Review 日期：2026-08-11，Asia/Shanghai。
- 使用 `codex-brief-antigravity-review` 的 Standalone Lightweight Review 路径；该路径使本次工作保持 findings-first、只读且不取得 implementation/completion authority。

## 2. Reviewer Assignment Contract

| 字段 | 本次绑定 |
|---|---|
| Object | Revised complete Plan R7；R6 BLOCKED 与 F-R6-001/F-R6-002 closure；Task 6 Step 2 producer status propagation；Step 2/3 fail-fast；Conda executable/dependency/channel/path/write boundary；R4/R5/R6/R7 连续性；allowlist/bindings；Git/Pi/runtime/canonical/archive/publication/completion authority |
| Decision | 仅判断原 bound Codex control-plane 是否可执行 Task 6 Step 2 exact Conda subshell，并在成功后执行 Step 3 exact subshell |
| Reviewer product/role | `codex` / `independent-reviewer` |
| Result authority | Governed Conda Plan amendment revision-7 Preflight evidence only |
| 非授权项 | Tasks 1–5 重执行/改写、source correctness/PASS/High Review、真实 Pi、runtime、Git、canonical、archive、Envelope、publication、completion、cleanup |

合同来源同时受 `Design:309`、`R7 inputs:5` 和 `Plan:35` 约束。

## 3. Scope、complete reads、SHA、命令与 missing evidence

### Complete reads

已完整读取 Router 要求的 29 项：

- `AGENTS.md`、`SKILL.md`、`CONTEXT.md`、`openspec/project.md`
- change proposal、design、tasks、delta spec、current canonical spec
- Revised Plan R7
- R4 inputs/PASS Review、RED evidence、source blocker
- R5 inputs/prompt/BLOCKED Review
- R6 inputs/prompt/BLOCKED Review
- R7 inputs
- 七个指定 references
- `scripts/validate_cross_cli_sync.py`

已完整读取 Companion 的：

- `AGENTS.md`
- `SKILL.md`
- `scripts/validate_templates.py`

已完整读取 T 下六个绑定文件：

- `preflight-source-bindings-r7.json`
- `source-delta-allowlist-r7.txt`
- Router/Companion source-start JSON
- Router/Companion R7 snapshot JSON

两个 backup 仅执行 path/mode/SHA/`tar -tf`，未提取。Router backup 为 27 entries；Companion backup 为 14 entries。

### Start/end immutable SHA

以下全部 `start = end = expected`：

| Input | SHA-256 |
|---|---|
| Revised Plan R7 | `3a6169b892151a29d7cfa1ce96798e15c659327c6db34fc1e054d65c6ed39a80` |
| R7 amendment inputs | `f565ac3e637c41286a083ad78f9417fe0384e97fae99534ead92e35ac258867c` |
| Proposal | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| Design | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| Current tasks | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| Spec delta | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| R4 inputs | `13a2e1a5e1f11517c39bb9fe00e140c6e61884dedc4bf21f1ede6c3cea048f75` |
| R4 PASS Review | `9fc3aa76e44bd722d8c7fb57f37d2c2e042b244963fc04b4d736fadbd5f8f030` |
| RED evidence | `4c3c74eaac76e01fd7a1536a32785b2fd33ae555b4ca1b6f505969fb6375c3ef` |
| Source blocker | `04857f7fd625b5f6a9b17ff8a9fc2d873eccf95de40fb290e47b44fc75317a88` |
| R5 inputs | `fe5c8ef2186b81257be389e30ce297cf5ed3f0d06f93dec5676a91077a79c381` |
| R5 prompt | `b151534cd424493699539608e9e9f2c49abb198d5acb83ce110e0033eb06ace6` |
| R5 BLOCKED Review | `64eadbe090dc3f50c2201348703c111088358eaf9677a56f3b444e3238a6b1f1` |
| R6 inputs | `a2444d79f6b20841ea55ec71faa481e0cf1b811cf24111e522734eb6b0ea5b23` |
| R6 prompt | `dc3d755b695242d524e0a746911a995f3cdb0232b114ba1b86b1a52d790d28d6` |
| R6 BLOCKED Review | `b6d41aa854ad8561ca94341408b1d513f43d2fd3ea7b1786d33da4df04339104` |
| Conda executable | `a543f4db6623ff7316d0549c2e5241196499a0d0b3e8d212772eeb2df084c8a3` |
| R7 allowlist | `6a0b0f27bcc61af2249e4d219fa8afb75f01ba67b8259c3c6cac32628acd61f0` |
| R7 bindings | `9d740c6a594de2f0b431ea815d870038b09be16b06506f10fd5ee5d5f95a3f0b` |
| Router source-start | `7805c4c70512d28b690241073fb134e9f9b7b93ddc0c3f51ea8d320c81ed0151` |
| Companion source-start | `737f700486279fd3d007ba8a9d6e7c96bfff18273eed41d443b6b44b355d068b` |
| Router R7 snapshot | `db498b0b1cbb0d9bd4daffee77a25acf8a3b572a63238be18bc40835a037a857` |
| Companion R7 snapshot | `f4eb4af4c836242eb6cc11311aac4bc89ebf68fb2957ccd515770a4317c31bf9` |
| Router backup | `a0b7a36e0964fe8e6b93bbcb24a2454bab1c3376159f7cd55f710054d464c491` |
| Companion backup | `3deab7e813efca3de22ff7d583a5ae089eec079c63842239d9adb85191fb4acc` |

### Read-only command compliance

实际使用的命令族仅有：

- `wc -l`
- `sed -n`
- `nl -ba`
- `rg`
- `stat`
- `readlink`
- `shasum -a 256`
- `tar -tf`
- 提示词给定的 exact Probe A、Probe B
- 四条指定 OpenSpec 命令
- 两条带 `PYTHONDONTWRITEBYTECODE=1` 的 project validator

未运行 `jq`、Conda CLI、pip、Git、Pi、quick_validate、implementation unittest、forward probe、source-delta、runtime 或 cleanup。Probe A 内部的 `/bin/zsh` 与 `/usr/bin/awk` 是提示词明确授权的 exact adversarial probe 组成部分，不是额外 reviewer 命令。

未创建、修改、删除、chmod、格式化或提取任何文件。

### Missing evidence

无本次 Preflight 所要求的 missing evidence。Conda create、quick/unit、source、runtime、completion 的执行证据有意不存在，属于后续阶段而非本次缺失。

## 4. Revision-7 summary

Revision 7 的实质修订仅为：

- 将 SHA、version、三个 mode producer 改成五个顶层 assignment-only simple commands。
- 每个 producer 后使用独立顶层 `test`。
- 建立 R7 input、55-entry allowlist、Plan/backups/baseline/allowlist binding 与 R7 partial-source snapshots。

依据 `R7 inputs:37` 与 `Plan:1020`，未发现对 R4/R5/R6 history、OpenSpec proposal/design/tasks/spec delta、Tasks 1–5、source behavior 或 Step 3 八条命令顺序的重写。

## 5. Findings

### P0

无。

### P1

无。

### P2

无。

### OBS-R7-001 — 验证证据的解释范围

- Severity：Observation
- Location：`Plan:1083`、`R7 inputs:5`
- Observed fact：本次只运行结构探针、OpenSpec validation 和两个 project validator；未执行 Conda create、quick/unit/source/runtime。
- Contract impact：无违反；结论仅覆盖 Plan 可执行性和边界。
- Non-blocking reason：这些执行被本次合同明确禁止，缺少其结果不能阻塞 Plan Preflight。
- Owner：原 bound Codex control-plane；后续 source reviewer/runtime executor 按各自任务接续。
- Release condition：Step 2 成功后生成环境证据，随后 Step 3 生成 validation evidence；source correctness 仍须 Task 7 独立 Review。
- Correction：本 revision 无需修正。
- Re-review trigger：任一 bound artifact/hash/path drift，或 Step 2/3 实际失败。

### OBS-R7-002 — Reviewer instance/thread ID unavailable

- Severity：Observation
- Location：Reviewer Assignment Contract / 本报告 §1
- Observed fact：平台未提供可记录的 instance/thread ID。
- Contract impact：无违反；合同明确允许如实记录 `unavailable` 与 `user_opened_separate_window`。
- Non-blocking reason：独立窗口来源已由用户明确指定，本 reviewer 亦未参与被排除角色。
- Owner：Codex platform / 原 bound control-plane。
- Release condition：持久化 Review 时记录这两个 literal；若平台未来提供 ID，可在后续独立 Review 中记录。
- Correction：本 revision 无需修正。
- Re-review trigger：出现 reviewer 身份冲突证据。

## 6. F-R6 closure matrix

| Finding | R6 blocker | R7 evidence | Closure |
|---|---|---|---|
| F-R6-001 | Producer 嵌在 `test "$(producer)" = ...` 中，可能由外层 `test` 掩盖 producer nonzero；见 `R6 Review:98` | 五个 producer 分别位于 `Plan:1020`、`:1032`、`:1048`、`:1050`、`:1052`，随后各自独立 `test`；Probe A shape PASS，两个 adversarial case 均 exit 7 且 `reached=false` | **CLOSED** |
| F-R6-002 | R6 reviewer 使用未授权 `jq`；见 `R6 Review:123` | 本次为新独立窗口；实际命令全部属于 allowlist；未运行 `jq` 或其他未列命令 | **CLOSED** |

## 7. Task 6 Step 2/3 producer/fail-fast matrix

| 检查项 | Exact evidence | 结果 |
|---|---|---|
| Step 2 shell boundary | `(` + `set -euo pipefail`，见 `Plan:1011` | PASS |
| 四组 path guards | Prefix/HOME/PKGS/TMP 各有独立顶层 `test ! -e` 与 `test ! -L`，见 `Plan:1023` | PASS |
| SHA producer | `ROLE_CONDA_SHA="$(...)"` 后独立 SHA `test` | PASS |
| Version producer | `ROLE_CONDA_VERSION="$(HOME=... "$ROLE_CONDA" --version)"` 后独立 version `test`，见 `Plan:1032` | PASS |
| Mode producers | HOME/PKGS/TMP 三个 plain assignment 后各自独立 `test`，见 `Plan:1048` | PASS |
| Wrapper absence | 五个 producer 均无 `export`、`readonly`、`typeset` 或外层 `test` wrapper | PASS |
| Single producer failure | Probe A：producer 输出 `expected` 后 exit 7；assignment 立即终止，`reached=false` | PASS |
| Pipeline producer failure | Probe A：pipefail pipeline 上游 exit 7；assignment 立即终止，`reached=false` | PASS |
| Conda create/order | Guards → isolated dirs → version check → exact create → executable/mode/dependency assertions，见 `Plan:1037` | PASS |
| Step 2 parse | `/bin/zsh -n` | PASS |
| Step 3 boundary | 独立 `(` + `set -euo pipefail`，见 `Plan:1088` | PASS |
| Step 3 order | 八条命令保持 Router quick/core/unit → Companion quick/templates/unit → 两条 OpenSpec，见 `Plan:1090` | PASS |
| Step 3 failure behavior | 首个 nonzero 停止；无 Conda recreate/fallback | PASS |
| Step 3 parse | `/bin/zsh -n` | PASS |

## 8. Conda isolation matrix

| Boundary | Evidence | 结果 |
|---|---|---|
| Executable | `/opt/anaconda3/bin/conda` regular file，mode `0755`，size 515，SHA 与 binding 一致 | PASS |
| Prefix | `T/conda-quick-validate-r1`：`stat` absent；`readlink` non-symlink | PASS |
| HOME | `T/conda-home-r1`：absent/non-symlink | PASS |
| Package cache | `T/conda-pkgs-r1`：absent/non-symlink | PASS |
| TMPDIR | `T/conda-tmp-r1`：absent/non-symlink | PASS |
| Host isolation | HOME、`CONDA_PKGS_DIRS`、TMPDIR、`PYTHONNOUSERSITE=1`、`CONDA_NO_PLUGINS=true` 显式绑定 | PASS |
| Solver/channel | `--solver classic --override-channels --channel defaults --no-default-packages` | PASS |
| Dependencies | Exact create 请求 `python=3.11`、`pyyaml>=6,<7`；后续断言 Python 3.11、PyYAML major 6，见 `Plan:1037` | PASS |
| Executable assertion | `test -x "$ROLE_PREFIX/bin/python"`，见 `Plan:1047` | PASS |
| Write boundary | 仅四个 T 下隔离路径；source、repo、base environment 不在写边界 | PASS |
| Prohibitions | 无 activate/init/config/base mutation、pip、fallback、automatic cleanup | PASS |
| Retention | 环境保留至 Task 11 明示 cleanup；本 verdict 不授权 cleanup，见 `Plan:1065` | PASS |

## 9. R4/R5/R6/R7 continuity matrix

| 阶段 | 连续性证据 | 结果 |
|---|---|---|
| R4 source-start | Router/Companion source-start SHA 均与 immutable table 一致 | PASS |
| R4 backups | Router mode `0600`、27 entries；Companion mode `0600`、14 entries；SHA 匹配；仅 `tar -tf`，未提取 | PASS |
| Recovery | Backup 仅用于显式 recovery，不自动 restore/cleanup，见 `Plan:212` | PASS |
| R4 PASS Review | SHA 未变；其 authority 未被回写或扩大 | PASS |
| R5 history | Inputs、prompt、BLOCKED Review 三个 SHA 未变；F-R5-001 历史仍保留 | PASS |
| R6 history | Inputs、prompt、BLOCKED Review 三个 SHA 未变；F-R6-001/F-R6-002 原始记录未回写 | PASS |
| R7 allowlist | Probe B：55 entries、55 unique、无 wildcard；完整包含 R6 的 52 项，只新增 R7 input/prompt/Review 三项 | PASS |
| R7 bindings | `schema_version=1`、正确 change ID；Plan SHA 绑定 current R7；backup/baseline/allowlist path、SHA、mode、count 完整 | PASS |
| Router R7 snapshot | 334 records；明确排除 R7 input 与 prompt 两项 | PASS |
| Companion R7 snapshot | 29 records；`excluded_paths=[]` | PASS |
| Partial-source interpretation | 两个 snapshot 只证明其采样时点的 partial-source 状态；不冒充 source PASS 或最终 source-delta | PASS |
| Canonical/OpenSpec continuity | Proposal、design、tasks、delta spec SHA 全部未漂移；当前 `openspec list` 为 24/41 tasks | PASS |

## 10. Authority matrix

| 行为 | 本 verdict authority |
|---|---|
| Reviewer 创建/激活 Conda environment | **无** |
| 原 bound control-plane 执行 Step 2 exact subshell | **有，但须先持久化并核验本完整 Review** |
| Step 2 失败后的 fallback/rebuild/cleanup | **无；必须停止** |
| Step 2 成功后执行 Step 3 exact subshell | **有，且仅在 Step 2 exit 0 后** |
| Tasks 1–5 重执行或改写 | **无** |
| Source correctness/PASS/High Review | **无** |
| 真实 Pi、runtime | **无** |
| Git commit/push/PR | **无** |
| Task/canonical state transition | **无** |
| Archive、Envelope、publication、completion | **无** |
| Cleanup | **无** |

## 11. Validation and probes

| Command/probe | Result |
|---|---|
| `openspec list` | exit 0；`add-role-first-review-routing 24/41 tasks` |
| `openspec list --specs` | exit 0；`skill-workflow-governance requirements 30` |
| `openspec validate add-role-first-review-routing --strict` | exit 0；valid |
| `openspec validate --all --strict --no-interactive` | exit 0；3 passed、0 failed |
| Router `validate_core_gates.py .` | exit 0；Core gates valid |
| Companion `validate_templates.py .` | exit 0；Validation succeeded |
| Probe A Step 2 parse | PASS |
| Probe A Step 3 parse | PASS |
| Probe A producer shape | PASS；assignment-only=5、comparisons=5 |
| Probe A single-producer propagation | PASS；exit=7、reached=false |
| Probe A pipeline-producer propagation | PASS；exit=7、reached=false |
| Probe B | PASS；entries=55、router=334、companion=29 |
| End SHA rebinding | 全部与 start/expected 一致 |
| End path occupancy | 四个 Conda paths 全部 absent/non-symlink |

这些 PASS 不证明 Conda create、quick/unit、source、runtime 或 completion。

## 12. Verdict

**PASS**

无 actionable P0/P1/P2。F-R6-001 与 F-R6-002 均已关闭。

## 13. Exact next action

将本完整 Review 返回原 bound Codex control-plane。Control-plane 应：

1. 将 Review 持久化到 R7 allowlist 中约定的 Review artifact，并核验当前 Plan、inputs、bindings、allowlist、snapshot、backup 和四个 Conda path 未漂移。
2. 仅运行 Revised Plan Task 6 Step 2 exact subshell。
3. 仅当 Step 2 exit 0 时，运行 Task 6 Step 3 exact subshell。
4. 任一命令 nonzero 或任一 binding/path drift 时立即停止，不 fallback、不隐式重建、不 cleanup。
5. 不重跑或改写 Tasks 1–5；不执行 source PASS/High Review、真实 Pi、runtime、Git、canonical、archive、Envelope、publication、completion 或 cleanup。
