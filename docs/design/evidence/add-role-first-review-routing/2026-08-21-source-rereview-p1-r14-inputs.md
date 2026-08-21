# Candidate Source High Re-review — P1 R14 bounded inputs

## Assignment

- product/role/profile: `codex` / `independent-reviewer` / `control-plane-high`
- implementation: fresh no-history `gpt-5.6-luna`, `max` reasoning
- purpose: decide whether R14 closes the remaining R13 generic/Pi cleanup P1
  and whether read-only four-target runtime verification may resume
- authority: source Review evidence only; no mutation, self-acceptance,
  canonical transition, runtime plan, runtime inspection, or completion claim

Read Router and Companion `AGENTS.md`/`SKILL.md`, the approved
OpenSpec/Plan, engineering invariants and closeout contract, prior R5 PASS,
R11/R12/R13 FAIL Reviews, then every bound R14 record. Review the complete
current delta without Git. Return `PASS`, `FAIL`, or `BLOCKED`; any
P0/P1/P2 blocks promotion.

## Exact bindings

| Input | Mode / SHA-256 |
|---|---|
| approved Plan | `0644` / `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| prior Source R5 PASS | `0644` / `073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4` |
| prior Source R11 FAIL | `0644` / `0d89c219a344f9943d9f324d4f36fc0cbb4ec503fc0bce0eb0ceb91912981d62` |
| prior Source R12 FAIL | `0644` / `35c38b467e5d2bacc4fdd90708c41801f36b494810a5ed4ea33b5b8fee24abc0` |
| prior Source R13 FAIL | `0644` / `5b7ffc4fb35a1072454145f3f1e104a21c4fa2bad28f9d7cab7ae82f5a823b17` |
| source verification | `0644` / `6173624440308a6330c3c91659f67870be8c989ef035c7abd60eb8208ce4a04a` |
| durable R13 delta summary | `0644` / `2ebfc39e4225adbbb6327925ae7bd0e4d0fdbbe907c750bb055611e4a47bc9ab` |
| corrected R14 script | `0644` / `939dc80effdd605fea745291c02dd1079b9f0ebdfa72e8a467942c92775502d0` |
| corrected R14 tests | `0644` / `6a25c1cbf6eecbf12cec695d29fda09488786017b76d821047f90ccfb69328a7` |
| Pi prompt | `0644` / `9cba75f75a714110d5efa3a9ff21112f51367a6626e3fdaea596b16544ff04c1` |
| R14 implementation backup root | `0700` / `/private/tmp/add-role-first-review-routing-p1r14-20260821-luna` |

The authoritative R13 delta and compare root remain bound by the R13 input:
private delta mode `0600` SHA
`d6c959d118e5f7bcf9f691131c1126be637c683bc03cd10fdb14ea4935113d48`,
bindings `fded0c8cc1f93e9591926118cac6c9d4ff838c980da7eedf79c9c0aadb46fa37`,
allowlist 93 entries SHA
`3531c68cbbb41b4de9e271adb51dbfc22367555565faeaabd4d064125e78ed98`,
compare root mode `0700`, and R13 result `89` actual with
`unexpected_paths: []`. The R14 delta must preserve the prior R12
allowlist failure and use a fresh mode-`0700` compare root. Intended R14
Review must start absent:
`docs/design/reviews/2026-08-21-add-role-first-review-routing-source-rereview-p1-r14.md`.

## Required adversarial decision

Trace exact production mechanisms with isolated temporary probes only:

1. Reproduce the retained-inode-moved-aside-without-unlink interleaving for
   generic and Pi cleanup while an unrelated inode replaces the cleanup name.
   No unrelated inode may be deleted or accepted.
2. Verify ownership-preserving atomic quarantine/no-replace claims the exact
   retained inode, rejects collisions/mismatch, fsyncs the directory, and
   unlinks only the revalidated quarantined object. Any uncertainty must leave
   visible recovery/blocked residue.
3. Recheck all R13 rollback, Pi rename-side-effect, blocked-evidence,
   descriptor/ctime, parent/receipt, sandbox, native/network and hidden-residue
   invariants. Do not run Pi, inspect runtime destinations, or create a plan.
4. Rebind the complete no-Git delta, compare root, durable summary, source
   verification, input, and all start/end hashes/modes. Keep Task 10 as the
   approved external limitation.

Bound implementation evidence: focused RoleFirst `47/47 PASS`,
cross-CLI `142/142 PASS`, workflow `124/124 PASS`, core validator
`PASS`, and quick validation `PASS`. Rerun relevant production probes
and required validation checks independently.

## Output

Return one neutral Markdown Review with assignment/independence, bindings,
complete delta classification, exact mechanism/test/probe trace, P0/P1/P2,
resume conditions, final verdict, and whether runtime verification may resume.
Do not write files, run Git/Pi, inspect runtime destinations, create a plan, or
claim completion.
