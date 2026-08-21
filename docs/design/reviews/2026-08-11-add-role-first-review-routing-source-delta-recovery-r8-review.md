# R8 Plan Preflight Review

## 结论

**Verdict：BLOCKED**

全部 immutable SHA、exact cache identity、allowlist、bindings、snapshots、backup 和路径占用在 Review 开始与结束时均未漂移；所有允许的静态验证和两个 exact probe 均通过。

但 Task 6 Step 5A 仍有两个 actionable P1：

1. source parent 的已绑定 mode `0755` 没有被事务代码检查，mode drift 不会阻塞。
2. 中断后重入已有 `prepared.json` 时，只校验内容并 fsync 目录，没有重新 fsync 文件本身，因此不能机械保证 move 前 prepared evidence durable。

因此不释放 Step 5A 或 Step 6。

---

## 1. Reviewer identity 与独立性

| 字段 | 结果 |
|---|---|
| reviewer_product | `codex` |
| reviewer_role | `independent-reviewer` |
| capability_profile | `control-plane-high` |
| instance/thread ID | `unavailable`，未编造 |
| 独立性依据 | 用户明确声明这是新打开的独立 Codex 窗口；本窗口未参与 R8 amendment、evidence preparation、R7 Review、source execution 或未来 recovery execution |
| 可验证限制 | 当前接口没有可供读取的实例或线程标识，因此不能提供系统级 instance-ID 证明 |
| 使用路线 | `codex-brief-antigravity-review` 的 Standalone Lightweight，只读检查，不写 Handoff/canonical/evidence 文件 |
| 实际状态变化 | 无文件写入、无 backup/recovery/source-delta/Git/Pi/runtime/canonical/archive/publication/completion 动作 |

---

## 2. Reviewer Assignment Contract

- `review_purpose.object`：完整 R8 Plan、exact generated-cache 字节绑定、backup/fsync/prepared/exclusive rename 事务、中断恢复、R8 allowlist/bindings/snapshots、R4–R7 continuity、后续 source-delta 和全部 authority boundary。
- `review_purpose.decision`：只决定原 bound Codex control-plane 是否可以运行 Task 6 Step 5A exact subshell，并仅在其 exit `0` 后运行 Step 6 exact source-delta command。
- `result_authority`：governed R8 source-delta recovery Plan Preflight evidence only。
- allowed verdicts：`PASS` / `BLOCKED`。
- 本次 `BLOCKED` 不授权 reviewer 或原 control-plane 执行任何 recovery、cleanup、source-delta 或后续操作。

---

## 3. 完整读取与命令记录

### 完整读至 EOF

Router，28/28：

1. `AGENTS.md`
2. `SKILL.md`
3. `CONTEXT.md`
4. `openspec/project.md`
5. proposal
6. design
7. tasks
8. change spec delta
9. canonical governance spec
10. R8 Plan
11. initial Plan Preflight inputs
12. initial Plan Preflight Review
13. schema6-red
14. source-verification
15. forward-summary JSON
16. R7 inputs
17. R7 prompt
18. R7 PASS Review
19. R8 inputs
20–26. 七个指定 governance references
27. `scripts/validate_cross_cli_sync.py`
28. `tests/test_cross_cli_sync.py`

Companion，3/3：

1. `AGENTS.md`
2. `SKILL.md`
3. `scripts/validate_templates.py`

Transaction bindings，7/7：

1. `preflight-source-bindings-r8.json`
2. R7 allowlist
3. R8 allowlist
4–5. Router/Companion source-start snapshots
6–7. Router/Companion R8 dispatch snapshots

读取使用 `wc -l`、分段 `sed -n`、`nl -ba` 和 `rg`。单行 snapshot JSON 逐记录展开显示直至 EOF。工作树内 `AGENTS.md` 通过 `rg --files -g AGENTS.md` 核对。

### 其他实际命令

- `shasum -a 256`：开始和结束各复算全部 20 项 binding。
- `stat`、`readlink`：cache、source parent、transaction root、backup、四个受限路径。
- `tar -tf`：仅查看两个 backup 的 member list，未提取、未读 member 内容。
- 四个 OpenSpec 命令。
- 两个指定 validator。
- Exact Probe A、Exact Probe B。
- 未运行 Git、Conda、pip、Pi、quick_validate、implementation unittest、forward runner、source-delta 或 runtime command。

