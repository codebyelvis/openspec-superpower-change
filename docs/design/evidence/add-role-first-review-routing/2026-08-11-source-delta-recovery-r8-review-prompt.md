# Independent Codex Task Prompt — R8 Source-delta Recovery Preflight

你是用户新打开的独立 Codex 窗口。你没有参与 R8 Plan amendment、输入
证据、source 实施或未来 cache recovery 执行。请进行一次完整、只读、
fail-closed 的 Plan Preflight Review；不要修改任何文件或状态。

## Reviewer Assignment Contract

- `review_purpose.object`：`add-role-first-review-routing` 完整 R8 Plan；唯一
  generated cache 的当前字节绑定；先备份、fsync、prepared evidence、再用
  same-filesystem exclusive rename 移除单一路径的事务；中断恢复；R8 exact
  allowlist/bindings/snapshots；R4–R7 evidence continuity；后续 source-delta；
  Git/Pi/runtime/canonical/archive/publication/completion authority boundary。
- `review_purpose.decision`：只决定原 bound Codex control-plane 是否可以执行
  R8 Plan Task 6 Step 5A exact subshell，并且仅在其 exit `0` 后执行 Task 6
  Step 6 exact source-delta command。
- `reviewer_product`：`codex`
- `reviewer_role`：`independent-reviewer`
- `capability_profile`：`control-plane-high`
- `independence_requirement`：用户打开的新 Codex 窗口；与 R8 amendment
  author、evidence preparer、R7 reviewer、source executor 及未来 recovery
  executor 分离。若 instance/thread ID 不可取得，如实写 `unavailable`，不得
  编造。
- `result_authority`：`governed R8 source-delta recovery Plan Preflight evidence only`
- allowed verdicts：`PASS` / `BLOCKED`

本 Review 不授权 reviewer 或原 control-plane 在 verdict 被接受前执行 backup、
move、delete、restore、cleanup、source-delta、source edit、Git、Pi、runtime、
canonical transition、archive、Envelope、publication 或 completion。即使 PASS，
也只释放上面 decision 中的两个有序命令，不授予其他权限。

## Paths

- Router root `R`：
  `/Users/elvis/file/develop/opensource/openspec-superpower-change`
- Companion root `C`：
  `/Users/elvis/file/develop/opensource/codex-brief-antigravity-review`
- Transaction root `T`：
  `/private/tmp/add-role-first-review-routing-20260810-FPWT9V`
- exact cache：
  `R/scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc`

## Required complete reads

逐文件完整读至 EOF，不得只读摘要：

### Router

1. `R/AGENTS.md`
2. `R/SKILL.md`
3. `R/CONTEXT.md`
4. `R/openspec/project.md`
5. `R/openspec/changes/add-role-first-review-routing/proposal.md`
6. `R/openspec/changes/add-role-first-review-routing/design.md`
7. `R/openspec/changes/add-role-first-review-routing/tasks.md`
8. `R/openspec/changes/add-role-first-review-routing/specs/skill-workflow-governance/spec.md`
9. `R/openspec/specs/skill-workflow-governance/spec.md`
10. `R/docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md`
11. `R/docs/design/evidence/add-role-first-review-routing/2026-08-10-plan-preflight-inputs.md`
12. `R/docs/design/reviews/2026-08-11-add-role-first-review-routing-plan-preflight-review.md`
13. `R/docs/design/evidence/add-role-first-review-routing/2026-08-10-schema6-red.md`
14. `R/docs/design/evidence/add-role-first-review-routing/2026-08-10-source-verification.md`
15. `R/docs/design/evidence/add-role-first-review-routing/2026-08-10-role-first-forward-summary.json`
16. `R/docs/design/evidence/add-role-first-review-routing/2026-08-11-conda-plan-amendment-r7-inputs.md`
17. `R/docs/design/evidence/add-role-first-review-routing/2026-08-11-conda-plan-amendment-r7-review-prompt.md`
18. `R/docs/design/reviews/2026-08-11-add-role-first-review-routing-conda-plan-amendment-r7-review.md`
19. `R/docs/design/evidence/add-role-first-review-routing/2026-08-11-source-delta-recovery-r8-inputs.md`
20. `R/references/local-instruction-checkpoint.md`
21. `R/references/request-modes.md`
22. `R/references/approved-implementation-workflow.md`
23. `R/references/step-evidence-gate.md`
24. `R/references/superpowers-adapter.md`
25. `R/references/self-evolution-rule.md`
26. `R/references/completion-contract.md`
27. `R/scripts/validate_cross_cli_sync.py`
28. `R/tests/test_cross_cli_sync.py`

