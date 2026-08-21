# Source High Re-review — P1 R12

## Assignment and independence

- Product/role/profile: `codex` / `independent-reviewer` / `control-plane-high`
- Fresh no-history implementation: `gpt-5.6-luna`, max reasoning
- Authority: source Review evidence only; no runtime plan, runtime inspection, mutation, self-acceptance, or completion claim
- Required Router/Companion governance files, engineering invariants, closeout contract, approved Plan, R5 PASS, R11 FAIL, and all bound R12 records were read completely.
- No project or private artifact was written. Temporary probes used isolated system temporary directories and were cleaned. No real Pi was run and no runtime destination was inspected.

Process note: one read-only `git status --short --branch` command was accidentally executed before review. No further Git command was run and no mutation occurred.

## Bindings and delta

The bound input matched mode `0644`, SHA-256 `e917722701521307f6bc295bed004ce841d2c748eabd0a897c6f46398a28fc6c`.

Key start/end bindings:

| Artifact | Start/preimage | End/current |
|---|---|---|
| Corrected script | `0600 / 301f4ba2ad3121e1e6799a34184540839715602e3c88608892a23439ae3c0aab` | `0644 / 36b7c55a5688d455192ff850825eb5807e606141129782df8dc4152f34e2ff54` |
| Corrected tests | `0600 / c061b5a02d5b601ee5ea3c521556a2dcbeaed318af5b0399c3f5c184bbfdb1c6` | `0644 / 2aeb37aa97bfbf7f542d9f6e67d64f4500f99c3d0e20d6ae8a67fa70e21524b7` |
| R11 Review | `0644 / 0d89c219a344f9943d9f324d4f36fc0cbb4ec503fc0bce0eb0ceb91912981d62` | unchanged |
| R5 Review | `0644 / 073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4` | unchanged |
| Approved Plan | `0644 / dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` | unchanged |
| Source verification | R11 preimage `0600 / a1aec85aac431b98375fdd51b60c19575d6dcd37c24501c74dd22633bd2e7995`; authoritative delta after also `a1aec...` | current evidence-only append `0644 / 960c857a5f7b14800eb9fa6e4a3252391d2bdca9871019814c4755d78c82a0bf` |
| R12 durable summary | evidence-only, `0644 / aa68cddb16622de36a3d08cb1012c9084f9dfa6a1fe9c5b2f324829ecb0e26d6` | matched |
| Pi prompt | `0644 / 9cba75f75a714110d5efa3a9ff21112f51367a6626e3fdaea596b16544ff04c1` | unchanged |
| Sanitized Pi attempt | `0600 / 2cc4d107db175acce6b66d9439ea8bab191d271695d4f75df4b1302dfa2c255b` | unchanged |
| Intended R12 Review | absent | absent |

Private R12 root and compare roots were mode `0700`; bound private delta, bindings, allowlist, and forward summary were mode `0600` with the supplied hashes. Retry1 delta was `0600 / 3e98e4015b8b461958172c538ea07798de4239d89a2ae0771a9eba1ec84c8e50`; bindings `0600 / b3c52f8cd141e70ab3f61d0366734c888513c5af59da4e6f089979fe24c7fd09`; allowlist `0600 / 2f60dd69f0ff969f5c0f937a7665c5087b8316fcecfc47330ca720954a0ae34f`; forward summary `0600 / 1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b`.

Authoritative retry1 delta:

- 85 actual paths: Router 71, Companion 14.
- Router: 23 modified, 45 added, 3 deleted.
- Companion: 14 modified.
- Three deletions are generated CPython 3.14 caches:
  - `docs/design/evidence/add-codex-skill-update/__pycache__/source-bootstrap-v2-helper.cpython-314.pyc`
  - `scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc`
  - `tests/__pycache__/test_cross_cli_sync.cpython-314.pyc`
- Router modified source/governance paths include `SKILL.md`, READMEs/changelog, source verification, R9 input, all relevant routing/completion/sync references, `validate_core_gates.py`, `validate_cross_cli_sync.py`, and the two test modules.
- Router added paths are the historical R1–R11 evidence/review records, Pi prompt, fixtures, and forward runner.
- Companion modified all 14 bound source/template/validator/test paths.
- Retry1 reports `source_delta: pass`, `unexpected_paths: []`, with 90 allowlisted entries. Five allowlist-only entries are expected evidence/context paths, not actual delta paths.

The first R12 allowlist attempt is preserved: bindings SHA `bb4aead50139702371159922429be24d271ba0a230164fe61283ea7775ce8ec5`, allowlist SHA `07691397dada7f2fb4081730d2627a24fbe701c632abf27450c47e729a278638`, compare root mode `0700`, output absent. It had 88 entries and rejected two unexpected generated cache deletions:

- `docs/design/evidence/add-codex-skill-update/__pycache__/source-bootstrap-v2-helper.cpython-314.pyc`
- `tests/__pycache__/test_cross_cli_sync.cpython-314.pyc`

## Mechanism and test trace

