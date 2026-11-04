# Engineering Invariants

## Project learning must be entry-discoverable and artifact-bound

Scope: project workflow, skill routing, completion gates, and their validators.

Invariant:

- A mandatory closeout path must be discoverable from the skill frontmatter in
  a fresh session; instructions available only after loading the skill cannot
  establish an unconditional trigger.
- Each portable governance artifact must own and validate its own responsibility
  boundary. A validator must not concatenate unrelated files in a way that lets
  required rules move into the wrong artifact while validation still passes.
- An explicit request to archive and distill a session triggers project-learning
  audit and promotion before completion. A chat summary is a reference to the
  durable result, never its only storage.
- Mechanically enforceable workflow invariants require a deterministic negative
  regression that rejects the previous wrong assumption.

Counterexample: `project-learning-closeout.md` is replaced with a placeholder
while its text is appended to a Candidate Card template, and a concatenation-
based validator still returns PASS. This is a false PASS even though every
required phrase still exists somewhere in the portable file set.

Loading pointer: agents read this file through `AGENTS.md`; executable policy
and completion order remain canonical in `SKILL.md` and
`references/project-learning-closeout.md`.

## Hashed Review lineage must parse the exact verified artifact bytes

Scope: Plan/Brief Preflight lineage, parent Review evidence, and semantic
regression fixtures.

Invariant:

- Hashed Plan/Brief lineage applies only when the risk profile requires a
  standalone Preflight artifact. Compact inline readiness creates no synthetic
  lineage solely for bookkeeping.
- One unchanged contract has at most one full Preflight and one terminal
  focused recheck. Same-scope implementation findings do not restart lineage;
  a protected-boundary change requires a newly authorized full Review.
- A historical revision may be anchored by an immutable parent Review instead
  of requiring old bytes to remain at a mutated current path.
- The parent Review's root revision and reviewer identity must be parsed from the
  exact bytes whose whole-file SHA-256 was verified. Hashing one path read and
  parsing a later read permits replacement between checks and is a false PASS.
- Every project-relative reference must be opened beneath the bound project root
  without following symlinks in any directory or leaf component. A final-leaf
  `O_NOFOLLOW` check alone does not prevent an intermediate-directory escape.
- Current reviewer identity must exactly match the parent Review and remain
  distinct from author and executor identities.

Counterexample: validation hashes `reviews/root.md`, another process replaces it,
and the checker reopens the path to parse attacker-chosen root/reviewer fields.
A second counterexample routes `reviews/` through a symlink outside project root
while only the final file is checked as regular.

Mechanical enforcement: the focused Preflight semantic fixture performs
single-descriptor hash/parse binding, descriptor-relative no-follow traversal,
and negative tests for parent-content drift, leaf/intermediate symlinks, and
reviewer replacement or identity reuse.

Loading pointer: agents read this file through `AGENTS.md`; the normative Review
contract remains in `references/approved-implementation-workflow.md`.

## Validation fixtures must be valid in every supported parser mode

Scope: YAML-backed workflow contracts and tests for the dependency-free parser
fallback.

Invariant: a fixture used by both PyYAML and the fallback parser must be valid
standard YAML after contract-marker/fence extraction. Run the affected test
suite once with an interpreter that provides PyYAML and once with the supported
dependency-free interpreter. A fallback-only PASS cannot prove parser parity.

Counterexample: a fenced contract closes with four backticks. The fallback
scalar parser ignores the stray backtick, while PyYAML rejects it, so validation
passes in one worktree interpreter and fails after cherry-pick in another.

Loading pointer: the dual validation requirement is declared in `AGENTS.md`;
this invariant explains why both paths are mandatory.

## External CLI debug traces remain temporary sensitive evidence

Scope: external CLI forward tests, discovery probes, runtime-sync
investigations, and their durable evidence.

Invariant:

- External CLI debug traces are temporary evidence because they may embed
  runtime authentication material, private prompts, session data, or other
  native CLI state even when the requested probe is read-only.
- Mode `0600` and a private temporary directory reduce exposure while a trace
  is needed; they do not make its content safe for durable promotion.
- A raw trace must not be quoted or echoed, copied into repository artifacts,
  or used as the persistent evidence object. Durable evidence retains only the
  minimum sanitized path/hash/result metadata needed to support the claim.
- After the source, runtime, forward-test, and Review gates no longer need the
  trace for rollback or investigation, remove the raw trace after final gates.
  If closeout is blocked, record the cleanup owner and resume condition instead
  of silently retaining it.

Counterexample: an agent stores a mode-`0600` CLI debug log in `/tmp`, searches
it for a Skill path, and then echoes matching raw lines into a Review. The file
permission limited filesystem access but did not redact authentication material
embedded in those lines.

Mechanical enforcement: the project test suite rejects raw `.debug.log` and
`.debug.jsonl` files under durable documentation, OpenSpec, or reference roots
and pins the handling rule in this entry.

Loading pointer: agents read this file through `AGENTS.md`; task plans may name
the exact temporary trace and cleanup checkpoint but must not duplicate or
weaken this invariant.

## Public distribution paths must remain symlink-bound

Scope: npm package allowlists, generated Codex adapters, and local release
artifacts derived from this repository.

Invariant:

- Every public distribution source and allowlist entry must be a regular file
  below its bound root without following symlinks in an intermediate directory
  or leaf component.
- A generated adapter output must remain below the repository root, reject
  symlinks anywhere in an existing generated tree, and bind the existing
  output directory identity again immediately before replacement.
- The npm dry-run file set must equal the explicit public allowlist expansion;
  a validator PASS cannot rely on `exists()` or `is_file()` following a symlink
  that npm silently omits.

Counterexample: `references/` or `distribution/codex-plugin/.codex-plugin/` is replaced by
a symlink to an outside directory. A final-file check follows it, copies or
deletes outside content, and reports a successful package or adapter build.

Mechanical enforcement: `scripts/build_codex_plugin.py` reuses
`validate_cross_cli_sync.validate_relative_path`, rejects output-parent and
existing-tree symlinks, and rechecks the output inode before replacement.
`scripts/validate_distribution.py` expands allowlists without following
symlinks and compares `npm pack --dry-run --json` with the expected file set;
`tests/test_distribution.py` contains negative regressions for each boundary.

Loading pointer: this guidance is loaded through `AGENTS.md`; the executable
details remain in the named builder, validator, and tests.

## Behavioral forward proofs must audit native events

Scope: external CLI behavioral forward tests, Skill-load probes, and any claim
that a result was produced without shell, filesystem, or tool fallback.

Invariant:

- A behavioral proof must audit the native event stream with a fail-closed
  allowlist. A read-only sandbox and an unchanged file snapshot prove only that
  no mutation occurred; they cannot exclude read-only fallback.
- Any tool, command, file, or MCP event invalidates a no-tool proof even when
  the final classifier, marker, or schema-constrained object is correct.
- Unknown event types, invalid JSONL, missing completion, or an unavailable
  supported event stream fail closed. Persist only sanitized counts and hashes,
  never raw events or message text.

Counterexample: a probe shell-reads `SKILL.md`, returns a marker-perfect answer,
and leaves the project snapshot unchanged. A marker-only classifier reports
PASS even though native Skill loading was never established.

Mechanical enforcement: the routing forward runner rejects non-message and
non-reasoning JSONL item types, and the project test suite supplies a
marker-perfect command event that must fail.

Loading pointer: agents read this file through `AGENTS.md`; forward-test plans
must bind the event-audit mechanism and sanitized evidence before claiming a
no-tool result.

## Reviewed runtime plan binds destination pre-state

Scope: cross-runtime synchronization, managed global-rule replacement, and
other reviewed plans that write existing or expected-absent destinations.

