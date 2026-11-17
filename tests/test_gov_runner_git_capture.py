#!/usr/bin/env python3
"""Focused stdlib tests for Autoloop git baseline capture, deterministic vetoes, and portable commit checks.

Author: elvis
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module {name} from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout


def _init_repo(repo: Path) -> str:
    repo.mkdir(parents=True, exist_ok=True)
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "dev@example.com")
    _git(repo, "config", "user.name", "dev")
    (repo / "README.md").write_text("init\n", encoding="utf-8")
    _git(repo, "add", "README.md")
    _git(repo, "commit", "-qm", "chore(init): bootstrap repo\n\n- add initial readme")
    return _git(repo, "branch", "--show-current").strip()


def _write_fake_pass_pi(script_path: Path) -> None:
    script_path.write_text(
        "#!/usr/bin/env python3\n"
        "import json, sys\n"
        'print(json.dumps({"type": "session", "id": "sess-fake-reviewer"}), flush=True)\n'
        'print(json.dumps({"type": "message_end", "message": {"role": "assistant", "stopReason": "stop", '
        '"content": [{"type": "text", "text": "AUTOLOOP_VERDICT: PASS\\n0 阻塞发现"}]}}), flush=True)\n',
        encoding="utf-8",
    )
    script_path.chmod(0o755)


class GovRunnerGitCaptureTests(unittest.TestCase):
    def test_committed_clean_branch_captures_diff_and_full_log(self) -> None:
        runner = _load_module("gov_runner_m1", ROOT / "scripts/gov_runner.py")
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            base_branch = _init_repo(repo)
            _git(repo, "checkout", "-qb", "feat/clean-slice", base_branch)
            (repo / "service.py").write_text("def calc():\n    return 42\n", encoding="utf-8")
            _git(repo, "add", "service.py")
            _git(
                repo,
                "commit",
                "-m",
                "feat(service): add deterministic calc",
                "-m",
                "- return 42 for baseline verification\n- keep pure function boundary",
            )

            raw = Path(tmp) / "raw"
            raw.mkdir()
            meta = runner.capture_git_snapshot(str(repo), raw, base_ref="", review_profile="fast")
            self.assertEqual(meta["base_status"], "resolved")
            self.assertFalse(meta["truncated"])
            branch_patch = (raw / "git.branch_diff.patch").read_text(encoding="utf-8")
            compat_patch = (raw / "git.diff.patch").read_text(encoding="utf-8")
            log_txt = (raw / "git.log.txt").read_text(encoding="utf-8")
            changed_txt = (raw / "git.changed_files.txt").read_text(encoding="utf-8")
            self.assertIn("def calc():", branch_patch)
            self.assertIn("def calc():", compat_patch)
            self.assertIn("feat(service): add deterministic calc", log_txt)
            self.assertIn("keep pure function boundary", log_txt)
            self.assertIn("service.py", changed_txt)

    def test_unresolved_detached_and_pre_mr_missing_base_ref_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_p = Path(tmp)
            repo = tmp_p / "detached-repo"
            base_branch = _init_repo(repo)
            head_sha = _git(repo, "rev-parse", "HEAD").strip()
            wt = tmp_p / "wt-detached"
            _git(repo, "worktree", "add", "-q", "--detach", str(wt), head_sha)

            fake_pi = tmp_p / "fake_pi.py"
            _write_fake_pass_pi(fake_pi)

            # Case A: detached clean worktree without base_ref and 0 branch commits must veto PASS
            ev_a = tmp_p / "ev-a"
            batch_a = tmp_p / "batch-a.json"
            batch_a.write_text(
                json.dumps(
                    {
                        "batch_id": "b-detached",
                        "mode": "pi-accept",
                        "review_profile": "fast",
                        "base_ref": "",
                        "allow_rerun": False,
                        "expected_resume": None,
                        "verify_cwd": str(wt),
                        "verify_command": "true",
                        "capture_git_diff": True,
                        "ledger_dir": str(tmp_p / "ledger-a"),
                        "evidence_dir": str(ev_a),
                        "stop_cmd": ["true"],
                        "pi_cmd": [sys.executable, str(fake_pi)],
                        "pi_prompt": "check {RAW} {CWD}",
                    }
                ),
                encoding="utf-8",
            )
            folder_a = tmp_p / "101-1"
            folder_a.mkdir()
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/gov_runner.py"),
                    "--batch",
                    str(batch_a),
                    "--folder",
                    str(folder_a),
                    "--session",
                    "s-101",
                    "--resume",
                    "",
                    "--cwd",
                    str(wt),
                ],
                env={**os.environ, "AGENT_AUTOLOOP_RUN": "101"},
                capture_output=True,
                text=True,
                check=True,
            )
            receipt_a = json.loads((ev_a / "run-101/receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt_a["verdict"], "FAIL")
            self.assertFalse((ev_a / "run-101/attempt-1/cli.argv.json").exists())

            # Case B: pre-mr with empty --base-ref must set base_status=missing_base_ref and FAIL before Pi
            _git(repo, "checkout", "-qb", "feat/attached", base_branch)
            (repo / "a.py").write_text("x = 1\n", encoding="utf-8")
            _git(repo, "add", "a.py")
            _git(repo, "commit", "-m", "feat(core): add a", "-m", "- add a.py")

            ev_b = tmp_p / "ev-b"
            batch_b = tmp_p / "batch-b.json"
            batch_b.write_text(
                json.dumps(
                    {
                        "batch_id": "b-premr-nobase",
                        "mode": "pi-accept",
                        "review_profile": "pre-mr",
                        "base_ref": "",
                        "allow_rerun": False,
                        "expected_resume": None,
                        "verify_cwd": str(repo),
                        "verify_command": "true",
                        "ledger_dir": str(tmp_p / "ledger-b"),
                        "evidence_dir": str(ev_b),
                        "stop_cmd": ["true"],
                        "pi_cmd": [sys.executable, str(fake_pi)],
                        "pi_prompt": "check {RAW} {CWD}",
                    }
                ),
                encoding="utf-8",
            )
            folder_b = tmp_p / "102-1"
            folder_b.mkdir()
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/gov_runner.py"),
                    "--batch",
                    str(batch_b),
                    "--folder",
                    str(folder_b),
                    "--session",
                    "s-102",
                    "--resume",
                    "",
                    "--cwd",
                    str(repo),
                ],
                env={**os.environ, "AGENT_AUTOLOOP_RUN": "102"},
                capture_output=True,
                text=True,
                check=True,
            )
            meta_b = json.loads((ev_b / "run-102/attempt-1/git.meta.json").read_text(encoding="utf-8"))
            receipt_b = json.loads((ev_b / "run-102/receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(meta_b["base_status"], "missing_base_ref")
            self.assertEqual(receipt_b["verdict"], "FAIL")
            self.assertFalse((ev_b / "run-102/attempt-1/cli.argv.json").exists())

    def test_three_dot_diff_excludes_target_only_commits_and_unions_manifest(self) -> None:
        runner = _load_module("gov_runner_m3", ROOT / "scripts/gov_runner.py")
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            base_branch = _init_repo(repo)
            (repo / "dirty_work.py").write_text("v = 0\n", encoding="utf-8")
            _git(repo, "add", "dirty_work.py")
            _git(repo, "commit", "-m", "chore(seed): add dirty target", "-m", "- seed file")

            _git(repo, "checkout", "-qb", "feat/branch", base_branch)
            (repo / "branch_only.py").write_text("branch_val = 1\n", encoding="utf-8")
            _git(repo, "add", "branch_only.py")
            _git(repo, "commit", "-m", "feat(branch): add branch file", "-m", "- branch change")

            # Advance target branch independently after fork
            _git(repo, "checkout", "-q", base_branch)
            (repo / "target_only.py").write_text("target_val = 99\n", encoding="utf-8")
            _git(repo, "add", "target_only.py")
            _git(repo, "commit", "-m", "feat(target): advance target", "-m", "- target only")

            # Return to feature branch and add uncommitted + untracked changes
            _git(repo, "checkout", "-q", "feat/branch")
            (repo / "dirty_work.py").write_text("v = 2\n", encoding="utf-8")
            (repo / "untracked_new.py").write_text("u = 3\n", encoding="utf-8")

            raw = Path(tmp) / "raw"
            raw.mkdir()
            meta = runner.capture_git_snapshot(str(repo), raw, base_ref=base_branch, review_profile="pre-mr")
            self.assertEqual(meta["base_status"], "resolved")
            branch_diff = (raw / "git.branch_diff.patch").read_text(encoding="utf-8")
            working_diff = (raw / "git.working_diff.patch").read_text(encoding="utf-8")
            manifest = (raw / "git.changed_files.txt").read_text(encoding="utf-8")

            self.assertIn("branch_only.py", branch_diff)
            self.assertNotIn("target_only.py", branch_diff)
            self.assertIn("dirty_work.py", working_diff)
            self.assertIn("branch_only.py", manifest)
            self.assertIn("dirty_work.py", manifest)
            self.assertIn("untracked_new.py", manifest)
            self.assertNotIn("target_only.py", manifest)

    def test_patch_exceeding_2mb_ceiling_marks_truncated_and_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_p = Path(tmp)
            repo = tmp_p / "repo"
            base_branch = _init_repo(repo)
            _git(repo, "checkout", "-qb", "feat/huge", base_branch)
            (repo / "huge.txt").write_text(("abcdefghij" * 80 + "\n") * 2600, encoding="utf-8")
            _git(repo, "add", "huge.txt")
            _git(repo, "commit", "-m", "feat(data): add large payload", "-m", "- exceed 2MB diff limit")

            fake_pi = tmp_p / "fake_pi.py"
            _write_fake_pass_pi(fake_pi)
            ev = tmp_p / "ev"
            batch = tmp_p / "batch.json"
            batch.write_text(
                json.dumps(
                    {
                        "batch_id": "b-huge",
                        "mode": "pi-accept",
                        "review_profile": "fast",
                        "base_ref": base_branch,
                        "allow_rerun": False,
                        "expected_resume": None,
                        "verify_cwd": str(repo),
                        "verify_command": "true",
                        "capture_git_diff": True,
                        "ledger_dir": str(tmp_p / "ledger"),
                        "evidence_dir": str(ev),
                        "stop_cmd": ["true"],
                        "pi_cmd": [sys.executable, str(fake_pi)],
                        "pi_prompt": "check {RAW} {CWD}",
                    }
                ),
                encoding="utf-8",
            )
            folder = tmp_p / "103-1"
            folder.mkdir()
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/gov_runner.py"),
                    "--batch",
                    str(batch),
                    "--folder",
                    str(folder),
                    "--session",
                    "s-103",
                    "--resume",
                    "",
                    "--cwd",
                    str(repo),
                ],
                env={**os.environ, "AGENT_AUTOLOOP_RUN": "103"},
                capture_output=True,
                text=True,
                check=True,
            )
            meta = json.loads((ev / "run-103/attempt-1/git.meta.json").read_text(encoding="utf-8"))
            receipt = json.loads((ev / "run-103/receipt.json").read_text(encoding="utf-8"))
            self.assertTrue(meta["truncated"])
            self.assertEqual(receipt["verdict"], "FAIL")
            self.assertFalse((ev / "run-103/attempt-1/cli.argv.json").exists())

    def test_check_commit_text_portable_hygiene_and_optional_policy_decoupling(self) -> None:
        checker = _load_module("check_commit_text_m5", ROOT / "scripts/check_commit_text.py")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_p = Path(tmp)
            # 1. Concise (<150 chars) valid Conventional Commit passes when no policy file exists
            short_ok = "feat(parser): guard empty token stream\n\n- return empty list before lexer allocation\n"
            res_ok = checker.validate_commit_text(short_ok, diff_text="", policy_path=tmp_p / "nonexistent.json")
            self.assertTrue(res_ok["ok"], res_ok)

            # 2. Literal \n and Co-authored-by: and token leaks fail in portable mode
            res_lit = checker.validate_commit_text("fix(api): bad\\nnewline\n\n- body line\n")
            self.assertFalse(res_lit["ok"])
            self.assertTrue(any("literal" in e.lower() or "\\n" in e for e in res_lit["errors"]))

            res_co = checker.validate_commit_text(
                "fix(api): clean bug\n\n- fix null check\n\nCo-authored-by: Bot <bot@example.com>\n"
            )
            self.assertFalse(res_co["ok"])

            res_tok = checker.validate_commit_text(
                "fix(api): clean bug\n\n- fix check\n",
                diff_text="+const token = '" + "glpat" + "-1234567890abcdefghij';\n",
            )
            self.assertFalse(res_tok["ok"])

            # 3. External policy JSON enforces profile char bounds, headings, and custom diff patterns
            policy = tmp_p / "commit-policy.json"
            policy.write_text(
                json.dumps(
                    {
                        "profiles": {
                            "initial": {
                                "min_body_chars": 150,
                                "max_body_chars": 280,
                                "required_headings": ["背景与技术约束：", "核心改动：", "验证结果：", "影响范围："],
                            },
                            "r2": {"min_body_chars": 120, "max_body_chars": 220},
                        },
                        "forbidden_added_line_patterns": [
                            r"\b10\.(?:\d{1,3}\.){2}\d{1,3}\b"
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            res_too_short = checker.validate_commit_text(
                short_ok, diff_text="", policy_path=policy, profile="initial"
            )
            self.assertFalse(res_too_short["ok"])

            valid_initial_body = (
                "fix(产业模型): 隔离单步分组键冲突避免整单降级\n\n"
                "背景与技术约束：\n"
                "- 同名分类与产品并存时此前未隔离单步异常导致整单升级失败，需保持32KB上下文预算不超限\n\n"
                "核心改动：\n"
                "- IndustryQueryExecutor改为单步异常捕获并保留已成功步骤事实，不放宽主键冲突校验\n\n"
                "验证结果：\n"
                "- 本地单元与集成测试45项全部通过，0失败，测试环境待部署后回放验收\n\n"
                "影响范围：\n"
                "- 仅限internal-service产业查询模块，外部接口与数据库脚本无变更\n"
            )
            res_policy_ok = checker.validate_commit_text(
                valid_initial_body, diff_text="+int limit = 50;\n", policy_path=policy, profile="initial"
            )
            self.assertTrue(res_policy_ok["ok"], res_policy_ok)

            res_priv_ip = checker.validate_commit_text(
                valid_initial_body,
                diff_text='+String host = "' + "10.0" + '.0.1";\n',
                policy_path=policy,
                profile="initial",
            )
            self.assertFalse(res_priv_ip["ok"])

            # 4. Empty commit_text must NEVER silently fall back to git_log_text; decorated log header parses cleanly
            decorated_log = (
                "commit 0123456789abcdef0123456789abcdef01234567 (HEAD -> feat/x)\n"
                "Author: dev <dev@example.com>\n"
                "Commit: dev <dev@example.com>\n\n"
                "    feat(parser): guard empty token stream\n\n"
                "    - return empty list before lexer allocation\n"
            )
            res_empty_override = checker.validate_commit_text(commit_text="   \n", git_log_text=decorated_log)
            self.assertFalse(res_empty_override["ok"])
            self.assertTrue(any("empty" in e for e in res_empty_override["errors"]))

            res_decorated_ok = checker.validate_commit_text(commit_text=None, git_log_text=decorated_log)
            self.assertTrue(res_decorated_ok["ok"], res_decorated_ok)

            # 5. Malformed JSON, directory policy path, bool char bound, and invalid regex fail closed cleanly
            bad_json = tmp_p / "broken.json"
            bad_json.write_text("{broken", encoding="utf-8")
            self.assertFalse(checker.validate_commit_text(short_ok, policy_path=bad_json)["ok"])
            self.assertFalse(checker.validate_commit_text(short_ok, policy_path=tmp_p)["ok"])

            bad_schema = tmp_p / "bad-schema.json"
            bad_schema.write_text(
                json.dumps(
                    {
                        "profiles": {"initial": {"min_body_chars": True, "required_headings": "not-a-list"}},
                        "forbidden_added_line_patterns": ["[unclosed"],
                    }
                ),
                encoding="utf-8",
            )
            res_bad_schema = checker.validate_commit_text(short_ok, policy_path=bad_schema, profile="initial")
            self.assertFalse(res_bad_schema["ok"])
            self.assertGreaterEqual(len(res_bad_schema["errors"]), 3)

    def test_agy_stream_json_driver_and_model_header_tolerance(self) -> None:
        ctl = _load_module("autoloop_ctl_agy_t", ROOT / "scripts/autoloop_ctl.py")
        runner = _load_module("gov_runner_agy_t", ROOT / "scripts/gov_runner.py")

        self.assertEqual(
            ctl.build_agy_cmd("antigravity/gemini-4-carbon:medium"),
            [
                "/Users/elvis/.gemini/antigravity-cli/bin/agy-readonly-review",
                "--model",
                "gemini-4-carbon-medium",
                "--output-format",
                "stream-json",
                "--disable-slash-commands",
            ],
        )
        self.assertEqual(
            ctl.build_agy_cmd("antigravity/gemini-4-carbon:high")[2],
            "gemini-4-carbon-high",
        )
        self.assertEqual(
            runner._extract_verdict_line("**模型信息**：Gemini 4 Carbon\n\nAUTOLOOP_VERDICT: PASS\n0 阻塞发现"),
            "AUTOLOOP_VERDICT: PASS",
        )
        self.assertEqual(
            runner._extract_verdict_line("普通正文\nAUTOLOOP_VERDICT: PASS"),
            "普通正文",
        )

        with tempfile.TemporaryDirectory() as tmp:
            tmp_p = Path(tmp)
            repo = tmp_p / "repo"
            base_branch = _init_repo(repo)
            _git(repo, "checkout", "-qb", "feat/agy-driver", base_branch)
            (repo / "app.py").write_text("x = 1\n", encoding="utf-8")
            _git(repo, "add", "app.py")
            _git(repo, "commit", "-m", "feat(core): add x", "-m", "- init x for agy driver test")

            req_dir = tmp_p / "req_external"
            req_dir.mkdir()
            req_file = req_dir / "req.md"
            req_file.write_text("# req\n", encoding="utf-8")

            fake_agy = tmp_p / "fake_agy.py"
            fake_agy.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, sys\n"
                "mode = os.environ.get('FAKE_AGY_MODE', 'pass')\n"
                "print(json.dumps({'event': 'init', 'conversation_id': 'conv-agy-123'}), flush=True)\n"
                "if mode == 'pass':\n"
                "    resp = '**模型信息**：Gemini 4 Carbon\\n\\nAUTOLOOP_VERDICT: PASS\\n0 阻塞发现'\n"
                "    print(json.dumps({'event': 'result', 'result': {'conversation_id': 'conv-agy-123', 'status': 'SUCCESS', 'response': resp}}), flush=True)\n"
                "elif mode == 'mid_bypass':\n"
                "    resp = '无关开场白\\nAUTOLOOP_VERDICT: PASS'\n"
                "    print(json.dumps({'event': 'result', 'result': {'conversation_id': 'conv-agy-123', 'status': 'SUCCESS', 'response': resp}}), flush=True)\n"
                "else:\n"
                "    print(json.dumps({'event': 'result', 'result': {'conversation_id': 'conv-agy-123', 'status': 'ERROR', 'error': 'upstream error'}}), flush=True)\n",
                encoding="utf-8",
            )
            fake_agy.chmod(0o755)

            # 1. Valid AGY stream-json PASS with model header prefix and --add-dir injection
            ev1 = tmp_p / "ev1"
            b1 = tmp_p / "b1.json"
            b1.write_text(
                json.dumps(
                    {
                        "batch_id": "b-agy-pass",
                        "mode": "pi-accept",
                        "reviewer_driver": "agy",
                        "extra_read_dirs": [str(req_dir)],
                        "review_profile": "fast",
                        "base_ref": base_branch,
                        "allow_rerun": False,
                        "expected_resume": None,
                        "verify_cwd": str(repo),
                        "verify_command": "true",
                        "capture_git_diff": True,
                        "ledger_dir": str(tmp_p / "ledger1"),
                        "evidence_dir": str(ev1),
                        "stop_cmd": ["true"],
                        "pi_cmd": [sys.executable, str(fake_agy)],
                        "pi_prompt": "check {RAW} {CWD}",
                    }
                ),
                encoding="utf-8",
            )
            f1 = tmp_p / "201-1"
            f1.mkdir()
            subprocess.run(
                [
                    sys.executable, str(ROOT / "scripts/gov_runner.py"),
                    "--batch", str(b1), "--folder", str(f1), "--session", "s-201", "--resume", "", "--cwd", str(repo),
                ],
                env={**os.environ, "AGENT_AUTOLOOP_RUN": "201", "FAKE_AGY_MODE": "pass"},
                capture_output=True, text=True, check=True,
            )
            argv1 = json.loads((ev1 / "run-201/attempt-1/cli.argv.json").read_text(encoding="utf-8"))
            self.assertIn("--add-dir", argv1)
            self.assertIn(str(req_dir.resolve()), argv1)
            self.assertIn(str((ev1 / "run-201/attempt-1").resolve()), argv1)
            self.assertEqual(argv1[-2], "-p")
            r1 = json.loads((ev1 / "run-201/receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(r1["verdict"], "PASS")
            self.assertEqual(r1["native_session"], "conv-agy-123")
            self.assertEqual(r1["first_line"], "AUTOLOOP_VERDICT: PASS")
            self.assertIn("agent_product: antigravity-cli", (ev1 / "run-201/report.md").read_text(encoding="utf-8"))

            # 2. Body-only AUTOLOOP_VERDICT: PASS behind unrelated first line must FAIL
            ev2 = tmp_p / "ev2"
            b2 = tmp_p / "b2.json"
            b2.write_text(
                json.dumps(
                    {
                        **json.loads(b1.read_text(encoding="utf-8")),
                        "batch_id": "b-agy-bypass",
                        "ledger_dir": str(tmp_p / "ledger2"),
                        "evidence_dir": str(ev2),
                    }
                ),
                encoding="utf-8",
            )
            f2 = tmp_p / "202-1"
            f2.mkdir()
            subprocess.run(
                [
                    sys.executable, str(ROOT / "scripts/gov_runner.py"),
                    "--batch", str(b2), "--folder", str(f2), "--session", "s-202", "--resume", "", "--cwd", str(repo),
                ],
                env={**os.environ, "AGENT_AUTOLOOP_RUN": "202", "FAKE_AGY_MODE": "mid_bypass"},
                capture_output=True, text=True, check=True,
            )
            r2 = json.loads((ev2 / "run-202/receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(r2["verdict"], "FAIL")

            # 3. Non-SUCCESS status aborts fail-closed
            ev3 = tmp_p / "ev3"
            b3 = tmp_p / "b3.json"
            b3.write_text(
                json.dumps(
                    {
                        **json.loads(b1.read_text(encoding="utf-8")),
                        "batch_id": "b-agy-err",
                        "ledger_dir": str(tmp_p / "ledger3"),
                        "evidence_dir": str(ev3),
                    }
                ),
                encoding="utf-8",
            )
            f3 = tmp_p / "203-1"
            f3.mkdir()
            subprocess.run(
                [
                    sys.executable, str(ROOT / "scripts/gov_runner.py"),
                    "--batch", str(b3), "--folder", str(f3), "--session", "s-203", "--resume", "", "--cwd", str(repo),
                ],
                env={**os.environ, "AGENT_AUTOLOOP_RUN": "203", "FAKE_AGY_MODE": "err"},
                capture_output=True, text=True, check=True,
            )
            self.assertTrue((ev3 / "run-203/report-abort.md").is_file())
            self.assertIn("upstream error", (ev3 / "run-203/report-abort.md").read_text(encoding="utf-8"))

    def test_workflow_review_optimizations_and_manifest_alignment(self) -> None:
        # 1. Portability: no hardcoded personal home/machine strings in autoloop_ctl.py
        ctl_text = (ROOT / "scripts/autoloop_ctl.py").read_text(encoding="utf-8")
        self.assertNotIn("/Users/elvis", ctl_text)
        self.assertNotIn("elvisdemacbook-pro", ctl_text)

        # 2. OpenSpec change match extracts real test commands from tasks.md / frontmatter while keeping plain fallback
        with tempfile.TemporaryDirectory() as tmp:
            tmp_p = Path(tmp)
            proj = tmp_p / "os-proj"
            ch = proj / "openspec/changes/add-feature-x"
            ch.mkdir(parents=True)
            (ch / "proposal.md").write_text("# Proposal\n", encoding="utf-8")
            (ch / "tasks.md").write_text(
                "- [ ] 1.1 Run `openspec validate <change-id> --strict`\n"
                "- [ ] 2.1 Run `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .`\n"
                "- [ ] 2.2 Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_gov_runner_git_capture`\n",
                encoding="utf-8",
            )
            env = {
                **os.environ,
                "AUTOLOOP_STATE_ROOT": str(tmp_p / "state"),
                "AUTOLOOP_NODE_BIN": "/custom/bin/node",
                "AUTOLOOP_AI_APP_REQ_DIR": str(tmp_p / "custom-ai-req"),
            }
            matched = json.loads(
                subprocess.run(
                    [sys.executable, str(ROOT / "scripts/autoloop_ctl.py"), "match", "--cwd", str(proj)],
                    env=env,
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout
            )
            self.assertTrue(matched["matched"])
            self.assertEqual(matched["source"], "openspec_change")
            self.assertEqual(
                matched["verify_cmd"],
                "openspec validate add-feature-x --strict && "
                "PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py . && "
                "PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_gov_runner_git_capture",
            )
            self.assertNotIn("verify_argv", matched)

            # Custom AUTOLOOP_AI_APP_REQ_DIR redirection works without hardcoded personal path
            ai_proj = tmp_p / "ai_app-feature"
            ai_proj.mkdir()
            (tmp_p / "custom-ai-req").mkdir(parents=True)
            init_out = json.loads(
                subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "scripts/autoloop_ctl.py"),
                        "init-req",
                        "--cwd",
                        str(ai_proj),
                        "--slug",
                        "portability-check",
                        "--title",
                        "Portability",
                        "--summary",
                        "Scope",
                        "--cmd",
                        "true",
                        "--accept",
                        "ok",
                    ],
                    env=env,
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout
            )
            self.assertEqual(Path(init_out["req_path"]).parent.resolve(), (tmp_p / "custom-ai-req").resolve())

            # 3. gov_runner manifest role & capability profile alignment (pi-accept vs pi-verify)
            repo = tmp_p / "repo"
            _init_repo(repo)
            (repo / "app.py").write_text("x = 2\n", encoding="utf-8")
            fake_agy = tmp_p / "fake-agy.py"
            fake_agy.write_text(
                "#!/usr/bin/env python3\n"
                "import json\n"
                "print(json.dumps({'event': 'init', 'conversation_id': 'conv-role-1'}), flush=True)\n"
                "print(json.dumps({'event': 'result', 'result': {'conversation_id': 'conv-role-1', 'status': 'SUCCESS', 'response': 'AUTOLOOP_VERDICT: PASS\\n0 阻塞发现'}}), flush=True)\n",
                encoding="utf-8",
            )
            fake_agy.chmod(0o755)
            for idx, (mode, exp_ev_role, exp_ag_role, exp_prof) in enumerate(
                [
                    ("pi-accept", "batch-review", "independent-reviewer", "control-plane-high"),
                    ("pi-verify", "attempt-report", "executor", "cohesive-medium"),
                ],
                start=301,
            ):
                ev_dir = tmp_p / f"ev-{idx}"
                b_file = tmp_p / f"b-{idx}.json"
                b_file.write_text(
                    json.dumps(
                        {
                            "batch_id": f"b-{idx}",
                            "mode": mode,
                            "reviewer_driver": "agy",
                            "review_profile": "fast",
                            "allow_rerun": False,
                            "expected_resume": None,
                            "verify_cwd": str(repo),
                            "verify_command": "true",
                            "capture_git_diff": True,
                            "ledger_dir": str(tmp_p / f"ledger-{idx}"),
                            "evidence_dir": str(ev_dir),
                            "stop_cmd": ["true"],
                            "pi_cmd": [sys.executable, str(fake_agy)],
                            "pi_prompt": "check {RAW} {CWD}",
                        }
                    ),
                    encoding="utf-8",
                )
                f_dir = tmp_p / f"{idx}-1"
                f_dir.mkdir()
                subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "scripts/gov_runner.py"),
                        "--batch",
                        str(b_file),
                        "--folder",
                        str(f_dir),
                        "--session",
                        f"s-{idx}",
                        "--resume",
                        "",
                        "--cwd",
                        str(repo),
                    ],
                    env={**os.environ, "AGENT_AUTOLOOP_RUN": str(idx)},
                    capture_output=True,
                    text=True,
                    check=True,
                )
                rep = (ev_dir / f"run-{idx}/report.md").read_text(encoding="utf-8")
                self.assertIn(f"evidence_role: {exp_ev_role}\n", rep)
                self.assertIn(f"agent_role: {exp_ag_role}\n", rep)
                self.assertIn(f"capability_profile: {exp_prof}\n", rep)
                self.assertNotIn("implementation-high", rep)

        # 4. Cold-path amendment extraction & overview refresh
        amend_ref = ROOT / "references/resume-context-amendments.md"
        self.assertTrue(amend_ref.is_file(), "missing references/resume-context-amendments.md")
        amend_text = amend_ref.read_text(encoding="utf-8")
        for key in (
            "strict-local-reviewer-binding",
            "strict-local-control-plane-rebind",
            "strict-local-control-plane-return",
        ):
            self.assertIn(key, amend_text)
        approved_text = (ROOT / "references/approved-implementation-workflow.md").read_text(encoding="utf-8")
        self.assertIn("references/resume-context-amendments.md", approved_text)
        self.assertLess(len(approved_text.splitlines()), 610)

        overview_text = (ROOT / "references/workflow-overview.md").read_text(encoding="utf-8")
        doc_wf_text = (ROOT / "docs/workflow.md").read_text(encoding="utf-8")
        self.assertNotIn("schema-3", overview_text)
        self.assertIn("schema-6", overview_text)
        self.assertIn("Four Hard Anchors", overview_text)
        self.assertIn("autoloop", overview_text)
        self.assertIn("Four Hard Anchors", doc_wf_text)


if __name__ == "__main__":
    unittest.main()
