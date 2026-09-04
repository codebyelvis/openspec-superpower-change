#!/usr/bin/env python3
"""Build the generated SkillsMP catalog adapter from the root SKILL.md."""

from __future__ import annotations

import argparse
import os
import secrets
import stat
import sys
from dataclasses import dataclass
from pathlib import Path


SKILL_NAME = "openspec-superpower-change"
TARGET_NAME = "SKILL.md"
STAGE_PREFIX = f".{SKILL_NAME}.stage-"
RECOVERY_PREFIX = f".{SKILL_NAME}.recovery-"
_DIR_FD_FUNCTIONS = (os.open, os.stat, os.mkdir, os.rename, os.unlink, os.rmdir)
_MISSING_DIR_FD = tuple(
    function.__name__
    for function in _DIR_FD_FUNCTIONS
    if function not in getattr(os, "supports_dir_fd", set())
)
_FD_LISTDIR_SUPPORTED = os.listdir in getattr(os, "supports_fd", set())
_NOFOLLOW_STAT_SUPPORTED = os.stat in getattr(
    os, "supports_follow_symlinks", set()
)


@dataclass(frozen=True)
class _SourceSnapshot:
    metadata: tuple[int, int, int, int, int, int, int, int, int]
    content: bytes


@dataclass(frozen=True)
class _OutputSnapshot:
    directory: tuple[int, int, int]
    target: tuple[int, int, int]
    target_nlink: int
    target_bytes: bytes


def _identity(metadata: os.stat_result) -> tuple[int, int, int]:
    return metadata.st_dev, metadata.st_ino, metadata.st_mode


def _source_metadata(
    metadata: os.stat_result,
) -> tuple[int, int, int, int, int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_nlink,
        metadata.st_uid,
        metadata.st_gid,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _entry_type(metadata: os.stat_result) -> str:
    if stat.S_ISLNK(metadata.st_mode):
        return "symlink"
    if stat.S_ISDIR(metadata.st_mode):
        return "directory"
    if stat.S_ISREG(metadata.st_mode):
        return "regular file"
    return "special or unsupported entry"


def _require_platform_capabilities() -> None:
    if not hasattr(os, "O_NOFOLLOW"):
        raise ValueError("required O_NOFOLLOW capability is unavailable")
    if not hasattr(os, "O_DIRECTORY"):
        raise ValueError("required O_DIRECTORY capability is unavailable")
    if _MISSING_DIR_FD:
        raise ValueError(
            "required dir_fd support is unavailable for: "
            + ", ".join(_MISSING_DIR_FD)
        )
    if not _FD_LISTDIR_SUPPORTED:
        raise ValueError(
            "required supports_fd capability for descriptor listdir is unavailable"
        )
    if not _NOFOLLOW_STAT_SUPPORTED:
        raise ValueError(
            "required supports_follow_symlinks capability for no-follow stat "
            "is unavailable"
        )


def _directory_flags() -> int:
    return (
        os.O_RDONLY
        | os.O_DIRECTORY
        | os.O_NOFOLLOW
        | getattr(os, "O_CLOEXEC", 0)
    )


def _regular_flags() -> int:
    return os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)


def _stat_at(parent_fd: int, name: str) -> os.stat_result | None:
    try:
        return os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        return None


def _require_directory_at(parent_fd: int, name: str, label: str) -> os.stat_result:
    metadata = _stat_at(parent_fd, name)
    if metadata is None:
        raise ValueError(f"{label} is missing")
    entry_type = _entry_type(metadata)
    if entry_type != "directory":
        raise ValueError(f"{label} is a {entry_type}, not a regular directory")
    return metadata


def _open_directory_at(parent_fd: int, name: str, label: str) -> int:
    before = _require_directory_at(parent_fd, name, label)
    try:
        descriptor = os.open(name, _directory_flags(), dir_fd=parent_fd)
    except OSError as error:
        raise ValueError(f"unable to open bound {label}") from error
    try:
        if _identity(os.fstat(descriptor)) != _identity(before):
            raise ValueError(f"{label} binding changed while opening")
    except Exception:
        os.close(descriptor)
        raise
    return descriptor


