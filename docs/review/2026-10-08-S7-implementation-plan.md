# S7 Project Session Resume Implementation Plan

> For agentic workers: use `superpowers:executing-plans` for inline implementation.
> Independent reviewers perform readiness, implementation and final gates only.

**Goal:** Resume unfinished authorized implementation from one verified project
checkpoint without inheriting chat or granting authority.

**Architecture:** A `## Session Resume` JSON fence in the same canonical status
file holds an explicit local schema-6 subset or an external Handoff reference,
plus progress. Existing Handoff APIs and gates remain unchanged. Validation and
read-only recovery use existing core tooling; no writer daemon or new ledger.

**Tech stack:** dependency-free Python/JSON, existing Markdown ownership parser,
unittest, native isolated Codex probes, current cross-CLI transactions.

**Spec:** `openspec/changes/add-project-session-resume/{proposal,design}.md`,
draft-v1 approved 2026-10-08; original artifact digest in CURRENT.

## Global Constraints

- Modify only SKILL, approved-implementation-workflow, direct-change-rule,
  validate_core_gates, test_workflow_rules, CHANGELOG and S7 artifacts/bookkeeping.
- No Handoff reference, companion, manifest, governance text, target, historical
  status, dependency, production or S8 edits. Bound Codex owner alone signs.
- Current source/main is the user-selected workspace; preserve all existing
  unrelated dirty files. No worktree mandate. Git closes this S7 slice only.
- Source baseline `95e6a51c1d6a405e54049262693b5ab95f2f45d7`; temporary source and
  runtime preimages recorded in CURRENT. Runtime rollback uses its transaction.
- Model/reasoning fixed gpt-6.1-sol/high, including independent Codex instances.

## Review Focus

1. Local/external relabeling or marker deletion must fail closed, not downgrade.
2. Changed verified inputs must return a verification action, preserving edits
   and the old checkpoint without asserting current PASS.
3. Wrong identity cannot become the old controller, even with “继续闭环”.
4. Missing/duplicate progress, unsafe paths and conflicting/duplicate changes
   must not be repaired from chat or chosen automatically.
5. Final verification and required Review remain distinct persisted stages;
   external `complete` always retains actual previous-status proof.

## Interfaces And Record

In `scripts/validate_core_gates.py`:

- `extract_resume_record(text: str, label: str) -> dict`: exactly one owned
  heading/fence, duplicate JSON keys rejected.
- `validate_resume_record(text: str, root: Path, *, previous_text: str | None =
  None, actor: dict | None = None) -> dict`: validate references, ownership,
  source fingerprints and transitions; return bounded read-only recovery data.
- `recover_project_session(root: Path, *, change_id: str | None = None,
  actor: dict | None = None) -> dict`: explicit selection or unique unfinished
  record; multiple unfinished records fail with selection required.
- CLI `--resume-status FILE --artifact-root ROOT`, optional `--previous-status`
  and `--resume-actor INSTANCE`. Existing `--status` is mutually exclusive and
  unchanged; actor absence is read-only recovery, never assignment.

Record outer keys: `record_kind`, `governance` (local) OR `contract_revision`
(external), and `progress`. Local governance is the 13-field approved subset.
Progress keys: `goal`, hashed `contract` / nullable hashed `plan`, `completed`
(hashed existing references), `next_action`, nullable `verified_revision`.
Contract is the existing scoped approval/authorization document, not a new one.
`next_action` has `action`, `owner`, `permission`, `inputs` (hashed references);
blocked state uses action `wait` and a nonblank persisted resume condition.
Verified revision has `revision`, `inputs` (path to hash-or-null absence mapping),
`fingerprint` (SHA-256 of sorted compact JSON inputs), `commands` (nonempty actual
command/result/evidence records). JSON nesting needs no YAML parser extension.
The approval/plan document must name the matching change, route/kind and required
verification commands; these facts are read from its explicit scoped metadata,
not inferred from chat. Local phase/complete evidence uses existing verification
and Review records referenced in progress; no external batch artifacts invented.

### Exact context and evidence encoding (F1)

