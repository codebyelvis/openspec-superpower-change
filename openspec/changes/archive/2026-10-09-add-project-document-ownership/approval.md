# S8 draft-v1 Approval Record

Author: elvis. Date: 2026-10-08.

- Change-id: `add-project-document-ownership`; revision: draft-v1; level: Major.
- Decision: approved for scoped implementation.
- Provenance: the user explicitly sent
  `迭代优化skill：已批准 add-project-document-ownership` after the concrete
  proposal-only report and linked contract. The original proposal/design phase
  labels record the earlier draft state; this decision advances that phase.
- Scope: exactly the proposal/design/spec/tasks reviewed in the prior round.
  No scope, acceptance, protected-path or authority design has been rewritten.
- The fixed iteration command activates the existing single-round source/main
  closure under contract §3.2: required local four-target scoped sync and this
  repository's add/commit/current-branch push after validation and Review.
  No manifest/target edits, other repository Git, production, release,
  force-push, history rewriting or real-document migration authority.
- Controller/author/executor: bound Codex `/root`, contract-local identity
  `s8-control-01`, role `control-plane`, profile `control-plane-high`.
- Required reviews: Codex independent-reviewer/control-plane-high;
  Preflight `s8-preflight-01`, implementation `s8-review-01`, final `s8-final-01`.
  Tool IDs are recorded by each dispatched instance. Final is distinct from
  executor and Implementation Reviewer. All use gpt-6.1-sol/high.
- Review authority: `governed-review-evidence`; only the bound Router accepts
  evidence, advances gates, reconciles/archive and claims completion.

## Exact Approved Draft Bytes

| File within this change | SHA-256 at approval |
|---|---|
| proposal.md | a4e465222f68340006caae873e56194be50cc2d84f66d276df76f51ead921e9d |
| design.md | a4a1409f223a37b874d313c10cec4ff89cee2ce83bb1563b4eaeca1739c49d7a |
| tasks.md | d06fbfd095fe76b6485fdbf157b40211aeaa0c0a74edaa83aefcd1e2530e0354 |
| specs/skill-workflow-governance/spec.md | af075dc7bee1e39fd08c1c3913f599cbb01c9583669d44c2efd0cef917e8e56b |

Fresh structured source/runtime backup:
`/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/openspec-S8-implementation-68h7vzmq`.
Immutable approved-byte copies are retained there while implementation/rollback
is pending. Only task checklist progress may advance without scope reapproval.
Proposal backup remains available until applicable closure and cleanup.

## Blocked Resume Binding

The following existing-format metadata preserves the approved S8 facts and
primary Implementation assignment for a blocked checkpoint only. It does not
replace the required distinct Final assignment or permit execution/completion.
Preflight F1 has no compatible completion path under this unchanged format.
The prerequisite remains outside S8 and requires its own Major scope decision.

## Resume Context

```json
{
  "change_id": "add-project-document-ownership",
  "record_kind": "local",
  "mode": "self-evolution",
  "approval_status": "approved",
  "risk_profile": "strict",
  "control_plane_owner": {
    "agent_product": "codex",
    "agent_instance_id": "s8-control-01",
    "agent_role": "control-plane",
    "capability_profile": "control-plane-high"
  },
  "allowed_actions": {
    "wait": "none",
    "preflight": "local-read",
    "implement": "local-edit",
    "verify": "local-read",
    "review": "local-read",
    "sync": "local-runtime-sync",
    "commit-push": "source-git-lease"
  },
  "verification_commands": [
    "PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 /Users/elvis/.codex-account-a/skills/.system/skill-creator/scripts/quick_validate.py .",
    "PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .",
    "PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 scripts/validate_core_gates.py .",
    "PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v",
    "PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 -m unittest discover -s tests -v",
    "openspec validate add-project-document-ownership --strict"
  ],
  "reviewer_assignment": {
    "review_purpose": {
      "object": "S8 scoped implementation and its bound evidence",
      "decision": "decide pass, fail or blocked for the independent implementation gate"
    },
    "agent_product": "codex",
    "agent_instance_id": "s8-review-01",
    "agent_role": "independent-reviewer",
    "capability_profile": "control-plane-high",
    "independence_requirement": {
      "kind": "distinct-contract-instance",
      "distinct_from": [
        "control_plane_owner",
        "executor_assignment"
      ]
    },
    "result_authority": "governed-review-evidence"
  }
}
```
