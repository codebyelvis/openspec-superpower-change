# Review draft: authorization reuse and advisory cross-validation

Author: elvis. Revision: draft-v2. Implementation approval: pending.

## Evidence And Failure Mechanisms

1. `references/approved-implementation-workflow.md` prohibits reconfirming an
   accepted option, but its stop list treats Git and external operations as
   unconditional stop categories. The applicable question is whether the exact
   action is already authorized, not whether the category sounds protected.
2. `references/confirmation-lease.md` invalidates on revision/hash changes but
   does not identify the authorization artifact clearly. Implementation bytes,
   Reports and status revisions are different from the approved scope contract.
3. Preflight actionable findings produce BLOCKED, and canonical BLOCKED prevents
   advancement. This must not prevent the authorized correction of the blocker
   itself or make every recoverable defect a new user decision.
4. Project Session Resume preserves immutable actor assignments. Losing an actor
   assignment does not mean the user's earlier design/action decisions expired.
5. `references/step-evidence-gate.md` offers compact gates but its unqualified
   Signoff Conditions still demand a code-fact table. The required facts and the
   presentation format need an explicit relationship.
6. Installed grok-cc `task_packet.py` always renders patch response rules and
   rejects a plain zero-finding report. `files` is both context and write scope.
   A no-write local probe reproduced both facts. The historical
   `docs/review/2026-10-16-native-startup-grok-cc-dispatch.json` prepared a proposed
   report-file diff for advisory output; that dispatch never happened because
   its remote runtime was unavailable, so it is not successful remote evidence.

Existing compact routing, two-round Preflight convergence, focused verification,
canonical ownership and repeat-send prevention are retained and reused.

## Proposed Normative Wording

### Authorization coverage before confirmation

> Before requesting confirmation, check the existing explicit user authorization
> against the proposed action, exact target, approved scope, applicable conditions
> and current actor assignment. A protected action category requires a new user
> decision only when the applicable authority is absent, expired, revoked,
> ambiguous or exceeded. Preserve valid authorization across ordinary phases and
> same-scope correction. Closed-loop wording alone grants no protected authority.

Store the decision in the existing approved contract, Plan/Status or applicable
lease. Do not create a permission registry or new canonical state. Reading the
same rule again, a model switch in the same assigned instance, a successful
subtask or routine progress report does not create a new approval boundary.

For this update, a later scoped approval covers implementation, ordinary
verification, required scoped runtime sync, same-scope fixes and the expressly
authorized publication targets. No second "may I start/test/review/push" prompt
is needed once those conditions hold. A changed target, force-push, new account,
new production effect or broadened scope is not covered.

### Authorization binding and evidence freshness

> A Confirmation Lease identifies the approved authorization artifact and its
> exact immutable revision/hash. Changing implementation files, test results,
> Reports or progress does not by itself change that authorization binding.
> Refresh affected evidence after changes. A changed bound contract or protected
> authorization dimension still invalidates the old binding.

Preserve every exact comparison in `validate_confirmation_lease`. This proposal
does not rebind an existing lease, accept changed contract bytes automatically,
normalize away hashes or retrofit historical evidence. New documentation and
call sites must name their actual authorization source using existing fields.
If an existing task really bound a mutable artifact, follow its existing contract
amendment path rather than silently changing what the old hash meant.

### Owner-aware blocker remediation

> BLOCKED prevents the gated transition. Classify the actual blocker owner and
> required next action. The assigned controller continues already authorized,
> same-scope correction and required recheck while the gate remains closed. Ask
> the user only when the next correction needs missing authority or a material
> decision. Do not implement before a required Preflight PASS or advance from
> stale, failed or blocked evidence.

Keep existing canonical lifecycle values, transition validation, Preflight
lineage limits and scope triage. "Correct the blocker" is not permission to
erase it, rewrite immutable evidence or start a third unchanged-contract
Preflight. Missing credentials, unreachable remote resources and unknown sends
are reported accurately; an additional user "yes" is not execution evidence.

