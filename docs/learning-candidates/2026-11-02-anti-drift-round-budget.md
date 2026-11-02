# Learning Candidate Card: Approved copy boundaries and closure facts

Change: `add-verify-anti-drift-round-budget`, archived as
`openspec/changes/archive/2026-11-02-add-verify-anti-drift-round-budget`.
Published commit `1899b131773a0a1b16f283364a06c0464432e06f` on `main`.

This card is the session distillation the user requested on 2026-11-02.
The archived closeout said the learning audit found no new project promotion.
That sentence is superseded by this explicit archive-and-distill request.
The archive file was not rewritten.

```yaml
status: promoted
event_kind: correction
severity: medium
scope: project-local
promotion_trigger: explicit-archive-distill
symptom: "Short copies gained a long-file-only sentence, evidence counts and patch bindings were misread, and an ordered close was reported again as an open risk."
prior_assumption: "The canonical long file, a summed event total, an advisor envelope, and an executor-held archive step could stand in for the approved copy, the completed record, the current task, and the user's close order."
correction_or_evidence:
  - "Archive evidence/phase-b.md records the short-copy revert and the completed command_execution count of 3."
  - "Archive closeout.md records the user-ordered close, the rejected previous-task patch, and that advisory review is not control-plane PASS."
  - "Commit 1899b131773a0a1b16f283364a06c0464432e06f contains the long and short skill copies and the three governance requirements only."
generalized_invariant: "Keep each approved copy, completed evidence record, current patch binding, and user-ordered close distinct. Advisory review and a newer local destination do not move those boundaries."
independent_reproductions: "User close-order correction; distinct advisory review of the short sentence, the doubled event count, the scripted exit, and the instruction-file symlink."
independence_rationale: "The user correction and the advisory review are different sources. Repeated paraphrases of either source are not a third reproduction."
duplicate_or_conflict_result: "Extends docs/engineering-invariants.md with one new section. It does not restate user-owned round-budget text, does not edit the managed governance block, and does not weaken Review PASS, promotion, or Git gates."
target_artifacts:
  - docs/engineering-invariants.md
  - tests/test_workflow_rules.py
mechanical_enforcement: required
mechanical_enforcement_reason: "The short-copy sentence and the live-file marker have a deterministic negative check. Runtime trees, native event logs, advisor envelopes, and the Git index have no in-repo fixture, so those items use the adversarial scenarios below."
verification:
  - "tests/test_workflow_rules.py rejects the long-file-only continuation in both packaged short copies."
  - "The same test rejects the user-owned round-budget marker in live skill copies and references/shared-global-governance.md."
review_result: pass
decision_owner: codex
decision_provenance: "2026-11-02: 本 Codex 会话 01a19a29-260b-7202-a419-ca93f534a872（product: Codex; role: control-plane; profile: control-plane-high）独立复核另一 Grok session 编写的学习产物，修正闭环措辞并重跑指定 2 项测试，通过后先写出 docs/design/reviews/2026-11-02-anti-drift-learning-promotion-review.md 的通过结论，再接受本项学习晋升。仅此审查是本次控制面 Review PASS；顾问或其他会话不代行该决定。Git 暂存、提交和 push 未获授权。"
```

