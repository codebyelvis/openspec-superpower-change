# Approved Implementation Workflow

For schema 6 Review routing, carry all six concepts without abbreviation:
Review purpose, reviewer product, role, capability, independence, and authority.
The normative assignment and product/instance boundary live in
`references/agent-capability-routing.md`; this reference does not create a
second authority.

Use after an OpenSpec proposal is approved, or after Direct Change has
classified and authorized an implementation that will use an external agent.
Compact local Direct Change uses `references/direct-change-rule.md` without
loading this workflow. On unchanged approved continuation, read current
canonical state and only the rules needed for the pending phase; reuse completed
planning, still-valid Preflight and unaffected evidence.

## OpenSpec And Superpowers Boundary

1. OpenSpec proposal/design/spec deltas are the approved change contract.
2. For OpenSpec-required work, that approval is the single design approval and
   does not require a duplicate `docs/superpowers/specs/` artifact or approval.
3. After approval, invoke `superpowers:writing-plans` for multi-step work that
   does not already have an applicable reviewed plan, and
   save the executable plan under the project-preferred path.
4. OpenSpec-backed work uses
   `openspec/changes/<change-id>/tasks.md` to track contract progress for that
   change. Direct Change reuses existing scoped Plan/Status/Handoff/equivalent
   state for continuity and does not require OpenSpec tasks.md. Continuity must
   not create a new OpenSpec change or second ledger. No global rule requires
   every work item to have OpenSpec tasks.md. Plan checkboxes are static
   execution steps only and never canonical task state.
5. Compact Direct Change does not require a large plan by default and does not
   create a Handoff or OpenSpec change solely because closed-loop or model-advice
   wording exists.
6. Compact low-risk Direct Change uses an inline readiness check and does not
   create a standalone Brief, Plan, or Preflight artifact. Single-slice
   standard/OpenSpec work uses one short Plan and no duplicate Brief; add a
   separate Brief only for external handoff or a materially distinct contract.

Follow `references/superpowers-adapter.md`; a generated plan does not grant Git
permission and must not create a second design approval.

## Plan And Evidence Granularity

- Group work by complete business slice, not by file count or technical layer.
- Include exact files, test commands, evidence profile, batch profile, negative
  searches, acceptance, rollback, and stop conditions.
- Apply Step Evidence Gate before and after each business slice or risk
  milestone, not every TDD micro-step. TDD owns RED/GREEN inside the slice.
- Use `superpowers:systematic-debugging` before changing unexplained failures.
- Use `superpowers:test-driven-development` for behavior changes, not for a
  test-only assertion of already-defined behavior.
- Proportional TDD adds one regression per distinct changed behavior or failure
  mechanism. Equivalent parameter, platform, timing, or race variants require
  a separately demonstrated risk; do not create them for ceremony.

## Plan And Brief Preflight Review

Compact low-risk Direct Change completes the same readiness facts inline and
does not require standalone Preflight. Single-slice standard/OpenSpec work uses
its one short Plan as the only planning artifact and runs one initial
Preflight. All strict, external, multi-slice, or protected-boundary work also
runs standalone Preflight. Review
the current Plan or Brief revision for contract coverage, placeholders, allowed
scope, production wiring where applicable, acceptance, exact verification
commands, evidence profile, rollback/stop conditions, branch/worktree choice,
and Git authority.
Preflight uses only `PASS` or `BLOCKED`; reserve `FAIL` for implementation or
post-implementation Review. Preflight PASS authorizes execution only and never
replaces Implementation Review, Final Review, or
`references/completion-contract.md`.

### Bounded convergence

`FULL_PREFLIGHT` and `FOCUSED_RECHECK` are Review modes.
`CONTROL_PLANE_ADJUDICATION` is an existing control-plane route outside Review,
not a third mode, schema, ledger, Handoff field, or canonical state.

For one unchanged contract, the hard ceiling is one `FULL_PREFLIGHT` plus at
most one terminal `FOCUSED_RECHECK`. There is no automatic R3+. The first full
Review consolidates all reasonably discoverable findings instead of staging
them across rounds. In plain terms, one terminal focused recheck is the ceiling,
not a renewable retry.

Use `FULL_PREFLIGHT` for the first Review in a lineage, a legacy Review missing
convergence fields, a replacement reviewer, or any protected-boundary change.
It covers the complete matrix and an independent adversarial probe. The
reviewer reports all reasonably discoverable findings together and records
`finding_completeness: true`; ordinary findings must not be intentionally
staged across rounds.

