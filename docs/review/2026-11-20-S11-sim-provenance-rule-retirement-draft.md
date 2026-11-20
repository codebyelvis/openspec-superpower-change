# S11 基于 SIM provenance 的规则退役：Major 审查草稿

Author: elvis。日期：2026-11-20。版本：draft-v2（已收敛独立只读审查 R1 的 5×P2 + 1×P3 发现）。状态：**Major／仅提案待批，暂不实现**。
change-id：`add-sim-provenance-rule-retirement`。

## Gate 0 与本轮授权边界

- 模式：`Self-Evolution / proposal-only`（用户显式口令：`迭代优化skill：基于 SIM provenance 的规则退役（仅提案）`）。
- 级别：**Major**（涉及受治理 skill/workflow 正文退役条件、不可退役边界与静态门禁校验；按 `references/project-learning-closeout.md:138` 与 `references/self-evolution-rule.md` 必须先完成 OpenSpec 草案与严格校验，停在待批门禁，严禁提前实现）。
- 本轮已授权范围：仅产出 `openspec/changes/add-sim-provenance-rule-retirement/{proposal,design,tasks,specs/...}.md`、本审查草稿及 `docs/iteration/{BACKLOG,CURRENT}.md` 的待批登记，执行提案校验与独立只读审查；**严禁**编辑 `SKILL.md`、`references/*`、`templates/*`、`scripts/*`、`tests/*`、`distribution/*`、四端运行时、6 组历史脏文件或执行 `git add/commit/push`。

## 1. 已观察问题（Observed Failures & Evidence）

1. **强模型代际收益反转（`arXiv:2611.18856v1` §4.3.2 Table 1）**：在跨代模型链（Gemini 2.5 -> 3.5 -> 3.8 -> 4 Argon）中，持续继承历史补丁在早期代际带来增益（`+3.5` / `+1.6`），但到强代模型 Gemini 4 Argon 时，裸种子冷启动（`95.6`）反超持续继承链（`94.8`，`-0.8`）。为早期弱模型累积的防御性正文在强模型上可能变为冗余阻力。
2. **单模型特化毒害共享 Harness（`arXiv:2611.18856v1` §4.3.3 Table 2）**：在 Grok 4.20 / Claude Opus 5.5 / Gemini 3.8 Flash 三模型共享一套 Harness 时，基于单模型演化的改动迁移到其余模型得分显著下滑（`66.84–72.24` vs 多模型联合综合 `75.24`）。本仓库通过四端同步服务 `Codex / Pi / Antigravity CLI / Grok CLI` 多模型共享同一套 Skill。
3. **本仓库现有治理断层**：
   - `references/project-learning-closeout.md:138` 与 `openspec/specs/skill-workflow-governance/spec.md:1922-1924` 已锁定“受治理正文精简或退役须走 Major Self-Evolution 审批，且不得删除 `Non-Negotiables` 或 validator-locked phrases”；
   - `S10`（`b344a26`）已在 `templates/learning-candidate-template.md`、`references/skill-iteration-loop.md` 与 `docs/iteration/BACKLOG.md` 建立 append-only 尝试记忆；
   - 但目前缺乏**仓库锚定的不可退役白名单/黑名单、确定性双向举证结构与生产级 `validate_core_gates.py` 自动校验**。

## 2. 期望行为（Desired Behavior）

