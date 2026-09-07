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
