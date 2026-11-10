#!/usr/bin/env python3
# Author: elvis. Persistent 2.1 pre-launch whitelist and post-output native-ID guard proof.
import json, sys
from pathlib import Path

G = Path(sys.argv[1]) / "guard-2-1"
(G / "raw").mkdir(parents=True, exist_ok=True)
(G / "fixtures/pi").mkdir(parents=True, exist_ok=True)
(G / "fixtures/codex").mkdir(parents=True, exist_ok=True)
(G / "codex-home/sessions/2026/11/09").mkdir(parents=True, exist_ok=True)

INITIAL_PHASES = ("r1", "timeout")
PI_ID = {"id": "6303cbde-d521-487a-a8ab-3f73344d5061", "path": str((G / "pi-session.jsonl").resolve())}
CODEX_ID = "01a1be19-0543-7f91-a85f-db4a2d82c7bd"
(G / "pi-session.jsonl").write_text(json.dumps({"type": "session", "id": PI_ID["id"], "cwd": str((G / "fixtures/pi").resolve())}) + "\n")
(G / "codex-home/sessions/2026/11/09" / f"rollout-{CODEX_ID}.jsonl").write_text(
    json.dumps({"type": "session_meta", "payload": {"id": CODEX_ID, "cwd": str((G / "fixtures/codex").resolve())}}) + "\n"
)
for prod, ident in (("pi", PI_ID), ("codex", CODEX_ID)):
    (G / "raw" / f"{prod}-r1.accepted.json").write_text(json.dumps({"terminal_accepted": True, "process_group_ended": True, "identity": ident}))
    (G / "raw" / f"{prod}-r1.process.json").write_text(json.dumps({"exit_code": 0, "timed_out": False, "process_group_ended": True, "state": "done"}))
(G / "raw/pi-unknown.accepted.json").write_text(json.dumps({"terminal_accepted": True, "process_group_ended": True, "identity": PI_ID}))
(G / "raw/pi-unknown.process.json").write_text(json.dumps({"exit_code": 0, "timed_out": False, "process_group_ended": True, "state": "unknown"}))


def verify_prelaunch(product, phase, identity=None, prior_phase="r1", cwd_override=None, expected_contract_identity=None):
    if phase not in INITIAL_PHASES and not identity:
        raise ValueError("BLOCKED: continuation requires an accepted non-empty identity")
    if phase in INITIAL_PHASES and identity is not None:
        raise ValueError("BLOCKED: initial/timeout phase cannot carry pre-bound continuation identity")
    if expected_contract_identity is not None and identity != expected_contract_identity:
        raise ValueError("BLOCKED: scheduler cleared or replaced bound resume session")
    if identity is not None:
        record = json.loads((G / "raw" / f"{product}-{prior_phase}.accepted.json").read_text())
        if not record.get("terminal_accepted") or not record.get("process_group_ended") or identity != record.get("identity"):
            raise ValueError("BLOCKED: missing or mismatched exact session")
        cwd = Path(cwd_override) if cwd_override else (G / "fixtures" / product)
        target = Path(identity["path"]) if product == "pi" else next((G / "codex-home/sessions").glob(f"**/*{identity}*.jsonl"))
        header = json.loads(target.read_text().splitlines()[0])
        header = header.get("payload", header)
        expected = identity["id"] if isinstance(identity, dict) else identity
        if header.get("id") != expected or Path(header.get("cwd", "")).resolve() != cwd.resolve():
            raise ValueError("BLOCKED: native identity/cwd mismatch")
        prev = json.loads((G / "raw" / f"{product}-{prior_phase}.process.json").read_text())
        if prev.get("exit_code") != 0 or prev.get("timed_out") or not prev.get("process_group_ended") or prev.get("state") == "unknown":
            raise ValueError("BLOCKED: previous execution not accepted or in unknown state")
    return True


def verify_post_output(product, events, expected_identity):
    actual = next((e.get("id" if product == "pi" else "thread_id") for e in events if e.get("type") in ("session", "thread.started")), None)
    expected = expected_identity["id"] if isinstance(expected_identity, dict) else expected_identity
    if expected is not None and actual != expected:
        raise ValueError(f"BLOCKED: post-output native session mismatch ({actual} != {expected})")
    return {"actual_native": actual, "expected_native": expected, "matched": True}


pi_events = [{"type": "session", "id": PI_ID["id"]}, {"type": "message_end", "message": {"role": "assistant", "stopReason": "stop"}}, {"type": "agent_settled", "aborted": False}]
codex_events = [{"type": "thread.started", "thread_id": CODEX_ID}, {"type": "turn.completed"}]
cases = []
for name, fn in [
    ("pi_r2_valid_prelaunch_and_post_output", lambda: {"prelaunch": verify_prelaunch("pi", "r2", PI_ID, expected_contract_identity=PI_ID), "post_output": verify_post_output("pi", pi_events, PI_ID)}),
    ("codex_r2_valid_prelaunch_and_post_output", lambda: {"prelaunch": verify_prelaunch("codex", "r2", CODEX_ID, expected_contract_identity=CODEX_ID), "post_output": verify_post_output("codex", codex_events, CODEX_ID)}),
    ("tightened_whitelist_focused_recheck_empty_identity", lambda: verify_prelaunch("pi", "focused_recheck", None)),
    ("tightened_whitelist_verify_resume_blank_identity", lambda: verify_prelaunch("codex", "verify_resume", "")),
    ("initial_phase_r1_with_unexpected_identity", lambda: verify_prelaunch("codex", "r1", CODEX_ID)),
    ("scheduler_cleared_or_replaced_bound_resume", lambda: verify_prelaunch("codex", "r2", "00000000-0000-0000-0000-000000000000", expected_contract_identity=CODEX_ID)),
    ("codex_changed_cwd_mismatch", lambda: verify_prelaunch("codex", "r2", CODEX_ID, cwd_override=str(G / "fixtures/pi"))),
    ("previous_execution_state_unknown", lambda: verify_prelaunch("pi", "focused_recheck", PI_ID, prior_phase="unknown")),
    ("post_output_silent_new_session_mismatch", lambda: verify_post_output("codex", [{"type": "thread.started", "thread_id": "01a1be19-0543-7f91-a85f-fffffffffffe"}, {"type": "turn.completed"}], CODEX_ID)),
]:
    try:
        cases.append({"case": name, "status": "ACCEPTED", "detail": fn()})
    except ValueError as ex:
        cases.append({"case": name, "status": "REJECTED_BEFORE_LAUNCH_OR_ACCEPT", "reason": str(ex)})

out = {"tightened_guard_line": "if phase not in INITIAL_PHASES and not identity:", "cases": cases}
(Path(sys.argv[1]) / "guard-2-1-results.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
assert [c["status"] for c in cases] == ["ACCEPTED", "ACCEPTED"] + ["REJECTED_BEFORE_LAUNCH_OR_ACCEPT"] * 7
print("guard_2_1_probe ok:", len(cases), "cases")
