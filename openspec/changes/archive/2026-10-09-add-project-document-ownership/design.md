# Project Document Ownership — draft-v1

Author: elvis. Status: proposal only; not approved for implementation.

## Context And Goals

S8 governs ordinary project-document placement using the existing Change Gate.
It does not create a documentation framework, global reorganization, second
learning pipeline, new registry, evidence format or completion authority.
Existing OpenSpec approval, learning triggers, owner assignments, protected
references and completion gates remain authoritative.

The concrete source evidence is the learning resolver's generic root-level
fallback and its duplication in the template and validation expectations.
Business-project scattering is user-reported; it has not been replayed in this
proposal phase. This repository already explicitly contracts its root-level
engineering guidance in AGENTS, so changing a generic default cannot move it.

## Decisions

### 1. One owner, a separate conditional entry

Maintain the ordinary-document rule in `references/project-learning-closeout.md`
under `Project Document Ownership`. Add one SKILL routing row to that subsection.
Clarify that the subsection can be used before document creation/authorized
relocation without loading or activating the promotion/closeout workflow.
Existing learning triggers still require all their current gates when applicable.

The Target resolver applies that same subsection. The Candidate Card template
points to the resolver rather than copying a default or directory policy.
Do not add a portable file, manifest selector, standalone path resolver, agent
hook, taxonomy registry, whole-repository scanner or automatic document mover.
The existing root validator checks the actual owning subsection and resolver;
presence of the same text elsewhere cannot satisfy that responsibility.

Alternative: a new reference would separate filenames more visibly but would
require a new portable inventory entry. Reusing an independent subsection in
the existing reference keeps this slice within the current manifest boundary.
This bounded placement choice is explicit for approval and can be revised
before implementation; it does not alter a user-owned authority decision.

### 2. Resolve purpose and local evidence before a default

For the task's proposed document, inspect applicable project instructions,
relevant index/navigation entries and nearby documents only. Resolve in order:

1. The user's explicit path and authoritative project position contracts.
   Conflicting applicable contracts are unresolved, not overridden by a default.
2. Established purpose/domain conventions, including existing guidance targets.
   A project may use `docs/ops/`, `handbook/platform/` or another existing
   structure. A directory's mere existence is insufficient proof of convention.
3. If neither exists, an appropriate purpose subdirectory, for example
   `docs/deployment/`, `docs/engineering/`, `docs/incidents/` or
   `docs/learning-candidates/`. These are examples, not a mandatory taxonomy.

Reserve docs-root files for index entry points and explicit user/project path
contracts. Do not invent a new root index or new folder when an existing
navigation/target already satisfies the task. If two destinations remain equally
plausible after scoped inspection, resolve that specific ambiguity before writes;
do not select by modification time or conduct an unrelated global documentation audit.

The engineering resolver falls back to
`docs/engineering/engineering-invariants.md` only when no explicit guidance path
or established convention exists. An existing guidance file referenced by the
project's AGENTS is reused. This repository retains its current root guidance;
no root AGENTS or engineering-invariant migration is part of S8.

### 3. Existing special-artifact locations win

AGENTS, CONTEXT and any CONTEXT-MAP, OpenSpec artifacts, collaboration state
(including `docs/agent-collab/<change-id>/status.md`) and iteration state
(`docs/iteration/CURRENT.md`, BACKLOG and LOG) keep their existing location
contracts. No generic purpose rule moves or clones them into another folder.

Approval/Plan/Review/evidence artifacts can carry exact-path/hash bindings.
Ordinary organization never rewrites them or their inbound contract references
to claim links are repaired. A needed bound-artifact change follows its existing
owner, authorization, revision and evidence rules; that expansion is outside
this scoped implementation. This proposal adds no re-signing or recovery authority.

### 4. Relocation has an explicit reference closure

An authorization to create a document is not a blanket authorization to move
existing ones. Before an authorized move, enumerate the selected documents,
destinations and the necessary inbound/outbound references/navigation affected
by those exact paths. Only documents and referring files within the current
authorization may change. If the needed closure includes an unauthorized file
or protected contract artifact, stop before moving and resolve that boundary.

Preserve document content, allowing only the necessary link edits. Repair
relative inbound/outbound links and anchors from their new source directories,
AGENTS navigation and applicable active references within the authorized closure.
Validate destination absence/compatibility, bound-project paths, ordinary-file
operations and links; a conflicting destination, project escape or unresolved
link blocks the move. Do not overwrite content, follow an out-of-project
symlink, automatically relocate unrelated history or rewrite external URLs.
Take scoped before/after content and file inventories so unrelated-file stability
is checked, rather than inferred from the agent's report.

