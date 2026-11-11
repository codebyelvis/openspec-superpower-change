# Auto-Generated Requirement Markdown & Zero-Arg `/autoloop` Closed-Loop

Author: elvis

Eliminates manual authoring of `docs/req/*.md` and `验收标准：` while preserving governed verification and independent read-only review.

## 1. Automatic Generation When Requirements Arrive (`init-req`)

Whenever a non-trivial requirement, feature slice, or multi-file change enters `openspec-superpower-change` (or is discussed before implementation) and no pending requirement `.md` / active OpenSpec change exists yet, automatically generate the standardized contract (`templates/req-template.md`) via `scripts/autoloop_ctl.py init-req`:

```bash
SKILL_ROOT="$(cd "$(dirname "<path-to-this-skill>/SKILL.md")" && pwd)"
python3 "$SKILL_ROOT/scripts/autoloop_ctl.py" init-req \
  --cwd "$PWD" \
  --slug "<short-slug>" \
  --title "<requirement title>" \
  --summary "<scope, target files, and explicit non-goals>" \
  --cmd "<deterministic test or build command>" \
  --accept "<验收标准：observable business & boundary assertions>"
```

- **Protected Repository Placement**: `init-req` automatically writes to `docs/req/YYYY-MM-DD-<slug>.md` in normal repositories, and redirects `ai_app` to the local Obsidian workbench (`模型开发工作台/docs/req/`) so protected repositories stay clean.
- **OpenSpec Non-Negotiables Preserved**: If the requirement introduces unapproved Major/protected changes, keep the OpenSpec approval stop before mutating production code (`proposal-workflow.md` changes are also auto-matched directly under `openspec/changes/<change-id>/`). Never run `git add/commit/push/reset/clean` without explicit user authorization.

## 2. Explicit `/autoloop` Trigger: Auto-Match or Session-Distill Fallback

When the user triggers `/autoloop` (even with **zero arguments**):

### Step 1: Auto-Match Pending Contract (`match`)
Run:
```bash
python3 "$SKILL_ROOT/scripts/autoloop_ctl.py" match --cwd "$PWD"
```
1. **If `"matched": true`**: Directly bind the matched `req_path` (`project_index` -> `docs/req/*.md` with `status != passed` -> active `openspec/changes/<change-id>/`), along with its embedded `verify_cmd` and `## 验收标准`.
2. **If `"matched": false` (`"fallback": "DISTILL_FROM_CURRENT_SESSION"`)**: Do **not** stop or ask the user to hand-write a markdown file. Immediately **distill the requirement scope, `verify_cmd`, and `## 验收标准` from the current session's conversation/context**, persist it via `autoloop_ctl.py init-req`, and proceed seamlessly. (Ask at most one consolidated question only if the current session has no clear requirement or has a blocking material ambiguity.)

### Step 2: Minimal Local Implementation & Fast Check
- Implement the slice following the Four Anti-Bloat Principles and run `verify_cmd` once locally.

### Step 3: Zero-Arg Governed Background Verification & Independent Read-Only Review (`run`)
```bash
python3 "$SKILL_ROOT/scripts/autoloop_ctl.py" run --cwd "$PWD"
```
- `run` automatically resolves the matched `docs/req/*.md` (or OpenSpec change), executes `verify_cmd` via `agent-autoloop` (`govpi`), runs an isolated read-only Pi review (`--tools read,grep,find,ls`) against the `.md` + `git diff`, verifies zero workspace mutation during review, and marks the requirement `status: passed` upon `"verdict": "PASS"`.
- On `"verdict": "FAIL"`, read `report_path`, apply minimal same-scope fixes, and re-run (at most 2 auto-repair rounds before stopping to report).
