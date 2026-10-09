# S9 Stage-Specific Resume Review Implementation Plan

> For agentic workers: use superpowers:executing-plans, with the selected
> Router-governed.md substitutions. Execute inline; preserve standalone strict
> Preflight, Implementation Review and Final Review. Plan checkboxes are static
> steps; OpenSpec tasks and canonical status own progress. No second ledger.

Author: elvis. Date: 2026-10-09. Plan revision: 1.
Goal: represent approved distinct strict-local reviewers and perform only the
specifically approved, blocked S8 context-binding amendment.
Architecture: exact-shape selection in the existing context/Review validator;
one opt-in read-only amendment check; existing canonical state and sync protocol.
Tech: Python stdlib, existing optional PyYAML parser, unittest, local native Codex CLI.
Spec: openspec/changes/support-stage-specific-resume-review/{proposal,design,tasks}.md
and specs/skill-workflow-governance/spec.md, draft-v1 approved exact bytes.
Approval record: docs/review/2026-10-09-S9-stage-review-binding-draft.md, Specific
Approval Record / Resume Context / Resume Amendment Authorization. Earlier draft
phase labels are history; the new specific decision accepts the OpenSpec contract.

## Gate 0, identity and global constraints

Self-Evolution / approved-implementation; Major / strict. Selected writing-plans,
writing-skills, TDD, executing-plans (Router-governed), requesting-code-review,
verification-before-completion and finishing-a-development-branch at closure.
Use systematic-debugging if an unexplained failure actually arises. No repeat
brainstorming: the specific four-artifact contract has been approved.

The user already authorized this true-source main/current workspace, native
model gpt-6.1-sol with reasoning high, autonomous same-scope fixes and the fixed
single-round source Git/sync lease. No new checkout/worktree/cd or model switch.
Controller/author/executor is actual Codex /root, existing instance s8-control-01,
control-plane/control-plane-high; no assignment transfer or invented executor.
Preflight is distinct Codex s9-preflight-01, independent-reviewer/control-plane-high,
governed-review-evidence. Implementation and Final use the actual same distinct
reviewer s9-review-01 through separate dispatches, purposes and prior snapshots;
this old-format bootstrap is specified by S9 and does not weaken S8 distinct Final.
All dispatches carry the governed variant and exact purpose/product/role/profile/
independence/authority. Only /root accepts evidence, transitions and completion.

Structured backup B =
/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/openspec-S9-implementation-ahva86yn.
Do not set HOME/CODEX_HOME shell variables. Account auth remains where configured;
canonical sync Codex root is /Users/elvis/.codex, not the account configuration root.
Private fixture/proposed-state/trace files live under B or private temp directories
outside skill discovery. No runtime copy writes before scoped sync apply.

## Allowed files, preservation and stop conditions

Production changes: references/approved-implementation-workflow.md only in Project
Session Resume; scripts/validate_core_gates.py only resume helpers/explicit CLI;
tests/test_workflow_rules.py existing ProjectSessionResumeTests; CHANGELOG Unreleased.
Bookkeeping: S9 own OpenSpec/approval/Plan/Review/verification/archive/canonical
status, docs/iteration/CURRENT.md/BACKLOG.md/LOG.md. Unique other-change writes:
S8 new resume-contract-v2.md and its existing canonical status, preserving all
old contracts/history. No S8 implementation/tasks/Plan/review signoff.

Freeze all original S8 approval/proposal/design/spec/tasks/Plan/evidence hashes and
all 44 pre-existing unrelated dirty regular files from B/manifest.json. Keep S1–S8
scope/priority rows and S8 completed-contract checklist facts. Existing S8 approval
hash is 233d318470241a5eb22eea9186bb372d72db6b65bf9556f6ffa818318e924873.

Forbidden: SKILL trigger/routing, OpenSpec decision boundaries, Superpowers choice,
external Handoff/schema-2/standard/compact/legacy semantics, companion/shared rules,
manifest/targets, AGENTS/CONTEXT, distribution/dependencies/production/business docs,
other repositories, unrelated historical/main specs and destructive Git. Ordinary
same-scope fixes run to verification and independent re-Review. A needed excluded
change, invalid approval, unavailable required evidence or required target drift
records BLOCKED with actual owner/resume condition; never bypass or broaden scope.
Preflight ceiling: one FULL_PREFLIGHT plus at most one eligible terminal focused
recheck; protected change/conflict/non-convergence goes to control-plane adjudication.

