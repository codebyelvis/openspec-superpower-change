#!/usr/bin/env python3
"""Plan, apply, and verify allowlisted synchronization across CLI runtimes."""
from __future__ import annotations

import argparse
import ctypes
import errno
import fcntl
import hashlib
import json
import os
import re
import shlex
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import uuid
from contextlib import contextmanager
from pathlib import Path, PurePosixPath


MANAGED_BLOCK_START = "<!-- CROSS_CLI_GOVERNANCE_BEGIN version={version} -->"
MANAGED_BLOCK_END = "<!-- CROSS_CLI_GOVERNANCE_END version={version} -->"
TARGET_ORDER = ("codex", "pi", "antigravity-cli", "grok-cli")
TARGET_IDS = set(TARGET_ORDER)
TARGET_RULE_LAYOUT = {
    "codex": (1, "AGENTS.md"),
    "pi": (1, "APPEND_SYSTEM.md"),
    "antigravity-cli": (2, "GEMINI.md"),
    "grok-cli": (1, "AGENTS.md"),
}
LEGACY_TARGET_ORDER = ("codex", "antigravity-cli", "grok-cli")
LEGACY_TARGET_IDS = set(LEGACY_TARGET_ORDER)
PORTABLE_TOP_LEVEL = {"SKILL.md", "references", "scripts", "templates", "agents"}
DENIED_SEGMENTS = {
    "auth", "authentication", "credential", "credentials", "token", "tokens",
    "session", "sessions", "history", "log", "logs", "cache", "caches",
    "model-settings", "settings", "hook", "hooks", "mcp", "bin", "binary",
    "binaries", "keys",
}
DENIED_SUFFIXES = {".key", ".pem", ".p12", ".pfx"}
REQUIRED_MANIFEST_KEYS = {"schema_version", "skills", "managed_rules", "targets"}
MANAGED_RULE_INVARIANT_COUNT = {1: 8, 2: 13, 3: 14, 4: 15, 5: 15, 6: 16}
PORTABLE_MANIFEST_PATH = "references/cross-cli-portable-manifest.json"
SANDBOX_EXECUTABLE = Path("/usr/bin/sandbox-exec")
RENAME_SWAP = 0x00000002
RENAME_EXCL = 0x00000004
AT_FDCWD = -2
RECEIPT_SCHEMA_VERSION = 1
RECEIPT_PENDING_STATES = {"prepared", "mutation-intent", "applied-uncommitted"}
RECEIPT_TERMINAL_STATES = {"verified", "restored", "recovery-blocked"}


class _ExactOwnerCleanupUnavailable(ValueError):
    """The host has no primitive that deletes an inode by retained fd."""
V6_MANAGED_RULE_BODIES = {
    "CCG-001": (
        "Canonical authority belongs only to the bound instance whose product is "
        "Codex and whose governing assignment binds role `control-plane`, profile "
        "`control-plane-high`, instance identity, and contract. That instance is the "
        "sole owner of routing, approval, canonical state transitions, evidence "
        "acceptance, final verification, and final completion; no product name alone "
        "grants authority."
    ),
    "CCG-002": (
        "Under schema 6, Codex, Pi, Antigravity CLI, and Grok CLI are equally eligible "
        "for explicitly assigned executor or independent-reviewer roles. Their outputs "
        "remain bounded evidence under the assigned role, profile, instance, and "
        "contract and cannot self-authorize a canonical transition or final completion."
    ),
    "CCG-010": (
        "New governed external Handoffs use schema 6 to bind Review purpose, product, "
        "contract-local instance, role, profile, independence requirement, and result "
        "authority. Active schema-4 or schema-5 contracts must drain under their frozen "
        "validators before deployment; older complete contracts/evidence remain "
        "immutable history and never authorize a schema-6 transition."
    ),
    "CCG-016": (
        "Every Review request, recommendation, prompt, or governed assignment resolves "
        "a non-blank Review purpose and one concrete reviewer product, role, capability "
        "profile, instance-independence requirement, and result authority. Codex, Pi, "
        "Antigravity CLI, and Grok CLI are equally eligible as assigned executors or "
        "independent reviewers; product identity never grants control-plane authority. "
        "A missing or blank purpose, unresolved “other agent” destination, product "
        "substitution, self-review, or missing required independent instance is "
        "fail-closed."
    ),
}


def _nonblank(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _safe_relative_syntax(relative_path) -> str:
    if not isinstance(relative_path, (str, os.PathLike)):
        raise ValueError("path must be relative text")
    value = os.fspath(relative_path)
    if not value or "\0" in value or "\\" in value or "://" in value:
        raise ValueError(f"unsafe path: {value!r}")
    if re.match(r"^[A-Za-z]:/", value):
        raise ValueError(f"unsafe path: {value!r}")
    pure = PurePosixPath(value)
    parts = value.split("/")
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"unsafe path: {value!r}")
    return value


def _denied_category(relative_path: str) -> str | None:
    lowered = relative_path.lower()
    if lowered == ".env" or any(lowered.endswith(suffix) for suffix in DENIED_SUFFIXES):
        return "sensitive-file"
    for raw_part in lowered.split("/"):
        stem = raw_part.rsplit(".", 1)[0]
        if raw_part in DENIED_SEGMENTS or stem in DENIED_SEGMENTS:
            return raw_part
        if raw_part.startswith(("auth-", "token-", "credential-", "session-")):
            return raw_part
    return None


def _require_portable_path(relative_path: str) -> str:
    value = _safe_relative_syntax(relative_path)
    category = _denied_category(value)
    if category:
        raise ValueError(f"denied category {category!r} at path {value!r}")
    first = value.split("/", 1)[0]
    if first not in PORTABLE_TOP_LEVEL:
        raise ValueError(f"path is outside portable allowlist: {value!r}")
    if first == "agents" and value != "agents/openai.yaml":
        raise ValueError(f"path is outside portable allowlist: {value!r}")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classify_sync_trigger(changed_paths, manifest):
    """Return whether changed source paths require the cross-runtime gate."""
    validated = validate_manifest(manifest)
    portable = {
        item["path"]
        for skill in validated["skills"]
        for item in skill["files"]
    }
    portable.add(validated["managed_rules"]["source"])
    portable.add(PORTABLE_MANIFEST_PATH)
    for changed in changed_paths:
        try:
            normalized = _safe_relative_syntax(changed)
        except ValueError:
            continue
        if normalized in portable:
            return True
    return False


def validate_manifest(manifest):
    """Validate the path-free portable-file and target declaration manifest."""
    if not isinstance(manifest, dict) or set(manifest) != REQUIRED_MANIFEST_KEYS:
        raise ValueError("manifest must contain only the declared top-level fields")
    if manifest["schema_version"] != 1:
        raise ValueError("manifest schema_version must be 1")
    rules = manifest["managed_rules"]
    if not isinstance(rules, dict) or set(rules) != {"version", "source", "invariant_ids"}:
        raise ValueError("managed_rules fields are invalid")
    if type(rules["version"]) is not int or rules["version"] < 1:
        raise ValueError("managed_rules version must be a positive integer")
    _require_portable_path(rules["source"])
    invariant_count = MANAGED_RULE_INVARIANT_COUNT.get(rules["version"])
    if invariant_count is None:
        raise ValueError("managed_rules version is not supported")
    expected_ids = [f"CCG-{number:03d}" for number in range(1, invariant_count + 1)]
    if rules["invariant_ids"] != expected_ids:
        raise ValueError(
            f"managed_rules invariant_ids must be CCG-001..CCG-{invariant_count:03d}"
        )
    is_v6 = rules["version"] == 6
    target_order = TARGET_ORDER if is_v6 else LEGACY_TARGET_ORDER
    target_ids = set(target_order)
    if not isinstance(manifest["skills"], list) or not manifest["skills"]:
        raise ValueError("manifest skills must be a non-empty list")
    seen_skills: set[str] = set()
    for skill in manifest["skills"]:
        _validate_skill_manifest(
            skill,
            seen_skills,
            allowed_target_ids=target_ids,
            exact_target_order=target_order if is_v6 else None,
        )
    if not isinstance(manifest["targets"], list) or not manifest["targets"]:
        raise ValueError("manifest targets must be a non-empty list")
    _validate_target_states(
        manifest["targets"],
        allow_pending=True,
        target_ids=target_ids,
        exact_target_order=target_order if is_v6 else None,
    )
    return manifest


def _validate_skill_manifest(
    skill,
    seen_skills: set[str],
    *,
    allowed_target_ids: set[str],
    exact_target_order: tuple[str, ...] | None,
) -> None:
    if not isinstance(skill, dict) or set(skill) != {"name", "source_alias", "files"}:
        raise ValueError("skill manifest fields are invalid")
    if not _nonblank(skill["name"]) or skill["name"] in seen_skills:
        raise ValueError("skill names must be non-blank and unique")
    seen_skills.add(skill["name"])
    if not _nonblank(skill["source_alias"]) or "/" in skill["source_alias"]:
        raise ValueError("source_alias must be path-free text")
    if not isinstance(skill["files"], list) or not skill["files"]:
        raise ValueError("skill files must be a non-empty list")
    seen_paths: set[str] = set()
    for item in skill["files"]:
        if not isinstance(item, dict) or set(item) != {"path", "targets"}:
            raise ValueError("portable file entries require path and targets")
        path = _require_portable_path(item["path"])
        if path in seen_paths:
            raise ValueError(f"duplicate portable path: {path!r}")
        seen_paths.add(path)
        targets = item["targets"]
        if (
            not isinstance(targets, list)
            or not targets
            or set(targets) - allowed_target_ids
            or len(targets) != len(set(targets))
        ):
            raise ValueError(f"invalid targets for portable path {path!r}")
        if exact_target_order is not None and targets != list(exact_target_order):
            raise ValueError(f"portable path {path!r} must target all runtimes in order")


def validate_relative_path(root, relative_path, *, must_exist=True):
    """Resolve one safe regular file below root without symlink escape."""
    value = _safe_relative_syntax(relative_path)
    root_path = Path(root)
    if not root_path.exists() or not root_path.is_dir() or root_path.is_symlink():
        raise ValueError(f"invalid declared root: {root_path}")
    resolved_root = root_path.resolve(strict=True)
    candidate = root_path.joinpath(*value.split("/"))
    current = root_path
    for part in value.split("/"):
        current = current / part
        if current.exists() or current.is_symlink():
            if current.is_symlink():
                raise ValueError(f"symlink path is not allowed: {value!r}")
    if not candidate.exists():
        if must_exist:
            raise ValueError(f"missing regular file: {value!r}")
        parent = candidate.parent.resolve(strict=True)
        try:
            parent.relative_to(resolved_root)
        except ValueError as exc:
            raise ValueError(f"path escapes declared root: {value!r}") from exc
        return candidate
    resolved = candidate.resolve(strict=True)
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(f"path escapes declared root: {value!r}") from exc
    if not stat.S_ISREG(candidate.stat(follow_symlinks=False).st_mode):
        raise ValueError(f"path is not a regular file: {value!r}")
    return candidate


def build_portable_manifest(source_root, relative_paths):
    """Return relative-path/SHA-256 records for allowlisted source files."""
    records = []
    for relative_path in relative_paths:
        value = _require_portable_path(relative_path)
        path = validate_relative_path(source_root, value)
        records.append({"path": value, "sha256": _sha256(path)})
    return records


def validate_portable_parity(source_root, target_root, file_records):
    """Validate exact portable-file path and SHA-256 parity."""
    if not isinstance(file_records, list) or not file_records:
        raise ValueError("portable parity requires file records")
    for record in file_records:
        if not isinstance(record, dict) or set(record) != {"path", "sha256"}:
            raise ValueError("portable parity records require path and sha256")
        value = _require_portable_path(record["path"])
        digest = record["sha256"]
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"invalid SHA-256 for path {value!r}")
        source = validate_relative_path(source_root, value)
        target = validate_relative_path(target_root, value)
        if _sha256(source) != digest or _sha256(target) != digest:
            raise ValueError(f"portable parity drift at path {value!r}")
    return True


def _marker_parts(text: str, version: int) -> tuple[str, str, str]:
    if not isinstance(text, str):
        raise ValueError("managed-rule input must be text")
    start = MANAGED_BLOCK_START.format(version=version)
    end = MANAGED_BLOCK_END.format(version=version)
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError("managed-rule file must contain exactly one matching marker pair")
    remaining = text.replace(start, "", 1).replace(end, "", 1)
    if "CROSS_CLI_GOVERNANCE_BEGIN" in remaining or "CROSS_CLI_GOVERNANCE_END" in remaining:
        raise ValueError("managed-rule file contains an additional marker")
    start_index = text.index(start) + len(start)
    end_index = text.index(end)
    if end_index < start_index or "CROSS_CLI_GOVERNANCE_" in text[start_index:end_index].split("\n", 1)[0]:
        raise ValueError("managed-rule markers are nested or out of order")
    body = text[start_index:end_index]
    if "CROSS_CLI_GOVERNANCE_BEGIN" in body or "CROSS_CLI_GOVERNANCE_END" in body:
        raise ValueError("managed-rule markers must not be nested or mismatched")
    return text[:start_index], body, text[end_index:]


def _any_managed_marker_parts(text: str) -> tuple[str, str, str, int]:
    """Return outside bytes, body, and version for one valid managed marker pair."""
    start_pattern = re.compile(r"<!-- CROSS_CLI_GOVERNANCE_BEGIN version=(\d+) -->")
    end_pattern = re.compile(r"<!-- CROSS_CLI_GOVERNANCE_END version=(\d+) -->")
    starts = list(start_pattern.finditer(text))
    ends = list(end_pattern.finditer(text))
    if len(starts) != 1 or len(ends) != 1 or text.count("CROSS_CLI_GOVERNANCE_") != 2:
        raise ValueError("managed-rule file has partial, mismatched, or duplicate markers")
    start, end = starts[0], ends[0]
    if start.group(1) != end.group(1) or start.end() > end.start():
        raise ValueError("managed-rule file has partial, mismatched, or duplicate markers")
    body = text[start.end():end.start()]
    if "CROSS_CLI_GOVERNANCE_" in body:
        raise ValueError("managed-rule markers must not be nested")
    return text[:start.start()], body, text[end.end():], int(start.group(1))


def _render_managed_block(prefix, old_body, suffix, canonical_body, *, version):
    newline = "\r\n" if old_body.startswith("\r\n") else "\n"
    normalized = canonical_body.replace("\r\n", "\n").replace("\r", "\n")
    rendered = normalized.replace("\n", newline)
    if not rendered.endswith(newline):
        rendered += newline
    start = MANAGED_BLOCK_START.format(version=version)
    end = MANAGED_BLOCK_END.format(version=version)
    return prefix + start + newline + rendered + end + suffix


def extract_managed_block(text, *, version):
    """Extract the unique versioned managed-rule body with LF normalization."""
    _, body, _ = _marker_parts(text, version)
    body = body.replace("\r\n", "\n")
    if body.startswith("\n"):
        body = body[1:]
    return body


def replace_managed_block(original, canonical_body, *, version):
    """Replace only the unique managed-rule body and preserve outside bytes."""
    prefix, old_body, suffix = _marker_parts(original, version)
    newline = "\r\n" if old_body.startswith("\r\n") else "\n"
    normalized = canonical_body.replace("\r\n", "\n").replace("\r", "\n")
    rendered = normalized.replace("\n", newline)
    if not rendered.endswith(newline):
        rendered += newline
    return prefix + newline + rendered + suffix


def install_managed_block(original, canonical_body, *, version):
    """Install or upgrade one valid block while preserving every outside byte."""
    marker_token = "CROSS_CLI_GOVERNANCE_"
    start = MANAGED_BLOCK_START.format(version=version)
    end = MANAGED_BLOCK_END.format(version=version)
    if marker_token in original:
        prefix, old_body, suffix, installed_version = _any_managed_marker_parts(original)
        if installed_version > version:
            raise ValueError("managed-rule version downgrade is not allowed")
        return _render_managed_block(
            prefix, old_body, suffix, canonical_body, version=version
        )
    newline = "\r\n" if "\r\n" in original and "\n" not in original.replace("\r\n", "") else "\n"
    separator = "" if not original or original.endswith(("\n", "\r")) else newline
    normalized = canonical_body.replace("\r\n", "\n").replace("\r", "\n")
    body = normalized.replace("\n", newline)
    if not body.endswith(newline):
        body += newline
    return f"{original}{separator}{start}{newline}{body}{end}{newline}"


def validate_managed_rule_parity(
    canonical_body, target_text, *, version, invariant_ids
):
    """Validate normalized body equality and stable invariant IDs."""
    canonical = canonical_body.replace("\r\n", "\n").replace("\r", "\n")
    if not canonical.endswith("\n"):
        canonical += "\n"
    actual = extract_managed_block(target_text, version=version)
    if actual != canonical:
        raise ValueError("managed-rule body hash mismatch")
    for invariant_id in invariant_ids:
        if canonical.count(f"[{invariant_id}]") != 1:
            raise ValueError(f"missing or duplicate invariant ID: {invariant_id}")
    validate_managed_rule_semantics(canonical, version=version)
    return True


def validate_managed_rule_semantics(canonical_body: str, *, version: int) -> bool:
    """Bind semantic bodies that changed in managed-rule version 6."""
    if version != 6:
        return True
    normalized = " ".join(canonical_body.split())
    for invariant_id, expected in V6_MANAGED_RULE_BODIES.items():
        if normalized.count(f"[{invariant_id}] {expected}") != 1:
            raise ValueError(f"managed-rule v6 semantic drift: {invariant_id}")
    return True


def _validate_target_states(
    targets,
    *,
    allow_pending,
    target_ids: set[str] | None = None,
    exact_target_order: tuple[str, ...] | None = None,
):
    if not isinstance(targets, list) or not targets:
        raise ValueError("target states must be a non-empty list")
    expected_target_ids = TARGET_IDS if target_ids is None else target_ids
    seen: set[str] = set()
    has_required = False
    for target in targets:
        required_fields = {
            "id", "selection", "result", "decision_owner", "evidence",
            "reason", "resume_condition",
        }
        if not isinstance(target, dict) or set(target) != required_fields:
            raise ValueError("target state fields are invalid")
        target_id = target["id"]
        if target_id not in expected_target_ids or target_id in seen:
            raise ValueError("target IDs must be canonical and unique")
        seen.add(target_id)
        if target["decision_owner"] != "codex":
            raise ValueError("target decision_owner must be codex")
        if not all(_nonblank(target[field]) for field in ("evidence", "reason", "resume_condition")):
            raise ValueError("target evidence, reason, and resume_condition must be non-blank")
        selection = target["selection"]
        result = target["result"]
        if selection == "required":
            has_required = True
            allowed_results = {"pass", "pending"} if allow_pending else {"pass"}
            if result not in allowed_results:
                raise ValueError(f"required target is not complete: {target_id}")
        elif selection == "not-applicable":
            if result != "not-applicable":
                raise ValueError("failed required target cannot be mislabeled not-applicable")
            reason = target["reason"].lower()
            if not any(term in reason for term in ("not installed", "unsupported", "excluded")):
                raise ValueError("not-applicable reason is not an allowed condition")
        else:
            raise ValueError("target selection must be required or not-applicable")
    if has_required and seen != expected_target_ids:
        raise ValueError("all declared required runtime targets must be present")
    if exact_target_order is not None:
        if [target["id"] for target in targets] != list(exact_target_order):
            raise ValueError("runtime targets must use the canonical order")
    return True


def validate_target_states(targets):
    """Require completion-ready states for every declared target."""
    return _validate_target_states(targets, allow_pending=False)


def validate_completion_authority(decision):
    """Require Codex ownership and reject auxiliary self-authorization."""
    if not isinstance(decision, dict) or decision.get("decision_owner") != "codex":
        raise ValueError("only codex may own the authoritative completion decision")
    if decision.get("result") not in {"pass", "fail", "blocked"}:
        raise ValueError("completion result is invalid")
    return True


def _regular_file(path: Path, label: str) -> os.stat_result:
    try:
        metadata = path.stat(follow_symlinks=False)
    except FileNotFoundError as exc:
        raise ValueError(f"missing {label}: {path}") from exc
    if not stat.S_ISREG(metadata.st_mode):
        raise ValueError(f"{label} is not a regular file: {path}")
    return metadata


def capture_destination_prestate(path: Path) -> dict:
    candidate = Path(path)
    try:
        metadata = candidate.stat(follow_symlinks=False)
    except FileNotFoundError:
        return {"kind": "absent"}
    if not stat.S_ISREG(metadata.st_mode):
        raise ValueError(f"destination pre-state is not a regular file: {candidate}")
    return {
        "kind": "file",
        "sha256": _sha256(candidate),
        "mode": stat.S_IMODE(metadata.st_mode),
    }


def _validate_prestate_shape(pre_state: dict, label: str) -> dict:
    if not isinstance(pre_state, dict) or pre_state.get("kind") not in {"absent", "file"}:
        raise ValueError(f"invalid destination pre-state: {label}")
    if pre_state["kind"] == "absent":
        if set(pre_state) != {"kind"}:
            raise ValueError(f"invalid absent destination pre-state: {label}")
        return pre_state
    if set(pre_state) != {"kind", "sha256", "mode"}:
        raise ValueError(f"invalid file destination pre-state: {label}")
    if not isinstance(pre_state["sha256"], str) or not re.fullmatch(
        r"[0-9a-f]{64}", pre_state["sha256"]
    ):
        raise ValueError(f"invalid destination pre-state SHA-256: {label}")
    if type(pre_state["mode"]) is not int or not 0 <= pre_state["mode"] <= 0o7777:
        raise ValueError(f"invalid destination pre-state mode: {label}")
    return pre_state


def assert_destination_prestate(path: Path, pre_state: dict, label: str) -> bool:
    expected = _validate_prestate_shape(pre_state, label)
    try:
        actual = capture_destination_prestate(path)
    except ValueError:
        raise ValueError(f"destination pre-state drift: {label}") from None
    if actual != expected:
        raise ValueError(f"destination pre-state drift: {label}")
    return True


def _directory_identity(metadata: os.stat_result) -> tuple[int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        stat.S_IMODE(metadata.st_mode),
        metadata.st_uid,
        metadata.st_gid,
    )


def _capture_directory_chain(path: Path, label: str) -> tuple[tuple[str, tuple], ...]:
    directory = Path(os.path.abspath(os.fspath(path)))
    if not directory.is_absolute():
        raise ValueError(f"{label} parent must be absolute")
    current = Path(directory.anchor)
    chain: list[tuple[str, tuple]] = []
    for component in ((), *directory.parts[1:]):
        if component:
            current = current / component
        try:
            metadata = current.stat(follow_symlinks=False)
        except OSError as exc:
            raise ValueError(f"{label} parent identity drift") from exc
        if not stat.S_ISDIR(metadata.st_mode):
            raise ValueError(f"{label} parent identity drift")
        chain.append((os.fspath(current), _directory_identity(metadata)))
    return tuple(chain)


def _assert_directory_chain(chain: tuple[tuple[str, tuple], ...], label: str) -> None:
    for raw_path, expected in chain:
        try:
            metadata = Path(raw_path).stat(follow_symlinks=False)
        except OSError as exc:
            raise ValueError(f"{label} parent identity drift") from exc
        if not stat.S_ISDIR(metadata.st_mode) or _directory_identity(metadata) != expected:
            raise ValueError(f"{label} parent identity drift")


@contextmanager
def _verified_parent(target: Path, label: str):
    logical_candidate = Path(os.path.abspath(os.fspath(target)))
    if logical_candidate.name in {"", ".", ".."}:
        raise ValueError(f"{label} target name is invalid")
    try:
        resolved_parent = logical_candidate.parent.resolve(strict=True)
    except OSError as exc:
        raise ValueError(f"{label} parent identity drift") from exc
    candidate = resolved_parent / logical_candidate.name
    chain = _capture_directory_chain(candidate.parent, label)
    flags = os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(candidate.parent, flags)
    except OSError as exc:
        raise ValueError(f"{label} parent identity drift") from exc
    guard = {
        "path": candidate.parent,
        "name": candidate.name,
        "fd": descriptor,
        "chain": chain,
        "identity": chain[-1][1],
    }
    try:
        _assert_parent_guard(guard, label)
        yield guard
    finally:
        os.close(descriptor)


def _assert_parent_guard(guard: dict, label: str) -> None:
    metadata = os.fstat(guard["fd"])
    if not stat.S_ISDIR(metadata.st_mode) or _directory_identity(metadata) != guard[
        "identity"
    ]:
        raise ValueError(f"{label} parent identity drift")
    _assert_directory_chain(guard["chain"], label)


def _directory_chain_value(chain: tuple[tuple[str, tuple], ...]) -> list[dict]:
    return [
        {"path": raw_path, "identity": list(identity)}
        for raw_path, identity in chain
    ]


def _validated_directory_chain(value, label: str) -> tuple[tuple[str, tuple], ...]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} directory chain is invalid")
    chain: list[tuple[str, tuple]] = []
    previous: Path | None = None
    for item in value:
        if not isinstance(item, dict) or set(item) != {"path", "identity"}:
            raise ValueError(f"{label} directory chain is invalid")
        path = Path(item["path"])
        identity = item["identity"]
        if (
            not path.is_absolute()
            or not isinstance(identity, list)
            or len(identity) != 5
            or not all(type(component) is int for component in identity)
        ):
            raise ValueError(f"{label} directory chain is invalid")
        if previous is not None and path.parent != previous:
            raise ValueError(f"{label} directory chain is invalid")
        chain.append((os.fspath(path), tuple(identity)))
        previous = path
    return tuple(chain)


def _validate_created_parent_records(value) -> list[dict]:
    if not isinstance(value, list):
        raise ValueError("created-parent records are invalid")
    logical_paths: set[str] = set()
    resolved_paths: set[str] = set()
    for record in value:
        if not isinstance(record, dict) or set(record) != {
            "logical_path",
            "path",
            "chain",
        }:
            raise ValueError("created-parent record fields are invalid")
        logical_path = Path(record["logical_path"])
        resolved_path = Path(record["path"])
        chain = _validated_directory_chain(record["chain"], "created parent")
        if (
            not logical_path.is_absolute()
            or not resolved_path.is_absolute()
            or os.fspath(resolved_path) != chain[-1][0]
            or os.fspath(logical_path) in logical_paths
            or os.fspath(resolved_path) in resolved_paths
        ):
            raise ValueError("created-parent record binding is invalid")
        logical_paths.add(os.fspath(logical_path))
        resolved_paths.add(os.fspath(resolved_path))
    return value


@contextmanager
def _recorded_directory_guard(chain_value, label: str):
    chain = _validated_directory_chain(chain_value, label)
    path = Path(chain[-1][0])
    flags = os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise ValueError(f"{label} parent identity drift") from exc
    guard = {
        "path": path,
        "name": path.name,
        "fd": descriptor,
        "chain": chain,
        "identity": chain[-1][1],
    }
    try:
        _assert_parent_guard(guard, label)
        yield guard
    finally:
        os.close(descriptor)


