# Design: add-role-first-review-routing

## Context

Current schema-5 governed Handoffs bind `agent_product`, contract-local
`agent_instance_id`, `agent_role`, and `capability_profile` in an exact
four-field `independent_reviewer_assignment`. The validators use a closed
product enum containing `codex`, `antigravity-cli`, and `grok-cli`, and the
portable runtime manifest declares those same three targets. This is
fail-closed, but it does not admit Pi or the complete Reviewer Assignment
Contract.

Standalone Review wording is intentionally lightweight and therefore does not
create Handoff state. It currently lacks a corresponding fail-closed output
contract: a response can tell the user to ask “another agent” without naming the
product, role, required instance separation, or result authority. The approved
design keeps standalone work lightweight while making its destination explicit.

Pi is installed in the observed environment as binary `pi` version `0.84.1`.
It supports Skill paths, `AGENTS.md`/context-file discovery, independent
sessions, non-interactive operation, and a read-only tool allowlist. Existing Pi
Skill copies are observed but are not a declared target and cannot be treated as
current until the new source, target plan, parity, validators, and discovery
checks pass.

The Router source worktree already contains unrelated, uncommitted work,
including changes to several candidate target files. Implementation must bind
the current actual bytes as preimages and add only this change's delta. The
Companion source worktree was observed clean at proposal time. Neither
observation is implementation authority; Preflight must refresh both.

## Goals / Non-Goals

### Goals

- Make reviewer selection explicit in every Review recommendation, prompt, and
  governed assignment.
- Give Codex, Pi, Antigravity CLI, and Grok CLI equal eligibility for executor
  and independent-reviewer roles.
- Keep role, capability profile, instance separation, and contract binding as
  the authority mechanism.
- Keep the bound Codex control-plane instance as the sole canonical decision
  owner.
- Add Pi to portable Skill/global-rule synchronization with deterministic,
  non-sensitive validation and target-local rollback.
- Mechanically reject missing assignments, product substitution, self-review,
  unknown products, and incomplete required-target synchronization.
- Introduce an unambiguous schema-6 Handoff boundary instead of making new
  reviewer fields optional inside schema 5.

### Non-Goals

- Add a new orchestration Skill or a second mutable global authority.
- Make all installed agents automatically eligible.
- Treat a fresh session label, product difference, or model name alone as
  independence evidence.
- Read or synchronize credentials, auth, session content, model configuration,
  extensions, caches, logs, or binaries.
- Rewrite active or historical Handoffs to use Pi.
- Resolve or absorb unrelated active OpenSpec lifecycles.

## Considered Approaches

### 1. Wording-only destination labels

Require responses to say Pi, Codex, Antigravity, or Grok but leave Pi outside
the evidence schema and runtime manifest. Rejected because it creates a product
that looks equivalent to the user but is rejected by governed evidence.

### 2. Add Pi only to the product enum

Allow Pi in Handoff evidence without synchronizing the governance Skills and
managed global rule to Pi. Rejected because contract eligibility could outpace
runtime instruction parity and discovery evidence.

### 3. Complete role-first integration

Selected. Add one schema-6 canonical product, one global invariant, one runtime
target, and the associated validators, fixtures, forward-tests,
synchronization, and rollback behavior. Keep older schema branches frozen, keep
the product allowlist closed, and preserve the existing Codex control-plane
boundary.

## Decisions

### 1. Role-first authority model

Schema-6 canonical products are exactly:

```text
codex
pi
antigravity-cli
grok-cli
```

Under schema 6, all four may be assigned `executor` or
`independent-reviewer`. A standard or
strict independent reviewer uses `control-plane-high`. The executor and reviewer
must use different contract-local instance IDs, even when their product is the
same. Product equality does not permit self-review, and product difference does
not override a reused or unproven instance.

Only a bound `codex` product with role `control-plane` and profile
`control-plane-high` owns routing, evidence acceptance, canonical transitions,
archive decisions, and final completion.

### 2. Reviewer Assignment Contract

Every response that asks, recommends, or instructs a Review must resolve:

- `review_purpose`: the object and decision being reviewed;
- `reviewer_product`: one canonical product;
- `reviewer_role`: `advisory-reviewer`, `independent-reviewer`, or the existing
  bound `control-plane` final-Review role as applicable;
- `capability_profile`: the required capability ceiling;
- `independence_requirement`: the product/session/instance condition and the
  implementation identity it must differ from;
- `result_authority`: advisory input, governed Review evidence, or canonical
  control-plane decision.

Standalone user-facing wording may express these fields in one concise sentence
and does not create Handoff state. New governed Handoff work uses the schema-6
structured assignment in Decision 3. The control plane applies this routing order:

1. an existing canonical assignment wins;
2. an eligible product explicitly selected by the user is preserved;
3. otherwise the control plane recommends one concrete eligible product based
   on file/tool access, capability, and instance independence;
4. if no eligible independent instance is available, required Review is
   `BLOCKED` rather than downgraded to a generic destination.

The following wording is unresolved and invalid when it is the only destination:
“another agent”, “independent agent”, “another model”, or equivalent language.
Alternatives may be listed only after one concrete recommendation is named and
each alternative's authority is clear.

### 3. Schema-6 governed Reviewer Assignment

New Handoff-backed external work uses `schema_version: 6`. Schema 6 replaces the
old `independent_reviewer_assignment` field with one always-present immutable
`reviewer_assignment` mapping. The mapping contains the six conceptual Reviewer
Assignment fields plus the contract-local reviewer instance:

- the schema-6 required top-level field set is exactly the frozen schema-5
  required set, minus `independent_reviewer_assignment`, plus
  `reviewer_assignment`, with `schema_version` equal to `6`;
- the schema-6 exact immutable field set is exactly the frozen schema-5
  `readonly_fields` set, minus `independent_reviewer_assignment`, plus
  `reviewer_assignment`; every other lifecycle field/value rule remains
  unchanged unless this design explicitly overrides it;
- an extra top-level compatibility discriminator is forbidden because
  `schema_version: 6` is the sole structural discriminator.

```yaml
reviewer_assignment:
  review_purpose:
    object: current batch implementation, Report, contract, and evidence
    decision: decide pass, fail, or blocked for this governed Review gate
  agent_product: grok-cli
  agent_instance_id: grok-reviewer-01
  agent_role: independent-reviewer
  capability_profile: control-plane-high
  independence_requirement:
    kind: distinct-contract-instance
    distinct_from:
      - control_plane_owner
      - executor_assignment
  result_authority: governed-review-evidence
```

The schema is exact and fail-closed:

- `review_purpose` contains exactly non-blank `object` and `decision` strings;
- `agent_product`, `agent_instance_id`, `agent_role`, and
  `capability_profile` use the schema-6 assignment validators;
- `independence_requirement` contains exactly
  `kind: distinct-contract-instance` and a duplicate-free `distinct_from` list
  of canonical assignment field names;
- standard/strict Review requires role `independent-reviewer`, profile
  `control-plane-high`, and `distinct_from` exactly
  `control_plane_owner` plus `executor_assignment`; the resolved instance ID
  must differ from both;
- compact inline Review binds product/instance/role/profile exactly to
  `control_plane_owner`, uses `distinct_from: [executor_assignment]`, retains a
  non-blank `independent_review_not_applicable_reason`, and still records
  `result_authority: governed-review-evidence`;
- governed Handoff `result_authority` is exactly
  `governed-review-evidence`; it never authorizes a canonical transition;
- the complete `reviewer_assignment`, `schema_version`, and the other routing
  fields appear in the exact `readonly_fields` set and cannot change during a
  lifecycle transition.

Schema-2 evidence manifests remain byte-compatible. Their product/instance/role/
profile must match the resolved schema-6 reviewer assignment, while
`contract_revision` plus `canonical_sha256` bind the entire earlier canonical
status, including Review purpose, independence requirement, and result
authority. A mismatch or attempted assignment mutation is rejected before a
transition. No second evidence-schema version is needed because the existing
source fingerprint already binds these immutable fields.