Put one `## Resume Context` JSON fence in the **existing approved contract**,
as a fixed factual summary, never a new approval document or mutable ledger.
Its exact fields: `change_id`, `record_kind`, `mode`, `approval_status`,
`risk_profile`, `control_plane_owner`, `allowed_actions` (action -> permission),
`verification_commands` (nonempty unique strings), `reviewer_assignment`
(existing full six-concept assignment, null only for compact inline Review).
Its existing authorization remains human-owned; this metadata, a CLI flag or
the validator cannot authenticate, create or broaden that authorization.
Missing context fails closed; bare prose “approved” is never inferred as approval.
All governance facts must match this hashed contract context; only approved or
not-required implementation can advance. Proposed/blocked context may be read
only as blocked state with reason/owner/condition and wait action. Local kind
cannot retain an external assignment/artifact/marker; kind and immutable
governance facts cannot change in a previous-status transition.

Verification evidence uses existing field concepts in one JSON result artifact:
`evidence_role: final-verification`, `evidence_result: pass`, `change_id`,
`contract_revision`, `source_fingerprint`, `agent_identity` (existing four-field
owner identity), `commands` (actual command -> exit-code map). Each checkpoint
command record names `command`, `result: pass`, hashed `evidence`; its exact
command must be covered with exit code 0 in the bound artifact. Required command
coverage comes from contract context; all revisions/fingerprints/owner identities
must agree. Tests use synthetic artifacts; acceptance probes capture real process
results before writing them. Validator checks consistency, not execution itself.

Local Review records in `completed` are hashed existing Review JSON artifacts
with `evidence_role: implementation-review | final-review`, `evidence_result`,
`change_id`, `contract_revision`, `source_fingerprint`, `canonical_sha256`,
`agent_identity`, `reviewer_assignment`. Standard/strict assignment must match
context exactly, carry purpose/product/role/capability/independence/authority and
be distinct from controller/executor; compact inline Review uses the bound owner
and null independent assignment under existing applicability. No external Report,
batch fields, evidence schema version, signature or new signoff owner is created.

Local transitions increment revision by one and preserve kind/immutable facts;
pause permits a same-phase checkpoint, complete is terminal. The compact local
ready-for-execution -> awaiting-final-verification path follows its existing
readiness/verification/inline Review; standard/strict also require accepted
implementation Review. Complete requires actual previous canonical bytes in
awaiting-final-verification, required verification persisted at that previous
revision and a separate final Review bound to its SHA/revision/fingerprint.
Atomic pending -> final-verification/final-Review/complete fails. Completed
inventory is read-only, never a new completion signoff or action.
External validation delegates all existing full-Handoff/evidence/previous-status
gates. New refs use single-descriptor, root-bound no-follow bytes; the existing
artifact reader may reuse this secure primitive internally without altering its
API, field set or declared gates. Any required semantic API expansion stops.
`--resume-actor` compares a supplied instance to existing assignment only: it is
an untrusted diagnostic string, not proof that the caller owns that identity.
No CLI writes status. The already-bound controller validates a temporary proposed
record against current canonical bytes and atomically replaces it; a fresh
unassigned native instance stays a read-only observer.

## Review Assignment

Controller/author/executor: Codex instance `s7-control-01`, control-plane-high.
Review product/role/profile: Codex / independent-reviewer / control-plane-high.
Preflight instance `s7-preflight-01`; implementation instance `s7-review-01`;
final instance `s7-final-01`. Each is distinct from controller/executor and from
the other stages. Purpose: inspect actual Plan or complete implementation/final
diff and evidence, decide PASS/FAIL/BLOCKED for that gate. Authority:
governed-review-evidence only; no writes, assignment, approval or completion.
Tool instance IDs will be bound in the corresponding Review record.

## Task 1: Checkpoint And Recovery

- [ ] Add `ProjectSessionResumeTests` to existing test_workflow_rules; assert
  missing runtime API gives RED, then exercise local/external positives and
  the five review-focus mechanisms using temporary real files.
