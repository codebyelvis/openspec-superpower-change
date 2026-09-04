# Change: Support Grok configured Skill discovery

## Why

Grok may intentionally discover user Skills from a configured shared root such
as the already governed Codex Skill root. The current sync verifier accepts only
Grok's default user root and therefore blocks even when native `grok inspect`
proves that Grok loads the freshly verified canonical files from another target
in the same reviewed transaction.

## What Changes

- Keep default Grok user-root discovery unchanged.
- Accept `configToml` discovery only when every expected Skill resolves beneath
  one consistent Skill root already bound in the same sync plan.
- Require that source target's receipt to be verified under the same plan and
  require complete canonical parity before accepting the Grok discovery digest.
- Bind the observed source type, root, paths, and source-target receipt digest
  into Grok discovery evidence.
- Reject mixed roots/types, paths outside planned roots, an unverified source
  target, or any content drift.

## Scope

- `scripts/validate_cross_cli_sync.py`
- `tests/test_cross_cli_sync.py`
- `references/cross-cli-sync.md`
- `references/sync-checklist.md`

No Grok configuration file is modified. No plan schema, target order, evidence
profile, lifecycle value, Git authority, publication authority, or managed rule
changes.

## Approval Status

- Change-id: `support-grok-configured-skill-discovery`
- Status: explicitly approved by the user on 2026-09-04
