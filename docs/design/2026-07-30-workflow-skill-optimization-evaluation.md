# 日常开发 Skill 工作流优化评估归档

Date: 2026-07-30

Source requirement: `docs/requirement/27-7-30工作流skill优化.md`

Decision: **方案 C — 继续使用现有组合**

Status: **DECISION CONFIRMED — evaluation archived; no workflow migration authorized**

## 1. 结论

本次评估确认继续使用当前组合：

```text
openspec-superpower-change
├─ OpenSpec：唯一权威变更合同与审批入口
├─ Superpowers：批准后的计划、实施、TDD、调试、Review、验证与分支纪律
└─ codex-brief-antigravity-review
   ├─ standalone prompt/Brief/read-only Review
   └─ valid-Handoff 下的 Brief -> Dispatch -> Report -> Review
```

该结论不表示 `mattpocock/skills` 没有可借鉴能力，而是当前证据不足以在
不削弱治理、且不增加同等或更高维护成本的前提下选择方案 A 或 B。

确认方案 C 后，本次实施边界固定为：

- 不删除 Superpowers；
- 不安装整套或单个 `mattpocock/skills`；
- 不修改 Router、Companion、Handoff、证据或完成契约；
- 不同步全局运行时；
- 不删除任何全局 Skill 或副本；
- 不执行 `git add`、commit、push、PR、release 或其他发布动作；
- 仅归档本评估结论。

## 2. A / B / C 客观门槛

| 方案                      | 判定                      | 证据                                                                                                                                             |
| ------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| A：完全删除 Superpowers   | **FAIL**            | 存在 worktree、branch finish 等暂无等价能力；计划、执行、Review 仍需自有适配；候选兼容验证不全；高风险沙盘和冷读未通过；替代架构没有完整回归证据 |
| B：仅保留最小不可替代子集 | **FAIL**            | 需要保留的 Superpowers 能力互相引用，不能形成独立安装、独立触发且不会重新拉回已删除能力的最小子集                                                |
| C：保持现有组合           | **PASS / selected** | 现有关键门禁有机械验证；替代后的复杂度、维护成本和风险目前不低于现状                                                                             |

方案 B 的主要依赖闭包为：

```text
using-git-worktrees
├─ subagent-driven-development 或 executing-plans
└─ finishing-a-development-branch

subagent-driven-development
├─ writing-plans
├─ requesting-code-review
├─ test-driven-development
├─ using-git-worktrees
└─ finishing-a-development-branch

executing-plans
├─ writing-plans
├─ using-git-worktrees
└─ finishing-a-development-branch

systematic-debugging
├─ test-driven-development
└─ verification-before-completion

writing-skills
└─ test-driven-development
```

因此，保留少数“不可替代项”会重新形成接近完整的依赖簇，不满足方案 B
的隔离门槛。

## 3. 两个现有项目的职责边界

| 项目                               | 权责                                                                                               | 不拥有的权限                                                                 |
| ---------------------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `openspec-superpower-change`     | Gate 0、OpenSpec 决策与审批、风险/证据 profile、实施路由、Handoff 创建、最终完成、跨 CLI 同步      | 不替代 Companion 的已交接 Brief/Report/Review attempt                        |
| `codex-brief-antigravity-review` | standalone 非状态改变文案/只读 Review，或 valid-Handoff 下的 Brief -> Dispatch -> Report -> Review | 不修改文件、不更改批准 scope、不自授权状态转换、不裁决 whole-task completion |
| Superpowers                        | 批准后的计划、worktree、TDD、调试、执行、Review、验证和分支收尾纪律                                | 不替代 OpenSpec 审批，不授予 commit/push 权限                                |

Companion 没有发现任何具体 `superpowers:<skill-name>` 调用。其相关内容是：

- standalone 路径不要求 Superpowers plan 的说明；
- 历史设计文档中的框架名称；
- `references/brief-template.md` 中一个
  `docs/superpowers/plans/YYYY-MM-DD-<change-id>.md` 路径示例；
