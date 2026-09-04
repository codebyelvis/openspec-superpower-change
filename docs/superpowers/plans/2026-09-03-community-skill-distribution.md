# Community Skill Distribution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the existing root skill discoverable and locally release-ready for Agent Skills clients, skills.sh, SkillsMP, Pi/npm, and Codex without creating a second authoring source or publishing externally.

**Architecture:** Keep the repository root as the canonical Agent Skill. Add root Pi/npm metadata and public distribution guidance, and generate a skill-only Codex plugin under `distribution/codex-plugin/` from the existing portable manifest. A stdlib-only builder and validator enforce package boundaries and generated-file parity.

**Tech Stack:** JSON package/plugin manifests, Python 3 standard library, `unittest`, npm dry-run, existing OpenSpec/core-gate validators.

---

## File map

- Create `package.json`: Pi/npm metadata and explicit publishable-file allowlist.
- Create `docs/distribution.md`: installation, discovery, security, dependency,
  and maintainer handoff instructions for all in-scope communities.
- Modify `README.md` and `README_cn.md`: link the distribution guide and show
  the short discovery commands.
- Create `scripts/build_codex_plugin.py`: deterministic projection of the
  canonical portable manifest into the Codex plugin adapter.
- Create `scripts/validate_distribution.py`: package metadata, package-boundary,
  plugin-manifest, symlink, and source-parity checks.
- Create `tests/test_distribution.py`: focused tests for metadata, the builder,
  the validator, and the npm dry-run file list.
- Generate `distribution/codex-plugin/.codex-plugin/plugin.json`, its
  `README.md`, and the manifest-listed skill files.
- Modify `openspec/changes/add-community-skill-distribution/tasks.md` only to
  reconcile completed implementation and verification steps.

The following existing files are intentionally not modified: `SKILL.md`,
`references/cross-cli-portable-manifest.json`, managed runtime rules, and the
portable source files. This is a distribution-only change and therefore does
not trigger cross-CLI runtime synchronization.

### Task 1: Add release metadata and public distribution guidance

**Files:**

- Create: `package.json`
- Create: `docs/distribution.md`
- Modify: `README.md`
- Modify: `README_cn.md`

- [ ] **Step 1: Add the exact root package manifest**

Create `package.json` with this shape, preserving the repository name and
using the initial distribution version `0.1.0`:

```json
{
  "name": "openspec-superpower-change",
  "version": "0.1.0",
  "description": "A governed change gate for AI-assisted engineering work.",
  "keywords": [
    "pi-package",
    "agent-skill",
    "agent-skills",
    "codex",
    "pi",
    "openspec",
    "superpowers"
  ],
  "license": "MIT",
  "homepage": "https://github.com/codebyelvis/openspec-superpower-change#readme",
  "repository": {
    "type": "git",
    "url": "git+https://github.com/codebyelvis/openspec-superpower-change.git"
  },
  "bugs": {
    "url": "https://github.com/codebyelvis/openspec-superpower-change/issues"
  },
  "engines": {
    "node": ">=20"
  },
  "pi": {
    "skills": ["./SKILL.md"]
  },
  "files": [
    "SKILL.md",
    "references/",
    "scripts/validate_core_gates.py",
    "scripts/validate_cross_cli_sync.py",
    "templates/",
    "docs/distribution.md",
    "README.md",
    "README_cn.md",
    "CHANGELOG.md",
    "LICENSE"
  ]
}
```

- [ ] **Step 2: Write the distribution guide**

Create `docs/distribution.md` with these exact operational facts:

```markdown
# Distribution and installation

The canonical source is the repository root and its `SKILL.md`. The generated
Codex adapter under `distribution/codex-plugin/` is release output, not a
second authoring source.

## Agent Skills and GitHub

Clone or point an Agent Skills-compatible client at:

`https://github.com/codebyelvis/openspec-superpower-change`

The skill entry point is `SKILL.md`. Review referenced files and scripts before
installing; a host client may grant a skill broad local-system access.

## skills.sh

```bash
npx skills add codebyelvis/openspec-superpower-change
```

skills.sh is a discovery/install path over the public repository. Its listing
is not a security certification. Inspect the source, references, and any
scripts before enabling the skill.

## SkillsMP

Search for `openspec-superpower-change` or the public GitHub repository in
SkillsMP. SkillsMP indexes public `SKILL.md` sources; it is not the canonical
source and does not replace source review. Follow the repository instructions
shown by the index rather than assuming a separate upload or API exists.

## Pi/npm

After a maintainer publishes the package to npm:

```bash
pi install npm:openspec-superpower-change
```

The root `package.json` uses the `pi-package` keyword and maps `pi.skills` to
`./SKILL.md`. Before publication, verify locally with `npm pack --dry-run`.

## Codex plugin

