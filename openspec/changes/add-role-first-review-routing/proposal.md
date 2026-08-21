# Change: Add role-first Review routing

## Why

The workflow already binds product, instance, role, and capability profile in
governed schema-5 Handoffs, but standalone Review recommendations and generated
prompts may still say only “another agent” or “an independent agent”. That leaves
the user to infer which product should receive the task, whether a new instance
is required, and whether the result is advisory evidence or a governed gate.

The current schema-5 `independent_reviewer_assignment` is also an exact
four-field mapping. Adding Review purpose, an explicit independence condition,
and result authority in place would either invalidate existing schema-5
contracts or leave new governed assignments fail-open. The new complete
Reviewer Assignment therefore requires a new Handoff schema boundary rather
than an ambiguous optional-field retrofit.

The current product allowlist also admits Codex, Antigravity CLI, and Grok CLI
but excludes Pi even though Pi exposes the required coding-agent primitives,
Skill loading, context-file loading, independent sessions, and read-only tools.
That exclusion reflects incomplete governance integration rather than a
role-based authority distinction.

## What Changes

- Add a single managed global invariant requiring every Review request,
  recommendation, prompt, or Handoff to state the Review purpose and name one
  concrete reviewer product, role, capability profile, instance-independence
  requirement, and result authority. Missing or blank purpose and generic
  unresolved destinations become invalid.
- Introduce Handoff schema 6 for newly created governed external work. Its
  immutable `reviewer_assignment` contains a structured Review purpose,
  reviewer product and instance, role, capability profile, structured
  independence requirement, and result authority.
- Admit `pi` in the schema-6 canonical product enum alongside `codex`,
  `antigravity-cli`, and `grok-cli` for executor and independent-reviewer roles.
- Keep the bound Codex `control-plane` instance as the sole owner of routing,
  evidence acceptance, canonical state, and final completion.
- Preserve user-selected reviewer products; when the user does not select one,
  require the control plane to recommend one concrete eligible product rather
  than return an unresolved “other agent” instruction.
- Add Pi as a required portable runtime target with Skill root
  `${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}/skills` and managed global-rule file
  `${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}/APPEND_SYSTEM.md`.
- Upgrade the managed governance block from version 5 to version 6 with exact
  invariant IDs `CCG-001` through `CCG-016` across Codex, Pi, Antigravity CLI,
  and Grok CLI. Revise `CCG-001`, `CCG-002`, and `CCG-010` so the same block binds canonical
  authority to the assigned Codex control-plane role/profile/instance/contract
  while giving all four products equal schema-6 executor/reviewer eligibility,
  preserving legacy schema boundaries, and preventing product names alone from
  granting authority.
- Extend Router and Companion validators, fixtures, forward-tests, sync
  planning, discovery/parity evidence, and rollback handling for Pi and the
  explicit reviewer-assignment contract.
- Freeze schema-4/schema-1 and schema-5 parent-context schema-2 validation,
  product sets, exact assignment shapes, and transition semantics. Pi is
  admitted only by a schema-6 parent context and cannot be backfilled into older
  authorization.
- Before any runtime upgrade, inventory every known canonical Handoff and require
  every active schema-4 or schema-5 contract to reach `complete` under its
  existing runtime/schema. After the switch, older complete contracts remain
  immutable history and cannot authorize a new transition.
- Isolate every Pi capability/help/prompt probe from the native Pi agent root by
  using fresh temporary process roots and denying native-root access. Direct
  `pi --help` or prompt probes against the native root are forbidden; actual Pi
  target validation remains deterministic and limited to declared Skill/global
  rule paths.

## Impact

- Affected spec: `skill-workflow-governance`.
- Affected source repositories:
  `openspec-superpower-change` and `codex-brief-antigravity-review`.
- Affected source surfaces: the two Skill entry points; capability, response,
  Handoff, Review, cross-CLI, and shared-governance references; validators;
  portable manifest; tests and fixtures; README/changelog only when needed to
  keep public documentation accurate.
- Affected runtime surfaces after separate implementation approval: declared
  Codex, Pi, Antigravity CLI, and Grok CLI Skill roots and their managed global
  rule blocks.
- Compatibility: existing active schema-4 and schema-5 contracts remain valid
  only under their frozen pre-upgrade validators and must finish before runtime
  deployment. Existing complete schema-4/schema-5 contracts and schema-1/schema-2
  evidence remain immutable history and are not revalidated as schema 6. New
  Handoffs use schema 6; no missing-field, timestamp, path, or prose inference may
  classify a newly supplied old-shape contract as grandfathered.
- Risk profile: standard Major Self-Evolution with `control-plane-high` Review,
  because routing, reviewer identity, validation, shared global governance, and
  required runtime synchronization change.

## Non-Goals

- Make Pi, Antigravity CLI, or Grok CLI a canonical control-plane owner.
- Let any executor or independent reviewer promote its own result or declare
  final completion.
- Derive authority from a model name, provider, benchmark, or product brand.
- Replace the closed fail-closed product allowlist with automatic discovery of
  arbitrary agents.
- Synchronize Pi credentials, auth, sessions, histories, model settings,
  caches, extensions, binaries, or any other CLI-native private state.
- Modify, re-ratify, merge, or clean the active `add-codex-skill-update` change
  or any archived change.
- Rewrite, migrate, resume after cutover, or grant new authority to any existing
  schema-4/schema-5 Handoff or schema-1/schema-2 evidence artifact.
- Grant Git staging, commit, push, publication, deployment, or destructive
  cleanup authority.

## Approval Status

- Change-id presented to user: `add-role-first-review-routing`.
- The user confirmed the role-first four-product design direction on
  2026-08-10. That design confirmation does not yet approve implementation of
  this exact artifact revision.
- Independent Proposal Review of the prior artifact revision returned
  `BLOCKED`: `RFRR-002` through `RFRR-005` were closed, while `RFRR-001` remained
  open because governed Handoff schema/compatibility was ambiguous. The user
  selected the schema-6 correction on 2026-08-10. This revision must receive a
  fresh independent Review and must not reuse either prior verdict as PASS.
- Strict validation result: `PASS` —
  `openspec validate add-role-first-review-routing --strict`.
- [ ] Independent proposal Review PASS from a new-window Codex with role
  `independent-reviewer`, profile `control-plane-high`, and an instance that did
  not author these artifacts.
- [ ] This specific scoped change-id approved for implementation.
