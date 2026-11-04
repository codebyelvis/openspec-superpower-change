# Design: Streamline plan-anchored execution

## Core Architecture: Anchor-at-Ends, Free-in-Middle

```text
[High-Capability Planner]              [Any Model Executor]                     [High-Capability Reviewer]
Single Four-Anchor Plan/Contract       Coarse-Grained Cohesive Batch            Complete-Diff & Regression Gate
├─ 1. Allowed/Forbidden File Scope ──► • Full implementation autonomy in scope ──► • Inspect complete git diff vs scope
├─ 2. Interfaces & path:line Facts     • No micro-step gates or interim JSONs     • Verify real regression test output
├─ 3. Cohesive Batch Milestones        • Run exact regression suite to GREEN      • Single consolidated Review report
└─ 4. Exact Regression Test Commands   • Record inline RED->GREEN proof line
```

## Key Decisions

### 1. Four-Anchor Plan Unification (No Duplicate Plan or Local Preflight JSON)

An approved OpenSpec change whose `design.md` and `tasks.md` define the **Four Hard Anchors**:
1. **Scope & Non-Goals**: exact allowed files/modules and forbidden boundaries;
2. **Code & Contract Facts**: target interfaces/signatures and `path:line` anchor points;
3. **Coarse-Grained Cohesive Batches**: 1 cohesive batch by default (or 2–3 milestone batches for cross-subsystem work);
4. **Executable Regression Gate**: exact test/build commands and required regression assertions;

is already an executable Plan. In this case, `superpowers:writing-plans` is not required to emit a second `implementation-plan.md`, and local single-agent execution proceeds after verifying a clean baseline (`git diff --stat` / approved baseline SHA) without standalone `preflight-full.json` / `preflight-focused.json` files. Cross-agent External Handoff retains its Preflight gate.

### 2. Coarse-Grained Execution and Inline RED-to-GREEN Proof

- Work is grouped into complete business batches rather than per-file or 5-minute micro-steps.
- Inside an approved batch, the executor model iterates freely on code and tests without stopping for intermediate conversational confirmation or writing standalone `red-green.json` / `native-green.json` files.
- To preserve TDD anti-forgery without file bloat, the final verification/review report records a concise inline RED-to-GREEN proof: failing test name, non-zero exit code, and one-line failure summary prior to the fix, followed by the passing command and exit code `0`.
- Localized bugfixes restoring intended behavior qualify for Direct Change without a pre-existing approved spec path in Gate 0 when they (a) include a failing-then-passing regression test, (b) do not alter external API, schema, permission, or lifecycle contracts, and (c) stay within the localized diff scope.

### 3. Lazy Session Resume and Clean `verified_revision.inputs`

- **Lazy Creation for `compact` and `standard`**: `docs/agent-collab/<change-id>/status.md` and `## Resume Context` are created only before an intentional pause, context compaction, or cross-window/external handoff. Single-window runs that finish in one session create no `status.md`.
- **Boundary-Only Refresh for `strict` and `self-evolution`**: Local `strict` and `self-evolution` tasks create `status.md` once at approval to bind `control_plane_owner` and refresh it only at review/completion transitions rather than every micro-step.
- **Clean Input Fingerprints**: `verified_revision.inputs` covers only the verified source, rule, config, and test files exercised by `verification_commands`. It explicitly excludes `CHANGELOG.md`, task ledgers (`tasks.md`, `BACKLOG.md`, `CURRENT.md`, `LOG.md`), and historical Review/Evidence reports so closeout documentation updates do not invalidate the verified source fingerprint.

### 4. Hot-Path / Cold-Path Partitioning in `approved-implementation-workflow.md`

To eliminate ~260 lines of cold-path reading overhead during routine execution while maintaining 100% compatibility with `scripts/validate_core_gates.py`, `references/cross-cli-portable-manifest.json`, and JEV routing fixtures:
- Keep all required normative phrases inside `references/approved-implementation-workflow.md`.
- Place an explicit `<!-- COLD_PATH_START: Read the sections below only on session resume, compaction recovery, blocked-context amendment, or control-plane rebind/return -->` boundary before `## Project Session Resume` so agents executing normal single-window tasks stop reading after the hot-path trunk.

## Rollback Path

Restore `SKILL.md`, `references/approved-implementation-workflow.md`, `references/direct-change-rule.md`, `references/step-evidence-gate.md`, `references/completion-contract.md`, and `tests/test_workflow_rules.py` from `/tmp/openspec-superpower-change-backup-20261104-131400`, and remove `openspec/changes/streamline-plan-anchored-execution/`.
