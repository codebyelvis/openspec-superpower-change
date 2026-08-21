## ADDED Requirements

### Requirement: Explicit governed Codex Skill update controller

The workflow SHALL provide an optional `codex-skill-update` controller for
registered Codex Skill dependency maintenance. Its narrowly scoped implicit
discovery and explicit `$codex-skill-update` invocation SHALL expose only
non-mutating audit, plan, verify, and report inspection. Mutation requests SHALL
return to Router-only internal transactions. Public and scheduled observation
and notification SHALL select only closed reviewed adapter IDs with fixed
absolute executable/argv schemas; registry, ref, package, and notification text
SHALL remain data and SHALL NOT select or interpolate code.

The controller SHALL NOT replace the Router as the control plane, become a
required dependency of the existing Scheme C execution path, or manufacture a
nonexistent native `codex skill update` command. State-changing apply,
initial `bootstrap-apply`, post-success rollback, `registry-replace`, schedule
installation/removal/replacement, and rollback-material cleanup SHALL re-enter
Router governance and SHALL require a current canonical approval artifact bound
to the exact action, target, scope, allowed paths, plan/receipt identity, and
expiry. Before mutation, an approved transaction SHALL durably activate a
single-use, restoration-only compensation lease. Automatic compensation under
that lease SHALL NOT require a second approval, but SHALL NOT continue forward
work after the original approval expires or is revoked.

#### Scenario: User asks for a Skill update audit

- **WHEN** the user explicitly invokes `$codex-skill-update`, sends
  `Codex Skill 更新巡检`, or asks to check one registered Skill
- **THEN** the controller runs the audit path
- **AND** it does not require or begin apply
- **AND** it does not change Router/Superpowers/Companion execution behavior

#### Scenario: User describes a native Codex subcommand

- **WHEN** the user informally says `codex skill update`
- **THEN** the Skill maps the intent to its own conversational or script
  interface
- **AND** it does not patch, shadow, or falsely document the `codex` CLI as
  providing that native subcommand

#### Scenario: State-changing update is requested

- **WHEN** the user asks to apply a Skill update or roll one back
- **THEN** the operation re-enters `openspec-superpower-change`
- **AND** platform command permission alone is not accepted as update approval
- **AND** the exact plan/receipt approval and any required Major OpenSpec
  approval are recorded before target mutation

### Requirement: Traceable managed registry and version evidence

The controller SHALL limit update guarantees to an explicit managed registry.
Each registered updateable package SHALL declare its canonical identity,
dependency group, installation mode, source/runtime observations, validation
contract, risk policy, and rollback adapter. Each discovered Skill entry SHALL
map its public name and relative path to exactly one package. One package MAY
expose multiple entries. Discovered Skills without registered provenance SHALL
be reported `UNMANAGED`; unknown or conflicting provenance SHALL NOT be guessed.
Observation methods SHALL be closed built-in adapter IDs rather than
registry-supplied commands.

The initial `bootstrap-apply` plan/approval SHALL bind the canonical registry
bytes, schema/revision/hash, complete package/entry/projection closure, selected
adapter identities/schemas, and exact initial controller-state layout.
Before planning or destination backup, the external Router SHALL load those
candidate bytes as data and construct the complete ownership graph against all
observed pre-state targets plus the Bootstrap Control Root without creating a
destination registry. Bootstrap SHALL install only those bytes. A later
registry change SHALL use a
fresh `registry-replace` plan, exact action approval, journal, conditional
final-child mutation, verification, and receipt. Any registry hash or closure
change SHALL invalidate the installed schedule-execution binding and SHALL
require a separately approved `schedule-replace` before scheduled package,
network, or notification activity resumes.

After registry load, the controller SHALL construct a global ownership graph for
every package source, runtime, release, discovery, projection, candidate,
backup, and managed target plus controller state and the Bootstrap Control
Root. It SHALL reject lexical
containment, realpath aliases, or device/inode aliases across ownership domains
except for an exact declared projection. The controller state root and OS
temporary root, plus a manager-owned common discovery container or release
store, SHALL be non-package graph anchors. A reviewed fixed layout MAY assign
distinct exact child entries/subtrees to controller roles, transactions, or
packages; controller-state metadata/backup/journal children SHALL remain one
declared controller domain. A package SHALL NOT claim or mutate a whole anchor.
Alias and overlap checks SHALL operate on exact leases and SHALL reject
cross-domain overlap or anchor-addressed mutation. The graph SHALL be
revalidated before any audit, plan, recovery, apply, rollback, schedule
mutation, or cleanup.
Filesystem use SHALL remain anchored to verified no-follow directory
descriptors or a platform-proven equivalent, bind existing components by
device/inode, anchor new children to a verified parent, and recheck identities
immediately before and after mutation. A component or symlink swap SHALL block
or trigger verified compensation rather than consume a stale resolved path. An
adapter without an equivalent safe primitive SHALL be blocked.

Every audit SHALL keep tested compatibility baseline, effective local version,
latest observed upstream version, and installation-channel available version as
four separate timestamped evidence values. Missing, stale, incomparable, or
conflicting evidence SHALL NOT produce `CURRENT`.

#### Scenario: Symlinked Git package has local divergence

- **GIVEN** a registered package exposes its Skills through a symlink to a Git
  checkout
- **WHEN** the checkout is dirty, has local commits, differs from its registered
  target, or is both ahead of and behind upstream
- **THEN** audit reports `DIVERGED` with non-sensitive evidence
- **AND** no pull, reset, clean, overwrite, or automatic patch resolution occurs

#### Scenario: Upstream and installation channel differ

- **WHEN** the latest observed upstream version differs from the version
  available through the registered installation channel
- **THEN** audit reports `CHANNEL_LAG`
- **AND** neither value is represented as the effective installed version

#### Scenario: Codex CLI version changes

- **WHEN** the Codex CLI or a plugin marketplace snapshot is refreshed
- **THEN** the controller re-observes the effective installed Skill separately
- **AND** it does not report the Skill updated unless installed-version and
  discovery evidence prove that state

#### Scenario: Discovered Skill has no registry entry

- **WHEN** Skill discovery finds an undeclared user or third-party Skill
- **THEN** audit reports it as `UNMANAGED`
- **AND** the controller does not invent a remote, channel, validator, or update
  guarantee

#### Scenario: One repository exposes a Skill collection

- **GIVEN** one registered Superpowers Git package exposes multiple
  `superpowers:*` Skill entries through one collection symlink
- **WHEN** audit or planning resolves their provenance and version
- **THEN** the package is the single update/version unit
- **AND** each discovered entry is verified against the package mapping
- **AND** no sub-Skill is independently pulled or replaced

#### Scenario: Duplicate discovered name has conflicting packages

- **WHEN** the same Skill name resolves from multiple packages, or an entry
  escapes its registered package root
- **THEN** audit records `MULTIPLE_SOURCES`
- **AND** apply eligibility is `BLOCKED` until the mapping is resolved

#### Scenario: Product-managed system or plugin Skill is discovered

- **WHEN** a Codex system Skill or manager-owned plugin Skill is inventoried
- **THEN** its package records its account/user scope and manager-owned
  observation source
- **AND** the generic controller does not overwrite system directories or plugin
  caches

#### Scenario: Two package identities alias one managed root

- **WHEN** different package IDs or root roles overlap, contain, or resolve to
  the same filesystem object outside an exact declared projection
- **THEN** audit records `BLOCKED_ROOT_ALIAS`
- **AND** no plan, mutation, rollback, or cleanup treats those identities as
  independent owners

#### Scenario: Roles share a manager or OS-owned container anchor

- **GIVEN** controller roles, transactions, or packages own reviewed distinct
  exact children/subtrees beneath one state, temporary, discovery, or release
  anchor
- **WHEN** the ownership graph is validated
- **THEN** the common anchored parent alone is not treated as a package overlap
- **AND** a whole-anchor package claim, cross-domain overlapping child lease, or
  mutation addressed to the anchor is `BLOCKED_ROOT_ALIAS`

#### Scenario: Registry content changes after bootstrap

- **WHEN** canonical registry bytes, schema/revision/hash, package/entry/
  projection closure, state layout, or adapter identity must change
- **THEN** the Router requires a fresh `registry-replace` plan and matching
  action approval before conditional replacement
- **AND** the prior installed schedule binding becomes drifted and cannot resume
  until a separately approved `schedule-replace` succeeds

### Requirement: Non-mutating scheduled freshness audit

The controller SHALL provide a one-shot read-only audit every Monday at 10:00
local time for the current macOS user and an on-demand equivalent. Audit MAY
inspect local metadata, use allowlisted network read operations, list installed
versions, and write sanitized reports inside the validated controller state
root. It SHALL NOT mutate a managed Skill, live Git checkout, plugin
marketplace, installer snapshot, registry entry, or update approval and SHALL
NOT chain into apply or rollback.

Every local or network observation and notification SHALL use a closed
read-only adapter with a fixed executable/argv schema, no shell or code
interpolation, and before/after installation-channel evidence. A registry value
that attempts to provide an executable, raw argv, mutation-capable flag, or
notification command SHALL be rejected before execution. Before invocation, an
external executable SHALL pass no-follow owner/type/mode checks and match the
adapter's reviewed content hash or platform code identity. The adapter SHALL
use a scrubbed fixed environment and disable ambient user/system config, hooks,
credential/proxy/remote helpers, interactive prompts, and mutation-capable
protocols unless an exact helper/protocol is separately reviewed and bound.
Unsupported or private observation SHALL return `UNKNOWN/BLOCKED` rather than
execute ambient configuration.

The controller SHALL treat a missing, failed, or older-than-eight-days
successful scheduled report as stale. A stale report SHALL NOT support a
`CURRENT` freshness claim.