### 未取得或按合同禁止取得的证据

- Codex instance/thread ID：`unavailable`。
- R8 Review 持久化文件：按预期仍不存在。
- Step 5A/Step 6 运行证据：未授权，未执行。
- backup member 内容：明确禁止读取，未读取。

---

## 4. Start/end SHA 与路径占用

所有行的完整 digest 在 start、end 和 expected 三者间相同：

| Artifact | SHA-256 | Start | End |
|---|---|---:|---:|
| R8 Plan | `a761b09cda72a9ca01e9e73c2fab861edb293d57c28b37ab0d90329ecdb42aaa` | match | match |
| R8 inputs | `c682a913f0ab2ba098c36913588a8a2c74e4da2408a0588760ebeb1cdbe322cb` | match | match |
| Proposal | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` | match | match |
| Design | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` | match | match |
| Tasks | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` | match | match |
| spec delta | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` | match | match |
| source verification | `5b014fd0178a7c66a3b328657e1ed3d1d681c73272eb3efee22797ff982f96ad` | match | match |
| forward summary | `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` | match | match |
| R7 inputs | `f565ac3e637c41286a083ad78f9417fe0384e97fae99534ead92e35ac258867c` | match | match |
| R7 prompt | `3092db504ca909a69df245229aaef826706832f36bc6e0a4223190c51a5615d5` | match | match |
| R7 PASS Review | `67bf414d43da1678809d1c40892ab0d1fbf16868247dc2584f88c10d3fd0faaa` | match | match |
| exact current cache | `5b7cd72df71d308929c08fb6ae047403b4374e1824a13f479e5034f468dfff49` | match | match |
| R8 allowlist | `2fa0f66b563f000eaf4ff933b0e2cecd22706f4906e0b1a70e0593b8dcc0666d` | match | match |
| R8 bindings | `01d92465d4e15fe0174905fceca49b3c2d49a1aba4f6d3dfc9ee78b1d6fcf096` | match | match |
| Router source-start | `7805c4c70512d28b690241073fb134e9f9b7b93ddc0c3f51ea8d320c81ed0151` | match | match |
| Companion source-start | `737f700486279fd3d007ba8a9d6e7c96bfff18273eed41d443b6b44b355d068b` | match | match |
| Router R8 dispatch | `5de292fd29d5d1edb9cfa099148686f080176a756bbe6c146dac69f966b3ee8b` | match | match |
| Companion R8 dispatch | `c9e67d141f875877da6d0922281d8a65aa4fcb2a9aa1afab32fa5dc3bb4baecf` | match | match |
| Router backup | `a0b7a36e0964fe8e6b93bbcb24a2454bab1c3376159f7cd55f710054d464c491` | match | match |
| Companion backup | `3deab7e813efca3de22ff7d583a5ae089eec079c63842239d9adb85191fb4acc` | match | match |

路径占用：

| Path | Start | End |
|---|---|---|
| `T/source-delta-recovery-r8` | absent、non-symlink | absent、non-symlink |
| `T/source-compare-r8` | absent、non-symlink | absent、non-symlink |
| `T/source-delta-r8.json` | absent、non-symlink | absent、non-symlink |
| R8 Review path | absent、non-symlink | absent、non-symlink |

Exact cache start/end 相同：

- regular、non-symlink
- mode `0644`
- size `168579`
- device `16777233`
- inode `170846033`
- nlink `1`
- uid/gid `501/20`
- atime `1786432366`
- mtime/ctime/birth `1786432346`
- SHA `5b7cd72…dfff49`

Source parent 当前为 real directory、mode `0755`、device `16777233`、uid/gid `501/20`。Transaction root 当前为 real directory、mode `0700`、同设备、uid `501`。

---

## 5. R8 amendment / transaction summary

R8 只新增：

- 一个 exact cache 路径；
- R8 inputs；
- R8 Review prompt；
- R8 Review artifact。

正常 fresh execution 的设计顺序是：

`exact identity check → recovery root → exclusive backup → backup fsync/verify → prepared write/fsync → RENAME_EXCL → 双目录 fsync → original chmod/fsync → verified evidence`

