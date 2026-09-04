# Implementation tasks

## Proposal and design

- [x] Research Pi/npm, Agent Skills, skills.sh, SkillsMP, and Codex plugin
  distribution contracts.
- [x] Record the canonical-source model and scope boundaries in the proposal
  and design.
- [x] Run `openspec validate add-community-skill-distribution --strict` and
  resolve any contract errors before implementation.

## Package and documentation

- [x] Add root Pi/npm metadata with version, keyword, manifest, repository,
  license, and explicit package allowlist.
- [x] Add public distribution/install documentation and link it from the
  repository README files.

## Codex adapter

- [x] Read and apply the plugin scaffold requirements.
- [x] Add a deterministic builder for the generated skill-only Codex plugin.
- [x] Generate the adapter from the existing portable manifest.
- [x] Add validation for plugin manifest shape, source parity, symlinks, and
  unexpected generated content.

## Verification

- [x] Add focused unit tests for metadata, package boundaries, and adapter
  parity.
- [x] Run npm package dry-run and local skills discovery checks.
- [x] Run the project quick validator, core-gate validator, and full test suite.
- [x] Perform an independent diff/review pass and fix all returned findings.
- [x] Run Project Learning Closeout and promote the symlink-boundary invariant
  after the required independent Review pass.
- [x] Hand off external publication steps without executing Git writes or
  external publication.