- 框架无关但与 Superpowers 习惯相似的 RED/GREEN、Review 和验证纪律。

Companion 的 Handoff、Brief、Report、Review、证据绑定、身份隔离、
PASS/FAIL/BLOCKED 和 final handback 契约必须保持冻结。

## 4. Superpowers 替代矩阵

分类：

- **直接替代**：候选核心能力已达到可用强度；
- **现有治理承担**：由 OpenSpec、证据门禁、Completion Contract 或当前
  Self-Evolution 承担；
- **轻量自有实现**：候选只能提供部分方法，需要新的受治理适配；
- **暂无等价**：构成方案 A 阻塞项。

| Superpowers 能力                   | 候选或现有承接                                                          | 判定                                       |
| ---------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------ |
| `brainstorming`                  | OpenSpec discovery + 已安装的`grill-with-docs`                        | 现有治理承担                               |
| `writing-plans`                  | `to-tickets` 只有垂直切片和阻塞边，没有文件、命令、预期输出及证据步骤 | 轻量自有实现                               |
| `executing-plans`                | 原版`implement` 过薄，且有 Git/Review 顺序缺陷                        | 轻量自有实现                               |
| `subagent-driven-development`    | Tickets frontier + Codex collaboration                                  | 轻量自有实现                               |
| `test-driven-development`        | `tdd`                                                                 | 直接替代核心能力                           |
| `systematic-debugging`           | `diagnosing-bugs`                                                     | 直接替代核心能力                           |
| `requesting-code-review`         | `code-review` 双轴模型                                                | 轻量 Codex diff/subagent 适配              |
| `verification-before-completion` | 当前 Completion Contract                                                | 现有治理承担                               |
| `using-git-worktrees`            | 候选无对应能力                                                          | **暂无等价**                         |
| `finishing-a-development-branch` | 候选无 merge/PR/keep/discard/cleanup 流程                               | **暂无等价**                         |
| `writing-skills`                 | Codex`skill-creator` + 当前 Self-Evolution                            | 现有治理承担                               |
| `dispatching-parallel-agents`    | Codex collaboration + 当前风险路由                                      | 轻量自有适配                               |
| `receiving-code-review`          | 当前 findings 修复、验证、重新 Review 回环                              | 现有治理承担                               |
| `using-superpowers`              | 当前顶层 Router                                                         | 现有治理承担；只能在其他依赖全部迁移后移除 |

没有任何候选 Skill 能独立承担现有 Step Evidence Gate、Handoff 状态机或
whole-task completion 决策。

## 5. `mattpocock/skills` 固定版本审计

审计版本：

