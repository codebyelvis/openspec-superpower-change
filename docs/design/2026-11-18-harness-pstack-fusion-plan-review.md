# `fuse-harness-pstack-guardrails` 设计稿独立评审结论

- **Author**: elvis
- **Reviewer**: Claude Opus 5.5（Antigravity，只读独立会话，`same_instance=false`）
- **Date**: 2026-11-18
- **Review Purpose**: Major Self-Evolution 设计稿 Preflight 评审（边界兼容 / 误伤漏判 / 反膨胀 / 执行闭环）
- **Reviewed Target**: `docs/design/2026-11-18-harness-pstack-fusion-analysis-and-plan.md`（`REVIEW_DRAFT`）
- **Repository Baseline**: `main` @ `7829572`（`origin/main..HEAD` 1 个本地提交，工作区含既有未暂存历史文件）
- **Result Authority**: advisory input only；不授予实现、Git、同步或完成权
- **Verdict**: **需修改（`FAIL`）** —— 7 项阻塞（B1–B7）+ 9 项改进（S1–S9）

> [!NOTE]
> 评审范围：设计稿全文；`SKILL.md`、`scripts/gov_runner.py`、`scripts/autoloop_ctl.py`、`scripts/validate_core_gates.py`（2480–2515 行）、`references/{autoloop-review-hunt,approved-implementation-workflow,autoloop-req-acceptance,project-learning-closeout,self-evolution-rule,skill-iteration-loop,cross-cli-sync,sync-checklist}.md`、`references/cross-cli-portable-manifest.json`、`tests/test_workflow_rules.py`（2181–2197、6128–6160 行）、`tests/test_gov_runner_git_capture.py` 的 `verify_command` 用例。
>
> 未运行：任何单测、`validate_core_gates.py`、`validate_cross_cli_sync.py`、`openspec validate`。全部结论基于源码与规则静态核对；本机 `python3 --version` = 3.11.7、`/usr/bin/python3 --version` = 3.9.6 为实测。

---

## 0. 给执行方（Carbon）的修订指令摘要

1. 设计稿不得直接进入实现。先按本文 §5 修订清单改稿，再走 **Phase A**（落盘并 `openspec validate fuse-harness-pstack-guardrails --strict` 后停下等批准）。
2. 收到 `迭代优化skill：已批准 fuse-harness-pstack-guardrails` 后才进入 **Phase B** 实现；Git `add/commit/push` 需用户另行显式授权。
3. 修订稿需回答每条 B/S 编号（采纳 / 不采纳 + 理由），便于 `FOCUSED_RECHECK`。

---

## 1. 边界兼容性

### B1【阻塞】审批顺序违反 Major Self-Evolution 门禁

- **依据**：
  - `references/self-evolution-rule.md:47-52`：“Major Self-Evolution starts only after a specific OpenSpec change exists, passes strict validation, and the user explicitly approves that change-id … approval of a review draft … does not substitute for approval of the concrete OpenSpec change.”
  - `references/skill-iteration-loop.md:30`：“The command does not approve a Major change-id that does not yet exist.”
- **问题**：设计稿 Anchor 3 让用户批准本设计稿后，Step 1 才创建 OpenSpec change，随后连续实现。批准对象是草稿而非已存在且通过 strict 的 change。
- **最小修复**：拆两段——Phase A 只落盘 `openspec/changes/fuse-harness-pstack-guardrails/` + `--strict` + 停；Phase B 凭 `迭代优化skill：已批准 <change-id>` 实现。

### B2【阻塞】Step 5 Git 写操作无授权来源

- **依据**：
  - `references/skill-iteration-loop.md:24-26`：Git 租约仅 Patch/Minor；“Major with `已批准 <change-id>` → Implement only the specific approved OpenSpec change and scoped contract.”
  - `SKILL.md:210-212`：“Never run `git add`, `git commit` … unless the user explicitly commands it.” / “Do not push without explicit user approval.”
- **问题**：示例批准语 `已批准 fuse-harness-pstack-guardrails，按计划推进` 不覆盖 `git add/commit/push`。
- **最小修复**：Step 5 改为独立授权点，明确需用户显式提交 / 推送指令。

### B3【阻塞】Major 草稿缺必备项

- **依据**：`references/self-evolution-rule.md:38-45` 要求草稿含 “exact rule snippets to add or change”“validation and forward-test plan”“rollback path”；第 31 行 Major 的 Forward-test 为 Required。
- **问题**：F2/F4/F5 只有意图描述，无待写入的规则原文；无回滚路径；Anchor 4 仅单元测试，未规划 `tests/run_*_forward_tests.py` 类 forward-test。
- **最小修复**：在设计稿补 §“Exact Rule Snippets”（逐文件给出新增/替换原文）、§“Rollback”（备份路径 + 还原命令 + 四端回退）、§“Forward-test”（至少一条 fast 模式高敏路径升档与一条零测试否决的隔离 fixture 正向演练）。

