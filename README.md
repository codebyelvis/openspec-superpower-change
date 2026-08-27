# openspec-superpower-change

[English](README.md) | [简体中文](README_cn.md)

`openspec-superpower-change` is a Codex skill that acts as the change-control entry gate for AI-assisted engineering work. It connects project-local rules, OpenSpec change contracts, Superpowers execution practices, and evidence-based verification into one repeatable workflow.

The goal is simple: an AI agent should not move from a request directly to implementation when the work may affect runtime behavior, public contracts, security, persistence, workflow routing, or operator-visible behavior.

## Highlights

- Classifies every request before state-changing work begins.
- Separates review-only, discovery, proposal, approved implementation, direct change, and self-evolution modes.
- Decides when OpenSpec is required and blocks implementation before approval.
- Routes approved work into Superpowers planning, TDD, debugging, and verification flows.
- Requires Step Evidence Gate output before progress or completion claims.
- Requires current-revision Plan/Brief Preflight Review before execution.
- Uses current schema-6 Handoff state plus schema-2 evidence to bind the full
  immutable Reviewer Assignment; frozen schema 4/5 records remain read-only
  legacy audit history and cannot authorize current work.
- Treats Codex, Pi, Antigravity CLI, and Grok CLI as equally eligible assigned
  executors/reviewers. Product names grant no authority; only the bound Codex
  `control-plane` / `control-plane-high` instance and contract own routing,
  evidence acceptance, canonical state, archive, and completion decisions.
- Requires every Review recommendation or request to state its purpose, one
  concrete product, role, capability profile, independence, and result authority.
- Separates platform, workflow-scope, and business/production authorization;
  High Review audits actual wiring, mechanisms, and an independent probe.
- Adds a read-only `backend-architecture-review` specialist for explicit backend
  proposal/design reviews, with bounded findings that keep Review/Fix work
  convergent toward the smallest project-consistent correction.
- Provides lightweight Authorized Execution Continuity for long tasks: resume
  approved work from canonical Plan/Status/Handoff state after compaction,
  recovery, or agent switches, and stop only at real blockers or completion.
- Provides allowlisted Codex/Pi/Antigravity/Grok runtime synchronization with a
  versioned managed governance block, target-local recovery, four-target
  completion, and sensitive-category denial. Pi uses
  `${PI_CODING_AGENT_DIR}/skills` and the managed block in
  `${PI_CODING_AGENT_DIR}/APPEND_SYSTEM.md`.
- Runs a conditional Domain Context Check so clear tasks stay lean while
  ambiguous project language enters `grill-with-docs` or the portable fallback.
- Turns costly corrections and Review findings into durable project knowledge
  and regression enforcement before final completion.

## Governed Caveman Lite

The built-in, default-off `governed-caveman-lite` profile makes ordinary Router
prose concise while keeping professional full sentences. Enable it for the
current conversation with `OpenSpec 精简模式：<任务>` (or send `OpenSpec 精简模式`
before the task), and disable it with `OpenSpec 正常模式`.

The profile changes presentation only. It does not require an external Caveman
skill, does not persist beyond the current conversation, and never compresses
away governance fields, approvals, evidence, critical commands, or security and
safety text.

## Why It Exists

AI coding agents can be effective, but in production-grade repositories they commonly fail in ways that are preventable:

- implementing before reading local project rules;
- treating a task checklist as an approved contract;
- using test-only evidence for runtime behavior claims;
- bypassing OpenSpec for API, persistence, security, or workflow changes;
- weakening governance rules while editing the governance skill itself;
- losing track of approval status across external-agent handoffs.

This skill turns those risks into explicit gates, references, and validation checkpoints.

## How It Fits