The corrected descriptor path uses one no-follow descriptor, device/inode/type/mode/UID/GID/nlink/size/mtime/ctime identity, and two equal SHA-256 reads. Ctime is ignored only at the reviewed post-rename boundary. Same-inode mutation after either hash, ctime-only pre-install drift, final-stable-check mutation, candidate substitution before install, blocked recovery substitution, quarantine substitution, and parent drift all passed the focused tests.

Focused verification passed:

- 41 generic/RoleFirst candidate, descriptor, Pi persistence, quarantine, cleanup, and native-target tests.
- 9 R3–R11 transaction, receipt, crash, sandbox, backup, and Pi launcher tests.
- Bound fresh evidence reports Router `258/258`, cross-CLI `134/134`, Companion `87/87`, OpenSpec `3/0`, forward `6/6`, and static/shared-byte/audit checks PASS.
- Task 10 remains the approved limitation: a network-backed model requiring native credentials cannot complete without an approved isolated offline/local or temporary non-native route.

The following isolated probes reproduced blocking defects.

## P1 findings

### P1-001 — Generic exchange rollback accepts a one-sided ownership match

Location: `scripts/validate_cross_cli_sync.py:1364-1420`.

`_restore_exchange_after_candidate_mismatch()` allows rollback when either the displaced binding or candidate binding matches:

```python
if not displaced_matches and not candidate_matches:
    raise ...
```

Probe: after `RENAME_SWAP`, the displaced temporary inode was replaced with an unrelated inode. The candidate at the official destination still matched, so rollback proceeded. The official destination ended with `unrelated-displaced`, while the candidate remained under a transaction-pending name. The function reported mutation-boundary failure instead of restoring the reviewed destination or preserving the state under an explicit unsafe name.

A full `apply_sync_transaction()` probe also showed the subsequent backup rollback can overwrite/delete the unrelated inode at the official destination.

### P1-002 — Generic and Pi cleanup retain a check-to-unlink race

Locations:

- Generic `_remove_bound_entry()`: 1443-1490
- Pi `_remove_exact_pi_unsafe_entry()`: 4961-5012

Both paths validate the cleanup name, then call `_guarded_unlink()` without revalidating the retained object immediately before unlink.

Probe: after the retained-binding check, the cleanup name was replaced with an unrelated inode. The unlink returned successfully, deleted the unrelated inode, and produced no recovery residue for both generic and Pi paths.

This directly violates the no-unrelated-inode-delete invariant.

### P1-003 — Pi rename-then-raise leaves official `PASS` evidence

Location: `_persist_pi_probe_result()`, 4647-4785.

`installed` is set only after `_renameatx()` returns. Probe made candidate-to-output rename mutate the namespace and then raise. The candidate disappeared, `installed` remained false, and the official output retained the original `PASS` bytes.

`execute_pi_probe()` returned an in-memory `BLOCKED` result, but the official output path still contained `PASS`. The persistence failure therefore leaves accepted-looking PASS evidence.

### P1-004 — Blocked recovery rename crash window accepts malformed blocked evidence

Location: `_create_pi_blocked_recovery()`, 4812-4932.

Probe substituted malformed bytes at the pending name, performed pending-to-blocked rename, and then raised after the namespace mutation. The resulting `persistence-blocked.*` path contained `MALFORMED` bytes.

The rename exception occurs before the post-rename identity/content revalidation and recovery branch. A crash at this boundary can therefore leave malformed or substituted content under a blocked-evidence name.

### P1-005 — Pi rollback collision leaves unrelated content at the official output

Locations: `_persist_pi_probe_result()`, 4710-4764; `_restore_pi_install_after_mismatch()`, 4788-4809.

Probe replaced the installed output with an unrelated inode and occupied the candidate name before rollback. `_restore_pi_install_after_mismatch()` rejected rollback because the candidate name was occupied. The candidate blocker was moved to `persistence-unsafe.*`, but the official output remained the unrelated bytes.

The outer fallback could not write BLOCKED evidence because the output was no longer absent. The caller returned BLOCKED while the official output remained unrelated non-evidence content.

## Severity summary

- P0: none observed.
- P1: five reproducible findings above.
- P2: none separately required; the P1 defects already block promotion.

The descriptor-binding and ordinary pre/post rename/quarantine protections are materially improved and pass their focused tests, but they do not close rollback, check-to-unlink, or rename-crash boundaries.

## Resume conditions and verdict

Read-only four-target runtime verification may **not resume**.

Required before a fresh independent review:

- Require both retained ownership sides before exchange rollback.
- Add immediate retained-object validation at the unlink boundary for generic and Pi cleanup.
- Handle rename-side-effect/exception windows by inspecting and classifying both names before any evidence name is accepted.
- Ensure Pi rollback collisions leave only explicit `persistence-unsafe`/`persistence-pending` residue and a durable mode-`0600` `BLOCKED` record.
- Add regression probes for all five findings, then rebind the complete R12 delta and perform a fresh source review.

Final verdict: **FAIL**.
