# Learning Candidate Card: Plan-anchored cohesive execution, lazy state, and commit-style parity

Change: `streamline-plan-anchored-execution`, archived as
`openspec/changes/archive/2026-11-04-streamline-plan-anchored-execution`.
Published commit `8a2ca6b11ebac2dd2387cd9cdbc76a74b90e3bf7` on `main`.

This card is the session distillation for streamlining plan-anchored execution, narrowing lazy state and review consolidation per external review, removing deprecated `grok-cc` references, and enforcing repository commit-message style parity.

```yaml
status: promoted
event_kind: correction
severity: medium
scope: project-local
promotion_trigger: explicit-archive-distill
symptom: "Multi-stage governance tasks suffered from duplicate OpenSpec/Superpowers planning, standalone JSON evidence sprawl (preflight/red-green/native-green), micro-step status.md SHA-256 self-invalidation loops, preloading 260 lines of cold-path recovery rules, stale grok-cc references, and a terse one-line English commit message that ignored repository git log conventions."
prior_assumption: "Every OpenSpec change needed a separate Superpowers plan and standalone preflight/TDD JSON files; verified_revision.inputs could include CHANGELOG.md and review reports; cold-path sections had to be split into a new file; and any Conventional Commit subject sufficed without checking git log."
correction_or_evidence:
  - "SKILL.md and references/approved-implementation-workflow.md unify four-anchor OpenSpec (design.md + tasks.md) with the executable Plan and waive standalone local preflight JSONs on a clean baseline."
  - "references/approved-implementation-workflow.md, step-evidence-gate.md, and completion-contract.md default single-slice work to a Single Cohesive Batch with inline RED-to-GREEN proof and a single consolidated Verification & Review report."
  - "SKILL.md and references/direct-change-rule.md allow three-condition localized bugfixes (failing-then-passing regression test, no external contract change, local diff scope) to use Direct Change without a pre-existing spec path."
  - "references/approved-implementation-workflow.md scopes lazy status.md creation to compact/standard while keeping approval-time creation for strict/self-evolution, excludes CHANGELOG.md/ledgers/historical reports from verified_revision.inputs, and marks cold-path sections in place via <!-- COLD_PATH_START."
  - "Active workflow references, specs, invariants, and tests remove deprecated grok-cc references."
  - "User correction on commit f4d2a33 replaced the one-line English commit message with the repository's established Chinese type(变更门禁): subject + structured bullet list in commit 8a2ca6b."
generalized_invariant: "Anchor at the ends (Four-Anchor Plan and full-diff + regression Final Review) and keep the middle free (coarse-grained cohesive batch, inline RED-to-GREEN proof, lazy status.md without metadata self-hashing, in-place cold-path marker), while inspecting git log before any authorized commit to preserve repository commit-message conventions."
independent_reproductions: "External agent architectural review of the 4-point optimization proposal; user architecture direction on anchor-at-ends execution, grok-cc deprecation, and explicit commit-message correction."
independence_rationale: "External static validator/blast-radius analysis and user operational corrections across execution and Git commit review are distinct independent sources."
duplicate_or_conflict_result: "Extends docs/engineering-invariants.md with section 14 and updates section 13 to remove grok-cc. Does not edit the managed governance block or weaken Non-Negotiables."
target_artifacts:
  - docs/engineering-invariants.md
  - tests/test_workflow_rules.py
mechanical_enforcement: required
mechanical_enforcement_reason: "Four-anchor unification, cohesive batch inline RED-to-GREEN proof, three-condition bugfix Direct Change, verified_revision.inputs exclusions, <!-- COLD_PATH_START marker, and grok-cc absence are deterministically enforced in tests/test_workflow_rules.py with positive assertions and negative mutation regressions. Commit message convention is covered by the adversarial Review scenario below because git commit messages are outside static file validation."
verification:
  - "tests/test_workflow_rules.py:SkillIterationEntryTests.test_streamline_plan_anchored_execution_invariants and test_delegated_review_and_closed_loop_continuity pass."
  - "scripts/validate_core_gates.py, scripts/validate_distribution.py, quick_validate.py, and all 520 unittests report PASS."
review_result: pass
decision_owner: codex
decision_provenance: "2026-11-04: Session 5565cd9a-ab2c-4ca0-b477-80d7c5ffbbcb archived and distilled streamline-plan-anchored-execution, external review refinements, grok-cc removal, and commit-style parity into engineering invariants."
```

Durable rule: [Plan-anchored cohesive execution, lazy state, and commit-style parity](../engineering-invariants.md#plan-anchored-cohesive-execution-lazy-state-and-commit-style-parity).

## Adversarial Review Scenario (Commit-Style Parity)

- **Setup**: An agent is authorized to run `git add`, `git commit`, and `git push` after modifying 10+ governance and specification files in this repository.
- **Wrong behavior**: The agent immediately runs `git commit -m "feat(workflow): short english summary"` without inspecting `git log -n 5`.
- **Required check**: Before running `git commit`, the agent inspects recent `git log` entries, observes the repository's `feat|docs(变更门禁): <中文标题>` + structured Chinese bullet-point body convention, and formats the commit message accordingly while staging only current-task files.