## Review focus and proof mapping

- Mixed/malformed maps must fail by exact shape, without legacy/profile fallback.
- Stage substitution, Final/Implementation identity reuse, role/profile/purpose/
  independence/authority errors cannot become accepted evidence on recovery.
- Amendment cannot change owner/actions/commands/history/blocked facts or revive a
  verified/complete/external checkpoint; its approving record is hashed and scoped.
- CLI must bind the actual canonical previous bytes and reject opt-in without
  previous/status/root, or with full external --status. It never writes status.
- Publishing S9 must not stage the incomplete S8 graph or invalidate S8 bindings.

Each risk has an actual-file regression below. New unit evidence is synthetic
consistency proof; actual independent Review and native file-tool proof remain.
No equivalent timing/platform matrix is added. Full suite is mandatory governance
blast radius; dual interpreters check the existing optional-parser boundary.

## Task 1: readiness and immutable bootstrap metadata

- [ ] Record actual specific user approval and four hashes in the existing stable
  S9 draft/approval record; append exactly one old-format Resume Context and one
  exact scoped Resume Amendment Authorization, then freeze that file.
- [ ] Create canonical docs/agent-collab/support-stage-specific-resume-review/status.md
  blocked, unverified, wait/none until independent Preflight PASS; bind the Plan.
  Update S8 only through the existing ordinary same-context blocked transition:
  record S9-approved prerequisite and replace mutable S9 tasks/BACKLOG inputs by
  the immutable S9 approval record. No S8 context amendment before source gates.
- [ ] Independent FULL_PREFLIGHT reads complete current Plan/contract/approval,
  verifies parser/API/CLI feasibility, Git/publication/sync boundaries and performs
  a private independent adversarial probe. Persist full result verbatim at
  docs/review/2026-10-09-S9-preflight-full.json. Any finding blocks implementation.
  An ordinary declared correction updates Plan/status binding and can use the
  same instance's sole focused recheck, with real parent/root/current hashes.

## Task 2: TDD for both changed mechanisms

Files: tests/test_workflow_rules.py; production remains old until observed RED.
Add shared fixture helpers to this existing class, not a new class duplicating
inherited tests. All fixtures use real temporary regular files/commands/hashes.
New methods (one per behavior/mechanism, with relevant subTest tables):

- test_strict_stage_assignments_support_distinct_reviewers_and_recovery
- test_stage_assignment_shape_and_eligibility_fail_closed
- test_stage_forms_do_not_change_other_resume_profiles
- test_stage_completion_rejects_wrong_stage_and_stale_evidence
- test_stage_terminal_recovery_revalidates_both_reviews
- test_explicit_approved_stage_context_amendment_preserves_blocked_history
- test_amendment_preserves_context_authority_and_canonical_fields
- test_amendment_requires_approved_exact_scope_and_safe_hashes
- test_amendment_rejects_wrong_lifecycle_and_verified_previous
- test_amendment_requires_actual_previous_and_never_external_status
- test_resume_amendment_cli_binding_and_option_exclusions

Run targeted positives first (all command environments set PYTHONDONTWRITEBYTECODE=1):

    PYTHONPATH=tests python3 -m unittest test_workflow_rules.ProjectSessionResumeTests.test_strict_stage_assignments_support_distinct_reviewers_and_recovery test_workflow_rules.ProjectSessionResumeTests.test_explicit_approved_stage_context_amendment_preserves_blocked_history -v

Expected RED: stage mapping fails the old full-assignment check; opt-in API is
missing. The amendment test asserts supported interface before invoking it so
missing implementation is an assertion failure rather than an accidental TypeError.
Create a private native-forward.py under B. It copies the old validator/rule to
an isolated project, declares the synthetic approved distinct-stage scenario,
and invokes actual native Codex with read-only tool access to attempt it. Retain
actual CLI validation rejection/tool evidence as baseline RED, not new signoff.

    python3 B/native-forward.py --phase red --output B/native-red.json

