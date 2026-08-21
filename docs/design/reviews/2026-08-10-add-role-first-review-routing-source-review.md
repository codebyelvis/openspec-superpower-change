# Add Role-First Review Routing — Candidate Source High Review

Verdict: FAIL

## 1. Decision scope

This Review covers only the Candidate source High Review gate for OpenSpec change `add-role-first-review-routing`. It decides whether Task 8 legacy drain and path/hash-only runtime-sync planning may begin.

It does not authorize runtime planning, runtime apply, Pi execution, synchronization, restore, canonical-state transition, OpenSpec archive, Git operations, publication, cleanup, or completion.

## 2. Reviewer identity and Assignment Contract

Reviewer identity: fresh independent Codex collaboration instance `/root/task7_source_high_review`.

- review_purpose: Review actual Router/Companion files, the complete no-Git reconstructed source delta, approved OpenSpec/Plan contract, validators/tests, fresh forward evidence, sensitive audit, and an independent adversarial routing chain; decide whether runtime planning may begin.
- reviewer_product: `codex`
- reviewer_role: `independent-reviewer`
- capability_profile: `control-plane-high`
- independence_requirement: fresh collaboration instance `/root/task7_source_high_review`, no inherited conversation turns, distinct from source authors/executors and bound control-plane; do not author/fix any reviewed artifact.
- result_authority: `governed implementation Review evidence only`; cannot mutate source/runtime/canonical state or authorize archive/Git/publication/completion. Only the original bound Codex control-plane may accept your evidence.

The Review was read-only. No reviewed artifact was authored or fixed. No Git command, Pi process, runtime plan/apply/restore/sync/discovery operation, credential read, native-state read, checkbox update, archive, cleanup, or canonical transition was performed.

## 3. Input verification

### Bound primary inputs

Every primary hash matched both at Review start and after all validation/probe work:

| Input | Expected SHA-256 | Start | End |
|---|---|---:|---:|
| Plan | `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` | PASS | PASS |
| Proposal | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` | PASS | PASS |
| Design | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` | PASS | PASS |
| Current Tasks | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` | PASS | PASS |
| Delta spec | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` | PASS | PASS |
| Source verification | `a2bd60a67c4fef9e7840ee1b12f75d6386def07218397dfb311755d92c8d8c56` | PASS | PASS |
| Durable source-delta summary | `55625e1b0c6a5832520e00975e61d1eeba758bd7c15e482a688dd8b4b41da57e` | PASS | PASS |
| Private authoritative source delta | `ffca933661288aab3df0f5d6f7476339bd7624353798442f8d9191982c8307d2` | PASS | PASS |
| Durable forward summary | `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` | PASS | PASS |
| Private forward summary | `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` | PASS | PASS |
| R9 Review | `f533c3b99029e88adc304aa7eb95b17cb8200a375154df1ec5b383c1e595a9c4` | PASS | PASS |

### Private evidence and recovery state

| Check | Result |
|---|---|
| R9 root is a real directory, mode `0700` | PASS |
| Recovery root is a real directory, mode `0700` | PASS |
| Private source delta is regular mode `0600` | PASS |
| Private forward summary is regular mode `0600` | PASS |
| `backup.pyc` regular mode `0600`, SHA `5b7cd72df71d308929c08fb6ae047403b4374e1824a13f479e5034f468dfff49` | PASS |
| `original-object.pyc` regular mode `0600`, same SHA | PASS |
| Source `scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc` remains absent | PASS |
| Target Review artifact absent at Review start | PASS |
| Target Review artifact absent at Review end | PASS |

### Complete no-Git delta boundary

