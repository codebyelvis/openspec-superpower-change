# S8 项目文档归属治理能力 — Major 审查草稿

作者：elvis。日期：2026-10-08。修订：draft-v1。
change-id：`add-project-document-ownership`。状态：仅提案，待具体批准。

## Gate 0 与当前授权

- 模式：Self-Evolution / proposal-only；分类 Major，拟议实施风险 strict。
- 已读：唯一迭代合同 §0、§3、§6，仓库 SKILL/AGENTS、迭代协议、
  Self-Evolution、Proposal Workflow、项目学习收尾、相关模板/验证器/测试、
  当前 BACKLOG/CURRENT、CONTEXT 与相关既有学习 spec；无嵌套 OpenSpec AGENTS。
- OpenSpec 必需：增加文档创建/迁移的路由规则，改变无约定项目的默认学习目标。
- Superpowers：none；目标及验收已经明确，本轮只起草工件，不加载实施方法。
- 当前只可新增本草稿、该 change 的 proposal/design/tasks/spec delta、
  S8 提案验证记录，并更新 CURRENT 与 BACKLOG 的 S8 状态。
- 不实现、不移动现有文档、不改 manifest、不写运行时、不执行 Git
  add/commit/push、不做生产操作；不重做 S1–S7。
- 下一动作：完成并严格校验 draft-v1，等待用户批准具体 change-id 与范围。
  实施前必须实际记录该批准；当前“闭环”与既有通用编辑权限不能替代它。

## 观察到的问题

用户报告业务项目的部署说明、工程经验散落在 docs 根目录；本轮没有访问
业务仓库，也不将该报告冒充已完成的行为回放。本仓库的可复核证据是：
`references/project-learning-closeout.md` 的 Target resolver 明确默认到
`docs/engineering-invariants.md`，Candidate Card 模板重复此默认值，
`validate_project_learning_gate` 和相关测试也绑定了旧默认文本。

本仓库 AGENTS 明确要求读取 `docs/engineering-invariants.md`，属于显式
位置契约，不能因改通用默认值而迁移。CONTEXT、OpenSpec、协作状态、
迭代状态也已有位置和引用契约。此前 S7 只解决续跑，不能借 S8 重写它。

## 期望行为与规则归属

普通项目文档创建或本次授权迁移前，先看任务范围内的目录/导航约定。
明确用户/项目位置契约优先，其次复用已有用途/领域约定，缺少约定才使用
合理用途子目录。允许项目已有目录位于 docs 之外，不强制统一结构。

规范正文集中到现有 `references/project-learning-closeout.md` 的独立
`Project Document Ownership` 小节；入口仅导航到该小节。读取归属小节
不会自动触发知识晋升或整套学习收尾。Target resolver 引用同一规则，
无约定工程经验默认改为 `docs/engineering/engineering-invariants.md`。
Template 只指向 resolver，避免维护第二份目录规则。

## 拟议实施文件与排除项

后续具体批准后，仅拟改：

- `SKILL.md`：新增必要的归属小节导航，不扩大 frontmatter 触发范围。
- `references/project-learning-closeout.md`：规范归属小节及 resolver 默认值。
- `templates/learning-candidate-template.md`：改为引用 canonical resolver。
- `scripts/validate_core_gates.py`：归属规则的 artifact-bound 检查。
- `tests/test_workflow_rules.py`：相关负例、实际文件与链接断言。
- `CHANGELOG.md`、本 change 工件、S8 专属审查/脱敏证据和迭代状态。

排除：AGENTS/CONTEXT 本体、已有工程经验文档、OpenSpec 主 spec 及历史
change、协作状态与 S7 规则、其他 skill/companion、共享治理块、manifest、
跨 CLI 目标清单、生成分发物、依赖、业务仓库和任何无关历史文档。
本仓库已有文档不迁移；迁移能力在隔离合成项目验证。若必须触及排除项，
停在 Major 范围修订及重新批准，不纳入当前切片。

## 精确拟议规则片段（本轮不写入运行规则）

入口路由新增一行：

```markdown
| Create or relocate project documentation | `references/project-learning-closeout.md` (Project Document Ownership only) |
```

归属小节与开头导航拟加入：

