# Cross-CLI Sync Review Findings Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the two independent final-Review blockers without widening the approved cross-CLI sync scope: bind schema-v2 managed-rule paths to canonical target runtime layout and reconcile the predecessor closeout ledger.

**Architecture:** Preserve schema-v2 shape and existing transaction lifecycle. Derive each target's canonical global-rule destination from its validated `skills_root` and target ID, validate generated and loaded plans against that binding, and let candidate/apply/verify consume only the validated binding. Record the ledger correction and evidence refresh in the existing archived change ledgers; do not create a second state machine or mutate Git.

**Tech Stack:** Python 3 standard library, `unittest`, JSON plans, OpenSpec strict validator, SHA-256 evidence.

---

### Task 1: Capture rollback material and establish preflight facts

**Files:**
- Read only: `scripts/validate_cross_cli_sync.py`
- Read only: `tests/test_cross_cli_sync.py`
- Read only: `openspec/changes/archive/2026-08-27-add-backend-architecture-review-continuity/tasks.md`
- Read only: `openspec/changes/archive/2026-08-27-add-scoped-cross-cli-sync-plans/tasks.md`

- [x] **Step 1: Create a mode-0600 structured pre-change backup outside the repository.**

Run a standard-library backup script that copies each affected existing file with metadata and writes a mode-0600 JSON manifest under `/private/tmp/fix-cross-cli-sync-review-findings-20260827/backup/`. Do not use `git reset`, `git clean`, or any destructive cleanup.

- [x] **Step 2: Record Gate-1 evidence.**

Confirm the reproducible failure is accepted by current `_validate_plan` and that `_target_candidate_entries` points at the replacement ordinary file after coherent destination/pre-state mutation. Confirm allowed implementation files are limited to the validator, its tests, sync reference/spec, learning artifacts if required, and the two archived task ledgers plus this plan.

- [x] **Step 3: Preflight-review this plan.**

Check exact acceptance, no schema expansion, target-specific path mapping, negative test coverage, full verification commands, rollback path, no runtime apply/commit/push, and ledger evidence refresh. Any gap blocks implementation until this plan is revised.

### Task 2: Add the failing canonical-destination regression

**Files:**
- Modify: `tests/test_cross_cli_sync.py:2269` near `ScopedPlanTamperTests.test_managed_rule_selection_tamper_fails_closed`

- [x] **Step 1: Add one regression covering coherent destination and pre-state tampering.**

Create a selected-managed-rule v2 fixture, create a regular replacement file outside the target's canonical rule path, mutate `targets.codex.managed_rule.destination` and `pre_state` together, and assert `_validate_plan` raises `ValueError`. Assert `_target_candidate_entries` is never reached for the tampered plan; assert replacement bytes remain unchanged. Also assert generated v2 plans bind each target to the target-specific canonical rule path:

```python
    def test_managed_rule_destination_and_prestate_tamper_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            selected = ("openspec-superpower-change:SKILL.md",)
            fixture = create_scoped_v6_sync_fixture(root, selected)
            plan = make_scoped_plan(
                fixture, selected, select_managed_rule=True
            )
            replacement = root / "codex" / "ordinary.txt"
            replacement.write_bytes(b"ordinary-file\n")
            target = plan["targets"]["codex"]
            target["managed_rule"]["destination"] = str(replacement)
            target["managed_rule"]["pre_state"] = sync.capture_destination_prestate(
                replacement
            )
            with self.assertRaises(ValueError):
                sync._validate_plan(plan)
            self.assertEqual(replacement.read_bytes(), b"ordinary-file\n")
```

The test must also verify the canonical binding for `codex`, `pi`, `antigravity-cli`, and `grok-cli` uses the fixture's target runtime layout, including Antigravity's sibling `GEMINI.md` location.

