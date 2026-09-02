# Superpowers Adapter

For schema 6 Review routing, carry all six concepts without abbreviation:
Review purpose, reviewer product, role, capability, independence, and authority.
The normative assignment and product/instance boundary live in
`references/agent-capability-routing.md`; this reference does not create a
second authority.

This adapter maps Superpowers artifact and permission defaults onto the
project's approved workflow. It does not weaken brainstorming, TDD, systematic
debugging, Review, worktree safety, or verification discipline.

## Phase-Aware Selective Invocation

Generic create/modify wording does not activate a sub-skill by itself. Gate 0
may record no applicable sub-skill for proposal drafting. Once a sub-skill is
selected, follow it completely; selective invocation never weakens its
HARD-GATE or discipline.

Concrete model identity does not grant authority or choose workflow weight.

## Router-Owned Method Selection

The Router normatively selects zero or more Superpowers methods for governed
work. A user-explicit `$superpowers:*` request chooses a method only; it grants
no workflow, business, Git, or completion authority. State-changing, Git, or
whole-task-completion work completes Gate 0 through exactly one applicable
Router before the method proceeds. If the workflow cannot load exactly one
applicable Router, it is `BLOCKED`.

Router-required child Skills remain eligible for native implicit matching as
defense in depth. Do not make them explicit-only until a supported runtime proves
native Router-to-child loading without shell/filesystem fallback or user
`$child` input. This contract is normative routing, not a claim that Codex
mechanically suppresses every unselected child.

When a selected child requests another phase, return to Router classification.
Each phase and Skill may be selected at most once for the bounded route;
unresolved or cyclic selection is `BLOCKED`. Every selected child retains its
complete rules and HARD-GATE behavior.

| Request | Route |
|---|---|
| Ordinary question | Direct answer or matching domain Skill; no Router or Superpowers meta-entry |
| Diagnose-only | Read-only domain diagnosis or `systematic-debugging`; stop and enter Router before any fix |
| Fully specified proposal-only | Router Gate 0; Router records Superpowers `none`, validates artifacts, and stops for approval |
| Material proposal ambiguity | Router selects brainstorming exactly once and preserves its HARD-GATE |
| Direct Change | Router selects debugging, TDD, and Review from cause and risk |
| Ordinary diff/Report/evidence Review | Companion Standalone Lightweight |
| Architecture, OpenSpec, authorization, or completion Review | Router Review-only |
| High-risk implementation | Router plus approved OpenSpec, plan, TDD, verification, and distinct Review |
| Whole-task completion | Router Completion Contract; child evidence cannot decide completion |
| User-explicit `$superpowers:*` | Respect the method request; state-changing/Git/completion scope enters Router first |

### Route Decision Record

Use this normative record when a routing probe or audit needs a stable,
machine-checkable decision. It does not grant authority beyond the route.

| Class | `route` | `result` | `selected_superpowers` | `state_change_allowed` | `git_authorized` | `completion_owner` |
|---|---|---|---|---:|---:|---|
| `ordinary_question` | `direct` | `answer` | `[]` | `false` | `false` | `none` |
| `diagnose_only` | `diagnose-only` | `stop-before-fix` | `["superpowers:systematic-debugging"]` | `false` | `false` | `none` |
| `proposal_only` | `openspec-proposal` | `stop-for-approval` | `[]` | `false` | `false` | `router` |
| `material_ambiguity` | `openspec-proposal` | `needs-user-decision` | `["superpowers:brainstorming"]` | `false` | `false` | `router` |
| `direct_change` | `direct-change` | `implementation-gated` | `["superpowers:systematic-debugging","superpowers:test-driven-development"]` | `true` | `false` | `router` |
| `ordinary_review` | `companion-standalone` | `review` | `[]` | `false` | `false` | `none` |
| `architecture_review` | `router-review-only` | `review` | `[]` | `false` | `false` | `router` |
| `high_risk_implementation` | `approved-implementation` | `implementation-gated` | `["superpowers:writing-plans","superpowers:test-driven-development","superpowers:requesting-code-review","superpowers:verification-before-completion"]` | `true` | `false` | `router` |
| `whole_task_completion` | `router-completion` | `completion-evaluation` | `["superpowers:verification-before-completion"]` | `false` | `false` | `router` |
| `explicit_method_no_git` | `router-gate-0` | `blocked` | `["superpowers:finishing-a-development-branch"]` | `false` | `false` | `router` |
| `missing_router` | `blocked` | `blocked` | `["superpowers:test-driven-development"]` | `false` | `false` | `none` |
| `duplicate_router` | `blocked` | `blocked` | `["superpowers:test-driven-development"]` | `false` | `false` | `none` |
| `cyclic_phase` | `router-gate-0` | `blocked` | `["fixture:child-a","fixture:child-b"]` | `false` | `false` | `router` |

