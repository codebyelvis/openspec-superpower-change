# Tasks: integrate-governed-cli-autoloop

用户已批准实施，批准记录见 approval.json；当前执行阶段 1；2026-11-09按用户路径 A 收敛自动入口为 Codex + Pi，AGY保留受限直调/手动回退。proposal PASS 不等于实施或运行时完成。

## 0. Proposal preparation (authorized now)

- [x] 0.1 核对已提交基线、既有双模规则、CLI help 与 Autoloop 机制，隔离原工作树改动。
- [x] 0.2 编写 proposal、design、tasks 和 `skill-workflow-governance` spec delta，明确四阶段及禁止扩权。
- [x] 0.3 运行 `openspec validate integrate-governed-cli-autoloop --strict`，核对仅提案文件发生变化。
- [x] 0.4 用独立 Pi CLI 只读审阅完整制品；保留真实 session、被审文件哈希和前后工作区不变证据；处理同范围发现并复核。
- [x] 0.5 整理提案摘要、change-id、实际路径与审阅/校验结论；交付状态保持 `awaiting-user-approval`，未取得实施批准。

提案证据：`evidence/proposal-review.md`、`evidence/verification.json`。0.4–0.5 是 Review 后的事实记录；实施进度以以下勾选与阶段证据为准。

## 1. Direct CLI calls (after approval)

- [x] 1.1 固定三端调用实例、cwd、必要环境、精确恢复方法及验收命令；确认实际修改文件子集。
- [x] 1.2 对当前支持子集 Codex + Pi 完成真实非交互/精确续接/本次受限权限/正常终态及宿主截止验证；不将宿主截止外推为后端取消。AGY保留受限直调/手动回退。
- [x] 1.3 对阶段 1 实际改动运行对应验证与独立 Review；保留必要治理上下文和原有限复查规则。

## 2. Background mechanism proof (after phase 1)

- [x] 2.1 在 disposable fixture 核对每次 CLI 启动前的绑定会话检查、结果后身份检查和受支持恢复方式。
- [x] 2.2 实测业务 FAIL、CLI 故障、调用侧被杀、worker timeout/unknown；证明不能越限重执行业务或静默换实例。
- [x] 2.3 若无法证明，记录 BLOCKED 并保持后台入口禁用；不得用 Prompt/started 掩盖，不自动修改引擎。需要新实现时先修订精确源码/安装路径、接口与验证命令，并获批。
- [x] 2.4 仅在机制成立后接受独立 Review 及安装/回滚清单；测试插件命名、stop、排空、清缓存、保留审计记录。

## 3. Single VERIFY batch (after phase 2 PASS)

- [x] 3.1 明确测试命令、受测 revision、执行权限、产物写入范围及原有 schema-6 assignment；启用一个已授权的手动事件。
- [x] 3.2 取得真实报告、原始结果及 schema-2/哈希证据；FAIL/BLOCKED 不转 FIX，不修改业务源码或 canonical status。
- [x] 3.3 核对传输完成与治理结论分离，完成本批次独立 Review。

## 4. Bound controller return (after phase 3 PASS)

- [x] 4.1 在正确账户/cwd 与精确原主控 thread 上验证 queue 入队、恢复、消费和证据接受；未恢复时保留人工入口。
- [x] 4.2 验证失效/重复信封不重复推进；只有绑定主控依现有 validator 与实际 previous status 处理合法迁移。
- [x] 4.3 按实际修改范围完成必要源码验证、Review 和受控运行时同步；分别报告未启用项，不提前归档或宣称集成完成。

阶段 1 实测记录：`evidence/phase-1-report.md`、`phase-1-facts.json`、`phase-1-manifest.json`。1.2 未完成：权限与超时证据有明确缺口；阶段 2–4 保持未启动。

Pi 对阶段事实报告 R1/R2 Review PASS，临时入口空身份 P2 已关闭；不替代 1.2 完整验收，1.3 的正式阶段接受仍待完整证据。详见 `evidence/phase-1-review.md`。

2026-11-06 阶段1补证：AGY真实5秒超时返回exit3/finished_reason=print_timeout；同次init暴露非只读工具，1.2/1.3仍未接受。见 `evidence/phase-1-continuation-report.md`。本轮未独立Review，旧Pi PASS不外推；后台未启用。

2026-11-09 已接收Pi原始独立审查回执：continuation-20261106 REPORT_REVIEW PASS，7项raw+4项artifact共11/11哈希在本次修改前复核一致并保留原字节；不包含已更新的来源二进制。见 `evidence/pi-continuation-review-receipt.json`。历史BLOCKED报告保持原样，后续状态以本次支持子集新验收为准。

2026-11-09 当前支持子集运行证据见 `evidence/phase-1-supported-report.md`；独立Review未接受前1.3仍待完成，后台阶段未启用。

