<!-- COOP_EVIDENCE_MANIFEST_START -->
```yaml
evidence_schema_version: 2
evidence_role: attempt-report
evidence_result: pass
change_id: integrate-governed-cli-autoloop
current_batch: 1
attempt: 1
contract_revision: 2
canonical_sha256: 2db5b42026ff231d0fd4e50a82e7a3f5550cf2fb8999a6d0794cca6beeab1049
agent_product: pi
agent_instance_id: 01a1c320-0e21-7477-8df6-063eab185552
agent_role: executor
capability_profile: implementation-high
```
<!-- COOP_EVIDENCE_MANIFEST_END -->

# Phase 3 Single Background VERIFY Batch Report (`3.1`–`3.3`)

## 1. `3.1` 批次契约、测试命令、权限与 Schema-6 Assignment

- **批次标识**：`real-verify-20261109-r3`（批次配置文件 `/Users/elvis/.local/state/governed-cli-autoloop/integrate-governed-cli-autoloop/real-20261109-r3/batch-real-verify-20261109-r3.json`）。
- **触发方式**：单次显式手动事件 `agent-autoloop emit gov.verify.run --subject real-verify-20261109-r3 --summary "phase 3 single VERIFY batch"`（不启用任何 `schedule`/cron 定时触发）。
- **受测工作区与 Revision**：`/Users/elvis/.codex-account-a/worktrees/8739/openspec-superpower-change`，`HEAD = 11e339dae5f92fc21a75cbe16bcc9b078e24b11a`。
- **固定验证命令**：`["/opt/homebrew/bin/openspec", "validate", "integrate-governed-cli-autoloop", "--strict"]`（由宿主受控 Runner `gov_runner.py` 执行并落盘原始输出，不授予模型 shell 或写工具权限）。
- **只读 Pi 调用参数（零 `codex-a` 额度消耗）**：
  ```json
  [
    "/Users/elvis/.local/bin/pi",
    "-p",
    "--mode", "json",
    "--no-mcp",
    "--no-extensions",
    "--no-skills",
    "--no-context-files",
    "--no-prompt-templates",
    "--tools", "read,grep,find,ls",
    "--provider", "amd-radeon",
    "--model", "DeepSeek-V4-Flash",
    "--session-dir", "/Users/elvis/.local/state/governed-cli-autoloop/integrate-governed-cli-autoloop/real-20261109-r3/evidence/run-11/attempt-1/pi-sessions"
  ]
  ```
- **产物写入范围**：仅限持久证据目录 `/Users/elvis/.local/state/governed-cli-autoloop/integrate-governed-cli-autoloop/real-20261109-r3/` 与本 change 的 `openspec/changes/integrate-governed-cli-autoloop/evidence/`；不修改业务源码、不修改 canonical status、不执行任何 Git 写操作。
- **Schema-6 Assignment 绑定**：
  - `purpose`: `"Phase 3 single-batch background VERIFY execution and evidence delivery"`
  - `product`: `"pi"`
  - `instance_id` (actual background VERIFY native session): `"01a1c320-0e21-7477-8df6-063eab185552"`（由受权执行会话 Pi `01a1bec5-45cb-76cc-9766-4c191329bdec` 派发）
  - `role`: `"executor"`
  - `profile`: `"implementation-high"`
  - `independence_requirement`: `"independent_from_control_plane_and_reviewer"`
  - `result_authority`: `"bounded-execution-evidence"`
  - `control_plane_native`: `"01a1aa6c-c4c8-7111-812f-02e1396290e7"`（Codex 主控）
  - `independent_reviewer_native`: `"01a1afbe-e61b-768b-896d-8a743ed83565"`（独立 Pi 审查实例）

---

## 2. `3.2` 真实运行结果、原始产物与 Schema-2 / 哈希证据

### 2.1 后台 Run `#11`（`VERIFY: PASS`）核心证据

- **Autoloop Run ID / 状态**：`run = 11`，`attempt = 1`，`state = "done"`，中台摘要：`#11 治理VERIFY单批次 做完了：报告已交付：治理结论见 report.md（VERIFY: PASS）`（状态变更日志见 `real-20261109-r3/why-verify-run11.json`）。
- **账本记录**（`real-20261109-r3/ledger/real-verify-20261109-r3.json`）：仅 1 次启动（`run: "11", attempt: 1, turn: 1, action: "launch"`）。
- **原生 Pi 会话文件**：`real-20261109-r3/evidence/run-11/attempt-1/pi-sessions/2026-11-10T01-34-18-886Z_01a1c320-0e21-7477-8df6-063eab185552.jsonl`（确认暴露工具仅为 `read,grep,find,ls`，`stopReason == "stop"`）。
- **原始结果与报告 SHA-256**（对齐 `real-20261109-r3/evidence/run-11/receipt.json`）：

