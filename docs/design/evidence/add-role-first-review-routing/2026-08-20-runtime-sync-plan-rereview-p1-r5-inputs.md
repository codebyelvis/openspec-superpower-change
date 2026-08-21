# Four-target Runtime Sync-plan High Re-review Inputs — P1 R5

## Assignment and authority

- reviewer product: `codex`
- reviewer role: `independent-reviewer`
- reviewer profile: `control-plane-high`
- reviewer implementation: fresh no-history `gpt-5.6-luna`, reasoning `max`,
  selected by the user to reduce token cost without weakening the gate
- independence: distinct from source authors, plan generator, target executor,
  all source/plan reviewers, and the original decision owner
- purpose: decide whether the regenerated read-only four-target runtime plan
  plus the corrected private-root containment boundary authorize runtime apply
- result authority: sync-plan Review evidence only; only the original control
  plane may accept it and authorize apply

Return one `PASS`, `FAIL`, or `BLOCKED`. Any actionable finding blocks apply.
Remain read-only: no Git, Pi, source/runtime mutation, replacement plan, Review
artifact write, self-acceptance, promotion, or completion claim.

## Accepted source gate and correction history

The original control plane accepts the persisted P1 R5 Candidate Source High
Review `PASS`. The prior runtime Sync-plan Review `FAIL` remains immutable
history and its old plan must not be reused.

| Input | Mode | SHA-256 |
|---|---:|---|
| P1 R5 source Review `docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r5.md` | `0644` | `073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4` |
| P1 R5 source input | `0644` | `9f95e38b666b862f2c954ec8e7d3b91f2528ec4756c508ae06c158a681ef4766` |
| prior runtime Sync-plan FAIL | `0644` | `8562b0ed1d4ef17dc34f100e783e72b02ae40138f8888b7516ef2566ecb255a8` |
| approved Plan | `0644` | `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| OpenSpec design | `0644` | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| OpenSpec specification | `0644` | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| OpenSpec tasks | `0644` | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| portable manifest | `0644` | `3c24865244034bdb6815c321db4ceaa69c903a6e6f4cb4e7154cd88f01ed7a8d` |
| corrected sync validator | `0644` | `332de6171495faa12b3acd6c7c39e8ee35972a9c87eebe216d9581cc3b520044` |
| corrected cross-CLI tests | `0644` | `97d46aec7247ab9e0f93d60b2c017248e22e4b54d2c53f3f01eaa83d0c9b1ed2` |

The source Review independently exercised 45/45 equality, nested,
other-target, normalized, existing-symlink-ancestor, direct-helper,
apply/restore/recover/verify/discovery/commit/verify-all combinations with no
unsafe side effect and found no P0/P1/P2.

## Fresh legacy drain and regenerated plan

| Input | Mode | SHA-256 |
|---|---:|---|
| `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/legacy-drain-r5.json` | `0600` | `cc1355940bbcaabff01bc242d8dcee62998f9570ca26421b192cdfd6c3a77983` |
| durable legacy summary | `0644` | `c3dd76b95090459c64251c0797c2842b449693b3241313907a7e5d937638202c` |
| new `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/runtime-sync-plan-r5.json` | `0600` | `6ae0cc4dcca9fbc8de9d1e4c1fc050d0fcc4dc7bde445a6bda85bb6845a51156` |
| frozen old `runtime-sync-plan.json` | `0600` | `63cb8288b704cd50e4c5bfa9318984fd958fa554c0e4e4c534e8c5cce3b3ed5d` |
| structured private root | `0700` | directory binding |

Fresh legacy result is `legacy_audit: "pass"`, `active_legacy_count: 0`,
`records: []`. The new plan command returned `plan: "pass"`. Fresh
`verify-prestate --target all` returned `prestate: "pass"` in exact order
`codex`, `pi`, `antigravity-cli`, `grok-cli`.

The new plan is 89,076 bytes. Its exact top-level schema is unchanged, contains
39 portable records plus one native managed-rule preimage per target, all
current preimages are regular files, and it serializes no content/native-body
field. The plan target object keys are JSON-sorted; exact execution order must
therefore be proven independently from the bound manifest, `TARGET_ORDER`,
plan validation, prior-target receipt gating, and tests.

## Exact target and private-root boundary

| Target | Skills root | Native rule file |
|---|---|---|
| `codex` | `/Users/elvis/.codex/skills` | `/Users/elvis/.codex/AGENTS.md` |
| `pi` | `/Users/elvis/.pi/agent/skills` | `/Users/elvis/.pi/agent/APPEND_SYSTEM.md` |
| `antigravity-cli` | `/Users/elvis/.gemini/antigravity-cli/skills` | `/Users/elvis/.gemini/GEMINI.md` |
| `grok-cli` | `/Users/elvis/.grok/skills` | `/Users/elvis/.grok/AGENTS.md` |

The intended apply revision binds these new absent private roots:

- backup root:
  `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/runtime-backups-r5`;
- transaction root:
  `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/runtime-transactions-r5`.

Both are absent at Review start, are children of the mode-`0700` structured
private root, and resolve outside every declared Skill discovery root. The old
unstarted `runtime-backups` / `runtime-transactions` names also remain absent.
Review the exact corrected guard at production entry points and prove these
proposed roots cannot be substituted into any discovery root before backup,
lock, receipt, restore, or destination mutation. Runtime apply must use only
the new plan SHA/path and these reviewed R5 root names.

## Required review scope

Read Router/Companion instructions and Skills, OpenSpec/Plan, source PASS,
prior plan FAIL, sync checklist/contract, manifest, complete new plan,
validator, and tests. Independently verify at start and end:

1. all bound hashes, types, modes, plan/source/destination preimages;
2. exact roots, containment, closure, uniqueness, symlink/type boundaries,
   manifest/managed-v6 semantics, and absence of sensitive/native contents;
3. all four discovery roots and preservation of `/Users/elvis/.agents/skills`
   symlinks outside the exact destination closure;
4. corrected backup/transaction containment against equality, nesting,
   another target, normalization, existing symlink ancestor, and direct helper
   or recovery bypass, always before any side effect;
5. exact order and later-target blocking until prior receipt is verified;
6. private modes, exclusive backup creation, receipt durability, exact restore,
   recovery-blocked/manual disposition, crash restart, and no early cleanup;
7. Pi isolation without invoking Pi, deterministic Codex/Antigravity
   discovery, Grok inspect contract, and sensitive-category exclusions;
8. zero legacy drain and non-authorizing completed legacy history;
9. all exact stop conditions and fresh prestate at both Review boundaries.

Use only read-only checks and isolated temporary fixtures. Do not inspect
unrelated native contents; bound plan path/hash/mode/prestate data is enough.

## Required output

Return one complete neutral Markdown Review suitable for verbatim persistence:
assignment/independence, start/end bindings, root/closure/preimage/order/
exclusion/backup/restore analysis with path:line/test evidence, isolated
adversarial results, fresh validation, findings by severity and exact resume
conditions, final `PASS`/`FAIL`/`BLOCKED`, and an explicit statement whether
runtime apply may begin.

The intended artifact is
`docs/design/reviews/2026-08-20-add-role-first-review-routing-runtime-sync-plan-rereview-p1-r5.md`.
It must remain absent during Review; the reviewer must not write it.
