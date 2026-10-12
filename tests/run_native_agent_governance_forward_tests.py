#!/usr/bin/env python3
"""Probe native Codex consumption of projected governance, not Skill loading.

Author: elvis. Raw process output is memory-only and never included in summaries.
"""
from __future__ import annotations

import argparse
import importlib.util
import hashlib
import json
import os
import signal
import subprocess
import tempfile
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "native_consumption_runtime", Path(__file__).with_name("run_superpowers_routing_forward_tests.py")
)
runtime = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(runtime)

ENUMS = {
    "delivery": ("none", "chat", "saved-advisory", "bound-attempt"),
    "preflight": ("none", "inline", "standalone", "blocked"),
    "plan_timing": ("none", "before-execution", "after-execution"),
    "artifact_path": ("none", "bound-plan", "bound-attempt", "user-selected", "docs-design"),
    "product": ("none", "codex", "claude-code", "cursor", "pi", "antigravity-cli", "grok-cli"),
    "qualification": ("none", "discovered-only", "portable-only", "runtime-qualified"),
    "authority": ("none", "advisory-input", "governed-review-evidence"),
    "action": ("answer", "proposal-only", "classify-persistence", "implementation-gated", "blocked"),
}
CASE_IDS = (
    "advisory_chat", "compact_local", "compact_external", "unapproved_major",
    "bound_plan", "shared_discovery", "claude_identity",
)
CLASSIFIER_GUIDE = """
These fields classify the scenario's requested work, not this probe's own answer.
Use action=answer for ordinary read-only questions/advisory/qualification audits;
implementation-gated for a locally authorized change or approved implementation
whose required readiness, plan, or evidence obligations must be met before work;
proposal-only for a Major change requiring a scoped OpenSpec proposal/approval;
classify-persistence only for a request to save a standalone advisory that still
needs Router classification; blocked for a structurally invalid identity/assignment.
Authority means authority established by the scenario evidence or accepted
assignment, not the observer's ability to answer this probe. Qualification audits
report the authority established by discovery/parity evidence, which grants none.
An explicit advisory review request has advisory-input; a valid governed review
assignment has governed-review-evidence. Rejected formal assignments have none;
possible advisory fallback is not the requested authority.
Delivery and paths refer to the scenario's artifacts, not this JSON response.
Use none for genuinely irrelevant fields. These observational labels grant no authority.
"""
SOURCE_FILES = (
    "references/shared-global-governance.md", "references/local-instruction-checkpoint.md",
)


def validate_observed(value: object) -> dict:
    if not isinstance(value, dict) or set(value) != set(ENUMS):
        raise runtime.ProbeFailure("invalid classifier shape")
    if any(not isinstance(value[key], str) or value[key] not in choices
           for key, choices in ENUMS.items()):
        raise runtime.ProbeFailure("invalid classifier enum")
    return value


