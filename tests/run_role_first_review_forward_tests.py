#!/usr/bin/env python3
"""Run isolated, sanitized role-first Review-routing forward probes."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
from pathlib import Path


OUTPUT_KEYS = frozenset(
    {
        "route_result",
        "review_purpose",
        "reviewer_product",
        "reviewer_role",
        "capability_profile",
        "independence_requirement",
        "result_authority",
        "blocker_owner",
        "resume_condition",
    }
)
EXPECTED_KEYS = frozenset(
    {
        "route_result",
        "reviewer_product",
        "reviewer_role",
        "capability_profile",
        "result_authority",
        "blocker_owner",
    }
)
SUMMARY_RECORD_KEYS = frozenset(
    {
        "case_id",
        "result",
        "reviewer_product",
        "reviewer_role",
        "capability_profile",
        "independence_category",
        "result_authority",
        "blocker_owner",
    }
)
PRODUCTS = ("codex", "pi", "antigravity-cli", "grok-cli")
ROLES = ("advisory-reviewer", "independent-reviewer", "control-plane")
PROFILES = ("control-plane-high", "cohesive-medium", "mechanical-low")
AUTHORITIES = (
    "advisory-input",
    "governed-review-evidence",
    "canonical-control-plane-decision",
)
BLOCKER_OWNERS = ("none", "control-plane", "user", "dependency")
CASE_IDS = (
    "generic_review_destination",
    "user_selected_pi",
    "new_window_codex",
    "advisory_review",
    "same_pi_session",
    "required_reviewer_unavailable",
)
CASE_TIMEOUT_SECONDS = 90
CLASSIFICATION_START = "<!-- ROLE_FIRST_REVIEW_CLASSIFICATION_START -->"
CLASSIFICATION_END = "<!-- ROLE_FIRST_REVIEW_CLASSIFICATION_END -->"


class ProbeFailure(RuntimeError):
    """A sanitized, non-sensitive forward-probe failure."""


def nonblank(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def canonical_schema() -> dict:
    """Return the exact approved JSON Schema for one model response."""
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "route_result",
            "review_purpose",
            "reviewer_product",
            "reviewer_role",
            "capability_profile",
            "independence_requirement",
            "result_authority",
            "blocker_owner",
            "resume_condition",
        ],
        "properties": {
            "route_result": {"enum": ["actionable", "blocked"]},
            "review_purpose": {
                "type": "object",
                "additionalProperties": False,
                "required": ["object", "decision"],
                "properties": {
                    "object": {"type": "string", "minLength": 1},
                    "decision": {"type": "string", "minLength": 1},
                },
            },
            "reviewer_product": {"enum": list(PRODUCTS)},
            "reviewer_role": {"enum": list(ROLES)},
            "capability_profile": {"enum": list(PROFILES)},
            "independence_requirement": {"type": "string", "minLength": 1},
            "result_authority": {"enum": list(AUTHORITIES)},
            "blocker_owner": {"enum": list(BLOCKER_OWNERS)},
            "resume_condition": {
                "anyOf": [
                    {"type": "string", "minLength": 1},
                    {"type": "null"},
                ]
            },
        },
    }


def validate_schema_document(schema: object) -> dict:
    """Reject any output schema that differs from the approved contract."""
    if schema != canonical_schema():
        raise ProbeFailure("output schema differs from the approved contract")
    return schema


def validate_fixture(cases: object) -> list[dict]:
    """Validate the six public prompts and private oracle records."""
    if not isinstance(cases, list) or len(cases) != len(CASE_IDS):
        raise ProbeFailure("case fixture must contain exactly six cases")
    if tuple(case.get("id") for case in cases if isinstance(case, dict)) != CASE_IDS:
        raise ProbeFailure("case fixture IDs or order are invalid")
    for case in cases:
        if (
            set(case) != {"id", "prompt", "expected", "accepted_alternatives"}
            or not nonblank(case["prompt"])
        ):
            raise ProbeFailure("case fixture shape is invalid")
        expected = case["expected"]
        if not isinstance(expected, dict) or set(expected) != EXPECTED_KEYS:
            raise ProbeFailure("case expected oracle shape is invalid")
        if (
            expected["route_result"] not in {"actionable", "blocked"}
            or expected["reviewer_product"] not in PRODUCTS
            or expected["reviewer_role"] not in ROLES
            or expected["capability_profile"] not in PROFILES
            or expected["result_authority"] not in AUTHORITIES
            or expected["blocker_owner"] not in BLOCKER_OWNERS
        ):
            raise ProbeFailure("case expected oracle value is invalid")
        alternatives = case["accepted_alternatives"]
        if not isinstance(alternatives, dict) or not set(alternatives).issubset(
            {"reviewer_product", "blocker_owner"}
        ):
            raise ProbeFailure("case alternative policy is invalid")
        domains = {
            "reviewer_product": PRODUCTS,
            "blocker_owner": BLOCKER_OWNERS,
        }
        for field, values in alternatives.items():
            if (
                not isinstance(values, list)
                or not values
                or len(values) != len(set(values))
                or expected[field] not in values
                or any(value not in domains[field] for value in values)
            ):
                raise ProbeFailure("case alternative values are invalid")
    return cases


def public_case(case: dict) -> dict:
    """Return only prompt data that may be sent to the model process."""
    return {"id": case["id"], "prompt": case["prompt"]}


def build_model_prompt(case_public: dict) -> str:
    """Build the natural prompt without loading the private expected oracle."""
    if set(case_public) != {"id", "prompt"} or not nonblank(case_public["prompt"]):
        raise ProbeFailure("public case shape is invalid")
    return (
        f"{case_public['prompt']}\n\n"
        "Classify only the requested Review assignment under the discovered "
        "Router and standalone Review instructions. Do not modify files, run "
        "tools, inspect credentials, or decide canonical completion. Name one "
        "concrete reviewer product and return only the output-schema fields. "
        "review_purpose.object and review_purpose.decision must be non-blank. "
        "independence_requirement must state the required instance separation "
        "or why the request is advisory-only. An actionable result uses "
        "blocker_owner none and resume_condition null; a blocked result names "
        "the blocker owner and a non-blank resume condition."
    )


def _same_instance_claim(value: str) -> bool:
    normalized = " ".join(value.lower().replace("_", " ").split())
    return bool(
        re.search(r"\bsame[ -](?:instance|session)\b", normalized)
        or re.search(r"\b同(?:一|个)(?:实例|会话|session)\b", normalized)
    )


def validate_observed(observed: object) -> dict:
    """Validate exact shape plus fail-closed role and blocker semantics."""
    if not isinstance(observed, dict) or set(observed) != OUTPUT_KEYS:
        raise ProbeFailure("observed output must contain the exact nine fields")
    purpose = observed["review_purpose"]
    if (
        not isinstance(purpose, dict)
        or set(purpose) != {"object", "decision"}
        or not nonblank(purpose["object"])
        or not nonblank(purpose["decision"])
    ):
        raise ProbeFailure("review purpose is invalid")
    if observed["route_result"] not in {"actionable", "blocked"}:
        raise ProbeFailure("route result is invalid")
    if observed["reviewer_product"] not in PRODUCTS:
        raise ProbeFailure("reviewer product is invalid")
    if observed["reviewer_role"] not in ROLES:
        raise ProbeFailure("reviewer role is invalid")
    if observed["capability_profile"] not in PROFILES:
        raise ProbeFailure("capability profile is invalid")
    if observed["result_authority"] not in AUTHORITIES:
        raise ProbeFailure("result authority is invalid")
    if observed["blocker_owner"] not in BLOCKER_OWNERS:
        raise ProbeFailure("blocker owner is invalid")
    independence = observed["independence_requirement"]
    if not nonblank(independence):
        raise ProbeFailure("independence requirement is blank")
    resume = observed["resume_condition"]
    if observed["route_result"] == "actionable":
        if observed["blocker_owner"] != "none" or resume is not None:
            raise ProbeFailure("actionable output cannot retain a blocker")
        if (
            observed["reviewer_role"] == "independent-reviewer"
            and _same_instance_claim(independence)
        ):
            raise ProbeFailure("same-instance independent Review cannot be actionable")
    elif (
        observed["blocker_owner"] == "none"
        or not nonblank(resume)
    ):
        raise ProbeFailure("blocked output requires owner and resume condition")
    if (
        observed["reviewer_role"] == "advisory-reviewer"
        and observed["result_authority"] != "advisory-input"
    ):
        raise ProbeFailure("advisory Review cannot claim governed authority")
    if (
        observed["reviewer_role"] == "independent-reviewer"
        and observed["result_authority"] != "governed-review-evidence"
    ):
        raise ProbeFailure("independent Review must remain governed evidence")
    return observed


def compare_expected(expected: dict, observed: dict) -> list[str]:
    """Compare the private oracle only after model output validation."""
    if not isinstance(expected, dict) or set(expected) != EXPECTED_KEYS:
        raise ProbeFailure("private expected oracle shape is invalid")
    return [
        f"{field} mismatch"
        for field in sorted(EXPECTED_KEYS)
        if expected[field] != observed[field]
    ]


def compare_case_expected(case: dict, observed: dict) -> list[str]:
    """Compare only contract-determined values from the private case oracle."""
    expected = case.get("expected") if isinstance(case, dict) else None
    alternatives = case.get("accepted_alternatives") if isinstance(case, dict) else None
    if not isinstance(expected, dict) or set(expected) != EXPECTED_KEYS:
        raise ProbeFailure("private expected oracle shape is invalid")
    if not isinstance(alternatives, dict):
        raise ProbeFailure("private alternative policy shape is invalid")
    mismatches = []
    for field in sorted(EXPECTED_KEYS):
        allowed = alternatives.get(field, [expected[field]])
        if observed[field] not in allowed:
            mismatches.append(f"{field} mismatch")
    return mismatches


def independence_category(observed: dict) -> str:
    if observed["reviewer_role"] == "advisory-reviewer":
        return "advisory-not-gate-bearing"
    if _same_instance_claim(observed["independence_requirement"]):
        return "same-instance-blocked"
    if observed["route_result"] == "blocked":
        return "required-instance-unavailable"
    return "instance-separated"


def sanitize_case_record(case_id: str, observed: dict, matched: bool) -> dict:
    """Reduce one validated response to the eight durable evidence fields."""
    if not nonblank(case_id):
        raise ProbeFailure("case ID is invalid")
    record = {
        "case_id": case_id,
        "result": "PASS" if matched else "FAIL",
        "reviewer_product": observed["reviewer_product"],
        "reviewer_role": observed["reviewer_role"],
        "capability_profile": observed["capability_profile"],
        "independence_category": independence_category(observed),
        "result_authority": observed["result_authority"],
        "blocker_owner": observed["blocker_owner"],
    }
    if set(record) != SUMMARY_RECORD_KEYS:
        raise ProbeFailure("sanitized summary record shape is invalid")
    return record


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_directory(raw: str, label: str) -> Path:
    candidate = Path(raw).expanduser()
    if candidate.is_symlink():
        raise ProbeFailure(f"{label} must not be a symlink")
    try:
        resolved = candidate.resolve(strict=True)
    except OSError:
        raise ProbeFailure(f"{label} is unavailable") from None
    if not resolved.is_dir():
        raise ProbeFailure(f"{label} must be a directory")
    return resolved


def resolve_file(raw: str, label: str) -> Path:
    candidate = Path(raw).expanduser()
    if candidate.is_symlink():
        raise ProbeFailure(f"{label} must not be a symlink")
    try:
        resolved = candidate.resolve(strict=True)
    except OSError:
        raise ProbeFailure(f"{label} is unavailable") from None
    if not resolved.is_file():
        raise ProbeFailure(f"{label} must be a file")
    return resolved


def extract_review_classification(path: Path) -> str:
    """Extract one exact startup-safe Review classification block."""
    text = path.read_text(encoding="utf-8")
    if text.count(CLASSIFICATION_START) != 1 or text.count(CLASSIFICATION_END) != 1:
        raise ProbeFailure("review classification markers are invalid")
    before, remainder = text.split(CLASSIFICATION_START, 1)
    block, after = remainder.split(CLASSIFICATION_END, 1)
    if CLASSIFICATION_END in before or CLASSIFICATION_START in after or not block.strip():
        raise ProbeFailure("review classification block is invalid")
    return block.strip()


def load_review_classification(router_root: Path, companion_root: Path) -> str:
    """Require all runtime routing surfaces to publish identical classification."""
    paths = (
        router_root / "SKILL.md",
        router_root / "references" / "agent-capability-routing.md",
        router_root / "references" / "response-patterns.md",
        companion_root / "SKILL.md",
    )
    blocks = [extract_review_classification(path) for path in paths]
    if any(block != blocks[0] for block in blocks[1:]):
        raise ProbeFailure("review classification blocks differ")
    return blocks[0]


def build_project_instructions(classification: str) -> str:
    """Bind reviewed classification bytes into automatically loaded instructions."""
    if not nonblank(classification):
        raise ProbeFailure("review classification is blank")
    return (
        "Use the two project-local governed Skills for Review routing. "
        "This probe is read-only and must not run tools or mutate state.\n\n"
        f"{classification.strip()}\n"
    )


def reject_nested_symlinks(root: Path) -> None:
    for path in root.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_symlink():
            raise ProbeFailure("reviewed source contains a nested symlink")


def copy_reviewed_source(source: Path, destination: Path) -> None:
    reject_nested_symlinks(source)
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
    )


def file_snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256(path)
        for path in sorted(root.rglob("*"), key=lambda item: item.as_posix())
        if path.is_file() and not path.is_symlink()
    }


def parse_event_trace(stdout: str) -> None:
    """Reject any model-side tool/command/MCP event from the read-only probe."""
    lifecycle = {"thread.started", "turn.started", "turn.completed"}
    item_events = {"item.started", "item.updated", "item.completed"}
    allowed_items = {"agent_message", "reasoning"}
    completed = False
    agent_messages = 0
    for line in stdout.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            raise ProbeFailure("model event stream is not valid JSONL") from None
        event_type = event.get("type") if isinstance(event, dict) else None
        if event_type in lifecycle:
            completed = completed or event_type == "turn.completed"
            continue
        if event_type not in item_events:
            raise ProbeFailure("model event stream contains an unknown event")
        item = event.get("item")
        if not isinstance(item, dict) or item.get("type") not in allowed_items:
            raise ProbeFailure("tool, command, file, or MCP event is forbidden")
        if event_type == "item.completed" and item["type"] == "agent_message":
            agent_messages += 1
    if not completed or agent_messages < 1:
        raise ProbeFailure("model event stream is incomplete")


def terminate_process(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=2)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def write_private_summary(path: Path, payload: dict) -> None:
    """Create one mode-0600 summary without following or replacing a path."""
    path = Path(path)
    if path.exists() or path.is_symlink():
        raise ProbeFailure("sanitized summary output must be absent")
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        json.dump(payload, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.chmod(path, 0o600)


def run_case(
    case: dict,
    schema_path: Path,
    router_root: Path,
    companion_root: Path,
    temporary_root: Path,
    classification: str,
) -> tuple[dict, bool]:
    """Run one isolated Codex classifier and discard every raw artifact."""
    case_public = public_case(case)
    with tempfile.TemporaryDirectory(
        prefix=f"role-first-{case_public['id']}-", dir=temporary_root
    ) as raw:
        case_root = Path(raw)
        os.chmod(case_root, 0o700)
        home = case_root / "home"
        project = case_root / "project"
        home.mkdir(mode=0o700)
        project.mkdir(mode=0o700)
        skills = project / ".agents" / "skills"
        skills.mkdir(parents=True)
        copy_reviewed_source(router_root, skills / "openspec-superpower-change")
        copy_reviewed_source(
            companion_root, skills / "codex-brief-antigravity-review"
        )
        instructions = project / "AGENTS.md"
        instructions.write_text(
            build_project_instructions(classification),
            encoding="utf-8",
        )
        runtime_schema = case_root / "output.schema.json"
        runtime_schema.write_bytes(schema_path.read_bytes())
        runtime_schema.chmod(0o600)
        output = case_root / "last-message.json"
        output.touch(mode=0o600)
        output.chmod(0o600)
        before = file_snapshot(project)
        command = [
            "codex",
            "exec",
            "--json",
            "--ephemeral",
            "--ignore-user-config",
            "--ignore-rules",
            "-c",
            'model_reasoning_effort="low"',
            "--sandbox",
            "read-only",
            "--skip-git-repo-check",
            "-C",
            str(project),
            "--output-schema",
            str(runtime_schema),
            "--output-last-message",
            str(output),
            build_model_prompt(case_public),
        ]
        environment = os.environ.copy()
        environment["HOME"] = str(home)
        process = subprocess.Popen(
            command,
            cwd=project,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        try:
            stdout, _stderr = process.communicate(timeout=CASE_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            terminate_process(process)
            raise ProbeFailure("model process timed out") from None
        if process.returncode != 0:
            raise ProbeFailure("model process returned a nonzero status")
        parse_event_trace(stdout)
        if file_snapshot(project) != before:
            raise ProbeFailure("read-only model process changed project bytes")
        try:
            observed = validate_observed(
                json.loads(output.read_text(encoding="utf-8"))
            )
        except json.JSONDecodeError:
            raise ProbeFailure("model output is not valid JSON") from None
        output.unlink()
        mismatches = compare_case_expected(case, observed)
        return sanitize_case_record(case["id"], observed, not mismatches), not mismatches


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", required=True)
    parser.add_argument("--output-schema", required=True)
    parser.add_argument("--router-root", required=True)
    parser.add_argument("--companion-root", required=True)
    parser.add_argument("--temporary-root", required=True)
    parser.add_argument("--sanitized-summary", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    temporary_root = Path(args.temporary_root).expanduser().absolute()
    created_temporary_root = False
    try:
        cases_path = resolve_file(args.cases, "case fixture")
        schema_path = resolve_file(args.output_schema, "output schema")
        router_root = resolve_directory(args.router_root, "Router root")
        companion_root = resolve_directory(args.companion_root, "Companion root")
        if temporary_root.exists() or temporary_root.is_symlink():
            raise ProbeFailure("temporary root must be new and absent")
        temporary_root.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        temporary_root.mkdir(mode=0o700)
        created_temporary_root = True
        cases = validate_fixture(json.loads(cases_path.read_text(encoding="utf-8")))
        validate_schema_document(json.loads(schema_path.read_text(encoding="utf-8")))
        if (
            (router_root / "references" / "handoff-contract.md").read_bytes()
            != (companion_root / "references" / "handoff-contract.md").read_bytes()
        ):
            raise ProbeFailure("Router and Companion Handoff bytes differ")
        classification = load_review_classification(router_root, companion_root)
        records = []
        all_pass = True
        for case in cases:
            record, matched = run_case(
                case,
                schema_path,
                router_root,
                companion_root,
                temporary_root,
                classification,
            )
            records.append(record)
            all_pass = all_pass and matched
        if any(temporary_root.iterdir()):
            raise ProbeFailure("raw model/process output remains after cleanup")
        summary_path = Path(args.sanitized_summary).expanduser().absolute()
        summary = {"schema_version": 1, "case_count": len(records), "results": records}
        write_private_summary(summary_path, summary)
        result = {
            "forward": "pass" if all_pass else "blocked",
            "case_count": len(records),
            "summary": str(summary_path),
        }
        print(json.dumps(result, sort_keys=True))
        return 0 if all_pass else 1
    except (OSError, ValueError, TypeError, ProbeFailure) as exc:
        print(
            json.dumps(
                {
                    "forward": "blocked",
                    "category": type(exc).__name__,
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 1
    finally:
        if created_temporary_root and temporary_root.exists():
            shutil.rmtree(temporary_root)


if __name__ == "__main__":
    sys.exit(main())
