# Governed Codex Skill Update Self-Evolution Review Draft

Document type: Major Self-Evolution review draft

Proposed change-id: `add-codex-skill-update`

Status: proposal-only; the exact OpenSpec change is not yet approved

## Observed failures

The Scheme C evaluation established a controlled third-party update procedure,
but no executable freshness controller currently exists:

1. `README.md` and `README_cn.md` explicitly state that the repository does not
   claim an automatic dependency checker exists.
2. The current Superpowers installation is a Git checkout exposed through a
   Skill symlink. The effective checkout is
   `v5.0.7-8-gcc7b33e`, is ahead of its cached upstream by one local commit and
   behind by seventeen commits, and therefore cannot be safely updated with a
   blind pull.
3. A Skill symlink follows local checkout changes but never fetches upstream
   changes. `codex update` updates the Codex CLI, not independent Skill
   checkouts or installer snapshots.
4. The installed Codex plugin command surface provides marketplace refresh and
   plugin add/remove operations, but no generic `codex skill update` or
   `codex plugin update` command.
5. The current runtime inventory contains no `codex-skill-update` Skill, no
   version registry for the workflow dependency group, and no scheduled
   freshness report.
6. The first isolated source-worktree attempt contains current proposal/design/
   spec/tasks bytes but only an older Major manifest and older proposal/tasks
   snapshots. Its apparent task 2.1 completion is a false-PASS evidence chain;
   the ref/worktree/admin path is quarantined as
   `BLOCKED_SOURCE_WORKTREE_RECOVERY` and cannot be repaired or reused.

The resulting failure mode is delayed discovery: a dependency can remain stale
or diverged until a human remembers to inspect every installation channel.

## Desired behavior

Create an independently maintained Codex Skill named `codex-skill-update` with
two strictly separated paths:

- `audit`, `plan`, and `verify` inspect registered dependencies or receipts,
  may write sanitized
  reports under the controller state root, and never mutate a managed Skill,
  Git checkout, plugin marketplace, or installation snapshot. Observation and
  notification use only closed reviewed adapters; registry text never becomes
  an executable command;
- `apply`, post-success `rollback`, schedule install/remove/replace, and cleanup are
  Router-only internal transactions that require a current action-bound approval
  artifact, then use an isolated candidate/pre-state, out-of-discovery-root
  compensation material, target-specific validation, an fsync-backed
  transaction journal, atomic promotion where supported, restart-safe recovery,
  a receipt, and verified restoration.

The user's latest dependency-maintenance choice is named **Update Policy U1**
in this contract: a weekly one-shot read-only audit is installed for the
current macOS user, while every update remains explicitly approved. U1 is a
maintenance policy inside the already selected workflow **Scheme C**; it is not
the earlier workflow Scheme A that would replace Superpowers. The scheduled job
is not a resident daemon and never chains into `apply`. An on-demand invocation
also rejects a stale scheduled result and refreshes the audit before making a
freshness claim.

The current schedule is fixed to Monday at 10:00 local time. Registering,
removing, or changing that LaunchAgent is itself a Router-governed,
planned/backed-up/verified mutation; only execution of an already-installed job
is the read-only audit path.

The conversational triggers are `$codex-skill-update`,
`Codex Skill 更新巡检`, `检查 <skill> 更新`, and
`生成 <skill> 升级计划`. The implementation must not shadow or patch the
`codex` executable to manufacture a nonexistent `codex skill update`
subcommand. Narrow implicit discovery is allowed only because the public Skill
path is non-mutating; every mutation request returns to the Router.

## Source and runtime boundaries

The controller is an optional sibling Skill rather than a new Router route:

| Surface | Proposed responsibility |
|---|---|
| `../codex-skill-update/` | Independent source tree and future Git repository |
| `~/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update/` | Quarantined first attempt; preserve-only evidence, never reused/repaired/deleted |
| `~/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update-v2/` | Absent replacement implementation worktree requiring new exact approval |
| `${CODEX_HOME}/skill-releases/codex-skill-update/<payload-sha256>/payload/` | Exact immutable allowlisted runtime payload with sibling canonical runtime lock |
| `${CODEX_HOME}/skills/codex-skill-update` | Atomic discovery symlink to exact release `payload/` |
| `${CODEX_HOME}/skill-update/` | Registry, sanitized reports, plans, receipts, lock, and backups |
| `${CODEX_HOME}/openspec-superpower-change/bootstrap-control/codex-skill-update/` | Router-owned first-install plan/approval/lease/journal/receipt root outside updater destinations |
| this repository | OpenSpec contract and bilingual integration documentation |

