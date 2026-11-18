# `openspec-superpower-change` 现状剖析与双标杆仓库（Engineering Harness + pstack）蒸馏融合实施计划

- **Author**: elvis
- **Date**: 2026-11-18
- **Revision**: `draft-v3`（已完成 `FOCUSED_RECHECK` R1–R9 全量收敛，并同步进入 **Phase A** 提案严格校验）
- **Status**: `PHASE_A_PROPOSED`（仅落盘 `openspec/changes/fuse-harness-pstack-guardrails/` 并通过 `--strict` 校验；等待 Phase A 独立审查与 `迭代优化skill：已批准 fuse-harness-pstack-guardrails` 后才进入 Phase B 实现）
- **Proposed OpenSpec Change ID**: `fuse-harness-pstack-guardrails`（Major Self-Evolution，Phase A 立项校验 + Phase B 获批实施）
- **Evaluated External Repositories**:
  1. `yezhwi/superpowers-engineering-harness`（`v0.3.2` candidate）
  2. `cursor/plugins` -> `pstack`（Lauren Tan / `@poteto`）

---

## 0. 独立评审（B1–B7 / S1–S9）与复审（R1–R9）闭环记录

本 `draft-v3` 已闭合初审（B1–B7、S1–S9）与复审 `FOCUSED_RECHECK`（R1–R9）：

- **初审两处反驳均获复审确认成立**（见评审稿 §6.2）：① F2 保持独立第 5 透镜 `diagnosability_context`（避免并入第 4 透镜误伤纯内存分支）；② `references/cross-cli-portable-manifest.json` 仅作 `--manifest` 入参，不放入 `--select-file`。
- **复审必修项 R1–R4（4/4 全部采纳并经 `/usr/bin/python3` 3.9.6 实测验证）**：
  1. **R1（失败签名防塌缩）**：`_compute_failure_signature` 改为提取排序去重后的失败用例 ID 集合（unittest `FAIL/ERROR:`、pytest `FAILED`、Maven Surefire `[ERROR]`）+ 跳过末尾汇总行（`FAILED (`、`=== ... failed`、`BUILD FAILURE`）后的**首个**具体错误行，实测不同失败用例签名严格不等、同一失败不同耗时签名恒等。
  2. **R2（URL 含 `@` 密码与 JSON 引号键值脱敏）**：`URL_CRED_REDACT_RE` 改用贪婪匹配至主机名前最后一个 `@`（`admin:p@ss@host` -> `admin:***@host`）；`SECRET_REDACT_RE` 兼容 JSON 双引号/单引号键值（`{"Authorization": "Bearer ..."}` -> `***`）；单测断言升级为“原始敏感子串零残留”。
  3. **R3（归档时机对齐 Completion Contract 与校验器锁定顺序）**：严格按 `completion-contract.md:91-95` 与 `validate_core_gates.py:2491-2497`，将 OpenSpec 归档移至四端同步与独立 Final Review 之后，并与用户显式 Git 授权绑定；未获 Git 授权前保持 change `active` 并记录 `owner` 与 `resume_condition`。
  4. **R4（独立审查员产品唯一化）**：Step B4 与 Step B8 均唯一绑定 `agent_product: antigravity-cli`（入口 `/Users/elvis/.gemini/antigravity-cli/bin/agy-readonly-review`、`--model gemini-4-carbon-high`），不再含糊写 `或 pi`，并同时记录执行会话 ID 与审查会话 `conversation_id` 证明 `same_instance=false`。
