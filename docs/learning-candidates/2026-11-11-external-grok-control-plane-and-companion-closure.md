# Learning Candidate: Runtime pin snapshot guards and out-of-slice companion helper closure

Author: `elvis`
Change: `allow-one-external-grok-control-plane`

```yaml
status: promoted
event_kind: review-finding
severity: medium
scope: project-local
promotion_trigger: explicit-archive-distill
symptom: "Materializing an authorized mode-0600 external pin broke ExternalGrokControlPlaneTests.setUp; separately, Companion validate_templates.py mirrored require_external_control_plane_section outside the shared core slice without defining _resume_section."
prior_assumption: "Asserting real_pin absence in setUp/tearDown sufficed to prove test isolation, and byte-equality of the shared core slice plus green layout validation sufficed to prove Companion gate parity."
correction_or_evidence:
  - "Stage-1 independent review identified that codex-brief-antigravity-review/scripts/validate_templates.py called _resume_section from require_external_control_plane_section without defining _resume_section outside the shared core slice; adding the bounded Markdown section helpers closed the NameError while keeping the shared core slice byte-equal."
  - "Autoloop run-17 independent Pi review identified tests/test_external_grok_control_plane.py:56,69 asserting self.assertFalse(self.real_pin.exists()), which failed all 8 tests in that module whenever an active mode-0600 pin existed on disk."
  - "Replacing the absence check with a pre/post (st_mode, bytes) immutability snapshot and adding test_companion_external_section_helper_closure passed all unit tests both with and without an active pin."
generalized_invariant: "Guard mocked runtime-pin paths with pre/post immutability snapshots rather than absence assertions, and verify symbol closure by directly invoking any gate mirrored outside a byte-synced shared slice."
independent_reproductions: "Two distinct independent review passes: Stage-1 AGY review caught the out-of-slice Companion helper gap, and Autoloop run-17 read-only Pi review caught the active-pin setUp regression."
independence_rationale: "Each defect was surfaced by a read-only reviewer inspecting code and running or auditing verification artifacts outside the authoring turn."
duplicate_or_conflict_result: "Complements existing shared-slice sync and scoped-publication invariants in docs/engineering-invariants.md without introducing a new workflow gate."
target_artifacts:
  - docs/engineering-invariants.md
  - docs/learning-candidates/2026-11-11-external-grok-control-plane-and-companion-closure.md
  - tests/test_external_grok_control_plane.py
mechanical_enforcement: required
mechanical_enforcement_reason: "Both invariants are mechanically enforceable via ExternalGrokControlPlaneTests setUp/tearDown snapshot equality and test_companion_external_section_helper_closure."
verification:
  - "Focused archive & learning verification passed: openspec validate --specs --strict (2/2 specs passed); tests.test_external_grok_control_plane + tests.test_workflow_rules 228/228 OK (including BRIEF_ROOT-resolved test_companion_external_section_helper_closure); scripts/validate_core_gates.py . OK; Companion validate_templates.py . OK."
  - "Independent read-only Pi learning review R2 (session 01a1ca08-d1fa-77ba-9854-045b3d17a2f4) returned LEARNING_REVIEW_VERDICT: PASS with 0 blocking findings and verified pre/post workspace fingerprint d17d03a3253e2728269beb89f1bd663b245136e1100b14eb6f687a62ffd64784."
review_result: pass
decision_owner: codex
decision_provenance: "Explicit user archive-and-distill request on 2026-11-11 following published commits 38d9bee1fd4f54062040f1270a6eea84b020b7ba (Router) and 8454c7fc5f16ce8d7f86c7a85886b639528ded67 (Companion); promoted after R2 read-only Pi review PASS."
```

## Durable targets and mechanical enforcement

- [Runtime pin tests and shared-slice companion gates](../engineering-invariants.md#runtime-pin-tests-and-shared-slice-companion-gates-must-preserve-live-snapshots-and-helper-closure).
- `tests/test_external_grok_control_plane.py`: `setUp` / `tearDown` `(st_mode, bytes)` snapshot check and `test_companion_external_section_helper_closure`.
- Companion `scripts/validate_templates.py`: bounded `_markdown_*` and `_resume_section` helpers outside the byte-identical shared core slice.
- Archived OpenSpec capability: `openspec/specs/external-grok-control-plane/spec.md` and `openspec/changes/archive/2026-11-11-allow-one-external-grok-control-plane/`.

## Bounded adversarial checks

1. Running `ExternalGrokControlPlaneTests` when `references/external-control-plane-rebinds.json` is absent (`None -> None`) or present as a mode-`0600` file (`(st_mode, bytes)` unchanged) must both pass while still failing if a test mutates or creates the real pin.
2. Calling Companion `validate_templates.require_external_control_plane_section` with a matching pinned Grok status must pass without `NameError`, and mutating the `## External Control Plane Rebind` JSON block must raise `must equal the pin entry`.
3. Dirty-worktree isolation: archiving and promoting learning in the repository does not stage unrelated October local-rebind drafts or claim cross-CLI runtime installation beyond verified targets.
