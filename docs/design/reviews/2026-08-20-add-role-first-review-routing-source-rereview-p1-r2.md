# Candidate Source High Re-review — P1 R2

**Verdict: FAIL**

**Read-only four-target runtime planning may not begin.**

## 1. Reviewer assignment and independence

- Reviewer product: `codex`
- Reviewer role: `independent-reviewer`
- Capability profile: `control-plane-high`
- Review purpose: independently decide whether the twice-corrected candidate source satisfies `add-role-first-review-routing` and may proceed to read-only four-target runtime planning
- Independence: fresh no-history instance, distinct from source authors, executors, prior reviewers, and the bound decision owner
- Result authority: governed implementation Review evidence only

This Review was read-only. I did not modify source or runtime files, run Git or Pi, inspect runtime destinations, create a runtime plan, update canonical state, write the intended Review artifact, or claim completion.

## 2. Bound-input integrity

Every bound hash and mode matched at both Review start and Review end.

| Input | Mode | Start/end SHA-256 | Result |
|---|---:|---|---|
| Implementation Plan | `0644` | `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` | PASS |
| OpenSpec proposal | `0644` | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` | PASS |
| OpenSpec design | `0644` | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` | PASS |
| OpenSpec delta specification | `0644` | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` | PASS |
| OpenSpec tasks | `0644` | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` | PASS |
| Source verification | `0644` | `92a0593203886fe8919d7c7ee8b7ab3313d4e9fa92a81382af0089b876c0e546` | PASS |
| Durable P1-R2 delta summary | `0644` | `7c96f9f5b53ae1ed33e791a126442a261f83d1315d3dd6c8825509e6334a74fa` | PASS |
| First source Review | `0644` | `35050b3e8766b055f11d3a55018d4a34c1aca87893f574b477bbfe28a9cf6ef1` | PASS |
| P1-R1 source re-review | `0644` | `44138637110b7643585d244721cf710f1f08a899dca874fd81df6ab1898d9719` | PASS |
| Corrected sync validator | `0644` | `cef9fca193364a8ccda204fb80a351a656ac5e22c2919c96ecbf28fc7203f4ff` | PASS |
| Corrected cross-CLI tests | `0644` | `95797ae3a2db091661f094c742a9247d098789ff1e453388580f61241e3ac1c8` | PASS |
| Router workflow tests | `0644` | `9e8f1d6904b0eb3e397eafb305f0e1743a77dcd9d9c715ac05e510f4e3aa2dc7` | PASS |
| Router README | `0644` | `44314b9c0f128ddcac90154ac5f36f167f70a66ab93aca61a4b46a86646f08ff` | PASS |
| Router README Chinese | `0644` | `b973047e8092a9b7550ab62db5e795c6a7a0ba30e51304a2541953d4379fb987` | PASS |
| Companion README | `0644` | `f260de8c1e97ca5ce282e39c432278ebed4699745d0cd6c650dc82ece9ffe0b5` | PASS |
| Companion README Chinese | `0644` | `d6180a9a0f54fc0d87934bd24efe320d5f9c7b45cb816292f86db5d1ba2b601c` | PASS |
| Companion workflow tests | `0644` | `65f8e4f2de06dfd050ef74310c94a84d76cec2b54c1955a1fdb66372d5f0b12c` | PASS |
| Private source delta | `0600` | `0e2efdc63378c35f9ff31b36e4471c79e9ffec28fbbfd54293e7cadd68ced6dd` | PASS |
| Private bindings | `0600` | `599616e5aacf064f4ef3c40eb51b7cb49fd8ff9362eac6ca30954f4dae7e3029` | PASS |
| Private allowlist | `0600` | `deb257062c43f18b22a79b97121f1c39991d43ca920289df7842ee6044184a50` | PASS |
| Private forward summary | `0600` | `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` | PASS |
| Private comparison root | `0700` directory | Not applicable | PASS |
| P1-R2 assignment input | `0644` | `9f9a48fdf4afc1890c30d170f5d195f8e059f01acba2606bb3c254b0dd1d2058` | PASS |

