# Candidate Source High Re-review — P1 R7 bounded inputs

## Assignment

- product/role/profile: `codex` / `independent-reviewer` / `control-plane-high`
- implementation: fresh no-history `gpt-5.6-luna`, `max` reasoning
- purpose: decide whether R7 closes Pi launcher executed-byte drift and whether
  read-only runtime planning may resume
- authority: source Review evidence only; no mutation, self-acceptance,
  canonical transition, runtime plan, or completion claim

Read Router and Companion `AGENTS.md`/`SKILL.md`, then the files below. The
prior R5 Source PASS remains accepted for unchanged role-first and transaction
surfaces; deeply review only the R6/R7 launcher delta and its interaction with
native/network isolation. Return `PASS`, `FAIL`, or `BLOCKED`; any P0/P1/P2
blocks planning.

## Exact bindings

| Input | Mode / SHA-256 |
|---|---|
| approved Plan | `0644` / `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| prior Source R5 PASS | `0644` / `073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4` |
| source verification | `0644` / `99f8c6372d08ced6698c19cea84c57e0e677edca5ac4f27dbf1bdecc8d1001cd` |
| durable R7 delta summary | `0644` / `74c04c0e28052f3165ebab5f86469099f925ac10e153caea780f559660b27016` |
| corrected script | `0644` / `1c373f5eb6ade5eaa8c0c4750e09a7f0726f25b87dc574775d6408edf73ec642` |
| corrected tests | `0644` / `be2c1016a22c1f4e4db8a091e5550a784fe0415b18542a805075891ef75820e0` |
| Pi prompt | `0644` / `9cba75f75a714110d5efa3a9ff21112f51367a6626e3fdaea596b16544ff04c1` |
| sanitized Pi attempt 01 | `0600` / `2cc4d107db175acce6b66d9439ea8bab191d271695d4f75df4b1302dfa2c255b` |
| private R7 delta | `0600` / `2f59d1d5ee658869be9afada9e1b510dfcedf6ccc1b47cbababb87c8fcc8d161` |
| private R7 bindings | `0600` / `6679c9f7ff3520b894445dcfac3ee33bcbd6362f6fe891c2fb24c15b6ece5243` |
| private R7 allowlist | `0600` / `f4f513c5012524c418b92418e732be6550e45e074c6d8b5bfc9adfb25c274f1a` |
| private R7 forward summary | `0600` / `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |
| R7 backup root | `0700` |
| R6 script preimage | `0600` / `98b759b3f47057006e1128a9e671f55c51ad08a274db43fa4504d4b035cc411d` |
| R6 test preimage | `0600` / `f3f290f44c440adcbd78e75364e093382d075c86c7f81b2f50440c007f27eb8c` |

Private R7 root:
`/private/tmp/add-role-first-review-routing-p1r7-20260820-kvklRO`.
The delta reports 68 actual (`54` Router, `14` Companion), 73 allowlisted,
`unexpected=[]`. Summary/verification/this input are evidence-only post-delta.
The intended R7 Review artifact must start absent.

## Required adversarial decision

Trace exact mechanisms/tests and use only small temporary production probes:

1. shell grammar and package-root binding fail closed;
2. inventory covers types, bytes, executable bit, and internal links while
   rejecting absolute/broken/escaping links and specials;
3. copy is symlink-unfollowed and source-before/source-after/snapshot digests
   must agree before execution;
4. live argv reads the private snapshot, original package is absent from live
   read rules, snapshot is exact read-only, and sandbox explicitly denies its
   writes;
5. runtime, snapshot, and reviewed-source digests are rechecked after process;
   source and snapshot interleaves cannot turn bound `BLOCKED` into accepted
   `PASS`;
6. failures return only sanitized fail-closed evidence and native target
   verification still never invokes Pi;
7. explicitly decide whether simultaneous network denial and native credential
   denial makes a model-backed Pi Review impossible. If this is an approved
   contract limitation rather than an implementation defect, say so and state
   the exact Task-10 resume condition.

Bound fresh evidence: Router 220/220, Companion 87/87, OpenSpec 3/0, static,
shared bytes, audit, real-package snapshot, forward 6/6, and delta all PASS.
Do not rerun full suites unless a contradiction requires it.

## Output

Return one concise neutral Markdown Review: assignment/independence, start/end
bindings, delta classification, exact mechanism/test/probe trace, P0/P1/P2 and
resume conditions, final verdict, and whether read-only runtime planning may
resume. Do not write files, run Git/Pi, inspect runtime destinations, or create
a plan.