- [x] **Step 2: Run the focused test and observe the expected RED failure.**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_cross_cli_sync.ScopedPlanTamperTests.test_managed_rule_destination_and_prestate_tamper_fail_closed -v
```

Expected: failure because current v2 validation accepts the coherently retargeted managed rule.

### Task 3: Implement canonical v2 managed-rule binding

**Files:**
- Modify: `scripts/validate_cross_cli_sync.py:27-31` for target rule-name constants
- Modify: `scripts/validate_cross_cli_sync.py:5890-5900` for generation-time binding
- Modify: `scripts/validate_cross_cli_sync.py:6022-6037` for v1 defense-in-depth binding
- Modify: `scripts/validate_cross_cli_sync.py:6185-6222` for v2 validation
- Modify: `scripts/validate_cross_cli_sync.py:6247-6255` for downstream binding access

- [x] **Step 1: Add one canonical target-rule resolver.**

Use a target-ID mapping with the documented runtime layout:

```python
TARGET_RULE_NAMES = {
    "codex": (1, "AGENTS.md"),
    "pi": (1, "APPEND_SYSTEM.md"),
    "antigravity-cli": (2, "GEMINI.md"),
    "grok-cli": (1, "AGENTS.md"),
}

def _canonical_rule_destination(target_id: str, skills_root: Path) -> Path:
    try:
        parent_levels, filename = TARGET_RULE_NAMES[target_id]
    except KeyError as exc:
        raise ValueError(f"unknown target: {target_id}") from exc
    if skills_root.name != "skills":
        raise ValueError(f"target skill root must end in skills: {target_id}")
    runtime_root = skills_root
    for _ in range(parent_levels):
        runtime_root = runtime_root.parent
    return runtime_root / filename
```

The resolver must be deterministic for isolated fixtures and real runtime paths. It must not inspect or trust `managed_rule.destination`.

- [x] **Step 2: Enforce the resolver during plan generation and v1/v2 loading.**

After resolving each target's `skills_root` and supplied rule path, require the supplied path to equal `_canonical_rule_destination(target_id, skills_root)` before capturing its pre-state. In `_validate_v1_plan` and `_validate_scoped_plan`, require the serialized rule destination to equal the same canonical path before `_regular_file` and pre-state validation. Preserve existing error redaction and exact object shapes.

- [x] **Step 3: Keep downstream consumers on the validated rule binding.**

Keep `_target_rule_binding` as the single access point. It may re-check the canonical destination defensively, but it must return the existing validated v1/v2 pre-state and selection fields without introducing a second transaction path. Candidate generation, apply, digest, verification, restore, and recovery must never use an unvalidated raw destination.

- [x] **Step 4: Run the focused RED test and complete GREEN.**

Run the named regression and the existing scoped plan/tamper/transaction classes. Expected: the new regression passes, existing v1/v2 tests remain green, and candidate generation never receives the tampered plan.

### Task 4: Synchronize contract and learning artifacts

**Files:**
- Modify: `references/cross-cli-sync.md`
- Modify: `references/sync-checklist.md` with the scoped binding rule
- Modify: `openspec/specs/skill-workflow-governance/spec.md`
- Modify: `openspec/changes/archive/2026-08-27-add-scoped-cross-cli-sync-plans/tasks.md` with correction evidence
- Modify: `docs/engineering-invariants.md`
- Create: `docs/learning-candidates/2026-08-27-scoped-managed-rule-destination-binding.md` for the high-severity false-PASS invariant

- [x] **Step 1: Document exact target-specific managed-rule binding.**

State that schema-v2 `managed_rule.destination` is accepted only when it equals the target-specific canonical path derived from `skills_root`: Codex/Pi/Grok use the parent runtime root; Antigravity uses the `.gemini` parent of its `antigravity-cli/skills` root. State that coherent destination/pre-state tampering is rejected before candidate/backup/apply.

- [x] **Step 2: Add the project-local invariant through the learning pipeline.**

Classify the P1 false-PASS as a high-severity integrity invariant. Persist only summarized project-relative provenance and SHA-256 values; no raw trace or sensitive runtime content. Add a deterministic negative regression reference. The learning audit records the invariant as project-local because one high-severity false-PASS event meets the promotion threshold.

- [x] **Step 3: Refresh scoped-change evidence references after implementation.**

Record new focused/full verification artifact paths and hashes, and explicitly mark prior plan/runtime/final evidence stale where its source SHA or plan binding changed. Do not claim old evidence still authorizes the changed source.

### Task 5: Reconcile predecessor closeout ledger

**Files:**
- Modify: `openspec/changes/archive/2026-08-27-add-backend-architecture-review-continuity/tasks.md`
- Modify: `openspec/changes/archive/2026-08-27-add-scoped-cross-cli-sync-plans/tasks.md`

- [x] **Step 1: Correct predecessor tasks 6.2 and 6.3 against actual evidence.**

Change both to checked only after fresh post-correction verification and Review evidence exist. Preserve the accepted evidence paths where still valid; add the new correction/final verification and independent Review paths with SHA-256 values. Do not rewrite unrelated historical evidence.

- [x] **Step 2: Make predecessor 6.4 explicit deferred work.**

Keep 6.4 unchecked if cleanup remains unauthorized, and state: owner `bound Codex control-plane/user authorization`; resume condition `after rollback/audit retention needs resolve and explicit cleanup authorization`; not a Completion requirement while retained evidence/backups remain required. This removes unexplained-open-task ambiguity without falsely claiming cleanup happened.

- [x] **Step 3: Refresh successor references and bindings.**

Update successor task 3.3 and closeout notes to reference the corrected predecessor ledger and new evidence hashes. Any final verification or Review artifact whose source tree/ledger SHA changed must be regenerated, not relabeled.

### Task 6: Strict verification and independent Review handback

**Files:**
- Read/verify all actual changed files and complete diff

- [x] **Step 1: Run fresh focused and full tests.**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_cross_cli_sync.ScopedPlanSelectionTests \
  tests.test_cross_cli_sync.ScopedPlanTamperTests \
  tests.test_cross_cli_sync.ScopedTransactionTests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

- [x] **Step 2: Run formal validators.**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .
openspec validate add-scoped-cross-cli-sync-plans --strict --no-interactive
openspec validate add-backend-architecture-review-continuity --strict --no-interactive

git diff --check
```

