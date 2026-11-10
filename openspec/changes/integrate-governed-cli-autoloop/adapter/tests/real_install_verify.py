#!/usr/bin/env python3
# Author: elvis. Task 2.4 + phase 3 on the live agent-autoloop install: copy-install govpi plugin, add one manual-event
# rule (backup first), real `agent-autoloop stop` drain test, one background Pi VERIFY batch, then rollback with
# worker restart (clears plugin import cache). Rollback always runs. Usage: real_install_verify.py <evidence-dir>
import hashlib, json, os, shutil, subprocess, sys, time
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
C = SRC.parent
W = SRC.parents[3]
R = Path(sys.argv[1]); R.mkdir(parents=True, exist_ok=True)
HOME = Path.home() / ".agent-autoloop"
RULES, PLUG = HOME / "rules.json", HOME / "plugins" / "govpi"
NODE = "/Users/elvis/.nvm/versions/node/v24.22.2/bin/node"  # same runtime as the launchd `up` service
AL = [NODE, "--disable-warning=ExperimentalWarning", str(HOME / "app/bin/agent-autoloop.ts")]
PI, OPENSPEC = shutil.which("pi"), shutil.which("openspec")
LABEL = f"gui/{os.getuid()}/agent-autoloop"
LOG = []
VERIFY_ID = os.environ.get("GOV_VERIFY_ID", "real-verify-20261109-r3")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

def sh(cmd, timeout=60, **kw):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, **kw)
    LOG.append({"at": time.strftime("%H:%M:%S"), "cmd": cmd, "exit": p.returncode, "stdout": p.stdout[-3000:], "stderr": p.stderr[-2000:]})
    return p

def batch(**kw):
    b = {"allow_rerun": False, "expected_resume": None, "ledger_dir": str(R / "ledger"), "evidence_dir": str(R / "evidence"),
         "stop_cmd": AL + ["stop"], **kw}
    (R / "batch.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")
    (R / f"batch-{kw['batch_id']}.json").write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n")

def ledger_run(batch_id, wait):
    f = R / "ledger" / f"{batch_id}.json"
    end = time.time() + wait
    while time.time() < end:
        if f.exists():
            return json.loads(f.read_text())["launches"][0]["run"]
        time.sleep(0.5)
    raise RuntimeError(f"no launch for {batch_id} within {wait}s")

def why(run, name):
    p = sh(AL + ["why", str(run), "--json"])
    (R / f"why-{name}-run{run}.json").write_text(p.stdout)
    return p.stdout

def wait_terminal(run, name, wait):
    end = time.time() + wait
    while time.time() < end:
        out = why(run, name)
        state = None
        for event in json.loads(out or "[]"):  # `why --json` is the run's change log
            for change in event.get("changes", []):
                if change.get("table") == "runs" and str(change.get("key")) == str(run):
                    state = (change.get("row") or {}).get("state") or state
        if state in ("done", "cancelled", "nothing", "failed"):
            return state
        time.sleep(2)
    return "timeout"

