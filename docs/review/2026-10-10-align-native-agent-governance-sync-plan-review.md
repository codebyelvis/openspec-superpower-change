# Native Agent Governance Runtime Sync Plan Review

Author: elvis. Date: 2026-10-10. Change: `align-native-agent-governance`, approved draft-v1.

Result: **PASS** for this exact schema-v2 scoped plan and its current execution readiness. No actionable finding remains. This is a separate runtime-plan review; it does not reopen source Preflight, perform a canonical transition, validate completed installation, or grant Git/publication/native-adaptation authority.

## Assignment and exact bindings

Reviewer: product `codex`, contract-local instance `align-native-sync-review`, role `independent-reviewer`, capability `control-plane-high`, authority `governed-review-evidence`, distinct from author/executor/control-plane `align-native-root`.

Review purpose: independently decide whether the exact reviewed four-target transaction plan is ready for its already-authorized execution. The bound control plane owns evidence acceptance and transitions. The Router-governed strict Review variant applies: actual source/diff inspection, critical reruns and independent adversarial evidence were performed. No apply, commit-target, native business probe, runtime/configuration/source/Git/state mutation or delegation was performed by this reviewer. Only this change-specific review artifact was written.

| Artifact | Whole-file SHA-256 |
| --- | --- |
| Durable plan: `docs/review/2026-10-10-align-native-agent-governance-sync-plan.json` | `6b96b7fa7a8e727cfe55a79f1eace532f4960e53d6748b1b12ff736e56d64376` |
| Actual private execution plan | `6b96b7fa7a8e727cfe55a79f1eace532f4960e53d6748b1b12ff736e56d64376` |
| Source Implementation Review r2: `docs/review/2026-10-10-align-native-agent-governance-implementation-r2.md` | `ff4a8a68aa8ca5c6eb9a9da497e7ea71ac0022c17650899eef6631dbe6958930` |
| Manifest: `references/cross-cli-portable-manifest.json` | `d8389bf24b9fb3bc22bde69f1b2ba5cfee0fb6245d38ff4dcb5fe2f7649d4116` |
| Canonical managed body: `references/shared-global-governance.md` | `960db63a0053c8d4311df61ff55f1534fd117868b39101d99b5666dd7e0a1977` |

Private container, as supplied and independently inspected:
`/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/align-native-agent-governance-b763154v`.
Execution uses its `sync-plan.json`; `runtime-backups` is the backup root and `runtime-transactions` the receipt root. The macOS `/var` alias resolves to `/private/var`; the resolved roots have no symlink components. The actual plan is mode `0600`; staging and both fresh empty runtime roots are mode `0700`, non-symlink directories outside every declared skill-discovery root. The durable root copy is byte-identical path/hash-only evidence and is not the transaction staging root.

All thirteen transferred source files match their bindings in `docs/review/2026-10-10-align-native-agent-governance-source-verification.json`. The reviewer inspected the complete corrected implementation diff and actual portable mechanisms. The changed synchronization code extends only managed-governance semantic validation; it does not introduce installer, target, native-hook, settings, dependency-link, identity/schema or transaction-lifecycle changes. Existing schema-6 product/authority and legacy-history boundaries remain intact. Companion files are exclusively unselected assertions.

## Scope and destination checks

Plan schema: **2**. Manifest schema: **1**. Managed-rule version: **6**. Exactly sixteen existing CCG IDs. Required application order comes from the unchanged canonical manifest and `TARGET_ORDER`: `codex`, `pi`, `antigravity-cli`, `grok-cli`. Alphabetical JSON-object serialization does not change that execution order.

| Target | Exact skill root | Exact managed destination | Whole-file prestate SHA-256 |
| --- | --- | --- | --- |
| codex | `/Users/elvis/.codex/skills` | `/Users/elvis/.codex/AGENTS.md` | `6893724a7f95510882fc5ac616c063d1446f2c3dbe1e136e0feffa1d933a19cc` |
| pi | `/Users/elvis/.pi/agent/skills` | `/Users/elvis/.pi/agent/APPEND_SYSTEM.md` | `a6be2edf44714a802aaeeede6dd2e65cd9e3f4e542a64d57c383a2e5c38e5c5f` |
| antigravity-cli | `/Users/elvis/.gemini/antigravity-cli/skills` | `/Users/elvis/.gemini/GEMINI.md` | `7fde09daec9bc5d56754a058a32ec48f983bae0898f59453ae00ca1853982006` |
| grok-cli | `/Users/elvis/.grok/skills` | `/Users/elvis/.grok/AGENTS.md` | `5114a280dec4d4b47d66540ae872b1e55b1d21eae18439f185695d640d6f29be` |

Default Codex is explicitly bound to `.codex`; active account-A is not a target. Every selected/asserted destination equals its validated `skills_root / skill / relative-path`, with regular files and no symlink path components. Every managed destination matches the target-specific canonical derivation. The plan binds reviewed mode/hash prestates for all 160 portable destinations and four global-rule files.

Every target has these **seven** selected portable operations, all for `openspec-superpower-change`:

- `references/cross-cli-sync.md`
- `references/local-instruction-checkpoint.md`
- `references/shared-global-governance.md`
- `references/superpowers-adapter.md`
- `references/sync-checklist.md`
- `scripts/validate_core_gates.py`
- `scripts/validate_cross_cli_sync.py`

