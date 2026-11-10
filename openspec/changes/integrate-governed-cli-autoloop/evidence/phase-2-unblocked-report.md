# Phase 2 Unblocked Mechanism Proof & Task 2.4 Installation / Drain / Rollback Report

## 1. 审批与契约依据

1. **阶段 2 初探报告独立审查回执**：`evidence/pi-phase-2-review-receipt.json`（源会话 `/Users/elvis/.pi/agent/sessions/--Users-elvis-file-develop-opensource-openspec-superpower-change--/2026-11-06T07-24-45-980Z_01a1afbe-e61b-768b-896d-8a743ed83565.jsonl` 第 `222` 行，`event_id=112f1a66`，单行去尾换行 SHA-256 `ca843eeb73f41af10ffa6f390bbda90bc2b5a2018c80eecadf6a362c81b09bf6`，结论 `REVIEW: PASS`）。
2. **用户明确批准修订阶段 2–4 实现边界**：`approval-amendment-phase2-unblock.json`（SHA-256 `2db5b42026ff231d0fd4e50a82e7a3f5550cf2fb8999a6d0794cca6beeab1049`）：
   - 在不修改 `~/.agent-autoloop/app/**` 引擎源码（223/223 文件 SHA-256 零变化）的前提下，采用【宿主侧持久化 Attempt/Session 账本 + 受控 Runner 主动调用 `agent-autoloop stop <run-id>`】的外层受控适配器方案：
     - **(a) `triedFresh` / `settleSession` 会话丢失或冲突拦截**：当 Turn 1 发生 CLI 故障被 `worker.ts:347` (`triedFresh`) 静默置空 `resume` 拉起 Turn 2，或被 `decide.ts:121` (`settleSession`) 因前序 `unknown` 置空 `resume` 时，外层 Runner 在启动 CLI 前由本地持久化账本检测到同 `run-attempt` 二次 Turn 或 `resume` 丢失/冲突，立即落盘 `report-abort.md` 并以 `exit 0` + 正常回执（`"执行中止：会话续接被拦截，已生成中止报告，禁止重跑"`）结束，直接阻断 `triedFresh` 与 `retryLater`；结果后若 native session 与绑定不符，同样落盘 `report-abort.md` 并以 `exit 0`（`"执行中止：结果后会话身份不符，已生成中止报告，禁止重跑"`）结束；
     - **(b) `retryLater` (`attempt >= 2`) 主动取消拦截**：当外层 worker timeout 或封装进程异常（如 `SIGKILL` `exit 137`）导致内核进入 `retryLater`（`attempt >= 2`）时，外层 Runner 在 `attempt >= 2` 启动前检查本地账本，若该治理批次不允许重跑（`allow_rerun: false`），立即主动调用 `agent-autoloop stop <run-id>` 取消当前 Run、落盘 `report-abort.md` 并拒绝启动 CLI；
   - 所有阶段 2–4 探针与运行证据目录固定在持久化路径 `/Users/elvis/.local/state/governed-cli-autoloop/integrate-governed-cli-autoloop/`。

---

## 2. 插件源码归属与结构（`2.4`）

| 角色 | 路径 | SHA-256 | 说明 |
|---|---|---|---|
| 插件入口（`use: "govpi"`） | `openspec/changes/integrate-governed-cli-autoloop/adapter/govpi/agent.ts` | `6b66c14aa200fbe372ab507b34f09463be4b4d4791014d71a1d816cc181dc5e1` | 构造受控 Runner 命令并解析 `META:` 行与终态文本 |
| 宿主受控 Runner | `openspec/changes/integrate-governed-cli-autoloop/adapter/gov_runner.py` | `436f3a2cdd50c7752cd0211f5d3890dcf2c13cb796137166a0831a3b957024ba` | 文件锁持久化账本、启动前/结果后守卫、`agent-autoloop stop <run>` 触发、`report.md`/`report-abort.md`/`receipt.json` 落盘 |
| `2.1` 持久守卫探针 | `openspec/changes/integrate-governed-cli-autoloop/adapter/tests/guard_2_1_probe.py` | 见 `phase-2-3-manifest.json` | 持久目录复验 9 项启动前白名单与结果后身份检查 |
| `2.2` 隔离机制证明脚本 | `openspec/changes/integrate-governed-cli-autoloop/adapter/tests/adapter_mechanism_proof.mjs` | 见 `phase-2-3-manifest.json` | 驱动真实未修改 `worker.ts` + `decide.ts` 实测 6 类场景 |
| `2.4` + `3` 真实安装/排空/VERIFY/回滚脚本 | `openspec/changes/integrate-governed-cli-autoloop/adapter/tests/real_install_verify.py` | 见 `phase-2-3-manifest.json` | 真实 `~/.agent-autoloop` 复制安装、`stop` 排空、单批次 Pi VERIFY、回滚与 `launchctl kickstart -k` 清缓存 |

