# Design: add-skillsmp-index-adapter

## Context

The repository root `SKILL.md` is canonical and is already consumed by Pi/npm
and direct Agent Skills installers. SkillsMP search has not indexed the skill,
while sampled catalog entries and the prior investigation indicate a nested
skill-directory crawler contract. A compatibility path is therefore needed
without creating another editable workflow source.

## Goals / Non-Goals

### Goals

- Expose the conventional `skills/openspec-superpower-change/SKILL.md` path to
  GitHub catalog crawlers.
- Make the adapter deterministic, byte-identical to the canonical root file,
  regular-file-only, and mechanically validated.
- Preserve Pi/npm package contents and one logical local-discovery result.

### Non-Goals

- Changing router semantics, trigger scope, OpenSpec/Superpowers boundaries,
  evidence gates, or completion claims.
- Changing the portable manifest or synchronizing runtime installations.
- Claiming or forcing immediate third-party index refreshes.
- Republishing npm, committing, pushing, or submitting to external services as
  part of source implementation.

## Decisions

- Decision: the root `SKILL.md` remains the only authoring source.
  - Rationale: Pi/npm and existing users already depend on it.
- Decision: the SkillsMP adapter is a generated regular file at
  `skills/openspec-superpower-change/SKILL.md`.
  - Rationale: a regular file is crawler-compatible; a symlink may be ignored
    and would violate the repository's public distribution safety invariant.
- Decision: add a focused index-adapter builder and leave the Codex plugin
  builder's mutation boundary unchanged.
  - Rationale: the two outputs have different ownership roots. Separate
    commands avoid a partial cross-product transaction while sharing constants
    and validation through the existing distribution modules.
- Decision: reserve only
  `skills/openspec-superpower-change/` as builder-owned generated output. It
  may be created when absent or replaced only when it contains exactly one
  regular `SKILL.md`; linked, special, or unexpected entries block replacement.
  - Rationale: exact closure makes ownership explicit and prevents deletion or
    overwrite of unrelated user files.
- Decision: stage the complete adapter as a sibling directory, capture the
  existing generated-directory identity, recheck it immediately before
  replacement, move the old generated directory to a unique same-filesystem
  recovery name, install the staged directory, and restore the old directory
  on any caught install failure. Residual recovery names fail closed and are
  reported for manual disposition rather than silently deleted.
  - Rationale: each command mutates one owned output and either restores its
    prior state or leaves explicit recovery evidence.
- Decision: the builder binds the repository and `skills/` directories with
  no-follow directory descriptors before mutation and performs every stage,
  recovery, rename, unlink, and cleanup operation relative to the retained
  `skills/` descriptor. It fails before mutation when the platform lacks the
  required `dir_fd`, descriptor-listing, no-follow-stat, `O_DIRECTORY`, or
  `O_NOFOLLOW` capabilities actually used by the implementation.
  - Rationale: pathname identity checks cannot close the check-to-rename parent
    rebinding window.
- Decision: canonical source and generated targets are single-link regular
  files. The builder revalidates the retained source identity, metadata, and
  bytes before deleting recovery evidence, and rechecks unknown stage/recovery
  siblings and live bindings at the same boundary. Verified recovery deletion
  is the transaction commit point; no later check may convert the committed
  build into failure.
  - Rationale: hard links, concurrent source replacement/in-place writes, and
    injected transaction residue must not produce a false successful build.
- Decision: diagnostics identify recovery through an authoritative live path
  only while live bindings are proven. Otherwise they report the retained
  parent device/inode plus recovery entry name and mark the lexical path
  untrusted. A cleanup failure augments rather than replaces the primary error.
  - Rationale: operators must not be directed to inspect or delete an unrelated
    object after pathname rebinding, and cleanup must not erase root cause.
- Decision: validate exact bytes, exact path closure, parent types, and npm
  exclusion.
  - Rationale: generated status is credible only when drift and path tricks
    fail closed.
- Alternative considered: manually copy the file. Rejected because it creates
  an unverified competing source.
- Alternative considered: symlink the root file. Rejected because crawler and
  public-path behavior is not portable.
- Alternative considered: republish npm only. Rejected because SkillsMP indexes
  GitHub source layout, not npm package metadata.

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| A scanner reports root and nested entries as duplicates | Verify the supported local `skills` CLI resolves one logical skill; document the nested path as a catalog adapter. |
| The generated mirror becomes stale | Builder rewrites it from root bytes; validator compares byte-for-byte and fails on drift or absence. |
| A symlink or special file redirects the public path | Builder and validator reject linked/non-regular parents and entries without following them. |
| The adapter leaks into npm/Pi | Keep `skills/` absent from `package.json.files` and assert the exact npm dry-run boundary. |
| SkillsMP still does not index immediately | Report third-party crawl latency as residual risk and verify the GitHub-side prerequisite only. |

## Migration / Rollback

Run the focused adapter builder, then run focused and full validation. If an
install failure is caught, the builder restores the captured adapter directory;
if restoration cannot be proven, it leaves and reports the unique recovery
directory and stops. Manual rollback may restore that directory, remove a
newly created adapter, or revert source files to the recorded pre-change backup
or worktree base commit. The canonical root skill, Codex plugin output, and npm
package remain unchanged throughout.
