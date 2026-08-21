# Learning Candidate Card: Forward Proofs Audit Native Events

```yaml
status: promoted
event_kind: false-pass
severity: high
scope: project-local
promotion_trigger: high-severity
symptom: A marker-perfect behavioral probe could pass after a read-only shell or file fallback because the runner discarded the native event stream and checked only final output plus filesystem mutation.
prior_assumption: Read-only sandboxing, a no-write snapshot, and a correct final marker were sufficient evidence that native Skill loading produced the result.
correction_or_evidence: The runner now captures JSONL in memory, rejects tool, command, file, MCP, unknown, and invalid events, and persists only sanitized counts; an actual probe and an independent adversarial event both exposed the old false-PASS path.
generalized_invariant: A no-tool behavioral proof audits the native event stream with a fail-closed allowlist; final-output correctness and no mutation cannot substitute for event evidence.
independent_reproductions: independent static Review attack plus an isolated native-loading control that emitted command events while leaving the snapshot unchanged
independence_rationale: The sources used different mechanisms and together established a high-severity false-PASS condition; either high-severity event is sufficient for promotion.
duplicate_or_conflict_result: Extends the existing temporary-trace hygiene invariant from evidence storage to evidence validity without weakening either rule.
target_artifacts: docs/engineering-invariants.md; tests/run_superpowers_routing_forward_tests.py; tests/test_workflow_rules.py
mechanical_enforcement: required
mechanical_enforcement_reason: Deterministic tests inject a marker-perfect command event and require the event parser to reject it; guidance text is also pinned by a focused regression.
verification: focused guidance regression RED then GREEN; marker-perfect command-event rejection GREEN; default and PyYAML full suites 150/150 PASS; independent learning Review PASS
review_result: pass
decision_owner: codex
decision_provenance: discovered during approved implementation High Review and promoted by the high-severity false-PASS threshold
```

## Non-sensitive provenance

- `docs/design/evidence/tighten-codex-superpowers-invocation-routing/2026-08-07-task-4-forward-tests.md` —
  `938a77f686410978238a25434d370a63ed18bc0c57ace50607bcc61efd249683`
- `tests/run_superpowers_routing_forward_tests.py` —
  `52570f985fe4920aba5666e130dde43311cd72e1d1753fd5381513f24ea276e1`
- `tests/test_workflow_rules.py` —
  `c6c120ff5d5237fa54f50bcf28b2c108bde253a246e9bffd60cc334597625916`

No raw trace, transcript, private prompt, credential, token, customer data, or
private source content is stored in this Candidate Card.