- **复审建议项 R5–R9（5/5 全部顺手采纳）**：
  - **R5**：`verify_command` 改用 `subprocess.Popen(..., start_new_session=True)`，超时后 `os.killpg(proc.pid, signal.SIGKILL)` 清理整棵子进程树，防 `mvn`/`pytest` 孤儿进程；
  - **R6**：在 §3.3(5) 补齐 `fast` 高敏升档追加到 Prompt 的完整原文 `FAST_HUNT_ESCALATION_ADDENDUM`；
  - **R7**：高敏路径除目录段匹配外，对末段文件名 stem（`Path(rel).stem.lower()`）增加 `("auth", "security", "permission", "migration")` 前缀匹配（覆盖 `src/auth.py`、`SecurityConfig.java` 等）；
  - **R8**：`v_code == 5` 时额外匹配 `\b0\s+selected\b|\b\d+\s+deselected\b`，覆盖 pytest `-k` 全反选场景；
  - **R9**：§3.6 回滚中的 `git checkout HEAD -- <files>` 明确标注须经用户显式授权，且执行前先备份待丢弃内容至 `/tmp`。

---

## 1. `openspec-superpower-change` 现状深度剖析

### 1.1 当前架构优势（已收敛成型的骨架）

当前体系坚持 **方案 C**（`openspec-superpower-change` + `OpenSpec` + `Superpowers` + `codex-brief-antigravity-review` + `/autoloop`）：
1. **窄触发与按行懒加载**（`SKILL.md:3-56`）：仅在显式请求门禁/路由/OpenSpec/`迭代优化skill`/归档蒸馏时加载。
2. **反仪式化执行减负**（`SKILL.md:176`、`references/approved-implementation-workflow.md:21-42, 261-277`）：四硬锚点合一、懒创建 `status.md`、单切片非 `strict` 合并报告。
3. **跨窗口与四端同步防篡改**（`references/handoff-contract.md`、`scripts/validate_core_gates.py`、`scripts/validate_cross_cli_sync.py`）：Schema-6 Handoff 与 Schema-2 证据清单保证四端一致。

### 1.2 本地第一阶段基线（`main` @ `7829572`）与既有脏文件隔离

本地 `main` 已 fast-forward 对齐 `origin/main`（`b8876b8`），并在 `7829572` 完成了去本机硬编码路径、OpenSpec 测试命令提取串联、`pi-accept` 审查角色对齐（`batch-review` / `independent-reviewer` / `control-plane-high`）及 `references/resume-context-amendments.md` 冷参考抽离（503 项单测全绿）。工作区中 6 组历史未暂存文件（`allow-one-external-grok-control-plane` 归档尾项等）作为 `OUT_OF_SCOPE_PREEXISTING_DEBT` 原样保护，严禁触碰。

### 1.3 待解决的 5 个工程短板

1. `launchd` 守护进程丢失调用端 `PATH` 顺序；`v_code != 0` 时未前置短路仍空耗数分钟只读审查（且超时孤儿进程未按进程组清理）；单测零执行伪通过缺少聚合识别。
2. `references/autoloop-review-hunt.md` 缺少外部 I/O 与异常黑盒/凭据泄露的独立条件透镜。
3. `fast` 模式修改 `db/migration`、`*.sql`、`auth*`、`SecurityConfig` 等高敏业务文件时缺少基于快照单一真源的自动升档。
4. `references/autoloop-req-acceptance.md` 缺少 `Attack the Premise` 与连续相同 `failure_signature` 停手约束。
5. `references/project-learning-closeout.md` 缺少受双信号门禁约束的四级机械加固阶梯与 Major 散文精简护栏。

---

## 2. 两大外部仓库蒸馏与融合取舍矩阵

### 2.1 明确拒绝项（Reject）

- **Harness**：拒绝 `.harness/*.yaml` 多文件状态机/`ESCALATED`/`Finding` 状态机（防第二状态系统与业务仓污染）；拒绝一刀切禁跑全量单测；拒绝 `.publication-retained/` 无 GC 存储引擎。
- **pstack**：拒绝 Cursor 专属组件（`bugbot`、`cursor-team-kit`）及日常默认多模型并发烧钱审查。

### 2.2 精准融合项（Adopt & Adapt — F1~F5）

