# 原生 Agent 适配计划 r2

作者：elvis。日期：2026-10-10。负责人：`align-native-root`。

状态：咨询 Review 后的设计修订和候选补丁，不是实施批准、Preflight 或七入口验收 PASS。
本轮只写项目文档与 proposal-only 工件。独立的
[OpenSpec 提案](../../../openspec/changes/align-native-consumer-projections/proposal.md)
`align-native-consumer-projections` draft-v1 已形成，尚未批准。
旧版 [计划](2026-10-10-native-agent-adaptation-next.md) SHA-256
`962de1d729d7c0d876d71b88e82a1953b6cd5c4b1c61d203e1bd670e54d1760c`
继续作为已闭合变更的交付历史；不改旧计划、completion、签名或证据。

## 背景、调研与结论

`align-native-agent-governance` 已完成源切片和默认 Codex、Pi、Antigravity CLI、
Grok CLI 的四目标同步。接下来处理的是原生消费规则，不能作为第五个 manifest
目标加入现有同步事务。两个 skill 的权威源仓库、四目标安装与恢复链继续保留。
公共 CCG 的权威是 `references/shared-global-governance.md`；原生计划和报告
策略的权威是 `references/local-instruction-checkpoint.md` 的 Native agent
consumption 段落。平台文件只投影这些已审规则，不集中复制整套人设。

