# Phase 1 supported-subset closeout plan

> **For agentic workers:** Use the existing router-governed `superpowers:executing-plans` method. Codex implements locally; Pi independently reviews. User already selected closed-loop execution. No Git or new execution-method approval.

Goal: close phase 1 for Codex + Pi under the user's 2026-11-09 path A authorization. AGY remains restricted direct/manual fallback; no static tool clipping or new Agent is required. No automatic AGY readiness claim.
Architecture: one disposable host probe, existing CLIs/account, raw terminal evidence. No installed runner, plugin, background event or rules edit.
Tech: Python standard library, installed Codex/Pi, OpenSpec CLI.
Spec: design.md and specs/skill-workflow-governance/spec.md with approval-amendment-20261109.json.

## Gate 0 and ownership

Approved implementation / FIX, strict evidence; individual probes VERIFY (no repair/retry authorization from a failure). Relevant references: existing SKILL.md, approved-implementation-workflow.md, step-evidence-gate.md, amended design/spec and preserved approval history. Methods: writing-plans / executing-plans / verification-before-completion, reuse router-governed variant. No adapter or iteration-loop. Existing approved worktree is unchanged. User authorizes the support-subset contract amendment; this is a new Preflight lineage, not a third round for the old unchanged contract.

Only this change's proposal/design/spec/tasks/approval/plan/evidence and `/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/governed-cli-phase1-s58l8ops/closure-20261109` may change. CLI-native session records may use existing logged-in account locations. Original repos, both SKILL.md, core scripts, global config, credentials, conda, installation, plugins, rules, Git and stages2–4 remain outside this slice. Backups and old 11-hash evidence already preserved under closure-20261109/before.

## Current commands

All subprocesses use argument arrays, explicit fixture cwd and existing Node24 PATH prefix `/Users/elvis/.nvm/versions/node/v24.22.2/bin`. Codex account remains `/Users/elvis/.codex-account-a`.

- Codex binary `/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex`, version `0.167.0-alpha.3.2`. R1: `exec --ignore-user-config --skip-git-repo-check --json -c sandbox_mode="read-only" -c approval_policy="never" -`. R2/write: `exec resume` with same options then exact UUID and `-`; stdin prompt, process cwd, no -s/-C on resume. No project config exists in fixture. Record actual sandbox policy, startup errors and native tool events; reject any observed external/MCP effect. This single fixture probe cannot certify arbitrary account or future plugin settings.
- Pi binary `/Users/elvis/.local/bin/pi`, version `1.5.0`: `--print --mode json --thinking high --no-mcp --no-extensions --no-skills --no-context-files --no-prompt-templates --tools read,grep,find,ls`. R1 adds new `--session-id UUID --session-dir <fixture-root>/pi-sessions`; R2/write uses verified exact `--session <absolute-jsonl>`, never --continue or session-id for resume. Tool exposure must be exactly read/grep/find/ls.
- Real model calls have a 180s host deadline, TERM own process group and at most5s before KILL remaining own group; record actual group disappearance. If previous exit/terminal/group/identity/cwd or session file isn't accepted, do not start its dependent call.

## One cohesive slice, existing acceptance groups only

1. Preserve Pi's exact continuation review text/event and 11 hashes before mutable tasks change (done). Run one FULL_PREFLIGHT on this revised scope/plan, at most one same-session focused correction. No existing product source tests are modified.
2. For Codex and Pi, fresh R1 reads only fixture input.txt and remembers per-product nonce; R2 retrieves nonce without tools or repeated nonce, and returns matching JSON. Parse real native ID and current terminal. Codex requires turn.completed, nonempty final text, no turn.failed/error; Pi requires final assistant stopReason=stop, agent_settled not aborted. Both require exit0, no deadline, ended process group, unchanged fixture. Before R2, verify exact session file exists/nonempty, header's native identity and normalized cwd, previous accepted terminal, and no unknown/live state. After R2, require native ID and nonce equal R1. Never accept a silent new session.
3. On the accepted session, one write probe per product asks to create only fixture forbidden.txt once with existing tools, no escalation or alternate paths. Codex requires actual correlated native tool denial (not model text alone), read-only sandbox policy and no fixture change. Pi requires actual toolsAdded set and no write tool, no fixture change. No tool list alone proves successful unauthorized execution. If evidence insufficient, retain BLOCKED.
4. One disposable host entry tests missing/empty/mismatched session, unknown previous state and changed cwd using the same launch guard without calling a model; all must reject before launch. One fresh no-tools-request CLI process per product is interrupted by a 1s host deadline: require own process group exit and no accepted normal completion. These are direct host deadline proofs, not CLI internal timeout or backend cancellation, and cannot satisfy stage2 worker/unknown proofs. No native session is resumed after interruption. These variations remain inside existing identity/permission/terminal groups, not a new matrix or persistent framework.
5. Preserve raw argv/stdout/stderr/exit/identity/files/tool-result evidence and SHA256 manifest, then `openspec validate integrate-governed-cli-autoloop --strict`; independent Pi Review of all changes and facts. Mark tasks1.2/1.3 complete only for this exact supported subset if actual acceptance passes and review has no actionable finding. Otherwise keep the specific failure pending. Historical AGY/report facts remain immutable. No stage2 dispatch in this slice.

## Review focus / stop

Unknown previous state cannot become fresh session; empty identity cannot bypass guard; changed binary cannot inherit old runtime PASS; stderr/exit0 alone cannot create completion; static tool definitions and executed authority differ; scope reduction is user-authorized and does not weaken remaining evidence/retry/ownership gates. Pi Reviewer provides bounded evidence, no canonical state or installation/Git authorization. Failure runs remaining independent checks then reports under G2; no unapproved fix. All temporary processes are owned by this slice, never stop user services or other sessions. Preserve evidence and untracked change; no destructive cleanup.
