# openspec-superpower-change

[English](README.md) | [简体中文](README_cn.md)

`openspec-superpower-change` 是一个 Codex Skill，用作 AI 辅助工程任务的变更准入入口。它把项目本地规则、OpenSpec 变更合同、Superpowers 执行纪律和基于证据的验证门禁连接成一个可重复执行的工作流。

核心目标很简单：当工作可能影响运行时行为、公开合同、安全、持久化、工作流路由或运维可见行为时，AI Agent 不能从用户请求直接跳到代码实现。

## 亮点

- 在任何状态改变工作开始前先分类请求。
- 区分 Review-only、Discovery First、OpenSpec proposal、Approved implementation、Direct Change 和 Self-Evolution。
- 判断何时必须使用 OpenSpec，并在获批前阻止实现。
- 将已批准工作路由到 Superpowers 的计划、TDD、调试和验证流程。
- 要求在推进或声明完成前输出 Step Evidence Gate 证据。
- 实施前要求对当前 revision 的 Plan/Brief 执行 Preflight Review。
- 当前外部协作使用 schema 6 与 schema 2 证据，绑定完整且不可变的 Reviewer
  Assignment；冻结的 schema 4/5 仅可做只读 legacy 审计，不能授权当前工作。
- Codex、Pi、Antigravity CLI 与 Grok CLI 在被指派的 executor/reviewer 角色上
  资格同等。产品名本身不授予权限；只有绑定的 Codex `control-plane` /
  `control-plane-high` 实例及合同拥有路由、证据接受、canonical state、归档与
  完成决策权。
- 每次 Review 推荐或请求都必须说明 purpose、具体产品、角色、能力 profile、
  独立性与结果权限。
- 区分平台权限、工作流范围批准与业务/生产批准；High Review 检查真实 diff、
  wiring、claim-to-mechanism 与独立探针。
- 增加只读 `backend-architecture-review` 专项路由，面向明确的后端方案/设计
  Review，以有界 finding 让 Review/Fix 收敛到最小且符合项目模式的修正。
- 提供轻量 Authorized Execution Continuity，支持长任务在 compaction、恢复或
  Agent 切换后从 canonical Plan/Status/Handoff 继续已批准工作，只在真实阻塞或
  完成时停止。
- 提供 allowlist 驱动的 Codex/Pi/Antigravity/Grok 运行时同步、版本化 managed
  governance block、逐目标恢复、四目标完成门与敏感类别拒绝。Pi 使用
  `${PI_CODING_AGENT_DIR}/skills`，managed block 位于
  `${PI_CODING_AGENT_DIR}/APPEND_SYSTEM.md`。
- 通过条件式 Domain Context Check，让语义清晰的任务保持轻量，只在领域语言或
  边界仍不清楚时进入 `grill-with-docs` 或便携 fallback。
- 在最终完成前，把高成本纠正与 Review finding 晋升为可发现的项目知识和可执行
  回归约束。
- 通过 Claim-to-Test Relevance Gate，将每条测试命令绑定到当前 acceptance 与已证明
  的 blast radius；无关的 frozen baseline 失败登记为
  `OUT_OF_SCOPE_PREEXISTING_DEBT`，不扩大任务范围。

## 治理精简模式

内建且默认关闭的 `governed-caveman-lite` profile 会精简普通 Router 表达，同时
保留专业、完整的句子。使用 `OpenSpec 精简模式：<任务>` 为当前会话启用，也可以
先单独发送 `OpenSpec 精简模式`；使用 `OpenSpec 正常模式` 关闭。

该 profile 只改变呈现方式，不依赖外部 Caveman Skill，也不会跨会话保存。治理
字段、审批、证据、关键命令以及安全文本不会被压缩或省略。

## 为什么需要它

AI Coding Agent 很有用，但在生产级仓库里常见的失败模式也很明确：

- 未读取本地项目规则就开始实现；
- 把任务清单当成已批准合同；
- 用测试层证据声明运行时行为已经正确；
- 对 API、持久化、安全或工作流变更绕过 OpenSpec；
- 在修改治理 Skill 时削弱治理规则本身；
- 外部 Agent 交接后丢失审批状态和风险边界。