### S1 F2/F3 与猎杀清单自身措辞冲突（Anchor 漏列修改点）

- `references/autoloop-review-hunt.md:1`（标题 `review_profile=pre-mr`）、`:5`（“Use this reference only in `pre-mr` read-only reviews”）、`:10`（“Four Conditional Hunt Lenses”）。F3 在 `fast` 下挂载该清单，不改则审查员可合理判整份清单 n/a。
- `scripts/autoloop_ctl.py:593` pre-mr 判定句要求每个 FAIL 给出“重试/分页/崩溃重入触发路径”，日志卫生类 finding 无法满足，需同步改写。
- `fast` prompt（`autoloop_ctl.py:596-607`）当前无猎杀清单条目与 `hunt:` 输出要求，F3 需写明升档后的 prompt 差异。
- **修复**：Anchor 1/2 显式列入上述三处。

### S2 F4 大部分已存在且贴近禁区

- `references/approved-implementation-workflow.md:511` 已有 “the same finding recurs after a verified fix”，并被 `tests/test_workflow_rules.py:2181-2197` 锁定。
- 新增大写 `NO_PROGRESS` 标记紧邻第 525 行 “Do not create an `ESCALATED` state … second state system”，语义上像引入 Harness 状态。
- **修复**：approved-implementation-workflow 侧不引入 `NO_PROGRESS`；最多在第 511 行补“或 `failure_signature` 相同”。

### S3 F4“不可达证明才可驳回”颠倒举证责任

- 冲突对象：全局反膨胀原则 1（“Review 亦不得以纯假设性风险阻断通过”）；`references/autoloop-review-hunt.md:7-8`（finding 须证明 concrete failure path、禁无调用方的防御性要求）；`approved-implementation-workflow.md` 约 497–501 行（scope 扩张应拒绝 / `OUT_OF_SCOPE_PREEXISTING_DEBT`）。
- **修复**：改为“已附可达触发路径的同范围 finding，不得以本地未复现驳回”；无触发路径者不要求实现方证明不可达；保留 scope triage 驳回理由。

### S4 F5 与学习晋升阈值冲突

- “既有散文规则再次被违反视为失效，须升档机械拦截”绕过 `references/project-learning-closeout.md:81`（two independent correction or Review signals）、`:94`（single low-risk task-local correction 不晋升）与 CCG-012（Candidate 不得自动改全局 Skill）。
- “主动精简冗余散文”可能被用于删除 Non-Negotiables 或 `validate_core_gates.py:2491-2510` 必检短语。
- **修复**：升档须经 Learning Candidate Pipeline；加护栏“精简治理散文本身按 Major 处理，不得删除校验器锁定短语或 Non-Negotiables”。

---

## 2. 误伤 / 漏判风险

### B4【阻塞】`setup_or_env_error` 把 Import 类错误判为环境问题

- **触发**：TDD RED（测试先引用尚未实现的模块/符号）、模块重命名、漏建 `__init__`，都会产生 `ModuleNotFoundError` / `ImportError`，属代码缺陷。
- **影响**：叠加 F4 第 1 条“优先修环境、不得盲改业务代码”，Agent 会去改 PATH 或 `pip install`（还可能触碰环境写边界），偏离根因。设计稿 Anchor 4 测试用例 `import nonexistent_pkg_xyz` 恰好与代码缺陷不可区分。
- **最小修复**：`setup_or_env_error` 仅凭退出码 `126/127` 或 `command not found` 判定；Import 类一律 `verification_failed`。

### B5【阻塞】`empty_test_execution` 误伤 Maven 多模块

- **触发**：`mvn -pl a,b -Dtest=X -Dsurefire.failIfNoSpecifiedTests=false test` 中不含 `X` 的模块打印 `Tests run: 0,`，整体退出码 0，其他模块真实执行。
- **最小修复**：聚合判定——全部输出中只要存在正计数（`Ran [1-9]\d* tests`、`Tests run: [1-9]`、`[1-9]\d* passed`）即不否决；仅在无任何正计数且命中零执行信号时否决。
- **附带**：pytest 零收集退出码为 `5`；Python ≥3.12 unittest `NO TESTS RAN` 亦退出 `5`。这些走 `v_code != 0` 分支会被归为 `verification_failed`，建议 `failure_kind` 同样可输出 `empty_test_execution`；pytest 系列正则在 `v_code == 0` 路径可删。
- **签名改动注意**：`evaluate_deterministic_vetoes(batch, snap_meta, raw)`（`gov_runner.py:350`）当前不接收 `v_code`，需从 `raw/verify.exit` 读取或扩参，并同步既有直接调用方。

### B6【阻塞】F3 无 `--base-ref` 时检测范围与审查快照不一致

