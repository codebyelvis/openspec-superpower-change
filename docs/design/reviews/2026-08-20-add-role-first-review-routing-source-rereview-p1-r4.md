# Candidate Source High Re-review — P1 R4

Date: 2026-08-20  
Change: `add-role-first-review-routing`  
Review type: Candidate Source High re-review  
Verdict: `PASS`

## Reviewer assignment and authority

- Reviewer product: `codex`
- Reviewer role: `independent-reviewer`
- Capability profile: `control-plane-high`
- Independence: fresh no-history instance, distinct from the authors, executors, prior reviewers, and bound decision owner
- Purpose: decide whether the four-times-corrected candidate source satisfies the approved change and may proceed to read-only four-target runtime planning
- Result authority: governed implementation Review evidence only

This Review did not modify source or runtime files, inspect runtime destinations, create a runtime plan, run Git or Pi, update canonical state, accept its own result, or make a completion claim.

## Bound-input integrity

All primary inputs were checked at both the start and end boundaries. Every file remained a regular mode-`0644` file with the same bound SHA-256.

| Primary input | Start/end mode | Start/end SHA-256 |
|---|---:|---|
| `docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md` | `0644` | `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| `openspec/changes/add-role-first-review-routing/proposal.md` | `0644` | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| `openspec/changes/add-role-first-review-routing/design.md` | `0644` | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| `openspec/changes/add-role-first-review-routing/specs/skill-workflow-governance/spec.md` | `0644` | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| `openspec/changes/add-role-first-review-routing/tasks.md` | `0644` | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| `docs/design/evidence/add-role-first-review-routing/2026-08-10-source-verification.md` | `0644` | `bbcf2cc726876409aae30b7cac577a198e8341593c04b74f5f4084caeab84f95` |
| `docs/design/evidence/add-role-first-review-routing/2026-08-20-source-delta-p1-r4-summary.json` | `0644` | `6028f0c3b1d457b516226374fc942adc4e160ac8771d7eb72ce8827c27692127` |
| First source Review | `0644` | `35050b3e8766b055f11d3a55018d4a34c1aca87893f574b477bbfe28a9cf6ef1` |
| P1 R1 Review | `0644` | `44138637110b7643585d244721cf710f1f08a899dca874fd81df6ab1898d9719` |
| P1 R2 Review | `0644` | `5991be2198f4387bb0e860733352fb98e063e22bfcd694eacd3f4704932429b3` |
| P1 R3 Review | `0644` | `c451abf26592caa0630f8d3b2d272e740ddde40d959cccc79f5d672d4b379c47` |
| `scripts/validate_cross_cli_sync.py` | `0644` | `8d8a18a4c6d9a7639fe963e08c1a799b0c5a531129fd6195c8cd9fd8c4315f1e` |
| `tests/test_cross_cli_sync.py` | `0644` | `15f787aa7f0e23fd60611d3d0c5639b1541aba7b760fd88d93efe635f8a37aa3` |
| Router `tests/test_workflow_rules.py` | `0644` | `9e8f1d6904b0eb3e397eafb305f0e1743a77dcd9d9c715ac05e510f4e3aa2dc7` |
| Router `README.md` | `0644` | `44314b9c0f128ddcac90154ac5f36f167f70a66ab93aca61a4b46a86646f08ff` |
| Router `README_cn.md` | `0644` | `b973047e8092a9b7550ab62db5e795c6a7a0ba30e51304a2541953d4379fb987` |
| Companion `README.md` | `0644` | `f260de8c1e97ca5ce282e39c432278ebed4699745d0cd6c650dc82ece9ffe0b5` |
| Companion `README_cn.md` | `0644` | `d6180a9a0f54fc0d87934bd24efe320d5f9c7b45cb816292f86db5d1ba2b601c` |
| Companion `tests/test_workflow_rules.py` | `0644` | `65f8e4f2de06dfd050ef74310c94a84d76cec2b54c1955a1fdb66372d5f0b12c` |

The private reproduction inputs also retained their exact start/end bindings:

| Private input | Start/end mode | Start/end SHA-256 |
|---|---:|---|
| `source-delta-r4-retry1.json` | `0600` | `235a4a44eb344f6f0ea96137546c26d7b3d0a7b2f250bc3ab17e7ad1c43834ec` |
| `preflight-source-bindings-r4.json` | `0600` | `dc6034f8c151d53857b0d78e5417fbff2e5dd8d66e710a2ec6f9f731a20059ae` |
| `source-delta-allowlist-r4.txt` | `0600` | `c170a3530a13c7aee65ec28b2c64ff16d545fa804ef8569ed9cc3eda5f235ff5` |
| `role-first-forward-summary-r4.json` | `0600` | `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |
| Successful compare directory | `0700` | directory binding |
| Retained failed-attempt compare directory | `0700` | directory binding; empty |