The non-mutating schedule planner SHALL emit a canonical plan for exactly one
of `schedule-install`, `schedule-remove`, or `schedule-replace`. It SHALL bind
the fixed label `com.openai.codex.skill-update-audit`, launch domain
`gui/<current-uid>`, exact plist path
`<current-user-home>/Library/LaunchAgents/com.openai.codex.skill-update-audit.plist`
and allowed-path set, exact program argv whose controller path is inside one
content-addressed immutable payload rather than the movable discovery symlink,
interpreter/executable identity, payload digest, runtime-lock hash and exact
closure, expected active updater discovery-entry
`lstat`/`readlink`/resolved-target identity, controller state-root identity,
registry schema/revision/hash, dependency-group ID and complete
package/entry/projection closure, every selected
observation/notification adapter ID plus executable/code identity and
argv-schema hash, Monday
`Weekday=1`/`Hour=10`/`Minute=0` (`0` and `7` are Sunday), observed before plist
presence/hash/mode and normalized effective loaded-configuration fingerprint,
candidate plist hash where applicable, creation/expiry, and automatic-failure
rollback plus a fixed `launchctl` timeout. A loaded label whose effective
configuration cannot be proven to come from the exact observed plist SHALL be
`BLOCKED_SCHEDULE_DRIFT`. The normalized
fingerprint SHALL cover label, domain, program, argv, calendar, and every other
rendered controller-owned key needed for exact restore/verification. A loaded
label with no plist SHALL also be blocked. Changing a present registration
SHALL be `schedule-replace`, not `schedule-install`.

Every successful schedule transaction SHALL write a canonical receipt binding
the schedule plan and approval hashes, before/after plist hashes and modes,
before/after normalized effective loaded configurations, schedule-execution
binding, validation evidence, timestamp, and rollback availability. A receipt
SHALL NOT authorize a later remove or replace transaction.

Every installed job SHALL execute the exact content-addressed controller
payload, not a movable discovery path, and SHALL revalidate its payload digest,
canonical runtime lock and exact closure, expected active discovery identity,
interpreter/executable identity, approved state-root identity, registry hash,
group ID, complete closure, and adapter executable/code/argv-schema identities
before package reads, network access, or notification. Controller runtime,
active discovery, registry, or other binding drift SHALL return
`BLOCKED_SCHEDULE_BINDING_DRIFT`, SHALL NOT produce an ordinary freshness
result, and SHALL require a fresh `schedule-replace` plan and approval.

#### Scenario: Weekly audit runs unattended

- **WHEN** the user-level scheduler invokes the non-interactive audit
- **THEN** the process performs only read operations against managed targets and
  writes a sanitized report under the controller state root
- **AND** the process exits without invoking plan, apply, rollback, plugin
  refresh, or live-checkout fetch

#### Scenario: Registry attempts to inject an observation command

- **WHEN** a registry supplies an executable, raw argv, mutation-capable
  observation, shell metacharacter, or notification program
- **THEN** audit rejects it before invoking any external process
- **AND** installation-channel snapshots remain unchanged

#### Scenario: Scheduled evidence is stale

- **WHEN** the latest successful scheduled report is missing or older than the
  freshness limit
- **THEN** the controller marks the evidence stale and refreshes or reports
  `UNKNOWN/BLOCKED`
- **AND** it does not reuse the stale result as proof that dependencies are
  current

#### Scenario: Schedule registration is installed or removed

- **WHEN** the user asks to install, remove, or change the LaunchAgent
  registration
- **THEN** the non-mutating planner records install, remove, or replace with the
  exact label, domain, plist, content-addressed payload/runtime-lock/active
  discovery identity, argv/interpreter hashes, state-root identity, registry and
  group closure, cadence, loaded-configuration pre-state, allowed paths,
  rollback, and expiry
- **AND** the Router records a matching exact action approval before filesystem
  or `launchctl` mutation
- **AND** the transaction backs up the pre-state outside discovery roots, uses
  no-replace or atomic exchange while preserving/verifying the displaced plist,
  verifies the exact label/plist/arguments, and automatically restores on
  failure

#### Scenario: Existing registration is changed

- **GIVEN** the fixed LaunchAgent label or plist is already present
- **WHEN** its bytes, arguments, cadence, or loaded state must change
- **THEN** the schedule plan action is `schedule-replace`
- **AND** neither an install approval nor the earlier receipt authorizes the
  replacement

#### Scenario: Loaded configuration does not match the observed plist

- **WHEN** the label is loaded from an unprovable or different effective
  configuration, or is loaded while the exact plist is absent
- **THEN** schedule planning returns `BLOCKED_SCHEDULE_DRIFT`
- **AND** no install, remove, replace, or guessed restoration runs

#### Scenario: Schedule transaction succeeds

- **WHEN** an approved schedule install, remove, or replace passes verification
- **THEN** its receipt binds plan/approval hashes and exact before/after
  plist/hash/mode/effective-loaded-configuration state
- **AND** later schedule mutation requires a fresh current plan and approval

#### Scenario: Scheduled execution binding drifts after installation

- **WHEN** the scheduled payload/runtime lock, active updater discovery,
  interpreter, state-root identity, registry hash, group ID, adapter identity,
  or complete package/entry/projection closure differs from the installed
  binding
- **THEN** the job returns `BLOCKED_SCHEDULE_BINDING_DRIFT` before package,
  network, or notification activity
- **AND** a fresh schedule-replace plan and approval are required

#### Scenario: Scheduled job execution is checked for mutation

- **GIVEN** the approved schedule registration is already installed
- **WHEN** its one-shot audit executes
- **THEN** managed target snapshots remain byte/path/mode/symlink identical
- **AND** only the validated controller state root may contain
  controller-created filesystem changes such as reports, locks, or timestamps
- **AND** a permitted local notification does not authorize any managed-target
  or installation-channel mutation

#### Scenario: Scheduled audit finds attention-required state

- **WHEN** audit finds an update, blocker, unmanaged/unknown required package,
  or audit failure
- **THEN** it emits one local notification containing only package names and
  headline statuses
- **AND** paths, refs, hashes, commands, error detail, credentials, and file
  contents are excluded
- **AND** notification delivery status is recorded without changing the audit
  result

#### Scenario: Scheduled audit is current

- **WHEN** all required packages are freshly `CURRENT` with no blocker
- **THEN** the audit writes its sanitized report
- **AND** it emits no update notification

#### Scenario: Controller state root overlaps a managed path

- **WHEN** the default or overridden state root is unowned, weakly permissioned,
  equal to, inside, contains, or resolves through a symlink into a discovery,
  source, runtime, release, candidate, or managed target root
- **THEN** the controller rejects it before the first write
- **AND** audit does not create a report, lock, registry, plan, receipt, or
  backup there

#### Scenario: Declared projection resolves to its managed target

- **GIVEN** the registry declares either a discovery symlink to an exact
  immutable release payload or a collection symlink to an exact authoritative
  package root
- **WHEN** audit verifies the lexical entry with `lstat`/`readlink`
- **THEN** that declared projection relationship is allowed
- **AND** global state, temporary candidate, compensation, backup, source,
  runtime, release-store, and managed-target isolation remains enforced

#### Scenario: Projection is chained, escaping, or unexpected

- **WHEN** a projection resolves outside its declared contained target, uses an
  undeclared chain, or differs from its registered target
- **THEN** audit records `DIVERGED` or `MULTIPLE_SOURCES`
- **AND** apply eligibility is `BLOCKED`

### Requirement: Deterministic compound update result

Every audit result SHALL keep `freshness_status`, `observations`,
`apply_eligibility`, and sorted unique `reason_codes` as separate structured
fields. Freshness SHALL use
`UNMANAGED > UNKNOWN > UPDATE_AVAILABLE > CURRENT`; apply eligibility SHALL use
`BLOCKED_MAJOR > BLOCKED > ELIGIBLE`. Observations including `DIVERGED`,
`CHANNEL_LAG`, `STALE_EVIDENCE`, and `MULTIPLE_SOURCES` SHALL remain present even
when a stronger apply blocker exists.

A `BLOCKED_MAJOR` reason SHALL map to `apply_eligibility=BLOCKED_MAJOR`.
Specialized reasons including `BLOCKED_LAYOUT_MIGRATION`,
`BLOCKED_RELEASE_COLLISION`, `BLOCKED_SELF_UPDATE`,
`BLOCKED_CHANNEL_MUTATION`, `BLOCKED_SCHEDULE_DRIFT`,
`BLOCKED_SCHEDULE_BINDING_DRIFT`, `BLOCKED_ROOT_ALIAS`, and
`BLOCKED_RECOVERY_REQUIRED` SHALL map to `apply_eligibility=BLOCKED` without
hiding any other reason. Mutation attempts SHALL report exactly one
`transaction_result`: `SUCCEEDED`, `BLOCKED`, `FAILED_COMPENSATED`, or
`RECOVERY_REQUIRED`. `FAILED_COMPENSATED` SHALL require verified restoration;
`RECOVERY_REQUIRED` SHALL block all new work.

#### Scenario: Divergence and Major gap coexist

- **GIVEN** a package has a local divergence and its candidate crosses a Major
  workflow boundary
- **WHEN** audit classifies the package
- **THEN** observations include `DIVERGED`
- **AND** apply eligibility is `BLOCKED_MAJOR`
- **AND** neither fact is hidden by a single ambiguous status label

#### Scenario: Compound status is rendered

- **WHEN** more than one freshness, observation, or eligibility condition
  applies
- **THEN** the controller uses the normative structured-field precedence
- **AND** table-driven fixtures produce one deterministic result for every
  covered pair

#### Scenario: Specialized blocker and transaction result are rendered

- **WHEN** a specialized blocker or failed transaction occurs
- **THEN** the controller retains its exact reason code and maps it to the
  normative apply eligibility
- **AND** it does not represent an unverified recovery as
  `FAILED_COMPENSATED` or `SUCCEEDED`

### Requirement: Immutable approval-bound update plan

Every update plan SHALL use an immutable candidate and canonical serialization
whose identifier binds the registry revision, canonical package ID, complete
expected discovered-entry/projection set, resolved authoritative/projection
targets, current fingerprint, candidate ref/fingerprint, exact allowed paths,
installation adapter, validation executable/code identity, argv/cwd, scrubbed
environment, network/write-containment policy, fixed adapter/boundary timeouts,
expected evidence, risk, expiry, stop conditions, and rollback strategy. An
adapter that cannot prove validator containment within the approved policy
SHALL be blocked.

Every installation mode MAY return a canonical diagnostic planning result, but
when an isolated candidate and the complete immutable-plan contract cannot be
proven, that result SHALL contain the exact blocker/resume condition and SHALL
NOT contain an actionable `plan-id`. A diagnostic result SHALL NOT be accepted
by approval minting or apply.

