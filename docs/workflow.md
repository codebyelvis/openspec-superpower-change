# Workflow

`openspec-superpower-change` routes governed changes proportionally by risk and contract impact rather than forcing a single heavy linear ceremony:

1. Read applicable local instructions and only the task-relevant code/docs and phase-selected references.
2. Record Gate 0 before state-changing edits, commands, or proposal creation (one line for obvious local reversible work).
3. Clarify domain terms or material trade-offs (`grill-with-docs` / `brainstorming`) only when unresolved choices materially affect scope, architecture, security, compatibility, or acceptance.
4. Decide whether OpenSpec is required (`references/openspec-decision-rule.md`).
5. **Compact Direct Change**: apply the minimal edit, run required/relevant checks, and record an inline diff/self-review without standalone Plan, Preflight, or `status.md` ceremony.
6. **Daily Requirement Closed-Loop (`/autoloop`)**: match or session-distill `docs/req/*.md` + `验收标准`, implement minimally, and run `scripts/autoloop_ctl.py run` for background verification plus isolated read-only AGY review (up to 2 auto-repair rounds).
7. **OpenSpec-Required Work**: draft and validate `openspec/changes/<change-id>/` with `openspec validate <change-id> --strict`, then stop for explicit user approval before implementation.
8. **Plan-Anchored Execution**: when approved OpenSpec `design.md` + `tasks.md` already define the Four Hard Anchors (scope, `path:line` targets, cohesive batches, exact test commands), execute directly without a duplicate Superpowers plan or standalone local Preflight JSON; otherwise generate an executable plan and run bounded Preflight Review (`FULL_PREFLIGHT` + at most one `FOCUSED_RECHECK`).
9. Apply Step Evidence Gate to complete business slices (recording concise inline RED-to-GREEN proof rather than intermediate JSON sprawl), not TDD micro-steps.
10. Run verification and profile-appropriate Review; actionable findings return to same-scope fix, fresh verification, and Review (stopping on the two-failure breaker or scope drift).
11. Run Project Learning Closeout when correction/Review history or an explicit archive/distill request triggers durable promotion.
12. Evaluate `references/completion-contract.md`: persist fresh final verification and Final Review (consolidated into one post-verification report on eligible single-slice standard work), reconcile OpenSpec `tasks.md`, archive when permitted, and report changed files, evidence, residual risks, and next steps.