| Capability | Responsibility | Owned By |
|---|---|---|
| Local project rules | Repository-specific constraints, review artifacts, handoff rules, commit conventions | Project `AGENTS.md` / local docs |
| Project knowledge | Domain glossary, engineering invariants, decisions, learning provenance, regression enforcement | `CONTEXT.md`, project docs/ADRs, Candidate Cards, tests/validators |
| OpenSpec | Change contract, requirements, scenarios, approval state | `openspec/` |
| Superpowers | Implementation planning, TDD, debugging, verification discipline | Superpowers skills |
| Step Evidence Gate | Evidence required before advancing or claiming completion | `references/step-evidence-gate.md` |
| Completion Contract | Single Router-owned whole-task success, stop, evidence, reconciliation, sync, and authority contract | `references/completion-contract.md` |
| Prompt / external batch review | Standalone prompt/diff review and Handoff-backed Brief/Report/Review attempts | `codex-brief-antigravity-review` |
| Backend architecture Review | Read-only specialist evidence for explicit backend proposal/design reviews covering boundaries, contracts, call chains, transactions, performance, stability, or over-design | `backend-architecture-review` |
| Authorized execution continuity | Lightweight continuation of approved work from canonical Plan/Status/Handoff state across long tasks, compaction, recovery, or agent switches | `references/approved-implementation-workflow.md` |
| openspec-superpower-change | Routing, risk classification, approval gate, self-evolution boundary | This skill |

## Core Workflow

```text
Read local rules
-> Gate 0 request classification
-> Domain Context Check; use grill-with-docs only for unresolved language/boundaries
-> classify phase and material choices
-> select Superpowers by phase, material ambiguity, and risk (generic create/modify wording is insufficient)
-> OpenSpec proposal if contracts or high-risk behavior change
-> stop until approval
-> Superpowers plan for approved implementation
-> Plan/Brief Preflight Review; revise and repeat until PASS
-> TDD / debugging / implementation discipline
-> Step Evidence Gate on complete business slices
-> verify -> Review -> fix and repeat until Review PASS
-> Project Learning Closeout; promote and verify/Review required project knowledge
-> persist fresh final verification evidence, then final diff/scope Review
-> reconcile/archive OpenSpec and validate after archive
-> authorized Git publication
-> session archive/distillation summary that references durable project artifacts
```

## Long-Task Continuity and Review Convergence

- **Authorized Execution Continuity** reuses unchanged, scope-bound canonical
  Plan/Status/Handoff or equivalent state. `continue` resumes the next approved
  task instead of restarting completed work or inventing a second task ledger.
- Continuity never grants new scope, credentials, production permission, or
  material product/business/architecture decisions. A blocker, new decision,
  scope expansion, missing resource, explicit pause/cancel, or completion stops
  the continuation path with an owner and resume condition where applicable.
- **Backend architecture Review** is the explicit route for proposal/design
  judgment about service boundaries, contracts, call chains, transactions,
  performance/stability, and over-design. It is read-only specialist evidence;
  it does not implement fixes or decide canonical Completion.
- Review output stays proportional: at most three material findings, each tied
  to evidence, trigger, impact, and the smallest project-consistent adjustment.
  Actionable findings return to `Fix -> Verify -> Review`; repeated widening or
  non-convergence stops as `BLOCKED` instead of expanding the solution.

## Detailed Decision Flow

The decisive order is:

```text
request facts -> Domain Context Check -> phase classification -> material-choice
check -> risk/evidence profile -> selected Superpowers full rules -> approval or
execution -> Project Learning Closeout -> final verification/Review -> archive ->
authorized publication -> session distillation
```

For governed state-changing, Git-mutating, or whole-task-completion work, the
Router chooses zero or more Superpowers methods; users do not need to name each
method. Naming a method explicitly grants no business, Git, workflow, or
completion authority and cannot bypass Gate 0. On Codex, `using-superpowers` is
explicit-only while Router-required child Skills remain eligible for implicit
matching until native nested loading is proven. Without a supported Skill-load
path/hash trace, actual prompt load or non-load is reported as `UNKNOWN` rather
than inferred from visible behavior.

| Phase | Required behavior |
|---|---|
| Entry / Gate 0 | Read local instructions and the affected project knowledge, classify the current request, choose evidence/capability profiles, and state whether confirmation is still required. |
| Domain Context Check | Inspect `CONTEXT-MAP.md`, `CONTEXT.md`, affected ADRs, docs, and code when project language may change. Clear language skips `grill-with-docs`; unresolved terms, actors, boundaries, states, or lifecycle enter it, or the complete portable Discovery First fallback. |
| Proposal-only | Inspect repository facts and existing specs. Use only reversible, explicit bounded assumptions; strictly validate proposal/design/spec/tasks and stop for approval of the exact change-id. Do not load planning/TDD/implementation Review merely because the request says create or modify. |
| Material choice | Security, compatibility, destructive migration, data lifecycle, scope, production authority, and testable acceptance remain user-owned choices. Delegating the choice to the agent still requires brainstorming and its full HARD-GATE. |
| Approved implementation | Refresh Gate 0, create an executable plan, Preflight Review the current revision, then use TDD/debugging and Step Evidence Gate on complete business slices. Every finding returns to fix -> verify -> Review. |
| External Handoff | The companion runs the complete current schema-6 Handoff lifecycle. Codex, Pi, Antigravity CLI, and Grok CLI may fill assigned executor/reviewer roles, but their evidence cannot advance canonical state until the bound Codex control plane accepts it. |
| Project Learning Closeout | After implementation Review PASS, audit corrections and findings. Automatic thresholds or an explicit request to archive and distill require promotion of confirmed project-local knowledge and regression enforcement. |
| Finalization | Run fresh final verification only after learning promotion, then final diff/scope/sensitive-data Review, task reconciliation, OpenSpec archive, and strict post-archive validation. |
| Publication | Git staging/commit/push remain separately authorized. The final session summary points to durable repository knowledge; it is never the only record. |

