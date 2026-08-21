# Candidate Source High Re-review — P1 R12 bounded inputs

## Assignment

- product/role/profile: `codex` / `independent-reviewer` / `control-plane-high`
- implementation: fresh no-history `gpt-5.6-luna`, `max` reasoning
- purpose: decide whether R12 closes all four R11 persistence P1 findings and
  whether read-only four-target runtime verification may resume
- authority: source Review evidence only; no mutation, self-acceptance,
  canonical transition, runtime plan, runtime inspection, or completion claim

Read Router and Companion `AGENTS.md`/`SKILL.md`, the approved OpenSpec/Plan,
engineering invariants and closeout contract, the prior R5 PASS and R11 FAIL,
then every bound R12 record. Review the complete current delta without Git.
Return `PASS`, `FAIL`, or `BLOCKED`; any P0/P1/P2 blocks promotion.

## Exact bindings

| Input | Mode / SHA-256 |
|---|---|
| approved Plan | `0644` / `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| prior Source R5 PASS | `0644` / `073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4` |
| prior Source R11 FAIL | `0644` / `0d89c219a344f9943d9f324d4f36fc0cbb4ec503fc0bce0eb0ceb91912981d62` |
| source verification | `0644` / `960c857a5f7b14800eb9fa6e4a3252391d2bdca9871019814c4755d78c82a0bf` |
| durable R12 delta summary | `0644` / `aa68cddb16622de36a3d08cb1012c9084f9dfa6a1fe9c5b2f324829ecb0e26d6` |
| corrected script | `0644` / `36b7c55a5688d455192ff850825eb5807e606141129782df8dc4152f34e2ff54` |
| corrected tests | `0644` / `2aeb37aa97bfbf7f542d9f6e67d64f4500f99c3d0e20d6ae8a67fa70e21524b7` |
| Pi prompt | `0644` / `9cba75f75a714110d5efa3a9ff21112f51367a6626e3fdaea596b16544ff04c1` |
| sanitized Pi attempt 01 | `0600` / `2cc4d107db175acce6b66d9439ea8bab191d271695d4f75df4b1302dfa2c255b` |
| authoritative private R12 retry1 delta | `0600` / `3e98e4015b8b461958172c538ea07798de4239d89a2ae0771a9eba1ec84c8e50` |
| private R12 retry1 bindings | `0600` / `b3c52f8cd141e70ab3f61d0366734c888513c5af59da4e6f089979fe24c7fd09` |
| private R12 retry1 allowlist | `0600` / `2f60dd69f0ff969f5c0f937a7665c5087b8316fcecfc47330ca720954a0ae34f` |
| private R12 forward summary | `0600` / `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |
| R12 private/retry1 compare roots | `0700` |
| R11 script preimage | `0600` / `301f4ba2ad3121e1e6799a34184540839715602e3c88608892a23439ae3c0aab` |
| R11 test preimage | `0600` / `c061b5a02d5b601ee5ea3c521556a2dcbeaed318af5b0399c3f5c184bbfdb1c6` |
| R11 verification preimage | `0600` / `a1aec85aac431b98375fdd51b60c19575d6dcd37c24501c74dd22633bd2e7995` |
| R11 input preimage | `0600` / `5af74bcf77dd292326c2e3ea4418b3e73c87ebb30b4f021029576a15040b9b83` |
| R11 Review preimage | `0600` / `0d89c219a344f9943d9f324d4f36fc0cbb4ec503fc0bce0eb0ceb91912981d62` |
| R11 durable-summary preimage | `0600` / `a3fbe1074cea7c163c507de02e79ba7dcec0c941b4c7b6bf52ca944ba7d02462` |
| failed R12 bindings | `0600` / `bb4aead50139702371159922429be24d271ba0a230164fe61283ea7775ce8ec5` |
| failed R12 allowlist | `0600` / `07691397dada7f2fb4081730d2627a24fbe701c632abf27450c47e729a278638` |
| failed R12 partial compare root | `0700`; output absent |

Private R12 root:
`/private/tmp/add-role-first-review-routing-p1r12-20260821-ww37dU`.
The authoritative delta is `source-delta-r12-retry1.json`; compare root is
`source-compare-r12-retry1`. It reports 85 actual (`71` Router, `14`
Companion), 90 allowlisted, `unexpected=[]`, with 37 modified, 45 added, and
three generated CPython 3.14 cache deletions. The durable summary, source-
verification append, and this input are evidence-only post-delta. The intended
Review must start absent:
`docs/design/reviews/2026-08-21-add-role-first-review-routing-source-rereview-p1-r12.md`.

## Required adversarial decision

Trace exact production mechanisms and use only isolated temporary probes:

1. Reproduce generic and Pi candidate-name substitution immediately before
   exclusive create/swap, immediately after namespace mutation, and during
   rollback. No unrelated inode may be overwritten, deleted, or accepted; the
   reviewed destination must be restored or the state must remain visibly
   blocked.
2. Verify one retained no-follow descriptor binds device/inode/type/mode/UID/
   GID/nlink/size/mtime/ctime plus two equal hashes. Probe same-inode mutation
   after each hash, after the final stable check, and ctime-only drift before
   install. Only a reviewed post-rename boundary may ignore ctime changes.
3. Prove Pi never rewrites an installed or candidate `PASS` inode. An uncertain
   object may remain only under explicit `persistence-pending` or
   `persistence-unsafe` non-evidence names. Fixed-schema mode-`0600` `BLOCKED`
   evidence must be written and file-fsynced under pending, then exclusively
   renamed, directory-fsynced, and identity/content-revalidated before a
   `persistence-blocked` name is accepted.
4. Probe blocked-recovery write/short-write/file-fsync/directory-fsync/rename-
   collision failures, candidate-binding failure, and substitutions before and
   after blocked/quarantine renames. No malformed or substituted object may
   remain under a blocked-evidence name; parent mapping drift must not report
   current evidence in a replacement tree.
5. Reproduce persistent cleanup failure and both check-to-rename/check-to-
   unlink interleavings for generic and Pi paths. Verify retained destination
   descriptors close on failure, no hidden `.cross-cli-sync.*` survives, and
   ambiguity leaves only explicit recovery state.
6. Verify R3–R11 parent/receipt/runtime/sandbox/native/network guarantees remain
   intact, public and portable source hashes outside the corrected script/tests
   did not drift, and repository-only R12 changes do not require a new runtime
   apply plan.
7. Rebind the authoritative retry1 delta, compare root, source summary, post-
   delta verification/input, and all start/end hashes/modes. Preserve the first
   R12 exact-allowlist failure as process evidence; do not promote or overwrite
   it.
8. Keep Task 10 classified as the approved limitation: a network-backed model
   requiring native credentials cannot complete until an approved isolated
   offline/local or temporary non-native route exists. Do not relax sandbox,
   run Pi, inspect runtime destinations, or create a runtime plan.

Bound fresh evidence: Router `258/258`, cross-CLI `134/134`, Companion
`87/87`, OpenSpec `3/0`, exact static/shared-byte/audit checks, forward `6/6`,
and the authoritative no-Git retry1 delta all PASS. Rerun focused tests and
isolated probes as needed; do not rerun full suites unless a contradiction
requires it.

## Output

Return one concise neutral Markdown Review with assignment/independence,
start/end bindings, complete delta classification, exact mechanism/test/probe
trace, P0/P1/P2 and resume conditions, final verdict, and whether read-only
runtime verification may resume. Do not write files, run Git/Pi, inspect
runtime destinations, create a plan, or claim project completion.
