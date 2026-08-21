# Candidate Source High Re-review — P1 R1

Verdict: **FAIL**

Decision scope: candidate source correctness for approved change `add-role-first-review-routing`. This verdict is implementation evidence only. It does not accept itself, update canonical state, authorize runtime changes, or claim completion.

**Read-only runtime planning may not begin.**

## Reviewer assignment and independence

- Product: `codex`
- Role: `independent-reviewer`
- Profile: `control-plane-high`
- Instance: fresh and distinct from authors, executors, the prior reviewer, and the decision-owning control plane
- Review mode: read-only
- Boundaries observed: no source edits, Git, Pi, runtime-destination inspection, runtime planning, canonical transition, archive, publication, or cleanup

## Input verification

All bound inputs retained identical start/end hashes and modes.

| Bound input | Mode | Start SHA-256 = End SHA-256 |
|---|---:|---|
| Plan | `0644` | `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229` |
| OpenSpec proposal | `0644` | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| OpenSpec design | `0644` | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| OpenSpec delta specification | `0644` | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| OpenSpec tasks | `0644` | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| Source verification | `0644` | `aaeb40bece860114b48327e6b67b5968c2832dfcb66c71ff6fd56ea7c13103d5` |
| Durable P1 source-delta summary | `0644` | `8c45a79406b09e5f7fafe0c5230c7ccac6ebcb2ca39dcbdbcb03c22a742f8adf` |
| Prior source Review | `0644` | `35050b3e8766b055f11d3a55018d4a34c1aca87893f574b477bbfe28a9cf6ef1` |
| Corrected sync validator | `0644` | `9f1cd9092cd0d98c18197437d7afc6911d63eda864eb5c4b73c391d67e759669` |
| Corrected sync tests | `0644` | `6b905e56fcb6d94eb01f4861b52ba9a063b2ad4c8a5e2191b6f924fcda6121f4` |
| Private source delta | `0600` | `c0e04d2c838f8694a0f78cd31263713119415225a13c71fcffd4c66df15b0f6d` |
| Private preflight bindings | `0600` | `a47a40f3878f7b34cb7fe73d36635e495b60c28b00eac57848ae2ba4f4293b71` |
| Private allowlist | `0600` | `5bcf0351ab9e0f5ef750b7d0034405ab215d3fb1156ac731df1026108fe7b2b3` |
| Private forward summary | `0600` | `1d32c75c564a4896c657ef8c7a1e79fb6c20d855e43be8c6aebd1e6c95cb408b` |
| Private comparison root | `0700` directory | No content hash applicable |

The intended rereview artifact remained absent; this reviewer did not write it.

## Complete-delta coverage

- Read the Router and Companion instructions, Skills, approved OpenSpec change, complete Plan, engineering invariants, closeout contract, all linked governance/synchronization contracts, source evidence, prior FAIL Review, and every changed/added record.
- Private delta result: `pass`.
- Actual records: `45` — Router `31`, Companion `14`.
- Exact allowlist entries: `49`.
- Unexpected paths: `[]`.
- `44/45` current records exactly matched the private after-state.
- The sole expected difference was Router source-verification: private-delta SHA `a2bd60…`, current bound SHA `aaeb40…`. This is the disclosed post-delta evidence append.
- The durable P1 delta summary and rereview input are also correctly classified as post-delta evidence-only records.
- Those evidence-only records do not repair or authorize candidate implementation behavior.

## Requirement and mechanism trace

