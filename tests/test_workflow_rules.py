import copy
import importlib.util
import os
import hashlib
import json
import re
import stat
import tempfile
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


PREFLIGHT_BOUNDARIES = (
    "scope", "contract/spec", "acceptance", "risk/evidence profile",
    "authority", "assignments", "allowed/forbidden files", "branch/worktree",
    "database/production", "Git/publication/deployment",
)


def _bound_regular_ref_bytes(root: Path, ref: dict[str, str]) -> bytes | None:
    path = ref.get("path")
    digest = ref.get("sha256")
    if not isinstance(path, str) or not re.fullmatch(r"[A-Za-z0-9._/-]+", path):
        return None
    logical = Path(path)
    if logical.is_absolute() or ".." in logical.parts or "\\" in path:
        return None
    directory_fds = []
    try:
        directory_flags = (
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
            | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
        )
        current_fd = os.open(root, directory_flags)
        directory_fds.append(current_fd)
        for component in logical.parts[:-1]:
            current_fd = os.open(component, directory_flags, dir_fd=current_fd)
            directory_fds.append(current_fd)
        file_fd = os.open(
            logical.parts[-1],
            os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_CLOEXEC", 0),
            dir_fd=current_fd,
        )
        with os.fdopen(file_fd, "rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                return None
            payload = stream.read()
    except (OSError, IndexError):
        return None
    finally:
        for directory_fd in reversed(directory_fds):
            os.close(directory_fd)
    if not isinstance(digest, str) or hashlib.sha256(payload).hexdigest() != digest:
        return None
    return payload


def _safe_regular_ref(root: Path, ref: dict[str, str]) -> bool:
    return _bound_regular_ref_bytes(root, ref) is not None


def _focused_preflight_fixture_eligible(
    root: Path, record: dict, author_id: str, executor_id: str,
) -> bool:
    reviewer = record.get("reviewer_identity", {})
    root_revision = record.get("lineage_root_revision", {})
    current_revision = record.get("reviewed_revision", {})
    parent_ref = record.get("parent_review", {})
    parent_bytes = _bound_regular_ref_bytes(root, parent_ref)
    if parent_bytes is None:
        return False
    try:
        parent = json.loads(parent_bytes)
    except (UnicodeError, json.JSONDecodeError):
        return False
    parent_reviewer = parent.get("reviewer_identity", {})
    return all((
        record.get("review_mode") == "FOCUSED_RECHECK",
        record.get("attempt") in (2, "terminal"),
        record.get("same_reviewer_instance") is True,
        reviewer == parent_reviewer,
        reviewer.get("agent_instance_id") not in {author_id, executor_id, None},
        root_revision.get("path") == current_revision.get("path"),
        parent.get("lineage_root_revision") == root_revision,
        _safe_regular_ref(root, current_revision),
        parent.get("finding_completeness") is True,
        record.get("mechanical_self_check") is True,
        record.get("diff_within_declared_corrections") is True,
        bool(record.get("declared_correction_set")),
        record.get("protected_boundaries")
        == {boundary: "unchanged" for boundary in PREFLIGHT_BOUNDARIES},
    ))


def resolve_brief_root() -> Path:
    configured = os.environ.get("BRIEF_SKILL_SOURCE")
    if configured:
        return Path(configured).resolve()

    companion_name = "codex-brief-antigravity-review"
    candidates = [ROOT.parent / companion_name]
    git_pointer = ROOT / ".git"
    if git_pointer.is_file():
        marker, separator, raw_git_dir = (
            git_pointer.read_text(encoding="utf-8").strip().partition(":")
        )
        if marker == "gitdir" and separator and raw_git_dir.strip():
            git_dir = Path(raw_git_dir.strip())
            if not git_dir.is_absolute():
                git_dir = (ROOT / git_dir).resolve()
            common_git_dir = next(
                (
                    parent
                    for parent in (git_dir, *git_dir.parents)
                    if parent.name == ".git"
                ),
                None,
            )
            if common_git_dir is not None:
                candidates.append(
                    common_git_dir.parent.parent / companion_name
                )

    for candidate in candidates:
        if (candidate / "scripts" / "validate_templates.py").is_file():
            return candidate.resolve()
    return candidates[0].resolve()


BRIEF_ROOT = resolve_brief_root()
BRIEF_HANDOFF = BRIEF_ROOT / "references" / "handoff-contract.md"

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


def markdown_visible_outside_html_comment(
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


def markdown_fence_candidate(
    line: str,
    *,
    closing: bool = False,
) -> tuple[str, str] | None:
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


def markdown_heading_spans(text: str) -> list[tuple[str, int, int, int]]:
    headings: list[tuple[str, int, int, int]] = []
    fence_char: str | None = None
    fence_length = 0
    in_html_comment = False
    offset = 0

    for raw_line in text.splitlines(keepends=True):
        line = raw_line.rstrip("\r\n")
        line_end = offset + len(line)
        if fence_char is not None:
            closing_fence = markdown_fence_candidate(line, closing=True)
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
                markdown_visible_outside_html_comment(
                    line,
                    in_html_comment,
                )
            )
            opening_fence = markdown_fence_candidate(visible_line)
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


def markdown_owned_section_bounds(text: str, heading: str) -> tuple[int, int]:
    heading_syntax = re.fullmatch(r"(#{1,6})[ \t]+[^\r\n]+", heading)
    if heading_syntax is None:
        raise AssertionError(f"invalid Markdown heading: {heading!r}")

    headings = markdown_heading_spans(text)
    matches = [item for item in headings if item[0] == heading]
    if len(matches) != 1:
        raise AssertionError(
            f"expected exactly one Markdown heading {heading!r}, found {len(matches)}"
        )

    _, _, _, section_start = matches[0]
    heading_level = len(heading_syntax.group(1))
    section_end = len(text)
    for _, level, start, _ in headings:
        if start > matches[0][2] and level <= heading_level:
            section_end = start
            break
    return section_start, section_end


def markdown_owned_section(text: str, heading: str) -> str:
    section_start, section_end = markdown_owned_section_bounds(text, heading)
    return text[section_start:section_end]


def strip_markdown_owned_obligation(
    text: str,
    heading: str,
    needle: str,
) -> str:
    section_start, section_end = markdown_owned_section_bounds(text, heading)
    section = text[section_start:section_end]
    if needle not in section:
        raise AssertionError(
            f"{needle!r} missing from Markdown owned section {heading!r}"
        )
    section = section.replace(needle, "removed protected contract")
    return text[:section_start] + section + text[section_end:]


def replace_owned_obligation_with_decoy(
    text: str,
    heading: str,
    needle: str,
    decoy: str,
) -> str:
    section_start, section_end = markdown_owned_section_bounds(text, heading)
    section = text[section_start:section_end]
    if needle not in section:
        raise AssertionError(
            f"{needle!r} missing from Markdown owned section {heading!r}"
        )
    section = section.replace(needle, "removed protected contract")
    section = f"{section.rstrip()}\n\n{decoy}\n"
    return text[:section_start] + section + text[section_end:]


def append_owned_fenced_example(
    text: str,
    heading: str,
    example: str,
) -> str:
    section_start, section_end = markdown_owned_section_bounds(text, heading)
    section = text[section_start:section_end]
    section = f"{section.rstrip()}\n\n{example}\n"
    return text[:section_start] + section + text[section_end:]


def replace_owned_heading_with_fenced_decoy(
    text: str,
    heading: str,
    renamed_heading: str,
    fence_marker: str,
) -> str:
    section = markdown_owned_section(text, heading)
    matches = list(re.finditer(rf"(?m)^{re.escape(heading)}$", text))
    if len(matches) != 1:
        raise AssertionError(
            f"expected one raw heading {heading!r}, found {len(matches)}"
        )
    if not section.endswith(("\n", "\r")):
        section += "\n"
    replacement = (
        f"{renamed_heading}\n\n"
        f"{fence_marker}markdown\n"
        f"{heading}{section}"
        f"{fence_marker}"
    )
    match = matches[0]
    return text[:match.start()] + replacement + text[match.end():]


def artifact(path: str) -> dict[str, str]:
    return {"path": path, "sha256": "a" * 64}


def evidence_manifest(
    role: str,
    result: str,
    change_id: str = "add-example-change",
    current_batch: int = 1,
    attempt: int = 1,
    contract_revision: int = 1,
    canonical_sha256: str = "b" * 64,
    agent_identity: str | None = None,
    agent_role: str | None = None,
) -> str:
    if agent_identity is None or agent_role is None:
        defaults = {
            "attempt-report": ("antigravity-cli", "executor"),
            "batch-review": ("grok-cli", "independent-reviewer"),
            "preflight-review": ("codex", "decision-owner"),
            "timeout-audit": ("codex", "decision-owner"),
            "final-verification": ("codex", "decision-owner"),
            "final-review": ("codex", "decision-owner"),
        }
        default_identity, default_role = defaults[role]
        agent_identity = agent_identity or default_identity
        agent_role = agent_role or default_role
    return (
        "<!-- COOP_EVIDENCE_MANIFEST_START -->\n"
        "```yaml\n"
        "evidence_schema_version: 1\n"
        f"evidence_role: {role}\n"
        f"evidence_result: {result}\n"
        f"change_id: {change_id}\n"
        f"current_batch: {current_batch}\n"
        f"attempt: {attempt}\n"
        f"contract_revision: {contract_revision}\n"
        f"canonical_sha256: {canonical_sha256}\n"
        f"agent_identity: {agent_identity}\n"
        f"agent_role: {agent_role}\n"
        "```\n"
        "<!-- COOP_EVIDENCE_MANIFEST_END -->\n"
    )


def schema5_evidence_manifest(
    role: str,
    result: str,
    change_id: str = "add-example-change",
    current_batch: int = 1,
    attempt: int = 1,
    contract_revision: int = 1,
    canonical_sha256: str = "b" * 64,
    high_review: bool = True,
) -> str:
    assignments = {
        "attempt-report": ("antigravity-cli", "antigravity-executor-01", "executor", "cohesive-medium"),
        "batch-review": ("grok-cli", "grok-reviewer-01", "independent-reviewer", "control-plane-high"),
        "preflight-review": ("codex", "codex-control-01", "control-plane", "control-plane-high"),
        "timeout-audit": ("codex", "codex-control-01", "control-plane", "control-plane-high"),
        "final-verification": ("codex", "codex-control-01", "control-plane", "control-plane-high"),
        "final-review": ("codex", "codex-control-01", "control-plane", "control-plane-high"),
    }
    product, instance, agent_role, profile = assignments[role]
    text = (
        "<!-- COOP_EVIDENCE_MANIFEST_START -->\n"
        "```yaml\n"
        "evidence_schema_version: 2\n"
        f"evidence_role: {role}\n"
        f"evidence_result: {result}\n"
        f"change_id: {change_id}\n"
        f"current_batch: {current_batch}\n"
        f"attempt: {attempt}\n"
        f"contract_revision: {contract_revision}\n"
        f"canonical_sha256: {canonical_sha256}\n"
        f"agent_product: {product}\n"
        f"agent_instance_id: {instance}\n"
        f"agent_role: {agent_role}\n"
        f"capability_profile: {profile}\n"
        "```\n"
        "<!-- COOP_EVIDENCE_MANIFEST_END -->\n"
    )
    if high_review and role in {"batch-review", "final-review"}:
        text += (
            "\nActual files and complete diff inspected\n"
            "Copy/transform/production wiring trace\n"
            "Critical reruns\n"
            "Claim-to-mechanism support\n"
            "Independent adversarial probe\n"
        )
    return text


def materialize_schema5_lease(data: dict, root: Path) -> None:
    text = (
        "<!-- COOP_CONFIRMATION_LEASE_START -->\n"
        "```yaml\n"
        "decision_id: decision-001\n"
        "artifact_revision: 2\n"
        f"artifact_sha256: {'a' * 64}\n"
        "approved_scope: approved source implementation\n"
        "approved_actions:\n"
        "  - run-safe-tests\n"
        "risk_profile: standard\n"
        "decision_source: ai-proposed/user-approved\n"
        "owner_instance_id: codex-control-01\n"
        "status: valid\n"
        "invalidation_conditions:\n"
        "  - scope-change\n"
        "```\n"
        "<!-- COOP_CONFIRMATION_LEASE_END -->\n"
    )
    target = root / data["confirmation_lease"]["path"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    data["confirmation_lease"]["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()


def schema4_contract(validator, handoff: str, **overrides) -> dict:
    data = validator.extract_handoff_contract(handoff, "handoff")
    for key in (
        "control_plane_owner", "executor_assignment",
        "independent_reviewer_assignment", "reviewer_assignment", "decision_source",
        "confirmation_lease", "confirmation_lease_status",
    ):
        data.pop(key, None)
    identity_fields = {
        "executor_agent": "antigravity-cli",
        "independent_reviewer_agent": "grok-cli",
        "decision_owner": "codex",
        "independent_review_not_applicable_reason": None,
    }
    data.update(schema_version=4, **identity_fields)
    data["readonly_fields"] = list(validator.LEGACY_IMMUTABLE_FIELDS)
    data.update(overrides)
    return data


def standard_reviewer_assignment(product="codex", instance="codex-reviewer-02"):
    return {
        "review_purpose": {
            "object": "current batch implementation, Report, contract, and evidence",
            "decision": "decide pass, fail, or blocked for this governed Review gate",
        },
        "agent_product": product,
        "agent_instance_id": instance,
        "agent_role": "independent-reviewer",
        "capability_profile": "control-plane-high",
        "independence_requirement": {
            "kind": "distinct-contract-instance",
            "distinct_from": ["control_plane_owner", "executor_assignment"],
        },
        "result_authority": "governed-review-evidence",
    }


def assert_schema6_fixture(data: dict, *, compact: bool = False) -> None:
    expected_assignment_fields = {
        "review_purpose", "agent_product", "agent_instance_id", "agent_role",
        "capability_profile", "independence_requirement", "result_authority",
    }
    if data.get("schema_version") != 6:
        raise AssertionError("schema-6 fixture has the wrong discriminator")
    if "independent_reviewer_assignment" in data:
        raise AssertionError("schema-5 reviewer field leaked into schema-6 fixture")
    if set(data.get("reviewer_assignment", {})) != expected_assignment_fields:
        raise AssertionError("schema-6 reviewer assignment shape is invalid")
    readonly = data.get("readonly_fields")
    if (
        not isinstance(readonly, list)
        or len(readonly) != len(set(readonly))
        or "reviewer_assignment" not in readonly
        or "independent_reviewer_assignment" in readonly
    ):
        raise AssertionError("schema-6 readonly replacement is invalid")
    if "independence_na_reason" in data:
        raise AssertionError("undefined compact reason field leaked into fixture")
    reason = data.get("independent_review_not_applicable_reason")
    if compact:
        if not isinstance(reason, str) or not reason.strip():
            raise AssertionError("compact fixture requires a nonblank NA reason")
    elif reason is not None:
        raise AssertionError("standard/strict fixture requires a null NA reason")


def schema6_contract(validator, handoff: str, **overrides) -> dict:
    data = validator.extract_handoff_contract(handoff, "handoff")
    if data.get("schema_version") == 5:
        old_assignment = data.pop("independent_reviewer_assignment")
        if set(old_assignment) != {
            "agent_product", "agent_instance_id", "agent_role", "capability_profile",
        }:
            raise AssertionError("unexpected frozen schema-5 reviewer shape")
        data["schema_version"] = 6
        data["reviewer_assignment"] = standard_reviewer_assignment(
            product=old_assignment["agent_product"],
            instance=old_assignment["agent_instance_id"],
        )
        data["readonly_fields"] = [
            "reviewer_assignment" if item == "independent_reviewer_assignment" else item
            for item in data["readonly_fields"]
        ]
    elif data.get("schema_version") != 6:
        raise AssertionError("schema6 test fixture requires schema 5 or schema 6")
    data.update(copy.deepcopy(overrides))
    assert_schema6_fixture(data)
    return data


def schema5_contract(validator, handoff: str, **overrides) -> dict:
    data = validator.extract_handoff_contract(handoff, "handoff")
    if data.get("schema_version") == 6:
        reviewer = data.pop("reviewer_assignment")
        data["schema_version"] = 5
        data["independent_reviewer_assignment"] = {
            key: reviewer[key]
            for key in (
                "agent_product", "agent_instance_id", "agent_role",
                "capability_profile",
            )
        }
        data["readonly_fields"] = [
            "independent_reviewer_assignment"
            if item == "reviewer_assignment" else item
            for item in data["readonly_fields"]
        ]
    elif data.get("schema_version") != 5:
        raise AssertionError("schema5 fixture requires schema 5 or schema 6")
    data.update(copy.deepcopy(overrides))
    return data


def render_handoff_contract(validator, data: dict) -> str:
    def scalar(value) -> str:
        if value is None:
            return "null"
        if value is True:
            return "true"
        if value is False:
            return "false"
        return str(value)

    def render(value, indent: int = 0) -> list[str]:
        prefix = " " * indent
        lines: list[str] = []
        if isinstance(value, dict):
            for key, item in value.items():
                if isinstance(item, (dict, list)):
                    lines.append(f"{prefix}{key}:")
                    lines.extend(render(item, indent + 2))
                else:
                    lines.append(f"{prefix}{key}: {scalar(item)}")
            return lines
        if isinstance(value, list):
            for item in value:
                if isinstance(item, (dict, list)):
                    raise AssertionError("test YAML renderer accepts scalar lists only")
                lines.append(f"{prefix}- {scalar(item)}")
            return lines
        raise AssertionError("test YAML renderer requires a mapping or list")

    payload = "\n".join(render(data))
    parsed = validator.simple_yaml_load(payload)
    if parsed != data:
        raise AssertionError("test YAML renderer did not round-trip the fixture")
    return (
        "<!-- COOP_HANDOFF_CONTRACT_START -->\n"
        "```yaml\n"
        f"{payload}\n"
        "```\n"
        "<!-- COOP_HANDOFF_CONTRACT_END -->\n"
    )


def compact_schema6_contract(validator, handoff: str, **overrides) -> dict:
    data = schema6_contract(validator, handoff)
    owner = data["control_plane_owner"]
    data["risk_profile"] = "compact"
    data["reviewer_assignment"] = {
        "review_purpose": {
            "object": "current compact implementation, evidence, and contract",
            "decision": "decide pass, fail, or blocked for the compact Review gate",
        },
        "agent_product": owner["agent_product"],
        "agent_instance_id": owner["agent_instance_id"],
        "agent_role": owner["agent_role"],
        "capability_profile": owner["capability_profile"],
        "independence_requirement": {
            "kind": "distinct-contract-instance",
            "distinct_from": ["executor_assignment"],
        },
        "result_authority": "governed-review-evidence",
    }
    data["independent_review_not_applicable_reason"] = (
        "compact inline Review is owned by the bound control-plane instance"
    )
    data.update(copy.deepcopy(overrides))
    assert_schema6_fixture(data, compact=True)
    return data


def set_nested(mapping: dict, path: tuple[str, ...], value) -> None:
    target = mapping
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def schema2_assignment_evidence_manifest(
    role: str,
    result: str,
    assignment: dict,
    *,
    change_id: str = "add-example-change",
    current_batch: int = 1,
    attempt: int = 1,
    contract_revision: int = 2,
    canonical_sha256: str = "b" * 64,
) -> str:
    text = (
        "<!-- COOP_EVIDENCE_MANIFEST_START -->\n"
        "```yaml\n"
        "evidence_schema_version: 2\n"
        f"evidence_role: {role}\n"
        f"evidence_result: {result}\n"
        f"change_id: {change_id}\n"
        f"current_batch: {current_batch}\n"
        f"attempt: {attempt}\n"
        f"contract_revision: {contract_revision}\n"
        f"canonical_sha256: {canonical_sha256}\n"
        f"agent_product: {assignment['agent_product']}\n"
        f"agent_instance_id: {assignment['agent_instance_id']}\n"
        f"agent_role: {assignment['agent_role']}\n"
        f"capability_profile: {assignment['capability_profile']}\n"
        "```\n"
        "<!-- COOP_EVIDENCE_MANIFEST_END -->\n"
    )
    if role in {"batch-review", "final-review"}:
        text += (
            "\nActual files and complete diff inspected\n"
            "Copy/transform/production wiring trace\n"
            "Critical reruns\n"
            "Claim-to-mechanism support\n"
            "Independent adversarial probe\n"
        )
    return text


def load_validator():
    path = ROOT / "scripts" / "validate_core_gates.py"
    spec = importlib.util.spec_from_file_location("validate_core_gates", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_routing_runner():
    path = ROOT / "tests" / "run_superpowers_routing_forward_tests.py"
    spec = importlib.util.spec_from_file_location("routing_forward_runner", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class WorkflowRulesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.response_patterns = (
            ROOT / "references" / "response-patterns.md"
        ).read_text(encoding="utf-8")
        cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")
        cls.readme_cn = (ROOT / "README_cn.md").read_text(encoding="utf-8")
        cls.request_modes = (ROOT / "references" / "request-modes.md").read_text(encoding="utf-8")
        cls.approved = (ROOT / "references" / "approved-implementation-workflow.md").read_text(encoding="utf-8")
        cls.completion = (
            ROOT / "references" / "completion-contract.md"
        ).read_text(encoding="utf-8")
        cls.handoff = (ROOT / "references" / "handoff-contract.md").read_text(encoding="utf-8")
        cls.proposal_workflow = (
            ROOT / "references" / "proposal-workflow.md"
        ).read_text(encoding="utf-8")
        cls.superpowers_adapter = (
            ROOT / "references" / "superpowers-adapter.md"
        ).read_text(encoding="utf-8")
        cls.shared_governance = (
            ROOT / "references" / "shared-global-governance.md"
        ).read_text(encoding="utf-8")
        cls.agent_capability_routing = (
            ROOT / "references" / "agent-capability-routing.md"
        ).read_text(encoding="utf-8")
        cls.local_checkpoint = (
            ROOT / "references" / "local-instruction-checkpoint.md"
        ).read_text(encoding="utf-8")
        cls.learning = (
            ROOT / "references" / "learning-candidate-pipeline.md"
        ).read_text(encoding="utf-8")

    def test_governed_caveman_lite_profile_is_entry_discoverable_and_bounded(self):
        frontmatter = self.skill.split("---", 2)[1]
        frontmatter_data = self.validator.yaml_load(frontmatter)
        self.assertIsInstance(frontmatter_data, dict)
        description = frontmatter_data["description"]
        self.assertIsInstance(description, str)
        for command in ("OpenSpec 精简模式", "OpenSpec 正常模式"):
            self.assertIn(command, description)
        self.assertIn("caveman 风格摘要", description)

        heading = "## Governed Caveman Lite output mode"
        profile = markdown_owned_section(self.skill, heading)
        normalized_profile = " ".join(profile.split())
        for obligation in GOVERNED_CAVEMAN_LITE_SKILL_OBLIGATIONS:
            self.assertIn(obligation, normalized_profile)

        response_heading = "### Governed Caveman Lite"
        response_profile = markdown_owned_section(
            self.response_patterns,
            response_heading,
        )
        normalized_response_profile = " ".join(response_profile.split())
        for obligation in GOVERNED_CAVEMAN_LITE_RESPONSE_OBLIGATIONS:
            self.assertIn(obligation, normalized_response_profile)

        legacy_profile = markdown_owned_section(
            self.skill,
            "## Legacy request-scoped output compatibility",
        )
        normalized_legacy_profile = " ".join(legacy_profile.split())
        for obligation in LEGACY_REQUEST_SCOPED_BREVITY_OBLIGATIONS:
            self.assertIn(obligation, normalized_legacy_profile)

        legacy_response = markdown_owned_section(
            self.response_patterns,
            "### Legacy request-scoped brevity",
        )
        normalized_legacy_response = " ".join(legacy_response.split())
        for obligation in LEGACY_REQUEST_SCOPED_BREVITY_OBLIGATIONS:
            self.assertIn(obligation, normalized_legacy_response)

    def test_governed_caveman_lite_validator_binds_owning_artifacts(self):
        self.assertTrue(
            hasattr(self.validator, "validate_governed_caveman_lite"),
            "validator must own governed Caveman Lite checks",
        )
        self.validator.validate_governed_caveman_lite(
            self.skill, self.response_patterns, self.readme, self.readme_cn
        )
        self.validator.validate_governed_caveman_lite(
            self.skill, self.response_patterns
        )
        with self.assertRaisesRegex(AssertionError, "bilingual READMEs"):
            self.validator.validate_governed_caveman_lite(
                self.skill, self.response_patterns, self.readme, None
            )
        with self.assertRaisesRegex(AssertionError, "bilingual READMEs"):
            self.validator.validate_governed_caveman_lite(
                self.skill, self.response_patterns, None, self.readme_cn
            )

        prefix, frontmatter, body = self.skill.split("---", 2)
        frontmatter_data = self.validator.yaml_load(frontmatter)
        self.assertIsInstance(frontmatter_data, dict)
        description = frontmatter_data["description"]
        self.assertIsInstance(description, str)
        for needle, error_label in (
            (
                "OpenSpec 精简模式",
                "SKILL.md governed Caveman Lite frontmatter",
            ),
            (
                "OpenSpec 正常模式",
                "SKILL.md governed Caveman Lite frontmatter",
            ),
            (
                "caveman 风格摘要",
                "SKILL.md legacy Caveman frontmatter",
            ),
        ):
            with self.subTest(owner="SKILL.md frontmatter", needle=needle):
                self.assertIn(needle, description)
                self.assertIn(needle, body)
                stripped_description = description.replace(
                    needle,
                    "removed frontmatter description value",
                )
                self.assertNotIn(needle, stripped_description)
                mutated_frontmatter = frontmatter.replace(
                    description,
                    stripped_description,
                    1,
                )
                mutated_frontmatter += (
                    f'# frontmatter decoy: {needle}\n'
                    f'frontmatter_decoy: "{needle}"\n'
                )
                mutated = f"{prefix}---{mutated_frontmatter}---{body}"
                _, mutated_frontmatter_text, mutated_body = mutated.split(
                    "---",
                    2,
                )
                mutated_data = self.validator.yaml_load(
                    mutated_frontmatter_text
                )
                self.assertNotIn(needle, mutated_data["description"])
                self.assertEqual(mutated_data["frontmatter_decoy"], needle)
                self.assertIn(needle, mutated_frontmatter_text)
                self.assertIn(needle, mutated_body)
                with self.assertRaisesRegex(
                    AssertionError,
                    error_label,
                ):
                    self.validator.validate_governed_caveman_lite(
                        mutated,
                        self.response_patterns,
                        self.readme,
                        self.readme_cn,
                    )

        for needle in GOVERNED_CAVEMAN_LITE_SKILL_OBLIGATIONS:
            with self.subTest(owner="SKILL.md", needle=needle):
                mutated = strip_markdown_owned_obligation(
                    self.skill, "## Governed Caveman Lite output mode", needle
                )
                with self.assertRaisesRegex(
                    AssertionError, "SKILL.md governed Caveman Lite"
                ):
                    self.validator.validate_governed_caveman_lite(
                        mutated,
                        self.response_patterns,
                        self.readme,
                        self.readme_cn,
                    )

        for needle in GOVERNED_CAVEMAN_LITE_RESPONSE_OBLIGATIONS:
            with self.subTest(owner="response-patterns.md", needle=needle):
                mutated = strip_markdown_owned_obligation(
                    self.response_patterns, "### Governed Caveman Lite", needle
                )
                with self.assertRaisesRegex(
                    AssertionError, "response-patterns.md governed Caveman Lite"
                ):
                    self.validator.validate_governed_caveman_lite(
                        self.skill, mutated, self.readme, self.readme_cn
                    )

        for owner, text, heading, decoy_heading, sibling_boundary, error_label in (
            (
                "SKILL.md",
                self.skill,
                "## Legacy request-scoped output compatibility",
                "## Unrelated legacy output compatibility",
                "\n## Mandatory Entry Gate",
                "SKILL.md legacy request-scoped brevity",
            ),
            (
                "response-patterns.md",
                self.response_patterns,
                "### Legacy request-scoped brevity",
                "### Unrelated legacy request brevity",
                "\n### Governed Caveman Lite",
                "response-patterns.md legacy request-scoped brevity",
            ),
        ):
            self.assertNotIn(decoy_heading, text)
            for needle in LEGACY_REQUEST_SCOPED_BREVITY_OBLIGATIONS:
                with self.subTest(owner=owner, legacy_needle=needle):
                    mutated = strip_markdown_owned_obligation(
                        text,
                        heading,
                        needle,
                    )
                    self.assertEqual(mutated.count(sibling_boundary), 1)
                    mutated = mutated.replace(
                        sibling_boundary,
                        f"\n\n{decoy_heading}\n\n{needle}\n{sibling_boundary}",
                        1,
                    )
                    self.assertIn(
                        needle,
                        markdown_owned_section(mutated, decoy_heading),
                    )
                    skill = mutated if owner == "SKILL.md" else self.skill
                    response_patterns = (
                        mutated
                        if owner == "response-patterns.md"
                        else self.response_patterns
                    )
                    with self.assertRaisesRegex(AssertionError, error_label):
                        self.validator.validate_governed_caveman_lite(
                            skill,
                            response_patterns,
                            self.readme,
                            self.readme_cn,
                        )

        for owner, text, heading in (
            ("README.md", self.readme, "## Governed Caveman Lite"),
            ("README_cn.md", self.readme_cn, "## 治理精简模式"),
        ):
            decoy_heading = "## Unrelated command example"
            self.assertNotIn(decoy_heading, text)
            for needle in ("OpenSpec 精简模式：<任务>", "OpenSpec 正常模式"):
                with self.subTest(owner=owner, needle=needle):
                    mutated = strip_markdown_owned_obligation(
                        text,
                        heading,
                        needle,
                    )
                    mutated = (
                        f"{mutated.rstrip()}\n\n{decoy_heading}\n\n{needle}\n"
                    )
                    self.assertIn(
                        needle,
                        markdown_owned_section(mutated, decoy_heading),
                    )
                    readme = mutated if owner == "README.md" else self.readme
                    readme_cn = (
                        mutated if owner == "README_cn.md" else self.readme_cn
                    )
                    with self.assertRaisesRegex(AssertionError, owner):
                        self.validator.validate_governed_caveman_lite(
                            self.skill,
                            self.response_patterns,
                            readme,
                            readme_cn,
                        )

    def test_governed_caveman_lite_validator_ignores_fenced_heading_decoys(self):
        for artifact, text, heading, renamed_heading, fence, error_label in (
            (
                "skill",
                self.skill,
                "## Governed Caveman Lite output mode",
                "## Renamed governed output mode",
                "```",
                "SKILL.md governed Caveman Lite",
            ),
            (
                "skill",
                self.skill,
                "## Legacy request-scoped output compatibility",
                "## Renamed legacy output compatibility",
                "~~~",
                "SKILL.md legacy request-scoped brevity",
            ),
            (
                "response_patterns",
                self.response_patterns,
                "### Governed Caveman Lite",
                "### Renamed governed response profile",
                "```",
                "response-patterns.md governed Caveman Lite",
            ),
            (
                "response_patterns",
                self.response_patterns,
                "### Legacy request-scoped brevity",
                "### Renamed legacy response brevity",
                "~~~",
                "response-patterns.md legacy request-scoped brevity",
            ),
            (
                "readme",
                self.readme,
                "## Governed Caveman Lite",
                "## Renamed governed README profile",
                "```",
                "README.md governed Caveman Lite",
            ),
            (
                "readme_cn",
                self.readme_cn,
                "## 治理精简模式",
                "## 重命名的治理精简模式",
                "~~~",
                "README_cn.md governed Caveman Lite",
            ),
        ):
            with self.subTest(artifact=artifact, heading=heading, fence=fence):
                mutated = replace_owned_heading_with_fenced_decoy(
                    text,
                    heading,
                    renamed_heading,
                    fence,
                )
                self.assertIn(f"{fence}markdown\n{heading}", mutated)
                with self.assertRaisesRegex(
                    AssertionError,
                    "found 0",
                ):
                    markdown_owned_section(mutated, heading)
                if artifact == "response_patterns":
                    token_budget = markdown_owned_section(
                        mutated,
                        "## Token budget control",
                    )
                    self.assertIn(
                        f"{fence}markdown\n{heading}",
                        token_budget,
                    )

                skill = mutated if artifact == "skill" else self.skill
                response_patterns = (
                    mutated
                    if artifact == "response_patterns"
                    else self.response_patterns
                )
                readme = mutated if artifact == "readme" else self.readme
                readme_cn = (
                    mutated if artifact == "readme_cn" else self.readme_cn
                )
                with self.assertRaisesRegex(
                    AssertionError,
                    re.escape(error_label),
                ):
                    self.validator.validate_governed_caveman_lite(
                        skill,
                        response_patterns,
                        readme,
                        readme_cn,
                    )

    def test_governed_caveman_lite_fallback_strips_yaml_inline_comments(self):
        prefix, _, body = self.skill.split("---", 2)
        inline_comment_frontmatter = (
            "\nname: openspec-superpower-change\n"
            "description: ordinary # OpenSpec 精简模式 OpenSpec 正常模式 "
            "caveman 风格摘要\n"
        )
        mutated = f"{prefix}---{inline_comment_frontmatter}---{body}"
        original_yaml = self.validator.yaml
        try:
            self.validator.yaml = None
            with self.assertRaisesRegex(AssertionError, "frontmatter"):
                self.validator.validate_governed_caveman_lite(
                    mutated,
                    self.response_patterns,
                    self.readme,
                    self.readme_cn,
                )
        finally:
            self.validator.yaml = original_yaml

    def test_governed_caveman_lite_fallback_rejects_malformed_quoted_frontmatter(
        self,
    ):
        prefix, _, body = self.skill.split("---", 2)
        malformed_descriptions = (
            (
                'description: "OpenSpec 精简模式 OpenSpec 正常模式 '
                "caveman 风格摘要"
            ),
            (
                "description: 'OpenSpec 精简模式 OpenSpec 正常模式 "
                "caveman 风格摘要"
            ),
            (
                r'description: "OpenSpec 精简模式 OpenSpec 正常模式 '
                r'caveman 风格摘要 \q"'
            ),
            (
                'description: "OpenSpec 精简模式 OpenSpec 正常模式 '
                'caveman 风格摘要" trailing'
            ),
        )
        original_yaml = self.validator.yaml
        yaml_implementations = [None]
        if original_yaml is not None:
            yaml_implementations.append(original_yaml)
        try:
            for yaml_implementation in yaml_implementations:
                self.validator.yaml = yaml_implementation
                for description in malformed_descriptions:
                    with self.subTest(
                        fallback=yaml_implementation is None,
                        description=description,
                    ):
                        frontmatter = (
                            "\nname: openspec-superpower-change\n"
                            f"{description}\n"
                        )
                        mutated = f"{prefix}---{frontmatter}---{body}"
                        with self.assertRaisesRegex(
                            AssertionError,
                            "frontmatter|invalid YAML",
                        ):
                            self.validator.validate_governed_caveman_lite(
                                mutated,
                                self.response_patterns,
                                self.readme,
                                self.readme_cn,
                            )
        finally:
            self.validator.yaml = original_yaml

    def test_governed_caveman_lite_scanner_ignores_comments_and_containers(self):
        scanner_fixture = """<!--
## HTML comment decoy
-->
- ```markdown
  ### List-fenced decoy
  ````
> ~~~
> ### Blockquote-fenced decoy
> ~~~~
> - ```markdown
>   ### Blockquote-list-fenced decoy
>   ````
- > ~~~
  > ### List-blockquote-fenced decoy
  > ~~~~
> 1. ```markdown
>    ### Blockquote-ordered-list-fenced decoy
>    ````
## Real owner
"""
        expected = ["## Real owner"]
        self.assertEqual(
            [item[0] for item in markdown_heading_spans(scanner_fixture)],
            expected,
        )
        self.assertEqual(
            [
                item[0]
                for item in self.validator._markdown_heading_spans(
                    scanner_fixture
                )
            ],
            expected,
        )

    def test_governed_caveman_lite_validator_rejects_fixed_owner_decoys(self):
        skill_heading = "## Governed Caveman Lite output mode"
        renamed_skill_heading = "## Renamed governed output mode"
        skill_decoy = (
            "<!--\n"
            f"{skill_heading}\n"
            + "\n".join(GOVERNED_CAVEMAN_LITE_SKILL_OBLIGATIONS)
            + "\n-->"
        )
        mutated_skill = self.skill.replace(
            skill_heading,
            renamed_skill_heading,
            1,
        ).replace(
            renamed_skill_heading,
            f"{renamed_skill_heading}\n\n{skill_decoy}",
            1,
        )
        with self.assertRaisesRegex(
            AssertionError,
            "SKILL.md governed Caveman Lite",
        ):
            self.validator.validate_governed_caveman_lite(
                mutated_skill,
                self.response_patterns,
                self.readme,
                self.readme_cn,
            )

        response_heading = "### Governed Caveman Lite"
        renamed_response_heading = "### Renamed governed response profile"
        response_decoy_lines = (
            (response_heading,)
            + GOVERNED_CAVEMAN_LITE_RESPONSE_OBLIGATIONS
        )
        response_decoy = (
            "- ```markdown\n"
            + "\n".join(f"  {line}" for line in response_decoy_lines)
            + "\n  ````"
        )
        mutated_response = self.response_patterns.replace(
            response_heading,
            renamed_response_heading,
            1,
        ).replace(
            renamed_response_heading,
            f"{renamed_response_heading}\n\n{response_decoy}",
            1,
        )
        self.assertIn(
            response_decoy,
            markdown_owned_section(
                mutated_response,
                "## Token budget control",
            ),
        )
        with self.assertRaisesRegex(
            AssertionError,
            "response-patterns.md governed Caveman Lite",
        ):
            self.validator.validate_governed_caveman_lite(
                self.skill,
                mutated_response,
                self.readme,
                self.readme_cn,
            )

        readme_heading = "## Governed Caveman Lite"
        renamed_readme_heading = "## Renamed governed README profile"
        readme_decoy = (
            "<!--\n"
            f"{readme_heading}\n"
            "OpenSpec 精简模式：<任务>\n"
            "OpenSpec 正常模式\n"
            "-->"
        )
        mutated_readme = self.readme.replace(
            readme_heading,
            renamed_readme_heading,
            1,
        ).replace(
            renamed_readme_heading,
            f"{renamed_readme_heading}\n\n{readme_decoy}",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "README.md"):
            self.validator.validate_governed_caveman_lite(
                self.skill,
                self.response_patterns,
                mutated_readme,
                self.readme_cn,
            )

        readme_cn_heading = "## 治理精简模式"
        renamed_readme_cn_heading = "## 重命名的治理精简模式"
        readme_cn_decoy = (
            "- ```markdown\n"
            f"  {readme_cn_heading}\n"
            "  OpenSpec 精简模式：<任务>\n"
            "  OpenSpec 正常模式\n"
            "  ````"
        )
        mutated_readme_cn = self.readme_cn.replace(
            readme_cn_heading,
            renamed_readme_cn_heading,
            1,
        ).replace(
            renamed_readme_cn_heading,
            f"{renamed_readme_cn_heading}\n\n{readme_cn_decoy}",
            1,
        )
        with self.assertRaisesRegex(AssertionError, "README_cn.md"):
            self.validator.validate_governed_caveman_lite(
                self.skill,
                self.response_patterns,
                self.readme,
                mutated_readme_cn,
            )

    def test_governed_caveman_lite_rejects_in_section_invisible_decoys(self):
        decoy_templates = (
            "<!--\n{needle}\n-->",
            "```text\n{needle}\n```",
            "- ```text\n  {needle}\n  ```",
            "> ~~~text\n> {needle}\n> ~~~",
            "> - ```text\n>   {needle}\n>   ```",
            "- > ~~~text\n  > {needle}\n  > ~~~",
            "10. Example:\n\n    ```text\n    {needle}\n    ```",
            "-   Example:\n\n    ~~~text\n    {needle}\n    ~~~",
            "    {needle}",
            "        {needle}",
            "\t{needle}",
            " \t{needle}",
            "- Rule:\n      {needle}",
            "10. Rule:\n        {needle}",
            "- Rule:\n  \t  {needle}",
        )
        owners = (
            (
                "skill",
                self.skill,
                "## Governed Caveman Lite output mode",
                "critical commands",
                "SKILL.md governed Caveman Lite",
            ),
            (
                "skill",
                self.skill,
                "## Legacy request-scoped output compatibility",
                "request-scoped compression",
                "SKILL.md legacy request-scoped brevity",
            ),
            (
                "response_patterns",
                self.response_patterns,
                "### Governed Caveman Lite",
                "critical commands",
                "response-patterns.md governed Caveman Lite",
            ),
            (
                "response_patterns",
                self.response_patterns,
                "### Legacy request-scoped brevity",
                "request-scoped compression",
                "response-patterns.md legacy request-scoped brevity",
            ),
            (
                "readme",
                self.readme,
                "## Governed Caveman Lite",
                "OpenSpec 正常模式",
                "README.md governed Caveman Lite",
            ),
            (
                "readme_cn",
                self.readme_cn,
                "## 治理精简模式",
                "OpenSpec 正常模式",
                "README_cn.md governed Caveman Lite",
            ),
        )
        for artifact, text, heading, needle, error_label in owners:
            for decoy_template in decoy_templates:
                decoy = decoy_template.format(needle=needle)
                with self.subTest(
                    artifact=artifact,
                    heading=heading,
                    decoy=decoy_template.splitlines()[0],
                ):
                    mutated = replace_owned_obligation_with_decoy(
                        text,
                        heading,
                        needle,
                        decoy,
                    )
                    skill = mutated if artifact == "skill" else self.skill
                    response_patterns = (
                        mutated
                        if artifact == "response_patterns"
                        else self.response_patterns
                    )
                    readme = mutated if artifact == "readme" else self.readme
                    readme_cn = (
                        mutated if artifact == "readme_cn" else self.readme_cn
                    )
                    with self.assertRaisesRegex(
                        AssertionError,
                        re.escape(error_label),
                    ):
                        self.validator.validate_governed_caveman_lite(
                            skill,
                            response_patterns,
                            readme,
                            readme_cn,
                        )

    def test_governed_caveman_lite_accepts_mixed_container_fenced_examples(
        self,
    ):
        examples = (
            "> - ```text\n>   harmless fenced example\n>   ```",
            "- > ~~~text\n  > harmless fenced example\n  > ~~~",
            (
                "10. Example:\n\n"
                "    ```text\n"
                "    harmless fenced example\n"
                "    ```"
            ),
            (
                "-   Example:\n\n"
                "    ~~~text\n"
                "    harmless fenced example\n"
                "    ~~~"
            ),
            "    harmless indented-code example",
            "\tharmless tab-indented-code example",
        )
        for example in examples:
            with self.subTest(example=example.splitlines()[0]):
                mutated = append_owned_fenced_example(
                    self.skill,
                    "## Governed Caveman Lite output mode",
                    example,
                )
                self.validator.validate_governed_caveman_lite(
                    mutated,
                    self.response_patterns,
                    self.readme,
                    self.readme_cn,
                )

    def test_governed_caveman_lite_accepts_visible_list_continuations(self):
        examples = (
            "- Rule:\n    critical commands",
            "10. Rule:\n    critical commands",
            "-   Rule:\n    critical commands",
            "> - Rule:\n>     critical commands",
            "- Rule:\n\tcritical commands",
            "10. Rule:\n\tcritical commands",
        )
        for example in examples:
            with self.subTest(example=example.splitlines()[0]):
                mutated = replace_owned_obligation_with_decoy(
                    self.skill,
                    "## Governed Caveman Lite output mode",
                    "critical commands",
                    example,
                )
                self.validator.validate_governed_caveman_lite(
                    mutated,
                    self.response_patterns,
                    self.readme,
                    self.readme_cn,
                )

    def test_description_does_not_claim_brief_or_external_batch_work(self):
        description = self.skill.split("---", 2)[1]
        self.assertNotIn("task or step breakdowns", description)
        self.assertNotIn("external-agent handoff", description)
        self.assertIn("modify files or behavior", description)

    def test_description_routes_explicit_archive_and_distill_requests(self):
        description = self.skill.split("---", 2)[1]
        self.assertIn("archive and distill", description)
        self.assertIn("Project Learning Closeout", description)
        self.assertIn("归档并蒸馏", description)

    def test_review_and_fix_is_not_review_only(self):
        self.assertIn("Review and fix", self.request_modes)
        self.assertIn("not Review-only", self.request_modes)

    def test_backend_architecture_review_route_is_explicit_and_narrow(self):
        normalized = " ".join(self.skill.split())
        for phrase in (
            "`backend-architecture-review`",
            "explicit backend architecture Review",
            "architecture/design, performance/stability, service/module boundaries, "
            "API/call chain/transaction boundaries, or over-design",
            "Review 一下这个 Bugfix 的 Diff",
            "Review 当前 Plan",
            "does not select the specialist",
            "read-only specialist evidence",
            "ordinary Review remains unchanged",
            "Gate, OpenSpec, Handoff, Evidence, PASS/FAIL/BLOCKED, Completion, "
            "and authority remain with this Router",
        ):
            self.assertIn(phrase, normalized)

    def test_non_backend_architecture_review_stays_router_review_only(self):
        normalized = " ".join(self.skill.split())
        for phrase in (
            "Other architecture Review",
            "Other architecture Review, OpenSpec need, implementation authorization, "
            "or whole-task completion evidence | This skill / Review-only",
            "Review-and-fix remains state-changing Router work",
        ):
            self.assertIn(phrase, normalized)
        self.assertNotIn(
            "Other architecture Review, OpenSpec need, implementation authorization, "
            "or whole-task completion evidence | `backend-architecture-review`",
            normalized,
        )

    def test_authorized_execution_continuity_reuses_canonical_state(self):
        normalized = " ".join(self.approved.split())
        for phrase in (
            "## Authorized Execution Continuity",
            "approved tasks remain Pending, no Blocker exists, and no new human "
            "decision is required",
            "continue with the next approved task",
            "Completing a subtask is not a stop condition",
            "must not trigger a continue prompt",
            "all approved tasks are complete",
            "state is `BLOCKED`",
            "new product, business, or architecture decision",
            "permission, credentials, or required resources",
            "high-risk, irreversible, or outside the approved scope",
            "user explicitly pauses or cancels",
            "Context Compaction, session recovery, a model or agent switch, or `继续`",
            "canonical Plan, Status, Handoff, or equivalent state",
            "goal, current task, Pending tasks, Blocker, Acceptance, and Verification",
            "Do not infer the next action from the previous chat response",
            "Do not create `.agent/goal.md`, a Task Manager, or a second state system",
            "at least one task-related action",
            "A summary, recommendation, or future plan alone is not progress",
            "Code written is progress, not Done",
            "Acceptance, Test, Build, Verification, and Evidence",
            "references/completion-contract.md",
            "OpenSpec-backed work uses `openspec/changes/<change-id>/tasks.md` to "
            "track contract progress",
            "Direct Change reuses existing scoped Plan/Status/Handoff/equivalent "
            "state for continuity",
            "does not require OpenSpec tasks.md",
            "Continuity must not create a new OpenSpec change or second ledger",
            "No global rule requires every work item to have OpenSpec tasks.md",
            "Plan checkboxes are static execution steps only",
            "never canonical task state",
        ):
            self.assertIn(phrase, normalized)

    def test_plan_checkboxes_are_static_and_tasks_are_canonical(self):
        plan = (
            ROOT / "docs" / "superpowers" / "plans" /
            "2026-08-25-backend-architecture-review-continuity.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(plan.split())
        self.assertIn("Checkboxes are static executable steps only.", normalized)
        self.assertIn(
            "For this change, canonical progress is read only from active "
            "OpenSpec tasks.md.",
            normalized,
        )
        self.assertIn(
            "Never infer pending work from an unchecked Plan step.",
            normalized,
        )
        self.assertNotIn("for tracking", normalized.lower())

    def test_material_complexity_checkpoint_is_conditional_and_ordered(self):
        normalized = " ".join(self.approved.split())
        heading = "## Conditional Minimal Implementation"
        self.assertIn(heading, normalized)
        trigger = (
            "only when a proposed implementation or Review fix would materially "
            "add an abstraction, component, layer, dependency, or wider scope"
        )
        self.assertIn(trigger, normalized)
        order = (
            "Need",
            "Repository Reuse",
            "Stdlib",
            "Platform Native",
            "Existing Dependency",
            "Small Local Implementation",
            "New Abstraction",
        )
        positions = [normalized.index(item, normalized.index(heading)) for item in order]
        self.assertEqual(positions, sorted(positions))
        for phrase in (
            "choose the first adequate option",
            "does not run for every ordinary Bugfix",
            "no mandatory checklist, artifact, gate, or output",
            "does not automatically select `backend-architecture-review`",
        ):
            self.assertIn(phrase, normalized)

    def test_review_fix_nonconvergence_blocks_scope_growth(self):
        approved = " ".join(self.approved.split())
        skill = " ".join(self.skill.split())
        for phrase in (
            "## Review/Fix Convergence",
            "same finding recurs after a verified fix",
            "fix-induced regression recurs",
            "multiple Review rounds do not converge",
            "reviewers materially conflict on the core approach",
            "architecture or requirements boundary",
            "fix scope keeps expanding",
            "abstraction, layer, component, or dependency",
            "stop before another widening fix",
            "return `BLOCKED` to `control-plane-high`",
            "blocker owner and resume condition",
            "Do not create an `ESCALATED` state",
            "Ordinary first-pass findings continue through the existing same-scope loop",
        ):
            self.assertIn(phrase, approved)
        self.assertIn(
            "Non-converging Review/Fix retries are not an unlimited automatic fix loop",
            skill,
        )
        self.assertIn("Review FAIL -> Fix same scope -> Verify -> Review again", skill)

    def test_direct_change_uses_risk_appropriate_evidence_profile_everywhere(self):
        direct = (ROOT / "references" / "direct-change-rule.md").read_text(encoding="utf-8")
        responses = (ROOT / "references" / "response-patterns.md").read_text(encoding="utf-8")
        for text in (self.request_modes, direct, responses):
            self.assertIn("public/API restoration", text)
            self.assertIn("strict", text)
        self.assertIn("Low-risk Direct Change", responses)
        self.assertIn("compact", responses)
        self.assertNotIn("Use compact Step Evidence Gate", direct)
        self.assertIn("Use the profile-appropriate Step Evidence Gate", direct)

    def test_openspec_and_superpowers_do_not_duplicate_design_approval(self):
        self.assertIn("single design approval", self.approved)
        self.assertIn("does not require a duplicate", self.approved)

    def test_compact_direct_change_uses_inline_fast_path(self):
        owners = {
            "direct": " ".join((ROOT / "references" / "direct-change-rule.md").read_text(encoding="utf-8").split()),
            "evidence": " ".join((ROOT / "references" / "step-evidence-gate.md").read_text(encoding="utf-8").split()),
            "skill": " ".join(self.skill.split()),
            "approved": " ".join(self.approved.split()),
            "requests": " ".join(self.request_modes.split()),
        }
        for phrase in (
            "inline readiness check",
            "does not create a standalone Brief, Plan, or Preflight artifact",
        ):
            self.assertIn(phrase, owners["direct"])
        self.assertIn("one short Plan, no duplicate Brief, and one initial Preflight", owners["skill"])
        self.assertIn("one `FULL_PREFLIGHT` plus at most one terminal `FOCUSED_RECHECK`", owners["approved"])
        self.assertIn("must not reopen Preflight", owners["approved"])
        self.assertIn("test-spec and test-quality concerns", owners["approved"])
        self.assertIn("one post-verification complete-diff Review may satisfy both Implementation Review and Final Review", owners["evidence"])
        self.assertIn("one regression per distinct changed behavior or failure mechanism", owners["skill"])
        self.assertIn("strong reasoning capability makes inline execution preferable", owners["skill"])
        self.assertIn("one initial Preflight", owners["requests"])
        self.assertIn("Only compact low-risk Direct Change may keep readiness inline", owners["requests"])
        self.assertNotIn("Do not create OpenSpec artifacts or Superpowers plans unless", owners["direct"])
        self.assertNotIn("Adjudication may permit one terminal focused recheck", owners["approved"])

    def test_strict_security_recovery_preserves_full_gates(self):
        completion = " ".join(self.completion.split())
        self_evolution = " ".join(
            (ROOT / "references" / "self-evolution-rule.md")
            .read_text(encoding="utf-8")
            .split()
        )
        for phrase in (
            "strict, external, multi-slice, and protected-boundary work",
            "separate Implementation Review and Final Review",
            "security, recovery, integrity/data-loss, authority, and false-PASS",
        ):
            self.assertIn(phrase, self_evolution)
            self.assertIn(phrase.lower(), completion.lower())
        self.assertIn("OpenSpec approval", self_evolution)
        self.assertIn("verification-before-completion", completion)
        self.assertIn("learning audit after implementation verification", completion)
        self.assertIn("combined eligibility and requires the normal separate Reviews", completion)
        self.assertIn("learning audit after implementation verification", " ".join(self.skill.split()))
        self.assertIn("learning audit after implementation verification", " ".join(self.request_modes.split()))

    def test_evidence_gate_operates_on_slices_not_micro_steps(self):
        self.assertIn("business slice", self.approved)
        self.assertIn("not every TDD micro-step", self.approved)

    def test_inline_step_evidence_stays_handoff_free(self):
        inline = (ROOT / "templates" / "evidence-template.md").read_text(encoding="utf-8")
        final = (ROOT / "templates" / "final-verification-template.md").read_text(encoding="utf-8")
        self.assertNotIn("COOP_EVIDENCE_MANIFEST_START", inline)
        self.assertIn("evidence_role: final-verification", final)

    def test_inline_implementation_requires_review(self):
        self.assertIn("inline implementation", self.approved)
        self.assertIn("Review PASS", self.approved)

    def test_completion_contract_is_canonical_and_discoverable(self):
        path = ROOT / "references" / "completion-contract.md"
        self.assertTrue(path.is_file(), "canonical completion contract missing")
        completion = path.read_text(encoding="utf-8")
        normalized = " ".join(completion.split())
        for heading in (
            "## Success", "## Evidence", "## Stop conditions",
            "## Learning and reconciliation", "## Cross-CLI sync",
            "## Git and publication authority", "## Residual risk",
        ):
            self.assertIn(heading, completion)
        for obligation in (
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
            self.assertIn(obligation, normalized)
        self.assertIn(
            "Run Project Learning Closeout after implementation Review PASS "
            "and before fresh final verification",
            normalized,
        )
        self.assertNotIn(
            "Run Project Learning Closeout after implementation Review PASS when",
            normalized,
        )
        self.assertIn("references/completion-contract.md", self.skill)

    def test_secondary_completion_surfaces_reference_canonical_contract(self):
        for relative in (
            "references/response-patterns.md",
            "references/approved-implementation-workflow.md",
            "references/step-evidence-gate.md",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("references/completion-contract.md", text, relative)
        evidence = (ROOT / "references" / "step-evidence-gate.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("business slice", evidence)
        self.assertIn("batch Review", evidence)
        skill_closure = self.skill.split("## Implementation And Closure", 1)[1].split(
            "## Capability And Evidence Profiles", 1
        )[0]
        approved_final = self.approved.split("## Final Completion", 1)[1].split(
            "## Tiered Authorization And High Review", 1
        )[0]
        self.assertNotIn("run Project Learning Closeout", skill_closure)
        self.assertNotIn("persist fresh `final_critical`", approved_final)
        self.assertNotIn("--previous-status", approved_final)
        self.assertNotIn("superpowers:verification-before-completion", approved_final)
        self.assertNotIn("Completion claim allowed", evidence)
        self.assertIn("whole-task decision is deferred", evidence)

    def test_phase_aware_superpowers_activation_precedes_broad_metadata(self):
        normalized_skill = " ".join(self.skill.split())
        normalized_adapter = " ".join(self.superpowers_adapter.split())
        normalized_governance = " ".join(self.shared_governance.split())
        self.assertIn("Phase-Aware Superpowers Activation", self.skill)
        self.assertIn(
            "Generic create/modify wording does not activate a Superpowers "
            "sub-skill by itself.",
            normalized_skill,
        )
        self.assertIn(
            "Generic create/modify wording does not activate a sub-skill by itself.",
            normalized_adapter,
        )
        expected_ccg_014 = (
            "[CCG-014] Governed state-changing, Git-mutating, or whole-task-completion "
            "work enters `openspec-superpower-change` Gate 0 through exactly one applicable "
            "Router before broad Superpowers metadata or any user-explicit "
            "`$superpowers:*` method proceeds. Generic create/modify wording alone does not "
            "activate a sub-skill; a user-explicit method request grants no independent "
            "workflow, business, Git, or completion authority; inability to load exactly "
            "one applicable Router is `BLOCKED`; once selected, each sub-skill's full rules "
            "remain in force."
        )
        self.assertIn(expected_ccg_014, normalized_governance)

    def test_superpowers_method_routing_is_exact_and_fail_closed(self):
        normalized = " ".join(
            (self.request_modes + "\n" + self.superpowers_adapter).split()
        )
        for required in (
            "Ordinary questions bypass the Router and the `using-superpowers` meta-entry",
            "Diagnose-only work remains read-only",
            "Router records Superpowers `none`",
            "user-explicit `$superpowers:*` request chooses a method only",
            "Router-required child Skills remain eligible for native implicit matching",
            "return to Router classification",
            "Each phase and Skill may be selected at most once",
            "cannot load exactly one applicable Router",
            "`BLOCKED`",
        ):
            self.assertIn(required, normalized)

        cases_path = ROOT / "tests" / "fixtures" / "superpowers-routing-cases.json"
        schema_path = (
            ROOT / "tests" / "fixtures" / "superpowers-routing-output.schema.json"
        )
        runner_path = ROOT / "tests" / "run_superpowers_routing_forward_tests.py"
        cases = json.loads(cases_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(
            {case["id"] for case in cases},
            {
                "ordinary_question",
                "diagnose_only",
                "proposal_only",
                "material_ambiguity",
                "direct_change",
                "ordinary_review",
                "architecture_review",
                "high_risk_implementation",
                "whole_task_completion",
                "explicit_method_no_git",
                "missing_router",
                "duplicate_router",
                "cyclic_phase",
            },
        )
        expected_keys = {
            "route",
            "result",
            "selected_superpowers",
            "state_change_allowed",
            "git_authorized",
            "completion_owner",
        }
        self.assertEqual(set(schema["required"]), expected_keys)
        self.assertEqual(set(schema["properties"]), expected_keys)
        self.assertIs(
            schema["properties"]["selected_superpowers"]["uniqueItems"], True
        )
        self.assertIn(
            "record a requested method even when authority blocks it",
            schema["properties"]["selected_superpowers"]["description"],
        )
        self.assertIn(
            "exactly one applicable Router owns the route",
            schema["properties"]["completion_owner"]["description"],
        )
        runner = runner_path.read_text(encoding="utf-8")
        self.assertIn("build_runtime_schema", runner)
        self.assertIn('router_source / "references" / "superpowers-adapter.md"', runner)
        self.assertIn('adapter_hash = sha256(target)', runner)
        self.assertIn(
            "selected_superpowers must include every canonical method selected or "
            "explicitly requested, even when authority blocks the route",
            runner,
        )
        self.assertIn('selected_schema.pop("uniqueItems")', runner)
        self.assertIn('restored_selected["uniqueItems"] = True', runner)
        normalized_adapter = " ".join(self.superpowers_adapter.split())
        self.assertIn("Route Decision Record", self.superpowers_adapter)
        for case in cases:
            expected = case["expected"]
            selected = json.dumps(
                expected["selected_superpowers"], separators=(",", ":")
            )
            record = (
                f"| `{case['id']}` | `{expected['route']}` | `{expected['result']}` | "
                f"`{selected}` | `{str(expected['state_change_allowed']).lower()}` | "
                f"`{str(expected['git_authorized']).lower()}` | "
                f"`{expected['completion_owner']}` |"
            )
            self.assertIn(" ".join(record.split()), normalized_adapter)
        self.assertIn("case_public = {key: value for key, value in case.items() if key != \"expected\"}", runner)
        self.assertIn("expected = case[\"expected\"]", runner)
        command_slice = runner.split("command = [", 1)[1].split("]", 1)[0]
        prompt_slice = runner.split("prompt =", 1)[1].split("command = [", 1)[0]
        self.assertNotIn("expected", command_slice)
        self.assertNotIn("expected", prompt_slice)

    def test_routing_forward_runner_rejects_marker_perfect_tool_fallback(self):
        runner = load_routing_runner()
        parser = getattr(runner, "parse_event_trace", None)
        self.assertTrue(callable(parser), "JSONL event parser is required")
        trace = "\n".join(
            (
                json.dumps({"type": "thread.started", "thread_id": "redacted"}),
                json.dumps({"type": "turn.started"}),
                json.dumps(
                    {
                        "type": "item.completed",
                        "item": {
                            "id": "redacted",
                            "type": "command_execution",
                            "command": "redacted",
                            "aggregated_output": "CHILD_NATIVE_MARKER_7F3A91",
                            "exit_code": 0,
                            "status": "completed",
                        },
                    }
                ),
                json.dumps(
                    {
                        "type": "item.completed",
                        "item": {
                            "id": "redacted",
                            "type": "agent_message",
                            "text": "CHILD_NATIVE_MARKER_7F3A91",
                        },
                    }
                ),
                json.dumps({"type": "turn.completed", "usage": {}}),
            )
        )
        with self.assertRaisesRegex(runner.ProbeFailure, "tool|command"):
            parser(trace)

    def test_routing_forward_runner_rejects_nested_source_symlink(self):
        runner = load_routing_runner()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            destination = root / "destination"
            outside = root / "outside.txt"
            source.mkdir()
            outside.write_text("outside\n", encoding="utf-8")
            (source / "nested-link").symlink_to(outside)
            with self.assertRaisesRegex(runner.ProbeFailure, "symlink"):
                runner.copy_tree(source, destination)
            self.assertFalse(destination.exists())

    def test_routing_forward_runner_closes_registration_interrupt_race(self):
        runner = load_routing_runner()
        register = getattr(runner, "register_active_process", None)
        self.assertTrue(callable(register), "race-safe process registration is required")
        process = mock.Mock(pid=424242)
        runner.INTERRUPTED.set()
        try:
            with mock.patch.object(runner, "terminate_process_group") as terminate:
                with self.assertRaisesRegex(runner.ProbeFailure, "interrupted"):
                    register(process)
                terminate.assert_called_once_with(process)
            self.assertNotIn(process.pid, runner.ACTIVE_PROCESSES)
            with mock.patch.object(runner, "terminate_all_children") as terminate_all:
                runner.handle_interruption(15, None)
                runner.handle_interruption(15, None)
                self.assertEqual(terminate_all.call_count, 2)
        finally:
            runner.INTERRUPTED.clear()

    def test_proposal_only_can_select_no_superpowers_subskill(self):
        normalized_skill = " ".join(self.skill.split())
        normalized = " ".join(self.proposal_workflow.split())
        normalized_adapter = " ".join(self.superpowers_adapter.split())
        normalized_request_modes = " ".join(self.request_modes.split())
        self.assertIn("proposal-only", normalized)
        self.assertIn("no implementation sub-skill", normalized)
        self.assertIn(
            "Public API implementation remains `strict`; its proposal-only draft "
            "does not automatically load implementation planning, TDD, or code Review.",
            normalized_request_modes,
        )
        self.assertIn(
            "Gate 0 loads no implementation sub-skill for proposal drafting. A "
            "material unresolved choice requires brainstorming.",
            normalized_request_modes,
        )
        self.assertIn(
            "A bounded assumption is allowed only when it is reversible at approval "
            "time, explicit in proposal/design, and does not decide security, "
            "compatibility, destructive migration, data lifecycle, production "
            "authority, or testable acceptance.",
            normalized,
        )
        self.assertIn(
            "A material unresolved choice affecting scope, security, compatibility, "
            "data lifecycle, production authority, or testable acceptance requires "
            "`superpowers:brainstorming`.",
            normalized,
        )
        self.assertIn(
            "A request to choose for the user does not resolve a material choice; "
            "invoke brainstorming and obtain acceptance before artifact finalization.",
            normalized_skill,
        )
        self.assertIn(
            "User delegation to choose an excluded boundary does not make it a "
            "bounded assumption; invoke brainstorming and obtain user acceptance "
            "before finalizing artifacts.",
            normalized,
        )
        self.assertIn(
            "Once a sub-skill is selected, follow it completely; selective "
            "invocation never weakens its HARD-GATE or discipline.",
            normalized_adapter,
        )

    def test_prompt_collision_scenario_catalog_covers_phase_git_and_hard_gate(self):
        path = ROOT / "tests" / "fixtures" / "prompt-collision-cases.json"
        self.assertTrue(path.is_file(), "prompt-collision fixture missing")
        cases = {case["id"]: case for case in json.loads(path.read_text(encoding="utf-8"))}
        expected_ids = {
            "proposal_only", "material_choice", "unauthorized_git",
            "authorized_git", "selected_hard_gate",
        }
        self.assertEqual(set(cases), expected_ids)
        for case in cases.values():
            self.assertTrue(case["prompt"].strip())
            self.assertTrue(case["observable"].strip())
            self.assertNotIn("expected", case)
        normalized = " ".join((self.skill + self.superpowers_adapter).split())
        self.assertIn("never grants Git permission", normalized)
        self.assertIn("current user explicitly authorizes", normalized)
        self.assertIn("no implementation sub-skill", " ".join(self.proposal_workflow.split()))
        self.assertIn("HARD-GATE", normalized)

    def test_model_identity_never_selects_workflow_weight(self):
        normalized_skill = " ".join(self.skill.split())
        normalized_adapter = " ".join(self.superpowers_adapter.split())
        normalized_capability_routing = " ".join(
            self.agent_capability_routing.split()
        )
        self.assertIn(
            "Model identity or version does not grant approval and does not select "
            "workflow weight.",
            normalized_skill,
        )
        self.assertIn(
            "Concrete model identity does not grant authority or choose workflow weight.",
            normalized_adapter,
        )
        self.assertIn(
            "Capability profiles are stable routing and authority ceilings. They are "
            "not model names, vendor tiers, security identities, or evidence of approval.",
            normalized_capability_routing,
        )
        self.assertIn(
            "Optional model metadata is observational only and MUST NOT influence "
            "validation, routing, or approval.",
            normalized_capability_routing,
        )

    def test_domain_context_check_is_conditional_and_precedes_material_choice(self):
        normalized = " ".join((self.skill + self.request_modes).split())
        self.assertIn("Domain Context Check", normalized)
        self.assertIn("before material", normalized)
        self.assertIn("does not invoke `grill-with-docs`", normalized)
        self.assertIn("complete portable Discovery First", normalized)
        self.assertIn("references/local-instruction-checkpoint.md", self.skill)

    def test_ignored_canonical_context_cannot_satisfy_shared_promotion(self):
        normalized = " ".join(self.local_checkpoint.split())
        self.assertIn("must not be intentionally ignored", normalized)
        self.assertIn(
            "does not require `git add`, commit, or push", normalized
        )

    def test_project_learning_gate_has_automatic_and_explicit_triggers(self):
        path = ROOT / "references" / "project-learning-closeout.md"
        self.assertTrue(path.is_file(), "project learning closeout reference missing")
        learning_closeout = path.read_text(encoding="utf-8")
        normalized = " ".join((self.learning + learning_closeout).split())
        self.assertIn("two independent correction or Review signals", normalized)
        self.assertIn("security, integrity, data-loss, or false-PASS", normalized)
        self.assertIn("archive and distill", normalized)
        self.assertIn("every confirmed project-local key point", normalized)
        self.assertIn("single low-risk task-local correction", normalized)
        self.assertIn("without creating durable documentation noise", normalized)

    def test_required_project_learning_blocks_completion_and_archive(self):
        path = ROOT / "references" / "project-learning-closeout.md"
        self.assertTrue(path.is_file(), "project learning closeout reference missing")
        learning_closeout = path.read_text(encoding="utf-8")
        normalized = " ".join(
            (self.skill + self.approved + learning_closeout).split()
        )
        self.assertIn("Project Learning Closeout", normalized)
        self.assertIn("final completion is `BLOCKED`", normalized)
        self.assertIn("before fresh final verification", normalized)
        self.assertIn("before OpenSpec", normalized)

    def test_learning_artifacts_are_layered_and_mechanical_rules_are_executable(self):
        closeout_path = ROOT / "references" / "project-learning-closeout.md"
        template_path = ROOT / "templates" / "learning-candidate-template.md"
        self.assertTrue(
            closeout_path.is_file(), "project learning closeout reference missing"
        )
        self.assertTrue(
            template_path.is_file(), "learning candidate template missing"
        )
        learning_closeout = closeout_path.read_text(encoding="utf-8")
        learning_template = template_path.read_text(encoding="utf-8")
        normalized = " ".join((learning_closeout + learning_template).split())
        self.assertIn("CONTEXT.md", normalized)
        self.assertIn("docs/engineering-invariants.md", normalized)
        self.assertIn("deterministic regression test or validator", normalized)
        self.assertIn("prose-only", normalized)
        self.assertIn("sensitive", normalized)

    def test_project_learning_validator_binds_rules_to_owned_artifacts(self):
        closeout = (
            ROOT / "references" / "project-learning-closeout.md"
        ).read_text(encoding="utf-8")
        template = (
            ROOT / "templates" / "learning-candidate-template.md"
        ).read_text(encoding="utf-8")
        self.validator.validate_project_learning_gate(
            self.skill, self.approved, self.completion, closeout, template
        )

        relocated_closeout = "# Project Learning Closeout\n\nPlaceholder.\n"
        with self.assertRaisesRegex(AssertionError, "project-learning-closeout"):
            self.validator.validate_project_learning_gate(
                self.skill,
                self.approved,
                self.completion,
                relocated_closeout,
                template + "\n" + closeout,
            )

        relocated_template = "# Learning Candidate Card\n\nPlaceholder.\n"
        with self.assertRaisesRegex(AssertionError, "learning-candidate-template"):
            self.validator.validate_project_learning_gate(
                self.skill,
                self.approved,
                self.completion,
                closeout + "\n" + template,
                relocated_template,
            )

    def test_project_learning_guidance_is_discoverable_from_project_instructions(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        invariants_path = ROOT / "docs" / "engineering-invariants.md"
        self.assertTrue(invariants_path.is_file(), "engineering invariants missing")
        invariants = invariants_path.read_text(encoding="utf-8")
        normalized = " ".join(invariants.split())
        self.assertIn("docs/engineering-invariants.md", agents)
        self.assertIn("references/project-learning-closeout.md", agents)
        self.assertIn("entry-discoverable and artifact-bound", normalized)
        self.assertIn("deterministic negative regression", normalized)

    def test_hashed_review_lineage_parses_exact_verified_bytes(self):
        invariants = (ROOT / "docs" / "engineering-invariants.md").read_text(
            encoding="utf-8"
        )
        normalized = " ".join(invariants.split()).lower()
        for required in (
            "hashed review lineage must parse the exact verified artifact bytes",
            "exact bytes whose whole-file sha-256 was verified",
            "replacement between checks",
            "intermediate-directory escape",
            "single-descriptor hash/parse binding",
            "reviewer replacement or identity reuse",
        ):
            with self.subTest(required=required):
                self.assertIn(required, normalized)

    def test_external_cli_debug_traces_are_temporary_and_not_durable(self):
        invariants = (ROOT / "docs" / "engineering-invariants.md").read_text(
            encoding="utf-8"
        )
        normalized = " ".join(invariants.split()).lower()
        for required in (
            "external cli debug traces",
            "temporary evidence",
            "mode `0600`",
            "must not be quoted or echoed",
            "remove the raw trace after final gates",
        ):
            with self.subTest(required=required):
                self.assertIn(required, normalized)

        durable_roots = (
            ROOT / "docs",
            ROOT / "openspec",
            ROOT / "references",
        )
        raw_traces = sorted(
            str(path.relative_to(ROOT))
            for durable_root in durable_roots
            for path in durable_root.rglob("*")
            if path.is_file()
            and (
                path.name.endswith(".debug.log")
                or path.name.endswith(".debug.jsonl")
            )
        )
        self.assertEqual([], raw_traces, "raw external CLI traces became durable")

    def test_behavioral_forward_proofs_fail_closed_on_tool_events(self):
        invariants = (ROOT / "docs" / "engineering-invariants.md").read_text(
            encoding="utf-8"
        )
        normalized = " ".join(invariants.split()).lower()
        for required in (
            "behavioral proof must audit the native event stream",
            "read-only sandbox and an unchanged file snapshot",
            "marker-perfect",
            "tool, command, file, or mcp event",
            "fail closed",
        ):
            with self.subTest(required=required):
                self.assertIn(required, normalized)

        runner = (
            ROOT / "tests" / "run_superpowers_routing_forward_tests.py"
        ).read_text(encoding="utf-8")
        self.assertIn("def parse_event_trace", runner)
        self.assertIn("tool or command event is forbidden", runner)

    def test_reviewed_runtime_sync_binds_destination_prestate(self):
        invariants = (ROOT / "docs" / "engineering-invariants.md").read_text(
            encoding="utf-8"
        )
        normalized = " ".join(invariants.split()).lower()
        for required in (
            "reviewed runtime plan binds destination pre-state",
            "source hashes alone",
            "hash, mode, or absence",
            "immediately before any backup or write",
            "pre-state drift",
            "restore the reviewed hash, mode, or absence",
        ):
            with self.subTest(required=required):
                self.assertIn(required, normalized)

        sync_validator = (
            ROOT / "scripts" / "validate_cross_cli_sync.py"
        ).read_text(encoding="utf-8")
        self.assertIn("def capture_destination_prestate", sync_validator)
        self.assertIn("def assert_destination_prestate", sync_validator)
        self.assertIn("def _assert_target_prestate", sync_validator)

    def test_qagent_fixture_separates_semantics_mechanism_and_regression(self):
        fixture = (
            ROOT
            / "tests"
            / "fixtures"
            / "project-learning"
            / "qagent-merged-paragraph.md"
        ).read_text(encoding="utf-8")
        self.assertIn("table-level annotation, not tabular data", fixture)
        self.assertIn("engineering invariant", fixture)
        self.assertIn("mechanical regression", fixture)

    def test_handoff_schema_has_closure_fields(self):
        for expected in (
            "schema_version: 6",
            "lifecycle_state:",
            "attempt:",
            "attempt_report_artifact:",
            "last_review_result:",
            "last_review_artifact:",
            "blocker_owner:",
            "resume_condition:",
            "final_verification:",
            "final_verification_artifact:",
            "final_review_result:",
            "final_review_artifact:",
        ):
            self.assertIn(expected, self.handoff)

    def test_complete_contract_requires_review_and_final_verification(self):
        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        data.update(
            lifecycle_state="complete",
            last_review_result="fail",
            final_verification="pending",
            final_review_result="pending",
            next_owner="user",
        )
        with self.assertRaisesRegex(AssertionError, "complete"):
            self.validator.validate_handoff_contract(data, "invalid-complete")

    def test_schema4_requires_bound_agent_identities_and_codex_decision_owner(self):
        data = schema4_contract(self.validator, self.handoff)
        self.validator.validate_legacy_handoff_contract(data, "schema4-identities")
        self.assertEqual(self.validator.LEGACY_SCHEMA_VERSION, 4)
        for field in (
            "executor_agent", "independent_reviewer_agent", "decision_owner",
        ):
            self.assertIn(field, self.validator.LEGACY_IMMUTABLE_FIELDS)

        for field, value in (
            ("executor_agent", "agy"),
            ("independent_reviewer_agent", "grok"),
            ("decision_owner", "antigravity-cli"),
        ):
            invalid = dict(data)
            invalid[field] = value
            with self.subTest(field=field, value=value):
                with self.assertRaisesRegex(AssertionError, "agent|identity|decision_owner"):
                    self.validator.validate_legacy_handoff_contract(invalid, "invalid-identity")

    def test_standard_and_strict_require_a_distinct_reviewer(self):
        self.assertEqual(self.validator.LEGACY_SCHEMA_VERSION, 4)
        for profile in ("standard", "strict"):
            same_agent = schema4_contract(
                self.validator, self.handoff, risk_profile=profile,
                independent_reviewer_agent="antigravity-cli",
            )
            with self.subTest(profile=profile, case="self-review"):
                with self.assertRaisesRegex(AssertionError, "reviewer|distinct|self-review"):
                    self.validator.validate_legacy_handoff_contract(same_agent, "self-review")

            no_reviewer = schema4_contract(
                self.validator, self.handoff, risk_profile=profile,
                independent_reviewer_agent="not-applicable",
                independent_review_not_applicable_reason="reviewed inline",
            )
            with self.subTest(profile=profile, case="not-applicable"):
                with self.assertRaisesRegex(AssertionError, "reviewer|not-applicable|compact"):
                    self.validator.validate_legacy_handoff_contract(no_reviewer, "missing-reviewer")

    def test_compact_not_applicable_reviewer_requires_a_reason(self):
        valid = schema4_contract(
            self.validator, self.handoff, risk_profile="compact",
            independent_reviewer_agent="not-applicable",
            independent_review_not_applicable_reason="Codex performs the inline Review",
        )
        self.validator.validate_legacy_handoff_contract(valid, "compact-inline-review")

        for reason in (None, "", "   "):
            invalid = dict(valid)
            invalid["independent_review_not_applicable_reason"] = reason
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(AssertionError, "reason|non-blank"):
                    self.validator.validate_legacy_handoff_contract(invalid, "missing-na-reason")

        concrete = schema4_contract(
            self.validator, self.handoff, risk_profile="compact",
            independent_review_not_applicable_reason="must be null",
        )
        with self.assertRaisesRegex(AssertionError, "reason|not-applicable|null"):
            self.validator.validate_legacy_handoff_contract(concrete, "unexpected-na-reason")

    def test_role_first_review_routing_wording_is_explicit(self):
        example = (
            "Review purpose: inspect the current implementation plan and decide PASS or "
            "BLOCKED; reviewer product: codex; role: independent-reviewer; capability: "
            "control-plane-high; independence: a user-opened new-window instance distinct "
            "from the plan author and executor; authority: governed Review evidence only."
        )
        self.assertIn(example, self.response_patterns)
        capability = (
            ROOT / "references" / "agent-capability-routing.md"
        ).read_text(encoding="utf-8")
        normalized_capability = " ".join(capability.split())
        for product in ("codex", "pi", "antigravity-cli", "grok-cli"):
            self.assertIn(product, capability)
        self.assertIn(
            "Only a bound `codex` product with role `control-plane` and profile "
            "`control-plane-high`",
            normalized_capability,
        )
        for phrase in (
            "canonical assignment",
            "explicitly selected by the user",
            "one concrete eligible product",
            "another agent",
            "independent agent",
            "another model",
            "BLOCKED",
        ):
            self.assertIn(phrase, self.response_patterns)

    def test_role_first_router_surfaces_bind_six_review_concepts(self):
        surfaces = (
            "SKILL.md",
            "references/request-modes.md",
            "references/response-patterns.md",
            "references/approved-implementation-workflow.md",
            "references/step-evidence-gate.md",
            "references/superpowers-adapter.md",
            "references/completion-contract.md",
        )
        required = (
            "Review purpose",
            "reviewer product",
            "role",
            "capability",
            "independence",
            "authority",
        )
        for relative in surfaces:
            text = (ROOT / relative).read_text(encoding="utf-8")
            normalized = " ".join(text.split())
            with self.subTest(surface=relative):
                for field in required:
                    self.assertIn(field, normalized)
                self.assertIn("schema 6", normalized)

    def test_role_first_review_kind_matrix_is_explicit_and_shared(self):
        companion_skill = (
            ROOT.parent / "codex-brief-antigravity-review" / "SKILL.md"
        )
        surfaces = (
            ROOT / "SKILL.md",
            ROOT / "references" / "agent-capability-routing.md",
            ROOT / "references" / "response-patterns.md",
            companion_skill,
        )
        required = (
            "A Review that decides whether implementation, execution, runtime "
            "planning, promotion, archive, or completion may proceed is "
            "gate-bearing",
            "use role `independent-reviewer`, profile `control-plane-high`, "
            "distinct-instance independence, and authority "
            "`governed-review-evidence`",
            "A standalone Review that explicitly does not decide a gate is advisory",
            "preserve any eligible user-selected product, use role "
            "`advisory-reviewer`, profile `control-plane-high`, "
            "advisory-not-gate-bearing independence, and authority `advisory-input`",
            "`cohesive-medium` and `mechanical-low` are "
            "executor/evidence-collection profiles, not Review profiles",
            "For standalone prompt or recommendation wording, a request to open "
            "or name a new distinct reviewer instance remains actionable after "
            "all six assignment concepts are resolved",
            "do not infer unavailability merely because a concrete instance ID "
            "or open window is not yet supplied",
            "Return `BLOCKED` only when the request explicitly says no eligible "
            "distinct instance exists or insists on reusing an implementation instance",
            "return `BLOCKED` with `blocker_owner: user` and a non-blank resume condition",
        )
        for surface in surfaces:
            normalized = " ".join(surface.read_text(encoding="utf-8").split())
            with self.subTest(surface=surface):
                for phrase in required:
                    self.assertIn(phrase, normalized)

    def test_current_router_surfaces_reject_legacy_current_wording(self):
        surfaces = (
            "SKILL.md",
            "references/request-modes.md",
            "references/response-patterns.md",
            "references/approved-implementation-workflow.md",
            "references/step-evidence-gate.md",
            "references/superpowers-adapter.md",
            "references/completion-contract.md",
            "references/agent-capability-routing.md",
        )
        forbidden = (
            "schema-version-5",
            "schema-5 Handoff",
            "required Codex, Antigravity CLI, or Grok CLI",
        )
        for relative in surfaces:
            text = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(surface=relative):
                for phrase in forbidden:
                    self.assertNotIn(phrase, text)

    def test_public_docs_bind_current_schema6_and_schema2_evidence(self):
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README_cn.md").read_text(encoding="utf-8")
        self.assertIn("Current governed status uses schema 6", english)
        self.assertIn("schema-2 evidence manifests", english)
        self.assertIn("Frozen schema-4/schema-5", english)
        self.assertNotIn("For an actual schema-4 external status", english)
        self.assertNotIn("Each referenced artifact embeds a schema-1 manifest", english)
        self.assertIn("当前受治理状态使用 schema 6", chinese)
        self.assertIn("schema-2 evidence manifest", chinese)
        self.assertIn("冻结的 schema-4/schema-5", chinese)
        self.assertNotIn("对实际 schema 4 外部状态", chinese)
        self.assertNotIn("每个引用 artifact 都内嵌 schema 1 manifest", chinese)


    def test_schema6_current_contract_accepts_all_four_reviewer_products(self):
        products = (
            ("codex", "codex-reviewer-02"),
            ("pi", "pi-reviewer-02"),
            ("antigravity-cli", "antigravity-reviewer-02"),
            ("grok-cli", "grok-reviewer-02"),
        )
        for product, instance in products:
            data = schema6_contract(self.validator, self.handoff)
            data["reviewer_assignment"] = standard_reviewer_assignment(product, instance)
            assert_schema6_fixture(data)
            with self.subTest(product=product):
                self.validator.validate_handoff_contract(data, "schema6-valid")

    def test_schema6_reviewer_assignment_exact_shape_fails_closed(self):
        invalid_mutations = (
            ("missing-assignment", lambda d: d.pop("reviewer_assignment")),
            ("missing-purpose", lambda d: d["reviewer_assignment"].pop("review_purpose")),
            (
                "blank-purpose",
                lambda d: d["reviewer_assignment"]["review_purpose"].update(object=" "),
            ),
            (
                "extra-purpose",
                lambda d: d["reviewer_assignment"]["review_purpose"].update(extra="x"),
            ),
            (
                "bad-independence-kind",
                lambda d: d["reviewer_assignment"]["independence_requirement"].update(
                    kind="session-label"
                ),
            ),
            (
                "duplicate-independence-target",
                lambda d: d["reviewer_assignment"]["independence_requirement"].update(
                    distinct_from=["executor_assignment", "executor_assignment"]
                ),
            ),
            (
                "canonical-authority",
                lambda d: d["reviewer_assignment"].update(
                    result_authority="canonical-decision"
                ),
            ),
            (
                "unknown-product",
                lambda d: d["reviewer_assignment"].update(agent_product="unknown-agent"),
            ),
        )
        for label, mutate in invalid_mutations:
            data = schema6_contract(self.validator, self.handoff)
            assert_schema6_fixture(data)
            mutate(data)
            with self.subTest(case=label):
                with self.assertRaisesRegex(
                    AssertionError,
                    "reviewer_assignment|review_purpose|independence|result_authority|agent_product",
                ):
                    self.validator.validate_handoff_contract(data, label)

    def test_schema6_standard_strict_and_compact_profiles_are_exact(self):
        for profile in ("standard", "strict"):
            valid = schema6_contract(self.validator, self.handoff, risk_profile=profile)
            self.validator.validate_handoff_contract(valid, f"{profile}-valid")

            invalid_cases = []
            wrong_targets = copy.deepcopy(valid)
            wrong_targets["reviewer_assignment"]["independence_requirement"][
                "distinct_from"
            ] = ["executor_assignment"]
            invalid_cases.append(("independence", wrong_targets))

            same_instance = copy.deepcopy(valid)
            same_instance["reviewer_assignment"]["agent_instance_id"] = (
                same_instance["control_plane_owner"]["agent_instance_id"]
            )
            invalid_cases.append(("instance", same_instance))

            wrong_role = copy.deepcopy(valid)
            wrong_role["reviewer_assignment"]["agent_role"] = "control-plane"
            invalid_cases.append(("agent_role", wrong_role))

            wrong_profile = copy.deepcopy(valid)
            wrong_profile["reviewer_assignment"]["capability_profile"] = "cohesive-medium"
            invalid_cases.append(("capability_profile", wrong_profile))

            unexpected_reason = copy.deepcopy(valid)
            unexpected_reason["independent_review_not_applicable_reason"] = "not allowed"
            invalid_cases.append(("reason", unexpected_reason))

            for expected, invalid in invalid_cases:
                with self.subTest(profile=profile, invalid=expected):
                    with self.assertRaisesRegex(
                        AssertionError,
                        f"{expected}|reviewer_assignment|standard|strict",
                    ):
                        self.validator.validate_handoff_contract(invalid, "invalid-profile")

        compact = compact_schema6_contract(self.validator, self.handoff)
        self.validator.validate_handoff_contract(compact, "compact-valid")
        owner = compact["control_plane_owner"]
        reviewer = compact["reviewer_assignment"]
        self.assertEqual(
            {
                key: reviewer[key]
                for key in (
                    "agent_product", "agent_instance_id", "agent_role",
                    "capability_profile",
                )
            },
            owner,
        )

        compact_cases = []
        wrong_identity = copy.deepcopy(compact)
        wrong_identity["reviewer_assignment"]["agent_instance_id"] = "codex-reviewer-09"
        compact_cases.append(("control-plane|identity|instance", wrong_identity))
        wrong_targets = copy.deepcopy(compact)
        wrong_targets["reviewer_assignment"]["independence_requirement"][
            "distinct_from"
        ] = ["control_plane_owner", "executor_assignment"]
        compact_cases.append(("independence", wrong_targets))
        same_executor = copy.deepcopy(compact)
        same_executor["executor_assignment"]["agent_instance_id"] = owner["agent_instance_id"]
        compact_cases.append(("executor|instance|distinct", same_executor))
        blank_reason = copy.deepcopy(compact)
        blank_reason["independent_review_not_applicable_reason"] = " "
        compact_cases.append(("reason|non-blank", blank_reason))
        for expected, invalid in compact_cases:
            with self.subTest(compact_invalid=expected):
                with self.assertRaisesRegex(AssertionError, expected):
                    self.validator.validate_handoff_contract(invalid, "invalid-compact")

    def test_schema6_current_and_legacy_validation_are_isolated(self):
        current_cases = (
            ("schema4", schema4_contract(self.validator, self.handoff)),
            ("schema5", schema5_contract(self.validator, self.handoff)),
        )
        for label, data in current_cases:
            with self.subTest(current_rejects=label):
                with self.assertRaisesRegex(
                    AssertionError, "current.*6|schema_version.*6"
                ):
                    self.validator.validate_handoff_contract(data, label)

        missing = self.validator.extract_handoff_contract(self.handoff, "missing")
        missing.pop("schema_version")
        with self.assertRaisesRegex(AssertionError, "current.*6|schema_version.*6"):
            self.validator.validate_handoff_contract(missing, "missing-schema")

        mislabeled = schema5_contract(self.validator, self.handoff)
        mislabeled["schema_version"] = 6
        with self.assertRaisesRegex(
            AssertionError,
            "reviewer_assignment|missing contract fields|unexpected contract fields",
        ):
            self.validator.validate_handoff_contract(mislabeled, "mislabeled-schema5")

        self.assertTrue(
            hasattr(self.validator, "validate_legacy_handoff_contract"),
            "production legacy-only validator API is missing",
        )

    def test_schema6_legacy_inventory_is_read_only_and_non_authorizing(self):
        self.assertTrue(
            hasattr(self.validator, "inventory_legacy_handoffs"),
            "production legacy inventory API is missing",
        )
        inventory = getattr(self.validator, "inventory_legacy_handoffs")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            status = root / "status.md"
            status.write_text(
                render_handoff_contract(
                    self.validator, schema5_contract(self.validator, self.handoff)
                ),
                encoding="utf-8",
            )
            with mock.patch.object(
                self.validator,
                "validate_transition",
                side_effect=AssertionError("legacy inventory called current transition"),
            ), mock.patch.object(
                self.validator,
                "validate_evidence_artifacts",
                side_effect=AssertionError("legacy inventory called evidence authority"),
            ):
                records = inventory([root])
        self.assertEqual(len(records), 1)
        self.assertEqual(
            set(records[0]),
            {"path", "schema_version", "lifecycle_state", "sha256", "drain_status"},
        )
        self.assertEqual(records[0]["schema_version"], 5)
        self.assertEqual(records[0]["lifecycle_state"], "ready-for-brief")

    def test_schema6_pi_is_current_only_and_cannot_backfill_legacy(self):
        self.assertTrue(
            hasattr(self.validator, "validate_legacy_handoff_contract"),
            "production legacy-only validator API is missing",
        )
        validate_legacy = getattr(self.validator, "validate_legacy_handoff_contract")

        schema4 = schema4_contract(
            self.validator, self.handoff, independent_reviewer_agent="pi"
        )
        with self.assertRaisesRegex(AssertionError, "reviewer|product|identity|agent"):
            validate_legacy(schema4, "schema4-pi")

        schema5 = schema5_contract(self.validator, self.handoff)
        schema5["independent_reviewer_assignment"]["agent_product"] = "pi"
        with self.assertRaisesRegex(AssertionError, "agent_product|product"):
            validate_legacy(schema5, "schema5-pi")

        schema6 = schema6_contract(self.validator, self.handoff)
        schema6["reviewer_assignment"] = standard_reviewer_assignment(
            "pi", "pi-reviewer-02"
        )
        self.validator.validate_handoff_contract(schema6, "schema6-pi")

    def test_schema6_reviewer_assignment_is_fully_readonly(self):
        readonly_mutations = (
            (("review_purpose", "object"), "changed review object"),
            (("review_purpose", "decision"), "changed review decision"),
            (("agent_product",), "pi"),
            (("agent_instance_id",), "changed-reviewer-09"),
            (("agent_role",), "control-plane"),
            (("capability_profile",), "cohesive-medium"),
            (
                ("independence_requirement", "distinct_from"),
                ["executor_assignment"],
            ),
            (("result_authority",), "canonical-control-plane-decision"),
        )
        for changed_path, changed_value in readonly_mutations:
            before = schema6_contract(self.validator, self.handoff)
            after = copy.deepcopy(before)
            after["contract_revision"] += 1
            after["lifecycle_state"] = "ready-for-execution"
            after["next_owner"] = "external-agent"
            set_nested(after["reviewer_assignment"], changed_path, changed_value)
            with self.subTest(changed_path=changed_path):
                with self.assertRaisesRegex(
                    AssertionError, "readonly|reviewer_assignment"
                ):
                    self.validator.validate_transition(
                        before, after, "assignment-mutation"
                    )

    def test_schema6_pi_review_evidence_matches_assignment_without_promotion(self):
        data = schema6_contract(self.validator, self.handoff)
        data["reviewer_assignment"] = standard_reviewer_assignment(
            "pi", "pi-reviewer-02"
        )
        data.update(
            lifecycle_state="ready-for-brief",
            current_batch=2,
            contract_revision=4,
            last_review_result="pass",
            attempt_report_artifact=artifact("report.md"),
            last_review_artifact=artifact("review.md"),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            materialize_schema5_lease(data, root)
            report = root / "report.md"
            report.write_text(
                schema2_assignment_evidence_manifest(
                    "attempt-report",
                    "pass",
                    data["executor_assignment"],
                    contract_revision=1,
                ),
                encoding="utf-8",
            )
            data["attempt_report_artifact"]["sha256"] = hashlib.sha256(
                report.read_bytes()
            ).hexdigest()
            review = root / "review.md"
            review.write_text(
                schema2_assignment_evidence_manifest(
                    "batch-review", "pass", data["reviewer_assignment"]
                ),
                encoding="utf-8",
            )
            data["last_review_artifact"]["sha256"] = hashlib.sha256(
                review.read_bytes()
            ).hexdigest()
            self.validator.validate_handoff_contract(data, "schema6-pi-evidence")
            canonical_before = copy.deepcopy(data)
            self.validator.validate_evidence_artifacts(
                data, root, "schema6-pi-evidence"
            )
            self.assertEqual(data, canonical_before)

            review.write_text(
                schema2_assignment_evidence_manifest(
                    "batch-review",
                    "pass",
                    standard_reviewer_assignment("codex", "pi-reviewer-02"),
                ),
                encoding="utf-8",
            )
            data["last_review_artifact"]["sha256"] = hashlib.sha256(
                review.read_bytes()
            ).hexdigest()
            with self.assertRaisesRegex(
                AssertionError, "identity|role|profile|assignment"
            ):
                self.validator.validate_evidence_artifacts(
                    data, root, "schema6-pi-impersonation"
                )


    def test_schema4_agent_identity_fields_are_immutable(self):
        before = schema4_contract(self.validator, self.handoff)
        after = dict(before)
        after.update(
            lifecycle_state="ready-for-execution",
            contract_revision=before["contract_revision"] + 1,
            next_owner="external-agent",
            executor_agent="grok-cli",
            independent_reviewer_agent="codex",
        )
        with self.assertRaisesRegex(
            AssertionError,
            "readonly field changed: (executor_agent|independent_reviewer_agent)",
        ):
            self.validator._validate_legacy_transition(before, after, "identity-change")

    def test_attempt_report_manifest_binds_executor_identity_and_role(self):
        data = schema4_contract(
            self.validator, self.handoff, lifecycle_state="ready-for-review",
            contract_revision=2, next_owner="codex-brief-antigravity-review",
            attempt_report_artifact=artifact("report.md"),
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            report = root / "report.md"
            report.write_text(evidence_manifest("attempt-report", "pass"), encoding="utf-8")
            data["attempt_report_artifact"] = {
                "path": "report.md", "sha256": hashlib.sha256(report.read_bytes()).hexdigest(),
            }
            self.validator.validate_legacy_handoff_contract(data, "executor-evidence")
            self.validator._validate_legacy_evidence_artifacts(data, root, "executor-evidence")

            report.write_text(evidence_manifest(
                "attempt-report", "pass", agent_identity="grok-cli", agent_role="independent-reviewer",
            ), encoding="utf-8")
            data["attempt_report_artifact"]["sha256"] = hashlib.sha256(report.read_bytes()).hexdigest()
            with self.assertRaisesRegex(AssertionError, "identity|role|executor|impersonation"):
                self.validator._validate_legacy_evidence_artifacts(data, root, "executor-impersonation")

    def test_batch_review_rejects_executor_self_review_and_impersonation(self):
        data = schema4_contract(
            self.validator, self.handoff, lifecycle_state="awaiting-final-verification",
            current_batch=2, contract_revision=3, last_review_result="pass",
            next_owner="openspec-superpower-change",
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            report = root / "report.md"
            review = root / "review.md"
            report.write_text(evidence_manifest(
                "attempt-report", "pass", current_batch=2, contract_revision=1,
            ), encoding="utf-8")
            review.write_text(evidence_manifest(
                "batch-review", "pass", current_batch=2, contract_revision=2,
                agent_identity="antigravity-cli", agent_role="independent-reviewer",
            ), encoding="utf-8")
            data["attempt_report_artifact"] = {
                "path": "report.md", "sha256": hashlib.sha256(report.read_bytes()).hexdigest(),
            }
            data["last_review_artifact"] = {
                "path": "review.md", "sha256": hashlib.sha256(review.read_bytes()).hexdigest(),
            }
            self.validator.validate_legacy_handoff_contract(data, "review-impersonation")
            with self.assertRaisesRegex(AssertionError, "identity|reviewer|self-review|impersonation"):
                self.validator._validate_legacy_evidence_artifacts(data, root, "review-impersonation")

    def test_timeout_audit_binds_codex_decision_owner_for_shared_artifact(self):
        data = schema4_contract(
            self.validator, self.handoff, lifecycle_state="blocked", contract_revision=2,
            last_review_result="blocked", blocked_reason="executor timeout",
            blocker_owner="external-agent", resume_condition="redispatch",
            next_owner="codex-brief-antigravity-review",
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            timeout = root / "timeout.md"
            timeout.write_text(evidence_manifest("timeout-audit", "blocked"), encoding="utf-8")
            ref = {"path": "timeout.md", "sha256": hashlib.sha256(timeout.read_bytes()).hexdigest()}
            data["attempt_report_artifact"] = ref
            data["last_review_artifact"] = ref
            self.validator.validate_legacy_handoff_contract(data, "timeout-identity")
            self.validator._validate_legacy_evidence_artifacts(data, root, "timeout-identity")

    def test_fallback_scalar_parser_handles_yaml_booleans_and_null(self):
        self.assertIs(self.validator.parse_scalar("true"), True)
        self.assertIs(self.validator.parse_scalar("false"), False)
        self.assertIsNone(self.validator.parse_scalar("null"))

    def test_fail_transition_cannot_advance_batch(self):
        before = self.validator.extract_handoff_contract(self.handoff, "handoff")
        before.update(
            lifecycle_state="ready-for-review",
            last_review_result="not-run",
            attempt_report_artifact=artifact("docs/agent-collab/change/report.md"),
        )
        after = dict(before)
        after.update(
            lifecycle_state="needs-fix",
            last_review_result="fail",
            last_review_artifact=artifact("docs/review/fail.md"),
            attempt=before["attempt"] + 1,
            contract_revision=before["contract_revision"] + 1,
            next_owner="codex-brief-antigravity-review",
        )
        after["current_batch"] = before["current_batch"] + 1
        with self.assertRaisesRegex(AssertionError, "same batch"):
            self.validator.validate_transition(before, after, "invalid-fail")

    def test_final_batch_pass_hands_back_to_router(self):
        before = self.validator.extract_handoff_contract(self.handoff, "handoff")
        before.update(
            lifecycle_state="ready-for-review",
            current_batch=before["planned_batches"],
            last_review_result="not-run",
            attempt_report_artifact=artifact("docs/agent-collab/change/report.md"),
        )
        after = dict(before)
        after.update(
            lifecycle_state="awaiting-final-verification",
            last_review_result="pass",
            last_review_artifact=artifact("docs/review/batch.md"),
            contract_revision=before["contract_revision"] + 1,
            next_owner="openspec-superpower-change",
        )
        self.validator.validate_transition(before, after, "final-pass")

    def test_both_skills_publish_same_closure_fields(self):
        if not BRIEF_HANDOFF.is_file():
            self.skipTest("companion repository is not checked out")
        brief_handoff = BRIEF_HANDOFF.read_text(encoding="utf-8")
        for expected in (
            "schema_version: 6",
            "lifecycle_state:",
            "attempt:",
            "attempt_report_artifact:",
            "last_review_result:",
            "last_review_artifact:",
            "final_verification:",
            "final_verification_artifact:",
            "final_review_result:",
            "final_review_artifact:",
        ):
            self.assertIn(expected, self.handoff)
            self.assertIn(expected, brief_handoff)

    def test_execution_contract_rejects_unapproved_proposal_mode(self):
        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        data.update(
            mode="openspec-proposal",
            approval_status="proposed",
            executor="codex",
            governor="openspec-superpower-change",
        )
        with self.assertRaisesRegex(AssertionError, "execution contract"):
            self.validator.validate_handoff_contract(data, "proposal")

    def test_regular_transition_cannot_change_batch_attempt_or_owner(self):
        before = self.validator.extract_handoff_contract(self.handoff, "handoff")
        after = dict(before)
        after.update(
            lifecycle_state="ready-for-execution",
            current_batch=before["current_batch"] + 1,
            attempt=99,
            next_owner="user",
            contract_revision=before["contract_revision"] + 1,
        )
        with self.assertRaisesRegex(AssertionError, "same batch and attempt|next_owner"):
            self.validator.validate_transition(before, after, "illegal-jump")

    def test_blocked_contract_requires_blocked_review_result(self):
        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        data.update(
            lifecycle_state="blocked",
            last_review_result="pass",
            blocked_reason="dependency unavailable",
            blocker_owner="dependency",
            resume_condition="dependency restored",
            next_owner="user",
        )
        with self.assertRaisesRegex(AssertionError, "blocked|tuple"):
            self.validator.validate_handoff_contract(data, "blocked-pass")

    def test_compact_contract_still_requires_typed_evidence_fields(self):
        data = compact_schema6_contract(self.validator, self.handoff)
        data.update(
            step_critical="pytest",
            final_critical="pytest",
            stop_conditions="none",
            verification_strategy="run tests",
        )
        with self.assertRaisesRegex(AssertionError, "list|mapping"):
            self.validator.validate_handoff_contract(data, "untyped-compact")

    def test_complete_state_is_terminal(self):
        before = self.validator.extract_handoff_contract(self.handoff, "handoff")
        before.update(
            lifecycle_state="complete",
            current_batch=before["planned_batches"],
            last_review_result="pass",
            final_review_result="pass",
            final_verification="pass",
            attempt_report_artifact=artifact("docs/agent-collab/change/report.md"),
            last_review_artifact=artifact("docs/review/batch.md"),
            final_verification_artifact=artifact("docs/agent-collab/change/final-verification.md"),
            final_review_artifact=artifact("docs/review/final.md"),
            next_owner="user",
        )
        after = dict(before)
        after.update(attempt=2, contract_revision=before["contract_revision"] + 1)
        with self.assertRaisesRegex(AssertionError, "terminal"):
            self.validator.validate_transition(before, after, "mutate-complete")

    def test_change_id_must_be_path_safe_slug(self):
        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        data["change_id"] = "../escape"
        with self.assertRaisesRegex(AssertionError, "change_id"):
            self.validator.validate_handoff_contract(data, "unsafe-change-id")

    def test_shared_handoff_contract_is_byte_identical(self):
        if not BRIEF_HANDOFF.is_file():
            self.skipTest("companion repository is not checked out")
        brief_handoff = BRIEF_HANDOFF.read_text(encoding="utf-8")
        self.assertEqual(self.handoff, brief_handoff)

    def test_shared_validator_core_is_byte_identical_when_companion_exists(self):
        brief_validator = BRIEF_ROOT / "scripts" / "validate_templates.py"
        if not brief_validator.is_file():
            self.skipTest("companion repository is not checked out")
        openspec_text = (ROOT / "scripts" / "validate_core_gates.py").read_text(encoding="utf-8")
        brief_text = brief_validator.read_text(encoding="utf-8")

        def core(text: str) -> str:
            return text.split("START =", 1)[1].split("def validate_frontmatter", 1)[0]

        self.assertEqual(core(openspec_text), core(brief_text))

    def test_final_gate_failure_can_return_to_fix_with_new_attempt(self):
        before = self._awaiting_contract("pass")
        after = dict(before)
        after.update(
            lifecycle_state="needs-fix",
            attempt=before["attempt"] + 1,
            contract_revision=before["contract_revision"] + 1,
            final_review_result="fail",
            final_review_artifact=artifact("docs/review/final-fail.md"),
            next_owner="openspec-superpower-change",
        )
        self.validator.validate_transition(before, after, "final-gate-fix")

    def test_all_external_profiles_require_nonblank_critical_commands(self):
        data = compact_schema6_contract(self.validator, self.handoff)
        data.update(step_critical=[], final_critical=[])
        with self.assertRaisesRegex(AssertionError, "step_critical|final_critical"):
            self.validator.validate_handoff_contract(data, "empty-critical")

        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        data.update(step_critical=["   "], final_critical=["\t"])
        with self.assertRaisesRegex(AssertionError, "non-blank"):
            self.validator.validate_handoff_contract(data, "blank-critical")

    def test_blank_stop_and_blocker_values_are_rejected(self):
        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        data["stop_conditions"] = [" "]
        with self.assertRaisesRegex(AssertionError, "stop_conditions"):
            self.validator.validate_handoff_contract(data, "blank-stop")

        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        data.update(
            lifecycle_state="blocked",
            last_review_result="blocked",
            last_review_artifact=artifact("docs/review/blocked.md"),
            attempt_report_artifact=artifact("docs/agent-collab/change/report-abort.md"),
            blocked_reason=" ",
            blocker_owner="dependency",
            resume_condition="\t",
            next_owner="user",
        )
        with self.assertRaisesRegex(AssertionError, "blocked_reason|resume_condition"):
            self.validator.validate_handoff_contract(data, "blank-blocker")

    def test_boolean_is_not_a_positive_integer(self):
        for key in ("current_batch", "planned_batches", "attempt", "contract_revision"):
            data = self.validator.extract_handoff_contract(self.handoff, "handoff")
            data[key] = True
            with self.subTest(key=key):
                with self.assertRaisesRegex(AssertionError, "positive integer"):
                    self.validator.validate_handoff_contract(data, f"bool-{key}")

    def test_readonly_fields_must_match_exactly_without_duplicates(self):
        base = self.validator.extract_handoff_contract(self.handoff, "handoff")
        for readonly in (
            list(base["readonly_fields"]) + ["attempt"],
            list(base["readonly_fields"]) + [base["readonly_fields"][0]],
            list(base["readonly_fields"])[1:],
        ):
            data = dict(base)
            data["readonly_fields"] = readonly
            with self.subTest(readonly=readonly):
                with self.assertRaisesRegex(AssertionError, "readonly_fields"):
                    self.validator.validate_handoff_contract(data, "readonly-mismatch")

    def test_result_and_artifact_fields_are_strictly_paired(self):
        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        data["last_review_artifact"] = artifact("docs/review/unexpected.md")
        with self.assertRaisesRegex(AssertionError, "last_review_artifact"):
            self.validator.validate_handoff_contract(data, "unexpected-review-artifact")

        data = self._awaiting_contract("pass")
        data["final_verification_artifact"] = None
        with self.assertRaisesRegex(AssertionError, "final_verification_artifact"):
            self.validator.validate_handoff_contract(data, "missing-final-evidence")

    def test_artifact_reference_must_be_safe_relative_path_and_sha256(self):
        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        data.update(
            lifecycle_state="ready-for-brief",
            last_review_result="pass",
            last_review_artifact={"path": "../escape", "sha256": "x"},
        )
        with self.assertRaisesRegex(AssertionError, "artifact|sha256|relative"):
            self.validator.validate_handoff_contract(data, "unsafe-artifact")

    def test_runtime_artifact_validation_checks_file_size_and_hash(self):
        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        data.update(
            lifecycle_state="ready-for-brief",
            current_batch=2,
            contract_revision=4,
            last_review_result="pass",
            attempt_report_artifact=artifact("docs/agent-collab/change/report.md"),
            last_review_artifact=artifact("docs/review/batch.md"),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            materialize_schema5_lease(data if "data" in locals() else current, root)
            report = root / "docs" / "agent-collab" / "change" / "report.md"
            report.parent.mkdir(parents=True)
            report.write_text(
                schema5_evidence_manifest(
                    "attempt-report", "pass", contract_revision=1
                ),
                encoding="utf-8",
            )
            data["attempt_report_artifact"]["sha256"] = hashlib.sha256(
                report.read_bytes()
            ).hexdigest()
            review = root / "docs" / "review" / "batch.md"
            review.parent.mkdir(parents=True)
            review.write_text(
                schema5_evidence_manifest(
                    "batch-review", "pass", contract_revision=2
                ),
                encoding="utf-8",
            )
            data["last_review_artifact"]["sha256"] = hashlib.sha256(review.read_bytes()).hexdigest()
            self.validator.validate_evidence_artifacts(data, root, "runtime")
            data["last_review_artifact"]["sha256"] = "0" * 64
            with self.assertRaisesRegex(AssertionError, "sha256"):
                self.validator.validate_evidence_artifacts(data, root, "runtime")

    def _awaiting_contract(self, verification: str = "pending") -> dict:
        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        data.update(
            lifecycle_state="awaiting-final-verification",
            current_batch=data["planned_batches"],
            last_review_result="pass",
            attempt_report_artifact=artifact("docs/agent-collab/change/report.md"),
            last_review_artifact=artifact("docs/review/batch.md"),
            final_verification=verification,
            final_verification_artifact=(
                artifact("docs/agent-collab/change/final-verification.md")
                if verification != "pending" else None
            ),
            final_review_result="pending",
            final_review_artifact=None,
            next_owner="openspec-superpower-change",
        )
        return data

    def test_final_verification_pass_can_be_persisted_before_final_review(self):
        before = self._awaiting_contract()
        after = self._awaiting_contract("pass")
        after["contract_revision"] = before["contract_revision"] + 1
        self.validator.validate_transition(before, after, "persist-final-verification")

    def test_complete_requires_persisted_verification_and_all_artifacts(self):
        before = self._awaiting_contract()
        after = self._awaiting_contract("pass")
        after.update(
            lifecycle_state="complete",
            final_review_result="pass",
            final_review_artifact=artifact("docs/review/final.md"),
            next_owner="user",
            contract_revision=before["contract_revision"] + 1,
        )
        with self.assertRaisesRegex(AssertionError, "persisted final verification"):
            self.validator.validate_transition(before, after, "atomic-complete")

        before = self._awaiting_contract("pass")
        after = dict(before)
        after.update(
            lifecycle_state="complete",
            final_review_result="pass",
            final_review_artifact=artifact("docs/review/final.md"),
            next_owner="user",
            contract_revision=before["contract_revision"] + 1,
        )
        self.validator.validate_transition(before, after, "evidenced-complete")

    def test_batch_blocked_cannot_resume_directly_to_review(self):
        before = self.validator.extract_handoff_contract(self.handoff, "handoff")
        before.update(
            lifecycle_state="blocked",
            last_review_result="blocked",
            attempt_report_artifact=artifact("docs/agent-collab/change/abort.md"),
            last_review_artifact=artifact("docs/review/blocked.md"),
            blocked_reason="dependency unavailable",
            blocker_owner="dependency",
            resume_condition="dependency restored",
            next_owner="user",
        )
        after = dict(before)
        after.update(
            lifecycle_state="ready-for-review",
            last_review_result="not-run",
            last_review_artifact=None,
            blocked_reason=None,
            blocker_owner="none",
            resume_condition=None,
            next_owner="codex-brief-antigravity-review",
            attempt=before["attempt"] + 1,
            contract_revision=before["contract_revision"] + 1,
        )
        with self.assertRaisesRegex(AssertionError, "invalid lifecycle transition"):
            self.validator.validate_transition(before, after, "skip-report")

    def test_needs_fix_accepts_batch_and_each_final_failure_stage(self):
        batch = self.validator.extract_handoff_contract(self.handoff, "handoff")
        batch.update(
            lifecycle_state="needs-fix",
            last_review_result="fail",
            attempt_report_artifact=artifact("docs/agent-collab/change/report.md"),
            last_review_artifact=artifact("docs/review/batch-fail.md"),
        )
        self.validator.validate_handoff_contract(batch, "batch-fail")

        verification = self._awaiting_contract()
        verification.update(
            lifecycle_state="needs-fix",
            final_verification="fail",
            final_verification_artifact=artifact("docs/agent-collab/change/final-verification-fail.md"),
        )
        self.validator.validate_handoff_contract(verification, "verification-fail")

        review = self._awaiting_contract("pass")
        review.update(
            lifecycle_state="needs-fix",
            final_review_result="fail",
            final_review_artifact=artifact("docs/review/final-fail.md"),
        )
        self.validator.validate_handoff_contract(review, "final-review-fail")

    def test_blocked_accepts_batch_and_each_final_block_stage(self):
        common = {
            "lifecycle_state": "blocked",
            "blocked_reason": "dependency unavailable",
            "blocker_owner": "dependency",
            "resume_condition": "dependency restored",
            "next_owner": "user",
        }
        batch = self.validator.extract_handoff_contract(self.handoff, "handoff")
        batch.update(
            **common,
            last_review_result="blocked",
            attempt_report_artifact=artifact("docs/agent-collab/change/abort.md"),
            last_review_artifact=artifact("docs/review/batch-blocked.md"),
        )
        self.validator.validate_handoff_contract(batch, "batch-blocked")

        verification = self._awaiting_contract()
        verification.update(
            **common,
            final_verification="blocked",
            final_verification_artifact=artifact("docs/agent-collab/change/final-verification-blocked.md"),
        )
        self.validator.validate_handoff_contract(verification, "verification-blocked")

        review = self._awaiting_contract("pass")
        review.update(
            **common,
            final_review_result="blocked",
            final_review_artifact=artifact("docs/review/final-blocked.md"),
        )
        self.validator.validate_handoff_contract(review, "final-review-blocked")

    def test_preflight_blocked_does_not_require_an_attempt_report(self):
        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        data.update(
            lifecycle_state="blocked",
            last_review_result="blocked",
            last_review_artifact=artifact("docs/review/preflight-blocked.md"),
            blocked_reason="brief has an unauthorized git step",
            blocker_owner="codex-brief-antigravity-review",
            resume_condition="brief revised and preflight rerun",
            next_owner="codex-brief-antigravity-review",
        )
        self.assertIsNone(data["attempt_report_artifact"])
        self.validator.validate_handoff_contract(data, "preflight-blocked")

    def test_final_review_blocked_resume_preserves_verification_evidence(self):
        before = self._awaiting_contract("pass")
        before.update(
            lifecycle_state="blocked",
            final_review_result="blocked",
            final_review_artifact=artifact("docs/review/final-blocked.md"),
            blocked_reason="reviewer unavailable",
            blocker_owner="dependency",
            resume_condition="reviewer available",
            next_owner="user",
        )
        after = dict(before)
        after.update(
            lifecycle_state="awaiting-final-verification",
            final_review_result="pending",
            final_review_artifact=None,
            blocked_reason=None,
            blocker_owner="none",
            resume_condition=None,
            next_owner="openspec-superpower-change",
            contract_revision=before["contract_revision"] + 1,
        )
        self.validator.validate_transition(before, after, "resume-final-review")

        replaced = dict(after)
        replaced["attempt_report_artifact"] = artifact("docs/agent-collab/change/replacement-report.md")
        replaced["last_review_artifact"] = artifact("docs/review/replacement-batch.md")
        with self.assertRaisesRegex(AssertionError, "cannot rewrite"):
            self.validator.validate_transition(before, replaced, "resume-final-review-rewrite")

    def test_runtime_artifact_validation_rejects_missing_empty_and_symlink_escape(self):
        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        data.update(
            lifecycle_state="ready-for-brief",
            current_batch=2,
            contract_revision=4,
            last_review_result="pass",
            attempt_report_artifact=artifact("docs/agent-collab/change/report.md"),
            last_review_artifact=artifact("docs/review/batch.md"),
        )
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "root"
            root.mkdir()
            materialize_schema5_lease(data, root)
            with self.assertRaisesRegex(AssertionError, "exist and be non-empty"):
                self.validator.validate_evidence_artifacts(data, root, "missing")

            report = root / "docs" / "agent-collab" / "change" / "report.md"
            review = root / "docs" / "review" / "batch.md"
            report.parent.mkdir(parents=True)
            review.parent.mkdir(parents=True)
            report.write_text(schema5_evidence_manifest("attempt-report", "pass"), encoding="utf-8")
            review.write_text("", encoding="utf-8")
            data["attempt_report_artifact"]["sha256"] = hashlib.sha256(report.read_bytes()).hexdigest()
            with self.assertRaisesRegex(AssertionError, "exist and be non-empty"):
                self.validator.validate_evidence_artifacts(data, root, "empty")

            outside = base / "outside.md"
            outside.write_text("outside\n", encoding="utf-8")
            review.unlink()
            review.symlink_to(outside)
            data["last_review_artifact"]["sha256"] = hashlib.sha256(outside.read_bytes()).hexdigest()
            with self.assertRaisesRegex(AssertionError, "outside artifact root"):
                self.validator.validate_evidence_artifacts(data, root, "symlink")

    def test_nonfinal_batch_promotion_requires_review_pass_and_keeps_decision_evidence(self):
        before = self.validator.extract_handoff_contract(self.handoff, "handoff")
        before.update(
            lifecycle_state="ready-for-review",
            attempt_report_artifact=artifact("docs/agent-collab/change/report.md"),
            next_owner="codex-brief-antigravity-review",
        )
        after = dict(before)
        after.update(
            lifecycle_state="ready-for-brief",
            current_batch=before["current_batch"] + 1,
            attempt=1,
            contract_revision=before["contract_revision"] + 1,
            attempt_report_artifact=None,
            last_review_result="not-run",
            last_review_artifact=None,
            next_owner="codex-brief-antigravity-review",
        )

        with self.assertRaisesRegex(AssertionError, "Review PASS|review evidence"):
            self.validator.validate_transition(before, after, "promote-without-review")

    def test_batch_decision_cannot_replace_the_report_that_was_reviewed(self):
        before = self.validator.extract_handoff_contract(self.handoff, "handoff")
        before.update(
            lifecycle_state="ready-for-review",
            current_batch=before["planned_batches"],
            attempt_report_artifact=artifact("docs/agent-collab/change/original-report.md"),
            next_owner="codex-brief-antigravity-review",
        )
        after = dict(before)
        after.update(
            lifecycle_state="awaiting-final-verification",
            contract_revision=before["contract_revision"] + 1,
            attempt_report_artifact=artifact("docs/agent-collab/change/replacement-report.md"),
            last_review_result="pass",
            last_review_artifact=artifact("docs/review/batch-pass.md"),
            next_owner="openspec-superpower-change",
        )

        with self.assertRaisesRegex(AssertionError, "attempt_report_artifact|reviewed Report"):
            self.validator.validate_transition(before, after, "replace-reviewed-report")

    def test_final_review_cannot_start_in_the_revision_that_first_persists_verification_pass(self):
        before = self._awaiting_contract()
        after = dict(before)
        after.update(
            lifecycle_state="blocked",
            contract_revision=before["contract_revision"] + 1,
            final_verification="pass",
            final_verification_artifact=artifact("docs/agent-collab/change/final-verification.md"),
            final_review_result="blocked",
            final_review_artifact=artifact("docs/review/final-review-blocked.md"),
            blocked_reason="reviewer unavailable",
            blocker_owner="dependency",
            resume_condition="reviewer available",
            next_owner="user",
        )

        with self.assertRaisesRegex(AssertionError, "persisted final verification|final Review"):
            self.validator.validate_transition(before, after, "atomic-final-verification-and-review")

    def test_blocked_self_transition_cannot_change_gate_tuple_or_evidence(self):
        before = self.validator.extract_handoff_contract(self.handoff, "handoff")
        before.update(
            lifecycle_state="blocked",
            current_batch=before["planned_batches"],
            attempt_report_artifact=artifact("docs/agent-collab/change/report-abort.md"),
            last_review_result="blocked",
            last_review_artifact=artifact("docs/review/batch-blocked.md"),
            blocked_reason="batch dependency unavailable",
            blocker_owner="dependency",
            resume_condition="batch dependency restored",
            next_owner="user",
        )
        after = dict(before)
        after.update(
            contract_revision=before["contract_revision"] + 1,
            last_review_result="pass",
            last_review_artifact=artifact("docs/review/fabricated-batch-pass.md"),
            final_verification="pass",
            final_verification_artifact=artifact("docs/agent-collab/change/fabricated-final-verification.md"),
            final_review_result="blocked",
            final_review_artifact=artifact("docs/review/final-review-blocked.md"),
            blocked_reason="final reviewer unavailable",
            resume_condition="final reviewer available",
        )

        with self.assertRaisesRegex(AssertionError, "blocked self-transition|result tuple|evidence"):
            self.validator.validate_transition(before, after, "rewrite-blocked-stage")

    def test_runtime_complete_snapshot_rejects_reused_artifact_with_mismatched_role_and_result(self):
        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "evidence.md"
            evidence.write_text(
                "# Review Result: FAIL\nNo verification commands were run.\n",
                encoding="utf-8",
            )
            shared_ref = {
                "path": "evidence.md",
                "sha256": hashlib.sha256(evidence.read_bytes()).hexdigest(),
            }
            data.update(
                lifecycle_state="complete",
                current_batch=data["planned_batches"],
                attempt_report_artifact=dict(shared_ref),
                last_review_result="pass",
                last_review_artifact=dict(shared_ref),
                final_verification="pass",
                final_verification_artifact=dict(shared_ref),
                final_review_result="pass",
                final_review_artifact=dict(shared_ref),
                next_owner="user",
            )

            with self.assertRaisesRegex(AssertionError, "artifact|evidence|result|role|distinct"):
                self.validator.validate_handoff_contract(data, "mixed-complete")
                self.validator.validate_evidence_artifacts(data, root, "mixed-complete")

    def test_runtime_evidence_manifest_binds_artifact_role_and_result(self):
        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        data.update(
            lifecycle_state="complete",
            current_batch=data["planned_batches"],
            contract_revision=5,
            last_review_result="pass",
            final_verification="pass",
            final_review_result="pass",
            next_owner="user",
        )
        specs = {
            "attempt_report_artifact": ("attempt-report.md", "attempt-report", "pass", 1),
            "last_review_artifact": ("batch-review.md", "batch-review", "pass", 2),
            "final_verification_artifact": ("final-verification.md", "final-verification", "pass", 3),
            "final_review_artifact": ("final-review.md", "final-review", "fail", 4),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            materialize_schema5_lease(data if "data" in locals() else current, root)
            for key, (path, role, result, revision) in specs.items():
                target = root / path
                target.write_text(
                    schema5_evidence_manifest(role, result, current_batch=2, contract_revision=revision),
                    encoding="utf-8",
                )
                data[key] = {"path": path, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}
            self.validator.validate_handoff_contract(data, "distinct-complete")
            with self.assertRaisesRegex(AssertionError, "evidence result"):
                self.validator.validate_evidence_artifacts(data, root, "distinct-complete")

    def test_timeout_audit_can_bind_report_and_review_without_other_role_reuse(self):
        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            materialize_schema5_lease(data if "data" in locals() else current, root)
            timeout = root / "timeout-audit.md"
            timeout.write_text(schema5_evidence_manifest("timeout-audit", "blocked"), encoding="utf-8")
            ref = {"path": timeout.name, "sha256": hashlib.sha256(timeout.read_bytes()).hexdigest()}
            data.update(
                lifecycle_state="blocked",
                contract_revision=2,
                attempt_report_artifact=dict(ref),
                last_review_result="blocked",
                last_review_artifact=dict(ref),
                blocked_reason="external agent timed out",
                blocker_owner="external-agent",
                resume_condition="timeout audit resolved",
                next_owner="codex-brief-antigravity-review",
            )
            self.validator.validate_handoff_contract(data, "timeout")
            self.validator.validate_evidence_artifacts(data, root, "timeout")

        conflicting = dict(data)
        conflicting["last_review_artifact"] = dict(data["last_review_artifact"])
        conflicting["last_review_artifact"]["sha256"] = "c" * 64
        with self.assertRaisesRegex(AssertionError, "distinct by role"):
            self.validator.validate_handoff_contract(conflicting, "timeout-conflict")

    def test_complete_rejects_preflight_review_as_batch_review_evidence(self):
        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        data.update(
            lifecycle_state="complete",
            current_batch=data["planned_batches"],
            contract_revision=5,
            last_review_result="pass",
            final_verification="pass",
            final_review_result="pass",
            next_owner="user",
        )
        specs = {
            "attempt_report_artifact": ("attempt.md", "attempt-report", "pass", 1),
            "last_review_artifact": ("preflight.md", "preflight-review", "pass", 2),
            "final_verification_artifact": ("verification.md", "final-verification", "pass", 3),
            "final_review_artifact": ("final-review.md", "final-review", "pass", 4),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            materialize_schema5_lease(data if "data" in locals() else current, root)
            for key, (path, role, result, revision) in specs.items():
                target = root / path
                target.write_text(
                    schema5_evidence_manifest(role, result, current_batch=2, contract_revision=revision),
                    encoding="utf-8",
                )
                data[key] = {"path": path, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}
            self.validator.validate_handoff_contract(data, "preflight-as-batch")
            with self.assertRaisesRegex(AssertionError, "evidence role|batch-review"):
                self.validator.validate_evidence_artifacts(data, root, "preflight-as-batch")

    def test_timeout_audit_is_blocked_only_and_cannot_satisfy_complete(self):
        data = self.validator.extract_handoff_contract(self.handoff, "handoff")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            timeout = root / "timeout.md"
            timeout.write_text(evidence_manifest("timeout-audit", "pass"), encoding="utf-8")
            shared = {"path": timeout.name, "sha256": hashlib.sha256(timeout.read_bytes()).hexdigest()}
            data.update(
                lifecycle_state="complete",
                current_batch=data["planned_batches"],
                attempt_report_artifact=dict(shared),
                last_review_result="pass",
                last_review_artifact=dict(shared),
                final_verification="pass",
                final_verification_artifact=artifact("verification.md"),
                final_review_result="pass",
                final_review_artifact=artifact("final-review.md"),
                next_owner="user",
            )
            with self.assertRaisesRegex(AssertionError, "timeout-audit|distinct|blocked"):
                self.validator.validate_handoff_contract(data, "timeout-complete")

    def test_runtime_rejects_stale_batch_and_attempt_evidence(self):
        data = self._awaiting_contract()
        data.update(attempt=9, contract_revision=10)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            materialize_schema5_lease(data if "data" in locals() else current, root)
            specs = {
                "attempt_report_artifact": ("report.md", "attempt-report", 1),
                "last_review_artifact": ("review.md", "batch-review", 2),
            }
            for key, (path, role, revision) in specs.items():
                target = root / path
                target.write_text(
                    schema5_evidence_manifest(role, "pass", current_batch=1, attempt=1, contract_revision=revision),
                    encoding="utf-8",
                )
                data[key] = {"path": path, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}
            with self.assertRaisesRegex(AssertionError, "required batch|required attempt"):
                self.validator.validate_evidence_artifacts(data, root, "stale-evidence")

    def test_runtime_complete_requires_and_validates_previous_status(self):
        previous = self._awaiting_contract("pass")
        previous["contract_revision"] = 4
        current = dict(previous)
        current.update(
            lifecycle_state="complete",
            contract_revision=5,
            final_review_result="pass",
            final_review_artifact=artifact("final-review.md"),
            next_owner="user",
        )
        previous_bytes = b"canonical previous status revision 4\n"
        previous_sha = hashlib.sha256(previous_bytes).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            materialize_schema5_lease(data if "data" in locals() else current, root)
            specs = {
                "attempt_report_artifact": ("report.md", "attempt-report", "pass", 1, "b" * 64),
                "last_review_artifact": ("batch-review.md", "batch-review", "pass", 2, "c" * 64),
                "final_verification_artifact": ("verification.md", "final-verification", "pass", 3, "d" * 64),
                "final_review_artifact": ("final-review.md", "final-review", "pass", 4, previous_sha),
            }
            for key, (path, role, result, revision, source_sha) in specs.items():
                target = root / path
                target.write_text(
                    schema5_evidence_manifest(
                        role,
                        result,
                        current_batch=2,
                        contract_revision=revision,
                        canonical_sha256=source_sha,
                    ),
                    encoding="utf-8",
                )
                current[key] = {"path": path, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}
            previous.update(
                attempt_report_artifact=current["attempt_report_artifact"],
                last_review_artifact=current["last_review_artifact"],
                final_verification_artifact=current["final_verification_artifact"],
            )
            with self.assertRaisesRegex(AssertionError, "requires previous canonical status"):
                self.validator.validate_evidence_artifacts(current, root, "complete-without-history")
            self.validator.validate_evidence_artifacts(
                current,
                root,
                "complete-with-history",
                previous=previous,
                previous_status_sha256=previous_sha,
            )

    def test_previous_status_binds_nonfinal_promotion_to_reviewed_attempt(self):
        previous = self.validator.extract_handoff_contract(self.handoff, "handoff")
        previous.update(
            lifecycle_state="ready-for-review",
            attempt=3,
            contract_revision=3,
            attempt_report_artifact=artifact("report.md"),
            next_owner="codex-brief-antigravity-review",
        )
        current = dict(previous)
        current.update(
            lifecycle_state="ready-for-brief",
            current_batch=2,
            attempt=1,
            contract_revision=4,
            last_review_result="pass",
            last_review_artifact=artifact("review.md"),
            next_owner="codex-brief-antigravity-review",
        )
        previous_sha = hashlib.sha256(b"reviewed attempt 3 status\n").hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            materialize_schema5_lease(data if "data" in locals() else current, root)
            report = root / "report.md"
            review = root / "review.md"
            report.write_text(
                schema5_evidence_manifest("attempt-report", "pass", attempt=2, contract_revision=1),
                encoding="utf-8",
            )
            review.write_text(
                schema5_evidence_manifest(
                    "batch-review",
                    "pass",
                    attempt=2,
                    contract_revision=3,
                    canonical_sha256=previous_sha,
                ),
                encoding="utf-8",
            )
            report_ref = {"path": report.name, "sha256": hashlib.sha256(report.read_bytes()).hexdigest()}
            review_ref = {"path": review.name, "sha256": hashlib.sha256(review.read_bytes()).hexdigest()}
            previous["attempt_report_artifact"] = report_ref
            current["attempt_report_artifact"] = report_ref
            current["last_review_artifact"] = review_ref
            with self.assertRaisesRegex(AssertionError, "wrong source attempt"):
                self.validator.validate_evidence_artifacts(
                    current,
                    root,
                    "wrong-attempt-promotion",
                    previous=previous,
                    previous_status_sha256=previous_sha,
                )

    def test_major_self_evolution_requires_specific_validated_contract(self):
        rule = (ROOT / "references" / "self-evolution-rule.md").read_text(encoding="utf-8")
        self.assertIn("specific OpenSpec change", rule)
        self.assertIn("passes\nstrict validation", rule)
        self.assertNotIn("after user approval or an explicitly approved", rule)

    def test_openspec_closeout_requires_task_reconciliation_and_archive_validation(self):
        self.assertIn("OpenSpec closeout", self.approved)
        self.assertIn("references/completion-contract.md", self.approved)
        self.assertNotIn("Reconcile `tasks.md`", self.approved)
        self.assertNotIn("strict validation after archive", self.approved)
        normalized_completion = " ".join(self.completion.split())
        self.assertIn("Reconcile `tasks.md`", normalized_completion)
        self.assertIn("strict validation after archive", normalized_completion)

    def test_superpowers_adapter_and_preflight_review_are_explicit(self):
        adapter = (ROOT / "references" / "superpowers-adapter.md").read_text(encoding="utf-8")
        self.assertIn("single OpenSpec design contract", adapter)
        self.assertIn("never grants Git permission", adapter)
        self.assertIn("Preflight Review", adapter)
        self.assertIn("artifact revision", adapter)
        self.assertIn("Preflight uses only `PASS` or `BLOCKED`", adapter)
        self.assertNotIn("Preflight `FAIL`", adapter + self.approved)

    def test_bounded_plan_preflight_convergence_contract_is_complete(self):
        evidence = (ROOT / "references" / "step-evidence-gate.md").read_text(encoding="utf-8")
        combined = "\n".join((self.skill, self.approved, self.superpowers_adapter, evidence))

        for required in (
            "FULL_PREFLIGHT", "FOCUSED_RECHECK", "CONTROL_PLANE_ADJUDICATION",
            "finding_completeness", "lineage_root_revision", "reviewed_revision",
            "parent_review", "same_reviewer_instance", "protected_boundaries",
            "declared_correction_set", "mechanical_self_check",
            "non_blocking_recommendations", "accepted_residual_risks",
        ):
            self.assertIn(required, combined)
        for boundary in (
            "scope", "contract/spec", "acceptance", "risk/evidence profile",
            "authority", "assignments", "allowed/forbidden files",
            "branch/worktree", "database/production", "Git/publication/deployment",
        ):
            self.assertIn(boundary, self.approved)
        for safety in (
            "P0/P1", "security", "integrity/data loss", "false evidence",
            "PASS", "BLOCKED",
        ):
            self.assertIn(safety, self.approved)
        self.assertIn("same reviewer instance", self.approved)
        self.assertIn("whole regular-file bytes", self.approved)
        self.assertIn("non-symlink", self.approved)
        self.assertIn("Missing legacy fields", self.approved)
        self.assertIn("two blocked Review results", self.approved)
        self.assertIn(
            "at most one terminal `FOCUSED_RECHECK`",
            " ".join(self.approved.split()),
        )
        self.assertIn("Implementation Review", combined)
        self.assertIn("Final Review", combined)
        self.assertIn("references/completion-contract.md", combined)
        self.assertNotIn("Preflight `FAIL`", combined)

    def test_focused_preflight_semantic_fixture_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = root / "docs" / "plan.md"
            review = root / "reviews" / "root.md"
            plan.parent.mkdir()
            review.parent.mkdir()
            plan.write_bytes(b"corrected plan revision\n")
            reviewer = {
                "agent_product": "codex",
                "agent_instance_id": "codex-reviewer-01",
                "agent_role": "independent-reviewer",
                "capability_profile": "control-plane-high",
            }
            historical_root = {
                "path": "docs/plan.md",
                "sha256": hashlib.sha256(b"original plan revision\n").hexdigest(),
            }
            parent = {
                "lineage_root_revision": historical_root,
                "reviewer_identity": reviewer,
                "finding_completeness": True,
            }
            review.write_text(
                json.dumps(parent, sort_keys=True), encoding="utf-8"
            )
            valid = {
                "review_mode": "FOCUSED_RECHECK",
                "attempt": 2,
                "same_reviewer_instance": True,
                "reviewer_identity": reviewer,
                "lineage_root_revision": historical_root,
                "reviewed_revision": {
                    "path": "docs/plan.md",
                    "sha256": hashlib.sha256(plan.read_bytes()).hexdigest(),
                },
                "parent_review": {
                    "path": "reviews/root.md",
                    "sha256": hashlib.sha256(review.read_bytes()).hexdigest(),
                },
                "mechanical_self_check": True,
                "diff_within_declared_corrections": True,
                "declared_correction_set": ["F-1:Plan section 2"],
                "protected_boundaries": {
                    boundary: "unchanged" for boundary in PREFLIGHT_BOUNDARIES
                },
            }
            self.assertTrue(
                _focused_preflight_fixture_eligible(
                    root, valid, "codex-author-01", "codex-executor-01"
                )
            )
            forged_review = review.with_name("forged.md")
            forged_parent = copy.deepcopy(parent)
            forged_parent["reviewer_identity"]["agent_instance_id"] = "attacker-reviewer"
            forged_review.write_text(
                json.dumps(forged_parent, sort_keys=True), encoding="utf-8"
            )
            real_open = os.open
            parent_leaf_opens = 0

            def replace_after_parent_open(path, flags, *args, **kwargs):
                nonlocal parent_leaf_opens
                descriptor = real_open(path, flags, *args, **kwargs)
                if path == review.name:
                    parent_leaf_opens += 1
                    if parent_leaf_opens == 1:
                        os.replace(forged_review, review)
                return descriptor

            with mock.patch("os.open", side_effect=replace_after_parent_open):
                self.assertTrue(
                    _focused_preflight_fixture_eligible(
                        root, valid, "codex-author-01", "codex-executor-01"
                    )
                )
            self.assertEqual(1, parent_leaf_opens)
            review.write_text(json.dumps(parent, sort_keys=True), encoding="utf-8")

            mutations = (
                ("current SHA", lambda r: r["reviewed_revision"].update(sha256="0" * 64)),
                ("path drift", lambda r: r["reviewed_revision"].update(path="docs/other.md")),
                ("parent SHA", lambda r: r["parent_review"].update(sha256="0" * 64)),
                ("reviewer replacement", lambda r: r["reviewer_identity"].update(agent_instance_id="codex-reviewer-02")),
                ("author reuse", lambda r: r["reviewer_identity"].update(agent_instance_id="codex-author-01")),
                ("boundary change", lambda r: r["protected_boundaries"].update(scope="changed")),
                ("undeclared diff", lambda r: r.update(diff_within_declared_corrections=False)),
                ("missing legacy metadata", lambda r: r.pop("parent_review")),
                ("invalid retry", lambda r: r.update(attempt=3)),
            )
            for label, mutate in mutations:
                candidate = copy.deepcopy(valid)
                mutate(candidate)
                with self.subTest(label=label):
                    self.assertFalse(
                        _focused_preflight_fixture_eligible(
                            root, candidate, "codex-author-01", "codex-executor-01",
                        )
                    )

            for label, mutate_parent in (
                ("parent root metadata", lambda p: p["lineage_root_revision"].update(sha256="f" * 64)),
                ("parent reviewer metadata", lambda p: p["reviewer_identity"].update(agent_instance_id="codex-reviewer-02")),
                ("incomplete full review", lambda p: p.update(finding_completeness=False)),
            ):
                forged_parent = copy.deepcopy(parent)
                mutate_parent(forged_parent)
                review.write_text(json.dumps(forged_parent, sort_keys=True), encoding="utf-8")
                candidate = copy.deepcopy(valid)
                candidate["parent_review"]["sha256"] = hashlib.sha256(review.read_bytes()).hexdigest()
                with self.subTest(label=label):
                    self.assertFalse(
                        _focused_preflight_fixture_eligible(
                            root, candidate, "codex-author-01", "codex-executor-01",
                        )
                    )
            review.write_text(json.dumps(parent, sort_keys=True), encoding="utf-8")

            link = root / "docs" / "linked.md"
            link.symlink_to(plan)
            symlinked = copy.deepcopy(valid)
            symlinked["lineage_root_revision"]["path"] = "docs/linked.md"
            symlinked["reviewed_revision"]["path"] = "docs/linked.md"
            self.assertFalse(
                _focused_preflight_fixture_eligible(
                    root, symlinked, "codex-author-01", "codex-executor-01",
                )
            )

            outside = root / "outside"
            outside.mkdir()
            (outside / "plan.md").write_bytes(plan.read_bytes())
            (root / "linked-parent").symlink_to(outside, target_is_directory=True)
            escaped = copy.deepcopy(valid)
            escaped["lineage_root_revision"]["path"] = "linked-parent/plan.md"
            escaped["reviewed_revision"]["path"] = "linked-parent/plan.md"
            escaped_parent = copy.deepcopy(parent)
            escaped_parent["lineage_root_revision"] = escaped["lineage_root_revision"]
            review.write_text(json.dumps(escaped_parent, sort_keys=True), encoding="utf-8")
            escaped["parent_review"]["sha256"] = hashlib.sha256(review.read_bytes()).hexdigest()
            self.assertFalse(
                _focused_preflight_fixture_eligible(
                    root, escaped, "codex-author-01", "codex-executor-01",
                )
            )

    def test_preflight_profiles_and_effect_based_risk_remain_proportionate(self):
        combined = "\n".join((self.approved, self.superpowers_adapter, (
            ROOT / "references" / "step-evidence-gate.md"
        ).read_text(encoding="utf-8")))
        for profile in ("compact", "standard", "strict"):
            self.assertIn(f"`{profile}`", combined)
        self.assertIn("existing private read-only", combined)
        self.assertIn("changed effects", combined)
        self.assertIn("Any profile change", combined)
        self.assertIn("real evidence", combined)
        self.assertIn("mocks", combined)
        self.assertIn("platform permission", combined)

    def test_brief_trigger_excludes_state_changing_and_final_completion(self):
        if not (BRIEF_ROOT / "SKILL.md").is_file():
            self.skipTest("companion repository is not checked out")
        description = (BRIEF_ROOT / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
        for expected in (
            "non-state-changing", "read-only", "does not request fixes",
            "final completion", "valid Handoff Contract", "file edits",
            "workflow/template changes",
        ):
            self.assertIn(expected, description)


    def _valid_lease(self):
        return {
            "decision_id": "decision-001",
            "artifact_revision": 2,
            "artifact_sha256": "a" * 64,
            "approved_scope": "approved source implementation",
            "approved_actions": ["run-safe-tests", "fix-review-finding"],
            "risk_profile": "standard",
            "decision_source": "ai-proposed/user-approved",
            "owner_instance_id": "codex-control-01",
            "status": "valid",
            "invalidation_conditions": ["scope-change", "risk-change", "user-correction"],
        }

    def _valid_review_evidence(self):
        return {
            "actual_diff_inspected": True,
            "production_wiring_trace": ["source -> transform -> runtime"],
            "critical_reruns": ["python3 -m unittest focused -v"],
            "independent_probe": {
                "kind": "adversarial",
                "command": "probe --bounded-input",
                "result": "pass",
            },
            "copy_fields": {
                "expected": ["id", "version"],
                "observed": ["id", "version"],
            },
            "claims": [{
                "claim": "restart recovery",
                "mechanism": "runner retry state machine",
                "evidence": "focused recovery probe",
            }],
        }

    def _schema5_contract(self):
        data = schema5_contract(self.validator, self.handoff)
        for key in (
            "executor_agent", "independent_reviewer_agent", "decision_owner",
        ):
            data.pop(key, None)
        data.update({
            "schema_version": 5,
            "control_plane_owner": {
                "agent_product": "codex",
                "agent_instance_id": "codex-control-01",
                "agent_role": "control-plane",
                "capability_profile": "control-plane-high",
            },
            "executor_assignment": {
                "agent_product": "codex",
                "agent_instance_id": "codex-executor-01",
                "agent_role": "executor",
                "capability_profile": "cohesive-medium",
            },
            "independent_reviewer_assignment": {
                "agent_product": "codex",
                "agent_instance_id": "codex-reviewer-01",
                "agent_role": "independent-reviewer",
                "capability_profile": "control-plane-high",
            },
            "decision_source": "ai-proposed/user-approved",
            "confirmation_lease": {
                "decision_id": "decision-001",
                "path": "docs/agent-collab/add-example-change/confirmation-lease.md",
                "sha256": "c" * 64,
            },
        })
        data["readonly_fields"] = list(self.validator.SCHEMA5_IMMUTABLE_FIELDS)
        return data

    def test_tiered_01_platform_permission_reuses_safe_command_lease(self):
        validate = getattr(self.validator, "validate_confirmation_lease", None)
        self.assertTrue(callable(validate), "Confirmation Lease behavior is not implemented")
        result = validate(self._valid_lease(), {
            "action": "run-safe-tests",
            "artifact_revision": 2,
            "artifact_sha256": "a" * 64,
            "scope": "approved source implementation",
            "risk_profile": "standard",
            "platform_authorized": True,
            "business_authorized": False,
        })
        self.assertEqual("reuse", result)

    def test_tiered_02_platform_permission_cannot_authorize_production_deletion(self):
        validate = getattr(self.validator, "validate_confirmation_lease", None)
        self.assertTrue(callable(validate), "layered authorization behavior is not implemented")
        with self.assertRaisesRegex(AssertionError, "business/production authorization"):
            validate(self._valid_lease(), {
                "action": "production-deletion",
                "artifact_revision": 2,
                "artifact_sha256": "a" * 64,
                "scope": "approved source implementation",
                "risk_profile": "strict",
                "platform_authorized": True,
                "business_authorized": False,
            })

    def test_tiered_03_ai_proposed_user_approved_provenance_is_preserved(self):
        validate = getattr(self.validator, "validate_decision_source", None)
        self.assertTrue(callable(validate), "decision provenance behavior is not implemented")
        self.assertEqual(
            "ai-proposed/user-approved",
            validate("ai-proposed/user-approved"),
        )
        with self.assertRaisesRegex(AssertionError, "decision_source"):
            validate("user-originated-from-ai-proposal")

    def test_tiered_04_mechanical_low_ambiguity_blocks_instead_of_designing(self):
        validate = getattr(self.validator, "validate_capability_action", None)
        self.assertTrue(callable(validate), "capability authority behavior is not implemented")
        self.assertEqual(
            "BLOCKED",
            validate("mechanical-low", "bounded-edit", ambiguity=True),
        )

    def test_tiered_05_high_review_detects_copy_field_loss_after_executor_pass(self):
        validate = getattr(self.validator, "validate_high_review_evidence", None)
        self.assertTrue(callable(validate), "High Review behavior is not implemented")
        evidence = self._valid_review_evidence()
        evidence["copy_fields"]["observed"] = ["id"]
        with self.assertRaisesRegex(AssertionError, "copy-field loss"):
            validate(evidence)

    def test_tiered_06_high_review_requires_independent_adversarial_probe(self):
        validate = getattr(self.validator, "validate_high_review_evidence", None)
        self.assertTrue(callable(validate), "independent probe behavior is not implemented")
        evidence = self._valid_review_evidence()
        evidence["independent_probe"] = None
        with self.assertRaisesRegex(AssertionError, "independent.*probe"):
            validate(evidence)

    def test_tiered_07_high_review_traces_claim_to_runtime_mechanism(self):
        validate = getattr(self.validator, "validate_high_review_evidence", None)
        self.assertTrue(callable(validate), "claim-to-mechanism behavior is not implemented")
        evidence = self._valid_review_evidence()
        evidence["claims"][0]["mechanism"] = ""
        with self.assertRaisesRegex(AssertionError, "claim-to-mechanism"):
            validate(evidence)

    def test_tiered_08_same_product_instances_cannot_self_review(self):
        contract = self._schema5_contract()
        self.validator.validate_legacy_handoff_contract(
            contract, "same-product-distinct-instance"
        )
        contract["independent_reviewer_assignment"]["agent_instance_id"] = "codex-executor-01"
        with self.assertRaisesRegex(AssertionError, "instance"):
            self.validator.validate_legacy_handoff_contract(
                contract, "same-instance-self-review"
            )

    def test_tiered_09_single_correction_creates_candidate_without_promotion(self):
        evaluate = getattr(self.validator, "evaluate_learning_candidate", None)
        self.assertTrue(callable(evaluate), "Learning Candidate behavior is not implemented")
        result = evaluate({
            "severity": "low",
            "scope": "task-local",
            "independent_reproductions": 1,
            "event_kind": "wording-correction",
        })
        self.assertTrue(result["candidate_created"])
        self.assertFalse(result["proposal_allowed"])
        self.assertFalse(result["implementation_allowed"])

    def test_tiered_10_high_severity_candidate_is_proposal_only_without_approval(self):
        evaluate = getattr(self.validator, "evaluate_learning_candidate", None)
        self.assertTrue(callable(evaluate), "Learning Candidate promotion behavior is not implemented")
        result = evaluate({
            "severity": "high",
            "scope": "global",
            "independent_reproductions": 1,
            "event_kind": "false-pass",
            "openspec_approval": False,
        })
        self.assertTrue(result["proposal_allowed"])
        self.assertFalse(result["implementation_allowed"])


    def _lease_artifact_text(
        self, owner_instance_id="codex-control-01", risk_profile="standard",
        decision_source="ai-proposed/user-approved",
    ):
        return (
            "<!-- COOP_CONFIRMATION_LEASE_START -->\n"
            "```yaml\n"
            "decision_id: decision-001\n"
            "artifact_revision: 2\n"
            f"artifact_sha256: {'a' * 64}\n"
            "approved_scope: approved source implementation\n"
            "approved_actions:\n"
            "  - run-safe-tests\n"
            f"risk_profile: {risk_profile}\n"
            f"decision_source: {decision_source}\n"
            f"owner_instance_id: {owner_instance_id}\n"
            "status: valid\n"
            "invalidation_conditions:\n"
            "  - scope-change\n"
            "```\n"
            "<!-- COOP_CONFIRMATION_LEASE_END -->\n"
        )

    def test_schema5_runtime_validates_confirmation_lease_artifact(self):
        validate = getattr(
            self.validator, "_validate_legacy_confirmation_lease_artifact", None
        )
        self.assertTrue(callable(validate), "runtime lease artifact validation is not implemented")
        data = self._schema5_contract()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / data["confirmation_lease"]["path"]
            target.parent.mkdir(parents=True)
            target.write_text(self._lease_artifact_text(), encoding="utf-8")
            data["confirmation_lease"]["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
            validate(data, root, "valid-lease")
            target.write_text(self._lease_artifact_text("wrong-owner"), encoding="utf-8")
            data["confirmation_lease"]["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
            with self.assertRaisesRegex(AssertionError, "owner_instance_id"):
                validate(data, root, "wrong-owner")
            target.write_text(self._lease_artifact_text(risk_profile="strict"), encoding="utf-8")
            data["confirmation_lease"]["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
            with self.assertRaisesRegex(AssertionError, "risk_profile"):
                validate(data, root, "wrong-risk")
            target.write_text(self._lease_artifact_text(decision_source="revoked"), encoding="utf-8")
            data["confirmation_lease"]["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
            with self.assertRaisesRegex(AssertionError, "revoked|valid"):
                validate(data, root, "revoked-lease")

    def test_schema5_high_review_artifact_requires_mechanism_sections(self):
        validate = getattr(self.validator, "validate_high_review_artifact_text", None)
        self.assertTrue(callable(validate), "runtime High Review artifact validation is not implemented")
        incomplete = schema5_evidence_manifest("batch-review", "pass", high_review=False)
        with self.assertRaisesRegex(AssertionError, "actual diff|production wiring|claim-to-mechanism|independent"):
            validate(incomplete, "incomplete-review")
        complete = incomplete + (
            "\nActual files and complete diff inspected\n"
            "Copy/transform/production wiring trace\n"
            "Critical reruns\n"
            "Claim-to-mechanism support\n"
            "Independent adversarial probe\n"
        )
        validate(complete, "complete-review")

    def test_schema4_inventory_blocks_active_and_allows_complete_history(self):
        inventory = getattr(self.validator, "inventory_active_schema4_statuses", None)
        self.assertTrue(callable(inventory), "schema-4 drain inventory is not implemented")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            status = root / "docs" / "agent-collab" / "legacy" / "status.md"
            status.parent.mkdir(parents=True)
            active = schema4_contract(
                self.validator,
                self.handoff,
                lifecycle_state="ready-for-execution",
                next_owner="external-agent",
            )
            status.write_text(
                render_handoff_contract(self.validator, active), encoding="utf-8"
            )
            self.assertEqual([status.resolve()], inventory([root]))

            complete = schema4_contract(
                self.validator,
                self.handoff,
                lifecycle_state="complete",
                current_batch=2,
                last_review_result="pass",
                final_verification="pass",
                final_review_result="pass",
                attempt_report_artifact=artifact("report.md"),
                last_review_artifact=artifact("review.md"),
                final_verification_artifact=artifact("verification.md"),
                final_review_artifact=artifact("final-review.md"),
                next_owner="user",
            )
            status.write_text(
                render_handoff_contract(self.validator, complete), encoding="utf-8"
            )
            self.assertEqual([], inventory([root]))


    def test_schema5_revoked_lease_blocks_and_cannot_be_reactivated(self):
        before = self._schema5_contract()
        before["confirmation_lease_status"] = "valid"
        after = dict(before)
        after.update(
            lifecycle_state="blocked",
            contract_revision=before["contract_revision"] + 1,
            last_review_result="blocked",
            last_review_artifact=artifact("docs/review/revoked-lease.md"),
            blocked_reason="user revoked the prior decision",
            blocker_owner="user",
            resume_condition="create a new explicitly authorized contract and Lease",
            next_owner="user",
            confirmation_lease_status="revoked",
        )
        self.validator._validate_legacy_transition(before, after, "revoke-lease")
        recovered = dict(after)
        recovered.update(
            lifecycle_state="ready-for-execution",
            contract_revision=after["contract_revision"] + 1,
            attempt=after["attempt"] + 1,
            last_review_result="not-run",
            last_review_artifact=None,
            blocked_reason=None,
            blocker_owner="none",
            resume_condition=None,
            next_owner="external-agent",
            confirmation_lease_status="valid",
        )
        with self.assertRaisesRegex(AssertionError, "revoked|new.*Lease|reactivat"):
            self.validator._validate_legacy_transition(
                after, recovered, "reactivate-old-lease"
            )

    def _load_role_first_forward_runner(self):
        runner_path = ROOT / "tests" / "run_role_first_review_forward_tests.py"
        self.assertTrue(runner_path.is_file(), "role-first forward runner is required")
        spec = importlib.util.spec_from_file_location(
            "role_first_review_forward_tests", runner_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_role_first_forward_fixture_withholds_expected_from_model_prompt(self):
        runner = self._load_role_first_forward_runner()
        self.assertTrue(
            hasattr(runner, "compare_case_expected"),
            "forward runner must support private contract alternatives",
        )
        fixture_path = (
            ROOT / "tests" / "fixtures" / "role-first-review-routing-cases.json"
        )
        schema_path = (
            ROOT
            / "tests"
            / "fixtures"
            / "role-first-review-routing-output.schema.json"
        )
        cases = json.loads(fixture_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        runner.validate_fixture(cases)
        runner.validate_schema_document(schema)
        self.assertEqual(len(cases), 6)
        for case in cases:
            public = runner.public_case(case)
            self.assertEqual(set(public), {"id", "prompt"})
            self.assertNotIn("expected", public)
            self.assertNotIn("accepted_alternatives", public)
            prompt = runner.build_model_prompt(public)
            self.assertNotIn(json.dumps(case["expected"], sort_keys=True), prompt)
            self.assertNotIn(
                json.dumps(case["accepted_alternatives"], sort_keys=True), prompt
            )

        generic = copy.deepcopy(cases[0]["expected"])
        generic["reviewer_product"] = "antigravity-cli"
        self.assertEqual(runner.compare_case_expected(cases[0], generic), [])
        wrong_role = dict(generic, reviewer_role="advisory-reviewer")
        self.assertIn(
            "reviewer_role mismatch",
            runner.compare_case_expected(cases[0], wrong_role),
        )

    def test_role_first_forward_runner_injects_reviewed_classification(self):
        runner = self._load_role_first_forward_runner()
        self.assertTrue(
            hasattr(runner, "load_review_classification"),
            "forward runner must load the reviewed classification block",
        )
        self.assertTrue(
            hasattr(runner, "build_project_instructions"),
            "forward runner must inject the reviewed block into startup instructions",
        )
        companion = ROOT.parent / "codex-brief-antigravity-review"
        classification = runner.load_review_classification(ROOT, companion)
        instructions = runner.build_project_instructions(classification)
        self.assertIn(classification, instructions)
        self.assertIn("gate-bearing", classification)
        self.assertIn("advisory-not-gate-bearing", classification)
        self.assertNotIn("accepted_alternatives", instructions)

    def test_role_first_forward_output_fails_closed_on_shape_and_substitution(self):
        runner = self._load_role_first_forward_runner()
        observed = {
            "route_result": "actionable",
            "review_purpose": {
                "object": "current implementation plan",
                "decision": "decide PASS or BLOCKED",
            },
            "reviewer_product": "codex",
            "reviewer_role": "independent-reviewer",
            "capability_profile": "control-plane-high",
            "independence_requirement": "new instance distinct from author and executor",
            "result_authority": "governed-review-evidence",
            "blocker_owner": "none",
            "resume_condition": None,
        }
        self.assertEqual(runner.validate_observed(observed), observed)
        for mutation in (
            {**observed, "extra": True},
            {key: value for key, value in observed.items() if key != "review_purpose"},
        ):
            with self.assertRaises(runner.ProbeFailure):
                runner.validate_observed(mutation)
        expected = {
            "route_result": "actionable",
            "reviewer_product": "pi",
            "reviewer_role": "advisory-reviewer",
            "capability_profile": "control-plane-high",
            "result_authority": "advisory-input",
            "blocker_owner": "none",
        }
        substituted = dict(observed)
        substituted.update(expected, reviewer_product="codex")
        self.assertIn("reviewer_product mismatch", runner.compare_expected(expected, substituted))

    def test_role_first_forward_semantics_reject_same_instance_and_incomplete_block(self):
        runner = self._load_role_first_forward_runner()
        same_instance = {
            "route_result": "actionable",
            "review_purpose": {
                "object": "current implementation",
                "decision": "decide the required High Review gate",
            },
            "reviewer_product": "pi",
            "reviewer_role": "independent-reviewer",
            "capability_profile": "control-plane-high",
            "independence_requirement": "same instance pi-executor-01",
            "result_authority": "governed-review-evidence",
            "blocker_owner": "none",
            "resume_condition": None,
        }
        with self.assertRaises(runner.ProbeFailure):
            runner.validate_observed(same_instance)
        blocked = dict(same_instance)
        blocked.update(route_result="blocked", blocker_owner="control-plane")
        with self.assertRaises(runner.ProbeFailure):
            runner.validate_observed(blocked)
        blocked["resume_condition"] = "open a distinct Pi reviewer session"
        self.assertEqual(runner.validate_observed(blocked), blocked)

    def test_role_first_forward_summary_is_sanitized_and_private(self):
        runner = self._load_role_first_forward_runner()
        observed = {
            "route_result": "blocked",
            "review_purpose": {
                "object": "current implementation",
                "decision": "decide required independent Review",
            },
            "reviewer_product": "pi",
            "reviewer_role": "independent-reviewer",
            "capability_profile": "control-plane-high",
            "independence_requirement": "distinct reviewer unavailable",
            "result_authority": "governed-review-evidence",
            "blocker_owner": "control-plane",
            "resume_condition": "open a distinct Pi reviewer session",
        }
        record = runner.sanitize_case_record("same_pi_session", observed, True)
        self.assertEqual(set(record), runner.SUMMARY_RECORD_KEYS)
        self.assertNotIn("review_purpose", record)
        self.assertNotIn("resume_condition", record)
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "summary.json"
            runner.write_private_summary(output, {"cases": [record]})
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o600)


class ClosedLoopRuntimeRoutingTests(unittest.TestCase):
    def test_closed_loop_runtime_routing_fixture(self):
        approved = (ROOT / "references" / "approved-implementation-workflow.md").read_text(encoding="utf-8")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        combined = "\n".join((approved, skill))
        for phrase in ("闭环推进", "继续闭环", "按推荐方案推进", "完成后统一 Review"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, combined)
        self.assertIn(
            "After an accepted recommendation, continue without confirming the same option",
            approved,
        )
        self.assertIn("asking whether to start the next approved safe step again", approved)
        self.assertNotIn("confirm A again", approved)
        self.assertIn("implementation detail", approved)
        self.assertIn("obvious minimal", approved)
        self.assertIn("formal A/B/C options", approved)

    def test_runtime_advice_is_non_authoritative_and_non_marker(self):
        routing = (ROOT / "references" / "agent-capability-routing.md").read_text(encoding="utf-8")
        handoff = (ROOT / "references" / "handoff-contract.md").read_text(encoding="utf-8")
        normalized = " ".join(routing.split())
        for row in (
            "Ordinary OpenSpec revision, `writing-plans`, routine read-only Review | Codex, high",
            "Cross-Track work, complex security boundary, difficult Plan Preflight, final gate-bearing Review | Codex, xhigh",
            "Closed contract and clear-scope cohesive implementation | Luna Max, recommended reasoning strength chosen by the current runtime",
            "Small mechanical modification | Current capable lower-cost model",
        ):
            with self.subTest(row=row):
                self.assertIn(" ".join(row.split()), normalized)
        self.assertEqual(routing.count("运行环境建议："), 1)
        advice_block = routing.split("运行环境建议：", 1)[1].split("```", 1)[0]
        for field in (
            "目标 Session：",
            "推荐模型：",
            "推理强度：",
            "切换原因：",
            "可复制任务提示词：",
            "完成后切回：",
        ):
            with self.subTest(field=field):
                self.assertEqual(advice_block.count(field), 1)
        for phrase in (
            "If the current model is sufficient, no runtime advice is emitted",
            "No block is required when no switch occurs",
            "Model/reasoning metadata never changes",
            "Luna Max is advice only",
            "approval",
            "authority",
            "PASS",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, routing)
        marker_start = "<!-- COOP_HANDOFF_CONTRACT_START -->"
        marker_end = "<!-- COOP_HANDOFF_CONTRACT_END -->"
        self.assertIn(marker_start, handoff)
        self.assertIn(marker_end, handoff)
        marker = handoff.split(marker_start, 1)[1].split(marker_end, 1)[0]
        self.assertNotIn("运行环境建议：", marker)
        self.assertIn("schema_version: 6", marker)
        self.assertIn("An old schema-6 Handoff without this optional block remains valid.", handoff)

    def test_closed_loop_preserves_existing_gates(self):
        approved = (ROOT / "references" / "approved-implementation-workflow.md").read_text(encoding="utf-8")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        normalized = " ".join(approved.split())
        for phrase in (
            "Plan Preflight",
            "Step Evidence",
            "implementation Review",
            "final verification",
            "Final Review",
            "Completion Contract",
            "smallest adequate design and artifact set",
            "reuse existing rules, templates, validators, and tests first",
            "Do not add a framework, schema, registry, runner, or ledger when direct mechanisms work",
            "For the current task, TDD covers changed acceptance, changed contracts, and credible regressions",
            "Do not create or run unrelated tests without an existing gate or demonstrated blast radius",
            "broader relevant gates remain mandatory",
            "If support machinery exceeds the change itself, simplify",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(" ".join(phrase.split()), normalized)
        self.assertIn(
            "For proportional implementation decisions, read `references/approved-implementation-workflow.md`.",
            skill,
        )


if __name__ == "__main__":
    unittest.main()
