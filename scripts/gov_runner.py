#!/usr/bin/env python3
# Author: elvis. Governed host-side runner for agent-autoloop (openspec-superpower-change).
# Enforces:
#   1. Per-event batch isolation via AGENT_AUTOLOOP_CONTEXT `events[-1].subject` -> `<batches_dir>/<subject>.json`
#      (backward-compatible with `--batch <file>`).
#   2. Persistent attempt/session ledger checked before any CLI launch:
#      a) second turn in same run-attempt (worker triedFresh) or resume mismatch (settleSession) -> report-abort.md, exit 0;
#      b) attempt >= 2 when batch forbids re-run (kernel retryLater) -> report-abort.md, `agent-autoloop stop <run>`, exit 0.
#   3. Deterministic local-ref Git baseline capture (`fast` vs `pre-mr`), 2MB patch ceiling, portable commit check,
#      pre/post-Pi fail-closed vetoes, and pre/post read-only Pi workspace fingerprint verification.
from __future__ import annotations

import argparse
import fcntl
import hashlib
import importlib.util
import json
import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

ABORT_RESUME = "执行中止：会话续接被拦截，已生成中止报告，禁止重跑"
ABORT_RERUN = "执行中止：重派被拦截，已调用 stop 并生成中止报告，禁止重跑"
SAFE_BATCH_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
MAX_PATCH_BYTES = 2_000_000
MAX_FAST_REFLOG_COMMITS = 50


def meta(**fields):
    print("META:" + json.dumps(fields, ensure_ascii=False), flush=True)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def resolve_batch_file(a) -> Path:
    if a.batch:
        return Path(a.batch)
    ctx_path = Path(a.context_file or os.environ.get("AGENT_AUTOLOOP_CONTEXT", ""))
    if not ctx_path.is_file():
        raise SystemExit(f"BLOCKED: context.json missing at {ctx_path}")
    ctx = json.loads(ctx_path.read_text(encoding="utf-8"))
    events = ctx.get("events") or []
    subject = (events[-1].get("subject") if events else "") or ""
    if not SAFE_BATCH_ID.match(subject):
        raise SystemExit(f"BLOCKED: invalid or empty batch subject {subject!r} in context.json")
    batch_file = (Path(a.batches_dir) / f"{subject}.json").resolve()
    if batch_file.parent != Path(a.batches_dir).resolve() or not batch_file.is_file():
        raise SystemExit(f"BLOCKED: batch contract missing at {batch_file}")
    return batch_file


def git_fingerprint(cwd: str) -> str:
    root = Path(cwd).resolve()
    h = hashlib.sha256()
    if subprocess.run(["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"], capture_output=True).returncode == 0:
        hd = subprocess.run(["git", "-C", str(root), "rev-parse", "--verify", "HEAD"], capture_output=True).stdout
        st = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "-z"], capture_output=True).stdout
        df = subprocess.run(["git", "-C", str(root), "diff", "HEAD"], capture_output=True).stdout
        h.update(b"GIT\0" + hd + b"\0" + st + b"\0" + df + b"\0")
        others = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--others", "--exclude-standard", "-z"],
            capture_output=True,
        ).stdout.split(b"\0")
        for raw_rel in sorted(filter(None, others)):
            rel = raw_rel.decode("utf-8", errors="surrogateescape")
            fp = root / rel
            h.update(raw_rel + b"\0")
            if fp.is_symlink():
                h.update(b"L:" + os.readlink(fp).encode("utf-8", errors="surrogateescape") + b"\0")
            elif fp.is_file():
                h.update(b"F:" + hashlib.sha256(fp.read_bytes()).digest() + b"\0")
        return h.hexdigest()

    skip_dirs = {".git", "__pycache__", ".pytest_cache", "node_modules", ".mypy_cache", ".ruff_cache"}
    h.update(b"DIR\0")
    for base, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in skip_dirs)
        for fn in sorted(files):
            if fn == ".DS_Store":
                continue
            fp = Path(base) / fn
            rel = str(fp.relative_to(root)).encode("utf-8", errors="surrogateescape")
            h.update(rel + b"\0")
            if fp.is_symlink():
                h.update(b"L:" + os.readlink(fp).encode("utf-8", errors="surrogateescape") + b"\0")
            elif fp.is_file():
                h.update(b"F:" + hashlib.sha256(fp.read_bytes()).digest() + b"\0")
    return h.hexdigest()


