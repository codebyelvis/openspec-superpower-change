# Independent Conda Plan Amendment Preflight Review Prompt — Revision 5

你是用户新打开的独立 Codex 窗口。请对
`add-role-first-review-routing` 的 Task 6 Conda Plan amendment 执行完整、只读、
fail-closed 的 Plan Preflight Review。

本次 Review 只决定：原 bound Codex control-plane 是否可以按修订 Plan 创建一个
隔离 Conda 环境，并从 Task 6 的第一条 `quick_validate` 命令重新开始 source
verification。它不重新授权 Tasks 1–5，也不决定 candidate source 是否 PASS。

## Reviewer Assignment Contract

- review_purpose.object:
  - 修订后的完整 implementation Plan；
  - 用户选择 Conda 后的解释器、依赖、channel、路径与写入边界；
  - PEP 668 blocker history；
  - 原 revision-4 Preflight/source-start/recovery 连续性；
  - 当前 partial-source snapshot；
  - R5 source-delta allowlist/bindings；
  - Task 6 exact commands、expected results、stop/cleanup boundary；
  - Git、Pi、runtime、canonical、archive、publication、completion authority。
- review_purpose.decision:
  仅决定是否允许原 bound Codex control-plane 创建 Plan 指定的隔离 Conda
  verification environment，并恢复 Task 6 source verification。
- reviewer_product: `codex`
- reviewer_role: `independent-reviewer`
- capability_profile: `control-plane-high`
- independence_requirement:
  - 必须是用户打开的新 Codex 窗口；
  - 不得是 Plan amendment 作者、Preflight evidence 准备者或 source executor；
  - 不得修改当前 revision；
  - 不得担任本 amendment 的 Conda/environment executor；
  - instance/thread ID 不可取得时如实记录 `unavailable`，并记录
    `user_opened_separate_window`。
- result_authority:
  - `governed Conda Plan amendment Preflight evidence only`；
  - verdict 只允许 `PASS` 或 `BLOCKED`；
  - `PASS` 只允许原 bound Codex control-plane 执行 Plan Task 6 Step 2，并从
    Step 3 的第一条命令恢复验证；
  - 不批准 source correctness/source High Review、runtime sync/apply/restore、真实
    Pi、Git、canonical transition、archive、Envelope、publication 或 completion。

## 严格只读边界

整个 Review：

- 不修改、创建、删除、格式化或 chmod 任何文件；
- 不创建/删除/更新/激活任何 Conda environment；
- 不运行 `conda create/install/update/remove/init/config` 或 pip；
- 不运行任何 Git 命令；
- 不运行任何 Pi 命令；
- 不运行 runtime sync/apply/restore/rollback/cleanup；
- 不提取 backup archive，只允许 `tar -tf`；
- 不更新 OpenSpec tasks、canonical workbench、archive 或任何完成状态；
- 不运行 `quick_validate`、implementation unit suites、forward probes 或
  source-delta 来冒充尚未恢复的 Task 6 evidence。

允许的只读命令：`wc -l`、`nl -ba`、`sed -n`、`rg`、`rg --files`、
`stat`、`readlink`、`shasum -a 256`、`tar -tf`、`command -v`、
`openspec list`、`openspec list --specs`、两条 OpenSpec strict validation，
以及带 `PYTHONDONTWRITEBYTECODE=1` 的当前 Router/Companion project validator。
不要运行 Conda CLI；Conda version 作为输入观察值，executable bytes 通过 SHA 绑定。

## Repository roots

- Router: `/Users/elvis/file/develop/opensource/openspec-superpower-change`
- Companion: `/Users/elvis/file/develop/opensource/codex-brief-antigravity-review`
- transaction root:
  `/private/tmp/add-role-first-review-routing-20260810-FPWT9V`

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
12. `docs/design/reviews/2026-08-11-add-role-first-review-routing-plan-preflight-review.md`
13. `docs/design/evidence/add-role-first-review-routing/2026-08-10-schema6-red.md`
14. `docs/design/evidence/add-role-first-review-routing/2026-08-10-source-verification.md`
15. `docs/design/evidence/add-role-first-review-routing/2026-08-11-conda-plan-amendment-inputs.md`
16. `references/local-instruction-checkpoint.md`
17. `references/request-modes.md`
18. `references/approved-implementation-workflow.md`
19. `references/step-evidence-gate.md`
20. `references/superpowers-adapter.md`
21. `references/self-evolution-rule.md`
22. `references/completion-contract.md`
23. `scripts/validate_cross_cli_sync.py`

