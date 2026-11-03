# Learning Candidate Card: Hanging states, completion deadlocks, and delegated review continuity

Change: `close-anti-drift-and-completion-deadlocks`, archived as
`openspec/changes/archive/2026-11-03-close-anti-drift-and-completion-deadlocks`.
Published commit `18c337c69417df8bb515fea4868d8611685d52f8` on `main`.

This card is the session distillation for resolving external review findings F1/F2 and user-authorized uninterrupted continuity.

```yaml
status: promoted
event_kind: correction
severity: high
scope: project-local
promotion_trigger: explicit-archive-distill
symptom: "Stop conditions referenced unrecorded task types and private numeric budgets, pre-existing debts caused infinite repair loops with completion contracts, and long tasks suffered polite interruption."
prior_assumption: "The agent could infer task-type changes without Gate 0 state, undefined numeric budgets would simply be ignored without explicit rules, completion contracts could unconditionally route FAIL to repair, and intermediate review required conversational pauses."
correction_or_evidence:
  - "SKILL.md and references/step-evidence-gate.md record task (VERIFY|DIAGNOSE|FIX|REVIEW) at Gate 0."
  - "SKILL.md defines explicit fallback for missing local numeric round budgets while keeping non-numeric stops active."
  - "references/completion-contract.md routes pre-existing debt to BLOCKED (blocker_owner: user) and subjects completion loops to SKILL.md's two-failure stop."
  - "SKILL.md, confirmation-lease.md, and approved-implementation-workflow.md enable uninterrupted progression upon delegated advisory review or closed-loop instruction."
  - "tests/test_workflow_rules.py verifies positive compliance and negative regressions."
generalized_invariant: "Hanging references, unrepairable debt, and delegated review continuity must resolve deterministically. Gate 0 binds state baselines, missing private thresholds fall back cleanly, pre-existing debt blocks without loops, and delegated review advances without redundant conversational pauses."
independent_reproductions: "External grok-cc architectural review F1, F2; user explicit instruction on delegated review and closed-loop continuity."
independence_rationale: "External static review and user-observed workflow friction are distinct independent sources."
duplicate_or_conflict_result: "Extends docs/engineering-invariants.md with section 13. Does not edit managed governance block or weaken Non-Negotiables."
target_artifacts:
  - docs/engineering-invariants.md
  - tests/test_workflow_rules.py
mechanical_enforcement: required
mechanical_enforcement_reason: "Gate 0 task type, pre-existing debt BLOCKED transition, two-failure bounds, and delegated review text have deterministic positive and negative unit test coverage in tests/test_workflow_rules.py."
verification:
  - "tests/test_workflow_rules.py:SkillIterationEntryTests verifies all four invariants and negative regressions."
  - "scripts/validate_core_gates.py and quick_validate.py report PASS."
review_result: pass
decision_owner: codex
decision_provenance: "2026-11-03: Session d353f057-9e21-47eb-8b88-c4f9bd5a7f1c reviewed and distilled F1/F2 resolution and delegated review continuity into engineering invariants."
```

Durable rule: [Hanging states, completion deadlocks, and delegated review continuity resolve deterministically](../engineering-invariants.md#hanging-states-completion-deadlocks-and-delegated-review-continuity-resolve-deterministically).

## 内容锚点

- `SKILL.md` Gate 0 一行式规范必须包含 `task: VERIFY|DIAGNOSE|FIX|REVIEW`。
- 数字轮次预算属于用户 File A 隐私，公开仓库不得写死具体数字，必须保留缺少数字预算时的跳过与物理兜底规则。
- 遇有既有缺陷（`OUT_OF_SCOPE_PREEXISTING_DEBT`），严禁在当前变更范围内自修复，必须转为 `BLOCKED`，交由用户决策。
- 收尾回环受两次失败即停约束，防止模型在收尾时因 completion contract 措辞产生无限活锁。
- 授权闭环推进或委托 grok-cc 顾问审查时，在审查通过后直接衔接下一切片，不插话询问。