- Private delta: `42` source-change records and `42` changed-path entries.
- Status counts: `36 modified`, `5 added`, `1 deleted`.
- Allowlist: regular mode `0600`, exactly `43` sorted path entries.
- `unexpected_paths=[]`.
- All `42/42` current after-states were rechecked at start and end.
- Every non-deleted path was a regular, non-symlink file with exact `after_mode` and `after_sha256`.
- The deleted cache remained absent.
- No candidate-source hash drift was found.
- `35/36` modified records have exact source-compare preimage bytes, and every available preimage SHA matches `before_sha256`.
- The remaining modified record, Router record 5, is the R9 input’s evidence-only pre-dispatch finalization. It is not a candidate implementation byte change. Its pre/post SHA transition is bound by the accepted R9 Review, while its current content and after hash were reviewed here.
- Candidate source therefore comprises 39 records: 35 compared modified files, three newly added forward-test files, and the deleted generated cache. Records 5–7 are separately classified as source-delta-after evidence-only writes.

### Evidence intentionally not obtained

Raw CLI/model traces, credentials, settings, sessions, history, native runtime contents, and Pi output were not read. The natural forward runner was not repeated. Only its bound, sanitized durable/private summaries were reviewed.

## 4. Reviewed scope and commands

The Review completely read both repositories’ `AGENTS.md` and `SKILL.md`, all specified OpenSpec/Plan/governance contracts, Router/Companion source files in the 42-record delta, source-compare preimages where available, validators, tests, forward fixtures/runner, public documentation, manifest, R9 evidence, and sanitized forward evidence.

No Git-based diff was used.

Fresh commands and results:

| Repository | Command | Result |
|---|---|---|
| Router | `/opt/anaconda3/bin/python /Users/elvis/.codex-account-a/skills/.system/skill-creator/scripts/quick_validate.py .` | PASS, `Skill is valid!` |
| Router | `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .` | PASS |
| Router | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | PASS, 186 tests |
| Router | `openspec validate add-role-first-review-routing --strict` | PASS |
| Router | `openspec validate --all --strict --no-interactive` | PASS, 3 passed / 0 failed |
| Companion | bound Conda `quick_validate.py .` | PASS |
| Companion | `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_templates.py .` | PASS |
| Companion | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | PASS, 86 tests |
| Router static search 1 | Exact Plan Task 6 Step 4 legacy/current negative pipeline | PASS, no unallowlisted output |
| Router static search 2 | Exact unresolved generic-reviewer negative pipeline | PASS, no unallowlisted output |
| Shared Handoff | Exact `cmp -s` | PASS |
| Shared bytes | Two specified byte-identity unit tests | PASS |
| Sensitive audit | Exact path-only audit command | PASS, final line `0 sensitive categories found` |

## 5. Architecture and behavior summary

The candidate implements four linked control surfaces:

1. Router and Companion classify Review by purpose and gate-bearing role before selecting a product. Eligible user-selected products are preserved; otherwise one concrete product is selected. Required unavailable independence is `BLOCKED`.
2. Current governed Handoff state is schema 6 with an exact, always-present, immutable seven-field `reviewer_assignment`, representing the six requested assignment concepts plus contract-local instance identity.
3. Schema-2 evidence manifests bind artifact role/result, product, instance, role, profile, source revision, batch, attempt, and canonical SHA. Only the bound Codex control-plane identity can provide final/control-plane evidence or accept transitions.
4. Four-target cross-CLI synchronization uses a path/hash-only plan, source and destination pre-state, private target-local backups, durable receipts, target ordering, verification, recovery, native-root exclusions, and sanitized Pi probing.

The first three surfaces are mechanically coherent across Router and Companion. The cross-CLI implementation has one release-blocking write-bound identity defect described below.

## 6. Findings

### P0

None.

### P1 — Destination identity is not bound at the namespace mutation boundary

Location:

- `scripts/validate_cross_cli_sync.py:1102-1109`
- `scripts/validate_cross_cli_sync.py:571-594`
- `scripts/validate_cross_cli_sync.py:1254-1263`
- `scripts/validate_cross_cli_sync.py:1297-1316`
- Related cleanup path: `scripts/validate_cross_cli_sync.py:614-630`