The skill-only plugin artifact is generated at
`distribution/codex-plugin/`. It contains `.codex-plugin/plugin.json` and the
portable files declared for this skill. A maintainer may submit that reviewed
artifact through the official Codex plugin submission flow or install it from
the local directory according to the host client instructions.

The router can reference the companion
`codex-brief-antigravity-review` skill and optional Superpowers skills. Those
dependencies are not silently bundled by this adapter; install them separately
when the host workflow requires them.

## Maintainer release handoff

Run the repository validators, the full test suite, `npm pack --dry-run --json`,
and the local skill discovery check before publishing. This repository change
does not execute `npm publish`, Codex portal submission, or a community upload.
Git staging, commit, and push remain separate maintainer actions.

ClawHub is intentionally out of scope for this MIT-licensed repository because
its current publication contract requires MIT-0.
```

- [ ] **Step 3: Link the guide from both READMEs**

Add a concise “Distribution” section to each README that links to
`docs/distribution.md` and names the five supported paths: Agent Skills/GitHub,
skills.sh, SkillsMP, Pi/npm, and Codex plugin. Keep the existing workflow
description unchanged.

- [ ] **Step 4: Check the configuration-only change**

Run:

```bash
python3 -m json.tool package.json >/dev/null
git diff --check
```

Expected: both commands exit `0` and no whitespace errors are printed.

### Task 2: Write failing distribution tests (TDD RED)

**Files:**

- Create: `tests/test_distribution.py`

- [ ] **Step 1: Add tests for the desired public API**

The test module must expose the real functions used by the builder and
validator and cover the package manifest, package boundary, generated plugin
parity, symlink rejection, and stale-output rejection. Use a temporary copy
of the repository for tests that mutate files. The central assertions are:

```python
def test_package_metadata_points_pi_at_canonical_skill(self):
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    self.assertIn("pi-package", package["keywords"])
    self.assertEqual(package["pi"], {"skills": ["./SKILL.md"]})
    self.assertEqual(package["license"], "MIT")

def test_builder_projects_manifest_files_byte_for_byte(self):
    with tempfile.TemporaryDirectory() as raw:
        copy_root = copy_tree(ROOT, Path(raw) / "repo")
        output = copy_root / "distribution" / "codex-plugin"
        build_codex_plugin.build(copy_root, output)
        self.assertEqual(
            distribution.validate_plugin(copy_root, output), []
        )

def test_validator_rejects_symlink_in_generated_plugin(self):
    with tempfile.TemporaryDirectory() as raw:
        copy_root = copy_tree(ROOT, Path(raw) / "repo")
        output = copy_root / "distribution" / "codex-plugin"
        build_codex_plugin.build(copy_root, output)
        link = output / "skills" / "openspec-superpower-change" / "SKILL-link.md"
        link.symlink_to(output / "skills" / "openspec-superpower-change" / "SKILL.md")
        self.assertTrue(any("symlink" in error for error in distribution.validate_plugin(copy_root, output)))