Invariant:

- A reviewed runtime plan binds destination pre-state as well as source
  identity. Source hashes alone cannot authorize overwriting whatever bytes
  happen to exist when apply begins.
- A schema-v2 managed global rule also binds its destination to the
  target-specific canonical runtime root derived from the validated `skills_root`;
  the serialized destination cannot redefine that root. Coherent destination and
  pre-state retargeting must fail before candidate or backup creation.
- Every destination and global rule records its reviewed hash, mode, or absence.
  Apply checks the complete target immediately before any backup or write; any
  pre-state drift aborts the target before mutation.
- Rollback must restore the reviewed hash, mode, or absence and verify that
  restoration. Later targets remain blocked after a target failure.

Counterexample: a reviewed plan contains only source hashes. Another process
changes a destination before apply, which then backs up and overwrites the new
bytes; its rollback restores the apply-time drift rather than the state the
reviewer authorized.

Mechanical enforcement: the sync planner records per-file and per-rule
pre-state, derives and validates the canonical managed-rule destination for
schema-v2 plans, apply checks it twice before the transaction, and deterministic
tests cover existing-file drift, absent-to-created drift, forced-failure rollback,
and coherent managed-rule destination/pre-state tampering.

Loading pointer: agents read this file through `AGENTS.md`; executable sync
behavior remains canonical in `scripts/validate_cross_cli_sync.py` and its
tests.

## Bound cleanup must preserve object identity across namespace transitions

Scope: cross-CLI candidate persistence, quarantine, recovery, and cleanup on
filesystems without an inode-bound deletion primitive.

Invariant:

- A final ownership check binds an object identity, not a pathname. Every later
  quarantine, recovery, rewrite, and deletion step must preserve that identity
  through a retained descriptor or an equivalent exact-owner primitive.
- A name-based unlink or reopen after the final check is not exact-owner
  cleanup. If the host cannot provide inode-bound deletion, fail closed: keep
  visible mode-0600 recovery/blocker evidence, preserve unrelated replacement
  inodes, and rewrite any retained PASS-shaped evidence through the already
  validated writable descriptor.
- A successful-looking recovery must never leave canonical JSON `verdict: PASS`
  evidence visible after an ownership or deletion uncertainty.

Counterexample: a quarantine name is replaced after its retained inode was
validated. Name-based deletion removes the unrelated inode, or a Pi retained
inode remains valid `PASS` evidence while recovery reports only `BLOCKED`.

Mechanical enforcement: `scripts/validate_cross_cli_sync.py` owns the
descriptor-bound seam and fail-closed fallback; deterministic regressions at
`tests/test_cross_cli_sync.py:1241-1299` and `:2540-2621` inject final-bind
replacement and assert unrelated-inode preservation, retained-descriptor
BLOCKED rewriting, mode-0600 blockers, and no JSON `PASS` residue.

Loading pointer: agents read this file through `AGENTS.md`; the production
cleanup path and focused regressions are the executable authority.

## Irreversible cleanup commit points have no rejecting tail

Scope: generated-adapter replacement and transactional cleanup which deletes
the final recoverable link to prior bytes.

Invariant:

- Complete every fallible identity, content, closure, and compensation check
  before deleting the final prior-state link.
- The successful deletion of that link is the commit point. Publish committed
  state immediately; later directory inspection, close, or removal is
  best-effort and cannot convert the committed operation into a recoverable
  failure claim.
- A failure before the commit point must preserve or exactly restore prior
  bytes. A failure after it must not enter compensation which falsely assumes
  those bytes still exist.

Counterexample: cleanup unlinks the recovery `SKILL.md`, then rejects because a
concurrent process inserts another directory entry before `rmdir`. The builder
reports failure and attempts compensation even though the only exact prior copy
has already been destroyed.