The apply path calls `assert_destination_prestate`, then later calls `atomic_replace`. `atomic_replace` rechecks only that the then-current target is a regular file and ultimately performs unconditional `os.replace(temporary, target)`. It does not prove that the namespace object displaced by `os.replace` is the object/hash that passed the reviewed pre-state check.

The restore path captures all admissible states first, then later performs unconditional `path.unlink()` or `atomic_replace()` based on those stale observations. External bytes introduced after the observation can therefore be deleted or overwritten.

Independent adversarial interleaving against the actual production functions produced:

```text
install-race-final=candidate
restore-race-final=absent
```

For apply, the probe inserted `external-drift` after `_install_candidate_entry`’s approved-state check and before `atomic_replace`; the candidate silently overwrote it. For restore-to-absence, the probe observed the candidate, introduced `external-drift`, then followed the production unlink branch; the external bytes were deleted.

This violates the reviewed destination-prestate and recovery guarantees in:

- `docs/engineering-invariants.md:115-122`
- `docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md:1842-1848`
- `docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md:1975-1980`

Existing tests do not close the gap:

- `tests/test_cross_cli_sync.py:497-516` covers drift that happens before the guard runs.
- `tests/test_cross_cli_sync.py:538-546` verifies same-directory replacement/mode/temp cleanup, not displaced-object identity.
- `tests/test_cross_cli_sync.py:1491-1506` proves receipt installation/swap ordering, not destination compare-and-swap behavior.
- Recovery tests cover already-present unknown digests and crash points, but not drift between admissibility capture and restore mutation.

Impact: runtime apply or recovery can overwrite/delete a destination state the reviewed plan did not authorize. Green suites can therefore false-PASS this integrity case.

Required correction:

- Bind and verify the actual displaced destination object at the write boundary for replacement and restore, with fail-closed recovery/manual disposition on mismatch.
- Close the absent-target exception-cleanup/unlink race as part of the same mechanism.
- Add production-path tests that inject existing-file, absent-file, symlink/type, and restore drift after the guard/admissibility observation but before namespace mutation.
- Repeat the complete source verification and fresh independent High Review.

### P2

None.

### Observation O1 — Evidence-only R9 input finalization has hash evidence but no extracted compare preimage

Record 5’s before SHA is `e4e44681…`, after SHA is `dcc8658b…`, and the transition is explicitly disclosed and accepted in the R9 Review. The source-compare tree does not contain that evidence-only pre-finalization content.

Non-blocking reason: the record is not part of the 39-record candidate implementation delta; its current bytes, exact after hash, purpose, and R9 provenance were reviewed. All 35 candidate modified files have exact preimage-byte comparisons.

Owner/decision: the bound control plane must continue treating records 5–7 as evidence-only history, not candidate source or runtime authority.

Release condition: any loss of the R9 binding, any further change to those evidence bytes, or any attempt to treat them as candidate implementation bytes requires a fresh evidence reconstruction and makes the next Review `BLOCKED`.

## 7. OpenSpec requirement/scenario and plan/task traceability

All 2 ADDED requirements, 4 MODIFIED requirements, and 39 scenarios are represented in the Plan traceability table and implementation/tests. One runtime-safety behavior remains failed.

