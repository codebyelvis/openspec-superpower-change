# 多 agent 规则复用：咨询评审合并与实施草案

作者：elvis。日期：2026-10-10。状态：proposal-only／待具体 change-id 批准。

关联提案：`openspec/changes/align-native-agent-governance/`，draft-v1。
本记录合并 Grok CLI、Cursor、Claude Code（claudex）的 advisory-input；
三份报告均不是 Preflight、批次 PASS、最终 Review 或实施批准。

## 背景与现状

目标是 Codex 主导、一项内容一个可编辑权威源、多个入口复用，降低人工
维护多个 agent 的漂移。现有两个源仓库与四目标同步机制已经承担核心
内容分发；本轮问题主要位于实际运行入口、原生规则覆盖和输出契约。

已有证据的范围：portable manifest 声明 Router 30 文件、Companion 10
文件；默认 Codex、Pi、Antigravity CLI、Grok CLI 的声明文件与源一致。
共享 skills、Claude、Cursor 通过链接消费默认 Codex 的副本。四个正式
目标是独立目录副本；不把链接消费者再算作独立安装事务。

实际 Codex 账户 A 的私有目录没有这两个 skill，其全局规则没有 CCG。
但本会话 skill 目录列出了共享入口，故“账户 A 完全无法使用 skill”
不成立。该目录证据证明发现来源，不证明正文执行、治理覆盖或行为验收。
控制面授权继续来自绑定实例与合同，不来自账户名、模型名或产品名。

`claudex`、`claudeg` 都启动 Claude Code；不同模型后端不改变产品。
现行 schema 6 只接受 codex、pi、antigravity-cli、grok-cli。Claude Code
和 Cursor 可以消费同源内容、提供咨询，不能借产品身份签正式门。

## 开源调研结果与取舍

