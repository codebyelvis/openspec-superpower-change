# Design: Bounded Plan Preflight Convergence

## Intent

Make Plan Preflight converge after one complete review and one bounded focused
recheck when only same-scope mechanical corrections change. Preserve every
existing safety, authority, implementation Review, final verification, and
completion boundary.

## Single owner

`references/approved-implementation-workflow.md` owns the normative convergence
contract. `SKILL.md`, `superpowers-adapter.md`, and `step-evidence-gate.md` point
to or specialize that contract without creating another state system.

## Convergence paths

### FULL_PREFLIGHT

Required for the first review in a lineage and whenever a protected boundary
changes. It covers contract/spec, scope/files, authority/canonical ownership,
command executability, branch/worktree/module origin,
database/production/Git boundaries, acceptance/verification, rollback/stop,
plan completeness, and one independent adversarial probe.

The reviewer returns all reasonably discoverable findings and records
`finding_completeness: true`. This does not suppress later safety findings; it
prevents intentionally staged or serial ordinary findings.

### FOCUSED_RECHECK

Allowed only when:

- the previous full review attested completeness;
- deterministic mechanical self-check passes;
- scope, contract/spec, acceptance, risk/evidence profile, authority,
  executor/reviewer assignments, allowed/forbidden files, branch/worktree,
  database/production, Git/publication/deployment boundaries are each explicitly
  recorded as unchanged; and
- the artifact diff is limited to declared findings plus mechanically necessary
  adjacent edits.

It checks prior finding closure, the correction diff and direct impact, every
protected-boundary assertion, safety overrides, and fresh mechanical evidence.
The same reviewer instance must continue while remaining independent from author
and executor. A reviewer-instance change requires `FULL_PREFLIGHT`.

### CONTROL_PLANE_ADJUDICATION

This is an existing-control-plane convergence route outside Preflight Review,
not a Review mode or canonical state. It produces no Preflight result or new
state artifact.

It is selected after two same-lineage blocked Review results, reviewer conflict,
expanding correction scope, an unauthorized protected-boundary change, or a late
ordinary finding that should have been found in the full review.

A protected-boundary change always ends focused eligibility. If the changed
boundary already has a valid control-plane-accepted decision, it starts a new
lineage at `FULL_PREFLIGHT`. Otherwise the current review is `BLOCKED` and enters
adjudication; after a decision, any authorized revision starts a new lineage at
full review.

The control plane consolidates findings once and chooses one existing path:
start a newly authorized lineage at full review, permit one terminal focused
recheck after one bounded same-lineage correction bundle, or remain blocked for
a material decision. A failed terminal recheck does not reopen an unlimited
loop.

## Minimal Review record

Reuse the existing Preflight Review artifact. Do not add a schema, registry,
ledger, Handoff field, canonical status field, or cross-runtime fingerprint
algorithm.

A full or focused Review records these human-auditable fields:

- `review_mode: FULL_PREFLIGHT | FOCUSED_RECHECK`;
- `lineage_root_revision`: safe project-relative path plus SHA-256 of the whole
  original Plan/Brief file;
- `reviewed_revision`: the same safe project-relative path plus SHA-256 of the
  whole current Plan/Brief file;
- `parent_review`: project-relative path and whole-file SHA-256, or `null` for
  the full root;
- `attempt: 1 | 2 | terminal`;
- `reviewer_identity`: the Review assignment's product, contract-local instance
  ID, role, and capability profile;
- `same_reviewer_instance: true | false`, derived by exact comparison with the
  immutable parent Review identity rather than trusted as a free assertion;
- `protected_boundaries`: one explicit `unchanged | changed` entry for scope,
  contract/spec, acceptance, risk/evidence profile, authority, assignments,
  allowed/forbidden files, branch/worktree, database/production,
  Git/publication/deployment;
- `declared_correction_set`: finding IDs and exact Plan/Brief section anchors;
- `mechanical_self_check`: result and evidence references;
- `finding_completeness`: required `true` for full review;
- `blocking_findings`, `non_blocking_recommendations`, and
  `accepted_residual_risks`; every residual risk records evidence, impact, and
  owner or decision.

All SHA values hash whole regular-file bytes exactly as stored, with no newline
normalization. Root and current revision paths must be identical safe
project-relative POSIX logical paths; path drift or same-hash substitution at
another path is invalid. The current hash is verified against the current
regular non-symlink file. At the full root, root and current hashes are equal.
After correction, the immutable parent Review file and its verified whole-file
hash anchor the prior root hash and reviewer identity; the historical root bytes
are not expected at the mutated current path. Every referenced evidence file
must be regular and non-symlink. Missing legacy fields select `FULL_PREFLIGHT`.
Invalid SHA/path/parent binding, reviewer identity mismatch, author/executor
identity reuse, `same_reviewer_instance: false`, or an undeclared diff prevents
focused eligibility. An unauthorized protected change is `BLOCKED` and uses
adjudication; an authorized protected change starts a new full lineage.

The protected-boundary checklist is an evidence assertion verified against the
actual Plan/Brief diff and referenced contract/authority artifacts. It is not a
machine-trusted digest and cannot override actual evidence.

## Finding classification

Gate-bearing Preflight keeps `PASS` and `BLOCKED` only.

Blocking findings include P0/P1, security, integrity/data loss, authority,
scope/contract/risk/acceptance changes, forbidden external effects, plan
non-executability, false evidence, and missing required rollback/stop behavior.

A non-blocking recommendation is optional before execution and cannot affect
acceptance, safety, authority, evidence integrity, or deterministic execution.
It records impact and owner/decision but does not convert PASS to BLOCKED.

A late P0/P1 or safety finding always blocks. If it was already discoverable in
the full revision, record a completeness breach and route to adjudication rather
than starting another serial ordinary-finding loop.

## Mechanical self-check

Reuse existing validators and project commands. Do not add a generic Plan state
engine. Before full human Review, deterministic checks cover when applicable:

- placeholders and undefined references;
- task files against allowed/forbidden files;
- executor attempts to update canonical state/checksums;
- unauthorized Git commands;
- fixed interpreter/runtime flags and bytecode/cache behavior;
- command paths, selectors, cwd, import bootstrap, launcher/module/test origin;
- request-schema fields against formulas and examples;
- branch/worktree and checksum consistency;
- forbidden database, production, generic-SQL, retry/fallback, publication, and
  deployment operations.

Project-specific checks stay in the Plan as exact commands. The global contract
requires their result; it does not invent a universal project parser.

## Plan proportionality

For OpenSpec-backed work, no placeholders means no unresolved material choice
and no non-executable step. Each business slice provides exact files and
responsibilities, interfaces/signatures, contract/acceptance references,
RED/GREEN intent, critical commands, rollback, and stop conditions. Full source
bodies are needed only when omitting them leaves a material implementation
choice unresolved. Exact references may replace repeated copied contracts.

## Risk classification

Risk follows changed effects. Merely reading a persistence substrate through an
existing private read-only boundary does not alone mean persistence semantics
change. Strict remains mandatory for changes to security/auth, public API/schema,
persistence semantics, migrations, write paths, deployment/rollback,
deletion/recovery, cross-tenant behavior, or production authority.

Any profile change is a protected-boundary change and requires full review. This
change does not downgrade an existing approved strict lineage.

## Compatibility and rollback

No Handoff schema, canonical lifecycle state, Reviewer Assignment, Completion
Contract, or shared global governance block changes. Source/runtime edits use
structured backups. A failed source validation restores source; a failed runtime
target restores only that target and stops later targets. All restored copies
must pass parity and discovery checks before work resumes.
