#!/usr/bin/env python3
"""Build the generated skill-only Codex plugin distribution."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
from pathlib import Path, PurePosixPath

try:
    from . import validate_cross_cli_sync as sync
except ImportError:  # pragma: no cover - used when invoked as a file.
    import validate_cross_cli_sync as sync


SKILL_NAME = "openspec-superpower-change"
PORTABLE_MANIFEST_PATH = Path("references/cross-cli-portable-manifest.json")
REPOSITORY_URL = "https://github.com/codebyelvis/openspec-superpower-change"
PROVENANCE_README = """# openspec-superpower-change Codex plugin

This directory is generated distribution output. The canonical skill source is
the repository root `SKILL.md`; the generated files are projected from
`references/cross-cli-portable-manifest.json`.

Do not edit the skill files in this directory directly. From the repository root,
regenerate them with:

```bash
python3 scripts/build_codex_plugin.py .
```
"""


def _load_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"unable to load JSON object: {path}") from error
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return payload


def load_root_manifest(root: Path) -> tuple[dict, dict]:
    """Load package metadata and the one canonical skill manifest entry."""
    root = root.resolve()
    package = _load_json(root / "package.json")
    manifest = _load_json(root / PORTABLE_MANIFEST_PATH)
    try:
        sync.validate_manifest(manifest)
    except (TypeError, ValueError) as error:
        raise ValueError(f"portable manifest is invalid: {error}") from error

    if package.get("name") != SKILL_NAME:
        raise ValueError(f"package name must be {SKILL_NAME!r}")
    if not isinstance(package.get("version"), str) or not package["version"].strip():
        raise ValueError("package version must be a non-empty string")

    skills = [item for item in manifest["skills"] if item.get("name") == SKILL_NAME]
    if len(skills) != 1:
        raise ValueError(f"portable manifest must contain exactly one {SKILL_NAME!r} entry")
    return package, skills[0]


def _relative_path(raw_path: str) -> PurePosixPath:
    if not isinstance(raw_path, str) or not raw_path or "\\" in raw_path:
        raise ValueError(f"manifest path is not safe: {raw_path!r}")
    path = PurePosixPath(raw_path)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"manifest path is not safe: {raw_path!r}")
    return path


def expected_skill_files(root: Path) -> list[str]:
    """Return declared source paths in manifest order after source checks."""
    root = root.resolve()
    _, skill = load_root_manifest(root)
    paths: list[str] = []
    for item in skill["files"]:
        path = _relative_path(item["path"])
        try:
            sync.validate_relative_path(root, path.as_posix())
        except (OSError, ValueError) as error:
            raise ValueError(
                f"manifest source is not a safe regular file: {path.as_posix()}"
            ) from error
        paths.append(path.as_posix())
    return paths


def _plugin_manifest(package: dict) -> dict:
    return {
        "name": package["name"],
        "version": package["version"],
        "description": package["description"],
        "author": {
            "name": "openspec-superpower-change contributors",
            "url": REPOSITORY_URL,
        },
        "homepage": package["homepage"],
        "repository": REPOSITORY_URL,
        "license": package["license"],
        "keywords": package["keywords"],
        "skills": "./skills/",
        "interface": {
            "displayName": "OpenSpec Superpower Change",
            "shortDescription": "Governed change gate for AI-assisted engineering",
            "longDescription": (
                "Routes material AI-assisted engineering changes through local "
                "rules, OpenSpec contracts, disciplined implementation, and evidence."
            ),
            "developerName": "openspec-superpower-change contributors",
            "category": "Developer Tools",
            "capabilities": ["Interactive", "Write"],
            "defaultPrompt": [
                "Use the governed change gate for this engineering task."
            ],
        },
    }


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _check_output_location(root_lexical: Path, root: Path, output: Path) -> None:
    resolved_root = root.resolve()
    resolved_parent = output.parent.resolve(strict=False)
    try:
        resolved_parent.relative_to(resolved_root)
    except ValueError as error:
        raise ValueError(
            f"refusing to write output outside repository root: {output.parent}"
        ) from error

    try:
        relative_parent = output.parent.relative_to(root_lexical)
    except ValueError:
        relative_parent = None
    if relative_parent is not None:
        current = root_lexical
        for part in relative_parent.parts:
            current /= part
            if current.is_symlink():
                raise ValueError(f"refusing symlink in output parent path: {current}")


def _reject_output_tree_symlinks(output: Path) -> None:
    for base, directories, files in os.walk(output, followlinks=False):
        base_path = Path(base)
        for name in [*directories, *files]:
            candidate = base_path / name
            if candidate.is_symlink():
                relative = candidate.relative_to(output).as_posix()
                raise ValueError(f"refusing symlink inside existing output: {relative}")


def _check_replaceable_output(
    root_lexical: Path,
    root: Path,
    output: Path,
) -> tuple[int, int] | None:
    _check_output_location(root_lexical, root, output)
    if output.is_symlink():
        raise ValueError(f"refusing to replace symlink output: {output}")
    if not output.exists():
        return None
    if not output.is_dir():
        raise ValueError(f"refusing to replace non-directory output: {output}")
    _reject_output_tree_symlinks(output)
    manifest = output / ".codex-plugin" / "plugin.json"
    if manifest.is_symlink() or not manifest.is_file():
        raise ValueError(
            "refusing to replace an unmarked directory; expected generated "
            f"plugin manifest: {manifest}"
        )
    metadata = output.stat(follow_symlinks=False)
    return metadata.st_dev, metadata.st_ino


def build(root: Path, output: Path) -> list[Path]:
    """Build the plugin into a staging directory and replace only marked output."""
    root_lexical = Path(os.path.abspath(os.path.expanduser(os.fspath(root))))
    root = root_lexical.resolve()
    output = Path(os.path.abspath(os.path.expanduser(os.fspath(output))))
    package, skill = load_root_manifest(root)
    source_paths = expected_skill_files(root)
    _check_replaceable_output(root_lexical, root, output)
    output.parent.mkdir(parents=True, exist_ok=True)
    existing_output_identity = _check_replaceable_output(root_lexical, root, output)

    stage = Path(tempfile.mkdtemp(prefix=f".{output.name}-", dir=output.parent))
    try:
        plugin_manifest_path = stage / ".codex-plugin" / "plugin.json"
        _write_json(plugin_manifest_path, _plugin_manifest(package))
        readme_path = stage / "README.md"
        readme_path.write_text(PROVENANCE_README, encoding="utf-8")

        generated: list[Path] = [plugin_manifest_path, readme_path]
        generated_skill_root = stage / "skills" / SKILL_NAME
        for relative in source_paths:
            source = sync.validate_relative_path(root, relative)
            destination = generated_skill_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            generated.append(destination)

        current_output_identity = _check_replaceable_output(root_lexical, root, output)
        if current_output_identity != existing_output_identity:
            raise ValueError("existing generated output changed during build")
        if existing_output_identity is not None:
            shutil.rmtree(output)
        stage.replace(output)
        return [output / path.relative_to(stage) for path in generated]
    except Exception:
        if stage.exists():
            shutil.rmtree(stage)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    output = args.output or (root / "distribution" / "codex-plugin")
    try:
        generated = build(root, output)
    except (OSError, ValueError) as error:
        print(f"FAIL: {error}")
        return 1
    for path in generated:
        print(f"generated {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
