# S7 项目实施关窗接力审查草稿

日期：2026-10-08。作者：elvis。状态：Major／proposal-only／未批准。
拟议 change-id：`add-project-session-resume`。本文件是审查草稿，不能授权实现。

## 已确认缺口与现有证据

- 合同补充 §7 指出：业务项目实施停手前没有统一的持久化义务；新窗口
  不能依赖最后一条聊天判断已完成工作、唯一下一动作或最佳验证版本。
- `references/approved-implementation-workflow.md` 已规定恢复 Plan/Status/Handoff
  及禁止第二套 task ledger；本项补持久化和恢复验证，不重做既有闭环机制。
- `references/handoff-contract.md` 的完整 schema 6 仅用于外部执行；
  `scripts/validate_core_gates.py::_validate_schema6_handoff_contract` 精确校验字段集。
  瘦状态直接传入现有 Handoff API 会被拒绝；缺字段不能成为自动降级条件。
- 新窗口不是已绑定控制面实例的身份凭证。恢复工作信息与签发状态、证据、
  完成结论是不同权限；当前规则禁止未绑定实例自任控制面。

## 期望行为与待批准选择

推荐复用 `docs/agent-collab/<change-id>/status.md`。同一个文件保留唯一
治理状态与一份进度记录：本地实施用 schema 6 的显式字段子集，外部协作
仍用完整 Handoff。进度字段不伪装成现有 schema 6 字段。

该兼容方案、Direct Change 的目录标识及身份恢复限制均为**待审阅设计**，
不是已接受的事实。具体编码、迁移表和替代方案以拟议 OpenSpec design 为准。
不把“继续闭环”解释为新批准、Git push、生产写入或控制面重新绑定。

## 拟议实现文件

| 文件 | 允许变化 |
|---|---|
| `SKILL.md` | 现有续跑段增加必要导航；不增加 always-on 或新的问答触发 |
| `references/approved-implementation-workflow.md` | 集中维护状态记录、停手、恢复和验证版本规则 |
| `references/direct-change-rule.md` | 多窗口且有待续工作时导航到同一规则；完整单轮 compact 不新增仪式 |
| `scripts/validate_core_gates.py` | 新增显式本地续跑入口、状态/版本/路径检查；完整 Handoff API 不放宽 |
| `tests/test_workflow_rules.py` | 变更行为的 RED/GREEN 与兼容性负例；复用现有测试结构 |
| `CHANGELOG.md`、本项 OpenSpec 工件、iteration 状态与证据 | 实现后按已批准范围记录验证、审查、同步与收尾 |

`references/handoff-contract.md`、companion 仓库、portable manifest、跨 CLI
目标名单、全局规则正文均无实现修改权限。若实际实现需要它们，先改提案并
重新审批。S8 文档归属及历史文档迁移不在本项范围。

## 拟议规则正文

> Before intentionally pausing, ending an advancing implementation turn, or
> handing work to a new window, persist the current state, completed work,
> exactly one next_action, blockers and resume_condition in the canonical
> status.md. Reuse the same record for local implementation and external
> collaboration; do not create a second task ledger.

> Resume only from validated persisted project state and its referenced
> contract, plan and evidence. “继续闭环” and “闭环推进” select the persisted
> next_action within existing authorization; they grant no new approval, Git,
> production, assignment, evidence-signoff or completion authority. When more
> than one unfinished change exists, ask the user to select one.

> The best checkpoint is the latest verified revision whose result and scope
> fingerprint have been persisted. Later unverified edits do not become PASS
> and must not overwrite that checkpoint or trigger an automatic rollback.

> Local resume records use an explicitly discriminated subset of schema 6.
> Complete external Handoffs retain their exact current schema and gates.
> Malformed, duplicate, stale or contradictory state is BLOCKED, never a
> fallback to a more permissive local record.

这些是未来拟加入规则，不在本轮写入 skill 或运行时。

## 验证与审查计划

当前只做草稿一致性、范围及 `openspec validate add-project-session-resume
--strict --no-interactive`；源 quick/core 用于检查既有门禁未被草稿影响。
不把这些结果称为 S7 行为验证或独立 Review PASS。

批准后的验证与 review 计划：

1. 现有测试结构中先 RED 后 GREEN：漏写唯一动作、聊天覆盖状态、验证后文件
   漂移、非法本地子集、外部缺字段降级、身份不匹配与非法完成迁移。
2. 隔离真实 forward-test：新窗口无旧聊天恢复验证版本和 next_action；严格
   场景检验篡改、未批准 Major、多个 change 与权限边界。审计原生事件；持久
   证据仅保留脱敏输入、摘要、命令、结果与指纹，不保存原始消息/trace。
3. quick_validate、core-gate、完整现有 unittest，fallback/PyYAML 两模式；
   旧完整 schema 6、独立外部 Review、previous-status 完成门禁及历史 4/5 不变。
4. 写入运行时前审查已有 scoped sync plan 的源、目的前态与只读断言；
   Codex/Pi/Antigravity/Grok 按现有事务 apply、validator、discovery、verify-all。
5. strict 实现审查及同步后完整 diff 的独立 final Review；执行者、控制面与
   reviewer 的实例、目的、product、role、capability、independence、authority
   必须在执行前按既有规则绑定。模型固定 gpt-6.1-sol／high 不替代实例独立性。
6. 本仓库 Git 收尾只服从该轮明确租约；不把 S7 业务续跑口令视为 Git 权限。

目前 reviewer 未指派、独立审查未执行、用户批准未取得；全部不得填 PASS。

## 本轮草稿验证记录

- `openspec validate add-project-session-resume --strict --no-interactive`：PASS；
  CLI 识别 5 条 ADDED requirement、11 个 scenario，未修改主 spec。
- 源 `quick_validate.py`：PASS；`validate_core_gates.py .`：fallback/PyYAML
  均 PASS。实现文件逐字节等于基线，不以该结果声称本地续跑已经可用。
- 草稿结构检查：13 个拟议 governance 字段均为现有 schema 6 字段；
  状态迁移表仅引用现有枚举；11 个 contract task 均未勾选。
- 范围检查：BACKLOG 仅 S7 状态改变；S1–S6/S8 全文、优先级、完成定义保持；
  已有无关工作状态保持；本轮没有 Git 提交／推送或 runtime apply。
- 审查性质：作者结构与范围自查；独立 Review、行为 RED/GREEN、native
  forward-test 和运行时同步验证均留待具体批准后的实现轮。

## 回滚与停手

草稿基线：`95e6a51c1d6a405e54049262693b5ab95f2f45d7`。结构化私有备份路径
记录在 `docs/iteration/CURRENT.md`，不位于 skill 发现目录。取消草稿时仅恢复
备份中的 CURRENT/BACKLOG 并删除本轮新建草稿/change 目录；不得 reset/clean
工作区或动已有五份修改 spec 及 JEV 文件。

实现后的源恢复使用当轮备份与确切改动清单；运行时只用相同事务的 restore
及 verify-all，不手工覆盖、不改历史、不自动迁移已有协作状态。

提案验证成功后仍停在具体 `add-project-session-resume` 和上述范围的用户批准。
