# Plan: support Grok configured Skill discovery

Approved change: `support-grok-configured-skill-discovery`.

1. Add one focused regression slice covering a valid same-plan `configToml`
   source and fail-closed mixed, unplanned, unverified, stale, or drifting sources.
2. Extend Grok discovery verification to accept configured roots only when the
   root maps uniquely to a planned target with a verified same-plan receipt and
   current canonical parity; bind the source and receipt evidence into the Grok
   discovery digest. Preserve existing `user` behavior and never read config.
3. Update the two sync references, run focused plus required project validation,
   then generate and Review a fresh scoped four-target plan and complete the
   transactional sync through `verify-all`.

Focused and required validation:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_cross_cli_sync -v
python3 /Users/elvis/.codex-account-a/skills/.system/skill-creator/scripts/quick_validate.py .
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
openspec validate support-grok-configured-skill-discovery --strict
```

Fresh scoped runtime plan and transaction:

```bash
set -euo pipefail
SYNC_ROOT=$(mktemp -d /tmp/openspec-grok-sync.XXXXXX)
chmod 700 "$SYNC_ROOT"
SYNC_PLAN="$SYNC_ROOT/plan.json"
SYNC_BACKUP="$SYNC_ROOT/backups"
SYNC_TX="$SYNC_ROOT/transactions"
mkdir -m 700 "$SYNC_TX"

python3 scripts/validate_cross_cli_sync.py plan \
  --manifest references/cross-cli-portable-manifest.json \
  --openspec-source "$PWD" \
  --brief-source /Users/elvis/file/develop/opensource/codex-brief-antigravity-review \
  --codex-skills-root /Users/elvis/.codex/skills --codex-rule-file /Users/elvis/.codex/AGENTS.md \
  --pi-skills-root /Users/elvis/.pi/agent/skills --pi-rule-file /Users/elvis/.pi/agent/APPEND_SYSTEM.md \
  --antigravity-skills-root /Users/elvis/.gemini/antigravity-cli/skills --antigravity-rule-file /Users/elvis/.gemini/GEMINI.md \
  --grok-skills-root /Users/elvis/.grok/skills --grok-rule-file /Users/elvis/.grok/AGENTS.md \
  --select-file openspec-superpower-change:SKILL.md \
  --select-file openspec-superpower-change:references/approved-implementation-workflow.md \
  --select-file openspec-superpower-change:references/completion-contract.md \
  --select-file openspec-superpower-change:references/cross-cli-sync.md \
  --select-file openspec-superpower-change:references/direct-change-rule.md \
  --select-file openspec-superpower-change:references/request-modes.md \
  --select-file openspec-superpower-change:references/self-evolution-rule.md \
  --select-file openspec-superpower-change:references/step-evidence-gate.md \
  --select-file openspec-superpower-change:references/sync-checklist.md \
  --select-file openspec-superpower-change:scripts/validate_cross_cli_sync.py \
  --output "$SYNC_PLAN"
python3 scripts/validate_cross_cli_sync.py verify-prestate --target all --plan "$SYNC_PLAN"

for target in codex pi antigravity-cli; do
  receipt="$SYNC_TX/$target.json"
  python3 scripts/validate_cross_cli_sync.py apply --target "$target" --plan "$SYNC_PLAN" --backup-root "$SYNC_BACKUP" --transaction-receipt "$receipt"
  python3 scripts/validate_cross_cli_sync.py verify --target "$target" --plan "$SYNC_PLAN" --transaction-receipt "$receipt"
  python3 scripts/validate_cross_cli_sync.py verify-discovery --target "$target" --plan "$SYNC_PLAN" --transaction-receipt "$receipt"
  python3 scripts/validate_cross_cli_sync.py commit-target --target "$target" --plan "$SYNC_PLAN" --transaction-receipt "$receipt"
done

receipt="$SYNC_TX/grok-cli.json"
python3 scripts/validate_cross_cli_sync.py apply --target grok-cli --plan "$SYNC_PLAN" --backup-root "$SYNC_BACKUP" --transaction-receipt "$receipt"
python3 scripts/validate_cross_cli_sync.py verify --target grok-cli --plan "$SYNC_PLAN" --transaction-receipt "$receipt"
(umask 077; cd /Users/elvis/.grok && grok inspect --json > "$SYNC_TX/grok-inspect.json")
python3 scripts/validate_cross_cli_sync.py verify-discovery --target grok-cli --plan "$SYNC_PLAN" --transaction-receipt "$receipt" --inspect-json "$SYNC_TX/grok-inspect.json" --consume
python3 scripts/validate_cross_cli_sync.py commit-target --target grok-cli --plan "$SYNC_PLAN" --transaction-receipt "$receipt"
python3 scripts/validate_cross_cli_sync.py verify-all --plan "$SYNC_PLAN" --transaction-root "$SYNC_TX"
```

Stop on the first failed command and do not start a later target. If the failed
target has a nonterminal receipt, run its exact `restore-target` command with
the same plan, backup root, and receipt before any retry; a recovery-blocked or
manual-disposition result ends the run without ad-hoc copying.

```bash
python3 scripts/validate_cross_cli_sync.py restore-target \
  --target "$target" --plan "$SYNC_PLAN" --backup-root "$SYNC_BACKUP" \
  --transaction-receipt "$SYNC_TX/$target.json"
```

Rollback: restore the four approved files from
`/tmp/openspec-grok-discovery-backup.kOYl9D`; runtime sync uses per-target
durable receipts and backups, restoring any uncommitted failed target.
