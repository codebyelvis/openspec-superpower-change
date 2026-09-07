# streamline-simple-change-gates Implementation Plan

## Scope

Implement the approved `streamline-simple-change-gates` contract in one
business slice. Change only the nine approved source/test files plus this plan,
OpenSpec progress, and required Review evidence. Do not change schemas,
profiles, lifecycle values, Git state, publication, or unrelated runtime logic.

Execution is bound to worktree
`/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/add-skillsmp-index-adapter`,
branch `add-skillsmp-index-adapter`, base
`272e37467f2ec8b29a72daac61c873bc612d12d2`. The branch also contains the
unfinished `add-skillsmp-index-adapter` change. Preserve that work. Governance
Reviews inspect only the nine approved source/test paths, this change's
OpenSpec/Plan/Review evidence, and the runtime-sync evidence produced below.

## Implementation

1. Add a small focused regression set to `tests/test_workflow_rules.py` for:
   compact inline execution, one Plan/no duplicate Brief for single-slice work,
   the two-pass Preflight ceiling, no Preflight reopen for same-scope findings,
   consolidated single-slice Review, proportional TDD, and strict preservation.
2. Update `SKILL.md` and the approved references so those assertions pass.
   Remove only contradictory universal wording; preserve safety, approval,
   verification-before-completion, strict effects, Git, and publication gates.
3. After source validation and a separate independent Implementation Review,
   synchronize the seven changed manifest-declared files to Codex, Pi,
   Antigravity CLI, and Grok CLI with schema-v2 scoped sync. Do not push.

## Runtime synchronization

Use these exact bindings and selectors:

```bash
SYNC_ROOT="$(mktemp -d /tmp/openspec-gates-sync.XXXXXX)"
SYNC_PLAN="$SYNC_ROOT/plan.json"
SYNC_TX="$SYNC_ROOT/transactions"
SYNC_BACKUP="$SYNC_ROOT/backups"
mkdir -p "$SYNC_TX" "$SYNC_BACKUP"

python3 scripts/validate_cross_cli_sync.py plan \
  --manifest references/cross-cli-portable-manifest.json \
  --openspec-source "$PWD" \
  --brief-source /Users/elvis/file/develop/opensource/codex-brief-antigravity-review \
  --codex-skills-root /Users/elvis/.codex/skills \
  --codex-rule-file /Users/elvis/.codex/AGENTS.md \
  --pi-skills-root /Users/elvis/.pi/agent/skills \
  --pi-rule-file /Users/elvis/.pi/agent/APPEND_SYSTEM.md \
  --antigravity-skills-root /Users/elvis/.gemini/antigravity-cli/skills \
  --antigravity-rule-file /Users/elvis/.gemini/GEMINI.md \
  --grok-skills-root /Users/elvis/.grok/skills \
  --grok-rule-file /Users/elvis/.grok/AGENTS.md \
  --select-file openspec-superpower-change:SKILL.md \
  --select-file openspec-superpower-change:references/approved-implementation-workflow.md \
  --select-file openspec-superpower-change:references/completion-contract.md \
  --select-file openspec-superpower-change:references/direct-change-rule.md \
  --select-file openspec-superpower-change:references/request-modes.md \
  --select-file openspec-superpower-change:references/self-evolution-rule.md \
  --select-file openspec-superpower-change:references/step-evidence-gate.md \
  --output "$SYNC_PLAN"
```

Review the path/hash-only plan. Then, in this exact target order, run `apply`,
`verify`, `verify-discovery`, and `commit-target`, using receipt
`$SYNC_TX/<target>.json` and backup root `$SYNC_BACKUP/<target>`:

```bash
python3 scripts/validate_cross_cli_sync.py apply --target <target> --plan "$SYNC_PLAN" --transaction-receipt "$SYNC_TX/<target>.json" --backup-root "$SYNC_BACKUP/<target>"
python3 scripts/validate_cross_cli_sync.py verify --target <target> --plan "$SYNC_PLAN" --transaction-receipt "$SYNC_TX/<target>.json"
python3 scripts/validate_cross_cli_sync.py verify-discovery --target <target> --plan "$SYNC_PLAN" --transaction-receipt "$SYNC_TX/<target>.json"
python3 scripts/validate_cross_cli_sync.py commit-target --target <target> --plan "$SYNC_PLAN" --transaction-receipt "$SYNC_TX/<target>.json"
```

Targets are `codex`, `pi`, `antigravity-cli`, `grok-cli`. On any apply or
verification failure before `commit-target`, run the matching command below
for that target and stop before the next target:

```bash
python3 scripts/validate_cross_cli_sync.py restore-target --target <target> --plan "$SYNC_PLAN" --backup-root "$SYNC_BACKUP/<target>" --transaction-receipt "$SYNC_TX/<target>.json"
```

For Grok, replace the generic discovery command with the following isolated,
mode-0600 evidence capture and consuming verification:

```bash
(umask 077; cd /Users/elvis/.grok && grok inspect --json > "$SYNC_TX/grok-inspect.json")
python3 scripts/validate_cross_cli_sync.py verify-discovery --target grok-cli --plan "$SYNC_PLAN" --transaction-receipt "$SYNC_TX/grok-cli.json" --inspect-json "$SYNC_TX/grok-inspect.json" --consume
```

After all four commits:

```bash
python3 scripts/validate_cross_cli_sync.py verify-all --plan "$SYNC_PLAN" --transaction-root "$SYNC_TX"
```

After a target is committed, same-scope Review findings are corrected forward
and resynchronized with a fresh reviewed plan. If the change is abandoned or
must be rolled back after one or more target commits, restore the nine canonical
source files from `/tmp/openspec-review-flow-backup.7cZ0C2`, validate the
restored source, generate a fresh schema-v2 reverse plan with the same exact
bindings/selectors and a new private sync root, Review its path/hash-only
prestate, and run the same apply/verify/discovery/commit/verify-all sequence.
Do not call `restore-target` on a committed (`verified`) receipt; it is only for
the current uncommitted target.

## Verification

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_workflow_rules -v
python /Users/elvis/.codex-account-a/skills/.system/skill-creator/scripts/quick_validate.py .
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
openspec validate streamline-simple-change-gates --strict
git diff --check
```

Run exactly two isolated static contract scenarios from the existing unittest
runner; each method uses only repository text fixtures and no runtime mutation:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_workflow_rules.WorkflowRulesTest.test_compact_direct_change_uses_inline_fast_path -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_workflow_rules.WorkflowRulesTest.test_strict_security_recovery_preserves_full_gates -v
```

Because this Major change modifies protected workflow boundaries, obtain a
separate independent Implementation Review before runtime sync. After sync,
Project Learning Closeout, and fresh final verification, obtain a separate
independent Final Review of the complete governance diff and runtime evidence.
Any same-scope finding returns directly to focused verification and the same
Review stage; it does not reopen Preflight unless a protected boundary changes.

## Rollback and stop conditions

Rollback uses `/tmp/openspec-review-flow-backup.7cZ0C2`. Stop for scope,
authority, strict-risk, schema/profile/lifecycle, Git/publication, or runtime
sync boundary changes. One initial Preflight is the only planned Preflight; if
blocked, consolidate corrections into one terminal recheck and do not open R3+.
