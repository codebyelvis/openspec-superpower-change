# Independent Conda Plan Amendment Preflight Review Prompt — Revision 7

你是用户新打开的另一个独立 Codex 窗口。请对
`add-role-first-review-routing` Task 6 Conda Plan amendment revision 7 执行
完整、只读、fail-closed 的 Plan Preflight Review。

Revision 6 因 `F-R6-001` 与 `F-R6-002` 返回 `BLOCKED`：Plan 的 hash、version、
mode producers 仍可能被外层 `test` 掩盖；R6 reviewer 还使用了未获准的 `jq`。
Revision 7 只修复 producer status propagation，并建立新的 immutable binding
chain。`F-R6-002` 只能由新的、严格遵守命令 allowlist 的 Review run 释放。

## Reviewer Assignment Contract

- review_purpose.object:
  - revised complete implementation Plan；
  - R6 `BLOCKED` Review 与 `F-R6-001`/`F-R6-002` closure；
  - Task 6 Step 2 assignment-only producer failure propagation；
  - Task 6 Step 2/3 fail-fast shell semantics；
  - Conda executable/dependency/channel/path/write boundary；
  - R4 source-start/recovery、R5/R6 history、R7 partial-source snapshot 连续性；
  - R7 allowlist/bindings；
  - Git/Pi/runtime/canonical/archive/publication/completion authority。
- review_purpose.decision:
  仅决定原 bound Codex control-plane 是否可执行 revised Plan Task 6 Step 2
  的 exact Conda subshell，并在成功后执行 Step 3 exact subshell。
- reviewer_product: `codex`
- reviewer_role: `independent-reviewer`
- capability_profile: `control-plane-high`
- independence_requirement:
  - 用户新打开的另一个 Codex 窗口；
  - 不得是 R5 reviewer、R6 reviewer、Plan/amendment author、evidence preparer、
    source executor 或未来 Conda/environment executor；
  - 不得修改当前 revision；
  - instance/thread ID 不可取得时如实记录 `unavailable` 与
    `user_opened_separate_window`。
- result_authority:
  - `governed Conda Plan amendment revision-7 Preflight evidence only`；
  - verdict 仅 `PASS` / `BLOCKED`；
  - 不批准 Tasks 1–5 重执行/改写、source correctness/PASS/High Review、真实 Pi、
    runtime、Git、canonical transition、archive、Envelope、publication、completion
    或 cleanup。

## Strict read-only boundary and command allowlist

- 不修改、创建、删除、chmod 或格式化任何文件；
- 不创建、激活、更新、删除任何 Conda environment；
- 不运行 Conda CLI、pip、quick_validate、implementation unittest、forward probe、
  source-delta、Git、Pi、runtime 或 cleanup；
- 不提取 backups，仅允许 `tar -tf`；
- 不更新 tasks、canonical state、archive、Envelope 或 completion；
- 明确禁止 `jq`；即使只读也不得使用未列出的替代命令。

允许的命令只有：

- `wc -l`
- `nl -ba`
- `sed -n`
- `rg`、`rg --files`
- `stat`
- `readlink`
- `shasum -a 256`
- `tar -tf`
- `command -v`
- 下文给出的两个 exact、read-only、`PYTHONDONTWRITEBYTECODE=1`
  `/usr/bin/python3 -` inline probes；不得自行扩展其读写范围
- OpenSpec list/strict validation
- 带 `PYTHONDONTWRITEBYTECODE=1` 的两个 project validators

任何未列出的命令尝试，无论是否写入或成功，都必须作为 actionable finding 并
返回 `BLOCKED`。

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
19. `docs/design/evidence/add-role-first-review-routing/2026-08-11-conda-plan-amendment-r6-review-prompt.md`
20. `docs/design/reviews/2026-08-11-add-role-first-review-routing-conda-plan-amendment-r6-review.md`
21. `docs/design/evidence/add-role-first-review-routing/2026-08-11-conda-plan-amendment-r7-inputs.md`
22. `references/local-instruction-checkpoint.md`
23. `references/request-modes.md`
24. `references/approved-implementation-workflow.md`
25. `references/step-evidence-gate.md`
26. `references/superpowers-adapter.md`
27. `references/self-evolution-rule.md`
28. `references/completion-contract.md`
29. `scripts/validate_cross_cli_sync.py`

