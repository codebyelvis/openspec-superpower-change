# Codex Skill Update 6.4 Blocker Resolution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (recommended) or superpowers:subagent-driven-development to execute this plan task-by-task. This plan is evidence recovery only and does not authorize schedule, runtime, discovery, Git, or cleanup mutation.

**Goal:** Resolve the Task 6.4 evidence blockers by reconciling the registry's multi-root discovery graph, proving the rollback adapter behavior in isolated fixtures, and obtaining a fresh process verification without changing managed state.

**Architecture:** Treat the installed registry as authoritative data: Router, Companion, and Superpowers use the shared `/Users/elvis/.codex` effective roots, while the optional updater uses the content-addressed `account-a` runtime discovery root. First perform a read-only identity and projection reconciliation. Then run the existing fake-launchd and receipt-bound rollback tests in the sibling source repository. Finally run one fresh Codex process with an explicit account/root declaration and require it to report any cross-root discovery limitation instead of guessing. No live LaunchAgent, discovery symlink, registry, state root, source tree, or Git ref is changed.

**Tech Stack:** macOS `launchctl print`, Codex CLI `0.147.0`, Python 3.11 `unittest`, content-addressed JSON evidence, OpenSpec `add-codex-skill-update`, and the existing `FakeLaunchdAdapter` test fixture.

---

## Gate 0 and authority

- Authoritative OpenSpec change worktree:
  `/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update-v2`.
- OpenSpec change:
  `/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update-v2/openspec/changes/add-codex-skill-update/`.
- Approved Major manifest SHA-256:
  `dfbf263e10ae0d9123b3045f6e250b4bfe9bbf3b4d0740f6a1393544db11de0c`.
- Approved raw artifact SHA-256 set: proposal
  `c930ba72173c9fdf5ec398a9d5d8e8b0b15c413f856e78f5c37bf85df3f72efd`,
  design `b32dae387a1a6f7e3d5a4159823250773264b0707d1e2e903f8072da6aba848a`,
  spec `251b794e7d814ada345e65c68ce80e20f61f08881e218a79e79b5347e5905585`,
  and tasks `557e23d31a77a5ebab1edd0c41e75dfb4cb6374e044c80eeff2fee0e718620c7`.
- Current checklist-bearing `tasks.md` SHA-256:
  `bea9d48ec0a2b83cc7e92e4efc06d479a8e61be324084b876961009fc9665758`.
  It is accepted only as a checklist-normalized successor of the approved raw
  tasks artifact; any contract-bearing drift is `BLOCKED`.
- Plan host path:
  `/Users/elvis/file/develop/opensource/openspec-superpower-change/docs/superpowers/plans/2026-08-06-codex-skill-update-6-4-blocker-resolution.md`.
  The plan host's stale `main`-worktree OpenSpec copy is neither the approved
  contract source nor an execution evidence sink.
- Approved contract item: `tasks.md` Task 6.4, fresh process/discovery verification for all four managed packages and every mapped entry/projection, plus a tested rollback instruction.
- Mode: approved implementation evidence recovery; no OpenSpec contract delta is proposed.
- Risk profile: strict, because this touches deployment evidence, discovery identity, schedule rollback evidence, and cross-account runtime interpretation.
- Control-plane owner: the Codex control-plane instance that receives the
  user's exact execution approval for this plan revision. External fresh Codex
  output is evidence only and cannot promote 6.4 by itself.
- User decision required before execution: approval of this plan, creation of
  only the three allowlisted evidence files in the authoritative v2 worktree,
  and one fresh model invocation. The plan does not grant permission to run
  `audit`, `plan`, `verify`, `launchctl bootstrap`, `launchctl load`,
  `launchctl kickstart`, any schedule mutation, any discovery switch, any
  cleanup, or any Git mutation. Read-only `git status --short --branch` is
  allowed for the Task 1 baseline and Task 4 no-drift checks only.

## Current evidence and blockers

The plan starts from these already observed, content-addressed records:

