#!/opt/anaconda3/bin/python3.11
"""Complete fail-closed executor for the approved v2 source bootstrap."""

import ctypes
import datetime
import fcntl
import hashlib
import json
import os
import stat
import struct
import subprocess
import sys


ROOT = "/Users/elvis/file/develop/opensource/openspec-superpower-change"
GIT_DIR = ROOT + "/.git"
GIT = "/opt/homebrew/Cellar/git/2.49.0/bin/git"
PYTHON = "/opt/anaconda3/bin/python3.11"
SANDBOX = "/usr/bin/sandbox-exec"
BASE_COMMIT = "92fce4cfea0fbaf0dd1dfbcc7cc320a5aafa7958"
BASE_TREE = "9799a5f6add566977e4e997bce57314fc81f28c4"
BRANCH = "add-codex-skill-update-v2"
BRANCH_REF = "refs/heads/" + BRANCH
TARGET_PARENT = "/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change"
TARGET_PATH = TARGET_PARENT + "/" + BRANCH
ADMIN_PATH = GIT_DIR + "/worktrees/" + BRANCH
APPROVAL_REL = "openspec/changes/add-codex-skill-update/approvals"
APPROVAL_DIR = ROOT + "/" + APPROVAL_REL
SOURCE_BOOTSTRAP_DIR = APPROVAL_DIR + "/source-bootstrap"
HELPER_REL = "docs/design/evidence/add-codex-skill-update/source-bootstrap-v2-helper.py"
HELPER_ABS = ROOT + "/" + HELPER_REL
PRESTATE_REL = "docs/design/evidence/add-codex-skill-update/source-bootstrap-v2-prestate.json"
LOCK_NAME = "source-bootstrap.lock"
JOURNAL_NAME = "recovery-v2-journal.jsonl"
ZERO_OID = "0" * 40
REFLOG_IDENTITY = "Codex Source Bootstrap <noreply@localhost> 1785816000 +0800"
CONTRACT_PATHS = (
    "openspec/changes/add-codex-skill-update/design.md",
    "openspec/changes/add-codex-skill-update/proposal.md",
    "openspec/changes/add-codex-skill-update/specs/skill-update-governance/spec.md",
    "openspec/changes/add-codex-skill-update/tasks.md",
)
PROFILE_PREFIX = APPROVAL_REL + "/source-bootstrap/profiles/"
EXPECTED_EXECUTABLES = {
    GIT: "03d4a6c5328d4a1ce84eba2765664284b1fb2414d9e657358733056a89a95954",
    PYTHON: "809bbac201b0d8f556186ae68533f9d40c5ccbe16c8875903590aa840fd67d59",
    SANDBOX: "8290e4be7387a0df83cd1559e86afd880464f269450573d012795761fe298f16",
}
EXPECTED_FIXED_ENVIRONMENT = {
    "LANG": "C",
    "LC_ALL": "C",
    "PATH": "/nonexistent",
    "PYTHONDONTWRITEBYTECODE": "1",
}
EXPECTED_CONTROL_PLANE_INSTANCE = "codex-cli@elvisdeMacBook-Pro.local:elvis"
EXPECTED_FD_PROTOCOL = [
    "open and retain repository root no-follow",
    "open and retain Git common directory no-follow",
    "open and retain .git/refs/heads no-follow",
    "open and retain .git/logs/refs/heads no-follow",
    "open and retain .git/worktrees no-follow",
    "open and retain worktree parent no-follow",
    "open and retain approval directory no-follow",
    "open and retain source-bootstrap directory no-follow",
    "re-fstat, phase-bound APFS nlink, and descriptor-relative no-follow identity checks before first write",
    "descriptor-relative verified lock plus no-replace journal/ref/reflog/admin/target/material/index writes and fsync",
]

# The reviewed prestate is captured before the new immutable authorization
# manifest exists. On the bound APFS volume, a directory's st_nlink increases
# for every durable immediate child entry, including regular files. Each phase
# therefore admits only the exact entries that the approved protocol has made
# durable by that boundary. No other parent-closure metadata may drift.
PARENT_NLINK_DELTAS = {
    "approval-recorded": {
        APPROVAL_DIR: 1,  # immutable authorization manifest
    },
    "journal-ready": {
        APPROVAL_DIR: 2,  # manifest plus held source-bootstrap lock
        SOURCE_BOOTSTRAP_DIR: 1,  # recovery journal
    },
    "post-bootstrap": {
        APPROVAL_DIR: 2,
        SOURCE_BOOTSTRAP_DIR: 1,
        GIT_DIR + "/refs/heads": 1,  # final loose branch ref
        GIT_DIR + "/logs/refs/heads": 1,  # final loose branch reflog
        GIT_DIR + "/worktrees": 1,  # worktree-admin directory
        TARGET_PARENT: 1,  # replacement worktree directory
    },
}
GIT_ENVIRONMENT = {
    "GIT_ALLOW_PROTOCOL": "",
    "GIT_ASKPASS": "/nonexistent",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_SYSTEM": "/dev/null",
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_PAGER": "",
    "GIT_PROTOCOL_FROM_USER": "0",
    "GIT_TERMINAL_PROMPT": "0",
    "HOME": "/private/tmp/openspec-source-bootstrap-home-v2-empty",
    "LANG": "C",
    "LC_ALL": "C",
    "PAGER": "",
    "PATH": "/nonexistent",
    "SSH_ASKPASS": "/nonexistent",
    "XDG_CONFIG_HOME": "/private/tmp/openspec-source-bootstrap-xdg-v2-empty",
}
EXPECTED_PROFILE = f"""(version 1)
(deny default)
(deny network*)
(allow file-read*)
(allow process-info*)
(allow sysctl-read)
(allow mach-lookup)
(allow process-fork)
(allow process-exec
  (literal "{PYTHON}")
  (literal "{GIT}"))
(allow file-write*
  (literal "/dev/null")
  (literal "{APPROVAL_DIR}/{LOCK_NAME}")
  (literal "{SOURCE_BOOTSTRAP_DIR}/{JOURNAL_NAME}")
  (literal "{GIT_DIR}/refs/heads/{BRANCH}")
  (literal "{GIT_DIR}/refs/heads/{BRANCH}.lock")
  (literal "{GIT_DIR}/logs/refs/heads/{BRANCH}")
  (literal "{GIT_DIR}/logs/refs/heads/{BRANCH}.lock")
  (literal "{ADMIN_PATH}")
  (subpath "{ADMIN_PATH}")
  (literal "{TARGET_PATH}")
  (subpath "{TARGET_PATH}"))
""".encode()
SANDBOX_EXEC_VECTOR = [
    SANDBOX, "-p", EXPECTED_PROFILE.decode("utf-8"), PYTHON, "-I", "-S",
    HELPER_ABS, "--contained",
]


class Blocked(Exception):
    pass


JOURNAL_FD = None
MANIFEST_SHA256 = None


def block(message):
    raise Blocked(message)


