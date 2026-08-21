#!/usr/bin/env python3
"""Run sanitized, isolated Codex routing probes for the governed route matrix."""
from __future__ import annotations

import argparse
import concurrent.futures
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
import threading
from pathlib import Path


OUTPUT_KEYS = {
    "route",
    "result",
    "selected_superpowers",
    "state_change_allowed",
    "git_authorized",
    "completion_owner",
}
ROUTER_NAME = "openspec-superpower-change"
FORBIDDEN_ORDINARY_TERMS = (
    "router",
    "gate 0",
    "openspec",
    "using-superpowers",
    "skill invocation",
)
CASE_TIMEOUT_SECONDS = 75
SUITE_DEADLINE_SECONDS = 250
MAX_WORKERS = 5
ACTIVE_PROCESSES: dict[int, subprocess.Popen[str]] = {}
ACTIVE_LOCK = threading.Lock()
INTERRUPTED = threading.Event()


class ProbeFailure(RuntimeError):
    """A sanitized failure safe to expose in probe evidence."""


def terminate_process_group(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=2)
        return
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        pass


def terminate_all_children() -> None:
    with ACTIVE_LOCK:
        processes = list(ACTIVE_PROCESSES.values())
    for process in processes:
        terminate_process_group(process)


def handle_interruption(signum, _frame) -> None:
    INTERRUPTED.set()
    terminate_all_children()


def register_active_process(process: subprocess.Popen[str]) -> None:
    with ACTIVE_LOCK:
        ACTIVE_PROCESSES[process.pid] = process
    if INTERRUPTED.is_set():
        terminate_process_group(process)
        with ACTIVE_LOCK:
            ACTIVE_PROCESSES.pop(process.pid, None)
        raise ProbeFailure("suite interrupted during subprocess registration")


def unregister_active_process(process: subprocess.Popen[str]) -> None:
    with ACTIVE_LOCK:
        ACTIVE_PROCESSES.pop(process.pid, None)


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
    except OSError as exc:
        raise ProbeFailure(f"{label} is unavailable: {type(exc).__name__}") from None
    if not resolved.is_dir():
        raise ProbeFailure(f"{label} must be a directory")
    return resolved


def resolve_file(raw: str, label: str) -> Path:
    candidate = Path(raw).expanduser()
    if candidate.is_symlink():
        raise ProbeFailure(f"{label} must not be a symlink")
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise ProbeFailure(f"{label} is unavailable: {type(exc).__name__}") from None
    if not resolved.is_file():
        raise ProbeFailure(f"{label} must be a file")
    return resolved


def reject_nested_symlinks(root: Path, label: str) -> None:
    pending = [root]
    while pending:
        current = pending.pop()
        for child in current.iterdir():
            if child.name == ".git" and child.is_dir() and not child.is_symlink():
                continue
            metadata = child.stat(follow_symlinks=False)
            if stat.S_ISLNK(metadata.st_mode):
                raise ProbeFailure(f"{label} contains nested symlink")
            if stat.S_ISDIR(metadata.st_mode):
                pending.append(child)


def read_skill_name(path: Path) -> str | None:
    try:
        prefix = path.read_text(encoding="utf-8")[:4096]
    except (OSError, UnicodeError):
        return None
    match = re.search(r"(?m)^name:\s*['\"]?([^'\"\n]+)", prefix)
    return match.group(1).strip() if match else None


def protected_skill_inventory(root: Path) -> list[tuple[str, str]]:
    inventory: list[tuple[str, str]] = []
    if not root.exists():
        return inventory
    for skill_file in sorted(root.rglob("SKILL.md")):
        name = read_skill_name(skill_file)
        if name == ROUTER_NAME or name == "using-superpowers" or (
            name and name.startswith("superpowers:")
        ):
            inventory.append((name, str(skill_file.resolve())))
    return inventory


def copy_tree(source: Path, destination: Path) -> None:
    reject_nested_symlinks(source, "copied source")
    shutil.copytree(
        source,
        destination,
        symlinks=True,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
    )


