# Changelog

## Unreleased

- Add provenance-gated rule retirement with SIM append-only tombstones
  (`S11`, Major `add-sim-provenance-rule-retirement`):
  - `references/self-evolution-rule.md`: add `## Provenance-Gated Rule
    Retirement` codifying Major-only approval, repository-anchored
    non-retirable files/sections (`SKILL.md`, `shared-global-governance.md`,
    `completion-contract.md`, `step-evidence-gate.md`, `handoff-contract.md`,
    `confirmation-lease.md`, `agent-capability-routing.md`,
    `openspec-decision-rule.md`, locked governance sections, and
    `Non-Negotiables`/`CCG-*`/`validator-locked` phrases), `origin_anchor`
    provenance, structured bidirectional proof (`mechanical-superseded` >=1
    entry or `cross-model-internalized` >=2 distinct normalized runtimes/model
    families without a closed model allowlist), and `BACKLOG.md` append-only
    `record_kind: sim-retirement` tombstones with `reopen_condition`.
  - `references/skill-iteration-loop.md` &
    `templates/learning-candidate-template.md`: add the 5th optimizer-memory
    guideline forbidding silent resurrection of `retired` rules unless fresh
    evidence triggers `reopen_condition`, and document `retired` alongside
    `reverted` as non-gating attempt memory.
  - `scripts/validate_core_gates.py` & `tests/test_workflow_rules.py`: add
    `NON_RETIRABLE_FILES`, `NON_RETIRABLE_SECTIONS`,
    `NON_RETIRABLE_SLUG_TOKENS`, `validate_sim_retirement_record`,
    `validate_sim_rule_retirement_guard`, and conditional `BACKLOG.md`
    retirement-block scanning wired into `main(...)` (compatible with
    distribution/runtime roots without `docs/iteration/`), with dual-YAML
    (`PyYAML` + `simple_yaml_load`) regression tests and isolated 2-scenario
    forward-tests.

- Add Self-Evolution attempt memory (`S10`, SIM-inspired Minor slice):
  - `templates/learning-candidate-template.md`: add optional, append-only
    `root_cause` and `attempts` (`provenance` / `change` / `predicted` /
    `observed`) fields compatible with both PyYAML and `simple_yaml_load`,
    retaining failed/reverted attempts as non-gating optimizer memory under
    existing redaction rules.
  - `references/skill-iteration-loop.md`: instruct Self-Evolution runs to read
    relevant BACKLOG `attempts` before modifying rules/scripts, record pre-eval
    `predicted` and post-eval `observed` in `CURRENT` and append attempts on
    closeout, apply four concise optimizer-memory reuse rules (from
    `arXiv:2611.18856v1` Appendix D.2), and explicitly keep SIM memory
    non-gating and out of everyday hot paths.
  - `docs/iteration/BACKLOG.md` & `tests/test_workflow_rules.py`: add one
    backfilled demonstration record (`Minor-autoloop-hardening`), track `S10`,
    and cover template/loop/BACKLOG dual-YAML parsing and non-gating guards
    with deterministic regression tests and an isolated forward-test.

- Harden `/autoloop` runtime guardrails, commit hygiene, and cold-path
  partitioning (`2026-11-19` Minor slice):
  - `scripts/gov_runner.py`: extend credential redaction to compound key
    prefixes (`access_token`, `DB_PASSWORD`, `OPENAI_API_KEY`), `Basic`/`Token`
    auth schemes, password-only URLs (`redis://:pwd@host`), raw token prefixes,
    and full/truncated PEM private key blocks without swallowing query emails or
    trailing error lines; fix `review_rejected` `failure_signature` collapse,
    Maven spaced duration (`0.421 s`) normalization, `FAILED (` footer leakage,
    and overly broad `TEST_HEADER_LINE_RE`; enforce exact-line anchored
    `_is_pass_verdict_line` to prevent False-PASS while tolerating plain `模型：`
    headers; isolate reviewer CLI in its own process group with `SIGTERM`
    `killpg`, `OSError` handling (`127`/`126` for list-form `verify_command` as
    well), and malformed JSON line tolerance; tighten `SHELL_CMD_MISSING_RE` to
    real shell errors; and inspect rename source paths (`parts[1:]`) for fast
    high-risk escalation.
  - `scripts/autoloop_ctl.py`: tighten `OPENSPEC_TEST_CMD_RE` (`mvn` safe
    charset and `[ \t]` whitespace only), ignore `README.md`/`INDEX.md`/
    `TEMPLATE.md` and terminal statuses in `match_project_req`, support CRLF and
    trailing `\n---` frontmatter symmetrically in `parse_req_markdown` and
    `mark_req_passed`, lock `project-index.json` updates via `fcntl.flock`, and
    stop in-flight `run_id` on wait timeout.
  - `scripts/check_commit_text.py`: exempt standard `Merge:` + `Merge ` commits
    in `git log` from Conventional Commit formatting while keeping secret/key
    and `Co-authored-by:` checks intact and applying `profile_cfg` to the first
    non-merge commit.
  - `references/approved-implementation-workflow.md`: relocate
    `<!-- COLD_PATH_START ... -->` and `## Project Session Resume` losslessly to
    the end of the file so everyday hot-path sections precede the cold-path
    marker as specified.
  - `tests/test_gov_runner_git_capture.py`: remove hardcoded personal path
    assertion, fix 14.5% SHA-256 hex collision flakiness (`123` -> `z9w8q7`),
    and add targeted regressions covering all fixes above.

