# S12 多模型联合评估门禁：Major 审查草稿

Author: elvis。日期：2026-11-20。版本：draft-v2（已收敛独立只读审查 R1 全部 3×P2 + 1×P3 发现）。状态：**Major／仅提案待批，暂不实现**。
change-id：`add-multi-model-eval-gate`。

## Gate 0 与本轮授权边界

- 模式：`Self-Evolution / proposal-only`（用户显式口令：`迭代优化skill：多模型联合评估门禁（仅提案`）。
- 级别：**Major**（涉及 Major Self-Evolution 便携行为改动的前向评估门禁、用户显式例外边界与静态校验器规则，须经严格 OpenSpec 提案审批后方可实现）。
- 本轮已授权范围：仅产出 `openspec/changes/add-multi-model-eval-gate/{proposal,design,tasks,specs/...}.md`、本审查草稿及 `docs/iteration/{BACKLOG,CURRENT}.md` 的待批登记，执行提案校验与独立只读审查；**严禁**编辑任何源码、规则、模板、测试、生成物、四端运行时、6 组历史脏文件或执行 `git add/commit/push`。

## 1. 已观察问题（Observed Failures & Evidence）

1. **单模型特化毒害共享 Harness（`arXiv:2611.18856v1` §4.3.3 Table 2）**：在 Grok 4.20 Reasoning / Claude Opus 5.5 / Gemini 3.8 Flash 共享同一套 Harness 时，基于单个模型演化的补丁迁移到其余两家模型得分大幅下滑（`66.84–72.24`），而基于多模型反馈联合综合（Unified Synthesis `75.24`）持平各模型专版（`75.20`）并显著优于裸种子（`73.28`）。
2. **本仓库四端共享的对称治理缺口**：
   - `S11`（`61d22ff`）已补齐**规则退役（删除旧规则）**的跨模型内化门槛，但**新增或修改** Major 级便携行为规则（触发范围、路由、OpenSpec/Superpowers 边界、证据/完成门禁）时，仍缺少结构化的多模型联合前向评估门禁与机械校验；
   - 若直接“一刀切”要求所有迭代都跑双模型会拖慢日常 Patch/Minor，而在第二模型短暂不可用时若无诚实例外通道又会造成永久死锁。

## 2. 期望行为（Desired Behavior）

1. **精准激活边界（零日常热路径摩擦）**：仅当 **Major Self-Evolution 且修改便携行为正文**（`references/cross-cli-portable-manifest.json` 内的 `SKILL.md`、`references/*.md` 或 `templates/*.md`）时强制触发；所有 **Patch / Minor**、纯机械脚本/测试/文档改动及普通业务项目一律豁免。
2. **复用 `docs/iteration/BACKLOG.md`（零新状态文件）**：以双 YAML 兼容的 `record_kind: sim-multi-model-eval` 块记录两种严格闭环态（均无条件禁 `status: promoted`）：
   - **`dual-covered`（默认）**：`>= 2` 条评估记录覆盖**至少 2 个独立归一化 `runtime` 或 2 个独立归一化 `model_family`**（直接复用 `S11` 开放世界归一化函数，无封闭模型白名单，遵循 `CCG-009` / `SKILL.md:145`）；**每一条评估**必须精确覆盖全部声明 `scenarios`（不漏场景、不重复、无未声明幽灵 ID）且全部为 `verdict: PASS`（严禁多数票或均值掩盖单模型 `FAIL`/`BLOCKED`）；严禁混入 waiver 字段。
   - **`single-model-waived`（不可用应急逃生阀，fail-closed）**：仅当第二运行时/模型家族确实不可用且**用户显式签认**（`waiver_owner: user`，严禁任何代理自批）时允许，须同时提供 `waiver_reason`、相对路径 `waiver_record_ref`、`followup_recheck_condition` 及 `>= 1` 条全场景 `PASS` 评估，并在交付报告中诚实标注单模型例外而非宣称双模型验证。
3. **生产接线与 S11 不可退役防线对齐**：在 `scripts/validate_core_gates.py:main(...)` 中将 `references/self-evolution-rule.md#multi-model-joint-forward-evaluation-gate` 加入 `NON_RETIRABLE_SECTIONS`，新增 `validate_multi_model_eval_guard`（锁定 owned 可见正文最小短语集）与 `_validate_backlog_sim_multi_model_evals`（自动校验 `BACKLOG.md` 全部 `sim-multi-model-eval` / 顶层 `coverage_status` YAML 块，强制规范字符串键名并按 `key in record` 拦截 `dual-covered` 混入 waiver 字段，兼容无 `docs/iteration/` 的分发与运行时副本，双解析器 `PyYAML` 与 `simple_yaml_load` 一致）。

## 3. 拟改文件清单（Files to Change — 仅批准后执行）

