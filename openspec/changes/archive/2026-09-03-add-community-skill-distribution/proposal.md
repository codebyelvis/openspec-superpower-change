# Change: Add community distribution adapters for the skill

## Why

The repository currently contains a valid Agent Skill, but it has no package
metadata or documented distribution path for the communities and clients that
can discover or install it. This makes the skill harder to find and forces
each client to infer packaging details from the repository layout.

This change adds release-facing metadata and generated adapters while keeping
the repository root as the only canonical source of the skill. The scope is
Pi/npm packaging, standards-based discovery through skills.sh and SkillsMP,
and a skill-only Codex plugin artifact.

## What Changes

### In scope

- Add a root `package.json` that exposes the root `SKILL.md` as a Pi package,
  uses the `pi-package` keyword, and constrains the npm package contents with
  an explicit allowlist.
- Add public installation and discovery documentation for Agent Skills,
  skills.sh, SkillsMP, Pi/npm, and Codex plugins.
- Add a generated skill-only Codex plugin adapter under
  `distribution/codex-plugin/`.
- Add a build script and validators/tests that prove the adapter is derived
  from the portable manifest and that package boundaries do not include
  internal project material.
- Add release dry-run checks (`npm pack --dry-run` and local skill discovery)
  to the verification workflow without publishing externally.

### Out of scope

- Changing the skill router, its trigger rules, OpenSpec boundaries,
  Superpowers boundaries, evidence gates, or completion claims.
- Changing the cross-CLI portable manifest or synchronised runtime files.
- Creating a second source of truth for the skill instructions.
- Executing `npm publish`, uploading to a Codex/plugin portal, or performing a
  manual submission to a community index.
- Publishing to ClawHub, whose publication contract requires MIT-0 and is not
  compatible with the repository's current MIT license boundary.

## Compatibility and release decisions

- The root repository remains a standard Agent Skill directory whose
  canonical instructions are `SKILL.md`.
- Pi/npm consumes the root package metadata and the root `SKILL.md` directly.
- skills.sh and SkillsMP consume the public GitHub repository and its standard
  `SKILL.md`; no platform-specific duplicate is added.
- The Codex plugin adapter is generated from the router's existing portable
  file manifest. Generated files are distribution output, not authoring
  sources.
- The initial package/plugin version is `0.1.0`. Future versions must be
  changed deliberately and kept consistent across package metadata and the
  generated plugin manifest.
- The package allowlist includes the skill instructions, required references,
  runtime validation scripts, templates, public documentation, changelog,
  and license. It excludes tests, OpenSpec change history, local instructions,
  caches, and other repository-only material.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| A package consumer receives internal or sensitive files | Use an explicit npm `files` allowlist and validate the actual pack dry-run file list. |
| The Codex adapter drifts from the canonical skill | Generate it from `references/cross-cli-portable-manifest.json` and validate byte-for-byte parity. |
| Consumers assume optional companion skills are bundled | Document the router's dependency boundary and distinguish the adapter from a self-contained workflow. |
| A community index treats discoverability as security certification | Document that indexes do not replace source inspection and disclose full-system-access implications. |
| A release workflow accidentally publishes | Keep external publication out of scripts/tests and verify only with local dry runs. |

## Approval status

- Change-id: `add-community-skill-distribution`
- Scope approval: the user explicitly authorized the bounded community scope
  (Agent Skills/GitHub, skills.sh, SkillsMP, Pi/npm, and Codex plugin) and
  closed-loop implementation on 2026-09-03.
- External publication approval: not granted and not required for this
  change; publication remains a documented handoff action.
