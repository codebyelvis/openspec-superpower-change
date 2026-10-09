# S8 Project Document Ownership Implementation Plan

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
  iteration state only. Source baseline `379667f9780a3e718f41021f8a92a82618a286e2`.
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
Set a private HOME; keep the existing account CODEX_HOME for authentication only,
no credential/config copying or settings/session changes. Disable unnecessary
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
- [ ] Update CHANGELOG/BACKLOG/LOG/CURRENT for S8 only, scope-check again,
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
`/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/openspec-S8-implementation-68h7vzmq/sync`
as S8_SYNC; set S8_PY to `/opt/anaconda3/bin/python3`. No commands below have
applied a runtime change. Create that private directory only when execution is
eligible. Keep the S7 canonical target roots; the current account CODEX_HOME is
an authentication location, not authorization to retarget synchronization.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py plan --manifest references/cross-cli-portable-manifest.json --openspec-source . --brief-source /Users/elvis/file/develop/opensource/codex-brief-antigravity-review --codex-skills-root /Users/elvis/.codex/skills --codex-rule-file /Users/elvis/.codex/AGENTS.md --pi-skills-root /Users/elvis/.pi/agent/skills --pi-rule-file /Users/elvis/.pi/agent/APPEND_SYSTEM.md --antigravity-skills-root /Users/elvis/.gemini/antigravity-cli/skills --antigravity-rule-file /Users/elvis/.gemini/GEMINI.md --grok-skills-root /Users/elvis/.grok/skills --grok-rule-file /Users/elvis/.grok/AGENTS.md --select-file openspec-superpower-change:SKILL.md --select-file openspec-superpower-change:references/project-learning-closeout.md --select-file openspec-superpower-change:templates/learning-candidate-template.md --select-file openspec-superpower-change:scripts/validate_core_gates.py --output "$S8_SYNC/plan.json"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py verify-prestate --plan "$S8_SYNC/plan.json"
```

Expected exit 0: schema 2, four selected files, 36 read-only assertions/target,
unchanged governance v6 and target order. Review the actual plan SHA/pre-state;
inventory known canonical legacy-status roots before apply. Active legacy 4/5
contracts block deployment until the existing drain condition is satisfied.

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

## Readiness Disposition

FULL_PREFLIGHT at Plan SHA d07e7388097c83dbc833278df6972ecffe70a624dacdcf6f15b5937a72904a10
returned BLOCKED; immutable Review:
`docs/review/2026-10-08-S8-preflight-full.json`. This revision fills ordinary
F2/F3 Plan details only; they still require eligible independent verification.
F1 remains: existing S7 resume metadata/validator binds one immutable reviewer
to both stages, while S8 requires distinct stage instances. No permitted Plan
workaround authorizes execution. Preserve the S8 contract and assignments;
the protected prerequisite must be selected, proposed and approved separately.
Do not restart unchanged-contract Preflight, implement S8 or change excluded
S7 evidence rules to hide this conflict.
