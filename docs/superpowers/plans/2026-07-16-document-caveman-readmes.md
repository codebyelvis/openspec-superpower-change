# Document Caveman READMEs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Explain the existing Caveman output-compression boundary in both skills' English and Chinese READMEs without changing governance or runtime behavior.

**Architecture:** Add one self-contained section to each README at the boundary between project positioning and workflow. Keep the two languages semantically aligned, specialize the allowed/forbidden compression boundary for each skill, and verify the documentation against existing validators and tests.

**Tech Stack:** Markdown, Git diff checks, Python validation scripts, `unittest`.

---

## File map

- Modify: `/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/document-caveman-readmes/README.md` — router English Caveman contract.
- Modify: `/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/document-caveman-readmes/README_cn.md` — router Chinese Caveman contract.
- Modify: `/Users/elvis/.config/superpowers/worktrees/codex-brief-antigravity-review/document-caveman-readmes/README.md` — companion English Caveman contract.
- Modify: `/Users/elvis/.config/superpowers/worktrees/codex-brief-antigravity-review/document-caveman-readmes/README_cn.md` — companion Chinese Caveman contract.
- Preserve: `/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/document-caveman-readmes/docs/superpowers/specs/2026-07-16-document-caveman-readme-design.md` — approved design and scope record.

### Task 1: Protect the pre-change state

- [x] **Step 1: Confirm repository scope**

Run:

```bash
git status --short
git -C /Users/elvis/.config/superpowers/worktrees/codex-brief-antigravity-review/document-caveman-readmes status --short
```

Expected: the router contains only the approved design/plan additions; the companion is clean.

- [x] **Step 2: Back up the four target files**

Create a uniquely named directory under `/private/tmp`, then copy both READMEs from each repository while preserving metadata.

Expected: four readable backup files exist outside repository discovery.

### Task 2: Document the router boundary

- [x] **Step 1: Add `Caveman Output Mode` to the English router README**

Insert after `How It Fits` and before `Core Workflow`. State all of the following explicitly:

- explicit activation examples: `caveman`, `少 token`, `更短`, `更精简`;
- base levels: `lite`, `full`, `ultra`;
- stop forms: `stop caveman`, `正常模式`;
- allowed compression: Gate 0 summaries, routing verdicts, findings, risk summaries, verification explanations;
- preserved content: exact technical terms, paths, commands, errors, required fields;
- forbidden loss/rewrite: OpenSpec proposals, Handoff Contracts, evidence manifests, state transitions, final-verification/final-Review evidence, critical commands, sensitive-data warnings;
- specialized skills: `caveman-commit`, `caveman-review`, `caveman-compress` do not grant workflow authority;
- copyable activation, level-switching, and stop examples.

- [x] **Step 2: Add `Caveman 输出压缩模式` to the Chinese router README**

Insert after `体系定位` and before `核心工作流`. Carry the same triggers, modes, stop forms, allowed/forbidden boundary, exactness promise, specialized-skill distinction, and examples in idiomatic Chinese.

- [x] **Step 3: Check router language parity and formatting**

Run focused searches for `Caveman`, `lite`, `full`, `ultra`, `stop caveman`, `caveman-commit`, `caveman-review`, and `caveman-compress` in both files, followed by:

```bash
git diff --check
```

Expected: every required term appears in both languages and diff check exits 0.

### Task 3: Document the companion boundary

- [x] **Step 1: Add `Caveman Output Mode` to the English companion README**

Insert after `Role Boundary` and before `Workflow`. State all of the following explicitly:

- the shared activation, level, stop, exactness, specialized-skill, and example contract;
- allowed compression: Standalone prompt/Brief/checklist wording, findings-first summaries, user-facing explanations;
- canonical Handoff and governed Brief/Report/Review artifacts keep standard templates;
- compression cannot remove lifecycle state, artifact paths, evidence roles/results, instance bindings, revision numbers, or SHA-256 constraints;
- batch promotion and final handback are unchanged.

- [x] **Step 2: Add `Caveman 输出压缩模式` to the Chinese companion README**

Insert after `角色边界` and before `工作流`. Carry the same triggers, modes, stop forms, allowed/forbidden boundary, exactness promise, specialized-skill distinction, and examples in idiomatic Chinese.

- [x] **Step 3: Check companion language parity and formatting**

Run the same focused term searches in both files, followed by:

```bash
git -C /Users/elvis/.config/superpowers/worktrees/codex-brief-antigravity-review/document-caveman-readmes diff --check
```

Expected: every required term appears in both languages and diff check exits 0.

### Task 4: Verify both repositories

- [x] **Step 1: Run router validation**

Run from `/Users/elvis/.config/superpowers/worktrees/openspec-superpower-change/document-caveman-readmes`:

```bash
/opt/anaconda3/bin/python3 /Users/elvis/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_core_gates.py .
PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 -m unittest discover -s tests -v
```

Expected: quick validation, core validation, and all tests PASS; the latter two prove the dependency-free fallback.

- [x] **Step 2: Run companion validation**

Run from `/Users/elvis/.config/superpowers/worktrees/codex-brief-antigravity-review/document-caveman-readmes`:

```bash
/opt/anaconda3/bin/python3 /Users/elvis/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_templates.py .
PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 -m unittest discover -s tests -v
```

Expected: quick validation, template validation, and all tests PASS.

### Task 5: Review scope and close safely

- [x] **Step 1: Review the complete diffs**

Run:

```bash
git diff -- README.md README_cn.md docs/superpowers/specs/2026-07-16-document-caveman-readme-design.md docs/superpowers/plans/2026-07-16-document-caveman-readmes.md
git -C /Users/elvis/.config/superpowers/worktrees/codex-brief-antigravity-review/document-caveman-readmes diff -- README.md README_cn.md
```

Expected: README wording matches the approved design; no trigger, routing, lifecycle, evidence, or completion behavior changed.

- [x] **Step 2: Confirm changed-file inventory**

Run both repositories' `git status --short`.

Expected: only the router design, plan, and two router READMEs plus the two companion READMEs are changed.

- [x] **Step 3: Remove the temporary backup**

Delete only the uniquely named backup directory after all checks and review PASS.

Expected: backup directory no longer exists; repository files remain unchanged by cleanup.

No Git staging, commit, push, runtime synchronization, branch deletion, or worktree deletion is authorized by this plan.
