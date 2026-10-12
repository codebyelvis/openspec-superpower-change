# Native Agent Governance Implementation Review — Revision 2

Author: elvis. Date: 2026-10-10. Change: `align-native-agent-governance`, approved draft-v1.

Result: **PASS** for the corrected source implementation. F1–F5 from the first Implementation Review are closed by the evidence below. This result supports guarded source transfer and generation of the existing scoped runtime-sync plan; that plan still requires its own review before apply. Runtime acceptance, Final Review and whole-task completion remain separate gates owned by the bound control plane.

## Assignment, continuity and bindings

The reviewer remains product `codex`, instance `align-native-implementation`, role `independent-reviewer`, capability profile `control-plane-high`, authority `governed-review-evidence`, distinct from author/executor/control-plane instance `align-native-root`. This is a correction review at the original Implementation Review stage. The approved scope, strict profile, Plan, Preflight, product/target sets, isolation and approval boundaries did not change. This review neither restarts Preflight nor performs a canonical transition.

The reviewer inspected actual corrected files and the complete relevant implementation diff, reran critical checks, performed independent adversarial probes and checked the final native evidence. The Router-governed review requirements remain in force. No implementation, runtime, Git or canonical-state mutation or further delegation was performed by this reviewer.

| Artifact | Whole-file SHA-256 |
| --- | --- |
| `docs/superpowers/plans/2026-10-10-align-native-agent-governance.md` | `8ec9d76241b3d25b1ce89e54bb0f094ac71dfe3a7c8d2ec0d71b94d18c8e5219` |
| `docs/review/2026-10-10-align-native-agent-governance-preflight.md` | `deed722c70c015ec4a38bef425d5cb62a2d922a9b61bb4d736406f2561edaadd` |
| Preserved first Implementation Review, `docs/review/2026-10-10-align-native-agent-governance-implementation.md` | `1af06f89a6b3cdc6a9a227f319f4991890fc05bdea9878c4ca9a49e3a82ca996` |
| Complete private review-package `corrected-implementation.diff` | `30d974e9b5891b75407db56669a674975133d736798b0425a692348a666be064` |
| Private `corrected-implementation-hashes.json` | `e7c7f4581a3e5e4650aa8822dc54e0743dc69ee261d345e441136f6a69caa143` |
| `docs/review/2026-10-10-align-native-agent-governance-source-verification.json` | `cc7089bdd505dc323503bd92f8493fdb5191f537c2ed1ba7b70386ef0f61c4be` |
| `docs/review/2026-10-10-align-native-agent-governance-forward.json` | `c15b4e52e8af47655af7384270fbde5edb077ac382671dcbb1ab0c43718da1cc` |

The durable source-verification artifact binds all thirteen reviewed source files. Its bindings and the private hash inventory were independently checked against the actual final isolated source. Relative to the preserved first review, these six file hashes changed; the other seven retain their first-review bindings:

```json
{
  "scripts/validate_core_gates.py": "be8a6b215b0b8b408ba9cb66036e98be97bd9c6872630aa0b8972969a91f54ea",
  "scripts/validate_cross_cli_sync.py": "640402ec081b2ceee22d515f8f97ee93bbae75ab102b1b2607c2024c44f607b9",
  "tests/test_workflow_rules.py": "ba2e486af4d0ab0f0286e5561826208728e7d404ab96faf4716afcda27471a14",
  "tests/test_cross_cli_sync.py": "4abec2ef2d907637efe8dbdb3fa5e8645222cb20dbaaba6fcde01d0a93930863",
  "tests/run_native_agent_governance_forward_tests.py": "20411c173bfe905a96355831578cdd5cfd454e184ab133a895e84276590eb4b4",
  "docs/engineering-invariants.md": "f24f3f9cdc4e23f874fa900c477c27e22e8b3518b74e48b628ac980024589c1b"
}
```

The original source's thirteen implementation paths still matched their prestates or expected absence at the final independent check. No source transfer was assumed. The fixture's original expectations remain byte-identical: SHA-256 `8d3c0c2d42e70e75125e5c95e9a14a6f395879202ba32f79ce8a95cdd16bb4b7`.

## Finding disposition

| Finding | Disposition and evidence |
| --- | --- |
| **F1: temporary-root cleanup contract** | **Closed.** The caller-named owned parent now contains a generated `routing-forward-native-*` directory compatible with the existing cleanup helper. Handler restoration is in an inner `finally`; cleanup failure suppresses summary publication and reports BLOCKED. Success is published after cleanup. Independent regressions exercised arbitrary caller names and injected cleanup failure. The final real native command exited 0 and its owned root was independently confirmed absent. |
| **F2: missing checkpoint obligations** | **Closed.** The owner check now includes destination precedence, publisher compatibility, backend-independent product identity and selective-hook protection. Thirty-four real-source clause mutations exercise the approved obligations. The reviewer independently repeated the original three failing mutations: all were rejected. Moved, comment-hidden and fenced checkpoint policy remains rejected. |
| **F3: hidden governance accepted by sync** | **Closed.** The actual v6 sync semantic validator now applies the same visible-Markdown parser used by core gates. Independent mutations passed through actual install/parity APIs rejected HTML-comment, tilde-fenced and indented-code governance. The author's regressions also cover backtick fences. The two portable scripts were copied alone into an isolated temporary directory and loaded in both directions successfully, including a separate isolated PyYAML interpreter. There is no import-time validation recursion or raw-text fallback. Versions 1–5 retain their existing semantic branch. |
| **F4: seven native cases failed** | **Closed for the bounded proof.** A case-independent classifier guide now defines the work being classified and the authority established by scenario evidence or accepted assignment. This resolves the distinction between an observer's ability to answer and the audited entry's authority. Expected fields were not changed or passed into the model prompt. The final real seven-case run has seven matches, valid native event audits, exit 0 and successful cleanup. Earlier 3/7 and 6/7 attempts remain recorded with their actual failures. |
| **F5: consumed bytes and hashes diverged** | **Closed.** Source files and the case fixture are each read once as bytes; decoding, projection/parsing and hashing use that same snapshot. The independent rerun of the source and fixture replacement regressions passed. These tests exercise actual preparation/hash/cleanup code with the process boundary stubbed; they are deterministic binding evidence and are not presented as native behavior. |