Companion：

1. `AGENTS.md`
2. `SKILL.md`
3. `scripts/validate_templates.py`

Temporary bindings（完整读取，不修改）：

1. `T/preflight-source-bindings-r7.json`
2. `T/source-delta-allowlist-r7.txt`
3. `T/router-tree-source-start.json`
4. `T/companion-tree-source-start.json`
5. `T/router-tree-conda-amendment-r7.json`
6. `T/companion-tree-conda-amendment-r7.json`

Backup 只核验 path/mode/SHA/`tar -tf`：

- `T/router-source-preflight-r4.tar`
- `T/companion-source-preflight.tar`

其中 `T` 必须展开为
`/private/tmp/add-role-first-review-routing-20260810-FPWT9V`。

## Immutable bindings

开始 Review 和 verdict 前各复算一次：

| Input | SHA-256 |
|---|---|
| Revised Plan R7 | `3a6169b892151a29d7cfa1ce96798e15c659327c6db34fc1e054d65c6ed39a80` |
| R7 amendment inputs | `f565ac3e637c41286a083ad78f9417fe0384e97fae99534ead92e35ac258867c` |
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
| R6 inputs | `a2444d79f6b20841ea55ec71faa481e0cf1b811cf24111e522734eb6b0ea5b23` |
| R6 prompt | `dc3d755b695242d524e0a746911a995f3cdb0232b114ba1b86b1a52d790d28d6` |
| R6 BLOCKED Review | `b6d41aa854ad8561ca94341408b1d513f43d2fd3ea7b1786d33da4df04339104` |
| Conda executable | `a543f4db6623ff7316d0549c2e5241196499a0d0b3e8d212772eeb2df084c8a3` |
| R7 allowlist | `6a0b0f27bcc61af2249e4d219fa8afb75f01ba67b8259c3c6cac32628acd61f0` |
| R7 bindings | `9d740c6a594de2f0b431ea815d870038b09be16b06506f10fd5ee5d5f95a3f0b` |
| Router source-start | `7805c4c70512d28b690241073fb134e9f9b7b93ddc0c3f51ea8d320c81ed0151` |
| Companion source-start | `737f700486279fd3d007ba8a9d6e7c96bfff18273eed41d443b6b44b355d068b` |
| Router R7 snapshot | `db498b0b1cbb0d9bd4daffee77a25acf8a3b572a63238be18bc40835a037a857` |
| Companion R7 snapshot | `f4eb4af4c836242eb6cc11311aac4bc89ebf68fb2957ccd515770a4317c31bf9` |
| Router backup | `a0b7a36e0964fe8e6b93bbcb24a2454bab1c3376159f7cd55f710054d464c491` |
| Companion backup | `3deab7e813efca3de22ff7d583a5ae089eec079c63842239d9adb85191fb4acc` |

只读确认四个 Conda path 仍 absent/non-symlink：

- `T/conda-quick-validate-r1`
- `T/conda-home-r1`
- `T/conda-pkgs-r1`
- `T/conda-tmp-r1`

任何 drift/occupancy 必须 `BLOCKED`。

## Exact read-only structural probes

### Probe A：Plan shell parse、producer shape 与 adversarial status propagation

只能从 Router root 原样运行；它从内存读取并解析 Plan，不写文件，不执行 Conda：