Each adapter SHALL define a canonical complete candidate fingerprint. A
filesystem candidate SHALL bind a sorted `lstat` inventory of path, type, mode,
regular-file content hash, symlink target, and link multiplicity, rejecting
escapes and undeclared hardlinks. A Git candidate SHALL additionally bind
repository/object format, commit/tree/ref, submodule identities, and the same
exact checked-out closure. A ref or version label alone SHALL NOT satisfy
immutable candidate binding.

Candidate retrieval SHALL use a restrictive OS temporary directory that is
outside and non-overlapping with state, discovery, source, runtime, release, and
managed target roots. Temporary candidate bytes SHALL be removed after planning;
apply SHALL retrieve and verify the same immutable fingerprint again.
For `git-symlink`, a user-requested plan MAY create only its fixed ephemeral
candidate object/checkout store, and an exact apply approval MAY create only the
bound immutable checkout under the allowed release root. Neither action SHALL
initialize or mutate a sibling source, live checkout, or other user repository,
or grant staging, commit, branch/tag/remote mutation, reset, clean, push, or
publication. Both SHALL use a closed Git materialization adapter with fixed
executable/code identity, scrubbed environment, disabled ambient
config/hooks/helpers/prompts, and bound protocol/ref policy.

Normal plans SHALL be stored under the validated controller state root. Before
first installation, the exact Major source-implementation authorization MAY
create only the restrictive Router-owned Bootstrap Control Root
`${CODEX_HOME}/openspec-superpower-change/bootstrap-control/codex-skill-update/`
outside every updater runtime/state/release/discovery/schedule destination, its
missing fixed manager anchors, and one immutable child workspace for each Major
authorization manifest. The canonical `bootstrap-apply` authority records,
plan, approval, compensation lease, journal, receipt, and closeout evidence
SHALL remain in the selected manifest-hash workspace; planning SHALL NOT create
or write the updater destination state root. The bootstrap root SHALL use
verified no-follow current-user `0700` directories and `0600` files and SHALL
participate in the global ownership graph.
Every absent fixed ancestor after the validated `${CODEX_HOME}` SHALL be
created separately with directory-FD-anchored no-replace semantics, restrictive
mode, parent fsync, and post-create owner/type/mode/device/inode verification.
The `openspec-superpower-change/` and `bootstrap-control/` containers SHALL be
manager-owned graph anchors, not package roots, and an existing safe anchor MAY
contain only separately declared child leases.

The final package root SHALL be constructed as a restrictive same-filesystem
sibling candidate whose fixed closure initially contains canonical
`control-root.json`, a mode-`0600` single-link `operation.lock`, and mode-`0700`
`authorizations/`. The stable marker SHALL bind exactly schema, absolute target,
package ID, and Router control-plane ID; it SHALL NOT bind a decision/session
instance, change-id, or Major manifest. The candidate name SHALL be bound to the
stable marker hash and SHALL be a temporary graph lease. Promotion SHALL use
atomic no-replace plus parent fsync. A matching stranded candidate or target
with the exact stable marker/closure SHALL be resume/reuse-only. An unmarked
empty target, mismatched marker, unsafe ancestor, undeclared sibling, or
foreign/ambiguous content SHALL block without repair, overwrite, deletion, or
guessed adoption.

Root initialization SHALL be the sole exception to acquiring the controller
operation lock first. Before promotion it MAY only verify/create the disclosed
fixed anchors and root closure; it SHALL NOT probe updater targets, create a
plan, invoke package/network adapters, or write updater destinations. After
promotion/reuse it SHALL immediately open, validate, and acquire the embedded
operation lock before any other work.

While holding that lock, the Router SHALL create or verify one immutable
`authorizations/<manifest-sha256>/` workspace. Its canonical marker SHALL bind
the manifest hash, change-id, raw artifact hashes, projection digest, decision
provenance/time, and control-plane instance. Its fixed layout SHALL contain only
verified no-overwrite content-addressed copies of the Major manifest/raw
snapshots, short authority lock and append-only revocations, plans, approvals,
leases, journals, receipts, and closeout evidence. Workspace creation SHALL use
same-filesystem no-replace plus fsync. Reapproval SHALL
create a new manifest-hash workspace and preserve all older workspaces and
receipts; it SHALL NOT rewrite the stable marker. An existing workspace SHALL
be reuse-only after exact marker/closure verification, and a known incomplete
journal there SHALL enter recovery. Before selecting or creating a workspace,
the locked Router SHALL enumerate and validate every declared workspace. Any
incomplete journal in an older workspace SHALL finish lease-bound recovery or
block all new work; reapproval SHALL NOT bypass it.

#### Scenario: Bootstrap control-root creation is interrupted

- **GIVEN** the exact Major authorization permits only the disclosed bootstrap
  control path and its missing fixed manager anchors
- **WHEN** creation stops after an ancestor or marked sibling candidate becomes
  durable but before final-root promotion
- **THEN** restart verifies and resumes only the exact stable anchor/candidate
  marker, identities, modes, and graph lease
- **AND** an unmarked empty target, foreign sibling, mismatched marker, or unsafe
  ancestor blocks without being repaired, deleted, or adopted

#### Scenario: Major contract is reapproved after root creation

- **GIVEN** the stable Bootstrap Control Root and an older manifest workspace
  already exist with exact safe closure
- **WHEN** a corrected contract receives a new immutable Major manifest
- **THEN** the Router preserves the stable marker and every old workspace and
  creates a new no-overwrite workspace named by the new manifest hash
- **AND** no plan, approval, journal, receipt, or closeout record from another
  workspace is adopted or rewritten
- **AND** any incomplete journal in an older workspace is recovered or blocks
  before the new workspace may plan or mutate

Plan creation SHALL grant no update authority. Immediately before apply the
controller SHALL recompute every current-state and plan binding and SHALL reject
tampered, expired, mismatched, or stale plans. Major version, trigger, routing,
authority, evidence, completion, installation-lifecycle, or unresolved local
divergence changes SHALL be `BLOCKED_MAJOR` until an exact OpenSpec contract is
approved. A Major plan SHALL bind the exact change-id,
immutable authorization-manifest SHA-256, approved raw
proposal/design/spec/tasks SHA-256 set, canonical contract-projection digest,
direct-user decision provenance, and decision timestamp. The projection SHALL
replace only line-leading `- [ ]`, `- [x]`, or `- [X]` markers in proposal and
tasks with `- [ ]`, leave design/spec bytes unchanged, and hash a
domain-prefixed canonical inventory of the four relative paths and projected
content hashes as
`{"files":[{"path":...,"sha256":...}],"schema":1}` with keys sorted and files
sorted by UTF-8 bytewise change-root-relative path in this exact order:
`design.md`, `proposal.md`, `specs/skill-update-governance/spec.md`, and
`tasks.md`. It SHALL use the exact UTF-8 prefix
`openspec-major-contract-projection-v1` followed by one NUL byte. It SHALL
preserve all other bytes.
Only after task 2.1 exact materialization and post-verification SHALL later
checklist progress avoid rewriting the manifest. Before that boundary the
complete approved material inventory SHALL remain byte-frozen. Any other artifact-byte change SHALL
invalidate Major eligibility until a new exact approval and manifest exist.

Before any post-approval checklist marker changes, the controller SHALL preserve
the exact approved bytes of all four artifacts at
`approvals/artifacts/<artifact-sha256>` with verified-parent, no-follow,
no-overwrite creation. Existing snapshots SHALL be reuse-only after exact
regular-file/content verification; missing, unsafe, or colliding evidence SHALL
block Major eligibility.

The authorization manifest SHALL be canonical UTF-8 JSON with sorted keys and
compact separators containing exactly: integer `schema` value `1`;
`change_id`; `artifact_hashes` as a path-to-SHA-256 object for the four raw
artifacts; `contract_projection_sha256`;
`source_bootstrap_prestate_sha256`; `source_bootstrap_material_hashes` as the
exact path-to-SHA-256 object for the complete approved untracked source/supporting
files; `source_bootstrap_git` containing exactly `executable_path`,
`executable_sha256`, `version`, `repository_root`, `git_common_dir`,
`object_format`, `base_commit`, `base_tree`, `branch_ref`, `worktree_path`, and
`worktree_admin_path`; `source_bootstrap_sandbox` containing exactly
`executable_path`, `executable_sha256`, `profile_sha256`,
`write_allowlist_sha256`, `invocation_argv_sha256`, `network_policy` (`DENY`),
`child_exec_policy` (`HELPER_AND_FIXED_READ_ONLY_GIT_ONLY`),
`source_bootstrap_helper` containing exactly `executable_path`,
`executable_sha256`, `fixed_argv`, `fixed_environment`, and
`fd_binding_protocol` (which SHALL enumerate every required internally retained
mutable-parent directory descriptor and no-follow continuity check used before
the first write); `decision_provenance` value
`direct-user-confirmation`; `decision_timestamp` as UTC RFC 3339; and
`control_plane_instance`. It SHALL contain no transcript or private prompt, and
its byte SHA-256 SHALL be its immutable identity and filename. Reapproval SHALL
create new snapshots as needed and a new manifest rather than rewrite prior
evidence.

From the exact user decision through snapshots, manifest/profile/journal setup,
and successful task 2.1 post-verification, all approved material paths
SHALL remain byte-identical to their manifest hashes. No checklist marker SHALL
change, and tasks 1.5/2.1 SHALL remain unchecked during that interval. Task 2.1
SHALL materialize each approved byte stream exactly once, no-overwrite. Only
after successful post-verification MAY task 1.5/2.1 markers and later
checklist-only progress change under the normalized projection rule. Any
pre-bootstrap marker or other byte drift SHALL block and require reapproval,
not overwrite or reconciliation.

The prior `add-codex-skill-update` ref/worktree/admin path SHALL be a
preserve-only quarantine when its current artifact bytes require a Major
manifest or raw snapshots that are absent there. Reapproval SHALL NOT repair,
reuse, delete, clean, or adopt that attempt. The replacement approval SHALL
name a distinct absent ref/worktree/admin target and bind the exact quarantine
state into its prestate; quarantine drift SHALL block before target reservation
or Git execution.

