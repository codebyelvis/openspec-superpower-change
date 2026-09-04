# Project Learning Closeout

Use this reference after implementation Review produces correction/finding
history, and whenever the user asks to archive and distill a completed session.
It promotes reusable project knowledge before the workflow claims completion.

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
| Easy-to-miss implementation or agent operating invariant | repository-defined guidance, default `docs/engineering-invariants.md` | generalized mechanism, scope, counterexample, and loading pointer |
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
