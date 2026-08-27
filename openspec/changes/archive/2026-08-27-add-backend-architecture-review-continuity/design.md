# Design: add-backend-architecture-review-continuity

## Context

`SKILL.md` currently routes architecture Review to the Router's Review-only
mode. That preserves authority but does not isolate backend-specific judgment,
and its broad wording cannot distinguish an explicit architecture request from
ordinary Diff/Bugfix/Plan Review. `references/approved-implementation-workflow.md`
already defines approval, Plan Preflight, implementation, verification, Review,
and final handback, but does not state that authorized pending work continues
until a legal stop condition occurs.

Targeted source review covered only the requested upstream files:

- `wshobson/agents`: backend architect, architecture reviewer (current file name
  `architect-review.md`), API design principles, architecture patterns, and
  microservices patterns;
- `github/awesome-copilot`: `SE: Architect`, `api-architect`, and focused
  architecture review/blueprint guidance.

Useful judgment dimensions are distilled. Their proactive orchestration,
implementation, mandatory document generation, fixed layer recipes, framework
selection, and full-system planning workflows are deliberately excluded.

## Decisions

### 1. Independent, minimal Skill source

Create `../backend-architecture-review` as an independent source tree with only:

```text
SKILL.md
README.md
references/review-dimensions.md
tests-or-examples/trigger-cases.md
```

Initialize local Git with branch `main`. Do not stage, commit, add remotes, push,
publish, or place the source under the Router repository. The source has no
imports, copied files, shared mutable state, or runtime dependency on the Router.

Install one absolute discovery symlink named `backend-architecture-review` in
each required Codex, Pi, Antigravity CLI, and Grok CLI Skill root. Every link
must have an absent reviewed pre-state, resolve exactly to the sibling source,
and pass Skill validation. This is local installation, not remote publication;
the links add no source copy or Router-manifest ownership.

### 2. Explicit-intent-only trigger

The metadata and body require an explicit backend architecture Review intent,
including architecture/design plus performance/stability, service/module
boundaries, API/call chain/transaction boundaries, or over-design analysis.

Generic `Review`, Diff, Bugfix, acceptance, and Plan requests are explicit
negative cases. A combined “architecture Review and fix” remains
state-changing Router work; the specialist may supply read-only findings but
cannot implement.

### 3. Local Review verdict, not governance state

The specialist returns only:

```text
Verdict: PASS / NEEDS_CHANGE / BLOCKED
```

`PASS` means no material architecture change is required. `NEEDS_CHANGE` means
one evidenced architecture defect requires correction. `BLOCKED` means the
review lacks necessary code, constraints, or decision input. These are local
specialist verdicts, never Router canonical `PASS`/`FAIL`/`BLOCKED` transitions.

Findings are ordered `Critical`, `Important`, then `Suggestion`; empty sections
are omitted. Suggestions do not prevent `PASS`. Reasonable simple designs pass
quickly, and every finding prefers the smallest project-consistent correction.

### 4. Seven bounded judgment dimensions

The Skill checks only:

1. architecture and responsibility boundaries;
2. interfaces and contracts;
3. dependencies and call chains;
4. data ownership and transaction boundaries;
5. performance and reliability;
6. evolution and complexity;
7. consistency with actual project code and constraints.

It reads real project evidence before applying patterns. It does not force Clean
Architecture, DDD, microservices, queues, caches, gateways, ADRs, diagrams, or
new abstractions merely because those patterns exist.

### 5. Thin Router integration

Modify only the Router's existing routing table/prose. An explicit backend
architecture specialty request selects `backend-architecture-review`; its
result returns as bounded evidence when the Router owns a later authorization or
completion decision. Ordinary Review and all existing authority remain
unchanged. No automatic second Review or agent dispatch is added.

### 6. Continuity reuses canonical state

Add one section to `references/approved-implementation-workflow.md`:

- continue the next approved pending task when no blocker or new human decision
  exists;
- stop only at complete approved scope, `BLOCKED`, a new product/business/
  architecture decision, missing permission/credential/resource, high-risk or
  irreversible/out-of-scope action, or explicit pause/cancel;
- after compaction, resume, model/agent switch, or `继续`, recover goal/current
  task/pending/blocker/acceptance/verification from existing canonical
  Plan/Status/Handoff or equivalent state, not prior chat prose;
- do not create `.agent/goal.md`, a Task Manager, or another state system;
- when pending work is executable, an advancing turn performs at least one real
  task action instead of only summarizing or recommending;
- code written is progress only; existing Acceptance/Test/Build/Verification/
  Evidence rules remain the Done definition.

