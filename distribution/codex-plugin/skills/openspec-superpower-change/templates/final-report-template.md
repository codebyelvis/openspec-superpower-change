# Final Report: <change-id or task>

文档类型：Final Closure Report
日志及版本：YYYY-MM-DD v1

## Conclusion

通过 / 有风险 / 需修改：<summary>

## Scope

- Changed files:
- Reviewed files:

## What changed

## Verification

| Command | Result |
|---|---|
| `<command>` | pass/fail |

- Final verification manifest: `<project-relative path>`
- SHA-256: `<64 lowercase hex>`

## Review

- Review profile: compact / standard / strict
- Review artifact or inline evidence:
- Result: PASS / FAIL / BLOCKED
- Fix/re-review rounds:
- Final Review artifact and SHA-256:

The final Review is a separate Review artifact carrying a schema-2
`final-review` manifest. Do not reuse the final-verification manifest or this
closure report as final Review evidence.

## Evidence

- <path:line or artifact reference>

## Residual risks

## Rollback

## OpenSpec closeout

- `tasks.md` reconciled: yes/no/not-applicable
- Archive state: archived / active with owner and resume condition / not-applicable
- Post-archive strict validation:

## Next steps

Completion is allowed only when final verification and Review both pass, their
required evidence is runtime-validated, and OpenSpec closeout is reconciled.
