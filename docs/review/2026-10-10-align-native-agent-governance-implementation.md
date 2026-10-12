# Native Agent Governance Implementation Review

Author: elvis. Date: 2026-10-10. Change: `align-native-agent-governance`, approved draft-v1.

Result: **FAIL**. Five actionable findings below prevent source transfer and runtime synchronization. This is source Implementation Review evidence only; it does not replace Final Review or authorize canonical transitions. Corrections remain at this Implementation Review stage under the unchanged approved scope and Preflight.

## Assignment and reviewed revision

- Purpose: independently determine whether the source implementation may proceed to guarded source transfer and runtime-sync planning.
- Product: `codex`; instance: `align-native-implementation`; role: `independent-reviewer`; capability profile: `control-plane-high`; authority: `governed-review-evidence`.
- Author/executor/control-plane instance: `align-native-root`. Reviewer is a distinct Codex instance and did not edit implementation, runtime, Git state or canonical task state, or dispatch further agents.
- Method: the selected Router-governed variant of `executing-plans`, including actual-file and complete-diff inspection, independent critical reruns and adversarial probes. The ordinary code-review template does not override these gates.
- Plan: `docs/superpowers/plans/2026-10-10-align-native-agent-governance.md`; whole-file SHA-256 `8ec9d76241b3d25b1ce89e54bb0f094ac71dfe3a7c8d2ec0d71b94d18c8e5219`.
- Preflight: `docs/review/2026-10-10-align-native-agent-governance-preflight.md`; SHA-256 `deed722c70c015ec4a38bef425d5cb62a2d922a9b61bb4d736406f2561edaadd`; inspected PASS is readiness evidence, not implementation acceptance.
- Complete implementation diff: private review-package `implementation.diff`; SHA-256 `1b847efe5226543f4236dafcd6f35ffb114994258105c60d40970f19b02d5320`.
- All proposal/design/spec/task hashes match the approved `openspec/changes/align-native-agent-governance/validation.md`. The reviewed implementation was the isolated working copy, before any transfer to the original source.

Reviewed source SHA-256 bindings, independently checked against actual files:

```json
{
  "references/shared-global-governance.md": "960db63a0053c8d4311df61ff55f1534fd117868b39101d99b5666dd7e0a1977",
  "references/local-instruction-checkpoint.md": "11e9c8db28264eb638f44198d222885df4ecf6a01c532deddd4119b27b845132",
  "references/superpowers-adapter.md": "851cbff37e5407c8c0c5c2872baa07b398f0d097aabcbe50eb29cb4c5b8b734f",
  "references/cross-cli-sync.md": "f52a9d7a3caabc265c8a2b059179096f86567a75d6e704543fd5e14b8b9dc4ec",
  "references/sync-checklist.md": "366f272094a2c24d8840c94159483636624b24cd1629219f7114959848905028",
  "scripts/validate_core_gates.py": "4c8505718aee4ac5f1de093d69b9fc9fba0f1826035049da75a61795d5a80b63",
  "scripts/validate_cross_cli_sync.py": "4d9ff254ea91944f7bad797c9d16097817d8e01ec723f13d4b065d2c5d94df1c",
  "tests/test_workflow_rules.py": "f55f57cca1702a085cdce7f229386eeea870b94949014e1f046dd95165d8446a",
  "tests/test_cross_cli_sync.py": "e3171ea1a59a5627dac92e489794b8040ed4060a42204f0d4052d4d65c42e3d8",
  "docs/engineering-invariants.md": "d66acd645c8c222c235c02be09f06234ec6927d360f439ced67c716e1a287ab8",
  "CHANGELOG.md": "9e1f1a594033ae42542c3e74bff4ee06723907f05532167d9d4fdf513ce1739b",
  "tests/fixtures/native-agent-governance-cases.json": "8d3c0c2d42e70e75125e5c95e9a14a6f395879202ba32f79ce8a95cdd16bb4b7",
  "tests/run_native_agent_governance_forward_tests.py": "0a9e3a252dc538569a5e454b40ff8ff270454d547e942b58ad611eb365429a01"
}
```

## Positive findings and scope

The source prose matches the approved compact-local and advisory boundaries. CCG-004 and CCG-014 compare complete owned paragraphs, so the tested appended compact-external waiver fails. CCG-001/002/010/016, `SKILL.md` and the portable manifest retain their prestate bytes. Four targets, sixteen IDs, managed version 6 and the schema/product boundary remain unchanged; no native hook/configuration or Companion implementation change is present in the reviewed diff.

All thirteen implementation files are proposal-listed. The work-copy/prestate comparison additionally found the permitted approval, plan and baseline records, plus generated Python bytecode outside the implementation package. The original source's thirteen implementation paths still match their prestates or expected absence. No historical source fixture was rewritten outside the two approved test files; legacy schema protection remains covered by existing checks.

