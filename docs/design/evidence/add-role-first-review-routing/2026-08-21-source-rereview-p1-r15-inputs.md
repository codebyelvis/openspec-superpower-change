# Candidate Source High Re-review — P1 R15 bounded inputs

## Assignment

- product/role/profile: `codex` / `independent-reviewer` / `control-plane-high`
- implementation: fresh no-history `gpt-5.6-luna`, `max` reasoning
- purpose: decide whether R15 closes the R14 final-quarantine unlink P1 while
  preserving safe cleanup semantics on Darwin/POSIX
- authority: source Review evidence only; no mutation, self-acceptance,
  canonical transition, runtime plan, runtime inspection, or completion claim

Read Router and Companion `AGENTS.md`/`SKILL.md`, the approved OpenSpec/Plan,
engineering invariants and closeout contract, prior R5 PASS and R11/R12/R13/R14
FAIL Reviews, then every bound R15 record. Review the complete current delta
without Git. Return `PASS`, `FAIL`, or `BLOCKED`; any P0/P1/P2 blocks promotion.

## Exact bindings

| Input | Mode / SHA-256 |
|---|---|
| approved Plan | `0644` / `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| prior Source R5 PASS | `0644` / `073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4` |
| prior Source R11 FAIL | `0644` / `0d89c219a344f9943d9f324d4f36fc0cbb4ec503fc0bce0eb0ceb91912981d62` |
| prior Source R12 FAIL | `0644` / `35c38b467e5d2bacc4fdd90708c41801f36b494810a5ed4ea33b5b8fee24abc0` |
| prior Source R13 FAIL | `0644` / `5b7ffc4fb35a1072454145f3f1e104a21c4fa2bad28f9d7cab7ae82f5a823b17` |
| prior Source R14 FAIL | `0644` / `21c8af525ada608343c9498697020d9dbd28a763bf461b4218ff4451a8b77cc5` |
| source verification | `0644` / `b219726855c17c8e0bd50005aadcbbc05d5e06bb7bead7e4b60be00312665335` |
| durable R14 delta summary | `0644` / `bf7b42c48e582723c76c739be1188de13e3a7cc453e8c8c793c162308de3f692` |
| durable R15 delta summary | `0644` / `0e117004c83b30a68d4b76d86dcc52cf80ba0be9436f78ff78fb2fdf6c58413c` |
| corrected R15 script | `0644` / `f4759f7e4f73576cfd6db3a8398ad43944a6ad7f9b6db968964c0444c03a881` |
| corrected R15 tests | `0644` / `5557cb2cdea3d95ae2cbf09a1c5420bb7faa4729829d81c8f0ca9859b7e9b063` |
| Pi prompt | `0644` / `9cba75f75a714110d5efa3a9ff21112f51367a6626e3fdaea596b16544ff04c1` |
| R15 implementation backup root | `0700` / `/private/tmp/add-role-first-review-routing-p1r15-20260821-luna` |

The authoritative R14 delta remains bound by the R14 input: private delta
mode `0600` SHA
`efce4e61a90ff14b9893cb852e2f09468e3af9be0e9c3857116587290c063e2f`,
bindings `8877e931ef9d12f5e093ced04f15ef3517f3fead4cfe1e9f43055b8db56ee42e`,
allowlist 96 entries SHA
`03fd6da52bd02345c595b370af0eebc47dce41dbd9e5046b8b0af2f0730c898d`,
compare root mode `0700`, and R14 result `92` actual with
`unexpected_paths: []`. The R15 delta must rebind both repositories against
the same reconstructed R9 baselines with a fresh mode-`0700` compare root.
Intended R15 Review must start absent:
`docs/design/reviews/2026-08-21-add-role-first-review-routing-source-rereview-p1-r15.md`.

## Required adversarial decision

Trace exact production mechanisms with isolated temporary probes only:

1. Reproduce replacement after the final retained-inode bind and before the
   deletion boundary for generic and Pi cleanup. No unrelated inode may be
   deleted or accepted.
2. Verify that Darwin/POSIX lacks an inode-CAS unlink primitive and that R15
   therefore fails closed without ordinary name-based deletion when exact-owner
   deletion is unavailable. Any uncertainty must leave visible recovery and/or
   mode-0600 blocked evidence; Pi must not leave PASS-shaped evidence.
3. Recheck all R11/R12/R13/R14 rollback, Pi rename-side-effect,
   blocked-evidence, descriptor/ctime, parent/receipt, sandbox, native/network
   and hidden-residue invariants. Do not run Pi, inspect runtime destinations,
   or create a plan.
4. Rebind the complete no-Git delta, compare root, durable summary, source
   verification, input, and all start/end hashes/modes. Keep Task 10 as the
   approved external limitation.

Bound R15 implementation evidence: focused P1 `6/6 PASS`, cross-CLI
`148/148 PASS`, Router workflow `124/124 PASS`, core validator `PASS`, and
quick validation `PASS`. Rerun relevant production probes and required
validation checks independently.

## Output

Return one neutral Markdown Review with assignment/independence, bindings,
complete delta classification, exact mechanism/test/probe trace, P0/P1/P2,
resume conditions, final verdict, and whether runtime verification may resume.
Do not write files, run Git/Pi, inspect runtime destinations, create a plan, or
claim completion.
