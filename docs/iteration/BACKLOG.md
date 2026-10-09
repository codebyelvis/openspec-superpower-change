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
| S8 项目文档归属治理能力 | 7（候选，排在既有项之后；待用户下一步指令） | Major | 用户补充优化项：项目文档归属治理能力 | 见下方 S8 候选详情；独立切片完成提案审批、隔离行为验证、链接检查、审查及必要同步 | Major／draft-v1 已批准；原 Preflight BLOCKED 保留，S9 绑定前置已解决，待下一轮 fresh changed-binding Plan／Preflight readiness，未实现 |
| S9 续跑证据分阶段审查者绑定 | 8（新增候选，排在既有项之后；待用户选片） | Major | S8 独立 Preflight F1 与控制面隔离复现；见候选证据 | 后续独立提案解决 strict 续跑与分阶段 reviewer 绑定的兼容冲突，保留批准、不可变合同、身份独立及分阶段完成门禁；具体验收须经独立提案批准，不扩入 S8 | done；已批准实施、独立门禁／原生／四端／归档严格校验 PASS；主提交 605a099 已推送，收尾元数据／清理待完成；S8 仍 blocked、未实现 |

S2 及以后只排队；不得重开方案 C、变成 session-start always-on、合并
mattpocock/skills 或 oso、自动发布 npm、把搜索可见性当完成条件或放宽
Major change-id 批准。

## S8 候选详情：项目文档归属治理能力

状态：**Major／待提案，暂不实现**。当前授权仅为收录候选；实施须等待
用户下一步指令及具体 change-id 批准。不授予 manifest 修改、运行时同步、
Git 提交／推送或生产操作权限；不纳入当前 S1 轮次，不改变 S1–S7 的范围、
优先级及推进约定，不覆盖 CURRENT。

2026-10-08 用户追加指定口令“迭代优化skill：S8 项目文档归属治理能力
（仅提案）”，本次只将候选推进为 `add-project-document-ownership`
draft-v1，并在此前 idle 的 CURRENT 记录 S8 待批轮次。上段保留候选收录
时的授权来源；本次仍不授予实施、manifest 修改、运行时同步、Git
提交／推送或生产操作权限。S1–S7 的条目、优先级及推进约定均不变。
审查草稿：`docs/review/2026-10-08-S8-project-document-ownership-draft.md`；
具体批准前不标 done，不将提案校验视作行为验收。
draft-v1 的新 change strict、quick/core 双解析及相关既有回归通过；
记录：`docs/review/2026-10-08-S8-project-document-ownership-proposal-validation.md`。

2026-10-08 用户发送具体已批准口令，S8 draft-v1 批准已记录于
`openspec/changes/add-project-document-ownership/approval.md`。独立
FULL_PREFLIGHT `docs/review/2026-10-08-S8-preflight-full.json` 为 BLOCKED：
现有 S7 续跑 context 的单一不可变 reviewer assignment 不能表示已批准的
不同 Implementation/Final 实例。改变该绑定属于排除的证据/生命周期边界；
S8 不放宽 scope、risk、independence，也不夹带 S7 修复。当前只完成批准/
备份/Plan/诊断，未编辑实施规则，未运行 S8 行为 GREEN 或同步/提交/push。
普通 Plan F2/F3 细节已补齐，尚未取得有效 Preflight PASS。

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

## S9 候选详情：续跑证据分阶段审查者绑定

收录阶段仅为未来候选，不覆盖 S8 CURRENT、不扩大 S8 切片。2026-10-09
按用户“后续都闭环推进不要再问我”及“继续闭环推进”的持续指令，自行
将当前已明确的 S8 前置问题推进为具体审查草稿和待批 OpenSpec；不修改
S7/证据/完成规则。S8 批准及通用继续授权不能批准 S9 实施。

