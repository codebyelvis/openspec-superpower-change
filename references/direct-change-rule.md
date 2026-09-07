# Direct Change Rule

Use Direct Change when OpenSpec is not required.

Allowed examples:

- requested bug fix restoring intended behavior;
- low-impact config tweak;
- formatting change;
- comment update;
- typo fix;
- docs-only update without contract impact;
- test-only change for existing behavior.

## Compact local work

For an obvious, local, reversible change outside every protected boundary,
record all Gate 0 facts in one line, make the minimum edit, run relevant
verification and required checks, then record a focused inline diff/self-review.
No separate Plan, Preflight, full TDD cycle, Domain Context checklist, grill,
Handoff, independent multi-agent Review or Learning Closeout is required solely
because files change. This is the existing `compact` path, not a new profile.

Behavior fixes still need cause evidence, a regression test and compact
business-slice signoff under `references/step-evidence-gate.md`; reuse an adequate
existing test. Non-behavioral edits do not need a test invented for the edit.
Read `references/completion-contract.md` when evaluating completion, not as an
entry bundle. Its fresh evidence, Review and applicable learning gates remain.

Continue task-related reads, minimal edits, required/relevant local checks and
fixes for failures introduced by this change without asking at each step.
Stop if scope expands, a protected boundary is touched, an existing approval
gate applies, or required evidence/authority is missing. Use
`references/openspec-decision-rule.md` when classification is uncertain.

## Other applicable gates

- Proceed without OpenSpec artifacts.
- Direct change means no proposal gate; it does not mean skipping code facts, scoped evidence, TDD/debugging, or verification when those gates apply.
- Still read applicable local instructions such as `AGENTS.md`.
- Use `superpowers:systematic-debugging` before changing code for unexplained failures.
- Outside the compact local exception above, use
  `superpowers:test-driven-development` for bugfix code and behavior changes.
  Once selected, its complete gates apply. A test-only addition should pass
  against current runtime behavior and uses focused verification instead; do
  not claim runtime behavior changed.
- Use the profile-appropriate Step Evidence Gate when the direct change is more
  than a typo, formatting, comment, small config-only, review-only,
  proposal-only, docs-only, or test-only task. Low-risk work normally uses
  `compact`; approved public/API restoration remains `strict`.
- New feature behavior still requires OpenSpec unless it is already covered by an approved spec.
- Public/user/operator-visible restoration requires an approved existing spec or
  equivalent project-authoritative contract whose exact path is recorded in
  Gate 0; it must not introduce schema, compatibility, or lifecycle behavior.
- Provide verification evidence before claiming completion.
- Do not create OpenSpec artifacts or Superpowers plans unless the user explicitly asks for them.
- Always Review before completion: a focused inline diff/self-review is enough
  for `compact`; use a distinct review pass if risk or scope becomes standard.
- Preflight Review the scoped execution outline before implementation outside
  the compact local exception above; external dispatch retains its Handoff gates.
- If external execution is requested, create a profile-appropriate
  schema-version-3 Handoff Contract and hand the batch to
  `codex-brief-antigravity-review`; only low-risk Direct Change defaults to
  `compact`, while approved public/API restoration remains `strict`.
- Any Review finding returns to fix -> verification -> Review on the same
  scope. `FAIL` or `BLOCKED` is not completion.
