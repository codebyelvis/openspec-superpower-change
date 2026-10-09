# S8 Resumed Project Document Ownership Implementation Plan

Author: elvis. New readiness lineage after approved S9; original Plan/Review immutable.

> For agentic workers: use `superpowers:executing-plans` for inline implementation.
> Apply its Router-governed variant; independent instances perform gate Reviews.

**Goal:** Place ordinary documents using existing project conventions, preserve
position contracts, and verify authorized moves using actual files and links.

**Architecture:** One independent subsection in the existing learning reference
owns placement; SKILL/template navigate to it and its canonical resolver.
Extend the existing core validator and unittest file. Native agents select and
perform synthetic file operations through a private bounded I/O fixture; no
production path resolver, mover, registry or persistent runner is introduced.

**Tech Stack:** existing Python standard library, Markdown, unittest, ephemeral
native Codex, scoped cross-CLI transactions.

**Spec:** `openspec/changes/add-project-document-ownership/{proposal,design}.md`
and its `specs/skill-workflow-governance/spec.md`; draft-v1 approved by the exact
user command, recorded in this change's `approval.md`.

## Global Constraints

- Scope: SKILL, project-learning-closeout, learning-candidate-template,
  validate_core_gates, test_workflow_rules, CHANGELOG and S8-specific artifacts/
  iteration state only. Source baseline `44493026aa3897c243f4ebab9b37bd402170343e`.
- No source AGENTS/CONTEXT/engineering-guidance moves, historical/main-spec,
  S7/Handoff/companion/shared-governance/manifest/target/dependency edits.
- Preserve all 44 pre-existing unrelated files and S1–S7 backlog rows.
- Use the user-selected source/main workspace and existing one-round Git lease;
  no extra worktree/SDD workspace or per-task commits. Commit after final gates.
- Fresh backup and approved-byte snapshot are recorded in CURRENT; raw native
  traces stay privately there and are removed after applicable closure.
- Model/reasoning fixed gpt-6.1-sol/high. Existing authorization, learning,
  evidence and completion gates remain intact; metadata grants no authority.

## Review Focus

1. Directory presence or recency cannot replace evidence of local convention.
2. Explicit root guidance and special artifact paths cannot inherit a generic move.
3. A missing authorized inbound-reference closure stops before mutation.
4. Copied rule/default text outside its owning section cannot satisfy validation.
5. Native claims without actual output/link/scope checks cannot become PASS.

## Interfaces And Exact Commands

Existing `validate_project_learning_gate(skill, approved, completion,
learning_closeout, learning_template)` keeps its interface. Extend its checks
with `validate_project_document_ownership(skill: str, closeout: str,
template: str) -> None`, owned heading/row extraction, the engineering fallback
and navigation-only/template ownership checks. This is source-local validation,
outside shared Handoff API and parity blocks.

Add `ProjectDocumentOwnershipTests` to `tests/test_workflow_rules.py`, including
test-only snapshot/link/behavior assertions usable by the private forward probe.
No test helper selects a destination or moves a real project document.

Focused command:
`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_workflow_rules.py -k ProjectDocumentOwnershipTests -v`.
PyYAML interpreter for parity/quick: `/opt/anaconda3/bin/python3`.

Required source commands after GREEN:

```bash
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 /Users/elvis/.codex-account-a/skills/.system/skill-creator/scripts/quick_validate.py .
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 scripts/validate_core_gates.py .
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 -m unittest discover -s tests -v
openspec validate add-project-document-ownership --strict
```

## Task 1: Owned Placement And Regression

- [ ] Pass independent FULL_PREFLIGHT of this Plan before test/implementation edits.
- [ ] Write focused failing checks for the canonical ownership section and
  resolver fallback, old-root/relocated-policy false PASS, navigation-only entry,
  actual-file link/content/scope audit failures, and preserved root-path exception.
- [ ] Explicit approved negatives in ProjectDocumentOwnershipTests:
  `test_ambiguous_destination_requires_no_mutation`,
  `test_destination_collision_preserves_existing_content`, and
  `test_project_escape_preserves_bound_project`. Use actual private files and
  assert unchanged content/paths before resolution. Native blocked-branch
  evidence identifies the ownership condition; an I/O helper rejection alone
  does not prove destination ambiguity/collision was recognized before mutation.
