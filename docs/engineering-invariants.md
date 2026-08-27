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