`selected_superpowers` records the exact canonical methods selected or
explicitly requested for the bounded route, even when authority blocks a
requested method. Direct Change records its current cause methods only;
approved high-risk implementation records its required lifecycle set.
`state_change_allowed` means the request may enter implementation after its
remaining gates and is true only for Direct Change and explicitly approved
high-risk implementation. `git_authorized` reflects current explicit Git
authority. `completion_owner` is `router` only when exactly one applicable
Router owns the route; bypass and missing/duplicate Router routes use `none`.
Router Gate 0 owns a cyclic route, but its result is `blocked`.

## Single OpenSpec Design Contract

When OpenSpec is required, brainstorming still explores intent, alternatives,
and trade-offs before implementation, but its design output and user-review
gate map to the **single OpenSpec design contract**: the same proposal/design,
change-id, and approval. Do not create, commit, or approve a second
`docs/superpowers/specs/` artifact for the same decision.

A scoped Direct Change that restores an already-defined behavior without a
creative design decision does not need a duplicate brainstorming artifact.
Ambiguity or a new behavior choice returns to brainstorming/OpenSpec.

## Executable Plan And Preflight Review

`superpowers:writing-plans` produces executable steps after approval. Before
implementation or external dispatch, run **Preflight Review** against the
current artifact revision:

- contract/spec coverage and absence of placeholders;
- allowed files, boundaries, production wiring, and acceptance;
- exact verification commands, evidence profile, rollback, and stop conditions;
- branch/worktree decision and unauthorized Git or duplicate-design steps.

Preflight uses only `PASS` or `BLOCKED`. Apply the bounded convergence contract
in `references/approved-implementation-workflow.md`: first lineage Review uses
`FULL_PREFLIGHT`; an unchanged-boundary correction may use `FOCUSED_RECHECK`
only with exact reviewer identity matching the immutable parent Review and
remaining distinct from author/executor, valid current whole-file and
parent-anchored historical revision bindings, mechanical self-check, and a declared correction-only
diff. Non-convergence routes outside Review through
`CONTROL_PLANE_ADJUDICATION`; it does not add a mode or state. Any actionable
finding is `BLOCKED` and does not authorize execution. Preflight PASS authorizes
execution only; it is not Implementation Review, Final Review, or completion
evidence. An unchanged artifact revision does not repeat ceremony.

Use `superpowers:subagent-driven-development` for suitable independent tasks in
the current session, or `superpowers:executing-plans` for a separate execution
session. An explicitly named external executor instead uses the Handoff-backed
brief governor. Do not create two execution governors for the same slice.

## Git And Worktree Permission

A Superpowers plan **never grants Git permission**. Remove `git add`,
`git commit`, `git push`, `git reset`, `git clean`, or equivalent publication
steps unless the current user explicitly authorizes those commands for this
task. Record any removal or authorization in Preflight Review.

Use a worktree when the selected execution skill or repository rules require
isolation. Never start implementation on `main`/`master` merely because a plan
mentions it; current-branch use requires explicit user consent.

## Granularity And Completion

Superpowers may retain RED/GREEN implementation actions inside a plan, but Step
Evidence Gate and Review operate on a complete business slice or explicit risk
milestone, not every two-to-five-minute action. Review findings restart the
appropriate fix/verification/Review loop. `verification-before-completion`
remains mandatory after final Review and OpenSpec closeout.

## Capability Profiles And Confirmation Reuse

A Superpowers execution style does not grant decision authority. Bind work to
`control-plane-high`, `cohesive-medium`, or `mechanical-low` and escalate when a
profile reaches its ceiling. Platform sandbox/prefix permission is only the tool
layer; it cannot satisfy workflow scope or business/production authorization.
An unchanged Confirmation Lease avoids duplicate prompts for safe commands and
the same finding's fix/verify/Review loop. Material revision, scope, risk,
production, credential, external-effect, destructive-Git, evidence, or user
changes invalidate the lease.
