# Candidate Source High Re-review — P1 R15

## Assignment and independence

- Product/role/profile: `codex` / `independent-reviewer` / `control-plane-high`
- Bound implementation: fresh no-history `gpt-5.6-luna`, max reasoning
- Authority: source Review evidence only
- Reviewed Router and Companion `AGENTS.md`/`SKILL.md`, engineering invariants, closeout contract, approved Plan/OpenSpec, prior R5 PASS and R11–R14 FAIL Reviews, the complete R15 delta, and current production source.
- No project/private writes, Git, Pi execution, runtime destination inspection, runtime plan, or completion claim performed.

## Bindings and delta

| Item | Mode | SHA-256 |
|---|---:|---|
| Approved Plan | 0644 | `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| R5 PASS | 0644 | `073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4` |
| R11 FAIL | 0644 | `0d89c219a344f9943d9f324d4f36fc0cbb4ec503fc0bce0eb0ceb91912981d62` |
| R12 FAIL | 0644 | `35c38b467e5d2bacc4fdd90708c41801f36b494810a5ed4ea33b5b8fee24abc0` |
| R13 FAIL | 0644 | `5b7ffc4fb35a1072454145f3f1e104a21c4fa2bad28f9d7cab7ae82f5a823b17` |
| R14 FAIL | 0644 | `21c8af525ada608343c9498697020d9dbd28a763bf461b4218ff4451a8b77cc5` |
| Current source verification | 0644 | `b219726855c17c8e0bd50005aadcbbc05d5e06bb7bead7e4b60be00312665335` |
| R15 input | 0644 | `54938207d773a24159414e9fc824fb1b493de6af7bcce11680ab5f7a62f9a36b` |
| R15 summary | 0644 | `0e117004c83b30a68d4b76d86dcc52cf80ba0be9436f78ff78fb2fdf6c58413c` |
| R15 script | 0644 | `f4759f7e4f73576cfd6db3a8398ad43944a6ad7f9b6db968964c0444c03a881` |
| R15 tests | 0644 | `5557cb2cdea3d95ae2cbf09a1c5420bb7faa4729829d81c8f0ca9859b7e9b063` |
| Private delta | 0600 | `5898349948ca8ade6cece1460f15367f3b0767d1057ae913de55ee52197576f9` |
| Private bindings | 0600 | `abbe2e5f5f0bd3871d8fc23834519ae993e7e5053b0cc4e4a27f75377ac6c923` |
| Private allowlist, 99 entries | 0600 | `5ad2294d2a6d9d1cd3e5662ac4d237a27dfe83da3409b79fb20a4691842e6f40` |

The R15 backup root is mode `0700` at
`/private/tmp/add-role-first-review-routing-p1r15-20260821-luna`. The intended
R15 Review artifact was absent.

The read-only rebind found `source_delta: pass`, `unexpected_paths: []`, and
all 95 records present with expected modes and hashes, except the two
explicitly expected evidence-only post-delta SHA changes for the
source-verification append and R15 input final binding. The delta contains 81
Router records and 14 Companion records: 23 Router modifications, 55
additions, 3 generated-cache deletions, and 14 Companion modifications. No
unrelated paths, symlinks, special files, or unallowlisted residue were found.

## Validation

Fresh validation results:

- Router core gates: PASS
- Router and Companion `quick_validate.py`: PASS using the authorized isolated Conda interpreter
- Router workflow tests: `124/124 PASS`
- Router cross-CLI tests: `148/148 PASS`
- Companion tests: `87/87 PASS`
- Companion template validation: PASS
- OpenSpec strict change validation: PASS
- OpenSpec strict all validation: `3 passed, 0 failed`
- Stale-schema/old-product and generic-agent wording checks: clean
- Shared Handoff identity/comparison checks: PASS
- Sensitive path audit: `0 sensitive categories found`
- Current project residue: only the previously bound pre-existing `cpython-311` caches; no R15 transaction, persistence, debug, raw-output, credential, or Pi-review residue

On Darwin, `os.unlinkat` is unavailable. The libc `unlinkat` symbol exists but
is name-based, not inode-CAS or unlink-by-retained-descriptor. The production
seam at `scripts/validate_cross_cli_sync.py:1103-1114` correctly raises
`_ExactOwnerCleanupUnavailable` and does not fall back to ordinary name-based
unlink.

## Fresh production probes

- Generic normal cleanup: fail-closed; retained object preserved as visible
  `transaction-unsafe` recovery, mode-0600 blocker written, no unrelated inode
  deleted or accepted.
- Generic replacement after final retained-inode bind: unrelated replacement
  preserved, retained inode preserved separately, visible recovery and blocker
  written; no unrelated deletion or acceptance.
- Pi normal cleanup with valid canonical `PASS` evidence: visible
  recovery/blocker residue was produced; all Pi JSON residue was `BLOCKED`, mode
  0600, with no remaining `PASS`.
- Pi replacement after final retained-inode bind: unrelated replacement was
  preserved and a mode-0600 blocker was written, but the retained valid `PASS`
  inode remained unchanged under the visible retained-aside name.

## Findings

### P0

None.

### P1-001 — Pi final-bind replacement leaves retained PASS evidence unchanged

Location: `scripts/validate_cross_cli_sync.py:1133-1155`, `:1290-1317`,
`:1201-1229`, and caller `:5558-5626`.

At `:1133-1153`, the final rebound descriptor is opened and validated before
the deletion seam. The fresh isolated probe then moved that exact retained
inode aside and replaced the quarantine name with unrelated bytes before
`_unlinkat_kernel`.

The seam correctly raised `_ExactOwnerCleanupUnavailable`, so the unrelated
inode was not deleted. However, the recovery branch at `:1290-1301` only calls
`_rewrite_bound_owned_content()` when `_retained_binding_matches_name()` still
matches the quarantine name. After the replacement, that check is false, so
the rewrite at `:1303-1310` is skipped. The already-validated retained
descriptor is closed at `:1154-1155`, and `_remove_exact_pi_unsafe_entry()`
swallows the failure at `:5623-5626`.

Result: the visible retained-aside object still contained valid JSON with
`"verdict": "PASS"` and mode `0600`, alongside the blocked evidence.

This violates the R15 requirements in
`docs/design/evidence/add-role-first-review-routing/2026-08-21-source-rereview-p1-r15-inputs.md:49-57`
and the source-verification claim at
`docs/design/evidence/add-role-first-review-routing/2026-08-10-source-verification.md:1771-1778`:
Pi must rewrite retained PASS-shaped evidence through the validated descriptor
and must not leave PASS-shaped evidence.

The regression at `tests/test_cross_cli_sync.py:2472-2538` misses this because
it writes arbitrary `b"original-pass\n"` bytes and checks only residue
existence, not semantic JSON verdict.

## P2

None.

## Resume conditions

1. Change Pi fail-closed recovery so the retained object is rewritten through
   the already validated descriptor, or otherwise guarantee that a retained
   PASS-shaped object cannot remain visible when its namespace name is replaced
   after final bind.
2. Add a valid canonical JSON PASS replacement probe and assert that every
   retained/recovery Pi evidence object is `BLOCKED`, with no PASS-shaped
   residue.
3. Preserve the existing generic guarantee that unrelated replacement inodes
   are never deleted or accepted.
4. Rerun the six focused R15 probes, full validators/tests, static and residue
   checks, complete no-Git delta rebinding, and obtain a fresh independent
   Candidate Source High Review.

## Final verdict

**FAIL — P1-001 remains open.**

Fail-closed deletion and unrelated-inode safety are materially improved, but
the current implementation does not satisfy the required Pi PASS-evidence
invariant. Runtime verification and planning must remain blocked; no Pi or
runtime operation may resume.