@contextmanager
def _verified_parent_with_creation(
    target: Path,
    label: str,
    expected_missing,
    known_records,
):
    logical_target = Path(os.path.abspath(os.fspath(target)))
    missing = [Path(os.path.abspath(os.fspath(item))) for item in expected_missing]
    known = {
        record["logical_path"]: record
        for record in _validate_created_parent_records(list(known_records))
    }
    if not missing:
        with _verified_parent(logical_target, label) as guard:
            yield guard, []
        return
    if missing[-1] != logical_target.parent:
        raise ValueError(f"{label} created-parent plan drift")
    previous = missing[0].parent
    for directory in missing:
        if directory.parent != previous:
            raise ValueError(f"{label} created-parent plan drift")
        previous = directory
    anchor_target = missing[0].parent / ".cross-cli-parent-anchor"
    created_guards: list[dict] = []
    new_records: list[dict] = []
    with _verified_parent(anchor_target, label) as anchor_guard:
        current_guard = anchor_guard
        try:
            for logical_directory in missing:
                name = logical_directory.name
                _assert_parent_guard(current_guard, label)
                existing_record = known.get(os.fspath(logical_directory))
                flags = os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
                if existing_record is None:
                    try:
                        os.mkdir(name, mode=0o755, dir_fd=current_guard["fd"])
                    except OSError as exc:
                        raise ValueError(f"{label} parent identity drift") from exc
                    os.fsync(current_guard["fd"])
                try:
                    descriptor = os.open(name, flags, dir_fd=current_guard["fd"])
                except OSError as exc:
                    raise ValueError(f"{label} parent identity drift") from exc
                metadata = os.fstat(descriptor)
                identity = _directory_identity(metadata)
                resolved_path = current_guard["path"] / name
                chain = current_guard["chain"] + ((os.fspath(resolved_path), identity),)
                child_guard = {
                    "path": resolved_path,
                    "name": name,
                    "fd": descriptor,
                    "chain": chain,
                    "identity": identity,
                }
                created_guards.append(child_guard)
                if existing_record is not None:
                    recorded_chain = _validated_directory_chain(
                        existing_record["chain"], label
                    )
                    if recorded_chain != chain or existing_record["path"] != os.fspath(
                        resolved_path
                    ):
                        raise ValueError(f"{label} parent identity drift")
                else:
                    new_records.append(
                        {
                            "logical_path": os.fspath(logical_directory),
                            "path": os.fspath(resolved_path),
                            "chain": _directory_chain_value(chain),
                        }
                    )
                _assert_parent_guard(child_guard, label)
                current_guard = child_guard
            yield current_guard, new_records
        finally:
            for guard in reversed(created_guards):
                os.close(guard["fd"])


def _sha256_descriptor(descriptor: int) -> str:
    digest = hashlib.sha256()
    while True:
        chunk = os.read(descriptor, 65536)
        if not chunk:
            return digest.hexdigest()
        digest.update(chunk)


def _descriptor_metadata(metadata: os.stat_result) -> dict:
    """Return the immutable identity/content-bound metadata for an open file."""
    return {
        "device": metadata.st_dev,
        "inode": metadata.st_ino,
        "type": stat.S_IFMT(metadata.st_mode),
        "mode": stat.S_IMODE(metadata.st_mode),
        "uid": metadata.st_uid,
        "gid": metadata.st_gid,
        "nlink": metadata.st_nlink,
        "size": metadata.st_size,
        "mtime_ns": metadata.st_mtime_ns,
        "ctime_ns": metadata.st_ctime_ns,
    }


def _descriptor_binding(descriptor: int, label: str) -> dict:
    """Capture a stable descriptor binding across two independent reads."""
    before = os.fstat(descriptor)
    if not stat.S_ISREG(before.st_mode):
        raise ValueError(f"{label} is not a regular file")
    before_identity = _descriptor_metadata(before)
    os.lseek(descriptor, 0, os.SEEK_SET)
    first_digest = _sha256_descriptor(descriptor)
    middle = os.fstat(descriptor)
    middle_identity = _descriptor_metadata(middle)
    os.lseek(descriptor, 0, os.SEEK_SET)
    second_digest = _sha256_descriptor(descriptor)
    after = os.fstat(descriptor)
    after_identity = _descriptor_metadata(after)
    if (
        before_identity != middle_identity
        or middle_identity != after_identity
        or first_digest != second_digest
    ):
        raise ValueError(f"{label} object changed during binding")
    return {
        "fd": descriptor,
        **after_identity,
        "sha256": second_digest,
    }


def _binding_identity(binding: dict) -> tuple:
    return tuple(binding[field] for field in (
        "device", "inode", "type", "mode", "uid", "gid", "nlink",
        "size", "mtime_ns", "ctime_ns",
    ))


def _binding_stable_identity(binding: dict) -> tuple:
    """Compare content/ownership state across a namespace rename.

    A rename legitimately updates ctime on several filesystems.  The full
    descriptor identity above still binds ctime for mutation checks; this
    narrower comparison is only for an object whose retained descriptor moved
    to a different name.
    """
    return tuple(binding[field] for field in (
        "device", "inode", "type", "mode", "uid", "gid", "nlink",
        "size", "mtime_ns",
    ))


def _binding_object_identity(binding: dict) -> tuple:
    return tuple(binding[field] for field in (
        "device", "inode", "type", "mode", "uid", "gid", "nlink",
    ))


def _binding_identity_matches(actual: dict, expected: dict) -> bool:
    try:
        return _binding_identity(actual) == _binding_identity(expected)
    except (KeyError, TypeError):
        return False


def _binding_stable_identity_matches(actual: dict, expected: dict) -> bool:
    try:
        return _binding_stable_identity(actual) == _binding_stable_identity(expected)
    except (KeyError, TypeError):
        return False


def _binding_object_identity_matches(actual: dict, expected: dict) -> bool:
    try:
        return _binding_object_identity(actual) == _binding_object_identity(expected)
    except (KeyError, TypeError):
        return False


def _stable_binding_matches(
    descriptor: int,
    ownership: dict,
    label: str,
    *,
    expected: dict | None = None,
    allow_rename_ctime: bool = False,
) -> bool:
    try:
        actual = _descriptor_binding(descriptor, label)
    except (OSError, ValueError):
        return False
    identity_matches = (
        _binding_stable_identity_matches
        if allow_rename_ctime
        else _binding_identity_matches
    )
    if not identity_matches(actual, ownership):
        return False
    if expected is None:
        return actual["sha256"] == ownership.get("sha256")
    return _binding_prestate(actual) == expected


def _write_descriptor(descriptor: int, content: bytes) -> None:
    view = memoryview(content)
    while view:
        written = os.write(descriptor, view)
        if written <= 0:
            raise OSError("descriptor write made no progress")
        view = view[written:]


def _capture_guarded_prestate(guard: dict, name: str, label: str) -> dict:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(name, flags, dir_fd=guard["fd"])
    except FileNotFoundError:
        return {"kind": "absent"}
    except OSError as exc:
        raise ValueError(f"{label} is not a regular file") from exc
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise ValueError(f"{label} is not a regular file")
        return {
            "kind": "file",
            "sha256": _sha256_descriptor(descriptor),
            "mode": stat.S_IMODE(metadata.st_mode),
        }
    finally:
        os.close(descriptor)


def _open_guarded_binding(
    guard: dict, name: str, label: str, *, writable: bool = False
) -> dict:
    flags = (os.O_RDWR if writable else os.O_RDONLY) | getattr(
        os, "O_NOFOLLOW", 0
    )
    try:
        descriptor = os.open(name, flags, dir_fd=guard["fd"])
    except OSError as exc:
        raise ValueError(f"{label} is not a regular file") from exc
    try:
        binding = _descriptor_binding(descriptor, label)
        binding["kind"] = "file"
        return binding
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        raise


def _binding_prestate(binding: dict) -> dict:
    return {
        "kind": "file",
        "sha256": binding["sha256"],
        "mode": binding["mode"],
    }


def _guarded_entry_exists(guard: dict, name: str) -> bool:
    try:
        os.stat(name, dir_fd=guard["fd"], follow_symlinks=False)
    except FileNotFoundError:
        return False
    return True


def _retained_binding_matches_name(
    guard: dict,
    name: str,
    ownership: dict,
    label: str,
    *,
    expected: dict | None = None,
    allow_rename_ctime: bool = False,
) -> bool:
    """Validate both the retained FD and the current directory name."""
    try:
        metadata = os.stat(name, dir_fd=guard["fd"], follow_symlinks=False)
    except OSError:
        return False
    if not stat.S_ISREG(metadata.st_mode):
        return False
    named = _descriptor_metadata(metadata)
    if not _binding_object_identity_matches(named, ownership):
        return False
    if not _stable_binding_matches(
        ownership["fd"],
        ownership,
        label,
        expected=expected,
        allow_rename_ctime=allow_rename_ctime,
    ):
        return False
    return True


def _retained_object_binding_matches_name(
    guard: dict, name: str, ownership: dict, label: str
) -> bool:
    """Bind a name to the retained object while allowing content drift.

    This is used only for preserving an uncertain object under a recovery
    name.  The descriptor is still required to be internally stable, but its
    digest may differ from the original PASS pre-state.
    """
    try:
        metadata = os.stat(name, dir_fd=guard["fd"], follow_symlinks=False)
    except OSError:
        return False
    if not stat.S_ISREG(metadata.st_mode):
        return False
    named = _descriptor_metadata(metadata)
    if not _binding_object_identity_matches(named, ownership):
        return False
    try:
        actual = _descriptor_binding(ownership["fd"], label)
    except (OSError, ValueError):
        return False
    return _binding_object_identity_matches(actual, ownership)


def _require_retained_binding(
    guard: dict,
    name: str,
    ownership: dict,
    label: str,
    *,
    expected: dict | None = None,
    allow_rename_ctime: bool = False,
) -> None:
    if not _retained_binding_matches_name(
        guard,
        name,
        ownership,
        label,
        expected=expected,
        allow_rename_ctime=allow_rename_ctime,
    ):
        raise ValueError(f"{label} candidate ownership or content drift")


def _rebind_before_unlink(guard: dict, name: str, context: dict) -> None:
    """Re-open and bind the exact cleanup name immediately before quarantine.

    Callers that first checked a retained object must publish a short-lived
    binding context so this low-level primitive performs one final
    ``O_NOFOLLOW`` descriptor bind immediately before the atomic quarantine.
    A substituted inode fails closed and remains available for the caller's
    visible recovery path.
    """
    if context.get("name") != name:
        return
    ownership = context["ownership"]
    label = context["label"]
    allow_rename_ctime = context.get("allow_rename_ctime", False)
    expected = context.get("expected")
    rebound = _open_guarded_binding(guard, name, label)
    try:
        identity_matches = (
            _binding_stable_identity_matches
            if allow_rename_ctime
            else _binding_identity_matches
        )
        if not identity_matches(rebound, ownership):
            raise ValueError(f"{label} cleanup ownership drift before unlink")
        if expected is not None and _binding_prestate(rebound) != expected:
            raise ValueError(f"{label} cleanup content drift before unlink")
        if not _stable_binding_matches(
            ownership["fd"],
            ownership,
            label,
            expected=expected,
            allow_rename_ctime=allow_rename_ctime,
        ):
            raise ValueError(f"{label} retained object drift before unlink")
    finally:
        os.close(rebound["fd"])


def _preserve_bound_unlink_residue(
    guard: dict, name: str, context: dict, label: str
) -> str | None:
    """Preserve an uncertain post-quarantine object under a recovery name."""
    output_name = context.get("recovery_output_name", name)
    suffix = context.get("recovery_suffix", "transaction-unsafe")
    if not _guarded_entry_exists(guard, name):
        return None
    moved = _move_entry_to_visible_recovery(
        guard,
        name,
        output_name,
        suffix,
        label,
    )
    if moved is None and _guarded_entry_exists(guard, name):
        raise ValueError(f"{label} cleanup recovery is blocked")
    return moved


def _unlinkat_kernel(dir_fd: int, name: str) -> None:
    """Remove one directory entry through the kernel boundary.

    No supported host primitive is allowed to claim exact-owner semantics here:
    both Darwin and POSIX ``unlinkat`` consume a directory entry name rather
    than a retained inode descriptor.  Keep this seam explicit so a future
    platform-specific fd-bound primitive can be added without reintroducing a
    name-based fallback.
    """
    raise _ExactOwnerCleanupUnavailable(
        "cleanup blocked: no exact-owner unlink-by-fd primitive"
    )


def _unlink_exact_owned_quarantined_entry(
    guard: dict,
    name: str,
    ownership: dict,
    expected: dict | None,
    label: str,
    *,
    allow_rename_ctime: bool,
) -> None:
    """Require an exact-owner deletion primitive at the final boundary.

    Keep the rebound descriptor open through the attempted syscall.  If the
    host cannot delete by retained inode descriptor, the syscall seam raises
    before any name-based unlink; the caller then publishes visible recovery
    and blocker residue.
    """
    rebound = _open_guarded_binding(guard, name, label)
    try:
        identity_matches = (
            _binding_stable_identity_matches
            if allow_rename_ctime
            else _binding_identity_matches
        )
        if not identity_matches(rebound, ownership):
            raise ValueError(f"{label} cleanup ownership drift at deletion boundary")
        if expected is not None and _binding_prestate(rebound) != expected:
            raise ValueError(f"{label} cleanup content drift at deletion boundary")
        if not _stable_binding_matches(
            ownership["fd"],
            ownership,
            label,
            expected=expected,
            allow_rename_ctime=allow_rename_ctime,
        ):
            raise ValueError(f"{label} retained object drift at deletion boundary")
        _assert_parent_guard(guard, label)
        _unlinkat_kernel(guard["fd"], name)
    finally:
        os.close(rebound["fd"])


def _write_bound_unlink_blocker(
    guard: dict, context: dict, label: str
) -> str | None:
    """Persist visible mode-0600 evidence when deletion is uncertain."""
    output_name = context.get("recovery_output_name", context.get("name", "cleanup"))
    suffix = context.get("blocked_suffix", "transaction-blocked")
    payload = context.get("blocked_content")
    if payload is None and suffix == "persistence-blocked":
        payload = _canonical_json_bytes(_blocked_pi_probe_result())
    if payload is None:
        payload = _canonical_json_bytes(
            {
                "category": "cleanup-deletion-uncertain",
                "label": label,
                "operation": "descriptor-relative-unlinkat",
                "schema_version": 1,
            }
        )
    previous_context = guard.pop("_bound_unlink_context", None)
    try:
        for _ in range(32):
            marker_name = _visible_recovery_name(output_name, suffix)
            try:
                _write_guarded_entry(
                    guard,
                    marker_name,
                    payload,
                    0o600,
                    f"{label} cleanup blocker",
                )
                os.fsync(guard["fd"])
                _assert_parent_guard(guard, f"{label} cleanup blocker")
                return marker_name
            except FileExistsError:
                continue
        raise ValueError(f"{label} cleanup blocker collision")
    finally:
        if previous_context is None:
            guard.pop("_bound_unlink_context", None)
        else:
            guard["_bound_unlink_context"] = previous_context


def _rewrite_bound_owned_content(
    guard: dict,
    name: str,
    ownership: dict,
    content: bytes,
    label: str,
    *,
    expected: dict | None,
) -> None:
    """Rewrite an owned inode through its already validated descriptor.

    The namespace name may have been replaced after the final quarantine bind,
    so reopening that name would either target an unrelated inode or fail to
    reach the retained object.  Production Pi ownership descriptors are
    writable and remain open across that boundary; use that descriptor for the
    BLOCKED rewrite and never resolve a replacement name.
    """
    del name
    descriptor = ownership.get("fd")
    if not isinstance(descriptor, int):
        raise ValueError(f"{label} retained descriptor is unavailable")
    try:
        flags = fcntl.fcntl(descriptor, fcntl.F_GETFL)
    except OSError as exc:
        raise ValueError(f"{label} retained descriptor is unavailable") from exc
    if (flags & os.O_ACCMODE) == os.O_RDONLY:
        raise ValueError(f"{label} retained descriptor is not writable")
    _assert_parent_guard(guard, label)
    current = _descriptor_binding(descriptor, label)
    if not _binding_stable_identity_matches(current, ownership):
        raise ValueError(f"{label} cleanup ownership drift while blocking")
    if expected is not None and _binding_prestate(current) != expected:
        raise ValueError(f"{label} cleanup content drift while blocking")
    blocked = bytes(content)
    os.ftruncate(descriptor, 0)
    os.lseek(descriptor, 0, os.SEEK_SET)
    _write_descriptor(descriptor, blocked)
    os.fsync(descriptor)
    rewritten = _descriptor_binding(descriptor, label)
    if (
        not _binding_object_identity_matches(rewritten, ownership)
        or rewritten["mode"] != ownership["mode"]
        or rewritten["sha256"] != hashlib.sha256(blocked).hexdigest()
    ):
        raise ValueError(f"{label} cleanup blocked rewrite drift")
    _assert_parent_guard(guard, label)


def _unlink_bound_quarantined_entry(
    guard: dict, name: str, context: dict
) -> None:
    """Quarantine, rebind, then unlink only the owned quarantine object.

    The initial name check is necessarily separate from the removal syscall.
    Move that name to a fresh no-replace quarantine name first, then validate
    the retained ownership binding against the actual quarantined object.  A
    collision or mismatch is preserved as visible recovery residue; no
    name-based unlink of the originally checked path is permitted.
    """
    label = context["label"]
    ownership = context["ownership"]
    expected = context.get("expected")
    allow_rename_ctime = context.get("allow_rename_ctime", False)
    _rebind_before_unlink(guard, name, context)
    quarantine_name = _visible_recovery_name(
        context.get("recovery_output_name", name),
        "transaction-unlink",
    )
    try:
        _renameatx(
            name,
            quarantine_name,
            RENAME_EXCL,
            source_dir_fd=guard["fd"],
            destination_dir_fd=guard["fd"],
        )
    except BaseException as exc:
        try:
            _preserve_bound_unlink_residue(guard, name, context, label)
        except BaseException as recovery_exc:
            raise ValueError(
                f"{label} cleanup quarantine collision recovery is blocked"
            ) from recovery_exc
        raise ValueError(f"{label} cleanup quarantine collision") from exc
    try:
        os.fsync(guard["fd"])
        _assert_parent_guard(guard, label)
        _require_retained_binding(
            guard,
            quarantine_name,
            ownership,
            label,
            expected=expected,
            allow_rename_ctime=allow_rename_ctime,
        )
        _unlink_exact_owned_quarantined_entry(
            guard,
            quarantine_name,
            ownership,
            expected,
            label,
            allow_rename_ctime=allow_rename_ctime,
        )
        context["deleted"] = True
    except BaseException as exc:
        try:
            if isinstance(exc, _ExactOwnerCleanupUnavailable):
                blocked_content = context.get("blocked_content")
                if blocked_content is not None:
                    quarantine_matches = _retained_binding_matches_name(
                        guard,
                        quarantine_name,
                        ownership,
                        label,
                        expected=expected,
                        allow_rename_ctime=allow_rename_ctime,
                    )
                    _rewrite_bound_owned_content(
                        guard,
                        quarantine_name,
                        ownership,
                        blocked_content,
                        label,
                        expected=expected,
                    )
                    context["recovery_suffix"] = (
                        "persistence-blocked"
                        if quarantine_matches
                        else "persistence-unsafe"
                    )
            if _guarded_entry_exists(guard, quarantine_name):
                _preserve_bound_unlink_residue(
                    guard, quarantine_name, context, label
                )
            if isinstance(exc, _ExactOwnerCleanupUnavailable):
                _write_bound_unlink_blocker(guard, context, label)
            elif not _guarded_entry_exists(guard, quarantine_name):
                _write_bound_unlink_blocker(guard, context, label)
        except BaseException as recovery_exc:
            raise ValueError(
                f"{label} cleanup quarantine recovery is blocked"
            ) from recovery_exc
        if isinstance(exc, _ExactOwnerCleanupUnavailable):
            raise
        raise ValueError(f"{label} cleanup quarantine ownership drift") from exc


def _guarded_unlink(guard: dict, name: str, *, missing_ok: bool = False) -> None:
    context = guard.get("_bound_unlink_context")
    if context is not None:
        _unlink_bound_quarantined_entry(guard, name, context)
        return
    try:
        os.unlink(name, dir_fd=guard["fd"])
    except FileNotFoundError:
        if not missing_ok:
            raise


def _write_guarded_entry(
    guard: dict, name: str, content: bytes, mode: int, label: str
) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(name, flags, mode, dir_fd=guard["fd"])
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb") as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        _assert_parent_guard(guard, label)
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        _guarded_unlink(guard, name, missing_ok=True)
        raise


def create_secure_backup(source, backup_dir, *, sensitive=False):
    """Create a non-discoverable backup; sensitive backups use mode 0600."""
    source_path = Path(source)
    metadata = _regular_file(source_path, "backup source")
    backup_root = Path(backup_dir)
    current = backup_root
    while not current.exists():
        if current.is_symlink():
            raise ValueError(f"backup directory cannot use symlinks: {backup_root}")
        current = current.parent
    if current.is_symlink() or backup_root.is_symlink():
        raise ValueError(f"backup directory cannot use symlinks: {backup_root}")
    resolved_backup = backup_root.resolve(strict=False)
    if "skills" in {part.lower() for part in resolved_backup.parts}:
        raise ValueError(f"backup directory must be outside skill discovery roots: {backup_root}")
    backup_root.mkdir(parents=True, exist_ok=True)
    if not backup_root.is_dir() or backup_root.is_symlink():
        raise ValueError(f"invalid backup directory: {backup_root}")
    descriptor, name = tempfile.mkstemp(prefix="cross-cli-backup-", dir=backup_root)
    backup = Path(name)
    try:
        mode = 0o600 if sensitive else stat.S_IMODE(metadata.st_mode)
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb") as output, source_path.open("rb") as input_file:
            for chunk in iter(lambda: input_file.read(65536), b""):
                output.write(chunk)
            output.flush()
            os.fsync(output.fileno())
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        backup.unlink(missing_ok=True)
        raise
    return backup


def _visible_recovery_name(output_name: str, suffix: str) -> str:
    return f"{output_name}.{suffix}.{uuid.uuid4().hex}"


def _move_entry_to_visible_recovery(
    parent_guard: dict,
    source_name: str,
    output_name: str,
    suffix: str,
    label: str,
) -> str | None:
    """Preserve an uncertain entry under an explicit, operator-visible name."""
    if not _guarded_entry_exists(parent_guard, source_name):
        return None
    for _ in range(32):
        destination_name = _visible_recovery_name(output_name, suffix)
        try:
            _renameatx(
                source_name,
                destination_name,
                RENAME_EXCL,
                source_dir_fd=parent_guard["fd"],
                destination_dir_fd=parent_guard["fd"],
            )
        except OSError as exc:
            if isinstance(exc, FileExistsError) or exc.errno in {
                errno.EEXIST, errno.ENOTEMPTY
            }:
                continue
            return None
        try:
            os.fsync(parent_guard["fd"])
        except OSError:
            pass
        return destination_name
    return None


def _cleanup_failed_same_directory_candidate(
    parent_guard: dict,
    candidate_name: str,
    output_name: str,
    ownership: dict | None,
    label: str,
) -> None:
    """Clean up a failed candidate without unlinking a substituted inode."""
    exact = False
    if ownership is not None:
        try:
            exact = _retained_binding_matches_name(
                parent_guard, candidate_name, ownership, label
            )
        except BaseException:
            exact = False
    if exact:
        try:
            _remove_bound_entry(
                parent_guard,
                candidate_name,
                ownership,
                output_name,
                label,
            )
            return
        except BaseException:
            # The name may have been replaced while cleanup was in progress.
            # Fall through to a visible, non-evidence recovery name.
            pass
    if _guarded_entry_exists(parent_guard, candidate_name):
        _move_entry_to_visible_recovery(
            parent_guard,
            candidate_name,
            output_name,
            "transaction-unsafe",
            label,
        )


def _write_same_directory_candidate(
    target: Path,
    content: bytes,
    mode: int,
    *,
    parent_guard: dict | None = None,
    label: str = "atomic destination",
) -> dict:
    if parent_guard is None:
        with _verified_parent(target, label) as owned_guard:
            return _write_same_directory_candidate(
                target,
                content,
                mode,
                parent_guard=owned_guard,
                label=label,
            )
    name = _visible_recovery_name(target.name, "transaction-pending")
    descriptor = None
    ownership = None
    try:
        flags = os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(
            os, "O_NOFOLLOW", 0
        )
        descriptor = os.open(name, flags, mode, dir_fd=parent_guard["fd"])
        os.fchmod(descriptor, mode)
        _write_descriptor(descriptor, bytes(content))
        ownership = _descriptor_binding(descriptor, label)
        os.fsync(descriptor)
        _assert_parent_guard(parent_guard, label)
        return {
            "path": parent_guard["path"] / name,
            "name": name,
            **ownership,
        }
    except BaseException:
        _cleanup_failed_same_directory_candidate(
            parent_guard, name, target.name, ownership, label
        )
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass
        raise


def _write_pi_probe_candidate(
    target: Path,
    content: bytes,
    mode: int,
    *,
    parent_guard: dict,
    blocked_content: bytes,
    label: str,
) -> dict:
    name = _visible_recovery_name(target.name, "persistence-pending")
    descriptor = None
    ownership = None
    try:
        flags = os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(
            os, "O_NOFOLLOW", 0
        )
        descriptor = os.open(name, flags, mode, dir_fd=parent_guard["fd"])
        os.fchmod(descriptor, mode)
        _write_descriptor(descriptor, bytes(content))
        ownership = _descriptor_binding(descriptor, label)
        os.fsync(descriptor)
        _assert_parent_guard(parent_guard, label)
    except BaseException:
        recovery_ownership = ownership
        if descriptor is not None and recovery_ownership is None:
            try:
                metadata = _descriptor_metadata(os.fstat(descriptor))
                if metadata["type"] == stat.S_IFREG:
                    recovery_ownership = {"fd": descriptor, **metadata}
            except (OSError, ValueError):
                recovery_ownership = None
        unsafe_name = None
        if descriptor is not None and recovery_ownership is not None:
            try:
                if _retained_object_binding_matches_name(
                    parent_guard, name, recovery_ownership, label
                ):
                    unsafe_name = _preserve_pi_entry_as_unsafe(
                        parent_guard, name, target.name, recovery_ownership, label
                    )
            except BaseException:
                # A name substitution is not evidence of ownership.  Keep any
                # resulting visible unsafe object, or leave the pending name
                # untouched, but never blindly move the current name again.
                pass
        blocked_name = None
        try:
            blocked_name = _create_pi_blocked_recovery(
                parent_guard, target.name, blocked_content, label
            )
        except BaseException:
            pass
        if (
            unsafe_name is not None
            and blocked_name is not None
            and ownership is not None
        ):
            try:
                _remove_exact_pi_unsafe_entry(
                    parent_guard,
                    unsafe_name,
                    ownership,
                    _binding_prestate(ownership),
                    label,
                )
            except BaseException:
                pass
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass
            descriptor = None
        raise
    return {
        "path": parent_guard["path"] / name,
        "name": name,
        "fd": descriptor,
        **ownership,
    }


def _guarded_identity_matches(guard: dict, name: str, ownership: dict) -> bool:
    try:
        metadata = os.stat(name, dir_fd=guard["fd"], follow_symlinks=False)
    except OSError:
        return False
    if not stat.S_ISREG(metadata.st_mode):
        return False
    return _binding_object_identity_matches(_descriptor_metadata(metadata), ownership)


def _rollback_exchange(
    temporary: Path,
    target: Path,
    candidate_state: dict,
    label: str,
    *,
    parent_guard: dict | None = None,
) -> None:
    if parent_guard is None:
        _renameatx(temporary, target, RENAME_SWAP)
        _fsync_directory(target.parent)
        rollback_temporary = capture_destination_prestate(temporary)
    else:
        _renameatx(
            temporary.name,
            target.name,
            RENAME_SWAP,
            source_dir_fd=parent_guard["fd"],
            destination_dir_fd=parent_guard["fd"],
        )
        os.fsync(parent_guard["fd"])
        rollback_temporary = _capture_guarded_prestate(
            parent_guard, temporary.name, label
        )
    try:
        if parent_guard is not None:
            _assert_parent_guard(parent_guard, label)
    except ValueError as exc:
        raise ValueError(
            f"destination exchange rollback is ambiguous: {label}; "
            f"preserved path: {temporary}"
        ) from exc
    if rollback_temporary != candidate_state:
        raise ValueError(
            f"destination exchange rollback is ambiguous: {label}; "
            f"preserved path: {temporary}"
        )


