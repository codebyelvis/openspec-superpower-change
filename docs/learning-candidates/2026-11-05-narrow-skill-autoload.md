# Learning Candidate: Narrow autoload, complete reference migration, and scoped delivery

Author: `elvis`
Change: `narrow-skill-autoload`

```yaml
status: promoted
event_kind: review-finding
severity: medium
scope: project-local
promotion_trigger: explicit-archive-distill
symptom: "Role-body migration left a forward reader on the old path; dirty source and installed prestate contained unrelated work that could not be published or removed."
prior_assumption: "Changing the two skill bodies and obvious assertions would close the migration; one whole-file snapshot could serve both publication and installation."
correction_or_evidence:
  - "Main worktree: 506 tests initially had one marker-extraction error; correcting the Companion reference path restored 506 passing tests. Pi independently identified and rechecked this same defect."
  - "Companion migration: 92 tests with eight RED failures became 92 passing tests after entry, location assertions and complete-body hash alignment."
  - "Publication used HEAD plus only this task's patch: Router 486 tests and Companion 92 tests passed. The 20-test difference came from excluded, unrelated untracked worktree tests."
  - "Codex installation used five selected files plus 36 parity assertions. Removing only this task's two validator-function changes recreated the original runtime bytes. Other three runtime copies and global rules stayed unchanged."
generalized_invariant: "Treat entry eligibility, post-entry governance, reference consumers, publication baseline and installation prestate as explicit separate scopes; verify each without expanding authorization or evidence claims."
independent_reproductions: "One runtime-independent regression plus a distinct Pi reviewer observation of the same reader defect; separate Codex installation Review checked destination preservation. These are not multiple independent production reproductions."
independence_rationale: "The executor ran deterministic tests; distinct Pi and Codex reviewer instances inspected files and bounded evidence without implementing the patch."
duplicate_or_conflict_result: "Extends existing authorization/evidence, copy-boundary and runtime-prestate guidance with consumer closure and exact release-candidate coverage; no new workflow gate or portable rule."
target_artifacts:
  - docs/engineering-invariants.md
  - docs/learning-candidates/2026-11-05-narrow-skill-autoload.md
mechanical_enforcement: required
mechanical_enforcement_reason: "Reuse existing entry/location/hash/forward-reader and scoped-sync regressions. Actual Git-index and installed-prestate identity are environment-specific; byte comparisons and adversarial Review cover those facts without inventing a new fixture or altering behavior."
verification:
  - "Fresh learning checks: Router description 2/2; classification and scoped-sync checks 21/21; Companion role checks 2/2. Independent reviewer reran Router 7/7 and Companion 4/4; all had zero failures/errors/skips."
review_result: pass
decision_owner: codex
decision_provenance: "User explicitly requested archive, distillation and GitHub push; Codex accepted the distinct reviewer learning PASS after fresh verification. Promotion is project-local and grants no new runtime or publication authority."
```

## Durable targets and existing enforcement

- [Explicit entry and lazy role context](../engineering-invariants.md#explicit-entry-and-lazy-role-context-must-agree-with-every-consumer).
- [Publication patch and installed prestate](../engineering-invariants.md#publish-the-approved-patch-and-preserve-the-installed-prestate-separately).
- Router: `tests/test_workflow_rules.py` — description tests, shared role-matrix test and `test_role_first_forward_runner_injects_reviewed_classification`.
- Companion repository: `tests/test_workflow_rules.py` — standalone and role-matrix tests; `scripts/validate_templates.py` — entry rejection and Handed-off hash checks.
- Sync: `tests/test_cross_cli_sync.py` — `ScopedPlanSelectionTests`, `ScopedPlanTamperTests`, `ScopedTransactionTests`.

## Bounded adversarial checks

1. A typo-only request must not load the Router; explicit OpenSpec and explicit archive/distillation requests remain selectable. A separately explicit Git request is judged by its own authority, not denied merely because the edit is a typo.
2. A named defect with a diagnose-only request stops before implementation; a current request explicitly authorizing that same repair continues only within its existing boundaries.
3. Moving the role block while leaving the forward reader on SKILL.md must fail. Valid Handoff still reads the complete role block; standalone review must not regain it through a duplicate.
4. A dirty shared validator and an already-installed advanced baseline must not be whole-file staged or overwritten. Compare the exact publish candidate and the installation patch separately.
5. Codex-only verified receipts and 486 release-candidate tests must not be described as four-target verification or 506 release tests. Native model loading and token savings remain unverified.

## Implementation and delivery evidence boundary

- Router publication: `72ceac33c5b7f63c712566d7eb38b56d8a300bca`.
- Companion publication: `8074739271021a097f56b75222a3d83dcb54d3da`.
- Reviewed Codex-only plan SHA-256: `de2840a13dce3dae162ec7b93bf3c7a8a1f433ec47db31c13504d5235da550a5`.
- Installed Router SKILL.md SHA-256: `51a5d65d2cdc6a4c520fe3721849b46137407a23e7dd6f6f93bbb8d11d206375`.
- Installed Companion SKILL.md SHA-256: `e88e8a541c72f7ebc715402e9b48bce799f917ebf9405d30adb62bec9771d527`.
- Codex content/discovery validation and the verified receipt cover the selected installation, not a model session. The excluded three targets' 123 files were unchanged. Four-target verify-all was not claimed.
- These are historical delivery facts. Closeout documentation verification does not rerun or upgrade runtime acceptance.

## Fresh archive verification

The isolated publication candidate passed 486 repository tests with zero failures, errors or skips after learning promotion and archive materialization. The core validator also passed with python3 -S, quick_validate passed, and openspec validate --specs --strict --no-interactive reported one spec passed and zero failed. Only the three approved requirements changed in the canonical spec; original proposal, design and delta bytes were preserved in the archive, and no change tasks remain unchecked. This verification covers repository closeout, not new runtime acceptance.
