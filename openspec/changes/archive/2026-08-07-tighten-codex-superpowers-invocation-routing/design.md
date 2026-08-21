# Design: tighten-codex-superpowers-invocation-routing

## Context

The archived `2026-07-20-streamline-workflow-prompt-contracts` change already
implemented the phase-aware Router contract and added its four requirements to
the base spec. A stale active copy of that completed contract cannot be extended
by re-adding those requirements. This follow-up change references the archived
contract as its predecessor and contains only the new Codex invocation and
authority delta.

The fresh account-a process still selected
`superpowers:using-superpowers` for an ordinary conversation because the Skill's
broad metadata requires invocation before every response. Codex already has
native explicit and description-based implicit Skill activation, and its
product metadata supports `policy.allow_implicit_invocation: false` while
retaining user-explicit invocation.

The tempting full-centralization design would also mark Router-required child
Skills explicit-only. Codex CLI 0.147.0 did not support that design in isolated
probes: user `$child` activation emitted the child's unique marker, but an
activated Router requesting the same explicit-only child returned
`CHILD_LOAD_BLOCKED`. A direct implicit Router prompt also did not expose the
Router's unique child-loading rule. No shell/filesystem read, copied child body,
or user `$child` fallback was allowed.

## Goals / Non-Goals

### Goals

- Remove only the redundant Codex implicit `using-superpowers` meta-entry.
- Preserve explicit `$superpowers:using-superpowers` availability.
- Keep the Router as the normative selector of zero or more methods for
  governed work without requiring users to name each method.
- Prevent broad metadata and explicit sub-skill requests from bypassing Router,
  Git, business, or completion authority.
- Define deterministic request routes, fail-closed behavior, bounded phase
  chaining, forward evidence, cross-host isolation, and rollback.

### Non-Goals

- Reopen the completed predecessor requirements or their implementation.
- Make Router-required children explicit-only without native loading proof.
- Implement nested Skill loading through shell/filesystem reads, copied rules,
  or user prompts.
- Change shared Superpowers Skill text or non-Codex discovery metadata.
- Grant Git or publication authority in any source checkout.

## Decisions

### 1. Use a follow-up change instead of reviving the archived predecessor

The active change-id is `tighten-codex-superpowers-invocation-routing`. The
archived predecessor remains immutable history. This change adds only two new
requirements and does not repeat the four requirements already present in the
base `skill-workflow-governance` spec.

### 2. Make only the Codex meta-entry explicit-only

Add this file to the source-managed Superpowers checkout:

```text
skills/using-superpowers/agents/openai.yaml
```

with this product policy:

```yaml
policy:
  allow_implicit_invocation: false
```

Update `docs/README.codex.md` and add
`tests/codex/using-superpowers-invocation-policy.test.js`. Do not edit the
shared `skills/using-superpowers/SKILL.md` description or body. Fresh Codex
sessions must prove an ordinary question does not exhibit the observable
meta-workflow and explicit `$superpowers:using-superpowers` still exhibits the
complete Skill's unique behavior. The metadata and deterministic fixture prove
the implicit-invocation policy. A session may claim actual load absence only
when a supported trace identifies loaded paths or hashes; otherwise record load
state `UNKNOWN` without weakening the behavioral acceptance result.

The source-managed checkout is ahead of and behind its configured remote.
Preserve that divergence and grant no fetch, merge, reset, clean, commit, push,
or publication authority.

### 3. Keep required children implicit until native nested loading is proven

Do not add `allow_implicit_invocation: false` to Router-required children in
this revision. They remain eligible for native implicit matching as defense in
depth. `CCG-014` and the Router define the normative phase decision, but this
implementation does not claim the host mechanically suppresses every
unselected child.

A future explicit-only child proposal requires repeatable evidence that:

1. the Router body is demonstrably loaded;
2. the Router selects a child absent from implicit context;
3. the complete child body loads without shell/filesystem fallback or user
   `$child` input;
4. an unselected child remains absent; and
5. missing or duplicate Router state fails closed.

That future change requires a separately approved scope.

### 4. Enforce authority precedence through portable CCG-014

A user-explicit `$superpowers:*` request chooses a method only. It grants no
workflow, Git, business, production, or completion authority. State-changing,
Git, or completion work enters Router Gate 0 before the method proceeds.

Revise `references/shared-global-governance.md` so `CCG-014` covers both broad
Superpowers metadata and user-explicit method requests. Increment the managed
rule from version 4 to version 5 in
`references/cross-cli-portable-manifest.json`, retaining invariant IDs
`CCG-001` through `CCG-015`. Update validators and tests to accept exactly this
version/invariant relationship and synchronize it to every declared required
runtime.

The exact replacement invariant is:

```text
- [CCG-014] Governed state-changing, Git-mutating, or whole-task-completion
  work enters `openspec-superpower-change` Gate 0 through exactly one applicable
  Router before broad Superpowers metadata or any user-explicit
  `$superpowers:*` method proceeds. Generic create/modify wording alone does not
  activate a sub-skill; a user-explicit method request grants no independent
  workflow, business, Git, or completion authority; inability to load exactly
  one applicable Router is `BLOCKED`; once selected, each sub-skill's full rules
  remain in force.
```

