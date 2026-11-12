#!/usr/bin/env python3
"""Portable Git commit message & added-diff hygiene checker with optional policy JSON hooks.

Author: elvis
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

COMMIT_HEADER_LINE_RE = re.compile(r"^commit [0-9a-f]{40,64}(?:\s+\(.*\))?$")
HEADER_RE = re.compile(r"^(feat|fix|refactor|perf|docs|test|build|chore)\(([^()\r\n]+)\):\s+\S+")
CO_AUTHORED_RE = re.compile(r"(?im)^\s*co-authored-by\s*:")
PRIVATE_KEY_RE = re.compile(r"-----BEGIN [A-Z0-9 ]*" + r"PRIVATE KEY-----")
SECRET_TOKEN_RE = re.compile(
    r"(?:glpat"
    r"-[A-Za-z0-9_-]{10,}|ghp"
    r"_[A-Za-z0-9]{20,}|github_pat"
    r"_[A-Za-z0-9_]{20,}|sk"
    r"-[A-Za-z0-9]{20,}|xox[baprs]"
    r"-[A-Za-z0-9-]{10,})"
)


def _is_strict_int(val: object) -> bool:
    return isinstance(val, int) and not isinstance(val, bool)


def _count_units(text: str, count_mode: str = "chars") -> int:
    no_url = re.sub(r"https?://\S+", "", text)
    if count_mode == "cjk_words":
        cjk = re.findall(r"[\u4e00-\u9fff]", no_url)
        words = re.findall(r"[A-Za-z0-9_.-]+", no_url)
        return len(cjk) + len(words)
    return len(no_url.replace("\n", "").strip())


def extract_commits_from_git_log_full(log_text: str) -> list[str]:
    """Extract raw commit messages from `git log --no-decorate --no-show-signature --format=full` output."""
    commits: list[str] = []
    cur_msg_lines: list[str] | None = None
    in_headers = False
    for line in (log_text or "").splitlines():
        if COMMIT_HEADER_LINE_RE.match(line):
            if cur_msg_lines is not None:
                msg = "\n".join(cur_msg_lines).strip("\n")
                if msg.strip():
                    commits.append(msg)
            cur_msg_lines = []
            in_headers = True
            continue
        if cur_msg_lines is None:
            continue
        if in_headers:
            if line == "":
                in_headers = False
            continue
        if line.startswith("    "):
            cur_msg_lines.append(line[4:])
        elif line == "":
            cur_msg_lines.append("")
        else:
            cur_msg_lines.append(line)
    if cur_msg_lines is not None:
        msg = "\n".join(cur_msg_lines).strip("\n")
        if msg.strip():
            commits.append(msg)
    return commits


def _added_diff_lines(diff_text: str) -> list[tuple[int, str]]:
    added: list[tuple[int, str]] = []
    for idx, line in enumerate((diff_text or "").splitlines(), start=1):
        if line.startswith("+") and not line.startswith("+++"):
            added.append((idx, line[1:]))
    return added


def _validate_single_message(
    msg: str,
    profile_cfg: dict | None = None,
    label: str = "commit",
) -> list[str]:
    errors: list[str] = []
    cleaned = (msg or "").replace("\r\n", "\n").strip("\n")
    if not cleaned.strip():
        return [f"{label}: commit message is empty"]

    if "\\n" in cleaned:
        errors.append(f"{label}: contains forbidden literal '\\n' escape sequence")

    if CO_AUTHORED_RE.search(cleaned):
        errors.append(f"{label}: contains forbidden 'Co-authored-by:' trailer")

    if PRIVATE_KEY_RE.search(cleaned) or SECRET_TOKEN_RE.search(cleaned):
        errors.append(f"{label}: contains private key or secret token pattern")

    lines = cleaned.split("\n")
    header = lines[0].strip()
    m = HEADER_RE.match(header)
    if not m or not m.group(2).strip():
        errors.append(
            f"{label}: header must match '<type>(<non-empty-scope>): <subject>' "
            "(allowed types: feat|fix|refactor|perf|docs|test|build|chore)"
        )

    if len(lines) < 3 or lines[1].strip() != "" or not "\n".join(lines[2:]).strip():
        errors.append(f"{label}: requires a blank line after header and a non-empty body")
        return errors

    body = "\n".join(lines[2:]).strip()
    if profile_cfg is not None:
        count_mode = str(profile_cfg.get("count_mode") or "chars")
        if count_mode not in ("chars", "cjk_words"):
            errors.append(f"policy: unsupported count_mode {count_mode!r}")
            count_mode = "chars"
        body_chars = _count_units(body, count_mode)
        min_c = profile_cfg.get("min_body_chars")
        max_c = profile_cfg.get("max_body_chars")
        if min_c is not None:
            if not _is_strict_int(min_c):
                errors.append("policy: min_body_chars must be an integer")
            elif body_chars < int(min_c):
                errors.append(f"{label}: body length {body_chars} < policy min_body_chars {min_c}")
        if max_c is not None:
            if not _is_strict_int(max_c):
                errors.append("policy: max_body_chars must be an integer")
            elif body_chars > int(max_c):
                errors.append(f"{label}: body length {body_chars} > policy max_body_chars {max_c}")

        req_headings = profile_cfg.get("required_headings")
        if req_headings is not None:
            if not isinstance(req_headings, list) or not all(isinstance(h, str) for h in req_headings):
                errors.append("policy: required_headings must be a list of strings")
            else:
                for heading in req_headings:
                    if heading not in body:
                        errors.append(f"{label}: missing required section heading {heading!r}")

        max_bullet = profile_cfg.get("max_bullet_chars")
        if max_bullet is not None:
            if not _is_strict_int(max_bullet):
                errors.append("policy: max_bullet_chars must be an integer")
            else:
                for b_line in body.splitlines():
                    stripped = b_line.strip()
                    if stripped.startswith("- "):
                        b_len = _count_units(stripped[2:], count_mode)
                        if b_len > int(max_bullet):
                            errors.append(
                                f"{label}: bullet exceeds max_bullet_chars {max_bullet} ({b_len} units)"
                            )
    return errors


def validate_commit_text(
    commit_text: str | None = None,
    diff_text: str = "",
    policy_path: str | Path | None = None,
    profile: str = "initial",
    git_log_text: str = "",
) -> dict:
    errors: list[str] = []
    policy: dict = {}
    policy_loaded = False
    profile_cfg: dict | None = None
    extra_patterns: list[re.Pattern[str]] = []

    if policy_path is not None and str(policy_path).strip():
        p = Path(policy_path).expanduser()
        if p.exists() or p.is_symlink():
            if not p.is_file():
                errors.append(f"policy_path is not a regular file: {p}")
            else:
                try:
                    loaded = json.loads(p.read_text(encoding="utf-8"))
                except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                    errors.append(f"invalid policy JSON at {p}: {exc}")
                else:
                    if not isinstance(loaded, dict):
                        errors.append(f"policy root at {p} must be a JSON object")
                    else:
                        policy = loaded
                        policy_loaded = True

    if policy_loaded:
        profiles_raw = policy.get("profiles")
        if profiles_raw is not None:
            if not isinstance(profiles_raw, dict):
                errors.append("policy: 'profiles' must be a JSON object")
            elif profile in profiles_raw:
                cand_cfg = profiles_raw.get(profile)
                if not isinstance(cand_cfg, dict):
                    errors.append(f"policy: profile {profile!r} must be a JSON object")
                else:
                    profile_cfg = cand_cfg

        raw_pats = policy.get("forbidden_added_line_patterns")
        if raw_pats is not None:
            if not isinstance(raw_pats, list) or not all(isinstance(x, str) for x in raw_pats):
                errors.append("policy: 'forbidden_added_line_patterns' must be a list of regex strings")
            else:
                for pat in raw_pats:
                    try:
                        extra_patterns.append(re.compile(pat))
                    except re.error as exc:
                        errors.append(f"policy: invalid regex {pat!r}: {exc}")

    messages: list[tuple[str, str]] = []
    if commit_text is not None:
        messages.append(("commit_msg", commit_text))
    elif git_log_text and git_log_text.strip():
        extracted = extract_commits_from_git_log_full(git_log_text)
        for idx, m_txt in enumerate(extracted, start=1):
            messages.append((f"commit[{idx}]", m_txt))

    if not messages:
        errors.append("no commit message provided for validation")
    else:
        for idx, (label, m_txt) in enumerate(messages):
            cfg = profile_cfg if idx == 0 else None
            errors.extend(_validate_single_message(m_txt, profile_cfg=cfg, label=label))

    for line_no, content in _added_diff_lines(diff_text):
        if PRIVATE_KEY_RE.search(content) or SECRET_TOKEN_RE.search(content):
            errors.append(f"diff+{line_no}: added line contains private key or secret token pattern")
        for rx in extra_patterns:
            if rx.search(content):
                errors.append(
                    f"diff+{line_no}: added line matched policy forbidden pattern {rx.pattern!r}"
                )

    return {
        "ok": len(errors) == 0,
        "policy_loaded": policy_loaded,
        "profile": profile,
        "checked_commits": len(messages),
        "errors": errors,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate commit message and diff hygiene")
    ap.add_argument("--commit-msg-file", default="", help="Path to commit message draft file")
    ap.add_argument("--git-log-file", default="", help="Path to git log --format=full output")
    ap.add_argument("--diff-file", action="append", default=[], help="Patch file(s) to scan added lines")
    ap.add_argument("--commit-policy", default="", help="Optional JSON policy path")
    ap.add_argument("--commit-profile", default="initial", help="Policy profile name (default: initial)")
    args = ap.parse_args()

    commit_text: str | None = None
    if args.commit_msg_file:
        p = Path(args.commit_msg_file).expanduser()
        if not p.is_file():
            out = {"ok": False, "errors": [f"commit_msg_file not found: {p}"]}
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 1
        try:
            commit_text = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            out = {"ok": False, "errors": [f"unable to read commit_msg_file {p}: {exc}"]}
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return 1

    git_log_text = ""
    if commit_text is None and args.git_log_file:
        lp = Path(args.git_log_file).expanduser()
        if lp.is_file():
            try:
                git_log_text = lp.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                out = {"ok": False, "errors": [f"unable to read git_log_file {lp}: {exc}"]}
                print(json.dumps(out, ensure_ascii=False, indent=2))
                return 1

    diff_chunks: list[str] = []
    for df in args.diff_file:
        dp = Path(df).expanduser()
        if dp.is_file():
            try:
                diff_chunks.append(dp.read_text(encoding="utf-8", errors="replace"))
            except OSError as exc:
                out = {"ok": False, "errors": [f"unable to read diff_file {dp}: {exc}"]}
                print(json.dumps(out, ensure_ascii=False, indent=2))
                return 1

    res = validate_commit_text(
        commit_text=commit_text,
        diff_text="\n".join(diff_chunks),
        policy_path=args.commit_policy or None,
        profile=args.commit_profile,
        git_log_text=git_log_text,
    )
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
