# Approved Implementation Workflow

For schema 6 Review routing, carry all six concepts without abbreviation:
Review purpose, reviewer product, role, capability, independence, and authority.
The normative assignment and product/instance boundary live in
`references/agent-capability-routing.md`; this reference does not create a
second authority.

Use after an OpenSpec proposal is approved, or after Direct Change has
classified and authorized an implementation that will use an external agent.

## OpenSpec And Superpowers Boundary

1. OpenSpec proposal/design/spec deltas are the approved change contract.
2. For OpenSpec-required work, that approval is the single design approval and
   does not require a duplicate `docs/superpowers/specs/` artifact or approval.
3. After approval, invoke `superpowers:writing-plans` for multi-step work and
   save the executable plan under the project-preferred path.
4. OpenSpec-backed work uses
   `openspec/changes/<change-id>/tasks.md` to track contract progress for that
   change. Direct Change reuses existing scoped Plan/Status/Handoff/equivalent
   state for continuity and does not require OpenSpec tasks.md. Continuity must
   not create a new OpenSpec change or second ledger. No global rule requires
   every work item to have OpenSpec tasks.md. Plan checkboxes are static
   execution steps only and never canonical task state.
5. A compact Direct Change needs no large plan unless complexity justifies it.

Follow `references/superpowers-adapter.md`; a generated plan does not grant Git
permission and must not create a second design approval.

## Plan And Evidence Granularity

- Group work by complete business slice, not by file count or technical layer.
- Include exact files, test commands, evidence profile, batch profile, negative
  searches, acceptance, rollback, and stop conditions.
- Apply Step Evidence Gate before and after each business slice or risk
  milestone, not every TDD micro-step. TDD owns RED/GREEN inside the slice.
- Use `superpowers:systematic-debugging` before changing unexplained failures.
- Use `superpowers:test-driven-development` for behavior changes, not for a
  test-only assertion of already-defined behavior.

## Plan And Brief Preflight Review

Before inline implementation or external dispatch, Review the current Plan or
Brief revision for contract coverage, placeholders, allowed scope, production
wiring where applicable, acceptance, exact verification commands, evidence
profile, rollback/stop conditions, branch/worktree choice, and Git authority.

- `compact` may use a focused inline Preflight Review.
- `standard` and `strict` require a distinct critical pass.
- Preflight uses only `PASS` or `BLOCKED`. Any actionable finding is
  `BLOCKED`; revise the artifact and Review it again. Reserve `FAIL` for
  implementation or post-implementation Review, where executed behavior can
  actually be wrong.
- Preflight `PASS` authorizes execution only; it is not design re-approval,
  implementation Review, or completion evidence.
- Rerun only when the artifact revision changes.

## Authorized Execution Continuity

During already authorized implementation, when approved tasks remain Pending, no
Blocker exists, and no new human decision is required, continue with the next
approved task. Completing a subtask is not a stop condition and must not trigger
a continue prompt. An advancing turn with executable pending work performs at
least one task-related action: read/search required code, edit, test/build,
verify, collect evidence, or update existing canonical state. A summary,
recommendation, or future plan alone is not progress.

Stop only when all approved tasks are complete, state is `BLOCKED`, a new
product, business, or architecture decision is required, permission,
credentials, or required resources are missing, the next operation is
high-risk, irreversible, or outside the approved scope, or the user explicitly
pauses or cancels.

After Context Compaction, session recovery, a model or agent switch, or `继续`,
recover from the canonical Plan, Status, Handoff, or equivalent state: goal,
current task, Pending tasks, Blocker, Acceptance, and Verification. Do not infer
the next action from the previous chat response. Do not create `.agent/goal.md`,
a Task Manager, or a second state system. Code written is progress, not Done.
Existing Acceptance, Test, Build, Verification, and Evidence rules, together
with `references/completion-contract.md`, remain the only Done criteria.

## Conditional Minimal Implementation

Use this lightweight judgment only when a proposed implementation or Review fix
would materially add an abstraction, component, layer, dependency, or wider
scope. Establish the approved Need, then choose the first adequate option:

```text
Need
-> Repository Reuse
-> Stdlib
-> Platform Native
-> Existing Dependency
-> Small Local Implementation
-> New Abstraction
```

An earlier project-consistent option wins when it satisfies the approved need.
This does not run for every ordinary Bugfix and creates no mandatory checklist,
artifact, gate, or output. It does not automatically select
`backend-architecture-review`; that Skill remains explicit-intent-only.

