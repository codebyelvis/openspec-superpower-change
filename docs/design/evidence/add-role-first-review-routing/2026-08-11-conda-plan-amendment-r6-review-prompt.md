# Independent Conda Plan Amendment Preflight Review Prompt — Revision 6

你是用户新打开的另一个独立 Codex 窗口。请对
`add-role-first-review-routing` Task 6 Conda Plan amendment revision 6 执行
完整、只读、fail-closed 的 Plan Preflight Review。

Revision 5 因 `F-R5-001` 返回 `BLOCKED`：Task 6 Step 2/3 的 exact shell
commands 没有机械 fail-fast。Revision 6 只修复该 finding，并建立新的 immutable
binding chain。

## Reviewer Assignment Contract

- review_purpose.object:
  - revised complete implementation Plan；
  - R5 `BLOCKED` Review 与 `F-R5-001` closure；
  - Task 6 Step 2/3 fail-fast shell semantics；
  - Conda executable/dependency/channel/path/write boundary；
  - R4 source-start/recovery、R5 history、R6 partial-source snapshot 连续性；
  - R6 allowlist/bindings；
  - Git/Pi/runtime/canonical/archive/publication/completion authority。
- review_purpose.decision:
  仅决定原 bound Codex control-plane 是否可执行 revised Plan Task 6 Step 2
  的 exact Conda subshell，并在成功后从 Step 3 第一条命令恢复 verification。
- reviewer_product: `codex`
- reviewer_role: `independent-reviewer`
- capability_profile: `control-plane-high`
- independence_requirement:
  - 用户新打开的另一个 Codex 窗口；
  - 不得是 R5 reviewer、Plan/amendment author、evidence preparer、source executor
    或未来 Conda/environment executor；
  - 不得修改当前 revision；
  - instance/thread ID 不可取得时如实记录 `unavailable` 与
    `user_opened_separate_window`。
- result_authority:
  - `governed Conda Plan amendment revision-6 Preflight evidence only`；
  - verdict 仅 `PASS` / `BLOCKED`；
  - 不批准 Tasks 1–5 重执行/改写、source correctness/PASS/High Review、真实 Pi、
    runtime、Git、canonical transition、archive、Envelope、publication、completion
    或 cleanup。

## Strict read-only boundary

- 不修改、创建、删除、chmod 或格式化任何文件；
- 不创建、激活、更新、删除任何 Conda environment；
- 不运行 Conda CLI、pip、quick_validate、implementation unittest、forward probe、
  source-delta、Git、Pi、runtime 或 cleanup；
- 不提取 backups，仅允许 `tar -tf`；
- 不更新 tasks、canonical state、archive、Envelope 或 completion。

允许：`wc -l`、`nl -ba`、`sed -n`、`rg`、`rg --files`、`stat`、
`readlink`、`shasum -a 256`、`tar -tf`、`command -v`、`/bin/zsh -n`
（只解析从 Plan 提取的 Step 2/3 blocks，不执行）、OpenSpec list/strict
validation，以及带 `PYTHONDONTWRITEBYTECODE=1` 的两个 project validators。

## Roots

- Router: `/Users/elvis/file/develop/opensource/openspec-superpower-change`
- Companion: `/Users/elvis/file/develop/opensource/codex-brief-antigravity-review`
- transaction root: `/private/tmp/add-role-first-review-routing-20260810-FPWT9V`

## Required complete reads

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
16. `docs/design/evidence/add-role-first-review-routing/2026-08-11-conda-plan-amendment-review-prompt.md`
17. `docs/design/reviews/2026-08-11-add-role-first-review-routing-conda-plan-amendment-review.md`
18. `docs/design/evidence/add-role-first-review-routing/2026-08-11-conda-plan-amendment-r6-inputs.md`
19. `references/local-instruction-checkpoint.md`
20. `references/request-modes.md`
21. `references/approved-implementation-workflow.md`
22. `references/step-evidence-gate.md`
23. `references/superpowers-adapter.md`
24. `references/self-evolution-rule.md`
25. `references/completion-contract.md`
26. `scripts/validate_cross_cli_sync.py`