```text
For document creation or authorized relocation, read Project Document Ownership
only. Reading it does not activate learning promotion or completion gates.
Existing learning-closeout triggers and required promotion remain unchanged.

Before creating or relocating an ordinary project document, resolve its purpose
or domain from scoped project instructions, relevant indexes/navigation and
nearby documents. An explicit user/project path contract wins; otherwise reuse
an established purpose/domain convention. Directory presence alone does not
prove a convention. With no convention, use a suitable purpose subdirectory,
such as docs/deployment/, docs/engineering/, docs/incidents/ or
docs/learning-candidates/. Reserve the docs root for index entry points and
explicitly contracted paths. Conflicting contracts or equally plausible
destinations require resolution; neither recency nor this default decides them.

Keep AGENTS.md, CONTEXT.md and its existing map, OpenSpec artifacts,
collaboration status and iteration-state files at their contracted locations.
Do not use ordinary document organization to rewrite bound approval/evidence
artifacts or override their existing owner, hash, transition or completion rules.

Relocate only explicitly authorized documents and the authorized reference
closure identified before the move. Repair relative inbound/outbound links,
agent navigation and applicable active references in the same change, retaining
document content except the required link edits. Do not move unrelated history,
follow a destination outside the bound project, overwrite a conflicting file,
or silently edit an unauthorized referring file. An incomplete authorized
reference closure blocks relocation until resolved through the existing gate.
```

Resolver 工程经验行的拟议默认目标：

```text
repository-defined guidance selected through Project Document Ownership;
with no explicit path or established convention,
docs/engineering/engineering-invariants.md
```

Template 对应规则拟改为：

```text
Choose durable knowledge targets through the canonical Target resolver and
Project Document Ownership in references/project-learning-closeout.md;
keep domain meaning, engineering invariants and ADR decisions in their own roles.
```

## 验证与 forward-test 计划

本轮只做新 change strict、quick/core 双解析及相关既有治理回归，检查
新增工件链接和允许文件范围，确保 44 个既有无关工作区文件及运行规则未改。
不把这些结果称作 S8 行为已实现、RED/GREEN、独立 Review 或同步 PASS。

具体批准后，先记录旧行为 RED，再实现并取得 GREEN。使用当前测试体系
及私有临时项目，读取/写入实际文件并检查内容、相对链接/锚点和范围快照；
不得用无工具的路由回答或仅规则文字作为实际文档行为证据。三个原生场景：

1. 现有 `docs/ops/` 部署约定与显式根目录工程经验契约优先，受保护文件不变。
2. 无约定的新项目创建部署说明和工程经验，落在用途子目录；入口仍只读匹配小节。
3. 明确授权的合成部署文档迁移，修复入链/出链与 AGENTS 导航，内容保留，
   无关历史/CONTEXT/OpenSpec/协作状态/迭代状态不变；授权引用闭包缺项时停手。

确定性负例另覆盖同级目的地歧义、目的地冲突/项目外链接、错误根目录默认、
规则挪到 Template 导致伪 PASS、链接断裂及未授权引用变化。断言检查实际
文件与解析结果；原生工具审计确认没有 off-scope 写入。只保留脱敏结果。

实施后的必需检查：quick（PyYAML）、core 和现有 unittest 全套（PyYAML
及无依赖解析各一次）、new change strict、实际 RED/GREEN 与链接检查。
便携文件变化须按既有四端同步协议审查 plan、核对授权、apply、verify-all；
没有相应授权就 BLOCKED，不以源仓库 PASS 代替同步完成。

## 审查计划与回滚

后续严格路径保留独立 Preflight、Implementation Review、distinct Final
Review。产品均拟为 `codex`，模型 gpt-6.1-sol，high；purpose 分别为
plan-preflight/implementation-review/final-review，role 均为
`independent-reviewer`，profile `control-plane-high`，authority
`governed-review-evidence`。实施前绑定实际 reviewer instance IDs 与 author/executor
身份；Preflight 与实现独立，Final 与实现及 Implementation Reviewer 独立。
未派发前不制造 assignment、签名或 PASS；缺少符合条件实例则 BLOCKED。
Router 保留唯一转换/完成权。审批后再按已批准合同写 canonical 执行 Plan。

提案备份：`/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/openspec-S8-proposal-4xkas497`。
包含 CURRENT/BACKLOG 等源文件快照、44 个无关文件基线 SHA-256 和只读运行时
快照；在待批期间保留，位于 skill 发现目录之外。

提案撤回只从该备份恢复本轮 CURRENT/BACKLOG，并删除本轮新建 S8 工件；
不得覆盖其他工作区变化。未来实施前重新建立当前源/运行时结构化备份，
运行时恢复走审查过的既有事务，不使用当前提案快照覆盖后续用户变化。