The sibling source path is a bounded approval-time assumption. No `git init`,
staging, commit, remote creation, push, plugin installation, or publication is
authorized by this draft.

The quarantined attempt is observed at HEAD
`92fce4cfea0fbaf0dd1dfbcc7cc320a5aafa7958` / tree
`9799a5f6add566977e4e997bce57314fc81f28c4`. It has manifest
`71c9773b0ac52589bb2e738757a42aec9116e7a7eb89f5af52881d4d6a61233d`
while the current artifact bytes require missing manifest
`b9f46ca5f253d11b8026131c23692f8e1e11ee72a757d47e0c83d65d4bbcf9e3`
and missing proposal/tasks snapshots
`2354ccc1aae092e409802e48efb1fb00b997d0365c94a7eaf22f0a40b4f3a03d` /
`d4e9c32a7ce2c10ae6526a2d5fc328d75f4c0d99f34c7ffd72c1cdfbc8d2b6c9`.
The schema-2 source-bootstrap prestate binds the full observed map and
preserve-only policy before a distinct absent replacement target may be used.

The first exact v2 decision was recorded as immutable manifest
`7df5c5ee0d3022dbed1f19c5de9e16855982b06c20fca49b99ffc742e9c3c0ff`,
but its helper failed closed before any source write: recording that manifest
raised the APFS `approvals/` `st_nlink` from the reviewed baseline 7 to 8, while
the helper still demanded 7. The v2 ref/reflog/admin/worktree, lock, journal, and
sibling source all remained absent. The manifest and snapshots are preserved as
failed-decision evidence and cannot authorize the corrected helper.

The corrected helper treats those link values as pre-decision baselines. On the
bound APFS volume it applies one closed phase table to lexical and retained-FD
checks: `approval-recorded` permits only the manifest; `journal-ready` permits
only the manifest, held approval-directory lock, and source-bootstrap journal;
`post-bootstrap` retains those entries and permits only the final ref, reflog,
admin directory, and replacement worktree in their respective parents.
Transient ref/reflog lock files must be absent at post-verification. Every
unlisted link-count delta or unknown phase blocks and requires reapproval.

The current proposal/context/review artifacts are untracked. After exact
approval, the worktree bootstrap preserves the old
`add-codex-skill-update` branch/worktree/admin path without mutation and creates
the local `add-codex-skill-update-v2` replacement branch/worktree. It copies only the approved task-local
files, content-addressed approved-byte snapshots, and immutable authorization
manifest plus bound sandbox profile to the same paths with
no-follow/no-overwrite semantics, verifies the
snapshot raw SHA-256 set, and requires every approved material path to remain byte-identical to
approval until task 2.1 post-verification. No checklist marker changes before
that boundary; task 2.1 materializes each approved byte stream exactly once.
Checklist-only progress may begin afterward under the unchanged contract
projection. It reruns strict validation before implementation. That approval
grants no staging, commit, or publication. The bootstrap does not copy the unrelated
`streamline-workflow-prompt-contracts` change.

The failed decision's manifest and raw snapshots are never adopted. The
content-addressed `eb8ddf6e...` sandbox profile is authority-neutral mechanism
content: it may be copied only after the corrected helper independently proves
exact expected bytes and the new manifest plus new exact user decision rebind
its hash. The old manifest grants no authority, and the quarantined
`892aec1c...` profile fails the current expected-byte check.

The approval manifest additionally binds the exact repository/common-Git-dir
identity, current complete security-relevant ref/worktree/local-config prestate
digest, every
repo/Git/ref/log/admin/worktree-parent no-follow device/inode component,
expected absence of the branch/ref-log/worktree/admin paths, base commit/tree,
fixed read-only Git identity, full helper/sandbox/profile/exec-vector identities,
and the complete approved untracked material hashes. The helper's read-only
`--launch` mode validates that closure and execs its exact inline-profile
sandbox vector; the self-attesting `--contained` mode owns the full task-2.1
transaction. It retains/revalidates every mutable parent including the approval
directories, fsyncs the exclusive lock/journal, atomically reserves the target
inode, creates the exact ref/reflog through no-replace hard-link promotion, and
creates the worktree-admin/target/material/index closure through directory-FD-
relative writes. Network and every child executable except the exact helper
interpreter and fixed read-only Git binary are denied. The base tree is
materialized from OID-reverified raw `ls-tree`/`cat-file` blobs, not checkout
conversion, and a valid Git index v2 is generated directly. Before/after
inventories and parent identities must differ only by the named ref and
worktree mapping. Parent/target exchange,
wrong base, an existing target, extra mutation, malicious filter/config, or
interrupted residue blocks without reuse, forced repair, deletion, reset, or
cleanup under this approval. If the platform cannot prove descriptor continuity
and sandboxed no-replace containment, Git is not launched.