Durable rule: [Approved copy boundaries and closure facts stay distinct](../engineering-invariants.md#approved-copy-boundaries-and-closure-facts-stay-distinct).

## 内容锚点

- 长版 `SKILL.md` SHA-256 `237e17e9488b996d4f736fc907413311fabc46beab4477a629de9be9d7f1a994`。批准的换行在 `required evidence.` 之后。
- 两份短版 SHA-256 `ef3f5361425693af5e582cf9f49e5f36888971b6f3903f1a2e034ac213594529`，保留 `Stop for`。误加续句时的中间哈希是 `2d5ac937ce0b4f015a945c5fd2006d5907fea04ecd3ce0ac8b58ccd19cbe80b8`，已退回。
- 官方同步计划 SHA-256 `fc761e5a2f579e83cb7f699eb915c77747ea17a2691c70ccdd28b64e50509e4b`。选择只有 `openspec-superpower-change:SKILL.md`，没有选择 managed rule。四个目标的 receipt 都是 `state=verified`。
- 用户所有的追加文本不在本仓库。归档 diff 只作历史记录，不把它抄进 skill 或 managed block。

## 踩坑

- 用户已经要求结束「有风险」循环时，不要因为执行者自己还没勾选剩余任务、还没归档，就再回一次有风险。该做的记录要做掉。这不把顾问审查写成控制面 PASS，也不自动授权 Git。
- `item.started` 和 completed 不要相加。这次 completed `command_execution` 是 3。写成 6 是重复计数。
- 短版不要带上长版才有的续句 `An already authorized same-scope correction may continue while its`。那句只属于已批准的长版上下文。
- 场景脚本自己打印失败并退出 124，只能证明「失败后上报并停止」。它不是墙钟超时，用户接受上报后也不再当作永久阻塞。
- 顾问补丁的 `END_PATCH` 必须是当前任务号。写成上一轮任务号时哈希失败。不要用 `--allow-unhashed` 救这个补丁；核对原文后手工改确认过的句子。
- `recover-final-reply` 在缺少 `end_turn` 时最多等 30 秒。模型还没写完就回收，会把这 30 秒耗尽，之后不能再开一轮 SSH。先等模型，再回收一次。
- 同步计划的私有目录父级必须是真实目录。macOS 上 `/tmp` 是指向 `/private/tmp` 的符号链接，计划会拒绝。用 `/private/tmp/<name>`，模式 `0700`。本机拒绝 `rm -rf` 时新建目录，不删除旧目录。
- 同一 spec 文件里还有未批准的 requirement 时，只暂存本次三条要求。暂存后把未批准的 hunk 恢复到工作区。这次留下的是 `Compatibility-preserving pinned dependency upgrade`。
- 发布后的本地更新只对齐已经相同的 `SKILL.md`。工作区比 `1899b13` 新、且运行时已经等于工作区的文件不要用 HEAD 覆盖。蒸馏时这五份就是这样：`references/agent-capability-routing.md`、`references/approved-implementation-workflow.md`、`references/shared-global-governance.md`、`scripts/validate_core_gates.py`、`scripts/validate_cross_cli_sync.py`。
- 不要把用户所有的 G1–G4 抄进 managed block。`~/.pi/agent/AGENTS.md` 本来就链接到 Codex 的 `AGENTS.md`，这不是违规，不要拆链接。
- 路由套件的 `{"forward": "PASS"}` 不是五题验证场景。那个 runner 会 `--ignore-rules`，并且禁止工具事件。
- `input_accepted`、屏幕文本、`finish` 的 `project_pass=false` 都不是完成。权威正文是带 `end_turn` 的 `recover-final-reply`。
- `openspec validate --all --strict` 里 `add-project-document-ownership` 没有 delta，是另一项既有失败。不要顺手改它。

## 可复用做法

- 一轮只做 VERIFY、DIAGNOSE、FIX、REVIEW 之一。VERIFY 失败就是上报，不带修复权。只有用户能改这一轮的类型。
- 同步用 schema v2，`--select-file openspec-superpower-change:SKILL.md`，不要加 `--select-managed-rule`。每个目标按 apply、verify、verify-discovery、commit-target 做完，再 `verify-all`。apply 前核对哈希。Grok discovery 用模式 `0600` 的 `grok inspect --json`，验完再 `--consume`。
- 两份 self-evolution backup 都留着。短版从 `*.before-evidence-sentence` 恢复，不整文件覆盖成长版。
- 用户明确要求闭环时，只办理该指令明确覆盖的剩余记录。勾选任务和 `openspec archive` 仍须满足实际验收、证据、控制面 Review 和仓库归档条件；不能用闭环指令代替这些门槛。顾问结论保持 advisory。Git 另等该次提交和 push 的明确授权；授权后只提交对应范围。保持 `main`、不新开分支是本次历史安排，不作为其他任务的通用规则。
- 本地 skill 已与发布提交的 `SKILL.md` 一致时，更新结束。不把运行时较新的未提交文件退回 HEAD。
- 学习蒸馏写到 `docs/learning-candidates/` 和根上的 `docs/engineering-invariants.md`。聊天摘要只指向这些文件。`status` 保持 `candidate`，`review_result` 保持 `pending`，直到 Codex 控制面记录 `promoted` 和 Review PASS。

## 对抗审查场景

机械测试覆盖不了的判断，审查时按这些场景否决：

- 证据写「command_execution 共 N」时，重数 completed 记录。N 等于 started 加 completed 就否决。
- 补丁 `patch_sha_ok` 不是 true，或 `END_PATCH` 不是当前任务号，就不得 `git apply`。
- 脚本退出码被写成墙钟超时，或用户已接受「上报并停止」后仍把它列成未关闭阻塞，就否决。
- `git diff --cached` 含有本次未批准的 requirement 标题，就不得提交。
- 刷新运行时前先比哈希。目标比发布提交新，且与当前工作区一致，就不得用 HEAD 覆盖。
- 预存的指令文件符号链接被当成 managed block 违规，并建议拆链接或把块抄到其他 CLI，就否决。
- 用路由套件的 `forward: PASS` 代替另一次行为探针，就否决。
- 顾问 `project_pass=false` 被写成控制面通过，或学习卡在没有 Codex Review PASS 时写成 `promoted`，就否决。

## 验证与未完成

- 聚焦回归是 `WorkflowRulesTest.test_packaged_copies_keep_approved_boundaries`。
- 本卡和 invariant 的 Git 提交、push 未获授权。
- 本 Codex 会话已先在 [控制面审查](../design/reviews/2026-11-02-anti-drift-learning-promotion-review.md) 记录通过结论，再将本卡更新为 `status: promoted`、`review_result: pass`。指定 2 项测试通过（0 失败、0 错误、0 跳过），本结论仅覆盖本项学习产物。
