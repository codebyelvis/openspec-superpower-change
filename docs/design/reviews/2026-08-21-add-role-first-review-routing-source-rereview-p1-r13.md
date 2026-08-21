# Candidate Source High Re-review — P1 R13

## Assignment and independence

- Reviewer: fresh no-history `codex / independent-reviewer / control-plane-high`, `gpt-5.6-luna`, max reasoning.
- Authority: source Review evidence only.
- No project/private artifact writes, Git, Pi execution, runtime-destination inspection, plan creation, or completion claim.

## Bindings and delta

- R13 input: mode `0644`, SHA-256 `913c09e3541f54f4736314cbe72003fae407bedbc86b4f5f1e7e44812d829cd0`.
- Script: `0644 / fd8a05c2d8126d1202847a60d574ab65edcee238d3c00c722797db69224e3295`.
- Tests: `0644 / 419774194a4254f6a8b253c7505c2722ad5e6509d1979a4acd0533f3df0ab689`.
- Private delta: `0600 / d6c959d118e5f7bcf9f691131c1126be637c683bc03cd10fdb14ea4935113d48`.
- Bindings: `0600 / fded0c8cc1f93e9591926118cac6c9d4ff838c980da7eedf79c9c0aadb46fa37`.
- Allowlist: 93 entries, `0600 / 3531c68cbbb41b4de9e271adb51dbfc22367555565faeaabd4d064125e78ed98`.
- Compare root: mode `0700`.
- Durable summary: `0644 / 2ebfc39e4225adbbb6327925ae7bd0e4d0fdbbe907c750bb055611e4a47bc9ab`.
- Complete delta: `89` paths — Router `75`, Companion `14`; `37` modified, `49` added, `3` deleted; `source_delta: pass`, `unexpected_paths: []`.
- Source verification current SHA: `4131d94996452d0832911957b7a92da6d6af84171e8cd2441c228e736985ab04`.
- The post-delta input normalization is disclosed evidence-only state.

## Mechanism, tests, and probes

The R13 implementation correctly adds both-sided ownership checks for generic exchange rollback, Pi rename-side-effect inspection, blocked-recovery validation, rollback-collision residue handling, and the requested regression coverage.

Independent validation:

- Cross-CLI suite: `140/140 PASS`.
- Router full suite: `264/264 PASS`.
- Core validator: `PASS`.
- Quick validation with the PyYAML-enabled interpreter: `PASS`.
- Fresh isolated short-write, fsync-failure, and blocked-name-collision probes: durable `BLOCKED` evidence was produced.
- Existing R13 tests for one-sided exchange, rename-then-raise, malformed blocked recovery, and Pi rollback collision passed.

However, a fresh isolated check-to-unlink probe found a P1 defect in both generic and Pi cleanup:

- Generic: `scripts/validate_cross_cli_sync.py:1041-1084, 1536-1552`
- Pi: `scripts/validate_cross_cli_sync.py:5318-5334`

After `_rebind_before_unlink()` opened and validated the retained descriptor, the reviewed inode was renamed aside while an unrelated inode was installed at the cleanup name. Because the retained descriptor remained linked and ctime is excluded at this boundary, validation passed; the subsequent name-based `os.unlink()` deleted the unrelated inode. No error or recovery residue was produced.

## Findings

- P0: none.
- P1: one — generic and Pi final check-to-unlink race can delete an unrelated inode.
- P2: none.

## Resume conditions

Replace the post-check name-based unlink with an ownership-preserving atomic quarantine/no-replace operation (or equivalent kernel-bound primitive), then unlink only the revalidated quarantined object. Add regressions where the retained inode is moved aside without unlinking and an unrelated inode replaces the cleanup name. Rebind the complete delta and obtain a fresh independent source Review.

## Verdict

**FAIL. Read-only runtime verification may not resume.**