facts = {"engine": AL, "pi": PI, "openspec": OPENSPEC, "worktree_head": sh(["git", "-C", str(W), "rev-parse", "HEAD"]).stdout.strip()}
facts["service_pid_before"] = (HOME / "up.pid").read_text().strip()
shutil.copy2(RULES, R / "rules.json.bak")
facts["rules_backup_sha256"] = sha(R / "rules.json.bak")
assert not PLUG.exists(), "govpi already installed"
try:
    # Install (copy from the versioned source location; `agent-autoloop add` would git clone).
    PLUG.mkdir(parents=True)
    for n in ("govpi/agent.ts", "gov_runner.py"):
        shutil.copy2(SRC / n, PLUG / Path(n).name)
    (PLUG / "install.json").write_text(json.dumps({"python": "/usr/bin/python3", "runner": str(PLUG / "gov_runner.py"), "batch": str(R / "batch.json")}) + "\n")
    facts["installed_sha256"] = {p.name: sha(p) for p in sorted(PLUG.iterdir())}
    facts["source_sha256"] = {n: sha(SRC / n) for n in ("govpi/agent.ts", "gov_runner.py")}
    shutil.copy2(SRC / "tests/fake_cli.sh", R / "fake_cli.sh")
    (R / "fixture-cwd").mkdir(exist_ok=True)
    rules = json.loads(RULES.read_text())
    rules["agents"]["gov-pi"] = {"name": "治理受控Pi", "worker": "elvisdemacbook-pro", "use": "govpi", "access": "read", "timeout": 10}
    rules["rules"].append({"name": "治理VERIFY单批次", "when": {"source": "local", "types": ["gov.verify.*"]}, "to": "gov-pi",
                           "cwd": str(R / "fixture-cwd"), "prompt": "受控 VERIFY 单批次；runner 只按批次合同执行。"})
    RULES.write_text(json.dumps(rules, ensure_ascii=False, indent=2) + "\n")
    facts["rules_installed_sha256"] = sha(RULES)
    time.sleep(3)
    sh(AL + ["emit", "gov.verify.probe", "--dry-run", "--subject", "gov-dry"])

    # 2.4 real stop drain (GOV_SKIP_STOPTEST=1 when already proven in an earlier evidence dir)
    if os.environ.get("GOV_SKIP_STOPTEST") != "1":
        batch(batch_id="real-stoptest-20261109-r3", mode="stub", stub_mode="hang", cli_cmd=["/bin/sh", str(R / "fake_cli.sh")])
        sh(AL + ["emit", "gov.verify.stoptest", "--subject", "gov-stop-r3", "--summary", "2.4 stop drain probe"])
        run = ledger_run("real-stoptest-20261109-r3", 90)
        time.sleep(2)
        facts["stoptest_run"] = run
        facts["stoptest_procs_before_stop"] = sh(["pgrep", "-fl", "fake_cli.sh"]).stdout
        facts["stoptest_stop_exit"] = sh(AL + ["stop", str(run)]).returncode
        facts["stoptest_state"] = wait_terminal(run, "stoptest", 60)
        time.sleep(2)
        facts["stoptest_procs_after"] = sh(["pgrep", "-fl", "fake_cli.sh|gov_runner.py"]).stdout
        facts["stoptest_cli_launches"] = (R / "cli-launches.log").read_text().splitlines() if (R / "cli-launches.log").exists() else []

    # Phase 3: one background VERIFY batch with read-only Pi (amd-radeon/DeepSeek-V4-Flash avoids codex-a quota)
    canonical_sha = sha(C / "approval-amendment-phase2-unblock.json")
    batch(batch_id=VERIFY_ID, mode="pi-verify", verify_cwd=str(W),
          change_id="integrate-governed-cli-autoloop", current_batch=1, contract_revision=2,
          canonical_sha256=canonical_sha,
          assignment={
              "schema_version": 6,
              "purpose": "Phase 3 single-batch background VERIFY execution and evidence delivery",
              "product": "pi",
              "role": "executor",
              "profile": "implementation-high",
              "independence_requirement": "independent_from_control_plane_and_reviewer",
              "result_authority": "bounded-execution-evidence",
              "control_plane_native": "01a1aa6c-c4c8-7111-812f-02e1396290e7",
              "independent_reviewer_native": "01a1afbe-e61b-768b-896d-8a743ed83565",
              "dispatch_executor_native": "01a1bec5-45cb-76cc-9766-4c191329bdec",
          },
          verify_command=[OPENSPEC, "validate", "integrate-governed-cli-autoloop", "--strict"],
          pi_cmd=[PI, "-p", "--mode", "json", "--no-mcp", "--no-extensions",
                  "--no-skills", "--no-context-files", "--no-prompt-templates",
                  "--tools", "read,grep,find,ls", "--provider", "amd-radeon", "--model", "DeepSeek-V4-Flash"],
          pi_prompt=("你是受控 VERIFY 只读报告者（role=verify-reporter，change=integrate-governed-cli-autoloop，batch=" + VERIFY_ID + "）。"
                     "只用 read 工具读取 {RAW}/verify.stdout、{RAW}/verify.stderr、{RAW}/verify.exit；不得写文件、不得修复、不得建议重跑或转 FIX。"
                     "第一行严格输出 `VERIFY: PASS` 或 `VERIFY: FAIL`（仅当 exit 为 0 且 stdout 含 is valid 时 PASS），"
                     "随后不超过 5 行：固定命令 `openspec validate integrate-governed-cli-autoloop --strict`、exit、关键输出原文。"))
    sh(AL + ["emit", "gov.verify.run", "--subject", VERIFY_ID, "--summary", "phase 3 single VERIFY batch"])
    vrun = ledger_run(VERIFY_ID, 90)
    facts["verify_run"] = vrun
    facts["verify_state"] = wait_terminal(vrun, "verify", 180)
finally:
    # Rollback: drain check, restore rules bytes, move plugin to audit dir, restart worker to drop the import cache.
    facts["drain_procs_before_rollback"] = sh(["pgrep", "-fl", "fake_cli.sh|gov_runner.py"]).stdout
    shutil.copy2(R / "rules.json.bak", RULES)
    if PLUG.exists():
        dest = R / "rolled-back-plugin-govpi"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.move(str(PLUG), dest)
    facts["kickstart_exit"] = sh(["launchctl", "kickstart", "-k", LABEL]).returncode
    time.sleep(6)
    facts["service_pid_after"] = (HOME / "up.pid").read_text().strip()
    facts["rules_restored_equal_backup"] = sha(RULES) == facts["rules_backup_sha256"]
    facts["plugin_absent_after_rollback"] = not PLUG.exists()
    facts["status_after_rollback"] = sh(AL + ["status"]).stdout[-1500:]
    (R / "real-facts.json").write_text(json.dumps(facts, ensure_ascii=False, indent=2) + "\n")
    (R / "real-commands.json").write_text(json.dumps(LOG, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(facts, ensure_ascii=False, indent=2))
