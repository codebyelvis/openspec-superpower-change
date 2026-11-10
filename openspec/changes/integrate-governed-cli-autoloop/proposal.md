# Change: Integrate governed CLI calls with bounded Autoloop transport

## Why

提交 `7c46180` 已规定默认 Headless CLI 互审、同 reviewer 复查和只读下一步查询，但相关文本测试不能证明本机 Codex、Pi、AGY 的参数、权限、续接和结果返回真正一致可用。`agent-autoloop` 的 Codex 颜色试跑已通过；正式治理批次尚未接入。首行身份前缀遮挡结论已经复现，内核自动重试与换新会话则存在需要约束的源码路径。

本 change 补齐调用与传输的可验证边界，复用既有治理，不重新设计状态机，也不把调度器的 `done` 当作任务完成。

## What Changes

1. 保留短任务默认 CLI 直调和人工 Prompt 回退；当前自动入口支持范围收敛为 Codex + Pi，并验证其准确参数、权限、原生会话和终态结果；AGY 保留受限直调/手动回退，不用通用 `use: command` 假装获得治理能力。
2. 在每次实际启动 CLI 前核对当前合同与期望恢复实例；禁止静默新建会话承接同一绑定身份。结果返回后再核对实际 native session。
3. 分开只读 Review、固定命令 VERIFY、宿主证据落盘职责。业务 `PASS/FAIL/BLOCKED` 与传输成功分别记录；无有效证据不得合成成功。
4. 将禁止越限重试、禁止换实例、正确处理超时及 `unknown` 作为后台启用硬条件。较短的内层超时只是局部措施；按 `approval-amendment-phase2-unblock.json` 批准的阶段 2–4 实现边界，在不修改 `~/.agent-autoloop/app/**` 引擎源码的前提下，采用宿主侧持久化 Attempt/Session 账本 + 受控 Runner（`adapter/gov_runner.py` + `adapter/govpi/agent.ts`）：(a) 当 `worker.ts:347` (`triedFresh`) 或 `decide.ts:121` (`settleSession`) 导致 `resume` 丢失/冲突时，在启动 CLI 前由本地持久化账本拦截，立即落盘 `report-abort.md` 并以 `exit 0` + 正常回执（`"执行中止：会话续接被拦截，已生成中止报告，禁止重跑"`）结束，直接阻断 `triedFresh` 与 `retryLater`；(b) 当外层 worker timeout 或封装异常进入 `retryLater`（`attempt >= 2`）且该批次禁止重跑时，在 `attempt >= 2` 启动 CLI 前主动调用 `agent-autoloop stop <run-id>` 取消当前 Run 并拒绝启动 CLI。所有阶段 2–4 探针与运行证据固定在持久目录 `/Users/elvis/.local/state/governed-cli-autoloop/integrate-governed-cli-autoloop/`。
5. 在单批次 VERIFY 验收后验证 `codex queue` 向原绑定主控回传，区分入队、恢复、消费和证据接受，保留人工恢复入口；当原 Codex 主控线程因模型下线/TUI 不支持（如 `gpt-6.1-sol`）或桌面端会话占用锁阻塞且用户明确授权将收尾交接给 Pi 时，允许由获准的受控 Pi 实例以只读方式从 `queue_1.sqlite` 读取并核验已入队信封与全量证据哈希，经独立 Pi 审查实例复核通过后完成本 change 收尾（不代表修改全局 `CCG-001` 规则，也不自动执行 `openspec archive` 或 Git 写操作）。
6. 定义源码归属、安装命名、停止在途任务和清缓存的回滚要求；保留审计证据。

## Scope and non-goals

- Affected spec: `skill-workflow-governance`，新增约束，不替换现有要求。
- 维持 schema-6、schema-2 证据、canonical status、control-plane 所有权、独立 Review、现有失败熔断及用户批准边界。
- `scripts/next_action.py` 保持只读；不新增治理状态、通用 runner、注册中心、自动换主控或自动换 reviewer。
- 不扩大 Skill 自动触发，不重新打开 `narrow-skill-autoload`，不改变轻量审阅加载规则。
- 不授权业务源码修改、Git stage/commit/push、生产、凭据、发布、全局指令调整或跨 CLI 同步。
- 不修改 `~/.agent-autoloop/app/**` 安装引擎。若插件无法满足机制门槛，报告 BLOCKED；引擎变更或新的监管组件须另行修订范围并获批。

## Impact and ownership

- 当前只新增本 change 的 `proposal.md`、`design.md`、`tasks.md`、spec delta 及最小审阅证据。
- 主仓库基线：`11e339dae5f92fc21a75cbe16bcc9b078e24b11a`。使用独立 worktree，不混入主工作树的 native-consumer / control-plane rebind 候选。
- 后续可能受影响的现有文件与各阶段允许范围见 `design.md`；这些是提议目标，不是当前实施许可。
- Companion 没有独立 OpenSpec，本 change 记录其候选目标 `references/agy-dispatch-template.md`。不修改两份主 `SKILL.md`。

## Approval and delivery boundary

状态：`approved / phases-0-4-completed-via-authorized-pi-closeout-handoff`。初始实施批准见 approval.json；2026-11-09 用户明确允许择一收敛，选路径 A 的 Codex + Pi 支持子集（见 approval-amendment-20261109.json）；阶段 2 初探报告 `BLOCKED` 经独立 Pi 审查通过（见 `evidence/pi-phase-2-review-receipt.json`）后，用户按 `tasks.md 2.3` 与 `design.md` Decision 4 明确批准阶段 2–4 外层受控适配器方案与持久证据路径（见 `approval-amendment-phase2-unblock.json`）；2026-11-10 在原 Codex 线程因 `gpt-6.1-sol` TUI 不支持及桌面端会话锁阻塞后，用户明确批准将阶段 4 收尾交接给 Pi（`01a1bfdd-efd8-77b3-8bc6-7513429647ce`）并由独立 Pi 审查窗口（`01a1c3e6-1465-728a-99c4-a25ee74b42ee`）复核收口（见 `approval-amendment-phase4-pi-closeout.json`）。

Pi 对提案的 PASS 只证明该版本提案可供用户决策，不批准代码、配置、安装或 canonical 状态迁移。用户明确批准本 change 的具体版本后，才可进入设计中已封闭范围的阶段；尚无可执行保证的后台路径保持禁用。

本次检查：`openspec validate integrate-governed-cli-autoloop --strict` 与独立 Pi 只读审阅。后续真实运行验收与当前结构/方案审阅分开记录。
