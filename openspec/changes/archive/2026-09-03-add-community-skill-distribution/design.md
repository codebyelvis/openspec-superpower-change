# Design: Community distribution adapters

## Canonical-source model

The repository root remains the authoring source:

```text
repository root/
├── SKILL.md                         # canonical skill router
├── references/                       # canonical supporting references
├── scripts/                          # canonical validators used by the skill
├── templates/                        # canonical workflow templates
├── package.json                       # Pi/npm release metadata
└── distribution/
    └── codex-plugin/                 # generated Codex distribution artifact
```

The Codex adapter is intentionally outside the root `skills/` directory so
skills.sh-style scanners do not discover a duplicate skill. Its contents are
generated from the `pi` router entry in
`references/cross-cli-portable-manifest.json` and are checked against that
manifest.

## Pi/npm package

The root `package.json` will:

- use the repository package name and initial version `0.1.0`;
- include the `pi-package` keyword;
- map `pi.skills` to `./SKILL.md`;
- declare the MIT license and public repository/homepage;
- use an explicit `files` allowlist for the publishable surface.

This supports `pi install npm:openspec-superpower-change` after a maintainer
publishes the package. The repository itself remains directly usable by
standard Agent Skills clients.

## Standard indexes

The public README and a dedicated distribution document will show the
repository source and commands for:

- skills.sh: `npx skills add codebyelvis/openspec-superpower-change`;
- SkillsMP: search/index the public GitHub repository and install from source;
- Pi: `pi install npm:openspec-superpower-change` after npm publication;
- Codex: install the generated plugin directory or use the published plugin
  submission flow after a maintainer reviews the generated artifact.

The documentation will distinguish a directory index from a package registry
and will include a source/security review warning because skills can execute
scripts and may have broad local-system access depending on the host client.

## Codex plugin adapter

The generated plugin will contain:

- `.codex-plugin/plugin.json` with plugin metadata, a non-empty author and
  interface block, and `skills: "./skills/"`;
- `skills/openspec-superpower-change/SKILL.md`;
- every file listed for the `openspec-superpower-change` router in the
  portable manifest, preserving relative paths;
- a generated README that explains provenance and regeneration.

The adapter will not invent or rewrite workflow instructions. If the source
manifest changes, the builder and validator will surface the required
regeneration. If the manifest does not change, this distribution-only change
does not invoke the cross-CLI runtime-sync workflow.

## Validation strategy

Validation has four layers:

1. OpenSpec strict validation for the change contract.
2. Unit tests for metadata, manifest projection, generated-file parity, and
   forbidden package paths.
3. The repository's existing core-gate validator and full test suite.
4. Local release dry runs: `npm pack --dry-run --json` and `npx skills ...
   --list`, with no network publication or account-side submission.
