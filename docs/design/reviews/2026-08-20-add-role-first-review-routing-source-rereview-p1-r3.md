# Candidate Source High Re-review — P1 R3

**Verdict: FAIL**

**Read-only four-target runtime planning may not begin.**

## 1. Reviewer assignment and independence

- Reviewer product: `codex`
- Reviewer role: `independent-reviewer`
- Capability profile: `control-plane-high`
- Review purpose: independently decide whether the thrice-corrected candidate source satisfies `add-role-first-review-routing` and may proceed to read-only four-target runtime planning
- Independence: fresh no-history instance distinct from authors, executors, prior reviewers, and the bound decision owner
- Result authority: governed implementation Review evidence only

This Review was read-only. I did not modify source or runtime files, run Git or Pi, inspect runtime destinations, create a runtime plan, update canonical state, write the intended Review artifact, or claim completion.

## 2. Bound-input integrity

Every bound primary/private input matched at both Review start and Review end.

| Input | Mode | Start/end SHA-256 | Result |
|---|---:|---|---|
| P1-R3 assignment input | `0644` | `2546f8b1a7165498d9334ae0c200fa7379ed284a9af25c1463b01de94b697cf1` | PASS |
| Implementation Plan | `0644` | `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` | PASS |
| OpenSpec proposal | `0644` | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` | PASS |
| OpenSpec design | `0644` | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` | PASS |
| OpenSpec delta specification | `0644` | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` | PASS |
| OpenSpec tasks | `0644` | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` | PASS |
| Source verification | `0644` | `fba7622846aecde308a7289958056b54aee0781b3af4a99ab2d2f4fe6a038f4a` | PASS |
| Durable P1-R3 delta summary | `0644` | `6b02a2a5a97155b80d0cff2a02efcdcfd73537719645b5e35a2c9f9095ea447c` | PASS |
| First source Review | `0644` | `35050b3e8766b055f11d3a55018d4a34c1aca87893f574b477bbfe28a9cf6ef1` | PASS |
| P1-R1 source re-review | `0644` | `44138637110b7643585d244721cf710f1f08a899dca874fd81df6ab1898d9719` | PASS |
| P1-R2 source re-review | `0644` | `5991be2198f4387bb0e860733352fb98e063e22bfcd694eacd3f4704932429b3` | PASS |
| Corrected sync validator | `0644` | `a6420e3ee88a606a0ccf963fe04d7725d53e995526d76abb07a8bef8ca307202` | PASS |
| Corrected cross-CLI tests | `0644` | `fbb702da40475a442c6abe6ea98ce4e337f8d6751a405853fd38f7abc64a2f95` | PASS |
| Router workflow tests | `0644` | `9e8f1d6904b0eb3e397eafb305f0e1743a77dcd9d9c715ac05e510f4e3aa2dc7` | PASS |
| Router README | `0644` | `44314b9c0f128ddcac90154ac5f36f167f70a66ab93aca61a4b46a86646f08ff` | PASS |
| Router README Chinese | `0644` | `b973047e8092a9b7550ab62db5e795c6a7a0ba30e51304a2541953d4379fb987` | PASS |
| Companion README | `0644` | `f260de8c1e97ca5ce282e39c432278ebed4699745d0cd6c650dc82ece9ffe0b5` | PASS |
| Companion README Chinese | `0644` | `d6180a9a0f54fc0d87934bd24efe320d5f9c7b45cb816292f86db5d1ba2b601c` | PASS |
| Companion workflow tests | `0644` | `65f8e4f2de06dfd050ef74310c94a84d76cec2b54c1955a1fdb66372d5f0b12c` | PASS |
| Private source delta | `0600` | `8a60ac663085bc765e49a30e47a1a19d10bbf3c19a78a574c6a0aa116fe027d8` | PASS |
| Private preflight bindings | `0600` | `bdbfa99b93bd17ff86c61a2f119b1c07a74785fb868519d80e1f5ed9f5060d6f` | PASS |
| Private allowlist | `0600` | `cfa09d50b6c83e13d252ddd4f9bdbbced55dcc86503ee6bbccad8b50c95eb847` | PASS |
| Private forward summary | `0600` | `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` | PASS |
| Private comparison root | `0700` directory | Not applicable | PASS |

The intended artifact `docs/design/reviews/2026-08-20-add-role-first-review-routing-source-rereview-p1-r3.md` remained absent. The governed `scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc` path also remained absent.

