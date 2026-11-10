# Phase 4 Bound Controller Return & User-Authorized Pi Closeout Handoff Report (`4.1`–`4.3`)

## 1. 阶段 4 契约修订与收尾归属（`approval-amendment-phase4-pi-closeout.json`）

1. **原 Codex 主控恢复实测阻碍事实（2026-11-10）**：
   - 用户尝试恢复 Codex 线程时，实测遇到三项平台/环境阻碍：① Codex TUI 拒绝 `gpt-6.1-sol`（`not supported when using Codex with a ChatGPT account`）；② 桌面端 ChatGPT App 占用会话锁导致 CLI 返回 `session is open in another app; no operation was sent`；③ 多行 `-C` 参数换行截断摩擦。
2. **用户明确授权交接给 Pi 收尾**：
   - 用户明确发出指令 `“我想让codex把收尾交给pi”`，按 `AGENTS.md` 第 3 行（当前会话中用户的直接要求优先）与本 change 修订记录 `approval-amendment-phase4-pi-closeout.json`（SHA-256 `b4a0bb1d4d5c383bb83403df388770fd34084b21474c0de6acefad1bd7f8720c`），将本 change 阶段 4（`4.1`–`4.3`）的队列信封消费、全量产物哈希核验与 change 级收尾交接给当前受控 Pi 实例（`01a1bfdd-efd8-77b3-8bc6-7513429647ce`，承接前序执行会话 `01a1bec5-45cb-76cc-9766-4c191329bdec`），并由独立 Pi 审查窗口（`01a1c3e6-1465-728a-99c4-a25ee74b42ee`）执行只读验收审查。
   - **严格边界**：仅对本 change 生效，不修改全局 `CROSS_CLI_GOVERNANCE`（`CCG-001`）或任何可移植 Skill 源码，不对 `~/.codex-account-a/queue_1.sqlite` 执行任何 `DELETE`/写操作，不执行 `openspec archive` 或任何 Git 写操作。

---

## 2. `4.1` 原主控线程核验、`codex queue` 入队、恢复受阻记录与授权 Pi 交接消费

1. **投递前主控线程与账户归属只读核验**（`gov_return.verify_bound_thread_in_codex_home`）：
   - 以只读 URI（`file:/Users/elvis/.codex-account-a/state_5.sqlite?mode=ro`）核验 `threads` 表：`id = 01a1aa6c-c4c8-7111-812f-02e1396290e7`，`cwd = /Users/elvis/file/develop/opensource/openspec-superpower-change`，`updated_at = 1794194304`；并核验 `session_index.jsonl:192`（`thread_name = "修正两个 Skill 主文档"`）。
   - 原主控线程在 `state_5.sqlite` 中记录的初始 `cwd` 为主仓库根目录，本 change 隔离在同仓库 worktree `/Users/elvis/.codex-account-a/worktrees/8739/openspec-superpower-change`，两者同属 `ALLOWED_CWDS` 允许的本仓库项目根路径。
   - 反例核验：不存在的线程 ID `00000000-0000-0000-0000-000000000000` 在投递前被直接拦截。
2. **真实 `codex queue` 入队与只读队列核验（已对齐 P3 精确字面值）**：
   - 入队记录：`queued_items.id = 01a1c38b-9744-72b0-b07f-2e0ba5bf2f25`（`thread_id = 01a1aa6c-c4c8-7111-812f-02e1396290e7`，`queue_order = 0`，`created_at_ms = 1794282067780`）。
   - 以只读 URI（`file:/Users/elvis/.codex-account-a/queue_1.sqlite?mode=ro`）核验：外层 `payload_json` 列（1716 字节）SHA-256 为 `ff9e89643bae2ac0e10e69e9bf1b9ded0c487338d9d653e1c0dca0de4760dbb0`；内嵌 `json.loads(payload_json)["UserInput"]["content"][0]["text"]` 紧凑 JSON 文本 SHA-256 为 `089e51c7e847fdbeb408146fa8b55c98d600bfb283b8dc97eeb64903d9a49341`；格式化落盘文件 `phase4-20261110/bounded-envelope.json` 的文件级 SHA-256 为 `9bdce28e84135624b0f0662010347b142032967697ef0b1d38f8e35f4fe1b2f7`（三者解析出的信封 JSON 键值完全相同）。
3. **历史 SQLite `DELETE` 操作披露与 Fail-Closed 保护（P1-2）**：
   - 初次探针编写阶段曾对 `queue_1.sqlite` 执行过两次探针行清理（仅移除同轮刚创建的临时行 `01a1c382-bfd7-7100-a8e0-d292cc6c33d6`，此前无既有用户队列消息）。现 `gov_return.py` 与 `phase4_return_probe.py` 已移除全部 SQLite 写语句，仅以 `?mode=ro` 只读访问，并对非预期占用队列项执行 fail-closed（`BLOCKED_OCCUPIED_QUEUE_REFUSED_NO_DELETE`）。