1. **F1（验证执行硬化：`scripts/autoloop_ctl.py` + `scripts/gov_runner.py`）**：
   - **F1.1 调用端 `PATH` 透传**：`autoloop_ctl.py run` 仅捕获 `os.environ.get("PATH", "")` 写入 `verify_env_path`，`gov_runner.py` 子进程优先使用。
   - **F1.2 进程组超时清理、失败前置短路、严格退出码分类、全覆盖脱敏与防塌缩签名**：
     - `Popen(..., start_new_session=True)` 执行验证命令，超时 `os.killpg(proc.pid, signal.SIGKILL)` 并归类 `failure_kind = "timeout"`（`v_code = 124`）；
     - 凡 `v_code != 0` 直接短路生成报告与回执（`cli_launched = False`）；
     - `failure_kind` 四分法：`timeout` | `setup_or_env_error`（仅 `v_code in (126, 127)` 或 Shell `command not found`，`ImportError` 归入 `verification_failed`）| `empty_test_execution`（`v_code == 5` 且匹配 `collected 0 items` / `NO TESTS RAN` / `Ran 0 tests` / `0 selected` / `\d+ deselected`）| `verification_failed`；
     - 经贪婪 URL 账密与兼容 JSON 引号的 `_redact_sensitive_text()` 脱敏后写入 `verify_error_excerpt`；基于“失败用例 ID 集合 + 跳过汇总尾行后的首个错误行”生成防塌缩 `failure_signature`。
   - **F1.3 聚合正计数豁免的零测试假绿否决**：`v_code == 0` 时，全文无任何正计数（`Ran [1-9]\d* tests`、`Tests run: [1-9]\d*`、`[1-9]\d* passed`）且命中零执行信号才否决。
2. **F2（独立第 5 透镜 `diagnosability_context`：`references/autoloop-review-hunt.md`）**：更新第 1/5/10 行兼容升档 `fast`，新增 5 行紧凑透镜（仅外部 I/O 或 `catch`/`except` 激活，抓“吞根因异常/缺作用域内业务主键或错误码黑盒”与“日志打印明文凭据”）。
3. **F3（基于 `git.changed_files.txt` 同源高敏路径与文件名升档）**：排除文档/测试路径段及根 `*.md` 后，匹配高敏目录段或末段文件名 stem 前缀 `("auth", "security", "permission", "migration")` 或 `.sql`；命中时保持 `fast`（免 `--base-ref` 报错）、默认模型升 `-high`、挂载 `HUNT_REF.parent` 并追加 `FAST_HUNT_ESCALATION_ADDENDUM`。
4. **F4（返修收敛纪律：仅改 `references/autoloop-req-acceptance.md:55`，零改动 `approved-implementation-workflow.md`）**：纳入环境错误先修、相同 `failure_signature` 停手、二次修复前 `Attack the Premise`、以及已附 `path:line` 与可达触发路径的同范围 `FAIL` 不得以本地未复现跳过。
5. **F5（受门禁约束的四级加固阶梯：`references/project-learning-closeout.md`）**：绑定既有双信号/高危触发与 Candidate Pipeline，按“架构单真源/删死代码 → 指路式校验器 → 行为测试 → 散文规则”排序，且治理散文精简须经 Major 审批、严禁删 `Non-Negotiables` 或校验器锁定短语。

---

## 3. 四硬锚点与两段式实施计划

### 3.1 Anchor 1 & Anchor 2：精确文件范围与禁止范围

- **Phase A 允许新建**：`openspec/changes/fuse-harness-pstack-guardrails/{proposal.md,design.md,tasks.md,specs/skill-workflow-governance/spec.md}`
- **Phase B 允许新建/修改**：`scripts/{autoloop_ctl.py,gov_runner.py}`、`references/{autoloop-review-hunt.md,autoloop-req-acceptance.md,project-learning-closeout.md}`、`CHANGELOG.md`、`distribution/codex-plugin/**`（生成物）、`tests/{test_gov_runner_git_capture.py,test_workflow_rules.py}`，以及获 Git 授权收尾时的 OpenSpec 归档文件。
- **严格禁止触碰**：`SKILL.md`、`references/approved-implementation-workflow.md`、`scripts/validate_core_gates.py`、`scripts/validate_cross_cli_sync.py`，以及工作区全部 6 组历史未暂存/未跟踪文件。