A revised artifact may use `FOCUSED_RECHECK` only when the same reviewer instance
remains independent from author and executor, mechanical self-check
passes, the correction diff closes only declared findings plus necessary
adjacent edits, and every protected boundary is verified unchanged:

- scope, contract/spec, acceptance, and risk/evidence profile;
- authority and executor/reviewer assignments;
- allowed/forbidden files and branch/worktree;
- database/production and Git/publication/deployment.

The existing Preflight Review artifact records:

- `review_mode: FULL_PREFLIGHT | FOCUSED_RECHECK`;
- `lineage_root_revision` and `reviewed_revision`, each containing the identical
  safe project-relative POSIX Plan/Brief path and its whole-file SHA-256;
- `parent_review`, containing a safe project-relative path and whole-file
  SHA-256, or `null` at the full root;
- `attempt: 1 | 2 | terminal`, exact `reviewer_identity` product/contract-local
  instance ID/role/capability profile, and `same_reviewer_instance` derived by
  exact comparison with immutable parent Review identity;
- `protected_boundaries`, `declared_correction_set`,
  `mechanical_self_check`, and `finding_completeness`;
- `blocking_findings`, `non_blocking_recommendations`, and
  `accepted_residual_risks`; every accepted residual risk records evidence,
  impact, and owner or decision.

Hash whole regular-file bytes exactly as stored without newline normalization.
Root/current paths are the same safe logical path. Verify current SHA against the
current regular non-symlink file. At the full root, root and current SHA values
match. After correction, verify the immutable `parent_review` file and use its
bound root SHA and reviewer identity to anchor history; do not require historical
root bytes to remain at the mutated current path. Every evidence reference must
resolve within project root to a regular non-symlink file. Path drift, same-hash
substitution at another path, invalid revision or parent binding, reviewer
identity mismatch or reuse of author/executor identity, or undeclared diff
prevents focused eligibility. Missing legacy fields select `FULL_PREFLIGHT`. The
protected-boundary checklist is
human-auditable evidence checked against the actual diff and referenced
contract/authority artifacts; it is not a machine-trusted digest.

Any actionable finding is `BLOCKED`. P0/P1, security, integrity/data loss,
authority, scope/contract/risk/acceptance, forbidden effect, false evidence,
non-executable Plan, and missing required rollback/stop behavior remain blocking
in every mode. A non-blocking recommendation is optional and cannot affect
acceptance, safety, authority, evidence integrity, or deterministic execution.
A non-actionable observation with actual risk remains separately classified in
`accepted_residual_risks`, not relabeled as advice or an unresolved finding.

After two blocked Review results in one lineage, reviewer conflict, expanding
correction scope, an unauthorized protected-boundary change, or a late ordinary
finding discoverable during full Review, route to
`CONTROL_PLANE_ADJUDICATION`. An authorized boundary change starts a new full
lineage; an unauthorized change remains BLOCKED until adjudicated. After a
blocked terminal recheck, adjudication may stop, resolve the boundary, or start
a newly authorized full lineage; it never authorizes another unchanged-contract
Preflight. A late P0/P1 or safety finding always blocks regardless of
completeness or retry limits.

After implementation begins, same-scope implementation or final Review findings
go directly through fix -> focused verification -> the same Review stage and
must not reopen Preflight. Reopen readiness only when a protected boundary
changes and the corresponding approval remains valid.

Before human Review, reuse deterministic project validators to check applicable
placeholders, undefined references, allowed/forbidden files, command and module
origins, unauthorized Git, branch/worktree, schema/formula examples, checksums,
and forbidden database, production, publication, or deployment operations.
Project-specific checks remain exact Plan commands; this contract adds no
universal parser.

Evidence stays proportionate: `compact` low-risk deterministic work may remain
inline with focused verification and concise Review; `standard` multi-step work
keeps required critical evidence and a distinct Review; `strict` effects keep
real evidence and explicit human business gates. Mocks or platform permission
cannot replace strict evidence or authorization. Risk follows changed effects:
reading persistence through an existing private read-only boundary does not by
itself change persistence semantics, but its required real read-only probes
remain mandatory. Any profile change ends focused eligibility and requires full
Review.

## Authorized Execution Continuity

During already authorized implementation, when approved tasks remain Pending, no
Blocker exists, and no new human decision is required, continue with the next
approved task. Completing a subtask is not a stop condition and must not trigger
a continue prompt. An advancing turn with executable pending work performs at
least one task-related action: read/search required code, edit, test/build,
verify, collect evidence, or update existing canonical state. A summary,
recommendation, or future plan alone is not progress.