1. 任何受治理 skill/workflow 正文规则退役继续严格归属 **Major Self-Evolution**（必须经具体 `已批准 <change-id>`、独立 Implementation Review、四端同步与独立 Final Review），绝不降级为 Minor。
2. **四道硬门槛（全部满足，缺一 `BLOCKED`）**：
   - **仓库锚定的不可退役红线（Hard Exclusion）**：强制 `target_surface` 使用 `<project-relative-path>#<section-slug>`（拒收无路径别名、路径穿越与 `#L171` 纯行号锚点）；永久禁止退役受保护文件（`SKILL.md`、`references/shared-global-governance.md`、`references/completion-contract.md`、`references/step-evidence-gate.md`、`references/handoff-contract.md`、`references/confirmation-lease.md`、`references/agent-capability-routing.md`、`references/openspec-decision-rule.md`）、锁定章节（如 `references/self-evolution-rule.md#hard-prohibitions`、`references/skill-iteration-loop.md#authorization`、`references/skill-iteration-loop.md#reading-budget-for-one-round`、`references/project-learning-closeout.md#triggers`、`references/project-learning-closeout.md#enforcement-and-review`）以及 `non-negotiables`/`ccg-`/`validator-locked` 兜底词。同时诚实界定：静态函数拦受保护 `target_surface`，任意被删正文是否触及锁表短语的最终防线仍是运行 `scripts/validate_core_gates.py`。
   - **SIM Provenance 溯源**：必须提供可核验 `origin_anchor`（`BACKLOG.md` 条目、Git commit、已归档 OpenSpec change 或 `CHANGELOG.md` 锚点）。
   - **结构化双向举证（`retirement_basis` + 嵌套 mapping `retirement_evidence`，双 YAML 兼容）**：
     - `mechanical-superseded`：至少 **1 条**包含非空相对路径 `validator_or_test` 与 `negative_case` 的确定性机械覆盖证据；
     - `cross-model-internalized`：至少 **2 条**各含单一值 `runtime`、`model_family`、`probe_ref` 的证据（禁止在单值内夹带 `/,;|` 塞多模型），经开放世界确定性归一化（`agy -> antigravity-cli`、`grok -> grok-cli`、剥离尾部档位/版本如 `gemini-4-carbon`/`gemini-4-argon` -> `gemini`，**不维护封闭模型白名单**）后，归一化 `runtime` 去重 `>= 2` **或** 归一化 `model_family` 去重 `>= 2`。
   - **Append-Only SIM 墓碑与防复辟**：不新建状态文件，复用 `docs/iteration/BACKLOG.md` 记录 `record_kind: sim-retirement`（**无条件禁止 `status: promoted`，无论 `decision_owner` 为何值**）、双 YAML 兼容 `attempts`（`observed` 以 `retired` 开头）与明确 `reopen_condition`；无新失败触发 `reopen_condition` 时不得静默恢复已退役正文。
3. **生产接线**：在 `scripts/validate_core_gates.py:main(...)` 中同时执行 `validate_sim_rule_retirement_guard` 与条件 `docs/iteration/BACKLOG.md` 扫描（当该文件存在时自动校验全部 `record_kind: sim-retirement` 或含 `retirement_basis` 的 YAML 块，兼容无 `docs/iteration/` 的分发与运行时副本）。

## 3. 拟改文件清单（Files to Change — 仅批准后执行）

- **Phase A（本轮仅提案实际触及）**：
  - `openspec/changes/add-sim-provenance-rule-retirement/{proposal,design,tasks}.md`
  - `openspec/changes/add-sim-provenance-rule-retirement/specs/skill-workflow-governance/spec.md`
  - `docs/review/2026-11-20-S11-sim-provenance-rule-retirement-draft.md`
  - `docs/iteration/BACKLOG.md`（仅追加 `S11` 待批行）、`docs/iteration/CURRENT.md`（仅登记待批轮次）
- **Phase B（须获 `迭代优化skill：已批准 add-sim-provenance-rule-retirement` 后方可修改）**：
  - `references/self-evolution-rule.md`
  - `references/skill-iteration-loop.md`
  - `templates/learning-candidate-template.md`
  - `scripts/validate_core_gates.py`
  - `tests/test_workflow_rules.py`
  - `distribution/codex-plugin`（通过 `scripts/build_codex_plugin.py .` 刷新）
  - `openspec/specs/skill-workflow-governance/spec.md`（归档合并）、`CHANGELOG.md`、`docs/iteration/{BACKLOG,CURRENT,LOG}.md`
- **明确排除**：不改 `SKILL.md`、不改 `references/shared-global-governance.md`（治理 v6）、不改 `references/project-learning-closeout.md`、不退役本轮之外的任何具体既有规则、不新建 `SIM.md`/`RETIRED.md`、零触碰 6 组历史脏工作区文件。

## 4. 拟议规则片段（Exact Rule Snippets — 尚未生效）

### 4.1 拟增至 `references/self-evolution-rule.md`

