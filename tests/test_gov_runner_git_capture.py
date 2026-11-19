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
                str(ctl.AGY_REVIEW_BIN),
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

    def test_verify_short_circuit_failure_kind_timeout_killpg_and_redaction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_p = Path(tmp)
            repo = tmp_p / "repo"
            _init_repo(repo)
            (repo / "app.py").write_text("x = 2\n", encoding="utf-8")

            fake_agy = tmp_p / "fake-agy.py"
            fake_agy.write_text(
                "#!/usr/bin/env python3\n"
                "import json\n"
                "print(json.dumps({'event': 'init', 'conversation_id': 'conv-pass-1'}), flush=True)\n"
                "print(json.dumps({'event': 'result', 'result': {'conversation_id': 'conv-pass-1', 'status': 'SUCCESS', 'response': 'AUTOLOOP_VERDICT: PASS\\n0 阻塞发现'}}), flush=True)\n",
                encoding="utf-8",
            )
            fake_agy.chmod(0o755)

            def _run_batch(run_no: int, extra: dict) -> tuple[dict, Path]:
                ev_dir = tmp_p / f"ev-{run_no}"
                b_file = tmp_p / f"b-{run_no}.json"
                payload = {
                    "batch_id": f"b-{run_no}",
                    "mode": "pi-accept",
                    "reviewer_driver": "agy",
                    "review_profile": "fast",
                    "allow_rerun": False,
                    "expected_resume": None,
                    "verify_cwd": str(repo),
                    "verify_command": "true",
                    "verify_timeout": 10,
                    "capture_git_diff": True,
                    "ledger_dir": str(tmp_p / f"ledger-{run_no}"),
                    "evidence_dir": str(ev_dir),
                    "stop_cmd": ["true"],
                    "pi_cmd": [sys.executable, str(fake_agy), "--model", "gemini-4-carbon-medium"],
                    "pi_prompt": "check {RAW} {CWD}",
                    **extra,
                }
                b_file.write_text(json.dumps(payload), encoding="utf-8")
                f_dir = tmp_p / f"{run_no}-1"
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
                        f"s-{run_no}",
                        "--resume",
                        "",
                        "--cwd",
                        str(repo),
                    ],
                    env={**os.environ, "AGENT_AUTOLOOP_RUN": str(run_no)},
                    capture_output=True,
                    text=True,
                    check=True,
                )
                rc = json.loads((ev_dir / f"run-{run_no}/receipt.json").read_text(encoding="utf-8"))
                return rc, ev_dir / f"run-{run_no}"

            # A. Missing executable (127) -> setup_or_env_error, short-circuited before CLI
            rc_env, run_env = _run_batch(401, {"verify_command": "nonexistent_cli_bin_xyz_99"})
            self.assertEqual(rc_env["verdict"], "FAIL")
            self.assertFalse(rc_env["cli_launched"])
            self.assertEqual(rc_env["failure_kind"], "setup_or_env_error")
            self.assertFalse((run_env / "attempt-1/cli.argv.json").exists())

            # B. ModuleNotFoundError (exit 1) -> verification_failed + full secret redaction (R2 + quoted space)
            leak_script = tmp_p / "leak_fail.py"
            leak_script.write_text(
                "import sys\n"
                "sys.stderr.write(\n"
                "    'conn=postgres://admin:p@ss@127.0.0.1:5432/db '\n"
                "    'headers={\"Authorization\": \"Bearer sk-abc z9w8q7\", \"api_key\":\"k1_sec\"} '\n"
                "    \"password: 'x y'\\n\"\n"
                ")\n"
                "raise ModuleNotFoundError(\"No module named 'missing_dep_q9'\")\n",
                encoding="utf-8",
            )
            rc_mod, run_mod = _run_batch(402, {"verify_command": f'"{sys.executable}" "{leak_script}"'})
            self.assertEqual(rc_mod["verdict"], "FAIL")
            self.assertFalse(rc_mod["cli_launched"])
            self.assertEqual(rc_mod["failure_kind"], "verification_failed")
            rep_mod = (run_mod / "report.md").read_text(encoding="utf-8")
            raw_rc_mod = (run_mod / "receipt.json").read_text(encoding="utf-8")
            for secret_sub in ("p@ss", "ss@", "sk-abc", "z9w8q7", "k1_sec", "x y", " y'"):
                self.assertNotIn(secret_sub, rep_mod)
                self.assertNotIn(secret_sub, raw_rc_mod)

            # C. Process-group timeout kills background grandchild (R5)
            pid_file = tmp_p / "grandchild.pid"
            sleep_spawner = tmp_p / "spawn_sleep.py"
            sleep_spawner.write_text(
                "import pathlib, subprocess, sys, time\n"
                f"p = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'])\n"
                f"pathlib.Path({str(pid_file)!r}).write_text(str(p.pid), encoding='utf-8')\n"
                "time.sleep(30)\n",
                encoding="utf-8",
            )
            rc_to, _ = _run_batch(
                403,
                {"verify_command": f'"{sys.executable}" "{sleep_spawner}"', "verify_timeout": 1},
            )
            self.assertEqual(rc_to["verdict"], "FAIL")
            self.assertEqual(rc_to["verify_exit_code"], 124)
            self.assertEqual(rc_to["failure_kind"], "timeout")
            self.assertFalse(rc_to["cli_launched"])
            grandchild_pid = int(pid_file.read_text(encoding="utf-8").strip())
            with self.assertRaises(ProcessLookupError):
                os.kill(grandchild_pid, 0)

            # D. Non-collapsing failure_signature on distinct unittest failures sharing FAILED (failures=1) footer (R1)
            runner_mod = _load_module("gov_runner_sig_test", ROOT / "scripts/gov_runner.py")
            sig_fn = runner_mod._compute_failure_signature
            out_a1 = (
                "======================================================================\n"
                "FAIL: test_alpha (tests.test_demo.DemoTest)\n"
                "AssertionError: 1 != 2 in /tmp/run_1/work\n"
                "Ran 2 tests in 0.014s\n\nFAILED (failures=1)\n"
            )
            out_a2 = (
                "======================================================================\n"
                "FAIL: test_alpha (tests.test_demo.DemoTest)\n"
                "AssertionError: 1 != 2 in /private/tmp/run_99/work\n"
                "Ran 2 tests in 1.932s\n\nFAILED (failures=1)\n"
            )
            out_b = (
                "======================================================================\n"
                "FAIL: test_beta (tests.test_demo.DemoTest)\n"
                "AssertionError: 'left' != 'right'\n"
                "Ran 2 tests in 0.014s\n\nFAILED (failures=1)\n"
            )
            self.assertEqual(
                sig_fn("verification_failed", 1, out_a1),
                sig_fn("verification_failed", 1, out_a2),
            )
            self.assertNotEqual(
                sig_fn("verification_failed", 1, out_a1),
                sig_fn("verification_failed", 1, out_b),
            )

            # E. Caller verify_env_path passthrough resolves custom tool (S6)
            custom_bin = tmp_p / "custom-bin"
            custom_bin.mkdir()
            tool = custom_bin / "custom_verify_ok_tool"
            tool.write_text("#!/bin/sh\necho 'Ran 3 tests in 0.01s'\nexit 0\n", encoding="utf-8")
            tool.chmod(0o755)
            rc_path, _ = _run_batch(
                404,
                {
                    "verify_command": "custom_verify_ok_tool",
                    "verify_env_path": f"{custom_bin}:{os.environ.get('PATH', '')}",
                },
            )
            self.assertEqual(rc_path["verdict"], "PASS")
            self.assertTrue(rc_path["cli_launched"])

    def test_zero_test_execution_veto_positive_exemption_and_pytest_exit5(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_p = Path(tmp)
            repo = tmp_p / "repo"
            _init_repo(repo)
            (repo / "app.py").write_text("x = 3\n", encoding="utf-8")

            fake_agy = tmp_p / "fake-agy.py"
            fake_agy.write_text(
                "#!/usr/bin/env python3\n"
                "import json\n"
                "print(json.dumps({'event': 'init', 'conversation_id': 'conv-z-1'}), flush=True)\n"
                "print(json.dumps({'event': 'result', 'result': {'conversation_id': 'conv-z-1', 'status': 'SUCCESS', 'response': 'AUTOLOOP_VERDICT: PASS\\n0 阻塞发现'}}), flush=True)\n",
                encoding="utf-8",
            )
            fake_agy.chmod(0o755)

            def _exec_verify(run_no: int, cmd_str: str) -> dict:
                ev_dir = tmp_p / f"ev-{run_no}"
                b_file = tmp_p / f"b-{run_no}.json"
                b_file.write_text(
                    json.dumps(
                        {
                            "batch_id": f"b-{run_no}",
                            "mode": "pi-accept",
                            "reviewer_driver": "agy",
                            "review_profile": "fast",
                            "allow_rerun": False,
                            "expected_resume": None,
                            "verify_cwd": str(repo),
                            "verify_command": cmd_str,
                            "capture_git_diff": True,
                            "ledger_dir": str(tmp_p / f"ledger-{run_no}"),
                            "evidence_dir": str(ev_dir),
                            "stop_cmd": ["true"],
                            "pi_cmd": [sys.executable, str(fake_agy)],
                            "pi_prompt": "check {RAW} {CWD}",
                        }
                    ),
                    encoding="utf-8",
                )
                f_dir = tmp_p / f"{run_no}-1"
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
                        f"s-{run_no}",
                        "--resume",
                        "",
                        "--cwd",
                        str(repo),
                    ],
                    env={**os.environ, "AGENT_AUTOLOOP_RUN": str(run_no)},
                    capture_output=True,
                    text=True,
                    check=True,
                )
                return json.loads((ev_dir / f"run-{run_no}/receipt.json").read_text(encoding="utf-8"))

            # 1. Single-suite zero tests with exit 0 -> vetoed before CLI
            r_zero = _exec_verify(501, "printf 'Ran 0 tests in 0.000s\\n\\nOK\\n'")
            self.assertEqual(r_zero["verdict"], "FAIL")
            self.assertFalse(r_zero["cli_launched"])
            self.assertEqual(r_zero["failure_kind"], "empty_test_execution")

            # 2. Multi-module output with 0 tests in module A and 4 tests in module B -> exempted
            r_multi = _exec_verify(502, "printf 'Tests run: 0, Failures: 0\\nTests run: 4, Failures: 0\\n'")
            self.assertEqual(r_multi["verdict"], "PASS")
            self.assertTrue(r_multi["cli_launched"])

            # 3. Pytest exit 5 collected 0 items -> empty_test_execution
            r_py0 = _exec_verify(503, "sh -c 'echo \"collected 0 items\"; exit 5'")
            self.assertEqual(r_py0["verdict"], "FAIL")
            self.assertFalse(r_py0["cli_launched"])
            self.assertEqual(r_py0["failure_kind"], "empty_test_execution")

            # 4. Pytest exit 5 all deselected (-k mismatch, R8) -> empty_test_execution
            r_desel = _exec_verify(504, "sh -c 'echo \"=== 5 deselected in 0.02s ===\"; exit 5'")
            self.assertEqual(r_desel["verdict"], "FAIL")
            self.assertFalse(r_desel["cli_launched"])
            self.assertEqual(r_desel["failure_kind"], "empty_test_execution")

    def test_fast_high_risk_path_escalation_from_changed_files_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_p = Path(tmp)
            fake_agy = tmp_p / "fake-agy.py"
            fake_agy.write_text(
                "#!/usr/bin/env python3\n"
                "import json\n"
                "print(json.dumps({'event': 'init', 'conversation_id': 'conv-esc-1'}), flush=True)\n"
                "print(json.dumps({'event': 'result', 'result': {'conversation_id': 'conv-esc-1', 'status': 'SUCCESS', 'response': 'AUTOLOOP_VERDICT: PASS\\n0 阻塞发现\\nhunt: n/a'}}), flush=True)\n",
                encoding="utf-8",
            )
            fake_agy.chmod(0o755)

            # Repo 1: Clean committed feature branch touching SQL migration + auth/security stems without --base-ref
            repo_risk = tmp_p / "repo-risk"
            base_branch = _init_repo(repo_risk)
            subprocess.run(["git", "-C", str(repo_risk), "checkout", "-qb", "feat/risk", base_branch], check=True)
            (repo_risk / "db/migration").mkdir(parents=True)
            (repo_risk / "src").mkdir(parents=True)
            (repo_risk / "db/migration/V1__init.sql").write_text("CREATE TABLE t(id INT);\n", encoding="utf-8")
            (repo_risk / "src/auth.py").write_text("def check(): return True\n", encoding="utf-8")
            (repo_risk / "src/SecurityConfig.java").write_text("class SecurityConfig {}\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo_risk), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo_risk), "commit", "-qm", "feat: add migration and auth"], check=True)

            ev_risk = tmp_p / "ev-risk"
            b_risk = tmp_p / "b-risk.json"
            hunt_ref = ROOT / "references/autoloop-review-hunt.md"
            b_risk.write_text(
                json.dumps(
                    {
                        "batch_id": "b-risk",
                        "mode": "pi-accept",
                        "reviewer_driver": "agy",
                        "extra_read_dirs": [],
                        "review_profile": "fast",
                        "base_ref": "",
                        "model_explicit": False,
                        "hunt_ref": str(hunt_ref.resolve()),
                        "hunt_dir": str(hunt_ref.parent.resolve()),
                        "allow_rerun": False,
                        "expected_resume": None,
                        "verify_cwd": str(repo_risk),
                        "verify_command": "printf 'Ran 2 tests in 0.01s\\n'",
                        "capture_git_diff": True,
                        "ledger_dir": str(tmp_p / "ledger-risk"),
                        "evidence_dir": str(ev_risk),
                        "stop_cmd": ["true"],
                        "pi_cmd": [
                            sys.executable,
                            str(fake_agy),
                            "--model",
                            "gemini-4-carbon-medium",
                            "--output-format",
                            "stream-json",
                        ],
                        "pi_prompt": "fast base prompt {RAW} {CWD}",
                    }
                ),
                encoding="utf-8",
            )
            f_risk = tmp_p / "601-1"
            f_risk.mkdir()
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/gov_runner.py"),
                    "--batch",
                    str(b_risk),
                    "--folder",
                    str(f_risk),
                    "--session",
                    "s-601",
                    "--resume",
                    "",
                    "--cwd",
                    str(repo_risk),
                ],
                env={**os.environ, "AGENT_AUTOLOOP_RUN": "601"},
                capture_output=True,
                text=True,
                check=True,
            )
            rc_risk = json.loads((ev_risk / "run-601/receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(rc_risk["verdict"], "PASS")
            self.assertEqual(
                rc_risk["risk_escalated_paths"],
                ["db/migration/V1__init.sql", "src/SecurityConfig.java", "src/auth.py"],
            )
            argv_risk = json.loads((ev_risk / "run-601/attempt-1/cli.argv.json").read_text(encoding="utf-8"))
            self.assertIn("gemini-4-carbon-high", argv_risk)
            self.assertNotIn("gemini-4-carbon-medium", argv_risk)
            self.assertIn(str(hunt_ref.parent.resolve()), argv_risk)
            self.assertIn("补充材料（高敏业务路径自动升档核查）", argv_risk[-1])

            # Repo 2: Docs and test seed SQL only -> must NOT escalate
            repo_safe = tmp_p / "repo-safe"
            base_safe = _init_repo(repo_safe)
            subprocess.run(["git", "-C", str(repo_safe), "checkout", "-qb", "feat/safe", base_safe], check=True)
            (repo_safe / "docs").mkdir(parents=True)
            (repo_safe / "src/test/resources").mkdir(parents=True)
            (repo_safe / "docs/note.md").write_text("# Doc\n", encoding="utf-8")
            (repo_safe / "src/test/resources/seed.sql").write_text("SELECT 1;\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo_safe), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo_safe), "commit", "-qm", "docs: add note and test seed"], check=True)

            ev_safe = tmp_p / "ev-safe"
            b_safe = tmp_p / "b-safe.json"
            b_safe.write_text(
                json.dumps(
                    {
                        **json.loads(b_risk.read_text(encoding="utf-8")),
                        "batch_id": "b-safe",
                        "verify_cwd": str(repo_safe),
                        "ledger_dir": str(tmp_p / "ledger-safe"),
                        "evidence_dir": str(ev_safe),
                    }
                ),
                encoding="utf-8",
            )
            f_safe = tmp_p / "602-1"
            f_safe.mkdir()
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/gov_runner.py"),
                    "--batch",
                    str(b_safe),
                    "--folder",
                    str(f_safe),
                    "--session",
                    "s-602",
                    "--resume",
                    "",
                    "--cwd",
                    str(repo_safe),
                ],
                env={**os.environ, "AGENT_AUTOLOOP_RUN": "602"},
                capture_output=True,
                text=True,
                check=True,
            )
            rc_safe = json.loads((ev_safe / "run-602/receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(rc_safe["verdict"], "PASS")
            self.assertEqual(rc_safe["risk_escalated_paths"], [])
            argv_safe = json.loads((ev_safe / "run-602/attempt-1/cli.argv.json").read_text(encoding="utf-8"))
            self.assertIn("gemini-4-carbon-medium", argv_safe)
            self.assertNotIn("补充材料（高敏业务路径自动升档核查）", argv_safe[-1])

    def test_redaction_signature_verdict_and_subprocess_hardening(self) -> None:
        runner = _load_module("gov_runner_harden", ROOT / "scripts/gov_runner.py")

        # F1: Compound key prefixes, Basic/Token auth, password-only URLs, raw tokens, and full/truncated PEM keys must be masked
        pem_begin = "-----BEGIN RSA " + "PRIVATE KEY-----"
        pem_end = "-----END RSA " + "PRIVATE KEY-----"
        fake_sk = "sk" + "-proj1234567890abcdefghij"
        raw_secret = (
            '{"access_token": "at_secret_99", "client_secret": "cs_secret_88"} '
            f"DB_PASSWORD=db_pass_77 OPENAI_API_KEY={fake_sk} "
            "Authorization: Basic dXNlcjpwYXNz "
            "redis://:redis_pwd@127.0.0.1:6379/0 "
            "raw=" + "glpat" + "-abcdefghij123456 "
            "https://example.com:8443?email=ops@example.com\n"
            f"{pem_begin}\nProc-Type: 4,ENCRYPTED\nMIIEpAIBAAKCAQEAfullbody1234567890==\n{pem_end}\n"
            f"{pem_begin}\nMIIEpAIBAAKCAQEAtruncbody9876543210==\nRuntimeError: after key"
        )
        masked = runner._redact_sensitive_text(raw_secret, limit=2000)
        for leak in (
            "at_secret_99",
            "cs_secret_88",
            "db_pass_77",
            fake_sk,
            "dXNlcjpwYXNz",
            "redis_pwd",
            "abcdefghij123456",
            "fullbody1234567890",
            "truncbody9876543210",
            "Proc-Type: 4,ENCRYPTED",
        ):
            self.assertNotIn(leak, masked, masked)
        self.assertIn("ops@example.com", masked)
        self.assertIn("RuntimeError: after key", masked)

        # F2: Distinct review_rejected findings must not collapse; Maven spaced durations must normalize;
        # ERROR: header must not mask distinct exception types
        rej_a = "AUTOLOOP_VERDICT: FAIL\n- src/foo.py:12 空指针风险\n"
        rej_b = "AUTOLOOP_VERDICT: FAIL\n- src/bar.py:88 SQL 注入风险\n"
        self.assertNotEqual(
            runner._compute_failure_signature("review_rejected", 0, rej_a),
            runner._compute_failure_signature("review_rejected", 0, rej_b),
        )
        mvn_1 = (
            "[ERROR] Tests run: 5, Failures: 1, Errors: 0, Skipped: 0, Time elapsed: 0.421 s <<< FAILURE! - in com.demo.FooTest\n"
            "[ERROR]   FooTest.testBar:42 expected: <1> but was: <2>\n"
        )
        mvn_2 = (
            "[ERROR] Tests run: 5, Failures: 1, Errors: 0, Skipped: 0, Time elapsed: 1.987 s <<< FAILURE! - in com.demo.FooTest\n"
            "[ERROR]   FooTest.testBar:42 expected: <1> but was: <2>\n"
        )
        self.assertEqual(
            runner._compute_failure_signature("verification_failed", 1, mvn_1),
            runner._compute_failure_signature("verification_failed", 1, mvn_2),
        )
        err_val = "ERROR: test_x (tests.T)\nTraceback:\nValueError: bad value\nFAILED (errors=1)\n"
        err_typ = "ERROR: test_x (tests.T)\nTraceback:\nTypeError: wrong type\nFAILED (errors=1)\n"
        self.assertNotEqual(
            runner._compute_failure_signature("verification_failed", 1, err_val),
            runner._compute_failure_signature("verification_failed", 1, err_typ),
        )
        generic_err_a = "ERROR: failed to connect to db\nexit status 1\n"
        generic_err_b = "ERROR: failed to parse config\nexit status 1\n"
        self.assertNotEqual(
            runner._compute_failure_signature("verification_failed", 1, generic_err_a),
            runner._compute_failure_signature("verification_failed", 1, generic_err_b),
        )

        # F3: Verdict PASS must be exact-line anchored (reject FAIL mentioning PASS) and accept plain '模型：' header
        self.assertFalse(runner._is_pass_verdict_line("AUTOLOOP_VERDICT: FAIL（未满足 AUTOLOOP_VERDICT: PASS）"))
        self.assertTrue(runner._is_pass_verdict_line("AUTOLOOP_VERDICT: PASS"))
        self.assertTrue(runner._is_pass_verdict_line("`AUTOLOOP_VERDICT: PASS`"))
        self.assertEqual(
            runner._extract_verdict_line("模型：Gemini 4 Carbon\nAUTOLOOP_VERDICT: PASS\n0 阻塞发现"),
            "AUTOLOOP_VERDICT: PASS",
        )

        # F4: AssertionError containing 'command not found' must stay verification_failed, while shell error stays setup_or_env_error
        self.assertEqual(
            runner._classify_verify_failure(1, False, "AssertionError: 'command not found' not in out"),
            "verification_failed",
        )
        self.assertEqual(
            runner._classify_verify_failure(1, False, "zsh:1: command not found: nonexistent_tool"),
            "setup_or_env_error",
        )

        # F4 (list argv missing binary + malformed JSON line tolerance) & F5 (rename away from high-risk path)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_p = Path(tmp)
            repo = tmp_p / "repo"
            base_branch = _init_repo(repo)
            _git(repo, "checkout", "-qb", "feat/harden", base_branch)
            (repo / "src/auth").mkdir(parents=True)
            (repo / "src/auth/guard.py").write_text("def ok(): return True\n", encoding="utf-8")
            _git(repo, "add", ".")
            _git(repo, "commit", "-qm", "feat(auth): add guard\n\n- add auth guard")

            # Rename away from src/auth/guard.py -> src/util/helper.py must still trigger high-risk escalation
            _git(repo, "checkout", "-qb", "feat/rename-auth")
            (repo / "src/util").mkdir(parents=True)
            _git(repo, "mv", "src/auth/guard.py", "src/util/helper.py")
            _git(repo, "commit", "-qm", "refactor(util): move guard\n\n- move auth file to util")
            raw_rn = tmp_p / "raw-rn"
            raw_rn.mkdir()
            runner.capture_git_snapshot(str(repo), raw_rn, base_ref="feat/harden", review_profile="fast")
            self.assertIn(
                "src/auth/guard.py",
                runner._detect_escalated_paths_from_changed_file(raw_rn / "git.changed_files.txt"),
            )

            # Missing binary passed as list verify_command must settle cleanly as setup_or_env_error (no crash)
            ev_missing = tmp_p / "ev-missing"
            b_missing = tmp_p / "b-missing.json"
            b_missing.write_text(
                json.dumps(
                    {
                        "batch_id": "b-list-missing",
                        "mode": "pi-accept",
                        "reviewer_driver": "agy",
                        "review_profile": "fast",
                        "base_ref": "feat/harden",
                        "allow_rerun": False,
                        "expected_resume": None,
                        "verify_cwd": str(repo),
                        "verify_command": ["nonexistent_bin_list_xyz_99", "--check"],
                        "capture_git_diff": True,
                        "ledger_dir": str(tmp_p / "ledger-m"),
                        "evidence_dir": str(ev_missing),
                        "stop_cmd": ["true"],
                        "pi_cmd": ["true"],
                        "pi_prompt": "check {RAW} {CWD}",
                    }
                ),
                encoding="utf-8",
            )
            f_missing = tmp_p / "701-1"
            f_missing.mkdir()
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/gov_runner.py"),
                    "--batch",
                    str(b_missing),
                    "--folder",
                    str(f_missing),
                    "--session",
                    "s-701",
                    "--resume",
                    "",
                    "--cwd",
                    str(repo),
                ],
                env={**os.environ, "AGENT_AUTOLOOP_RUN": "701"},
                capture_output=True,
                text=True,
                check=True,
            )
            rc_m = json.loads((ev_missing / "run-701/receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(rc_m["verdict"], "FAIL")
            self.assertEqual(rc_m["verify_exit_code"], 127)
            self.assertEqual(rc_m["failure_kind"], "setup_or_env_error")
            self.assertFalse(rc_m["cli_launched"])

            # Reviewer CLI emitting a non-JSON '{noise' line before valid stream-json result must not crash
            noisy_agy = tmp_p / "noisy-agy.py"
            noisy_agy.write_text(
                "#!/usr/bin/env python3\n"
                "import json\n"
                "print('{not-valid-json startup noise', flush=True)\n"
                "print(json.dumps({'event': 'init', 'conversation_id': 'conv-noisy-1'}), flush=True)\n"
                "print(json.dumps({'event': 'result', 'result': {'conversation_id': 'conv-noisy-1', 'status': 'SUCCESS', 'response': 'AUTOLOOP_VERDICT: PASS\\n0 阻塞发现'}}), flush=True)\n",
                encoding="utf-8",
            )
            noisy_agy.chmod(0o755)
            ev_noisy = tmp_p / "ev-noisy"
            b_noisy = tmp_p / "b-noisy.json"
            b_noisy.write_text(
                json.dumps(
                    {
                        "batch_id": "b-noisy",
                        "mode": "pi-accept",
                        "reviewer_driver": "agy",
                        "review_profile": "fast",
                        "base_ref": "feat/harden",
                        "allow_rerun": False,
                        "expected_resume": None,
                        "verify_cwd": str(repo),
                        "verify_command": "printf 'Ran 1 test in 0.01s\\n'",
                        "capture_git_diff": True,
                        "ledger_dir": str(tmp_p / "ledger-n"),
                        "evidence_dir": str(ev_noisy),
                        "stop_cmd": ["true"],
                        "pi_cmd": [sys.executable, str(noisy_agy)],
                        "pi_prompt": "check {RAW} {CWD}",
                    }
                ),
                encoding="utf-8",
            )
            f_noisy = tmp_p / "702-1"
            f_noisy.mkdir()
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/gov_runner.py"),
                    "--batch",
                    str(b_noisy),
                    "--folder",
                    str(f_noisy),
                    "--session",
                    "s-702",
                    "--resume",
                    "",
                    "--cwd",
                    str(repo),
                ],
                env={**os.environ, "AGENT_AUTOLOOP_RUN": "702"},
                capture_output=True,
                text=True,
                check=True,
            )
            rc_n = json.loads((ev_noisy / "run-702/receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(rc_n["verdict"], "PASS")
            self.assertEqual(rc_n["native_session"], "conv-noisy-1")

    def test_autoloop_ctl_merge_commit_req_hygiene_and_cold_path_partition(self) -> None:
        ctl = _load_module("autoloop_ctl_harden", ROOT / "scripts/autoloop_ctl.py")
        checker = _load_module("check_commit_text_harden", ROOT / "scripts/check_commit_text.py")

        # F5.1: OPENSPEC_TEST_CMD_RE must reject shell metacharacters and embedded newlines in commands
        self.assertIsNotNone(ctl.OPENSPEC_TEST_CMD_RE.match("mvn -Dtest=DemoTest test"))
        for bad_mvn in (
            "mvn test; rm -rf /",
            "mvn -Darg=$(whoami) test",
            "mvn test | tee out.log",
            "mvn test\nrm -rf /",
        ):
            self.assertIsNone(ctl.OPENSPEC_TEST_CMD_RE.match(bad_mvn), bad_mvn)

        # F5.2: match_project_req skips README.md / archived reqs, parses CRLF frontmatter,
        # and mark_req_passed updates trailing-\n--- frontmatter in place without duplicating blocks
        with tempfile.TemporaryDirectory() as tmp:
            tmp_p = Path(tmp)
            proj = tmp_p / "proj"
            req_dir = proj / "docs/req"
            req_dir.mkdir(parents=True)
            (req_dir / "2026-11-18-old.md").write_text(
                "---\r\nreq_id: old\r\nstatus: archived\r\nverify_cmd: \"true\"\r\n---\r\n# Old\r\n",
                encoding="utf-8",
            )
            (req_dir / "2026-11-19-real.md").write_bytes(
                b"---\r\nreq_id: real\r\nstatus: ready\r\nverify_cmd: \"python3 -m unittest\"\r\n---\r\n\r\n## \xe9\xaa\x8c\xe6\x94\xb6\xe6\xa0\x87\xe5\x87\x86\r\n- ok\r\n"
            )
            readme = req_dir / "README.md"
            readme.write_text("# Docs Req Index\n", encoding="utf-8")
            os.utime(readme, (readme.stat().st_atime + 60, readme.stat().st_mtime + 60))

            orig_index = ctl.INDEX_FILE
            try:
                ctl.INDEX_FILE = tmp_p / "state/project-index.json"
                matched = ctl.match_project_req(proj)
                self.assertTrue(matched["matched"])
                self.assertEqual(matched["req_id"], "real")
                self.assertEqual(matched["verify_cmd"], "python3 -m unittest")
            finally:
                ctl.INDEX_FILE = orig_index

            tail_only = req_dir / "2026-11-19-tail-only.md"
            tail_only.write_bytes(b"---\r\nreq_id: tail\r\nstatus: ready\r\nverify_cmd: \"true\"\r\n---")
            self.assertEqual(ctl.parse_req_markdown(tail_only)["verify_cmd"], "true")
            ctl.mark_req_passed(tail_only)
            rewritten = tail_only.read_text(encoding="utf-8")
            self.assertEqual(rewritten.count("---\n"), 2, rewritten)
            self.assertEqual(ctl.parse_req_markdown(tail_only)["status"], "passed")
            self.assertEqual(ctl.parse_req_markdown(tail_only)["verify_cmd"], "true")

            # Policy check after merge commit still enforces profile_cfg on the first non-merge commit
            policy = tmp_p / "merge-policy.json"
            policy.write_text(json.dumps({"profiles": {"initial": {"min_body_chars": 80}}}), encoding="utf-8")
            res_merge_policy = checker.validate_commit_text(
                commit_text=None,
                git_log_text=(
                    "commit 1111111111111111111111111111111111111111\n"
                    "Merge: aaaaaaa bbbbbbb\n"
                    "Author: dev <dev@example.com>\n"
                    "Commit: dev <dev@example.com>\n\n"
                    "    Merge branch 'main' into feat/demo\n\n"
                    "commit 2222222222222222222222222222222222222222\n"
                    "Author: dev <dev@example.com>\n"
                    "Commit: dev <dev@example.com>\n\n"
                    "    feat(demo): add real feature\n\n"
                    "    - too short\n"
                ),
                policy_path=policy,
                profile="initial",
            )
            self.assertFalse(res_merge_policy["ok"])
            self.assertTrue(any("min_body_chars" in e for e in res_merge_policy["errors"]))

        # F5.3: Standard git merge commits in git.log.txt bypass Conventional Commit format while preserving secret checks
        merge_log_ok = (
            "commit 1111111111111111111111111111111111111111\n"
            "Merge: aaaaaaa bbbbbbb\n"
            "Author: dev <dev@example.com>\n"
            "Commit: dev <dev@example.com>\n\n"
            "    Merge branch 'main' into feat/demo\n\n"
            "commit 2222222222222222222222222222222222222222\n"
            "Author: dev <dev@example.com>\n"
            "Commit: dev <dev@example.com>\n\n"
            "    feat(demo): add real feature\n\n"
            "    - keep merge history clean\n"
        )
        res_merge_ok = checker.validate_commit_text(commit_text=None, git_log_text=merge_log_ok)
        self.assertTrue(res_merge_ok["ok"], res_merge_ok)

        merge_log_secret = (
            "commit 1111111111111111111111111111111111111111\n"
            "Merge: aaaaaaa bbbbbbb\n"
            "Author: dev <dev@example.com>\n"
            "Commit: dev <dev@example.com>\n\n"
            "    Merge branch 'main' with token " + "glpat" + "-1234567890abcdef\n\n"
            "commit 2222222222222222222222222222222222222222\n"
            "Author: dev <dev@example.com>\n"
            "Commit: dev <dev@example.com>\n\n"
            "    feat(demo): add real feature\n\n"
            "    - keep merge history clean\n"
        )
        res_merge_sec = checker.validate_commit_text(commit_text=None, git_log_text=merge_log_secret)
        self.assertFalse(res_merge_sec["ok"])

        # F6: COLD_PATH_START must partition only cold recovery tail, never hot execution trunk sections
        approved_text = (ROOT / "references/approved-implementation-workflow.md").read_text(encoding="utf-8")
        cold_pos = approved_text.index("<!-- COLD_PATH_START")
        resume_pos = approved_text.index("## Project Session Resume")
        for hot_heading in (
            "## Conditional Minimal Implementation",
            "## Review/Fix Convergence",
            "## Inline Implementation",
            "## External Implementation",
            "## Final Completion",
            "## OpenSpec closeout",
            "## Tiered Authorization And High Review",
        ):
            self.assertLess(approved_text.index(hot_heading), cold_pos, f"{hot_heading} must precede COLD_PATH_START")
        self.assertLess(cold_pos, resume_pos)


if __name__ == "__main__":
    unittest.main()
