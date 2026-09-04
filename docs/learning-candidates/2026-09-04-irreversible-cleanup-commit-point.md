# Learning Candidate: Irreversible cleanup commit point

```yaml
status: promoted
event_kind: integrity
severity: high
scope: project-local
promotion_trigger: high-severity
symptom: "Adapter build could fail after deleting the only exact prior-state copy."
prior_assumption: "Directory rmdir was the commit point even though recovery SKILL.md had already been unlinked."
correction_or_evidence: "Independent Review reproduced a residue race between unlink and rmdir; the focused RED regression reproduced the same loss boundary."
generalized_invariant: "Deleting the final recoverable link is the commit point; all later cleanup must be non-rejecting."
independent_reproductions: "Independent reviewer adversarial probe and control-plane deterministic regression."
independence_rationale: "The reviewer used a separate instance and probe; the regression was then added in the implementation workspace."
duplicate_or_conflict_result: "No conflicting project invariant found."
target_artifacts: "docs/engineering-invariants.md; scripts/build_skillsmp_adapter.py; tests/test_distribution.py"
mechanical_enforcement: required
mechanical_enforcement_reason: "The race is deterministic at the unlink/rmdir seam."
verification: "Focused recovery tests 5/5 PASS; independent Review PASS."
review_result: pass
decision_owner: codex
decision_provenance: "Approved add-skillsmp-index-adapter closeout; independent implementation Review PASS on 2026-09-04."
```

Evidence paths:

- `docs/design/reviews/2026-09-04-add-skillsmp-index-adapter-implementation-review.md`
- `scripts/build_skillsmp_adapter.py`
- `tests/test_distribution.py`
