from __future__ import annotations

import importlib
import inspect
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "scripts" / "build_codex_plugin.py"
SKILLSMP_BUILDER_PATH = ROOT / "scripts" / "build_skillsmp_adapter.py"
VALIDATOR_PATH = ROOT / "scripts" / "validate_distribution.py"
SKILL_NAME = "openspec-superpower-change"
ADAPTER_RELATIVE_PATH = Path("skills") / SKILL_NAME / "SKILL.md"


REPOSITORY_MUTATION_OBSERVER_SCRIPT = r'''
def install_repository_mutation_observer(root):
    repository_identities = set()
    for candidate in [root, *root.rglob("*")]:
        metadata = candidate.stat(follow_symlinks=False)
        repository_identities.add((metadata.st_dev, metadata.st_ino))

    root_path = os.path.normpath(os.path.abspath(os.fspath(root)))
    mutation_events = []
    write_open_flags = 0
    for flag_name in ("O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "O_APPEND"):
        write_open_flags |= getattr(os, flag_name, 0)

    def descriptor_targets_repository(directory_fd):
        if directory_fd is None or directory_fd == -1:
            return False
        try:
            metadata = os.fstat(directory_fd)
        except OSError:
            return False
        return (metadata.st_dev, metadata.st_ino) in repository_identities

    def descriptor_path(directory_fd):
        if directory_fd is None or directory_fd == -1:
            return None
        for descriptor_root in ("/proc/self/fd", "/dev/fd"):
            try:
                return os.readlink(f"{descriptor_root}/{directory_fd}")
            except OSError:
                continue
        return None

    def path_targets_repository(path, directory_fd=None):
        if isinstance(path, int):
            return descriptor_targets_repository(path)
        try:
            raw_path = os.fsdecode(path)
        except TypeError:
            return False
        if directory_fd is not None and directory_fd != -1:
            if descriptor_targets_repository(directory_fd):
                return True
            base_path = descriptor_path(directory_fd)
            if base_path is None:
                return False
            raw_path = os.path.join(base_path, raw_path)
        candidate = os.path.normpath(
            raw_path if os.path.isabs(raw_path) else os.path.abspath(raw_path)
        )
        try:
            return os.path.commonpath((root_path, candidate)) == root_path
        except ValueError:
            return False

    def record_mutation(event, *targets, flags=None):
        if not any(
            path_targets_repository(path, directory_fd)
            for path, directory_fd in targets
        ):
            return
        record = {"event": event}
        if flags is not None:
            record["flags"] = flags
        mutation_events.append(record)

    def audit_repository_mutations(event, arguments):
        if event in {"os.mkdir", "os.rmdir", "os.remove", "os.unlink"}:
            path = arguments[0]
            directory_fd = arguments[2] if event == "os.mkdir" else arguments[1]
            record_mutation(event, (path, directory_fd))
        elif event in {"os.rename", "os.replace"}:
            source, destination, source_fd, destination_fd = arguments[:4]
            record_mutation(
                event,
                (source, source_fd),
                (destination, destination_fd),
            )
        elif event == "os.link":
            source, destination, source_fd, destination_fd = arguments[:4]
            record_mutation(
                event,
                (source, source_fd),
                (destination, destination_fd),
            )
        elif event == "os.symlink":
            destination = arguments[1]
            directory_fd = arguments[2]
            record_mutation(event, (destination, directory_fd))
        elif event == "os.chmod":
            path, _, directory_fd = arguments[:3]
            record_mutation(event, (path, directory_fd))
        elif event == "open":
            path, mode, flags = arguments[:3]
            writes = bool(flags & write_open_flags) or (
                isinstance(mode, str) and any(marker in mode for marker in "wax+")
            )
            if writes:
                record_mutation(event, (path, None), flags=flags)

    def check_link_direction_coverage():
        root_fd = os.open(root, os.O_RDONLY)
        outside_path = os.fspath(root.parent / "outside-link-audit-target")
        scenarios = {
            "repo_to_outside": ("SKILL.md", outside_path, root_fd, -1),
            "outside_to_repo": (outside_path, "link-target", -1, root_fd),
        }
        coverage = {}
        try:
            for direction, arguments in scenarios.items():
                mutation_events.clear()
                audit_repository_mutations("os.link", arguments)
                coverage[direction] = mutation_events == [{"event": "os.link"}]
        finally:
            os.close(root_fd)
            mutation_events.clear()
        return coverage

    link_direction_coverage = check_link_direction_coverage()
    sys.addaudithook(audit_repository_mutations)
    return mutation_events, link_direction_coverage

mutation_events, link_direction_coverage = install_repository_mutation_observer(root)
'''


def copy_tree(source: Path, destination: Path) -> Path:
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
    )
    return destination


def write_adapter(root: Path, content: bytes | None = None) -> Path:
    adapter = root / ADAPTER_RELATIVE_PATH
    adapter.parent.mkdir(parents=True, exist_ok=True)
    adapter.write_bytes(content if content is not None else (root / "SKILL.md").read_bytes())
    return adapter


def remove_adapter(root: Path) -> None:
    adapter_root = root / ADAPTER_RELATIVE_PATH.parent
    if adapter_root.is_symlink():
        adapter_root.unlink()
    elif adapter_root.exists():
        shutil.rmtree(adapter_root)


def validate_adapter_in_subprocess(root: Path) -> list[str]:
    script = """
import json
import sys
from pathlib import Path
from scripts import validate_distribution

print(json.dumps(validate_distribution.validate_skillsmp_adapter(Path(sys.argv[1]))))
"""
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-c", script, str(root)],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        raise AssertionError(
            "bounded adapter-validator subprocess failed: "
            + result.stdout
            + result.stderr
        )
    return json.loads(result.stdout)


def validate_adapter_after_parent_rebind_in_subprocess(
    root: Path, outside: Path, rebind_after_call: int = 1
) -> dict[str, object]:
    script = """
import json
import sys
from pathlib import Path
from unittest import mock
from scripts import build_skillsmp_adapter as builder
from scripts import validate_distribution

root = Path(sys.argv[1])
outside = Path(sys.argv[2])
output = root / "skills" / builder.SKILL_NAME
displaced = root.parent / "displaced-adapter"
original_open = getattr(validate_distribution, "_open_adapter_directory", None)
rebind_after_call = int(sys.argv[3])
rebound = False
calls = 0

def open_with_parent_rebind(candidate_root):
    global calls, rebound
    bound = original_open(candidate_root)
    calls += 1
    if calls == rebind_after_call:
        output.rename(displaced)
        output.symlink_to(outside, target_is_directory=True)
        rebound = True
    return bound

if original_open is None:
    errors = []
else:
    with mock.patch.object(
        validate_distribution,
        "_open_adapter_directory",
        side_effect=open_with_parent_rebind,
    ):
        errors = validate_distribution.validate_skillsmp_adapter(root)

print(json.dumps({
    "errors": errors,
    "rebound": rebound,
    "calls": calls,
    "seam_missing": original_open is None,
}))
"""
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            script,
            str(root),
            str(outside),
            str(rebind_after_call),
        ],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        raise AssertionError(
            "bounded adapter parent-rebind subprocess failed: "
            + result.stdout
            + result.stderr
        )
    return json.loads(result.stdout)


def reject_adapter_build_in_subprocess(root: Path) -> str:
    script = """
import json
import sys
from pathlib import Path

try:
    from scripts import build_skillsmp_adapter
except Exception as error:
    print(json.dumps({"result": "import-failed", "detail": repr(error)}))
    raise SystemExit(20)

try:
    build_skillsmp_adapter.build(Path(sys.argv[1]))
except ValueError as error:
    print(json.dumps({"result": "rejected", "detail": str(error)}))
except Exception as error:
    print(json.dumps({"result": "unexpected-error", "detail": repr(error)}))
    raise SystemExit(21)
else:
    print(json.dumps({"result": "accepted"}))
    raise SystemExit(22)
"""
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-c", script, str(root)],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        raise AssertionError(
            "bounded adapter-builder subprocess did not deliberately reject: "
            + result.stdout
            + result.stderr
        )
    payload = json.loads(result.stdout)
    if payload.get("result") != "rejected":
        raise AssertionError(f"adapter builder did not reject special state: {payload}")
    return str(payload["detail"])


def run_builder_install_probe_in_subprocess(
    root: Path, scenario: str, outside: Path | None = None
) -> dict[str, object]:
    script = """
import json
import inspect
import os
import stat
import sys
import tempfile
from pathlib import Path
from unittest import mock
from scripts import build_skillsmp_adapter as builder

root = Path(sys.argv[1])
scenario = sys.argv[2]
outside = Path(sys.argv[3]) if len(sys.argv) > 3 else None
skills = root / "skills"
source = root / "SKILL.md"
original_install = builder._install_staged_adapter
calls = 0
lure_prepared = False
external_before = None
injection_performed = False

def identity_snapshot(candidate):
    result = {}
    for path in [candidate, *sorted(candidate.rglob("*"))]:
        relative = "." if path == candidate else path.relative_to(candidate).as_posix()
        metadata = path.stat(follow_symlinks=False)
        record = [
            metadata.st_dev,
            metadata.st_ino,
            stat.S_IMODE(metadata.st_mode),
            metadata.st_nlink,
        ]
        if path.is_symlink():
            result[relative] = ["symlink", *record, os.readlink(path)]
        elif path.is_dir():
            result[relative] = ["directory", *record]
        elif path.is_file():
            result[relative] = ["file", *record, path.read_bytes().hex()]
        else:
            result[relative] = ["special", *record, stat.S_IFMT(metadata.st_mode)]
    return result

def install_with_probe(skills_fd, stage_name, output_name):
    global calls, lure_prepared, external_before, injection_performed
    if not isinstance(skills_fd, int) or isinstance(skills_fd, bool):
        raise TypeError("_install_staged_adapter requires a skills directory descriptor")
    if not isinstance(stage_name, str) or not stage_name.startswith(builder.STAGE_PREFIX):
        raise TypeError("_install_staged_adapter requires the reserved stage entry name")
    if output_name != builder.SKILL_NAME:
        raise TypeError("_install_staged_adapter requires the canonical output entry name")
    calls += 1
    if calls == 1:
        if scenario == "parent-rebind":
            lure = outside / stage_name
            lure.mkdir()
            (lure / "SKILL.md").write_bytes(source.read_bytes())
            lure_prepared = True
            external_before = identity_snapshot(outside)
            displaced = root.parent / "displaced-skills"
            skills.rename(displaced)
            skills.symlink_to(outside, target_is_directory=True)
        elif scenario == "source-replace":
            source.rename(root.parent / "captured-source.md")
            source.write_bytes(b"concurrently replaced canonical source\\n")
        elif scenario == "source-inplace":
            source.write_bytes(b"concurrently modified canonical source\\n")
        elif scenario == "stage-residue":
            residue = skills / f"{builder.STAGE_PREFIX}injected-review"
            residue.mkdir()
            (residue / "evidence.txt").write_bytes(b"unknown stage residue\\n")
        elif scenario == "recovery-residue":
            residue = skills / f"{builder.RECOVERY_PREFIX}injected-review"
            residue.mkdir()
            (residue / "evidence.txt").write_bytes(b"unknown recovery residue\\n")
        else:
            raise AssertionError(f"unknown install probe: {scenario}")
        injection_performed = True
    return original_install(skills_fd, stage_name, output_name)

legacy_install = tuple(inspect.signature(original_install).parameters) != (
    "skills_fd",
    "stage_name",
    "output_name",
)
if scenario == "parent-rebind" and legacy_install:
    # Fail-only witness: prove the legacy Path seam follows the rebound parent.
    stage = Path(tempfile.mkdtemp(prefix=builder.STAGE_PREFIX, dir=skills))
    (stage / "SKILL.md").write_bytes(source.read_bytes())
    lure = outside / stage.name
    lure.mkdir()
    (lure / "SKILL.md").write_bytes(source.read_bytes())
    lure_prepared = True
    injection_performed = True
    external_before = identity_snapshot(outside)
    skills.rename(root.parent / "displaced-skills")
    skills.symlink_to(outside, target_is_directory=True)
    calls = 1
    try:
        original_install(skills / stage.name, skills / builder.SKILL_NAME)
    except Exception as error:
        result = {
            "success": False,
            "error": f"{type(error).__name__}: {error}",
            "calls": calls,
        }
    else:
        result = {
            "success": True,
            "generated": str(skills / builder.SKILL_NAME / "SKILL.md"),
            "calls": calls,
        }
else:
    with mock.patch.object(
        builder,
        "_install_staged_adapter",
        side_effect=install_with_probe,
    ):
        try:
            generated = builder.build(root)
        except Exception as error:
            result = {
                "success": False,
                "error": f"{type(error).__name__}: {error}",
                "calls": calls,
            }
        else:
            result = {"success": True, "generated": str(generated), "calls": calls}

if scenario == "parent-rebind":
    result["lure_prepared"] = lure_prepared
    result["external_unchanged"] = (
        external_before is not None and identity_snapshot(outside) == external_before
    )
result["injection_performed"] = injection_performed

print(json.dumps(result))
"""
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [sys.executable, "-c", script, str(root), scenario]
    if outside is not None:
        command.append(str(outside))
    result = subprocess.run(
        command,
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        raise AssertionError(
            "bounded install-boundary subprocess failed: "
            + result.stdout
            + result.stderr
        )
    return json.loads(result.stdout)


def run_builder_without_capability_in_subprocess(
    root: Path, capability: str
) -> dict[str, object]:
    script = """
import json
import os
import sys
from pathlib import Path

root = Path(sys.argv[1])
capability = sys.argv[2]
if capability in {"O_NOFOLLOW", "O_DIRECTORY"}:
    if hasattr(os, capability):
        delattr(os, capability)
elif capability == "dir_fd":
    os.supports_dir_fd = set()
else:
    raise AssertionError(f"unknown capability probe: {capability}")
from scripts import build_skillsmp_adapter as builder
""" + REPOSITORY_MUTATION_OBSERVER_SCRIPT + """
try:
    generated = builder.build(root)
except Exception as error:
    result = {
        "success": False,
        "error": f"{type(error).__name__}: {error}",
    }
else:
    result = {
        "success": True,
        "generated": str(generated),
    }
result.update({
    "link_direction_coverage": link_direction_coverage,
    "mutation_events": mutation_events,
})
print(json.dumps(result))
"""
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-c", script, str(root), capability],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        raise AssertionError(
            "bounded capability-absence subprocess failed: "
            + result.stdout
            + result.stderr
        )
    return json.loads(result.stdout)


