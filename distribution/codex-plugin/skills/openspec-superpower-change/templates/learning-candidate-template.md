# Learning Candidate Card

```yaml
status: candidate | promoted | rejected | blocked
event_kind: correction | review-finding | security | integrity | data-loss | false-pass
severity: low | medium | high
scope: task-local | project-local | global
promotion_trigger: threshold | explicit-archive-distill | high-severity | none
symptom:
prior_assumption:
correction_or_evidence:
generalized_invariant:
independent_reproductions:
independence_rationale:
duplicate_or_conflict_result:
target_artifacts:
mechanical_enforcement: required | infeasible | not-applicable
mechanical_enforcement_reason:
verification:
review_result: pending | pass | fail | blocked
decision_owner: codex
decision_provenance:
```

## Rules

- Use project-relative evidence references and SHA-256 values when available.
- Summarize the evidence; do not copy a full conversation or Review transcript.
- Keep credentials, tokens, private prompts, customer data, and other sensitive
  content out of this artifact.
- Put domain meaning in `CONTEXT.md`, engineering/agent invariants in the
  repository-defined guidance (default `docs/engineering-invariants.md`), and
  qualifying decisions in ADRs.
- When behavior is mechanically enforceable, require a deterministic regression
  test or validator; prose-only documentation cannot satisfy promotion.
- When mechanical enforcement is infeasible, require a non-blank reason and an
  explicit adversarial Review scenario.
- Only the Codex control plane records `promoted` and accepts Review PASS.