`source_bootstrap_prestate_sha256` SHALL be SHA-256 over the exact UTF-8 prefix
`source-worktree-bootstrap-prestate-v2`, one NUL, and canonical sorted-key
compact JSON containing exactly `schema` (integer `2`), `repository`,
`git_executable`, `base_commit`, `base_tree`, `symbolic_head`, `refs`,
`ref_exclusions`, `worktrees`, `local_config_sha256`, `parent_closure`,
`target_absence`, and `quarantines`.
`repository` SHALL contain exactly `repository_root`, `repository_root_dev`,
`repository_root_ino`, `git_common_dir`, `git_common_dir_dev`,
`git_common_dir_ino`, and `object_format`. `git_executable` SHALL contain
exactly `path`, `sha256`, and `version`. Each `refs` entry SHALL contain exactly
`name`, `object_oid`, and `object_type`, sorted by the UTF-8 bytes of those
fields. `refs` SHALL contain every observed ref except names under an exact
bound exclusion. `ref_exclusions` SHALL contain exactly one entry containing
exactly `prefix` (`refs/codex/turn-diffs/`) and `policy`
(`OBSERVE_ALLOW_EXTERNAL_DRIFT_DENY_BOOTSTRAP_WRITE`). That control-plane-owned
checkpoint namespace SHALL be observed for diagnostics but not content-bound,
SHALL NOT occur in the sandbox write allowlist, and no other namespace SHALL be
excluded. Each `worktrees` entry SHALL contain exactly `path`, `head`, and
`branch`, with JSON `null` for a detached branch, sorted by path bytes.
`local_config_sha256` SHALL hash the exact no-follow, single-link common
`.git/config` bytes with UTF-8 prefix `source-worktree-local-config-v1` and one
NUL; that config SHALL be strictly parsed before read-only Git inspection or helper execution.

`parent_closure` SHALL be path-bytewise sorted; every entry SHALL contain
exactly `path`, `type` (`directory`), `dev`, `ino`, `uid`, `mode`, and `nlink`.
It SHALL include every existing component from filesystem anchors through the
repository root, common Git directory, `.git/refs/heads`,
`.git/logs/refs/heads`, `.git/worktrees`, disclosed worktree parent, approval
directory, and source-bootstrap directory. No
component SHALL be a symlink or group/world writable at a mutable
manager-owned anchor. `target_absence` SHALL contain exactly `branch_ref`,
`branch_reflog_path`, `worktree_path`, and `worktree_admin_path`, each
`ABSENT`.
`quarantines` SHALL be sorted by `worktree_path`. Each entry SHALL contain
exactly `status` (`BLOCKED_SOURCE_WORKTREE_RECOVERY`), `branch_ref`,
`worktree_path`, `worktree_dev`, `worktree_ino`, `worktree_admin_path`,
`worktree_admin_dev`, `worktree_admin_ino`, `head`, `tree`,
`observed_manifest_sha256`, `missing_required_manifest_sha256`,
`observed_artifact_hashes` as a sorted path-to-SHA-256 object,
`missing_required_snapshot_sha256` as a sorted array, and `mutation_policy`
(`PRESERVE_NO_REUSE_REPAIR_DELETE`).
Paths, hashes, versions, refs, OIDs, types, and absence values SHALL be JSON
strings; every `*_dev`, `*_ino`, `dev`, `ino`, `uid`, and `nlink` SHALL be an
integer; `mode` SHALL be a
four-digit lowercase octal string. No undeclared key or JSON coercion SHALL be
accepted.
The reviewed prestate evidence file SHALL contain exactly that canonical compact
JSON followed by one LF. The digest input SHALL be the exact file bytes with
that one final LF removed, without parsing or reserialization; any missing or
extra line ending or other byte drift SHALL block.

Those `nlink` values SHALL be the reviewed pre-decision baseline for the bound
APFS volume, where each durable immediate child entry changes the observed
directory `st_nlink`, including a regular file. Parent-closure validation SHALL
use one closed phase table for both lexical `lstat` and retained-descriptor
`fstat` checks. `approval-recorded` SHALL permit only approval-directory `+1`
for the new immutable manifest. `journal-ready` SHALL permit only approval-
directory `+2` for that manifest plus the held source-bootstrap lock and source-
bootstrap-directory `+1` for the no-replace journal. `post-bootstrap` SHALL
retain those deltas and permit only branch-ref-parent `+1`, branch-reflog-parent
`+1`, worktree-admin-parent `+1`, and replacement-worktree-parent `+1` for the
final ref, reflog, admin directory, and target directory. The transient ref and
reflog `.lock` entries SHALL be absent at the post phase. Every unlisted link-
count delta, unknown phase, or device/inode/owner/mode/type drift SHALL block.

After the exact decision, the decision recorder MAY create only the four raw
content-addressed snapshots and one canonical manifest with verified-parent
no-follow/no-overwrite writes; it SHALL NOT create replacement source state.
The manifest-bound helper SHALL be the sole task-2.1 executor. Its fixed
external argv SHALL be
`-I -S <absolute-approved-helper-path> --launch`; that read-only launcher SHALL
revalidate the exact artifact/snapshot/material/profile/manifest closure and
then `execve` the manifest-bound `/usr/bin/sandbox-exec` with the exact profile
bytes inline, exact interpreter, and `--contained` helper argv.
`invocation_argv_sha256` SHALL hash UTF-8 prefix
`source-worktree-sandbox-exec-vector-v1`, one NUL, and canonical compact JSON
`{"argv":[...],"schema":1}` containing that complete `execve` vector.
Because the reviewed prestate precedes the new manifest, the launcher's and
contained helper's initial parent checks SHALL apply `approval-recorded`, not
the unadjusted pre-decision link count.

The canonical profile SHALL deny network, every process execution except the
exact helper interpreter and manifest-bound Git binary, and all writes except
`/dev/null`, the exact source-bootstrap lock/journal, branch ref/ref-lock,
branch reflog/log-lock, reserved target subtree, and exact worktree-admin
subtree. The contained helper SHALL compare the profile file to its exact
expected bytes and SHALL actively attest network denial, forbidden write-open
denial, and unauthorized child-exec denial. Direct unsandboxed `--contained`
execution SHALL block. The only Git child invocations SHALL be a source-bound
fixed read-only allowlist of `rev-parse`, `symbolic-ref`, `for-each-ref`,
`worktree list`, `ls-tree`, `cat-file`, and post-bootstrap `status` with scrubbed
configuration and `GIT_OPTIONAL_LOCKS=0`.

Inside the sandbox the helper SHALL open every filesystem component no-follow
and internally retain descriptors for repository root, Git common directory,
`.git/refs/heads`, `.git/logs/refs/heads`, `.git/worktrees`, worktree parent,
approval directory, and source-bootstrap directory. Before the first
potentially creating open and again after journal setup it SHALL re-`fstat`
each against the schema-2 identity and reopen every absolute and
descriptor-relative lexical chain no-follow to prove continuity. It SHALL
revalidate the complete quarantine bytes/absence evidence and exact new
ref/reflog/admin/target absence at that boundary.
The first check SHALL use `approval-recorded`; the post-lock-and-journal check,
which remains before any replacement-state write, SHALL use `journal-ready`.

Only after that boundary SHALL it open and fsync the current-user-owned,
single-link mode-`0600` exclusive `approvals/source-bootstrap.lock`, fsync the
approval parent, create the canonical journal no-replace, and fsync the journal
and source-bootstrap parent. Under the held worktree-parent descriptor it SHALL
reserve the target directory by atomic `mkdirat` no-replace with mode `0700`,
record and retain its device/inode, while leaving ref/reflog/admin absent.

Because macOS `/dev/fd/<directory-fd>` is not traversable as a pathname prefix,
the helper SHALL NOT pass repository or target paths to a mutating Git command.
It SHALL create the exact loose branch ref and reflog through `.lock`
no-replace files plus same-directory descriptor-relative hard-link promotion
that fails when the destination exists, followed by lock unlink, create the
exact worktree-admin child and its `commondir`, `gitdir`, `HEAD`, `ORIG_HEAD`,
and `logs/HEAD` files no-replace, then create only the target `.git` link file.
It SHALL fsync every file and affected retained directory. Interruption SHALL
preserve the incomplete target as recovery evidence and block reuse or cleanup.

Before the helper writes replacement state, fixed read-only Git
`ls-tree`/`cat-file` plumbing SHALL preload and verify the bound regular-blob
base closure and independently recompute every SHA-1
`blob <length>\0<bytes>` OID under scrubbed
system/global/inherited config, restrictive empty config homes,
`GIT_OPTIONAL_LOCKS=0`, and hook/filter/helper/prompt/network denial. The
descriptor-read local config SHALL reject executable hooks, filters, diff/merge
drivers, helpers, aliases, includes, protocol rewrites, submodule commands,
worktree config, or maintenance. No `worktree add`, `--force`, `-B`, checkout,
switch, reset, clean, fetch, clone, remote, submodule, maintenance, credential,
or arbitrary Git mutation command is authorized.

Before first write and at post-verification, task 2.1 SHALL revalidate every
retained descriptor against the exact phase-specific `parent_closure`, reopen
every lexical component no-follow, and prove the reserved target/admin paths
still name their retained inodes. If the platform cannot prove descriptor-rooted target binding before the
first source write, the no-replace property for ref/admin paths, or the profile's exact
deny-by-default write allowlist, descriptor-rooted mutable-parent writes, or
first-write re-fstat continuity, task 2.1 SHALL NOT launch the helper or write source state.
Post-verification SHALL use `post-bootstrap` only after ref/reflog lock
promotion and lock-file removal. A regression test SHALL bind every allowed
per-phase delta and SHALL reject an unknown phase.
The profile SHALL be stored no-overwrite at
`approvals/source-bootstrap/profiles/<profile-sha256>.sb`.
`write_allowlist_sha256` SHALL hash the exact UTF-8 prefix
`source-worktree-write-allowlist-v1`, one NUL, and canonical sorted-key compact
JSON `{"paths":[{"access":...,"path":...}],"schema":1}`. Each sorted entry
SHALL contain exactly `access` (`create-or-write` or `read-write-device`) and
one absolute `path`; the only entries SHALL be `/dev/null` as
`read-write-device` plus the source-bootstrap lock/journal, ref/ref-lock,
reflog/log-lock, reserved target, and exact admin child as `create-or-write`.
If the platform cannot prove the
exact profile implements this deny-by-default allowlist, no-replace ref/admin
creation, or descriptor continuity, the helper SHALL NOT run.

