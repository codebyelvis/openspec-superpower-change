# Project Learning Closeout

Use this reference after implementation Review produces correction/finding
history, and whenever the user asks to archive and distill a completed session.
It promotes reusable project knowledge before the workflow claims completion.
The independent ownership subsection also applies before ordinary document work.

## Project Document Ownership

Apply this subsection before creating or relocating an ordinary project document.
Reading ownership alone does not trigger learning promotion; the existing
Triggers, Target resolver, enforcement and completion gates still govern learning.

### Destination precedence

1. Respect explicit user/project path contracts first. Inspect task-relevant
   project instructions, navigation and nearby documents for the intended purpose
   or domain; do not require a whole-repository map or inventory.
2. Reuse established purpose/domain conventions, including directories outside
   `docs/` when the project uses them. Directory existence alone is not evidence
   of a convention: look for relevant navigation and existing documents.
3. With no applicable contract or convention, use a suitable purpose subdirectory,
   for example `docs/deployment/`, `docs/engineering/`, `docs/incidents/`, or
   `docs/learning-candidates/`. Do not impose a universal project layout.

Reserve the docs root for index entry points and explicitly contracted files.
Conflicting applicable contracts or equally plausible destinations must be
resolved before writes; file recency and a generic fallback cannot decide them.
For example, an explicit AGENTS link to `docs/engineering-invariants.md` preserves
that root guidance contract even when another project's unconstrained engineering
fallback uses a purpose directory.

### Protected locations and bound references

Preserve the existing location contracts of `AGENTS.md`, `CONTEXT.md`,
`CONTEXT-MAP.md`, OpenSpec artifacts, collaboration state such as
`docs/agent-collab/<change-id>/status.md`, and iteration state under `docs/iteration/`.
Ordinary directory rules never relocate or clone these special artifacts.
Approval, Plan, Review and evidence paths may have exact path/hash bindings;
their existing owner, authorization, revision and evidence rules remain binding.
Document organization grants no migration, re-signing, state-transition or
completion authority over them.

### Authorized relocation and reference closure

Creation authority is not blanket migration authority. Before an authorized
move, enumerate the selected documents, agreed destinations and required
inbound/outbound references, anchors, AGENTS navigation and applicable active
references. Only the currently authorized documents and referring files may
change. An unauthorized required reference or protected bound artifact stops
the operation before any mutation; resolve the scope through the existing gate.

Check destination collision, bound-project paths, ordinary-file operations and
link resolution before moving. Do not overwrite conflicting content, follow
symlinks, escape the bound project or leave unresolved links. Preserve substantive
content except necessary link edits; repair relative links and anchors from the
new directories and authorized navigation. Do not rewrite external URLs or
automatically move unrelated historical documents. Verify actual before/after
file inventories, content and link resolution, including unchanged unrelated
files; an agent's report alone cannot establish these facts.

## Position in the workflow

```text
Implement -> Verify -> Review PASS
-> Project Learning Closeout
-> promote -> verify -> Review learning artifacts
-> fresh final verification -> final Review
-> OpenSpec reconcile/archive and strict validation
-> session archive/distillation summary
```

Run this gate before fresh final verification and before OpenSpec task
reconciliation or archive. If promotion changes executable behavior, return to
the approved implementation/TDD loop; do not hide that change as documentation.

## Triggers

Promotion is mandatory when:

- two independent correction or Review signals establish the same generalized
  project invariant; or
- one high-severity security, integrity, data-loss, or false-PASS event
  establishes it.

Repeated paraphrases of one source are not independent. A user correction and a
distinct reviewer observation may be independent evidence.

When the user asks to archive and distill the session, always run the learning
audit and promote every confirmed project-local key point through the
repository's normal change path even if the automatic threshold was not met.
A chat-only archive is not project promotion.

A single low-risk task-local correction remains in the current Plan, Review, or
session summary. If the audit finds no confirmed project-local candidate,
continue without creating durable documentation noise.

## Target resolver

| Knowledge | Default target | Boundary |
|---|---|---|
| Project-specific domain term, meaning, relationship, or resolved ambiguity | nearest `CONTEXT.md` selected by `CONTEXT-MAP.md`, or a lazily created root `CONTEXT.md` | glossary only; no implementation cause, chronology, task, or solution detail |
| Easy-to-miss implementation or agent operating invariant | contracted or established guidance under Project Document Ownership; otherwise `docs/engineering/engineering-invariants.md` | generalized mechanism, scope, counterexample, and loading pointer |
| Hard-to-reverse, surprising choice with real alternatives | `docs/adr/NNNN-slug.md` | decision and reason only |
| Mechanically enforceable behavior | deterministic regression test or validator | must reject the prior wrong assumption; prose-only evidence is insufficient |
| Candidate provenance | default `docs/learning-candidates/YYYY-MM-DD-<slug>.md` | summarized evidence references; no transcript dump |

When future agents would not discover engineering-invariant guidance, add a
minimal link from the nearest repository agent-instruction file through the
project's normal change path. Do not duplicate the full rule there.

## Durability and Git authority

In a Git repository, canonical context and engineering-invariant artifacts must
not be intentionally ignored. Include active additions/modifications in the
changed-file inventory, but do not infer authorization for `git add`, commit, or
push. If publication remains pending, report that state honestly.

## Candidate evidence and safety

Use `templates/learning-candidate-template.md`. The Codex control plane owns
scope classification, target selection, redaction, promotion, and completion.
External Review findings are evidence inputs, not self-authorization.

Persist only summarized project-relative evidence paths and SHA-256 values when
available. Never persist full chat transcripts, private prompts, credentials,
tokens, customer data, or other sensitive content in Candidate Cards, context,
engineering guidance, or forward fixtures.

## Enforcement and Review

For a mechanically enforceable invariant, add a deterministic regression test or
validator that fails for the prior wrong assumption. If deterministic
enforcement is infeasible, record a non-blank reason and an explicit adversarial
Review scenario. The learning diff still requires focused verification and
Review PASS.

The final completion is `BLOCKED` when a mandatory or explicitly requested
project-local promotion lacks any of:

- classified Candidate Card and non-sensitive provenance;
- correct durable target artifact;
- non-ignored shared knowledge where Git is used;
- deterministic enforcement, or a justified infeasibility fallback;
- focused verification and Review PASS.

The session archive/distillation summary references the durable artifacts and
evidence; it never becomes their only storage location.
