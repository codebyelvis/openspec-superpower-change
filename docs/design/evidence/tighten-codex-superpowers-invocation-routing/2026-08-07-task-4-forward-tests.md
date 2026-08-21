# Task 4 isolated behavioral forward evidence

Date: 2026-08-07
Change: `tighten-codex-superpowers-invocation-routing`
Stage: Task 4, isolated behavioral forward tests

## Binding and source boundary

- Router source: `/Users/elvis/file/develop/opensource/openspec-superpower-change`
- Staged Superpowers source: `/private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/staging/superpowers`
- Authenticated Codex root: `/Users/elvis/.codex-account-a`
- Private probe HOME: `/private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/forward/staged-policy-probe/home`
- Probe project: `/private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/forward/staged-policy-probe/project`
- `prompt_load`: `UNKNOWN`; no supported native load trace was claimed.

Staged source hashes:

```text
docs/README.codex.md: 37bd4b936d13b04815832b7aef41a68176d040e1ea38b91e3d1508c6a5893745
skills/using-superpowers/SKILL.md: 316e29381219adf0cac62190c67aeabf427d6e6e5f2735541d502b3d339be7aa
skills/using-superpowers/agents/openai.yaml: a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94
tests/codex/using-superpowers-invocation-policy.test.js: 52264db5788cd57017f440ce77ac70203ea283bb87280d814fca604dc0db2360
```

## Required validation

Command: `node --test tests/codex/using-superpowers-invocation-policy.test.js`

- Exit: `0`
- Result: 2 tests passed.

Command: `node --test tests/finishing-branch-policy.test.js`

- Exit: `0`
- Result: 1 test passed.

Command: `python3 tests/run_superpowers_routing_forward_tests.py --router-source /Users/elvis/file/develop/opensource/openspec-superpower-change --managed-rule-source /Users/elvis/file/develop/opensource/openspec-superpower-change/references/shared-global-governance.md --superpowers-source /private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/staging/superpowers/skills --cases /Users/elvis/file/develop/opensource/openspec-superpower-change/tests/fixtures/superpowers-routing-cases.json --schema /Users/elvis/file/develop/opensource/openspec-superpower-change/tests/fixtures/superpowers-routing-output.schema.json --codex-home /Users/elvis/.codex-account-a --sanitized-summary /private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/forward/router-green-summary.json`

- Exit: `0`
- Output: `routing forward tests: 13 PASS, 0 FAIL`
- Sanitized summary SHA-256: `d530b28464873696a147c87d9256444f8d5ce5f9e70ba816d86f053fcd846cbc`
- Summary mode: `0600`
- Runner SHA-256: `52570f985fe4920aba5666e130dde43311cd72e1d1753fd5381513f24ea276e1`
- JSONL audit: 52 lifecycle/message events, 13 completed agent-message
  events, 0 reasoning events, and 0 tool/command/file events.
- All 13 fixture IDs passed exact route/result/authority/completion and canonical selected-method set checks.

The earlier summary SHA-256
`6b946d33d41350aae9e5e1b162d10f8c468c84e2f2bdd3a13e4d41be4acd670c`
predates JSONL event auditing and is superseded; it is not evidence for the
no-tool claim.

The earlier command with schema path `/private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/forward/openspec-superpower-routing-output.schema.json` exited `2` due to an input-path typo and produced no summary. It is recorded as an input error, not a behavior result.

## Fresh staged-policy probes

Each probe used a new `codex exec --json --ephemeral` session, pinned
`CODEX_HOME=/Users/elvis/.codex-account-a`, private HOME,
`--ignore-user-config --ignore-rules`, `--sandbox read-only`, and the isolated
project above. JSONL stdout was audited in memory using the same fail-closed
allowlist as the Router matrix. Only sanitized classifiers, hashes, and event
counts were retained.

| Probe | Exit | Sanitized result |
|---|---:|---|
| ordinary question | 0 | PASS; factual answer classifier matched; no observable meta-workflow |
| `$superpowers:using-superpowers` body probe | 0 | `questions_are_tasks=true`; `skill_type_priority=["process skills","implementation skills"]`; `skill_check_threshold_percent=1` |
| `$superpowers:systematic-debugging` body probe | 0 | `iron_law="NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"` |
| `$superpowers:test-driven-development` body probe | 0 | `first_rule="NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"`; `lifecycle="RED-GREEN-REFACTOR"` |

Authoritative sanitized audit:

`/private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/forward/staged-policy-pass-20260807.json`

- SHA-256: `7f2aaa27184d05d3605565b3877e0f032d1b4df8b52199dcfce5f29d589724ca`.
- Mode: `0600`.
- JSONL audit: 16 lifecycle/message events, 4 completed agent-message
  events, 0 reasoning events, and 0 tool/command/file events.
- The audit binds all four last-message hashes, copied-fixture hashes, schema
  hashes, staged-source hashes, classifiers, and Codex version.
- `prompt_load` remains `UNKNOWN`; behavioral PASS is not promoted into an
  unsupported load-absence claim.

## Diagnostic reconciliation

The 17:15 probe record was not accepted because its schema incorrectly required the legacy-snapshot field `instruction_priority`; the current bound implementation plan requires `skill_type_priority`. The staged Skill body and current plan both support the corrected three-field classifier. The corrected fresh using-superpowers probe passed with exit `0`.

The first direct systematic-debugging probe also exited `0` but used an underspecified classifier prompt and did not return the marker. A second fresh schema-constrained probe asked for the exact Iron Law code-block text and passed. This is a probe-classifier mismatch, not a source, subprocess, input, schema, or infrastructure failure.

Those individual pre-event-audit body-probe files are superseded and do not
support the no-tool claim. The earlier staged aggregate with SHA-256
`0d15c9ca4b18310b492ef23702c41d98396842a1ed8772e9b3e6a2dec08d8f7c`
reported `BLOCKED`; it was removed only after the authoritative PASS audit was
validated, as recorded in `forward-test-summary.json`.

## Gate result

Task 4 behavioral forward evidence is `PASS`: the current event-audited Router
matrix is green, staged metadata/body behavior is green with zero observed
tool events in isolated fresh sessions, direct child skills remain explicitly
callable, and no live Superpowers files were modified.