---

## 3. 持久目录 `2.1`–`2.2` 隔离机制证明结果（`adapter-proof-20261109`）

持久证据目录：`/Users/elvis/.local/state/governed-cli-autoloop/integrate-governed-cli-autoloop/adapter-proof-20261109`

- **`2.1` 9 项启动前白名单与结果后身份检查**（`guard-2-1-results.json`）：2 项正向（Pi R2、Codex R2）`ACCEPTED`，7 项反向（`focused_recheck` 空身份、`verify_resume` 空串、`r1` 夹带身份、调度器清空/替换 `resume`、`cwd` 漂移、前序 `unknown`、结果后 `thread_id` 不匹配）全部 `REJECTED_BEFORE_LAUNCH_OR_ACCEPT`。
- **`2.2` 6 项外层受控适配器机制实测**（`adapter-mechanism-results.json`，`assertions: []`，退出码 `0`）：

| 编号 | 场景 | Run ID | 实际 CLI 启动次数 | 账本记录 `(attempt, turn, resume, action)` | 终态与关键证据 |
|---|---|---:|---:|---|---|
| `s1` | 业务 `VERIFY: FAIL` 与传输 `done` 分离 | `2` | `1` (`2\|report_fail\|bound-session-001`) | `(1, 1, "bound-session-001", "launch")` | `state: "done", attempts: 0`，`evidence/run-2/report.md` 落盘 `VERIFY: FAIL`，不重跑不转 FIX |
| `s2` | Turn 1 CLI 未 `started` 故障 + `worker.ts:347` `triedFresh` | `3` | `1`（Turn 2 CLI 未启动） | `(1, 1, "bound-session-001", "launch")`, `(1, 2, null, "abort")` | Turn 2 被账本拦截，落盘 `evidence/run-3/report-abort.md`，返回 `exit 0` `"执行中止：会话续接被拦截，已生成中止报告，禁止重跑"`，`state: "done", attempts: 0`，阻断 `triedFresh` 与 `retryLater` |
| `s3` | 封装进程被 `SIGKILL` (`exit 137`) + `decide.ts` `retryLater` | `4` | `1`（`attempt 2` CLI 未启动） | `(1, 1, null, "launch")`, `(2, 1, "d738...", "stop")` | `attempt 1` 异常退出后内核重派 `attempt 2`；Runner 在启动 CLI 前调用 `stop 4`（`cancel_at` 生效）、落盘 `evidence/run-4/report-abort.md` 并结束，拒绝二次启动 CLI |
| `s4` | Worker 自身超时（`timeout: 1`）+ `decide.ts` `retryLater` | `5` | `1`（`attempt 2` CLI 未启动） | `(1, 1, null, "launch")`, `(2, 1, "ddb9...", "stop")` | `attempt 1` 被 worker timeout 终止后内核重派 `attempt 2`；Runner 在启动 CLI 前调用 `stop 5`、落盘 `evidence/run-5/report-abort.md` 并结束，拒绝二次启动 CLI |
| `s5` | 中台租约超时 `unknown` (`run 7`) + `settleSession` 抹除 `resume` | `8` | `0`（CLI 零启动） | `(1, 1, null, "abort")` | `settleSession` 将 `run 8` 的 `resume` 置为 `null`；Runner 启动前账本比对 `expected_resume="bound-session-001"` 立即拦截，落盘 `evidence/run-8/report-abort.md` 并返回 `"执行中止：会话续接被拦截，已生成中止报告，禁止重跑"` |
| `s6` | 结果后 native session 身份不匹配 | `10` | `1` (`10\|wrong_session\|bound-session-001`) | `(1, 1, "bound-session-001", "launch")` | CLI 返回 `SESSION:wrong-session-999 != bound-session-001`；Runner 落盘 `evidence/run-10/report-abort.md`，不生成有效 `report.md`，返回 `"执行中止：结果后会话身份不符，已生成中止报告，禁止重跑"` |

- **引擎零修改核验**：`autoloop-app-before.json` 与 `autoloop-app-after.json` 对 `/Users/elvis/.agent-autoloop/app` 全部 **223/223** 个非 `.git` 文件 SHA-256 比对完全一致。

---

## 4. `2.4` 真实运行时安装、`stop` 排空、回滚与清缓存验证

