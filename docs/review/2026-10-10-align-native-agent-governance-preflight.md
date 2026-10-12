# Native Agent Governance Preflight Review

Author: elvis. Date: 2026-10-10. Change: `align-native-agent-governance`, approved draft-v1.

Result: **PASS**. This is independent source-plan readiness evidence only. The bound control plane owns acceptance and all canonical transitions; implementation, runtime synchronization, Final Review and whole-task completion remain separate gates.

## Lineage and assignment

```json
{
  "review_mode": "FULL_PREFLIGHT",
  "attempt": 1,
  "lineage_root_revision": {
    "path": "docs/superpowers/plans/2026-10-10-align-native-agent-governance.md",
    "sha256": "8ec9d76241b3d25b1ce89e54bb0f094ac71dfe3a7c8d2ec0d71b94d18c8e5219"
  },
  "reviewed_revision": {
    "path": "docs/superpowers/plans/2026-10-10-align-native-agent-governance.md",
    "sha256": "8ec9d76241b3d25b1ce89e54bb0f094ac71dfe3a7c8d2ec0d71b94d18c8e5219"
  },
  "parent_review": null,
  "same_reviewer_instance": null,
  "author_identity": {
    "agent_product": "codex",
    "agent_instance_id": "align-native-root"
  },
  "executor_identity": {
    "agent_product": "codex",
    "agent_instance_id": "align-native-root"
  },
  "reviewer_identity": {
    "agent_product": "codex",
    "agent_instance_id": "align-native-preflight",
    "agent_role": "independent-reviewer",
    "capability_profile": "control-plane-high"
  },
  "review_purpose": {
    "object": "approved draft-v1 source implementation plan",
    "decision": "whether implementation under this concrete plan may proceed"
  },
  "independence_requirement": {
    "kind": "distinct-contract-instance",
    "distinct_from": ["author_identity", "executor_identity"]
  },
  "result_authority": "governed-review-evidence",
  "protected_boundaries": {
    "scope": "verified-approved-draft-v1",
    "contract_spec": "verified-hashes-match",
    "acceptance": "verified-plan-preserves-required-gates",
    "risk_evidence_profile": "strict-unchanged",
    "authority": "bound-control-plane-only",
    "assignments": "reviewer-distinct-from-author-executor",
    "allowed_forbidden_files": "verified-proposal-list-and-exclusions",
    "branch_worktree": "approved-isolated-filesystem-copy-no-Git-write",
    "database_production": "excluded",
    "Git_publication_deployment": "no-Git-publication-production-authority; reviewed-runtime-sync-later"
  },
  "declared_correction_set": [],
  "mechanical_self_check": {
    "result": "PASS",
    "current_plan_regular_non_symlink": true,
    "project_relative_path_binding": true,
    "whole_file_sha256_verified": true,
    "root_current_paths_identical": true,
    "root_current_sha256_identical": true,
    "reviewer_distinct_from_author_executor": true,
    "parent_identity_comparison": "not-applicable-full-root",
    "approval_contract_hashes_match": true
  },
  "finding_completeness": true,
  "blocking_findings": [],
  "non_blocking_recommendations": [],
  "accepted_residual_risks": [
    {
      "id": "R1",
      "evidence": "openspec/changes/align-native-agent-governance/design.md",
      "impact": "AGENTS consumption and portable parity do not qualify actual native entries or close the wider goal",
      "owner": "align-native-root",
      "decision": "retain exclusions and later exact-path adaptation plan"
    },
    {
      "id": "R2",
      "evidence": "openspec/changes/align-native-agent-governance/specs/skill-workflow-governance/spec.md",
      "impact": "Grok publisher compatibility may require separately supported hook isolation",
      "owner": "align-native-root",
      "decision": "no hook edits or product widening in this slice"
    },
    {
      "id": "R3",
      "evidence": "docs/superpowers/plans/2026-10-10-align-native-agent-governance.md",
      "impact": "implementation and runtime acceptance remain pending after source-plan readiness",
      "owner": "align-native-root",
      "decision": "execute all existing required gates before claiming acceptance"
    }
  ]
}
```

