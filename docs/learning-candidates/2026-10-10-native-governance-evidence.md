# Learning Candidate Card: Native Governance and Evidence Boundaries

Author: elvis. Change: `align-native-agent-governance`.

The promotion/review state below refers to the existing invariant target and its
regressions, accepted from independent Implementation Review r2. This new
classified provenance card still requires the current independent Final Review;
it cannot substitute for that gate or declare source-slice completion.

```yaml
status: promoted
event_kind: integrity
severity: high
scope: project-local
promotion_trigger: high-severity
symptom: >-
  Separate source/fixture reads could record a digest for bytes never consumed
  by a behavioral probe. A caller-named run root also violated the cleanup
  helper's ownership contract and could leave an unsuccessful probe lifecycle.
prior_assumption: >-
  Pathname re-reading was equivalent to hashing the observed instruction/input
  snapshot; successful case classification was sufficient before cleanup.
correction_or_evidence:
  - path: docs/review/2026-10-10-align-native-agent-governance-implementation.md
    sha256: 1af06f89a6b3cdc6a9a227f319f4991890fc05bdea9878c4ca9a49e3a82ca996
    summary: >-
      F1 and F5 independently reproduced real preparation/cleanup failures.
      Source replacement was intercepted before native process launch;
      it is not evidence of a model failure.
  - path: docs/review/2026-10-10-align-native-agent-governance-implementation-r2.md
    sha256: ff4a8a68aa8ca5c6eb9a9da497e7ea71ac0022c17650899eef6631dbe6958930
    summary: Independent corrected-source Review closed F1-F5 and reviewed the invariant target.
generalized_invariant: >-
  Governance and acceptance evidence retain their actual scope, identity and
  ownership. Hash the exact bytes consumed, reject hidden or misplaced policy,
  and publish probe success only after its required owned lifecycle succeeds.
  Portable/discovery parity cannot establish native loading or role authority.
independent_reproductions:
  - >-
    Distinct Implementation reviewer reproduced a real pre-launch source
    replacement that mismatched projected and recorded bytes, and a real
    directory cleanup rejection; see the first Review's F1/F5.
  - >-
    Author reproduced preparation replacement and actual directory lifecycle
    through deterministic regressions before the corrections. Only the process
    boundary was stubbed; no stub result was accepted as native behavior.
  - >-
    Independent corrected Implementation and Final reviewers reran the binding,
    lifecycle and real-validator regressions on the accepted source.
independence_rationale: >-
  The initial reviewer was a distinct Codex instance from the author and used
  separate isolated preparation/cleanup probes. The Final reviewer was distinct
  from both. Independent probes are not repeated paraphrases of a model answer.
duplicate_or_conflict_result: >-
  Extend the existing contracted native-consumption invariant section and its
  existing owner pointers. No duplicate global rule, new installer, native
  platform mutation or historical evidence rewrite is introduced.
target_artifacts:
  - path: docs/engineering-invariants.md
    sha256: f24f3f9cdc4e23f874fa900c477c27e22e8b3518b74e48b628ac980024589c1b
    section: Native consumption and evidence qualification stay scoped
  - path: references/local-instruction-checkpoint.md
    sha256: 11e9c8db28264eb638f44198d222885df4ecf6a01c532deddd4119b27b845132
    section: Native agent consumption
mechanical_enforcement: required
mechanical_enforcement_reason: >-
  Snapshot binding, owned cleanup, finite native events and owner-visible
  obligations have deterministic counterexamples; prose alone is insufficient.
verification:
  target_review:
    path: docs/review/2026-10-10-align-native-agent-governance-implementation-r2.md
    sha256: ff4a8a68aa8ca5c6eb9a9da497e7ea71ac0022c17650899eef6631dbe6958930
    result: pass
  regression_files:
    - path: tests/test_workflow_rules.py
      sha256: ba2e486af4d0ab0f0286e5561826208728e7d404ab96faf4716afcda27471a14
      tests: >-
        NativeAgentConsumptionTests, including exact source/fixture byte binding,
        owned cleanup failure/handler restoration and 34 owner-clause mutations.
    - path: tests/test_cross_cli_sync.py
      sha256: 4abec2ef2d907637efe8dbdb3fa5e8645222cb20dbaaba6fcde01d0a93930863
      tests: NativeConsumptionManagedRulesTests through real semantic/parity APIs.
  completed_source_verification:
    path: docs/review/2026-10-10-align-native-agent-governance-final-verification.json
    sha256: 90fb3b92f52738f9954e7537b615327c9b76014caa136ca4cf3fd2fbb47f97c6
    result: Unchanged-source full suites pass 492 tests in each parser mode.
  bounded_native_evidence:
    path: docs/review/2026-10-10-align-native-agent-governance-forward.json
    sha256: c15b4e52e8af47655af7384270fbde5edb077ac382671dcbb1ab0c43718da1cc
    scope: >-
      Final 7/7 native Codex projected-AGENTS classifications; not Skill-body
      loading, another entry, or reproduced pre-change model failure.
  provenance_review: Pending current independent Final Review of this new card.
review_result: pass
decision_owner: codex
decision_provenance: >-
  Bound control-plane instance align-native-root accepts the existing target
  promotion under the approved change, based on distinct Implementation Review
  r2. High severity is the acceptance-evidence integrity risk demonstrated by
  F5, not an invented native model or production failure. This card records that
  accepted target decision; its new provenance must pass Final Review before
  source-slice completion. No global, Git or native-adaptation authority follows.
```

Loading remains through `AGENTS.md` to the contracted engineering invariant and
SKILL's affected-instruction route to the native checkpoint. This card preserves
non-sensitive classification and provenance; it is not a second operating rule.