持久证据目录：
- `/Users/elvis/.local/state/governed-cli-autoloop/integrate-governed-cli-autoloop/real-20261109-r3`（主验收：含 `2.4` 真实 `stop` 排空 Run `#10` + 阶段 `3` 单批次后台 `VERIFY: PASS` Run `#11` + 完整回滚）
- `/Users/elvis/.local/state/governed-cli-autoloop/integrate-governed-cli-autoloop/real-20261109`（附加真实故障注入证明：含 `2.4` 真实 `stop` 排空 Run `#3` + 真实服务下 Run `#4` 因模型配置报错触发 `attempt 2` 自动执行 `agent-autoloop stop 4` 转为 `cancelled`，并暴露长轮询 `/cancel` 立即下发 `SIGTERM` 的时序边界，已在最终版 `gov_runner.py` 中通过先写 `report-abort.md` 并设置 `SIG_IGN` 修复）

逐项核验结果（详见 `real-20261109-r3/real-facts.json`）：

1. **备份与复制安装**：
   - 备份 `~/.agent-autoloop/rules.json` 至 `real-20261109-r3/rules.json.bak`（SHA-256 `16a403549c5080a3bd27f30c10901f130bb2f458750bb8f4ec7921973d9c30c5`）。
   - 将受管源码复制到 `~/.agent-autoloop/plugins/govpi/{agent.ts,gov_runner.py,install.json}`，安装后 `agent.ts`（`6b66c14a...`）与 `gov_runner.py`（`436f3a2c...`）SHA-256 与源码 100% 一致。
   - 在 `~/.agent-autoloop/rules.json` 新增受控 Agent `gov-pi`（`use: "govpi", access: "read", timeout: 10`）与手动事件规则 `gov.verify.*`（安装态 SHA-256 `b3c090a8cf69439dd2563aa9e30643be4926d091604b97309538a8933e51e082`），并通过 `agent-autoloop emit gov.verify.probe --dry-run` 预演通过。
2. **真实 `agent-autoloop stop <run-id>` 在途排空（Run `#10`）**：
   - 触发手动事件 `gov.verify.stoptest`，worker 认领 Run `#10` 并启动在途进程 `pid 11347`（`/bin/sh .../fake_cli.sh hang NULL_RESUME`）。
   - 执行 `/Users/elvis/.nvm/versions/node/v24.22.2/bin/node --disable-warning=ExperimentalWarning ~/.agent-autoloop/app/bin/agent-autoloop.ts stop 10`，退出码 `0`（输出 `"通知它停了。"`）。
   - 轮询 `agent-autoloop why 10 --json`（保存于 `real-20261109-r3/why-stoptest-run10.json`）确认 Run `#10` 状态变为 `cancelled`（`summary: "已停止"`），`pgrep -fl "fake_cli.sh|gov_runner.py"` 确认为空（在途进程组完全退出，且未触发 `retryLater`）。
3. **真实服务下 `attempt 2` 自动 `stop` 拦截复验（`real-20261109` Run `#4`）**：
   - 在 `real-20261109` 中，Run `#4` `attempt 1` 因未显式指定非 `codex` 模型命中 `gpt-6.1-sol` 账号限制返回 `exit 4`；5 分钟后内核 `retryLater` 派发 `4-2`（`attempt 2`），`gov_runner.py` 在启动 CLI 前由本地账本 `real-20261109/ledger/real-verify-20261109.json` 拦截 `attempt == 2` 并主动调用 `agent-autoloop stop 4`，使真实服务中的 Run `#4` 直接收口为 `state: "cancelled"`（日志见 `~/.agent-autoloop/logs/` 第 306–308 行：`run 4: stopping (cancel)` -> `run 4: cancelled`）。同时发现真实中台长轮询收到 `/cancel` 后会立即向 Runner 进程组发送 `SIGTERM`，故在最终版 `gov_runner.py`（`436f3a2c...`）中调整为先落盘 `report-abort.md` 并设置 `signal.signal(signal.SIGTERM, signal.SIG_IGN)` 再调用 `stop_cmd`。
4. **回滚、清缓存与审计保留**：
   - 确认无在途进程（`drain_procs_before_rollback: ""`）后，将 `rules.json.bak` 还原回 `~/.agent-autoloop/rules.json`，校验 SHA-256 恢复为 `16a403549c5080a3bd27f30c10901f130bb2f458750bb8f4ec7921973d9c30c5`（`rules_restored_equal_backup: true`）。
   - 将 `~/.agent-autoloop/plugins/govpi` 移存至持久审计目录 `real-20261109-r3/rolled-back-plugin-govpi`，确认 `~/.agent-autoloop/plugins/govpi` 已移除（`plugin_absent_after_rollback: true`）。
   - 执行 `launchctl kickstart -k gui/501/agent-autoloop`（`exit 0`），服务主进程 PID 从 `2525` 切换为 `11992`，清除 worker 进程内的插件 ESM `import()` 缓存。
   - 回滚后 `agent-autoloop status` 确认仅保留原有 `Codex` agent，Run `#3..#11` 历史记录、`why-*.json` 及 `~/.agent-autoloop/worker/runs/` 审计记录完整保留。