- Registry: `/Users/elvis/.codex-account-a/skill-update/registry.json`, SHA-256 `bc272c3391fe41a5a9d76c10f0533ce5196185d27ce052c043d598f51a34bae1`.
- Audit bindings: `/Users/elvis/.codex-account-a/skill-update/audit-bindings.json`, SHA-256 `5020a34c0e4642b16d04abb23a43267da10a3159c00fb80184d875612fb925d3`.
- Latest scheduled report: `/Users/elvis/.codex-account-a/skill-update/reports/93c12131233f027e1073ba51716395359d84b78f3bcee44fab45dd7cb9422ff5.json`.
- Schedule receipt: `/Users/elvis/.codex-account-a/skill-update/receipts/7a9439a4e5388387815f7092e1ababe70ee4beb6cd6d08073c4bda0882770175.json`, `transaction_result=SUCCEEDED`.
- Schedule binding: `/Users/elvis/.codex-account-a/skill-update/bindings/schedule-execution.json`, inner `binding_sha256=35705b61361a0b72da593a11264567935e91945192d519f319296d87492e666a`.
- Fresh verifier result at `2026-08-06T09:48:55Z`: `BLOCKED` because the quota-bearing process used `account-wb`, account-a automatic discovery was not proven, and no post-success rollback receipt/test existed.

The known package observations remain data, not permission to mutate:

- `companion`: `UPDATE_AVAILABLE`, `ELIGIBLE`, `SUCCEEDED`.
- `router`: `UPDATE_AVAILABLE`, `ELIGIBLE`, `SUCCEEDED`.
- `superpowers`: `UNKNOWN`, `BLOCKED_ADAPTER_BINDING_INCOMPLETE`, `BLOCKED`.
- `updater`: `UPDATE_AVAILABLE`, `DIVERGED`, `BLOCKED_DIVERGED`, `BLOCKED`.

## Scope and non-goals

Allowed read or test targets:

- Authoritative change/evidence worktree:
  `/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update-v2`.
- Plan host repository, read-only during execution:
  `/Users/elvis/file/develop/opensource/openspec-superpower-change`.
- Managed registry and evidence: `/Users/elvis/.codex-account-a/skill-update`.
- Shared effective discovery roots: `/Users/elvis/.codex/skills` and `/Users/elvis/.codex/superpowers`.
- Account-a updater discovery and immutable release: `/Users/elvis/.codex-account-a/skills/codex-skill-update` and its content-addressed release.
- Quota-bearing fresh-process home: `/Users/elvis/.codex-account-wb`.
- Reviewed source test repository: `/Users/elvis/file/develop/opensource/codex-skill-update`.

Explicit non-goals:

- Do not copy Router, Companion, or Superpowers into `account-a`.
- Do not copy the updater into `account-wb` or the shared `.codex` root.
- Do not switch or replace any discovery symlink.
- Do not write any runtime state-root audit report, receipt, plan, registry, binding, lease, journal, plist, or notification. The only execution-time writes allowed are the three sanitized evidence files defined below.
- Do not invoke updater `audit`, `plan`, or `verify` commands.
- Do not execute `launchctl bootstrap`, `load`, `kickstart`, `bootout`, or any real rollback.
- Do not run `git add`, `commit`, `reset`, `clean`, `push`, or alter any ref/worktree.
- Do not delete or clean the absent candidate, retained compensation, immutable release, debug trace, or any other material.

## Durable evidence and task handoff

The control plane must persist sanitized, canonical JSON evidence in the repository so that Task 2, Task 3, and the final 6.4 review have a durable chain. The allowed evidence root is:

`/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update-v2/docs/design/evidence/add-codex-skill-update/`

The only execution-time files permitted by this plan are these no-replace artifacts:

1. `2026-08-06-task-6.4-rollback-test-evidence.json`
2. `2026-08-06-task-6.4-fresh-process-evidence.json`
3. `2026-08-06-task-6.4-blocker-resolution-evidence.json`

The control plane writes each artifact atomically only after the corresponding task completes. Each artifact is canonical JSON and contains, at minimum, `schema`, `kind`, the computed `plan_sha256`, `generated_at`, `result`, `commands` with exact argument arrays, working directory, exit code, and sanitized result, plus the task-specific evidence, `blocker_owner`, and `resume_condition`. A child artifact records its parent artifact path and SHA-256; the final artifact additionally contains the SHA-256 of the Task 2 and Task 3 artifacts and the final decision. An artifact does not contain a self-referential hash: its file SHA-256 is computed after the atomic write and recorded by its child or in the control-plane response. Dynamic values are computed at execution time; the plan contains no literal placeholder values.