### Companion

1. `C/AGENTS.md`
2. `C/SKILL.md`
3. `C/scripts/validate_templates.py`

### Transaction bindings

1. `T/preflight-source-bindings-r8.json`
2. `T/source-delta-allowlist-r7.txt`
3. `T/source-delta-allowlist-r8.txt`
4. `T/router-tree-source-start.json`
5. `T/companion-tree-source-start.json`
6. `T/router-tree-source-delta-recovery-r8-dispatch.json`
7. `T/companion-tree-source-delta-recovery-r8-dispatch.json`

对两个 backup 只核验 path、type、mode、SHA 和 `tar -tf` member list；禁止
提取或读取 member contents：

- `T/router-source-preflight-r4.tar`
- `T/companion-source-preflight.tar`

对 exact cache 只核验 path/type/mode/size/device/inode/link-count/time/SHA，
不要打印或反汇编二进制内容。

## Immutable SHA-256 bindings

Review 开始和 verdict 前各复算一次；任何 drift 都是 `BLOCKED`：

| Artifact | Expected SHA-256 |
|---|---|
| R8 Plan | `a761b09cda72a9ca01e9e73c2fab861edb293d57c28b37ab0d90329ecdb42aaa` |
| R8 inputs | `c682a913f0ab2ba098c36913588a8a2c74e4da2408a0588760ebeb1cdbe322cb` |
| Proposal | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| Design | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| Tasks | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| spec delta | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| source verification | `5b014fd0178a7c66a3b328657e1ed3d1d681c73272eb3efee22797ff982f96ad` |
| current forward summary | `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |
| R7 inputs | `f565ac3e637c41286a083ad78f9417fe0384e97fae99534ead92e35ac258867c` |
| R7 prompt | `3092db504ca909a69df245229aaef826706832f36bc6e0a4223190c51a5615d5` |
| R7 PASS Review | `67bf414d43da1678809d1c40892ab0d1fbf16868247dc2584f88c10d3fd0faaa` |
| exact current cache | `5b7cd72df71d308929c08fb6ae047403b4374e1824a13f479e5034f468dfff49` |
| R8 allowlist | `2fa0f66b563f000eaf4ff933b0e2cecd22706f4906e0b1a70e0593b8dcc0666d` |
| R8 bindings | `01d92465d4e15fe0174905fceca49b3c2d49a1aba4f6d3dfc9ee78b1d6fcf096` |
| Router source-start | `7805c4c70512d28b690241073fb134e9f9b7b93ddc0c3f51ea8d320c81ed0151` |
| Companion source-start | `737f700486279fd3d007ba8a9d6e7c96bfff18273eed41d443b6b44b355d068b` |
| Router R8 dispatch snapshot | `5de292fd29d5d1edb9cfa099148686f080176a756bbe6c146dac69f966b3ee8b` |
| Companion R8 dispatch snapshot | `c9e67d141f875877da6d0922281d8a65aa4fcb2a9aa1afab32fa5dc3bb4baecf` |
| Router backup | `a0b7a36e0964fe8e6b93bbcb24a2454bab1c3376159f7cd55f710054d464c491` |
| Companion backup | `3deab7e813efca3de22ff7d583a5ae089eec079c63842239d9adb85191fb4acc` |

Source-start cache record must remain exactly:

- SHA `425e7753b96e7cca2ad645d9a5385e52532e83dd19540ecb7d11ba3adb768c66`
- size `64486`
- mode `0644`

Current cache must remain regular/non-symlink, size `168579`, mode `0644`,
device `16777233`, inode `170846033`, link count `1`, current SHA above. If the
inode changes but the exact bytes/type/mode/path remain stable, report the drift
and return `BLOCKED`; do not silently relax the reviewed identity.

At Review start and end these paths must remain absent and non-symlink:

- `T/source-delta-recovery-r8`
- `T/source-compare-r8`
- `T/source-delta-r8.json`
- `R/docs/design/reviews/2026-08-11-add-role-first-review-routing-source-delta-recovery-r8-review.md`

## Allowed read-only commands

只允许：

- `wc -l`
- `nl -ba`
- `sed -n`
- `rg`、`rg --files`
- `stat`
- `readlink`
- `shasum -a 256`
- `tar -tf`（禁止提取）
- `openspec list`
- `openspec list --specs`
- `openspec validate add-role-first-review-routing --strict`
- `openspec validate --all --strict --no-interactive`
- `PYTHONDONTWRITEBYTECODE=1 python3 R/scripts/validate_core_gates.py R`
- `PYTHONDONTWRITEBYTECODE=1 python3 C/scripts/validate_templates.py C`
- 下列两个 exact in-memory probes

禁止 Git、Conda、pip、Pi、quick_validate、implementation unittest、forward
runner、source-delta、runtime command、backup extraction，以及未列出的命令。

### Exact Probe A — transaction code structure and parse

```bash
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 - <<'PY'
import ast
from pathlib import Path