```bash
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 - <<'PY'
import pathlib
import subprocess

path = pathlib.Path("docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md")
plan = path.read_text(encoding="utf-8")

def fenced_after(marker: str) -> str:
    start = plan.index(marker)
    token = chr(96) * 3 + "bash\n"
    begin = plan.index(token, start) + len(token)
    end = plan.index("\n" + chr(96) * 3, begin)
    return plan[begin:end]

step2 = fenced_after("**Step 2: Create the independently reviewed Conda verification environment**")
step3 = fenced_after("**Step 3: Run quick/project/unit validation**")
for name, block in (("step2", step2), ("step3", step3)):
    parsed = subprocess.run(["/bin/zsh", "-n"], input=block, text=True, capture_output=True)
    assert parsed.returncode == 0, (name, parsed.stderr)
    print(f"{name}-shell-parse: pass")

assert 'test "$(shasum' not in step2
assert 'test "$(HOME=' not in step2
assert 'test "$(stat' not in step2
for name in (
    "ROLE_CONDA_SHA",
    "ROLE_CONDA_VERSION",
    "ROLE_CONDA_HOME_MODE",
    "ROLE_CONDA_PKGS_MODE",
    "ROLE_CONDA_TMP_MODE",
):
    assert step2.count(name + '="$(') == 1, name
    assert step2.count('test "$' + name + '"') == 1, name
print("producer-comparison-shape: pass; assignment_only=5; comparisons=5")

cases = {
    "single-producer": r'''(
set -euo pipefail
VALUE="$(/bin/zsh -c 'print -n expected; exit 7')"
test "$VALUE" = expected
print reached
)''',
    "pipeline-producer": r'''(
set -euo pipefail
VALUE="$(/bin/zsh -c 'print expected; exit 7' | /usr/bin/awk '{print $1}')"
test "$VALUE" = expected
print reached
)''',
}
for name, script in cases.items():
    result = subprocess.run(["/bin/zsh"], input=script, text=True, capture_output=True)
    assert result.returncode == 7, (name, result.returncode, result.stdout, result.stderr)
    assert "reached" not in result.stdout
    print(f"{name}-failure-propagation: pass; exit=7; reached=false")
PY
```

### Probe B：R7 allowlist/bindings/snapshot shape

只能原样运行；它只读 T 下已绑定文件，不写文件：

```bash
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 - \
  /private/tmp/add-role-first-review-routing-20260810-FPWT9V <<'PY'
import hashlib
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
r6 = (root / "source-delta-allowlist-r6.txt").read_text(encoding="utf-8").splitlines()
r7_path = root / "source-delta-allowlist-r7.txt"
r7 = r7_path.read_text(encoding="utf-8").splitlines()
assert len(r6) == 52
assert len(r7) == 55
assert len(set(r7)) == 55
assert not (set(r6) - set(r7))
assert set(r7) - set(r6) == {
    "router\tdocs/design/evidence/add-role-first-review-routing/2026-08-11-conda-plan-amendment-r7-inputs.md",
    "router\tdocs/design/evidence/add-role-first-review-routing/2026-08-11-conda-plan-amendment-r7-review-prompt.md",
    "router\tdocs/design/reviews/2026-08-11-add-role-first-review-routing-conda-plan-amendment-r7-review.md",
}
for line in r7:
    product, relative = line.split("\t")
    assert product in {"router", "companion"}
    assert not any(char in relative for char in "*?[")

bindings = json.loads((root / "preflight-source-bindings-r7.json").read_text(encoding="utf-8"))
assert set(bindings) == {
    "schema_version", "change_id", "plan", "backups",
    "preflight_tree_baselines", "source_delta_allowlist",
}
assert bindings["schema_version"] == 1
assert bindings["change_id"] == "add-role-first-review-routing"
assert bindings["plan"]["sha256"] == "3a6169b892151a29d7cfa1ce96798e15c659327c6db34fc1e054d65c6ed39a80"
assert bindings["source_delta_allowlist"]["sha256"] == hashlib.sha256(r7_path.read_bytes()).hexdigest()
assert bindings["source_delta_allowlist"]["entries"] == 55

router = json.loads((root / "router-tree-conda-amendment-r7.json").read_text(encoding="utf-8"))
companion = json.loads((root / "companion-tree-conda-amendment-r7.json").read_text(encoding="utf-8"))
assert len(router["records"]) == 334
assert len(companion["records"]) == 29
assert router["excluded_paths"] == [
    "docs/design/evidence/add-role-first-review-routing/2026-08-11-conda-plan-amendment-r7-inputs.md",
    "docs/design/evidence/add-role-first-review-routing/2026-08-11-conda-plan-amendment-r7-review-prompt.md",
]
assert companion["excluded_paths"] == []
print("r7-allowlist-bindings-snapshots: pass; entries=55; router=334; companion=29")
PY
```

