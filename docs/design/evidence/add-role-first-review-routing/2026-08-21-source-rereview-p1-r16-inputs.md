# Candidate Source High Re-review — P1 R16 bounded inputs

## Assignment

- product/role/profile: `codex` / `independent-reviewer` / `control-plane-high`
- implementation: fresh no-history `gpt-5.6-luna`, `max` reasoning
- purpose: decide whether R16 closes the R15 Pi retained `PASS`-evidence residue
  boundary while preserving generic fail-closed cleanup on Darwin/POSIX
- authority: source Review evidence only; no mutation, self-acceptance,
  canonical transition, runtime plan, runtime inspection, or completion claim

Read Router and Companion `AGENTS.md`/`SKILL.md`, the approved OpenSpec/Plan,
engineering invariants and closeout contract, prior R5 PASS and R11/R12/R13/R14/R15
FAIL Reviews, then every bound R16 record. Review the complete current delta
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
| prior Source R15 FAIL | `0644` / `c77d7a284867063abdcaccb941844cc673550aeaf18228fecfd3f383ff29f3fc` |
| current source verification | `0644` / `b7bcbfb9c826f2dc27c71abe88f071aa03aa9b89dc8f2446fb89b74c3a97340c` |
| corrected R16 script | `0644` / `09813290af1b6c869215e6c372849334730eddce33860797407b61e9b8619ea6` |
| corrected R16 tests | `0644` / `57424b7da282e505acc6b32b6c72ef04c6f58b942757388357f14b7bc513b590` |
| R16 implementation backup root | `0700` / `/private/tmp/add-role-first-review-routing-p1r16-20260821-luna` |

The R15 authoritative source delta remains bound by the R15 input: private
delta mode `0600` SHA
`5898349948ca8ade6cece1460f15367f3b0767d1057ae913de55ee52197576f9`, bindings
`abbe2e5f5f0bd3871d8fc23834519ae993e7e5053b0cc4e4a27f75377ac6c923`, allowlist
`99` entries SHA
`5ad2294d2a6d9d1cd3e5662ac4d237a27dfe83da3409b79fb20a4691842e6f40`, compare
root mode `0700`, and R15 result `95` actual with `unexpected_paths: []`.
R16 must rebind both repositories against the same reconstructed R9 baselines
with a fresh mode-`0700` compare root. The intended R16 Review and durable R16
summary must start absent.

The R16 private delta, preflight bindings, and durable summary are generated
after this input is created and are then bound here as evidence-only final
state. Their initial delta records intentionally capture the pre-delta input
state; the final input hash is recorded after the delta and Review append.

### Generated R16 evidence bindings

- private delta: `/private/tmp/add-role-first-review-routing-p1r16-20260821-luna/evidence/source-delta-r16.json`, mode `0600`, SHA-256 `b4670cb53ad033ddc198b42d5e06315aaa47f091efc7253b68889d2023299bce`;
- preflight bindings: `/private/tmp/add-role-first-review-routing-p1r16-20260821-luna/evidence/preflight-source-bindings-r16.json`, mode `0600`, SHA-256 `b328f4e18ae4243aeebe03b816d1585d5b5fb438fa5591b014e8eec60f5857ca`;
- allowlist: `/private/tmp/add-role-first-review-routing-p1r16-20260821-luna/evidence/source-delta-allowlist-r16.txt`, `102` entries, mode `0600`, SHA-256 `8ce732f416d70f0caf5391e1dc9ff63450543a1e7154d67efe64b07626542032`;
- compare root: `/private/tmp/add-role-first-review-routing-p1r16-20260821-luna/source-compare-r16-clean`, mode `0700`;
- durable summary: `docs/design/evidence/add-role-first-review-routing/2026-08-21-source-delta-p1-r16-summary.json`, mode `0644`, SHA-256 `f409f302910303daa421c0e5c265cd34bf1fbd06145864d55dc859376362dfdc`;
- complete delta: `98` records (`84` Router, `14` Companion): `23` Router modifications, `58` Router additions, `3` generated-cache deletions, and `14` Companion modifications; `unexpected_paths: []`.
- fresh forward summary: `/private/tmp/add-role-first-review-routing-p1r16-20260821-luna/forward/summary.json`, mode `0600`, SHA-256 `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b`.

The private delta was generated before this final evidence binding and before
the R16 Review artifact. This input's post-delta SHA is therefore evidence-only
and must be checked at Review start and end.

## Required adversarial decision

Trace exact production mechanisms with isolated temporary probes only:

1. Reproduce replacement after the final retained-inode bind for Generic and
   Pi cleanup. No unrelated inode may be deleted or accepted.
2. Verify that when exact-owner deletion is unavailable, Pi rewrites the
   retained object through its already validated writable descriptor, even if
   the quarantine namespace is replaced, and leaves no canonical JSON
   `verdict: PASS` residue. Any uncertainty must leave visible recovery and/or
   mode-0600 blocked evidence.
3. Recheck all R11/R12/R13/R14/R15 rollback, Pi rename-side-effect,
   blocked-evidence, descriptor/ctime, parent/receipt, sandbox, native/network
   and hidden-residue invariants. Do not run Pi, inspect runtime destinations,
   or create a plan.
4. Rebind the complete no-Git delta, compare root, durable summary, source
   verification, input, and all start/end hashes/modes. Keep Task 10 as the
   approved external limitation.

Bound R16 implementation evidence: focused P1 `7/7 PASS`, cross-CLI
`149/149 PASS`, Router workflow `124/124 PASS`, full discovery `273/273 PASS`,
core validator `PASS`, and quick validation `PASS`. Rerun relevant production
probes and required validation checks independently.

## Output

Return one neutral Markdown Review with assignment/independence, bindings,
complete delta classification, exact mechanism/test/probe trace, P0/P1/P2,
resume conditions, final verdict, and whether runtime verification may resume.
Do not write files, run Git/Pi, inspect runtime destinations, create a plan, or
claim completion.