Companion：

1. `AGENTS.md`
2. `SKILL.md`
3. `scripts/validate_templates.py`

Temporary bindings（完整读取，不修改）：

1. `T/preflight-source-bindings-r6.json`
2. `T/source-delta-allowlist-r6.txt`
3. `T/router-tree-source-start.json`
4. `T/companion-tree-source-start.json`
5. `T/router-tree-conda-amendment-r6.json`
6. `T/companion-tree-conda-amendment-r6.json`

Backup 只核验 path/mode/SHA/`tar -tf`：

- `T/router-source-preflight-r4.tar`
- `T/companion-source-preflight.tar`

其中 `T` 必须展开为
`/private/tmp/add-role-first-review-routing-20260810-FPWT9V`。

## Immutable bindings

开始 Review 和 verdict 前各复算一次：

| Input | SHA-256 |
|---|---|
| Revised Plan R6 | `341a0e7320c436c734b4b29d7992287a70c50bef627607d0dd18fe1a313a66d6` |
| R6 amendment inputs | `a2444d79f6b20841ea55ec71faa481e0cf1b811cf24111e522734eb6b0ea5b23` |
| Proposal | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| Design | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| Current tasks | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| Spec delta | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| R4 inputs | `13a2e1a5e1f11517c39bb9fe00e140c6e61884dedc4bf21f1ede6c3cea048f75` |
| R4 PASS Review | `9fc3aa76e44bd722d8c7fb57f37d2c2e042b244963fc04b4d736fadbd5f8f030` |
| RED evidence | `4c3c74eaac76e01fd7a1536a32785b2fd33ae555b4ca1b6f505969fb6375c3ef` |
| Source blocker | `04857f7fd625b5f6a9b17ff8a9fc2d873eccf95de40fb290e47b44fc75317a88` |
| R5 inputs | `fe5c8ef2186b81257be389e30ce297cf5ed3f0d06f93dec5676a91077a79c381` |
| R5 prompt | `b151534cd424493699539608e9e9f2c49abb198d5acb83ce110e0033eb06ace6` |
| R5 BLOCKED Review | `64eadbe090dc3f50c2201348703c111088358eaf9677a56f3b444e3238a6b1f1` |
| Conda executable | `a543f4db6623ff7316d0549c2e5241196499a0d0b3e8d212772eeb2df084c8a3` |
| R6 allowlist | `02bb64585bdc8da44c360307fae28e3a8575b37c93096cd0c5e3ce653ae2c16a` |
| R6 bindings | `14cc54cf0a8c9a8a60347006b55627c65011fda631b6a99e161c00b19f5600e3` |
| Router source-start | `7805c4c70512d28b690241073fb134e9f9b7b93ddc0c3f51ea8d320c81ed0151` |
| Companion source-start | `737f700486279fd3d007ba8a9d6e7c96bfff18273eed41d443b6b44b355d068b` |
| Router R6 snapshot | `3d2b018faa70839c8cb32f4f8c44b8709d4b8581b8e8dbe9ea105159ead60a4d` |
| Companion R6 snapshot | `f4eb4af4c836242eb6cc11311aac4bc89ebf68fb2957ccd515770a4317c31bf9` |
| Router backup | `a0b7a36e0964fe8e6b93bbcb24a2454bab1c3376159f7cd55f710054d464c491` |
| Companion backup | `3deab7e813efca3de22ff7d583a5ae089eec079c63842239d9adb85191fb4acc` |

只读确认四个 Conda path 仍 absent/non-symlink：

- `T/conda-quick-validate-r1`
- `T/conda-home-r1`
- `T/conda-pkgs-r1`
- `T/conda-tmp-r1`

任何 drift/occupancy 必须 `BLOCKED`。