```markdown
## Provenance-Gated Rule Retirement

Retiring governed skill or workflow prose remains **Major Self-Evolution**
requiring an approved OpenSpec change (`已批准 <change-id>`), independent
Implementation Review, required cross-CLI sync, and independent Final Review.
Every retirement proposal must satisfy four conditions:

1. **Repository-anchored non-retirable exclusion**: Express `target_surface` as
   `<project-relative-path>#<section-slug>` (no pathless aliases or line-number
   anchors). Never retire protected governance files (`SKILL.md`,
   `references/shared-global-governance.md`, `references/completion-contract.md`,
   `references/step-evidence-gate.md`, `references/handoff-contract.md`,
   `references/confirmation-lease.md`, `references/agent-capability-routing.md`,
   `references/openspec-decision-rule.md`), locked governance sections, or any
   `Non-Negotiables`, `CCG-*`, or `validator-locked` phrase. Running
   `scripts/validate_core_gates.py` remains the final mechanical check that no
   validator-locked phrase was removed.
2. **SIM provenance anchoring**: Cite a verifiable `origin_anchor` (BACKLOG SIM
   entry, Git commit, archived OpenSpec change, or `CHANGELOG.md` entry) naming
   the prior model/runtime failure mode that motivated the rule.
3. **Structured bidirectional retirement proof (`retirement_basis`)**:
   - `mechanical-superseded`: at least one structured evidence entry naming a
     deterministic `validator_or_test` path and `negative_case` that rejects the
     prior failure mode; OR
   - `cross-model-internalized`: at least two structured evidence entries
     (`runtime`, `model_family`, `probe_ref`) showing unhinted non-recurrence
     across at least two distinct normalized runtimes or two distinct normalized
     model families (open-world normalization, no closed model allowlist).
4. **Append-only SIM tombstone**: Record approved retirement in
   `docs/iteration/BACKLOG.md` using `record_kind: sim-retirement` (never
   `status: promoted`, regardless of `decision_owner`), a dual-YAML `attempts`
   entry whose `observed` starts with `retired`, and an explicit
   `reopen_condition`. Do not create a separate retirement state file.
```

### 4.2 拟修改 `references/skill-iteration-loop.md`（Step 3，行 50 起）

```markdown
   使用既有尝试记忆遵循 5 条准则：
   - 优先复用已有根因诊断（`root_cause`）；
   - 理由（rationale）可跨模型或跨轮次沿用，具体实现须按当前模型与环境重新评估；
   - 已测失败或标为 `reverted` 的方向仅在出现新证据时才重访；
   - 不匹配任何已有诊断时才新建条目；
   - 已被标为 `retired` 的规则仅在新失败证据触发其 `reopen_condition` 时才重审恢复，不静默复辟；受治理正文的规则退役本身始终属 Major Self-Evolution，须先走 OpenSpec 审批与 `references/self-evolution-rule.md` 退役门禁。
```

### 4.3 拟微调 `templates/learning-candidate-template.md`（`## Rules` 末条）

```markdown
- `root_cause` and `attempts` are optional, append-only Self-Evolution memory
  fields: retain failed, superseded, or retired attempts marked `reverted` or
  `retired`, write `predicted` before verification and `observed` after, and
  keep all entries within the redaction rules above. They are non-gating
  optimizer memory only and do not alter completion, evidence, or Review
  authority.
```

## 5. 验证与前向测试计划（Validation & Forward-Test Plan）

- **本轮（Phase A，仅验证提案与既有基线未破损）**：
  - `/opt/homebrew/bin/openspec validate add-sim-provenance-rule-retirement --strict`
  - `design.md` 两类退役 YAML schema 双解析等价核验（`PyYAML` 与 `simple_yaml_load`）
  - `/opt/anaconda3/bin/python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .`
  - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_core_gates.py .`（no-PyYAML）与 `PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 scripts/validate_core_gates.py .`（PyYAML）
  - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_distribution.py .`
  - 单账号原生 `readonly-reviewer` 独立只读审查提案草稿与 Delta Spec（R1 -> R2 `FOCUSED_RECHECK` `PASS`）。
