# Layered Authorization And Confirmation Lease

## Authorization layers

1. **Tool/platform authorization**: sandbox, command prefix, network, or CLI
   permission. It answers only whether the platform can attempt an operation.
2. **Scope/workflow authorization**: approved OpenSpec, current Plan/Brief,
   allowlist, artifact revision, and evidence profile.
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
the schema-5 Handoff. The artifact uses one
`COOP_CONFIRMATION_LEASE_START/END` YAML marker and is checked by path and SHA-256
without logging its contents.

## Reuse matrix

A valid unchanged lease is reusable for read-only inspection, safe tests, diff
checks, and the same finding's fix -> verify -> Review loop. Reuse records the
new evidence result but does not repeat confirmation.

Closed-loop continuation reuses this same matrix for approved safe work; it does
not create a per-continue Lease or require a new Lease for each safe step. The
complete continuation rule and its stop boundaries live in
`references/approved-implementation-workflow.md`.

The lease expires when revision/hash, scope, acceptance, risk, production impact,
credentials, external side effects, destructive Git need, evidence assumptions,
or the user's decision changes. `deferred` and `revoked` provenance cannot
remain valid. A newly required business/production decision always returns to
the user even if the platform command prefix is already allowed.