### 3.3 Exact Rule & Code Snippets（逐文件精确原文 — 经 Python 3.9 实测）

#### (1) `references/autoloop-review-hunt.md`

第 1–10 行替换为：
```markdown
# Conditional Read-Only Hunt Reference (`pre-mr` & Risk-Escalated `fast`)

Author: elvis

Use this reference in `pre-mr` read-only reviews and in `fast` reviews escalated by high-risk business paths. Keep strict Scope Lock and Anti-Bloat discipline:

1. **Changed-Hunk Attribution Only**: Every `FAIL` finding MUST anchor to an exact `path:line` modified in `git.branch_diff.patch` or `git.working_diff.patch`, and prove a concrete failure path that did not exist on the target baseline before this change.
2. **Conditional Activation (`hunt: n/a`)**: Evaluate each lens below **only** when the diff actually touches that mechanism. When a lens does not apply to the diff, record `hunt: n/a` for that lens. Never fail a change for "missing defensive guards" without a real in-repo caller or reachable runtime trigger, never emit naming/formatting/style nitpicks, and never report untouched pre-existing issues on the target branch.

## Five Conditional Hunt Lenses
```

第 35 行末尾追加：
```markdown

5. **External & Exception Diagnosability (`diagnosability_context`)**
   - **Activate when**: Diff adds or alters external I/O calls (HTTP/RPC/DB/MQ/CLI) or `catch`/`except` error-handling blocks.
   - **Check**:
     - Error paths must not silently swallow root-cause exceptions or log external/state failures without an available in-scope business identifier or error status/code needed for production triage;
     - Logs and error payloads must never output raw credentials, tokens, secrets, or connection passwords.
```

#### (2) `references/autoloop-req-acceptance.md`（替换第 55 行）

```markdown
- On `"verdict": "FAIL"`, inspect `failure_kind`, `failure_signature`, and `report_path`: if `failure_kind == "setup_or_env_error"`, fix the command/PATH environment rather than mutating product code; stop immediately if two consecutive runs produce the identical `failure_signature`; before a second code-repair attempt, state in one sentence and directly check the shared premise assumed by the first failed fix (`Attack the Premise`). Never dismiss a same-scope `FAIL` finding that cites an exact diff `path:line` and concrete trigger path merely as "not reproduced locally" (at most 2 auto-repair rounds before stopping to report).
```

#### (3) `references/project-learning-closeout.md`（第 136 行后新增一段，原文本零删减）

```markdown

When an item already meets the mandatory `## Triggers` threshold above and passes `references/learning-candidate-pipeline.md` scope classification, prefer the highest feasible enforcement layer: (1) architectural single-source-of-truth or dead-code removal so agents cannot copy obsolete patterns, (2) static validators or types whose error message names the canonical replacement, (3) observable behavior regression tests, and (4) prose guidance last for judgment-only boundaries. Any condensation or retirement of governed skill/workflow prose remains subject to Major Self-Evolution approval and must never remove `Non-Negotiables` or validator-locked phrases.
```

#### (4) `scripts/autoloop_ctl.py` 精确新增/调整片段

```python
# cmd_run() line 593 pre-mr FAIL attribution rule:
"- 每个 `FAIL` 发现必须同时给出本次 Diff 内的准确 `path:line`，以及仓库内真实消费者或可达的重试/分页/崩溃重入/异常黑盒触发路径。"

# batch_payload additions:
"verify_env_path": os.environ.get("PATH", ""),
"model_explicit": bool((args.model or "").strip()),
"hunt_ref": str(HUNT_REF.resolve()),
"hunt_dir": str(HUNT_REF.parent.resolve()) if HUNT_REF.parent.is_dir() else "",