def _git_run(cwd: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", cwd, *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _git_run_bytes(cwd: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", cwd, *args], capture_output=True)


def _parse_name_status_z(raw_bytes: bytes) -> dict[str, str]:
    text = raw_bytes.decode("utf-8", errors="replace")
    tokens = text.split("\0")
    if tokens and tokens[-1] == "":
        tokens.pop()
    entries: dict[str, str] = {}
    i = 0
    while i < len(tokens):
        status = tokens[i]
        i += 1
        if not status or i >= len(tokens):
            break
        first = tokens[i]
        i += 1
        if status.startswith(("R", "C")) and i < len(tokens):
            second = tokens[i]
            i += 1
            entries[second] = f"{status}\t{first}\t{second}"
        else:
            entries[first] = f"{status}\t{first}"
    return entries


def _write_bounded_patch(path: Path, raw_bytes: bytes) -> tuple[int, bool]:
    total = len(raw_bytes)
    if total > MAX_PATCH_BYTES:
        path.write_bytes(raw_bytes[:MAX_PATCH_BYTES])
        return total, True
    path.write_bytes(raw_bytes)
    return total, False


def _resolve_commit(cwd: str, ref: str) -> str:
    if not ref or ref.startswith("-"):
        return ""
    p = _git_run(cwd, "rev-parse", "--verify", "-q", f"{ref}^{{commit}}")
    return p.stdout.strip() if p.returncode == 0 else ""


def _commit_count(cwd: str, rev_range: str) -> int | None:
    p = _git_run(cwd, "rev-list", "--count", rev_range)
    if p.returncode == 0 and p.stdout.strip().isdigit():
        return int(p.stdout.strip())
    return None


