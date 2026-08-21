# Independent Plan Preflight Review Prompt — Revision 4

你是用户新打开的独立 Codex 窗口。你的任务是只读审查
`add-role-first-review-routing` 当前实施计划与 Preflight 输入，决定原 bound
Codex control-plane 是否可以开始 source implementation。

## Reviewer Assignment Contract

- review_purpose:
  审查当前完整 implementation plan、批准的 schema-6 OpenSpec 合同、source/runtime
  preimages、backup/rollback、TDD/verification、Review gates、legacy drain、Pi isolation、
  four-target sync、Git/authority 边界，最终只决定当前 plan revision 是否可以进入
  source execution。
- reviewer_product: `codex`
- reviewer_role: `independent-reviewer`
- capability_profile: `control-plane-high`
- independence_requirement:
  - 必须是用户打开的新 Codex 窗口；
  - 不得是编写 plan/proposal 或准备 preflight evidence 的原 control-plane 实例；
  - 不得参与当前 revision 的文件修改；
  - 不得作为后续 source executor；
  - instance/thread ID 不可取得时如实记录 `unavailable`，并记录
    `user_opened_separate_window`。
- result_authority:
  - `governed Plan Preflight evidence only`；
  - 只允许 verdict `PASS` 或 `BLOCKED`；
  - `PASS` 仅表示原 bound Codex control-plane 可接受该证据并开始计划中的 source
    RED/GREEN tasks；
  - 不批准 runtime sync/apply、Pi execution、canonical transition、archive、Envelope、
    Git、publication 或 final completion。

## 严格只读边界

第一轮及整个 Review：

- 不修改、创建、删除或格式化任何文件；
- 不运行任何 Git 命令；
- 不运行任何 Pi 命令，包括 `pi --help`、`pi --version` 或 prompt；
- 不运行 runtime sync/apply/restore/rollback/cleanup；
- 不读取 Pi credentials、auth、settings、sessions、history、models、extensions、
  caches、logs 或其他 private/native state；
- 不更新 OpenSpec checkboxes、workbench canonical state 或 archive；
- 不签发 Handoff、Envelope、approval 或 completion；
- 不提取 backup archive；只允许核验其路径、mode、SHA 和 `tar -tf` 文件清单。

允许的只读命令：`wc -l`、`nl -ba`、`sed -n`、`rg`、`rg --files`、
`find`（仅当 `rg` 无法表达所需 inventory）、`stat`、`readlink`、
`shasum -a 256`、`tar -tf`、`openspec list`、`openspec list --specs`、
OpenSpec strict validation，以及带 `PYTHONDONTWRITEBYTECODE=1` 的当前 Router/Companion
validator。不要运行 implementation tests 或 forward probes 来冒充未实施 GREEN。

## Repository roots

- Router:
  `/Users/elvis/file/develop/opensource/openspec-superpower-change`
- Companion:
  `/Users/elvis/file/develop/opensource/codex-brief-antigravity-review`

## 必须完整读取的输入

Router：

1. `AGENTS.md`
2. `SKILL.md`
3. `CONTEXT.md`
4. `openspec/project.md`
5. `openspec/changes/add-role-first-review-routing/proposal.md`
6. `openspec/changes/add-role-first-review-routing/design.md`
7. `openspec/changes/add-role-first-review-routing/tasks.md`
8. `openspec/changes/add-role-first-review-routing/specs/skill-workflow-governance/spec.md`
9. `openspec/specs/skill-workflow-governance/spec.md`
10. `docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md`
11. `docs/design/evidence/add-role-first-review-routing/2026-08-10-plan-preflight-inputs.md`
12. `references/local-instruction-checkpoint.md`
13. `references/request-modes.md`
14. `references/approved-implementation-workflow.md`
15. `references/step-evidence-gate.md`
16. `references/superpowers-adapter.md`
17. `references/self-evolution-rule.md`
18. `references/handoff-contract.md`
19. `references/agent-capability-routing.md`
20. `references/cross-cli-sync.md`
21. `references/sync-checklist.md`
22. `references/completion-contract.md`
23. `references/shared-global-governance.md`
24. `references/cross-cli-portable-manifest.json`
25. `scripts/validate_core_gates.py`
26. `scripts/validate_cross_cli_sync.py`
27. `tests/test_workflow_rules.py`
28. `tests/test_cross_cli_sync.py`

Companion：

1. `AGENTS.md`
2. `SKILL.md`
3. `agents/openai.yaml`
4. `references/handed-off-external-execution.md`
5. `references/handoff-contract.md`
6. `references/agy-dispatch-template.md`
7. `references/brief-template.md`
8. `references/report-template.md`
9. `references/review-template.md`
10. `references/timeout-audit-template.md`
11. `scripts/validate_templates.py`
12. `tests/test_workflow_rules.py`