### Recovery and narrow questions

> Recovery preserves recorded user decisions and separately validates the current
> actor's assignment. An identity blocker does not reopen approved design or
> scope. Each necessary confirmation identifies the uncovered decision, relevant
> prior authorization, material delta or missing authority, exact blocking rule
> and action that the answer would enable.

Retain the existing original-owner/rebind restrictions. This change does not
authorize a new window to impersonate the previous controller. Independent work
that does not depend on a missing answer continues when already authorized.

### Compact signoff presentation

> Compact signoff retains all applicable factual, verification, scope and Review
> requirements. Scoped inline path/line or diff references may carry the code
> facts and positive/negative checks; a separately formatted fact table and the
> full twelve-part output are not required solely by the Signoff Conditions.

Full evidence remains necessary where the existing risk or contract requires it.
This clarifies representation; it does not permit unsupported factual claims,
skipped regression evidence or weaker protected-path signoff.

## Project-side grok-cc Advisory Routing

This round changes only the Router. A user-requested advisory consultation does
not itself create a schema-6 external implementation batch, additional formal
Preflight or duplicate batch Review. Preserve any already-required formal gate
and the distinction between asking for advice and delegating implementation.

Reuse explicit authorization for the same task, bound target and reviewed
payload. Continue permitted reads, recovery and local checks without asking
whether to proceed again. Creating a new terminal, changing its binding or
recovering an unknown send retains the actual grok-cc restrictions; project
rules cannot grant authority that its transport contract does not provide.

Until its native report protocol exists, use the current supported transport
and manually accept only the requested advisory-report output path. A correct
transport hash does not prove that the report covers the supplied acceptance,
nor that its claims are correct. The report remains advisory and is not promoted
to a formal gate PASS.

## Separate Future Design: Native Advisory Result Protocol

This subsection is a design recommendation, not this round's implementation,
installation, publication or completion requirement. A later grok-cc source
change could add a small separate path within its existing packet helper:

- Inputs: task ID, explicit review purpose, exact read-only file snapshots and
  their hashes, the relevant acceptance/diff context, and advisory authority.
- A review packet has no writable project paths. Supplied context never becomes
  a patch allowlist. A patch returned for this mode is an invalid result.
- Output: one bounded report bound to task ID and the consumed snapshot digest,
  actual reviewer product `claude-code`, reviewed scope, findings with evidence,
  unverified items and a result such as findings/no-findings/incomplete.
- Accept a complete zero-finding report. Require integrity and complete output;
  do not run `git apply` or create a dummy report patch for a review result.
- Use existing task/binding/cursor/intent handling. The wrapper records verified
  transport identity from existing binding evidence; model-declared identity or
  a hash alone never proves authority or business correctness.
- Codex evaluates each finding against actual local files and acceptance before
  fixing it, and performs the relevant local verification. Remote assertions
  remain advisory; do not map them to a formal schema-6 PASS.
- Same-scope correction uses existing authorization. Already authorized same-
  target dispatch, reads and result collection do not need another confirmation.
  Existing creation/rebind, unknown-send and export restrictions remain intact.
- Review once per cohesive business slice or material decision; focus any
  follow-up on changed evidence. Existing user-required reviews remain required.

The installed grok-cc payload already differs from its source, including its
binding helper. A future source/installation contract must first establish a
reviewed baseline that preserves those existing changes and obey its source-
publication-before-installation rule. This Router update does not reconcile,
publish or overwrite those bytes.

Formal Claude Code reviewer eligibility, independent-session pooling and format
export preauthorization are separate future changes. They are unnecessary to
provide a faithful advisory report and are not granted here.

## Source File Boundaries

Router candidates, edited only when needed for the approved acceptance:

- `SKILL.md`
- `references/approved-implementation-workflow.md`
- `references/confirmation-lease.md`
- `references/step-evidence-gate.md`
- `references/completion-contract.md`
- `references/local-instruction-checkpoint.md`
- `scripts/validate_core_gates.py`
- `tests/test_workflow_rules.py`
- Existing relevant routing fixture/probe files, selected explicitly in the
  implementation Plan; no new runner or state schema.
