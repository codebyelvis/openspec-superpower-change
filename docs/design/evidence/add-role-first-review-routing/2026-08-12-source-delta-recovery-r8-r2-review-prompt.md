# Independent Codex Task Prompt — R8 Revision-2 Recovery Preflight

你是用户新打开的独立 Codex 窗口。你未参与 R8 revision 1/2 Plan 编写、
evidence preparation、source implementation 或未来 recovery execution。请对
`add-role-first-review-routing` 的 R8 revision 2 做完整、只读、fail-closed 的
Plan Preflight Review，不得修改任何文件或状态。

## Reviewer Assignment Contract

- `review_purpose.object`：完整 revised R8-r2 Plan；revision-1 `BLOCKED`
  findings `R8-P1-01` / `R8-P1-02` 的机械关闭；exact cache 与 source-parent
  identity/mode；retained dirfd 的 `RENAME_EXCL`；fresh/resumed prepared evidence
  durability；R8-r2 allowlist/bindings/snapshots；R4–R8 history；Step 6 ordering；
  Git/Pi/runtime/canonical/archive/publication/completion boundary。
- `review_purpose.decision`：只判断原 bound Codex control-plane 是否可执行
  revised Task 6 Step 5A exact subshell，并仅在 Step 5A exit `0` 后执行 Step 6。
- `reviewer_product`：`codex`
- `reviewer_role`：`independent-reviewer`
- `capability_profile`：`control-plane-high`
- `independence_requirement`：用户新开的 Codex 窗口；区别于 amendment author、
  revision-1 reviewer、evidence preparer、source executor 和未来 recovery
  executor。无法取得 instance/thread ID 时记录 `unavailable`，不得编造。
- `result_authority`：`governed R8 revision-2 source-delta recovery Plan Preflight evidence only`
- allowed verdicts：`PASS` / `BLOCKED`

本 Review 不授权 backup、move/delete、restore、cleanup、source-delta、source
edit、Git、Pi、runtime、canonical transition、archive、Envelope、publication
或 completion。即使 PASS，也只释放上述两个严格有序命令。

## Paths

- Router `R`：`/Users/elvis/file/develop/opensource/openspec-superpower-change`
- Companion `C`：`/Users/elvis/file/develop/opensource/codex-brief-antigravity-review`
- Transaction root `T`：`/private/tmp/add-role-first-review-routing-20260810-FPWT9V`
- exact cache：`R/scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc`
- exact source parent：`R/scripts/__pycache__`

## Required complete reads

完整读取至 EOF：

### Router

1. `R/AGENTS.md`
2. `R/SKILL.md`
3. `R/CONTEXT.md`
4. `R/openspec/project.md`
5. Proposal、Design、Tasks、change spec delta、current canonical spec
6. `R/docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md`
7. initial R4 Preflight inputs 与 PASS Review
8. schema6 RED evidence
9. source verification 与 current forward summary
10. R7 inputs/prompt/PASS Review
11. R8 revision-1 inputs/prompt/BLOCKED Review
12. `R/docs/design/evidence/add-role-first-review-routing/2026-08-12-source-delta-recovery-r8-r2-inputs.md`
13. `R/references/local-instruction-checkpoint.md`
14. `R/references/request-modes.md`
15. `R/references/approved-implementation-workflow.md`
16. `R/references/step-evidence-gate.md`
17. `R/references/superpowers-adapter.md`
18. `R/references/self-evolution-rule.md`
19. `R/references/completion-contract.md`
20. `R/scripts/validate_cross_cli_sync.py`
21. `R/tests/test_cross_cli_sync.py`

具体历史路径：