Only `refs/codex/turn-diffs/` is excluded from ref-content binding because it is
a control-plane-owned volatile checkpoint namespace. The exclusion and policy
are themselves bound, the bootstrap sandbox cannot write there, and every
other ref remains exact and drift-blocking.

Before any state write, the controller builds a global ownership graph for the
Bootstrap Control Root plus state, discovery, package source, runtime, release,
candidate, backup, and managed target roots of every package. It verifies lexical containment,
`lstat`, real paths, device/inode identity where paths exist, current-user
ownership, and restrictive permissions. Except for the two exact declared
projection forms, independent package-owned roots may not overlap, contain, or
alias one another. Manager/OS-owned state, temporary, discovery, and release
containers are non-package anchors: a reviewed fixed layout may lease exact
children/subtrees to controller roles, transactions, or packages, while
controller-state metadata/backup/journal children remain one controller domain.
A whole-container claim, cross-domain overlapping child lease, or
anchor-addressed mutation is rejected. An environment override, cross-package
alias, or alternate package ID resolving to the running updater payload is
rejected.

The Router remains the state-changing control plane. Read-only audit, plan, and
verify may run directly through the new Skill. Apply, user-requested post-success
rollback, registry replacement, schedule installation, and schedule removal
must re-enter
`openspec-superpower-change`, honor Major Self-Evolution when applicable, and
record a current action-bound approval artifact. Automatic compensation after
an approved mutation starts uses a pre-intent single-use restoration lease and
does not request a second decision; approval expiry/revocation stops forward
progress.
The first updater installation is the distinct `bootstrap-apply` action. This
Major source approval may create only the restrictive Router-owned
`${CODEX_HOME}/openspec-superpower-change/bootstrap-control/codex-skill-update/`
governance root outside every updater destination plus only its missing fixed
manager-owned parent anchors. Each parent is created with anchored no-replace
and fsync; the final root is atomically promoted from a same-filesystem
candidate whose stable canonical marker binds only target, package, schema, and
Router control plane and whose fixed closure includes the operation lock.
Each Major manifest receives a separate immutable child workspace for bootstrap
authority, exact no-overwrite Major manifest/raw-snapshot copies, and closeout
evidence; reapproval preserves older workspaces, and any unfinished journal in
any older workspace must recover or block before new work.
Empty/unmarked or foreign roots are never adopted. This root initializer is the
only pre-operation-lock path and cannot probe or write updater targets. Only
after source High
Review PASS does the Router, running from fixed reviewed source outside the
destination, write there a fresh deployment plan binding its own exact
executable/code/source identity plus the exact initial registry/state
layout/group/adapter closure and obtain a separate exact action approval. This
Major contract approval alone is not runtime installation authority.

## Exact rule draft

The new Skill contract will include rules equivalent to:

```text
Audit never updates a managed Skill, fetches into a live checkout, refreshes a
plugin marketplace, or chains into apply.
Observation and notification select only a closed built-in adapter enum with a
fixed absolute executable and argv schema. Registry values are data, never
commands, shell fragments, executable paths, or notification programs.

Keep tested compatibility baseline, effective local version, latest observed
upstream version, and installation-channel available version as four distinct
values. Unknown or incomparable evidence is BLOCKED/UNKNOWN, never CURRENT.

Model one updateable package separately from its discovered Skill entries. One
Superpowers repository/collection owns every `superpowers:*` entry; duplicate
names or entries escaping the package root are MULTIPLE_SOURCES/BLOCKED.

Create an immutable plan bound to the registry revision, canonical package,
complete expected discovered-entry/projection set, resolved targets, current
fingerprint, candidate ref and fingerprint, validation executable/code identity,
argv/cwd/environment/network/write policy, fixed adapter/boundary timeouts, risk
classification, expiration, and rollback strategy. A plan is not approval.
Every installation mode can return a canonical diagnostic planning result, but
one that lacks an isolated complete candidate or safe adapter carries only its
blocker/resume condition and no actionable `plan-id`.
Normal plans live under validated controller state. The first
`bootstrap-apply` authority/plan/approval/lease/journal/receipt and final
closeout chain live in the current manifest-hash workspace under the stable
Bootstrap Control Root and create no updater destination state before action
approval. Its missing fixed parent anchors are individually verified and
created no-replace; its stable marked root is promoted atomically, then its
embedded operation lock is acquired before selecting/creating a workspace.
Only exact marked stranded roots/workspaces are resumable, and reapproval
creates a new workspace without rewriting prior evidence.
An adapter-specific candidate fingerprint binds the complete path/type/mode/
content/link closure, plus Git object-format/commit/tree/ref/submodule evidence
when applicable. A Major plan additionally binds the exact approved OpenSpec
change-id, immutable manifest hash, raw proposal/design/spec/tasks SHA-256 set,
checklist-normalized contract-projection digest, decision provenance, and
decision time. Later progress ticks do not rewrite this manifest; any
contract-bearing projection change requires a new approval. The approval-time
record is
`openspec/changes/add-codex-skill-update/approvals/<manifest-sha256>.json`;
reapproval creates a new immutable manifest rather than rewriting prior
evidence. Before any progress marker changes, the exact four approved byte
streams are preserved with no-follow/no-overwrite semantics at
`approvals/artifacts/<artifact-sha256>` so the manifest's raw hash set remains
reproducible.
The public maintenance CLI exposes no direct mutation command. The Router
records a canonical action/target/scope/expiry-bound approval artifact after
the user's exact decision, and only the internal transaction entrypoint accepts
that artifact. For Major work, its scope hash contains the same OpenSpec
authorization binding. The binding is audit evidence, not a cryptographic proof
of a human identity; the Router remains responsible for the decision.
Revocation uses a separate Router-owned append-only authority channel with a
short no-follow authority lock. A transaction holds that lock from the
revocation/expiry check through durable intent, atomic mutation, fsync, and
boundary result, so revocation can be recorded while the long operation lock is
held and has one order relative to every boundary.

Apply only the exact user-approved current plan. Recheck every binding before
mutation; stage and validate outside the live target; back up outside every
Skill discovery root. Managed directory installs use immutable version
directories and a conditional final-child switch. Creation uses atomic
no-replace; replacement uses atomic exchange that preserves and verifies the
displaced object; removal exchanges with a unique tombstone and then
exclusively relocates/verifies that tombstone so the destination is absent.
Identity drift restores or preserves every object, never unlinks a mismatch,
and blocks when no safe platform primitive exists. Terminal unlink is confined
to a continuously verified transaction-exclusive private closure; otherwise
quarantine is retained with a cleanup blocker. An existing plain copied directory is
`BLOCKED_LAYOUT_MIGRATION` until separately approved migration. Verify fresh
discovery and version evidence, then write a receipt. Before the first mutation,
write and fsync a canonical journal binding plan/approval hashes, pre-state,
allowed paths, compensation material, and phase; while approval is current,
prepare a single-use restoration-only compensation lease before
`MUTATION_INTENT`, then activate it only when the fsynced intent transition
rechecks current/unrevoked approval; fsync each phase transition.
Every entrypoint detects an incomplete journal before new work. Public and
scheduled paths return `RECOVERY_REQUIRED` and re-enter the Router without
target mutation; Router-owned recovery uses only the compensation lease if the
original approval expired/revoked and never resumes forward mutation.
All entrypoints except the fixed-root initializer hold one verified no-follow,
owner/mode/nlink-bound controller operation lock across state
reads/probes/writes; bootstrap uses the lock embedded in the stable Bootstrap
Control Root, so audit cannot overlap registry/apply/schedule mutation and
consume mixed state.
Each target-changing substep durably records `MUTATION_INTENT` first. Only a
`PREPARED` phase with exact unchanged-pre-state proof may remove bound staging;
`MUTATION_INTENT` or later is treated as possibly changed and restores/verifies
the prior state unless a durable success receipt proves completion.
Missing, corrupt, or ambiguous recovery evidence returns `RECOVERY_REQUIRED`
without further mutation. A later post-success rollback
first matches the receipt-bound canonical after-fingerprint across payload
content/modes, discovery link metadata/target, resolved target, registry
revision/hash, and allowed-path-set hash. For `git-symlink`, that fingerprint
additionally binds repository identity, Git-dir/worktree paths, object format,
HEAD/tree/ref, index, remote/ref mapping, submodule state, canonical status, and
path/type/mode/content digests for every tracked and untracked worktree entry
outside Git internals.

Never pull, reset, clean, overwrite a dirty/ahead checkout, silently discard a
local patch, auto-update the controller executing the transaction, or treat a
Codex CLI/marketplace refresh as proof that an installed Skill changed. Version
1 permanently blocks controller self-apply and returns the Router-owned
deployment resume condition. Self-target detection uses the running executable,
payload, discovery, release, and resolved root identities, not a package name.
An external fixed Router with disjoint resolved identities may execute the
exact initial `bootstrap-apply` only when fresh evidence proves no running,
active discovered, or ambiguous updater installation; executor-to-target
aliasing or using bootstrap as an update shortcut still blocks.
Version 1 keeps plugin replacement audit/diagnostic-plan-only.

Bootstrap binds and installs only canonical initial registry bytes/schema/
revision/hash, exact state layout, complete package/entry/projection closure,
and adapter identities. Before planning/backup, the external Router uses those
candidate bytes to build the ownership graph against observed targets and the
Bootstrap Control Root without creating a destination registry. Any later
registry change is a separate
`registry-replace` plan/action and invalidates the installed schedule until a
separately approved schedule-replace succeeds.

A user-requested Git plan may create and remove only its fixed ephemeral
candidate store. An exact Git-backed apply approval may create only the
plan-bound immutable candidate checkout under its allowed release root. Neither
action initializes or mutates a sibling source, live checkout, or other user
repository and neither grants staging, commit, branch/tag/remote mutation,
reset, clean, push, or publication.

Major version, trigger, routing, authority, evidence, completion, installation
lifecycle, or unresolved local-divergence changes are BLOCKED_MAJOR and require
an approved OpenSpec change whose exact artifact hashes remain bound through
plan, approval, and receipt.

Policy-required current/previous/schedule-referenced releases are
RETAINED_BY_POLICY. Any genuinely BLOCKED required cleanup or raw-trace
deletion stops closeout before final verification; an owner/resume note is not
gate approval. Final evidence is a canonical content-addressed no-overwrite
chain in the current Major workspace: canonical task-6.7 runtime-Review and
task-7.1 Project-Learning PASS prerequisites; a child eligibility record that
validates their exact kind/hash/manifest/time/parent chain; preliminary
verification whose parent is that eligibility hash and which binds governed
fingerprints, sanitized command/results/freshness, and raw-trace pre-hashes; a
child PASS binding verified trace absence and unchanged fingerprints plus the
predicted OpenSpec archive projection; then a later independent High Review
whose parent is that PASS and inspects the projection. Only that exact
archive/main-spec result may follow, and strict validation plus a child archive
receipt are required. Missing/wrong/stale eligibility, same-revision Review,
unsafe/non-canonical records, archive drift, or later governed-state drift
cannot support completion.

Audit may be scheduled; apply and rollback are never scheduled. Git staging,
commit, push, PR, release, and publication remain separately authorized.
```

