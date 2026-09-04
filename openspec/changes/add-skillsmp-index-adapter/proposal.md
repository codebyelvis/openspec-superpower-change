# Change: Add a SkillsMP index compatibility adapter

## Why

The published repository and npm package are installable, but SkillsMP does
not currently return `openspec-superpower-change` in search. The strongest
available catalog evidence indicates that SkillsMP discovers nested
`skills/<name>/SKILL.md` entries and ignores a repository-root-only
`SKILL.md`. The previous distribution design assumed the root entry was
sufficient, so waiting or republishing the unchanged npm package cannot repair
this repository-layout mismatch.

## What Changes

- Keep the root `SKILL.md` as the only authoring source and Pi/npm entry point.
- Add `skills/openspec-superpower-change/SKILL.md` as a generated, regular-file
  GitHub index adapter whose bytes must equal the root `SKILL.md`.
- Add a focused index-adapter builder and extend the existing distribution
  validator so a missing, stale, linked, special, or unexpected index adapter
  fails closed without coupling its mutation to Codex plugin generation.
- Keep `skills/` outside the npm `files` allowlist and verify that local
  standards-based discovery still exposes one logical skill.
- Correct public distribution documentation to describe the compatibility
  path and the asynchronous, third-party indexing boundary.

## Impact

- Affected specs: `skill-distribution`
- Affected code: `scripts/build_skillsmp_adapter.py`,
  `scripts/validate_distribution.py`, `tests/test_distribution.py`, generated
  `skills/openspec-superpower-change/SKILL.md`, and public distribution docs
- Risks: duplicate discovery, mirror drift, symlink/path escape, and accidental
  npm inclusion; all are bounded by deterministic generation and negative
  validation tests

## Approval Status

- Change-id presented to user: `add-skillsmp-index-adapter`
- Strict validation result: PASS (`openspec validate
  add-skillsmp-index-adapter --strict`, 2026-09-04)
- [x] Proposal reviewed in substance through the 2026-09-04 investigation and
  recommended generated-mirror repair
- [x] This specific scoped change-id approved for implementation by the user's
  2026-09-04 instruction to start the repair after that recommendation
- Git commit/push and external publication remain separate actions; this
  approval does not authorize them.