The runner retains finite classifier fields, memory-only raw stdout/stderr, private per-case directories, read-only execution, event auditing and explicit `native_skill_loading: not-tested` scope. Its current defects below do not justify upgrading that bounded evidence to native Skill-body loading or seven-entry acceptance.

## Actionable findings

### F1 — Important: accepted temporary-root names cannot be cleaned

Location: `tests/run_native_agent_governance_forward_tests.py:155` and `:182`.

The new CLI accepts any absent `--temporary-root`, creates it, then calls the existing `validated_remove_run_root` helper. That helper requires a basename beginning with `routing-forward-`. The actual `native-green-run` root does not satisfy this contract. An independent temporary-directory probe returned `refusing cleanup of an unowned run-root` and retained the directory. The exception escapes `finally`, skips handler restoration and can turn a printed PASS into a nonzero process exit after native work has already run.

Correction: align root creation/validation with the cleanup ownership contract before launching cases, restore handlers even when cleanup fails, and publish success only after required cleanup succeeds. Add a CLI-level regression for an otherwise-valid caller-selected temporary-root name and for cleanup failure; do not weaken the existing helper's ownership checks.

### F2 — Important: several approved owner obligations are not enforced

Location: `scripts/validate_core_gates.py:2219`; `tests/test_workflow_rules.py:78`.

The checkpoint validator checks selected substrings but omits meaningful approved safeguards. Independent mutations of the real checkpoint all passed `validate_native_agent_consumption`:

| Mutation | Actual result |
| --- | --- |
| Replace the user's authorized scope/project conventions/existing contract destination sentence with a native-default-only destination | ACCEPTED |
| Replace the publisher path/format incompatibility instruction to report conflict with silent use of the native default | ACCEPTED |
| Change `backends do not change product identity` to `backends may change product identity` | ACCEPTED |

These are the exact path, publisher and real-launcher failure mechanisms covered by the approved design. The plan also requires negative checks for each new safety obligation, while the new deletion test covers only six selected clauses. Current good prose therefore lacks the promised regression protection.

Correction: bind the complete approved obligations in their owned checkpoint section, including destination precedence, publisher applicability/compatibility, real product identity and selective-hook protection. Exercise each obligation through the real validator, retaining moved/hidden-text negatives. No source or runtime policy expansion is needed.

### F3 — Important: direct sync validation accepts comment-hidden or fenced governance

Location: `scripts/validate_cross_cli_sync.py:438`.

Wrapping the actual complete governance source in `<!-- ... -->` or a fenced `text` block still passes `validate_managed_rule_semantics(..., version=6)`. The reviewer also passed each mutated body through the real `install_managed_block` and `validate_managed_rule_parity` APIs with all sixteen invariant IDs: both were ACCEPTED. The raw regex recognizes CCG bullet lines without checking whether they are active Markdown instructions.

The new core-gate wrapper correctly rejects those same mutations after applying visible-content parsing, but the direct synchronization validation path does not share that guarantee. Thus a hidden managed body can be installed and receive parity/semantic PASS from the sync API even though the new consumption contract is absent as active instructions.

Correction: make the actual managed-semantics/parity owner reject hidden and fenced source bodies, preserving existing exact CCG bodies and historical-version behavior. Add negative regressions through the real synchronization API, not just the core wrapper.

### F4 — Important: required seven-case native proof has four failures

Location: `tests/fixtures/native-agent-governance-cases.json`; `tests/run_native_agent_governance_forward_tests.py:72` and `:116`.

The completed private `native-green-summary.json` has SHA-256 `6b4dc31eb622b572df8dd0ed57245f7ac6533164c29a0004d2447bc9ebc59994`. It contains seven cases, only three PASS, and these four mismatches:

| Case | Expected field | Observed field |
| --- | --- | --- |
| `compact_local` | `action: implementation-gated` | `action: answer` |
| `unapproved_major` | `action: proposal-only` | `action: blocked` |
| `bound_plan` | `action: implementation-gated` | `action: classify-persistence` |
| `claude_identity` | `authority: none` | `authority: advisory-input` |

Each case has four native events, one agent message and zero tool events. The desired inline readiness, before-execution bound plan, refusal of unapproved implementation and real Claude product identity appear in the corresponding finite outputs. These mismatches do not independently prove a governance violation: the schema exposes enum labels without defining whether `action` classifies the simulated work or the current classification request, and whether `authority` means the rejected formal assignment or permitted advisory capacity.

Correction: define classifier semantics independently of expected answers, resolve fixture expectations against the approved behavior, then rerun all seven actual native cases. Do not copy expected classifications into model input, reinterpret this run as PASS, or invent a reproduced native-rule failure. Owner: `align-native-root`; resume condition: fresh seven-case match with valid event audits and a successful runner lifecycle.

