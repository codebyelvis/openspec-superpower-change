# Design: Close anti-drift hanging states, completion deadlocks, and uninterrupted closed-loop execution

Change-ID: `close-anti-drift-and-completion-deadlocks`
Author: elvis

## Technical Decisions

### 1. Explicit Gate 0 Task Type Recording
In `references/step-evidence-gate.md` and `SKILL.md`, record `task: VERIFY|DIAGNOSE|FIX|REVIEW` in Gate 0 facts.
This provides a verifiable baseline for the stop condition "a task-type change".

### 2. Public Fallback for Numeric Round Budgets
In `SKILL.md`, add:
`If local instructions define no numeric round budget, numeric stops are skipped; boundary, new root cause, advisor-repeat, and two-failure stops remain binding.`
This preserves File A private thresholds without breaking public/distributed runs.

### 3. Pre-existing Debt as BLOCKED Stop
In `references/completion-contract.md`:
`A required-check failure classified as pre-existing debt (OUT_OF_SCOPE_PREEXISTING_DEBT) must not enter self-repair; it transitions to BLOCKED, blocker_owner: user, resume = user confirms an authorized fix slice or records an approved baseline exception.`

### 4. Bounded Completion Loops & Operational Definitions
In `references/completion-contract.md`:
- `SKILL.md`'s two-failure and round-budget stops bound every loop across contract re-entries.
- 1 attempt = 1 code/config edit + its verification.
- Named fix slice = explicit symptom and location specified in the literal request.

### 5. Delegated Review and Uninterrupted Closed-Loop Execution
In `SKILL.md`, `references/confirmation-lease.md`, and `references/approved-implementation-workflow.md`:
When the user's literal prompt specifies closed-loop execution (e.g., "闭环推进") or delegates intermediate approvals/reviews to an advisory reviewer (e.g., "改为询问 grok-cc"):
- Intermediate stages (Plan Preflight, slice execution, local check repairs, step evidence signoff) proceed smoothly from one authorized slice to the next once review/verification PASS evidence is established, without pausing for redundant human conversational confirmations.
- The agent halts ONLY when:
  1. An unresolved `FAIL` reaches breaker limits (two failed attempts on the same slice);
  2. A genuine `BLOCKED` condition occurs (missing required credentials, schema/API breaking change, out-of-scope files);
  3. Reaching user-reserved boundaries (Git add/commit/push, destructive operations, production release).
