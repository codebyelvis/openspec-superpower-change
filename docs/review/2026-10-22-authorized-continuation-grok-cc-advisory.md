# grok-cc 顾问审查：reduce-redundant-confirmation-and-review-overhead draft-v2

- task_id: a80661a5-eddc-4a84-b771-6149c734c1c4
- 日期：2026-10-22
- 审查者产品：Claude Code（advisory reviewer，非 schema-6 产品）
- 性质：advisory-input。不是 OpenSpec 批准，不是正式 Preflight/Implementation/Final Review PASS，不构成 Major 批准记录。
- 结果：findings（P1 ×2，P2 ×5，P3 ×4）

## 审查范围

直接审读（主控提供的快照）：proposal.md、design.md、tasks.md、specs/skill-workflow-governance/spec.md、SKILL.md、references/confirmation-lease.md、references/direct-change-rule.md、references/step-evidence-gate.md、references/local-instruction-checkpoint.md。

未审读（只出现在 design 的主控证据摘要中，本报告不声称直接审读）：references/approved-implementation-workflow.md、references/completion-contract.md、scripts/validate_core_gates.py 及 validate_confirmation_lease、tests/test_workflow_rules.py、现行 skill-workflow-governance 基线 spec、grok-cc task_packet.py、完整 implementation reference、历史 dispatch JSON。

未运行任何测试，未读取或修改云端项目。未收到既有日志，因此没有通过/失败计数，本报告也不构成 Mac 验收。

## 发现

### P1-1 SKILL.md 中按类别无条件停止的 Git/外部动作条款未列入修正范围；本轮发布还依赖一条尚未生效的新规则

位置：SKILL.md §Implementation And Closure 第 4 段（"Git writes, production, publication, external writes, and destructive actions still stop at existing boundaries"）、第 5 段（"Stop for ... separately authorized external actions, Git writes ..."）；§Non-Negotiables 最后两条；design.md §Evidence And Failure Mechanisms 第 1 项；proposal.md §Approval And Publication 第 2 段。

失败场景：design 第 1 项只把 approved-implementation-workflow.md 的停止列表认定为根因。如果实施只改该文件和 confirmation-lease.md，SKILL.md 仍会按类别无条件停在 "Git writes"。在验收 2 的前向探测里，代理会读到 Router 入口的无条件条款与 reference 的复用条款互相冲突，再按同一段的 "conflicting contracts" 停下来，重新请求推送确认，这正是用户的痛点。另外，proposal 声称本轮 push "no repeated Git approval is requested"，但执行 3.5 的会话在同步前仍受现行规则约束。现行规则 "Never run git add/commit ... unless the user explicitly commands it" 要求用户显式下达 add/commit 命令，而 "push this update" 是否覆盖 commit 并没有记录。

最小修正：
(a) 在 design 证据第 1 项和 Source File Boundaries 中明确列出上述 SKILL.md 两段，并给出限定措辞，例如 "... stop unless the exact action, target and scope are already explicitly authorized"。在验收 2 的前向探测中断言入口条款与 reference 不冲突。Non-Negotiables 中 add/commit/push 两条保持不变，只说明既有的显式指令已满足要求。
(b) 在 proposal §Approval And Publication 中逐字引用用户的原始推送指令，或按路径/时间指向它，并说明它按现行规则同时满足 commit 和 push 的显式要求。如果它不覆盖 commit，就把 commit 列为发布前唯一需要询问的增量。

### P1-2 授权哈希的对象不明确：现行文本把 Plan/Brief 修订列为授权层，与验收 5 冲突

位置：references/confirmation-lease.md §Authorization layers 第 2 项（"Scope/workflow authorization: approved OpenSpec, current Plan/Brief, allowlist, artifact revision"）及 §Confirmation Lease 字段表；design.md §Authorization binding and evidence freshness；Acceptance 3、5；spec ADDED "Authorization binding is separate from evidence freshness"。

失败场景：standard/strict 外部任务的租约 `artifact_sha256` 绑定了 Plan 或 Brief 的修订，现行第 2 层允许这样做。Preflight 返回 BLOCKED 后，主控修正 Plan 中的测试命令（验收 5），Plan 的哈希随之变化。validate_confirmation_lease 精确比较失败，按 design 的 "follow its existing contract amendment path" 回到用户确认，验收 5 就无法成立。反过来，如果实施者把 Plan 当作"证据"而放宽比较，又违反了"保留精确比较"。此外，现有字段（decision_id、artifact_revision、artifact_sha256、decision_source）都没有标明哈希对应哪个文件，而 design 又要求 "using existing fields"，所以新租约仍可能绑定可变产物。