| Area | Production mechanism | Verification result |
|---|---|---|
| Role-first routing and concrete assignment | Shared classification across Router Skill/routing/response surfaces and Companion Skill; schema requires product, role, profile, purpose, independence, authority, blocker owner, and resume condition. Four-product enum is stated at `references/agent-capability-routing.md:28`. | PASS in validators, unit coverage, and six bound forward cases. |
| Schema-6/schema-2 identity | Current evidence identity is defined at `references/handoff-contract.md:209`; historical schema-4/schema-1 isolation is explicit at `references/handoff-contract.md:215-216`. Companion templates declare schema 6 and schema-2 binding at their lines `3` and `16`. | Production contract PASS; public documentation has Finding P2-1. |
| Current/legacy isolation | Deployment drain and evidence transition rules at `references/approved-implementation-workflow.md:69-90`; legacy inventory is separate from current `--status` validation in `scripts/validate_core_gates.py:2371-2384` and `2501-2512`. | Mechanism PASS; public documentation conflict remains. |
| Four-target planning | Four target identifiers and canonical target set are bound at `scripts/validate_cross_cli_sync.py:27-30`; manifest, managed-file, discovery, sensitive-exclusion, and parity tests passed. | PASS. |
| Existing destination integrity | `capture_destination_prestate` at `scripts/validate_cross_cli_sync.py:489-501`; candidate creation at `571-587`; exchange verification and recovery at `590-665`. Tests at `tests/test_cross_cli_sync.py:528-554` and `1543-1581`. | Leaf-object correction works, but parent namespace identity is not bound; Finding P1-1. |
| Absent destination integrity | Exclusive creation at `scripts/validate_cross_cli_sync.py:685-713`; restore removal at `1343-1379`. Tests at `tests/test_cross_cli_sync.py:556-583` and `1583-1621`. | Leaf-object correction works, but parent namespace identity is not bound; Finding P1-1. |
| Final-leaf type/link changes and candidate-write failure | Displaced-object validation in `612-665`; exclusive create in `685-713`. Tests at `tests/test_cross_cli_sync.py:585-637`. | PASS for tested final-leaf cases. |
| Apply/restore recovery | Candidate installation at `scripts/validate_cross_cli_sync.py:1179-1198`; target-local restore at `1408-1459`; later-target isolation begins at `tests/test_cross_cli_sync.py:1623`. | Leaf-level ambiguous state stops safely, subject to Findings P1-1 and P1-2. |
| Receipt durability | Initial exclusive receipt at `scripts/validate_cross_cli_sync.py:936-949`; receipt advancement at `951-976`. | FAIL; Finding P1-2. |
| Shared bytes | Router/Companion Handoff files and shared validator core. | Byte comparisons and both identity tests PASS. |
| Public documentation | Router README lines `382-396`/Chinese `348-362`; Companion README lines `177-179`/Chinese `164-165`. | FAIL; Finding P2-1. |

## Concurrency and recovery invariant evaluation

The corrected leaf-level behavior was confirmed:

- An existing final file changed after its initial check is detected from the displaced object and restored when recovery is unambiguous.
- Concurrent creation of an initially absent final file is rejected by exclusive installation.
- Final-leaf link/type changes stop rather than being accepted as the reviewed file.
- Candidate-write failure does not remove a separately created destination.
- Existing-file and absent-file restore checks stop and mark recovery blocked on incompatible leaf state.
- Ambiguous exchange recovery retains a disposition path rather than reporting a verified restore.

Two broader invariants still fail:

1. Destination parent-directory identity is not retained through the mutation boundary. Temporary-directory safety checks for both existing and absent destinations completed successfully against a different parent namespace while leaving the originally reviewed parent unchanged.
2. Receipt advancement detects changed receipt bytes only after exchange, but its unconditional cleanup discards the displaced receipt and leaves the locally revised receipt live.

## Fresh verification results

| Command/check | Result |
|---|---|
| Six focused P1 integrity tests | `6/6`, PASS |
| `python3 -m unittest tests.test_cross_cli_sync` | `69` tests, `OK` |
| Router `quick_validate.py` using `/opt/anaconda3/bin/python` | `Skill is valid!` |
| Router `scripts/validate_core_gates.py` | PASS |
| Router full unittest discovery | `192` tests, `OK` |
| Companion `quick_validate.py` using `/opt/anaconda3/bin/python` | `Skill is valid!` |
| Companion `scripts/validate_templates.py` | PASS |
| Companion full unittest discovery | `86` tests, `OK` |
| `openspec validate add-role-first-review-routing --strict` | PASS |
| `openspec validate --all --strict --no-interactive` | `3 passed / 0 failed` |
| Both Plan Step-4 negative searches | Empty/PASS |
| Shared Handoff `cmp` | PASS |
| Shared Handoff and validator-core unit checks | `2/2`, PASS |
| Source-only sensitive audit | `0 sensitive categories found` |
| Bound forward evidence | Hash/mode valid; six records, all PASS |
| Complete source delta | `45` actual, `49` allowlisted, `unexpected_paths: []` |

The original isolated Conda interpreter remains unavailable as disclosed. The accepted `/opt/anaconda3/bin/python` replacement was used only for PyYAML-dependent quick validation; dependency-free validators and tests passed with default `python3`. This evidence drift is recorded and is not represented as an exact replay of the old environment.

Passing automated checks do not negate the findings below: the focused tests cover final-leaf changes, not parent namespace continuity or receipt-exchange preservation, and the negative searches do not reject stale schema-4/schema-1 public instructions.

## Findings

### P1-1 — Destination parent identity is not bound at mutation time

- Severity: **P1**
- Evidence:
  - `scripts/validate_cross_cli_sync.py:489-501`
  - `scripts/validate_cross_cli_sync.py:571-587`
  - `scripts/validate_cross_cli_sync.py:612-713`
  - `scripts/validate_cross_cli_sync.py:824-840`
  - `scripts/validate_cross_cli_sync.py:1179-1198`
  - `scripts/validate_cross_cli_sync.py:1343-1379`