### 4. Single managed global invariant

`references/shared-global-governance.md` is the single runtime-authoritative
managed body. Version 6 revises the first two existing invariants so role and
contract binding, rather than product shorthand, define authority:

```text
[CCG-001] Canonical authority belongs only to the bound instance whose product
is Codex and whose governing assignment binds role `control-plane`, profile
`control-plane-high`, instance identity, and contract. That instance is the sole
owner of routing, approval, canonical state transitions, evidence acceptance,
final verification, and final completion; no product name alone grants authority.
[CCG-002] Under schema 6, Codex, Pi, Antigravity CLI, and Grok CLI are equally
eligible for explicitly assigned executor or independent-reviewer roles. Their
outputs remain bounded evidence under the assigned role, profile, instance, and
contract and cannot self-authorize a canonical transition or final completion.
[CCG-010] New governed external Handoffs use schema 6 to bind Review purpose,
product, contract-local instance, role, profile, independence requirement, and
result authority. Active schema-4 or schema-5 contracts must drain under their
frozen validators before deployment; older complete contracts/evidence remain
immutable history and never authorize a schema-6 transition.
```

Version 6 also adds:

```text
[CCG-016] Every Review request, recommendation, prompt, or governed assignment
resolves a non-blank Review purpose and one concrete reviewer product, role,
capability profile, instance-independence requirement, and result authority.
Codex, Pi, Antigravity CLI, and Grok CLI are equally eligible as assigned
executors or independent reviewers; product identity never grants control-plane
authority. A missing or blank purpose, unresolved “other agent” destination,
product substitution, self-review, or missing required independent instance is
fail-closed.
```

The managed version becomes 6 and the manifest requires exact IDs `CCG-001`
through `CCG-016`. Validators and regression fixtures bind the complete semantic
body of revised `CCG-001`, revised `CCG-002`, revised `CCG-010`, and new
`CCG-016`, not only their IDs, count, version, or aggregate hash. Operational
references and templates implement this invariant but do not define a competing
authority.

### 5. Pi runtime target

The target resolves from `PI_CODING_AGENT_DIR`, defaulting to
`$HOME/.pi/agent`:

- Skill root: `${PI_CODING_AGENT_DIR}/skills`;
- global rule: `${PI_CODING_AGENT_DIR}/APPEND_SYSTEM.md`;
- executable: `pi`.

The first governed Pi apply requires the v6 block to be absent or to match the
reviewed expected pre-state. It appends exactly one managed block while
preserving all native bytes. Later applies replace only the bytes between the
versioned markers. Backups are mode `0600`, live outside discovery roots, and
their contents are never logged.

Pi target validation uses resolved path containment, regular-file/no-symlink
closure, portable relative-path/SHA parity, Skill quick validators, project
validators, and managed-block version/ID/body parity. Validation of the actual
native target does not invoke Pi and reads only declared Skill/global-rule paths.

Pi executable capability checks (`command -v pi`, version/help surface checks,
and any optional prompt probe) run in a fresh temporary process environment:
both `HOME` and `PI_CODING_AGENT_DIR` resolve inside the temporary root; inherited
Pi session/context/Skill loading is disabled; prompt probes additionally use
`--no-session`, `--no-context-files`, `--no-skills`, a read-only tool allowlist,
and network denial. The real native Pi root is denied by an enforceable
filesystem guard and is not an allowed probe input. The probe records only
command/result and sanitized capability names, then verifies the temporary root
inventory. If native-root denial or isolation cannot be mechanically proven, the
CLI probe is `BLOCKED` or omitted in favor of deterministic file/static checks;
direct native-root `pi --help`, version, or prompt probes are never acceptable
evidence. A prompt probe is supporting evidence only and cannot replace
deterministic validation.

The sync boundary excludes `auth.json`, sessions, histories, models/settings,
extensions, caches, logs, binaries, and every Pi-native file outside the single
managed block and declared Skill closure.

### 6. Source and validation surfaces