## 3. Reviewed scope and complete-delta coverage

The complete current Router and Companion source, instructions, Skills, contracts, tests, documentation, OpenSpec records, evidence, delta records, and all three prior FAIL Reviews were reviewed without Git.

The bound private delta reports:

- `source_delta: "pass"`
- 51 actual records: 37 Router and 14 Companion
- 37 modified, 13 added, 1 deleted
- 55 exact allowlist entries
- `unexpected_paths: []`

Fifty of the 51 private-delta after-states still match current mode and SHA exactly. The sole difference is the disclosed evidence-only append to source verification:

- Private-delta after-state: `92a0593203886fe8919d7c7ee8b7ab3313d4e9fa92a81382af0089b876c0e546`
- Current bound state: `fba7622846aecde308a7289958056b54aee0781b3af4a99ab2d2f4fe6a038f4a`

The durable P1-R3 summary and this P1-R3 input record were added after the private delta and are also evidence-only. A fresh temporary no-Git reconstruction therefore reported:

- 53 actual current paths
- 55 allowlisted paths
- `unexpected_paths: []`

The two allowlisted but non-actual paths are unchanged `CONTEXT.md` and the still-absent intended P1-R3 Review artifact. The post-delta evidence records do not change candidate implementation behavior or authorize runtime planning.

## 4. Requirement-to-mechanism-to-test trace

| Requirement | Production mechanism | Test/evidence | Result |
|---|---|---|---|
| Role-first, gate-bearing/advisory classification | `SKILL.md:82-105`; `references/agent-capability-routing.md:28-54`; Companion `SKILL.md:74-105` | Router and Companion workflow suites; bound forward summary 6/6 | PASS |
| Concrete schema-6 Reviewer Assignment | `scripts/validate_core_gates.py:629-743`, current entry `918-923` | Router tests `2223-2354`; Companion tests `749-832` | PASS |
| Immutable Reviewer Assignment | `scripts/validate_core_gates.py:1380-1406` | Router tests `2443-2470`; Companion equivalent | PASS |
| Schema-2 evidence identity bound to assignment | `scripts/validate_core_gates.py:1241-1278` | Router tests `2472-2530`; Companion equivalent | PASS |
| Current/legacy isolation | `scripts/validate_core_gates.py:918-933` | Router/Companion current and legacy suites; public guidance | PASS |
| Sequential final verification/Review | `scripts/validate_core_gates.py:1508-1546` | Transition suites in both repositories | PASS |
| Four-target manifest and ordering | `scripts/validate_cross_cli_sync.py:27-28`; `references/cross-cli-portable-manifest.json:1-65`; plan validation `3436-3512` | Cross-CLI module and closure tests | PASS |
| Deterministic discovery and portable parity | `scripts/validate_cross_cli_sync.py:280-324`, `2366-2390`, `3580-3599` | Cross-CLI full suite | PASS |
| Sensitive-category exclusions | `scripts/validate_cross_cli_sync.py:3602-3610` and manifest deny rules | Path/category-only audit | PASS |
| Public schema-6/schema-2 guidance | Router README `382-408`, Chinese `348-373`; Companion README `205-215`, Chinese `190-198` | Public-doc assertions in both workflow suites | PASS |
| Descriptor-bound creation of initially absent parents | `scripts/validate_cross_cli_sync.py:693-771`, install/persistence `1797-1900` | Tests `1880-1991`; fresh persistence-failure probe | PASS |
| Exact created-parent identity recorded before leaf installation | Receipt callback `1811-1823`, `1880-1887` | Test `1993-2018` | PASS for generation; FAIL for restore-time semantic binding |
| Restore accepts only the planned transaction-created directories | Validation `642-667`; binding `2056-2076`; cleanup `2079-2151`; restore `2179-2248` | Existing cleanup tests and fresh malformed-record probe | **FAIL** |
| Non-empty cleanup and rollback ambiguity block safely | `scripts/validate_cross_cli_sync.py:2086-2137` | Tests `2020-2125`; fresh temporary rollback-ambiguity probe | PASS when the record itself is trustworthy |
| Durable receipt-history blocker | `scripts/validate_cross_cli_sync.py:1398-1589` | Tests `2127-2220`; fresh branch inspection | PASS |
| Every later gate rejects retained blocker | `scripts/validate_cross_cli_sync.py:1769-1789`, `2186`, `2398`, `2428`, `2486`, `2513`, `2583-2585` | Later-target, recovery, verification, and ambiguity tests | PASS |