The harness expects and audits the old-stage rejection; an unrelated CLI/auth
failure is environment evidence, not valid RED. B is expanded to the actual
absolute path when running. No private harness is added to repository or runtime.

## Task 3: minimal policy/API implementation and GREEN

Edit only the owned reference/validator/tests. Keep context outer fields and local
schema/progress shape fixed. Add RESUME_REVIEW_PHASES and a local assignment helper
that selects exact seven-key legacy or exact two-key strict map; validate both
map entries, phase-specific independence, owner and two-instance distinctness.
_resume_review selects by evidence_role, retaining its existing full binding checks.
Recorded-complete stage-form recovery checks both retained stage Reviews.

Extend validate_resume_record with amendment_approval: dict | None = None. An
opt-in requires actual previous text and a changed local strict contract ref;
otherwise reject. Validate the actual previous state/context through _resume_loaded.
Load the approving record once via _resume_ref, validate exact authorization keys
and approved/self-evolution/strict same-owner Resume Context with explicit
amend-review-binding/local-edit. Check safe distinct target path, old contract
ref and approved map. All context facts except assignment stay equal; new
Implementation entry exactly preserves the old assignment. Both records remain
approved/strict/blocked/unverified and otherwise equal except contract ref and
revision+1. Reject all unknown/duplicate keys, symlinks, stale hashes and forbidden
diffs. Ordinary immutable transitions and full external validation stay unchanged.

Add --resume-amendment-approval with a hashed-reference JSON value; parse it with
existing duplicate-safe JSON reader. Require --resume-status/--artifact-root/
--previous-status; reject --status and an external record. Use actual canonical
path checks and previous bytes already owned by the CLI. No authentication,
writer, signer, new state family or automatic migration is introduced.

    PYTHONPATH=tests python3 -m unittest test_workflow_rules.ProjectSessionResumeTests -v
    PYTHONPATH=tests /opt/anaconda3/bin/python3 -m unittest test_workflow_rules.ProjectSessionResumeTests -v

GREEN includes guarded positives and each declared negative, old strict single
assignment, standard/compact and existing full external cases. Preserve the
current atomic/stale/checkpoint/assignment negatives. Store actual RED/GREEN
commands and original/final rule/validator/test hashes in sanitized S9 evidence.

## Task 4: actual-file native proof and Implementation Review

Build private fixture workflow from the existing resume test fixture patterns,
with actual small app/test files and real verification process exits. The private
native harness invokes fixed gpt-6.1-sol/high via:

    codex exec --json --ephemeral --ignore-user-config --ignore-rules --model gpt-6.1-sol -c model_reasoning_effort="high" --sandbox read-only --skip-git-repo-check -C <private fixture> --output-last-message <private result> -

Use workspace-write only for the explicitly authorized private amendment scenario;
stdin carries private prompts, never shell interpolation. Auth remains at the
configured account; no token/key copying or refresh, session/config/rule mutation,
production/network probe or Pi process. Fixed per-call timeout 600 seconds;
poll in at most 60-second increments with progress updates. Do not print raw JSONL.

    python3 B/native-forward.py --phase green --output B/native-green.json

Required actual native scenarios/effects:
1. Distinct Implementation and Final review instances inspect actual files and
   actual verification, returning their own stage JSON; controller persists each
   legal revision. New read-only instance recovers pending final gates without
   impersonating the owner, and actual complete requires previous persisted bytes.
2. Authorized blocked old-context amendment: native tools validate the new
   actual context/proposed state with exact scoped approval, then only the bound
   fixture controller atomically replaces it after prior-byte equality; verify
   old contract/history equal and new status still blocked. Unauthorized branch
   is rejected before canonical mutation.
3. Compatibility/adversarial fixture assertions independently check legacy and
   external rejection, swapped/reused instances, unsafe refs/duplicate keys/stale
   evidence. These assertions call production logic on actual files; no mock source.

Audit completion and command/tool events fail-closed, bind actual native thread IDs
to declared fixture instances, process exits, source hashes and before/after inventories.
Synthetic fixture approval validates consistency only and is not source gate signoff.
Keep raw traces privately while needed, persist sanitized counts/hashes/results at
S9 native/red-green evidence paths. Unknown events/missing effects/off-scope writes
block proof. Source independent review is separately assigned through collaboration.