- **依据**：`scripts/gov_runner.py:222-231` fast 模式会按 `@{upstream}` → reflog `Created from` 自动解析基线，审查员能看到已提交未推送的分支 Diff。
- **问题**：`_detect_high_risk_paths(cwd, base_ref)` 若在 `base_ref` 为空时只看工作区，“本地 commit 后再零参数 `/autoloop`”场景高敏路径漏判，且与审查员所见不一致。
- **最小修复**：复用 gov_runner 同一基线解析（同目录 importlib 加载，仿 `_load_commit_checker`），或把判定移到快照后基于 `git.changed_files.txt`；保持单一真源。

### S5 F3 路径规则漏网与挂载方式

- 漏网：Flyway 默认 `db/migration`（单数）、Liquibase `db/changelog`、Java 包 `permission`（单数）、`oauth`/`authz`/`authentication`。误升档只多耗算力（安全方向），漏升档才是风险。建议按路径段匹配同义词集合；`tests/`、`test/` 排除需明确为“任意路径段”而非仅顶层（否则 `src/test/resources/*.sql` 升档，可接受但应写明）。
- 挂载：`gov_runner.py:629` 只接受目录（`os.path.isdir`），不能把 `HUNT_REF` 文件直接放进 `extra_read_dirs`；沿用 `autoloop_ctl.py:612` 的 `HUNT_REF.parent`。

### S6 F1.1 PATH 末尾追加无法修复所述 Homebrew `python3` 问题

- launchd PATH 中 `/usr/bin` 在前，`python3` 仍解析为 `/usr/bin/python3`（本机 3.9.6）。
- **修复**：`autoloop_ctl.py run` 在用户终端执行时把当前 `PATH` 写入 batch（如 `verify_env_path`），gov_runner 构造子进程 env 时使用；无需硬编码 `/opt/homebrew/bin`（也与 `7829572` 去机器路径的方向一致）。

### S7 `failure_signature` 归一化未定义

- 不剥离耗时（`in 0.123s`）、临时路径、内存地址、时间戳，签名几乎永不相等，早停失效；过度归一化则误判相等。
- Anchor 4 仅断言同一 `assert 1 == 2` 稳定，覆盖不足。
- **建议**：签名 = `failure_kind` + 失败用例 ID 集合（或首个错误行）剥离数字/路径后的 SHA-256 前 16 位；补“同失败不同耗时签名相等 / 不同失败签名不等”两条断言。

### S8 `verify_error_excerpt` 未脱敏

- 1200 字符 stderr 尾部会透传到 `autoloop_ctl.py` 标准输出并进入对话；stderr 可能含 Token、连接串、认证头。这与 F2 第 ③ 条及全局安全底线自相矛盾。
- **修复**：输出前做最小脱敏（`(?i)(token|secret|password|authorization|api[_-]?key)\s*[:=]\s*\S+`、`://user:pass@`），`receipt.json` 同样处理；原始 `verify.stderr` 保留在 raw 目录不外显。

---

## 3. 反膨胀

| 融合项 | 评审建议 |
|---|---|
| F1.1 PATH 补齐 | 收窄为透传调用方 PATH（S6），删除固定目录列表 |
| F1.2 短路 + 二分 | 保留短路；分类按 B4 收窄为退出码判定 |
| F1.3 零执行否决 | 保留，改正计数豁免聚合判定（B5）；pytest 正则可删 |
| F2 诊断透镜 | ① 与第 4 透镜 “no silent exception swallowing”（`autoloop-review-hunt.md:34`）重复；② `log.error` 后 rethrow 属团队风格；③ 凭证泄露已是全局安全底线。**建议仅保留“吞异常 / 异常日志缺业务主键”一条，或并入第 4 透镜** |
| F3 高敏升档 | 保留，按 B6/S5 修正；控制在单函数内 |
| F4 返修纪律 | approved-implementation-workflow 侧整段删除（S2）；autoloop-req-acceptance 侧保留一行 `Attack the Premise`。“最多 2 轮”上限下签名早停最多省 1 轮，可并入同一行 |
| F5 四级阶梯 | 保留一句阶梯；“主动精简”必须加 S4 护栏 |

---

## 4. 执行闭环完整性

### B7【阻塞】Anchor 3 缺必经治理阶段

- **依据**：
  - `scripts/validate_core_gates.py:2491-2497` 锁定顺序：`Implement -> Verify -> Review PASS -> Project Learning Closeout -> fresh final verification -> final Review -> OpenSpec reconcile/archive and strict validation`。
  - `references/cross-cli-sync.md:95-102`：`validated source + Review PASS -> generate plan -> Review plan and target snapshots -> apply … -> verify all required targets -> final Review`。
  - CCG-004 / CCG-007：Preflight Review → Implement → Verify → Review；便携核心 Skill 优化须 final Codex Review。
