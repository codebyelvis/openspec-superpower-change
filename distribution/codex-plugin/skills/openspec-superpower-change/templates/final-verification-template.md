# Final Verification Evidence: <change-id>

文档类型：Final Verification Evidence
日志及版本：YYYY-MM-DD v1

<!-- COOP_EVIDENCE_MANIFEST_START -->
```yaml
evidence_schema_version: 2
evidence_role: final-verification
evidence_result: pass
change_id: <change-id>
current_batch: <final batch>
attempt: <attempt>
contract_revision: <verified canonical revision>
canonical_sha256: <verified canonical SHA-256>
agent_product: codex
agent_instance_id: <canonical control-plane instance>
agent_role: control-plane
capability_profile: control-plane-high
```
<!-- COOP_EVIDENCE_MANIFEST_END -->

Set `evidence_result` to the actual lowercase result. The revision and SHA-256
identify the `awaiting-final-verification` canonical status that was verified.
After saving and hashing this file, do not edit its manifest or body.

## Commands And Results

| Command | Exit code | Result | Raw output path |
|---|---:|---|---|
| `<final_critical command>` | 0/non-zero | PASS/FAIL/BLOCKED | `<path>` |

## Scope And Assertions

- Final batch / attempt:
- Required acceptance layers:
- Key assertions and actual values:
- Diff/worktree fingerprint:

## Residual Risk

- <accepted risk, owner, or none>

## Result

PASS / FAIL / BLOCKED