Closed-loop continuation intent includes “闭环推进”, “继续闭环”, “按推荐方案推进”,
and “完成后统一 Review”. It means continue within the already approved scope
and current canonical Plan/Status/Handoff: safe, reversible reads, edits, tests,
verification, same-scope Review/Fix, and existing-state updates. It does not
expand scope or authorize database writes, production operations, external
messages, publication, deployment, destructive actions, or Git writes.

After an accepted recommendation, continue without confirming the same option or
asking whether to start the next approved safe step again. A material choice is
presented once as one focused question and is not reopened after selection unless
scope or risk changes. A status report is a status update and is
non-confirmation progress, not a confirmation request. Continue to the next
approved pending task while no blocker or new human decision exists.
Finish reversible preparation first so Git, publication, and external writes are
handed to the user as a concrete, reviewable result.

When several options differ only in implementation detail and an obvious minimal
recommendation satisfies the approved need, adopt that recommendation directly;
do not ask the user to choose among formal A/B/C options. Ask one focused
question, or enter `brainstorming`/`grill-with-docs`, only when the choice would
materially change the business, product, architecture, security, compatibility,
acceptance, or an approved contract. Once the solution and terminology are
closed, a long task does not re-enter `grill-with-docs`; only a new material
decision does.

Stop only when all approved tasks are complete; when a new human decision is
required because scope, risk, acceptance, product, business, architecture,
security, credentials, resources, compatibility, or another contract choice
changes. This includes a new product, business, or architecture decision;
missing permission, credentials, or required resources; and any high-risk,
irreversible, or outside the approved scope step. Stop also when the next step
requires production writes or deletion, database writes, production
operations, external effects/messages, release, publication, deployment,
destructive actions, destructive Git, or any other Git authority; when the
contract is contradictory, recovery is not reversible, scope would expand,
canonical state is `BLOCKED`, or the user explicitly pauses or cancels.

After Context Compaction, session recovery, a model or agent switch, or `继续`,
including a new window, recover from the canonical Plan, Status, Handoff, or
equivalent state: goal,
current task, Pending tasks, Blocker, Acceptance, and Verification. Do not infer the next action from the previous chat response. Do not create `.agent/goal.md`,
a Task Manager, or a second state system. Code written is progress,
not Done. Existing Acceptance, Test, Build, Verification, and Evidence rules,
together with `references/completion-contract.md`, remain the only Done criteria.

“完成后统一 Review” retains the applicable readiness/Plan Preflight, Step Evidence,
implementation Review, final verification, Final Review, and Completion Contract;
it never skips or defers a required gate.

For compact or standard single-slice work that is not strict, external,
multi-slice, or protected-boundary work, one post-verification complete-diff
Review may satisfy both Implementation Review and Final Review under
`references/completion-contract.md`; test-spec and test-quality concerns are
included in that implementation/final Review by default, not mandatory
standalone Review gates. The strict and protected paths retain separate gates.

## Project Session Resume

On `继续`, `继续闭环`, compaction or a new window, recover unfinished authorized
work from `docs/agent-collab/<change-id>/status.md`, never the previous chat reply.
Reuse the existing OpenSpec change-id; unfinished Direct Change uses its existing
scoped ID or a stable `direct-<slug>` when a checkpoint is first needed. Finished
single-turn compact work creates no checkpoint. Multiple unfinished changes
require explicit selection, never modification-time or priority selection.
Legacy schema-4/schema-5 stays on its immutable audit path, without migration.

Before voluntarily stopping or ending an advancing implementation turn, persist
the actual phase, completed evidence, one next action, blocker owner and resume
condition in this same canonical file. Do not checkpoint every TDD micro-step.
Keep existing Plan/tasks as the task list; add no second ledger, schema family,
autosave hook or conversation replay. Unexpected termination may leave unverified
edits: preserve them and the historical checkpoint, then verify/fix.

### Record and contract binding

Status owns exactly one `## Session Resume` section with one JSON fence.
Its explicit `record_kind` selects these exact outer fields:

- `local`: `record_kind`, `governance`, `progress`. Governance contains exactly
  `schema_version`, `change_id`, `mode`, `approval_status`, `risk_profile`,
  `contract_revision`, `lifecycle_state`, `control_plane_owner`, `blocked_reason`,
  `blocker_owner`, `resume_condition`, `next_owner`, `readonly_fields`.
  Use existing schema-6 meanings/enums and its applicable immutable subset:
  schema version, change, mode, approval, risk, control-plane owner and readonly
  fields. Do not invent external executor, batch or Report artifacts.