## Review questions

逐项引用 exact path:line/artifact：

1. Revision 7 是否只修 `F-R6-001` 与派生 binding，没有重写 R4/R5/R6
   history、OpenSpec contract、Tasks 1–5、source behavior 或 Step 3 顺序？
2. Step 2 是否仍是 closed `set -euo pipefail` subshell，四组 path guards仍为
   独立顶层 `test ! -e` / `test ! -L`，且 `/bin/zsh -n` PASS？
3. SHA、version、三个 mode producers 是否各自为 plain assignment-only simple
   command，随后才是独立 `test`；不存在 `export`/`readonly`/`typeset` 等可能
   改写 producer exit status 的 wrapper？
4. Producer 输出期望值后返回 nonzero 时，普通 command substitution 与
   `pipefail` pipeline 是否都在 assignment 处终止，不能到达 comparison 或后续命令？
5. `conda create`、executable assertion、Python/PyYAML assertion、无 fallback/
   automatic cleanup 规则是否未回归？
6. Step 3 是否保持 exact `set -euo pipefail` subshell和原八条命令顺序，首个
   nonzero 停止且不隐式重建 Conda？
7. Conda executable/path/HOME/cache/TMPDIR/plugin/classic solver/defaults/
   Python/PyYAML/write boundaries 是否未回归？
8. R7 allowlist 是否 55 unique/no-wildcard entries，完整保留 R6 52 entries并只
   增加 R7 input/prompt/Review 三项；R7 bindings是否绑定 current Plan？
9. R4 source-start/backups、R5/R6 `BLOCKED` Reviews是否保持不可回写；R7
   snapshots是否如实为 partial-source evidence？
10. 本 reviewer 是否全程只使用本提示词明确允许的命令，特别是没有 `jq`、Conda、
    Git、Pi、quick/unit/forward/source-delta/runtime 命令？
11. PASS 是否只允许 control-plane 执行 Step 2，成功后执行 Step 3；不授权 source
    PASS/Review、Pi/runtime/Git/canonical/archive/publication/completion/cleanup？

## Required validation

Router root：

```bash
openspec list
openspec list --specs
openspec validate add-role-first-review-routing --strict
openspec validate --all --strict --no-interactive
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .
```

Companion root：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_templates.py .
```

另外运行上文 exact Probe A 与 Probe B。不得运行 Conda create、quick_validate、
implementation unittest、forward probe 或 source-delta。

这些 PASS 不证明 Conda create、quick/unit/source/runtime/completion。

## Verdict rule

- 无 actionable P0/P1/P2、全部 hash/path/shape/parse/status-propagation/
  command-compliance/authority 边界通过，且 `F-R6-001` 与 `F-R6-002` 均关闭，
  才可 `PASS`。
- 任一 drift、finding、模糊 fail-fast、producer failure masking、隐式 fallback、
  path 占用、未声明写入、未列命令或权限扩大必须 `BLOCKED`。
- Observation 必须有 non-blocking reason、owner、release condition。

## Required output

完整返回：

1. Reviewer identity
2. Reviewer Assignment Contract
3. Scope/complete reads/start-end SHA/read-only commands/missing evidence
4. Revision-7 summary
5. Findings P0/P1/P2/Observation（完整 finding fields）
6. `F-R6-001`/`F-R6-002` closure matrix
7. Task 6 Step 2/3 producer/fail-fast command matrix
8. Conda isolation matrix
9. R4/R5/R6/R7 continuity and allowlist/bindings/snapshot/recovery matrix
10. Authority matrix
11. Validation/Probe A/Probe B results
12. Verdict：仅 `PASS` / `BLOCKED`
13. Exact next action

若 `PASS`：要求把完整 Review 返回原 bound Codex control-plane；reviewer 不创建
环境。Control-plane 持久化并核验后，只运行 revised Plan Task 6 Step 2 exact
subshell；成功后运行 Step 3 exact subshell。不得重跑/改写 Tasks 1–5，不得执行
source PASS/High Review、真实 Pi、runtime、Git、canonical、archive、publication、
completion 或 cleanup。

若 `BLOCKED`：列出最小 correction set，reviewer 不修文件或环境。
