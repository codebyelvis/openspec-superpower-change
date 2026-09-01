# Step Evidence Gate Reference

For schema 6 Review routing, carry all six concepts without abbreviation:
Review purpose, reviewer product, role, capability, independence, and authority.
The normative assignment and product/instance boundary live in
`references/agent-capability-routing.md`; this reference does not create a
second authority.

Use this reference when the main skill requires the full 12-part output template
for a high-risk, multi-step, or contract-changing implementation step.

Full evidence requirements do not always require verbose output. Report compactly
when all evidence is complete and the step is not high-risk, contract-changing,
or explicitly requested in full.

“Step” means a complete business slice or explicit risk milestone. It does not
mean every two-to-five-minute TDD checkbox. TDD owns RED/GREEN micro-steps;
this gate decides whether the slice may advance.


## Compact Gate Templates

Use these compact gates unless the full 12-part template is required by risk, contract impact, or user request.

Evidence profiles:

- `compact`: focused verification for low-risk direct, docs, formatting, config, or existing-behavior test work.
- `standard`: run `step_critical` for each batch; review reruns critical plus one independent behavior check; run `final_critical` once at the final batch unless later code changes invalidate it.
- `strict`: security, auth, public API/schema, persistence, migration, deployment, rollback, deletion/recovery, or cross-tenant work; real acceptance cannot be replaced by mocks or unit tests.

### Gate 0: Before action

- Mode:
- References read:
- OpenSpec decision:
- Required Superpowers sub-skills:
- Risk level:
- User confirmation required: yes/no
- Next action:

Gate 0 must happen before file modification, state-changing command, implementation, or proposal artifact creation.

### Gate 1: Before implementation

- Evidence gathered:
- Root cause candidate:
- Files allowed to change:
- Tests to add/run:
- Rollback path:
- Stop condition:

### Gate 2: Before slice signoff or whole-task handback

This gate records slice evidence only; the whole-task decision is deferred to
`references/completion-contract.md`.

- Changed files:
- Verification commands:
- Results:
- Residual risks:
- Out-of-scope changes checked:
- Review result and artifact/inline evidence:
- Whole-task decision: deferred to `references/completion-contract.md`

## Claim-to-Test Relevance Gate

Before executing tests, establish this mapping for each command:

```text
current change / acceptance claim
-> demonstrated blast radius
-> exact test command
```

A test enters the execution scope only when at least one of these is true:

- The current task changes the code, configuration, contract, or behavior that
  the test covers.
- The test directly verifies the current acceptance claim.
- The current Plan or Brief explicitly lists that exact command.
- Concrete evidence demonstrates that the current change may affect the test's
  covered scope.

None of these, by itself, authorizes a test: a file classified as `TEST`, a
shared business directory, a larger upstream diff, a Reviewer's suggestion to
"run something more complete," or a test name that merely looks related.

For a frozen baseline, accepted preimage, or historical upstream failure, when
the failure was not introduced by the current task, does not overturn the
current acceptance, does not invalidate the current evidence claim, and does
not affect the current slice's safety or evidence integrity, mark it
`OUT_OF_SCOPE_PREEXISTING_DEBT`. Record only the fact, impact, and owner; do not
fix it, expand the test scope, or block the current gate. An accepted upstream preimage is not upstream release validation; it does not approve or validate the entire upstream release.

An existing failure may block the current task only when the current change
introduced or amplified it, it directly violates the current acceptance, it
proves a Report/Plan/Brief pass claim false, or it breaks the current slice's
safety, evidence integrity, or runtime contract.

Keep environment evidence separate from assertion failures. Missing
dependencies, directory layout, credentials, network, or same-workspace
component problems are not automatically product regressions and do not by
themselves authorize broader tests or fixes.

When a Reviewer proposes a test not listed in the current Plan or Brief, first
state its corresponding acceptance, concrete call-chain or file relationship
to the current change, demonstrated blast radius, and why existing verification
is insufficient. If those points cannot be stated, do not execute the test.

### Generic counterexample

```text
某集成任务接受 frozen upstream revision 作为 preimage。
upstream diff 中包含多个历史测试文件。
Reviewer 发现其中一个与本次集成无关的既有断言失败。

错误处理：
因为文件分类为 TEST，就运行整个目录并阻断集成。

正确处理：
先检查该失败是否由本次集成引入、是否验证当前 acceptance、
是否推翻当前 evidence claim。
若均否，则登记 OUT_OF_SCOPE_PREEXISTING_DEBT，
不修复、不扩展测试、不阻断当前集成。
```