def _restore_exchange_after_candidate_mismatch(
    parent_guard: dict,
    temporary_name: str,
    target_name: str,
    displaced_ownership: dict,
    label: str,
    *,
    candidate_ownership: dict | None = None,
) -> None:
    """Restore the reviewed destination while preserving an unrelated candidate."""
    displaced_matches = _retained_binding_matches_name(
        parent_guard,
        temporary_name,
        displaced_ownership,
        label,
        allow_rename_ctime=True,
    )
    candidate_matches = candidate_ownership is not None and _retained_binding_matches_name(
        parent_guard,
        target_name,
        candidate_ownership,
        label,
        allow_rename_ctime=True,
    )
    # An exchange rollback is safe only while both retained namespace sides
    # still point at the reviewed displaced object and the written candidate.
    # A one-sided match is not enough: swapping in that state can overwrite a
    # live unrelated inode at the official destination.
    if not displaced_matches or not candidate_matches:
        # Neither side is safe to exchange in isolation.  Preserve every
        # currently named object under an explicit non-evidence recovery name
        # so the official destination cannot silently retain or publish an
        # uncertain inode while the caller reports the blocked boundary.
        for current_name in (target_name, temporary_name):
            if _guarded_entry_exists(parent_guard, current_name):
                _move_entry_to_visible_recovery(
                    parent_guard,
                    current_name,
                    target_name,
                    "transaction-unsafe",
                    label,
                )
        raise ValueError(
            f"destination exchange rollback is ambiguous: {label}"
        )
    _renameatx(
        temporary_name,
        target_name,
        RENAME_SWAP,
        source_dir_fd=parent_guard["fd"],
        destination_dir_fd=parent_guard["fd"],
    )
    os.fsync(parent_guard["fd"])
    _assert_parent_guard(parent_guard, label)
    if displaced_matches and not _retained_binding_matches_name(
        parent_guard,
        target_name,
        displaced_ownership,
        label,
        allow_rename_ctime=True,
    ):
        raise ValueError(
            f"destination exchange rollback is ambiguous: {label}"
        )
    if candidate_matches and not _retained_binding_matches_name(
        parent_guard,
        temporary_name,
        candidate_ownership,
        label,
        allow_rename_ctime=True,
    ):
        raise ValueError(
            f"destination exchange rollback is ambiguous: {label}"
        )


def _restore_create_after_candidate_mismatch(
    parent_guard: dict,
    target_name: str,
    candidate_name: str,
    label: str,
) -> None:
    """Move a substituted create destination back to its candidate name."""
    _renameatx(
        target_name,
        candidate_name,
        RENAME_EXCL,
        source_dir_fd=parent_guard["fd"],
        destination_dir_fd=parent_guard["fd"],
    )
    os.fsync(parent_guard["fd"])
    _assert_parent_guard(parent_guard, label)
    if _guarded_entry_exists(parent_guard, target_name):
        raise ValueError(f"destination create rollback is ambiguous: {label}")


def _remove_bound_entry(
    parent_guard: dict,
    name: str,
    ownership: dict,
    output_name: str,
    label: str,
    *,
    allow_rename_ctime: bool = False,
) -> None:
    """Remove only an exact retained object, preserving races as recovery files."""
    _require_retained_binding(
        parent_guard,
        name,
        ownership,
        label,
        allow_rename_ctime=allow_rename_ctime,
    )
    quarantine_name = _visible_recovery_name(output_name, "transaction-cleanup")
    _renameatx(
        name,
        quarantine_name,
        RENAME_EXCL,
        source_dir_fd=parent_guard["fd"],
        destination_dir_fd=parent_guard["fd"],
    )
    try:
        os.fsync(parent_guard["fd"])
        _assert_parent_guard(parent_guard, label)
        _require_retained_binding(
            parent_guard,
            quarantine_name,
            ownership,
            label,
            allow_rename_ctime=True,
        )
        previous_unlink_context = parent_guard.get("_bound_unlink_context")
        unlink_context = {
            "name": quarantine_name,
            "ownership": ownership,
            "expected": _binding_prestate(ownership),
            "label": label,
            "allow_rename_ctime": True,
            "recovery_output_name": output_name,
            "recovery_suffix": "transaction-unsafe",
            "blocked_suffix": "transaction-blocked",
        }
        parent_guard["_bound_unlink_context"] = unlink_context
        try:
            _guarded_unlink(parent_guard, quarantine_name)
        finally:
            if previous_unlink_context is None:
                parent_guard.pop("_bound_unlink_context", None)
            else:
                parent_guard["_bound_unlink_context"] = previous_unlink_context
        os.fsync(parent_guard["fd"])
        _assert_parent_guard(parent_guard, label)
    except BaseException:
        if unlink_context.get("deleted"):
            try:
                _write_bound_unlink_blocker(parent_guard, unlink_context, label)
            except BaseException as blocker_exc:
                raise ValueError(
                    f"{label} post-delete cleanup uncertainty is blocked"
                ) from blocker_exc
        if _guarded_entry_exists(parent_guard, quarantine_name):
            _move_entry_to_visible_recovery(
                parent_guard,
                quarantine_name,
                output_name,
                "transaction-unsafe",
                label,
            )
        raise


def atomic_replace(path, content, *, mode=None, expected_state=None, label=None):
    """Replace a reviewed file and validate the object displaced by the swap."""
    target = Path(path)
    review_label = label or "atomic replacement target"
    if not isinstance(content, (bytes, bytearray)):
        raise ValueError("atomic replacement content must be bytes")
    with _verified_parent(target, review_label) as parent_guard:
        actual = _capture_guarded_prestate(parent_guard, target.name, review_label)
        expected = (
            actual
            if expected_state is None
            else _validate_prestate_shape(expected_state, review_label)
        )
        if expected["kind"] != "file" or actual["kind"] != "file":
            raise ValueError(f"replacement pre-state must be a file: {review_label}")
        target_mode = actual["mode"] if mode is None else mode
        destination_binding = _open_guarded_binding(
            parent_guard, target.name, review_label
        )
        if _binding_prestate(destination_binding) != expected:
            os.close(destination_binding["fd"])
            raise ValueError(f"destination pre-state drift: {review_label}")
        candidate_bytes = bytes(content)
        candidate_state = {
            "kind": "file",
            "sha256": hashlib.sha256(candidate_bytes).hexdigest(),
            "mode": target_mode,
        }
        try:
            candidate = _write_same_directory_candidate(
                target,
                candidate_bytes,
                target_mode,
                parent_guard=parent_guard,
                label=review_label,
            )
        except BaseException:
            try:
                os.close(destination_binding["fd"])
            except OSError:
                pass
            raise
        temporary_name = candidate["name"]
        swapped = False
        restored = False
        candidate_consumed = False
        try:
            _assert_parent_guard(parent_guard, review_label)
            _require_retained_binding(
                parent_guard,
                temporary_name,
                candidate,
                review_label,
                expected=candidate_state,
            )
            _renameatx(
                temporary_name,
                target.name,
                RENAME_SWAP,
                source_dir_fd=parent_guard["fd"],
                destination_dir_fd=parent_guard["fd"],
            )
            swapped = True
            try:
                _require_retained_binding(
                    parent_guard,
                    target.name,
                    candidate,
                    review_label,
                    expected=candidate_state,
                    allow_rename_ctime=True,
                )
                _require_retained_binding(
                    parent_guard,
                    temporary_name,
                    destination_binding,
                    review_label,
                    expected=expected,
                    allow_rename_ctime=True,
                )
                os.fsync(parent_guard["fd"])
                _assert_parent_guard(parent_guard, review_label)
                _require_retained_binding(
                    parent_guard,
                    target.name,
                    candidate,
                    review_label,
                    expected=candidate_state,
                    allow_rename_ctime=True,
                )
                _require_retained_binding(
                    parent_guard,
                    temporary_name,
                    destination_binding,
                    review_label,
                    expected=expected,
                    allow_rename_ctime=True,
                )
            except BaseException as exc:
                try:
                    _restore_exchange_after_candidate_mismatch(
                        parent_guard,
                        temporary_name,
                        target.name,
                        destination_binding,
                        review_label,
                        candidate_ownership=candidate,
                    )
                    restored = True
                except BaseException as rollback_exc:
                    raise ValueError(
                        f"destination mutation-boundary drift rollback is blocked: "
                        f"{review_label}; preserved path: "
                        f"{parent_guard['path'] / temporary_name}"
                    ) from rollback_exc
                raise ValueError(
                    f"destination mutation-boundary drift: {review_label}"
                ) from exc
            try:
                _remove_bound_entry(
                    parent_guard,
                    temporary_name,
                    destination_binding,
                    target.name,
                    review_label,
                    allow_rename_ctime=True,
                )
            except _ExactOwnerCleanupUnavailable:
                # The candidate is already installed by the verified atomic
                # exchange.  Keep the displaced object and blocker visible;
                # only the cleanup sub-operation is blocked on this host.
                candidate_consumed = True
        finally:
            if swapped and not restored and not candidate_consumed:
                try:
                    if _retained_binding_matches_name(
                        parent_guard,
                        target.name,
                        candidate,
                        review_label,
                        expected=candidate_state,
                        allow_rename_ctime=True,
                    ) and _retained_binding_matches_name(
                        parent_guard,
                        temporary_name,
                        destination_binding,
                        review_label,
                        expected=expected,
                        allow_rename_ctime=True,
                    ):
                        _restore_exchange_after_candidate_mismatch(
                            parent_guard,
                            temporary_name,
                            target.name,
                            destination_binding,
                            review_label,
                            candidate_ownership=candidate,
                        )
                        restored = True
                except BaseException:
                    pass
            if not candidate_consumed and not restored:
                _move_entry_to_visible_recovery(
                    parent_guard,
                    temporary_name,
                    target.name,
                    "transaction-unsafe",
                    review_label,
                )
            os.close(candidate["fd"])
            os.close(destination_binding["fd"])
    return target


def atomic_create(
    path,
    content,
    *,
    mode=0o644,
    expected_state=None,
    label=None,
    parent_guard=None,
):
    """Install a fully written candidate only while the destination is absent."""
    target = Path(path)
    review_label = label or "atomic creation target"
    if not isinstance(content, (bytes, bytearray)):
        raise ValueError("atomic creation content must be bytes")
    if parent_guard is None:
        with _verified_parent(target, review_label) as owned_guard:
            return atomic_create(
                target,
                content,
                mode=mode,
                expected_state=expected_state,
                label=review_label,
                parent_guard=owned_guard,
            )
    _assert_parent_guard(parent_guard, review_label)
    actual = _capture_guarded_prestate(parent_guard, target.name, review_label)
    if actual != {"kind": "absent"}:
        raise FileExistsError(f"create target already exists: {target}")
    expected = (
        actual
        if expected_state is None
        else _validate_prestate_shape(expected_state, review_label)
    )
    if expected != {"kind": "absent"}:
        raise ValueError(f"creation pre-state must be absent: {review_label}")
    candidate = _write_same_directory_candidate(
        target,
        bytes(content),
        mode,
        parent_guard=parent_guard,
        label=review_label,
    )
    candidate_name = candidate["name"]
    installed = False
    restored = False
    try:
        _assert_parent_guard(parent_guard, review_label)
        candidate_state = {
            "kind": "file",
            "sha256": hashlib.sha256(bytes(content)).hexdigest(),
            "mode": mode,
        }
        _require_retained_binding(
            parent_guard,
            candidate_name,
            candidate,
            review_label,
            expected=candidate_state,
        )
        try:
            _renameatx(
                candidate_name,
                target.name,
                RENAME_EXCL,
                source_dir_fd=parent_guard["fd"],
                destination_dir_fd=parent_guard["fd"],
            )
        except OSError as exc:
            if exc.errno in {errno.EEXIST, errno.ENOTEMPTY}:
                raise ValueError(
                    f"destination mutation-boundary drift: {review_label}"
                ) from exc
            raise
        installed = True
        try:
            _require_retained_binding(
                parent_guard,
                target.name,
                candidate,
                review_label,
                expected=candidate_state,
                allow_rename_ctime=True,
            )
        except BaseException as exc:
            try:
                _restore_create_after_candidate_mismatch(
                    parent_guard, target.name, candidate_name, review_label
                )
                restored = True
            except BaseException as rollback_exc:
                raise ValueError(
                    f"destination mutation-boundary drift rollback is blocked: "
                    f"{review_label}; preserved path: "
                    f"{parent_guard['path'] / target.name}"
                ) from rollback_exc
            raise ValueError(
                f"destination mutation-boundary drift: {review_label}"
            ) from exc
        os.fsync(parent_guard["fd"])
        try:
            _assert_parent_guard(parent_guard, review_label)
            _require_retained_binding(
                parent_guard,
                target.name,
                candidate,
                review_label,
                expected=candidate_state,
                allow_rename_ctime=True,
            )
        except BaseException:
            if installed and not restored:
                try:
                    _restore_create_after_candidate_mismatch(
                        parent_guard, target.name, candidate_name, review_label
                    )
                    restored = True
                except BaseException as rollback_exc:
                    raise ValueError(
                        f"destination create rollback is blocked: {review_label}"
                    ) from rollback_exc
            raise
    finally:
        if not restored and _guarded_entry_exists(parent_guard, candidate_name):
            _move_entry_to_visible_recovery(
                parent_guard,
                candidate_name,
                target.name,
                "transaction-unsafe",
                review_label,
            )
        os.close(candidate["fd"])
    return target


def apply_sync_transaction(operations, backup_dir, *, verify=None):
    """Apply operations as a group or restore already changed files."""
    if not isinstance(operations, list) or not operations:
        raise ValueError("sync transaction requires operations")
    backups: list[tuple[Path, Path, int]] = []
    created_files: list[tuple[Path, dict, str]] = []
    created_directories: list[dict] = []
    try:
        for operation in operations:
            if not isinstance(operation, dict) or not {"path", "content"} <= set(operation):
                raise ValueError("sync operation fields are invalid")
            target = Path(operation["path"])
            if operation.get("create"):
                if target.exists() or target.is_symlink():
                    raise FileExistsError(f"create target already exists: {target}")
                continue
            metadata = _regular_file(target, "sync target")
            backup = create_secure_backup(target, backup_dir, sensitive=bool(operation.get("sensitive", False)))
            backups.append((target, backup, stat.S_IMODE(metadata.st_mode)))
        for operation in operations:
            if operation.get("inject_failure"):
                raise RuntimeError("injected sync failure")
            target = Path(operation["path"])
            if operation.get("create"):
                label = os.fspath(target)
                with _verified_parent_with_creation(
                    target,
                    label,
                    _missing_parents(target.parent),
                    created_directories,
                ) as (parent_guard, new_records):
                    created_directories.extend(new_records)
                    atomic_create(
                        target,
                        operation["content"],
                        mode=operation.get("mode", 0o644),
                        expected_state={"kind": "absent"},
                        label=label,
                        parent_guard=parent_guard,
                    )
                created_files.append(
                    (target, capture_destination_prestate(target), label)
                )
            else:
                atomic_replace(target, operation["content"], mode=operation.get("mode"))
        if verify is not None:
            verify()
    except BaseException:
        for target, backup, original_mode in reversed(backups):
            atomic_replace(target, backup.read_bytes(), mode=original_mode)
        for target, state, label in reversed(created_files):
            _atomic_remove_if_matches(target, state, label)
        for record in sorted(
            created_directories,
            key=lambda item: len(Path(item["logical_path"]).parts),
            reverse=True,
        ):
            _remove_created_directory(record, "sync transaction created parent")
        raise
    return [backup for _, backup, _ in backups]


def _canonical_json_bytes(value) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )


def _value_sha256(value) -> str:
    return hashlib.sha256(_canonical_json_bytes(value)).hexdigest()


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _ensure_private_directory(path: Path) -> Path:
    directory = Path(path)
    missing: list[Path] = []
    current = directory
    while not current.exists():
        if current.is_symlink():
            raise ValueError(f"private directory cannot use symlinks: {directory}")
        missing.append(current)
        current = current.parent
    if not current.is_dir() or current.is_symlink():
        raise ValueError(f"invalid private directory parent: {current}")
    for item in reversed(missing):
        item.mkdir(mode=0o700)
        _fsync_directory(item.parent)
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError(f"invalid private directory: {directory}")
    metadata = directory.stat(follow_symlinks=False)
    if stat.S_IMODE(metadata.st_mode) != 0o700:
        raise ValueError(f"private directory must use mode 0700: {directory}")
    return directory


def _assert_runtime_root_outside_discovery(
    plan: dict, runtime_root: Path, label: str
) -> Path:
    candidate = Path(runtime_root)
    resolved_candidate = candidate.resolve(strict=False)
    for target_id in TARGET_ORDER:
        discovery_root = Path(
            plan["targets"][target_id]["skills_root"]
        ).resolve(strict=True)
        try:
            resolved_candidate.relative_to(discovery_root)
        except ValueError:
            continue
        raise ValueError(
            f"{label} must remain outside every Skill discovery root: {candidate}"
        )
    return candidate


def _assert_runtime_private_roots(
    plan: dict,
    *,
    backup_root: Path | None = None,
    transaction_root: Path | None = None,
) -> None:
    if backup_root is not None:
        _assert_runtime_root_outside_discovery(plan, backup_root, "backup root")
    if transaction_root is not None:
        _assert_runtime_root_outside_discovery(
            plan, transaction_root, "transaction root"
        )


def _write_exclusive_fsynced(path: Path, content: bytes, *, mode: int = 0o600) -> Path:
    target = Path(path)
    if not isinstance(content, (bytes, bytearray)):
        raise ValueError("exclusive content must be bytes")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(target, flags, mode)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb") as output:
            output.write(bytes(content))
            output.flush()
            os.fsync(output.fileno())
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        target.unlink(missing_ok=True)
        raise
    return target


def _renameatx(
    source: Path | str,
    destination: Path | str,
    flags: int,
    *,
    source_dir_fd: int = AT_FDCWD,
    destination_dir_fd: int = AT_FDCWD,
) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    function = getattr(libc, "renameatx_np", None)
    if function is None:
        raise ValueError("renameatx_np is required for durable receipts")
    function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    function.restype = ctypes.c_int
    result = function(
        source_dir_fd,
        os.fsencode(source),
        destination_dir_fd,
        os.fsencode(destination),
        flags,
    )
    if result != 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error), os.fspath(destination))


@contextmanager
def _target_transaction_lock(
    transaction_root: Path, target_id: str, plan: dict
):
    _assert_runtime_private_roots(plan, transaction_root=transaction_root)
    root = _ensure_private_directory(transaction_root)
    lock_path = root / f"{target_id}.lock"
    flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(lock_path, flags, 0o600)
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or stat.S_IMODE(metadata.st_mode) != 0o600:
            raise ValueError("transaction lock must be a mode-0600 regular file")
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError(f"transaction lock is already held: {target_id}") from exc
        os.fsync(descriptor)
        _fsync_directory(root)
        yield
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def _validate_receipt_shape(receipt: dict) -> dict:
    required = {
        "schema_version",
        "target",
        "plan_sha256",
        "destination_preimage_sha256",
        "candidate_sha256",
        "backup_manifest_sha256",
        "transaction_id",
        "revision",
        "previous_receipt_sha256",
        "state",
    }
    optional = {
        "content_verification_sha256",
        "created_parent_records",
        "discovery_verification_sha256",
        "recovery_reason",
    }
    if not isinstance(receipt, dict) or not required <= set(receipt):
        raise ValueError("transaction receipt fields are invalid")
    if set(receipt) - required - optional:
        raise ValueError("transaction receipt has unexpected fields")
    if receipt["schema_version"] != RECEIPT_SCHEMA_VERSION:
        raise ValueError("transaction receipt schema is invalid")
    if receipt["target"] not in TARGET_IDS:
        raise ValueError("transaction receipt target is invalid")
    for field in (
        "plan_sha256",
        "destination_preimage_sha256",
        "candidate_sha256",
        "backup_manifest_sha256",
    ):
        if not isinstance(receipt[field], str) or not re.fullmatch(
            r"[0-9a-f]{64}", receipt[field]
        ):
            raise ValueError(f"transaction receipt {field} is invalid")
    if not _nonblank(receipt["transaction_id"]):
        raise ValueError("transaction receipt ID is invalid")
    if type(receipt["revision"]) is not int or receipt["revision"] < 1:
        raise ValueError("transaction receipt revision is invalid")
    previous = receipt["previous_receipt_sha256"]
    if receipt["revision"] == 1:
        if previous is not None:
            raise ValueError("initial receipt previous hash must be null")
    elif not isinstance(previous, str) or not re.fullmatch(r"[0-9a-f]{64}", previous):
        raise ValueError("transaction receipt previous hash is invalid")
    if receipt["state"] not in RECEIPT_PENDING_STATES | RECEIPT_TERMINAL_STATES:
        raise ValueError("transaction receipt state is invalid")
    for field in ("content_verification_sha256", "discovery_verification_sha256"):
        if field in receipt and not re.fullmatch(r"[0-9a-f]{64}", receipt[field]):
            raise ValueError(f"transaction receipt {field} is invalid")
    if "recovery_reason" in receipt and not _nonblank(receipt["recovery_reason"]):
        raise ValueError("transaction receipt recovery reason is invalid")
    if "created_parent_records" in receipt:
        _validate_created_parent_records(receipt["created_parent_records"])
    return receipt


def _read_receipt(path: Path) -> tuple[dict, str]:
    receipt_path = Path(path)
    metadata = _regular_file(receipt_path, "transaction receipt")
    if receipt_path.is_symlink() or stat.S_IMODE(metadata.st_mode) != 0o600:
        raise ValueError("transaction receipt must be a mode-0600 regular file")
    raw = receipt_path.read_bytes()
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("transaction receipt JSON is invalid") from exc
    return _validate_receipt_shape(value), hashlib.sha256(raw).hexdigest()


def _install_initial_receipt(path: Path, receipt: dict) -> dict:
    receipt_path = Path(path)
    _validate_receipt_shape(receipt)
    with _verified_parent(receipt_path, "transaction receipt") as parent_guard:
        if _capture_guarded_prestate(
            parent_guard, receipt_path.name, "transaction receipt"
        ) != {"kind": "absent"}:
            raise ValueError("transaction receipt already exists")
        temporary_name = f".{receipt_path.name}.tmp-{uuid.uuid4().hex}"
        _write_guarded_entry(
            parent_guard,
            temporary_name,
            _canonical_json_bytes(receipt),
            0o600,
            "transaction receipt",
        )
        installed = False
        try:
            _assert_parent_guard(parent_guard, "transaction receipt")
            _renameatx(
                temporary_name,
                receipt_path.name,
                RENAME_EXCL,
                source_dir_fd=parent_guard["fd"],
                destination_dir_fd=parent_guard["fd"],
            )
            installed = True
            os.fsync(parent_guard["fd"])
            _assert_parent_guard(parent_guard, "transaction receipt")
        except BaseException as exc:
            if installed:
                try:
                    _renameatx(
                        receipt_path.name,
                        temporary_name,
                        RENAME_EXCL,
                        source_dir_fd=parent_guard["fd"],
                        destination_dir_fd=parent_guard["fd"],
                    )
                    os.fsync(parent_guard["fd"])
                except BaseException as rollback_exc:
                    raise ValueError(
                        "initial receipt parent drift rollback is blocked"
                    ) from rollback_exc
            raise exc
        finally:
            _guarded_unlink(parent_guard, temporary_name, missing_ok=True)
    return receipt


def _install_receipt_transition_blocker(
    parent_guard: dict,
    receipt: dict,
    live_receipt_sha256: str,
) -> str:
    name = f"{receipt['target']}.manual-disposition.json"
    value = {
        "schema_version": 1,
        "target": receipt["target"],
        "plan_sha256": receipt["plan_sha256"],
        "receipt_sha256": live_receipt_sha256,
        "category": "receipt-history-transition-in-progress",
        "required_action": "control-plane manual disposition",
    }
    _write_guarded_entry(
        parent_guard,
        name,
        _canonical_json_bytes(value),
        0o600,
        "receipt transition blocker",
    )
    os.fsync(parent_guard["fd"])
    _assert_parent_guard(parent_guard, "receipt transition blocker")
    return name


def _advance_receipt(path: Path, state: str, **updates) -> dict:
    receipt_path = Path(path)
    current, current_sha = _read_receipt(receipt_path)
    revised = dict(current)
    revised.update(updates)
    revised.update(
        revision=current["revision"] + 1,
        previous_receipt_sha256=current_sha,
        state=state,
    )
    _validate_receipt_shape(revised)
    history = _ensure_private_directory(receipt_path.parent / "history")
    history_path = history / f"{current['target']}-revision-{current['revision']}.json"
    with _verified_parent(receipt_path, "transaction receipt") as parent_guard:
        current_state = {
            "kind": "file",
            "sha256": current_sha,
            "mode": 0o600,
        }
        if _capture_guarded_prestate(
            parent_guard, receipt_path.name, "transaction receipt"
        ) != current_state:
            raise ValueError("receipt mutation-boundary drift")
        temporary_name = f".{receipt_path.name}.tmp-{uuid.uuid4().hex}"
        temporary = parent_guard["path"] / temporary_name
        revised_bytes = _canonical_json_bytes(revised)
        candidate_state = {
            "kind": "file",
            "sha256": hashlib.sha256(revised_bytes).hexdigest(),
            "mode": 0o600,
        }
        _write_guarded_entry(
            parent_guard,
            temporary_name,
            revised_bytes,
            0o600,
            "transaction receipt",
        )
        safe_to_remove_temporary = True
        with _verified_parent(history_path, "transaction receipt history") as history_guard:
            try:
                _assert_parent_guard(parent_guard, "transaction receipt")
                _assert_parent_guard(history_guard, "transaction receipt history")
                _renameatx(
                    temporary_name,
                    receipt_path.name,
                    RENAME_SWAP,
                    source_dir_fd=parent_guard["fd"],
                    destination_dir_fd=parent_guard["fd"],
                )
                safe_to_remove_temporary = False
                os.fsync(parent_guard["fd"])
                _assert_parent_guard(parent_guard, "transaction receipt")
                displaced = _capture_guarded_prestate(
                    parent_guard, temporary_name, "displaced transaction receipt"
                )
                if displaced != current_state:
                    try:
                        _rollback_exchange(
                            temporary,
                            receipt_path,
                            candidate_state,
                            "transaction receipt",
                            parent_guard=parent_guard,
                        )
                        safe_to_remove_temporary = True
                    except BaseException as exc:
                        raise ValueError(
                            "receipt mutation-boundary drift rollback is blocked; "
                            f"preserved path: {temporary}"
                        ) from exc
                    raise ValueError("receipt mutation-boundary drift")
                history_installed = False
                blocker_name = None
                try:
                    blocker_name = _install_receipt_transition_blocker(
                        parent_guard,
                        current,
                        candidate_state["sha256"],
                    )
                    _assert_parent_guard(history_guard, "transaction receipt history")
                    _renameatx(
                        temporary_name,
                        history_path.name,
                        RENAME_EXCL,
                        source_dir_fd=parent_guard["fd"],
                        destination_dir_fd=history_guard["fd"],
                    )
                    history_installed = True
                    os.fsync(history_guard["fd"])
                    os.fsync(parent_guard["fd"])
                    _assert_parent_guard(parent_guard, "transaction receipt")
                    _assert_parent_guard(history_guard, "transaction receipt history")
                    _guarded_unlink(parent_guard, blocker_name)
                    os.fsync(parent_guard["fd"])
                    _assert_parent_guard(parent_guard, "transaction receipt")
                    blocker_name = None
                except BaseException as exc:
                    if history_installed:
                        try:
                            history_state = _capture_guarded_prestate(
                                history_guard,
                                history_path.name,
                                "transaction receipt history",
                            )
                            if history_state != current_state:
                                raise ValueError("transaction receipt history is ambiguous")
                            _renameatx(
                                receipt_path.name,
                                history_path.name,
                                RENAME_SWAP,
                                source_dir_fd=parent_guard["fd"],
                                destination_dir_fd=history_guard["fd"],
                            )
                            os.fsync(parent_guard["fd"])
                            os.fsync(history_guard["fd"])
                            if _capture_guarded_prestate(
                                parent_guard,
                                receipt_path.name,
                                "transaction receipt",
                            ) != current_state:
                                raise ValueError("transaction receipt rollback is ambiguous")
                            if _capture_guarded_prestate(
                                history_guard,
                                history_path.name,
                                "transaction receipt history",
                            ) != candidate_state:
                                raise ValueError("transaction receipt rollback is ambiguous")
                            _guarded_unlink(history_guard, history_path.name)
                            os.fsync(history_guard["fd"])
                            if blocker_name is not None:
                                _guarded_unlink(
                                    parent_guard, blocker_name, missing_ok=True
                                )
                                os.fsync(parent_guard["fd"])
                                blocker_name = None
                        except BaseException as rollback_exc:
                            raise ValueError(
                                "receipt history installation rollback is blocked"
                            ) from rollback_exc
                    else:
                        try:
                            _rollback_exchange(
                                temporary,
                                receipt_path,
                                candidate_state,
                                "transaction receipt",
                                parent_guard=parent_guard,
                            )
                            safe_to_remove_temporary = True
                            if blocker_name is not None:
                                _guarded_unlink(
                                    parent_guard, blocker_name, missing_ok=True
                                )
                                os.fsync(parent_guard["fd"])
                                blocker_name = None
                        except BaseException as rollback_exc:
                            raise ValueError(
                                "receipt history installation rollback is blocked; "
                                f"preserved path: {temporary}"
                            ) from rollback_exc
                    raise exc
            finally:
                if safe_to_remove_temporary:
                    _guarded_unlink(parent_guard, temporary_name, missing_ok=True)
    return revised