- Fuse deterministic verification guardrails, diagnosability hunt lens, and
  learning enforcement hierarchy (`fuse-harness-pstack-guardrails`): pass caller
  `PATH` (`verify_env_path`) into `gov_runner.py`, isolate verification process
  groups (`start_new_session=True` + `os.killpg` on timeout/SIGTERM), short-circuit
  non-zero verification exits before launching the read-only reviewer CLI with
  4-way `failure_kind` (`timeout` / `setup_or_env_error` / `empty_test_execution`
  / `verification_failed`), mask URL `@`-containing passwords and quoted JSON
  secrets in `verify_error_excerpt`, and compute test-ID-aware non-collapsing
  `failure_signature` hashes; veto zero-test `v_code == 0` runs unless at least
  one positive test count ran; add 5th conditional hunt lens
  `diagnosability_context` and snapshot-sourced `fast` high-risk path/stem
  escalation (`-high` + `autoloop-review-hunt.md`); and codify `Attack the
  Premise` repair convergence and the 4-tier mechanical learning hierarchy.

- Align `/autoloop` OpenSpec test extraction, review manifest roles, portability,
  and cold-path/overview docs: extract deterministic test/validator commands from
  `openspec/changes/<id>/{proposal,tasks,design}.md` when matching active OpenSpec
  changes; align `gov_runner.py` `pi-accept` manifest output to `batch-review` /
  `independent-reviewer` / `control-plane-high` (and `pi-verify` to
  `cohesive-medium`); remove hardcoded personal machine paths in
  `scripts/autoloop_ctl.py` in favor of environment overrides and dynamic host
  probing; extract rare blocked-context/control-plane rebind rules into
  `references/resume-context-amendments.md`; and refresh
  `references/workflow-overview.md` and `docs/workflow.md` for schema-6 and
  Four Hard Anchors.

- Add deterministic read-only next-action query and dual-mode Headless CLI
  cross-review (`add-next-action-query` & `optimize-closed-loop-runtime-routing`):
  add `scripts/next_action.py` (`--status <path>`) delegating transition
  legality exclusively to `validate_transition` via `probe_transition_candidate`
  and `EXPECTED_OWNERS` in `scripts/validate_core_gates.py` (with zero-transition
  strict `blocked` resume echo, fail-closed `BLOCKED` on invalid status, and
  advisory-only non-promotable output); and add dual-mode cross-verification
  routing (`pi -p` / `agy -p` direct Headless CLI invocation by default with
  copyable Review Prompt fallback and closed-loop `FULL_PREFLIGHT -> Fix ->
  FOCUSED_RECHECK` / `Review -> Fix -> Verify -> Review` chaining).

- Streamline plan-anchored execution (`streamline-plan-anchored-execution`):
  unify approved four-anchor OpenSpec (`design.md` + `tasks.md`) with the
  executable Plan without duplicate Superpowers plans or standalone local
  Preflight JSONs; default to coarse-grained `Single Cohesive Batch` execution
  with inline RED-to-GREEN proof instead of intermediate `red-green.json` /
  `native-green.json` file sprawl; allow three-condition localized bugfixes to
  use Direct Change without a pre-existing spec path; keep `status.md` lazy for
  `compact`/`standard` work and exclude `CHANGELOG.md`/ledgers/historical
  reports from `verified_revision.inputs`; add in-place `<!-- COLD_PATH_START`
  partitioning in `references/approved-implementation-workflow.md`; and remove
  deprecated `grok-cc` references.

- Close anti-drift hanging references, task type recording, and completion deadlocks:
  record Gate 0 task type (`task: VERIFY|DIAGNOSE|FIX|REVIEW`); add fallback for
  missing local numeric round budgets; route pre-existing debt to `BLOCKED` instead
  of self-repair; bound completion loops by the two-failure stop across re-entries;
  and enable uninterrupted closed-loop execution when delegated review or closed-loop
  intent is authorized.

