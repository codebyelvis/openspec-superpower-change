# Self-Evolution Rule

Use this reference when the user asks to improve, refactor, repair, extend, test, or synchronize `openspec-superpower-change` itself.

## Positioning

This skill may improve its own instructions, references, templates, examples, and validation fixtures only through controlled self-evolution.

Self-evolution must never weaken approval gates, evidence gates, verification requirements, or user-control boundaries. Any change that affects request routing, OpenSpec decision rules, Superpowers execution rules, Step Evidence Gate signoff conditions, or completion-claim rules requires an approved change contract before implementation.

For global personal skill edits, short-circuit only unrelated business-project OpenSpec recursion. Do not short-circuit user approval, structured backup, self-evolution gate, RED/GREEN forward-test, validation, rollback, or final reporting. If the skill source itself is being changed as an OpenSpec-managed product repository, require OpenSpec approval.

## Triggers

Enter Self-Evolution mode when the user asks to:

- optimize, refactor, or repair this skill;
- add or reorganize references;
- update `SKILL.md` trigger description or navigation;
- convert repeated lessons into durable skill rules;
- improve examples, templates, validation fixtures, or forward-tests;
- synchronize local and open-source versions of this skill;
- change how this skill routes OpenSpec, Superpowers, discovery, evidence, or completion gates.

## Change levels

| Level | Examples | OpenSpec | Backup | Forward-test | Direct edit allowed |
|---|---|---:|---:|---:|---:|
| Patch | typo, formatting, broken link, minor wording | No | Yes | Optional | Yes |
| Minor | new reference, template, example, response pattern, validation fixture | Usually no | Yes | Recommended | Yes with report |
| Major | trigger scope, request routing, OpenSpec boundary, Superpowers boundary, evidence signoff, completion-claim rule | Yes | Yes | Required | No before approval |

If unsure whether a self-evolution change is Minor or Major, treat it as Major.


## Major Self-Evolution Review Draft Flow

For Major self-evolution, the first deliverable must be a review draft plan, not direct edits. The plan must be stored in the active project or skill review workspace and include:

- observed failures;
- desired behavior;
- files to change;
- exact rule snippets to add or change;
- validation and forward-test plan;
- rollback path.

Major Self-Evolution starts only after a specific OpenSpec change exists, passes
strict validation, and the user explicitly approves that change-id and scoped
contract. A generic request to improve the skill, approval of a review draft, or
runtime edit permission does not substitute for approval of the concrete
OpenSpec change. Record the approval before editing; scope expansion requires a
new approval decision.

## Backup lifecycle

Backups created for self-evolution are temporary rollback aids, not history.
Long-term history must be managed by the configured source repositories for
`openspec-superpower-change` and `codex-brief-antigravity-review`, not by runtime
backup directories.

Rules:

- Create a structured temporary backup before editing.
- Keep it while validation, forward-test, and rollback decisions are unresolved.
- After validation/forward-test pass and the final state is synced to the
  open-source repo, delete temporary backups, `.bak.*` files, and discoverable
  `*.backup*` skill directories.
- Never leave backup skill directories under
  `${CODEX_HOME:-$HOME/.codex}/skills/`;
  they can be discovered as duplicate skills.
- If validation fails or rollback is needed, keep the backup only until rollback
  or user decision is complete, then clean it up.

Before editing, create a timestamped backup of the runtime skill. Run
`quick_validate.py` with a Python interpreter that provides PyYAML; keep the
project validator usable without PyYAML. For example:

```bash
"${PYTHON_BIN:-python3}" "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" "${CODEX_HOME:-$HOME/.codex}/skills/openspec-superpower-change"
PYTHONDONTWRITEBYTECODE=1 python3 "${CODEX_HOME:-$HOME/.codex}/skills/openspec-superpower-change/scripts/validate_core_gates.py" "${CODEX_HOME:-$HOME/.codex}/skills/openspec-superpower-change"
```

Forward-tests must run in a temporary copy or isolated fixture when practical.
Do not mutate `${CODEX_HOME:-$HOME/.codex}/skills/` during forward-tests except
for the explicitly approved target skill edit.

## Required workflow

1. State that Self-Evolution mode is active.
2. Read current `SKILL.md` and affected references.
3. Classify the change level: Patch, Minor, or Major.
4. Create a timestamped temporary structured backup before editing.
5. State the change intent, affected files, expected behavior impact, and rollback path.
6. Decide whether OpenSpec is required.
7. Implement only within the approved skill scope.
8. Run `quick_validate.py` for the skill folder.
9. Run static semantic checks relevant to the change.
10. Run forward-test for Minor changes when practical and for all Major changes after approval.
11. Run profile-appropriate Review; findings return to edit, validation, forward-test, and Review.
12. If portable core-skill files or the shared governance block changed, run
    `references/cross-cli-sync.md` for every declared required Codex, Pi,
    Antigravity CLI, and Grok CLI target. Any stale/failed target is `BLOCKED`.
13. Report changed files, validation results, Review/forward-test results,
    cross-CLI target results, backup cleanup result, residual risks, and rollback path.

## Hard prohibitions

- Do not self-modify without a backup.
- Do not delete backups before validation/forward-test and rollback decisions are complete.
- Do not leave `.bak.*` files or `*.backup*` skill directories after a successful update.
- Do not weaken Non-negotiables.
- Do not bypass OpenSpec approval for Major self-evolution.
- Do not remove verification-before-completion.
- Do not remove Step Evidence Gate signoff conditions.
- Do not silently broaden the skill trigger scope.
- Do not install third-party plugins, alter other skills, or modify production projects unless explicitly requested and separately gated.
- Do not sync to GitHub or push without explicit user approval.
- Do not synchronize auth, tokens, sessions, history, logs, caches, model
  settings, hooks, MCP credentials, binaries, or other CLI-native configuration.

## Validation checklist

Minimum validation after any self-evolution edit:

```bash
"${PYTHON_BIN:-python3}" "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" "${CODEX_HOME:-$HOME/.codex}/skills/openspec-superpower-change"
```

Static checks should confirm:

- `SKILL.md` frontmatter has only `name` and `description`.
- New references are linked from `SKILL.md` when they are part of the routing surface.
- Non-negotiables remain present.
- OpenSpec, Superpowers, Step Evidence Gate, and verification boundaries remain present.
- The change does not introduce private project details into a shareable artifact.

## Forward-test guidance

Use fresh subagents or isolated fixtures. Prompts should ask the agent to use the skill naturally, not to inspect your expected answer.

Recommended self-evolution forward-tests:

1. Review-only request about improving a reference: should not modify files.
2. Minor self-evolution request in a temporary copy: should backup, edit, validate, and report.
3. Major self-evolution request: should require OpenSpec approval before implementation.

## Report format

After self-evolution, report:

- change level;
- temporary backup path and cleanup result;
- files changed;
- why the change was made;
- behavior impact;
- validation commands and results;
- forward-test results;
- residual risks;
- rollback command or path.

## Governed Learning Candidates

Use `learning-candidate-pipeline.md` for user corrections and discovered
invariants. Candidate capture may be automatic, but task-local and project-local
candidates stay within their scope. A global candidate requires two independent
reproductions or one high-severity security, integrity, or false-PASS event even
to propose Self-Evolution. Implementation still requires the specific approved
OpenSpec Change, backup, TDD, forward-tests, Review, runtime synchronization, and
separate publication authorization. Prefer deterministic validators/tests over
repeating mechanical prose.