该 Skill 将这些风险转化为明确的门禁、参考文件和验证检查点。

## 体系定位

| 能力 | 职责 | 归属 |
|---|---|---|
| 本地项目规则 | 仓库约束、review 落盘、handoff、提交规范 | 项目 `AGENTS.md` / 本地文档 |
| 项目知识 | 领域词汇、工程不变量、决策、学习来源与回归约束 | `CONTEXT.md`、项目文档/ADR、Candidate Card、测试/validator |
| OpenSpec | 变更合同、需求、场景、审批状态 | `openspec/` |
| Superpowers | 实施计划、TDD、调试、验证纪律 | Superpowers skills |
| Step Evidence Gate | 推进或声明完成前所需证据 | `references/step-evidence-gate.md` |
| Prompt / 外部批次 Review | 独立 prompt/diff Review 与 Handoff-backed Brief/Report/Review attempt | `codex-brief-antigravity-review` |
| 后端架构 Review | 面向明确后端方案/设计的只读专项证据，覆盖边界、合同、调用链、事务、性能、稳定性和过度设计 | `backend-architecture-review` |
| Authorized Execution Continuity | 基于 canonical Plan/Status/Handoff 的轻量长任务续跑，覆盖 compaction、恢复和 Agent 切换 | `references/approved-implementation-workflow.md` |
| openspec-superpower-change | 路由、风险分类、审批门禁、自我演进边界 | 本 Skill |

## 核心工作流

```text
读取本地规则
-> Gate 0 请求分类
-> Domain Context Check；仅在语言/边界仍未解决时使用 grill-with-docs
-> 分类任务阶段与实质选择
-> 按阶段、实质歧义和风险选择 Superpowers（通用创建/修改语义不足以触发）
-> 合同或高风险行为变化时创建 OpenSpec proposal
-> 停下等待审批
-> 为已批准实现创建 Superpowers plan
-> Plan/Brief Preflight Review；修订并循环到 PASS
-> 按 TDD / 调试 / 实施纪律执行
-> 对完整业务 slice 应用 Step Evidence Gate
-> 验证 -> Review -> 修正，循环到 Review PASS
-> Project Learning Closeout；晋升并验证/Review 必需项目知识
-> 持久化 fresh final verification 证据，再执行最终 diff/范围 Review
-> 对账/归档 OpenSpec，并执行归档后严格验证
-> 经授权的 Git 发布
-> 引用持久化项目产物的会话归档/蒸馏总结
```

## 长任务连续执行与 Review 收敛

- **Authorized Execution Continuity** 复用未变化且范围绑定的 canonical
  Plan/Status/Handoff 或等价状态。`continue` 只续跑下一项已批准任务，不重启已
  完成工作，也不创建第二套任务台账。
- Continuity 不授予新范围、凭证、生产权限或实质性的产品/业务/架构决策权。
  出现阻塞、新决策、范围扩张、资源缺失、显式暂停/取消或完成时停止；适用时记录
  owner 与 resume condition。
- **Backend architecture Review** 是明确后端方案/设计判断的专项路由，检查服务
  边界、合同、调用链、事务、性能/稳定性与过度设计。它只产生只读专项证据，不实施
  修复，也不决定 canonical Completion。
- Review 保持比例性：最多 3 个 material finding；每个都绑定 evidence、trigger、
  impact 与最小项目一致修正。可行动 finding 返回 `Fix -> Verify -> Review`；重复
  扩大范围或不收敛时返回 `BLOCKED`，不继续堆叠方案。

## 详细决策流程

决定性顺序如下：

```text
请求事实 -> Domain Context Check -> 阶段分类 -> 实质选择检查 -> 风险/证据
profile -> 被选中 Superpowers 的完整规则 -> 批准或执行 -> Project Learning
Closeout -> 最终验证/Review -> 归档 -> 经授权发布 -> 会话蒸馏
```

对受治理的状态变更、Git mutation 或整任务完成判定，Router 选择零个或多个
Superpowers 方法；用户无需逐一显式点名。显式点名方法不授予业务、Git、工作流
或完成权限，也不能绕过 Gate 0。Codex 上的 `using-superpowers` 仅允许显式调用，
Router 所需子技能在原生嵌套加载获得证明前仍保留 implicit matching。若没有受支持
的 Skill-load 路径/hash trace，实际 prompt 是否加载必须记为 `UNKNOWN`，不能从可见
行为反推。