- `R/docs/design/evidence/add-role-first-review-routing/2026-08-10-plan-preflight-inputs.md`
- `R/docs/design/reviews/2026-08-11-add-role-first-review-routing-plan-preflight-review.md`
- `R/docs/design/evidence/add-role-first-review-routing/2026-08-10-schema6-red.md`
- `R/docs/design/evidence/add-role-first-review-routing/2026-08-10-source-verification.md`
- `R/docs/design/evidence/add-role-first-review-routing/2026-08-10-role-first-forward-summary.json`
- `R/docs/design/evidence/add-role-first-review-routing/2026-08-11-conda-plan-amendment-r7-inputs.md`
- `R/docs/design/evidence/add-role-first-review-routing/2026-08-11-conda-plan-amendment-r7-review-prompt.md`
- `R/docs/design/reviews/2026-08-11-add-role-first-review-routing-conda-plan-amendment-r7-review.md`
- `R/docs/design/evidence/add-role-first-review-routing/2026-08-11-source-delta-recovery-r8-inputs.md`
- `R/docs/design/evidence/add-role-first-review-routing/2026-08-11-source-delta-recovery-r8-review-prompt.md`
- `R/docs/design/reviews/2026-08-11-add-role-first-review-routing-source-delta-recovery-r8-review.md`

### Companion

1. `C/AGENTS.md`
2. `C/SKILL.md`
3. `C/scripts/validate_templates.py`

### Transaction artifacts

1. `T/preflight-source-bindings-r8-r2.json`
2. `T/source-delta-allowlist-r8.txt`
3. `T/source-delta-allowlist-r8-r2.txt`
4. Router/Companion source-start inventories
5. `T/router-tree-source-delta-recovery-r8-r2-dispatch.json`
6. `T/companion-tree-source-delta-recovery-r8-r2-dispatch.json`

对两个 R4 backup 只核验 path/type/mode/SHA 与 `tar -tf` member list，禁止
提取或读取 member 内容。对 cache 只核验 metadata/SHA，不打印或反汇编 bytes。

## Immutable SHA-256 bindings

开始和 verdict 前各复算一次；任何 drift 都是 `BLOCKED`：

| Artifact | Expected SHA-256 |
|---|---|
| revised R8-r2 Plan | `24c17f8d9170f48c201bbbdf0b8624e0d282f47c35f2c61baac53f01b3c4b1f0` |
| R8-r2 inputs | `a7870875194d8050d9bc34a168e8085ed6beb1c1e788ef083132bbdeb880d26c` |
| Proposal | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| Design | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| Tasks | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| spec delta | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| source verification | `5b014fd0178a7c66a3b328657e1ed3d1d681c73272eb3efee22797ff982f96ad` |
| current forward summary | `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |
| R8-r1 inputs | `c682a913f0ab2ba098c36913588a8a2c74e4da2408a0588760ebeb1cdbe322cb` |
| R8-r1 prompt | `4385533d80174a6e6d657e12e5b30f7c166c06727e1bfa35e4a3ac3fe9a1d89b` |
| R8-r1 BLOCKED Review | `792e64a77a75ea87a4d2c726a5ca88421194fbcb3146609f4b2daca7c767359e` |
| exact cache | `5b7cd72df71d308929c08fb6ae047403b4374e1824a13f479e5034f468dfff49` |
| R8-r2 allowlist | `a53c1d2b8a46f6e4ca8e9b99e8ec6a90f4a27415ef3341760744a7f0e2dc8b26` |
| R8-r2 bindings | `e6e423c30dee8c3b678e94f74aea67667bb61d6c79b60c099a58632f2cefeba3` |
| Router source-start | `7805c4c70512d28b690241073fb134e9f9b7b93ddc0c3f51ea8d320c81ed0151` |
| Companion source-start | `737f700486279fd3d007ba8a9d6e7c96bfff18273eed41d443b6b44b355d068b` |
| Router R8-r2 dispatch snapshot | `929958fbde3d78ff66282ceb3bdee3b301fae68f400875cf02a8b869d3bb678d` |
| Companion R8-r2 dispatch snapshot | `c9e67d141f875877da6d0922281d8a65aa4fcb2a9aa1afab32fa5dc3bb4baecf` |
| Router backup | `a0b7a36e0964fe8e6b93bbcb24a2454bab1c3376159f7cd55f710054d464c491` |
| Companion backup | `3deab7e813efca3de22ff7d583a5ae089eec079c63842239d9adb85191fb4acc` |

Exact cache 必须保持 regular/non-symlink、mode `0644`、size `168579`、device
`16777233`、inode `170846033`、nlink `1`、uid/gid `501/20`。

Exact source parent 必须保持 real directory/non-symlink、mode `0755`、device
`16777233`、inode `163934412`、uid/gid `501/20`。

开始和结束时必须 absent/non-symlink：

- `T/source-delta-recovery-r8`
- `T/source-compare-r8`
- `T/source-delta-r8.json`
- `R/docs/design/reviews/2026-08-12-add-role-first-review-routing-source-delta-recovery-r8-r2-review.md`

Revision-1 Review path 应存在且 SHA 与上表匹配。

## Allowed read-only commands

仅允许：`wc -l`、`nl -ba`、`sed -n`、`rg`/`rg --files`、`stat`、
`readlink`、`shasum -a 256`、`tar -tf`、`openspec list`、
`openspec list --specs`、两条 strict OpenSpec validation、两个指定 project
validator，以及下面两个 exact in-memory probes。

禁止 Git、Conda、pip、Pi、quick_validate、implementation unittest、forward
runner、source-delta、runtime、backup extraction 和未列命令。

### Exact Probe A — parse and finding closure

```bash
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 - <<'PY'
import ast
from pathlib import Path