def _missing_parents(path: Path) -> list[str]:
    missing: list[Path] = []
    current = path
    while not current.exists():
        if current.is_symlink():
            raise ValueError(f"destination parent cannot use symlinks: {current}")
        missing.append(current)
        current = current.parent
    if not current.is_dir() or current.is_symlink():
        raise ValueError(f"invalid destination parent: {current}")
    return [str(item) for item in reversed(missing)]


def _target_candidate_entries(plan: dict, target_id: str) -> list[dict]:
    target = plan["targets"][target_id]
    skills_root = Path(target["skills_root"])
    entries: list[dict] = []
    for item in target["files"]:
        source_root = Path(plan["sources"][item["source_alias"]])
        source = validate_relative_path(source_root, item["path"])
        if _sha256(source) != item["sha256"]:
            raise ValueError(f"source SHA-256 drift: {item['skill']}/{item['path']}")
        destination = Path(item["destination"])
        _contained(skills_root, destination, "skill destination")
        pre_state = _validate_prestate_shape(
            item["pre_state"], f"{target_id}:{item['skill']}/{item['path']}"
        )
        content = source.read_bytes()
        mode = pre_state.get("mode", 0o644)
        entries.append(
            {
                "path": str(destination),
                "label": f"{item['skill']}/{item['path']}",
                "pre_state": pre_state,
                "candidate_sha256": hashlib.sha256(content).hexdigest(),
                "candidate_mode": mode,
                "created_parents": _missing_parents(destination.parent),
                "content": content,
                "sensitive": False,
            }
        )
    rule_binding, rule_selected = _target_rule_binding(plan, target_id)
    if not rule_selected:
        return entries
    rule = plan["managed_rules"]
    rule_source = validate_relative_path(
        Path(plan["sources"][rule["source_alias"]]), rule["path"]
    )
    if _sha256(rule_source) != rule["sha256"]:
        raise ValueError("managed-rule source SHA-256 drift")
    rule_file = Path(rule_binding["destination"])
    pre_state = _validate_prestate_shape(
        rule_binding["pre_state"], f"{target_id}:global-rule"
    )
    if pre_state["kind"] != "file":
        raise ValueError("global rule pre-state must be a file")
    original = rule_file.read_text(encoding="utf-8")
    updated = install_managed_block(
        original,
        rule_source.read_text(encoding="utf-8"),
        version=rule["version"],
    ).encode("utf-8")
    entries.append(
        {
            "path": str(rule_file),
            "label": "global-rule",
            "pre_state": pre_state,
            "candidate_sha256": hashlib.sha256(updated).hexdigest(),
            "candidate_mode": pre_state["mode"],
            "created_parents": [],
            "content": updated,
            "sensitive": True,
        }
    )
    return entries


def _manifest_entry(entry: dict, object_name: str | None) -> dict:
    value = {
        "path": entry["path"],
        "label": entry["label"],
        "pre_state": entry["pre_state"],
        "candidate_sha256": entry["candidate_sha256"],
        "candidate_mode": entry["candidate_mode"],
        "created_parents": entry["created_parents"],
        "backup_object": object_name,
        "backup_sha256": None,
    }
    return value


def _prepare_target_backup(
    plan: dict,
    target_id: str,
    plan_sha256: str,
    backup_root: Path,
    transaction_id: str,
) -> tuple[dict, str, list[dict]]:
    _assert_runtime_private_roots(plan, backup_root=backup_root)
    root = _ensure_private_directory(Path(backup_root))
    target_root = root / target_id
    if target_root.exists() or target_root.is_symlink():
        raise ValueError(f"target backup already exists: {target_id}")
    target_root.mkdir(mode=0o700)
    _fsync_directory(root)
    objects = target_root / "objects"
    objects.mkdir(mode=0o700)
    _fsync_directory(target_root)

    candidates = _target_candidate_entries(plan, target_id)
    manifest_entries: list[dict] = []
    for index, entry in enumerate(candidates, 1):
        pre_state = entry["pre_state"]
        object_name = None
        manifest_entry = _manifest_entry(entry, object_name)
        if pre_state["kind"] == "file":
            source = Path(entry["path"])
            assert_destination_prestate(source, pre_state, entry["label"])
            object_name = f"object-{index:04d}.bin"
            object_path = objects / object_name
            content = source.read_bytes()
            _write_exclusive_fsynced(object_path, content, mode=0o600)
            manifest_entry["backup_object"] = f"objects/{object_name}"
            manifest_entry["backup_sha256"] = hashlib.sha256(content).hexdigest()
        manifest_entries.append(manifest_entry)
    _fsync_directory(objects)

    manifest = {
        "schema_version": 1,
        "target": target_id,
        "plan_sha256": plan_sha256,
        "transaction_id": transaction_id,
        "entries": manifest_entries,
    }
    manifest_path = target_root / "manifest.json"
    _write_exclusive_fsynced(manifest_path, _canonical_json_bytes(manifest), mode=0o600)
    _fsync_directory(target_root)
    _fsync_directory(root)
    manifest_sha = _sha256(manifest_path)
    if _load_json(manifest_path) != manifest:
        raise ValueError("backup manifest re-open verification failed")
    for entry in manifest_entries:
        if entry["backup_object"] is None:
            continue
        object_path = target_root / entry["backup_object"]
        if _sha256(object_path) != entry["backup_sha256"]:
            raise ValueError("backup object re-open verification failed")
    return manifest, manifest_sha, candidates


def _closure_digest(entries: list[dict], key: str) -> str:
    if key == "pre_state":
        value = [
            {"path": entry["path"], "pre_state": entry["pre_state"]}
            for entry in entries
        ]
    elif key == "candidate":
        value = [
            {
                "path": entry["path"],
                "sha256": entry["candidate_sha256"],
                "mode": entry["candidate_mode"],
            }
            for entry in entries
        ]
    else:
        raise ValueError("unknown closure digest")
    return _value_sha256(value)


def _receipt_path_for(root: Path, target_id: str) -> Path:
    return Path(root) / f"{target_id}.json"


def _orphaned_receipt_temporaries(transaction_root: Path) -> list[Path]:
    return sorted(
        Path(transaction_root).glob(".*.json.tmp-*"),
        key=lambda item: item.name,
    )


def _assert_no_transaction_blockers(transaction_root: Path) -> None:
    root = Path(transaction_root)
    if list(root.glob("*.manual-disposition.json")):
        raise ValueError("manual transaction disposition blocks this operation")
    if _orphaned_receipt_temporaries(root):
        raise ValueError("orphaned receipt temporary blocks this operation")


def _require_prior_targets_verified(
    transaction_root: Path, target_id: str, plan_sha256: str
) -> None:
    root = Path(transaction_root)
    _assert_no_transaction_blockers(root)
    target_index = TARGET_ORDER.index(target_id)
    for prior in TARGET_ORDER[:target_index]:
        receipt, _ = _read_receipt(_receipt_path_for(root, prior))
        if receipt["state"] != "verified" or receipt["plan_sha256"] != plan_sha256:
            raise ValueError(f"prior target is not verified: {prior}")
    for later in TARGET_ORDER[target_index + 1 :]:
        if _receipt_path_for(root, later).exists():
            raise ValueError(f"later target already started: {later}")


def _invoke_crash_hook(crash_hook, point: str) -> None:
    if crash_hook is not None:
        crash_hook(point)


def _install_candidate_entry(
    entry: dict,
    known_created_parents: list[dict] | None = None,
    record_created_parents=None,
) -> None:
    path = Path(entry["path"])
    assert_destination_prestate(path, entry["pre_state"], entry["label"])
    if entry["pre_state"]["kind"] == "absent":
        known = [] if known_created_parents is None else known_created_parents
        with _verified_parent_with_creation(
            path,
            entry["label"],
            entry.get("created_parents", _missing_parents(path.parent)),
            known,
        ) as (parent_guard, new_records):
            if new_records:
                if record_created_parents is None:
                    raise ValueError("created-parent evidence callback is required")
                record_created_parents(new_records)
            atomic_create(
                path,
                entry["content"],
                mode=entry["candidate_mode"],
                expected_state=entry["pre_state"],
                label=entry["label"],
                parent_guard=parent_guard,
            )
    else:
        atomic_replace(
            path,
            entry["content"],
            mode=entry["candidate_mode"],
            expected_state=entry["pre_state"],
            label=entry["label"],
        )


def apply_target(
    plan: dict,
    target_id: str,
    backup_root: Path,
    transaction_receipt: Path,
    *,
    plan_sha256: str,
    crash_hook=None,
) -> dict:
    """Apply one target inside a durable receipt-bound recovery window."""
    if target_id not in TARGET_IDS:
        raise ValueError(f"unknown target: {target_id}")
    receipt_path = Path(transaction_receipt)
    if receipt_path.name != f"{target_id}.json":
        raise ValueError("transaction receipt name must bind the target")
    transaction_root = receipt_path.parent
    _assert_runtime_private_roots(
        plan,
        backup_root=backup_root,
        transaction_root=transaction_root,
    )
    with _target_transaction_lock(transaction_root, target_id, plan):
        _require_prior_targets_verified(transaction_root, target_id, plan_sha256)
        if receipt_path.exists() or receipt_path.is_symlink():
            raise ValueError("transaction receipt already exists")
        _assert_target_prestate(plan, target_id)
        transaction_id = uuid.uuid4().hex
        manifest, manifest_sha, candidates = _prepare_target_backup(
            plan, target_id, plan_sha256, Path(backup_root), transaction_id
        )
        _invoke_crash_hook(crash_hook, "after-backup-before-prepared")
        initial = {
            "schema_version": RECEIPT_SCHEMA_VERSION,
            "target": target_id,
            "plan_sha256": plan_sha256,
            "destination_preimage_sha256": _closure_digest(
                manifest["entries"], "pre_state"
            ),
            "candidate_sha256": _closure_digest(manifest["entries"], "candidate"),
            "backup_manifest_sha256": manifest_sha,
            "transaction_id": transaction_id,
            "revision": 1,
            "previous_receipt_sha256": None,
            "state": "prepared",
        }
        _install_initial_receipt(receipt_path, initial)
        try:
            _invoke_crash_hook(crash_hook, "after-prepared-before-intent")
            _advance_receipt(receipt_path, "mutation-intent")
            created_parent_records: list[dict] = []

            def persist_created_parents(new_records: list[dict]) -> None:
                created_parent_records.extend(new_records)
                _validate_created_parent_records(created_parent_records)
                _advance_receipt(
                    receipt_path,
                    "mutation-intent",
                    created_parent_records=list(created_parent_records),
                )

            for index, entry in enumerate(candidates):
                _install_candidate_entry(
                    entry,
                    created_parent_records,
                    persist_created_parents,
                )
                if index == 0:
                    _invoke_crash_hook(crash_hook, "after-first-destination-write")
            _invoke_crash_hook(
                crash_hook, "after-last-destination-fsync-before-applied"
            )
            return _advance_receipt(receipt_path, "applied-uncommitted")
        except Exception:
            try:
                _restore_target_locked(
                    plan,
                    target_id,
                    plan_sha256,
                    Path(backup_root),
                    receipt_path,
                )
            except Exception:
                pass
            raise


def _load_verified_backup_manifest(
    receipt: dict, backup_root: Path, target_id: str, plan_sha256: str
) -> tuple[dict, Path]:
    target_root = Path(backup_root) / target_id
    if not target_root.is_dir() or target_root.is_symlink():
        raise ValueError("target backup root is invalid")
    metadata = target_root.stat(follow_symlinks=False)
    if stat.S_IMODE(metadata.st_mode) != 0o700:
        raise ValueError("target backup root must use mode 0700")
    manifest_path = target_root / "manifest.json"
    manifest_metadata = _regular_file(manifest_path, "backup manifest")
    if manifest_path.is_symlink() or stat.S_IMODE(manifest_metadata.st_mode) != 0o600:
        raise ValueError("backup manifest must use mode 0600")
    if _sha256(manifest_path) != receipt["backup_manifest_sha256"]:
        raise ValueError("backup manifest SHA-256 drift")
    manifest = _load_json(manifest_path)
    if not isinstance(manifest, dict) or set(manifest) != {
        "schema_version", "target", "plan_sha256", "transaction_id", "entries"
    }:
        raise ValueError("backup manifest fields are invalid")
    if (
        manifest["schema_version"] != 1
        or manifest["target"] != target_id
        or manifest["plan_sha256"] != plan_sha256
        or manifest["transaction_id"] != receipt["transaction_id"]
        or not isinstance(manifest["entries"], list)
        or not manifest["entries"]
    ):
        raise ValueError("backup manifest binding is invalid")
    if _closure_digest(manifest["entries"], "pre_state") != receipt[
        "destination_preimage_sha256"
    ]:
        raise ValueError("backup preimage binding is invalid")
    if _closure_digest(manifest["entries"], "candidate") != receipt["candidate_sha256"]:
        raise ValueError("backup candidate binding is invalid")
    expected_entry_fields = {
        "path", "label", "pre_state", "candidate_sha256", "candidate_mode",
        "created_parents", "backup_object", "backup_sha256",
    }
    for entry in manifest["entries"]:
        if not isinstance(entry, dict) or set(entry) != expected_entry_fields:
            raise ValueError("backup manifest entry fields are invalid")
        _validate_prestate_shape(entry["pre_state"], entry["label"])
        if not re.fullmatch(r"[0-9a-f]{64}", entry["candidate_sha256"]):
            raise ValueError("backup candidate SHA-256 is invalid")
        if type(entry["candidate_mode"]) is not int:
            raise ValueError("backup candidate mode is invalid")
        if not isinstance(entry["created_parents"], list) or not all(
            _nonblank(item) for item in entry["created_parents"]
        ):
            raise ValueError("backup created-parent list is invalid")
        if entry["pre_state"]["kind"] == "absent":
            if entry["backup_object"] is not None or entry["backup_sha256"] is not None:
                raise ValueError("absent preimage must not have a backup object")
            continue
        if not _nonblank(entry["backup_object"]) or not re.fullmatch(
            r"[0-9a-f]{64}", entry["backup_sha256"] or ""
        ):
            raise ValueError("backup object binding is invalid")
        object_path = validate_relative_path(target_root, entry["backup_object"])
        object_metadata = _regular_file(object_path, "backup object")
        if stat.S_IMODE(object_metadata.st_mode) != 0o600:
            raise ValueError("backup object must use mode 0600")
        if _sha256(object_path) != entry["backup_sha256"]:
            raise ValueError("backup object SHA-256 drift")
    return manifest, target_root


def _candidate_state(entry: dict) -> dict:
    return {
        "kind": "file",
        "sha256": entry["candidate_sha256"],
        "mode": entry["candidate_mode"],
    }


def _atomic_remove_if_matches(path: Path, expected_state: dict, label: str) -> None:
    """Move the boundary object aside, validate it, then remove only that object."""
    target = Path(path)
    expected = _validate_prestate_shape(expected_state, label)
    if expected["kind"] != "file":
        raise ValueError(f"removal pre-state must be a file: {label}")
    with _verified_parent(target, label) as parent_guard:
        if _capture_guarded_prestate(parent_guard, target.name, label) != expected:
            raise ValueError(f"destination mutation-boundary drift: {label}")
        quarantine_name = f".cross-cli-remove.{uuid.uuid4().hex}"
        quarantine = parent_guard["path"] / quarantine_name
        try:
            _assert_parent_guard(parent_guard, label)
            try:
                _renameatx(
                    target.name,
                    quarantine_name,
                    RENAME_EXCL,
                    source_dir_fd=parent_guard["fd"],
                    destination_dir_fd=parent_guard["fd"],
                )
            except OSError as exc:
                raise ValueError(
                    f"destination mutation-boundary drift: {label}"
                ) from exc
            try:
                os.fsync(parent_guard["fd"])
                _assert_parent_guard(parent_guard, label)
                displaced = _capture_guarded_prestate(
                    parent_guard, quarantine_name, label
                )
                if displaced != expected:
                    raise ValueError(f"destination mutation-boundary drift: {label}")
                _assert_parent_guard(parent_guard, label)
                _guarded_unlink(parent_guard, quarantine_name)
                os.fsync(parent_guard["fd"])
            except BaseException:
                if _guarded_entry_exists(parent_guard, quarantine_name):
                    try:
                        _renameatx(
                            quarantine_name,
                            target.name,
                            RENAME_EXCL,
                            source_dir_fd=parent_guard["fd"],
                            destination_dir_fd=parent_guard["fd"],
                        )
                        os.fsync(parent_guard["fd"])
                    except BaseException as exc:
                        raise ValueError(
                            f"destination mutation-boundary drift rollback is blocked: "
                            f"{label}; preserved path: {quarantine}"
                        ) from exc
                raise
        except BaseException:
            raise


def _planned_created_parent_paths(manifest: dict) -> list[str]:
    planned: list[str] = []
    seen: set[str] = set()
    for entry in manifest["entries"]:
        entry_paths = [
            os.fspath(Path(os.path.abspath(raw_parent)))
            for raw_parent in entry["created_parents"]
        ]
        if entry_paths:
            expected_parent = os.fspath(
                Path(os.path.abspath(entry["path"])).parent
            )
            if entry_paths[-1] != expected_parent:
                raise ValueError("backup created-parent hierarchy is invalid")
            for parent, child in zip(entry_paths, entry_paths[1:]):
                if Path(child).parent != Path(parent):
                    raise ValueError("backup created-parent hierarchy is invalid")
        for raw_path in entry_paths:
            if raw_path not in seen:
                seen.add(raw_path)
                planned.append(raw_path)
    return planned


def _bound_created_parent_records(receipt: dict, manifest: dict) -> list[dict]:
    records = _validate_created_parent_records(
        list(receipt.get("created_parent_records", []))
    )
    planned = _planned_created_parent_paths(manifest)
    recorded = [record["logical_path"] for record in records]
    if receipt["state"] == "prepared":
        expected = []
    elif receipt["state"] == "mutation-intent":
        expected = planned[: len(recorded)]
    else:
        expected = planned
    if recorded != expected:
        raise ValueError("created-parent evidence does not match the reviewed plan")
    final_identities: set[tuple[int, int, int, int, int]] = set()
    for record in records:
        logical_path = Path(record["logical_path"])
        try:
            logical_metadata = logical_path.stat(follow_symlinks=False)
            resolved_path = logical_path.resolve(strict=True)
        except OSError as exc:
            raise ValueError("created-parent logical binding is invalid") from exc
        if not stat.S_ISDIR(logical_metadata.st_mode):
            raise ValueError("created-parent logical binding is invalid")
        chain = _validated_directory_chain(record["chain"], "created parent")
        if (
            os.fspath(resolved_path) != record["path"]
            or chain != _capture_directory_chain(resolved_path, "created parent")
            or chain[-1][1] in final_identities
        ):
            raise ValueError("created-parent logical binding is invalid")
        final_identities.add(chain[-1][1])
    for raw_path in planned[len(recorded) :]:
        path = Path(raw_path)
        try:
            path.stat(follow_symlinks=False)
        except FileNotFoundError:
            continue
        except OSError as exc:
            raise ValueError("unbound created-parent state") from exc
        raise ValueError("unbound created-parent state")
    return records


def _remove_created_directory(record: dict, label: str) -> None:
    _validate_created_parent_records([record])
    chain = _validated_directory_chain(record["chain"], label)
    parent_chain = _directory_chain_value(chain[:-1])
    name = Path(record["path"]).name
    expected_identity = chain[-1][1]
    quarantine_name = f".cross-cli-parent-remove.{uuid.uuid4().hex}"
    with _recorded_directory_guard(parent_chain, label) as parent_guard:
        try:
            metadata = os.stat(name, dir_fd=parent_guard["fd"], follow_symlinks=False)
        except OSError as exc:
            raise ValueError(f"{label} identity drift") from exc
        if not stat.S_ISDIR(metadata.st_mode) or _directory_identity(
            metadata
        ) != expected_identity:
            raise ValueError(f"{label} identity drift")
        moved = False
        try:
            _assert_parent_guard(parent_guard, label)
            _renameatx(
                name,
                quarantine_name,
                RENAME_EXCL,
                source_dir_fd=parent_guard["fd"],
                destination_dir_fd=parent_guard["fd"],
            )
            moved = True
            os.fsync(parent_guard["fd"])
            _assert_parent_guard(parent_guard, label)
            quarantined = os.stat(
                quarantine_name,
                dir_fd=parent_guard["fd"],
                follow_symlinks=False,
            )
            if not stat.S_ISDIR(quarantined.st_mode) or _directory_identity(
                quarantined
            ) != expected_identity:
                raise ValueError(f"{label} identity drift")
            os.rmdir(quarantine_name, dir_fd=parent_guard["fd"])
            moved = False
            os.fsync(parent_guard["fd"])
            _assert_parent_guard(parent_guard, label)
        except BaseException:
            if moved:
                try:
                    _renameatx(
                        quarantine_name,
                        name,
                        RENAME_EXCL,
                        source_dir_fd=parent_guard["fd"],
                        destination_dir_fd=parent_guard["fd"],
                    )
                    os.fsync(parent_guard["fd"])
                except BaseException as exc:
                    raise ValueError(
                        f"{label} rollback is blocked; preserved path: "
                        f"{parent_guard['path'] / quarantine_name}"
                    ) from exc
            raise


def _assert_created_parent_roots_absent(records: list[dict]) -> None:
    logical_paths = {record["logical_path"] for record in records}
    for record in records:
        if os.fspath(Path(record["logical_path"]).parent) in logical_paths:
            continue
        chain = _validated_directory_chain(record["chain"], "created parent")
        with _recorded_directory_guard(
            _directory_chain_value(chain[:-1]), "created parent"
        ) as parent_guard:
            if _guarded_entry_exists(parent_guard, Path(record["path"]).name):
                raise ValueError("created-parent cleanup is incomplete")
            _assert_parent_guard(parent_guard, "created parent")


def _admissible_restore_state(entry: dict) -> str:
    try:
        actual = capture_destination_prestate(Path(entry["path"]))
    except ValueError:
        return "unknown"
    if actual == entry["pre_state"]:
        return "preimage"
    if actual == _candidate_state(entry):
        return "candidate"
    return "unknown"


def _mark_recovery_blocked(receipt_path: Path, reason: str) -> None:
    try:
        receipt, _ = _read_receipt(receipt_path)
        if receipt["state"] in RECEIPT_PENDING_STATES:
            _advance_receipt(
                receipt_path,
                "recovery-blocked",
                recovery_reason=reason,
            )
    except Exception:
        pass


def _restore_target_locked(
    plan: dict,
    target_id: str,
    plan_sha256: str,
    backup_root: Path,
    receipt_path: Path,
) -> dict:
    _assert_no_transaction_blockers(receipt_path.parent)
    receipt, _ = _read_receipt(receipt_path)
    if (
        receipt["target"] != target_id
        or receipt["plan_sha256"] != plan_sha256
        or receipt["state"] not in RECEIPT_PENDING_STATES
    ):
        raise ValueError("receipt is not eligible for target-local restore")
    try:
        manifest, target_backup_root = _load_verified_backup_manifest(
            receipt, backup_root, target_id, plan_sha256
        )
        created_parent_records = _bound_created_parent_records(receipt, manifest)
        forms = [_admissible_restore_state(entry) for entry in manifest["entries"]]
        if receipt["state"] == "prepared":
            if any(form != "preimage" for form in forms):
                raise ValueError("prepared receipt destination drift")
        elif "unknown" in forms:
            raise ValueError("target closure is ambiguous")

        if receipt["state"] != "prepared":
            for entry, form in reversed(list(zip(manifest["entries"], forms))):
                path = Path(entry["path"])
                pre_state = entry["pre_state"]
                if pre_state["kind"] == "absent":
                    if form == "candidate":
                        _atomic_remove_if_matches(
                            path, _candidate_state(entry), entry["label"]
                        )
                    continue
                if form == "preimage":
                    continue
                object_path = validate_relative_path(
                    target_backup_root, entry["backup_object"]
                )
                atomic_replace(
                    path,
                    object_path.read_bytes(),
                    mode=pre_state["mode"],
                    expected_state=_candidate_state(entry),
                    label=entry["label"],
                )
            for record in sorted(
                created_parent_records,
                key=lambda item: len(Path(item["logical_path"]).parts),
                reverse=True,
            ):
                _remove_created_directory(record, "target restore created parent")
            _assert_created_parent_roots_absent(created_parent_records)
        for entry in manifest["entries"]:
            assert_destination_prestate(
                Path(entry["path"]), entry["pre_state"], entry["label"]
            )
        _advance_receipt(receipt_path, "restored")
        return {
            "restore": "pass",
            "target": target_id,
            "restored": True,
            "later_targets_started": False,
        }
    except Exception as exc:
        _mark_recovery_blocked(receipt_path, "target-local recovery could not be proven")
        raise ValueError("target-local recovery is blocked") from exc


def _manual_disposition(
    transaction_root: Path,
    target_id: str,
    plan_sha256: str,
    receipt_path: Path | None,
    category: str,
) -> Path:
    root = _ensure_private_directory(transaction_root)
    output = root / f"{target_id}.manual-disposition.json"
    if output.exists() or output.is_symlink():
        return output
    receipt_sha = None
    if receipt_path is not None and receipt_path.exists() and not receipt_path.is_symlink():
        try:
            receipt_sha = _sha256(receipt_path)
        except OSError:
            receipt_sha = None
    value = {
        "schema_version": 1,
        "target": target_id,
        "plan_sha256": plan_sha256,
        "receipt_sha256": receipt_sha,
        "category": category,
        "required_action": "control-plane manual disposition",
    }
    _write_exclusive_fsynced(output, _canonical_json_bytes(value), mode=0o600)
    _fsync_directory(root)
    return output


