## ADDED Requirements

### Requirement: Verified native CLI invocation within existing routing

本轮自动入口候选 SHALL 限定为 Codex、Pi，并分别核验其真实可执行入口、
版本、参数、工作目录、必要环境、终态输出和超时行为。CLI 帮助、文本断言、
历史调用成功 SHALL NOT 代替当前目标路径的运行证据。调用 SHALL 保留已有
schema-6 产品、实例、角色、profile 和独立性分配；产品名称不授予主控权限。
短任务 SHALL 保持已有默认直调及手动降级入口；普通实现、typo、格式、注释、
非契约文档、已授权同范围继续修改和单独只读审阅 SHALL NOT 因接入 autoloop
而自动加载 Router 或后台流程。所需治理上下文 SHALL 按当前任务保留。

AGY SHALL 保留为受限直调/手动回退，不作为本轮阶段1通过的前置条件；
未经当前版本权限验收 SHALL NOT 纳入阶段2–3自动只读入口。AGY静态工具列表
不裁剪本身 SHALL NOT 被宣称为越权执行；也不得仅因单次动作拒绝而宣称完整只读。

#### Scenario: Native flags differ between products

- **WHEN** 同一受控任务选择 Codex、Pi 或 Antigravity CLI
- **THEN** 调用使用该产品已验证的非交互和精确恢复参数，不机械共享 `-p`、
  sandbox 或最近会话参数
- **AND** 目标 CLI 不可用或能力未验证时报告明确边界，不静默换产品或放宽权限

#### Scenario: Ordinary lightweight request remains lightweight

- **WHEN** 用户只要求普通 typo 修正或独立只读审阅
- **THEN** 原有窄触发与 Standalone Lightweight 边界继续生效
- **AND** 不因 CLI 调用便利而新增 Handoff、后台任务或全量 reference 加载

### Requirement: Exact session identity before every native launch

对于已绑定且要求续接的受控调用，每次真正启动 CLI 前 SHALL 从当前有效的
canonical assignment 与任务证据取得期望恢复目标，核对本次实际收到的
session、工作目录及精确会话定位。获准的首次调用 SHALL 按其有效角色与范围
创建会话并记录实际 native ID；Standalone Lightweight SHALL NOT 因本要求
新增 Handoff 或 canonical assignment。
要求原实例续接时，目标缺失、被清空、身份不符或执行状态未知 SHALL 阻止启动，
不得回退最近会话或静默创建新实例。终态返回后 SHALL 再核对实际 native session
与原绑定；后验判废 SHALL NOT 被宣称为已预防错误实例执行。原生 session、
contract-local instance 与 autoloop run/card 标识 SHALL 保持各自含义。

#### Scenario: Required reviewer session is unavailable

- **GIVEN** `FOCUSED_RECHECK` 要求继续原 reviewer 实例
- **WHEN** 精确会话不存在，或调度器在派工后清空了本次恢复目标
- **THEN** 启动前检查拒绝该轮，并向主控报告 `BLOCKED`
- **AND** 不用新会话沿用原 reviewer 身份；有效前序证据和复查次数上限不变

#### Scenario: Previous execution state is unknown

- **WHEN** 同一绑定会话的前次执行仍运行中或已失联且完成状态未知
- **THEN** 调用保留未知事实，先核实前次执行，再决定是否允许恢复
- **AND** 不把失联等同于安全重跑，不并发进入同一会话或自动清空绑定重开

### Requirement: Role-specific permissions and host-owned evidence output

只读 Review SHALL 仅暴露经验证的读取能力，显式处理 MCP、扩展和产品原生
权限差异；`access: read` 或 Prompt 本身 SHALL NOT 被当作跨产品通用沙箱。
VERIFY SHALL 只执行已批准的验证命令，并限定所需临时目录和产物写入范围。
受控调用侧 SHALL 从真实输出保存报告和哈希，模型只读权限不得为此升级为
完整写权限。现有 schema-2 证据与 schema-6 assignment SHALL 继续匹配；
宿主观测报告不得冒充主控或独立 reviewer 的签署。

#### Scenario: Review tool selection leaves writable tools exposed

- **WHEN** Pi 工具白名单仍保留 MCP 或扩展写工具，或 AGY 的只读隔离未经验证
- **THEN** 该调用不能宣称只读 Review 就绪，必须收紧并验证实际暴露能力
- **AND** 不使用跳过权限或 `full` 作为修复，不删除任务必要治理上下文

#### Scenario: Verification requires commands and report files

- **WHEN** VERIFY 需要运行测试并生成证据，而模型只读工具不支持执行或写文件
- **THEN** 由已批准的受控执行侧运行固定命令并落盘真实结果，或报告能力阻塞
- **AND** 验证失败只交事实和证据，不自动升级为 FIX，不修改业务源码或 canonical 状态

### Requirement: Proven bounded transport without false completion

后台接入 SHALL 区分传输交付与治理结论。只有检查确实结束且有效报告已交付时，
传输层才可记录完成；报告可为 `PASS`、`FAIL` 或 `BLOCKED`，均不因此自动重做。
未执行、报告缺失、部分流输出、固定身份前缀或历史 PASS SHALL NOT 被解释为当前
任务通过。不得伪造 `started` 或依赖 Prompt 改写内核策略。

