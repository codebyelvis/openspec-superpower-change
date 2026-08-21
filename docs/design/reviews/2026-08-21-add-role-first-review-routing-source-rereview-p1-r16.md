# Candidate Source High Re-review — P1 R16

## Assignment and independence

- Product/role/profile: `codex` / `independent-reviewer` / `control-plane-high`
- Authority: source Review evidence only.
- Read Router and Companion `AGENTS.md`/`SKILL.md`, engineering invariants,
  closeout contract, approved Plan/OpenSpec, prior R5 PASS and R11–R15 FAIL
  Reviews.
- No project/private writes, Git, Pi execution, runtime-destination
  inspection, runtime plan, or completion claim performed.
- Final R16 input SHA was verified at both review boundaries: mode `0644`,
  SHA-256 `f5a6c9e4505f0f793399b223c557c01c85106427421005b7e9ca5547845eb0d6`.

## Bindings

| Input | Mode / SHA-256 |
|---|---|
| Approved Plan | `0644` / `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| Prior Source R5 PASS | `0644` / `073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4` |
| Prior Source R11 FAIL | `0644` / `0d89c219a344f9943d9f324d4f36fc0cbb4ec503fc0bce0eb0ceb91912981d62` |
| Prior Source R12 FAIL | `0644` / `35c38b467e5d2bacc4fdd90708c41801f36b494810a5ed4ea33b5b8fee24abc0` |
| Prior Source R13 FAIL | `0644` / `5b7ffc4fb35a1072454145f3f1e104a21c4fa2bad28f9d7cab7ae82f5a823b17` |
| Prior Source R14 FAIL | `0644` / `21c8af525ada608343c9498697020d9dbd28a763bf461b4218ff4451a8b77cc5` |
| Prior Source R15 FAIL | `0644` / `c77d7a284867063abdcaccb941844cc673550aeaf18228fecfd3f383ff29f3fc` |
| Current source verification | `0644` / `b7bcbfb9c826f2dc27c71abe88f071aa03aa9b89dc8f2446fb89b74c3a97340c` |
| R16 implementation script | `0644` / `09813290af1b6c869215e6c372849334730eddce33860797407b61e9b8619ea6` |
| R16 tests | `0644` / `57424b7da282e505acc6b32b6c72ef04c6f58b942757388357f14b7bc513b590` |
| R16 private delta | `0600` / `b4670cb53ad033ddc198b42d5e06315aaa47f091efc7253b68889d2023299bce` |
| R16 private bindings | `0600` / `b328f4e18ae4243aeebe03b816d1585d5b5fb438fa5591b014e8eec60f5857ca` |
| R16 allowlist, 102 entries | `0600` / `8ce732f416d70f0caf5391e1dc9ff63450543a1e7154d67efe64b07626542032` |
| R16 durable summary | `0644` / `f409f302910303daa421c0e5c265cd34bf1fbd06145864d55dc859376362dfdc` |
| Fresh forward summary | `0600` / `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |
| Compare root | mode `0700`, `/private/tmp/add-role-first-review-routing-p1r16-20260821-luna/source-compare-r16-clean` |

The intended R16 Review artifact was absent at review start and end.

## Complete delta classification

The authoritative no-Git delta reports:

- `98` records total: `84` Router and `14` Companion.
- Router: `23` modified, `58` added, `3` expected generated-cache deletions.
- Companion: `14` modified.
- `source_delta: pass`; `unexpected_paths: []`.
- All current implementation/source records matched expected hashes and modes.
- The only expected evidence-only discrepancy was the R16 input’s pre-final-
  append after-hash; the current final input SHA is the explicitly required
  `f5a6c9e...`.
- Four allowlist-only evidence paths were reviewed: Router `CONTEXT.md`, the
  prior R6 Review, the durable R16 summary, and the intentionally absent R16
  Review artifact. No delta-only paths existed.
- Compare-root inspection found no symlinks or special files. Before-preimage
  checks matched all applicable records; only expected baseline-excluded
  historical/cache records were absent.
- Supplemental recheck evidence also reported `source_delta: pass` and
  `unexpected_paths: []`, but retained its earlier pre-append R16 input hash
  and was not promoted over the final binding.

No unallowlisted source, private, debug, raw-output, credential, or token
residue was found.

## Production mechanism review

### Exact-owner deletion boundary

`_unlinkat_kernel()` explicitly raises `_ExactOwnerCleanupUnavailable` at
`scripts/validate_cross_cli_sync.py:1103-1114`. Darwin lacks `os.unlinkat`;
the available libc `unlinkat` is name-based and supplies no inode-CAS or
unlink-by-retained-descriptor primitive.

The final generic cleanup path at `scripts/validate_cross_cli_sync.py:1117-1155`
reopens and validates the retained object, checks identity, prestate, stability,
and parent binding, then invokes the seam without any name-based fallback.

On failure, `scripts/validate_cross_cli_sync.py:1264-1345` preserves visible
recovery and writes an explicit blocker. Generic cleanup therefore does not
delete or accept an unrelated replacement inode.

### Pi retained-object rewrite

