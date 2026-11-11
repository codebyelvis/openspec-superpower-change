## ADDED Requirements

### Requirement: External owner stays Codex without the pin
An external schema-6 handoff SHALL keep Codex as its only control-plane product when `references/external-control-plane-rebinds.json` is missing, empty, or not exactly one entry.

#### Scenario: Missing external pin
- **WHEN** the external pin is absent and a proposed handoff sets `control_plane_owner.agent_product` to `grok-cli`
- **THEN** validation rejects that owner

### Requirement: One pinned external owner move
A mode-0600 single-entry pin MAY name one external change whose next revision replaces the Codex control-plane owner with the pinned `grok-cli` owner. The new instance MAY equal the executor instance and MUST differ from the bound reviewer instance. The validator MUST NOT authenticate the caller.

#### Scenario: Pinned Grok owner distinct from reviewer
- **WHEN** the pin matches the proposed owner and that instance differs from the bound reviewer, including when it equals `executor_assignment.agent_instance_id`
- **THEN** validation accepts the owner move and does not grant Git, install, deploy, or business-write authority

#### Scenario: Owner equals reviewer
- **WHEN** the pinned Grok owner instance id equals `reviewer_assignment.agent_instance_id`
- **THEN** validation rejects the move

### Requirement: The move is not completion
The owner move SHALL stay in `awaiting-final-verification`, keep both final gates `pending`, and increment `contract_revision` by exactly one. It MUST reject a same-revision transition to `complete`.

#### Scenario: Early complete
- **WHEN** the proposed owner move sets `lifecycle_state` to `complete`
- **THEN** validation rejects the transition
