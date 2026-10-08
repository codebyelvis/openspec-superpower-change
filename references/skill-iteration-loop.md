# Skill Iteration Loop

本协议把现有 Self-Evolution 门禁收成一轮可续跑过程。
一条口令只执行本 skill 仓库一个切片，结束即停，不进入无限自治。

## Entry commands

以下任一口令进入本协议，大小写与空格不敏感：

- `迭代优化skill`
- `迭代优化这个skill`
- `iterate this skill`
- `optimize skill closed loop`

附切片名时只做指定切片，例如 `迭代优化skill：落地迭代入口`。
Major 的实现口令为 `迭代优化skill：已批准 <change-id>`；须核对具体
已批准 OpenSpec change 与范围，不能把口令中的任意字符串当作有效批准。
无切片名时取 `docs/iteration/BACKLOG.md` 中最高优先级且未阻塞的一项。

## Authorization

| Level / approval | Authorized next action |
|---|---|
| Patch / Minor | One slice: edit, validate, local sync, commit and push this repository's current branch. |
| Major without `已批准 <change-id>` | OpenSpec change draft and review plan only; stop awaiting approval. No implementation. |
| Major with `已批准 <change-id>` | Implement only the specific approved OpenSpec change and scoped contract. |

Never push another repository.
No force-push, history rewriting, or remote branch deletion.
The command does not approve a Major change-id that does not yet exist.

口令不授权业务项目改动、削弱 Non-negotiables、自动升级 Superpowers 或
OpenSpec 上游、发布 npm 或宣称 skills.sh 上架成功；分发可见性仍是异步的。
Git 租约仅覆盖本切片的 add、commit 和本仓库当前分支 push，一轮结束即终止。
其他路径的 push 禁令不变；所有原有审批、证据、Review 与用户控制边界保留。

## One-round sequence

1. 读取仓库 `SKILL.md`、本协议、`references/self-evolution-rule.md`、
   `docs/iteration/BACKLOG.md` 与 `docs/iteration/CURRENT.md`。
   只按当前决策加载相关规则，不通读全部 references。
2. `CURRENT.md` 有未完成轮次时先恢复该轮，不新开；否则按指定切片或
   backlog 优先级选择一个切片并写入 CURRENT。
3. 声明 Self-Evolution / Gate 0，按实际影响分类；不确定按 Major。
   Major 先产出 OpenSpec change 草稿与审查计划，停在待批；只有具体
   `已批准 <change-id>` 的范围才进入实现。
4. 实现前创建结构化临时备份，记录恢复路径。备份不得放在 skill 发现目录。
5. 只改本切片允许的文件与行为。触发范围、OpenSpec/Superpowers 边界、
   证据签发、完成权声明仍属 Major；若碰到这些边界就停在提案，不能夹带。
   不改变跨 CLI 目标名单，不重复实现已有门禁与分发适配。
6. 按 Self-Evolution 执行 quick_validate、`scripts/validate_core_gates.py`
   与受影响 unittest；路由或 description 变更跑现有 unittest 全套。
   quick_validate 使用带 PyYAML 的 Python，项目验证与测试也须通过
   dependency-free fallback。Major 须有 RED/GREEN forward-test；
   保留原有 profile 对应的 Review 与完成条件。
7. 便携核心或治理块变更时读取 `references/sync-checklist.md` 和
   `references/cross-cli-sync.md`，执行 plan → 审查 → 授权范围内 apply →
   verify-all。目标仍是 Codex、Pi、Antigravity、Grok；失败记 BLOCKED，
   不跳过，不扩大同步范围。CURRENT 记录审查过的同步计划哈希。
8. 验证、Review 和所需同步通过后，更新 CHANGELOG Unreleased，标记切片
   done，追加 LOG，清空或归档 CURRENT；然后只提交本切片文件并推送
   本仓库当前分支。提交信息沿用既有风格，正文写切片 id。
9. 推送成功后删除本轮临时备份。推送或其他必需步骤失败时保留恢复所需
   备份，CURRENT 记录非空阻塞原因与恢复动作，不宣称完成，不开启下一项。
10. 报告只含：做了什么、验证与同步结果、commit、backlog 下一项、
    下一句口令。成功后下一句可为 `迭代优化skill：收敛 Superpowers 选择证据`；
    未完成时下一句恢复当前切片。

## Persistent state

- BACKLOG：每项记录 id、优先级、Patch/Minor/Major、来源、完成定义与状态。
- CURRENT：记录当前 change-id、切片 id、备份路径、验证命令与结果、
  同步计划哈希、commit、阻塞原因；未完成轮次优先恢复。