def _read_all(descriptor: int) -> bytes:
    chunks: list[bytes] = []
    while True:
        chunk = os.read(descriptor, 1024 * 1024)
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)


def _read_source_snapshot(root_fd: int, source_name: str) -> _SourceSnapshot:
    """Read one single-link source through the retained repository fd."""
    before = _stat_at(root_fd, source_name)
    if before is None:
        raise ValueError(f"canonical root {source_name} is missing")
    if not stat.S_ISREG(before.st_mode):
        raise ValueError(f"canonical root {source_name} must be a regular file")
    if before.st_nlink != 1:
        raise ValueError(f"canonical root {source_name} must be a single-link file")
    try:
        descriptor = os.open(source_name, _regular_flags(), dir_fd=root_fd)
    except OSError as error:
        raise ValueError(f"unable to open canonical root {source_name}") from error
    try:
        opened = os.fstat(descriptor)
        if _source_metadata(opened) != _source_metadata(before):
            raise ValueError(f"canonical root {source_name} binding changed while opening")
        content = _read_all(descriptor)
        after = os.fstat(descriptor)
        live = _stat_at(root_fd, source_name)
        if (
            live is None
            or _source_metadata(after) != _source_metadata(opened)
            or _source_metadata(live) != _source_metadata(opened)
        ):
            raise ValueError(f"canonical root {source_name} changed while reading")
        return _SourceSnapshot(_source_metadata(opened), content)
    finally:
        os.close(descriptor)


def _read_target(
    adapter_fd: int, label: str
) -> tuple[bytes, tuple[int, int, int], int]:
    before = _stat_at(adapter_fd, TARGET_NAME)
    if before is None:
        raise ValueError(f"{label} target is missing")
    entry_type = _entry_type(before)
    if entry_type != "regular file":
        raise ValueError(f"{label} target is a {entry_type}, not a regular file")
    if before.st_nlink != 1:
        raise ValueError(f"{label} target must be a single-link file")
    try:
        descriptor = os.open(TARGET_NAME, _regular_flags(), dir_fd=adapter_fd)
    except OSError as error:
        raise ValueError(f"unable to open {label} target") from error
    try:
        opened = os.fstat(descriptor)
        if _identity(opened) != _identity(before) or opened.st_nlink != 1:
            raise ValueError(f"{label} target binding changed while opening")
        content = _read_all(descriptor)
        after = os.fstat(descriptor)
        live = _stat_at(adapter_fd, TARGET_NAME)
        if (
            live is None
            or _identity(after) != _identity(opened)
            or after.st_nlink != 1
            or _identity(live) != _identity(opened)
            or live.st_nlink != 1
        ):
            raise ValueError(f"{label} target changed while reading")
        return content, _identity(opened), opened.st_nlink
    finally:
        os.close(descriptor)


def _snapshot_adapter_at(
    skills_fd: int, output_name: str, label: str
) -> _OutputSnapshot:
    before = _require_directory_at(skills_fd, output_name, label)
    adapter_fd = _open_directory_at(skills_fd, output_name, label)
    try:
        names = set(os.listdir(adapter_fd))
        if names != {TARGET_NAME}:
            details: list[str] = []
            if TARGET_NAME not in names:
                details.append(f"missing {TARGET_NAME}")
            unexpected = sorted(names - {TARGET_NAME})
            if unexpected:
                details.append("unexpected entries: " + ", ".join(unexpected))
            raise ValueError(
                f"{label} must contain exactly {TARGET_NAME} ("
                + "; ".join(details)
                + ")"
            )
        target_bytes, target_identity, target_nlink = _read_target(adapter_fd, label)
        after = os.fstat(adapter_fd)
        live = _stat_at(skills_fd, output_name)
        if (
            live is None
            or _identity(after) != _identity(before)
            or _identity(live) != _identity(before)
        ):
            raise ValueError(f"{label} binding changed during snapshot")
        return _OutputSnapshot(
            _identity(after), target_identity, target_nlink, target_bytes
        )
    finally:
        os.close(adapter_fd)


