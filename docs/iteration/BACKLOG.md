# Skill Iteration Backlog

来源合同：`docs/requirement/openspec-superpower-change-iteration-plan.md` 第 4 节。
用户指定的第 7 节补充当前存于同目录 `openspec-superpower-change-iteration-plan (1).md`；仅收录 S7，不替换原合同或扩大 S1 实现范围。
按优先级从小到大，每轮只取一项；未完成 CURRENT 优先恢复。

| id / 切片 | 优先级 | 类别 | 来源 | 完成定义 | 状态 |
|---|---|---|---|---|---|
| S1 迭代入口本身（落地迭代入口） | 1 | Minor；触发边界变化升 Major | 合同 §3、§4 S1；补充 §7 仅收录 | 固定口令进 description 与路由；协议与三份状态文件存在；S2–S6 入队，S7 为待提案；验证覆盖路由、Major 批准及 push 范围；本地 SKILL 一致；本仓库提交推送；报告下一口令 | done |
| S7 项目实施也能关窗接力 | 1.5（S1 之后、S2 之前） | Major | 用户指定合同补充 §7 | 后续独立一轮先产出 OpenSpec 提案与状态迁移表；单 agent 与外部 handoff 共用 docs/agent-collab/<change-id>/，瘦状态为 schema 6 子集；停手前记录状态、已完成、唯一 next_action、阻塞与 resume_condition，新会话按持久状态续跑；最佳状态绑定最近验证通过且已落盘的 revision；继续闭环／闭环推进不授予 Git push、生产写入或新批准；多个未完成 change 时询问用户，不自动挑选；无已批准 change-id 不实现 | done；add-project-session-resume 已批准实施，源／原生／四端／独立审查与归档严格校验通过，主提交已推送，临时备份／trace 已清理 |
| S2 收敛 Superpowers 选择证据 | 2 | Minor；Router 选择权边界变化升 Major | 合同 §4 S2，Unreleased Router 选择规则 | 用已有 forward-test 与缺失 fixture 覆盖普通问答不进 meta-entry、proposal-only 不加载 TDD/planning、点名方法不授予 Git/完成权、低风险 Direct Change 方法集为空；失败先红后绿；不增加默认加载的 skill 正文 | done |
| S3 迭代候选进入 backlog 的窄管道 | 3 | Minor | 合同 §4 S3，Project Learning Closeout | 同类 Self-Evolution/Review 修正信号两次以上时只追加候选；用现有 learning-candidate-template 字段子集；有规则与示例；无新自动改写器，不自动合入 SKILL | done |
| S4 过触发成本的静态预算 | 4 | Minor | 合同 §4 S4，按行读取约束 | 协议中增加本轮允许阅读表；轻量 validator 拒绝入口要求先读完全部 references；不改业务证据门禁 | done |
| S5 skill 自改的工作区隔离说明 | 5 | Patch 或 Minor | 合同 §4 S5，真源/生成物/运行时区分 | 协议说明仓库根是真源，distribution 与嵌套 SKILL 是生成物；起轮确认真源，运行时仅 sync apply 写入；不引入新的 worktree 强制命令 | done |
| S6 上游对照节奏，而不是自动升级 | 6（季度） | Minor | 合同 §4 S6，sync-checklist 上游边界 | 对照 Superpowers/OpenSpec/Spec Kit 入口形状，仅更新 docs/iteration/upstream-notes.md，提供笔记模板与“笔记不是升级批准”规则；可采纳项另开切片，不改依赖 | done（2026 Q4；下一对照窗口 2027 Q1） |
| S8 项目文档归属治理能力 | 7（候选，排在既有项之后；待用户下一步指令） | Major | 用户补充优化项：项目文档归属治理能力 | 见下方 S8 候选详情；独立切片完成提案审批、隔离行为验证、链接检查、审查及必要同步 | Major／待提案，暂不实现 |

S2 及以后只排队；不得重开方案 C、变成 session-start always-on、合并
mattpocock/skills 或 oso、自动发布 npm、把搜索可见性当完成条件或放宽
Major change-id 批准。

## S8 候选详情：项目文档归属治理能力

状态：**Major／待提案，暂不实现**。当前授权仅为收录候选；实施须等待
用户下一步指令及具体 change-id 批准。不授予 manifest 修改、运行时同步、
Git 提交／推送或生产操作权限；不纳入当前 S1 轮次，不改变 S1–S7 的范围、
优先级及推进约定，不覆盖 CURRENT。

背景：业务项目新生成的部署说明、工程经验散落在 docs 根目录；现有
`references/project-learning-closeout.md` 默认目标 `docs/engineering-invariants.md`
也会持续产生这个问题。

目标能力（仅描述后续拟议能力，本轮不执行）：

1. 创建项目文档前先识别已有目录约定，按用途或领域归属，优先复用现有
   目录，不强制所有项目采用同一结构。
2. 无约定时使用合理的用途子目录，例如 deployment、engineering、incidents、
   learning-candidates；docs 根目录保留索引入口和用户／项目契约明确指定的文件。
3. 文档迁移同步修正相对链接、AGENTS 导航及相关有效引用；只整理本次授权
   文件，不自动搬迁无关历史文档。
4. 保留 AGENTS.md、CONTEXT.md、OpenSpec 工件和协作状态文件各自已有的
   位置契约，不用通用目录规则覆盖它们。
5. 学习收尾的默认工程经验目标调整为用途子目录中的文件；规则集中维护，
   SKILL.md 只保留必要导航，不复制多份正文。

后续独立切片验收：

- 已有目录约定优先；无约定时不把普通新文档散落在 docs 根目录。
- 显式根目录契约及 OpenSpec／协作状态路径不被误迁移。
- 迁移后引用可解析，文件内容保留，无关文件不变。
- 使用隔离场景与链接检查验证实际行为，不仅检查规则文字。
- 按现有 Self-Evolution 流程完成提案审批、测试、审查及必要同步。
