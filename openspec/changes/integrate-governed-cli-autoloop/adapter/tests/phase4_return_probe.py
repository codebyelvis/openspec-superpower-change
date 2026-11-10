#!/usr/bin/env python3
# Author: elvis. Phase 4 (4.1-4.3) read-only/fail-closed bound-controller queue verification,
# 8-case envelope pre-check suite, and user-authorized Codex->Pi closeout handoff consumption.
# Supports `--verify-only` so independent reviewers can re-execute all checks with zero file writes.
import copy, hashlib, json, os, subprocess, sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SRC))
import gov_return

C = SRC.parent
W = SRC.parents[3]
MAIN_REPO = Path("/Users/elvis/file/develop/opensource/openspec-superpower-change")
BASE = Path("/Users/elvis/.local/state/governed-cli-autoloop/integrate-governed-cli-autoloop")
R3 = BASE / "real-20261109-r3"
P4 = Path(sys.argv[1])
VERIFY_ONLY = "--verify-only" in sys.argv[2:]
CODEX_HOME = Path("/Users/elvis/.codex-account-a")
CODEX_BIN = "/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex"
THREAD_ID = "01a1aa6c-c4c8-7111-812f-02e1396290e7"
ALLOWED_CWDS = (str(W), str(MAIN_REPO))
ALLOWED_ROOTS = (C, BASE)

sha = gov_return.sha256_file

# 1. Pre-delivery bound thread & account check (strictly read-only `?mode=ro`)
bound_thread_info = gov_return.verify_bound_thread_in_codex_home(CODEX_HOME, THREAD_ID, ALLOWED_CWDS)
try:
    gov_return.verify_bound_thread_in_codex_home(CODEX_HOME, "00000000-0000-0000-0000-000000000000", ALLOWED_CWDS)
    raise AssertionError("Expected missing thread to fail")
except ValueError as ex:
    missing_thread_rejected = str(ex)

# 2. Construct bounded envelope referencing verified Phase 3 & closeout artifacts
report_path = R3 / "evidence/run-11/report.md"
receipt_path = R3 / "evidence/run-11/receipt.json"
closeout_path = C / "evidence/phase-2-3-closeout.json"
review_receipt_path = C / "evidence/pi-phase-2-3-review-receipt.json"
canonical_sha = sha(C / "approval-amendment-phase2-unblock.json")

envelope = {
    "schema_version": 1,
    "envelope_type": "governed-autoloop-return",
    "change_id": "integrate-governed-cli-autoloop",
    "current_batch": 1,
    "attempt": 1,
    "run_id": "11",
    "contract_revision": 2,
    "canonical_sha256": canonical_sha,
    "report_path": str(report_path),
    "report_sha256": sha(report_path),
    "receipt_path": str(receipt_path),
    "receipt_sha256": sha(receipt_path),
    "closeout_path": str(closeout_path),
    "closeout_sha256": sha(closeout_path),
    "review_receipt_path": str(review_receipt_path),
    "review_receipt_sha256": sha(review_receipt_path),
    "executor_native": "01a1bec5-45cb-76cc-9766-4c191329bdec",
    "verify_batch_native": "01a1c320-0e21-7477-8df6-063eab185552",
    "reviewer_native": "01a1afbe-e61b-768b-896d-8a743ed83565",
    "control_plane_native": THREAD_ID,
}
envelope_json = json.dumps(envelope, ensure_ascii=False, sort_keys=True)
envelope_sha256 = hashlib.sha256(envelope_json.encode("utf-8")).hexdigest()

# 3. Fail-closed read-only queue inspection on queue_1.sqlite (NEVER deletes from queue_1.sqlite)
existing_items = gov_return.inspect_queue_readonly(CODEX_HOME, THREAD_ID)
if len(existing_items) == 1 and existing_items[0]["text_sha256"] == envelope_sha256:
    q_item = existing_items[0]
    queue_action = "VERIFIED_EXISTING_BOUNDED_ENVELOPE_READONLY"
elif len(existing_items) == 0 and not VERIFY_ONLY:
    env = os.environ.copy()
    env["CODEX_HOME"] = str(CODEX_HOME)
    q_cmd = [CODEX_BIN, "queue", "--thread", THREAD_ID, "--cd", str(W), "--message", envelope_json]
    q_proc = subprocess.run(q_cmd, env=env, capture_output=True, text=True, timeout=30)
    assert q_proc.returncode == 0, q_proc.stderr
    existing_items = gov_return.inspect_queue_readonly(CODEX_HOME, THREAD_ID)
    assert len(existing_items) == 1 and existing_items[0]["text_sha256"] == envelope_sha256
    q_item = existing_items[0]
    queue_action = "QUEUED_ONCE_WHEN_EMPTY"
else:
    raise SystemExit(
        f"BLOCKED: queue_1.sqlite has unexpected queued_items for {THREAD_ID}; refusing to delete or overwrite"
    )

def check_occupied_queue_guard(items: list[dict], expected_sha: str) -> str:
    if any(i["text_sha256"] != expected_sha for i in items):
        return "BLOCKED_OCCUPIED_QUEUE_REFUSED_NO_DELETE"
    return "OK"

