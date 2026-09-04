# SkillsMP Index Adapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:executing-plans to implement this plan task-by-task. OpenSpec
> tasks are the canonical progress ledger; the checkboxes below are static
> execution instructions.

**Goal:** Add a generated nested GitHub catalog adapter that makes the
repository structurally discoverable by SkillsMP without changing the
canonical skill or npm package.

**Architecture:** The root `SKILL.md` remains authoritative. A focused builder
projects its bytes to `skills/openspec-superpower-change/SKILL.md` in one
builder-owned output namespace, leaving Codex plugin generation independent.
The validator enforces exact path/type/content closure and npm exclusion.
Public docs separate source readiness from asynchronous third-party indexing.

**Tech Stack:** Python 3 standard library, `unittest`, OpenSpec CLI, npm dry-run,
and `npx skills` local discovery.

---

## File map

- Modify `tests/test_distribution.py`: RED regressions for generation, drift,
  unsafe entries, npm exclusion, and one logical discovery result.
- Create `scripts/build_skillsmp_adapter.py`: safely generate only the nested
  catalog adapter with staged replacement and explicit recovery semantics.
- Modify `scripts/validate_distribution.py`: validate exact adapter closure and
  canonical byte parity.
- Create `skills/openspec-superpower-change/SKILL.md`: generated regular-file
  mirror of root `SKILL.md`.
- Modify `docs/distribution.md`, `README.md`, `README_cn.md`, and `CHANGELOG.md`:
  explain the compatibility adapter and external index latency.
- Modify the active OpenSpec task ledger and add review/evidence artifacts only
  as required by the project completion contract.

The portable manifest, root `SKILL.md`, workflow references, runtime installs,
package version, and `package.json.files` remain unchanged. No cross-CLI runtime
sync is triggered.

### Task 1: Prove the missing behavior (RED)

**Files:** Modify `tests/test_distribution.py`.

- [ ] Add tests requiring the builder to create the exact nested regular file
  with root bytes.
- [ ] Add validator tests for missing, stale, symlinked, FIFO/special, and
  unexpected adapter content.
- [ ] Add builder tests for symlinked `skills/` and skill-name parents, external
  target non-mutation, existing-output identity drift, caught install failure
  restoration, and visible recovery residue when restoration cannot be proven.
- [ ] Add corrective RED tests for parent rebinding immediately before a
  mutation, hard-linked source/adapter targets, canonical-source replacement
  and in-place writes, unknown stage/recovery residue introduced during install,
  and missing descriptor/no-follow platform capabilities.
- [ ] Add implementation-review RED tests proving every final source,
  output, residue, and live-binding check precedes recovery deletion; platform
  support for descriptor listing and no-follow stat is rejected before any
  mutation; rebound recovery diagnostics do not claim an untrusted lexical
  path; and cleanup failures preserve the primary exception.
- [ ] Strengthen npm dry-run assertions so every `skills/` path is forbidden.
- [ ] Add an isolated `npx skills add . --list` probe asserting one logical
  skill.
- [ ] Run only the focused tests and confirm failures are caused by the absent
  adapter behavior.

### Task 2: Implement deterministic generation and validation (GREEN)

**Files:** Create `scripts/build_skillsmp_adapter.py`, modify
`scripts/validate_distribution.py`, and create the generated adapter.

- [ ] Reserve only `skills/openspec-superpower-change/` as generated output;
  require exact existing closure `{SKILL.md}` and no-follow regular-file checks
  for every parent/entry before replacement.
- [ ] Stage the full adapter as a sibling directory; capture and recheck the
  existing output identity, move it to a unique same-filesystem recovery name,
  install the stage, and restore prior state on caught failure. Unknown recovery
  residue must fail closed and remain visible for manual disposition.
- [ ] Keep deterministic safety seams at module level:
  `_check_replaceable_output(skills_fd, output_name)`,
  `_install_staged_adapter(skills_fd, stage_name, output_name)`,
  `_restore_recovery(skills_fd, recovery_name, output_name)`, and
  `_verify_restored_snapshot(skills_fd, output_name, snapshot)`. The canonical
  source is captured/rechecked by `_read_source_snapshot(root_fd, "SKILL.md")`.
  All mutation seams receive retained directory descriptors and single entry
  names, never mutation-authorizing absolute paths. Tests may patch only these
  declared seams; the underlying descriptor-relative primitive remains an
  implementation choice.
- [ ] Bind repository and `skills/` directories with `O_DIRECTORY |
  O_NOFOLLOW`, and perform stage/recovery creation, install, restore, unlink,
  and cleanup using supported `dir_fd` operations against the retained
  descriptor. Fail before mutation if any actually used `dir_fd`, descriptor
  listing, or no-follow stat primitive is unavailable.
- [ ] Require source and adapter targets to be single-link regular files.
  Revalidate source identity/metadata/bytes and unknown stage/recovery residue
  immediately before recovery cleanup. Treat verified recovery deletion as the
  commit point and perform no later check that can turn the committed build
  into failure. Source replacement,
  in-place writes, or injected residue must compensate or fail with visible
  evidence.
- [ ] When a live pathname binding is untrusted, report recovery by its retained
  parent device/inode and entry name instead of presenting a lexical path as
  authoritative. Preserve the primary failure when cleanup also fails.
- [ ] Keep `scripts/build_codex_plugin.py` and its output mutation-independent.
- [ ] Extend `validate()` to require exact adapter path closure and byte parity.
- [ ] Expose `validate_skillsmp_adapter(root)` as the focused validation API;
  the aggregate `validate()` entry point must call it and preserve its errors.
- [ ] Keep a deterministic validator safety seam
  `_open_adapter_directory(root)` that returns the no-follow bound directory
  descriptors/identity used for all subsequent residue, closure, and target
  traversal. Race tests may replace pathnames only after this seam returns; a
  correct implementation must continue on the bound objects and detect any
  pathname-binding drift before returning PASS.
- [ ] Run the builder and focused tests until GREEN; refactor only after GREEN.

### Task 3: Correct public expectations

**Files:** Modify `docs/distribution.md`, `README.md`, `README_cn.md`, and
`CHANGELOG.md`.

- [ ] Document the nested file as a generated, non-authoritative GitHub catalog
  adapter.
- [ ] State that Pi gallery, skills.sh, and SkillsMP search visibility depends
  on external asynchronous indexing and is not guaranteed immediately.
- [ ] Preserve existing install commands and root Pi/npm entry point.

### Task 4: Review and verify

**Files:** Modify OpenSpec tasks and add governed evidence/review artifacts when
required.

- [ ] Run focused distribution tests, distribution validator, npm dry-run, and
  isolated local skills discovery.
- [ ] Run the required quick validator, core gates, and all unit tests.
- [ ] Obtain independent implementation Review, fix all blocking findings, and
  re-run affected checks.
- [ ] Run Project Learning Closeout, persist final verification, obtain the
  independent final Review, and reconcile/archive only when authorized.

Run the verification sequence from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_distribution -v
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_distribution.py .
npm pack --dry-run --json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_distribution.DistributionTests.test_local_skills_cli_discovers_exactly_one_logical_skill -v
PYTHON_BIN=python
"$PYTHON_BIN" "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" .
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
openspec validate add-skillsmp-index-adapter --strict
git diff --check
```

Git staging, commit, push, npm publication, and external submissions are not
steps in this plan because this execution has no Git-write or publication
authority.
