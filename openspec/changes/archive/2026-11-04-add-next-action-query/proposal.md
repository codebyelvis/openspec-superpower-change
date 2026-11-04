# Change: Add deterministic next-action query for canonical status

## Why

The canonical schema-6 `status.md` plus `scripts/validate_core_gates.py`
already form a deterministic closed state machine. However the question
"what is the legal next step" is re-derived every turn by the main-thread
LLM from prose status files, even though the transition rules already exist
mechanically in the validator. This invites drift: the LLM can infer a
different next action than the validator would enforce.

Cloud Claude Code (grok-cc) analysis, round-3, `STATUS: SUFFICIENT`,
identified exactly one real structure gap (G1): a read-only "next action"
query is missing. This proposal adds it without a new state system, runner,
or framework, per `router-governed` ("No ... new state system are
introduced") and `agent-capability-routing` ("do not add a framework,
registry, or runner for this").

## What Changes

- Add a read-only next-action query exposed by the validator path.
- Query output is strictly advisory: no status writes, no proposed-status
  generation, no authority transfer, no evidence promotion.
- Reuse the existing transition and owner tables in the validator; do not
  copy or duplicate the transition rules.
- Output the legal next state, required evidence roles bound to
  executor/reviewer/control-plane identity, allowed `next_owner`, lease
  state, and (when blocked) `blocker_owner` + `resume_condition`.
- Fail closed: if structural validation fails, output `BLOCKED` with reason
  and no next-action suggestion.

## Impact

- Affected specs: `skill-workflow-governance` (new capability requirement
  and scenarios).
- Affected code: `scripts/validate_core_gates.py` (sibling read-only
  query) and possibly a new sibling script; no change to the validator's
  authoritative transition logic.
- Risks: low; read-only advisory output. Risk profile standard or higher
  per grok-cc: separate implementation Review and final Review, no combined
  shortcut. Requires four-target cross-CLI sync because `scripts/` is
  portable content per `cross-cli-sync` / `cross-cli-portable-manifest.json`.

## Approval Status

- Change-id presented to user: `add-next-action-query`
- Strict validation result: PASS (`openspec validate add-next-action-query --strict`)
- [x] Proposal reviewed
- [x] This specific scoped change-id approved for implementation