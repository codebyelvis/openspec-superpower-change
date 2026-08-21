# Plan Review: Codex Skill Update 6.4 Blocker Resolution

- 文档类型：Implementation Plan Preflight Review（read-only）
- 日志及版本：2026-08-06 / Grok Review-only session / plan rev `docs/superpowers/plans/2026-08-06-codex-skill-update-6-4-blocker-resolution.md`
- 结论：`需修改`
- 验证范围：
  - 计划全文
  - `openspec/changes/add-codex-skill-update/tasks.md` Task 6.4
  - `openspec/changes/add-codex-skill-update/specs/skill-update-governance/spec.md`（transaction/rollback 相关）
  - 已安装证据：`registry.json`、`audit-bindings.json`、`controller-state.json`、schedule report/receipt、LaunchAgent plist 存在性
  - 兄弟源码测试：`codex-skill-update/tests/test_update_engine.py`、`test_skill_contract.py` 中计划点名方法是否存在，以及 `PYTHONPATH=tests` 下可运行性抽检
  - 账号根：`/Users/elvis/.codex`、`/Users/elvis/.codex-account-a`、`/Users/elvis/.codex-account-wb/skills` 只读对照
- 模式：Review-only；本 review 仅落盘结论，不修改被审计划，不授权执行

## Gate 0（本 review）

1. Mode：Review-only / plan preflight
2. References：`openspec-superpower-change/SKILL.md`、`references/request-modes.md`、`references/response-patterns.md`
3. OpenSpec：已有 approved change `add-codex-skill-update`；本计划声明为 Task 6.4 evidence recovery，不提出 contract delta —— 分类合理
4. Superpowers：执行前需 `executing-plans` 或 `subagent-driven-development`；本 review 不加载实施 sub-skill
5. Risk：strict；下一步 = 修订计划后重新 Preflight，用户批准后再执行

## 问题与风险

### 阻塞项（必须改计划后再执行）

1. **Durable evidence 落点缺失（High）**  
   Completion evidence 要求返回 discovery graph 表、测试命令/exit code、rollback instruction、no-drift checks 与最终 PASS/BLOCKED，但 non-goals 禁止写入 skill-update 下的 audit/report/receipt/plan/registry 等，且计划未指定允许写入的 durable 路径（例如 `docs/design/evidence/add-codex-skill-update/...` 或 Major workspace 下只读-可追加证据目录）。  
   后果：6.4 证据可能只留在会话文本，无法支撑 Task 6.6 High Review、checklist 勾选与后续 closeout。  
   **修改要求：** 明确 1 个允许的 sanitized evidence 输出路径与最小字段清单；禁止把 raw CLI 长 trace 写入 durable 文件。

2. **Task 2 → Task 3 证据交接断裂（High）**  
   Task 3 的 fresh Codex prompt 要求 “Verify ... the isolated rollback-test evidence”，但 Task 2 仅跑 unittest，未规定测试结果如何落盘、哈希或路径供 fresh process 读取。  
   后果：独立 `codex exec` 进程无法核验不存在的“rollback-test evidence”文件，只能猜测或空转。  
   **修改要求：** Task 2 结束后将 focused test 命令、exit code、时间戳写入上述 durable evidence 文件；Task 3 只引用该路径，不要求进程重跑测试或臆测结果。

3. **“discovered / discovers” 验收语义不闭合（High）**  
   Task 6.4 原文要求在 fresh process 中 verify managed packages 与 every mapped discovered entry/projection。计划优先使用 `CODEX_HOME=/Users/elvis/.codex-account-wb`，而 registry 绑定：
   - companion/router/superpowers → shared `/Users/elvis/.codex/...`
   - updater → `/Users/elvis/.codex-account-a/skills/codex-skill-update`  
   实测 `account-wb/skills` 已有同名 `openspec-superpower-change` / `codex-brief-antigravity-review` 等本地入口，**自动 discovery 的根与 registry-bound effective root 可能不是同一路径**。Acceptance matrix 中 “discovers the intended shared roots” 可被误读为 process skill inventory 通过即可。  
   先前 blocker 正是 “account-a automatic discovery was not proven”；本计划以 multi-root registry 权威 + 显式 limitation 报告替代跨账号自动发现，方向合理，但 **PASS 条件必须写死为 registry-bound path identity 验证**，而不是 CODEX_HOME 下同名 skill 自动发现。  
   **修改要求：**  
   - 在 Acceptance matrix / Task 1 Step 3 / Task 3 统一写明：6.4 本切片的 “verify discovered entry/projection” = 对 registry-bound effective path 做 `lstat`/`readlink`/内容或树身份核验 + 记录 process `CODEX_HOME` 与任何自动发现局限；  
   - 明确禁止把 `account-wb` 下同名 skill 当作 registry mapping PASS；  
   - 若执行者把 “automatic discovery of all four under one CODEX_HOME” 仍当作必达条件，则本计划在无 discovery-switch 时只能产出 `BLOCKED_DISCOVERY_ROOT`，不得静默 PASS。

