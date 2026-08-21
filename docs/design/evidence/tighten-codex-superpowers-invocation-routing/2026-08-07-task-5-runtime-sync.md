# Task 5 runtime synchronization evidence

Date: 2026-08-07  
Change: `tighten-codex-superpowers-invocation-routing`

## Reviewed plan

- Plan: `/private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/runtime-sync-plan.json`
- Mode: `0600`
- SHA-256: `8ea18aa5aedb013bb9674e4cebc2e485497ae82904d76d5ad429156d273cf87a`
- Manifest SHA-256:
  `678467379a148aedc66ef164275f1e51c6ca546a5a6dcbf19fe03f07ac542e69`
- Managed-rule version/body: v5,
  `96158069ce5b7287e628d4f02b2d1f313a62f7cf9c50d9b6ebf068bf9829e537`
- The plan bound all 39 portable destinations and the global rule file for
  each target to exact pre-state hashes and modes. Four portable files differed
  from source on each target. The pre-state audit passed before apply.
- Active schema-4 status inventory was empty immediately before the first
  target apply.

## Per-target result

| Target | Apply | Verify | Backup objects | Final rule-file SHA-256 |
|---|---|---|---:|---|
| Codex | PASS | PASS | 40 | `8985a13981a72a300430ed56368af288526ef4d88e47a43b25e68bdc56be32f1` |
| Antigravity CLI | PASS | PASS | 40 | `17835ec162117680aeb700ec548b9bf4a05d8a1ae3427babfbe427242d079a4f` |
| Grok CLI | PASS | PASS | 40 | `d8cc710655ea2356b6b3a4bd7356950bfe9edc89cc18ce29c3e77e3029f5efe8` |

`verify-all` passed after the three sequential transactions. Router and Brief
quick/core/template validators passed for all three runtimes. Grok native
discovery passed and its mode-`0600` raw inspection file was consumed. The
paths-only sensitive audit reported zero categories.

## Live Codex Superpowers result

The reviewed delta remained exactly three paths and live bytes became identical
to staging:

```text
docs/README.codex.md: 37bd4b936d13b04815832b7aef41a68176d040e1ea38b91e3d1508c6a5893745
skills/using-superpowers/agents/openai.yaml: a1499d95abd8447558c535fe5554adcc3c9b988a0a39264a6283d430effe1e94
tests/codex/using-superpowers-invocation-policy.test.js: 52264db5788cd57017f440ce77ac70203ea283bb87280d814fca604dc0db2360
```

The shared `skills/using-superpowers/SKILL.md` remained unchanged at
`316e29381219adf0cac62190c67aeabf427d6e6e5f2735541d502b3d339be7aa`.
Live Node policy tests passed 2/2 and the finishing policy passed 1/1.

Two initial live body probes exposed classifier-format ambiguity. Each failed
transaction was immediately restored to the exact README hash and absent-file
pre-state before diagnosis. A focused Preflight accepted the final prompt
format constraint, and three isolated directory-symlink controls passed before
the final apply.

Authoritative live sanitized audit:

`/private/tmp/tighten-codex-superpowers-invocation-routing-20260807-c6xd9A/forward/live-policy-pass-20260807.json`

- SHA-256: `8648406d7d6037ad7e459b5a386ca0fe38458c8d8f9530731079b359c01fa867`
- Mode: `0600`
- Four fresh real-global-discovery sessions: PASS
- Event audit: 16 lifecycle/message events, 4 completed agent messages, and
  0 tool/command/file events
- `prompt_load`: `UNKNOWN`; the behavioral result is not a load-trace claim

No Git operation or publication action was performed.

## Learning audit decisions

- The no-tool false-PASS gap and destination-pre-state overwrite gap each met
  the high-severity promotion threshold. Candidate Cards, durable engineering
  invariants, and deterministic enforcement were added for focused Review.
- The archived-change duplication and live source/runtime symlink coupling were
  distinct, single implementation corrections already contained by the new
  change-id and staging/apply plan. They did not independently establish one
  further generalized invariant, so no additional durable artifact was added.