plan = Path("/Users/elvis/file/develop/opensource/openspec-superpower-change/docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md").read_text()
section = plan[plan.index('- [ ] **Step 5A: Execute the independently reviewed R8 single-cache recovery**'):]
start_marker = "PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 - <<'PY'\n"
start = section.index(start_marker) + len(start_marker)
end = section.index("\nPY\n)\n```", start)
code = section[start:end]
ast.parse(code)

required = {
    'EXPECTED_SOURCE_PARENT_MODE = 0o755',
    'EXPECTED_SOURCE_PARENT_DEVICE = 16777233',
    'EXPECTED_SOURCE_PARENT_INODE = 163934412',
    'EXPECTED_SOURCE_PARENT_UID = 501',
    'EXPECTED_SOURCE_PARENT_GID = 20',
    'def validate_source_parent_fd(fd: int)',
    'os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW',
    'require_exact_payload(PREPARED, prepared_payload, durable=True)',
    'access = os.O_RDWR if durable else os.O_RDONLY',
    'if durable:\n            os.fsync(fd)',
    'validate_source_parent_fd(source_parent_fd)',
    'rename_exclusive(\n            source_parent_fd,',
    'recovery_fd,\n            ORIGINAL.name,',
}
forbidden = [
    'os.unlink(', 'os.remove(', 'os.replace(', 'os.rename(',
    'shutil.rmtree(', '.unlink(', 'rm -', 'git ', 'pi ', 'AT_FDCWD',
]
missing = sorted(x for x in required if x not in code)
hits = sorted(x for x in forbidden if x in code)
assert not missing, missing
assert not hits, hits

parent_open = code.index('source_parent_fd = os.open(')
root_create = code.index('if not os.path.lexists(RECOVERY_ROOT):')
assert parent_open < root_create
parent_validate = code.index('source_parent_stat = validate_source_parent_fd(source_parent_fd)')
assert parent_validate < root_create

prepared_branch = code[
    code.index('if os.path.lexists(PREPARED):'):
    code.index('if os.path.lexists(VERIFIED) and (')
]
assert prepared_branch.index('require_exact_payload(PREPARED, prepared_payload, durable=True)') < prepared_branch.index('os.fsync(recovery_fd)')

rename_branch = code[
    code.index('source_fd, source_stat = open_exact_regular('):
    code.index('moved_stat = os.lstat(ORIGINAL)')
]
assert rename_branch.index('validate_source_parent_fd(source_parent_fd)') < rename_branch.index('rename_exclusive(')
assert rename_branch.index('recovery root identity or mode drift before rename') < rename_branch.index('rename_exclusive(')

print('r8-r2-finding-closure: pass')
PY
```

Expected：`r8-r2-finding-closure: pass`。

### Exact Probe B — R8-r1 to R8-r2 binding delta

```bash
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 - <<'PY'
import json
from pathlib import Path