Run mandatory source verification commands from the immutable approval Resume
Context (quick, core dual, full unittest dual) and:

    OPENSPEC_TELEMETRY=0 openspec validate support-stage-specific-resume-review --strict --no-interactive
    git diff --check -- references/approved-implementation-workflow.md scripts/validate_core_gates.py tests/test_workflow_rules.py CHANGELOG.md docs/iteration

Run scope/link/hash checks against B/manifest.json, including 44 unrelated files,
all original S8 artifacts and approval, frozen four S9 contracts (checkbox progress
alone excepted), forbidden runtime/global-rule changes and exact portable selection.
Persist verification evidence using actual process results. Independent s9-review-01
reruns critical checks and its own adversarial amendment/recovery probe, reads the
complete actual scoped diff, and returns full Implementation Review. Resolve any
in-scope actionable finding through fresh verification and the same-stage re-Review.

## Task 5: exact existing four-target sync

Create/review immutable path/hash/prestate plan after Implementation Review PASS:

    python3 scripts/validate_cross_cli_sync.py plan --manifest references/cross-cli-portable-manifest.json --openspec-source /Users/elvis/file/develop/opensource/openspec-superpower-change --brief-source /Users/elvis/file/develop/opensource/codex-brief-antigravity-review --codex-skills-root /Users/elvis/.codex/skills --codex-rule-file /Users/elvis/.codex/AGENTS.md --pi-skills-root /Users/elvis/.pi/agent/skills --pi-rule-file /Users/elvis/.pi/agent/APPEND_SYSTEM.md --antigravity-skills-root /Users/elvis/.gemini/antigravity-cli/skills --antigravity-rule-file /Users/elvis/.gemini/GEMINI.md --grok-skills-root /Users/elvis/.grok/skills --grok-rule-file /Users/elvis/.grok/AGENTS.md --select-file openspec-superpower-change:references/approved-implementation-workflow.md --select-file openspec-superpower-change:scripts/validate_core_gates.py --output B/sync-plan.json
    python3 scripts/validate_cross_cli_sync.py verify-prestate --plan B/sync-plan.json --target all

Independent reviewer inspects actual plan/hash, exact two mutations per target,
unselected full assertions/v6 global rule parity and reviewed destination pre-state.
Inventory known canonical state for active legacy before planning and immediately
before first apply through existing --legacy-inventory-root/output interface.
No selectors/targets/manifest/shared body changes. For each T in the fixed order
codex, pi, antigravity-cli, grok-cli, use receipt B/transactions/T.json:

    python3 scripts/validate_cross_cli_sync.py apply --target T --plan B/sync-plan.json --transaction-receipt B/transactions/T.json --backup-root B/sync-backups/T
    python3 scripts/validate_cross_cli_sync.py verify --target T --plan B/sync-plan.json --transaction-receipt B/transactions/T.json
    python3 scripts/validate_cross_cli_sync.py verify-discovery --target T --plan B/sync-plan.json --transaction-receipt B/transactions/T.json
    python3 scripts/validate_cross_cli_sync.py commit-target --target T --plan B/sync-plan.json --transaction-receipt B/transactions/T.json

For Grok, capture grok inspect --json privately mode 0600, pass --inspect-json
<private inspect> --consume to verify-discovery; accept only current protocol's
user or verified earlier same-plan configToml source. Do not read/edit config.

    python3 scripts/validate_cross_cli_sync.py verify-all --plan B/sync-plan.json --transaction-root B/transactions

Failure blocks later targets. Rollback only reviewed selected target bytes through:

    python3 scripts/validate_cross_cli_sync.py restore-target --target T --plan B/sync-plan.json --backup-root B/sync-backups/T --transaction-receipt B/transactions/T.json

Do not manually copy runtime or restore unselected files/global blocks. Verify
all required runtime validators/discovery/full parity and receipt final states;
store sanitized source/target hashes and plan digest. Do not claim portable closure
with failed/stale discovery or an uncommitted transaction receipt.