def test_npm_dry_run_contains_only_public_files(self):
    result = subprocess.run(
        ["npm", "pack", "--dry-run", "--json"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    files = {item["path"] for item in json.loads(result.stdout)[0]["files"]}
    self.assertNotIn("AGENTS.md", files)
    self.assertFalse(any(path.startswith("openspec/") for path in files))
    self.assertFalse(any(path.startswith("tests/") for path in files))
    self.assertNotIn("distribution/codex-plugin/SKILL.md", files)
```

Implement the test helpers `copy_tree`, `setUp`, and `tearDown` so the suite
does not modify the working tree and removes any temporary npm metadata if the
host npm version creates it.

- [ ] **Step 2: Run the focused tests and verify RED**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_distribution -v
```

Expected: FAIL because `scripts.build_codex_plugin` and
`scripts.validate_distribution` do not yet exist. A test import error is not an
acceptable RED result; fix the test import/setup until the failure identifies
the missing implementation.

### Task 3: Implement the builder and validator (TDD GREEN)

**Files:**

- Create: `scripts/build_codex_plugin.py`
- Create: `scripts/validate_distribution.py`

- [ ] **Step 1: Implement manifest projection**

Implement these concrete functions in `scripts/build_codex_plugin.py`:

```python
def load_root_manifest(root: Path) -> tuple[dict, dict]: ...
def expected_skill_files(root: Path) -> list[str]: ...
def build(root: Path, output: Path) -> list[Path]: ...
def main(argv: list[str] | None = None) -> int: ...
```

`load_root_manifest` must parse `package.json` and
`references/cross-cli-portable-manifest.json`, call the existing
`validate_cross_cli_sync.validate_manifest`, and select only the
`openspec-superpower-change` skill entry. `expected_skill_files` must return
the manifest paths in declared order and reject missing or non-regular source
files. `build` must stage files under
`skills/openspec-superpower-change/<manifest path>`, write the official
skill-only manifest shape with `skills: "./skills/"`, a non-empty `author`
object, and the required `interface` metadata (`displayName`,
`shortDescription`, `longDescription`, `developerName`, `category`,
`capabilities`, and `defaultPrompt` as a one-to-three-item string array with
each item at most 128 characters), then write a provenance README without
copying workflow prose.

The builder must refuse an output symlink and must only replace an existing
output directory when its `.codex-plugin/plugin.json` exists and its resolved
parent is the requested output parent. This prevents an accidental overwrite
of an unrelated directory while allowing deterministic regeneration.

- [ ] **Step 2: Implement boundary and parity validation**

Implement these concrete functions in `scripts/validate_distribution.py`:

```python
def validate_package(root: Path) -> list[str]: ...
def validate_plugin(root: Path, output: Path) -> list[str]: ...
def validate(root: Path, output: Path) -> list[str]: ...
def main(argv: list[str] | None = None) -> int: ...
```

`validate_package` must require the package name/version, MIT license,
`pi-package`, `pi.skills == ["./SKILL.md"]`, repository URL, and an explicit
allowlist with no `.`/`*`/parent traversal entries. `validate_plugin` must
reject symlinks, absolute/traversal paths, missing or unexpected files, invalid
plugin JSON, and bytes that differ from each manifest-listed source file.
`validate` combines both checks and returns stable human-readable errors. The
CLI prints `PASS` only when the error list is empty and exits nonzero otherwise.

- [ ] **Step 3: Run the focused tests and verify GREEN**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_distribution -v
```

Expected: all focused tests pass, including the negative symlink and package
boundary cases.

### Task 4: Generate and validate the Codex adapter

**Files:**

- Create: `distribution/codex-plugin/.codex-plugin/plugin.json`
- Create: `distribution/codex-plugin/README.md`
- Create: `distribution/codex-plugin/skills/openspec-superpower-change/` files
  generated by `scripts/build_codex_plugin.py`
- Modify: `openspec/changes/add-community-skill-distribution/tasks.md`

- [ ] **Step 1: Run the builder against the repository**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_codex_plugin.py .
```

Expected: the output lists the generated plugin manifest, provenance README,
and exactly the current `openspec-superpower-change` portable files.

- [ ] **Step 2: Validate the generated adapter**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_distribution.py .
```

Expected: `PASS` and exit code `0`. The generated plugin must contain no
symlinks and no second skill directory.

- [ ] **Step 3: Re-run the builder to prove deterministic regeneration**

Run the builder command a second time and compare the sorted file hashes from
the two runs. Expected: identical hashes for every generated file.

- [ ] **Step 4: Reconcile the OpenSpec task ledger**

Mark only the completed implementation and local verification items in
`openspec/changes/add-community-skill-distribution/tasks.md`. Leave external
publication handoff unchecked because no publication is executed in this
change.

### Task 5: Full verification and review

**Files:**

- Test: `tests/test_distribution.py`
- Validate: all package, plugin, OpenSpec, core-gate, and existing test files

- [ ] **Step 1: Run release dry-run checks**

Run:

```bash
npm pack --dry-run --json
npx --yes skills@latest add . --list
```

Expected: npm prints a JSON file list with no tests, OpenSpec change history,
local instructions, or generated Codex adapter; skills CLI discovers only the
canonical root skill. A Node engine warning from the installed skills CLI is
recorded if present but does not turn a successful discovery into a failure.

- [ ] **Step 2: Run all required repository validators**

Choose a Python interpreter with PyYAML for the first command, then run:

```bash
"${PYTHON_BIN:-python3}" "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" .
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Expected: `Skill is valid!`, core-gate `PASS`, and the complete unittest suite
with zero failures.

- [ ] **Step 3: Perform the independent review pass**

Review the diff against `openspec/changes/add-community-skill-distribution/` and
check each requirement: one canonical source, Pi metadata, explicit npm
boundary, skills.sh/SkillsMP guidance, Codex plugin parity, no external
publication, and ClawHub license boundary. If a finding is material, fix it,
rerun the focused test, rerun the relevant validator, and review the changed
surface again.

- [ ] **Step 4: Finalize without Git or external publication**

Run `git status --short`, `git diff --check`, and the final validators again.
Report the exact files and verification evidence. Do not run `git add`,
`git commit`, `git push`, `npm publish`, or a community/plugin upload.

## Self-review checklist

- Spec coverage: Tasks 1 and 2 cover canonical source, Pi/npm metadata, package
  boundaries, standard indexes, Codex parity, and publication/license limits;
  Tasks 3–5 implement and verify every requirement.
- Placeholder scan: no step depends on “TBD”, an unbounded “add validation”, or
  an unspecified file. All implementation APIs and commands are named.
- Type consistency: builder APIs use `Path` and return `list[Path]`; validator
  APIs use `Path` and return `list[str]`; tests import those exact names.
