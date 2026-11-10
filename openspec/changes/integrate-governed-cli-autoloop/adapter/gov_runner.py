#!/usr/bin/env python3
# Author: elvis. Governed host-side runner for agent-autoloop (change integrate-governed-cli-autoloop).
# Persistent attempt/session ledger checked before any CLI launch:
#   a) a second turn in the same run-attempt (worker triedFresh) or a resume that differs from the batch contract
#      (scheduler/settleSession cleared or replaced it) -> report-abort.md, exit 0, abort receipt; CLI not launched.
#   b) attempt >= 2 when the batch forbids re-run (kernel retryLater) -> report-abort.md, `agent-autoloop stop <run>`,
#      exit 0; CLI not launched.
import argparse, fcntl, hashlib, json, os, signal, subprocess, sys, time
from pathlib import Path

ABORT_RESUME = "执行中止：会话续接被拦截，已生成中止报告，禁止重跑"
ABORT_RERUN = "执行中止：重派被拦截，已调用 stop 并生成中止报告，禁止重跑"


def meta(**fields):
    print("META:" + json.dumps(fields, ensure_ascii=False), flush=True)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    for name in ("batch", "folder", "session", "resume", "cwd"):
        ap.add_argument("--" + name, required=True)
    a = ap.parse_args()
    batch = json.loads(Path(a.batch).read_text())
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
        # Live hub wakes the worker's long-poll on /cancel and worker sends SIGTERM to this process group immediately;
        # ignore SIGTERM and flush report-abort.md + stdout before invoking stop so the abort report is never truncated.
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


def launch(batch, a, run, attempt, resume, ev):
    raw = ev / f"attempt-{attempt}"
    raw.mkdir(exist_ok=True)
    v_code = 0
    if batch["mode"] == "stub":
        cmd = batch["cli_cmd"] + [batch["stub_mode"], resume or "NULL_RESUME"]
    else:  # pi-verify: run the fixed command, then read-only Pi writes the report from the raw output.
        v = subprocess.run(batch["verify_command"], cwd=batch["verify_cwd"], capture_output=True, text=True, timeout=600)
        v_code = v.returncode
        (raw / "verify.stdout").write_text(v.stdout)
        (raw / "verify.stderr").write_text(v.stderr)
        (raw / "verify.exit").write_text(f"{v.returncode}\n")
        prompt = batch["pi_prompt"].replace("{RAW}", str(raw))
        cmd = batch["pi_cmd"] + ["--session-dir", str(raw / "pi-sessions")] + \
            (["--session", resume] if resume else []) + [prompt]
    (raw / "cli.argv.json").write_text(json.dumps(cmd, ensure_ascii=False, indent=2) + "\n")
    proc = subprocess.Popen(cmd, cwd=a.cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    session, started, lines = None, False, []
    with open(raw / "cli.stdout", "w") as out:
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
    err = proc.stderr.read()
    code = proc.wait()
    (raw / "cli.stderr").write_text(err)
    (raw / "cli.exit").write_text(f"{code}\n")
    if code != 0:
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
            meta(session=session, started=started)
            sys.stderr.write("BLOCKED: assistant stopReason != stop")
            return 4
        text = "".join(c.get("text", "") for c in last.get("content", []) if c.get("type") == "text").strip()
    expected = batch.get("expected_resume")
    if expected and session != expected:
        with open(ev / "report-abort.md", "a") as f:
            f.write(f"# 执行中止报告\n\n- post-output session {session!r} != expected {expected!r}\n- 治理结论: BLOCKED\n\n")
        meta(session=session, started=True, finished=True)
        print("执行中止：结果后会话身份不符，已生成中止报告，禁止重跑", flush=True)
        return 0
    first_line = text.splitlines()[0] if text else "空"
    if batch["mode"] == "pi-verify":
        ev_result = "pass" if (v_code == 0 and "VERIFY: PASS" in first_line) else "fail"
        c_sha = batch.get("canonical_sha256", "0" * 64)
        c_rev = batch.get("contract_revision", 2)
        manifest = (
            "<!-- COOP_EVIDENCE_MANIFEST_START -->\n```yaml\n"
            f"evidence_schema_version: 2\nevidence_role: attempt-report\nevidence_result: {ev_result}\n"
            f"change_id: {batch.get('change_id', 'integrate-governed-cli-autoloop')}\n"
            f"current_batch: {batch.get('current_batch', 1)}\nattempt: {attempt}\n"
            f"contract_revision: {c_rev}\ncanonical_sha256: {c_sha}\n"
            f"agent_product: pi\nagent_instance_id: {session}\n"
            f"agent_role: executor\ncapability_profile: implementation-high\n```\n"
            "<!-- COOP_EVIDENCE_MANIFEST_END -->\n\n"
        )
        (ev / "report.md").write_text(manifest + text + "\n")
    else:
        (ev / "report.md").write_text(text + "\n")
    receipt = {"evidence_schema_version": 2, "batch_id": batch["batch_id"], "run": run, "attempt": attempt,
               "native_session": session, "verify_exit_code": v_code,
               "assignment": batch.get("assignment"),
               "canonical_status_modified": False, "business_source_modified": False,
               "report_sha256": sha(ev / "report.md"),
               "raw_sha256": {p.name: sha(p) for p in sorted(raw.glob("*")) if p.is_file()}}
    (ev / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    meta(session=session, started=True, finished=True)
    print("报告已交付：治理结论见 report.md（" + first_line + "）", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