def run_builder_after_root_rebind_in_subprocess(
    root: Path, replacement: Path
) -> dict[str, object]:
    script = """
import json
import os
import stat
import sys
from pathlib import Path
from unittest import mock
from scripts import build_skillsmp_adapter as builder

root = Path(sys.argv[1])
replacement = Path(sys.argv[2])
displaced = root.parent / "displaced-original-root"
original_read = getattr(builder, "_read_source_snapshot", None)
root_metadata = root.stat(follow_symlinks=False)
root_identity = (root_metadata.st_dev, root_metadata.st_ino)
calls = 0
rebound = False
bound_original = True
replacement_before = None

def identity_snapshot(candidate):
    result = {}
    for path in [candidate, *sorted(candidate.rglob("*"))]:
        relative = "." if path == candidate else path.relative_to(candidate).as_posix()
        metadata = path.stat(follow_symlinks=False)
        record = [
            metadata.st_dev,
            metadata.st_ino,
            stat.S_IMODE(metadata.st_mode),
            metadata.st_nlink,
        ]
        if path.is_symlink():
            result[relative] = ["symlink", *record, os.readlink(path)]
        elif path.is_dir():
            result[relative] = ["directory", *record]
        elif path.is_file():
            result[relative] = ["file", *record, path.read_bytes().hex()]
        else:
            result[relative] = ["special", *record, stat.S_IFMT(metadata.st_mode)]
    return result

def read_with_root_rebind(root_fd, source_name):
    global calls, rebound, bound_original, replacement_before
    if not isinstance(root_fd, int) or isinstance(root_fd, bool):
        raise TypeError("_read_source_snapshot requires a root directory descriptor")
    if source_name != "SKILL.md":
        raise TypeError("_read_source_snapshot requires the canonical source entry name")
    metadata = os.fstat(root_fd)
    bound_original = bound_original and (
        metadata.st_dev,
        metadata.st_ino,
    ) == root_identity
    snapshot = original_read(root_fd, source_name)
    calls += 1
    if calls == 1:
        root.rename(displaced)
        replacement.rename(root)
        replacement_before = identity_snapshot(root)
        rebound = True
    return snapshot

if original_read is None:
    result = {
        "success": False,
        "error": "missing _read_source_snapshot(root_fd, source_name)",
        "seam_missing": True,
        "calls": calls,
    }
else:
    with mock.patch.object(
        builder,
        "_read_source_snapshot",
        side_effect=read_with_root_rebind,
    ):
        try:
            generated = builder.build(root)
        except Exception as error:
            result = {
                "success": False,
                "error": f"{type(error).__name__}: {error}",
                "seam_missing": False,
                "calls": calls,
            }
        else:
            result = {
                "success": True,
                "generated": str(generated),
                "seam_missing": False,
                "calls": calls,
            }

result["rebound"] = rebound
result["bound_original"] = bound_original
result["replacement_unchanged"] = (
    rebound
    and replacement_before is not None
    and identity_snapshot(root) == replacement_before
)
print(json.dumps(result))
"""
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-c", script, str(root), str(replacement)],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        raise AssertionError(
            "bounded repository-root rebind subprocess failed: "
            + result.stdout
            + result.stderr
        )
    return json.loads(result.stdout)


def run_builder_with_skills_mutation_trap_in_subprocess(
    root: Path,
) -> dict[str, object]:
    script = """
import json
import os
import sys
from pathlib import Path
from scripts import build_skillsmp_adapter as builder

root = Path(sys.argv[1])
""" + REPOSITORY_MUTATION_OBSERVER_SCRIPT + """
try:
    generated = builder.build(root)
except Exception as error:
    result = {
        "success": False,
        "error": f"{type(error).__name__}: {error}",
    }
else:
    result = {
        "success": True,
        "generated": str(generated),
    }
result.update({
    "link_direction_coverage": link_direction_coverage,
    "mutation_events": mutation_events,
})
print(json.dumps(result))
"""
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-c", script, str(root)],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        raise AssertionError(
            "bounded hard-link mutation-boundary subprocess failed: "
            + result.stdout
            + result.stderr
        )
    return json.loads(result.stdout)


def run_builder_recovery_commit_probe_in_subprocess(
    root: Path, scenario: str, replacement: Path | None = None
) -> dict[str, object]:
    script = """
import json
import os
import stat
import sys
from pathlib import Path
from unittest import mock
from scripts import build_skillsmp_adapter as builder

root = Path(sys.argv[1])
scenario = sys.argv[2]
replacement = Path(sys.argv[3]) if len(sys.argv) > 3 else None
skills = root / "skills"
source = root / "SKILL.md"
displaced_root = root.parent / "retained-original-root"
displaced_skills = root.parent / "retained-original-skills"
original_read = builder._read_source_snapshot
injected = False
recovery_observed = False
recovery_unlink_observed = False
commit_event_observed = None
retained_skills = skills
external_before = None
post_commit_scenarios = {
    "source-drift-after-commit",
    "output-drift-after-commit",
    "residue-after-commit",
    "root-rebind-after-commit",
    "skills-rebind-after-commit",
}

def identity_snapshot(candidate):
    result = {}
    for path in [candidate, *sorted(candidate.rglob("*"))]:
        relative = "." if path == candidate else path.relative_to(candidate).as_posix()
        metadata = path.stat(follow_symlinks=False)
        record = [
            metadata.st_dev,
            metadata.st_ino,
            stat.S_IMODE(metadata.st_mode),
            metadata.st_nlink,
        ]
        if path.is_symlink():
            result[relative] = ["symlink", *record, os.readlink(path)]
        elif path.is_dir():
            result[relative] = ["directory", *record]
        elif path.is_file():
            result[relative] = ["file", *record, path.read_bytes().hex()]
        else:
            result[relative] = ["special", *record, stat.S_IFMT(metadata.st_mode)]
    return result

old_output = skills / builder.SKILL_NAME
old_target = old_output / builder.TARGET_NAME
old_directory_metadata = old_output.stat(follow_symlinks=False)
old_target_metadata = old_target.stat(follow_symlinks=False)
old_identity = [
    old_directory_metadata.st_dev,
    old_directory_metadata.st_ino,
    stat.S_IMODE(old_directory_metadata.st_mode),
    old_target_metadata.st_dev,
    old_target_metadata.st_ino,
    stat.S_IMODE(old_target_metadata.st_mode),
    old_target_metadata.st_nlink,
    old_target.read_bytes().hex(),
]

def retained_recovery_names(root_fd):
    skills_fd = None
    try:
        skills_fd = os.open(
            "skills",
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
            dir_fd=root_fd,
        )
    except OSError:
        return []
    try:
        return sorted(
            name
            for name in os.listdir(skills_fd)
            if name.startswith(builder.RECOVERY_PREFIX)
        )
    finally:
        os.close(skills_fd)

def read_with_transaction_probe(root_fd, source_name):
    global injected, recovery_observed
    global retained_skills, external_before
    recovery_names = retained_recovery_names(root_fd)
    if recovery_names:
        recovery_observed = True
        if not injected:
            injected = True
            if scenario == "source-replace-before-commit":
                source.rename(root.parent / "captured-source-before-commit.md")
                source.write_bytes(b"replacement source before recovery commit\\n")
            elif scenario == "source-inplace-before-commit":
                source.write_bytes(b"in-place source drift before recovery commit\\n")
            elif scenario == "root-rebind-before-commit":
                if replacement is None:
                    raise AssertionError("root rebind requires a replacement tree")
                external_before = identity_snapshot(replacement)
                root.rename(displaced_root)
                replacement.rename(root)
                retained_skills = displaced_root / "skills"
            elif scenario == "skills-rebind-before-commit":
                if replacement is None:
                    raise AssertionError("skills rebind requires an external directory")
                external_before = identity_snapshot(replacement)
                skills.rename(displaced_skills)
                skills.symlink_to(replacement, target_is_directory=True)
                retained_skills = displaced_skills
            else:
                raise AssertionError(f"unknown pre-commit scenario: {scenario}")
    return original_read(root_fd, source_name)

skills_metadata = skills.stat(follow_symlinks=False)
skills_identity = (skills_metadata.st_dev, skills_metadata.st_ino)

def descriptor_matches_skills(directory_fd):
    if directory_fd is None or directory_fd == -1:
        return False
    try:
        metadata = os.fstat(directory_fd)
    except OSError:
        return False
    return (metadata.st_dev, metadata.st_ino) == skills_identity

def descriptor_path(directory_fd):
    if directory_fd is None or directory_fd == -1:
        return None
    for descriptor_root in ("/proc/self/fd", "/dev/fd"):
        try:
            return os.readlink(f"{descriptor_root}/{directory_fd}")
        except OSError:
            continue
    return None

def inject_after_recovery_commit_boundary():
    global retained_skills, external_before
    if scenario == "source-drift-after-commit":
        source.write_bytes(b"source changed after recovery commit\\n")
    elif scenario == "output-drift-after-commit":
        (retained_skills / builder.SKILL_NAME / builder.TARGET_NAME).write_bytes(
            b"generated output changed after recovery commit\\n"
        )
    elif scenario == "residue-after-commit":
        residue = retained_skills / f"{builder.STAGE_PREFIX}post-commit-review"
        residue.mkdir()
        (residue / "evidence.txt").write_bytes(b"post-commit residue\\n")
    elif scenario == "root-rebind-after-commit":
        if replacement is None:
            raise AssertionError("root rebind requires a replacement tree")
        external_before = identity_snapshot(replacement)
        root.rename(displaced_root)
        replacement.rename(root)
        retained_skills = displaced_root / "skills"
    elif scenario == "skills-rebind-after-commit":
        if replacement is None:
            raise AssertionError("skills rebind requires an external directory")
        external_before = identity_snapshot(replacement)
        skills.rename(displaced_skills)
        skills.symlink_to(replacement, target_is_directory=True)
        retained_skills = displaced_skills
    else:
        raise AssertionError(f"unknown post-commit scenario: {scenario}")

def audit_recovery_commit(event, arguments):
    global injected, recovery_observed, recovery_unlink_observed
    global commit_event_observed
    if scenario not in post_commit_scenarios:
        return
    if event in {"os.remove", "os.unlink"}:
        path, directory_fd = arguments[:2]
        parent = descriptor_path(directory_fd)
        if (
            os.fsdecode(path) == builder.TARGET_NAME
            and parent is not None
            and os.path.basename(parent).startswith(builder.RECOVERY_PREFIX)
        ):
            recovery_observed = True
            recovery_unlink_observed = True
        return
    if event != "os.rmdir" or injected:
        return
    path, directory_fd = arguments[:2]
    if (
        not isinstance(path, (str, bytes, os.PathLike))
        or not os.fsdecode(path).startswith(builder.RECOVERY_PREFIX)
        or not descriptor_matches_skills(directory_fd)
    ):
        return
    recovery_observed = True
    commit_event_observed = event
    injected = True
    inject_after_recovery_commit_boundary()

def run_build():
    try:
        generated = builder.build(root)
    except Exception as error:
        return {
            "success": False,
            "error": f"{type(error).__name__}: {error}",
        }
    return {"success": True, "generated": str(generated)}

if scenario in post_commit_scenarios:
    sys.addaudithook(audit_recovery_commit)
    result = run_build()
else:
    with mock.patch.object(
        builder,
        "_read_source_snapshot",
        side_effect=read_with_transaction_probe,
    ):
        result = run_build()

recoverable = []
canonical_matches_prior = False
if retained_skills.exists() and retained_skills.is_dir():
    for candidate in retained_skills.iterdir():
        if not (
            candidate.name == builder.SKILL_NAME
            or candidate.name.startswith(builder.RECOVERY_PREFIX)
        ):
            continue
        try:
            target = candidate / builder.TARGET_NAME
            directory_metadata = candidate.stat(follow_symlinks=False)
            target_metadata = target.stat(follow_symlinks=False)
            candidate_identity = [
                directory_metadata.st_dev,
                directory_metadata.st_ino,
                stat.S_IMODE(directory_metadata.st_mode),
                target_metadata.st_dev,
                target_metadata.st_ino,
                stat.S_IMODE(target_metadata.st_mode),
                target_metadata.st_nlink,
                target.read_bytes().hex(),
            ]
        except OSError:
            continue
        if candidate_identity == old_identity:
            recoverable.append(candidate.name)
            if candidate.name == builder.SKILL_NAME:
                canonical_matches_prior = True

canonical_exists = os.path.lexists(retained_skills / builder.SKILL_NAME)
recovery_matches_prior = any(
    name.startswith(builder.RECOVERY_PREFIX) for name in recoverable
)
prior_state_compensated = canonical_matches_prior or recovery_matches_prior

if scenario in {
    "root-rebind-before-commit",
    "root-rebind-after-commit",
} and replacement is not None:
    external_after = identity_snapshot(root)
elif scenario in {
    "skills-rebind-before-commit",
    "skills-rebind-after-commit",
} and replacement is not None:
    external_after = identity_snapshot(replacement)
else:
    external_after = None

result.update({
    "injected": injected,
    "recovery_observed": recovery_observed,
    "recovery_unlink_observed": recovery_unlink_observed,
    "commit_event_observed": commit_event_observed,
    "recoverable": recoverable,
    "canonical_exists": canonical_exists,
    "prior_state_compensated": prior_state_compensated,
    "external_unchanged": (
        external_before is None or external_after == external_before
    ),
})
print(json.dumps(result))
"""
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [sys.executable, "-c", script, str(root), scenario]
    if replacement is not None:
        command.append(str(replacement))
    result = subprocess.run(
        command,
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        raise AssertionError(
            "bounded recovery-commit subprocess failed: "
            + result.stdout
            + result.stderr
        )
    return json.loads(result.stdout)


def run_builder_capability_preflight_probe_in_subprocess(
    root: Path, capability: str
) -> dict[str, object]:
    script = """
import json
import os
import stat
import sys
from pathlib import Path

root = Path(sys.argv[1])
capability = sys.argv[2]
if capability == "supports_fd:listdir":
    os.supports_fd = set(os.supports_fd) - {os.listdir}
elif capability == "supports_follow_symlinks:stat":
    os.supports_follow_symlinks = set(os.supports_follow_symlinks) - {os.stat}
else:
    raise AssertionError(f"unknown capability probe: {capability}")
from scripts import build_skillsmp_adapter as builder

def identity_snapshot(candidate):
    result = {}
    for path in [candidate, *sorted(candidate.rglob("*"))]:
        relative = "." if path == candidate else path.relative_to(candidate).as_posix()
        metadata = path.stat(follow_symlinks=False)
        record = [
            metadata.st_dev,
            metadata.st_ino,
            stat.S_IMODE(metadata.st_mode),
            metadata.st_nlink,
        ]
        if path.is_symlink():
            result[relative] = ["symlink", *record, os.readlink(path)]
        elif path.is_dir():
            result[relative] = ["directory", *record]
        elif path.is_file():
            result[relative] = ["file", *record, path.read_bytes().hex()]
        else:
            result[relative] = ["special", *record, stat.S_IFMT(metadata.st_mode)]
    return result

before = identity_snapshot(root)
""" + REPOSITORY_MUTATION_OBSERVER_SCRIPT + """
try:
    generated = builder.build(root)
except Exception as error:
    result = {
        "success": False,
        "error": f"{type(error).__name__}: {error}",
    }
else:
    result = {"success": True, "generated": str(generated)}

result.update({
    "link_direction_coverage": link_direction_coverage,
    "mutation_events": mutation_events,
    "tree_unchanged": identity_snapshot(root) == before,
    "skills_exists": os.path.lexists(root / "skills"),
})
print(json.dumps(result))
"""
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-c", script, str(root), capability],
        cwd=root,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        raise AssertionError(
            "bounded capability-preflight subprocess failed: "
            + result.stdout
            + result.stderr
        )
    return json.loads(result.stdout)


def run_builder_rebound_recovery_diagnostic_probe_in_subprocess(
    root: Path, outside: Path
) -> dict[str, object]:
    script = """
import json
import os
import stat
import sys
from pathlib import Path
from unittest import mock
from scripts import build_skillsmp_adapter as builder

root = Path(sys.argv[1])
outside = Path(sys.argv[2])
skills = root / "skills"
displaced = root.parent / "retained-skills-with-recovery"
original_install = builder._install_staged_adapter
old_output = skills / builder.SKILL_NAME
old_target = old_output / builder.TARGET_NAME
old_directory_metadata = old_output.stat(follow_symlinks=False)
old_target_metadata = old_target.stat(follow_symlinks=False)
old_identity = [
    old_directory_metadata.st_dev,
    old_directory_metadata.st_ino,
    stat.S_IMODE(old_directory_metadata.st_mode),
    old_target_metadata.st_dev,
    old_target_metadata.st_ino,
    stat.S_IMODE(old_target_metadata.st_mode),
    old_target_metadata.st_nlink,
    old_target.read_bytes().hex(),
]
recovery_name = None
retained_identity = None
injected = False

def fail_install_after_rebind(skills_fd, stage_name, output_name):
    global recovery_name, retained_identity, injected
    retained = os.fstat(skills_fd)
    retained_identity = [retained.st_dev, retained.st_ino]
    recovery_names = sorted(
        name for name in os.listdir(skills_fd)
        if name.startswith(builder.RECOVERY_PREFIX)
    )
    if len(recovery_names) != 1:
        raise AssertionError(f"expected one retained recovery, got {recovery_names!r}")
    recovery_name = recovery_names[0]
    skills.rename(displaced)
    skills.symlink_to(outside, target_is_directory=True)
    injected = True
    raise OSError("PRIMARY_REBOUND_INSTALL_FAILURE")

with (
    mock.patch.object(
        builder,
        "_install_staged_adapter",
        side_effect=fail_install_after_rebind,
    ),
    mock.patch.object(
        builder,
        "_restore_recovery",
        side_effect=OSError("SECONDARY_RESTORE_FAILURE"),
    ),
):
    try:
        builder.build(root)
    except Exception as error:
        result = {
            "success": False,
            "error": f"{type(error).__name__}: {error}",
        }
    else:
        result = {"success": True, "error": ""}

real_recovery = displaced / recovery_name if recovery_name is not None else displaced
try:
    target = real_recovery / builder.TARGET_NAME
    directory_metadata = real_recovery.stat(follow_symlinks=False)
    target_metadata = target.stat(follow_symlinks=False)
    recovery_identity = [
        directory_metadata.st_dev,
        directory_metadata.st_ino,
        stat.S_IMODE(directory_metadata.st_mode),
        target_metadata.st_dev,
        target_metadata.st_ino,
        stat.S_IMODE(target_metadata.st_mode),
        target_metadata.st_nlink,
        target.read_bytes().hex(),
    ]
except OSError:
    recovery_identity = None

result.update({
    "injected": injected,
    "recovery_name": recovery_name,
    "retained_identity": retained_identity,
    "real_recovery_matches": recovery_identity == old_identity,
    "lexical_recovery": str(root / "skills" / recovery_name) if recovery_name else "",
})
print(json.dumps(result))
"""
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-c", script, str(root), str(outside)],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        raise AssertionError(
            "bounded rebound-recovery diagnostic subprocess failed: "
            + result.stdout
            + result.stderr
        )
    return json.loads(result.stdout)


