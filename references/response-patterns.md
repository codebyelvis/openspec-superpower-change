# Response Patterns

## Review-only requests

1. State that no files will be changed.
2. State whether the described change would require OpenSpec if implemented.
3. Summarize unclear terms, risks, missing artifacts, approval gates, and recommendations.
4. If architecture Review also needs a handoff summary, include it as a
   secondary output without treating it as a standalone governed Brief.
5. For standalone prompt wording or ordinary diff/Report review, route to
   `codex-brief-antigravity-review` instead of creating change-gate artifacts.

For schema 6, every Review request states Review purpose, reviewer product,
role, capability, independence, and authority. Resolve the destination in this
order: existing canonical assignment; a product explicitly selected by the user
when eligible; one concrete eligible product recommended by the control plane;
otherwise `BLOCKED`. The phrases “another agent”, “independent agent”, and
“another model” are unresolved when they are the only destination.

<!-- ROLE_FIRST_REVIEW_CLASSIFICATION_START -->
Use this exact classification before selecting a product:

- A Review that decides whether implementation, execution, runtime planning,
  promotion, archive, or completion may proceed is gate-bearing: use role
  `independent-reviewer`, profile `control-plane-high`, distinct-instance
  independence, and authority `governed-review-evidence`.
- A standalone Review that explicitly does not decide a gate is advisory:
  preserve any eligible user-selected product, use role `advisory-reviewer`,
  profile `control-plane-high`, advisory-not-gate-bearing independence, and
  authority `advisory-input`.
- `cohesive-medium` and `mechanical-low` are executor/evidence-collection
  profiles, not Review profiles.
- For standalone prompt or recommendation wording, a request to open or name a
  new distinct reviewer instance remains actionable after all six assignment
  concepts are resolved; do not infer unavailability merely because a concrete
  instance ID or open window is not yet supplied.
- Return `BLOCKED` only when the request explicitly says no eligible distinct
  instance exists or insists on reusing an implementation instance.
- When a required distinct reviewer instance is unavailable because the user
  must open or provide one, return `BLOCKED` with `blocker_owner: user` and a
  non-blank resume condition.
<!-- ROLE_FIRST_REVIEW_CLASSIFICATION_END -->

Valid concise example:

Review purpose: inspect the current implementation plan and decide PASS or BLOCKED; reviewer product: codex; role: independent-reviewer; capability: control-plane-high; independence: a user-opened new-window instance distinct from the plan author and executor; authority: governed Review evidence only.

## Discovery-first requests

1. State that Phase 0 discovery is needed and why.
2. Read existing glossary, ADRs, code, and relevant docs.
3. Ask one focused question at a time with a recommended answer.
4. Update glossary or propose ADRs only when decisions crystallize.
5. Continue to OpenSpec once language and boundaries are stable enough.

## OpenSpec-required implementation requests

1. State that the request requires OpenSpec.
2. Say implementation is blocked pending proposal approval.
3. Use Discovery First if language or boundaries are unclear.
4. Create or update the required OpenSpec artifacts.
5. Run strict validation.
6. Present the proposal summary and wait for user approval.
7. After approval, create the Superpowers plan before implementation.
8. Include Step Evidence Gate checkpoints in the implementation plan.
9. When the plan is saved, provide its path and ask whether to execute inline or with subagents.

## Direct change requests

1. State that OpenSpec is not required and briefly why.
2. Apply the profile-appropriate Step Evidence Gate before editing when the
   direct change is gated. Low-risk Direct Change normally uses `compact`;
   approved public/API restoration remains `strict`.
3. Use TDD or systematic debugging as applicable, then implement the scoped change.
4. Run targeted official verification.
5. For gated direct changes, report results at the selected evidence profile.
6. Run focused diff/self-review; findings return to fix and re-verification.
7. Report changed files, tests, Review result, and verification evidence.

Before Direct Change implementation, Preflight Review the scoped execution
outline when it is more than a non-behavioral micro edit.

## Token budget control

- If user requests a shorter output, default to compact structure + one-line
  conclusion.
- Allowed compressed content:
  - Gate 0 summary
  - discovery findings list
  - actionable findings with file+位置级别
  - verification command list
- Forbidden compression:
  - 省略审计边界、openSpec/superpowers 切换依据或 `BLOCKED` 原因
  - 省略证据角色、结果、文件路径或哈希的最小闭环字段
  - 将 `PASS`/`FAIL`/`BLOCKED` 的语义替换为模糊描述
  - 用 caveman 语气替代 OpenSpec、handoff 或 final-review 的结构化文本

### Legacy request-scoped brevity

Requests for `少 token/更短/更精简/像 caveman 说` enable request-scoped compression for the current request.
This does not activate or persist `governed-caveman-lite`.
Only `OpenSpec 精简模式` activates the named conversation profile.
Legacy brevity remains subject to the same protected-surface rules below; it cannot omit governance or safety content.

### Governed Caveman Lite

The built-in `governed-caveman-lite` profile does not activate by default.
Enable it with `OpenSpec 精简模式：<任务>`, or send `OpenSpec 精简模式` before the task.
While active, use concise professional full sentences without filler, repetition, fragment-heavy prose, or unexplained abbreviations.

It remains active for the current conversation until disabled or the conversation ends.
Disable it with `OpenSpec 正常模式`.
A new conversation starts in normal output mode and creates no account, repository, or runtime preference.
The latest explicit OpenSpec mode command controls Router prose, so normal mode wins even after a prior Caveman-style instruction.

It is presentation state only, never invokes or delegates to a separate `caveman` skill, and works when one is unavailable.
It does not change routing, approval, evidence, Review, verification, completion, Git, or publication authority.

Compression may shorten ordinary response prose only. Protected content remains structurally complete:

- Gate 0 and every mandatory governance-step or approval field;
- OpenSpec artifacts and Superpowers implementation plans;
- Handoff/evidence artifacts and canonical state transitions;
- PASS/FAIL/BLOCKED, final verification, and final Review;
- critical commands, rollback instructions, security warnings, destructive confirmations, and sensitive-data handling.

Governance output keeps every required field and ordering constraint present; governance clarity and safety override compression.

## Gate 0 pattern

Use before any state-changing action:

1. Mode: state the active mode.
2. References read: list the exact references and why they are sufficient.
3. OpenSpec decision: yes/no/uncertain with one-line reason.
4. Required Superpowers: list required sub-skills or state none.
5. Risk and confirmation: state risk level, next action, and whether user confirmation is required.

For a non-behavioral micro change, combine these fields into one concise line.

## Implementation blocked by gate

1. State the blocking gate.
2. State what evidence, approval, reference, or decision is missing.
3. State the safest next action.
4. Do not modify files or run state-changing commands until the gate clears.

## Interrupted / dirty diff audit pattern

When interrupted due to process concerns:

1. Stop implementation immediately.
2. List files changed before interruption.
3. Mark each change as validated, unvalidated, or partial.
4. Recommend revert, keep, or park for each file.
5. State that no further implementation will happen until the user confirms.

## Self-evolution review draft pattern

For Major self-evolution before approval:

1. State that Self-Evolution mode is active and Major.
2. Provide or update a review draft plan, not implementation.
3. Include affected files, exact rule snippets, validation, forward-test, and rollback path.
4. Stop for review/approval before editing the skill.

## Completion pattern

Use `references/completion-contract.md` as the only normative whole-task
checklist. The response reports its outcome: final Review result and evidence,
fresh final verification commands/results, reconciliation and required runtime
sync status, accepted residual risks, and whether completion is allowed. A
`FAIL` or `BLOCKED` outcome is reported as such and returns to correction or its
recorded resume condition.
