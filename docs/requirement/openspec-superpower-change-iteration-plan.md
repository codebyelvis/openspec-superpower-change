# openspec-superpower-change 长期迭代入口与下一轮优化合同

状态：可直接交给 Codex / 任意已加载本 skill 的 agent 执行。
真源仓库：https://github.com/codebyelvis/openspec-superpower-change
适用对象：本地主力 skill `openspec-superpower-change` 本身，不是业务项目。
编写日期：2026-10-08

本文件是下一轮实施合同，也是之后所有轮次的入口说明。落地后，用户不必再为每一轮单独生成任务提示词。

## 0. 给执行 agent 的使用方式

收到本文件，或之后收到固定口令，都按同一协议做 **一轮**，不要展开成无限自治，也不要顺手改治理语义。

固定口令（任一即进入，大小写与空格不敏感）：

- `迭代优化skill`
- `迭代优化这个skill`
- `iterate this skill`
- `optimize skill closed loop`

口令只授权 **本 skill 仓库的一轮闭环**。不授权业务仓库改动，不授权削弱 Non-negotiables，不授权 force-push、改写历史、删除远程分支。

若口令附带切片名，只做该切片。例如：`迭代优化skill：落地迭代入口`。
若口令附带已批准 change-id，Major 才可进入实现。例如：`迭代优化skill：已批准 add-skill-iteration-loop`。
没有切片名时，从 `docs/iteration/BACKLOG.md` 取优先级最高且未阻塞的一项。

一轮结束必须留下可续跑状态。下一轮任何人只要再说一次口令即可继续。

## 1. 定位：这个 skill 不是又一个 harness

市面高星项目大多是「模型外面的运行时」或「SDLC 技能包」。本 skill 是项目级变更闸门：在请求和实现之间插入分类、合同、证据和完成权。不要把它改成第三个 Superpowers，也不要把它改成 Spec Kit 克隆。

| 项目 | 量级（2026-10 公开口径，约数） | 它解决什么 | 对本 skill 的取舍 |
|---|---|---|---|
| obra/superpowers | ~296k stars | 会话级工程纪律：brainstorm、plan、TDD、debug、review。session-start hook 让技能默认进入 | 继续当执行器，不合并进本仓库。它的 always-on hook 正是过触发来源。本仓库 Unreleased 已把 `using-superpowers` 收成 explicit-only、Router 独占方法选择。不要回退 |
| github/spec-kit | ~141k stars | constitution + 显式命令面（specify/plan/tasks/implement/converge），扩展/preset | 借「显式口令 = 一个有界过程」，不借八阶段仪式。迭代入口应对齐这个形状 |
| Fission OpenSpec | ~58k–69k stars | 变更增量：explore / propose / apply / archive，30+ agent 适配 | 已是本 skill 的合同层。skill 自身的 Major 演进继续走 OpenSpec change，不另造合同格式 |
| BMAD-METHOD | ~54k stars，skills.sh 安装量更高 | 多技能编排；`bmad-build-auto` 是一轮无人值守迭代；另有 retrospective | 借「一轮迭代」而不是「一直跑」。借 retrospective 的形状写迭代日志 |
| OpenSpec+Superpowers bridge（moyaspace/oso 等） | 低 stars | worktree 隔离，避免并行改同一工作区 | 本 skill 自改时可选 worktree，避免改到一半污染正在使用的运行时副本 |
| Hermes 一类 learning loop | 产品向，非本场景直接依赖 | 经验沉淀成 skill | 已有 `learning-candidate-pipeline` 与 Project Learning Closeout。迭代入口应消费候选，而不是另起学习系统 |
| OpenCode / Codex CLI / Pi | harness 本体，10万–20万 stars 量级 | 工具、沙箱、会话 | 只通过已有 `cross-cli-sync` 同步运行时。不在本仓库重写 harness |

2026-07-30 已选定方案 C：保持 OpenSpec + Superpowers + review skill 的组合。本计划不重开这个决策。

已落地、本轮禁止重复实现：

- Gate 0、proposal-only、Domain Context Check 条件触发
- Superpowers 方法由 Router 选择；`using-superpowers` explicit-only
- Completion Contract、schema-6 reviewer assignment
- Codex / Pi / Antigravity / Grok 的 cross-cli sync、receipt、verify-all
- Self-Evolution 的 Patch / Minor / Major 分级、备份、forward-test
- skills.sh / SkillsMP / Pi npm / Codex plugin 分发适配

## 2. 真正的缺口

Self-Evolution 已经规定「改这个 skill 要走门禁」，但没有把长期优化收成可重复的一轮。

现在每次优化都要人工重写任务提示词，因为仓库里没有：

