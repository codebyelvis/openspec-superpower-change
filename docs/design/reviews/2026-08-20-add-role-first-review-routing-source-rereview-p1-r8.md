# Source High Review — R8

**Assignment / bindings.** Fresh no-history `codex / independent-reviewer / control-plane-high`; source evidence only. The bound R8 input matched mode `0644` and SHA-256 `cd6c52d487f46e43dbbc1c95e58fba3bbad2e9a26f62780e95561a4baa7cfb22`. Required Plan, R5/R7 Reviews, verification, R8 summary, script, tests, and private evidence bindings matched. Delta: 71 actual paths (Router 57, Companion 14), 76 allowlisted, `unexpected=[]`; no project/runtime files were written.

**Evidence.** The nine focused R8 tests passed. Direct probes confirmed R7’s direct corrections: package-contained runtime rejection, sanitized setup/launch failures, fixed-schema private `BLOCKED` output, drift checks for regular files, native-target no-Pi behavior, and native/network denials.

**Findings.**

- **P1 — hard-link runtime alias accepted** — `scripts/validate_cross_cli_sync.py:3323-3342`. A non-symlink runtime path outside the package, hard-linked to a package executable, passes `resolve()` containment and executes package bytes outside the private snapshot, producing `PASS`. Reject runtime aliases by inode/device (`samefile`) against package files and add a regression probe.
- **P1 — reviewed symlink-target drift undetected** — `scripts/validate_cross_cli_sync.py:3565-3585`. `_reviewed_tree_digest()` records every symlink only as `symlink-denied`; retargeting `link -> a` to `link -> b` after execution leaves the digest unchanged and accepts `PASS`. Reject reviewed-root symlinks or bind target identity/content into the digest, with a retarget regression.
- **P1 — persistence failure can leave accepted `PASS` artifact** — `scripts/validate_cross_cli_sync.py:3772-3788`. Injecting output-directory `fsync` failure after the file write returns sanitized `BLOCKED`, but leaves a mode-`0600` artifact containing `PASS`. Make persistence atomic/transactional and ensure any failure removes or replaces the artifact with `BLOCKED`; add an injected-failure test.

P0: none. P2: none. The approved Task-10 native-credential/network limitation remains unchanged; sandbox denials must not be relaxed.

**Verdict: FAIL.** Read-only runtime planning may not resume. Resume requires correction of all three P1s, focused regression evidence, refreshed source-delta bindings, and a fresh independent Source High Review PASS.