This section changes execution continuity, not Completion authority. For
OpenSpec-backed work, the active change's `tasks.md` tracks contract progress.
Direct Change reuses existing scoped Plan/Status/Handoff/equivalent state and
must not create a new OpenSpec change or second ledger. No global rule requires
OpenSpec tasks for every work item. Executable Plan checkboxes are static
execution steps only and never represent canonical task state.

### 7. Conditional minimal implementation and converging Review/Fix

Keep ordinary Bugfix and first-pass same-scope fixes on their current path. Only
when a proposed implementation or Review fix would materially add an
abstraction, component, layer, dependency, or wider scope, choose the first
adequate option in this order:

```text
Need
-> Repository Reuse
-> Stdlib
-> Platform Native
-> Existing Dependency
-> Small Local Implementation
-> New Abstraction
```

This is a lightweight judgment, not a mandatory checklist or Quality Gate. It
adds no output requirement when an ordinary localized fix already has an
adequate project-consistent implementation.

Retain `Review FAIL -> Fix -> Verify -> Review`. Before another retry, treat a
repeated same finding, fix-induced repeated regression, multi-round failure to
converge, core reviewer conflict, suspected architecture/requirements boundary,
expanding scope, or accumulating abstraction/layer/dependency as a convergence
signal. Stop further widening changes and use existing `BLOCKED` plus
`control-plane-high` Review/control-plane handling for one boundary decision.
Do not create `ESCALATED`, a Finding lifecycle, another Review gate, or another
authority. After the existing blocker is resolved, the normal same-scope loop
may resume.

The specialist remains optional and explicit-intent-only. It may provide bounded
read-only over-design evidence when backend architecture Review is explicitly
requested; ordinary Review never invokes it automatically.

### 8. Inline execution and independent Review

The current Pi session executes directly under the user's scoped authorization;
it is not an external Handoff batch, so no schema-6 Handoff is created. The
executable plan is stored at
`docs/superpowers/plans/2026-08-25-backend-architecture-review-continuity.md`
and receives a fresh read-only Preflight Review before source implementation.
A fresh ephemeral Codex instance, role `independent-reviewer`, profile
`control-plane-high`, distinct from the Pi executor, provides governed Review
evidence only. It cannot mutate files, canonical state, or Completion.

## Validation

- RED/GREEN project tests bind explicit trigger and non-trigger phrases,
  specialist boundaries, canonical return authority, pending-work continuation,
  stop conditions, resume semantics, real-action requirement, existing Done
  criteria, conditional minimal-implementation ordering, and non-converging
  Review/Fix escalation through existing mechanisms.
- `tests-or-examples/trigger-cases.md` covers specialist trigger, non-trigger,
  quick PASS, over-design restraint, real long-transaction/call-chain defects,
  and read-only boundaries.
- Continuity evidence comes from a private `/private/tmp` real-agent forward
  runner, not a Router repository fixture or the sibling specialist Skill. Each
  fresh `codex exec --ephemeral --sandbox read-only` scenario reads the current
  source Skill, approved workflow, and isolated canonical Plan/Status; it covers
  pending/resume/`继续` action events, BLOCKED/legal-stop enforcement, trace
  guards, evidence hashes/modes, and mutation probes that must go RED. The user
  accepted r4 semantic evidence after its frozen post-processor rejected exact
  CWD-relative reads; Source High Review must independently verify those paths
  resolve to the bound fixtures, with no runner change or retry.
- The preserved private answer-free `r1` trace supplies the behavioral RED:
  repeated same-finding regressions, expanding scope, and a proposed abstraction
  still advanced to the pending target action. Deterministic static GREEN plus a
  required fresh Source High Review adversarial convergence scenario supplies
  minimal forward evidence. Do not add another dedicated runner, event
  lifecycle, repository fixture, or state artifact.
- Run `quick_validate.py` on the new Skill and Router source/runtime copies.
- Verify all four local discovery symlinks resolve exactly to the independent
  sibling source before syncing the Router route that names it.
- Run Router validator, unittest suite, focused forward scenarios, and complete
  diff Review. Before runtime apply, mechanically require an exact two-file
  mutation set per target. If current synchronization tooling plans unchanged
  Router, Companion, or global-rule replacements, record runtime sync as
  `BLOCKED` and leave tooling changes to a separately approved scope.

## Rollback

Create timestamped backups outside Skill discovery roots before modifying Router
source or runtime files. Restore only exact changed files if validation or sync
fails. The new sibling is isolated; rollback may leave it untracked for user
disposition rather than deleting it without fresh destructive authorization.
No Git staging, commit, reset, clean, push, or publication is authorized.
