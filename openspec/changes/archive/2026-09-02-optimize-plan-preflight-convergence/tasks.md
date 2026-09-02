# Tasks: optimize-plan-preflight-convergence

## 1. Contract and approval

- [x] 1.1 Strictly validate proposal/design/spec/tasks.
- [x] 1.2 Obtain independent Proposal Review PASS.
- [x] 1.3 Record explicit approval of this exact change-id and scoped revision.

## 2. Pre-change safety and RED

- [x] 2.1 Inventory source/runtime prestates and create structured temporary backups.
- [x] 2.2 Add focused workflow tests for Review-record ownership, current whole-file SHA/path/symlink rules, immutable parent anchoring of historical root SHA and exact reviewer identity, mode selection, authorized/unauthorized protected-boundary changes, replacement or author/executor-reused reviewer, legacy missing metadata, revision/parent binding, undeclared diffs, safety blocking, finding completeness, retry adjudication, recommendations, separately classified accepted residual risks with evidence/impact/owner-or-decision, Plan proportionality, and lifecycle preservation.
- [x] 2.3 Run focused tests and record expected RED caused by missing convergence rules.

## 3. Minimal implementation

- [x] 3.1 Add the normative convergence contract to `references/approved-implementation-workflow.md`.
- [x] 3.2 Update `SKILL.md` and `references/superpowers-adapter.md` to route revision changes through that contract.
- [x] 3.3 Update `references/step-evidence-gate.md` with blocking/recommendation and effect-based risk rules.
- [x] 3.4 Extend `scripts/validate_core_gates.py` only with direct semantic assertions needed by this change.
- [x] 3.5 Update `README.md` and `README_cn.md` with the user-visible behavior.

## 4. Source verification and Review

- [x] 4.1 Run focused GREEN.
- [x] 4.2 Run quick validation, core validation, full unittest, strict OpenSpec validation, and `git diff --check`.
- [x] 4.3 Obtain independent implementation High Review PASS over actual files and complete diff.

## 5. Runtime synchronization

- [x] 5.1 Generate and Review a scoped path/hash-only cross-CLI plan for changed portable files.
- [x] 5.2 Apply and verify Codex, Pi, Antigravity CLI, and Grok CLI in manifest order.
- [x] 5.3 Verify full portable parity, discovery, validators, and sensitive-category exclusion.

## 6. Completion and publication

- [x] 6.1 Run Project Learning Closeout and promote only confirmed reusable invariants.
- [x] 6.2 Run fresh final verification after the last source/runtime/learning change.
- [x] 6.3 Obtain independent final Review PASS.
- [x] 6.4 Reconcile tasks and archive the OpenSpec change with strict post-archive validation when repository semantics permit.
- [x] 6.5 Remove temporary backups after rollback is no longer needed.
- [ ] 6.6 Commit and push the verified source changes under the user's explicit Git publication authorization.
