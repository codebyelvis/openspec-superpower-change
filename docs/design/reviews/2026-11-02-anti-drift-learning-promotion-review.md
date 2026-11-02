# Anti-drift learning promotion review

文档类型：项目学习晋升控制面审查
日期：2026-11-02
结论：通过
验证范围：仅评审候选卡、工程不变量新增节和指定回归；结论不扩展到归档变更、运行时同步、发布或其他未提交改动。
作者：elvis

## 身份、目的与权限

- Review purpose：判断本项项目级学习是否有正确的持久化目标、可执行回归、非敏感证据和有效晋升条件。
- Reviewer product：Codex。
- Reviewer role：control-plane。
- Capability profile：control-plane-high。
- Instance：本 Codex 会话 `01a19a29-260b-7202-a419-ca93f534a872`。
- Independence：用户明确指定执行者是另一 Grok session。本会话未编写收到的三份学习产物；独立读取文件、完整学习 diff 并重跑证据。本会话仅修正下述候选卡措辞和执行审查后的状态记录。
- Result authority：本会话只接受这一项学习晋升、记录 Review PASS 并决定候选状态。另一 Grok session 的执行产物与 grok-cc advisory 结论均为输入证据，不能替代本次控制面决定。
- 未获得 `git add`、commit、push、安装或同步授权。本次不调用外部顾问，不创建新的执行派发，不修改归档、`SKILL.md` 或 managed block。

## Gate 0 与输入

模式为 Project Learning Closeout。只涉及项目文档、既有行为回归和本次审查记录，按 Direct Change 处理，不新增或重做 OpenSpec。
保留原执行者与当前审查者的独立性；采用完整学习 diff 审查和独立负向探针。选用 `superpowers:verification-before-completion`，无需另建实现计划或新增行为 TDD。

已读取：

- `AGENTS.md`、根 `SKILL.md`。
- `references/project-learning-closeout.md`、`templates/learning-candidate-template.md`。
- `references/learning-candidate-pipeline.md`、`references/direct-change-rule.md`、`references/completion-contract.md`。
- `docs/learning-candidates/2026-11-02-anti-drift-round-budget.md`。
- `docs/engineering-invariants.md`，重点为新增节 “Approved copy boundaries and closure facts stay distinct”。
- `tests/test_workflow_rules.py` 的指定回归、导航回归与必要加载上下文。
- `openspec/changes/archive/2026-11-02-add-verify-anti-drift-round-budget/closeout.md` 和 `evidence/phase-b.md`。

只读核对确认 `HEAD`、`main`、本地 `origin/main` 引用均为 `1899b131773a0a1b16f283364a06c0464432e06f`；没有 fetch 或重新发布。
归档中的旧结论保留历史语义，本次仅对学习产物作出新判断。

## 发现与最小修改

必须修改的问题共 1 项，已关闭。

候选卡“可复用做法”原先把用户要求闭环直接连到勾选剩余任务及 `openspec archive`，容易被读成可绕过实际验收与控制面 Review。
本会话将其限定为：只办理该指令明确覆盖的记录；任务勾选和归档仍依赖实际验收、证据、控制面 Review 与仓库归档条件。
同一句还明确 Git 需要该次授权，保持 `main`、不新开分支仅是本次历史安排。
这保留原本批准边界，不修改任何工作流实现或共享治理规则。

工程不变量与测试源码无须修改，保持收到时的内容。
晋升前已确认候选卡是 `status: candidate`、`review_result: pending`；本审查结论先落盘，之后才允许记录 `promoted` 和 `pass`。

## 必要条件逐项判断