Companion：

1. `AGENTS.md`
2. `SKILL.md`
3. `scripts/validate_templates.py`

Temporary bindings（完整读取，不得修改）：

1. `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/preflight-source-bindings-r5.json`
2. `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/source-delta-allowlist-r5.txt`
3. `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/router-tree-source-start.json`
4. `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/companion-tree-source-start.json`
5. `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/router-tree-conda-amendment-r5.json`
6. `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/companion-tree-conda-amendment-r5.json`

Backup 仅核验 path/mode/SHA 与 `tar -tf`：

- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/router-source-preflight-r4.tar`
- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/companion-source-preflight.tar`

## Immutable input bindings

Review 开始与输出 verdict 前各复算一次：

| Input | SHA-256 |
|---|---|
| Revised Plan | `c7158746403282c1d1800fb98c4cf042677e390aaf6c8aabb9ac46e078308fb2` |
| Conda amendment inputs | `fe5c8ef2186b81257be389e30ce297cf5ed3f0d06f93dec5676a91077a79c381` |
| Proposal | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| Design | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| Current tasks progress | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| Spec delta | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| Initial R4 Preflight inputs | `13a2e1a5e1f11517c39bb9fe00e140c6e61884dedc4bf21f1ede6c3cea048f75` |
| Initial R4 Preflight Review PASS | `9fc3aa76e44bd722d8c7fb57f37d2c2e042b244963fc04b4d736fadbd5f8f030` |
| RED evidence | `4c3c74eaac76e01fd7a1536a32785b2fd33ae555b4ca1b6f505969fb6375c3ef` |
| Source verification blocker evidence | `04857f7fd625b5f6a9b17ff8a9fc2d873eccf95de40fb290e47b44fc75317a88` |
| Conda executable `/opt/anaconda3/bin/conda` | `a543f4db6623ff7316d0549c2e5241196499a0d0b3e8d212772eeb2df084c8a3` |
| R5 source-delta allowlist | `99238be04ccb2f8951a1c7430688bad4d17dd1c1739744794ac3f6f66632e3d9` |
| R5 source bindings | `c53f714bf9aa6df8147f8ec01f6d41a5e47c4617b39a289130a39d56987ed731` |
| Router source-start inventory | `7805c4c70512d28b690241073fb134e9f9b7b93ddc0c3f51ea8d320c81ed0151` |
| Companion source-start inventory | `737f700486279fd3d007ba8a9d6e7c96bfff18273eed41d443b6b44b355d068b` |
| Router amendment snapshot | `dc8d1d4ca4d410f5e5bd0d2f7f8d817d3a2d50d8c81d729e564eb357afe04a4e` |
| Companion amendment snapshot | `f4eb4af4c836242eb6cc11311aac4bc89ebf68fb2957ccd515770a4317c31bf9` |
| Router source backup R4 | `a0b7a36e0964fe8e6b93bbcb24a2454bab1c3376159f7cd55f710054d464c491` |
| Companion source backup | `3deab7e813efca3de22ff7d583a5ae089eec079c63842239d9adb85191fb4acc` |

还必须只读确认以下四个路径仍 absent 且不是 symlink：

- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-quick-validate-r1`
- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-home-r1`
- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-pkgs-r1`
- `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-tmp-r1`

任何 binding 漂移或路径占用都必须 verdict `BLOCKED`，不得修复。

## Review questions

逐项回答并引用 exact `path:line` 或 artifact：

1. Approved Proposal/Design/spec 是否未变，Task ledger 是否仅有证据支持的
   checkbox progress，Conda 是否只是 execution-method amendment？
2. Plan revision 是否最小化到 Task 6，并明确不重新授权 Tasks 1–5 或新增 source
   behavior？
3. 用户的 Conda 决定与此前“标准 pip 被拒绝即停止、禁止
   `--break-system-packages`”的边界是否被准确保留？
4. `/opt/anaconda3/bin/conda` 是否 exact hash-bound；prefix/HOME/package cache/TMPDIR
   是否全部在 mode-0700 transaction root 中、review 时 absent，并禁止
   occupied/symlink reuse？
5. `conda create` 是否 exact、禁用 plugins、显式使用内建 `classic` solver、只允许
   `defaults`、Python 3.11 与 PyYAML 6.x，且不 activate、不 `conda init`、不改
   config/base、不用 pip/其他 interpreter？
6. Isolated `HOME` 和 `CONDA_PKGS_DIRS` 是否把 Conda 的可写状态限制在 review
   path；是否仍存在未声明的用户/base mutation 路径？若无法判断必须 `BLOCKED`。
7. Post-create assertions 是否机械证明 Python 3.11、PyYAML major 6、executable 与
   private parents；standard create/guard 失败是否明确停止而不 fallback？
8. 两个 `quick_validate` 是否只使用 bound Conda Python，而 project validators、
   unittest、OpenSpec 是否继续使用 default `python3`/原命令，避免掩盖 fallback？
9. 原 R4 Preflight/source-start/recovery evidence 是否保持不变并仍有历史意义；新
   amendment snapshot 是否如实标为 partial-source review evidence，而没有冒充新的
   pre-implementation baseline？
10. R5 allowlist 是否恰好 49 个 unique/no-wildcard entries，只比 R4 增加 Plan 和
    三个 exact amendment evidence/Review path；R5 bindings 是否满足当前
    `source-delta` exact schema并绑定 revised Plan？
11. Plan 是否错误授权新的 source edit、source PASS、runtime/Pi/Git/canonical/archive/
    publication/completion，或允许删除 Conda environment/backup？
12. 如果 amendment PASS，恢复点是否精确为 Task 6 Step 2 创建环境，然后从 Step 3
    第一条 quick validation 开始；任何后续 FAIL/BLOCKED 是否仍停止？

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

这些结果只证明当前 contract/project-validator consistency，不能证明 Conda create、
quick validation、source correctness、Pi/runtime parity 或 completion。

## Verdict rule

- 只有无 actionable P0/P1/P2 finding、全部 immutable binding 未漂移、四个 Conda
  path 仍 absent、环境写入/依赖/命令/stop/authority 边界机械闭合时返回 `PASS`。
- 任一 finding、漂移、占用、未声明写入、模糊命令、fallback、scope/authority leak
  或无法安全判断都返回 `BLOCKED`。
- Observation 必须说明为何不阻塞、owner 和 release condition；不得把 finding
  改名后返回 PASS。

## Required output

完整返回：

1. Reviewer identity
2. Reviewer Assignment Contract
3. Scope、完整读取清单、开始/结束 SHA、实际只读命令、未取得证据
4. Amendment/Plan summary
5. Findings：P0 / P1 / P2 / Observation；每项含 finding_id、severity、exact
   path:line/artifact、observed fact、violated contract、impact、required correction、
   re-review requirement
6. Prior R4 Preflight/source-start continuity matrix
7. Conda executable/path/write/channel/dependency/isolation matrix
8. Task 6 exact-command/expected/stop matrix
9. R5 allowlist/bindings/current-snapshot/recovery matrix
10. Authority matrix
11. Validation commands/results
12. Verdict：仅 `PASS` 或 `BLOCKED`
13. Exact next action

若 `PASS`，Exact next action 必须说明：把完整 Review 原文返回原 bound Codex
control-plane；独立 reviewer 不创建环境。原 control-plane 复核、持久化本 Review 后，
只执行 Plan Task 6 Step 2 的 exact Conda command；成功后从 Step 3 第一条命令恢复
Task 6 verification。不得重跑/改写 Tasks 1–5，不得执行真实 Pi、runtime、Git、
canonical、archive、publication 或 completion。

若 `BLOCKED`，列出最小修订集合并返回 control-plane；不得自行修文件或环境。
