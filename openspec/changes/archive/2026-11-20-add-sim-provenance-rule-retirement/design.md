# Design: Provenance-Gated Rule Retirement with SIM Append-Only Tombstones

Author: elvis. Revision: draft-v2. Status: proposal-only (awaiting explicit approval of `add-sim-provenance-rule-retirement`).

## 1. Architectural Options Considered

| Option | Summary | Assessment |
|---|---|---|
| **Option 1 (Recommended)** | Formalize provenance-gated retirement in `references/self-evolution-rule.md` + `references/skill-iteration-loop.md`, reuse `docs/iteration/BACKLOG.md` append-only SIM records (`record_kind: sim-retirement`), and enforce boundaries in `scripts/validate_core_gates.py:main(...)` via `validate_sim_rule_retirement_guard` + `validate_sim_retirement_record`. | Zero new state files; preserves Major gate and zero everyday hot-path token cost; anchors protected exclusions to concrete repository files/sections; enforces deterministic multi-runtime/model-family independence without a closed model allowlist; fully dual-YAML compatible. |
| **Option 2 (Rejected)** | Create a dedicated `docs/iteration/RETIRED_RULES.md` ledger file. | Violates the repository's anti-sprawl guardrail against adding new iteration state files and splits retirement history away from `S10` `BACKLOG.md` attempt memory. |
| **Option 3 (Rejected)** | Downgrade prose rule retirement to Minor when one frontier model passes an isolated test. | Violates `references/project-learning-closeout.md:138` and `openspec/specs/skill-workflow-governance/spec.md:1922-1924`; empirically refuted by `arXiv:2611.18856v1` §4.3.3 where single-model edits hurt sibling models in a shared harness. |

## 2. SIM Retirement Record Contract (Dual-YAML Compatible)

Retirement tombstones reuse `docs/iteration/BACKLOG.md` using pure nested mappings compatible with both `PyYAML` (`yaml.safe_load`) and `scripts/validate_core_gates.py:simple_yaml_load` (no list-of-dicts, no inline `#` comments, no unquoted `: ` inside scalars).

### 2.1 `mechanical-superseded` Shape

```yaml
record_kind: sim-retirement
slice: S12
root_cause: legacy prose workaround replaced by static validator
target_surface: references/example-guide.md#legacy-note
origin_anchor: commit-abc1234
retirement_basis: mechanical-superseded
retirement_evidence:
  evidence_1:
    validator_or_test: scripts/validate_core_gates.py
    negative_case: test_rejects_legacy_workaround_regression
reopen_condition: static validator is removed or regression recurs in CI
attempts:
  attempt_1:
    provenance: gemini-4-neon / agy / 2026-11-20 / S12
    change: removed redundant legacy prose after validator coverage landed
    predicted: core gates and regression suite remain green without prose
    observed: retired - mechanical validator rejects counterexample identically
```

### 2.2 `cross-model-internalized` Shape

```yaml
record_kind: sim-retirement
slice: S12
root_cause: older model forgot command framing without verbose prose hint
target_surface: references/example-guide.md#verbose-hint
origin_anchor: commit-def5678
retirement_basis: cross-model-internalized
retirement_evidence:
  evidence_1:
    runtime: antigravity-cli
    model_family: gemini
    probe_ref: docs/review/s12-probe-agy-gemini.json
  evidence_2:
    runtime: codex
    model_family: gpt
    probe_ref: docs/review/s12-probe-codex-gpt.json
reopen_condition: any declared CLI target reproduces the original failure mode
attempts:
  attempt_1:
    provenance: gemini-4-neon / agy / 2026-11-20 / S12
    change: removed obsolete verbose prose hint after dual-runtime forward proof
    predicted: both isolated forward probes stay green without the prose hint
    observed: retired - 2 distinct runtimes and model families passed unhinted
```

### 2.3 Deterministic Fail-Closed Rules (`validate_sim_retirement_record`)

`scripts/validate_core_gates.py` SHALL expose `validate_sim_retirement_record(record: dict) -> None` with these exact invariants:

1. **Unconditional Ban on `status: promoted` in Retirement Records**: Reject unconditionally if `record.get("status")` (case-insensitive) equals `"promoted"`, regardless of `decision_owner`. Retirement tombstones are non-gating optimizer memory expressed strictly via `record_kind: sim-retirement` and `observed: retired - ...`.
2. **Required Non-Blank Scalars**: `record_kind` MUST equal `"sim-retirement"`; `slice`, `root_cause`, `target_surface`, `origin_anchor`, `retirement_basis`, and `reopen_condition` MUST be non-empty strings.
3. **Structured `target_surface` & Repository-Anchored Protected Exclusion**:
   - `target_surface` MUST match `<project-relative-path>#<section-slug>` with exactly one `#`:
     - Reject missing `#`, empty path or slug, absolute paths, `..` traversal, backslashes, or pure line-number anchors (`#L171`, `#L10-L20`, `#171`).
     - Normalize path by stripping leading `./`; normalize section slug by lowercasing and collapsing runs of non-`[a-z0-9]` characters to `-` (stripping leading/trailing `-`).
   - Reject if normalized path is in `NON_RETIRABLE_FILES`:
     - `SKILL.md`
     - `references/shared-global-governance.md`
     - `references/completion-contract.md`
     - `references/step-evidence-gate.md`
     - `references/handoff-contract.md`
     - `references/confirmation-lease.md`
     - `references/agent-capability-routing.md`
     - `references/openspec-decision-rule.md`
   - Reject if `<normalized-path>#<normalized-slug>` is in `NON_RETIRABLE_SECTIONS`:
     - `references/self-evolution-rule.md#hard-prohibitions`
     - `references/self-evolution-rule.md#change-levels`
     - `references/self-evolution-rule.md#provenance-gated-rule-retirement`
     - `references/skill-iteration-loop.md#authorization`
     - `references/skill-iteration-loop.md#reading-budget-for-one-round`
     - `references/project-learning-closeout.md#triggers`
     - `references/project-learning-closeout.md#enforcement-and-review`
   - Reject if normalized slug contains any fallback protected token in `NON_RETIRABLE_SLUG_TOKENS`: `non-negotiables`, `ccg-`, `validator-locked`.
   - **Boundary Honesty**: `validate_sim_retirement_record` blocks protected `target_surface` metadata; the final mechanical defense verifying that no validator-locked phrase was deleted from any non-excluded file remains executing `scripts/validate_core_gates.py`.
4. **Structured `retirement_basis` & Open-World Multi-Model/Runtime Normalization**:
   - `retirement_basis` MUST be strictly `"mechanical-superseded"` or `"cross-model-internalized"`.
   - `retirement_evidence` MUST be a non-empty mapping (`dict`) of named evidence entries (`evidence_1`, `evidence_2`, ...), each itself a `dict`.
   - When `retirement_basis == "mechanical-superseded"`:
     - Require `>= 1` evidence entry; each entry MUST have non-empty strings `validator_or_test` (relative path without `..` or absolute prefix) and `negative_case`.
   - When `retirement_basis == "cross-model-internalized"`:
     - Require `>= 2` evidence entries; each entry MUST have non-empty single-value strings `runtime`, `model_family`, and `probe_ref`.
     - Single-value enforcement: reject `runtime` or `model_family` containing multi-value separators (`/`, `,`, `;`, `|`, whitespace).
     - Deterministic open-world normalization (NO closed model allowlist, honoring `CCG-009` and `SKILL.md:145`):
       - `runtime`: lowercase, collapse `_` to `-`, apply canonical alias map `{"agy": "antigravity-cli", "antigravity": "antigravity-cli", "grok": "grok-cli"}`.
       - `model_family`: lowercase, collapse `_` to `-`, strip repeated trailing tier/version tokens (`-(?:low|medium|high|xhigh|mini|flash|pro|lite|max|reasoning|carbon|argon|neon|opus|sonnet|haiku)$` and trailing `-(?:v?\d+(?:\.\d+)*)$` so e.g. `gemini-4-carbon` and `gemini-4-argon` both normalize to `gemini`, `claude-opus-5.5` and `claude-sonnet-4` normalize to `claude`, while new families like `deepseek-v4` normalize to `deepseek` and are accepted without editing any allowlist).
     - Independence rule: PASS only if `len(unique_normalized_runtimes) >= 2 or len(unique_normalized_model_families) >= 2`.
5. **Tombstone Attempt Verification**: `attempts` MUST be a non-empty mapping; every attempt entry MUST be a mapping with non-empty `provenance`, `change`, `predicted`, `observed`, and at least one attempt's `observed` MUST start with `"retired"` (case-insensitive).

### 2.4 Production Wiring in `scripts/validate_core_gates.py:main(...)`