def capture_git_snapshot(
    work_cwd: str,
    raw: Path,
    base_ref: str = "",
    review_profile: str = "fast",
) -> dict:
    profile = (review_profile or "fast").strip() or "fast"
    req_base = (base_ref or "").strip()

    if _git_run(work_cwd, "rev-parse", "--is-inside-work-tree").returncode != 0:
        meta_obj = {
            "base_status": "not_git_repo",
            "requested_base_ref": req_base,
            "resolved_base_sha": "",
            "merge_base_sha": "",
            "head_sha": "",
            "detached": False,
            "branch_commit_count": 0,
            "working_dirty": False,
            "untracked_count": 0,
            "changed_file_count": 0,
            "branch_diff_bytes": 0,
            "working_diff_bytes": 0,
            "truncated": False,
        }
        (raw / "git.meta.json").write_text(json.dumps(meta_obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return meta_obj

    st = _git_run(work_cwd, "status", "-sb")
    (raw / "git.status.txt").write_text(st.stdout, encoding="utf-8")

    head_sha = _resolve_commit(work_cwd, "HEAD")
    sym = _git_run(work_cwd, "symbolic-ref", "-q", "--short", "HEAD")
    branch_name = sym.stdout.strip() if sym.returncode == 0 else ""
    detached = not bool(branch_name)

    working_ns_raw = _git_run_bytes(work_cwd, "diff", "--name-status", "-z", "--find-renames", "HEAD").stdout if head_sha else b""
    working_entries = _parse_name_status_z(working_ns_raw)
    untracked_raw = _git_run_bytes(work_cwd, "ls-files", "--others", "--exclude-standard", "-z").stdout
    untracked_paths = [
        p.decode("utf-8", errors="replace")
        for p in untracked_raw.split(b"\0")
        if p
    ]
    working_diff_raw = _git_run_bytes(work_cwd, "diff", "--find-renames", "HEAD").stdout if head_sha else b""
    working_dirty = bool(working_entries) or bool(untracked_paths)

    base_status = "unresolved"
    resolved_base_sha = ""
    merge_base_sha = ""

    if profile == "pre-mr" and not req_base:
        base_status = "missing_base_ref"
    elif req_base:
        cand_sha = _resolve_commit(work_cwd, req_base)
        if not cand_sha or not head_sha:
            base_status = "invalid_base_ref"
        else:
            mb = _git_run(work_cwd, "merge-base", cand_sha, head_sha)
            if mb.returncode != 0 or not mb.stdout.strip():
                base_status = "invalid_base_ref"
            else:
                resolved_base_sha = cand_sha
                merge_base_sha = mb.stdout.strip()
                base_status = "resolved"
    elif head_sha and not detached:
        # Tier 2 (fast only): @{upstream}..HEAD first, else branch `Created from <ref>` reflog within 50 commits
        up_sha = _resolve_commit(work_cwd, "@{upstream}")
        if up_sha:
            mb = _git_run(work_cwd, "merge-base", head_sha, up_sha)
            mb_sha = mb.stdout.strip() if mb.returncode == 0 else ""
            if mb_sha and mb_sha != head_sha:
                resolved_base_sha = up_sha
                merge_base_sha = mb_sha
                base_status = "resolved"
        if base_status != "resolved":
            rl = _git_run(work_cwd, "reflog", "show", "--format=%H\t%gs", branch_name)
            if rl.returncode == 0:
                for line in rl.stdout.splitlines():
                    if "\t" not in line:
                        continue
                    entry_sha, subject = line.split("\t", 1)
                    m = re.match(r"^branch:\s+Created from\s+(.+)$", subject.strip())
                    if not m:
                        continue
                    raw_ref = m.group(1).strip()
                    cand_sha = entry_sha.strip() if raw_ref == "HEAD" else (_resolve_commit(work_cwd, raw_ref) or entry_sha.strip())
                    if not cand_sha:
                        continue
                    mb = _git_run(work_cwd, "merge-base", head_sha, cand_sha)
                    mb_sha = mb.stdout.strip() if mb.returncode == 0 else ""
                    if not mb_sha or mb_sha == head_sha:
                        continue
                    cnt = _commit_count(work_cwd, f"{mb_sha}..{head_sha}")
                    if cnt is not None and 1 <= cnt <= MAX_FAST_REFLOG_COMMITS:
                        resolved_base_sha = cand_sha
                        merge_base_sha = mb_sha
                        base_status = "resolved"
                        break
    elif head_sha and detached:
        # Tier 3 (fast only): detached HEAD reflog (`checkout: moving from <ref>` / `reset: moving to <ref>`)
        rl = _git_run(work_cwd, "log", "-g", "--format=%gs", "HEAD")
        if rl.returncode == 0:
            for subject in rl.stdout.splitlines():
                subj = subject.strip()
                m = re.match(r"^checkout:\s+moving from\s+(\S+)\s+to\s+", subj) or re.match(
                    r"^reset:\s+moving to\s+(\S+)$", subj
                )
                if not m:
                    continue
                cand_sha = _resolve_commit(work_cwd, m.group(1))
                if not cand_sha or cand_sha == head_sha:
                    continue
                if _git_run(work_cwd, "merge-base", "--is-ancestor", cand_sha, head_sha).returncode != 0:
                    continue
                cnt = _commit_count(work_cwd, f"{cand_sha}..{head_sha}")
                if cnt is not None and 1 <= cnt <= MAX_FAST_REFLOG_COMMITS:
                    resolved_base_sha = cand_sha
                    merge_base_sha = cand_sha
                    base_status = "resolved"
                    break

    branch_entries: dict[str, str] = {}
    branch_diff_raw = b""
    compat_diff_raw = working_diff_raw
    log_text = ""
    branch_commit_count = 0

    if base_status == "resolved" and resolved_base_sha and merge_base_sha:
        branch_ns_raw = _git_run_bytes(
            work_cwd, "diff", "--name-status", "-z", "--find-renames", f"{resolved_base_sha}...HEAD"
        ).stdout
        branch_entries = _parse_name_status_z(branch_ns_raw)
        branch_diff_raw = _git_run_bytes(
            work_cwd, "diff", "--find-renames", f"{resolved_base_sha}...HEAD"
        ).stdout
        lg = _git_run(work_cwd, "log", "--no-decorate", "--no-show-signature", "--format=full", f"{merge_base_sha}..HEAD")
        log_text = lg.stdout if lg.returncode == 0 else ""
        branch_commit_count = _commit_count(work_cwd, f"{merge_base_sha}..HEAD") or 0
        if working_dirty:
            compat_diff_raw = _git_run_bytes(work_cwd, "diff", "--find-renames", merge_base_sha).stdout
        else:
            compat_diff_raw = branch_diff_raw

    union_map: dict[str, str] = {}
    union_map.update(branch_entries)
    union_map.update(working_entries)
    for up in untracked_paths:
        union_map.setdefault(up, f"?\t{up}")
    changed_lines = [union_map[k] for k in sorted(union_map)]
    (raw / "git.changed_files.txt").write_text(
        ("\n".join(changed_lines) + "\n") if changed_lines else "",
        encoding="utf-8",
    )
    (raw / "git.log.txt").write_text(log_text, encoding="utf-8")

    b_bytes, b_trunc = _write_bounded_patch(raw / "git.branch_diff.patch", branch_diff_raw)
    w_bytes, w_trunc = _write_bounded_patch(raw / "git.working_diff.patch", working_diff_raw)
    _, c_trunc = _write_bounded_patch(raw / "git.diff.patch", compat_diff_raw)
    truncated = b_trunc or w_trunc or c_trunc

    meta_obj = {
        "base_status": base_status,
        "requested_base_ref": req_base,
        "resolved_base_sha": resolved_base_sha,
        "merge_base_sha": merge_base_sha,
        "head_sha": head_sha,
        "detached": detached,
        "branch_commit_count": branch_commit_count,
        "working_dirty": working_dirty,
        "untracked_count": len(untracked_paths),
        "changed_file_count": len(changed_lines),
        "branch_diff_bytes": b_bytes,
        "working_diff_bytes": w_bytes,
        "truncated": truncated,
    }
    (raw / "git.meta.json").write_text(json.dumps(meta_obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return meta_obj


def _load_commit_checker(batch: dict):
    cand = batch.get("commit_checker")
    checker_path = Path(cand) if cand else (Path(__file__).resolve().parent / "check_commit_text.py")
    if not checker_path.is_file():
        raise RuntimeError(f"check_commit_text.py missing at {checker_path}")
    spec = importlib.util.spec_from_file_location("autoloop_check_commit_text", checker_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {checker_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def evaluate_deterministic_vetoes(batch: dict, snap_meta: dict | None, raw: Path) -> list[str]:
    errors: list[str] = []
    profile = (batch.get("review_profile") or "fast").strip() or "fast"
    commit_msg_file = (batch.get("commit_msg_file") or "").strip()

    if snap_meta is not None:
        bs = snap_meta.get("base_status")
        if bs == "missing_base_ref":
            errors.append("pre-mr 模式必须显式传入 --base-ref（base_status=missing_base_ref）")
        elif bs == "invalid_base_ref":
            errors.append(f"--base-ref={snap_meta.get('requested_base_ref')!r} 无法解析为本地提交（base_status=invalid_base_ref）")
        elif bs == "not_git_repo" and profile == "pre-mr":
            errors.append("pre-mr 模式要求目标目录为有效 Git 仓库")

        if snap_meta.get("truncated"):
            errors.append(f"Git Diff 超过 {MAX_PATCH_BYTES} 字节上限（truncated=true），拒绝在残缺补丁上签收")

        if profile == "pre-mr" and bs not in ("resolved", "missing_base_ref", "invalid_base_ref"):
            errors.append(f"pre-mr 基线未解析（base_status={bs}）")

        clean_worktree = not snap_meta.get("working_dirty") and int(snap_meta.get("untracked_count") or 0) == 0
        if bs != "not_git_repo" and clean_worktree and (bs != "resolved" or int(snap_meta.get("branch_diff_bytes") or 0) == 0):
            errors.append(f"工作区干净且无可见分支净 Diff（base_status={bs}），拒绝空变更签收 PASS")

    log_file = raw / "git.log.txt"
    log_text = ""
    if log_file.is_file():
        try:
            log_text = log_file.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            errors.append(f"无法读取 git.log.txt：{exc}")

    if profile == "pre-mr" and (commit_msg_file or log_text.strip()):
        commit_text: str | None = None
        can_validate_commit = True
        if commit_msg_file:
            cp = Path(commit_msg_file).expanduser()
            if not cp.is_file():
                errors.append(f"--commit-msg-file 文件不存在：{cp}")
                can_validate_commit = False
            else:
                try:
                    commit_text = cp.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError) as exc:
                    errors.append(f"--commit-msg-file 读取失败（{cp}）：{exc}")
                    can_validate_commit = False
        if can_validate_commit:
            try:
                checker = _load_commit_checker(batch)
                diff_parts: list[str] = []
                for name in ("git.branch_diff.patch", "git.working_diff.patch"):
                    pf = raw / name
                    if pf.is_file():
                        diff_parts.append(pf.read_text(encoding="utf-8", errors="replace"))
                c_res = checker.validate_commit_text(
                    commit_text=commit_text,
                    diff_text="\n".join(diff_parts),
                    policy_path=batch.get("commit_policy") or None,
                    profile=batch.get("commit_profile") or "initial",
                    git_log_text="" if commit_text is not None else log_text,
                )
                (raw / "commit_check.json").write_text(
                    json.dumps(c_res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
                )
                if not c_res.get("ok"):
                    for item in c_res.get("errors") or []:
                        errors.append(f"Commit 门禁未通过：{item}")
            except Exception as exc:
                errors.append(f"Commit 检查器异常：{exc}")

    return errors


def _write_report_and_receipt(
    *,
    batch: dict,
    ev: Path,
    raw: Path,
    run: str,
    attempt: int,
    session: str | None,
    v_code: int,
    readonly_ok: bool,
    passed: bool,
    text: str,
    cli_launched: bool = True,
    veto_errors: list[str] | None = None,
) -> None:
    ev_result = "pass" if passed else "fail"
    first_line = text.splitlines()[0] if text else "空"
    if batch["mode"] in ("pi-verify", "pi-accept"):
        c_sha = batch.get("canonical_sha256", "0" * 64)
        c_rev = batch.get("contract_revision", 1)
        manifest = (
            "<!-- COOP_EVIDENCE_MANIFEST_START -->\n```yaml\n"
            f"evidence_schema_version: 2\nevidence_role: attempt-report\nevidence_result: {ev_result}\n"
            f"change_id: {batch.get('change_id', batch['batch_id'])}\n"
            f"current_batch: {batch.get('current_batch', 1)}\nattempt: {attempt}\n"
            f"contract_revision: {c_rev}\ncanonical_sha256: {c_sha}\n"
            f"agent_product: pi\nagent_instance_id: {session or 'pre-cli-deterministic-gate'}\n"
            f"agent_role: executor\ncapability_profile: implementation-high\n```\n"
            "<!-- COOP_EVIDENCE_MANIFEST_END -->\n\n"
        )
        (ev / "report.md").write_text(manifest + text + "\n", encoding="utf-8")
    else:
        (ev / "report.md").write_text(text + "\n", encoding="utf-8")

    receipt = {
        "evidence_schema_version": 2,
        "batch_id": batch["batch_id"],
        "verdict": "PASS" if passed else "FAIL",
        "run": run,
        "attempt": attempt,
        "native_session": session,
        "cli_launched": cli_launched,
        "verify_exit_code": v_code,
        "reviewer_readonly_verified": readonly_ok,
        "veto_errors": veto_errors or [],
        "first_line": first_line,
        "report_path": str(ev / "report.md"),
        "report_sha256": sha(ev / "report.md"),
        "raw_sha256": {p.name: sha(p) for p in sorted(raw.glob("*")) if p.is_file()},
    }
    (ev / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", default="")
    ap.add_argument("--batches-dir", default="")
    ap.add_argument("--context-file", default="")
    for name in ("folder", "session", "resume", "cwd"):
        ap.add_argument("--" + name, required=True)
    a = ap.parse_args()
    if not a.batch and not a.batches_dir:
        raise SystemExit("BLOCKED: either --batch or --batches-dir is required")

    batch = json.loads(resolve_batch_file(a).read_text(encoding="utf-8"))
    run = os.environ["AGENT_AUTOLOOP_RUN"]
    folder_run, attempt = Path(a.folder).name.rsplit("-", 1)
    if folder_run != run:
        raise SystemExit(f"BLOCKED: folder {a.folder} does not belong to run {run}")
    attempt = int(attempt)
    resume = a.resume or None
    ev = Path(batch["evidence_dir"]) / f"run-{run}"
    ev.mkdir(parents=True, exist_ok=True)
    ledger_dir = Path(batch["ledger_dir"])
    ledger_dir.mkdir(parents=True, exist_ok=True)
    ledger_file = ledger_dir / f"{batch['batch_id']}.json"
    with open(ledger_dir / ".lock", "a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        ledger = json.loads(ledger_file.read_text()) if ledger_file.exists() else {"batch_id": batch["batch_id"], "launches": []}
        same_attempt = [x for x in ledger["launches"] if x["run"] == run and x["attempt"] == attempt]
        action, reason = "launch", None
        if attempt >= 2 and not batch.get("allow_rerun", False):
            action, reason = "stop", f"attempt {attempt} is a kernel re-dispatch; batch forbids re-run"
        elif same_attempt:
            action, reason = "abort", "second turn in the same run-attempt (worker triedFresh); prior session not reused"
        elif resume != batch.get("expected_resume"):
            action, reason = "abort", f"resume {resume!r} != contract expected_resume {batch.get('expected_resume')!r}"
        record = {"run": run, "attempt": attempt, "turn": len(same_attempt) + 1, "folder": a.folder,
                  "session_arg": a.session, "resume_arg": resume, "pid": os.getpid(),
                  "at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "action": action, "reason": reason}
        ledger["launches"].append(record)
        tmp = ledger_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
        tmp.replace(ledger_file)
    if action != "launch":
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        with open(ev / "report-abort.md", "a") as f:
            f.write(f"# 执行中止报告\n\n- batch: `{batch['batch_id']}`\n- run/attempt/turn: {run}/{attempt}/{record['turn']}\n"
                    f"- action: `{action}`\n- reason: {reason}\n- resume_arg: `{resume}`\n- CLI launched: no\n"
                    f"- 治理结论: BLOCKED（禁止重跑，不转 FIX）\n")
            f.flush()
        meta(session=a.session, started=True, finished=True)
        print(ABORT_RERUN if action == "stop" else ABORT_RESUME, flush=True)
        if action == "stop":
            p = subprocess.run(batch["stop_cmd"] + [run], capture_output=True, text=True, timeout=30)
            stop = {"cmd": batch["stop_cmd"] + [run], "exit": p.returncode, "stdout": p.stdout, "stderr": p.stderr}
            with open(ev / "report-abort.md", "a") as f:
                f.write(f"- stop: `{json.dumps(stop, ensure_ascii=False)}`\n\n")
                f.flush()
        return 0
    return launch(batch, a, run, attempt, resume, ev)


def launch(batch, a, run, attempt, resume, ev):
    raw = ev / f"attempt-{attempt}"
    raw.mkdir(exist_ok=True)
    v_code = 0
    snap_meta: dict | None = None
    veto_errors: list[str] = []
    work_cwd = batch.get("verify_cwd") or a.cwd
    if batch["mode"] == "stub":
        cmd = batch["cli_cmd"] + [batch["stub_mode"], resume or "NULL_RESUME"]
        fp_before_pi = "stub"
    else:
        v_cmd = batch.get("verify_command")
        if not v_cmd or (isinstance(v_cmd, str) and not v_cmd.strip()):
            with open(ev / "report-abort.md", "a") as f:
                f.write("# 执行中止报告\n\n- reason: empty verify_command is forbidden\n- 治理结论: BLOCKED（禁止空命令验收）\n\n")
            meta(session=a.session, started=True, finished=True)
            print("执行中止：验证命令为空，禁止无命令验收", flush=True)
            return 0
        with open(raw / "verify.stdout", "w") as v_out, open(raw / "verify.stderr", "w") as v_err:
            use_shell = isinstance(v_cmd, str)
            v = subprocess.run(v_cmd, shell=use_shell, cwd=work_cwd, stdout=v_out, stderr=v_err, text=True,
                               timeout=int(batch.get("verify_timeout", 600)))
            v_code = v.returncode
        (raw / "verify.exit").write_text(f"{v_code}\n")

        review_profile = (batch.get("review_profile") or "fast").strip() or "fast"
        if batch.get("capture_git_diff") or review_profile == "pre-mr":
            snap_meta = capture_git_snapshot(
                work_cwd,
                raw,
                base_ref=batch.get("base_ref", ""),
                review_profile=review_profile,
            )

        veto_errors = evaluate_deterministic_vetoes(batch, snap_meta, raw)
        if veto_errors:
            body_lines = [
                "AUTOLOOP_VERDICT: FAIL",
                "",
                "确定性前置门禁未通过（未启动只读审查 CLI）：",
                *[f"- {err}" for err in veto_errors],
            ]
            text = "\n".join(body_lines)
            _write_report_and_receipt(
                batch=batch,
                ev=ev,
                raw=raw,
                run=run,
                attempt=attempt,
                session=None,
                v_code=v_code,
                readonly_ok=True,
                passed=False,
                text=text,
                cli_launched=False,
                veto_errors=veto_errors,
            )
            meta(session=a.session, started=True, finished=True)
            print("报告已交付：治理结论见 report.md（AUTOLOOP_VERDICT: FAIL）", flush=True)
            return 0

        fp_before_pi = git_fingerprint(work_cwd)
        prompt = batch["pi_prompt"].replace("{RAW}", str(raw)).replace("{CWD}", str(work_cwd))
        cmd = batch["pi_cmd"] + ["--session-dir", str(raw / "pi-sessions")] + \
            (["--session", resume] if resume else []) + [prompt]

    (raw / "cli.argv.json").write_text(json.dumps(cmd, ensure_ascii=False, indent=2) + "\n")
    session, started, lines = None, False, []
    with open(raw / "cli.stdout", "w") as out, open(raw / "cli.stderr", "w") as err_f:
        proc = subprocess.Popen(cmd, cwd=work_cwd, stdout=subprocess.PIPE, stderr=err_f, text=True)
        for line in proc.stdout:
            out.write(line)
            out.flush()
            lines.append(line.rstrip("\n"))
            if batch["mode"] == "stub":
                if line.startswith("SESSION:"):
                    session = line.split(":", 1)[1].strip()
                hit = line.startswith("STARTED")
            else:
                event = json.loads(line) if line.startswith("{") else {}
                if event.get("type") == "session":
                    session = event.get("id")
                hit = event.get("type") == "session"
            if hit and not started:
                started = True
                meta(session=session or a.session, started=True)
        code = proc.wait()

    err = (raw / "cli.stderr").read_text(errors="replace")
    (raw / "cli.exit").write_text(f"{code}\n")
    if code != 0:
        if started and not batch.get("allow_rerun", False):
            with open(ev / "report-abort.md", "a") as f:
                f.write(f"# 执行中止报告\n\n- cli exit {code}: `{err.strip()[:500]}`\n- 治理结论: BLOCKED（禁止重跑）\n\n")
            meta(session=session or a.session, started=True, finished=True)
            print("执行中止：CLI 异常退出，已生成中止报告，禁止重跑", flush=True)
            return 0
        meta(session=session or a.session, started=started)
        sys.stderr.write(err or f"cli exit {code}")
        return code
    if batch["mode"] == "stub":
        text = "\n".join(l for l in lines if not l.startswith(("STARTED", "SESSION:")))
    else:
        events = [json.loads(l) for l in lines if l.startswith("{")]
        finals = [e["message"] for e in events if e.get("type") == "message_end" and e.get("message", {}).get("role") == "assistant"]
        last = finals[-1] if finals else {}
        if last.get("stopReason") != "stop":
            err_msg = last.get("errorMessage") or f"stopReason={last.get('stopReason')!r}"
            if not batch.get("allow_rerun", False):
                with open(ev / "report-abort.md", "a") as f:
                    f.write(f"# 执行中止报告\n\n- assistant error: `{err_msg}`\n- 治理结论: BLOCKED（禁止重跑）\n\n")
                meta(session=session or a.session, started=True, finished=True)
                print(f"执行中止：模型未正常完成（{err_msg[:120]}），禁止重跑", flush=True)
                return 0
            meta(session=session, started=started)
            sys.stderr.write(f"BLOCKED: assistant stopReason != stop ({err_msg})")
            return 4
        text = "".join(c.get("text", "") for c in last.get("content", []) if c.get("type") == "text").strip()
    expected = batch.get("expected_resume")
    if expected and session != expected:
        with open(ev / "report-abort.md", "a") as f:
            f.write(f"# 执行中止报告\n\n- post-output session {session!r} != expected {expected!r}\n- 治理结论: BLOCKED\n\n")
        meta(session=session, started=True, finished=True)
        print("执行中止：结果后会话身份不符，已生成中止报告，禁止重跑", flush=True)
        return 0

    fp_after_pi = "stub" if batch["mode"] == "stub" else git_fingerprint(work_cwd)
    readonly_ok = (fp_before_pi == fp_after_pi)
    if not readonly_ok:
        with open(ev / "report-abort.md", "a") as f:
            f.write("# 执行中止报告\n\n- reason: Workspace mutated during read-only Pi review\n- 治理结论: BLOCKED\n\n")
        meta(session=session, started=True, finished=True)
        print("执行中止：只读审查期间工作区发生变化，结果作废", flush=True)
        return 0

    first_line = text.splitlines()[0] if text else "空"
    passed = (
        (v_code == 0)
        and not veto_errors
        and ("AUTOLOOP_VERDICT: PASS" in first_line or "VERIFY: PASS" in first_line)
    )
    _write_report_and_receipt(
        batch=batch,
        ev=ev,
        raw=raw,
        run=run,
        attempt=attempt,
        session=session,
        v_code=v_code,
        readonly_ok=readonly_ok,
        passed=passed,
        text=text,
        cli_launched=True,
        veto_errors=veto_errors,
    )
    meta(session=session, started=True, finished=True)
    print("报告已交付：治理结论见 report.md（" + first_line + "）", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
