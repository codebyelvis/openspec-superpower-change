# streamline-simple-change-gates Control-Plane Adjudication

## Decision

`CONTROL_PLANE_ADJUDICATION: CONTINUE`

The terminal `FOCUSED_RECHECK` closed findings 1, 2, 4, 5, and 6 and blocked
only because the runtime-sync execution sequence omitted discovery verification
and post-commit rollback handling. No scope, contract/spec, acceptance,
risk/evidence profile, authority, assignment, allowed/forbidden-file,
branch/worktree, database/production, or Git/publication/deployment boundary
changed.

## Resolution

The Plan now binds each target to
`apply -> verify -> verify-discovery -> commit-target`, captures Grok discovery
through a private `grok inspect --json` artifact, restores an uncommitted failed
target with `restore-target`, and handles post-commit abandonment by restoring
the validated canonical source backup and executing a newly reviewed reverse
schema-v2 sync plan. This matches the script state machine: `commit-target`
requires both content and discovery digests, while `restore-target` accepts only
pending receipt states.

The correction is mechanical and remains inside the approved execution and
rollback boundaries. Under the existing bounded-convergence contract, this
adjudication is not a third Preflight and does not request or authorize R3.
Implementation may proceed under the already approved OpenSpec change, with the
separate Implementation Review and Final Review retained for this Major change.

Before apply, deterministic plan generation rejected the environment-derived
`/Users/elvis/.codex-account-a` binding because it has no canonical Codex rule
file or installed target skill. Read-only inventory bound the actual existing
Codex runtime to `/Users/elvis/.codex/skills` and `/Users/elvis/.codex/AGENTS.md`;
the other three target bindings were unchanged. No runtime mutation occurred.
The Plan now uses that existing canonical Codex installation. This corrects the
target path without adding a target or changing synchronization authority.

## Evidence

- Initial and terminal reviewer: `01a06b80-4efd-7dc2-8455-489f2c4da6c1`
- Terminal reviewed Plan SHA-256:
  `0258a99a73a37964253399d90ec1ba43c664640dc1ab6d954ee2971d254e99fc`
- Canonical backup: `/tmp/openspec-review-flow-backup.7cZ0C2`
- Worktree:
  `/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-skillsmp-index-adapter`
- Branch/base: `add-skillsmp-index-adapter` /
  `272e37467f2ec8b29a72daac61c873bc612d12d2`