- Reuse exact existing authorization before asking again; distinguish immutable
  approval bindings from refreshed execution evidence and scoped blocker repair
  from gate advancement. Accept complete inline facts where compact reporting
  already applies, and keep grok-cc advice separate from implementation handoff.
  Preserve approval, actor, transport, independent Review and completion gates.

- Align shared native instruction consumption: expose the compact-local
  Preflight exception and ordinary advisory route, preserve required plan timing
  and bound artifact paths, and distinguish actual-entry qualification from
  four-target portable parity. Keep both skills, schema/product sets and native
  hook/config exclusions; add owner-bound negative regressions and a bounded
  native Codex projected-instruction probe.

- S8: resolve ordinary document placement from explicit project contracts and
  established conventions before purpose-directory fallbacks. Centralize the
  ownership rule and engineering learning target; preserve protected artifact
  locations and require authorized reference closure for document moves.

- S9: add strict-local stage-specific resume reviewer binding and an explicit,
  approved blocked-context amendment check; preserve legacy and external gates.

- Add approved S7 project-session checkpoints in the existing canonical status,
  an explicit local schema-6 subset, hashed verification/review bindings and
  read-only recovery diagnostics. Preserve full external Handoff APIs, approval
  and instance ownership; stale inputs require verification without rollback.
  Strict recovery retains implementation Review before final completion.

- Add S6 quarterly upstream-entry notes and a reusable observation template
  with commit-pinned primary sources. Notes do not approve upgrades or rule
  adoption; no dependency or runtime content changes. Keep the next review
  window at 2027 Q1.

- Document S5 workspace boundaries: edit the known repository-root source,
  treat distribution and nested catalog adapters as generated output, and
  write installed runtime content through reviewed sync transactions.
  No new mandatory worktree flow or synchronization target is introduced.

- Add S4 phase-selected reading budgets and a lightweight entry lint that
  rejects affirmative whole-reference preloading while preserving scoped,
  negative, and fenced example text. Static evidence does not claim native
  prompt-load measurements or change business evidence gates.

- Add S3's narrow iteration-candidate capture rule and a fictional backlog/Card
  example: two independent same-mechanism corrections record a future candidate,
  repeated reminders do not count, duplicates retain their scope and priority,
  and capture grants no implementation or publication authority. Reuse the
  existing learning template without an automatic rule rewriter; required
  project-learning promotion and Major approval remain intact.

- Add S2 selection evidence to four existing isolated Superpowers routing
  probes: ordinary-question bypass, proposal-only, compact Direct Change,
  and explicit method requests without Git or completion authority. Record
  bounded selection reasons, reject missing/mismatched records, and preserve
  the legacy six-field route schema. Probes use gpt-6.1-sol/high; Router rules
  and default-loaded Skill bodies are unchanged.

- Add the bounded S1 skill-iteration entry, persistent backlog/current/log,
  and one-round repository Git lease. Validate its routing, Major approval
  guard, and repository-only push scope; synchronize the portable entry to
  Codex, Pi, Antigravity CLI, and Grok CLI. S2–S8 remain backlog items, with
  S7/S8 awaiting separate Major proposals and approval.

- Keep authorized same-scope work moving, name the blocking skill rule when
  pausing, keep default prose plain, and keep tests proportional to the change.
  OpenSpec, evidence signoff, and completion gates are unchanged.

- Add a generated, byte-identical
  `skills/openspec-superpower-change/SKILL.md` compatibility adapter for nested
  catalog indexers, with fail-closed generation/validation and explicit
  asynchronous search-visibility guidance.
- Add Pi/npm package metadata, skills.sh and SkillsMP discovery guidance, and
  a generated skill-only Codex plugin adapter with package-boundary and source
  parity validation.
- Add schema-6 role-first Reviewer Assignments with structured purpose and
  independence, four-product executor/reviewer eligibility, frozen schema-4/5
  legacy audit, and Codex-instance-bound canonical authority.
- Add Pi as the fourth required portable/runtime target, upgrade the managed
  governance block to version 6 (`CCG-001` through `CCG-016`), and add durable
  target-local transaction receipts, recovery, discovery, and verify-all gates.
- Add six isolated natural Review-routing forward cases with private oracles and
  sanitized mode-`0600` evidence.

- Make Codex `superpowers:using-superpowers` explicit-only while keeping its
  complete body available to explicit invocation and leaving Router-required
  child Skills implicit until native nested loading is proven.
- Give the Router sole zero-or-more Superpowers method selection for governed
  work; explicit method requests grant no workflow, business, Git, or completion
  authority, cyclic selection is blocked, and ordinary questions bypass the
  meta-entry. Strengthen portable `CCG-014` and managed-rule version 5; report
  prompt load as `UNKNOWN` when no supported path/hash trace exists.

- Add one Router-owned Completion Contract for whole-task success, evidence,
  stop conditions, learning/OpenSpec reconciliation, cross-CLI sync,
  Git/publication authority, and residual risk.
