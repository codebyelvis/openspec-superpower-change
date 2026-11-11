#!/usr/bin/env python3
"""Built-in governed agent-autoloop controller: auto-generate/match `docs/req/*.md` + `验收标准` and run closed-loop verification.

Author: elvis
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, time, uuid
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
RUNNER_SRC = SCRIPTS_DIR / "gov_runner.py"
AL_HOME = Path.home() / ".agent-autoloop"
RULES_FILE = AL_HOME / "rules.json"
PLUG_DIR = AL_HOME / "plugins" / "govpi"
STATE_ROOT = Path(os.environ.get("AUTOLOOP_STATE_ROOT") or (Path.home() / ".local/state/governed-cli-autoloop/runtime"))
BATCHES_DIR = STATE_ROOT / "batches"
LEDGER_DIR = STATE_ROOT / "ledger"
EVIDENCE_DIR = STATE_ROOT / "evidence"
BACKUPS_DIR = STATE_ROOT / "backups"
INDEX_FILE = STATE_ROOT / "project-index.json"
AI_APP_WORKBENCH_REQ_DIR = Path("/Users/elvis/file/develop/notes/Typora/10_Projects/ai-app-docs/模型开发工作台/docs/req")

NODE_BIN = "/Users/elvis/.nvm/versions/node/v24.22.2/bin/node"
AL_CMD = [NODE_BIN, "--disable-warning=ExperimentalWarning", str(AL_HOME / "app/bin/agent-autoloop.ts")]
PI_BIN = shutil.which("pi") or "/Users/elvis/.local/bin/pi"
PI_ANTIGRAVITY_EXT = Path.home() / ".pi/agent/npm/node_modules/pi-antigravity/src/index.ts"
LAUNCHD_LABEL = f"gui/{os.getuid()}/agent-autoloop"
SAFE_SLUG = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fff_-]+")
SAFE_CHANGE_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,127}$")

AGENT_TS_CODE = """// Author: elvis. Governed host-side adapter for agent-autoloop (change integrate-governed-cli-autoloop).
// Passes turn.contextFile so gov_runner.py resolves per-event isolated batch contracts (<batches_dir>/<subject>.json)
// without shared single-file overwrite; stays backward-compatible with static `c.batch` for mechanism fixtures.
import { readFileSync } from "node:fs";
import { join } from "node:path";

const install = () => JSON.parse(readFileSync(join(import.meta.dirname, "install.json"), "utf8"));