- Repository: [https://github.com/mattpocock/skills](https://github.com/mattpocock/skills)
- Commit:
  [`2ab958093e83e0ec752e6c1c5932da465bf23e0c`](https://github.com/mattpocock/skills/commit/2ab958093e83e0ec752e6c1c5932da465bf23e0c)
- Commit date: 2026-07-28

### 5.1 可借鉴能力

- `grilling`：一次一问，事实先查、决定交给用户；
- `domain-modeling`：领域词汇与 ADR 条件；
- `to-tickets`：tracer-bullet 垂直切片和 blocking edges；
- `tdd`：公共 seam、逐条 RED -> GREEN、避免实现耦合和同义反复测试；
- `diagnosing-bugs`：red-capable 反馈环、最小复现、可证伪假设和清理；
- `code-review`：Standards 与 Spec 两个隔离审查轴。

### 5.2 不可原样采用的能力

`implement` 当前顺序为：

```text
tdd -> tests/typecheck -> code-review -> commit current branch
```

但 `code-review` 只检查：

```text
git diff <fixed-point>...HEAD
```

这不会包含尚未 commit 的 working-tree 实现；`implement` 也没有提供
fixed point。结果可能是 Review 得到空 diff，随后仍无条件 commit。

因此原版 `implement` 同时存在：

- 未提交改动漏审风险；
- 无条件 commit 越权；
- fixed point 缺失；
- commit 前无法从 commit message 定位来源 spec；
- 无 PASS/FAIL/BLOCKED、证据 freshness 或最终完成门禁。

### 5.3 Codex 兼容性

Codex 当前显式 Skill 调用使用 `$skill` 或 `/skills`。候选正文大量使用
`/tdd`、`/code-review`、`/grilling` 等 Claude 风格调用，需要平台适配。

候选 user-invoked Skill 的 `agents/openai.yaml` 正确使用：

```yaml
policy:
  allow_implicit_invocation: false
```

但本机 Codex `quick_validate.py` 对固定版本的验证结果为：

| Skill                        | 结果                                                  |
| ---------------------------- | ----------------------------------------------------- |
| `tdd`                      | PASS                                                  |
| `diagnosing-bugs`          | PASS                                                  |
| `code-review`              | PASS                                                  |
| `grilling`                 | PASS                                                  |
| `grill-with-docs`          | FAIL：`disable-model-invocation`                    |
| `to-spec`                  | FAIL：`disable-model-invocation`                    |
| `to-tickets`               | FAIL：`disable-model-invocation`                    |
| `implement`                | FAIL：`disable-model-invocation`                    |
| `setup-matt-pocock-skills` | FAIL：`disable-model-invocation`                    |
| `handoff`                  | FAIL：`argument-hint`、`disable-model-invocation` |

其他兼容风险：

- `code-review` 使用 Claude `Agent/general-purpose` 工具名，需要映射到
  Codex collaboration；
- `setup-matt-pocock-skills` 优先修改 `CLAUDE.md`，而不是 Codex
  `AGENTS.md`；
- tracker 操作默认依赖 `gh` CLI，并会创建外部 issue；
- `to-spec` 会创建第二份 issue spec，与 OpenSpec 唯一权威边界冲突；
- `handoff` 是 OS 临时目录中的普通摘要，没有 canonical status、哈希、
  freshness 或消费确认；
- 当前已安装同名 `grill-with-docs`。Codex 对同名 Skill 不合并，再安装会
  形成并存和选择冲突。

### 5.4 若未来选择性引入的完整闭包

```text
grill-with-docs
└─ grilling + domain-modeling + CONTEXT/ADR 格式参考

to-spec / to-tickets
└─ setup-matt-pocock-skills（缺 tracker 配置时）

implement
├─ tdd
└─ code-review
   └─ setup-matt-pocock-skills（缺 tracker 配置时）

diagnosing-bugs
└─ 可选 improve-codebase-architecture
   └─ codebase-design + grilling + domain-modeling
```

方案 C 的实际安装闭包为：**空集合**。

## 6. 门禁削弱风险

| 现有门禁           | 原样引入候选的风险                                         | 风险 |
| ------------------ | ---------------------------------------------------------- | ---- |
| 变更准入与风险分级 | 可从 spec/ticket 直接进入`implement`，没有 Gate 0        | 高   |
| OpenSpec 审批      | `to-spec` 创建另一份 issue spec，形成双权威              | 高   |
| Step Evidence Gate | 没有 canonical status、哈希 manifest 或 freshness 证明     | 严重 |
| Review 失败回环    | `code-review` 只报告，不负责修复、验证和重新 Review      | 高   |
| PASS/FAIL/BLOCKED  | 没有规范状态机和合法转换                                   | 严重 |
| 最终完成契约       | 没有 fresh final verification 或 Router 独占完成权         | 严重 |
| 外部 Agent 身份    | 没有 product/instance/role/profile 与证据绑定              | 严重 |
| Git 授权           | `implement` 无条件 commit；未发现 push，但 commit 仍越权 | 严重 |
| Ticket freshness   | 没有 OpenSpec change-id、批准版本或失效机制                | 高   |

## 7. 沙盘验证

| 场景                          | 结果                                                                                                  |
| ----------------------------- | ----------------------------------------------------------------------------------------------------- |
| 低风险文档小修                | 当前 Direct Change/compact 路径可闭环；无需候选或 Superpowers 实施子 Skill                            |
| 普通多文件功能                | 候选能补充 Tickets/TDD/双轴 Review，但缺批准版本绑定、可执行计划、证据执行器与安全收尾；方案 A 未闭合 |
| API、数据、运行时或外部 Agent | 必须保留 strict OpenSpec、真实验收、schema-5 Handoff、身份/证据绑定和最终完成契约；候选无法替代       |

## 8. 隔离冷读

冷读样本使用现有 fixture change：

```text
change-id: add-notification-preferences
approved-version:
  fixture-v1@sha256:42b1a089bf297a98efb50298e3f219b783e13fc7c23ec1d89c5134beac8717df
```

派生 Ticket 共同绑定：

```text
source_change_id=add-notification-preferences
source_approved_version=fixture-v1@sha256:42b1a089...
```

Freshness 规则：

- 任一 proposal/design/tasks/spec source hash 或 approved-version 改变；
- 所有未完成 Ticket 立即转为 `STALE`；
- 禁止继续实施；
- 必须从新版本重新生成并重新审核/批准。

真正隔离的冷读通过一次性 Codex 会话执行：

- `codex exec --ephemeral`
- `--ignore-user-config`
- `--ignore-rules`
- `--sandbox read-only`
- 临时隔离工作目录；
- 只提供权威 OpenSpec、派生 Tickets 和最小项目规则；
- 不允许调用工具、访问文件系统或修改文件。

冷读 Agent 正确还原了：

- 目标；
- 已知/未知修改范围；
- 两张 Ticket 的交付和依赖；
- Preflight、TDD、真实 API acceptance、Review 和 final verification；
- approved-version 与 source hash 失效规则。

最终冷读结论为 **BLOCKED**，因为以下内容没有被权威契约唯一确定：

- 成功状态码；
- 响应 envelope；
- required 字段缺失的语义；
- 是否需要持久化；
- 仓库现有 auth/error/test 命令与约定。

该结果证明版本绑定与 Preflight stop condition 有效，但也证明当前样本尚
不能满足方案 A 所要求的“冷读全部通过”。

## 9. 全局 Skill 盘点

### 9.1 必须保留

- `/Users/elvis/.agents/skills` 标准发现根及其软链接；
- `/Users/elvis/.codex-account-a/skills/.system`；
- `/Users/elvis/.codex/skills/.system`；
- account-a 插件托管缓存；
- Router、Companion 及 Grok 跨 CLI 副本；
- `/Users/elvis/.codex/superpowers` 主工作树；
- 当前会话直接暴露的本地个人 Skill。

`/Users/elvis/.agents/skills/superpowers` 是到
`/Users/elvis/.codex/superpowers/skills` 的软链接，不是重复物化副本。

### 9.2 当前工作流依赖

- `openspec-superpower-change`；
- `codex-brief-antigravity-review`；
- 14 个 `superpowers:*` Skill；
- 对应发现软链接与实体目标；
- 条件性 `grill-with-docs`。

### 9.3 能力重复或待核对

- `.agents/skills` 与 `.codex/skills` 中的 `cavecrew`、`caveman*`
  同名实体；
- 两套 `.codex/.tmp/.../superpowers` 插件物化副本；
- `.codex.backup.20260626112600/superpowers` 历史备份；
- 已安装本地 `grill-with-docs` 与候选同名。

六组 cave 树在两处字节相同，`caveman-commit` 两处内容不同；仍未证明
其他 runtime 不依赖其中一处。

两套临时 Superpowers 副本彼此相同，但与主工作树有 6 个 Skill 版本不同，
不能当作同内容冗余直接删除。

legacy `notebooklm` 包含认证和 library 数据。即使未在当前 Skill 清单中暴露，
也不能仅因缺少引用而删除。

### 9.4 删除结论

| 分类         | 结果             |
| ------------ | ---------------- |
| 已无用途     | 无可证实对象     |
| 可以永久删除 | **空集合** |

本次没有创建删除备份，因为没有删除行为或已确认删除目标。

Superpowers 主工作树当前：

- HEAD: `cc7b33e858797644ecbfc6eaf8bad39dcb406bd8`
- working tree: clean
- branch: `ahead 1, behind 17`
- 本地 ahead commit 不在远端分支中。

若未来删除，必须先创建 Git bundle 或完整结构化备份；不能假设重新 clone
第三方 origin 即可恢复该本地版本。

## 10. 源码与运行时残留

归档写入前的 Router 评估快照（不含本归档文档）：

- 100 个文件包含 `Superpowers` 泛称或具体调用；
- 74 处具体 `superpowers:*` 调用；
- 覆盖 `SKILL.md`、references、tests、validators、README、历史 OpenSpec、
  design、Review 和 evidence。

同一时点的 Companion 评估快照：

- 5 个文件包含说明性/历史 Superpowers 引用；
- 0 个具体 `superpowers:<skill-name>` 调用。

运行时：

- Superpowers 主树包含 14 个 Skill；
- `.agents/skills/superpowers` 发现软链接仍存在；
- 多个历史/临时副本仍存在。

因此不能声明源码层或运行时层“完全剔除”，方案 C 也不提出该声明。

## 11. 验证证据

### Router

```text
quick_validate.py: PASS
scripts/validate_core_gates.py: PASS
unittest: 142 tests PASS
```

### Companion

```text
quick_validate.py: PASS
scripts/validate_templates.py: PASS
unittest: 74 tests PASS
```

Fresh 合计：**216 tests PASS**。

验证期间没有修改、安装、卸载、同步、commit 或 push。

## 12. Project Learning 审计

评估中没有发现需要额外提升为新工程不变量的独立规则：

- OpenSpec 唯一权威；
- 平台权限不替代业务/审批权限；
- evidence、Review、fresh verification 和 final completion 不得削弱；
- Skill/source/runtime 删除必须可恢复且单独确认；
- 历史证据不能为实现“零引用”而静默改写。

这些规则已经存在于当前 Skill、Non-negotiables、工程不变量和 Completion
Contract 中。新增第二份规则或 Candidate Card 只会造成重复。

本归档文档是确认方案 C 的耐久评估记录；不把聊天记录、完整外部 trace、
凭据或其他敏感内容写入仓库。

## 13. 已知剩余问题

1. Companion 的 `references/handoff-contract.md` 示例调用不存在的
   `scripts/validate_core_gates.py`；实际验证器是
   `scripts/validate_templates.py`。该问题不在本次“仅归档”范围内。
2. Router 工作树在评估前已有以下 user-owned untracked 状态，本次保持不变：
   - `CONTEXT.md`
   - `docs/requirement/27-7-30工作流skill优化.md`
   - `openspec/changes/streamline-workflow-prompt-contracts/`
3. Companion 工作树在评估结束时为 clean。
4. 方案 C 保留 Superpowers 的上下文负担和能力重叠；这是确认接受的非阻塞代价。

## 14. 回滚与重新评估条件

本次只新增该归档文档，不改变行为或运行时。若需回滚，只需移除该未发布归档
文件；没有 runtime、Skill、配置、Git history 或外部系统状态需要恢复。

只有出现以下新证据时才应重新评估 A/B：

- worktree 和 branch-finish 出现经过验证的等价实现；
- OpenSpec-version-bound Tickets、fresh-session execution 和 evidence
  state machine 完成实现与回归验证；
- `implement` 的工作区 Review 与 commit 授权问题被修复；
- 候选通过当前 Codex frontmatter、invocation、subagent 和 tracker 兼容验证；
- 三类沙盘及真正隔离冷读全部 PASS；
- 精确全局删除名单具备依赖证明、结构化备份和恢复演练。

重新评估或实施 A/B 属于 Major Self-Evolution，必须创建具体 OpenSpec change，
strict validate，并由用户明确批准该 change-id 和 scoped contract 后才可修改。