The intended artifact `docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r2.md` remained absent throughout.

## 3. Reviewed scope and complete-delta coverage

The complete Router and Companion trees were read without Git:

- Router: 269 files, 3,731,164 bytes
- Companion: 23 files, 299,151 bytes
- `.git` contents were excluded
- Each repository contains only its root `AGENTS.md` and `SKILL.md` as local instruction/Skill files

The private delta reports:

- `source_delta: "pass"`
- 48 actual records: 34 Router, 14 Companion
- 37 modified, 10 added, 1 deleted
- 52 exact allowlist entries
- `unexpected_paths: []`

All 48 records were accounted for against current state. Thirty-five of the 37 modified records have exact comparison-root preimage bytes. The two without comparison preimages are evidence-only history:

- `2026-08-20-evidence-rehydration-r9-inputs.md`, whose transition is already bound by the accepted R9 evidence
- source verification, whose delta-after value was followed by the disclosed P1-R2 evidence append

The 48-record delta contains 39 candidate-source records and nine evidence/history records. The four allowlisted paths not reported as actual changes are:

- unchanged `CONTEXT.md`
- post-delta durable P1-R2 summary
- post-delta P1-R2 input record
- the still-absent intended P1-R2 Review artifact

The current source-verification append, durable summary, and P1-R2 input are correctly classified as post-delta evidence-only state. They do not repair implementation behavior or authorize runtime planning.

## 4. Requirement-to-mechanism-to-test trace

| Requirement | Production mechanism | Test/evidence | Result |
|---|---|---|---|
| Gate-bearing versus advisory Review classification | `SKILL.md:96`; `references/agent-capability-routing.md:45`; Companion `SKILL.md:87` | Router tests `2092-2219`; bound forward summary 6/6 | PASS |
| Exact schema-6 Reviewer Assignment | `scripts/validate_core_gates.py:682-743`, current-only entry at `918-923` | Router tests `2223-2354`; Companion equivalent suite | PASS |
| Full assignment immutability | `scripts/validate_core_gates.py:1380-1406` | Router tests `2443-2470` | PASS |
| Schema-2 identity bound to assignment | `scripts/validate_core_gates.py:1241-1278` | Router tests `2472-2520` | PASS |
| Current/legacy isolation | `scripts/validate_core_gates.py:918-933`, inventory `1039-1065` | Router tests `2356-2441`; Companion tests `882-961` | PASS |
| Four-target manifest and ordering | `scripts/validate_cross_cli_sync.py:27-30`, manifest validation `157-234`, plan generation/validation `2997-3140` | Cross-CLI full suite and plan/closure tests | PASS |
| Public schema-6/schema-2 guidance | Router README `382-402`, Chinese `348-367`; Companion README `205-215`, Chinese `190-198` | Router test `2208-2219`; Companion test `736-745` | PASS |
| Existing-parent destination mutation boundary | parent guard `533-608`; descriptor-relative operations `620-675`; swap/exclusive install `777-935` | Cross-CLI tests `542-751`, `1847-1876` | PASS for existing parents |
| Initially absent parent creation | path-based creation `863-877`, called before descriptor ownership at `1561-1572` | No focused regression; isolated integrity test reproduced incorrect success | FAIL |
| Restore cleanup of created parents | path-based cleanup `1854-1861`, followed by path-based final assertion `1862-1866` | No focused regression; isolated integrity test reproduced false restore success | FAIL |
| Receipt displacement and direct rollback | `_advance_receipt` `1215-1286` | Tests `1636-1718` | PASS for direct receipt displacement |
| Receipt-history collision | `_advance_receipt` `1287-1357` | Test `1720-1744` | PASS for a collision before history installation; incomplete for post-install recovery |
| Later-target exclusion | `_require_prior_targets_verified` `1538-1553` | Later-target tests and isolated receipt test | FAIL for ambiguous post-history rollback |

## 5. Integrity and recovery analysis

### First Review boundary: final destination object

The first correction successfully replaces unconditional leaf replacement/removal:

- Existing targets use `RENAME_SWAP`, validate the exact displaced object, and restore the displaced state when validation fails.
- Absent targets use `RENAME_EXCL`, so a concurrently introduced leaf prevents installation.
- Final-leaf link/type changes fail validation.
- Restore-to-absence first moves the leaf to quarantine, validates it, and restores it if removal cannot be proven.
- Unknown target-closure state moves the receipt to `recovery-blocked`.
- Apply exceptions invoke the target-local restore path and do not start later targets.

The focused tests and independent temporary checks confirm these leaf-object branches.

### P1-R1 boundary: parent identity

The P1-R2 correction binds an already-existing resolved parent chain and retains a no-follow descriptor through candidate creation and leaf mutation. Existing-parent mapping, type, link, and identity changes are detected.

That protection begins too late when destination parents are absent:

1. `_install_candidate_entry` verifies the absent leaf.
2. `_create_parent_directories` creates missing directories by path.
3. Only afterward does `atomic_create` open and bind the then-current resolved parent.

An isolated temporary integrity check changed the mapping after step 2. The production function returned success and installed candidate bytes in the replacement tree. The originally created reviewed tree remained without the candidate. This is a false verified apply path.

### Restore and cleanup branches

Existing-file restore through `atomic_replace`, absent-leaf restore through quarantine, unknown closure, and leaf-level rollback all stop safely.

Created-parent cleanup does not use the bound parent descriptor or saved directory identities. It calls `Path.rmdir()` on recorded strings and suppresses every `OSError`. An isolated temporary integrity check changed the mapping after leaf removal but before cleanup. The replacement empty directory was removed, the reviewed directory was preserved elsewhere, and `_restore_target_locked` returned:

- `restore: "pass"`
- `restored: true`
- receipt state `restored`

This affects state not proven by the reviewed plan and falsely reports verified restoration.

### Receipt and history branches

The direct receipt-displacement correction works:

- The exact displaced receipt must equal the expected current receipt.
- Unambiguous drift restores the changed live receipt.
- If that direct rollback cannot complete, the displaced receipt remains in an orphan temporary recognized by later-target checks.
- A pre-existing history collision causes the live receipt to be restored and leaves the collision unchanged.

A later branch remains unsafe. Once the displaced current receipt has been installed into history, a subsequent durability/identity failure enters the `history_installed` rollback branch at `scripts/validate_cross_cli_sync.py:1302-1338`. If that rollback also cannot complete, the function raises but creates neither a manual-disposition record nor another blocker recognized by `_require_prior_targets_verified`.

An isolated temporary integrity check produced:

- `_advance_receipt` raised `receipt history installation rollback is blocked`
- the live receipt remained revision 2 with state `verified`
- history retained revision 1
- no recognized manual-disposition or orphan-temporary blocker existed
- the later-target guard returned success

Therefore a failed receipt transition can be interpreted as verified during a later invocation.

## 6. Findings

### P0

None.

### P1-1 — Initially absent parent directories are not bound before creation and install

**Location**

- `scripts/validate_cross_cli_sync.py:863-877`
- `scripts/validate_cross_cli_sync.py:1561-1572`

**Problem**

Missing parent directories are created with path-based operations before the descriptor-bound `atomic_create` guard is established. A mapping change after creation can redirect the final install while the function reports success.

**Minimum correction**

- Start from a verified existing ancestor descriptor.
- Create every missing component descriptor-relatively with exclusive, no-follow operations.
- Bind each created directory’s device/inode/mode/owner identity.
- Retain and recheck the complete chain through candidate creation and final install.
- On any mismatch, preserve observed state, enter blocking recovery, and prevent later targets.
- Add production-path tests for initially absent multi-level parents, mapping changes, link/type changes, and ancestor identity changes.

### P1-2 — Restore cleanup may remove an unreviewed replacement directory and report success

**Location**

- `scripts/validate_cross_cli_sync.py:1854-1866`

**Problem**

Cleanup iterates recorded path strings with `Path.rmdir()` and ignores all failures. It neither proves that the removed directory is one created by this transaction nor binds cleanup to the retained directory descriptor.

