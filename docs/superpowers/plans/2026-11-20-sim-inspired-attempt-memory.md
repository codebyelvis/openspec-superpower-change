# RSI / SIM 映射到 Skill 自进化的落地计划（v2）

Author: elvis
日期：2026-11-20
来源：`arXiv:2611.18856v1`（Self-Improvement Memory Enables Continual Recursive Self-Improvement），经 X 帖 `akshay_pachaar/status/2123030996899774607` 引入
基线：`main` `HEAD = b629d7c`
执行方：切换 Gemini 4 Neon 后按 `迭代优化skill` 协议执行

> v1 纠偏：v1 把 P0 放在 `/autoloop` 返修历史上。那是 policy 做业务任务的返修，论文明确说 SIM 服务 optimizer、不服务 policy，属于跑偏，已降为不做项。

## 0. 概念映射（论文 → 本仓库）

| 论文 | 本仓库 Self-Evolution |
|---|---|
| Harness `H` | 本 skill：`SKILL.md`、`references/`、`scripts/`、validators |
| Policy `M` | 日常运行 skill 的模型/CLI：Codex、AGY（Carbon/Neon/Opus）、Pi、Grok |
| Optimizer（Proposer + Selector） | 执行 `迭代优化skill` 的 Agent + 独立只读 Reviewer |
| Evolve 反馈 `F_t` | Review finding、forward-test RED、用户纠正、autoloop 失败 |
| 运行历史 `D_t` | Git 历史、`docs/iteration/LOG.md`、`docs/review/*` |
| Transfer（CRSI） | 换模型/换窗口续做自改；四端同步后同一 harness 服务多模型（§4.3.3） |
| SIM | **缺失**：按根因聚合的尝试记录（改动+理由、测前预测、实测结果含失败、provenance） |

当前缺口证据：

- `LOG.md` 按切片时间序记录，不按根因聚合；失败/被推翻的尝试散落在 `docs/review/*`，例如 Minor-autoloop-hardening 首轮 3×P2+2×P3 只在汇总行出现。
- 自改流程没有测前 `predicted`，验证后只记 PASS。
- 规则没有 provenance（哪个模型/CLI、因哪次失败加入），换模型继续优化时 optimizer 看不到理由，对应论文中 Harness Transfer 的失败模式。
- 本次 Neon 调研 → Opus Review → Neon 实现，本身就是一次跨模型续做，正是 CRSI 场景。

## 1. 切片 1（Minor，核心）：Self-Evolution 尝试记忆

口令：`迭代优化skill：自进化尝试记忆（SIM）`

### 存放位置（不新建文件）
复用 `docs/iteration/BACKLOG.md` 已有的“按机制分组的候选详情 + Candidate Card YAML”作为 SIM 的问题条目（problem entry）。每个切片/候选详情下追加 `attempts`。
若用户明确同意新建单文件（如 `docs/iteration/SIM.md`），再改用独立文件；默认不新建。

### 改动
1. `templates/learning-candidate-template.md`：YAML 新增可选字段
   ```yaml
   root_cause:          # recurring problem this card belongs to (SIM problem entry)
   attempts:            # append-only; keep failed / reverted attempts
     - provenance:      # model + cli + date + slice, e.g. gemini-4-neon / agy / 2026-11-20 / S10
       change:          # files + what changed + rationale (1-2 lines)
       predicted:       # RED cases / Review findings expected to turn green, written BEFORE verification
       observed:        # fixed / missed / reverted, written AFTER verification
   ```
   Rules 追加：attempts 只追加不覆盖；被推翻的尝试保留并标 `reverted`；仍受脱敏规则约束。
2. `references/skill-iteration-loop.md`（对应论文 Appendix D.2 的 optimizer 使用准则，压缩为 4 条）：
   - One-round sequence 第 3 步后：修改某条规则或脚本前，先读 BACKLOG 中引用该文件/机制的 `attempts`；
   - 实现前在 CURRENT 写 `predicted`，验证后写 `observed`，收尾时追加到对应条目 `attempts`（Review 首轮被打回的修复也算一次 attempt）；
   - 使用准则：先复用已有诊断；理由沿用，实现需按当前模型重新评估；已测失败的方向只有出现新证据才重试；不匹配任何已有诊断时新建条目；
   - 明确写：`predicted/observed/attempts` 仅为 optimizer 记忆，不是完成条件、不签发证据、不改变 Review 判定，不进入日常业务热路径。
   - Reading budget 表“起轮或恢复”行：BACKLOG 读取范围包含与当前切片相关条目的 `attempts`（仍按当前决策取行，不全量预加载）。