Task 2.1 SHALL materialize the exact base tree without checkout using only fixed
`ls-tree`/`cat-file` raw-blob plumbing plus directory-FD-anchored no-follow/
no-overwrite writes and parent fsync. The approved base SHALL contain only
regular `100644`/`100755` entries; any other tree mode SHALL block. It SHALL
then copy only manifest-bound untracked source/supporting material, raw
snapshots, manifest, and newly reapproved content-addressed sandbox profile as
their exact bound bytes with the same contained mechanism. It SHALL NOT copy or
adopt any prior-attempt manifest or snapshot. Existing profile bytes MAY be
reused only as immutable mechanism content when they independently equal the
current helper's exact expected profile, the new manifest binds their hash, and
the new exact user decision approves them. Prior profile use SHALL grant no
authority; the quarantined `892aec1c...` profile SHALL fail the current expected-
bytes/hash check. It SHALL create a Git index v2
containing `DIRC`, path-byte-sorted base entries, each held-target-FD stat tuple,
bound mode/OID/path, eight-byte entry padding, and a SHA-1 trailer; the admin
`index` SHALL be written no-follow/no-overwrite and fsynced with its parents.
Post-verification SHALL prove that parent identities,
quarantines, exclusion policy, and non-excluded refs/worktrees/local config
differ from prestate only through the named new `add-codex-skill-update-v2` ref
at the bound commit and named replacement worktree/admin mapping with the bound
HEAD/tree, SHALL prove the bootstrap had no write capability for the excluded
checkpoint namespace even if diagnostic external drift was observed, and SHALL verify
the reserved target/admin identities, exact ref/reflog/admin bytes and base
tree, tracked-clean status, exact file/directory path closure including
directory owner/mode and no extra empty or ignored directory, exact approved
untracked hashes, and
unchanged index bytes across read-only `status`. It SHALL re-read the full
quarantine artifact/manifest/missing-manifest/missing-snapshot evidence after
registration. Parent/target exchange, existing
targets, wrong base/identity, executable config, filter execution, extra
mutation, or interruption residue SHALL return
`BLOCKED_SOURCE_WORKTREE_RECOVERY`; no reuse, force, reset, repair, deletion,
or cleanup is authorized by the source-implementation approval.

The public maintenance CLI SHALL NOT expose a mutation or approval-minting
command. After the user's exact decision, the Router SHALL record a canonical
approval artifact containing decision owner/instance/provenance, action, target,
scope hash, allowed-path-set hash, plan/receipt ID, and expiry. The internal
transaction SHALL reject a missing, stale, tampered, or field-mismatched
artifact. Action SHALL be exactly one of `apply`, `bootstrap-apply`, `rollback`,
`registry-replace`, `schedule-install`, `schedule-remove`, `schedule-replace`,
or `cleanup`. The artifact is auditable governance evidence and SHALL NOT be
represented as cryptographic proof of human identity. For a Major plan, its
scope hash and receipt SHALL retain the identical OpenSpec authorization
binding; missing or mismatched artifact hashes SHALL remain `BLOCKED_MAJOR`.
A later direct-user revocation SHALL use an independent Router-owned
`authority/` channel under validated normal state or the selected bootstrap
workspace. That channel SHALL contain a current-user-owned mode-`0600`,
single-link, no-follow `authority.lock` and an append-only
`revocations/<approval-sha256>.json` namespace. A revocation record SHALL be
canonical sorted-key compact UTF-8 JSON containing exactly schema `1`, kind
`approval-revocation`, approval SHA-256, decision owner/control-plane instance/
provenance, and UTC RFC 3339 decision time. It SHALL be created no-replace and
the file and parents SHALL be fsynced. An existing path SHALL be reuse-only
after exact regular-file canonical-content verification; unsafe ownership,
mode, links, closure, or collision SHALL block. It SHALL NOT delete or rewrite
approval evidence, and public paths SHALL NOT mint it.

The authority lock SHALL NOT acquire or wait for the transaction-long operation
lock, so the Router can record a revocation while an operation holds that lock.
A forward transaction SHALL acquire locks only in operation-then-authority
order and SHALL hold the authority lock from its expiry/revocation recheck
through durable boundary intent, atomic target mutation, all required fsyncs,
and the durable boundary result. The journal SHALL record UTC and monotonic
authority-check time; expiry at or before that instant SHALL block, while a
later expiry SHALL be ordered after this one bounded boundary and block the
next. A revocation linearized before the boundary SHALL block it. A revocation
linearized after a started boundary SHALL block the next forward boundary and,
after intent, permit only compensation-lease restoration. Terminal success
receipt/lease consumption SHALL be a boundary; a revocation ordered after
terminal success SHALL be non-retroactive and SHALL require a new rollback
decision.

#### Scenario: Revocation races with mutation intent

- **GIVEN** a transaction holds the controller operation lock and a current
  approval has a prepared but inactive compensation lease
- **WHEN** Router revocation and the first `MUTATION_INTENT` boundary race
- **THEN** the short authority lock gives them one durable order
- **AND** revocation-first causes no target mutation or active lease
- **AND** boundary-first completes only that boundary, then no later forward
  boundary runs and lease-bound restoration is the only mutation authority

#### Scenario: Current state changes after planning

- **GIVEN** a plan was created for a fixed current fingerprint
- **WHEN** the source, runtime, discovered-entry/projection set, symlink target,
  registry revision, candidate, or validation contract changes before apply
- **THEN** apply rejects the plan as stale
- **AND** a new plan and approval are required

#### Scenario: User approves a different or partial identifier

- **WHEN** the recorded user decision does not match the current canonical
  `plan-id`
- **THEN** apply is `BLOCKED`
- **AND** no target or installation channel is mutated

#### Scenario: Approval action or scope does not match

- **WHEN** an approval artifact names a different action, target, scope,
  allowed-path set, plan/receipt, control-plane owner, or expiry
- **THEN** the internal transaction returns `BLOCKED`
- **AND** the public CLI cannot mint a replacement approval

#### Scenario: Superpowers has a Major divergence

- **GIVEN** the effective Superpowers checkout contains a local patch and the
  observed candidate crosses a Major workflow boundary
- **WHEN** a direct apply is requested
- **THEN** the controller returns `BLOCKED_MAJOR`
- **AND** preserves the effective checkout until a separate approved migration
  proves compatibility, validation, discovery, and rollback

#### Scenario: Major authorization names another artifact revision

- **WHEN** a Major plan or approval omits the change-id, manifest hash, recorded
  approved raw-artifact hash set, or approved projection hash; binds another
  revision; or the current contract projection differs from the approved
  projection
- **THEN** apply remains `BLOCKED_MAJOR`
- **AND** platform permission or a direction-only decision cannot substitute for
  the exact OpenSpec authorization

#### Scenario: Approved raw-artifact evidence is unavailable

- **WHEN** a manifest snapshot is missing, linked, non-regular, colliding, or
  does not hash to the recorded artifact value
- **THEN** Major plan/apply eligibility remains `BLOCKED_MAJOR`
- **AND** checklist normalization or a matching projection digest cannot
  substitute for the exact approved raw bytes

#### Scenario: Source-worktree prestate is wrong or already occupied

- **WHEN** repository/Git/sandbox executable or profile identity, parent
  closure, base commit/tree, non-excluded refs, exact exclusion policy,
  worktrees, local config, approved
  material hashes, or any expected-absent branch/ref-log/worktree/admin
  component differs from the exact approval
- **THEN** task 2.1 returns `BLOCKED_SOURCE_WORKTREE_RECOVERY` before mutation
- **AND** it does not reuse, force, reset, repair, delete, or clean the target

#### Scenario: Volatile control-plane checkpoint changes across approval turns

- **GIVEN** the exact schema-2 prestate excludes only
  `refs/codex/turn-diffs/` under its bound deny-bootstrap-write policy
- **WHEN** the control plane changes that namespace before task 2.1
- **THEN** the change is diagnostic external drift and does not invalidate the
  exact non-excluded ref inventory
- **AND** any other exclusion, any non-excluded ref drift, or any sandbox write
  authority into the excluded namespace blocks before Git execution

#### Scenario: A prior source-worktree attempt lacks current approval evidence

- **GIVEN** a prior ref/worktree/admin path whose artifact bytes require a
  manifest or raw snapshots that are absent there
- **WHEN** a corrected Major contract names a distinct absent replacement
  ref/worktree/admin target
- **THEN** the schema-2 prestate binds the prior attempt's exact ref, HEAD/tree,
  paths, observed manifest/artifact hashes, missing evidence, and preserve-only
  policy
- **AND** the replacement may proceed only while every bound quarantine
  identity and evidence byte remains unchanged
- **AND** neither direction approval nor exact replacement approval authorizes
  repair, reuse, deletion, cleanup, or adoption of the quarantined attempt

#### Scenario: Source-worktree parent or reservation changes at the boundary

- **WHEN** any repository/common-dir/ref/log/admin/worktree-parent/approval/
  source-bootstrap component is exchanged, a symlink is inserted, an empty target is raced in, or the
  reserved target no longer names its retained inode
- **THEN** descriptor revalidation or the write-deny sandbox blocks Git before
  an unapproved identity can be mutated
- **AND** inability to prove anchored no-replace containment is fail-closed

#### Scenario: Ambient Git behavior or interruption escapes the bootstrap

- **WHEN** a hook/filter/process driver/helper/include/alias/protocol rewrite,
  prompt, network attempt, non-regular base entry, extra ref/config/worktree
  mutation, or partial interrupted residue is observed
- **THEN** task 2.1 blocks and records the exact mismatch
- **AND** no current approval authorizes residue adoption or destructive repair

#### Scenario: Source helper is not exactly contained or indexed

- **WHEN** the helper/profile/sandbox exec-vector/argv/environment/FD protocol
  drifts, direct `--contained` execution lacks active sandbox denial, a raw blob
  fails independent OID verification, or the generated index is absent,
  malformed, changed by status, or reports a tracked delta
- **THEN** task 2.1 returns `BLOCKED_SOURCE_WORKTREE_RECOVERY`
- **AND** no ref/worktree residue is reused, repaired, or cleaned under that
  approval

#### Scenario: Checklist progress crosses the source-bootstrap boundary

- **WHEN** any approved material path changes before task 2.1
  post-verification
- **THEN** exact materialization is blocked even when the change is only a
  checklist marker
- **AND** after exact materialization, checklist-only progress preserving the
  contract projection is allowed without manifest rewrite

#### Scenario: Candidate expands the capability surface

