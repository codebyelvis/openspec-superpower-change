# S8 Approved Stage-Specific Resume Context

Author: elvis. This immutable metadata sidecar is the sole S8 binding amendment
authorized by support-stage-specific-resume-review; original S8 approval, scope,
acceptance and readiness history remain unchanged.

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
    "implementation-review": {
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
    },
    "final-review": {
      "review_purpose": {
        "object": "S8 final verification and closure",
        "decision": "decide pass, fail or blocked for the independent final gate"
      },
      "agent_product": "codex",
      "agent_instance_id": "s8-final-01",
      "agent_role": "independent-reviewer",
      "capability_profile": "control-plane-high",
      "independence_requirement": {
        "kind": "distinct-contract-instance",
        "distinct_from": [
          "control_plane_owner",
          "executor_assignment",
          "implementation_reviewer"
        ]
      },
      "result_authority": "governed-review-evidence"
    }
  }
}
```