- [ ] Run focused tests; require observed failures for missing ownership/default
  functionality, rather than typos or a helper import error. Record RED.
- [ ] Run the baseline native fallback case before editing rules. Its already
  accepted engineering lesson must expose the existing root fallback; actual
  fixture output/checks determine RED, not an answer-only route decision.
- [ ] Add the approved exact ownership rule, change only the unconstrained
  engineering resolver fallback, replace template duplication with a pointer,
  and add one matching-row SKILL navigation. Implement owned validator checks.
- [ ] Finish CHANGELOG Unreleased S8 source entry before source fingerprint and
  Implementation/fresh verification/Final; no fingerprinted source edit afterward.
- [ ] Reach focused GREEN in both parser modes; run required source commands.
  Existing AGENTS/root-guidance discoverability test must remain unchanged.

## Task 2: Real Native Acceptance And Independent Review

- [ ] Use a private stdlib probe at the implementation backup's `probe.py`,
  called as `python3 <backup>/probe.py --stage current --case conventions`,
  `--case fallback`, and `--case migration`. Baseline uses the same fallback
  prompt/checker with `--stage baseline`; inspect actual output and event audit.
- [ ] conventions: existing docs/ops deployment directory and explicit root
  engineering guidance are reused; special files retain bytes/paths.
- [ ] fallback: actual deploy/engineering documents land in purpose directories,
  engineering defaults to docs/engineering/engineering-invariants.md; no ordinary
  root addition or promotion triggered merely by reading ownership.
- [ ] migration: complete/ and blocked/ synthetic project roots exercise an
  authorized move plus an unauthorized inbound-reference branch. Complete move
  repairs inbound/outbound relative links/anchors and AGENTS navigation, retaining
  content; blocked fixture remains byte-identical. Unrelated history and all
  protected fixtures are unchanged. The two roots are one distinct mechanism.
- [ ] Require command events and actual file diffs. Only the private bounded
  `fixture_io.py` read/write/move commands may execute; it enforces root-bound
  regular-file reads and explicit per-fixture writes, never policy choices.
  Unknown tools/events, shell chains, missing output, changed immutable fixtures
  or failed link/content/scope assertions block PASS. Keep sanitized results only.
- [ ] Obtain independent Implementation Review of actual uncommitted scope,
  tests and native evidence, with a separate adversarial probe. Resolve same-scope
  findings by TDD/focused checks and the same review stage; no new Preflight.

Native execution uses stdin prompts and:
`codex exec --json --ephemeral --ignore-user-config --ignore-rules --model gpt-6.1-sol -c 'model_reasoning_effort="high"' --sandbox workspace-write --skip-git-repo-check -C <private-fixture> --output-last-message <private-result> -`.
Inherit existing HOME and account CODEX_HOME unchanged for authentication only;
never assign/repurpose HOME/CODEX_HOME, copy credentials/config or change settings/sessions. Disable unnecessary
native integrations using supported invocation options when available. Fixture
AGENTS limits tools to mechanical I/O; parent snapshots and JSONL audit fail closed.
Source and installed runtime are never writable probe fixtures.

## Task 3: Scoped Sync And Closure

- [ ] Run existing learning closeout if findings/corrections trigger it; preserve
  its existing threshold, durable path contracts and Review requirements.
- [ ] Generate schema-v2 sync plan selecting exactly openspec SKILL.md,
  references/project-learning-closeout.md, templates/learning-candidate-template.md,
  scripts/validate_core_gates.py; all unselected files and governance v6 are
  read-only assertions. Same four required targets, unchanged manifest.
- [ ] Independent Review checks selection/source hashes and destination pre-state;
  apply/verify each target in canonical order with private receipts/backups,
  then verify-all including validators/discovery. Failure restores current target
  and blocks later targets. Bind actual plan hash and commands in S8 evidence.
- [ ] Capture fresh final source/runtime verification, then obtain independent
  distinct Final Review; Final cannot reuse the Implementation Reviewer/author.
- [ ] Reconcile the 11 OpenSpec tasks and archive using `--yes --skip-specs`
  to preserve the excluded dirty main spec. Strict-validate exact archived bytes
  in a private copy when the CLI cannot address archive directory IDs directly.