## Project Learning Layers

One costly lesson may produce several small artifacts, each with one job:

| Knowledge | Durable location | What must not go there |
|---|---|---|
| Domain language and semantic relationships | `CONTEXT.md` / `CONTEXT-MAP.md` | implementation causes, incident chronology, task lists |
| Easy-to-miss implementation or agent invariant | repository policy, default `docs/engineering-invariants.md` | full chat/Review transcript |
| Hard-to-reverse, surprising trade-off | `docs/adr/NNNN-slug.md` | ordinary or easily reversible fixes |
| Promotion provenance | `docs/learning-candidates/YYYY-MM-DD-<slug>.md` | secrets, customer data, private prompts |
| Mechanically enforceable behavior | deterministic regression test or validator | prose-only claims |
| Session archive/distillation | final summary with links to the artifacts above | becoming the sole knowledge store |

Automatic promotion is required after two independent correction/Review signals
establish the same project invariant, or one high-severity security, integrity,
data-loss, or false-PASS event establishes it. An explicit archive-and-distill
request always runs the audit and promotes every confirmed project-local key
point. Required promotion blocks completion until focused verification and
Review PASS.

## Concerns and Mechanisms

| Concern | Mechanism |
|---|---|
| Broad metadata creates unnecessary ceremony | Phase-aware precedence (`CCG-014`) routes governed work through exactly one Router, while ordinary questions bypass the Router and Codex `using-superpowers` meta-entry. |
| An explicit Superpowers method appears to grant authority | It chooses discipline only; Router Gate 0 still owns workflow, business, Git, and completion authority and fails closed without exactly one applicable Router. |
| Disabling Superpowers removes safeguards | Activation is adaptive; once selected, every sub-skill keeps its complete rules. |
| Agents silently choose auth/compatibility behavior | Material user-owned choices still require brainstorming and approval. |
| `CONTEXT.md` exists only as a stale local file | Canonical shared context must not be intentionally ignored and must enter the change inventory. |
| A hard-won bug lesson remains only in chat | Candidate Card + Project Learning Closeout + correct durable artifact + regression enforcement. |
| An external PASS is mistaken for completion | Codex remains the control plane; learning, final verification, final Review, archive, and sync gates still apply. |

## Workflow Optimization Decision (2026-07-30)

The evaluated workflow remains on **Scheme C: keep the existing combination**.
OpenSpec stays the single authoritative change contract, Superpowers continues
to provide post-approval engineering discipline, and
`codex-brief-antigravity-review` keeps its standalone and Handoff-backed Review
responsibilities.

- No Superpowers skill or runtime copy was removed.
- No `mattpocock/skills` package was installed; the selected dependency closure
  is empty.
- No global skill qualified for permanent deletion.
- Useful ideas from `mattpocock/skills` remain future candidates, including
  `tdd`, `diagnosing-bugs`, dual-axis `code-review`, domain grilling, and
  tracer-bullet ticket slicing.
- Schemes A/B remain blocked by missing worktree and branch-finish equivalents,
  unsafe `implement` Review/commit ordering, Codex compatibility gaps, and
  incomplete evidence/lifecycle parity.

### How to interpret “currently best”

“Best” has an explicit boundary here: it is the risk-adjusted choice among
Schemes A/B/C for the pinned versions, current Codex environment, and governance
constraints evaluated in this project. It is not an absolute ranking of every
industry workflow, future release, or development scenario. Scheme A replaces
Superpowers completely, Scheme B retains only a minimal subset, and Scheme C
keeps the existing combination. The primary comparison is the cross-project
governance lifecycle, not how quickly one skill can be learned or how deeply it
understands a particular technology stack.

