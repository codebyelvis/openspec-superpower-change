# Add Role-First Review Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Review routing explicitly role-first, introduce an exact schema-6 Reviewer Assignment Contract, and add Pi as the fourth governed executor/reviewer runtime without granting any product canonical authority.

**Architecture:** The Router and Companion keep frozen schema-4/schema-5 parsers for read-only legacy audit, while every current creation, validation, evidence, transition, resume, and completion entry point accepts schema 6 only. The Router remains the canonical source for the managed v6 governance body and four-target portable manifest; source changes are completed and independently reviewed before a separate reviewed, target-local runtime transaction.

**Tech Stack:** Markdown Skills/references/templates, OpenSpec, default Python 3
for dependency-free project validators/tests, an isolated Conda Python 3.11
environment with PyYAML 6.x for the two approved `quick_validate` commands,
`unittest`, JSON fixtures, isolated Codex forward probes, macOS `sandbox-exec`
for optional Pi capability probes, path/SHA-256 preimage guards, and atomic
cross-CLI synchronization.

**Evidence profile:** `standard` for source slices; `control-plane-high` independent Review for Plan Preflight, candidate source, sync plan, learning, and final gates.

**Approved contract:** `add-role-first-review-routing`, explicitly approved by the user on 2026-08-10 after independent Proposal Review `PASS`.

**Approved artifact SHA-256:**

- `proposal.md`: `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330`
- `design.md`: `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480`
- `tasks.md`: `764a5401f7f5ec86348f3bfcabb854b196b26793b1b842b236f3731eafa7ffea`
- spec delta: `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384`

**Git boundary:** Do not create a Git worktree, stage, commit, push, fetch,
merge, reset, clean, checkout, publish, or mutate the index, refs, objects, or
working tree. The R9 evidence-rehydration amendment below is the sole exception
to the former blanket command prohibition: after the fresh R9 backup exists, it
may run only the ten exact read-only `git cat-file blob` extractions named by
R9, solely to reproduce hash-bound historical preimage bytes in the private R9
root. No other Git command or Git-derived authority is permitted.

**Runtime boundary:** Do not invoke Pi, alter any runtime Skill/global-rule target, update canonical workbench state, archive the change, or remove backups until the plan reaches its separately assigned gate. Source Plan Preflight `PASS` authorizes source execution only; source High Review and sync-plan Review are still required before runtime apply.

**Structured backup root:** `/private/tmp/add-role-first-review-routing-20260810-FPWT9V` (mode `0700`, outside every Skill discovery root).

**Preflight input record:** `docs/design/evidence/add-role-first-review-routing/2026-08-10-plan-preflight-inputs.md`; it binds final plan/source/runtime preimages, the two source backup archives, complete hidden-file-aware no-Git baselines, the exact source-delta allowlist, and `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/preflight-source-bindings-r4.json` without embedding native file contents.

**Mid-execution amendment input record:**
`docs/design/evidence/add-role-first-review-routing/2026-08-11-conda-plan-amendment-r7-inputs.md`
binds the Conda executable, absent isolated paths, unchanged original recovery
inputs, current partial source state, revised source-delta allowlist/bindings,
the prior Task 6 blocker evidence, and R5 `BLOCKED` finding `F-R5-001`. It
supplements rather than rewrites the accepted revision-4 Preflight or revision-5
Review evidence.

**Task 6 Conda amendment:** After the default Python 3.14 interpreter failed to
import PyYAML and its standard user install was refused by PEP 668, the user
authorized using their Conda installation. This Plan revision binds only
`/opt/anaconda3/bin/conda` (reviewed version `24.4.0`, SHA-256
`a543f4db6623ff7316d0549c2e5241196499a0d0b3e8d212772eeb2df084c8a3`)
and the isolated prefix, home, and package cache declared in Task 6. Creation
remains blocked until the amendment receives fresh independent Plan Preflight
`PASS`. The amendment does not reopen Tasks 1–5, authorize another source edit,
or grant runtime, Pi, Git, canonical, archive, publication, or completion
authority.

**Task 6 source-delta recovery amendment R8:** Task 6 Steps 3–5 reached fresh
PASS, but the complete no-Git source-delta gate found one modified generated
cache outside the revision-7 exact allowlist:
`scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc`. The user
authorized a minimal revision-8 recovery amendment on 2026-08-11: add only that
path plus the R8 evidence/Review paths to the exact allowlist, create and fsync
a private byte backup, then remove only that cache path through the reviewed
same-filesystem transaction below. The source-start SHA remains evidence, not
the restoration target; the current cache SHA is the byte set that must be
backed up before removal. No backup, move, deletion, source-delta rerun, Git,
Pi, runtime, canonical, archive, publication, completion, or cleanup is
authorized until the R8 amendment receives fresh independent Plan Preflight
`PASS`.

**Current R8 revision-2 amendment input record:**
`docs/design/evidence/add-role-first-review-routing/2026-08-12-source-delta-recovery-r8-r2-inputs.md`
binds the current and source-start cache hashes, exact single-path transaction,
the unchanged R4 backups/source-start inventories, the revision-2 exact
allowlist/bindings, partial-source snapshots, and all prior R4–R8 Review
history. The revision-1 R8 Review remains durably `BLOCKED`; revision 2 closes
only its two P1 findings and adds only its own three evidence/Review paths. It
grants no broad cache cleanup or restore authority.

**Task 6 evidence-rehydration amendment R9:** The R8-r2 Review artifact and its
ephemeral backup, baseline, allowlist, bindings, and dispatch snapshots were
not durably preserved, while the source cache and both candidate repositories
remain at the reviewed R8-r2 state. The user authorized a narrow R9 recovery on
2026-08-20. R9 must first retain fresh mode-`0600` current-tree backups under
`/private/tmp/add-role-first-review-routing-r9-r2-20260820-4hEfNB` (mode `0700`),
then rehydrate each of the 36 historical file preimages to the SHA-256 values
already recorded in the durable R4 input record. Six Router bytes may come only
from the exact object IDs recorded in the R9 inputs; four Companion bytes may
come only from the exact `HEAD:<path>` objects recorded there; all other bytes
must come from an exact current or runtime file whose SHA matches the durable
preimage table. R9 creates new archives, reconstructed source baselines,
preflight snapshots, allowlist, and bindings with new hashes and provenance. It
must never claim to recreate the missing containers or their historical hashes.

R9 also records a process deviation: read-only Git diagnostics were run during
blocker diagnosis before this amendment was written. Those commands did not
change the index, refs, objects, or working tree, but the deviation remains an
explicit Review input. R9 supersedes only the missing-artifact preconditions of
Task 6 Steps 5A–6. It does not reopen Tasks 1–5, broaden the single-cache
transaction, or grant source edits, other cleanup, Pi, runtime, canonical,
archive, publication, completion, or Git-write authority. The R9 preparation
and exact extraction procedure is bound by
`docs/design/evidence/add-role-first-review-routing/2026-08-20-evidence-rehydration-r9-inputs.md`.
Task 6 Step 5A remains blocked until an independent control-plane-high
Preflight is persisted at
`docs/design/reviews/2026-08-20-add-role-first-review-routing-evidence-rehydration-r9-review.md`
and accepted as `PASS` by the original control plane.

R9 preparation attempt 1 is retained at
`/private/tmp/add-role-first-review-routing-r9-20260820-OHY1Et`. It generated
private preimage objects only, then stopped before continuity output because its
probe omitted the `excluded_paths` field used by R8-r2 Preflight snapshots. It
made no repository, cache, or runtime mutation and is not an execution input.
R9 revision 2 uses the fresh root above, retains both the original pre-R9 backup
bytes and fresh pre-r2 backups, and corrects only that snapshot-schema error.

**Execution sub-skills after Preflight acceptance:** Use `superpowers:test-driven-development` for Tasks 1–5, `superpowers:writing-skills` while editing either Skill package, `superpowers:systematic-debugging` before changing any unexplained failing behavior, `superpowers:requesting-code-review` at Task 7, and `superpowers:verification-before-completion` at Task 11. Use exactly one execution governor—inline `superpowers:executing-plans` or user-approved subagent-driven execution—after the control plane accepts Plan Preflight `PASS`.

---

## Exact file map

Router source repository `/Users/elvis/file/develop/opensource/openspec-superpower-change`:

- Modify `SKILL.md`: four-product role eligibility, schema-6/current-vs-legacy routing, concrete Review destination wording.
- Modify `references/approved-implementation-workflow.md`: schema-6 current creation and pre-deployment schema-4/schema-5 drain.
- Modify `references/agent-capability-routing.md`: four-product equality under assigned roles and Codex control-plane instance-only authority.
- Modify `references/completion-contract.md`: four-target completion wording and legacy/current boundary where referenced.
- Modify `references/cross-cli-portable-manifest.json`: Pi target, all portable target lists, managed version 6, IDs `CCG-001` through `CCG-016`.
- Modify `references/cross-cli-sync.md`: Pi root/global file, deterministic discovery, probe isolation, target-local restore, four-target closure.
- Modify `references/handoff-contract.md`: canonical schema-6 example, exact immutable `reviewer_assignment`, current/legacy audit rules.
- Modify `references/request-modes.md`: concrete role-first standalone Review recommendation contract.
- Modify `references/response-patterns.md`: mandatory purpose/product/role/profile/independence/authority response pattern.
- Modify `references/self-evolution-rule.md`: four-target Major Self-Evolution closure.
- Modify `references/shared-global-governance.md`: revised `CCG-001`, `CCG-002`, `CCG-010`, and new `CCG-016`.
- Modify `references/step-evidence-gate.md`: schema-6 Reviewer Assignment and evidence-binding language.
- Modify `references/superpowers-adapter.md`: schema-6 Plan/Review assignment boundary where routing evidence is described.
- Modify `references/sync-checklist.md`: Pi paths, four-target commands, schema-4/schema-5 drain.
- Modify `scripts/validate_core_gates.py`: separated schema-4/schema-5/schema-6 validators, current-only entry points, legacy inventory, schema-2 parent binding.
- Modify `scripts/validate_cross_cli_sync.py`: Pi target, v6 semantic checks, deterministic discovery, safe isolated probe contract, receipt-bound apply/verify/restore/commit/verify-all, and complete no-Git source-delta audit.
- Delete only `scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc`
  after R8 Preflight `PASS`, exact current-byte backup, and the reviewed
  same-filesystem no-replace transaction. No other cache or generated path is
  authorized.
- Modify `tests/test_workflow_rules.py`: Router RED/GREEN contract, transition, legacy isolation, wording, and evidence tests.
- Modify `tests/test_cross_cli_sync.py`: four-target/v6/Pi safety, discovery, restore, and closure tests.
- Create `tests/fixtures/role-first-review-routing-cases.json`: six natural Review-routing prompts with withheld expected records.
- Create `tests/fixtures/role-first-review-routing-output.schema.json`: exact standalone output record schema.
- Create `tests/run_role_first_review_forward_tests.py`: isolated, read-only, sanitized forward-test runner.
- Modify `README.md`, `README_cn.md`, and `CHANGELOG.md`: current schema 6 and four-product public behavior.
- Create/update evidence only under `docs/design/evidence/add-role-first-review-routing/`.
- Create Review artifacts only under `docs/design/reviews/` after the assigned independent reviewer returns them.
- Modify `openspec/changes/add-role-first-review-routing/tasks.md` only for evidence-backed checkbox reconciliation; do not rewrite contract-bearing task text.

Companion source repository `/Users/elvis/file/develop/opensource/codex-brief-antigravity-review`:

- Modify `SKILL.md`: concrete four-product standalone and handed-off Review assignments.
- Modify `agents/openai.yaml`: metadata aligned with the standalone/handed-off four-product routes.
- Modify `references/agy-dispatch-template.md`: schema-6 assignment and purpose/authority fields.
- Modify `references/brief-template.md`: schema-6 immutable reviewer assignment and Preflight binding.
- Modify `references/handed-off-external-execution.md`: current schema-6-only governor plus non-authorizing legacy audit.
- Modify `references/handoff-contract.md`: byte-identical canonical contract shared with Router.
- Modify `references/report-template.md`: schema-6 coordinates and reviewer assignment display.
- Modify `references/review-template.md`: schema-6 Reviewer Assignment, purpose, identity, independence, authority, and transition audit.
- Modify `references/timeout-audit-template.md`: schema-6/current reviewer binding.
- Modify `scripts/validate_templates.py`: the same shared schema validator core plus Companion-specific template checks.
- Modify `tests/test_workflow_rules.py`: Companion RED/GREEN, current/legacy, template, and evidence tests.
- Modify `README.md`, `README_cn.md`, and `CHANGELOG.md`: public schema-6/four-product behavior.

No other source, runtime, active change, archived change, workbench, or project file is in scope. A needed extra file returns `BLOCKED` for scope approval.

## Preflight and stop contract

Before the first source implementation edit:

1. Verify the plan and approved four artifact hashes have not changed.
2. Verify every allowlisted existing source file against the durable preflight record and structured backup.
3. Verify every absent-to-be-created path is still absent and every parent remains a real non-symlink directory.
4. Re-inventory known canonical Handoff roots. An active schema-4 or schema-5 contract does not block source development, but it blocks the first runtime apply and must be recorded with owner/resume condition.
5. Refuse direct native-root Pi commands. Source tests may exercise only simulated probe functions; the optional real probe occurs after its plan gate with a temporary `HOME` and `PI_CODING_AGENT_DIR`, a `sandbox-exec` native-root deny rule, read-only tools, and network denial.
6. Stop if unrelated bytes would be overwritten, a preimage drifts, a symlink/non-regular file appears, a sensitive category is required, a Review assignment is incomplete, or a required validator/Review is `FAIL`/`BLOCKED`.
7. After the accepted Plan Preflight Review is stored, but immediately before
   the first source edit, require the two exact source-start paths below to be
   absent and capture both complete trees with this reviewed command. It includes
   hidden files and all existing Review/evidence/task files and excludes only
   the root `.git` entry without reading it:

```bash
umask 077
python3 - \
  /Users/elvis/file/develop/opensource/openspec-superpower-change \
  /private/tmp/add-role-first-review-routing-20260810-FPWT9V/router-tree-source-start.json \
  /Users/elvis/file/develop/opensource/codex-brief-antigravity-review \
  /private/tmp/add-role-first-review-routing-20260810-FPWT9V/companion-tree-source-start.json <<'PY'
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory(root_text: str) -> dict:
    root = Path(root_text)
    root_stat = root.lstat()
    if not stat.S_ISDIR(root_stat.st_mode) or root.is_symlink():
        raise SystemExit(f"invalid inventory root: {root}")
    records = []

    def visit(directory: Path, prefix: Path) -> None:
        for entry in sorted(os.scandir(directory), key=lambda item: item.name):
            relative = prefix / entry.name
            if prefix == Path() and entry.name == ".git":
                continue
            path = Path(entry.path)
            metadata = path.lstat()
            mode = format(stat.S_IMODE(metadata.st_mode), "04o")
            if stat.S_ISREG(metadata.st_mode):
                kind = "file"
                sha256 = digest_file(path)
            elif stat.S_ISDIR(metadata.st_mode):
                kind = "directory"
                sha256 = None
            elif stat.S_ISLNK(metadata.st_mode):
                kind = "symlink"
                target = os.readlink(path).encode("utf-8", "surrogateescape")
                sha256 = hashlib.sha256(target).hexdigest()
            else:
                kind = "other"
                sha256 = None
            records.append({
                "path": relative.as_posix(),
                "kind": kind,
                "mode": mode,
                "size": metadata.st_size,
                "sha256": sha256,
            })
            if kind == "directory":
                visit(path, relative)

    visit(root, Path())
    return {"schema_version": 1, "root": str(root), "records": records}


arguments = sys.argv[1:]
if len(arguments) != 4:
    raise SystemExit("expected two root/output pairs")
for root_text, output_text in zip(arguments[0::2], arguments[1::2]):
    output = Path(output_text)
    if output.exists() or output.is_symlink():
        raise SystemExit(f"inventory output already exists: {output}")
    payload = (json.dumps(inventory(root_text), sort_keys=True) + "\n").encode()
    descriptor = os.open(
        output,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
        0o600,
    )
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    print(json.dumps({"inventory": "pass", "output": str(output)}, sort_keys=True))
PY
```

Expected: two stdout JSON objects with `inventory: "pass"`; both output files
are regular mode `0600`. Persist their SHA-256 and record counts in the Task 1
RED evidence before editing. Any occupied output, unreadable entry, special-file
ambiguity, or failure to capture the full tree is `BLOCKED`.

Rollback before runtime apply is not an automatic permission in this Plan. The
structured source archives are recovery inputs only: if source restoration is
needed, stop `BLOCKED`, bind the current candidate hashes, prepare an exact
per-path restore plan limited to this Plan's allowlist, independently Review
that restore plan with this complete assignment: purpose is to inspect bound
current/backup/per-path bytes and decide whether the restore may run; product
`codex`; role `independent-reviewer`; profile `control-plane-high`; independence
is a user-opened instance distinct from the source executor and restore-plan
author; authority is restore-plan evidence only. Only then restore from a fresh
extraction. Never restore
the implementation Plan, evidence, Review artifacts, OpenSpec tasks, or an
unrelated path. Runtime rollback is different: it is target-local, implemented
and tested as part of the reviewed sync command, and uses only the failing
target's fresh transaction backup.

---

### Task 1: Add Router and Companion RED tests for schema 6

**Files:**

- Modify: Router `tests/test_workflow_rules.py`
- Modify: Companion `tests/test_workflow_rules.py`
- Test: both `tests/test_workflow_rules.py`

- [ ] **Step 1: Add schema-specific test builders without changing production code**

Add a schema-6 builder next to the existing schema-4/schema-5 helpers in both suites:

```python
def schema6_contract(validator, handoff: str, **overrides) -> dict:
    data = validator.extract_handoff_contract(handoff, "handoff")
    if data.get("schema_version") != 5:
        raise AssertionError("schema6 test fixture requires the frozen schema-5 example")
    old_assignment = data.pop("independent_reviewer_assignment")
    if set(old_assignment) != {
        "agent_product", "agent_instance_id", "agent_role", "capability_profile"
    }:
        raise AssertionError("unexpected frozen schema-5 reviewer shape")
    data["schema_version"] = 6
    data["reviewer_assignment"] = standard_reviewer_assignment(
        product=old_assignment["agent_product"],
        instance=old_assignment["agent_instance_id"],
    )
    data["readonly_fields"] = [
        "reviewer_assignment"
        if item == "independent_reviewer_assignment"
        else item
        for item in data["readonly_fields"]
    ]
    if "independent_reviewer_assignment" in data["readonly_fields"]:
        raise AssertionError("schema-5 readonly field leaked into schema-6 fixture")
    data.update(copy.deepcopy(overrides))
    return data


def standard_reviewer_assignment(product="codex", instance="codex-reviewer-02"):
    return {
        "review_purpose": {
            "object": "current batch implementation, Report, contract, and evidence",
            "decision": "decide pass, fail, or blocked for this governed Review gate",
        },
        "agent_product": product,
        "agent_instance_id": instance,
        "agent_role": "independent-reviewer",
        "capability_profile": "control-plane-high",
        "independence_requirement": {
            "kind": "distinct-contract-instance",
            "distinct_from": ["control_plane_owner", "executor_assignment"],
        },
        "result_authority": "governed-review-evidence",
    }


def compact_schema6_contract(validator, handoff: str, **overrides) -> dict:
    data = schema6_contract(validator, handoff)
    owner = data["control_plane_owner"]
    data["risk_profile"] = "compact"
    data["reviewer_assignment"] = {
        "review_purpose": {
            "object": "current compact implementation, evidence, and contract",
            "decision": "decide pass, fail, or blocked for the compact Review gate",
        },
        "agent_product": owner["agent_product"],
        "agent_instance_id": owner["agent_instance_id"],
        "agent_role": owner["agent_role"],
        "capability_profile": owner["capability_profile"],
        "independence_requirement": {
            "kind": "distinct-contract-instance",
            "distinct_from": ["executor_assignment"],
        },
        "result_authority": "governed-review-evidence",
    }
    data["independent_review_not_applicable_reason"] = (
        "compact inline Review is owned by the bound control-plane instance"
    )
    if not data["independent_review_not_applicable_reason"].strip():
        raise AssertionError("compact fixture requires a nonblank NA reason")
    if "independence_na_reason" in data:
        raise AssertionError("undefined compact reason field leaked into fixture")
    data.update(copy.deepcopy(overrides))
    return data
```

The builder is test-owned but contract-faithful: it performs the exact approved
schema-5-to-schema-6 field replacement and never calls a not-yet-implemented
production schema-6 helper during fixture setup. Add a `compact_schema6_contract`
helper that starts from this valid schema-6 shape, changes `risk_profile` to
`compact`, copies product/instance/role/profile from `control_plane_owner`, sets
`distinct_from` to exactly `["executor_assignment"]`, and supplies the required
nonblank top-level `independent_review_not_applicable_reason`. Before applying
an intentional invalid mutation, and for every valid acceptance case, tests
assert the fixture has schema 6, no
`independent_reviewer_assignment`, an exact seven-key `reviewer_assignment`, the
exact readonly replacement, a nonblank
`independent_review_not_applicable_reason`, and no undefined
`independence_na_reason` key.

- [ ] **Step 2: Add exact-shape and fail-closed RED cases**

Add table-driven tests that mutate one copy at a time and require rejection for:

```python
invalid_mutations = (
    lambda d: d.pop("reviewer_assignment"),
    lambda d: d["reviewer_assignment"].pop("review_purpose"),
    lambda d: d["reviewer_assignment"]["review_purpose"].update(object=" "),
    lambda d: d["reviewer_assignment"]["review_purpose"].update(extra="x"),
    lambda d: d["reviewer_assignment"]["independence_requirement"].update(kind="session-label"),
    lambda d: d["reviewer_assignment"]["independence_requirement"].update(
        distinct_from=["executor_assignment", "executor_assignment"]
    ),
    lambda d: d["reviewer_assignment"].update(result_authority="canonical-decision"),
    lambda d: d["reviewer_assignment"].update(agent_product="unknown-agent"),
)
```

Also assert that standard/strict requires exact `distinct_from` members, three distinct resolved instance IDs, reviewer role `independent-reviewer`, profile `control-plane-high`, and null NA reason. Assert compact requires reviewer identity equal to control plane, `distinct_from: [executor_assignment]`, a distinct executor instance, and a nonblank NA reason.

- [ ] **Step 3: Add current/legacy isolation RED cases**

Require `validate_handoff_contract` to reject schema 4, schema 5, missing schema, and schema-5 shape mislabeled as 6. Require a new read-only `inventory_legacy_handoffs` entry to report only `path`, `schema_version`, `lifecycle_state`, `sha256`, and `drain_status`; assert it cannot call current transition/evidence APIs. Require schema-4/schema-5 structural helpers to reject Pi while schema 6 accepts Pi.

- [ ] **Step 4: Add evidence and transition RED cases**

Add this complete mutation helper and table-driven transition test:

```python
def set_nested(mapping, path, value):
    target = mapping
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


readonly_mutations = (
    (("review_purpose", "object"), "changed review object"),
    (("review_purpose", "decision"), "changed review decision"),
    (("agent_product",), "pi"),
    (("agent_instance_id",), "changed-reviewer-09"),
    (("agent_role",), "control-plane"),
    (("capability_profile",), "cohesive-medium"),
    (("independence_requirement", "distinct_from"), ["executor_assignment"]),
    (("result_authority",), "canonical-control-plane-decision"),
)
for changed_path, changed_value in readonly_mutations:
    before = schema6_contract(self.validator, self.handoff)
    after = copy.deepcopy(before)
    after["contract_revision"] += 1
    after["lifecycle_state"] = "ready-for-execution"
    after["next_owner"] = "external-agent"
    set_nested(after["reviewer_assignment"], changed_path, changed_value)
    with self.assertRaisesRegex(AssertionError, "readonly|reviewer_assignment"):
        self.validator.validate_transition(before, after, "assignment-mutation")
```

Add schema-2 evidence tests for Pi product/instance/role/profile matching in a schema-6 parent, and frozen Pi rejection in a schema-5 parent helper. Add a PASS-review test showing that evidence validation alone does not mutate or promote canonical state.

The RED proof is a valid-schema acceptance test that calls the current public
`validate_handoff_contract` and therefore fails on the missing schema-6
production behavior. Mutation cases may also fail at that current-schema gate
during RED, but no failure caused by `KeyError`, a missing fixture field, or a
test-only helper counts as RED evidence. After GREEN, rerun every mutation case
and require the exact assignment/readonly/identity error asserted by the test.