def write_fixture_skill(destination: Path, name: str, description: str, body: str) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    (destination / "SKILL.md").write_text(
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        "---\n\n"
        f"{body.rstrip()}\n",
        encoding="utf-8",
    )


def install_fixture(
    case_public: dict,
    project: Path,
    router_source: Path,
    managed_rule_source: Path,
    superpowers_source: Path,
) -> tuple[int, str | None, str | None]:
    fixture = case_public.get("fixture")
    if not isinstance(fixture, dict):
        raise ProbeFailure(f"{case_public['id']}: invalid fixture declaration")
    skills_root = project / ".agents" / "skills"
    skills_root.mkdir(parents=True)

    router_mode = fixture.get("router", False)
    if router_mode is True:
        copy_tree(router_source, skills_root / ROUTER_NAME)
        router_count = 1
    elif router_mode == "missing":
        router_count = 0
    elif router_mode == "duplicate":
        copy_tree(router_source, skills_root / f"{ROUTER_NAME}-one")
        copy_tree(router_source, skills_root / f"{ROUTER_NAME}-two")
        router_count = 2
    elif router_mode is False:
        router_count = 0
    else:
        raise ProbeFailure(f"{case_public['id']}: unsupported Router fixture")

    superpowers = fixture.get("superpowers", [])
    if not isinstance(superpowers, list) or any(
        not isinstance(name, str) or not name for name in superpowers
    ):
        raise ProbeFailure(f"{case_public['id']}: invalid Superpowers inventory")
    if superpowers:
        destination_root = skills_root / "superpowers"
        destination_root.mkdir()
        for name in superpowers:
            source = superpowers_source / name
            if source.is_symlink() or not source.is_dir():
                raise ProbeFailure(f"{case_public['id']}: missing child Skill {name}")
            copy_tree(source.resolve(), destination_root / name)

    if fixture.get("cycle"):
        write_fixture_skill(
            skills_root / "fixture-child-a",
            "fixture:child-a",
            "Use when Child A asks for Child B in the bounded routing-cycle probe.",
            "Request fixture:child-b, then return to Router classification. Do not run tools.",
        )
        write_fixture_skill(
            skills_root / "fixture-child-b",
            "fixture:child-b",
            "Use when Child B asks for Child A in the bounded routing-cycle probe.",
            "Request fixture:child-a, forming a cycle. The Router must block. Do not run tools.",
        )

    managed_hash = None
    adapter_hash = None
    if fixture.get("managed_rule"):
        target = project / "AGENTS.md"
        shutil.copy2(managed_rule_source, target)
        managed_hash = sha256(target)
    elif case_public["id"] != "ordinary_question":
        adapter_source = router_source / "references" / "superpowers-adapter.md"
        if adapter_source.is_symlink() or not adapter_source.is_file():
            raise ProbeFailure(
                f"{case_public['id']}: same-revision Superpowers adapter missing"
            )
        target = project / "AGENTS.md"
        shutil.copy2(adapter_source, target)
        adapter_hash = sha256(target)

    discovered = [
        read_skill_name(path)
        for path in sorted(skills_root.rglob("SKILL.md"))
    ]
    observed_router_count = sum(name == ROUTER_NAME for name in discovered)
    if observed_router_count != router_count:
        raise ProbeFailure(
            f"{case_public['id']}: Router inventory {observed_router_count}, "
            f"expected fixture count {router_count}"
        )
    return router_count, managed_hash, adapter_hash


def file_snapshot(root: Path) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            snapshot[str(path.relative_to(root))] = sha256(path)
    return snapshot


