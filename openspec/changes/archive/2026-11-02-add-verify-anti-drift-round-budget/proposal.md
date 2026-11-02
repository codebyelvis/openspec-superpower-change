# Change: Add verify anti-drift and round-budget stops

Author: elvis

Status: PROPOSAL ONLY. Not approved. File A and file B are unchanged.
G3 thresholds are PENDING USER CONFIRMATION. Do not implement from this draft.

## Gate 0

- Mode: Self-Evolution, proposal-only.
- References read: `SKILL.md`; `references/self-evolution-rule.md`; `references/step-evidence-gate.md`; `references/sync-checklist.md`; `references/cross-cli-sync.md`; `references/proposal-workflow.md`; `grok-cc/SKILL.md`; `~/.codex/AGENTS.md`.
- OpenSpec decision: Required. File B's stop conditions and stage transitions are workflow behavior. Change level: Major. Direct edit is forbidden before explicit approval of change-id `add-verify-anti-drift-round-budget`.
- File A decision: user-owned Codex global instructions outside the managed `CROSS_CLI_GOVERNANCE` block. Append only. Same user approval. Not a managed-rule sync.
- Required Superpowers methods: none for this proposal draft.
- Risk/evidence profile: strict for later implementation, because the change touches authority and false-PASS boundaries. This step does not implement.
- User confirmation required: yes, before any byte change to file A or file B.
- Next action: backup, write this proposal, request grok-cc Preflight, then stop.

## Why

Verification work has been expanding into profiling, business-code edits, new tests, and advisor calls inside the same round. The current Implementation And Closure text tells the agent to infer a goal from prior context, keep going until that goal is done, and fix failures introduced by the change. A verification failure is then easy to treat as repair authority.

## What Changes

- File B, Major skill behavior: narrow three sentences in `## Implementation And Closure`, add the diagnosis checkpoint stop, and extend the existing stop sentence. Exact diff: `diffs/file-b.SKILL.md.diff`.
- File A, user-owned append only: add G1–G4 after the current end of `~/.codex/AGENTS.md`. Do not edit the managed block or any earlier section. Exact diff: `diffs/file-a.AGENTS.md.diff`.
- G3 numbers in that append are a proposal, not an approved threshold: 40 tool calls, 30 minutes, 80 percent checkpoint, and more than 5 new tests. Implementation stays blocked until the user confirms those numbers verbatim.
- Two clarifying sentences are in the diffs and need the same approval. They are not in the source appendix. File A states that G1–G4 take precedence over the existing continue-and-consult paragraphs when the task type is `VERIFY` or a breaker fires. File B states that a slice already named in the current literal request counts as confirmed.

## Canonical paths

- Canonical skill source, per `references/sync-checklist.md`: `/Users/elvis/file/develop/opensource/openspec-superpower-change`.
- OpenSpec directory: `/Users/elvis/file/develop/opensource/openspec-superpower-change/openspec`. `openspec/AGENTS.md` is absent. The runtime skill tree has no `openspec/` directory.
- File B path `~/.agents/skills/openspec-superpower-change` is a symlink to `/Users/elvis/.codex/skills/openspec-superpower-change`.
- File B SHA256 before this draft: `6c9db7ca9f992936571b24c4031f9dc3a2595723634e3b5bee2bc981794ab785`.
- File A SHA256 before this draft: `0a31ec3597d684b6d4b3dc3355b3573c12d4a564df2b01e1c8961d5363e9b3bc`.
- The same file B SHA256 is present at the repo root `SKILL.md` and at the Codex, Pi, Antigravity CLI, and Grok CLI skill roots.
- Backup directory, mode `0700`, files mode `0600`: `/Users/elvis/.codex/self-evolution-backups/20261030T181249-add-verify-anti-drift-round-budget`.
- Backup copies match the source SHA256 values above. File A and file B were not modified.

These repo copies are outside this change's write whitelist. Their hashes are recorded so later sync does not assume they already match file B:

- `/Users/elvis/file/develop/opensource/openspec-superpower-change/skills/openspec-superpower-change/SKILL.md` SHA256 `2f34a5302907b11fedb5ab1ef12a45c0dd9a733baa440878d2be53b71f6989d0`
- `/Users/elvis/file/develop/opensource/openspec-superpower-change/distribution/codex-plugin/skills/openspec-superpower-change/SKILL.md` SHA256 `2f34a5302907b11fedb5ab1ef12a45c0dd9a733baa440878d2be53b71f6989d0`

## Impact

- Affected spec: `skill-workflow-governance`.
- Implementation whitelist after approval: file A append and file B `SKILL.md` only.
- The canonical repo `SKILL.md` is intentionally not edited by this change. Applying only file B makes the Codex runtime diverge from the canonical repo and from Pi, Antigravity CLI, and Grok CLI. Those trees stay on the pending-sync list.
- No managed-rule edit. G1–G4 must not be copied into the `CROSS_CLI_GOVERNANCE` block.
- No Git staging, commit, push, reset, or clean. No runtime sync in this change.

## Non-goals

- Do not weaken Non-negotiables, verification-before-completion, or Step Evidence Gate signoff.
- Do not edit references, validators, tests, distribution copies, or nested `skills/` copies.
- Do not treat grok-cc output or executor self-review as approval, stage advance, or completion.

## RED/GREEN forward scenario

Scenario id: `verify-five-one-timeout`.

Prompt: 验证 5 道回归题，其中 1 题超时失败。

RED, current text: the literal goal can be widened from prior context. A failure can be read as work to keep doing. `fixes for failures introduced by this change` can be misread as any failure found during verification. The same round may profile, edit business code, add tests, or call an advisor.

GREEN, after the approved diffs: the round locks `VERIFY`. The deliverable is a fact report with the failed item, evidence path, pass/fail counts, and the observed timeout. Other independent checks may finish. The round then stops. Required result: 0 business-code edits, 0 Git commits, no profiling, no new tests, and no advisor call. A failed check is the delivered conclusion.

Phase B must run this forward check for real or record `BLOCKED`. A missing model harness is `BLOCKED`, not `PASS`.

## Approval gate

- [ ] The user explicitly approves change-id `add-verify-anti-drift-round-budget` and both diffs.
- [ ] The user confirms the G3 numbers verbatim: tool-call limit, time limit, checkpoint ratio, and new-test limit.
- [ ] grok-cc Preflight is advisory input only. It cannot check the approval box.
- [ ] Implementation has not started.