Mechanical enforcement:
`tests/test_distribution.py::DistributionTests::test_skillsmp_builder_residue_between_recovery_unlink_and_rmdir_cannot_reject`
injects that race. `scripts/build_skillsmp_adapter.py` marks the recovery unlink
as commit and makes its remaining cleanup non-rejecting.

Loading pointer: agents read this file through `AGENTS.md`; the executable
commit boundary remains in the named builder and regression.

## Native consumption and evidence qualification stay scoped

Scope: shared governance, actual-account/native consumer audits, plan/report
placement and four-target synchronization.

Invariant:

- A portable product snapshot and a native entry are different evidence scopes.
  Record actual config root, launcher, instruction source, discovered skill
  paths and dependency hash. Missing private copies cannot disprove shared
  discovery; another account's parity cannot qualify native loading or behavior.
- Content reuse does not expand formal products, instances or authority.
  Claude launchers keep the Claude Code product, and a publisher cannot confer
  a schema-6 role or rewrite already-bound attempt evidence.
- Required plans exist before execution at their bound/project-selected paths.
  Native fallback directories never relocate or duplicate immutable evidence.
  Standalone advisory defaults to chat; persistence returns to classification.
- Compact-local inline readiness is not a compact-external Preflight waiver.
  Managed CCG-004/014 own their complete paragraphs; a correct prefix followed
  by a contradictory waiver must fail. Native policy belongs in its checkpoint
  section; another artifact, hidden comments or fenced examples cannot supply it.
- Evidence hashes bind the exact consumed bytes. Read source and fixture inputs
  once; decode, project and hash that same snapshot. A later pathname read may
  describe replacement content that never entered the observed run.
- A probe lifecycle is part of acceptance. Restore signal handlers on cleanup
  failure and report success only after owned-directory cleanup succeeds;
  a printed success followed by a cleanup exception is not a passing command.
- Behavioral proof describes its actual instruction-delivery mechanism. Native
  Codex consuming projected project AGENTS is not proof of Skill-body loading,
  other native agents or seven-entry acceptance. Raw events stay temporary;
  sanitized enum/audit/hash results retain these limitations.

Counterexamples: an empty account-specific skill folder is labeled unavailable
while the catalog lists shared skills; a publisher assigns itself Codex identity;
CCG-004 has a valid prefix followed by a compact-external waiver; policy moved
into an adapter still passes a concatenation-based checker; a no-tool classifier
is reported as native Skill loading across seven agents.

Mechanical enforcement: `NativeConsumptionManagedRulesTests` invokes the real
managed-body validator for universal Preflight, missing advisory and contradictory
waiver mutations. `NativeAgentConsumptionTests` invokes owner-bound consumption
checks and rejects hidden/moved clauses, extra classifier fields and invalid
native events. Its preparation replacement tests bind hashes to projected/read
bytes; CLI cleanup tests cover arbitrary caller names and failure without PASS
publication. The seven-case native runner reports only its projected-instruction
scope and never upgrades that evidence to native Skill loading.

Loading pointer: `references/local-instruction-checkpoint.md` (Native agent
consumption), reachable from SKILL's existing affected-instructions row; existing
adapter and synchronization references point to this same owner.

## Authorization, evidence freshness and presentation are separate checks

Scope: approved continuation, confirmation leases, compact slice signoff and
bounded cloud advisory review.

Invariant:

- Ask again only when the actual action, target, scope, conditions or actor is
  not covered. A protected category still needs its explicit authority; its
  name alone does not invalidate authority already granted for that action.
- New approval leases bind the immutable approved decision, not a mutable
  execution Plan. Preserve every historical exact binding. Refresh stale
  implementation evidence without relabeling it as a changed user decision;
  changed approved assumptions or contract bytes still invalidate reuse.
- A closed gate forbids advancement, not authorized same-scope remediation.
  Existing reviewer independence and convergence limits remain binding.