def validate_observed(observed: object, schema: dict) -> dict:
    if not isinstance(observed, dict) or set(observed) != OUTPUT_KEYS:
        raise ProbeFailure("schema mismatch: exact six output fields required")
    properties = schema.get("properties", {})
    for key in ("route", "result", "completion_owner"):
        allowed = properties.get(key, {}).get("enum", [])
        if observed[key] not in allowed:
            raise ProbeFailure(f"schema mismatch: invalid {key}")
    selected = observed["selected_superpowers"]
    allowed_skills = properties.get("selected_superpowers", {}).get("items", {}).get(
        "enum", []
    )
    if not isinstance(selected, list) or len(selected) != len(set(selected)):
        raise ProbeFailure("schema mismatch: selected_superpowers must be a unique array")
    if any(item not in allowed_skills for item in selected):
        raise ProbeFailure("schema mismatch: invalid selected_superpowers item")
    for key in ("state_change_allowed", "git_authorized"):
        if type(observed[key]) is not bool:
            raise ProbeFailure(f"schema mismatch: {key} must be boolean")
    return observed


def build_runtime_schema(canonical: dict, destination: Path) -> Path:
    runtime_schema = json.loads(json.dumps(canonical))
    try:
        selected_schema = runtime_schema["properties"]["selected_superpowers"]
    except (KeyError, TypeError):
        raise ProbeFailure("canonical schema lacks selected_superpowers") from None
    if selected_schema.get("uniqueItems") is not True:
        raise ProbeFailure("canonical schema must require unique selected_superpowers")
    selected_schema.pop("uniqueItems")
    restored = json.loads(json.dumps(runtime_schema))
    restored_selected = restored["properties"]["selected_superpowers"]
    restored_selected["uniqueItems"] = True
    if restored != canonical:
        raise ProbeFailure("runtime schema transform changed more than uniqueItems")
    descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
        json.dump(runtime_schema, stream, indent=2, sort_keys=True)
        stream.write("\n")
    os.chmod(destination, 0o600)
    return destination


def compare_expected(expected: dict, observed: dict) -> list[str]:
    mismatches: list[str] = []
    if set(expected) != OUTPUT_KEYS:
        return ["fixture expected object does not contain exact six fields"]
    for key in OUTPUT_KEYS - {"selected_superpowers"}:
        if expected[key] != observed[key]:
            mismatches.append(f"{key} mismatch")
    if set(expected["selected_superpowers"]) != set(observed["selected_superpowers"]):
        mismatches.append("selected_superpowers mismatch")
    return sorted(mismatches)


def sanitized_subprocess_category(stderr: str) -> str:
    lowered = stderr.lower()
    if "invalid schema" in lowered or "response_format" in lowered:
        return "output-schema-rejected"
    if "uniqueitems" in lowered or "unique_items" in lowered:
        return "output-schema-keyword-unsupported"
    if "authentication" in lowered or "unauthorized" in lowered:
        return "authentication-failure"
    if "connection" in lowered or "network" in lowered:
        return "transport-failure"
    return "unspecified-subprocess-failure"


def parse_event_trace(stdout: str) -> dict[str, int]:
    allowed_lifecycle = {"thread.started", "turn.started", "turn.completed"}
    allowed_item_events = {"item.started", "item.updated", "item.completed"}
    allowed_item_types = {"agent_message", "reasoning"}
    counts = {
        "event_count": 0,
        "agent_message_count": 0,
        "reasoning_event_count": 0,
        "tool_event_count": 0,
    }
    saw_turn_completed = False
    for line in stdout.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            raise ProbeFailure("invalid JSONL event trace") from None
        if not isinstance(event, dict) or not isinstance(event.get("type"), str):
            raise ProbeFailure("invalid JSONL event object")
        counts["event_count"] += 1
        event_type = event["type"]
        if event_type in allowed_lifecycle:
            if event_type == "turn.completed":
                saw_turn_completed = True
            continue
        if event_type not in allowed_item_events:
            raise ProbeFailure(f"unknown JSONL event type: {event_type}")
        item = event.get("item")
        if not isinstance(item, dict) or item.get("type") not in allowed_item_types:
            counts["tool_event_count"] += 1
            item_type = item.get("type") if isinstance(item, dict) else "missing"
            raise ProbeFailure(f"tool or command event is forbidden: {item_type}")
        if event_type == "item.completed" and item["type"] == "agent_message":
            counts["agent_message_count"] += 1
        if item["type"] == "reasoning":
            counts["reasoning_event_count"] += 1
    if not saw_turn_completed or counts["agent_message_count"] < 1:
        raise ProbeFailure("incomplete JSONL event trace")
    return counts


