# Native Agent Governance Final Review

Author: elvis. Date: 2026-10-10. Change: `align-native-agent-governance`, approved draft-v1.

Result: **FAIL**. One actionable closeout finding remains: the required classified Learning Candidate Card is missing. The reviewed source implementation, completed four-target transaction, bounded native evidence and follow-up plan have no additional actionable finding from this review. This result does not authorize completion or backup cleanup.

## Assignment, authority and review boundary

Review purpose: independent strict Final Review of the approved source-and-existing-four-runtime slice, its required learning delivery and next native-adaptation plan. Reviewer product: `codex`; instance: `align-native-final-review`; role: `independent-reviewer`; capability: `control-plane-high`; independence: distinct from author/executor/control-plane `align-native-root`, Implementation reviewer `align-native-implementation` and runtime-plan reviewer `align-native-sync-review`; authority: `governed-review-evidence` only.

Gate 0: Router Review-only within the already-approved Major Self-Evolution scope; `SKILL.md`, project AGENTS, approved proposal/design/spec/plan, capability/completion/learning/sync references and selected executing-plans/requesting-code-review Router-governed variant were read. Fresh verification-before-completion discipline was applied. The only authorized repository write by this reviewer is this review artifact. No implementation, native/runtime/configuration, canonical state, evidence history or Git mutation, native model probe or further delegation was performed. Isolated regression fixtures and in-memory mutations supplied independent evidence.

The original implementation Plan and Preflight remain valid; this same-scope Final Review finding does not reopen them. Canonical task reconciliation and cleanup are subsequent owner actions. Their current pending checkboxes are not represented as acceptance evidence and are not additional findings.

## Exact evidence and complete-diff inspection

| Artifact | Whole-file SHA-256 |
| --- | --- |
| `docs/superpowers/plans/2026-10-10-align-native-agent-governance.md` | `8ec9d76241b3d25b1ce89e54bb0f094ac71dfe3a7c8d2ec0d71b94d18c8e5219` |
| `docs/review/2026-10-10-align-native-agent-governance-preflight.md` | `deed722c70c015ec4a38bef425d5cb62a2d922a9b61bb4d736406f2561edaadd` |
| `docs/review/2026-10-10-align-native-agent-governance-implementation-r2.md` | `ff4a8a68aa8ca5c6eb9a9da497e7ea71ac0022c17650899eef6631dbe6958930` |
| Complete corrected source diff, independently rebuilt from preserved prestates and actual source | `30d974e9b5891b75407db56669a674975133d736798b0425a692348a666be064` |
| `docs/review/2026-10-10-align-native-agent-governance-final-verification.json` | `90fb3b92f52738f9954e7537b615327c9b76014caa136ca4cf3fd2fbb47f97c6` |
| `docs/review/2026-10-10-align-native-agent-governance-sync-plan.json` | `6b96b7fa7a8e727cfe55a79f1eace532f4960e53d6748b1b12ff736e56d64376` |
| `docs/review/2026-10-10-align-native-agent-governance-forward.json` | `c15b4e52e8af47655af7384270fbde5edb077ac382671dcbb1ab0c43718da1cc` |
| `docs/review/2026-10-10-align-native-agent-governance-learning-closeout.md` | `ef3f9bc9e9cd76c79adbb30a4df70c55d74a15f854782aa30ea8bcd1532afef8` |
| `docs/superpowers/plans/2026-10-10-native-agent-adaptation-next.md` | `962de1d729d7c0d876d71b88e82a1953b6cd5c4b1c61d203e1bd670e54d1760c` |

The reviewer read the complete thirteen-file implementation diff and actual affected code/docs, then regenerated that diff from the preserved prestate and current checkout: byte-identical. All thirteen source hashes match the final-verification manifest. The other 540 original Router files and all 23 original Companion files retain their baseline contents/modes; pre-existing dirty specs and JEV material remain preserved. Neither SKILL body, portable manifest, Companion contract nor existing schema/product/history rules changed.

