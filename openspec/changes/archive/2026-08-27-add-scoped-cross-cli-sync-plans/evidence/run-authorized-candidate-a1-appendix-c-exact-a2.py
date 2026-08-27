from __future__ import annotations
import hashlib, json, os, re, stat, sys
from pathlib import Path

AUTH_KEYS = {
    "schema_version", "purpose", "root", "implementation_plan_path",
    "implementation_plan_sha256", "sync_plan_path", "sync_plan_sha256",
    "plan_review_path", "plan_review_sha256", "source_review_path",
    "source_review_sha256", "candidate_root", "candidate_bundle_path",
    "candidate_bundle_sha256", "candidate_script_path",
    "candidate_script_sha256", "candidate_inventory_sha256", "guard_path",
    "guard_sha256", "interpreter_path", "interpreter_sha256",
    "operation_set", "target_order", "managed_rule_selected",
}
BUNDLE_KEYS = {
    "schema_version", "candidate_root", "files", "changed_paths",
    "script_sha256", "evidence",
}
EXPECTED_CHANGED = {
    "scripts/validate_cross_cli_sync.py",
    "tests/test_cross_cli_sync.py",
    "references/cross-cli-sync.md",
    "references/sync-checklist.md",
}
ALLOWED_COMMANDS = {
    "verify-prestate", "apply", "verify", "verify-discovery", "commit-target",
    "restore-target", "recover-pending", "verify-all",
}
def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
def regular(path: Path, mode: int | None = None) -> Path:
    metadata = path.stat(follow_symlinks=False)
    if path.is_symlink() or not stat.S_ISREG(metadata.st_mode):
        raise SystemExit("BLOCKED: non-regular trusted artifact")
    if mode is not None and stat.S_IMODE(metadata.st_mode) != mode:
        raise SystemExit("BLOCKED: trusted artifact mode drift")
    return path
def check_ref(path_text: str, expected: str, mode: int | None = None) -> Path:
    path = regular(Path(path_text), mode)
    if sha(path) != expected:
        raise SystemExit("BLOCKED: trusted artifact SHA drift")
    return path
CANONICAL_ROOT = Path(
    "/Users/elvis/file/develop/opensource/openspec-superpower-change"
).resolve(strict=True)
CANONICAL_TASKS = (
    CANONICAL_ROOT
    / "openspec/changes/add-scoped-cross-cli-sync-plans/tasks.md"
)
CANONICAL_EVIDENCE = (
    CANONICAL_ROOT
    / "openspec/changes/add-scoped-cross-cli-sync-plans/evidence"
)
if len(sys.argv) < 3 or sys.argv[1] != "--":
    raise SystemExit("BLOCKED: invalid guard invocation")
self_path = Path(__file__).resolve(strict=True)
match = re.fullmatch(r"run-authorized-candidate-a([1-9][0-9]*)\.py", self_path.name)
if self_path.parent != CANONICAL_EVIDENCE or match is None:
    raise SystemExit("BLOCKED: noncanonical guard path")
attempt = match.group(1)
auth_path = CANONICAL_EVIDENCE / f"batch-a-launch-authorization-a{attempt}.json"
tasks_path = regular(CANONICAL_TASKS)
tasks_text = tasks_path.read_text(encoding="utf-8")
anchors = re.findall(
    rf"^Batch-A launch authorization a{attempt} SHA-256: ([0-9a-f]{{64}})$",
    tasks_text,
    re.M,
)
if len(anchors) != 1 or sha(regular(auth_path, 0o600)) != anchors[0]:
    raise SystemExit("BLOCKED: canonical launch anchor mismatch")
auth = json.loads(auth_path.read_text(encoding="utf-8"))
if set(auth) != AUTH_KEYS or auth["schema_version"] != 1:
    raise SystemExit("BLOCKED: launch authorization shape")
if auth["purpose"] != "execute reviewed Batch-A scoped sync":
    raise SystemExit("BLOCKED: launch authorization purpose")
if Path(auth["root"]).resolve(strict=True) != CANONICAL_ROOT:
    raise SystemExit("BLOCKED: canonical root substitution")
check_ref(auth["guard_path"], auth["guard_sha256"], 0o600)
if Path(auth["guard_path"]).resolve(strict=True) != Path(__file__).resolve(strict=True):
    raise SystemExit("BLOCKED: guard substitution")