- [ ] Update only mutable BACKLOG/LOG/CURRENT closure bookkeeping for S8, scope-check again,
  stage explicit S8 source/artifact paths, commit on main and push origin main
  under the existing iteration lease. Never include 44 unrelated files.
- [ ] Remove only owned implementation/proposal backups/raw traces after push;
  persist actual commit/cleanup result and finish the iteration report.

## Review Assignment, Stop And Rollback

Controller/author/executor `s8-control-01` maps to bound Codex `/root`.
Codex independent-reviewer/control-plane-high instances:
Preflight `s8-preflight-01`, Implementation `s8-review-01`, Final `s8-final-01`.
Purpose is the respective gate; authority `governed-review-evidence`, never
approval/state/completion. Bind actual tool instance IDs in Review artifacts.
Every dispatch includes Router-governed.md and the full relevant uncommitted diff.

Stop for unauthorized/protected scope need, changed acceptance/risk/authority,
failed/stale verification, missing native proof, unsafe pre-state or failed sync.
Source rollback restores only approved changed paths from the fresh backup;
runtime rollback uses the bound reviewed transaction. Preserve unrelated work.

Plan self-check: all five new spec requirements map to Tasks 1–3; all five
Review Focus mechanisms have deterministic checks and actual native evidence.
Task interfaces: Task 1 produces the owned checks/test audit, Task 2 consumes
that audit for actual native outputs, Task 3 consumes reviewed source/evidence.
No other task system, fresh decision or duplicate design approval is needed.

## Exact Sync Bindings (F3 Plan correction; planned only)

