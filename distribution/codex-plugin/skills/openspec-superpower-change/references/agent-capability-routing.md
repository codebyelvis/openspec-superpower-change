# Agent Capability Routing

Capability profiles are stable routing and authority ceilings. They are not
model names, vendor tiers, security identities, or evidence of approval.

## Profiles

| Profile | Suitable work | Authority ceiling |
|---|---|---|
| `control-plane-high` | architecture, OpenSpec, security, migration, ambiguous debugging, Preflight, evidence audit, independent probes, promotion, archive, completion | may propose and audit decisions; user-owned gates still require the user |
| `cohesive-medium` | approved cohesive multi-file implementation with closed architecture and authorization | may implement only the bound scope; cannot change OpenSpec scope, risk, acceptance, production authority, canonical promotion, or completion |
| `mechanical-low` | deterministic one-to-two-file edits, generation, focused tests, command execution, evidence collection | cannot design, broaden scope, decide security/production matters, or resolve ambiguity |

A profile recommends capability and limits authority; it never grants authority
because a concrete model happens to be powerful. Optional model metadata is
observational only and MUST NOT influence validation, routing, or approval.

## Non-authoritative runtime advice

| Work | Default suggestion |
|---|---|
| Ordinary OpenSpec revision, `writing-plans`, routine read-only Review | Codex, high |
| Cross-Track work, complex security boundary, difficult Plan Preflight, final gate-bearing Review | Codex, xhigh |
| Closed contract and clear-scope cohesive implementation | Luna Max, recommended reasoning strength chosen by the current runtime |
| Small mechanical modification | Current capable lower-cost model |

Model/reasoning metadata never changes `agent_product`, capability profile,
evidence, approval, authority, or PASS. Luna Max is advice only and never a
schema-6 `agent_product` value. If the current model is sufficient, no runtime advice is emitted. No block is required when no switch occurs.

An actual switch event is one approved execution-boundary transition in which the
effective model or reasoning target changes and the return target is known;
merely considering a model is not a switch event. “Once” is scoped to one
control-plane response/dispatch chain for that one approved transition. For one
switch event, the control plane authors one complete block once:

```text
运行环境建议：
- 目标 Session：
- 推荐模型：
- 推理强度：
- 切换原因：
- 可复制任务提示词：
- 完成后切回：
```

The block is optional and human-readable. It is emitted only for an actual
switch; when the current runtime is sufficient, omit it. An associated Brief or
dispatch may copy the existing block verbatim. The downstream surface must not regenerate or ask for a second notice. After compaction, a new window, an agent/model switch, or
“继续”, recovery copies an already-present non-canonical block when one is
available and otherwise emits none; it does not infer a new switch from chat
history. A later independent effective environment transition is a new event.
The block is never a capability assignment or approval and is not appended to
canonical `status.md`.

## Mandatory escalation

`mechanical-low` and `cohesive-medium` return `BLOCKED` without changing scope
when they encounter an unexpected failure, ambiguous contract, security field,
forbidden path, production credential, approval change, destructive action, or
open architecture decision. Medium also blocks on any proposed change to risk,
acceptance, production authority, canonical state, or final completion.

## Assignment rules

Schema 6 products are exactly `codex`, `pi`, `antigravity-cli`, and `grok-cli`.
All four are equally eligible for an assigned `executor` or
`independent-reviewer` role. Standard and strict work bind different executor
and reviewer instance IDs even when the product is the same; product equality
never permits self-review.

Only a bound `codex` product with role `control-plane` and profile
`control-plane-high`, plus the matching contract-local instance and canonical
contract, owns routing, evidence acceptance, canonical transitions, archive,
and completion decisions. Product or model name alone grants no authority.

Every Review request, recommendation, or instruction resolves six concepts:
Review purpose, reviewer product, role, capability, independence, and authority.
Apply an existing canonical assignment first; otherwise preserve a product
explicitly selected by the user; otherwise recommend one concrete eligible
product. If no eligible independent instance exists, return `BLOCKED`.

<!-- ROLE_FIRST_REVIEW_CLASSIFICATION_START -->
Use this exact classification before selecting a product:

- A Review that decides whether implementation, execution, runtime planning,
  promotion, archive, or completion may proceed is gate-bearing: use role
  `independent-reviewer`, profile `control-plane-high`, distinct-instance
  independence, and authority `governed-review-evidence`.
- A standalone Review that explicitly does not decide a gate is advisory:
  preserve any eligible user-selected product, use role `advisory-reviewer`,
  profile `control-plane-high`, advisory-not-gate-bearing independence, and
  authority `advisory-input`.
- `cohesive-medium` and `mechanical-low` are executor/evidence-collection
  profiles, not Review profiles.
- For standalone prompt or recommendation wording, a request to open or name a
  new distinct reviewer instance remains actionable after all six assignment
  concepts are resolved; do not infer unavailability merely because a concrete
  instance ID or open window is not yet supplied.
- Return `BLOCKED` only when the request explicitly says no eligible distinct
  instance exists or insists on reusing an implementation instance.
- When a required distinct reviewer instance is unavailable because the user
  must open or provide one, return `BLOCKED` with `blocker_owner: user` and a
  non-blank resume condition.
<!-- ROLE_FIRST_REVIEW_CLASSIFICATION_END -->
