# Distribution and installation

The canonical source is the repository root and its `SKILL.md`. The generated
Codex adapter under `distribution/codex-plugin/` is release output, not a
second authoring source.

## Agent Skills and GitHub

Clone or point an Agent Skills-compatible client at:

`https://github.com/codebyelvis/openspec-superpower-change`

The skill entry point is `SKILL.md`. Review referenced files and scripts before
installing; a host client may grant a skill broad local-system access.

## [skills.sh](https://skills.sh/)

```bash
npx skills add codebyelvis/openspec-superpower-change
```

skills.sh is a discovery/install path over the public repository. Its listing
is not a security certification. Inspect the source, references, and any
scripts before enabling the skill.

## [SkillsMP](https://skillsmp.com/)

Search for `openspec-superpower-change` or the public GitHub repository in
SkillsMP. SkillsMP indexes public `SKILL.md` sources; it is not the canonical
source and does not replace source review. Follow the repository instructions
shown by the index rather than assuming a separate upload or API exists.

## [Pi/npm](https://pi.dev/packages)

After a maintainer publishes the package to npm:

```bash
pi install npm:openspec-superpower-change
```

The root `package.json` uses the `pi-package` keyword and maps `pi.skills` to
`./SKILL.md`. Before publication, verify locally with `npm pack --dry-run`.

## [Codex plugin](https://developers.openai.com/plugins/build/plugins)

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