- **问题**：计划只有自举 `/autoloop`（被修改的 gov_runner 验收自身改动，属自证，非独立 Review）；缺独立 Implementation Review、Project Learning Closeout、fresh final verification、final Review、同步计划 Review、fuse change 归档与 `openspec/specs/skill-workflow-governance/spec.md` 回写。
- **最小修复**：Anchor 3 按上述顺序补齐，并为每个 Review 指定 product / role / profile / `same_instance=false`（CCG-016）。

### S9 Step 3 自举命令实际跑不到预期内容

- `scripts/autoloop_ctl.py:309`：tasks 全部勾选的 change 会被跳过；实现完成后 `match` 会转去命中仓库内其他十余个活跃 change 之一。
- `scripts/autoloop_ctl.py:72` `OPENSPEC_TEST_CMD_RE` 不匹配 `PYTHONPATH=. … /opt/homebrew/bin/python3 -m unittest …` 与 `python3 "$HOME/…/quick_validate.py"`，自动提取只剩 `openspec validate`。
- **修复**：显式 `--req openspec/changes/fuse-harness-pstack-guardrails/proposal.md --cmd "<全量门禁命令>"`。

### 历史未暂存文件隔离缺口

1. **测试态 ≠ 提交态**：全量单测运行在含 `tests/test_external_grok_control_plane.py` 改动与未跟踪 `openspec/changes/archive/2026-11-11-*`、`openspec/specs/external-grok-control-plane/` 的脏工作区，GREEN 不代表最终 commit。建议本地 commit 后 `git worktree add /tmp/<x> HEAD` 在干净副本重跑全量（只读于主工作区，不触碰既有文件）。
2. **快照混入历史文件**：`gov_runner.py:304` 把未跟踪路径并入 `git.changed_files.txt`，自举审查员会看到历史债务并可能判 FAIL；Prompt 须列明 `OUT_OF_SCOPE_PREEXISTING_DEBT` 路径。
3. **学习落点冲突**：本次存在 Review 历史，按 `AGENTS.md` 完成前需读 `docs/engineering-invariants.md` 与 Closeout；若需晋升到该文件，其已有未暂存改动且被列为禁改。计划须预先决策：本次不晋升 / 晋升到其他目标 / 先处置该历史债务（需用户决定）。

### 四端同步缺口

- **选择范围**：须覆盖 `origin/main..最终提交` 全部便携文件，含 `7829572` 新增的 `references/resume-context-amendments.md` 与 `references/cross-cli-portable-manifest.json` 变更；v2 计划要求未选文件已与运行时一致（`cross-cli-sync.md` Scoped plan 规则），新文件必然不满足会被 prestate 拦截。
- **顺序**：`verify-all` 在四端全部完成后执行一次，而非每端一次；同步前插入“Review plan and target snapshots”。
- **与 Git 的先后**：建议 本地 commit（需授权）→ 四端同步 → push，使运行时 parity 绑定具体提交哈希，避免 push 失败时运行时领先 Git。

### 守护进程 Python 版本漂移

- `scripts/autoloop_ctl.py:375` 守护进程固定 `/usr/bin/python3`（本机 3.9.6）；`tests/test_gov_runner_git_capture.py` 用 `sys.executable`（3.11）运行 gov_runner。F1 若写入 3.10+ 语法（`match`、运行期 `X | Y`、`itertools.pairwise` 等），单测全绿而守护进程崩溃。
- **修复**：Anchor 4 增加 `/usr/bin/python3 -m py_compile scripts/gov_runner.py scripts/check_commit_text.py`。

### 可选（不阻塞）

- `gov_runner.py:579` 的 `subprocess.run(..., timeout=...)` 抛 `TimeoutExpired` 未捕获，守护进程无 receipt、`collect_result` 只得 `BLOCKED` 无信息；launchd 环境问题常表现为挂起。若 F1 已在此处改动，可顺带归类 `failure_kind: "timeout"`；否则留作后续切片，避免扩范围。

---

## 5. 修订清单（Carbon 回填）