4. **授权 Pi 收尾交接消费与证据接受**（`gov_return.consume_queued_envelope_via_authorized_handoff`）：
   - 核验 `approval-amendment-phase4-pi-closeout.json` 存在且绑定 `change_id == "integrate-governed-cli-autoloop"`、`previous_control_plane_native == "01a1aa6c-c4c8-7111-812f-02e1396290e7"` 及 `authorized_phase4_closeout_owner.instance_id == "01a1bfdd-efd8-77b3-8bc6-7513429647ce"`（反例：缺失授权文件时直接抛出 `BLOCKED: approval-amendment-phase4-pi-closeout.json missing`）。
   - 从 `queue_1.sqlite?mode=ro` 只读提取队列项 `01a1c38b-9744-72b0-b07f-2e0ba5bf2f25`，完整校验信封 Schema、`contract_revision == 2`、`canonical_sha256` 及 4 项引用产物（`report.md`、`receipt.json`、`phase-2-3-closeout.json`、`pi-phase-2-3-review-receipt.json`）的磁盘 SHA-256 全部零误差匹配，生成 `evidence/phase-4-pi-handoff-acceptance.json`（`status: "ACCEPTED_VIA_USER_AUTHORIZED_PI_CLOSEOUT_HANDOFF"`）。
   - 四阶段状态记录于 `evidence/phase-4-delivery-receipt.json`：`queued: true`、`resume_attempted_on_codex: true`（`codex_native_resume_outcome: "BLOCKED_BY_MODEL_AND_APP_SESSION_LOCK"`）、`consumed_via_authorized_pi_handoff: true`、`governance_accepted_for_change_closeout: true`。

---

## 3. `4.2` 8 项信封去重与失效/篡改/越界/状态失配拦截证明

在 `phase4-20261110/phase4-results.json` 中通过 `gov_return.precheck_return_envelope()`（纯内存集合比对，无第二份持久化状态文件 `return-dedup-ledger.json`）实测通过全部 8/8 场景：

| 编号 | 场景 | 结果 `status` | `eligible_for_owner_review` | 说明 |
|---|---|---|---|---|
| 1 | `1_valid_first_precheck` | `PRECHECK_PASSED_AWAITING_BOUND_CONTROL_PLANE` | `true` | 首次合法信封，4 项产物路径/SHA-256、`contract_revision: 2`、`canonical_sha256`、目标主控 ID 与 `previous_status` 均匹配 |
| 2 | `2_duplicate_same_batch_attempt` | `DUPLICATE_NOOP` | `false` | 同一 `(change_id, batch=1, attempt=1)` 重复投递，返回 `DUPLICATE_NOOP`，不重复执行或重复推进 |
| 3 | `3_stale_contract_revision` | `REJECTED_STALE_CONTRACT` | `false` | `contract_revision: 1 != 2`，拦截过期修订信封 |
| 4 | `4_stale_canonical_sha256` | `REJECTED_STALE_CONTRACT` | `false` | `canonical_sha256` 不匹配，拦截过期指纹信封 |
| 5 | `5_tampered_report_sha256` | `REJECTED_ARTIFACT_HASH_MISMATCH` | `false` | `report_sha256` 与磁盘实际 `report.md`（`2cc3f95e...`）不一致，拦截篡改产物 |
| 6 | `6_out_of_scope_path_traversal` | `REJECTED_PATH_OUT_OF_SCOPE` | `false` | `report_path` 指向 `/etc/hosts`（超出允许根目录），在读取文件前拦截 |
| 7 | `7_mismatched_target_control_plane_native` | `REJECTED_TARGET_CONTROLLER_MISMATCH` | `false` | 信封目标 `control_plane_native` 不一致，拦截错投信封 |
| 8 | `8_mismatched_previous_status` | `REJECTED_PREVIOUS_STATUS_MISMATCH` | `false` | 期望前序状态与实际当前状态不符，拦截状态失配 |

---

## 4. `4.3` 验证结果、未启用项与归档边界

1. **验证结果**：
   - `python3 adapter/tests/phase4_return_probe.py /Users/elvis/.local/state/governed-cli-autoloop/integrate-governed-cli-autoloop/phase4-20261110 --verify-only`：`exit 0`（8/8 预检场景 + 授权 Pi 交接消费核验通过，`second_state_file_exists: false`）。
   - `openspec validate integrate-governed-cli-autoloop --strict`：`exit 0`（`Change 'integrate-governed-cli-autoloop' is valid`）。
   - `python3 /Users/elvis/.codex/scripts/sync_user_global.py --check`：`exit 0`（五端状态全部 `OK`）。
2. **显式未启用项与边界**：
   - AGY `1.5.3` 自动只读入口未启用（保留受限直调/手动回退）；
   - 后台 `agent-autoloop` 常驻规则未启用（`~/.agent-autoloop/rules.json` 已恢复备份 SHA-256 `16a403549c5080a3bd27f30c10901f130bb2f458750bb8f4ec7921973d9c30c5`，`~/.agent-autoloop/plugins` 为空）；
   - 不执行 `openspec archive`，不执行任何 Git 写操作；`queue_1.sqlite` 中队列记录 `01a1c38b-9744-72b0-b07f-2e0ba5bf2f25` 与 `~/.pi/agent/settings.json` 中 `openai-codex/*` 条目保持原状，是否清理由用户本人决定。