## Protected boundaries and completeness

All reasonably discoverable findings from the supplied contract, plan, current source and inspected evidence were consolidated in this full review. No actionable finding remains.

| Boundary | Independent check |
| --- | --- |
| Scope and contract/spec | Proposal, design, full spec delta, tasks, validation and approval read. Proposal/design/spec/tasks whole-file hashes match the approved validation record. Proposal's original proposed-status prose is historical; `approval.md` records the subsequent exact change-id approval. |
| Acceptance and risk | Major Self-Evolution, strict profile retained. Exact CCG-004 replacement and append-only CCG-014 clarification; CCG-001/002/010/016 preserved. Artifact-owned validation, RED/GREEN, seven bounded consumption cases and separate later reviews remain required. |
| Authority and assignments | Root author/executor `align-native-root`; reviewer `align-native-preflight` is a distinct Codex instance. Review evidence cannot authorize scope, products, transitions or completion. Advisory launchers cannot sign formal gates. |
| Allowed files | Exactly five proposal-listed references; two validators; two existing tests; new native case fixture and runner; engineering invariants; changelog; change-specific contract/plan/review/evidence artifacts. Eleven existing implementation files are byte-identical in source and isolated work copy; two planned implementation files are absent in both. |
| Forbidden files and effects | Companion, dirty main spec, other active changes and pre-existing untracked content preserved. No trigger/schema/product/manifest/dependency/distribution migration or immutable history rewrite. No account-A, Claude/Cursor/Grok native configuration, hook, dependency-link, credential, session or model replication. |
| Isolation and Git | Approved temporary filesystem copy retained; no worktree or Git mutation required. Source transfer later uses individual hash/absence guards. No staging, commit, reset, clean, push or publication authority. |
| Database/production/deployment | No business data or production path enters this slice. Runtime synchronization is gated later by a separate reviewed exact path/hash/prestate plan. |
| Runtime targets and native bytes | Manifest schema 1, managed version 6, 16 IDs and ordered `codex`, `pi`, `antigravity-cli`, `grok-cli` retained. Five references are declared portable, including the governance source; seven selected portable files plus the managed block fit the current manifest. Default Codex must be explicitly bound; exact destinations are reviewed before apply. Unselected closure is asserted; outside-block bytes and native hooks stay excluded. |
| Rollback and stop | Fresh structured prestates exist outside discovery. Source rollback restores only scoped bytes; runtime recovery uses receipts/backups and stops later targets on failure. Drift, failed evidence, excluded edits, actionable findings and protected-boundary changes stop the affected phase. |

The reviewer read `AGENTS.md`, `SKILL.md`, the Router-governed variant, relevant review/capability/evidence/self-evolution/sync rules, actual five references, the affected validator mechanisms, relevant tests, the portable manifest, the reusable native runner, and engineering/learning closeout rules. No source implementation or runtime write was performed by this reviewer.

## Fresh independent evidence