2026-11-09 最后Pi阶段验收Review在210秒宿主截止下退出143，没有有效结论；1.3保持未勾选。恢复材料见 `evidence/phase-1-review-resume-prompt.md`，此前运行探针通过但不替代该门禁。不得把超时会话当正常终态续接。

2026-11-09 独立Pi审查实例（`01a1afbe-e61b-768b-896d-8a743ed83565`，`independent-reviewer`/`control-plane-high`/`advisory-input`，与原绑定主控Codex `01a1aa6c-c4c8-7111-812f-02e1396290e7` 及本次受权收口执行者Pi `01a1bec5-45cb-76cc-9766-4c191329bdec` 严格分离，且不宣称与超时实例 `20804c85-aefd-4743-9848-b2f17d9f61cf` 为 `same_reviewer_instance`）完成阶段1支持子集（Codex + Pi）最终验收审查并给出 `REVIEW: PASS`（0阻塞发现；独立核验61/61 manifest文件哈希、3/3合同哈希、8/8源文件及24/24关键事件行哈希、3项内存逆向调用拦截全部通过；原始会话第148行 `event_id=3d0c120b` 单行SHA-256 `6a8e66d3d9e7359fbb16fedbf2451be963455daa2b1475b3730a6a4dbc56222e`，见 `evidence/pi-phase-1-supported-review-receipt.json`、`evidence/phase-1-supported-review.md`、`evidence/phase-1-supported-closeout.json`）。勾选 `1.3`；AGY保留受限直调/手动回退，阶段2–4后台入口尚未启用。

2026-11-09 阶段2隔离机制证明（`2.1`–`2.3`）已在 `/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/governed-cli-phase1-s58l8ops/phase2-20261109` 完成实测（见 `evidence/phase-2-report.md`、`evidence/phase-2-facts.json`、`evidence/phase-2-manifest.json`）：
- `2.1` 已完成：在隔离fixture中将启动前续接守卫收紧为初始阶段白名单（`if phase not in ('r1', 'timeout') and not identity:`），完成9项启动前绑定会话检查与结果后native ID核验（含扩展续接阶段名、调度器清空 `resume`、`unknown` 前序状态、后验换会话拦截）。
- `2.2` 已完成：在不修改 `~/.agent-autoloop/app/**`（223/223文件SHA-256零变化）且不消耗 `codex-a` 在线额度的前提下，驱动真实 `worker/worker.ts`、`worker/contract.ts` 与 `kernel/decide.ts` 实测5类场景，证实：封装存活时可将业务 `VERIFY FAIL` 与传输 `done` 分离；但在未达 `started` 的CLI故障下 `worker.ts:292`（`triedFresh`）会自动清空 `resume` 换新UUID重跑Turn 2，在调用侧被 `SIGKILL`（`exit 137`）与封装启动前拦截下 `decide.ts:289-332`（`retryLater`）会自动重派最多10次（`MAX_ATTEMPTS = 10`），在 worker 自身 `timeout` 下 `worker.ts:281-287` 硬编码忽略 `Adapter.read().text` 返回 `outcome: "failed"` 并触发 `retryLater`，在中台租约过期进入 `unknown`（`decide.ts:225`）后 `settleSession`（`decide.ts:116-127`）会静默抹除同线程后续轮次的显式 `resume`。
- `2.3` 已完成：按 `design.md` Decision 4 缺省决定，如实记录阶段 2 为 `BLOCKED`（`STAGE_2_BLOCKED_BY_ENGINE_MECHANISM_GAP`），停止阶段 2，保持后台 `autoloop` 治理入口禁用（`background_enabled: false`），继续使用阶段 1 已验收的 Codex + Pi 直接 CLI；`2.4` 及阶段 `3`–`4` 保持未启动，待独立 Pi 审查窗口（`01a1afbe-e61b-768b-896d-8a743ed83565`）只读 Review 与原绑定主控 Codex（`01a1aa6c-c4c8-7111-812f-02e1396290e7`）最终核认。

2026-11-09 已接收独立 Pi 审查窗口（`01a1afbe-e61b-768b-896d-8a743ed83565`）对阶段 1 收口落盘与阶段 2 `2.1`–`2.3 BLOCKED` 机制证明的正式验收回执 `REVIEW: PASS`（源会话第 `222` 行 `event_id=112f1a66`，单行去尾换行 SHA-256 `ca843eeb73f41af10ffa6f390bbda90bc2b5a2018c80eecadf6a362c81b09bf6`，已落盘 `evidence/pi-phase-2-review-receipt.json`；保留原 `evidence/phase-2-report.md`、`evidence/phase-2-facts.json`、`evidence/phase-2-manifest.json` 字节不变）。

