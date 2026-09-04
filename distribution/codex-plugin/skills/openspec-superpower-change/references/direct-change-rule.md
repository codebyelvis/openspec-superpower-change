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

Rules:

- Proceed without OpenSpec artifacts.
- Direct change means no proposal gate; it does not mean skipping code facts, scoped evidence, TDD/debugging, or verification when those gates apply.
- Still read applicable local instructions such as `AGENTS.md`.
- Use `superpowers:systematic-debugging` before changing code for unexplained failures.
- Use `superpowers:test-driven-development` for bugfix code and behavior
  changes. A test-only addition for already-defined behavior should pass
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
- Compact low-risk Direct Change does not create OpenSpec artifacts or a
  Superpowers plan. Profile-driven escalation may require one short Plan even
  when the user did not explicitly request it.
- Always Review before completion: a focused inline diff/self-review is enough
  for `compact`; use a distinct review pass if risk or scope becomes standard.
- Compact low-risk Direct Change uses an inline readiness check and does not
  create a standalone Brief, Plan, or Preflight artifact. Escalate to one short
  Plan and profile-appropriate Preflight only when standard risk, coordination,
  external execution, multiple slices, or a protected boundary requires it.
- If external execution is requested, create a profile-appropriate
  schema-version-3 Handoff Contract and hand the batch to
  `codex-brief-antigravity-review`; only low-risk Direct Change defaults to
  `compact`, while approved public/API restoration remains `strict`.
- Any Review finding returns to fix -> verification -> Review on the same
  scope. `FAIL` or `BLOCKED` is not completion.