Every artifact write is bound to the reviewed sibling source module
`/Users/elvis/file/develop/opensource/codex-skill-update/scripts/codex_skill_update.py`,
whose pre-execution SHA-256 must equal
`6da49b5c93a2cc209f5e54dae51d04eaef06d7009b9d852029db635e7d2c90fe`.
The control plane invokes `/opt/anaconda3/bin/python3.11` with `-B -I -S`, loads
that absolute module with `importlib.util.spec_from_file_location`, serializes
the in-memory record with `canonical_json()`, opens the already-existing
evidence parent with `_dir_anchor()`, and calls `_write_no_replace_at()` with
mode `0o600`. It then reads the file through `_read_canonical_record()`, compares
the returned record with the in-memory record, and computes the file SHA-256.
Do not call `_write_no_replace()`: that higher-level helper requires a private
`0700` parent, while this repository evidence directory intentionally keeps its
existing worktree mode. Source hash drift, an existing filename, a symlink or
identity mismatch, non-canonical bytes, short write, fsync failure, read-back
mismatch, or bytecode creation is `BLOCKED_EVIDENCE_WRITE`; do not fall back to
shell redirection, truncate/replace, or a second filename.

Raw Codex prompts, model transcripts, environment dumps, credentials, session identifiers, and unredacted command output must not be copied into these files. Existing runtime state-root artifacts and pre-existing repository files, including any bytecode residue, are not modified or cleaned by this plan. A failed or blocked task still writes its sanitized artifact before the control plane stops, unless the evidence root itself is unavailable; that unavailability is a blocker.

Task 3 may start only after the Task 2 artifact exists, parses as canonical JSON, has a freshly computed SHA-256, and has `result=PASS`. If Task 2 is not `PASS`, no fresh process is invoked; the control plane writes the Task 3 artifact with `result=BLOCKED`, `fresh_process=NOT_RUN`, the Task 2 dependency result, blocker owner, and resume condition. Task 4 may start only after the Task 3 artifact exists and is hash-linked. The final artifact is the durable input for the later 6.6 review; chat output alone is not completion evidence.

## Discovery evidence contract

For every registry package, mapped entry, and projection, discovery evidence must compare the exact registry-bound effective path with the path observed by the fresh process. The comparison record must include:

- package or projection identifier;
- registry-bound effective path;
- observed discovered path and its `CODEX_HOME`/process root;
- symlink/readlink result and resolved target, where applicable;
- entry or payload fingerprint/tree fingerprint;
- `identity_equal`, which is true only when path identity and content identity match the registry-bound record; and
- a discovery classification.

`AUTO_DISCOVERY_PASS` is valid only when the fresh process reports the exact registry-bound path and matching identity. Direct inspection by an explicitly supplied path is `DIRECT_PATH_ONLY`, not automatic discovery. A same-name skill found under another `CODEX_HOME` or root is `NAME_ONLY_COLLISION` and cannot satisfy the gate. A missing process-visible projection, unresolved path, or ambiguous duplicate is `BLOCKED_DISCOVERY_ROOT`. The control plane, not the external Codex process, applies these classifications and owns the final decision.

## Acceptance matrix

The plan is successful only if every applicable row is evidenced:

| Gate | Required result | Blocking result |
| --- | --- | --- |
| Registry root mapping | Every package, entry, and projection resolves to the exact registry-bound root without alias or containment drift | Any guessed root, duplicate source, account ambiguity, or hash drift |
| Fresh process | The process reports its own `CODEX_HOME`; every package, entry, and projection is classified by exact registry-bound path and identity; the updater's account-a discovery limitation or proof is explicit | `DIRECT_PATH_ONLY`, `NAME_ONLY_COLLISION`, an unproven cross-root claim, or any missing identity field |
| Rollback adapter | Receipt-bound rollback, hard-kill recovery, fake schedule removal, and failure restoration tests pass in isolated temporary fixtures | Any test failure, missing fake adapter, or test writes outside its temporary fixture |
| Production safety | `launchctl print`, plist, receipt, binding, payload lock, and managed state remain unchanged; only the three explicitly allowed repository evidence files may be added | Any managed-state mutation, unapproved command, or evidence write outside the allowlist |
| 6.4 decision | PASS only when all mapped entries/projections are verified and the rollback instruction is backed by passing isolated tests; known package `BLOCKED`/`DIVERGED` observations remain visible | Any unresolved discovery identity or rollback evidence gap remains `BLOCKED` |

