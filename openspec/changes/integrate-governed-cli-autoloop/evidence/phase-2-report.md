# Phase 2 background mechanism proof report (`BLOCKED` — background entry remains disabled)

**结论**：阶段 2 一次性隔离机制探针（`2.1`–`2.3`）已在 `/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/governed-cli-phase1-s58l8ops/phase2-20261109` 完成实测。按 `design.md` Decision 4 与 `specs/skill-workflow-governance/spec.md` 硬门槛，现有受支持插件接口（`Adapter.command(turn)` + `Adapter.read(stdout, code, stderr)`，在不修改 `~/.agent-autoloop/app/**` 引擎、不新增常驻监督组件、不伪造 `started` 或虚假成功报告的前提下）**无法阻止调用侧被杀（`SIGKILL`）、worker 超时或续接守卫拒绝后的内核 10 次自动重派（`retryLater`），也无法阻止 `worker.ts:292`（`triedFresh`）与 `decide.ts:125`（`settleSession`）静默清空绑定 `resume` 会话**。依契约如实记录阶段 2 为 **`BLOCKED`（`STAGE_2_BLOCKED_BY_ENGINE_MECHANISM_GAP`）**，后台治理入口保持禁用（`background_enabled: false`），继续使用阶段 1 已验收的 Codex + Pi 直接 CLI 调用；阶段 `2.4` 及阶段 `3`–`4` 保持未启动。

---

## 1. 隔离边界与不变性验证

- **一次性探针目录**：`/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/governed-cli-phase1-s58l8ops/phase2-20261109`（通过 `AGENT_AUTOLOOP_HOME` 与 `AGENT_AUTOLOOP_RULES` 指向临时子目录 `autoloop-home`，未触碰 `~/.agent-autoloop/rules.json`、`~/.agent-autoloop/hub.db` 或 `~/.agent-autoloop/plugins`）。
- **引擎源码零修改**：`/Users/elvis/.agent-autoloop/app` 下全部 **223/223** 个非 `.git` 文件在探针运行前后 SHA-256 完全一致（见 `autoloop-app-before.json` 与 `autoloop-app-after.json`）。
- **阶段 1 原始证据零修改**：`/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/governed-cli-phase1-s58l8ops/closure-20261109` 下全部 **61/61** 个文件 SHA-256 与 `evidence/phase-1-supported-manifest.json` 保持 100% 一致。
- **零在线模型消耗**：本阶段全部通过本机 Python 3 与 Node `v24.22.2` 直接驱动真实 Autoloop `worker.ts` / `decide.ts` / `contract.ts` 与本地进程组故障注入完成，未发起任何消耗 `codex-a` 额度的在线模型调用。

---

## 2. `2.1` 启动前绑定会话检查、结果后身份检查与恢复方式核对

在 `phase2-20261109/probe.py` 中落实阶段 1 独立审查建议，将启动前续接守卫收紧为初始阶段白名单：

```python
INITIAL_PHASES = ('r1', 'timeout')
if phase not in INITIAL_PHASES and not identity:
    raise ValueError('BLOCKED: continuation requires an accepted non-empty identity')
```

实测 9 项启动前/结果后守卫场景（见 `guard-2-1-results.json`）：

| 编号 | 场景 | 结果 | 关键证据 |
|---|---|---|---|
| 1 | `pi_r2_valid_prelaunch_and_post_output` | `ACCEPTED` | 启动前核对原生会话文件与 `cwd`，结果后核对 `actual_native == 6303cbde-d521-487a-a8ab-3f73344d5061` |
| 2 | `codex_r2_valid_prelaunch_and_post_output` | `ACCEPTED` | 启动前核对 rollout JSONL 与 `cwd`，结果后核对 `actual_native == 01a1be19-0543-7f91-a85f-db4a2d82c7bd` |
| 3 | `tightened_whitelist_focused_recheck_empty_identity` | `REJECTED` | 扩展续接阶段名 `focused_recheck` 传 `identity=None` 被初始阶段白名单直接拦截 |
| 4 | `tightened_whitelist_verify_resume_blank_identity` | `REJECTED` | 扩展续接阶段名 `verify_resume` 传 `identity=""` 被初始阶段白名单直接拦截 |
| 5 | `initial_phase_r1_with_unexpected_identity` | `REJECTED` | 初始阶段 `r1` 夹带预绑定 `identity` 被拒绝 |
| 6 | `scheduler_cleared_or_replaced_bound_resume` | `REJECTED` | 模拟调度器清空或替换 `turn.resume`（与合同绑定 `expected_contract_identity` 不符），在 CLI 启动前拦截 |
| 7 | `codex_changed_cwd_mismatch` | `REJECTED` | 原生会话头 `cwd` 与当前进程 `cwd` 不一致，启动前拒绝 |
| 8 | `previous_execution_state_unknown` | `REJECTED` | 前序执行状态为 `unknown`，启动前拒绝恢复 |
| 9 | `post_output_silent_new_session_mismatch` | `REJECTED` | 输出返回的新 `thread_id` 与绑定身份不符，后验检查判废（`BLOCKED: post-output native session mismatch`） |