Also run the repository-required `quick_validate.py` with a PyYAML-capable interpreter and the dependency-free fallback validator.

- [x] **Step 3: Run the adversarial coherent-tamper probe.**

Use an isolated temporary fixture to mutate managed-rule destination and matching pre-state to an ordinary UTF-8 file. Assert v2 validation rejects before candidate creation, the ordinary file bytes remain unchanged, and no backup/receipt path is created. This is supporting evidence in addition to the deterministic regression.

- [x] **Step 4: Refresh final verification evidence after the last mutation.**

Record commands, exit codes, output hashes, changed-file inventory, source/runtime parity status, OpenSpec ledger status, and stale-evidence boundaries under `/private/tmp/fix-cross-cli-sync-review-findings-20260827/`. The reviewed schema-v2 runtime plan passed independent Sync-plan Review and was applied one target at a time; Git staging, commit, push, and destructive cleanup remain unauthorized. Final fresh evidence is bound in stable pointer `final-verification/current/summary.json` and the corrected supplemental Grok Review manifest.

- [x] **Step 5: Obtain a new distinct independent High Review.**

Review purpose: inspect the complete source/test/spec/ledger correction diff, decide whether both P1 findings are fixed, and test the coherent managed-rule destination/pre-state attack. Reviewer product: Grok CLI; role: `independent-reviewer`; capability: `control-plane-high`; independence: fresh Grok instance distinct from this executor, prior Pi reviewers, and all executors; authority: `governed-review-evidence` only. Review artifact: `/private/tmp/fix-cross-cli-sync-review-findings-20260827/final-review/grok-r1/review.final.md`, SHA-256 `c545bcdb8d946eb23cb4488807036696b1d0474e68d55b227a31b5113ae8b568`; result `PASS`, no actionable P0/P1/P2 finding. This evidence does not authorize a self-directed Completion transition.

- [x] **Step 6: Run Project Learning Closeout, then final verification and OpenSpec reconciliation.**

Learning candidate remains durable, non-sensitive, mechanically enforced, and `status: candidate`; promotion remains a bound Codex control-plane decision. Fresh final verification, four-runtime parity, strict validators, ledger reconciliation, and evidence binding are recorded in stable pointer `final-verification/current/summary.json` and `final-evidence-manifest-grok-r1.json`. Git commit/push and destructive cleanup remain unauthorized or deferred. Do not claim Completion without bound control-plane acceptance.