- Compact evidence may be inline only when every required fact and regression
  check is present and the existing risk/contract allows compact reporting.
  A table adds no evidence. High-risk/full-contract reporting is not compact.
- Bounded CC advice is an evidence input. Local adjudication and formal reviews
  still decide acceptance; an accepted send, idle terminal or advisory verdict
  never establishes formal PASS.

Counterexamples: asking the user to repeat an exact approved normal push;
silently re-signing a legacy Plan-bound lease after editing that Plan;
accepting stale verification because authorization remains valid; rejecting
complete eligible inline evidence solely for lacking a table; accepting CC
advice as final completion.

Mechanical enforcement: the production-lease and stale-resume tests in
`tests/test_workflow_rules.py` exercise exact bindings, authority, invalidation
and separate implementation fingerprints. Natural-language routing and
evidence sufficiency additionally need fresh-agent adversarial review: keyword
presence cannot establish a model's decision. The matched forward record
proves the observed compact-table regression without inventing baseline
failures for cases the old rules already handled correctly.

Loading pointer: this file is linked from AGENTS. Normative owners remain
`SKILL.md`, `references/confirmation-lease.md`,
`references/approved-implementation-workflow.md`,
`references/step-evidence-gate.md` and
`references/local-instruction-checkpoint.md`.

## Approved copy boundaries and closure facts stay distinct

Scope: packaged skill copies, portable sync selection, evidence writeups,
runtime refresh, and a user-ordered delivery close for this repository.

Invariant:

- A shorter packaged copy keeps the sentence approved for that copy. A
  continuation present only in the canonical long file is not copied across.
- Portable sync selects only the approved artifact. Text that lives outside
  the managed governance block is not selected into that block. A pre-existing
  symlink of an instruction file is not a managed-block copy and is not repaired
  by breaking the link.
- A local refresh compares each destination with the published bytes. A
  destination that already matches stays. A destination newer than the
  published commit, when it still matches the current worktree, stays in place.
- Evidence counts a completed record of one item type once. A scripted non-zero
  exit is the scenario's reported stop, not a measured wall-clock timeout.
- An advisor patch is applied only when its end marker names the current task
  and the hash matches those bytes.
- When the user orders the delivery loop closed, perform the remaining
  user-gated record they named. Do not answer again with an open risk whose
  only cause is that this ordered step is still undone. That order does not
  relabel advisory review as control-plane PASS, does not set learning status
  to `promoted`, and does not authorize Git. An unrelated hunk in a shared
  file stays out of that authorized commit.

Counterexample: the long-file continuation is inserted into both short
`SKILL.md` copies; started and completed command events are added together; a
patch whose end marker names the previous task is applied; after the user asks
how to close, the reply repeats an open risk without doing the ordered check;
published bytes are copied over runtime files that are newer than that commit.

Mechanical enforcement: `tests/test_workflow_rules.py` rejects the long-file-only
continuation in both packaged short copies and rejects the user-owned round-budget
marker in the live skill copies and the managed governance source. Runtime trees,
native event logs, advisor envelopes, and the Git index have no deterministic
in-repo fixture; those comparisons use the adversarial scenarios on the
2026-11-02 candidate card.

Loading pointer: agents read this file through `AGENTS.md`. Approved long and
short sentences remain in the published `SKILL.md` copies and
`openspec/changes/archive/2026-11-02-add-verify-anti-drift-round-budget/`.
This section does not restate user-owned round-budget text.

## Hanging states, completion deadlocks, and delegated review continuity resolve deterministically

Scope: Gate 0 task type classification, public environment budget fallbacks, pre-existing debt transitions, bounded completion loops, and delegated advisory review.

Invariant:

- A task-type stop condition requires an immutable objective baseline recorded at Gate 0. An agent must not infer a task-type transition without that recorded state.
- Numeric round budgets remain private user configuration. In public or distributed runtimes lacking private instructions, numeric limits are skipped gracefully, while physical boundary, new root cause, advisor-repeat, and two-failure stops remain binding.
- A pre-existing failure (`OUT_OF_SCOPE_PREEXISTING_DEBT`) must never enter self-repair under the current task. It must transition deterministically to `BLOCKED`, `blocker_owner: user`.
- The two-failure stop in `SKILL.md` bounds all `fix -> verify -> Review` loops across re-entries in `completion-contract.md`. Reading completion contracts at closure cannot override that bound into an infinite live-lock.
- When the user explicitly instructs closed-loop execution or delegates intermediate approvals to an advisory reviewer, establishing review/verification PASS evidence satisfies that intermediate gate and advances immediately to the next slice without pausing for human conversational confirmation.

Counterexample: Gate 0 lacks task classification, so an agent halts arbitrarily on perceived task changes; missing local budget numbers cause the agent to invent limits or fail validation; an out-of-scope failure sends completion into an infinite repair loop; an agent repeatedly asks the user for polite permission to continue after delegated advisory review already gave PASS evidence.

Mechanical enforcement: `tests/test_workflow_rules.py` tests Gate 0 task type presence, budget fallback text, pre-existing debt `BLOCKED` transition, two-failure completion bounds, and delegated review continuity, along with negative mutation regressions.

Loading pointer: agents read this file through `AGENTS.md`. Normative owners are `SKILL.md`, `references/step-evidence-gate.md`, `references/completion-contract.md`, `references/confirmation-lease.md`, and `references/approved-implementation-workflow.md`.

## Plan-anchored cohesive execution, lazy state, and commit-style parity

Scope: OpenSpec/Plan four-anchor unification, coarse-grained cohesive batch execution, three-condition bugfix Direct Change, lazy `status.md` and `verified_revision.inputs` hygiene, in-place cold-path partitioning, deprecated advisor cleanup, and authorized Git commit message conventions.

Invariant:

- When an approved OpenSpec `design.md` and `tasks.md` already define the Four Hard Anchors (allowed/forbidden file scope, `path:line` interface facts, coarse-grained cohesive batches, and exact regression commands), they serve directly as the executable Plan without requiring a duplicate Superpowers `implementation-plan.md` or standalone local `preflight-full.json` / `preflight-focused.json` files on a clean baseline.
- Execution defaults to coarse-grained cohesive business batches (`Single Cohesive Batch` for single-slice changes). Inside an approved batch, the executor iterates freely on implementation and tests without standalone `red-green.json` or `native-green.json` files, recording a concise inline RED-to-GREEN proof (failing test name, non-zero exit code, and one-line failure summary before the fix, followed by exit code `0`) in a single consolidated Verification & Review report.
- A localized bugfix restoring intended behavior may use Direct Change without a pre-existing spec path when backed by a failing-then-passing regression test, no external API/schema/permission/lifecycle change, and scope bounded by the local diff.
- Local `compact` and `standard` changes create `docs/agent-collab/<change-id>/status.md` lazily only before an intentional stop, compaction, or cross-window/external handoff; local `strict` and `self-evolution` changes create `status.md` at approval and refresh at review/completion boundaries rather than every micro-step. Exclude `CHANGELOG.md`, task ledgers, and historical Review/Evidence reports from `verified_revision.inputs` so closeout edits never trigger self-hash invalidation loops.
- `references/approved-implementation-workflow.md` partitions its everyday execution trunk from cold-path recovery sections (`Project Session Resume`, blocked-context amendment, control-plane rebind/return) via `<!-- COLD_PATH_START` in place rather than adding extra portable manifest files.
- Before executing an authorized `git commit`, always inspect `git log` to match the repository's established commit message convention (Chinese `type(变更门禁): summary` plus structured bullet points for multi-file governance changes) rather than defaulting to a terse one-line English subject.

