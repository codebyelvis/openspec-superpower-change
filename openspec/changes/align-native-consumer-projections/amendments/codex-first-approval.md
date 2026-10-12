# Specific Approval: Codex-first Native Consumer Projections

Author: elvis. Date: 2026-10-12. Owner: `align-native-root`, product `codex`.

User instruction received verbatim: **：已批准 align-native-consumer-projections codex-first-draft-v1。范围仅账户 A AGENTS.md 和默认 Codex model_instructions.md，其余四文件延期**。

Approved amendment: `amendments/codex-first-draft-v1.md`, SHA-256
`8008f85aff9c2b8b0414fed3bd63c11755a116516153ec70d9a0d72b0bf4a6a9`.
Original six-row manifest remains
`662c5fc5547f610b5175dad81a8c0cd59f9eeebc0f03f15f7a361d9279a768f9`;
select only original rows **01 then 05**, with unchanged candidate bytes and 0644 modes.
Rows 02/03/04/06 are deferred unchanged assertions, never callable write rows.
Original draft-v2 approval, snapshots, six-file plan and package remain history;
they cannot supply a two-file transaction PASS.

This approval records scope and permits preparation and gated implementation.
Native writes still require fresh two-entry mechanism qualification and complete-package
independent Preflight. Do not request a second approval for an unchanged plan.
No settings/authentication/hooks/dependencies/binaries/publisher/Git/publication
authority is added.

## Clarified observations and preserved excluded state

The old design's account-A model-instructions assumption is superseded only
for the HOME-descendant cwd observed in the 2026-10-12 native evidence:
**both default Codex and account A consume row 05**. Both require fresh candidate
body and A–F/P1–P4 acceptance. This is not every cwd or IDE equivalence.
Preserve immutable historical bytes instead of rewriting their earlier facts.

Owner preserves current account-A config hash
`75d9a7d2e8df0ad543a043b0ff0e38e3c9c920a912f3d40ad6ac497535c540b3`,
mode 0600, device 16777231/inode 197774844. Earlier hash
`cc20886e5db221058fa903669b71f7bd00c7c11efda1f908d97bfb8692aec3b3`
remains unexplained drift evidence. Bind current excluded metadata in the new
package and independent Preflight; further drift stops execution. No config
copy, write, restore or guessed causal attribution is authorized.

The existing native-app notify boundary remains
`docs/review/2026-10-12-codex-native-callback-boundary.json`.
It permits declared ordinary harness startup/session state and existing completion
notification, with no all-host-read-only, callback-success or all-auth-files-unchanged
claim. Bind callback controls before actual runs. Current observer and actual parser
dependency must both be bound and verified; historical mechanisms cannot qualify
a changed observer retroactively.

## Execution isolation and review ownership

Use a fresh private root
`/Users/elvis/Library/Caches/native-agent-adaptation/project-codex-first-20261012/`
(0700, children 0600), outside native discovery, for exact commands, fixtures,
backups and temporary evidence. Source repositories receive only existing task,
plan and sanitized evidence documents; preserve their dirty/untracked work.
No Git/worktree/branch writes or source skill behavior changes are planned.

Preflight is a fresh `FULL_PREFLIGHT` lineage with eligible Codex product,
`independent-reviewer`, `control-plane-high`,
`governed-review-evidence`, instance `native-consumer-preflight-review`,
distinct from author/executor `align-native-root`.
Its purpose is whether native **two-file** implementation under the concrete
plan may proceed. Implementation and Final reviewers remain the two distinct
assignments below; none is already signed.

This is the approved current contract context for the same change-id and canonical
status, not another workflow ledger. Rebinding from the six-file context is backed
by the explicit user scope decision above; the special validator flag for a
reviewer-only self-evolution amendment does not apply to this scope approval.

## Resume Context

```json
{
  "change_id": "align-native-consumer-projections",
  "record_kind": "local",
  "mode": "approved-implementation",
  "approval_status": "approved",
  "risk_profile": "strict",
  "control_plane_owner": {
    "agent_product": "codex",
    "agent_instance_id": "align-native-root",
    "agent_role": "control-plane",
    "capability_profile": "control-plane-high"
  },
  "allowed_actions": {
    "wait": "none",
    "diagnose": "local-read",
    "verify": "local-read",
    "implement": "local-write"
  },
  "verification_commands": [
    "openspec validate align-native-consumer-projections --strict",
    "PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .",
    "PYTHONDONTWRITEBYTECODE=1 python3 /Users/elvis/Library/Caches/native-agent-adaptation/project-codex-first-20261012/fixture_tests.py"
  ],
  "reviewer_assignment": {
    "implementation-review": {
      "agent_product": "codex",
      "agent_instance_id": "native-consumer-implementation-review",
      "agent_role": "independent-reviewer",
      "capability_profile": "control-plane-high",
      "review_purpose": {
        "object": "align-native-consumer-projections implementation-review",
        "decision": "whether scoped implementation findings are closed before final verification"
      },
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
      "agent_product": "codex",
      "agent_instance_id": "native-consumer-final-review",
      "agent_role": "independent-reviewer",
      "capability_profile": "control-plane-high",
      "review_purpose": {
        "object": "align-native-consumer-projections final-review",
        "decision": "whether fresh scoped evidence supports owner completion"
      },
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