## Task 1: Reconcile the registry-bound discovery graph

**Files:**
- Read: `/Users/elvis/.codex-account-a/skill-update/registry.json`
- Read: `/Users/elvis/.codex-account-a/skill-update/audit-bindings.json`
- Read: `/Users/elvis/.codex-account-a/skill-update/controller-state.json`
- Read: `/Users/elvis/.codex/skills/`
- Read: `/Users/elvis/.codex/superpowers/`
- Read: `/Users/elvis/.codex-account-a/skills/codex-skill-update`
- Modify: none

- [ ] **Step 1: Recompute the registry and binding hashes as data.**

Run from
`/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update-v2`:

```bash
jq -c '{entries,projections,groups,packages}' /Users/elvis/.codex-account-a/skill-update/registry.json
jq -c '[.packages[] | {package_id,effective:.effective.path,observed:.observed.path,channel:.channel.path}]' /Users/elvis/.codex-account-a/skill-update/audit-bindings.json
shasum -a 256 /Users/elvis/.codex-account-a/skill-update/registry.json /Users/elvis/.codex-account-a/skill-update/audit-bindings.json
jq -c '{registry_sha256,audit_bindings_sha256,major_manifest_sha256}' /Users/elvis/.codex-account-a/skill-update/controller-state.json
git -C /Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update-v2 status --short --branch
git -C /Users/elvis/file/develop/opensource/openspec-superpower-change status --short --branch
```

Expected result: the two file hashes match the installed controller state; the
effective paths are shared `.codex` for `companion`, `router`, and
`superpowers`, and account-a runtime discovery for `updater`. Retain both Git
status outputs as the no-drift baseline; do not normalize, stage, clean, or
otherwise alter either dirty worktree.

- [ ] **Step 2: Check each mapped entry and projection without invoking the updater.**

Run read-only `lstat`/`readlink`/tree inventory checks for the four effective paths and both declared projections. Record only path identity, type, mode, content/tree hash, and mapping result. For each record, retain the registry-bound path, observed path, resolved target, and exact identity comparison required by the Discovery evidence contract. Do not infer that an absent account-a Router or Companion path is a defect when the registry explicitly binds the shared `.codex` path.

Expected result: every declared mapping has one exact observed root; no unmanaged duplicate is adopted; the updater symlink resolves to the immutable `188f94b4f303965a03f07383e9c5ab733906cef39918255d86e679bf49a556fe/payload` release.

- [ ] **Step 3: Apply the identity decision gate.**

Use the following rule in the evidence record:

```text
The registry-bound effective path is authoritative for this verification.
Do not require all four packages to live below one CODEX_HOME.
"Discovered" means that the process reports the exact registry-bound path and
matching path/content identity; a skill name or direct file inspection is not
enough. A same-name skill under another CODEX_HOME is NAME_ONLY_COLLISION.
If a fresh process cannot discover the registry-bound updater projection, record
BLOCKED_DISCOVERY_ROOT and stop. Do not repair the projection in this plan.
```

Expected result: either `DISCOVERY_GRAPH_PASS` with the split roots explicitly recorded, or `BLOCKED_DISCOVERY_ROOT` with a new runtime discovery-switch plan required as the resume condition.

## Task 2: Prove rollback behavior in isolated fake adapters

**Files:**
- Read and execute tests from `/Users/elvis/file/develop/opensource/codex-skill-update/tests/test_update_engine.py`
- Read and execute contract tests from `/Users/elvis/file/develop/opensource/codex-skill-update/tests/test_skill_contract.py`
- Create, atomically and no-replace: `/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update-v2/docs/design/evidence/add-codex-skill-update/2026-08-06-task-6.4-rollback-test-evidence.json`
- Managed runtime mutation: none

- [ ] **Step 1: Run the receipt-bound rollback and recovery tests.**

Run with the working directory `/Users/elvis/file/develop/opensource/codex-skill-update`:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest -v \
  test_update_engine.AuthorityTransactionRecoveryTests.test_receipt_bound_rollback \
  test_update_engine.AuthorityTransactionRecoveryTests.test_rollback_hard_kill_uses_its_own_recoverable_journal