### F5 — Important: source/fixture hashes can describe bytes never consumed

Location: `tests/run_native_agent_governance_forward_tests.py:63` and `:141`, `:173`.

The runner reads source text for the AGENTS projection and separately reopens the path to hash it. It similarly reads fixture inputs/expectations at suite start but hashes the fixture after the native runs. A concurrent replacement can therefore bind an old projection or old expectations to new file hashes.

An independent isolated adversarial probe invoked the actual `run_case`, replaced a temporary source immediately before its hash read, and intercepted process creation before any native launch. The generated AGENTS contained the original bytes while the recorded source digest matched the replacement bytes. No native answer was mocked or claimed by this probe; it demonstrates the preparation-stage hash-binding defect.

Correction: read each source/fixture once as bytes; hash, decode/parse and project those same bytes. Bind the generated instruction/input hashes as needed to the exact observed run, and add deterministic replacement regressions. This is the approved hash-bound proof requirement, not permission to expand native entry scope.

## Independent verification

Executed on the bound isolated source with `PYTHONDONTWRITEBYTECODE=1`:

| Evidence | Result |
| --- | --- |
| `python3 scripts/validate_core_gates.py .` | PASS, exit 0 |
| Focused unittest command below | PASS, 32 tests, no failures or skips |
| Actual source SHA-256, approved contract hashes, plan/preflight bindings | MATCH |
| Original-source implementation prestate/absence guards | MATCH; transfer has not occurred |
| F1 cleanup ownership probe | Reproduced failure |
| F2 real-validator checkpoint mutations | Reproduced three incorrect ACCEPTED results |
| F3 actual managed install/parity mutations | Reproduced hidden/fenced ACCEPTED results; core wrapper rejects both |
| F5 actual pre-launch preparation with an isolated replacement seam | Reproduced mismatched consumed/hashed bytes |

Focused unittest invocation:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys, unittest
sys.path.insert(0, 'tests')
names = [
    'test_workflow_rules.NativeAgentConsumptionTests',
    'test_cross_cli_sync.NativeConsumptionManagedRulesTests',
    'test_cross_cli_sync.ScopedPlanSelectionTests',
    'test_cross_cli_sync.ScopedPlanTamperTests',
    'test_cross_cli_sync.ScopedTransactionTests',
    'test_workflow_rules.WorkflowRulesTest.test_schema6_reviewer_assignment_exact_shape_fails_closed',
    'test_workflow_rules.WorkflowRulesTest.test_schema6_standard_strict_and_compact_profiles_are_exact',
    'test_workflow_rules.WorkflowRulesTest.test_tiered_08_same_product_instances_cannot_self_review',
    'test_cross_cli_sync.DurableTargetTransactionTests.test_four_target_order_and_verify_all_require_verified_pi',
]
result = unittest.TextTestRunner(verbosity=1).run(
    unittest.defaultTestLoader.loadTestsFromNames(names)
)
raise SystemExit(not result.wasSuccessful())
PY
```

The executor's two fresh suite logs were inspected: 487 tests PASS in dependency-free mode and 487 PASS in the isolated PyYAML mode. Those full runs are executor evidence, not a second independent full-suite execution. Reported quick validation, Companion validation and strict OpenSpec validation do not cure the reproduced findings. The native summary was independently inspected rather than independently regenerated by this reviewer.

Both pre-change native baselines remain `baseline-complies`. The observed RED for universal CCG-004, absent advisory exception and appended compact-external waiver is deterministic validator evidence. It must not be described as a reproduced native model failure.

## Evidence bounds and disposition

Finding completeness: all reasonably discoverable findings from the supplied contract, actual reviewed files, complete diff and current evidence are consolidated above. No actionable finding is downgraded to a recommendation. No separate non-blocking recommendation is proposed.

Declined to judge: actual native Skill-body loading, seven actual entry acceptance and native hook enforcement, because they are explicitly outside this slice and the supplied project-AGENTS probe cannot establish them. Runtime-sync plan destinations and apply/recovery results remain later separate gates; none exists as reviewed implementation acceptance here.

Existing accepted residual risk remains owned by `align-native-root`: four-target portable parity cannot qualify alternate accounts or consumers, and Grok publisher compatibility needs its own supported adaptation evidence. No product, schema, target, hook or authority expansion is authorized by this Review.

Return F1–F5 to the author for same-scope correction, relevant fresh verification and independent Implementation Review. Preserve unchanged Plan/Preflight and all source prestates/backups needed for recovery. Raw native traces/configuration/authentication were neither copied nor exposed in this artifact. Source transfer, runtime planning/apply acceptance, Final Review and whole-task completion remain unapproved by this result.