Preflight temporary bindings（同样必须完整读取，但不得修改或提取 backup）：

1. `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/preflight-source-bindings-r4.json`
2. `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/source-delta-allowlist-r4.txt`
3. `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/router-tree-preflight-r4.json`
4. `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/companion-tree-preflight-r4.json`

## Immutable input bindings

开始 Review 与输出 verdict 前各复算一次：

| 输入 | SHA-256 |
|---|---|
| Plan | `d621b09ad030dfdfd02ad45478ad7156486fc63c392ef0816cb99bc252af6a23` |
| Preflight input record | `13a2e1a5e1f11517c39bb9fe00e140c6e61884dedc4bf21f1ede6c3cea048f75` |
| Proposal | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| Design | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| Tasks | `764a5401f7f5ec86348f3bfcabb854b196b26793b1b842b236f3731eafa7ffea` |
| Spec delta | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| Router source backup revision 4 | `a0b7a36e0964fe8e6b93bbcb24a2454bab1c3376159f7cd55f710054d464c491` |
| Companion source backup | `3deab7e813efca3de22ff7d583a5ae089eec079c63842239d9adb85191fb4acc` |
| Router no-Git tree baseline revision 4 | `f5506db159dd77fe5b9401a20a77d9796183f5515c0e20abb466147f8dc3f859` |
| Companion no-Git tree baseline revision 4 | `cf4924df7707cf665d41de48300eb59ce8097f0ee0dd298fd7039e5db625b064` |
| Exact source-delta allowlist | `ad6531d92126e6c5e07c2251bff1e535b9f308f382f64541dff2b3e8ebaab3d6` |
| Machine preflight source bindings | `4fde9680e9d43f8268ef66ea9c31c10f3b92899d6930d5f6bb5d371ccad0c2fe` |

Backup paths：

- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/router-source-preflight-r4.tar`
- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/companion-source-preflight.tar`
- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/router-tree-preflight-r4.json`
- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/companion-tree-preflight-r4.json`
- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/source-delta-allowlist-r4.txt`
- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/preflight-source-bindings-r4.json`

若任一绑定漂移，verdict 必须为 `BLOCKED`，不得改文件或尝试修复。

## Review questions

逐项回答并引用 `path:line`：

1. Plan 是否完整覆盖 2 个 ADDED、4 个 MODIFIED requirements 和 39 个 scenarios？
2. Plan 是否是可执行实现计划而非第二份设计合同？是否存在占位符、模糊步骤、未定义
   函数/字段、前后不一致名称或缺少 expected result 的命令？
3. Exact file map 是否覆盖所需 Router/Companion/public/test/template/validator surfaces，
   又没有吸收 `add-codex-skill-update`、旧 archive、workbench 或其他文件？
4. schema-6 current-only API 与 schema-4/schema-5 read-only legacy audit 是否机械隔离？
   expanded Pi enum 是否可能泄漏到旧 parent/evidence branch？
5. Exact `reviewer_assignment` 是否覆盖 structured purpose、product、instance、role、
   profile、structured independence、evidence-only authority、readonly transition 和
   canonical-SHA binding？standard/strict/compact 是否都可实现且 fail-closed？
6. RED/GREEN/TDD、source verification、natural forward-test 和 High Review 是否有明确
   文件、代码接口、命令、预期结果及重新 Review loop？是否存在 test-only fake contract？
7. Pi integration 是否覆盖 manifest、target arguments、root containment、sensitive
   exclusion、deterministic discovery、optional process isolation、native-root denial、
   target-local restore 和 verify-all？Actual native validation 是否保证不调用 Pi？
8. 当前环境中 `CODEX_HOME=/Users/elvis/.codex-account-a` 与实际 discovered
   `/Users/elvis/.codex/skills` 的差异是否被安全消歧？`.agents/skills` symlink 是否明确
   保持不变？后续 Sync-plan Review 是否仍需绑定 exact target？
9. Preflight source hashes、absent creation paths、source backup archives、runtime observed
   preimages 和 zero-known-Handoff 结果是否足以开始 source work？哪些证据必须在
   source Review 后/first apply 前刷新？
10. Backup/rollback/stop conditions 是否禁止盲目 restore、跨 target rollback、native
    state copy、preimage drift、active old schema、scope expansion 和 unsafe cleanup？
11. Review assignments 是否对 Proposal、Plan、candidate source、sync plan、Pi adversarial、
    Learning、Final gate 都明确 purpose/product/role/profile/independence/authority？
12. Plan 是否错误授权 Git、Pi、runtime、canonical state、archive、Envelope、publication
    或 completion？
13. 保持 OpenSpec `tasks.md` 在 approved hash、不立即勾选 1.4/1.5，是否被 Preflight
    record 如实解释且不会让实施者误判授权？后续是否只允许 evidence-backed progress？
