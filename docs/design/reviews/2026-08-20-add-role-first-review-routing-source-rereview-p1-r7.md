## Candidate Source High Re-review — P1 R7

### Assignment and independence

- Product/role/profile: `codex` / `independent-reviewer` / `control-plane-high`
- Fresh no-history `gpt-5.6-luna`, max reasoning.
- Authority: source Review evidence only; no mutation, acceptance, runtime planning, or completion.

### Bindings and delta

- Input manifest: mode `0644`, SHA-256 `cd7d259935e58be01c3f65b6a96bda587425d8196b26e7a9eaa8bbf1bbbd374a`.
- Plan, R5 Review, verification, corrected launcher script/tests, Pi prompt/attempt, R7 private delta/bindings/allowlist/forward summary, and R6 preimages all matched their listed modes and hashes.
- R7 backup/compare root: mode `0700`.
- Intended R7 Review artifact: absent at start and end.
- Source delta: `PASS`; 68 actual paths (`54` Router, `14` Companion), 73 allowlisted, `unexpected_paths: []`.
- Reused accepted evidence: Router `220/220`, Companion `87/87`, OpenSpec `3/0`, static/shared-byte/audit/real-package/forward `6/6` all PASS. No full-suite rerun.

### Mechanism and probe trace

- `/bin/sh` exact single-`exec` grammar: targeted tests PASS; ambiguous, relative, missing-forwarding, linked-entrypoint, and escaping-link cases reject.
- Package inventory: custom production probe confirmed file bytes, executable bits, directories, and internal links; absolute, broken, escaping links, and FIFO reject.
- Snapshot: symlink-unfollowed copy, source-before/source-after/snapshot digest agreement, read-only modes, snapshot write-deny rule, source/snapshot interleave tests all PASS.
- Post-process checks: runtime drift, snapshot drift, reviewed-source drift, malformed output, and source-before-run mutation all remain sanitized `BLOCKED`; native target verification does not invoke Pi.
- Network/native-root denial is explicit. This is an approved contract limitation: a network-backed model requiring native credentials cannot complete Task 10 under the current sandbox.

### Findings

#### P1 — package-contained runtime bypasses executed-byte binding

Location: `scripts/validate_cross_cli_sync.py:3329-3341,3449-3463`

The launcher snapshot replaces only `argv[1]` with the private entrypoint. A valid absolute executable runtime located inside the original package is retained as `argv[0]`; its package path also remains reachable through generated ancestor/read rules.

A temporary production probe placed an executable `/usr/bin/perl` copy inside the package. `execute_pi_probe` returned `success=True`, `pi_probe: "pass"`, `verdict: "PASS"` while executing the original package runtime, not a snapshot runtime.

Required action: reject runtimes contained by the package, or snapshot and execute the runtime too; add a regression test, rerun focused/full validation and source delta, then obtain fresh High Review.

#### P1 — pre-process failures leak unsanitized errors and produce no evidence

Location: `scripts/validate_cross_cli_sync.py:3596-3614,4216-4231`

Validation, snapshot materialization, read-root, and subprocess-launch exceptions occur before the sanitizing block. A CLI probe with an invalid launcher exited `1` with empty stdout, no output artifact, and raw stderr:

`cross-cli sync validation failed: missing Pi launcher entrypoint: /does/not/exist`

Required action: convert all probe setup/launch exceptions into the fixed-schema mode-`0600` sanitized `BLOCKED` artifact; suppress raw exception text for `probe-pi`; add setup-error regression tests.

### Network/credential decision

The simultaneous network denial and native credential denial is an approved Task-10 contract limitation, not itself an implementation defect. Task 10 may resume only after an approved isolated route provides a model-backed Pi executable/backend that can complete with both denials intact (for example, an offline/local backend with temporary non-native credentials), followed by a fresh exact `probe-pi` run producing sanitized mode-`0600` evidence. Do not relax the sandbox ad hoc.

### Verdict

**FAIL**

- P0: none
- P1: two findings above
- P2: none

Read-only runtime planning **may not resume** until both P1 findings are corrected, reverified, source-delta evidence is refreshed, and a fresh independent Source High Review returns `PASS`.
