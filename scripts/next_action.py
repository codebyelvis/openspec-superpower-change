#!/usr/bin/env python3
"""Deterministic read-only next-action query for canonical schema-6 status.md.

Author: elvis
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_core_gates import (  # noqa: E402
    ALLOWED_TRANSITIONS,
    ARTIFACT_FIELDS,
    EXPECTED_OWNERS,
    NEXT_OWNERS,
    STATE_TUPLES,
    _result_tuple,
    _transition_artifact_field,
    extract_handoff_contract,
    probe_transition_candidate,
    read,
    validate_handoff_contract,
)


def _identity_summary(assignment: dict) -> dict[str, str]:
    return {
        "agent_product": assignment["agent_product"],
        "agent_instance_id": assignment["agent_instance_id"],
        "agent_role": assignment["agent_role"],
        "capability_profile": assignment["capability_profile"],
    }


def _bound_roles_for_artifact(
    data: dict,
    artifact_field: str | None,
    next_state: str,
) -> list[dict]:
    if artifact_field is None:
        return []
    executor = _identity_summary(data["executor_assignment"])
    reviewer = _identity_summary(data["reviewer_assignment"])
    control_plane = _identity_summary(data["control_plane_owner"])

    if artifact_field == "attempt_report_artifact":
        return [
            {
                "evidence_role": "attempt-report",
                "artifact_field": artifact_field,
                "bound_identity": executor,
            }
        ]
    if artifact_field == "last_review_artifact":
        roles = [
            {
                "evidence_role": "batch-review",
                "artifact_field": artifact_field,
                "bound_identity": reviewer,
            }
        ]
        if next_state == "blocked":
            roles.extend(
                [
                    {
                        "evidence_role": "preflight-review",
                        "artifact_field": artifact_field,
                        "bound_identity": control_plane,
                    },
                    {
                        "evidence_role": "timeout-audit",
                        "artifact_field": artifact_field,
                        "bound_identity": control_plane,
                    },
                ]
            )
        return roles
    if artifact_field == "final_verification_artifact":
        return [
            {
                "evidence_role": "final-verification",
                "artifact_field": artifact_field,
                "bound_identity": control_plane,
            }
        ]
    if artifact_field == "final_review_artifact":
        return [
            {
                "evidence_role": "final-review",
                "artifact_field": artifact_field,
                "bound_identity": control_plane,
            }
        ]
    return []


def query_next_action(text: str, label: str = "status.md") -> dict:
    try:
        data = extract_handoff_contract(text, label)
        validate_handoff_contract(data, label)
    except Exception as exc:
        return {
            "status": "BLOCKED",
            "advisory": True,
            "promotable": False,
            "authoritative": False,
            "reason": str(exc),
            "legal_next_transitions": [],
            "suggested_next_action": None,
        }

    state = data["lifecycle_state"]
    tuple_now = _result_tuple(data)
    base = {
        "status": "OK",
        "advisory": True,
        "promotable": False,
        "authoritative": False,
        "change_id": data["change_id"],
        "contract_revision": data["contract_revision"],
        "current_state": state,
        "result_tuple": {
            "last_review_result": tuple_now[0],
            "final_verification": tuple_now[1],
            "final_review_result": tuple_now[2],
        },
        "current_next_owner": data["next_owner"],
        "allowed_next_owners": sorted(EXPECTED_OWNERS[state]),
        "confirmation_lease_status": data["confirmation_lease_status"],
    }

    if state == "blocked":
        base.update(
            {
                "blocked_reason": data["blocked_reason"],
                "blocker_owner": data["blocker_owner"],
                "resume_condition": data["resume_condition"],
                "legal_next_transitions": [],
                "suggested_next_action": None,
            }
        )
        return base

    transitions: list[dict] = []
    for next_state in sorted(ALLOWED_TRANSITIONS[state]):
        candidate_after = probe_transition_candidate(data, next_state)
        if candidate_after is None:
            continue
        artifact_field = _transition_artifact_field(data, candidate_after)
        transitions.append(
            {
                "next_state": next_state,
                "allowed_next_owners": sorted(EXPECTED_OWNERS[next_state]),
                "required_evidence_roles": _bound_roles_for_artifact(
                    data, artifact_field, next_state
                ),
                "requires_previous_status": (
                    next_state == "complete" or artifact_field is not None
                ),
            }
        )

    base["legal_next_transitions"] = transitions
    return base


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only advisory next-action query for canonical schema-6 status.md."
    )
    parser.add_argument(
        "--status",
        required=True,
        type=Path,
        help="Path to canonical status.md (read-only)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        text = read(args.status)
    except Exception as exc:
        payload = {
            "status": "BLOCKED",
            "advisory": True,
            "promotable": False,
            "authoritative": False,
            "reason": str(exc),
            "legal_next_transitions": [],
            "suggested_next_action": None,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    payload = query_next_action(text, label=str(args.status))
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["status"] == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