```

Expected result: both tests pass; the fixture restores the old target, writes a complete rollback journal, and converts an injected hard kill into `FAILED_COMPENSATED` without touching a live user path. The result, exact argv, cwd, exit code, named test IDs, and isolated fixture scope are retained for the Task 2 evidence artifact.

- [ ] **Step 2: Run the fake schedule removal and restoration tests.**

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest -v \
  test_update_engine.RegistryScheduleNotificationTests.test_schedule_action_prestate_matrix \
  test_update_engine.RegistryScheduleNotificationTests.test_fake_schedule_transaction_and_restore \
  test_update_engine.RegistryScheduleNotificationTests.test_schedule_remove_and_failure_restore
```

Expected result: all named tests pass; the fake adapter proves successful remove and `FAILED_COMPENSATED` restoration. No real `launchctl` command is permitted. The schedule-remove and failure-restore results are retained separately from the package rollback results.

- [ ] **Step 3: Run the public mutation-boundary contract tests.**

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python3 -m unittest -v \
  test_skill_contract.ContractMetadataRedTests.test_public_parser_exposes_read_only_commands_only \
  test_skill_contract.ContractMetadataRedTests.test_mutation_requests_return_router_handoff
```

Expected result: the public updater surface remains read-only and all mutation-shaped requests remain Router handoffs. This command and its exit code are also included in the Task 2 artifact.

- [ ] **Step 4: Record the tested rollback instruction.**

After Steps 1-3, including when a named test fails, the control plane must write `2026-08-06-task-6.4-rollback-test-evidence.json` with the canonical results, source test-file SHA-256 values, exact test commands and exit codes, `live_launchctl=NOT_RUN`, and `git_operation=NOT_RUN`. After the atomic write, compute the artifact file SHA-256 for the Task 3 parent link and control-plane response; do not embed a self-referential hash in the file. The artifact result is `PASS` only if every named test passes. A missing, malformed, non-canonical, or failing artifact prevents a fresh process invocation.

The artifact must retain both rollback instructions verbatim in sanitized form:

```text
Package receipt-bound rollback is not executed by Task 6.4. The Router must
first create a fresh receipt-bound rollback plan against the package receipt,
current after-fingerprint, immediately previous immutable release, and exact
registry/discovery/binding identity; obtain matching user approval, activate
the exact compensation lease, perform the fixed rollback transaction, verify
the rollback receipt and resulting package identity, and request cleanup
separately. Missing or corrupt receipt-bound rollback material is BLOCKED.