- [ ] Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
  -p test_workflow_rules.py -k ProjectSessionResumeTests -v`; preserve RED result.
- [ ] Implement the listed interfaces, secure single-read regular-file binding,
  unchanged full-Handoff dispatch and explicit CLI. Keep local transitions
  distinct from external validation without weakening either's existing gates.
- [ ] Centralize actual field examples and pause/resume instructions in approved
  implementation reference; add only necessary navigation to SKILL/Direct Change.
- [ ] Run focused suite to GREEN in both parser modes, then existing full suite,
  quick/core, strict OpenSpec and independent implementation Review.

## Task 2: Real Forward Proof And Closure

- [ ] In an isolated project, native fresh Codex without old chat restores the
  persisted next action as a read-only observer; audit events and actual file
  readouts. Baseline validator's missing resume interface must produce RED;
  changed validator plus persisted actual verification must produce GREEN.
- [ ] Strict probe covers stale input and wrong authority/multiple unfinished
  work; no new runner/fixture system, raw logs transient and results sanitized.
- [ ] Review a scoped four-file portable plan and destination pre-state; apply,
  validate, discover and verify-all Codex/Pi/Antigravity/Grok using existing tools.
- [ ] Read existing engineering invariants and learning closeout after findings;
  promote only qualifying project-local learning within approved boundaries.
- [ ] Fresh source/runtime verification, independent final Review, OpenSpec
  task reconciliation and applicable archive validation; reconcile iteration
  state, scoped Git commit/push, then owned backup/trace cleanup.

Stop for forbidden-file need, scope/compatibility/acceptance expansion, invalid
approval, stale/failed evidence, unsupported native probe, unsafe sync pre-state
or missing authority. Same-scope findings return to fix/verify/the same gate.

Plan self-check: every S7 requirement maps to Task 1 or 2; all five Review Focus
items have focused tests, planned native mechanisms and exact gate commands.

## Native proof mechanism (F3)

Use a temporary standard-library script under CURRENT.backup, not a new repo
runner. For baseline/current, copy the selected Skill snapshot to an isolated
fixture outside discovery. Create a synthetic Direct Change project with app,
unit test, approved contract context, canonical status and captured real command
result artifacts. Parent known fixture owner persists a checkpoint after real
verification, validates temporary proposed bytes against the canonical record,
then atomically replaces it; test actual on-disk revision/action/fingerprint.
No business repository or installed Skill is a test fixture.

Native command: `codex exec --json --ephemeral --ignore-user-config --ignore-rules
--model gpt-6.1-sol -c 'model_reasoning_effort="high"' --sandbox read-only
--skip-git-repo-check -C <private-project> --output-schema <private-schema>
--output-last-message <private-result> <synthetic-resume-request>`.
Private HOME; authenticated account CODEX_HOME only for native authentication,
no credential copying/config edits/session writes. Fixture instructions grant
read-only observation and exact validator/test commands; the new child has no
controller mutation or signing assignment and does not impersonate the old owner.

Audit complete JSONL fail-closed: only known thread/turn lifecycle, agent_message,
reasoning and command_execution events. Command events must be exactly the
fixture validator or focused unit verification command; reject other tools,
shell fallbacks, unknown events and incomplete execution. The old no-tool routing
auditor is not reused for this command-bearing proof. Require actual validator
exit/result plus unchanged fixture file hashes for native read-only cases.
Strict case rejects stale fingerprint/wrong identity without altering source or
owner. No claim of native persistence, zero tools, production or whole-task PASS;
parent persistence plus native recovery form the separate real mechanisms.
Timeout 120 seconds/case; raw events/result/stderr private 0600 and transient.
Persist only command templates, synthetic inputs, counts/hashes and bounded
results under `docs/iteration/evidence/S7-project-session-resume.json`.

## Exact checks and transaction templates (F2, F4)

`S7_BACKUP` is the recorded CURRENT private backup; `S7_PY` is its
`validation-venv/bin/python` with PyYAML 6.0.3. Default `python3` is fallback.
`S7_PLAN=$S7_BACKUP/sync/plan.json`, receipts are `$S7_BACKUP/sync/<target>.json`.
Execute commands separately, capture outputs and require exit 0:

```bash
"$S7_PY" "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" .
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .
PYTHONDONTWRITEBYTECODE=1 "$S7_PY" scripts/validate_core_gates.py .
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 "$S7_PY" -m unittest discover -s tests -v
OPENSPEC_TELEMETRY=0 openspec validate add-project-session-resume --strict --no-interactive
git diff --check
```

Sync plan uses `python3 scripts/validate_cross_cli_sync.py plan` with
`--manifest references/cross-cli-portable-manifest.json --openspec-source "$PWD"
--brief-source "$PWD/../codex-brief-antigravity-review"` and these exact roots:
Codex `$HOME/.codex/skills`, rule `$HOME/.codex/AGENTS.md`; Pi
`$HOME/.pi/agent/skills`, rule `$HOME/.pi/agent/APPEND_SYSTEM.md`; Antigravity
`$HOME/.gemini/antigravity-cli/skills`, rule `$HOME/.gemini/GEMINI.md`; Grok
`$HOME/.grok/skills`, rule `$HOME/.grok/AGENTS.md`, using
`--codex-skills-root/--codex-rule-file`, `--pi-skills-root/--pi-rule-file`,
`--antigravity-skills-root/--antigravity-rule-file`,
`--grok-skills-root/--grok-rule-file` respectively. Select exactly
`openspec-superpower-change:SKILL.md`, `:references/approved-implementation-workflow.md`,
`:references/direct-change-rule.md`, `:scripts/validate_core_gates.py` via four
repeatable `--select-file` flags, output `--output "$S7_PLAN"`. No managed-rule
selector. Review hashes/pre-state and all 36 read-only assertions before apply.

For each target in codex/pi/antigravity-cli/grok-cli order, commands use prefix
`PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py`:

```text
apply --target <target> --plan <S7_PLAN> --transaction-receipt <receipt> --backup-root <S7_BACKUP/sync/backups>
verify --target <target> --plan <S7_PLAN> --transaction-receipt <receipt>
verify-discovery --target <target> --plan <S7_PLAN> --transaction-receipt <receipt>
commit-target --target <target> --plan <S7_PLAN> --transaction-receipt <receipt>
verify-all --plan <S7_PLAN> --transaction-root <S7_BACKUP/sync>
```

Before commit-target run each target Skill's quick_validate, core-gate and
companion validate_templates with both interpreters. Grok discovery additionally
uses `grok inspect --json` captured to private 0600 `<inspect-json>` (never echoed),
then `verify-discovery ... --inspect-json <inspect-json> --consume`; validate its
configured root against the same-plan prior receipt. Pi process is not invoked.
Re-inventory known canonical legacy status roots immediately before first apply.
On a failure: `restore-target --target <target> --plan <S7_PLAN> --backup-root
<S7_BACKUP/sync/backups> --transaction-receipt <receipt>`, then
`verify-prestate --target <target> --plan <S7_PLAN>`; preserve blocked evidence.
Already committed targets use a newly reviewed reverse scoped plan against the
restored canonical source, never a stale transaction or manual runtime copy.

After sync and any learning correction, rerun relevant fresh source gates and
verify-all before final Review. Reconcile tasks and archive only if allowed:
this tooling change may use `openspec archive add-project-session-resume --yes
--skip-specs` to preserve forbidden, preexisting dirty main specs; record skipped
spec merge explicitly. Run strict validation of the resulting
`archive/<date>-add-project-session-resume` change with `--type change`; if CLI
cannot validate it directly, strict-validate its exact bytes in a private isolated
OpenSpec fixture. Never run --all or rewrite unrelated archived/main specs.

Negative scope check: compare `git status --short` and hashes to structured
backup, allowing only listed S7 paths; verify Handoff, companion, manifest,
managed rule and unrelated files unchanged. Persist actual commands/results,
not raw private traces. Source rollback restores only backed-up S7 preimages and
removes only this round's new files; no reset/clean or user-change deletion.
