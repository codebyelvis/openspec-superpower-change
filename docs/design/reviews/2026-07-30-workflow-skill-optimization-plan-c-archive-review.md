# 方案 C 本地归档 Review

- **文档类型**：Archive / Decision Review（Review-only）
- **日期及版本**：2026-07-30 / plan-c-archive-review
- **结论**：**通过**
- **验证范围**：
  - `docs/design/2026-07-30-workflow-skill-optimization-evaluation.md`（全文 + SHA-256 + 卫生检查）
  - `docs/requirement/27-7-30工作流skill优化.md`（需求源对照）
  - Router 工作树 `git status` / 无 tracked diff
  - Companion 源码 `references/handoff-contract.md` 与 `scripts/`
  - Superpowers 运行时主树 `/Users/elvis/.codex/superpowers`
  - 独立重跑：Router `validate_core_gates.py` + 142 unittest；Companion `validate_templates.py` + 74 unittest

> 本文件“发布闭环补充”之前保留最初 archive-only Review 的历史口径。用户
> 随后明确授权双语 README 更新、精确 Git 发布和本地 Skill parity 核对；
> 当前发布口径及现行归档哈希以文末补充为准。

## Gate 0（Review-only）

1. **mode**：Review-only；不修改运行时、契约、Skill，不执行 staging/commit/push。
2. **OpenSpec**：本次仅为「方案 C 评估归档」验收，不实施 A/B/迁移；若未来实施 A/B 或修改治理契约，属 Major Self-Evolution，须单独 OpenSpec change + 用户批准。
3. **Superpowers sub-skills**：无（只读审查，不实施）。
4. **risk/evidence**：归档文档审查 + 关键事实独立复验；不授权安装/删除/同步。

## 问题与风险

**未发现阻塞问题。**

已确认的非阻塞残留（归档 §13 已正确记录，且不在本次「仅归档」范围）：

1. Companion `references/handoff-contract.md` 示例仍引用不存在的 `scripts/validate_core_gates.py`；实际脚本为 `scripts/validate_templates.py`。属文档/示例漂移，应单独 Direct Change 或小型 docs fix，不得混入本归档任务。
2. 方案 C 接受 Superpowers 上下文负担与能力重叠；归档已声明为确认代价，不构成本次失败项。
3. Router 工作树仍有用户既有 untracked 项（`CONTEXT.md`、需求文档、`openspec/changes/streamline-workflow-prompt-contracts/`）；与本次归档并存，未误伤。

## 独立复验事实

| 声明 | 复验结果 |
|---|---|
| 原始 archive-only Review 的归档 SHA-256 `c09926405b0b1b99df53369f158bc3c70c5e70003e3e461f7e84e8e4d929ce4d` | **当时匹配**；现行发布哈希见文末补充 |
| 最终换行、无尾随空格 | **通过** |
| 敏感信息扫描（常见密钥/token 模式） | **无命中** |
| 决策 = 方案 C，边界 = 仅归档、不安装/删除/改契约/Git 发布 | **正文明确且一致** |
| 原始 Review 时 Router 无 tracked 改动；仅 untracked 归档 + 既有项 | **当时由 `git status` 确认；分支与 `origin/main` 一致** |
| Router `validate_core_gates.py` + 142 tests | **独立重跑 PASS（142 OK）** |
| Companion `validate_templates.py` + 74 tests | **独立重跑 PASS（74 OK）** |
| Companion 0 处 `superpowers:<skill>` 具体调用；约 5 文件泛称/历史引用 | **`superpowers:` 匹配 0；5 文件含 Superpowers/superpowers** |
| Router 具体 `superpowers:*` 约 74 处（评估快照口径） | **独立计数 74（排除本归档文件）** |
| Superpowers HEAD `cc7b33e...`、clean、ahead 1 / behind 17、14 skills、`.agents` 软链 | **全部匹配** |
| Companion handoff 示例错误路径 | **确认**：`handoff-contract.md:287` 写 `validate_core_gates.py`；`scripts/` 仅有 `validate_templates.py` |
| 未安装/删除 Skill、未改 Companion/治理契约 | **工作树与测试结果支持；无 tracked skill 变更** |

## 决策与范围判定