- Replace independent completion checklists with validated pointers while
  retaining slice- and batch-specific evidence rules.
- Add a static prompt-collision scenario catalog for proposal-only routing,
  material brainstorming, unauthorized/authorized Git plans, and selected
  HARD-GATE preservation; runtime forward-test evidence is tracked separately
  and the catalog is not treated as behavioral proof.

## 0.6.0 - 2026-07-15

- Add a conditional Domain Context Check before material-choice routing; clear
  work stays lean while unresolved language enters `grill-with-docs` or the
  complete portable Discovery First fallback.
- Add Project Learning Closeout with automatic project-local promotion after
  independent correction/Review evidence or one high-severity event.
- Make explicit archive-and-distill requests audit the whole task and promote
  every confirmed project-local key point before final completion.
- Keep `CONTEXT.md` glossary-only, route engineering traps to project guidance,
  and require deterministic regression tests/validators when practical; prose
  or a chat summary cannot substitute for executable enforcement.
- Add managed invariant `CCG-015`, manifest version 4, a portable Candidate Card
  template, qagent-shaped regression fixture, validators, and cross-CLI tests.
- Expose archive/distill routing in Skill frontmatter and bind closeout/template
  rules to their owning artifacts so relocation cannot produce a false PASS.
- Promote this change's own review lesson into project engineering guidance and
  deterministic regressions; synchronize and verify 37 portable files on each
  required Codex, Antigravity, and Grok runtime.

## 0.5.0 - 2026-07-15

- Route governed work through phase-aware Gate 0 classification before broad
  Superpowers metadata, using managed invariant `CCG-014` and manifest version 3.
- Add the `proposal-only` path, allow only explicit bounded assumptions, and
  require brainstorming with its intact HARD-GATE for material choices,
  including choices the user delegates to the agent.
- Keep approved implementation planning, TDD, Preflight, Review, evidence, and
  verification gates unchanged, independent of model identity or version.
- Make companion standalone Review explicit and request-scoped, findings-first,
  and non-automatic after OpenSpec artifact generation.
- Verify 117 router tests with zero skips, 72 companion tests, durable 5/5/25
  forward evidence, and all three declared runtime targets with 12 installed
  validators and target-appropriate discovery checks.
- Treat the first shared-workspace S2 result as invalid harness contamination,
  not a product bug. After reset, fix the real delegated authentication/
  compatibility brainstorming bypass, add regression coverage, and pass Review.
- Replace the earlier non-durable five-scenario behavior summaries with fresh
  per-scenario resets and 25 persisted evidence files.
- Record completed OpenSpec archival, post-archive strict validation, final High
  Review, verified temporary-resource cleanup, and separately authorized
  Router/Companion publication; retain Superpowers upstream reconciliation as a
  residual boundary.

## 0.4.0 - 2026-07-11

- Add stable High/Medium/Low capability profiles without binding authority to
  concrete model names.
- Upgrade new external contracts to schema 5 and schema-2 evidence with
  product/instance/role/profile separation and active schema-4 drain gating.
- Add layered authorization, hash-bound Confirmation Leases, decision
  provenance, governed Learning Candidates, and High mechanism Review.
- Upgrade the managed governance block to version 2 (`CCG-001` through
  `CCG-013`) and keep runtime publication separately authorized.

## 0.3.0 - 2026-07-11

- Upgrade external collaboration to schema 4 with immutable executor,
  independent-reviewer, and Codex decision-owner identities.
- Add allowlisted Codex, Antigravity CLI, and Grok CLI synchronization with
  atomic rollback, first-install support, deterministic discovery, and parity checks.
- Add the versioned `CCG-001` through `CCG-008` shared governance block while
  preserving every CLI-native rule outside the managed markers.
- Block completion on required-runtime drift and reject sensitive categories,
  unsafe paths, symlinks, non-regular files, or tampered sync plans.

## 0.2.0 - 2026-07-10

- Add Plan/Brief Preflight Review and an explicit OpenSpec-aware Superpowers adapter.
- Upgrade external Handoff state to schema 3 with hashed evidence references and sequential final gates.
- Reject blank verification/blocker values, boolean integers, and readonly-field drift.
- Add runtime role/result/batch/attempt/source-fingerprint manifests, transition
  history validation, and OpenSpec task/archive closeout rules.
- Strengthen adversarial routing/lifecycle tests and standalone-clone compatibility.
- Add caveman output-compression boundary: keep caveman as a presentation-only mode and
  prevent governance/closure fields from being compressed away.

## 0.1.0 - 2026-06-22

- Initialize `openspec-superpower-change` as a standalone open-source skill project.
- Define the project as an AI development change gate rather than ordinary SDD.
- Add core references, examples, templates, and design documents.