def restore_target(
    plan: dict,
    target_id: str,
    backup_root: Path,
    transaction_receipt: Path,
    *,
    plan_sha256: str,
) -> dict:
    receipt_path = Path(transaction_receipt)
    transaction_root = receipt_path.parent
    _assert_runtime_private_roots(
        plan,
        backup_root=backup_root,
        transaction_root=transaction_root,
    )
    with _target_transaction_lock(transaction_root, target_id, plan):
        try:
            return _restore_target_locked(
                plan, target_id, plan_sha256, Path(backup_root), receipt_path
            )
        except Exception:
            if not receipt_path.exists() or receipt_path.is_symlink():
                _manual_disposition(
                    transaction_root,
                    target_id,
                    plan_sha256,
                    receipt_path,
                    "untrusted-or-missing-receipt",
                )
            raise


def cleanup_success_artifacts(backup_paths, temporary_paths):
    """Remove successful-run backup and temporary regular files."""
    for path in [*backup_paths, *temporary_paths]:
        candidate = Path(path)
        if not candidate.exists():
            continue
        _regular_file(candidate, "cleanup artifact")
        candidate.unlink()
    return True


def validate_grok_discovery(inspect_output, expected_skills, expected_root):
    """Validate ``grok inspect --json`` skill names and canonical paths."""
    try:
        payload = json.loads(inspect_output)
    except (TypeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid grok inspect JSON") from exc
    skills = payload.get("skills")
    if not isinstance(skills, list):
        raise ValueError("grok inspect JSON has no skills list")
    expected_root_text = os.path.normpath(os.fspath(expected_root))
    found: dict[str, str] = {}
    for skill in skills:
        if not isinstance(skill, dict) or not isinstance(skill.get("source"), dict):
            continue
        if skill["source"].get("type") != "user":
            continue
        found[skill.get("name")] = os.path.normpath(str(skill["source"].get("path", "")))
    for name in expected_skills:
        expected = os.path.join(expected_root_text, name, "SKILL.md")
        if found.get(name) != expected:
            raise ValueError(f"grok discovery missing expected skill path: {name}")
    return True


def validate_antigravity_discovery(runtime_root, expected_skills, file_records):
    """Validate Antigravity root and deterministic portable-file closure."""
    root = Path(runtime_root)
    if not root.exists() or not root.is_dir() or root.is_symlink():
        raise ValueError(f"invalid antigravity runtime root: {root}")
    if set(file_records) != set(expected_skills):
        raise ValueError("antigravity discovery records do not match expected skills")
    for name in expected_skills:
        if not _nonblank(name) or "/" in name or "\\" in name:
            raise ValueError("invalid skill name")
        skill_root = root / name
        if not skill_root.is_dir() or skill_root.is_symlink():
            raise ValueError(f"missing antigravity skill directory: {name}")
        for record in file_records[name]:
            if not isinstance(record, dict) or "path" not in record:
                raise ValueError(f"invalid discovery record for skill: {name}")
            path = validate_relative_path(skill_root, record["path"])
            digest = record.get("sha256")
            if digest is not None and _sha256(path) != digest:
                raise ValueError(f"antigravity portable drift: {name}/{record['path']}")
    return True


def validate_deterministic_discovery(runtime_root, expected_skills, file_records):
    """Validate deterministic portable closure for non-Grok runtimes."""
    return validate_antigravity_discovery(runtime_root, expected_skills, file_records)


def _current_target_digest(plan: dict, target_id: str) -> str:
    records = [
        {
            "path": item["destination"],
            "state": capture_destination_prestate(Path(item["destination"])),
        }
        for item in _target_verification_items(plan, target_id)
    ]
    rule, _ = _target_rule_binding(plan, target_id)
    records.append(
        {
            "path": rule["destination"],
            "state": capture_destination_prestate(Path(rule["destination"])),
        }
    )
    return _value_sha256(records)


def verify_target_with_receipt(
    plan: dict,
    target_id: str,
    transaction_receipt: Path,
    *,
    plan_sha256: str,
) -> dict:
    receipt_path = Path(transaction_receipt)
    with _target_transaction_lock(receipt_path.parent, target_id, plan):
        _assert_no_transaction_blockers(receipt_path.parent)
        receipt, _ = _read_receipt(receipt_path)
        if (
            receipt["target"] != target_id
            or receipt["plan_sha256"] != plan_sha256
            or receipt["state"] != "applied-uncommitted"
            or "content_verification_sha256" in receipt
        ):
            raise ValueError("content verification receipt state is invalid")
        verify_target(plan, target_id)
        digest = _current_target_digest(plan, target_id)
        _advance_receipt(
            receipt_path,
            "applied-uncommitted",
            content_verification_sha256=digest,
        )
    return {"verify": "pass", "target": target_id}


def verify_discovery_with_receipt(
    plan: dict,
    target_id: str,
    transaction_receipt: Path,
    *,
    plan_sha256: str,
    inspect_json: Path | None = None,
    consume: bool = False,
) -> dict:
    receipt_path = Path(transaction_receipt)
    with _target_transaction_lock(receipt_path.parent, target_id, plan):
        _assert_no_transaction_blockers(receipt_path.parent)
        receipt, _ = _read_receipt(receipt_path)
        if (
            receipt["target"] != target_id
            or receipt["plan_sha256"] != plan_sha256
            or receipt["state"] != "applied-uncommitted"
            or "content_verification_sha256" not in receipt
            or "discovery_verification_sha256" in receipt
        ):
            raise ValueError("discovery verification receipt state is invalid")
        records = _target_records(plan, target_id)
        evidence = {
            "target": target_id,
            "skills": sorted(records),
            "content_sha256": receipt["content_verification_sha256"],
        }
        if target_id == "grok-cli":
            if inspect_json is None:
                raise ValueError("Grok discovery requires --inspect-json")
            inspect_path = _absolute_without_symlink_resolution(inspect_json)
            metadata = _regular_file(inspect_path, "Grok inspect artifact")
            if inspect_path.is_symlink() or stat.S_IMODE(metadata.st_mode) != 0o600:
                raise ValueError("Grok inspect artifact must use mode 0600")
            validate_grok_discovery(
                inspect_path.read_text(encoding="utf-8"),
                sorted(records),
                plan["targets"][target_id]["skills_root"],
            )
            evidence["inspect_sha256"] = _sha256(inspect_path)
        else:
            if inspect_json is not None or consume:
                raise ValueError("inspect JSON is forbidden for deterministic targets")
            validate_deterministic_discovery(
                plan["targets"][target_id]["skills_root"],
                sorted(records),
                records,
            )
        digest = _value_sha256(evidence)
        _advance_receipt(
            receipt_path,
            "applied-uncommitted",
            discovery_verification_sha256=digest,
        )
        if target_id == "grok-cli" and consume:
            Path(inspect_json).unlink()
            _fsync_directory(Path(inspect_json).parent)
    return {"discovery": "pass", "target": target_id, "consumed": consume}


def commit_target(
    plan: dict,
    target_id: str,
    transaction_receipt: Path,
    *,
    plan_sha256: str,
) -> dict:
    receipt_path = Path(transaction_receipt)
    with _target_transaction_lock(receipt_path.parent, target_id, plan):
        _assert_no_transaction_blockers(receipt_path.parent)
        receipt, _ = _read_receipt(receipt_path)
        if (
            receipt["target"] != target_id
            or receipt["plan_sha256"] != plan_sha256
            or receipt["state"] != "applied-uncommitted"
            or "content_verification_sha256" not in receipt
            or "discovery_verification_sha256" not in receipt
        ):
            raise ValueError("target cannot commit without both verification digests")
        verify_target(plan, target_id)
        if _current_target_digest(plan, target_id) != receipt[
            "content_verification_sha256"
        ]:
            raise ValueError("target content changed after verification")
        _advance_receipt(receipt_path, "verified")
    return {"commit": "pass", "target": target_id}


def recover_pending(
    plan: dict,
    backup_root: Path,
    transaction_root: Path,
    *,
    plan_sha256: str,
) -> dict:
    _assert_runtime_private_roots(
        plan,
        backup_root=backup_root,
        transaction_root=transaction_root,
    )
    root = _ensure_private_directory(transaction_root)
    if list(root.glob("*.manual-disposition.json")):
        raise ValueError("manual disposition blocks transaction recovery")
    orphaned_temporaries = _orphaned_receipt_temporaries(root)
    if orphaned_temporaries:
        observed = orphaned_temporaries[0]
        match = re.fullmatch(
            r"\.((?:codex|pi|antigravity-cli|grok-cli))\.json\.tmp-.+",
            observed.name,
        )
        target_id = match.group(1) if len(orphaned_temporaries) == 1 and match else "unresolved"
        _manual_disposition(
            root,
            target_id,
            plan_sha256,
            observed if len(orphaned_temporaries) == 1 else None,
            "orphaned-receipt-temporary",
        )
        raise ValueError("orphaned receipt temporary blocks transaction recovery")
    for target_id in TARGET_ORDER:
        receipt_path = _receipt_path_for(root, target_id)
        backup_target = Path(backup_root) / target_id
        if not receipt_path.exists():
            if backup_target.exists() or backup_target.is_symlink():
                _manual_disposition(
                    root,
                    target_id,
                    plan_sha256,
                    None,
                    "orphaned-backup-before-prepared",
                )
                raise ValueError("orphaned backup requires manual disposition")
            continue
        try:
            receipt, _ = _read_receipt(receipt_path)
        except Exception as exc:
            _manual_disposition(
                root,
                target_id,
                plan_sha256,
                receipt_path,
                "untrusted-receipt",
            )
            raise ValueError("untrusted receipt requires manual disposition") from exc
        if receipt["plan_sha256"] != plan_sha256:
            raise ValueError("stale receipt plan binding")
        if receipt["state"] in RECEIPT_PENDING_STATES:
            restored = restore_target(
                plan,
                target_id,
                backup_root,
                receipt_path,
                plan_sha256=plan_sha256,
            )
            return {
                "recovery": restored["restore"],
                "target": target_id,
                "restored": restored["restored"],
                "later_targets_started": False,
            }
        if receipt["state"] == "recovery-blocked":
            raise ValueError("recovery-blocked receipt requires manual disposition")
    raise ValueError("transaction root is not reusable; a fresh reviewed root is required")


def verify_all_receipts(
    plan: dict,
    transaction_root: Path,
    *,
    plan_sha256: str,
) -> dict:
    _assert_runtime_private_roots(plan, transaction_root=transaction_root)
    root = _ensure_private_directory(transaction_root)
    if list(root.glob("*.manual-disposition.json")) or _orphaned_receipt_temporaries(root):
        raise ValueError("transaction evidence contains blocked or orphaned state")
    for target_id in TARGET_ORDER:
        receipt, _ = _read_receipt(_receipt_path_for(root, target_id))
        if (
            receipt["target"] != target_id
            or receipt["plan_sha256"] != plan_sha256
            or receipt["state"] != "verified"
            or "content_verification_sha256" not in receipt
            or "discovery_verification_sha256" not in receipt
        ):
            raise ValueError(f"target receipt is not verified: {target_id}")
        verify_target(plan, target_id)
        if _current_target_digest(plan, target_id) != receipt[
            "content_verification_sha256"
        ]:
            raise ValueError(f"verified target content drift: {target_id}")
    return {"verify_all": "pass", "targets": list(TARGET_ORDER)}


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def inventory_source_tree(root: Path) -> dict:
    """Inventory a complete source tree without following symlinks or reading .git."""
    source_root = Path(root)
    metadata = source_root.lstat()
    if not stat.S_ISDIR(metadata.st_mode) or source_root.is_symlink():
        raise ValueError("source inventory root must be a regular directory")
    resolved_root = source_root.resolve(strict=True)
    records: list[dict] = []

    def visit(directory: Path, prefix: Path) -> None:
        try:
            entries = sorted(os.scandir(directory), key=lambda item: item.name)
        except OSError as exc:
            raise ValueError("source inventory entry is unreadable") from exc
        for entry in entries:
            if prefix == Path() and entry.name == ".git":
                continue
            relative = prefix / entry.name
            path = Path(entry.path)
            current = path.lstat()
            mode = format(stat.S_IMODE(current.st_mode), "04o")
            if stat.S_ISREG(current.st_mode):
                kind = "file"
                digest = _sha256(path)
            elif stat.S_ISDIR(current.st_mode):
                kind = "directory"
                digest = None
            elif stat.S_ISLNK(current.st_mode):
                kind = "symlink"
                target = os.readlink(path).encode("utf-8", "surrogateescape")
                digest = hashlib.sha256(target).hexdigest()
            else:
                kind = "other"
                digest = None
            records.append(
                {
                    "path": relative.as_posix(),
                    "kind": kind,
                    "mode": mode,
                    "size": current.st_size,
                    "sha256": digest,
                }
            )
            if kind == "directory":
                visit(path, relative)

    visit(resolved_root, Path())
    return {"schema_version": 1, "root": str(resolved_root), "records": records}


def _validate_source_inventory(value: object, expected_root: Path | None = None) -> dict:
    if not isinstance(value, dict) or set(value) != {"schema_version", "root", "records"}:
        raise ValueError("source inventory fields are invalid")
    if value["schema_version"] != 1 or not isinstance(value["records"], list):
        raise ValueError("source inventory schema is invalid")
    if expected_root is not None and value["root"] != str(Path(expected_root).resolve(strict=True)):
        raise ValueError("source inventory root binding is invalid")
    seen: set[str] = set()
    for record in value["records"]:
        if not isinstance(record, dict) or set(record) != {
            "path", "kind", "mode", "size", "sha256"
        }:
            raise ValueError("source inventory record fields are invalid")
        path = record["path"]
        if not _nonblank(path) or path in seen:
            raise ValueError("source inventory path is invalid or duplicated")
        pure = PurePosixPath(path)
        if pure.is_absolute() or ".." in pure.parts or "\\" in path or path == ".git" or path.startswith(".git/"):
            raise ValueError("source inventory path is unsafe")
        seen.add(path)
        if record["kind"] not in {"file", "directory", "symlink", "other"}:
            raise ValueError("source inventory kind is invalid")
        if not isinstance(record["mode"], str) or not re.fullmatch(r"[0-7]{4}", record["mode"]):
            raise ValueError("source inventory mode is invalid")
        if type(record["size"]) is not int or record["size"] < 0:
            raise ValueError("source inventory size is invalid")
        if record["kind"] in {"file", "symlink"}:
            if not isinstance(record["sha256"], str) or not re.fullmatch(
                r"[0-9a-f]{64}", record["sha256"]
            ):
                raise ValueError("source inventory SHA-256 is invalid")
        elif record["sha256"] is not None:
            raise ValueError("non-file source inventory SHA-256 must be null")
    return value


def _validate_preflight_source_inventory(
    value: object,
    expected_root: Path,
    expected_excluded_paths: object,
) -> dict:
    """Validate the preflight-only exclusion list without loosening source-start inventories."""
    if not isinstance(value, dict) or set(value) != {
        "schema_version", "root", "records", "excluded_paths"
    }:
        raise ValueError("preflight source inventory fields are invalid")
    excluded_paths = value["excluded_paths"]
    if (
        not isinstance(excluded_paths, list)
        or excluded_paths != expected_excluded_paths
        or len(excluded_paths) != len(set(excluded_paths))
    ):
        raise ValueError("preflight source inventory exclusions are invalid")
    for path in excluded_paths:
        if not isinstance(path, str) or not _nonblank(path):
            raise ValueError("preflight source inventory exclusion is invalid")
        pure = PurePosixPath(path)
        if pure.is_absolute() or ".." in pure.parts or "\\" in path:
            raise ValueError("preflight source inventory exclusion is unsafe")
    inventory = _validate_source_inventory(
        {
            "schema_version": value["schema_version"],
            "root": value["root"],
            "records": value["records"],
        },
        expected_root,
    )
    recorded_paths = {record["path"] for record in inventory["records"]}
    if recorded_paths.intersection(excluded_paths):
        raise ValueError("preflight source inventory exclusion was also recorded")
    return inventory


def compare_source_inventory(
    baseline: dict,
    current: dict,
    repository: str,
    allowlist: set[str],
) -> tuple[list[dict], list[str]]:
    """Return complete changed records and every path outside the exact allowlist."""
    if repository not in {"router", "companion"}:
        raise ValueError("source repository identity is invalid")
    before = _validate_source_inventory(baseline)
    after = _validate_source_inventory(current)
    before_records = {record["path"]: record for record in before["records"]}
    after_records = {record["path"]: record for record in after["records"]}
    changes: list[dict] = []
    unexpected: list[str] = []
    for path in sorted(set(before_records) | set(after_records)):
        old = before_records.get(path)
        new = after_records.get(path)
        if old == new:
            continue
        if (
            old is not None
            and new is not None
            and old["kind"] == new["kind"] == "directory"
            and {key: value for key, value in old.items() if key != "size"}
            == {key: value for key, value in new.items() if key != "size"}
        ):
            continue
        status_value = "added" if old is None else "deleted" if new is None else "modified"
        changes.append(
            {
                "repository": repository,
                "path": path,
                "status": status_value,
                "before_sha256": old["sha256"] if old else None,
                "after_sha256": new["sha256"] if new else None,
                "before_mode": old["mode"] if old else None,
                "after_mode": new["mode"] if new else None,
            }
        )
        identity = f"{repository}\t{path}"
        if identity not in allowlist:
            unexpected.append(identity)
    return changes, unexpected


def prepare_source_compare_root(path: Path) -> Path:
    """Create one new mode-0700 compare directory without resolving its leaf."""
    target = Path(path).expanduser().absolute()
    if target.exists() or target.is_symlink():
        raise ValueError("source compare root must be new and absent")
    parent = target.parent.resolve(strict=True)
    if not parent.is_dir() or parent.is_symlink():
        raise ValueError("source compare parent must be a regular directory")
    target.mkdir(mode=0o700)
    _fsync_directory(parent)
    if stat.S_IMODE(target.stat().st_mode) != 0o700:
        raise ValueError("source compare root must use mode 0700")
    return target


def _safe_archive_members(archive: tarfile.TarFile, expected_entries: int) -> list[tarfile.TarInfo]:
    members = archive.getmembers()
    if len(members) != expected_entries:
        raise ValueError("source backup member count mismatch")
    seen: set[str] = set()
    for member in members:
        name = member.name
        pure = PurePosixPath(name)
        if (
            not _nonblank(name)
            or pure.is_absolute()
            or ".." in pure.parts
            or "\\" in name
            or name in seen
            or not member.isfile()
        ):
            raise ValueError("source backup contains an unsafe member")
        seen.add(name)
    return members


def safe_extract_source_archive(
    archive_path: Path,
    destination: Path,
    expected_sha256: str,
    expected_entries: int,
) -> list[dict]:
    """Validate then exclusively extract regular backup members; never use extractall."""
    source = Path(archive_path)
    metadata = _regular_file(source, "source backup archive")
    if source.is_symlink() or stat.S_IMODE(metadata.st_mode) != 0o600:
        raise ValueError("source backup archive must be a mode-0600 regular file")
    if _sha256(source) != expected_sha256:
        raise ValueError("source backup archive SHA-256 mismatch")
    with tarfile.open(source, "r:*") as archive:
        members = _safe_archive_members(archive, expected_entries)
        target_root = prepare_source_compare_root(destination)
        extracted: list[dict] = []
        for member in members:
            relative = PurePosixPath(member.name)
            parent = target_root.joinpath(*relative.parts[:-1])
            parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            if parent.is_symlink():
                raise ValueError("source backup extraction parent is unsafe")
            output = parent / relative.name
            stream = archive.extractfile(member)
            if stream is None:
                raise ValueError("source backup member cannot be read")
            descriptor = os.open(
                output,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
                0o600,
            )
            digest = hashlib.sha256()
            size = 0
            with os.fdopen(descriptor, "wb") as handle:
                for chunk in iter(lambda: stream.read(65536), b""):
                    handle.write(chunk)
                    digest.update(chunk)
                    size += len(chunk)
                handle.flush()
                os.fsync(handle.fileno())
            if size != member.size:
                raise ValueError("source backup extracted size mismatch")
            _fsync_directory(parent)
            extracted.append(
                {"path": member.name, "sha256": digest.hexdigest(), "size": size}
            )
        _fsync_directory(target_root)
    return extracted


def _validate_bound_file(binding: dict, label: str, *, count_field: str | None = None) -> Path:
    required = {"path", "sha256", "mode"}
    if count_field is not None:
        required.add(count_field)
    if not isinstance(binding, dict) or not required.issubset(binding):
        raise ValueError(f"{label} binding is invalid")
    path = Path(binding["path"])
    metadata = _regular_file(path, label)
    if path.is_symlink() or format(stat.S_IMODE(metadata.st_mode), "04o") != binding["mode"]:
        raise ValueError(f"{label} mode/type binding mismatch")
    if _sha256(path) != binding["sha256"]:
        raise ValueError(f"{label} SHA-256 binding mismatch")
    if count_field is not None and (
        type(binding[count_field]) is not int or binding[count_field] < 0
    ):
        raise ValueError(f"{label} count binding is invalid")
    return path


def _load_source_delta_allowlist(binding: dict) -> set[str]:
    path = _validate_bound_file(
        binding, "source delta allowlist", count_field="entries"
    )
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) != binding["entries"] or len(lines) != len(set(lines)):
        raise ValueError("source delta allowlist count or uniqueness mismatch")
    allowed: set[str] = set()
    for line in lines:
        repository, separator, relative = line.partition("\t")
        pure = PurePosixPath(relative)
        if (
            repository not in {"router", "companion"}
            or not separator
            or not _nonblank(relative)
            or pure.is_absolute()
            or ".." in pure.parts
            or "\\" in relative
            or any(character in relative for character in "*?[")
        ):
            raise ValueError("source delta allowlist entry is unsafe")
        allowed.add(line)
    return allowed


def generate_source_delta(args) -> dict:
    """Validate bound backups and prove the complete no-Git source delta."""
    bindings_path = Path(args.bindings)
    bindings_metadata = _regular_file(bindings_path, "source delta bindings")
    if bindings_path.is_symlink() or stat.S_IMODE(bindings_metadata.st_mode) != 0o600:
        raise ValueError("source delta bindings must be a mode-0600 regular file")
    bindings = _load_json(bindings_path)
    if not isinstance(bindings, dict) or set(bindings) != {
        "schema_version", "change_id", "plan", "backups",
        "preflight_tree_baselines", "source_delta_allowlist",
    } or bindings["schema_version"] != 1:
        raise ValueError("source delta bindings schema is invalid")
    plan_binding = bindings["plan"]
    if not isinstance(plan_binding, dict) or set(plan_binding) != {"path", "sha256"}:
        raise ValueError("source delta Plan binding is invalid")
    plan_path = Path(plan_binding["path"])
    _regular_file(plan_path, "source delta Plan")
    if plan_path.is_symlink() or _sha256(plan_path) != plan_binding["sha256"]:
        raise ValueError("source delta Plan SHA-256 binding mismatch")

    router_root = Path(args.router_root).resolve(strict=True)
    companion_root = Path(args.companion_root).resolve(strict=True)
    if not router_root.is_dir() or router_root.is_symlink():
        raise ValueError("Router source root is invalid")
    if not companion_root.is_dir() or companion_root.is_symlink():
        raise ValueError("Companion source root is invalid")
    roots = {"router": router_root, "companion": companion_root}
    baselines = {
        "router": Path(args.router_baseline),
        "companion": Path(args.companion_baseline),
    }
    allowed = _load_source_delta_allowlist(bindings["source_delta_allowlist"])
    compare_root = prepare_source_compare_root(args.compare_root)
    all_changes: list[dict] = []
    unexpected: list[str] = []

    for repository in ("router", "companion"):
        preflight_binding = bindings["preflight_tree_baselines"][repository]
        if not isinstance(preflight_binding, dict) or set(preflight_binding) != {
            "path", "sha256", "mode", "records", "excluded_paths"
        }:
            raise ValueError("preflight tree baseline binding is invalid")
        preflight_path = _validate_bound_file(
            preflight_binding,
            f"{repository} preflight tree baseline",
            count_field="records",
        )
        preflight_value = _validate_preflight_source_inventory(
            _load_json(preflight_path),
            roots[repository],
            preflight_binding["excluded_paths"],
        )
        if len(preflight_value["records"]) != preflight_binding["records"]:
            raise ValueError("preflight tree baseline record count mismatch")

        baseline_path = baselines[repository]
        baseline_metadata = _regular_file(
            baseline_path, f"{repository} source-start baseline"
        )
        if baseline_path.is_symlink() or stat.S_IMODE(baseline_metadata.st_mode) != 0o600:
            raise ValueError("source-start baseline must be mode 0600")
        baseline = _validate_source_inventory(
            _load_json(baseline_path), roots[repository]
        )
        current = inventory_source_tree(roots[repository])
        changes, repository_unexpected = compare_source_inventory(
            baseline, current, repository, allowed
        )
        all_changes.extend(changes)
        unexpected.extend(repository_unexpected)

        backup_binding = bindings["backups"][repository]
        backup_path = _validate_bound_file(
            backup_binding, f"{repository} source backup", count_field="entries"
        )
        extracted = safe_extract_source_archive(
            backup_path,
            compare_root / f"{repository}-backup",
            backup_binding["sha256"],
            backup_binding["entries"],
        )
        baseline_records = {record["path"]: record for record in baseline["records"]}
        for record in extracted:
            source_record = baseline_records.get(record["path"])
            if (
                source_record is None
                or source_record["kind"] != "file"
                or source_record["sha256"] != record["sha256"]
            ):
                raise ValueError("source backup bytes do not match source-start baseline")

    if unexpected:
        raise ValueError("source delta contains paths outside the exact allowlist")
    payload = {
        "source_delta": "pass",
        "changed_paths": [
            f"{change['repository']}\t{change['path']}" for change in all_changes
        ],
        "source_changes": all_changes,
        "unexpected_paths": [],
        "compare_root": str(compare_root),
    }
    output = Path(args.output).expanduser().absolute()
    if output.exists() or output.is_symlink():
        raise ValueError("source delta output must be new and absent")
    _write_exclusive_fsynced(output, _canonical_json_bytes(payload), mode=0o600)
    _fsync_directory(output.parent)
    return payload


