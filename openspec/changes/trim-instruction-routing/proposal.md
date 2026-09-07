# Change: Trim instruction routing

Revision: `v1`
Status: `approved for scoped implementation`
Approval: user explicitly stated “批准 trim-instruction-routing v1 的具体范围”.
Subsequent local autonomy covers safe implementation choices without repeated
confirmation. After the concrete validator/test/runner incompatibilities were
reported, the user directed “继续闭环推进” and required analysis, repair and
continuation instead of another handback. This authorizes the specific
compatibility follow-up below, not unrelated gate or product changes.

Approved compatibility follow-up to v1: update only
`scripts/validate_core_gates.py`, `tests/test_workflow_rules.py`,
`tests/run_role_first_review_forward_tests.py` and
`tests/fixtures/superpowers-routing-cases.json` as needed to follow the new
instruction owners and bounded compact selection. Preserve existing negative
checks for missing/decoy owner content, approval, evidence, authority and parser
integrity. No new tests, runner, schema or framework. Existing source verification,
forward evidence, Review and exact-file runtime sync remain required.

Local sync compatibility amendment (delegated approval recorded before edits):
the user's explicit instruction “我授权你自己遇到待批准的思考后按你推荐的批准
闭环推进 本地不再询问” authorizes the control plane to resolve this local
follow-up. All four runtimes already share identical pre-existing changes in
`references/self-evolution-rule.md`, `references/cross-cli-sync.md`,
`references/sync-checklist.md`, and `scripts/validate_cross_cli_sync.py`.
Preserve those exact runtime bytes in the canonical source, rather than
overwriting user changes or hiding assertion drift with a composite snapshot.
The first difference recommends representative fast/strict forward scenarios;
this task still runs every already-required check. The other three accept Grok
`configToml` discovery only through one earlier same-plan verified target,
full-closure parity and bound receipt/content evidence, with descriptor-bound
inspect reading. Do not add other discovery sources, alter native configuration,
waive parity, change future Major approval, or add a framework/test matrix.
Back up these four source preimages, run existing checks, Review the complete
amendment and exact-file sync plan, then verify every required runtime.
Independent reviewer `/root/preflight` confirmed this delegated authority;
reviewer evidence is not itself the authorization.

## Why

