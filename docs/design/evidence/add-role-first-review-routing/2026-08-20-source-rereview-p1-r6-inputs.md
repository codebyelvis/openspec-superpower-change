# Candidate Source High Re-review Inputs — P1 R6

## Assignment and authority

- reviewer product: `codex`
- reviewer role: `independent-reviewer`
- reviewer profile: `control-plane-high`
- reviewer implementation: fresh no-history `gpt-5.6-luna` with `max`
  reasoning, distinct from authors, executors, prior reviewers, and decision owner
- purpose: decide whether the sixth-corrected source safely binds the real Pi
  launcher chain and may return to read-only four-target runtime planning
- result authority: implementation Review evidence only; no source/runtime
  mutation, canonical transition, self-acceptance, or completion authority

Return explicit `PASS`, `FAIL`, or `BLOCKED`. Any P0/P1/P2 finding blocks
runtime planning and requires another correction/re-review revision.

## Required read set and bindings

Read both project `AGENTS.md` and `SKILL.md` files completely; the approved
OpenSpec proposal/design/spec/tasks and Plan; engineering invariants and
learning-closeout contract; sync and Pi isolation contracts; complete source
verification; all previous source and sync-plan Reviews; the sanitized Pi
attempt-01 result; the complete current Router/Companion trees; every delta
record; production implementation and tests. Do not rely on this summary in
place of the bound files.

Primary mode-`0644` inputs:

| Input | SHA-256 |
|---|---|
| Plan `docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md` | `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| OpenSpec proposal | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| OpenSpec design | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| OpenSpec delta spec | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| OpenSpec tasks | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| source verification | `55c1c272e51664acaaa8b38cb19dff6c3754f1c333ddab27da1c3b4a11e8e62b` |
| durable R6 delta summary | `23485e9b237e218fc2bdbcfab305f41e5e62c5b400d533f24fd9a94a58b104a3` |
| corrected `scripts/validate_cross_cli_sync.py` | `98b759b3f47057006e1128a9e671f55c51ad08a274db43fa4504d4b035cc411d` |
| corrected `tests/test_cross_cli_sync.py` | `f3f290f44c440adcbd78e75364e093382d075c86c7f81b2f50440c007f27eb8c` |
| Pi adversarial prompt | `9cba75f75a714110d5efa3a9ff21112f51367a6626e3fdaea596b16544ff04c1` |
| prior Candidate Source R5 PASS | `073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4` |
| prior Sync-plan R5 PASS | `b0714b11b826de230bea71e909ffaea916953ada136188ad7df11a1c6502c886` |

Private read-only reproduction inputs:

| Input | Mode / SHA-256 |
|---|---|
| sanitized Pi attempt 01 `/private/tmp/add-role-first-review-routing-20260810-FPWT9V/pi-adversarial-review.json` | `0600` / `2cc4d107db175acce6b66d9439ea8bab191d271695d4f75df4b1302dfa2c255b` |
| R6 delta `source-delta-r6-retry1.json` | `0600` / `6e89942768da96045c14645dfb196d2fe89e4877c963acaa676152e0c66c32ae` |
| R6 bindings `preflight-source-bindings-r6.json` | `0600` / `08af96bf93646d8a5f04cd25a5fe342c7237633172755b41c24128c4ae9950f3` |
| R6 allowlist `source-delta-allowlist-r6.txt` | `0600` / `7e9bc9e8ecd2cff5a9a1d35be32596533e7a4ed5340e3c25a9978a9eb37f454d` |
| R6 forward summary | `0600` / `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |
| R6 backup root | `0700` |
| script preimage | `0600` / `332de6171495faa12b3acd6c7c39e8ee35972a9c87eebe216d9581cc3b520044` |
| test preimage | `0600` / `97d46aec7247ab9e0f93d60b2c017248e22e4b54d2c53f3f01eaa83d0c9b1ed2` |
| source-verification preimage | `0600` / `52bca43ed01b18f959f3afe6bca22016d98cf584737a0ef88d0107cc3cc6050b` |

The bound delta reports `66` actual paths (`52` Router, `14` Companion), `70`
allowlisted, and `unexpected_paths: []`. The durable summary, verification
append, and this input are evidence-only post-delta records. Reconstruct and
classify the current delta without Git. The project-root `antigravity-cli`
artifact must remain absent; its preserved private copy is non-source history.

## R6 integrity proof to challenge

Attempt 01 reached no Pi business verdict because the sandbox bound only the
wrapper/shebang and denied its second-stage Node process. The candidate claims:

1. a shell launcher with live content is accepted only when it contains one
   exact `exec ABS_RUNTIME ABS_ENTRYPOINT "$@"` command;
2. runtime and entrypoint must be regular/non-symlink as applicable, executable
   where required, and entrypoint must bind to a nearest named package manifest;
3. extra shell commands, relative paths, missing forwarding, malformed quoting,
   linked targets, missing package metadata, and native-root overlap fail closed;
4. execution bypasses the mutable shell layer and invokes only the resolved
   runtime plus bound entrypoint, while read access is limited to required
   system/runtime/package/read roots;
5. temporary HOME/agent-root isolation, native-root deny, network deny,
   read-only tools, sanitized schema, and fail-closed evidence remain intact;
6. the correction does not make deterministic native-target verification invoke
   Pi and does not authorize runtime planning from the stale R5 plan.

Trace each claim through exact path:line mechanisms and tests. Use only isolated
temporary production-function probes. Include adversarial cases for oversized or
non-UTF8 launchers, comments/blank lines, shell metacharacters/substitutions,
symlink leaf/ancestor changes, package-root substitution, runtime replacement,
native/read-root overlap, macOS `/bin/sh` variants, executable/read profile
closure, output schema, and post-build drift. Explicitly assess whether the
approved simultaneous network/native-root denial makes an actual model-backed Pi
Review mechanically impossible; distinguish a source defect from an approved
contract limitation and state the exact resume condition.

Re-evaluate all earlier P1 corrections and four-target transaction/recovery
branches. Fresh evidence: Router `218/218`, cross-CLI `94/94`, Companion `87/87`,
OpenSpec `3/0`, exact negative searches/shared bytes/audit PASS, forward `6/6`,
and no unexpected source path.

## Required output

Return one neutral complete Markdown Review with assignment/independence,
start/end bindings, complete-delta classification, requirement→mechanism→test
traces, adversarial production probes, validation evidence, findings by severity
and exact resume conditions, final `PASS`/`FAIL`/`BLOCKED`, and whether read-only
runtime planning may resume.

Do not modify files, run Git or Pi, inspect runtime destinations, create a
runtime plan, accept your own verdict, or claim completion.
