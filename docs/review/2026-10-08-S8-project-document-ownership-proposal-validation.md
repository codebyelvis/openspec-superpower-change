# S8 draft-v1 提案验证记录

作者：elvis。日期：2026-10-08。
change-id：`add-project-document-ownership`。阶段：proposal-only。

## 结论与适用范围

提案工件校验 PASS，当前等待具体批准。以下结果验证新 change 的格式、
既有门禁及本轮改动范围；不证明 S8 行为已实现。具体批准、实施 Plan/
Preflight、RED/GREEN、原生文件行为、独立实现/Final Review、运行时同步
均未执行。tasks 的 11 项批准/实施/闭环任务全部未勾选。

## 已执行检查

| 检查 | 实际执行与结果 |
|---|---|
| OpenSpec | `openspec validate add-project-document-ownership --strict`，退出 0，valid |
| quick | `PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 /Users/elvis/.codex-account-a/skills/.system/skill-creator/scripts/quick_validate.py .`，退出 0，Skill is valid |
| core / fallback | `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .`，退出 0 |
| core / PyYAML | `PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 scripts/validate_core_gates.py .`，退出 0 |
| 相关既有 unittest / PyYAML | Python heredoc 用 unittest loader 加载下述 7 个 WorkflowRulesTest 方法及 SkillIterationEntryTests 整类，17 项，全部通过 |
| 相关既有 unittest / fallback | Python heredoc 分别加载 8 项匹配测试和 SkillIterationEntryTests 的 10 项；一项重复，17 个不同测试全部通过 |
| 引用与工件 | 13 个实际源/工件引用均为已有普通文件；新工件无尾随空白、围栏成对；示例/未来目标不冒充现存文件 |
| 范围 | 44 个起轮无关文件及 14 个未授权编辑的已备份源文件 SHA-256 未变；S1–S7 七行 backlog 字节相同；只读核对四个相关运行时文件与快照相同 |
| Git 状态 | 起轮 HEAD 仍为 `379667f9780a3e718f41021f8a92a82618a286e2`；`git diff --cached --quiet` 退出 0；CURRENT/BACKLOG scoped `git diff --check` 通过；本轮无 add/commit/push |

解析器：fallback `/opt/homebrew/opt/python@3.14/bin/python3.14` 无 PyYAML；
PyYAML `/opt/anaconda3/bin/python3`，已有 PyYAML 6.0。未修改仓库依赖。
本轮没有改 SKILL 路由或运行规则，只更新提案/迭代状态，故运行相关既有
回归；后续实现路由变化时仍必须运行双解析的现有全套 unittest。

七个 WorkflowRulesTest 方法：

- `test_proposal_only_can_select_no_superpowers_subskill`
- `test_project_learning_gate_has_automatic_and_explicit_triggers`
- `test_required_project_learning_blocks_completion_and_archive`
- `test_learning_artifacts_are_layered_and_mechanical_rules_are_executable`
- `test_project_learning_validator_binds_rules_to_owned_artifacts`
- `test_project_learning_guidance_is_discoverable_from_project_instructions`
- `test_tiered_10_high_severity_candidate_is_proposal_only_without_approval`

## 待审批工件字节身份

以下 SHA-256 只标识本次待审合同，不是批准、manifest 或签发凭证：

| change 内文件 | SHA-256 |
|---|---|
| proposal.md | a4e465222f68340006caae873e56194be50cc2d84f66d276df76f51ead921e9d |
| design.md | a4a1409f223a37b874d313c10cec4ff89cee2ce83bb1563b4eaeca1739c49d7a |
| tasks.md | d06fbfd095fe76b6485fdbf157b40211aeaa0c0a74edaa83aefcd1e2530e0354 |
| specs/skill-workflow-governance/spec.md | af075dc7bee1e39fd08c1c3913f599cbb01c9583669d44c2efd0cef917e8e56b |

## 备份与续跑

结构化备份位于
`/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/openspec-S8-proposal-4xkas497`，
权限 0700，含源文件快照、只读运行时快照及范围核对结果。待具体批准/回滚
决策期间保留；未使用的临时验证 venv 已删除，没有产生原生 trace。
后续若批准实施，先创建新实施备份，不复用此提案快照覆盖后来变化。

CURRENT 保存唯一下一动作：等待用户明确批准此 change-id 与 draft-v1 范围。
读取本次 proposal/design/tasks/spec 和审查草稿继续，不重做 S1–S7，
不把本记录作为 Review PASS、实现完成或同步授权。
