# Layered Authorization And Confirmation Lease

## Authorization layers

1. **Tool/platform authorization**: sandbox, command prefix, network, or CLI
   permission. It answers only whether the platform can attempt an operation.
2. **Scope/workflow authorization**: approved OpenSpec or scoped user decision,
   allowlist, immutable authorization revision, and evidence profile. The
   current Plan/Brief implements that scope and retains its required Preflight;
   its ordinary execution edits are not a new scope decision.
3. **Business/production authorization**: real credentials, paid/real endpoints,
   production writes or deletion, migration, release, archive, promotion,
   destructive Git, external messages, and equivalent user-owned actions.

A lower layer never satisfies a higher layer. Existing platform permission avoids
a duplicate chat prompt for the same safe command, but it never authorizes a new
workflow scope or business/production action.

## Confirmation Lease

A Confirmation Lease binds exactly:

- `decision_id`;
- positive `artifact_revision` and lowercase `artifact_sha256`;
- `approved_scope` and non-empty `approved_actions`;
- `risk_profile` and `decision_source`;
- `owner_instance_id`;
- `status: valid`;
- non-empty `invalidation_conditions`.

Compact inline work may record these fields inline. Standard/strict external work
stores a typed artifact referenced by immutable `confirmation_lease` fields in
the schema-6 Handoff. The artifact uses one
`COOP_CONFIRMATION_LEASE_START/END` YAML marker and is checked by path and SHA-256
without logging its contents.

For a new lease, identify the actual immutable approved OpenSpec artifact or
scoped decision record by path/identifier in `approved_scope`; keep
`decision_source` as its existing provenance enum. `artifact_revision` and
`artifact_sha256` bind that authorization artifact, not mutable implementation,
Plan/Brief, Report, test results or progress. Refresh affected evidence when
those change. Preserve every exact comparison and historical binding: if an
existing lease actually binds a Plan/Brief, changing those bound bytes still
uses its existing approval/amendment path, never a silent reinterpretation.

## Reuse matrix

A valid unchanged lease is reusable for read-only inspection, safe tests, diff
checks, and the same finding's fix -> verify -> Review loop. Reuse records the
new evidence result but does not repeat confirmation.

For a protected action, reuse also requires existing explicit authority covering
the exact action, target, scope, conditions and actor. An approved action list
or platform permission alone is not business/production authorization. Changed
targets or effects require their own coverage; generic continuation is not it.

Closed-loop continuation reuses this same matrix for approved safe work; it does
not create a per-continue Lease or require a new Lease for each safe step.
When the user explicitly instructs closed-loop execution (e.g. "闭环推进") or
delegates intermediate approvals/reviews to an advisory reviewer (e.g. "改为询问 grok-cc"),
intermediate transitions between approved slices continue without repeating
confirmation once review/verification PASS evidence is recorded. Pauses remain
reserved for genuine blockers, breaker fires (two failures on the same slice),
or explicit Git and production boundaries. The complete continuation rule and
its stop boundaries live in `references/approved-implementation-workflow.md`.

The lease expires when its bound authorization revision/hash, scope, acceptance,
risk, production impact, credentials, external side effects, destructive Git
need, approved evidence assumptions, or the user's decision changes. Evidence
assumptions mean approved acceptance requirements such as real-environment or
endpoint requirements, not merely stale test/Report results after a scoped fix.
Contradictory evidence still invalidates the lease; refreshed results cannot
waive changed acceptance or another invalidation condition.
`deferred` and `revoked` provenance cannot
remain valid. A newly required business/production decision always returns to
the user even if the platform command prefix is already allowed.