Router implementation may update only the approved logical surfaces:

- `SKILL.md`;
- `references/agent-capability-routing.md`;
- `references/response-patterns.md`;
- `references/shared-global-governance.md`;
- `references/cross-cli-sync.md`;
- `references/cross-cli-portable-manifest.json`;
- Handoff/approved-workflow/step-evidence/completion text needed to define
  schema-6 creation, immutable assignment/evidence binding, schema-4/schema-5
  drain, and four-product authority;
- `scripts/validate_core_gates.py` and `scripts/validate_cross_cli_sync.py`;
- focused tests/fixtures and necessary public documentation.

Companion implementation may update only:

- `SKILL.md`;
- Review/Handoff templates needed to express the assignment;
- `scripts/validate_templates.py`;
- focused tests/fixtures and necessary public documentation.

Any exact implementation file list must be frozen in the post-approval Plan and
Preflight. Scope expansion returns for approval.

### 7. Review assignments for this bootstrap

Every row is a complete Reviewer Assignment Contract. “Distinct” means the
reviewer instance did not author, execute, or canonically decide the artifact it
reviews; unavailable required independence returns `BLOCKED`.

| Gate | `review_purpose` | `reviewer_product` | `reviewer_role` | `capability_profile` | `independence_requirement` | `result_authority` |
|---|---|---|---|---|---|---|
| Proposal Review | Review the complete current proposal/design/tasks/spec revision and decide `PASS` or `BLOCKED` for presentation to the user as an implementation contract | `codex` | `independent-reviewer` | `control-plane-high` | user-opened new-window instance distinct from the authoring control plane | governed Proposal Review evidence only; cannot approve implementation |
| Plan Preflight Review | Review the complete current implementation plan and decide whether execution may start under the approved contract | `codex` | `independent-reviewer` | `control-plane-high` | user-opened new-window instance distinct from plan author and intended executor | governed Preflight evidence only; authorizes execution only after control-plane acceptance |
| Candidate source High Review | Review actual Router/Companion files, complete diffs, validators, tests, and adversarial routing behavior and decide whether runtime planning may begin | `codex` | `independent-reviewer` | `control-plane-high` | fresh new-window instance distinct from source authors/executors | governed implementation Review evidence only; cannot mutate runtime or canonical state |
| Sync-plan Review | Review path/hash plan, target/native preimages, isolation, backup/restore, sensitive exclusions, order, and stop conditions and decide whether target apply may begin | `codex` | `independent-reviewer` | `control-plane-high` | fresh new-window instance distinct from sync-plan author and target executor | governed sync-plan Review evidence only; cannot apply or authorize canonical transition |
| Pi adversarial Review | Adversarially review candidate schema-6 Pi role parity, isolated capability evidence, assignment behavior, and four-target result after candidate validation admits Pi | `pi` | `independent-reviewer` | `control-plane-high` | fresh isolated Pi session distinct from every Pi executor and artifact author | governed adversarial Review evidence only; bound Codex control plane decides acceptance |
| Learning Review | Review promoted non-sensitive learning artifacts and deterministic enforcement and decide whether closeout may proceed | `codex` | `independent-reviewer` | `control-plane-high` | fresh new-window instance distinct from learning author/promoter | governed learning Review evidence only; cannot reconcile or archive |
| Final High Review | Review the complete final source/runtime/evidence revision, actual files/diffs, final verification, residuals, and completion claims and decide `PASS` or `BLOCKED` | `codex` | `independent-reviewer` | `control-plane-high` | user-opened new-window instance distinct from authors, executors, and the bound decision owner | governed final Review evidence only; cannot declare canonical completion |

Canonical routing, evidence acceptance, archive, and completion remain decisions
of the current bound Codex `control-plane`/`control-plane-high` instance under the
approved contract; that decision-owner statement is not a substitute Review row.

Pi evidence created now cannot be backdated as authorization under the old
three-product enum. This bootstrap uses the already valid independent Codex
route until the candidate four-product validation and final source Review pass.