The shared CCG-004 replacement and CCG-014 append match the approved text. The two changed paragraphs use exact complete-paragraph checks, and the native checkpoint obligations are validated within their owning visible Markdown section. The mutual dynamic imports are lazy function calls, without import-time validator recursion. The runner hashes the same bytes used for projection/parsing, audits native events, restores signal handlers and publishes successful output only after owned cleanup.

## Fresh independent checks

All reviewer Python commands used `PYTHONDONTWRITEBYTECODE=1`. No additional whole-suite or seven-case native model run was needed.

| Command or check | Actual result |
| --- | --- |
| `python3 scripts/validate_core_gates.py .` | Exit 0; current source core gates valid. |
| `python3 scripts/validate_cross_cli_sync.py verify-all --plan <private-container>/sync-plan.json --transaction-root <private-container>/runtime-transactions` | Exit 0; all four targets verified in canonical order. |
| `openspec validate align-native-agent-governance --strict` | Exit 0; valid. |
| Focused unittest selection below | 23 tests, exit 0, no failures, errors or skips. |
| Independent real-validator negative probes below | All 16 mutations rejected. |
| Actual source/runtime content and mode inspection | All 160 portable destinations match their bound source hashes; seven selected files and 33 assertions per target. |
| Managed native outside-byte inspection | All four outside-block digests match the preserved runtime prestates. |
| Receipt inspection | All four private receipts are verified and byte-identical to their durable copies; plan/content hashes remain bound. |
| Source/evidence freshness | Two full-suite log hashes, source hashes, native summary, learning and next-plan bindings match the final-verification manifest. |
| Next-plan native prestates | All six regular file hashes, proposed dependency hash, protected publisher hash and existing Cursor symlink target match actual local objects. |
| Learning artifact visibility | Existing engineering invariant and closeout paths, and proposed candidate path, are not Git-ignored. |

Private container used read-only for receipts, prior bytes and logs:
`/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/align-native-agent-governance-b763154v`.

The focused suite was loaded using `unittest.defaultTestLoader.loadTestsFromNames` with `tests` on `sys.path`:

```text
test_workflow_rules.NativeAgentConsumptionTests
test_cross_cli_sync.NativeConsumptionManagedRulesTests
test_cross_cli_sync.ScopedPlanTamperTests
test_workflow_rules.WorkflowRulesTest.test_schema6_current_contract_accepts_all_four_reviewer_products
test_workflow_rules.WorkflowRulesTest.test_schema6_reviewer_assignment_exact_shape_fails_closed
test_workflow_rules.WorkflowRulesTest.test_schema6_standard_strict_and_compact_profiles_are_exact
test_workflow_rules.WorkflowRulesTest.test_schema6_current_and_legacy_validation_are_isolated
test_workflow_rules.WorkflowRulesTest.test_tiered_08_same_product_instances_cannot_self_review
test_cross_cli_sync.DurableTargetTransactionTests.test_four_target_order_and_verify_all_require_verified_pi
```

Independent probes called current production APIs using real source strings, the actual reviewed sync plan and a valid current schema-6 fixture:

- Managed body hidden in a tilde fence, indented code or an HTML comment: install/parity API rejected all three.
- Valid CCG-014 prefix followed by a native-save authority waiver: rejected.
- Native checkpoint content hidden in a tilde fence or moved below a foreign heading: rejected.
- Actual sync plan with an extra Claude target, omitted Pi assertion, changed Grok source hash or deselected Codex managed rule: rejected.
- Actual plan coherently retargeted to account-A AGENTS with that file's genuine current prestate: rejected before mutation.
- Formal reviewer products `claude-code`, `claudex` and `cursor`, publisher-conferred canonical authority and executor-instance self-review: rejected.

Two reviewer probe harness mistakes were corrected before accepting their results: an overly strict log-tail regex did not account for buffered unittest fixture output after `OK`, and the schema mutation initially used `instance_id` instead of `agent_instance_id`. The corrected complete probes ran successfully; neither issue indicated a product failure or changed evidence/source files.