| 阶段 | 必需行为 |
|---|---|
| 入口 / Gate 0 | 读取本地指令和受影响项目知识，分类当前请求，选择证据/能力 profile，并说明是否仍需确认。 |
| Domain Context Check | 当项目语言可能变化时，检查 `CONTEXT-MAP.md`、`CONTEXT.md`、相关 ADR、文档和代码。语言清晰则跳过 `grill-with-docs`；术语、参与者、边界、状态或生命周期仍不清楚时进入该 Skill，或使用完整便携 Discovery First fallback。 |
| Proposal-only | 先检查仓库事实与既有 spec。只允许可逆、显式的有界假设；严格验证 proposal/design/spec/tasks，并停下等待确切 change-id 批准。不能仅因请求含“创建/修改”就加载 planning、TDD 或 implementation Review。 |
| 实质选择 | 安全、兼容、破坏性迁移、数据生命周期、范围、生产授权与可测试验收仍由用户决定。用户把选择委托给 Agent，也仍需 brainstorming 及其完整 HARD-GATE。 |
| 已批准实施 | 刷新 Gate 0，创建可执行计划，对当前 revision 执行 Preflight Review，再对完整业务 slice 使用 TDD/调试与 Step Evidence Gate。任何 finding 都返回修复 -> 验证 -> Review。 |
| 外部 Handoff | companion 执行完整的当前 schema-6 Handoff 生命周期。Codex、Pi、Antigravity CLI 与 Grok CLI 都可承担被指派的 executor/reviewer；证据只有经绑定 Codex control plane 接受后才可推进 canonical state。 |
| Project Learning Closeout | implementation Review PASS 后审计纠正与 finding。达到自动阈值或用户显式要求归档并蒸馏时，必须晋升确认的项目级知识并建立回归约束。 |
| 最终化 | 学习晋升后才执行 fresh final verification，随后进行最终 diff/范围/敏感数据 Review、任务对账、OpenSpec 归档及归档后严格验证。 |
| 发布 | Git staging/commit/push 仍需独立授权。最终会话总结必须引用持久化仓库知识，不能成为唯一记录。 |

## 项目学习分层

同一条高成本经验可以生成多个小产物，但每个产物只承担一种职责：

| 知识 | 持久化位置 | 禁止放入 |
|---|---|---|
| 领域语言与语义关系 | `CONTEXT.md` / `CONTEXT-MAP.md` | 实现原因、事故时间线、任务列表 |
| 易忽略的实现或 Agent 不变量 | 仓库规则指定位置，默认 `docs/engineering-invariants.md` | 完整聊天/Review 原文 |
| 难以逆转且出人意料的真实取舍 | `docs/adr/NNNN-slug.md` | 普通或容易撤销的小修复 |
| 晋升来源 | `docs/learning-candidates/YYYY-MM-DD-<slug>.md` | 密钥、客户数据、私有 prompt |
| 可机械执行的行为 | 确定性回归测试或 validator | 仅靠文字声明 |
| 会话归档/蒸馏 | 引用上述产物的最终总结 | 成为唯一知识存储 |

同一项目不变量被两个独立纠正/Review 信号确认，或出现一次高严重度安全、
完整性、数据丢失或 false-PASS 事件时，必须自动晋升。用户显式要求归档并蒸馏
时，必须执行审计并晋升每个已确认的 project-local 关键点。必需晋升在完成 focused
verification 和 Review PASS 前阻断最终完成。

## 担忧与解决机制