def _check_replaceable_output(
    skills_fd: int, output_name: str
) -> _OutputSnapshot | None:
    """Validate only the builder-owned output name through the skills fd."""
    if output_name != SKILL_NAME:
        raise ValueError(f"SkillsMP adapter output name must equal {SKILL_NAME}")
    metadata = _stat_at(skills_fd, output_name)
    if metadata is None:
        return None
    entry_type = _entry_type(metadata)
    if entry_type != "directory":
        raise ValueError(
            f"SkillsMP adapter directory is a {entry_type}, not a regular directory"
        )
    return _snapshot_adapter_at(skills_fd, output_name, "SkillsMP adapter directory")


def _install_staged_adapter(
    skills_fd: int, stage_name: str, output_name: str
) -> None:
    """Install the staged directory inside the retained skills namespace."""
    os.rename(
        stage_name,
        output_name,
        src_dir_fd=skills_fd,
        dst_dir_fd=skills_fd,
    )


def _restore_recovery(
    skills_fd: int, recovery_name: str, output_name: str
) -> None:
    """Restore the captured directory inside the retained skills namespace."""
    os.rename(
        recovery_name,
        output_name,
        src_dir_fd=skills_fd,
        dst_dir_fd=skills_fd,
    )


def _verify_restored_snapshot(
    skills_fd: int, output_name: str, snapshot: _OutputSnapshot
) -> bool:
    """Return whether compensation restored the exact captured object state."""
    try:
        return _snapshot_adapter_at(
            skills_fd, output_name, "restored SkillsMP adapter"
        ) == snapshot
    except (OSError, ValueError):
        return False


def _open_root(root: Path) -> tuple[int, tuple[int, int, int]]:
    try:
        before = root.stat(follow_symlinks=False)
    except FileNotFoundError as error:
        raise ValueError(f"repository root is missing: {root}") from error
    entry_type = _entry_type(before)
    if entry_type != "directory":
        raise ValueError(f"repository root is a {entry_type}, not a regular directory")
    try:
        root_fd = os.open(root, _directory_flags())
    except OSError as error:
        raise ValueError(
            f"unable to open repository root without following links: {root}"
        ) from error
    try:
        identity = _identity(os.fstat(root_fd))
        if identity != _identity(before):
            raise ValueError("repository root binding changed while opening")
        return root_fd, identity
    except Exception:
        os.close(root_fd)
        raise


def _verify_live_bindings(
    root: Path,
    root_identity: tuple[int, int, int],
    skills_identity: tuple[int, int, int] | None = None,
) -> None:
    live_root, live_root_identity = _open_root(root)
    live_skills: int | None = None
    try:
        if live_root_identity != root_identity:
            raise ValueError("repository root pathname binding changed")
        if skills_identity is not None:
            live_skills = _open_directory_at(
                live_root, "skills", "SkillsMP skills parent"
            )
            if _identity(os.fstat(live_skills)) != skills_identity:
                raise ValueError("SkillsMP skills parent pathname binding changed")
    finally:
        if live_skills is not None:
            os.close(live_skills)
        os.close(live_root)


def _open_or_create_skills(
    root_fd: int,
) -> tuple[int, tuple[int, int, int], bool]:
    metadata = _stat_at(root_fd, "skills")
    created = False
    if metadata is None:
        os.mkdir("skills", 0o755, dir_fd=root_fd)
        created = True
    elif _entry_type(metadata) != "directory":
        raise ValueError(
            f"SkillsMP skills parent is a {_entry_type(metadata)}, not a regular directory"
        )
    skills_fd = _open_directory_at(root_fd, "skills", "SkillsMP skills parent")
    return skills_fd, _identity(os.fstat(skills_fd)), created


def _residue_names(skills_fd: int) -> list[str]:
    return sorted(
        name
        for name in os.listdir(skills_fd)
        if name.startswith((STAGE_PREFIX, RECOVERY_PREFIX))
    )