### 非阻塞但应修补

4. **Rollback instruction 覆盖面偏窄（Medium）**  
   Task 2 同时跑了 package receipt-bound rollback 与 schedule remove/restore 测试，但 retained instruction 只描述 schedule-remove。Task 6.4 的 “tested rollback instruction” 更贴近 post-success package/runtime rollback 语义。  
   **建议：** 保留两条已测试、明确未对 live 执行的指令：  
   - package/post-success receipt-bound rollback（对应 AuthorityTransactionRecoveryTests）  
   - schedule-remove（对应 RegistryScheduleNotificationTests）

5. **Fresh process 命令与控制面身份（Low）**  
   计划写 control-plane owner 为 “current Codex session”，与 Grok 做 plan review 不冲突，但执行时必须仍由 Codex 控制面审计 evidence 并记录 6.4 决策；外部 `codex exec` 输出只能作 evidence。建议在 Task 4 Step 3 再写一句 “only control-plane records the 6.4 PASS/BLOCKED transition”。

6. **Package 观测字段缩写（Low / 事实澄清）**  
   计划中的 `UPDATE_AVAILABLE` / `ELIGIBLE` / `BLOCKED_ADAPTER_BINDING_INCOMPLETE` 等与 schedule report 字段一致（分别对应 `freshness_status` / `apply_eligibility` / `reason_codes`），内容核对通过。建议在证据表中使用报表原字段名，避免后续 High Review 字段对不上。

## 事实核对（通过项）

| 断言 | 结果 |
| --- | --- |
| registry SHA-256 `bc272c33…bae1` | 与文件及 `controller-state.registry_sha256` 一致 |
| audit-bindings SHA-256 `5020a34c…25d3` | 与文件及 `controller-state.audit_bindings_sha256` 一致 |
| 四 package effective roots 分割 | companion/router/superpowers → `.codex`；updater → account-a |
| entries=4, projections=2 | 与 registry 一致 |
| updater symlink → `188f94b4…/payload` | 存在且匹配计划 |
| 点名 unittest 方法 | 均存在；`PYTHONPATH=tests` 下 `test_receipt_bound_rollback` 可绿 |
| schedule receipt `transaction_result=SUCCEEDED` | 与 receipt 一致 |
| superpowers / updater package `transaction_result=BLOCKED` | 与 report 一致 |
| 无 mutation 授权边界 | 清晰；禁止 audit/plan/verify、launchctl 变更、Git、cleanup、discovery switch |
| 不单独宣称 whole-task completion | 明确禁止勾 tasks.md / archive / closeout |

## 摘要

计划在 **安全边界、非目标、停止条件、多根 registry 权威、fake-adapter 回滚测试替代 live rollback** 上质量高，哈希与测试锚点大体可执行。  
但作为 Task 6.4 evidence recovery 的 **Preflight 仍未通过**，因为：

1. 没有 durable evidence 落点；  
2. Task 2 结果无法被 Task 3 fresh process 核验；  
3. “discovered / discovers” 在 multi-home + 同名 skill 并存时的 PASS 语义未写死，存在误 PASS 风险。

这些问题属于计划修订，不需要 OpenSpec contract delta。

## 后续建议

1. 修订计划：补齐 evidence 路径、Task 2→3 交接、discovery 验收语义；可选补全双 rollback instruction。  
2. 修订后重新 Preflight Review；PASS 后再请求用户批准执行（含一次 fresh model invocation）。  
3. 执行顺序保持：Task 1 图对账 → Task 2 隔离测试并落盘 → Task 3 fresh process → Task 4 控制面裁决。  
4. 即使 6.4 PASS，`superpowers` adapter incomplete 与 `updater` DIVERGED 仍须作为可见 residual 进入 6.6，不得被本计划“洗白”为已治理消除。

## 本 review 不授权

- 不授权执行本计划  
- 不授权任何 schedule / registry / discovery / Git / cleanup 变更  
- 不将 Task 6.4 标为完成  
- 不修改被审计划文件（仅落盘本 review）
