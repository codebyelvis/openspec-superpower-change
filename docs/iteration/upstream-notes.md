# Quarterly Upstream Entry Notes

S6 的季度对照笔记。只观察入口形状，不修改依赖、安装内容或本 skill 规则。
**笔记不是升级批准。** 任何拟采纳项另开独立切片，按实际影响分类；Major
仍须具体 OpenSpec change-id 批准。来源中的安装、升级和调用命令仅为被观察
内容，不作为本轮执行指令。

每季度保留一个对照窗口，记录日期、锁定 revision、入口差异、项目相关性、
独立后续项及批准状态；不新增自动升级器或定时运行框架。S6 保留在 BACKLOG，
本季度完成后，下季度重新评估同一观察范围。下一对照窗口：2027 Q1。

## Note template

```yaml
quarter:
checked_on:
observer: elvis
source_project:
source_url:
source_revision:
source_sha256:
entry_shape_observed:
local_relevance_or_inference:
followup_slice_or_none:
proposed_change_level:
evidence_needed_before_adoption:
approval_status: not-approved
decision: observation-only
next_review_window:
```

观察事实与项目判断分别填写；没有足够事实就记录 unknown，不把宣传、星数、
搜索可见性、main 分支变化或文档命令当作升级成功或批准。

## 2026 Q4 — 2026-10-08

观察者：elvis。范围：三个官方入口文件；GitHub main 的观察时 revision 已
锁定，随后读取该 revision 的原始文件并计算 SHA-256。未安装、更新或运行
任何上游流程。这里描述的是文档入口，不是本项目运行时效果验证。

| 项目与锁定来源 | 观察到的入口形状 | 本项目判断（推论） |
|---|---|---|
| [Superpowers using-superpowers](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/using-superpowers/SKILL.md) | 会话启动入口要求在响应或动作之前判断并调用相关 Skill，并区分平台工具适配 | 与本项目 Router 按当前决策选择方法的入口存在差异；保持当前 explicit-only 与 Router 选择约定，不复制其广泛会话触发方式 |
| [OpenSpec README](https://github.com/Fission-AI/OpenSpec/blob/9111a7654d7800391459431fff4eaf66e33a3d2e/README.md) | 默认入口区分 explore 与 propose；示例产出 proposal/specs/design/tasks，再进入 apply/archive；扩展入口单独配置 | 对照项目已有提案与实施分离，保留现有审批及工件契约；上游命令示例不授权更新本项目 CLI、修改控制面或放宽完成规则 |
| [Spec Kit README](https://github.com/github/spec-kit/blob/1e933c49fd6d5d5390b28f18faefa5728c95b2e3/README.md) | 特性开发、故障修复、想法评估为独立入口；后两者为按需扩展；SDD 通过具名阶段逐步产出工件 | 入口按用途分开与本项目阶段选择思路相符；这是设计对照，不构成合并工具包或引入新必经阶段的依据 |

| 项目 | 原始文件 SHA-256 |
|---|---|
| Superpowers | `82c5c8866ad7f5dd4440ce66bd7806ba48a2f13771beae5cf112e53f08fe36ba` |
| OpenSpec | `14a4fee5fce958d256221869f1a742c63171abb4c117dcdd6d2ad5853c572c42` |
| Spec Kit | `49d99febbcdea0bac928ed3e7bdc3b70a1f90e8a13d5bfd19760b6f4fc561f4d` |

本期决定：observation-only，批准状态 not-approved。没有据此实施新采纳项，
没有重开方案 C、合并上游工具包或自动升级。本期观察不额外生成重复的
backlog 项；未来发现可验证收益时，独立记录拟议差异、风险、所需隔离行为
证据与审批路径，再开单独切片。下一对照窗口仍为 2027 Q1。