This repository has no authorized real-document move in S8. Future behavior
verification uses synthetic projects in private temporary locations. Migration
of any business project's real document requires that project's own scoped authorization.

## Acceptance And Evidence Plan After Approval

Implementation begins with a fresh structured source/runtime backup and a
canonical strict execution Plan under the existing workflow. OpenSpec tasks
track contract progress and do not substitute for that Plan. Record old behavior
RED against a fixture/counterexample before edits, then GREEN for each changed
mechanism; no new routing runner or production probe is needed.

Use three isolated native scenarios with gpt-6.1-sol/high and real file tools:

| Scenario | Required observable result |
|---|---|
| Existing deployment convention plus explicit engineering-root contract | New deployment note uses the existing domain directory; engineering target reuses the contracted file; protected artifacts retain bytes and paths |
| No existing convention | New deployment note and learning engineering guidance use suitable purpose subdirectories, including the engineering fallback; no ordinary docs-root addition; reading ownership alone does not activate promotion |
| Authorized migration and incomplete-closure branch | Actual selected document move preserves content, repairs relative inbound/outbound links/anchors and AGENTS navigation; unrelated and protected snapshots stay equal; a separate fixture with an unauthorized referring file stops before mutation |

Deterministic assertions in the existing tests inspect actual paths, bytes,
relative link/anchor resolution and before/after inventories for those fixtures.
Additional focused negatives cover equally plausible destinations, destination
collision/project escape, missing link closure, mistaken root default and
policy text moved into a non-owning template. Test the ownership of the resolver
default, not the absence of the old path from explicit-contract examples.
Keep the existing test proving this repository's AGENTS/root guidance is discoverable.

The native audit must confirm actual authorized reads/writes and fail closed on
missing tool evidence, claimed-but-absent output or off-scope writes. An
answer-only routing probe is insufficient. Keep raw CLI traces privately only
while needed; durable evidence contains sanitized results and scoped hashes,
not prompts, credentials, conversations or business content.

Required implementation checks: quick_validate with PyYAML; core and full
existing unittest suite with PyYAML and dependency-free fallback; new-change
strict validation; actual RED/GREEN, link/content/scope evidence. Since SKILL
routing changes, an affected-tests-only shortcut cannot replace the full suite.
No implementation test or forward-test is claimed by current draft validation.

## Review And Sync Boundaries

The strict route retains distinct readiness, implementation and final gates.
Bind concrete instances before dispatch, following the existing capability rules:

| Purpose | Product | Role | Profile | Independence | Authority |
|---|---|---|---|---|---|
| Plan Preflight | codex | independent-reviewer | control-plane-high | distinct from Plan author/executor | governed-review-evidence |
| Implementation Review | codex | independent-reviewer | control-plane-high | distinct from implementation author/executor | governed-review-evidence |
| Final Review | codex | independent-reviewer | control-plane-high | distinct from implementation and Implementation Reviewer | governed-review-evidence |

All use the user's fixed gpt-6.1-sol/high; model metadata grants no authority.
No instance is assigned and no gate-bearing PASS exists during proposal drafting.
Preflight approves readiness only; the bound Router retains evidence acceptance,
state transition and completion. Lack of an eligible instance blocks that actual gate.

After approved portable changes, read the existing sync checklist/cross-CLI
protocol, review a scoped plan and destination pre-state, verify current action
authorization, then apply and verify every existing required Codex/Pi/Antigravity/
Grok target. No target-list or manifest modification is allowed. A needed
excluded edit requires a new scoped decision. Missing sync authority or a stale
required target is BLOCKED; source tests do not imply runtime completion.

Run learning closeout if triggered, fresh final verification and independent
Final Review before approved reconciliation/archive/iteration closeout. Git
operations require the applicable explicit iteration lease and never include
the 44 pre-existing unrelated files. None of these write/closure authorities is
granted by the current proposal-only command.

## Rollback And Approval Decision

The draft review records the private proposal backup. It can restore only this
round's CURRENT/BACKLOG edits and remove this round's newly created artifacts;
it is not permission to reset the worktree or runtime. Retain it while approval
and rollback decisions are pending. Implementation creates fresh backups and
uses the reviewed existing sync transaction for any authorized runtime rollback.

Approve or revise draft-v1's single-owner subsection, precedence, fallback,
protected-path behavior, authorized reference closure and actual-file acceptance.
Specific approval must be recorded against this change and exact contract before
any rule/validator/runtime implementation. Scope, OpenSpec/Superpowers boundary,
evidence signing, completion authority or target-list changes need new approval.
