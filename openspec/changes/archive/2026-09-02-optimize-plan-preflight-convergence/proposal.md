# Change: Optimize Plan Preflight convergence

## Why

Low-risk, same-scope Plan corrections can currently trigger repeated full
Preflight Reviews. The current contract blocks on every actionable finding and
reruns whenever artifact bytes change, but it does not distinguish a first full
review from a focused recheck, require first-pass finding completeness, or bound
same-lineage retry count. Mechanical plan defects therefore consume repeated
High Review effort even when scope, contract, risk, authority, and safety
boundaries remain unchanged.

## What Changes

- Add three convergence paths without adding canonical states: Preflight review
  modes `FULL_PREFLIGHT` and `FOCUSED_RECHECK`, plus the existing-control-plane
  route `CONTROL_PLANE_ADJUDICATION` outside Preflight Review.
- Keep gate results exactly `PASS` or `BLOCKED`.
- Require the first full review to cover one complete review matrix, run an
  independent adversarial probe, and attest finding completeness.
- Permit finding-only recheck when every protected boundary is explicitly
  verified unchanged and the artifact diff is limited to declared same-scope
  corrections.
- Store compact lineage root/current/parent whole-file hashes, parent-anchored
  reviewer identity, protected-boundary checklist, correction set, mechanical
  evidence, completeness, findings,
  recommendations, and separately classified accepted residual risks only inside
  the existing Preflight Review artifact; it remains Review evidence and never
  becomes canonical task/Handoff/status state.
- Route a second same-lineage `BLOCKED`, reviewer conflict, scope growth,
  unauthorized protected-boundary change, or a late finding that should have
  been detected in the full review to the existing control-plane mechanism for
  one bounded adjudication. An already-authorized boundary change starts a new
  lineage at full review instead.
- Separate non-blocking recommendations from actionable findings. Advice cannot
  waive acceptance, safety, evidence integrity, or authority.
- Require deterministic mechanical Plan self-checks before human Preflight.
- Interpret executable Plan completeness by business slice: exact boundaries,
  interfaces, TDD intent, critical commands, rollback, and stop conditions are
  required; complete implementation bodies are required only when omission
  leaves a material choice unresolved.
- Clarify that evidence profile follows changed effects, not merely a substrate
  being read. Any profile change remains protected and forces full review.
- Update English and Chinese READMEs.

## Scope

Source files:

- `SKILL.md`
- `references/approved-implementation-workflow.md`
- `references/superpowers-adapter.md`
- `references/step-evidence-gate.md`
- `scripts/validate_core_gates.py`
- `tests/test_workflow_rules.py`
- `README.md`
- `README_cn.md`
- `docs/engineering-invariants.md` when Project Learning Closeout confirms a reusable invariant
- this OpenSpec change

Runtime targets after source validation and independent Review:

- Codex
- Pi
- Antigravity CLI
- Grok CLI

Only portable files selected by the existing cross-CLI manifest are synchronized.
README, tests, and OpenSpec history remain repository-only.

## Non-Goals

- Skip Plan Preflight, Implementation Review, Final Review, or Completion
  Contract.
- Weaken database-write, production, Git, publication, deployment, security,
  authorization, schema/API, migration, deletion, or recovery gates.
- Permit P0/P1, security, data-loss, authority, scope, contract, risk, or
  acceptance findings to pass.
- Add a new lifecycle state, Handoff, Quality Gate, Finding ledger, task manager,
  reviewer product, or final authority.
- Automatically downgrade an existing revision lineage's evidence profile.
- Modify `superpowers:writing-plans` itself.

## Compatibility

Existing Preflight artifacts remain valid historical Review evidence. Missing
convergence metadata selects a new `FULL_PREFLIGHT`; it never guesses focused
eligibility. Focused recheck requires a human-auditable record embedded in the
existing Review artifact and bound to the current whole-file artifact plus an
immutable parent Review that anchors historical root SHA-256 and reviewer
identity. Existing canonical lifecycle values, Handoff schema 6, schema-2
evidence, Reviewer Assignment, Confirmation Lease, and Completion Contract
remain unchanged.

## Evidence and Safety

This is Major Self-Evolution because it changes Preflight routing and evidence
signoff. Implementation requires focused RED/GREEN tests, project validators,
complete source tests, independent High Review, reviewed scoped cross-CLI sync,
four-target parity/discovery validation, fresh final verification, and final
Review. Temporary structured backups are required before source/runtime edits.
Git commit and push use the user's explicit publication authorization.

## Approval Status

- Change-id: `optimize-plan-preflight-convergence`
- Risk/evidence profile: `strict`
- Decision provenance: `ai-proposed/user-approved`
- The user approved closed-loop implementation of the previously presented
  Bounded Preflight Convergence recommendation. Exact artifact approval remains
  subject to strict validation and the repository's Major Self-Evolution gate.
