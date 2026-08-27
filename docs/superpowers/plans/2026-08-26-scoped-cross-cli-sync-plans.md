# Scope-Bound Cross-CLI Sync Implementation Plan

> **For Luna Max:** use `executing-plans`, `test-driven-development`,
> `systematic-debugging`, `writing-skills`, `requesting-code-review`, and
> `verification-before-completion`. `requesting-code-review` invokes only the
> checkpoint Review named here. Active OpenSpec `tasks.md` is canonical
> progress; Plan checkboxes are static steps.

**Goal:** Add explicit scope-bound plans to the existing cross-CLI validator,
unblock the predecessor's exact two-file runtime sync, then synchronize the
scoped mechanism's exact three portable files.

**Architecture:** Keep one planner and durable receipt/backup/recovery flow.
No-selector plans remain schema v1/full-manifest. Explicit selectors emit
sync-plan schema v2: selected `files` mutate, unselected `assertions` prove
parity/prestate without mutation, and `managed_rule.selected` controls rule
mutation. Build/review in a private candidate tree, close/archive predecessor,
then promote canonical source.

## Gate and agent assignments

Change-id: `add-scoped-cross-cli-sync-plans`.

Current authority covers proposal/Plan only. Stop before candidate creation,
RED, implementation, runtime plan/apply, or archive until:

1. strict OpenSpec and fresh Plan Preflight PASS;
2. user explicitly approves this exact change-id, four canonical files, Batch-A
   two-file runtime set, Batch-B three-file runtime set, and dynamic archives;
3. bound Codex control-plane accepts approval and records it in proposal/tasks.

Execution is **direct inline Pi work**, not external dispatch:

- product/model/reasoning: Pi / `openai-codex/gpt-5.6-luna` / exactly `max`;
- role/profile: `executor` / `cohesive-medium`;
- instance: fresh inline Luna instance distinct from author and reviewers;
- authority: approved edits/tests/runtime commands only; no evidence acceptance,
  Git, archive, scope, or Completion authority.

No Handoff, Brief, Report, Confirmation Lease, or second ledger is created. If
execution moves to an external agent/new-window Handoff, this Plan is invalid;
return `BLOCKED` and create a separate schema-6 Plan.

Every checkpoint Review resolves:

- non-blank purpose named in that checkpoint;
- product/model/reasoning: Codex / `openai-codex/gpt-5.6-sol` / `max`;
- role/profile: `independent-reviewer` / `control-plane-high`;
- fresh instance distinct from Luna, author, control plane, and prior reviewers;
- result authority: `governed-review-evidence` only.

Only bound Codex control-plane/control-plane-high accepts evidence, updates
canonical task evidence anchors, authorizes runtime/archive, and decides
Completion.

## Allowed closure after approval

Canonical source:

```text
scripts/validate_cross_cli_sync.py
tests/test_cross_cli_sync.py
references/cross-cli-sync.md
references/sync-checklist.md
openspec/changes/add-scoped-cross-cli-sync-plans/**
docs/superpowers/plans/2026-08-26-scoped-cross-cli-sync-plans.md
docs/review/<UTC-date>-add-scoped-cross-cli-sync-plans-<purpose>-a<attempt>.md
```

The OpenSpec evidence subdirectory may contain only attempt-specific immutable
mode-`0600` launch authorizations/guards. Review artifacts are never overwritten.
Control-plane, not Luna, writes launch authorization and canonical evidence
anchors.

Predecessor closeout may update its existing tasks/Plan, dynamically archive its
exact active tree, and update only
`openspec/specs/skill-workflow-governance/spec.md` as allowed by OpenSpec.
This change's closeout has the same dynamic archive/spec allowance.

Runtime Batch A operations per target:

```text
openspec-superpower-change/SKILL.md
openspec-superpower-change/references/approved-implementation-workflow.md
```

Runtime Batch B operations per target:

```text
openspec-superpower-change/scripts/validate_cross_cli_sync.py
openspec-superpower-change/references/cross-cli-sync.md
openspec-superpower-change/references/sync-checklist.md
```

Managed rule is unselected. Companion files, unchanged Router files,
credentials/auth/tokens/sessions/history/logs/caches/model settings/hooks/MCP/
binaries/CLI-native bytes are excluded.

No Git staging, commit, branch/worktree creation, merge, reset, clean, push,
publication, or unowned deletion.

## Fixed base values

Every shell block re-declares values; prior shell state is not trusted:

```bash
set -euo pipefail
umask 077
ROOT=/Users/elvis/file/develop/opensource/openspec-superpower-change
BRIEF_SOURCE=/Users/elvis/file/develop/opensource/codex-brief-antigravity-review
CHANGE=add-scoped-cross-cli-sync-plans
TASKS="$ROOT/openspec/changes/$CHANGE/tasks.md"
PY=/opt/homebrew/bin/python3
PY_REAL=/opt/homebrew/Cellar/python@3.14/3.14.2_1/Frameworks/Python.framework/Versions/3.14/bin/python3.14
PY_REAL_SHA=00c07e4d31048b15eebbe4c883f229338c5b2d598e9ee061da39b7fccba20cad
PY_YAML=/opt/anaconda3/bin/python3
QUICK_VALIDATE=/Users/elvis/.codex/skills/.system/skill-creator/scripts/quick_validate.py
test "$(realpath "$PY")" = "$PY_REAL"
test "$(shasum -a 256 "$PY_REAL" | awk '{print $1}')" = "$PY_REAL_SHA"
test "$($PY --version 2>&1)" = 'Python 3.14.2'
test "$($PY_YAML --version 2>&1)" = 'Python 3.11.7'
```