## 5. Software-integrity and recovery analysis

### First correction generation: leaf-object identity

The leaf replacement/removal correction remains coherent. Descriptor-bound parent guards, exchange/exclusive operations, exact displaced-state validation, and quarantine rollback protect existing and absent destination leaves. Receipt displacement and direct rollback tests at `tests/test_cross_cli_sync.py:1638-1768`, together with leaf mutation tests at `653-798` and restore tests at `1769-1878`, cover mapping, link, type, collision, and rollback branches.

No regression was found in this generation.

### Second correction generation: existing-parent chains, receipt rollback, and public contracts

Existing directory chains are captured and rechecked by `scripts/validate_cross_cli_sync.py:543-608`. Receipt transitions validate the live object and its displaced state before history advancement. Router and Companion public documents now describe schema 6, schema-2 evidence, and frozen schema-4/schema-5 audit-only behavior consistently.

No regression was found in these corrected areas.

### Third correction generation: initially absent parents

`_verified_parent_with_creation` starts from a verified existing ancestor, creates each missing component descriptor-relatively, opens it no-follow, captures the full identity chain, retains descriptors through leaf install, and detects mapping/link/type/ancestor changes (`scripts/validate_cross_cli_sync.py:693-771`).

New records are persisted through a receipt transition before `atomic_create` installs the leaf (`1797-1823`, `1877-1900`). A fresh temporary failure injected between directory creation and receipt persistence left a `recovery-blocked` receipt, did not install the leaf, and prevented later progress. This branch now fails closed.

### Created-parent restore and cleanup

For a trusted record, `_remove_created_directory` verifies the recorded chain and final identity, moves the directory descriptor-relatively to an exclusive quarantine name, fsyncs, removes only the exact empty object, and attempts rollback on failure (`2079-2137`). Existing tests preserve replacement/non-empty directories (`tests/test_cross_cli_sync.py:2020-2125`). A fresh rollback-ambiguity probe confirmed that an obstructed rollback retained the quarantine object and reported a blocking error.

The trust boundary for the record itself is incomplete:

- `_validate_created_parent_records` checks field shape, absolute paths, uniqueness, chain continuity, and only that the chain’s last path equals `record["path"]` (`642-667`).
- `_bound_created_parent_records` checks that recorded `logical_path` values are a subset of planned logical paths and that the independently supplied path/chain exists (`2056-2076`).
- It never proves that a record’s `path` and `chain` are the actual resolved identity produced for that `logical_path` by the reviewed plan.
- `_remove_created_directory` consequently removes the directory selected by the unbound `path`/`chain` (`2079-2137`).
- `_assert_created_parent_roots_absent` repeats the same unbound mapping (`2140-2151`), after which restore advances the receipt to `restored` (`2228-2239`).

A fresh isolated temporary check supplied structurally valid, complete logical-path records whose `path`/`chain` fields described distinct unrelated empty directories. Production `restore_target`:

- removed all four unrelated directories,
- left all four directories actually created by the transaction,
- returned `restore: "pass"`, and
- advanced the receipt to `restored`.

This is an unsafe state change outside the identity proven by the reviewed transaction and a false successful-restore result.

The existing focused test at `tests/test_cross_cli_sync.py:1993-2018` checks only record fields, the planned logical-path set, terminal path equality, and identity length. The suite contains no negative coverage for semantic logical-path/path mismatch, arbitrary valid-chain substitution, truncated anchor provenance, or conditionally incomplete record sets.

### Receipt-history transition and later gates

The P1-R3 transition blocker is installed mode `0600` and fsynced before history movement (`scripts/validate_cross_cli_sync.py:1398-1421`). Successful history installation removes it only after both directories and chains are rechecked (`1497-1520`). Successful rollback restores exact live/history states before removing it; failed or ambiguous rollback retains it (`1521-1584`).

Tests at `tests/test_cross_cli_sync.py:2127-2220` cover successful and failed post-history rollback. The later-target, restore, content verification, discovery, commit, recovery, and verify-all gates all reject the retained marker. No remaining defect was found in this branch.

## 6. Findings

### P0

None.

### P1-1 — Restore-time created-parent evidence is not bound from logical path to actual path and chain

**Locations**