## Task 6: sole S8 metadata amendment, learning and final gates

After source proof, Implementation Review and sync PASS, create only S8
resume-contract-v2.md by copying all old context facts and the exact approved
stage mapping from the frozen authorization section. Read the actual latest S8
canonical bytes. Proposed state keeps everything except contract ref and revision+1.
Store actual proposed bytes outside the project, then run both parsers:

    python3 scripts/validate_core_gates.py . --resume-status B/s8-proposed.md --artifact-root . --previous-status docs/agent-collab/add-project-document-ownership/status.md --resume-actor s8-control-01 --resume-amendment-approval '<actual hashed S9 approval JSON>'
    /opt/anaconda3/bin/python3 scripts/validate_core_gates.py . --resume-status B/s8-proposed.md --artifact-root . --previous-status docs/agent-collab/add-project-document-ownership/status.md --resume-actor s8-control-01 --resume-amendment-approval '<actual hashed S9 approval JSON>'

Expected factual result: blocked, verified_revision null, authority_granted false.
Before atomic replacement require actual canonical bytes still equal the validated
previous; keep the immutable prior snapshot in sanitized S9 amendment evidence.
The actual old contract and all original S8 artifacts remain byte-identical.
Then a separate ordinary same-context blocked transition updates only the blocker
reason/resume condition to fresh S8 readiness, without signing it or editing Plan.
Publish immutable sanitized S8 amendment facts/snapshots with source/old/new hashes,
not the incomplete active S8 graph. Keep S8 canonical/new context locally pending
its own authorized closure, and explicitly inventory this intentional local state.

Read existing project engineering guidance and project-learning-closeout; audit
the two original independent global signals and this change's correction history.
The new owned policy and deterministic regression provide durable enforcement;
record provenance in S9 closeout. Any new required project-local promotion follows
only approved scope; a protected expansion stops, never hides behind learning.

Fresh source checks cover all actual final source/evidence changes including
amendment. S9 verification fingerprint binds owned stable source/approval/test
and immutable amendment proof, not S8 future mutable checkpoints, CURRENT/BACKLOG
or the new verification evidence itself. Separately compare actual local S8 state
against captured amendment facts before final Review; report it as still blocked.
Persist verified awaiting-final-verification revision before distinct Final Review
by the same bound s9-review-01 instance. Final inspects actual complete diff and
reruns required verification plus an independent actual-file adversarial probe.
No source/learning change after this gate without affected verification/re-Review.

## Task 7: owned reconciliation, Git and cleanup

Reconcile only S9 checklist. Archive S9 with --yes --skip-specs; do not touch the
dirty main spec or any unrelated/historical change. If CLI cannot validate an
archive path, validate exact archive bytes under the actual ID in a private
isolated OpenSpec root. Repair only S9's moved relative navigation as mechanical
owned closeout metadata, recording old/new artifact hashes; do not change approved
scope/acceptance. Recheck actual archive strict, scoped links and runtime verify-all.
No --no-validate, force, reset/clean or publication beyond this repository.

Invoke finishing-a-development-branch under the Router: integration choice is
already authorized current-main commit/push, no redundant options question.
Stage only explicit S9 code/tests/CHANGELOG, own docs/canonical/archived artifacts
and iteration metadata. Never git add -A/., never stage original S8 graph or its
new context/status, or 44 unrelated files. Compare staged name/hash inventory
before each commit. First source commit uses existing conventional style with
body S9; push main and verify remote exact commit. Then record source commit and
complete S9 canonical against actual persisted verified/Final snapshot, restore
CURRENT to preserved S8 pending fresh-readiness state, append LOG once and commit/
push only final owned bookkeeping if needed. No unreviewed implementation in that
metadata commit. Verify exact remote tip; a failed push keeps backups and pending
iteration state, never declares closure.

After successful required publication delete only this S9 implementation/proposal
backup and private traces/receipts/fixtures, with validated containment/non-symlink
paths. Retain S8 backups because its scope/rollback is unfinished. Cleanup records
must not delete raw artifacts before durable sanitized evidence exists. Report
only the contract's five fields and next S8 resume phrase; do not start S8 as part
of the same approved S9 slice.