Interpreter/path/hash drift requires Plan revision and fresh Preflight.

## Deterministic attempt paths

Each Review checkpoint starts attempt 1. On actionable finding, control-plane
records `needs-fix` in the existing task, increments that checkpoint attempt by
exactly one, and preserves every prior artifact. No overwrite or ad-hoc suffix.

```text
/private/tmp/add-scoped-cross-cli-sync-plans-20260826/<checkpoint>/a<attempt>/
docs/review/<UTC-date>-add-scoped-cross-cli-sync-plans-<purpose>-a<attempt>.md
openspec/changes/add-scoped-cross-cli-sync-plans/evidence/
  batch-a-launch-authorization-a<attempt>.json
  run-authorized-candidate-a<attempt>.py
```

Attempt numbers are artifact naming only, not another task state. Active
`tasks.md` records the current accepted attempt and exact evidence SHA. Gaps,
duplicates, occupied new paths, or missing prior evidence are `BLOCKED`.
Runtime failure never auto-increments or retries; recovery stops for a new
control-plane decision and fresh Sync-plan Review.

---

## Task 1: Approval and fresh prestate

- [ ] Record exact user approval; first Pending becomes Task 2.1.
- [ ] Start fresh inline Pi/Luna Max and re-read AGENTS, SKILL, Self-Evolution,
  sync/Handoff authority references, both changes, and this Plan.
- [ ] Confirm `main`, HEAD
  `c1448d60744884f23054aa0e57608f99190aee9f`, expected existing dirty closure,
  predecessor `BLOCKED_TARGETED_TOOLING`, and no unrelated status.
- [ ] Create fresh structured backup attempt 1 outside discovery roots, mode
  `0700`; copy exactly four canonical preimages. Mode-`0600` manifest binds
  path/SHA/mode, HEAD, NUL-safe status, approval, Plan, and tasks SHA.

Review-draft backup
`/private/tmp/openspec-scoped-sync-plan-draft-20260826Tl1T65Y` is evidence only,
not implementation rollback.

```bash
openspec validate "$CHANGE" --strict --no-interactive
git -C "$ROOT" diff --check
test ! -e "$ROOT/.harness"
test ! -e "$ROOT/.agent/goal.md"
```

## Task 2: Baseline, candidate, and RED

Set checkpoint attempt from canonical tasks, initially `ATTEMPT=1`:

```bash
BASE=/private/tmp/add-scoped-cross-cli-sync-plans-20260826/candidate/a$ATTEMPT
BASELINE="$BASE/baseline"
CANDIDATE="$BASE/candidate"
EVIDENCE="$BASE/evidence"
for p in "$BASELINE" "$CANDIDATE" "$EVIDENCE"; do test ! -e "$p"; done
mkdir -p -m 700 "$BASELINE" "$CANDIDATE" "$EVIDENCE"
```

Generated caches are **read-only excluded**, never blockers and never deleted.
Before copy, write their relative paths/SHA/modes to
`$EVIDENCE/excluded-caches.json` mode `0600`. Exclusion is exactly every
`__pycache__` directory, `*.pyc`, and `.pytest_cache`; reject source symlinks
outside `.git`. Copy repository twice excluding `.git` and those cache patterns.
Record complete file/type/mode/SHA inventories; baseline and candidate initially
match. Later candidate delta must be exactly:

```text
scripts/validate_cross_cli_sync.py
tests/test_cross_cli_sync.py
references/cross-cli-sync.md
references/sync-checklist.md
```

No cache cleanup authorization exists.

Add RED classes:

```text
ScopedPlanSelectionTests
ScopedPlanTamperTests
ScopedTransactionTests
```

Required RED:

1. two selectors produce v2/two operations each target;
2. all other files assertions; rule unselected;
3. only explicit rule selector creates rule candidate;
4. duplicate/malformed/unknown/unsafe/sensitive/target-incomplete/non-v6
   selectors fail before output;
5. selection/partition/destination/hash/prestate/rule tampering fails;
6. selected prestate drift blocks before backup/receipt;
7. assertion/rule drift blocks and is byte-identical;
8. scoped round trip mutates selected only; full closure verifies/discovers;
9. restore/recover includes selected only and blocks later targets;
10. no-selector v1 and existing crash/recovery remain green.

```bash
cd "$CANDIDATE"
PYTHONDONTWRITEBYTECODE=1 "$PY" -m unittest \
  tests.test_cross_cli_sync.ScopedPlanSelectionTests \
  tests.test_cross_cli_sync.ScopedPlanTamperTests \
  tests.test_cross_cli_sync.ScopedTransactionTests -v \
  >"$EVIDENCE/red.stdout" 2>"$EVIDENCE/red.stderr"
```

Capture exit separately mode `0600`; require failures only from missing scoped
behavior.

## Task 3: Exact v2 implementation

Add repeatable `plan --select-file SKILL:PATH` and boolean
`--select-managed-rule`. No selector keeps v1 exact behavior.

Portable manifest remains `schema_version == 1`. Scoped eligibility means
`managed_rules.version == 6`, manifest targets and every selected entry target
exactly `codex,pi,antigravity-cli,grok-cli` in order.

V2 top-level exact keys:

```text
schema_version, manifest_path, manifest_sha256, sources, selection,
managed_rules, targets
```

`selection` exact:

```json
{"files":[{"skill":"openspec-superpower-change","path":"SKILL.md"}],"managed_rule":false}
```

Each target: manifest target-state fields plus exactly
`skills_root,files,assertions,managed_rule`; omit v1
`rule_file/rule_pre_state`. File/assertion records exact keys:

```text
skill, source_alias, path, sha256, destination, pre_state
```

Target managed rule exact keys: `selected,destination,pre_state`. Top-level
managed rule keeps v1 keys `version,source_alias,path,sha256,invariant_ids`.

Rules:

- at least one selected file/rule operation;
- selectors normalized in manifest order and duplicate/unknown/unsafe/
  sensitive/target-incomplete rejected;
- `files` equals selection; `assertions` is every unselected entry exactly once;
- lists preserve relative manifest order and partition full manifest;
- target/top-level rule selection equal;
- generation requires all assertions/unselected rule already parity;
- `_validate_plan` dispatches exact v1/v2 validation and rebinds source,
  destination, and prestate;
- operation helper: v1/v2 `files`;
- verification helper: v1 `files`, v2 `files + assertions`;
- rule helper: v1 selected, v2 conditional;
- prestate helper: full verification closure plus rule;
- thread helpers through `_target_candidate_entries`, `_target_records`,
  `_assert_target_prestate`, `_legacy_apply_target_without_receipt`,
  `verify_target`, `_current_target_digest`;
- backup/candidate/restore/recovery use operations only;
- verify/discovery/digest/commit/verify-all use full closure;
- no dependency, manifest, routing, state, second script, or transaction flow.

Update only two declared references. Run/capture GREEN and full checks:

```bash
cd "$CANDIDATE"
PYTHONDONTWRITEBYTECODE=1 "$PY" -m unittest \
  tests.test_cross_cli_sync.ScopedPlanSelectionTests \
  tests.test_cross_cli_sync.ScopedPlanTamperTests \
  tests.test_cross_cli_sync.ScopedTransactionTests -v
PYTHONDONTWRITEBYTECODE=1 "$PY" -m unittest tests.test_cross_cli_sync -v
"$PY_YAML" "$QUICK_VALIDATE" .
PYTHONDONTWRITEBYTECODE=1 "$PY" scripts/validate_core_gates.py .
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/validate_core_gates.py .
PYTHONDONTWRITEBYTECODE=1 "$PY" -m unittest discover -s tests -v
openspec validate "$CHANGE" --strict --no-interactive
```

Each command has separate mode-`0600` stdout/stderr/exit evidence.

## Task 4: Candidate Source Review

Mechanically inventory candidate; reject symlink/cache and any delta outside
four files. Create immutable mode-`0600` bundle containing all file hashes/modes,
exact changed pre/post hashes, script SHA, RED/GREEN/full evidence hashes,
backup/Plan/tasks hashes.

Review purpose: decide candidate source correctness/security before using
unversioned bootstrap bytes. Fresh Codex/Sol max independent reviewer inspects
actual files/complete diff and probes selector normalization, partition/rule
tampering, assertion drift, assertion backup/restore leakage, v1 regression,
unsafe paths, and recovery. Persist attempt-specific `docs/review/...candidate-
source-aN.md`; control-plane records path/SHA in Task 2.5.

Finding: preserve attempt, increment exactly one, copy prior candidate to fresh
attempt, fix/verify/review; regenerate bundle. PASS does not authorize runtime.

## Shared legacy drain

Authoritative roots:

```text
$ROOT
$BRIEF_SOURCE
/Users/elvis/file/develop/workspace/ai-app/ai_app
/Users/elvis/file/develop/workspace/python/gitlabnew-python/qagent/qagent_service
/Users/elvis/file/develop/workspace/java/gitlabnew-jdk21/llm-workflow-service
/Users/elvis/file/develop/opensource/openharness
```

`qagentOldSanBox` is noncanonical. A newly known canonical root invalidates the
Review. Before each Sync-plan Review and again immediately before first apply,
write a different absent output:

```bash
OUT="$RUN_ROOT/legacy-$STAGE.json"
test ! -e "$OUT"
PYTHONDONTWRITEBYTECODE=1 "$PY" "$ROOT/scripts/validate_core_gates.py" "$ROOT" \
  --legacy-inventory-root "$ROOT" \
  --legacy-inventory-root "$BRIEF_SOURCE" \
  --legacy-inventory-root /Users/elvis/file/develop/workspace/ai-app/ai_app \
  --legacy-inventory-root /Users/elvis/file/develop/workspace/python/gitlabnew-python/qagent/qagent_service \
  --legacy-inventory-root /Users/elvis/file/develop/workspace/java/gitlabnew-jdk21/llm-workflow-service \
  --legacy-inventory-root /Users/elvis/file/develop/opensource/openharness \
  --legacy-inventory-output "$OUT" >"$OUT.stdout" 2>"$OUT.stderr"
test "$(stat -f %Lp "$OUT")" = 600
"$PY" - "$OUT" <<'PY'
import json,sys
from pathlib import Path
v=json.loads(Path(sys.argv[1]).read_text())
assert v['legacy_audit']=='pass' and v['active_legacy_count']==0
assert all(r['drain_status']=='complete-history' for r in v['records'])
PY
```

Use `STAGE=before-plan-review` and `before-first-apply`; hash all outputs. Draft
PASS evidence is
`/private/tmp/scoped-sync-plan-draft-legacy-audit-20260826-r1.json`, SHA
`cc1355940bbcaabff01bc242d8dcee62998f9570ca26421b192cdfd6c3a77983`,
but never replaces execution audits.

