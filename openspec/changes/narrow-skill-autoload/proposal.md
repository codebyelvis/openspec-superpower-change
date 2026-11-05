# Change: Narrow skill autoload and lightweight context

## Why

`openspec-superpower-change` 的 description 将普通文件修改也作为自动触发条件；诊断停顿条款与当前请求已授权修复的情况冲突。`codex-brief-antigravity-review` 的主入口还向轻量审阅注入外部执行的角色分配与分类正文。

## What Changes

1. **BREAKING**：Router 仅在用户明确要求 OpenSpec、变更门禁、路由，或说「迭代优化skill」时加载；按用户后续补充，明确要求 archive/distillation 也是入口。普通实现、typo、格式、注释、非契约文档、已授权同范围继续修改和单独只读审阅不自动加载。
2. 用户当前请求已点名缺陷并要求修复时，诊断后直接执行那一处单假设修复；仅诊断仍停。失败两次、范围扩大、新根因、Git、生产、破坏性操作的停止条件不变。
3. Companion 的角色分配和 `ROLE_FIRST_REVIEW_CLASSIFICATION` 正文移入仅 Handed-off External Execution 读取的 reference。Standalone Lightweight 审阅输出仅为范围、发现、`PASS/FAIL/BLOCKED`、下一步。

批准、证据、完成、schema-6、control-plane 所有权、生产、凭据及破坏性 Git 边界均不变。有效 Handoff Contract 的治理要求全部保留。

## Impact

- Affected spec: `skill-workflow-governance`。
- Router 目标：`/Users/elvis/file/develop/opensource/openspec-superpower-change/SKILL.md`。
- Companion 仓库没有 `openspec/`；其目标路径由本 change 的 spec delta 管理，不新建第二套 OpenSpec。
- Companion 目标：`/Users/elvis/file/develop/opensource/codex-brief-antigravity-review/SKILL.md` 与 `references/handed-off-external-execution.md`。
- 本步只创建 proposal、design、tasks、spec delta。两边源码和安装目录中的 `SKILL.md` 均不修改。不进入 skill-iteration-loop，不加载 superpowers-adapter，不同步 Pi、Antigravity 或 Grok，不安装或配置 agent-autoloop，不重构。
- 校验通过只代表 proposal 结构有效。必须收到用户下一条明确批准后才能实施；不授权 Git 提交、推送、发布或运行时同步。