def _reject_unknown_residue(skills_fd: int, allowed: set[str]) -> None:
    unknown = [name for name in _residue_names(skills_fd) if name not in allowed]
    if unknown:
        raise ValueError(
            "refusing to build while unknown SkillsMP staging/recovery residue "
            "is present: " + ", ".join(unknown)
        )


def _new_absent_name(skills_fd: int, prefix: str) -> str:
    for _ in range(128):
        name = prefix + secrets.token_hex(12)
        if _stat_at(skills_fd, name) is None:
            return name
    raise RuntimeError(f"unable to reserve a unique {prefix} entry name")


def _create_stage(
    skills_fd: int, source: _SourceSnapshot
) -> tuple[str, int, _OutputSnapshot]:
    for _ in range(128):
        stage_name = _new_absent_name(skills_fd, STAGE_PREFIX)
        try:
            os.mkdir(stage_name, 0o700, dir_fd=skills_fd)
        except FileExistsError:
            continue
        stage_fd: int | None = None
        try:
            stage_fd = _open_directory_at(skills_fd, stage_name, "staged adapter")
            os.fchmod(stage_fd, 0o755)
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
            target_fd = os.open(TARGET_NAME, flags, 0o644, dir_fd=stage_fd)
            try:
                remaining = memoryview(source.content)
                while remaining:
                    written = os.write(target_fd, remaining)
                    if written <= 0:
                        raise OSError("unable to write staged SkillsMP adapter")
                    remaining = remaining[written:]
                os.fchmod(target_fd, 0o644)
            finally:
                os.close(target_fd)
            snapshot = _snapshot_adapter_at(skills_fd, stage_name, "staged adapter")
            if snapshot.target_bytes != source.content:
                raise RuntimeError("staged SkillsMP adapter differs from canonical source")
            return stage_name, stage_fd, snapshot
        except Exception:
            if stage_fd is not None:
                os.close(stage_fd)
            raise
    raise RuntimeError("unable to create a unique SkillsMP staging directory")


def _same_objects(skills_fd: int, name: str, snapshot: _OutputSnapshot) -> bool:
    metadata = _stat_at(skills_fd, name)
    if (
        metadata is None
        or not stat.S_ISDIR(metadata.st_mode)
        or (metadata.st_dev, metadata.st_ino) != snapshot.directory[:2]
    ):
        return False
    try:
        descriptor = _open_directory_at(skills_fd, name, "captured adapter evidence")
    except (OSError, ValueError):
        return False
    try:
        if set(os.listdir(descriptor)) != {TARGET_NAME}:
            return False
        target = _stat_at(descriptor, TARGET_NAME)
        return bool(
            target is not None
            and stat.S_ISREG(target.st_mode)
            and target.st_nlink == 1
            and (target.st_dev, target.st_ino) == snapshot.target[:2]
        )
    finally:
        os.close(descriptor)


def _move_owned(
    skills_fd: int,
    source_name: str,
    destination_name: str,
    snapshot: _OutputSnapshot,
) -> None:
    if not _same_objects(skills_fd, source_name, snapshot):
        raise RuntimeError(f"refusing to move identity-mismatched adapter: {source_name}")
    if _stat_at(skills_fd, destination_name) is not None:
        raise RuntimeError(f"refusing to replace unexpected entry: {destination_name}")
    os.rename(
        source_name,
        destination_name,
        src_dir_fd=skills_fd,
        dst_dir_fd=skills_fd,
    )
    if not _same_objects(skills_fd, destination_name, snapshot):
        raise RuntimeError(f"adapter identity changed while moving to {destination_name}")


