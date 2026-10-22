# Change: Reduce redundant confirmation and advisory Review overhead

Author: elvis. Revision: draft-v2. Status: proposed, not approved for implementation.

## Why

Users repeatedly authorize the recommended work and still encounter another
confirmation for the same action. Current continuation rules prohibit that, but
category-wide stop clauses, ambiguous authorization hash ownership, and
undifferentiated BLOCKED handling can override the intended continuation.

Frequent Codex-to-grok-cc cross-validation also uses a patch-only transport for
read-only advice. A valid zero-finding report is rejected, and supplied context
and writable files share one allowlist. These are avoidable coordination costs.

## What Changes

- Check existing explicit authorization for the exact action, target, scope,
  conditions and current actor before asking again. Already authorized scoped
  Git publication or external Review does not require another polite approval.
- Bind Confirmation Lease revision/hash to the actual approved authorization
  artifact. Keep evidence freshness independent: changed implementation or test
  evidence requires appropriate re-verification, not renewed scope approval.
- Keep a failed gate closed while the assigned controller performs already
  authorized, same-scope remediation. Ask the user only for a missing authority
  or material decision, with the exact uncovered delta and rule.
- Preserve prior user decisions during recovery while separately checking
  instance assignment. Do not reopen the design merely to resolve an identity
  blocker, and do not introduce automatic ownership transfer.
- Clarify how compact inline evidence satisfies existing signoff facts without
  requiring a separately formatted code-fact table or full twelve-part report.
- Classify grok-cc consultation as bounded advisory input, reuse authorized
  dispatch and collection, and avoid adding a formal external execution workflow
  solely because another model is consulted. Preserve transport and formal gates.
- Record the native read-only grok-cc report interface as a separate design
  recommendation; it is not implementation or publication scope for this round.
- Exercise actual decision and transport scenarios with existing validators,
  tests and isolated forward probes; do not add another state machine or runner.

## Scope

The only implementation/publication source is `openspec-superpower-change`:
Router continuation, authorization/evidence interpretation, blocker handling,
compact presentation and advisory routing. grok-cc is the user-requested
advisory reviewer for this round, not a second source repository to publish.

Exact files, proposed wording, verification and rollback are in `design.md`.
Existing dirty changes and source/runtime drift are pre-existing user work.
Only the new reviewed change is eligible for staging and publication. No other
active OpenSpec change is resumed, completed, migrated or published by this work.

## Non-Goals

- No new formal reviewer product, schema-6 identity or completion authority.
  Claude Code remains an advisory reviewer; Grok Bot does not rename it Grok CLI.
- No automatic terminal creation, rebind, owner transfer, unknown-send replay,
  draft clearing, account/network/configuration changes or registry reset.
- No weaker Major approval, protected-action authority, evidence freshness,
  independent Review, required tests or final completion condition.
- No new Resume schema, broad reference reorganization, blanket gate merging,
  upstream dependency upgrade, business project change or package release.
- No automatic adoption or deletion of unrelated source/runtime drift.
- No grok-cc source edit, installation, manifest rewrite or publication. Its
  native read-only result protocol remains a separately scoped future change.

## Approval And Publication

The current request authorizes analysis, preparation, one grok-cc advisory Review
and publication of the requested update after its required gates. It does not
approve a concrete Major contract that did not yet exist. Implementation of
this exact draft remains pending explicit approval of
`reduce-redundant-confirmation-and-review-overhead`.

Publication uses this repository's verified `origin/main`, includes only this
change, and never force-pushes or publishes unrelated pending commits. The user's
existing instruction to push this update remains valid after the required gates;
no repeated Git approval is requested for that unchanged scoped action.

Cloud Review uses the current real Codex session. Read-only discovery found no
binding for that session. Creating its Claude Code terminal requires the exact
Grok Bot/hello target choice under the current grok-cc creation rule. No cloud
Review has been sent or obtained at proposal creation.

## Validation

- Strict OpenSpec validation of this change.
- Router quick validation, core gates and the full existing unittest suite for
  governance changes, with both PyYAML and supported dependency-free paths.
- Focused RED/GREEN for each distinct behavior; isolated forward scenarios for
  authorized continuation and preserved protected boundaries.
- Isolated advisory-routing forward proof preserving the actual Claude Code
  identity and distinguishing transport status from formal project evidence.
- Required independent Preflight, Implementation and Final Reviews; the user-
  requested Claude Code opinion remains additional advisory evidence.
- Reviewed Router four-target scoped sync and verification with exact destination
  prestates and unrelated runtime drift preserved.

## Success

The same authorized work proceeds without repeated confirmation; new authority
still requires the existing approval path. CC consultation stays within its
advisory role and does not acquire execution ceremony merely from its remote
transport. Local evidence, independent formal Review, required runtime parity
and scoped publication are verified before reporting this update complete.
