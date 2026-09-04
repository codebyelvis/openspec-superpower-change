#!/usr/bin/env python3
"""Validate public package metadata and generated Codex distribution output."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path, PurePosixPath

try:
    from . import build_codex_plugin as builder
except ImportError:  # pragma: no cover - used when invoked as a file.
    import build_codex_plugin as builder


EXPECTED_PACKAGE_FILES = {
    "SKILL.md",
    "references/",
    "scripts/validate_core_gates.py",
    "scripts/validate_cross_cli_sync.py",
    "templates/",
    "docs/distribution.md",
    "README.md",
    "README_cn.md",
    "CHANGELOG.md",
    "LICENSE",
}
PLUGIN_ALLOWED_KEYS = {
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "skills",
    "interface",
}
INTERFACE_REQUIRED_KEYS = {
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "category",
    "capabilities",
    "defaultPrompt",
}
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def _load_json(path: Path, label: str, errors: list[str]) -> dict | None:
    if path.is_symlink() or not path.is_file():
        errors.append(f"{label} is missing or not a regular file")
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        errors.append(f"{label} must contain valid JSON")
        return None
    if not isinstance(value, dict):
        errors.append(f"{label} must contain a JSON object")
        return None
    return value


def _non_empty_string(payload: dict, key: str, label: str, errors: list[str]) -> str | None:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}.{key} must be a non-empty string")
        return None
    return value


def _safe_package_entry(raw: object) -> bool:
    if not isinstance(raw, str) or not raw or "\\" in raw or "*" in raw:
        return False
    normalized = raw.rstrip("/")
    path = PurePosixPath(normalized)
    return not path.is_absolute() and all(part not in {"", ".", ".."} for part in path.parts)


def _collect_package_entry_files(root: Path, raw: str, errors: list[str]) -> set[str]:
    """Expand one npm files entry without following symlinks."""
    path = root / raw.rstrip("/")
    if path.is_symlink():
        errors.append(f"package.json.files entry must not be a symlink: {raw}")
        return set()
    if path.is_file():
        return {path.relative_to(root).as_posix()}
    if not path.is_dir():
        errors.append(f"package.json.files entry is missing or not regular: {raw}")
        return set()

    collected: set[str] = set()
    for base, directories, files in os.walk(path, followlinks=False):
        base_path = Path(base)
        for name in directories:
            child = base_path / name
            if child.is_symlink():
                errors.append(
                    "package.json.files directory contains symlink: "
                    f"{child.relative_to(root).as_posix()}"
                )
        for name in files:
            child = base_path / name
            relative = child.relative_to(root).as_posix()
            if child.is_symlink():
                errors.append(f"package.json.files directory contains symlink: {relative}")
            elif child.is_file():
                collected.add(relative)
            else:
                errors.append(f"package.json.files contains unsupported entry: {relative}")
    return collected


def validate_package(root: Path) -> list[str]:
    errors: list[str] = []
    root = root.resolve()
    package = _load_json(root / "package.json", "package.json", errors)
    if package is None:
        return errors

    name = _non_empty_string(package, "name", "package.json", errors)
    version = _non_empty_string(package, "version", "package.json", errors)
    _non_empty_string(package, "description", "package.json", errors)
    if name != builder.SKILL_NAME:
        errors.append(f"package.json.name must be {builder.SKILL_NAME!r}")
    if version is not None and SEMVER.fullmatch(version) is None:
        errors.append("package.json.version must use strict x.y.z semver")
    if package.get("license") != "MIT":
        errors.append("package.json.license must be MIT")
    keywords = package.get("keywords")
    if not isinstance(keywords, list) or "pi-package" not in keywords:
        errors.append("package.json.keywords must include pi-package")
    pi = package.get("pi")
    if pi != {"skills": ["./SKILL.md"]}:
        errors.append('package.json.pi must equal {"skills": ["./SKILL.md"]}')
    repository = package.get("repository")
    if not isinstance(repository, dict) or repository.get("url") != (
        "git+https://github.com/codebyelvis/openspec-superpower-change.git"
    ):
        errors.append("package.json.repository.url is not the canonical GitHub URL")

    files = package.get("files")
    if not isinstance(files, list) or any(not _safe_package_entry(item) for item in files):
        errors.append("package.json.files must contain only safe relative entries")
    elif set(files) != EXPECTED_PACKAGE_FILES:
        errors.append(
            "package.json.files must exactly match the documented public allowlist"
        )
    if isinstance(files, list):
        for raw in files:
            if not isinstance(raw, str):
                continue
            if _safe_package_entry(raw):
                _collect_package_entry_files(root, raw, errors)
    return errors


def validate_npm_package(root: Path) -> list[str]:
    """Compare npm's dry-run file list with the explicit public allowlist."""
    errors: list[str] = []
    root = root.resolve()
    package = _load_json(root / "package.json", "package.json", errors)
    if package is None:
        return errors
    files = package.get("files")
    if not isinstance(files, list):
        errors.append("package.json.files must be an array before npm validation")
        return errors

    expected = {"package.json"}
    for raw in files:
        if isinstance(raw, str) and _safe_package_entry(raw):
            expected.update(_collect_package_entry_files(root, raw, errors))

    npm = shutil.which("npm")
    if npm is None:
        errors.append("npm executable is required for the package dry-run")
        return errors
    result = subprocess.run(
        [npm, "pack", "--dry-run", "--json"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        errors.append(f"npm pack --dry-run failed: {result.stderr.strip()}")
        return errors
    try:
        records = json.loads(result.stdout)
        actual = {item["path"] for item in records[0]["files"]}
    except (KeyError, IndexError, TypeError, json.JSONDecodeError):
        errors.append("npm pack --dry-run did not return a valid file list")
        return errors
    if actual != expected:
        missing = sorted(expected - actual)
        unexpected = sorted(actual - expected)
        if missing:
            errors.append(f"npm package is missing public files: {', '.join(missing)}")
        if unexpected:
            errors.append(f"npm package has unexpected files: {', '.join(unexpected)}")
    return errors


def _plugin_files(output: Path, errors: list[str]) -> set[str]:
    actual: set[str] = set()
    if output.is_symlink():
        errors.append("generated plugin root must not be a symlink")
        return actual
    if not output.is_dir():
        errors.append("generated plugin root is missing")
        return actual
    for base, directories, files in os.walk(output, followlinks=False):
        base_path = Path(base)
        for name in [*directories, *files]:
            path = base_path / name
            relative = path.relative_to(output).as_posix()
            if path.is_symlink():
                errors.append(f"generated plugin contains symlink: {relative}")
            elif path.is_file():
                actual.add(relative)
            elif path.is_dir() and name in directories:
                continue
            else:
                errors.append(f"generated plugin contains unsupported entry: {relative}")
    return actual


def validate_plugin(root: Path, output: Path) -> list[str]:
    errors: list[str] = []
    root_lexical = Path(os.path.abspath(os.path.expanduser(os.fspath(root))))
    root = root_lexical.resolve()
    output = Path(os.path.abspath(os.path.expanduser(os.fspath(output))))
    try:
        builder._check_output_location(root_lexical, root, output)
    except ValueError as error:
        errors.append(str(error))
        return errors
    try:
        package, _ = builder.load_root_manifest(root)
        source_paths = builder.expected_skill_files(root)
    except (OSError, ValueError) as error:
        errors.append(f"canonical source is invalid: {error}")
        return errors

    manifest_path = output / ".codex-plugin" / "plugin.json"
    manifest = _load_json(manifest_path, ".codex-plugin/plugin.json", errors)
    actual_files = _plugin_files(output, errors)
    expected_files = {
        ".codex-plugin/plugin.json",
        "README.md",
        *{
            f"skills/{builder.SKILL_NAME}/{relative}"
            for relative in source_paths
        },
    }
    if actual_files != expected_files:
        missing = sorted(expected_files - actual_files)
        unexpected = sorted(actual_files - expected_files)
        if missing:
            errors.append(f"generated plugin is missing files: {', '.join(missing)}")
        if unexpected:
            errors.append(f"generated plugin has unexpected files: {', '.join(unexpected)}")

    if manifest is None:
        return errors
    unknown = sorted(set(manifest) - PLUGIN_ALLOWED_KEYS)
    if unknown:
        errors.append(f"plugin.json has unsupported fields: {', '.join(unknown)}")
    for key in ("name", "version", "description", "homepage", "repository", "license"):
        _non_empty_string(manifest, key, "plugin.json", errors)
    if manifest.get("name") != package.get("name"):
        errors.append("plugin.json.name must match package.json.name")
    if manifest.get("version") != package.get("version"):
        errors.append("plugin.json.version must match package.json.version")
    if manifest.get("license") != "MIT":
        errors.append("plugin.json.license must be MIT")
    if manifest.get("skills") != "./skills/":
        errors.append('plugin.json.skills must equal "./skills/"')

    author = manifest.get("author")
    if not isinstance(author, dict):
        errors.append("plugin.json.author must be an object")
    else:
        _non_empty_string(author, "name", "plugin.json.author", errors)
    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append("plugin.json.interface must be an object")
    else:
        for key in sorted(INTERFACE_REQUIRED_KEYS):
            if key == "capabilities":
                values = interface.get(key)
                if not isinstance(values, list) or not all(
                    isinstance(value, str) and value.strip() for value in values
                ):
                    errors.append("plugin.json.interface.capabilities must be a string array")
            elif key == "defaultPrompt":
                prompts = interface.get(key)
                if (
                    not isinstance(prompts, list)
                    or not 1 <= len(prompts) <= 3
                    or not all(
                        isinstance(prompt, str)
                        and bool(prompt.strip())
                        and len(prompt) <= 128
                        for prompt in prompts
                    )
                ):
                    errors.append(
                        "plugin.json.interface.defaultPrompt must contain 1-3 "
                        "non-empty strings of at most 128 characters"
                    )
            else:
                _non_empty_string(interface, key, "plugin.json.interface", errors)

    skill_root = output / "skills" / builder.SKILL_NAME
    for relative in source_paths:
        source = root.joinpath(*PurePosixPath(relative).parts)
        destination = skill_root / relative
        if destination.is_symlink() or not destination.is_file():
            continue
        try:
            if source.read_bytes() != destination.read_bytes():
                errors.append(f"generated file differs from canonical source: {relative}")
        except OSError:
            errors.append(f"unable to compare generated file: {relative}")
    return errors


def validate(root: Path, output: Path, *, check_npm: bool = True) -> list[str]:
    errors = [*validate_package(root), *validate_plugin(root, output)]
    if check_npm:
        errors.extend(validate_npm_package(root))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--skip-npm",
        action="store_true",
        help="Skip npm pack --dry-run when npm is unavailable",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    output = args.output or (root / "distribution" / "codex-plugin")
    errors = validate(root, output, check_npm=not args.skip_npm)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