| 编号 | 类别 | 修订要求 | 采纳 / 不采纳 + 理由 |
|---|---|---|---|
| B1 | 审批 | 拆 Phase A（OpenSpec strict 后停）/ Phase B（凭 `迭代优化skill：已批准 <id>`） | **采纳**。见设计稿 §3.1、§3.4：拆为 Phase A（仅落盘四份 OpenSpec 工件并跑通 `--strict` 后停手）与 Phase B（收到显式 `迭代优化skill：已批准 fuse-harness-pstack-guardrails` 后实施），严格对齐 `references/self-evolution-rule.md:47-52`。 |
| B2 | Git | Step 5 改为独立显式授权点 | **采纳**。见设计稿 §3.1、§3.4 Step B9：`git add/commit` 与 `git push` 设为独立显式用户授权门禁，不从 `已批准 <id>` 推断，严格遵守 `SKILL.md:210-212` 与 `references/skill-iteration-loop.md:24-26`。 |
| B3 | 草稿 | 补 Exact Rule Snippets、Rollback、Forward-test | **采纳**。见设计稿新增 §3.3（逐文件新增/替换原文与锁定短语核对）、§3.5.B（隔离目录双场景 Forward-test）与 §3.6（四端事务/本机插件/仓库精确路径回滚）。 |
| B4 | F1.2 | `setup_or_env_error` 仅退出码 126/127 / `command not found` | **采纳**。见设计稿 §2.2 F1.2、§3.3(5)、§3.5.A.1：`setup_or_env_error` 仅凭退出码 `126/127` 或 Shell 级 `command not found` 判定，`ImportError`/`ModuleNotFoundError` 一律归为 `verification_failed`（另顺带捕获 `TimeoutExpired` 为 `timeout`/`124`）。 |
| B5 | F1.3 | 正计数豁免聚合判定；退出码 5 归类 | **采纳**。见设计稿 §2.2 F1.3、§3.3(5)、§3.5.A.2：全文存在 `Ran [1-9]\d* tests` / `Tests run: [1-9]\d*` / `[1-9]\d* passed` 正计数即豁免；`v_code == 5` 且命中零收集归类为 `empty_test_execution`；`evaluate_deterministic_vetoes(batch, snap_meta, raw)` 保持三参数签名从 `verify.exit` 读码。 |
| B6 | F3 | 复用 gov_runner 基线解析或基于快照判定 | **采纳**（采用基于快照单一真源方案）。见设计稿 §2.2 F3、§3.3(5)：直接在 `gov_runner.py` 生成 `git.changed_files.txt` 后执行高敏路径扫描与升档，零重复 Git 调用且与审查员所见范围 100% 一致。 |
| B7 | 闭环 | 补 Implementation Review → Closeout → final verification → final Review → 同步计划 Review → archive | **采纳**。见设计稿 §3.4 Step B4–B8：补齐 CCG-016 六要素独立 Implementation Review、Project Learning Closeout（含脏文件冲突预决策）、OpenSpec 归档与 strict 校验、Fresh Final Verification、同步计划快照审查与四端 `verify-all`、独立 Final Review；同时在 §0 第 2 条修正评审正文 §4（第 160 行）细节——依据 `scripts/validate_cross_cli_sync.py:6053-6054` 与 `references/cross-cli-portable-manifest.json:8-45`，`cross-cli-portable-manifest.json` 仅作 `--manifest` 入参，不可放入 `--select-file`（否则抛未声明异常）。 |
| S1 | F2/F3 | 改 hunt 文件第 1/5/10 行与 `autoloop_ctl.py:593`、fast prompt | **采纳**（附 §0 第 1 条局部反驳）。见设计稿 §3.2、§3.3(1)(4)：已将 `autoloop-review-hunt.md:1,5,10`、`autoloop_ctl.py:593` 及 `fast` 升档注入指令纳入；采纳 §3 删除 `log.error + rethrow` 风格项，但**反驳并入第 4 透镜**（依据 `references/autoloop-review-hunt.md:32` 第 4 透镜对所有纯内存 `if` 分支均激活，独立第 5 透镜仅在外部 I/O 或 `catch/except` 激活，其余 `hunt: n/a` 更防误伤）。 |
| S2 | F4 | approved-implementation-workflow 不引入 `NO_PROGRESS` | **采纳**（并采纳 §3 反膨胀整段删除建议）。见设计稿 §2.2 F4、§3.2：Phase B 完全不修改 `references/approved-implementation-workflow.md`，消除触碰 `tests/test_workflow_rules.py:2181-2197` 锁定短语及伪状态名风险。 |
| S3 | F4 | 驳回门槛限定为“已附可达触发路径的 finding” | **采纳**。见设计稿 §3.3(2)：在 `references/autoloop-req-acceptance.md:55` 限定仅对“已给出本次 Diff `path:line` 与具体可达触发路径”的同范围 `FAIL` 禁止以本地未复现跳过，不颠倒无依据意见的举证责任。 |
| S4 | F5 | 走 Candidate Pipeline；精简护栏 | **采纳**。见设计稿 §3.3(3)：在 `references/project-learning-closeout.md` 明确须先满足 `## Triggers` 阈值与 `learning-candidate-pipeline.md` 分类，且精简治理散文按 Major 门禁审批、严禁删除 `Non-Negotiables` 或 `validate_core_gates.py:2491-2510` 锁定短语。 |
| S5 | F3 | 路径段同义词集合；`HUNT_REF.parent` | **采纳**。见设计稿 §3.3(4)(5)：按路径段集合 `{"migration","migrations","changelog","auth","authn","authz","oauth","security","permission","permissions"}` 或 `.sql` 匹配（按路径段排除 `docs/doc/test/tests/__tests__/fixtures` 及根 `*.md`）；`--add-dir` 统一传目录 `HUNT_REF.parent`。 |
| S6 | F1.1 | 透传调用方 PATH | **采纳**。见设计稿 §2.2 F1.1、§3.3(4)：移除固定目录追加，由 `autoloop_ctl.py run` 仅捕获 `os.environ.get("PATH", "")` 写入本地批次 `verify_env_path`，`gov_runner.py` 子进程优先采用，彻底解决 `/usr/bin/python3` 遮蔽问题。 |
| S7 | F1.2 | 定义签名归一化 + 两条断言 | **采纳**。见设计稿 §3.3(5) `_compute_failure_signature` 与 §3.5.A.3：剥离时间戳、浮点耗时、十六进制地址与 `/tmp`/`/var/folders` 路径后哈希，并补充同失败不同耗时签名相等、不同失败签名不等两条断言。 |
| S8 | F1.2 | excerpt 脱敏 | **采纳**。见设计稿 §3.3(5) `_redact_sensitive_text` 与 §3.5.A.3：对 Token/Secret/Password/Authorization/API-Key 与 URL 内嵌账密脱敏后再写入 `report.md`、`receipt.json` 及终端输出。 |
| S9 | Step 3 | 显式 `--req` + `--cmd`；干净 worktree 重跑；py_compile 3.9 | **采纳**。见设计稿 §3.4 Step B3/B9 与 §3.5.C：增加 `/usr/bin/python3 -m py_compile` 3.9 门禁；自举显式传 `--req` + `--cmd` 并声明历史债务路径；未获 Git 授权前用 `git archive HEAD` + 允许文件覆盖的干净临时树跑全套测试，获批 commit 后再用 `git worktree add` 复核 `HEAD`。 |

