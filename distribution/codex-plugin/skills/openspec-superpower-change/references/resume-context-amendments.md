# Blocked-Context Amendments and Control-Plane Rebind/Return

Read this cold-path reference only when handling a specifically approved
`strict-local-reviewer-binding`, `strict-local-control-plane-rebind`, or
`strict-local-control-plane-return` operation on a `BLOCKED` strict-local
`status.md` record. Ordinary session recovery and ordinary transitions do not
load this file.

## 1. Specifically approved reviewer-binding amendment (`strict-local-reviewer-binding`)

Ordinary transitions preserve the exact immutable contract reference. The sole
opt-in is `validate_resume_record(..., amendment_approval=<safe hashed ref>)`,
or `--resume-amendment-approval '<hashed-reference JSON>'` together with
`--resume-status`, `--artifact-root` and actual canonical `--previous-status`.
Never use it with full external `--status`. The validator remains read-only and
returns `authority_granted: false`; factual validation cannot authenticate an
actor, establish user approval or grant signing, Git or production authority.
The Router must first record specific approval of the scoped amendment.

That approving contract owns exactly one `## Resume Amendment Authorization`
JSON fence with exactly `amendment_kind: strict-local-reviewer-binding`, target
`change_id`, exact hashed `previous_contract`, safe distinct `next_contract_path`
and the complete approved stage `reviewer_assignment` map. Its own nine-field
Resume Context is approved/self-evolution/strict/local, binds the same controller
and explicitly permits `amend-review-binding: local-edit`.

Validate the actual previous state and both immutable contexts through the
existing duplicate-safe, descriptor-bound hash/parse and no-symlink rules. Both
states must remain approved/strict/local/blocked with null verified revision.
The old context has the legacy full assignment; the new Implementation entry
equals it exactly. Preserve every other context fact, including owner, actions
and critical commands. Preserve every canonical fact, including blocker, wait
action, goal, Plan and completed history, except the new contract reference and
revision increment by exactly one. Bind approval to that exact target, original
reference, new path and full map. No silent migration or new PASS is permitted.

Only the already-bound controller may perform the specifically authorized atomic
replacement after checking that actual prior canonical bytes remain identical
to those validated. Keep the old approved contract and immutable prior snapshot;
concurrent drift blocks replacement. A separate authorized ordinary same-context
transition may later resolve the blocker after fresh readiness. This amendment
does not sign readiness, alter historical evidence or close the target change.

## 2. Task-scoped local control-plane rebind (`strict-local-control-plane-rebind`)

The second opt-in is `strict-local-control-plane-rebind`. It is not selected by
`--resume-amendment-approval`. The validator reads one local, non-portable pin at
`references/task-scoped-control-plane-rebinds.json`. The pin is absent from
cross-CLI sync and from `references/cross-cli-portable-manifest.json`. Missing,
empty, or not-exactly-one content keeps the owner product set `{codex}`. A
symlink, malformed payload, duplicate JSON key, or mode other than `0600` fails
closed. The single entry must deep-equal the active contract heading
`## Control Plane Rebind`. Its previous owner is Codex. Its new owner is one
pinned schema-6 product. For this opt-in the executor native is not a separate
field: `native_session_id` must be a string equal to the new owner's instance
id, and that one value is the executor native. Both reviewers are distinct
`grok-cli` `independent-reviewer` / `control-plane-high` instances with
`governed-review-evidence` authority, and each must differ from that executor
native and from the other reviewer. The comparison is a field check; it does
not authenticate the caller. The previous contract bytes, `allowed_actions`,
and `verification_commands` stay unchanged. The one owner transition stays
`blocked`, keeps `verified_revision` null, increments revision by exactly one,
and may change only `control_plane_owner`, the contract reference,
`contract_revision`, `blocked_reason`, and `resume_condition`. Afterwards
`control_plane_owner` is readonly again. This opt-in does not grant Git,
install, deploy, or business-write authority and does not set
`authority_granted` to true. The skill source must not hardcode a private
session id or an industry change-id. The older reviewer-binding amendment
remains unchanged.

## 3. Guarded return to Codex control plane (`strict-local-control-plane-return`)

The reverse opt-in is `strict-local-control-plane-return`, selected only through
the existing hashed `--resume-amendment-approval` and actual `--previous-status`.
Specific user approval must precede implementation and application. Its safe
project-relative artifact contains an approved strict/local/self-evolution
`Resume Context`, explicit `return-control-plane: local-edit`, and the original
two independent reviewer identities. One `## Resume Return Authorization` JSON
fence has exactly `amendment_kind`, `change_id`, `previous_status_sha256`,
`previous_contract`, `original_contract`, `control_plane_owner`,
`native_session_id`, and `pin_sha256`. Mixed or duplicate authorizations reject.
The actual blocked predecessor must match its hash and the active single-entry
pin. Restore only that pin's original Codex owner and unchanged original
contract reference, including its permissions and reviewer assignments. Preserve
strict/local/approved/blocked, null verification, every progress field except
contract, and all governance fields except owner, revision+1, blocked_reason and
resume_condition. Ordinary owner changes and the older amendment stay unchanged.

Native metadata and `--resume-actor` never authenticate or grant authority.
Before application the Router must separately verify the actual original native
through supported platform/recovery evidence, confirm the former writer is idle,
and pass the approved tests, independent Implementation/Final Review and required
scoped synchronization. Preserve immutable file prestates and metadata, establish
exclusive application ownership, and prevalidate against the actual predecessor.
Retire only the exact matched pin first, recheck for drift, atomically replace
the single canonical file, then load it with ordinary Codex rules. These are two
guarded operations, not an atomic two-file transaction. Never automatically
reactivate a retired pin or overwrite foreign concurrent state. Failure after
retirement preserves revoked authority and the known phase; uncertain outcomes
block without blind retries. A return grants no business readiness, completion,
Git, installation, deployment, or other production permission.