- **WHEN** candidate diff adds or changes scripts, executable modes, hooks, MCP
  servers, apps, tools, implicit-invocation policy, trigger scope, or dependency
  closure
- **THEN** apply eligibility is `BLOCKED_MAJOR`
- **AND** a semantic version label or release note cannot bypass exact diff,
  contract, validation, and approval Review

### Requirement: Content-addressed exact runtime payload

The repository-only `references/runtime-manifest.json` SHALL be a reviewed
build allowlist/schema declaring exact relative paths and expected normalized
modes and SHALL NOT be copied into or self-hashed by the runtime payload. The
builder SHALL resolve it into canonical
`runtime-lock.json` bytes containing schema version `1` and a sorted inventory
of every allowed regular file's POSIX relative path, normalized `0644` or
`0755` mode, and SHA-256 content digest. It SHALL reject absolute paths, empty
segments, `.`, `..`, backslashes, NUL, traversal encodings, symlinks,
hard-linked files, non-regular files, unreviewed top-level paths, and sensitive
or repository-only categories.

The payload identifier SHALL be SHA-256 over a fixed schema/domain prefix plus
the UTF-8, sorted-key, compact-separator canonical lock bytes. A release SHALL
contain exactly `<payload-sha256>/payload/` and sibling
`runtime-lock.json`; the discovery symlink SHALL target the exact `payload/`
directory. The stored lock SHALL itself be canonical and recompute to the
release-directory digest. Every listed file type, mode, and digest SHALL match,
every payload directory SHALL be mode `0755`, and no missing, extra, or linked
entry SHALL be accepted.

The digest directory SHALL be a current-user-owned mode-`0755` directory whose
top level contains exactly `payload/` and `runtime-lock.json`. Every existing
release-path component SHALL pass no-follow checks. The lock SHALL be a
current-user-owned, mode-`0644`, single-link regular file verified with `lstat`;
its canonical bytes SHALL be read only after those checks. A lock symlink,
hardlink, wrong owner/mode, non-canonical encoding, or extra top-level entry
SHALL be a blocker/collision even when dereferencing currently yields expected
bytes.

Release finalization SHALL verify and seal a restrictive same-filesystem sibling
temporary directory before a platform-proven atomic no-replace rename into the
content-addressed destination; an adapter without that primitive SHALL be
`BLOCKED`. If that digest destination already exists, it SHALL be verify-only:
exact closure MAY be reused, while any mismatch SHALL return
`BLOCKED_RELEASE_COLLISION` without overwriting bytes. A sibling temporary
symlink SHALL use atomic no-replace for an approved absent pre-state or atomic
exchange preserving/verifying the displaced entry for an approved present
pre-state; unconditional `os.replace` SHALL NOT perform the discovery switch.
Exact-lock verification SHALL run before plan acceptance, promotion, fresh
discovery, rollback, and cleanup.

#### Scenario: Runtime allowlist contains an unsafe entry

- **WHEN** an allowlist or candidate entry is absolute, traversing,
  backslash-containing, linked, non-regular, sensitive, or outside reviewed
  runtime top-level paths
- **THEN** runtime-lock construction is `BLOCKED`
- **AND** no release or discovery entry is created or changed

#### Scenario: Payload closure differs from its lock

- **WHEN** a payload has a missing or extra entry, wrong type or mode, content
  hash mismatch, symlink, or non-`0755` directory
- **THEN** verification is `BLOCKED`
- **AND** the payload cannot be promoted, discovered, or used for rollback

#### Scenario: Runtime lock or digest-directory closure is unsafe

- **WHEN** the lock is linked, has the wrong owner/mode, is non-canonical, has a
  symlink ancestor, or the digest directory has any extra/missing top-level
  entry
- **THEN** verification returns `BLOCKED_RELEASE_COLLISION` or an equivalent
  pre-finalization blocker
- **AND** no lock bytes are trusted and no existing release is repaired

#### Scenario: Same-digest release already exists

- **WHEN** the content-addressed release destination already exists
- **THEN** an exact lock/closure match is reused without mutation
- **AND** any mismatch returns `BLOCKED_RELEASE_COLLISION`
- **AND** the existing destination is never overwritten or repaired in place

### Requirement: Transactional apply, verification, and rollback

The controller SHALL require every public or internal entrypoint except the
fixed Bootstrap-root initializer defined above to first acquire and retain one
controller operation lock through journal detection, bound-state reads,
external probes, report/plan/receipt writes, verification, and any transaction.
The normal lock
SHALL be a current-user-owned mode-`0600`, single-link regular file opened
no-follow under validated controller state; bootstrap SHALL use the lock
embedded in the stable Bootstrap Control Root and select a manifest workspace
only after acquiring it. Its held descriptor identity SHALL be revalidated and
its path SHALL never be replaced. Unsafe/unavailable locking SHALL block. A
scheduled/on-demand audit SHALL NOT overlap apply, registry, schedule, rollback,
or cleanup and consume mixed state. The short authority lock SHALL follow the
fixed nesting and boundary-linearization rules above.

An approved apply or `bootstrap-apply` SHALL stage candidates and temporary
compensation material outside every Skill discovery root, resolve and contain
every real path, reject symlink escapes, run declared validation without a
shell, and promote only through an adapter that proves conditional atomic
replacement and deterministic rollback.
Directory-based apply SHALL use immutable version directories and a
same-filesystem conditional discovery-symlink replacement. An existing
non-empty plain copied runtime SHALL be `BLOCKED_LAYOUT_MIGRATION` rather than
exposed to a non-atomic directory swap.

Before the first target mutation of apply, `bootstrap-apply`, post-success
rollback, `registry-replace`, schedule install/remove/replace, or
retained-material cleanup, the controller SHALL write and fsync a canonical
transaction journal. Normal journals SHALL live in the validated controller
state root; first-bootstrap authority/evidence SHALL live only in the selected
Bootstrap manifest workspace until the state root is conditionally installed.

While the original approval is current and before the first
`MUTATION_INTENT`, the Router SHALL prepare and fsync a canonical single-use
compensation lease binding transaction/plan/approval hashes, exact pre-state,
restoration-only paths, compensation hashes, and terminal conditions. The lease
SHALL activate only when the fsynced `MUTATION_INTENT` transition rechecks the
still-current, unrevoked approval and binds the lease hash while holding the
authority lock through the atomic mutation and durable boundary result. Every
forward mutation and terminal-success boundary SHALL repeat that linearized
check. Expiry or revocation before intent SHALL block without target mutation
or active lease; after intent it SHALL stop the next forward boundary and
permit only exact lease-bound restoration/verification.
The lease SHALL NOT authorize a new candidate, forward resume, post-success
rollback, registry/schedule change, or retained cleanup, and SHALL be consumed
by a durable success receipt or verified restoration.
Missing/corrupt/ambiguous lease evidence SHALL be `RECOVERY_REQUIRED`.

The journal SHALL bind the compensation-lease hash, pre-state fingerprint,
allowed paths, compensation material, and phase. It SHALL atomically persist and
fsync every phase transition. Compensation bytes/hashes and their directories
SHALL be durable before the journal authorizes mutation; every filesystem
rename/switch SHALL fsync affected parent directories before phase advancement.

Every final-child mutation SHALL use a platform-proven conditional protocol
anchored to the verified parent. Creation of an expected-absent child SHALL use
atomic no-replace. Replacement of an expected-present child SHALL use atomic
exchange with a sibling candidate, preserving the displaced object. Removal
SHALL exchange the expected child with a unique journal-bound tombstone, verify
the displaced object, then atomically no-replace-relocate and verify that exact
tombstone in an absent private quarantine slot so the destination becomes
absent. The displaced object's type, device/inode, mode, link metadata/target,
and content hash SHALL match approved pre-state at every step. A mismatch SHALL
be exchanged or moved back when unambiguous; no identity-mismatched object SHALL
be unlinked, and concurrent ambiguity SHALL be `RECOVERY_REQUIRED`. The
approved removed object SHALL remain compensation until a durable receipt or
restoration permits transaction-bound cleanup. Terminal unlink SHALL occur only
inside a transaction-exclusive current-user-owned private closure whose
directory descriptor, owner/mode, path identity, entry set, and entry
identities remain bound through deletion. If an adapter cannot prove that
envelope or observes drift, it SHALL retain the quarantine and return a cleanup
blocker. Unconditional `os.replace`, check-then-overwrite, check-then-unlink, or
an adapter without every required primitive SHALL be blocked.

Every controller entrypoint SHALL detect an incomplete journal before new
audit, plan, verify, apply, rollback, registry, schedule, or cleanup work.
Public and scheduled paths SHALL return `RECOVERY_REQUIRED` and re-enter the
Router without target mutation. Router-owned recovery SHALL acquire the same
lock and use only the compensation lease when the original approval is no
longer current. Before each target-changing substep it SHALL durably record
pre-state plus `MUTATION_INTENT`. Only a `PREPARED` phase whose target is proven
still equal to pre-state MAY clean journal-bound staging without restoration.
`MUTATION_INTENT` and every later incomplete phase SHALL treat the target as
possibly changed and restore and verify prior state unless a durable success
receipt proves completion; phase alone SHALL NOT prove non-mutation or success.

After promotion the controller SHALL verify target tests/validators, planned
hash/ref parity, effective runtime version, fresh Skill discovery, and managed
dependency-group status before writing a sanitized receipt. Any failure SHALL
automatically compensate under the activated restoration-only lease by
restoring prior bytes, modes, registration, and symlink target, verifying the
restored state, and returning `FAILED_COMPENSATED`. A missing, corrupt, or ambiguous
journal/compensation record SHALL return
`RECOVERY_REQUIRED`/`BLOCKED_RECOVERY_REQUIRED`, record owner and resume
condition, and permit no further mutation.

#### Scenario: Candidate validation fails

- **WHEN** any target validator, test, parity check, version observation, or
  discovery probe fails
- **THEN** the prior target is restored and verified
- **AND** no success receipt or updated claim is produced

#### Scenario: Installation channel lacks a safe adapter

- **WHEN** an installation mode cannot prove isolated validation, atomic
  promotion, fresh verification, and rollback
- **THEN** apply returns `BLOCKED` with an owner and resume condition
- **AND** remove/reinstall or in-place overwrite is not used as an implicit
  fallback

#### Scenario: Version 1 plugin replacement is requested