### 8. Schema-specific identity compatibility

Implementation uses separate closed constants and exact validation branches:

- schema-4 contracts and schema-1 evidence: the exact pre-change legacy sets and
  shapes, frozen without Pi;
- schema-5 contracts and schema-2 evidence when validated in a schema-5 parent
  context: the exact pre-change three-product enum and four-field assignment
  shape, frozen without Pi or Reviewer Assignment extensions;
- schema-6 contracts: exactly `codex`, `pi`, `antigravity-cli`, `grok-cli`, the
  exact `reviewer_assignment` mapping in Decision 3, and schema-2 evidence bound
  through the canonical schema-6 source fingerprint.

Before the first runtime apply, Preflight inventories every known canonical
`docs/agent-collab/*/status.md`. Any active schema-4 or schema-5 contract blocks
deployment until it reaches `complete` using the existing pre-upgrade runtime
and schema. The inventory is repeated immediately before apply. After the switch:

- Router/Companion current-status creation, validation, and transition entry
  points accept only schema 6 for current governed work;
- complete schema-4/schema-5 contracts and their evidence remain byte-immutable
  audit history and are never treated as current transition authority;
- no missing field, timestamp, file path, mtime, prose claim, or product value
  may classify an old-shape contract as grandfathered;
- Pi is rejected by schema 4 and schema 5 and accepted only by schema 6.

Legacy inspection is a separate read-only inventory/audit path, not a branch of
the current transition validator. It may parse frozen schema-4/schema-5 bytes
only to report path, schema, lifecycle, immutable fingerprint, and whether the
pre-deployment drain is clear. It cannot emit current-contract PASS, accept new
evidence, validate a transition, resume work, or authorize completion. After
cutover, any non-complete old schema is `BLOCKED`; a complete old schema remains
history only.

No expanded enum or assignment validator may be shared back into an older
branch. Router and Companion RED/GREEN tests must prove the drain gate, old-shape
rejection after cutover, immutable history handling, and schema-6-only Pi
acceptance. This change does not migrate or reinterpret any historical artifact.

## Validation Strategy

### RED/GREEN identity and routing tests

1. Pi executor and Pi reviewer assignments are rejected before implementation
   and accepted after implementation when instance IDs differ.
2. Same-instance Pi self-review and same-instance Codex self-review are rejected.
3. Unknown products and a non-Codex control-plane owner are rejected.
4. User-selected Pi cannot be silently substituted with another product.
5. A governed or standalone Review missing or blank purpose, product, role,
   profile, required instance condition, or result authority is rejected.
6. Standard/strict work without an independent reviewer is `BLOCKED`.
7. Reviewer PASS cannot promote canonical state or final completion.
8. Schema-4/schema-5 Pi assignments and legacy Pi evidence are rejected;
   equivalent schema-6 Pi assignments use the new four-product enum.
9. Schema-6 `reviewer_assignment` rejects missing/extra/blank purpose fields,
   wrong independence targets, mutable assignment deltas, identity/evidence
   mismatch, and non-evidence result authority.
10. Any active schema-4 or schema-5 Handoff blocks runtime deployment; after
    cutover an old-shape contract cannot start or resume a transition.

### Standalone forward-tests

1. “Ask another agent to Review” produces one concrete recommended product and
   the complete concise assignment contract.
2. “Send this to Pi for Review” preserves Pi and labels the result authority.
3. “Use a new Codex window” requires a distinct instance.
4. A Pi executor cannot assign the same Pi session as independent reviewer.
5. Advisory Review is clearly non-authoritative.
6. Required Review with no eligible instance returns `BLOCKED`.

### Cross-runtime tests

- The manifest and sync plan contain exactly the declared required targets:
  Codex, Pi, Antigravity CLI, and Grok CLI.
- All four receive identical portable source files and the v6 managed body.
- Pi path traversal, symlink escape, sensitive category, missing binary,
  missing Skill, managed-block mismatch, validator failure, or native-byte drift
  fails before or during only the affected target.