2026-11-09 用户按 `tasks.md 2.3` 与 `design.md` Decision 4 明确批准修订阶段 2–4 实现边界（见 `approval-amendment-phase2-unblock.json`，SHA-256 `2db5b42026ff231d0fd4e50a82e7a3f5550cf2fb8999a6d0794cca6beeab1049`），在不修改 `~/.agent-autoloop/app/**`（223/223 文件 SHA-256 零变化）的前提下，采用宿主侧持久化 Attempt/Session 账本 + 受控 Runner 主动调用 `agent-autoloop stop <run-id>` 的外层受控适配器方案（`openspec/changes/integrate-governed-cli-autoloop/adapter/{govpi/agent.ts,gov_runner.py,tests/*}`），并将所有阶段 2–4 探针与运行证据固定在持久路径 `/Users/elvis/.local/state/governed-cli-autoloop/integrate-governed-cli-autoloop/`：
- 持久隔离机制证明（`adapter-proof-20261109`）已完成：复验 `2.1` 9/9 启动前白名单与结果后身份检查（`guard-2-1-results.json`），并通过 `adapter_mechanism_proof.mjs` 实测 `s1`–`s6` 共 6/6 场景（`adapter-mechanism-results.json`，`assertions: []`，`exit 0`）：(a) `s2`（Turn 1 CLI 故障 + `worker.ts:347` `triedFresh`）与 `s5`（`run 7` 租约过期 `unknown` + `decide.ts:121` `settleSession` 抹除 `resume`）均在启动 CLI 前由本地持久化账本拦截，落盘 `report-abort.md` 并以 `exit 0` 返回 `"执行中止：会话续接被拦截，已生成中止报告，禁止重跑"`，阻断 `triedFresh` 与 `retryLater`；`s6`（结果后会话身份不符）落盘 `report-abort.md` 并以 `exit 0` 返回 `"执行中止：结果后会话身份不符，已生成中止报告，禁止重跑"`；(b) `s3`（调用侧 `SIGKILL` `exit 137`）与 `s4`（worker 自身 `timeout`）进入 `retryLater` 后，在 `attempt 2` 启动 CLI 前由账本拦截并主动触发 `stop <run-id>`、落盘 `report-abort.md`、拒绝二次启动 CLI。
- `2.4` 已完成（`real-20261109-r3` 与 `real-20261109`，详见 `evidence/phase-2-unblocked-report.md`）：完成受管源码复制安装至 `~/.agent-autoloop/plugins/govpi/`（`use: "govpi"`）、`rules.json` 备份与新增 `gov-pi` / `gov.verify.*`、真实 `agent-autoloop stop 10`（及 `real-20261109` 中 `stop 3` 与 `attempt 2` 自动 `stop 4`）在途排空验证（状态转为 `cancelled`，进程完全退出）、`rules.json` 字节级还原（SHA-256 `16a403549c5080a3bd27f30c10901f130bb2f458750bb8f4ec7921973d9c30c5`）、插件移存至 `rolled-back-plugin-govpi`、`launchctl kickstart -k gui/501/agent-autoloop` 重启 worker 清缓存（`pid 2525 -> 11992`）及审计记录保留验证。勾选 `2.4`。
- `3.1`–`3.2` 已完成（`real-20261109-r3` Run `#11`，详见 `evidence/phase-3-verify-report.md`）：通过手动事件 `gov.verify.run` 触发单批次后台 `VERIFY`，由 `gov_runner.py` 在 worktree `11e339dae5f92fc21a75cbe16bcc9b078e24b11a` 执行固定命令 `openspec validate integrate-governed-cli-autoloop --strict`（`exit 0`），并调用只读 Pi（`--no-mcp --no-extensions --no-skills --no-context-files --no-prompt-templates --tools read,grep,find,ls --provider amd-radeon --model DeepSeek-V4-Flash`，不消耗 `codex-a` 额度，native session `01a1c320-0e21-7477-8df6-063eab185552`）生成带 Schema-2 manifest 的 `report.md`（SHA-256 `2cc3f95e78f996c71da099a4d2d07ee5832363204a40e0a99af784d0c3db1314`）与 `receipt.json`；未修改业务源码或 canonical status，无任何 Git 写操作。勾选 `3.1`、`3.2`；`3.3` 待独立 Pi 审查窗口（`01a1afbe-e61b-768b-896d-8a743ed83565`）只读复核，阶段 `4`（`4.1`–`4.3`）保持未启动。