3. 回填（只做一条，验证格式可用）：为 `Minor-autoloop-hardening` 在 BACKLOG 补一条简短条目，含 R1 首轮 3×P2+2×P3 → 修复 → FOCUSED_RECHECK PASS 的 attempts，provenance 标注当时模型/CLI。不批量回填历史。
4. 不改 `SKILL.md`、`project-learning-closeout.md`、`docs/engineering-invariants.md`。

### 验收
- forward-test（Minor 推荐）：隔离 fixture 中给一条带 `attempts`（含 1 条 reverted）的条目，用新会话执行一次只读“规划修改该规则”，检查输出引用了已有 rationale，且没有重提已标 reverted 的方案。1 个场景即可。
- 若测试锁定模板字段或迭代协议字段子集，同步更新断言（先 `grep -rn "independence_rationale\|decision_provenance" tests/`）。
- `validate_core_gates.py` 的阅读预算静态检查保持通过。
- 两个文件都在便携清单（`references/cross-cli-portable-manifest.json:27`、`:42`），需要四端同步。

## 2. 后续候选（本轮不做）

| 候选 | 级别 | 论文依据 | 说明 |
|---|---|---|---|
| 规则退役：依据 provenance 删除只为早期弱模型添加的规则 | Major | §4.3.2：Gemini 4 Argon 上 Fresh RSI 95.6 高于续做 94.8 | `project-learning-closeout.md:138` 规定退役规则正文须走 Major；需 OpenSpec 提案 + `迭代优化skill：已批准 <change-id>` |
| 多模型联合评估：自改的 forward-test 至少覆盖 2 个不同模型/CLI | Major 或 Minor 视是否成为门禁 | §4.3.3：多模型联合反馈 75.24，持平各模型专版 75.20，高于单模型迁移 | 作为门禁则改证据规则，属 Major |
| `/autoloop` 返修尝试历史 | 不属于 SIM | 论文 SIM 不服务 policy | 有独立价值可另提，不挂 RSI 名义 |

## 3. 通用闭环（按 `references/skill-iteration-loop.md`）

1. 起轮读取：`SKILL.md`、`references/skill-iteration-loop.md`、`references/self-evolution-rule.md`、`docs/iteration/{BACKLOG,CURRENT}.md`；CURRENT 写入切片 id、备份路径、`predicted`。
2. 备份到 `/private/tmp/osc-backup-<timestamp>`。
3. 实现 + forward-test。
4. 校验：
   - `/usr/bin/python3 -m py_compile scripts/*.py`
   - `/opt/anaconda3/bin/python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .`
   - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_core_gates.py .`
   - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_distribution.py .`
   - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 -m unittest discover -s tests -v`，并在 `/private/tmp/<parent>/openspec-superpower-change` 干净树中跑一次无 PyYAML fallback（`<parent>/` 下软链 `codex-brief-antigravity-review`）
   - 受影响时运行 `scripts/build_codex_plugin.py .`
5. 单账号原生 `readonly-reviewer` 子代理做独立只读 Review，拿到 `PASS`（最多 2 轮 FOCUSED_RECHECK）。
6. `scripts/validate_cross_cli_sync.py` 四端 plan → apply → `verify-all`（路径用 `/private/tmp/...`，含 `grok inspect --json`）。
7. 收尾：更新 CHANGELOG Unreleased、BACKLOG（本切片自身也写 attempts）/ LOG，CURRENT 回到 idle；`check_commit_text.py` 校验；只精确 `git add` 本切片文件；commit + push 当前分支；清理 `/private/tmp/osc-*`。

## 4. 硬边界

- 6 组历史脏文件零触碰：`docs/engineering-invariants.md`、`tests/test_external_grok_control_plane.py`、`openspec/changes/allow-one-external-grok-control-plane/**`、`docs/learning-candidates/2026-11-11-external-grok-control-plane-and-companion-closure.md`、`openspec/changes/archive/2026-11-11-allow-one-external-grok-control-plane/**`、`openspec/specs/external-grok-control-plane/**`。
- 默认不新建状态文件；不改触发范围、审批、证据签发、完成权；`predicted/attempts` 不得做成阻断门禁（一旦需要即升 Major，停在提案）。
- 不做规则退役，不做自动 RSI 外循环，不引入外部依赖。