Post-success schedule rollback is not executed by Task 6.4. The Router must
first create a fresh receipt-bound schedule-remove plan against the installed
schedule receipt and current after-fingerprint, obtain matching user approval,
activate the exact compensation lease, perform the fixed launchctl removal
transaction, verify the rollback receipt and loaded state, and request cleanup
separately. Missing or corrupt rollback material is BLOCKED.
```

```text
The two instructions above are evidence-backed guidance only. No package
rollback, schedule-remove, launchctl mutation, or cleanup is executed by this
plan.
```

Expected result: both instructions are backed by the isolated fake-adapter tests and are clearly marked as unexecuted against the live package and LaunchAgent. The plan does not invent a package apply receipt; if none exists, a future package rollback request must remain blocked until a new receipt-bound plan supplies one.

## Task 3: Fresh process verification under an explicit root declaration

**Files:**
- Read: registry, audit bindings, effective roots, updater release, schedule receipt, and existing scheduled report
- Read: `/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update-v2/docs/design/evidence/add-codex-skill-update/2026-08-06-task-6.4-rollback-test-evidence.json`
- Create, atomically and no-replace: `/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update-v2/docs/design/evidence/add-codex-skill-update/2026-08-06-task-6.4-fresh-process-evidence.json`

- [ ] **Step 1: Invoke one fresh, read-only Codex process for the selected account.**

The execution prompt must require the process to report its own `CODEX_HOME`, inspect the registry-bound shared roots and account-a updater projection, verify all four package mappings and both projections, preserve `BLOCKED`/`DIVERGED` states, and stop on any discovery-root ambiguity. It must explicitly forbid updater `audit/plan/verify`, schedule commands, writes, notifications, network, Git, cleanup, and nested Codex execution. For every package, entry, and projection it must report the exact registry-bound effective path, observed path, resolved target, path/tree fingerprint, process root, and identity comparison. A same-name skill from another root must be reported as `NAME_ONLY_COLLISION`; direct inspection without process discovery must be `DIRECT_PATH_ONLY`.

Preferred quota-bearing invocation:

```bash
env CODEX_HOME=/Users/elvis/.codex-account-wb /opt/homebrew/bin/codex \
  --ask-for-approval never exec --ephemeral --sandbox read-only \
  -C /Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update-v2 \
  'Fresh Codex process verification for approved OpenSpec Task 6.4 under /Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update-v2 and Major manifest dfbf263e10ae0d9123b3045f6e250b4bfe9bbf3b4d0740f6a1393544db11de0c. Report this process CODEX_HOME and discoverable skills. Read the registry and audit bindings under /Users/elvis/.codex-account-a/skill-update and verify all four workflow-core packages, every mapped entry, and both projections against their registry-bound effective roots: shared /Users/elvis/.codex for Router, Companion, and Superpowers, and account-a content-addressed runtime discovery for the updater. Preserve BLOCKED and DIVERGED statuses. Verify the account-a updater payload, runtime lock, discovery symlink, LaunchAgent print, receipt, journal, lease, report, and /Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update-v2/docs/design/evidence/add-codex-skill-update/2026-08-06-task-6.4-rollback-test-evidence.json. For every package and projection report the exact registry-bound path, observed process-discovered path, resolved target, fingerprint, process root, identity equality, and whether the result is AUTO_DISCOVERY_PASS, DIRECT_PATH_ONLY, NAME_ONLY_COLLISION, or BLOCKED_DISCOVERY_ROOT. Do not adopt the stale OpenSpec copy under /Users/elvis/file/develop/opensource/openspec-superpower-change as the approved contract. Do not run updater audit, plan, or verify; do not write files, send notifications, use network, run Git, change schedule, run launchctl mutation, execute rollback or cleanup, or invoke another Codex process. Return per-check PASS or BLOCKED and a final verdict; state any account-root discovery limitation explicitly.'
```

If the process is instead run with `CODEX_HOME=/Users/elvis/.codex-account-a`, its result must explicitly state that Router/Companion are not present below account-a and may not claim their automatic discovery. The two account identities must never be conflated.

- [ ] **Step 2: Reconcile the fresh result with Task 1 and Task 2 evidence.**

Before starting the fresh invocation, the control plane must assert that the Task 2 artifact exists, parses as canonical JSON, compute its current SHA-256, and confirm `result=PASS`. Otherwise write the dependency-blocked Task 3 artifact described above and stop without a fresh invocation. After the invocation returns, the control plane must write the Task 3 artifact with a sanitized per-check matrix, the process `CODEX_HOME`, the external invocation exit code, the exact discovery classifications, and the Task 2 artifact path and SHA-256. The external process output is input only; it is not itself the durable evidence artifact.

Expected result: the process exits successfully, confirms the split registry-bound graph, verifies every mapped entry/projection with `AUTO_DISCOVERY_PASS`, preserves the known package observations, and cites the tested package and schedule rollback instructions. A process that only inspects account-a files, reports a same-name skill, or proves only direct-path access is insufficient. The Task 3 artifact result is `PASS` only when the external invocation exit code is `0`, all required discovery classifications are `AUTO_DISCOVERY_PASS`, and no blocker is present.

- [ ] **Step 3: Stop on any blocker.**

If the fresh result is `BLOCKED_DISCOVERY_ROOT`, `BLOCKED_ROLLBACK_EVIDENCE`, `FAIL`, stale, or contradictory, retain the result and stop. A new discovery-switch, registry-replace, schedule-remove, or rollback execution plan requires a separate exact scope and approval; it is not silently added to this plan.

## Task 4: Final read-only reconciliation and review

**Files:**
- Read: `/Users/elvis/Library/LaunchAgents/com.openai.codex.skill-update-audit.plist`
- Read: `launchctl print gui/501/com.openai.codex.skill-update-audit`
- Read: `/Users/elvis/.codex-account-a/skill-update/`
- Read and hash: `/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update-v2/docs/design/evidence/add-codex-skill-update/2026-08-06-task-6.4-rollback-test-evidence.json`
- Read and hash: `/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update-v2/docs/design/evidence/add-codex-skill-update/2026-08-06-task-6.4-fresh-process-evidence.json`
- Read: authoritative v2 worktree and plan-host repository Git status
- Create, atomically and no-replace: `/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update-v2/docs/design/evidence/add-codex-skill-update/2026-08-06-task-6.4-blocker-resolution-evidence.json`

- [ ] **Step 1: Recheck the installed scheduler and immutable payload.**

Run only:

```bash
/bin/launchctl print gui/501/com.openai.codex.skill-update-audit
find /Users/elvis/.codex-account-a/skill-releases/codex-skill-update/188f94b4f303965a03f07383e9c5ab733906cef39918255d86e679bf49a556fe/payload \
  \( -type d -name __pycache__ -o -type f -name '*.pyc' \) -print
