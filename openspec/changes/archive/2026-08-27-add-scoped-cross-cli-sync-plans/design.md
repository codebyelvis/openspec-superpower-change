# Design: add-scoped-cross-cli-sync-plans

## Context

The existing `scripts/validate_cross_cli_sync.py plan` validates one path-free
portable manifest, captures source hashes and destination prestate, and emits
all declared files plus the managed global rule for all four runtimes. Its
receipt-bound apply path already supplies ordered targets, secure backups,
atomic installation, rollback, recovery, content verification, discovery, and
commit evidence.

The predecessor permits exactly these runtime mutations per target:

```text
openspec-superpower-change/SKILL.md
openspec-superpower-change/references/approved-implementation-workflow.md
```

The audited full plan instead contains 29 Router files, 10 Companion files, and
one global-rule candidate per target. Expanding the predecessor is forbidden.

## Minimal Implementation Judgment

```text
Need: exact reviewed mutation closure
-> Repository Reuse: existing planner + durable transaction machinery (chosen)
-> Stdlib: argparse/json/path/hash helpers already present
-> Platform Native: existing fsync/rename/receipt primitives already present
-> Existing Dependency: none needed
-> Small Local Implementation: scoped schema/partition helpers
-> New Abstraction: rejected
```

A temporary-manifest workaround is rejected because the current plan still
rewrites the managed rule. A manual copy wrapper is rejected because it bypasses
durable receipts and recovery. A second permanent sync tool is rejected because
it duplicates security-critical machinery.

## Decisions

### 1. Explicit selectors; no Git inference

Scoped mode is selected only when one or more of these options is present:

```text
--select-file openspec-superpower-change:SKILL.md
--select-file openspec-superpower-change:references/approved-implementation-workflow.md
--select-managed-rule
```

`--select-file` is repeatable. Split once on `:`; skill names are path-free and
portable paths already reject colon-bearing URL/drive syntax. Reject duplicates,
unknown skill/path pairs, sensitive/unsafe paths, and entries that do not target
all four schema-6 runtimes. Scoped mode requires at least one operation.

No selector preserves the legacy full-manifest plan path exactly. Do not infer
selection from repository dirt, timestamps, source/runtime differences, or a
chat instruction.

### 2. Scoped plan schema v2

Legacy full plans remain schema version 1 and retain their current shape.
Scoped plans use sync-plan schema version 2. The portable manifest remains
`schema_version: 1`; “schema-6 eligible” means
`managed_rules.version == 6`, target IDs exactly
`codex, pi, antigravity-cli, grok-cli` in that order, and every selected file's
`targets` exactly that order.

The v2 top-level key set is exactly:

```text
schema_version, manifest_path, manifest_sha256, sources, selection,
managed_rules, targets
```

`manifest_path`, `manifest_sha256`, `sources`, and top-level `managed_rules`
retain their v1 shapes. `selection` is exactly:

```json
{
  "files": [
    {"skill": "openspec-superpower-change", "path": "SKILL.md"}
  ],
  "managed_rule": false
}
```

Every selected file object has exactly `skill,path`. Selection is normalized in
manifest order. Each v2 target contains its exact manifest target-state fields
plus exactly `skills_root,files,assertions,managed_rule`; it omits v1
`rule_file` and `rule_pre_state`. Every `files` and `assertions` record has
exactly the v1 file-record keys:

```text
skill, source_alias, path, sha256, destination, pre_state
```

`managed_rule` has exactly:

```text
selected, destination, pre_state
```

Its canonical version/source/path/SHA/invariant IDs remain only in top-level
`managed_rules`. `files` contains selected file operations only;
`assertions` contains every unselected manifest file. `files + assertions` must
partition the complete manifest exactly once; each list preserves relative
manifest order. The selected set must equal top-level `selection` for every
target. `managed_rule.selected` must equal top-level
`selection.managed_rule`.

The full plan hash binds selection, source hashes, all target prestates, and the
operation/assertion partition into every receipt. Moving an item between
`files` and `assertions`, selecting the rule, changing a path, or expanding a
closure invalidates the reviewed plan hash or plan validation.

### 3. Assertions prove parity but never become candidates

At plan generation, every unselected destination and the unselected managed
rule must already match canonical source/parity. Otherwise planning is
`BLOCKED`; scoped mode cannot conceal unrelated stale runtime state.

At apply, prestate is rechecked for selected files, assertions, and the managed
rule before backup creation. Backup manifests and candidate lists contain only
selected files and the managed rule only when `selected=true`.

After apply, content verification, discovery, target digest, commit, and
verify-all cover selected plus asserted files and the managed rule. Concurrent
drift in an assertion blocks verification; rollback restores only objects the
transaction selected and mutated.

### 4. Compatibility helpers, not parallel flows

Add small internal helpers that normalize v1/v2 access:

- selected operation records: v1 `target.files`, v2 `target.files`;
- complete verification records: v1 `target.files`, v2 deterministic
  `target.files + target.assertions`;
- managed-rule operation: always selected through v1 `rule_file/rule_pre_state`,
  conditional through v2 `target.managed_rule`;
- target prestate closure: all verification records plus the rule binding.

Thread only these helpers through `_target_candidate_entries`,
`_target_records`, `_assert_target_prestate`,
`_legacy_apply_target_without_receipt`, `verify_target`, and
`_current_target_digest`. `_validate_plan` dispatches exact v1 validation or
exact v2 validation. Backup/restore/recovery continue to consume only candidate
entries, so assertions cannot enter their manifests.