1. 一个写进 `SKILL.md` description 的固定口令，让任意已加载本 skill 的 agent 识别。
2. 一份持久 backlog 和当前轮状态，让下一轮不用重新调研整个仓库。
3. 一口令对应的授权租约：本地运行时同步 + 本仓库 commit/push。今天 git push 被硬禁止，除非用户另批；所以闭环在最后一步断开。
4. 一轮的完成定义：验证、同步、推送、回写 backlog、删除临时备份、给出下一句口令。

缺口不是「再加更多闸门」，而是「把已有闸门收成一个可续跑的入口」。

## 3. 第一刀：落地迭代入口

这是下一轮唯一必做切片。做完之前不要开始第 4 节的实质优化。

### 3.1 要新增的文件

- `references/skill-iteration-loop.md`：本协议的规范正文。agent 读到口令后只读这一份，外加 backlog 和 self-evolution-rule。
- `docs/iteration/BACKLOG.md`：长期切片队列。每项含 id、优先级、类别（Patch/Minor/Major）、来源、完成定义、状态。
- `docs/iteration/CURRENT.md`：当前轮。空模板即可；有轮次时写 change-id、切片 id、备份路径、验证命令、同步计划哈希、commit、阻塞原因。
- `docs/iteration/LOG.md`：追加式轮次记录。一轮一行：日期、切片、结果、commit、残留。

`SKILL.md` 只加路由，不把协议正文塞进入口文件。description 增加一句：用户说「迭代优化skill」或等价口令时，进入 skill 自身迭代闭环，读取 `references/skill-iteration-loop.md`。

路由表增加一行：迭代口令 → `references/skill-iteration-loop.md`，并仍受 `references/self-evolution-rule.md` 约束。

### 3.2 一口令一轮的步骤

执行 agent 按顺序做，做完即停。

1. 读 `SKILL.md`、`references/skill-iteration-loop.md`、`references/self-evolution-rule.md`、`docs/iteration/BACKLOG.md`、`docs/iteration/CURRENT.md`。不要通读全部 references。
2. 若 `CURRENT.md` 有未完成轮次，先恢复该轮，不新开。
3. 否则取口令指定切片，或 backlog 中最高优先级且未阻塞的一项。写入 `CURRENT.md`。
4. 分类：
   - Patch / Minor：口令本身就是这一轮的编辑、验证、本地同步、本仓库 push 授权。
   - Major：先产出 OpenSpec change 草稿和审查计划，停在待批。只有口令写明 `已批准 <change-id>` 才实现。不确定就当 Major。
5. 实现前做结构化临时备份。备份不得留在 skill 发现目录。
6. 只改本切片范围。触发范围、OpenSpec/Superpowers 边界、证据签发、完成权声明，仍是 Major。
7. 验证：quick_validate、`scripts/validate_core_gates.py`、受影响的 unittest。路由或 description 变更跑现有 unittest 全套。Major 要有 RED/GREEN forward-test。
8. 便携核心或治理块有变更时，走 `references/cross-cli-sync.md`：plan → 授权范围内 apply → verify-all。目标仍是 Codex、Pi、Antigravity、Grok。失败是 BLOCKED，不是跳过。
9. 验证和需要的同步通过后：更新 CHANGELOG Unreleased、把切片标成 done、追加 LOG、清空或归档 CURRENT。然后在本仓库提交并推送当前分支。提交信息使用仓库既有风格，正文写切片 id。
10. 推送成功后删除临时备份。报告只含：做了什么、验证与同步结果、commit、backlog 下一项、下一句口令。

口令不等于：

- 批准一个尚未存在的 Major change-id
- 推送本仓库以外的仓库
- 发布 npm / skills.sh 上架成功声明（分发可见性仍是异步的）
- 自动升级 Superpowers 或 OpenSpec 上游

### 3.3 与现有规则的衔接

`references/self-evolution-rule.md` 里「没有明确用户批准不得 push」保留，但增加一条：固定迭代口令是对本仓库一轮 push 的明确批准。其他路径的 push 禁令不变。

`AGENTS.md` 同步这一条例外，避免 agent 读到旧禁令后停在推送前。

Non-negotiables 不改。迭代入口不能用来放宽审批、证据、Review 或用户控制边界。

### 3.4 这一刀的完成定义

- 固定口令写进 `SKILL.md` description 和路由表。
- 四个新文件存在，且 BACKLOG 已填入第 4 节切片。
- 现有 validator 覆盖：口令路由存在、Major 无 change-id 时不得出现实现承诺、push 范围限于本仓库。
- 本地 skill 副本与仓库根 `SKILL.md` 一致。
- 本仓库已提交并推送。
- 报告末尾给出下一句口令，例如：`迭代优化skill：收敛 Superpowers 选择证据`。

## 4. 入口落地后的实质切片