plan = Path("/Users/elvis/file/develop/opensource/openspec-superpower-change/docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md").read_text()
marker = '- [ ] **Step 5A: Execute the independently reviewed R8 single-cache recovery**'
section = plan[plan.index(marker):]
start_marker = "PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 - <<'PY'\n"
start = section.index(start_marker) + len(start_marker)
end = section.index("\nPY\n)\n```", start)
code = section[start:end]
ast.parse(code)
required = {
    'SOURCE = Path("/Users/elvis/file/develop/opensource/openspec-superpower-change/scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc")',
    'EXPECTED_SHA256 = "5b7cd72df71d308929c08fb6ae047403b4374e1824a13f479e5034f468dfff49"',
    'SOURCE_START_SHA256 = "425e7753b96e7cca2ad645d9a5385e52532e83dd19540ecb7d11ba3adb768c66"',
    'EXPECTED_SIZE = 168579',
    'EXPECTED_SOURCE_DEVICE = 16777233',
    'EXPECTED_SOURCE_INODE = 170846033',
    'EXPECTED_SOURCE_NLINK = 1',
    'EXPECTED_SOURCE_UID = 501',
    'EXPECTED_SOURCE_GID = 20',
    'RENAME_EXCL = 0x00000004',
    'require_source_identity=True',
    'copy_backup()',
    'write_exclusive(PREPARED, prepared_payload)',
    'rename_exclusive(SOURCE, ORIGINAL)',
    'os.fsync(backup_fd)',
    'fsync_dir(SOURCE.parent)',
}
missing = sorted(item for item in required if item not in code)
forbidden = [
    'os.unlink(', 'os.remove(', 'os.replace(', 'os.rename(',
    'shutil.rmtree(', '.unlink(', 'rm -', 'git ', 'pi ',
]
hits = sorted(item for item in forbidden if item in code)
main = code[code.index("if os.path.lexists(BACKUP):"):]
pre_recovery = code[
    code.index("if not os.path.lexists(RECOVERY_ROOT):"):
    code.index("recovery_stat = os.lstat(RECOVERY_ROOT)")
]
assert pre_recovery.index("open_exact_regular(") < pre_recovery.index("os.mkdir(")
assert main.index("copy_backup()") < main.index("write_exclusive(PREPARED, prepared_payload)") < main.index("rename_exclusive(SOURCE, ORIGINAL)")
assert not missing, missing
assert not hits, hits
print("r8-transaction-structure: pass")
PY
```

Expected exact stdout: `r8-transaction-structure: pass`.

### Exact Probe B — allowlist, bindings and snapshot shape

```bash
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 - <<'PY'
import hashlib
import json
from pathlib import Path

T = Path("/private/tmp/add-role-first-review-routing-20260810-FPWT9V")
old = (T / "source-delta-allowlist-r7.txt").read_text().splitlines()
new = (T / "source-delta-allowlist-r8.txt").read_text().splitlines()
expected_additions = {
    "router\tscripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc",
    "router\tdocs/design/evidence/add-role-first-review-routing/2026-08-11-source-delta-recovery-r8-inputs.md",
    "router\tdocs/design/evidence/add-role-first-review-routing/2026-08-11-source-delta-recovery-r8-review-prompt.md",
    "router\tdocs/design/reviews/2026-08-11-add-role-first-review-routing-source-delta-recovery-r8-review.md",
}
assert len(old) == 55 and len(new) == 59 and len(new) == len(set(new))
assert set(old).issubset(new)
assert set(new) - set(old) == expected_additions
assert not any(any(mark in line for mark in "*?[") for line in new)

bindings = json.loads((T / "preflight-source-bindings-r8.json").read_text())
assert bindings["schema_version"] == 1
assert bindings["change_id"] == "add-role-first-review-routing"
assert bindings["plan"]["sha256"] == "a761b09cda72a9ca01e9e73c2fab861edb293d57c28b37ab0d90329ecdb42aaa"
assert bindings["source_delta_allowlist"]["sha256"] == "2fa0f66b563f000eaf4ff933b0e2cecd22706f4906e0b1a70e0593b8dcc0666d"
assert bindings["source_delta_allowlist"]["entries"] == 59