# collect_result() additions:
"cli_launched": rc.get("cli_launched", True),
"failure_kind": rc.get("failure_kind"),
"failure_signature": rc.get("failure_signature"),
"veto_errors": rc.get("veto_errors") or [],
"verify_error_excerpt": rc.get("verify_error_excerpt", ""),
"risk_escalated_paths": rc.get("risk_escalated_paths") or [],
```

#### (5) `scripts/gov_runner.py` 精确核心片段（含 R1/R2/R5/R6/R7/R8，Python 3.9 实测通过）

```python
POSITIVE_TEST_COUNT_RE = re.compile(
    r"(?:\bRan\s+[1-9]\d*\s+tests?\b|\bTests\s+run:\s*[1-9]\d*\b|\b[1-9]\d*\s+passed\b)"
)
ZERO_TEST_EXEC_RE = re.compile(
    r"(?:\bRan\s+0\s+tests?\s+in\b|\bcollected\s+0\s+items\b|\bTests\s+run:\s*0\s*,|"
    r"===\s*no\s+tests\s+ran\b|\bNO\s+TESTS\s+RAN\b|\bThere\s+are\s+no\s+tests\s+to\s+run\b)",
    re.I,
)
PYTEST_DESELECTED_EXIT5_RE = re.compile(r"(?:\b0\s+selected\b|\b\d+\s+deselected\b)", re.I)
SHELL_CMD_MISSING_RE = re.compile(
    r"(?:command\s+not\s+found|not\s+recognized\s+as\s+an\s+internal\s+or\s+external\s+command)",
    re.I,
)
SECRET_REDACT_RE = re.compile(
    r"(?i)(\b(?:token|secret|password|passwd|authorization|api[_-]?key)\b[\"\']?\s*[:=]\s*[\"\']?(?:Bearer\s+)?)([^\s\"\',;}]+)"
)
URL_CRED_REDACT_RE = re.compile(r"(://[^/\s:@]+:)([^\s/]+)(@[^@\s/]+)")
FAILED_ID_PATTERNS = (
    re.compile(r"^(?:FAIL|ERROR):\s+(\S+(?:\s+\([^)]+\))?)", re.M),
    re.compile(r"^FAILED\s+(\S+)", re.M),
    re.compile(r"^\[ERROR\]\s+([A-Za-z0-9_.$]+(?:#\S+|\(\S+\)|:\d+))", re.M),
)
SUMMARY_FOOTER_RE = re.compile(
    r"^(?:FAILED\s+\(|=+\s+.*failed|\[ERROR\]\s+BUILD\s+FAILURE\b)", re.I
)
HIGH_RISK_SEGMENTS = frozenset(
    {"migration", "migrations", "changelog", "auth", "authn", "authz", "oauth", "security", "permission", "permissions"}
)
HIGH_RISK_STEM_PREFIXES = ("auth", "security", "permission", "migration")
NON_BUSINESS_SEGMENTS = frozenset({"docs", "doc", "test", "tests", "__tests__", "fixtures"})

FAST_HUNT_ESCALATION_ADDENDUM = (
    "\n\n补充材料（高敏业务路径自动升档核查）：\n"
    "5. 条件猎杀清单：`{HUNT_REF}`\n"
    "升档附加规则：\n"
    "- 第 2 行起除 Findings First 外，必须附带 `hunt:` 适用性摘要；严格按条件猎杀清单核查本次变更触及的路径，未触及的类别记录 `hunt: n/a`，严禁因“未加无依据防御代码”、命名/格式偏好或目标分支未触碰旧问题判 `FAIL`。\n"
    "- 每个 `FAIL` 发现必须同时给出本次 Diff 内的准确 `path:line`，以及仓库内真实消费者或可达的重试/分页/崩溃重入/异常黑盒触发路径。"
)


def _redact_sensitive_text(text: str, limit: int = 1200) -> str:
    masked = URL_CRED_REDACT_RE.sub(r"\1***\3", text or "")
    masked = SECRET_REDACT_RE.sub(r"\1***", masked)
    return masked[-limit:] if len(masked) > limit else masked