14. Public docs、shared Handoff bytes、shared validator core、sensitive scan、legacy drain、
    four-target verification 和 post-archive validation 是否都在正确时序？
15. `PF-001` 是否已真正关闭：compact helper 是否写入批准合同的 exact top-level
    `independent_review_not_applicable_reason`、断言 nonblank、拒绝未定义的
    `independence_na_reason`，且 Pi CLI 段不再含错位 schema fixture prose？valid fixture
    是否进入 production current-validator RED，而非 malformed/setup failure？
16. `PF-002A` 是否已真正关闭：每个 target 是否通过 mode-0600 receipt 将 apply、verify、
    discovery、commit 置于一个可恢复的未提交窗口？所有 post-apply failure 是否调用 exact
    `restore-target`，校验 plan/backup/preimage，停止 later targets；restore failure 是否
    fail-closed/manual disposition；verify-all 是否只接受四个同 plan 的 verified receipts？
17. `PF-002B` 是否已真正关闭：Preflight baseline 是否包含 hidden `.gitignore` 与全部 17
    个既有 Review，只精确排除两个后续自变的 planning artifacts；source-start inventory
    是否在 accepted Review 后、首个 source edit 前覆盖除 root `.git` 外完整树；45-entry
    allowlist 是否无 wildcard/duplicate；`source-delta` 是否给出 exact command、完整树差异、
    safe no-follow archive extraction、unexpected-path failure 与 expected JSON/mode？
18. `PF3-001` 是否已真正关闭：每个 target 是否在任何 destination mutation 前先完成并
    fsync closed backup，再 durable install mode-`0600` `prepared` receipt，并在首个写入前
    durable transition 到 `mutation-intent`？receipt create/update 是否使用 exclusive/no-follow、
    atomic install/swap、file+directory fsync 和 current-SHA guard？`prepared`、首写后的 partial
    mutation、末写后但 `applied-uncommitted` 前，以及 orphaned pre-receipt material 是否都有
    exact restart/restore/manual-disposition 规则与真实 production-path interruption tests？任一
    `recovery-blocked` 是否禁止 later target 和 `verify-all`？

## Required validation

在 Router root 执行：

```bash
openspec validate add-role-first-review-routing --strict
openspec validate --all --strict --no-interactive
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .
```

在 Companion root 执行：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_templates.py .
```

这些 PASS 只能证明当前 pre-implementation baseline/Proposal/Plan 格式一致，不能宣称
schema-6 implementation、Pi parity、runtime sync 或 completion 已通过。

## Verdict rule

- 只有无 actionable P0/P1/P2 finding，所有绑定未漂移，Plan 无 placeholder/fake
  contract/authority leak，且 rollback/stop/verification/Review chain 完整时，返回 `PASS`。
- 任一 actionable finding、输入漂移、缺失证据、权限冲突或无法安全判断时，返回
  `BLOCKED`。
- Observation 必须明确说明为何不阻塞、owner 和后续 release condition；不能把未关闭
  finding 改名为 Observation 后返回 PASS。

## Required output

完整返回以下结构，不要只给一句 verdict：

1. Reviewer identity
2. Reviewer Assignment Contract
3. Scope、完整读取清单、开始/结束 SHA、实际只读命令、未取得证据
4. Plan/architecture summary
5. Findings：P0 / P1 / P2 / Observation
   - 每项包含 `finding_id`、severity、exact `path:line`、observed fact、violated
     contract、impact、required correction、whether re-review is required
6. Prior-finding closure matrix：`PF-001`、`PF-002A`、`PF-002B`、`PF3-001` 逐项只能为 `CLOSED` 或 `OPEN`
7. OpenSpec requirement/scenario traceability matrix
8. Schema-6/current-vs-legacy/evidence-binding matrix
9. Exact-command matrix：source-start、Task 6、8、9、10 的 command/arguments/expected/stop-or-restore，且 Task 9 单列 pre-mutation receipt 与 `recover-pending`
10. Pi integration/safety/four-target matrix
11. File allowlist、preimage、backup、rollback、dirty/no-Git matrix
12. Reviewer-assignment gate matrix
13. Validation commands/results
14. Verdict：仅 `PASS` 或 `BLOCKED`
15. Exact next action

若 `PASS`，Exact next action 必须说明：把完整 Review 原文返回原 bound Codex
control-plane；不得自行实施。原 control-plane 复核并接受证据、持久化 Review，并按
Plan 的 exact command 捕获完整 source-start inventories 后，才可开始 Plan Task 1
source RED tests；runtime/Pi/Git/canonical/archive/completion 仍未授权。

若 `BLOCKED`，Exact next action 必须列出要返回原 control-plane 修订的最小 finding
集合；不得修文件。