**Minimum correction**

- Record the exact identities of all transaction-created directories.
- Remove them only descriptor-relatively, in reverse order, after verifying exact identity, emptiness, and containment.
- Treat mapping, identity, type, or cleanup-verification mismatch as `recovery-blocked`.
- Do not suppress a cleanup failure when restore correctness depends on it.
- Add tests showing replacement directories are preserved and restore cannot report `pass` until exact cleanup/restoration is proven.

### P1-3 — Post-history receipt rollback ambiguity is not recognized by the later-target gate

**Location**

- `scripts/validate_cross_cli_sync.py:1287-1357`
- `scripts/validate_cross_cli_sync.py:1538-1553`

**Problem**

After history installation, a failed rollback may leave the revised live receipt marked `verified`. No durable recognized blocker is created, and the later-target guard checks only manual-disposition files, orphan receipt temporaries, and the live receipt’s state/plan hash.

**Minimum correction**

- On every post-history rollback ambiguity, create durable mode-`0600` manual-disposition or equivalent recovery evidence before returning.
- Make later-target, recovery, commit, and verify-all paths reject that evidence.
- Treat the live receipt as untrusted even if its serialized state says `verified`.
- Add focused tests for failure after history rename, history/receipt directory fsync failure, parent recheck failure, successful rollback, failed rollback, retained evidence, and later-target exclusion.

### P2

None.

## 7. Fresh validation evidence

| Command/check | Result |
|---|---|
| Router `/opt/anaconda3/bin/python …/quick_validate.py .` | PASS — `Skill is valid!` |
| Router `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .` | PASS |
| Router `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | PASS — 200 tests |
| Cross-CLI module `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_cross_cli_sync -v` | PASS — 76 tests |
| Companion `/opt/anaconda3/bin/python …/quick_validate.py .` | PASS |
| Companion project validator | PASS |
| Companion full unittest discovery | PASS — 87 tests |
| `openspec validate add-role-first-review-routing --strict` | PASS |
| `openspec validate --all --strict --no-interactive` | PASS — 3 passed, 0 failed |
| Both exact Task 6 negative searches | PASS — empty |
| Router/Companion Handoff `cmp -s` | PASS |
| Shared Handoff and validator-core identity tests | PASS — 2/2 |
| Path-only sensitive audit | PASS — `0 sensitive categories found` |
| Bound forward summary | PASS — 6/6, mode `0600`, expected SHA |
| Complete source-delta audit | PASS — 48 actual, 52 allowlisted, no unexpected paths |

The original isolated Conda environment was not represented as replayed. Its real `bin/python3.11` object remains unavailable. The two quick validators used `/opt/anaconda3/bin/python`, previously accepted for this gate; dependency-free validators and tests used default `python3`.

Green suites do not override the findings because the missing-parent creation, created-parent cleanup, and post-history rollback branches are not covered by the current focused tests.

## 8. Correction and resume conditions

Runtime planning may resume only after all three P1 findings are corrected and the following are complete:

1. Add RED/GREEN production-path tests for the missing-parent, cleanup, and post-history recovery branches.
2. Implement descriptor-relative parent creation and exact created-directory cleanup.
3. Make every ambiguous receipt-history state durable and recognizable by all later-target gates.
4. Rerun both quick/project validators, Router 200+ suite, Companion 87+ suite, cross-CLI module, OpenSpec strict/all, both negative searches, shared-byte checks, sensitive audit, and forward evidence.
5. Regenerate the complete no-Git source delta and bindings.
6. Obtain a fresh independent full Candidate source High Review.

## 9. Final decision

**FAIL**

The role-first routing, schema-6/schema-2 identity model, current/legacy isolation, four-target manifest semantics, sensitive exclusions, public documentation, shared bytes, and most leaf-level recovery behavior are coherent.

However, three production paths can affect state not proven by the reviewed plan or can falsely record/accept verified apply or restore status. Every actionable finding blocks promotion.

**Read-only four-target runtime planning may not begin.**