按这个顺序放进 BACKLOG。每次口令只取一项。

### S1 迭代入口本身

类别：Minor，除非实现时发现必须改触发边界，那时升为 Major 并停在提案。
完成定义见 3.4。
这是本文件交付后的第一轮。

### S2 收敛 Superpowers 选择证据

类别：Minor，若改 Router 选择权边界则升 Major。
背景：Unreleased 已把 always-on 收成 Router 选择。缺的是可审计的选择记录：Gate 0 是否写明选了哪些方法、为什么不选、explicit 请求没有被当成工作流授权。
做法：抽一组已有 forward-test 能表达的场景，缺的补 fixture，不新增运行时框架。场景至少包括：普通问答不进 meta-entry；proposal-only 不加载 TDD/planning；用户点名某个 Superpowers 方法但不授予 Git/完成权；低风险 Direct Change 的方法集为空。
完成定义：失败用例先红后绿；不增加默认加载的 skill 正文。

### S3 迭代候选进入 backlog 的窄管道

类别：Minor。
背景：Project Learning Closeout 会把项目教训晋升为知识。skill 自身的反复修正还要人记得写进下一轮提示词。
做法：规定 Self-Evolution 或 Review 修正出现两次以上同类信号时，追加一条 backlog 候选，而不是直接改规则。候选用现有 `templates/learning-candidate-template.md` 的字段子集。不自动合并进 `SKILL.md`。
完成定义：有一条从修正信号到 backlog 行的规则和示例；没有新的自动改写器。

### S4 过触发成本的静态预算

类别：Minor。
背景：Superpowers 全包约 2.5 万词；Spec Kit / OpenSpec 的常驻成本在数百 token 的 description 层。本 skill 的风险不是单文件太大，而是一次请求连锁读入 proposal、planning、TDD、review。
做法：在迭代协议里加一张「本轮允许阅读」表：入口只读 loop + self-evolution + backlog。给 `scripts/validate_core_gates.py` 增加一个轻量检查，标记 `SKILL.md` 路由是否仍要求按行读取而不是全量 references。
完成定义：检查能失败于「入口文件要求先读完全部 references」。不改业务项目的证据门禁。

### S5 skill 自改的工作区隔离说明

类别：Patch 或 Minor。
背景：低星 bridge 项目用 worktree 解决并行改动互相覆盖。本 skill 的运行时副本和 git 真源不是同一个目录，自改时更容易改错边。
做法：在迭代协议写明真源是仓库根，`distribution/` 和 `skills/openspec-superpower-change/SKILL.md` 是生成物。一轮开始时确认当前目录是真源克隆；运行时目录只在 sync apply 阶段写入。不引入新的 worktree 强制命令，除非现有脚本已经支持。
完成定义：协议能让下一个 agent 分清真源、生成物、运行时副本。

### S6 上游对照节奏，而不是自动升级

类别：Minor。
背景：`sync-checklist.md` 已禁止无审查的上游升级。长期迭代仍需要固定的对照点，否则每轮都重新搜。
做法：BACKLOG 保留一个季度切片「对照 Superpowers / OpenSpec / Spec Kit 的入口形状」。对照只更新 `docs/iteration/upstream-notes.md`，不改依赖。发现可采纳项再开独立切片。
完成定义：有笔记模板和一条规则：笔记不是升级批准。

明确不做：

- 重开方案 C，拆掉 OpenSpec 或 Superpowers
- 把本 skill 改成 session-start always-on
- 合并 mattpocock/skills 或 oso
- 自动发布 npm，或把搜索可见写成完成条件
- 为了「更智能」放宽 Major 的 change-id 批准

## 5. 之后用户侧只需要说的话

入口落地并推送后，本地 skill 更新完成。之后对任意已加载该 skill 的 agent：

```text
迭代优化skill
```

指定下一刀时：

```text
迭代优化skill：收敛 Superpowers 选择证据
```

Major 提案被批准后：

```text
迭代优化skill：已批准 <change-id>
```

不需要再附本文件，除非 agent 看不到仓库。看不到仓库时，把本文件和仓库路径一起给它。

## 6. 本轮交给 Codex 的边界

现在立刻执行的只有 S1。

允许改：`SKILL.md` description 与路由一行、`AGENTS.md` 的 push 例外一句、`references/self-evolution-rule.md` 的口令租约一段、第 3.1 节四个新文件、覆盖口令路由的测试、CHANGELOG Unreleased。

不允许改：OpenSpec 何时必需、证据签发条件、完成权、Superpowers 选择权、跨 CLI 目标名单。这些若被 S1 碰到，停下来标 Major，不要夹带。

完成后按 3.2 第 9–10 步推送本仓库，并在回复末尾写出下一句口令。