- **WHEN** a `codex-plugin` package is selected for apply
- **THEN** version 1 returns `BLOCKED_CHANNEL_MUTATION`
- **AND** an update plan or OpenSpec approval does not grant plugin installation
  or remove/reinstall authority

#### Scenario: Plain copied runtime is targeted

- **WHEN** a source-runtime or installer-snapshot target is an existing
  non-empty directory rather than an approved immutable-release/symlink layout
- **THEN** apply returns `BLOCKED_LAYOUT_MIGRATION`
- **AND** no two-rename directory replacement or visibility gap occurs

#### Scenario: Atomic switch is interrupted

- **WHEN** a real subprocess is hard-killed before release finalization, before
  symlink replacement, immediately after replacement, or during post-promotion
  verification and the controller restarts
- **THEN** the current discovery entry is always either the complete prior or
  complete candidate release
- **AND** the fsynced journal drives contained cleanup or verified restoration
  before any new work

#### Scenario: Final child drifts after the last precheck

- **GIVEN** a final discovery, plist, registry, state-root, or cleanup child was
  approved as absent or with an exact pre-state identity
- **WHEN** another object appears or replaces it after the last ordinary check
  but before the mutation primitive
- **THEN** atomic no-replace blocks, or replacement/removal exchange preserves
  and detects the mismatched displaced object
- **AND** exchange/move-back or recovery leaves every mismatched object intact
  and the transaction returns `BLOCKED`/`RECOVERY_REQUIRED` without
  unconditional overwrite or unlink

#### Scenario: Approval expires after mutation intent

- **GIVEN** the current approval activated a valid compensation lease before
  `MUTATION_INTENT`
- **WHEN** the approval expires or is revoked before a durable success receipt
- **THEN** no forward mutation resumes
- **AND** restart may use the lease only to restore and verify exact pre-state
- **AND** an expiry before `MUTATION_INTENT` grants no target mutation or lease
  activation

#### Scenario: Recovery evidence is corrupt or ambiguous

- **WHEN** restart finds an incomplete journal whose pre-state or compensation
  evidence cannot be verified
- **THEN** the controller returns `RECOVERY_REQUIRED`
- **AND** it records an owner/resume condition and performs no guessed mutation

#### Scenario: Controller or its alias is targeted

- **WHEN** the transaction executor resolves from or aliases the target running
  executable, payload, discovery entry, or release
- **THEN** its live process may audit and plan but cannot replace itself
- **AND** version 1 returns `BLOCKED_SELF_UPDATE`
- **AND** records the Router-owned resume condition for a separately approved
  fixed-source deployment and new-process discovery verification

#### Scenario: External Router bootstraps the same package ID

- **GIVEN** the action is the exactly approved initial `bootstrap-apply`
- **AND** the fixed Router executor's resolved code/source/payload identities
  are disjoint from every updater target
- **WHEN** the canonical bootstrap plan is executed from the Bootstrap Control
  Root
- **THEN** package ID `codex-skill-update` alone does not trigger
  `BLOCKED_SELF_UPDATE`
- **AND** any executor-to-target alias still blocks before destination backup or
  mutation

#### Scenario: Bootstrap action targets an active installation

- **WHEN** fresh process/discovery/registry evidence finds a running, active
  discovered, or ambiguous updater installation
- **THEN** `bootstrap-apply` is `BLOCKED`
- **AND** it cannot substitute for a separately governed fixed-source update

#### Scenario: Failed apply compensates automatically

- **GIVEN** the user approved the exact apply transaction
- **WHEN** validation or verification fails before success
- **THEN** the pre-intent compensation lease restores and verifies the exact
  prior state without granting forward authority
- **AND** transaction result is `FAILED_COMPENSATED`
- **AND** no second rollback approval is requested

#### Scenario: User requests rollback after success

- **GIVEN** an apply receipt records a current and immediately previous verified
  immutable release
- **WHEN** the user requests a post-success rollback
- **THEN** the Router records a new receipt-bound rollback approval
- **AND** rollback first recomputes and matches the receipt's adapter-specific
  canonical after-fingerprint, including common discovery
  `lstat`/`readlink`, resolved target, registry revision/hash, and
  allowed-path-set hash fields
- **AND** source-runtime/snapshot fingerprints include exact payload
  lock/content/modes, while git-symlink fingerprints include repository
  identity and Git-dir/worktree paths, object format, HEAD/tree, symbolic ref or
  detached state, index checksum, remote/ref mapping, submodule state, canonical
  status, and path/type/mode/content digests for all tracked and untracked
  worktree entries outside Git internals
- **AND** later user edits or missing/corrupt rollback material return `BLOCKED`
  instead of being overwritten or reconstructed

#### Scenario: Rollback material is cleaned

- **WHEN** cleanup of immutable releases or receipt-bound material is requested
- **THEN** the Router records a separate cleanup plan and approval bound to the
  exact receipt, paths, hashes, and expiry
- **AND** cleanup cannot remove the current or only immediately previous
  known-good release
- **AND** cleanup cannot remove a payload referenced by an installed
  schedule-execution binding until a separately approved schedule
  remove/replace is verified
- **AND** the receipt records any material that is no longer available

#### Scenario: Transaction-local temporary material is finalized

- **WHEN** staging or compensation remains inside an in-progress action
- **THEN** the same action may remove it only while its approval remains current
  and after a durable success receipt or verified-restoration record
- **AND** expiry/revocation-driven lease recovery retains remaining material
  until a new exact cleanup approval
- **AND** journal finalization does not authorize deletion of retained
  post-success or receipt-bound material

#### Scenario: Diagnostic or receipt is persisted

- **WHEN** the controller writes a report, plan, receipt, or rollback result
- **THEN** it contains only minimum non-sensitive paths, hashes, refs, commands,
  timestamps, statuses, and evidence results
- **AND** it excludes credentials, tokens, environment values, private prompts,
  raw traces, and file contents

### Requirement: Canonical final evidence and Review chain

Closeout SHALL use only `closeout/` in the selected immutable Major workspace,
outside every governed source/runtime/schedule/registry/rollback/cleanup
fingerprint. Directories SHALL be current-user-owned mode `0700`; records SHALL
be current-user-owned mode `0600`, single-link regular files. Every component
SHALL be opened no-follow and descriptor-verified. Canonical sorted-key compact
UTF-8 JSON SHALL be created no-replace at
`prerequisites/<record-sha256>.json`,
`eligibility/<record-sha256>.json`,
`preliminary/<record-sha256>.json`, `passes/<record-sha256>.json`, or
`reviews/<record-sha256>.json`; post-Review archive receipts SHALL use
`archives/<record-sha256>.json`. The filename SHALL be SHA-256 of exact bytes.
Files and affected parents SHALL be fsynced; existing exact records SHALL be
verify-only. Unsafe closure, collision, rewrite, or mutable alias SHALL block
completion.

Task 6.7 SHALL persist one prerequisite containing exactly `schema` (integer
`1`), `kind` (`runtime-high-review`), `change_id`,
`major_manifest_sha256`, `reviewer`, `executor`, `started_at`, `completed_at`,
`changed_file_inventory_sha256`, `governed_fingerprints`,
`claim_mechanism_coverage_sha256`, `adversarial_probe_sha256`, and `result`
(`PASS`). Task 7.1 SHALL persist a later prerequisite containing exactly
`schema` (integer `1`), `kind` (`project-learning-closeout-review`),
`change_id`, `major_manifest_sha256`, `parent_runtime_review_sha256`,
`reviewer`, `executor`, `started_at`, `completed_at`,
`candidate_inventory_sha256`, `promoted_artifact_inventory_sha256`,
`enforcement_results_sha256`, `changed_file_inventory_sha256`,
`findings_sha256`, and `result` (`PASS`). Each reviewer SHALL differ from its
executor. The runtime record's `governed_fingerprints` SHALL contain exactly
`current_source`, `sibling_source`, `runtime`, `operational_state`, `registry`,
`schedule`, and `rollback_cleanup`. Both SHALL be canonical content-addressed files under
`prerequisites/`; the learning parent SHALL be the exact runtime record, and
learning start SHALL NOT precede runtime Review completion.

After validating both prerequisite paths, exact bytes, filename hashes, kinds,
PASS results, change/manifest identity, distinct identities, parent, and time
order, task 7.1 SHALL create one record under `eligibility/` containing exactly
`schema` (integer `1`), `kind` (`final-verification-eligibility`), `change_id`,
`major_manifest_sha256`, `parent_runtime_review_sha256`,
`parent_learning_closeout_sha256`, `post_learning_source_fingerprints`,
`created_at`, and `result` (`READY`). `post_learning_source_fingerprints` SHALL
contain exactly `current_source` and `sibling_source`; creation SHALL NOT
precede learning Review completion.

The preliminary record SHALL contain exactly the keys `schema` (integer `1`),
`kind` (`final-verification-preliminary`), `change_id`,
`major_manifest_sha256`, `parent_evidence_sha256`, `executor`, `started_at`,
`completed_at`, `result` (`AWAITING_TRACE_REMOVAL`),
`governed_fingerprints`, `openspec_contract_projection_sha256`,
`openspec_archive_projection_sha256`, `command_results`, and `raw_traces`.
`governed_fingerprints` SHALL contain
exactly `current_source`, `sibling_source`, `runtime`, `operational_state`,
`registry`, `schedule`, and `rollback_cleanup`, each the SHA-256 of its
canonical exact inventory. The plan-bound source inventories SHALL exclude Git
metadata, map the active or archived OpenSpec change to one logical change-root
path, include every supporting file exactly, and exclude only the four contract
artifacts whose complete behavior-bearing projected bytes SHALL instead be
bound by `openspec_contract_projection_sha256`; operational state SHALL exclude
this evidence plane. Each sorted `command_results` entry SHALL contain exactly `argv`,
`cwd_token_sha256`, `started_at`, `completed_at`, `freshness_at`, `exit_code`,
and `sanitized_result_sha256`. Each sorted `raw_traces` entry SHALL contain
exactly `logical_id`, `path_token_sha256`, `parent_dev`, `parent_ino`, `size`,
and `sha256`, never trace bytes or sensitive content.
`parent_evidence_sha256` SHALL equal the eligibility record's exact
filename/content SHA-256. Preliminary creation SHALL revalidate the full
prerequisite chain and require its current/sibling source fingerprints to equal
`post_learning_source_fingerprints`. Missing, wrong-kind, non-PASS,
cross-manifest, parent-mismatched, time-inverted, or source-stale evidence SHALL
block preliminary creation.