| Evidence | Observed result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .` | Exit 0, core gates valid. |
| Focused unittest suite through the real validators/transactions | Exit 0; 23 tests, no failures or skips. Included all `ScopedPlanSelectionTests`, `ScopedPlanTamperTests`, `ScopedTransactionTests`; `WorkflowRulesTest.test_schema6_reviewer_assignment_exact_shape_fails_closed`, `.test_schema6_standard_strict_and_compact_profiles_are_exact`, `.test_tiered_08_same_product_instances_cannot_self_review`; `DurableTargetTransactionTests.test_four_target_order_and_verify_all_require_verified_pi`. |
| `openspec validate align-native-agent-governance --strict` | Exit 0, change valid. |
| Fresh prestate comparison | 551 Router and 23 Companion inventoried regular files retain exact SHA-256 and mode. No symlink traversal was needed. Backup container is outside skill discovery; reviewer inspected metadata only. |
| Plan/approval/baseline path check | Regular files with no symlink in the leaf or parent chain. Whole-file plan hash above verified without newline normalization. |

Baseline evidence inspected at `docs/review/2026-10-10-align-native-agent-governance-baseline.json`: executor's 478-test dependency-free baseline, PyYAML quick validation and core gates passed. The reviewer independently reran the critical scope/identity/transaction checks above rather than representing the executor's full suite as a second independent run.

Both pre-change native probes are **baseline-complies**: compact-local returned inline readiness/no plan, and the native-default/bound-plan case returned before-execution/bound-plan. Each has four events, one agent message and zero tool events. No native behavior failure was reproduced. The approved design's RED gate requires real validator failures for the changed governance assumptions before production rule edits; it does not require forcing a healthy model to fail. The reviewer independently observed the current real managed-semantics validator accepting the old universal CCG-004 and absent advisory exception. New tests must turn those actual deterministic acceptance holes into observed RED, then GREEN and historical-mutation rejection. Native forward proof remains a separate required gate.

## Independent adversarial probe

The reviewer invoked actual current validator APIs using fresh in-memory mutations, without editing implementation or runtime files:

- Schema-6 reviewer product substitutions to `claude-code`, `cursor`, `claudex` and `claudeg` were each rejected. Canonical-authority substitutions and self-review protection were also exercised by the focused tests.
- Adding a fifth `codex-account-a` portable target was rejected by `validate_manifest`.
- Adding `references/hooks/publisher.json` as a portable file was rejected by `validate_manifest`.
- `parse_event_trace` accepted a bounded four-event, message-only completed trace and rejected an otherwise correct classifier accompanied by a command event, an unknown event or missing turn completion.
- Focused transaction tests independently exercised coherent managed-rule destination/prestate tampering, selector scope, unselected drift, selected-only writes, full-closure verification and ordered-target barriers.

These probes establish current fail-closed mechanisms, not implemented new semantics. Extending v6's exact owned CCG-004/014 checks must retain its existing CCG-001/002/010/016 bindings and legacy fixture bytes. The new consumer validator must validate each artifact separately and reject misowned/comment-hidden clauses and a contradictory compact-external waiver. The plan includes those checks; independent Implementation Review must inspect their actual implementation and rerun them.

The planned native runner is required to load hash-bound temporary project AGENTS text, retain existing CODEX_HOME only for authentication, use an empty private HOME, permit no tool events, and report finite classifier/audit/hash fields. Those bounds support only the observed instruction-consumption classifier. They cannot qualify another account, prove native Skill-body loading, another actual entry or runtime hook enforcement, or confer new control-plane authority. Runtime plan destinations and hooks remain governed by the existing transaction and separate adaptation boundary; classifier output grants no mutation authority. Actual implementation must be inspected at Implementation Review.

## Accepted residual risks and pending gates

- **Bounded native evidence:** Project AGENTS consumption is the deliberately limited proof. Actual native Skill-body loading and seven-entry acceptance remain unverified. Impact: portable parity and classifier PASS cannot close the wider goal. Owner: `align-native-root`; decision: retain these explicit exclusions and the later exact-path adaptation plan.
- **Grok publisher compatibility:** The contract records an inspected Claude-only hook compatibility risk, not a reproduced enforcement failure. Impact: native Grok behavior may still require later supported hook isolation. Owner: `align-native-root`; decision: no hook edits or product widening in this slice.
- **Pending implementation acceptance:** Source RED/GREEN, seven fresh native cases, required dual-parser quick/core/full tests, unchanged Companion validation, implementation review, reviewed runtime transaction, final verification and Final Review have not passed yet. Impact: this PASS provides readiness evidence only. Owner: `align-native-root`; resume conditions are the approved plan's existing gates.

No recommendation is used to hide an actionable finding; no failed or missing implementation evidence is promoted to PASS by this preflight.