| 条件 | 独立核对与判断 |
| --- | --- |
| 两份短版保留批准边界 | 两份均无长版续句，均保留 `Stop for scope/protected-boundary changes`；SHA-256 同为 `ef3f5361425693af5e582cf9f49e5f36888971b6f3903f1a2e034ac213594529`。 |
| 长版保留既有续句 | 根 `SKILL.md` 仍含 `An already authorized same-scope correction may continue while its`；SHA-256 为 `237e17e9488b996d4f736fc907413311fabc46beab4477a629de9be9d7f1a994`。 |
| 用户标记不进入现用源文件 | 根和两份短版 `SKILL.md`、`references/shared-global-governance.md` 均无 `CODEX_ANTI_DRIFT_ROUND_BUDGET`。归档 diff 的历史标记不在禁止范围。 |
| 不变量只追加指定节 | 与 `1899b13:docs/engineering-invariants.md` 逐字节比较，原文件为当前文件完整前缀；后缀只含 1 个新增二级标题，即指定节。前面的各节未改写。 |
| 晋升身份与顺序正确 | 审查开始及结论落盘前均为 candidate/pending；只有本会话可在本结论和测试通过后更新状态。顾问结论未被冒充为控制面 PASS。 |
| 非敏感且持久 | 候选卡为摘要、路径、哈希及规则判断，无密钥、完整对话或私有 prompt；候选卡和工程不变量均不被 Git 忽略。聊天不是唯一存储。 |

## 对抗审查场景

以下逐项审阅候选卡及指定归档证据；这是对学习规则与证据表述的复核，不重新执行旧的云端会话、运行时同步或行为探针。

1. 完成项计数：`phase-b.md` 区分 started 与 completed，completed 的类型计数为 2、3、3，合计 8；`command_execution` 为 3，并解释 6 是错误相加。候选卡没有继承错误计数。未重读原始 native events，不把文档算术核对称为原始事件重数。
2. 补丁绑定：归档记载旧任务号 `END_PATCH` 导致哈希不可用且未执行 `git apply`。卡片要求当前任务号与哈希同时有效，没有用顾问正文绕过补丁门槛。
3. 脚本失败范围：卡片及归档明确 124 是脚本退出码，不证明墙钟超时。保留“失败后上报并停止”的范围，没有把该脚本退出码继续列为学习晋升阻塞。
4. Git 范围：当前 `git diff --cached --name-only` 为空；没有暂存未批准 requirement。本次仍不执行 Git 写操作。
5. 运行时防回退：卡片和不变量均要求比对目标、发布提交及当前工作区；不得以 HEAD 覆盖更新且匹配工作区的目标。本次不刷新运行时，不宣称重新验证旧同步收据。
6. 预存符号链接：卡片不建议拆除既有指令文件链接，也不把它等同 managed block 复制。只审查规则表述，不重新修改或认证本机链接状态。
7. 探针范围：没有用路由套件的 `forward: PASS` 替代五题探针。旧探针的脚本失败范围按历史记录保留，不在此重新认证原变更的业务完成。
8. 完成权限：顾问 `project_pass=false` 和 advisory 结果均不构成控制面通过。执行者未先把学习状态改为 promoted；本次通过只由本 Codex 会话作出。

无未关闭的必须修改项。动态运行时、原始日志与历史派发信封没有本轮重放；这些场景采用候选卡中明确的对抗审查，不能据此宣布运行时或归档变更重新验收通过。

## 新鲜验证

