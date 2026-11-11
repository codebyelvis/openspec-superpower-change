# Requirement Markdown + Acceptance Criteria Closed-Loop (`docs/req/*.md` + `验收标准：...`)

Author: elvis

Use this path when the user supplies a concrete requirement document (such as `docs/req/<name>.md` or an equivalent project requirement `.md`) together with explicit acceptance criteria (`验收标准：<测试命令或业务要求>`, or acceptance rules already stated inside that `.md`).

## Governance & Contract Boundary

1. **Authoritative Execution Anchor**: Record the exact `.md` path, its SHA-256, and the target verification command in a single-line Gate 0 entry. When the work stays within an already-approved scope, localized bugfix/restoration, or user-authorized slice defined by that `.md`, use the `.md` + acceptance criteria directly as the execution plan—do not ask the user to hand-author `batch.json`, UUIDs, hashes, or duplicate planning files.
2. **OpenSpec Non-Negotiables Preserved**: If the requirement introduces unapproved protected changes (new public API/schema/migration, security/permission changes, or cross-module architectural changes outside an approved spec), keep the OpenSpec approval stop before mutating production code. Never run `git add`, `git commit`, `git push`, `git reset`, or `git clean` without explicit user authorization.

## Three-Step Closed-Loop Execution

### Step 1: Align `docs/req/<name>.md` and `验收标准：`
- Read the requirement `.md` and extract target files, invariants, and exact acceptance criteria.
- Resolve one deterministic verification command `--cmd` (explicit user command takes priority; Java/Maven projects must use the configured Maven 3.6.3 baseline when applicable).
- Ask at most one consolidated question only if a material requirement ambiguity blocks implementation.

### Step 2: Minimal Local Implementation & Fast Check
- Implement the change following the Four Anti-Bloat Principles (no speculative defense, single entry validation, inline single-use logic, no broad `try/catch` around deterministic logic).
- Run the target verification command locally once to confirm baseline green before background signoff.

### Step 3: One-Command Governed `agent-autoloop` Verification & Independent Read-Only Review
Invoke this skill's built-in controller (`scripts/autoloop_ctl.py`, co-located next to `scripts/validate_core_gates.py` in the active skill root):

```bash
SKILL_ROOT="$(cd "$(dirname "<path-to-this-skill>/SKILL.md")" && pwd)"
python3 "$SKILL_ROOT/scripts/autoloop_ctl.py" run \
  --cwd "$PWD" \
  --req "docs/req/<name>.md" \
  --accept "<验收标准：测试命令或业务要求>" \
  --cmd "<deterministic verification command>"
```

What `scripts/autoloop_ctl.py` enforces automatically:
- **Idempotent plugin/rule setup**: Ensures `~/.agent-autoloop/plugins/govpi/` and the manual-event rule `gov.verify.*` in `~/.agent-autoloop/rules.json` match `scripts/gov_runner.py` (backs up `rules.json` before edits; never modifies `~/.agent-autoloop/app/**`).
- **Per-batch isolation**: Passes a unique `batch_id` via the event `subject` (`context.json`) to `<batches_dir>/<batch_id>.json`, preventing concurrent/queued batch overwrite.
- **Anti-runaway & session guard**: Persistent ledger blocks silent `triedFresh` session replacement and calls `agent-autoloop stop <run>` on any `attempt >= 2` re-dispatch so failed/timed-out runs never loop 10 times.
- **Read-only independent review**: Runs `--cmd`, captures `git status -sb` / `git diff HEAD`, launches an isolated read-only Pi reviewer (`--tools read,grep,find,ls`), verifies zero workspace mutation across the review window (`reviewer_readonly_verified: true`), and writes a Schema-2 `report.md` + `receipt.json`.
- **Bounded auto-repair (max 2 rounds)**:
  - On `"verdict": "PASS"`: evaluate whole-task completion under `references/completion-contract.md` and reportChanged files, verification command/counts, and `report_path`.
  - On `"verdict": "FAIL"`: read `report_path`, fix the cited defect within the same authorized scope, and re-run `autoloop_ctl.py run` (circuit-break and report to the user after at most 2 failed repair rounds or on `"BLOCKED"`).
  - For long-running suites (>5 min), pass `--async` to return `batch_id` immediately and query later with `autoloop_ctl.py status <batch_id>`.