| Evaluation scale | Current combination | `mattpocock/skills` | Current judgment |
|---|---|---|---|
| Quick start for one low-risk project | More concepts and gates create a higher initial learning cost | Individual skills are concise, direct, and easier to adopt | Candidate is lighter |
| Long-term maintenance across projects, services, and stacks | Contract, risk, evidence, Review, and completion rules are centralized; each project supplies its native build and test commands | Raw adoption still needs project-specific authorization, evidence, branch, and lifecycle adapters | Current combination is more stable |
| Auditability and reproducibility | OpenSpec revisions, Handoff identity, evidence freshness, and final-completion ownership can be checked consistently | TDD, debugging, and Review methods are strong, but no equivalent whole lifecycle contract exists | Current combination is more complete |
| Stack-specific depth | Does not replace a project's framework, deployment, security, or data toolchain | Also operates at the method layer and does not supply project-specific expertise automatically | Native project tooling decides |
| Maintenance at scale | More components, but one centralized upgrade can serve many projects and amortize the fixed cost | A single skill is easy to maintain; making it own the full lifecycle can create adapter copies and project drift | Use candidates for isolated capabilities; keep current governance for the combination |

The precise conclusion is therefore: **the current combination is the default
best choice among the evaluated schemes for cross-project, cross-service, and
cross-stack engineering governance; `mattpocock/skills` is easier to learn for
a single low-risk project or isolated capability.** It remains a candidate
source for TDD, debugging, dual-axis Review, domain clarification, and vertical
slicing. Adopt or replace capabilities only when a measured gap and complete
parity evidence justify a new Self-Evolution change.

### Keeping third-party dependencies current

Scheme C does not promise that every dependency is silently upgraded to the
latest release. Blind upstream tracking would break reproducibility and could
change triggers, authority, or completion rules without Review. The guarantee
to pursue is **traceable provenance, detectable staleness, verified upgrades,
and recoverable rollback**.

The version ledger must record the **tested compatibility baseline, effective
local version, latest observed upstream version, and version currently
available through the installation channel** separately. These values can
differ: a marketplace mirror can lag its source repository, and updating the
Codex CLI does not update an independent Git clone, symlinked skill, or
downloaded skill.

| Installation mode | Actual update semantics | Required action |
|---|---|---|
| Project-maintained source → runtime copy | The Git repository is authoritative; the runtime copy does not follow it automatically | Synchronize and verify parity with `references/sync-checklist.md` |
| Git clone + skill symlink | The symlink exposes local checkout changes only; it does not fetch official releases | Compare the upstream SHA explicitly and perform a controlled update after reconciling local commits |
| Codex marketplace plugin | The plugin manager records an installed version; an upstream release does not by itself prove the local installation changed | Verify with `codex plugin list --json`, refresh through the supported marketplace flow, and validate in a new session |
| Skill downloaded by `skill-installer` | Installation is a snapshot; the installer stops when the destination already exists and is not an in-place updater | Record the source ref/SHA, back up, replace or reinstall deliberately, and revalidate |

A controlled dependency upgrade closes this loop:

1. Record the installation mode, four version values, upstream source, symlink
   target, and local patches.
2. Detect upstream releases read-only and review release notes plus the actual
   diff. Detection is not automatic approval.
3. Create a temporary backup and reconcile local patches in an isolated copy or
   branch.
4. Run upstream tests plus the Router and Companion validators, unit suites,
   required-skill inventory/discovery checks, and real-behavior forward
   scenarios. Existing validator PASS alone does not prove third-party
   compatibility.
5. Synchronize to runtime only after Review PASS; start a new session and verify
   discovery paths and the effective version.
6. Record the new version, evidence, and rollback point. Restore the previous
   version and stop promotion on any failure.

An upgrade that changes trigger scope, OpenSpec or Superpowers boundaries,
evidence gates, or completion rules is Major Self-Evolution and requires an
approved OpenSpec change first. This repository does not currently claim an
automatic dependency-freshness checker; until one is implemented, maintenance
must run these checks explicitly and must not equate “discoverable skill” with
“latest official version.”

