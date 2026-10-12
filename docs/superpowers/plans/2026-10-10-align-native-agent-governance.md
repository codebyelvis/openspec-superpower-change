# Native Agent Governance Implementation Plan

> **For agentic workers:** Use `superpowers:executing-plans` with the Router-governed variant; the approved isolation is a temporary working copy. Do not create an SDD ledger or Git commits.

Author: elvis. Change: `align-native-agent-governance` draft-v1. Approved by the user: `已批准 align-native-agent-governance`, 2026-10-10.

**Goal:** Align shared native instruction consumption while preserving both skills, existing authority and four-target transaction safety.

**Architecture:** Update the existing shared block and local checkpoint; enforce each policy in its own artifact. Extend current validators and reuse the existing no-tool native-event auditor for a bounded Codex instruction-consumption probe. Source validation and independent Review precede any reviewed runtime transaction.

**Tech stack:** Python standard library, unittest, OpenSpec; isolated PyYAML environment only for the required parser mode/quick validation.

**Spec:** `openspec/changes/align-native-agent-governance/{proposal,design}.md` and its `specs/skill-workflow-governance/spec.md`.

## Global Constraints And Authority

- Strict profile. Root author/executor/control-plane instance: `align-native-root` (current `/root`). Reviewer is a distinct Codex instance, role `independent-reviewer`, profile `control-plane-high`, authority `governed-review-evidence`; it cannot authorize scope or canonical transitions.
- Approved isolation: temporary filesystem working copy, preserving original file hashes and Companion. No Git writes, native overlays, auth/session/model replication or publication.
- Runtime targets/order: `codex`, `pi`, `antigravity-cli`, `grok-cli`; bind default Codex explicitly. Manifest schema 1, managed-rule version 6, sixteen existing IDs and four formal products remain unchanged.
- Allowed source files are exactly the proposal list. Companion, dirty main spec/other active changes and all pre-existing untracked files remain unchanged. Plans/evidence/approval records are change-specific artifacts.
- Exact shared snippets come from design sections 3/4. Preserve CCG-001/002/010/016 and CCG-014's existing paragraph. Runtime mutation remains selected portable files and four managed blocks only.
- Stop on prestate drift, an excluded edit, failed required evidence, actionable findings or scope/protected-boundary changes. Source rollback restores only scoped files; target recovery uses existing receipt/backup machinery.
- Seven-entry native loading/behavior is outside this slice. The probe tests native Codex consumption of a hash-bound temporary AGENTS projection, not native Skill-body loading or other agents.

## Review Focus

- Compact external must not inherit compact-local inline readiness; preserve distinct required Preflight/evidence.
- Missing clauses moved to unrelated sections/files or hidden in comments must fail their owner validator.
- A shared discovery catalog with an empty private directory must neither be labeled unavailable nor promoted to qualified runtime.
- Native publisher defaults must not confer a formal product/role or rewrite bound evidence.
- Native defaults must not turn required plans into after-execution bookkeeping or move bound paths.

## Task 1: Preflight And RED Baseline

Files: this plan, change approval/evidence records, `tests/test_workflow_rules.py`, `tests/test_cross_cli_sync.py` and new case fixture/forward runner.

- [ ] Check approved artifact hashes and capture fresh structured source backups outside skill discovery. Existing workspace baseline: 478 unittest tests, exit 0 in the dependency-free mode.
- [ ] Independent Preflight inspects complete approved contract, this executable plan, actual affected source, baseline evidence, forbidden effects and independent adversarial case; bind the whole-file plan hash in a separate Review artifact. Result is PASS or BLOCKED.
- [ ] Before rule edits, execute a read-only native baseline scenario using the current shared governance projection: obvious compact local typo, no protected effects, no user-requested plan. Record observed classifier fields and native event audit without persisting raw traces. Expected new behavior is inline readiness; report actual baseline mismatch rather than inventing an agent failure if it complies.
- [ ] Add tests invoking real validators, not text-only grep: new positive consumption validation must fail on missing obligations before implementation; source mutation to old universal CCG-004 or removed advisory exception must fail after implementation. Preserve exact legacy v6 fixture bodies while adding updated CCG-004/014 fixtures.

Interfaces: `validate_native_agent_consumption(governance: str, checkpoint: str, adapter: str, cross_cli: str, checklist: str) -> None` in `scripts/validate_core_gates.py`, raising AssertionError for missing/misowned obligations. `validate_managed_rule_semantics(body: str, *, version: int) -> bool` retains its API and adds exact owned CCG-004/014 validation to v6.

