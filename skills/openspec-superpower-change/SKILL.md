---
name: openspec-superpower-change
description: "Use for file/behavior changes, change classification, OpenSpec/Direct Change routing, evidence-based completion, archive/distillation, or skill self-evolution. Excludes ordinary questions, standalone wording/read-only diff review, and valid handed-off batches."
---

# OpenSpec + Superpowers Change Gate

Project-level change gate: classify the request, protect approval boundaries,
select implementation discipline, and own evidence-based completion.
Ordinary questions and read-only diagnosis do not enter implementation.

## Mandatory Entry Gate

Before edits, state-changing commands, proposal creation or implementation,
record Gate 0: mode and references read; OpenSpec decision and reason; required
Superpowers methods (or none); risk/evidence profile, next action and whether
confirmation is required. Inspection-only reads may establish classification.

An obvious local reversible change outside protected boundaries uses one line
for all Gate 0 facts. Read applicable local instructions and the current task's
code/docs; do not load the repository, all references or a whole workflow bundle.
Uncertain OpenSpec classification uses `references/openspec-decision-rule.md`.

## Routing Boundary

| Current request or decision | Read / route |
|---|---|
| Clear typo, formatting, comment, non-contractual docs or localized internal restoration | `references/direct-change-rule.md` |
| Behavioral slice evidence | `references/step-evidence-gate.md` |
| OpenSpec boundary or uncertain contract impact | `references/openspec-decision-rule.md`; when required, `references/proposal-workflow.md` |
| Approved implementation, including unchanged continuation | Existing canonical Plan/Status and `references/approved-implementation-workflow.md` |
| Select implementation methods for the current phase | `references/superpowers-adapter.md` |
| Unclear request mode or domain language | `references/request-modes.md`; affected local/domain instructions use `references/local-instruction-checkpoint.md` |
| Review architecture, OpenSpec need, authority or whole-task completion | This Router; `references/request-modes.md` |
| Explicit backend architecture Review, without a fix | `backend-architecture-review`, read-only bounded evidence |
| Standalone wording or ordinary read-only diff/Report/evidence Review | `codex-brief-antigravity-review` / standalone |
| Execute, resume or review a valid handed-off batch | `codex-brief-antigravity-review` / handed-off, taking routing priority |
| Create an external execution Handoff | `references/approved-implementation-workflow.md`, `references/handoff-contract.md`, `references/agent-capability-routing.md`, `references/confirmation-lease.md` |
| Assign a reviewer or decide capability/authority | `references/agent-capability-routing.md` |
| Edit this skill | `references/self-evolution-rule.md`; required behavioral evidence uses `references/step-evidence-gate.md` |
| Correction/Review history or explicit archive and distill request | `references/project-learning-closeout.md`; candidate classification uses `references/learning-candidate-pipeline.md` |
| Source/runtime sync | `references/sync-checklist.md`; portable changes also use `references/cross-cli-sync.md` |
| Requested output mode or response template | `references/response-patterns.md` |
| Whole-task completion | `references/completion-contract.md`, at completion rather than implementation entry |

Read the matching rows only when their decisions arise; do not accumulate rows
merely because a request contains "fix", "continue" or "Self-Evolution".
Reuse already-read unchanged rules and current evidence after continuation.
“Review and fix” is state-changing Router work, not Review-only. Generic
Bugfix/Diff/Plan/acceptance Review does not select the backend specialist.
Specialists provide bounded evidence, never canonical transitions or completion.

## OpenSpec Boundary

OpenSpec is required for new functionality, architecture or pattern changes,
public/operator-visible behavior, security, migrations, API/schema/data
lifecycle, broad refactors, runtime control flow, routing or workflow lifecycle.
A skill's trigger, routing, required artifact, transition, evidence or completion
rule is workflow behavior. "Small", reversible or low-risk does not waive this
boundary. Editorial wording that changes none of those contracts may use Direct Change.

Localized internal restoration, small config-only work without protected effects,
typo/comment/formatting, non-contractual docs and existing-behavior tests may use
Direct Change. Public/user/operator-visible restoration requires an approved
existing spec or equivalent project-authoritative contract, its exact path in
Gate 0, and no contract, schema, compatibility or lifecycle change; otherwise
OpenSpec is required. This exception does not lower the evidence profile.

## Implementation And Closure

For compact local Direct Change, follow its rule: minimum edit, relevant required
checks and focused inline diff/self-review. Behavioral fixes retain regression
evidence and compact business-slice signoff. A separate Plan, Preflight or full
TDD cycle is not universally required for this bounded path.

