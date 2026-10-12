# 原生适配咨询反馈处理 r2

作者：elvis。日期：2026-10-10。处理者：`align-native-root`。
性质：owner 对聊天 advisory-input 的核实与设计修订记录，不签署正式 Review 或实施批准。

Review 对象旧计划 hash 为
`962de1d729d7c0d876d71b88e82a1953b6cd5c4b1c61d203e1bd670e54d1760c`。
本轮收到两份文本：第一份按 Cursor 会话自述归类；第二份自述 `grok-cli`。
原稿独立路径/身份事件未交付，不能把本汇总当作各 reviewer 原稿或 hash 证明。
claudex 新版结果尚未收到。结论：旧计划确需修改；六文件投影可准备具体候选，
Superpowers 与 Grok 单 hook 隔离仍不具备写入条件。

## 核实结果和处置

| 发现 | 本机核实 / 处置 |
|---|---|
| CLAUDE.md 被两片修改却共享 prestate | 成立；合并成一次 CCG+路径候选，原 0600 模式保留。其余保护段不改 |
| 文件候选表不能表示七个入口 | 成立；r2 分离八配置台账与六文件候选。原七名称含两个 Codex 配置；claudex/claudeg 单独 session 验收 |
| 默认 Codex 与账户 A 的加载链不同 | config binding 成立；只提取 model_instructions_file 键，未输出完整配置。账户 A 无该键；native loading 仍待观察 |
| 共享发现证据不足 | 私有缺失不能否定共享；本宿主的可用 skill 目录确列出两项，但不能宣称独立 CLI 已加载 |
| Cursor CCG-004/014 旧内容 | 成立，hash 与旧表相同；用既有 managed primitives 生成当前 CCG，frontmatter/块外保持 |
| Claude/Cursor 投影也可能进入 Grok | 默认兼容文档成立；r2 增加 Grok 交叉验收。inspect 不能替代具体规则加载事件 |
| 计划默认三处与 Grok 强制 Review 落盘冲突 | 成立；候选绑定三处 exact text，Grok 整个 Review 交付段及后续引用一起改 |
| Publisher/Companion 文件名范围重叠 | 实际脚本纯函数 decide 拒绝 Companion 正式 *-review.md 的 Write；未执行 publish 或真实工具回放。r2 加 P1/P2/P3 共存门槛 |
| Superpowers 目录名不证明 Router 兼容 | 成立；正文 hash/版本真实，仍是 broad entry。候选降为待验证样本，Cursor 链接及相邻 5.0.7 方法全部保持 |
| broad entry 必然直接覆盖 CCG | 证据不足；using-superpowers 明写 user instructions 优先于 skill，静态触发张力不能直接推出运行冲突。版本/发现/方法混用仍未验收，所以不改链接 |
| Grok 单条禁用 key 未确定 | 成立；随包文档只给 Space/disabled-hooks 概念。无稳定兼容 key、隔离试验或回滚；保持阻断，拒绝 vendor-wide hooks=false / allow_managed_hooks_only |
| 工具 trial 没版本和命令 | 成立；三候选均排除，不启动试点，不把原调研当锁定版本接收 |
| 备份/恢复不具体 | r2 指定非发现目录和文件名/mode、恢复条件；真实恢复命令与故障注入仍是 Preflight 待办，未满足前禁止 HOME 写入，不宣称已经解决 |
| 没有七入口真实验收 | 成立；A–F/P1–P3 分类和逐入口 help 命令可供后续合同选择，尚无模型/native-load PASS |

## 本轮实际验证

六个普通目标文件、publisher、候选依赖 hash 与旧计划一致；CLAUDE.md 为 0600，
其余六文件候选表中目标为 0644。Cursor using-superpowers literal link text 为
`/Users/elvis/.codex/superpowers/skills/using-superpowers`，相邻方法也指 5.0.7。
两个 package.json 分别声明 5.0.7 和 6.4.2。没有 retarget。

[候选元数据](2026-10-10-native-agent-adaptation-r2-candidates.json) SHA-256
`662c5fc5547f610b5175dad81a8c0cd59f9eeebc0f03f15f7a361d9279a768f9`：
六候选在私有临时目录生成；exact replacements 均唯一，逆向还原均等于原文件，
受管 parity 成立；所有 586 个既有项目普通文件在新增 metadata 前 hash/mode 保持。
目标本机 hash/mode 不变。临时完整个人文件/候选/备份均已清理。

Publisher 未改，hash
`3ec6d1fd6945b619368794374b90a87c3c1abdc3c0f2b079fd186b135d9e5522`。
仅 import 并调用纯函数 decide，以下离线断言通过：Companion attempt review、
Grok docs/design/reviews review、publisher 会话 review 都拒绝直接 Write；
body.draft.md 不因 review 文件名保护而拒绝；LAUNCHERS 精确为 claudex/claudeg。
这些断言不证明 hook 运行、session 身份真实性或实际发布成功/失败。

两次只读 `grok inspect --json` 均 exit 0，捕获相同输出 SHA-256
`4da884c07eef74b64b96a085dcbd123f994241bd9d9bbba3769eb5c846361c99`。
只持久化最小审计摘要：guard 注册 2 条，事件 session_start / pre_tool_use，
compatibilityStatus 均 enabled；codeisland-hook.sh 注册 11 条，状态均 enabled。
脱敏遍历未取得 CLAUDE.md、两份 Cursor rules 或 native codeisland.json 的独立
来源记录，故不能声称每条规则的 native loading 或两处 codeisland 的来源保持
已经验收。没有 raw JSON 文件，未运行 hook、publisher 或模型会话。

help-only 检查：codex exec、claude、cursor agent、grok、pi、agy 均 exit 0。
确认 CLI 可用选项后写入 r2；没有把空 tools 字符串、plan mode、session 开关
视作免副作用保证。claudex/claudeg launcher 的模型轮次没有启动。

## 下一步及学习审计

见 [r2 计划](../superpowers/plans/2026-10-10-native-agent-adaptation-next-r2.md)。
已关闭的是文档设计中的 stale prestate、名单混用与未经验证依赖绑定；未关闭的是
真实恢复命令、原生事件加载/行为证明、稳定 Grok 单 hook 机制及最终实施批准。
这份记录不把 advisory-input 升为正式 gate-bearing PASS。

读取工程不变量与 learning closeout 后，本轮发现均落在已存在的
“Native consumption and evidence qualification stay scoped”与
“Reviewed runtime plan binds destination pre-state”范围。本轮仅候选/文档修订，
没有新的实际高严重性故障或执行规则变更，不新增一份重复全局规则或声称学习晋升。
本汇总保留本次核实和尚未闭合的门槛；后续实施仍应在审批范围内通过确定性反例
验证跨片 prestate、publisher 路径冲突和隔离失败，不能只靠本次散文记录。