The non-mutating schedule planner binds `schedule-install`,
`schedule-remove`, or `schedule-replace` to the fixed LaunchAgent label,
`gui/<current-uid>` domain, exact current-user plist/allowed paths, program argv
whose controller path is inside one exact content-addressed payload rather than
the movable discovery symlink, interpreter/executable identity, payload digest,
runtime-lock hash/exact closure, active discovery identity, controller
state-root identity, registry schema/revision/hash, group ID and complete
package/entry/projection closure, selected observation/notification adapter
executable/code/argv-schema identities, launchd
`Weekday=1`/`Hour=10`/`Minute=0` Monday fields, observed plist hash/mode,
normalized effective loaded-config fingerprint, candidate plist hash, expiry,
and failure rollback. A loaded job whose effective
configuration cannot be
proven to match the exact observed plist is `BLOCKED_SCHEDULE_DRIFT`; an absent
plist with a loaded label is also blocked. Changing an existing registration is
replace, not install. The Router's matching approval precedes mutation, and the
resulting schedule receipt binds plan/approval hashes and exact before/after
plist plus effective loaded configuration. Plist creation/replacement uses
atomic no-replace/exchange and verifies the preserved displaced object. Every
job run rechecks its exact payload/runtime lock/active discovery plus the full
schedule execution binding before package, network, or notification activity;
controller runtime, registry, or other drift requires a newly approved
schedule-replace. Neither a prior receipt nor a different action approval can
authorize a later schedule change.

