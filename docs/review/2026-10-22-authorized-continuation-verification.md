# Implementation verification

Change: `reduce-redundant-confirmation-and-review-overhead`. This is slice
evidence; whole-task completion remains pending Final Review, runtime sync and
scoped publication. The tested clean candidate starts at source commit
`1242605fc4bb52c5644027697d71587e4a9dcc74`; unrelated integration changes are
excluded. Paths/lines below refer to that candidate plus this owned delta.

## 1. Goal and boundary

Strict Major Self-Evolution, specifically approved draft-v2. Remove redundant
confirmation/formatting and advisory ceremony without weakening authority,
identity, freshness, transport, Review or completion. Preflight r2 PASS precedes
implementation. No grok-cc/Companion implementation, native configuration or
unrelated change is included.

## 2. Code facts

| Fact | Candidate evidence |
| --- | --- |
| Entry checks exact existing authorization before routed stops/confirmation | `SKILL.md:87` |
| New lease identifies immutable approval; historical exact bindings remain | `references/confirmation-lease.md:37` |
| Authorized remediation is distinct from advancing a blocked gate | `references/approved-implementation-workflow.md:218` |
| Complete inline facts satisfy already-eligible compact reporting | `references/step-evidence-gate.md:258` |
| Cloud advice does not become execution handoff or formal PASS | `references/local-instruction-checkpoint.md:64` |
| Actual validator tests require explicit covered external authority | `tests/test_workflow_rules.py:4615` |
| Exact dimensions, all nine flags and revoked/deferred state reject | `tests/test_workflow_rules.py:4631` |
| Real source/Plan edits retain contract hash; stale recovery and changed approval reject | `tests/test_workflow_rules.py:5260` |

## 3. Positive checks

Existing production validators already support legal lease reuse; no validator
or schema change was needed. Three focused test methods passed before rule
changes and after them. This is preservation coverage, not fabricated RED.
The semantic RED is five agents demanding a redundant table; five fresh matched
after agents now accept complete inline facts. All other baseline decisions
remain correct. See `2026-10-22-authorized-continuation-forward.md`.

## 4. Negative checks

Actual tests reject absent business authority, unlisted action, changed bound
revision/hash/scope/risk, nine invalidation flags, revoked/deferred provenance
and invalid status. Real stale source fingerprints reject recovery even while
the unchanged approval lease reuses. Additional fresh-agent probes reject new
push targets, force-push, missing evidence, owner impersonation, unknown-send
replay, missing Major approval and high-risk compact-report shortcuts.
The Non-negotiables block and all validator bytes are unchanged in the owned
delta. The Direct Change reference and Companion are unchanged.

## 5. Cause

Broad stop wording obscured the already-supported authorization predicate;
approval-object identity was not named clearly; the signoff list unconditionally
demanded a table despite compact presentation eligibility. No claim is made that
all user-reported friction reproduced in the seven baseline cases.

## 6. Minimal correction

Clarify existing predicates and evidence representation in five portable files;
add two validator test methods and extend one stale-input test. No state machine,
registry, schema, runner, transport or new mandatory report was introduced.

## 7. Owned scope

`SKILL.md`, four references (approved workflow, lease, step gate, local checkpoint),
`tests/test_workflow_rules.py`, `CHANGELOG.md`, and this change's required approved
governance/review artifacts. Implementation is still in an isolated clean
candidate; dirty integration source and runtime files have not yet been changed.

## 8. Commands

In the clean candidate: installed `quick_validate.py .` with cached PyYAML;
`python3 scripts/validate_core_gates.py .` in both supported parser modes;
`python3 -m unittest discover -s tests -v` in both modes; named strict OpenSpec
validation; focused three-method validator regressions; archive-compatible
no-index whitespace comparison. Python bytecode writes were disabled.

## 9. Results and environment correction

- Quick validation, core validation in both modes, strict OpenSpec: PASS.
- Full fallback suite: 472 tests, PASS, 74.587 s.
- Full PyYAML suite: 472 tests, PASS, 73.634 s.
- New/extended focused validator methods: 3 tests, PASS before and after rules.
- Matched agent decisions: five fresh samples, seven cases each; additional
  adversarial decision exercise passed the described boundaries.
- Companion source quick/templates and 91-test fallback suite: PASS.
- Companion installed Codex runtime quick/templates: PASS, unchanged files.

The Plan's direct Companion runtime unittest command failed at discovery because
portable installation does not contain `tests/`. This is a test-harness/layout
error, not an assertion regression or reason to install tests into runtime.
A private exact runtime copy was supplemented only with the source `tests/`,
`README.md`, `README_cn.md` and `AGENTS.md` needed by that suite. Intermediate
fixture attempts exposed the omitted README and AGENTS harness inputs; after
supplying them, all 91 tests passed in 0.121 s. A directory comparison confirmed
that those four harness additions were the only differences from installed
runtime. This tests installed payload bytes using the source harness, not
native loading or a claim that tests ship in runtime. No runtime/Companion edit
or protected-boundary change was required; retain the frozen reviewed Plan and
record this same-scope command correction here for Implementation Review.

## 10. Self-review

The matched after fixture preserves every unrelated integration instruction;
its five owned deltas equal those in the clean candidate. No validator comparison,
product identity, assignment, transport or required Review gate was removed.
Agent results, not wording assertions, support the changed instruction behavior.
The requested cloud report was completely checked and locally evaluated; it
remains advisory, never formal readiness or project acceptance.

## 11. Remaining gates

Independent Implementation Review, learning closeout, integration verification,
reviewed four-target sync, fresh final evidence/Final Review, reconciliation,
tested indexed-tree publication and owned cleanup remain pending. Existing
unrelated source/runtime material remains user-owned and outside publication.

## 12. Next-step permission

Independent Implementation Review may inspect this complete candidate and
evidence. Integration/runtime advancement waits for its PASS. Whole-task
completion is not claimed by this report.