在上述候选卡措辞修正后运行用户指定命令：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_workflow_rules.WorkflowRulesTest.test_packaged_copies_keep_approved_boundaries tests.test_workflow_rules.WorkflowRulesTest.test_project_learning_guidance_is_discoverable_from_project_instructions -v
```

结果：退出码 0，2 项测试通过，0 失败、0 错误、0 跳过。
覆盖长短版差异、live marker 排除和工程学习入口可发现性；不代表全量测试或运行时验收。本轮未运行全量测试。

独立对抗探针在自动清理的临时目录中复制相关输入，调用实际回归方法，未修改仓库源文件：

- 向两份短版分别补入长版续句：2 种错误均被拒绝。
- 分别删去两份短版的 `Stop for`：2 种错误均被拒绝。
- 向根、两份短版及 managed source 分别加入用户标记：4 种错误均被拒绝。
- 从长版删除既有续句：1 种错误被拒绝。
- 正常副本与仅归档出现历史标记：2 个对照均通过。

合计 9/9 个负向变体被拒绝，2/2 个对照通过。该结果验证确定性回归的拒绝能力，不是模型行为或真实运行时同步的证明。

## 晋升决定与剩余边界

本项达到项目级学习持久化和 Review PASS 条件。依据本轮用户的明确授权，本会话在本结论写出后将候选卡更新为 `status: promoted`、`review_result: pass`、`decision_owner: codex`，并将本会话标识及此审查路径写入 `decision_provenance`。
这是一项本地学习晋升，不是 commit、push、安装或原归档变更的新完成声明。状态更新后的最终核验另记于文末。

本次收到的工程不变量与回归文件属于另一 Grok session 的既有学习改动。本会话只修正候选卡文字、记录其审查后状态，并新建本审查。
本项最终应保留的未提交文件为：

```text
 M docs/engineering-invariants.md
 M tests/test_workflow_rules.py
?? docs/learning-candidates/2026-11-02-anti-drift-round-budget.md
?? docs/design/reviews/2026-11-02-anti-drift-learning-promotion-review.md
```

保留原因：本提示未授权暂存、提交或 push。后续由用户决定是否授权发布这 4 份本地学习成果；现在无需用户操作。

## 其余既有未提交项

起始工作区共有 62 条状态记录，其中本项既有学习文件 3 条、其余既有项 59 条。
以下仅按 Git 状态登记，不据此认领内容或修改权。本会话不编辑、不暂存、不丢弃；继续保留给原任务或文件负责人处理。

```text
 M openspec/changes/add-role-first-review-routing/specs/skill-workflow-governance/spec.md
 M openspec/changes/optimize-closed-loop-runtime-routing/specs/skill-workflow-governance/spec.md
 M openspec/changes/reduce-redundant-confirmation-and-review-overhead/tasks.md
 M openspec/changes/streamline-simple-change-gates/specs/skill-workflow-governance/spec.md
 M openspec/changes/support-grok-configured-skill-discovery/specs/skill-workflow-governance/spec.md
 M openspec/specs/skill-workflow-governance/spec.md
 M references/agent-capability-routing.md
 M references/approved-implementation-workflow.md
 M references/shared-global-governance.md
 M scripts/validate_core_gates.py
 M scripts/validate_cross_cli_sync.py
 M tests/test_cross_cli_sync.py