Each also has **33** unselected assertions, including all ten Companion portable files, plus the selected managed block. Selection, manifest-order normalization, source hashes and complete operation/assertion partition were independently checked. No native account, hook, settings, auth/session/model file or dependency link is a mutation operation.

The reviewer called the actual candidate-construction API in memory only. It produced exactly eight candidates per target: seven selected files plus the global rule. Every current global file is already version 6; current raw UTF-8 bytes equal the text-reader snapshot. For each computed candidate, native prefix and suffix match the actual original exactly, and the managed body passes real parity/semantic validation. No candidate was persisted or installed. Native outside bytes and existing modes remain covered by the existing transaction.

## Fresh independent verification and adversarial probe

| Check | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py verify-prestate --plan <private-container>/sync-plan.json --target all` | Exit 0; all four target prestates pass. |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .` | Exit 0; current transferred source valid. |
| Actual source/manifest/review/plan hash checks | MATCH; both plan copies equal; all thirteen reviewed source bindings match. |
| Scoped read-only regression rerun | Eight tests, exit 0, no failures/errors/skips: all `NativeConsumptionManagedRulesTests`, all `ScopedPlanTamperTests`, and `ScopedPlanSelectionTests.test_generation_rejects_noncanonical_managed_rule_destination`. These tests do not execute apply or commit-target. |
| Isolated/in-memory actual-plan mutations | Unknown fifth target; native-hook selector; changed selected source hash; missing assertion; assertion moved into mutation set; managed deselection; product substitution; unsupported schema: each rejected by the real plan validator. |
| Coherent managed destination/prestate retarget | A new harmless isolated file with its correct prestate was still rejected as a managed destination. No runtime file was changed. |
| Ordered-target counterexample | A later target without an earlier verified same-plan receipt was rejected by the real prior-target guard. |
| Reviewer probe non-mutation audit | All 164 actual runtime file fingerprints remained unchanged after the probes. |
| Known project lifecycle inventory | The two current `docs/agent-collab/*/status.md` files are schema 6 and `complete`; no active schema-4/schema-5 status was found in that project inventory. |

The reviewer read current CLI help for `apply`, `verify`, `verify-discovery`, `commit-target`, `verify-all`, and `verify-prestate`, and inspected the actual receipt, backup, destination, discovery and recovery paths. Critical evidence uses the real current validator, not a text-only or mock acceptance claim.

## Execution and recovery boundaries retained

The exact current command interface requires sequential per-target `apply --plan ... --target ... --backup-root ... --transaction-receipt ...`, receipt-bound `verify`, target quick/core/unchanged Companion template validation, `verify-discovery`, then `commit-target`. Receipts use canonical names `codex.json`, `pi.json`, `antigravity-cli.json`, `grok-cli.json` beneath the private transaction root. `commit-target` is a sync-receipt operation and grants no Git authority.

The reviewer also inspected the private `run-reviewed-sync-target.py` orchestration supplied before handback. It binds the exact plan hash and root evidence copy, resolves its private container, invokes the existing CLI sequence above, runs both target core parser modes, keeps Grok inspect output private, uses canonical receipts and stops with current-target restore on check failure. It introduces no distributed installer or native configuration mutation. The installer retains the actual order/receipt/prestate barriers; the wrapper's PASS-text check does not replace this independent review or control-plane evidence acceptance.

The real implementation verifies full target prestates before backups, persists prepared/mutation-intent/applied-uncommitted receipt state around writes, creates private mode-`0600` backups/manifests/receipts and mode-`0700` directories, and requires verified earlier same-plan receipts before later targets. Unselected assertions are never candidates or backups. Content/discovery/commit/verify-all check the complete portable closure, not only selected files.

Grok discovery remains required after its installation. Private `grok inspect --json` output must be supplied to `verify-discovery --inspect-json ... --consume` without printing raw contents. User discovery must match the planned Grok root; configured discovery must uniquely map to an earlier same-plan verified target with fresh full-closure parity and receipt/content digest binding. Neither discovery path reads or modifies Grok configuration. Codex/Pi/Antigravity use deterministic closure; no Pi native process is required.

Immediately before first apply, repeat known active-legacy inventory and relevant prestates. Any source/hash/prestate drift, failed required verification, unresolved finding or protected-boundary change blocks the affected phase. An apply/verification/discovery failure requires current-target restore/recovery with verified reviewed preimage and stops later targets; recovery-blocked evidence and backups remain available for disposition. Final source/runtime verification and separate Final Review follow installation and remain pending.

## Completeness and accepted residual risks

All reasonably discoverable findings from this plan, current source, runtime prestates and supplied evidence were consolidated. `blocking_findings: []`; `non_blocking_recommendations: []`; `finding_completeness: true`.

- **Runtime acceptance is pending.** This readiness PASS does not assert installation, Grok discovery or final verification has succeeded. Owner: `align-native-root`; decision: execute existing sequential verification/recovery and final gates.
- **Qualification stays bounded.** Four-target portable parity cannot qualify account-A, other linked consumers, native Skill-body loading, seven actual entries or Grok hook enforcement. Owner: `align-native-root`; decision: preserve the separate exact-path native-adaptation plan and its pending acceptance.
- **Prestate is temporal.** The reviewed prestates are current observations; apply must reject subsequent drift. Owner: `align-native-root`; decision: preserve the existing immediate prestate checks and stop/recovery contract.

The user-approved source/sync scope remains unchanged. This review grants no additional authority and requires no waiting for the later post-sync Full Final gate before returning its bounded readiness result.