def _compute_failure_signature(failure_kind: str, v_code: int, raw_output: str) -> str:
    failed_ids = sorted(
        {m.strip() for pat in FAILED_ID_PATTERNS for m in pat.findall(raw_output or "")}
    )
    key_line = ""
    for ln in (x.strip() for x in (raw_output or "").splitlines() if x.strip()):
        if SUMMARY_FOOTER_RE.match(ln):
            continue
        if any(tok in ln for tok in ("AssertionError", "Error", "Exception", "FAILED", "ERROR", "command not found", "exit")):
            key_line = ln
            break
    if not key_line and raw_output:
        non_footer = [
            x.strip()
            for x in raw_output.splitlines()
            if x.strip() and not SUMMARY_FOOTER_RE.match(x.strip())
        ]
        key_line = non_footer[0] if non_footer else ""
    norm = re.sub(r"\b\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?\b", "<ts>", key_line)
    norm = re.sub(r"\b\d+\.\d+s\b", "<dur>", norm)
    norm = re.sub(r"0x[0-9a-fA-F]+", "<addr>", norm)
    norm = re.sub(r"(?:/private)?/(?:tmp|var/folders)/\S+", "<tmp>", norm)
    joined_ids = ";".join(failed_ids)
    return hashlib.sha256(f"{failure_kind}|{v_code}|{joined_ids}|{norm}".encode("utf-8")).hexdigest()[:16]


def _detect_escalated_paths_from_changed_file(changed_txt: Path) -> list[str]:
    if not changed_txt.is_file():
        return []
    matched: list[str] = []
    for raw_line in changed_txt.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = raw_line.split("\t")
        rel = (parts[-1] if parts else "").strip()
        if not rel or ("/" not in rel and rel.lower().endswith(".md")):
            continue
        norm_rel = rel.replace("\\", "/")
        segs = [s.lower() for s in norm_rel.split("/") if s]
        if any(s in NON_BUSINESS_SEGMENTS for s in segs):
            continue
        stem = Path(norm_rel).stem.lower()
        if (
            norm_rel.lower().endswith(".sql")
            or any(s in HIGH_RISK_SEGMENTS for s in segs)
            or stem.startswith(HIGH_RISK_STEM_PREFIXES)
        ):
            matched.append(rel)
    return sorted(set(matched))


def _run_verify_command(v_cmd, work_cwd: str, timeout_sec: int, verify_env_path: str, v_out, v_err) -> tuple[int, bool]:
    env = dict(os.environ)
    if (verify_env_path or "").strip():
        env["PATH"] = verify_env_path.strip()
    proc = subprocess.Popen(
        v_cmd,
        shell=isinstance(v_cmd, str),
        cwd=work_cwd,
        env=env,
        stdout=v_out,
        stderr=v_err,
        text=True,
        start_new_session=True,
    )
    try:
        return proc.wait(timeout=timeout_sec), False
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.wait()
        return 124, True