Reuse the existing apply, receipt, backup, restore, recovery, discovery, and
ordered-target functions. Do not fork a second transaction lifecycle. Existing
v1 no-selector round trips and recovery tests must remain green.

### 5. Bootstrap without canonical source overlap

Changing the canonical sync script before resolving the predecessor would make
the tool itself another unsynchronized portable file. Avoid that cycle:

1. Copy the four implementation preimages into a private isolated candidate
   tree outside every discovery root and outside Git worktrees.
2. Keep an immutable full-tree baseline beside the candidate. Read-only inventory
   existing generated caches, exclude them from both copies, and never delete
   them. Reject symlinks and any candidate delta outside the exact four allowed
   files. Persist mode-`0600` inventories and RED/GREEN/full/Review hashes.
3. After fresh candidate Source and Sync-plan Reviews, the bound control plane
   writes an exclusive canonical OpenSpec launch-authorization artifact and
   records its SHA in active `tasks.md`. It binds Plan, Reviews, bundle, script,
   resolved isolated interpreter, selected plan, and operation set. Before every
   candidate invocation, a Plan-defined guard validates that trusted external
   anchor and the complete candidate inventory, then executes the candidate via
   the hash-bound real interpreter with `-I -S`.
4. Generate a v2 plan selecting only the predecessor's two approved files.
   Full assertions use unchanged canonical source and must pass. Obtain fresh
   assigned Codex/Sol Sync-plan Review; apply one target at a time through
   existing durable receipts; verify and Review all four; then close and archive
   the predecessor under its existing contract.
5. Only then copy the exact reviewed candidate changes into canonical source
   after fresh backup/prestate checks. Re-run all validation and Source High
   Review.
6. Use the canonical scoped tool to synchronize exactly this change's three
   portable files: the script and two references. Tests and contract artifacts
   remain repository-only.

The isolated candidate is bootstrap evidence, not canonical state or a second
ledger. Active OpenSpec `tasks.md` files remain the only progress ledgers.

### 6. Agent and authority split

Execution is direct inline work in a fresh Pi session switched to Luna Max. It
resumes the approved active OpenSpec `tasks.md`; it is not an external-agent
batch and creates no Handoff, Brief, Report, Confirmation Lease, or second
ledger. If the user instead requests external dispatch/new-window Handoff, stop
and create a separate schema-6 contract/Plan before execution.

Implementation executor:

- product: Pi;
- model: `openai-codex/gpt-5.6-luna` with reasoning level exactly `max`;
- role: `executor`;
- capability profile: `cohesive-medium`;
- instance: fresh inline instance distinct from author/reviewers;
- authority: scoped file/test/runtime execution only after approval; no evidence
  acceptance, Git, archive, or canonical completion authority.

Each checkpoint Review has a new explicit assignment:

- purpose: candidate Source, Batch-A Sync-plan/runtime, canonical Source,
  Batch-B Sync-plan/runtime, or final closeout as named by the Plan;
- product/model: Codex / `openai-codex/gpt-5.6-sol` at exactly `max`;
- role/profile: `independent-reviewer` / `control-plane-high`;
- instance: fresh and distinct from Luna, author, control plane, and every prior
  reviewer;
- result authority: governed evidence only.

Only the bound Codex control-plane/control-plane-high instance accepts evidence,
updates canonical task/evidence anchors, authorizes runtime apply/archive, and
decides Completion.

## Validation

### RED/GREEN

- Selected two-file plan contains exactly two `files` operations per target,
  every other manifest file in `assertions`, and `managed_rule.selected=false`.
- Duplicate, unknown, unsafe, sensitive, non-v6, target-incomplete, and empty
  scoped selections fail before output creation.
- Selection/partition/rule tampering fails `_validate_plan` and every downstream
  command.
- Selected destination prestate drift blocks before backup/receipt.
- Unselected destination or managed-rule drift blocks planning or apply and is
  never rewritten.
- Scoped apply/verify/discovery/commit/verify-all mutates only selected bytes;
  unselected files and native global-rule bytes remain byte-identical.
- Scoped failure/restore/recover touches only selected transaction entries and
  blocks later targets.
- Legacy no-selector full plan round trip and existing crash/recovery tests stay
  green.

### Project evidence

- Focused scoped-sync tests, full `tests/test_cross_cli_sync.py`, full unittest,
  `quick_validate.py`, dual-interpreter core gates, strict OpenSpec, and
  `git diff --check`.
- Independent adversarial Source High Review inspects actual candidate/canonical
  files and tests operation-vs-assertion tampering.
- Separate Sync-plan Review checks exact target operation sets, source hashes,
  prestates, no rule operation, private roots, legacy-contract drain, and
  ordered rollback before either runtime batch.
- Runtime verification covers parity, validators, deterministic discovery,
  Grok inspect, receipts, and final all-target Review.

## Rollback

Candidate-tree failure deletes nothing automatically; retain the private tree
and backup for control-plane disposition. Runtime failure restores only the
current target through its verified receipt/backup and blocks later targets.
Canonical implementation rollback restores only the four declared source
preimages from a fresh structured backup. Never reset/clean Git, modify native
rule bytes outside the managed block, or delete evidence/backups before Review
and rollback needs resolve.
