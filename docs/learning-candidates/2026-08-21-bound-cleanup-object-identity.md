# Learning Candidate Card

```yaml
status: promoted
event_kind: false-pass
severity: high
scope: project-local
promotion_trigger: high-severity
symptom: "A quarantine-name replacement could delete an unrelated inode or leave visible canonical Pi PASS evidence while recovery reported BLOCKED."
prior_assumption: "A final pathname recheck plus name-relative unlink/reopen was sufficient to preserve cleanup ownership."
correction_or_evidence: "R14 reproduced unrelated-inode deletion; R15 made deletion fail closed; R15 reproduced retained valid Pi PASS after final-bind replacement; R16 rewrites through the validated retained descriptor and preserves the replacement."
generalized_invariant: "Final cleanup ownership binds an object identity, not a pathname. Without an exact-owner deletion primitive, preserve visible mode-0600 recovery/blocker evidence, never delete an unrelated replacement, and neutralize retained PASS-shaped evidence through the retained writable descriptor."
independent_reproductions: "docs/design/reviews/2026-08-21-add-role-first-review-routing-source-rereview-p1-r14.md (SHA-256 21c8af525ada608343c9498697020d9dbd28a763bf461b4218ff4451a8b77cc5); docs/design/reviews/2026-08-21-add-role-first-review-routing-source-rereview-p1-r15.md (SHA-256 c77d7a284867063abdcaccb941844cc673550aeaf18228fecfd3f383ff29f3fc); docs/design/reviews/2026-08-21-add-role-first-review-routing-source-rereview-p1-r16.md (SHA-256 dab79a6a8b03a80b9a453c0dbc79a5af9de406835e43670cc26c6de9e113acb4)."
independence_rationale: "R14 and R15 independent Source High Reviews exposed distinct ownership failures; R16 independently verified the corrected production path and canonical-PASS regression. One high-severity false-PASS/integrity event is sufficient for promotion."
duplicate_or_conflict_result: "Complements existing pre-state, sensitive-trace, and native-event invariants; it adds the cleanup object-identity boundary without changing approval or publication authority."
target_artifacts: "docs/engineering-invariants.md; tests/test_cross_cli_sync.py"
mechanical_enforcement: required
mechanical_enforcement_reason: "The invariant is enforced by descriptor-bound production cleanup and deterministic final-bind replacement regressions."
verification: "R16 focused P1 7/7 PASS; Router cross-CLI 149/149 PASS; Router workflow 124/124 PASS; full discovery 273/273 PASS; Companion 87/87 PASS; OpenSpec strict/all 3/0; canonical Pi PASS residue probe PASS."
review_result: pass
decision_owner: codex
decision_provenance: "Promoted during Project Learning Closeout after the R16 implementation Review PASS and the high-severity false-PASS threshold; source Review and final evidence are bound by source-verification."
```