- Problem: destination prestate records only the final file’s absence or content/mode. Candidate creation and namespace operations subsequently resolve path-string parents relative to the process working namespace. No verified parent-directory handle or ancestor identity is carried into the operation.
- Safety-check result: in temporary-directory checks covering an existing and an absent destination, the operation returned success in a different parent namespace while the originally reviewed parent remained unchanged.
- Impact: apply or restore can affect a location outside the reviewed destination tree and still report success. This violates containment, path/type-change stop conditions, and the requirement that only the reviewed destination state may change.
- Required correction:
  - Bind the destination root and complete parent chain, including no-link/type and directory identity.
  - Perform candidate creation and final namespace operations relative to verified, no-follow directory handles.
  - Revalidate containment and parent identity at the mutation boundary.
  - Treat any parent-chain change as `BLOCKED`, preserving all observed state.
  - Add focused existing/absent apply and restore tests for parent mapping and parent type changes.
  - Rerun the complete verification/delta workflow and obtain a fresh independent High Review.

### P1-2 — Receipt advancement does not preserve a concurrently changed receipt

- Severity: **P1**
- Evidence:
  - `scripts/validate_cross_cli_sync.py:951-976`
  - The current receipt is read at `953`.
  - Exchange occurs at `967`.
  - Displaced hash validation occurs at `969`.
  - Cleanup unconditionally removes the temporary entry at `975`.
- Problem: when the receipt changes between the initial read and exchange, the code detects the mismatch only after installing a revision based on stale input. Cleanup then removes the displaced, unreviewed receipt instead of restoring or preserving it.
- Safety-check result: the function raised the expected drift error, but the live receipt remained at the locally generated next revision, the separately changed receipt was not preserved, and no history or recovery temporary remained.
- Impact: durable transaction evidence can be lost while a misleading live state remains. Recovery and later-target eligibility can no longer be established from complete evidence.
- Required correction:
  - Apply mutation-boundary validation and recovery semantics to receipts as strictly as destination files.
  - On mismatch, restore the prior live state when unambiguous; otherwise preserve both states in mode-`0600` recovery evidence with an explicit manual-disposition marker.
  - Never remove a displaced receipt whose exact expected identity has not been established.
  - Add focused tests for receipt change during every state transition, history installation, recovery-blocked handling, and later-target exclusion.
  - Rerun full verification/delta and obtain a fresh independent High Review.

### P2-1 — Public documentation still describes the legacy evidence contract as current

- Severity: **P2**
- Evidence:
  - `README.md:382-396` says an actual schema-4 status should use current `--status` validation and that referenced artifacts use schema 1.
  - `README_cn.md:348-362` repeats the same guidance.
  - Companion `README.md:177-179` and `README_cn.md:164-165` state that Report/Review evidence uses schema 1.
  - These conflict with Router `README.md:17-18`, Companion `README.md:25-26`, and the schema-6/schema-2 production contract.
- Problem: current `--status` validation calls the current schema-6 contract validator; legacy schema-4/schema-5 records are handled by the separate legacy-inventory audit. The documentation can therefore direct users to an invalid command/contract combination and misstate current evidence fields.
- Impact: operators may reject valid current evidence, attempt to treat frozen legacy evidence as current, or produce schema-1 evidence for a schema-6 assignment.
- Required correction:
  - Update both Router and Companion English/Chinese documentation to describe current schema 6 with schema-2 evidence.
  - Describe schema-4/schema-5 only as frozen legacy audit/drain inputs using the actual legacy-inventory interface.
  - Add validator tests that reject conflicting current-schema statements in public documentation.

## Governance invariants

- Authority: this FAIL is governed implementation evidence only; only the original control plane may accept and act on it.
- Isolation: reviewer identity and instance separation satisfy the High Review requirement.
- PASS/FAIL/BLOCKED: actionable P1 and P2 findings require correction; they cannot be downgraded by otherwise passing tests.
- Completion: no source, runtime, OpenSpec, Handoff, archive, publication, or whole-change completion is claimed.
- Runtime: no runtime destination was inspected or changed, and no runtime plan was created.
- Git/Pi: neither was invoked.
- Source integrity: no file was created, modified, removed, or restored by this reviewer.

## Authorized next action

Return the candidate to correction for P1-1, P1-2, and P2-1. After correction, create fresh complete verification and source-delta evidence and dispatch a new independent Candidate source High Review.

**Read-only four-target runtime planning remains blocked.**