**复审判据（`FOCUSED_RECHECK`）**：B1–B7 全部采纳或给出有规则依据的不采纳理由；修订稿新增的 Exact Rule Snippets 不删除 `validate_core_gates.py` 与 `tests/test_workflow_rules.py` 已锁定短语；设计稿状态仍为 `REVIEW_DRAFT`，期间不修改运行期规则、脚本或跨端副本。

---

## 6. FOCUSED_RECHECK（R2，对照设计稿 `draft-v2`）

- **Date**: 2026-11-18
- **Reviewer**: Claude Opus 5.5（Antigravity，只读独立会话，`same_instance=false`）
- **Scope**: 设计稿 `draft-v2` 全文（346 行）+ 本文 §5 回填；核对 `validate_cross_cli_sync.py` 子命令/参数、`cross-cli-portable-manifest.json`、`completion-contract.md:75-95`、`cross-cli-sync.md:72-77`；用 `/tmp` 临时 Python 片段实跑 §3.3(5) 的 3 个正则/函数。
- **未运行**：仓库单测、校验器、`openspec validate`。
- **工作区**：`git status --porcelain` 与 R1 前一致，仅新增两份 `docs/design/` 未跟踪文档；`SKILL.md`、`scripts/`、`references/`、`tests/`、`openspec/`、`distribution/` 无本轮改动。
- **Verdict**: **需小修（`FAIL`，4 项必修 R1–R4，均为局部片段修正）**。B1–B7 在设计层面已闭合；两处反驳均成立。R1–R4 修正后可直接进入 Phase A，无需再次全量复审；Phase A 产出的 OpenSpec 工件在 `已批准` 前仍需一次独立 Review。

### 6.1 原 B/S 闭合判定

| 编号 | 判定 | 备注 |
|---|---|---|
| B1 / B2 | 闭合 | §3.1、§3.4 Phase A 停手 + Step B9 独立 Git 授权 |
| B3 | 闭合 | §3.3 / §3.5.B / §3.6 齐备；R3、R4、R6 为片段内缺陷 |
| B4 | 闭合 | 126/127 + `command not found`；`ImportError` → `verification_failed` |
| B5 | 闭合 | 正计数豁免聚合判定；退出码 5 归类（见 R8 小缺口） |
| B6 | 闭合 | 改为基于 `git.changed_files.txt` 判定，与审查员快照同源 |
| B7 | **部分闭合** | 阶段已补齐，但归档时机与 Review 产品绑定有误（R3、R4） |
| S1–S6、S9 | 闭合 | — |
| S7 | **未闭合** | 归一化方案实测失效（R1） |
| S8 | **未闭合** | 脱敏正则实测漏网（R2） |

### 6.2 反驳裁定

1. **F2 保持独立第 5 透镜（反驳 §3）**：**成立**。`references/autoloop-review-hunt.md:32` 第 4 透镜的激活条件是 “Diff adds conditional branches, fallback paths, or bugfixes”，并入会让纯内存修复也被迫接受日志审查。撤回原建议。
2. **manifest 不进 `--select-file`（修正 §4）**：**成立**。实测 `references/cross-cli-portable-manifest.json` 未在自身 `files` 中声明（自引用计数 0），`workflow-overview.md` 同样未声明；`validate_cross_cli_sync.py:6053-6054` 对未声明选择器抛 `ValueError`，`plan` 子命令 `--manifest` 为必填（`:6598`）。§3.4 Step B7 的 7 个选择器与 `git diff --name-only origin/main..HEAD` 中已声明的便携文件一致。撤回原建议。