Counterexample: an agent writes duplicate `implementation-plan.md`, `preflight-full.json`, `red-green.json`, and `native-green.json` files for a single-slice local change; includes `CHANGELOG.md` and review reports in `verified_revision.inputs` so updating closeout evidence invalidates the verified revision seventeen times; splits `approved-implementation-workflow.md` into a new file that breaks 40+ routing assertions; or commits a 24-file architectural change with a one-line English commit message ignoring `git log` history.

Mechanical enforcement: `tests/test_workflow_rules.py:SkillIterationEntryTests.test_streamline_plan_anchored_execution_invariants` and `test_delegated_review_and_closed_loop_continuity` verify the four-anchor rule, cohesive batch inline RED-to-GREEN proof, three-condition bugfix Direct Change, `verified_revision.inputs` exclusions, `<!-- COLD_PATH_START` marker, `grok-cc` removal, and negative mutation regressions. Commit-style parity is verified via adversarial Review scenario on the 2026-11-04 candidate card.

Loading pointer: agents read this file through `AGENTS.md`. Normative owners are `SKILL.md`, `references/approved-implementation-workflow.md`, `references/direct-change-rule.md`, `references/step-evidence-gate.md`, and `references/completion-contract.md`.

## Dual-mode headless cross-review, validator-delegated next-action query, and post-receipt closeout recording

Scope: `pi -p` / `agy -p` headless CLI cross-verification, read-only tool boundaries, `scripts/next_action.py` transition probing via `scripts/validate_core_gates.py`, static Plan checkbox preservation, and closeout report SHA-256 / review-receipt integrity.

Invariant:

- When a distinct `independent-reviewer` instance is required and local Headless CLI (`pi -p` / `agy -p`) is available, the executor invokes the independent reviewer session directly by default (chaining `FULL_PREFLIGHT -> Fix -> FOCUSED_RECHECK` and `Review -> Fix -> Verify -> Review` up to circuit breakers) and falls back to a copyable Review Prompt only when requested by the user or blocked by CLI timeout/rate-limit/interaction. Headless review invocations must enforce a verifiable read-only boundary (`pi --tools read,grep,find,ls` without `bash`/`edit`/`write`; `agy --effort high -p` without default `--dangerously-skip-permissions`; plus before/after workspace snapshot checks).
- Read-only sibling queries such as `scripts/next_action.py` must import transition and owner tables (`ALLOWED_TRANSITIONS`, `STATE_TUPLES`, `NEXT_OWNERS`, `EXPECTED_OWNERS`, `ARTIFACT_FIELDS`) and delegate transition legality exclusively to `validate_transition` via `probe_transition_candidate` in `scripts/validate_core_gates.py`, never re-implementing batch-count or tuple-state conditionals.
- Closeout reports must record exact 64-character SHA-256 digests computed from disk bytes (`shasum -a 256`), keep Plan checkboxes static (`[ ]`), and never pre-record a reviewer's `PASS` before that reviewer's final signoff receipt arrives.

Counterexample: a headless review command passes `--dangerously-skip-permissions` or `--tools bash` as a default "read-only" flag; `next_action.py` writes its own `_is_transition_applicable` checking `current_batch == planned_batches`; or a closeout report extrapolates a 12-char hash prefix or marks an in-flight reviewer as `PASS` before the re-review completes.

Mechanical enforcement: `tests/test_workflow_rules.py:ClosedLoopRuntimeRoutingTests.test_dual_mode_headless_cli_cross_review_and_closed_loop_chaining` and `tests/test_next_action.py:NextActionQueryTests` (`test_imports_single_source_of_truth_from_validate_core_gates`, `test_transition_decisions_delegate_exclusively_to_validate_transition`) enforce dual-mode routing and zero duplicated transition logic.

Loading pointer: agents read this file through `AGENTS.md`. Normative owners are `references/agent-capability-routing.md`, `references/approved-implementation-workflow.md`, `scripts/validate_core_gates.py`, and `scripts/next_action.py`.
