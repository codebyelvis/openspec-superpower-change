# add-skillsmp-index-adapter Preflight Review

## Reviewer Assignment

- Review purpose: decide whether the current OpenSpec contract and
  implementation plan may enter implementation
- Reviewer product: `codex`
- Reviewer role: `independent-reviewer`
- Capability profile: `control-plane-high`
- Independence: `distinct-instance`
- Result authority: `governed-review-evidence`
- Reviewer instance: `01a066e4-54ca-7d00-b8eb-3e149d90f90c`

## R1

- Verdict: `BLOCKED`
- Findings: the first plan coupled Codex plugin and repository adapter mutation
  without atomic failure/ownership semantics; RED coverage did not explicitly
  include special files and parent-path symlinks; proposal validation status
  was stale.
- Required correction: isolate the adapter builder, define owned output and
  recovery semantics, add the missing negative tests, and synchronize the
  strict-validation result.

## R2

- Verdict: `PASS`
- Critical findings: none
- Important findings: none
- Minor findings: none
- Evidence accepted:
  - `openspec validate add-skillsmp-index-adapter --strict`: PASS
  - `git diff --check`: PASS
  - isolated baseline: quick validator PASS, core gates PASS, 324 tests PASS
  - the focused builder, reserved output namespace, staged replacement,
    identity recheck, restoration/residue behavior, and complete RED matrix are
    explicit in the revised design and plan
- Decision: implementation may begin within the approved scope.

## R3

- Verdict: `BLOCKED`
- Findings: the amended descriptor-relative design was not yet synchronized
  with the RED seam signatures, and the corrective matrix did not yet prove
  parent rebinding, hard-link rejection, source drift, transaction residue,
  and missing platform primitives.
- Required correction: fix the exact fd-plus-entry seam signatures in the plan,
  add the corrective RED matrix, and update the OpenSpec implementation ledger.

## R4

- Verdict: `PASS`
- Critical findings: none
- Important findings: none
- Minor findings: none
- Evidence accepted:
  - `openspec validate add-skillsmp-index-adapter --strict`: PASS
  - `git diff --check`: PASS
  - focused RED suite: 69 tests, 49 PASS / 20 expected FAIL, with no errors,
    skips, or hangs
  - independent RED specification review: PASS
  - independent RED test-quality review: PASS
  - exact descriptor-plus-entry seams and corrective coverage for repository
    and `skills/` rebinding, hard links, source drift, transaction residue, and
    missing `O_NOFOLLOW`, `O_DIRECTORY`, or `dir_fd` support
- Decision: production implementation may resume for tasks 2.4 and 2.5 within
  the approved SkillsMP adapter scope.

## Authority Boundary

This review authorizes implementation entry only. It does not authorize Git
staging/commit/push, runtime synchronization, npm publication, external
submission, OpenSpec archive, canonical completion, or self-acceptance by the
executor.
