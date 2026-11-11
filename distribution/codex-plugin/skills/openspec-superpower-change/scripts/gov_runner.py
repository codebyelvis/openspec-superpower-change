#!/usr/bin/env python3
# Author: elvis. Governed host-side runner for agent-autoloop (openspec-superpower-change).
# Enforces:
#   1. Per-event batch isolation via AGENT_AUTOLOOP_CONTEXT `events[-1].subject` -> `<batches_dir>/<subject>.json`
#      (backward-compatible with `--batch <file>`).
#   2. Persistent attempt/session ledger checked before any CLI launch:
#      a) second turn in same run-attempt (worker triedFresh) or resume mismatch (settleSession) -> report-abort.md, exit 0;
#      b) attempt >= 2 when batch forbids re-run (kernel retryLater) -> report-abort.md, `agent-autoloop stop <run>`, exit 0.
#   3. File-backed stderr redirection and pre/post read-only Pi workspace fingerprint verification.
import argparse, fcntl, hashlib, json, os, re, signal, subprocess, sys, time
from pathlib import Path

ABORT_RESUME = "执行中止：会话续接被拦截，已生成中止报告，禁止重跑"
ABORT_RERUN = "执行中止：重派被拦截，已调用 stop 并生成中止报告，禁止重跑"
SAFE_BATCH_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def meta(**fields):
    print("META:" + json.dumps(fields, ensure_ascii=False), flush=True)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def resolve_batch_file(a) -> Path:
    if a.batch:
        return Path(a.batch)
    ctx_path = Path(a.context_file or os.environ.get("AGENT_AUTOLOOP_CONTEXT", ""))
    if not ctx_path.is_file():
        raise SystemExit(f"BLOCKED: context.json missing at {ctx_path}")
    ctx = json.loads(ctx_path.read_text(encoding="utf-8"))
    events = ctx.get("events") or []
    subject = (events[-1].get("subject") if events else "") or ""
    if not SAFE_BATCH_ID.match(subject):
        raise SystemExit(f"BLOCKED: invalid or empty batch subject {subject!r} in context.json")
    batch_file = (Path(a.batches_dir) / f"{subject}.json").resolve()
    if batch_file.parent != Path(a.batches_dir).resolve() or not batch_file.is_file():
        raise SystemExit(f"BLOCKED: batch contract missing at {batch_file}")
    return batch_file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", default="")
    ap.add_argument("--batches-dir", default="")
    ap.add_argument("--context-file", default="")
    for name in ("folder", "session", "resume", "cwd"):
        ap.add_argument("--" + name, required=True)
    a = ap.parse_args()
    if not a.batch and not a.batches_dir:
        raise SystemExit("BLOCKED: either --batch or --batches-dir is required")

    batch = json.loads(resolve_batch_file(a).read_text(encoding="utf-8"))
    run = os.environ["AGENT_AUTOLOOP_RUN"]
    folder_run, attempt = Path(a.folder).name.rsplit("-", 1)
    if folder_run != run:
        raise SystemExit(f"BLOCKED: folder {a.folder} does not belong to run {run}")
    attempt = int(attempt)
    resume = a.resume or None
    ev = Path(batch["evidence_dir"]) / f"run-{run}"
    ev.mkdir(parents=True, exist_ok=True)
    ledger_dir = Path(batch["ledger_dir"])
    ledger_dir.mkdir(parents=True, exist_ok=True)
    ledger_file = ledger_dir / f"{batch['batch_id']}.json"
    with open(ledger_dir / ".lock", "a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        ledger = json.loads(ledger_file.read_text()) if ledger_file.exists() else {"batch_id": batch["batch_id"], "launches": []}
        same_attempt = [x for x in ledger["launches"] if x["run"] == run and x["attempt"] == attempt]
        action, reason = "launch", None
        if attempt >= 2 and not batch.get("allow_rerun", False):
            action, reason = "stop", f"attempt {attempt} is a kernel re-dispatch; batch forbids re-run"
        elif same_attempt:
            action, reason = "abort", "second turn in the same run-attempt (worker triedFresh); prior session not reused"
        elif resume != batch.get("expected_resume"):
            action, reason = "abort", f"resume {resume!r} != contract expected_resume {batch.get('expected_resume')!r}"
        record = {"run": run, "attempt": attempt, "turn": len(same_attempt) + 1, "folder": a.folder,
                  "session_arg": a.session, "resume_arg": resume, "pid": os.getpid(),
                  "at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "action": action, "reason": reason}
        ledger["launches"].append(record)
        tmp = ledger_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
        tmp.replace(ledger_file)
    if action != "launch":
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        with open(ev / "report-abort.md", "a") as f:
            f.write(f"# 执行中止报告\n\n- batch: `{batch['batch_id']}`\n- run/attempt/turn: {run}/{attempt}/{record['turn']}\n"
                    f"- action: `{action}`\n- reason: {reason}\n- resume_arg: `{resume}`\n- CLI launched: no\n"
                    f"- 治理结论: BLOCKED（禁止重跑，不转 FIX）\n")
            f.flush()
        meta(session=a.session, started=True, finished=True)
        print(ABORT_RERUN if action == "stop" else ABORT_RESUME, flush=True)
        if action == "stop":
            p = subprocess.run(batch["stop_cmd"] + [run], capture_output=True, text=True, timeout=30)
            stop = {"cmd": batch["stop_cmd"] + [run], "exit": p.returncode, "stdout": p.stdout, "stderr": p.stderr}
            with open(ev / "report-abort.md", "a") as f:
                f.write(f"- stop: `{json.dumps(stop, ensure_ascii=False)}`\n\n")
                f.flush()
        return 0
    return launch(batch, a, run, attempt, resume, ev)


def git_fingerprint(cwd: str) -> str:
    if subprocess.run(["git", "-C", cwd, "rev-parse", "--is-inside-work-tree"], capture_output=True).returncode != 0:
        return "non-git"
    st = subprocess.run(["git", "-C", cwd, "status", "--porcelain"], capture_output=True, text=True).stdout
    df = subprocess.run(["git", "-C", cwd, "diff", "HEAD"], capture_output=True, text=True).stdout
    return hashlib.sha256((st + "\0" + df).encode("utf-8")).hexdigest()


def launch(batch, a, run, attempt, resume, ev):
    raw = ev / f"attempt-{attempt}"
    raw.mkdir(exist_ok=True)
    v_code = 0
    work_cwd = batch.get("verify_cwd") or a.cwd
    if batch["mode"] == "stub":
        cmd = batch["cli_cmd"] + [batch["stub_mode"], resume or "NULL_RESUME"]
        fp_before_pi = "stub"
    else:
        v_cmd = batch.get("verify_command")
        if v_cmd:
            with open(raw / "verify.stdout", "w") as v_out, open(raw / "verify.stderr", "w") as v_err:
                use_shell = isinstance(v_cmd, str)
                v = subprocess.run(v_cmd, shell=use_shell, cwd=work_cwd, stdout=v_out, stderr=v_err, text=True,
                                   timeout=int(batch.get("verify_timeout", 600)))
                v_code = v.returncode
        else:
            (raw / "verify.stdout").write_text("(no verify_command specified)\n")
            (raw / "verify.stderr").write_text("")
        (raw / "verify.exit").write_text(f"{v_code}\n")

        if batch.get("capture_git_diff") and subprocess.run(
            ["git", "-C", work_cwd, "rev-parse", "--is-inside-work-tree"], capture_output=True
        ).returncode == 0:
            st = subprocess.run(["git", "-C", work_cwd, "status", "-sb"], capture_output=True, text=True)
            df = subprocess.run(["git", "-C", work_cwd, "diff", "HEAD"], capture_output=True, text=True)
            (raw / "git.status.txt").write_text(st.stdout)
            (raw / "git.diff.patch").write_text(df.stdout[:200_000])

        fp_before_pi = git_fingerprint(work_cwd)
        prompt = batch["pi_prompt"].replace("{RAW}", str(raw)).replace("{CWD}", str(work_cwd))
        cmd = batch["pi_cmd"] + ["--session-dir", str(raw / "pi-sessions")] + \
            (["--session", resume] if resume else []) + [prompt]

    (raw / "cli.argv.json").write_text(json.dumps(cmd, ensure_ascii=False, indent=2) + "\n")
    session, started, lines = None, False, []
    with open(raw / "cli.stdout", "w") as out, open(raw / "cli.stderr", "w") as err_f:
        proc = subprocess.Popen(cmd, cwd=work_cwd, stdout=subprocess.PIPE, stderr=err_f, text=True)
        for line in proc.stdout:
            out.write(line)
            out.flush()
            lines.append(line.rstrip("\n"))
            if batch["mode"] == "stub":
                if line.startswith("SESSION:"):
                    session = line.split(":", 1)[1].strip()
                hit = line.startswith("STARTED")
            else:
                event = json.loads(line) if line.startswith("{") else {}
                if event.get("type") == "session":
                    session = event.get("id")
                hit = event.get("type") == "session"
            if hit and not started:
                started = True
                meta(session=session or a.session, started=True)
        code = proc.wait()

    err = (raw / "cli.stderr").read_text(errors="replace")
    (raw / "cli.exit").write_text(f"{code}\n")
    if code != 0:
        if started and not batch.get("allow_rerun", False):
            with open(ev / "report-abort.md", "a") as f:
                f.write(f"# 执行中止报告\n\n- cli exit {code}: `{err.strip()[:500]}`\n- 治理结论: BLOCKED（禁止重跑）\n\n")
            meta(session=session or a.session, started=True, finished=True)
            print("执行中止：CLI 异常退出，已生成中止报告，禁止重跑", flush=True)
            return 0
        meta(session=session or a.session, started=started)
        sys.stderr.write(err or f"cli exit {code}")
        return code
    if batch["mode"] == "stub":
        text = "\n".join(l for l in lines if not l.startswith(("STARTED", "SESSION:")))
    else:
        events = [json.loads(l) for l in lines if l.startswith("{")]
        finals = [e["message"] for e in events if e.get("type") == "message_end" and e.get("message", {}).get("role") == "assistant"]
        last = finals[-1] if finals else {}
        if last.get("stopReason") != "stop":
            err_msg = last.get("errorMessage") or f"stopReason={last.get('stopReason')!r}"
            if not batch.get("allow_rerun", False):
                with open(ev / "report-abort.md", "a") as f:
                    f.write(f"# 执行中止报告\n\n- assistant error: `{err_msg}`\n- 治理结论: BLOCKED（禁止重跑）\n\n")
                meta(session=session or a.session, started=True, finished=True)
                print(f"执行中止：模型未正常完成（{err_msg[:120]}），禁止重跑", flush=True)
                return 0
            meta(session=session, started=started)
            sys.stderr.write(f"BLOCKED: assistant stopReason != stop ({err_msg})")
            return 4
        text = "".join(c.get("text", "") for c in last.get("content", []) if c.get("type") == "text").strip()
    expected = batch.get("expected_resume")
    if expected and session != expected:
        with open(ev / "report-abort.md", "a") as f:
            f.write(f"# 执行中止报告\n\n- post-output session {session!r} != expected {expected!r}\n- 治理结论: BLOCKED\n\n")
        meta(session=session, started=True, finished=True)
        print("执行中止：结果后会话身份不符，已生成中止报告，禁止重跑", flush=True)
        return 0

    fp_after_pi = "stub" if batch["mode"] == "stub" else git_fingerprint(work_cwd)
    readonly_ok = (fp_before_pi == fp_after_pi)
    if not readonly_ok:
        with open(ev / "report-abort.md", "a") as f:
            f.write("# 执行中止报告\n\n- reason: Workspace mutated during read-only Pi review\n- 治理结论: BLOCKED\n\n")
        meta(session=session, started=True, finished=True)
        print("执行中止：只读审查期间工作区发生变化，结果作废", flush=True)
        return 0

    first_line = text.splitlines()[0] if text else "空"
    passed = (v_code == 0) and ("AUTOLOOP_VERDICT: PASS" in first_line or "VERIFY: PASS" in first_line)
    ev_result = "pass" if passed else "fail"
    if batch["mode"] in ("pi-verify", "pi-accept"):
        c_sha = batch.get("canonical_sha256", "0" * 64)
        c_rev = batch.get("contract_revision", 1)
        manifest = (
            "<!-- COOP_EVIDENCE_MANIFEST_START -->\n```yaml\n"
            f"evidence_schema_version: 2\nevidence_role: attempt-report\nevidence_result: {ev_result}\n"
            f"change_id: {batch.get('change_id', batch['batch_id'])}\n"
            f"current_batch: {batch.get('current_batch', 1)}\nattempt: {attempt}\n"
            f"contract_revision: {c_rev}\ncanonical_sha256: {c_sha}\n"
            f"agent_product: pi\nagent_instance_id: {session}\n"
            f"agent_role: executor\ncapability_profile: implementation-high\n```\n"
            "<!-- COOP_EVIDENCE_MANIFEST_END -->\n\n"
        )
        (ev / "report.md").write_text(manifest + text + "\n")
    else:
        (ev / "report.md").write_text(text + "\n")

    receipt = {
        "evidence_schema_version": 2,
        "batch_id": batch["batch_id"],
        "verdict": "PASS" if passed else "FAIL",
        "run": run,
        "attempt": attempt,
        "native_session": session,
        "verify_exit_code": v_code,
        "reviewer_readonly_verified": readonly_ok,
        "first_line": first_line,
        "report_path": str(ev / "report.md"),
        "report_sha256": sha(ev / "report.md"),
        "raw_sha256": {p.name: sha(p) for p in sorted(raw.glob("*")) if p.is_file()},
    }
    (ev / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    meta(session=session, started=True, finished=True)
    print("报告已交付：治理结论见 report.md（" + first_line + "）", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
