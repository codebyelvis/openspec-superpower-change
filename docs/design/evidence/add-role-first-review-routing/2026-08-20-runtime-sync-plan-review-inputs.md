# Four-target Runtime Sync-plan High Review Inputs

## Assignment and authority

- reviewer product: `codex`
- reviewer role: `independent-reviewer`
- reviewer profile: `control-plane-high`
- reviewer implementation: fresh no-history `gpt-5.6-luna`, reasoning `max`,
  selected by the user to reduce token cost without weakening the gate
- independence: distinct from source authors, plan generator, target executor,
  prior source reviewers, and the original decision owner
- purpose: decide whether the read-only four-target runtime plan correctly
  binds roots, source bytes, destination preimages, closure, managed rules,
  exclusions, target order, backups, restore conditions, and stop boundaries
- result authority: sync-plan Review evidence only; only the original control
  plane may accept it and authorize runtime apply

Return only `PASS`, `FAIL`, or `BLOCKED`. Any actionable finding blocks apply.
The reviewer must remain read-only and must not run Git or Pi, modify any
runtime/source file, generate a replacement plan, or accept its own verdict.

## Accepted source gate

The original control plane accepts the persisted P1 R4 Candidate Source High
Review `PASS` as the Task 7 implementation-evidence gate:

| Input | Mode | SHA-256 |
|---|---:|---|
| `docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r4.md` | `0644` | `579c4486fadd8574af24ae112e81519b87d266cdecb0621c30b7c176ec0dce70` |
| `docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md` | `0644` | `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| `openspec/changes/add-role-first-review-routing/design.md` | `0644` | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| `openspec/changes/add-role-first-review-routing/specs/skill-workflow-governance/spec.md` | `0644` | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| `openspec/changes/add-role-first-review-routing/tasks.md` | `0644` | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| `references/cross-cli-portable-manifest.json` | `0644` | `3c24865244034bdb6815c321db4ceaa69c903a6e6f4cb4e7154cd88f01ed7a8d` |
| `scripts/validate_cross_cli_sync.py` | `0644` | `8d8a18a4c6d9a7639fe963e08c1a799b0c5a531129fd6195c8cd9fd8c4315f1e` |

## Legacy drain gate

The exact Task 8 legacy inventory command exited `0` with
`legacy_audit: "pass"`, `active_legacy_count: 0`, and no records. Core gates
also passed.

| Input | Mode | SHA-256 |
|---|---:|---|
| `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/legacy-drain.json` | `0600` | `cc1355940bbcaabff01bc242d8dcee62998f9570ca26421b192cdfd6c3a77983` |
| `docs/design/evidence/add-role-first-review-routing/2026-08-20-legacy-drain-summary.json` | `0644` | `c3dd76b95090459c64251c0797c2842b449693b3241313907a7e5d937638202c` |

Confirm that any nonzero active legacy count would block deployment, completed
legacy history would remain immutable/non-authorizing, and an empty record set
does not migrate or rewrite anything.

## Bound runtime plan

The exact approved Task 8 `plan` command exited `0` with `plan: "pass"` and
wrote:

| Input | Mode | SHA-256 |
|---|---:|---|
| `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/runtime-sync-plan.json` | `0600` | `63cb8288b704cd50e4c5bfa9318984fd958fa554c0e4e4c534e8c5cce3b3ed5d` |

The plan has exact top-level keys `managed_rules`, `manifest_path`,
`manifest_sha256`, `schema_version`, `sources`, and `targets`. Recursive object
keys contain only target/source identifiers and these path/hash/status fields:
`decision_owner`, `destination`, `evidence`, `files`, `id`, `invariant_ids`,
`kind`, `mode`, `path`, `pre_state`, `reason`, `result`, `resume_condition`,
`rule_file`, `rule_pre_state`, `selection`, `sha256`, `skill`, `skills_root`,
`source_alias`, and `version`. No content/native-body field is present.

The four target records each have 39 file entries, all currently bound as
regular-file preimages, and `result: "pending"`:

| Target | Skills root | Native rule file |
|---|---|---|
| `codex` | `/Users/elvis/.codex/skills` | `/Users/elvis/.codex/AGENTS.md` |
| `pi` | `/Users/elvis/.pi/agent/skills` | `/Users/elvis/.pi/agent/APPEND_SYSTEM.md` |
| `antigravity-cli` | `/Users/elvis/.gemini/antigravity-cli/skills` | `/Users/elvis/.gemini/GEMINI.md` |
| `grok-cli` | `/Users/elvis/.grok/skills` | `/Users/elvis/.grok/AGENTS.md` |

The plan schema does not serialize a separate `target_order` field. Determine
whether the combination of the bound manifest order and production constant /
validator / apply state machine still proves exact execution order
`codex → pi → antigravity-cli → grok-cli`; treat any ambiguity as a finding.

## Required review scope

Read the Router and Companion instructions/Skills, approved OpenSpec and full
Plan, accepted source Review, sync checklist, portable manifest, sync
validator/tests, legacy drain, and complete runtime plan. Independently verify:

1. exact start/end hash and mode of every bound input;
2. plan schema, source roots, manifest hash, managed v6 IDs/body hash, and
   absence of native/sensitive contents;
3. every source path/hash and destination preimage path/kind/mode/hash;
4. containment, symlink/type boundaries, deterministic 39-file closure per
   target, no missing/extra/duplicate destination, and preservation of
   `/Users/elvis/.agents/skills` symlinks outside the destination closure;
5. exact four-target order and later-target blocking until each earlier target
   is receipt-verified;
6. private mode-`0600` plan/receipts, mode-`0700` backup/transaction roots,
   exclusive backup creation, exact restore/rollback conditions, manual
   disposition behavior, and no cleanup before closure;
7. Pi isolation and discovery contract, Antigravity deterministic discovery,
   Grok inspect contract, sensitive-category exclusions, and no credential /
   session / log / cache / model-setting copying;
8. preimage freshness at Review start/end without modifying runtime;
9. legacy drain remains zero and no active legacy evidence can authorize
   schema 6;
10. exact stop conditions: any drift, link/type mismatch, unexpected path,
    failed verification, blocked recovery, or non-PASS Review prevents apply or
    later-target progress.

Use read-only validation and temporary isolated checks only. Do not inspect
unrelated native contents; plan and preimage hashes/modes/paths are sufficient.

## Required output

Return one complete neutral Markdown Review suitable for verbatim persistence:

- assignment/independence and evidence-only authority;
- start/end binding table;
- root/closure/preimage/order/exclusion/backup/restore analysis with path:line
  mechanism and test evidence;
- fresh read-only validation results;
- findings by severity and exact resume conditions;
- final `PASS`, `FAIL`, or `BLOCKED`;
- explicit statement whether runtime apply may begin.

The intended Review artifact is
`docs/design/reviews/2026-08-20-add-role-first-review-routing-runtime-sync-plan-review.md`.
It must remain absent during Review. This reviewer must not write it.
