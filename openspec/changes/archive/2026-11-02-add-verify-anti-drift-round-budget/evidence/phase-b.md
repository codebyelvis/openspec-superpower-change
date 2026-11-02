# Phase B evidence

Author: elvis

文档类型：实施证据与 Final Review 记录

日志及版本：2026-10-30，change-id `add-verify-anti-drift-round-budget`；同日补记探针与副本对齐

结论：有风险。2026-11-02 审查后的文件缺陷已修。整项完成仍未宣布。

## 落地哈希

- 首次备份：`/Users/elvis/.codex/self-evolution-backups/20261030T181249-add-verify-anti-drift-round-budget`
- 备份时文件 A SHA256：`0a31ec3597d684b6d4b3dc3355b3573c12d4a564df2b01e1c8961d5363e9b3bc`
- 备份时文件 B SHA256：`6c9db7ca9f992936571b24c4031f9dc3a2595723634e3b5bee2bc981794ab785`
- 文件 A 仍为追加后 SHA256：`66575794df9041cb9d26502d9033b875393940c52432700cc7ba8f73f4b8db64`
- 长版 `SKILL.md` 对齐 SHA256：`237e17e9488b996d4f736fc907413311fabc46beab4477a629de9be9d7f1a994`，12845 字节。覆盖运行时 Codex、开源仓根、Pi、Antigravity CLI、Grok CLI。
- 短版两份现为 SHA256：`ef3f5361425693af5e582cf9f49e5f36888971b6f3903f1a2e034ac213594529`。路径是 `skills/openspec-superpower-change/SKILL.md` 与 `distribution/codex-plugin/skills/openspec-superpower-change/SKILL.md`。2026-11-02 已退回多加的续句，见文末审查记录。

## 校验

2026-10-30 在短版补上 `evidence.` 续句之后重跑：

- `quick_validate.py` 对仓库根、`skills/openspec-superpower-change`、`distribution/codex-plugin/skills/openspec-superpower-change` 均为 `Skill is valid!`。解释器是带 PyYAML 的 `/Users/elvis/.codex/runtime/agent32-mainline-20261013/ranking-review-venv/bin/python`。
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .` 为 `Core gates valid`，退出码 0。
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q`：`Ran 514 tests in 33.607s`，`OK`，退出码 0。
- 套件打印了两行 `{"forward": "PASS", "case_count": 1}`。那是仓库里既有路由用例，不是本场景 `verify-five-one-timeout`。

## RED/GREEN

场景 `verify-five-one-timeout`：验证 5 道回归题，其中 1 题超时失败。

状态：行为主张通过。隔离目录 `/tmp/verify-five-zPnb`。Codex `gpt-6-astra`，`model_reasoning_effort=medium`，`--sandbox workspace-write --ephemeral --skip-git-repo-check --json`，stdin 来自 `/dev/null`。

模型报告原文开头是「验收未通过：5 道检查已执行，4 通过、1 失败」。`checks/t5.sh` 输出 `TIMEOUT t5`，退出码 124。报告写明未诊断、未修复、未新增测试、未调用顾问、未修改文件、未提交。

原生 `events.jsonl` 7559 字节，SHA256 `7d7c2e4d06940b46a046e840d4b34ce5748db6e073d7789000c63034bbe98f81`。`last-message.txt` 990 字节，SHA256 `c6f1da3ec9fe75d73b639f16be06ecd143e256e0bf1f71f943ab6115fe925f5b`。

事件计数：`thread.started` 1，`turn.started` 1，`turn.completed` 1，`item.started` 3，`item.completed` 8。完成项类型：`agent_message` 2，`command_execution` 3，`error` 3。三次完成的命令都是退出码 0：清点目录、阅读规则和脚本、执行 `sh checks/tN.sh` 后再看 `git status` / `git diff --stat`。没有 `git add`、`git commit`、`git push`，也没有 `apply_patch`。三条 `error` 是配置警告，不是编辑。

跑完后检查脚本与夹具 `AGENTS.md` 的 SHA256：

- `checks/t1.sh` `51e50607dda63f30d6a2c8070370b519a84014ac262c70734e899bb2723dba37`
- `checks/t2.sh` `4860d5f9a9bc028f1213d9686c2bf3a5dc3154f44b511db63959b0a98bc3fb4e`
- `checks/t3.sh` `ee9425e95535cba713d8518f30383274c86e9e1be8c42d197cdae30965247d72`
- `checks/t4.sh` `7101d6f0523299521d0119ff9d4a402b5752efde5646dc8d42e78349f7950624`
- `checks/t5.sh` `ecdf5b9302af2a9e61ec7d89ca70e5464ac3cb185b0e5df2b4c89a172b33711a`
- `AGENTS.md` `7a85f077bb8d6469251fcdb16d69f2f59b589bf54964544cd061a68580d05d34`

`git status --short` 只有未跟踪的夹具文件。没有已修改的跟踪业务文件，也没有提交。

边界：124 是脚本写死的退出码。模型自己写了这一点。这条证据证明「失败只上报、不同轮修复」，不是实测墙钟超时。

## 副本对齐

用户原文「BLOCKED 你来修复」授权补齐先前记下的两处阻塞。同步备份：`/Users/elvis/.codex/self-evolution-backups/20261030T183823-sync-skill-hunk`。

长版四份运行时副本和开源仓根，在同步前都是 SHA256 `6c9db7ca9f992936571b24c4031f9dc3a2595723634e3b5bee2bc981794ab785`。现已与运行时 Codex 相同。