---

## 3. `2.2` 五类故障与边界实测（对照 `worker/worker.ts` 与 `kernel/decide.ts`）

通过 `phase2_autoloop_mechanism_probe.mjs` 驱动 `/Users/elvis/.agent-autoloop/app/worker/worker.ts`（`createWorker`）、`worker/contract.ts`（`readMessage`）与 `kernel/decide.ts`（`decide`），实测结果记录于 `autoloop-2-2-results.json`：

1. **业务 `VERIFY FAIL` 与首行身份前缀（`contract.ts:89-106`, `decide.ts:357-402`）**：
   - 原始输出含首行身份前缀 `"[Grok-4.20]\n没跑成：验证失败"` 时，`readMessage()` 取首行 `"[Grok-4.20]"` 误判为 `outcome: "done"`；若首行直接为 `"没跑成：验证失败"`，则 `readMessage()` 返回 `outcome: "failed"` 并触发 `retryLater()` 重跑。
   - **存活封装路径（可证明）**：当受控封装自身存活、完成固定验证并落盘 `raw/verify-fail-report.json` 后，向标准输出打印传输完成摘要 `"报告已交付：治理结论 VERIFY FAIL（详见 verify-fail-report.json，不重跑不转FIX）"`，Run 2 在保持绑定会话 `bound-session-001` 下以 `state: "done", attempts: 0` 结束，实现传输交付与治理 `FAIL` 分离且不触发重跑。
2. **CLI 启动/恢复故障且未达 `started`（`worker/worker.ts:289-303` + `kernel/decide.ts:289-332`）**：
   - Run 3 携带绑定会话 `resume: "bound-session-001"` 启动 Turn 1，模拟 CLI 在 `turn.started` 前报错退出（`exit 1`, `started: false`，遵守 `design.md` 不伪造 `started: true`）。
   - **实测缺口 A（Worker 静默换新会话 `triedFresh`）**：`worker.ts:292-298` 立即打印 `"run 3: couldn't go on in bound-session-001 (CLI startup error before turn.started); starting a new session"`，将 `entry.triedFresh = true`、`entry.resume = null`、`entry.session = "cce0fd1c-a412-447c-9306-dfd7540b9117"`，并在同一 Run 内直接拉起 Turn 2（`launches.log` 实测：`cli_fault_before_started|NULL_RESUME|cce0fd1c-...|85368`）。
   - **实测缺口 B（守卫拦截后仍触发内核重派）**：虽然受控封装在 Turn 2 启动前检测到 `resume == NULL_RESUME` 并以 `exit 22`（`BLOCKED_BY_WRAPPER_PRELAUNCH`）拒绝启动模型，但 `worker.ts:304` 随之向中台提交 `outcome: "failed"`，`decide.ts:396` 调用 `retryLater()` 将 Run 3 设回 `state: "queued", attempts: 1, not_before: "2026-11-09T03:05:02.000Z"`，进入最多 10 次重派循环。
3. **调用侧/封装进程被杀（`SIGKILL` / `exit 137`，`worker/worker.ts:212-220, 304` + `kernel/decide.ts:39, 289-332`）**：
   - Run 4 模拟封装进程在落盘有效报告前被 `kill -9`（`exit 137`）。按 `design.md` Decision 4，禁止将未完成/被杀的任务伪造为正常 `done` 报告。
   - **实测缺口 C（10 次自动重跑 `MAX_ATTEMPTS = 10`）**：每次 `exit 137` 均由 `worker.ts` 上报 `outcome: "failed", error: "exit 137"`，`decide.ts:289-332` 连续重入队派发 **10 次**（`attempts: 1..9` 全部回到 `state: "queued"`，第 3 次发出 `failing` 通知，直到第 **10** 次才转为 `state: "cancelled", summary: "连续 10 次没跑成，不再自动重试"`）。现有 `Adapter` 接口无任何合法返回值可在不伪造 `done`/不改引擎的前提下终止 `retryLater`。