1. **方案选择**：在需求门槛下，A（完全剔除）与 B（最小子集）被记录为 FAIL，C 为 PASS/selected，论证链条完整（替代矩阵、依赖闭包、门禁削弱表、沙盘、冷读 BLOCKED、全局删除空集合）。
2. **实施边界**：原始归档阶段将动作收窄为「仅新增评估文档」；当时与仓库状态一致，无范围漂移。
3. **回滚**：原始归档阶段仅需移除未跟踪归档文件；后续发布范围与回滚见文末补充。
4. **重新评估门槛**：§14 将 A/B 重开条件绑定到可验证证据与 OpenSpec Major，避免聊天层偷跑迁移。

## 事实偏差 / 遗漏

- **无阻塞性事实偏差。** 用户报告的验证数字与本机独立重跑一致。
- 归档正文未内嵌自身 SHA-256（由交付说明单独给出）；本次 Review 以磁盘文件哈希为准，已对齐。
- 外部候选仓库固定 commit `2ab9580...`、冷读一次性会话与 `quick_validate.py` 对候选 frontmatter 的 FAIL 表，本次未重新拉取/重跑外部仓库；作为评估过程证据接受，**不影响**「方案 C 仅归档」结论的可验收性。若未来重开 A/B，须在新 change 下刷新该部分证据。

## 摘要

方案 C 本地归档**可验收**：新增评估文档内容完整、卫生与哈希正确，范围严格限于归档，Router/Companion 机械验证与 Superpowers 运行时快照可独立复现，既有残留问题已正确外置且未越权处理。不授权 Git 操作；归档文件保持 untracked，待用户单独决定。

## 后续建议（非阻塞）

1. 用户自行决定是否 `git add` / commit 该归档（及是否连同需求文档一并纳入）。
2. 另开任务修正 Companion `handoff-contract.md` 示例路径：`validate_core_gates.py` → `validate_templates.py`（建议配套最小测试或文档一致性检查）。
3. 在 worktree / branch-finish 等价能力、OpenSpec 版本绑定 Tickets、implement 授权修复等新证据出现前，不重开 A/B。

## 发布闭环补充（2026-07-30）

用户在 archive-only Review 后明确授权：

- 将方案 C 需求、评估和 Review 纳入 Git；
- 同步更新 `README.md` 与 `README_cn.md`；
- 核对并在需要时更新本地 Codex Skill；
- commit 并 push `origin/main`，不创建 PR。

当前拟发布文件固定为：

1. `README.md`
2. `README_cn.md`
3. `docs/requirement/27-7-30工作流skill优化.md`
4. `docs/design/2026-07-30-workflow-skill-optimization-evaluation.md`
5. `docs/design/reviews/2026-07-30-workflow-skill-optimization-plan-c-archive-review.md`

发布准备阶段检测到评估归档发生 Markdown 表格重排：行数仍为 450，但旧
archive-only SHA-256 `c0992640...ce4d` 已不再对应磁盘文件。旧版本未进入
Git，无法宣称逐字仅格式变化，因此没有回退或覆盖该并发改动；当前全文重新按
需求、方案 C 边界、敏感信息和验证声明复核，现行 SHA-256 为：

```text
2fe6a1a187908d68de55bbf43f3742e3f955ab3cabdf6851fce3ea6e12d6d0bc
```

本地 runtime portable 文件无需覆盖写入：

- Router source ↔ Codex runtime：`29/29` 一致；
- Companion source ↔ Codex runtime：`10/10` 一致；
- README 与设计/历史文档不在 cross-CLI portable manifest 中，不触发
  Antigravity CLI 或 Grok CLI 同步。

发布前验证重新执行：

- Router：`quick_validate.py` PASS、`validate_core_gates.py` PASS、
  142 tests PASS；
- Companion：`quick_validate.py` PASS、`validate_templates.py` PASS、
  74 tests PASS；
- Codex runtime Router/Companion：各自 quick validator 与项目 validator
  PASS；
- 五个发布文件：最终换行、尾随空格、常见密钥/token 模式与相对链接检查
  PASS。

`CONTEXT.md` 与 `openspec/changes/streamline-workflow-prompt-contracts/` 仍为
既有未跟踪项，不属于本次 staging 范围。整体回滚应恢复双语 README，并移除
需求、评估和 Review 三份新增文档；本次没有 runtime、Skill、配置或外部系统
状态需要恢复。