- `scripts/validate_cross_cli_sync.py:642-667`
- `scripts/validate_cross_cli_sync.py:2056-2076`
- `scripts/validate_cross_cli_sync.py:2079-2151`
- `scripts/validate_cross_cli_sync.py:2179-2248`
- `tests/test_cross_cli_sync.py:1993-2018`

**Problem**

A record can preserve a planned `logical_path` while supplying a different, internally valid absolute `path` and directory chain. Restore accepts that record, removes the unrelated directory it names, leaves the transaction-created planned hierarchy behind, and records successful restoration.

**Required correction**

- Bind every planned logical created-parent path to the exact resolved path, verified ancestor provenance, full chain, and identity captured during creation.
- Validate an exact one-to-one record set, rather than a subset plus current path-existence heuristic.
- Reject missing, extra, reordered, duplicate, hierarchy-inconsistent, truncated-provenance, or logical/path/chain-mismatched records before any restore mutation.
- Ensure cleanup and final absence checks consume only this plan-bound mapping.
- On any binding failure, preserve observed state, move or retain the receipt in a blocking state, and prevent all later gates.

**Required tests**

Add RED/GREEN production-path cases for:

- logical-path/path mismatch,
- substitution of a different valid absolute chain,
- incomplete or truncated chain provenance,
- missing and extra records,
- wrong hierarchy/depth and duplicate identities,
- substituted empty and non-empty directories,
- no change to unrelated paths,
- exact cleanup of the actual transaction-created hierarchy,
- receipt not advancing to `restored` on any mismatch, and
- later-target/recovery/verify-all exclusion after rejection.

## 7. Fresh validation evidence

| Command/check | Result |
|---|---|
| Router `/opt/anaconda3/bin/python …/quick_validate.py .` | PASS — `Skill is valid!` |
| Router `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .` | PASS |
| Router `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | PASS — 208 tests |
| Cross-CLI module `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_cross_cli_sync -v` | PASS — 84 tests |
| Companion `/opt/anaconda3/bin/python …/quick_validate.py .` | PASS — `Skill is valid!` |
| Companion `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_templates.py .` | PASS |
| Companion full unittest discovery | PASS — 87 tests |
| `openspec validate add-role-first-review-routing --strict` | PASS |
| `openspec validate --all --strict --no-interactive` | PASS — 3 passed, 0 failed |
| Both exact Plan negative searches | PASS — empty |
| Shared Router/Companion Handoff byte comparison | PASS |
| Shared Handoff plus validator-core identity tests | PASS — 2/2 |
| Path/category-only sensitive audit | PASS — `0 sensitive categories found` |
| Bound forward summary | PASS — 6/6 result rows, expected mode/SHA |
| Fresh temporary no-Git source-delta reconstruction | PASS — 53 actual, 55 allowlisted, no unexpected paths |
| Fresh initially-absent-parent persistence-failure probe | PASS — recovery blocked before leaf install |
| Fresh created-parent cleanup rollback-ambiguity probe | PASS — quarantine preserved and branch blocked |
| Fresh malformed created-parent record probe | **FAIL — unsafe unrelated cleanup and false `restored` state reproduced** |

The unavailable historical Conda interpreter was not represented as exactly replayed. Quick validation used `/opt/anaconda3/bin/python`, previously accepted for this gate; dependency-free validators and tests used default `python3`.

The green suites do not override the P1 finding because they lack a negative semantic binding test for `created_parent_records`.

## 8. Correction and resume conditions

Read-only runtime planning may resume only after:

1. The P1 created-parent logical/path/chain binding defect is corrected.
2. Focused RED/GREEN malformed, incomplete, and substituted-record tests pass and prove no unrelated path can be changed.
3. Both repositories’ quick/project validators and complete suites, the 84-test cross-CLI module, OpenSpec strict/all, negative searches, shared-byte checks, sensitive audit, and forward evidence are rerun fresh.
4. Complete no-Git source delta, bindings, durable summary, and source verification are regenerated.
5. A fresh independent Candidate Source High Re-review returns explicit `PASS`.

## 9. Final decision

**FAIL**

Role-first routing, concrete schema-6/schema-2 identity, current/legacy isolation, four-target manifest semantics, deterministic discovery, sensitive exclusions, public documentation, shared bytes, missing-parent creation, trusted-record cleanup rollback, and receipt-history blockers are otherwise coherent.

However, restore can accept semantically unbound created-parent evidence, remove unrelated directories, leave actual transaction-created directories behind, and still record success. This actionable P1 finding blocks promotion.

**Read-only four-target runtime planning may not begin.**
