# Candidate Source High Review — P1 R14

Final verdict: **FAIL**  
Runtime verification may resume: **NO**

## Assignment and independence

- Product / role / profile: `codex` / `independent-reviewer` / `control-plane-high`
- Scope: complete current Router + Companion source delta and R14 cleanup correction.
- Authority: source Review evidence only.
- I read the complete Router and Companion `AGENTS.md`/`SKILL.md`, engineering invariants, project-learning closeout, approved OpenSpec/plan, and prior R5 PASS plus R11/R12/R13 FAIL Reviews.
- No project/private files were written. No Git, Pi, runtime plan, or runtime-destination inspection was performed.

## Bound inputs

| Input | Mode / SHA-256 |
|---|---|
| R14 input | `0644` / `dc2263902857a88c3daae1728714e05b08ee3181e3d26b99e3524f99c29a2ff4` |
| Source verification | `0644` / `6173624440308a6330c3c91659f67870be8c989ef035c7abd60eb8208ce4a04a` |
| R14 summary | `0644` / `bf7b42c48e582723c76c739be1188de13e3a7cc453e8c8c793c162308de3f692` |
| Private R14 delta | `0600` / `efce4e61a90ff14b9893cb852e2f09468e3af9be0e9c3857116587290c063e2f` |
| Preflight bindings | `0600` / `8877e931ef9d12f5e093ced04f15ef3517f3fead4cfe1e9f43055b8db56ee42e` |
| Allowlist | `0600` / `03fd6da52bd02345c595b370af0eebc47dce41dbd9e5046b8b0af2f0730c898d` |
| Current source | `0644` / `939dc80effdd605fea745291c02dd1079b9f0ebdfa72e8a467942c92775502d0` |
| Current tests | `0644` / `6a25c1cbf6eecbf12cec695d29fda09488786017b76d821047f90ccfb69328a7` |
| R14 private root / compare root | `0700` / `0700` |

Approved plan SHA: `dbf838c4b46d4212f57052b813be067c7448a48c6744d59fda25dce18684c229`.

Prior Reviews:

- R5 PASS: `073a367b6fa82e512bcb16df8c4f95152c9f9db76cd3c360201d36cc122dd9b4`
- R11 FAIL: `0d89c219a344f9943d9f324d4f36fc0cbb4ec503fc0bce0eb0ceb91912981d62`
- R12 FAIL: `35c38b467e5d2bacc4fdd90708c41801f36b494810a5ed4ea33b5b8fee24abc0`
- R13 FAIL: `5b7ffc4fb35a1072454145f3f1e104a21c4fa2bad28f9d7cab7ae82f5a823b17`

## Delta classification

The bound private delta reports:

- `source_delta: pass`
- `unexpected_paths: []`
- 92 actual paths total:
  - Router: 23 modified, 52 added, 3 deleted generated caches = 78
  - Companion: 14 modified = 14

The 96-entry allowlist has four intentional non-actual entries: unchanged Router
`CONTEXT.md`, absent intended R14 Review, the R14 summary evidence artifact,
and the allowlist-only R6 Review path. No actual path is missing from the
allowlist.

I inspected every changed/added file and the current implementation source. No
unrelated source path, sensitive artifact, or R14-introduced hidden residue was
found.

The current source-verification and R14-input files contain explicitly
disclosed evidence-only appends after the authoritative delta. A fresh
recomputation therefore sees the post-delta R14 summary as one additional
allowlisted record; this does not alter the bound 92-path implementation
classification.

## Verification performed

Passing checks:

- Bound RoleFirst forward evidence: `47/47 PASS`
- Router cross-CLI suite: `142/142 PASS`
- Router workflow suite: `124/124 PASS`
- Companion workflow suite: `87/87 PASS`
- Router and Companion core validators: PASS
- PyYAML-backed quick validation using `/opt/anaconda3/bin/python3`: PASS for both
- Strict OpenSpec validation: `3 passed, 0 failed`
- Shared handoff/validator identity checks: PASS
- Static stale-wording and sensitive-category checks: PASS; `0 sensitive categories found`
- Hidden-residue scan: no R14 transaction/persistence/debug residue

The system Python quick validator lacked PyYAML, so the documented PyYAML-capable
interpreter was used.

## R14 mechanism review

R14 correctly added:

- `_rebind_before_unlink()` at `scripts/validate_cross_cli_sync.py:1041-1076`
- exclusive Darwin `renameatx_np(..., RENAME_EXCL)` quarantine
- directory fsync and parent revalidation
- ownership/content revalidation of the quarantined name
- visible recovery handling for collisions and mismatches
- generic and Pi regressions for rebind-before-quarantine races

The new tests cover the race before the shared helper and the race inside
`_rebind_before_unlink()`:

- Generic: `tests/test_cross_cli_sync.py:1027-1069`, `1074-1128`
- Pi: `tests/test_cross_cli_sync.py:2066-2117`, `2119-2178`

## P1 finding

### P1-001 — Final quarantine unlink remains a name-replacement race

Location:

- `scripts/validate_cross_cli_sync.py:1138-1146`
- Generic caller: `scripts/validate_cross_cli_sync.py:1626`
- Pi caller: `scripts/validate_cross_cli_sync.py:5410`

`_unlink_bound_quarantined_entry()` revalidates ownership at lines 1138–1145,
then performs ordinary name-based:

```python
os.unlink(quarantine_name, dir_fd=guard["fd"])
```

at line 1146. `dir_fd` anchors the directory, not the inode. An unrelated inode
can replace `quarantine_name` after the final ownership check and before
`unlink`.

Fresh isolated probes reproduced this for both production paths:

- Generic: retained inode moved to `retained-final-aside`, unrelated inode
  installed at the quarantine name; the unrelated inode was deleted and no
  recovery residue remained.
- Pi: identical result; the Pi cleanup helper returned without preserving the
  unrelated object.

This is distinct from the R14-tested pre-quarantine race. The existing tests do
not inject a replacement between the final quarantine
`_require_retained_binding()` and the actual `os.unlink()`.

The same error branch at lines 1147–1154 only preserves residue if the name
still exists. An injected delete-then-error leaves no name to preserve; the
generic path reports an error without residue and the Pi outer handler at lines
5427–5430 swallows it. This is part of the same fail-closed cleanup defect.

This violates the R14 input requirement that no unrelated inode be deleted and
that any uncertainty leave visible recovery/blocked residue
(`2026-08-21-source-rereview-p1-r14-inputs.md:50-56`) and the plan’s explicit
prohibition on unlinking another object
(`docs/superpowers/plans/2026-08-10-add-role-first-review-routing.md:1679-1684`).

## Severity summary

- P0: none
- P1: 1 — P1-001
- P2: none

## Resume conditions

Runtime verification must remain stopped.

Before a new Review:

1. Replace the final name-based unlink with a deletion boundary that preserves
   exact inode ownership, or another kernel-backed design whose post-check
   replacement safety is demonstrated.
2. Add deterministic generic and Pi tests that replace the quarantined inode
   after the final ownership check and before deletion.
3. Add failure-injection coverage proving post-delete uncertainty leaves
   visible recovery/blocked residue.
4. Re-run the complete fresh no-Git source delta, validators, suites,
   sensitive/residue checks, and independent Candidate Source High Review.

Only a fresh control-plane-accepted `PASS` may authorize runtime planning or
runtime verification. Task 10 Pi execution remains outside this Review and was
not run.