2026-11-10 独立 Pi 审查窗口（`01a1afbe-e61b-768b-896d-8a743ed83565`，`independent-reviewer`/`control-plane-high`/`advisory-input`，独立于原绑定主控 Codex `01a1aa6c-c4c8-7111-812f-02e1396290e7`、派发执行者 Pi `01a1bec5-45cb-76cc-9766-4c191329bdec` 及后台 `VERIFY` 执行实例 Pi `01a1c320-0e21-7477-8df6-063eab185552`）完成阶段 2（`2.1`–`2.4`）与阶段 3（`3.1`–`3.3`）独立只读验收审查并给出 `REVIEW: PASS`（0 阻塞发现；独立重算 `evidence/phase-2-3-manifest.json` 全部 246/246 项磁盘文件 SHA-256 零误差、`/Users/elvis/.agent-autoloop/app` 223/223 文件快照 `fb8afd68...` 零变化、`openspec validate integrate-governed-cli-autoloop --strict` 退出码 `0`；源会话 `/Users/elvis/.pi/agent/sessions/--Users-elvis-file-develop-opensource-openspec-superpower-change--/2026-11-06T07-24-45-980Z_01a1afbe-e61b-768b-896d-8a743ed83565.jsonl` 第 `268` 行 `event_id=881e2990`，单行去尾换行 SHA-256 `8fb8e5ddb92edb416b77457f9b20b11538d1c8fba2b39a15b38a270b2bb64022`，见 `evidence/pi-phase-2-3-review-receipt.json` 与 `evidence/phase-2-3-closeout.json`；受审的 `evidence/phase-2-unblocked-report.md`、`evidence/phase-3-verify-report.md`、`evidence/phase-2-3-facts.json`、`evidence/phase-2-3-manifest.json` 保持原字节不变）。勾选 `3.3`；阶段 1–3 已全部收口完成，阶段 `4`（`4.1`–`4.3` 原绑定主控 `01a1aa6c-c4c8-7111-812f-02e1396290e7` 回传、证据消费与最终状态迁移）待主控额度恢复后执行。

2026-11-10 在原 Codex 主控线程恢复受阻（Codex TUI 不支持 ChatGPT 账户下的 `gpt-6.1-sol`、桌面端会话锁返回 `no operation was sent`）后，用户明确发出指令 `“我想让codex把收尾交给pi”`，按 `approval-amendment-phase4-pi-closeout.json`（SHA-256 `b4a0bb1d4d5c383bb83403df388770fd34084b21474c0de6acefad1bd7f8720c`）将本 change 阶段 4（`4.1`–`4.3`）收尾交接给受控 Pi 实例（`01a1bfdd-efd8-77b3-8bc6-7513429647ce`）并完成全部闭环（持久证据目录 `/Users/elvis/.local/state/governed-cli-autoloop/integrate-governed-cli-autoloop/phase4-20261110`，详见 `evidence/phase-4-report.md`、`evidence/phase-4-delivery-receipt.json`、`evidence/phase-4-pi-handoff-acceptance.json`、`evidence/phase-4-owner-manual-resume.md`、`evidence/pi-phase-4-review-receipt.json`、`evidence/phase-4-closeout.json`）：
- `4.1` 已完成：以 `?mode=ro` 只读连接核实原主控线程 `01a1aa6c-c4c8-7111-812f-02e1396290e7` 与队列项 `01a1c38b-9744-72b0-b07f-2e0ba5bf2f25`（`created_at_ms = 1794282067780`，`envelope_sha256 = 089e51c7e847fdbeb408146fa8b55c98d600bfb283b8dc97eeb64903d9a49341`），如实记录原 Codex 线程恢复受阻边界与人工恢复入口，并通过 `gov_return.consume_queued_envelope_via_authorized_handoff()` 完成授权 Pi 只读消费与全量产物 SHA-256 核验（`evidence/phase-4-pi-handoff-acceptance.json`）。
- `4.2` 已完成：完成 8/8 信封去重、过期、篡改、越界、状态失配拦截验证与缺失交接授权拦截验证，已移除第二份持久化状态文件 `return-dedup-ledger.json` 与全部 SQLite 写操作（对非预期占用队列项 fail-closed `BLOCKED_OCCUPIED_QUEUE_REFUSED_NO_DELETE`）。
- `4.3` 已完成：`openspec validate integrate-governed-cli-autoloop --strict`（`exit 0`）与 `phase4_return_probe.py --verify-only`（`exit 0`）通过；独立 Pi 审查实例 `01a1c3e6-1465-728a-99c4-a25ee74b42ee` 完成 R1（行 `28` `event_id=01717df6`）与同实例 R2 `FOCUSED_RECHECK`（行 `67` `event_id=c625c327`，单行去尾换行 SHA-256 `655d7accc0f351e3c2469f9edcab484183d7ffa999049ad90b5e2ad41b643fc6`）只读验收审查并给出 `REVIEW: PASS`（0 阻塞发现，66/66 项 Manifest 哈希零误差，审查前后工作区与 SQLite 零变化）；显式报告未启用项（AGY 自动只读入口未启用、常驻后台规则已回滚、不执行 `openspec archive` 或 Git 写操作）。勾选 `4.1`–`4.3`，阶段 0–4 全部收口完成。
