# Learning Candidate Card: Runtime Sync Destination Pre-state

```yaml
status: promoted
event_kind: integrity
severity: high
scope: project-local
promotion_trigger: high-severity
symptom: A reviewed sync plan bound source hashes but not live destination bytes, so apply could silently overwrite drift that occurred after Review and rollback would preserve the wrong pre-state.
prior_assumption: Revalidating canonical source hashes immediately before apply was sufficient to keep a reviewed runtime synchronization transaction safe.
correction_or_evidence: Plans now bind every destination and rule file to hash, mode, or absence; apply checks all pre-states twice before mutation, and adversarial tests prove drift aborts before backup or write and rollback restores the reviewed state.
generalized_invariant: A reviewed mutating plan binds destination pre-state and rechecks it immediately before the transaction; source identity alone does not authorize overwriting concurrent destination changes.
independent_reproductions: independent High Review data-flow analysis plus deterministic existing-file and absent-to-created drift probes
independence_rationale: The reviewer identified the integrity gap statically and isolated runtime tests reproduced both overwrite classes through separate destination states.
duplicate_or_conflict_result: Specializes the existing backup and rollback rules by defining which pre-state Review authorizes; no conflict with source-of-truth or one-target-at-a-time rules.
target_artifacts: docs/engineering-invariants.md; scripts/validate_cross_cli_sync.py; tests/test_cross_cli_sync.py; tests/test_workflow_rules.py
mechanical_enforcement: required
mechanical_enforcement_reason: Sync tests mutate an existing rule and create an expected-absent destination after planning, require apply to fail before backup or write, and verify forced-failure rollback restores bytes, mode, and absence.
verification: focused guidance regression RED then GREEN; isolated drift and rollback regression GREEN; default and PyYAML full suites 150/150 PASS; independent learning Review PASS
review_result: pass
decision_owner: codex
decision_provenance: discovered during approved implementation High Review and promoted by the high-severity integrity threshold
```

## Non-sensitive provenance

- `docs/design/evidence/tighten-codex-superpowers-invocation-routing/2026-08-07-task-5-runtime-sync.md` —
  `d5e9c244941f5cab03272a266df0179e30d6bc9ba43e9a4eee654c43e236c926`
- `scripts/validate_cross_cli_sync.py` —
  `7c6248b3f34cf94b8ea2930f65a30c768970d0a38b666268d72fe5f6016acdd0`
- `tests/test_cross_cli_sync.py` —
  `4799819c0e1647d4c9b660abf0d75e6e566849cf0a3f9596c670a27518dee2d6`

No raw trace, transcript, private prompt, credential, token, customer data, or
private source content is stored in this Candidate Card.
