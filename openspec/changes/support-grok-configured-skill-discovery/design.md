# Design: Grok configured Skill discovery

## Decision

Treat native `grok inspect --json` as authoritative about the active Skill
source, but accept a configured source only when the transaction can prove that
the observed root is already one of its own governed runtime roots.

For `source.type == user`, retain the existing exact Grok-root rule. For
`source.type == configToml`, require all expected Skills to share one root equal
to a target `skills_root` in the reviewed plan. If it is another target, that
target must precede Grok and have a `verified` receipt for the same plan. Verify
the full portable closure at that source root before persisting discovery.

Include source type/root/path records and the verified source receipt digest in
the Grok discovery hash. Never read or mutate `config.toml`, and never accept an
arbitrary path merely because native output names it.

## Verification

Add one positive configured-Codex-root scenario and focused negative cases for
mixed roots, unplanned roots, unverified source receipt, and content drift.
Retain all existing default-root and wrong-path tests.

## Rollback

Restore the four scoped source/test files from a structured temporary backup.
Runtime targets remain protected by a new reviewed sync plan and existing
per-target transaction recovery.