- `external`: `record_kind`, `contract_revision`, `progress`. The same file's
  complete Handoff remains the sole governance source; required fields, lease,
  assignment, transitions, evidence and previous-status gates remain intact.
  Progress stays outside the Handoff marker. Missing fields, marker deletion or
  parse errors cannot select the local path or downgrade an external contract.

`progress` has exactly `goal`, hashed `contract`, nullable hashed `plan`,
`completed` (hashed existing work/evidence references), `next_action` and nullable
`verified_revision`. References use safe project-relative regular files and
whole-file `sha256`; reject duplicate keys/sections and symlinks in every path
component. Hash and parse the same descriptor's bytes. Do not copy mutable
progress into a Brief. An outstanding external batch keeps its already-persisted
wait action: change progress before execution SHA capture or after ownership
returns through the existing validated transition.

Put exactly one `## Resume Context` JSON fence in the **existing scoped approved
contract**, as immutable factual metadata, never a new approval document.
Its exact fields are `change_id`, `record_kind`, `mode`, `approval_status`,
`risk_profile`, `control_plane_owner`, `allowed_actions` (action -> permission),
`verification_commands` (nonempty unique command strings), `reviewer_assignment`
(existing full assignment for standard/strict, the strict-local stage form below,
or null only for local compact inline Review). External context carries the exact full Handoff assignment,
including compact's bound control-plane Review; it cannot substitute null,
another instance or malformed metadata.
Facts must match governance. Bare prose “approved”, metadata and validator PASS
cannot create authorization or enlarge scope. Proposed/blocked approval stays
blocked with a reason, owner, resume condition and `wait` action.

Only local strict contexts may use an exact two-key `reviewer_assignment` mapping:
`implementation-review` and `final-review`, each containing the complete existing
seven-field assignment. Validate both entries on every load, including blocked
states; reject mixed, missing, unknown or duplicate keys without shape fallback.
Both reviewers are eligible independent-reviewer/control-plane-high instances
with explicit purpose and governed-review-evidence authority. Implementation
independence names exactly `control_plane_owner` and `executor_assignment`;
Final additionally names `implementation_reviewer`. Both contract instance IDs
must differ from the bound controller/local executor and from each other. Local
execution does not invent an external executor assignment. Legacy single
assignments retain their original separate-gate behavior; standard, compact and
full external Handoff retain their existing shapes and applicability.

Example progress before verification (replace hashes with actual file hashes):

```json
{
  "goal": "Verify the authorized implementation",
  "contract": {"path": "contract.md", "sha256": "<actual SHA-256>"},
  "plan": null,
  "completed": [],
  "next_action": {
    "action": "verify", "owner": "openspec-superpower-change",
    "permission": "local-read", "inputs": []
  },
  "verified_revision": null
}
```

Nonterminal `next_action` has exactly `action`, existing `owner`, `permission`
and hashed `inputs`; it must match context authorization and governance's next
owner. Blocked means wait for its persisted condition; complete has
`next_action: null`. Continuation grants no Git, production, credential,
destructive, external-write or completion authority.

### Verified checkpoint and persisted transitions

A best checkpoint is the latest **verified and persisted** scoped revision,
not the newest edit/chat message or a required Git commit. `verified_revision`
has exactly `revision`, `inputs` (path -> SHA-256 or null for expected absence),
`fingerprint` (SHA-256 of sorted compact JSON inputs), `commands`. Each command
record has `command`, `result: pass`, hashed `evidence`. Cover all context
critical commands and verification-relevant source/config/tests; Review checks
declared scope. Exclude canonical status and new evidence outputs to avoid
self-hash cycles. A mismatch blocks current PASS: preserve checkpoint and edits,
then verify current inputs before advancing.

Existing JSON verification evidence records `evidence_role: final-verification`,
`evidence_result: pass`, `change_id`, `contract_revision`, `source_fingerprint`,
`agent_identity`, `commands` (actual command -> exit-code mapping). Required
commands must have actual exit 0 and matching owner/revision/fingerprint.
Validation checks binding/consistency, not whether a command ran; capture real
process results before persistence. Synthetic unittest evidence is not signoff.