Nested bindings were independently checked:

- Router source-preimage archive: mode `0600`, 22 entries, SHA-256 `ab5cc517ce385d8bbe06bea357c8b4b80b11353d06cabd5edf63ae5edfcddf1a`.
- Companion source-preimage archive: mode `0600`, 14 entries, SHA-256 `c3531d76d57ae446e29a66be460f613501ad1b01ac482d42ec3673825156f026`.
- Router preflight inventory: mode `0600`, 344 records, SHA-256 `9ce8e154ed62299f4ff83b2639b4378fc3d33d27e7c53d666221b0e5f6f0dd69`; its two declared exclusions matched.
- Companion preflight inventory: mode `0600`, 29 records, SHA-256 `e91bc13f3efcb1446de5452b97138cc5214ccb064488f151d159590ebc535844`; exclusions were empty.
- Router reconstructed source-start baseline: mode `0600`, 341 records, SHA-256 `7b5ffcaff49e6c08758f6fefd0fb1b64ce42fb44f85485f8dfec9f9508d81e3d`.
- Companion reconstructed source-start baseline: mode `0600`, 29 records, SHA-256 `dce42a6765431453e6d3962a90b248d3114a4b6a8d362688c9afa354da04bc46`.
- The successful compare directory contained 36 regular mode-`0600` reconstructed files. The failed compare directory remained empty, and its failed-attempt output remained absent.

The governed `cpython-314` cache path and the intended P1 R4 Review path were absent at the end boundary. The historical `cpython-311` cache remained present and unchanged during this Review.

## Complete source-delta coverage

The complete Router and Companion changed-record set, governance contracts, evidence history, prior Reviews, production mechanisms, tests, fixtures, templates, and public documentation were inspected.

The bound private delta reports:

- 54 actual paths: 40 Router and 14 Companion;
- 58 exact allowlist entries;
- no unexpected path.

A fresh independent no-Git reconstruction against the same source-start baselines returned:

- `source_delta: pass`;
- 56 actual paths: 42 Router and 14 Companion;
- no unexpected path;
- output mode `0600`, SHA-256 `49bde5be1e5b703bb0c4287d72e4c751046d0340fda8228d68a24ee25a0a5c17`;
- isolated compare root mode `0700`.

The 56-path result is consistent with the bound 54-path delta. The later durable summary and P1 R4 input add two Router paths; the source-verification append changes bytes on a path already counted by the original delta. The two non-actual allowlist entries are unchanged `CONTEXT.md` and the still-absent intended P1 R4 Review artifact. These are evidence-only classifications, not candidate implementation bytes.

The first R4 delta invocation is correctly classified as a separate reviewer-input error: it supplied preflight inventories where source-start inventories were required, stopped with an inventory-shape error, created only the empty retained compare directory, and wrote no result. The successful retry used new output and compare paths. No product defect or same-transaction continuation is inferred.

## Requirement-to-mechanism-to-test trace

