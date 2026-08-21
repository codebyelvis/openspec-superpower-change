# Candidate Source High Re-review — P1 R8 bounded inputs

## Assignment

- product/role/profile: `codex` / `independent-reviewer` / `control-plane-high`
- implementation: fresh no-history `gpt-5.6-luna`, `max` reasoning
- purpose: decide whether R8 closes both R7 P1 findings and whether read-only
  runtime planning may resume
- authority: source Review evidence only; no mutation, self-acceptance,
  canonical transition, runtime plan, or completion claim

Read Router and Companion `AGENTS.md`/`SKILL.md`, then every bound file below.
The prior R5 Source PASS remains accepted only for unchanged role-first and
transaction surfaces. Deeply review the R6–R8 launcher/probe delta and its
interaction with sandbox/native/network isolation. Return `PASS`, `FAIL`, or
`BLOCKED`; any P0/P1/P2 blocks planning.

## Exact bindings

| Input | Mode / SHA-256 |
|---|---|
| approved Plan | `0644` / `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| prior Source R5 PASS | `0644` / `073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4` |
| prior Source R7 FAIL | `0644` / `399bff18097231d069bf597edcef9e0ebacd358e7e636e40974006fdab784e44` |
| source verification | `0644` / `cd72c82bd54367877ca2021ec8c2f3cc213c87f773d9bc04fca2ec1d599a3f49` |
| durable R8 delta summary | `0644` / `e237004079db66d11364547d1702cc374e024e6d635abe6115d849c2a03fdcd8` |
| corrected script | `0644` / `92c8c13889dd6613fa8d224b0fcddd63db841be8720a63e5a00c08ff4fd4581a` |
| corrected tests | `0644` / `3a5c08f805df17764c641f93123187eb95200717eb4654c4de208e4c988a5556` |
| Pi prompt | `0644` / `9cba75f75a714110d5efa3a9ff21112f51367a6626e3fdaea596b16544ff04c1` |
| sanitized Pi attempt 01 | `0600` / `2cc4d107db175acce6b66d9439ea8bab191d271695d4f75df4b1302dfa2c255b` |
| private R8 delta | `0600` / `382b9b5b5b4802b24f012df449177a5bce6837948762110642d061e19e6ca700` |
| private R8 bindings | `0600` / `ad7152453735b7eebdde1a9e30667cc048850f16581f47516436b14720e86c0a` |
| private R8 allowlist | `0600` / `4f36ff2a983b801bbc12c9612b92d36217e268520a250a7d352e5b964c0cd018` |
| private R8 forward summary | `0600` / `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |
| R8 backup/compare roots | `0700` |
| R7 script preimage | `0600` / `1c373f5eb6ade5eaa8c0c4750e09a7f0726f25b87dc574775d6408edf73ec642` |
| R7 test preimage | `0600` / `be2c1016a22c1f4e4db8a091e5550a784fe0415b18542a805075891ef75820e0` |
| R7 verification preimage | `0600` / `99f8c6372d08ced6698c19cea84c57e0e677edca5ac4f27dbf1bdecc8d1001cd` |
| R7 input preimage | `0600` / `cd7d259935e58be01c3f65b6a96bda587425d8196b26e7a9eaa8bbf1bbbd374a` |
| R7 Review preimage | `0600` / `399bff18097231d069bf597edcef9e0ebacd358e7e636e40974006fdab784e44` |

Private R8 root:
`/private/tmp/add-role-first-review-routing-p1r8-20260820-9yiUoW`.
The delta reports 71 actual (`57` Router, `14` Companion), 76 allowlisted,
`unexpected=[]`. Summary/verification/this input are evidence-only post-delta.
The intended R8 Review artifact must start absent.

## Required adversarial decision

Trace exact production mechanisms/tests and use only small temporary probes:

1. prove every accepted shell-launcher runtime resolves outside the original
   package, including symlink/alias containment, while the supported real
   launcher shape still uses the private entrypoint snapshot;
2. prove validation, package snapshot, reviewed-root, subprocess-launch, stdout,
   drift, and evidence-persistence failures cannot expose raw exception text or
   produce an accepted verdict;
3. with a new valid output path under a mode-`0700` parent, prove every setup or
   launch failure produces the exact fixed-schema mode-`0600` `BLOCKED`
   artifact and the CLI emits no raw path or error;
4. prove the normal valid production path still returns PASS/BLOCKED according
   to schema output, and runtime/snapshot/reviewed-source drift still overrides
   otherwise valid stdout;
5. confirm native target verification never invokes Pi and the simultaneous
   native-root/network denials remain intact;
6. explicitly classify the approved Task-10 limitation: a network-backed model
   requiring native credentials cannot complete until an approved isolated
   offline/local or temporary non-native route exists. Do not relax the sandbox.

Bound fresh evidence: Router 223/223, cross-CLI 99/99, Companion 87/87,
OpenSpec 3/0, exact static/shared-byte/audit checks, forward 6/6, and no-Git
delta all PASS. Rerun focused tests/probes as needed; do not rerun full suites
unless a contradiction requires it.

## Output

Return one concise neutral Markdown Review: assignment/independence, start/end
bindings, delta classification, exact mechanism/test/probe trace, P0/P1/P2 and
resume conditions, final verdict, and whether read-only runtime planning may
resume. Do not write files, run Git/Pi, inspect runtime destinations, or create
a plan.