?? docs/JEV_PHASE0_HANDOFF.md
?? docs/agent-collab/complete-native-consumer-adaptation/
?? docs/design/JEV_INTEGRATION_PLAN.md
?? docs/requirement/grok-cli-task-optimize-skill.md
?? docs/review/2026-09-04-platform-catalog-indexing-investigation.md
?? docs/review/2026-10-13-closeout-cursor-observer-source-summary.json
?? docs/review/2026-10-13-closeout-grok-native-loading-summary.json
?? docs/review/2026-10-13-closeout-grok-native-loading-v2-summary.json
?? docs/review/2026-10-13-closeout-grok-native-loading-v3-summary.json
?? docs/review/2026-10-13-closeout-sandbox-readiness-fixtures.json
?? docs/review/2026-10-13-native-consumer-closeout-current-verification.json
?? docs/review/2026-10-13-native-consumer-closeout-draft.md
?? docs/review/2026-10-13-native-consumer-closeout-preparation.json
?? docs/review/2026-10-13-native-consumer-closeout-progress.md
?? docs/review/2026-10-14-native-consumer-claudex-observation-summary.json
?? docs/review/2026-10-14-native-consumer-handoff-checkpoint.json
?? docs/review/2026-10-14-native-consumer-observer-advisory-review.md
?? docs/review/2026-10-15-native-consumer-control-plane-adjudication.json
?? docs/review/2026-10-15-native-consumer-fresh-cursor-evidence.json
?? docs/review/2026-10-16-claude-startup-adjudication.json
?? docs/review/2026-10-16-claude-startup-preflight.json
?? docs/review/2026-10-16-native-startup-grok-cc-dispatch.json
?? docs/review/2026-10-16-native-startup-mechanism-correction.json
?? docs/review/2026-10-17-claude-startup-slice-confirmation.md
?? docs/review/2026-10-17-native-consumer-approval-basis.md
?? docs/review/2026-10-17-native-consumer-schema6-cutover-inventory.json
?? docs/review/2026-10-17-row03-producer-receipt.md
?? docs/review/2026-10-18-native-consumer-temp-write-deviation.json
?? docs/review/2026-10-19-claude-startup-full-preflight.json
?? docs/review/2026-10-19-claude-startup-tty-adjudication.md
?? docs/review/2026-10-19-native-startup-preflight-submission.md
?? docs/review/cursor-stream-audit.claudex.0e821cad-e39b-48d7-b680-93c101916634.r1.review.md
?? docs/review/native-consumer-observer-closeout.claudex.0e821cad-e39b-48d7-b680-93c101916634.r1.review.md
?? docs/review/native-consumer-observer-closeout.claudex.0e821cad-e39b-48d7-b680-93c101916634.r2.review.md
?? docs/superpowers/plans/2026-10-13-complete-native-consumer-adaptation.md
?? openspec/changes/allow-task-scoped-grok-control-plane-rebind/
?? openspec/changes/archive/2026-09-28-upgrade-workflow-dependencies/
?? openspec/changes/complete-native-consumer-adaptation/
?? openspec/changes/restore-original-codex-control-plane/
?? references/jev/
?? scripts/jev_advisory_router.py
?? scripts/jev_eval.py
?? tests/fixtures/jev_routing_cases.json
?? tests/test_control_plane_return.py
?? tests/test_jev_advisory_router.py
?? tests/test_jev_eval_offline.py
?? tests/test_task_scoped_control_plane_rebind.py
```

## 晋升后最终核验

本 Codex 会话已核对最终候选卡：`status: promoted`、`review_result: pass`、`decision_owner: codex`。
`decision_provenance` 绑定本会话 `01a19a29-260b-7202-a419-ca93f534a872` 和本审查文件，且没有将顾问身份或其他会话记为控制面 PASS。

状态更新后再次完整运行上述指定命令：`Ran 2 tests in 0.007s`，`OK`，退出码 0；2 通过，0 失败、0 错误、0 跳过。
限定本项的 `git diff --check` 无输出、退出码 0；完整学习 diff 与最终候选卡已复核，无未关闭 finding，本项最终控制面结论为通过。

最终学习产物 SHA-256：

| 文件 | SHA-256 |
| --- | --- |
| `docs/learning-candidates/2026-11-02-anti-drift-round-budget.md` | `b3f3cebbebd8aeab23aa73ffd81c589a77b1322bd04c9ed827c8d8ce446f454c` |
| `docs/engineering-invariants.md` | `3c0ad2e816e401091f8d7cb3a065c09f671644266889849d81c2352f41603181` |
| `tests/test_workflow_rules.py` | `4828ad60c66e12bafe4865329254c49b9559f6d5f9c653a3946860d9f9eff440` |

最终 Git 状态共 63 条记录：本项 4 条和上列其余既有项 59 条。
Git index 清单 SHA-256 前后均为 `088ecfad8f1a275ee5c771ed7071182461b23dfbe91677643ab2c3725c6d797f`，未发生暂存。
本轮保护快照确认：归档文件和三份 `SKILL.md` 的哈希未变，managed source 哈希未变；收到的工程不变量、测试文件内容也未变。
其余 59 条既有项的状态及已记录对象的 inode、大小、mtime、mode 均未变；未编辑或暂存这些项。目录状态记录仅代表 Git 的目录聚合展示，不将其视为对子文件的内容验收。
本次没有写入任何安装运行时，也没有覆盖比发布提交更新的本地文件。未提交状态与后续责任按上文保留。