- Call `validate_sim_rule_retirement_guard(self_rule, loop, learning_template)` directly inside `main(...)` for every validated skill root.
- Also inside `main(...)`: when `(root / "docs" / "iteration" / "BACKLOG.md").is_file()` (so distribution and runtime copies without `docs/iteration/` continue passing cleanly), extract every fenced ` ```yaml ... ``` ` block from `BACKLOG.md`, parse via `yaml_load`, and whenever a block has `record_kind == "sim-retirement"` or contains key `"retirement_basis"`, invoke `validate_sim_retirement_record(parsed)`.

## 3. Target Files, Cohesive Batch, and Exact Verification Anchors (Phase B Only)

### Batch 1 (Single Cohesive Implementation Batch after Approval)

- **Target files**:
  1. `references/self-evolution-rule.md`: add `## Provenance-Gated Rule Retirement`.
  2. `references/skill-iteration-loop.md`: update Step 3 from `4 条准则` to `5 条准则` and append the non-resurrection / Major-only retirement rule.
  3. `templates/learning-candidate-template.md`: extend the last `## Rules` bullet to cover `reverted` and `retired`.
  4. `scripts/validate_core_gates.py`: add `NON_RETIRABLE_FILES`, `NON_RETIRABLE_SECTIONS`, `NON_RETIRABLE_SLUG_TOKENS`, `validate_sim_retirement_record`, `validate_sim_rule_retirement_guard`, and wire both (plus conditional `docs/iteration/BACKLOG.md` retirement-block scanning) into `main(...)`.
  5. `tests/test_workflow_rules.py`: add RED->GREEN unit tests and negative counterexamples covering all 5 fail-closed rules, normalization edge cases (alias collapse `agy`==`antigravity-cli`, tier collapse `gemini-4-carbon`==`gemini-4-argon`, open-world acceptance `deepseek-v4`, line-anchor rejection `#L171`, `BACKLOG.md` end-to-end `main(...)` scan rejection, and guard mutation checks) under both PyYAML and `simple_yaml_load`.
  6. `distribution/codex-plugin` (regenerated via `/opt/homebrew/bin/python3 scripts/build_codex_plugin.py .`).
  7. `CHANGELOG.md`, `docs/iteration/{BACKLOG,CURRENT,LOG}.md` (and `openspec/specs/skill-workflow-governance/spec.md` on archive).

- **Exact verification & closure commands (Phase B)**:
  - `/usr/bin/python3 -m py_compile scripts/*.py`
  - `/opt/anaconda3/bin/python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .`
  - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_core_gates.py .` (dependency-free fallback)
  - `PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 scripts/validate_core_gates.py .` (PyYAML)
  - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_distribution.py .`
  - `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 -m unittest discover -s tests -v` (main repo + clean-tree no-PyYAML fallback under `/private/tmp/<parent>/openspec-superpower-change` with sibling symlink `codex-brief-antigravity-review`)
  - Isolated read-only forward-test (2 scenarios: reject retiring protected/single-model rule; respect `retired` tombstone without silent resurrection)
  - Independent Implementation Review (`readonly-reviewer`, `same_instance=false`) -> `PASS`
  - Four-target (`codex`, `pi`, `antigravity-cli`, `grok-cli` with `grok inspect --json --consume`) schema-v2 scoped sync for the 4 modified portable files (`references/self-evolution-rule.md`, `references/skill-iteration-loop.md`, `templates/learning-candidate-template.md`, `scripts/validate_core_gates.py`) via `scripts/validate_cross_cli_sync.py` + `verify-all` (managed rule v6 untouched)
  - Independent Final Review (`same_instance=false`, distinct from executor, verifying full diff, fresh tests, and four-target `verify-all` evidence per `CCG-007` & `CCG-016`) -> `PASS` before commit/push.

## 4. Compatibility & Rollback

- **Backward compatibility**: All existing Candidate Cards and `S10` `sim-backfill` / `sim-slice-record` entries remain valid unchanged. `SKILL.md` frontmatter, routing table, `Non-Negotiables`, and shared governance block v6 are untouched.
- **Proposal-only rollback (Phase A)**: Remove `openspec/changes/add-sim-provenance-rule-retirement/` and `docs/review/2026-11-20-S11-sim-provenance-rule-retirement-draft.md`, and restore `docs/iteration/{BACKLOG,CURRENT}.md` to pre-proposal lines (never touch the 6 legacy dirty groups).
- **Post-approval rollback (Phase B)**: Restore from `/private/tmp/osc-backup-<timestamp>` prior to push, or `git revert <commit>` plus transactional reverse scoped sync via `scripts/validate_cross_cli_sync.py`.
