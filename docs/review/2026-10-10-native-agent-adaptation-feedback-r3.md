# 原生适配咨询反馈处理 r3

作者：elvis。日期：2026-10-10。处理者：`align-native-root`。
性质：owner 对已收齐的 Grok、Cursor、claudex 咨询输入的处置，不是 Preflight 或实施批准。

Claudex 回传结论为“有风险”：六文件候选静态成立，无需重做；恢复、事件机制和真实
消费验收仍 pending。报告自述产品 Claude Code、launcher claudex、advisory-input，
SessionStart session ID 为 `25832b15-d6c4-411b-9b16-de1a4e2d0a5b`。
这些身份数据来自用户转交文本，未取得本轮原生事件认证，不能升级为正式门禁签名。
独立原稿路径/hash 未交付，本文件是核实摘要，保留旧 r2 处理记录原字节。

## 三条建议的核实与关闭

1. **保留摘要边界已明确。** 重新计算六项摘要和长度均吻合。计算先删除 unique old
   exact-text，再通过现有 `_marker_parts` 去掉原受管 body，保留 start/end marker
   和其他 prefix/suffix 原字节；UTF-8 不归一化换行。Grok 摘要确实排除了没有被
   修改的 CCG body，因此另行检查原/候选 CCG body 字节相同、候选 canonical parity。
   定义进入 draft-v2 design/spec 和 r3 计划；原六文件候选 JSON 与全部候选 hash 不改。
2. **验收分成写前和写后两种证据阶段。** `event-mechanism-qualified` 表示写前
   命令、来源观察、事件审计、超时与副作用控制已合格；`native-load/behavior-accepted`
   表示写后候选生效的真实加载与行为接受。它们仅是本片证据阶段，不是新增 canonical
   status 或 Handoff 字段。旧配置证明不当作新候选通过，也不要求写前就证明候选生效。
3. **新增 P4 正式首行污染负例。** 个人“亮哥：”回复前缀保持。正式报告首行若为
   `亮哥：# Review Result: PASS`，应拒绝接受；正文与聊天外层分别检查。这项写入
   design/spec/tasks 和 r3 验收矩阵，本轮未做真实模型回放，不宣称 P4 native PASS。

## 新鲜准备证据

[隔离准备证据](2026-10-10-native-consumer-preparation-r3.json)：六项源 prestate/mode、
候选 hash、保留摘要/长度重新核验；在私有 fixture 调用现有 atomic_replace 做六次
候选替换和六次恢复，均回到原字节/模式，backup mode 0600。九项现有负例回归通过，
覆盖漂移、symlink/parent/candidate 替换、swap 后恢复与恢复期间漂移阻断。无 skip、
failure 或 error。fixture 根已清理，六个 native 文件未写，publisher 未调用。
这些证据支持复用现有原语，不等于尚未形成的 native approval/receipt/command 包。

[Codex 原生 prompt 检查](2026-10-10-native-consumer-codex-prompt-inspection.json)：
在空私有临时 cwd，继承现有身份分别指定默认 CODEX_HOME 与账户 A，原生
`codex debug prompt-input` 均 exit 0。输入列表各包含对应完整 AGENTS.md 一次，
不包含另一配置的完整 AGENTS；没有注入 project AGENTS，没有模型调用。
检查未在输入列表找到完整 model_instructions.md，因此不能据此证明该 base
instructions 加载或不加载。两项 AGENTS 组装机制已有实证，默认 model instructions、
模型事件/行为及其他入口仍 pending。raw 输出仅内存处理，不落盘、不摘录。
官方命令用途见 [OpenAI Developer commands](https://learn.chatgpt.com/docs/developer-commands#codex-debug-prompt-input)。

## 当前决定和剩余门槛

三份咨询已经收齐；本次修订不改六文件候选，不要求再发一次全量设计咨询。
提交审批的合同为 `align-native-consumer-projections` **draft-v2**。
原 draft-v1 五份提案文件保留在该 change 的 `revisions/draft-v1/`；旧 r2 计划、
candidate、反馈以及前一已完成变更的证据全部保持。

具体 draft-v2 批准尚未记录。完整恢复命令/receipt 包、原生事件机制资格及独立
Preflight 仍待实施前关闭；真实候选加载/行为是写后完成门。正式 attempt 与
publisher 的冲突继续按“停止发布”处理，既未互通，也不授权发布。
Superpowers、Grok 单 hook 隔离、开源工具试点和七名称八配置完整等价保持另案。

本轮是 proposal-only 与隔离准备，不修改可执行共享规则；重复注意事项已有工程
不变量覆盖，没有新的实际高严重性事件。当前反馈在本片工件中关闭，不重复晋升
全局规则。正式实施仍需要相应的确定性反例、学习审计和独立 Review。