Audit output keeps `freshness_status`, `observations`, `apply_eligibility`, and
sorted `reason_codes` as separate fields with deterministic precedence.
Specialized blockers such as `BLOCKED_LAYOUT_MIGRATION`,
`BLOCKED_RELEASE_COLLISION`, `BLOCKED_SELF_UPDATE`,
`BLOCKED_CHANNEL_MUTATION`, `BLOCKED_SCHEDULE_DRIFT`,
`BLOCKED_SCHEDULE_BINDING_DRIFT`, `BLOCKED_ROOT_ALIAS`, and
`BLOCKED_RECOVERY_REQUIRED` map to `apply_eligibility=BLOCKED`;
`BLOCKED_MAJOR` maps to `BLOCKED_MAJOR`. Transactions separately report exactly
one of `SUCCEEDED`, `BLOCKED`, `FAILED_COMPENSATED`, or `RECOVERY_REQUIRED`.
This keeps a `DIVERGED` observation and detailed cause visible while the
stronger apply or recovery decision remains authoritative.

## Installation modes and initial dependency group

The controller will model four installation modes without pretending that they
have identical update semantics:

1. `source-runtime`: compare a source tree with a copied runtime tree.
2. `git-symlink`: compare checkout, symlink target, local commits/dirty state,
   remote ref, and candidate ref.
3. `codex-plugin`: distinguish installed plugin version, current marketplace
   snapshot version, and separately observed upstream version.
4. `installer-snapshot`: bind the downloaded snapshot to its source ref and
   replace only through staged validation and rollback.

All modes support audit and plan. Version 1 keeps `codex-plugin` apply blocked
because no plugin-manager mutation authorization is defined. Other automated
apply is implemented only where the adapter can prove an isolated candidate,
deterministic target, complete validation, atomic promotion, and rollback.
Unsupported channel mutations return `BLOCKED_CHANNEL_MUTATION` with an exact
owner and resume condition rather than falling back to remove/reinstall guesses.

The first managed package group is `workflow-core`:

- `openspec-superpower-change`;
- `codex-brief-antigravity-review`;
- `superpowers`;
- `codex-skill-update`.

The Superpowers item is one package that maps all expected `superpowers:*`
discovered entries. `mattpocock/skills` remains an uninstalled candidate and is
not represented as an active dependency. Other discovered Skills without
registered provenance are reported `UNMANAGED`; the controller does not invent
their source.

## Candidate files

### New sibling source

- `AGENTS.md`
- `SKILL.md`
- `agents/openai.yaml`
- `references/update-contract.md`
- `references/installation-modes.md`
- `references/version-ledger.md`
- `references/runtime-manifest.json`
- `scripts/codex_skill_update.py`
- `scripts/validate_update_contract.py`
- `templates/registry.example.json`
- `templates/com.openai.codex.skill-update-audit.plist`
- `tests/test_skill_contract.py`
- `tests/test_update_engine.py`
- `tests/fixtures/forward-cases.json`
- `README.md`
- `README_cn.md`
- implementation evidence under `docs/design/`

The runtime release is built only from the reviewed, repository-only
runtime-manifest allowlist. The builder produces a canonical runtime lock with
sorted safe POSIX relative paths, regular-file type, normalized mode, and
content SHA-256, then derives the payload digest from domain-separated canonical
lock bytes. Repository-only AGENTS/README/test/fixture/OpenSpec/Git/design files
are not copied into the discovered Skill payload. Missing, extra, traversing,
backslash-containing, symlinked, hard-linked, mode-changed, or content-changed
entries fail closed. Release finalization requires an atomic no-replace
primitive. An existing same-digest release is verify-only: exact closure is
reused; any mismatch is `BLOCKED_RELEASE_COLLISION` and is never overwritten.
The digest directory itself contains exactly `payload/` and
`runtime-lock.json`; the lock and every existing ancestor are checked with
no-follow semantics, and the lock is a current-user-owned single-link regular
file with mode `0644` and canonical bytes.

### Current repository

- `CONTEXT.md`
- `README.md`
- `README_cn.md`
- focused integration assertions in `tests/test_workflow_rules.py`
- the active OpenSpec artifacts for `add-codex-skill-update`
- `docs/design/evidence/add-codex-skill-update/source-bootstrap-v2-helper.py`
- `docs/design/evidence/add-codex-skill-update/source-bootstrap-v2-prestate.json`
- the content-addressed v2 source-bootstrap sandbox profile
- the exact Review-predicted post-archive
  `openspec/specs/skill-update-governance/spec.md`

The Router `SKILL.md`, its portable manifest, and its cross-CLI runtime copies
are not candidate files. The updater remains optional and Codex-specific.

## Validation and forward-test plan

