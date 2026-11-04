# Tasks: streamline-plan-anchored-execution

## 1. Cohesive Batch: Contract, Rules, and Regression Suite

- [x] 1.1 Create and validate the OpenSpec contract `streamline-plan-anchored-execution` (`openspec validate streamline-plan-anchored-execution --strict`).
- [x] 1.2 Add focused RED regression test in `tests/test_workflow_rules.py` covering four-anchor OpenSpec/Plan unification, inline RED-to-GREEN proof without standalone intermediate JSON bloat, three-condition bugfix Direct Change, lazy `status.md` / clean `verified_revision.inputs` exclusions, and hot/cold-path reading boundary.
- [x] 1.3 Update `SKILL.md`, `references/approved-implementation-workflow.md`, `references/direct-change-rule.md`, `references/step-evidence-gate.md`, and `references/completion-contract.md` to turn the new regression test GREEN while preserving all existing validator and unittest invariants.
- [x] 1.4 Rebuild generated distribution/skill adapters if applicable and run `quick_validate.py`, `scripts/validate_core_gates.py .`, and `python3 -m unittest discover -s tests -v`.
- [x] 1.5 Perform complete-diff Review, verify clean scope, and clean up temporary pre-edit backup.
