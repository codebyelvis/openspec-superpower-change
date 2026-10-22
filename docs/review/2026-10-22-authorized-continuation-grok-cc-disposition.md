# Cloud advisory disposition

Change: `reduce-redundant-confirmation-and-review-overhead`, approved draft-v2.
Controller: original assigned Codex instance. This records local assessment of
advice, not formal Preflight, implementation verification or Final Review PASS.

## Complete report recovery

The one accepted Claude Code task's existing `advisory.diff` was recovered by
read-only SFTP after the user woke Grok Bot. Strict existing host-key checking
remained enabled; no trust, authentication, network or model configuration was
changed. Original runtime, terminal and process incarnation matched. No new
terminal, repeated model submission or export was used.

The exact recovered diff has SHA-256
`488419b72bd00ffeb3ca21434709274e70425cb44486830f8c6d0f49cbc0c5b7`
and 128 LF bytes, matching the original terminal's completion metadata. A local
envelope was assembled from those already observed task/hash/count markers
around the unchanged file bytes; it is not described as a captured transcript.
Installed `task_packet.py check` passed against the original draft-v2 packet,
including all context prestates and Git apply check. The only output was the
requested new advisory report. The checked report body was then added locally
with `apply_patch`; no suggested source edit was applied.

The report is
`docs/review/2026-10-22-authorized-continuation-grok-cc-advisory.md`.
Its snapshot preceded approval; its pending-approval observations are historical,
not a claim that the later explicit approval is absent.

## Finding dispositions

| Finding | Local evidence and disposition |
| --- | --- |
| P1-1: entry stop clauses / Git authority | Partially confirmed. `SKILL.md` is already an approved edit candidate and Plan Task 2 includes it. Clarify its two broad stop clauses and make coverage checking apply to routed stop clauses too. Preserve both Git Non-negotiables. The user's original instruction was “一起分析后让grok-cc review一轮你闭环推进 优化 推送git 然后本次更新 闭环推进”; subsequent exact change-id approval includes original tasks 3.5, “Commit and push only this change ... origin/main”. Together these are existing specific commit/push authority, not authority inferred from generic continuation or from the new rule. |
| P1-2: Plan versus authorization hash | Confirmed documentation ambiguity. Name the immutable approved OpenSpec/decision artifact in existing `approved_scope` prose for new leases; retain the `decision_source` enum, all exact comparisons and historical bindings. A mutable execution Plan/Brief/status is not substituted for that artifact. Plan corrections still need the required Preflight recheck. Test changed Plan/source bytes versus changed bound approval bytes. No new field or validator is needed. |
| P2-1: evidence assumptions | Confirmed ambiguity. Distinguish changed approved acceptance/evidence assumptions from stale test/Report results after an authorized fix. Keep contradictory evidence and every existing invalidation flag rejecting. Refresh affected evidence; do not treat refresh itself as changed authority. |
| P2-2: Direct Change stop clause | Address within the already approved Router entry. Explicitly apply coverage checking when a route says to stop at a protected boundary: check existing authority and gates, ask only for the missing delta. The direct rule's local-edit exception does not itself authorize publication. Add a Direct Change publication forward probe; keep the direct rule file unchanged and do not widen its classification. |
| P2-3: untested staged tree / dirty hunks | Already addressed by the executable Plan: implement and test a clean base candidate, apply only reviewed owned delta to dirty integration, reject conflicts, and construct the original index from the scoped cached patch. Compare its tree with the tested clean release tree before commit, then verify parent and remote. This does not adopt unrelated dirty work or rely on integration-only results. |
| P2-4: MODIFIED scenario loss | Checked actual clean HEAD and integration baseline; their original requirement blocks are identical. All five scenario titles survive, all five bodies are intentionally rewritten, and three scenarios are added. Detailed mapping below; no silent scenario deletion was reproduced. Preserve approved delta bytes. |
| P2-5: advisory output-only scope | Local acceptance check used the installed `diff_paths` parser, exact new-file headers and one report hunk. Actual report and a zero-finding report fixture accepted; extra source path, existing-file mutation and extra hunk fixtures each rejected as whole patches. This is a task-local transport-boundary probe, not new production Router enforcement. No transport/source edits are authorized. |
| P3-1: compact profile versus presentation | Confirmed terminology risk. Limit inline representation to cases already eligible for compact reporting, independently of profile labels. Keep high-risk/contract-changing/full-request evidence requirements, path:line or path-anchored hunk references and positive/negative checks. |
| P3-2: independent scope check | Existing focused Preflight already requires the same independent reviewer and complete unchanged protected-boundary matrix. Retain it explicitly when describing remediation; do not let controller classification substitute for recheck. |
| P3-3: dispatch count/payload | This authorization covers the one submitted draft-v2 advisory and its existing collection/recovery, not a second changed-payload opinion. No second cloud review is planned. Existing unknown-send/export restrictions remain unchanged. |
| P3-4: future protocol promotion | The approved design labels that section a future recommendation and excludes grok-cc implementation/install/publication. Do not promote its proposed interface as an approved implemented invariant during closeout. Preserve the approved draft instead of moving/editing its bound bytes. Router sync to Grok CLI is not installation of grok-cc. |

These dispositions refine the implementation Plan within the unchanged approved
scope, files, acceptance, risk and authority. They do not amend the four bound
draft-v2 artifacts or claim that planned fixes have already passed validation.

## Original scenario mapping

| Original scenario | Approved delta |
| --- | --- |
| Pending task without blocker | Retains title; replaces task-global blocker wording with the proposed action's missing authority/material-decision predicate; retains no repeat confirmation. |
| Advancing turn requires action | Retains title; compresses action examples into authorized task-related action; summary/future plan alone still is not progress. |
| Canonical resume | Retains title; adds valid assignment and decision reuse. Recovery triggers and no second state system remain in the requirement body. |
| Legal stop condition | Retains title; intentionally distinguishes a blocked transition from independently authorized remediation. Missing authority, evidence/resources, material decisions, scope and user pause/cancel still stop the action. Completed work remains governed by the unchanged Completion Contract; high-risk/irreversible effects retain their required explicit authority and evidence, rather than stopping solely by category. |
| Code has been written but evidence is incomplete | Retains title; compresses the evidence list and explicitly includes Review. The requirement body retains all existing Done mechanisms. |

Added: explicit Review/publication authorization reuse, new-instance assignment
boundary, and missing concrete Major approval. No baseline scenario is silently
dropped, and no high-risk/irreversible authority or completion condition is waived.

## Readiness

The cloud-output dependency D1 now has complete checked evidence and local
dispositions. F1/F2 corrections remain in the Plan. The original independent
reviewer's one terminal focused recheck is still required before implementation;
this document does not grant readiness or rewrite the blocked r1 report.
