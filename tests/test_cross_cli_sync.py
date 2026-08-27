from __future__ import annotations

import json
import hashlib
import errno
import io
import inspect
import os
import stat
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from scripts import validate_cross_cli_sync as sync


SKILLS = ["openspec-superpower-change", "codex-brief-antigravity-review"]
INVARIANTS = [f"CCG-{number:03d}" for number in range(1, 9)]
V6_INVARIANTS = [f"CCG-{number:03d}" for number in range(1, 17)]

V6_SEMANTIC_BODIES = {
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


def required_target(target_id: str, result: str = "pass") -> dict:
    return {
        "id": target_id,
        "selection": "required",
        "result": result,
        "decision_owner": "codex",
        "evidence": f"evidence/{target_id}.json",
        "reason": "selected collaboration runtime",
        "resume_condition": "rerun parity and discovery checks",
    }


def portable_manifest() -> dict:
    return {
        "schema_version": 1,
        "skills": [
            {
                "name": SKILLS[0],
                "source_alias": "openspec",
                "files": [
                    {"path": "SKILL.md", "targets": ["codex", "antigravity-cli", "grok-cli"]},
                    {
                        "path": "references/cross-cli-sync.md",
                        "targets": ["codex", "antigravity-cli", "grok-cli"],
                    },
                    {
                        "path": "scripts/validate_core_gates.py",
                        "targets": ["codex", "antigravity-cli", "grok-cli"],
                    },
                ],
            },
            {
                "name": SKILLS[1],
                "source_alias": "brief",
                "files": [
                    {"path": "SKILL.md", "targets": ["codex", "antigravity-cli", "grok-cli"]}
                ],
            },
        ],
        "managed_rules": {
            "version": 1,
            "source": "references/shared-global-governance.md",
            "invariant_ids": INVARIANTS,
        },
        "targets": [
            required_target("codex"),
            required_target("antigravity-cli"),
            required_target("grok-cli"),
        ],
    }


def portable_manifest_v6() -> dict:
    manifest = portable_manifest()
    target_order = ["codex", "pi", "antigravity-cli", "grok-cli"]
    for skill in manifest["skills"]:
        for item in skill["files"]:
            item["targets"] = list(target_order)
    manifest["managed_rules"] = {
        "version": 6,
        "source": "references/shared-global-governance.md",
        "invariant_ids": list(V6_INVARIANTS),
    }
    manifest["targets"] = [
        required_target(target_id, "pending") for target_id in target_order
    ]
    return manifest


def create_v6_sync_fixture(root: Path) -> dict:
    openspec = root / "openspec"
    brief = root / "brief"
    openspec.mkdir()
    brief.mkdir()
    for relative in (
        "SKILL.md",
        "references/cross-cli-sync.md",
        "scripts/validate_core_gates.py",
    ):
        path = openspec / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"portable {relative}\n", encoding="utf-8")
    (brief / "SKILL.md").write_text("portable brief\n", encoding="utf-8")
    managed = openspec / "references" / "shared-global-governance.md"
    managed.write_text(
        (
            Path(__file__).parents[1]
            / "references"
            / "shared-global-governance.md"
        ).read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    manifest_path = root / "manifest.json"
    manifest_path.write_text(json.dumps(portable_manifest_v6()), encoding="utf-8")
    target_values = {}
    for target_id, prefix in (
        ("codex", "codex"),
        ("pi", "pi"),
        ("antigravity-cli", "antigravity"),
        ("grok-cli", "grok"),
    ):
        runtime = root / target_id
        skills = runtime / "skills"
        skills.mkdir(parents=True)
        rule_name = {
            "codex": "AGENTS.md",
            "pi": "APPEND_SYSTEM.md",
            "antigravity-cli": None,
            "grok-cli": "AGENTS.md",
        }[target_id]
        rule = (
            root / "GEMINI.md"
            if target_id == "antigravity-cli"
            else runtime / rule_name
        )
        rule.write_text(f"native-{target_id}\n", encoding="utf-8")
        target_values[f"{prefix}_skills_root"] = skills
        target_values[f"{prefix}_rule_file"] = rule
    args = SimpleNamespace(
        manifest=manifest_path,
        openspec_source=openspec,
        brief_source=brief,
        **target_values,
    )
    plan = sync.generate_plan(args)
    plan_path = root / "sync-plan.json"
    plan_path.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    plan_path.chmod(0o600)
    transaction_root = root / "transactions"
    transaction_root.mkdir(mode=0o700)
    return {
        "plan": plan,
        "plan_path": plan_path,
        "plan_sha256": sync._sha256(plan_path),
        "backup_root": root / "backups",
        "transaction_root": transaction_root,
    }


def _scoped_args(fixture: dict, selected_files, *, select_managed_rule=False):
    root = fixture["plan_path"].parent
    return SimpleNamespace(
        manifest=root / "manifest.json",
        openspec_source=root / "openspec",
        brief_source=root / "brief",
        codex_skills_root=root / "codex" / "skills",
        codex_rule_file=root / "codex" / "AGENTS.md",
        pi_skills_root=root / "pi" / "skills",
        pi_rule_file=root / "pi" / "APPEND_SYSTEM.md",
        antigravity_skills_root=root / "antigravity-cli" / "skills",
        antigravity_rule_file=root / "GEMINI.md",
        grok_skills_root=root / "grok-cli" / "skills",
        grok_rule_file=root / "grok-cli" / "AGENTS.md",
        select_file=list(selected_files),
        select_managed_rule=select_managed_rule,
    )


def create_scoped_v6_sync_fixture(root: Path, selected_files) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    fixture = create_v6_sync_fixture(root)
    selected = set(selected_files)
    manifest = portable_manifest_v6()
    source_roots = {"openspec": root / "openspec", "brief": root / "brief"}
    managed_source = source_roots["openspec"] / "references" / "shared-global-governance.md"
    managed_text = managed_source.read_text(encoding="utf-8")
    for target_id in sync.TARGET_ORDER:
        target = fixture["plan"]["targets"][target_id]
        rule = Path(target["rule_file"])
        rule.write_text(
            sync.install_managed_block(
                f"native-{target_id}\n", managed_text, version=6
            ),
            encoding="utf-8",
        )
        skills_root = Path(target["skills_root"])
        for skill in manifest["skills"]:
            source_root = source_roots[skill["source_alias"]]
            for item in skill["files"]:
                key = f"{skill['name']}:{item['path']}"
                if key in selected:
                    continue
                source = source_root / item["path"]
                destination = skills_root / skill["name"] / item["path"]
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(source.read_bytes())
    return fixture


def write_plan_file(fixture: dict, plan: dict) -> Path:
    path = fixture["plan_path"].parent / "scoped-plan.json"
    path.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    path.chmod(0o600)
    return path


def _legacy_plan_to_v2(plan: dict, selected_files, *, select_managed_rule=False) -> dict:
    selected = {
        tuple(value.split(":", 1)) if isinstance(value, str) else tuple(value)
        for value in selected_files
    }
    ordered = [
        {"skill": item["skill"], "path": item["path"]}
        for item in plan["targets"]["codex"]["files"]
        if (item["skill"], item["path"]) in selected
    ]
    targets = {}
    for target_id, target in plan["targets"].items():
        state = {
            key: value
            for key, value in target.items()
            if key not in {"skills_root", "rule_file", "rule_pre_state", "files"}
        }
        files = [
            dict(item)
            for item in target["files"]
            if (item["skill"], item["path"]) in selected
        ]
        assertions = [
            dict(item)
            for item in target["files"]
            if (item["skill"], item["path"]) not in selected
        ]
        targets[target_id] = {
            **state,
            "skills_root": target["skills_root"],
            "files": files,
            "assertions": assertions,
            "managed_rule": {
                "selected": select_managed_rule,
                "destination": target["rule_file"],
                "pre_state": target["rule_pre_state"],
            },
        }
    return {
        "schema_version": 2,
        "manifest_path": plan["manifest_path"],
        "manifest_sha256": plan["manifest_sha256"],
        "sources": dict(plan["sources"]),
        "selection": {
            "files": ordered,
            "managed_rule": select_managed_rule,
        },
        "managed_rules": dict(plan["managed_rules"]),
        "targets": targets,
    }


def make_scoped_plan(fixture: dict, selected_files, *, select_managed_rule=False) -> dict:
    plan = sync.generate_plan(
        _scoped_args(
            fixture,
            selected_files,
            select_managed_rule=select_managed_rule,
        )
    )
    if plan.get("schema_version") == 1:
        plan = _legacy_plan_to_v2(
            plan,
            selected_files,
            select_managed_rule=select_managed_rule,
        )
    return plan


def scoped_plan_cli_command(fixture: dict, output: Path, selectors, *, managed_rule=False):
    root = fixture["plan_path"].parent
    command = [
        sys.executable,
        str(Path(sync.__file__)),
        "plan",
        "--manifest",
        str(root / "manifest.json"),
        "--openspec-source",
        str(root / "openspec"),
        "--brief-source",
        str(root / "brief"),
        "--codex-skills-root",
        str(root / "codex" / "skills"),
        "--codex-rule-file",
        str(root / "codex" / "AGENTS.md"),
        "--pi-skills-root",
        str(root / "pi" / "skills"),
        "--pi-rule-file",
        str(root / "pi" / "APPEND_SYSTEM.md"),
        "--antigravity-skills-root",
        str(root / "antigravity-cli" / "skills"),
        "--antigravity-rule-file",
        str(root / "GEMINI.md"),
        "--grok-skills-root",
        str(root / "grok-cli" / "skills"),
        "--grok-rule-file",
        str(root / "grok-cli" / "AGENTS.md"),
    ]
    for selector in selectors:
        command.extend(["--select-file", selector])
    if managed_rule:
        command.append("--select-managed-rule")
    command.extend(["--output", str(output)])
    return command


class ManifestAndTriggerTests(unittest.TestCase):
    def test_portable_manifest_accepts_only_declared_schema(self):
        self.assertEqual(sync.validate_manifest(portable_manifest()), portable_manifest())

    def test_manifest_accepts_version_2_tiered_governance_invariants(self):
        manifest = portable_manifest()
        manifest["managed_rules"]["version"] = 2
        manifest["managed_rules"]["invariant_ids"] = [
            f"CCG-{number:03d}" for number in range(1, 14)
        ]
        self.assertEqual(sync.validate_manifest(manifest), manifest)

    def test_manifest_accepts_version_3_adaptive_routing_invariants(self):
        manifest = portable_manifest()
        manifest["managed_rules"]["version"] = 3
        manifest["managed_rules"]["invariant_ids"] = [
            f"CCG-{number:03d}" for number in range(1, 15)
        ]
        self.assertEqual(sync.validate_manifest(manifest), manifest)

    def test_manifest_accepts_version_4_project_learning_invariants(self):
        manifest = portable_manifest()
        manifest["managed_rules"]["version"] = 4
        manifest["managed_rules"]["invariant_ids"] = [
            f"CCG-{number:03d}" for number in range(1, 16)
        ]
        try:
            validated = sync.validate_manifest(manifest)
        except ValueError as exc:
            self.fail(f"managed-rule version 4 should be supported: {exc}")
        self.assertEqual(validated, manifest)

    def test_manifest_accepts_version_5_explicit_method_authority(self):
        manifest = portable_manifest()
        manifest["managed_rules"]["version"] = 5
        manifest["managed_rules"]["invariant_ids"] = [
            f"CCG-{number:03d}" for number in range(1, 16)
        ]
        try:
            validated = sync.validate_manifest(manifest)
        except ValueError as exc:
            self.fail(f"managed-rule version 5 should be supported: {exc}")
        self.assertEqual(validated, manifest)

    def test_project_learning_files_are_portable_to_every_required_runtime(self):
        manifest = json.loads(
            (Path(__file__).parents[1] / "references" / "cross-cli-portable-manifest.json")
            .read_text(encoding="utf-8")
        )
        router_files = {
            item["path"]: set(item["targets"])
            for skill in manifest["skills"]
            if skill["name"] == "openspec-superpower-change"
            for item in skill["files"]
        }
        expected_targets = {"codex", "pi", "antigravity-cli", "grok-cli"}
        for relative in (
            "references/local-instruction-checkpoint.md",
            "references/project-learning-closeout.md",
            "templates/learning-candidate-template.md",
        ):
            with self.subTest(relative=relative):
                self.assertIn(relative, router_files)
                self.assertEqual(router_files[relative], expected_targets)

    def test_manifest_rejects_sensitive_categories(self):
        for denied in (
            "auth.json",
            "tokens/access-token",
            "sessions/current.json",
            "history/events.json",
            "logs/sync.log",
            "cache/index",
            "model-settings.json",
            "settings.json",
            "hooks/pre-run.sh",
            "mcp/credentials.json",
            "bin/agent",
            ".env",
            "keys/client.pem",
        ):
            with self.subTest(denied=denied):
                manifest = portable_manifest()
                manifest["skills"][0]["files"].append(
                    {"path": denied, "targets": ["codex"]}
                )
                with self.assertRaisesRegex(ValueError, "denied"):
                    sync.validate_manifest(manifest)

    def test_trigger_requires_sync_for_any_portable_or_shared_rule_change(self):
        for changed in (
            ["SKILL.md"],
            ["references/cross-cli-sync.md"],
            ["references/shared-global-governance.md"],
            ["references/cross-cli-portable-manifest.json"],
        ):
            with self.subTest(changed=changed):
                self.assertTrue(sync.classify_sync_trigger(changed, portable_manifest()))

    def test_repository_only_changes_do_not_trigger_runtime_sync(self):
        changed = [
            "README.md",
            "CHANGELOG.md",
            "tests/test_cross_cli_sync.py",
            "docs/design/history.md",
            "openspec/changes/archive/change/proposal.md",
        ]
        self.assertFalse(sync.classify_sync_trigger(changed, portable_manifest()))

    def test_companion_validator_metadata_is_portable_to_every_required_runtime(self):
        manifest = json.loads(
            (Path(__file__).parents[1] / "references" / "cross-cli-portable-manifest.json")
            .read_text(encoding="utf-8")
        )
        metadata = [
            item
            for skill in manifest["skills"]
            if skill["name"] == "codex-brief-antigravity-review"
            for item in skill["files"]
            if item["path"] == "agents/openai.yaml"
        ]
        self.assertEqual(len(metadata), 1)
        self.assertEqual(
            set(metadata[0]["targets"]),
            {"codex", "pi", "antigravity-cli", "grok-cli"},
        )


class PathAndParityTests(unittest.TestCase):
    def test_path_validation_rejects_absolute_traversal_url_and_backslash(self):
        with tempfile.TemporaryDirectory() as tmp:
            for unsafe in (
                "/tmp/escape",
                "../escape",
                "references/../escape",
                "https://example.invalid/file",
                "C:/secret",
                "references\\escape.md",
                "references//empty.md",
                "references/./dot.md",
                "references/nul\0.md",
            ):
                with self.subTest(unsafe=unsafe):
                    with self.assertRaises(ValueError):
                        sync.validate_relative_path(Path(tmp), unsafe)

    def test_path_validation_rejects_symlink_escape_and_non_regular_file(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside:
            root = Path(tmp)
            outside_file = Path(outside) / "secret"
            outside_file.write_text("do not disclose", encoding="utf-8")
            (root / "escape").symlink_to(outside_file)
            (root / "directory").mkdir()
            for candidate in ("escape", "directory"):
                with self.subTest(candidate=candidate):
                    with self.assertRaises(ValueError):
                        sync.validate_relative_path(root, candidate)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO is not supported")
    def test_path_validation_rejects_fifo(self):
        with tempfile.TemporaryDirectory() as tmp:
            fifo = Path(tmp) / "pipe"
            os.mkfifo(fifo)
            with self.assertRaises(ValueError):
                sync.validate_relative_path(Path(tmp), "pipe")

    def test_portable_manifest_records_relative_sha256(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "SKILL.md").write_text("portable\n", encoding="utf-8")
            records = sync.build_portable_manifest(root, ["SKILL.md"])
            self.assertEqual(records[0]["path"], "SKILL.md")
            self.assertRegex(records[0]["sha256"], r"^[0-9a-f]{64}$")

    def test_portable_parity_rejects_missing_stale_and_extra_files(self):
        with tempfile.TemporaryDirectory() as source_tmp, tempfile.TemporaryDirectory() as target_tmp:
            source = Path(source_tmp)
            target = Path(target_tmp)
            (source / "SKILL.md").write_text("current\n", encoding="utf-8")
            records = [{"path": "SKILL.md", "sha256": "0" * 64}]
            with self.assertRaises(ValueError):
                sync.validate_portable_parity(source, target, records)


class ManagedMarkerTests(unittest.TestCase):
    def setUp(self):
        self.body = "\n".join(f"- [{item}] invariant" for item in INVARIANTS) + "\n"
        self.start = sync.MANAGED_BLOCK_START.format(version=1)
        self.end = sync.MANAGED_BLOCK_END.format(version=1)

    def test_extract_rejects_missing_duplicate_mismatched_and_nested_markers(self):
        invalid = [
            "native only\n",
            f"{self.start}\na\n{self.end}\n{self.start}\nb\n{self.end}\n",
            f"{self.start}\na\n{sync.MANAGED_BLOCK_END.format(version=2)}\n",
            f"{self.start}\n{self.start}\na\n{self.end}\n{self.end}\n",
        ]
        for text in invalid:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    sync.extract_managed_block(text, version=1)

    def test_marker_replacement_preserves_every_outside_byte(self):
        prefix = "native-prefix\r\n"
        suffix = "native-suffix\r\n"
        original = f"{prefix}{self.start}\r\nold\r\n{self.end}\r\n{suffix}"
        replaced = sync.replace_managed_block(original, self.body, version=1)
        self.assertTrue(replaced.startswith(prefix + self.start))
        self.assertTrue(replaced.endswith(self.end + "\r\n" + suffix))

    def test_first_install_appends_one_block_and_preserves_native_prefix_bytes(self):
        original = "native-prefix\r\nnative-suffix"
        installed = sync.install_managed_block(original, self.body, version=1)
        self.assertEqual(installed[: len(original)], original)
        self.assertEqual(installed.count(self.start), 1)
        self.assertEqual(installed.count(self.end), 1)
        self.assertTrue(
            sync.validate_managed_rule_parity(
                self.body, installed, version=1, invariant_ids=INVARIANTS
            )
        )

    def test_version_upgrade_replaces_markers_and_preserves_outside_bytes(self):
        v2_ids = [f"CCG-{number:03d}" for number in range(1, 14)]
        v2_body = "\n".join(f"- [{item}] invariant" for item in v2_ids) + "\n"
        prefix = "native-prefix\r\n"
        suffix = "native-suffix\r\n"
        original = f"{prefix}{self.start}\r\n{self.body}{self.end}\r\n{suffix}"
        upgraded = sync.install_managed_block(original, v2_body, version=2)
        v2_start = sync.MANAGED_BLOCK_START.format(version=2)
        v2_end = sync.MANAGED_BLOCK_END.format(version=2)
        self.assertTrue(upgraded.startswith(prefix + v2_start))
        self.assertTrue(upgraded.endswith(v2_end + "\r\n" + suffix))
        self.assertNotIn(self.start, upgraded)
        self.assertNotIn(self.end, upgraded)
        self.assertTrue(sync.validate_managed_rule_parity(
            v2_body, upgraded, version=2, invariant_ids=v2_ids
        ))

    def test_first_install_rejects_partial_or_mismatched_existing_marker(self):
        for original in (
            f"native\n{self.start}\npartial\n",
            f"native\n{sync.MANAGED_BLOCK_START.format(version=2)}\nold\n"
            f"{sync.MANAGED_BLOCK_END.format(version=2)}\n",
            f"{self.start}\n{self.body}{self.end}\n"
            f"{sync.MANAGED_BLOCK_START.format(version=2)}\nold\n"
            f"{sync.MANAGED_BLOCK_END.format(version=2)}\n",
        ):
            with self.subTest(original=original):
                with self.assertRaises(ValueError):
                    sync.install_managed_block(original, self.body, version=1)

    def test_managed_rule_parity_requires_body_hash_and_all_invariants(self):
        target = f"native\n{self.start}\n{self.body}{self.end}\noverlay\n"
        self.assertTrue(
            sync.validate_managed_rule_parity(
                self.body, target, version=1, invariant_ids=INVARIANTS
            )
        )
        with self.assertRaises(ValueError):
            sync.validate_managed_rule_parity(
                self.body,
                target.replace("CCG-008", "CCG-999"),
                version=1,
                invariant_ids=INVARIANTS,
            )


class TargetStateTests(unittest.TestCase):
    def test_all_required_targets_must_pass(self):
        self.assertTrue(
            sync.validate_target_states(
                [
                    required_target(target_id)
                    for target_id in ("codex", "pi", "antigravity-cli", "grok-cli")
                ]
            )
        )

    def test_failed_required_target_cannot_be_mislabeled_not_applicable(self):
        target = required_target("grok-cli", "blocked")
        target["selection"] = "not-applicable"
        target["reason"] = "discovery failed"
        with self.assertRaises(ValueError):
            sync.validate_target_states([target])

    def test_not_applicable_requires_owner_evidence_reason_and_resume_condition(self):
        valid = {
            "id": "grok-cli",
            "selection": "not-applicable",
            "result": "not-applicable",
            "decision_owner": "codex",
            "evidence": "evidence/grok-not-installed.json",
            "reason": "CLI is not installed",
            "resume_condition": "install Grok CLI and redeclare it required",
        }
        required = [required_target(target_id) for target_id in (
            "codex", "pi", "antigravity-cli"
        )]
        self.assertTrue(sync.validate_target_states([*required, valid]))
        for field in ("decision_owner", "evidence", "reason", "resume_condition"):
            with self.subTest(field=field):
                invalid = dict(valid)
                invalid[field] = ""
                with self.assertRaises(ValueError):
                    sync.validate_target_states([*required, invalid])


class BackupAtomicAndCleanupTests(unittest.TestCase):
    @staticmethod
    def _candidate_entry(path: Path, pre_state: dict) -> dict:
        return {
            "path": str(path),
            "pre_state": pre_state,
            "label": f"test:{path.name}",
            "content": b"candidate\n",
            "candidate_mode": 0o644,
        }

    @staticmethod
    def _replace_parent_directory(
        target: Path, *, replacement_content: bytes | None
    ) -> tuple[Path, Path]:
        reviewed_parent = target.parent
        moved_parent = reviewed_parent.with_name(f"{reviewed_parent.name}-reviewed")
        reviewed_parent.rename(moved_parent)
        reviewed_parent.mkdir()
        if replacement_content is not None:
            replacement = reviewed_parent / target.name
            replacement.write_bytes(replacement_content)
            replacement.chmod(0o644)
        return moved_parent, reviewed_parent

    def test_destination_prestate_rejects_existing_and_absent_drift(self):
        capture = getattr(sync, "capture_destination_prestate", None)
        check = getattr(sync, "assert_destination_prestate", None)
        self.assertTrue(callable(capture), "destination pre-state capture is required")
        self.assertTrue(callable(check), "destination pre-state assertion is required")
        self.assertIn("_assert_target_prestate(plan, target_id)", inspect.getsource(sync.apply_target))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            existing = root / "existing.md"
            missing = root / "missing.md"
            existing.write_text("reviewed\n", encoding="utf-8")
            existing.chmod(0o640)
            existing_state = capture(existing)
            absent_state = capture(missing)
            existing.write_text("drifted\n", encoding="utf-8")
            missing.write_text("concurrent-create\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "pre-state drift"):
                check(existing, existing_state, "existing")
            with self.assertRaisesRegex(ValueError, "pre-state drift"):
                check(missing, absent_state, "missing")

    def test_install_rejects_post_check_existing_file_drift_at_swap_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            target.write_text("reviewed\n", encoding="utf-8")
            entry = self._candidate_entry(
                target, sync.capture_destination_prestate(target)
            )
            original_rename = sync._renameatx
            injected = False

            def drift_before_swap(source, destination, flags, **kwargs):
                nonlocal injected
                if (
                    not injected
                    and Path(destination).name == target.name
                    and flags == sync.RENAME_SWAP
                ):
                    target.write_text("external-drift\n", encoding="utf-8")
                    target.chmod(0o644)
                    injected = True
                return original_rename(source, destination, flags, **kwargs)

            with mock.patch.object(sync, "_renameatx", side_effect=drift_before_swap):
                with self.assertRaisesRegex(ValueError, "mutation-boundary drift"):
                    sync._install_candidate_entry(entry)
            self.assertTrue(injected)
            self.assertFalse(target.exists())
            unsafe = list(target.parent.glob(f"{target.name}.transaction-unsafe.*"))
            self.assertTrue(unsafe)
            self.assertTrue(any(path.read_bytes() == b"external-drift\n" for path in unsafe))

    def test_install_rejects_post_check_absent_file_creation_at_exclusive_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "SKILL.md"
            entry = self._candidate_entry(
                target, sync.capture_destination_prestate(target)
            )
            original_rename = sync._renameatx
            injected = False

            def create_before_exclusive_move(source, destination, flags, **kwargs):
                nonlocal injected
                if (
                    not injected
                    and Path(destination).name == target.name
                    and flags == sync.RENAME_EXCL
                ):
                    target.write_text("external-create\n", encoding="utf-8")
                    target.chmod(0o644)
                    injected = True
                return original_rename(source, destination, flags, **kwargs)

            with mock.patch.object(
                sync, "_renameatx", side_effect=create_before_exclusive_move
            ):
                with self.assertRaisesRegex(ValueError, "mutation-boundary drift"):
                    sync._install_candidate_entry(entry)
            self.assertTrue(injected)
            self.assertEqual(target.read_text(encoding="utf-8"), "external-create\n")

    def test_install_rejects_post_check_symlink_substitution_at_swap_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "RULES.md"
            external = root / "external.md"
            target.write_text("reviewed\n", encoding="utf-8")
            external.write_text("external-target\n", encoding="utf-8")
            entry = self._candidate_entry(
                target, sync.capture_destination_prestate(target)
            )
            original_rename = sync._renameatx
            injected = False

            def symlink_before_swap(source, destination, flags, **kwargs):
                nonlocal injected
                if (
                    not injected
                    and Path(destination).name == target.name
                    and flags == sync.RENAME_SWAP
                ):
                    target.unlink()
                    target.symlink_to(external.name)
                    injected = True
                return original_rename(source, destination, flags, **kwargs)

            with mock.patch.object(sync, "_renameatx", side_effect=symlink_before_swap):
                with self.assertRaisesRegex(ValueError, "mutation-boundary drift"):
                    sync._install_candidate_entry(entry)
            self.assertTrue(injected)
            self.assertFalse(target.exists())
            unsafe = list(target.parent.glob(f"{target.name}.transaction-unsafe.*"))
            self.assertTrue(unsafe)
            self.assertTrue(any(path.is_symlink() and os.readlink(path) == external.name for path in unsafe))

    def test_atomic_create_failure_never_unlinks_concurrent_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "new-skill.md"
            original_fsync = sync.os.fsync
            injected = False

            def fail_after_external_create(descriptor):
                nonlocal injected
                if not injected:
                    target.write_text("external-create\n", encoding="utf-8")
                    target.chmod(0o644)
                    injected = True
                    raise OSError("injected candidate fsync failure")
                return original_fsync(descriptor)

            with mock.patch.object(sync.os, "fsync", side_effect=fail_after_external_create):
                with self.assertRaisesRegex(OSError, "candidate fsync failure"):
                    sync.atomic_create(target, b"candidate\n")
            self.assertTrue(injected)
            self.assertTrue(target.is_file(), "concurrent destination must be preserved")
            self.assertEqual(target.read_text(encoding="utf-8"), "external-create\n")

    def test_atomic_replace_rejects_parent_mapping_change_before_candidate_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp) / "runtime"
            parent.mkdir()
            target = parent / "AGENTS.md"
            target.write_bytes(b"reviewed\n")
            expected = sync.capture_destination_prestate(target)
            original_writer = sync._write_same_directory_candidate
            moved_parent = None

            def replace_parent_before_write(path, content, mode, **kwargs):
                nonlocal moved_parent
                moved_parent, _ = self._replace_parent_directory(
                    Path(path), replacement_content=b"reviewed\n"
                )
                return original_writer(path, content, mode, **kwargs)

            with mock.patch.object(
                sync,
                "_write_same_directory_candidate",
                side_effect=replace_parent_before_write,
            ):
                with self.assertRaisesRegex(ValueError, "parent.*drift"):
                    sync.atomic_replace(
                        target,
                        b"candidate\n",
                        expected_state=expected,
                        label="parent-replace",
                    )
            self.assertIsNotNone(moved_parent)
            self.assertEqual((moved_parent / target.name).read_bytes(), b"reviewed\n")
            self.assertEqual(target.read_bytes(), b"reviewed\n")

    def test_atomic_create_rejects_parent_mapping_change_before_candidate_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp) / "runtime"
            parent.mkdir()
            target = parent / "SKILL.md"
            expected = sync.capture_destination_prestate(target)
            original_writer = sync._write_same_directory_candidate
            moved_parent = None

            def replace_parent_before_write(path, content, mode, **kwargs):
                nonlocal moved_parent
                moved_parent, _ = self._replace_parent_directory(
                    Path(path), replacement_content=None
                )
                return original_writer(path, content, mode, **kwargs)

            with mock.patch.object(
                sync,
                "_write_same_directory_candidate",
                side_effect=replace_parent_before_write,
            ):
                with self.assertRaisesRegex(ValueError, "parent.*drift"):
                    sync.atomic_create(
                        target,
                        b"candidate\n",
                        expected_state=expected,
                        label="parent-create",
                    )
            self.assertIsNotNone(moved_parent)
            self.assertFalse((moved_parent / target.name).exists())
            self.assertFalse(target.exists())

    def test_atomic_replace_rejects_parent_symlink_substitution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            parent = root / "runtime"
            alternate = root / "alternate"
            parent.mkdir()
            alternate.mkdir()
            target = parent / "RULES.md"
            target.write_bytes(b"reviewed\n")
            alternate_target = alternate / target.name
            alternate_target.write_bytes(b"reviewed\n")
            expected = sync.capture_destination_prestate(target)
            original_writer = sync._write_same_directory_candidate
            moved_parent = root / "runtime-reviewed"

            def substitute_parent_before_write(path, content, mode, **kwargs):
                parent.rename(moved_parent)
                parent.symlink_to(alternate, target_is_directory=True)
                return original_writer(path, content, mode, **kwargs)

            with mock.patch.object(
                sync,
                "_write_same_directory_candidate",
                side_effect=substitute_parent_before_write,
            ):
                with self.assertRaisesRegex(ValueError, "parent.*drift"):
                    sync.atomic_replace(
                        target,
                        b"candidate\n",
                        expected_state=expected,
                        label="parent-symlink",
                    )
            self.assertEqual((moved_parent / target.name).read_bytes(), b"reviewed\n")
            self.assertEqual(alternate_target.read_bytes(), b"reviewed\n")

    def test_sensitive_backup_is_0600_and_outside_discovery_root(self):
        with tempfile.TemporaryDirectory() as source_tmp, tempfile.TemporaryDirectory() as backup_tmp:
            source = Path(source_tmp) / "AGENTS.md"
            source.write_text("private native overlay\n", encoding="utf-8")
            backup = sync.create_secure_backup(source, Path(backup_tmp), sensitive=True)
            self.assertEqual(stat.S_IMODE(backup.stat().st_mode), 0o600)
            self.assertFalse(str(backup).startswith(str(source.parent / "skills")))

    def test_backup_root_symlink_cannot_redirect_into_skill_discovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "AGENTS.md"
            source.write_text("native rules\n", encoding="utf-8")
            discovery = root / "runtime" / "skills" / "hidden-backups"
            discovery.mkdir(parents=True)
            redirected = root / "backup-link"
            redirected.symlink_to(discovery, target_is_directory=True)
            with self.assertRaises(ValueError):
                sync.create_secure_backup(source, redirected, sensitive=True)

    def test_atomic_replace_preserves_live_mode_and_leaves_no_temp_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            target.write_text("old\n", encoding="utf-8")
            target.chmod(0o644)
            sync.atomic_replace(target, b"new\n")
            self.assertEqual(target.read_bytes(), b"new\n")
            self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o644)
            self.assertEqual(list(Path(tmp).glob(".cross-cli-sync.*")), [])

    def test_atomic_replace_rejects_candidate_substitution_before_swap(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            target.write_bytes(b"reviewed\n")
            original_rename = sync._renameatx
            injected = False

            def substitute_candidate(source, destination, flags, **kwargs):
                nonlocal injected
                candidate = target.parent / Path(source).name
                if (
                    not injected
                    and Path(destination).name == target.name
                    and flags == sync.RENAME_SWAP
                    and candidate.exists()
                ):
                    candidate.unlink()
                    unrelated = target.parent / "unrelated-candidate"
                    unrelated.write_bytes(b"unrelated\n")
                    unrelated.rename(candidate)
                    injected = True
                return original_rename(source, destination, flags, **kwargs)

            with mock.patch.object(sync, "_renameatx", side_effect=substitute_candidate):
                with self.assertRaisesRegex(ValueError, "candidate|mutation-boundary|ambiguous"):
                    sync.atomic_replace(target, b"candidate\n")

            self.assertTrue(injected)
            self.assertFalse(target.exists())
            unsafe = list(target.parent.glob(f"{target.name}.transaction-unsafe.*"))
            self.assertTrue(unsafe)
            self.assertTrue(any(path.read_bytes() == b"unrelated\n" for path in unsafe))

    def test_atomic_create_rejects_candidate_substitution_before_exclusive_move(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "SKILL.md"
            original_rename = sync._renameatx
            injected = False

            def substitute_candidate(source, destination, flags, **kwargs):
                nonlocal injected
                candidate = target.parent / Path(source).name
                if (
                    not injected
                    and Path(destination).name == target.name
                    and flags == sync.RENAME_EXCL
                    and candidate.exists()
                ):
                    candidate.unlink()
                    unrelated = target.parent / "unrelated-candidate"
                    unrelated.write_bytes(b"unrelated\n")
                    unrelated.rename(candidate)
                    injected = True
                return original_rename(source, destination, flags, **kwargs)

            with mock.patch.object(sync, "_renameatx", side_effect=substitute_candidate):
                with self.assertRaisesRegex(ValueError, "candidate|mutation-boundary|ambiguous"):
                    sync.atomic_create(target, b"candidate\n")

            self.assertTrue(injected)
            self.assertFalse(target.exists())
            pending = list(target.parent.glob(f"{target.name}.transaction-*"))
            self.assertTrue(pending)
            self.assertEqual(pending[0].read_bytes(), b"unrelated\n")

    def test_atomic_replace_restores_destination_after_post_swap_candidate_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "RULES.md"
            target.write_bytes(b"reviewed\n")
            original_rename = sync._renameatx
            injected = False

            def substitute_destination(source, destination, flags, **kwargs):
                nonlocal injected
                result = original_rename(source, destination, flags, **kwargs)
                if (
                    not injected
                    and Path(destination).name == target.name
                    and flags == sync.RENAME_SWAP
                ):
                    target.unlink()
                    unrelated = target.parent / "unrelated-destination"
                    unrelated.write_bytes(b"unrelated\n")
                    unrelated.rename(target)
                    injected = True
                return result

            with mock.patch.object(sync, "_renameatx", side_effect=substitute_destination):
                with self.assertRaisesRegex(ValueError, "candidate|mutation-boundary|ambiguous"):
                    sync.atomic_replace(target, b"candidate\n")

            self.assertTrue(injected)
            self.assertFalse(target.exists())
            unsafe = list(target.parent.glob(f"{target.name}.transaction-unsafe.*"))
            self.assertTrue(unsafe)
            self.assertTrue(any(path.read_bytes() == b"unrelated\n" for path in unsafe))

    def test_atomic_replace_requires_both_exchange_bindings_for_rollback(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "RULES.md"
            target.write_bytes(b"reviewed\n")
            original_rename = sync._renameatx
            injected = False

            def replace_displaced_after_swap(source, destination, flags, **kwargs):
                nonlocal injected
                result = original_rename(source, destination, flags, **kwargs)
                temporary = target.parent / Path(source).name
                if (
                    not injected
                    and Path(destination).name == target.name
                    and flags == sync.RENAME_SWAP
                ):
                    temporary.unlink()
                    unrelated = target.parent / "unrelated-displaced"
                    unrelated.write_bytes(b"unrelated-displaced\n")
                    unrelated.rename(temporary)
                    injected = True
                return result

            with mock.patch.object(
                sync, "_renameatx", side_effect=replace_displaced_after_swap
            ):
                with self.assertRaisesRegex(ValueError, "rollback|mutation-boundary|ambiguous"):
                    sync.atomic_replace(target, b"candidate\n")

            self.assertTrue(injected)
            self.assertFalse(target.exists())
            unsafe = list(target.parent.glob(f"{target.name}.transaction-unsafe.*"))
            self.assertTrue(unsafe)
            self.assertTrue(any(path.read_bytes() == b"unrelated-displaced\n" for path in unsafe))

    def test_atomic_create_restores_candidate_after_post_install_destination_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "SKILL.md"
            original_rename = sync._renameatx
            injected = False

            def substitute_destination(source, destination, flags, **kwargs):
                nonlocal injected
                result = original_rename(source, destination, flags, **kwargs)
                if (
                    not injected
                    and Path(destination).name == target.name
                    and flags == sync.RENAME_EXCL
                ):
                    target.unlink()
                    unrelated = target.parent / "unrelated-destination"
                    unrelated.write_bytes(b"unrelated\n")
                    unrelated.rename(target)
                    injected = True
                return result

            with mock.patch.object(sync, "_renameatx", side_effect=substitute_destination):
                with self.assertRaisesRegex(ValueError, "candidate|mutation-boundary|ambiguous"):
                    sync.atomic_create(target, b"candidate\n")

            self.assertTrue(injected)
            self.assertFalse(target.exists())
            pending = list(target.parent.glob(f"{target.name}.transaction-*"))
            self.assertTrue(pending)
            self.assertEqual(pending[0].read_bytes(), b"unrelated\n")

    def test_generic_candidate_fsync_cleanup_failure_uses_visible_recovery_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "SKILL.md"
            original_fsync = sync.os.fsync
            original_unlink = sync._guarded_unlink
            failed = False

            def fail_candidate_fsync(descriptor):
                nonlocal failed
                if not failed:
                    failed = True
                    raise OSError("injected generic candidate fsync failure")
                return original_fsync(descriptor)

            def fail_candidate_cleanup(guard, name, *, missing_ok=False):
                if name.startswith(
                    (
                        f"{target.name}.transaction-pending.",
                        f"{target.name}.transaction-cleanup.",
                        ".cross-cli-sync.",
                    )
                ):
                    raise OSError("injected generic candidate cleanup failure")
                return original_unlink(guard, name, missing_ok=missing_ok)

            with mock.patch.object(sync.os, "fsync", side_effect=fail_candidate_fsync), \
                    mock.patch.object(sync, "_guarded_unlink", side_effect=fail_candidate_cleanup):
                with self.assertRaisesRegex(OSError, "generic candidate|cleanup|fsync"):
                    sync.atomic_create(target, b"candidate\n")

            self.assertTrue(failed)
            self.assertFalse(list(target.parent.glob(".cross-cli-sync.*")))
            recovery = list(target.parent.glob(f"{target.name}.transaction-*"))
            self.assertTrue(recovery)
            self.assertEqual(recovery[0].read_bytes(), b"candidate\n")

    def test_generic_candidate_cleanup_rejects_substitution_after_guard_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "SKILL.md"
            original_assert_parent_guard = sync._assert_parent_guard
            injected = False

            def fail_after_substitution(guard, label):
                nonlocal injected
                pending = list(
                    guard["path"].glob(f"{target.name}.transaction-pending.*")
                )
                if pending and not injected:
                    candidate = pending[0]
                    candidate.unlink()
                    unrelated = guard["path"] / "unrelated-candidate"
                    unrelated.write_bytes(b"unrelated\n")
                    unrelated.chmod(0o600)
                    unrelated.rename(candidate)
                    injected = True
                    raise OSError("injected parent-guard failure after substitution")
                return original_assert_parent_guard(guard, label)

            with mock.patch.object(
                sync, "_assert_parent_guard", side_effect=fail_after_substitution
            ):
                with self.assertRaisesRegex(OSError, "parent-guard|substitution|failure"):
                    sync.atomic_create(target, b"candidate\n")

            self.assertTrue(injected)
            survivors = [
                path for path in target.parent.iterdir() if path.name != target.name
            ]
            self.assertTrue(any(path.read_bytes() == b"unrelated\n" for path in survivors))
            self.assertFalse(any(path.name.startswith(".cross-cli-sync.") for path in survivors))
            self.assertTrue(
                any(path.name.startswith(f"{target.name}.transaction-unsafe.") for path in survivors)
            )

    def test_generic_bound_cleanup_rechecks_before_unlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "cleanup-candidate"
            target.write_bytes(b"candidate\n")
            unrelated_bytes = b"unrelated-after-unlink-check\n"
            original_unlink = sync._guarded_unlink
            injected = False

            with sync._verified_parent(target, "generic unlink race") as guard:
                ownership = sync._open_guarded_binding(
                    guard, target.name, "generic unlink race"
                )
                try:
                    def substitute_before_unlink(unlink_guard, name, *, missing_ok=False):
                        nonlocal injected
                        if not injected and name.startswith(
                            f"{target.name}.transaction-cleanup."
                        ):
                            cleanup = target.parent / name
                            cleanup.unlink()
                            replacement = target.parent / "unrelated-cleanup"
                            replacement.write_bytes(unrelated_bytes)
                            replacement.rename(cleanup)
                            injected = True
                        return original_unlink(
                            unlink_guard, name, missing_ok=missing_ok
                        )

                    with mock.patch.object(
                        sync, "_guarded_unlink", side_effect=substitute_before_unlink
                    ):
                        with self.assertRaisesRegex(ValueError, "cleanup|ownership|drift|ambiguous"):
                            sync._remove_bound_entry(
                                guard,
                                target.name,
                                ownership,
                                target.name,
                                "generic unlink race",
                            )
                finally:
                    os.close(ownership["fd"])

            self.assertTrue(injected)
            survivors = list(target.parent.iterdir())
            self.assertTrue(any(path.read_bytes() == unrelated_bytes for path in survivors))
            self.assertFalse(any(path.name.startswith(".cross-cli-sync.") for path in survivors))

    def test_generic_bound_cleanup_quarantines_after_rebind_race(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "cleanup-candidate"
            target.write_bytes(b"candidate\n")
            unrelated_bytes = b"unrelated-after-rebind\n"
            original_rebind = sync._rebind_before_unlink
            injected = False

            with sync._verified_parent(target, "generic post-rebind unlink race") as guard:
                ownership = sync._open_guarded_binding(
                    guard, target.name, "generic post-rebind unlink race"
                )
                try:
                    def move_retained_and_replace_name(check_guard, name, context):
                        nonlocal injected
                        result = original_rebind(check_guard, name, context)
                        if not injected:
                            cleanup = target.parent / name
                            retained_aside = target.parent / "retained-aside"
                            cleanup.rename(retained_aside)
                            unrelated = target.parent / "unrelated-post-rebind"
                            unrelated.write_bytes(unrelated_bytes)
                            unrelated.rename(cleanup)
                            injected = True
                        return result

                    with mock.patch.object(
                        sync,
                        "_rebind_before_unlink",
                        side_effect=move_retained_and_replace_name,
                    ):
                        with self.assertRaisesRegex(ValueError, "cleanup|ownership|drift|ambiguous"):
                            sync._remove_bound_entry(
                                guard,
                                target.name,
                                ownership,
                                target.name,
                                "generic post-rebind unlink race",
                            )
                finally:
                    os.close(ownership["fd"])

            self.assertTrue(injected)
            self.assertTrue(
                any(
                    path.read_bytes() == unrelated_bytes
                    for path in target.parent.iterdir()
                    if path.is_file()
                )
            )
            self.assertTrue(
                list(target.parent.glob(f"{target.name}.transaction-unsafe.*"))
            )
            self.assertTrue((target.parent / "retained-aside").exists())

    def test_generic_bound_cleanup_rejects_replacement_after_final_owner_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "cleanup-candidate"
            target.write_bytes(b"candidate\n")
            unrelated_bytes = b"unrelated-after-final-owner-check\n"
            original_require = sync._require_retained_binding
            injected = False

            with sync._verified_parent(target, "generic final owner check race") as guard:
                ownership = sync._open_guarded_binding(
                    guard, target.name, "generic final owner check race"
                )
                try:
                    def replace_after_final_owner_check(
                        check_guard,
                        name,
                        check_ownership,
                        label,
                        *,
                        expected=None,
                        allow_rename_ctime=False,
                    ):
                        nonlocal injected
                        value = original_require(
                            check_guard,
                            name,
                            check_ownership,
                            label,
                            expected=expected,
                            allow_rename_ctime=allow_rename_ctime,
                        )
                        if not injected and name.startswith(
                            f"{target.name}.transaction-unlink."
                        ):
                            quarantine = target.parent / name
                            quarantine.rename(target.parent / "retained-final-aside")
                            unrelated = target.parent / "unrelated-final-owner-check"
                            unrelated.write_bytes(unrelated_bytes)
                            unrelated.rename(quarantine)
                            injected = True
                        return value

                    with mock.patch.object(
                        sync,
                        "_require_retained_binding",
                        side_effect=replace_after_final_owner_check,
                    ):
                        with self.assertRaisesRegex(ValueError, "cleanup|ownership|drift|ambiguous"):
                            sync._remove_bound_entry(
                                guard,
                                target.name,
                                ownership,
                                target.name,
                                "generic final owner check race",
                            )
                finally:
                    os.close(ownership["fd"])

            self.assertTrue(injected)
            self.assertTrue(
                any(
                    path.read_bytes() == unrelated_bytes
                    for path in target.parent.iterdir()
                    if path.is_file()
                )
            )
            self.assertTrue(
                list(target.parent.glob(f"{target.name}.transaction-unsafe.*"))
            )
            self.assertTrue((target.parent / "retained-final-aside").exists())

    def test_generic_bound_cleanup_records_post_delete_uncertainty(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "cleanup-candidate"
            target.write_bytes(b"candidate\n")
            injected = False

            def delete_then_raise(dir_fd, name):
                nonlocal injected
                injected = True
                os.unlink(name, dir_fd=dir_fd)
                raise OSError("injected post-delete uncertainty")

            with sync._verified_parent(target, "generic post-delete uncertainty") as guard:
                ownership = sync._open_guarded_binding(
                    guard, target.name, "generic post-delete uncertainty"
                )
                try:
                    with mock.patch.object(
                        sync,
                        "_unlinkat_kernel",
                        create=True,
                        side_effect=delete_then_raise,
                    ):
                        with self.assertRaisesRegex(ValueError, "uncertain|blocked|cleanup"):
                            sync._remove_bound_entry(
                                guard,
                                target.name,
                                ownership,
                                target.name,
                                "generic post-delete uncertainty",
                            )
                finally:
                    os.close(ownership["fd"])

            self.assertTrue(injected)
            blockers = list(target.parent.glob(f"{target.name}.transaction-blocked.*"))
            self.assertTrue(blockers)
            self.assertTrue(all(stat.S_IMODE(path.stat().st_mode) == 0o600 for path in blockers))
            self.assertFalse(list(target.parent.glob(f"{target.name}.transaction-unlink.*")))
            self.assertFalse(any(path.name.startswith(".cross-cli-sync.") for path in target.parent.iterdir()))

    def test_generic_bound_cleanup_fail_closes_replacement_after_final_bind(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "cleanup-candidate"
            target.write_bytes(b"candidate\n")
            unrelated_bytes = b"unrelated-after-final-bind\n"
            original_open = sync._open_guarded_binding
            injected = False

            with sync._verified_parent(target, "generic final bind race") as guard:
                ownership = sync._open_guarded_binding(
                    guard, target.name, "generic final bind race"
                )
                try:
                    def replace_after_final_bind(
                        bind_guard, name, label, *, writable=False
                    ):
                        nonlocal injected
                        binding = original_open(
                            bind_guard, name, label, writable=writable
                        )
                        if not injected and name.startswith(
                            f"{target.name}.transaction-unlink."
                        ):
                            quarantine = target.parent / name
                            quarantine.rename(target.parent / "retained-final-bind-aside")
                            unrelated = target.parent / "unrelated-final-bind"
                            unrelated.write_bytes(unrelated_bytes)
                            unrelated.rename(quarantine)
                            injected = True
                        return binding

                    with mock.patch.object(
                        sync,
                        "_open_guarded_binding",
                        side_effect=replace_after_final_bind,
                    ):
                        with self.assertRaisesRegex(ValueError, "cleanup|ownership|blocked"):
                            sync._remove_bound_entry(
                                guard,
                                target.name,
                                ownership,
                                target.name,
                                "generic final bind race",
                            )
                finally:
                    os.close(ownership["fd"])

            self.assertTrue(injected)
            self.assertTrue(
                any(path.read_bytes() == unrelated_bytes for path in target.parent.iterdir())
            )
            self.assertTrue(
                list(target.parent.glob(f"{target.name}.transaction-unsafe.*"))
            )
            self.assertTrue((target.parent / "retained-final-bind-aside").exists())
            self.assertTrue(list(target.parent.glob(f"{target.name}.transaction-blocked.*")))
            self.assertFalse(
                any(path.name.startswith(".cross-cli-sync.") for path in target.parent.iterdir())
            )

    def test_atomic_replace_closes_destination_binding_when_candidate_write_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "SKILL.md"
            target.write_bytes(b"old\n")
            captured = []
            original_open_binding = sync._open_guarded_binding

            def capture_destination(guard, name, label, *, writable=False):
                binding = original_open_binding(
                    guard, name, label, writable=writable
                )
                if name == target.name:
                    captured.append(binding["fd"])
                return binding

            with mock.patch.object(
                sync, "_open_guarded_binding", side_effect=capture_destination
            ), mock.patch.object(
                sync,
                "_write_same_directory_candidate",
                side_effect=OSError("injected candidate write failure"),
            ):
                with self.assertRaisesRegex(OSError, "candidate write"):
                    sync.atomic_replace(target, b"new\n")

            self.assertEqual(len(captured), 1)
            with self.assertRaises(OSError) as error:
                os.fstat(captured[0])
            self.assertEqual(error.exception.errno, errno.EBADF)

    def test_atomic_create_rejects_candidate_ctime_drift_before_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "SKILL.md"
            original_write = sync._write_same_directory_candidate
            drifted = False

            def write_then_drift(*args, **kwargs):
                nonlocal drifted
                candidate = original_write(*args, **kwargs)
                candidate_path = Path(candidate["path"])
                metadata = candidate_path.stat()
                os.utime(
                    candidate_path,
                    ns=(metadata.st_mtime_ns, metadata.st_mtime_ns),
                )
                drifted = candidate_path.stat().st_ctime_ns != candidate["ctime_ns"]
                return candidate

            with mock.patch.object(
                sync,
                "_write_same_directory_candidate",
                side_effect=write_then_drift,
            ):
                with self.assertRaisesRegex(ValueError, "candidate|drift|mutation"):
                    sync.atomic_create(target, b"candidate\n")

            self.assertTrue(drifted)
            self.assertFalse(target.exists())
            self.assertFalse(any(path.name.startswith(".cross-cli-sync.") for path in target.parent.iterdir()))

    def test_transaction_rolls_back_prior_replacements_after_midway_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "first.md"
            second = root / "second.md"
            first.write_text("first-old\n", encoding="utf-8")
            second.write_text("second-old\n", encoding="utf-8")
            operations = [
                {"path": first, "content": b"first-new\n"},
                {"path": second, "content": b"second-new\n", "inject_failure": True},
            ]
            with self.assertRaisesRegex(RuntimeError, "injected sync failure"):
                sync.apply_sync_transaction(operations, root / "backups")
            self.assertEqual(first.read_text(encoding="utf-8"), "first-old\n")
            self.assertEqual(second.read_text(encoding="utf-8"), "second-old\n")

    def test_transaction_rolls_back_only_files_and_directories_it_created(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            existing = root / "existing"
            existing.mkdir()
            created = existing / "new-skill" / "references" / "rule.md"
            operations = [
                {"path": created, "content": b"portable\n", "create": True},
                {
                    "path": root / "failure.md",
                    "content": b"never-written\n",
                    "create": True,
                    "inject_failure": True,
                },
            ]
            with self.assertRaisesRegex(RuntimeError, "injected sync failure"):
                sync.apply_sync_transaction(operations, root / "backups")
            self.assertTrue(existing.is_dir())
            self.assertFalse((existing / "new-skill").exists())
            self.assertFalse((root / "failure.md").exists())

    def test_transaction_creates_missing_regular_file_without_overwriting(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "skill" / "SKILL.md"
            backups = sync.apply_sync_transaction(
                [{"path": target, "content": b"created\n", "create": True}],
                root / "backups",
            )
            self.assertEqual(backups, [])
            self.assertEqual(target.read_bytes(), b"created\n")
            with self.assertRaises((FileExistsError, ValueError)):
                sync.apply_sync_transaction(
                    [{"path": target, "content": b"overwrite\n", "create": True}],
                    root / "other-backups",
                )

    def test_transaction_rolls_back_when_post_apply_verification_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            existing = root / "existing.md"
            created = root / "new-skill" / "SKILL.md"
            existing.write_text("old\n", encoding="utf-8")
            existing.chmod(0o640)
            reviewed_hash = sync._sha256(existing)

            def fail_verification():
                raise ValueError("post-apply parity failure")

            with self.assertRaisesRegex(ValueError, "post-apply parity failure"):
                sync.apply_sync_transaction(
                    [
                        {"path": existing, "content": b"new\n"},
                        {"path": created, "content": b"created\n", "create": True},
                    ],
                    root / "backups",
                    verify=fail_verification,
                )
            self.assertEqual(existing.read_text(encoding="utf-8"), "old\n")
            self.assertEqual(sync._sha256(existing), reviewed_hash)
            self.assertEqual(stat.S_IMODE(existing.stat().st_mode), 0o640)
            self.assertFalse((root / "new-skill").exists())

    def test_success_cleanup_removes_backups_and_temporary_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            backup = Path(tmp) / "backup"
            temporary = Path(tmp) / ".cross-cli-sync.temp"
            backup.write_text("backup", encoding="utf-8")
            temporary.write_text("temporary", encoding="utf-8")
            sync.cleanup_success_artifacts([backup], [temporary])
            self.assertFalse(backup.exists())
            self.assertFalse(temporary.exists())

    def test_diagnostics_never_disclose_sensitive_file_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            secret = "SENSITIVE_SENTINEL_VALUE"
            denied = Path(tmp) / "auth.json"
            denied.write_text(secret, encoding="utf-8")
            with self.assertRaises(ValueError) as caught:
                sync.build_portable_manifest(Path(tmp), ["auth.json"])
            self.assertNotIn(secret, str(caught.exception))


class DiscoveryTests(unittest.TestCase):
    def test_grok_inspect_requires_both_skills_from_expected_user_root(self):
        root = "/home/user/.grok/skills"
        payload = {
            "skills": [
                {
                    "name": name,
                    "source": {"type": "user", "path": f"{root}/{name}/SKILL.md"},
                }
                for name in SKILLS
            ]
        }
        self.assertTrue(sync.validate_grok_discovery(json.dumps(payload), SKILLS, root))

    def test_grok_discovery_rejects_wrong_or_missing_skill_path(self):
        payload = {
            "skills": [
                {
                    "name": SKILLS[0],
                    "source": {"type": "project", "path": "/tmp/wrong/SKILL.md"},
                }
            ]
        }
        with self.assertRaises(ValueError):
            sync.validate_grok_discovery(
                json.dumps(payload), SKILLS, "/home/user/.grok/skills"
            )

    def test_antigravity_discovery_uses_deterministic_manifest_closure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            records = {}
            for name in SKILLS:
                skill = root / name
                skill.mkdir()
                (skill / "SKILL.md").write_text(f"name: {name}\n", encoding="utf-8")
                records[name] = [{"path": "SKILL.md"}]
            self.assertTrue(sync.validate_antigravity_discovery(root, SKILLS, records))


class CrossCliForwardTests(unittest.TestCase):
    def test_premature_completion_is_blocked_until_all_required_targets_pass(self):
        targets = [
            required_target("codex"),
            required_target("pi"),
            required_target("antigravity-cli"),
            required_target("grok-cli", "pending"),
        ]
        with self.assertRaises(ValueError):
            sync.validate_target_states(targets)

    def test_auxiliary_self_approval_cannot_complete_sync(self):
        with self.assertRaises(ValueError):
            sync.validate_completion_authority(
                {
                    "decision_owner": "antigravity-cli",
                    "reviewer_agent": "antigravity-cli",
                    "result": "pass",
                }
            )

    def test_missing_grok_sync_blocks_completion(self):
        with self.assertRaises(ValueError):
            sync.validate_target_states(
                [required_target("codex"), required_target("antigravity-cli")]
            )

    def test_stale_antigravity_files_block_completion(self):
        with tempfile.TemporaryDirectory() as source_tmp, tempfile.TemporaryDirectory() as target_tmp:
            source = Path(source_tmp)
            target = Path(target_tmp)
            (source / "SKILL.md").write_text("source\n", encoding="utf-8")
            (target / "SKILL.md").write_text("stale\n", encoding="utf-8")
            records = sync.build_portable_manifest(source, ["SKILL.md"])
            with self.assertRaises(ValueError):
                sync.validate_portable_parity(source, target, records)

    def test_credential_copying_is_rejected(self):
        manifest = portable_manifest()
        manifest["skills"][0]["files"].append(
            {"path": "auth/token.json", "targets": ["grok-cli"]}
        )
        with self.assertRaisesRegex(ValueError, "denied"):
            sync.validate_manifest(manifest)


class CliContractTests(unittest.TestCase):
    def test_cli_exposes_the_executable_sync_contract(self):
        result = subprocess.run(
            [sys.executable, str(Path(sync.__file__)), "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        for command in (
            "plan", "apply", "verify", "verify-all", "verify-discovery", "audit"
        ):
            self.assertIn(command, result.stdout)

    def test_plan_apply_and_verify_round_trip_in_isolated_runtimes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            openspec = root / "openspec"
            brief = root / "brief"
            openspec.mkdir()
            brief.mkdir()
            for relative in (
                "SKILL.md",
                "references/cross-cli-sync.md",
                "scripts/validate_core_gates.py",
            ):
                path = openspec / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"portable {relative}\n", encoding="utf-8")
            (brief / "SKILL.md").write_text("portable brief\n", encoding="utf-8")
            managed = openspec / "references" / "shared-global-governance.md"
            managed.write_text(
                (
                    Path(__file__).parents[1]
                    / "references"
                    / "shared-global-governance.md"
                ).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps(portable_manifest_v6()), encoding="utf-8")
            target_args = []
            for cli in ("codex", "pi", "antigravity", "grok"):
                runtime = root / cli
                skills = runtime / "skills"
                skills.mkdir(parents=True)
                rule_name = {
                    "codex": "AGENTS.md",
                    "pi": "APPEND_SYSTEM.md",
                    "antigravity": None,
                    "grok": "AGENTS.md",
                }[cli]
                rule = (
                    root / "GEMINI.md"
                    if cli == "antigravity"
                    else runtime / rule_name
                )
                rule.write_text(f"native-{cli}\n", encoding="utf-8")
                target_args.extend(
                    [f"--{cli}-skills-root", str(skills), f"--{cli}-rule-file", str(rule)]
                )
            plan = root / "sync-plan.json"
            script = str(Path(sync.__file__))
            plan_result = subprocess.run(
                [
                    sys.executable,
                    script,
                    "plan",
                    "--manifest",
                    str(manifest),
                    "--openspec-source",
                    str(openspec),
                    "--brief-source",
                    str(brief),
                    *target_args,
                    "--output",
                    str(plan),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(plan_result.returncode, 0, plan_result.stderr)
            planned = json.loads(plan.read_text(encoding="utf-8"))
            transaction_root = root / "transactions"
            transaction_root.mkdir(mode=0o700)
            for target in planned["targets"].values():
                self.assertIn("rule_pre_state", target)
                for item in target["files"]:
                    self.assertIn("destination", item)
                    self.assertIn("pre_state", item)

            prestate_result = subprocess.run(
                [
                    sys.executable,
                    script,
                    "verify-prestate",
                    "--target",
                    "all",
                    "--plan",
                    str(plan),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(prestate_result.returncode, 0, prestate_result.stderr)
            self.assertEqual(
                json.loads(prestate_result.stdout),
                {"prestate": "pass", "targets": list(sync.TARGET_ORDER)},
            )

            codex_target = planned["targets"]["codex"]
            absent_destination = Path(codex_target["files"][0]["destination"])
            self.assertEqual(codex_target["files"][0]["pre_state"], {"kind": "absent"})
            absent_destination.parent.mkdir(parents=True)
            absent_destination.write_text("concurrent-create\n", encoding="utf-8")
            stale_absent = subprocess.run(
                [
                    sys.executable,
                    script,
                    "apply",
                    "--target",
                    "codex",
                    "--plan",
                    str(plan),
                    "--backup-root",
                    str(root / "backups"),
                    "--transaction-receipt",
                    str(transaction_root / "codex.json"),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(stale_absent.returncode, 0)
            self.assertIn("pre-state drift", stale_absent.stderr)
            self.assertEqual(
                absent_destination.read_text(encoding="utf-8"), "concurrent-create\n"
            )
            self.assertFalse((root / "backups" / "codex").exists())
            absent_destination.unlink()

            codex_rule = Path(codex_target["rule_file"])
            reviewed_rule = codex_rule.read_bytes()
            reviewed_rule_mode = stat.S_IMODE(codex_rule.stat().st_mode)
            codex_rule.write_text("concurrent-rule-drift\n", encoding="utf-8")
            stale_rule = subprocess.run(
                [
                    sys.executable,
                    script,
                    "apply",
                    "--target",
                    "codex",
                    "--plan",
                    str(plan),
                    "--backup-root",
                    str(root / "backups"),
                    "--transaction-receipt",
                    str(transaction_root / "codex.json"),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(stale_rule.returncode, 0)
            self.assertIn("pre-state drift", stale_rule.stderr)
            self.assertEqual(codex_rule.read_text(encoding="utf-8"), "concurrent-rule-drift\n")
            self.assertFalse((root / "backups" / "codex").exists())
            codex_rule.write_bytes(reviewed_rule)
            codex_rule.chmod(reviewed_rule_mode)

            for target in ("codex", "pi", "antigravity-cli", "grok-cli"):
                receipt = transaction_root / f"{target}.json"
                apply_result = subprocess.run(
                    [
                        sys.executable,
                        script,
                        "apply",
                        "--target",
                        target,
                        "--plan",
                        str(plan),
                        "--backup-root",
                        str(root / "backups"),
                        "--transaction-receipt",
                        str(receipt),
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(apply_result.returncode, 0, apply_result.stderr)
                verify_result = subprocess.run(
                    [
                        sys.executable, script, "verify", "--target", target,
                        "--plan", str(plan), "--transaction-receipt", str(receipt),
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(verify_result.returncode, 0, verify_result.stderr)
                discovery_command = [
                    sys.executable, script, "verify-discovery", "--target", target,
                    "--plan", str(plan), "--transaction-receipt", str(receipt),
                ]
                if target == "grok-cli":
                    inspect_json = transaction_root / "grok-inspect.json"
                    grok_root = planned["targets"][target]["skills_root"]
                    inspect_json.write_text(
                        json.dumps({
                            "skills": [
                                {
                                    "name": name,
                                    "source": {
                                        "type": "user",
                                        "path": f"{grok_root}/{name}/SKILL.md",
                                    },
                                }
                                for name in SKILLS
                            ]
                        }),
                        encoding="utf-8",
                    )
                    inspect_json.chmod(0o600)
                    discovery_command.extend(["--inspect-json", str(inspect_json)])
                discovery_result = subprocess.run(
                    discovery_command, capture_output=True, text=True, check=False,
                )
                self.assertEqual(
                    discovery_result.returncode, 0, discovery_result.stderr
                )
                commit_result = subprocess.run(
                    [
                        sys.executable, script, "commit-target", "--target", target,
                        "--plan", str(plan), "--transaction-receipt", str(receipt),
                    ],
                    capture_output=True, text=True, check=False,
                )
                self.assertEqual(commit_result.returncode, 0, commit_result.stderr)
            verify_all = subprocess.run(
                [
                    sys.executable, script, "verify-all", "--plan", str(plan),
                    "--transaction-root", str(transaction_root),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(verify_all.returncode, 0, verify_all.stderr)

            tampered = json.loads(plan.read_text(encoding="utf-8"))
            tampered["targets"]["grok-cli"]["files"].pop()
            plan.write_text(json.dumps(tampered), encoding="utf-8")
            rejected = subprocess.run(
                [
                    sys.executable, script, "verify-all", "--plan", str(plan),
                    "--transaction-root", str(transaction_root),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("plan", rejected.stderr.lower())


class ScopedPlanSelectionTests(unittest.TestCase):
    SELECTED_TWO = (
        "openspec-superpower-change:references/cross-cli-sync.md",
        "openspec-superpower-change:SKILL.md",
    )

    def test_cli_exposes_scoped_selector_options(self):
        result = subprocess.run(
            [sys.executable, str(Path(sync.__file__)), "plan", "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--select-file", result.stdout)
        self.assertIn("--select-managed-rule", result.stdout)

    def test_cli_generates_v2_and_rejects_invalid_selection_before_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_scoped_v6_sync_fixture(Path(tmp), self.SELECTED_TWO)
            output = Path(tmp) / "cli-scoped.json"
            result = subprocess.run(
                scoped_plan_cli_command(
                    fixture,
                    output,
                    reversed(self.SELECTED_TWO),
                ),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.is_file())
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o600)
            planned = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(planned["schema_version"], 2)
            bad_output = Path(tmp) / "cli-invalid.json"
            bad_result = subprocess.run(
                scoped_plan_cli_command(
                    fixture,
                    bad_output,
                    ("openspec-superpower-change:unknown.md",),
                ),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(bad_result.returncode, 0)
            self.assertFalse(bad_output.exists())

    def test_cli_rejects_unsafe_selector_without_echoing_raw_value(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_scoped_v6_sync_fixture(Path(tmp), self.SELECTED_TWO)
            sentinel = "PRIVATE-SELECTOR-SENTINEL-9f1e"
            selector = f"openspec-superpower-change:https://{sentinel}.invalid"
            output = Path(tmp) / "unsafe-selector.json"
            result = subprocess.run(
                scoped_plan_cli_command(fixture, output, (selector,)),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())
            self.assertNotIn(sentinel, result.stderr)
            self.assertNotIn(selector, result.stderr)

    def test_two_selected_files_become_operations_and_rest_assertions(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_scoped_v6_sync_fixture(
                Path(tmp), self.SELECTED_TWO
            )
            plan = sync.generate_plan(
                _scoped_args(fixture, self.SELECTED_TWO)
            )
            self.assertEqual(plan["schema_version"], 2)
            self.assertEqual(
                set(plan),
                {
                    "schema_version",
                    "manifest_path",
                    "manifest_sha256",
                    "sources",
                    "selection",
                    "managed_rules",
                    "targets",
                },
            )
            expected_selected = [
                ("openspec-superpower-change", "SKILL.md"),
                ("openspec-superpower-change", "references/cross-cli-sync.md"),
            ]
            expected_assertions = [
                ("openspec-superpower-change", "scripts/validate_core_gates.py"),
                ("codex-brief-antigravity-review", "SKILL.md"),
            ]
            self.assertEqual(
                plan["selection"],
                {
                    "files": [
                        {"skill": skill, "path": path}
                        for skill, path in expected_selected
                    ],
                    "managed_rule": False,
                },
            )
            for target_id in sync.TARGET_ORDER:
                target = plan["targets"][target_id]
                self.assertEqual(
                    [(item["skill"], item["path"]) for item in target["files"]],
                    expected_selected,
                )
                self.assertEqual(
                    [(item["skill"], item["path"]) for item in target["assertions"]],
                    expected_assertions,
                )
                self.assertEqual(len(target["files"]), 2)
                self.assertEqual(len(target["assertions"]), 2)
                self.assertNotIn("rule_file", target)
                self.assertNotIn("rule_pre_state", target)
                self.assertEqual(
                    set(target["managed_rule"]),
                    {"selected", "destination", "pre_state"},
                )
                self.assertFalse(target["managed_rule"]["selected"])
            candidate_entries = sync._target_candidate_entries(plan, "codex")
            self.assertEqual(
                [entry["label"] for entry in candidate_entries],
                [
                    "openspec-superpower-change/SKILL.md",
                    "openspec-superpower-change/references/cross-cli-sync.md",
                ],
            )

    def test_managed_rule_is_selected_only_when_explicitly_requested(self):
        with tempfile.TemporaryDirectory() as tmp:
            selected = ("openspec-superpower-change:SKILL.md",)
            fixture = create_scoped_v6_sync_fixture(Path(tmp), selected)
            plan = sync.generate_plan(
                _scoped_args(
                    fixture,
                    selected,
                    select_managed_rule=True,
                )
            )
            self.assertEqual(plan["schema_version"], 2)
            self.assertEqual(
                plan["selection"],
                {
                    "files": [
                        {
                            "skill": "openspec-superpower-change",
                            "path": "SKILL.md",
                        }
                    ],
                    "managed_rule": True,
                },
            )
            for target in plan["targets"].values():
                self.assertEqual(len(target["files"]), 1)
                self.assertEqual(len(target["assertions"]), 3)
                self.assertTrue(target["managed_rule"]["selected"])
            candidate_entries = sync._target_candidate_entries(plan, "codex")
            self.assertEqual(
                [entry["label"] for entry in candidate_entries],
                ["openspec-superpower-change/SKILL.md", "global-rule"],
            )

    def test_invalid_scoped_selectors_fail_before_plan_creation(self):
        invalid = (
            ("",),
            ("openspec-superpower-change:SKILL.md", "openspec-superpower-change:SKILL.md"),
            ("unknown-skill:SKILL.md",),
            ("openspec-superpower-change:../SKILL.md",),
            ("openspec-superpower-change:auth/token.json",),
            ("openspec-superpower-change:not-in-manifest.md",),
        )
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_scoped_v6_sync_fixture(Path(tmp), self.SELECTED_TWO)
            for selectors in invalid:
                with self.subTest(selectors=selectors):
                    with self.assertRaises(ValueError):
                        sync.generate_plan(_scoped_args(fixture, selectors))

    def test_non_v6_or_target_incomplete_manifest_is_rejected_for_scoped_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_scoped_v6_sync_fixture(Path(tmp), self.SELECTED_TWO)
            manifest_path = fixture["plan_path"].parent / "manifest.json"
            for label, manifest in (
                ("non-v6", portable_manifest()),
                ("target-incomplete", portable_manifest_v6()),
            ):
                with self.subTest(label=label):
                    if label == "target-incomplete":
                        manifest["skills"][0]["files"][0]["targets"] = list(
                            sync.TARGET_ORDER[:-1]
                        )
                    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                    with self.assertRaises(ValueError):
                        sync.generate_plan(
                            _scoped_args(
                                fixture,
                                ("openspec-superpower-change:SKILL.md",),
                            )
                        )

    def test_generation_rejects_stale_unselected_assertion_before_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_scoped_v6_sync_fixture(Path(tmp), self.SELECTED_TWO)
            plan = fixture["plan"]
            assertion = next(
                item
                for item in plan["targets"]["codex"]["files"]
                if item["path"] == "scripts/validate_core_gates.py"
            )
            destination = Path(assertion["destination"])
            destination.write_bytes(b"generation-assertion-drift\n")
            output = Path(tmp) / "stale-assertion-plan.json"
            result = subprocess.run(
                scoped_plan_cli_command(fixture, output, self.SELECTED_TWO),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())
            self.assertEqual(destination.read_bytes(), b"generation-assertion-drift\n")

    def test_generation_rejects_stale_unselected_rule_before_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_scoped_v6_sync_fixture(Path(tmp), self.SELECTED_TWO)
            rule = Path(fixture["plan"]["targets"]["codex"]["rule_file"])
            rule.write_bytes(b"generation-rule-drift\n")
            output = Path(tmp) / "stale-rule-plan.json"
            result = subprocess.run(
                scoped_plan_cli_command(fixture, output, self.SELECTED_TWO),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())
            self.assertEqual(rule.read_bytes(), b"generation-rule-drift\n")

    def test_generation_rejects_noncanonical_managed_rule_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            selected = ("openspec-superpower-change:SKILL.md",)
            fixture = create_scoped_v6_sync_fixture(root, selected)
            replacement = root / "codex" / "ordinary.txt"
            replacement.write_bytes(b"ordinary-file\n")
            args = _scoped_args(
                fixture, selected, select_managed_rule=True
            )
            args.codex_rule_file = replacement
            with self.assertRaisesRegex(ValueError, "global rule destination"):
                sync.generate_plan(args)
            self.assertEqual(replacement.read_bytes(), b"ordinary-file\n")


class ScopedPlanTamperTests(unittest.TestCase):
    SELECTED = (
        "openspec-superpower-change:SKILL.md",
        "openspec-superpower-change:references/cross-cli-sync.md",
    )

    def _validated_plan(self, root: Path) -> dict:
        fixture = create_scoped_v6_sync_fixture(root, self.SELECTED)
        plan = make_scoped_plan(fixture, self.SELECTED)
        self.assertEqual(plan["schema_version"], 2)
        try:
            validated = sync._validate_plan(plan)
        except ValueError as exc:
            self.fail(f"scoped v2 baseline is not accepted: {exc}")
        self.assertEqual(validated, plan)
        return plan

    def _assert_tamper_rejected(self, plan: dict, mutate) -> None:
        tampered = json.loads(json.dumps(plan))
        mutate(tampered)
        with self.assertRaises(ValueError):
            sync._validate_plan(tampered)

    def test_selection_partition_destination_hash_and_prestate_tamper_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mutations = {
                "selection": lambda plan: plan["selection"]["files"].append(
                    {
                        "skill": "openspec-superpower-change",
                        "path": "scripts/validate_core_gates.py",
                    }
                ),
                "partition": lambda plan: plan["targets"]["codex"]["files"].append(
                    plan["targets"]["codex"]["assertions"].pop()
                ),
                "destination": lambda plan: plan["targets"]["codex"]["files"][0].update(
                    {"destination": "/tmp/not-a-skill-destination"}
                ),
                "hash": lambda plan: plan["targets"]["codex"]["files"][0].update(
                    {"sha256": "0" * 64}
                ),
                "prestate": lambda plan: plan["targets"]["codex"]["files"][0].update(
                    {
                        "pre_state": {
                            "kind": "file",
                            "sha256": "not-a-sha256",
                            "mode": 0o644,
                        }
                    }
                ),
            }
            for label, mutation in mutations.items():
                with self.subTest(label=label):
                    plan = self._validated_plan(root / label)
                    self._assert_tamper_rejected(plan, mutation)

    def test_managed_rule_selection_tamper_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = self._validated_plan(Path(tmp))
            self._assert_tamper_rejected(
                plan,
                lambda value: value["targets"]["codex"]["managed_rule"].update(
                    {"selected": True}
                ),
            )

    def test_managed_rule_destination_and_prestate_tamper_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            selected = ("openspec-superpower-change:SKILL.md",)
            fixture = create_scoped_v6_sync_fixture(root, selected)
            plan = make_scoped_plan(
                fixture, selected, select_managed_rule=True
            )
            resolved_root = root.resolve()
            expected_rules = {
                "codex": resolved_root / "codex" / "AGENTS.md",
                "pi": resolved_root / "pi" / "APPEND_SYSTEM.md",
                "antigravity-cli": resolved_root / "GEMINI.md",
                "grok-cli": resolved_root / "grok-cli" / "AGENTS.md",
            }
            for target_id, expected in expected_rules.items():
                target = plan["targets"][target_id]
                skills_root = Path(target["skills_root"])
                self.assertEqual(
                    Path(target["managed_rule"]["destination"]), expected
                )
                self.assertEqual(
                    sync._canonical_rule_destination(target_id, skills_root),
                    expected,
                )
            replacement = root / "codex" / "ordinary.txt"
            replacement.write_bytes(b"ordinary-file\\n")
            target = plan["targets"]["codex"]
            target["managed_rule"]["destination"] = str(replacement)
            target["managed_rule"]["pre_state"] = sync.capture_destination_prestate(
                replacement
            )
            with self.assertRaises(ValueError):
                sync._validate_plan(plan)
            with self.assertRaises(ValueError):
                sync._target_candidate_entries(plan, "codex")
            transaction_root = root / "transactions"
            transaction_root.mkdir(mode=0o700, exist_ok=True)
            receipt = transaction_root / "codex.json"
            with self.assertRaises(ValueError):
                sync.apply_target(
                    plan,
                    "codex",
                    root / "backups",
                    receipt,
                    plan_sha256="0" * 64,
                )
            self.assertFalse(receipt.exists())
            self.assertFalse((root / "backups").exists())
            self.assertEqual(replacement.read_bytes(), b"ordinary-file\\n")


class ScopedTransactionTests(unittest.TestCase):
    SELECTED = (
        "openspec-superpower-change:SKILL.md",
        "openspec-superpower-change:references/cross-cli-sync.md",
    )

    def _runtime_fixture(self, root: Path):
        fixture = create_scoped_v6_sync_fixture(root, self.SELECTED)
        plan = make_scoped_plan(fixture, self.SELECTED)
        self.assertEqual(plan["schema_version"], 2)
        try:
            validated = sync._validate_plan(plan)
        except ValueError as exc:
            self.fail(f"scoped v2 baseline is not accepted: {exc}")
        self.assertEqual(validated, plan)
        plan_path = write_plan_file(fixture, plan)
        return fixture, plan, plan_path

    def test_selected_prestate_drift_blocks_before_backup_or_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture, plan, plan_path = self._runtime_fixture(Path(tmp))
            target = plan["targets"]["codex"]
            selected_destination = Path(target["files"][0]["destination"])
            selected_destination.parent.mkdir(parents=True, exist_ok=True)
            selected_destination.write_text("selected-prestate-drift\n", encoding="utf-8")
            backup_root = Path(tmp) / "backups"
            receipt = Path(tmp) / "transactions" / "codex.json"
            with self.assertRaisesRegex(ValueError, "pre-state drift"):
                sync.apply_target(
                    plan,
                    "codex",
                    backup_root,
                    receipt,
                    plan_sha256=sync._sha256(plan_path),
                )
            self.assertFalse(receipt.exists())
            self.assertFalse(backup_root.exists())
            self.assertEqual(
                selected_destination.read_text(encoding="utf-8"),
                "selected-prestate-drift\n",
            )

    def test_unselected_assertion_drift_blocks_and_preserves_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture, plan, plan_path = self._runtime_fixture(Path(tmp))
            target = plan["targets"]["codex"]
            assertion = target["assertions"][0]
            destination = Path(assertion["destination"])
            original = destination.read_bytes()
            destination.write_bytes(b"assertion-drift\n")
            backup_root = Path(tmp) / "backups"
            receipt = Path(tmp) / "transactions" / "codex.json"
            with self.assertRaisesRegex(ValueError, "pre-state drift"):
                sync.apply_target(
                    plan,
                    "codex",
                    backup_root,
                    receipt,
                    plan_sha256=sync._sha256(plan_path),
                )
            self.assertFalse(receipt.exists())
            self.assertFalse(backup_root.exists())
            self.assertNotEqual(destination.read_bytes(), original)
            self.assertEqual(destination.read_bytes(), b"assertion-drift\n")

    def test_unselected_managed_rule_drift_blocks_and_preserves_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture, plan, plan_path = self._runtime_fixture(Path(tmp))
            target = plan["targets"]["codex"]
            destination = Path(target["managed_rule"]["destination"])
            original = destination.read_bytes()
            destination.write_bytes(b"rule-drift\n")
            backup_root = Path(tmp) / "backups"
            receipt = Path(tmp) / "transactions" / "codex.json"
            with self.assertRaisesRegex(ValueError, "pre-state drift"):
                sync.apply_target(
                    plan,
                    "codex",
                    backup_root,
                    receipt,
                    plan_sha256=sync._sha256(plan_path),
                )
            self.assertFalse(receipt.exists())
            self.assertFalse(backup_root.exists())
            self.assertNotEqual(destination.read_bytes(), original)
            self.assertEqual(destination.read_bytes(), b"rule-drift\n")

    def test_scoped_round_trip_verifies_full_closure_and_preserves_unselected_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture, plan, plan_path = self._runtime_fixture(Path(tmp))
            root = Path(tmp)
            transaction_root = root / "transactions"
            backup_root = root / "backups"
            plan_sha256 = sync._sha256(plan_path)
            snapshots = {}
            for target_id in sync.TARGET_ORDER:
                target = plan["targets"][target_id]
                snapshots[target_id] = {
                    "assertions": {
                        item["path"]: Path(item["destination"]).read_bytes()
                        for item in target["assertions"]
                    },
                    "rule": Path(target["managed_rule"]["destination"]).read_bytes(),
                }
            for target_id in sync.TARGET_ORDER:
                receipt = transaction_root / f"{target_id}.json"
                applied = sync.apply_target(
                    plan,
                    target_id,
                    backup_root,
                    receipt,
                    plan_sha256=plan_sha256,
                )
                self.assertEqual(applied["state"], "applied-uncommitted")
                self.assertEqual(
                    sync.verify_target_with_receipt(
                        plan,
                        target_id,
                        receipt,
                        plan_sha256=plan_sha256,
                    ),
                    {"verify": "pass", "target": target_id},
                )
                if target_id == "grok-cli":
                    inspect_json = transaction_root / "grok-inspect.json"
                    inspect_json.write_text(
                        json.dumps(
                            {
                                "skills": [
                                    {
                                        "name": name,
                                        "source": {
                                            "type": "user",
                                            "path": f"{plan['targets'][target_id]['skills_root']}/{name}/SKILL.md",
                                        },
                                    }
                                    for name in SKILLS
                                ]
                            }
                        ),
                        encoding="utf-8",
                    )
                    inspect_json.chmod(0o600)
                    discovery = sync.verify_discovery_with_receipt(
                        plan,
                        target_id,
                        receipt,
                        plan_sha256=plan_sha256,
                        inspect_json=inspect_json,
                        consume=True,
                    )
                    self.assertFalse(inspect_json.exists())
                else:
                    discovery = sync.verify_discovery_with_receipt(
                        plan,
                        target_id,
                        receipt,
                        plan_sha256=plan_sha256,
                    )
                self.assertEqual(discovery, {"discovery": "pass", "target": target_id, "consumed": target_id == "grok-cli"})
                self.assertEqual(
                    sync.commit_target(
                        plan,
                        target_id,
                        receipt,
                        plan_sha256=plan_sha256,
                    ),
                    {"commit": "pass", "target": target_id},
                )
                backup_manifest = json.loads(
                    (backup_root / target_id / "manifest.json").read_text(encoding="utf-8")
                )
                self.assertEqual(len(backup_manifest["entries"]), 2)
                self.assertTrue(
                    all(entry["label"] != "global-rule" for entry in backup_manifest["entries"])
                )
            self.assertEqual(
                sync.verify_all_receipts(
                    plan,
                    transaction_root,
                    plan_sha256=plan_sha256,
                ),
                {"verify_all": "pass", "targets": list(sync.TARGET_ORDER)},
            )
            for target_id, snapshot in snapshots.items():
                target = plan["targets"][target_id]
                for item in target["assertions"]:
                    self.assertEqual(
                        Path(item["destination"]).read_bytes(),
                        snapshot["assertions"][item["path"]],
                    )
                self.assertEqual(
                    Path(target["managed_rule"]["destination"]).read_bytes(),
                    snapshot["rule"],
                )

    def test_restore_restores_selected_only_and_blocks_later_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture, plan, plan_path = self._runtime_fixture(Path(tmp))
            root = Path(tmp)
            transaction_root = root / "transactions"
            backup_root = root / "backups"
            plan_sha256 = sync._sha256(plan_path)
            target = plan["targets"]["codex"]
            assertions = {
                item["path"]: Path(item["destination"]).read_bytes()
                for item in target["assertions"]
            }
            rule_path = Path(target["managed_rule"]["destination"])
            rule_bytes = rule_path.read_bytes()
            receipt = transaction_root / "codex.json"
            sync.apply_target(plan, "codex", backup_root, receipt, plan_sha256=plan_sha256)
            restored = sync.restore_target(
                plan,
                "codex",
                backup_root,
                receipt,
                plan_sha256=plan_sha256,
            )
            self.assertEqual(
                restored,
                {
                    "restore": "pass",
                    "target": "codex",
                    "restored": True,
                    "later_targets_started": False,
                },
            )
            for item in target["files"]:
                self.assertFalse(Path(item["destination"]).exists())
            for item in target["assertions"]:
                self.assertEqual(Path(item["destination"]).read_bytes(), assertions[item["path"]])
            self.assertEqual(rule_path.read_bytes(), rule_bytes)
            with self.assertRaisesRegex(ValueError, "prior target is not verified"):
                sync.apply_target(
                    plan,
                    "pi",
                    backup_root,
                    transaction_root / "pi.json",
                    plan_sha256=plan_sha256,
                )

    def test_recover_pending_restores_selected_only_and_blocks_later_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture, plan, plan_path = self._runtime_fixture(Path(tmp))
            root = Path(tmp)
            transaction_root = root / "transactions"
            backup_root = root / "backups"
            plan_sha256 = sync._sha256(plan_path)
            target = plan["targets"]["codex"]
            assertions = {
                item["path"]: Path(item["destination"]).read_bytes()
                for item in target["assertions"]
            }
            rule_path = Path(target["managed_rule"]["destination"])
            rule_bytes = rule_path.read_bytes()
            receipt = transaction_root / "codex.json"
            sync.apply_target(plan, "codex", backup_root, receipt, plan_sha256=plan_sha256)
            recovered = sync.recover_pending(
                plan,
                backup_root,
                transaction_root,
                plan_sha256=plan_sha256,
            )
            self.assertEqual(
                recovered,
                {
                    "recovery": "pass",
                    "target": "codex",
                    "restored": True,
                    "later_targets_started": False,
                },
            )
            for item in target["files"]:
                self.assertFalse(Path(item["destination"]).exists())
            for item in target["assertions"]:
                self.assertEqual(Path(item["destination"]).read_bytes(), assertions[item["path"]])
            self.assertEqual(rule_path.read_bytes(), rule_bytes)
            with self.assertRaisesRegex(ValueError, "prior target is not verified"):
                sync.apply_target(
                    plan,
                    "pi",
                    backup_root,
                    transaction_root / "pi.json",
                    plan_sha256=plan_sha256,
                )


class RoleFirstV6CrossCliRedTests(unittest.TestCase):
    @staticmethod
    def _pass_result() -> dict:
        return {
            "pi_probe": "pass",
            "reviewer_identity": {
                "product": "pi",
                "role": "independent-reviewer",
                "capability_profile": "control-plane-high",
            },
            "bound_input_hashes": {},
            "verdict": "PASS",
            "findings": [],
        }

    def _pi_persistence_fixture(self, root: Path) -> tuple[Path, Path, dict]:
        evidence = root / "evidence"
        evidence.mkdir(mode=0o700)
        output = evidence / "pi-review.json"
        return evidence, output, self._pass_result()

    def test_pi_candidate_substitution_before_install_never_accepts_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence, output, result = self._pi_persistence_fixture(Path(tmp))
            original_rename = sync._renameatx
            injected = False

            def substitute_candidate(source, destination, flags, **kwargs):
                nonlocal injected
                candidate = evidence / Path(source).name
                if (
                    not injected
                    and Path(destination).name == output.name
                    and flags == sync.RENAME_EXCL
                    and candidate.exists()
                ):
                    candidate.unlink()
                    unrelated = evidence / "unrelated-pi-candidate"
                    unrelated.write_bytes(b"unrelated\n")
                    unrelated.chmod(0o600)
                    unrelated.rename(candidate)
                    injected = True
                return original_rename(source, destination, flags, **kwargs)

            with mock.patch.object(sync, "_renameatx", side_effect=substitute_candidate):
                with self.assertRaisesRegex(ValueError, "candidate|persistence|ambiguous"):
                    sync._persist_pi_probe_result(SimpleNamespace(output=output), result)

            self.assertTrue(injected)
            self.assertFalse(output.exists())
            survivors = [path for path in evidence.iterdir() if path != output]
            self.assertTrue(survivors)
            self.assertTrue(any(path.read_bytes() == b"unrelated\n" for path in survivors))
            self.assertFalse(any(path.name.startswith(".cross-cli-sync.") for path in survivors))

    def test_pi_post_install_destination_mismatch_restores_unrelated_object(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence, output, result = self._pi_persistence_fixture(Path(tmp))
            original_rename = sync._renameatx
            injected = False

            def substitute_destination(source, destination, flags, **kwargs):
                nonlocal injected
                value = original_rename(source, destination, flags, **kwargs)
                if (
                    not injected
                    and Path(destination).name == output.name
                    and flags == sync.RENAME_EXCL
                ):
                    output.unlink()
                    unrelated = evidence / "unrelated-pi-destination"
                    unrelated.write_bytes(b"unrelated\n")
                    unrelated.chmod(0o600)
                    unrelated.rename(output)
                    injected = True
                return value

            with mock.patch.object(sync, "_renameatx", side_effect=substitute_destination):
                with self.assertRaisesRegex(ValueError, "candidate|persistence|ambiguous"):
                    sync._persist_pi_probe_result(SimpleNamespace(output=output), result)

            self.assertTrue(injected)
            self.assertFalse(output.exists())
            survivors = [path for path in evidence.iterdir() if path != output]
            self.assertTrue(survivors)
            self.assertTrue(any(path.read_bytes() == b"unrelated\n" for path in survivors))
            self.assertFalse(any(path.name.startswith(".cross-cli-sync.") for path in survivors))

    def test_pi_descriptor_binding_rejects_same_inode_mutation_after_first_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "candidate"
            target.write_bytes(b"stable\n")
            original_hash = sync._sha256_descriptor
            calls = 0

            def mutate_after_first(descriptor):
                nonlocal calls
                digest = original_hash(descriptor)
                calls += 1
                if calls == 1:
                    mutator = os.open(target, os.O_RDWR)
                    try:
                        os.ftruncate(mutator, 0)
                        os.write(mutator, b"mutated-after-first\n")
                    finally:
                        os.close(mutator)
                return digest

            with sync._verified_parent(target, "binding-test") as guard:
                with mock.patch.object(sync, "_sha256_descriptor", side_effect=mutate_after_first):
                    with self.assertRaisesRegex(ValueError, "binding|changed|drift"):
                        sync._open_guarded_binding(guard, target.name, "binding-test")
            self.assertEqual(calls, 2)
            self.assertEqual(target.read_bytes(), b"mutated-after-first\n")

    def test_pi_descriptor_binding_rejects_same_inode_mutation_after_second_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "candidate"
            target.write_bytes(b"stable\n")
            original_hash = sync._sha256_descriptor
            calls = 0

            def mutate_after_second(descriptor):
                nonlocal calls
                digest = original_hash(descriptor)
                calls += 1
                if calls == 2:
                    mutator = os.open(target, os.O_RDWR)
                    try:
                        os.ftruncate(mutator, 0)
                        os.write(mutator, b"mutated-after-second\n")
                    finally:
                        os.close(mutator)
                return digest

            with sync._verified_parent(target, "binding-test") as guard:
                with mock.patch.object(sync, "_sha256_descriptor", side_effect=mutate_after_second):
                    with self.assertRaisesRegex(ValueError, "binding|changed|drift"):
                        sync._open_guarded_binding(guard, target.name, "binding-test")
            self.assertEqual(calls, 2)
            self.assertEqual(target.read_bytes(), b"mutated-after-second\n")

    def test_pi_binding_identity_rejects_ctime_only_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "candidate"
            target.write_bytes(b"stable\n")
            with sync._verified_parent(target, "ctime binding test") as guard:
                binding = sync._open_guarded_binding(
                    guard, target.name, "ctime binding test"
                )
            try:
                mismatched = dict(binding)
                mismatched["ctime_ns"] += 1
                self.assertFalse(sync._binding_identity_matches(binding, mismatched))
            finally:
                os.close(binding["fd"])

    def test_pi_rewrite_rejects_same_inode_mutation_immediately_before_rewrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence, output, result = self._pi_persistence_fixture(root)
            output.write_bytes(sync._canonical_json_bytes(result))
            output.chmod(0o600)
            expected = sync.capture_destination_prestate(output)
            blocked = sync._canonical_json_bytes(sync._blocked_pi_probe_result())
            original_identity = sync._guarded_identity_matches
            mutated = False

            def mutate_after_identity(guard, name, ownership):
                nonlocal mutated
                value = original_identity(guard, name, ownership)
                if value and not mutated:
                    descriptor = os.open(name, os.O_WRONLY, dir_fd=guard["fd"])
                    try:
                        os.ftruncate(descriptor, 0)
                        os.write(descriptor, b"same-inode-drift\n")
                        os.fsync(descriptor)
                    finally:
                        os.close(descriptor)
                    mutated = True
                return value

            with sync._verified_parent(output, "Pi rewrite test") as guard:
                ownership = {
                    "device": output.stat().st_dev,
                    "inode": output.stat().st_ino,
                    "type": stat.S_IFREG,
                    "sha256": expected["sha256"],
                    "mode": 0o600,
                    "uid": output.stat().st_uid,
                    "gid": output.stat().st_gid,
                    "nlink": output.stat().st_nlink,
                    "size": output.stat().st_size,
                    "mtime_ns": output.stat().st_mtime_ns,
                    "ctime_ns": output.stat().st_ctime_ns,
                }
                with mock.patch.object(
                    sync, "_guarded_identity_matches", side_effect=mutate_after_identity
                ):
                    with self.assertRaisesRegex(ValueError, "ambiguous|changed|drift"):
                        sync._rewrite_guarded_pi_evidence(
                            guard,
                            output.name,
                            expected,
                            blocked,
                            "Pi rewrite test",
                            ownership=ownership,
                        )

            self.assertTrue(mutated)
            self.assertFalse(output.exists())
            unsafe = list(evidence.glob(f"{output.name}.persistence-unsafe.*"))
            self.assertTrue(unsafe)
            self.assertTrue(
                any(path.read_bytes() == b"same-inode-drift\n" for path in unsafe)
            )
            blocked = list(evidence.glob(f"{output.name}.persistence-blocked.*"))
            self.assertTrue(blocked)
            self.assertTrue(
                all(
                    json.loads(path.read_text(encoding="utf-8"))["verdict"] == "BLOCKED"
                    for path in blocked
                )
            )

    def test_pi_rewrite_does_not_overwrite_after_final_stable_check_race(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence, output, result = self._pi_persistence_fixture(root)
            output.write_bytes(sync._canonical_json_bytes(result))
            output.chmod(0o600)
            expected = sync.capture_destination_prestate(output)
            blocked = sync._canonical_json_bytes(sync._blocked_pi_probe_result())
            original_stable = sync._stable_binding_matches
            calls = 0
            mutated = False

            def mutate_after_final_stable(
                descriptor,
                ownership,
                label,
                *,
                expected=None,
                allow_rename_ctime=False,
            ):
                nonlocal calls, mutated
                value = original_stable(
                    descriptor,
                    ownership,
                    label,
                    expected=expected,
                    allow_rename_ctime=allow_rename_ctime,
                )
                calls += 1
                if value and calls == 2:
                    mutator = os.open(output, os.O_WRONLY)
                    try:
                        os.ftruncate(mutator, 0)
                        os.write(mutator, b"same-inode-after-final-stable\n")
                        os.fsync(mutator)
                    finally:
                        os.close(mutator)
                    mutated = True
                return value

            with sync._verified_parent(output, "Pi rewrite race test") as guard:
                ownership = sync._open_guarded_binding(
                    guard, output.name, "Pi rewrite race test"
                )
                try:
                    with mock.patch.object(
                        sync,
                        "_stable_binding_matches",
                        side_effect=mutate_after_final_stable,
                    ):
                        with self.assertRaisesRegex(ValueError, "ambiguous|changed|drift"):
                            sync._rewrite_guarded_pi_evidence(
                                guard,
                                output.name,
                                expected,
                                blocked,
                                "Pi rewrite race test",
                                ownership=ownership,
                            )
                finally:
                    os.close(ownership["fd"])

            self.assertTrue(mutated)
            self.assertGreaterEqual(calls, 2)
            survivors = list(evidence.iterdir())
            self.assertFalse(output.exists() and output.read_bytes() == blocked)
            self.assertTrue(
                any(path.read_bytes() == b"same-inode-after-final-stable\n" for path in survivors)
            )
            self.assertFalse(any(path.name.startswith(".cross-cli-sync.") for path in survivors))

    def test_pi_blocked_recovery_rejects_post_bind_name_substitution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence, output, result = self._pi_persistence_fixture(root)
            blocked = sync._canonical_json_bytes(sync._blocked_pi_probe_result())
            original_require = sync._require_retained_binding
            injected = False

            def substitute_after_bind(
                guard,
                name,
                ownership,
                label,
                *,
                expected=None,
                allow_rename_ctime=False,
            ):
                nonlocal injected
                value = original_require(
                    guard,
                    name,
                    ownership,
                    label,
                    expected=expected,
                    allow_rename_ctime=allow_rename_ctime,
                )
                if (
                    not injected
                    and name.startswith(f"{output.name}.persistence-blocked.")
                    and value is None
                ):
                    replacement = evidence / name
                    replacement.unlink()
                    unrelated = evidence / "unrelated-blocked-recovery"
                    unrelated.write_bytes(sync._canonical_json_bytes(result))
                    unrelated.chmod(0o600)
                    unrelated.rename(replacement)
                    injected = True
                return value

            with sync._verified_parent(output, "Pi blocked recovery test") as guard:
                with mock.patch.object(
                    sync,
                    "_require_retained_binding",
                    side_effect=substitute_after_bind,
                ):
                    with self.assertRaisesRegex(ValueError, "blocked|ambiguous|drift"):
                        sync._create_pi_blocked_recovery(
                            guard, output.name, blocked, "Pi blocked recovery test"
                        )

            self.assertTrue(injected)
            self.assertFalse(
                any(
                    path.name.startswith(f"{output.name}.persistence-blocked.")
                    and path.read_bytes() != blocked
                    for path in evidence.iterdir()
                )
            )
            unsafe = list(evidence.glob(f"{output.name}.persistence-unsafe.*"))
            self.assertTrue(unsafe)
            self.assertTrue(any(path.read_bytes() != blocked for path in unsafe))

    def test_pi_unsafe_cleanup_preserves_substitution_after_retained_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence, output, result = self._pi_persistence_fixture(root)
            unsafe_name = f"{output.name}.persistence-unsafe.fixed"
            unsafe_path = evidence / unsafe_name
            original_bytes = b"original-pass\n"
            unsafe_path.write_bytes(original_bytes)
            unsafe_path.chmod(0o600)
            unrelated_bytes = b"unrelated-after-check\n"
            original_retain = sync._retained_binding_matches_name
            injected = False

            with sync._verified_parent(output, "Pi unsafe cleanup race") as guard:
                ownership = sync._open_guarded_binding(
                    guard, unsafe_name, "Pi unsafe cleanup race"
                )
                try:
                    expected = sync._binding_prestate(ownership)

                    def substitute_after_check(
                        check_guard, name, check_ownership, label, *, expected=None,
                        allow_rename_ctime=False,
                    ):
                        nonlocal injected
                        if allow_rename_ctime:
                            value = original_retain(
                                check_guard,
                                name,
                                check_ownership,
                                label,
                                expected=expected,
                                allow_rename_ctime=True,
                            )
                        else:
                            value = original_retain(
                                check_guard,
                                name,
                                check_ownership,
                                label,
                                expected=expected,
                            )
                        if value and name == unsafe_name and not injected:
                            unsafe_path.unlink()
                            replacement = evidence / "unrelated-unsafe-cleanup"
                            replacement.write_bytes(unrelated_bytes)
                            replacement.chmod(0o600)
                            replacement.rename(unsafe_path)
                            injected = True
                        return value

                    with mock.patch.object(
                        sync,
                        "_retained_binding_matches_name",
                        side_effect=substitute_after_check,
                    ):
                        sync._remove_exact_pi_unsafe_entry(
                            guard,
                            unsafe_name,
                            ownership,
                            expected,
                            "Pi unsafe cleanup race",
                        )
                finally:
                    os.close(ownership["fd"])

            self.assertTrue(injected)
            survivors = list(evidence.iterdir())
            self.assertTrue(
                any(path.read_bytes() == unrelated_bytes for path in survivors)
            )
            self.assertFalse(any(path.name.startswith(".cross-cli-sync.") for path in survivors))

    def test_pi_unsafe_cleanup_rechecks_before_unlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence, output, result = self._pi_persistence_fixture(root)
            unsafe_name = f"{output.name}.persistence-unsafe.fixed"
            unsafe_path = evidence / unsafe_name
            unsafe_path.write_bytes(b"original-pass\n")
            unsafe_path.chmod(0o600)
            unrelated_bytes = b"unrelated-after-pi-unlink-check\n"
            original_unlink = sync._guarded_unlink
            injected = False

            with sync._verified_parent(output, "Pi unsafe unlink race") as guard:
                ownership = sync._open_guarded_binding(
                    guard, unsafe_name, "Pi unsafe unlink race"
                )
                try:
                    expected = sync._binding_prestate(ownership)

                    def substitute_before_unlink(unlink_guard, name, *, missing_ok=False):
                        nonlocal injected
                        if not injected and name.startswith(
                            f"{output.name}.persistence-cleanup."
                        ):
                            cleanup = evidence / name
                            cleanup.unlink()
                            replacement = evidence / "unrelated-pi-cleanup"
                            replacement.write_bytes(unrelated_bytes)
                            replacement.chmod(0o600)
                            replacement.rename(cleanup)
                            injected = True
                        return original_unlink(
                            unlink_guard, name, missing_ok=missing_ok
                        )

                    with mock.patch.object(
                        sync, "_guarded_unlink", side_effect=substitute_before_unlink
                    ):
                        sync._remove_exact_pi_unsafe_entry(
                            guard,
                            unsafe_name,
                            ownership,
                            expected,
                            "Pi unsafe unlink race",
                        )
                finally:
                    os.close(ownership["fd"])

            self.assertTrue(injected)
            survivors = list(evidence.iterdir())
            self.assertTrue(any(path.read_bytes() == unrelated_bytes for path in survivors))
            self.assertFalse(any(path.name.startswith(".cross-cli-sync.") for path in survivors))

    def test_pi_unsafe_cleanup_quarantines_after_rebind_race(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence, output, result = self._pi_persistence_fixture(root)
            unsafe_name = f"{output.name}.persistence-unsafe.fixed"
            unsafe_path = evidence / unsafe_name
            unsafe_path.write_bytes(b"original-pass\n")
            unsafe_path.chmod(0o600)
            unrelated_bytes = b"unrelated-after-pi-rebind\n"
            original_rebind = sync._rebind_before_unlink
            injected = False

            with sync._verified_parent(output, "Pi post-rebind unlink race") as guard:
                ownership = sync._open_guarded_binding(
                    guard, unsafe_name, "Pi post-rebind unlink race"
                )
                try:
                    expected = sync._binding_prestate(ownership)

                    def move_retained_and_replace_name(check_guard, name, context):
                        nonlocal injected
                        result = original_rebind(check_guard, name, context)
                        if not injected:
                            cleanup = evidence / name
                            retained_aside = evidence / "pi-retained-aside"
                            cleanup.rename(retained_aside)
                            unrelated = evidence / "unrelated-pi-post-rebind"
                            unrelated.write_bytes(unrelated_bytes)
                            unrelated.chmod(0o600)
                            unrelated.rename(cleanup)
                            injected = True
                        return result

                    with mock.patch.object(
                        sync,
                        "_rebind_before_unlink",
                        side_effect=move_retained_and_replace_name,
                    ):
                        sync._remove_exact_pi_unsafe_entry(
                            guard,
                            unsafe_name,
                            ownership,
                            expected,
                            "Pi post-rebind unlink race",
                        )
                finally:
                    os.close(ownership["fd"])

            self.assertTrue(injected)
            self.assertTrue(
                any(
                    path.read_bytes() == unrelated_bytes
                    for path in evidence.iterdir()
                    if path.is_file()
                )
            )
            self.assertTrue(
                list(evidence.glob(f"{output.name}.persistence-unsafe.*"))
            )
            self.assertTrue((evidence / "pi-retained-aside").exists())

    def test_pi_unsafe_cleanup_rejects_replacement_after_final_owner_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence, output, result = self._pi_persistence_fixture(root)
            unsafe_name = f"{output.name}.persistence-unsafe.fixed"
            unsafe_path = evidence / unsafe_name
            unsafe_path.write_bytes(b"original-pass\n")
            unsafe_path.chmod(0o600)
            unrelated_bytes = b"unrelated-pi-after-final-owner-check\n"
            original_require = sync._require_retained_binding
            injected = False

            with sync._verified_parent(output, "Pi final owner check race") as guard:
                ownership = sync._open_guarded_binding(
                    guard, unsafe_name, "Pi final owner check race"
                )
                try:
                    expected = sync._binding_prestate(ownership)

                    def replace_after_final_owner_check(
                        check_guard,
                        name,
                        check_ownership,
                        label,
                        *,
                        expected=None,
                        allow_rename_ctime=False,
                    ):
                        nonlocal injected
                        value = original_require(
                            check_guard,
                            name,
                            check_ownership,
                            label,
                            expected=expected,
                            allow_rename_ctime=allow_rename_ctime,
                        )
                        if not injected and name.startswith(
                            f"{output.name}.transaction-unlink."
                        ):
                            quarantine = evidence / name
                            quarantine.rename(evidence / "pi-retained-final-aside")
                            unrelated = evidence / "unrelated-pi-final-owner-check"
                            unrelated.write_bytes(unrelated_bytes)
                            unrelated.chmod(0o600)
                            unrelated.rename(quarantine)
                            injected = True
                        return value

                    with mock.patch.object(
                        sync,
                        "_require_retained_binding",
                        side_effect=replace_after_final_owner_check,
                    ):
                        sync._remove_exact_pi_unsafe_entry(
                            guard,
                            unsafe_name,
                            ownership,
                            expected,
                            "Pi final owner check race",
                        )
                finally:
                    os.close(ownership["fd"])

            self.assertTrue(injected)
            self.assertTrue(
                any(
                    path.read_bytes() == unrelated_bytes
                    for path in evidence.iterdir()
                    if path.is_file()
                )
            )
            self.assertTrue(list(evidence.glob(f"{output.name}.persistence-unsafe.*")))
            self.assertTrue((evidence / "pi-retained-final-aside").exists())

    def test_pi_unsafe_cleanup_records_post_delete_uncertainty(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence, output, result = self._pi_persistence_fixture(root)
            unsafe_name = f"{output.name}.persistence-unsafe.fixed"
            unsafe_path = evidence / unsafe_name
            unsafe_path.write_bytes(b"original-pass\n")
            unsafe_path.chmod(0o600)
            injected = False

            def delete_then_raise(dir_fd, name):
                nonlocal injected
                injected = True
                os.unlink(name, dir_fd=dir_fd)
                raise OSError("injected Pi post-delete uncertainty")

            with sync._verified_parent(output, "Pi post-delete uncertainty") as guard:
                ownership = sync._open_guarded_binding(
                    guard, unsafe_name, "Pi post-delete uncertainty"
                )
                try:
                    expected = sync._binding_prestate(ownership)
                    with mock.patch.object(
                        sync,
                        "_unlinkat_kernel",
                        create=True,
                        side_effect=delete_then_raise,
                    ):
                        sync._remove_exact_pi_unsafe_entry(
                            guard,
                            unsafe_name,
                            ownership,
                            expected,
                            "Pi post-delete uncertainty",
                        )
                finally:
                    os.close(ownership["fd"])

            self.assertTrue(injected)
            blockers = list(evidence.glob(f"{output.name}.persistence-blocked.*"))
            self.assertTrue(blockers)
            self.assertTrue(all(stat.S_IMODE(path.stat().st_mode) == 0o600 for path in blockers))
            self.assertFalse(list(evidence.glob(f"{output.name}.transaction-unlink.*")))
            self.assertFalse(any(path.name.startswith(".cross-cli-sync.") for path in evidence.iterdir()))

    def test_pi_unsafe_cleanup_fail_closes_replacement_after_final_bind(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence, output, result = self._pi_persistence_fixture(root)
            unsafe_name = f"{output.name}.persistence-unsafe.fixed"
            unsafe_path = evidence / unsafe_name
            unsafe_path.write_bytes(b"original-pass\n")
            unsafe_path.chmod(0o600)
            unrelated_bytes = b"unrelated-pi-after-final-bind\n"
            original_open = sync._open_guarded_binding
            injected = False

            with sync._verified_parent(output, "Pi final bind race") as guard:
                ownership = sync._open_guarded_binding(
                    guard, unsafe_name, "Pi final bind race"
                )
                try:
                    expected = sync._binding_prestate(ownership)

                    def replace_after_final_bind(
                        bind_guard, name, label, *, writable=False
                    ):
                        nonlocal injected
                        binding = original_open(
                            bind_guard, name, label, writable=writable
                        )
                        if not injected and name.startswith(
                            f"{output.name}.transaction-unlink."
                        ):
                            quarantine = evidence / name
                            quarantine.rename(evidence / "pi-retained-final-bind-aside")
                            unrelated = evidence / "pi-unrelated-final-bind"
                            unrelated.write_bytes(unrelated_bytes)
                            unrelated.chmod(0o600)
                            unrelated.rename(quarantine)
                            injected = True
                        return binding

                    with mock.patch.object(
                        sync,
                        "_open_guarded_binding",
                        side_effect=replace_after_final_bind,
                    ):
                        sync._remove_exact_pi_unsafe_entry(
                            guard,
                            unsafe_name,
                            ownership,
                            expected,
                            "Pi final bind race",
                        )
                finally:
                    os.close(ownership["fd"])

            self.assertTrue(injected)
            self.assertTrue(
                any(path.read_bytes() == unrelated_bytes for path in evidence.iterdir())
            )
            self.assertTrue(
                list(evidence.glob(f"{output.name}.persistence-unsafe.*"))
            )
            self.assertTrue((evidence / "pi-retained-final-bind-aside").exists())
            self.assertTrue(
                list(evidence.glob(f"{output.name}.persistence-blocked.*"))
            )
            self.assertFalse(
                any(path.name.startswith(".cross-cli-sync.") for path in evidence.iterdir())
            )

    def test_pi_unsafe_cleanup_blocks_canonical_pass_after_final_bind_replacement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence, output, result = self._pi_persistence_fixture(root)
            unsafe_name = f"{output.name}.persistence-unsafe.fixed"
            unsafe_path = evidence / unsafe_name
            pass_bytes = sync._canonical_json_bytes(result)
            self.assertEqual(json.loads(pass_bytes)["verdict"], "PASS")
            unsafe_path.write_bytes(pass_bytes)
            unsafe_path.chmod(0o600)
            unrelated_bytes = b"unrelated-pi-canonical-final-bind\n"
            original_open = sync._open_guarded_binding
            injected = False

            with sync._verified_parent(output, "Pi canonical PASS final bind race") as guard:
                ownership = sync._open_guarded_binding(
                    guard,
                    unsafe_name,
                    "Pi canonical PASS final bind race",
                )
                try:
                    expected = sync._binding_prestate(ownership)

                    def replace_after_final_bind(
                        bind_guard, name, label, *, writable=False
                    ):
                        nonlocal injected
                        binding = original_open(
                            bind_guard, name, label, writable=writable
                        )
                        if not injected and name.startswith(
                            f"{output.name}.transaction-unlink."
                        ):
                            quarantine = evidence / name
                            quarantine.rename(
                                evidence / "pi-retained-canonical-pass-aside"
                            )
                            unrelated = evidence / "pi-unrelated-canonical-final-bind"
                            unrelated.write_bytes(unrelated_bytes)
                            unrelated.chmod(0o600)
                            unrelated.rename(quarantine)
                            injected = True
                        return binding

                    with mock.patch.object(
                        sync,
                        "_open_guarded_binding",
                        side_effect=replace_after_final_bind,
                    ):
                        sync._remove_exact_pi_unsafe_entry(
                            guard,
                            unsafe_name,
                            ownership,
                            expected,
                            "Pi canonical PASS final bind race",
                        )
                finally:
                    os.close(ownership["fd"])

            self.assertTrue(injected)
            self.assertTrue(
                any(path.read_bytes() == unrelated_bytes for path in evidence.iterdir())
            )
            blocked_bytes = sync._canonical_json_bytes(sync._blocked_pi_probe_result())
            retained_aside = evidence / "pi-retained-canonical-pass-aside"
            self.assertTrue(retained_aside.exists())
            self.assertEqual(stat.S_IMODE(retained_aside.stat().st_mode), 0o600)
            self.assertEqual(retained_aside.read_bytes(), blocked_bytes)
            for path in evidence.iterdir():
                if not path.is_file():
                    continue
                try:
                    payload = json.loads(path.read_text(encoding="utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    continue
                self.assertNotEqual(payload.get("verdict"), "PASS", path.name)
            self.assertTrue(
                list(evidence.glob(f"{output.name}.persistence-blocked.*"))
            )
            self.assertFalse(
                any(path.name.startswith(".cross-cli-sync.") for path in evidence.iterdir())
            )

    def test_pi_persist_rename_then_raise_never_leaves_official_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence, output, result = self._pi_persistence_fixture(Path(tmp))
            original_rename = sync._renameatx
            raised = False

            def rename_then_raise(source, destination, flags, **kwargs):
                nonlocal raised
                value = original_rename(source, destination, flags, **kwargs)
                if (
                    not raised
                    and Path(destination).name == output.name
                    and flags == sync.RENAME_EXCL
                ):
                    raised = True
                    raise OSError("injected rename-after-namespace-mutation")
                return value

            args = SimpleNamespace(output=output)
            with mock.patch.object(sync, "_renameatx", side_effect=rename_then_raise):
                persisted, success = sync.execute_pi_probe(args)

            self.assertTrue(raised)
            self.assertFalse(success)
            self.assertEqual(persisted["verdict"], "BLOCKED")
            self.assertFalse(output.exists())
            blocked = list(evidence.glob(f"{output.name}.persistence-blocked.*"))
            self.assertTrue(blocked)
            blocked_bytes = sync._canonical_json_bytes(sync._blocked_pi_probe_result())
            self.assertTrue(
                all(path.read_bytes() == blocked_bytes for path in blocked)
            )

    def test_pi_blocked_recovery_rename_then_raise_never_accepts_malformed_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence, output, result = self._pi_persistence_fixture(root)
            blocked = sync._canonical_json_bytes(sync._blocked_pi_probe_result())
            malformed = b"MALFORMED-BLOCKED-EVIDENCE\n"
            original_rename = sync._renameatx
            raised = False

            def rename_then_corrupt_and_raise(source, destination, flags, **kwargs):
                nonlocal raised
                value = original_rename(source, destination, flags, **kwargs)
                if (
                    not raised
                    and Path(destination).name.startswith(
                        f"{output.name}.persistence-blocked."
                    )
                    and flags == sync.RENAME_EXCL
                ):
                    raised = True
                    blocked_path = evidence / Path(destination).name
                    blocked_path.write_bytes(malformed)
                    blocked_path.chmod(0o600)
                    raise OSError("injected blocked rename-after-mutation")
                return value

            with sync._verified_parent(output, "Pi blocked rename race") as guard:
                with mock.patch.object(
                    sync, "_renameatx", side_effect=rename_then_corrupt_and_raise
                ):
                    with self.assertRaises((OSError, ValueError)):
                        sync._create_pi_blocked_recovery(
                            guard, output.name, blocked, "Pi blocked rename race"
                        )

            self.assertTrue(raised)
            self.assertFalse(
                any(
                    path.name.startswith(f"{output.name}.persistence-blocked.")
                    and path.read_bytes() == malformed
                    for path in evidence.iterdir()
                )
            )
            unsafe = list(evidence.glob(f"{output.name}.persistence-unsafe.*"))
            self.assertTrue(unsafe)
            self.assertTrue(any(path.read_bytes() == malformed for path in unsafe))

    def test_pi_rollback_collision_moves_unrelated_output_and_writes_blocked_residue(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence, output, result = self._pi_persistence_fixture(Path(tmp))
            original_write_candidate = sync._write_pi_probe_candidate
            original_fsync_directory = sync._fsync_directory
            original_rename = sync._renameatx
            candidate_name = None
            injected = False
            unrelated = b"unrelated-pi-rollback-collision\n"

            def capture_candidate(*args, **kwargs):
                nonlocal candidate_name
                value = original_write_candidate(*args, **kwargs)
                candidate_name = value["name"]
                return value

            def collide_during_rollback(path):
                nonlocal injected
                if not injected and Path(path) == evidence and output.exists() and candidate_name:
                    output.unlink()
                    replacement = evidence / "unrelated-pi-rollback"
                    replacement.write_bytes(unrelated)
                    replacement.chmod(0o600)
                    replacement.rename(output)
                    blocker = evidence / candidate_name
                    blocker.write_bytes(b"candidate-name-blocker\n")
                    blocker.chmod(0o600)
                    injected = True
                    raise OSError("injected rollback collision")
                return original_fsync_directory(path)

            args = SimpleNamespace(output=output)
            with mock.patch.object(
                sync, "_write_pi_probe_candidate", side_effect=capture_candidate
            ), mock.patch.object(
                sync, "_fsync_directory", side_effect=collide_during_rollback
            ):
                persisted, success = sync.execute_pi_probe(args)

            self.assertTrue(injected)
            self.assertFalse(success)
            self.assertEqual(persisted["verdict"], "BLOCKED")
            self.assertFalse(output.exists())
            blocked = list(evidence.glob(f"{output.name}.persistence-blocked.*"))
            self.assertTrue(blocked)
            blocked_bytes = sync._canonical_json_bytes(sync._blocked_pi_probe_result())
            self.assertTrue(
                all(path.read_bytes() == blocked_bytes for path in blocked)
            )
            unsafe = list(evidence.glob(f"{output.name}.persistence-unsafe.*"))
            self.assertTrue(unsafe)
            self.assertTrue(any(path.read_bytes() == unrelated for path in unsafe))

    def test_pi_blocked_recovery_uses_pending_name_before_write_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence, output, result = self._pi_persistence_fixture(root)
            blocked = sync._canonical_json_bytes(sync._blocked_pi_probe_result())
            original_write = sync._write_descriptor
            saw_pending = False

            def fail_after_pending(descriptor, content):
                nonlocal saw_pending
                saw_pending = any(
                    path.name.startswith(f"{output.name}.persistence-pending.")
                    for path in evidence.iterdir()
                )
                original_write(descriptor, content[:1])
                raise OSError("injected blocked recovery write failure")

            with sync._verified_parent(output, "Pi blocked pending test") as guard:
                with mock.patch.object(
                    sync, "_write_descriptor", side_effect=fail_after_pending
                ):
                    with self.assertRaisesRegex(OSError, "blocked recovery write"):
                        sync._create_pi_blocked_recovery(
                            guard, output.name, blocked, "Pi blocked pending test"
                        )

            self.assertTrue(saw_pending)
            self.assertFalse(
                any(
                    path.name.startswith(f"{output.name}.persistence-blocked.")
                    for path in evidence.iterdir()
                )
            )

    def test_pi_candidate_binding_failure_creates_independent_blocked_recovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence, output, result = self._pi_persistence_fixture(Path(tmp))
            content = sync._canonical_json_bytes(result)
            blocked = sync._canonical_json_bytes(sync._blocked_pi_probe_result())
            original_binding = sync._descriptor_binding
            calls = 0

            def fail_first_binding(descriptor, label):
                nonlocal calls
                calls += 1
                if calls == 1:
                    raise ValueError("injected candidate binding failure")
                return original_binding(descriptor, label)

            with sync._verified_parent(output, "Pi candidate binding failure") as guard:
                with mock.patch.object(
                    sync, "_descriptor_binding", side_effect=fail_first_binding
                ):
                    with self.assertRaisesRegex(ValueError, "candidate binding failure"):
                        sync._write_pi_probe_candidate(
                            output,
                            content,
                            0o600,
                            parent_guard=guard,
                            blocked_content=blocked,
                            label="Pi candidate binding failure",
                        )

            self.assertGreaterEqual(calls, 2)
            blocked_entries = list(evidence.glob(f"{output.name}.persistence-blocked.*"))
            self.assertTrue(blocked_entries)
            self.assertTrue(
                all(
                    stat.S_IMODE(path.stat().st_mode) == 0o600
                    and path.read_bytes() == blocked
                    for path in blocked_entries
                )
            )
            self.assertFalse(output.exists())
            self.assertFalse(any(path.name.startswith(".cross-cli-sync.") for path in evidence.iterdir()))

    def test_pi_quarantine_rejects_candidate_substitution_before_rename(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence, output, result = self._pi_persistence_fixture(root)
            content = sync._canonical_json_bytes(result)
            blocked = sync._canonical_json_bytes(sync._blocked_pi_probe_result())
            candidate_info = None
            injected = False

            with sync._verified_parent(output, "Pi quarantine test") as guard:
                candidate_info = sync._write_pi_probe_candidate(
                    output,
                    content,
                    0o600,
                    parent_guard=guard,
                    blocked_content=blocked,
                    label="Pi quarantine test",
                )

                original_retained = sync._retained_binding_matches_name

                def substitute_before_quarantine(
                    guard,
                    name,
                    ownership,
                    label,
                    *,
                    expected=None,
                    allow_rename_ctime=False,
                ):
                    nonlocal injected
                    value = original_retained(
                        guard,
                        name,
                        ownership,
                        label,
                        expected=expected,
                        allow_rename_ctime=allow_rename_ctime,
                    )
                    if not injected and name == candidate_info["name"] and value:
                        candidate = evidence / name
                        candidate.unlink()
                        unrelated = evidence / "unrelated-quarantine"
                        unrelated.write_bytes(content)
                        unrelated.chmod(0o600)
                        unrelated.rename(candidate)
                        injected = True
                    return value

                try:
                    with mock.patch.object(
                        sync,
                        "_retained_binding_matches_name",
                        side_effect=substitute_before_quarantine,
                    ):
                        with self.assertRaisesRegex(ValueError, "candidate|ambiguous|quarantine"):
                            sync._quarantine_pi_probe_candidate(
                                guard,
                                candidate_info["name"],
                                {
                                    "kind": "file",
                                    "sha256": hashlib.sha256(content).hexdigest(),
                                    "mode": 0o600,
                                },
                                output.name,
                                "Pi quarantine test",
                                ownership=candidate_info,
                            )
                finally:
                    if candidate_info.get("fd") is not None:
                        os.close(candidate_info["fd"])

            self.assertTrue(injected)
            self.assertTrue(
                any(path.name.startswith(f"{output.name}.persistence-unsafe.") for path in evidence.iterdir())
            )
            blocked = list(evidence.glob(f"{output.name}.persistence-blocked.*"))
            self.assertTrue(blocked)
            self.assertTrue(
                all(
                    json.loads(path.read_text(encoding="utf-8"))["verdict"] == "BLOCKED"
                    for path in blocked
                )
            )

    def test_pi_quarantine_parent_drift_after_rename_does_not_park_current_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence, output, result = self._pi_persistence_fixture(root)
            content = sync._canonical_json_bytes(result)
            blocked = sync._canonical_json_bytes(sync._blocked_pi_probe_result())
            original_rename = sync._renameatx
            moved = evidence.with_name("evidence-moved")
            drifted = False

            with sync._verified_parent(output, "Pi quarantine drift test") as guard:
                candidate_info = sync._write_pi_probe_candidate(
                    output,
                    content,
                    0o600,
                    parent_guard=guard,
                    blocked_content=blocked,
                    label="Pi quarantine drift test",
                )

                def drift_after_quarantine(source, destination, flags, **kwargs):
                    nonlocal drifted
                    value = original_rename(source, destination, flags, **kwargs)
                    if (
                        not drifted
                        and Path(destination).name.startswith(f"{output.name}.persistence-unsafe.")
                        and flags == sync.RENAME_EXCL
                    ):
                        evidence.rename(moved)
                        evidence.mkdir(mode=0o700)
                        drifted = True
                    return value

                try:
                    with mock.patch.object(sync, "_renameatx", side_effect=drift_after_quarantine):
                        with self.assertRaisesRegex(ValueError, "parent|quarantine|ambiguous"):
                            sync._quarantine_pi_probe_candidate(
                                guard,
                                candidate_info["name"],
                                {
                                    "kind": "file",
                                    "sha256": hashlib.sha256(content).hexdigest(),
                                    "mode": 0o600,
                                },
                                output.name,
                                "Pi quarantine drift test",
                                ownership=candidate_info,
                            )
                finally:
                    if candidate_info.get("fd") is not None:
                        os.close(candidate_info["fd"])

            self.assertTrue(drifted)
            self.assertFalse(any(path.name.startswith(f"{output.name}.persistence-blocked.") for path in evidence.iterdir()))

    def test_pi_neutralization_failure_uses_visible_unsafe_recovery_object(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence, output, result = self._pi_persistence_fixture(Path(tmp))
            original_fsync = sync.os.fsync
            failed = False

            def fail_candidate_fsync(descriptor):
                nonlocal failed
                if not failed:
                    failed = True
                    raise OSError("injected Pi candidate fsync failure")
                return original_fsync(descriptor)

            with mock.patch.object(sync, "_execute_pi_probe", return_value=(result, True)), \
                    mock.patch.object(sync.os, "fsync", side_effect=fail_candidate_fsync), \
                    mock.patch.object(
                        sync,
                        "_create_pi_blocked_recovery",
                        side_effect=OSError("injected blocked recovery failure"),
                    ):
                persisted, success = sync.execute_pi_probe(SimpleNamespace(output=output))

            self.assertTrue(failed)
            self.assertFalse(success)
            self.assertEqual(persisted["verdict"], "BLOCKED")
            self.assertFalse(output.exists())
            self.assertFalse(any(path.name.startswith(".cross-cli-sync.") for path in evidence.iterdir()))
            unsafe = list(evidence.glob(f"{output.name}.persistence-unsafe.*"))
            self.assertTrue(unsafe)
            self.assertEqual(stat.S_IMODE(unsafe[0].stat().st_mode), 0o600)

    def test_pi_persistence_quarantine_collision_retries_visible_blocked_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence, output, result = self._pi_persistence_fixture(Path(tmp))
            original_fsync = sync.os.fsync
            original_rename = sync._renameatx
            failed = False
            collided = False

            def fail_candidate_fsync(descriptor):
                nonlocal failed
                if not failed:
                    failed = True
                    raise OSError("injected Pi candidate fsync failure")
                return original_fsync(descriptor)

            def collide_once(source, destination, flags, **kwargs):
                nonlocal collided
                if (
                    not collided
                    and Path(destination).name.startswith(f"{output.name}.persistence-blocked.")
                ):
                    collided = True
                    raise FileExistsError("injected blocked recovery collision")
                return original_rename(source, destination, flags, **kwargs)

            with mock.patch.object(sync, "_execute_pi_probe", return_value=(result, True)), \
                    mock.patch.object(sync.os, "fsync", side_effect=fail_candidate_fsync), \
                    mock.patch.object(sync, "_renameatx", side_effect=collide_once):
                persisted, success = sync.execute_pi_probe(SimpleNamespace(output=output))

            self.assertTrue(failed)
            self.assertTrue(collided)
            self.assertFalse(success)
            self.assertEqual(persisted["verdict"], "BLOCKED")
            blocked = list(evidence.glob(f"{output.name}.persistence-blocked.*"))
            self.assertTrue(blocked)
            self.assertTrue(all(json.loads(path.read_text(encoding="utf-8"))["verdict"] == "BLOCKED" for path in blocked))

    def test_managed_v6_binds_exact_changed_semantics(self):
        self.assertEqual(sync.MANAGED_RULE_INVARIANT_COUNT.get(6), 16)
        body = (
            Path(__file__).parents[1]
            / "references"
            / "shared-global-governance.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(body.split())
        for invariant_id, expected in V6_SEMANTIC_BODIES.items():
            with self.subTest(invariant_id=invariant_id):
                self.assertIn(f"[{invariant_id}] {expected}", normalized)
        validator = getattr(sync, "validate_managed_rule_semantics", None)
        self.assertTrue(callable(validator), "v6 semantic validator is required")
        self.assertTrue(validator(body, version=6))

    def test_managed_v6_semantics_fail_closed_on_each_critical_omission(self):
        validator = getattr(sync, "validate_managed_rule_semantics", None)
        self.assertTrue(callable(validator), "v6 semantic validator is required")
        body = "\n".join(
            f"- [{invariant_id}] {text}"
            for invariant_id, text in V6_SEMANTIC_BODIES.items()
        ) + "\n"
        self.assertTrue(validator(body, version=6))
        for missing in (
            "control-plane-high",
            "instance identity",
            "contract",
            "Pi",
            "Antigravity CLI",
            "Grok CLI",
            "schema-5 contracts must drain",
            "immutable history",
            "Review purpose",
            "other agent",
            "fail-closed",
        ):
            with self.subTest(missing=missing):
                mutated = body.replace(missing, "omitted", 1)
                with self.assertRaises(ValueError):
                    validator(mutated, version=6)

    def test_manifest_v6_requires_four_targets_in_exact_order(self):
        manifest = portable_manifest_v6()
        try:
            validated = sync.validate_manifest(manifest)
        except ValueError as exc:
            self.fail(f"managed-rule version 6 with Pi must be supported: {exc}")
        self.assertEqual(validated, manifest)
        expected = ["codex", "pi", "antigravity-cli", "grok-cli"]
        for skill in manifest["skills"]:
            for item in skill["files"]:
                self.assertEqual(item["targets"], expected)
        self.assertEqual([item["id"] for item in manifest["targets"]], expected)
        self.assertEqual(manifest["managed_rules"]["invariant_ids"], V6_INVARIANTS)

        missing_pi = portable_manifest_v6()
        missing_pi["targets"].pop(1)
        with self.assertRaises(ValueError):
            sync.validate_manifest(missing_pi)

        reordered = portable_manifest_v6()
        reordered["skills"][0]["files"][0]["targets"] = [
            "pi", "codex", "antigravity-cli", "grok-cli"
        ]
        with self.assertRaises(ValueError):
            sync.validate_manifest(reordered)

    def test_cli_exposes_pi_prestate_probe_and_receipt_contract(self):
        script = str(Path(sync.__file__))
        root_help = subprocess.run(
            [sys.executable, script, "--help"], capture_output=True, text=True, check=False
        )
        self.assertEqual(root_help.returncode, 0, root_help.stderr)
        for command in (
            "verify-prestate", "probe-pi", "restore-target", "recover-pending",
            "commit-target",
        ):
            self.assertIn(command, root_help.stdout)

        plan_help = subprocess.run(
            [sys.executable, script, "plan", "--help"],
            capture_output=True, text=True, check=False,
        )
        self.assertIn("--pi-skills-root", plan_help.stdout)
        self.assertIn("--pi-rule-file", plan_help.stdout)

        apply_help = subprocess.run(
            [sys.executable, script, "apply", "--help"],
            capture_output=True, text=True, check=False,
        )
        self.assertIn("--transaction-receipt", apply_help.stdout)

        verify_all_help = subprocess.run(
            [sys.executable, script, "verify-all", "--help"],
            capture_output=True, text=True, check=False,
        )
        self.assertIn("--transaction-root", verify_all_help.stdout)

    def test_build_pi_probe_is_pure_isolated_and_fail_closed(self):
        builder = getattr(sync, "build_pi_probe", None)
        self.assertTrue(callable(builder), "build_pi_probe is required")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "pi"
            executable.write_text("#!/bin/sh\n", encoding="utf-8")
            executable.chmod(0o755)
            temporary = root / "isolated"
            temporary.mkdir()
            native = root / "native-pi"
            native.mkdir()
            contract = builder(
                executable,
                temporary,
                native,
                prompt="Review the bound source and return PASS or BLOCKED.",
            )
            self.assertEqual(
                set(contract),
                {
                    "argv", "env", "sandbox_profile", "allowed_output_fields",
                    "launcher_snapshot",
                },
            )
            self.assertIsNone(contract["launcher_snapshot"])
            self.assertEqual(
                set(contract["env"]),
                {"HOME", "PI_CODING_AGENT_DIR", "PATH", "LANG", "LC_ALL"},
            )
            self.assertTrue(
                Path(contract["env"]["HOME"]).is_relative_to(temporary.resolve())
            )
            self.assertTrue(
                Path(contract["env"]["PI_CODING_AGENT_DIR"]).is_relative_to(
                    temporary.resolve()
                )
            )
            for flag in (
                "--no-session", "--no-context-files", "--no-skills", "--tools", "-p"
            ):
                self.assertIn(flag, contract["argv"])
            self.assertIn("read,grep,find,ls", contract["argv"])
            self.assertIn(str(native.resolve()), contract["sandbox_profile"])
            self.assertIn("network*", contract["sandbox_profile"])

            executable_link = root / "pi-link"
            executable_link.symlink_to(executable)
            with self.assertRaises(ValueError):
                builder(executable_link, temporary, native)
            with self.assertRaises(ValueError):
                builder(executable, native, native)

    def test_build_pi_probe_binds_a_single_shell_exec_launcher(self):
        builder = getattr(sync, "build_pi_probe", None)
        self.assertTrue(callable(builder), "build_pi_probe is required")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / "pi-package"
            cli = package / "dist" / "cli.pl"
            cli.parent.mkdir(parents=True)
            (package / "package.json").write_text(
                '{"name":"fake-pi"}\n', encoding="utf-8"
            )
            cli.write_text(
                'print qq({"verdict":"PASS","findings":[]}\\n);\n',
                encoding="utf-8",
            )
            cli.chmod(0o755)
            executable = root / "pi"
            executable.write_text(
                f'#!/bin/sh\nexec /usr/bin/perl {cli} "$@"\n', encoding="utf-8"
            )
            executable.chmod(0o755)
            temporary = root / "isolated"
            temporary.mkdir()
            native = root / "native-pi"
            native.mkdir()

            contract = builder(executable, temporary, native, prompt="Review JSON.")
            profile = contract["sandbox_profile"]
            self.assertIn('(literal "/usr/bin/perl")', profile)
            self.assertNotIn(str(package.resolve()), profile)
            self.assertTrue(Path(contract["argv"][1]).is_relative_to(temporary.resolve()))
            self.assertIn(
                f'(deny file-write* (subpath "{temporary.resolve() / "launcher-package"}"))',
                profile,
            )
            self.assertEqual(
                set(contract["launcher_snapshot"]),
                {
                    "source_root", "destination_root", "entrypoint_relative",
                    "source_inventory_sha256", "runtime_path", "runtime_binding",
                },
            )

    def test_build_pi_probe_rejects_package_contained_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / "pi-package"
            runtime = package / "bin" / "runtime"
            cli = package / "dist" / "cli.pl"
            runtime.parent.mkdir(parents=True)
            cli.parent.mkdir(parents=True)
            (package / "package.json").write_text(
                '{"name":"fake-pi"}\n', encoding="utf-8"
            )
            runtime.write_text("#!/bin/sh\n", encoding="utf-8")
            runtime.chmod(0o755)
            cli.write_text("# fake cli\n", encoding="utf-8")
            cli.chmod(0o755)
            executable = root / "pi"
            executable.write_text(
                f'#!/bin/sh\nexec {runtime} {cli} "$@"\n', encoding="utf-8"
            )
            executable.chmod(0o755)
            temporary = root / "isolated"
            temporary.mkdir()
            native = root / "native-pi"
            native.mkdir()

            with self.assertRaisesRegex(
                ValueError, "runtime must remain outside package"
            ):
                sync.build_pi_probe(executable, temporary, native)

    def test_build_pi_probe_rejects_hard_linked_package_runtime_alias(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / "pi-package"
            package_runtime = package / "bin" / "runtime"
            cli = package / "dist" / "cli.pl"
            package_runtime.parent.mkdir(parents=True)
            cli.parent.mkdir(parents=True)
            (package / "package.json").write_text(
                '{"name":"fake-pi"}\n', encoding="utf-8"
            )
            package_runtime.write_text("#!/bin/sh\n", encoding="utf-8")
            package_runtime.chmod(0o755)
            runtime_alias = root / "runtime-alias"
            os.link(package_runtime, runtime_alias)
            cli.write_text("# fake cli\n", encoding="utf-8")
            cli.chmod(0o755)
            executable = root / "pi"
            executable.write_text(
                f'#!/bin/sh\nexec {runtime_alias} {cli} "$@"\n', encoding="utf-8"
            )
            executable.chmod(0o755)
            temporary = root / "isolated"
            temporary.mkdir()
            native = root / "native-pi"
            native.mkdir()

            with self.assertRaisesRegex(ValueError, "runtime aliases package"):
                sync.build_pi_probe(executable, temporary, native)

    def test_build_pi_probe_rejects_runtime_alias_created_during_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / "pi-package"
            package_runtime = package / "bin" / "runtime"
            cli = package / "dist" / "cli.pl"
            package_runtime.parent.mkdir(parents=True)
            cli.parent.mkdir(parents=True)
            (package / "package.json").write_text(
                '{"name":"fake-pi"}\n', encoding="utf-8"
            )
            package_runtime.write_text("#!/bin/sh\n", encoding="utf-8")
            package_runtime.chmod(0o755)
            cli.write_text("# fake cli\n", encoding="utf-8")
            cli.chmod(0o755)
            runtime = root / "runtime"
            runtime.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            runtime.chmod(0o755)
            executable = root / "pi"
            executable.write_text(
                f'#!/bin/sh\nexec {runtime} {cli} "$@"\n', encoding="utf-8"
            )
            executable.chmod(0o755)
            temporary = root / "isolated"
            temporary.mkdir()
            native = root / "native-pi"
            native.mkdir()
            original_sha256 = sync._sha256
            swapped = False

            def alias_runtime_during_inventory(path):
                nonlocal swapped
                if Path(path).resolve() == package_runtime.resolve() and not swapped:
                    runtime.unlink()
                    os.link(package_runtime, runtime)
                    swapped = True
                return original_sha256(path)

            with mock.patch.object(
                sync, "_sha256", side_effect=alias_runtime_during_inventory
            ), self.assertRaisesRegex(ValueError, "runtime identity drift"):
                sync.build_pi_probe(executable, temporary, native)

            self.assertTrue(swapped)

    def test_build_pi_probe_rejects_ambiguous_shell_launchers(self):
        builder = getattr(sync, "build_pi_probe", None)
        self.assertTrue(callable(builder), "build_pi_probe is required")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / "pi-package"
            cli = package / "dist" / "cli.js"
            cli.parent.mkdir(parents=True)
            (package / "package.json").write_text(
                '{"name":"fake-pi"}\n', encoding="utf-8"
            )
            cli.write_text("// fake cli\n", encoding="utf-8")
            cli.chmod(0o755)
            runtime = root / "runtime"
            runtime.write_text("#!/bin/sh\n", encoding="utf-8")
            runtime.chmod(0o755)
            cli_link = package / "linked-cli.js"
            cli_link.symlink_to(cli)
            temporary = root / "isolated"
            temporary.mkdir()
            native = root / "native-pi"
            native.mkdir()
            cases = {
                "extra-command": (
                    f'#!/bin/sh\necho unsafe\nexec {runtime} {cli} "$@"\n'
                ),
                "relative-runtime": f'#!/bin/sh\nexec runtime {cli} "$@"\n',
                "missing-forwarding": f"#!/bin/sh\nexec {runtime} {cli}\n",
                "linked-entrypoint": (
                    f'#!/bin/sh\nexec {runtime} {cli_link} "$@"\n'
                ),
            }
            for label, body in cases.items():
                with self.subTest(label=label):
                    executable = root / f"pi-{label}"
                    executable.write_text(body, encoding="utf-8")
                    executable.chmod(0o755)
                    with self.assertRaises(ValueError):
                        builder(executable, temporary, native)

            outside = root / "outside.js"
            outside.write_text("// outside\n", encoding="utf-8")
            (package / "external-link.js").symlink_to(outside)
            executable = root / "pi-external-package-link"
            executable.write_text(
                f'#!/bin/sh\nexec {runtime} {cli} "$@"\n', encoding="utf-8"
            )
            executable.chmod(0o755)
            with self.assertRaises(ValueError):
                builder(executable, temporary, native)

    def test_probe_pi_cli_sanitizes_setup_failure_into_private_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            missing_executable = root / "raw-sensitive-path-do-not-leak"
            native = root / "native"
            native.mkdir()
            temporary = root / "probe-temp"
            temporary.mkdir()
            prompt = root / "prompt.md"
            prompt.write_text("Review the bound source.\n", encoding="utf-8")
            reviewed = root / "reviewed"
            reviewed.mkdir()
            evidence = root / "evidence"
            evidence.mkdir(mode=0o700)
            output = evidence / "pi-review.json"

            completed = subprocess.run(
                [
                    sys.executable,
                    str(Path(sync.__file__)),
                    "probe-pi",
                    "--pi-executable",
                    str(missing_executable),
                    "--native-pi-root",
                    str(native),
                    "--temporary-root",
                    str(temporary),
                    "--prompt-file",
                    str(prompt),
                    "--read-root",
                    str(reviewed),
                    "--output",
                    str(output),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 1)
            self.assertEqual(completed.stderr, "")
            result = json.loads(completed.stdout)
            self.assertEqual(
                set(result),
                {
                    "pi_probe", "reviewer_identity", "bound_input_hashes",
                    "verdict", "findings",
                },
            )
            self.assertEqual(result["pi_probe"], "blocked")
            self.assertEqual(result["verdict"], "BLOCKED")
            self.assertTrue(output.is_file())
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o600)
            persisted = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(persisted, result)
            combined = completed.stdout + completed.stderr + output.read_text(
                encoding="utf-8"
            )
            self.assertNotIn(str(missing_executable), combined)
            self.assertNotIn("does not exist", combined)

    def test_probe_pi_sanitizes_subprocess_launch_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "fake-pi"
            executable.write_text("#!/usr/bin/perl\n", encoding="utf-8")
            executable.chmod(0o755)
            native = root / "native-sensitive-path"
            native.mkdir()
            temporary = root / "probe-temp"
            temporary.mkdir()
            prompt = root / "prompt.md"
            prompt.write_text("Review the bound source.\n", encoding="utf-8")
            reviewed = root / "reviewed"
            reviewed.mkdir()
            evidence = root / "evidence"
            evidence.mkdir(mode=0o700)
            output = evidence / "pi-review.json"
            args = SimpleNamespace(
                pi_executable=executable,
                native_pi_root=native,
                temporary_root=temporary,
                prompt_file=prompt,
                read_root=[reviewed],
                output=output,
            )

            with mock.patch.object(
                sync.subprocess,
                "run",
                side_effect=OSError(f"raw launch failure: {native}"),
            ):
                result, success = sync.execute_pi_probe(args)

            self.assertFalse(success)
            self.assertEqual(result["pi_probe"], "blocked")
            self.assertEqual(result["verdict"], "BLOCKED")
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o600)
            persisted = output.read_text(encoding="utf-8")
            self.assertNotIn(str(native), persisted)
            self.assertNotIn("raw launch failure", persisted)

    def test_reviewed_tree_digest_rejects_retargetable_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reviewed = root / "reviewed"
            reviewed.mkdir()
            (reviewed / "a").write_text("first\n", encoding="utf-8")
            (reviewed / "b").write_text("second\n", encoding="utf-8")
            (reviewed / "current").symlink_to("a")

            with self.assertRaisesRegex(ValueError, "must not contain symlinks"):
                sync._reviewed_tree_digest(reviewed)

    def test_probe_pi_rejects_top_level_reviewed_root_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "fake-pi"
            executable.write_text("#!/usr/bin/perl\n", encoding="utf-8")
            executable.chmod(0o755)
            native = root / "native"
            native.mkdir()
            temporary = root / "probe-temp"
            temporary.mkdir()
            prompt = root / "prompt.md"
            prompt.write_text("Review the bound source.\n", encoding="utf-8")
            reviewed = root / "reviewed"
            reviewed.mkdir()
            (reviewed / "input.md").write_text("reviewed bytes\n", encoding="utf-8")
            reviewed_link = root / "reviewed-link"
            reviewed_link.symlink_to(reviewed, target_is_directory=True)
            evidence = root / "evidence"
            evidence.mkdir(mode=0o700)
            output = evidence / "pi-review.json"
            completed = SimpleNamespace(
                returncode=0,
                stdout='{"verdict":"PASS","findings":[]}',
                stderr="",
            )

            with mock.patch.object(sync.subprocess, "run", return_value=completed):
                result, success = sync.execute_pi_probe(
                    SimpleNamespace(
                        pi_executable=executable,
                        native_pi_root=native,
                        temporary_root=temporary,
                        prompt_file=prompt,
                        read_root=[reviewed_link],
                        output=output,
                    )
                )

            self.assertFalse(success)
            self.assertEqual(result["pi_probe"], "blocked")
            self.assertEqual(result["verdict"], "BLOCKED")

    def test_probe_pi_rejects_reviewed_regular_file_mode_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "fake-pi"
            executable.write_text("#!/usr/bin/perl\n", encoding="utf-8")
            executable.chmod(0o755)
            native = root / "native"
            native.mkdir()
            temporary = root / "probe-temp"
            temporary.mkdir()
            prompt = root / "prompt.md"
            prompt.write_text("Review the bound source.\n", encoding="utf-8")
            reviewed = root / "reviewed"
            reviewed.mkdir()
            reviewed_file = reviewed / "input.md"
            reviewed_file.write_text("reviewed bytes\n", encoding="utf-8")
            reviewed_file.chmod(0o644)
            evidence = root / "evidence"
            evidence.mkdir(mode=0o700)
            output = evidence / "pi-review.json"
            completed = SimpleNamespace(
                returncode=0,
                stdout='{"verdict":"PASS","findings":[]}',
                stderr="",
            )

            def change_mode_then_return(*_args, **_kwargs):
                reviewed_file.chmod(0o600)
                return completed

            with mock.patch.object(
                sync.subprocess, "run", side_effect=change_mode_then_return
            ):
                result, success = sync.execute_pi_probe(
                    SimpleNamespace(
                        pi_executable=executable,
                        native_pi_root=native,
                        temporary_root=temporary,
                        prompt_file=prompt,
                        read_root=[reviewed],
                        output=output,
                    )
                )

            self.assertFalse(success)
            self.assertEqual(result["pi_probe"], "blocked")
            self.assertEqual(result["verdict"], "BLOCKED")

    def test_probe_pi_removes_pass_artifact_when_directory_fsync_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "fake-pi"
            executable.write_text("#!/usr/bin/perl\n", encoding="utf-8")
            executable.chmod(0o755)
            native = root / "native"
            native.mkdir()
            temporary = root / "probe-temp"
            temporary.mkdir()
            prompt = root / "prompt.md"
            prompt.write_text("Review the bound source.\n", encoding="utf-8")
            reviewed = root / "reviewed"
            reviewed.mkdir()
            evidence = root / "evidence"
            evidence.mkdir(mode=0o700)
            output = evidence / "pi-review.json"
            args = SimpleNamespace(
                pi_executable=executable,
                native_pi_root=native,
                temporary_root=temporary,
                prompt_file=prompt,
                read_root=[reviewed],
                output=output,
            )
            original_fsync_directory = sync._fsync_directory
            installed_inode = None

            def fail_output_directory(path):
                nonlocal installed_inode
                if Path(path) == evidence:
                    installed_inode = output.stat().st_ino
                    raise OSError("injected output directory fsync failure")
                return original_fsync_directory(path)

            completed = SimpleNamespace(
                returncode=0,
                stdout='{"verdict":"PASS","findings":[]}',
                stderr="",
            )
            with mock.patch.object(sync.subprocess, "run", return_value=completed), \
                    mock.patch.object(
                        sync, "_fsync_directory", side_effect=fail_output_directory
                    ):
                result, success = sync.execute_pi_probe(args)

            self.assertFalse(success)
            self.assertEqual(result["pi_probe"], "blocked")
            self.assertEqual(result["verdict"], "BLOCKED")
            self.assertFalse(output.exists())
            blocked = list(evidence.glob(f"{output.name}.persistence-blocked.*"))
            self.assertTrue(blocked)
            self.assertTrue(
                all(stat.S_IMODE(path.stat().st_mode) == 0o600 for path in blocked)
            )
            self.assertTrue(
                all(
                    json.loads(path.read_text(encoding="utf-8"))
                    == sync._blocked_pi_probe_result()
                    for path in blocked
                )
            )

    def test_probe_pi_neutralizes_pass_artifact_when_rollback_unlink_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp) / "evidence"
            evidence.mkdir(mode=0o700)
            output = evidence / "pi-review.json"
            args = SimpleNamespace(output=output)
            pass_result = {
                "pi_probe": "pass",
                "reviewer_identity": {
                    "product": "pi",
                    "role": "independent-reviewer",
                    "capability_profile": "control-plane-high",
                },
                "bound_input_hashes": {},
                "verdict": "PASS",
                "findings": [],
            }
            original_fsync_directory = sync._fsync_directory
            original_guarded_unlink = sync._guarded_unlink

            def fail_output_directory(path):
                if Path(path) == evidence:
                    raise OSError("injected output directory fsync failure")
                return original_fsync_directory(path)

            def fail_output_unlink(guard, name, *, missing_ok=False):
                if name == output.name:
                    raise OSError("injected rollback unlink failure")
                return original_guarded_unlink(guard, name, missing_ok=missing_ok)

            with mock.patch.object(
                sync, "_execute_pi_probe", return_value=(pass_result, True)
            ), mock.patch.object(
                sync, "_fsync_directory", side_effect=fail_output_directory
            ), mock.patch.object(
                sync, "_guarded_unlink", side_effect=fail_output_unlink
            ):
                result, success = sync.execute_pi_probe(args)

            self.assertFalse(success)
            self.assertEqual(result["verdict"], "BLOCKED")
            if output.exists():
                persisted = json.loads(output.read_text(encoding="utf-8"))
                self.assertEqual(persisted["pi_probe"], "blocked")
                self.assertEqual(persisted["verdict"], "BLOCKED")

    def test_probe_pi_removes_hidden_candidate_when_candidate_unlink_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp) / "evidence"
            evidence.mkdir(mode=0o700)
            output = evidence / "pi-review.json"
            args = SimpleNamespace(output=output)
            pass_result = {
                "pi_probe": "pass",
                "reviewer_identity": {
                    "product": "pi",
                    "role": "independent-reviewer",
                    "capability_profile": "control-plane-high",
                },
                "bound_input_hashes": {},
                "verdict": "PASS",
                "findings": [],
            }
            original_renameatx = sync._renameatx

            def collide_at_output(
                source, destination, flags, *, source_dir_fd=None,
                destination_dir_fd=None
            ):
                if destination == output.name:
                    raise FileExistsError("injected exclusive rename collision")
                return original_renameatx(
                    source,
                    destination,
                    flags,
                    source_dir_fd=source_dir_fd,
                    destination_dir_fd=destination_dir_fd,
                )

            def fail_hidden_unlink(_guard, _name, *, missing_ok=False):
                raise OSError("injected persistent candidate unlink failure")

            with mock.patch.object(
                sync, "_execute_pi_probe", return_value=(pass_result, True)
            ), mock.patch.object(
                sync, "_renameatx", side_effect=collide_at_output
            ), mock.patch.object(
                sync, "_guarded_unlink", side_effect=fail_hidden_unlink
            ):
                result, success = sync.execute_pi_probe(args)

            self.assertFalse(success)
            self.assertEqual(result["verdict"], "BLOCKED")
            self.assertEqual(
                [path.name for path in evidence.iterdir()
                 if path.name.startswith(".cross-cli-sync.")],
                [],
            )
            for path in evidence.iterdir():
                if path.is_file():
                    if path.name.startswith((
                        f"{output.name}.persistence-unsafe.",
                        f"{output.name}.persistence-pending.",
                    )):
                        continue
                    persisted = json.loads(path.read_text(encoding="utf-8"))
                    self.assertNotEqual(persisted.get("verdict"), "PASS")

    def test_probe_pi_candidate_fsync_failure_quarantines_blocked_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp) / "evidence"
            evidence.mkdir(mode=0o700)
            output = evidence / "pi-review.json"
            args = SimpleNamespace(output=output)
            pass_result = {
                "pi_probe": "pass",
                "reviewer_identity": {
                    "product": "pi",
                    "role": "independent-reviewer",
                    "capability_profile": "control-plane-high",
                },
                "bound_input_hashes": {},
                "verdict": "PASS",
                "findings": [],
            }
            original_fsync = sync.os.fsync
            original_guarded_unlink = sync._guarded_unlink
            fsync_failed = False

            def fail_candidate_fsync(descriptor):
                nonlocal fsync_failed
                if not fsync_failed:
                    fsync_failed = True
                    raise OSError("injected candidate fsync failure")
                return original_fsync(descriptor)

            def fail_hidden_unlink(guard, name, *, missing_ok=False):
                if name.startswith(".cross-cli-sync.") or name.startswith(
                    f"{output.name}.persistence-blocked."
                ):
                    raise OSError("injected candidate unlink failure")
                return original_guarded_unlink(guard, name, missing_ok=missing_ok)

            with mock.patch.object(
                sync, "_execute_pi_probe", return_value=(pass_result, True)
            ), mock.patch.object(
                sync.os, "fsync", side_effect=fail_candidate_fsync
            ), mock.patch.object(
                sync, "_guarded_unlink", side_effect=fail_hidden_unlink
            ):
                result, success = sync.execute_pi_probe(args)

            self.assertTrue(fsync_failed)
            self.assertFalse(success)
            self.assertEqual(result["verdict"], "BLOCKED")
            self.assertEqual(
                [path.name for path in evidence.iterdir()
                 if path.name.startswith(".cross-cli-sync.")],
                [],
            )
            for path in evidence.iterdir():
                self.assertTrue(
                    path.name.startswith(f"{output.name}.persistence-blocked.")
                )
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
                self.assertEqual(
                    json.loads(path.read_text(encoding="utf-8")),
                    sync._blocked_pi_probe_result(),
                )

    def test_probe_pi_candidate_parent_guard_failure_quarantines_blocked_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp) / "evidence"
            evidence.mkdir(mode=0o700)
            output = evidence / "pi-review.json"
            args = SimpleNamespace(output=output)
            pass_result = {
                "pi_probe": "pass",
                "reviewer_identity": {
                    "product": "pi",
                    "role": "independent-reviewer",
                    "capability_profile": "control-plane-high",
                },
                "bound_input_hashes": {},
                "verdict": "PASS",
                "findings": [],
            }
            original_assert_parent_guard = sync._assert_parent_guard
            original_guarded_unlink = sync._guarded_unlink
            guard_failed = False

            def fail_after_candidate(guard, label):
                nonlocal guard_failed
                candidate_exists = any(
                    item.name.startswith((
                        ".cross-cli-sync.",
                        f"{output.name}.persistence-pending.",
                    ))
                    for item in evidence.iterdir()
                )
                if candidate_exists and not guard_failed:
                    guard_failed = True
                    raise OSError("injected candidate parent guard failure")
                return original_assert_parent_guard(guard, label)

            def fail_hidden_unlink(guard, name, *, missing_ok=False):
                if name.startswith((
                    ".cross-cli-sync.",
                    f"{output.name}.persistence-pending.",
                )) or name.startswith(
                    f"{output.name}.persistence-blocked."
                ):
                    raise OSError("injected candidate unlink failure")
                return original_guarded_unlink(guard, name, missing_ok=missing_ok)

            with mock.patch.object(
                sync, "_execute_pi_probe", return_value=(pass_result, True)
            ), mock.patch.object(
                sync, "_assert_parent_guard", side_effect=fail_after_candidate
            ), mock.patch.object(
                sync, "_guarded_unlink", side_effect=fail_hidden_unlink
            ):
                result, success = sync.execute_pi_probe(args)

            self.assertTrue(guard_failed)
            self.assertFalse(success)
            self.assertEqual(result["verdict"], "BLOCKED")
            self.assertEqual(
                [path.name for path in evidence.iterdir()
                 if path.name.startswith(".cross-cli-sync.")],
                [],
            )
            for path in evidence.iterdir():
                self.assertTrue(
                    path.name.startswith(f"{output.name}.persistence-blocked.")
                )
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
                self.assertEqual(
                    json.loads(path.read_text(encoding="utf-8")),
                    sync._blocked_pi_probe_result(),
                )

    def test_probe_pi_persistence_rollback_preserves_same_content_replacement_inode(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp) / "evidence"
            evidence.mkdir(mode=0o700)
            output = evidence / "pi-review.json"
            alias = evidence / "pi-review-alias.json"
            args = SimpleNamespace(output=output)
            pass_result = {
                "pi_probe": "pass",
                "reviewer_identity": {
                    "product": "pi",
                    "role": "independent-reviewer",
                    "capability_profile": "control-plane-high",
                },
                "bound_input_hashes": {},
                "verdict": "PASS",
                "findings": [],
            }
            pass_bytes = sync._canonical_json_bytes(pass_result)
            original_fsync_directory = sync._fsync_directory
            replacement = evidence / "replacement.json"
            replacement_inode = None
            swapped = False

            def swap_same_content_replacement(path):
                nonlocal replacement_inode, swapped
                if Path(path) == evidence and not swapped:
                    replacement.write_bytes(pass_bytes)
                    replacement.chmod(0o600)
                    os.link(replacement, alias)
                    replacement_inode = replacement.stat().st_ino
                    output.unlink()
                    replacement.rename(output)
                    swapped = True
                    raise OSError("injected output directory fsync failure")
                return original_fsync_directory(path)

            with mock.patch.object(
                sync, "_execute_pi_probe", return_value=(pass_result, True)
            ), mock.patch.object(
                sync, "_fsync_directory", side_effect=swap_same_content_replacement
            ):
                result, success = sync.execute_pi_probe(args)

            self.assertTrue(swapped)
            self.assertFalse(success)
            self.assertEqual(result["verdict"], "BLOCKED")
            self.assertFalse(output.exists())
            self.assertTrue(alias.exists())
            recovery = list(evidence.glob(f"{output.name}.persistence-*." + "*"))
            self.assertTrue(recovery)
            self.assertTrue(any(path.name.startswith(f"{output.name}.persistence-unsafe.") for path in recovery))
            unsafe = [
                path for path in recovery
                if path.name.startswith(f"{output.name}.persistence-unsafe.")
            ]
            self.assertTrue(unsafe)
            self.assertEqual(unsafe[0].stat().st_ino, replacement_inode)
            self.assertEqual(alias.stat().st_ino, replacement_inode)
            self.assertEqual(unsafe[0].read_bytes(), pass_bytes)

    def test_probe_pi_persistence_rollback_never_unlinks_installed_output_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp) / "evidence"
            evidence.mkdir(mode=0o700)
            output = evidence / "pi-review.json"
            alias = evidence / "pi-review-alias.json"
            args = SimpleNamespace(output=output)
            pass_result = {
                "pi_probe": "pass",
                "reviewer_identity": {
                    "product": "pi",
                    "role": "independent-reviewer",
                    "capability_profile": "control-plane-high",
                },
                "bound_input_hashes": {},
                "verdict": "PASS",
                "findings": [],
            }
            pass_bytes = sync._canonical_json_bytes(pass_result)
            original_fsync_directory = sync._fsync_directory
            original_guarded_unlink = sync._guarded_unlink
            original_identity_matches = sync._guarded_identity_matches
            replacement = evidence / "replacement.json"
            replacement_inode = None
            swapped = False
            installed_unlink_called = False

            def fail_output_directory(path):
                if Path(path) == evidence:
                    raise OSError("injected output directory fsync failure")
                return original_fsync_directory(path)

            def swap_after_identity_check(guard, name, ownership):
                nonlocal replacement_inode, swapped
                result = original_identity_matches(guard, name, ownership)
                if name == output.name and result and not swapped:
                    replacement.write_bytes(pass_bytes)
                    replacement.chmod(0o600)
                    os.link(replacement, alias)
                    replacement_inode = replacement.stat().st_ino
                    output.unlink()
                    replacement.rename(output)
                    swapped = True
                return result

            def track_installed_unlink(guard, name, *, missing_ok=False):
                nonlocal installed_unlink_called
                if name == output.name:
                    installed_unlink_called = True
                return original_guarded_unlink(
                    guard, name, missing_ok=missing_ok
                )

            with mock.patch.object(
                sync, "_execute_pi_probe", return_value=(pass_result, True)
            ), mock.patch.object(
                sync, "_fsync_directory", side_effect=fail_output_directory
            ), mock.patch.object(
                sync, "_guarded_unlink", side_effect=track_installed_unlink
            ), mock.patch.object(
                sync, "_guarded_identity_matches", side_effect=swap_after_identity_check
            ):
                result, success = sync.execute_pi_probe(args)

            self.assertTrue(swapped)
            self.assertFalse(success)
            self.assertEqual(result["verdict"], "BLOCKED")
            self.assertFalse(installed_unlink_called)
            self.assertFalse(output.exists())
            self.assertTrue(alias.exists())
            recovery = list(evidence.glob(f"{output.name}.persistence-*." + "*"))
            self.assertTrue(recovery)
            self.assertTrue(any(path.name.startswith(f"{output.name}.persistence-unsafe.") for path in recovery))
            unsafe = [
                path for path in recovery
                if path.name.startswith(f"{output.name}.persistence-unsafe.")
            ]
            self.assertTrue(unsafe)
            self.assertEqual(unsafe[0].stat().st_ino, replacement_inode)
            self.assertEqual(alias.stat().st_ino, replacement_inode)
            self.assertEqual(unsafe[0].read_bytes(), pass_bytes)

    @unittest.skipUnless(Path("/usr/bin/sandbox-exec").is_file(), "sandbox-exec required")
    def test_probe_pi_wrapper_allows_its_bound_second_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / "pi-package"
            cli = package / "dist" / "cli.pl"
            cli.parent.mkdir(parents=True)
            (package / "package.json").write_text(
                '{"name":"fake-pi"}\n', encoding="utf-8"
            )
            cli.write_text(
                'print qq({"verdict":"PASS","findings":[]}\\n);\n',
                encoding="utf-8",
            )
            cli.chmod(0o755)
            executable = root / "fake-pi"
            executable.write_text(
                f'#!/bin/sh\nexec /usr/bin/perl {cli} "$@"\n', encoding="utf-8"
            )
            executable.chmod(0o755)
            native = root / "native"
            native.mkdir()
            temporary = root / "probe-temp"
            temporary.mkdir()
            prompt = root / "prompt.md"
            prompt.write_text("Review the bound source and return JSON.\n", encoding="utf-8")
            reviewed = root / "reviewed"
            reviewed.mkdir()
            (reviewed / "input.md").write_text("reviewed bytes\n", encoding="utf-8")
            evidence = root / "evidence"
            evidence.mkdir(mode=0o700)
            output = evidence / "pi-review.json"
            result, success = sync.execute_pi_probe(
                SimpleNamespace(
                    pi_executable=executable,
                    native_pi_root=native,
                    temporary_root=temporary,
                    prompt_file=prompt,
                    read_root=[reviewed],
                    output=output,
                )
            )
            self.assertTrue(success)
            self.assertEqual(result["pi_probe"], "pass")
            self.assertEqual(result["verdict"], "PASS")

    @unittest.skipUnless(Path("/usr/bin/sandbox-exec").is_file(), "sandbox-exec required")
    def test_probe_pi_executes_snapshot_not_post_build_source_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / "pi-package"
            cli = package / "dist" / "cli.pl"
            cli.parent.mkdir(parents=True)
            (package / "package.json").write_text(
                '{"name":"fake-pi"}\n', encoding="utf-8"
            )
            cli.write_text(
                'print qq({"verdict":"BLOCKED","findings":[]}\\n);\n',
                encoding="utf-8",
            )
            cli.chmod(0o755)
            executable = root / "fake-pi"
            executable.write_text(
                f'#!/bin/sh\nexec /usr/bin/perl {cli} "$@"\n', encoding="utf-8"
            )
            executable.chmod(0o755)
            native = root / "native"
            native.mkdir()
            temporary = root / "probe-temp"
            temporary.mkdir()
            prompt = root / "prompt.md"
            prompt.write_text("Return JSON.\n", encoding="utf-8")
            reviewed = root / "reviewed"
            reviewed.mkdir()
            (reviewed / "input.md").write_text("reviewed bytes\n", encoding="utf-8")
            evidence = root / "evidence"
            evidence.mkdir(mode=0o700)
            output = evidence / "pi-review.json"
            original_run = sync.subprocess.run

            def mutate_source_then_run(*args, **kwargs):
                cli.write_text(
                    'print qq({"verdict":"PASS","findings":[]}\\n);\n',
                    encoding="utf-8",
                )
                cli.chmod(0o755)
                return original_run(*args, **kwargs)

            with mock.patch.object(
                sync.subprocess, "run", side_effect=mutate_source_then_run
            ):
                result, success = sync.execute_pi_probe(
                    SimpleNamespace(
                        pi_executable=executable,
                        native_pi_root=native,
                        temporary_root=temporary,
                        prompt_file=prompt,
                        read_root=[reviewed],
                        output=output,
                    )
                )
            self.assertTrue(success)
            self.assertEqual(result["verdict"], "BLOCKED")

    @unittest.skipUnless(Path("/usr/bin/sandbox-exec").is_file(), "sandbox-exec required")
    def test_probe_pi_rejects_post_snapshot_entrypoint_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = root / "pi-package"
            cli = package / "dist" / "cli.pl"
            cli.parent.mkdir(parents=True)
            (package / "package.json").write_text(
                '{"name":"fake-pi"}\n', encoding="utf-8"
            )
            cli.write_text(
                'print qq({"verdict":"BLOCKED","findings":[]}\\n);\n',
                encoding="utf-8",
            )
            cli.chmod(0o755)
            executable = root / "fake-pi"
            executable.write_text(
                f'#!/bin/sh\nexec /usr/bin/perl {cli} "$@"\n', encoding="utf-8"
            )
            executable.chmod(0o755)
            native = root / "native"
            native.mkdir()
            temporary = root / "probe-temp"
            temporary.mkdir()
            prompt = root / "prompt.md"
            prompt.write_text("Return JSON.\n", encoding="utf-8")
            reviewed = root / "reviewed"
            reviewed.mkdir()
            (reviewed / "input.md").write_text("reviewed bytes\n", encoding="utf-8")
            evidence = root / "evidence"
            evidence.mkdir(mode=0o700)
            output = evidence / "pi-review.json"
            original_run = sync.subprocess.run

            def mutate_snapshot_then_run(command, *args, **kwargs):
                snapshot_entrypoint = Path(command[5])
                snapshot_entrypoint.chmod(0o644)
                snapshot_entrypoint.write_text(
                    'print qq({"verdict":"PASS","findings":[]}\\n);\n',
                    encoding="utf-8",
                )
                snapshot_entrypoint.chmod(0o444)
                return original_run(command, *args, **kwargs)

            with mock.patch.object(
                sync.subprocess, "run", side_effect=mutate_snapshot_then_run
            ):
                result, success = sync.execute_pi_probe(
                    SimpleNamespace(
                        pi_executable=executable,
                        native_pi_root=native,
                        temporary_root=temporary,
                        prompt_file=prompt,
                        read_root=[reviewed],
                        output=output,
                    )
                )
            self.assertFalse(success)
            self.assertEqual(result["pi_probe"], "blocked")
            self.assertEqual(result["verdict"], "BLOCKED")

    def test_native_target_verification_never_invokes_pi_probe(self):
        source = inspect.getsource(sync.verify_target)
        self.assertNotIn("build_pi_probe(", source)
        self.assertNotIn("subprocess", source)

    @unittest.skipUnless(Path("/usr/bin/sandbox-exec").is_file(), "sandbox-exec required")
    def test_probe_pi_wrapper_sanitizes_a_fake_isolated_process(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "fake-pi"
            executable.write_text(
                "#!/usr/bin/perl\n"
                "print qq({\\\"verdict\\\":\\\"PASS\\\","
                "\\\"findings\\\":[]}\\n);\n",
                encoding="utf-8",
            )
            executable.chmod(0o755)
            native = root / "native"
            native.mkdir()
            temporary = root / "probe-temp"
            temporary.mkdir()
            prompt = root / "prompt.md"
            prompt.write_text("Review the bound source and return JSON.\n", encoding="utf-8")
            reviewed = root / "reviewed"
            reviewed.mkdir()
            (reviewed / "input.md").write_text("reviewed bytes\n", encoding="utf-8")
            evidence = root / "evidence"
            evidence.mkdir(mode=0o700)
            output = evidence / "pi-review.json"
            result, success = sync.execute_pi_probe(
                SimpleNamespace(
                    pi_executable=executable,
                    native_pi_root=native,
                    temporary_root=temporary,
                    prompt_file=prompt,
                    read_root=[reviewed],
                    output=output,
                )
            )
            self.assertTrue(success)
            self.assertEqual(result["pi_probe"], "pass")
            self.assertEqual(result["verdict"], "PASS")
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o600)
            persisted = output.read_text(encoding="utf-8")
            self.assertNotIn(str(native.resolve()), persisted)
            self.assertNotIn("reviewed bytes", persisted)


class DurableTargetTransactionTests(unittest.TestCase):
    def _rewrite_receipt(self, path: Path, receipt: dict) -> None:
        path.write_bytes(sync._canonical_json_bytes(receipt))
        path.chmod(0o600)

    def _advance_target(self, fixture: dict, target_id: str) -> Path:
        receipt = fixture["transaction_root"] / f"{target_id}.json"
        sync.apply_target(
            fixture["plan"],
            target_id,
            fixture["backup_root"],
            receipt,
            plan_sha256=fixture["plan_sha256"],
        )
        sync.verify_target_with_receipt(
            fixture["plan"],
            target_id,
            receipt,
            plan_sha256=fixture["plan_sha256"],
        )
        inspect_json = None
        if target_id == "grok-cli":
            inspect_json = fixture["transaction_root"] / "grok-inspect.json"
            root = fixture["plan"]["targets"][target_id]["skills_root"]
            payload = {
                "skills": [
                    {
                        "name": name,
                        "source": {
                            "type": "user",
                            "path": f"{root}/{name}/SKILL.md",
                        },
                    }
                    for name in SKILLS
                ]
            }
            inspect_json.write_text(json.dumps(payload), encoding="utf-8")
            inspect_json.chmod(0o600)
        sync.verify_discovery_with_receipt(
            fixture["plan"],
            target_id,
            receipt,
            plan_sha256=fixture["plan_sha256"],
            inspect_json=inspect_json,
        )
        sync.commit_target(
            fixture["plan"],
            target_id,
            receipt,
            plan_sha256=fixture["plan_sha256"],
        )
        return receipt

    def test_apply_rejects_backup_root_inside_any_discovery_root_before_mutation(self):
        for discovery_target in sync.TARGET_ORDER:
            with self.subTest(discovery_target=discovery_target):
                with tempfile.TemporaryDirectory() as tmp:
                    fixture = create_v6_sync_fixture(Path(tmp))
                    unsafe_backup = (
                        Path(
                            fixture["plan"]["targets"][discovery_target][
                                "skills_root"
                            ]
                        )
                        / ".runtime-backups"
                    )
                    receipt = fixture["transaction_root"] / "codex.json"
                    with self.assertRaisesRegex(
                        ValueError, "outside every Skill discovery root"
                    ):
                        sync.apply_target(
                            fixture["plan"],
                            "codex",
                            unsafe_backup,
                            receipt,
                            plan_sha256=fixture["plan_sha256"],
                        )
                    self.assertFalse(unsafe_backup.exists())
                    self.assertFalse(receipt.exists())
                    self.assertTrue(
                        sync._assert_target_prestate(fixture["plan"], "codex")
                    )

    def test_apply_rejects_transaction_root_inside_any_discovery_root_before_mutation(self):
        for discovery_target in sync.TARGET_ORDER:
            with self.subTest(discovery_target=discovery_target):
                with tempfile.TemporaryDirectory() as tmp:
                    fixture = create_v6_sync_fixture(Path(tmp))
                    unsafe_transaction = (
                        Path(
                            fixture["plan"]["targets"][discovery_target][
                                "skills_root"
                            ]
                        )
                        / ".runtime-transactions"
                    )
                    receipt = unsafe_transaction / "codex.json"
                    with self.assertRaisesRegex(
                        ValueError, "outside every Skill discovery root"
                    ):
                        sync.apply_target(
                            fixture["plan"],
                            "codex",
                            fixture["backup_root"],
                            receipt,
                            plan_sha256=fixture["plan_sha256"],
                        )
                    self.assertFalse(unsafe_transaction.exists())
                    self.assertFalse(fixture["backup_root"].exists())
                    self.assertTrue(
                        sync._assert_target_prestate(fixture["plan"], "codex")
                    )

    def test_receipt_is_durable_before_mutation_and_requires_both_digests(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            receipt = sync.apply_target(
                fixture["plan"],
                "codex",
                fixture["backup_root"],
                receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            self.assertEqual(receipt["state"], "applied-uncommitted")
            self.assertEqual(stat.S_IMODE(receipt_path.stat().st_mode), 0o600)
            self.assertEqual(
                stat.S_IMODE(fixture["transaction_root"].stat().st_mode), 0o700
            )
            history = fixture["transaction_root"] / "history"
            states = [
                json.loads(path.read_text(encoding="utf-8"))["state"]
                for path in sorted(history.glob("codex-revision-*.json"))
            ]
            self.assertEqual(states[0], "prepared")
            self.assertGreaterEqual(len(states), 2)
            self.assertEqual(set(states[1:]), {"mutation-intent"})
            with self.assertRaises(ValueError):
                sync.commit_target(
                    fixture["plan"], "codex", receipt_path,
                    plan_sha256=fixture["plan_sha256"],
                )
            sync.verify_target_with_receipt(
                fixture["plan"], "codex", receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            with self.assertRaises(ValueError):
                sync.commit_target(
                    fixture["plan"], "codex", receipt_path,
                    plan_sha256=fixture["plan_sha256"],
                )
            sync.verify_discovery_with_receipt(
                fixture["plan"], "codex", receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            committed = sync.commit_target(
                fixture["plan"], "codex", receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            self.assertEqual(committed, {"commit": "pass", "target": "codex"})
            final, _ = sync._read_receipt(receipt_path)
            self.assertEqual(final["state"], "verified")

    def test_four_target_order_and_verify_all_require_verified_pi(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            codex_receipt = fixture["transaction_root"] / "codex.json"
            sync.apply_target(
                fixture["plan"], "codex", fixture["backup_root"], codex_receipt,
                plan_sha256=fixture["plan_sha256"],
            )
            with self.assertRaisesRegex(ValueError, "prior target"):
                sync.apply_target(
                    fixture["plan"], "pi", fixture["backup_root"],
                    fixture["transaction_root"] / "pi.json",
                    plan_sha256=fixture["plan_sha256"],
                )
            sync.verify_target_with_receipt(
                fixture["plan"], "codex", codex_receipt,
                plan_sha256=fixture["plan_sha256"],
            )
            sync.verify_discovery_with_receipt(
                fixture["plan"], "codex", codex_receipt,
                plan_sha256=fixture["plan_sha256"],
            )
            sync.commit_target(
                fixture["plan"], "codex", codex_receipt,
                plan_sha256=fixture["plan_sha256"],
            )
            with self.assertRaises(ValueError):
                sync.verify_all_receipts(
                    fixture["plan"], fixture["transaction_root"],
                    plan_sha256=fixture["plan_sha256"],
                )
            for target_id in ("pi", "antigravity-cli", "grok-cli"):
                self._advance_target(fixture, target_id)
            self.assertEqual(
                sync.verify_all_receipts(
                    fixture["plan"], fixture["transaction_root"],
                    plan_sha256=fixture["plan_sha256"],
                ),
                {"verify_all": "pass", "targets": list(sync.TARGET_ORDER)},
            )

    @unittest.skipUnless(hasattr(os, "fork"), "crash recovery requires fork")
    def test_real_apply_crash_points_are_recoverable_or_manual(self):
        scenarios = (
            ("after-backup-before-prepared", None),
            ("after-prepared-before-intent", "prepared"),
            ("after-first-destination-write", "mutation-intent"),
            ("after-last-destination-fsync-before-applied", "mutation-intent"),
        )
        for crash_point, expected_state in scenarios:
            with self.subTest(crash_point=crash_point), tempfile.TemporaryDirectory() as tmp:
                fixture = create_v6_sync_fixture(Path(tmp))
                receipt_path = fixture["transaction_root"] / "codex.json"
                pid = os.fork()
                if pid == 0:
                    def crash_hook(point):
                        if point == crash_point:
                            os._exit(91)
                    sync.apply_target(
                        fixture["plan"], "codex", fixture["backup_root"],
                        receipt_path, plan_sha256=fixture["plan_sha256"],
                        crash_hook=crash_hook,
                    )
                    os._exit(0)
                _, status = os.waitpid(pid, 0)
                self.assertEqual(os.waitstatus_to_exitcode(status), 91)
                if expected_state is None:
                    self.assertFalse(receipt_path.exists())
                    with self.assertRaisesRegex(ValueError, "orphaned backup"):
                        sync.recover_pending(
                            fixture["plan"], fixture["backup_root"],
                            fixture["transaction_root"],
                            plan_sha256=fixture["plan_sha256"],
                        )
                    self.assertTrue(
                        (fixture["transaction_root"] /
                         "codex.manual-disposition.json").is_file()
                    )
                    continue
                receipt, _ = sync._read_receipt(receipt_path)
                self.assertEqual(receipt["state"], expected_state)
                recovered = sync.recover_pending(
                    fixture["plan"], fixture["backup_root"],
                    fixture["transaction_root"],
                    plan_sha256=fixture["plan_sha256"],
                )
                self.assertEqual(recovered["recovery"], "pass")
                self.assertTrue(recovered["restored"])
                restored, _ = sync._read_receipt(receipt_path)
                self.assertEqual(restored["state"], "restored")
                sync._assert_target_prestate(fixture["plan"], "codex")
                self.assertFalse(
                    (fixture["transaction_root"] / "pi.json").exists()
                )

    def test_orphaned_receipt_temporary_requires_manual_disposition(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            orphan = fixture["transaction_root"] / ".codex.json.tmp-orphan"
            orphan.write_text("untrusted receipt bytes\n", encoding="utf-8")
            orphan.chmod(0o600)
            with self.assertRaisesRegex(ValueError, "orphaned receipt temporary"):
                sync.recover_pending(
                    fixture["plan"], fixture["backup_root"],
                    fixture["transaction_root"],
                    plan_sha256=fixture["plan_sha256"],
                )
            disposition = (
                fixture["transaction_root"]
                / "codex.manual-disposition.json"
            )
            self.assertTrue(disposition.is_file())
            self.assertEqual(stat.S_IMODE(disposition.stat().st_mode), 0o600)
            payload = json.loads(disposition.read_text(encoding="utf-8"))
            self.assertEqual(payload["category"], "orphaned-receipt-temporary")
            self.assertEqual(payload["receipt_sha256"], sync._sha256(orphan))

    def test_receipt_advance_restores_concurrent_receipt_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            sync.apply_target(
                fixture["plan"], "codex", fixture["backup_root"], receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            current, _ = sync._read_receipt(receipt_path)
            drifted = dict(current, transaction_id="concurrent-receipt-drift")
            drifted_bytes = sync._canonical_json_bytes(drifted)
            original_rename = sync._renameatx
            injected = False

            def drift_before_receipt_swap(source, destination, flags, **kwargs):
                nonlocal injected
                if (
                    not injected
                    and Path(destination).name == receipt_path.name
                    and flags == sync.RENAME_SWAP
                ):
                    receipt_path.write_bytes(drifted_bytes)
                    receipt_path.chmod(0o600)
                    injected = True
                return original_rename(source, destination, flags, **kwargs)

            with mock.patch.object(
                sync, "_renameatx", side_effect=drift_before_receipt_swap
            ):
                with self.assertRaisesRegex(ValueError, "receipt.*drift"):
                    sync._advance_receipt(
                        receipt_path,
                        "recovery-blocked",
                        recovery_reason="test drift",
                    )
            self.assertTrue(injected)
            self.assertEqual(receipt_path.read_bytes(), drifted_bytes)
            self.assertEqual(
                list(fixture["transaction_root"].glob(".codex.json.tmp-*")), []
            )

    def test_receipt_advance_preserves_displaced_state_when_rollback_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            sync.apply_target(
                fixture["plan"], "codex", fixture["backup_root"], receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            current, _ = sync._read_receipt(receipt_path)
            drifted = dict(current, transaction_id="preserved-receipt-drift")
            drifted_bytes = sync._canonical_json_bytes(drifted)
            original_rename = sync._renameatx
            exchange_calls = 0

            def block_receipt_rollback(source, destination, flags, **kwargs):
                nonlocal exchange_calls
                if flags == sync.RENAME_SWAP and Path(destination).name == receipt_path.name:
                    exchange_calls += 1
                    if exchange_calls == 1:
                        receipt_path.write_bytes(drifted_bytes)
                        receipt_path.chmod(0o600)
                    elif exchange_calls == 2:
                        raise OSError("injected receipt rollback failure")
                return original_rename(source, destination, flags, **kwargs)

            with mock.patch.object(
                sync, "_renameatx", side_effect=block_receipt_rollback
            ):
                with self.assertRaisesRegex(ValueError, "rollback.*blocked"):
                    sync._advance_receipt(
                        receipt_path,
                        "recovery-blocked",
                        recovery_reason="test rollback",
                    )
            self.assertEqual(exchange_calls, 2)
            orphans = list(fixture["transaction_root"].glob(".codex.json.tmp-*"))
            self.assertEqual(len(orphans), 1)
            self.assertEqual(orphans[0].read_bytes(), drifted_bytes)
            with self.assertRaisesRegex(ValueError, "orphaned receipt temporary"):
                sync._require_prior_targets_verified(
                    fixture["transaction_root"], "pi", fixture["plan_sha256"]
                )

    def test_receipt_history_collision_restores_live_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            sync.apply_target(
                fixture["plan"], "codex", fixture["backup_root"], receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            current, _ = sync._read_receipt(receipt_path)
            current_bytes = receipt_path.read_bytes()
            collision = (
                fixture["transaction_root"]
                / "history"
                / f"codex-revision-{current['revision']}.json"
            )
            collision.write_bytes(b"occupied history evidence\n")
            collision.chmod(0o600)
            with self.assertRaises(OSError):
                sync._advance_receipt(
                    receipt_path,
                    "recovery-blocked",
                    recovery_reason="test collision",
                )
            self.assertEqual(receipt_path.read_bytes(), current_bytes)
            self.assertEqual(collision.read_bytes(), b"occupied history evidence\n")

    def test_unknown_current_digest_becomes_recovery_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            sync.apply_target(
                fixture["plan"], "codex", fixture["backup_root"], receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            destination = Path(
                fixture["plan"]["targets"]["codex"]["files"][0]["destination"]
            )
            destination.write_text("unknown external bytes\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "recovery is blocked"):
                sync.restore_target(
                    fixture["plan"], "codex", fixture["backup_root"], receipt_path,
                    plan_sha256=fixture["plan_sha256"],
                )
            blocked, _ = sync._read_receipt(receipt_path)
            self.assertEqual(blocked["state"], "recovery-blocked")
            self.assertFalse((fixture["transaction_root"] / "pi.json").exists())

    def test_restore_rejects_post_check_existing_file_drift_at_swap_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            sync.apply_target(
                fixture["plan"], "codex", fixture["backup_root"], receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            target = Path(fixture["plan"]["targets"]["codex"]["rule_file"])
            original_rename = sync._renameatx
            injected = False

            def drift_before_restore_swap(source, destination, flags, **kwargs):
                nonlocal injected
                if (
                    not injected
                    and Path(destination).name == target.name
                    and flags == sync.RENAME_SWAP
                ):
                    target.write_text("external-restore-drift\n", encoding="utf-8")
                    target.chmod(0o644)
                    injected = True
                return original_rename(source, destination, flags, **kwargs)

            with mock.patch.object(
                sync, "_renameatx", side_effect=drift_before_restore_swap
            ):
                with self.assertRaisesRegex(ValueError, "recovery is blocked"):
                    sync.restore_target(
                        fixture["plan"], "codex", fixture["backup_root"], receipt_path,
                        plan_sha256=fixture["plan_sha256"],
                    )
            self.assertTrue(injected)
            self.assertFalse(target.exists())
            unsafe = list(target.parent.glob(f"{target.name}.transaction-unsafe.*"))
            self.assertTrue(unsafe)
            self.assertTrue(
                any(path.read_bytes() == b"external-restore-drift\n" for path in unsafe)
            )
            blocked, _ = sync._read_receipt(receipt_path)
            self.assertEqual(blocked["state"], "recovery-blocked")
            self.assertFalse((fixture["transaction_root"] / "pi.json").exists())

    def test_restore_rejects_post_check_absent_file_drift_at_remove_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            sync.apply_target(
                fixture["plan"], "codex", fixture["backup_root"], receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            target = Path(
                fixture["plan"]["targets"]["codex"]["files"][0]["destination"]
            )
            original_rename = sync._renameatx
            injected = False

            def drift_before_remove(source, destination, flags, **kwargs):
                nonlocal injected
                if (
                    not injected
                    and Path(source).name == target.name
                    and flags == sync.RENAME_EXCL
                ):
                    target.write_text("external-remove-drift\n", encoding="utf-8")
                    target.chmod(0o644)
                    injected = True
                return original_rename(source, destination, flags, **kwargs)

            with mock.patch.object(sync, "_renameatx", side_effect=drift_before_remove):
                with self.assertRaisesRegex(ValueError, "recovery is blocked"):
                    sync.restore_target(
                        fixture["plan"], "codex", fixture["backup_root"], receipt_path,
                        plan_sha256=fixture["plan_sha256"],
                    )
            self.assertTrue(injected)
            self.assertEqual(
                target.read_text(encoding="utf-8"), "external-remove-drift\n"
            )
            blocked, _ = sync._read_receipt(receipt_path)
            self.assertEqual(blocked["state"], "recovery-blocked")
            self.assertFalse((fixture["transaction_root"] / "pi.json").exists())

    def test_restore_remove_rejects_parent_mapping_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            parent = root / "runtime"
            parent.mkdir()
            target = parent / "created.md"
            target.write_bytes(b"candidate\n")
            expected = sync.capture_destination_prestate(target)
            moved_parent = root / "runtime-reviewed"
            original_rename = sync._renameatx
            injected = False

            def replace_parent_before_remove(source, destination, flags, **kwargs):
                nonlocal injected
                if not injected and flags == sync.RENAME_EXCL:
                    parent.rename(moved_parent)
                    parent.mkdir()
                    target.write_bytes(b"candidate\n")
                    target.chmod(0o644)
                    injected = True
                return original_rename(source, destination, flags, **kwargs)

            with mock.patch.object(
                sync, "_renameatx", side_effect=replace_parent_before_remove
            ):
                with self.assertRaisesRegex(ValueError, "parent.*drift"):
                    sync._atomic_remove_if_matches(target, expected, "parent-remove")
            self.assertTrue(injected)
            self.assertEqual((moved_parent / target.name).read_bytes(), b"candidate\n")
            self.assertEqual(target.read_bytes(), b"candidate\n")

    def test_apply_binds_new_multilevel_parent_before_candidate_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            target = Path(
                fixture["plan"]["targets"]["codex"]["files"][0]["destination"]
            )
            created_root = Path(
                fixture["plan"]["targets"]["codex"]["skills_root"]
            ) / "openspec-superpower-change"
            parked_root = created_root.with_name("openspec-reviewed-parent")
            original_create = sync.atomic_create
            injected = False

            def remap_before_candidate(path, content, **kwargs):
                nonlocal injected
                if not injected and Path(path) == target:
                    created_root.rename(parked_root)
                    created_root.mkdir()
                    injected = True
                return original_create(path, content, **kwargs)

            with mock.patch.object(
                sync, "atomic_create", side_effect=remap_before_candidate
            ):
                with self.assertRaisesRegex(ValueError, "parent.*drift|recovery.*blocked"):
                    sync.apply_target(
                        fixture["plan"],
                        "codex",
                        fixture["backup_root"],
                        receipt_path,
                        plan_sha256=fixture["plan_sha256"],
                    )
            self.assertTrue(injected)
            self.assertFalse(target.exists())
            self.assertFalse((parked_root / target.name).exists())

    def test_apply_rejects_new_parent_link_substitution_before_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            target = Path(
                fixture["plan"]["targets"]["codex"]["files"][0]["destination"]
            )
            created_root = Path(
                fixture["plan"]["targets"]["codex"]["skills_root"]
            ) / "openspec-superpower-change"
            parked_root = created_root.with_name("openspec-reviewed-parent")
            outside = Path(tmp) / "replacement-parent"
            outside.mkdir()
            original_create = sync.atomic_create
            injected = False

            def substitute_before_candidate(path, content, **kwargs):
                nonlocal injected
                if not injected and Path(path) == target:
                    created_root.rename(parked_root)
                    created_root.symlink_to(outside, target_is_directory=True)
                    injected = True
                return original_create(path, content, **kwargs)

            with mock.patch.object(
                sync, "atomic_create", side_effect=substitute_before_candidate
            ):
                with self.assertRaisesRegex(ValueError, "parent.*drift|recovery.*blocked"):
                    sync.apply_target(
                        fixture["plan"],
                        "codex",
                        fixture["backup_root"],
                        receipt_path,
                        plan_sha256=fixture["plan_sha256"],
                    )
            self.assertTrue(injected)
            self.assertFalse((outside / target.name).exists())
            self.assertFalse((parked_root / target.name).exists())

    def test_apply_rejects_new_parent_type_substitution_before_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            target = Path(
                fixture["plan"]["targets"]["codex"]["files"][0]["destination"]
            )
            created_root = Path(
                fixture["plan"]["targets"]["codex"]["skills_root"]
            ) / "openspec-superpower-change"
            parked_root = created_root.with_name("openspec-reviewed-parent")
            original_create = sync.atomic_create
            injected = False

            def substitute_before_candidate(path, content, **kwargs):
                nonlocal injected
                if not injected and Path(path) == target:
                    created_root.rename(parked_root)
                    created_root.write_bytes(b"replacement type\n")
                    injected = True
                return original_create(path, content, **kwargs)

            with mock.patch.object(
                sync, "atomic_create", side_effect=substitute_before_candidate
            ):
                with self.assertRaisesRegex(ValueError, "parent.*drift|recovery.*blocked"):
                    sync.apply_target(
                        fixture["plan"],
                        "codex",
                        fixture["backup_root"],
                        receipt_path,
                        plan_sha256=fixture["plan_sha256"],
                    )
            self.assertTrue(injected)
            self.assertTrue(created_root.is_file())
            self.assertFalse((parked_root / target.name).exists())

    def test_receipt_durably_binds_every_created_parent_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            sync.apply_target(
                fixture["plan"],
                "codex",
                fixture["backup_root"],
                receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            receipt, _ = sync._read_receipt(receipt_path)
            self.assertIn("created_parent_records", receipt)
            records = receipt.get("created_parent_records", [])
            planned = {
                raw_parent
                for entry in sync._load_verified_backup_manifest(
                    receipt, fixture["backup_root"], "codex", fixture["plan_sha256"]
                )[0]["entries"]
                for raw_parent in entry["created_parents"]
            }
            self.assertEqual({record["logical_path"] for record in records}, planned)
            for record in records:
                self.assertEqual(set(record), {"logical_path", "path", "chain"})
                self.assertEqual(record["chain"][-1]["path"], record["path"])
                self.assertEqual(len(record["chain"][-1]["identity"]), 5)

    def test_restore_rejects_created_parent_logical_path_chain_substitution(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            sync.apply_target(
                fixture["plan"],
                "codex",
                fixture["backup_root"],
                receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            receipt, _ = sync._read_receipt(receipt_path)
            actual_records = receipt["created_parent_records"]
            candidate = Path(
                fixture["plan"]["targets"]["codex"]["files"][0]["destination"]
            )
            unrelated_root = Path(tmp) / "unrelated-created-parents"
            unrelated_root.mkdir()
            unrelated_paths = []
            substituted_records = []
            for index, record in enumerate(actual_records):
                unrelated = unrelated_root / f"directory-{index}"
                unrelated.mkdir()
                unrelated = unrelated.resolve(strict=True)
                unrelated_paths.append(unrelated)
                chain = sync._capture_directory_chain(unrelated, "test unrelated parent")
                substituted_records.append(
                    {
                        "logical_path": record["logical_path"],
                        "path": os.fspath(unrelated),
                        "chain": sync._directory_chain_value(chain),
                    }
                )
            retained = unrelated_paths[0] / "retained-state.txt"
            retained.write_bytes(b"unrelated state\n")
            receipt["created_parent_records"] = substituted_records
            self._rewrite_receipt(receipt_path, receipt)

            with self.assertRaisesRegex(ValueError, "recovery is blocked"):
                sync.restore_target(
                    fixture["plan"],
                    "codex",
                    fixture["backup_root"],
                    receipt_path,
                    plan_sha256=fixture["plan_sha256"],
                )

            self.assertTrue(candidate.is_file())
            self.assertTrue(all(path.is_dir() for path in unrelated_paths))
            self.assertEqual(retained.read_bytes(), b"unrelated state\n")
            self.assertTrue(
                all(Path(record["path"]).is_dir() for record in actual_records)
            )
            blocked, _ = sync._read_receipt(receipt_path)
            self.assertEqual(blocked["state"], "recovery-blocked")
            with self.assertRaisesRegex(ValueError, "prior target"):
                sync._require_prior_targets_verified(
                    fixture["transaction_root"], "pi", fixture["plan_sha256"]
                )
            with self.assertRaisesRegex(ValueError, "manual disposition"):
                sync.recover_pending(
                    fixture["plan"],
                    fixture["backup_root"],
                    fixture["transaction_root"],
                    plan_sha256=fixture["plan_sha256"],
                )

    def test_restore_rejects_reordered_created_parent_records_before_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            sync.apply_target(
                fixture["plan"],
                "codex",
                fixture["backup_root"],
                receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            receipt, _ = sync._read_receipt(receipt_path)
            candidate = Path(
                fixture["plan"]["targets"]["codex"]["files"][0]["destination"]
            )
            receipt["created_parent_records"] = list(
                reversed(receipt["created_parent_records"])
            )
            self._rewrite_receipt(receipt_path, receipt)

            with self.assertRaisesRegex(ValueError, "recovery is blocked"):
                sync.restore_target(
                    fixture["plan"],
                    "codex",
                    fixture["backup_root"],
                    receipt_path,
                    plan_sha256=fixture["plan_sha256"],
                )
            self.assertTrue(candidate.is_file())

    def test_restore_rejects_truncated_created_parent_chain_before_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            sync.apply_target(
                fixture["plan"],
                "codex",
                fixture["backup_root"],
                receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            receipt, _ = sync._read_receipt(receipt_path)
            candidate = Path(
                fixture["plan"]["targets"]["codex"]["files"][0]["destination"]
            )
            first = receipt["created_parent_records"][0]
            self.assertGreater(len(first["chain"]), 2)
            first["chain"] = first["chain"][-2:]
            self._rewrite_receipt(receipt_path, receipt)

            with self.assertRaisesRegex(ValueError, "recovery is blocked"):
                sync.restore_target(
                    fixture["plan"],
                    "codex",
                    fixture["backup_root"],
                    receipt_path,
                    plan_sha256=fixture["plan_sha256"],
                )
            self.assertTrue(candidate.is_file())

    def test_restore_rejects_created_parent_hierarchy_or_identity_mismatch(self):
        for mutation in ("hierarchy", "identity"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                fixture = create_v6_sync_fixture(Path(tmp))
                receipt_path = fixture["transaction_root"] / "codex.json"
                sync.apply_target(
                    fixture["plan"],
                    "codex",
                    fixture["backup_root"],
                    receipt_path,
                    plan_sha256=fixture["plan_sha256"],
                )
                receipt, _ = sync._read_receipt(receipt_path)
                records = receipt["created_parent_records"]
                self.assertGreater(len(records), 1)
                candidate = Path(
                    fixture["plan"]["targets"]["codex"]["files"][0]["destination"]
                )
                if mutation == "hierarchy":
                    records[0]["path"], records[-1]["path"] = (
                        records[-1]["path"],
                        records[0]["path"],
                    )
                    records[0]["chain"], records[-1]["chain"] = (
                        records[-1]["chain"],
                        records[0]["chain"],
                    )
                else:
                    records[0]["chain"][-1]["identity"] = list(
                        records[1]["chain"][-1]["identity"]
                    )
                self._rewrite_receipt(receipt_path, receipt)

                with self.assertRaisesRegex(ValueError, "recovery is blocked"):
                    sync.restore_target(
                        fixture["plan"],
                        "codex",
                        fixture["backup_root"],
                        receipt_path,
                        plan_sha256=fixture["plan_sha256"],
                    )
                self.assertTrue(candidate.is_file())

    def test_restore_rejects_missing_or_extra_created_parent_records(self):
        for mutation in ("missing", "extra"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                fixture = create_v6_sync_fixture(Path(tmp))
                receipt_path = fixture["transaction_root"] / "codex.json"
                sync.apply_target(
                    fixture["plan"],
                    "codex",
                    fixture["backup_root"],
                    receipt_path,
                    plan_sha256=fixture["plan_sha256"],
                )
                receipt, _ = sync._read_receipt(receipt_path)
                candidate = Path(
                    fixture["plan"]["targets"]["codex"]["files"][0]["destination"]
                )
                if mutation == "missing":
                    receipt["created_parent_records"] = receipt[
                        "created_parent_records"
                    ][:-1]
                else:
                    unrelated = Path(tmp) / "extra-created-parent"
                    unrelated.mkdir()
                    unrelated = unrelated.resolve(strict=True)
                    receipt["created_parent_records"].append(
                        {
                            "logical_path": os.fspath(unrelated),
                            "path": os.fspath(unrelated),
                            "chain": sync._directory_chain_value(
                                sync._capture_directory_chain(
                                    unrelated, "test extra parent"
                                )
                            ),
                        }
                    )
                self._rewrite_receipt(receipt_path, receipt)

                with self.assertRaisesRegex(ValueError, "recovery is blocked"):
                    sync.restore_target(
                        fixture["plan"],
                        "codex",
                        fixture["backup_root"],
                        receipt_path,
                        plan_sha256=fixture["plan_sha256"],
                    )
                self.assertTrue(candidate.is_file())

    def test_restore_preserves_replacement_for_created_parent_and_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            sync.apply_target(
                fixture["plan"],
                "codex",
                fixture["backup_root"],
                receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            receipt, _ = sync._read_receipt(receipt_path)
            manifest, _ = sync._load_verified_backup_manifest(
                receipt, fixture["backup_root"], "codex", fixture["plan_sha256"]
            )
            final_absent = Path(
                next(
                    entry["path"]
                    for entry in manifest["entries"]
                    if entry["pre_state"]["kind"] == "absent"
                )
            )
            created_root = Path(
                fixture["plan"]["targets"]["codex"]["skills_root"]
            ) / "openspec-superpower-change"
            parked_root = created_root.with_name("openspec-reviewed-parent")
            original_remove = sync._atomic_remove_if_matches
            injected = False

            def remap_after_last_leaf(path, expected_state, label):
                nonlocal injected
                result = original_remove(path, expected_state, label)
                if not injected and Path(path) == final_absent:
                    created_root.rename(parked_root)
                    created_root.mkdir()
                    injected = True
                return result

            with mock.patch.object(
                sync, "_atomic_remove_if_matches", side_effect=remap_after_last_leaf
            ):
                with self.assertRaisesRegex(ValueError, "recovery is blocked"):
                    sync.restore_target(
                        fixture["plan"],
                        "codex",
                        fixture["backup_root"],
                        receipt_path,
                        plan_sha256=fixture["plan_sha256"],
                    )
            self.assertTrue(injected)
            self.assertTrue(created_root.is_dir())
            self.assertTrue(parked_root.is_dir())
            blocked, _ = sync._read_receipt(receipt_path)
            self.assertEqual(blocked["state"], "recovery-blocked")

    def test_restore_preserves_nonempty_created_parent_and_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            sync.apply_target(
                fixture["plan"],
                "codex",
                fixture["backup_root"],
                receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            receipt, _ = sync._read_receipt(receipt_path)
            manifest, _ = sync._load_verified_backup_manifest(
                receipt, fixture["backup_root"], "codex", fixture["plan_sha256"]
            )
            final_absent = Path(
                next(
                    entry["path"]
                    for entry in manifest["entries"]
                    if entry["pre_state"]["kind"] == "absent"
                )
            )
            created_root = Path(
                fixture["plan"]["targets"]["codex"]["skills_root"]
            ) / "openspec-superpower-change"
            retained = created_root / "retained-state.txt"
            original_remove = sync._atomic_remove_if_matches
            injected = False

            def retain_state_after_last_leaf(path, expected_state, label):
                nonlocal injected
                result = original_remove(path, expected_state, label)
                if not injected and Path(path) == final_absent:
                    retained.write_bytes(b"retained\n")
                    injected = True
                return result

            with mock.patch.object(
                sync, "_atomic_remove_if_matches", side_effect=retain_state_after_last_leaf
            ):
                with self.assertRaisesRegex(ValueError, "recovery is blocked"):
                    sync.restore_target(
                        fixture["plan"],
                        "codex",
                        fixture["backup_root"],
                        receipt_path,
                        plan_sha256=fixture["plan_sha256"],
                    )
            self.assertTrue(injected)
            self.assertEqual(retained.read_bytes(), b"retained\n")
            self.assertEqual(list(created_root.parent.glob(".cross-cli-parent-remove.*")), [])

    def test_post_history_failure_with_successful_rollback_clears_blocker(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            sync.apply_target(
                fixture["plan"],
                "codex",
                fixture["backup_root"],
                receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            original_bytes = receipt_path.read_bytes()
            original_rename = sync._renameatx
            original_fsync = sync.os.fsync
            history_fd = None
            failed_history_fsync = False

            def record_history(source, destination, flags, **kwargs):
                nonlocal history_fd
                if flags == sync.RENAME_EXCL and "-revision-" in Path(destination).name:
                    history_fd = kwargs["destination_dir_fd"]
                return original_rename(source, destination, flags, **kwargs)

            def fail_first_history_fsync(descriptor):
                nonlocal failed_history_fsync
                if descriptor == history_fd and not failed_history_fsync:
                    failed_history_fsync = True
                    raise OSError("injected history durability failure")
                return original_fsync(descriptor)

            with mock.patch.object(
                sync, "_renameatx", side_effect=record_history
            ), mock.patch.object(sync.os, "fsync", side_effect=fail_first_history_fsync):
                with self.assertRaisesRegex(OSError, "history durability"):
                    sync._advance_receipt(receipt_path, "verified")
            self.assertTrue(failed_history_fsync)
            self.assertEqual(receipt_path.read_bytes(), original_bytes)
            self.assertFalse(
                (fixture["transaction_root"] / "codex.manual-disposition.json").exists()
            )

    def test_post_history_rollback_ambiguity_blocks_later_targets(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            sync.apply_target(
                fixture["plan"],
                "codex",
                fixture["backup_root"],
                receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            original_rename = sync._renameatx
            original_fsync = sync.os.fsync
            history_fd = None
            failed_history_fsync = False

            def record_history_and_block_rollback(
                source, destination, flags, **kwargs
            ):
                nonlocal history_fd
                destination_name = Path(destination).name
                if flags == sync.RENAME_EXCL and "-revision-" in destination_name:
                    history_fd = kwargs["destination_dir_fd"]
                elif (
                    flags == sync.RENAME_SWAP
                    and Path(source).name == receipt_path.name
                    and "-revision-" in destination_name
                ):
                    raise OSError("injected history rollback failure")
                return original_rename(source, destination, flags, **kwargs)

            def fail_first_history_fsync(descriptor):
                nonlocal failed_history_fsync
                if descriptor == history_fd and not failed_history_fsync:
                    failed_history_fsync = True
                    raise OSError("injected history durability failure")
                return original_fsync(descriptor)

            with mock.patch.object(
                sync, "_renameatx", side_effect=record_history_and_block_rollback
            ), mock.patch.object(sync.os, "fsync", side_effect=fail_first_history_fsync):
                with self.assertRaisesRegex(ValueError, "history.*rollback.*blocked"):
                    sync._advance_receipt(receipt_path, "verified")
            self.assertTrue(failed_history_fsync)
            live, _ = sync._read_receipt(receipt_path)
            self.assertEqual(live["state"], "verified")
            with self.assertRaisesRegex(ValueError, "manual|blocked"):
                sync._require_prior_targets_verified(
                    fixture["transaction_root"], "pi", fixture["plan_sha256"]
                )
            disposition = fixture["transaction_root"] / "codex.manual-disposition.json"
            self.assertTrue(disposition.is_file())
            self.assertEqual(stat.S_IMODE(disposition.stat().st_mode), 0o600)

    def test_pi_failures_restore_only_pi_and_never_start_later_targets(self):
        for phase in ("internal-apply", "external-verify", "external-discovery"):
            with self.subTest(phase=phase), tempfile.TemporaryDirectory() as tmp:
                fixture = create_v6_sync_fixture(Path(tmp))
                self._advance_target(fixture, "codex")
                codex_destination = Path(
                    fixture["plan"]["targets"]["codex"]["files"][0]["destination"]
                )
                codex_candidate = codex_destination.read_bytes()
                pi_receipt = fixture["transaction_root"] / "pi.json"
                if phase == "internal-apply":
                    def fail_after_first(point):
                        if point == "after-first-destination-write":
                            raise RuntimeError("injected Pi apply failure")
                    with self.assertRaisesRegex(RuntimeError, "injected Pi"):
                        sync.apply_target(
                            fixture["plan"], "pi", fixture["backup_root"],
                            pi_receipt, plan_sha256=fixture["plan_sha256"],
                            crash_hook=fail_after_first,
                        )
                    restored, _ = sync._read_receipt(pi_receipt)
                    self.assertEqual(restored["state"], "restored")
                else:
                    sync.apply_target(
                        fixture["plan"], "pi", fixture["backup_root"], pi_receipt,
                        plan_sha256=fixture["plan_sha256"],
                    )
                    if phase == "external-discovery":
                        sync.verify_target_with_receipt(
                            fixture["plan"], "pi", pi_receipt,
                            plan_sha256=fixture["plan_sha256"],
                        )
                    restored = sync.restore_target(
                        fixture["plan"], "pi", fixture["backup_root"], pi_receipt,
                        plan_sha256=fixture["plan_sha256"],
                    )
                    self.assertEqual(restored["restore"], "pass")
                sync._assert_target_prestate(fixture["plan"], "pi")
                self.assertEqual(codex_destination.read_bytes(), codex_candidate)
                self.assertFalse(
                    (fixture["transaction_root"] / "antigravity-cli.json").exists()
                )
                self.assertFalse(
                    (fixture["transaction_root"] / "grok-cli.json").exists()
                )

    def test_restore_verification_failure_retains_recovery_blocked_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = create_v6_sync_fixture(Path(tmp))
            receipt_path = fixture["transaction_root"] / "codex.json"
            sync.apply_target(
                fixture["plan"], "codex", fixture["backup_root"], receipt_path,
                plan_sha256=fixture["plan_sha256"],
            )
            original_replace = sync.atomic_replace

            def corrupt_restore(path, content, *, mode=None):
                return original_replace(path, b"restore-verification-failure\n", mode=mode)

            with mock.patch.object(sync, "atomic_replace", side_effect=corrupt_restore):
                with self.assertRaisesRegex(ValueError, "recovery is blocked"):
                    sync.restore_target(
                        fixture["plan"], "codex", fixture["backup_root"], receipt_path,
                        plan_sha256=fixture["plan_sha256"],
                    )
            blocked, _ = sync._read_receipt(receipt_path)
            self.assertEqual(blocked["state"], "recovery-blocked")
            self.assertTrue((fixture["backup_root"] / "codex" / "manifest.json").is_file())

    def test_receipt_install_and_swap_have_no_nonatomic_fallback(self):
        initial_source = inspect.getsource(sync._install_initial_receipt)
        advance_source = inspect.getsource(sync._advance_receipt)
        self.assertIn("RENAME_EXCL", initial_source)
        self.assertIn("RENAME_SWAP", advance_source)
        self.assertNotIn("os.replace", initial_source)
        self.assertNotIn("os.replace", advance_source)
        apply_source = inspect.getsource(sync.apply_target)
        self.assertLess(
            apply_source.index("_prepare_target_backup"),
            apply_source.index("_install_initial_receipt"),
        )
        self.assertLess(
            apply_source.index('"mutation-intent"'),
            apply_source.index("_install_candidate_entry"),
        )


class SourceDeltaTests(unittest.TestCase):
    @staticmethod
    def _write_private_json(path: Path, value: dict) -> None:
        path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")
        path.chmod(0o600)

    def test_complete_inventory_includes_hidden_review_and_symlink_but_not_git(self):
        inventory = getattr(sync, "inventory_source_tree", None)
        self.assertTrue(callable(inventory), "complete source inventory is required")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".git").mkdir()
            (root / ".git" / "ignored").write_text("git bytes\n", encoding="utf-8")
            (root / ".gitignore").write_text("*.pyc\n", encoding="utf-8")
            review = root / "docs" / "design" / "reviews" / "existing.md"
            review.parent.mkdir(parents=True)
            review.write_text("review bytes\n", encoding="utf-8")
            (root / "target.txt").write_text("target\n", encoding="utf-8")
            (root / "link.txt").symlink_to("target.txt")
            records = inventory(root)["records"]
            paths = {record["path"] for record in records}
            self.assertIn(".gitignore", paths)
            self.assertIn("docs/design/reviews/existing.md", paths)
            self.assertIn("link.txt", paths)
            self.assertFalse(any(path == ".git" or path.startswith(".git/") for path in paths))
            link_record = next(record for record in records if record["path"] == "link.txt")
            self.assertEqual(link_record["kind"], "symlink")
            self.assertEqual(
                link_record["sha256"],
                sync.hashlib.sha256(b"target.txt").hexdigest(),
            )

    def test_source_inventory_diff_rejects_hidden_and_existing_review_changes(self):
        inventory = getattr(sync, "inventory_source_tree", None)
        compare = getattr(sync, "compare_source_inventory", None)
        self.assertTrue(callable(inventory), "complete source inventory is required")
        self.assertTrue(callable(compare), "source inventory comparison is required")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".gitignore").write_text("before\n", encoding="utf-8")
            review = root / "docs" / "design" / "reviews" / "existing.md"
            review.parent.mkdir(parents=True)
            review.write_text("before\n", encoding="utf-8")
            allowed = root / "allowed.md"
            allowed.write_text("before\n", encoding="utf-8")
            baseline = inventory(root)
            (root / ".gitignore").write_text("after\n", encoding="utf-8")
            review.write_text("after\n", encoding="utf-8")
            allowed.write_text("after\n", encoding="utf-8")
            changes, unexpected = compare(
                baseline,
                inventory(root),
                "router",
                {"router\tallowed.md"},
            )
            self.assertEqual(
                {change["path"] for change in changes},
                {".gitignore", "docs/design/reviews/existing.md", "allowed.md"},
            )
            self.assertEqual(
                unexpected,
                ["router\t.gitignore", "router\tdocs/design/reviews/existing.md"],
            )

    def test_safe_source_archive_rejects_traversal_and_occupied_compare_root(self):
        safe_extract = getattr(sync, "safe_extract_source_archive", None)
        prepare_root = getattr(sync, "prepare_source_compare_root", None)
        self.assertTrue(callable(safe_extract), "safe source archive extraction is required")
        self.assertTrue(callable(prepare_root), "exclusive compare-root creation is required")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "malicious.tar"
            with tarfile.open(archive, "w") as stream:
                payload = b"escape\n"
                member = tarfile.TarInfo("../escape.txt")
                member.size = len(payload)
                stream.addfile(member, io.BytesIO(payload))
            destination = root / "compare"
            with self.assertRaises(ValueError):
                safe_extract(archive, destination, sync._sha256(archive), 1)
            self.assertFalse(destination.exists())
            destination.mkdir()
            with self.assertRaises(ValueError):
                prepare_root(destination)

    def test_bound_source_delta_reports_before_after_hashes_and_exact_allowlist(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            router = root / "router"
            companion = root / "companion"
            router.mkdir()
            companion.mkdir()
            router_file = router / "allowed.md"
            companion_file = companion / "SKILL.md"
            router_file.write_text("before\n", encoding="utf-8")
            companion_file.write_text("companion\n", encoding="utf-8")
            nested = router / "nested"
            nested.mkdir()
            router_baseline_value = sync.inventory_source_tree(router)
            companion_baseline_value = sync.inventory_source_tree(companion)
            router_baseline = root / "router-start.json"
            companion_baseline = root / "companion-start.json"
            router_preflight = root / "router-preflight.json"
            companion_preflight = root / "companion-preflight.json"
            for path, value in (
                (router_baseline, router_baseline_value),
                (companion_baseline, companion_baseline_value),
                (
                    router_preflight,
                    {
                        **router_baseline_value,
                        "excluded_paths": ["planning-input.md"],
                    },
                ),
                (
                    companion_preflight,
                    {**companion_baseline_value, "excluded_paths": []},
                ),
            ):
                self._write_private_json(path, value)

            router_backup = root / "router.tar"
            companion_backup = root / "companion.tar"
            for archive_path, source, member_name in (
                (router_backup, router_file, "allowed.md"),
                (companion_backup, companion_file, "SKILL.md"),
            ):
                with tarfile.open(archive_path, "w") as archive:
                    archive.add(source, arcname=member_name, recursive=False)
                archive_path.chmod(0o600)
            plan = root / "plan.md"
            plan.write_text("approved plan\n", encoding="utf-8")
            allowlist = root / "allowlist.txt"
            allowlist.write_text(
                "router\tallowed.md\nrouter\tnested/new.md\nrouter\tnew.md\n",
                encoding="utf-8",
            )
            allowlist.chmod(0o600)
            bindings = {
                "schema_version": 1,
                "change_id": "source-delta-test",
                "plan": {"path": str(plan), "sha256": sync._sha256(plan)},
                "backups": {
                    "router": {
                        "path": str(router_backup),
                        "sha256": sync._sha256(router_backup),
                        "mode": "0600",
                        "entries": 1,
                    },
                    "companion": {
                        "path": str(companion_backup),
                        "sha256": sync._sha256(companion_backup),
                        "mode": "0600",
                        "entries": 1,
                    },
                },
                "preflight_tree_baselines": {
                    "router": {
                        "path": str(router_preflight),
                        "sha256": sync._sha256(router_preflight),
                        "mode": "0600",
                        "records": len(router_baseline_value["records"]),
                        "excluded_paths": ["planning-input.md"],
                    },
                    "companion": {
                        "path": str(companion_preflight),
                        "sha256": sync._sha256(companion_preflight),
                        "mode": "0600",
                        "records": len(companion_baseline_value["records"]),
                        "excluded_paths": [],
                    },
                },
                "source_delta_allowlist": {
                    "path": str(allowlist),
                    "sha256": sync._sha256(allowlist),
                    "mode": "0600",
                    "entries": 3,
                },
            }
            bindings_path = root / "bindings.json"
            self._write_private_json(bindings_path, bindings)
            before_hash = sync._sha256(router_file)
            router_file.write_text("after\n", encoding="utf-8")
            (router / "new.md").write_text("new\n", encoding="utf-8")
            (nested / "new.md").write_text("nested\n", encoding="utf-8")
            output = root / "delta.json"
            result = sync.generate_source_delta(
                SimpleNamespace(
                    bindings=bindings_path,
                    router_root=router,
                    companion_root=companion,
                    router_baseline=router_baseline,
                    companion_baseline=companion_baseline,
                    compare_root=root / "compare",
                    output=output,
                )
            )
            self.assertEqual(result["source_delta"], "pass")
            self.assertEqual(result["unexpected_paths"], [])
            self.assertEqual(
                result["changed_paths"],
                [
                    "router\tallowed.md",
                    "router\tnested/new.md",
                    "router\tnew.md",
                ],
            )
            modified = next(
                item for item in result["source_changes"]
                if item["path"] == "allowed.md"
            )
            self.assertEqual(modified["before_sha256"], before_hash)
            self.assertEqual(modified["after_sha256"], sync._sha256(router_file))
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE((root / "compare").stat().st_mode), 0o700)


if __name__ == "__main__":
    unittest.main()
