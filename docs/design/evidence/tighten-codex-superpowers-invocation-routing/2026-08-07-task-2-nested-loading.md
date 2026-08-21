# Task 2.1 nested-loading control evidence

**Change:** `tighten-codex-superpowers-invocation-routing`

The fresh controls used Codex CLI `0.147.0`, a private HOME, the pinned
`CODEX_HOME=/Users/elvis/.codex-account-a`, a new isolated project copied only
from the fixture root, `--ephemeral --ignore-user-config --ignore-rules`,
`--json`, `--sandbox read-only`, `--skip-git-repo-check`, and
`--output-last-message`. JSONL stdout was audited in memory and rejected any
tool, command, file, MCP, unknown, or invalid event. No raw stdout, stderr,
debug trace, command text, reasoning, message text, or prompt transcript was
persisted.

## Fixture binding

- Fixture source: `/private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/forward/nested-probe/project`.
- Child Skill SHA-256:
  `3186e023c68c87e4c58cf03dd58e08613ec9be500fde8ddd9a72815649502766`.
- Codex explicit-only metadata SHA-256:
  `a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94`.
- Router probe Skill SHA-256:
  `07c03729540f0d0592bc0ad184ff4a92a835f4bf440b4445a7a85dfcef8ebaff`.
- Fallback ban: shell/filesystem reads, copied child bodies, and user `$child`
  fallback were forbidden; only native Skill activation was accepted.

## Fresh result

Authoritative event-audited sanitized record:

`/private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/forward/nested-loading-pass-20260807.json`

- SHA-256: `b3c8582baf1d8c730ae0f74acb5d94c01ed8ab02dce7eeca1da177d1cbead232`.
- Mode: `0600`.
- Four subprocesses exited `0`.
- JSONL audit: 18 lifecycle/message events, 6 completed agent-message
  events, 0 reasoning events, and 0 tool/command/file events.
- `child_implicit`: child marker absent — PASS.
- `child_explicit`: exact `CHILD_NATIVE_MARKER_7F3A91` — PASS.
- `router_implicit`: Router and child markers absent — PASS.
- `router_explicit`: exact `CHILD_LOAD_BLOCKED` — PASS.
- Protected duplicate precheck: private HOME and account-a contained no
  Router, `using-superpowers`, or `superpowers:*` entry; the project contained
  only the two named probe fixtures.

The two earlier marker-only records predate JSONL event auditing and are
superseded; neither supports the fallback-ban claim. They are retained only as
temporary diagnostic history at
`/private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/forward/nested-probe-repro-20260807T164000+0800.json`
and
`/private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/forward/nested-probe-repro-20260807T164000+0800-validated.json`.
The event-audited record above is the sole authoritative result.