After classification and authorization, infer the current goal from the request
and prior context, then keep going until that goal is done. Treat "help me",
"can you", and "I want to" as instructions to do the work. Do not stop at
acknowledging capability, proposing a plan, or asking whether to continue
already authorized same-scope work. Ordinary questions and read-only diagnosis
still do not enter implementation.

Before asking for approval or a clarifying question, finish the already
authorized work that makes the next step concrete and reviewable. The user
approves a concrete result. Git writes, production, publication, external
writes, and destructive actions still stop at existing boundaries. Do not
invent extra warnings, disclaimers, or approval checklists from hypothetical
risk.

For approved work, continue safe same-scope reads, edits, relevant local checks
and fixes for failures introduced by this change without stepwise confirmation.
Reuse completed Plan/Preflight and unaffected evidence; retain pending required
gates. Stop for scope/protected-boundary changes, an explicit approval boundary,
production/credential/destructive or separately authorized external actions,
Git writes, conflicting contracts or missing required evidence.

Superpowers methods are selected by current phase and actual unresolved
decisions, not generic create/modify metadata. Once selected, preserve their
complete gates. Domain discovery is for affected terms or unresolved material
choices. Model identity or version grants no authority and selects no process weight.

Whole-task closure follows `references/completion-contract.md`. No second
completion checklist lives here. An external batch PASS means
`awaiting-final-verification`, not task completion.

## Capability And Evidence Profiles

Use `compact` for low-risk local work; `standard` retains distinct Review;
`strict` retains real evidence and explicit business gates for protected
effects. Definitions, signoff and required checks live in
`references/step-evidence-gate.md`; capability/assignment rules live in
`references/agent-capability-routing.md`. Do not downgrade an existing profile
to take a shortcut.

## Self-Evolution

Classify the actual change using `references/self-evolution-rule.md`.
Major changes require the specific approved OpenSpec contract, structured backup,
RED/GREEN forward-test, required validation, Review and applicable runtime sync.
The label alone does not activate unrelated implementation phases.

The existing `governed-caveman-lite` presentation controls
(`OpenSpec 精简模式` / `OpenSpec 正常模式`) and legacy request-scoped brevity
remain in `references/response-patterns.md`; no new mode is introduced.

## Non-Negotiables

- Do not let `CONTEXT.md` replace OpenSpec artifacts.
- Do not let required project learning remain only in chat, Review output, or
  prose-only context when deterministic regression enforcement is practical.
- Do not let OpenSpec `tasks.md` replace a Superpowers implementation plan.
- Do not use Superpowers planning to bypass OpenSpec approval.
- Do not implement OpenSpec-required work before approval.
- Do not gate every TDD micro-step; do not skip the business-slice evidence gate.
- Do not advance with `FAIL`, `BLOCKED`, stale evidence, or unresolved findings.
- Do not claim completion without fresh verification evidence and Review PASS.
- Do not accept empty critical commands, blank blocker details, evidence-free
  external PASS, or an atomic final-verification/final-Review completion update.
- New schema-6 external artifacts carry the exact immutable
  `reviewer_assignment`; schema-2 evidence binds product, instance, role,
  capability profile, result, change, batch, attempt, and source canonical
  revision/SHA-256 back to that parent assignment. Historical schema-4/schema-5
  contracts and their evidence remain immutable legacy history. Runtime
  `complete` validation requires the actual previous status.
- The bound Codex control-plane instance is the only decision owner; executor or
  reviewer output cannot self-authorize a transition or final completion.
- Platform/tool permission never substitutes for OpenSpec, production, archive,
  promotion, release, destructive Git, or another user-owned authorization.
- Do not claim a portable global skill optimization complete while any declared
  required Codex, Pi, Antigravity CLI, or Grok CLI target is stale or unverified.
- Do not duplicate mutable Handoff Contract blocks outside canonical `status.md`.
- Self-evolution cannot weaken approval, evidence, review, verification, or
  user-control boundaries.
- The user's explicit current instruction on task goal, scope, prose, whether to
  continue, and whether to skip extra polite confirmation takes precedence over
  this skill's presentation defaults. It does not waive OpenSpec boundaries,
  production, credential, or destructive actions, unauthorized Git writes, the
  Completion Contract, evidence gates, schema-6 control-plane ownership, or
  user-control boundaries. When the user asks for a protected change, follow the
  existing OpenSpec or approval path and name the blocking rule.
- When this skill requires permission, confirmation, leaving work unfinished, or
  diverging from the user's intent, name the exact file path, quote the relevant
  instruction, say whether that is a rule or your interpretation, and state the
  next step.
- Never run `git add`, `git commit`, `git reset`, or `git clean` unless the user
  explicitly commands it.
- Do not push without explicit user approval.