def _remove_owned(skills_fd: int, name: str, snapshot: _OutputSnapshot) -> None:
    if _snapshot_adapter_at(skills_fd, name, "builder-owned adapter") != snapshot:
        raise RuntimeError(f"refusing to clean unverified builder entry: {name}")
    descriptor = _open_directory_at(skills_fd, name, "builder-owned adapter")
    try:
        target = _stat_at(descriptor, TARGET_NAME)
        if (
            target is None
            or not stat.S_ISREG(target.st_mode)
            or target.st_nlink != 1
            or _identity(target) != snapshot.target
        ):
            raise RuntimeError(f"builder-owned target changed before cleanup: {name}")
        os.unlink(TARGET_NAME, dir_fd=descriptor)
        if os.listdir(descriptor):
            raise RuntimeError(f"builder-owned directory changed during cleanup: {name}")
    finally:
        os.close(descriptor)
    live = _stat_at(skills_fd, name)
    if live is None or (live.st_dev, live.st_ino) != snapshot.directory[:2]:
        raise RuntimeError(f"builder-owned directory changed before removal: {name}")
    # Ordinary stage cleanup remains rejecting; recovery deletion uses the
    # explicit unlink commit point below.
    os.rmdir(name, dir_fd=skills_fd)


def _commit_recovery_cleanup(
    skills_fd: int, name: str, snapshot: _OutputSnapshot, on_commit
) -> None:
    """Delete the last prior-state link, then perform only best-effort cleanup."""
    if _snapshot_adapter_at(skills_fd, name, "builder-owned recovery") != snapshot:
        raise RuntimeError(f"refusing to clean unverified recovery entry: {name}")
    descriptor = _open_directory_at(skills_fd, name, "builder-owned recovery")
    try:
        target = _stat_at(descriptor, TARGET_NAME)
        if (
            target is None
            or not stat.S_ISREG(target.st_mode)
            or target.st_nlink != 1
            or _identity(target) != snapshot.target
        ):
            raise RuntimeError(f"recovery target changed before commit: {name}")
        os.unlink(TARGET_NAME, dir_fd=descriptor)
    except Exception:
        os.close(descriptor)
        raise

    # Unlink is the recovery commit point: exact prior bytes no longer exist.
    # Publish that state before any cleanup which can race or fail.
    on_commit()
    try:
        entries = os.listdir(descriptor)
    except Exception:
        entries = None
    finally:
        try:
            os.close(descriptor)
        except OSError:
            pass
    if entries:
        return
    if entries is None:
        return
    try:
        live = _stat_at(skills_fd, name)
        if live is None or (live.st_dev, live.st_ino) != snapshot.directory[:2]:
            return
        os.rmdir(name, dir_fd=skills_fd)
    except Exception:
        return


def _retain_unproven(
    skills_fd: int,
    output_name: str,
    recovery_name: str,
    snapshot: _OutputSnapshot,
) -> str:
    if _same_objects(skills_fd, recovery_name, snapshot):
        return recovery_name
    if not _same_objects(skills_fd, output_name, snapshot):
        if _stat_at(skills_fd, recovery_name) is not None:
            return recovery_name
        if _stat_at(skills_fd, output_name) is not None:
            return output_name
        return "."
    if _stat_at(skills_fd, recovery_name) is not None:
        return recovery_name
    _move_owned(skills_fd, output_name, recovery_name, snapshot)
    if _stat_at(skills_fd, output_name) is not None:
        raise RuntimeError("canonical adapter output remained after recovery relocation")
    return recovery_name


def _evidence_diagnostic(root: Path, skills_fd: int, name: str) -> str:
    retained = os.fstat(skills_fd)
    return (
        f"untrusted lexical path {root / 'skills' / name}; "
        f"recovery entry {name!r}; retained skills identity "
        f"dev={retained.st_dev}, inode={retained.st_ino}"
    )