## Task 5: Batch-A plan, Review, and trusted launch anchor

Plan attempt root:

```bash
PLAN_ATTEMPT=1 # or exact next attempt recorded by control-plane after finding
RUN_ROOT=/private/tmp/add-scoped-cross-cli-sync-plans-20260826/batch-a-plan/a$PLAN_ATTEMPT
PLAN="$RUN_ROOT/plan.json"
test ! -e "$RUN_ROOT"; mkdir -m 700 -p "$RUN_ROOT"
```

Before launch authorization exists, Luna may invoke candidate **only for
read-only plan generation** through the fixed real interpreter and candidate
hash from accepted Source Review:

```bash
PYTHONDONTWRITEBYTECODE=1 "$PY_REAL" -I -S \
  "$CANDIDATE/scripts/validate_cross_cli_sync.py" plan \
  --manifest "$ROOT/references/cross-cli-portable-manifest.json" \
  --openspec-source "$ROOT" --brief-source "$BRIEF_SOURCE" \
  --select-file openspec-superpower-change:SKILL.md \
  --select-file openspec-superpower-change:references/approved-implementation-workflow.md \
  --codex-skills-root /Users/elvis/.codex/skills --codex-rule-file /Users/elvis/.codex/AGENTS.md \
  --pi-skills-root /Users/elvis/.pi/agent/skills --pi-rule-file /Users/elvis/.pi/agent/APPEND_SYSTEM.md \
  --antigravity-skills-root /Users/elvis/.gemini/antigravity-cli/skills --antigravity-rule-file /Users/elvis/.gemini/GEMINI.md \
  --grok-skills-root /Users/elvis/.grok/skills --grok-rule-file /Users/elvis/.grok/AGENTS.md \
  --output "$PLAN"
PYTHONDONTWRITEBYTECODE=1 "$PY_REAL" -I -S \
  "$CANDIDATE/scripts/validate_cross_cli_sync.py" verify-prestate --target all --plan "$PLAN"
```

Before each command, independently recompute candidate bundle/script/interpreter
hashes from Task 4 evidence. Require v2; exact two operations/37 assertions per
target; rule false; plan mode 0600; full parity/prestate; no runtime root. Run
legacy `before-plan-review`.

Review purpose: pre-apply Batch-A Sync-plan safety. Fresh Codex/Sol max reviewer
binds Plan/candidate/source/manifest/destination/prestate/legacy hashes and
requires exact two operations, no rule/Companion/assertion candidate. Finding
creates next plan attempt root; never overwrite.

After PASS, **control-plane** creates these new immutable mode-`0600` files:

```text
openspec/changes/add-scoped-cross-cli-sync-plans/evidence/
  run-authorized-candidate-a<attempt>.py
  batch-a-launch-authorization-a<attempt>.json
```

Launch authorization exact fields:

```text
schema_version, purpose, root, implementation_plan_path,
implementation_plan_sha256, sync_plan_path, sync_plan_sha256,
plan_review_path, plan_review_sha256, source_review_path, source_review_sha256,
candidate_root, candidate_bundle_path, candidate_bundle_sha256,
candidate_script_path, candidate_script_sha256, candidate_inventory_sha256,
guard_path, guard_sha256, interpreter_path, interpreter_sha256,
operation_set, target_order, managed_rule_selected
```

It binds current Plan SHA, accepted Source/Sync-plan Reviews, candidate complete
inventory, fixed interpreter, exact two operations, target order, and rule
false. Control-plane records exactly one line in active tasks:

```text
Batch-A launch authorization a<attempt> SHA-256: <64 lowercase hex>
```

The guard reads that line, requires exactly one match, verifies authorization
SHA, its own SHA, Plan/Reviews/bundle/candidate complete inventory/script/
interpreter/selected plan hashes and fields, then executes only:

```text
<interpreter> -I -S <candidate-script> <supplied sync args>
```

with minimal fixed environment and `PYTHONDONTWRITEBYTECODE=1`. Authorization is
external to candidate; bundle+guard substitution cannot preserve the
canonical tasks anchor. Every candidate runtime invocation uses guard; direct
candidate runtime commands are forbidden after anchor creation.

## Exact captured recovery helpers

Before runtime, define evidence root mode `0700`. Every command writes separate
mode-`0600` stdout/stderr/exit. No `|| true`; use the exact `capture` helper in
Appendix B, which records nonzero status without toggling the caller's
`errexit` state.

For `restore-target`, require exit 0 and exact safe fields:

```text
restore=pass, target=<current>, restored=true, later_targets_started=false
```

For `recover-pending`, current CLI intentionally exits 1 on both safe recovery
and blocked recovery. Require exit **1**, parse stdout JSON, and classify:

- safe recovery only if `recovery=pass`, expected target, `restored=true`,
  `later_targets_started=false`;
- otherwise `recovery=blocked`/unresolved; preserve manual-disposition evidence.

Either result stops the batch and later targets. Never infer from exit alone.
Parser command, parsed fields, receipt/backup/plan hashes are evidence.

## Task 6: Batch-A runtime and predecessor post-archive final gate

Runtime root is derived from accepted plan attempt and must be absent:

```bash
RUNTIME_ROOT=/private/tmp/add-scoped-cross-cli-sync-plans-20260826/batch-a-runtime/a$PLAN_ATTEMPT
BACKUPS="$RUNTIME_ROOT/backups"; TX="$RUNTIME_ROOT/transactions"
RUNTIME_EVIDENCE="$RUNTIME_ROOT/evidence"
mkdir -p -m 700 "$BACKUPS" "$TX" "$RUNTIME_EVIDENCE"
```

Before first apply: trusted guard PASS; authorization/tasks/Plan/reviews/source/
destination unchanged; fresh legacy `before-first-apply`; guarded
`verify-prestate --target all`; no receipt/backup object.

For each target in fixed order `codex,pi,antigravity-cli,grok-cli`:

1. guarded `apply`;
2. guarded `verify`;
3. runtime Router quick/core and Companion quick/template validators;
4. guarded deterministic `verify-discovery` (never launch Pi);
5. Grok only: fresh mode-0600 `/Users/elvis/.grok/bin/grok inspect --json`,
   never echo, pass `--consume`;
6. guarded `commit-target`.

Skill roots:

```text
codex=/Users/elvis/.codex/skills
pi=/Users/elvis/.pi/agent/skills
antigravity-cli=/Users/elvis/.gemini/antigravity-cli/skills
grok-cli=/Users/elvis/.grok/skills
```

Apply interruption/uncertainty uses captured `recover-pending` parser above.
Post-apply verify/validator/discovery failure uses captured `restore-target`
parser. Commit uncertainty uses captured `recover-pending`. Any failure stops;
no next target/retry/manual copy. After four commits, guarded `verify-all` and
fresh runtime Review purpose “Batch-A exact runtime parity/receipt/discovery and
rollback boundary” through fresh Codex/Sol.

Then, before canonical tool promotion:

1. predecessor Project Learning Closeout;
2. reconcile predecessor tasks;
3. compute `ARCHIVE_DATE=$(date -u +%F)`, require collision-free exact archive
   destination, archive, verify unique actual destination and allowed canonical
   spec update;
4. strict post-archive validation;
5. fresh predecessor **post-archive** final verification;
6. fresh Codex/Sol final Review purpose “predecessor post-archive complete diff,
   source/runtime parity, learning, archive, and Completion evidence”;
7. bound control-plane accepts Completion.

Archive is before final verification/Review. No stale pre-archive Review
satisfies Completion.

## Task 7: Canonical promotion and Source Review

Only after predecessor Completion: verify accepted candidate/backup hashes,
current branch/HEAD/status, and archive. Atomically replace exactly four
canonical files with accepted candidate bytes/modes. Require canonical hashes
equal bundle. Copy no cache/evidence/OpenSpec/candidate-only file.

Run all Task 3 checks against ROOT, strict all OpenSpec, diff/status. Review
purpose: canonical v1/v2 source correctness and complete production wiring.
Fresh Codex/Sol max reviewer inspects actual files/complete diff and repeats
adversarial partition, assertion, receipt/recovery, and legacy probes. Finding
creates deterministic next candidate/canonical Review attempt; no runtime Plan
exists until PASS.

## Task 8: Batch-B plan and runtime

Plan attempt root is deterministic and exclusive. Generate with canonical tool
and complete standard roots/arguments from Task 5, selectors exactly:

```text
scripts/validate_cross_cli_sync.py
references/cross-cli-sync.md
references/sync-checklist.md
```

No `--select-managed-rule`. Require v2, exactly three operations, all other
entries asserted, rule false, full parity/prestate. Run legacy before-plan.
Fresh Codex/Sol Review purpose: Batch-B exact three-file pre-apply Sync-plan.
Finding creates next plan attempt.

No candidate guard is needed; canonical script/Plan/Review hashes are rechecked
immediately before apply. Run fresh legacy before-first-apply and prestate.
Execute same captured per-target matrix and recovery parsing with canonical
script, then verify-all and fresh runtime Review purpose “Batch-B all-target
parity, discovery, receipts, and unselected-byte preservation”.

## Appendix A: Exact Batch-B plan command

```bash
PYTHONDONTWRITEBYTECODE=1 "$PY_REAL" -I -S \
  "$ROOT/scripts/validate_cross_cli_sync.py" plan \
  --manifest "$ROOT/references/cross-cli-portable-manifest.json" \
  --openspec-source "$ROOT" --brief-source "$BRIEF_SOURCE" \
  --select-file openspec-superpower-change:scripts/validate_cross_cli_sync.py \
  --select-file openspec-superpower-change:references/cross-cli-sync.md \
  --select-file openspec-superpower-change:references/sync-checklist.md \
  --codex-skills-root /Users/elvis/.codex/skills --codex-rule-file /Users/elvis/.codex/AGENTS.md \
  --pi-skills-root /Users/elvis/.pi/agent/skills --pi-rule-file /Users/elvis/.pi/agent/APPEND_SYSTEM.md \
  --antigravity-skills-root /Users/elvis/.gemini/antigravity-cli/skills --antigravity-rule-file /Users/elvis/.gemini/GEMINI.md \
  --grok-skills-root /Users/elvis/.grok/skills --grok-rule-file /Users/elvis/.grok/AGENTS.md \
  --output "$PLAN"
PYTHONDONTWRITEBYTECODE=1 "$PY_REAL" -I -S \
  "$ROOT/scripts/validate_cross_cli_sync.py" verify-prestate --target all --plan "$PLAN"
```

## Appendix B: Exact captured target matrix

Before use set reviewed `RUN_ROOT`, `PLAN`, `BACKUPS`, `TX`, and
`RUNTIME_EVIDENCE`. For Batch A:

```bash
INVOKE=("$PY_REAL" -I -S "$GUARD" --)
```

For Batch B:

```bash
INVOKE=("$PY_REAL" -I -S "$ROOT/scripts/validate_cross_cli_sync.py")
```

Use these exact helpers:

```bash
capture() {
  label=$1; shift
  rc=0
  "$@" >"$RUNTIME_EVIDENCE/$label.stdout" \
    2>"$RUNTIME_EVIDENCE/$label.stderr" || rc=$?
  printf '%s\n' "$rc" >"$RUNTIME_EVIDENCE/$label.exit"
  chmod 600 "$RUNTIME_EVIDENCE/$label."{stdout,stderr,exit}
  return "$rc"
}
parse_recovery() {
  mode=$1; target=$2; label=$3
  "$PY_REAL" -I -S - "$mode" "$target" \
    "$RUNTIME_EVIDENCE/$label.stdout" "$RUNTIME_EVIDENCE/$label.exit" <<'PY'
import json,sys
from pathlib import Path
mode,target,out,exit_path=sys.argv[1:]
value=json.loads(Path(out).read_text())
rc=int(Path(exit_path).read_text())
if mode=='restore':
    assert rc==0 and value=={
        'restore':'pass','target':target,'restored':True,
        'later_targets_started':False,
    }
else:
    assert rc==1
    assert value=={
        'recovery':'pass','target':target,'restored':True,
        'later_targets_started':False,
    }
PY
}
restore_and_stop() {
  target=$1; label=$2; receipt="$TX/$target.json"
  capture "$label-restore" "${INVOKE[@]}" restore-target \
    --target "$target" --plan "$PLAN" --backup-root "$BACKUPS" \
    --transaction-receipt "$receipt" || return 91
  parse_recovery restore "$target" "$label-restore" || return 92
  return 90
}
recover_and_stop() {
  target=$1; label=$2; rc=0
  capture "$label-recover" "${INVOKE[@]}" recover-pending \
    --plan "$PLAN" --backup-root "$BACKUPS" --transaction-root "$TX" || rc=$?
  test "$rc" = 1 || return 93
  parse_recovery recover "$target" "$label-recover" || return 94
  return 90
}
run_target() {
  target=$1; skills=$2; receipt="$TX/$target.json"
  test ! -e "$receipt"
  capture "$target-apply" "${INVOKE[@]}" apply --target "$target" \
    --plan "$PLAN" --backup-root "$BACKUPS" \
    --transaction-receipt "$receipt" || recover_and_stop "$target" "$target-apply"
  capture "$target-verify" "${INVOKE[@]}" verify --target "$target" \
    --plan "$PLAN" --transaction-receipt "$receipt" \
    || restore_and_stop "$target" "$target-verify"
  capture "$target-router-quick" "$PY_YAML" "$QUICK_VALIDATE" \
    "$skills/openspec-superpower-change" \
    || restore_and_stop "$target" "$target-router-quick"
  capture "$target-router-core" env PYTHONDONTWRITEBYTECODE=1 "$PY" \
    "$skills/openspec-superpower-change/scripts/validate_core_gates.py" \
    "$skills/openspec-superpower-change" \
    || restore_and_stop "$target" "$target-router-core"
  capture "$target-brief-quick" "$PY_YAML" "$QUICK_VALIDATE" \
    "$skills/codex-brief-antigravity-review" \
    || restore_and_stop "$target" "$target-brief-quick"
  capture "$target-brief-core" env PYTHONDONTWRITEBYTECODE=1 "$PY" \
    "$skills/codex-brief-antigravity-review/scripts/validate_templates.py" \
    "$skills/codex-brief-antigravity-review" \
    || restore_and_stop "$target" "$target-brief-core"
  if test "$target" = grok-cli; then
    inspect="$RUNTIME_EVIDENCE/grok-inspect.json"; test ! -e "$inspect"
    inspect_rc=0
    /Users/elvis/.grok/bin/grok inspect --json >"$inspect" \
      2>"$RUNTIME_EVIDENCE/grok-inspect.stderr" || inspect_rc=$?
    printf '%s\n' "$inspect_rc" >"$RUNTIME_EVIDENCE/grok-inspect.exit"
    chmod 600 "$inspect" "$RUNTIME_EVIDENCE/grok-inspect."{stderr,exit}
    test "$inspect_rc" = 0 || restore_and_stop "$target" grok-inspect
    capture "$target-discovery" "${INVOKE[@]}" verify-discovery \
      --target "$target" --plan "$PLAN" --transaction-receipt "$receipt" \
      --inspect-json "$inspect" --consume \
      || restore_and_stop "$target" "$target-discovery"
  else
    capture "$target-discovery" "${INVOKE[@]}" verify-discovery \
      --target "$target" --plan "$PLAN" --transaction-receipt "$receipt" \
      || restore_and_stop "$target" "$target-discovery"
  fi
  capture "$target-commit" "${INVOKE[@]}" commit-target --target "$target" \
    --plan "$PLAN" --transaction-receipt "$receipt" \
    || recover_and_stop "$target" "$target-commit"
}
run_target codex /Users/elvis/.codex/skills
run_target pi /Users/elvis/.pi/agent/skills
run_target antigravity-cli /Users/elvis/.gemini/antigravity-cli/skills
run_target grok-cli /Users/elvis/.grok/skills
capture verify-all "${INVOKE[@]}" verify-all --plan "$PLAN" --transaction-root "$TX"
```