未发现 `unlink`、`remove`、`replace`、普通 rename fallback、`rmtree`、wildcard 或 recursive cleanup。

source-start cache `425e7753…768c66`、size `64486`、mode `0644` 只作为历史 comparison evidence；Plan 的 backup、original 和恢复判断均绑定 current SHA `5b7cd72…dfff49`，没有将 source-start bytes 用作 restore target。

---

## 6. Findings

### P0

无。

### R8-P1-01 — source parent mode drift 未被阻塞

- Severity：P1
- Exact location：[R8 Plan:1395](/Users/elvis/file/develop/opensource/openspec-superpower-change/docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md:1395)、[R8 inputs:61](/Users/elvis/file/develop/opensource/openspec-superpower-change/docs/design/evidence/add-role-first-review-routing/2026-08-11-source-delta-recovery-r8-inputs.md:61)
- Observed fact：代码只检查 source parent 是 real directory 且 device 与 transaction root 相同；没有检查证据绑定的 mode `0755`。Transaction root 自身则检查了 `0700` 和 owner。
- Violated contract：Required Question 7；R8 inputs 对 source parent type/device/mode 的绑定；fail-closed drift 要求。
- Impact：source parent 漂移为例如 `0777` 时，cache bytes/inode 即使未变，事务仍会继续。可写目录会扩大路径替换竞态；post-rename inode check 虽可能最终报错，但在报错前可能已将非 reviewed replacement 移入 recovery root，违反“只 move exact source object”的机械边界。
- Required correction：在任何 recovery-root 创建前及 rename 紧前，对 source parent 的 real-directory、mode `0755`、device 和 owner/identity 做绑定检查；最好持有 no-follow directory fd 并用 dirfd 锚定 exclusive rename，避免父路径替换窗口。
- Owner：R8 Plan amendment author / 原 bound Codex control-plane。
- Release condition：修订后的 exact command 对 source-parent mode/identity drift 返回 nonzero，且 probe 明确断言该 guard。
- Re-review：是；Plan SHA、R8 bindings 和受 Plan 影响的 final snapshot 必须重绑定。

### R8-P1-02 — resumed prepared evidence 未重新 fsync 文件

- Severity：P1
- Exact location：[R8 Plan:1321](/Users/elvis/file/develop/opensource/openspec-superpower-change/docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md:1321)、[R8 Plan:1458](/Users/elvis/file/develop/opensource/openspec-superpower-change/docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md:1458)、[R8 inputs:78](/Users/elvis/file/develop/opensource/openspec-superpower-change/docs/design/evidence/add-role-first-review-routing/2026-08-11-source-delta-recovery-r8-inputs.md:78)
- Observed fact：fresh `write_exclusive(PREPARED, …)` 会 fsync 文件；但中断后如果 `PREPARED` 已存在，`require_exact_payload()` 只读取和比较 bytes，随后只 `fsync_dir(RECOVERY_ROOT)`，没有 `fsync` prepared fd。
- Violated contract：prepared evidence 必须在 removal 前 durable；所有硬中断点必须从 exact durable state 重入。
- Impact：若进程在完整写入后、prepared 文件 fsync 完成前被硬中断，重入可看到 exact bytes 并继续 rename；目录 fsync 不等价于文件数据 fsync。于是 move 可以发生在 prepared 文件尚未重新确认为 durable 的状态。
- Required correction：existing-prepared 分支必须在 no-follow、regular、mode `0600`、exact payload 和 path/fd identity 校验后，对该 fd 再执行 `os.fsync()`，然后 fsync recovery directory，之后才允许 rename。建议对 existing `verified.json` 使用相同 durable helper。
- Owner：R8 Plan amendment author / 原 bound Codex control-plane。
- Release condition：加入可机械检查的“existing prepared file fsync precedes rename”断言，并覆盖 fresh、partial、exact-resume 三种状态。
- Re-review：是；完整 R8 Plan 和所有更新 binding 需重新独立 Preflight。

### P2

无额外独立 P2。上述两项不能降级为 observation，因为都直接影响 PASS 条件。

### R8-O-01 — probe 覆盖边界