def run_builder_primary_and_cleanup_failure_probe_in_subprocess(
    root: Path,
) -> dict[str, object]:
    script = """
import json
import os
import sys
from pathlib import Path
from unittest import mock
from scripts import build_skillsmp_adapter as builder

root = Path(sys.argv[1])
cleanup_injected = False

def corrupt_owned_stage_then_fail(skills_fd, stage_name, output_name):
    global cleanup_injected
    stage_fd = os.open(
        stage_name,
        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
        dir_fd=skills_fd,
    )
    try:
        evidence_fd = os.open(
            "SECONDARY_CLEANUP_FAILURE",
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
            dir_fd=stage_fd,
        )
        os.close(evidence_fd)
        cleanup_injected = True
    finally:
        os.close(stage_fd)
    raise OSError("PRIMARY_INSTALL_FAILURE")

with mock.patch.object(
    builder,
    "_install_staged_adapter",
    side_effect=corrupt_owned_stage_then_fail,
):
    try:
        builder.build(root)
    except Exception as error:
        messages = [f"{type(error).__name__}: {error}"]
        notes = list(getattr(error, "__notes__", ()))
        cause = error.__cause__
        while cause is not None:
            messages.append(f"{type(cause).__name__}: {cause}")
            notes.extend(getattr(cause, "__notes__", ()))
            cause = cause.__cause__
        result = {
            "success": False,
            "messages": messages,
            "notes": notes,
        }
    else:
        result = {"success": True, "messages": [], "notes": []}

result["cleanup_injected"] = cleanup_injected
print(json.dumps(result))
"""
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, "-c", script, str(root)],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        raise AssertionError(
            "bounded primary-plus-cleanup failure subprocess failed: "
            + result.stdout
            + result.stderr
        )
    return json.loads(result.stdout)


def tree_snapshot(root: Path) -> dict[str, tuple]:
    snapshot: dict[str, tuple] = {}
    for base, directories, files in os.walk(root, followlinks=False):
        base_path = Path(base)
        for name in [*directories, *files]:
            path = base_path / name
            relative = path.relative_to(root).as_posix()
            metadata = path.stat(follow_symlinks=False)
            mode = stat.S_IMODE(metadata.st_mode)
            if path.is_symlink():
                snapshot[relative] = ("symlink", os.readlink(path), mode)
            elif path.is_dir():
                snapshot[relative] = ("directory", mode)
            elif path.is_file():
                snapshot[relative] = ("file", path.read_bytes(), mode)
            else:
                snapshot[relative] = ("special", stat.S_IFMT(metadata.st_mode), mode)
    return snapshot


def tree_identity_snapshot(root: Path) -> dict[str, tuple]:
    snapshot: dict[str, tuple] = {}
    for path in [root, *sorted(root.rglob("*"))]:
        relative = "." if path == root else path.relative_to(root).as_posix()
        metadata = path.stat(follow_symlinks=False)
        identity = (
            metadata.st_dev,
            metadata.st_ino,
            stat.S_IMODE(metadata.st_mode),
            metadata.st_nlink,
        )
        if path.is_symlink():
            snapshot[relative] = ("symlink", *identity, os.readlink(path))
        elif path.is_dir():
            snapshot[relative] = ("directory", *identity)
        elif path.is_file():
            snapshot[relative] = ("file", *identity, path.read_bytes())
        else:
            snapshot[relative] = ("special", *identity, stat.S_IFMT(metadata.st_mode))
    return snapshot


def identifies_unsafe_file_type(messages: list[str] | str) -> bool:
    text = messages if isinstance(messages, str) else "\n".join(messages)
    return any(
        marker in text.lower()
        for marker in ("directory", "regular", "special", "unsupported")
    )


def adapter_directory_snapshot(
    adapter_root: Path,
) -> tuple[bytes, tuple[int, int, int], tuple[int, int, int]]:
    adapter = adapter_root / "SKILL.md"
    root_metadata = adapter_root.stat(follow_symlinks=False)
    adapter_metadata = adapter.stat(follow_symlinks=False)
    return (
        adapter.read_bytes(),
        (
            root_metadata.st_dev,
            root_metadata.st_ino,
            stat.S_IMODE(root_metadata.st_mode),
        ),
        (
            adapter_metadata.st_dev,
            adapter_metadata.st_ino,
            stat.S_IMODE(adapter_metadata.st_mode),
        ),
    )


def adapter_snapshot(root: Path) -> tuple[bytes, tuple[int, int, int], tuple[int, int, int]]:
    return adapter_directory_snapshot(root / ADAPTER_RELATIVE_PATH.parent)


