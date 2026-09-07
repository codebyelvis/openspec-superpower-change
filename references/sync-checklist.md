# Sync Checklist

Use this checklist whenever `openspec-superpower-change` changes in either the local runtime skill or the open-source project.

## Scope

This checklist applies to:

- Patch self-evolution when the change should be shared across local/open-source copies;
- all Minor self-evolution changes;
- all Major self-evolution changes after OpenSpec approval;
- any change touching `SKILL.md`, `references/`, `scripts/`, `templates/`, or examples.

## Required paths

Set these for the current checkout instead of hardcoding a user's home path:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
OPENSPEC_SKILL_SOURCE="${OPENSPEC_SKILL_SOURCE:-$PWD}"
BRIEF_SKILL_SOURCE="${BRIEF_SKILL_SOURCE:-$(dirname "$PWD")/codex-brief-antigravity-review}"
ANTIGRAVITY_CLI_HOME="${ANTIGRAVITY_CLI_HOME:-$HOME/.gemini/antigravity-cli}"
GROK_HOME="${GROK_HOME:-$HOME/.grok}"
PI_CODING_AGENT_DIR="${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}"
```

For portable core-skill or shared-governance changes, also read
`references/cross-cli-sync.md`. The open-source repositories are the canonical
sources; only the bound Codex control-plane instance/contract is the
authoritative decision owner. Codex, Pi, Antigravity CLI, and Grok CLI are
required runtime targets unless the user declares a valid `not-applicable`
decision before synchronization.

## Pre-change checklist

1. Confirm the change level: Patch, Minor, or Major.
2. If Major, stop and require OpenSpec approval before implementation.
3. Confirm the intended source of truth for this change: local runtime, open-source project, or both.
4. Create timestamped temporary structured backups before editing both affected trees.
5. Check the open-source repo is clean before editing:

```bash
git -C "$OPENSPEC_SKILL_SOURCE" status -sb
```

## Sync checklist

1. Apply the change to the intended primary tree.
2. Apply the same logical change to the secondary tree unless explicitly out of scope.
3. Compare key files when both trees should stay aligned:
   - `SKILL.md`
   - `references/handoff-contract.md`
   - `references/superpowers-adapter.md`
   - `references/self-evolution-rule.md`
   - `references/step-evidence-gate.md`
   - `references/sync-checklist.md`
   - `scripts/validate_core_gates.py`
   - companion Brief `SKILL.md`, evidence templates, Handoff Contract, and
     `scripts/validate_templates.py`
4. Do not force byte-for-byte equality when local runtime needs stricter execution details than the open-source project.
5. Do require logical equality for:
   - Non-negotiables;
   - OpenSpec approval boundary;
   - Superpowers planning boundary;
   - Step Evidence Gate signoff boundary;
   - Self-Evolution Patch/Minor/Major classification;
   - backup, validation, forward-test, and no-push-without-approval rules.
6. When portable manifest content changed, generate and Review a path/hash-only
   cross-CLI sync plan, then apply and verify Codex, Pi, Antigravity CLI, and
   Grok CLI one target at a time. A failed target is restored and blocks later
   targets.
7. Update only the versioned managed governance block in each CLI global rule
   file. Preserve all native bytes outside the marker block.

### Scoped plan verification

- No selector keeps legacy sync-plan schema v1 and its complete mutation closure.
- Use repeatable `--select-file <skill-name>:<portable-relative-path>` and,
  only when approved, `--select-managed-rule` for schema-v2 scoped plans.
- Require managed-rule version 6, exact four-target coverage, normalized
  manifest-order selectors, and at least one selected operation.
- Verify v2 `files` contains mutation operations only and `assertions` contains
  every unselected manifest file exactly once. The managed rule is a separate
  conditional operation and is `selected: false` by default.
- Before planning/apply, require parity for every assertion and every
  unselected rule. Prestate drift blocks before backup or receipt creation.
- Review the path/hash-only plan before apply. Backups, receipts, restore, and
  recovery consume selected operations only; content verification, discovery,
  digest, commit, and `verify-all` cover the full selected-plus-asserted closure.
- Bind v2 `managed_rule.destination` to the target-specific canonical runtime
  path derived from the absolute `skills_root`: Codex/Pi/Grok use the parent
  root (`AGENTS.md`/`APPEND_SYSTEM.md`/`AGENTS.md`), while Antigravity uses the
  grandparent `.gemini` root (`GEMINI.md`). Reject destination/pre-state
  retargeting before candidate, backup, or apply.
- Reject empty, duplicate, unknown, unsafe, sensitive, target-incomplete, and
  non-v6 selections before writing a plan. Never infer scope from Git status or
  use a manual-copy path.

## Validation checklist

Run for both local and open-source copies when present:

```bash
"${PYTHON_BIN:-python3}" "$CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py" "$CODEX_HOME/skills/openspec-superpower-change"
PYTHONDONTWRITEBYTECODE=1 python3 "$CODEX_HOME/skills/openspec-superpower-change/scripts/validate_core_gates.py" "$CODEX_HOME/skills/openspec-superpower-change"
"${PYTHON_BIN:-python3}" "$CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py" "$OPENSPEC_SKILL_SOURCE"
PYTHONDONTWRITEBYTECODE=1 python3 "$OPENSPEC_SKILL_SOURCE/scripts/validate_core_gates.py" "$OPENSPEC_SKILL_SOURCE"
"${PYTHON_BIN:-python3}" "$CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py" "$CODEX_HOME/skills/codex-brief-antigravity-review"
PYTHONDONTWRITEBYTECODE=1 python3 "$CODEX_HOME/skills/codex-brief-antigravity-review/scripts/validate_templates.py" "$CODEX_HOME/skills/codex-brief-antigravity-review"
"${PYTHON_BIN:-python3}" "$CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py" "$BRIEF_SKILL_SOURCE"
PYTHONDONTWRITEBYTECODE=1 python3 "$BRIEF_SKILL_SOURCE/scripts/validate_templates.py" "$BRIEF_SKILL_SOURCE"
```

Set `PYTHON_BIN` to an interpreter with PyYAML. Run both repositories'
standard-library `unittest` suites with default `python3` to exercise fallback behavior.

For a cross-CLI-triggering change, additionally run
`scripts/validate_cross_cli_sync.py` in plan, per-target apply/verify, and
verify-all modes. Confirm Grok discovery with `grok inspect --json`; Codex, Pi,
and Antigravity use deterministic manifest/reference closure plus compatible
validators. Pi native validation never runs Pi; any optional Pi process probe
uses the isolated temporary-root contract in `cross-cli-sync.md`.

When Grok reports `source.type=configToml`, require all expected Skills to share
one exact root that maps uniquely to an earlier target in the reviewed plan.
Accept it only after that target's same-plan receipt is `verified` and a fresh
full-closure parity check passes; bind the reported paths and source receipt
digest into discovery evidence. Reject mixed or unplanned roots/types, missing
Skills, stale receipts, or drift. Do not inspect or mutate `config.toml`.

## Forward-test checklist

Run forward-tests when:

- the change is Minor and affects routing, examples, references, scripts, or validation behavior;
- the change is Major after approval;
- reviewers explicitly request it.

Minimum scenarios:

1. Review-only should not modify files.
2. Direct bugfix should not require OpenSpec and must verify.
3. OpenSpec-required new behavior should stop before implementation.
4. Major self-evolution weakening request must require OpenSpec and refuse direct implementation.
5. Minor self-evolution in a temporary copy should backup, edit, validate, and report.

## Backup cleanup checklist

After validation and required forward-tests pass:

1. Remove temporary structured backups created for the update.
2. Remove `.bak.*` files from the runtime skill and open-source working trees.
3. Remove discoverable `*.backup*` skill directories from `$CODEX_HOME/skills/`.
4. Keep a temporary backup only when validation fails, rollback is pending, or the
   user explicitly asks to retain it.
5. Treat the open-source git history as the long-term version history; do not
   keep parallel backup histories in skill discovery paths.
6. Remove obsolete discoverable backup skill directories only after their exact
   real paths are inventoried, validated as contained non-symlink directories,
   and explicitly authorized for deletion.

## Git checklist for open-source sync

1. Review diff:

```bash
git -C "$OPENSPEC_SKILL_SOURCE" diff --stat
git -C "$OPENSPEC_SKILL_SOURCE" diff
```

2. Commit with a clear message.
3. Push only after explicit user approval.
4. Report commit hash and validation results.

## Report checklist

Every sync report must include:

- change level;
- source of truth;
- temporary backup paths and cleanup result;
- changed files in local runtime skill;
- changed files in open-source project;
- validation commands and results;
- forward-test result when run;
- cross-CLI trigger decision, required targets, per-target sync/discovery result,
  managed-rule version/body hash, and any `BLOCKED`/`not-applicable` evidence;
- residual risks;
- rollback path.

## Schema-6 Deployment Drain

Before applying portable schema-6 files, inventory every known canonical
`docs/agent-collab/*/status.md`. Any active schema-4/schema-5 contract blocks
deployment until it completes under its old runtime. Never rewrite, silently
migrate, resume after cutover, ignore, or abandon active legacy state. Complete
legacy contracts/evidence remain immutable. Retain only non-sensitive inventory
fields and repeat the check immediately before the first runtime apply.
