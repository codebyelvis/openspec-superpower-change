# Design: verify anti-drift and round budget

Author: elvis

## Decision

Keep the numeric round budget in file A only. File B says `reaching the round budget` and does not hard-code 40 or 30. The two files land together or not at all. A skill-only edit would name a budget that has no approved number.

File B remains an English skill instruction. File A remains Chinese user-owned Codex text. The append goes after the last existing marker and outside `CROSS_CLI_GOVERNANCE_BEGIN/END`.

## Stage interaction

`VERIFY` produces the fact report and stops after remaining independent checks. It does not enter a fix slice.

`DIAGNOSE` ends at a user-visible checkpoint. A single-hypothesis fix starts only after that slice is confirmed. The current literal user request can be that confirmation. The agent must not ask a second time for the same named slice.

`FIX` may continue same-scope work that the user already approved. `fixes for failures introduced by this change` still excludes pre-existing failures found during verification. The same slice stops after two failed fix attempts.

`REVIEW` is not converted into a fix by review findings.

## Clarifying sentences

The source appendix did not contain two sentences that this draft adds, because the current files would otherwise contradict the new rules:

- File A precedence sentence. Existing text says to keep going and to consult grok-cc on material ambiguity. G2 forbids an advisor call in a `VERIFY` failure round. The append states the narrow precedence instead of rewriting the older section.
- File B already-named-slice sentence. Existing text says not to re-ask for already authorized same-scope work. S2's new stop would re-ask even when the user already named the slice. The sentence preserves the existing no-repeat rule.

## Sync boundary

This change does not generate or apply a cross-CLI plan. After any future implementation, Codex runtime `SKILL.md` will differ from the canonical repo and the other three required runtimes until a separate user authorization. File A is native text outside the managed block, so the portable sync path must not absorb it.

## Rollback

Phase A rollback is deletion of this change directory. The backup is a read-only copy. File A and file B rollback after a future implementation is a byte restore from the backup, followed by a fresh SHA256 compare. Do not delete the backup before that decision.
