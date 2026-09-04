# Learning Candidate Card

```yaml
status: promoted
event_kind: review-finding
severity: high
scope: project-local
promotion_trigger: threshold
symptom: Public distribution validation initially accepted symlinked source/output paths.
prior_assumption: Checking only the final source file or output marker was sufficient to bind a distribution path.
correction_or_evidence: Two independent reviewers reproduced source-parent, output-parent, npm-allowlist, and existing-output symlink escapes in isolated temporary copies.
generalized_invariant: Every public distribution source, package allowlist entry, and generated-output path must remain inside its bound root without following symlinks; replacement must recheck the existing output tree and object identity immediately before mutation.
independent_reproductions: "Arendt review: source-parent/output-parent/npm allowlist probes; Kepler review: existing .codex-plugin symlink probe."
independence_rationale: The findings came from separate reviewer agents inspecting the same contract and reproduced distinct path-binding failures.
duplicate_or_conflict_result: No conflict with existing project symlink-boundary invariants; this adds the public-package/generated-adapter scope.
target_artifacts: "docs/engineering-invariants.md; scripts/build_codex_plugin.py; scripts/validate_distribution.py; tests/test_distribution.py"
mechanical_enforcement: required
mechanical_enforcement_reason: Validators and negative unittest cases reject parent/leaf source symlinks, output-parent/tree symlinks, allowlist symlinks, output identity drift, and npm file-set drift.
verification: "scripts/validate_distribution.py PASS; official plugin validator PASS; 19 focused distribution tests PASS; evidence hashes: build c3f7162a392c9987bcb7c818e9e4090d66a97773dfe79b72222bf3d822c57e37, validator bcb31cf04aa1e6897a0f50fa67aaa39ab033f89be477adcbcef6bbce2dfd95df, tests 0a200a60a45e1cd1a8e75962c1282be660d62dddc124484894d7ed097d6584a7, spec e403a125201f110094daf91d19b9207060fd5d902ca9bbcf1dfd05364df8f6aa, invariants e7d80dd8e9a18ed985eaf9ec9c65e0f240ad7702bbaf042e3cec35624f50e4c1"
review_result: pass
decision_owner: codex
decision_provenance: "2026-09-03 community distribution change; LEARNING REVIEW PASS after focused verification and independent Review of the durable invariant."
```

## Promotion note

This candidate records only sanitized project-relative evidence and no private
prompt, credential, or external runtime content. It becomes `promoted` only
after the invariant is present in the engineering guidance and the focused
validator/tests plus an independent Review pass.