- [ ] **Step 5: Run focused RED suites**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_workflow_rules -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s /Users/elvis/file/develop/opensource/codex-brief-antigravity-review/tests -v
```

Expected: only newly added schema-6/role-first tests fail; pre-existing tests
pass. At least one failure in each suite must be the valid schema-6 contract
reaching the production current-schema check. Zero fixture/setup `KeyError`,
`AttributeError`, malformed-shape, or missing-test-data failures are allowed.
Persist sanitized names and production assertion reasons under
`docs/design/evidence/add-role-first-review-routing/2026-08-10-schema6-red.md`;
do not persist raw environment/session data.

### Task 2: Implement the exact current schema-6 validator and frozen legacy audit

**Files:**

- Modify: Router `scripts/validate_core_gates.py`
- Modify: Router `references/handoff-contract.md`
- Modify: Companion `scripts/validate_templates.py`
- Modify: Companion `references/handoff-contract.md`
- Test: Router and Companion workflow-rule suites

- [ ] **Step 1: Split constants so expanded products cannot leak backward**

Replace shared identity/schema constants with separate closed sets:

```python
SCHEMA_VERSION = 6
SCHEMA5_VERSION = 5
LEGACY_SCHEMA_VERSION = 4
EVIDENCE_SCHEMA_VERSION = 2
LEGACY_EVIDENCE_SCHEMA_VERSION = 1
SCHEMA6_AGENT_PRODUCTS = {"codex", "pi", "antigravity-cli", "grok-cli"}
SCHEMA5_AGENT_PRODUCTS = {"codex", "antigravity-cli", "grok-cli"}
SCHEMA4_EXECUTOR_PRODUCTS = {"antigravity-cli", "grok-cli"}
SCHEMA4_REVIEWER_PRODUCTS = SCHEMA5_AGENT_PRODUCTS | {"not-applicable"}
SCHEMA6_AGENT_ROLES = {"control-plane", "executor", "independent-reviewer"}
SCHEMA5_AGENT_ROLES = {"control-plane", "executor", "independent-reviewer"}
```

Change `_validate_assignment` to accept an explicit `allowed_products` argument. Every schema-5 call passes `SCHEMA5_AGENT_PRODUCTS`; every schema-6 call passes `SCHEMA6_AGENT_PRODUCTS`. No current expanded constant may be referenced by schema-4/schema-5 validation.

- [ ] **Step 2: Add exact Reviewer Assignment validators**

Add these production interfaces in the shared validator core:

```python
REVIEW_PURPOSE_FIELDS = {"object", "decision"}
INDEPENDENCE_FIELDS = {"kind", "distinct_from"}
REVIEWER_ASSIGNMENT_FIELDS = {
    "review_purpose", "agent_product", "agent_instance_id", "agent_role",
    "capability_profile", "independence_requirement", "result_authority",
}


def _validate_review_purpose(value, label: str) -> None:
    if not isinstance(value, dict) or set(value) != REVIEW_PURPOSE_FIELDS:
        raise AssertionError(f"{label}: review_purpose must contain exactly object/decision")
    if not all(_is_nonblank(value[key]) for key in REVIEW_PURPOSE_FIELDS):
        raise AssertionError(f"{label}: review_purpose values must be non-blank")


