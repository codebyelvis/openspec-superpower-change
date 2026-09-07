## Proposal

- [x] Read original article and affected instruction owners; classify Major.
- [x] Draft the exact instruction-only scope and rule snippets.
- [x] Strictly validate this change and present it for approval.
- [x] Record explicit user approval of `trim-instruction-routing` revision `v1`.

## One approved implementation slice

- [x] Refresh structured backup; satisfy applicable existing implementation-entry gates without duplicate design or unrelated ceremony.
- [x] Apply the bounded description/router/reference/AGENTS wording changes; preserve all protected gates and resolve only in-scope wording collisions.
- [x] Run current required validators, both parser paths and the existing suite; reuse isolated Major routing/lifecycle forward-tests for before/after evidence, adding no tests.
- [x] Obtain required Review, perform applicable exact-file runtime sync/verification, reconcile this task list and report results; no push.

## Current evidence

- Status: complete locally. Source, all four runtime deployments, required
  checks, final Review and temporary-backup cleanup passed. Git/publication
  remain unrequested and were not performed.
- Instruction files: `SKILL.md`, `AGENTS.md`, and references
  `direct-change-rule.md`, `superpowers-adapter.md`, `request-modes.md`,
  `approved-implementation-workflow.md`, `local-instruction-checkpoint.md`,
  `completion-contract.md`, `step-evidence-gate.md`, `response-patterns.md`.
- Approved compatibility follow-up: existing `scripts/validate_core_gates.py`,
  `tests/test_workflow_rules.py`,
  `tests/run_role_first_review_forward_tests.py`, and
  `tests/fixtures/superpowers-routing-cases.json`. Owner/wording expectations
  follow the trimmed router; no new tests, schema, runner or framework.
  Missing/decoy owner, approval, authority, evidence and parser-negative checks
  remain. Every routing fixture retains full-row route/state/signoff assertions.
- Root size: 21,312 -> 9,216 bytes (about 57% smaller). This is file size,
  not measured token savings.
- Compatibility FULL_PREFLIGHT: PASS; independent Codex reviewer
  `/root/preflight`, `control-plane-high`, governed-review-evidence only.
  Approved proposal SHA-256:
  `208ac8d8ff7d6923570d6000f73b4fc9a7a3c72fe58a2e3fc36c4c37af164aba`.
- Implementation Review: restored moved noncompact method mappings and
  corrected a test branch that omitted other routing-row assertions; independent
  recheck reports source PASS. Non-negotiables equal HEAD byte-for-byte.
- Existing fresh-agent baseline reproduced over-reading and mandatory small-fix
  TDD/Preflight. After-edit seven read-only routing decisions follow intended
  paths; these are decision evidence, not native lifecycle claims.
- Existing native routing runner: 13 PASS / 0 FAIL, all original cases, audited
  native events. The first invocation found duplicate packaged Skill discovery;
  the same unchanged runner passed against an isolated runtime-only source copy.
  Post-merge rerun also passed 13/13, zero tool events; sanitized final summary
  `routing-forward-merged.json` SHA-256:
  `9c643756d6a9242ae2078e103cb16fa403e67f8df28549525bd4c985eb6a335a`.
- Isolated Minor lifecycle: backup -> one-word example edit -> quick validation
  with PyYAML -> core validation with dependency-free fallback -> diff/preimage
  checks, all PASS. Fixture `/tmp/openspec-minor-lifecycle.l4CVB7/candidate`;
  no source/runtime mutation and no portable-completion claim from this fixture.
- Post-merge quick validation with PyYAML: PASS. Core validator with PyYAML and
  dependency-free fallback: PASS. Full unittest suite after the last test repair:
  324 tests PASS under each parser; companion fallback suite 91 PASS. Strict OpenSpec validation and
  `git diff --check`: PASS.
- Learning audit: owner-bound validation and complete routing-row coverage are
  already durable project invariants with existing negative regressions. The
  task-local corrections restore those obligations; no new generalized
  invariant or requested archive/distillation requires a new learning document.

## Runtime reconciliation

- No staging, Git commit, push, archive or publication performed.
- Initial exact-file planning found four pre-existing common runtime differences:
  `references/self-evolution-rule.md`, `references/cross-cli-sync.md`,
  `references/sync-checklist.md`, `scripts/validate_cross_cli_sync.py`.
- The explicit delegated local-repair authorization was recorded in the proposal
  amendment before importing those exact existing bytes into canonical source.
  No runtime preimage was overwritten to resolve this drift; no future Major
  approval rule was changed. Current proposal SHA-256:
  `ca4b644c735c8ac4ee0824b5c9ae6859533954463a4beb2cd73a3594b7ce97f5`.
- A composite staging source would conceal noncanonical assertion drift;
  independent Review rejected it. It was not used; canonical parity was restored
  through the recorded compatibility amendment.
- Independent four-file and sync-plan Review: PASS. Plan SHA-256:
  `25577a602c21994fe66babcbc715c71d8f2c89d5fe19ffb7f9faa315e6f01eac`.
  Schema 2: ten selected files per target, 29 unselected assertions; version-6
  managed global rules unselected and unchanged. Full prestate passed before
  apply. Known source documentation roots contained no legacy canonical status.
  Managed-rule body SHA-256:
  `0040153a954ab0a6599e3eb951e8fa6b7715710745616f1f404904bf056c11d2`.
- Codex -> Pi -> Antigravity -> Grok: apply, content verification, discovery,
  transaction commit all PASS. Interruption occurred after Codex verified and
  Pi applied; receipts were inspected and Pi resumed at verification, without
  duplicate apply. Final `verify-all`: PASS. Grok native inspect was consumed
  without echoing raw content. Target quick/core validators and companion
  quick/template validation: PASS.
- Sanitized logs, reviewed plan and receipts are outside discovery roots at
  `/tmp/openspec-instruction-cleanup-approved.KEhSTyD1`. Structured backups
  and isolated fixtures were removed after final gates, including the abandoned
  raw run from interruption. No backup/raw-inspect artifacts remain in that
  evidence directory. Unrelated pre-existing runtime transaction files and
  repository work are preserved.
- Final Review: PASS, independent Codex `/root/preflight`,
  `independent-reviewer / control-plane-high`, governed-review-evidence only.
  Complete eighteen-file diff and claims inspected; all findings closed.
  The control plane verified cleanup and recorded local completion.
- No temporary rollback copy is retained after success. Source Git history and
  this uncommitted task diff remain available for a separately authorized,
  path-scoped revert; retained sync receipts document the applied pre-state.