export default {
  command(turn) {
    const c = install();
    const batchArgs = c.batches_dir ? ["--batches-dir", c.batches_dir] : ["--batch", c.batch];
    return [
      c.python,
      c.runner,
      ...batchArgs,
      "--context-file",
      turn.contextFile ?? "",
      "--folder",
      turn.folder,
      "--session",
      turn.session,
      "--resume",
      turn.resume ?? "",
      "--cwd",
      turn.cwd,
    ];
  },
  read(stdout, code, stderr) {
    const lines = stdout.split("\\n").filter(Boolean);
    const metaLine = lines.findLast((l) => l.startsWith("META:"));
    const meta = metaLine ? JSON.parse(metaLine.slice(5)) : {};
    const text = lines.filter((l) => !l.startsWith("META:")).join("\\n");
    const base = { session: meta.session, started: Boolean(meta.started) };
    if (code === null) return { ...base, finished: Boolean(meta.finished) };
    if (code !== 0) return { ...base, error: stderr.trim() || "exit " + code };
    return { ...base, finished: true, text };
  },
  link: (s) => "gov://" + s,
};
"""


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def default_req_dir(cwd: Path) -> Path:
    parts = {p.lower() for p in cwd.resolve().parts}
    if "ai_app" in parts and AI_APP_WORKBENCH_REQ_DIR.parent.is_dir():
        return AI_APP_WORKBENCH_REQ_DIR
    return cwd.resolve() / "docs" / "req"


def parse_req_markdown(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    meta = {"status": "ready", "verify_cmd": "", "req_id": path.stem}
    body = text
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            fm = text[4:end]
            body = text[end + 5:]
            for line in fm.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    val = v.strip()
                    if len(val) >= 2 and val[0] == '"' and val[-1] == '"':
                        try:
                            val = json.loads(val)
                        except json.JSONDecodeError:
                            val = val[1:-1]
                    elif len(val) >= 2 and val[0] == "'" and val[-1] == "'":
                        val = val[1:-1].replace("''", "'")
                    meta[k.strip()] = val
    accept = ""
    m = re.search(r"^##\s*(?:验收标准|Acceptance Criteria)\s*$([\s\S]*?)(?=^##\s+|\Z)", body, re.M)
    if m:
        accept = m.group(1).strip()
    return {
        "req_path": str(path.resolve()),
        "req_id": meta.get("req_id") or path.stem,
        "status": meta.get("status") or "ready",
        "verify_cmd": meta.get("verify_cmd") or "",
        "accept": accept or "以需求文档正文与验证命令退出码 0 为准",
    }


def mark_req_passed(path: Path) -> None:
    if not path.is_file():
        return
    txt = path.read_text(encoding="utf-8")
    if txt.startswith("---\n"):
        end = txt.find("\n---\n", 4)
        if end != -1:
            fm = txt[4:end]
            if re.search(r"(?m)^status:\s*.*$", fm):
                fm = re.sub(r"(?m)^status:\s*.*$", "status: passed", fm)
            else:
                fm = fm.rstrip("\n") + "\nstatus: passed"
            path.write_text(f"---\n{fm}\n---\n{txt[end + 5:]}", encoding="utf-8")
            return
    path.write_text(f"---\nstatus: passed\n---\n\n{txt}", encoding="utf-8")


def load_index() -> dict:
    return json.loads(INDEX_FILE.read_text(encoding="utf-8")) if INDEX_FILE.is_file() else {}


def save_index(idx: dict) -> None:
    STATE_ROOT.mkdir(parents=True, exist_ok=True)
    tmp = INDEX_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(INDEX_FILE)


def cmd_init_req(args) -> int:
    cwd = Path(args.cwd).resolve()
    req_dir = Path(args.out_dir).resolve() if args.out_dir else default_req_dir(cwd)
    req_dir.mkdir(parents=True, exist_ok=True)
    slug = SAFE_SLUG.sub("-", args.slug.strip()).strip("-") or "task"
    date_prefix = time.strftime("%Y-%m-%d")
    req_id = slug if re.match(r"^\d{4}-\d{2}-\d{2}-", slug) else f"{date_prefix}-{slug}"
    req_path = req_dir / f"{req_id}.md"

    v_cmd = (args.cmd or "").strip()
    if not v_cmd:
        raise SystemExit("BLOCKED: --cmd verification command must not be empty")
    encoded_cmd = json.dumps(v_cmd, ensure_ascii=False)
    cmd_bullet = f"1. 命令验收：`{v_cmd}` 退出码为 `0`。\n"
    content = (
        f"---\nreq_id: {req_id}\nstatus: ready\nverify_cmd: {encoded_cmd}\n---\n\n"
        f"# {args.title.strip()}\n\n"
        f"## 需求与边界\n\n{args.summary.strip()}\n\n"
        f"## 验收标准\n\n{cmd_bullet}{args.accept.strip()}\n"
    )
    req_path.write_text(content, encoding="utf-8")

    idx = load_index()
    idx[str(cwd)] = {"active_req_path": str(req_path.resolve()), "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    save_index(idx)
    out = parse_req_markdown(req_path)
    out["created"] = True
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


def match_project_req(cwd: Path) -> dict:
    cwd = cwd.resolve()
    idx = load_index().get(str(cwd)) or {}
    pinned = idx.get("active_req_path")
    if pinned and Path(pinned).is_file():
        parsed = parse_req_markdown(Path(pinned))
        if parsed["status"] != "passed":
            return {"matched": True, "source": "project_index", **parsed}

    req_dir = default_req_dir(cwd)
    if req_dir.is_dir():
        candidates = sorted(req_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
        for cand in candidates:
            parsed = parse_req_markdown(cand)
            if parsed["status"] != "passed":
                return {"matched": True, "source": "docs_req_dir", **parsed}

    changes_dir = cwd / "openspec" / "changes"
    if changes_dir.is_dir():
        active_dirs = sorted(
            [
                d for d in changes_dir.iterdir()
                if d.is_dir() and d.name != "archive" and SAFE_CHANGE_ID.match(d.name) and (d / "proposal.md").is_file()
            ],
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        for ch_dir in active_dirs:
            tasks_p = ch_dir / "tasks.md"
            if tasks_p.is_file() and "- [ ]" not in tasks_p.read_text(encoding="utf-8"):
                continue
            return {
                "matched": True,
                "source": "openspec_change",
                "req_path": str((ch_dir / "proposal.md").resolve()),
                "req_id": ch_dir.name,
                "status": "ready",
                "verify_cmd": f"openspec validate {ch_dir.name} --strict",
                "verify_argv": ["openspec", "validate", ch_dir.name, "--strict"],
                "accept": f"满足 openspec/changes/{ch_dir.name}/ 下 proposal.md、design.md 与 tasks.md 的验收要求",
            }

    return {
        "matched": False,
        "cwd": str(cwd),
        "expected_req_dir": str(req_dir),
        "fallback": "DISTILL_FROM_CURRENT_SESSION",
        "next_action": (
            "No pending docs/req/*.md or active OpenSpec change found. Distill the requirement & acceptance "
            "criteria from the current session conversation, persist via `autoloop_ctl.py init-req`, then run."
        ),
    }


def worker_name() -> str:
    cfg = json.loads((AL_HOME / "config.json").read_text(encoding="utf-8"))
    w = cfg.get("worker")
    return w["name"] if isinstance(w, dict) else "elvisdemacbook-pro"


def ensure_installed() -> dict:
    for d in (BATCHES_DIR, LEDGER_DIR, EVIDENCE_DIR, BACKUPS_DIR):
        d.mkdir(parents=True, exist_ok=True)
    PLUG_DIR.mkdir(parents=True, exist_ok=True)

    changed = False
    agent_dst = PLUG_DIR / "agent.ts"
    if not agent_dst.is_file() or agent_dst.read_text(encoding="utf-8") != AGENT_TS_CODE:
        agent_dst.write_text(AGENT_TS_CODE, encoding="utf-8")
        changed = True

    runner_dst = PLUG_DIR / "gov_runner.py"
    if not runner_dst.is_file() or sha256_file(RUNNER_SRC) != sha256_file(runner_dst):
        shutil.copy2(RUNNER_SRC, runner_dst)
        runner_dst.chmod(0o755)
        changed = True

    install_cfg = json.dumps(
        {
            "python": "/usr/bin/python3",
            "runner": str(runner_dst),
            "batches_dir": str(BATCHES_DIR),
        },
        ensure_ascii=False,
        indent=2,
    ) + "\n"
    install_file = PLUG_DIR / "install.json"
    if not install_file.is_file() or install_file.read_text(encoding="utf-8") != install_cfg:
        install_file.write_text(install_cfg, encoding="utf-8")
        changed = True

    rules = json.loads(RULES_FILE.read_text(encoding="utf-8"))
    desired_agent = {
        "name": "受控验收与独立审查Pi",
        "worker": worker_name(),
        "use": "govpi",
        "access": "read",
        "timeout": 15,
    }
    desired_rule = {
        "name": "受控日常验收闭环",
        "when": {"source": "local", "types": ["gov.verify.*"]},
        "to": "gov-pi",
        "cwd": str(STATE_ROOT),
        "prompt": "受控日常验收批次；gov_runner.py 严格按 context.json subject 对应的隔离批次合同执行。",
    }
    rules_changed = False
    if rules.get("agents", {}).get("gov-pi") != desired_agent:
        rules.setdefault("agents", {})["gov-pi"] = desired_agent
        rules_changed = True
    existing_idx = next((i for i, r in enumerate(rules.get("rules", [])) if r.get("to") == "gov-pi"), None)
    if existing_idx is None:
        rules.setdefault("rules", []).append(desired_rule)
        rules_changed = True
    elif rules["rules"][existing_idx] != desired_rule:
        rules["rules"][existing_idx] = desired_rule
        rules_changed = True

    if rules_changed:
        ts = time.strftime("%Y%m%d-%H%M%S")
        shutil.copy2(RULES_FILE, BACKUPS_DIR / f"rules.json.{ts}.bak")
        tmp = RULES_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(rules, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tmp.replace(RULES_FILE)

    restarted = False
    if changed:
        subprocess.run(["launchctl", "kickstart", "-k", LAUNCHD_LABEL], check=True, capture_output=True)
        time.sleep(2.5)
        restarted = True
    elif rules_changed:
        time.sleep(1.5)

    return {"plugin_updated": changed, "rules_updated": rules_changed, "service_restarted": restarted}


def read_run_state(run_id: str) -> tuple[str | None, str | None]:
    p = subprocess.run(AL_CMD + ["why", str(run_id), "--json"], capture_output=True, text=True, timeout=30)
    if p.returncode != 0:
        return None, None
    state, summary = None, None
    for event in json.loads(p.stdout or "[]"):
        for ch in event.get("changes", []):
            if ch.get("table") == "runs" and str(ch.get("key")) == str(run_id):
                row = ch.get("row") or {}
                state = row.get("state") or state
                if "summary" in row and row["summary"] is not None:
                    summary = row["summary"]
    return state, summary


def build_pi_cmd(model_spec: str) -> list[str]:
    provider, rest = model_spec.split("/", 1) if "/" in model_spec else ("antigravity", model_spec)
    if ":" in rest:
        model, thinking = rest.rsplit(":", 1)
    else:
        model = rest
        thinking = "low" if "flash" in model.lower() else "medium"
    cmd = [
        PI_BIN, "-p", "--mode", "json", "--thinking", thinking,
        "--no-mcp", "--no-extensions", "--no-skills", "--no-context-files", "--no-prompt-templates",
        "--tools", "read,grep,find,ls",
    ]
    if provider == "antigravity" and PI_ANTIGRAVITY_EXT.is_file():
        cmd += ["-e", str(PI_ANTIGRAVITY_EXT)]
    cmd += ["--provider", provider, "--model", model]
    return cmd


def collect_result(batch_id: str) -> dict:
    ledger_file = LEDGER_DIR / f"{batch_id}.json"
    if not ledger_file.is_file():
        return {"batch_id": batch_id, "verdict": "PENDING", "reason": "Waiting for worker to claim batch"}
    ledger = json.loads(ledger_file.read_text(encoding="utf-8"))
    launches = ledger.get("launches") or []
    if not launches:
        return {"batch_id": batch_id, "verdict": "PENDING", "reason": "No launches recorded yet"}
    run_id = str(launches[0]["run"])
    state, summary = read_run_state(run_id)
    ev = EVIDENCE_DIR / f"run-{run_id}"
    receipt_file = ev / "receipt.json"
    abort_file = ev / "report-abort.md"
    if state == "queued" and (ev / "attempt-1/cli.exit").is_file():
        subprocess.run(AL_CMD + ["stop", run_id], capture_output=True, text=True, timeout=15)
        return {"batch_id": batch_id, "run_id": run_id, "state": "cancelled", "verdict": "BLOCKED", "summary": summary}
    if state not in ("done", "cancelled", "nothing", "failed"):
        return {"batch_id": batch_id, "run_id": run_id, "state": state or "running", "verdict": "RUNNING"}
    if abort_file.is_file():
        return {
            "batch_id": batch_id,
            "run_id": run_id,
            "state": state,
            "verdict": "BLOCKED",
            "summary": summary,
            "abort_report_path": str(abort_file),
        }
    if receipt_file.is_file():
        rc = json.loads(receipt_file.read_text(encoding="utf-8"))
        return {
            "batch_id": batch_id,
            "run_id": run_id,
            "state": state,
            "verdict": rc.get("verdict", "FAIL"),
            "verify_exit_code": rc.get("verify_exit_code"),
            "reviewer_readonly_verified": rc.get("reviewer_readonly_verified", True),
            "reviewer_session": rc.get("native_session"),
            "report_path": rc.get("report_path"),
            "report_sha256": rc.get("report_sha256"),
            "first_line": rc.get("first_line"),
        }
    return {"batch_id": batch_id, "run_id": run_id, "state": state, "verdict": "BLOCKED", "summary": summary}


def cmd_run(args) -> int:
    cwd = Path(args.cwd).resolve()
    if not cwd.is_dir():
        raise SystemExit(f"ERROR: --cwd directory not found: {cwd}")

    matched_source = "explicit_arg"
    if args.req:
        req_path = Path(args.req).expanduser()
        if not req_path.is_absolute():
            req_path = (cwd / req_path).resolve()
        if not req_path.is_file():
            raise SystemExit(f"ERROR: requirement markdown file not found: {req_path}")
        parsed = parse_req_markdown(req_path)
    else:
        matched = match_project_req(cwd)
        if not matched.get("matched"):
            print(json.dumps(matched, ensure_ascii=False, indent=2))
            return 2
        matched_source = matched["source"]
        req_path = Path(matched["req_path"])
        parsed = matched

    if args.cmd:
        verify_cmd: str | list[str] = args.cmd.strip()
    elif parsed.get("verify_argv"):
        verify_cmd = list(parsed["verify_argv"])
    else:
        verify_cmd = (parsed.get("verify_cmd") or "").strip()
    if not verify_cmd:
        raise SystemExit(f"BLOCKED: empty verify_cmd in {req_path} is forbidden; provide --cmd or set verify_cmd in frontmatter")
    accept_text = (args.accept if args.accept else parsed.get("accept", "")).strip() or "以需求文档内的验收标准与固定验证命令退出码 0 为准"

    setup = ensure_installed()
    batch_id = f"al-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"

    prompt = (
        f"你是独立只读验收与代码审查员（role=independent-reviewer，batch={batch_id}）。\n"
        "严禁尝试任何写操作；仅用 read/grep/find/ls 检查以下材料：\n"
        f"1. 需求文档：`{req_path}`\n"
        f"2. 验收标准：{accept_text}\n"
        "3. 固定验证命令执行结果：`{RAW}/verify.exit`、`{RAW}/verify.stdout`、`{RAW}/verify.stderr`\n"
        "4. 当前工作区变更快照（若存在）：`{RAW}/git.status.txt`、`{RAW}/git.diff.patch`（项目根目录 `{CWD}`）\n\n"
        "判定规则：\n"
        "- 仅当 `verify.exit` 为 `0`、需求与验收标准已满足、且代码无实质缺陷/无明显违背反膨胀四原则的阻塞问题时，首行严格输出 `AUTOLOOP_VERDICT: PASS`；否则首行严格输出 `AUTOLOOP_VERDICT: FAIL`。\n"
        "- 首行之后输出 Findings First（无阻塞问题写 `0 阻塞发现`；有阻塞问题逐条给出准确 `path:line`、原因与最小修复建议）以及 3 行内验证摘要。"
    )

    batch_payload = {
        "batch_id": batch_id,
        "change_id": parsed.get("req_id", batch_id),
        "mode": "pi-accept",
        "allow_rerun": False,
        "expected_resume": None,
        "verify_cwd": str(cwd),
        "verify_command": verify_cmd,
        "verify_timeout": args.timeout,
        "capture_git_diff": True,
        "canonical_sha256": sha256_file(req_path),
        "contract_revision": 1,
        "ledger_dir": str(LEDGER_DIR),
        "evidence_dir": str(EVIDENCE_DIR),
        "stop_cmd": AL_CMD + ["stop"],
        "pi_cmd": build_pi_cmd(args.model),
        "pi_prompt": prompt,
    }
    (BATCHES_DIR / f"{batch_id}.json").write_text(json.dumps(batch_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    emit = subprocess.run(
        AL_CMD + ["emit", "gov.verify.run", "--subject", batch_id, "--summary", f"{req_path.name}: {accept_text[:80]}"],
        capture_output=True, text=True, timeout=30,
    )
    if emit.returncode != 0:
        raise SystemExit(f"ERROR: agent-autoloop emit failed: {emit.stderr or emit.stdout}")

    if args.async_mode:
        print(json.dumps({"batch_id": batch_id, "matched_req": str(req_path), "matched_source": matched_source, "mode": "async", "verdict": "DISPATCHED", "setup": setup}, ensure_ascii=False, indent=2))
        return 0

    deadline = time.time() + args.timeout + 120
    last = {}
    while time.time() < deadline:
        last = collect_result(batch_id)
        if last.get("verdict") not in ("PENDING", "RUNNING"):
            break
        time.sleep(2.0)
    else:
        last = {"batch_id": batch_id, "verdict": "TIMEOUT", "detail": last}

    last["matched_req"] = str(req_path)
    last["matched_source"] = matched_source
    if last.get("verdict") == "PASS" and matched_source != "openspec_change":
        mark_req_passed(req_path)
    print(json.dumps(last, ensure_ascii=False, indent=2))
    return 0 if last.get("verdict") == "PASS" else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Built-in governed /autoloop controller")
    sub = ap.add_subparsers(dest="sub", required=True)

    sub.add_parser("ensure", help="Idempotently install/update govpi plugin and rules.json entry")

    p_init = sub.add_parser("init-req", help="Create standardized docs/req/YYYY-MM-DD-<slug>.md with acceptance criteria")
    p_init.add_argument("--cwd", default=os.getcwd(), help="Target project directory")
    p_init.add_argument("--out-dir", default="", help="Optional override directory for req markdown")
    p_init.add_argument("--slug", required=True, help="Short slug for requirement filename")
    p_init.add_argument("--title", required=True, help="Requirement title")
    p_init.add_argument("--summary", required=True, help="Requirement scope & boundaries")
    p_init.add_argument("--cmd", required=True, help="Deterministic verification shell command (non-empty)")
    p_init.add_argument("--accept", required=True, help="Acceptance criteria items")

    p_match = sub.add_parser("match", help="Auto-match pending docs/req/*.md or active OpenSpec change for --cwd")
    p_match.add_argument("--cwd", default=os.getcwd(), help="Target project directory")

    p_run = sub.add_parser("run", help="Run governed background verification + independent read-only review")
    p_run.add_argument("--cwd", default=os.getcwd(), help="Target project directory")
    p_run.add_argument("--req", default="", help="Optional requirement markdown path (auto-matched when omitted)")
    p_run.add_argument("--accept", default="", help="Optional acceptance override (read from matched req when omitted)")
    p_run.add_argument("--cmd", default="", help="Optional verification command override (read from matched req when omitted)")
    p_run.add_argument("--model", default="antigravity/gemini-4-carbon:medium", help="Reviewer provider/model[:thinking]")
    p_run.add_argument("--timeout", type=int, default=600, help="Max verification timeout seconds")
    p_run.add_argument("--async", dest="async_mode", action="store_true", help="Dispatch and return batch_id immediately")

    p_st = sub.add_parser("status", help="Check status/result of a batch_id")
    p_st.add_argument("batch_id")

    p_stop = sub.add_parser("stop", help="Stop an in-flight agent-autoloop run_id")
    p_stop.add_argument("run_id")

    args = ap.parse_args()
    if args.sub == "ensure":
        print(json.dumps(ensure_installed(), ensure_ascii=False, indent=2))
        return 0
    if args.sub == "init-req":
        return cmd_init_req(args)
    if args.sub == "match":
        print(json.dumps(match_project_req(Path(args.cwd)), ensure_ascii=False, indent=2))
        return 0
    if args.sub == "run":
        return cmd_run(args)
    if args.sub == "status":
        print(json.dumps(collect_result(args.batch_id), ensure_ascii=False, indent=2))
        return 0
    if args.sub == "stop":
        return subprocess.run(AL_CMD + ["stop", str(args.run_id)], text=True).returncode
    return 1


if __name__ == "__main__":
    sys.exit(main())