- **批准后（Phase B）**：
  - 先写 RED 测试覆盖 `validate_sim_retirement_record` 全部 fail-closed 负例（真实受保护文件 `SKILL.md#routing-boundary` / `references/completion-contract.md#evidence`、锁定章节 `references/skill-iteration-loop.md#authorization`、纯行号 `#L171`、缺 `origin_anchor`/`reopen_condition`、非法 `retirement_basis`、同运行时别名 `agy`/`antigravity-cli` + 同家族子档 `gemini-4-carbon`/`gemini-4-argon` 碰撞、单值塞多模型 `gemini/claude`、开放接纳新家族 `deepseek-v4`、无条件拒收 `status: promoted` 即使 `decision_owner: codex`）以及 `main(...)` 对临时 `BACKLOG.md` 违规退役块的端到端拦停与 `validate_sim_rule_retirement_guard` 变体拒收；实现后转 GREEN，双解析器结果等价。
  - 运行全量校验：
    - `/usr/bin/python3 -m py_compile scripts/*.py`
    - `/opt/anaconda3/bin/python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .`
    - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_core_gates.py .`（no-PyYAML）
    - `PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 scripts/validate_core_gates.py .`（PyYAML）
    - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_distribution.py .`
    - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 -m unittest discover -s tests -v`（主仓 + 干净树无 PyYAML fallback）
  - 运行 2 场景隔离只读 forward-test：① 尝试退役受保护规则或仅单模型/同家族证据的规则被拒（`BLOCKED`）；② 新会话读取带 `retired` 墓碑与未触发 `reopen_condition` 的条目后不静默复辟已退役正文。
  - 通过独立只读 Implementation Review（`same_instance=false`）后，执行四端（`codex` / `pi` / `antigravity-cli` / `grok-cli` 含 `grok inspect --json --consume`）4 文件 schema-v2 scoped sync（`references/self-evolution-rule.md`、`references/skill-iteration-loop.md`、`templates/learning-candidate-template.md`、`scripts/validate_core_gates.py`；治理块 v6 不变）与 `verify-all`。
  - **独立 Final Review（`CCG-007` & `CCG-016`）**：在 `verify-all` 通过后、归档/commit/push 之前，由独立只读审查实例核验最终完整 diff、新鲜双解析测试与四端 `verify-all` 证据并拿到 `PASS`。

## 6. 回滚路径（Rollback Path）

- **Phase A 仅提案回滚**：直接删除 `openspec/changes/add-sim-provenance-rule-retirement/` 与 `docs/review/2026-11-20-S11-sim-provenance-rule-retirement-draft.md`，还原 `docs/iteration/{BACKLOG,CURRENT}.md` 中本轮追加行（不触碰 6 组历史脏文件与任何运行时）。
- **Phase B 批准后回滚**：推送前从 `/private/tmp/osc-backup-<timestamp>` 恢复；推送后通过 `git revert <commit>` 并走 `scripts/validate_cross_cli_sync.py` 事务同步四端还原。

## Specific Approval Record

- **Current status**: **APPROVED FOR PHASE B IMPLEMENTATION**（actual user command: `迭代优化skill：已批准 add-sim-provenance-rule-retirement`，2026-11-20）
- **Backup path**: `/private/tmp/osc-backup-20261120-103237`
- **Frozen approved OpenSpec artifacts (draft-v2)**:

| Approved artifact | SHA-256 at approval |
|---|---|
| `openspec/changes/add-sim-provenance-rule-retirement/proposal.md` | `834b661b64bb716bf2855e42c9ee9768ee6d4fdc077c023efd652a700845ab55` |
| `openspec/changes/add-sim-provenance-rule-retirement/design.md` | `68214eda49c2c09a586f4316723d744c62b965bc72110c6e234d9e1180c59dd0` |
| `openspec/changes/add-sim-provenance-rule-retirement/tasks.md` | `f3828e895dc9192c3a54e26dda53d51b73700f94f1141f97057bded3d4842ac3` |
| `openspec/changes/add-sim-provenance-rule-retirement/specs/skill-workflow-governance/spec.md` | `a78c03c634307ca12b2be899636876613176d6563960c038e143c38f8ce1aa28` |

本段记录事实性批准快照后即冻结，不向本文件追加后续 Review 或收尾结果。
