# Draft-v2 proposal verification

Author: elvis. Date: 2026-10-10. Status: draft-v2 approved; execution readiness blocked.
Owner: align-native-root. No native mutation is recorded or claimed complete.
Draft-v1 raw artifacts and its original validation record are preserved under
`revisions/draft-v1/`; r2 plan/feedback/candidate remain unchanged.

## Exact draft-v2 bindings (immutable approved copies under revisions/draft-v2)

| Artifact | SHA-256 |
|---|---|
| proposal.md | `ec14b519e47e6e4c459f6a3aa511c1c0ecc26d73534b03b2bb683c7f75c816c6` |
| design.md | `ef9b214e3757de94ab4460a8974875b609821458db69bff76dfdb708aa2f0c69` |
| tasks.md | `aa678998ed2653f007cde3baf77c37cfde45c5465f42e8d9055226e8f87a7867` |
| specs/skill-workflow-governance/spec.md | `bd2cbb8dd6ed1baf78d977564adc2d9b9c904f4ef6e3e11f88d9f606f6abaf8b` |
| docs/review/2026-10-10-native-agent-adaptation-r2-candidates.json | `662c5fc5547f610b5175dad81a8c0cd59f9eeebc0f03f15f7a361d9279a768f9` |
| docs/superpowers/plans/2026-10-10-native-agent-adaptation-next-r3.md | `5774b3999556aa1f157538a743211260642906741c1c98001f1df3b0aaa2ba5b` |
| docs/review/2026-10-10-native-agent-adaptation-feedback-r3.md | `3166158892dc9eacf949b9b33706f36975805714d519a65eca894d39f4954f88` |
| docs/review/2026-10-10-native-consumer-preparation-r3.json | `f890e1e613b24f6042ac65cbc59476e4bc545edbc361b063fe34426b7f693e1f` |
| docs/review/2026-10-10-native-consumer-codex-prompt-inspection.json | `9241a54fa845f2ad5463c137bc2220494141aa7b193794d59b8185cb8a1b1f81` |

## Fresh verification

- `openspec validate align-native-consumer-projections --strict`: exit 0 after
  draft-v2 proposal/design/spec/tasks and r3 plan/feedback were formed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .`: exit 0.
- Six complete candidate reconstructions, exact-text digests, preserved byte
  digests/lengths and current native prestate/modes match the unchanged r2 JSON.
- Six isolated candidate replacements/restorations through existing
  `atomic_replace` pass; original modes restored, including Claude 0600.
- Nine existing focused drift/link/swap/recovery regressions pass with no
  skip/failure/error. Full source implementation suites are not newly claimed.
- Separate unchanged Grok managed-body byte equality and canonical parity pass.
- Two native `codex debug prompt-input` commands exit 0 under default and
  account-A roots; each exposes its own complete AGENTS body once. Scope is
  native prompt assembly only, no project projection, model call or behavior.
- Native input-list output did not expose the complete model_instructions body;
  that observation neither proves inactivity nor completes source qualification.
- Ten local links in r3 plan/feedback resolve. All implementation tasks remain
  unchecked. Six live target hashes/modes, candidate JSON and r2 history remain.
- Private fixture and prompt-inspection directories were removed after checks;
  no full personal file, raw prompt output or model trace was promoted.

## Advisory disposition and owner self-review

Grok, Cursor and claudex advisory inputs have been received. Claudex found no
candidate defect requiring replacement, and its three clarifications now enter
this draft: explicit digest boundary, pre-write versus post-write evidence
phases, and P4 formal-body prefix rejection. Its reported session/identity
remains user-supplied advisory provenance, not an independently certified gate.
No repeat full design advisory is requested for the unchanged six candidates.

Focused owner review accepts this proposal as reviewable. It checks actual
text, hashes, strict spec scenarios and metadata; it does not sign independent
Preflight, implementation Review or final Review. It retains the personal
prefix rules and publisher first-line incompatibility instead of rewriting
existing evidence or broadening scope.

## Pending approval and implementation gates

Specific draft-v2 approval is recorded in `approval.md`. Private native command
and backup preparation now exists with 20 command-level fixture cases and
independent advisory correction; actual entry/source/event mechanisms and
independent Preflight remain pending. Cursor observation is blocked, and actual
Claude launcher startup rewrites credential-bearing runtime settings excluded
by the approved contract. See the new execution evidence and proposed Codex-first
amendment; no native write is authorized by those preparation records. `event-mechanism-qualified` must pass before writes;
`native-load/behavior-accepted` must pass on the installed candidate afterward.
P4 is a defined negative scenario, not a newly observed native model PASS.

No skill source behavior, installed rule, publisher, hook, credential,
Superpowers link, other active spec or Git write is part of this proposal-only
turn. Pi/agy and seven-name/eight-config equivalence remain excluded from this
native write slice. The current records cannot authorize apply or publication.

## Approved continuation verification

- Existing full source suite: 492 tests, exit 0, fresh in this continuation.
- Private execution fixture suite: 20 cases, failures 0; six apply/restore pairs
  and actual inode/content/link/type/receipt/authority/candidate-drift negatives.
- Distinct advisory reviewer independently reproduced three command defects,
  then verified correction and 20/20 cases; this is not formal Preflight.
- Strict OpenSpec/core checks pass; `check` validates the six-file package only.
- Native bytes/modes/identities remain unchanged; private root 0700 and files
  0600. Backups remain owned by align-native-root while blocked, outside discovery.
- No native model/session launch, publisher or Git operation occurred.
- Current implementation Plan and sanitized evidence live under existing
  docs/superpowers/plans and docs/review paths. Native acceptance remains pending.
