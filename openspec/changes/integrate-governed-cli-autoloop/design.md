# Design: integrate-governed-cli-autoloop

## Intent and existing evidence

当前 Codex 主控继续持有 `openspec-superpower-change` 的路由、批准核对、证据接受和完成判断；Codex / Pi / AGY 依 assignment 执行或审阅；Autoloop 仅承载获准后台任务。短任务不因接入而增加后台流程。

| 证据 | 已知事实 | 不可外推的结论 |
|---|---|---|
| 提交 `7c46180` 与现有双模规则 | 默认直接互审、有限复查和 `next_action.py` 已存在 | 文本断言不是三端真实互调验收 |
| Codex 0.166.0 / AGY 1.5.2 / Pi 1.5.0 的本机 help | 支持非交互、结构化输出和各自的恢复参数 | help 成功不证明权限、身份或恢复成功 |
| 本机 Autoloop Codex 颜色试跑 | 已完成提问、回答蓝色、`turn.completed` | 尚未接入治理合同、Pi/AGY 或主控回传 |
| `readMessage` 内存探针 | `身份前缀\nFAILED: ...` 被解析为 `done` | 尚未验证局部修正方案 |
| 安装源码静态路径 | 失败计数上限 10；换会话与 worker 超时分支存在 | 没有进行崩溃/超时/失联故障注入 |

事实入口：Autoloop `worker/agents.ts:39`、`worker/worker.ts:328`、`kernel/decide.ts:120,318`、`worker/contract.ts:89`、`protocol/rules.ts`、`cli/main.ts:693`。行号仅辅助定位，以安装版本的符号和实际文件为准。

## Decisions

### 1. Reuse direct CLI calls; preserve product differences

2026-11-09 采用用户路径 A 的支持范围收敛方案：阶段 2–3 的自动入口候选仅 Codex + Pi。AGY 不作为本轮阶段 1 通过的前置条件，保留受限直调/手动回退；未证实完整权限时不得作为自动独立只读 Reviewer。1.5.2 的动作拒绝/超时和 Pi 符号分析只作历史证据，当前版本1.5.3不继承运行验收。未来纳入AGY自动入口须另补针对当前版本的动作拦截或裁剪证据。此选择不修改全局只读义务，也不把工具名称列表本身当权限执行结果。

复用当前主控的命令执行能力与既有审阅流程，不创建通用派工框架。调用时记录具体可执行文件、版本、cwd、必要账户目录和 assignment；不记录凭据。

- Codex 使用 `exec` / `exec resume` 及 JSONL；`-p` 是 profile。恢复命令通过进程 cwd 与支持的 `-c` 设置权限，不能照搬新会话专用参数。
- Pi 只读审阅至少核对 `--no-mcp --no-extensions --tools read,grep,find,ls`，不得额外加载写工具扩展。R1 取得会话后，R2 使用已核实存在的精确会话目标；不存在即拒绝，不使用最近会话或允许静默创建的恢复路径。
- AGY 的 `--conversation`、结构化输出、有限 `--print-timeout` 分别验收。`--mode plan --sandbox` 是待验证候选，不预先称为可靠只读隔离，不使用权限绕过参数。
- 精简上下文只减少无关自动发现，必要的角色、范围和治理条款必须明确传入。未具备能力时报告具体 BLOCKED，不能静默换产品或放宽权限。

### 2. Session identity is checked before execution and after output

contract-local instance、native session、Autoloop run/card 是不同标识，复用既有合同/证据承载身份，不新增 canonical schema 字段。任何附加运行元数据只用于观测，不授权身份或状态。

对于已绑定且要求续接的受控调用，每次真正启动 CLI 前重新读取适用合同及当前 revision，核对角色、允许范围、期望 native session 与实际传入目标。获准的首次调用按有效角色与范围创建会话，记录实际 native ID；Standalone Lightweight 不因此新增 Handoff 或 canonical assignment。恢复要求遭调度器清空、会话不存在、上一轮 `unknown` 或独立性不成立时，拒绝启动。仅在结果返回后比对 ID 不能阻止错误实例已经执行任务，故后验检查是额外的证据接受检查。