- Direct Pi CLI probes against the native agent root fail validation. Capability
  probes pass only with a fresh temporary `HOME`/`PI_CODING_AGENT_DIR`, denied
  native-root access, disabled inherited state, and sanitized evidence.
- `verify-all` fails if any declared required target is missing, stale,
  undiscoverable, or unverified.

### Review and completion evidence

Source validators, both unittest suites, cross-skill compatibility tests,
isolated forward-tests, sensitive scans, complete actual diffs, four-target
parity, and independent adversarial probes must pass. Project Learning Closeout,
fresh final verification, final High Review, task reconciliation, archive, and
post-archive strict validation follow the Completion Contract.

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| Pi is admitted in contracts before its runtime carries current rules | Candidate source Review precedes a reviewed target plan; global completion remains blocked until Pi parity and validation pass |
| Generic wording remains in unstructured chat | Add `CCG-016`, response-pattern enforcement, deterministic prompt fixtures, and isolated forward-tests |
| Product equality is mistaken for same-instance independence | Bind and compare contract-local instance IDs for every governed assignment |
| Product difference is mistaken for canonical authority | Keep control-plane ownership fixed to Codex and label result authority explicitly |
| Existing dirty Router work is overwritten | Bind current preimage hashes, patch only approved hunks, stop on drift, and Review the complete actual diff |
| Pi native configuration or secrets leak into sync evidence | Closed sync allowlist plus isolated temporary process roots, native-root denial, disabled inherited state, read-only/no-network prompt probes, and path/category-only diagnostics |
| One runtime fails after earlier targets changed | Per-target atomic apply, target-local secure backup, verified restoration, and stop before later targets |
| Same schema number ambiguously accepts old and new assignment shapes | Use schema 6 for the new exact shape, drain active schema-4/schema-5 before deployment, and reject old-shape current transitions after cutover |
| Rule duplication diverges | Keep the v6 managed block as the single runtime authority and mechanically validate revised `CCG-001/002/010/016` semantics plus version/ID/body parity |

## Migration / Rollback

1. After exact implementation approval, create fresh structured backups for the
   two source repositories and every target selected for mutation. Do not reuse
   historical backups.
2. Freeze current source and destination preimages with path, type, mode, and
   SHA-256 guards; preserve unrelated dirty bytes.
3. Complete RED, source implementation, GREEN, validators, forward-tests, and
   source High Review before any runtime mutation.
4. Inventory every known canonical Handoff root and stop until every active
   schema-4/schema-5 contract reaches `complete` under the pre-upgrade runtime;
   repeat the no-active-old-schema inventory immediately before apply.
5. Generate a path/hash-only sync plan and obtain the exact Sync-plan Review
   assignment defined in Decision 7.
6. Apply and verify one target at a time in this order: Codex, Pi,
   Antigravity CLI, Grok CLI. An implementation Plan may change the order only
   with an explicit, reviewed safety rationale.
7. On target failure, restore only that target from its fresh backup, verify the
   restored preimage, stop later targets, and retain the active change with an
   owner and resume condition.
8. Remove temporary backups only after all closeout gates and rollback needs
   are resolved. Never leave discoverable backup Skill directories.

No Git staging, commit, push, publication, deployment, or destructive cleanup is
authorized by this design or by later OpenSpec approval.

## Stop Conditions

- A source or destination preimage changes after Review.
- An unrelated dirty change would be overwritten or cannot be separated.
- Any active schema-4 or schema-5 Handoff remains at the deployment boundary.
- Pi paths cannot be resolved inside the declared root without symlink escape.
- A required Review purpose, product, instance, role, profile, independence
  condition, or authority field is missing or blank.
- Any source/runtime validator, forward-test, parity, discovery, sensitive scan,
  target restoration, or independent Review fails or is blocked.
- Implementation would need to read, copy, or alter credentials, sessions,
  settings, model stores, extensions, logs, caches, binaries, or unapproved
  native bytes.
- A Pi capability probe would resolve or gain access to the native Pi agent root,
  or its isolation/native-root denial cannot be mechanically proved.