See the [full evaluation](docs/design/2026-07-30-workflow-skill-optimization-evaluation.md)
and [independent Review](docs/design/reviews/2026-07-30-workflow-skill-optimization-plan-c-archive-review.md).
Re-evaluation requires the evidence listed in section 14 of the evaluation and,
for an A/B implementation, a separately approved Major Self-Evolution change.

## Request Modes

| Mode | Use When | File Changes? |
|---|---|---:|
| Review-only | The user asks this change gate to review architecture, authorization, risk, or completion evidence. | No |
| Backend architecture Review | The user explicitly asks for backend architecture/design Review covering boundaries, contracts, calls, transactions, performance/stability, or over-design. | No |
| Discovery First | Terms, actors, lifecycle, or boundaries are unclear. | Usually glossary / context only |
| OpenSpec proposal | New capability, behavior contract, architecture, security, persistence, API, or workflow changes are needed. | Proposal artifacts only |
| Approved implementation | An OpenSpec-backed proposal has been explicitly approved. | Yes, after plan |
| Direct Change | Low-risk restoration, typo, formatting, docs-only, config-only, or tests for existing behavior. | Yes, scoped |
| Self-Evolution | This skill, its references, validators, examples, or sync rules are being changed. | Yes, gated |

For proposal-only drafting, Gate 0 may select no Superpowers sub-skill when
repository facts and bounded assumptions produce a reviewable contract. If
brainstorming is selected for a material unresolved choice, its complete
HARD-GATE remains in force; after implementation is approved, planning,
Preflight, TDD, Review, evidence, verification, and archive gates remain
unchanged.

Standalone task-prompt/Brief/checklist writing and ordinary read-only diff or Report review belong to `codex-brief-antigravity-review`. “Review and fix” returns here because it is implementation.

## Gate 0

Before editing files, running state-changing commands, creating proposal artifacts, or starting implementation, the agent must state:

1. active request mode;
2. references read and why they are sufficient;
3. whether OpenSpec is required;
4. required Superpowers sub-skills;
5. risk level, next action, and whether user confirmation is required.

## OpenSpec Boundary

OpenSpec is required for:

- new functionality or public behavior changes;
- API, schema, data lifecycle, persistence, or migration changes;
- security, sandbox, permissions, cross-tenant behavior, or auth changes;
- runtime tool exposure, cache strategy, request routing, skill routing, or workflow lifecycle changes;
- broad refactors that alter system boundaries;
- skill workflow changes.

OpenSpec may be skipped only for narrow restoration of existing intended behavior, small config changes without contract impact, typo/comment/formatting changes, docs-only updates without behavior impact, or tests for already-defined behavior.

## Evidence Profiles

| Profile | Typical Use |
|---|---|
| compact | Low-risk docs, formatting, config, or localized direct changes. |
| standard | Default multi-step implementation, review, and verification. |
| strict | Security, auth, public API/schema, persistence, migration, deployment, rollback, or cross-tenant work. |

## Repository Structure

```text
.
├── SKILL.md
├── references/
│   ├── request-modes.md
│   ├── local-instruction-checkpoint.md
│   ├── learning-candidate-pipeline.md
│   ├── project-learning-closeout.md
│   ├── openspec-decision-rule.md
│   ├── proposal-workflow.md
│   ├── approved-implementation-workflow.md
│   ├── direct-change-rule.md
│   ├── step-evidence-gate.md
│   ├── superpowers-adapter.md
│   ├── self-evolution-rule.md
│   ├── sync-checklist.md
│   ├── cross-cli-sync.md
│   └── cross-cli-portable-manifest.json
├── scripts/
│   ├── validate_core_gates.py
│   └── validate_cross_cli_sync.py
├── tests/
│   ├── test_workflow_rules.py
│   └── test_cross_cli_sync.py
├── openspec/
│   ├── project.md
│   └── changes/
├── examples/
├── templates/
│   └── learning-candidate-template.md
└── docs/
```

## Key References