`started` 只表示 CLI 已实际接收本轮，不作为禁止重试的策略开关。`read(stdout, code, stderr)` 没有 Turn 参数且插件可能缓存复用，不通过共享的“最近一次 Turn”保存逐任务身份。

### 3. Review, VERIFY and evidence writers have separate permissions

只读 Reviewer 读取允许材料、输出审阅正文；受控调用侧保存原始输出并据实际身份生成产物。固定测试由获准执行端按明确命令运行，允许的临时文件和结果目录单独列明；不因任务叫 VERIFY 就授予任意业务写入，也不要求 Pi 的纯读取工具运行 shell。

宿主不得冒充 reviewer 或 control-plane 签署结论。保留原始终态输出、原生身份、被测源码/合同指纹及执行命令；只能由实际有权实例完成其 evidence role。模型摘要、退出码 0 或无 warning 都不能代替有效报告与验证。

### 4. Transport completion is not governance success

只有实际检查结束且有效报告落盘，才可由调用侧明确输出“报告已交付，治理结论 FAIL/BLOCKED”等传输完成信息。产物内容、退出原因和回执分开，不修改全局身份前缀规则，不宽泛剥离模型正文，不把未完成任务伪装成成功报告。

以下限制必须通过可执行机制和故障证据证明，不能用 Prompt 声明代替：

- 该批次的失败/复查次数遵守其现有合同及用户任务类型；业务 VERIFY FAIL 不重跑、不转 FIX。
- 期望恢复的实例不得由 worker 或内核静默替换。
- CLI 错误、调用侧崩溃/被杀、worker 自身超时与失联 `unknown` 分别处理；unknown 不等于确定失败或已取消。
- 较短的内层超时只覆盖调用侧仍存活且能完成终止、落盘和交付的情况。不得据此声称消除了引擎失败重派。

确定的缺省决定是：证据不足则后台治理入口保持禁用，继续直接 CLI。当前方案不授权修改引擎、新增常驻监督组件或伪造 `started`。若现有受支持接口不能满足约束，停止阶段 2，明确缺口；选取新机制须修订设计/范围并重新取得相应批准。

2026-11-09 按 `tasks.md 2.3` 与本节约定，在阶段 2 初探报告 `BLOCKED` 经独立 Pi 审查通过（`evidence/pi-phase-2-review-receipt.json`）后，用户明确批准修订阶段 2–4 实现边界（记录于 `approval-amendment-phase2-unblock.json`）：

- 在不修改 `~/.agent-autoloop/app/**` 引擎源码的前提下，采用【宿主侧持久化 Attempt/Session 账本 + 受控 Runner 主动调用 `agent-autoloop stop <run-id>`（或 `ownerClient().cancel(runId)`）】的外层受控适配器方案（源码位于 `openspec/changes/integrate-governed-cli-autoloop/adapter/{govpi/agent.ts,gov_runner.py,tests/*}`）：
  1. 当 Turn 1 发生 CLI 故障或被 `worker.ts:347` (`triedFresh`) 静默置空 `resume` 拉起 Turn 2，或被 `decide.ts:121` (`settleSession`) 因前序 `unknown` 置空 `resume` 时，外层 Runner 在启动 CLI 前由本地持久化账本检测到同 `run-attempt` 二次 Turn 或 `resume` 丢失/冲突，立即落盘 `report-abort.md` 并以 `exit 0` + 正常回执（`"执行中止：会话续接被拦截，已生成中止报告，禁止重跑"`）结束，直接阻断 `triedFresh` 与 `retryLater`；结果后若 native session 与绑定不一致，同样落盘 `report-abort.md` 并以 `exit 0`（`"执行中止：结果后会话身份不符，已生成中止报告，禁止重跑"`）结束；
  2. 当发生外层 worker timeout 或封装进程异常（如 `SIGKILL` `exit 137`）导致内核进入 `retryLater`（`attempt >= 2`）时，外层 Runner 在 `attempt >= 2` 启动前检查本地账本，若该治理批次不允许重跑（`allow_rerun: false`），立即主动调用 `agent-autoloop stop <run-id>` 取消当前 Run、落盘 `report-abort.md` 并拒绝启动 CLI；
