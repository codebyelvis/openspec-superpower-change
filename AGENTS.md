# AGENTS.md

## Project positioning

`openspec-superpower-change` is a project-level AI development change gate, not an ordinary SDD workflow.

## Required behavior for agents

- Read `SKILL.md` before changing this project.
- Read only task-relevant code/docs and the references selected for the current
  phase. Do not require a whole-repository map or all references before an edit.
- Continue authorized local, reversible reads, minimal edits, relevant/required
  checks and fixes for failures introduced by this change without stepwise
  confirmation. Preserve scope and approval boundaries; do not self-approve Major
  changes or production, credential, destructive, Git or publication authority.
- Before completion after correction/Review history, or when asked to archive and
  distill a session, read `docs/engineering-invariants.md` and
  `references/project-learning-closeout.md`.
- Use Self-Evolution mode when modifying this skill itself.
- Create a backup before self-evolution changes.
- Treat trigger scope, OpenSpec boundaries, Superpowers boundaries, Step Evidence Gate signoff conditions, and completion-claim rules as Major self-evolution. Major changes require OpenSpec approval before implementation.
- Do not weaken Non-negotiables.
- Do not push without explicit user approval.

## Validation

Use acceptance, demonstrated blast radius and change-class required checks.
Self-evolution retains quick validation and core-gate validation. Routing or
governance changes require the full existing unittest suite, including this
Major cleanup. Other edits run affected tests instead of a blanket full suite.
Explicitly required checks in an active approved contract remain mandatory.

Required commands for routing/governance changes:

```bash
"${PYTHON_BIN:-python3}" "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" .
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

`quick_validate.py` requires PyYAML; choose `PYTHON_BIN` from an environment that provides it. Project validators and tests must also pass with the dependency-free fallback.

## Sync

Read `references/sync-checklist.md` before syncing changes between the local runtime skill and this open-source project.
