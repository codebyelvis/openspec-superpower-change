# Skill Iteration Loop

本协议把现有 Self-Evolution 门禁收成一轮可续跑过程。
一条口令只执行本 skill 仓库一个切片，结束即停，不进入无限自治。

## Entry commands

以下任一口令进入本协议，大小写与空格不敏感：

- `迭代优化skill`
- `迭代优化这个skill`
- `iterate this skill`
- `optimize skill closed loop`

附切片名时只做指定切片，例如 `迭代优化skill：落地迭代入口`。
Major 的实现口令为 `迭代优化skill：已批准 <change-id>`；须核对具体
已批准 OpenSpec change 与范围，不能把口令中的任意字符串当作有效批准。
无切片名时取 `docs/iteration/BACKLOG.md` 中最高优先级且未阻塞的一项。

## Authorization

| Level / approval | Authorized next action |
|---|---|
| Patch / Minor | One slice: edit, validate, local sync, commit and push this repository's current branch. |
| Major without `已批准 <change-id>` | OpenSpec change draft and review plan only; stop awaiting approval. No implementation. |
| Major with `已批准 <change-id>` | Implement only the specific approved OpenSpec change and scoped contract. |

Never push another repository.
No force-push, history rewriting, or remote branch deletion.
The command does not approve a Major change-id that does not yet exist.

口令不授权业务项目改动、削弱 Non-negotiables、自动升级 Superpowers 或
OpenSpec 上游、发布 npm 或宣称 skills.sh 上架成功；分发可见性仍是异步的。
Git 租约仅覆盖本切片的 add、commit 和本仓库当前分支 push，一轮结束即终止。
其他路径的 push 禁令不变；所有原有审批、证据、Review 与用户控制边界保留。

## One-round sequence

1. 读取仓库 `SKILL.md`、本协议、`references/self-evolution-rule.md`、
   `docs/iteration/BACKLOG.md` 与 `docs/iteration/CURRENT.md`。
   只按当前决策加载相关规则，不通读全部 references。
2. `CURRENT.md` 有未完成轮次时先恢复该轮，不新开；否则按指定切片或
   backlog 优先级选择一个切片并写入 CURRENT。
3. 声明 Self-Evolution / Gate 0，按实际影响分类；不确定按 Major。
   Major 先产出 OpenSpec change 草稿与审查计划，停在待批；只有具体
   `已批准 <change-id>` 的范围才进入实现。
4. 实现前创建结构化临时备份，记录恢复路径。备份不得放在 skill 发现目录。
5. 只改本切片允许的文件与行为。触发范围、OpenSpec/Superpowers 边界、
   证据签发、完成权声明仍属 Major；若碰到这些边界就停在提案，不能夹带。
   不改变跨 CLI 目标名单，不重复实现已有门禁与分发适配。
6. 按 Self-Evolution 执行 quick_validate、`scripts/validate_core_gates.py`
   与受影响 unittest；路由或 description 变更跑现有 unittest 全套。
   quick_validate 使用带 PyYAML 的 Python，项目验证与测试也须通过
   dependency-free fallback。Major 须有 RED/GREEN forward-test；
   保留原有 profile 对应的 Review 与完成条件。
7. 便携核心或治理块变更时读取 `references/sync-checklist.md` 和
   `references/cross-cli-sync.md`，执行 plan → 审查 → 授权范围内 apply →
   verify-all。目标仍是 Codex、Pi、Antigravity、Grok；失败记 BLOCKED，
   不跳过，不扩大同步范围。CURRENT 记录审查过的同步计划哈希。
8. 验证、Review 和所需同步通过后，更新 CHANGELOG Unreleased，标记切片
   done，追加 LOG，清空或归档 CURRENT；然后只提交本切片文件并推送
   本仓库当前分支。提交信息沿用既有风格，正文写切片 id。
9. 推送成功后删除本轮临时备份。推送或其他必需步骤失败时保留恢复所需
   备份，CURRENT 记录非空阻塞原因与恢复动作，不宣称完成，不开启下一项。
10. 报告只含：做了什么、验证与同步结果、commit、backlog 下一项、
    下一句口令。成功后下一句可为 `迭代优化skill：收敛 Superpowers 选择证据`；
    未完成时下一句恢复当前切片。

## Persistent state

- BACKLOG：每项记录 id、优先级、Patch/Minor/Major、来源、完成定义与状态。
- CURRENT：记录当前 change-id、切片 id、备份路径、验证命令与结果、
  同步计划哈希、commit、阻塞原因；未完成轮次优先恢复。
- LOG：追加式，一轮一行，字段为日期、切片、结果、commit、残留。

状态记录不替代 OpenSpec、现有证据或 Completion Contract，不签发新的完成权。