- Severity：Observation
- Location：Exact Probe A。
- Observed fact：Probe A 验证了 backup→prepared→rename 的文本顺序和必需常量，但没有断言 source-parent mode guard，也没有断言 resumed prepared fd 的 fsync。
- Impact：解释了 probe PASS 与总体 BLOCKED 并不冲突。
- Required correction：作为两项 P1 修订的一部分扩充 probe。
- Owner：Plan amendment author。
- Release condition：随 P1 关闭。
- Re-review：是。

---

## 7. Exact-cache / backup / interruption matrix

| 状态点 | Reviewed behavior | 结果 |
|---|---|---|
| Review pre-state | exact cache 全 identity/SHA 匹配；四个目标路径空闲 | PASS |
| Recovery-root 创建前 | 先检查 exact cache；T 为 real `0700`/owner；source parent real/same-device | **source-parent mode guard 缺失** |
| Fresh backup | `O_EXCL|O_NOFOLLOW`、mode `0600`、copy current bytes、file fsync、hash/mode verify、directory fsync | PASS |
| 中断于 backup 写入 | 完整 exact backup 可重入；partial/mismatch 被保留并 nonzero | PASS/fail-closed |
| Fresh prepared | exclusive `0600` write、file fsync、directory fsync，发生在 rename 前 | PASS |
| 中断于 prepared | partial/mismatch 阻塞；exact-visible 但未完成 fsync 的文件可重入后直接继续 | **BLOCKED：缺重新 file fsync** |
| 中断于 rename 前 | source exact、original absent 才允许 rename | PASS |
| 中断于 rename | source/original 两种 atomic namespace 结果均可识别；两者共存或两者均无则阻塞 | PASS/fail-closed |
| 中断于 chmod | original `0644` 或 `0600` 可继续；其他 mode 阻塞 | PASS |
| 中断于 verified | inconsistent marker/namespace 阻塞；exact marker 可继续 | PASS；建议 durable helper 同步加强 |
| 成功终态 | source absent；backup/original current SHA、mode `0600`；无 cleanup/restore | 设计满足，但被两个前置 P1 阻塞 |

---

## 8. R7→R8 continuity

| 项目 | 核验结果 |
|---|---|
| R7 allowlist | 55 项 |
| R8 allowlist | 59 项、无 duplicate、无 wildcard |
| Exact additions | cache + inputs + prompt + Review，共四项 |
| Bindings | schema `1`、change ID 正确、Plan SHA 和 allowlist SHA/count 正确 |
| Router source-start | immutable；cache 历史记录仍是 SHA `425e7753…`, size `64486`, mode `0644` |
| Companion source-start | immutable |
| Router R8 dispatch | 338 records；只排除 R8 inputs/prompt；current cache record exact |
| Companion R8 dispatch | 29 records；无 excluded path |
| 非 final preparation snapshots | 明确无 completion/source-delta authority |
| R4–R7 evidence | 所有指定 SHA 开始/结束一致 |
| Router backup | regular、mode `0600`、SHA match、27 members |
| Companion backup | regular、mode `0600`、SHA match、14 members |

Router backup members：

```text
SKILL.md
CONTEXT.md
README.md
README_cn.md
CHANGELOG.md
references/approved-implementation-workflow.md
references/agent-capability-routing.md
references/completion-contract.md
references/cross-cli-portable-manifest.json
references/cross-cli-sync.md
references/handoff-contract.md
references/request-modes.md
references/response-patterns.md
references/self-evolution-rule.md
references/shared-global-governance.md
references/step-evidence-gate.md
references/superpowers-adapter.md
references/sync-checklist.md
scripts/validate_core_gates.py
scripts/validate_cross_cli_sync.py
tests/test_workflow_rules.py
tests/test_cross_cli_sync.py
openspec/changes/add-role-first-review-routing/proposal.md
openspec/changes/add-role-first-review-routing/design.md
openspec/changes/add-role-first-review-routing/tasks.md
openspec/changes/add-role-first-review-routing/specs/skill-workflow-governance/spec.md
docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md
```

Companion backup members：

```text
SKILL.md
README.md
README_cn.md
CHANGELOG.md
agents/openai.yaml
references/agy-dispatch-template.md
references/brief-template.md
references/handed-off-external-execution.md
references/handoff-contract.md
references/report-template.md
references/review-template.md
references/timeout-audit-template.md
scripts/validate_templates.py
tests/test_workflow_rules.py
```

