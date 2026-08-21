# Candidate Source High Re-review — P1 R13 bounded inputs

## Assignment

- product/role/profile: `codex` / `independent-reviewer` / `control-plane-high`
- implementation: fresh no-history `gpt-5.6-luna`, `max` reasoning
- purpose: decide whether R13 closes all five R12 persistence P1 findings and
  whether read-only four-target runtime verification may resume
- authority: source Review evidence only; no mutation, self-acceptance,
  canonical transition, runtime plan, runtime inspection, or completion claim

Read Router and Companion `AGENTS.md`/`SKILL.md`, the approved OpenSpec/Plan,
engineering invariants and closeout contract, the prior R5 PASS, R11 FAIL, and
R12 FAIL, then every bound R13 record. Review the complete current delta without
Git. Return `PASS`, `FAIL`, or `BLOCKED`; any P0/P1/P2 blocks promotion.

## Exact bindings

| Input | Mode / SHA-256 |
|---|---|
| approved Plan | `0644` / `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| prior Source R5 PASS | `0644` / `073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4` |
| prior Source R11 FAIL | `0644` / `0d89c219a344f9943d9f324d4f36fc0cbb4ec503fc0bce0eb0ceb91912981d62` |
| prior Source R12 FAIL | `0644` / `35c38b467e5d2bacc4fdd90708c41801f36b494810a5ed4ea33b5b8fee24abc0` |
| source verification | `0644` / `4131d94996452d0832911957b7a92da6d6af84171e8cd2441c228e736985ab04` |
| durable R12 delta summary | `0644` / `aa68cddb16622de36a3d08cb1012c9084f9dfa6a1fe9c5b2f324829ecb0e26d6` |
| durable R13 delta summary | `0644` / `2ebfc39e4225adbbb6327925ae7bd0e4d0fdbbe907c750bb055611e4a47bc9ab` |
| corrected R13 script | `0644` / `fd8a05c2d8126d1202847a60d574ab65edcee238d3c00c722797db69224e3295` |
| corrected R13 tests | `0644` / `419774194a4254f6a8b253c7505c2722ad5e6509d1979a4acd0533f3df0ab689` |
| Pi prompt | `0644` / `9cba75f75a714110d5efa3a9ff21112f51367a6626e3fdaea596b16544ff04c1` |
| sanitized Pi attempt 01 | `0600` / `2cc4d107db175acce6b66d9439ea8bab191d271695d4f75df4b1302dfa2c255b` |
| R13 implementation backup root | `0700` / `/private/tmp/add-role-first-review-routing-p1r13-20260821-luna` |

The authoritative R12 delta and compare root remain bound by the R12 input:

- private delta: `0600` /
  `3e98e4015b8b461958172c538ea07798de4239d89a2ae0771a9eba1ec84c8e50`;
- bindings: `0600` /
  `b3c52f8cd141e70ab3f61d0366734c888513c5af59da4e6f089979fe24c7fd09`;
- allowlist: `0600` /
  `2f60dd69f0ff969f5c0f937a7665c5087b8316fcecfc47330ca720954a0ae34f`;
- forward summary: `0600` /
  `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b`;
- compare root: `0700`.

The R13 source delta must preserve the first R12 exact-allowlist failure as
process evidence and use a fresh mode-`0700` compare root. The intended R13
Review must start absent:
`docs/design/reviews/2026-08-21-add-role-first-review-routing-source-rereview-p1-r13.md`.

## Required adversarial decision

Trace exact production mechanisms and use only isolated temporary probes:

1. Prove generic exchange rollback requires both displaced and candidate
   retained ownership bindings; any one-sided match must fail closed without
   overwriting or deleting an unrelated inode.
2. Reproduce generic and Pi cleanup replacement interleavings immediately
   before unlink; no unrelated inode may be deleted, and a mismatch must leave
   explicit recovery state.
3. Prove Pi rename-then-raise cannot leave official `PASS` evidence; inspect
   both names after namespace side effects and classify the result as durable
   `BLOCKED`/unsafe.
4. Probe blocked pending-to-blocked rename exception, collision, short-write,
   and malformed-substitution paths; no malformed or substituted bytes may be
   accepted under a blocked-evidence name.
5. Probe Pi rollback collision; official output must not retain unrelated bytes,
   and only explicit `persistence-unsafe`/`persistence-pending` recovery
   residue plus durable mode-`0600` `BLOCKED` evidence may remain.
6. Recheck R12 descriptor identity, ctime boundary, parent/receipt/sandbox and
   native/network guarantees, public/portable parity, and no hidden cleanup
   residue. Do not run Pi, inspect runtime destinations, or create a plan.
7. Rebind the complete no-Git delta, compare root, summary, source verification,
   input, and all start/end hashes/modes. Keep Task 10 as the approved external
   limitation.

Bound fresh R13 evidence from implementation: focused P1 classes `102/102`,
cross-CLI `140/140`, Router full `264/264`, core validator PASS, and
quick validation PASS. The independent reviewer must rerun relevant isolated
production probes and the required validation matrix.

## Output

Return one concise neutral Markdown Review with assignment/independence,
start/end bindings, complete delta classification, exact
mechanism/test/probe trace, P0/P1/P2 and resume conditions, final verdict, and
whether read-only runtime verification may resume. Do not write files, run Git,
run Pi, inspect runtime destinations, create a plan, or claim completion.