def run_case(case: dict, router_root: Path, temporary_parent: Path) -> dict:
    """Run a real native process and retain only bounded result/audit metadata."""
    with tempfile.TemporaryDirectory(prefix=case["id"] + "-", dir=temporary_parent) as raw:
        case_root = Path(raw)
        case_root.chmod(0o700)
        project, private_home = case_root / "project", case_root / "home"
        project.mkdir(mode=0o700)
        private_home.mkdir(mode=0o700)
        if runtime.protected_skill_inventory(Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills"):
            raise runtime.ProbeFailure("authenticated account has additional governed Skills")
        sections, hashes = [], {}
        for relative in SOURCE_FILES:
            path = runtime.resolve_file(str(router_root / relative), "projected source")
            source_bytes = path.read_bytes()
            sections.append(source_bytes.decode("utf-8"))
            hashes[relative] = hashlib.sha256(source_bytes).hexdigest()
        (project / "AGENTS.md").write_text(
            "# Native fixture defaults\n\n" + case["native_default"] +
            "\n\n# Governed source instructions\n\n" + "\n\n".join(sections),
            encoding="utf-8",
        )
        before = runtime.file_snapshot(project)
        schema = {
            "type": "object", "additionalProperties": False, "required": list(ENUMS),
            "properties": {key: {"enum": list(values)} for key, values in ENUMS.items()},
        }
        schema_path, output_path = case_root / "schema.json", case_root / "result.json"
        schema_path.write_text(json.dumps(schema), encoding="utf-8")
        schema_path.chmod(0o600)
        output_path.touch(mode=0o600)
        # Expectations and comparison fields never enter the model prompt.
        prompt = case["prompt"] + CLASSIFIER_GUIDE + (
            "\nClassify only under loaded instructions; do not read files, invoke tools, "
            "perform the requested work or mutate state. Return only schema fields. "
            "Use none for fields irrelevant to this request. Classifier fields are "
            "observational evidence and never grant authority."
        )
        environment = os.environ.copy()
        environment["HOME"] = str(private_home)
        command = [
            "codex", "exec", "--json", "--ephemeral", "--ignore-user-config", "--ignore-rules",
            "--sandbox", "read-only", "--skip-git-repo-check", "-C", str(project),
            "--output-schema", str(schema_path), "--output-last-message", str(output_path), prompt,
        ]
        process = subprocess.Popen(
            command, cwd=project, env=environment, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, start_new_session=True,
        )
        runtime.register_active_process(process)
        try:
            try:
                stdout, _stderr = process.communicate(timeout=90)
            except subprocess.TimeoutExpired:
                runtime.terminate_process_group(process)
                raise runtime.ProbeFailure("native process timed out") from None
        finally:
            runtime.unregister_active_process(process)
        if process.returncode != 0:
            raise runtime.ProbeFailure("native process returned nonzero")
        audit = runtime.parse_event_trace(stdout)
        if runtime.file_snapshot(project) != before:
            raise runtime.ProbeFailure("native process changed project")
        try:
            observed = validate_observed(json.loads(output_path.read_text(encoding="utf-8")))
        except (ValueError, OSError):
            raise runtime.ProbeFailure("invalid native classifier output") from None
        mismatches = [key for key, expected in case["expected"].items() if observed[key] != expected]
        return {
            "id": case["id"], "result": "PASS" if not mismatches else "FAIL",
            "observed": observed, "mismatched_fields": mismatches, "event_audit": audit,
            "source_hashes": hashes, "instructions_delivery": "temporary-project-AGENTS",
            "native_skill_loading": "not-tested", "raw_trace_retained": False,
        }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--router-root", required=True)
    parser.add_argument("--temporary-root", required=True)
    parser.add_argument("--sanitized-summary", required=True)
    parser.add_argument("--case", action="append", choices=CASE_IDS)
    args = parser.parse_args(argv)
    prior_handlers = {sig: signal.getsignal(sig) for sig in (signal.SIGTERM, signal.SIGINT)}
    for sig in prior_handlers:
        signal.signal(sig, runtime.handle_interruption)
    run_root = owned_parent = owned_identity = None
    summary = None
    status = 1
    outcome = {"forward": "BLOCKED", "reason": "invalid-input-or-native-proof"}
    try:
        root = runtime.resolve_directory(args.router_root, "Router source")
        fixture_path = runtime.resolve_file(
            str(root / "tests/fixtures/native-agent-governance-cases.json"), "case fixture"
        )
        fixture_bytes = fixture_path.read_bytes()
        fixture = json.loads(fixture_bytes.decode("utf-8"))
        cases = fixture.get("cases") if isinstance(fixture, dict) else None
        if not isinstance(cases, list) or tuple(case.get("id") for case in cases) != CASE_IDS:
            raise runtime.ProbeFailure("invalid native case inventory")
        for case in cases:
            if set(case) != {"id", "native_default", "prompt", "expected"}:
                raise runtime.ProbeFailure("invalid native case shape")
            if any(not isinstance(case[key], str) or not case[key].strip() for key in ("native_default", "prompt")):
                raise runtime.ProbeFailure("empty native case input")
            expected = case["expected"]
            if not isinstance(expected, dict) or not expected or any(
                key not in ENUMS or value not in ENUMS[key] for key, value in expected.items()
            ):
                raise runtime.ProbeFailure("invalid private case expectation")
        requested = Path(args.temporary_root).expanduser().absolute()
        if requested.exists() or requested.is_symlink():
            raise runtime.ProbeFailure("temporary root must be absent")
        requested.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        owned_parent = requested.parent.resolve() / requested.name
        owned_parent.mkdir(mode=0o700)
        parent_state = owned_parent.stat()
        owned_identity = (parent_state.st_dev, parent_state.st_ino)
        run_root = Path(tempfile.mkdtemp(prefix="routing-forward-native-", dir=owned_parent))
        selected = set(args.case or CASE_IDS)
        records = []
        for case in cases:
            if case["id"] not in selected:
                continue
            try:
                records.append(run_case(case, root, run_root))
            except runtime.ProbeFailure:
                records.append({"id": case["id"], "result": "BLOCKED", "reason": "native-proof-unavailable"})
        summary = {
            "schema_version": 1, "scope": "native-Codex-projected-instruction-consumption",
            "seven_entry_acceptance": "not-tested", "case_count": len(records),
            "fixture_sha256": hashlib.sha256(fixture_bytes).hexdigest(), "results": records,
        }
        passed = all(record["result"] == "PASS" for record in records)
        status = 0 if passed else 1
        outcome = {"forward": "PASS" if passed else "BLOCKED", "case_count": len(records)}
    except (runtime.ProbeFailure, OSError, ValueError, TypeError):
        status = 1
    finally:
        try:
            runtime.terminate_all_children()
            if run_root is not None:
                runtime.validated_remove_run_root(run_root, run_root.parent)
            if owned_parent is not None:
                state = owned_parent.lstat()
                if owned_parent.is_symlink() or (state.st_dev, state.st_ino) != owned_identity:
                    raise runtime.ProbeFailure("temporary parent ownership changed")
                owned_parent.rmdir()  # Only our empty, unchanged parent can be removed.
        except (runtime.ProbeFailure, OSError):
            status = 1
            summary = None
            outcome = {"forward": "BLOCKED", "reason": "owned-cleanup-failed"}
        finally:
            for sig, handler in prior_handlers.items():
                signal.signal(sig, handler)
    if summary is not None:
        try:
            runtime.safe_write_summary(Path(args.sanitized_summary).expanduser().absolute(), summary)
        except (runtime.ProbeFailure, OSError):
            status = 1
            outcome = {"forward": "BLOCKED", "reason": "summary-publication-failed"}
    print(json.dumps(outcome))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
