# Tasks: tighten-codex-superpowers-invocation-routing

## 1. Proposal and approval

- [x] 1.1 Confirm the predecessor is archived, its four requirements are in the
  base spec, and the stale same-id active copy cannot be extended safely.
- [x] 1.2 Create a follow-up proposal/design/spec/tasks containing only the new
  Codex invocation and authority delta.
- [x] 1.3 Run strict OpenSpec validation and correct every finding.
- [x] 1.4 Run an independent read-only delta Review and correct every actionable
  finding.
- [x] 1.5 Present the exact follow-up change-id and record explicit approval;
  predecessor approval does not authorize this change.

## 2. RED evidence and decision gates

- [x] 2.1 Preserve or rerun the isolated Codex 0.147.0 controls proving user
  `$child` succeeds while Router-to-explicit-only-child returns
  `CHILD_LOAD_BLOCKED`; record paths, hashes, command, output, and the ban on
  shell/filesystem fallback.
- [x] 2.2 Add a deterministic RED source regression proving
  `using-superpowers` lacks Codex-specific explicit-only metadata and its Codex
  README still claims automatic discovery.
- [x] 2.3 Add RED routing scenarios for ordinary questions, diagnose-only,
  proposal-only with Superpowers `none`, material brainstorming, Direct Change,
  both Review classes, user-explicit `$superpowers:*`, whole-task completion,
  missing/duplicate Router, and bounded phase chaining.
- [x] 2.4 Add RED checks binding the exact CCG-014 v5 replacement text and
  managed-rule version 5, plus unchanged shared `using-superpowers/SKILL.md` and
  non-Codex Superpowers invocation metadata.

## 3. GREEN source implementation

- [x] 3.1 In a non-discoverable structured staging copy of the exact live
  Superpowers pre-state, add
  `skills/using-superpowers/agents/openai.yaml` with
  `policy.allow_implicit_invocation: false`, update `docs/README.codex.md`, and
  add `tests/codex/using-superpowers-invocation-policy.test.js` in the
  source-managed Superpowers checkout.
- [x] 3.2 Update `references/superpowers-adapter.md` and
  `references/request-modes.md` with the exact route table, explicit-method
  authority, finite phase return, native child-loading limitation, and
  fail-closed behavior.
- [x] 3.3 Install the design's exact `CCG-014` replacement text, bump
  managed-rule version 4 to 5 with invariant IDs `CCG-001` through `CCG-015`,
  and bind `tests/test_workflow_rules.py` and `tests/test_cross_cli_sync.py` to
  the exact rule/version contract.
- [x] 3.4 Update README/README_cn, changelog, manifests, and other navigation or
  validation surfaces required by the scoped source changes.
- [x] 3.5 Do not modify Router-required child invocation metadata or shared
  `using-superpowers/SKILL.md` bytes.

## 4. Source validation and Review

- [x] 4.1 Run required `quick_validate.py`, project validators,
  dependency-free fallback checks, and full test suites in the Router repository
  and the staged Superpowers copy without touching the live discovery target.
- [x] 4.2 Run fresh isolated Codex sessions proving an ordinary question does
  not exhibit the `using-superpowers` meta-workflow, explicit
  `$superpowers:using-superpowers` exhibits the complete Skill's unique
  behavior, and Router-required child safety behavior remains available. Claim
  actual load absence only with a supported path/hash trace; otherwise record
  prompt-load state `UNKNOWN` separately from behavioral PASS.
- [x] 4.3 Prove Router-to-explicit-only-child remains blocked/unsupported rather
  than claiming nested activation, and verify missing/duplicate Router and
  cyclic phase routes fail closed.
- [x] 4.4 Run a distinct High Review over both complete source diffs, actual
  files, route behavior, Git authority, cross-host isolation, tests, and
  rollback.
- [x] 4.5 Fix every actionable finding and repeat affected validation,
  forward-tests, and Review until PASS.

## 5. Runtime synchronization

- [x] 5.1 Inventory active external contracts and exact required runtime targets;
  stop on incompatible state.
- [x] 5.2 Generate and Review path/hash-only sync plans from validated Router
  source and the staged Superpowers delta; bind every live target to fresh
  pre-state hashes and backups.
- [x] 5.3 Synchronize managed-rule version 5 to Codex, Antigravity CLI, and Grok
  CLI one at a time; restore and stop on any target failure.
- [x] 5.4 Apply the reviewed three-path Codex-specific Superpowers delta once to
  the checkout that is also the live symlink target; immediately run source and
  fresh-session verification, restore exact pre-state on failure, and perform no
  Superpowers Git operation.
- [x] 5.5 Run verify-all, fresh discovery checks, shared/non-Codex hash checks,
  and final cross-target Review.

## 6. Closeout

- [x] 6.1 Run Project Learning Closeout only for confirmed implementation
  learnings; do not promote proposal assumptions.
- [x] 6.2 Run fresh final critical validation and final Review after corrections
  or any learning promotion.
- [x] 6.3 Reconcile tasks, update closeout docs, archive the change, and run
  strict post-archive validation.
- [x] 6.4 Remove temporary backups only after source/runtime/forward-test/Review
  gates pass; report limitations, residual risks, and rollback proof.