| 担忧 | 机制 |
|---|---|
| 宽泛 metadata 带来不必要仪式 | 阶段优先规则 `CCG-014` 让受治理工作先进入唯一 Router；普通问答旁路 Router 与 Codex `using-superpowers` meta-entry。 |
| 显式点名 Superpowers 方法看似授予权限 | 它只选择工程纪律；工作流、业务、Git 与完成权限仍属于 Router Gate 0，无法加载唯一 Router 时 fail closed。 |
| 完全关闭 Superpowers 会丢失保护 | 只自适应选择是否激活；一旦选中，子技能完整规则保持不变。 |
| Agent 偷偷决定认证/兼容行为 | 用户拥有的实质选择仍必须 brainstorming 并获批准。 |
| `CONTEXT.md` 只是过期本地文件 | 共享权威 context 不得被故意 ignore，并必须进入 changed-file inventory。 |
| 高成本 bug 经验只留在聊天中 | Candidate Card + Project Learning Closeout + 正确持久化产物 + 回归约束。 |
| 外部 PASS 被误当最终完成 | Codex 保持 control plane；学习、最终验证、最终 Review、归档与同步门继续生效。 |

## 工作流优化决策（2026-07-30）

本轮评估最终选择 **方案 C：继续使用现有组合**。OpenSpec 保持唯一权威变更
合同，Superpowers 继续提供批准后的工程实施纪律，
`codex-brief-antigravity-review` 继续承担 standalone 与 Handoff-backed
Review 职责。

- 未删除任何 Superpowers Skill 或运行时副本。
- 未安装任何 `mattpocock/skills`；最终依赖闭包为空。
- 没有任何全局 Skill 满足永久删除条件。
- `mattpocock/skills` 中的 `tdd`、`diagnosing-bugs`、双轴
  `code-review`、领域 grilling 与 tracer-bullet Ticket 切分仍作为未来候选。
- 方案 A/B 仍受阻于 worktree 与 branch-finish 等价能力缺失、
  `implement` 的 Review/commit 顺序风险、Codex 兼容缺口，以及证据与生命周期
  门禁尚未达到等价。

### 如何理解“当前最优”

这里的“最优”有明确边界：它是本次固定版本、当前 Codex 环境和本项目治理
约束下，方案 A/B/C 中风险调整后的选择；不是对全行业工作流、未来版本或所有
开发场景的绝对排名。方案 A 表示完全替换 Superpowers，方案 B 表示仅保留最小
子集，方案 C 表示保持现有组合。本次主要比较跨项目治理闭环，而不是单项 Skill
的学习速度或某个技术栈的编码深度。

| 评价尺度 | 当前组合 | `mattpocock/skills` | 当前判断 |
|---|---|---|---|
| 单个低风险项目快速开始 | 概念和门禁较多，初始学习成本更高 | 单项 Skill 精简直接，更容易上手 | 候选更轻 |
| 多项目、多服务、跨技术栈长期维护 | 统一合同、风险、证据、Review 与完成规则；项目只需接入原生构建和测试命令 | 原样使用时仍需为各项目补齐授权、证据、分支与生命周期适配 | 当前组合更稳 |
| 审计与可复现性 | OpenSpec 版本、Handoff 身份、证据 freshness 和最终完成权责可统一核验 | TDD、调试、Review 等方法强，但没有同等的整体生命周期合同 | 当前组合更完整 |
| 技术栈专项能力 | 不替代项目自身框架、部署、安全和数据工具链 | 同样属于方法层，不自动提供项目专项能力 | 由项目原生工具决定 |
| 规模化维护成本 | 组件较多，但集中升级一次后可跨项目复用，固定成本随项目数量摊薄 | 单项维护简单；若承担完整治理，适配副本和项目差异可能逐步碎片化 | 单点采用候选更简单，组合治理由当前方案承担 |

因此，准确表述是：**当前组合是已评估方案中，跨项目、跨服务和跨技术栈工程
治理闭环的默认最优选择；`mattpocock/skills` 在单个低风险项目或孤立能力
场景更容易上手。** 后者并未被否定，仍作为 TDD、调试、双轴 Review、领域
澄清和垂直切片等能力的候选来源。只有出现可测量缺口和完整等价证据时，才应
通过新的 Self-Evolution change 选择性引入或替换。

### 第三方依赖如何保持更新

方案 C 不承诺“所有依赖永远自动升级到最新版本”。静默追随上游会破坏版本
可复现性，并可能在没有 Review 的情况下改变触发、权限或完成规则。这里要保证
的是**来源可追溯、过期可检测、升级经过验证、失败可以回滚**。

