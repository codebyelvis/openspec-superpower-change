# Candidate Source High Re-review — P1 R10 bounded inputs

## Assignment

- product/role/profile: `codex` / `independent-reviewer` / `control-plane-high`
- implementation: fresh no-history `gpt-5.6-luna`, `max` reasoning
- purpose: decide whether R10 closes all five R9 P1 findings and whether
  read-only runtime planning may resume
- authority: source Review evidence only; no mutation, self-acceptance,
  canonical transition, runtime plan, or completion claim

Read Router and Companion `AGENTS.md`/`SKILL.md`, then every bound file below.
The prior R5 Source PASS remains accepted only for unchanged role-first and
transaction surfaces. Deeply review the R6–R10 launcher/probe delta and its
interaction with sandbox/native/network isolation. Return `PASS`, `FAIL`, or
`BLOCKED`; any P0/P1/P2 blocks planning.

## Exact bindings

| Input | Mode / SHA-256 |
|---|---|
| approved Plan | `0644` / `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| prior Source R5 PASS | `0644` / `073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4` |
| prior Source R9 FAIL | `0644` / `9d563300e93c63f55cfce321c90712e1e329c0ada45e38270a7ffaa856377fcf` |
| source verification | `0644` / `ddd8fad9f32760fa0de02281a191cf31ec606f73adc8474297bd2c47997453be` |
| durable R10 delta summary | `0644` / `c95079e11be22f0f6c6e965ea4984f9c90d703e9e951c0f2144f78d8d0c2bc8c` |
| corrected script | `0644` / `8b9d21ed256b7a2a11dfd40043b2af1e938d9ed50e8b0185a5a174eb5120f77e` |
| corrected tests | `0644` / `146bed95e60c28144095470c1a639f619caa04c8ca14d28d08a245fbf39b8318` |
| Pi prompt | `0644` / `9cba75f75a714110d5efa3a9ff21112f51367a6626e3fdaea596b16544ff04c1` |
| sanitized Pi attempt 01 | `0600` / `2cc4d107db175acce6b66d9439ea8bab191d271695d4f75df4b1302dfa2c255b` |
| authoritative private R10 delta | `0600` / `f6e05c35c620fe2c50e24346d23b76c672ef73703017aaf339bf41071b19c271` |
| private R10 bindings | `0600` / `1a27b71a8cb59b1ca1f542a6c1e78f8b0e488ae05adb8ffeb1d0a3c1deebc762` |
| private R10 allowlist | `0600` / `3adc35f24774fb5942df74047f2da2b3db9d0c1a51d7c2a1bbbf453317779998` |
| private final R10 forward summary | `0600` / `6fe31cbfde08855d035ac52caf139d42d5e96ac995380c09017b156281bc79ef` |
| R10 backup/authoritative compare roots | `0700` |
| R9 script preimage | `0600` / `e847f1c7cc73cd2c4b3fc4cf3ee3bfb8369fd431feb1bdf632f6654ff16d280f` |
| R9 test preimage | `0600` / `d77e19b190a4887b30e954f7c284d43ae3f66d13b3755707fce7986229010c5d` |
| R9 verification preimage | `0600` / `2e651b24eccfc472ab0cbcd67e2fff2298858c275f5ea3c251bf9223f11ee0f1` |
| R9 input preimage | `0600` / `f0d1866ddf9b6b0126166d556f4d96b81e3f63bbe413505342e678d9ef06baa0` |
| R9 Review preimage | `0600` / `9d563300e93c63f55cfce321c90712e1e329c0ada45e38270a7ffaa856377fcf` |
| R9 durable-summary preimage | `0600` / `479ec0c6677195aa1174f60495a398daaf170974aa80e482ac5f74f40fc91ec6` |
| corrected retained first R9 delta | `0600` / `64aca2527cf0f1e513054ac29ab406958cd1de81cc6206e4176396ddacf73dc4` |
| non-authoritative pre-hardening R10 delta | `0600` / `cab67e501d7f3a524549fb568545759b246c3e878d1a711d5164671674c85371` |
| non-authoritative R10 retry1 delta | `0600` / `db634968ea2ac0441491aaa921379ceb92342fa25d0e1d172e77cc1a2a540f76` |
| failed-baseline compare root and pre-hardening compare roots | `0700` |

Private R10 root:
`/private/tmp/add-role-first-review-routing-p1r10-20260820-Bun7oJ`.
The authoritative delta is `source-delta-r10-retry2.json`; its compare root is
`source-compare-r10-retry2`. It reports 78 actual (`64` Router, `14`
Companion), 82 allowlisted, `unexpected=[]`, and the governed cpython-314 cache
path deleted relative to baseline. The failed-baseline compare directory and
the two pre-hardening deltas/comparison roots are retained and explicitly
non-authoritative. Summary/verification/this input are evidence-only
post-delta. The intended R10 Review artifact must start absent:
`docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r10.md`.

## Required adversarial decision

Trace exact production mechanisms/tests and use only small temporary probes:

1. prove launcher runtime binding is descriptor-based and remains identical
   before/during/after both inventory passes, package snapshotting, and actual
   process launch; cover hard-link and same-content inode substitutions at each
   boundary and confirm the supported real launcher still executes its private
   entrypoint snapshot;
2. prove raw top-level and nested reviewed-root symlinks are rejected before
   resolution/launch, and root/directory/file mapping, identity, mode, and
   content drift all override otherwise valid stdout;
3. prove evidence persistence is fail-closed under candidate creation,
   exclusive rename collision, parent identity/mapping drift, file/directory
   fsync failure, rollback-unlink failure, and persistent candidate-unlink
   failure; a returned `BLOCKED` must leave neither accepted `PASS` bytes nor a
   `.cross-cli-sync.*` candidate and must not overwrite unrelated state;
4. when cleanup cannot remove an exact candidate, prove only fixed-schema
   mode-`0600` `BLOCKED` bytes can survive under an explicit visible
   persistence-blocked quarantine, and that no such evidence can be mistaken
   for accepted PASS;
5. independently reproduce the corrected retained first-R9-delta SHA and
   classify the failed/pre-hardening R10 records without promoting them;
6. prove all R7–R9 guarantees remain intact: package-contained/preexisting
   aliased runtimes and raw exceptions fail closed, output is sanitized,
   snapshot/source drift is detected, native target verification never invokes
   Pi, and native-root/network denials remain simultaneous;
7. explicitly classify the approved Task-10 limitation: a network-backed model
   requiring native credentials cannot complete until an approved isolated
   offline/local or temporary non-native route exists. Do not relax the sandbox.

Bound fresh evidence: Router 231/231, cross-CLI 107/107, Companion 87/87,
OpenSpec 3/0, exact static/shared-byte/audit checks, final forward 6/6, and the
authoritative no-Git delta all PASS. Rerun focused tests/probes as needed; do
not rerun full suites unless a contradiction requires it.

## Output

Return one concise neutral Markdown Review: assignment/independence, start/end
bindings, complete delta and retained-record classification, exact
mechanism/test/probe trace, P0/P1/P2 and resume conditions, final verdict, and
whether read-only runtime planning may resume. Do not write files, run Git/Pi,
inspect runtime destinations, or create a plan.