- LOG：追加式，一轮一行，字段为日期、切片、结果、commit、残留。

状态记录不替代 OpenSpec、现有证据或 Completion Contract，不签发新的完成权。

## Iteration candidate capture

本节只收录本 skill 自身的后续优化候选，不替代
`learning-candidate-pipeline.md` 的 scope 分类或
`project-learning-closeout.md` 的项目知识晋升；已触发的必需晋升照常执行。
业务项目的 task-local / project-local 教训不能仅因重复就升级为全局 skill 规则。

Self-Evolution 或 Review 修正中，两个以上独立信号指向同一机制和适用范围时，
在本轮已授权的仓库文件范围内向 `docs/iteration/BACKLOG.md` 追加一条候选。
同一来源的转述、同一 finding 的反复提醒、同一失败的重跑不算独立信号。
未达阈值时保留当前 Plan/Review 中的证据，不为凑数建立 backlog 项。
高严重度事件仍走已有学习门禁，本节不新增也不降低其批准条件。

收录步骤：

1. 按同一机制、范围和拟议目标查重；已存在时只向该候选补充脱敏证据，
   不重复建项、不改既有状态或优先级。与现有规则冲突时标记候选 `blocked`，
   保留双方证据，交回控制面或用户决定。
2. 新项使用下一个空闲 S 编号，排在现有项之后；保留所有已有项的范围、
   优先级和推进约定。写齐 BACKLOG 六列，状态为“candidate／待用户选片；
   暂不实现”，类别按拟议实际影响填写；不确定或涉及受保护边界为 Major，
   状态为“Major／待提案，暂不实现”。
3. 在 BACKLOG 对应详情中使用
   `../templates/learning-candidate-template.md` 的字段子集：`status`、
   `event_kind`、`severity`、`scope`、`symptom`、`correction_or_evidence`、
   `generalized_invariant`、`independent_reproductions`、`independence_rationale`、
   `duplicate_or_conflict_result`、`target_artifacts`、`mechanical_enforcement`、
   `review_result`、`decision_owner`、`decision_provenance`。
   只保留摘要、项目相对证据路径及已有 SHA-256，不复制对话或 Review 原文，
   不保存凭据、客户数据或私有提示词。
4. 追加候选不覆盖 CURRENT，不插入或扩展当前切片，不自动合入 SKILL.md，
   不自动改写规则，不触发候选的运行时同步、Git 或生产操作。
   候选先等待用户后续选片；未选片候选不参与无切片口令的自动取项。
   Major 的实现仍须具体 change-id 批准。
   收录本身不授予提案审批、证据签发、学习晋升或完成权。

### Example: correction signals to a backlog candidate

以下是隔离示例，不是实际发现，不加入真实队列。两个独立来源分别记录
一次相同机制的修正：一个 Self-Evolution 验证发现示例文件的相对导航断链，
另一份独立 Review 在另一个示例中发现同一断链机制。完成当前授权修正后，
把“示例导航回归覆盖”收为后续候选，不顺手扩展本轮实现。

示例行（`S<n>` 在真实收录时替换为下一个空闲编号；优先级排在既有项之后）：

| id / 切片 | 优先级 | 类别 | 来源 | 完成定义 | 状态 |
|---|---|---|---|---|---|
| S<n> 示例导航回归覆盖 | 既有项之后 | Minor | 下方两项独立修正证据 | 后续独立切片用隔离示例验证相对导航可解析 | candidate／待用户选片；暂不实现 |

对应详情沿用 Candidate Card 字段子集：

```yaml
status: candidate
event_kind: correction
severity: low
scope: project-local
symptom: 两个独立示例的相对导航断链
correction_or_evidence:
  - tests/fixtures/example-a/review.md（隔离示例来源，非真实文件）
  - tests/fixtures/example-b/review.md（隔离示例来源，非真实文件）
generalized_invariant: 示例导航应在各自目录下解析到有效目标
independent_reproductions: 2
independence_rationale: 不同示例的独立验证与 Review，不是同一 finding 的转述或重跑
duplicate_or_conflict_result: 示例假定未发现重复或冲突；真实收录须先核对
target_artifacts:
  - docs/iteration/BACKLOG.md
mechanical_enforcement: required
review_result: pending
decision_owner: codex
decision_provenance: 当前控制面仅收录候选；后续选片后按既有 Self-Evolution 流程分类验证
```

反例：同一个 Review finding 被提醒两次仍只有一个来源，不新增候选；
阈值达成也不意味着可以直接修改 SKILL.md 或实现 Major。