The new engineering-invariant text generalizes F1 and F5: evidence hashes describe consumed bytes, and required cleanup must succeed before reporting success. Its loading pointer and regression references are accurate. This learning revision remains inside the approved documentation scope and introduces no new product, schema, target, hook, authority or implementation phase.

## Independent checks

All reviewer Python commands used `PYTHONDONTWRITEBYTECODE=1`; isolated Python invocations also used `-I -B` where applicable. Fresh checks were rerun after the final runner revision and the learning-document addition.

| Check | Observed result |
| --- | --- |
| `python3 scripts/validate_core_gates.py .` | PASS, exit 0 on final source |
| Focused unittest set below | PASS, 37 tests, no failures or skips on final source |
| Detached two-script portable loading | PASS for repeated core → sync → visibility-parser loads and direct sync calls; PASS with dependency-free and isolated PyYAML interpreters |
| Original F2 mutation set | All rejected by the actual checkpoint owner validator |
| Additional hidden governance probes | HTML comments, tilde fences and indented code rejected by real managed parity validation |
| Historical semantic branch | Versions 1–5 preserve prior acceptance behavior; no legacy body rewrite |
| Final source, original prestates, native summary and full-suite log hashes | MATCH |

Focused unittest set, loaded through `unittest.defaultTestLoader.loadTestsFromNames` with `tests` added to `sys.path`:

```text
test_workflow_rules.NativeAgentConsumptionTests
test_cross_cli_sync.NativeConsumptionManagedRulesTests
test_cross_cli_sync.ScopedPlanSelectionTests
test_cross_cli_sync.ScopedPlanTamperTests
test_cross_cli_sync.ScopedTransactionTests
test_workflow_rules.WorkflowRulesTest.test_schema6_reviewer_assignment_exact_shape_fails_closed
test_workflow_rules.WorkflowRulesTest.test_schema6_standard_strict_and_compact_profiles_are_exact
test_workflow_rules.WorkflowRulesTest.test_tiered_08_same_product_instances_cannot_self_review
test_cross_cli_sync.DurableTargetTransactionTests.test_four_target_order_and_verify_all_require_verified_pi
```

The executor's final executable revision passed both complete suites: **492 tests with the dependency-free parser and 492 with PyYAML**, zero failures, errors or skips. Their log hashes match the durable verification record. Those suites ran before the subsequent documentation-only invariant addition; fresh affected tests and core validation covered that addition, including the reviewer's final-source reruns above. Final source/runtime verification remains a later gate. Quick validation, strict OpenSpec validation and unchanged Companion validation are separately recorded executor evidence, not claimed as independent full-suite reruns here.

## Native evidence boundary

The final private native summary has SHA-256 `3a3101d7459cce39513bfd44412999dd3acdefeba01a82c37440531866cfa88f`. The reviewer verified that the final attempt embedded in the durable forward artifact equals that summary, that its source/fixture hashes match this review's source, and that it records actual exit 0 and successful owned cleanup. Each of the seven cases reports exactly four native events, one agent message, zero tool events and no mismatched expected fields. The owned final run directory is absent.

This is observed native Codex classifier behavior under temporary project AGENTS projection plus the documented classifier guide. It does not prove native Skill-body loading, behavior without that guide, another actual account/entry or seven-entry acceptance. The reviewer inspected the executor's native evidence and did not run an additional seven-case native suite. Mocked lifecycle or replacement tests are not counted among these seven cases.

Both pre-change native baselines were compliant. The initial and intermediate enum mismatches were classifier-contract defects, not proof of a reproduced governance violation. Deterministic RED/GREEN rejection of the old universal Preflight rule, missing advisory exception and contradictory external waiver remains the actual source-regression evidence.

## Completeness and remaining gates

No actionable finding remains in this reviewed source scope. All reasonably discoverable findings from the supplied corrected files, complete diff and evidence have been reported. No recommendation is used to hide an unresolved requirement. The original FAIL review remains immutable; this artifact records its correction result rather than rewriting it.

Declined to judge: native Skill-body loading, seven actual entries and Grok hook enforcement, which remain outside this source slice; the forthcoming native-adaptation plan is not approved by this review. Existing accepted residual risks remain owned by `align-native-root`: portable parity cannot qualify alternate consumers, and native Grok publisher compatibility requires separate supported adaptation evidence.

The control plane may use this PASS for the already-authorized guarded source transfer and scoped runtime-plan preparation. Exact runtime destinations/prestates, transaction apply/verify/recovery, final verification and separate Final Review remain pending. No Git, publication, native configuration mutation or whole-task completion authority is granted. Raw native traces, authentication and configuration were not copied into this review.
