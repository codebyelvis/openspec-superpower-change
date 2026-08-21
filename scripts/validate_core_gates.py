#!/usr/bin/env python3
"""Validate non-negotiable routing, lifecycle, evidence, and completion gates."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path, PurePosixPath

try:
    import yaml
except ModuleNotFoundError:  # The supported subset has a dependency-free fallback.
    yaml = None


START = "<!-- COOP_HANDOFF_CONTRACT_START -->"
END = "<!-- COOP_HANDOFF_CONTRACT_END -->"
EVIDENCE_START = "<!-- COOP_EVIDENCE_MANIFEST_START -->"
EVIDENCE_END = "<!-- COOP_EVIDENCE_MANIFEST_END -->"
LEASE_START = "<!-- COOP_CONFIRMATION_LEASE_START -->"
LEASE_END = "<!-- COOP_CONFIRMATION_LEASE_END -->"
SCHEMA_VERSION = 6
SCHEMA5_VERSION = 5
LEGACY_SCHEMA_VERSION = 4
EVIDENCE_SCHEMA_VERSION = 2
LEGACY_EVIDENCE_SCHEMA_VERSION = 1
SCHEMA6_AGENT_PRODUCTS = {"codex", "pi", "antigravity-cli", "grok-cli"}
SCHEMA5_AGENT_PRODUCTS = {"codex", "antigravity-cli", "grok-cli"}
SCHEMA4_EXECUTOR_PRODUCTS = {"antigravity-cli", "grok-cli"}
SCHEMA4_REVIEWER_PRODUCTS = SCHEMA5_AGENT_PRODUCTS | {"not-applicable"}
AGENT_ROLES = {"executor", "independent-reviewer", "decision-owner"}
SCHEMA6_AGENT_ROLES = {"control-plane", "executor", "independent-reviewer"}
SCHEMA5_AGENT_ROLES = {"control-plane", "executor", "independent-reviewer"}
CAPABILITY_PROFILES = {"control-plane-high", "cohesive-medium", "mechanical-low"}
DECISION_SOURCES = {
    "ai-proposed/user-approved", "user-originated", "user-corrected",
    "evidence-discovered", "deferred", "revoked",
}
BUSINESS_PRODUCTION_ACTIONS = {
    "production-deletion", "production-write", "real-credentials", "paid-endpoint",
    "migration", "release", "archive", "promotion", "destructive-git",
    "external-message",
}
RISK_PROFILES = {"compact", "standard", "strict"}
BATCH_PROFILES = {"single", "cohesive", "staged"}
BUSINESS_ACCEPTANCE = {"required", "optional", "not-applicable"}
MODES = {
    "review-only", "discovery-first", "openspec-proposal",
    "approved-implementation", "direct-change", "self-evolution",
}
APPROVAL_STATUSES = {"not-required", "proposed", "approved", "blocked"}
EXECUTORS = {"codex", "external-agent"}
GOVERNORS = {"openspec-superpower-change", "codex-brief-antigravity-review"}
NEXT_OWNERS = {
    "openspec-superpower-change", "codex-brief-antigravity-review",
    "external-agent", "user",
}
LIFECYCLE_STATES = {
    "ready-for-brief", "ready-for-execution", "ready-for-review",
    "needs-fix", "blocked", "awaiting-final-verification", "complete",
}
REVIEW_RESULTS = {"not-run", "pass", "fail", "blocked"}
FINAL_RESULTS = {"pending", "pass", "fail", "blocked"}
BLOCKER_OWNERS = {
    "none", "openspec-superpower-change", "codex-brief-antigravity-review",
    "external-agent", "user", "dependency",
}
ALLOWED_TRANSITIONS = {
    "ready-for-brief": {"ready-for-execution", "blocked"},
    "ready-for-execution": {"ready-for-review", "blocked"},
    "ready-for-review": {
        "needs-fix", "blocked", "ready-for-brief",
        "awaiting-final-verification",
    },
    "needs-fix": {"ready-for-execution", "blocked"},
    "blocked": {
        "ready-for-brief", "ready-for-execution", "needs-fix",
        "awaiting-final-verification", "blocked",
    },
    "awaiting-final-verification": {
        "awaiting-final-verification", "complete", "needs-fix", "blocked",
    },
    "complete": set(),
}
LEGACY_IMMUTABLE_FIELDS = {
    "schema_version", "change_id", "mode", "approval_status", "risk_profile",
    "batch_profile", "planned_batches", "executor", "governor",
    "executor_agent", "independent_reviewer_agent", "decision_owner",
    "independent_review_not_applicable_reason",
    "step_critical", "final_critical", "business_acceptance",
    "stop_conditions", "verification_strategy", "readonly_fields",
}
SCHEMA5_IMMUTABLE_FIELDS = {
    "schema_version", "change_id", "mode", "approval_status", "risk_profile",
    "batch_profile", "planned_batches", "executor", "governor",
    "control_plane_owner", "executor_assignment",
    "independent_reviewer_assignment",
    "independent_review_not_applicable_reason", "decision_source",
    "confirmation_lease", "step_critical", "final_critical",
    "business_acceptance", "stop_conditions", "verification_strategy",
    "readonly_fields",
}
SCHEMA6_IMMUTABLE_FIELDS = (
    SCHEMA5_IMMUTABLE_FIELDS
    - {"independent_reviewer_assignment"}
    | {"reviewer_assignment"}
)
# Current-schema compatibility alias for callers that inspect immutable fields.
IMMUTABLE_FIELDS = SCHEMA6_IMMUTABLE_FIELDS
ARTIFACT_FIELDS = (
    "attempt_report_artifact", "last_review_artifact",
    "final_verification_artifact", "final_review_artifact",
)
EVIDENCE_ROLES = {
    "attempt-report", "batch-review", "preflight-review", "timeout-audit",
    "final-verification", "final-review",
}
EVIDENCE_RESULTS = {"pass", "fail", "blocked"}
STATE_TUPLES = {
    "ready-for-brief": {
        ("not-run", "pending", "pending"),
        ("pass", "pending", "pending"),
    },
    "ready-for-execution": {("not-run", "pending", "pending")},
    "ready-for-review": {("not-run", "pending", "pending")},
    "needs-fix": {
        ("fail", "pending", "pending"),
        ("pass", "fail", "pending"),
        ("pass", "pass", "fail"),
    },
    "blocked": {
        ("blocked", "pending", "pending"),
        ("pass", "blocked", "pending"),
        ("pass", "pass", "blocked"),
    },
    "awaiting-final-verification": {
        ("pass", "pending", "pending"),
        ("pass", "pass", "pending"),
    },
    "complete": {("pass", "pass", "pass")},
}


def parse_scalar(value: str):
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "~"}:
        return None
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def simple_yaml_load(text: str) -> dict:
    lines = [
        (len(raw) - len(raw.lstrip(" ")), raw.strip())
        for raw in text.splitlines()
        if raw.strip() and not raw.lstrip().startswith("#")
    ]
    if not lines:
        return {}

    def parse_block(index: int, indent: int):
        is_list = lines[index][1].startswith("- ")
        container = [] if is_list else {}
        while index < len(lines):
            line_indent, line = lines[index]
            if line_indent < indent:
                break
            if line_indent > indent:
                raise AssertionError("fallback YAML has unexpected indentation")
            if is_list:
                if not line.startswith("- "):
                    raise AssertionError("fallback YAML mixes list and mapping entries")
                item = line[2:].strip()
                if not item:
                    raise AssertionError("fallback YAML does not allow empty list items")
                container.append(parse_scalar(item))
                index += 1
                continue
            if line.startswith("- ") or ":" not in line:
                raise AssertionError("fallback YAML mapping entry is invalid")
            key, raw_value = line.split(":", 1)
            key = key.strip()
            if not key or key in container:
                raise AssertionError("fallback YAML has an empty or duplicate key")
            raw_value = raw_value.strip()
            index += 1
            if raw_value:
                container[key] = parse_scalar(raw_value)
                continue
            if index < len(lines) and lines[index][0] > indent:
                child_indent = lines[index][0]
                container[key], index = parse_block(index, child_indent)
            else:
                container[key] = {}
        return container, index

    result, consumed = parse_block(0, lines[0][0])
    if consumed != len(lines) or not isinstance(result, dict):
        raise AssertionError("fallback YAML root must be one complete mapping")
    return result


def yaml_load(text: str):
    return yaml.safe_load(text) if yaml is not None else simple_yaml_load(text)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise AssertionError(f"missing required file: {path}") from exc


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"{label}: missing required text: {needle!r}")


def extract_handoff_contract(text: str, label: str) -> dict:
    if text.count(START) != 1 or text.count(END) != 1:
        raise AssertionError(f"{label}: handoff contract must have exactly one marker block")
    body = text.split(START, 1)[1].split(END, 1)[0].strip()
    if body.startswith("```yaml"):
        body = body.removeprefix("```yaml").strip()
    if body.endswith("```"):
        body = body[:-3].strip()
    data = yaml_load(body)
    if not isinstance(data, dict):
        raise AssertionError(f"{label}: handoff contract must be a YAML mapping")
    return data


def extract_evidence_manifest(text: str, label: str) -> dict:
    if text.count(EVIDENCE_START) != 1 or text.count(EVIDENCE_END) != 1:
        raise AssertionError(f"{label}: evidence artifact must have exactly one manifest block")
    body = text.split(EVIDENCE_START, 1)[1].split(EVIDENCE_END, 1)[0].strip()
    if body.startswith("```yaml"):
        body = body.removeprefix("```yaml").strip()
    if body.endswith("```"):
        body = body[:-3].strip()
    data = yaml_load(body)
    if not isinstance(data, dict):
        raise AssertionError(f"{label}: evidence manifest must be a YAML mapping")
    return data


def extract_confirmation_lease(text: str, label: str) -> dict:
    if text.count(LEASE_START) != 1 or text.count(LEASE_END) != 1:
        raise AssertionError(f"{label}: Confirmation Lease must have exactly one marker block")
    body = text.split(LEASE_START, 1)[1].split(LEASE_END, 1)[0].strip()
    if body.startswith("```yaml"):
        body = body.removeprefix("```yaml").strip()
    if body.endswith("```"):
        body = body[:-3].strip()
    data = yaml_load(body)
    if not isinstance(data, dict):
        raise AssertionError(f"{label}: Confirmation Lease must be a YAML mapping")
    return data


def _require_positive_int(data: dict, key: str, label: str) -> None:
    if type(data[key]) is not int or data[key] < 1:
        raise AssertionError(f"{label}: {key} must be a positive integer")


def _is_nonblank(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_string_list(value, key: str, label: str) -> None:
    if not isinstance(value, list) or not value:
        raise AssertionError(f"{label}: {key} must be a non-empty string list")
    if not all(_is_nonblank(item) for item in value):
        raise AssertionError(f"{label}: {key} entries must be non-blank strings")


def _validate_artifact_ref(value, required: bool, key: str, label: str) -> None:
    if value is None:
        if required:
            raise AssertionError(f"{label}: {key} is required")
        return
    if not isinstance(value, dict) or set(value) != {"path", "sha256"}:
        raise AssertionError(f"{label}: {key} must be a path/sha256 mapping or null")
    path = value["path"]
    digest = value["sha256"]
    if not _is_nonblank(path) or path != path.strip():
        raise AssertionError(f"{label}: {key}.path must be non-blank")
    if "\\" in path or "://" in path:
        raise AssertionError(f"{label}: {key}.path must be project-relative")
    pure = PurePosixPath(path)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in path.split("/")):
        raise AssertionError(f"{label}: {key}.path must be a safe project-relative path")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise AssertionError(f"{label}: {key}.sha256 must be 64 lowercase hex characters")


def _result_tuple(data: dict) -> tuple[str, str, str]:
    return (
        data["last_review_result"],
        data["final_verification"],
        data["final_review_result"],
    )


def _validate_distinct_artifact_paths(data: dict, label: str) -> None:
    fields_by_path: dict[str, list[str]] = {}
    for key in ARTIFACT_FIELDS:
        ref = data[key]
        if ref is not None:
            fields_by_path.setdefault(ref["path"], []).append(key)
    for path, fields in fields_by_path.items():
        if len(fields) == 1:
            continue
        if (
            set(fields) == {"attempt_report_artifact", "last_review_artifact"}
            and data["lifecycle_state"] == "blocked"
            and _result_tuple(data) == ("blocked", "pending", "pending")
            and data["attempt_report_artifact"] == data["last_review_artifact"]
        ):
            continue
        raise AssertionError(
            f"{label}: evidence artifact paths must be distinct by role: {path} used by {fields}"
        )


def _validate_schema4_handoff_contract(data: dict, label: str) -> None:
    required = {
        "schema_version", "change_id", "mode", "approval_status",
        "risk_profile", "batch_profile", "current_batch", "planned_batches",
        "attempt", "contract_revision", "lifecycle_state",
        "attempt_report_artifact", "last_review_result", "last_review_artifact",
        "blocked_reason", "blocker_owner", "resume_condition",
        "final_verification", "final_verification_artifact",
        "final_review_result", "final_review_artifact", "executor", "governor",
        "executor_agent", "independent_reviewer_agent", "decision_owner",
        "independent_review_not_applicable_reason",
        "next_owner", "step_critical", "final_critical",
        "business_acceptance", "stop_conditions", "verification_strategy",
        "readonly_fields",
    }
    missing = sorted(required - set(data))
    unexpected = sorted(set(data) - required)
    if missing:
        raise AssertionError(f"{label}: missing contract fields: {missing}")
    if unexpected:
        raise AssertionError(f"{label}: unexpected contract fields: {unexpected}")
    if data["schema_version"] != LEGACY_SCHEMA_VERSION:
        raise AssertionError(f"{label}: schema_version must be {LEGACY_SCHEMA_VERSION}")
    enums = {
        "mode": MODES,
        "approval_status": APPROVAL_STATUSES,
        "risk_profile": RISK_PROFILES,
        "batch_profile": BATCH_PROFILES,
        "executor": EXECUTORS,
        "governor": GOVERNORS,
        "next_owner": NEXT_OWNERS,
        "lifecycle_state": LIFECYCLE_STATES,
        "last_review_result": REVIEW_RESULTS,
        "blocker_owner": BLOCKER_OWNERS,
        "final_verification": FINAL_RESULTS,
        "final_review_result": FINAL_RESULTS,
    }
    for key, allowed in enums.items():
        if data[key] not in allowed:
            raise AssertionError(f"{label}: invalid {key}")
    for key in ("current_batch", "planned_batches", "attempt", "contract_revision"):
        _require_positive_int(data, key, label)
    if data["current_batch"] > data["planned_batches"]:
        raise AssertionError(f"{label}: current_batch must not exceed planned_batches")
    if not isinstance(data["change_id"], str) or not re.fullmatch(
        r"[a-z0-9]+(?:-[a-z0-9]+)*", data["change_id"]
    ):
        raise AssertionError(f"{label}: change_id must be a path-safe kebab-case slug")
    if data["executor"] != "external-agent" or data["governor"] != "codex-brief-antigravity-review":
        raise AssertionError(f"{label}: execution contract requires external-agent executor and brief governor")
    if data["executor_agent"] not in SCHEMA4_EXECUTOR_PRODUCTS:
        raise AssertionError(f"{label}: invalid executor agent identity")
    if data["independent_reviewer_agent"] not in SCHEMA4_REVIEWER_PRODUCTS:
        raise AssertionError(f"{label}: invalid independent reviewer agent identity")
    if data["decision_owner"] != "codex":
        raise AssertionError(f"{label}: decision_owner must be codex")
    reviewer = data["independent_reviewer_agent"]
    reason = data["independent_review_not_applicable_reason"]
    if reviewer == "not-applicable":
        if data["risk_profile"] != "compact":
            raise AssertionError(f"{label}: not-applicable reviewer is allowed only for compact")
        if not _is_nonblank(reason):
            raise AssertionError(f"{label}: not-applicable reviewer requires a non-blank reason")
    else:
        if reviewer == data["executor_agent"]:
            raise AssertionError(f"{label}: executor and independent reviewer must be distinct")
        if reason is not None:
            raise AssertionError(f"{label}: reviewer reason must be null unless reviewer is not-applicable")
    if data["mode"] not in {"approved-implementation", "direct-change", "self-evolution"}:
        raise AssertionError(f"{label}: execution contract has invalid mode")
    if data["mode"] in {"approved-implementation", "self-evolution"} and data["approval_status"] != "approved":
        raise AssertionError(f"{label}: execution contract must be approved")
    if data["mode"] == "direct-change" and data["approval_status"] not in {"not-required", "approved"}:
        raise AssertionError(f"{label}: direct-change execution contract has invalid approval")

    acceptance = data["business_acceptance"]
    acceptance_keys = {"unit", "pipeline", "api", "real_business"}
    if not isinstance(acceptance, dict) or set(acceptance) != acceptance_keys:
        raise AssertionError(f"{label}: business_acceptance must contain exactly {sorted(acceptance_keys)}")
    for key in acceptance_keys:
        if acceptance[key] not in BUSINESS_ACCEPTANCE:
            raise AssertionError(f"{label}: invalid business_acceptance.{key}")
    for key in ("step_critical", "final_critical", "stop_conditions"):
        _validate_string_list(data[key], key, label)
    strategy = data["verification_strategy"]
    if not isinstance(strategy, dict) or set(strategy) != {"step", "final"} or not all(
        _is_nonblank(strategy[key]) for key in ("step", "final")
    ):
        raise AssertionError(f"{label}: verification_strategy must be a non-blank step/final string mapping")
    readonly = data["readonly_fields"]
    if (
        not isinstance(readonly, list)
        or not all(isinstance(item, str) for item in readonly)
        or len(readonly) != len(set(readonly))
        or set(readonly) != LEGACY_IMMUTABLE_FIELDS
    ):
        raise AssertionError(f"{label}: readonly_fields must exactly match immutable fields without duplicates")

    state = data["lifecycle_state"]
    result_tuple = _result_tuple(data)
    if result_tuple not in STATE_TUPLES[state]:
        raise AssertionError(f"{label}: invalid result tuple for {state}")
    expected_owners = {
        "ready-for-brief": {"codex-brief-antigravity-review"},
        "ready-for-execution": {"external-agent"},
        "ready-for-review": {"codex-brief-antigravity-review"},
        "needs-fix": {"codex-brief-antigravity-review", "openspec-superpower-change"},
        "blocked": NEXT_OWNERS,
        "awaiting-final-verification": {"openspec-superpower-change"},
        "complete": {"user"},
    }
    if data["next_owner"] not in expected_owners[state]:
        raise AssertionError(f"{label}: invalid next_owner for {state}")

    if state == "blocked":
        if not _is_nonblank(data["blocked_reason"]):
            raise AssertionError(f"{label}: blocked_reason must be non-blank")
        if data["blocker_owner"] == "none":
            raise AssertionError(f"{label}: blocked requires blocker_owner")
        if not _is_nonblank(data["resume_condition"]):
            raise AssertionError(f"{label}: resume_condition must be non-blank")
    elif data["blocked_reason"] is not None or data["blocker_owner"] != "none" or data["resume_condition"] is not None:
        raise AssertionError(f"{label}: non-blocked state must clear blocker fields")

    report_required = state in {
        "ready-for-review", "needs-fix",
        "awaiting-final-verification", "complete",
    } or (state == "ready-for-brief" and data["last_review_result"] == "pass")
    _validate_artifact_ref(data["attempt_report_artifact"], report_required, "attempt_report_artifact", label)
    report_forbidden = state == "ready-for-execution" or (
        state == "ready-for-brief" and data["last_review_result"] == "not-run"
    )
    if report_forbidden and data["attempt_report_artifact"] is not None:
        raise AssertionError(f"{label}: attempt_report_artifact must be null before a Report exists")
    _validate_artifact_ref(
        data["last_review_artifact"],
        data["last_review_result"] != "not-run",
        "last_review_artifact",
        label,
    )
    if data["last_review_result"] == "not-run" and data["last_review_artifact"] is not None:
        raise AssertionError(f"{label}: last_review_artifact must be null while Review is not-run")
    _validate_artifact_ref(
        data["final_verification_artifact"],
        data["final_verification"] != "pending",
        "final_verification_artifact",
        label,
    )
    if data["final_verification"] == "pending" and data["final_verification_artifact"] is not None:
        raise AssertionError(f"{label}: final_verification_artifact must be null while pending")
    _validate_artifact_ref(
        data["final_review_artifact"],
        data["final_review_result"] != "pending",
        "final_review_artifact",
        label,
    )
    if data["final_review_result"] == "pending" and data["final_review_artifact"] is not None:
        raise AssertionError(f"{label}: final_review_artifact must be null while pending")
    if state in {"awaiting-final-verification", "complete"} and data["current_batch"] != data["planned_batches"]:
        raise AssertionError(f"{label}: final states require final batch")
    if state in {"needs-fix", "blocked"} and result_tuple[0] == "pass" and data["current_batch"] != data["planned_batches"]:
        raise AssertionError(f"{label}: final-gate failure or block requires final batch")
    _validate_distinct_artifact_paths(data, label)


def validate_decision_source(value: str) -> str:
    if value not in DECISION_SOURCES:
        raise AssertionError("decision_source must use an allowed provenance value")
    return value


def validate_capability_action(profile: str, action: str, ambiguity: bool = False) -> str:
    if profile not in CAPABILITY_PROFILES:
        raise AssertionError("invalid capability profile")
    if ambiguity and profile in {"mechanical-low", "cohesive-medium"}:
        return "BLOCKED"
    if profile == "mechanical-low" and action in BUSINESS_PRODUCTION_ACTIONS:
        return "BLOCKED"
    if profile == "cohesive-medium" and action in {
        "architecture-decision", "openspec-scope-change", "risk-change",
        "acceptance-change", "final-completion",
    }:
        return "BLOCKED"
    return "ALLOW"


def validate_confirmation_lease(lease: dict, context: dict) -> str:
    required = {
        "decision_id", "artifact_revision", "artifact_sha256", "approved_scope",
        "approved_actions", "risk_profile", "decision_source", "owner_instance_id",
        "status", "invalidation_conditions",
    }
    if not isinstance(lease, dict) or set(lease) != required:
        raise AssertionError("Confirmation Lease must contain exactly the typed fields")
    for key in ("decision_id", "approved_scope", "owner_instance_id"):
        if not _is_nonblank(lease[key]):
            raise AssertionError(f"Confirmation Lease {key} must be non-blank")
    _require_positive_int(lease, "artifact_revision", "Confirmation Lease")
    if not isinstance(lease["artifact_sha256"], str) or not re.fullmatch(
        r"[0-9a-f]{64}", lease["artifact_sha256"]
    ):
        raise AssertionError("Confirmation Lease artifact_sha256 must be lowercase SHA-256")
    _validate_string_list(lease["approved_actions"], "approved_actions", "Confirmation Lease")
    _validate_string_list(
        lease["invalidation_conditions"], "invalidation_conditions", "Confirmation Lease"
    )
    if lease["risk_profile"] not in RISK_PROFILES:
        raise AssertionError("Confirmation Lease risk_profile is invalid")
    validate_decision_source(lease["decision_source"])
    if lease["decision_source"] in {"deferred", "revoked"}:
        raise AssertionError("deferred or revoked decision cannot keep a valid Confirmation Lease")
    if lease["status"] != "valid":
        raise AssertionError("Confirmation Lease is not valid")
    action = context.get("action")
    if action in BUSINESS_PRODUCTION_ACTIONS and not context.get("business_authorized", False):
        raise AssertionError("explicit business/production authorization is required")
    invalidated = (
        context.get("artifact_revision") != lease["artifact_revision"]
        or context.get("artifact_sha256") != lease["artifact_sha256"]
        or context.get("scope") != lease["approved_scope"]
        or context.get("risk_profile") != lease["risk_profile"]
        or action not in lease["approved_actions"]
        or any(context.get(flag, False) for flag in (
            "scope_changed", "acceptance_changed", "risk_changed",
            "production_impact_changed", "credentials_changed",
            "external_side_effect_changed", "destructive_git_changed",
            "contradictory_evidence", "user_decision_changed",
        ))
    )
    if invalidated:
        raise AssertionError("Confirmation Lease is invalidated for the current scope/revision/risk")
    return "reuse"


def evaluate_learning_candidate(candidate: dict) -> dict[str, bool]:
    severity = candidate.get("severity")
    scope = candidate.get("scope")
    reproductions = candidate.get("independent_reproductions")
    event_kind = candidate.get("event_kind")
    if severity not in {"low", "medium", "high", "critical"}:
        raise AssertionError("Learning Candidate severity is invalid")
    if scope not in {"task-local", "project-local", "global"}:
        raise AssertionError("Learning Candidate scope is invalid")
    if type(reproductions) is not int or reproductions < 1 or not _is_nonblank(event_kind):
        raise AssertionError("Learning Candidate evidence is invalid")
    severe_event = severity in {"high", "critical"} and event_kind in {
        "security", "integrity", "false-pass",
    }
    proposal_allowed = scope == "global" and (reproductions >= 2 or severe_event)
    implementation_allowed = proposal_allowed and candidate.get("openspec_approval") is True
    return {
        "candidate_created": True,
        "proposal_allowed": proposal_allowed,
        "implementation_allowed": implementation_allowed,
    }


def validate_high_review_evidence(evidence: dict) -> None:
    required = {
        "actual_diff_inspected", "production_wiring_trace", "critical_reruns",
        "independent_probe", "copy_fields", "claims",
    }
    if not isinstance(evidence, dict) or set(evidence) != required:
        raise AssertionError("High Review evidence fields are incomplete")
    if evidence["actual_diff_inspected"] is not True:
        raise AssertionError("High Review must inspect the actual diff")
    _validate_string_list(
        evidence["production_wiring_trace"], "production_wiring_trace", "High Review"
    )
    _validate_string_list(evidence["critical_reruns"], "critical_reruns", "High Review")
    probe = evidence["independent_probe"]
    if not isinstance(probe, dict) or set(probe) != {"kind", "command", "result"}:
        raise AssertionError("High Review requires an independent adversarial or business-chain probe")
    if probe["kind"] not in {"adversarial", "business-chain"} or not _is_nonblank(probe["command"]):
        raise AssertionError("High Review independent probe is invalid")
    copy_fields = evidence["copy_fields"]
    if not isinstance(copy_fields, dict) or set(copy_fields) != {"expected", "observed"}:
        raise AssertionError("High Review copy-field evidence is invalid")
    expected = copy_fields["expected"]
    observed = copy_fields["observed"]
    if not isinstance(expected, list) or not isinstance(observed, list) or set(expected) - set(observed):
        raise AssertionError("High Review detected copy-field loss")
    claims = evidence["claims"]
    if not isinstance(claims, list):
        raise AssertionError("High Review claims must be a list")
    for claim in claims:
        if not isinstance(claim, dict) or set(claim) != {"claim", "mechanism", "evidence"}:
            raise AssertionError("High Review claim-to-mechanism entry is invalid")
        if not all(_is_nonblank(claim[key]) for key in ("claim", "mechanism", "evidence")):
            raise AssertionError("High Review claim-to-mechanism support is required")


def _validate_assignment(
    value,
    field: str,
    expected_role: str,
    allowed_profiles: set[str],
    allowed_products: set[str],
    label: str,
) -> None:
    required = {"agent_product", "agent_instance_id", "agent_role", "capability_profile"}
    if not isinstance(value, dict) or set(value) != required:
        raise AssertionError(f"{label}: {field} must contain exactly product/instance/role/profile")
    if value["agent_product"] not in allowed_products:
        raise AssertionError(f"{label}: {field} has invalid agent_product")
    if not isinstance(value["agent_instance_id"], str) or not re.fullmatch(
        r"[a-z0-9][a-z0-9._-]{2,63}", value["agent_instance_id"]
    ):
        raise AssertionError(f"{label}: {field} has invalid agent_instance_id")
    if value["agent_role"] != expected_role:
        raise AssertionError(f"{label}: {field} has invalid agent_role")
    if value["capability_profile"] not in allowed_profiles:
        raise AssertionError(f"{label}: {field} has invalid capability_profile")


REVIEW_PURPOSE_FIELDS = {"object", "decision"}
INDEPENDENCE_FIELDS = {"kind", "distinct_from"}
REVIEWER_ASSIGNMENT_FIELDS = {
    "review_purpose", "agent_product", "agent_instance_id", "agent_role",
    "capability_profile", "independence_requirement", "result_authority",
}


def _validate_review_purpose(value, label: str) -> None:
    if not isinstance(value, dict) or set(value) != REVIEW_PURPOSE_FIELDS:
        raise AssertionError(f"{label}: review_purpose must contain exactly object/decision")
    if not all(_is_nonblank(value[key]) for key in REVIEW_PURPOSE_FIELDS):
        raise AssertionError(f"{label}: review_purpose values must be non-blank")


def _validate_independence(value, expected: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != INDEPENDENCE_FIELDS:
        raise AssertionError(f"{label}: independence_requirement fields are invalid")
    if value["kind"] != "distinct-contract-instance":
        raise AssertionError(f"{label}: independence kind is invalid")
    distinct_from = value["distinct_from"]
    if (
        not isinstance(distinct_from, list)
        or not all(isinstance(item, str) for item in distinct_from)
        or len(distinct_from) != len(set(distinct_from))
        or set(distinct_from) != expected
    ):
        raise AssertionError(f"{label}: independence targets are invalid")


def _validate_schema6_reviewer_assignment(data: dict, label: str) -> None:
    reviewer = data["reviewer_assignment"]
    if not isinstance(reviewer, dict) or set(reviewer) != REVIEWER_ASSIGNMENT_FIELDS:
        raise AssertionError(
            f"{label}: reviewer_assignment must contain exactly the governed seven fields"
        )
    _validate_review_purpose(reviewer["review_purpose"], label)
    if reviewer["result_authority"] != "governed-review-evidence":
        raise AssertionError(f"{label}: reviewer_assignment result_authority is invalid")

    owner = data["control_plane_owner"]
    executor = data["executor_assignment"]
    reason = data["independent_review_not_applicable_reason"]
    identity_fields = {
        "agent_product", "agent_instance_id", "agent_role", "capability_profile"
    }
    reviewer_identity = {key: reviewer[key] for key in identity_fields}
    if data["risk_profile"] in {"standard", "strict"}:
        _validate_assignment(
            reviewer_identity,
            "reviewer_assignment",
            "independent-reviewer",
            {"control-plane-high"},
            SCHEMA6_AGENT_PRODUCTS,
            label,
        )
        _validate_independence(
            reviewer["independence_requirement"],
            {"control_plane_owner", "executor_assignment"},
            label,
        )
        if reason is not None:
            raise AssertionError(f"{label}: standard/strict reviewer reason must be null")
        instance_ids = {
            owner["agent_instance_id"],
            executor["agent_instance_id"],
            reviewer["agent_instance_id"],
        }
        if len(instance_ids) != 3:
            raise AssertionError(
                f"{label}: control-plane, executor, and reviewer instance IDs must differ"
            )
    else:
        _validate_assignment(
            reviewer_identity,
            "reviewer_assignment",
            owner["agent_role"],
            {owner["capability_profile"]},
            SCHEMA6_AGENT_PRODUCTS,
            label,
        )
        _validate_independence(
            reviewer["independence_requirement"], {"executor_assignment"}, label
        )
        if any(reviewer[key] != owner[key] for key in identity_fields):
            raise AssertionError(
                f"{label}: compact reviewer identity must equal the control-plane owner"
            )
        if reviewer["agent_instance_id"] == executor["agent_instance_id"]:
            raise AssertionError(f"{label}: compact executor instance must be distinct")
        if not _is_nonblank(reason):
            raise AssertionError(f"{label}: compact reviewer requires a non-blank reason")


def _validate_confirmation_lease_ref(value, label: str) -> None:
    if not isinstance(value, dict) or set(value) != {"decision_id", "path", "sha256"}:
        raise AssertionError(f"{label}: confirmation_lease must be a decision-id/path/sha256 mapping")
    if not _is_nonblank(value["decision_id"]):
        raise AssertionError(f"{label}: confirmation_lease.decision_id must be non-blank")
    _validate_artifact_ref({"path": value["path"], "sha256": value["sha256"]}, True, "confirmation_lease", label)


def _validate_schema5_handoff_contract(data: dict, label: str) -> None:
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA5_VERSION:
        raise AssertionError(f"{label}: legacy schema_version must be {SCHEMA5_VERSION}")
    required = {
        "schema_version", "change_id", "mode", "approval_status",
        "risk_profile", "batch_profile", "current_batch", "planned_batches",
        "attempt", "contract_revision", "lifecycle_state",
        "attempt_report_artifact", "last_review_result", "last_review_artifact",
        "blocked_reason", "blocker_owner", "resume_condition",
        "final_verification", "final_verification_artifact",
        "final_review_result", "final_review_artifact", "executor", "governor",
        "control_plane_owner", "executor_assignment", "independent_reviewer_assignment",
        "independent_review_not_applicable_reason", "decision_source",
        "confirmation_lease", "confirmation_lease_status", "next_owner",
        "step_critical", "final_critical",
        "business_acceptance", "stop_conditions", "verification_strategy",
        "readonly_fields",
    }
    missing = sorted(required - set(data))
    unexpected = sorted(set(data) - required)
    if missing:
        raise AssertionError(f"{label}: missing contract fields: {missing}")
    if unexpected:
        raise AssertionError(f"{label}: unexpected contract fields: {unexpected}")
    legacy = dict(data)
    legacy.update({
        "schema_version": LEGACY_SCHEMA_VERSION,
        # Reuse only schema-4 lifecycle checks; schema-5 assignments are
        # validated independently below and may use the Codex product.
        "executor_agent": "antigravity-cli",
        "independent_reviewer_agent": (
            "not-applicable" if data["independent_reviewer_assignment"] is None
            else "grok-cli"
        ),
        "decision_owner": "codex",
    })
    for key in (
        "control_plane_owner", "executor_assignment", "independent_reviewer_assignment",
        "decision_source", "confirmation_lease", "confirmation_lease_status",
    ):
        legacy.pop(key, None)
    legacy["readonly_fields"] = list(LEGACY_IMMUTABLE_FIELDS)
    _validate_schema4_handoff_contract(legacy, label)
    _validate_assignment(
        data["control_plane_owner"], "control_plane_owner", "control-plane",
        {"control-plane-high"}, SCHEMA5_AGENT_PRODUCTS, label,
    )
    if data["control_plane_owner"]["agent_product"] != "codex":
        raise AssertionError(f"{label}: schema-5 control_plane_owner must use Codex")
    _validate_assignment(
        data["executor_assignment"], "executor_assignment", "executor",
        CAPABILITY_PROFILES, SCHEMA5_AGENT_PRODUCTS, label,
    )
    reviewer = data["independent_reviewer_assignment"]
    if reviewer is None:
        if data["risk_profile"] != "compact" or not _is_nonblank(data["independent_review_not_applicable_reason"]):
            raise AssertionError(f"{label}: reviewer may be not-applicable only for compact with a reason")
    else:
        _validate_assignment(
            reviewer, "independent_reviewer_assignment", "independent-reviewer",
            {"control-plane-high"}, SCHEMA5_AGENT_PRODUCTS, label,
        )
        if data["independent_review_not_applicable_reason"] is not None:
            raise AssertionError(f"{label}: reviewer reason must be null when a reviewer is assigned")
        if reviewer["agent_instance_id"] == data["executor_assignment"]["agent_instance_id"]:
            raise AssertionError(f"{label}: executor and independent reviewer instance IDs must differ")
    instance_ids = [
        data["control_plane_owner"]["agent_instance_id"],
        data["executor_assignment"]["agent_instance_id"],
    ] + ([] if reviewer is None else [reviewer["agent_instance_id"]])
    if len(instance_ids) != len(set(instance_ids)):
        raise AssertionError(f"{label}: control-plane, executor, and reviewer instance IDs must differ")
    validate_decision_source(data["decision_source"])
    _validate_confirmation_lease_ref(data["confirmation_lease"], label)
    if data["confirmation_lease_status"] not in {"valid", "deferred", "revoked"}:
        raise AssertionError(f"{label}: invalid confirmation_lease_status")
    if data["confirmation_lease_status"] != "valid" and data["lifecycle_state"] != "blocked":
        raise AssertionError(f"{label}: deferred/revoked Lease requires blocked lifecycle")
    readonly = data["readonly_fields"]
    if not isinstance(readonly, list) or len(readonly) != len(set(readonly)) or set(readonly) != SCHEMA5_IMMUTABLE_FIELDS:
        raise AssertionError(f"{label}: readonly_fields must exactly match schema-5 immutable fields")


def _validate_schema6_handoff_contract(data: dict, label: str) -> None:
    schema5_required = {
        "schema_version", "change_id", "mode", "approval_status",
        "risk_profile", "batch_profile", "current_batch", "planned_batches",
        "attempt", "contract_revision", "lifecycle_state",
        "attempt_report_artifact", "last_review_result", "last_review_artifact",
        "blocked_reason", "blocker_owner", "resume_condition",
        "final_verification", "final_verification_artifact",
        "final_review_result", "final_review_artifact", "executor", "governor",
        "control_plane_owner", "executor_assignment", "independent_reviewer_assignment",
        "independent_review_not_applicable_reason", "decision_source",
        "confirmation_lease", "confirmation_lease_status", "next_owner",
        "step_critical", "final_critical", "business_acceptance",
        "stop_conditions", "verification_strategy", "readonly_fields",
    }
    required = (
        schema5_required - {"independent_reviewer_assignment"} | {"reviewer_assignment"}
    )
    missing = sorted(required - set(data))
    unexpected = sorted(set(data) - required)
    if missing:
        raise AssertionError(f"{label}: missing contract fields: {missing}")
    if unexpected:
        raise AssertionError(f"{label}: unexpected contract fields: {unexpected}")

    common = dict(data)
    common.update({
        "schema_version": LEGACY_SCHEMA_VERSION,
        "executor_agent": "antigravity-cli",
        "independent_reviewer_agent": (
            "not-applicable" if data["risk_profile"] == "compact" else "grok-cli"
        ),
        "decision_owner": "codex",
    })
    for key in (
        "control_plane_owner", "executor_assignment", "reviewer_assignment",
        "decision_source", "confirmation_lease", "confirmation_lease_status",
    ):
        common.pop(key, None)
    common["readonly_fields"] = list(LEGACY_IMMUTABLE_FIELDS)
    _validate_schema4_handoff_contract(common, label)

    _validate_assignment(
        data["control_plane_owner"],
        "control_plane_owner",
        "control-plane",
        {"control-plane-high"},
        SCHEMA6_AGENT_PRODUCTS,
        label,
    )
    if data["control_plane_owner"]["agent_product"] != "codex":
        raise AssertionError(f"{label}: current control_plane_owner must use Codex")
    _validate_assignment(
        data["executor_assignment"],
        "executor_assignment",
        "executor",
        CAPABILITY_PROFILES,
        SCHEMA6_AGENT_PRODUCTS,
        label,
    )
    _validate_schema6_reviewer_assignment(data, label)
    validate_decision_source(data["decision_source"])
    _validate_confirmation_lease_ref(data["confirmation_lease"], label)
    if data["confirmation_lease_status"] not in {"valid", "deferred", "revoked"}:
        raise AssertionError(f"{label}: invalid confirmation_lease_status")
    if (
        data["confirmation_lease_status"] != "valid"
        and data["lifecycle_state"] != "blocked"
    ):
        raise AssertionError(f"{label}: deferred/revoked Lease requires blocked lifecycle")
    readonly = data["readonly_fields"]
    if (
        not isinstance(readonly, list)
        or len(readonly) != len(set(readonly))
        or set(readonly) != SCHEMA6_IMMUTABLE_FIELDS
    ):
        raise AssertionError(
            f"{label}: readonly_fields must exactly match schema-6 immutable fields"
        )


def validate_handoff_contract(data: dict, label: str) -> None:
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        raise AssertionError(
            f"{label}: current Handoff schema_version must be {SCHEMA_VERSION}"
        )
    _validate_schema6_handoff_contract(data, label)


def validate_legacy_handoff_contract(data: dict, label: str) -> None:
    schema_version = data.get("schema_version") if isinstance(data, dict) else None
    if schema_version == LEGACY_SCHEMA_VERSION:
        _validate_schema4_handoff_contract(data, label)
    elif schema_version == SCHEMA5_VERSION:
        _validate_schema5_handoff_contract(data, label)
    else:
        raise AssertionError(f"{label}: legacy schema must be 4 or 5")


def _transition_artifact_field(before: dict, after: dict) -> str | None:
    before_state = before["lifecycle_state"]
    after_state = after["lifecycle_state"]
    if before_state == "ready-for-execution" and after_state == "ready-for-review":
        return "attempt_report_artifact"
    if before_state == "ready-for-review":
        return "last_review_artifact"
    if before_state in {"ready-for-brief", "ready-for-execution", "needs-fix"} and after_state == "blocked":
        return "last_review_artifact"
    if before_state == "awaiting-final-verification":
        if _result_tuple(before) == ("pass", "pending", "pending") and after_state in {
            "awaiting-final-verification", "needs-fix", "blocked",
        }:
            return "final_verification_artifact"
        if _result_tuple(before) == ("pass", "pass", "pending") and after_state in {
            "complete", "needs-fix", "blocked",
        }:
            return "final_review_artifact"
    return None


def _resolve_hashed_artifact(ref: dict, root: Path, key: str, label: str) -> tuple[Path, str]:
    _validate_artifact_ref(ref, True, key, label)
    target = (root / ref["path"]).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise AssertionError(f"{label}: {key} resolves outside artifact root") from exc
    if not target.is_file() or target.stat().st_size == 0:
        raise AssertionError(f"{label}: {key} file must exist and be non-empty: {target}")
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    if digest != ref["sha256"]:
        raise AssertionError(f"{label}: {key} sha256 mismatch")
    return target, target.read_text(encoding="utf-8")


def _validate_confirmation_lease_artifact(
    data: dict, artifact_root: Path, label: str
) -> None:
    root = artifact_root.resolve()
    if not root.is_dir():
        raise AssertionError(f"{label}: artifact root is not a directory: {root}")
    ref = data["confirmation_lease"]
    target, text = _resolve_hashed_artifact(
        {"path": ref["path"], "sha256": ref["sha256"]},
        root,
        "confirmation_lease",
        label,
    )
    lease = extract_confirmation_lease(text, f"{label}:{target}")
    action = lease.get("approved_actions", [None])
    action = action[0] if isinstance(action, list) and action else None
    validate_confirmation_lease(lease, {
        "action": action,
        "artifact_revision": lease.get("artifact_revision"),
        "artifact_sha256": lease.get("artifact_sha256"),
        "scope": lease.get("approved_scope"),
        "risk_profile": lease.get("risk_profile"),
        "platform_authorized": True,
        "business_authorized": True,
    })
    if lease["decision_id"] != ref["decision_id"]:
        raise AssertionError(f"{label}: Confirmation Lease decision_id does not match canonical status")
    if lease["owner_instance_id"] != data["control_plane_owner"]["agent_instance_id"]:
        raise AssertionError(f"{label}: Confirmation Lease owner_instance_id does not match control plane")
    if lease["decision_source"] != data["decision_source"]:
        raise AssertionError(f"{label}: Confirmation Lease decision_source does not match canonical status")
    if lease["risk_profile"] != data["risk_profile"]:
        raise AssertionError(f"{label}: Confirmation Lease risk_profile does not match canonical status")


def validate_confirmation_lease_artifact(
    data: dict, artifact_root: Path, label: str
) -> None:
    validate_handoff_contract(data, f"{label}:current-parent")
    _validate_confirmation_lease_artifact(data, artifact_root, label)


def _validate_legacy_confirmation_lease_artifact(
    data: dict, artifact_root: Path, label: str
) -> None:
    validate_legacy_handoff_contract(data, f"{label}:legacy-parent")
    if data["schema_version"] == SCHEMA5_VERSION:
        _validate_confirmation_lease_artifact(data, artifact_root, label)


def validate_high_review_artifact_text(text: str, label: str) -> None:
    lowered = text.lower()
    groups = (
        ("actual files and complete diff", "actual diff"),
        ("production wiring trace", "production wiring"),
        ("critical reruns", "critical rerun"),
        ("claim-to-mechanism",),
        ("independent adversarial probe", "independent business-chain probe", "independent probe"),
    )
    for alternatives in groups:
        if not any(value in lowered for value in alternatives):
            raise AssertionError(
                f"{label}: High Review requires actual diff, production wiring, critical reruns, "
                "claim-to-mechanism, and an independent probe"
            )


def inventory_legacy_handoffs(roots: list[Path]) -> list[dict]:
    records: list[dict] = []
    seen: set[Path] = set()
    for raw_root in roots:
        root = Path(raw_root).resolve()
        if not root.is_dir():
            raise AssertionError(f"legacy inventory root is not a directory: {root}")
        for status in root.rglob("status.md"):
            if status.is_symlink():
                raise AssertionError(f"legacy inventory status may not be a symlink: {status}")
            resolved = status.resolve()
            try:
                resolved.relative_to(root)
            except ValueError as exc:
                raise AssertionError(
                    f"legacy inventory status resolves outside root: {status}"
                ) from exc
            if resolved in seen:
                continue
            seen.add(resolved)
            text = read(resolved)
            if START not in text and END not in text:
                continue
            data = extract_handoff_contract(text, str(resolved))
            if data.get("schema_version") not in {
                LEGACY_SCHEMA_VERSION, SCHEMA5_VERSION,
            }:
                continue
            validate_legacy_handoff_contract(data, str(resolved))
            lifecycle_state = data["lifecycle_state"]
            records.append({
                "path": str(resolved),
                "schema_version": data["schema_version"],
                "lifecycle_state": lifecycle_state,
                "sha256": hashlib.sha256(resolved.read_bytes()).hexdigest(),
                "drain_status": (
                    "complete-history" if lifecycle_state == "complete" else "active"
                ),
            })
    return sorted(records, key=lambda record: record["path"])


def inventory_active_schema4_statuses(roots: list[Path]) -> list[Path]:
    """Compatibility view for frozen schema-4 unit regressions only."""
    return [
        Path(record["path"])
        for record in inventory_legacy_handoffs(roots)
        if record["schema_version"] == LEGACY_SCHEMA_VERSION
        and record["drain_status"] == "active"
    ]


def _write_exclusive_json(path: Path, payload: dict) -> None:
    target = path.resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(target, flags, 0o600)
    try:
        body = (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()
        os.write(descriptor, body)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    os.chmod(target, 0o600)
    directory_fd = os.open(target.parent, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def _validate_evidence_artifacts(
    data: dict,
    artifact_root: Path,
    label: str,
    previous: dict | None = None,
    previous_status_sha256: str | None = None,
    *,
    legacy_parent: bool = False,
) -> None:
    if legacy_parent:
        validate_legacy_handoff_contract(data, f"{label}:legacy-parent")
    else:
        validate_handoff_contract(data, f"{label}:current-parent")
    root = artifact_root.resolve()
    if not root.is_dir():
        raise AssertionError(f"{label}: artifact root is not a directory: {root}")
    if legacy_parent:
        _validate_legacy_confirmation_lease_artifact(data, root, label)
    else:
        validate_confirmation_lease_artifact(data, root, label)
    manifests: dict[str, dict] = {}
    for key in ARTIFACT_FIELDS:
        ref = data.get(key)
        if ref is None:
            continue
        target, artifact_text = _resolve_hashed_artifact(ref, root, key, label)
        manifest = extract_evidence_manifest(artifact_text, f"{label}:{key}")
        if data["schema_version"] == LEGACY_SCHEMA_VERSION:
            expected_fields = {
                "evidence_schema_version", "evidence_role", "evidence_result", "change_id",
                "current_batch", "attempt", "contract_revision", "canonical_sha256",
                "agent_identity", "agent_role",
            }
            expected_evidence_version = LEGACY_EVIDENCE_SCHEMA_VERSION
        else:
            expected_fields = {
                "evidence_schema_version", "evidence_role", "evidence_result", "change_id",
                "current_batch", "attempt", "contract_revision", "canonical_sha256",
                "agent_product", "agent_instance_id", "agent_role", "capability_profile",
            }
            expected_evidence_version = EVIDENCE_SCHEMA_VERSION
        if set(manifest) != expected_fields:
            raise AssertionError(
                f"{label}: {key} evidence manifest must contain exactly {sorted(expected_fields)}"
            )
        if manifest["evidence_schema_version"] != expected_evidence_version:
            raise AssertionError(f"{label}: {key} has invalid evidence schema version")
        if manifest["evidence_role"] not in EVIDENCE_ROLES:
            raise AssertionError(f"{label}: {key} has invalid evidence role")
        if manifest["evidence_result"] not in EVIDENCE_RESULTS:
            raise AssertionError(f"{label}: {key} has invalid evidence result")
        if data["schema_version"] == LEGACY_SCHEMA_VERSION:
            if manifest["agent_identity"] not in SCHEMA5_AGENT_PRODUCTS:
                raise AssertionError(f"{label}: {key} has invalid agent identity")
            if manifest["agent_role"] not in AGENT_ROLES:
                raise AssertionError(f"{label}: {key} has invalid agent role")
        else:
            allowed_products = (
                SCHEMA6_AGENT_PRODUCTS
                if data["schema_version"] == SCHEMA_VERSION
                else SCHEMA5_AGENT_PRODUCTS
            )
            if manifest["agent_product"] not in allowed_products:
                raise AssertionError(f"{label}: {key} has invalid agent_product")
            if not _is_nonblank(manifest["agent_instance_id"]):
                raise AssertionError(f"{label}: {key} has invalid agent_instance_id")
            allowed_roles = (
                SCHEMA6_AGENT_ROLES
                if data["schema_version"] == SCHEMA_VERSION
                else SCHEMA5_AGENT_ROLES
            )
            if manifest["agent_role"] not in allowed_roles:
                raise AssertionError(f"{label}: {key} has invalid agent_role")
            if manifest["capability_profile"] not in CAPABILITY_PROFILES:
                raise AssertionError(f"{label}: {key} has invalid capability_profile")
        if manifest["change_id"] != data["change_id"]:
            raise AssertionError(f"{label}: {key} change_id does not match canonical status")
        for coordinate in ("current_batch", "attempt", "contract_revision"):
            _require_positive_int(manifest, coordinate, f"{label}:{key}")
        if not isinstance(manifest["canonical_sha256"], str) or not re.fullmatch(
            r"[0-9a-f]{64}", manifest["canonical_sha256"]
        ):
            raise AssertionError(f"{label}: {key} canonical_sha256 must be 64 lowercase hex characters")
        if manifest["contract_revision"] >= data["contract_revision"]:
            raise AssertionError(f"{label}: {key} must reference an earlier canonical revision")
        manifests[key] = manifest

    batch_blocked = (
        data["lifecycle_state"] == "blocked"
        and _result_tuple(data) == ("blocked", "pending", "pending")
    )
    role_rules = {
        "attempt_report_artifact": (
            {"attempt-report", "timeout-audit"} if batch_blocked else {"attempt-report"}
        ),
        "last_review_artifact": (
            {"batch-review", "preflight-review", "timeout-audit"}
            if batch_blocked else {"batch-review"}
        ),
        "final_verification_artifact": {"final-verification"},
        "final_review_artifact": {"final-review"},
    }
    result_fields = {
        "last_review_artifact": "last_review_result",
        "final_verification_artifact": "final_verification",
        "final_review_artifact": "final_review_result",
    }
    for key, manifest in manifests.items():
        if manifest["evidence_role"] not in role_rules[key]:
            raise AssertionError(f"{label}: {key} evidence role does not match artifact field")
        result_field = result_fields.get(key)
        if result_field and manifest["evidence_result"] != data[result_field]:
            raise AssertionError(f"{label}: {key} evidence result does not match canonical status")
        if (
            data["schema_version"] == SCHEMA_VERSION
            and data["risk_profile"] in {"standard", "strict"}
            and manifest["evidence_role"] in {"batch-review", "final-review"}
        ):
            validate_high_review_artifact_text(
                (root / data[key]["path"]).read_text(encoding="utf-8"),
                f"{label}:{key}",
            )
        if manifest["evidence_role"] in {"preflight-review", "timeout-audit"} and (
            not batch_blocked or manifest["evidence_result"] != "blocked"
        ):
            raise AssertionError(
                f"{label}: {manifest['evidence_role']} is only valid for a blocked batch state"
            )

        evidence_role = manifest["evidence_role"]
        if data["schema_version"] == LEGACY_SCHEMA_VERSION:
            if evidence_role == "attempt-report":
                expected_identity_role = (data["executor_agent"], "executor")
            elif evidence_role == "batch-review":
                if data["independent_reviewer_agent"] == "not-applicable":
                    expected_identity_role = (data["decision_owner"], "decision-owner")
                else:
                    expected_identity_role = (
                        data["independent_reviewer_agent"], "independent-reviewer",
                    )
            else:
                expected_identity_role = (data["decision_owner"], "decision-owner")
            actual_identity_role = (manifest["agent_identity"], manifest["agent_role"])
        else:
            if evidence_role == "attempt-report":
                assignment = data["executor_assignment"]
            elif evidence_role == "batch-review":
                assignment = (
                    data["reviewer_assignment"]
                    if data["schema_version"] == SCHEMA_VERSION
                    else data["independent_reviewer_assignment"]
                )
                if assignment is None:
                    assignment = data["control_plane_owner"]
            else:
                assignment = data["control_plane_owner"]
            expected_identity_role = (
                assignment["agent_product"], assignment["agent_instance_id"],
                assignment["agent_role"], assignment["capability_profile"],
            )
            actual_identity_role = (
                manifest["agent_product"], manifest["agent_instance_id"],
                manifest["agent_role"], manifest["capability_profile"],
            )
        if actual_identity_role != expected_identity_role:
            raise AssertionError(
                f"{label}: {key} agent identity/role/profile does not match the canonical assignment"
            )

    expected_batch = data["current_batch"]
    if data["lifecycle_state"] == "ready-for-brief" and data["last_review_result"] == "pass":
        expected_batch -= 1
    if expected_batch < 1:
        raise AssertionError(f"{label}: completed-batch evidence has no prior batch")
    for key, manifest in manifests.items():
        if manifest["current_batch"] != expected_batch:
            raise AssertionError(f"{label}: {key} does not belong to the required batch")
    if data["lifecycle_state"] == "ready-for-brief" and data["last_review_result"] == "pass":
        attempts = {manifest["attempt"] for manifest in manifests.values()}
        if len(attempts) != 1:
            raise AssertionError(f"{label}: completed batch artifacts must bind one attempt")
    else:
        expected_attempt = data["attempt"] - 1 if data["lifecycle_state"] == "needs-fix" else data["attempt"]
        if expected_attempt < 1:
            raise AssertionError(f"{label}: needs-fix evidence requires a prior attempt")
        for key, manifest in manifests.items():
            if manifest["attempt"] != expected_attempt:
                raise AssertionError(f"{label}: {key} does not belong to the required attempt")

    report_manifest = manifests.get("attempt_report_artifact")
    review_manifest = manifests.get("last_review_artifact")
    if report_manifest and review_manifest and review_manifest["evidence_role"] == "batch-review":
        if report_manifest["contract_revision"] >= review_manifest["contract_revision"]:
            raise AssertionError(f"{label}: batch Review must follow the Report source revision")
    verification_manifest = manifests.get("final_verification_artifact")
    final_review_manifest = manifests.get("final_review_artifact")
    if verification_manifest and final_review_manifest:
        if verification_manifest["contract_revision"] >= final_review_manifest["contract_revision"]:
            raise AssertionError(f"{label}: final Review must follow final verification in a later revision")

    report_ref = data.get("attempt_report_artifact")
    review_ref = data.get("last_review_artifact")
    if report_ref is not None and review_ref is not None and report_ref["path"] == review_ref["path"]:
        if report_ref != review_ref or manifests["attempt_report_artifact"]["evidence_role"] != "timeout-audit":
            raise AssertionError(
                f"{label}: only one identical timeout-audit may serve as Report and Review evidence"
            )

    if previous is not None:
        if previous_status_sha256 is None or not re.fullmatch(r"[0-9a-f]{64}", previous_status_sha256):
            raise AssertionError(f"{label}: previous canonical status SHA-256 is required")
        _validate_transition(
            previous,
            data,
            f"{label}:previous-transition",
            legacy_parent=legacy_parent,
        )
        transition_key = _transition_artifact_field(previous, data)
        if transition_key is not None:
            manifest = manifests.get(transition_key)
            if manifest is None:
                raise AssertionError(f"{label}: transition requires {transition_key}")
            if manifest["contract_revision"] != previous["contract_revision"]:
                raise AssertionError(f"{label}: transition evidence has the wrong source revision")
            if manifest["canonical_sha256"] != previous_status_sha256:
                raise AssertionError(f"{label}: transition evidence has the wrong canonical SHA-256")
            if manifest["current_batch"] != previous["current_batch"]:
                raise AssertionError(f"{label}: transition evidence has the wrong source batch")
            if manifest["attempt"] != previous["attempt"]:
                raise AssertionError(f"{label}: transition evidence has the wrong source attempt")
    elif data["lifecycle_state"] == "complete":
        raise AssertionError(f"{label}: complete runtime validation requires previous canonical status")


def validate_evidence_artifacts(
    data: dict,
    artifact_root: Path,
    label: str,
    previous: dict | None = None,
    previous_status_sha256: str | None = None,
) -> None:
    _validate_evidence_artifacts(
        data,
        artifact_root,
        label,
        previous,
        previous_status_sha256,
        legacy_parent=False,
    )


def _validate_legacy_evidence_artifacts(
    data: dict,
    artifact_root: Path,
    label: str,
    previous: dict | None = None,
    previous_status_sha256: str | None = None,
) -> None:
    _validate_evidence_artifacts(
        data,
        artifact_root,
        label,
        previous,
        previous_status_sha256,
        legacy_parent=True,
    )


def _validate_transition(
    before: dict,
    after: dict,
    label: str,
    *,
    legacy_parent: bool,
) -> None:
    contract_validator = (
        validate_legacy_handoff_contract if legacy_parent else validate_handoff_contract
    )
    contract_validator(before, f"{label}:before")
    if not isinstance(after, dict):
        contract_validator(after, f"{label}:after")
    if before["schema_version"] != after["schema_version"]:
        raise AssertionError(f"{label}: schema version cannot change in place")
    if legacy_parent:
        immutable_fields = (
            LEGACY_IMMUTABLE_FIELDS
            if before["schema_version"] == LEGACY_SCHEMA_VERSION
            else SCHEMA5_IMMUTABLE_FIELDS
        )
    else:
        immutable_fields = SCHEMA6_IMMUTABLE_FIELDS
    for key in immutable_fields:
        if key not in after or before[key] != after[key]:
            raise AssertionError(f"{label}: readonly field changed: {key}")
    contract_validator(after, f"{label}:after")
    if not legacy_parent or before["schema_version"] == SCHEMA5_VERSION:
        before_lease_status = before["confirmation_lease_status"]
        after_lease_status = after["confirmation_lease_status"]
        if before_lease_status in {"deferred", "revoked"} and after_lease_status != before_lease_status:
            raise AssertionError(f"{label}: deferred/revoked Lease cannot be reactivated; create a new contract and Lease")
        if before_lease_status == "valid" and after_lease_status in {"deferred", "revoked"}:
            if after["lifecycle_state"] != "blocked":
                raise AssertionError(f"{label}: deferred/revoked Lease must transition to blocked")
        elif after_lease_status != before_lease_status:
            raise AssertionError(f"{label}: invalid confirmation_lease_status transition")
    current_state = before["lifecycle_state"]
    next_state = after["lifecycle_state"]
    if current_state == "complete":
        raise AssertionError(f"{label}: complete is terminal")
    if after["contract_revision"] != before["contract_revision"] + 1:
        raise AssertionError(f"{label}: contract_revision must increment by one")
    if next_state not in ALLOWED_TRANSITIONS[current_state]:
        raise AssertionError(f"{label}: invalid lifecycle transition")
    if next_state in {"needs-fix", "blocked"} and after["current_batch"] != before["current_batch"]:
        raise AssertionError(f"{label}: FAIL/BLOCKED must stay on the same batch")
    if current_state == "blocked" and next_state == "blocked":
        if after["current_batch"] != before["current_batch"] or after["attempt"] != before["attempt"]:
            raise AssertionError(f"{label}: blocked self-transition must keep batch and attempt")
        if _result_tuple(after) != _result_tuple(before):
            raise AssertionError(f"{label}: blocked self-transition must keep the result tuple")
        for key in ARTIFACT_FIELDS:
            if after[key] != before[key]:
                raise AssertionError(f"{label}: blocked self-transition cannot rewrite evidence: {key}")
    elif next_state == "blocked":
        if current_state == "awaiting-final-verification":
            before_tuple = _result_tuple(before)
            after_tuple = _result_tuple(after)
            expected = {
                ("pass", "pending", "pending"): ("pass", "blocked", "pending"),
                ("pass", "pass", "pending"): ("pass", "pass", "blocked"),
            }
            if expected.get(before_tuple) != after_tuple:
                raise AssertionError(
                    f"{label}: final Review requires persisted final verification before BLOCKED"
                )
        elif _result_tuple(after) != ("blocked", "pending", "pending"):
            raise AssertionError(f"{label}: batch work must use the batch BLOCKED tuple")

    if current_state == "ready-for-review" and next_state == "ready-for-brief":
        if before["current_batch"] >= before["planned_batches"]:
            raise AssertionError(f"{label}: final PASS must hand back to router")
        if after["current_batch"] != before["current_batch"] + 1 or after["attempt"] != 1:
            raise AssertionError(f"{label}: non-final PASS must advance one batch and reset attempt")
        if _result_tuple(after) != ("pass", "pending", "pending"):
            raise AssertionError(f"{label}: non-final promotion requires Review PASS and review evidence")
    elif next_state == "needs-fix":
        if after["current_batch"] != before["current_batch"] or after["attempt"] != before["attempt"] + 1:
            raise AssertionError(f"{label}: FAIL must stay on the same batch and increment attempt")
    elif current_state == "blocked" and next_state != "blocked":
        if after["current_batch"] != before["current_batch"]:
            raise AssertionError(f"{label}: resumed work must stay on the same batch")
        if next_state == "awaiting-final-verification":
            if after["attempt"] != before["attempt"]:
                raise AssertionError(f"{label}: final-gate recovery keeps the implementation attempt")
            before_tuple = _result_tuple(before)
            after_tuple = _result_tuple(after)
            valid_resume = (
                before_tuple == ("pass", "blocked", "pending")
                and after_tuple == ("pass", "pending", "pending")
                and after["final_verification_artifact"] is None
            ) or (
                before_tuple == ("pass", "pass", "blocked")
                and after_tuple == ("pass", "pass", "pending")
                and after["final_verification_artifact"] == before["final_verification_artifact"]
            )
            if not valid_resume:
                raise AssertionError(f"{label}: invalid final-gate recovery")
            for key in ("attempt_report_artifact", "last_review_artifact"):
                if after[key] != before[key]:
                    raise AssertionError(f"{label}: final-gate recovery cannot rewrite {key}")
        elif after["attempt"] != before["attempt"] + 1:
            raise AssertionError(f"{label}: batch recovery must use a fresh attempt")
    elif after["current_batch"] != before["current_batch"] or after["attempt"] != before["attempt"]:
        raise AssertionError(f"{label}: transition must keep the same batch and attempt")

    if current_state == "ready-for-review" and next_state == "awaiting-final-verification":
        if before["current_batch"] != before["planned_batches"]:
            raise AssertionError(f"{label}: only final batch can hand back")
        if _result_tuple(after) != ("pass", "pending", "pending"):
            raise AssertionError(f"{label}: final handback requires batch Review PASS")
    if current_state == "ready-for-review" and next_state in {
        "ready-for-brief", "needs-fix", "blocked", "awaiting-final-verification",
    }:
        expected_tuples = {
            "ready-for-brief": ("pass", "pending", "pending"),
            "needs-fix": ("fail", "pending", "pending"),
            "blocked": ("blocked", "pending", "pending"),
            "awaiting-final-verification": ("pass", "pending", "pending"),
        }
        if _result_tuple(after) != expected_tuples[next_state]:
            raise AssertionError(f"{label}: batch decision has an invalid Review result tuple")
        if after["attempt_report_artifact"] != before["attempt_report_artifact"]:
            raise AssertionError(f"{label}: batch Review cannot replace the reviewed Report artifact")
    if current_state == "awaiting-final-verification" and next_state in {"needs-fix", "blocked"}:
        before_tuple = _result_tuple(before)
        after_tuple = _result_tuple(after)
        expected = {
            ("pass", "pending", "pending"): {
                "needs-fix": ("pass", "fail", "pending"),
                "blocked": ("pass", "blocked", "pending"),
            },
            ("pass", "pass", "pending"): {
                "needs-fix": ("pass", "pass", "fail"),
                "blocked": ("pass", "pass", "blocked"),
            },
        }
        if expected.get(before_tuple, {}).get(next_state) != after_tuple:
            raise AssertionError(
                f"{label}: final Review requires persisted final verification in a prior revision"
            )
        for key in ("attempt_report_artifact", "last_review_artifact"):
            if after[key] != before[key]:
                raise AssertionError(f"{label}: final gate cannot rewrite {key}")
        if before_tuple == ("pass", "pass", "pending") and (
            after["final_verification_artifact"] != before["final_verification_artifact"]
        ):
            raise AssertionError(f"{label}: final Review cannot replace verification evidence")
    if current_state == "awaiting-final-verification" and next_state == "awaiting-final-verification":
        if _result_tuple(before) != ("pass", "pending", "pending") or _result_tuple(after) != ("pass", "pass", "pending"):
            raise AssertionError(f"{label}: awaiting self-transition only persists final verification PASS")
        for key in ("attempt_report_artifact", "last_review_artifact"):
            if before[key] != after[key]:
                raise AssertionError(f"{label}: final verification cannot rewrite {key}")
    if next_state == "complete":
        if _result_tuple(before) != ("pass", "pass", "pending"):
            raise AssertionError(f"{label}: complete requires persisted final verification PASS")
        if after["final_verification_artifact"] != before["final_verification_artifact"]:
            raise AssertionError(f"{label}: final Review cannot replace verification evidence")
        for key in ("attempt_report_artifact", "last_review_artifact"):
            if after[key] != before[key]:
                raise AssertionError(f"{label}: final Review cannot replace {key}")


def validate_transition(before: dict, after: dict, label: str) -> None:
    _validate_transition(before, after, label, legacy_parent=False)


def _validate_legacy_transition(before: dict, after: dict, label: str) -> None:
    _validate_transition(before, after, label, legacy_parent=True)


def validate_frontmatter(skill: str) -> None:
    if not skill.startswith("---\n"):
        raise AssertionError("SKILL.md: missing YAML frontmatter")
    parts = skill.split("---\n", 2)
    keys = [
        line.split(":", 1)[0].strip()
        for line in parts[1].splitlines()
        if line.strip() and not line.startswith(" ") and ":" in line
    ]
    if keys != ["name", "description"]:
        raise AssertionError(f"SKILL.md: frontmatter keys must be name, description only; got {keys}")


GOVERNED_CAVEMAN_LITE_PROFILE_OBLIGATIONS = (
    "governed-caveman-lite",
    "OpenSpec 精简模式：<任务>",
    "send `OpenSpec 精简模式` before the task",
    "OpenSpec 正常模式",
    "concise professional full sentences",
    "current conversation",
    "until disabled or the conversation ends",
    "A new conversation starts in normal output mode",
    "no account, repository, or runtime preference",
    "latest explicit OpenSpec mode command",
    "even after a prior Caveman-style instruction",
    "presentation state only",
    "never invokes or delegates to a separate `caveman` skill",
    "works when one is unavailable",
    "does not activate by default",
    "routing, approval, evidence, Review, verification, completion, Git, or publication authority",
)
GOVERNED_CAVEMAN_LITE_PROTECTED_OBLIGATIONS = (
    "Gate 0",
    "OpenSpec artifacts",
    "Superpowers implementation plans",
    "Handoff/evidence artifacts",
    "canonical state transitions",
    "PASS/FAIL/BLOCKED",
    "final verification",
    "final Review",
    "critical commands",
    "rollback instructions",
    "security warnings",
    "destructive confirmations",
    "sensitive-data handling",
    "every required field and ordering constraint",
)
GOVERNED_CAVEMAN_LITE_SKILL_OBLIGATIONS = (
    GOVERNED_CAVEMAN_LITE_PROFILE_OBLIGATIONS
    + ("mandatory governance/approval fields",)
    + GOVERNED_CAVEMAN_LITE_PROTECTED_OBLIGATIONS
)
GOVERNED_CAVEMAN_LITE_RESPONSE_OBLIGATIONS = (
    GOVERNED_CAVEMAN_LITE_PROFILE_OBLIGATIONS
    + ("mandatory governance-step or approval field",)
    + GOVERNED_CAVEMAN_LITE_PROTECTED_OBLIGATIONS
)
LEGACY_REQUEST_SCOPED_BREVITY_OBLIGATIONS = (
    "少 token/更短/更精简/像 caveman 说",
    "request-scoped compression",
    "current request",
    "does not activate or persist `governed-caveman-lite`",
    "Only `OpenSpec 精简模式` activates the named conversation profile",
    "same protected-surface rules",
)


def _governed_yaml_scalar(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        return stripped
    if stripped[0] in "|>[{&*!@`":
        raise ValueError("unsupported YAML scalar form")
    if stripped[0] not in {'"', "'"}:
        for index, char in enumerate(stripped):
            if char == "#" and (
                index == 0 or stripped[index - 1].isspace()
            ):
                return stripped[:index].rstrip()
        return stripped

    quote = stripped[0]
    index = 1
    while index < len(stripped):
        char = stripped[index]
        if quote == '"' and char == "\\":
            if index + 1 >= len(stripped):
                raise ValueError("unterminated YAML escape")
            escape = stripped[index + 1]
            if escape in "0abtnvfre \"\\/N_LP":
                index += 2
                continue
            widths = {"x": 2, "u": 4, "U": 8}
            if escape not in widths:
                raise ValueError("unsupported YAML escape")
            width = widths[escape]
            digits = stripped[index + 2:index + 2 + width]
            if (
                len(digits) != width
                or re.fullmatch(r"[0-9A-Fa-f]+", digits) is None
            ):
                raise ValueError("invalid YAML hexadecimal escape")
            index += 2 + width
            continue
        if quote == "'" and char == "'":
            if index + 1 < len(stripped) and stripped[index + 1] == "'":
                index += 2
                continue
        if char == quote:
            tail = stripped[index + 1:]
            if tail and not (
                tail[0].isspace()
                and tail.lstrip().startswith("#")
            ):
                raise ValueError("unexpected text after quoted YAML scalar")
            return stripped[:index + 1]
        index += 1
    raise ValueError("unterminated quoted YAML scalar")


def _load_governed_frontmatter(text: str):
    if yaml is not None:
        return yaml.safe_load(text)

    normalized_lines: list[str] = []
    seen_keys: set[str] = set()
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line[0].isspace() or ":" not in raw_line:
            raise ValueError("unsupported YAML frontmatter structure")
        key, value = raw_line.split(":", 1)
        key = key.strip()
        if (
            re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", key) is None
            or key in seen_keys
        ):
            raise ValueError("invalid or duplicate YAML key")
        seen_keys.add(key)
        normalized_lines.append(
            f"{key}: {_governed_yaml_scalar(value)}"
        )
    return simple_yaml_load("\n".join(normalized_lines))


def _markdown_visible_outside_html_comment(
    line: str,
    in_comment: bool,
) -> tuple[str, bool]:
    visible: list[str] = []
    cursor = 0
    while cursor < len(line):
        if in_comment:
            comment_end = line.find("-->", cursor)
            if comment_end == -1:
                return "".join(visible), True
            cursor = comment_end + 3
            in_comment = False
        else:
            comment_start = line.find("<!--", cursor)
            if comment_start == -1:
                visible.append(line[cursor:])
                break
            visible.append(line[cursor:comment_start])
            cursor = comment_start + 4
            in_comment = True
    return "".join(visible), in_comment


def _markdown_container_position(line: str) -> int:
    position = 0
    container_patterns = (
        r" {0,3}>[ \t]?",
        r" {0,3}(?:[-+*]|\d{1,9}[.)])[ \t]+",
    )
    while position < len(line):
        for pattern in container_patterns:
            container = re.match(pattern, line[position:])
            if container is not None:
                position += container.end()
                break
        else:
            break
    return position


def _markdown_fence_candidate(
    line: str,
    *,
    closing: bool = False,
) -> tuple[str, str] | None:
    position = _markdown_container_position(line)

    candidate = re.match(
        r"^ {0,3}(`{3,}|~{3,})(.*)$",
        line[position:],
    )
    if candidate is not None:
        return candidate.group(1), candidate.group(2)
    if closing:
        continuation = re.match(
            r"^ {2,}(`{3,}|~{3,})(.*)$",
            line[position:],
        )
        if continuation is not None:
            return continuation.group(1), continuation.group(2)
    return None


def _markdown_heading_spans(
    text: str,
) -> list[tuple[str, int, int, int]]:
    headings: list[tuple[str, int, int, int]] = []
    fence_char: str | None = None
    fence_length = 0
    in_html_comment = False
    offset = 0

    for raw_line in text.splitlines(keepends=True):
        line = raw_line.rstrip("\r\n")
        line_end = offset + len(line)
        if fence_char is not None:
            closing_fence = _markdown_fence_candidate(
                line,
                closing=True,
            )
            if closing_fence is not None:
                marker, suffix = closing_fence
                if (
                    marker[0] == fence_char
                    and len(marker) >= fence_length
                    and not suffix.strip()
                ):
                    fence_char = None
                    fence_length = 0
        else:
            visible_line, in_html_comment = (
                _markdown_visible_outside_html_comment(
                    line,
                    in_html_comment,
                )
            )
            opening_fence = _markdown_fence_candidate(visible_line)
            if opening_fence is not None and not (
                opening_fence[0].startswith("`")
                and "`" in opening_fence[1]
            ):
                marker = opening_fence[0]
                fence_char = marker[0]
                fence_length = len(marker)
            else:
                heading_match = re.fullmatch(
                    r"(#{1,6})[ \t]+[^\r\n]+",
                    visible_line,
                )
                if heading_match is not None and line.startswith("#"):
                    headings.append(
                        (
                            visible_line,
                            len(heading_match.group(1)),
                            offset,
                            line_end,
                        )
                    )
        offset += len(raw_line)

    return headings


def _markdown_owned_section(
    text: str,
    heading: str,
    label: str,
) -> tuple[str, int, int]:
    heading_syntax = re.fullmatch(r"(#{1,6})[ \t]+[^\r\n]+", heading)
    if heading_syntax is None:
        raise AssertionError(f"{label}: invalid Markdown heading {heading!r}")

    headings = _markdown_heading_spans(text)
    matches = [item for item in headings if item[0] == heading]
    if len(matches) != 1:
        raise AssertionError(
            f"{label}: expected exactly one Markdown heading {heading!r}; "
            f"found {len(matches)}"
        )

    _, _, heading_start, section_start = matches[0]
    heading_level = len(heading_syntax.group(1))
    section_end = len(text)
    for _, level, start, _ in headings:
        if start > heading_start and level <= heading_level:
            section_end = start
            break
    return text[section_start:section_end], heading_start, section_end


def _markdown_blockquote_content(line: str) -> tuple[int, str]:
    depth = 0
    position = 0
    while position < len(line):
        marker = re.match(r" {0,3}>[ \t]?", line[position:])
        if marker is None:
            break
        position += marker.end()
        depth += 1
    return depth, line[position:]


def _markdown_column_width(text: str) -> int:
    column = 0
    for char in text:
        if char == "\t":
            column += 4 - (column % 4)
        else:
            column += 1
    return column


def _markdown_leading_indent(line: str) -> tuple[int, int]:
    column = 0
    index = 0
    while index < len(line) and line[index] in " \t":
        if line[index] == "\t":
            column += 4 - (column % 4)
        else:
            column += 1
        index += 1
    return column, index


def _markdown_indent_index(line: str, target_column: int) -> int | None:
    if target_column == 0:
        return 0
    column = 0
    index = 0
    while index < len(line) and line[index] in " \t":
        if line[index] == "\t":
            column += 4 - (column % 4)
        else:
            column += 1
        index += 1
        if column >= target_column:
            return index
    return None


def _markdown_list_prefix(line: str) -> tuple[int, int] | None:
    marker = re.match(
        r"^(?P<indent>[ \t]*)(?:[-+*]|\d{1,9}[.)])(?P<spacing>[ \t]+)",
        line,
    )
    if marker is None:
        return None
    return (
        _markdown_column_width(marker.group("indent")),
        _markdown_column_width(marker.group(0)),
    )


def _markdown_visible_content(text: str) -> str:
    visible_lines: list[str] = []
    fence_char: str | None = None
    fence_length = 0
    fence_quote_depth: int | None = None
    fence_list_indent: int | None = None
    in_html_comment = False
    list_stacks: dict[int, list[tuple[int, int]]] = {}

    for raw_line in text.splitlines():
        line = raw_line.rstrip("\r\n")
        if fence_char is not None:
            closing_fence = _markdown_fence_candidate(
                line,
                closing=True,
            )
            if closing_fence is not None:
                marker, suffix = closing_fence
                if (
                    marker[0] == fence_char
                    and len(marker) >= fence_length
                    and not suffix.strip()
                ):
                    fence_char = None
                    fence_length = 0
                    fence_quote_depth = None
                    fence_list_indent = None
                continue
            if fence_list_indent is None:
                continue
            quote_depth, list_line = _markdown_blockquote_content(line)
            leading, _ = _markdown_leading_indent(list_line)
            if (
                quote_depth == fence_quote_depth
                and leading >= fence_list_indent
            ):
                content_index = _markdown_indent_index(
                    list_line,
                    fence_list_indent,
                )
                if content_index is None:
                    continue
                closing_fence = _markdown_fence_candidate(
                    list_line[content_index:],
                    closing=True,
                )
                if closing_fence is not None:
                    marker, suffix = closing_fence
                    if (
                        marker[0] == fence_char
                        and len(marker) >= fence_length
                        and not suffix.strip()
                    ):
                        fence_char = None
                        fence_length = 0
                        fence_quote_depth = None
                        fence_list_indent = None
                continue
            fence_char = None
            fence_length = 0
            fence_quote_depth = None
            fence_list_indent = None

        visible_line, in_html_comment = (
            _markdown_visible_outside_html_comment(
                line,
                in_html_comment,
            )
        )
        quote_depth, list_line = _markdown_blockquote_content(
            visible_line
        )
        stack = list_stacks.setdefault(quote_depth, [])
        list_prefix = _markdown_list_prefix(list_line)
        active_list_indent: int | None = None
        logical_line = list_line

        if list_prefix is not None:
            base_indent, content_indent = list_prefix
            valid_list_item = (
                base_indent <= 3
                or (
                    bool(stack)
                    and (
                        base_indent == stack[-1][0]
                        or base_indent >= stack[-1][1]
                    )
                )
            )
            if valid_list_item:
                while stack and base_indent <= stack[-1][0]:
                    stack.pop()
                stack.append((base_indent, content_indent))
                active_list_indent = content_indent
            else:
                list_prefix = None

        if list_prefix is None:
            if not list_line.strip():
                visible_lines.append(visible_line)
                continue
            leading, _ = _markdown_leading_indent(list_line)
            while stack and leading < stack[-1][1]:
                stack.pop()
            if stack:
                active_list_indent = stack[-1][1]
                relative_indent = leading - active_list_indent
                if relative_indent >= 4:
                    continue
                content_index = _markdown_indent_index(
                    list_line,
                    active_list_indent,
                )
                if content_index is None:
                    continue
                logical_line = list_line[content_index:]
            elif leading >= 4:
                continue

        opening_fence = _markdown_fence_candidate(visible_line)
        if opening_fence is None and logical_line != list_line:
            opening_fence = _markdown_fence_candidate(logical_line)
            if opening_fence is not None:
                fence_quote_depth = quote_depth
                fence_list_indent = active_list_indent
        if opening_fence is not None and not (
            opening_fence[0].startswith("`")
            and "`" in opening_fence[1]
        ):
            marker = opening_fence[0]
            fence_char = marker[0]
            fence_length = len(marker)
            continue
        fence_quote_depth = None
        fence_list_indent = None
        visible_lines.append(visible_line)

    return "\n".join(visible_lines)


def validate_governed_caveman_lite(
    skill: str,
    response_patterns: str,
    readme: str | None = None,
    readme_cn: str | None = None,
) -> None:
    frontmatter_match = re.match(
        r"\A---\r?\n(?P<frontmatter>.*?)\r?\n---(?:\r?\n|\Z)",
        skill,
        flags=re.DOTALL,
    )
    if frontmatter_match is None:
        raise AssertionError(
            "SKILL.md governed Caveman Lite frontmatter: "
            "missing YAML frontmatter"
        )
    try:
        frontmatter = _load_governed_frontmatter(
            frontmatter_match.group("frontmatter")
        )
    except Exception as exc:
        raise AssertionError(
            "SKILL.md governed Caveman Lite frontmatter: invalid YAML"
        ) from exc
    if not isinstance(frontmatter, dict):
        raise AssertionError(
            "SKILL.md governed Caveman Lite frontmatter: "
            "frontmatter must be a mapping"
        )
    description = frontmatter.get("description")
    if not isinstance(description, str):
        raise AssertionError(
            "SKILL.md governed Caveman Lite frontmatter: "
            "description must be a string"
        )
    require(
        description,
        "caveman 风格摘要",
        "SKILL.md legacy Caveman frontmatter",
    )
    for command in ("OpenSpec 精简模式", "OpenSpec 正常模式"):
        require(
            description,
            command,
            "SKILL.md governed Caveman Lite frontmatter",
        )

    skill_profile, _, _ = _markdown_owned_section(
        skill,
        "## Governed Caveman Lite output mode",
        "SKILL.md governed Caveman Lite",
    )
    normalized_skill_profile = " ".join(
        _markdown_visible_content(skill_profile).split()
    )
    for obligation in GOVERNED_CAVEMAN_LITE_SKILL_OBLIGATIONS:
        require(
            normalized_skill_profile,
            obligation,
            "SKILL.md governed Caveman Lite",
        )

    legacy_skill_profile, _, _ = _markdown_owned_section(
        skill,
        "## Legacy request-scoped output compatibility",
        "SKILL.md legacy request-scoped brevity",
    )
    normalized_legacy_skill_profile = " ".join(
        _markdown_visible_content(legacy_skill_profile).split()
    )
    for obligation in LEGACY_REQUEST_SCOPED_BREVITY_OBLIGATIONS:
        require(
            normalized_legacy_skill_profile,
            obligation,
            "SKILL.md legacy request-scoped brevity",
        )

    _, token_budget_heading_start, token_budget_end = _markdown_owned_section(
        response_patterns,
        "## Token budget control",
        "response-patterns.md governed Caveman Lite parent",
    )
    response_profile, response_heading_start, response_profile_end = (
        _markdown_owned_section(
            response_patterns,
            "### Governed Caveman Lite",
            "response-patterns.md governed Caveman Lite",
        )
    )
    if not (
        token_budget_heading_start
        < response_heading_start
        < response_profile_end
        <= token_budget_end
    ):
        raise AssertionError(
            "response-patterns.md governed Caveman Lite: "
            "heading must be owned by ## Token budget control"
        )
    normalized_response_profile = " ".join(
        _markdown_visible_content(response_profile).split()
    )
    for obligation in GOVERNED_CAVEMAN_LITE_RESPONSE_OBLIGATIONS:
        require(
            normalized_response_profile,
            obligation,
            "response-patterns.md governed Caveman Lite",
        )

    legacy_response, legacy_response_heading_start, legacy_response_end = (
        _markdown_owned_section(
            response_patterns,
            "### Legacy request-scoped brevity",
            "response-patterns.md legacy request-scoped brevity",
        )
    )
    if not (
        token_budget_heading_start
        < legacy_response_heading_start
        < legacy_response_end
        <= token_budget_end
    ):
        raise AssertionError(
            "response-patterns.md legacy request-scoped brevity: "
            "heading must be owned by ## Token budget control"
        )
    normalized_legacy_response = " ".join(
        _markdown_visible_content(legacy_response).split()
    )
    for obligation in LEGACY_REQUEST_SCOPED_BREVITY_OBLIGATIONS:
        require(
            normalized_legacy_response,
            obligation,
            "response-patterns.md legacy request-scoped brevity",
        )

    if (readme is None) != (readme_cn is None):
        raise AssertionError(
            "governed Caveman Lite requires both bilingual READMEs or neither"
        )
    if readme is None:
        return

    for owner, text, heading in (
        ("README.md", readme, "## Governed Caveman Lite"),
        ("README_cn.md", readme_cn, "## 治理精简模式"),
    ):
        section, _, _ = _markdown_owned_section(
            text,
            heading,
            f"{owner} governed Caveman Lite",
        )
        normalized_section = " ".join(
            _markdown_visible_content(section).split()
        )
        for command in ("OpenSpec 精简模式：<任务>", "OpenSpec 正常模式"):
            require(
                normalized_section,
                command,
                f"{owner} governed Caveman Lite",
            )


def validate_project_learning_gate(
    skill: str,
    approved: str,
    completion: str,
    learning_closeout: str,
    learning_template: str,
) -> None:
    try:
        frontmatter = skill.split("---", 2)[1]
    except IndexError as exc:
        raise AssertionError("SKILL.md: missing frontmatter") from exc
    normalized_skill = " ".join(skill.split())
    normalized_approved = " ".join(approved.split())
    normalized_completion = " ".join(completion.split())
    normalized_closeout = " ".join(learning_closeout.split())
    normalized_template = " ".join(learning_template.split())

    for needle in (
        "archive and distill",
        "Project Learning Closeout",
        "归档并蒸馏",
    ):
        require(frontmatter, needle, "SKILL.md frontmatter description")

    require(
        normalized_skill,
        "follows `references/completion-contract.md`",
        "SKILL.md project learning routing",
    )
    require(
        normalized_approved,
        "`references/completion-contract.md`",
        "approved-implementation-workflow.md",
    )
    for needle in (
        "Run Project Learning Closeout after implementation Review PASS",
        "before fresh final verification",
        "OpenSpec reconciliation/archive",
        "A chat-only summary is not durable promotion",
    ):
        require(normalized_completion, needle, "completion-contract.md learning routing")

    for needle in (
        "Implement -> Verify -> Review PASS",
        "-> Project Learning Closeout",
        "-> fresh final verification -> final Review",
        "-> OpenSpec reconcile/archive and strict validation",
        "two independent correction or Review signals",
        "one high-severity security, integrity, data-loss, or false-PASS event",
        "archive and distill the session",
        "every confirmed project-local key point",
        "single low-risk task-local correction",
        "docs/engineering-invariants.md",
        "deterministic regression test or validator",
        "Never persist full chat transcripts",
        "credentials",
        "tokens",
        "customer data",
        "final completion is `BLOCKED`",
    ):
        require(normalized_closeout, needle, "project-learning-closeout.md")

    for needle in (
        "status: candidate | promoted | rejected | blocked",
        "event_kind: correction | review-finding | security | integrity | data-loss | false-pass",
        "scope: task-local | project-local | global",
        "promotion_trigger: threshold | explicit-archive-distill | high-severity | none",
        "independent_reproductions:",
        "independence_rationale:",
        "target_artifacts:",
        "mechanical_enforcement: required | infeasible | not-applicable",
        "mechanical_enforcement_reason:",
        "verification:",
        "review_result: pending | pass | fail | blocked",
        "decision_owner: codex",
        "decision_provenance:",
        "do not copy a full conversation or Review transcript",
        "credentials, tokens, private prompts",
        "customer data",
        "deterministic regression test or validator",
        "prose-only documentation cannot satisfy promotion",
        "Only the Codex control plane records `promoted`",
    ):
        require(normalized_template, needle, "learning-candidate-template.md")


def validate_reference_links(root: Path, skill: str) -> None:
    for link in re.findall(r"`(references/[^`]+\.md)`", skill):
        if not (root / link).is_file():
            raise AssertionError(f"SKILL.md: linked reference missing: {link}")


def validate_completion_contract(
    skill: str,
    completion: str,
    response_patterns: str,
    approved: str,
    evidence: str,
) -> None:
    normalized = " ".join(completion.split())
    for heading in (
        "## Success", "## Evidence", "## Stop conditions",
        "## Learning and reconciliation", "## Cross-CLI sync",
        "## Git and publication authority", "## Residual risk",
    ):
        require(completion, heading, "completion-contract.md")
    for needle in (
        "fresh final evidence", "final Review PASS",
        "Project Learning Closeout", "OpenSpec task reconciliation",
        "strict validation after archive", "every declared required runtime",
        "explicit user authorization", "FAIL", "BLOCKED",
        "final_critical", "hashed evidence manifest", "--previous-status",
        "tests/logs", "sensitive information", "temporary files",
        "unrelated changes", "superpowers:verification-before-completion",
        "A chat-only summary is not durable promotion",
        "Reconcile `tasks.md`", "Update project-required design/closeout documentation",
    ):
        require(normalized, needle, "completion-contract.md")
    require(
        normalized,
        "Run Project Learning Closeout after implementation Review PASS and "
        "before fresh final verification",
        "completion-contract.md",
    )
    if "Run Project Learning Closeout after implementation Review PASS when" in normalized:
        raise AssertionError("completion-contract.md: conditional Learning entry weakens closeout")
    for text, label in (
        (skill, "SKILL.md"),
        (response_patterns, "response-patterns.md"),
        (approved, "approved-implementation-workflow.md"),
        (evidence, "step-evidence-gate.md"),
    ):
        require(text, "references/completion-contract.md", label)

    skill_closure = skill.split("## Implementation And Closure", 1)[1].split(
        "## Capability And Evidence Profiles", 1
    )[0]
    approved_final = approved.split("## Final Completion", 1)[1].split(
        "## Tiered Authorization And High Review", 1
    )[0]
    forbidden_secondary = (
        (skill_closure, "run Project Learning Closeout", "SKILL.md closure"),
        (approved_final, "persist fresh `final_critical`", "approved final section"),
        (approved_final, "--previous-status", "approved final section"),
        (approved_final, "superpowers:verification-before-completion", "approved final section"),
        (evidence, "Completion claim allowed", "step-evidence-gate.md"),
    )
    for text, needle, label in forbidden_secondary:
        if needle in text:
            raise AssertionError(f"{label}: independent completion rule remains: {needle!r}")
    require(evidence, "whole-task decision is deferred", "step-evidence-gate.md")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--status", type=Path)
    parser.add_argument("--artifact-root", type=Path)
    parser.add_argument("--previous-status", type=Path)
    parser.add_argument("--legacy-inventory-root", action="append", type=Path, default=[])
    parser.add_argument("--legacy-inventory-output", type=Path)
    args = parser.parse_args(argv[1:])
    if bool(args.status) != bool(args.artifact_root):
        parser.error("--status and --artifact-root must be provided together")
    if args.previous_status and not args.status:
        parser.error("--previous-status requires --status and --artifact-root")
    if bool(args.legacy_inventory_root) != bool(args.legacy_inventory_output):
        parser.error(
            "--legacy-inventory-root and --legacy-inventory-output are required together"
        )
    return args


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv if argv is None else argv
    args = parse_args(argv)
    root = Path(args.root).resolve()
    skill = read(root / "SKILL.md")
    request_modes = read(root / "references" / "request-modes.md")
    approved = read(root / "references" / "approved-implementation-workflow.md")
    response_patterns = read(root / "references" / "response-patterns.md")
    readme_path = root / "README.md"
    readme_cn_path = root / "README_cn.md"
    readme = read(readme_path) if readme_path.is_file() else None
    readme_cn = read(readme_cn_path) if readme_cn_path.is_file() else None
    completion = read(root / "references" / "completion-contract.md")
    self_rule = read(root / "references" / "self-evolution-rule.md")
    evidence = read(root / "references" / "step-evidence-gate.md")
    handoff = read(root / "references" / "handoff-contract.md")
    adapter = read(root / "references" / "superpowers-adapter.md")
    capability = read(root / "references" / "agent-capability-routing.md")
    lease = read(root / "references" / "confirmation-lease.md")
    learning = read(root / "references" / "learning-candidate-pipeline.md")
    local_checkpoint = read(root / "references" / "local-instruction-checkpoint.md")
    learning_closeout = read(root / "references" / "project-learning-closeout.md")
    learning_template = read(root / "templates" / "learning-candidate-template.md")
    final_verification_template = read(root / "templates" / "final-verification-template.md")

    validate_frontmatter(skill)
    validate_reference_links(root, skill)
    validate_governed_caveman_lite(
        skill,
        response_patterns,
        readme,
        readme_cn,
    )
    validate_completion_contract(
        skill, completion, response_patterns, approved, evidence
    )
    for needle in (
        "OpenSpec + Superpowers Change Gate", "Self-Evolution",
        "Do not implement OpenSpec-required work before approval",
        "Do not claim completion without fresh verification evidence and Review PASS",
        "Handoff Contract", "codex-brief-antigravity-review",
        "Review and fix", "not Review-only", "Preflight Review",
    ):
        require(skill + request_modes + approved, needle, "routing gates")
    for needle in (
        "single design approval", "not every TDD micro-step",
        "inline implementation", "Review PASS",
        "OpenSpec closeout",
    ):
        require(approved, needle, "approved-implementation-workflow.md")
    require(completion, "final_critical", "completion-contract.md")
    for needle in (
        "Do not self-modify without a backup",
        "Do not bypass OpenSpec approval for Major self-evolution",
        "specific OpenSpec change", "Do not sync to GitHub or push without explicit user approval",
        "Backups created for self-evolution are temporary rollback aids, not history.",
    ):
        require(self_rule, needle, "self-evolution-rule.md")
    for needle in (
        "business slice", "Review Gate", "No completion claim is allowed without Review PASS",
        "path:line", "Formal verification",
    ):
        require(evidence, needle, "step-evidence-gate.md")
    for needle in (
        "single OpenSpec design contract", "never grants Git permission",
        "Preflight Review", "artifact revision",
    ):
        require(adapter, needle, "superpowers-adapter.md")

    for needle in (
        "control-plane-high", "cohesive-medium", "mechanical-low",
        "model names", "BLOCKED",
    ):
        require(capability, needle, "agent-capability-routing.md")
    for needle in (
        "Tool/platform authorization", "Scope/workflow authorization",
        "Business/production authorization", "invalidation_conditions",
    ):
        require(lease, needle, "confirmation-lease.md")
    for needle in (
        "Candidate Card", "two independent", "false-PASS", "proposal creation only",
    ):
        require(learning, needle, "learning-candidate-pipeline.md")
    validate_project_learning_gate(
        skill, approved, completion, learning_closeout, learning_template
    )
    for needle in (
        "must not be intentionally ignored",
        "does not require `git add`, commit, or push",
    ):
        require(local_checkpoint, needle, "local-instruction-checkpoint.md")

    contract = extract_handoff_contract(handoff, "handoff-contract.md")
    validate_handoff_contract(contract, "handoff-contract.md")
    require(handoff, "must not embed another mutable block", "handoff-contract.md")
    require(handoff, "awaiting-final-verification", "handoff-contract.md")
    for needle in (
        "COOP_EVIDENCE_MANIFEST_START", "evidence_role", "evidence_result",
        "current_batch", "attempt", "contract_revision", "canonical_sha256",
        "agent_product", "agent_instance_id", "agent_role", "capability_profile",
        "control_plane_owner", "executor_assignment", "reviewer_assignment",
        "decision_source", "confirmation_lease",
        "timeout-audit", "role-to-state binding", "result-to-status binding",
    ):
        require(handoff, needle, "handoff-contract.md")
    for needle in (
        "COOP_EVIDENCE_MANIFEST_START", "evidence_role: final-verification",
        "evidence_result:", "current_batch:", "attempt:",
        "contract_revision:", "canonical_sha256:",
        "agent_product: codex", "agent_instance_id:",
        "agent_role: control-plane", "capability_profile: control-plane-high",
    ):
        require(final_verification_template, needle, "final-verification-template.md")
    if args.legacy_inventory_root:
        records = inventory_legacy_handoffs(args.legacy_inventory_root)
        active = [record for record in records if record["drain_status"] == "active"]
        payload = {
            "legacy_audit": "pass" if not active else "blocked",
            "active_legacy_count": len(active),
            "records": records,
        }
        _write_exclusive_json(args.legacy_inventory_output, payload)
        print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
        if active:
            raise AssertionError("active schema-4/schema-5 Handoff blocks schema-6 deployment")
    if args.status:
        status_path = args.status.resolve()
        status = extract_handoff_contract(read(status_path), str(args.status))
        validate_handoff_contract(status, str(args.status))
        previous = None
        previous_sha256 = None
        if args.previous_status:
            previous_path = args.previous_status.resolve()
            previous_text = read(previous_path)
            previous = extract_handoff_contract(previous_text, str(args.previous_status))
            validate_handoff_contract(previous, str(args.previous_status))
            validate_evidence_artifacts(previous, args.artifact_root, str(args.previous_status))
            previous_sha256 = hashlib.sha256(previous_path.read_bytes()).hexdigest()
        validate_evidence_artifacts(
            status,
            args.artifact_root,
            str(args.status),
            previous=previous,
            previous_status_sha256=previous_sha256,
        )
        print(f"Runtime Handoff status valid: {args.status}")
    print(f"Core gates valid: {root}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"Core gate validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