def run_case(
    case: dict,
    router_source: Path,
    managed_rule_source: Path,
    superpowers_source: Path,
    runtime_schema_path: Path,
    schema: dict,
    codex_home: Path,
    temp_parent: Path,
) -> dict:
    case_public = {key: value for key, value in case.items() if key != "expected"}
    case_id = case_public.get("id")
    if not isinstance(case_id, str) or not case_id:
        raise ProbeFailure("case without a valid id")
    if not isinstance(case_public.get("prompt"), str) or not case_public["prompt"].strip():
        raise ProbeFailure(f"{case_id}: empty prompt")

    with tempfile.TemporaryDirectory(prefix=f"routing-{case_id}-", dir=temp_parent) as raw:
        case_root = Path(raw)
        os.chmod(case_root, 0o700)
        private_home = case_root / "home"
        project = case_root / "project"
        private_home.mkdir(mode=0o700)
        project.mkdir(mode=0o700)
        (private_home / ".agents" / "skills").mkdir(parents=True)

        if protected_skill_inventory(private_home / ".agents" / "skills"):
            raise ProbeFailure(f"{case_id}: private HOME contains governed Skills")
        account_inventory = protected_skill_inventory(codex_home / "skills")
        if account_inventory:
            raise ProbeFailure(f"{case_id}: authenticated CODEX_HOME has duplicate governed Skills")

        router_count, managed_hash, adapter_hash = install_fixture(
            case_public,
            project,
            router_source,
            managed_rule_source,
            superpowers_source,
        )
        before = file_snapshot(project)
        result_path = case_root / "last-message.txt"
        result_path.touch(mode=0o600)
        os.chmod(result_path, 0o600)

        ordinary = case_id == "ordinary_question"
        if ordinary:
            prompt = case_public["prompt"]
        else:
            prompt = case_public["prompt"] + (
                "\nClassify this request under the discovered workflow instructions. "
                "Use any Route Decision Record already present in the loaded project "
                "instructions; loading project instructions does not make the Router "
                "the completion owner of a bypass route. Do not read files or run tools. "
                "selected_superpowers must include every canonical method selected or explicitly requested, even when authority blocks the route; it grants no authority. "
                "Do not modify files or execute the requested work. Return only the "
                "output-schema fields."
            )
        command = [
            "codex", "exec", "--json", "--ephemeral", "--ignore-user-config", "--ignore-rules",
            "-c", 'model_reasoning_effort="low"',
            "--sandbox", "read-only", "--skip-git-repo-check", "-C", str(project),
        ]
        if not ordinary:
            command.extend(["--output-schema", str(runtime_schema_path)])
        command.extend(["--output-last-message", str(result_path), prompt])
        environment = os.environ.copy()
        environment.update({
            "HOME": str(private_home),
            "CODEX_HOME": str(codex_home),
        })
        if INTERRUPTED.is_set():
            raise ProbeFailure(f"{case_id}: suite interrupted before subprocess start")
        process = subprocess.Popen(
            command,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        register_active_process(process)
        try:
            try:
                stdout, stderr = process.communicate(timeout=CASE_TIMEOUT_SECONDS)
            except subprocess.TimeoutExpired:
                terminate_process_group(process)
                raise ProbeFailure(
                    f"{case_id}: Codex subprocess timed out after "
                    f"{CASE_TIMEOUT_SECONDS}s"
                ) from None
        finally:
            unregister_active_process(process)
        if INTERRUPTED.is_set():
            raise ProbeFailure(f"{case_id}: suite interrupted")
        if process.returncode != 0:
            category = sanitized_subprocess_category(stderr)
            raise ProbeFailure(
                f"{case_id}: Codex subprocess exit {process.returncode} ({category})"
            )
        event_audit = parse_event_trace(stdout)
        if file_snapshot(project) != before:
            raise ProbeFailure(f"{case_id}: read-only probe mutated project files")

        try:
            raw_result = result_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            raise ProbeFailure(f"{case_id}: unreadable last message") from None
        result_path.unlink(missing_ok=True)

        if ordinary:
            lowered = raw_result.lower()
            if not all(word in lowered for word in ("set", "unique", "list")):
                raise ProbeFailure(f"{case_id}: factual-response classifier mismatch")
            if any(term in lowered for term in FORBIDDEN_ORDINARY_TERMS):
                raise ProbeFailure(f"{case_id}: observable meta-workflow leaked")
            observed = {
                "route": "direct",
                "result": "answer",
                "selected_superpowers": [],
                "state_change_allowed": False,
                "git_authorized": False,
                "completion_owner": "none",
            }
        else:
            try:
                observed = validate_observed(json.loads(raw_result), schema)
            except json.JSONDecodeError:
                raise ProbeFailure(f"{case_id}: last message is not valid JSON") from None

        expected = case["expected"]
        mismatches = compare_expected(expected, observed)
        return {
            "id": case_id,
            "status": "PASS" if not mismatches else "FAIL",
            "observed": observed,
            "mismatches": mismatches,
            "router_inventory_count": router_count,
            "managed_rule_sha256": managed_hash,
            "adapter_sha256": adapter_hash,
            "event_audit": event_audit,
        }


def safe_write_summary(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if path.exists() and (path.is_symlink() or not path.is_file()):
        raise ProbeFailure("sanitized summary target is not a regular file")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, indent=2, sort_keys=True)
            stream.write("\n")
    finally:
        if path.exists():
            os.chmod(path, 0o600)


def run_case_sanitized(case: dict, *args) -> dict:
    try:
        return run_case(case, *args)
    except ProbeFailure as exc:
        return {
            "id": case.get("id", "invalid-case"),
            "status": "FAIL",
            "mismatches": [str(exc)],
        }
    except Exception as exc:
        return {
            "id": case.get("id", "invalid-case"),
            "status": "FAIL",
            "mismatches": [f"unexpected worker failure: {type(exc).__name__}"],
        }


def validated_remove_run_root(run_root: Path, parent: Path) -> None:
    resolved_parent = parent.resolve(strict=True)
    resolved_root = run_root.resolve(strict=True)
    if resolved_root.parent != resolved_parent:
        raise ProbeFailure("refusing cleanup outside the forward-summary parent")
    if not resolved_root.name.startswith("routing-forward-"):
        raise ProbeFailure("refusing cleanup of an unowned run-root")
    if stat.S_IMODE(resolved_root.stat().st_mode) != 0o700:
        raise ProbeFailure("refusing cleanup of run-root without mode 0700")
    shutil.rmtree(resolved_root)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--router-source", required=True)
    parser.add_argument("--managed-rule-source", required=True)
    parser.add_argument("--superpowers-source", required=True)
    parser.add_argument("--cases", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--codex-home", required=True)
    parser.add_argument("--sanitized-summary", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        router_source = resolve_directory(args.router_source, "Router source")
        managed_rule_source = resolve_file(args.managed_rule_source, "managed-rule source")
        superpowers_source = resolve_directory(args.superpowers_source, "Superpowers source")
        cases_path = resolve_file(args.cases, "case fixture")
        schema_path = resolve_file(args.schema, "output schema")
        codex_home = resolve_directory(args.codex_home, "Codex home")
        if managed_rule_source.parent.parent != router_source:
            raise ProbeFailure("Router and managed-rule sources are not the same revision")
        if codex_home != Path("/Users/elvis/.codex-account-a").resolve(strict=True):
            raise ProbeFailure("Codex home must be the pinned account-a auth root")
        cases = json.loads(cases_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        if not isinstance(cases, list) or len(cases) != 13:
            raise ProbeFailure("case fixture must contain exactly 13 cases")
        if set(schema.get("required", [])) != OUTPUT_KEYS:
            raise ProbeFailure("schema must require the exact six output fields")

        summary_path = Path(args.sanitized_summary).expanduser().absolute()
        summary_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        run_root = Path(
            tempfile.mkdtemp(prefix="routing-forward-", dir=summary_path.parent)
        )
        os.chmod(run_root, 0o700)
        prior_sigterm = signal.getsignal(signal.SIGTERM)
        prior_sigint = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGTERM, handle_interruption)
        signal.signal(signal.SIGINT, handle_interruption)
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
        ordered_results: dict[int, dict] = {}
        futures: dict[concurrent.futures.Future, tuple[int, str]] = {}
        try:
            runtime_schema_path = build_runtime_schema(
                schema, run_root / "runtime-output-schema.json"
            )
            for index, case in enumerate(cases):
                future = executor.submit(
                    run_case_sanitized,
                    case,
                    router_source,
                    managed_rule_source,
                    superpowers_source,
                    runtime_schema_path,
                    schema,
                    codex_home,
                    run_root,
                )
                futures[future] = (index, case.get("id", "invalid-case"))
            done, not_done = concurrent.futures.wait(
                futures, timeout=SUITE_DEADLINE_SECONDS
            )
            if not_done:
                INTERRUPTED.set()
                terminate_all_children()
            for future in done:
                index, case_id = futures[future]
                try:
                    ordered_results[index] = future.result()
                except Exception as exc:
                    ordered_results[index] = {
                        "id": case_id,
                        "status": "FAIL",
                        "mismatches": [
                            f"unexpected future failure: {type(exc).__name__}"
                        ],
                    }
            for future in not_done:
                index, case_id = futures[future]
                future.cancel()
                ordered_results[index] = {
                    "id": case_id,
                    "status": "FAIL",
                    "mismatches": [
                        f"suite deadline exceeded after {SUITE_DEADLINE_SECONDS}s"
                    ],
                }
        finally:
            executor.shutdown(wait=True, cancel_futures=True)
            terminate_all_children()
            for future, (index, case_id) in futures.items():
                if index in ordered_results:
                    continue
                if future.done() and not future.cancelled():
                    try:
                        ordered_results[index] = future.result()
                        continue
                    except Exception as exc:
                        reason = f"unexpected future failure: {type(exc).__name__}"
                else:
                    reason = "suite interrupted" if INTERRUPTED.is_set() else "missing worker result"
                ordered_results[index] = {
                    "id": case_id,
                    "status": "FAIL",
                    "mismatches": [reason],
                }
            signal.signal(signal.SIGTERM, prior_sigterm)
            signal.signal(signal.SIGINT, prior_sigint)
            validated_remove_run_root(run_root, summary_path.parent)
            INTERRUPTED.clear()

        results = [ordered_results[index] for index in range(len(cases))]

        failed = sum(result["status"] != "PASS" for result in results)
        payload = {
            "schema_version": 1,
            "router_source": str(router_source),
            "managed_rule_sha256": sha256(managed_rule_source),
            "superpowers_source": str(superpowers_source),
            "case_count": len(results),
            "failed": failed,
            "results": results,
        }
        safe_write_summary(summary_path, payload)
        print(f"routing forward tests: {len(results) - failed} PASS, {failed} FAIL")
        for result in results:
            if result["status"] != "PASS":
                print(f"FAIL {result['id']}: {', '.join(result['mismatches'])}")
        return 1 if failed else 0
    except (OSError, ValueError, json.JSONDecodeError, ProbeFailure) as exc:
        print(f"routing forward tests input failure: {type(exc).__name__}: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
