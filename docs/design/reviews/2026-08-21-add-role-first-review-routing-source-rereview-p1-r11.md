# Source High Re-review — P1 R11

- Assignment: fresh no-history `codex / independent-reviewer / control-plane-high`; source evidence only. No Git, Pi, runtime destinations, project writes, or intended Review write.
- Bound inputs were rechecked unchanged at end. Primary hashes/modes: Plan `0644 dbf838c4…`, R5 `0644 073a367b…`, R10 `0644 3543495d…`, source verification `0644 a1aec85a…`, R11 summary `0644 a3fbe107…`, corrected script `0644 301f4ba2…`, corrected tests `0644 c061b5a0…`, Pi prompt `0644 9cba75f7…`, R11 input `0644 5af74bcf…`.
- Private R11 delta/bindings/allowlist/forward artifacts remain `0600` with hashes `11c7608e…`, `525f418a…`, `20a4b3be…`, `1d32c75c…`; private and compare roots remain `0700`. R10 preimages remain the bound `0600` artifacts. Intended Review and governed `validate_cross_cli_sync.cpython-314.pyc` remain absent.

## Delta

Authoritative no-Git delta remains `pass`: 80 paths total (Router 66, Companion 14), 37 modified, 42 added, 1 deleted, 85 allowlisted, `unexpected_paths=[]`. The disclosed post-delta reporting-helper field-name error remains evidence-process-only and was not promoted or used to rerun the authoritative delta.

## Verification

Existing focused persistence, rollback, atomic, sandbox, symlink/tree, snapshot, native/no-Pi, and transaction tests passed in corrected runs (`19/19`, `8/8`, and `11/11`). Green tests do not override the independent adversarial probes.

Fresh probes found:

1. **P1 — candidate ownership race before install.** Replacing the Pi candidate immediately before `RENAME_EXCL` returned `PASS/success`, with output inode equal to the unrelated replacement. Generic `atomic_replace` and `atomic_create` likewise accepted a substituted candidate inode. Relevant code: `scripts/validate_cross_cli_sync.py:956-1015`, `:1180-1194`, `:1279-1295`, `:4195-4205`.

2. **P1 — descriptor content race.** Mutating file contents after `_sha256_descriptor` but on the same inode made `_open_guarded_binding` return the stale digest; rollback then succeeded and rewrote that concurrently changed inode. Identity checks catch path/inode replacement, but not same-inode content mutation. Relevant code: `:813-842`, `:4245-4279`.

3. **P1 — quarantine rename is not revalidated.** Candidate substitution immediately before quarantine produced visible `PASS` quarantine evidence. Parent mapping substitution immediately before or immediately after rename returned success while placing evidence in the parked old parent. Relevant code: `:1081-1116`, `:4282-4308`.

4. **P1 — persistent cleanup failure remains unsafe.** Candidate fsync failure plus neutralization failure, and candidate parent-guard failure plus neutralization failure, left hidden `.cross-cli-sync.*` `PASS` candidates while the public result was `BLOCKED`. Persistent quarantine rename collision left hidden `BLOCKED` evidence; generic candidate fsync plus cleanup failure also retained a hidden candidate.

P0: none.  
P1: four findings above.  
P2: none.

## Verdict

**FAIL. Read-only runtime planning may not resume.**

Required before re-review: bind and revalidate candidate device/inode/content/mode immediately before install for Pi and generic atomic paths; close same-inode descriptor content races; revalidate candidate identity and parent mapping after quarantine rename; and guarantee persistent failure paths leave no hidden candidate or unvalidated evidence. Task 10 remains the approved network-backed/native-credentials limitation.