router = json.loads((T / "router-tree-source-delta-recovery-r8-dispatch.json").read_text())
companion = json.loads((T / "companion-tree-source-delta-recovery-r8-dispatch.json").read_text())
assert len(router["records"]) == 338
assert router["excluded_paths"] == [
    "docs/design/evidence/add-role-first-review-routing/2026-08-11-source-delta-recovery-r8-inputs.md",
    "docs/design/evidence/add-role-first-review-routing/2026-08-11-source-delta-recovery-r8-review-prompt.md",
]
assert len(companion["records"]) == 29 and companion["excluded_paths"] == []
cache = [r for r in router["records"] if r["path"] == "scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc"]
assert cache == [{
    "kind": "file",
    "mode": "0644",
    "path": "scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc",
    "sha256": "5b7cd72df71d308929c08fb6ae047403b4374e1824a13f479e5034f468dfff49",
    "size": 168579,
}]
print("r8-bindings-shape: pass; allowlist=59; router=338; companion=29")
PY
```

Expected exact stdout:
`r8-bindings-shape: pass; allowlist=59; router=338; companion=29`.

## Required Review questions

逐项明确回答：

1. R8 是否只扩大到一个 exact pycache path 和三个 R8 evidence/Review paths？
2. 当前 SHA/size/mode/inode 是否与 Review binding 一致？source-start bytes 是否
   只作历史证据，未被当成 restore target？
3. backup 是否在任何 removal 前 exclusive/no-follow 创建、校验并 fsync？
4. `prepared.json` 是否在 move 前 durable；move 是否只对 exact source 使用
   same-filesystem `RENAME_EXCL`？
5. 硬中断发生在 recovery-root 创建、backup、prepared、rename、chmod、verified
   各点时，重入是否只继续 exact state，歧义是否 fail-closed？
6. backup 和 moved original 是否都保留 exact current bytes、mode `0600`；是否
   没有 overwrite/unlink/rmtree/recursive cleanup？
7. source/transaction parent 的 type/device/mode guards 是否充分；symlink、special
   file、cross-device 或 drift 是否阻塞？
8. R8 allowlist 是否严格为 R7 55 项加四项；是否无 wildcard/duplicate/其他
   cleanup path？
9. bindings、source-start、backups、R8 final snapshots 与 R4–R7 history 是否
   immutable/可追溯；非 final R8 preparation snapshots 是否明确无 authority？
10. Step 6 是否只在 Step 5A exit `0` 后使用 R8 bindings/compare/output 路径，且
    仍要求完整 no-Git delta PASS？
11. Plan 是否没有扩展到其他 source edit、cleanup、Git、Pi、runtime、canonical、
    archive、publication、Envelope 或 completion？
12. 是否存在 fake contract、未定义参数、不可机械验证的成功判据、危险 restore、
    或 executor 必须临场发明的关键行为？

## Required output

返回完整报告，至少包含：

1. Reviewer identity 与独立性证据
2. Reviewer Assignment Contract
3. 完整读取清单、实际命令、未取得证据
4. start/end SHA table 与 path occupancy
5. R8 amendment/transaction summary
6. Findings：P0/P1/P2/Observations；每项含 ID、severity、exact path/line、
   observed fact、violated contract、impact、required correction、owner、release
   condition、是否需 re-review
7. exact-cache / backup-before-removal / interruption-state matrix
8. R7→R8 allowlist、bindings、snapshots、backup/history continuity matrix
9. source-delta ordering 与 authority matrix
10. validation/probe results
11. verdict：`PASS` 或 `BLOCKED`
12. exact next action

`PASS` 条件：无 actionable P0/P1/P2；所有 immutable SHA 开始/结束匹配；exact
cache 未漂移；recovery/compare/delta/Review paths 仍未被占用；backup-before-
removal、durability、interruption resume、单一路径范围和 authority boundary
均机械闭合。

如果 `PASS`，exact next action 必须只允许原 bound Codex control-plane：先持久化
完整 Review，再复核 binding/cache/path 未漂移，然后执行 Task 6 Step 5A；只有
Step 5A exit `0` 才可执行 Step 6。任何 nonzero/drift 都必须停止，不 cleanup、
fallback 或扩大范围。

如果 `BLOCKED`，返回最小修订集合；不得自行修复或执行 recovery。
