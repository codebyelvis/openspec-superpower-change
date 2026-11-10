#!/usr/bin/env python3
# Author: elvis. Host-side Phase 4 bound-controller return & user-authorized Pi closeout handoff verifier
# (change integrate-governed-cli-autoloop).
# Scope boundary:
#   - Opens state_5.sqlite and queue_1.sqlite strictly read-only (`?mode=ro`).
#   - Verifies envelope schema, path confinement, artifact SHA-256s, contract revision/fingerprint,
#     and deduplication against already-accepted canonical evidence snapshots in memory.
#   - Does NOT create a second persistent governance state file (spec.md:116).
#   - Under approval-amendment-phase4-pi-closeout.json, allows the user-authorized Pi closeout instance
#     to read and verify the queued envelope in queue_1.sqlite (?mode=ro) when the original Codex thread
#     is blocked by TUI model support / app session lock.
import hashlib, json, re, sqlite3
from pathlib import Path

REQUIRED_ENVELOPE_KEYS = {
    "schema_version",
    "envelope_type",
    "change_id",
    "current_batch",
    "attempt",
    "run_id",
    "contract_revision",
    "canonical_sha256",
    "report_path",
    "report_sha256",
    "receipt_path",
    "receipt_sha256",
    "closeout_path",
    "closeout_sha256",
    "review_receipt_path",
    "review_receipt_sha256",
    "executor_native",
    "verify_batch_native",
    "reviewer_native",
    "control_plane_native",
}
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_bound_thread_in_codex_home(codex_home: Path, expected_thread_id: str, allowed_cwds: tuple[str, ...]) -> dict:
    db_path = codex_home / "state_5.sqlite"
    idx_path = codex_home / "session_index.jsonl"
    if not db_path.is_file() or not idx_path.is_file():
        raise ValueError("BLOCKED: CODEX_HOME state_5.sqlite or session_index.jsonl missing")
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        row = con.execute(
            "SELECT id, cwd, substr(title, 1, 80), updated_at FROM threads WHERE id = ?",
            (expected_thread_id,),
        ).fetchone()
    finally:
        con.close()
    if not row:
        raise ValueError(f"BLOCKED: bound controller thread {expected_thread_id} not found in state_5.sqlite")
    thread_id, thread_cwd, title_head, updated_at = row
    resolved_cwd = str(Path(thread_cwd).resolve())
    allowed_resolved = {str(Path(p).resolve()) for p in allowed_cwds}
    if resolved_cwd not in allowed_resolved:
        raise ValueError(f"BLOCKED: bound thread cwd {resolved_cwd} not in allowed project roots {sorted(allowed_resolved)}")
    thread_name = None
    for line in idx_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        if obj.get("id") == expected_thread_id:
            thread_name = obj.get("thread_name")
            break
    if thread_name is None:
        raise ValueError(f"BLOCKED: bound controller thread {expected_thread_id} missing from session_index.jsonl")
    return {
        "thread_id": thread_id,
        "thread_cwd": resolved_cwd,
        "thread_name_in_index": thread_name,
        "first_prompt_head": title_head,
        "updated_at": updated_at,
        "in_session_index": True,
    }


def inspect_queue_readonly(codex_home: Path, thread_id: str) -> list[dict]:
    q_path = codex_home / "queue_1.sqlite"
    if not q_path.is_file():
        raise ValueError("BLOCKED: CODEX_HOME queue_1.sqlite missing")
    con = sqlite3.connect(f"file:{q_path}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "SELECT id, thread_id, queue_order, created_at_ms, payload_json FROM queued_items WHERE thread_id = ? ORDER BY queue_order ASC",
            (thread_id,),
        ).fetchall()
    finally:
        con.close()
    items = []
    for r in rows:
        raw_payload = r[4]
        payload = json.loads(raw_payload)
        text = payload.get("UserInput", {}).get("content", [{}])[0].get("text", "")
        items.append({
            "id": r[0],
            "thread_id": r[1],
            "queue_order": r[2],
            "created_at_ms": r[3],
            "payload_json_length": len(raw_payload),
            "payload_json_sha256": hashlib.sha256(raw_payload.encode("utf-8")).hexdigest(),
            "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "text_length": len(text),
            "text": text,
        })
    return items