Any helper return `90..94` is a legal `BLOCKED` stop. Preserve outputs; do not
continue to next target. A blocked recovery JSON intentionally fails
`parse_recovery` and returns 94.

## Appendix C: Exact trusted candidate guard

Candidate bundle exact top-level keys are
`schema_version,candidate_root,files,changed_paths,script_sha256,evidence`.
`files` maps every relative regular file to exact `sha256,mode`; no symlink or
cache is present. `evidence` maps immutable RED/GREEN/full artifact paths to
SHA-256. Control-plane writes this exact guard source; Luna does not edit it:

```python
from __future__ import annotations
import hashlib, json, os, re, stat, sys
from pathlib import Path

AUTH_KEYS = {
    "schema_version", "purpose", "root", "implementation_plan_path",
    "implementation_plan_sha256", "sync_plan_path", "sync_plan_sha256",
    "plan_review_path", "plan_review_sha256", "source_review_path",
    "source_review_sha256", "candidate_root", "candidate_bundle_path",
    "candidate_bundle_sha256", "candidate_script_path",
    "candidate_script_sha256", "candidate_inventory_sha256", "guard_path",
    "guard_sha256", "interpreter_path", "interpreter_sha256",
    "operation_set", "target_order", "managed_rule_selected",
}
BUNDLE_KEYS = {
    "schema_version", "candidate_root", "files", "changed_paths",
    "script_sha256", "evidence",
}
EXPECTED_CHANGED = {
    "scripts/validate_cross_cli_sync.py",
    "tests/test_cross_cli_sync.py",
    "references/cross-cli-sync.md",
    "references/sync-checklist.md",
}
ALLOWED_COMMANDS = {
    "verify-prestate", "apply", "verify", "verify-discovery", "commit-target",
    "restore-target", "recover-pending", "verify-all",
}
def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
def regular(path: Path, mode: int | None = None) -> Path:
    metadata = path.stat(follow_symlinks=False)
    if path.is_symlink() or not stat.S_ISREG(metadata.st_mode):
        raise SystemExit("BLOCKED: non-regular trusted artifact")
    if mode is not None and stat.S_IMODE(metadata.st_mode) != mode:
        raise SystemExit("BLOCKED: trusted artifact mode drift")
    return path
def check_ref(path_text: str, expected: str, mode: int | None = None) -> Path:
    path = regular(Path(path_text), mode)
    if sha(path) != expected:
        raise SystemExit("BLOCKED: trusted artifact SHA drift")
    return path
CANONICAL_ROOT = Path(
    "/Users/elvis/file/develop/opensource/openspec-superpower-change"
).resolve(strict=True)
CANONICAL_TASKS = (
    CANONICAL_ROOT
    / "openspec/changes/add-scoped-cross-cli-sync-plans/tasks.md"
)
CANONICAL_EVIDENCE = (
    CANONICAL_ROOT
    / "openspec/changes/add-scoped-cross-cli-sync-plans/evidence"
)
if len(sys.argv) < 3 or sys.argv[1] != "--":
    raise SystemExit("BLOCKED: invalid guard invocation")
self_path = Path(__file__).resolve(strict=True)
match = re.fullmatch(r"run-authorized-candidate-a([1-9][0-9]*)\.py", self_path.name)
if self_path.parent != CANONICAL_EVIDENCE or match is None:
    raise SystemExit("BLOCKED: noncanonical guard path")
attempt = match.group(1)
auth_path = CANONICAL_EVIDENCE / f"batch-a-launch-authorization-a{attempt}.json"
tasks_path = regular(CANONICAL_TASKS)
tasks_text = tasks_path.read_text(encoding="utf-8")
anchors = re.findall(
    rf"^Batch-A launch authorization a{attempt} SHA-256: ([0-9a-f]{{64}})$",
    tasks_text,
    re.M,
)
if len(anchors) != 1 or sha(regular(auth_path, 0o600)) != anchors[0]:
    raise SystemExit("BLOCKED: canonical launch anchor mismatch")
auth = json.loads(auth_path.read_text(encoding="utf-8"))
if set(auth) != AUTH_KEYS or auth["schema_version"] != 1:
    raise SystemExit("BLOCKED: launch authorization shape")
if auth["purpose"] != "execute reviewed Batch-A scoped sync":
    raise SystemExit("BLOCKED: launch authorization purpose")
if Path(auth["root"]).resolve(strict=True) != CANONICAL_ROOT:
    raise SystemExit("BLOCKED: canonical root substitution")
check_ref(auth["guard_path"], auth["guard_sha256"], 0o600)
if Path(auth["guard_path"]).resolve(strict=True) != Path(__file__).resolve(strict=True):
    raise SystemExit("BLOCKED: guard substitution")
interpreter = check_ref(auth["interpreter_path"], auth["interpreter_sha256"])
if Path(sys.executable).resolve(strict=True) != interpreter.resolve(strict=True):
    raise SystemExit("BLOCKED: interpreter substitution")
check_ref(auth["implementation_plan_path"], auth["implementation_plan_sha256"])
sync_plan_path = check_ref(auth["sync_plan_path"], auth["sync_plan_sha256"], 0o600)
check_ref(auth["source_review_path"], auth["source_review_sha256"])
check_ref(auth["plan_review_path"], auth["plan_review_sha256"])
bundle_path = check_ref(auth["candidate_bundle_path"], auth["candidate_bundle_sha256"], 0o600)
bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
if set(bundle) != BUNDLE_KEYS or bundle["schema_version"] != 1:
    raise SystemExit("BLOCKED: candidate bundle shape")
root = Path(auth["candidate_root"])
if root != Path(bundle["candidate_root"]) or root.is_symlink() or not root.is_dir():
    raise SystemExit("BLOCKED: candidate root")
if set(bundle["changed_paths"]) != EXPECTED_CHANGED:
    raise SystemExit("BLOCKED: candidate delta")
actual = {}
for path in root.rglob("*"):
    rel = path.relative_to(root).as_posix()
    if path.is_symlink():
        raise SystemExit("BLOCKED: candidate symlink")
    if path.is_file():
        if "__pycache__" in path.parts or path.suffix == ".pyc" or ".pytest_cache" in path.parts:
            raise SystemExit("BLOCKED: candidate cache")
        actual[rel] = {
            "sha256": sha(path),
            "mode": format(stat.S_IMODE(path.stat(follow_symlinks=False).st_mode), "04o"),
        }
if actual != bundle["files"]:
    raise SystemExit("BLOCKED: candidate inventory drift")
canonical_inventory = json.dumps(actual, sort_keys=True, separators=(",", ":")).encode()
if hashlib.sha256(canonical_inventory).hexdigest() != auth["candidate_inventory_sha256"]:
    raise SystemExit("BLOCKED: candidate inventory binding")
script = check_ref(auth["candidate_script_path"], auth["candidate_script_sha256"])
if script != root / "scripts/validate_cross_cli_sync.py" or bundle["script_sha256"] != auth["candidate_script_sha256"]:
    raise SystemExit("BLOCKED: candidate script binding")
for path_text, expected in bundle["evidence"].items():
    check_ref(path_text, expected, 0o600)
plan = json.loads(sync_plan_path.read_text(encoding="utf-8"))
if plan.get("schema_version") != 2 or auth["managed_rule_selected"] is not False:
    raise SystemExit("BLOCKED: scoped plan/rule binding")
if auth["target_order"] != ["codex", "pi", "antigravity-cli", "grok-cli"]:
    raise SystemExit("BLOCKED: target order")
expected_ops = [list(item) for item in auth["operation_set"]]
for target_id in auth["target_order"]:
    observed = [[item["skill"], item["path"]] for item in plan["targets"][target_id]["files"]]
    if observed != expected_ops or plan["targets"][target_id]["managed_rule"]["selected"] is not False:
        raise SystemExit("BLOCKED: operation-set drift")
args = sys.argv[2:]
if not args or args[0] not in ALLOWED_COMMANDS:
    raise SystemExit("BLOCKED: candidate command not authorized")
if any(item.startswith("--plan=") for item in args):
    raise SystemExit("BLOCKED: joined plan argument is forbidden")
plan_indices = [index for index, item in enumerate(args) if item == "--plan"]
if len(plan_indices) != 1 or plan_indices[0] + 1 >= len(args):
    raise SystemExit("BLOCKED: candidate command requires one plan")
plan_index = plan_indices[0]
try:
    supplied_plan = Path(args[plan_index + 1]).resolve(strict=True)
except OSError as exc:
    raise SystemExit("BLOCKED: candidate plan path") from exc
if supplied_plan != sync_plan_path.resolve(strict=True):
    raise SystemExit("BLOCKED: alternate candidate plan")
forward_args = list(args)
forward_args[plan_index + 1] = str(sync_plan_path.resolve(strict=True))
environment = {
    "HOME": str(auth_path.parent),
    "PATH": "/usr/bin:/bin",
    "PYTHONDONTWRITEBYTECODE": "1",
}
os.execve(
    str(interpreter),
    [str(interpreter), "-I", "-S", str(script), *forward_args],
    environment,
)
```