interpreter = check_ref(auth["interpreter_path"], auth["interpreter_sha256"])
if Path(sys.executable).resolve(strict=True) != interpreter.resolve(strict=True):
    raise SystemExit("BLOCKED: interpreter substitution")
check_ref(auth["implementation_plan_path"], auth["implementation_plan_sha256"])
sync_plan_path = check_ref(auth["sync_plan_path"], auth["sync_plan_sha256"], 0o600)
check_ref(auth["source_review_path"], auth["source_review_sha256"])
check_ref(auth["plan_review_path"], auth["plan_review_sha256"])
bundle_path = check_ref(auth["candidate_bundle_path"], auth["candidate_bundle_sha256"], 0o600)
bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
if set(bundle) != BUNDLE_KEYS or bundle["schema_version"] != 1:
    raise SystemExit("BLOCKED: candidate bundle shape")
root = Path(auth["candidate_root"])
if root != Path(bundle["candidate_root"]) or root.is_symlink() or not root.is_dir():
    raise SystemExit("BLOCKED: candidate root")
if set(bundle["changed_paths"]) != EXPECTED_CHANGED:
    raise SystemExit("BLOCKED: candidate delta")
actual = {}
for path in root.rglob("*"):
    rel = path.relative_to(root).as_posix()
    if path.is_symlink():
        raise SystemExit("BLOCKED: candidate symlink")
    if path.is_file():
        if "__pycache__" in path.parts or path.suffix == ".pyc" or ".pytest_cache" in path.parts:
            raise SystemExit("BLOCKED: candidate cache")
        actual[rel] = {
            "sha256": sha(path),
            "mode": format(stat.S_IMODE(path.stat(follow_symlinks=False).st_mode), "04o"),
        }
if actual != bundle["files"]:
    raise SystemExit("BLOCKED: candidate inventory drift")
canonical_inventory = json.dumps(actual, sort_keys=True, separators=(",", ":")).encode()
if hashlib.sha256(canonical_inventory).hexdigest() != auth["candidate_inventory_sha256"]:
    raise SystemExit("BLOCKED: candidate inventory binding")
script = check_ref(auth["candidate_script_path"], auth["candidate_script_sha256"])
if script != root / "scripts/validate_cross_cli_sync.py" or bundle["script_sha256"] != auth["candidate_script_sha256"]:
    raise SystemExit("BLOCKED: candidate script binding")
for path_text, expected in bundle["evidence"].items():
    check_ref(path_text, expected, 0o600)
plan = json.loads(sync_plan_path.read_text(encoding="utf-8"))
if plan.get("schema_version") != 2 or auth["managed_rule_selected"] is not False:
    raise SystemExit("BLOCKED: scoped plan/rule binding")
if auth["target_order"] != ["codex", "pi", "antigravity-cli", "grok-cli"]:
    raise SystemExit("BLOCKED: target order")
expected_ops = [list(item) for item in auth["operation_set"]]
for target_id in auth["target_order"]:
    observed = [[item["skill"], item["path"]] for item in plan["targets"][target_id]["files"]]
    if observed != expected_ops or plan["targets"][target_id]["managed_rule"]["selected"] is not False:
        raise SystemExit("BLOCKED: operation-set drift")
args = sys.argv[2:]
if not args or args[0] not in ALLOWED_COMMANDS:
    raise SystemExit("BLOCKED: candidate command not authorized")
if any(item.startswith("--plan=") for item in args):
    raise SystemExit("BLOCKED: joined plan argument is forbidden")
plan_indices = [index for index, item in enumerate(args) if item == "--plan"]
if len(plan_indices) != 1 or plan_indices[0] + 1 >= len(args):
    raise SystemExit("BLOCKED: candidate command requires one plan")
plan_index = plan_indices[0]
try:
    supplied_plan = Path(args[plan_index + 1]).resolve(strict=True)
except OSError as exc:
    raise SystemExit("BLOCKED: candidate plan path") from exc
if supplied_plan != sync_plan_path.resolve(strict=True):
    raise SystemExit("BLOCKED: alternate candidate plan")
forward_args = list(args)
forward_args[plan_index + 1] = str(sync_plan_path.resolve(strict=True))
environment = {
    "HOME": str(auth_path.parent),
    "PATH": "/usr/bin:/bin",
    "PYTHONDONTWRITEBYTECODE": "1",
}
os.execve(
    str(interpreter),
    [str(interpreter), "-I", "-S", str(script), *forward_args],
    environment,
)