def expected_parent_nlink(path, baseline, phase):
    if phase not in PARENT_NLINK_DELTAS:
        block(f"unknown parent-link validation phase: {phase}")
    return baseline + PARENT_NLINK_DELTAS[phase].get(path, 0)


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def sha256_regular_path(path):
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as error:
        block(f"cannot open bound executable {path}: {error}")
    try:
        value = os.fstat(fd)
        if not stat.S_ISREG(value.st_mode):
            block(f"bound executable is not regular: {path}")
        digest = hashlib.sha256()
        while True:
            chunk = os.read(fd, 1024 * 1024)
            if not chunk:
                return digest.hexdigest()
            digest.update(chunk)
    finally:
        os.close(fd)


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sandbox_exec_vector_sha256():
    return sha256_bytes(b"source-worktree-sandbox-exec-vector-v1\0" +
                        canonical_json({"argv": SANDBOX_EXEC_VECTOR, "schema": 1}))


def safe_parts(path):
    if not isinstance(path, str) or not path or path.startswith("/") or "\\" in path:
        block(f"unsafe relative path: {path!r}")
    parts = path.split("/")
    if any(part in ("", ".", "..") for part in parts):
        block(f"unsafe relative path: {path!r}")
    path.encode("utf-8")
    return parts


def open_directory(path):
    if not os.path.isabs(path):
        block(f"directory path is not absolute: {path}")
    try:
        current = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError as error:
        block(f"cannot retain filesystem root: {error}")
    try:
        for part in [item for item in path.split("/") if item]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=current)
            os.close(current)
            current = child
        return current
    except OSError as error:
        os.close(current)
        block(f"cannot retain no-follow directory {path}: {error}")


def open_relative_directory(root_fd, relative_path):
    parts = safe_parts(relative_path)
    current = os.dup(root_fd)
    try:
        for part in parts:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=current)
            os.close(current)
            current = child
        return current
    except OSError as error:
        os.close(current)
        block(f"cannot retain relative directory {relative_path}: {error}")


def directory_identity(fd, label):
    try:
        value = os.fstat(fd)
    except OSError as error:
        block(f"cannot fstat {label}: {error}")
    if not stat.S_ISDIR(value.st_mode):
        block(f"{label} is not a directory")
    return value


def require_same_directory(left_fd, right_fd, label):
    left = directory_identity(left_fd, label + " retained")
    right = directory_identity(right_fd, label + " reopened")
    if (left.st_dev, left.st_ino) != (right.st_dev, right.st_ino):
        block(f"descriptor/lexical directory continuity drift: {label}")


def verify_retained_bindings(prestate, repo_fd, git_fd, refs_fd, logs_fd, worktrees_fd,
                             target_parent_fd, approval_fd, source_bootstrap_fd, phase):
    expected = {entry["path"]: entry for entry in prestate["parent_closure"]}
    retained_by_path = {
        ROOT: repo_fd,
        GIT_DIR: git_fd,
        GIT_DIR + "/refs/heads": refs_fd,
        GIT_DIR + "/logs/refs/heads": logs_fd,
        GIT_DIR + "/worktrees": worktrees_fd,
        TARGET_PARENT: target_parent_fd,
        APPROVAL_DIR: approval_fd,
        SOURCE_BOOTSTRAP_DIR: source_bootstrap_fd,
    }
    for path, fd in retained_by_path.items():
        if path not in expected:
            block(f"retained directory absent from prestate closure: {path}")
        value = directory_identity(fd, path)
        entry = expected[path]
        expected_nlink = expected_parent_nlink(path, entry["nlink"], phase)
        if ((value.st_dev, value.st_ino, value.st_uid,
             format(stat.S_IMODE(value.st_mode), "04o"), value.st_nlink) !=
                (entry["dev"], entry["ino"], entry["uid"], entry["mode"], expected_nlink)):
            block(f"retained directory prestate identity drift: {path}")

    reopened = []
    try:
        reopened_repo = open_directory(ROOT)
        reopened.append(reopened_repo)
        require_same_directory(repo_fd, reopened_repo, "repository root")
        for relative_path, retained_fd, label in (
                (".git", git_fd, "Git common directory"),
                (".git/refs/heads", refs_fd, "branch-ref parent"),
                (".git/logs/refs/heads", logs_fd, "branch-reflog parent"),
                (".git/worktrees", worktrees_fd, "worktree-admin parent"),
                ("openspec/changes/add-codex-skill-update/approvals", approval_fd,
                 "approval directory"),
                ("openspec/changes/add-codex-skill-update/approvals/source-bootstrap",
                 source_bootstrap_fd, "source-bootstrap directory")):
            current = open_relative_directory(reopened_repo, relative_path)
            reopened.append(current)
            require_same_directory(retained_fd, current, label)
        reopened_target_parent = open_directory(TARGET_PARENT)
        reopened.append(reopened_target_parent)
        require_same_directory(target_parent_fd, reopened_target_parent, "worktree parent")
    finally:
        for fd in reversed(reopened):
            os.close(fd)


def open_parent(root_fd, relative_path, create=False):
    parts = safe_parts(relative_path)
    current = os.dup(root_fd)
    try:
        for part in parts[:-1]:
            try:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current)
            except FileNotFoundError:
                if not create:
                    raise
                os.mkdir(part, 0o755, dir_fd=current)
                os.fsync(current)
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current)
                os.fchmod(child, 0o755)
                os.fsync(child)
            os.close(current)
            current = child
        return current, parts[-1]
    except OSError as error:
        os.close(current)
        block(f"cannot traverse {relative_path!r}: {error}")


def read_regular(root_fd, relative_path, max_size=64 * 1024 * 1024):
    parent, name = open_parent(root_fd, relative_path)
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent)
    except OSError as error:
        os.close(parent)
        block(f"cannot read {relative_path!r}: {error}")
    try:
        value = os.fstat(fd)
        if not stat.S_ISREG(value.st_mode) or value.st_nlink != 1 or value.st_size > max_size:
            block(f"unsafe source file: {relative_path!r}")
        chunks = []
        remaining = value.st_size
        while remaining:
            data = os.read(fd, min(1024 * 1024, remaining))
            if not data:
                block(f"short read: {relative_path!r}")
            chunks.append(data)
            remaining -= len(data)
        return b"".join(chunks), stat.S_IMODE(value.st_mode)
    finally:
        os.close(fd)
        os.close(parent)


def inventory_regular_files(root_fd, prefix=""):
    observed_files = []
    observed_directories = {}
    for name in sorted(os.listdir(root_fd), key=lambda item: item.encode("utf-8")):
        if not name or name in (".", "..") or "/" in name or "\\" in name:
            block(f"unsafe inventory entry: {name!r}")
        relative = prefix + name
        try:
            value = os.stat(name, dir_fd=root_fd, follow_symlinks=False)
        except OSError as error:
            block(f"cannot inventory {relative}: {error}")
        if stat.S_ISDIR(value.st_mode) and not stat.S_ISLNK(value.st_mode):
            if value.st_uid != os.getuid():
                block(f"inventory directory owner mismatch: {relative}")
            observed_directories[relative] = stat.S_IMODE(value.st_mode)
            try:
                child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                dir_fd=root_fd)
            except OSError as error:
                block(f"cannot retain inventory directory {relative}: {error}")
            try:
                child_files, child_directories = inventory_regular_files(child, relative + "/")
                observed_files.extend(child_files)
                observed_directories.update(child_directories)
            finally:
                os.close(child)
        elif stat.S_ISREG(value.st_mode) and value.st_nlink == 1:
            observed_files.append(relative)
        else:
            block(f"non-regular or linked inventory entry: {relative}")
    return observed_files, observed_directories