```

### 3.4 Anchor 3：两段式受控执行序列（Phase A / Phase B — 含 R3, R4 修正）

#### Phase A：OpenSpec 立项与严格校验（当前阶段）
1. 创建 `openspec/changes/fuse-harness-pstack-guardrails/{proposal.md,design.md,tasks.md,specs/skill-workflow-governance/spec.md}`（完整内嵌 R1–R9 精确规则与代码锚点）。
2. 执行 `openspec validate fuse-harness-pstack-guardrails --strict` 确认零错误通过。
3. **停手等待独立审查与用户具体批准**：对 Phase A 产出进行一次独立只读审查，等待用户显式发送 `迭代优化skill：已批准 fuse-harness-pstack-guardrails`。

#### Phase B：获批实施与严格收尾顺序（严格对齐 `completion-contract.md:91-95` 与 `validate_core_gates.py:2491-2497`）
1. **Step B1（结构化临时备份）**：确认/刷新 `/tmp/osc-self-evo-backup-<ts>` 四端临时备份。
2. **Step B2（RED -> GREEN 实现与分发物重生成）**：先写 RED 单测验证失败，再完成 F1–F5 实现、更新 `CHANGELOG.md`，并运行 `python3 scripts/build_codex_plugin.py .`。
3. **Step B3（Python 3.9 语法门禁 + 干净快照树全量验证 + 隔离 Forward-Test）**：
   - 执行 `/usr/bin/python3 -m py_compile scripts/gov_runner.py scripts/autoloop_ctl.py scripts/check_commit_text.py`；
   - 通过 `git archive HEAD` + 覆盖拷入本次允许改动文件构造 `/tmp/osc-clean-verify-<ts>` 干净树，运行全套 `quick_validate.py`、`validate_core_gates.py`、`validate_distribution.py` 与 `unittest discover -s tests -v`；
   - 执行 §3.5.B 隔离 Forward-Test 及显式 `--req openspec/changes/fuse-harness-pstack-guardrails/proposal.md --cmd "<全量校验命令>"` 自举演练。
4. **Step B4（独立 Implementation Review — 唯一产品绑定 R4）**：
   - 唯一绑定 `agent_product: antigravity-cli`（调用 `/Users/elvis/.gemini/antigravity-cli/bin/agy-readonly-review --model gemini-4-carbon-high --output-format stream-json --disable-slash-commands --add-dir /private/tmp`），`agent_role: independent-reviewer`，`capability_profile: control-plane-high`，`independence: distinct-contract-instance`（同时记录当前执行会话 ID 与审查子进程返回的独立 `conversation_id` 证明 `same_instance=false`），`result_authority: governed-review-evidence`。取得 `PASS` 后方可推进。
5. **Step B5（Project Learning Closeout 审计）**：
   - 读取 `docs/engineering-invariants.md` 与 `references/project-learning-closeout.md`；确认本次经验均已由代码/单测/目标参考文件机械化承载后记录无需额外散文晋升（严禁触碰未暂存的 `docs/engineering-invariants.md`；若确需写入该文件则转 `BLOCKED` 交用户先处置脏文件）。
6. **Step B6（Fresh Final Verification）**：
   - 在干净快照树重新执行完整门禁与单测套件，落盘最新验证证据。
7. **Step B7（四端跨 CLI 同步计划快照审查与原子同步）**：
   - 运行 `scripts/validate_cross_cli_sync.py plan`（`--manifest references/cross-cli-portable-manifest.json` + 7 个已声明变更便携文件的 `--select-file`）；
   - 执行 `verify-prestate --target all` 并审查计划与目标快照；按 `codex -> pi -> antigravity-cli -> grok-cli` 逐端 `apply -> verify -> verify-discovery -> commit-target`，全部完成后执行一次 `verify-all`。
8. **Step B8（独立 Final Review — 唯一产品绑定 R4）**：
   - 再次调用独立 `agy-readonly-review`（`agent_product: antigravity-cli`，`agent_role: independent-reviewer`，`capability_profile: control-plane-high`，全新独立 `conversation_id` 满足 `same_instance=false`）覆盖完整源码 Diff、Fresh Final Verification 与四端 `verify-all` 回执，取得 `PASS`。
9. **Step B9（独立 Git 授权门禁与 OpenSpec 归档收口 — R3）**：
   - **未获显式 Git 授权时**：按 `completion-contract.md:93-95` **保持 `fuse-harness-pstack-guardrails` 处于 active**（勾选已完成实现任务，保留归档/发布待办并记录 `owner: user`、`resume_condition: explicit git commit and push authorization`），停手汇报。
   - **获显式 Git 授权后**：执行精确路径 `git add` -> `check_commit_text.py` -> `git commit` -> `git worktree add` 干净复核 -> 对账归档 `fuse-harness-pstack-guardrails` 并更新 `openspec/specs/skill-workflow-governance/spec.md` -> 归档后 `openspec validate --strict` 与归档 Diff 聚焦复核/提交 -> `git push origin main` -> 清理临时备份。

### 3.5 Anchor 4 & Forward-Test Plan（含 R1, R2, R5, R7, R8 补充断言）

#### A. 确定性单测矩阵（`tests/test_gov_runner_git_capture.py` & `tests/test_workflow_rules.py`）
1. **退出码分类、进程组超时清理与前置短路（B4 + R5）**：
   - `nonexistent_cli_bin_xyz_99`（exit `127`）$\rightarrow$ `cli_launched is False`，`failure_kind == "setup_or_env_error"`；
   - `ModuleNotFoundError`（exit `1`）$\rightarrow$ `failure_kind == "verification_failed"`；
   - Shell 派生后台孙进程 `sh -c 'python3 -c "import time; time.sleep(30)"'` 超时（`verify_timeout=1`）$\rightarrow$ `v_code == 124`，`failure_kind == "timeout"`，且超时返回后孙进程已被 `killpg` 彻底终止无残留。
2. **多模块正计数豁免与 pytest 反选退出码 `5` 归类（B5 + R8）**：
   - 单模块 `Ran 0 tests in 0.000s`（exit `0`）$\rightarrow$ `empty_test_execution` 否决；
   - 多模块 `Tests run: 0` + `Tests run: 4`（exit `0`）$\rightarrow$ 正计数豁免通过；
   - pytest `collected 0 items` 或 `5 deselected`（exit `5`）$\rightarrow$ `failure_kind == "empty_test_execution"`。
3. **防塌缩签名与敏感子串零残留脱敏（R1 + R2）**：
   - 两个不同 unittest 用例失败（`FAIL: test_a ... AssertionError: 1 != 2 ... FAILED (failures=1)` vs `FAIL: test_b ... AssertionError: x != y ... FAILED (failures=1)`）$\rightarrow$ **`failure_signature` 严格不等**；同一 `test_a` 在不同耗时与 `/tmp` 路径下签名严格相等；
   - 输入同时含 `postgres://admin:p@ss@127.0.0.1:5432/db` 与 JSON `{"Authorization": "Bearer sk-abc123", "api_key":"k1_sec"}` $\rightarrow$ 断言 `p@ss`、`ss@`、`sk-abc`、`k1_sec` 任一敏感子串在 `report.md` 与 `receipt.json` 中均不出现（`assertNotIn`）。