Eric Provencher's [original article](https://x.com/i/article/2095989703967125509),
linked by [his post](https://x.com/pvncher/status/2095991462416490862), recommends
short selection descriptions, a minimal root router, contextual repository
instructions, explicit safe authority, and completion criteria. The complete
article body was read through the FxTwitter mirror of the original post after
X returned HTTP 403; no translated summary substitutes for the original.

Observed conflicts in this repository:

- `SKILL.md` permits a one-line micro-change Gate 0 but requires Preflight for
  every implementation and TDD for every bugfix.
- Its Read Matrix stacks implementation, Direct Change, checkpoint and
  completion references; long role, output-mode and execution details remain
  in the root as well as their owners.
- `direct-change-rule.md`, `superpowers-adapter.md` and `response-patterns.md`
  repeat mandatory TDD/Preflight selection for localized fixes.
- `completion-contract.md` unconditionally starts Learning Closeout, while
  `project-learning-closeout.md` identifies correction/history and explicit
  archive requests as its entry conditions.
- `AGENTS.md` requires the full repository suite before completion. This is a
  current required check, not permission to skip it during this cleanup.

## Scope and short review draft

This is Major Self-Evolution: trigger scope, request routing and Superpowers
selection change; contextual completion loading also needs approval. Approval
must name `trim-instruction-routing` revision `v1`. It is not inherited from
another active change or from the request to start work.

| Action | Exact files and purpose |
|---|---|
| Shorten | `SKILL.md`: description, Gate 0 and task-based reference routing |
| Move | Root execution/Review/sync/handoff details to their existing owners; output presentation to `references/response-patterns.md` |
| Remove unconditional selection | `references/direct-change-rule.md`, `references/superpowers-adapter.md`, `references/request-modes.md`, `references/approved-implementation-workflow.md`, `references/response-patterns.md`: bounded small-work exceptions and unchanged-scope continuation |
| Make reads contextual | `references/local-instruction-checkpoint.md`, `references/completion-contract.md`: affected context and conditional learning entry |
| Clarify verification scope | `AGENTS.md`, `references/step-evidence-gate.md`: acceptance/blast radius plus all change-class required checks |
| Preserve | All Non-negotiables; `references/openspec-decision-rule.md`, `references/self-evolution-rule.md`, learning promotion thresholds, Handoff/schema/authority rules and existing validators/tests |

No new skill, mode, profile, reference file, framework, product behavior,
validator, test, dependency, ledger or test matrix. The compatibility follow-up
above adjusts existing validation only. No other skill/source edit.
Existing approval, independent Review and runtime-sync obligations remain;
this proposal cannot authorize bypassing them. Existing untracked work is excluded.

### Exact proposed rule snippets

Description (selection boundaries first):

> Use for file/behavior changes, change classification, OpenSpec/Direct Change routing, evidence-based completion, archive/distillation, or skill self-evolution. Excludes ordinary questions, standalone wording/read-only diff review, and valid handed-off batches.

Root and Direct Change (one normative owner, root points to it):

> For an obvious, local, reversible change that does not touch a protected
> boundary, record all Gate 0 facts in one line, make the minimum edit, run
> relevant verification and required checks, then record a focused diff/self-
> review and finish. Do not require a separate Plan, Preflight, full TDD cycle,
> Domain Context checklist, grill, Handoff, independent multi-agent Review or
> Learning Closeout solely because files change. Behavior fixes still require
> regression evidence and compact slice signoff. Diagnose an unexplained cause
> before fixing it. Select Superpowers methods only for the current phase;
> once selected, preserve their complete gates.

Reading and root reduction:

> Read applicable local instructions and only the references needed for the
> current decision. A clear compact Direct Change reads its rule; behavior
> evidence reads Step Evidence Gate; ambiguous classification reads the
> OpenSpec decision rule. Consult the completion owner at completion, not as
> an implementation-entry bundle. Read context only for affected terms; load
> Review assignments, Handoff, sync and presentation details when used.

Safe continuation:

> Within existing authorization, continue task-related reads, minimal edits,
> required and relevant local checks, and fixes for failures introduced by
> this change without asking at each step. Resume an approved unchanged scope
> from its current canonical state without restarting proposal, approval,
> completed planning or unaffected checks. Preserve outstanding contract gates.

Verification and closeout:

> Run every check explicitly required for the current change class, then any
> additional verification justified by acceptance or demonstrated blast radius.
> This skill does not impose a full suite on every downstream task. In this
> skill repository, retain quick validation for self-evolution, core-gate
> validation and both parser paths; routing/governance changes retain the full
> existing unittest suite. This Major cleanup runs all currently required checks.
> Re-run affected checks after new edits or relevant failures; record unrelated
> failures as OUT_OF_SCOPE_PREEXISTING_DEBT without broadening the task.
> Load Learning Closeout for correction/Review history or explicit archive and
> distillation; preserve every mandatory promotion trigger and completion block.
> Fresh verification and profile-appropriate Review PASS remain mandatory.

Stops and protected boundaries:

> Stop for scope expansion, an existing approval boundary, conflicting contract
> semantics, missing required evidence, production/credential/destructive or
> separately authorized external actions, Git writes or push. A small-fix label
> never bypasses new-feature, public-contract, API/schema, persistence,
> security/permissions, workflow-routing or other existing OpenSpec boundaries.
> Major self-evolution still requires explicit approval of its exact OpenSpec
> change before implementation. Model identity grants no additional authority.

## Acceptance and verification

The attached delta defines the bounded routing cases; it is a review contract,
not a new executable test matrix. Before implementation, take a fresh structured
backup and record the explicit approval. Use one scoped implementation slice;
no duplicate design approval or unrelated Plan/Preflight/TDD ceremony. Preserve
the existing required Major forward-test and independent Review gates.

- Before asking approval: `openspec validate trim-instruction-routing --strict`.
- After approved edits: existing `quick_validate.py` with PyYAML,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .`, and
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`.
  Run the required validator/suite with PyYAML and the dependency-free fallback.
- Reuse existing isolated routing/lifecycle forward-test facilities for
  before/after evidence of the attached cases. Add no tests or runner. Record
  actual reads/results; do not claim measured token savings from file size.
- Inspect the complete scoped diff for broken links, duplicate or contradictory
  owners, protected-boundary retention and no unrelated writes. If an existing
  assertion pins text to the old location and fails, report the conflict;
  apply only the approved compatibility follow-up above and never waive the check.
- Before runtime writes, apply the existing sync checklist and exact changed-file
  target plan/verification requirements. Never mark source-only edits as a
  completed portable installation; missing required authority/parity blocks it.

## Rollback and approval

Pre-draft backup contains source instructions and the runtime instruction
preimage outside discovery roots. Before implementation refresh that backup
and retain its path in local evidence. Restore only files changed by this task
from their preimages if rollback is needed; do not overwrite unrelated work.
Follow existing backup retention/cleanup and runtime rollback rules.

Approval is recorded above. No staging, commit, push or publication is
authorized. Items that would weaken signoff, Non-negotiables, mandatory
checks, learning promotion or Major approval are excluded even after approval.
