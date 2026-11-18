# Document Caveman README Integration Design

Date: 2026-07-16
Mode: Direct Change / compact

## Goal

Document the already-implemented Caveman output-compression boundary in both
open-source skill projects so users can understand when it activates, what it
may compress, and which governance artifacts must remain complete.

This change is documentation-only. It does not change skill triggers, routing,
approval, evidence, lifecycle, completion, or runtime behavior.

## Files

- `openspec-superpower-change/README.md`
- `openspec-superpower-change/README_cn.md`
- `codex-brief-antigravity-review/README.md`
- `codex-brief-antigravity-review/README_cn.md`

## Placement

Add one standalone section after project positioning/role boundaries and before
the main workflow:

- English: `Caveman Output Mode`
- Chinese: `Caveman 输出压缩模式`

This placement makes output style visible before readers interpret workflow
examples, without mixing presentation concerns into routing or evidence rules.

## Shared Content Contract

Both projects explain:

1. Caveman is a presentation/output-compression layer, not a governance layer.
2. It activates only after an explicit request such as `caveman`, `少 token`,
   `更短`, or `更精简`.
3. Base mode supports `lite`, `full`, and `ultra`; `stop caveman` or `正常模式`
   disables persistent compression.
4. Technical terms, paths, commands, error strings, and required fields remain
   exact even when surrounding explanation is compressed.
5. `caveman-commit`, `caveman-review`, and `caveman-compress` are specialized
   tools for commit messages, review comments, and memory files; they do not
   grant workflow authority.
6. Include short copyable activation, level-switching, and stop examples.

## Router-Specific Boundary

The router README allows compression for Gate 0 summaries, routing verdicts,
findings, risk summaries, and verification explanations.

It explicitly forbids compression from removing or rewriting required content
in OpenSpec proposals, Handoff Contracts, evidence manifests, state
transitions, final-verification/final-Review evidence, critical commands, or
sensitive-data warnings. OpenSpec, Superpowers, Review, and completion gates
remain unchanged.

## Companion-Specific Boundary

The companion README allows compression for Standalone prompt/Brief/checklist
wording, findings-first summaries, and user-facing explanations.

Canonical Handoff state and governed Brief/Report/Review artifacts continue to
use their standard templates. Compression may not remove lifecycle state,
artifact paths, evidence roles/results, instance bindings, revision numbers, or
SHA-256 constraints. Batch promotion and final handback rules remain unchanged.

## Language Parity

English and Chinese sections must carry the same triggers, supported modes,
allowed content, forbidden content, specialized-skill distinctions, and
examples. Wording may be idiomatic rather than byte-identical.

## Validation

Run after editing:

1. English/Chinese keyword and semantic-parity checks.
2. `git diff --check` in both repositories.
3. Router quick validator, core validator, and unit tests.
4. Companion quick validator, template validator, and unit tests.
5. Confirm only README files plus this approved design artifact changed.

README and design-history files are repository-only surfaces, so this change
does not trigger cross-CLI runtime synchronization.
