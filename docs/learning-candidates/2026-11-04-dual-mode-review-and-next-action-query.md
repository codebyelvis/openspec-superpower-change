# Learning Candidate Card: Dual-mode headless cross-review, validator-delegated next-action query, and post-receipt closeout recording

Author: `elvis`
Change: `add-next-action-query` (archived as `openspec/changes/archive/2026-11-04-add-next-action-query`) and `optimize-closed-loop-runtime-routing` dual-mode cross-review update.

```yaml
status: promoted
event_kind: review-finding
severity: medium
scope: project-local
promotion_trigger: two-independent-signals
symptom: "Headless cross-review examples initially included non-read-only flags (--tools bash / --dangerously-skip-permissions); scripts/next_action.py initially duplicated batch/tuple transition conditionals in _is_transition_applicable; and the closeout report initially extrapolated SHA-256 suffixes and pre-recorded a reviewer PASS before R3 signoff completed."
prior_assumption: "Prompt-level read-only instructions sufficed even with broad CLI flags; table-only imports in next_action.py prevented rule duplication; and closeout reports could pre-fill expected reviewer PASS status before invoking the reviewer."
correction_or_evidence:
  - "agy Final Review R1 (session cfaad7d8-0c84-4870-b741-9b31c29edee4) caught 4 SHA-256 digest mismatches in docs/review/2026-11-04-add-next-action-query-closeout.md; fixed from exact shasum -a 256 disk bytes and verified in R2 PASS."
  - "codex-a Review R1/R2 (gpt-6-astra, medium, read-only) caught P1 non-read-only CLI flags in global rules, P2 _is_transition_applicable conditional duplication in scripts/next_action.py, and P2 static Plan checkbox / pre-recorded PASS in closeout.md; all fixed and verified in R3 PASS."
generalized_invariant: "Enforce verifiable read-only tool/snapshot boundaries for headless cross-reviews, delegate sibling transition queries exclusively to validate_transition via probe_transition_candidate in validate_core_gates.py, keep Plan checkboxes static, and record only actual disk SHA-256 digests and received review verdicts in closeout reports."
independent_reproductions: "2 (independent agy Final Review session cfaad7d8-0c84-4870-b741-9b31c29edee4 and independent codex-a read-only review sessions)."
independence_rationale: "Distinct reviewer products and sessions (antigravity-cli and codex-a) independently inspected the implementation and closeout artifacts."
duplicate_or_conflict_result: "Extends docs/engineering-invariants.md with section 15. Does not weaken Non-Negotiables."
target_artifacts:
  - docs/engineering-invariants.md
  - scripts/validate_core_gates.py
  - scripts/next_action.py
  - tests/test_next_action.py
  - tests/test_workflow_rules.py
mechanical_enforcement: required
mechanical_enforcement_reason: "tests/test_next_action.py asserts absence of _is_transition_applicable and planned_batches in scripts/next_action.py and verifies 1-to-1 delegation to probe_transition_candidate / validate_transition; tests/test_workflow_rules.py enforces dual-mode headless CLI cross-review routing."
verification:
  - "tests/test_next_action.py (7 tests) and tests/test_workflow_rules.py (218 tests) pass."
  - "scripts/validate_core_gates.py, quick_validate.py, and openspec validate pass."
review_result: pass
decision_owner: codex
decision_provenance: "2026-11-04: Promoted during add-next-action-query archive and closeout after agy and codex-a independent reviews."
```

Durable rule: [Dual-mode headless cross-review, validator-delegated next-action query, and post-receipt closeout recording](../engineering-invariants.md#dual-mode-headless-cross-review-validator-delegated-next-action-query-and-post-receipt-closeout-recording).