Local Review JSON artifacts in `completed` use existing field concepts:
`evidence_role: implementation-review | final-review`, `evidence_result: pass`,
`change_id`, `contract_revision`, `source_fingerprint`, `canonical_sha256`,
`agent_identity`, `reviewer_assignment`. Bind applicable phases to actual prior
canonical bytes. Standard/strict Review matches the independent assignment's
purpose, product, role, capability, independence and evidence authority; compact
inline Review uses the bound owner and null independent assignment. The existing
Completion Contract decides applicability; no new signoff owner is introduced.
For the strict-local stage form, `evidence_role` selects exactly its approved
entry. Evidence still carries one full assignment and its identity, never the
mapping or an arbitrary eligible reviewer. Recorded-complete stage-form recovery
rechecks both retained phase Reviews and verified consistency, including Final's
revision matching the persisted verified revision. This read-only
check does not recreate or claim the original actual previous canonical bytes.

Validate proposed transitions against actual prior canonical bytes before the
already-bound controller atomically replaces status. Preserve kind/context and
immutable governance; increment revision by one. Same-phase pauses are allowed.
Local compact may enter awaiting-final-verification from ready-for-execution
with verified inputs; standard/strict retains implementation Review first.
Standalone recovery and completion also validate that retained Review; checking
only the phase-entry transition cannot establish a recovered phase is valid.
Final verification must be persisted in awaiting-final-verification before a
separate final Review and complete transition. Complete requires that actual
previous revision/SHA and unchanged verified checkpoint; atomic verify/review/
complete fails. Terminal recovery is read-only and never signs completion again.
External transitions delegate to unchanged full Handoff validators.

### Specifically approved blocked-context amendment

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

### Read-only recovery and identity

Every loaded agent may read selected state. A new unassigned instance cannot
impersonate the recorded control plane or inherit signing/completion rights.
A model switch in the same bound instance does not change assignment. Reuse
approved safe actions only with the existing required assignment; any rebind
uses existing authority rules. New instances report the boundary after read-only
recovery. No automatic identity transfer or rollback is introduced.

Use existing tooling explicitly (these commands are read-only):

```bash
python3 scripts/validate_core_gates.py . --resume-status <canonical-status> --artifact-root <project-root>
python3 scripts/validate_core_gates.py . --resume-status <temporary-proposed-status> --artifact-root <project-root> --previous-status <actual-canonical-status>
```

Keep temporary proposed status outside the project; canonical status is the
single ledger. Optional `--resume-actor <instance>` compares a diagnostic string
to the assignment only; it does not authenticate the caller or grant rights.
`--resume-status` is explicit and mutually exclusive with existing `--status`,
which still requires complete external Handoff. Python `recover_project_session`
inventories canonical status and requires selection when ambiguous. Invalid or
missing context, stale inputs or assignments fail closed; never reconstruct
authority or current PASS from chat.

## Conditional Minimal Implementation

### Proportional Implementation

For the current task, use the smallest adequate design and artifact set: reuse
existing rules, templates, validators, and tests first. Do not add a framework,
schema, registry, runner, or ledger when direct mechanisms work. For the current
task, TDD covers changed acceptance, changed contracts, and credible regressions.
Do not create or run unrelated tests without an existing gate or demonstrated
blast radius; broader relevant gates remain mandatory. If support machinery
exceeds the change itself, simplify.

Use this lightweight judgment only when a proposed implementation or Review fix
would materially add an abstraction, component, layer, dependency, or wider
scope. Establish the approved Need, then choose the first adequate option:

```text
Need
-> Repository Reuse
-> Stdlib
-> Platform Native
-> Existing Dependency
-> Small Local Implementation
-> New Abstraction
```

An earlier project-consistent option wins when it satisfies the approved need.
This does not run for every ordinary Bugfix and creates no mandatory checklist,
artifact, gate, or output. It does not automatically select
`backend-architecture-review`; that Skill remains explicit-intent-only.

## Review/Fix Convergence

### Finding scope triage

When a Review finding arrives, before reproducing or fixing it, judge it in
this order:

```text
1. finding 是否由当前变更引入？
2. 是否验证当前 acceptance？
3. 是否推翻当前证据声明？
4. 是否位于批准的 blast radius 或精确测试范围？
5. 修复是否仍在当前授权范围？
```

Findings related to the current task enter the normal `Fix -> Verify -> Review`
loop. A failure belonging to a frozen baseline or accepted preimage that does
not meet the current-task conditions is recorded as
`OUT_OF_SCOPE_PREEXISTING_DEBT` with its fact, impact, and owner. If a Reviewer
expands the requested test or fix scope, explicitly reject that expansion; do
not take over unrelated problems merely to make Review PASS.