Only after that record is durable and all consumers finish SHALL every listed
raw trace be removed. The Router SHALL revalidate the exact parents, prove each
logical path absent, and recompute all governed fingerprints. It SHALL then
create one PASS record containing exactly `schema` (integer `1`), `kind`
(`final-verification-pass`), `change_id`, `major_manifest_sha256`,
`parent_preliminary_sha256`, `governed_fingerprints`,
`openspec_contract_projection_sha256`, `openspec_archive_projection_sha256`,
`trace_absence`, `sealed_at`, and `result` (`PASS`). Each sorted
`trace_absence` entry SHALL contain exactly
`logical_id`, `path_token_sha256`, `predelete_sha256`, `parent_dev`,
`parent_ino`, and `verified_absent_at`. A missing trace-absence proof, changed
fingerprint/projection, or `BLOCKED` cleanup SHALL prevent the PASS seal.

Final High Review SHALL be a later record, not a field in the PASS. It SHALL
contain exactly `schema` (integer `1`), `kind` (`final-high-review`),
`change_id`, `major_manifest_sha256`, `parent_pass_sha256`, `reviewer`,
`executor`, `started_at`, `completed_at`, `inspected_artifact_hashes`,
`changed_file_inventory_sha256`, `critical_reruns`,
`claim_mechanism_coverage_sha256`, `adversarial_probe`,
`openspec_archive_projection_sha256`, `findings`, and `result` (`PASS`).
Reviewer and executor identities SHALL differ.

Before preliminary creation, the Router SHALL compute
`openspec_archive_projection_sha256` without changing governed source. It SHALL
hash the exact UTF-8 prefix `openspec-archive-projection-v1` plus one NUL and a
sorted-key compact canonical inventory binding the exact archive destination,
logical change-root relocation/absence, checklist-normalized four-artifact
projection, and every affected main-spec/supporting path with predicted
post-archive type/mode/content hash. Final Review SHALL inspect this projection.
After Review, archive MAY perform only this exact transition. The Router SHALL
verify actual normalized inventory and strict post-archive validation, then
create an archive receipt containing exactly `schema` (integer `1`), `kind`
(`openspec-archive-receipt`), `change_id`, `major_manifest_sha256`,
`parent_review_sha256`, `expected_archive_projection_sha256`,
`actual_archive_inventory_sha256`, `strict_validation`, `archived_at`, and
`result` (`PASS`). `strict_validation` SHALL contain exactly `argv`,
`exit_code`, `sanitized_result_sha256`, and `completed_at`. Mismatch or strict
failure SHALL invalidate PASS/Review and create no receipt.

Runtime completion SHALL verify the full preliminary/PASS/Review/archive parent
chain and fresh governed fingerprints. After PASS, only new immutable records
in this closeout plane, normalized checklist progress, and the exact
Review-approved archive projection SHALL be non-invalidating; any other
governed change SHALL invalidate PASS and Review.

Policy-required current/previous/schedule-referenced releases SHALL be
`RETAINED_BY_POLICY`, not failed cleanup. Any required cleanup or raw-trace
deletion that returns `BLOCKED` SHALL stop before preliminary final evidence;
recording an owner/resume condition SHALL NOT permit gate advancement.

#### Scenario: Required cleanup is blocked

- **WHEN** required transaction, retained-material, or raw-trace cleanup cannot
  prove authorized safe completion
- **THEN** closeout records `BLOCKED`, owner, resume condition, and rollback
  availability/hash and stops before final verification
- **AND** no preliminary, PASS, final Review, archive, or completion evidence
  may treat the blocker as an accepted exception

#### Scenario: Final verification traces are removed

- **GIVEN** all required cleanup is complete and one canonical preliminary
  record durably binds governed fingerprints and every trace pre-delete hash
- **WHEN** the exact traces are removed and their parent identities/absence plus
  unchanged governed fingerprints are verified
- **THEN** one no-overwrite child PASS record seals that proof
- **AND** a distinct independent Review record may be created only later with
  the PASS hash as parent

#### Scenario: Final verification eligibility is missing, wrong, or stale

- **GIVEN** task 6.7 runtime Review and task 7.1 Project Learning Closeout are
  required predecessors
- **WHEN** either prerequisite or the eligibility record is missing, has a
  wrong path/hash/kind/result/change/manifest/identity/time order, has a broken
  parent relation, or its post-learning source fingerprint is stale
- **THEN** no preliminary final-verification record is created
- **AND** an arbitrary hash in `parent_evidence_sha256` cannot advance closeout

#### Scenario: Governed state changes after PASS

- **WHEN** source/runtime/schedule/registry/rollback/cleanup state changes after
  PASS other than permitted closeout records, normalized checklist progress, or
  the exact Review-approved archive projection
- **THEN** the PASS and any child Review are stale
- **AND** fresh preliminary, trace cleanup, PASS, and Review records are required

#### Scenario: OpenSpec change is archived after final Review

- **GIVEN** final High Review PASS binds the predicted archive projection
- **WHEN** the Router archives the change and updates main specs
- **THEN** the actual normalized change relocation and every affected path/hash
  equal the prediction and strict post-archive validation passes
- **AND** one no-overwrite archive receipt names the Review as parent
- **AND** any projection mismatch or strict failure invalidates the final gates
  and produces no PASS archive receipt

### Requirement: Scheme C and publication boundaries remain intact

Installing or running the controller SHALL NOT install candidate dependencies,
update Superpowers, alter the Scheme C architecture, modify Router portable
files, or synchronize optional updater content to Antigravity CLI or Grok CLI.
The first managed package group SHALL include Router, Companion, the single
Superpowers repository/collection mapped to its multiple discovered entries,
and the updater; `mattpocock/skills` SHALL remain outside the active installed
dependency closure unless a future separately approved change selects it.

Audit, planning, update approval, implementation success, and receipt creation
SHALL NOT grant Git initialization or mutation of sibling/source/live user
repositories, staging, commit, branch/tag/remote mutation, reset, clean, push,
PR, release, plugin installation, or publication authority. The narrowly
authorized ephemeral/immutable Git candidate materialization defined above
SHALL NOT broaden this boundary. The sole exception is the separately explicit
exact source-implementation approval for task 2.1, which MAY create only the
disclosed local `add-codex-skill-update-v2` branch ref and replacement isolated
worktree, SHALL NOT mutate the quarantined prior `add-codex-skill-update`
ref/worktree/admin path, and SHALL NOT grant staging, commit, remote, push, PR,
release, plugin installation, or publication authority.

Initial controller installation SHALL be a `bootstrap-apply` executed by the
Router from fixed reviewed source outside every destination after source High
Review PASS. Fresh process/discovery/registry evidence SHALL prove there is no
running or active discovered updater installation; inactive partial exact
pre-state MAY be recovery input, but bootstrap SHALL NOT update an active or
ambiguous installation. The plan SHALL be
written in the exact Major-manifest workspace under the stable Bootstrap
Control Root and bind
the external Router executable/code/source identity and hashes, absent/existing
pre-state, exact updater source/candidate/runtime-lock hashes, canonical initial
registry bytes/schema/revision/hash, complete package/entry/projection and
adapter closure, exact initial state layout, allowed paths, backup, validation,
rollback, Major authorization, and expiry, plus a separate exact action-bound
approval. Approval of the Major implementation contract alone
SHALL authorize only source work, the disclosed Bootstrap Control Root, and its
missing fixed manager anchors plus the immutable manifest workspace/authority/
closeout evidence plane, not this updater runtime/state mutation.

#### Scenario: Initial controller deployment is requested

- **GIVEN** source validation and High Review have passed
- **WHEN** the updater runtime is to be installed for the first time
- **THEN** the external Router requires the fresh bootstrap plan and matching
  `bootstrap-apply` approval before backup or destination mutation
- **AND** the destination updater cannot authorize or execute its own bootstrap
- **AND** the selected Bootstrap manifest workspace retains the fsynced
  authority/plan/approval/lease/journal until the conditionally installed exact
  state layout, imported
  evidence, and sanitized receipt are verified

#### Scenario: Bootstrap is killed before state-root completion

- **GIVEN** updater runtime/state destinations were absent or matched the exact
  bootstrap pre-state before approval
- **WHEN** the external Router is hard-killed after `MUTATION_INTENT` and
  restarts
- **THEN** the selected Bootstrap manifest workspace's journal and compensation
  lease restore and verify exact pre-state before any new work
- **AND** no destination plan/journal is required to recover an absent state
  root

#### Scenario: Controller installation completes

- **WHEN** the updater source/runtime, registry, schedule, tests, and discovery
  checks pass
- **THEN** the runtime payload exactly matches its canonical runtime lock and is
  installed as an atomic discovery symlink to the immutable release's exact
  `payload/` directory
- **AND** repository-only instructions, READMEs, tests, fixtures, OpenSpec, Git
  metadata, and design evidence are absent from that payload
- **AND** no managed dependency is updated merely because the controller was
  installed
- **AND** the existing Scheme C execution path remains unchanged

#### Scenario: Closeout reaches final Review

- **GIVEN** runtime/schedule/registry High Review has passed and Project
  Learning Closeout has been applied, independently reviewed, and linked by the
  canonical eligibility record
- **WHEN** transaction-local cleanup, any separately approved retained cleanup,
  and raw-trace removal are complete with no required cleanup `BLOCKED`
- **THEN** one fresh final verification creates the canonical preliminary
  record in the selected Major workspace with the eligibility hash as parent
  before removing its listed traces
- **AND** verified trace absence plus unchanged governed fingerprints create the
  child PASS seal
- **AND** a distinct final High Review record starts only later with that PASS
  hash as parent
- **AND** only the immutable closeout evidence plane, normalized checklist
  progress, and the exact Review-approved archive plus strict child receipt may
  change after PASS without invalidation
- **AND** any later governed-state cleanup/correction or archive drift
  invalidates both gates and requires fresh verification and Review before
  completion

#### Scenario: Source implementation passes

- **WHEN** all source/runtime update-controller acceptance checks pass
- **THEN** Git and publication status are reported separately
- **AND** no sibling/source/live `git init`, staging, commit,
  branch/tag/remote mutation, reset, clean, push, PR, release, plugin
  installation, or publication occurs without its own explicit user
  authorization
