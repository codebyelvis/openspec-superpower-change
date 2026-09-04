# OpenSpec Decision Rule

Create or update an OpenSpec change when the request involves:

- new functionality;
- architecture or pattern changes;
- behavior-changing performance work;
- security model changes;
- migrations with user-visible or operator-visible impact;
- public behavior changes;
- API/schema changes;
- data lifecycle changes;
- deployment, recovery, or operator-visible behavior changes;
- broad refactors that alter system boundaries or lifecycle;
- skill workflow changes.
- agent runtime control flow, tool exposure, cache strategy, request routing, skill routing, or workflow lifecycle changes.

## Agent workflow boundary

Agent runtime, tool exposure, cache strategy, request routing, skill routing, workflow lifecycle, sandbox/security boundary, and operator-visible behavior changes default to OpenSpec-required or Discovery First. Do not classify them as Direct Change merely because the user reports a bug.

For public/user/operator-visible behavior, OpenSpec may be skipped only when an
approved existing spec or equivalent project-authoritative contract explicitly
covers the behavior, Gate 0 records its exact path, and implementation narrowly
restores that contract without schema, compatibility, or lifecycle changes.

Skip OpenSpec only for:

- internal bug fixes restoring intended behavior, or public restoration meeting
  the approved-contract rule above;
- small config-only changes without user-visible, operator-visible, security, deployment, recovery, or performance-semantics impact;
- comments, formatting, or typo fixes;
- docs-only updates without contract impact;
- tests for already-defined behavior.

If unsure and the change may affect architecture, public behavior, system boundaries, data lifecycle, security, performance, deployment, recovery, or operator-visible behavior, choose OpenSpec.

If unsure but the change appears localized and only restores already-intended behavior, treats comments/formatting/typos, adds tests for existing behavior, or changes small configuration without user-visible, operator-visible, security, deployment, recovery, or performance-semantics impact, proceed as a direct change and document the assumption.

## Global personal skill self-evolution

For global personal skill edits under a personal runtime skill directory, short-circuit only unrelated business-project OpenSpec recursion. Do not short-circuit user approval, structured backup, self-evolution gate, RED/GREEN forward-test, validation, rollback, or final reporting.

If the skill source itself is being changed inside an OpenSpec-managed product or open-source repository, and the change will be published as that repository's product behavior, require OpenSpec approval.