### 6.3 新发现（必修）

**R1【必修】`_compute_failure_signature` 对真实测试框架输出塌缩为同一签名**

- **证据**（实跑 §3.3(5) 原函数）：两个不同 unittest 失败（`test_a` 的 `AssertionError: 1 != 2` 与 `test_b` 的 `AssertionError: 'x' != 'y'`）均取到最后一行 `FAILED (failures=1)`，签名同为 `d11e1f4d7c70a8c4`。pytest 末行 `=== 1 failed in <dur> ===`、Maven 末行 `[ERROR] … BUILD FAILURE` 同理。
- **影响**：第 1 轮修好 `test_a`、第 2 轮暴露 `test_b` 时被误判“签名相同”而提前停止自动返修，`NO_PROGRESS` 早停误触发。方向安全（不会假 PASS），但让 F4 早停规则在常见场景下失效。§3.5.A.3 的 `python3 -c 'assert …'` 用例覆盖不到。
- **最小修复**：签名键改为“失败用例 ID 集合 + 首个错误行”：
  - 提取 `^(?:FAIL|ERROR): (\S+ \([^)]+\))`（unittest）、`^FAILED (\S+)`（pytest）、`^\[ERROR\]\s+(\S+\.\S+:\d+)|Tests in error`（surefire）；排序去重后拼接；
  - 无用例 ID 时，取首个（而非最后一个）含 `Error`/`Exception`/`command not found` 的行；
  - 补断言：两个不同 unittest 失败用例（均以 `FAILED (failures=1)` 结尾）签名必须不等。

**R2【必修】脱敏正则两处实测漏网**

- **证据**：
  - `postgres://admin:p@ss@127.0.0.1/db` → `postgres://admin:***@ss@127.0.0.1/db`，密码尾段 `ss` 泄露（`[^@\s/]+` 在第一个 `@` 截断）；
  - `{"Authorization": "Bearer sk-abc", "api_key":"k1"}` 完全未脱敏（键名后的引号阻断 `\s*[:=]`）。JSON 形态的错误体在 HTTP 客户端异常里很常见。
- **最小修复**：
  - URL：`(://[^/\s:@]+:)(\S+)(@[^@\s]*$|@(?=[^@\s]*(?:/|\s|$)))` 或改用贪婪 `([^\s/]+)@`，匹配到最后一个 `@`；
  - 键值：键名后允许可选引号，即 `\b(token|secret|password|passwd|authorization|api[_-]?key)\b["']?\s*[:=]\s*["']?(?:Bearer\s+)?`，值匹配 `[^\s"',}]+`；
  - §3.5.A.3 断言改为“原始密码/Token 的任一子串均不出现在 excerpt 中”（而非仅“含 `***`”），并补 JSON 形态用例。

**R3【必修】归档时机违反 Completion Contract**

- **依据**：`references/completion-contract.md:91-95` 原文为 “Archive only when repository semantics permit it … If deployment, release, or another required lifecycle remains outstanding, keep the change active and record its owner and resume condition.” 另 `validate_core_gates.py:2491-2497` 锁定顺序为 `… -> fresh final verification -> final Review -> OpenSpec reconcile/archive and strict validation`。
- **问题**：§3.4 Step B6 在四端同步（B7）、Final Review（B8）与需另行授权的 Git 提交/推送（B9）之前归档。若用户不授权 push 或同步失败，变更已被归档，但生命周期未完成。
- **最小修复**：顺序改为
  B4 Implementation Review → B5 Learning Closeout → fresh final verification → B7 四端同步 → B8 Final Review → **获 Git 授权后** commit → 干净 worktree 复核 → push → 归档 + `openspec validate --strict` → 归档 diff 的 focused Review/提交（同属 Git 授权范围）。未获 Git 授权时保持 change active，记录 `owner` 与 `resume condition`。

**R4【必修】Step B4/B8 审查者产品未唯一化**

- **依据**：CCG-016 要求 “one concrete reviewer product … unresolved ‘other agent’ destination … is fail-closed”。全局规则：`pi` 不可用，Review 统一走 `/Users/elvis/.gemini/antigravity-cli/bin/agy-readonly-review`。
- **问题**：Step B4 写 `agent_product: antigravity-cli 或 pi`；Step B8 未写产品。
- **最小修复**：B4/B8 均写死 `agent_product: antigravity-cli`（入口 `agy-readonly-review --effort high`，`--add-dir /private/tmp` + 净 Diff 绝对路径），并写明与执行实例不同的 `conversation_id`。若执行方本身也是 AGY，额外记录执行会话 ID 以证明 `same_instance=false`。