def _validate_independence(value, expected: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != INDEPENDENCE_FIELDS:
        raise AssertionError(f"{label}: independence_requirement fields are invalid")
    if value["kind"] != "distinct-contract-instance":
        raise AssertionError(f"{label}: independence kind is invalid")
    distinct_from = value["distinct_from"]
    if (
        not isinstance(distinct_from, list)
        or not all(isinstance(item, str) for item in distinct_from)
        or len(distinct_from) != len(set(distinct_from))
        or set(distinct_from) != expected
    ):
        raise AssertionError(f"{label}: independence targets are invalid")
```

Add `_validate_schema6_reviewer_assignment(data, label)` that applies standard/strict or compact rules exactly as approved and validates resolved instance separation.

- [ ] **Step 3: Add schema-6 shape and current-only entry point**

Define `SCHEMA6_IMMUTABLE_FIELDS` as the existing schema-5 immutable set with `independent_reviewer_assignment` removed and `reviewer_assignment` added. Implement `_validate_schema6_handoff_contract` with the exact same replacement in its required top-level fields and reuse only common lifecycle checks that do not carry schema identity semantics.

Use these public boundaries:

```python
def validate_handoff_contract(data: dict, label: str) -> None:
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        raise AssertionError(f"{label}: current Handoff schema_version must be {SCHEMA_VERSION}")
    _validate_schema6_handoff_contract(data, label)


def validate_legacy_handoff_contract(data: dict, label: str) -> None:
    schema_version = data.get("schema_version") if isinstance(data, dict) else None
    if schema_version == LEGACY_SCHEMA_VERSION:
        _validate_schema4_handoff_contract(data, label)
    elif schema_version == SCHEMA5_VERSION:
        _validate_schema5_handoff_contract(data, label)
    else:
        raise AssertionError(f"{label}: legacy schema must be 4 or 5")
```

Current CLI `--status` and `--previous-status` use only
`validate_handoff_contract`. Rename `--schema4-inventory-root` to repeatable
`--legacy-inventory-root` and add required `--legacy-inventory-output` whenever
one or more inventory roots are supplied. The output is a mode-`0600` JSON
object with exact top-level keys `legacy_audit`, `active_legacy_count`, and
`records`; each record has only `path`, `schema_version`, `lifecycle_state`,
`sha256`, and `drain_status`. The audit uses only
`validate_legacy_handoff_contract` and exits nonzero if any schema-4/schema-5
lifecycle is not `complete`. Successful stdout is exactly one JSON object with
`legacy_audit: "pass"` and `active_legacy_count: 0`, followed by the existing
`Core gates valid: <root>` line.

- [ ] **Step 4: Bind schema-2 identity by parent schema without an evidence bump**

Refactor evidence assignment resolution to:

```python
def _evidence_assignment(data: dict, evidence_role: str) -> dict:
    if evidence_role == "attempt-report":
        return data["executor_assignment"]
    if evidence_role == "batch-review":
        return data["reviewer_assignment"]
    return data["control_plane_owner"]
```

For compact batch Review, `reviewer_assignment` already equals the control plane. Current evidence accepts only schema-6 products. Keep a private legacy parent-context identity check for frozen unit regressions, but do not expose it through current status/transition/resume/completion CLI paths. Continue to bind the entire Reviewer Assignment through the earlier `contract_revision` and `canonical_sha256`.

- [ ] **Step 5: Rewrite the shared Handoff contract and copy it byte-identically**

The canonical example must use `schema_version: 6`, replace the old four-field reviewer mapping with the exact seven-key mapping from the approved design, and apply the same replacement in `readonly_fields`. Document current-only validation, pre-deployment drain, immutable completed legacy history, and evidence-only result authority. Copy the final bytes to Companion and verify:

```bash
cmp -s \
  /Users/elvis/file/develop/opensource/openspec-superpower-change/references/handoff-contract.md \
  /Users/elvis/file/develop/opensource/codex-brief-antigravity-review/references/handoff-contract.md
```

Expected: exit `0`.

- [ ] **Step 6: Keep the shared validator core byte-identical**

Apply the schema core to Router first, then replace Companion's shared prefix from byte 0 through the line before Companion-only `validate_frontmatter`. The existing regression that compares the shared core must pass; do not independently retype two validator implementations.

- [ ] **Step 7: Run focused GREEN suites**

Run both workflow-rule suites. Expected: Task 1 tests and all existing transition/evidence tests pass; any old test that intentionally exercises schema 4/5 calls the explicit legacy helper and does not use current authority APIs.

### Task 3: Implement role-first Router and Companion wording

**Files:**

- Modify: Router `SKILL.md`
- Modify: Router `references/agent-capability-routing.md`
- Modify: Router `references/request-modes.md`
- Modify: Router `references/response-patterns.md`
- Modify: Router `references/approved-implementation-workflow.md`
- Modify: Router `references/step-evidence-gate.md`
- Modify: Router `references/superpowers-adapter.md`
- Modify: Router `references/completion-contract.md`
- Modify: Companion `SKILL.md`
- Modify: Companion `agents/openai.yaml`
- Modify: Companion `references/handed-off-external-execution.md`
- Modify: Companion `references/agy-dispatch-template.md`
- Modify: Companion `references/brief-template.md`
- Modify: Companion `references/report-template.md`
- Modify: Companion `references/review-template.md`
- Modify: Companion `references/timeout-audit-template.md`
- Modify: Router and Companion workflow tests

- [ ] **Step 1: Add exact concise standalone assignment wording**

The Router response pattern and Companion Standalone route must require all six labeled fields. Use this exact valid example in tests and documentation:

```text
Review purpose: inspect the current implementation plan and decide PASS or BLOCKED; reviewer product: codex; role: independent-reviewer; capability: control-plane-high; independence: a user-opened new-window instance distinct from the plan author and executor; authority: governed Review evidence only.
```

The routing order is canonical assignment, explicit user product, one concrete control-plane recommendation, then `BLOCKED`. Reject generic “another agent”, “independent agent”, or “another model” when it is the only destination.

- [ ] **Step 2: Update product/authority language without creating a second authority**

Every Router/Companion surface must say that all four products are eligible only for assigned executor/reviewer roles, while canonical authority requires the bound Codex product plus `control-plane`, `control-plane-high`, instance, and contract. Remove statements that give Codex authority by product name alone or limit governed executor/reviewer roles to Antigravity/Grok.

- [ ] **Step 3: Update templates to display the complete immutable assignment**

Brief/Report/Review/dispatch/timeout templates must display nonblank purpose object/decision, product, instance, role, profile, `distinct_from`, and result authority. Replace schema-5 coordinate rows with schema 6. Preserve schema-2 evidence manifests and require their identity to match the parent schema-6 assignment.

- [ ] **Step 4: Add static regressions**

Add exact normalized assertions for all six conceptual assignment fields, the four-product enum, user-product preservation, instance separation, evidence-only Review authority, and current schema 6. Add negative searches that fail if an operational current-workflow section still says `schema-version-5`, `schema-5 Handoff`, or names only the old three products. Historical changelog and explicitly labeled legacy sections are allowed.

### Task 4: Upgrade the managed rule and four-target manifest

**Files:**

- Modify: Router `references/shared-global-governance.md`
- Modify: Router `references/cross-cli-portable-manifest.json`
- Modify: Router `references/cross-cli-sync.md`
- Modify: Router `references/self-evolution-rule.md`
- Modify: Router `references/sync-checklist.md`
- Modify: Router `scripts/validate_cross_cli_sync.py`
- Modify: Router `tests/test_cross_cli_sync.py`

- [ ] **Step 1: Add v6 semantic RED assertions**

Add `MANAGED_RULE_INVARIANT_COUNT[6] = 16` tests and exact normalized body assertions for approved `CCG-001`, `CCG-002`, `CCG-010`, and `CCG-016`. Tests must reject a v6 body that has correct markers/IDs/hash but omits role/profile/instance/contract authority, any one product, old-schema drain, immutable history, purpose, or fail-closed generic destination behavior.

- [ ] **Step 2: Update the single managed body**

Replace only `CCG-001`, `CCG-002`, and `CCG-010` with the approved design text and append `CCG-016`. Keep `CCG-003` through `CCG-009` and `CCG-011` through `CCG-015` semantically unchanged.

- [ ] **Step 3: Add Pi to every manifest target list**

For every portable file entry, set targets to this exact list and order:

```json
["codex", "pi", "antigravity-cli", "grok-cli"]
```

Set managed version 6 and exact IDs `CCG-001` through `CCG-016`. Add the required pending Pi target state with Codex decision owner and nonblank evidence/reason/resume fields. Validation must require all four target IDs when any target is required.

- [ ] **Step 4: Add Pi CLI path arguments and deterministic discovery**

Extend `_target_arguments` and `plan` parser with:

```python
"pi": {
    "skills_root": str(args.pi_skills_root.resolve()),
    "rule_file": str(args.pi_rule_file.resolve()),
}
```

Add `--pi-skills-root` / `--pi-rule-file`. Extend `verify-discovery` to all four
target IDs; `--inspect-json` is forbidden for Codex/Pi/Antigravity and required
for Grok. Codex, Pi, and Antigravity use deterministic root plus portable
closure validation; Grok additionally validates its mode-`0600` inspect JSON.
Add `verify-prestate --plan <path> --target <codex|pi|antigravity-cli|grok-cli|all>`;
it performs only path containment, root/type/mode/symlink, source SHA, destination
SHA, managed-marker, and plan-fingerprint guards and prints
`{"prestate":"pass","targets":[...]}` on exit 0. A missing/stale target remains
`BLOCKED`, never `not-applicable`.

- [ ] **Step 5: Implement the isolated Pi probe contract**

Add pure helpers that validate/build but do not automatically run a probe during native target validation:

```python
def build_pi_probe(
    pi_executable: Path,
    temporary_root: Path,
    native_pi_root: Path,
    *,
    prompt: str | None = None,
) -> dict:
    # returns argv, env, sandbox_profile, allowed_output_fields
```

The returned environment sets both `HOME` and `PI_CODING_AGENT_DIR` below `temporary_root`; the sandbox profile denies file read/write below the resolved native root and denies network. Prompt argv includes `--no-session`, `--no-context-files`, `--no-skills`, and a read-only tool allowlist. Reject a symlink, containment overlap, missing `/usr/bin/sandbox-exec`, native-root HOME/PI values, or a profile without explicit native-root denial. Actual target `verify_target` must never call this helper or Pi.

Expose this helper only through the explicitly invoked command:

```text
probe-pi --pi-executable <regular-file> --native-pi-root <root>
  --temporary-root <new-empty-root> --prompt-file <review-prompt>
  --read-root <reviewed-source-root> [--read-root ...] --output <result-json>
```

The wrapper creates its sandbox profile and temporary HOME itself and launches
this exact inner argv through `/usr/bin/sandbox-exec`:

```text
/Users/elvis/.local/bin/pi --no-session --no-context-files --no-skills
  --tools read,grep,find,ls -p <complete prompt bytes>
```

The subprocess environment is an explicit allowlist containing only temporary
`HOME`, temporary `PI_CODING_AGENT_DIR`, `PATH=/usr/bin:/bin:/Users/elvis/.local/bin`,
and locale values. The sandbox permits read-only access only to system runtime
files plus each `--read-root`, permits writes only below `--temporary-root`,
denies reads and writes below the resolved native Pi root, and denies network.
The output file is mode `0600`, contains only reviewer identity/categories,
bound input hashes, verdict, and complete sanitized findings, and is rejected if
it contains a native-root path, environment dump, credential/session/settings
category, raw debug trace, or an unrecognized key. Missing flags, unsupported Pi
CLI behavior, sandbox denial not being mechanically provable, or any attempted
native-root access returns exit 1 and a sanitized `pi_probe: "blocked"` result;
the executor must not relax the isolation contract.

- [ ] **Step 6: Prove target-local restore and four-target closure**

Add a mode-`0600` per-target transaction receipt outside every discovery root.
`apply` requires `--transaction-receipt` and implements this exact durable state
machine:

```text
absent
  -> prepared
  -> mutation-intent
  -> applied-uncommitted
  -> verified

prepared | mutation-intent | applied-uncommitted
  -> restored

prepared | mutation-intent | applied-uncommitted
  -> recovery-blocked
```

The immutable receipt fields are `schema_version`, `target`, `plan_sha256`,
`destination_preimage_sha256`, `candidate_sha256`,
`backup_manifest_sha256`, and `transaction_id`. Every state revision also has
`revision`, `previous_receipt_sha256`, and `state`. Before publishing
`prepared`, `apply` MUST create every target-local backup object and the closed
backup manifest with `O_CREAT|O_EXCL|O_NOFOLLOW`, mode `0600`; fsync every file,
fsync every created backup directory, re-open and hash the complete backup, and
bind the verified manifest SHA in the receipt. No destination byte may change
before a complete `prepared` receipt is durably installed.

Receipt creation and state replacement use one production helper under a
nonblocking per-target `flock` on a real mode-`0600` lock file in the mode-`0700`
transaction root. It writes a same-directory regular temporary file using
`O_CREAT|O_EXCL|O_NOFOLLOW`, mode `0600`, writes the complete canonical JSON,
flushes and fsyncs it, then atomically installs the initial receipt with macOS
`renameatx_np(..., RENAME_EXCL)` or atomically swaps a state revision with
`renameatx_np(..., RENAME_SWAP)`. After a swap, it verifies the displaced
receipt byte hash equals the expected current receipt, installs that displaced
revision under a no-replace `history/revision-<n>.json` name, and fsyncs both
history and receipt parent directories. Unsupported atomic primitives, a
symlink/non-regular/mode mismatch, current-receipt SHA drift, or any fsync error
is `BLOCKED`; `os.replace`, unlink-then-rename, or an un-fsynced receipt is not an
allowed fallback.

After `prepared` is durable, `apply` atomically advances and fsyncs the receipt
to `mutation-intent` before the first destination write. A crash in this state
is conservatively treated as a partial mutation even if no write occurred.
Each destination candidate is written through a same-directory mode-`0600`
temporary regular file, fsynced, atomically installed with the approved
preimage guard, and followed by an fsync of its parent directory. Only after
all target files and target directories are durable may the receipt atomically
advance to `applied-uncommitted`. `verify` and `verify-discovery` each require
that state and atomically add their sanitized digest without committing it.
Add these exact commands:

```text
restore-target --target <target> --plan <plan> --backup-root <root>
  --transaction-receipt <receipt>
recover-pending --plan <plan> --backup-root <root>
  --transaction-root <root>
commit-target --target <target> --plan <plan>
  --transaction-receipt <receipt>
```

`restore-target` accepts only `prepared`, `mutation-intent`, or
`applied-uncommitted`. It revalidates the receipt, Plan, target, backup-manifest
SHA, every backup object, and the current target closure before writing. In
`prepared`, an exact reviewed destination preimage is verified without a write
and the state advances to `restored`; any mismatch is a protocol/external-drift
violation and becomes `recovery-blocked`. In `mutation-intent` or
`applied-uncommitted`, every governed current path must match either its bound
preimage or its bound candidate form, with no unknown path/type/mode; otherwise
restoration is ambiguous and becomes `recovery-blocked` without overwriting the
unknown bytes. An admissible restore writes only that target from the verified
backup, fsyncs every restored file and affected parent directory, verifies the
exact reviewed destination preimage, and atomically changes state to
`restored`.

Successful restore stdout has exact keys `restore`, `target`, `restored`, and
`later_targets_started`, with values `"pass"`, the target, `true`, and `false`.
A restoration that cannot prove safe compensation atomically changes a valid
receipt to `recovery-blocked`; if the receipt itself cannot be trusted, it
preserves all bytes and creates a separate exclusive mode-`0600`
`<target>.manual-disposition.json` binding the receipt/plan/observed hashes.
Either case prints the same keys with `restore: "blocked"` and
`restored: false`, returns nonzero, and requires control-plane manual
disposition. Later targets are forbidden whenever a receipt is not `verified`
or either recovery-blocked form exists.

`recover-pending` is the only restart entry. It rejects an unbound/orphaned
backup or temporary receipt, restores the single earliest target in
`prepared`/`mutation-intent`/`applied-uncommitted` using the rules above, never
resumes forward mutation in the same invocation, returns nonzero after either a
successful restore or a block, and reports exact JSON keys `recovery`, `target`,
`restored`, and `later_targets_started`. A transaction root containing only
`verified`/`restored` receipts is still not reusable; retry requires a new
absent transaction root and fresh Sync-plan Review. `commit-target` requires
both content and discovery digests, reruns target verification, atomically
changes state to `verified`, and prints
`{"commit":"pass","target":"..."}`. No command deletes backups, receipts,
history, or manual-disposition evidence.

The production `apply` command catches any ordinary exception after durable
`prepared`, invokes the same target-local restoration routine before returning,
and returns nonzero even when compensation succeeds. An uncatchable process or
host interruption leaves the last fsynced receipt state for the next
`recover-pending` invocation; no restart path may infer success from destination
bytes or skip recovery because candidate bytes appear complete.

Extend isolated CLI round-trip tests with four temporary targets. Drive the
real production transaction function in a child process with an injected crash
hook, never a fake receipt builder. Cover these exact interruption points:

1. after the verified backup is fsynced but before `prepared` is installed:
   destination remains the exact preimage, no final receipt exists, orphaned
   transaction material blocks reuse and requires manual disposition;
2. after `prepared` is fsynced but before `mutation-intent`: receipt is
   `prepared`; `recover-pending` verifies the unchanged preimage, marks it
   `restored`, returns nonzero, and no later target starts;
3. immediately after the first destination write: durable receipt remains
   `mutation-intent`; recovery restores and verifies the exact preimage;
4. after the last destination write and destination-directory fsync but before
   `applied-uncommitted`: durable receipt remains `mutation-intent`; recovery
   restores and verifies the exact preimage.

Assert call ordering proves backup object/manifest fsync precedes `prepared`,
`prepared` receipt/file-parent fsync precedes `mutation-intent`,
`mutation-intent` receipt/file-parent fsync precedes the first destination
write, and all destination/file-parent fsyncs precede `applied-uncommitted`.
Also inject an internal Pi apply exception, an external Pi `verify` failure,
and an external Pi `verify-discovery` failure after prior Codex commit. Each
admissible path restores only Pi, verifies its reviewed preimage, leaves Codex
candidate bytes committed, keeps Antigravity/Grok functions uncalled, and
stops. Inject an unknown current-path digest and a restore verification failure;
both require `recovery-blocked`, `restored: false`, retained evidence, and no
broad/manual fallback. A target cannot be committed without both verification
digests; a later target cannot start while the earlier receipt is
`prepared`/`mutation-intent`/`applied-uncommitted`/`restored`/
`recovery-blocked`. Extend `verify-all` with required `--transaction-root`; it
accepts only four `verified` receipts bound to the same plan and fails on an
orphan, manual-disposition file, or missing/stale/unverified Pi.

- [ ] **Step 7: Implement complete no-Git inventory and safe source-delta evidence**

Add a `source-delta` subcommand with this exact interface:

```text
source-delta --bindings <preflight-bindings-json>
  --router-root <router-root> --companion-root <companion-root>
  --router-baseline <source-start-json>
  --companion-baseline <source-start-json>
  --compare-root <new-absent-directory> --output <delta-json>
```

The inventory walks every entry without following symlinks, including hidden
files such as `.gitignore`; it excludes only the root `.git` entry and its
children. Each sorted record contains exactly relative path, kind, mode, size,
and either a regular-file SHA-256, a SHA-256 of symlink-target bytes, or null for
other kinds. The bindings JSON supplies exact Plan, backup, preflight baseline,
and source-delta allowlist paths/hashes. Any hash/type/mode mismatch is
`BLOCKED`.

Before archive extraction, require a new absent compare root, validate the
archive SHA and exact member inventory, reject absolute/traversal paths,
duplicates, links, devices, and non-regular members, and create every output
with exclusive no-follow semantics beneath a mode-`0700` compare root. Never
call `extractall`. Compare backup bytes to current allowlisted source bytes and
the complete source-start inventories to current trees. Output is mode `0600`
JSON with exact keys `source_delta`, `changed_paths`, `source_changes`,
`unexpected_paths`, and `compare_root`; success requires
`source_delta: "pass"` and an empty `unexpected_paths` array.

Tests create hidden `.gitignore`, existing unrelated Review files, nested
directories, symlinks, and malicious tar members. They must prove `.git/**` is
the only tree exclusion, changes to an existing unrelated Review or hidden file
are detected, only exact allowlist paths pass, occupied compare roots fail,
malicious archives never extract, and the validated archive/source comparison
reports correct before/after SHA values.

### Task 5: Add natural standalone forward-test fixtures

**Files:**

- Create: Router `tests/fixtures/role-first-review-routing-cases.json`
- Create: Router `tests/fixtures/role-first-review-routing-output.schema.json`
- Create: Router `tests/run_role_first_review_forward_tests.py`
- Modify: Router `tests/test_workflow_rules.py`

- [ ] **Step 1: Create six prompt cases without exposing expected values to the model**

Create this exact fixture; `expected` is test-oracle data that is loaded only
after the model process exits:

```json
[
  {
    "id": "generic_review_destination",
    "prompt": "让另一个 agent Review 当前实施计划，决定是否可以开始执行；不要修改文件。",
    "expected": {"route_result": "actionable", "reviewer_product": "codex", "reviewer_role": "independent-reviewer", "capability_profile": "control-plane-high", "result_authority": "governed-review-evidence", "blocker_owner": "none"}
  },
  {
    "id": "user_selected_pi",
    "prompt": "把这份只读设计报告交给 Pi Review；保留我指定的产品并说明它的结果权限。",
    "expected": {"route_result": "actionable", "reviewer_product": "pi", "reviewer_role": "advisory-reviewer", "capability_profile": "control-plane-high", "result_authority": "advisory-input", "blocker_owner": "none"}
  },
  {
    "id": "new_window_codex",
    "prompt": "请明确要求新窗口 Codex 独立 Review 当前 plan，决定 PASS 或 BLOCKED；不要实施。",
    "expected": {"route_result": "actionable", "reviewer_product": "codex", "reviewer_role": "independent-reviewer", "capability_profile": "control-plane-high", "result_authority": "governed-review-evidence", "blocker_owner": "none"}
  },
  {
    "id": "advisory_review",
    "prompt": "请推荐一个具体产品只做这份报告的咨询性 Review，不决定任何 gate。",
    "expected": {"route_result": "actionable", "reviewer_product": "codex", "reviewer_role": "advisory-reviewer", "capability_profile": "control-plane-high", "result_authority": "advisory-input", "blocker_owner": "none"}
  },
  {
    "id": "same_pi_session",
    "prompt": "Pi session pi-executor-01 已完成实现，现在让同一个 pi-executor-01 做必须独立的 High Review。",
    "expected": {"route_result": "blocked", "reviewer_product": "pi", "reviewer_role": "independent-reviewer", "capability_profile": "control-plane-high", "result_authority": "governed-review-evidence", "blocker_owner": "control-plane"}
  },
  {
    "id": "required_reviewer_unavailable",
    "prompt": "当前没有任何与作者和执行者不同的可用实例，但 strict gate 要求独立 Review；给出下一步。",
    "expected": {"route_result": "blocked", "reviewer_product": "codex", "reviewer_role": "independent-reviewer", "capability_profile": "control-plane-high", "result_authority": "governed-review-evidence", "blocker_owner": "user"}
  }
]
```

The runner additionally requires nonblank `review_purpose.object`,
`review_purpose.decision`, and `independence_requirement` for every case;
blocked cases require a nonblank `resume_condition`, while actionable cases
require `resume_condition: null`.

- [ ] **Step 2: Create an exact output schema**

Create this complete JSON Schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "route_result", "review_purpose", "reviewer_product", "reviewer_role",
    "capability_profile", "independence_requirement", "result_authority",
    "blocker_owner", "resume_condition"
  ],
  "properties": {
    "route_result": {"enum": ["actionable", "blocked"]},
    "review_purpose": {
      "type": "object",
      "additionalProperties": false,
      "required": ["object", "decision"],
      "properties": {
        "object": {"type": "string", "minLength": 1},
        "decision": {"type": "string", "minLength": 1}
      }
    },
    "reviewer_product": {"enum": ["codex", "pi", "antigravity-cli", "grok-cli"]},
    "reviewer_role": {"enum": ["advisory-reviewer", "independent-reviewer", "control-plane"]},
    "capability_profile": {"enum": ["control-plane-high", "cohesive-medium", "mechanical-low"]},
    "independence_requirement": {"type": "string", "minLength": 1},
    "result_authority": {"enum": ["advisory-input", "governed-review-evidence", "canonical-control-plane-decision"]},
    "blocker_owner": {"enum": ["none", "control-plane", "user", "dependency"]},
    "resume_condition": {
      "anyOf": [
        {"type": "string", "minLength": 1},
        {"type": "null"}
      ]
    }
  }
}
```

Use JSON Schema enums/types, `additionalProperties: false`, required fields, and local nonblank/semantic checks.

- [ ] **Step 3: Implement isolated execution and sanitized evidence**

Follow the existing Superpowers routing runner's isolation pattern: fresh temporary project/HOME, explicit Router source, no inherited project rules, read-only sandbox, no Git requirement, output schema, mode-`0600` transient output, and deletion after extracting only the structured record. Never persist raw reasoning, session, debug, auth, environment, or filesystem traces.

The runner CLI is exact:

```text
run_role_first_review_forward_tests.py
  --cases <cases-json> --output-schema <schema-json>
  --router-root <router-source> --companion-root <companion-source>
  --temporary-root <new-empty-root> --sanitized-summary <summary-json>
```

It prints one JSON object with exact keys `forward`, `case_count`, and
`summary`; successful values are `"pass"`, `6`, and the absolute summary path.
The summary is mode `0600`; each case record contains only `case_id`, `result`,
`reviewer_product`, `reviewer_role`, `capability_profile`,
`independence_category`, `result_authority`, and `blocker_owner`. The runner
deletes all raw model/process outputs before returning. Any missing raw-output
cleanup, extra summary field, non-0600 mode, or case mismatch returns exit 1.

- [ ] **Step 4: Add fixture/runner tests**

Unit tests must prove expected values are withheld from the prompt, invalid extra/missing fields fail, Pi substitution fails, same-instance output cannot be actionable, blocked output requires owner/resume, and sanitized summary contains only case ID/result/assignment fields.

### Task 6: Update public documentation and run source verification

**Files:**

- Modify: Router `README.md`, `README_cn.md`, `CHANGELOG.md`
- Modify: Companion `README.md`, `README_cn.md`, `CHANGELOG.md`
- Create/update: Router `docs/design/evidence/add-role-first-review-routing/`

- [ ] **Step 1: Update current public behavior**

Document schema 6, schema-2 evidence binding, four equal executor/reviewer products, Codex bound control-plane authority, concrete Review assignments, Pi root/global-rule path, and four-target completion. Keep schema-4/schema-5 text only in explicitly historical/legacy contexts.

- [ ] **Step 2: Create the independently reviewed Conda verification environment**

Run exactly from the Router root only after the Conda Plan amendment receives
fresh independent Preflight `PASS`:

```bash
(
set -euo pipefail
umask 077
ROLE_CONDA=/opt/anaconda3/bin/conda
ROLE_CONDA_PREFIX=/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-quick-validate-r1
ROLE_CONDA_HOME=/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-home-r1
ROLE_CONDA_PKGS=/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-pkgs-r1
ROLE_CONDA_TMP=/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-tmp-r1

ROLE_CONDA_SHA="$(shasum -a 256 "$ROLE_CONDA" | awk '{print $1}')"
test "$ROLE_CONDA_SHA" = \
  a543f4db6623ff7316d0549c2e5241196499a0d0b3e8d212772eeb2df084c8a3
test ! -e "$ROLE_CONDA_PREFIX"
test ! -L "$ROLE_CONDA_PREFIX"
test ! -e "$ROLE_CONDA_HOME"
test ! -L "$ROLE_CONDA_HOME"
test ! -e "$ROLE_CONDA_PKGS"
test ! -L "$ROLE_CONDA_PKGS"
test ! -e "$ROLE_CONDA_TMP"
test ! -L "$ROLE_CONDA_TMP"
mkdir -m 0700 "$ROLE_CONDA_HOME" "$ROLE_CONDA_PKGS" "$ROLE_CONDA_TMP"
ROLE_CONDA_VERSION="$(HOME="$ROLE_CONDA_HOME" CONDA_PKGS_DIRS="$ROLE_CONDA_PKGS" \
  TMPDIR="$ROLE_CONDA_TMP" PYTHONNOUSERSITE=1 CONDA_NO_PLUGINS=true \
  "$ROLE_CONDA" --version)"
test "$ROLE_CONDA_VERSION" = "conda 24.4.0"

HOME="$ROLE_CONDA_HOME" \
CONDA_PKGS_DIRS="$ROLE_CONDA_PKGS" \
TMPDIR="$ROLE_CONDA_TMP" \
PYTHONNOUSERSITE=1 \
CONDA_NO_PLUGINS=true \
  "$ROLE_CONDA" create --yes \
    --prefix "$ROLE_CONDA_PREFIX" \
    --solver classic --override-channels --channel defaults --no-default-packages \
    'python=3.11' 'pyyaml>=6,<7'

test -x "$ROLE_CONDA_PREFIX/bin/python"
ROLE_CONDA_HOME_MODE="$(stat -f '%Lp' "$ROLE_CONDA_HOME")"
test "$ROLE_CONDA_HOME_MODE" = 700
ROLE_CONDA_PKGS_MODE="$(stat -f '%Lp' "$ROLE_CONDA_PKGS")"
test "$ROLE_CONDA_PKGS_MODE" = 700
ROLE_CONDA_TMP_MODE="$(stat -f '%Lp' "$ROLE_CONDA_TMP")"
test "$ROLE_CONDA_TMP_MODE" = 700
"$ROLE_CONDA_PREFIX/bin/python" - <<'PY'
import sys
import yaml

assert sys.version_info[:2] == (3, 11), sys.version
assert yaml.__version__.split(".")[0] == "6", yaml.__version__
print(f"conda-verification-python: pass; python={sys.version_info.major}.{sys.version_info.minor}; pyyaml-major=6")
PY
)
```

Expected: every precondition exits `0`; Conda creates only the reviewed prefix
plus its isolated home/package-cache/temporary paths under the existing mode-`0700`
transaction root; the final line is exactly
`conda-verification-python: pass; python=3.11; pyyaml-major=6`. Conda may fetch
only from the explicit `defaults` channel. Do not activate the environment,
run `conda init`, change Conda configuration, update/modify base, use pip, use
`--break-system-packages`, reuse an occupied prefix, or substitute another
Conda executable/interpreter. If the standard `conda create` is refused or any
guard fails, the subshell exits immediately at that command; record `BLOCKED`
and stop without fallback or automatic cleanup. Retain the isolated environment
until Task 6 evidence and its dependent Reviews no longer need reproduction;
cleanup remains governed by Task 11.

The SHA, Conda version, and three mode producers are each captured by a plain
assignment-only simple command before a separate `test`. Under
`set -euo pipefail`, a nonzero producer status therefore terminates the
subshell before comparison and cannot be replaced by a successful `test`.

- [ ] **Step 3: Run quick/project/unit validation**

Run exactly from the Router root:

```bash
(
set -euo pipefail
/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-quick-validate-r1/bin/python /Users/elvis/.codex-account-a/skills/.system/skill-creator/scripts/quick_validate.py /Users/elvis/file/develop/opensource/openspec-superpower-change
PYTHONDONTWRITEBYTECODE=1 python3 /Users/elvis/file/develop/opensource/openspec-superpower-change/scripts/validate_core_gates.py /Users/elvis/file/develop/opensource/openspec-superpower-change
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s /Users/elvis/file/develop/opensource/openspec-superpower-change/tests -v
/private/tmp/add-role-first-review-routing-20260810-FPWT9V/conda-quick-validate-r1/bin/python /Users/elvis/.codex-account-a/skills/.system/skill-creator/scripts/quick_validate.py /Users/elvis/file/develop/opensource/codex-brief-antigravity-review
PYTHONDONTWRITEBYTECODE=1 python3 /Users/elvis/file/develop/opensource/codex-brief-antigravity-review/scripts/validate_templates.py /Users/elvis/file/develop/opensource/codex-brief-antigravity-review
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s /Users/elvis/file/develop/opensource/codex-brief-antigravity-review/tests -v
openspec validate add-role-first-review-routing --strict
openspec validate --all --strict --no-interactive
)
```

Expected: all eight commands exit `0`; unit tests report no failure/error,
OpenSpec reports `3 passed / 0 failed`, and each project validator prints its
documented success line. Only the two `quick_validate` commands use the bound
Conda interpreter; all project validators and unit tests deliberately remain on
the default `python3` to verify dependency-free fallback behavior. Any missing,
drifted, or non-executable Conda interpreter is `BLOCKED`; do not recreate it
implicitly inside this step or substitute another interpreter.
The control-plane executes this reviewed subshell as one block; `set -euo pipefail`
makes the first nonzero command stop the sequence. It must record that command
and result as `BLOCKED`; it must not continue to the next command.

- [ ] **Step 4: Run static and cross-skill checks**

Run these exact commands from the Router root:

```bash
! (rg -n -i 'schema-version-5|schema[ -]?5 handoff is current|three required targets|codex product alone (owns|decides)|codex alone (owns|decides)' \
  SKILL.md references README.md README_cn.md \
  | rg -v -i 'legacy|historical|history|frozen|audit|drain|reject|invalid|example of prohibited')
! (rg -n -i '(another agent|independent agent|another model).*(review|reviewer)' \
  SKILL.md references README.md README_cn.md \
  | rg -v -i 'reject|forbid|invalid|unresolved|prohibit|must name|不得|禁止|拒绝|未解析')
cmp -s references/handoff-contract.md /Users/elvis/file/develop/opensource/codex-brief-antigravity-review/references/handoff-contract.md
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_workflow_rules.WorkflowRulesTest.test_shared_handoff_contract_is_byte_identical \
  tests.test_workflow_rules.WorkflowRulesTest.test_shared_validator_core_is_byte_identical_when_companion_exists -v
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py audit \
  --openspec-source /Users/elvis/file/develop/opensource/openspec-superpower-change \
  --brief-source /Users/elvis/file/develop/opensource/codex-brief-antigravity-review \
  --report-paths-only
```

Expected: both negated pipelines exit `0` and emit no unallowlisted line; `cmp`
and both byte-identity tests exit `0`; audit exits `0` and its final stdout line
is exactly `0 sensitive categories found`. The negative-search policy allows
only lines explicitly labeled legacy/history/audit/drain or lines that reject a
generic destination; it does not allow current normative text, public behavior,
or templates to use the rejected phrases.

- [ ] **Step 5: Run GREEN forward tests**

Run exactly:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tests/run_role_first_review_forward_tests.py \
  --cases tests/fixtures/role-first-review-routing-cases.json \
  --output-schema tests/fixtures/role-first-review-routing-output.schema.json \
  --router-root /Users/elvis/file/develop/opensource/openspec-superpower-change \
  --companion-root /Users/elvis/file/develop/opensource/codex-brief-antigravity-review \
  --temporary-root /private/tmp/add-role-first-review-routing-20260810-FPWT9V/forward-run \
  --sanitized-summary /private/tmp/add-role-first-review-routing-20260810-FPWT9V/role-first-forward-summary.json
stat -f '%Lp %N' /private/tmp/add-role-first-review-routing-20260810-FPWT9V/role-first-forward-summary.json
```

Expected: runner exit `0` and stdout JSON has `forward: "pass"`,
`case_count: 6`, and the exact summary path; `stat` prints mode `600`. Copy only
the validated eight-field-per-case summary into durable evidence with its SHA.
The transient runner directory must contain no raw output when the command
returns; a cleanup or schema failure is `BLOCKED`.

- [ ] **Step 5A: Execute the independently reviewed R9 single-cache recovery**

Do not run this step until the complete R9 amendment Review has been persisted
at
`docs/design/reviews/2026-08-20-add-role-first-review-routing-evidence-rehydration-r9-review.md`,
its bound inputs have not drifted, and the original control plane has accepted
its verdict as `PASS`. Run the following exact command from the Router root.
It backs up the exact current bytes before using an exclusive same-filesystem
rename to remove only the reviewed generated cache from the source tree:

```bash
(
set -euo pipefail
umask 077
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 - <<'PY'
import ctypes
import hashlib
import json
import os
import stat
from pathlib import Path

SOURCE = Path("/Users/elvis/file/develop/opensource/openspec-superpower-change/scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc")
TRANSACTION_ROOT = Path("/private/tmp/add-role-first-review-routing-r9-r2-20260820-4hEfNB")
RECOVERY_ROOT = TRANSACTION_ROOT / "source-delta-recovery-r9"
BACKUP = RECOVERY_ROOT / "backup.pyc"
ORIGINAL = RECOVERY_ROOT / "original-object.pyc"
PREPARED = RECOVERY_ROOT / "prepared.json"
VERIFIED = RECOVERY_ROOT / "verified.json"
EXPECTED_SHA256 = "5b7cd72df71d308929c08fb6ae047403b4374e1824a13f479e5034f468dfff49"
SOURCE_START_SHA256 = "425e7753b96e7cca2ad645d9a5385e52532e83dd19540ecb7d11ba3adb768c66"
EXPECTED_SIZE = 168579
EXPECTED_SOURCE_MODE = 0o644
EXPECTED_SOURCE_DEVICE = 16777233
EXPECTED_SOURCE_INODE = 170846033
EXPECTED_SOURCE_NLINK = 1
EXPECTED_SOURCE_UID = 501
EXPECTED_SOURCE_GID = 20
EXPECTED_SOURCE_PARENT_MODE = 0o755
EXPECTED_SOURCE_PARENT_DEVICE = 16777233
EXPECTED_SOURCE_PARENT_INODE = 163934412
EXPECTED_SOURCE_PARENT_UID = 501
EXPECTED_SOURCE_PARENT_GID = 20
RENAME_EXCL = 0x00000004


def fsync_dir(path: Path) -> None:
    fd = os.open(str(path), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def sha256_fd(fd: int) -> str:
    os.lseek(fd, 0, os.SEEK_SET)
    digest = hashlib.sha256()
    while True:
        chunk = os.read(fd, 1024 * 1024)
        if not chunk:
            break
        digest.update(chunk)
    return digest.hexdigest()


def validate_source_parent_fd(fd: int) -> os.stat_result:
    opened = os.fstat(fd)
    linked = os.lstat(SOURCE.parent)
    expected = (
        EXPECTED_SOURCE_PARENT_DEVICE,
        EXPECTED_SOURCE_PARENT_INODE,
        EXPECTED_SOURCE_PARENT_MODE,
        EXPECTED_SOURCE_PARENT_UID,
        EXPECTED_SOURCE_PARENT_GID,
    )
    for current in (opened, linked):
        actual = (
            current.st_dev,
            current.st_ino,
            stat.S_IMODE(current.st_mode),
            current.st_uid,
            current.st_gid,
        )
        if not stat.S_ISDIR(current.st_mode) or actual != expected:
            raise RuntimeError("source parent identity or mode drift")
    return opened


def open_exact_regular(
    path: Path,
    allowed_modes: set[int],
    require_source_identity: bool = False,
) -> tuple[int, os.stat_result]:
    fd = os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW)
    try:
        before = os.fstat(fd)
        linked = os.lstat(path)
        if not stat.S_ISREG(before.st_mode):
            raise RuntimeError(f"not a regular file: {path}")
        if (before.st_dev, before.st_ino) != (linked.st_dev, linked.st_ino):
            raise RuntimeError(f"path/fd identity mismatch: {path}")
        if stat.S_IMODE(before.st_mode) not in allowed_modes:
            raise RuntimeError(f"unexpected mode: {path}")
        if before.st_size != EXPECTED_SIZE:
            raise RuntimeError(f"unexpected size: {path}")
        if require_source_identity and (
            before.st_dev,
            before.st_ino,
            before.st_nlink,
            before.st_uid,
            before.st_gid,
        ) != (
            EXPECTED_SOURCE_DEVICE,
            EXPECTED_SOURCE_INODE,
            EXPECTED_SOURCE_NLINK,
            EXPECTED_SOURCE_UID,
            EXPECTED_SOURCE_GID,
        ):
            raise RuntimeError(f"unexpected reviewed object identity: {path}")
        if sha256_fd(fd) != EXPECTED_SHA256:
            raise RuntimeError(f"unexpected SHA-256: {path}")
        after = os.fstat(fd)
        linked_after = os.lstat(path)
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
        ):
            raise RuntimeError(f"file drift while reading: {path}")
        if (before.st_dev, before.st_ino) != (linked_after.st_dev, linked_after.st_ino):
            raise RuntimeError(f"path identity drift while reading: {path}")
        return fd, before
    except Exception:
        os.close(fd)
        raise


def canonical_json(payload: dict) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def write_exclusive(path: Path, payload: bytes) -> None:
    fd = os.open(
        str(path),
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
        0o600,
    )
    try:
        view = memoryview(payload)
        while view:
            written = os.write(fd, view)
            view = view[written:]
        os.fsync(fd)
    finally:
        os.close(fd)
    if stat.S_IMODE(os.lstat(path).st_mode) != 0o600:
        raise RuntimeError(f"unexpected evidence mode: {path}")


def require_exact_payload(path: Path, payload: bytes, durable: bool = False) -> None:
    access = os.O_RDWR if durable else os.O_RDONLY
    fd = os.open(str(path), access | os.O_NOFOLLOW)
    try:
        before = os.fstat(fd)
        linked = os.lstat(path)
        if (
            not stat.S_ISREG(before.st_mode)
            or stat.S_IMODE(before.st_mode) != 0o600
            or (before.st_dev, before.st_ino) != (linked.st_dev, linked.st_ino)
        ):
            raise RuntimeError(f"invalid evidence file: {path}")
        chunks = []
        while True:
            chunk = os.read(fd, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        if b"".join(chunks) != payload:
            raise RuntimeError(f"evidence mismatch: {path}")
        if durable:
            os.fsync(fd)
        after = os.fstat(fd)
        linked_after = os.lstat(path)
        if (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
        ) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
        ) or (before.st_dev, before.st_ino) != (
            linked_after.st_dev,
            linked_after.st_ino,
        ):
            raise RuntimeError(f"evidence drift while reading: {path}")
    finally:
        os.close(fd)


def copy_backup() -> None:
    source_fd, _ = open_exact_regular(
        SOURCE,
        {EXPECTED_SOURCE_MODE},
        require_source_identity=True,
    )
    try:
        os.lseek(source_fd, 0, os.SEEK_SET)
        backup_fd = os.open(
            str(BACKUP),
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
        )
        try:
            while True:
                chunk = os.read(source_fd, 1024 * 1024)
                if not chunk:
                    break
                view = memoryview(chunk)
                while view:
                    written = os.write(backup_fd, view)
                    view = view[written:]
            os.fsync(backup_fd)
        finally:
            os.close(backup_fd)
    finally:
        os.close(source_fd)
    backup_fd, _ = open_exact_regular(BACKUP, {0o600})
    os.close(backup_fd)
    fsync_dir(RECOVERY_ROOT)


def rename_exclusive(
    source_dir_fd: int,
    source_name: str,
    destination_dir_fd: int,
    destination_name: str,
) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    renameatx_np = libc.renameatx_np
    renameatx_np.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    renameatx_np.restype = ctypes.c_int
    result = renameatx_np(
        source_dir_fd,
        os.fsencode(source_name),
        destination_dir_fd,
        os.fsencode(destination_name),
        RENAME_EXCL,
    )
    if result != 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error), source_name, destination_name)


transaction_stat = os.lstat(TRANSACTION_ROOT)
if (
    not stat.S_ISDIR(transaction_stat.st_mode)
    or stat.S_IMODE(transaction_stat.st_mode) != 0o700
    or transaction_stat.st_uid != os.getuid()
):
    raise RuntimeError("transaction root must be a real mode-0700 directory")
source_parent_fd = os.open(
    str(SOURCE.parent),
    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
)
source_parent_stat = validate_source_parent_fd(source_parent_fd)
if source_parent_stat.st_dev != transaction_stat.st_dev:
    raise RuntimeError("source and recovery roots must be on the same filesystem")

if not os.path.lexists(RECOVERY_ROOT):
    source_fd, _ = open_exact_regular(
        SOURCE,
        {EXPECTED_SOURCE_MODE},
        require_source_identity=True,
    )
    os.close(source_fd)
    os.mkdir(RECOVERY_ROOT, 0o700)
    fsync_dir(TRANSACTION_ROOT)
recovery_stat = os.lstat(RECOVERY_ROOT)
if not stat.S_ISDIR(recovery_stat.st_mode) or stat.S_IMODE(recovery_stat.st_mode) != 0o700:
    raise RuntimeError("recovery root must be a real mode-0700 directory")
if recovery_stat.st_dev != source_parent_stat.st_dev:
    raise RuntimeError("recovery root filesystem drift")
recovery_fd = os.open(
    str(RECOVERY_ROOT),
    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
)
recovery_opened = os.fstat(recovery_fd)
if (recovery_opened.st_dev, recovery_opened.st_ino) != (
    recovery_stat.st_dev,
    recovery_stat.st_ino,
):
    raise RuntimeError("recovery root path/fd identity mismatch")
allowed_names = {BACKUP.name, ORIGINAL.name, PREPARED.name, VERIFIED.name}
if not set(os.listdir(RECOVERY_ROOT)).issubset(allowed_names):
    raise RuntimeError("unexpected recovery-root entry")

prepared_payload = canonical_json(
    {
        "backup_path": str(BACKUP),
        "change_id": "add-role-first-review-routing",
        "operation": "single-path-generated-cache-backup-and-remove",
        "original_object_path": str(ORIGINAL),
        "removal_mechanism": "renameatx_np:RENAME_EXCL",
        "schema_version": 1,
        "source_current_sha256": EXPECTED_SHA256,
        "source_mode": "0644",
        "source_path": str(SOURCE),
        "source_size": EXPECTED_SIZE,
        "source_start_sha256": SOURCE_START_SHA256,
    }
)
verified_payload = canonical_json(
    {
        "backup_sha256": EXPECTED_SHA256,
        "change_id": "add-role-first-review-routing",
        "original_object_sha256": EXPECTED_SHA256,
        "schema_version": 1,
        "source_absent": True,
        "source_path": str(SOURCE),
        "source_recovery": "pass",
    }
)

if os.path.lexists(BACKUP):
    backup_fd, _ = open_exact_regular(BACKUP, {0o600})
    try:
        os.fsync(backup_fd)
    finally:
        os.close(backup_fd)
    fsync_dir(RECOVERY_ROOT)
else:
    if not os.path.lexists(SOURCE) or os.path.lexists(ORIGINAL):
        raise RuntimeError("cannot create backup from the reviewed source state")
    copy_backup()

if os.path.lexists(PREPARED):
    require_exact_payload(PREPARED, prepared_payload, durable=True)
    os.fsync(recovery_fd)
else:
    if not os.path.lexists(SOURCE) or os.path.lexists(ORIGINAL):
        raise RuntimeError("cannot prepare the reviewed transaction state")
    write_exclusive(PREPARED, prepared_payload)
    fsync_dir(RECOVERY_ROOT)

if os.path.lexists(VERIFIED) and (
    os.path.lexists(SOURCE) or not os.path.lexists(ORIGINAL)
):
    raise RuntimeError("verified marker is inconsistent with the namespace state")

if os.path.lexists(ORIGINAL):
    if os.path.lexists(SOURCE):
        raise RuntimeError("source and moved original cannot coexist")
    original_fd, _ = open_exact_regular(
        ORIGINAL,
        {EXPECTED_SOURCE_MODE, 0o600},
        require_source_identity=True,
    )
    os.close(original_fd)
else:
    if not os.path.lexists(SOURCE):
        raise RuntimeError("source is absent without a recoverable moved original")
    source_fd, source_stat = open_exact_regular(
        SOURCE,
        {EXPECTED_SOURCE_MODE},
        require_source_identity=True,
    )
    try:
        validate_source_parent_fd(source_parent_fd)
        current_recovery = os.lstat(RECOVERY_ROOT)
        if (current_recovery.st_dev, current_recovery.st_ino) != (
            recovery_opened.st_dev,
            recovery_opened.st_ino,
        ) or stat.S_IMODE(current_recovery.st_mode) != 0o700:
            raise RuntimeError("recovery root identity or mode drift before rename")
        rename_exclusive(
            source_parent_fd,
            SOURCE.name,
            recovery_fd,
            ORIGINAL.name,
        )
        moved_stat = os.lstat(ORIGINAL)
        if (moved_stat.st_dev, moved_stat.st_ino) != (source_stat.st_dev, source_stat.st_ino):
            raise RuntimeError("moved-object identity mismatch")
    finally:
        os.close(source_fd)
    os.fsync(source_parent_fd)
    os.fsync(recovery_fd)

validate_source_parent_fd(source_parent_fd)
os.fsync(source_parent_fd)
os.fsync(recovery_fd)
original_fd, _ = open_exact_regular(
    ORIGINAL,
    {EXPECTED_SOURCE_MODE, 0o600},
    require_source_identity=True,
)
try:
    os.fchmod(original_fd, 0o600)
    os.fsync(original_fd)
finally:
    os.close(original_fd)
original_fd, _ = open_exact_regular(
    ORIGINAL,
    {0o600},
    require_source_identity=True,
)
os.close(original_fd)
if os.path.lexists(SOURCE):
    raise RuntimeError("source cache remains after exclusive move")
fsync_dir(RECOVERY_ROOT)

if os.path.lexists(VERIFIED):
    require_exact_payload(VERIFIED, verified_payload, durable=True)
else:
    write_exclusive(VERIFIED, verified_payload)
os.fsync(recovery_fd)
os.close(recovery_fd)
os.close(source_parent_fd)

print(
    json.dumps(
        {
            "backup_sha256": EXPECTED_SHA256,
            "source_absent": True,
            "source_cache_recovery": "pass",
            "source_path": str(SOURCE),
        },
        sort_keys=True,
        separators=(",", ":"),
    )
)
PY
)
```

Expected: the command exits `0`; the final stdout line contains
`"source_cache_recovery":"pass"`, the exact source path, the reviewed current
SHA, and `"source_absent":true`; recovery root mode is `0700`; `backup.pyc`,
`original-object.pyc`, `prepared.json`, and `verified.json` are regular,
no-follow mode-`0600` files; both byte objects have SHA-256
`5b7cd72df71d308929c08fb6ae047403b4374e1824a13f479e5034f468dfff49`;
and only the exact source cache path is absent. The source-start SHA is recorded
only as historical evidence and is never restored over the current bytes.

Any source SHA/size/mode/path drift, occupied unexpected recovery entry,
cross-filesystem layout, link/special file, backup mismatch, exclusive rename
failure, or `fsync` failure is `BLOCKED`. The command may resume only its own
exact, validated recovery-root states after interruption; it never overwrites,
unlinks, recursively removes, restores, or cleans another object. An ambiguous
state remains preserved for a separate reviewed disposition. Do not execute
Step 6 after any nonzero result.

- [ ] **Step 6: Recalculate complete source preimages/diff evidence without Git**

Run the Task 4 `source-delta` command against the R9 reconstructed source
baselines and the hash-bound exact allowlist. The reconstructed baselines roll
back exactly the 36 hash-proven file preimages and remove the three originally
absent forward-test paths; they deliberately freeze Plan/OpenSpec/evidence
history at the R9 Preflight boundary instead of pretending to reproduce the
missing historical source-start containers. The R9 current-tree backups,
preflight snapshots, provenance manifest, and independently reviewed continuity
record cover that frozen history. Use these exact commands from the Router
root:

```bash
umask 077
test ! -e /private/tmp/add-role-first-review-routing-r9-r2-20260820-4hEfNB/source-compare-r9
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py source-delta \
  --bindings /private/tmp/add-role-first-review-routing-r9-r2-20260820-4hEfNB/preflight-source-bindings-r9.json \
  --router-root /Users/elvis/file/develop/opensource/openspec-superpower-change \
  --companion-root /Users/elvis/file/develop/opensource/codex-brief-antigravity-review \
  --router-baseline /private/tmp/add-role-first-review-routing-r9-r2-20260820-4hEfNB/router-tree-reconstructed-source-baseline-r9.json \
  --companion-baseline /private/tmp/add-role-first-review-routing-r9-r2-20260820-4hEfNB/companion-tree-reconstructed-source-baseline-r9.json \
  --compare-root /private/tmp/add-role-first-review-routing-r9-r2-20260820-4hEfNB/source-compare-r9 \
  --output /private/tmp/add-role-first-review-routing-r9-r2-20260820-4hEfNB/source-delta-r9.json
stat -f '%Lp %N' \
  /private/tmp/add-role-first-review-routing-r9-r2-20260820-4hEfNB/source-compare-r9 \
  /private/tmp/add-role-first-review-routing-r9-r2-20260820-4hEfNB/source-delta-r9.json
```

Expected: `test` and `source-delta` exit `0`; stdout JSON has
`source_delta: "pass"` and `unexpected_paths: []`; `stat` reports compare-root
mode `700` and delta mode `600`. Every changed tree entry, including hidden
files, existing Review files, evidence and `tasks.md`, must be either unchanged
or named exactly in the bound allowlist. Both backups must pass SHA/member/type/
containment validation and safe exclusive extraction. Any unexpected path,
occupied compare root, archive mismatch, link/special member, or incomplete
source comparison is `BLOCKED`. Copy only relative path/status/SHA/mode records
to durable source evidence; never copy source contents or use the compare root
as restore authority.

### Task 7: Obtain candidate source High Review

**Files:**

- Create: Router `docs/design/reviews/2026-08-10-add-role-first-review-routing-source-review.md` only from the returned independent Review text.
- Update: evidence after findings are resolved.

- [ ] **Step 1: Prepare a full independent new-window Codex prompt**

Bind actual Router/Companion files, before/after hashes, complete non-Git diff reconstruction, validators/tests, forward summary, sensitive scan, and approved contract. Assignment is product `codex`, role `independent-reviewer`, profile `control-plane-high`, fresh user-opened instance distinct from authors/executors, purpose to decide whether runtime planning may begin, and implementation-evidence-only authority.

- [ ] **Step 2: Stop for the independent verdict**

Any actionable finding returns to the source slice for fix, fresh validation, and a new full Review revision. Only control-plane-accepted `PASS` permits runtime planning. Do not run Pi or mutate runtime while this gate is pending.

### Task 8: Drain old schemas and create/review the four-target sync plan

**Files:**

- Create: path/hash-only plan under the structured backup root, mode `0600`.
- Create: sanitized drain and sync-plan Review evidence under Router `docs/design/evidence/add-role-first-review-routing/` and `docs/design/reviews/`.
- Do not modify runtime in this task.

- [ ] **Step 1: Inventory every known canonical Handoff root**

Use the schema-6 validator's `--legacy-inventory-root` against all known Router/Companion/project roots. Persist only path, schema version, lifecycle, SHA-256, and drain status. Any active schema 4 or 5 is `BLOCKED` until it reaches `complete` under the pre-upgrade runtime; never migrate, abandon, rewrite, or resume it after cutover.

Run exactly from the Router root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py . \
  --legacy-inventory-root /Users/elvis/file/develop/opensource/openspec-superpower-change \
  --legacy-inventory-root /Users/elvis/file/develop/opensource/codex-brief-antigravity-review \
  --legacy-inventory-root /Users/elvis/file/develop/workspace/ai-app/ai_app \
  --legacy-inventory-output /private/tmp/add-role-first-review-routing-20260810-FPWT9V/legacy-drain.json
stat -f '%Lp %N' /private/tmp/add-role-first-review-routing-20260810-FPWT9V/legacy-drain.json
```

Expected: exit `0`; first stdout JSON has `legacy_audit: "pass"` and
`active_legacy_count: 0`; the final stdout line is the normal core-gates success
line; `stat` reports mode `600`. Any active record or any record key outside the
five sanitized fields blocks deployment. A completed record remains immutable
audit history and is not migrated or accepted as current evidence.

- [ ] **Step 2: Generate a fresh four-target plan**

Resolve and bind exact paths rather than inheriting process variables. Current
Preflight observed that `CODEX_HOME=/Users/elvis/.codex-account-a` does not
contain the governed Skills or `AGENTS.md`, while
`/Users/elvis/.agents/skills/{openspec-superpower-change,codex-brief-antigravity-review}`
are symlinks to the real `/Users/elvis/.codex/skills` targets. Therefore the
candidate plan uses:

- Codex: `/Users/elvis/.codex/skills`, `/Users/elvis/.codex/AGENTS.md`; preserve the `.agents/skills` symlinks without replacement.
- Pi: `${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}/skills`, `${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}/APPEND_SYSTEM.md`
- Antigravity: `${ANTIGRAVITY_CLI_HOME:-$HOME/.gemini/antigravity-cli}/skills`, `$HOME/.gemini/GEMINI.md`
- Grok: `${GROK_HOME:-$HOME/.grok}/skills`, `${GROK_HOME:-$HOME/.grok}/AGENTS.md`

The plan records only paths, modes, kinds, SHA-256 values, source mapping, managed v6 IDs/body hash, target order, backup root, and stop/restore conditions. It must not record global-rule contents or sensitive/native configuration.

Generate it with this exact command from the Router root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py plan \
  --manifest references/cross-cli-portable-manifest.json \
  --openspec-source /Users/elvis/file/develop/opensource/openspec-superpower-change \
  --brief-source /Users/elvis/file/develop/opensource/codex-brief-antigravity-review \
  --codex-skills-root /Users/elvis/.codex/skills \
  --codex-rule-file /Users/elvis/.codex/AGENTS.md \
  --pi-skills-root /Users/elvis/.pi/agent/skills \
  --pi-rule-file /Users/elvis/.pi/agent/APPEND_SYSTEM.md \
  --antigravity-skills-root /Users/elvis/.gemini/antigravity-cli/skills \
  --antigravity-rule-file /Users/elvis/.gemini/GEMINI.md \
  --grok-skills-root /Users/elvis/.grok/skills \
  --grok-rule-file /Users/elvis/.grok/AGENTS.md \
  --output /private/tmp/add-role-first-review-routing-20260810-FPWT9V/runtime-sync-plan.json
stat -f '%Lp %N' /private/tmp/add-role-first-review-routing-20260810-FPWT9V/runtime-sync-plan.json
```

Expected: exit `0`; stdout is JSON with `plan: "pass"` and the exact absolute
output path; `stat` reports mode `600`. The plan's target order is exactly
`["codex", "pi", "antigravity-cli", "grok-cli"]`, every source/destination
preimage matches the fresh source Review state, and the Pi native file's
contents are not embedded. Recalculate and record the plan SHA before Review.

- [ ] **Step 3: Obtain independent Sync-plan Review**

Use product `codex`, role `independent-reviewer`, profile `control-plane-high`, fresh instance distinct from plan author/target executor, purpose covering roots/preimages/isolation/closure/backup/restore/exclusions/order/stop conditions, and sync-plan-evidence-only authority. Only accepted `PASS` authorizes apply.

### Task 9: Apply and verify four targets one at a time

**Files:**

- Runtime targets exactly as bound by the reviewed plan.
- Evidence under Router `docs/design/evidence/add-role-first-review-routing/`.

- [ ] **Step 1: Repeat legacy drain and all destination preimage guards**

Immediately before the first apply, require zero active schema-4/schema-5 contracts and exact plan/source/destination SHA matches. Drift is `BLOCKED` and requires a new plan Review.

Repeat the exact Task 8 legacy-inventory command, writing
`legacy-drain-preapply.json`, then run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py verify-prestate \
  --target all \
  --plan /private/tmp/add-role-first-review-routing-20260810-FPWT9V/runtime-sync-plan.json
```

Expected: exit `0` and stdout JSON exactly identifies `prestate: "pass"` with
targets in reviewed order. Any plan/source/destination hash, mode, type, root,
symlink, managed marker, legacy drain, or backup-root drift returns exit 1 and
requires a new path/hash plan plus a fresh Sync-plan Review.

- [ ] **Step 2: Apply Codex, then Pi, then Antigravity, then Grok**

For each target: create and fully fsync a fresh mode-`0600` target-local backup
outside discovery roots, durably install the `prepared` receipt, durably advance
it to `mutation-intent`, atomically apply only manifest paths and the managed
block, run portable parity, managed v6 semantic/body parity, target-compatible
validators, and discovery, then advance. A handled failure from `prepared`
onward restores only the current target, verifies its reviewed preimage, stops
all later targets, and records owner/resume condition. A hard interruption is
handled only by the reviewed `recover-pending` restart gate; it never resumes
forward mutation in the recovery invocation.

Use this exact transaction sequence from the Router root. The helper contains
the complete reviewed restore invocation; it always returns nonzero after a
successful restore so `set -e` stops before the next target:

```bash
set -e
ROLE_SYNC_PLAN=/private/tmp/add-role-first-review-routing-20260810-FPWT9V/runtime-sync-plan.json
ROLE_BACKUP_ROOT=/private/tmp/add-role-first-review-routing-20260810-FPWT9V/runtime-backups
ROLE_RECEIPT_ROOT=/private/tmp/add-role-first-review-routing-20260810-FPWT9V/runtime-transactions
if test -e "$ROLE_BACKUP_ROOT" || test -e "$ROLE_RECEIPT_ROOT"; then
  if PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py recover-pending \
    --plan "$ROLE_SYNC_PLAN" \
    --backup-root "$ROLE_BACKUP_ROOT" \
    --transaction-root "$ROLE_RECEIPT_ROOT"; then
    echo 'recover-pending unexpectedly returned success' >&2
  fi
  exit 1
fi
test ! -e "$ROLE_BACKUP_ROOT"
test ! -e "$ROLE_RECEIPT_ROOT"
mkdir -m 700 "$ROLE_RECEIPT_ROOT"

restore_and_stop() {
  role_target="$1"
  role_receipt="$2"
  PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py restore-target \
    --target "$role_target" \
    --plan "$ROLE_SYNC_PLAN" \
    --backup-root "$ROLE_BACKUP_ROOT" \
    --transaction-receipt "$role_receipt"
  return 1
}

ROLE_RECEIPT="$ROLE_RECEIPT_ROOT/codex.json"
test ! -e "$ROLE_RECEIPT"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py apply \
  --target codex --plan "$ROLE_SYNC_PLAN" --backup-root "$ROLE_BACKUP_ROOT" \
  --transaction-receipt "$ROLE_RECEIPT"
if ! PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py verify \
  --target codex --plan "$ROLE_SYNC_PLAN" --transaction-receipt "$ROLE_RECEIPT"; then
  restore_and_stop codex "$ROLE_RECEIPT"
fi
if ! PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py verify-discovery \
  --target codex --plan "$ROLE_SYNC_PLAN" --transaction-receipt "$ROLE_RECEIPT"; then
  restore_and_stop codex "$ROLE_RECEIPT"
fi
if ! PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py commit-target \
  --target codex --plan "$ROLE_SYNC_PLAN" --transaction-receipt "$ROLE_RECEIPT"; then
  restore_and_stop codex "$ROLE_RECEIPT"
fi

ROLE_RECEIPT="$ROLE_RECEIPT_ROOT/pi.json"
test ! -e "$ROLE_RECEIPT"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py apply \
  --target pi --plan "$ROLE_SYNC_PLAN" --backup-root "$ROLE_BACKUP_ROOT" \
  --transaction-receipt "$ROLE_RECEIPT"
if ! PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py verify \
  --target pi --plan "$ROLE_SYNC_PLAN" --transaction-receipt "$ROLE_RECEIPT"; then
  restore_and_stop pi "$ROLE_RECEIPT"
fi
if ! PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py verify-discovery \
  --target pi --plan "$ROLE_SYNC_PLAN" --transaction-receipt "$ROLE_RECEIPT"; then
  restore_and_stop pi "$ROLE_RECEIPT"
fi
if ! PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py commit-target \
  --target pi --plan "$ROLE_SYNC_PLAN" --transaction-receipt "$ROLE_RECEIPT"; then
  restore_and_stop pi "$ROLE_RECEIPT"
fi

ROLE_RECEIPT="$ROLE_RECEIPT_ROOT/antigravity-cli.json"
test ! -e "$ROLE_RECEIPT"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py apply \
  --target antigravity-cli --plan "$ROLE_SYNC_PLAN" --backup-root "$ROLE_BACKUP_ROOT" \
  --transaction-receipt "$ROLE_RECEIPT"
if ! PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py verify \
  --target antigravity-cli --plan "$ROLE_SYNC_PLAN" --transaction-receipt "$ROLE_RECEIPT"; then
  restore_and_stop antigravity-cli "$ROLE_RECEIPT"
fi
if ! PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py verify-discovery \
  --target antigravity-cli --plan "$ROLE_SYNC_PLAN" --transaction-receipt "$ROLE_RECEIPT"; then
  restore_and_stop antigravity-cli "$ROLE_RECEIPT"
fi
if ! PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py commit-target \
  --target antigravity-cli --plan "$ROLE_SYNC_PLAN" --transaction-receipt "$ROLE_RECEIPT"; then
  restore_and_stop antigravity-cli "$ROLE_RECEIPT"
fi

ROLE_RECEIPT="$ROLE_RECEIPT_ROOT/grok-cli.json"
test ! -e "$ROLE_RECEIPT"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py apply \
  --target grok-cli --plan "$ROLE_SYNC_PLAN" --backup-root "$ROLE_BACKUP_ROOT" \
  --transaction-receipt "$ROLE_RECEIPT"
if ! PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py verify \
  --target grok-cli --plan "$ROLE_SYNC_PLAN" --transaction-receipt "$ROLE_RECEIPT"; then
  restore_and_stop grok-cli "$ROLE_RECEIPT"
fi
umask 077
if ! /Users/elvis/.local/bin/grok inspect --json \
  > /private/tmp/add-role-first-review-routing-20260810-FPWT9V/grok-inspect.json; then
  restore_and_stop grok-cli "$ROLE_RECEIPT"
fi
if ! PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py verify-discovery \
  --target grok-cli \
  --inspect-json /private/tmp/add-role-first-review-routing-20260810-FPWT9V/grok-inspect.json \
  --consume --plan "$ROLE_SYNC_PLAN" --transaction-receipt "$ROLE_RECEIPT"; then
  restore_and_stop grok-cli "$ROLE_RECEIPT"
fi
if ! PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py commit-target \
  --target grok-cli --plan "$ROLE_SYNC_PLAN" --transaction-receipt "$ROLE_RECEIPT"; then
  restore_and_stop grok-cli "$ROLE_RECEIPT"
fi
```

Expected for every successful `apply`: exit `0`, JSON `apply: "pass"`, exact
target, a positive backup count, and an `applied-uncommitted` mode-`0600`
receipt whose history proves `prepared` and `mutation-intent` were each fsynced
before the first destination mutation; target-local backup objects and manifest
are regular mode `0600` and were re-hashed before `prepared`. Every
`verify`/`verify-discovery` records its digest in that receipt, Grok discovery
consumes its mode-`0600` inspect artifact, and `commit-target` returns
`commit: "pass"` only after both digests exist. Any handled failure from
`prepared` onward executes the exact target-local recovery rules; any
post-apply verify, discovery, or commit failure executes the exact
`restore-target`, verifies the reviewed preimage, returns nonzero, and stops
before later targets. A hard interruption is discovered on restart by the
exact `recover-pending` command; it restores or reports `recovery-blocked`,
always returns nonzero, and never starts or resumes a later target. A failure
before durable `prepared` must leave the destination at its exact reviewed
preimage and leave any orphaned transaction material as blocking evidence.
Do not invoke a broad restore, reuse another target's backup, delete recovery
evidence, or proceed from `prepared`/`mutation-intent`/
`applied-uncommitted`/`restored`/`recovery-blocked`.

- [ ] **Step 3: Run verify-all**

Require all four required targets, both Skills' portable closure, exact v6 markers/IDs/body, and compatible discovery. Missing/stale/unverified Pi or any other required target is `BLOCKED`.

Run exactly:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py verify-all \
  --plan /private/tmp/add-role-first-review-routing-20260810-FPWT9V/runtime-sync-plan.json \
  --transaction-root /private/tmp/add-role-first-review-routing-20260810-FPWT9V/runtime-transactions
```

Expected: exit `0`; stdout JSON has `verify_all: "pass"` and exact sorted target
IDs `["antigravity-cli", "codex", "grok-cli", "pi"]`. Any missing target,
portable mismatch, v6 semantic/body mismatch, discovery failure, or stale
preimage returns exit 1 and blocks canonical progression.

### Task 10: Obtain the Pi adversarial Review

**Files:**

- Create: sanitized Pi Review evidence under Router `docs/design/reviews/`.

- [ ] **Step 1: Start only a fresh isolated Pi reviewer session**

Use temporary `HOME` and `PI_CODING_AGENT_DIR`, explicit candidate Skill paths, no inherited sessions/context/Skills, read-only tools, network denial, and an enforceable native-root deny profile. Reviewer is product `pi`, role `independent-reviewer`, profile `control-plane-high`, session distinct from every Pi executor/author, purpose to adversarially decide role parity/assignment/isolation/four-target findings, and governed-evidence-only authority.

First create the complete standalone prompt at
`docs/design/evidence/add-role-first-review-routing/2026-08-10-pi-adversarial-review-prompt.md`
using the defined six-field assignment, exact candidate source/evidence hashes,
the reviewed sync-plan hash, and the allowed read roots. Record its SHA. Confirm
that `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/pi-review-01`
does not exist; an occupied path is `BLOCKED`, not a cleanup authorization.
Then run exactly from the Router root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_cross_cli_sync.py probe-pi \
  --pi-executable /Users/elvis/.local/bin/pi \
  --native-pi-root /Users/elvis/.pi/agent \
  --temporary-root /private/tmp/add-role-first-review-routing-20260810-FPWT9V/pi-review-01 \
  --prompt-file docs/design/evidence/add-role-first-review-routing/2026-08-10-pi-adversarial-review-prompt.md \
  --read-root /Users/elvis/file/develop/opensource/openspec-superpower-change \
  --read-root /Users/elvis/file/develop/opensource/codex-brief-antigravity-review \
  --output /private/tmp/add-role-first-review-routing-20260810-FPWT9V/pi-adversarial-review.json
stat -f '%Lp %N' /private/tmp/add-role-first-review-routing-20260810-FPWT9V/pi-adversarial-review.json
```

Expected: wrapper exit `0`; stdout JSON has `pi_probe: "pass"`,
`native_root_denied: true`, `network_denied: true`, and the exact output path;
`stat` reports `600`. The inner Pi command is exactly the Task 4 argv and may
read only the two candidate roots. Any unsupported flag/version, sandbox or
read-root ambiguity, native-root access attempt, network access, unrecognized
output field, or inability to prove isolation returns `BLOCKED`; do not run
`pi --help`, `pi --version`, or a native-root fallback.

- [ ] **Step 2: Accept only sanitized complete findings**

Persist reviewer identity/category, input hashes, command category, result, and complete findings without credentials, session content, settings, debug traces, or native-root contents. Pi cannot mutate runtime, accept its own result, update canonical state, or declare completion. Any actionable finding returns to fix/verify/Review.

### Task 11: Learning, fresh final verification, final Review, and closeout

**Files:**

- Modify/create only the project learning, OpenSpec task, evidence, Review, and archive artifacts required by the Completion Contract.

- [ ] **Step 1: Run Project Learning Closeout and Learning Review**

Audit the full correction history. Promote only confirmed non-sensitive invariants; prefer deterministic validators/tests over prose. Obtain the defined fresh Codex Learning Review before final verification.

- [ ] **Step 2: Run fresh final verification after the last mutation**

Repeat both repository quick validators/project validators/unit suites, OpenSpec strict/all validation, source negative searches/sensitive audit, shared-byte checks, six forward cases, four-target parity/managed semantics/discovery, and legacy drain. Persist command, result, artifact hashes, and freshness boundary.

- [ ] **Step 3: Obtain Final High Review**

Use a user-opened new-window Codex distinct from authors, executors, and bound decision owner. Bind the complete actual source/runtime/evidence revision, final commands, residuals, task/plan reconciliation, and completion claims. Result authority is final-Review evidence only.

- [ ] **Step 4: Reconcile and archive only when permitted**

Update OpenSpec checkboxes only from accepted evidence, reconcile every plan checkbox, update the base spec through ordinary OpenSpec archive semantics, archive only after Final High Review `PASS`, then run post-archive strict validation and preserve its receipt. Do not update workbench canonical state or issue an Envelope unless separately authorized.

- [ ] **Step 5: Cleanup only with exact safe authority**

After every gate is closed and rollback/investigation is no longer needed, inventory the exact temporary backup paths, prove containment/non-symlink identity, and request/verify any separately required cleanup authority. Never run destructive Git or broad recursive cleanup. Git/publication remains unrequested and out of scope.

---

## OpenSpec traceability

| Approved requirement/scenario group | Plan coverage |
|---|---|
| Explicit role-first reviewer assignment: generic request, nonblank purpose, selected Pi preservation, same-instance rejection, advisory authority, unavailable reviewer | Tasks 1, 3, and 5 RED/GREEN/static/natural forward cases |
| Schema-6 governed Reviewer Assignment: exact standard/strict and compact shapes, malformed/extended rejection, readonly transition, canonical-SHA evidence binding, old-shape rejection, non-authorizing legacy audit | Tasks 1 and 2 validator/evidence/transition implementation plus Task 7 source High Review |
| Codex-primary auxiliary collaboration: separated Review, unavailable reviewer, self-review/impersonation, unknown owner, product-name authority rejection, PASS cannot complete, correction loop, active legacy blocker | Tasks 1–3, Task 7, Task 8 drain, Task 10 Pi Review, and Task 11 final owner decision |
| Four-runtime synchronization: all targets required, isolated Pi probe, unavailable/not-applicable distinction, repository-only trigger | Task 4 manifest/CLI/probe tests and Tasks 8–9 reviewed runtime transaction |
| Safe semantic global-rule alignment: native-byte preservation, full v6 semantics, portable parity, sensitive exclusion, unsafe path | Task 4 semantic/path/restore tests, Task 6 sensitive/static validation, and Tasks 8–9 plan/apply/verify |
| Frozen schema-5 identity: active drain, Pi rejection in schema 5 and schema 4/1, immutable complete history, product substitution, schema-6 evidence impersonation, repeated no-active-old-schema proof | Tasks 1–2 current/legacy branches, Task 3 product preservation, and Tasks 8–9 drain/preimage gates |

## Plan self-review checklist

- Contract coverage: all 2 added requirements, 4 modified requirements, and 39 approved scenarios map to Tasks 1–11.
- Current/legacy boundary: schema 6 is the sole current discriminator; schema 4/5 are audit/drain only and never current authority.
- Reviewer Assignment: purpose, product, instance, role, profile, independence, and result authority are exact and immutable.
- Pi safety: native target validation never invokes Pi; any optional Pi process runs only after its gate in isolated temporary roots with native-root denial.
- Runtime safety: source High Review precedes sync planning; sync-plan Review precedes target apply; per-target restore stops later targets.
- Git authority: no Git mutation or publication is authorized; R9 contains only
  ten exact read-only object-byte extractions after a fresh backup, records the
  earlier diagnostic deviation, and grants those bytes evidence provenance
  rather than repository authority.
- Scope: only the explicit file map, evidence/Review paths, later runtime plan targets, task reconciliation, and permitted archive projection may change.
- Completion: no source/runtime/Review PASS is whole-task completion; fresh final verification and Final High Review remain distinct gates.