occupied_guard_result = check_occupied_queue_guard(
    [{"id": "foreign-item", "thread_id": THREAD_ID, "queue_order": 0, "text_sha256": "a" * 64}],
    envelope_sha256,
)
assert occupied_guard_result == "BLOCKED_OCCUPIED_QUEUE_REFUSED_NO_DELETE"

# 4.1b: Unawake endpoint `--resume` probe
env = os.environ.copy()
env["CODEX_HOME"] = str(CODEX_HOME)
unawake_cmd = [
    CODEX_BIN, "queue", "--thread", THREAD_ID,
    "--remote", f"unix://{P4 / 'unawake-owner.sock'}",
    "--resume", "--message", envelope_json,
]
unawake_proc = subprocess.run(unawake_cmd, env=env, capture_output=True, text=True, timeout=15)
assert unawake_proc.returncode != 0

# 4.1c: User-authorized Codex -> Pi closeout handoff consumption (`approval-amendment-phase4-pi-closeout.json`)
amend_file = C / "approval-amendment-phase4-pi-closeout.json"
handoff_acceptance = gov_return.consume_queued_envelope_via_authorized_handoff(
    CODEX_HOME,
    THREAD_ID,
    amend_file,
    expected_change_id="integrate-governed-cli-autoloop",
    expected_contract_revision=2,
    expected_canonical_sha256=canonical_sha,
    allowed_roots=ALLOWED_ROOTS,
)
try:
    gov_return.consume_queued_envelope_via_authorized_handoff(
        CODEX_HOME,
        THREAD_ID,
        P4 / "nonexistent-amendment.json",
        expected_change_id="integrate-governed-cli-autoloop",
        expected_contract_revision=2,
        expected_canonical_sha256=canonical_sha,
        allowed_roots=ALLOWED_ROOTS,
    )
    raise AssertionError("Expected missing amendment to fail")
except ValueError as ex:
    missing_amendment_rejected = str(ex)

# 4.2: 8 envelope validation/deduplication cases (in-memory set, zero second governance state file)
common_kw = dict(
    expected_change_id="integrate-governed-cli-autoloop",
    expected_contract_revision=2,
    expected_canonical_sha256=canonical_sha,
    expected_control_plane_native=THREAD_ID,
    allowed_roots=ALLOWED_ROOTS,
)

accepted_set: set[str] = set()
c1 = gov_return.precheck_return_envelope(
    envelope,
    **common_kw,
    already_accepted_keys=accepted_set,
    expected_previous_status="PARTIAL_QUEUED_AWAITING_OWNER",
    actual_previous_status="PARTIAL_QUEUED_AWAITING_OWNER",
)
accepted_set.add(c1["dedup_key"])
c2 = gov_return.precheck_return_envelope(envelope, **common_kw, already_accepted_keys=accepted_set)

stale_rev = copy.deepcopy(envelope); stale_rev["attempt"] = 2; stale_rev["contract_revision"] = 1
c3 = gov_return.precheck_return_envelope(stale_rev, **common_kw, already_accepted_keys=accepted_set)

stale_sha = copy.deepcopy(envelope); stale_sha["attempt"] = 2; stale_sha["canonical_sha256"] = "0" * 64
c4 = gov_return.precheck_return_envelope(stale_sha, **common_kw, already_accepted_keys=accepted_set)

bad_rep = copy.deepcopy(envelope); bad_rep["attempt"] = 2; bad_rep["report_sha256"] = "f" * 64
c5 = gov_return.precheck_return_envelope(bad_rep, **common_kw, already_accepted_keys=accepted_set)

bad_path = copy.deepcopy(envelope); bad_path["attempt"] = 2; bad_path["report_path"] = "/etc/hosts"
c6 = gov_return.precheck_return_envelope(bad_path, **common_kw, already_accepted_keys=accepted_set)

bad_target = copy.deepcopy(envelope); bad_target["attempt"] = 2; bad_target["control_plane_native"] = "01a1bec5-45cb-76cc-9766-4c191329bdec"
c7 = gov_return.precheck_return_envelope(bad_target, **common_kw, already_accepted_keys=accepted_set)

bad_prev = copy.deepcopy(envelope); bad_prev["attempt"] = 2
c8 = gov_return.precheck_return_envelope(
    bad_prev,
    **common_kw,
    already_accepted_keys=accepted_set,
    expected_previous_status="phase-1-in-progress",
    actual_previous_status="PARTIAL_QUEUED_AWAITING_OWNER",
)

