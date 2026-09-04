from __future__ import annotations

import importlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "scripts" / "build_codex_plugin.py"
VALIDATOR_PATH = ROOT / "scripts" / "validate_distribution.py"


def copy_tree(source: Path, destination: Path) -> Path:
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
    )
    return destination


class DistributionTests(unittest.TestCase):
    def _load_modules(self):
        self.assertTrue(BUILDER_PATH.is_file(), "builder implementation is missing")
        self.assertTrue(VALIDATOR_PATH.is_file(), "validator implementation is missing")
        importlib.invalidate_caches()
        return (
            importlib.import_module("scripts.build_codex_plugin"),
            importlib.import_module("scripts.validate_distribution"),
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
        self.assertNotIn("scripts/build_codex_plugin.py", files)

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
        self.assertNotIn("scripts/build_codex_plugin.py", files)


if __name__ == "__main__":
    unittest.main()