T = Path("/private/tmp/add-role-first-review-routing-20260810-FPWT9V")
old = (T / "source-delta-allowlist-r8.txt").read_text().splitlines()
new = (T / "source-delta-allowlist-r8-r2.txt").read_text().splitlines()
expected_additions = {
    "router\tdocs/design/evidence/add-role-first-review-routing/2026-08-12-source-delta-recovery-r8-r2-inputs.md",
    "router\tdocs/design/evidence/add-role-first-review-routing/2026-08-12-source-delta-recovery-r8-r2-review-prompt.md",
    "router\tdocs/design/reviews/2026-08-12-add-role-first-review-routing-source-delta-recovery-r8-r2-review.md",
}
assert len(old) == 59 and len(new) == 62 and len(new) == len(set(new))
assert set(old).issubset(new) and set(new) - set(old) == expected_additions
assert not any(any(mark in line for mark in "*?[") for line in new)

bindings = json.loads((T / "preflight-source-bindings-r8-r2.json").read_text())
assert bindings["schema_version"] == 1
assert bindings["plan"]["sha256"] == "24c17f8d9170f48c201bbbdf0b8624e0d282f47c35f2c61baac53f01b3c4b1f0"
assert bindings["source_delta_allowlist"]["sha256"] == "a53c1d2b8a46f6e4ca8e9b99e8ec6a90f4a27415ef3341760744a7f0e2dc8b26"
assert bindings["source_delta_allowlist"]["entries"] == 62

router = json.loads((T / "router-tree-source-delta-recovery-r8-r2-dispatch.json").read_text())
companion = json.loads((T / "companion-tree-source-delta-recovery-r8-r2-dispatch.json").read_text())
assert len(router["records"]) == 341
assert router["excluded_paths"] == [
    "docs/design/evidence/add-role-first-review-routing/2026-08-12-source-delta-recovery-r8-r2-inputs.md",
    "docs/design/evidence/add-role-first-review-routing/2026-08-12-source-delta-recovery-r8-r2-review-prompt.md",
]
assert len(companion["records"]) == 29 and companion["excluded_paths"] == []
print('r8-r2-bindings: pass; allowlist=62; router=341; companion=29')
PY
```

Expected：`r8-r2-bindings: pass; allowlist=62; router=341; companion=29`。

## Required Review questions

1. Revision-1 Review 是否原文保留、SHA 不变，两个 P1 是否分别机械关闭？
2. source-parent `mode/device/inode/uid/gid` 是否在任何 mutation 前及 rename
   紧前复核？持有 dirfd 是否防止父路径替换窗口？
3. `renameatx_np(RENAME_EXCL)` 是否只使用 retained source/recovery dirfd 和
   basename，而非 `AT_FDCWD`/重新解析绝对路径？
4. existing prepared 分支是否在 rename 前通过 no-follow/path-fd identity/
   exact bytes/mode 检查，并对该 file fd fsync，再 fsync recovery dirfd？
5. fresh prepared、existing verified、backup 和 namespace interruption states
   是否仍 fail-closed？
6. Revision-2 allowlist 是否严格为 revision 1 的 59 项加三个 governance
   artifact，无其他 cache/cleanup path、wildcard 或 duplicate？
7. Step 6 是否只在 accepted PASS + Step 5A exit `0` 后使用 r8-r2 bindings，
   且仍要求完整 `unexpected_paths: []`？
8. 是否存在新 fd leak、exception 后误继续、未定义参数、fake probe、危险
   fallback/restore 或 executor 临场决策？
9. Git/Pi/runtime/canonical/archive/publication/completion 是否仍未授权？

## Required output

返回完整报告，至少包含 identity/assignment、complete reads/commands、start/end
SHA/path occupancy、revision summary、P0/P1/P2/Observations、prior-finding closure
matrix、source-parent/dirfd matrix、prepared durability/interruption matrix、
allowlist/binding/history matrix、authority/ordering、validation/probes、verdict 和
exact next action。

`PASS` 仅在无 actionable P0/P1/P2、全部 SHA/path/cache/parent identity 不漂移、
两个旧 P1 真正关闭且没有新 unsafe path 时成立。

若 `PASS`：只允许原 control-plane 先持久化完整 revision-2 Review，复核所有
binding/cache/parent/空闲路径后执行 Step 5A；仅 Step 5A exit `0` 后执行 Step 6。
任何 nonzero/drift 立即停止，不 cleanup/fallback/扩大范围。

若 `BLOCKED`：返回最小修订集合，不自行修复或执行 recovery。