## Review questions

逐项引用 exact path:line/artifact：

1. Revision 6 是否只修 `F-R5-001` 与派生 binding，没有重写 R4/R5 history、
   OpenSpec contract、Tasks 1–5 或 source behavior？
2. Step 2 exact block 是否是一个 closed subshell，首两行依次为 `(`、
   `set -euo pipefail`，最后为 `)`，且 `/bin/zsh -n` 解析 PASS？
3. 四个 path 是否各有独立、top-level `test ! -e` 和 `test ! -L`，不存在会被
   `set -e` 条件语义豁免的 `&&`/`||` guard list？
4. Conda hash/version、mkdir、create、executable/mode/Python/PyYAML assertion 是否
   都是 fail-fast subshell 中的 standalone required command；任一 nonzero 是否立即
   终止，且无 fallback/automatic cleanup？
5. `shasum | awk` 是否受 `pipefail` 约束，version command substitution failure 是否
   会导致 enclosing `test` nonzero；是否仍有早期失败被末尾成功掩盖的路径？
6. Step 3 是否也是 exact `set -euo pipefail` subshell，八条验证按顺序执行并在首个
   nonzero 停止，不能继续到后续 quick/unit/OpenSpec command？
7. Conda executable/path/HOME/cache/TMPDIR/plugin/classic solver/defaults/
   Python/PyYAML/write boundaries 是否未回归？
8. R6 allowlist 是否 52 unique/no-wildcard entries，完整保留 R5 49 entries并只增加
   R6 input/prompt/Review 三项；R6 bindings 是否 exact schema并绑定 current Plan？
9. R4 source-start/backups与R5 `BLOCKED` Review是否保持不可回写；R6 snapshots是否
   如实为 partial-source evidence？
10. PASS 是否只允许 control-plane 执行 Step 2，成功后执行 Step 3；不授权 source
    PASS/Review、Pi/runtime/Git/canonical/archive/publication/completion/cleanup？

## Required validation

Router root：

```bash
openspec validate add-role-first-review-routing --strict
openspec validate --all --strict --no-interactive
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .
```

Companion root：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_templates.py .
```

另外只解析、不执行 Task 6 Step 2/3 shell blocks：使用内存/stdin 将 exact block
传给 `/bin/zsh -n`；不得创建临时脚本。

这些 PASS 不证明 Conda create、quick/unit/source/runtime/completion。

## Verdict rule

- 无 actionable P0/P1/P2、全部 hash/path/shape/parse/authority 边界通过，且
  `F-R5-001` 机械关闭，才可 `PASS`。
- 任一 drift、finding、模糊 fail-fast、隐式 fallback、占用、未声明写入或权限扩大
  必须 `BLOCKED`。
- Observation 必须有 non-blocking reason、owner、release condition。

## Required output

完整返回：

1. Reviewer identity
2. Reviewer Assignment Contract
3. Scope/complete reads/start-end SHA/read-only commands/missing evidence
4. Revision-6 summary
5. Findings P0/P1/P2/Observation（完整 finding fields）
6. `F-R5-001` closure matrix
7. Task 6 Step 2/3 fail-fast command matrix
8. Conda isolation matrix
9. R4/R5/R6 continuity and allowlist/bindings/snapshot/recovery matrix
10. Authority matrix
11. Validation/parse results
12. Verdict：仅 `PASS` / `BLOCKED`
13. Exact next action

若 `PASS`：要求把完整 Review 返回原 bound Codex control-plane；reviewer 不创建
环境。Control-plane 持久化并核验后，只运行 revised Plan Task 6 Step 2 exact
subshell；成功后运行 Step 3 exact subshell。不得重跑/改写 Tasks 1–5，不得执行
source PASS/High Review、真实 Pi、runtime、Git、canonical、archive、publication、
completion 或 cleanup。

若 `BLOCKED`：列出最小 correction set，reviewer 不修文件或环境。
