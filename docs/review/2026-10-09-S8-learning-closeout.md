# S8 Learning Closeout

Author: elvis. Date: 2026-10-09. Scope: approved S8 only.
Audit snapshot: corrected implementation and four-target sync have passed;
the consolidated-input implementation re-Review and distinct Final are pending.

```yaml
status: promoted
event_kind: false-pass
severity: high
scope: project-local
promotion_trigger: high-severity
symptom: the test-side document audit accepted changed link destinations and a source directory symlink
prior_assumption: removing Markdown destinations preserved content and checking the source leaf excluded symlink traversal
correction_or_evidence:
  - docs/review/2026-10-09-S8-implementation-review-full.json
  - docs/review/2026-10-09-S8-audit-correction.json
  - docs/review/2026-10-09-S8-implementation-review-corrected.json
generalized_invariant: a document relocation audit must retain external URL bytes and local referent/query/fragment identity through the selected move mapping, and reject every source symlink component before reading
independent_reproductions: 2
independence_rationale: the independent implementation reviewer exercised actual adverse files; the control plane separately reproduced all three accepted wrong effects, observed three failing new regressions, and fixed the same approved test-side audit
duplicate_or_conflict_result: existing ownership content-preservation and bound-project requirements cover this behavior; existing engineering guidance already explains ancestor symlink safety; no new rule copy, guidance edit or backlog candidate is needed
target_artifacts:
  - tests/test_workflow_rules.py
  - references/project-learning-closeout.md
mechanical_enforcement: required
mechanical_enforcement_reason: actual file identities, bytes and path components can be checked deterministically within the approved test-side audit
verification: three observed RED failures followed by 17 focused GREEN tests in both environments, full suites of 478 each, and actual re-audit of seven native branches
review_result: pass
decision_owner: codex
decision_provenance: bound s8-control-01 accepted distinct s8-review-01 corrected implementation PASS e385e6f4b5f241202d18f5ce5a393ee9e82f7ad66871f61bb0fc5f2576bfce13 under the original specific add-project-document-ownership approval
```

The durable mechanical promotion is the existing audit plus
`test_move_cannot_change_external_url`,
`test_relative_repair_cannot_switch_to_another_existing_target`, and
`test_source_intermediate_symlink_is_rejected_without_local_links` in
[the approved test file](../../tests/test_workflow_rules.py).
The owning [relocation rule](../../references/project-learning-closeout.md#authorized-relocation-and-reference-closure)
already requires these properties. Neither target moves ordinary project files
or changes evidence, completion, reviewer selection or shared governance.

The [corrected Review](2026-10-09-S8-implementation-review-corrected.json)
independently rejected both link-retargeting counterexamples, an additional
query change, and ancestor symlink traversal while accepting legitimate repaired
navigation. Its whole-file SHA is recorded above. The
[correction record](2026-10-09-S8-audit-correction.json), SHA
`1396cea0e1cb8d5aadca8869f122a8b98578e9364cd608e9c5bffbe32740f84c`,
retains actual RED/GREEN evidence; the
[native revalidation](2026-10-09-S8-native-audit-revalidation.json), SHA
`b2045caada940f6a4513fea3fc665d3257b3b6702effdb235aefd7d132996829`,
binds unchanged real native effects to the stronger audit.

This Candidate Card uses the contracted S8 review-artifact location and the
canonical template fields. Its `review_result` describes the accepted durable
code promotion, not a Final or a claim that this new audit artifact has already
been independently reviewed. The consolidated-input implementation re-Review
must review this exact artifact before fresh persisted verification and a
separate Final. No source change follows that promotion merely to add prose.

Other corrections were local orchestration details: fixture read permissions,
a private native case label, and the sync wrapper's receipt field name. The
[sync evidence](2026-10-09-S8-sync.json) records the wrapper error, both rejected
post-commit calls and the actual successful four-target `verify-all`; rejected
calls are never counted as PASS. These details do not introduce another
independent project invariant or a new production framework. No domain glossary,
ADR, protected guidance edit or new global candidate arose in this audit.

This summary retains non-sensitive provenance and durable targets only.
Private native prompts, traces and transaction backups remain temporary until
publication and rollback gates settle, then are removed under the existing
owned-backup cleanup contract.