| Requirement | Production mechanism | Independent or regression evidence |
|---|---|---|
| Role-first routing and concrete product preservation | Shared exact classification blocks in `SKILL.md:96-118`, `references/agent-capability-routing.md:41-67`, `references/response-patterns.md:15-46`, and Companion `SKILL.md:81-111` | Router tests `tests/test_workflow_rules.py:2092-2207`, forward-runner tests `:3829-3972`, Companion tests `:638-735`; fresh six-case forward run passed |
| Exact schema-6 reviewer assignment | Exact assignment shape, purpose, authority, product/profile, and independence validation in `scripts/validate_core_gates.py:637-740` and byte-identical Companion core | Router tests `:2223-2495`; Companion tests `:749-1022`; all four reviewer products and current/legacy separation passed |
| Schema-2 evidence identity | Exact evidence fields and assignment matching in `scripts/validate_core_gates.py:1133-1279` | Router tests `:2472`, `:2553`, `:3233`; corresponding Companion cases passed |
| Deterministic created-parent plan | Manifest-order hierarchy validation and deterministic de-duplication in `scripts/validate_cross_cli_sync.py:2048-2069` | Independent production-function check confirmed order, de-duplication, and malformed-hierarchy rejection |
| Receipt-state exactness | Empty `prepared`, exact prefix `mutation-intent`, and exact full later state in `scripts/validate_cross_cli_sync.py:2072-2085`; present unrecorded paths rejected at `:2104-2112` | Independent checks passed for all three states, forbidden records, present unrecorded state, and missing/full state |
| Logical/path/chain semantic binding | Logical path must be a directory, resolve to recorded path, and reproduce the complete chain in `scripts/validate_cross_cli_sync.py:2086-2103` | Independent substitution, truncated provenance, hierarchy, and identity checks passed; regression tests `tests/test_cross_cli_sync.py:2024-2193` passed |
| Evidence durable before leaf installation | Descriptor-relative parent creation and chain capture at `scripts/validate_cross_cli_sync.py:693-765`; receipt persistence before leaf creation at `:1797-1823` and `:1875-1900` | Tests `tests/test_cross_cli_sync.py:1850-2023` and real crash-point recovery passed |
| Reject before restore mutation | `_bound_created_parent_records` is called before closure inspection or mutation in `_restore_target_locked`, `scripts/validate_cross_cli_sync.py:2216-2271` | Reorder, truncation, missing/extra, valid-chain substitution, mapping/link/type, and unchanged-leaf regression cases passed |
| Exact created-directory cleanup | Descriptor-bound reverse-depth quarantine, identity recheck, empty-object removal, and root-absence proof at `scripts/validate_cross_cli_sync.py:2116-2189` | Exact cleanup, replacement preservation, and non-empty preservation tests `tests/test_cross_cli_sync.py:2241-2344` passed |
| Durable blocked state and later-gate exclusion | Recovery-blocked transition in the restore path; prior-target gate `scripts/validate_cross_cli_sync.py:1769-1789`; recovery gate `:2542-2611`; all-target gate `:2614-2638` | Substitution, post-history ambiguity, target-local isolation, and later-target regression cases passed |
| Four-target order and discovery | Canonical order and versioned manifest enforcement in `scripts/validate_cross_cli_sync.py:27-30`, `:176-201`, `:404-459`; deterministic discovery and receipt verification in the later target functions | Manifest/order test `tests/test_cross_cli_sync.py:1268`; four-target test `:1525`; discovery tests `:896-923`; full suite passed |
| Complete source-delta boundary | Complete no-Git inventory at `scripts/validate_cross_cli_sync.py:2645-2735`; bound allowlist/archive/baseline comparison at `:2900-3055` | Bound 54-path delta and fresh independent 56-path post-evidence reconstruction both passed |

## Correction-history integrity analysis

1. The first correction established destination pre-state and final-leaf mutation-boundary checks. Those mechanisms remain active and their concurrency and rollback branches pass.

2. P1 R1 added existing-parent identity binding, direct receipt-history recovery, and corrected current public contracts. The current implementation retains full directory-chain guards and atomic receipt transitions; schema-6 public and validator surfaces agree.