| Requirement | Scenario coverage | Plan/tasks and mechanism | Result |
|---|---|---|---|
| ADDED: Explicit role-first reviewer assignment | generic request; blank purpose; user-selected Pi; same instance; advisory Review; unavailable reviewer | Plan Tasks 1, 3, 5; OpenSpec tasks 3.1–3.3, 4.2, 5.1–5.4; Router/Companion wording and six forward cases | PASS |
| ADDED: Schema-6 governed Reviewer Assignment Contract | standard/strict; compact; incomplete/extended shape; immutable transition; evidence bound to different purpose/assignment; old-shape current input; legacy audit not current authority | Plan Tasks 1–2 and 7; OpenSpec tasks 3.1–3.2, 4.1–4.2, 5.2–5.3; validator/evidence/transition tests | PASS |
| MODIFIED: Codex-primary auxiliary-agent collaboration | separated Review; unavailable second reviewer; self-review; unknown identity/owner; product-name authority; reviewer completion claim; correction loop; active legacy blocker | Plan Tasks 1–3, 7–11; OpenSpec tasks 3.1–5.4 and later drain/final gates | PASS for source routing/authority; later runtime/final gates intentionally pending |
| MODIFIED: Post-optimization cross-CLI synchronization gate | four required runtimes; Pi capability probe; unavailable target; explicit not-applicable; mislabeled failure; repository-only changes | Plan Task 4 and Tasks 8–9; manifest, planner, target-state validation, Pi probe, discovery and receipts | FAIL due P1 write-bound prestate defect |
| MODIFIED: Safe semantic global-rule alignment | native formats; stale v6 authority wording; portable parity; sensitive category; unsafe source/destination path | Plan Task 4, Task 6 checks, Tasks 8–9; managed markers, path validation, backup/restore, sensitive audit | FAIL due P1 apply/restore identity race |
| MODIFIED: Schema-5 product, instance, and role identity | active schema 5; Pi in schema 5; Pi in schema 4/1; complete old history; product substitution; schema-6 impersonation; no active old schema | Plan Tasks 1–2 and 8–9; isolated legacy validator/inventory and current-only CLI wiring | PASS for source implementation; Task 8 drain remains unstarted |

Task ledger trace:

- OpenSpec tasks 1.1–5.4 are implemented and covered.
- Tasks 6.1–6.3 remain correctly unchecked because the control plane has not accepted a source Review PASS.
- Task 6.4 is now required by this finding.
- Tasks 7.1 onward and Plan Tasks 8–11 remain unauthorized.

## 8. Source-delta file-by-file coverage

Every record below was read and checked against its responsibility, current type/mode/SHA, and applicable preimage/content evidence.

| Records | Repository/responsibility | Exact paths | Coverage result |
|---|---|---|---|
| 1–4 | Router public entry surfaces | `CHANGELOG.md`; `README.md`; `README_cn.md`; `SKILL.md` | 4/4 modified preimage diffs and after bindings PASS |
| 5–7 | R9 evidence-only history | R9 `inputs.md`; R9 review prompt; R9 Review | 3/3 current content/after bindings PASS; record 5 handled under O1 |
| 8–20 | Router governance and portable contract | `agent-capability-routing.md`; `approved-implementation-workflow.md`; `completion-contract.md`; portable manifest; `cross-cli-sync.md`; shared Handoff; `request-modes.md`; `response-patterns.md`; `self-evolution-rule.md`; `shared-global-governance.md`; `step-evidence-gate.md`; `superpowers-adapter.md`; `sync-checklist.md` | 13/13 modified preimage diffs and after bindings PASS |
| 21 | Generated cache | `scripts/__pycache__/validate_cross_cli_sync.cpython-314.pyc` | Deleted, absent, recovery bytes/modes/SHA PASS |
| 22–23 | Router production validators/runtime | `scripts/validate_core_gates.py`; `scripts/validate_cross_cli_sync.py` | 2/2 modified preimage diffs and after bindings PASS; record 23 contains P1 |
| 24–28 | Router fixtures/runner/tests | role-first cases; output schema; forward runner; cross-CLI tests; workflow tests | 5/5 content/bindings PASS; three added, two compared modified |
| 29–33 | Companion public/entry surfaces | `CHANGELOG.md`; `README.md`; `README_cn.md`; `SKILL.md`; `agents/openai.yaml` | 5/5 modified preimage diffs and after bindings PASS |
| 34–40 | Companion execution/review templates | dispatch; brief; handed-off execution; shared Handoff; report; review; timeout audit | 7/7 modified preimage diffs and after bindings PASS |
| 41–42 | Companion validator/tests | `scripts/validate_templates.py`; `tests/test_workflow_rules.py` | 2/2 modified preimage diffs and after bindings PASS |