def precheck_return_envelope(
    envelope: dict,
    *,
    expected_change_id: str,
    expected_contract_revision: int,
    expected_canonical_sha256: str,
    expected_control_plane_native: str,
    allowed_roots: tuple[Path, ...],
    already_accepted_keys: set[str] | None = None,
    expected_previous_status: str | None = None,
    actual_previous_status: str | None = None,
) -> dict:
    if not isinstance(envelope, dict) or set(envelope.keys()) != REQUIRED_ENVELOPE_KEYS:
        return {"status": "REJECTED_SCHEMA_MISMATCH", "eligible_for_owner_review": False, "reason": "Envelope keys do not match bounded schema"}
    if envelope.get("schema_version") != 1 or envelope.get("envelope_type") != "governed-autoloop-return":
        return {"status": "REJECTED_SCHEMA_MISMATCH", "eligible_for_owner_review": False, "reason": "Unsupported schema_version or envelope_type"}
    if envelope.get("change_id") != expected_change_id:
        return {"status": "REJECTED_CHANGE_MISMATCH", "eligible_for_owner_review": False, "reason": "change_id mismatch"}
    if envelope.get("control_plane_native") != expected_control_plane_native:
        return {"status": "REJECTED_TARGET_CONTROLLER_MISMATCH", "eligible_for_owner_review": False, "reason": "control_plane_native target mismatch"}
    if expected_previous_status is not None and expected_previous_status != actual_previous_status:
        return {
            "status": "REJECTED_PREVIOUS_STATUS_MISMATCH",
            "eligible_for_owner_review": False,
            "reason": f"previous_status {expected_previous_status!r} != actual {actual_previous_status!r}",
        }
    if envelope.get("contract_revision") != expected_contract_revision or envelope.get("canonical_sha256") != expected_canonical_sha256:
        return {
            "status": "REJECTED_STALE_CONTRACT",
            "eligible_for_owner_review": False,
            "reason": "Stale or mismatched contract_revision / canonical_sha256",
        }
    for sha_key in ("canonical_sha256", "report_sha256", "receipt_sha256", "closeout_sha256", "review_receipt_sha256"):
        if not HEX64.match(str(envelope.get(sha_key, ""))):
            return {"status": "REJECTED_INVALID_SHA256", "eligible_for_owner_review": False, "reason": f"Invalid 64-hex digest in {sha_key}"}

    resolved_roots = [r.resolve() for r in allowed_roots]
    for path_key, sha_key in (
        ("report_path", "report_sha256"),
        ("receipt_path", "receipt_sha256"),
        ("closeout_path", "closeout_sha256"),
        ("review_receipt_path", "review_receipt_sha256"),
    ):
        p = Path(envelope[path_key]).resolve()
        if not any(p == root or root in p.parents for root in resolved_roots):
            return {"status": "REJECTED_PATH_OUT_OF_SCOPE", "eligible_for_owner_review": False, "reason": f"{path_key} ({p}) outside allowed roots"}
        if not p.is_file():
            return {"status": "REJECTED_MISSING_ARTIFACT", "eligible_for_owner_review": False, "reason": f"{path_key} ({p}) missing on disk"}
        actual_sha = sha256_file(p)
        if actual_sha != envelope[sha_key]:
            return {
                "status": "REJECTED_ARTIFACT_HASH_MISMATCH",
                "eligible_for_owner_review": False,
                "reason": f"{path_key} sha256 {actual_sha} != envelope {envelope[sha_key]}",
            }

    dedup_key = f"{envelope['change_id']}:batch-{envelope['current_batch']}:attempt-{envelope['attempt']}"
    accepted = already_accepted_keys if already_accepted_keys is not None else set()
    if dedup_key in accepted:
        return {
            "status": "DUPLICATE_NOOP",
            "eligible_for_owner_review": False,
            "dedup_key": dedup_key,
            "reason": "Duplicate envelope for same (change_id, current_batch, attempt) already present in accepted evidence; no re-execution",
        }
    return {
        "status": "PRECHECK_PASSED_AWAITING_BOUND_CONTROL_PLANE",
        "eligible_for_owner_review": True,
        "dedup_key": dedup_key,
        "note": "Pre-check prototype; canonical acceptance requires bound Codex control-plane or explicit user-authorized Phase 4 closeout handoff.",
    }


def consume_queued_envelope_via_authorized_handoff(
    codex_home: Path,
    thread_id: str,
    amendment_file: Path,
    *,
    expected_change_id: str,
    expected_contract_revision: int,
    expected_canonical_sha256: str,
    allowed_roots: tuple[Path, ...],
) -> dict:
    if not amendment_file.is_file():
        raise ValueError("BLOCKED: approval-amendment-phase4-pi-closeout.json missing")
    amendment = json.loads(amendment_file.read_text(encoding="utf-8"))
    if amendment.get("change_id") != expected_change_id or amendment.get("previous_control_plane_native") != thread_id:
        raise ValueError("BLOCKED: amendment change_id or previous_control_plane_native mismatch")
    owner = amendment.get("authorized_phase4_closeout_owner") or {}
    if owner.get("product") != "pi" or not owner.get("instance_id"):
        raise ValueError("BLOCKED: amendment does not bind a concrete Pi closeout owner")

    items = inspect_queue_readonly(codex_home, thread_id)
    if len(items) != 1:
        raise ValueError(f"BLOCKED: expected exactly 1 queued item for {thread_id}, found {len(items)}")
    item = items[0]
    envelope = json.loads(item["text"])
    pre = precheck_return_envelope(
        envelope,
        expected_change_id=expected_change_id,
        expected_contract_revision=expected_contract_revision,
        expected_canonical_sha256=expected_canonical_sha256,
        expected_control_plane_native=thread_id,
        allowed_roots=allowed_roots,
        already_accepted_keys=set(),
        expected_previous_status="PARTIAL_QUEUED_AWAITING_OWNER",
        actual_previous_status="PARTIAL_QUEUED_AWAITING_OWNER",
    )
    if not pre["eligible_for_owner_review"]:
        raise ValueError(f"BLOCKED: queued envelope failed precheck: {pre}")
    return {
        "status": "ACCEPTED_VIA_USER_AUTHORIZED_PI_CLOSEOUT_HANDOFF",
        "queued_item_id": item["id"],
        "thread_id": thread_id,
        "queue_order": item["queue_order"],
        "created_at_ms": item["created_at_ms"],
        "payload_json_sha256": item["payload_json_sha256"],
        "envelope_sha256": item["text_sha256"],
        "dedup_key": pre["dedup_key"],
        "authorized_closeout_owner": owner,
        "amendment_sha256": sha256_file(amendment_file),
    }