## Review Gate

- `compact`: focused diff/self-review may be recorded inline.
- `standard`: use a distinct review pass after implementation and slice
  verification.
- `strict`: use an independent review pass and all required real acceptance
  layers.
- External Handoff-backed Review is the batch review gate and must not be
  duplicated merely for ceremony.
- Every actionable finding, regardless of severity label, returns to the same
  scope for fix -> verification -> Review. A non-actionable observation is
  recorded separately as an accepted residual risk with an owner or decision.
- `BLOCKED` records owner and resume condition; after recovery, refresh evidence
  and Review the same scope again.
- No completion claim is allowed without Review PASS.
- External batch Review additionally requires runtime-validated hashed references
  for the attempt Report and batch Review. Final verification/final Review and
  the whole-task decision are governed by `references/completion-contract.md`.
  New schema-2 manifests bind product/instance/role/profile plus
  role/result/change/batch/attempt/source fingerprint, and `complete` validates
  against the actual previous status. Historical schema-4/schema-1 evidence is
  immutable. Standard/strict external execution rejects same-instance self-review;
  the bound Codex control-plane instance remains decision owner.
- High Review evidence includes actual diff inspection, production wiring trace,
  critical reruns, claim-to-mechanism support, and an independent adversarial or
  business-chain probe. Metadata labels alone cannot prove runtime behavior.

## Interrupted / Dirty Diff Audit

When the user interrupts due to process concerns, stop implementation and run a diff audit before continuing.

Audit output must include:

1. Files changed before interruption.
2. Which changes are validated, unvalidated, or partial.
3. Which changes should be reverted, kept, or parked.
4. Confirmation that no further implementation will happen until the user confirms.

Do not use the audit to justify continuing implementation without user confirmation.

## Full Output Template

1. Step goal
   - State the current task, boundary, risk, review entry point, and acceptance
     criteria.
2. Code fact table
   - Every fact must include `path:line` evidence.
   - Cover entry point, call chain, behavior location, test coverage, missing
     verification, docs/type/schema/spec contract location, and old error path
     or residual.
3. Positive check result
   - Identify existing correct capability, partial implementation, test
     foundation, and docs/type/schema/spec synchronization points.
4. Negative search result
   - Search for old fields, old API paths, old schema shapes, old docs examples,
     old test assertions, fallback or compatibility logic, deprecated aliases,
     old error messages, and outdated public claims.
   - For compact evidence on localized direct fixes, narrow this to residuals
     directly related to the defect, touched contract, affected field, path,
     error message, or changed behavior.
5. Root cause and gap analysis
   - Explain why the current state does not satisfy the step.
   - Locate the root cause layer: runtime, schema, API, frontend, docs, tests,
     spec, or contract mismatch.
   - Explain why existing tests did not block the issue when relevant.
6. Implementation strategy
   - State the minimal change needed.
   - Explain why the fix does not hide the root cause with `try`/`except`,
     fallback, or compatibility behavior unless the approved contract requires it.
7. Step change scope
   - List allowed files and actual files changed.
   - Record unrelated findings as residual risk unless they block this step.
8. Verification commands and tests
   - List official commands for tests, type checks, build, and
     `openspec validate <change-id> --strict` when applicable.
   - Mark host-machine ad hoc commands as supporting evidence only.
9. Verification result
   - State pass/fail for each command.
   - Include failures and warnings, and whether warnings affect the conclusion.
10. Self-review result
    - Answer whether the step had scope drift, fake contracts, test-only claims
      without runtime change, docs-only claims without runtime change, tests used
      as the only evidence, or inconsistency across code facts, tests, docs,
      types, and specs.
11. Residual risk
    - List unresolved issues that do not block the current step.
    - If a residual issue blocks the step, stop and fix it instead of signing off.
12. Next-step permission
    - Write `yes` only when all signoff conditions below are satisfied.
    - Otherwise write `no` and continue working on the current step.

## Signoff Conditions

Only allow the next step when all conditions hold:

- Code fact table was produced.
- Every fact has `path:line` evidence.
- Positive checks are complete.
- Negative searches are complete.
- Formal verification has run with the repository's required commands.
- Required Review has passed for the evidence profile.
- There are no out-of-scope edits.
- No fake contract was introduced.
- No old error path or outdated public claim remains in the step scope.
- The current step's acceptance criteria pass.

## Conditional Runtime/Test Rule

Use precise change-type rules:

- Runtime behavior change: runtime code and a regression test are required.
- API/schema/contract change: synchronize implementation, schema or type
  definitions, docs or specs, and tests that cover the contract.
- Docs-only, test-only, or proposal-only step: do not claim runtime behavior
  changed.
- Refactor-only step: new tests are optional only when existing behavior tests
  are run and are sufficient for the touched behavior.

## High-Risk Full Evidence Example: API/Schema Migration

Use this example when a change affects API compatibility, schema shape, persistence semantics, migration behavior, security, or operator-visible behavior. Do not collapse this into a compact report unless the user explicitly accepts the loss of detail and the change is no longer high risk.

### Scenario

A change renames a public API field from `token` to `accessToken`, migrates stored records, and keeps no compatibility alias unless the approved contract explicitly requires one.

### Full evidence example

1. **Step goal**
   - Goal: replace the public response field and persistence schema according to the approved spec.
   - Boundary: API serializer, schema/type definitions, migration, tests, and public docs for the affected endpoint only.
   - Risk: clients may break if old `token` output remains documented or if migration drops data.
   - Review entry point: `src/api/tokens.ts:42`, `src/db/migrations/20260623_rename_token.sql:1`.
   - Acceptance criteria: API returns `accessToken`, persisted data migrates without loss, no old public claim remains.

2. **Code fact table**

   | Fact | Evidence |
   |---|---|
   | Current API serializer emits old field | `src/api/tokens.ts:42` |
   | Public type still exposes old field | `src/types/token.ts:8` |
   | Existing migration framework applies ordered SQL files | `src/db/migrate.ts:31` |
   | Existing tests assert old field | `tests/api/tokens.test.ts:67` |
   | Public docs mention old field | `docs/api/tokens.md:24` |

3. **Positive check result**
   - Existing API tests cover token creation response.
   - Migration runner already has rollback test coverage.
   - Docs and types have clear synchronization points.

4. **Negative search result**
   - Search old field: `rg -n "\btoken\b" src tests docs openspec`.
   - Search compatibility aliases: `rg -n "accessToken.*token|token.*accessToken|legacy|compat" src tests docs`.
   - Search outdated docs examples: `rg -n "token:" docs examples`.
   - Result must explicitly list remaining matches and explain whether each is valid.

5. **Root cause and gap analysis**
   - Root cause layer: API/schema/docs contract mismatch.
   - Existing tests did not block the issue because they asserted the old contract.

6. **Implementation strategy**
   - Update serializer, types, migration, tests, docs, and spec references together.
   - Do not add fallback aliases unless the approved OpenSpec contract requires backward compatibility.

7. **Step change scope**
   - Allowed files: serializer, type definition, migration, endpoint tests, API docs, affected spec delta.
   - Actual files changed: list exact files.
   - Out-of-scope findings: record separately as residual risk.

8. **Verification commands and tests**

   ```bash
   openspec validate <change-id> --strict
   pnpm test tests/api/tokens.test.ts
   pnpm test tests/db/migrations.test.ts
   pnpm typecheck
   pnpm build
   ```

   Host-machine ad hoc commands are supporting evidence only, not formal verification.

9. **Verification result**
   - `openspec validate <change-id> --strict`: pass/fail with relevant output.
   - API test: pass/fail with relevant output.
   - Migration test: pass/fail with relevant output.
   - Typecheck/build: pass/fail with relevant output.
   - Warnings: state whether they affect the conclusion.

10. **Self-review result**
    - Scope drift: yes/no.
    - Fake contract introduced: yes/no.
    - Test-only claim without runtime change: yes/no.
    - Docs-only claim without runtime change: yes/no.
    - Tests used as only evidence: yes/no.
    - Code/tests/docs/types/spec consistency: pass/fail.

11. **Residual risk**
    - Example: external clients may still rely on old field; mitigation must be in approved migration/communication plan.
    - Blocking residuals must be fixed before signoff.

12. **Next-step permission**
    - `yes` only if all signoff conditions pass.
    - `no` if any old field, outdated public claim, missing migration verification, or failed formal command remains.
