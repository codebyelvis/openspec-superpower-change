# 方案 A（更新策略 U1）提案复核

- **文档类型**：OpenSpec Proposal Review（独立复核）
- **日期**：2026-07-31
- **版本**：add-codex-skill-update / proposal-review-2026-07-31
- **结论**：**通过**
- **范围**：`openspec/changes/add-codex-skill-update/{proposal.md,design.md,tasks.md,specs/skill-update-governance/spec.md}`、`CONTEXT.md`、`docs/design/2026-07-30-governed-skill-update-review-draft.md`

## 0. 复核入口与边界

- 未进行任何代码或运行时状态变更；仅复核 OpenSpec 提案与治理约束。
- OpenSpec 决策：Major Self-Evolution / strict / control-plane-high，未越权到实现阶段。
- Risk/evidence：提案级别复核只做授权边界与机制一致性确认，不执行 Git/发布/安装。
- 结果：无阻塞性问题。

## 1. 关键哈希与投影

### 原始提案集合

- change-id：`add-codex-skill-update`
- `CONTEXT.md`（SHA-256）：`4b1fbf7c44863d502cc95c0938ce8433fad7894d84548b429153b3f52dffa5fd`
- `docs/design/2026-07-30-governed-skill-update-review-draft.md`（SHA-256）：`bfeae297d9766bb69b08478fe70adb0de3b66ed367e84cfeceadac4c937084fd`
- `openspec/changes/add-codex-skill-update/proposal.md`（SHA-256）：`2354ccc1aae092e409802e48efb1fb00b997d0365c94a7eaf22f0a40b4f3a03d`
- `openspec/changes/add-codex-skill-update/design.md`（SHA-256）：`a41f987f2fab4494bb87cab010f1f53162962325ec40795c82764cc61f7f572e`
- `openspec/changes/add-codex-skill-update/tasks.md`（SHA-256）：`d4e9c32a7ce2c10ae6526a2d5fc328d75f4c0d99f34c7ffd72c1cdfbc8d2b6c9`
- `openspec/changes/add-codex-skill-update/specs/skill-update-governance/spec.md`（SHA-256）：`d482ae3cd2a6a9d2743863e5af41a59805c0c5ce00f2344c156248d59261a4f9`
- `checklist-normalized contract-projection`（SHA-256）：`04e86ae925fb03efa579db74784ad4f141e0f9ace3365a5b3c9ebeb3cc5e66db`

### `openspec validate` 与基础校验

- `openspec validate add-codex-skill-update --strict`：`PASS`
- `quick_validate.py` / `validate_core_gates.py` / `python3 -m unittest discover -s tests -v`：`PASS`（142）

## 2. 覆盖项逐项复核

### 2.1 Source boundary 与权限边界

当前提案仅新增/修改了：
- OpenSpec 提案文本
- 本地上下文与 review draft（untracked，已作为批准素材）
- 验证/同步策略

未在提案阶段引入对 live repo 或代码树的直接变更权限；边界声明与任务 2.1 的 worktree 限制一致。**PASS**

### 2.2 Update authority 与授权载体

方案明确区分：
- 读请求（`audit`/`plan`/`verify`）；
- 状态变更通过 Router 进行；
- `allow_implicit_invocation` 仅用于窄域非变更场景；
- `$codex-skill-update` 为确定性入口；
- 每次实际 `apply`、`rollback`、`schedule`、`cleanup` 需要独立 Router 记录批准。  
无“伪造原生命令”或越权入口。**PASS**

### 2.3 Scheduler / apply-mutating paths

提案将 schedule 安装/替换/移除定义为 Router 事务，不与只读审计合并，并要求 `launchd` 参数语义严格校验；`Weekday=1`、`Hour=10`、`Minute=0` 在文档与验证说明中一致。  
未发现 schedule 可直接触发目标变更的路径。**PASS**

### 2.4 Adapters、rollback、recovery

公共 parser 对可见行为列举为 `audit`/`plan`/`verify`/`report`，不授予 mutation token；`git-symlink` 与 runtime lock 回滚均使用固定候选物与原子协议，失败后要求恢复与审计重入。  
`BLOCKED_SELF_UPDATE`、`RECOVERY_REQUIRED` 边界已写在提案与规范并被任务约束引用。**PASS**

### 2.5 Git/publication authority

提案与 tasks 明确不授权：
- git `init/commit/push`
- PR/release
- runtime 安装与 publication
  
明确说明仅在用户确认的 exact 变更下进入实现。**PASS**

## 3. 结果与后续动作

- 未发现阻塞项，未发现未闭环高风险 finding。
- 当前 revision 任务 1.4/1.5 均已通过收口；
- 复核结论与关键哈希已落盘为本文件；
- 用户明确同意当前变更粒度和提案范围后，可在 1.5 进行 exact 精确授权登记。  

## 4. 复核摘要

提案复核通过。关键结论：本版本在边界、授权、schedule、Adapter、recovery 与 git/publication 权限上闭环一致，且未出现“变更承诺缺失、路径越权、权限错配、或无依据的公开能力承诺”。  
