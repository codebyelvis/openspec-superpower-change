# Distribution and installation

The canonical source is the repository root and its `SKILL.md`. The generated
Codex adapter under `distribution/codex-plugin/` is release output, not a
second authoring source.

The generated `skills/openspec-superpower-change/SKILL.md` file is a
catalog-compatibility adapter for nested-path indexers. It is also not an
authoring source and must remain byte-identical to the root `SKILL.md`.

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
scripts before enabling the skill. A successful CLI install does not guarantee
immediate search visibility; third-party ingestion and indexing are
asynchronous and outside this repository's control.

## [SkillsMP](https://skillsmp.com/)

Search for `openspec-superpower-change` or the public GitHub repository in
SkillsMP. The repository exposes the generated nested compatibility path
`skills/openspec-superpower-change/SKILL.md` for catalog discovery while the
root `SKILL.md` remains canonical. Regenerate it after root changes with:

```bash
python3 scripts/build_skillsmp_adapter.py .
```

SkillsMP is not the canonical source and does not replace source review. Its
crawler and search refresh are asynchronous; generating or pushing the adapter
cannot guarantee a listing time.

## [Pi/npm](https://pi.dev/packages)

```bash
pi install npm:openspec-superpower-change
```

The root `package.json` uses the `pi-package` keyword and maps `pi.skills` to
`./SKILL.md`. Before publication, verify locally with `npm pack --dry-run`.
The direct package/detail page and catalog search may refresh through different
third-party paths, so successful npm publication does not guarantee immediate
Pi search visibility.

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

Run `python3 scripts/build_skillsmp_adapter.py .`, the repository validators,
the full test suite, `npm pack --dry-run --json`, and the local skill discovery
check before publishing. This repository change does not execute `npm publish`,
Codex portal submission, or a community upload. Git staging, commit, and push
remain separate maintainer actions. Pi, skills.sh, and SkillsMP search results
are asynchronous third-party state and are not guaranteed by a successful
local build, install, or package publication.

ClawHub is intentionally out of scope for this MIT-licensed repository because
its current publication contract requires MIT-0.
