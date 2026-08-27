# Learning Candidate Card: Scoped Managed-Rule Destination Binding

```yaml
status: candidate
event_kind: false-pass
severity: high
scope: project-local
promotion_trigger: high-severity
symptom: A schema-v2 plan accepted a managed-rule destination and matching pre-state for an unrelated regular file, allowing downstream candidate generation to treat that file as the global governance rule.
prior_assumption: Root containment and a matching serialized pre-state were sufficient to authorize a managed global-rule destination.
correction_or_evidence: Independent final Review evidence identified the coherent destination/pre-state bypass; the deterministic regression reproduces it and now requires target-specific canonical runtime binding.
generalized_invariant: A managed global-rule destination must be derived from its validated target runtime binding and cannot be redefined by plan data; destination/pre-state tampering must fail before candidate or backup creation.
independent_reproductions: independent final Review adversarial probe; deterministic scoped-plan tamper regression
independence_rationale: The Review probe and the repository regression exercise the same prior assumption through separate evidence paths; the high-severity false-PASS threshold is met without relying on recurrence.
duplicate_or_conflict_result: Existing reviewed-runtime pre-state invariant covers byte/mode drift but not destination identity; this candidate adds the missing target-binding boundary.
target_artifacts: docs/engineering-invariants.md; scripts/validate_cross_cli_sync.py; tests/test_cross_cli_sync.py; references/cross-cli-sync.md; references/sync-checklist.md; openspec/specs/skill-workflow-governance/spec.md
mechanical_enforcement: required
mechanical_enforcement_reason: The validator can deterministically derive four target-specific rule paths, and the regression rejects coherent destination/pre-state retargeting before candidate, backup, or apply.
verification: RED focused regression before fix; GREEN focused scoped plan/tamper/transaction suite after fix; final fresh verification `final-verification/current/summary.json` with current hash recorded in the bound evidence manifest
review_result: pass
decision_owner: codex
decision_provenance: user-requested correction; promotion remains subject to Project Learning Closeout and independent Review
```

## Non-sensitive provenance

- User-provided final Review evidence: `/tmp/final-workflow-optimization-acceptance-review-r1.I1RqrX`
  SHA-256 `b9c3717ffc597466f806772ec188ac74bc5bcd524235b5e619045589a9481d3`.
- Correction implementation plan: `docs/superpowers/plans/2026-08-27-fix-cross-cli-sync-review-findings.md`.
- Deterministic regression: `tests/test_cross_cli_sync.py`.
- Independent Review: `/private/tmp/fix-cross-cli-sync-review-findings-20260827/final-review/final-r1/review.final.md`
  SHA-256 `cd336bb0f30432f0261d4dc1ac86484b8b3495f806f9f7a4fbb70ba259922b81`.
- Later r2 self-reference failure is retained as non-authorizing correction evidence.
- Supplemental independent Grok Review: `/private/tmp/fix-cross-cli-sync-review-findings-20260827/final-review/grok-r1/review.final.md`
  SHA-256 `c545bcdb8d946eb23cb4488807036696b1d0474e68d55b227a31b5113ae8b568`.

No chat transcript, private prompt, credential, token, customer data, or raw
runtime trace is stored in this Candidate Card.