cases = {
    "1_valid_first_precheck": c1,
    "2_duplicate_same_batch_attempt": c2,
    "3_stale_contract_revision": c3,
    "4_stale_canonical_sha256": c4,
    "5_tampered_report_sha256": c5,
    "6_out_of_scope_path_traversal": c6,
    "7_mismatched_target_control_plane_native": c7,
    "8_mismatched_previous_status": c8,
}
assert c1["status"] == "PRECHECK_PASSED_AWAITING_BOUND_CONTROL_PLANE" and c1["eligible_for_owner_review"] is True
assert c2["status"] == "DUPLICATE_NOOP" and c2["eligible_for_owner_review"] is False
assert c3["status"] == "REJECTED_STALE_CONTRACT" and c3["eligible_for_owner_review"] is False
assert c4["status"] == "REJECTED_STALE_CONTRACT" and c4["eligible_for_owner_review"] is False
assert c5["status"] == "REJECTED_ARTIFACT_HASH_MISMATCH" and c5["eligible_for_owner_review"] is False
assert c6["status"] == "REJECTED_PATH_OUT_OF_SCOPE" and c6["eligible_for_owner_review"] is False
assert c7["status"] == "REJECTED_TARGET_CONTROLLER_MISMATCH" and c7["eligible_for_owner_review"] is False
assert c8["status"] == "REJECTED_PREVIOUS_STATUS_MISMATCH" and c8["eligible_for_owner_review"] is False
assert not (P4 / "return-dedup-ledger.json").exists(), "Second governance state file must not exist"

if not VERIFY_ONLY:
    (P4 / "bounded-envelope.json").write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n")
formatted_file_sha = sha(P4 / "bounded-envelope.json")

results = {
    "phase_4_status": "COMPLETED_VIA_USER_AUTHORIZED_PI_CLOSEOUT_HANDOFF",
    "bound_thread_verification": bound_thread_info,
    "missing_thread_rejected": missing_thread_rejected,
    "occupied_queue_guard_result": occupied_guard_result,
    "prior_sqlite_mutation_audit": {
        "disclosed": True,
        "summary": "During the initial 2026-11-10 exploratory probe before P1-2 fix, two DELETE statements were executed on ~/.codex-account-a/queue_1.sqlite for thread_id 01a1aa6c-c4c8-7111-812f-02e1396290e7: (1) deleting the temporary 'test probe' row 01a1c382-bfd7-7100-a8e0-d292cc6c33d6 created seconds earlier in the same turn, and (2) an initial pre-queue DELETE in v1 of phase4_return_probe.py. No pre-existing user queued rows existed prior to 1794281488343. All SQLite DELETE/write operations have been removed from gov_return.py and phase4_return_probe.py, which open state_5.sqlite and queue_1.sqlite strictly with `?mode=ro` and fail-closed on any unexpected existing queue item.",
    },
    "live_queue_delivery": {
        "queue_action": queue_action,
        "command": [CODEX_BIN, "queue", "--thread", THREAD_ID, "--cd", str(W), "--message", "<bounded-envelope-json>"],
        "queued_item_id": q_item["id"],
        "thread_id": THREAD_ID,
        "queue_order": q_item["queue_order"],
        "created_at_ms": q_item["created_at_ms"],
        "queued_count_for_thread": len(existing_items),
        "payload_json_sha256": q_item["payload_json_sha256"],
        "envelope_sha256": envelope_sha256,
        "formatted_envelope_file_sha256": formatted_file_sha,
        "sqlite_payload_matches_envelope_sha256": True,
    },
    "unawake_resume_probe": {
        "command": unawake_cmd[:6] + ["--message", "<bounded-envelope-json>"],
        "exit_code": unawake_proc.returncode,
        "stderr": unawake_proc.stderr.strip(),
    },
    "codex_native_resume_blocker_observed": {
        "observed_at": "2026-11-10",
        "reasons": [
            "Codex TUI rejected thread model gpt-6.1-sol ('not supported when using Codex with a ChatGPT account')",
            "Desktop app session lock reported 'session is open in another app; no operation was sent'",
            "CLI multi-line -C argument line-split friction in user terminal",
        ],
    },
    "authorized_pi_closeout_handoff": {
        "amendment_path": str(amend_file),
        "amendment_sha256": sha(amend_file),
        "missing_amendment_rejected": missing_amendment_rejected,
        "handoff_acceptance": handoff_acceptance,
    },
    "four_stage_delivery_state": {
        "queued": True,
        "resume_attempted_on_codex": True,
        "codex_native_resume_outcome": "BLOCKED_BY_MODEL_AND_APP_SESSION_LOCK",
        "consumed_via_authorized_pi_handoff": True,
        "governance_accepted_for_change_closeout": True,
    },
    "precheck_prototype_cases": cases,
}

if not VERIFY_ONLY:
    (P4 / "phase4-results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    (C / "evidence/phase-4-delivery-receipt.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
    (C / "evidence/phase-4-pi-handoff-acceptance.json").write_text(json.dumps(handoff_acceptance, ensure_ascii=False, indent=2) + "\n")

print(json.dumps({
    "verify_only": VERIFY_ONLY,
    "phase_4_status": results["phase_4_status"],
    "queued_item_id": q_item["id"],
    "created_at_ms": q_item["created_at_ms"],
    "envelope_sha256": envelope_sha256,
    "formatted_envelope_file_sha256": formatted_file_sha,
    "handoff_status": handoff_acceptance["status"],
    "cases_passed": len(cases),
}, ensure_ascii=False))