| 方案 | 可复用能力 | 本次决定 |
| --- | --- | --- |
| [Rulesync](https://github.com/dyoshikawa/rulesync) | 多工具规则格式生成、目标/功能筛选、隔离输入输出、dry-run | 暂不安装；未来有明确格式生成缺口时，锁定版本做 rules-only 隔离试点 |
| [Vercel Skills](https://github.com/vercel-labs/skills) | SKILL.md 安装、链接或复制 | 当前分发与 parity 已成立，不替换现有安装链 |
| [Ruler](https://github.com/intellectronica/ruler) | 规则与相关配置分发 | 本次不采用，避免引入超出治理正文的配置管理面 |

Rulesync 的公开支持矩阵与 global-mode 指南有范围差异；“列出产品”
不等于支持本机实际入口和全局目录。任何后续试点必须以锁定版本代码
和隔离生成结果验收。[支持矩阵](https://rulesync.dyoshikawa.com/reference/supported-tools.html)、
[全局模式](https://rulesync.dyoshikawa.com/guide/global-mode.html)、
[输入输出分离](https://rulesync.dyoshikawa.com/guide/separate-input-root)。

取舍：复用成熟工具是解决具体缺口的方法，不能成为更换已存在的事务、
身份与证据链的目标。当前清单同步器已经具备源哈希、目标 pre-state、
备份、receipt、单目标恢复和后续目标阻断；再装一套同步器会增加输出
所有者。保持当前链路，是调研与三份咨询反馈合并后的决定。

## A–G 反馈处理

| 项目 | 采用的修订 | 边界与证据限制 |
| --- | --- | --- |
| A Grok 导入 Claude hook | 将原生兼容隔离列为后续逐路径适配，先确认只排除 guard 的支持机制 | inspect 注册与 launcher 拒绝已知；真实 Grok 工具调用被拦尚未复现。不能扩大白名单，也不能笼统关闭全部 hook |
| B 产品身份 | 四产品集合保持；Claude/Cursor 为消费者或咨询方 | 新增正式产品另立 Major，不冒填 codex/grok-cli |
| C 报告格式与路径 | publisher 报告和合同 attempt 证据保持各自绑定 | publisher 前置来源注释与首行要求存在张力，未证明 validator 已失败。本轮不支持 Claude 正式签门，故不改 publisher/Companion 格式 |
| D 聊天与落盘 | 普通 advisory 默认聊天；明确保存先回 Router 分类；批次只写已绑定路径 | 保存报告不会自动取得 gate 权限。原生 publisher 适用时不得绕过 |
| E CCG-004 | 将 compact **本地**例外写入公共块 | compact 外部、standard/strict、多切片和受保护边界保留所需独立门 |
| F Superpowers | 保留 Router 优先；增加普通问答与咨询例外；记录实际依赖路径/hash | 不以目录名含 router 推断正文正确，也不把旧入口缺口等同已发生故障 |
| G 计划时点与路径 | 需要计划时执行前形成或复用；已有绑定和项目约定优先 | docs/design 只是无更具体约定时的默认；不迁移或重写历史证据 |

定位依据：`references/shared-global-governance.md` CCG-004/014；
`references/direct-change-rule.md`；`references/superpowers-adapter.md`；
`references/project-learning-closeout.md` Project Document Ownership；
`references/cross-cli-sync.md`；`scripts/validate_cross_cli_sync.py`；
Companion 的 `SKILL.md`、`references/handed-off-external-execution.md`。
原生配置位置只作为本地审查输入，不复制全文到共享规则。

## Companion 的保留与融合

保留 `codex-brief-antigravity-review` 独立 skill：standalone 只读咨询轻量
交付；已有 Handoff 下负责 Brief、Report、Review、attempt、证据与恢复。
Router 继续负责变更分类、批准、canonical 状态和完成边界。

分发工具只安装内容，不接管 governor。两仓库当前同名 Handoff reference
保留为已有的兼容工件，本轮不新增可编辑合同副本，也不做去重迁移。
运行时唯一可变合同仍是 canonical status 中的绑定块。

## 可实施范围与具体片段

第一片只修共享治理和消费约定，完整文件白名单与**精确 CCG-004、
CCG-014、输出/计划规则片段**见提案 `design.md`。源与四目标同步取得
相应证据后，再提交原生适配计划，避免一份批准无限扩展到 HOME 配置。

第二片必须逐入口说明：真实产品、launcher、配置根、规则源、skill
发现路径、Superpowers 依赖、publisher 策略、受管范围和验收证据。
账户 A 复用已发现的共享 skill，不能为补规则复制认证或会话。
Claude/Cursor 继续消费内容；Grok 的兼容隔离必须有安装版本支持证据。
原生适配的确切路径/pre-state/片段、备份、回滚和验收具备后，另行批准。

两片共有的停止条件：未获具体 Major 批准、路径/pre-state 漂移、所需
检查失败、证据不新鲜、未解决的 review finding，或者触及排除文件。
原有脏文件和未跟踪文件原样保留，不清理、不纳入本片。

## 验证与回滚

当前只做 OpenSpec 严格校验、提案一致性和前后文件指纹检查。
这不构成实现、测试套件、模型回放或最终 Review PASS。

批准后的 RED/GREEN 必须拒绝原来的错误假设：所有 compact 都免门、
所有 governed 都建 Preflight、私有目录缺文件等于不可发现、默认账户
parity 等于实际入口已验证、原生目录覆盖绑定路径、publisher 获得正式
产品权、四端同步可顺便写 hooks。验证归属具体工件，不能靠拼接其他
文件的正文通过。保留 PyYAML 和依赖无关模式、完整原有 unittest、
quick validation、core gates 及源/运行时声明闭包检查。

行为回放按不同失败机制覆盖一次；原生加载/无工具结论检查 native
events，正确回答或文件没变不能替代。具体用例和命令见 `design.md`。
七入口仍须自己的验收，不能用四端哈希替代。临时 raw trace 不落仓库。

已创建结构化临时备份与两仓库文件指纹，保留在 skill discovery 之外。
Codex 负责源回滚；四目标使用既有 receipt 与逐目标恢复。源回滚只撤销
本片差异，不能 reset/clean 原工作区。待审批/回滚决策未完成时保留备份；
闭环通过后按既有规则清理临时备份，不作为第二份版本历史。

## 未完成项

- 此 change-id 尚未批准；源规则和运行时未修改。
- 原生适配精确方案与批准尚未完成。
- 七入口真实模型行为回放尚未完成。
- Git 写入、push、公开发布和重叠变更归档未授权。

这些待办不妨碍当前提案可审阅，但阻止宣称用户的整项治理复用目标完成。
