# Change: Allow one external Grok control-plane owner

## Why

`migrate-codex-a-session-memory` is an external schema-6 handoff. Its control plane is Codex, and the user approved moving that owner to a non-Codex product. The existing `strict-local-control-plane-rebind` accepts a Grok owner only for one local strict contract that stays `blocked`. It does not change an external handoff, and it does not grant completion.

## What Changes

- Add one separate, non-portable, mode-0600 pin for a single external handoff owner move.
- Allow exactly one transition: the pinned external change replaces its Codex `control_plane_owner` with the pinned `grok-cli` owner.
- Keep lifecycle, evidence results, executor, reviewer, lease, and completion rules unchanged in that transition.
- Allow the new owner instance to equal that external handoff's executor instance while requiring it to differ from the bound reviewer.
- Do not grant `complete` in the owner move; keep both final gates `pending`.

## Impact

- Affected specs: `external-grok-control-plane`
- Affected code, after approval of this change-id: `scripts/validate_core_gates.py` and the external-handoff rule text that currently says the control plane product must be Codex
- Risks: an owner instance equal to the bound reviewer would permit self-review. This change rejects that shape.
- The local pin `references/task-scoped-control-plane-rebinds.json` stays unused and unchanged.

## Approval Status

- Change-id presented to user: `allow-one-external-grok-control-plane`
- Strict validation result: exit 0, `Change 'allow-one-external-grok-control-plane' is valid`
- [x] Proposal reviewed
- [x] This specific scoped change-id approved for implementation
- User approval recorded before validator edits: `已批准 allow-one-external-grok-control-plane`