`tests/test_workflow_rules.py` binds the exact invariant text and fail-closed
clauses. `tests/test_cross_cli_sync.py` binds managed-rule version 5 to the same
`CCG-001` through `CCG-015` set.

This portable rule changes authority precedence, not another host's
Superpowers discovery or invocation metadata.

### 5. Use an exact request-routing table

| Request | Route |
|---|---|
| Ordinary question | Direct answer or matching domain Skill; no Router or Superpowers meta-entry |
| Diagnose-only | Read-only domain diagnosis or `systematic-debugging`; stop and enter Router before any fix |
| Fully specified proposal-only | Router Gate 0 with Superpowers `none`; validate artifacts and stop for approval |
| Material proposal ambiguity | Router selects brainstorming exactly once and preserves its HARD-GATE |
| Direct Change | Router selects debugging, TDD, and Review from cause and risk |
| Ordinary diff/Report/evidence Review | Companion Standalone Lightweight |
| Architecture, OpenSpec, authorization, or completion Review | Router Review-only |
| High-risk implementation | Router plus approved OpenSpec, plan, TDD, verification, and distinct Review |
| Whole-task completion | Router Completion Contract; child evidence cannot decide completion |
| User-explicit `$superpowers:*` | Respect the method request; state-changing/Git/completion scope enters Router first |

### 6. Fail closed and bound phase chaining

If state-changing, Git, or completion work cannot load exactly one applicable
Router, return `BLOCKED`; a child cannot continue on implicit or explicit
activation alone. Diagnose-only work remains read-only and must stop for Router
reclassification before a fix.

When a child requests another phase, control returns to the Router. Each phase
and Skill may be selected at most once for the bounded route. An unresolved or
cyclic selection is `BLOCKED`. Every selected child retains its complete rules
and HARD-GATE behavior.

### 7. Separate portable source sync from the live Superpowers target

The source surfaces are:

- Router repository: `references/superpowers-adapter.md`,
  `references/request-modes.md`, `references/shared-global-governance.md`,
  `references/cross-cli-portable-manifest.json`, validators, tests, README files,
  and changelog;
- source-managed Superpowers checkout:
  `skills/using-superpowers/agents/openai.yaml`, `docs/README.codex.md`, and
  `tests/codex/using-superpowers-invocation-policy.test.js`.

The global `.agents/skills/superpowers` discovery entry links directly to the
source-managed Superpowers checkout. Editing that checkout is therefore an
immediate runtime change; it is not a separate source-first target.

For the Superpowers slice, create a non-discoverable structured staging copy of
the exact live checkout pre-state without creating a Git worktree or changing
Git state. Implement RED/GREEN and validate the three scoped paths in staging.
Review the complete staged delta against recorded live path/hash preconditions.
Then take a fresh live backup and apply exactly that reviewed delta once to the
combined source/runtime target. Immediately run source regression plus fresh
Codex discovery tests; on any failure, restore the three paths to their exact
pre-state and stop.

The Router repository remains an ordinary source-first change. Validate and
Review it before synchronizing portable governance to Codex, Antigravity CLI,
and Grok CLI through the existing reviewed plan/apply/verify-all process. No
runtime step is authorized by proposal approval alone; exact implementation
approval is still required.

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| Only the meta-entry is suppressed, so a broad child may still match | State the limitation; keep normative Router precedence and behavior forward-tests; do not claim full mechanical centralization |
| Explicit-only child silently loses TDD or Review | Keep required children implicit until native nested loading is repeatably proven |
| User-explicit child bypasses Router authority | Enforce versioned CCG-014 and fail closed without exactly one Router |
| Router is omitted, duplicated, or truncated | Test missing/duplicate discovery and block governed work |
| Child chain recurses or inflates context | Return every phase transition to Router; select each phase/Skill once |
| Codex metadata affects other hosts | Change product-specific metadata only; verify shared Skill and non-Codex metadata hashes |
| Portable authority differs across runtimes | Synchronize managed-rule version 5 and require cross-target parity |
| Divergent Superpowers checkout is overwritten | Preserve provenance and prohibit Git reconciliation or publication |
| Treating the live Superpowers checkout as offline source changes runtime before Review | Build and Review in a non-discoverable structured copy, then use one backup/apply/verify transaction on the symlink target |

## Migration and Compatibility

There is no data, Handoff, or OpenSpec lifecycle migration. The archived parent
contract stays complete. Router approval, evidence, Review, and Completion
Contract outcomes remain unchanged or stricter.

Codex gains one product-specific invocation policy. Other hosts retain their
existing Superpowers bootstrap paths, shared `SKILL.md` bytes, and discovery
metadata. The portable CCG-014 authority clarification is intentionally shared
through managed-rule version 5.

## Rollback

Create fresh structured per-target backups before approved live application. If
staging validation, fresh-session behavior, runtime synchronization, or Review
fails, restore the affected live target to its exact pre-change bytes when it
was touched, verify hashes and prior behavior, stop later targets, and report
`BLOCKED`.

For the Codex invocation slice, restore all three reviewed live paths—removing
the new `agents/openai.yaml` only when it was absent in the pre-state—and prove
the previous implicit behavior returned. Do not use fetch, merge, reset, clean,
commit, push, or unrelated checkout mutation as a rollback mechanism. Keep
staging and temporary backups until correction and Review resolve.