- `references/request-modes.md`: operating modes and constraints.
- `references/local-instruction-checkpoint.md`: local rules and canonical context durability checks.
- `references/learning-candidate-pipeline.md`: candidate scope, thresholds, and promotion authority.
- `references/project-learning-closeout.md`: project knowledge targets, enforcement, and completion blocking.
- `references/openspec-decision-rule.md`: when OpenSpec is mandatory.
- `references/proposal-workflow.md`: proposal creation and validation flow.
- `references/approved-implementation-workflow.md`: approved implementation workflow.
- `references/completion-contract.md`: the only normative whole-task completion checklist.
- `references/direct-change-rule.md`: low-risk direct change requirements.
- `references/step-evidence-gate.md`: compact and full evidence templates.
- `references/superpowers-adapter.md`: OpenSpec-aware Superpowers artifact, permission, and Preflight mapping.
- `references/self-evolution-rule.md`: rules for changing this skill.
- `references/sync-checklist.md`: local runtime and open-source copy synchronization.
- `references/cross-cli-sync.md`: four required runtime targets, managed-rule
  parity, discovery, target-local recovery, and completion blocking.

## Installation

Copy or link this skill into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R openspec-superpower-change "${CODEX_HOME:-$HOME/.codex}/skills/openspec-superpower-change"
```

## Validation

Run validation after editing the skill:

```bash
"${PYTHON_BIN:-python3}" "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" /path/to/openspec-superpower-change
PYTHONDONTWRITEBYTECODE=1 python3 /path/to/openspec-superpower-change/scripts/validate_core_gates.py /path/to/openspec-superpower-change
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s /path/to/openspec-superpower-change/tests -v
```

Current governed status uses schema 6 with an immutable Reviewer Assignment.
Validate its schema-2 evidence manifests with:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 /path/to/openspec-superpower-change/scripts/validate_core_gates.py \
  /path/to/openspec-superpower-change \
  --status /project/docs/agent-collab/<change-id>/status.md \
  --artifact-root /project
```

Each referenced artifact embeds a schema-2 evidence manifest that binds its
role/result/change/batch/attempt/source fingerprint plus assigned product,
instance, role, and capability profile. Before a transition introduces new
evidence, validate a proposed status from outside the project with
`--previous-status /project/docs/agent-collab/<change-id>/status.md`; this is
mandatory for `complete`. Replace the one canonical status only after PASS, and
do not persist a second marker block in the project.

Frozen schema-4/schema-5 records are legacy audit/drain inputs only. Inventory
them separately; never pass them to current `--status` validation or migrate
them into schema 6:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 /path/to/openspec-superpower-change/scripts/validate_core_gates.py \
  /path/to/openspec-superpower-change \
  --legacy-inventory-root /project \
  --legacy-inventory-output /private/tmp/legacy-drain.json
```

`quick_validate.py` requires PyYAML; set `PYTHON_BIN` accordingly. The project validator and tests exercise the dependency-free fallback.

Portable core-skill changes must additionally use
`scripts/validate_cross_cli_sync.py` to generate a path/hash-only plan, apply and
verify each explicitly authorized runtime target, verify discovery/parity, and
run the path/category-only sensitive audit. Runtime/global writes remain subject
to explicit user authorization.

## Example Prompts

```text
Use openspec-superpower-change review-only mode. Read local rules, inspect this implementation plan, and report whether it requires OpenSpec. Do not modify files.
```

```text
Use openspec-superpower-change as the entry gate. Decide whether this requires Discovery First or an OpenSpec proposal before implementation.
```

```text
Use Direct Change mode. Confirm this restores intended behavior, make the smallest fix, run verification, and report evidence before claiming completion.
```

```text
Use backend-architecture-review for a read-only Review of this backend proposal. Inspect the actual project code and report only material boundary, contract, transaction, performance, stability, or over-design findings.
```

```text
Continue the approved task from its canonical Plan/Status/Handoff state. Do not restart completed work, create a second ledger, or expand scope without a new decision.
```

## Maintenance Notes

- Update both `README.md` and `README_cn.md` for every published repository
  change, keeping user-visible behavior, decisions, validation, and
  compatibility notes aligned.
- Do not weaken approval gates, evidence gates, or completion-claim rules.
- Do not let OpenSpec `tasks.md` replace a Superpowers implementation plan.
- Do not let `CONTEXT.md` replace OpenSpec proposal artifacts.
- Do not let required project learning remain only in chat, Review output, or
  prose when deterministic enforcement is possible.
- Do not sync runtime and open-source copies with directory-level overwrites; use the sync checklist.
- Do not complete verified-but-unreviewed work; any Review finding restarts correction, verification, and Review.
- Do not call OpenSpec-backed work closed with unreconciled tasks or without the
  repository-appropriate archive and post-archive validation.

## License

MIT. See [LICENSE](LICENSE).