### 6.4 改进项（不阻塞，建议顺手处理）

| 编号 | 问题 | 建议 |
|---|---|---|
| R5 | `subprocess.run(shell=True, timeout=…)` 超时只杀 `/bin/sh`，`mvn`/`pytest` 等孙进程成为孤儿继续运行并写 `verify.stdout` | `Popen(..., start_new_session=True)` + 超时 `os.killpg(proc.pid, SIGKILL)`；单测断言超时后无残留子进程 |
| R6 | §2.2 F3 “在 fast Prompt 末尾追加 5 透镜条件猎杀指令” 未给出原文，违背 B3 的 exact snippet 要求 | 在 §3.3(5) 补追加文本原文（含 `hunt:` 输出要求与 FAIL 判定句） |
| R7 | 高敏判定只看完整路径段，`src/auth.py`、`AuthService.java`、`SecurityConfig.java` 不命中 | 对末段追加 `Path(seg).stem.lower()` 的前缀/全等判定（如 `auth`、`security`、`permission`）；误升档代价低 |
| R8 | pytest 全部被 `-k` 反选时输出 `N deselected`、退出码 5，但不含 `collected 0 items` / `no tests ran`，落入 `verification_failed` | `v_code == 5` 时额外匹配 `\b0 selected\b\|\bdeselected\b` |
| R9 | §3.6 回滚的 `git checkout HEAD -- <files>` 会丢弃改动，属破坏性操作 | 标注“执行前需用户显式授权”，并先把待丢弃内容备份到 `/tmp` |

### 6.5 下一步

1. Carbon 按 R1–R4 修正设计稿 §3.3(5)、§3.4、§3.5.A.3（R5–R9 可选）。
2. 无需再走全量 `FOCUSED_RECHECK`；修正后直接执行 Phase A（落盘 OpenSpec 工件并通过 `openspec validate fuse-harness-pstack-guardrails --strict`，然后停下）。
3. Phase A 工件在用户发出 `迭代优化skill：已批准 fuse-harness-pstack-guardrails` 前，需一次独立只读 Review，重点核对 R1–R4 已嵌入 `design.md`/`tasks.md`。

### 6.6 Carbon 修正回填与 Phase A 落盘记录

| 编号 | 级别 | 处置结果与落盘位置 |
|---|---|---|
| R1 | 必修 | **已采纳并经 `/usr/bin/python3` 3.9.6 实测验证**。提取排序去重后的失败用例 ID 集合（unittest/pytest/surefire）+ 跳过 `FAILED (` / `=== ... failed` / `BUILD FAILURE` 尾行后的首个错误行（禁用 Python 3.12 专有 f-string 反斜杠语法）；已写入设计稿 `draft-v3` §3.3(5)、§3.5.A.3 及 OpenSpec `design.md` / `tasks.md`。 |
| R2 | 必修 | **已采纳并经 `/usr/bin/python3` 3.9.6 实测验证**。URL 改用贪婪 `(://[^/\s:@]+:)([^\s/]+)(@[^@\s/]+)` 覆盖密码内含 `@`；键值正则兼容 JSON 引号 `["\']?\s*[:=]\s*["\']?`；单测升级为敏感子串零残留断言；已写入设计稿 `draft-v3` §3.3(5)、§3.5.A.3 及 OpenSpec `design.md` / `tasks.md`。 |
| R3 | 必修 | **已采纳**。严格对齐 `completion-contract.md:91-95` 与 `validate_core_gates.py:2491-2497`，将 OpenSpec 归档移至四端同步与 Final Review 之后且绑定显式 Git 授权；未获 Git 授权时保持 change `active` 并记录 `owner` 与 `resume_condition`；已写入设计稿 `draft-v3` §3.4 Step B6–B9 及 OpenSpec `tasks.md`。 |
| R4 | 必修 | **已采纳**。Step B4 与 Step B8 均唯一绑定 `agent_product: antigravity-cli`（入口 `agy-readonly-review`、`--model gemini-4-carbon-high`），同时记录执行会话 ID 与独立审查 `conversation_id` 证明 `same_instance=false`；已写入设计稿 `draft-v3` §3.4 及 OpenSpec `design.md` / `tasks.md`。 |
| R5–R9 | 建议 | **5 项全部顺手采纳**：R5（`Popen(..., start_new_session=True)` + 超时 `os.killpg` 杀进程组）、R6（补齐 `FAST_HUNT_ESCALATION_ADDENDUM` 原文）、R7（末段文件名 stem 匹配 `auth/security/permission/migration` 前缀）、R8（`v_code == 5` 额外匹配 `0 selected` / `\d+ deselected`）、R9（回滚命令标注须用户显式授权并先备份至 `/tmp`）；均已同步嵌入 `draft-v3` 与 OpenSpec 工件。 |