Totals: 42/42 records covered; 39 candidate-source records and three separately identified evidence-only records; zero unexpected paths.

Router and Companion Handoff contracts are byte-identical. The shared validator-core identity test also passes. No contract drift was found among Handoff/template/validator/agent YAML/README/CHANGELOG/manifest surfaces.

## 9. Schema 6, current-versus-legacy, and evidence-binding matrix

| Concern | Production mechanism | Test/probe evidence | Result |
|---|---|---|---|
| Exact always-present assignment | `validate_core_gates.py:652-690`, exact seven fields and structured purpose | `test_schema6_reviewer_assignment_exact_shape_fails_closed`, `tests/test_workflow_rules.py:2223-2267` | PASS |
| Four-product enum | `_validate_assignment`, `validate_core_gates.py:629-649`; schema-6 product set | all-four-products test and Pi evidence test | PASS |
| Standard/strict exact shape | `validate_core_gates.py:699-723` | profile mutations at `tests/test_workflow_rules.py:2269-2305` | PASS |
| Compact closed shape | `validate_core_gates.py:724-743` | compact cases at `tests/test_workflow_rules.py:2307-2340` | PASS |
| No medium/low Review profile | standard/strict accepts only `control-plane-high`, `validate_core_gates.py:699-706` | wrong `cohesive-medium` rejection at `tests/test_workflow_rules.py:2291-2305` | PASS |
| Full immutability | exact schema-6 readonly set at `validate_core_gates.py:907-915`; transition equality at `:1401-1406` | every nested assignment component mutated at `tests/test_workflow_rules.py:2429-2456` | PASS |
| Evidence identity tuple | `validate_core_gates.py:1256-1278` | Pi-to-Codex substitution through production evidence validation at `tests/test_workflow_rules.py:2458-2520` | PASS |
| Canonical source SHA | `validate_core_gates.py:1320-1341` | stale/reused evidence tests in both suites | PASS |
| Current schema only | `validate_handoff_contract`, `validate_core_gates.py:918-923`; CLI current path `:2513-2532` | `test_schema6_current_and_legacy_validation_are_isolated`, `tests/test_workflow_rules.py:2342-2369` | PASS |
| Frozen schema 4/5 | separate legacy validator `validate_core_gates.py:926-933`; inventory-only CLI branch `:2501-2512` | legacy non-authorizing inventory and Pi legacy rejection tests | PASS |
| Pi cannot back-authorize legacy | legacy product sets remain frozen | `tests/test_workflow_rules.py:2405-2427` | PASS |
| Complete transition | persisted final verification and immutable prior evidence at `validate_core_gates.py:1529-1542` | `tests/test_workflow_rules.py:2908-2930` | PASS |

## 10. Reviewer-routing and authority matrix

| Case | Required route | Mechanism/evidence | Result |
|---|---|---|---|
| Gate-bearing Review | `independent-reviewer`, `control-plane-high`, distinct instance, governed evidence | Router/Companion classification; six-case forward summary | PASS |
| Advisory Review | `advisory-reviewer`, `control-plane-high`, `advisory-input` | routing docs and forward cases | PASS |
| Eligible user-selected product | preserve selection | user-selected Pi forward case | PASS |
| Generic “another agent” | resolve one concrete eligible product | generic destination forward case and negative search | PASS |
| Same implementation instance | reject/block; do not self-review | assignment instance-set validation and forward case | PASS |
| Required reviewer unavailable | explicit `BLOCKED`, owner and resume condition | forward cases use owner `user`; runner validates nonblank resume | PASS |
| Product/model name as authority | reject | Codex control-plane product + role + profile + instance + contract checks | PASS |
| Standard/strict medium/low reviewer | reject | validator accepts only `control-plane-high` | PASS |
| Reviewer/executor PASS | evidence only; cannot self-authorize state/completion | transition/evidence validation | PASS |
| Canonical acceptance | only matching bound Codex control-plane instance/contract | shared governance and validator | PASS |

