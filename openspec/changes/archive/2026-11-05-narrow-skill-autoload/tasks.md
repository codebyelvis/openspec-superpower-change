## 1. Proposal only — 本轮范围

- [x] 1.1 核对两个仓库的 OpenSpec 结构和相关契约，确认 Companion 没有 `openspec/`。
- [x] 1.2 创建 proposal、短 design 和覆盖三项契约的 spec delta，列明跨仓库目标路径与不变边界。
- [x] 1.3 运行 `openspec validate narrow-skill-autoload --strict`，确认仅新增本 change 文件、两边源码及安装副本的 `SKILL.md` 未变。
- [x] 1.4 交付内容限定为 proposal 摘要和 change-id；本步到此停止，用户下一条明确批准仍待取得。

## 2. Implementation — 用户已批准，限本契约闭环

- [x] 2.1 取得用户对本 change 的明确批准，并核对与有效活动契约的重叠；不以提案校验替代批准。
- [x] 2.2 按批准契约收窄 Router description 与自动入口文字，并修正已点名且授权修复时的诊断停顿分支。
- [x] 2.3 将 Companion 角色分配与 ROLE_FIRST 分类正文移到 Handed-off 专用 reference，收窄 Standalone 审阅输出。
- [x] 2.4 对三项契约及不变边界执行适用验证与 Review；不得凭文本检查宣称真实运行时加载已验证。

本任务清单不授权同步 Pi、Antigravity 或 Grok，不授权安装、Git、发布或修改其他活动 change。适用的批准、证据及完成要求保持原样。

用户后续授权同契约校验对齐与闭环推进；额外目标和确切验证范围见 `design.md` 的 Approved implementation scope。

## Source verification — 2026-11-05

- Router description：旧文本 2 项失败，修改后 2 项通过。
- 主仓库：初次 506 项、1 error（forward runner 旧路径），修正读取路径后 506 项通过，0 failure/error/skip。
- Companion：RED 92 项、8 failures；GREEN 92 项通过，0 failure/error/skip。
- 双方 quick_validate、validate_core_gates / validate_templates（包括无 PyYAML 模式）、OpenSpec strict 与 git diff --check 通过。
- Pi 同一独立会话审阅发现旧读取路径，修复后复核 PASS；两轮只读前后 Git 状态和受审文件 SHA-256 均一致。独立 Codex 源码审阅 PASS。Review 是限定证据输入，不授予用户权限或 canonical completion。
- 文本探针：普通 typo 不自动加载；显式 OpenSpec 加载；诊断-only 停止；当前请求点名并授权修复则直接继续；Standalone 不读角色正文，Handoff 读完整 reference。
- 角色段与原 governor 内容字节保全；原 Router Non-Negotiables、YAML 注释夹具及 Caveman 义务保持不变。
- 没有安装、跨端同步、Git 提交或推送；当前安装副本未变。没有验证实际运行时自动加载、上下文隔离或 token 节省，不宣称全局 skill 优化已部署完成。

实际源文件修改范围：

- 主仓库：SKILL.md、scripts/validate_core_gates.py、tests/test_workflow_rules.py、tests/run_role_first_review_forward_tests.py。
- codex-brief-antigravity-review 仓库：SKILL.md、references/handed-off-external-execution.md、scripts/validate_templates.py、tests/test_workflow_rules.py。
- 本 change 的 proposal/design/spec/tasks 记录用户补充的 explicit archive/distillation 入口、授权和验证状态；未改其他活动 change。

### Description 原文

```yaml
description: "Use for file/behavior changes, change classification, OpenSpec/Direct Change routing, evidence-based completion, archive/distillation, or skill self-evolution. Excludes ordinary questions, standalone wording/read-only diff review, and valid handed-off batches. 用户说「迭代优化skill」或等价口令时，进入 skill 自身迭代闭环，读取 references/skill-iteration-loop.md。"
```

### Description 新文

```yaml
description: "Use only when the user explicitly requests OpenSpec, change gating (变更门禁), or routing (路由), says「迭代优化skill」, or explicitly requests archive/distillation. Do not auto-load for ordinary implementation, typo, formatting, comments, non-contractual docs, already-authorized same-scope continuation, or standalone read-only review. Excludes ordinary questions, standalone wording/read-only diff review, and valid handed-off batches. For「迭代优化skill」, read references/skill-iteration-loop.md."
```

## Authorized Codex installation and publication — 2026-11-05

用户随后明确授权同步安装与推送。本次只安装实际被 Codex 发现的两个 skill，继续排除 Pi、Antigravity、Grok 独立副本，不改全局治理块。以上 Source verification 中的未安装/未推送说明属于前一阶段。

- 使用 validate_cross_cli_sync.py scoped v2 计划，仅选择 5 个文件，36 个未选文件断言；Codex required，其余三端 not-applicable。
- Codex apply、verify、verify-discovery、commit-target 全部通过，事务收据为 verified；两个安装版 quick_validate 和无 PyYAML validator 均通过。
- 实际发现入口 /Users/elvis/.agents/skills/ 下两个链接仍解析到 /Users/elvis/.codex/skills/。安装后的主入口文本与本契约一致。
- 排除三端的 123 个 portable 文件哈希未变；managed rule 未选择。没有运行四端 verify-all，也不宣称四端同步完成。
- 安装保留原 runtime 已存在的其他任务内容：core validator 只引入本任务两个函数的修改。公开提交从 HEAD 精确提取本任务补丁，不包含其余未提交的 rebind/原生消费等工作。
- 精确发布候选重新验证：主仓库 486 项通过，Companion 92 项通过，均无失败、错误、跳过。主仓库数量比工作区 506 少 20，是未纳入其他任务未跟踪测试所致。候选 core validator、quick_validate 和 OpenSpec strict 通过。
- 本次暂存的 8 份源文件逐字节等于该已验证候选；此任务另外纳入四份 OpenSpec 制品。Git 推送结果由交付会话报告，不在提交前预记成功。
- 安装内容与发现路径校验不等于新模型会话的自动加载或 token 节省实证。

## Archive and project learning closeout — 2026-11-05

- 用户明确要求归档、蒸馏并推送 GitHub。Router 源码提交 72ceac33c5b7f63c712566d7eb38b56d8a300bca、Companion 源码提交 8074739271021a097f56b75222a3d83dcb54d3da 已发布到各自 origin/main。
- 本次归档只物化已批准的三项 spec 修改，不改变 SKILL、校验器、安装目录或其他活动 change。
- 项目蒸馏已写入 docs/learning-candidates/2026-11-05-narrow-skill-autoload.md 和 docs/engineering-invariants.md 的两节，复用现有回归，不增加运行时门禁。
- 学习验证：Router description 2/2、分类与scoped-sync 21/21、Companion角色2/2通过；独立审阅者另重跑Router7/7和Companion4/4通过，并返回学习Review PASS。
- 归档目录校验确认只有三项批准的 requirement 被物化，proposal/design/delta 原字节保留；精确归档发布候选486项测试、核心校验、quick_validate和spec strict通过。最终独立审阅核对上述证据及完整归档diff。真实模型自动加载、上下文隔离和token节省仍不在已验证范围内。
