# Runtime Sync-plan High Re-review — P1 R5

- Reviewer: fresh no-history Codex, independent-reviewer, control-plane-high
- Scope: read-only evidence review；未修改 project/runtime、Git、Pi 或 Review artifact
- Intended Review artifact: absent

## Bindings

Required input:

- mode `0644`
- SHA-256 `213d8166583978c17d87136953385e0756e46d176b0204c326590fad086494c1`

Bound source/design/validation inputs all matched their recorded modes and SHA-256 values, including source Review, prior runtime FAIL, approved Plan, OpenSpec design/spec/tasks, portable manifest, corrected validator, and corrected tests.

New plan:

- Path: `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/runtime-sync-plan-r5.json`
- mode `0600`
- SHA-256 `6ae0cc4dcca9fbc8de9d1e4c1fc050d0fcc4dc7bde445a6bda85bb6845a51156`
- schema validation: pass
- targets: `codex`, `pi`, `antigravity-cli`, `grok-cli`

Start/end checks:

- `verify-prestate --target all`: pass at start and end
- structured private root: mode `0700`, non-symlink
- R5 backup root: absent at start/end
- R5 transaction root: absent at start/end
- legacy root names: absent
- intended Review artifact: absent

## Plan and closure

- Four targets contain 39 portable records plus one managed-rule preimage each.
- 160 destination paths are unique.
- All destination preimages are regular files with matching type/mode/content hashes.
- Source and destination containment, closure, symlink/type boundaries, and managed-v6 manifest semantics validated.
- No serialized sensitive/native-body fields were found.
- `/Users/elvis/.agents/skills/{openspec-superpower-change,codex-brief-antigravity-review}` symlinks remain preserved and outside the exact destination closure.
- Legacy drain is empty: `active_legacy_count=0`, `records=[]`.

Execution order is independently established as:

`codex → pi → antigravity-cli → grok-cli`

The validator’s `TARGET_ORDER`, manifest validation, prior-target receipt gating, and `verify_all_receipts` all enforce this order. Later targets cannot start before earlier targets are verified.

## Private-root adversarial review

The corrected shared guard resolves candidate roots and rejects equality or nesting under every discovery root before directory creation or lock/receipt/backup side effects.

Verified call paths include:

- public apply, restore, recovery
- direct `_prepare_target_backup`
- direct `_target_transaction_lock`
- receipt verification, discovery verification, commit, and verify-all
- recovery/orphaned-backup paths

Temporary isolated probes covered:

- equality
- nested path
- other-target discovery root
- normalized path
- existing symlink ancestor

All 76 probes rejected before side effects; target closures remained unchanged. Reviewed R5 backup and transaction roots were accepted as outside every discovery root and remained absent.

Relevant implementation locations include `_assert_runtime_root_outside_discovery`, `_target_transaction_lock`, `_prepare_target_backup`, `apply_target`, `restore_target`, and `recover_pending`.

## Lifecycle and isolation

- Backup objects/manifests use exclusive creation, no-follow behavior, mode `0600`, hashing, and fsync.
- Receipts are durable before mutation and bind plan, preimage, candidate, backup, and transaction identities.
- Restore handles drift, unknown state, created-parent identity, manual disposition, and recovery blocking.
- Crash-point, receipt durability, restore, recovery, ordering, and four-target tests passed.
- Pi was not invoked. Pi handling was limited to pure probe/fixture validation; native target verification does not call Pi.
- Discovery and sensitive-exclusion checks passed, including Grok inspect constraints.
- Cross-CLI test result: 91 tests passed.
- Core gate validator passed.

## Scope note

A read-only audit was invoked once with the Companion runtime directory as `--brief-source`; it returned zero sensitive categories, created no files, and did not invoke Pi. The directory is a bound target discovery root; its output was not used as acceptance authority. No further unrelated runtime destination inspection was performed.

## Findings

- P0: none
- P1: none
- P2: none

The plan JSON does not itself serialize backup/transaction-root fields. The R5 input binding therefore remains an execution precondition: apply must use exactly the reviewed R5 plan path/SHA and exact R5 root names. Any substituted root or plan invalidates this review and must stop.

## Verdict

**PASS**

Runtime apply may begin only after the original control plane accepts this Review and uses the exact R5 plan and private-root bindings above.
