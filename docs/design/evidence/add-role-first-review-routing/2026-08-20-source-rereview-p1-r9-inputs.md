# Candidate Source High Re-review — P1 R9 bounded inputs

## Assignment

- product/role/profile: `codex` / `independent-reviewer` / `control-plane-high`
- implementation: fresh no-history `gpt-5.6-luna`, `max` reasoning
- purpose: decide whether R9 closes all three R8 P1 findings and whether
  read-only runtime planning may resume
- authority: source Review evidence only; no mutation, self-acceptance,
  canonical transition, runtime plan, or completion claim

Read Router and Companion `AGENTS.md`/`SKILL.md`, then every bound file below.
The prior R5 Source PASS remains accepted only for unchanged role-first and
transaction surfaces. Deeply review the R6–R9 launcher/probe delta and its
interaction with sandbox/native/network isolation. Return `PASS`, `FAIL`, or
`BLOCKED`; any P0/P1/P2 blocks planning.

## Exact bindings

| Input | Mode / SHA-256 |
|---|---|
| approved Plan | `0644` / `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| prior Source R5 PASS | `0644` / `073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4` |
| prior Source R8 FAIL | `0644` / `c99d1206f7666d8dbd67c8bc480649b0c1cadabaf75e6a4395e8f1138f31f5ad` |
| source verification | `0644` / `2e651b24eccfc472ab0cbcd67e2fff2298858c275f5ea3c251bf9223f11ee0f1` |
| durable R9 delta summary | `0644` / `479ec0c6677195aa1174f60495a398daaf170974aa80e482ac5f74f40fc91ec6` |
| corrected script | `0644` / `e847f1c7cc73cd2c4b3fc4cf3ee3bfb8369fd431feb1bdf632f6654ff16d280f` |
| corrected tests | `0644` / `d77e19b190a4887b30e954f7c284d43ae3f66d13b3755707fce7986229010c5d` |
| Pi prompt | `0644` / `9cba75f75a714110d5efa3a9ff21112f51367a6626e3fdaea596b16544ff04c1` |
| sanitized Pi attempt 01 | `0600` / `2cc4d107db175acce6b66d9439ea8bab191d271695d4f75df4b1302dfa2c255b` |
| authoritative private R9 delta | `0600` / `a16ef355cd8ecfb59fed2dfbfd46e370557c9c3b44373d220744f2b02e62237e` |
| private R9 bindings | `0600` / `a3b48b4cb204204cf0641997b923be5f619080885e06676ca7aec2035a1ddc9d` |
| private R9 allowlist | `0600` / `cceb69b843e569f7c99189346e8ced845862fc8e4421c2c8b46c135e86196fc9` |
| private R9 forward summary | `0600` / `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |
| R9 backup/authoritative compare roots | `0700` |
| R8 script preimage | `0600` / `92c8c13889dd6613fa8d224b0fcddd63db841be8720a63e5a00c08ff4fd4581a` |
| R8 test preimage | `0600` / `3a5c08f805df17764c641f93123187eb95200717eb4654c4de208e4c988a5556` |
| R8 verification preimage | `0600` / `cd72c82bd54367877ca2021ec8c2f3cc213c87f773d9bc04fca2ec1d599a3f49` |
| R8 input preimage | `0600` / `cd6c52d487f46e43dbbc1c95e58fba3bbad2e9a26f62780e95561a4baa7cfb22` |
| R8 Review preimage | `0600` / `c99d1206f7666d8dbd67c8bc480649b0c1cadabaf75e6a4395e8f1138f31f5ad` |
| recovered generated cpython-314 cache | `0600` / `0d5a538b7d5729a1dc19177b6a50566b82a13d0e088f54e514a194ef12b6ce18` |
| retained non-authoritative first R9 delta | `0600` / `64aca252ecec2b8665a498b2b11d579011c2d4577a69ae786a047567b0336f37` |
| retained first R9 compare root | `0700` |

Private R9 root:
`/private/tmp/add-role-first-review-routing-p1r9-20260820-4TSC3a`.
The authoritative retry delta is
`source-delta-r9-retry1.json`; its compare root is
`source-compare-r9-retry1`. It reports 74 actual (`60` Router, `14`
Companion), 79 allowlisted, `unexpected=[]`, and the governed cpython-314
cache path deleted relative to baseline. The first delta/compare pair is
retained only to account for the locally regenerated cache; do not treat it as
the source candidate. Summary/verification/this input are evidence-only
post-delta. The intended R9 Review artifact must start absent:
`docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r9.md`.

## Required adversarial decision

Trace exact production mechanisms/tests and use only small temporary probes:

1. prove the accepted launcher runtime is identity-distinct from every regular
   package file, including hard-link aliases introduced before inventory and
   adversarial aliases or drift during inventory, while the supported real
   launcher still runs the private entrypoint snapshot;
2. prove every symlink in the reviewed source root is rejected before launch,
   including retarget attempts, and that regular-file/mode/content drift remains
   bound by the reviewed-tree digest;
3. prove Pi Review evidence persistence is a complete transaction across
   candidate creation, exclusive rename, collision, parent mapping/identity
   drift, file and directory fsync failures, and guarded rollback: a returned
   `BLOCKED` result must not leave a residual accepted `PASS` artifact or hidden
   candidate and must never overwrite unrelated state;
4. prove all R7/R8 guarantees remain intact: package-contained runtimes and raw
   setup/launch exceptions fail closed, fixed-schema mode-`0600` evidence is
   produced when the declared path is usable, and stdout/runtime/snapshot/source
   drift cannot produce an accepted verdict;
5. confirm native target verification never invokes Pi and the simultaneous
   native-root/network denials remain intact;
6. explicitly classify the approved Task-10 limitation: a network-backed model
   requiring native credentials cannot complete until an approved isolated
   offline/local or temporary non-native route exists. Do not relax the sandbox.

Bound fresh evidence: Router 226/226, cross-CLI 102/102, Companion 87/87,
OpenSpec 3/0, exact static/shared-byte/audit checks, forward 6/6, and the
authoritative no-Git delta all PASS. Rerun focused tests/probes as needed; do
not rerun full suites unless a contradiction requires it.

## Output

Return one concise neutral Markdown Review: assignment/independence, start/end
bindings, delta classification (including the retained cache incident), exact
mechanism/test/probe trace, P0/P1/P2 and resume conditions, final verdict, and
whether read-only runtime planning may resume. Do not write files, run Git/Pi,
inspect runtime destinations, or create a plan.