Commands: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_workflow_rules.py -v` and the equivalent `test_cross_cli_sync.py`; record expected failing new tests before production changes.

## Task 2: GREEN Source And Native Consumption Proof

Files: proposal-listed five references, two validators, two existing test files, `tests/fixtures/native-agent-governance-cases.json`, `tests/run_native_agent_governance_forward_tests.py`, engineering invariants and changelog.

- [ ] Apply exact CCG-004 replacement/CCG-014 append. Add `## Native agent consumption` to the local checkpoint with exact design text, entry metadata and real Claude-launcher identity; append minimal pointers to adapter/cross-cli/checklist.
- [ ] Add owner-bound validation for CCG paragraphs and the checkpoint section plus pointers. Reuse existing visible-Markdown section parser so comment/code or content moved to an unrelated section cannot pass. Do not concatenate artifacts to satisfy obligations.
- [ ] Extend tests through actual validator calls: remove each new safety obligation, move the full checkpoint section under another owner, hide policy as comments, restore universal Preflight and append a contradictory compact-external waiver. Each must be rejected. Existing schema product substitution and sequential drift/recovery tests remain required.
- [ ] Add seven fixture cases exactly matching design: advisory chat; compact local; compact external; unapproved Major; bound plan; alternate shared discovery; Claude product substitution. Keep expected fields separate from model input.
- [ ] Runner API: `run_case(case: dict, router_root: Path, temporary_parent: Path) -> dict`, `validate_observed(value: object) -> dict`, `main(argv: list[str] | None = None) -> int`. CLI: `--router-root`, `--temporary-root`, `--sanitized-summary`, optional repeatable `--case`. Output is finite classifier enums and audit/hash metadata only. Reuse `parse_event_trace`, private directories, process-group timeout and snapshot helpers from `run_superpowers_routing_forward_tests.py`; never print/copy raw stdout/stderr or private prompts.
- [ ] For the probe, project AGENTS automatically receives the exact source governance/checkpoint consumption sections and fixture native defaults; hash each input. Keep CODEX_HOME for existing auth without copying auth, use an empty private HOME and `codex exec --json --ephemeral --ignore-user-config --ignore-rules --sandbox read-only --skip-git-repo-check`; leave model/effort defaults intact. Output schema contains `delivery`, `preflight`, `plan_timing`, `artifact_path`, `product`, `qualification`, `authority`, `action`. Reject missing/extra keys, invalid enums, incomplete/unknown/tool native events and project mutation. Do not claim native Skill loading from these events.
- [ ] Execute all seven cases with `PYTHONDONTWRITEBYTECODE=1 python3 tests/run_native_agent_governance_forward_tests.py --router-root . --temporary-root <private-new-root> --sanitized-summary <private-summary>`; require seven actual matches and sufficient native event audit, with raw outputs removed. A correct classifier without audit is not PASS.
- [ ] Run quick_validate with the isolated PyYAML interpreter, core gates/full unittest with default dependency-free python3 and with PyYAML interpreter. Run unchanged Companion quick/core template validator and source/runtime contract-byte checks. Run `openspec validate align-native-agent-governance --strict`.

Tests assert each realistic source mutation is rejected by the real validator and the runner rejects tool/unknown/malformed events. Changes to constraints happen only in their owned artifact. Generalized invariant promotion points to those tests and the loaded checkpoint, not this task history.

## Task 3: Independent Implementation Review And Existing Sync

- [ ] Distinct Codex Implementation Review inspects all changed files/complete diff, reruns critical checks and independent adversarial mutations. Supply Router-governed variant and full assignment. Same-scope findings use fix/verify/independent Review, without restarting Preflight.
- [ ] Compare unchanged originals to baseline, then copy only reviewed allowed files from the isolated work copy into source using per-file original hash/absence guards. No blanket tree replacement.
- [ ] Generate sync-plan schema v2 using existing script, explicit default Codex skills root, sibling Companion source, the five changed portable references and two validators as `--select-file` selectors, and `--select-managed-rule`. Exact target skill roots/global-rule paths are reviewed, not inferred from active CODEX_HOME. Unselected portable closure remains parity assertions.
- [ ] Independently review path/hash-only plan and its prestate, source/manifest hashes, selectors, four ordered targets, native byte exclusions, discovery/recovery and backups. Apply only after PASS.
- [ ] Run the existing plan/apply-target/verify-target/commit-target/verify-all and receipt commands exactly as documented by current CLI help. A target failure triggers existing restore/recovery and blocks later targets. `commit-target` is the sync receipt operation, never Git commit. Keep receipts/backups outside skill discovery.
- [ ] Verify all forty source/runtime portable files per target, native outside-block bytes, managed body hashes and Grok inspected discovery. Unselected Companion remains unchanged. File/inspect results cannot become seven-agent behavior claims.

## Task 4: Fresh Final Verification And Native Adaptation Plan

- [ ] Run final required source/runtime verification after last change and required generalized learning promotion, then obtain separate independent Final Review. Hash-bind final source, evidence and receipts; fix/reverify/review any findings.
- [ ] Produce next local native-adaptation review plan only, with exact per-path prestates/candidates where inspection permits; explicit unresolved native mechanism/acceptance blockers stay visible. Do not edit account A, Claude/Cursor overlays, Grok settings/hooks or dependency links.
- [ ] Update canonical existing task checkboxes/evidence by actual results; report source-slice status and pending seven-entry work. Keep only sanitized evidence. Clean temporary raw traces immediately after audit and temporary backups only when their required validation/sync/final gates and rollback decisions are satisfied.

## Progress And Evidence

- Approval received for draft-v1, before implementation.
- Original source fingerprints verified; work copy and refreshed backups prepared outside discovery. Pre-existing files preserved.
- Baseline dependency-free unittest: 478 tests, exit 0. No implementation rules changed yet.
- Implementation, Preflight, RED/GREEN, native proofs, runtime sync and final gates: pending.