def _compensate(
    skills_fd: int,
    root: Path,
    existing: _OutputSnapshot | None,
    stage_name: str,
    stage_snapshot: _OutputSnapshot,
    recovery_name: str | None,
    install_error: Exception,
) -> None:
    evidence_name: str | None = None
    try:
        if _same_objects(skills_fd, SKILL_NAME, stage_snapshot):
            _move_owned(skills_fd, SKILL_NAME, stage_name, stage_snapshot)
        elif _stat_at(skills_fd, SKILL_NAME) is not None:
            raise RuntimeError(
                "canonical adapter output is an unknown object; refusing to replace it"
            )
        if existing is not None:
            assert recovery_name is not None
            if _stat_at(skills_fd, SKILL_NAME) is not None:
                evidence_name = (
                    recovery_name
                    if _stat_at(skills_fd, recovery_name) is not None
                    else SKILL_NAME
                )
                raise RuntimeError("canonical adapter output is occupied during recovery")
            _restore_recovery(skills_fd, recovery_name, SKILL_NAME)
            verifier_error: Exception | None = None
            try:
                restored = _verify_restored_snapshot(skills_fd, SKILL_NAME, existing)
            except Exception as error:
                restored = False
                verifier_error = error
            if not restored:
                evidence_name = _retain_unproven(
                    skills_fd, SKILL_NAME, recovery_name, existing
                )
                detail = f": {verifier_error}" if verifier_error is not None else ""
                raise RuntimeError(
                    "restored SkillsMP adapter snapshot could not be proven; "
                    "evidence remains at "
                    f"{_evidence_diagnostic(root, skills_fd, evidence_name)}{detail}"
                )
    except Exception as compensation_error:
        if evidence_name is None:
            if recovery_name and _stat_at(skills_fd, recovery_name) is not None:
                evidence_name = recovery_name
            elif _stat_at(skills_fd, SKILL_NAME) is not None:
                evidence_name = SKILL_NAME
            else:
                evidence_name = "."
        raise RuntimeError(
            "SkillsMP adapter install failed and exact compensation was not proven; "
            "inspect recovery evidence at "
            f"{_evidence_diagnostic(root, skills_fd, evidence_name)}: "
            f"{compensation_error}"
        ) from install_error
    raise install_error


def _cleanup_created_skills(
    root_fd: int,
    skills_fd: int,
    skills_identity: tuple[int, int, int],
) -> None:
    if os.listdir(skills_fd):
        return
    live = _stat_at(root_fd, "skills")
    if (
        live is None
        or _identity(os.fstat(skills_fd)) != skills_identity
        or _identity(live) != skills_identity
    ):
        raise RuntimeError("refusing to remove identity-mismatched skills parent")
    os.rmdir("skills", dir_fd=root_fd)