- 所有阶段 2–4 探针与运行证据目录固定在持久化路径 `/Users/elvis/.local/state/governed-cli-autoloop/integrate-governed-cli-autoloop/`（不再使用重启即清理的 `/var/folders/.../T/`）。

### 5. Return to the actual bound controller

`codex queue --thread <exact-native-id> --message <bounded-envelope> --resume` 仅为待验证回传入口。显式使用绑定主控的账户目录和项目 cwd；线程与账户映射须有证据，不从产品名称或当前 shell 推断。

信封引用当前 change/batch/attempt、报告路径/哈希及合同 revision/哈希，不承载可覆盖授权的指令。路径必须在该次获准证据范围内，不能用事件正文引导任意文件读取。主控重新读取真实状态与报告，验证身份、哈希、新鲜度和已有规则后，才可能接受证据或迁移状态。

入队、尝试恢复、目标主控实际消费、治理接受四种事实分别记录在既有证据中，不新增 lifecycle 状态。重复信封只核对已有接受记录，不重复执行业务或推进。缺少消费证据时如实报告等待人工恢复，不因命令 exit 0 或无 warning 声称自动闭环。当原绑定 Codex 主控线程因平台/模型下线（如 TUI 不支持 `gpt-6.1-sol`）、桌面应用会话占用锁或额度耗尽无法直接恢复，且用户明确授权将本 change 的阶段 4 收尾交接给指定 Pi 实例时（记录于 `approval-amendment-phase4-pi-closeout.json`），由获准 Pi 实例以只读方式（`?mode=ro`）从 `queue_1.sqlite` 读取并核验该线程已入队的受控信封、全部产物 SHA-256 及前序状态，落盘阶段 4 交接验收记录并交独立 Pi 审查实例复核通过后完成本 change 收尾（不修改全局 `CCG-001` 规则，不执行 `openspec archive` 或 Git 写操作）。

### 6. Source ownership and rollback

后续插件只从受版本管理的独立源码安装；`add` 用仓库名决定插件目录和 `use`，一个仓库根入口不会自动安装多个子插件。源码位置、根入口、安装路径、受影响运行时和精确版本必须先进入获批文件清单，不能把安装目录当唯一真源。在严禁 Git 写操作的约束下，本 change 阶段 2.4–3 的插件源码归属固定为本 worktree 下 `openspec/changes/integrate-governed-cli-autoloop/adapter/{govpi/agent.ts,gov_runner.py}`，通过文件复制安装到 `~/.agent-autoloop/plugins/govpi/{agent.ts,gov_runner.py,install.json}`（`use: "govpi"`），不触发 `agent-autoloop add` 的 `git clone`。

回滚先停止新增派发，使用 `agent-autoloop stop <run-id>` 处理本批次在途任务，核实状态与进程退出，再恢复规则/插件版本并重启受影响 worker 清除缓存。保留审计记录，不承诺零残留；不触及其他任务、凭据或 Skill 安装副本。

## Four phases and bounded file ownership

已获批实施；本轮仅收口阶段1的 Codex + Pi 支持子集。后阶段不得越过前阶段和自身的证据门槛。