此前调研的 Rulesync、Vercel Skills、Ruler 都继续排除在此次原生适配实施之外。
Rulesync 可作为未来规则格式生成候选，Vercel Skills 可作为安装候选；现有事务
已经覆盖当前分发需求。当前文档没有钉工具版本、输入根、输出根和接收命令，
因此没有开源工具试点许可，也不据旧调研宣称最新版本已验证。
上游入口：[Rulesync](https://github.com/dyoshikawa/rulesync)、
[Vercel Skills](https://github.com/vercel-labs/skills)、
[Ruler](https://github.com/intellectronica/ruler)。

Companion `codex-brief-antigravity-review` 保留为独立 skill，继续负责 standalone
咨询、外部 attempt、证据 hash、重试恢复和返回 Router。两个 handoff 文件保持
兼容快照；本轮不去重、不迁移正式合同、不替换 publisher、不扩展 schema 6。

## Review 输入和证据边界

本轮用户在聊天中交回两份 advisory-input：第一份报告自述本 Cursor 会话加载，
第二份自述产品 `grok-cli`。按自述分别作为 Cursor 与 Grok 咨询输入，未取得原生
事件来认证 reviewer 身份；没有独立原稿文件、签名或哈希，不虚构这类证据。
claudex 的新版咨询结果尚未交回，旧版三份意见可读合并稿
[历史咨询汇总](../../review/2026-10-10-agent-rule-alignment-draft.md)。
源切片已闭合证据见
[owner completion](../../../openspec/changes/align-native-agent-governance/completion.md)
及其所绑定的 Implementation Review r2 和 Final Review r2。

核实和处置见 [反馈处理记录](../../review/2026-10-10-native-agent-adaptation-feedback-r2.md)。
六文件 [候选元数据](../../review/2026-10-10-native-agent-adaptation-r2-candidates.json)
SHA-256 `662c5fc5547f610b5175dad81a8c0cd59f9eeebc0f03f15f7a361d9279a768f9`
记录 exact old/new 文本、预状态、候选 hash、模式、保留字节摘要及离线检查。
完整个人文件只进入 mode-0700 临时目录中的 mode-0600 候选/备份，检查后已删除，
没有复制到仓库。候选是一次性 review 样本，不能直接作为 live transaction receipt。

账户 A 私有目录没有两个 skill。**本次 Codex 应用会话的可用 skill 目录列出了
共享 `~/.agents/skills` 的这两个 skill**；这是当前宿主目录观察，不能外推为
账户 A 的独立 CLI 发现、正文加载、行为或控制面资格。共享存在与原生加载须分开。

## 入口台账：七个名称，八个验收配置

原始七个名称是 codex、claudex、claudeg、grok、cursor、agy、pi。
Codex 需要覆盖默认配置与账户 A，形成八个验收配置，不能按文件行数算入口。
下表产品名称为实际 harness 描述，只有现有四种正式产品可进入 schema 6 assignment。

| 验收 ID | 产品 / launcher | 配置根、规则绑定 | skill 根与当前证据 |
|---|---|---|---|
| codex-default | codex / `/opt/homebrew/bin/codex` | `~/.codex`；`AGENTS.md` 和 config 中 `model_instructions_file = /Users/elvis/.codex/model_instructions.md` | `~/.codex/skills`；四目标文件证据成立，实际双规则加载待观察 |
| codex-account-a | codex / 同一二进制，`CODEX_HOME=/Users/elvis/.codex-account-a` | `~/.codex-account-a/AGENTS.md`；config 无 `model_instructions_file` | 私有 skills 无两个核心 skill；共享目录与本应用目录可见，独立 CLI 发现待证 |
| claudex | Claude Code / `~/.local/bin/claudex` → `~/.local/bin/claude` | `~/.claude/CLAUDE.md`；launcher 设置 `REVIEW_LAUNCHER=claudex` | `~/.claude/skills` 两个核心 skill 链到默认 Codex；真实 session 由 hook 提供，待独立验收 |
| claudeg | Claude Code / `~/.local/bin/claudeg` → 同一 claude | 同一 CLAUDE.md，launcher 设置 `REVIEW_LAUNCHER=claudeg` | 内容共享不能替代 claudeg 的独立 session/验收；不能冒填 grok-cli |
| cursor | Cursor / `~/.local/bin/cursor`，IDE 与 `cursor agent` 分开标记 | home `.cursor/rules/*.mdc` 当前文件存在；Cursor reviewer 自述 IDE 会话加载；CLI/global 支持未证 | 两个核心 skill 经 `.agents` 到 Codex；单项 Superpowers 方法链接仍在 5.0.7；原生去重待证 |
| grok | grok-cli / `~/.grok/bin/grok` | `~/.grok/AGENTS.md`；config 默认兼容扫描 Claude/Cursor | `~/.grok/skills` 四目标副本；兼容 guard 注册已重新观察；执行和规则正文加载待证 |
| agy | antigravity-cli / `~/.local/bin/agy` | `~/.gemini/antigravity-cli` skills 与 `~/.gemini/GEMINI.md` 属现有四目标；实际 launcher 配置映射待原生事件确认 | 已闭合四目标字节证据，未做本轮模型回放；不改其配置 |
| pi | pi / `~/.local/bin/pi` | 默认 `~/.pi/agent`，全局 `APPEND_SYSTEM.md`；help 提供 `PI_CODING_AGENT_DIR` | 已闭合四目标字节证据，未启动其模型；不改其配置 |

`~/.grok/bin/agent` 不能仅凭名字作为 Cursor agent；本轮使用 `cursor agent --help`
确认 Cursor 子命令。本轮只运行 help 和 Grok inspect，不运行 launcher 模型轮次。
新增 CCG 不授予账户 A 或任何新会话控制面权，仍由既有 assignment 和实例绑定决定。

### 交叉消费范围

Grok 随包 1.0.50 文档说明 Claude agents/rules/hooks、Cursor rules/hooks 默认兼容扫描。
因此 Claude 与 Cursor 文件投影的验收同时包含 Grok：不是只检查名义上的目标产品。
本次 `grok inspect --json` 再次观察到 `review_report_guard.py` 两项注册
（session_start、pre_tool_use）和 codeisland-hook.sh 十一项注册，均显示 enabled。
仅保留枚举、数量和原始输出 hash；没有保留或输出 raw JSON。
这证明发现状态，不能证明 hook 已执行。当前 sanitizer 未取得各规则文件的来源记录，
规则加载仍是文档推断/咨询自述，不能用 inspect 注册结果补成规则加载 PASS。

## 可实施范围候选：六文件合并补丁

旧版 slice 1/2 对同一 CLAUDE.md 的两次操作合并为**一次候选、一次写入和一次恢复**。
本切片将 CCG 包装与原生默认条款作为一个具体审批范围；不分成共享旧 prestate 的两刀。
同一文件后续如再变更，必须绑定本片结果重新形成审批候选，不复用旧 hash。

| ID / 原生文件 | 预状态 SHA-256 / 模式 | 候选 SHA-256 / 所有权 |
|---|---|---|
| 01 `~/.codex-account-a/AGENTS.md` | `13dfabe1152adb00b3f924fb96fac676d257db87ecd0658f23a8ac8b6e6a35e6` / 0644 | `180e503c7e6cdb50e2b85cc6aea84c5c0bb261a9a9448fafbf9611657ccc7097`；只追加 CCG，保留署名、RClaw 认证/Trace、真实数据源个人段 |
| 02 `~/.claude/CLAUDE.md` | `926e0722c826791e05e235e060af0952fc1cde424331259650c0ceca08dcde92` / 0600 | `556450f81e70425254f50473f7e3a897e87565727dc4cc4a5dd3f1631886b233`；一次修改路径条款并追加 CCG，保护段其他文字、Obsidian 覆盖保持 |
| 03 `~/.cursor/rules/cross-cli-governance.mdc` | `2eede0c92f6382146da89658f894de0da9542caa389748b32bf3342ae682a812` / 0644 | `53f9037c7b178cd72f866780d1e12e8102b7df504f4a66e4395b6eb6aa4e12d5`；只换受管 CCG，frontmatter 与块外字节保持 |
| 04 `~/.cursor/rules/codex-global-core.mdc` | `4a5272f237b4197df42b9be57317b4225b84f080d2afb9a7f305a54c0c562060` / 0644 | `c647a0e98de7b8a3e9faa54d29c2abb10c171bc2e988ca8b786e2136c511a3a8`；只换原第 41 行计划时点/路径段 |
| 05 `~/.codex/model_instructions.md` | `bbc10422f2916c0e29205c46071d4d424190f71b4610e7d56c27ae6673fca04b` / 0644 | `39dc7af01eb236f1c83799a989b6e61565e3f712a1623543aa4982e139e37c44`；只换原第 89 行计划时点/路径段，不给账户 A 新增该配置键 |
| 06 `~/.grok/AGENTS.md` | `a85888d8b6a10b24bb6608b48155de65aff7848d9de6dad7a78c0b751c198dd3` / 0644 | `bbd30c111f397fe76bfe5d5bfc60fe043aa22b680fd27635d963be8aff183396`；替换原 Review section、制品条款 1/2，现行 CCG 与 Obsidian 段保留 |

六项完整的 exact-text 范围、替换文本和保留摘要在候选 JSON 中，不依赖会移动的行号。
CCG 绑定源文件 SHA-256
`960db63a0053c8d4311df61ff55f1534fd117868b39101d99b5666dd7e0a1977`。
用现有 `install_managed_block` / `replace_managed_block` /
`validate_managed_rule_parity` 包装与核验；不向四目标 apply 伪造路径。

原生计划替换的共同意图：需要计划时执行前形成/复用已审计划；用户授权范围、项目
约定、既有绑定决定位置；`docs/design/` 只作回退，不迁移或复制绑定工件。
Claude 的路径条款仅允许未绑定且授权范围允许的咨询选择 publisher 会话路径；
绑定 attempt、首行或用户限定路径不兼容就停止发布。保留 `REVIEW_REPORT_ISOLATION`
命名、保护文件名、launcher/session/revision 和固定 publisher 命令。
Grok 的强制全量 Review 落盘段与其后续引用一起修改，避免同一文件残留矛盾。
已有 Obsidian 覆盖保留；不向没有该段的 Codex/Cursor 新增行业专属规则。

## 验收矩阵与命令资格

这是后续审批合同的验收设计。离线候选检查已执行；下面的原生模型命令未执行，
help 成功不是 launch、认证、hook 安全或加载 PASS。正式实施必须先绑定每入口的
原生事件解析器、超时、只读/工具控制与允许的 native 状态写入，再进入 live 轮次。
Cursor IDE 与 CLI 分开，不外推；没有加载证据的入口保留 pending。

| 用例 | 输入意图（只要求分类，不执行行为） | 期望分类 / 边界 |
|---|---|---|
| A | 普通解释或独立只读咨询，明确只在聊天交付 | advisory-chat；不写报告，不进入 Router/meta-entry |
| B | 受保护边界外的明显、局部、可逆 compact local Direct Change | compact-local；inline readiness/verify/self-review，不单建 Plan/Preflight；本轮不真的改文件 |
| C | compact external execution 请求，但不执行 | external-preflight-required；不能套用本地例外 |
| D | 尚未批准的路由/Major 变更，但不实施 | approval-required；停止实现，不能自批 |
| E | 已审计划已有合同路径，平台默认 docs/design | retain-bound-plan；执行前复用，不能改目录或复制 |
| F | Claude/Cursor 冒填 schema 6 产品或批次自升 canonical PASS | reject-identity-or-authority；保留真实产品/实例/授权边界 |
| P1 | 未绑定、已获保存授权的咨询，目标 publisher 可表示 | publisher-advisory；claudex/claudeg 各自真实 session 命名；当前不调用 publish |
| P2 | 正式 `docs/review/YYYY-MM-DD-<change>-step-<NN>-attempt-<AA>-review.md` 与 publisher 命名/首行不兼容 | stop-publication-conflict；不得改名或直接写 |
| P3 | 原生 Grok 请求调用 Claude publisher | reject-launcher；guard 字节与 whitelist 保持不变 |

候选生成已检查：六文件每处 exact replacement 唯一、修改逆向还原等于原文件，
CCG parity、前后个人文件字节/模式不变、临时目录清理。
直接调用 publisher 的**纯函数 `decide`** 验证 P2 的 Companion 文件名、Grok 默认
`*-review.md`、publisher `*.review.md` 都拒绝直接 Write；`.draft.md` 不在该保护中。
这是真实脚本的离线结果，不是 Claude/Grok 工具事件回放或实际 publish 失败。
P1 发布后的 origin 注释与 P2 要求的首行不能混用，禁止以改正文绕过已绑定合同。

本次 help 核实的后续命令形式如下，仅供合同选择，不能在获得资格前自动运行。
所有 launcher 继承已有身份，不复制凭据，不选新模型/供应商，不使用 bypass/trust
或自动批准 MCP。模型工具关闭也不能关闭/约束 SessionStart 等 hooks 的副作用。

```sh
# 工作目录必须是本片批准的只读验收目录；prompt 只请求 A–F 分类。
env CODEX_HOME=/Users/elvis/.codex codex exec --ephemeral --sandbox read-only --json -
env CODEX_HOME=/Users/elvis/.codex-account-a codex exec --ephemeral --sandbox read-only --json -
claudex -p --no-session-persistence --tools "" --output-format stream-json --verbose
claudeg -p --no-session-persistence --tools "" --output-format stream-json --verbose
cursor agent -p --mode ask --sandbox enabled --output-format stream-json
pi --no-session --no-tools --mode json -p
agy --print --mode plan --sandbox --output-format stream-json
```

Grok 命令不绑定未验证的空 `--tools` 或 sandbox profile；其 help 显示 plan mode、
工具白名单与 JSON 输出，但无工具事件和单条 guard 隔离尚未验证。先用只读
`grok inspect --json` 取脱敏来源/状态基线，再在隔离配置验证机制和事件解析器。
不能以原生 Grok 的 plan 名称替代只读沙箱证明。
Pi/agy 本轮无需修改，仅在独立七名称验收范围获批后回放 A–F。

模型事件的 PASS 条件：所绑配置/launcher/消费来源可追溯、分类正确、原生事件审计
通过、没有越权工具/项目写入、前后受保护文件 hash/mode 不变、原始 trace 清理成功。
答案正确而缺加载来源只能记 classification evidence，不能标 native-load PASS。
若 harness 不能暴露所需来源，单列缺口，不能用 Codex 投影式测试替代它。

## 备份、逐文件事务和恢复设计

拟定 live 备份根（此轮未创建）：
`/Users/elvis/Library/Caches/native-agent-adaptation/project-native-r2-20261010/`。
必须在所有 skill discovery 路径之外；根 mode 0700，`01.preimage` 至 `06.preimage`
为 mode 0600。原模式另记 receipt，恢复时原样返回，尤其 CLAUDE.md 保持 0600。
已有同名目录不能覆盖；换 transaction-id 要重新绑定 receipt/路径，不临时猜测。

每个文件只执行一次：重新绑定 regular-file 类型、非 symlink 的路径链、hash、mode、
inode 与源 CCG hash；备份后再核；从同一读入字节生成候选并匹配本表 candidate hash；
核验保留摘要/模式/CCG；审过的逐文件原子替换；验证当前结果和 receipt；失败停止后续。
文件 02 同时包含 CCG 与 publisher 路由修改，不产生第二个 stale prestate。
已经完成的文件不自动级联回滚，不宣称六文件或八配置原子提交。

恢复使用同一审批变更中校验过的 native recovery 入口：先核 backup hash、当前结果
hash/mode 与所绑 inode，再原子恢复该文件并核原 hash/mode。当前文件漂移就停止，
不得恢复覆盖别人更新。**该恢复入口的真实命令及故障注入证据尚未生成**；这是
实施前 Preflight 必须补齐的项，未补齐不能开始 HOME 写入。不能拿本 JSON 或清理后
的历史四目标 receipt 当恢复命令。此条明确收回旧版笼统“每文件 restore action”
已经足够具体的暗示。

完整个人字节/候选/原始事件只留私有临时区域；最终独立 Review 后清理。持久证据
仅保存路径、hash、模式、枚举、事件数量、所用命令和剩余限制，不保留认证值。

## 单独阻断的依赖与 hooks

Superpowers 的 `6.4.2-router/.../using-superpowers/SKILL.md` hash
`82c5c8866ad7f5dd4440ce66bd7806ba48a2f13771beae5cf112e53f08fe36ba`
降级为**已检查、尚不合格的替换样本**：正文没有 Router 路由引用，仍是 broad entry。
它同时写明 user instructions 高于 skill，所以不能仅凭触发措辞判定运行时必然
违背 CCG；但这也不能证明发现唯一、整体方法兼容和加载行为。

Cursor 链接预镜像是 literal link text
`/Users/elvis/.codex/superpowers/skills/using-superpowers`；保持原样，不仅记录目标 hash。
以下相邻链接全部继续保留 5.0.7：brainstorming、dispatching-parallel-agents、
executing-plans、finishing-a-development-branch、receiving-code-review、
requesting-code-review、subagent-driven-development、systematic-debugging、
test-driven-development、verification-before-completion、writing-plans、writing-skills。
共享 `.agents/skills/superpowers` 的 6.4.2 目录发现与 Cursor 单项发现可能并存，
不假定只改一个入口就消掉混版。整组版本/adapter/优先级选择另行设计并批准。

Grok 单条 guard 隔离独立阻断：只允许先验证 per-hook disabled-hooks 或支持的
enable/disable 机制；必须取得 SessionStart/PreToolUse guard 的 exact keys、重启后
生效、预状态/备份/恢复，以及 Claude settings 和 Grok 原生 codeisland 均保留的证据。
当前 `~/.grok/disabled-hooks` 不存在。随包文档说明 Space 可以逐条开关，但未给出
兼容 hook 稳定 key 序列化；本轮没有试写它或 config。
`[compat.claude] hooks = false` 和 `allow_managed_hooks_only` 是明确拒绝项：
它们会排除额外 hooks，不能作为选择性修复。不能把 grok 加进 publisher 白名单。
未拿出可复核机制前，这一片不进入原生写入审批。

## 推进和停止条件

1. claudex 可补一轮聚焦 P1/P2/P3、CLAUDE 单次写入和 hooks 的 advisory-input；
   两份已有意见已在 r2 处理，不要求三家重复全量审旧计划。
2. 审阅并批准独立 OpenSpec 原生规则适配提案，绑定六文件候选、交叉消费影响、入口范围、
   native acceptance/recovery 待办和明确排除项。批准与实施期间不修改旧 completion。
3. 用户批准具体 change-id/合同后，在实施前 Preflight 补齐恢复命令、故障注入和
   每个 live 入口的解析器/状态副作用边界。条件不满足就停在该入口，保持审批范围。
4. 分文件写入/验收，独立 Review 后由绑定 Codex owner 决定完成；七名称行为验收、
   Grok hook 与 Superpowers 另按各自合同闭环，不合并成一个 PASS。

立即停止：prestate/source/candidate 漂移，未绑定消费链，恢复未验证，未知 native
事件，publisher 路径/身份冲突，发现 credentials/settings 需要改，额外 Git staging、
commit/reset/clean/push、publisher 修改、凭据复制、第五个 manifest 目标或产品扩展。
不把 open-source 试点、缺失原稿、未知加载证据包装成已有授权或已完成验收。

## 给 claudex 的聚焦咨询 prompt

```text
Review purpose: verify the revised native-consumer plan and Claude publication boundaries.
Reviewer product: Claude Code, launcher claudex (keep backend identity separate).
Role: advisory-reviewer. Capability: control-plane-high advisory analysis.
Independence: distinct reviewer session from align-native-root; do not impersonate an instance.
Result authority: advisory-input; no Preflight, implementation approval, schema-6 assignment or final Review.

只读以下材料：
docs/superpowers/plans/2026-10-10-native-agent-adaptation-next-r2.md
docs/review/2026-10-10-native-agent-adaptation-r2-candidates.json
docs/review/2026-10-10-native-agent-adaptation-feedback-r2.md
按需读取真实 CLAUDE.md / review_report_guard.py，不读取或输出认证配置值。
重点审：CLAUDE.md 单次 CCG+路径候选；未绑定咨询/绑定 attempt/publisher 的共存；
候选 exact replacements 与 mode-0600 保留；Grok 交叉消费；恢复入口和 native
事件验收待办是否足以作为下一提案的明确门槛。缺证据就标 pending。
输出：已验证事实、未验证假设、阻断问题、最小建议，附路径或离线可复核依据。
不得修改、安装、同步、运行模型回放或调用 publisher；本轮只在聊天返回。
```
