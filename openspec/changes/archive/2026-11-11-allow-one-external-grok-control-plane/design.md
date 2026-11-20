# Design: one external Grok control-plane owner

## Decision

External schema-6 handoffs remain Codex-owned unless a second skill-local pin exists. The pin path is `references/external-control-plane-rebinds.json`. It is not the local rebind pin, not a symlink, mode `0600`, and a one-entry JSON array. A missing pin leaves the external owner product set as `{codex}`. Malformed JSON, a duplicate key, or any other mode fails closed.

The single entry deep-equals the active handoff section `## External Control Plane Rebind`. Validator source does not hardcode a session id or a business change-id.

Required keys:

- `amendment_kind`: `external-control-plane-rebind`
- `scope`: `this-change-only`
- `change_id`
- `previous_control_plane_owner`: product `codex`, role `control-plane`, profile `control-plane-high`
- `control_plane_owner`: product `grok-cli`, role `control-plane`, profile `control-plane-high`
- `previous_status_sha256`: SHA-256 of the canonical status file before the move

The new owner instance id may equal `executor_assignment.agent_instance_id` and differs from `reviewer_assignment.agent_instance_id`. The comparison does not authenticate the caller. `authority_granted` stays false.

## Transition

The move is one revision on the same external handoff. It may change only:

- `control_plane_owner` to the pinned Grok owner
- `contract_revision` by exactly 1
- `blocked_reason`
- `resume_condition`

Lifecycle stays `awaiting-final-verification`. `final_verification` stays `pending`. `final_review_result` stays `pending`. Attempt report, batch review, lease, executor, and reviewer references stay byte-equal. `complete` in the same revision is rejected. Git, install, deploy, and business writes stay unauthorized.

After this revision, `control_plane_owner` is readonly again. Later final verification and final Review bind the new Grok owner.

## Non-goals

This change does not write the pin, edit `migrate-codex-a-session-memory` status, or mark that change complete. It does not alter `strict-local-control-plane-rebind` or CCG-001.