| 阶段 | 工作与完成证据 | 文件边界 |
|---|---|---|
| 1. 直接调用 | Codex + Pi 受限调用、准确续接、权限、宿主截止与终态结果；AGY未验收能力显式排除，失败明确回报 | disposable fixture 与证据目录；若恢复已规定的命令示例，候选仅为 Router 的 `references/agent-capability-routing.md`、`references/approved-implementation-workflow.md`、`docs/engineering-invariants.md`、现有 `tests/test_workflow_rules.py`，以及 Companion 的 `references/agy-dispatch-template.md` 与对应现有测试；实施前固定实际所需子集 |
| 2. 后台机制证明 | 在持久隔离目录证明身份/重试约束，含宿主故障与 unknown；验证插件源码归属、安装、`stop` 排空、清缓存与回滚审计 | `openspec/changes/integrate-governed-cli-autoloop/adapter/{govpi/agent.ts,gov_runner.py,tests/*}`、持久探针目录 `/Users/elvis/.local/state/governed-cli-autoloop/integrate-governed-cli-autoloop/`、临时演练与回滚的 `~/.agent-autoloop/plugins/govpi/` 及 `~/.agent-autoloop/rules.json`（先备份、演练后回滚恢复），不修改 `~/.agent-autoloop/app/**` |
| 3. 一个 VERIFY 批次 | 固定测试命令、有效报告、业务失败不修复、canonical status 保持不变 | 已获准的持久证据目录与 `openspec/changes/integrate-governed-cli-autoloop/evidence/`；显式手动事件规则 `gov-pi` / `gov.verify.*` 在 `~/.agent-autoloop/rules.json` 中先备份、单批次执行后随 `2.4` 回滚恢复；使用只读 Pi（`amd-radeon/DeepSeek-V4-Flash`）避免消耗 `codex-a` 额度；不接定时、业务修复或 Git 操作 |
| 4. 主控回传 | 四级返回证据及重复消息不重复推进；或原主控受阻时经用户明确授权由指定 Pi 实例只读核验队列信封并完成本 change 收尾 | 原绑定主控线程队列（只读核验 `?mode=ro`）、`approval-amendment-phase4-pi-closeout.json` 及获准证据路径 |

明确不改：两份主 `SKILL.md`、`next_action.py`、核心 validator/state schema、全局 AGENTS/GEMINI、conda、ai_app 依赖、安装引擎，以及现有未决工作树候选。运行态安装/同步不是 proposal 准备权限。若后续修改受控可移植文件，仍走原有同步门禁，不能手工复制绕过。

## Acceptance and verification

当前 proposal 检查：`openspec validate integrate-governed-cli-autoloop --strict`；Pi 实例只读完整四文件及相关机制，调用前后比对工作区状态和文件 SHA-256。报告只评价提案，不声称后台集成已验收。

后续仅五组关键真实验收，具体命令随受测 CLI 当前 help 和获批 fixture 固定，未固定前不得开始相应执行：

1. 当前受支持的 Codex + Pi 精确续接：R1 保存 nonce、R2 核对原上下文和实际 native ID；缺失目标拒绝启动，换 cwd 不误创建。
2. 职责与权限：只读 Review 写入诱导被拒绝，工具清单与前后状态/文件哈希一致；VERIFY 仅运行固定命令并允许指定产物写入。
3. 失败与终态：业务 FAIL、CLI 错误、内层超时、调用侧被杀、worker 超时/unknown、首行前缀；无虚假 PASS，无越限业务执行或未经批准换会话。
4. 一个 VERIFY 报告：真实命令/原始输出、schema-2 证据、角色及 64 位 SHA-256 对齐；executor 不修改 canonical status；回滚实际排空并清缓存。
5. 主控回传：可恢复与不可恢复两种情况，原主控真实读取并核验证据；重复投递不重复执行/推进。

五组不是全量跨产品笛卡尔矩阵，不新增超过五个测试的授权。需要扩大测试或实现范围时显式修订范围。未来若改治理源码，仍必须运行原有 quick validation、core gates、完整 unittest 和相关 forward evidence；本轮只改提案制品，不以未运行这些实现检查宣称实现通过。

## Alternatives and approval boundary

直接 CLI 保留为默认和可用退路；通用 `use: command` 不满足原生身份/权限/恢复证明，不能直接承载正式治理批次。仅 Prompt 限次、强制 started、全局去前缀及新建通用 runner 均不采用。未知的引擎扩展不被隐含批准。

本 change 已取得实施批准及2026-11-09支持范围收敛授权；Review 只作证据，不扩张该授权。阶段 2 若不可行，交付真实阻碍，不扩大为 fork 引擎或修改全局配置。