## 11. Cross-CLI, Pi, and runtime safety matrix

| Control | Production path | Result |
|---|---|---|
| Exact four-target enum/order | `validate_cross_cli_sync.py:25-81`, v6 manifest validation `:157-198` | PASS |
| Path/hash-only plan with roots/source/prestates | planning and validation `:2460-2604` | PASS |
| Closed target-local backups | candidate/backup construction `:915-1045` | PASS |
| Durable prepared/mutation-intent receipts | receipt installation and revision chain `:790-899`, apply `:1132-1163` | PASS |
| Destination guard at actual write | check then unconditional replace `:1102-1109`, `:571-594` | FAIL, P1 |
| Recover only reviewed target state | restore observation then unconditional unlink/replace `:1254-1338` | FAIL, P1 |
| Stop later targets | prior-target checks `:1079-1094`; recovery/verify-all `:1592-1688` | PASS |
| Verify-all same-plan closure | receipt plan SHA and content/discovery digests `:1664-1688` | PASS |
| Managed v6 semantics/body parity | exact managed bodies and marker tests | PASS |
| Portable closure and discovery | target records and deterministic/Grok discovery validators | PASS |
| Pi target roots and enum | Pi included in exact target order/manifest | PASS |
| Pi native-root denial and isolated process | `build_pi_probe`/`execute_pi_probe`, `:2182-2457` | PASS by code/tests; Pi was not run here |
| Sensitive exclusions/path-only diagnostics | manifest validation and exact path-only audit | PASS |
| Runtime plan/apply authorization | Task 7 PASS prerequisite | NOT AUTHORIZED |

## 12. Independent adversarial routing-chain results

### Chain 1 — Schema 5 or old assignment cannot enter current transition

Production chain:

1. Current CLI status and previous-status parsing call only `validate_handoff_contract` at `scripts/validate_core_gates.py:2513-2532`.
2. That function requires schema 6 at `:918-923`.
3. Current transitions select the current validator at `:1387-1406` and expose it through `validate_transition` at `:1545-1546`.
4. A schema-5 object or a schema-5 object relabeled as schema 6 is rejected before transition authority.

Evidence: `test_schema6_current_and_legacy_validation_are_isolated`, `tests/test_workflow_rules.py:2342-2369`, passed in both repository suites.

Result: PASS.

### Chain 2 — Reviewer product/instance/role/profile mismatch rejects evidence

Production chain:

1. Assignment identity shape and values are validated at `scripts/validate_core_gates.py:629-649`.
2. Batch-review evidence selects the canonical `reviewer_assignment` at `:1256-1263`.
3. Product, instance, role, and profile are compared as one exact tuple at `:1268-1278`.
4. Any single-field substitution fails the same tuple comparison.

Evidence: `test_schema6_pi_review_evidence_matches_assignment_without_promotion`, `tests/test_workflow_rules.py:2458-2520`, passed through the production evidence validator. Contract-level role/profile/instance mutations also pass through production rejection at `:2269-2305`.

Result: PASS.

### Chain 3 — Same-instance/self-review and product-name-only authority are rejected

Production chain:

1. Standard/strict requires owner, executor, and reviewer instance IDs to form a three-element set at `scripts/validate_core_gates.py:715-723`.
2. Reviewer role/profile are fixed to `independent-reviewer` / `control-plane-high` at `:699-706`.
3. Canonical owner must separately satisfy Codex product, control-plane role/profile, instance, and contract checks at `:879-888`.
4. Evidence still has to match the canonical role/profile/instance tuple at `:1268-1278`.

Evidence: current schema-6 same-instance, role, and profile cases at `tests/test_workflow_rules.py:2281-2305`; evidence substitution at `:2458-2520`; forward `same_pi_session` is blocked with an owner.

Result: PASS.

### Chain 4 — Executor/reviewer PASS cannot advance `complete`

Production chain:

1. Attempt reports bind the executor; batch Reviews bind the reviewer; final/control evidence binds the control-plane owner at `scripts/validate_core_gates.py:1256-1275`.
2. Transition evidence binds the previous canonical SHA, revision, batch, and attempt at `:1320-1341`.
3. `complete` requires the previous revision already contain persisted final-verification PASS at `:1535-1539`.
4. Final Review cannot replace attempt, batch-review, or verification evidence at `:1538-1542`.
5. A complete snapshot without a previous status is rejected at `:1342-1343`.

Evidence: `test_complete_contract_requires_review_and_final_verification`, `tests/test_workflow_rules.py:2018-2028`; `test_complete_requires_persisted_verification_and_all_artifacts`, `:2908-2930`; reused/mismatched completion evidence test at `:3189-3217`.

Result: PASS.

## 13. Validation, static, forward, and sensitive results

- Router validation: all required commands passed; 186 unit tests passed.
- Companion validation: all required commands passed; 86 unit tests passed.
- Strict OpenSpec change validation passed.
- Strict all-spec validation passed with exactly 3 passed / 0 failed.
- Both Task 6 Step 4 negative searches passed with no unallowlisted lines.
- Shared Handoff exact-byte comparison passed.
- Shared Handoff and validator-core identity tests passed.
- Path-only sensitive audit passed with exactly `0 sensitive categories found`.
- Durable/private forward summaries are byte-identical, contain six cases, and retain only sanitized case/result/routing fields.
- The natural forward model runner was not repeated, as required.
- No raw CLI/model/native trace was persisted or read.
- All primary and 42-record end hashes remained unchanged after validation.

The green validation result does not override P1: the current tests do not exercise drift after the destination guard but before namespace mutation.

## 14. Residual risks

- P1 leaves runtime apply and recovery capable of overwriting or deleting unreviewed concurrent destination state.
- Task 8 legacy inventory and runtime destination snapshots have not been performed; this is correct for the current stop boundary.
- The R9 private root and its evidence-only classification must remain available and unchanged for the next Review.
- Forward evidence is sanitized summary evidence, not a raw replay; freshness remains bound to its specified SHA.
- No claim is made about actual runtime target state, because runtime roots were not inspected in this gate.

## 15. Verdict rationale

The contract, routing, schema-6 identity/evidence model, legacy isolation, public documentation, cross-repository parity, forward evidence, and validation suites are otherwise coherent and fully bound.

However, P1 is an actual production behavior error in the runtime applicator and recovery path. It creates a false-PASS route where destination state can change after the approved check and still be overwritten or deleted. Any actionable P0/P1/P2 finding prohibits PASS. The Candidate source High Review therefore fails, and Task 8 may not begin.

## 16. Minimal correction and re-review set

1. Correct destination replacement, absent-target cleanup, and restore so that the actual namespace object displaced/deleted is proven to be the reviewed preimage or candidate state at the mutation boundary.
2. On identity mismatch, preserve evidence, enter a blocked/manual-disposition state, and stop all later targets.
3. Add production-path adversarial tests for post-check existing-file drift, absent-file creation, symlink/type substitution, and restore drift.
4. Regenerate the complete no-Git source delta and evidence bindings for the corrected candidate.
5. Rerun every Router/Companion validator/test, both strict OpenSpec commands, Task 6 Step 4 checks, sensitive audit, forward evidence gate as prescribed by the refreshed plan, and the independent adversarial chains.
6. Obtain a fresh full independent Candidate source High Review.

## 17. Authorized next action

Return this complete Review text to the original bound Codex control-plane. The control-plane may treat it only as governed implementation Review evidence of `FAIL`.

It may authorize and execute only the minimal source correction/evidence-refresh loop above, followed by a fresh full independent Review. Task 8 legacy drain and runtime-sync planning must not begin.

Runtime apply, Pi, runtime discovery/sync/restore, canonical transition, OpenSpec archive, Git, publication, cleanup, and completion remain prohibited.