A non-live synthetic layout probe at
`/private/tmp/openspec-worktree-layout-probe-20260804` reproduced the helper's
exact `commondir`/`gitdir`/`HEAD`/`ORIG_HEAD`/logs/target-gitfile/ref structure
while using only a read-only object alternate. Git 2.49.0 resolved the expected
common directory, linked target, branch, HEAD, and base tree through both
`rev-parse` and `worktree list --porcelain`. The initial probe exposed a real
RED gap: without a generated index, every base path appeared deleted. The
corrected helper materialized 169 raw base blobs and generated a v2 index at
SHA-256 `ea36afd1de3e0980a630896765250e034af7c8882699c9348d6dd9980e963800`;
Git 2.49.0 then returned zero porcelain status bytes and left that index hash
unchanged. This is mechanism evidence only;
it creates no authority and touched no live ref/worktree path.

A second deny-default sandbox probe used an `os.path.realpath` temporary
replacement root and the same literal/subpath rule shape as the reviewed
profile. The contained Python process successfully performed descriptor-based
`mkdir`, O_EXCL write, `fchmod`, file/directory `fsync`, hard-link no-replace
promotion, lock unlink, and Python-to-bound-Git `--version`/`rev-parse`; an
outer read-only closure check passed. The first probe intentionally exposed the
lexical binding: a `/var/...` profile did not authorize the real
`/private/var/...` inode and sandbox denied the first `mkdir`. A separate
inventory RED showed that file-only walking missed extra empty directories;
the corrected helper binds exact file and directory sets plus directory
owner/mode and rejects empty or ignored extras. These probes used temporary
paths only and created no live v2 source state or authority.

A focused source-bootstrap regression first failed because the reviewed helper
had no phase-aware parent-link function. After correction, five tests bind the
entire phase table by exact dictionary equality, derive the current `8 -> 9 ->
10` approval-directory expectations from the canonical prestate, cover every
parent-closure path, bind all helper call sites to their required phases through
AST inspection, and enforce unlisted/unknown-phase fail-closed behavior. This
test is approval-bound supporting material and grants no task-2.1 authority by
itself.
A disposable same-filesystem APFS probe independently observed `st_nlink`
`2 -> 3 -> 4 -> 3 -> 4` for empty, one file, hard-link promotion, transient-lock
removal, and one file plus one directory, respectively; only the probe's own
temporary closure was removed.

After approval, use Skill TDD:

1. Run seven fresh-agent pressure scenarios without the candidate Skill and
   preserve the observed RED behavior.
2. Add deterministic RED tests for contract ownership, quarantined-worktree
   drift and no-repair/no-reuse enforcement, closed non-mutating
   audit/notification adapters and malicious registry commands, version
   separation, dirty/ahead Git protection, stale-plan rejection,
   package/entry mapping (duplicate names, escaping entries, and no independent
   Superpowers sub-Skill update), global root ownership/alias containment plus
   allowed controller/package/transaction sibling leases and blocked
   whole-container/anchor-addressed/cross-domain overlapping leases,
   action-bound and Major OpenSpec hash mismatch, compound-status/reason/result
   precedence, immutable raw-artifact snapshot tamper/collision and canonical
   projection order, source-worktree repository/Git/sandbox/base/prestate/
   target-absence/material-hash mismatch, ref/log/admin/worktree-parent
   exchange, target takeover/symlink insertion, reservation/profile/
   write-allowlist drift, force/reuse/reset prohibition, malicious hook/filter/
   process/config/helper/prompt/network denial, raw-blob materialization,
   before/after ref/worktree/config closure, pre-bootstrap marker rejection,
   post-bootstrap normalized marker acceptance, and interruption residue
   blocking, Bootstrap Control Root anchored parent creation,
   stable-marker/embedded-lock promotion plus per-manifest reapproval workspace
   isolation, pre-approval destination non-mutation and exact initial registry/
   state/group/adapter binding, operation-lock-independent revocation channel
   permission/link/canonical/collision checks and authority-lock linearization
   at every boundary, approval expiry/revocation and restoration-only lease
   behavior at every phase,
   expected-absent no-replace, expected-present replacement
   exchange, and removal exchange/tombstone/exclusive relocation under
   last-check drift while preserving/restoring the displaced object,
   external same-package bootstrap versus executor alias, real subprocess
   hard-kill at mutation-intent/bootstrap boundaries plus restart recovery,
   stale/failed/
   eight-day report boundaries, temporary candidate cleanup, argv/no-shell/
   metacharacter/ref-as-data/cwd containment, runtime-lock and lock-file
   path/type/mode/content/hardlink/top-level exact closure, no-replace
   finalization and collision behavior, schedule-plan/receipt/action/
   registry-group/state-root/exact-controller-payload/runtime-lock/
   active-discovery/loaded-config/real-Monday binding and runtime/registry
   schedule invalidation, receipt-bound
   adapter-specific after-fingerprint drift including Git checkout drift,
   failed-validation compensation, persistent versus transaction cleanup
   authority, required-cleanup BLOCKED stop, canonical preliminary/PASS/
   independent-Review schema and parent chain, trace absence, post-seal drift,
   predicted/actual archive-main-spec inventory and strict child receipt,
   sensitive-output hygiene, and alias-resistant self-update blocking.