Executor full-suite evidence was inspected, not claimed as an independent rerun: 492 tests in each of the fallback and PyYAML modes, with log hashes `d9bdd641cc68da1799c20037a0cad5ac4931f1254c9f7cbf8aa901413438dd6b` and `fe98390e64d79c2e95ce1d910c3deaa541280bd2afe3f4a44b8e7c12cdc0fef6`. Source quick/core checks in both modes, unchanged Companion 91-test/quick/template checks and per-target checks are executor evidence bound in the final manifest. No later source change invalidated them at this review boundary.

The three preserved native attempt exits are 1, 1 and 0. The final private summary equals the durable embedded summary and matches its hash. All seven records have four native events, one agent message, zero tool events, no mismatch and matching source/fixture hashes; final owned cleanup is recorded successful. Raw Grok inspection is absent. These results establish only Codex temporary project-AGENTS consumption with the case-independent classifier guide. They do not establish Skill-body loading, behavior without that guide, another account or seven actual entries.

## Consolidated actionable finding

**FR1 — Important, closeout requirement: missing classified Candidate Card.**

Location: `docs/review/2026-10-10-align-native-agent-governance-learning-closeout.md:5` and `references/project-learning-closeout.md:121`, `:138`.

The closeout correctly declares mandatory promotion and points to durable invariants and tests, but no corresponding classified Candidate Card exists under the established learning-candidate convention or in the supplied closeout. The normative reference requires the template and blocks completion when a mandatory promotion lacks a classified card and non-sensitive provenance. The current prose does not record the required classification, independent evidence/independence rationale, duplicate/conflict disposition, decision provenance and per-candidate target/enforcement/review boundary in the requested artifact form. Existing Implementation Review of the invariant cannot substitute for this missing closeout deliverable.

Minimal correction: create a change-specific card using `templates/learning-candidate-template.md`, with project-local classification, actual trigger/severity, summarized hashed source/Review evidence, target and deterministic enforcement pointers, the bound decision owner and explicit distinction between already-reviewed invariant targets and the newly added provenance. Link it from the closeout; verify hashes, required fields, non-ignored placement, redaction and references; refresh affected final evidence and return for independent review at this same Final Review stage. Do not change the thirteen accepted source files, rerun native models, widen native adaptation, rewrite historical evidence or reopen Preflight for this correction.

`blocking_findings: [FR1]`; `non_blocking_recommendations: []`; `finding_completeness: true`. All reasonably discoverable findings from the supplied complete diff, actual files, logs, scope and risk-appropriate probes have been consolidated here. No actionable issue is deferred as a residual risk.

## Follow-up plan, declined-to-judge items and residual ownership

The next native plan is delivered as a reviewable follow-up, not an executable approval. It preserves Companion and the existing installer; distinguishes launcher from formal product identity; identifies Claude publisher/path conflicts; retains immutable attempt paths and personal ownership overrides; and binds current candidate native files/dependency/publisher states. Grok selective hook exclusion is expressly unverified and not implementation-ready. The absence of that mechanism is accurately scoped follow-up work, not a failure of the currently approved four-target source slice.

Declined to judge:

- Actual loading and behavior of all seven native entries, including account A, Claude/Cursor and launcher publication: outside the approved implementation slice and not exercised here. Owner: `align-native-root`; decision: obtain the separately scoped adaptation approval and actual-entry evidence before such claims.
- Grok selective hook compatibility and any native configuration/link mutation: no supported selective mechanism or approved exact-key mutation is supplied. Owner: `align-native-root`; decision: isolated mechanism research/readiness review before requesting or exercising native-write authority.
- Git publication, archival and canonical whole-task completion: not authorized to this reviewer. Owner: the bound control plane with applicable user authorization; the source slice may only advance after FR1 correction and same-stage Review PASS.

Accepted non-blocking residual risk: native prestates are observations in time, so the next approved adaptation must recheck them; four-target parity remains narrower than native-entry qualification. The plan carries the appropriate stop/rollback conditions. No new native writes or authority are approved by this review.

Temporary rollback backups correctly remain retained while Final Review is FAIL. After correction, fresh affected verification and an independent Final Review PASS, the owner may reconcile canonical tasks and perform the already-required scoped cleanup. The whole seven-entry user goal, publication and overlapping-spec archival remain unclaimed.