git -C /Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-codex-skill-update-v2 status --short --branch
git -C /Users/elvis/file/develop/opensource/openspec-superpower-change status --short --branch
```

Expected result: LaunchAgent remains loaded/not running with `runs=1` and last
exit `0`; schedule remains Monday 10:00; payload has no bytecode. Relative to
the Task 1 snapshots, the authoritative v2 worktree contains only its
pre-existing dirty state plus the three explicitly allowed evidence artifacts,
and the plan-host repository is unchanged. No tracked file, managed state-root
artifact, runtime payload, Git index, ref, or unrelated untracked file changes.

- [ ] **Step 2: Run control-plane review of the evidence matrix.**

Read both task artifacts, recompute their file SHA-256 values, and write the final artifact with parent artifact paths and hashes. Review actual command output and confirm that every PASS claim has a fresh command, every BLOCKED claim has an owner/resume condition, known package blockers remain visible, no raw CLI trace is copied into durable evidence, registry-bound path identity is explicit for every discovery claim, and no user authorization was broadened. The final artifact must be canonical JSON and its own SHA-256 must be reported to the user.

- [ ] **Step 3: Decide the 6.4 transition.**

Record exactly one outcome in the final evidence artifact and in the control-plane response:

```text
PASS: discovery graph, all mapped entries/projections, isolated rollback tests,
and fresh process evidence reconcile; live schedule remains untouched.

BLOCKED: include blocker owner and resume condition; do not mark Task 6.4 done.
```

Do not reconcile `tasks.md`, archive the OpenSpec change, run full closeout, or claim whole-task completion from this plan alone. An external fresh Codex verdict can support the matrix but cannot decide this transition.

## Rollback and stop conditions

- This plan has no forward mutation and therefore has no automatic compensation lease.
- If any managed path, registry hash, binding, LaunchAgent, or payload identity changes during verification, stop and report drift; do not restore by guesswork.
- If the fake tests fail, stop at Task 2 and create a correction plan under the same approved scope before changing source.
- If the fresh process cannot prove the intended root, stop at Task 3 and request a new discovery-switch or account-selection decision.
- If any allowlisted evidence filename already exists, stop before execution; no evidence artifact may be replaced by this plan.
- Package receipt-bound rollback and schedule-remove are separate future operations; either requires its own receipt-bound plan, approval, and verification. Neither is authorized here.
- If a real schedule rollback is later requested, create a new `schedule-remove` plan and exact approval; this plan does not authorize it.
- No Git staging, commit, reset, clean, push, or publication is part of this plan.

## Completion evidence

The control plane must write and return:

1. A sanitized discovery graph table with package, entry, projection, effective root, process root, and PASS/BLOCKED result.
2. The exact focused test commands and their exit codes.
3. The Task 2 artifact path and SHA-256, containing package receipt-bound rollback and schedule-remove instructions plus an explicit statement that live rollback was not executed.
4. The Task 3 artifact path and SHA-256, containing the fresh process root and exact registry-bound discovery classifications.
5. The final artifact path and SHA-256, linking the preceding artifacts and recording the final decision.
6. Fresh LaunchAgent, payload, registry/binding, report/receipt, and Git no-drift checks.
7. One final `PASS` or `BLOCKED` decision with owner and resume condition.

The three evidence artifacts are completion evidence for this recovery attempt; the plan itself is not, does not change the OpenSpec task checklist, and does not authorize any state-changing operation.