## Review/Fix Convergence

Keep the existing `Review FAIL -> Fix -> Verify -> Review` loop. Ordinary
first-pass findings continue through the existing same-scope loop. Before
another retry, treat the loop as non-converging when evidence shows that:

- the same finding recurs after a verified fix;
- a fix-induced regression recurs;
- multiple Review rounds do not converge;
- reviewers materially conflict on the core approach;
- the root problem may be an architecture or requirements boundary;
- fix scope keeps expanding; or
- a small need keeps accumulating an abstraction, layer, component, or dependency.

When a signal applies, stop before another widening fix and return `BLOCKED` to
`control-plane-high` through the existing Review/control-plane mechanism. Record
the blocker owner and resume condition, then re-evaluate the original approved
need, boundary, and smallest adequate correction. Resume the normal same-scope
loop only after that boundary decision resolves the blocker.

Do not create an `ESCALATED` state, Finding lifecycle, Quality Gate, Task
Contract, second state system, new multi-agent flow, or new final authority.

## Inline Implementation

1. Execute the plan inline with TDD/debugging as applicable.
2. Run slice verification.
3. For `compact`, run a focused diff/self-review.
4. For `standard` or `strict` inline implementation, invoke
   `superpowers:requesting-code-review` after implementation and before final
   verification. Review PASS is required.
5. Any finding returns to the same slice: fix, refresh verification, and Review
   again. Do not carry unresolved findings into the next slice.

## External Implementation

1. Create one schema-version-6 Handoff Contract at canonical `status.md`, with
   immutable control-plane/executor assignments and the exact immutable
   `reviewer_assignment`, decision provenance, and a Confirmation Lease. Before
   schema-6 deployment, active schema-4/schema-5 contracts MUST finish under
   their old runtime; they MUST NOT be migrated, resumed after cutover, or used
   as current transition authority.
2. A low-risk Direct Change may use `compact`/`single`; approved public/API
   restoration remains `strict`, and OpenSpec-backed work uses its approved
   evidence and batch profiles.
3. Hand Brief/Report/Review attempts to `codex-brief-antigravity-review`.
4. The external Review is the batch code-review gate; do not duplicate it with
   a second Superpowers review for the same batch.
5. `FAIL` or `BLOCKED` stays on the same batch and must re-enter Review with
   fresh attempt evidence.
6. Non-final `PASS` advances one batch. Final `PASS` sets
   `awaiting-final-verification` and returns ownership to this router.
7. Brief and Report carry the same execution-revision canonical SHA-256. A
   mismatch blocks Review and batch promotion.
8. Every evidence-bearing transition validates its proposed status against the
   actual prior canonical status before replacement. New schema-2 manifests bind
   product/instance/role/profile plus result/change/batch/attempt/source
   revision/SHA-256. Standard/strict executor and reviewer instance IDs differ,
   even for the same product. Compact binds `reviewer_assignment` to the bound
   control-plane identity, keeps it distinct from the executor, and requires the
   top-level non-blank not-applicable reason. Historical schema-4/schema-5
   contracts and their evidence are immutable.
9. Manual copy/paste of a state-changing standard/strict Brief does not downgrade
   governance. Validate the same Handoff and evidence chain before promotion.

## Final Completion

After all inline slices pass, or after external handback, stop using this
route-specific workflow as completion authority and evaluate
`references/completion-contract.md`. This section defines no independent
whole-task checklist.

## OpenSpec closeout

OpenSpec closeout eligibility, reconciliation, archival validation, and active
owner/resume outcomes are governed exclusively by
`references/completion-contract.md`. This section defines no second closeout
checklist.

For OpenSpec-backed multi-step work, skip the Superpowers plan only when the
user explicitly says to skip it. Compact Direct Change does not require a large
plan by default. Never skip final verification or Review.

## Tiered Authorization And High Review

Route capability through `agent-capability-routing.md`. Platform permission,
workflow scope, and business/production authorization are independent layers.
Reuse an unchanged Confirmation Lease for safe checks and same-finding loops;
request a new user decision for any invalidating production, risk, scope,
credential, external-effect, destructive-Git, evidence, or user-decision change.

For standard/strict work, High Review inspects actual files and the complete
diff, traces copy/transform/production wiring and every behavior claim to its
mechanism, reruns critical evidence, and adds an independent adversarial or real
business-chain probe. Executor PASS cannot substitute for this Review.