版本台账必须分别记录**已验证兼容基线、本机实际生效版本、上游最新观察版本
和安装渠道当前可用版本**。这些值可能不同：插件市场镜像可以落后于上游源码，
升级 Codex CLI 也不会自动升级独立 Git clone、软链或下载型 Skill。

| 安装方式 | 实际更新语义 | 必需动作 |
|---|---|---|
| 本项目维护的 source → runtime 副本 | Git 仓库是权威来源；运行时副本不会自行跟随 | 按 `references/sync-checklist.md` 同步并验证 parity |
| Git clone + Skill 软链 | 软链只传播本地 checkout 的变化，不会自动拉取官方更新 | 显式比较 upstream SHA，处理本地提交后受控更新 |
| Codex 插件市场安装 | 由插件管理器记录安装版本；不能仅凭官方发布推断本机已更新 | 用 `codex plugin list --json` 核验安装版本，按受支持的 marketplace 流程刷新，并在新会话验证 |
| `skill-installer` 下载的 Skill | 安装的是一个快照；目标目录已存在时 installer 会停止，不是原地 updater | 记录来源 ref/SHA，备份后显式替换或重装并重新验证 |

受控升级应完成以下闭环：

1. 记录安装方式、四类版本值、上游来源、软链目标和本地补丁。
2. 只读检测上游新版本，审查 release notes 与实际 diff；检测到新版本不等于
   自动批准升级。
3. 创建临时备份，在隔离副本或分支中处理本地补丁与上游变化。
4. 运行上游自带测试，以及 Router、Companion 的 validator、单元测试、必需
   Skill inventory/discovery 检查和真实行为 forward scenarios；仅有现有
   validator PASS 不能证明第三方兼容。
5. Review PASS 后才同步到运行时；启动新会话核验发现路径与实际版本。
6. 记录新版本、验证证据和回滚点。任何失败恢复旧版本并停止推广。

若依赖升级改变触发范围、OpenSpec/Superpowers 边界、证据门禁或完成规则，
它就是 Major Self-Evolution，必须先有获批 OpenSpec change。仓库目前没有宣称
存在自动依赖巡检器；在机械化 freshness check 落地前，维护时必须显式执行上述
检查，不能把“可发现 Skill”当成“已跟随官方最新版本”。

详见[完整评估](docs/design/2026-07-30-workflow-skill-optimization-evaluation.md)
与[独立 Review](docs/design/reviews/2026-07-30-workflow-skill-optimization-plan-c-archive-review.md)。
重新评估必须满足评估文档第 14 节的证据条件；实施 A/B 还需单独批准 Major
Self-Evolution change。

## 请求模式

| 模式 | 适用场景 | 是否改文件 |
|---|---|---:|
| Review-only | 用户要求本总入口评审架构、实施授权、风险或完成证据。 | 否 |
| 后端架构 Review | 用户明确要求评审后端方案/设计，覆盖边界、合同、调用链、事务、性能/稳定性或过度设计。 | 否 |
| Discovery First | 术语、参与者、生命周期或边界不清。 | 通常只改 glossary / context |
| OpenSpec proposal | 需要新增能力、行为合同、架构、安全、持久化、API 或工作流变更。 | 只改 proposal 产物 |
| Approved implementation | OpenSpec-backed proposal 已明确获批。 | 是，需先有计划 |
| Direct Change | 低风险恢复、拼写、格式、无行为影响文档、配置或既有行为测试。 | 是，范围受限 |
| Self-Evolution | 修改本 Skill、参考文件、校验器、示例或同步规则。 | 是，受门禁约束 |

在 proposal-only 起草阶段，如果仓库事实和有界假设足以形成可评审合同，Gate 0
可以不选择任何 Superpowers 子技能。如果因实质未决选择而选中 brainstorming，
其完整 HARD-GATE 仍然有效；实施获批后，计划、Preflight、TDD、Review、证据、
验证和归档门禁均保持不变。

独立 task prompt/Brief/checklist 编写和普通 diff/Report 只读 Review 归 `codex-brief-antigravity-review`；“Review 并修复”属于实施，必须回到本总入口。

## Gate 0

