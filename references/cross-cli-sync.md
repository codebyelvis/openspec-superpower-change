# Cross-CLI Skill Synchronization

Use this reference after a validated change to portable runtime content in
`openspec-superpower-change`, `codex-brief-antigravity-review`, or the shared
global governance block.

## Authority and roles

- Canonical authority belongs only to the bound Codex `control-plane` /
  `control-plane-high` instance and contract; a product name alone grants no
  authority.
- Codex, Pi, Antigravity CLI, and Grok CLI are equally eligible for assigned
  executor or independent-reviewer roles. Their results are governed evidence
  until the bound control plane accepts them.
- Standard/strict external work uses different executor and reviewer identities.
  If the second auxiliary CLI is unavailable, Codex performs the distinct Review;
  if no distinct reviewer is available, the batch is `BLOCKED`.

## Trigger boundary

Run this gate when a path declared in
`references/cross-cli-portable-manifest.json` or the managed body in
`references/shared-global-governance.md` changes. A README, changelog, test,
design-history, or archived OpenSpec-only change does not trigger runtime sync.

## Scope-bound plan mode

The `plan` command keeps legacy no-selector behavior as sync-plan schema v1:
it contains the complete manifest mutation set and the managed rule operation.
Passing one or more explicit selectors switches to schema v2:

```text
--select-file <skill-name>:<portable-relative-path>   # repeatable
--select-managed-rule
```

Scoped mode is valid only for managed-rule version 6 and the exact target order
`codex`, `pi`, `antigravity-cli`, `grok-cli`. Selectors are normalized into
manifest order; duplicate, unknown, unsafe, sensitive, empty, or
not-target-complete selections are rejected before a plan is written. At least
one file or the managed rule must be selected.

Each v2 target partitions the complete manifest into `files` (mutation
operations) and `assertions` (read-only parity/prestate closure). The selected
managed rule is represented separately and defaults to `selected: false`.
Unselected files and an unselected rule must already be at canonical parity when
the plan is generated and are rechecked before apply. They are never backed up,
replaced, or included as transaction candidates. Verification, discovery,
digest, commit, and `verify-all` still cover the complete selected-plus-asserted
closure. The reviewed plan hash binds the selection, partition, source hashes,
and every destination pre-state.

### Canonical managed-rule destination binding

A schema-v2 `managed_rule.destination` is not an independently trusted path. It
must equal the target-specific canonical path derived from that target's
validated absolute `skills_root` (which must end in `/skills`): Codex, Pi, and
Grok use the parent runtime root with `AGENTS.md`, `APPEND_SYSTEM.md`, and
`AGENTS.md` respectively; Antigravity uses the grandparent `.gemini` root with
`GEMINI.md`. Plan generation and plan loading enforce this exact binding before
pre-state acceptance. Coherent edits to `destination` and its `pre_state` are
rejected before candidate, backup, or apply work, and downstream operations
consume only the validated binding.

## Runtime surfaces

Defaults may be overridden by environment variables, but all resolved paths must
remain inside their declared roots:

| Target | Skill root | Global rule file |
|---|---|---|
| Codex | `${CODEX_HOME:-$HOME/.codex}/skills` | `${CODEX_HOME:-$HOME/.codex}/AGENTS.md` |
| Pi | `${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}/skills` | `${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}/APPEND_SYSTEM.md` |
| Antigravity CLI | `${ANTIGRAVITY_CLI_HOME:-$HOME/.gemini/antigravity-cli}/skills` | `$HOME/.gemini/GEMINI.md` |
| Grok CLI | `${GROK_HOME:-$HOME/.grok}/skills` | `${GROK_HOME:-$HOME/.grok}/AGENTS.md` |

Installed targets selected by the user are `required`. `not-applicable` is valid
only for an uninstalled, unsupported, or explicitly excluded target and requires
Codex owner, evidence, reason, and resume condition. Failure, staleness, or
discovery failure is `BLOCKED`, never `not-applicable`.

## Managed global rule block

`references/shared-global-governance.md` is the canonical managed body. Each
global rule file contains exactly one matching versioned begin/end marker block.
Only bytes inside that block may change; native CLI rules outside it must remain
byte-identical. Parity requires all stable `CCG-*` invariant IDs and the canonical
body SHA-256.

## Safe sequence

```text
validated source + Review PASS
-> generate path/hash-only sync plan
-> Review plan and target snapshots
-> apply one target atomically
-> validate target manifest, managed block, skill validators, and discovery
-> repeat next target
-> verify all required targets
-> final Review
```

Each target uses a durable receipt installed before mutation and remains
uncommitted through content and discovery verification. Failure restores only
the current target from its verified secure backup, verifies the reviewed
preimage, and stops before later targets. Recovery-blocked evidence is retained
for manual disposition. Rule backups and receipts are mode `0600`, remain
outside every Skill discovery root, and never have their contents logged.

## Portable and forbidden content

Only manifest-declared `SKILL.md`, linked `references/`, required `scripts/`,
`templates/`, and supported metadata are portable. Reject absolute/traversal or
URL paths, backslashes, symlink escapes, and non-regular files.

Never synchronize credentials, auth/token files, sessions, history, logs,
caches, model/settings files, hooks, MCP secrets, CLI binaries, or `.env`/private
key material. Diagnostics report only path and category, never matching values.

## Verification

- All targets: portable path/SHA-256 parity, managed-block parity, quick validator,
  and repository-specific validator.
- Pi: deterministic root and portable closure validation never invokes Pi. An
  explicitly requested process probe must use a fresh temporary HOME and
  `PI_CODING_AGENT_DIR`, deny native-root reads/writes and network, disable
  sessions/context/Skills, and expose read-only tools only; otherwise it is
  `BLOCKED`.
- Antigravity CLI: deterministic root, linked-file closure, and validators;
  an optional non-mutating prompt cannot replace these checks.
- Grok CLI: deterministic checks plus `grok inspect --json` path verification.
  Inspect output is mode `0600`, read only for required skill paths, not echoed,
  and removed after verification.

Before schema-6 deployment, active schema-4/schema-5 contracts drain under their
frozen runtime. Complete legacy history remains immutable and never authorizes a
schema-6 transition. Do not claim global Skill optimization complete until all
four required targets and the final bound-control-plane Review pass.
