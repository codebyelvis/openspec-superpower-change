# Draft-v1 proposal verification

Author: elvis. Date: 2026-10-10. Status: proposal-only, no approval recorded.

## Exact draft bindings

| Artifact | SHA-256 |
|---|---|
| proposal.md | `c912f9051b150cd02aaf679cacc833981eeb6b1ae5aa0128838616e0df6f2f12` |
| design.md | `e2a68bd46ad6afa438907c1d442e73ab8804121dc3b485c6a8d2fa7c469bc313` |
| tasks.md | `77ef85261e229cfe1b5e4a81b7d26994ed08f7222ecbfa8b7a83ecd6e43b0643` |
| specs/skill-workflow-governance/spec.md | `65068ac3e05e318ed54d958b03baa3f3d3ff44a5624b7dbc65ce015c1d78d1e2` |
| docs/review/2026-10-10-native-agent-adaptation-r2-candidates.json | `662c5fc5547f610b5175dad81a8c0cd59f9eeebc0f03f15f7a361d9279a768f9` |
| docs/superpowers/plans/2026-10-10-native-agent-adaptation-next-r2.md | `34004053de5fc4670728fe4d4352c1496561e984a2ec70eeb3061aa4974d34b3` |
| docs/review/2026-10-10-native-agent-adaptation-feedback-r2.md | `ea5b3b144a8a0f3d7fe0206c253d917edf678e3962658c6e275f00d2fb871a09` |

## Executed checks

- `openspec validate align-native-consumer-projections --strict`: exit 0.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .`: exit 0.
- Fresh inline Python reconstruction of all six candidates from persisted exact
  edits and canonical source: 6/6 match their candidate SHA-256.
- Fresh target preimage hashes/modes and protected publisher hash: unchanged.
- Eight relative Markdown links across the seven draft/input artifacts resolve.
- Original delivered plan retains its completion-bound SHA-256; no task in the
  new proposed change is checked as implemented.
- Candidate preparation preserves all 586 existing project ordinary files
  before its first metadata addition; full private candidates/preimages were
  removed after verification. No native target write or publisher call.

Focused owner self-review checks the actual added documents and candidate
metadata for unique file ownership, single Claude prestate, real product/config
distinctions, source policy boundaries, cross-consumption, path protection,
private-content handling and unresolved mechanisms. It accepts this draft as
reviewable; it is not independent Preflight or implementation Review PASS.

No source/installed governance behavior changed in this turn, so the full
implementation suites or model forward tests were not rerun. Prior 492/91
suite results belong to the earlier completed source slice, not to this proposed
native implementation. Recovery commands, failure injections, actual-entry
event qualification, independent Preflight, native writes and behavior checks
remain pending in tasks.md. Claudex's follow-up advisory remains outstanding.

No source rule, other active spec, existing completion/evidence, native hook,
publisher, dependency link, credential or Git state was intentionally changed.