R16 changes `scripts/validate_cross_cli_sync.py:1201-1246` so the blocked
rewrite uses the already validated retained descriptor rather than reopening
the namespace name. It:

- verifies descriptor availability and writable access;
- rechecks parent identity, object identity, and exact prestate;
- truncates/writes/fsyncs through the retained descriptor;
- rebinds and verifies object identity, mode, and blocked-content SHA.

The exact-owner failure branch at `scripts/validate_cross_cli_sync.py:1305-1338`
now performs this rewrite even when the quarantine namespace has been replaced.
It chooses `persistence-blocked` only when the quarantine name still identifies
the retained object; otherwise it preserves the unrelated replacement as
`persistence-unsafe` while neutralizing the retained inode through its
descriptor.

Pi candidates are created with `O_RDWR` at
`scripts/validate_cross_cli_sync.py:1544-1565`. The defensive read-only
ownership path at `scripts/validate_cross_cli_sync.py:5568-5667` upgrades
through the validated same-name binding with `writable=True`, rechecks
identity/prestate, and closes the upgraded descriptor on every path.

## Fresh isolated production probes

All probes used temporary directories only and imported the current production
source.

- Darwin/POSIX primitive check: `os.unlinkat` unavailable; libc symbol present
  but name-based; production seam raised `_ExactOwnerCleanupUnavailable`.
- Generic final-bind replacement:
  - replacement injected after final retained-object bind;
  - unrelated inode preserved;
  - retained inode preserved separately;
  - visible unsafe recovery and mode-`0600` blocker produced;
  - no unrelated deletion or acceptance.
- Generic post-delete uncertainty:
  - fail-closed;
  - mode-`0600` blocker retained;
  - no hidden transaction candidate remained.
- Pi normal cleanup with canonical PASS input:
  - no canonical JSON `verdict: PASS` residue;
  - recovery/blocker objects were mode `0600`;
  - retained evidence was rewritten to canonical BLOCKED bytes.
- Pi final-bind replacement with canonical PASS input:
  - replacement injected after final bind;
  - unrelated inode preserved;
  - retained inode rewritten through its validated descriptor;
  - retained-aside content became BLOCKED;
  - `pi_pass_residue: []`;
  - blocker modes were `0600`.
- Read-only ownership descriptor upgrade:
  - `writable=True` upgrade observed and succeeded;
  - identity/prestate remained bound;
  - final replacement still produced no accepted PASS evidence.
- An intentionally impossible writable-upgrade branch retained only visible
  `persistence-unsafe` recovery plus mode-`0600` BLOCKED evidence, without an
  official accepted output. This is the specified uncertainty fallback and is
  not a promotion-blocking finding.

The new semantic regression at `tests/test_cross_cli_sync.py:2540-2621` uses
valid canonical JSON PASS bytes, performs final-bind replacement, asserts
retained-aside rewrite to BLOCKED, checks every JSON residue for
`verdict != PASS`, and verifies no temporary candidate remains. Generic
coverage is at `tests/test_cross_cli_sync.py:1241-1299`.

## Validation and residue checks

Fresh/current validation:

- Router core gates: PASS.
- Router quick validation: PASS.
- Companion quick validation: PASS.
- Router workflow: `124/124 PASS`.
- Router cross-CLI: `149/149 PASS`.
- Router full discovery: `273/273 PASS`.
- Companion full suite: `87/87 PASS`.
- Companion template validation: PASS.
- OpenSpec strict/all: `3 passed, 0 failed`.
- Static policy-negative searches: clean.
- Shared Handoff and shared validator identity checks: PASS.
- Sensitive audit: `0 sensitive categories found`.
- Forward summary: all `6/6` sanitized cases PASS.

Current project residue is limited to the previously bound pre-existing Python
3.11 caches:

- `docs/design/evidence/add-codex-skill-update/__pycache__/source-bootstrap-v2-helper.cpython-311.pyc`
- `scripts/__pycache__/validate_cross_cli_sync.cpython-311.pyc`
- `tests/__pycache__/test_cross_cli_sync.cpython-311.pyc`

No R16 transaction, persistence, debug, raw-output, credential, Pi-review,
symlink, or special-file residue exists.

## Findings

### P0

None.

### P1

None.

R15’s P1—retained canonical Pi PASS bytes surviving final-bind namespace
replacement—is closed by the descriptor-based rewrite at
`scripts/validate_cross_cli_sync.py:1201-1246`, the exact-owner failure
integration at `:1305-1338`, the writable-upgrade path at `:5568-5667`, and the
valid-canonical-PASS regression at `tests/test_cross_cli_sync.py:2540-2621`.

### P2

None.

## Resume conditions

The R16 source gate is satisfied. Runtime verification may resume under its
separately approved runtime gate and plan, while preserving the approved Task
10 external limitation.

This Source Review did not run Pi, inspect runtime destinations, create a
runtime plan, mutate runtime state, or authorize completion. The parent agent
may persist this Review text through the authorized evidence workflow.

## Final verdict

**PASS — R16 closes the R15 retained-PASS evidence boundary.**

No P0, P1, or P2 finding remains. Source-level promotion is permitted, and
runtime verification may resume only through the subsequent governed runtime
phase.