def write_new(root_fd, relative_path, payload, mode):
    parent, name = open_parent(root_fd, relative_path, create=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    try:
        fd = os.open(name, flags, mode, dir_fd=parent)
    except OSError as error:
        os.close(parent)
        block(f"cannot create {relative_path!r}: {error}")
    try:
        os.fchmod(fd, mode)
        view = memoryview(payload)
        while view:
            written = os.write(fd, view)
            if written <= 0:
                block(f"short write: {relative_path!r}")
            view = view[written:]
        os.fsync(fd)
    finally:
        os.close(fd)
    os.fsync(parent)
    os.close(parent)


def promote_no_replace(parent_fd, lock_name, final_name, label):
    try:
        os.link(lock_name, final_name, src_dir_fd=parent_fd, dst_dir_fd=parent_fd,
                follow_symlinks=False)
    except OSError as error:
        block(f"cannot no-replace promote {label}: {error}")
    os.fsync(parent_fd)
    try:
        os.unlink(lock_name, dir_fd=parent_fd)
    except OSError as error:
        block(f"cannot remove promoted lock for {label}: {error}")
    os.fsync(parent_fd)


def require_absent(parent_fd, name, label):
    try:
        os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        return
    except OSError as error:
        block(f"cannot prove absence of {label}: {error}")
    block(f"expected-absent path is present: {label}")


def run_git(arguments, cwd=ROOT):
    command = [GIT, *arguments]
    result = subprocess.run(command, cwd=cwd, env=GIT_ENVIRONMENT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        block(f"read-only Git command failed {arguments!r}: {result.stderr.decode('utf-8', 'replace')}")
    return result.stdout


def parse_worktrees(raw):
    worktrees = []
    record = {}
    for line in raw.decode("utf-8").splitlines() + [""]:
        if not line:
            if record:
                worktrees.append({"path": record["worktree"], "head": record["HEAD"],
                                  "branch": record.get("branch")})
                record = {}
            continue
        key, *rest = line.split(" ", 1)
        record[key] = rest[0] if rest else True
    return sorted(worktrees, key=lambda item: item["path"].encode())


def observed_refs(excluded_prefix):
    raw = run_git(["for-each-ref", "--format=%(refname)%09%(objectname)%09%(objecttype)"])
    values = []
    for line in raw.decode("utf-8").splitlines():
        name, oid, object_type = line.split("\t")
        if name.startswith(excluded_prefix):
            continue
        values.append({"name": name, "object_oid": oid, "object_type": object_type})
    return sorted(values, key=lambda item: (item["name"].encode(), item["object_oid"].encode(),
                                            item["object_type"].encode()))


def contract_projection(artifact_bytes):
    normalized = {}
    for path, raw in artifact_bytes.items():
        if path.endswith("proposal.md") or path.endswith("tasks.md"):
            lines = raw.splitlines(keepends=True)
            fixed = []
            for line in lines:
                if line.startswith((b"- [ ]", b"- [x]", b"- [X]")):
                    line = b"- [ ]" + line[5:]
                fixed.append(line)
            raw = b"".join(fixed)
        normalized[path.removeprefix("openspec/changes/add-codex-skill-update/")] = raw
    files = [{"path": path, "sha256": sha256_bytes(raw)}
             for path, raw in sorted(normalized.items(), key=lambda item: item[0].encode())]
    return sha256_bytes(b"openspec-major-contract-projection-v1\0" +
                        canonical_json({"files": files, "schema": 1}))


def validate_quarantines(value, phase):
    for quarantine in value["quarantines"]:
        try:
            worktree = os.lstat(quarantine["worktree_path"])
            admin = os.lstat(quarantine["worktree_admin_path"])
        except OSError as error:
            block(f"{phase} quarantine identity unavailable: {error}")
        if (worktree.st_dev, worktree.st_ino) != (quarantine["worktree_dev"],
                                                  quarantine["worktree_ino"]):
            block(f"{phase} quarantined worktree identity drift")
        if (admin.st_dev, admin.st_ino) != (quarantine["worktree_admin_dev"],
                                            quarantine["worktree_admin_ino"]):
            block(f"{phase} quarantined admin identity drift")
        quarantine_root = open_directory(quarantine["worktree_path"])
        quarantine_admin = None
        try:
            quarantine_admin = open_directory(quarantine["worktree_admin_path"])
            opened_worktree = directory_identity(quarantine_root, phase + " quarantine worktree")
            opened_admin = directory_identity(quarantine_admin, phase + " quarantine admin")
            if ((opened_worktree.st_dev, opened_worktree.st_ino) !=
                    (quarantine["worktree_dev"], quarantine["worktree_ino"]) or
                    (opened_worktree.st_dev, opened_worktree.st_ino) !=
                    (worktree.st_dev, worktree.st_ino)):
                block(f"{phase} quarantined worktree lstat/FD continuity drift")
            if ((opened_admin.st_dev, opened_admin.st_ino) !=
                    (quarantine["worktree_admin_dev"], quarantine["worktree_admin_ino"]) or
                    (opened_admin.st_dev, opened_admin.st_ino) !=
                    (admin.st_dev, admin.st_ino)):
                block(f"{phase} quarantined admin lstat/FD continuity drift")
            for path, digest in quarantine["observed_artifact_hashes"].items():
                raw, _ = read_regular(quarantine_root, path)
                if sha256_bytes(raw) != digest:
                    block(f"{phase} quarantine artifact drift: {path}")
            observed_manifest = ("openspec/changes/add-codex-skill-update/approvals/" +
                                 quarantine["observed_manifest_sha256"] + ".json")
            raw, _ = read_regular(quarantine_root, observed_manifest)
            if sha256_bytes(raw) != quarantine["observed_manifest_sha256"]:
                block(f"{phase} quarantine observed manifest drift")
            missing_manifest = ("openspec/changes/add-codex-skill-update/approvals/" +
                                quarantine["missing_required_manifest_sha256"] + ".json")
            for missing in [missing_manifest] + [
                "openspec/changes/add-codex-skill-update/approvals/artifacts/" + digest
                for digest in quarantine["missing_required_snapshot_sha256"]
            ]:
                parent, name = open_parent(quarantine_root, missing)
                try:
                    require_absent(parent, name, missing)
                finally:
                    os.close(parent)
        finally:
            if quarantine_admin is not None:
                os.close(quarantine_admin)
            os.close(quarantine_root)


def validate_prestate(repo_fd, git_fd, prestate_raw, expected_digest, phase):
    if not prestate_raw.endswith(b"\n") or prestate_raw.endswith(b"\n\n"):
        block("prestate evidence line ending mismatch")
    canonical = prestate_raw[:-1]
    if sha256_bytes(b"source-worktree-bootstrap-prestate-v2\0" + canonical) != expected_digest:
        block("prestate digest mismatch")
    try:
        value = json.loads(canonical)
    except Exception as error:
        block(f"prestate JSON invalid: {error}")
    expected_top_keys = {
        "base_commit", "base_tree", "git_executable", "local_config_sha256",
        "parent_closure", "quarantines", "ref_exclusions", "refs", "repository",
        "schema", "symbolic_head", "target_absence", "worktrees",
    }
    if (canonical_json(value) != canonical or value.get("schema") != 2 or
            set(value) != expected_top_keys):
        block("prestate is not canonical schema 2")
    if (set(value["repository"]) != {"git_common_dir", "git_common_dir_dev",
                                      "git_common_dir_ino", "object_format",
                                      "repository_root", "repository_root_dev",
                                      "repository_root_ino"} or
            set(value["git_executable"]) != {"path", "sha256", "version"} or
            set(value["target_absence"]) != {"branch_ref", "branch_reflog_path",
                                              "worktree_admin_path", "worktree_path"} or
            any(set(entry) != {"dev", "ino", "mode", "nlink", "path", "type", "uid"}
                for entry in value["parent_closure"]) or
            any(set(entry) != {"branch", "head", "path"} for entry in value["worktrees"]) or
            any(set(entry) != {"name", "object_oid", "object_type"} for entry in value["refs"])):
        block("prestate nested key set mismatch")
    exclusion = value.get("ref_exclusions")
    expected_exclusion = [{"policy": "OBSERVE_ALLOW_EXTERNAL_DRIFT_DENY_BOOTSTRAP_WRITE",
                           "prefix": "refs/codex/turn-diffs/"}]
    if exclusion != expected_exclusion:
        block("volatile ref exclusion mismatch")
    expected_absence = {
        "branch_ref": "ABSENT", "branch_reflog_path": "ABSENT",
        "worktree_admin_path": "ABSENT", "worktree_path": "ABSENT",
    }
    if value["target_absence"] != expected_absence:
        block("replacement target-absence evidence mismatch")
    expected_quarantine_keys = {
        "branch_ref", "head", "missing_required_manifest_sha256",
        "missing_required_snapshot_sha256", "mutation_policy",
        "observed_artifact_hashes", "observed_manifest_sha256", "status", "tree",
        "worktree_admin_dev", "worktree_admin_ino", "worktree_admin_path",
        "worktree_dev", "worktree_ino", "worktree_path",
    }
    if (len(value["quarantines"]) != 1 or
            set(value["quarantines"][0]) != expected_quarantine_keys):
        block("quarantine evidence key set mismatch")
    quarantine = value["quarantines"][0]
    if (quarantine["status"] != "BLOCKED_SOURCE_WORKTREE_RECOVERY" or
            quarantine["mutation_policy"] != "PRESERVE_NO_REUSE_REPAIR_DELETE" or
            quarantine["branch_ref"] != "refs/heads/add-codex-skill-update" or
            quarantine["worktree_path"] != TARGET_PARENT + "/add-codex-skill-update" or
            quarantine["worktree_admin_path"] != GIT_DIR + "/worktrees/add-codex-skill-update" or
            quarantine["head"] != BASE_COMMIT or quarantine["tree"] != BASE_TREE or
            set(quarantine["observed_artifact_hashes"]) != set(CONTRACT_PATHS) or
            quarantine["missing_required_snapshot_sha256"] !=
            sorted(quarantine["missing_required_snapshot_sha256"], key=lambda item: item.encode())):
        block("quarantine evidence semantic mismatch")
    root_stat = directory_identity(repo_fd, "repository root")
    git_stat = directory_identity(git_fd, "Git common directory")
    repository = value["repository"]
    if (repository["repository_root"], repository["repository_root_dev"],
            repository["repository_root_ino"]) != (ROOT, root_stat.st_dev, root_stat.st_ino):
        block("repository identity drift")
    if (repository["git_common_dir"], repository["git_common_dir_dev"],
            repository["git_common_dir_ino"]) != (GIT_DIR, git_stat.st_dev, git_stat.st_ino):
        block("Git common-directory identity drift")
    expected_git = {"path": GIT, "sha256": EXPECTED_EXECUTABLES[GIT], "version": "2.49.0"}
    if (repository["object_format"] != "sha1" or value["base_commit"] != BASE_COMMIT or
            value["base_tree"] != BASE_TREE or value["git_executable"] != expected_git):
        block("repository object format or base drift")
    if run_git(["symbolic-ref", "-q", "HEAD"]).decode().strip() != value["symbolic_head"]:
        block("symbolic HEAD drift")
    if observed_refs(exclusion[0]["prefix"]) != value["refs"]:
        block("non-excluded ref inventory drift")
    if parse_worktrees(run_git(["worktree", "list", "--porcelain"])) != value["worktrees"]:
        block("worktree inventory drift")
    config_raw, _ = read_regular(git_fd, "config")
    config_digest = sha256_bytes(b"source-worktree-local-config-v1\0" + config_raw)
    if config_digest != value["local_config_sha256"]:
        block("local config drift")
    lowered = config_raw.lower()
    for token in (b"include", b"hookspath", b"filter.", b"diff.", b"merge.", b"alias.",
                  b"credential.", b"fsmonitor", b"maintenance.", b"protocol.", b"submodule.",
                  b"worktreeconfig", b"core.worktree"):
        if token in lowered:
            block(f"executable-capable local config token: {token!r}")
    for entry in value["parent_closure"]:
        try:
            current = os.lstat(entry["path"])
        except OSError as error:
            block(f"parent closure unavailable {entry['path']}: {error}")
        observed = {"type": "directory", "dev": current.st_dev, "ino": current.st_ino,
                    "uid": current.st_uid, "mode": format(stat.S_IMODE(current.st_mode), "04o"),
                    "nlink": current.st_nlink}
        expected = {key: entry[key] for key in observed}
        expected["nlink"] = expected_parent_nlink(entry["path"], entry["nlink"], phase)
        if not stat.S_ISDIR(current.st_mode) or stat.S_ISLNK(current.st_mode) or observed != expected:
            block(f"parent closure drift: {entry['path']}")
    closure_paths = [entry["path"] for entry in value["parent_closure"]]
    required_closure = {
        ROOT, GIT_DIR, GIT_DIR + "/refs/heads", GIT_DIR + "/logs/refs/heads",
        GIT_DIR + "/worktrees", TARGET_PARENT, ROOT + "/openspec",
        ROOT + "/openspec/changes", ROOT + "/openspec/changes/add-codex-skill-update",
        APPROVAL_DIR, SOURCE_BOOTSTRAP_DIR,
    }
    if (closure_paths != sorted(closure_paths, key=lambda item: item.encode()) or
            not required_closure.issubset(closure_paths)):
        block("parent closure ordering or required coverage mismatch")
    if value["refs"] != sorted(value["refs"], key=lambda item: (
            item["name"].encode(), item["object_oid"].encode(), item["object_type"].encode())):
        block("ref evidence ordering mismatch")
    if value["worktrees"] != sorted(value["worktrees"], key=lambda item: item["path"].encode()):
        block("worktree evidence ordering mismatch")
    for directory, name, label in (
            (GIT_DIR + "/refs/heads", BRANCH, BRANCH_REF),
            (GIT_DIR + "/logs/refs/heads", BRANCH, "branch reflog"),
            (GIT_DIR + "/worktrees", BRANCH, ADMIN_PATH)):
        parent = open_directory(directory)
        try:
            require_absent(parent, name, label)
        finally:
            os.close(parent)
    if os.path.lexists(TARGET_PATH):
        block("replacement worktree target is present")
    validate_quarantines(value, "pre-bootstrap")
    return value


def select_manifest(repo_fd, approval_fd, artifact_bytes, projection, prestate_digest):
    candidates = []
    for name in os.listdir(approval_fd):
        if len(name) != 69 or not name.endswith(".json") or any(c not in "0123456789abcdef" for c in name[:-5]):
            continue
        try:
            raw, _ = read_regular(approval_fd, name)
            manifest = json.loads(raw)
        except Exception:
            continue
        digest = sha256_bytes(raw)
        if digest != name[:-5] or canonical_json(manifest) != raw:
            continue
        current_hashes = {path: sha256_bytes(data) for path, data in artifact_bytes.items()}
        if (manifest.get("schema") == 1 and manifest.get("change_id") == "add-codex-skill-update" and
                manifest.get("artifact_hashes") == current_hashes and
                manifest.get("contract_projection_sha256") == projection and
                manifest.get("source_bootstrap_prestate_sha256") == prestate_digest and
                manifest.get("source_bootstrap_git", {}).get("branch_ref") == BRANCH_REF and
                manifest.get("source_bootstrap_git", {}).get("worktree_path") == TARGET_PATH and
                manifest.get("source_bootstrap_git", {}).get("worktree_admin_path") == ADMIN_PATH):
            candidates.append((digest, manifest))
    if len(candidates) != 1:
        block(f"expected exactly one current authorization manifest, observed {len(candidates)}")
    return candidates[0]


def validate_manifest(repo_fd, manifest_sha, manifest, artifact_bytes, prestate_raw):
    expected_manifest_keys = {
        "artifact_hashes", "change_id", "contract_projection_sha256",
        "control_plane_instance", "decision_provenance", "decision_timestamp", "schema",
        "source_bootstrap_git", "source_bootstrap_helper", "source_bootstrap_material_hashes",
        "source_bootstrap_prestate_sha256", "source_bootstrap_sandbox",
    }
    if set(manifest) != expected_manifest_keys:
        block("authorization manifest key set mismatch")
    timestamp = manifest.get("decision_timestamp")
    if (manifest.get("schema") != 1 or manifest.get("change_id") != "add-codex-skill-update" or
            manifest.get("decision_provenance") != "direct-user-confirmation" or
            manifest.get("control_plane_instance") != EXPECTED_CONTROL_PLANE_INSTANCE or
            not isinstance(timestamp, str) or len(timestamp) != 20 or
            timestamp[4:5] != "-" or timestamp[7:8] != "-" or timestamp[10:11] != "T" or
            timestamp[13:14] != ":" or timestamp[16:17] != ":" or timestamp[19:] != "Z" or
            not (timestamp[:4] + timestamp[5:7] + timestamp[8:10] + timestamp[11:13] +
                 timestamp[14:16] + timestamp[17:19]).isdigit()):
        block("authorization manifest decision metadata mismatch")
    try:
        datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        block("authorization manifest decision timestamp is invalid")
    helper = manifest["source_bootstrap_helper"]
    expected_argv = ["-I", "-S", HELPER_ABS, "--launch"]
    if (set(helper) != {"executable_path", "executable_sha256", "fixed_argv",
                        "fixed_environment", "fd_binding_protocol"} or
            helper.get("executable_path") != PYTHON or
            helper.get("executable_sha256") != EXPECTED_EXECUTABLES[PYTHON] or
            helper.get("fixed_argv") != expected_argv or
            helper.get("fixed_environment") != EXPECTED_FIXED_ENVIRONMENT or
            helper.get("fd_binding_protocol") != EXPECTED_FD_PROTOCOL):
        block("helper identity/argv/environment/fd protocol mismatch")
    git = manifest["source_bootstrap_git"]
    expected_git = {"executable_path": GIT, "executable_sha256": EXPECTED_EXECUTABLES[GIT],
                    "version": "2.49.0", "repository_root": ROOT, "git_common_dir": GIT_DIR,
                    "object_format": "sha1", "base_commit": BASE_COMMIT, "base_tree": BASE_TREE,
                    "branch_ref": BRANCH_REF, "worktree_path": TARGET_PATH,
                    "worktree_admin_path": ADMIN_PATH}
    if git != expected_git:
        block("source-bootstrap Git binding mismatch")
    sandbox = manifest["source_bootstrap_sandbox"]
    if (set(sandbox) != {"child_exec_policy", "executable_path", "executable_sha256",
                         "invocation_argv_sha256", "network_policy", "profile_sha256",
                         "write_allowlist_sha256"} or
            sandbox.get("executable_path") != SANDBOX or
            sandbox.get("executable_sha256") != EXPECTED_EXECUTABLES[SANDBOX] or
            sandbox.get("invocation_argv_sha256") != sandbox_exec_vector_sha256() or
            sandbox.get("network_policy") != "DENY" or
            sandbox.get("child_exec_policy") != "HELPER_AND_FIXED_READ_ONLY_GIT_ONLY"):
        block("sandbox binding mismatch")
    profile_hash = sandbox.get("profile_sha256")
    profile_rel = PROFILE_PREFIX + profile_hash + ".sb"
    profile_raw, _ = read_regular(repo_fd, profile_rel)
    if (sha256_bytes(profile_raw) != profile_hash or profile_raw != EXPECTED_PROFILE or
            b"refs/codex/turn-diffs" in profile_raw):
        block("sandbox profile hash or volatile-ref write policy mismatch")
    paths = [
        {"access": "read-write-device", "path": "/dev/null"},
        {"access": "create-or-write", "path": APPROVAL_DIR + "/" + LOCK_NAME},
        {"access": "create-or-write", "path": SOURCE_BOOTSTRAP_DIR + "/" + JOURNAL_NAME},
        {"access": "create-or-write", "path": GIT_DIR + "/refs/heads/" + BRANCH},
        {"access": "create-or-write", "path": GIT_DIR + "/refs/heads/" + BRANCH + ".lock"},
        {"access": "create-or-write", "path": GIT_DIR + "/logs/refs/heads/" + BRANCH},
        {"access": "create-or-write", "path": GIT_DIR + "/logs/refs/heads/" + BRANCH + ".lock"},
        {"access": "create-or-write", "path": ADMIN_PATH},
        {"access": "create-or-write", "path": TARGET_PATH},
    ]
    paths.sort(key=lambda item: item["path"].encode())
    allow_digest = sha256_bytes(b"source-worktree-write-allowlist-v1\0" +
                                canonical_json({"paths": paths, "schema": 1}))
    if sandbox.get("write_allowlist_sha256") != allow_digest:
        block("write allowlist digest mismatch")
    material = manifest["source_bootstrap_material_hashes"]
    if not isinstance(material, dict) or HELPER_REL not in material or PRESTATE_REL not in material:
        block("helper or prestate evidence absent from approved material map")
    forbidden_prefix = APPROVAL_REL + "/"
    for path, digest in material.items():
        if path.startswith(forbidden_prefix) or path in artifact_bytes:
            block(f"prior approval or contract artifact illegally placed in material map: {path}")
        raw, _ = read_regular(repo_fd, path)
        if sha256_bytes(raw) != digest:
            block(f"approved material hash mismatch: {path}")
    if sha256_bytes(prestate_raw) != material[PRESTATE_REL]:
        block("prestate evidence file hash mismatch")
    for path, digest in manifest["artifact_hashes"].items():
        snapshot = APPROVAL_REL + "/artifacts/" + digest
        raw, _ = read_regular(repo_fd, snapshot)
        if sha256_bytes(raw) != digest or raw != artifact_bytes[path]:
            block(f"current artifact snapshot mismatch: {path}")
    return profile_rel, material


def preload_base():
    resolved_tree = run_git(["rev-parse", BASE_COMMIT + "^{tree}"]).decode().strip()
    if resolved_tree != BASE_TREE:
        block("base tree drift")
    raw = run_git(["ls-tree", "-rz", "-r", "--full-tree", BASE_COMMIT])
    entries = []
    total = 0
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, path_bytes = record.split(b"\t", 1)
        mode_raw, object_type, oid_raw = metadata.split(b" ")
        if mode_raw not in (b"100644", b"100755") or object_type != b"blob":
            block(f"non-regular base entry: {record!r}")
        path = path_bytes.decode("utf-8")
        safe_parts(path)
        data = run_git(["cat-file", "blob", oid_raw.decode("ascii")])
        expected_oid = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        if expected_oid != oid_raw.decode("ascii"):
            block(f"base blob OID/content mismatch: {path}")
        total += len(data)
        if total > 64 * 1024 * 1024:
            block("base material exceeds bounded preload")
        entries.append({"path": path, "mode": int(mode_raw, 8),
                        "oid": bytes.fromhex(oid_raw.decode("ascii")), "data": data})
    entries.sort(key=lambda item: item["path"].encode())
    return entries


def make_index(target_fd, entries):
    encoded = []
    for entry in entries:
        parent, name = open_parent(target_fd, entry["path"])
        try:
            value = os.stat(name, dir_fd=parent, follow_symlinks=False)
        finally:
            os.close(parent)
        if not stat.S_ISREG(value.st_mode):
            block(f"tracked target entry is not regular: {entry['path']}")
        path = entry["path"].encode("utf-8")
        ctime_ns = value.st_ctime_ns
        mtime_ns = value.st_mtime_ns
        fixed = struct.pack(
            ">LLLLLLLLLL20sH",
            (ctime_ns // 1_000_000_000) & 0xFFFFFFFF,
            (ctime_ns % 1_000_000_000) & 0xFFFFFFFF,
            (mtime_ns // 1_000_000_000) & 0xFFFFFFFF,
            (mtime_ns % 1_000_000_000) & 0xFFFFFFFF,
            value.st_dev & 0xFFFFFFFF,
            value.st_ino & 0xFFFFFFFF,
            entry["mode"],
            value.st_uid & 0xFFFFFFFF,
            value.st_gid & 0xFFFFFFFF,
            value.st_size & 0xFFFFFFFF,
            entry["oid"],
            min(len(path), 0xFFF),
        )
        body = fixed + path + b"\0"
        body += b"\0" * ((8 - (len(body) % 8)) % 8)
        encoded.append(body)
    content = b"DIRC" + struct.pack(">LL", 2, len(encoded)) + b"".join(encoded)
    return content + hashlib.sha1(content).digest()


def append_journal(kind, **fields):
    global JOURNAL_FD
    if JOURNAL_FD is None:
        return
    record = {"kind": kind, "manifest_sha256": MANIFEST_SHA256, "schema": 1, **fields}
    payload = canonical_json(record) + b"\n"
    view = memoryview(payload)
    while view:
        written = os.write(JOURNAL_FD, view)
        if written <= 0:
            block("short source-bootstrap journal write")
        view = view[written:]
    os.fsync(JOURNAL_FD)


def assert_sandbox_containment():
    try:
        sandbox_library = ctypes.CDLL("/usr/lib/libsandbox.1.dylib")
        sandbox_check = sandbox_library.sandbox_check
        sandbox_check.restype = ctypes.c_int
        pid = os.getpid()
        if sandbox_check(pid, b"network-outbound", 0) != 1:
            block("active sandbox does not deny outbound network")
        if sandbox_check(pid, b"process-exec", 1, b"/bin/sh") != 1:
            block("active sandbox does not deny unauthorized child execution")
    except Blocked:
        raise
    except Exception as error:
        block(f"cannot attest active sandbox: {error}")
    for path in (ROOT + "/SKILL.md", GIT_DIR + "/config"):
        try:
            fd = os.open(path, os.O_WRONLY | os.O_NOFOLLOW)
        except PermissionError:
            continue
        except OSError as error:
            block(f"cannot prove sandbox write denial for {path}: {error}")
        else:
            os.close(fd)
            block(f"active sandbox permits forbidden write-open: {path}")


def load_launch_authorization():
    repo_fd = open_directory(ROOT)
    approval_fd = open_directory(APPROVAL_DIR)
    try:
        artifact_bytes = {path: read_regular(repo_fd, path)[0] for path in CONTRACT_PATHS}
        projection = contract_projection(artifact_bytes)
        prestate_raw, _ = read_regular(repo_fd, PRESTATE_REL)
        if not prestate_raw.endswith(b"\n"):
            block("prestate evidence lacks final LF")
        prestate_digest = sha256_bytes(b"source-worktree-bootstrap-prestate-v2\0" +
                                      prestate_raw[:-1])
        manifest_sha, manifest = select_manifest(repo_fd, approval_fd, artifact_bytes,
                                                 projection, prestate_digest)
        validate_manifest(repo_fd, manifest_sha, manifest, artifact_bytes, prestate_raw)
    finally:
        os.close(approval_fd)
        os.close(repo_fd)


def launch_contained_executor():
    if dict(os.environ) != EXPECTED_FIXED_ENVIRONMENT:
        block("source-bootstrap fixed environment mismatch")
    if sys.argv != [HELPER_ABS, "--launch"]:
        block("source-bootstrap launcher argv mismatch")
    for path, digest in EXPECTED_EXECUTABLES.items():
        if sha256_regular_path(path) != digest:
            block(f"executable identity drift: {path}")
    load_launch_authorization()
    os.execve(SANDBOX, SANDBOX_EXEC_VECTOR, EXPECTED_FIXED_ENVIRONMENT)


def main():
    global JOURNAL_FD, MANIFEST_SHA256
    if dict(os.environ) != EXPECTED_FIXED_ENVIRONMENT:
        block("source-bootstrap fixed environment mismatch")
    if sys.argv != [HELPER_ABS, "--contained"]:
        block("source-bootstrap contained argv mismatch")
    assert_sandbox_containment()
    os.umask(0o077)
    for path, digest in EXPECTED_EXECUTABLES.items():
        if sha256_regular_path(path) != digest:
            block(f"executable identity drift: {path}")

    repo_fd = open_directory(ROOT)
    git_fd = open_relative_directory(repo_fd, ".git")
    refs_fd = open_relative_directory(git_fd, "refs/heads")
    logs_fd = open_relative_directory(git_fd, "logs/refs/heads")
    worktrees_fd = open_relative_directory(git_fd, "worktrees")
    target_parent_fd = open_directory(TARGET_PARENT)
    approval_fd = open_relative_directory(
        repo_fd, "openspec/changes/add-codex-skill-update/approvals")
    source_bootstrap_fd = open_relative_directory(approval_fd, "source-bootstrap")
    artifact_bytes = {path: read_regular(repo_fd, path)[0] for path in CONTRACT_PATHS}
    projection = contract_projection(artifact_bytes)
    prestate_raw, _ = read_regular(repo_fd, PRESTATE_REL)
    if not prestate_raw.endswith(b"\n"):
        block("prestate evidence lacks final LF")
    prestate_digest = sha256_bytes(b"source-worktree-bootstrap-prestate-v2\0" + prestate_raw[:-1])
    manifest_sha, manifest = select_manifest(repo_fd, approval_fd, artifact_bytes,
                                             projection, prestate_digest)
    MANIFEST_SHA256 = manifest_sha
    profile_rel, material = validate_manifest(repo_fd, manifest_sha, manifest,
                                              artifact_bytes, prestate_raw)
    prestate = validate_prestate(repo_fd, git_fd, prestate_raw, prestate_digest,
                                 "approval-recorded")
    base_entries = preload_base()

    require_absent(refs_fd, BRANCH, BRANCH_REF)
    require_absent(logs_fd, BRANCH, "branch reflog")
    require_absent(worktrees_fd, BRANCH, ADMIN_PATH)
    require_absent(target_parent_fd, BRANCH, TARGET_PATH)
    require_absent(source_bootstrap_fd, JOURNAL_NAME, "source-bootstrap recovery journal")

    # Exact retained/lexical binding check before the first potentially creating open.
    validate_prestate(repo_fd, git_fd, prestate_raw, prestate_digest, "approval-recorded")
    verify_retained_bindings(prestate, repo_fd, git_fd, refs_fd, logs_fd, worktrees_fd,
                             target_parent_fd, approval_fd, source_bootstrap_fd,
                             "approval-recorded")

    try:
        lock_fd = os.open(LOCK_NAME, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600,
                          dir_fd=approval_fd)
    except OSError as error:
        block(f"cannot open source-bootstrap lock: {error}")
    lock_stat = os.fstat(lock_fd)
    if (not stat.S_ISREG(lock_stat.st_mode) or lock_stat.st_uid != os.getuid() or
            stat.S_IMODE(lock_stat.st_mode) != 0o600 or lock_stat.st_nlink != 1):
        block("unsafe source-bootstrap lock")
    os.fsync(lock_fd)
    os.fsync(approval_fd)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as error:
        block(f"source-bootstrap lock unavailable: {error}")
    try:
        JOURNAL_FD = os.open(JOURNAL_NAME, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                             0o600, dir_fd=source_bootstrap_fd)
    except OSError as error:
        block(f"cannot create recovery journal: {error}")
    os.fsync(source_bootstrap_fd)
    append_journal("PREPARED", prestate_sha256=prestate_digest,
                   contract_projection_sha256=projection)

    # Last identity/absence check before the first replacement-state write.
    validate_prestate(repo_fd, git_fd, prestate_raw, prestate_digest, "journal-ready")
    verify_retained_bindings(prestate, repo_fd, git_fd, refs_fd, logs_fd, worktrees_fd,
                             target_parent_fd, approval_fd, source_bootstrap_fd,
                             "journal-ready")

    try:
        os.mkdir(BRANCH, 0o700, dir_fd=target_parent_fd)
    except OSError as error:
        block(f"cannot reserve target: {error}")
    target_fd = os.open(BRANCH, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                        dir_fd=target_parent_fd)
    target_stat = directory_identity(target_fd, "reserved target")
    if target_stat.st_uid != os.getuid() or stat.S_IMODE(target_stat.st_mode) != 0o700 or os.listdir(target_fd):
        block("reserved target ownership/mode/emptiness mismatch")
    append_journal("TARGET_RESERVED", target_dev=target_stat.st_dev, target_ino=target_stat.st_ino)

    try:
        os.mkdir(BRANCH, 0o700, dir_fd=worktrees_fd)
    except OSError as error:
        block(f"cannot reserve worktree admin child: {error}")
    admin_fd = os.open(BRANCH, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=worktrees_fd)
    write_new(admin_fd, "commondir", b"../..\n", 0o600)
    write_new(admin_fd, "gitdir", (TARGET_PATH + "/.git\n").encode(), 0o600)
    write_new(admin_fd, "HEAD", ("ref: " + BRANCH_REF + "\n").encode(), 0o600)
    write_new(admin_fd, "ORIG_HEAD", (BASE_COMMIT + "\n").encode(), 0o600)
    os.mkdir("logs", 0o700, dir_fd=admin_fd)
    admin_logs_fd = os.open("logs", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=admin_fd)
    write_new(admin_logs_fd, "HEAD",
              f"{ZERO_OID} {BASE_COMMIT} {REFLOG_IDENTITY}\n".encode(), 0o600)
    os.fsync(admin_logs_fd)
    os.close(admin_logs_fd)
    write_new(target_fd, ".git", ("gitdir: " + ADMIN_PATH + "\n").encode(), 0o600)

    for entry in base_entries:
        write_new(target_fd, entry["path"], entry["data"],
                  0o755 if entry["mode"] == 0o100755 else 0o644)

    extra = {}
    extra.update(artifact_bytes)
    for path in material:
        extra[path] = read_regular(repo_fd, path)[0]
    for path, digest in manifest["artifact_hashes"].items():
        snapshot = APPROVAL_REL + "/artifacts/" + digest
        extra[snapshot] = read_regular(repo_fd, snapshot)[0]
    manifest_rel = APPROVAL_REL + "/" + manifest_sha + ".json"
    extra[manifest_rel] = read_regular(repo_fd, manifest_rel)[0]
    extra[profile_rel] = read_regular(repo_fd, profile_rel)[0]
    base_paths = {entry["path"] for entry in base_entries}
    if base_paths.intersection(extra):
        block("approved untracked material collides with base tree")
    for path, data in sorted(extra.items(), key=lambda item: item[0].encode()):
        write_new(target_fd, path, data, 0o644)

    index_raw = make_index(target_fd, base_entries)
    write_new(admin_fd, "index", index_raw, 0o600)
    index_digest = sha256_bytes(index_raw)
    os.fsync(admin_fd)
    os.fsync(worktrees_fd)
    os.fsync(target_fd)
    os.fsync(target_parent_fd)
    append_journal("MATERIALIZED", index_sha256=index_digest,
                   untracked_file_count=len(extra))

    branch_log = (f"{ZERO_OID} {BASE_COMMIT} {REFLOG_IDENTITY}"
                  f"\tbranch: Created from {BASE_COMMIT}\n").encode()
    write_new(logs_fd, BRANCH + ".lock", branch_log, 0o600)
    promote_no_replace(logs_fd, BRANCH + ".lock", BRANCH, "branch reflog")
    write_new(refs_fd, BRANCH + ".lock", (BASE_COMMIT + "\n").encode(), 0o600)
    promote_no_replace(refs_fd, BRANCH + ".lock", BRANCH, "branch ref")
    append_journal("REGISTERED")

    expected_refs = list(prestate["refs"]) + [
        {"name": BRANCH_REF, "object_oid": BASE_COMMIT, "object_type": "commit"}
    ]
    expected_refs.sort(key=lambda item: (item["name"].encode(), item["object_oid"].encode(),
                                         item["object_type"].encode()))
    if observed_refs(prestate["ref_exclusions"][0]["prefix"]) != expected_refs:
        block("post-bootstrap ref delta mismatch")
    expected_worktrees = list(prestate["worktrees"]) + [
        {"path": TARGET_PATH, "head": BASE_COMMIT, "branch": BRANCH_REF}
    ]
    expected_worktrees.sort(key=lambda item: item["path"].encode())
    if parse_worktrees(run_git(["worktree", "list", "--porcelain"])) != expected_worktrees:
        block("post-bootstrap worktree delta mismatch")
    if run_git(["-C", TARGET_PATH, "rev-parse", "HEAD^{tree}"]).decode().strip() != BASE_TREE:
        block("replacement worktree base tree mismatch")
    index_after_read, index_mode = read_regular(admin_fd, "index")
    status = run_git(["--no-optional-locks", "-C", TARGET_PATH, "status", "--porcelain=v1",
                      "--untracked-files=all"]).decode("utf-8")
    index_after_status, index_mode_after = read_regular(admin_fd, "index")
    if (index_after_read != index_after_status or sha256_bytes(index_after_status) != index_digest or
            index_mode != 0o600 or index_mode_after != 0o600):
        block("read-only status changed the index")
    observed_untracked = set()
    for line in status.splitlines():
        if not line.startswith("?? "):
            block(f"tracked status is not clean: {line}")
        observed_untracked.add(line[3:])
    if observed_untracked != set(extra):
        block("untracked status closure mismatch")
    expected_target_files = base_paths | set(extra) | {".git"}
    target_files, target_directories = inventory_regular_files(target_fd)
    expected_target_directories = {
        "/".join(path.split("/")[:index])
        for path in expected_target_files
        for index in range(1, len(path.split("/")))
    }
    if (set(target_files) != expected_target_files or
            target_directories != {path: 0o755 for path in expected_target_directories}):
        block("target filesystem closure mismatch")
    for entry in base_entries:
        actual, actual_mode = read_regular(target_fd, entry["path"])
        expected_mode = 0o755 if entry["mode"] == 0o100755 else 0o644
        if actual != entry["data"] or actual_mode != expected_mode:
            block(f"tracked base material drift: {entry['path']}")
    for path, expected in extra.items():
        actual, actual_mode = read_regular(target_fd, path)
        if actual != expected or actual_mode != 0o644:
            block(f"target material drift: {path}")
    final_target = os.stat(BRANCH, dir_fd=target_parent_fd, follow_symlinks=False)
    if ((final_target.st_dev, final_target.st_ino) != (target_stat.st_dev, target_stat.st_ino) or
            final_target.st_uid != os.getuid() or stat.S_IMODE(final_target.st_mode) != 0o700):
        block("reserved target identity/ownership/mode changed")
    final_admin = os.stat(BRANCH, dir_fd=worktrees_fd, follow_symlinks=False)
    admin_stat = directory_identity(admin_fd, "worktree admin")
    if ((final_admin.st_dev, final_admin.st_ino) != (admin_stat.st_dev, admin_stat.st_ino) or
            admin_stat.st_uid != os.getuid() or stat.S_IMODE(admin_stat.st_mode) != 0o700):
        block("worktree admin identity/ownership/mode drift")
    expected_admin_files = {
        "commondir": b"../..\n",
        "gitdir": (TARGET_PATH + "/.git\n").encode(),
        "HEAD": ("ref: " + BRANCH_REF + "\n").encode(),
        "ORIG_HEAD": (BASE_COMMIT + "\n").encode(),
        "logs/HEAD": f"{ZERO_OID} {BASE_COMMIT} {REFLOG_IDENTITY}\n".encode(),
    }
    for path, expected in expected_admin_files.items():
        actual, actual_mode = read_regular(admin_fd, path)
        if actual != expected or actual_mode != 0o600:
            block(f"worktree admin file drift: {path}")
    admin_files, admin_directories = inventory_regular_files(admin_fd)
    if (set(admin_files) != set(expected_admin_files) | {"index"} or
            admin_directories != {"logs": 0o700}):
        block("worktree admin filesystem closure mismatch")
    target_git, target_git_mode = read_regular(target_fd, ".git")
    if target_git != ("gitdir: " + ADMIN_PATH + "\n").encode() or target_git_mode != 0o600:
        block("target .git link-file drift")
    branch_ref_raw, branch_ref_mode = read_regular(refs_fd, BRANCH)
    branch_log_raw, branch_log_mode = read_regular(logs_fd, BRANCH)
    if (branch_ref_raw != (BASE_COMMIT + "\n").encode() or branch_log_raw != branch_log or
            branch_ref_mode != 0o600 or branch_log_mode != 0o600):
        block("branch ref/reflog bytes drift")
    verify_retained_bindings(prestate, repo_fd, git_fd, refs_fd, logs_fd, worktrees_fd,
                             target_parent_fd, approval_fd, source_bootstrap_fd,
                             "post-bootstrap")
    validate_prestate_post_only(prestate)
    append_journal("PASS", index_sha256=index_digest,
                   ref=BRANCH_REF, worktree_path=TARGET_PATH)
    print("SOURCE_WORKTREE_BOOTSTRAP_PASS")


def validate_prestate_post_only(prestate):
    for entry in prestate["parent_closure"]:
        try:
            current = os.lstat(entry["path"])
        except OSError as error:
            block(f"post-bootstrap parent closure unavailable {entry['path']}: {error}")
        expected_nlink = expected_parent_nlink(
            entry["path"], entry["nlink"], "post-bootstrap")
        if (not stat.S_ISDIR(current.st_mode) or stat.S_ISLNK(current.st_mode) or
                current.st_dev != entry["dev"] or current.st_ino != entry["ino"] or
                current.st_uid != entry["uid"] or
                format(stat.S_IMODE(current.st_mode), "04o") != entry["mode"] or
                current.st_nlink != expected_nlink):
            block(f"post-bootstrap parent closure drift: {entry['path']}")
    config_fd = open_directory(GIT_DIR)
    try:
        config_raw, _ = read_regular(config_fd, "config")
    finally:
        os.close(config_fd)
    if sha256_bytes(b"source-worktree-local-config-v1\0" + config_raw) != prestate["local_config_sha256"]:
        block("post-bootstrap local config drift")
    if run_git(["symbolic-ref", "-q", "HEAD"]).decode().strip() != prestate["symbolic_head"]:
        block("post-bootstrap symbolic HEAD drift")
    validate_quarantines(prestate, "post-bootstrap")


def entrypoint():
    try:
        if sys.argv == [HELPER_ABS, "--launch"]:
            launch_contained_executor()
        elif sys.argv == [HELPER_ABS, "--contained"]:
            main()
        else:
            block("source-bootstrap entrypoint argv mismatch")
    except Blocked as error:
        try:
            append_journal("BLOCKED", reason=str(error))
        except Exception:
            pass
        print(f"BLOCKED_SOURCE_WORKTREE_RECOVERY: {error}", file=sys.stderr)
        raise SystemExit(70)
    except Exception as error:
        try:
            append_journal("BLOCKED", reason=f"unexpected {type(error).__name__}: {error}")
        except Exception:
            pass
        print(f"BLOCKED_SOURCE_WORKTREE_RECOVERY: unexpected {type(error).__name__}", file=sys.stderr)
        raise SystemExit(70)


if __name__ == "__main__":
    entrypoint()
