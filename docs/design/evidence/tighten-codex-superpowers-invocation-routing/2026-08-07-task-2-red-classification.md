# Task 2 RED classification evidence

**Change:** `tighten-codex-superpowers-invocation-routing`

**Control-plane result:** Task 2.1–2.4 evidence gate satisfied. The existing
`add-codex-skill-update` change and its evidence are outside this record and
were not read for mutation, changed, or cleaned.

## Valid RED

Command:

```text
python3 tests/run_superpowers_routing_forward_tests.py --router-source /private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/baseline/openspec-superpower-change --managed-rule-source /private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/baseline/openspec-superpower-change/references/shared-global-governance.md --superpowers-source /private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/staging/superpowers/skills --cases tests/fixtures/superpowers-routing-cases.json --schema tests/fixtures/superpowers-routing-output.schema.json --codex-home /Users/elvis/.codex-account-a --sanitized-summary /private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/forward/router-red-repro-20260807T163000+0800.json
```

- Exit code: `1`.
- Sanitized summary: `/private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/forward/router-red-repro-20260807T163000+0800.json`.
- Summary SHA-256: `cc38d47349c23a0691f70e6d6481826888d97de429610944dabcbe1f38902584`.
- Summary mode: `0600`.
- Matrix: `13` cases; `4` behavior PASS; `9` behavior FAIL.
- Every failed case contained a valid six-field observed classifier. All nine
  failures were classifier mismatches: `diagnose_only`, `proposal_only`,
  `material_ambiguity`, `direct_change`, `ordinary_review`,
  `high_risk_implementation`, `explicit_method_no_git`, `missing_router`, and
  `cyclic_phase`.
- No failed case was an input, schema, subprocess, timeout, transport, or
  infrastructure failure.
- The runner's read-only mutation guard passed for every completed case; no
  `read-only probe mutated project files` result occurred.
- Independent audit result: `VALID_RED`, with `mutation_guard=PASS`, summary
  mode `0600`, and no non-behavior failure category.

## Invalid current-suite diagnostic retained separately

The first current-source reproduction remains evidence of why subprocess
failures cannot be promoted to behavior RED:

- `/private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/forward/router-current-repro-20260807T160000+0800.json`,
  SHA-256 `2fdddc2aff6c35c90dfb8c436aac737ca8b12d2f63b661ea39b853db679434cb`.
- Outer exit code: `1`; `5` PASS, `7` subprocess timeouts, `1` classifier
  mismatch (`duplicate_router`).
- This result is explicitly **not** valid RED. Single-case and five-worker
  isolated replays passed the timeout cases, confirming the timeout category
  is not a stable behavior assertion.

## Root cause and TDD repair

The stable classifier mismatch was `duplicate_router`: route/result/authority
fields were correct, but the model omitted the explicitly requested
`superpowers:test-driven-development` from `selected_superpowers` after the
duplicate Router correctly blocked the route. The approved Route Decision
Record says this field records explicitly requested methods even when authority
blocks them.

The focused regression was first run before the repair:

- Command: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_workflow_rules.WorkflowRulesTest.test_superpowers_method_routing_is_exact_and_fail_closed -v`
- Exit code: `1`.
- Failure: runner prompt lacked the explicit-method observability contract.

The minimal runner prompt contract was then added. Fresh verification:

- The same focused command: exit code `0`, `Ran 1 test`, `OK`.
- The isolated `duplicate_router` classifier then returned the exact expected
  six-field object with `selected_superpowers=["superpowers:test-driven-development"]`.
- The three Task 2 focused tests returned exit code `0`, `Ran 3 tests`, `OK`.

## Source bindings at the RED gate

- Current managed rule SHA-256: `96158069ce5b7287e628d4f02b2d1f313a62f7cf9c50d9b6ebf068bf9829e537`.
- Baseline managed rule SHA-256: `3cec896a53b16c1b2782343cb08301c62e38ac71c44cb45c82daa1ca8f054ac3`.
- Fixture SHA-256: `270cf3774ac3a50179d7deacf424d42f3bb3de51203002785d88d03c0e158081`.
- Canonical output schema SHA-256: `bd922eaa360a31778ed9de468b8fa94ead1eb3899b78dce901ae1dc98f4279ba`.
- Staged shared `using-superpowers/SKILL.md` SHA-256:
  `316e29381219adf0cac62190c67aeabf427d6e6e5f2735541d502b3d339be7aa`.
- Codex CLI: `codex-cli 0.147.0`.

No raw Codex stdout, stderr, debug trace, prompt transcript, credential,
session data, or account configuration is persisted here.