在编辑文件、运行状态改变命令、创建 proposal 产物或开始实现之前，Agent 必须说明：

1. 当前请求模式；
2. 已读取的参考文件，以及为什么足够；
3. 是否需要 OpenSpec；
4. 所需 Superpowers 子技能；
5. 风险级别、下一步动作，以及是否需要用户确认。

## OpenSpec 边界

以下场景必须使用 OpenSpec：

- 新功能或公开行为变化；
- API、schema、数据生命周期、持久化或迁移变化；
- 安全、沙箱、权限、跨租户行为或认证变化；
- Runtime 工具暴露、缓存策略、请求路由、Skill 路由或工作流生命周期变化；
- 改变系统边界的大范围重构；
- Skill 工作流变化。

只有在恢复既有预期行为、小型无合同影响配置变更、拼写/注释/格式修复、无行为影响文档更新，或为既有行为补测试时，才可以跳过 OpenSpec。

## 证据等级

| 等级 | 典型场景 |
|---|---|
| compact | 低风险文档、格式、配置或局部直接变更。 |
| standard | 默认的多步骤实现、评审和验证。 |
| strict | 安全、认证、公开 API/schema、持久化语义、迁移/写路径、部署/回滚、删除/恢复、跨租户行为或生产权限。 |

## 有界 Plan Preflight

一个 revision lineage 的首次 Plan/Brief Review 使用完整
`FULL_PREFLIGHT`。只有 reviewer identity 与不可变 parent Review 精确匹配且
不同于 author/executor、所有受保护边界不变、当前 whole-file path/SHA 与
parent-anchored 历史绑定有效且机械检查通过时，纯纠错 revision
才可使用 `FOCUSED_RECHECK`。同一 lineage 两轮 BLOCKED、reviewer 冲突、范围
扩张或未授权边界变化，进入有界 `CONTROL_PLANE_ADJUDICATION`；它不是第三种
Review mode 或生命周期状态。P0/P1、安全、完整性、权限、
scope/contract/risk/acceptance、虚假证据和不可执行 Plan finding 始终阻断。
可选建议与已接受残余风险必须分开记录。

证据强度保持比例化：compact 简洁验证，standard 保留独立 Review 与关键证据，
strict 保留真实证据和人工业务门禁。风险按 changed effects 判断；仅通过既有私有
只读持久化边界读取，不自动代表持久化语义发生变化。

## 仓库结构

```text
.
├── SKILL.md
├── references/
│   ├── request-modes.md
│   ├── local-instruction-checkpoint.md
│   ├── learning-candidate-pipeline.md
│   ├── project-learning-closeout.md
│   ├── openspec-decision-rule.md
│   ├── proposal-workflow.md
│   ├── approved-implementation-workflow.md
│   ├── direct-change-rule.md
│   ├── step-evidence-gate.md
│   ├── superpowers-adapter.md
│   ├── self-evolution-rule.md
│   ├── sync-checklist.md
│   ├── cross-cli-sync.md
│   └── cross-cli-portable-manifest.json
├── scripts/
│   ├── validate_core_gates.py
│   └── validate_cross_cli_sync.py
├── tests/
│   ├── test_workflow_rules.py
│   └── test_cross_cli_sync.py
├── openspec/
│   ├── project.md
│   └── changes/
├── examples/
├── templates/
│   └── learning-candidate-template.md
└── docs/
```

## 关键参考文件

- `references/request-modes.md`：工作模式与约束。
- `references/local-instruction-checkpoint.md`：本地规则与权威 context 持久性检查。
- `references/learning-candidate-pipeline.md`：候选范围、阈值与晋升权威。
- `references/project-learning-closeout.md`：项目知识目标、回归约束与完成阻断。
- `references/openspec-decision-rule.md`：何时必须使用 OpenSpec。
- `references/proposal-workflow.md`：proposal 创建与验证流程。
- `references/approved-implementation-workflow.md`：批准后的实施流程。
- `references/direct-change-rule.md`：低风险直接变更要求。
- `references/step-evidence-gate.md`：compact/full 证据模板。
- `references/superpowers-adapter.md`：OpenSpec-aware Superpowers 产物、权限和 Preflight 映射。
- `references/self-evolution-rule.md`：修改本 Skill 的规则。
- `references/sync-checklist.md`：运行时副本与开源副本同步规则。
- `references/cross-cli-sync.md`：四端 target、managed-rule parity、discovery、
  逐目标恢复与完成阻断规则。