| 文件 | 路径（相对于 `real-20261109-r3/evidence/run-11/`） | SHA-256 | 说明 |
|---|---|---|---|
| Schema-2 报告 | `report.md` | `2cc3f95e78f996c71da099a4d2d07ee5832363204a40e0a99af784d0c3db1314` | 含 `COOP_EVIDENCE_MANIFEST_START`（`evidence_schema_version: 2`, `canonical_sha256: 2db5b42026ff231d0fd4e50a82e7a3f5550cf2fb8999a6d0794cca6beeab1049`）及 `VERIFY: PASS` 正文 |
| 结构化回执 | `receipt.json` | 见 `phase-2-3-manifest.json` | 绑定 Schema-6 assignment、`report_sha256`、`raw_sha256`、`canonical_status_modified: false`、`business_source_modified: false` |
| 固定命令 stdout | `attempt-1/verify.stdout` | `2c3620840ed6cf18c49f13d38cbfe6818de03169762fc995b3b033f464eb85f7` | `Change 'integrate-governed-cli-autoloop' is valid\n` |
| 固定命令 stderr | `attempt-1/verify.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 空（0 字节） |
| 固定命令 exit | `attempt-1/verify.exit` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | `0\n` |
| Pi 调用参数 | `attempt-1/cli.argv.json` | `5e664a8acd2ac779d27cee1420b041bdd414f1f9fa7510be160b5e554b29666d` | 完整只读参数列表 |
| Pi 原始 JSONL | `attempt-1/cli.stdout` | `16cc4629305550bd42622ad1741133639419a5210996471e07c825c707f9a8a5` | 含 `session`、`tool_execution_start/end` (`read`)、`message_end` (`stopReason: "stop"`)、`agent_settled` |
| Pi stderr | `attempt-1/cli.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 空（0 字节） |
| Pi exit | `attempt-1/cli.exit` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | `0\n` |

### 2.2 `FAIL / BLOCKED` 不转 `FIX`、不重跑业务证明

1. **业务 `VERIFY: FAIL` 场景**（`adapter-proof-20261109/adapter-mechanism-results.json` `s1_business_verify_fail`）：当验证结论为 `VERIFY: FAIL` 时，Runner 落盘 `evidence/run-2/report.md`（`VERIFY: FAIL（业务失败，不重跑不转FIX）`），向 Autoloop 返回传输交付摘要 `"报告已交付：治理结论见 report.md（VERIFY: FAIL（业务失败，不重跑不转FIX））"`，Run 2 以 `state: "done", attempts: 0` 结束，CLI 仅执行 1 次，不触发 `retryLater`，不转 `FIX`。
2. **真实服务 CLI 异常 / `BLOCKED` 场景**（`real-20261109` Run `#4`）：当 `attempt 1` 因模型报错返回 `BLOCKED: assistant stopReason != stop`（`exit 4`）触发内核 `retryLater` 时，`attempt 2` 在启动 CLI 前被 `gov_runner.py` 持久化账本（`real-20261109/ledger/real-verify-20261109.json`）拦截并主动执行 `agent-autoloop stop 4` 将 Run `#4` 转为 `cancelled`，拒绝再次启动 CLI，且未改动任何业务文件或 canonical status（针对真实中台长轮询收到 `/cancel` 后立即下发 `SIGTERM` 导致原顺序来不及写 `report-abort.md` 的时序细节，最终版 `gov_runner.py` `436f3a2c...` 已改为在调用 `stop_cmd` 前先 flush `report-abort.md` 并设置 `SIG_IGN`）。

---

## 3. `3.3` 传输完成与治理结论分离及独立审查门禁

- **传输完成与治理结论分离**：
  - 传输层（`agent-autoloop` Run 状态 `done` / `cancelled`）仅表示后台受控 Runner 已完成当次执行或中止回执投递；
  - 治理层结论唯一以落盘的 `report.md`（含 Schema-2 manifest 与 SHA-256）或 `report-abort.md` 为准，且必须经独立 Reviewer 审查与原绑定 Codex 主控核认后方可推进 canonical 状态。
- **当前状态**：`2.4`、`3.1`、`3.2` 已完成；`3.3` 待独立审查窗口（Pi `01a1afbe-e61b-768b-896d-8a743ed83565`）只读复核本批次证据；阶段 `4`（`4.1`–`4.3` 原绑定主控 `01a1aa6c-c4c8-7111-812f-02e1396290e7` 回传与最终状态接受）在阶段 3 独立 Review `PASS` 前保持未启动。