- This OpenSpec change, `CHANGELOG.md`, and required scoped review/learning
  artifacts under existing project conventions.
- Generated adapters only through existing generators if required validation
  shows the source changes affect them.

No grok-cc source or installation file is an edit candidate for this round.
Do not edit its binding registry, authentication, model, network or native
configuration. Do not edit Companion governance merely to
duplicate the Router's continuation rule. Any demonstrated incompatible
Companion behavior requires an explicit scoped amendment before changing it.

## Acceptance And Verification Plan

1. After accepting option A, ordinary pending in-scope work proceeds without
   asking to accept A or to start the next safe step again.
2. Explicit authorization to dispatch one scoped Review and publish a scoped
   update is reused after required gates; another destination or force-push
   remains unauthorized.
3. A same-scope fix changes source hashes and refreshes affected tests/Review,
   while the unchanged approved contract keeps its authorization.
4. Changed approval bytes, revoked authority, increased scope/risk, production
   effects and missing Major approval still block the applicable action.
5. A fixable Plan defect is corrected and rechecked without another user prompt;
   implementation remains prohibited before Preflight PASS and its existing
   convergence limits remain effective.
6. A new unassigned instance preserves decisions but cannot sign as the original
   controller. An identity issue is described as that issue, not design rejection.
7. Compact inline signoff is accepted with complete relevant evidence; missing
   regression or required strict evidence is still rejected.
8. A standalone advisory request does not create an execution Handoff or claim
   formal Review PASS. Existing transport constraints and a user-required cloud
   opinion remain applicable; missing cloud output is not called successful.
9. Neither a second model nor an unchanged explicit dispatch authorization
   creates a new user decision. A new target, unknown send, implementation
   delegation or changed approved contract still follows its actual boundaries.

Use existing production validation functions for mechanical lease/evidence
checks and existing test files for regressions. Test-owned models cannot be
reported as production enforcement. Isolated agent forward runs must demonstrate
the selected continuation/routing decisions; keyword presence is supporting
coverage only. Add one scenario per distinct changed mechanism, not redundant
platform/wording permutations.

Required Router commands:

```bash
openspec validate reduce-redundant-confirmation-and-review-overhead --strict
"${PYTHON_BIN:-python3}" "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" .
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Choose the quick-validator interpreter that has PyYAML. Run project validators
and tests with the supported dependency-free fallback as required by AGENTS.
Reviewers verify changed behavior and actual local evidence, not just metadata.
No grok-cc source suite or installation work is required because it is unchanged.

## Review, Synchronization And Publication

The requested cloud round reviews this draft and its concrete wording. Existing
transport may carry its advisory report as a proposed report-file diff until
native advisory mode exists in a later separately approved change. Manually
enforce that output-only path locally;
do not mistake the current packet context allowlist for a read/write separation.
No remote source implementation or formal gate decision is requested.

The already-existing Major path owns approval, reviewed implementation Plan,
backup, independent Preflight, Implementation/Final Review and completion.
Read the existing sync checklist before constructing the scoped Router plan;
validate and review exact source/destination prestates, then verify all required
Codex, Pi, Antigravity CLI and Grok CLI targets. One target's success cannot stand
in for another target or for native loading evidence.

Preserve dirty baseline changes. Before commit, compare this round against its
own preimage and stage only reviewed owned deltas. Verify this source's origin/main
and reject unrelated ahead commits or drift before any push. No force-push,
release or unrelated pending-work publication is covered.

## Rollback

Before implementation, refresh structured backups of the exact selected source
and runtime prestates outside skill discovery roots. Restore only this round's
owned edits while preserving later or unrelated user changes. Use existing sync
transaction rollback for Router runtime changes. Keep backup and blocker evidence
until validation, synchronization, publication and cleanup outcomes are known. Never reset the
worktree, delete unknown recovery files or rewrite Git history to roll back.