def build(root: Path = Path(".")) -> Path:
    """Generate and atomically install the nested SkillsMP adapter."""
    _require_platform_capabilities()
    root = Path(os.path.abspath(os.path.expanduser(os.fspath(root))))
    root_fd, root_identity = _open_root(root)
    skills_fd: int | None = None
    skills_identity: tuple[int, int, int] | None = None
    skills_created = False
    stage_fd: int | None = None
    stage_name: str | None = None
    stage_snapshot: _OutputSnapshot | None = None
    recovery_name: str | None = None
    recovery_committed = False
    try:
        source = _read_source_snapshot(root_fd, TARGET_NAME)
        if _read_source_snapshot(root_fd, TARGET_NAME) != source:
            raise ValueError("canonical root SKILL.md changed during initial capture")
        _verify_live_bindings(root, root_identity)
        skills_fd, skills_identity, skills_created = _open_or_create_skills(root_fd)
        _verify_live_bindings(root, root_identity, skills_identity)
        existing = _check_replaceable_output(skills_fd, SKILL_NAME)
        _reject_unknown_residue(skills_fd, set())
        if _read_source_snapshot(root_fd, TARGET_NAME) != source:
            raise ValueError("canonical root SKILL.md changed before staging")

        stage_name, stage_fd, stage_snapshot = _create_stage(skills_fd, source)
        allowed = {stage_name}
        _reject_unknown_residue(skills_fd, allowed)
        current = _check_replaceable_output(skills_fd, SKILL_NAME)
        if current != existing:
            raise ValueError("existing SkillsMP adapter changed during build")
        if _read_source_snapshot(root_fd, TARGET_NAME) != source:
            raise ValueError("canonical root SKILL.md changed before install")
        _verify_live_bindings(root, root_identity, skills_identity)
        _reject_unknown_residue(skills_fd, allowed)

        if existing is not None:
            recovery_name = _new_absent_name(skills_fd, RECOVERY_PREFIX)
            _move_owned(skills_fd, SKILL_NAME, recovery_name, existing)
            allowed.add(recovery_name)
            if _snapshot_adapter_at(
                skills_fd, recovery_name, "captured recovery adapter"
            ) != existing:
                raise RuntimeError(
                    f"captured SkillsMP recovery cannot be verified: {recovery_name}"
                )
            _reject_unknown_residue(skills_fd, allowed)

        try:
            _install_staged_adapter(skills_fd, stage_name, SKILL_NAME)
            allowed.discard(stage_name)
            installed = _snapshot_adapter_at(
                skills_fd, SKILL_NAME, "installed SkillsMP adapter"
            )
            if installed != stage_snapshot:
                raise RuntimeError(
                    "installed SkillsMP adapter identity is not the staged identity"
                )
            if _read_source_snapshot(root_fd, TARGET_NAME) != source:
                raise ValueError("canonical root SKILL.md changed during install")
            _verify_live_bindings(root, root_identity, skills_identity)
            _reject_unknown_residue(skills_fd, allowed)

            final_source = _read_source_snapshot(root_fd, TARGET_NAME)
            final_output = _snapshot_adapter_at(
                skills_fd, SKILL_NAME, "generated SkillsMP adapter"
            )
            if final_source != source or final_output != stage_snapshot:
                raise RuntimeError(
                    "SkillsMP adapter or canonical source changed before success"
                )
            _reject_unknown_residue(skills_fd, allowed)
            _verify_live_bindings(root, root_identity, skills_identity)

            if existing is not None:
                assert recovery_name is not None
                if _snapshot_adapter_at(
                    skills_fd, recovery_name, "verified recovery adapter"
                ) != existing:
                    raise RuntimeError(
                        "refusing to delete unverified recovery evidence: "
                        f"{recovery_name}"
                    )
                if stage_fd is not None:
                    os.close(stage_fd)
                    stage_fd = None

                def mark_recovery_committed() -> None:
                    nonlocal recovery_committed, recovery_name
                    recovery_committed = True
                    recovery_name = None

                _commit_recovery_cleanup(
                    skills_fd, recovery_name, existing, mark_recovery_committed
                )
        except Exception as install_error:
            _compensate(
                skills_fd,
                root,
                existing,
                stage_name,
                stage_snapshot,
                recovery_name,
                install_error,
            )
        return root / "skills" / SKILL_NAME / TARGET_NAME
    finally:
        primary_error = sys.exception()
        cleanup_errors: list[Exception] = []
        if not recovery_committed:
            try:
                if (
                    skills_fd is not None
                    and stage_name is not None
                    and stage_snapshot is not None
                    and _stat_at(skills_fd, stage_name) is not None
                ):
                    _remove_owned(skills_fd, stage_name, stage_snapshot)
            except Exception as error:
                cleanup_errors.append(error)
        if stage_fd is not None:
            try:
                os.close(stage_fd)
            except OSError as error:
                cleanup_errors.append(error)
        if (
            not recovery_committed
            and skills_created
            and skills_fd is not None
            and skills_identity is not None
        ):
            try:
                _cleanup_created_skills(root_fd, skills_fd, skills_identity)
            except Exception as error:
                cleanup_errors.append(error)
        if skills_fd is not None:
            try:
                os.close(skills_fd)
            except OSError as error:
                cleanup_errors.append(error)
        try:
            os.close(root_fd)
        except OSError as error:
            cleanup_errors.append(error)
        if cleanup_errors and primary_error is not None:
            detail = "; ".join(str(error) for error in cleanup_errors)
            primary_error.add_note(f"secondary SkillsMP cleanup failure: {detail}")
        elif cleanup_errors and not recovery_committed:
            detail = "; ".join(str(error) for error in cleanup_errors)
            raise RuntimeError(f"SkillsMP adapter cleanup failed: {detail}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", type=Path)
    args = parser.parse_args(argv)
    try:
        generated = build(args.root)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"FAIL: {error}")
        return 1
    print(f"generated {generated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