Use private transaction root
`/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/openspec-S8-resumed-jd5ww5mw/sync`
as S8_SYNC; set S8_PY to `/opt/anaconda3/bin/python3`. No commands below have
applied a runtime change. Create that private directory only when execution is
eligible. Keep the S7 canonical target roots; the current account CODEX_HOME is
an authentication location, not authorization to retarget synchronization.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py plan --manifest references/cross-cli-portable-manifest.json --openspec-source . --brief-source /Users/elvis/file/develop/opensource/codex-brief-antigravity-review --codex-skills-root /Users/elvis/.codex/skills --codex-rule-file /Users/elvis/.codex/AGENTS.md --pi-skills-root /Users/elvis/.pi/agent/skills --pi-rule-file /Users/elvis/.pi/agent/APPEND_SYSTEM.md --antigravity-skills-root /Users/elvis/.gemini/antigravity-cli/skills --antigravity-rule-file /Users/elvis/.gemini/GEMINI.md --grok-skills-root /Users/elvis/.grok/skills --grok-rule-file /Users/elvis/.grok/AGENTS.md --select-file openspec-superpower-change:SKILL.md --select-file openspec-superpower-change:references/project-learning-closeout.md --select-file openspec-superpower-change:templates/learning-candidate-template.md --select-file openspec-superpower-change:scripts/validate_core_gates.py --output "$S8_SYNC/plan.json"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py verify-prestate --target all --plan "$S8_SYNC/plan.json"
```

Expected exit 0: schema 2, four selected files, 36 read-only assertions/target,
unchanged governance v6 and target order. Review the actual plan SHA/pre-state;
run the exact two inventory checks below. Active legacy 4/5 or invalid records
block deployment; require active_legacy_count=0 in both actual outputs.

### Exact Source Companion And Legacy Checks

Companion source remains read-only. Before plan generation execute:

```bash
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 /Users/elvis/.codex-account-a/skills/.system/skill-creator/scripts/quick_validate.py /Users/elvis/file/develop/opensource/codex-brief-antigravity-review
PYTHONDONTWRITEBYTECODE=1 python3 /Users/elvis/file/develop/opensource/codex-brief-antigravity-review/scripts/validate_templates.py /Users/elvis/file/develop/opensource/codex-brief-antigravity-review
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s /Users/elvis/file/develop/opensource/codex-brief-antigravity-review/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py . --legacy-inventory-root /Users/elvis/file/develop/opensource/openspec-superpower-change/docs/agent-collab --legacy-inventory-output "$S8_SYNC/legacy-before-plan.json"
```

The existing CLI requires directory roots to exist. This exact command binds
the sole actually existing canonical docs/agent-collab root. Before planning and
immediately before apply, independently check the ten known canonical candidates
below for existence with Path.is_dir(), recording absolute logical path and bool
in sanitized S8 evidence. At the reviewed baseline the other nine are absent;
do not pass absent paths to inventory, create them or invent statuses. If any
additional candidate becomes present, stop planning/apply for reviewed existing
root coverage under the same sync scope; never silently omit it. Require
exit0 and active_legacy_count=0. Immediately before the FIRST runtime apply repeat
the same exact inventory command, replacing only output filename with
legacy-immediately-before-apply.json, and repeat verify-prestate --target all.
Bind both sanitized inventory results AND all ten root existence observations
in S8 sync evidence. Recheck the exact set immediately before first apply. No apply if either inventory
or any bound destination prestate has changed or fails.

For target IDs codex/pi/antigravity-cli/grok-cli in order, set S8_TARGET to the
actual ID and S8_SKILLS_ROOT to its exact root above. Execute separately and
capture exit 0 for each:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py apply --target "$S8_TARGET" --plan "$S8_SYNC/plan.json" --transaction-receipt "$S8_SYNC/$S8_TARGET.json" --backup-root "$S8_SYNC/backups"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py verify --target "$S8_TARGET" --plan "$S8_SYNC/plan.json" --transaction-receipt "$S8_SYNC/$S8_TARGET.json"
PYTHONDONTWRITEBYTECODE=1 "$S8_PY" /Users/elvis/.codex-account-a/skills/.system/skill-creator/scripts/quick_validate.py "$S8_SKILLS_ROOT/openspec-superpower-change"
PYTHONDONTWRITEBYTECODE=1 "$S8_PY" /Users/elvis/.codex-account-a/skills/.system/skill-creator/scripts/quick_validate.py "$S8_SKILLS_ROOT/codex-brief-antigravity-review"
PYTHONDONTWRITEBYTECODE=1 python3 "$S8_SKILLS_ROOT/openspec-superpower-change/scripts/validate_core_gates.py" "$S8_SKILLS_ROOT/openspec-superpower-change"
PYTHONDONTWRITEBYTECODE=1 "$S8_PY" "$S8_SKILLS_ROOT/openspec-superpower-change/scripts/validate_core_gates.py" "$S8_SKILLS_ROOT/openspec-superpower-change"
PYTHONDONTWRITEBYTECODE=1 python3 "$S8_SKILLS_ROOT/codex-brief-antigravity-review/scripts/validate_templates.py" "$S8_SKILLS_ROOT/codex-brief-antigravity-review"
PYTHONDONTWRITEBYTECODE=1 "$S8_PY" "$S8_SKILLS_ROOT/codex-brief-antigravity-review/scripts/validate_templates.py" "$S8_SKILLS_ROOT/codex-brief-antigravity-review"
```

With the same `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py`
prefix, codex/pi/antigravity-cli use `verify-discovery --target "$S8_TARGET"
--plan "$S8_SYNC/plan.json" --transaction-receipt "$S8_SYNC/$S8_TARGET.json"`.
Grok instead captures `grok inspect --json` privately to 0600
`$S8_SYNC/grok-inspect.json` without echo, then uses `verify-discovery --target
grok-cli --plan "$S8_SYNC/plan.json" --transaction-receipt
"$S8_SYNC/grok-cli.json" --inspect-json "$S8_SYNC/grok-inspect.json" --consume`.
Do not also run the generic Grok form or invoke Pi as a process.

After each verified/discovered target, run `commit-target --target "$S8_TARGET"
--plan "$S8_SYNC/plan.json" --transaction-receipt "$S8_SYNC/$S8_TARGET.json"`
with that prefix. After all four, run `verify-all --plan "$S8_SYNC/plan.json"
--transaction-root "$S8_SYNC"`. All required targets must be verified.