4. **快照同源高敏目录段与文件名 stem 升档（B6 + S5 + R6 + R7） + `PATH` 透传（S6）**：
   - 已提交 `db/migration/V1__init.sql`、`src/auth.py` 或 `src/SecurityConfig.java`（工作区干净、无 `--base-ref`）$\rightarrow$ 均命中 `risk_escalated_paths`，自动升 `-high`、挂载 `HUNT_REF.parent` 并注入 `FAST_HUNT_ESCALATION_ADDENDUM`；仅改 `docs/note.md` 或 `src/test/resources/seed.sql` 不升档。

#### B. 隔离 Forward-Test 演练计划
在 `/tmp/osc-forward-test-<ts>` 隔离临时仓库执行 2 个端到端演练：① 零执行假绿前置拦截；② 已提交 `db/migration/V2__add_idx.sql` 在零参数 `fast` 模式下自动升档 `-high` + 激活 5 透镜清单。

### 3.6 Rollback Plan（含 R9 授权护栏）

1. **四端运行时回滚**：使用 `validate_cross_cli_sync.py restore-target` 或从 `/tmp/osc-self-evo-backup-<ts>` 恢复对应目录并重跑双校验器。
2. **本机 `agent-autoloop` 插件回滚**：从备份恢复 `scripts/gov_runner.py` 后执行 `python3 scripts/autoloop_ctl.py ensure`。
3. **开源仓库回滚（须显式用户授权 — R9）**：严禁使用 `git reset` 或 `git clean`；如需丢弃本次允许范围内的已跟踪文件未提交改动，**必须先获得用户显式授权**（`SKILL.md:210`），先将待回滚文件完整备份至 `/tmp/osc-rollback-stash-<ts>/`，再仅对允许文件列表执行精确恢复并移除新建的 `openspec/changes/fuse-harness-pstack-guardrails/`。
