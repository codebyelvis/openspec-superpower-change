# Runtime Sync-plan High Review — FAIL

## Assignment and authority

- Product: `codex`
- Role: `independent-reviewer`
- Profile: `control-plane-high`
- Reviewer: fresh no-history `gpt-5.6-luna`, distinct from authors, plan generator, executor, prior reviewers, and decision owner
- Purpose: determine whether runtime apply may begin
- Authority: sync-plan Review evidence only; this Review does not authorize apply or canonical state

The complete private plan (89,076 bytes), approved Plan, OpenSpec artifacts, Router/Companion Skills, sync references, source Review, manifest, validator, tests, and legacy-drain records were read read-only. No Git, Pi, source/runtime mutation, or Review-artifact write occurred.

## Start/end bindings

All bindings remained unchanged at both boundaries.

| Input | Mode | SHA-256 |
|---|---:|---|
| review input | `0644` | `f262cb550bfd0086ac4db07c85b74f1bcf5560f462ca9e8ff7bdca5de5e9f023` |
| accepted source Review | `0644` | `579c4486fadd8574af24ae112e81519b87d266cdecb0621c30b7c176ec0dce70` |
| approved Plan | `0644` | `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| OpenSpec design | `0644` | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| OpenSpec spec | `0644` | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| tasks | `0644` | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| portable manifest | `0644` | `3c24865244034bdb6815c321db4ceaa69c903a6e6f4cb4e7154cd88f01ed7a8d` |
| sync validator | `0644` | `8d8a18a4c6d9a7639fe963e08c1a799b0c5a531129fd6195c8cd9fd8c4315f1e` |
| private legacy drain | `0600` | `cc1355940bbcaabff01bc242d8dcee62998f9570ca26421b192cdfd6c3a77983` |
| legacy summary | `0644` | `c3dd76b95090459c64251c0797c2842b449693b3241313907a7e5d937638202c` |
| private runtime plan | `0600` | `63cb8288b704cd50e4c5bfa9318984fd958fa554c0e4e4c534e8c5cce3b3ed5d` |

## Plan/root/closure/preimage/order review

- Source roots are exactly the bound Router and Companion roots.
- Each target has 39 portable entries plus one managed-rule entry.
- All 40 entries per target are bound regular-file preimages; end-boundary `verify-prestate --target all` passed.
- Plan schema and nested keys match the declared path/hash/status-only shape; no content/native body field exists.
- Manifest SHA, managed version `6`, IDs `CCG-001`–`CCG-016`, and managed body SHA `0040153a954ab0a6599e3eb951e8fa6b7715710745616f1f404904bf056c11d2` match.
- Source path/hash validation, containment, type checks, qualified-source uniqueness, destination uniqueness, and sensitive-category exclusions passed.
- `/Users/elvis/.agents/skills` symlinks are outside the exact destination closure and remain untouched.
- Exact order is proven by `TARGET_ORDER` (`scripts/validate_cross_cli_sync.py:27-30`), manifest-order validation (`:176-201`, `:459-461`), prior-target receipt gating (`:1777-1789`), and tests (`tests/test_cross_cli_sync.py:1525-1564`), despite no serialized `target_order` field.

## Discovery and recovery review

- Pi probe construction binds temporary `HOME`/`PI_CODING_AGENT_DIR`, disables sessions/context/Skills, restricts tools, denies network/native-root access (`scripts/validate_cross_cli_sync.py:3132-3235`); native target validation does not invoke Pi.
- Antigravity deterministic closure and Grok inspect-path validation are implemented at `:2380-2405` and `:2356-2377`; receipt-bound discovery is at `:2454-2511`.
- Exclusive mode-0600 backup objects/manifests, fsync ordering, receipt transitions, atomic restore, recovery-blocked/manual disposition, and later-target stop conditions are implemented at `:1204-1223`, `:1348-1589`, `:1680-1735`, `:1834-1912`, and `:2216-2285`.
- Legacy drain is zero and schema-4/schema-5 history is non-authorizing; corresponding tests pass (`tests/test_workflow_rules.py:2386-2435`).

## Findings

### Major / P1 — discovery-root containment is not enforced for runtime backup and transaction roots

The governing sync contract requires backups and receipts to remain outside every Skill discovery root (`references/cross-cli-sync.md:64-69`).

However:

- `apply_target` accepts caller-supplied `backup_root` and receipt paths (`scripts/validate_cross_cli_sync.py:1834-1857`).
- `_prepare_target_backup` only checks mode-0700/private-directory properties (`:1680-1695`); it does not reject a backup root inside any target `skills_root`.
- `_target_transaction_lock` only checks mode-0700 root and mode-0600 lock (`:1253-1267`); it does not reject a transaction root inside a discovery root.

A temporary isolated fixture reproduced both violations: a mode-0700 backup root inside `skills_root` was accepted, and a mode-0700 transaction root inside `skills_root` was accepted. No real runtime was modified.

This is not covered by the existing `create_secure_backup` tests (`tests/test_cross_cli_sync.py:753-771`), which exercise a different helper.

Required resume condition:

1. Add a mechanical guard, or bind and validate exact runtime roots, rejecting backup and transaction roots resolved inside every declared discovery root before any backup, receipt, or destination mutation.
2. Add isolated regression tests proving in-discovery roots fail before mutation.
3. Refresh the source evidence, regenerate the runtime plan, and obtain a new independent Sync-plan Review.

## Fresh validation

- Router quick validator: PASS
- Router core gates: PASS
- Router unittest suite: 213 tests, PASS
- Companion quick validator: PASS
- Companion template validator: PASS
- Companion unittest suite: 87 tests, PASS
- Actual-plan prestate verification: PASS at start and end
- Temporary closure/order/transaction/restore checks: PASS
- Temporary Pi isolation contract construction: PASS; Pi executable not invoked
- Legacy active count: `0`
- Runtime backup root, transaction root, Grok artifact, and intended Review artifact: absent at end

## Final decision

`FAIL`

Runtime apply may not begin.
