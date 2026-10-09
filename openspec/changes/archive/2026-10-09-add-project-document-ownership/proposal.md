# Change: Add Project Document Ownership

Author: elvis. Revision: draft-v1. Date: 2026-10-08.

## Why

The user reports that new deployment notes and engineering lessons are scattered
in business projects' docs roots. The current learning resolver and Candidate
Card also repeat `docs/engineering-invariants.md` as the generic fallback.
There is no scoped rule for reusing a project's document conventions before
creation or for preserving links and protected path contracts during an
authorized relocation. This proposal addresses S8 only; S1–S7 remain closed.

## What Changes

- Resolve ordinary document destinations from explicit user/project contracts,
  then existing purpose/domain conventions, then a suitable purpose subdirectory.
  Existing project structures may be outside docs; no universal layout is imposed.
- Keep docs-root index entries and explicit path contracts; preserve AGENTS,
  CONTEXT/maps, OpenSpec, collaboration state and iteration-state locations.
- Require authorized document/reference closure, retained content and resolved
  inbound/outbound links and navigation for any authorized relocation.
- Own the rule in an independent Project Document Ownership subsection of
  `references/project-learning-closeout.md`; SKILL only navigates to it.
  Reading that subsection does not activate learning promotion.
- Use `docs/engineering/engineering-invariants.md` only when no project-specific
  engineering guidance path or convention exists; remove the template's copied
  fallback in favor of the canonical resolver. This repository's expressly
  contracted `docs/engineering-invariants.md` stays where it is.
- Validate actual isolated file operations and links, alongside artifact-owned
  rule checks, through the existing validation/test infrastructure.

## Impact And Scoped Files

Affected capability: `skill-workflow-governance` (ADDED requirements).

Future implementation scope, conditional on the specific approved contract:

- `SKILL.md`: minimal matching-row navigation; no frontmatter scope expansion.
- `references/project-learning-closeout.md`: canonical independent ownership
  subsection and Target resolver fallback.
- `templates/learning-candidate-template.md`: resolver navigation, no copied policy.
- `scripts/validate_core_gates.py`: artifact-bound ownership/resolver checks.
- `tests/test_workflow_rules.py`: affected regressions and isolated file/link checks.
- `CHANGELOG.md`, this change's artifacts, S8-specific review/sanitized evidence
  and iteration bookkeeping at their existing locations.

No migration of this repository's existing docs. No AGENTS/CONTEXT body edits,
OpenSpec main-spec or historical-change edits, S7 resume changes, companion,
shared governance, manifest, target-list, generated-distribution, dependency,
production or business-repository changes. A needed excluded change stops for
a revised Major scope and new approval. No new runtime framework is introduced.

## Current Approval And Authority

- Change-id: `add-project-document-ownership`.
- Revision: `draft-v1`; classification: Major Self-Evolution.
- Status: `proposed`; approval of this exact contract: **not obtained**.
- Current user instruction: S8 **proposal only**. Authorized outputs are the
  review draft, these OpenSpec artifacts, the proposal validation record and
  S8 CURRENT/BACKLOG state. No implementation, runtime sync, manifest edit,
  Git add/commit/push, production action or real-document relocation this round.
- General edit permission, prior slice approval and closed-loop language do not
  approve this new change. Later execution must record specific approval and
  check the applicable sync/Git lease; this draft supplies no such current lease.
- Review draft: `docs/review/2026-10-08-S8-project-document-ownership-draft.md`.
- Design decisions and acceptance are specified in `design.md` and the delta.
  Approval accepts that scoped design, not a claim of implementation or PASS.