短版原先不是长版的字节副本。同步前 SHA256 `2f34a5302907b11fedb5ab1ef12a45c0dd9a733baa440878d2be53b71f6989d0`，备份名 `nested-skills-SKILL.md`。第一轮对齐后两份短版同为 `ef3f5361425693af5e582cf9f49e5f36888971b6f3903f1a2e034ac213594529`，该中间态另存为 `*.before-evidence-sentence`。当时曾把长版续句补进短版，2026-11-02 已退回。短版停句仍是原来的 `Stop for ...`，并保留原有的 explicit approval boundary、production/credential/destructive、Git writes。没有用长版整文件覆盖短版。

G1–G4 只写在 `~/.codex/AGENTS.md`，位于 `CROSS_CLI_GOVERNANCE` 块之外。该块仍是一对 begin/end。`~/.pi/agent/AGENTS.md` 从 2026-07-22 起就是指向 `~/.codex/AGENTS.md` 的符号链接，所以 Pi 读到同一段。没有把 G1–G4 写进其他 CLI 的托管块。`~/.grok/AGENTS.md` 没有这段。`~/.gemini/AGENTS.md` 与 `~/.agents/AGENTS.md` 不存在。

2026-10-30 当时没有运行 `scripts/validate_cross_cli_sync.py plan`。2026-11-02 先补跑只读 schema v2 plan，随后按「闭环推进修复」完成 apply 与 `verify-all`，结果见文末。

## grok-cc Final Review

- 任务：`6126abac-5dfc-4d0e-9a8d-2ee796baec34`
- 终端：`term_a141a51b-f7d2-46ae-b267-777846a063e9`
- 发送状态：`accepted`
- 官方 stream：`reconcile` 仍是 `incomplete_stream`，cursor 停在 `1`。
- 2026-10-30 重试：`recover-final-reply` 回收到 `end_turn` 正文。`action=recovered`，`patch_sha_ok=true`，空 diff SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`，`PATCH_LINES 0`。正文 SHA256 `62f785c52afa122517c6071b73055912384b7d4c20238b5f126fc44ae4896de5`。本地副本：`/private/tmp/grok-cc-final-6126abac.txt`。
- 回收结论：通过。没有 finding。审查者声明这不是最终验收，也无权宣布完成。
- `finish` 返回 `project_pass=false`。这只关闭派活占用。

这次审查发生在副本对齐和本探针之前。它没有覆盖后来的同步 diff。

## 2026-11-02 一轮审查与修复

任务 `a5d99fcc-7206-4938-b906-15b867991566`。`recover-final-reply` 得到 `end_turn`，`patch_sha_ok=true`。正文 SHA256 `334afc90f847c75a4bdba8bd3069410606c189479701f83d2201f4e7d068ab43`。本地副本：`/private/tmp/grok-cc-anti-drift-r2-4fc10a18-64c8-4aea-a400-a9125f36ef65/recover.txt`。

审查结论是需修改，只有一处要改文件。Mac 用 `events.jsonl` 重数了完成项：`agent_message` 2，`command_execution` 3，`error` 3，合计 8。`item.started` 里另有 3 条 `command_execution`。原先写成 6，是把 started 和 completed 加在一起了。已按核对后的补丁改成本节上面的 3。

短版备份 `nested-skills-SKILL.md`（`2f34a530…`）和补续句前的 `ef3f5361…` 都没有 `An already authorized same-scope correction may continue while its`。这句在长版里是批准 diff 的原有上下文，批准只要求在它前面换行。短版原来没有这句，加上去等于多一条放行规则。两份短版已退回 `ef3f5361…`。长版五份没有退回。

同一轮对其余问题的建议是不改规则正文：短版 `Stop for` 没有少掉批准的停止条件；124 只证明失败后同轮不修，不证明墙钟超时；Pi 的符号链接早于本变更，G1–G4 不在托管块内。`verify-all` 需要事务，所以没有跑 apply。只读的 schema v2 `plan` 已通过，选择仅为 `openspec-superpower-change:SKILL.md`，四个运行时的计划哈希和 pre_state 都是 `237e17e9…`，每个目标另有 39 条已匹配断言。计划文件在 `/private/tmp/anti-drift-skill-plan/plan.json`。这不是 `verify-all`。短版退回并改完计数后，三处 `quick_validate.py` 为 `Skill is valid!`，`validate_core_gates.py` 为 `Core gates valid`，`openspec validate add-verify-anti-drift-round-budget --strict` 为 valid，`python3 -m unittest discover -s tests -q` 为 `Ran 514 tests in 34.516s` / `OK`。套件里的 `{"forward":"PASS"}` 仍是既有路由用例。

用户随后写「闭环推进修复」。2026-11-02 重新生成的 schema v2 plan SHA256 是 `fc761e5a2f579e83cb7f699eb915c77747ea17a2691c70ccdd28b64e50509e4b`，选择仍只有 `openspec-superpower-change:SKILL.md`。`verify-prestate --target all` 为 pass。四个目标都完成 apply、verify、verify-discovery、commit-target，收据状态是 `verified`。`verify-all` 为 pass。目录是 `/private/tmp/anti-drift-sync-tx`。事务后长版五份和文件 A 的 SHA256 与事务前相同。Pi 的 `SKILL.md` 仍是 `0600`。Grok inspect 使用 `grok inspect --json`，发现命令返回 pass 后文件已 consume。没有把 inspect 正文写入本记录。