On failure stop later targets. The same prefix's `restore-target --target
"$S8_TARGET" --plan "$S8_SYNC/plan.json" --backup-root "$S8_SYNC/backups"
--transaction-receipt "$S8_SYNC/$S8_TARGET.json"` restores the reviewed preimage.
Where pending-journal recovery applies, use `recover-pending --plan
"$S8_SYNC/plan.json" --backup-root "$S8_SYNC/backups" --transaction-root
"$S8_SYNC"`. Preserve receipt/authorization checks; no manual runtime copying.

## Fresh Changed-Binding Readiness Root

Original Plan SHA d8baab34dedc8043c857df53e62387d6a0d8b6078a27a8ddfeb7c37e3f582df6
and original BLOCKED Preflight f68f1bd8b3d344a3dce787ac5886ea9a0a609c0365d7337d4b6b10a9611af629
remain immutable history. This Plan starts a new FULL_PREFLIGHT lineage because
S9 specifically approved and implemented the protected stage binding change.
Do not use an unchanged-contract recheck or relabel the old BLOCKED result.

Original S8 approval SHA 233d318470241a5eb22eea9186bb372d72db6b65bf9556f6ffa818318e924873
and four-artifact draft-v1 remain authoritative. Current immutable context is
openspec/changes/add-project-document-ownership/resume-contract-v2.md, SHA
798ea76ff6b0dd62f59bc7062fd5acd3587bae2d55c43013ed9479a1b20e2a62.
Its exact full implementation-review/final-review assignments select s8-review-01
and s8-final-01. Use those distinct actual agents; no scope/risk/authority change.
S9 source 605a099 and final published tip 4449302, its accepted Final and actual
amendment proof establish the prerequisite. New S8 readiness remains pending.

Fresh private backup: /var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/openspec-S8-resumed-jd5ww5mw.
B denotes that exact path. Its source/runtime/four-contract/unrelated baseline
is post-S9; never restore pre-S9 runtime from the older S8 backup as this round's
rollback. Retain the two old S8 owned backups until actual S8 publication/cleanup.

## Exact Test And Native Interfaces

Task 1 produces only test-side `_document_snapshot(root: Path) -> dict`,
`_assert_document_links(root: Path, paths: list[str]) -> None`, and
`_audit_document_fixture(root: Path, before: dict, expectation: dict) -> dict`
in tests/test_workflow_rules.py. These audit observed files; they neither choose
destinations nor perform moves. The private probe imports those helpers and
checks actual native outputs, links/anchors and snapshots. Core rule validation
uses validate_project_document_ownership(skill: str, closeout: str, template: str)
inside the existing project learning validation path, with owned heading/row
checks; no new CLI option, production resolver, scanner or framework.

Focused tests explicitly cover owned subsection/default relocation, minimal
navigation, template resolver pointer, old default, unchanged explicit root
contracts, broken links/anchors, changed content, unauthorized history changes,
ambiguous destinations, destination collision and project escape. The latter
three each require real files and no mutation plus native recognition, never
only the I/O helper's rejection. Keep existing root AGENTS discoverability test
unchanged. Full existing suite remains mandatory in both parsers.

Private fixture_io.py is a root-bound mechanical CLI with
`python3 B/fixture_io.py <case-root> read <relative-path>`,
`write <relative-path> <base64-utf8-content>`, and
`move <relative-source> <relative-destination>`.
Only fixture-listed regular reads and explicitly authorized write paths are
accepted; it makes no policy choice. Parent audits every native command/event,
actual outputs and whole-fixture snapshots. Source/runtime are never writable
fixtures. Base64 is document text, never credentials or prompts in publication.

Conventions fixture proves established deployment navigation and root guidance
reuse: new deployment note links to the existing contracted guidance, which stays
byte-identical; empty alternative directory is insufficient convention evidence.
Fallback fixture permits BOTH old-root and new-purpose destinations so I/O limits
cannot force GREEN. Baseline reads current old resolver and creates actual files;
expected new engineering target must fail before rule edits. Current ownership
plus Target resolver must create actual purpose files. Reading placement alone
creates no extra promotion/candidate/Plan/Review or protected artifacts.

Migration native case contains independent complete and blocked roots. Complete
move repairs actual inbound/outbound relative links/anchors and AGENTS navigation.
Unauthorized-reference root, equally plausible indexed conventions, collision and
out-of-project destination roots must each explain its own blocker before ANY
mutation; unchanged paths/content and absence of write/move tool events are
required. Do not add a whole-project scanner or make a fixture helper solve policy.
The four actual native invocations are baseline fallback, current conventions,
current fallback and current migration with its stop branches; model fixed
 gpt-6.1-sol/high and events fail closed. Reuse unchanged evidence only by actual
source/rule/hash comparison, recording exact unaffected mechanisms honestly.

## Canonical Checkpoints And Distinct Final

Existing canonical path docs/agent-collab/add-project-document-ownership/status.md
and bound owner s8-control-01 remain. Ordinary blocked revision5->6 updates only
new Plan reference/condition/inputs, keeping immutable context and verified=null.
After this full BLOCKED result, ordinary blocked6->7 records the corrected Plan
and this immutable full Review. Terminal same-instance focused PASS then permits
ready-for-execution at the actual persisted blocked revision plus one, with
actual evidence and implement/local-edit; never replay historical revision7->8. Later legal source/Review/verification
transitions increment against actual prior bytes. No micro-step checkpointing.
For strict entry to awaiting-final-verification, bind implementation full Review
to actual previous ready-for-review bytes and current scoped fingerprint.
Persist fresh verified revision BEFORE dispatching s8-final-01. Complete requires
exact actual persisted previous, unchanged verified object and separate full Final.
Use the existing validator; Root alone accepts evidence and atomically writes.

Scoped fingerprints bind changed six production files, stable immutable approval provenance/
context, this frozen Plan, actual RED/GREEN/native/Preflight and required immutable
sync/learning proofs. Exclude canonical, mutable iteration/tasks and new evidence
outputs to avoid cycles. If immutable final evidence adds new inputs after source
Review, perform fresh same-stage Implementation re-Review at that fingerprint,
then persist new final verification and obtain distinct Final. Never restart
Preflight for ordinary implementation/review corrections.

## Owned Archive Path Binding And Publication

Only S8 is reconciled/archived with --yes --skip-specs. Its original approval,
four contracts and owned evidence remain unchanged except checklist progress and
mechanical moved navigation. This repo's existing docs/engineering-invariants.md,
AGENTS/CONTEXT, S9 artifacts and all unrelated/historical/main specs stay intact.

The approved resume-contract-v2.md has an immutable exact path/hash binding.
Archive does not permit rewriting progress.contract or re-signing a new context.
After native OpenSpec archive, retain the byte-identical immutable sidecar at its
ORIGINAL approved regular-file path, restore only that owned preimage, remove
its redundant newly archived copy, and immediately verify actual canonical
recovery against unchanged context. Archive the four contract files/approval,
strict-validate exact archived bytes as scheduled below. No other artifact is
restored at the original source location.
The residual original change directory is only this fixed metadata anchor;
OpenSpec list reports no-tasks, not an implementation proposal. Private actual
CLI feasibility already observed that behavior; it is a local S8 closure detail,
not a new rule/CLI/record schema or authority. Preflight must independently audit
this path-preservation arrangement and any real risk before implementation.

Publish only S8-approved six source files, S8 graph/context/canonical/new evidence,
owned archive and iteration metadata. Preserve all 44 unrelated files AND every
S9 immutable artifact. First scoped source/main push after all gates; verify exact
remote tip, then legitimate canonical completion/idle CURRENT/one LOG row and
owned metadata commit/push. Delete only three S8 owned backups/private traces/
transactions after required source and metadata publication; record actual
cleanup, fresh archive/link/scope checks and final owned bookkeeping push as
needed. No new slice starts in this round. Git style conventional, body S8.

## Plan Self-Check And Stop

All five spec requirements map to Tasks1-3; exact native mechanics, full dual
validation, protected path/reference closure, independent assignments, two-file
history preservation, four-target plan/receipt/discovery/rollback and source Git
lease are bound. The original F2/F3 corrections are included; F1 has separately
approved S9 enforcement. No new scope decision or repeated user confirmation.
Any excluded edit, actionable Preflight finding, unknown native effect, missing
real output/link proof, false/atomic signoff, stale required target or failed push
blocks its actual gate. Preserve backups and use existing adjudication rather
than granting new authority or repeating unchanged Preflight.

## Bounded Full-Preflight Corrections

Root full Review docs/review/2026-10-09-S8-resumed-preflight-full.json SHA
8651505d62a743d6fdece91d9ed7f347a8409fce8890d218ac3734ac38898372
binds original Plan550d1ca and all four findings once. This correction set is:
S8-PF-ARCHIVE-FRESHNESS (source update ordering, stable provenance, exact archived
execution root); S8-PF-PRESTATE-ARG (--target all); S8-PF-LEGACY-INVENTORY (ten
known roots, exact existing CLI, output and immediate repeat);
S8-PF-COMPANION-CHECKS (existing read-only source check matrix). Adjacent canonical
revision numbers and readiness metadata only reflect actual legal checkpoints.
Same actual s8-preflight-01 performs one terminal FOCUSED_RECHECK of these changes.
Original scope/spec/acceptance/risk/assignments/authority/paths/branch are unchanged.

Create immutable S8 evidence docs/review/2026-10-09-S8-approval-provenance.json
with exact original approval bytes233d318, original four approved contract hashes,
and observed existing user approval. It is a stable provenance copy, NEVER new
approval authority. Verify original bytes before archive and exact archived
approval bytes afterward. Bind this stable evidence path instead of future-moving
original approval in verified.inputs; approved progress.contract stays exact798.
No Resume schema/API/signoff/commands or protected artifact location rule changes.

Execute all SIX literal immutable critical commands above from source root after
source edits and again for the fresh persisted final verification. Record actual
execution roots. After Final, reconcile/archive only owned mutable tasks/navigation
and preserve byte-identical context at its exact path. Source CHANGELOG, frozen
Plan/provenance/native/learning/sync inputs do not change. Immediately recover
canonical and recompute scoped fingerprint; any drift blocks publication/completion
and invokes legal correction, same-stage Implementation re-Review, fresh persisted
verification and distinct Final before completion.

After archive, the source sidecar-only anchor is honestly no-tasks; active-ID
strict from source then exits1 and is not claimed PASS. Copy the four exact actual
archived contract bytes into B/archive-validation/openspec/changes/
add-project-document-ownership, with minimal isolated OpenSpec config; execute
the SAME sixth literal command openspec validate add-project-document-ownership
--strict from B/archive-validation and record its cwd, copied-file hashes, exit0.
This mandatory exact-archived-byte validation is additional closure evidence;
it never overwrites prior actual source critical results or context commands.
Verify original approval provenance, immutable context, links and all current
fingerprinted inputs after archive and publication. No new source input is
introduced merely by mutable closure evidence; do not erase stale-input detection.

### Exact Known Canonical Inventory Candidates

- `/Users/elvis/file/develop/opensource/openspec-superpower-change/docs/agent-collab`
- `/Users/elvis/file/develop/opensource/codex-brief-antigravity-review/docs/agent-collab`
- `/Users/elvis/.codex/skills/openspec-superpower-change/docs/agent-collab`
- `/Users/elvis/.codex/skills/codex-brief-antigravity-review/docs/agent-collab`
- `/Users/elvis/.pi/agent/skills/openspec-superpower-change/docs/agent-collab`
- `/Users/elvis/.pi/agent/skills/codex-brief-antigravity-review/docs/agent-collab`
- `/Users/elvis/.gemini/antigravity-cli/skills/openspec-superpower-change/docs/agent-collab`
- `/Users/elvis/.gemini/antigravity-cli/skills/codex-brief-antigravity-review/docs/agent-collab`
- `/Users/elvis/.grok/skills/openspec-superpower-change/docs/agent-collab`
- `/Users/elvis/.grok/skills/codex-brief-antigravity-review/docs/agent-collab`

The in-flight306332 draft's ten-root command actually exited1 for absent roots.
That failure is retained in focused Review; it grants no readiness. Before the
single terminal focused Review was issued, Root paused its unfinished inspection
and corrected only the original S8-PF-LEGACY-INVENTORY finding: exact sole existing
root CLI plus ten-root existence assertions. Parent full8651505/root550d and the
same actual reviewer remain; no extra terminal outcome, FULL round, contract,
protected boundary, permission or authority is introduced. Reviewer independently
assesses focused eligibility and may still BLOCK; Root never self-approves PASS.