## 安装

复制或链接到 Codex skills 目录：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R openspec-superpower-change "${CODEX_HOME:-$HOME/.codex}/skills/openspec-superpower-change"
```

## 验证

修改 Skill 后运行：

```bash
"${PYTHON_BIN:-python3}" "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" /path/to/openspec-superpower-change
PYTHONDONTWRITEBYTECODE=1 python3 /path/to/openspec-superpower-change/scripts/validate_core_gates.py /path/to/openspec-superpower-change
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s /path/to/openspec-superpower-change/tests -v
```

当前受治理状态使用 schema 6，并包含不可变 Reviewer Assignment。使用以下
命令验证其 schema-2 evidence manifest：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 /path/to/openspec-superpower-change/scripts/validate_core_gates.py \
  /path/to/openspec-superpower-change \
  --status /project/docs/agent-collab/<change-id>/status.md \
  --artifact-root /project
```

每个引用 artifact 都内嵌 schema-2 evidence manifest，绑定
role/result/change/batch/attempt/source fingerprint，以及被分配的 product、
instance、role 和 capability profile。引入新证据的 transition 应先在项目外
生成 proposed status，并加
`--previous-status /project/docs/agent-collab/<change-id>/status.md` 验证；
`complete` 强制要求该参数。仅在 PASS 后替换唯一 canonical status，项目内
不得持久化第二个 marker block。

冻结的 schema-4/schema-5 记录只能作为 legacy audit/drain 输入。必须单独
盘点，不得交给当前 `--status` 校验，也不得迁移成 schema 6：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 /path/to/openspec-superpower-change/scripts/validate_core_gates.py \
  /path/to/openspec-superpower-change \
  --legacy-inventory-root /project \
  --legacy-inventory-output /private/tmp/legacy-drain.json
```

`quick_validate.py` 需要 PyYAML；请通过 `PYTHON_BIN` 选择可用解释器。项目 validator 和测试会覆盖无 PyYAML fallback。

便携核心 Skill 发生变化时，还必须使用
`scripts/validate_cross_cli_sync.py` 生成仅含路径/哈希的计划，并在获得明确
授权后逐端 apply/verify，完成 discovery/parity 与仅报告路径/类别的敏感审计。

## 示例 Prompt

```text
Use openspec-superpower-change review-only mode. Read local rules, inspect this implementation plan, and report whether it requires OpenSpec. Do not modify files.
```

```text
Use openspec-superpower-change as the entry gate. Decide whether this requires Discovery First or an OpenSpec proposal before implementation.
```

```text
Use Direct Change mode. Confirm this restores intended behavior, make the smallest fix, run verification, and report evidence before claiming completion.
```

```text
Use backend-architecture-review for a read-only Review of this backend proposal. Inspect the actual project code and report only material boundary, contract, transaction, performance, stability, or over-design findings.
```

```text
Continue the approved task from its canonical Plan/Status/Handoff state. Do not restart completed work, create a second ledger, or expand scope without a new decision.
```

## 维护说明

- 每次发布仓库更新时同步更新 `README.md` 与 `README_cn.md`，确保用户可见
  行为、决策、验证结果与兼容性说明保持一致。
- 不得削弱审批门禁、证据门禁或完成声明规则。
- 不得让 OpenSpec `tasks.md` 替代 Superpowers implementation plan。
- 不得让 `CONTEXT.md` 替代 OpenSpec proposal 产物。
- 当确定性约束可行时，不得让必需项目学习只留在聊天、Review 输出或纯文字中。
- 不得用目录级覆盖同步运行时副本和开源副本；必须使用 sync checklist。
- 不得完成“已验证但未 Review”的工作；Review 发现问题必须重新修正、验证和 Review。
- OpenSpec-backed 工作存在未对账任务，或尚未完成适用的归档及归档后验证时，不得声明合同闭环。

## License

MIT. See [LICENSE](LICENSE).