- **Phase A（本轮仅提案实际触及）**：
  - `openspec/changes/add-multi-model-eval-gate/{proposal,design,tasks}.md`
  - `openspec/changes/add-multi-model-eval-gate/specs/skill-workflow-governance/spec.md`
  - `docs/review/2026-11-20-S12-multi-model-eval-gate-draft.md`
  - `docs/iteration/BACKLOG.md`（仅追加 `S12` 待批行）、`docs/iteration/CURRENT.md`（仅登记待批轮次）
- **Phase B（须获 `迭代优化skill：已批准 add-multi-model-eval-gate` 后方可修改）**：
  - `references/self-evolution-rule.md`
  - `references/skill-iteration-loop.md`
  - `scripts/validate_core_gates.py`
  - `tests/test_workflow_rules.py`
  - `distribution/codex-plugin`（通过 `scripts/build_codex_plugin.py .` 刷新）
  - `openspec/specs/skill-workflow-governance/spec.md`（归档合并）、`CHANGELOG.md`、`docs/iteration/{BACKLOG,CURRENT,LOG}.md`
- **明确排除**：不改 `SKILL.md`、不改 `templates/learning-candidate-template.md`、不改 `references/shared-global-governance.md`（治理 v6）、不改 `references/project-learning-closeout.md`、不新建状态文件、不引入多账号并发调用、零触碰 6 组历史脏工作区文件。

## 4. 拟议规则片段（Exact Rule Snippets — 尚未生效）

### 4.1 拟增至 `references/self-evolution-rule.md`（紧随 `## Provenance-Gated Rule Retirement` 之后）

