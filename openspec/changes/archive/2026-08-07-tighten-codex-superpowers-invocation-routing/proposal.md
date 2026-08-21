# Change: Tighten Codex Superpowers invocation routing

## Why

The archived `2026-07-20-streamline-workflow-prompt-contracts` change already
established phase-aware Superpowers routing, prompt-collision tests, and the
Router-owned Completion Contract. Its requirements are present in the base
`skill-workflow-governance` spec and SHALL NOT be re-added or reopened as an
active change.

A fresh account-a Codex process exposed one remaining host-specific collision:
`superpowers:using-superpowers` is implicitly selected at conversation start,
so ordinary questions enter a redundant meta-workflow before native Skill
matching. Independent Review agreed that the Router should own governed
Superpowers method selection, but rejected an unproven design that would make
Router-required children explicit-only.

Isolated Codex CLI 0.147.0 probes resolved the key runtime uncertainty for this
revision: a user-explicit child loaded successfully, while an activated Router
could not natively load the same child after it was made explicit-only. This
follow-up therefore narrows only the redundant Codex meta-entry and strengthens
authority precedence without claiming unsupported nested Skill activation.

## What Changes

- Make only `superpowers:using-superpowers` unavailable for implicit Codex
  invocation through product-specific `agents/openai.yaml` metadata. Preserve
  user-explicit `$superpowers:using-superpowers` and leave shared Skill text and
  non-Codex Superpowers discovery metadata unchanged.
- Keep Router-required Superpowers children eligible for native implicit
  matching until a supported runtime proves Router-to-explicit-only-child
  loading without shell/filesystem fallback or user `$child` input.
- Define the Router as the normative selector of zero or more Superpowers
  methods for governed work; users do not need to name each selected method.
- Strengthen portable `CCG-014` so neither broad metadata nor a user-explicit
  `$superpowers:*` request can bypass Router Gate 0 or grant workflow, Git,
  business, or completion authority. Synchronize managed-rule version 5 to all
  declared required runtimes.
- Define exact routes for ordinary questions, diagnose-only work,
  proposal-only work, Direct Change, ordinary read-only Review, Router
  Review-only, high-risk implementation, completion, and explicit sub-skill
  requests.
- Add RED/GREEN source tests, isolated fresh-session forward-tests,
  fail-closed Router tests, bounded phase-chain tests, cross-host isolation
  checks, and exact source/runtime rollback evidence.

## Non-Goals

- Do not reopen or duplicate the completed Option 2, Completion Contract,
  Companion isolation, or measured prompt-load requirements from the archived
  parent change.
- Do not make Router-required children explicit-only in this revision.
- Do not require the user to name every `$superpowers:*` Skill or remove the
  Superpowers family.
- Do not change the shared `using-superpowers/SKILL.md` description or body.
- Do not change non-Codex Superpowers discovery or invocation metadata.
- Do not weaken OpenSpec approval, TDD, Preflight, Review, verification,
  evidence, Git authority, runtime synchronization, or final completion rules.
- Do not fetch, merge, reset, clean, commit, push, publish, or reconcile the
  divergent Superpowers Git checkout under this approval contract.

## Impact

- Affected spec: `skill-workflow-governance`.
- Predecessor, not active implementation scope:
  `openspec/changes/archive/2026-07-20-streamline-workflow-prompt-contracts/`.
- Router source surfaces: `references/superpowers-adapter.md`,
  `references/request-modes.md`, `references/shared-global-governance.md`,
  `references/cross-cli-portable-manifest.json`, validators, tests, README files,
  and changelog.
- Source-managed Superpowers surfaces:
  `skills/using-superpowers/agents/openai.yaml`, `docs/README.codex.md`, and
  `tests/codex/using-superpowers-invocation-policy.test.js`.
- Runtime surfaces: managed-rule version 5 in the declared Codex, Antigravity
  CLI, and Grok CLI rule targets; Codex-only `using-superpowers` metadata in the
  live Superpowers checkout that is also the symlink-discovered runtime target.
- Superpowers staging: RED/GREEN and source validation occur in a
  non-discoverable structured copy of the exact live pre-state. The reviewed
  three-file delta is then applied once to the combined source/runtime target
  with immediate verification or byte-exact rollback.
- Compatibility: shared Superpowers Skill bytes and non-Codex Superpowers
  discovery metadata remain unchanged; Router approval and completion outcomes
  remain at least as strict.
- Risk: Major Self-Evolution because Skill routing, global authority precedence,
  and runtime discovery behavior change.

## Evidence Boundary

- Codex CLI 0.147.0 observed user-explicit child activation succeeding.
- The same isolated environment observed Router-to-explicit-only-child return
  `CHILD_LOAD_BLOCKED` without shell/filesystem fallback.
- Therefore only `using-superpowers` may become Codex explicit-only in this
  change. Any child-policy expansion requires new repeatable evidence and a new
  approved scope.
- Runtime-path/hash evidence SHALL be preserved or rerun during RED evidence;
  this proposal does not treat the preliminary transcript as implementation
  verification.

## Approval Status

- On 2026-08-07 the user authorized extending the prior design direction and
  submitting it for reapproval.
- Independent Review then proved the original change was already archived and
  its requirements merged, so this contract uses a follow-up change-id instead
  of reviving the completed change.
- Independent read-only delta Review PASS was recorded on 2026-08-07 for this
  follow-up proposal/design/spec/tasks revision, with no actionable findings and
  no implementation, Git, update, switch, cleanup, or runtime action.
- That authorization permits proposal correction and Review only; it does not
  authorize implementation or runtime synchronization.
- [x] The exact change-id `tighten-codex-superpowers-invocation-routing` and its
  complete scoped contract are approved for implementation.