3. Implement the smallest controller that makes those tests GREEN.
4. Run sibling `quick_validate.py`, `validate_update_contract.py`, and its full
   dependency-free unittest suite.
5. Run this repository's required `quick_validate.py`,
   `validate_core_gates.py`, and full unittest suite.
6. Run isolated forward scenarios:
   - audit-only under time pressure;
   - diverged Git+symlink checkout;
   - marketplace snapshot newer while installed version is unchanged;
   - installer snapshot candidate whose validator fails;
   - Codex CLI newer while custom Skill is unchanged;
   - approved `source-runtime` happy path;
   - urgent “update everything” request without precise targets.
7. Run a distinct source High Review before runtime installation.
8. After runtime and schedule operations, run a second High Review over the
   installed payload, schedule, generated registry/report, rollback proof, and
   every public README claim. Fix, reverify, and re-Review until PASS before
   Project Learning Closeout.
9. After Project Learning Closeout, complete any authorized cleanup, persist
   sanitized evidence, and stop if any required cleanup or trace deletion is
   `BLOCKED`. Then run one fresh post-cleanup final verification, persist the
   canonical content-addressed preliminary record before deleting its bound raw
   traces, verify exact absence and unchanged governed fingerprints, and create
   the child PASS seal. Start the distinct final High Review only in a later
   child record and Review the predicted canonical OpenSpec archive projection.
   After PASS, only the immutable closeout evidence plane, normalized checklist
   progress, and that exact Review-approved archive transition may change
   without invalidation. Verify actual archive inventory, strict validation,
   and a child archive receipt; later governed-state cleanup/correction or
   archive drift invalidates both gates.

The baseline and forward runner may not read an expected answer, design
document, or tests. RED runs have no candidate Skill in discovery and preserve
the observed result. GREEN runs use the same prompts and may discover the
candidate Skill normally through an isolated runtime, but the runner does not
inspect its body directly. Raw external CLI traces remain temporary sensitive
evidence; durable evidence retains only sanitized hashes, paths, commands, and
results.
After the last gate that needs them, raw traces are removed from their private
temporary directory. A blocked required cleanup records its owner/resume
condition and stops before final evidence.
Final-verification traces are removed only after their sanitized/hash-bound
command/result/freshness evidence is durable and before final High Review.

## Rollback

Before source implementation, record the sibling/Bootstrap Control Root/updater
destination pre-states and back up only current-repository or pre-existing
sibling-source files covered by the exact Major source approval. Runtime/state/
release backups wait for the exact `bootstrap-apply`; schedule backup waits for
its exact schedule approval. Before a normal managed Skill apply, resolve the
exact real target and store temporary compensation material under
`${CODEX_HOME}/skill-update/backups/<receipt-id>/`, outside all discovery roots
and with restrictive permissions; first-bootstrap compensation/journal evidence
stays in the selected immutable workspace under the independent Bootstrap
Control Root. Successful version-directory transactions retain the prior
immutable release plus its receipt as the post-success rollback point. Keep at
least the current and immediately previous verified release; cleanup is a
separately approved mutation and cannot remove the only known-good rollback
point or a payload referenced by an installed schedule.

Staging and compensation material that remains strictly inside an in-progress
transaction is removed as part of that same action only while approval remains
current and after a durable receipt or verified restoration. Lease-only recovery
after expiry/revocation retains leftovers until a new cleanup approval. Any
retained post-success, receipt-bound, rollback, or release material also
requires a new canonical cleanup plan and `cleanup` approval bound to its exact
paths and receipt. Journal finalization never expands either authority.

If replacement source implementation fails, restore only pre-existing changed
files and preserve any incomplete source worktree/ref/admin residue as a new
explicit recovery blocker; do not delete, repair, reuse, or adopt it. If runtime
installation, scheduled-audit installation, or a
managed update fails, restore the prior bytes, modes, and symlink target, verify
the restored fingerprint and discovery behavior, then stop.

Repository history is the long-term source rollback mechanism after separate
Git authorization. No destructive Git command or publication is part of this
draft.
