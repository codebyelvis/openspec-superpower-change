# Candidate Source High Re-review — P1 R11 bounded inputs

## Assignment

- product/role/profile: `codex` / `independent-reviewer` / `control-plane-high`
- implementation: fresh no-history `gpt-5.6-luna`, `max` reasoning
- purpose: decide whether R11 closes both R10 persistence P1 findings and
  whether read-only four-target runtime planning may resume
- authority: source Review evidence only; no mutation, self-acceptance,
  canonical transition, runtime plan, or completion claim

Read Router and Companion `AGENTS.md`/`SKILL.md`, the approved OpenSpec/Plan,
the prior R5 PASS and R10 FAIL, then every bound R11 record. Review the complete
current delta without Git. Return `PASS`, `FAIL`, or `BLOCKED`; any P0/P1/P2
blocks planning.

## Exact bindings

| Input | Mode / SHA-256 |
|---|---|
| approved Plan | `0644` / `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| prior Source R5 PASS | `0644` / `073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4` |
| prior Source R10 FAIL | `0644` / `3543495d547ef12982e59b36968ca90087d85967590e4eb5535a3414e9aa5c06` |
| source verification | `0644` / `a1aec85aac431b98375fdd51b60c19575d6dcd37c24501c74dd22633bd2e7995` |
| durable R11 delta summary | `0644` / `a3fbe1074cea7c163c507de02e79ba7dcec0c941b4c7b6bf52ca944ba7d02462` |
| corrected script | `0644` / `301f4ba2ad3121e1e6799a34184540839715602e3c88608892a23439ae3c0aab` |
| corrected tests | `0644` / `c061b5a02d5b601ee5ea3c521556a2dcbeaed318af5b0399c3f5c184bbfdb1c6` |
| Pi prompt | `0644` / `9cba75f75a714110d5efa3a9ff21112f51367a6626e3fdaea596b16544ff04c1` |
| sanitized Pi attempt 01 | `0600` / `2cc4d107db175acce6b66d9439ea8bab191d271695d4f75df4b1302dfa2c255b` |
| authoritative private R11 delta | `0600` / `11c7608e5fe7b0c9d0d43b22e474777f40fa6e5d999f223009f573555b49c8c5` |
| private R11 bindings | `0600` / `525f418a2b137eaa0f963e9b189070ee3d67f5f9e839a0de58e3d9c26474c85e` |
| private R11 allowlist | `0600` / `20a4b3be6516b55c7df40b63309d34f1f28a72498ff8c5ebccd107fb764cc3de` |
| private R11 forward summary | `0600` / `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |
| R11 private/compare roots | `0700` |
| R10 script preimage | `0600` / `8b9d21ed256b7a2a11dfd40043b2af1e938d9ed50e8b0185a5a174eb5120f77e` |
| R10 test preimage | `0600` / `146bed95e60c28144095470c1a639f619caa04c8ca14d28d08a245fbf39b8318` |
| R10 verification preimage | `0600` / `ddd8fad9f32760fa0de02281a191cf31ec606f73adc8474297bd2c47997453be` |
| R10 input preimage | `0600` / `bbe790f6b6c5a2666bd3f6fad2afeefa0e168976acf119783d50905736254705` |
| R10 Review preimage | `0600` / `3543495d547ef12982e59b36968ca90087d85967590e4eb5535a3414e9aa5c06` |
| R10 durable-summary preimage | `0600` / `c95079e11be22f0f6c6e965ea4984f9c90d703e9e951c0f2144f78d8d0c2bc8c` |

Private R11 root:
`/private/tmp/add-role-first-review-routing-p1r11-20260820-kth4IL` (created
before the date boundary and retained mode `0700`). The authoritative delta is
`source-delta-r11.json`; compare root is `source-compare-r11`. It reports 80
actual (`66` Router, `14` Companion), 85 allowlisted, `unexpected=[]`, and the
governed cpython-314 cache path deleted relative to baseline. The durable
summary and this input are evidence-only post-delta. The intended Review must
start absent:
`docs/design/reviews/2026-08-21-add-role-first-review-routing-source-rereview-p1-r11.md`.

## Required adversarial decision

Trace exact production mechanisms and use only isolated temporary probes:

1. Reproduce the R10 candidate-file-fsync plus cleanup failure and candidate
   parent-guard plus cleanup failure boundaries. Prove public `BLOCKED` cannot
   leave accepted `PASS` bytes or a hidden `.cross-cli-sync.*` candidate; any
   retained generated evidence must be visible, fixed-schema `BLOCKED`, and
   mode `0600`.
2. Reproduce same-content/mode different-inode substitution after install and
   immediately before rollback. Prove rollback neither unlinks nor rewrites
   the replacement inode, including at the former check-to-unlink boundary.
3. Independently test candidate-name substitution before exclusive install,
   mapping/identity changes during descriptor binding, and changes immediately
   before/after quarantine rename. No unrelated inode may be overwritten,
   deleted, or accepted as evidence; any ambiguity must return `BLOCKED`.
4. Verify descriptor binding uses one no-follow descriptor with before/after
   identity checks and that installed rollback mutates only the verified owned
   descriptor. Test content/mode/device/inode mismatch, short/failed write,
   file fsync, directory fsync, rename collision, and persistent cleanup
   failure branches.
5. Prove generic atomic candidate behavior is unchanged, output collision is
   exclusive, parent identity/mapping checks remain effective, exceptions and
   evidence remain sanitized, and R7–R10 runtime/symlink/tree/native/network
   guarantees remain intact.
6. Rebind the authoritative delta, compare root, source summary, post-delta
   verification/input, and all start/end hashes/modes. Classify the disclosed
   post-delta reporting-helper field-name error as evidence process only; do
   not promote it or silently rerun the authoritative delta.
7. Keep Task 10 classified as the approved limitation: a network-backed model
   requiring native credentials cannot complete until an approved isolated
   offline/local or temporary non-native route exists. Do not relax sandbox or
   inspect native runtime destinations.

Bound fresh evidence: Router 235/235, cross-CLI 111/111, Companion 87/87,
OpenSpec 3/0, exact static/shared-byte/audit checks, forward 6/6, and the
authoritative no-Git delta all PASS. Rerun focused tests/probes as needed; do
not rerun full suites unless a contradiction requires it.

## Output

Return one concise neutral Markdown Review with assignment/independence,
start/end bindings, complete delta classification, exact mechanism/test/probe
trace, P0/P1/P2 and resume conditions, final verdict, and whether read-only
runtime planning may resume. Do not write files, run Git/Pi, inspect runtime
destinations, or create a plan.