def _absolute_without_symlink_resolution(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def _canonical_rule_destination(target_id: str, skills_root: Path) -> Path:
    try:
        parent_levels, filename = TARGET_RULE_LAYOUT[target_id]
    except KeyError as exc:
        raise ValueError(f"unknown target: {target_id}") from exc
    root = Path(skills_root)
    if not root.is_absolute() or root.name != "skills":
        raise ValueError(f"target skill root is not canonical: {target_id}")
    try:
        resolved_root = root.resolve(strict=True)
    except OSError as exc:
        raise ValueError(f"target skill root is not canonical: {target_id}") from exc
    if resolved_root != root:
        raise ValueError(f"target skill root is not canonical: {target_id}")
    runtime_root = resolved_root
    for _ in range(parent_levels):
        runtime_root = runtime_root.parent
    return runtime_root / filename


def _contained(root: Path, candidate: Path, label: str) -> Path:
    resolved_root = root.resolve(strict=True)
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes declared root: {candidate}") from exc
    return candidate


def _target_arguments(args) -> dict[str, dict[str, str]]:
    return {
        "codex": {
            "skills_root": str(args.codex_skills_root.resolve()),
            "rule_file": str(args.codex_rule_file.resolve()),
        },
        "pi": {
            "skills_root": str(args.pi_skills_root.resolve()),
            "rule_file": str(args.pi_rule_file.resolve()),
        },
        "antigravity-cli": {
            "skills_root": str(args.antigravity_skills_root.resolve()),
            "rule_file": str(args.antigravity_rule_file.resolve()),
        },
        "grok-cli": {
            "skills_root": str(args.grok_skills_root.resolve()),
            "rule_file": str(args.grok_rule_file.resolve()),
        },
    }


def _sandbox_literal(path: Path) -> str:
    return str(path).replace("\\", "\\\\").replace('"', '\\"')


def _probe_package_inventory(
    root: Path, *, forbidden_file_identity: tuple[int, int] | None = None
) -> tuple[list[dict], str]:
    package = root.resolve(strict=True)
    if not package.is_dir() or package.is_symlink():
        raise ValueError("Pi launcher package root is invalid")
    records: list[dict] = []
    for path in sorted(package.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(package).as_posix()
        metadata = path.stat(follow_symlinks=False)
        if stat.S_ISLNK(metadata.st_mode):
            target = Path(os.readlink(path))
            if target.is_absolute():
                raise ValueError("Pi launcher package symlink must be relative")
            try:
                path.resolve(strict=True).relative_to(package)
            except (OSError, ValueError) as exc:
                raise ValueError("Pi launcher package symlink escapes package") from exc
            records.append(
                {"path": relative, "kind": "symlink", "target": os.fspath(target)}
            )
        elif stat.S_ISDIR(metadata.st_mode):
            records.append({"path": relative, "kind": "directory"})
        elif stat.S_ISREG(metadata.st_mode):
            if forbidden_file_identity == (metadata.st_dev, metadata.st_ino):
                raise ValueError("Pi launcher runtime aliases package file")
            records.append(
                {
                    "path": relative,
                    "kind": "file",
                    "sha256": _sha256(path),
                    "executable": bool(metadata.st_mode & 0o111),
                }
            )
        else:
            raise ValueError("Pi launcher package contains a special file")
    return records, _value_sha256(records)


def _regular_file_binding(path: Path, label: str) -> dict:
    candidate = Path(path)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(candidate, flags)
    except OSError as exc:
        raise ValueError(f"{label} identity drift") from exc
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError(f"{label} identity drift")
        content_sha256 = _sha256_descriptor(descriptor)
        after = os.fstat(descriptor)
        before_identity = (
            before.st_dev,
            before.st_ino,
            stat.S_IMODE(before.st_mode),
            before.st_uid,
            before.st_gid,
            before.st_size,
            before.st_mtime_ns,
        )
        after_identity = (
            after.st_dev,
            after.st_ino,
            stat.S_IMODE(after.st_mode),
            after.st_uid,
            after.st_gid,
            after.st_size,
            after.st_mtime_ns,
        )
        if before_identity != after_identity:
            raise ValueError(f"{label} identity drift")
        return {
            "device": before.st_dev,
            "inode": before.st_ino,
            "mode": stat.S_IMODE(before.st_mode),
            "uid": before.st_uid,
            "gid": before.st_gid,
            "size": before.st_size,
            "mtime_ns": before.st_mtime_ns,
            "sha256": content_sha256,
        }
    finally:
        os.close(descriptor)


def _assert_regular_file_binding(path: Path, expected: dict, label: str) -> None:
    try:
        actual = _regular_file_binding(path, label)
    except (OSError, ValueError) as exc:
        raise ValueError(f"{label} identity drift") from exc
    if actual != expected:
        raise ValueError(f"{label} identity drift")


def _probe_package_root(entrypoint: Path) -> Path:
    resolved = entrypoint.resolve(strict=True)
    for candidate in (resolved.parent, *resolved.parents[1:]):
        manifest = candidate / "package.json"
        if not manifest.exists() or manifest.is_symlink():
            continue
        _regular_file(manifest, "Pi launcher package manifest")
        try:
            payload = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Pi launcher package manifest is invalid") from exc
        if not isinstance(payload, dict) or not _nonblank(payload.get("name")):
            raise ValueError("Pi launcher package manifest has no package name")
        return candidate.resolve(strict=True)
    raise ValueError("Pi launcher entrypoint is not inside a bound package")


def _materialize_probe_package_snapshot(snapshot: dict) -> str:
    required = {
        "source_root", "destination_root", "entrypoint_relative",
        "source_inventory_sha256", "runtime_path", "runtime_binding",
    }
    if not isinstance(snapshot, dict) or set(snapshot) != required:
        raise ValueError("Pi launcher snapshot contract is invalid")
    source = Path(snapshot["source_root"])
    destination = Path(snapshot["destination_root"])
    relative = snapshot["entrypoint_relative"]
    if (
        not _nonblank(relative)
        or PurePosixPath(relative).is_absolute()
        or ".." in PurePosixPath(relative).parts
        or destination.exists()
        or destination.is_symlink()
    ):
        raise ValueError("Pi launcher snapshot destination is invalid")
    _assert_regular_file_binding(
        Path(snapshot["runtime_path"]),
        snapshot["runtime_binding"],
        "Pi launcher runtime",
    )
    _, source_before = _probe_package_inventory(source)
    if source_before != snapshot["source_inventory_sha256"]:
        raise ValueError("Pi launcher package changed before snapshot")
    try:
        shutil.copytree(source, destination, symlinks=True)
    except OSError as exc:
        raise ValueError("Pi launcher package snapshot failed") from exc
    _, source_after = _probe_package_inventory(source)
    _assert_regular_file_binding(
        Path(snapshot["runtime_path"]),
        snapshot["runtime_binding"],
        "Pi launcher runtime",
    )
    snapshot_records, snapshot_digest = _probe_package_inventory(destination)
    if source_after != source_before or snapshot_digest != source_before:
        raise ValueError("Pi launcher package changed during snapshot")
    for record in snapshot_records:
        path = destination / record["path"]
        if record["kind"] == "file":
            path.chmod(0o555 if record["executable"] else 0o444)
    for record in reversed(snapshot_records):
        if record["kind"] == "directory":
            (destination / record["path"]).chmod(0o555)
    destination.chmod(0o555)
    _fsync_directory(destination.parent)
    _assert_probe_package_snapshot(snapshot)
    return snapshot_digest


def _assert_probe_package_snapshot(snapshot: dict) -> None:
    _assert_regular_file_binding(
        Path(snapshot["runtime_path"]),
        snapshot["runtime_binding"],
        "Pi launcher runtime",
    )
    destination = Path(snapshot["destination_root"])
    records, digest = _probe_package_inventory(destination)
    if digest != snapshot["source_inventory_sha256"]:
        raise ValueError("Pi launcher package snapshot drift")
    if stat.S_IMODE(destination.stat(follow_symlinks=False).st_mode) != 0o555:
        raise ValueError("Pi launcher package snapshot root is writable")
    for record in records:
        if record["kind"] == "symlink":
            continue
        path = destination / record["path"]
        mode = stat.S_IMODE(path.stat(follow_symlinks=False).st_mode)
        expected = 0o555 if record["kind"] == "directory" else (
            0o555 if record["executable"] else 0o444
        )
        if mode != expected:
            raise ValueError("Pi launcher package snapshot mode drift")


def _probe_exec_contract(executable: Path) -> dict:
    resolved = executable.resolve(strict=True)
    executables = [resolved]
    read_files = [resolved]
    read_roots: list[Path] = []
    argv_prefix = [resolved]
    package_root = None
    entrypoint_relative = None
    package_inventory_sha256 = None
    runtime_binding = None
    with resolved.open("rb") as stream:
        first_line = stream.readline(4096)
    if not first_line.startswith(b"#!"):
        return {
            "executables": executables,
            "read_files": read_files,
            "read_roots": read_roots,
            "argv_prefix": argv_prefix,
            "package_root": package_root,
            "entrypoint_relative": entrypoint_relative,
            "package_inventory_sha256": package_inventory_sha256,
            "runtime_binding": runtime_binding,
        }
    try:
        shebang = shlex.split(first_line[2:].decode("utf-8").strip())
    except (UnicodeDecodeError, ValueError) as exc:
        raise ValueError("Pi executable shebang is invalid") from exc
    if not shebang:
        raise ValueError("Pi executable shebang is empty")
    interpreter = Path(shebang[0]).resolve(strict=True)
    executables.append(interpreter)
    read_files.append(interpreter)
    if interpreter == Path("/usr/bin/env") and len(shebang) >= 2:
        resolved_command = shutil.which(
            shebang[-1], path="/usr/bin:/bin:/Users/elvis/.local/bin"
        )
        if resolved_command is None:
            raise ValueError("Pi executable interpreter is unavailable in the probe PATH")
        env_interpreter = Path(resolved_command).resolve(strict=True)
        executables.append(env_interpreter)
        read_files.append(env_interpreter)
        interpreter = env_interpreter

    if interpreter == Path("/bin/sh"):
        launcher_bytes = resolved.read_bytes()
        if len(launcher_bytes) > 16_384:
            raise ValueError("Pi shell launcher exceeds the bounded size")
        try:
            launcher_text = launcher_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Pi shell launcher is not UTF-8") from exc
        body = [line.strip() for line in launcher_text.splitlines()[1:] if line.strip()]
        if body:
            if len(body) != 1:
                raise ValueError("Pi shell launcher must contain one exec command")
            try:
                command = shlex.split(body[0], posix=True)
            except ValueError as exc:
                raise ValueError("Pi shell launcher command is invalid") from exc
            if len(command) != 4 or command[0] != "exec" or command[3] != "$@":
                raise ValueError("Pi shell launcher must forward arguments exactly")
            runtime_path = Path(command[1])
            entrypoint_path = Path(command[2])
            if not runtime_path.is_absolute() or not entrypoint_path.is_absolute():
                raise ValueError("Pi shell launcher paths must be absolute")
            if runtime_path.is_symlink() or entrypoint_path.is_symlink():
                raise ValueError("Pi shell launcher targets must not be symlinks")
            runtime_metadata = _regular_file(runtime_path, "Pi launcher runtime")
            if not (runtime_metadata.st_mode & stat.S_IXUSR):
                raise ValueError("Pi launcher runtime is not executable")
            _regular_file(entrypoint_path, "Pi launcher entrypoint")
            runtime_resolved = runtime_path.resolve(strict=True)
            runtime_binding = _regular_file_binding(
                runtime_path, "Pi launcher runtime"
            )
            entrypoint_resolved = entrypoint_path.resolve(strict=True)
            executables = [runtime_resolved]
            argv_prefix = [runtime_resolved, entrypoint_resolved]
            read_files.extend(
                (runtime_path, runtime_resolved, entrypoint_path, entrypoint_resolved)
            )
            package_root = _probe_package_root(entrypoint_path)
            try:
                runtime_resolved.relative_to(package_root)
            except ValueError:
                pass
            else:
                raise ValueError("Pi launcher runtime must remain outside package")
            entrypoint_relative = entrypoint_resolved.relative_to(
                package_root
            ).as_posix()
            _, package_inventory_sha256 = _probe_package_inventory(
                package_root,
                forbidden_file_identity=(
                    runtime_metadata.st_dev,
                    runtime_metadata.st_ino,
                ),
            )
            _assert_regular_file_binding(
                runtime_path, runtime_binding, "Pi launcher runtime"
            )
            _, confirmed_package_inventory_sha256 = _probe_package_inventory(
                package_root,
                forbidden_file_identity=(
                    runtime_binding["device"],
                    runtime_binding["inode"],
                ),
            )
            _assert_regular_file_binding(
                runtime_path, runtime_binding, "Pi launcher runtime"
            )
            if confirmed_package_inventory_sha256 != package_inventory_sha256:
                raise ValueError("Pi launcher package changed during inventory")
            read_roots.append(package_root)
            homebrew_cellar = Path("/opt/homebrew/Cellar")
            try:
                runtime_resolved.relative_to(homebrew_cellar)
            except ValueError:
                pass
            else:
                read_roots.append(runtime_resolved.parents[1])
                homebrew_opt = Path("/opt/homebrew/opt")
                if homebrew_opt.is_dir() and not homebrew_opt.is_symlink():
                    read_roots.append(homebrew_opt.resolve(strict=True))

    return {
        "executables": list(dict.fromkeys(executables)),
        "read_files": list(dict.fromkeys(read_files)),
        "read_roots": list(dict.fromkeys(read_roots)),
        "argv_prefix": argv_prefix,
        "package_root": package_root,
        "entrypoint_relative": entrypoint_relative,
        "package_inventory_sha256": package_inventory_sha256,
        "runtime_binding": runtime_binding,
    }


def _probe_exec_chain(executable: Path) -> list[Path]:
    return _probe_exec_contract(executable)["executables"]


def _sandbox_ancestor_literals(paths: list[Path]) -> str:
    ancestors: set[Path] = {Path("/")}
    for path in paths:
        current = path.resolve(strict=False)
        while current != current.parent:
            ancestors.add(current.parent)
            current = current.parent
    return " ".join(
        f'(literal "{_sandbox_literal(path)}")'
        for path in sorted(ancestors, key=lambda item: str(item))
    )


def build_pi_probe(
    pi_executable: Path,
    temporary_root: Path,
    native_pi_root: Path,
    *,
    prompt: str | None = None,
) -> dict:
    """Build a pure, isolated Pi probe contract without launching Pi."""
    executable = Path(pi_executable)
    temporary = Path(temporary_root)
    native = Path(native_pi_root)
    _regular_file(executable, "Pi executable")
    if executable.is_symlink():
        raise ValueError("Pi executable must not be a symlink")
    if not temporary.is_dir() or temporary.is_symlink():
        raise ValueError("Pi temporary root must be a regular directory")
    if any(temporary.iterdir()):
        raise ValueError("Pi temporary root must be new and empty")
    if not native.is_dir() or native.is_symlink():
        raise ValueError("native Pi root must be a regular directory")
    sandbox_metadata = _regular_file(SANDBOX_EXECUTABLE, "sandbox-exec")
    if not (sandbox_metadata.st_mode & stat.S_IXUSR):
        raise ValueError("sandbox-exec is not executable")

    temporary_resolved = temporary.resolve(strict=True)
    native_resolved = native.resolve(strict=True)
    try:
        temporary_resolved.relative_to(native_resolved)
    except ValueError:
        pass
    else:
        raise ValueError("Pi temporary root overlaps native root")
    try:
        native_resolved.relative_to(temporary_resolved)
    except ValueError:
        pass
    else:
        raise ValueError("native Pi root overlaps temporary root")

    home = temporary_resolved / "home"
    agent_dir = temporary_resolved / "pi-agent"
    launch_contract = _probe_exec_contract(executable)
    launcher_snapshot = None
    argv_prefix = list(launch_contract["argv_prefix"])
    launch_read_files = list(launch_contract["read_files"])
    launch_read_roots = list(launch_contract["read_roots"])
    package_root = launch_contract["package_root"]
    if package_root is not None:
        for first, second in (
            (package_root, temporary_resolved),
            (temporary_resolved, package_root),
        ):
            try:
                first.relative_to(second)
            except ValueError:
                pass
            else:
                raise ValueError("Pi launcher package overlaps temporary root")
        snapshot_root = temporary_resolved / "launcher-package"
        snapshot_entrypoint = snapshot_root / launch_contract["entrypoint_relative"]
        launcher_snapshot = {
            "source_root": str(package_root),
            "destination_root": str(snapshot_root),
            "entrypoint_relative": launch_contract["entrypoint_relative"],
            "source_inventory_sha256": launch_contract[
                "package_inventory_sha256"
            ],
            "runtime_path": str(argv_prefix[0]),
            "runtime_binding": launch_contract["runtime_binding"],
        }
        argv_prefix = [argv_prefix[0], snapshot_entrypoint]

        def outside_package(path: Path) -> bool:
            try:
                path.resolve(strict=True).relative_to(package_root)
            except ValueError:
                return True
            return False

        launch_read_files = [
            path for path in launch_read_files if outside_package(path)
        ]
        launch_read_roots = [
            path for path in launch_read_roots if path.resolve(strict=True) != package_root
        ]
    argv = [
        *(str(path) for path in argv_prefix),
        "--no-session",
        "--no-context-files",
        "--no-skills",
        "--tools",
        "read,grep,find,ls",
    ]
    if prompt is not None:
        if not _nonblank(prompt):
            raise ValueError("Pi probe prompt must be non-blank")
        argv.extend(["-p", prompt])
    native_literal = _sandbox_literal(native_resolved)
    temporary_literal = _sandbox_literal(temporary_resolved)
    executable_chain = launch_contract["executables"]
    for dependency in [
        *launch_contract["read_files"], *launch_contract["read_roots"]
    ]:
        try:
            dependency.resolve(strict=True).relative_to(native_resolved)
        except ValueError:
            pass
        else:
            raise ValueError("Pi probe launcher dependency overlaps native root")
    executable_literal = _sandbox_literal(executable.resolve(strict=True))
    process_literals = " ".join(
        f'(literal "{_sandbox_literal(path)}")' for path in executable_chain
    )
    ancestor_literals = _sandbox_ancestor_literals(
        [
            *executable_chain,
            *launch_read_files,
            *launch_read_roots,
            temporary_resolved,
            native_resolved,
        ]
    )
    launch_file_literals = " ".join(
        f'(literal "{_sandbox_literal(path)}")' for path in launch_read_files
    )
    launch_root_rules = " ".join(
        f'(subpath "{_sandbox_literal(path)}")' for path in launch_read_roots
    )
    snapshot_write_deny = ""
    if launcher_snapshot is not None:
        snapshot_write_deny = (
            f'(deny file-write* (subpath "'
            f'{_sandbox_literal(Path(launcher_snapshot["destination_root"]))}"))'
        )
    profile = "\n".join(
        (
            "(version 1)",
            "(deny default)",
            "(allow process-info*)",
            "(allow sysctl-read)",
            "(allow mach-lookup)",
            "(allow process-fork)",
            f"(allow process-exec {process_literals})",
            "(allow file-read* (subpath \"/System\") (subpath \"/usr\") "
            "(subpath \"/bin\") (subpath \"/Library\") "
            "(subpath \"/sbin\") (subpath \"/dev\") "
            "(subpath \"/private/etc\") (subpath \"/private/var/db\") "
            f"{ancestor_literals})",
            f'(allow file-read* (literal "{executable_literal}") {launch_file_literals})',
            f"(allow file-read* {launch_root_rules})" if launch_root_rules else "",
            f'(allow file-read* (subpath "{temporary_literal}"))',
            '(allow file-write* (literal "/dev/null"))',
            f'(allow file-write* (subpath "{temporary_literal}"))',
            snapshot_write_deny,
            f'(deny file-read* (subpath "{native_literal}"))',
            f'(deny file-write* (subpath "{native_literal}"))',
            "(deny network*)",
        )
    ) + "\n"
    return {
        "argv": argv,
        "env": {
            "HOME": str(home),
            "PI_CODING_AGENT_DIR": str(agent_dir),
            "PATH": "/usr/bin:/bin:/Users/elvis/.local/bin",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
        },
        "sandbox_profile": profile,
        "allowed_output_fields": [
            "pi_probe",
            "reviewer_identity",
            "bound_input_hashes",
            "verdict",
            "findings",
        ],
        "launcher_snapshot": launcher_snapshot,
    }


def _reviewed_tree_digest(root: Path) -> str:
    reviewed = Path(root)
    try:
        reviewed_metadata = reviewed.stat(follow_symlinks=False)
    except OSError as exc:
        raise ValueError("Pi reviewed source root must be a regular directory") from exc
    if not stat.S_ISDIR(reviewed_metadata.st_mode):
        raise ValueError("Pi reviewed source root must be a regular directory")
    records = [
        {
            "path": ".",
            "kind": "directory",
            "mode": stat.S_IMODE(reviewed_metadata.st_mode),
            "device": reviewed_metadata.st_dev,
            "inode": reviewed_metadata.st_ino,
            "uid": reviewed_metadata.st_uid,
            "gid": reviewed_metadata.st_gid,
        }
    ]
    for path in sorted(reviewed.rglob("*"), key=lambda item: item.as_posix()):
        if ".git" in path.parts:
            continue
        relative = path.relative_to(reviewed).as_posix()
        metadata = path.stat(follow_symlinks=False)
        if stat.S_ISLNK(metadata.st_mode):
            raise ValueError("Pi reviewed source root must not contain symlinks")
        elif stat.S_ISDIR(metadata.st_mode):
            records.append(
                {
                    "path": relative,
                    "kind": "directory",
                    "mode": stat.S_IMODE(metadata.st_mode),
                    "device": metadata.st_dev,
                    "inode": metadata.st_ino,
                    "uid": metadata.st_uid,
                    "gid": metadata.st_gid,
                }
            )
        elif stat.S_ISREG(metadata.st_mode):
            binding = _regular_file_binding(path, "Pi reviewed source file")
            if (
                binding["device"],
                binding["inode"],
                binding["mode"],
                binding["uid"],
                binding["gid"],
                binding["size"],
                binding["mtime_ns"],
            ) != (
                metadata.st_dev,
                metadata.st_ino,
                stat.S_IMODE(metadata.st_mode),
                metadata.st_uid,
                metadata.st_gid,
                metadata.st_size,
                metadata.st_mtime_ns,
            ):
                raise ValueError("Pi reviewed source changed during digest")
            records.append(
                {
                    "path": relative,
                    "kind": "file",
                    "mode": binding["mode"],
                    "device": binding["device"],
                    "inode": binding["inode"],
                    "uid": binding["uid"],
                    "gid": binding["gid"],
                    "sha256": binding["sha256"],
                }
            )
        else:
            raise ValueError("Pi reviewed source contains a special file")
    reviewed_after = reviewed.stat(follow_symlinks=False)
    if (
        reviewed_after.st_dev,
        reviewed_after.st_ino,
        stat.S_IMODE(reviewed_after.st_mode),
        reviewed_after.st_uid,
        reviewed_after.st_gid,
    ) != (
        reviewed_metadata.st_dev,
        reviewed_metadata.st_ino,
        stat.S_IMODE(reviewed_metadata.st_mode),
        reviewed_metadata.st_uid,
        reviewed_metadata.st_gid,
    ):
        raise ValueError("Pi reviewed source changed during digest")
    return _value_sha256(records)


def _validate_pi_findings(findings) -> list[dict]:
    if not isinstance(findings, list):
        raise ValueError("Pi findings must be a list")
    required = {"severity", "category", "location", "summary", "required_action"}
    cleaned = []
    for finding in findings:
        if not isinstance(finding, dict) or set(finding) != required:
            raise ValueError("Pi finding fields are invalid")
        if not all(_nonblank(finding[field]) for field in required):
            raise ValueError("Pi finding fields must be non-blank")
        cleaned.append(dict(finding))
    return cleaned


def _blocked_pi_probe_result() -> dict:
    return {
        "pi_probe": "blocked",
        "reviewer_identity": {
            "product": "pi",
            "role": "independent-reviewer",
            "capability_profile": "control-plane-high",
        },
        "bound_input_hashes": {},
        "verdict": "BLOCKED",
        "findings": [
            {
                "severity": "P1",
                "category": "probe-isolation-or-output",
                "location": "isolated-pi-process",
                "summary": "Pi probe could not produce mechanically acceptable evidence.",
                "required_action": "Keep the gate BLOCKED; do not relax isolation.",
            }
        ],
    }


def _execute_pi_probe(args) -> tuple[dict, bool]:
    """Run the explicitly requested Pi process inside the reviewed sandbox."""
    prompt_path = Path(args.prompt_file)
    prompt_metadata = _regular_file(prompt_path, "Pi review prompt")
    if prompt_path.is_symlink() or stat.S_IMODE(prompt_metadata.st_mode) & 0o022:
        raise ValueError("Pi review prompt must not be symlinked or writable by group/other")
    prompt = prompt_path.read_text(encoding="utf-8")
    contract = build_pi_probe(
        args.pi_executable,
        args.temporary_root,
        args.native_pi_root,
        prompt=prompt,
    )
    temporary = Path(args.temporary_root).resolve(strict=True)
    native = Path(args.native_pi_root).resolve(strict=True)
    launcher_snapshot = contract["launcher_snapshot"]
    if launcher_snapshot is not None:
        _materialize_probe_package_snapshot(launcher_snapshot)
    runtime_path = Path(contract["argv"][0])
    runtime_binding = (
        launcher_snapshot["runtime_binding"]
        if launcher_snapshot is not None
        else _regular_file_binding(runtime_path, "Pi launcher runtime")
    )
    read_roots = []
    input_hashes = {"review-prompt": hashlib.sha256(prompt.encode("utf-8")).hexdigest()}
    for index, raw_root in enumerate(args.read_root, 1):
        root = _absolute_without_symlink_resolution(Path(raw_root))
        reviewed_digest = _reviewed_tree_digest(root)
        resolved_root = root.resolve(strict=True)
        try:
            resolved_root.relative_to(native)
        except ValueError:
            pass
        else:
            raise ValueError("native Pi root cannot be a reviewed read root")
        read_roots.append(root)
        input_hashes[f"reviewed-source-{index}"] = reviewed_digest

    for directory in (Path(contract["env"]["HOME"]), Path(contract["env"]["PI_CODING_AGENT_DIR"])):
        directory.mkdir(mode=0o700)
    profile = contract["sandbox_profile"]
    read_rules = "\n".join(
        (
            f'(allow file-read* {_sandbox_ancestor_literals(read_roots)})',
            *(
                f'(allow file-read* (subpath "{_sandbox_literal(root)}"))'
                for root in read_roots
            ),
        )
    )
    profile = profile.replace(
        f'(deny file-read* (subpath "{_sandbox_literal(native)}"))',
        read_rules
        + "\n"
        + f'(deny file-read* (subpath "{_sandbox_literal(native)}"))',
    )
    profile_path = temporary / "pi-probe.sb"
    _write_exclusive_fsynced(profile_path, profile.encode("utf-8"), mode=0o600)
    _fsync_directory(temporary)

    command = [str(SANDBOX_EXECUTABLE), "-f", str(profile_path), "--", *contract["argv"]]
    _assert_regular_file_binding(
        runtime_path, runtime_binding, "Pi launcher runtime"
    )
    completed = subprocess.run(
        command,
        cwd=temporary,
        env=contract["env"],
        capture_output=True,
        text=True,
        check=False,
    )
    success = False
    findings = []
    verdict = "BLOCKED"
    if completed.returncode == 0:
        try:
            payload = json.loads(completed.stdout)
            if not isinstance(payload, dict) or set(payload) != {"verdict", "findings"}:
                raise ValueError("Pi stdout schema is invalid")
            if payload["verdict"] not in {"PASS", "BLOCKED"}:
                raise ValueError("Pi verdict is invalid")
            findings = _validate_pi_findings(payload["findings"])
            verdict = payload["verdict"]
            success = True
        except (ValueError, json.JSONDecodeError):
            success = False
    try:
        _assert_regular_file_binding(
            runtime_path, runtime_binding, "Pi launcher runtime"
        )
        if launcher_snapshot is not None:
            _assert_probe_package_snapshot(launcher_snapshot)
        for index, root in enumerate(read_roots, 1):
            if _reviewed_tree_digest(root) != input_hashes[
                f"reviewed-source-{index}"
            ]:
                raise ValueError("Pi reviewed source drift")
    except (OSError, ValueError):
        success = False
    if not success:
        findings = [
            {
                "severity": "P1",
                "category": "probe-isolation-or-output",
                "location": "isolated-pi-process",
                "summary": "Pi probe could not produce mechanically acceptable evidence.",
                "required_action": "Keep the gate BLOCKED; do not relax isolation.",
            }
        ]
        verdict = "BLOCKED"
    result = {
        "pi_probe": "pass" if success else "blocked",
        "reviewer_identity": {
            "product": "pi",
            "role": "independent-reviewer",
            "capability_profile": "control-plane-high",
        },
        "bound_input_hashes": input_hashes,
        "verdict": verdict,
        "findings": findings,
    }
    serialized = _canonical_json_bytes(result)
    lowered = serialized.decode("utf-8").lower()
    forbidden = (
        str(native).lower(),
        "credential",
        "session",
        "settings",
        "environment dump",
        "raw debug trace",
    )
    if any(value and value in lowered for value in forbidden):
        result = {
            "pi_probe": "blocked",
            "reviewer_identity": {
                "product": "pi",
                "role": "independent-reviewer",
                "capability_profile": "control-plane-high",
            },
            "bound_input_hashes": input_hashes,
            "verdict": "BLOCKED",
            "findings": [
                {
                    "severity": "P1",
                    "category": "sensitive-output-rejected",
                    "location": "isolated-pi-process",
                    "summary": "Probe output matched a forbidden sensitive category.",
                    "required_action": "Keep the gate BLOCKED and inspect only sanitized evidence.",
                }
            ],
        }
        success = False
        serialized = _canonical_json_bytes(result)
    return result, success


def _persist_pi_blocked_recovery(
    parent_guard: dict,
    output_name: str,
    blocked_content: bytes,
    label: str,
) -> str:
    """Install and durably validate one mode-0600 BLOCKED recovery record."""
    try:
        blocked_name = _create_pi_blocked_recovery(
            parent_guard, output_name, blocked_content, label
        )
    except BaseException as exc:
        raise ValueError(
            f"{label} persistence-blocked evidence could not be made durable"
        ) from exc
    if not blocked_name or _guarded_entry_exists(parent_guard, output_name):
        raise ValueError(
            f"{label} persistence-blocked evidence left an official output"
        )
    return blocked_name


def _persist_pi_probe_result(args, result: dict) -> None:
    output = _absolute_without_symlink_resolution(args.output)
    _ensure_private_directory(output.parent)
    content = _canonical_json_bytes(result)
    expected = {
        "kind": "file",
        "sha256": hashlib.sha256(content).hexdigest(),
        "mode": 0o600,
    }
    blocked_content = _canonical_json_bytes(_blocked_pi_probe_result())
    label = "Pi probe evidence"
    with _verified_parent(output, label) as parent_guard:
        if _capture_guarded_prestate(parent_guard, output.name, label) != {
            "kind": "absent"
        }:
            raise ValueError("Pi probe evidence output must be new and absent")
        candidate = _write_pi_probe_candidate(
            output,
            content,
            0o600,
            parent_guard=parent_guard,
            label=label,
            blocked_content=blocked_content,
        )
        installed = False
        restored = False
        rewritten_blocked = False
        try:
            _assert_parent_guard(parent_guard, label)
            _require_retained_binding(
                parent_guard,
                candidate["name"],
                candidate,
                label,
                expected=expected,
            )
            try:
                _renameatx(
                    candidate["name"],
                    output.name,
                    RENAME_EXCL,
                    source_dir_fd=parent_guard["fd"],
                    destination_dir_fd=parent_guard["fd"],
                )
            except BaseException:
                # renameatx_np may have changed the namespace before raising.
                # Inspect both names and never leave an accepted-looking PASS
                # at the official output when that boundary is uncertain.
                if _retained_binding_matches_name(
                    parent_guard,
                    output.name,
                    candidate,
                    label,
                    expected=expected,
                    allow_rename_ctime=True,
                ):
                    try:
                        _rewrite_guarded_pi_evidence(
                            parent_guard,
                            output.name,
                            expected,
                            blocked_content,
                            label,
                            ownership=candidate,
                            allow_rename_ctime=True,
                        )
                        rewritten_blocked = True
                    except BaseException:
                        _preserve_pi_unexpected_entry(
                            parent_guard, output.name, output.name, label
                        )
                        _persist_pi_blocked_recovery(
                            parent_guard, output.name, blocked_content, label
                        )
                else:
                    if _guarded_entry_exists(parent_guard, output.name):
                        _preserve_pi_unexpected_entry(
                            parent_guard, output.name, output.name, label
                        )
                    if _guarded_entry_exists(parent_guard, candidate["name"]):
                        try:
                            _quarantine_pi_probe_candidate(
                                parent_guard,
                                candidate["name"],
                                expected,
                                output.name,
                                label,
                                ownership=candidate,
                            )
                        except BaseException:
                            _move_entry_to_visible_recovery(
                                parent_guard,
                                candidate["name"],
                                output.name,
                                "persistence-unsafe",
                                label,
                            )
                    if not _guarded_entry_exists(parent_guard, output.name):
                        _persist_pi_blocked_recovery(
                            parent_guard, output.name, blocked_content, label
                        )
                raise
            installed = True
            try:
                _require_retained_binding(
                    parent_guard,
                    output.name,
                    candidate,
                    label,
                    expected=expected,
                    allow_rename_ctime=True,
                )
                _fsync_directory(output.parent)
                _assert_parent_guard(parent_guard, label)
                _require_retained_binding(
                    parent_guard,
                    output.name,
                    candidate,
                    label,
                    expected=expected,
                    allow_rename_ctime=True,
                )
            except BaseException as exc:
                if _retained_binding_matches_name(
                    parent_guard,
                    output.name,
                    candidate,
                    label,
                    expected=expected,
                    allow_rename_ctime=True,
                ):
                    try:
                        _rewrite_guarded_pi_evidence(
                            parent_guard,
                            output.name,
                            expected,
                            blocked_content,
                            label,
                            ownership=candidate,
                            allow_rename_ctime=True,
                        )
                        rewritten_blocked = True
                    except BaseException as rollback_exc:
                        if _guarded_entry_exists(parent_guard, output.name):
                            try:
                                _preserve_pi_unexpected_entry(
                                    parent_guard, output.name, output.name, label
                                )
                            except BaseException:
                                pass
                        if not _guarded_entry_exists(parent_guard, output.name):
                            try:
                                _persist_pi_blocked_recovery(
                                    parent_guard, output.name, blocked_content, label
                                )
                            except BaseException:
                                pass
                        raise ValueError(
                            "Pi probe evidence persistence rollback is ambiguous"
                        ) from rollback_exc
                else:
                    try:
                        _restore_pi_install_after_mismatch(
                            parent_guard,
                            output.name,
                            candidate["name"],
                            label,
                            candidate_ownership=candidate,
                            expected=expected,
                        )
                        restored = True
                    except BaseException as rollback_exc:
                        if _guarded_entry_exists(parent_guard, output.name):
                            try:
                                _preserve_pi_unexpected_entry(
                                    parent_guard, output.name, output.name, label
                                )
                            except BaseException:
                                pass
                        if not _guarded_entry_exists(parent_guard, output.name):
                            try:
                                _persist_pi_blocked_recovery(
                                    parent_guard, output.name, blocked_content, label
                                )
                            except BaseException:
                                pass
                        raise ValueError(
                            "Pi probe evidence persistence rollback is ambiguous"
                        ) from rollback_exc
                raise
        except BaseException:
            if installed and not restored and not rewritten_blocked and _guarded_entry_exists(
                parent_guard, output.name
            ):
                try:
                    if not _retained_binding_matches_name(
                        parent_guard,
                        output.name,
                        candidate,
                        label,
                        expected=expected,
                        allow_rename_ctime=True,
                    ):
                        _restore_pi_install_after_mismatch(
                            parent_guard,
                            output.name,
                            candidate["name"],
                            label,
                            candidate_ownership=candidate,
                            expected=expected,
                        )
                        restored = True
                except BaseException:
                    if _guarded_entry_exists(parent_guard, output.name):
                        try:
                            _preserve_pi_unexpected_entry(
                                parent_guard, output.name, output.name, label
                            )
                        except BaseException:
                            pass
                    if not _guarded_entry_exists(parent_guard, output.name):
                        try:
                            _persist_pi_blocked_recovery(
                                parent_guard, output.name, blocked_content, label
                            )
                        except BaseException:
                            pass
            raise
        finally:
            if _guarded_entry_exists(parent_guard, candidate["name"]):
                try:
                    _quarantine_pi_probe_candidate(
                        parent_guard,
                        candidate["name"],
                        expected,
                        output.name,
                        label,
                        ownership=candidate,
                        allow_rename_ctime=restored,
                    )
                except BaseException:
                    _move_entry_to_visible_recovery(
                        parent_guard,
                        candidate["name"],
                        output.name,
                        "persistence-unsafe",
                        label,
                    )
            os.close(candidate["fd"])


def _preserve_pi_unexpected_entry(
    parent_guard: dict,
    name: str,
    output_name: str,
    label: str,
) -> str | None:
    """Move an unbound current entry out of an official Pi evidence name.

    This is used only after a namespace failure makes the expected candidate
    binding unavailable.  The current object is rebound with O_NOFOLLOW,
    moved to an explicit ``persistence-unsafe`` name, fsynced, and rebound
    again before callers are allowed to continue recovery.
    """
    if not _guarded_entry_exists(parent_guard, name):
        return None
    try:
        binding = _open_guarded_binding(parent_guard, name, label)
    except BaseException as exc:
        # A substituted symlink or special file cannot be descriptor-bound.
        # It is still safe to move by directory FD to a visible non-evidence
        # name; never follow it or unlink it in place.
        moved_name = _move_entry_to_visible_recovery(
            parent_guard, name, output_name, "persistence-unsafe", label
        )
        if moved_name is None or _guarded_entry_exists(parent_guard, name):
            raise ValueError(
                f"{label} persistence-unsafe preservation is ambiguous"
            ) from exc
        os.fsync(parent_guard["fd"])
        _assert_parent_guard(parent_guard, label)
        return moved_name
    try:
        moved_name = _preserve_pi_entry_as_unsafe(
            parent_guard, name, output_name, binding, label
        )
        if moved_name is None or _guarded_entry_exists(parent_guard, name):
            raise ValueError(f"{label} persistence-unsafe preservation is ambiguous")
        return moved_name
    finally:
        os.close(binding["fd"])


def _restore_pi_install_after_mismatch(
    parent_guard: dict,
    output_name: str,
    candidate_name: str,
    label: str,
    *,
    candidate_ownership: dict | None = None,
    expected: dict | None = None,
) -> None:
    output_matches_candidate = False
    if candidate_ownership is not None:
        output_matches_candidate = _retained_binding_matches_name(
            parent_guard,
            output_name,
            candidate_ownership,
            label,
            expected=expected,
            allow_rename_ctime=True,
        )
    if _guarded_entry_exists(parent_guard, candidate_name):
        # A collision at the candidate name means the output cannot be moved
        # back safely.  Preserve whichever object currently occupies the
        # official output as non-evidence before reporting the ambiguity.
        if _guarded_entry_exists(parent_guard, output_name):
            _preserve_pi_unexpected_entry(
                parent_guard, output_name, output_name, label
            )
        raise ValueError(f"Pi probe evidence persistence rollback is ambiguous: {label}")
    if not output_matches_candidate:
        if _guarded_entry_exists(parent_guard, output_name):
            _preserve_pi_unexpected_entry(
                parent_guard, output_name, output_name, label
            )
        raise ValueError(f"Pi probe evidence persistence rollback is ambiguous: {label}")
    _renameatx(
        output_name,
        candidate_name,
        RENAME_EXCL,
        source_dir_fd=parent_guard["fd"],
        destination_dir_fd=parent_guard["fd"],
    )
    os.fsync(parent_guard["fd"])
    if _guarded_entry_exists(parent_guard, output_name):
        raise ValueError(f"Pi probe evidence persistence rollback is ambiguous: {label}")
    try:
        _assert_parent_guard(parent_guard, label)
    except BaseException as exc:
        raise ValueError(f"Pi probe evidence persistence rollback is ambiguous: {label}") from exc


def _create_pi_blocked_recovery(
    parent_guard: dict,
    output_name: str,
    content: bytes,
    label: str,
) -> str:
    """Create BLOCKED through a visible pending-to-final rename boundary."""
    blocked_bytes = bytes(content)
    blocked_expected = {
        "kind": "file",
        "sha256": hashlib.sha256(blocked_bytes).hexdigest(),
        "mode": 0o600,
    }
    flags = os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    for _ in range(32):
        pending_name = _visible_recovery_name(output_name, "persistence-pending")
        descriptor = None
        try:
            descriptor = os.open(pending_name, flags, 0o600, dir_fd=parent_guard["fd"])
        except OSError as exc:
            if isinstance(exc, FileExistsError) or exc.errno in {
                errno.EEXIST, errno.ENOTEMPTY
            }:
                continue
            raise
        try:
            os.fchmod(descriptor, 0o600)
            _write_descriptor(descriptor, blocked_bytes)
            binding = _descriptor_binding(descriptor, label)
            if (
                binding["mode"] != 0o600
                or binding["sha256"] != blocked_expected["sha256"]
            ):
                raise ValueError(f"{label} blocked recovery binding drift")
            os.fsync(descriptor)
            os.fsync(parent_guard["fd"])
            _assert_parent_guard(parent_guard, label)
            _require_retained_binding(
                parent_guard,
                pending_name,
                binding,
                label,
                expected=blocked_expected,
            )
            _assert_parent_guard(parent_guard, label)
            _require_retained_binding(
                parent_guard,
                pending_name,
                binding,
                label,
                expected=blocked_expected,
            )
            _assert_parent_guard(parent_guard, label)
            for _ in range(32):
                blocked_name = _visible_recovery_name(
                    output_name, "persistence-blocked"
                )
                try:
                    _renameatx(
                        pending_name,
                        blocked_name,
                        RENAME_EXCL,
                        source_dir_fd=parent_guard["fd"],
                        destination_dir_fd=parent_guard["fd"],
                    )
                except BaseException as exc:
                    if isinstance(exc, OSError) and (
                        isinstance(exc, FileExistsError)
                        or exc.errno in {errno.EEXIST, errno.ENOTEMPTY}
                    ):
                        continue
                    # The namespace may already contain the destination even
                    # when renameatx_np reports an error.  Inspect both names
                    # before accepting any persistence-blocked evidence.
                    blocked_matches = False
                    if _guarded_entry_exists(parent_guard, blocked_name):
                        blocked_matches = _retained_binding_matches_name(
                            parent_guard,
                            blocked_name,
                            binding,
                            label,
                            expected=blocked_expected,
                            allow_rename_ctime=True,
                        )
                    pending_exists = _guarded_entry_exists(parent_guard, pending_name)
                    if blocked_matches and not pending_exists:
                        try:
                            os.fsync(parent_guard["fd"])
                            _assert_parent_guard(parent_guard, label)
                            _require_retained_binding(
                                parent_guard,
                                blocked_name,
                                binding,
                                label,
                                expected=blocked_expected,
                                allow_rename_ctime=True,
                            )
                            _assert_parent_guard(parent_guard, label)
                            _require_retained_binding(
                                parent_guard,
                                blocked_name,
                                binding,
                                label,
                                expected=blocked_expected,
                                allow_rename_ctime=True,
                            )
                        except BaseException:
                            blocked_matches = False
                    if not blocked_matches:
                        if _guarded_entry_exists(parent_guard, blocked_name):
                            _preserve_pi_unexpected_entry(
                                parent_guard, blocked_name, output_name, label
                            )
                        if _guarded_entry_exists(parent_guard, pending_name):
                            _preserve_pi_unexpected_entry(
                                parent_guard, pending_name, output_name, label
                            )
                    raise ValueError(
                        f"{label} persistence-blocked rename boundary is ambiguous"
                    ) from exc
                try:
                    os.fsync(parent_guard["fd"])
                    _assert_parent_guard(parent_guard, label)
                    _require_retained_binding(
                        parent_guard,
                        blocked_name,
                        binding,
                        label,
                        expected=blocked_expected,
                        allow_rename_ctime=True,
                    )
                    _assert_parent_guard(parent_guard, label)
                    _require_retained_binding(
                        parent_guard,
                        blocked_name,
                        binding,
                        label,
                        expected=blocked_expected,
                        allow_rename_ctime=True,
                    )
                    _assert_parent_guard(parent_guard, label)
                    return blocked_name
                except BaseException:
                    if _guarded_entry_exists(parent_guard, blocked_name):
                        _move_entry_to_visible_recovery(
                            parent_guard,
                            blocked_name,
                            output_name,
                            "persistence-unsafe",
                            label,
                        )
                    raise
            raise ValueError(f"{label} persistence quarantine collision")
        except BaseException:
            if _guarded_entry_exists(parent_guard, pending_name):
                _move_entry_to_visible_recovery(
                    parent_guard,
                    pending_name,
                    output_name,
                    "persistence-unsafe",
                    label,
                )
            raise
        finally:
            if descriptor is not None:
                try:
                    os.close(descriptor)
                except OSError:
                    pass
    raise ValueError(f"{label} persistence quarantine collision")


def _preserve_pi_entry_as_unsafe(
    parent_guard: dict,
    name: str,
    output_name: str,
    ownership: dict,
    label: str,
) -> str | None:
    """Move the current namespace entry to an explicit non-evidence name."""
    moved_name = _move_entry_to_visible_recovery(
        parent_guard,
        name,
        output_name,
        "persistence-unsafe",
        label,
    )
    if moved_name is None:
        return None
    os.fsync(parent_guard["fd"])
    _assert_parent_guard(parent_guard, label)
    if not _retained_object_binding_matches_name(
        parent_guard, moved_name, ownership, label
    ):
        raise ValueError(f"{label} persistence recovery object identity is ambiguous")
    return moved_name


def _remove_exact_pi_unsafe_entry(
    parent_guard: dict,
    unsafe_name: str,
    ownership: dict,
    expected: dict,
    label: str,
) -> None:
    """Remove only an exact object through a name-bound rename boundary."""
    upgraded = None
    try:
        access_flags = fcntl.fcntl(ownership["fd"], fcntl.F_GETFL)
        if (access_flags & os.O_ACCMODE) == os.O_RDONLY:
            upgraded = _open_guarded_binding(
                parent_guard, unsafe_name, label, writable=True
            )
            if (
                not _binding_stable_identity_matches(upgraded, ownership)
                or _binding_prestate(upgraded) != expected
            ):
                raise ValueError(f"{label} retained writable binding drift")
            ownership = upgraded
        _require_retained_binding(
            parent_guard,
            unsafe_name,
            ownership,
            label,
            allow_rename_ctime=True,
        )
        cleanup_name = _visible_recovery_name(
            parent_guard["name"], "persistence-cleanup"
        )
        _renameatx(
            unsafe_name,
            cleanup_name,
            RENAME_EXCL,
            source_dir_fd=parent_guard["fd"],
            destination_dir_fd=parent_guard["fd"],
        )
        try:
            os.fsync(parent_guard["fd"])
            _assert_parent_guard(parent_guard, label)
            _require_retained_binding(
                parent_guard,
                cleanup_name,
                ownership,
                label,
                allow_rename_ctime=True,
            )
            previous_unlink_context = parent_guard.get("_bound_unlink_context")
            unlink_context = {
                "name": cleanup_name,
                "ownership": ownership,
                "expected": expected,
                "label": label,
                "allow_rename_ctime": True,
                "recovery_output_name": parent_guard["name"],
                "recovery_suffix": "persistence-unsafe",
                "blocked_suffix": "persistence-blocked",
                "blocked_content": _canonical_json_bytes(_blocked_pi_probe_result()),
            }
            parent_guard["_bound_unlink_context"] = unlink_context
            try:
                _guarded_unlink(parent_guard, cleanup_name)
            finally:
                if previous_unlink_context is None:
                    parent_guard.pop("_bound_unlink_context", None)
                else:
                    parent_guard["_bound_unlink_context"] = previous_unlink_context
            os.fsync(parent_guard["fd"])
            _assert_parent_guard(parent_guard, label)
        except BaseException:
            if unlink_context.get("deleted"):
                try:
                    _write_bound_unlink_blocker(
                        parent_guard, unlink_context, label
                    )
                except BaseException:
                    pass
            if _guarded_entry_exists(parent_guard, cleanup_name):
                _move_entry_to_visible_recovery(
                    parent_guard,
                    cleanup_name,
                    parent_guard["name"],
                    "persistence-unsafe",
                    label,
                )
    except BaseException:
        # An explicit unsafe recovery object is the required fail-closed
        # residue when cleanup cannot be proven durable.
        if upgraded is not None:
            try:
                os.close(upgraded["fd"])
            except OSError:
                pass
        return
    if upgraded is not None:
        try:
            os.close(upgraded["fd"])
        except OSError:
            pass


def _rewrite_guarded_pi_evidence(
    parent_guard: dict,
    name: str,
    expected: dict,
    content: bytes,
    label: str,
    *,
    ownership: dict,
    allow_rename_ctime: bool = False,
) -> str:
    try:
        binding = _open_guarded_binding(
            parent_guard,
            name,
            "Pi probe evidence persistence rollback",
            writable=True,
        )
    except ValueError as exc:
        raise ValueError("Pi probe evidence persistence rollback is ambiguous") from exc
    validation_error = None
    unsafe_name = None
    blocked_name = None
    try:
        try:
            rollback_label = "Pi probe evidence persistence rollback"
            identity_matches = (
                _binding_stable_identity_matches
                if allow_rename_ctime
                else _binding_identity_matches
            )
            if (
                _binding_prestate(binding) != expected
                or not identity_matches(binding, ownership)
                or not _guarded_identity_matches(parent_guard, name, binding)
                or not _stable_binding_matches(
                    binding["fd"],
                    binding,
                    rollback_label,
                    expected=expected,
                    allow_rename_ctime=allow_rename_ctime,
                )
                or not _stable_binding_matches(
                    binding["fd"],
                    binding,
                    rollback_label,
                    expected=expected,
                    allow_rename_ctime=allow_rename_ctime,
                )
                or not _retained_binding_matches_name(
                    parent_guard,
                    name,
                    ownership,
                    rollback_label,
                    expected=expected,
                    allow_rename_ctime=allow_rename_ctime,
                )
            ):
                raise ValueError("Pi probe evidence persistence rollback is ambiguous")
            _assert_parent_guard(parent_guard, label)
        except BaseException as exc:
            validation_error = exc

        try:
            unsafe_name = _preserve_pi_entry_as_unsafe(
                parent_guard, name, parent_guard["name"], ownership, label
            )
            if unsafe_name is None and validation_error is None:
                validation_error = ValueError(
                    "Pi probe evidence persistence rollback is ambiguous"
                )
        except BaseException as exc:
            if validation_error is None:
                validation_error = exc

        try:
            blocked_name = _create_pi_blocked_recovery(
                parent_guard, parent_guard["name"], bytes(content), label
            )
        except BaseException as exc:
            if validation_error is None:
                validation_error = exc

        if blocked_name is None:
            if validation_error is None:
                validation_error = ValueError(
                    "Pi probe evidence persistence rollback is ambiguous"
                )
        elif unsafe_name is not None and validation_error is None:
            _remove_exact_pi_unsafe_entry(
                parent_guard, unsafe_name, ownership, expected, label
            )
        if validation_error is not None:
            raise ValueError(
                "Pi probe evidence persistence rollback is ambiguous"
            ) from validation_error
        return blocked_name
    finally:
        os.close(binding["fd"])


def _quarantine_pi_probe_candidate(
    parent_guard: dict,
    candidate_name: str,
    expected: dict,
    output_name: str,
    label: str,
    *,
    ownership: dict,
    allow_rename_ctime: bool = False,
) -> None:
    _assert_parent_guard(parent_guard, label)
    _require_retained_binding(
        parent_guard,
        candidate_name,
        ownership,
        label,
        expected=expected,
        allow_rename_ctime=allow_rename_ctime,
    )
    _rewrite_guarded_pi_evidence(
        parent_guard,
        candidate_name,
        expected,
        _canonical_json_bytes(_blocked_pi_probe_result()),
        label,
        ownership=ownership,
        allow_rename_ctime=allow_rename_ctime,
    )


def execute_pi_probe(args) -> tuple[dict, bool]:
    """Run Pi and reduce every setup, launch, or output failure to BLOCKED."""
    try:
        result, success = _execute_pi_probe(args)
    except Exception:
        result, success = _blocked_pi_probe_result(), False
    try:
        _persist_pi_probe_result(args, result)
    except Exception:
        result, success = _blocked_pi_probe_result(), False
    return result, success


def _safe_scoped_path(relative_path) -> str:
    try:
        return _require_portable_path(relative_path)
    except ValueError:
        raise ValueError("scoped file path is invalid or denied") from None


def _parse_scoped_selection(manifest: dict, raw_selectors, managed_rule) -> tuple[set[tuple[str, str]], list[dict]]:
    if manifest["managed_rules"]["version"] != 6:
        raise ValueError("scoped selection requires managed-rule version 6")
    if type(managed_rule) is not bool:
        raise ValueError("managed-rule selector must be boolean")
    if not isinstance(raw_selectors, list):
        raise ValueError("file selectors must be a list")
    known: list[tuple[str, str]] = []
    target_by_pair: dict[tuple[str, str], list[str]] = {}
    for skill in manifest["skills"]:
        for item in skill["files"]:
            pair = (skill["name"], item["path"])
            known.append(pair)
            target_by_pair[pair] = item["targets"]
    known_set = set(known)
    selected: set[tuple[str, str]] = set()
    for raw in raw_selectors:
        if not isinstance(raw, str) or ":" not in raw:
            raise ValueError("file selector must use skill:path syntax")
        skill_name, relative_path = raw.split(":", 1)
        if not _nonblank(skill_name):
            raise ValueError("file selector skill must be non-blank")
        relative_path = _safe_scoped_path(relative_path)
        pair = (skill_name, relative_path)
        if pair not in known_set:
            raise ValueError("selected file is not declared by the manifest")
        if pair in selected:
            raise ValueError("duplicate selected file")
        if target_by_pair[pair] != list(TARGET_ORDER):
            raise ValueError("selected file must target every schema-6 runtime")
        selected.add(pair)
    if not selected and not managed_rule:
        raise ValueError("scoped selection must select a file or managed rule")
    normalized = [
        {"skill": skill_name, "path": relative_path}
        for skill_name, relative_path in known
        if (skill_name, relative_path) in selected
    ]
    return selected, normalized


def generate_plan(args) -> dict:
    manifest_path = args.manifest.resolve(strict=True)
    manifest = _load_json(manifest_path)
    validate_manifest(manifest)
    raw_selectors = getattr(args, "select_file", None)
    managed_rule_selected = getattr(args, "select_managed_rule", False)
    if raw_selectors is None:
        raw_selectors = []
    scoped = bool(raw_selectors) or bool(managed_rule_selected)
    selected_pairs: set[tuple[str, str]] = set()
    normalized_selection: list[dict] = []
    if scoped:
        selected_pairs, normalized_selection = _parse_scoped_selection(
            manifest, raw_selectors, managed_rule_selected
        )
    sources = {
        "openspec": args.openspec_source.resolve(strict=True),
        "brief": args.brief_source.resolve(strict=True),
    }
    for alias, root in sources.items():
        if not root.is_dir() or root.is_symlink():
            raise ValueError(f"invalid {alias} source root: {root}")
    target_paths = _target_arguments(args)
    target_states = {item["id"]: dict(item) for item in manifest["targets"]}
    targets: dict[str, dict] = {}
    for target_id, paths in target_paths.items():
        skills_root = Path(paths["skills_root"])
        rule_file = Path(paths["rule_file"])
        if not skills_root.is_dir() or skills_root.is_symlink():
            raise ValueError(f"invalid target skill root: {target_id}")
        canonical_rule = _canonical_rule_destination(target_id, skills_root)
        if rule_file != canonical_rule:
            raise ValueError(f"{target_id} global rule destination is not canonical")
        _regular_file(rule_file, f"{target_id} global rule file")
        targets[target_id] = {
            **target_states[target_id],
            **paths,
            "rule_pre_state": capture_destination_prestate(rule_file),
            "files": [],
        }
        if scoped:
            targets[target_id]["assertions"] = []
    for skill in manifest["skills"]:
        source_root = sources[skill["source_alias"]]
        for item in skill["files"]:
            source = validate_relative_path(source_root, item["path"])
            digest = _sha256(source)
            pair = (skill["name"], item["path"])
            for target_id in item["targets"]:
                skills_root = Path(targets[target_id]["skills_root"])
                destination = skills_root / skill["name"] / Path(item["path"])
                _contained(skills_root, destination, "skill destination")
                record = {
                    "skill": skill["name"],
                    "source_alias": skill["source_alias"],
                    "path": item["path"],
                    "sha256": digest,
                    "destination": str(destination),
                    "pre_state": capture_destination_prestate(destination),
                }
                if scoped and pair not in selected_pairs:
                    targets[target_id]["assertions"].append(record)
                else:
                    targets[target_id]["files"].append(record)
    rules = manifest["managed_rules"]
    rule_source = validate_relative_path(sources["openspec"], rules["source"])
    managed_rules = {
        "version": rules["version"],
        "source_alias": "openspec",
        "path": rules["source"],
        "sha256": _sha256(rule_source),
        "invariant_ids": rules["invariant_ids"],
    }
    if not scoped:
        return {
            "schema_version": 1,
            "manifest_path": str(manifest_path),
            "manifest_sha256": _sha256(manifest_path),
            "sources": {alias: str(root) for alias, root in sources.items()},
            "managed_rules": managed_rules,
            "targets": targets,
        }

    canonical_rule = rule_source.read_text(encoding="utf-8")
    for target_id, target in targets.items():
        skills_root = Path(target["skills_root"])
        assertion_groups: dict[str, list[dict]] = {}
        for item in target["assertions"]:
            assertion_groups.setdefault(item["skill"], []).append(item)
        for skill_name, records in assertion_groups.items():
            source_alias = records[0]["source_alias"]
            validate_portable_parity(
                Path(sources[source_alias]),
                skills_root / skill_name,
                [{"path": item["path"], "sha256": item["sha256"]} for item in records],
            )
        if not managed_rule_selected:
            validate_managed_rule_parity(
                canonical_rule,
                Path(target["rule_file"]).read_text(encoding="utf-8"),
                version=rules["version"],
                invariant_ids=rules["invariant_ids"],
            )

    scoped_targets = {}
    for target_id, target in targets.items():
        state = {key: target[key] for key in target_states[target_id]}
        scoped_targets[target_id] = {
            **state,
            "skills_root": target["skills_root"],
            "files": target["files"],
            "assertions": target["assertions"],
            "managed_rule": {
                "selected": managed_rule_selected,
                "destination": target["rule_file"],
                "pre_state": target["rule_pre_state"],
            },
        }
    return {
        "schema_version": 2,
        "manifest_path": str(manifest_path),
        "manifest_sha256": _sha256(manifest_path),
        "sources": {alias: str(root) for alias, root in sources.items()},
        "selection": {
            "files": normalized_selection,
            "managed_rule": managed_rule_selected,
        },
        "managed_rules": managed_rules,
        "targets": scoped_targets,
    }


def _validate_v1_plan(plan: dict) -> dict:
    required = {"schema_version", "manifest_path", "manifest_sha256", "sources", "managed_rules", "targets"}
    if not isinstance(plan, dict) or set(plan) != required or plan["schema_version"] != 1:
        raise ValueError("sync plan fields or schema are invalid")
    manifest_path = Path(plan["manifest_path"])
    if _sha256(validate_relative_path(manifest_path.parent, manifest_path.name)) != plan["manifest_sha256"]:
        raise ValueError("sync plan manifest SHA-256 drift")
    manifest = _load_json(manifest_path)
    validate_manifest(manifest)
    if set(plan["sources"]) != {"openspec", "brief"} or set(plan["targets"]) != TARGET_IDS:
        raise ValueError("sync plan sources or targets are invalid")
    source_roots = {alias: Path(root) for alias, root in plan["sources"].items()}
    for root in source_roots.values():
        path = Path(root)
        if not path.is_dir() or path.is_symlink():
            raise ValueError(f"invalid source root in plan: {path}")
    rules = manifest["managed_rules"]
    rule_source = validate_relative_path(source_roots["openspec"], rules["source"])
    expected_rules = {
        "version": rules["version"],
        "source_alias": "openspec",
        "path": rules["source"],
        "sha256": _sha256(rule_source),
        "invariant_ids": rules["invariant_ids"],
    }
    if plan["managed_rules"] != expected_rules:
        raise ValueError("sync plan managed-rule binding is stale or tampered")
    manifest_targets = {item["id"]: item for item in manifest["targets"]}
    state_fields = set(next(iter(manifest_targets.values())))
    for target_id, target in plan["targets"].items():
        if not isinstance(target, dict) or set(target) != state_fields | {
            "skills_root", "rule_file", "rule_pre_state", "files"
        }:
            raise ValueError(f"sync plan target fields are invalid: {target_id}")
        if {key: target[key] for key in state_fields} != manifest_targets[target_id]:
            raise ValueError(f"sync plan target state is stale or tampered: {target_id}")
        skills_root = Path(target["skills_root"])
        if not skills_root.is_dir() or skills_root.is_symlink():
            raise ValueError(f"invalid target skill root in plan: {target_id}")
        canonical_rule = _canonical_rule_destination(target_id, skills_root)
        if Path(target["rule_file"]) != canonical_rule:
            raise ValueError(f"sync plan global rule destination is stale or tampered: {target_id}")
        _regular_file(Path(target["rule_file"]), f"{target_id} global rule file")
        rule_pre_state = _validate_prestate_shape(
            target["rule_pre_state"], f"{target_id} global rule file"
        )
        if rule_pre_state["kind"] != "file":
            raise ValueError(f"global rule pre-state must be a file: {target_id}")
        expected_files = []
        for skill in manifest["skills"]:
            for item in skill["files"]:
                if target_id not in item["targets"]:
                    continue
                source = validate_relative_path(source_roots[skill["source_alias"]], item["path"])
                expected_files.append({
                    "skill": skill["name"],
                    "source_alias": skill["source_alias"],
                    "path": item["path"],
                    "sha256": _sha256(source),
                })
        if len(target["files"]) != len(expected_files):
            raise ValueError(f"sync plan portable-file binding is stale or tampered: {target_id}")
        for planned, expected in zip(target["files"], expected_files):
            if not isinstance(planned, dict) or set(planned) != set(expected) | {
                "destination", "pre_state"
            }:
                raise ValueError(f"sync plan portable-file fields are invalid: {target_id}")
            if {key: planned[key] for key in expected} != expected:
                raise ValueError(f"sync plan portable-file binding is stale or tampered: {target_id}")
            expected_destination = str(
                skills_root / planned["skill"] / Path(planned["path"])
            )
            if planned["destination"] != expected_destination:
                raise ValueError(f"sync plan destination is stale or tampered: {target_id}")
            _contained(skills_root, Path(planned["destination"]), "skill destination")
            _validate_prestate_shape(
                planned["pre_state"],
                f"{target_id}:{planned['skill']}/{planned['path']}",
            )
    return plan


def _validate_scoped_plan(plan: dict) -> dict:
    required = {
        "schema_version", "manifest_path", "manifest_sha256", "sources",
        "selection", "managed_rules", "targets",
    }
    if (
        not isinstance(plan, dict)
        or set(plan) != required
        or plan["schema_version"] != 2
    ):
        raise ValueError("scoped sync plan fields or schema are invalid")
    manifest_path = Path(plan["manifest_path"])
    if _sha256(validate_relative_path(manifest_path.parent, manifest_path.name)) != plan["manifest_sha256"]:
        raise ValueError("sync plan manifest SHA-256 drift")
    manifest = _load_json(manifest_path)
    validate_manifest(manifest)
    if manifest["managed_rules"]["version"] != 6:
        raise ValueError("scoped sync plan requires managed-rule version 6")
    if set(plan["sources"]) != {"openspec", "brief"} or set(plan["targets"]) != TARGET_IDS:
        raise ValueError("scoped sync plan sources or targets are invalid")
    source_roots = {alias: Path(root) for alias, root in plan["sources"].items()}
    for root in source_roots.values():
        if not root.is_dir() or root.is_symlink():
            raise ValueError(f"invalid source root in plan: {root}")

    rules = manifest["managed_rules"]
    rule_source = validate_relative_path(source_roots["openspec"], rules["source"])
    expected_rules = {
        "version": rules["version"],
        "source_alias": "openspec",
        "path": rules["source"],
        "sha256": _sha256(rule_source),
        "invariant_ids": rules["invariant_ids"],
    }
    if plan["managed_rules"] != expected_rules:
        raise ValueError("scoped sync plan managed-rule binding is stale or tampered")

    selection = plan["selection"]
    if not isinstance(selection, dict) or set(selection) != {"files", "managed_rule"}:
        raise ValueError("scoped selection fields are invalid")
    if type(selection["managed_rule"]) is not bool or not isinstance(selection["files"], list):
        raise ValueError("scoped selection values are invalid")
    all_entries = []
    known: set[tuple[str, str]] = set()
    target_by_pair: dict[tuple[str, str], list[str]] = {}
    for skill in manifest["skills"]:
        for item in skill["files"]:
            pair = (skill["name"], item["path"])
            known.add(pair)
            target_by_pair[pair] = item["targets"]
            source = validate_relative_path(source_roots[skill["source_alias"]], item["path"])
            all_entries.append(
                {
                    "skill": skill["name"],
                    "source_alias": skill["source_alias"],
                    "path": item["path"],
                    "sha256": _sha256(source),
                    "targets": item["targets"],
                }
            )
    selected: set[tuple[str, str]] = set()
    for item in selection["files"]:
        if not isinstance(item, dict) or set(item) != {"skill", "path"}:
            raise ValueError("scoped selection file fields are invalid")
        skill_name = item["skill"]
        relative_path = _safe_scoped_path(item["path"])
        pair = (skill_name, relative_path)
        if pair not in known:
            raise ValueError("scoped selection contains an unknown file")
        if pair in selected:
            raise ValueError("scoped selection contains a duplicate file")
        if target_by_pair[pair] != list(TARGET_ORDER):
            raise ValueError("scoped selection file is not target-complete")
        selected.add(pair)
    expected_selection = [
        {"skill": entry["skill"], "path": entry["path"]}
        for entry in all_entries
        if (entry["skill"], entry["path"]) in selected
    ]
    if selection["files"] != expected_selection:
        raise ValueError("scoped selection order or closure is stale or tampered")
    if not selected and not selection["managed_rule"]:
        raise ValueError("scoped selection has no mutation operation")

    manifest_targets = {item["id"]: item for item in manifest["targets"]}
    state_fields = set(next(iter(manifest_targets.values())))

    def validate_file_records(planned, expected, target_id, category):
        if not isinstance(planned, list) or len(planned) != len(expected):
            raise ValueError(f"scoped {category} closure is stale or tampered: {target_id}")
        for record, expected_entry in zip(planned, expected):
            expected_fields = {
                key: expected_entry[key]
                for key in ("skill", "source_alias", "path", "sha256")
            }
            if not isinstance(record, dict) or set(record) != set(expected_fields) | {
                "destination", "pre_state"
            }:
                raise ValueError(f"scoped {category} fields are invalid: {target_id}")
            if {key: record[key] for key in expected_fields} != expected_fields:
                raise ValueError(f"scoped {category} binding is stale or tampered: {target_id}")
            skills_root = Path(plan["targets"][target_id]["skills_root"])
            expected_destination = str(
                skills_root / record["skill"] / Path(record["path"])
            )
            if record["destination"] != expected_destination:
                raise ValueError(f"scoped destination is stale or tampered: {target_id}")
            _contained(skills_root, Path(record["destination"]), "skill destination")
            _validate_prestate_shape(
                record["pre_state"],
                f"{target_id}:{record['skill']}/{record['path']}",
            )

    for target_id, target in plan["targets"].items():
        expected_target_fields = state_fields | {
            "skills_root", "files", "assertions", "managed_rule"
        }
        if not isinstance(target, dict) or set(target) != expected_target_fields:
            raise ValueError(f"scoped target fields are invalid: {target_id}")
        if {key: target[key] for key in state_fields} != manifest_targets[target_id]:
            raise ValueError(f"scoped target state is stale or tampered: {target_id}")
        skills_root = Path(target["skills_root"])
        if not skills_root.is_dir() or skills_root.is_symlink():
            raise ValueError(f"invalid target skill root in plan: {target_id}")
        canonical_rule = _canonical_rule_destination(target_id, skills_root)
        selected_entries = [
            entry
            for entry in all_entries
            if target_id in entry["targets"]
            and (entry["skill"], entry["path"]) in selected
        ]
        assertion_entries = [
            entry
            for entry in all_entries
            if target_id in entry["targets"]
            and (entry["skill"], entry["path"]) not in selected
        ]
        validate_file_records(target["files"], selected_entries, target_id, "operation")
        validate_file_records(target["assertions"], assertion_entries, target_id, "assertion")
        managed = target["managed_rule"]
        if not isinstance(managed, dict) or set(managed) != {
            "selected", "destination", "pre_state"
        }:
            raise ValueError(f"scoped managed-rule fields are invalid: {target_id}")
        if managed["selected"] != selection["managed_rule"]:
            raise ValueError(f"scoped managed-rule selection is stale or tampered: {target_id}")
        if Path(managed["destination"]) != canonical_rule:
            raise ValueError(f"scoped global rule destination is stale or tampered: {target_id}")
        _regular_file(Path(managed["destination"]), f"{target_id} global rule file")
        rule_pre_state = _validate_prestate_shape(
            managed["pre_state"], f"{target_id} global rule file"
        )
        if rule_pre_state["kind"] != "file":
            raise ValueError(f"global rule pre-state must be a file: {target_id}")
    return plan


def _validate_plan(plan: dict) -> dict:
    if not isinstance(plan, dict):
        raise ValueError("sync plan fields or schema are invalid")
    if plan.get("schema_version") == 1:
        return _validate_v1_plan(plan)
    if plan.get("schema_version") == 2:
        return _validate_scoped_plan(plan)
    raise ValueError("sync plan fields or schema are invalid")


def _read_plan(path: Path) -> dict:
    return _validate_plan(_load_json(path.resolve(strict=True)))


def _target_verification_items(plan: dict, target_id: str) -> list[dict]:
    target = plan["targets"][target_id]
    if plan["schema_version"] == 2:
        return [*target["files"], *target["assertions"]]
    return list(target["files"])


def _target_rule_binding(plan: dict, target_id: str) -> tuple[dict, bool]:
    target = plan["targets"][target_id]
    canonical_rule = _canonical_rule_destination(
        target_id, Path(target["skills_root"])
    )
    if plan["schema_version"] == 2:
        managed = target["managed_rule"]
        if Path(managed["destination"]) != canonical_rule:
            raise ValueError(f"global rule destination is stale or tampered: {target_id}")
        return managed, managed["selected"]
    if Path(target["rule_file"]) != canonical_rule:
        raise ValueError(f"global rule destination is stale or tampered: {target_id}")
    return {
        "destination": target["rule_file"],
        "pre_state": target["rule_pre_state"],
    }, True


def _target_records(plan: dict, target_id: str) -> dict[str, list[dict]]:
    records: dict[str, list[dict]] = {}
    for item in _target_verification_items(plan, target_id):
        records.setdefault(item["skill"], []).append(
            {"path": item["path"], "sha256": item["sha256"]}
        )
    return records


def _assert_target_prestate(plan: dict, target_id: str) -> bool:
    for item in _target_verification_items(plan, target_id):
        assert_destination_prestate(
            Path(item["destination"]),
            item["pre_state"],
            f"{target_id}:{item['skill']}/{item['path']}",
        )
    rule, _ = _target_rule_binding(plan, target_id)
    assert_destination_prestate(
        Path(rule["destination"]),
        rule["pre_state"],
        f"{target_id}:global-rule",
    )
    return True


def _legacy_apply_target_without_receipt(
    plan: dict, target_id: str, backup_root: Path
) -> list[Path]:
    if target_id not in TARGET_IDS:
        raise ValueError(f"unknown target: {target_id}")
    target = plan["targets"][target_id]
    skills_root = Path(target["skills_root"])
    if not skills_root.is_dir() or skills_root.is_symlink():
        raise ValueError(f"invalid target skill root: {target_id}")
    operations = []
    for item in target["files"]:
        source_root = Path(plan["sources"][item["source_alias"]])
        source = validate_relative_path(source_root, item["path"])
        if _sha256(source) != item["sha256"]:
            raise ValueError(f"source SHA-256 drift: {item['skill']}/{item['path']}")
        destination = Path(item["destination"])
        _contained(skills_root, destination, "skill destination")
        create = item["pre_state"]["kind"] == "absent"
        operations.append({"path": destination, "content": source.read_bytes(), "create": create})
    rule = plan["managed_rules"]
    rule_source = validate_relative_path(Path(plan["sources"][rule["source_alias"]]), rule["path"])
    if _sha256(rule_source) != rule["sha256"]:
        raise ValueError("managed-rule source SHA-256 drift")
    rule_binding, rule_selected = _target_rule_binding(plan, target_id)
    _assert_target_prestate(plan, target_id)
    if rule_selected:
        rule_file = Path(rule_binding["destination"])
        original = rule_file.read_text(encoding="utf-8")
        updated = install_managed_block(original, rule_source.read_text(encoding="utf-8"), version=rule["version"])
        operations.append({"path": rule_file, "content": updated.encode("utf-8"), "sensitive": True})
    _assert_target_prestate(plan, target_id)
    return apply_sync_transaction(
        operations,
        backup_root / target_id,
        verify=lambda: verify_target(plan, target_id),
    )


def verify_target(plan: dict, target_id: str) -> bool:
    if target_id not in TARGET_IDS:
        raise ValueError(f"unknown target: {target_id}")
    target = plan["targets"][target_id]
    skills_root = Path(target["skills_root"])
    verification_items = _target_verification_items(plan, target_id)
    for skill, records in _target_records(plan, target_id).items():
        source_alias = next(
            item["source_alias"]
            for item in verification_items
            if item["skill"] == skill
        )
        validate_portable_parity(
            Path(plan["sources"][source_alias]), skills_root / skill, records
        )
    rule = plan["managed_rules"]
    canonical = validate_relative_path(Path(plan["sources"][rule["source_alias"]]), rule["path"]).read_text(encoding="utf-8")
    rule_binding, _ = _target_rule_binding(plan, target_id)
    rule_text = Path(rule_binding["destination"]).read_text(encoding="utf-8")
    validate_managed_rule_parity(
        canonical,
        rule_text,
        version=rule["version"],
        invariant_ids=rule["invariant_ids"],
    )
    return True


def audit_sources(source_roots) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    content_patterns = (
        ("private-key", re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
        ("assigned-secret", re.compile(rb"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"][A-Za-z0-9_./+\-=]{16,}")),
    )
    for root in source_roots:
        root_path = Path(root).resolve(strict=True)
        for path in root_path.rglob("*"):
            if ".git" in path.parts or not path.is_file() or path.is_symlink():
                continue
            relative = path.relative_to(root_path).as_posix()
            category = _denied_category(relative)
            if category:
                findings.append({"path": relative, "category": category})
                continue
            data = path.read_bytes()
            for label, pattern in content_patterns:
                if pattern.search(data):
                    findings.append({"path": relative, "category": label})
    return findings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan")
    plan.add_argument("--manifest", type=Path, required=True)
    plan.add_argument("--openspec-source", type=Path, required=True)
    plan.add_argument("--brief-source", type=Path, required=True)
    for prefix in ("codex", "pi", "antigravity", "grok"):
        plan.add_argument(f"--{prefix}-skills-root", type=Path, required=True)
        plan.add_argument(f"--{prefix}-rule-file", type=Path, required=True)
    plan.add_argument(
        "--select-file",
        action="append",
        default=None,
        metavar="SKILL:PATH",
        help="select one manifest file for scoped schema-v2 planning (repeatable)",
    )
    plan.add_argument(
        "--select-managed-rule",
        action="store_true",
        help="select the managed global rule for scoped schema-v2 planning",
    )
    plan.add_argument("--output", type=Path, required=True)

    for name in ("apply", "verify"):
        command = commands.add_parser(name)
        command.add_argument("--target", choices=sorted(TARGET_IDS), required=True)
        command.add_argument("--plan", type=Path, required=True)
        command.add_argument("--transaction-receipt", type=Path, required=True)
        if name == "apply":
            command.add_argument("--backup-root", type=Path, required=True)

    verify_all = commands.add_parser("verify-all")
    verify_all.add_argument("--plan", type=Path, required=True)
    verify_all.add_argument("--transaction-root", type=Path, required=True)

    prestate = commands.add_parser("verify-prestate")
    prestate.add_argument("--plan", type=Path, required=True)
    prestate.add_argument(
        "--target", choices=[*TARGET_ORDER, "all"], required=True
    )

    discovery = commands.add_parser("verify-discovery")
    discovery.add_argument("--target", choices=list(TARGET_ORDER), required=True)
    discovery.add_argument("--inspect-json", type=Path)
    discovery.add_argument("--plan", type=Path, required=True)
    discovery.add_argument("--transaction-receipt", type=Path, required=True)
    discovery.add_argument("--consume", action="store_true")

    probe = commands.add_parser("probe-pi")
    probe.add_argument("--pi-executable", type=Path, required=True)
    probe.add_argument("--native-pi-root", type=Path, required=True)
    probe.add_argument("--temporary-root", type=Path, required=True)
    probe.add_argument("--prompt-file", type=Path, required=True)
    probe.add_argument("--read-root", type=Path, action="append", required=True)
    probe.add_argument("--output", type=Path, required=True)

    restore = commands.add_parser("restore-target")
    restore.add_argument("--target", choices=list(TARGET_ORDER), required=True)
    restore.add_argument("--plan", type=Path, required=True)
    restore.add_argument("--backup-root", type=Path, required=True)
    restore.add_argument("--transaction-receipt", type=Path, required=True)

    recover = commands.add_parser("recover-pending")
    recover.add_argument("--plan", type=Path, required=True)
    recover.add_argument("--backup-root", type=Path, required=True)
    recover.add_argument("--transaction-root", type=Path, required=True)

    commit = commands.add_parser("commit-target")
    commit.add_argument("--target", choices=list(TARGET_ORDER), required=True)
    commit.add_argument("--plan", type=Path, required=True)
    commit.add_argument("--transaction-receipt", type=Path, required=True)

    audit = commands.add_parser("audit")
    audit.add_argument("--openspec-source", type=Path, required=True)
    audit.add_argument("--brief-source", type=Path, required=True)
    audit.add_argument("--report-paths-only", action="store_true", required=True)

    source_delta = commands.add_parser("source-delta")
    source_delta.add_argument("--bindings", type=Path, required=True)
    source_delta.add_argument("--router-root", type=Path, required=True)
    source_delta.add_argument("--companion-root", type=Path, required=True)
    source_delta.add_argument("--router-baseline", type=Path, required=True)
    source_delta.add_argument("--companion-baseline", type=Path, required=True)
    source_delta.add_argument("--compare-root", type=Path, required=True)
    source_delta.add_argument("--output", type=Path, required=True)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "plan":
            output = _absolute_without_symlink_resolution(args.output)
            _ensure_private_directory(output.parent)
            plan = generate_plan(args)
            content = (json.dumps(plan, indent=2, sort_keys=True) + "\n").encode("utf-8")
            if output.exists() or output.is_symlink():
                _regular_file(output, "sync plan output")
                atomic_replace(output, content, mode=0o600)
            else:
                atomic_create(output, content, mode=0o600)
            print(json.dumps({"plan": "pass", "output": str(output)}, sort_keys=True))
        elif args.command == "apply":
            plan = _read_plan(args.plan)
            receipt = apply_target(
                plan,
                args.target,
                args.backup_root.resolve(),
                args.transaction_receipt,
                plan_sha256=_sha256(args.plan.resolve(strict=True)),
            )
            print(
                json.dumps(
                    {
                        "apply": "pass",
                        "target": args.target,
                        "receipt_state": receipt["state"],
                    },
                    sort_keys=True,
                )
            )
        elif args.command == "verify":
            plan = _read_plan(args.plan)
            print(
                json.dumps(
                    verify_target_with_receipt(
                        plan,
                        args.target,
                        args.transaction_receipt,
                        plan_sha256=_sha256(args.plan.resolve(strict=True)),
                    ),
                    sort_keys=True,
                )
            )
        elif args.command == "verify-all":
            plan = _read_plan(args.plan)
            print(
                json.dumps(
                    verify_all_receipts(
                        plan,
                        args.transaction_root,
                        plan_sha256=_sha256(args.plan.resolve(strict=True)),
                    ),
                    sort_keys=True,
                )
            )
        elif args.command == "verify-prestate":
            plan = _read_plan(args.plan)
            targets = list(TARGET_ORDER) if args.target == "all" else [args.target]
            for target_id in targets:
                _assert_target_prestate(plan, target_id)
            print(json.dumps({"prestate": "pass", "targets": targets}, sort_keys=True))
        elif args.command == "verify-discovery":
            plan = _read_plan(args.plan)
            print(
                json.dumps(
                    verify_discovery_with_receipt(
                        plan,
                        args.target,
                        args.transaction_receipt,
                        plan_sha256=_sha256(args.plan.resolve(strict=True)),
                        inspect_json=args.inspect_json,
                        consume=args.consume,
                    ),
                    sort_keys=True,
                )
            )
        elif args.command == "commit-target":
            plan = _read_plan(args.plan)
            print(
                json.dumps(
                    commit_target(
                        plan,
                        args.target,
                        args.transaction_receipt,
                        plan_sha256=_sha256(args.plan.resolve(strict=True)),
                    ),
                    sort_keys=True,
                )
            )
        elif args.command == "restore-target":
            plan = _read_plan(args.plan)
            try:
                result = restore_target(
                    plan,
                    args.target,
                    args.backup_root,
                    args.transaction_receipt,
                    plan_sha256=_sha256(args.plan.resolve(strict=True)),
                )
                print(json.dumps(result, sort_keys=True))
            except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
                print(
                    json.dumps(
                        {
                            "restore": "blocked",
                            "target": args.target,
                            "restored": False,
                            "later_targets_started": False,
                        },
                        sort_keys=True,
                    )
                )
                return 1
        elif args.command == "recover-pending":
            plan = _read_plan(args.plan)
            try:
                result = recover_pending(
                    plan,
                    args.backup_root,
                    args.transaction_root,
                    plan_sha256=_sha256(args.plan.resolve(strict=True)),
                )
                print(json.dumps(result, sort_keys=True))
            except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
                print(
                    json.dumps(
                        {
                            "recovery": "blocked",
                            "target": "unresolved",
                            "restored": False,
                            "later_targets_started": False,
                        },
                        sort_keys=True,
                    )
                )
            return 1
        elif args.command == "probe-pi":
            result, success = execute_pi_probe(args)
            print(json.dumps(result, sort_keys=True))
            if not success:
                return 1
        elif args.command == "source-delta":
            print(json.dumps(generate_source_delta(args), sort_keys=True))
        elif args.command == "audit":
            findings = audit_sources([args.openspec_source, args.brief_source])
            for finding in findings:
                print(f"{finding['category']}: {finding['path']}")
            if findings:
                raise ValueError(f"{len(findings)} sensitive categories found")
            print("0 sensitive categories found")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        if args.command == "probe-pi":
            print(json.dumps(_blocked_pi_probe_result(), sort_keys=True))
        else:
            print(f"cross-cli sync validation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