Do not replay every command from a Review before performing this scope triage.
"Read or classify all test files" does not mean "execute all test files." An
accepted upstream preimage does not approve or validate the entire upstream release.

Keep the existing `Review FAIL -> Fix -> Verify -> Review` loop. Ordinary
first-pass findings continue through the existing same-scope loop. Before
another retry, treat the loop as non-converging when evidence shows that:

- the same finding recurs after a verified fix;
- a fix-induced regression recurs;
- multiple Review rounds do not converge;
- reviewers materially conflict on the core approach;
- the root problem may be an architecture or requirements boundary;
- fix scope keeps expanding; or
- a small need keeps accumulating an abstraction, layer, component, or dependency.

When a signal applies, stop before another widening fix and return `BLOCKED` to
`control-plane-high` through the existing Review/control-plane mechanism. Record
the blocker owner and resume condition, then re-evaluate the original approved
need, boundary, and smallest adequate correction. Resume the normal same-scope
loop only after that boundary decision resolves the blocker.

Do not create an `ESCALATED` state, Finding lifecycle, Quality Gate, Task
Contract, second state system, new multi-agent flow, or new final authority.

## Inline Implementation

1. Execute the plan inline with TDD/debugging as applicable.
2. Run slice verification.
3. For `compact`, run a focused diff/self-review.
4. For `standard` or `strict` inline implementation, invoke
   `superpowers:requesting-code-review` after implementation and before final
   verification. Review PASS is required.
5. Any finding returns to the same slice: fix, refresh verification, and Review
   again. Do not carry unresolved findings into the next slice.

## External Implementation

1. Create one schema-version-6 Handoff Contract at canonical `status.md`, with
   immutable control-plane/executor assignments and the exact immutable
   `reviewer_assignment`, decision provenance, and a Confirmation Lease. Before
   schema-6 deployment, active schema-4/schema-5 contracts MUST finish under
   their old runtime; they MUST NOT be migrated, resumed after cutover, or used
   as current transition authority.
2. A low-risk Direct Change may use `compact`/`single`; approved public/API
   restoration remains `strict`, and OpenSpec-backed work uses its approved
   evidence and batch profiles.
3. Hand Brief/Report/Review attempts to `codex-brief-antigravity-review`.
4. The external Review is the batch code-review gate; do not duplicate it with
   a second Superpowers review for the same batch.
5. `FAIL` or `BLOCKED` stays on the same batch and must re-enter Review with
   fresh attempt evidence.
6. Non-final `PASS` advances one batch. Final `PASS` sets
   `awaiting-final-verification` and returns ownership to this router.
7. Brief and Report carry the same execution-revision canonical SHA-256. A
   mismatch blocks Review and batch promotion.
8. Every evidence-bearing transition validates its proposed status against the
   actual prior canonical status before replacement. New schema-2 manifests bind
   product/instance/role/profile plus result/change/batch/attempt/source
   revision/SHA-256. Standard/strict executor and reviewer instance IDs differ,
   even for the same product. Compact binds `reviewer_assignment` to the bound
   control-plane identity, keeps it distinct from the executor, and requires the
   top-level non-blank not-applicable reason. Historical schema-4/schema-5
   contracts and their evidence are immutable.
9. Manual copy/paste of a state-changing standard/strict Brief does not downgrade
   governance. Validate the same Handoff and evidence chain before promotion.

## Final Completion

After all inline slices pass, or after external handback, stop using this
route-specific workflow as completion authority and evaluate
`references/completion-contract.md`. This section defines no independent
whole-task checklist.

## OpenSpec closeout

OpenSpec closeout eligibility, reconciliation, archival validation, and active
owner/resume outcomes are governed exclusively by
`references/completion-contract.md`. This section defines no second closeout
checklist.

For OpenSpec-backed multi-step work, skip the Superpowers plan only when the
user explicitly says to skip it. Compact Direct Change does not require a large
plan by default. Never skip final verification or Review.

## Tiered Authorization And High Review

Route capability through `agent-capability-routing.md`. Platform permission,
workflow scope, and business/production authorization are independent layers.
Reuse an unchanged Confirmation Lease for safe checks and same-finding loops;
request a new user decision for any invalidating production, risk, scope,
credential, external-effect, destructive-Git, evidence, or user-decision change.

For standard/strict work, High Review inspects actual files and the complete
diff, traces copy/transform/production wiring and every behavior claim to its
mechanism, reruns critical evidence, and adds an independent adversarial or real
business-chain probe. Executor PASS cannot substitute for this Review.