3. P1 R2 identified initially absent parent creation, exact directory cleanup, and post-history ambiguity. The next correction moved creation under verified ancestor descriptors, persisted created-parent records before leaf installation, replaced path-only cleanup with identity-bound quarantine, and made ambiguous history state block every later gate. The focused and full suites exercise successful rollback, ambiguous rollback, exact cleanup, retained non-empty state, recovery, and later-target exclusion.

4. P1 R3 correctly found that a planned logical path could still be paired with an independently valid different path and chain. P1 R4 closes that gap before restore mutation by deriving one ordered plan from the bound manifest, requiring the receipt’s logical paths to equal the state-specific plan sequence, resolving each logical path, comparing it to the recorded path, and recapturing the complete chain.

The independent temporary production-function matrix passed 14 checks covering:

- empty prepared state;
- exact mutation-intent prefix;
- exact applied full state;
- forbidden prepared records;
- present unrecorded planned state;
- missing, extra, and reordered records;
- logical/resolved-path/chain substitution;
- truncated root provenance;
- identity mismatch;
- malformed hierarchy;
- deterministic de-duplication;
- preservation of non-empty unrelated state.

Fourteen focused end-to-end production integration tests also passed, including mapping/link/type changes, complete durable records, substitution, order, provenance, hierarchy, identity, missing/extra records, empty and non-empty replacement state, real crash recovery, durable later-gate exclusion, and target-local failure isolation.

The validation order ensures malformed or substituted parent evidence is rejected before target content changes. Rejection retains actual and unrelated state, advances the pending receipt to `recovery-blocked` when the receipt transition remains available, and prevents recovery or later-target progress. Exact proven state still restores successfully and removes only the directories created by that transaction.

## Fresh verification

| Verification | Fresh result |
|---|---|
| Router quick validator using `/opt/anaconda3/bin/python` | PASS |
| Router project validator | `Core gates valid` |
| Cross-CLI module | 89 tests, OK |
| Router full suite | 213 tests, OK |
| Companion quick validator using `/opt/anaconda3/bin/python` | PASS |
| Companion project validator | PASS |
| Companion full suite | 87 tests, OK |
| OpenSpec change strict validation | PASS |
| OpenSpec all strict validation | 3 passed, 0 failed |
| Both exact policy searches | Empty |
| Shared Handoff byte comparison | PASS |
| Shared validator-core byte test | PASS |
| Path-only excluded-category audit | 0 categories found |
| Fresh no-Git source reconstruction | 56 actual, 58 allowlisted, no unexpected path |
| Independent production-function matrix | 14 checks, PASS |
| Focused production integration set | 14 tests, OK |
| Fresh isolated role-routing probe | 6/6 rows PASS |

The fresh routing summary is mode `0600`, SHA-256 `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b`, identical to the bound summary. Its raw per-case temporary directories were removed by the runner.

The original isolated Conda interpreter remains unavailable. The quick validators used the previously accepted `/opt/anaconda3/bin/python`; this Review does not represent that as an exact replay of the missing environment. Dependency-free validators and tests used the default `python3`.

One initial reviewer-only end-boundary helper stopped before performing file comparisons because a shell-reserved local variable altered command lookup. The corrected read-only helper was rerun immediately and every binding passed. No candidate or runtime file changed.

## Findings

No P0, P1, or P2 finding was identified.

There is no candidate correction or re-review resume condition. The remaining workflow condition is control-plane acceptance and persistence of this evidence; this reviewer cannot perform that acceptance.

## Final verdict

`PASS`

The corrected candidate source satisfies the approved change and closes the P1 R3 semantic created-parent binding gap without regressing the previously corrected branches.

Read-only four-target runtime planning may begin after the original bound control plane accepts and persists this `PASS`. This Review does not itself start runtime planning and does not authorize runtime mutation, promotion, archive, publication, or completion.