class DistributionTests(unittest.TestCase):
    def _load_modules(self):
        self.assertTrue(BUILDER_PATH.is_file(), "builder implementation is missing")
        self.assertTrue(VALIDATOR_PATH.is_file(), "validator implementation is missing")
        importlib.invalidate_caches()
        return (
            importlib.import_module("scripts.build_codex_plugin"),
            importlib.import_module("scripts.validate_distribution"),
        )

    def _load_skillsmp_builder(self):
        self.assertTrue(
            SKILLSMP_BUILDER_PATH.is_file(),
            "SkillsMP adapter builder implementation is missing",
        )
        importlib.invalidate_caches()
        return importlib.import_module("scripts.build_skillsmp_adapter")

    def _load_distribution_validator(self):
        self.assertTrue(VALIDATOR_PATH.is_file(), "validator implementation is missing")
        importlib.invalidate_caches()
        return importlib.import_module("scripts.validate_distribution")

    def _assert_exact_recovery_evidence(
        self,
        root: Path,
        builder,
        before: tuple[bytes, tuple[int, int, int], tuple[int, int, int]],
        expected_target_mode: int,
        error: BaseException,
    ) -> tuple[Path, Path]:
        output = root / ADAPTER_RELATIVE_PATH.parent
        self.assertFalse(
            os.path.lexists(output),
            "canonical adapter output must be absent after unproven recovery",
        )
        recovery_entries = [
            path
            for path in (root / "skills").iterdir()
            if path.name.startswith(builder.RECOVERY_PREFIX)
        ]
        self.assertEqual(
            len(recovery_entries),
            1,
            "unproven recovery must leave one visible recovery-prefixed entry",
        )
        recovery = recovery_entries[0]
        recovery_metadata = recovery.stat(follow_symlinks=False)
        self.assertFalse(recovery.is_symlink(), "recovery evidence must not be a symlink")
        self.assertTrue(
            stat.S_ISDIR(recovery_metadata.st_mode),
            "recovery evidence must be a directory",
        )
        self.assertEqual(
            (
                recovery_metadata.st_dev,
                recovery_metadata.st_ino,
                stat.S_IMODE(recovery_metadata.st_mode),
            ),
            before[1],
            "recovery directory must be the captured adapter directory object",
        )
        evidence = recovery / "SKILL.md"
        self.assertEqual(set(recovery.iterdir()), {evidence})
        evidence_metadata = evidence.stat(follow_symlinks=False)
        self.assertFalse(evidence.is_symlink(), "recovery target must not be a symlink")
        self.assertTrue(stat.S_ISREG(evidence_metadata.st_mode))
        self.assertEqual(
            (evidence_metadata.st_dev, evidence_metadata.st_ino),
            before[2][:2],
            "recovery target must be the captured adapter target object",
        )
        self.assertEqual(stat.S_IMODE(evidence_metadata.st_mode), expected_target_mode)
        self.assertEqual(
            evidence_metadata.st_nlink,
            1,
            "recovery target must not be a hard-link copy",
        )
        self.assertEqual(evidence.read_bytes(), before[0])
        self.assertIn(str(recovery), str(error))
        self.assertTrue(recovery.exists(), "the recovery path reported by the error must exist")
        return recovery, evidence

    def _assert_prior_adapter_compensated_or_recovered(
        self,
        root: Path,
        builder,
        before: tuple[bytes, tuple[int, int, int], tuple[int, int, int]],
    ) -> None:
        skills = root / "skills"
        output = skills / builder.SKILL_NAME
        candidates = []
        if os.path.lexists(output):
            candidates.append(output)
        candidates.extend(
            path
            for path in skills.iterdir()
            if path.name.startswith(builder.RECOVERY_PREFIX)
        )
        retained = []
        for candidate in candidates:
            metadata = candidate.stat(follow_symlinks=False)
            if candidate.is_symlink() or not stat.S_ISDIR(metadata.st_mode):
                continue
            if set(path.name for path in candidate.iterdir()) != {"SKILL.md"}:
                continue
            target = candidate / "SKILL.md"
            target_metadata = target.stat(follow_symlinks=False)
            if target.is_symlink() or not stat.S_ISREG(target_metadata.st_mode):
                continue
            if adapter_directory_snapshot(candidate) == before:
                retained.append(candidate)
        self.assertTrue(
            retained,
            "prior generated adapter object must be compensated at canonical output "
            "or retained as visible recovery evidence",
        )

    def _assert_transaction_seam_call(
        self, seam, builder, skills: Path, transient_prefix: str
    ) -> None:
        seam.assert_called_once()
        if transient_prefix == builder.STAGE_PREFIX:
            seam_name = "_install_staged_adapter"
            transient_parameter = "stage_name"
        else:
            self.assertEqual(transient_prefix, builder.RECOVERY_PREFIX)
            seam_name = "_restore_recovery"
            transient_parameter = "recovery_name"
        signature = inspect.signature(getattr(builder, seam_name))
        try:
            bound = signature.bind(*seam.call_args.args, **seam.call_args.kwargs)
        except TypeError as error:
            self.fail(f"invalid {seam_name} call: {error}")
        self.assertEqual(
            tuple(bound.arguments),
            ("skills_fd", transient_parameter, "output_name"),
        )
        skills_fd = bound.arguments["skills_fd"]
        transient_name = bound.arguments[transient_parameter]
        output_name = bound.arguments["output_name"]
        self.assertIsInstance(skills_fd, int)
        self.assertNotIsInstance(skills_fd, bool)
        self.assertIsInstance(transient_name, str)
        self.assertTrue(transient_name.startswith(transient_prefix))
        self.assertEqual(output_name, builder.SKILL_NAME)

    def _assert_restored_verifier_call(self, seam, builder, skills: Path) -> None:
        seam.assert_called_once()
        signature = inspect.signature(builder._verify_restored_snapshot)
        try:
            bound = signature.bind(*seam.call_args.args, **seam.call_args.kwargs)
        except TypeError as error:
            self.fail(f"invalid _verify_restored_snapshot call: {error}")
        self.assertEqual(
            tuple(bound.arguments),
            ("skills_fd", "output_name", "snapshot"),
        )
        skills_fd = bound.arguments["skills_fd"]
        output_name = bound.arguments["output_name"]
        snapshot = bound.arguments["snapshot"]
        self.assertIsInstance(skills_fd, int)
        self.assertNotIsInstance(skills_fd, bool)
        self.assertEqual(output_name, builder.SKILL_NAME)
        self.assertIsNotNone(snapshot)

    def _assert_builder_rejects_injected_residue(
        self, scenario: str, prefix: str, evidence_bytes: bytes
    ) -> None:
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root)
            before = adapter_snapshot(copy_root)
            residue = copy_root / "skills" / f"{prefix}injected-review"

            result = run_builder_install_probe_in_subprocess(copy_root, scenario)

            self.assertEqual(result["calls"], 1)
            self.assertTrue(
                result.get("injection_performed"),
                f"install-boundary residue injection did not execute: {result!r}",
            )
            self.assertFalse(residue.is_symlink())
            self.assertTrue(residue.is_dir(), "unknown transaction residue was removed")
            evidence = residue / "evidence.txt"
            self.assertEqual(set(residue.iterdir()), {evidence})
            self.assertEqual(evidence.read_bytes(), evidence_bytes)
            self.assertFalse(
                result["success"],
                f"builder reported success with injected residue: {result!r}",
            )
            self._assert_prior_adapter_compensated_or_recovered(
                copy_root, builder, before
            )

    def _assert_builder_fails_without_capability(self, capability: str) -> None:
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root)
            skills_before = tree_identity_snapshot(copy_root / "skills")

            result = run_builder_without_capability_in_subprocess(
                copy_root, capability
            )

            self.assertEqual(
                tree_identity_snapshot(copy_root / "skills"), skills_before
            )
            self.assertEqual(
                {"repo_to_outside": True, "outside_to_repo": True},
                result.get("link_direction_coverage"),
                result,
            )
            self.assertEqual(
                [],
                result.get("mutation_events"),
                f"builder attempted skills mutation before rejecting {capability}: {result!r}",
            )
            self.assertFalse(
                result["success"],
                f"builder ran without required {capability} capability: {result!r}",
            )
            diagnostic = str(result.get("error", "")).lower()
            diagnostic_tokens = {
                capability.lower(),
                capability.lower().replace("_", "-"),
                capability.lower().replace("_", " "),
            }
            self.assertTrue(
                any(token in diagnostic for token in diagnostic_tokens),
                f"missing {capability} portability diagnostic: {diagnostic}",
            )

    def test_package_metadata_points_pi_at_canonical_skill(self):
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        self.assertIn("pi-package", package["keywords"])
        self.assertEqual(package["pi"], {"skills": ["./SKILL.md"]})
        self.assertEqual(package["license"], "MIT")
        self.assertEqual(package["name"], "openspec-superpower-change")

    def test_package_allowlist_does_not_publish_internal_material(self):
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        files = set(package["files"])
        self.assertIn("SKILL.md", files)
        self.assertIn("references/", files)
        self.assertNotIn(".", files)
        self.assertNotIn("*", files)
        self.assertFalse(any(path.startswith("openspec") for path in files))
        self.assertFalse(any(path.startswith("tests") for path in files))
        self.assertFalse(any(path.startswith("distribution") for path in files))
        self.assertFalse(
            any(path.rstrip("/") == "skills" or path.startswith("skills/") for path in files)
        )
        self.assertNotIn("scripts/build_codex_plugin.py", files)

    def test_skillsmp_builder_declares_descriptor_relative_safety_seams(self):
        builder = self._load_skillsmp_builder()
        expected = {
            "_check_replaceable_output": ("skills_fd", "output_name"),
            "_install_staged_adapter": ("skills_fd", "stage_name", "output_name"),
            "_restore_recovery": ("skills_fd", "recovery_name", "output_name"),
            "_verify_restored_snapshot": ("skills_fd", "output_name", "snapshot"),
            "_read_source_snapshot": ("root_fd", "source_name"),
        }
        actual = {}
        for name in expected:
            seam = getattr(builder, name, None)
            actual[name] = (
                tuple(inspect.signature(seam).parameters) if callable(seam) else None
            )
        self.assertEqual(actual, expected)

    def test_skillsmp_builder_creates_exact_regular_adapter_from_root_skill(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            remove_adapter(copy_root)
            builder.build(copy_root)
            adapter = copy_root / ADAPTER_RELATIVE_PATH
            self.assertFalse(adapter.is_symlink())
            self.assertTrue(adapter.is_file())
            self.assertEqual(adapter.read_bytes(), (copy_root / "SKILL.md").read_bytes())
            self.assertEqual(set(adapter.parent.iterdir()), {adapter})

    def test_skillsmp_builder_reads_and_rechecks_source_through_bound_root(self):
        builder = self._load_skillsmp_builder()
        original_read = getattr(builder, "_read_source_snapshot", None)
        self.assertIsNotNone(
            original_read,
            "builder must declare _read_source_snapshot(root_fd, source_name)",
        )
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root)
            root_metadata = copy_root.stat(follow_symlinks=False)
            observed: list[tuple[int, str]] = []

            def read_source_snapshot(root_fd, source_name):
                self.assertIsInstance(root_fd, int)
                self.assertNotIsInstance(root_fd, bool)
                self.assertEqual(source_name, "SKILL.md")
                bound_metadata = os.fstat(root_fd)
                self.assertEqual(
                    (bound_metadata.st_dev, bound_metadata.st_ino),
                    (root_metadata.st_dev, root_metadata.st_ino),
                )
                observed.append((root_fd, source_name))
                return original_read(root_fd, source_name)

            with mock.patch.object(
                builder,
                "_read_source_snapshot",
                side_effect=read_source_snapshot,
            ):
                builder.build(copy_root)

            self.assertGreaterEqual(
                len(observed),
                2,
                "canonical source must be captured and rechecked before success",
            )

    def test_skillsmp_builder_rejects_repository_root_path_rebind(self):
        with tempfile.TemporaryDirectory() as raw:
            temporary_root = Path(raw)
            copy_root = copy_tree(ROOT, temporary_root / "repo")
            write_adapter(copy_root)
            replacement = temporary_root / "replacement-root"
            replacement.mkdir()
            replacement_source = replacement / "SKILL.md"
            replacement_source.write_bytes((copy_root / "SKILL.md").read_bytes())
            replacement_skills = replacement / "skills"
            replacement_skills.mkdir()
            sentinel = replacement / "replacement-sentinel.txt"
            sentinel.write_bytes(b"replacement root must remain unchanged\n")
            replacement_before = tree_identity_snapshot(replacement)

            result = run_builder_after_root_rebind_in_subprocess(
                copy_root, replacement
            )

            self.assertFalse(
                result.get("seam_missing"),
                f"root-bound source seam is unavailable: {result!r}",
            )
            self.assertTrue(result["rebound"], result)
            self.assertGreaterEqual(
                result["calls"],
                2,
                "source snapshot seam was not re-entered after root pathname rebind",
            )
            self.assertTrue(
                result["bound_original"],
                f"source recheck escaped the retained root descriptor: {result!r}",
            )
            self.assertEqual(
                tree_identity_snapshot(copy_root),
                replacement_before,
                "replacement root object/tree changed after pathname rebind",
            )
            self.assertTrue(
                result["replacement_unchanged"],
                f"replacement root closure changed in the bounded probe: {result!r}",
            )
            self.assertFalse(
                result["success"],
                f"builder reported success through the replacement root: {result!r}",
            )

    def test_skillsmp_validator_accepts_exact_adapter(self):
        validator = self._load_distribution_validator()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root)
            self.assertEqual(validator.validate_skillsmp_adapter(copy_root), [])

    def test_skillsmp_validator_rejects_missing_adapter(self):
        validator = self._load_distribution_validator()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            remove_adapter(copy_root)
            errors = validator.validate_skillsmp_adapter(copy_root)
            self.assertTrue(any("missing" in error.lower() for error in errors))

    def test_skillsmp_validator_rejects_stale_adapter(self):
        validator = self._load_distribution_validator()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root, b"stale adapter\n")
            errors = validator.validate_skillsmp_adapter(copy_root)
            self.assertTrue(any("differ" in error.lower() for error in errors))

    def test_skillsmp_validator_rejects_symlinked_target(self):
        validator = self._load_distribution_validator()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            adapter = copy_root / ADAPTER_RELATIVE_PATH
            remove_adapter(copy_root)
            adapter.parent.mkdir(parents=True)
            adapter.symlink_to(copy_root / "SKILL.md")
            errors = validator.validate_skillsmp_adapter(copy_root)
            self.assertTrue(any("symlink" in error.lower() for error in errors))

    def test_skillsmp_validator_rejects_hard_linked_target(self):
        validator = self._load_distribution_validator()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            adapter = write_adapter(copy_root)
            peer = Path(raw) / "adapter-hard-link-peer.md"
            os.link(adapter, peer)
            before = adapter.stat(follow_symlinks=False)
            peer_bytes = peer.read_bytes()

            errors = validator.validate_skillsmp_adapter(copy_root)

            after = peer.stat(follow_symlinks=False)
            self.assertEqual(
                (after.st_dev, after.st_ino, stat.S_IMODE(after.st_mode)),
                (before.st_dev, before.st_ino, stat.S_IMODE(before.st_mode)),
            )
            self.assertEqual(peer.read_bytes(), peer_bytes)
            self.assertEqual(after.st_nlink, 2)
            self.assertTrue(
                any("link" in error.lower() for error in errors),
                f"validator accepted adapter target with st_nlink={after.st_nlink}",
            )

    def test_skillsmp_validator_rejects_adapter_parent_rebind_race(self):
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root)
            output = copy_root / ADAPTER_RELATIVE_PATH.parent
            outside = Path(raw) / "external-adapter"
            outside.mkdir()
            sentinel = outside / "SKILL.md"
            sentinel.write_bytes((copy_root / "SKILL.md").read_bytes())
            outside_before = tree_snapshot(outside)

            result = validate_adapter_after_parent_rebind_in_subprocess(
                copy_root, outside
            )

            self.assertEqual(tree_snapshot(outside), outside_before)
            self.assertFalse(
                result["seam_missing"],
                "declared validator seam _open_adapter_directory is missing",
            )
            self.assertTrue(result["rebound"], "race injection did not run")
            self.assertTrue(output.is_symlink())
            errors = result["errors"]
            self.assertIsInstance(errors, list)
            self.assertTrue(errors, "validator accepted a rebound adapter parent")
            self.assertTrue(
                any(
                    marker in "\n".join(errors).lower()
                    for marker in ("parent", "binding", "symlink", "drift", "changed")
                ),
                errors,
            )

    def test_skillsmp_validator_rejects_rebind_after_final_directory_bind(self):
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root)
            output = copy_root / ADAPTER_RELATIVE_PATH.parent
            outside = Path(raw) / "external-final-bind-adapter"
            outside.mkdir()
            sentinel = outside / "SKILL.md"
            sentinel.write_bytes((copy_root / "SKILL.md").read_bytes())
            outside_before = tree_snapshot(outside)

            result = validate_adapter_after_parent_rebind_in_subprocess(
                copy_root, outside, rebind_after_call=2
            )

            self.assertFalse(result["seam_missing"])
            self.assertEqual(result["calls"], 2, "validator did not perform final bind")
            self.assertTrue(result["rebound"], "final-bind race injection did not run")
            self.assertTrue(output.is_symlink())
            self.assertEqual(tree_snapshot(outside), outside_before)
            errors = result["errors"]
            self.assertIsInstance(errors, list)
            self.assertTrue(
                errors,
                "validator returned PASS after its final bound directory pathname drifted",
            )
            self.assertTrue(
                any(
                    marker in "\n".join(errors).lower()
                    for marker in ("binding", "symlink", "drift", "changed")
                ),
                errors,
            )

    def test_skillsmp_validator_rejects_symlinked_skills_parent_without_escape(self):
        validator = self._load_distribution_validator()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            skills_root = copy_root / "skills"
            if skills_root.exists():
                shutil.rmtree(skills_root)
            outside = Path(raw) / "outside-skills"
            outside.mkdir()
            sentinel = outside / "sentinel.txt"
            sentinel.write_bytes(b"validator must not change external parent")
            before = {path.name: path.read_bytes() for path in outside.iterdir()}
            skills_root.symlink_to(outside, target_is_directory=True)

            errors = validator.validate_skillsmp_adapter(copy_root)

            self.assertTrue(any("symlink" in error.lower() for error in errors))
            self.assertEqual(
                {path.name: path.read_bytes() for path in outside.iterdir()},
                before,
            )

    def test_skillsmp_validator_rejects_symlinked_skill_parent_without_escape(self):
        validator = self._load_distribution_validator()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            remove_adapter(copy_root)
            skills_root = copy_root / "skills"
            skills_root.mkdir(exist_ok=True)
            outside = Path(raw) / "outside-skill"
            outside.mkdir()
            sentinel = outside / "SKILL.md"
            sentinel.write_bytes(b"validator must not change external skill")
            before = {path.name: path.read_bytes() for path in outside.iterdir()}
            (skills_root / SKILL_NAME).symlink_to(outside, target_is_directory=True)

            errors = validator.validate_skillsmp_adapter(copy_root)

            self.assertTrue(any("symlink" in error.lower() for error in errors))
            self.assertEqual(
                {path.name: path.read_bytes() for path in outside.iterdir()},
                before,
            )

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO creation is unavailable")
    def test_skillsmp_validator_rejects_special_target(self):
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            adapter = copy_root / ADAPTER_RELATIVE_PATH
            remove_adapter(copy_root)
            adapter.parent.mkdir(parents=True)
            unrelated = copy_root / "unrelated.txt"
            unrelated.write_bytes(b"validator must not change unrelated content")
            os.mkfifo(adapter)
            errors = validate_adapter_in_subprocess(copy_root)
            self.assertTrue(identifies_unsafe_file_type(errors))
            self.assertTrue(stat.S_ISFIFO(adapter.stat(follow_symlinks=False).st_mode))
            self.assertEqual(
                unrelated.read_bytes(), b"validator must not change unrelated content"
            )

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO creation is unavailable")
    def test_skillsmp_validator_rejects_special_skills_parent(self):
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            skills_root = copy_root / "skills"
            if skills_root.exists():
                shutil.rmtree(skills_root)
            unrelated = copy_root / "unrelated.txt"
            unrelated.write_bytes(b"validator must preserve unrelated content")
            os.mkfifo(skills_root)

            errors = validate_adapter_in_subprocess(copy_root)

            self.assertTrue(identifies_unsafe_file_type(errors))
            self.assertTrue(stat.S_ISFIFO(skills_root.stat(follow_symlinks=False).st_mode))
            self.assertEqual(
                unrelated.read_bytes(), b"validator must preserve unrelated content"
            )

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO creation is unavailable")
    def test_skillsmp_validator_rejects_special_skill_parent(self):
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            remove_adapter(copy_root)
            skills_root = copy_root / "skills"
            skills_root.mkdir(exist_ok=True)
            output = skills_root / SKILL_NAME
            unrelated = copy_root / "unrelated.txt"
            unrelated.write_bytes(b"validator must preserve unrelated content")
            os.mkfifo(output)

            errors = validate_adapter_in_subprocess(copy_root)

            self.assertTrue(identifies_unsafe_file_type(errors))
            self.assertTrue(stat.S_ISFIFO(output.stat(follow_symlinks=False).st_mode))
            self.assertEqual(
                unrelated.read_bytes(), b"validator must preserve unrelated content"
            )

    def test_skillsmp_validator_rejects_unexpected_adapter_file(self):
        validator = self._load_distribution_validator()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            adapter = write_adapter(copy_root)
            (adapter.parent / "unexpected.txt").write_text(
                "outside the generated closure\n", encoding="utf-8"
            )
            errors = validator.validate_skillsmp_adapter(copy_root)
            self.assertTrue(any("unexpected" in error.lower() for error in errors))

    def test_skillsmp_validator_rejects_unexpected_adapter_directory(self):
        validator = self._load_distribution_validator()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            adapter = write_adapter(copy_root)
            (adapter.parent / "unexpected").mkdir()
            errors = validator.validate_skillsmp_adapter(copy_root)
            self.assertTrue(any("unexpected" in error.lower() for error in errors))

    def test_skillsmp_validator_rejects_unexpected_adapter_symlink_without_escape(self):
        validator = self._load_distribution_validator()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            adapter = write_adapter(copy_root)
            outside = Path(raw) / "outside-unexpected"
            outside.mkdir()
            sentinel = outside / "sentinel.txt"
            sentinel.write_bytes(b"unexpected symlink target must not change")
            before = {path.name: path.read_bytes() for path in outside.iterdir()}
            unexpected = adapter.parent / "unexpected-link"
            unexpected.symlink_to(sentinel)

            errors = validator.validate_skillsmp_adapter(copy_root)

            self.assertTrue(any("symlink" in error.lower() for error in errors))
            self.assertEqual(
                {path.name: path.read_bytes() for path in outside.iterdir()},
                before,
            )

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO creation is unavailable")
    def test_skillsmp_validator_rejects_unexpected_special_entry(self):
        self._load_distribution_validator()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            adapter = write_adapter(copy_root)
            os.mkfifo(adapter.parent / "unexpected-fifo")
            errors = validate_adapter_in_subprocess(copy_root)
            self.assertTrue(
                any(
                    "unexpected" in error.lower()
                    or identifies_unsafe_file_type(error)
                    for error in errors
                )
            )

    def test_distribution_validator_includes_skillsmp_adapter_validation(self):
        plugin_builder, validator = self._load_modules()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            plugin_output = copy_root / "generated-plugin"
            plugin_builder.build(copy_root, plugin_output)
            remove_adapter(copy_root)
            errors = validator.validate(copy_root, plugin_output, check_npm=False)
            self.assertTrue(any("adapter" in error.lower() for error in errors))

    def _assert_validator_rejects_builder_residue(self, prefix: str) -> None:
        plugin_builder, validator = self._load_modules()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root)
            plugin_output = copy_root / "generated-plugin"
            plugin_builder.build(copy_root, plugin_output)
            residue = copy_root / "skills" / f"{prefix}leftover"
            residue.mkdir()
            (residue / "evidence.txt").write_bytes(b"visible builder residue\n")
            before = tree_snapshot(residue)

            focused_errors = validator.validate_skillsmp_adapter(copy_root)
            aggregate_errors = validator.validate(
                copy_root, plugin_output, check_npm=False
            )

            self.assertEqual(tree_snapshot(residue), before)
            self.assertTrue(
                focused_errors
                and any(residue.name in error for error in focused_errors)
                and aggregate_errors
                and any(residue.name in error for error in aggregate_errors),
                "focused and aggregate validation must report visible builder "
                f"residue {residue.name!r}; focused={focused_errors!r}, "
                f"aggregate={aggregate_errors!r}",
            )

    def test_skillsmp_validator_rejects_stage_prefixed_sibling_residue(self):
        builder = self._load_skillsmp_builder()
        self._assert_validator_rejects_builder_residue(builder.STAGE_PREFIX)

    def test_skillsmp_validator_rejects_recovery_prefixed_sibling_residue(self):
        builder = self._load_skillsmp_builder()
        self._assert_validator_rejects_builder_residue(builder.RECOVERY_PREFIX)

    def test_skillsmp_builder_rejects_symlinked_skills_parent_without_escape(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            skills_root = copy_root / "skills"
            if skills_root.exists():
                shutil.rmtree(skills_root)
            outside = Path(raw) / "outside-skills"
            outside.mkdir()
            sentinel = outside / "sentinel.txt"
            sentinel.write_bytes(b"must remain unchanged")
            (copy_root / "skills").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                builder.build(copy_root)
            self.assertEqual(sentinel.read_bytes(), b"must remain unchanged")
            self.assertEqual(set(outside.iterdir()), {sentinel})

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO creation is unavailable")
    def test_skillsmp_builder_rejects_special_skills_parent(self):
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            skills_root = copy_root / "skills"
            if skills_root.exists():
                shutil.rmtree(skills_root)
            unrelated = copy_root / "unrelated.txt"
            unrelated.write_bytes(b"builder must preserve unrelated content")
            outside = Path(raw) / "outside"
            outside.mkdir()
            sentinel = outside / "sentinel.txt"
            sentinel.write_bytes(b"builder must preserve external content")
            os.mkfifo(skills_root)

            error = reject_adapter_build_in_subprocess(copy_root)

            self.assertTrue(identifies_unsafe_file_type(error))
            self.assertTrue(stat.S_ISFIFO(skills_root.stat(follow_symlinks=False).st_mode))
            self.assertEqual(unrelated.read_bytes(), b"builder must preserve unrelated content")
            self.assertEqual(sentinel.read_bytes(), b"builder must preserve external content")
            self.assertEqual(set(outside.iterdir()), {sentinel})

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO creation is unavailable")
    def test_skillsmp_builder_rejects_special_skill_parent(self):
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            remove_adapter(copy_root)
            skills_root = copy_root / "skills"
            skills_root.mkdir(exist_ok=True)
            output = skills_root / SKILL_NAME
            unrelated = copy_root / "unrelated.txt"
            unrelated.write_bytes(b"builder must preserve unrelated content")
            outside = Path(raw) / "outside"
            outside.mkdir()
            sentinel = outside / "sentinel.txt"
            sentinel.write_bytes(b"builder must preserve external content")
            os.mkfifo(output)

            error = reject_adapter_build_in_subprocess(copy_root)

            self.assertTrue(identifies_unsafe_file_type(error))
            self.assertTrue(stat.S_ISFIFO(output.stat(follow_symlinks=False).st_mode))
            self.assertEqual(unrelated.read_bytes(), b"builder must preserve unrelated content")
            self.assertEqual(sentinel.read_bytes(), b"builder must preserve external content")
            self.assertEqual(set(outside.iterdir()), {sentinel})

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO creation is unavailable")
    def test_skillsmp_builder_rejects_special_target(self):
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            remove_adapter(copy_root)
            adapter = copy_root / ADAPTER_RELATIVE_PATH
            adapter.parent.mkdir(parents=True)
            unrelated = copy_root / "unrelated.txt"
            unrelated.write_bytes(b"builder must preserve unrelated content")
            outside = Path(raw) / "outside"
            outside.mkdir()
            sentinel = outside / "sentinel.txt"
            sentinel.write_bytes(b"builder must preserve external content")
            os.mkfifo(adapter)

            error = reject_adapter_build_in_subprocess(copy_root)

            self.assertTrue(identifies_unsafe_file_type(error))
            self.assertTrue(stat.S_ISFIFO(adapter.stat(follow_symlinks=False).st_mode))
            self.assertEqual(unrelated.read_bytes(), b"builder must preserve unrelated content")
            self.assertEqual(sentinel.read_bytes(), b"builder must preserve external content")
            self.assertEqual(set(outside.iterdir()), {sentinel})

    def test_skillsmp_builder_rejects_symlinked_output_without_external_mutation(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            skills_root = copy_root / "skills"
            remove_adapter(copy_root)
            skills_root.mkdir(exist_ok=True)
            outside = Path(raw) / "outside-adapter"
            outside.mkdir()
            sentinel = outside / "SKILL.md"
            sentinel.write_bytes(b"external adapter must not change")
            (skills_root / SKILL_NAME).symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                builder.build(copy_root)
            self.assertEqual(sentinel.read_bytes(), b"external adapter must not change")
            self.assertEqual(set(outside.iterdir()), {sentinel})

    def test_skillsmp_builder_rejects_symlinked_target_without_external_mutation(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            remove_adapter(copy_root)
            adapter = copy_root / ADAPTER_RELATIVE_PATH
            adapter.parent.mkdir(parents=True)
            outside = Path(raw) / "outside-target"
            outside.mkdir()
            sentinel = outside / "sentinel.md"
            sentinel.write_bytes(b"external target must not change")
            companion = outside / "companion.txt"
            companion.write_bytes(b"external tree must not change")
            before = {
                path.name: path.read_bytes()
                for path in outside.iterdir()
            }
            adapter.symlink_to(sentinel)

            with self.assertRaises(ValueError):
                builder.build(copy_root)

            after = {
                path.name: path.read_bytes()
                for path in outside.iterdir()
            }
            self.assertEqual(after, before)
            self.assertTrue(adapter.is_symlink())
            self.assertEqual(adapter.readlink(), sentinel)

    def test_skillsmp_builder_rejects_existing_output_with_unexpected_regular_file(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            adapter = write_adapter(copy_root, b"preexisting adapter\n")
            unexpected = adapter.parent / "unexpected.txt"
            unexpected.write_bytes(b"preexisting unexpected content\n")
            before = {
                path.name: path.read_bytes()
                for path in adapter.parent.iterdir()
            }

            with self.assertRaises(ValueError):
                builder.build(copy_root)

            self.assertEqual(
                {path.name: path.read_bytes() for path in adapter.parent.iterdir()},
                before,
            )

    def test_skillsmp_builder_rejects_existing_output_with_unexpected_directory(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            adapter = write_adapter(copy_root, b"preexisting adapter\n")
            unexpected = adapter.parent / "unexpected"
            unexpected.mkdir()
            (unexpected / "nested.txt").write_bytes(b"nested preexisting content\n")
            before = tree_snapshot(adapter.parent)

            with self.assertRaises(ValueError):
                builder.build(copy_root)

            self.assertEqual(tree_snapshot(adapter.parent), before)

    def test_skillsmp_builder_rejects_existing_output_with_unexpected_symlink(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            adapter = write_adapter(copy_root, b"preexisting adapter\n")
            outside = Path(raw) / "outside-builder-unexpected"
            outside.mkdir()
            sentinel = outside / "sentinel.txt"
            sentinel.write_bytes(b"external unexpected target\n")
            unexpected = adapter.parent / "unexpected-link"
            unexpected.symlink_to(sentinel)

            with self.assertRaises(ValueError):
                builder.build(copy_root)

            self.assertEqual(adapter.read_bytes(), b"preexisting adapter\n")
            self.assertTrue(unexpected.is_symlink())
            self.assertEqual(unexpected.readlink(), sentinel)
            self.assertEqual(sentinel.read_bytes(), b"external unexpected target\n")
            self.assertEqual(set(outside.iterdir()), {sentinel})

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO creation is unavailable")
    def test_skillsmp_builder_rejects_existing_output_with_unexpected_special_entry(self):
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            adapter = write_adapter(copy_root, b"preexisting adapter\n")
            unexpected = adapter.parent / "unexpected-fifo"
            os.mkfifo(unexpected)
            unrelated = copy_root / "unrelated.txt"
            unrelated.write_bytes(b"unrelated content must remain unchanged\n")
            before = tree_snapshot(adapter.parent)

            error = reject_adapter_build_in_subprocess(copy_root)

            self.assertTrue(
                "unexpected" in error.lower() or identifies_unsafe_file_type(error)
            )
            self.assertEqual(tree_snapshot(adapter.parent), before)
            self.assertEqual(
                unrelated.read_bytes(), b"unrelated content must remain unchanged\n"
            )

    def test_skillsmp_builder_rejects_existing_hard_linked_target_before_mutation(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            adapter = write_adapter(copy_root)
            peer = Path(raw) / "existing-adapter-peer.md"
            os.link(adapter, peer)
            skills_before = tree_snapshot(copy_root / "skills")
            adapter_before = adapter_snapshot(copy_root)
            peer_before = peer.stat(follow_symlinks=False)
            peer_bytes = peer.read_bytes()

            result = run_builder_with_skills_mutation_trap_in_subprocess(copy_root)

            self.assertEqual(tree_snapshot(copy_root / "skills"), skills_before)
            self.assertEqual(adapter_snapshot(copy_root), adapter_before)
            peer_after = peer.stat(follow_symlinks=False)
            self.assertEqual(
                (
                    peer_after.st_dev,
                    peer_after.st_ino,
                    stat.S_IMODE(peer_after.st_mode),
                ),
                (
                    peer_before.st_dev,
                    peer_before.st_ino,
                    stat.S_IMODE(peer_before.st_mode),
                ),
            )
            self.assertEqual(peer_after.st_nlink, 2)
            self.assertEqual(peer.read_bytes(), peer_bytes)
            self.assertFalse(result["success"], result)
            self.assertEqual(
                {"repo_to_outside": True, "outside_to_repo": True},
                result.get("link_direction_coverage"),
                result,
            )
            self.assertEqual(
                [],
                result.get("mutation_events"),
                f"hard-linked adapter was not rejected before skills mutation: {result!r}",
            )
            self.assertIn("link", str(result.get("error", "")).lower())

    def test_skillsmp_builder_rejects_hard_linked_source_before_skills_mutation(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root)
            source = copy_root / "SKILL.md"
            peer = Path(raw) / "canonical-source-peer.md"
            os.link(source, peer)
            skills_before = tree_snapshot(copy_root / "skills")
            adapter_before = adapter_snapshot(copy_root)
            source_before = source.stat(follow_symlinks=False)
            peer_bytes = peer.read_bytes()

            result = run_builder_with_skills_mutation_trap_in_subprocess(copy_root)

            self.assertEqual(tree_snapshot(copy_root / "skills"), skills_before)
            self.assertEqual(adapter_snapshot(copy_root), adapter_before)
            source_after = source.stat(follow_symlinks=False)
            peer_after = peer.stat(follow_symlinks=False)
            self.assertEqual(
                (source_after.st_dev, source_after.st_ino),
                (source_before.st_dev, source_before.st_ino),
            )
            self.assertEqual(
                (
                    peer_after.st_dev,
                    peer_after.st_ino,
                    stat.S_IMODE(peer_after.st_mode),
                ),
                (
                    source_before.st_dev,
                    source_before.st_ino,
                    stat.S_IMODE(source_before.st_mode),
                ),
            )
            self.assertEqual(source_after.st_nlink, 2)
            self.assertEqual(peer.read_bytes(), peer_bytes)
            self.assertFalse(result["success"], result)
            self.assertEqual(
                {"repo_to_outside": True, "outside_to_repo": True},
                result.get("link_direction_coverage"),
                result,
            )
            self.assertEqual(
                [],
                result.get("mutation_events"),
                f"hard-linked source was not rejected before skills mutation: {result!r}",
            )
            self.assertIn("link", str(result.get("error", "")).lower())

    def test_skillsmp_builder_rejects_existing_output_identity_drift(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root)
            output = copy_root / ADAPTER_RELATIVE_PATH.parent
            original_check = builder._check_replaceable_output
            calls = 0
            observed_contract: list[tuple[object, object]] = []

            def check_with_preinstall_rebind(skills_fd, output_name):
                nonlocal calls
                observed_contract.append((skills_fd, output_name))
                if not isinstance(skills_fd, int) or isinstance(skills_fd, bool):
                    raise TypeError(
                        "_check_replaceable_output requires a skills directory descriptor"
                    )
                if output_name != builder.SKILL_NAME:
                    raise TypeError(
                        "_check_replaceable_output requires the canonical output name"
                    )
                calls += 1
                if calls == 2:
                    displaced = Path(raw) / "captured-adapter"
                    shutil.move(output, displaced)
                    output.mkdir()
                    (output / "SKILL.md").write_bytes(
                        b"concurrently substituted adapter\n"
                    )
                return original_check(skills_fd, output_name)

            with mock.patch.object(
                builder,
                "_check_replaceable_output",
                side_effect=check_with_preinstall_rebind,
            ):
                with self.assertRaises((TypeError, ValueError)):
                    builder.build(copy_root)
            self.assertTrue(observed_contract)
            self.assertTrue(
                all(
                    isinstance(skills_fd, int)
                    and not isinstance(skills_fd, bool)
                    and output_name == builder.SKILL_NAME
                    for skills_fd, output_name in observed_contract
                ),
                f"unexpected replaceability seam calls: {observed_contract!r}",
            )
            self.assertGreaterEqual(calls, 2)
            self.assertEqual(
                (output / "SKILL.md").read_bytes(),
                b"concurrently substituted adapter\n",
            )

    def test_skillsmp_builder_rejects_skills_parent_rebind_at_install_boundary(self):
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root)
            skills = copy_root / "skills"
            outside = Path(raw) / "external-skills"
            outside.mkdir()
            sentinel = outside / "sentinel.txt"
            sentinel.write_bytes(b"external tree must remain unchanged\n")
            outside_metadata = outside.stat(follow_symlinks=False)
            sentinel_metadata = sentinel.stat(follow_symlinks=False)
            outside_identity = (
                outside_metadata.st_dev,
                outside_metadata.st_ino,
                stat.S_IMODE(outside_metadata.st_mode),
            )
            sentinel_identity = (
                sentinel_metadata.st_dev,
                sentinel_metadata.st_ino,
                stat.S_IMODE(sentinel_metadata.st_mode),
                sentinel_metadata.st_nlink,
                sentinel.read_bytes(),
            )

            result = run_builder_install_probe_in_subprocess(
                copy_root, "parent-rebind", outside
            )

            self.assertTrue(
                result.get("lure_prepared"),
                f"install probe did not create the actual stage-name lure: {result!r}",
            )
            self.assertTrue(result.get("injection_performed"), result)
            outside_after = outside.stat(follow_symlinks=False)
            sentinel_after = sentinel.stat(follow_symlinks=False)
            self.assertEqual(
                (
                    outside_after.st_dev,
                    outside_after.st_ino,
                    stat.S_IMODE(outside_after.st_mode),
                ),
                outside_identity,
            )
            self.assertEqual(
                (
                    sentinel_after.st_dev,
                    sentinel_after.st_ino,
                    stat.S_IMODE(sentinel_after.st_mode),
                    sentinel_after.st_nlink,
                    sentinel.read_bytes(),
                ),
                sentinel_identity,
            )
            self.assertTrue(
                result.get("external_unchanged"),
                f"external lure tree changed at the install boundary: {result!r}",
            )
            self.assertTrue(skills.is_symlink(), "parent-rebind injection did not run")
            self.assertEqual(result["calls"], 1)
            self.assertTrue(
                result.get("injection_performed"),
                f"source replacement injection did not execute: {result!r}",
            )
            self.assertFalse(
                result["success"],
                f"builder accepted a rebound skills parent: {result!r}",
            )

    def test_skillsmp_builder_rejects_source_path_replacement_at_install_boundary(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root)
            before = adapter_snapshot(copy_root)

            result = run_builder_install_probe_in_subprocess(
                copy_root, "source-replace"
            )

            self.assertEqual(result["calls"], 1)
            self.assertTrue(
                result.get("injection_performed"),
                f"source in-place drift injection did not execute: {result!r}",
            )
            self.assertFalse(
                result["success"],
                f"builder returned success after source replacement: {result!r}",
            )
            self._assert_prior_adapter_compensated_or_recovered(
                copy_root, builder, before
            )

    def test_skillsmp_builder_rejects_source_inplace_drift_at_install_boundary(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root)
            before = adapter_snapshot(copy_root)

            result = run_builder_install_probe_in_subprocess(
                copy_root, "source-inplace"
            )

            self.assertEqual(result["calls"], 1)
            self.assertTrue(
                result.get("injection_performed"),
                f"source in-place drift injection did not execute: {result!r}",
            )
            self.assertFalse(
                result["success"],
                f"builder returned success after in-place source drift: {result!r}",
            )
            self._assert_prior_adapter_compensated_or_recovered(
                copy_root, builder, before
            )

    def test_skillsmp_builder_rejects_stage_residue_injected_at_install_boundary(self):
        builder = self._load_skillsmp_builder()
        self._assert_builder_rejects_injected_residue(
            "stage-residue", builder.STAGE_PREFIX, b"unknown stage residue\n"
        )

    def test_skillsmp_builder_rejects_recovery_residue_injected_at_install_boundary(self):
        builder = self._load_skillsmp_builder()
        self._assert_builder_rejects_injected_residue(
            "recovery-residue",
            builder.RECOVERY_PREFIX,
            b"unknown recovery residue\n",
        )

    def test_skillsmp_builder_fails_before_mutation_without_nofollow_capability(self):
        self._assert_builder_fails_without_capability("O_NOFOLLOW")

    def test_skillsmp_builder_fails_before_mutation_without_odirectory_capability(self):
        self._assert_builder_fails_without_capability("O_DIRECTORY")

    def test_skillsmp_builder_fails_before_mutation_without_dir_fd_support(self):
        self._assert_builder_fails_without_capability("dir_fd")

    def test_skillsmp_builder_preserves_prior_state_on_source_replacement_before_recovery_commit(self):
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root, b"prior adapter before source replacement\n")

            result = run_builder_recovery_commit_probe_in_subprocess(
                copy_root, "source-replace-before-commit"
            )

            self.assertTrue(result.get("injected"), result)
            self.assertFalse(
                result["success"],
                f"builder committed after source replacement: {result!r}",
            )
            self.assertTrue(
                result.get("prior_state_compensated"),
                "source replacement left the new output blocking exact prior-state "
                f"compensation: {result!r}",
            )

    def test_skillsmp_builder_preserves_prior_state_on_source_inplace_drift_before_recovery_commit(self):
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root, b"prior adapter before in-place source drift\n")

            result = run_builder_recovery_commit_probe_in_subprocess(
                copy_root, "source-inplace-before-commit"
            )

            self.assertTrue(result.get("injected"), result)
            self.assertFalse(
                result["success"],
                f"builder committed after in-place source drift: {result!r}",
            )
            self.assertTrue(
                result.get("prior_state_compensated"),
                "in-place source drift left the new output blocking exact prior-state "
                f"compensation: {result!r}",
            )

    def test_skillsmp_builder_preserves_prior_state_on_root_rebind_before_recovery_commit(self):
        with tempfile.TemporaryDirectory() as raw:
            raw_root = Path(raw)
            copy_root = copy_tree(ROOT, raw_root / "repo")
            write_adapter(copy_root, b"prior adapter before root rebind\n")
            replacement = raw_root / "replacement-root"
            replacement.mkdir()
            (replacement / "sentinel.txt").write_bytes(
                b"replacement root must remain untouched\n"
            )

            result = run_builder_recovery_commit_probe_in_subprocess(
                copy_root, "root-rebind-before-commit", replacement
            )

            self.assertTrue(result.get("injected"), result)
            self.assertFalse(
                result["success"],
                f"builder committed after repository-root rebind: {result!r}",
            )
            self.assertTrue(result.get("external_unchanged"), result)
            self.assertTrue(
                result.get("prior_state_compensated"),
                "root rebind left the new output blocking exact prior-state "
                f"compensation: {result!r}",
            )

    def test_skillsmp_builder_preserves_prior_state_on_skills_rebind_before_recovery_commit(self):
        with tempfile.TemporaryDirectory() as raw:
            raw_root = Path(raw)
            copy_root = copy_tree(ROOT, raw_root / "repo")
            write_adapter(copy_root, b"prior adapter before skills rebind\n")
            outside = raw_root / "outside-skills"
            outside.mkdir()
            (outside / "sentinel.txt").write_bytes(
                b"external skills tree must remain untouched\n"
            )

            result = run_builder_recovery_commit_probe_in_subprocess(
                copy_root, "skills-rebind-before-commit", outside
            )

            self.assertTrue(result.get("injected"), result)
            self.assertFalse(
                result["success"],
                f"builder committed after skills-parent rebind: {result!r}",
            )
            self.assertTrue(result.get("external_unchanged"), result)
            self.assertTrue(
                result.get("prior_state_compensated"),
                "skills rebind left the new output blocking exact prior-state "
                f"compensation: {result!r}",
            )

    def test_skillsmp_builder_runs_no_rejecting_checks_after_recovery_commit(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            original_source = (copy_root / "SKILL.md").read_bytes()
            write_adapter(copy_root, b"prior adapter deleted at commit\n")

            result = run_builder_recovery_commit_probe_in_subprocess(
                copy_root, "source-drift-after-commit"
            )

            self.assertTrue(result.get("recovery_observed"), result)
            self.assertEqual("os.rmdir", result.get("commit_event_observed"), result)
            self.assertTrue(result.get("injected"), result)
            self.assertTrue(
                result["success"],
                "a check after verified recovery deletion converted a committed build "
                f"into failure: {result!r}",
            )
            self.assertEqual(
                (copy_root / "SKILL.md").read_bytes(),
                b"source changed after recovery commit\n",
            )
            output = copy_root / "skills" / builder.SKILL_NAME
            self.assertEqual((output / builder.TARGET_NAME).read_bytes(), original_source)
            self.assertFalse(
                any(
                    path.name.startswith(builder.RECOVERY_PREFIX)
                    for path in (copy_root / "skills").iterdir()
                )
            )

    def test_skillsmp_builder_output_drift_after_recovery_commit_cannot_reject(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root, b"prior adapter deleted at commit\n")

            result = run_builder_recovery_commit_probe_in_subprocess(
                copy_root, "output-drift-after-commit"
            )

            self.assertEqual("os.rmdir", result.get("commit_event_observed"), result)
            self.assertTrue(result.get("injected"), result)
            self.assertTrue(
                result["success"],
                "an output check after recovery commit converted a committed build "
                f"into failure: {result!r}",
            )
            output = copy_root / "skills" / builder.SKILL_NAME / builder.TARGET_NAME
            self.assertEqual(
                output.read_bytes(),
                b"generated output changed after recovery commit\n",
            )

    def test_skillsmp_builder_residue_after_recovery_commit_cannot_reject(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root, b"prior adapter deleted at commit\n")

            result = run_builder_recovery_commit_probe_in_subprocess(
                copy_root, "residue-after-commit"
            )

            self.assertEqual("os.rmdir", result.get("commit_event_observed"), result)
            self.assertTrue(result.get("injected"), result)
            self.assertTrue(
                result["success"],
                "a residue check after recovery commit converted a committed build "
                f"into failure: {result!r}",
            )
            residue = (
                copy_root
                / "skills"
                / f"{builder.STAGE_PREFIX}post-commit-review"
            )
            self.assertEqual(
                (residue / "evidence.txt").read_bytes(),
                b"post-commit residue\n",
            )

    def test_skillsmp_builder_residue_between_recovery_unlink_and_rmdir_cannot_reject(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root, b"prior adapter committed at unlink\n")
            original_unlink = builder.os.unlink
            injected = False

            def unlink_then_inject(path, *args, **kwargs):
                nonlocal injected
                result = original_unlink(path, *args, **kwargs)
                directory_fd = kwargs.get("dir_fd")
                if not injected and os.fsdecode(path) == builder.TARGET_NAME:
                    injected = True
                    residue_fd = os.open(
                        "injected-after-recovery-unlink",
                        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                        0o600,
                        dir_fd=directory_fd,
                    )
                    os.close(residue_fd)
                return result

            with mock.patch.object(builder.os, "unlink", side_effect=unlink_then_inject):
                generated = builder.build(copy_root)

            self.assertTrue(injected)
            self.assertEqual(generated.read_bytes(), (copy_root / "SKILL.md").read_bytes())

    def test_skillsmp_builder_root_rebind_after_recovery_commit_cannot_reject(self):
        with tempfile.TemporaryDirectory() as raw:
            raw_root = Path(raw)
            copy_root = copy_tree(ROOT, raw_root / "repo")
            write_adapter(copy_root, b"prior adapter deleted at commit\n")
            replacement = raw_root / "replacement-root"
            replacement.mkdir()
            (replacement / "sentinel.txt").write_bytes(
                b"replacement root remains live after commit\n"
            )

            result = run_builder_recovery_commit_probe_in_subprocess(
                copy_root, "root-rebind-after-commit", replacement
            )

            self.assertEqual("os.rmdir", result.get("commit_event_observed"), result)
            self.assertTrue(result.get("injected"), result)
            self.assertTrue(result.get("external_unchanged"), result)
            self.assertTrue(
                result["success"],
                "a root-binding check after recovery commit converted a committed "
                f"build into failure: {result!r}",
            )
            self.assertEqual(
                (copy_root / "sentinel.txt").read_bytes(),
                b"replacement root remains live after commit\n",
            )

    def test_skillsmp_builder_skills_rebind_after_recovery_commit_cannot_reject(self):
        with tempfile.TemporaryDirectory() as raw:
            raw_root = Path(raw)
            copy_root = copy_tree(ROOT, raw_root / "repo")
            write_adapter(copy_root, b"prior adapter deleted at commit\n")
            outside = raw_root / "outside-skills"
            outside.mkdir()
            (outside / "sentinel.txt").write_bytes(
                b"replacement skills remains live after commit\n"
            )

            result = run_builder_recovery_commit_probe_in_subprocess(
                copy_root, "skills-rebind-after-commit", outside
            )

            self.assertEqual("os.rmdir", result.get("commit_event_observed"), result)
            self.assertTrue(result.get("injected"), result)
            self.assertTrue(result.get("external_unchanged"), result)
            self.assertTrue(
                result["success"],
                "a skills-binding check after recovery commit converted a committed "
                f"build into failure: {result!r}",
            )
            self.assertTrue((copy_root / "skills").is_symlink())
            self.assertEqual(
                (copy_root / "skills" / "sentinel.txt").read_bytes(),
                b"replacement skills remains live after commit\n",
            )

    def test_skillsmp_builder_fails_before_skills_creation_without_fd_listdir_support(self):
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            shutil.rmtree(copy_root / "skills")

            result = run_builder_capability_preflight_probe_in_subprocess(
                copy_root, "supports_fd:listdir"
            )

            self.assertEqual(
                {"repo_to_outside": True, "outside_to_repo": True},
                result.get("link_direction_coverage"),
                result,
            )
            self.assertEqual([], result.get("mutation_events"), result)
            self.assertFalse(result["success"], result)
            self.assertTrue(result.get("tree_unchanged"), result)
            self.assertFalse(result.get("skills_exists"), result)
            diagnostic = str(result.get("error", "")).lower()
            self.assertIn("listdir", diagnostic)
            self.assertTrue(
                "supports_fd" in diagnostic
                or "descriptor listing" in diagnostic
                or "file descriptor" in diagnostic,
                diagnostic,
            )

    def test_skillsmp_builder_fails_before_skills_creation_without_nofollow_stat_support(self):
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            shutil.rmtree(copy_root / "skills")

            result = run_builder_capability_preflight_probe_in_subprocess(
                copy_root, "supports_follow_symlinks:stat"
            )

            self.assertEqual(
                {"repo_to_outside": True, "outside_to_repo": True},
                result.get("link_direction_coverage"),
                result,
            )
            self.assertEqual([], result.get("mutation_events"), result)
            self.assertFalse(result["success"], result)
            self.assertTrue(result.get("tree_unchanged"), result)
            self.assertFalse(result.get("skills_exists"), result)
            diagnostic = str(result.get("error", "")).lower()
            self.assertIn("stat", diagnostic)
            self.assertTrue(
                "follow_symlinks" in diagnostic
                or "no-follow stat" in diagnostic
                or "nofollow stat" in diagnostic,
                diagnostic,
            )

    def test_skillsmp_builder_reports_rebound_recovery_by_retained_identity(self):
        with tempfile.TemporaryDirectory() as raw:
            raw_root = Path(raw)
            copy_root = copy_tree(ROOT, raw_root / "repo")
            write_adapter(copy_root, b"real recovery evidence after rebind\n")
            outside = raw_root / "outside-skills"
            outside.mkdir()
            (outside / "sentinel.txt").write_bytes(b"unrelated live pathname\n")

            result = run_builder_rebound_recovery_diagnostic_probe_in_subprocess(
                copy_root, outside
            )

            self.assertTrue(result.get("injected"), result)
            self.assertFalse(result["success"], result)
            self.assertTrue(result.get("real_recovery_matches"), result)
            error = str(result.get("error", ""))
            recovery_name = str(result.get("recovery_name", ""))
            retained_identity = result.get("retained_identity") or []
            self.assertTrue(recovery_name, result)
            self.assertIn(recovery_name, error)
            self.assertEqual(len(retained_identity), 2, result)
            self.assertIn(str(retained_identity[0]), error)
            self.assertIn(str(retained_identity[1]), error)
            self.assertIn("untrusted", error.lower())
            self.assertNotIn("/dev/fd/", error)
            self.assertNotIn("/proc/self/fd/", error)

    def test_skillsmp_builder_cleanup_failure_preserves_primary_exception(self):
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root, b"prior adapter survives dual failure\n")

            result = run_builder_primary_and_cleanup_failure_probe_in_subprocess(
                copy_root
            )

            self.assertTrue(result.get("cleanup_injected"), result)
            self.assertFalse(result["success"], result)
            diagnostic = "\n".join(
                [*result.get("messages", []), *result.get("notes", [])]
            )
            self.assertIn("PRIMARY_INSTALL_FAILURE", diagnostic)
            self.assertIn("SECONDARY_CLEANUP_FAILURE", diagnostic)

    def test_skillsmp_builder_restores_exact_adapter_after_caught_install_failure(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            adapter = write_adapter(copy_root, b"previous exact adapter state\n")
            adapter.parent.chmod(0o750)
            adapter.chmod(0o640)
            before = adapter_snapshot(copy_root)
            skills = copy_root / "skills"

            with (
                mock.patch.object(
                    builder,
                    "_install_staged_adapter",
                    side_effect=OSError("injected adapter install failure"),
                ) as install_staged_adapter,
                mock.patch.object(
                    builder,
                    "_restore_recovery",
                    wraps=builder._restore_recovery,
                ) as restore_recovery,
                mock.patch.object(
                    builder,
                    "_verify_restored_snapshot",
                    wraps=builder._verify_restored_snapshot,
                ) as verify_restored_snapshot,
            ):
                with self.assertRaises((OSError, RuntimeError, ValueError)):
                    builder.build(copy_root)
            self._assert_transaction_seam_call(
                install_staged_adapter,
                builder,
                skills,
                builder.STAGE_PREFIX,
            )
            self._assert_transaction_seam_call(
                restore_recovery,
                builder,
                skills,
                builder.RECOVERY_PREFIX,
            )
            self._assert_restored_verifier_call(
                verify_restored_snapshot, builder, skills
            )
            self.assertEqual(adapter_snapshot(copy_root), before)
            self.assertFalse(
                any("recovery" in path.name.lower() for path in (copy_root / "skills").iterdir())
            )

    def test_skillsmp_builder_preserves_recovery_residue_when_restore_is_unprovable(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            adapter = write_adapter(copy_root, b"previous exact adapter state\n")
            skills = copy_root / "skills"
            with (
                mock.patch.object(
                    builder,
                    "_install_staged_adapter",
                    side_effect=OSError("injected adapter install failure"),
                ) as install_staged_adapter,
                mock.patch.object(
                    builder,
                    "_restore_recovery",
                    wraps=builder._restore_recovery,
                ) as restore_recovery,
                mock.patch.object(
                    builder,
                    "_verify_restored_snapshot",
                    return_value=False,
                ) as verify_restored_snapshot,
            ):
                with self.assertRaises((OSError, RuntimeError, ValueError)):
                    builder.build(copy_root)
            self._assert_transaction_seam_call(
                install_staged_adapter, builder, skills, builder.STAGE_PREFIX
            )
            self._assert_transaction_seam_call(
                restore_recovery, builder, skills, builder.RECOVERY_PREFIX
            )
            self._assert_restored_verifier_call(
                verify_restored_snapshot, builder, skills
            )
            recovery = [
                path
                for path in (copy_root / "skills").iterdir()
                if "recovery" in path.name.lower()
            ]
            self.assertTrue(recovery, "unprovable restoration must leave recovery residue")
            self.assertTrue(all(not path.is_symlink() for path in recovery))
            self.assertTrue(
                any(
                    (path / "SKILL.md").read_bytes()
                    == b"previous exact adapter state\n"
                    for path in recovery
                )
            )

    def test_skillsmp_builder_preserves_recovery_when_restore_operation_fails(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            write_adapter(copy_root, b"prior adapter preserved in recovery\n")
            skills = copy_root / "skills"
            with (
                mock.patch.object(
                    builder,
                    "_install_staged_adapter",
                    side_effect=OSError("injected adapter install failure"),
                ) as install_staged_adapter,
                mock.patch.object(
                    builder,
                    "_restore_recovery",
                    side_effect=OSError("injected recovery failure"),
                ) as restore_recovery,
            ):
                with self.assertRaises((OSError, RuntimeError, ValueError)):
                    builder.build(copy_root)

            self._assert_transaction_seam_call(
                install_staged_adapter, builder, skills, builder.STAGE_PREFIX
            )
            self._assert_transaction_seam_call(
                restore_recovery, builder, skills, builder.RECOVERY_PREFIX
            )

            recovery = [
                path
                for path in (copy_root / "skills").iterdir()
                if "recovery" in path.name.lower()
            ]
            self.assertTrue(recovery, "failed recovery must remain visible")
            self.assertTrue(
                any(
                    (path / "SKILL.md").read_bytes()
                    == b"prior adapter preserved in recovery\n"
                    for path in recovery
                )
            )

    def test_skillsmp_builder_retains_real_recovery_after_restored_mode_drift(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            adapter = write_adapter(copy_root, b"restored object evidence\n")
            adapter.parent.chmod(0o750)
            adapter.chmod(0o640)
            before = adapter_snapshot(copy_root)
            mutation: dict[str, object] = {}
            skills = copy_root / "skills"

            def mutate_restored_mode(skills_fd, output_name, snapshot):
                if not isinstance(skills_fd, int) or isinstance(skills_fd, bool):
                    raise TypeError(
                        "_verify_restored_snapshot requires a skills descriptor"
                    )
                if output_name != builder.SKILL_NAME or snapshot is None:
                    raise TypeError(
                        "_verify_restored_snapshot requires output name and snapshot"
                    )
                mutation["contract"] = (skills_fd, output_name, snapshot)
                output = skills / output_name
                directory_metadata = output.stat(follow_symlinks=False)
                target = output / "SKILL.md"
                target_before = target.stat(follow_symlinks=False)
                target.chmod(0o600)
                target_after = target.stat(follow_symlinks=False)
                mutation["directory"] = (
                    directory_metadata.st_dev,
                    directory_metadata.st_ino,
                    stat.S_IMODE(directory_metadata.st_mode),
                )
                mutation["target_before"] = (
                    target_before.st_dev,
                    target_before.st_ino,
                    stat.S_IMODE(target_before.st_mode),
                )
                mutation["target_after"] = (
                    target_after.st_dev,
                    target_after.st_ino,
                    stat.S_IMODE(target_after.st_mode),
                )
                mutation["bytes"] = target.read_bytes()
                return False

            with (
                mock.patch.object(
                    builder,
                    "_install_staged_adapter",
                    side_effect=OSError("injected adapter install failure"),
                ) as install_staged_adapter,
                mock.patch.object(
                    builder,
                    "_verify_restored_snapshot",
                    side_effect=mutate_restored_mode,
                ) as verify_restored_snapshot,
            ):
                with self.assertRaises(RuntimeError) as raised:
                    builder.build(copy_root)

            self._assert_transaction_seam_call(
                install_staged_adapter, builder, skills, builder.STAGE_PREFIX
            )
            self._assert_restored_verifier_call(
                verify_restored_snapshot, builder, skills
            )
            self.assertIn(
                "contract",
                mutation,
                "restored verifier was not called with its descriptor-relative signature",
            )
            self.assertEqual(
                mutation["directory"],
                before[1],
                "verifier must observe the captured adapter directory object",
            )
            self.assertEqual(
                mutation["target_before"],
                before[2],
                "verifier must observe the captured adapter target object",
            )
            self.assertEqual(
                mutation["target_after"],
                (before[2][0], before[2][1], 0o600),
                "mode drift must preserve the target inode",
            )
            self.assertEqual(mutation["bytes"], before[0])
            self._assert_exact_recovery_evidence(
                copy_root, builder, before, 0o600, raised.exception
            )

    def test_skillsmp_builder_retains_real_recovery_after_verifier_exception(self):
        builder = self._load_skillsmp_builder()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            adapter = write_adapter(copy_root, b"verifier exception evidence\n")
            adapter.parent.chmod(0o750)
            adapter.chmod(0o640)
            before = adapter_snapshot(copy_root)
            restored: dict[str, object] = {}
            skills = copy_root / "skills"

            def fail_restored_verifier(skills_fd, output_name, snapshot):
                if not isinstance(skills_fd, int) or isinstance(skills_fd, bool):
                    raise TypeError(
                        "_verify_restored_snapshot requires a skills descriptor"
                    )
                if output_name != builder.SKILL_NAME or snapshot is None:
                    raise TypeError(
                        "_verify_restored_snapshot requires output name and snapshot"
                    )
                restored["contract"] = (skills_fd, output_name, snapshot)
                output = skills / output_name
                directory_metadata = output.stat(follow_symlinks=False)
                target = output / "SKILL.md"
                target_metadata = target.stat(follow_symlinks=False)
                restored["directory"] = (
                    directory_metadata.st_dev,
                    directory_metadata.st_ino,
                    stat.S_IMODE(directory_metadata.st_mode),
                )
                restored["target"] = (
                    target_metadata.st_dev,
                    target_metadata.st_ino,
                    stat.S_IMODE(target_metadata.st_mode),
                )
                restored["bytes"] = target.read_bytes()
                raise RuntimeError("injected restored verifier exception")

            with (
                mock.patch.object(
                    builder,
                    "_install_staged_adapter",
                    side_effect=OSError("injected adapter install failure"),
                ) as install_staged_adapter,
                mock.patch.object(
                    builder,
                    "_verify_restored_snapshot",
                    side_effect=fail_restored_verifier,
                ) as verify_restored_snapshot,
            ):
                with self.assertRaises(RuntimeError) as raised:
                    builder.build(copy_root)

            self._assert_transaction_seam_call(
                install_staged_adapter, builder, skills, builder.STAGE_PREFIX
            )
            self._assert_restored_verifier_call(
                verify_restored_snapshot, builder, skills
            )
            self.assertIn(
                "contract",
                restored,
                "restored verifier was not called with its descriptor-relative signature",
            )
            self.assertEqual(restored["directory"], before[1])
            self.assertEqual(restored["target"], before[2])
            self.assertEqual(restored["bytes"], before[0])
            self._assert_exact_recovery_evidence(
                copy_root, builder, before, before[2][2], raised.exception
            )

    def test_builder_projects_manifest_files_byte_for_byte(self):
        builder, validator = self._load_modules()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            output = copy_root / "generated-plugin"
            generated = builder.build(copy_root, output)
            self.assertTrue(generated)
            self.assertEqual(validator.validate_plugin(copy_root, output), [])

    def test_generated_plugin_has_skill_only_manifest_shape(self):
        builder, validator = self._load_modules()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            output = copy_root / "generated-plugin"
            builder.build(copy_root, output)
            plugin = json.loads(
                (output / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
            )
            self.assertEqual(plugin["name"], "openspec-superpower-change")
            self.assertEqual(plugin["version"], "0.1.0")
            self.assertEqual(plugin["license"], "MIT")
            self.assertEqual(plugin["skills"], "./skills/")
            self.assertEqual(
                plugin["interface"]["defaultPrompt"],
                ["Use the governed change gate for this engineering task."],
            )
            write_adapter(copy_root)
            self.assertEqual(validator.validate(copy_root, output), [])

    def test_validator_rejects_invalid_default_prompt_shape(self):
        builder, validator = self._load_modules()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            output = copy_root / "generated-plugin"
            builder.build(copy_root, output)
            manifest_path = output / ".codex-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["interface"]["defaultPrompt"] = "not-an-array"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            errors = validator.validate_plugin(copy_root, output)
            self.assertTrue(any("defaultPrompt" in error for error in errors))

    def test_validator_rejects_overlong_default_prompt(self):
        builder, validator = self._load_modules()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            output = copy_root / "generated-plugin"
            builder.build(copy_root, output)
            manifest_path = output / ".codex-plugin" / "plugin.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["interface"]["defaultPrompt"] = ["x" * 129]
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            errors = validator.validate_plugin(copy_root, output)
            self.assertTrue(any("at most 128" in error for error in errors))

    def test_validator_rejects_symlink_in_generated_plugin(self):
        builder, validator = self._load_modules()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            output = copy_root / "generated-plugin"
            builder.build(copy_root, output)
            skill_root = output / "skills" / "openspec-superpower-change"
            link = skill_root / "SKILL-link.md"
            link.symlink_to(skill_root / "SKILL.md")
            errors = validator.validate_plugin(copy_root, output)
            self.assertTrue(any("symlink" in error.lower() for error in errors))

    def test_validator_rejects_generated_source_drift(self):
        builder, validator = self._load_modules()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            output = copy_root / "generated-plugin"
            builder.build(copy_root, output)
            generated_skill = output / "skills" / "openspec-superpower-change" / "SKILL.md"
            generated_skill.write_text("drift\n", encoding="utf-8")
            errors = validator.validate_plugin(copy_root, output)
            self.assertTrue(any("differs" in error.lower() for error in errors))

    def test_validator_rejects_unexpected_regular_file(self):
        builder, validator = self._load_modules()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            output = copy_root / "generated-plugin"
            builder.build(copy_root, output)
            extra = output / "skills" / "openspec-superpower-change" / "extra.md"
            extra.write_text("unexpected\n", encoding="utf-8")
            errors = validator.validate_plugin(copy_root, output)
            self.assertTrue(any("unexpected" in error.lower() for error in errors))

    def test_builder_rejects_symlink_output_parent_escape(self):
        builder, _ = self._load_modules()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            outside = copy_root.parent / "outside-output"
            outside.mkdir()
            linked_parent = copy_root / "linked-output-parent"
            linked_parent.symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                builder.build(copy_root, linked_parent / "codex-plugin")
            self.assertFalse((outside / "codex-plugin").exists())

    def test_validator_rejects_allowlisted_symlink(self):
        _, validator = self._load_modules()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            public_doc = copy_root / "docs" / "distribution.md"
            outside = copy_root.parent / "outside-doc.md"
            outside.write_text("outside\n", encoding="utf-8")
            public_doc.unlink()
            public_doc.symlink_to(outside)
            errors = validator.validate_package(copy_root)
            self.assertTrue(any("symlink" in error.lower() for error in errors))

    def test_npm_validator_matches_the_complete_public_file_set(self):
        _, validator = self._load_modules()
        self.assertEqual(validator.validate_npm_package(ROOT), [])

    def test_builder_rejects_symlink_output(self):
        builder, _ = self._load_modules()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            target = copy_root / "real-output"
            builder.build(copy_root, target)
            link = copy_root / "linked-output"
            link.symlink_to(target, target_is_directory=True)
            with self.assertRaises(ValueError):
                builder.build(copy_root, link)

    def test_builder_rejects_parent_symlink_source(self):
        builder, _ = self._load_modules()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            references = copy_root / "references"
            outside = copy_root.parent / "outside-references"
            shutil.move(references, outside)
            references.symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                builder.build(copy_root, copy_root / "generated-plugin")

    def test_builder_rejects_unmarked_existing_output(self):
        builder, _ = self._load_modules()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            output = copy_root / "generated-plugin"
            output.mkdir(parents=True)
            (output / "unrelated.txt").write_text("do not replace", encoding="utf-8")
            with self.assertRaises(ValueError):
                builder.build(copy_root, output)
            self.assertEqual(
                (output / "unrelated.txt").read_text(encoding="utf-8"),
                "do not replace",
            )

    def test_builder_rejects_symlink_inside_existing_output(self):
        builder, _ = self._load_modules()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            output = copy_root / "generated-plugin"
            builder.build(copy_root, output)
            plugin_metadata = output / ".codex-plugin"
            outside = copy_root.parent / "outside-plugin-metadata"
            outside.mkdir()
            shutil.move(plugin_metadata / "plugin.json", outside / "plugin.json")
            plugin_metadata.rmdir()
            plugin_metadata.symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                builder.build(copy_root, output)
            self.assertTrue((outside / "plugin.json").is_file())

    def test_validator_rejects_symlink_output_parent(self):
        builder, validator = self._load_modules()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            source_output = copy_root / "generated-plugin"
            builder.build(copy_root, source_output)
            outside = copy_root.parent / "outside-validator-output"
            shutil.copytree(source_output, outside)
            linked_parent = copy_root / "linked-validator-parent"
            linked_parent.symlink_to(outside, target_is_directory=True)
            errors = validator.validate_plugin(
                copy_root, linked_parent / "generated-plugin"
            )
            self.assertTrue(any("output" in error.lower() for error in errors))

    def test_builder_rejects_existing_output_identity_drift(self):
        builder, _ = self._load_modules()
        with tempfile.TemporaryDirectory() as raw:
            copy_root = copy_tree(ROOT, Path(raw) / "repo")
            output = copy_root / "generated-plugin"
            builder.build(copy_root, output)
            original_check = builder._check_replaceable_output
            calls = 0

            def check_and_replace_after_capture(root_lexical, root, candidate):
                nonlocal calls
                calls += 1
                identity = original_check(root_lexical, root, candidate)
                if calls == 2:
                    replacement = copy_root / "replacement-copy"
                    shutil.copytree(candidate, replacement)
                    shutil.rmtree(candidate)
                    shutil.copytree(replacement, candidate)
                return identity

            with mock.patch.object(
                builder,
                "_check_replaceable_output",
                side_effect=check_and_replace_after_capture,
            ):
                with self.assertRaises(ValueError):
                    builder.build(copy_root, output)
            self.assertTrue((output / ".codex-plugin" / "plugin.json").is_file())

    def test_npm_dry_run_contains_only_public_files(self):
        result = subprocess.run(
            ["npm", "pack", "--dry-run", "--json"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        records = json.loads(result.stdout)
        files = {item["path"] for item in records[0]["files"]}
        self.assertIn("package.json", files)
        self.assertIn("SKILL.md", files)
        self.assertNotIn("AGENTS.md", files)
        self.assertFalse(any(path.startswith("openspec/") for path in files))
        self.assertFalse(any(path.startswith("tests/") for path in files))
        self.assertFalse(any(path.startswith("distribution/") for path in files))
        self.assertFalse(any(path == "skills" or path.startswith("skills/") for path in files))
        self.assertNotIn("scripts/build_codex_plugin.py", files)

    def test_local_skills_cli_discovers_exactly_one_logical_skill(self):
        with tempfile.TemporaryDirectory() as raw:
            temporary_root = Path(raw)
            copy_root = copy_tree(ROOT, temporary_root / "repo")
            write_adapter(copy_root)
            isolated_user_root = temporary_root / "isolated-user"
            npm_state_root = temporary_root / "npm-state"
            temporary_npm_cache = temporary_root / "npm-cache"
            npm_prefix = isolated_user_root / "npm-prefix"
            isolated_paths = {
                "HOME": isolated_user_root / "home",
                "CODEX_HOME": isolated_user_root / "codex",
                "XDG_CONFIG_HOME": isolated_user_root / "xdg-config",
                "XDG_CACHE_HOME": isolated_user_root / "xdg-cache",
                "XDG_DATA_HOME": isolated_user_root / "xdg-data",
                "XDG_STATE_HOME": isolated_user_root / "xdg-state",
                "FLATPAK_XDG_CONFIG_HOME": isolated_user_root / "flatpak-config",
                "CLAUDE_CONFIG_DIR": isolated_user_root / "claude",
                "AUTOHAND_HOME": isolated_user_root / "autohand",
                "HERMES_HOME": isolated_user_root / "hermes",
                "VIBE_HOME": isolated_user_root / "vibe",
                "APPDATA": isolated_user_root / "appdata",
                "LOCALAPPDATA": isolated_user_root / "local-appdata",
                "USERPROFILE": isolated_user_root / "user-profile",
            }
            for path in [
                *isolated_paths.values(),
                npm_prefix / "bin",
                npm_prefix / "lib",
                npm_state_root,
                temporary_npm_cache / "_npx",
            ]:
                path.mkdir(parents=True, exist_ok=True)
            npm_cache_result = subprocess.run(
                ["npm", "config", "get", "cache"],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertEqual(npm_cache_result.returncode, 0, npm_cache_result.stderr)
            npm_cache = Path(npm_cache_result.stdout.strip()).resolve()
            self.assertTrue(npm_cache.is_dir(), "existing npm cache is unavailable")
            candidates = []
            for manifest_path in sorted(npm_cache.glob("_npx/*/node_modules/skills/package.json")):
                try:
                    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    continue
                if manifest.get("name") == "skills" and manifest.get("version") == "1.5.18":
                    candidates.append(manifest_path.parents[2])
            self.assertTrue(
                candidates,
                "evidence gap: no cached skills package with exact version 1.5.18",
            )
            source_execution = candidates[0]
            copied_execution = temporary_npm_cache / "_npx" / source_execution.name
            try:
                shutil.copytree(source_execution, copied_execution, symlinks=True)
            except OSError as error:
                self.fail(f"evidence gap: unable to copy cached skills@1.5.18: {error}")
            copied_manifest = copied_execution / "node_modules" / "skills" / "package.json"
            copied_package = json.loads(copied_manifest.read_text(encoding="utf-8"))
            self.assertEqual(copied_package.get("version"), "1.5.18")
            copied_cli = copied_execution / "node_modules" / "skills" / "dist" / "cli.mjs"
            self.assertFalse(copied_cli.is_symlink())
            self.assertTrue(copied_cli.is_file(), "copied pinned CLI source is unavailable")
            cli_source = copied_cli.read_text(encoding="utf-8")
            self.assertIn("process.env.DISABLE_TELEMETRY", cli_source)
            self.assertIn("process.env.DO_NOT_TRACK", cli_source)
            self.assertIn(
                "return !process.env.DISABLE_TELEMETRY && !process.env.DO_NOT_TRACK;",
                cli_source,
            )
            before_repository = tree_snapshot(copy_root)
            before_user_roots = tree_snapshot(isolated_user_root)
            before_copied_execution = tree_snapshot(copied_execution)
            before_cache = tree_snapshot(temporary_npm_cache)
            environment = os.environ.copy()
            environment.update({key: str(path) for key, path in isolated_paths.items()})
            environment.update(
                {
                    "CI": "1",
                    "DISABLE_TELEMETRY": "1",
                    "DO_NOT_TRACK": "1",
                    "NODE_DISABLE_COMPILE_CACHE": "1",
                    "NO_UPDATE_NOTIFIER": "1",
                    "TMPDIR": str(npm_state_root),
                    "npm_config_cache": str(temporary_npm_cache),
                    "npm_config_globalconfig": str(npm_state_root / "global-npmrc"),
                    "npm_config_logs_dir": str(npm_state_root / "logs"),
                    "npm_config_offline": "true",
                    "npm_config_prefix": str(npm_prefix),
                    "npm_config_tmp": str(npm_state_root),
                    "npm_config_update_notifier": "false",
                    "npm_config_userconfig": str(npm_state_root / "npmrc"),
                }
            )
            result = subprocess.run(
                [
                    "npx",
                    "--offline",
                    "--no-install",
                    "skills@1.5.18",
                    "add",
                    str(copy_root),
                    "--list",
                ],
                cwd=copied_execution,
                env=environment,
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            combined_output = result.stdout + result.stderr
            # List mode is intentional: installation tracking is outside this test's scope.
            self.assertEqual(
                result.returncode,
                0,
                "evidence gap or discovery failure from pinned offline skills CLI:\n"
                + combined_output,
            )
            plain = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", result.stdout)
            self.assertIn("Found 1 skill", plain)
            logical_skill_lines = [
                line
                for line in plain.splitlines()
                if line.strip(" │").strip() == SKILL_NAME
            ]
            self.assertEqual(len(logical_skill_lines), 1, plain)
            self.assertEqual(
                tree_snapshot(copy_root),
                before_repository,
                "--list changed the temporary repository",
            )
            self.assertEqual(
                tree_snapshot(isolated_user_root),
                before_user_roots,
                "--list created user-level installation output",
            )
            self.assertEqual(
                tree_snapshot(copied_execution),
                before_copied_execution,
                "npx altered the copied pinned execution artifact",
            )
            after_cache = tree_snapshot(temporary_npm_cache)
            cache_changes = {
                path
                for path in set(before_cache) | set(after_cache)
                if before_cache.get(path) != after_cache.get(path)
            }
            self.assertFalse(
                {path for path in cache_changes if path.startswith("_npx/")},
                f"npx changed copied execution cache state: {sorted(cache_changes)}",
            )


if __name__ == "__main__":
    unittest.main()