Before acceptance, test this guard with positive invocation plus mutations of
anchor, auth, guard, interpreter, bundle, candidate, reviews, sync plan,
operation set, managed rule, and command; every mutation must fail before the
candidate script starts.

## Task 9: Archive before final evidence

After Batch-B runtime Review PASS:

1. Project Learning Closeout;
2. reconcile active tasks and mark ready-to-archive evidence, not Completion;
3. compute UTC archive destination, require absent/collision-free;
4. archive `add-scoped-cross-cli-sync-plans` and verify unique actual path plus
   only allowed canonical spec update;
5. run strict post-archive validation;
6. run fresh full source/runtime final verification after archive;
7. fresh Codex/Sol Review purpose: post-archive actual files/complete diff,
   production wiring, both runtime batches, learning, archive, critical reruns,
   and independent adversarial probe;
8. bound control-plane alone decides Completion.

Cleanup owned candidate/backups/evidence only after both rollback needs resolve
and explicit destructive authorization. Never stage, commit, push, publish,
reset, clean, or delete unrelated state.

## Stop conditions

Return `BLOCKED` on missing approval; inline assignment/model drift; branch/HEAD/
status/prestate drift; attempt gap/overwrite; candidate/bundle/Review/launch-
authorization/hash drift; interpreter drift; selector/partition ambiguity;
assertion/rule parity failure; active legacy contract; stale/non-PASS Review;
runtime/receipt/recovery/discovery uncertainty; archive collision/unexpected
mutation; need to modify manifest/routing/authority/transaction lifecycle/
another source file/operation set; or unauthorized Git/publication/destruction.

Record evidence, owner `control-plane-high`, and resume condition in existing
OpenSpec tasks. Do not add state or widen retries.
