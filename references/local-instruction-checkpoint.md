# Local Instruction Checkpoint

Read applicable local instructions before acting. Consult this reference when
affected local/domain context needs checking; it is not an every-edit bundle.

## Required first checks

1. Read root `AGENTS.md` when it exists.
2. Read `openspec/AGENTS.md` when OpenSpec work or files in its scope are involved.
3. Inspect existing OpenSpec specs and active changes when OpenSpec may apply.
4. Check `CONTEXT.md` according to the rules below.
5. Decide the request mode.

## CONTEXT.md checkpoint

For OpenSpec work, discovery, domain-language changes, boundary changes, or iterations that introduce or alter domain terms:

- This checkpoint is mandatory.
- If `CONTEXT.md` does not exist, create it by extracting established domain terms from architecture docs, code, and existing specs.
- If it exists, verify it covers terms introduced or affected by the current change and add missing entries before proceeding.
- In a Git repository, canonical shared `CONTEXT.md` / `CONTEXT-MAP.md` must not be intentionally ignored.
  An ignored local copy cannot satisfy durable shared promotion. Active changes
  may remain untracked or modified because this check does not require `git add`, commit, or push
  without separate authorization.

For localized direct bug fixes and low-risk direct changes:

- Read existing `CONTEXT.md` only when affected terms need clarification.
- If it is missing or irrelevant, state the scoped assumption and continue.
- Do not create or update glossary files solely to perform a small fix.

Never let glossary updates replace proposal, spec, code, or verification evidence.
Use `project-learning-closeout.md` when corrections or Review findings need
project-level promotion; do not put implementation chronology in the glossary.

## Mode decision

Choose one mode:

- review-only or non-implementation;
- direct change;
- discovery first;
- OpenSpec proposal first;
- approved implementation.

Resolve uncertainty with `openspec-decision-rule.md`: possible protected effects
require OpenSpec; a localized restoration with no such effect may record its
scoped assumption and continue. Do not run a whole-repository context audit.

## Native agent consumption

When auditing or adapting an actual entry, record its real product, launcher,
active configuration root, native instruction sources, discovered skill paths,
Superpowers dependency path and SHA-256, delivery policy and observed evidence.
A missing private skill directory does not prove missing shared discovery.
A discovery catalog or another account's parity does not prove native loading, behavior or authority.
Only the existing bound instance and contract grants control-plane authority.

Claude Code and Cursor are content consumers and advisory reviewers, not
schema-6 products. `claudex` and `claudeg` are Claude Code launchers; model
backends do not change product identity. Sharing content does not share
credentials, sessions, instances or permissions.

When a plan is required, form or reuse the applicable reviewed plan before
execution. Resolve its destination from the user's authorized scope, project
conventions and existing contract. A native `docs/design/` default is only a
fallback; it cannot relocate or duplicate an already-bound plan or evidence.
An incompatible request to change an immutable binding requires a newly
approved contract, never silent path replacement.

Standalone read-only advisory output defaults to chat. Explicitly requested
persistence returns to Router classification and then respects the user's
destination and the native publisher, when that publisher applies. Saving an
advisory does not make it gate-bearing. A governed external batch writes only
its bound project-relative attempt artifacts with the assigned real product,
instance, role and evidence format. Native publisher names and batch paths
cannot substitute for each other or rewrite already-bound evidence.

Check publisher applicability before constructing a saved advisory path. If the
required publisher cannot represent the authorized path and format, report the
conflict; do not bypass its guard or claim publication. Chat advisory, saved
advisory and formal attempt evidence retain their separate authority boundaries.

An alternate account or native consumer is not a fifth portable target.
Native rules, hooks and configuration outside the four managed blocks require
a separate exact path/prestate adaptation plan, appropriate approval, backup,
supported mechanism, acceptance and rollback. Do not retarget the portable
manifest or widen a publisher whitelist to avoid that boundary. In particular,
registered compatibility hooks do not prove runtime enforcement; a selective
isolation mechanism must be verified before changing unrelated protections.