4. **Worker 自身超时（`worker/worker.ts:281-287, 376-377`）**：
   - Run 5 配置 `timeout: 1`（1 分钟），推进时钟超过 60 秒后 `worker.ts:377` 调用 `stop(entry, "timeout")` 发送 `SIGTERM`。
   - **实测缺口 D（Worker 超时硬编码覆盖为 `failed` 并重派）**：在 `conclude()`（`worker.ts:281-287`）中，`if (entry.why === "timeout")` 分支位于 `resultFrom(readMessage(seen.text))` 之前，**无条件忽略 `Adapter.read()` 返回的任何 `text`**，直接写入 `{ outcome: "failed", error: "超过 1 分钟还没结束，已停止" }`；中台 `decide.ts:396` 随后将其转入 `retryLater()`（`state: "queued", attempts: 1`）。插件接口对此分支完全无控制权。
5. **中台租约超时 `unknown` 与 `settleSession` 静默清空恢复目标（`kernel/decide.ts:116-127, 223-230`）**：
   - Run 6 建立绑定会话 `bound-session-001`；Run 7 认领该会话后超过 `RUN_LEASE`（5 分钟）未出现在 worker 心跳中，`sweep()`（`decide.ts:225`）将 Run 7 置为 `state: "unknown"`。
   - 随后在同 `(rule, lane)` 上通过回答绑定 `session: "bound-session-001"` 的卡片生成 Run 8（认领前数据库中 `run8.resume === "bound-session-001"`）。
   - **实测缺口 E（`settleSession` 静默抹除显式 `resume`）**：当 worker 认领 Run 8 时，`claimNext()` 调用 `settleSession()`（`decide.ts:116-127`），因检测到同线程存在 `state: "unknown"` 的 Run 7 持有 `bound-session-001`（`going.some((other) => (other.session ?? other.resume) === session)`），执行 `put(draft, "runs", run.id, nulls("session", "resume"))` 将 Run 8 的 `resume` 静默清空为 `null`，worker 随即生成新 UUID `97bc9f83-1773-40d8-a62b-2400f1e1c255` 启动（`launches.log`: `unknown_check_launch|NULL_RESUME|97bc9f83-...|86081`）。即便封装启动前守卫拦截了 `NULL_RESUME`（`exit 23`），该拦截结果仍被 `decide.ts` 送入 `retryLater()` 循环。

---

## 4. `2.3` 阶段 2 门禁判定与缺省收口决定

对照 `design.md` Decision 4（*"确定的缺省决定是：证据不足则后台治理入口保持禁用，继续直接 CLI。当前方案不授权修改引擎、新增常驻监督组件或伪造 started。若现有受支持接口不能满足约束，停止阶段 2，明确缺口；选取新机制须修订设计/范围并重新取得相应批准"*）：

1. **阶段 2 结论**：**`BLOCKED`（`STAGE_2_BLOCKED_BY_ENGINE_MECHANISM_GAP`）**。
2. **已验证可行的局部能力**：
   - 宿主席位/封装内的启动前会话白名单守卫（`2.1`）与结果后 native ID 核验可阻止错误会话实际启动模型或被错误接受；
   - 封装存活时的业务 `VERIFY FAIL` 可通过传输层摘要与落盘报告分离，避免触发 `retryLater`。
3. **现有受支持接口无法跨越的 4 项引擎级缺口**：
   - `worker/worker.ts:292-298`：未 `started` 失败时自动 `triedFresh = true` 清空 `resume` 并在同 Run 内静默重开新会话；
   - `worker/worker.ts:281-287`：worker 自身 `timeout` 分支硬编码返回 `{ outcome: "failed" }`，绕过 `Adapter.read().text`；
   - `kernel/decide.ts:39, 289-332, 396`：凡 `outcome === "failed"`（含封装被 `SIGKILL`、worker `timeout`、封装启动前 `BLOCKED` 拒绝）一律进入 `retryLater` 自动重派最多 **10 次**；
   - `kernel/decide.ts:116-127`：当同 `(rule, lane)` 存在 `claimed` 或 `unknown` 轮次持有同一会话时，`settleSession` 静默将后续轮次的显式 `resume` 置为 `null`。
4. **当前动作与后续条件**：
   - 停止阶段 2，**保持后台 `autoloop` 治理入口禁用（`background_enabled: false`）**，不进入 `2.4`（插件安装/回滚演练）及阶段 `3`–`4`；
   - 日常受控互审与验证继续使用阶段 1 已验收通过的 **Codex + Pi 直接 CLI 调用**；
   - 未来若需启用后台治理批次，必须先另行立项/修订设计并获用户批准（例如：在引擎支持 per-rule `maxRetries: 0` / `allowFreshSessionOnResumeError: false` / `preserveResumeOnUnknown: block`，或获批在宿主席位引入持久熔断状态并在未获准重派时主动调用 `cancel(runId)`）。