最小修正：在 design 中规定由某个现有字段（例如 `decision_source` 或 `approved_scope`）写明被哈希授权产物的路径或标识，并规定新租约的授权产物是获批的 OpenSpec change 或用户决定记录，而不是 Plan、Brief 或 status。同时把 confirmation-lease.md 第 2 层中 Plan/Brief 的角色改写为"在获批范围内、由 Preflight 验证的执行产物"。再增加一组 RED/GREEN：获批的 OpenSpec 不变而 Plan 哈希变化时，不重新询问用户，但必须经 Preflight 复核；获批 change 的字节变化时，租约失效。如果现行 validate_confirmation_lease 或既有任务确实绑定了 Plan，旧语义保持不变，新规则只对新租约生效。design 已声明不回溯，这里只需补充识别规则。

### P2-1 租约失效条件中的 "evidence assumptions" 会抵消证据新鲜度与授权的分离

位置：references/confirmation-lease.md §Reuse matrix 末段（"The lease expires when ... evidence assumptions ... changes"）；design.md §Authorization binding and evidence freshness 没有处理该词。

失败场景：同范围修复改动了代码，某个测试结果需要重跑。代理把"证据已失效"解释为 "evidence assumptions changed"，判定租约过期，重新请求范围确认，与 spec "Same-scope fix changes code" 相悖。

最小修正：在 design 中写出该条款的目标措辞。例如：只有获批合同中记录的证据前提发生变化（如要求真实环境、真实端点或某个验收层）才使租约失效；刷新后的测试结果、Report 和进度不属于此类。再加一个与验收 3 同组的负向用例。

### P2-2 direct-change-rule.md 中按类别停止的条款不在编辑候选内

位置：references/direct-change-rule.md §Compact local work 末段（"Stop if scope expands, a protected boundary is touched, an existing approval gate applies ..."）；design.md §Source File Boundaries 没有列出该文件，但它在本次 allowlist 中。

失败场景：在用户已显式授权推送的 Direct Change 路径中，"a protected boundary is touched" 会按类别触发停止，绕过新的授权覆盖检查，又产生一次推送确认。

最小修正：二选一。把该文件加入候选，采用与 SKILL.md 相同的限定措辞（"... touched without applicable explicit authorization"）；或者在 design 中说明 Direct Change 路径为何不受影响，并在前向场景中覆盖一次。

### P2-3 发布前验证的是脏工作树，而不是实际暂存/提交的树

位置：design.md §Review, Synchronization And Publication 第 3 段及 §Rollback；proposal.md §Scope（"Existing dirty changes ... are pre-existing user work"）。

失败场景：SKILL.md 或 tests 中已有用户未提交的改动。quick/core/unittest 在包含这些改动的工作树上通过，随后只暂存本轮 owned delta 并推送，结果推送的树从未被验证。如果用户的改动恰好使某个断言通过，origin/main 实际可能处于失败状态。另外，当同一文件中 owned hunk 与用户 hunk 相邻或重叠时，"stage only reviewed owned deltas" 没有可执行的机制，可能误提交用户的改动。

最小修正：
(a) 编辑前记录每个候选文件的 dirty 状态。如果 owned 改动与用户既有 hunk 重叠，就暂停，只针对该文件请求决定。
(b) 用非交互方式暂存，例如"owned diff 相对 preimage 生成补丁，再 `git apply --cached`"，并核对 `git diff --cached` 与审过的 owned diff 逐字节一致。
(c) 推送前，在由暂存树导出的临时目录或临时 worktree 中重跑必需的 Router 检查。回滚同样只反向应用 owned diff。

### P2-4 MODIFIED 需求可能静默删除既有场景

位置：spec.md §MODIFIED Requirements "Authorized execution continuity"。

失败场景：OpenSpec 的 MODIFIED 块会整体替换原需求。如果基线 spec 中该需求包含本快照里没有的场景（基线未提供，无法核对），strict validate 依然会通过，但这些场景会在归档时被删除，形成未经审查的行为回归。

最小修正：主控在实施前逐条对比基线需求与 MODIFIED 块，列出所有被删除或改写的场景，并在 design 中逐一说明这些删改是有意的。

### P2-5 顾问报告的唯一输出路径缺少负向验收

位置：design.md §Project-side grok-cc Advisory Routing 第 3 段、§Review, Synchronization And Publication 第 1 段；Acceptance 8。

