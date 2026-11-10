# Phase 4 Bound Controller Manual Resume Entry & Authorized Pi Closeout Handoff (`01a1aa6c-c4c8-7111-812f-02e1396290e7` -> `01a1bfdd-efd8-77b3-8bc6-7513429647ce`)

## 1. 当前投递与交接闭环状态（四级分离记录：`COMPLETED_VIA_USER_AUTHORIZED_PI_CLOSEOUT_HANDOFF`）

| 阶段 | 状态 | 证据与说明 |
|---|---|---|
| 1. 入队（`queued`） | **`true`** | 已通过 `codex queue` 写入 `/Users/elvis/.codex-account-a/queue_1.sqlite`（`queued_items.id = 01a1c38b-9744-72b0-b07f-2e0ba5bf2f25`，`thread_id = 01a1aa6c-c4c8-7111-812f-02e1396290e7`，`queue_order = 0`，`created_at_ms = 1794282067780`；外层 `payload_json` 列 1716 字节 SHA-256 `ff9e89643bae2ac0e10e69e9bf1b9ded0c487338d9d653e1c0dca0de4760dbb0`，内嵌 `UserInput.content[0].text` 紧凑 JSON 字符串 `envelope_sha256 = 089e51c7e847fdbeb408146fa8b55c98d600bfb283b8dc97eeb64903d9a49341`，格式化文件 `bounded-envelope.json` SHA-256 `9bdce28e84135624b0f0662010347b142032967697ef0b1d38f8e35f4fe1b2f7`） |
| 2. 尝试恢复（`resume_attempted_on_codex`） | **`true`**（受阻记录） | 实测两类不可恢复边界：① 未唤醒端点 `--remote unix://.../unawake-owner.sock --resume` 失败；② 原主控线程因 TUI 不支持 `gpt-6.1-sol` 与桌面 App 会话占用锁返回 `no operation was sent`（`BLOCKED_BY_MODEL_AND_APP_SESSION_LOCK`） |
| 3. 授权交接消费（`consumed_via_authorized_pi_handoff`） | **`true`** | 按用户明确授权 `approval-amendment-phase4-pi-closeout.json`（`“我想让codex把收尾交给pi”`），由受控 Pi 实例 `01a1bfdd-efd8-77b3-8bc6-7513429647ce` 通过 `gov_return.consume_queued_envelope_via_authorized_handoff()` 以 `?mode=ro` 只读方式从 `queue_1.sqlite` 读取并完整核验该队列项与 4 项引用产物 SHA-256 |
| 4. 本 change 收尾接受（`governance_accepted_for_change_closeout`） | **`true`** | 已落盘 `evidence/phase-4-pi-handoff-acceptance.json`（`status: "ACCEPTED_VIA_USER_AUTHORIZED_PI_CLOSEOUT_HANDOFF"`），并经独立 Pi 审查实例 `01a1c3e6-1465-728a-99c4-a25ee74b42ee` 只读复核通过 |

---

## 2. 保留的原 Codex 线程人工入口与可选队列清理说明

- 尽管本 change 已按用户授权由 Pi 完成阶段 4 收尾，原 Codex 线程的人工恢复单行命令仍保留备查：
  ```bash
  cd /Users/elvis/.codex-account-a/worktrees/8739/openspec-superpower-change
  CODEX_HOME=/Users/elvis/.codex-account-a /Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex resume 01a1aa6c-c4c8-7111-812f-02e1396290e7 -m gpt-5.6-sol
  ```
- 若后续不再需要原 Codex 线程消费 `~/.codex-account-a/queue_1.sqlite` 中的队列项 `01a1c38b-9744-72b0-b07f-2e0ba5bf2f25`，可由用户本人执行以下一行命令将其移除（本执行窗口遵守只读边界，不自行执行 `DELETE`）：
  ```bash
  sqlite3 ~/.codex-account-a/queue_1.sqlite "DELETE FROM queued_items WHERE id='01a1c38b-9744-72b0-b07f-2e0ba5bf2f25';"
  ```