没有提取 archive。

---

## 9. Source-delta ordering 与 authority

| 阶段 | 条件 | Authority |
|---|---|---|
| Persist R8 Review | 完整 Review 持久化并由原 control-plane 接受 | 只建立 Preflight evidence |
| Step 5A | Review PASS 且所有 binding/cache/path 再复核无漂移 | 只允许 exact single-cache transaction |
| Step 6 | 仅 Step 5A exit `0` | 只允许 exact R8 no-Git source-delta command |
| Step 6 nonzero/drift | 立即停止 | 不 cleanup、不 fallback、不扩大范围 |
| Git/Pi/runtime/canonical/archive/publication/Envelope/completion | 无论本 Review 结果 | 未授权 |

Plan 的 Step 6 明确使用 R8 bindings、source-start baselines、`source-compare-r8` 和 `source-delta-r8.json`，并要求完整树 inventory、backup validation、allowlist enforcement 和 `unexpected_paths: []`。

---

## 10. Required questions

1. **是。** R8 只扩大一个 exact pycache path 和三个 R8 evidence/Review paths。
2. **是。** 当前 SHA/size/mode/device/inode/nlink 全部匹配；source-start bytes 仅为历史证据，不是 restore target。
3. **是。** fresh/resumed exact backup 在 removal 前 no-follow/exclusive 创建或验证并 fsync。
4. **部分否。** fresh prepared durable；existing prepared 重入缺 file fsync。Rename 本身是 exact-path、same-filesystem `RENAME_EXCL`。
5. **否。** root/backup/rename/chmod/verified 状态基本闭合；prepared exact-visible-but-not-durable 的重入状态未闭合。
6. **成功正常路径是。** backup/original 都使用 current bytes 和 mode `0600`；没有 overwrite/unlink/rmtree/recursive cleanup。
7. **否。** symlink、special file、cross-device、cache identity drift 会阻塞，但 source-parent mode drift 不会阻塞。
8. **是。** 严格为 55+4，无 wildcard、duplicate 或额外 cleanup path。
9. **是。** bindings、source-start、backups、final dispatch snapshots 与 R4–R7 可追溯；非 final snapshots 无 authority。
10. **是。** Step 6 只在 Step 5A exit `0` 后，使用 R8 exact paths，并要求 no-Git complete delta PASS。
11. **是。** 没有授权其他 source edit、Git、Pi、runtime、canonical、archive、publication、Envelope 或 completion。
12. **存在两个必须修订的机械缺口。** 未发现 fake contract、未定义参数或危险 restore；缺口是 source-parent mode guard 和 resumed prepared durability。

---

## 11. Validation / probe results

| Command | Result |
|---|---|
| `openspec list` | change 可见，24/41 tasks |
| `openspec list --specs` | governance spec，30 requirements |
| change strict validation | `Change 'add-role-first-review-routing' is valid` |
| all strict validation | `3 passed, 0 failed` |
| Router core gates | `Core gates valid`，exit `0` |
| Companion templates | `Validation succeeded`，exit `0` |
| Exact Probe A | `r8-transaction-structure: pass` |
| Exact Probe B | `r8-bindings-shape: pass; allowlist=59; router=338; companion=29` |

这些 PASS 不覆盖两项 P1 所述的 transaction semantic gaps。

---

## 12. Exact next action

最小修订集合：

1. 只修订 Task 6 Step 5A：
   - 绑定并检查 source parent mode/identity，确保 drift 在任何 mutation 前阻塞；
   - existing `prepared.json` 在 rename 前重新验证并 fsync 文件，再 fsync 目录。
2. 扩充结构 probe，机械断言：
   - source-parent mode guard；
   - resumed prepared file fsync 严格早于 `rename_exclusive`。
3. 重算并持久化新的 Plan SHA、R8 inputs/bindings、受影响的 final dispatch snapshot 和 Review prompt；保持 R4–R7 历史 immutable。
4. 从 recovery/compare/delta/Review 四路径仍为空闲的状态重新发起独立 R8 Plan Preflight Review。

在新的独立 Review 返回并被接受为 `PASS` 前：**不得执行 Step 5A、Step 6、cleanup、fallback 或任何扩大范围的动作。**