失败场景：现行传输的 allowlist 既是上下文范围，也是可写范围（本次 allowlist 就包含 SKILL.md、proposal.md 等）。如果返回的补丁除了报告文件还修改了 SKILL.md，而主控只检查"报告路径存在"，或者整体执行 `git apply` 把多余的 hunk 一并应用，顾问输出就变成了未经审查的规则修改。design 对此只有一句 "manually enforce"，没有可验证的判据。

最小修正：在 Acceptance 8 或前向探测中加入判据：补丁唯一允许的目标是从 `--- /dev/null` 新建指定的报告路径；只要出现其他路径、对已存在文件的修改或额外 hunk，就整体拒收，不做部分应用。零发现报告同样适用。

### P3-1 "compact signoff" 混用了 compact 证据档位与 compact 模板两种含义

位置：step-evidence-gate.md §Compact Gate Templates 与 §Signoff Conditions；design.md §Compact signoff presentation；spec ADDED "Compact signoff permits inline factual evidence"。

失败场景："compact" 既指 `compact` 证据档位，也指 standard 同样使用的 compact 模板。实施者可能只对 `compact` 档位放宽，standard 仍被要求出事实表，痛点依旧；也可能把放宽扩展到高风险或改变合同的步骤，造成越界。另外，"diff references" 如果没有锚定到 path:line，就不满足现行 "Every fact has `path:line` evidence"。

最小修正：把适用范围限定为"step-evidence-gate 已允许精简报告的情形（非 high-risk、非 contract-changing、未要求完整输出），与档位无关"。把 Signoff Conditions 第 1–2 条改写为"代码事实已记录（表格或行内），每条带 path:line，或带锚定到 path 的 hunk"，而不是删除这两条。

### P3-2 阻塞修复的"同范围"判定缺少独立复核

位置：design.md §Owner-aware blocker remediation；spec "Repairable Preflight defect"。

失败场景：主控自行认定某项修正属于"同范围"，没有询问用户就扩大了 Plan，而复核只检查原发现是否已修复。

最小修正：在该场景的 THEN 中加一句：复核（Preflight recheck）必须明确确认修正没有超出获批范围和风险档位；否则按 "Blocker requires new authority" 处理。

### P3-3 顾问派发授权按"次数"计还是按"payload 修订"计，没有说明

位置：design.md §Project-side grok-cc Advisory Routing 第 2 段（"same task, bound target and reviewed payload"）；proposal §Approval And Publication（"one grok-cc advisory Review"）。

失败场景：处理本报告的发现后 payload 发生变化。主控可能误以为同一授权覆盖第二次派发；也可能对一次本应被覆盖的同 payload 重试再次询问。

最小修正：说明本轮授权的范围是"一次派发，加上对这次结果的收集，以及同一 dispatch 的恢复"。修订后如需复审，作为新增量向用户询问，或明确写明不计划复审。

### P3-4 未来原生协议章节放在本轮 change 中，归档时可能被当作已接受的设计

位置：design.md §Separate Future Design: Native Advisory Result Protocol。

失败场景：归档或 distill 时，该章节被当作已批准的设计提升为 project learning，后续 grok-cc 变更被误认为"已有获批方案"。

最小修正：在本 change 中只保留一句指向未来独立 change 的说明，把细节移到不随本 change 归档的 docs/design 草案；或者在章节首行标注"不随本 change 归档或提升"。另外，在验证计划中注明 Router 同步目标 "Grok CLI" 不等于安装 grok-cc，避免与非目标混淆。

## 无发现的检查项

- 范围与非目标：Router-only 实施和发布、不改 grok-cc 源码和安装、不自动转移归属、不新增 schema 或注册表，各处表述一致，未发现越界。
- Major 批准：proposal 与 spec "A new Major contract is not approved" 都正确保持了实施待批状态；未发现本报告或用户的泛化请求被当作批准。
- 独立性：proposal §Validation 保留了独立的 Preflight/Implementation/Final Review，Claude Code 意见只作为附加 advisory，与 local-instruction-checkpoint.md 一致。
- 身份：Claude Code 未被升格为 schema-6 产品；"Grok Bot 不将其改称 Grok CLI"的表述前后一致。
- 过度设计：除 P3-4 外，未发现新增状态机、runner 或注册表。

## 未验证项

- approved-implementation-workflow.md 停止列表的实际措辞、validate_confirmation_lease 实际比较的字段、基线 spec 的原需求文本、tests/test_workflow_rules.py 的现有覆盖：均未提供，相关结论有待主控核实。
- tasks 1.4 所称 strict validate 通过，以及 design 第 6 项 no-write 探测的结果：未复现。
- 用户原始授权指令的原文与范围：未提供，P1-1(b) 需要主控核对。
- 既有日志：未提供，没有计数；本报告不构成 Mac 验收。
