# Change: Add project session resume checkpoints

## Why

The approved workflow already recovers Plan/Status/Handoff after a window or
model switch, but it does not require unfinished local implementations to
persist completed work, one next action, blockers and the latest verified
revision before stopping. Chat summaries cannot serve as canonical state.

The S7 supplement to the iteration contract requests this persistence duty.
It is Major Self-Evolution. The user approved this concrete draft-v1 and its
scoped design on 2026-10-08 by replying “批准” to the proposal/approval report.

## What Changes

- Reuse `docs/agent-collab/<change-id>/status.md` for pending local and external
  implementation. Add one progress section in that file, without another
  ledger, harness, hook, global resume index or schema version.
- Propose an explicit local discriminator and schema-6 field subset. Preserve
  the complete external Handoff API, exact required fields, assignments,
  evidence fingerprints and transition gates. Missing external fields never
  trigger local fallback.
- Persist current state, completed references, exactly one nonterminal
  `next_action`, blockers and `resume_condition` before an intentional pause,
  implementation-turn end or window handoff. Resume from the validated record
  and its contract/plan/evidence references, never from the last reply.
- Bind the best checkpoint to the latest verified **and persisted** revision
  and scoped source-input fingerprint. Later edits remain unverified; do not
  roll them back automatically or reuse a stale PASS.
- Treat `继续闭环` / `闭环推进` as bounded continuation. Multiple unfinished
  changes require user selection. New instances may read recovery state, but
  do not acquire control-plane, signing, Git or production authority.

## Impact And File Scope

Proposed implementation files only:

- `SKILL.md`: minimal navigation within the existing continuation section;
- `references/approved-implementation-workflow.md`: canonical resume rules;
- `references/direct-change-rule.md`: conditional navigation for unfinished
  multi-window local implementation;
- `scripts/validate_core_gates.py`: explicit resume validation and transition
  entry, leaving existing Handoff validation strict;
- `tests/test_workflow_rules.py`: focused behavioral/compatibility regressions;
- `CHANGELOG.md`, this change's OpenSpec files, S7-specific iteration status,
  review and sanitized evidence artifacts for the authorized slice.

No changes to `references/handoff-contract.md`, companion source, manifests,
shared global-rule text, CLI targets, dependency versions, existing project
status/history or unrelated active changes. If one becomes necessary, stop and
revise the scoped proposal for a new approval. S8 is excluded.

The local encoding, Direct Change identifier, ownership recovery constraints
and source fingerprint in `design.md` are accepted within this scoped approval.
The approval does not claim implementation or validation is already complete.

## Approval Status

- Change-id: `add-project-session-resume`
- Revision: `draft-v1`
- Classification: Major Self-Evolution; future implementation risk `strict`
- Status: `approved-for-implementation`; scoped implementation approval:
  **obtained**, user reply “批准”, 2026-10-08
- Design acceptance: **obtained**; independent implementation/final Review:
  **pending**
- General edit permission and closed-loop requests do not approve this concrete
  change-id. Approval must name this change and scoped design.
- Iteration closure: the existing S7 iteration continues under the user's
  approved scoped closed-loop request and contract §3.2; after required gates,
  apply reviewed local sync and commit/push only this repository's current
  branch. No other repository, production, release or destructive Git authority.
- Review draft: `docs/review/2026-10-08-S7-project-session-resume-draft.md`
