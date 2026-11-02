# Tasks

## 1. Approval

- [x] 1.1 User verbatim approval of change-id `add-verify-anti-drift-round-budget`, `diffs/file-a.AGENTS.md.diff`, and `diffs/file-b.SKILL.md.diff`
- [x] 1.2 User confirmation of G3 numbers: 40 tool calls, 30 minutes, 80 percent checkpoint, and new-test limit 5

## 2. Implementation

- [x] 2.1 Append only the approved file A diff
- [x] 2.2 Replace only the approved file B hunks
- [x] 2.3 Re-hash both files and compare them with the backup

## 3. Evidence

- [x] 3.1 Run the existing skill structure and syntax validators against the edited runtime skill
- [x] 3.2 Run forward scenario `verify-five-one-timeout`, or record `BLOCKED` without a PASS

Result of 3.2 is the isolated Codex probe in `/tmp/verify-five-zPnb`: 4 pass, 1 fail (`checks/t5.sh` exit 124), 0 business-file edits, 0 Git commits. Native events are in `evidence/phase-b.md`. Exit 124 is the script's own status, not a measured wall-clock timeout.

## 4. Review and handback

- [x] 4.1 grok-cc Final Review as advisory input, one re-review at most
- [x] 4.2 Hand back as awaiting user acceptance

The user replied `闭环吧` on 2026-10-30. grok-cc returned advisory `通过` with no finding. That review predates the later probe and the SKILL.md copy alignment.

## 5. Closeout

- [x] 5.1 Record the user closeout, the two blockers, and the decision not to archive
- [x] 5.2 Whole-task completion

5.2 is checked because the user ordered the loop closed on 2026-11-02. The approved rules are landed, `verify-all` passed, and the three evidence-wording fixes named by task `31ba3769-243c-4e3c-b490-bf0240964383` are applied. No Git. See `closeout.md`.