```yaml
status: blocked
event_kind: review-finding
severity: high
scope: global
symptom: strict 本地续跑仅有一个不可变 reviewer assignment，无法接受合同要求的不同实现与 Final reviewer
correction_or_evidence:
  - docs/review/2026-10-08-S8-preflight-full.json（F1，独立阶段绑定矩阵）
  - docs/review/2026-10-08-S8-major-prerequisite-conflict.json（控制面真实文件完整转换复现）
generalized_invariant: 续跑与完成证据应能表示已批准的各阶段独立审查身份，不能以复用同一实例或替换不可变 context 来冒充满足合同
independent_reproductions: 2
independence_rationale: 独立 reviewer 直接测试阶段绑定矩阵；控制面另建文件测试完整进入/完成转换及 context 替换，非 finding 转述或同一失败重跑
duplicate_or_conflict_result: S1-S8 无同范围候选；与当前 S7 单 assignment 规则冲突，保留两方证据；S9 draft-v1 已具体化，实施等待该合同批准
target_artifacts:
  - docs/iteration/BACKLOG.md
  - openspec/changes/support-stage-specific-resume-review/{proposal,design,tasks}.md
  - openspec/changes/support-stage-specific-resume-review/specs/skill-workflow-governance/spec.md
mechanical_enforcement: required
review_result: blocked
decision_owner: codex
decision_provenance: 用户持续闭环指令允许完成当前前置问题的具体待批提案；S8 原批准及通用闭环/编辑权限不授权实施 S9 受保护变更
```


### S9 draft-v1 提案进展（2026-10-09）

- change-id：support-stage-specific-resume-review；Major／仅提案，未批准实施。
- [审查草稿](../review/2026-10-09-S9-stage-review-binding-draft.md)；
  [唯一设计合同](../../openspec/changes/archive/2026-10-09-support-stage-specific-resume-review/design.md)。
- 推荐 strict-local 分阶段 assignment 加显式受限的 blocked context 修订；
  legacy/standard/compact/external 保持，普通 context 仍不可变。
- 该方案及 S8 唯一元数据修订须具体 S9 批准；未改规则/测试或旧 S8 合同，
  不授予 S8 readiness、实现、完成或本轮同步/Git 权限。
- 新 change strict 已通过；其他提案校验见
  [提案验证记录](../review/2026-10-09-S9-stage-review-binding-proposal-validation.md)。
- S1–S8 的范围、优先级、完成状态和批准不变；S8 CURRENT 保留未完成轮次。


### S9 draft-v1 已批准实施（2026-10-09）

用户具体口令“：迭代优化skill：已批准 support-stage-specific-resume-review”
已核对四份合同并记录在现有 S9 review draft 的 Specific Approval Record。
本轮只实施 S9，S8 仅走已批准的受限 context 元数据转换；其原批准/范围/
独立 Final 不变，实施仍等待前置完成后的新 readiness。
执行 Plan：docs/review/2026-10-09-S9-implementation-plan.md；源/运行时新备份
已建，独立 Preflight 已 PASS，源 RED/GREEN 与原生实际文件场景通过，
独立 Implementation Review 与四端同步 PASS，受限 S8 元数据转换已落盘；
S9 实际 final 输入集的 Implementation re-Review 与单独 Final Review 已 PASS；归档／Git／清理尚待。通用继续不再重复询问；具体新 scope 仍受原门禁。


### S9 门禁及源发表结果（2026-10-09）

仅已批准 S9 实施。quick/core 双解析、全套各 461 项、实际原生 RED/GREEN、
独立 Preflight／Implementation／amended-input re-Review／单独 Final、四端两文件
scoped sync／discovery／verify-all 及归档 exact-byte strict 均 PASS。
源提交 `605a09937df3f8acb7762ba2277a97d2203e5e59` 已推送 main，远端已核对。
S9 canonical complete revision 8 绑定实际 persisted final 7；旧 Review 和批准未改。
S8 guarded 修订只建立新分阶段 context 及 blocked revision 5，verified=null；
原 11 个 S8 工件不变，整个原图及新 context/status 本轮均未提交。CURRENT
恢复 S8 fresh changed-binding Plan／Preflight 待办；不把 S8 实现夹入 S9。
本次收尾元数据推送及 S9 自有备份／trace 清理待完成；S8 两份备份保留。