治理批次启用前 MUST 证明每次实际执行遵守其已有重试上限和禁止换实例要求，
覆盖 CLI 错误、封装自身异常或终止、worker 超时及未知执行状态。较短的内层
超时只可证明封装能够捕获并交付的路径，不能证明覆盖所有外层故障。现有机制
不能满足这些条件时 SHALL 保持该后台能力禁用并交回主控决定；不得以重试十次、
失败回执中的 `ask` 或新建会话绕过已有熔断与权限边界。经用户明确批准修订范围后，
在不修改 `~/.agent-autoloop/app/**` 引擎源码的前提下，外层受控适配器 SHALL
通过宿主侧持久化 Attempt/Session 账本与受控 Runner 实现上述边界：当 `worker.ts`
(`triedFresh`) 或 `decide.ts` (`settleSession`) 导致 `resume` 丢失或冲突时，在
启动 CLI 前落盘 `report-abort.md` 并以 `exit 0` 及正常中止回执结束以阻断
`triedFresh` 与 `retryLater`；当外层 worker timeout 或封装异常进入 `retryLater`
(`attempt >= 2`) 且批次禁止重跑时，在 `attempt >= 2` 启动 CLI 前主动调用
`agent-autoloop stop <run-id>` 取消当前 Run 并拒绝启动 CLI。

#### Scenario: Identity prefix precedes a failure conclusion

- **WHEN** 模型原始输出的首行是身份前缀，后续才是失败或无操作结论
- **THEN** 受控结果处理保留原始输出，并从已验证的当前终态结果生成传输摘要
- **AND** 不把前缀当完成证据，不宽泛删除模型正文或默认修改全局身份规则

#### Scenario: Outer failure escapes the shorter timeout

- **GIVEN** 内层时限短于 autoloop worker 时限
- **WHEN** 封装被终止、未能交付有效报告，或 worker 自身超时而产生重派路径
- **THEN** 该路径必须有经验证的执行边界，阻止超出原治理授权的重复执行或换实例
- **AND** 缺少此证据时不启用治理批次，不伪造正常报告掩盖未知或未完成的执行

### Requirement: Bound control-plane delivery and evidence acceptance

后台返回 SHALL 使用原绑定主控的 native thread、账号环境及项目范围，并携带
现有批次、attempt、revision 和证据路径/哈希所需的最小信息。消息入队、线程恢复、
主控消费、证据接受 SHALL 分别报告；`queue --resume` 退出码为零或没有 warning
不证明后续步骤成功。只有绑定 Codex control-plane（或当原 Codex 线程因平台模型限制/桌面会话锁无法恢复且经用户对本 change 明确书面授权交接时的指定 Pi 收尾实例）SHALL 按原 schema-6 合同与
既有 validator 接受证据并推进本 change 状态；`next_action.py` SHALL 保持只读
查询，调度记录 SHALL NOT 成为第二份治理状态。人工卡片回答仅对相应决定有效，
不得扩大范围或授予 Git、生产、凭据、发布及破坏性操作权限。

#### Scenario: Queued message does not wake its owner

- **WHEN** `codex queue --resume` 成功退出，但目标线程未恢复或没有实际消费报告
- **THEN** 状态仅报告已证实的投递阶段，并提供原主控的人工恢复入口
- **AND** 不转投其他账号或线程，不声称证据已接受或任务已完成

#### Scenario: Duplicate or stale completion notification

- **WHEN** 同一批次和 attempt 的通知重复到达，或其 revision/产物哈希已失效
- **THEN** 主控依现有 canonical 状态与磁盘证据去重或拒绝过期结果
- **AND** 不重复执行业务或推进状态，不因通知正文写有 PASS 而跳过验证与 Review

### Requirement: Staged enablement and reversible runtime installation

实施 MUST 在用户明确批准 `integrate-governed-cli-autoloop` 的具体契约后开始。
后续启用 SHALL 按顺序完成：当前支持子集的直接调用验收、隔离试跑中的传输边界证明、
一个手动触发的 VERIFY 后台批次、原主控回传与验收。每阶段只能在前序通过且
自身授权有效时开始。插件 SHALL 在明确的源码真源维护；安装目录与 `use` 必须一致，
在禁止 Git 写操作的约束下可从 worktree 受管源码目录复制安装而不触发 `git clone`，
不手改安装目录引擎源码。阶段 2–4 的探针与运行证据目录 SHALL 固定在持久化路径，
不放在系统重启即清理的临时目录。不得扩大为通用编排框架或变更既有 schema、
主控所有权、完成契约、全局规则及源/runtime 同步权限。

回滚 SHALL 停止新派发，排空或显式停止本次在途任务并确认进程退出，恢复已知
规则/插件版本，重启受影响 worker 清理缓存并验证运行状态。审计记录按既有策略
保留，不宣称删除插件目录即可零残留回滚。

#### Scenario: Proposal review passes before implementation approval

- **WHEN** proposal 严格校验和独立 Pi 只读 Review 通过
- **THEN** 只可报告契约制品已准备好，等待用户对具体 change 的实施批准
- **AND** 不安装插件、修改运行时规则、改写 Skill 或启动业务批次

#### Scenario: Roll back a cached plugin with work in flight

- **WHEN** 本次插件需回滚且 worker 已缓存 adapter 或仍有在途任务
- **THEN** 使用实际支持的 `agent-autoloop stop <run-id>` 发出必要停止请求，并核实
  取消状态及进程退出，再完成版本恢复、worker 重启与状态验证
- **AND** 不使用不存在的 `cancel` CLI，不把停止请求响应当成已停，不删除审计记录