```markdown
## Multi-Model Joint Forward Evaluation Gate

For **Major Self-Evolution** changes that modify portable behavioral prose
(`SKILL.md`, `references/*.md`, or `templates/*.md` declared in
`references/cross-cli-portable-manifest.json`), forward-test evidence must guard
against single-model overfitting across the shared multi-CLI harness. Patch and
Minor slices, ordinary business projects, and non-behavioral script/test-only
changes are exempt.

Record the dual-YAML evaluation summary in `docs/iteration/BACKLOG.md` using
`record_kind: sim-multi-model-eval` (never `status: promoted`, no new state
file) under one of two fail-closed closure modes:

1. **`dual-covered` (default)**: Run the full declared `scenarios` set across at
   least two distinct normalized `runtime` values or two distinct normalized
   `model_family` values (open-world normalization reusing `S11` rules, no
   closed model allowlist). Every evaluation must cover every declared scenario
   with `verdict: PASS`; a failing model cannot be averaged or outvoted.
2. **`single-model-waived` (outage fallback)**: Permitted only when a second
   runtime/model family is genuinely unavailable and explicitly approved by the
   user (`waiver_owner: user`, non-empty `waiver_reason`, relative
   `waiver_record_ref`, `followup_recheck_condition`, plus at least one
   full-scenario `PASS` evaluation). Agents may never self-waive, and final
   reports must disclose the waiver instead of claiming dual-model verification.
```

### 4.2 拟修改 `references/skill-iteration-loop.md`（`## One-round sequence` 第 6 步，行 62–66）

```markdown
6. 按 Self-Evolution 执行 quick_validate、`scripts/validate_core_gates.py`
   与受影响 unittest；路由或 description 变更跑现有 unittest 全套。
   quick_validate 使用带 PyYAML 的 Python，项目验证与测试也须通过
   dependency-free fallback。Major 须有 RED/GREEN forward-test；
   当 Major 变更修改便携行为正文（`references/cross-cli-portable-manifest.json`
   内的 `SKILL.md`、`references/*.md` 或 `templates/*.md`）时，须满足
   `references/self-evolution-rule.md` 的 `Multi-Model Joint Forward Evaluation Gate`
   （`dual-covered` 全场景全 `PASS`，或经用户显式批准的 `single-model-waived`，
   记录于 `docs/iteration/BACKLOG.md` 的 `record_kind: sim-multi-model-eval` 块）；
   Patch/Minor 及非行为脚本/测试改动豁免。保留原有 profile 对应的 Review 与完成条件。
```

## 5. 验证与前向测试计划（Validation & Forward-Test Plan）

- **本轮（Phase A，仅验证提案与既有基线未破损）**：
  - `/opt/homebrew/bin/openspec validate add-multi-model-eval-gate --strict`
  - `design.md` 两套 YAML schema（`dual-covered` 与 `single-model-waived`）双解析等价核验（`PyYAML` 与 `simple_yaml_load`）
  - `/opt/anaconda3/bin/python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .`
  - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_core_gates.py .`（no-PyYAML）与 `PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 scripts/validate_core_gates.py .`（PyYAML）
  - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_distribution.py .`
  - 单账号原生 `readonly-reviewer` 独立只读审查提案草稿与 Delta Spec（R1 -> R2 `FOCUSED_RECHECK` `PASS`）。
- **批准后（Phase B）**：
  - 先写 RED 测试覆盖 `NON_RETIRABLE_SECTIONS` 拒绝退役 `references/self-evolution-rule.md#multi-model-joint-forward-evaluation-gate`、`validate_multi_model_eval_record` 正负全集（有效 `dual-covered` 跨运行时与跨模型家族含 `deepseek-v4`；有效 `single-model-waived`；拒收数字/YAML 保留字键名、同运行时别名+同家族子档、漏场景/重复场景/幽灵场景、单模型 `FAIL`/`BLOCKED` 混 `PASS`、非 `user` 自批 `waiver_owner`、`dual-covered` 按键存在性 `key in record` 拒收含空/null 的 waiver 字段、`status: promoted` 即使 `decision_owner: codex`、非法 `evidence_ref` 穿越路径）及 `main(...)` 对 `BACKLOG.md` 违规块（含大写/尾空格 fence 与行内注释）拦停、嵌套 `coverage_status` 非误报和 `validate_multi_model_eval_guard` owned 可见正文变体拒收；实现后转 GREEN，双解析器结果等价。
  - 运行全量校验：
    - `/usr/bin/python3 -m py_compile scripts/*.py`
    - `/opt/anaconda3/bin/python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .`
    - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_core_gates.py .`（no-PyYAML）
    - `PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 scripts/validate_core_gates.py .`（PyYAML）
    - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_distribution.py .`
    - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 -m unittest discover -s tests -v`（主仓 + 干净树无 PyYAML fallback）
    - `PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 -m unittest discover -s tests -p test_workflow_rules.py -v`（PyYAML）
  - 运行 2 场景隔离只读 forward-test（场景 1：Minor 豁免不死锁；场景 2：Major 便携正文改动缺第二模型且无用户 waiver 时被阻断），按 S12 自身契约以身作则完成跨模型家族/运行时串行评估（单账号无并发，若第二模型/运行时不可用则须请求用户显式签署 `single-model-waived`），**并在进入 Implementation Review 之前将 S12 自举的 `record_kind: sim-multi-model-eval` 块（附真实 `evidence_ref` / `waiver_record_ref`）写入 `docs/iteration/BACKLOG.md` 并重跑双解析 `validate_core_gates.py .` 验证通过**。
  - 通过独立只读 Implementation Review（`same_instance=false`，同时核验代码、测试与已落盘的 S12 `sim-multi-model-eval` 块及 `evidence_ref`）后，执行四端（`codex` / `pi` / `antigravity-cli` / `grok-cli` 含 `grok inspect --json --consume`）3 文件 schema-v2 scoped sync（`references/self-evolution-rule.md`、`references/skill-iteration-loop.md`、`scripts/validate_core_gates.py`；治理块 v6 不变）与 `verify-all`。
  - 归档 OpenSpec 合并主 spec（`openspec validate --specs --strict`），完成 `CHANGELOG.md` 与 `docs/iteration/{BACKLOG,CURRENT,LOG}.md` 更新并重跑双解析 `validate_core_gates.py .` + `validate_distribution.py .`，随后由**独立 Final Reviewer**（区别于执行者与 Implementation Reviewer，`CCG-007` & `CCG-016`）核验合并主 spec、完整最终 diff 与四端 `verify-all` 证据拿到 `PASS` 后，仅做纯状态收口（`BACKLOG` `done`、`CURRENT` `idle`、归档 `tasks.md` 末项勾选）、`check_commit_text.py` 与精确提交推送。

## 6. 回滚路径（Rollback Path）

- **Phase A 仅提案回滚**：直接删除 `openspec/changes/add-multi-model-eval-gate/` 与 `docs/review/2026-11-20-S12-multi-model-eval-gate-draft.md`，还原 `docs/iteration/{BACKLOG,CURRENT}.md` 本轮追加行（不触碰 6 组历史脏文件与任何运行时）。
- **Phase B 批准后回滚**：推送前从 `/private/tmp/osc-backup-<timestamp>` 恢复；推送后通过 `git revert <commit>` 并走 `scripts/validate_cross_cli_sync.py` 事务同步四端还原。

## Specific Approval Record

- **Current status**: **APPROVED FOR PHASE B IMPLEMENTATION**（actual user command: `迭代优化skill：已批准 add-multi-model-eval-gate`，2026-11-20）
- **Frozen approved OpenSpec artifacts (draft-v2)**:

| Approved artifact | SHA-256 at approval |
|---|---|
| `openspec/changes/add-multi-model-eval-gate/proposal.md` | `b465cbf5c55a909c55482b72610fa98a00ea48980d87e100512e879b23bd77af` |
| `openspec/changes/add-multi-model-eval-gate/design.md` | `fc17283be19a606e77d35e0263542c956ccb4c75c7f2e52bbfc9b019d4ee2db5` |
| `openspec/changes/add-multi-model-eval-gate/tasks.md` | `59f887ae376af5f4a9bc932c6b31905b4f32f2178a5a3d120031016de6e48441` |
| `openspec/changes/add-multi-model-eval-gate/specs/skill-workflow-governance/spec.md` | `189efbb133fb2c70b817c6958f75525dd355fcc478c41bce336f489f799d41c8` |

本段记录事实性批准快照后即冻结，不向本文件追加后续 Review 或收尾结果。
