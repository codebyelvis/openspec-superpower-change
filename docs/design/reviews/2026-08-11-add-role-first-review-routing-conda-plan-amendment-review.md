# Independent Conda Plan Amendment Preflight Review — Revision 5

## 1. Reviewer identity

- Reviewer product: `codex`
- Reviewer role: `independent-reviewer`
- Capability profile: `control-plane-high`
- Instance/thread ID: `unavailable`
- Independence evidence: `user_opened_separate_window`
- Participation: did not author the Plan amendment, Preflight evidence, or
  source implementation; did not modify the revision; will not act as the
  Conda/environment or source executor.
- Review route: `codex-brief-antigravity-review` standalone, read-only,
  evidence-only.
- Review mutation: none; no file, mode, or Conda-environment mutation.

Path aliases:

- `R`: `/Users/elvis/file/develop/opensource/openspec-superpower-change`
- `C`: `/Users/elvis/file/develop/opensource/codex-brief-antigravity-review`
- `T`: `/private/tmp/add-role-first-review-routing-20260810-FPWT9V`

## 2. Reviewer Assignment Contract

| Field | Binding |
|---|---|
| `review_purpose.object` | Revised implementation Plan; Conda interpreter, dependency, channel, path and write boundaries; PEP 668 blocker history; R4 Preflight/source-start/recovery continuity; partial-source snapshot; R5 allowlist/bindings; Task 6 commands/results/stop/cleanup; Git/Pi/runtime/canonical/archive/publication/completion authority |
| `review_purpose.decision` | Decide only whether the original bound Codex control-plane may create the reviewed isolated Conda verification environment and resume Task 6 source verification |
| `reviewer_product` | `codex` |
| `reviewer_role` | `independent-reviewer` |
| `capability_profile` | `control-plane-high` |
| `independence_requirement` | User-opened window distinct from amendment author, evidence preparer, and source/environment executor |
| `result_authority` | governed Conda Plan amendment Preflight evidence only |
| Explicit non-authorizations | Re-running/rewriting Tasks 1–5, source correctness/PASS, source High Review, Pi, runtime, Git, canonical transition, archive, Envelope, publication, completion, Conda cleanup |

## 3. Scope, reads, SHA, and read-only commands

The reviewer read every Router, Companion, temporary-binding, and backup-list
input required by the revision-5 prompt. Router inputs included `AGENTS.md`,
`SKILL.md`, `CONTEXT.md`, OpenSpec project/proposal/design/tasks/specs, the
revised Plan, R4 inputs/Review, RED and blocker evidence, amendment inputs,
required workflow references, and `validate_cross_cli_sync.py`. Companion
inputs included `AGENTS.md`, `SKILL.md`, and `validate_templates.py`.

The reviewer also read R4 allowlist/bindings to prove the exact R5 increment.
Backups were inspected only with metadata, SHA, and `tar -tf`; no archive was
extracted.

All 19 required immutable inputs matched at Review start and end:

| Input | SHA-256 |
|---|---|
| Revised Plan | `c7158746403282c1d1800fb98c4cf042677e390aaf6c8aabb9ac46e078308fb2` |
| Conda amendment inputs | `fe5c8ef2186b81257be389e30ce297cf5ed3f0d06f93dec5676a91077a79c381` |
| Proposal | `970fdbb94fbbc3454db620ef2b2475b4ddb327042ad303c938d268b4710a9330` |
| Design | `612627c7036e402e3bd39fb1d4f435adf70e6212165047c394f64a32c10c0480` |
| Current tasks | `54a795219972dd7b7a56beabc4facbe948bff77bd39edfd1e0856629b7d203ed` |
| Spec delta | `99e716013a085ead35388ac401415dc4078c00ccc2846e8dbd14a14ed9244384` |
| Initial R4 inputs | `13a2e1a5e1f11517c39bb9fe00e140c6e61884dedc4bf21f1ede6c3cea048f75` |
| Initial R4 Review | `9fc3aa76e44bd722d8c7fb57f37d2c2e042b244963fc04b4d736fadbd5f8f030` |
| RED evidence | `4c3c74eaac76e01fd7a1536a32785b2fd33ae555b4ca1b6f505969fb6375c3ef` |
| Source blocker evidence | `04857f7fd625b5f6a9b17ff8a9fc2d873eccf95de40fb290e47b44fc75317a88` |
| Conda executable | `a543f4db6623ff7316d0549c2e5241196499a0d0b3e8d212772eeb2df084c8a3` |
| R5 allowlist | `99238be04ccb2f8951a1c7430688bad4d17dd1c1739744794ac3f6f66632e3d9` |
| R5 bindings | `c53f714bf9aa6df8147f8ec01f6d41a5e47c4617b39a289130a39d56987ed731` |
| Router source-start | `7805c4c70512d28b690241073fb134e9f9b7b93ddc0c3f51ea8d320c81ed0151` |
| Companion source-start | `737f700486279fd3d007ba8a9d6e7c96bfff18273eed41d443b6b44b355d068b` |
| Router amendment snapshot | `dc8d1d4ca4d410f5e5bd0d2f7f8d817d3a2d50d8c81d729e564eb357afe04a4e` |
| Companion amendment snapshot | `f4eb4af4c836242eb6cc11311aac4bc89ebf68fb2957ccd515770a4317c31bf9` |
| Router backup | `a0b7a36e0964fe8e6b93bbcb24a2454bab1c3376159f7cd55f710054d464c491` |
| Companion backup | `3deab7e813efca3de22ff7d583a5ae089eec079c63842239d9adb85191fb4acc` |

The local Review prompt matched
`b151534cd424493699539608e9e9f2c49abb198d5acb83ce110e0033eb06ace6`.
The transaction root was a real mode-`0700` directory owned by `elvis`; the
Conda executable was a mode-`0755`, 515-byte regular file. All four proposed
Conda paths were absent and non-symlinks at Review start and end.

Read-only command families were `wc -l`, `nl -ba`, `sed -n`, `rg`, `stat`,
`readlink`, `shasum -a 256`, `tar -tf`, `command -v`, OpenSpec listing/strict
validation, and the two project validators with `PYTHONDONTWRITEBYTECODE=1`.
No Git, Conda CLI, pip, Pi, quick validation, unit suite, forward probe,
source-delta, runtime operation, or archive extraction was run.

## 4. Amendment and Plan assessment

1. Approved contract and progress matched: Proposal/Design/spec were unchanged;
   tasks were `24 checked / 17 unchecked`, with Tasks 6.1–8.7 incomplete.
2. Amendment scope was limited to the Task 6 verification environment and
   source-delta binding; it did not reopen Tasks 1–5 or add source behavior.
3. PEP 668 continuity matched: the authorized standard user pip attempt stopped
   on refusal and did not use `--break-system-packages` or an alternate
   interpreter.
4. Conda bytes and all four private paths were correctly bound and guarded.
5. The create command correctly disabled plugins, selected classic solver,
   overrode channels to defaults, disabled default packages, and bounded Python
   3.11/PyYAML 6.x without activation/init/config/base/pip fallback.
6. Declared writes were limited to the private prefix, HOME, package cache, and
   TMPDIR; external writes were stop conditions.
7. Post-create assertions were individually adequate, but the exact shell block
   lacked a mechanical fail-fast boundary. This is `F-R5-001`.
8. Only the two quick validators used Conda; project validators/tests/OpenSpec
   remained on default Python/original commands.
9. R4 continuity was honest; amendment snapshots did not masquerade as new
   pre-implementation baselines.
10. R5 allowlist/bindings were exact: 49 unique, wildcard-free entries, with
    precisely four additions over R4 and a schema-1 binding to the revised Plan.
11. No explicit authority expansion was observed.
12. The intended resume point was accurate, but the missing fail-fast mechanism
    prevented authorization.

## 5. Findings

### P0

None.

### P1 — `F-R5-001`: Task 6 Step 2 does not mechanically fail closed

- exact locations:
  - Plan Task 6 Step 2 exact block, line 1009;
  - hash/path/version guards, line 1017;
  - Conda create, line 1028;
  - declared stop behavior, line 1052.
- observed fact: the block used `umask 077` followed by ordinary shell commands,
  with no `set -e`, explicit error branch, or equivalent per-command gate.
  A normal shell can continue after a failed guard or create command.
- violated contract: Plan Preflight and Step 2 require every guard/create/
  assertion failure to stop and return `BLOCKED`.
- impact:
  - hash/version failure could still reach directory creation or Conda;
  - an occupied prefix check could still reach `conda create --prefix`;
  - a failed create could still reach post-create assertions, and a final
    successful assertion could mask the earlier nonzero result.
- required correction:
  1. add a reliable fail-fast boundary, such as a closed subshell with
     `set -euo pipefail`;
  2. split each `test ! -e ... && test ! -L ...` into independent top-level
     fail-fast tests or explicit failure branches;
  3. make every hash/path/version/mkdir/create/post-create failure stop without
     fallback or automatic cleanup;
  4. make Task 6 Step 3 mechanically stop at the first nonzero command.
- re-review: required after Plan and all derived hashes/bindings/snapshots/prompt
  are refreshed. The executor may not add the shell options ad hoc.

### P2

None.

### Observations

- `OBS-R5-001`: current OpenSpec and project validators passed, but they do not
  inspect Task 6 shell fail-fast or prove Conda/source correctness. Owner:
  control-plane. Release: fix `F-R5-001`, re-Preflight, then generate real Task
  6 evidence.
- `OBS-R5-002`: instance/thread ID was unavailable but permitted by the
  assignment when paired with `user_opened_separate_window`. No fabricated ID
  is required.

## 6. R4/source-start continuity

R4 inputs/Review, RED evidence, Router/Companion source-start inventories, and
both backups remained unchanged. R4 remained the historical pre-implementation
boundary; the amendment snapshots remained partial-source Review evidence only.
No restore/delete authority was introduced.

## 7. Conda matrix

The executable hash, absent private prefix/HOME/package-cache/TMPDIR, parent
mode, plugin/solver/channel/package/user-site restrictions, and prohibitions on
activation/init/config/base/pip were all closed. The only blocking surface was
guard/create sequencing without mechanical fail-fast.

## 8. Task 6 command matrix

Step 2 contained all required guards, exact create command, and assertions, but
did not mechanically stop on the first failure. Step 3 preserved the correct
interpreter split, but likewise needed an explicit first-nonzero stop boundary.
Later Task 6 static/forward/source-delta steps were not authorized by this
Review.

## 9. R5 and recovery matrix

- R5 allowlist: 49 lines, unique, no wildcards, exact four-entry increment.
- R5 bindings: exact schema 1, revised Plan, R4 backups/baselines, R5 allowlist.
- Router amendment snapshot: 328 records, two explicit planning exclusions.
- Companion amendment snapshot: 29 records, no exclusions.
- Backups: SHA/mode/member counts matched; not extracted.
- Restore authority: none.

## 10. Authority matrix

This `BLOCKED` Review authorizes only the original control-plane to persist the
Review as evidence and prepare the minimal Plan correction. It does not
authorize Conda creation, quick validation, source changes/PASS/Review, Pi,
runtime, Git, canonical transition, archive, Envelope, publication, completion,
or cleanup.

## 11. Validation results

| Command | Result |
|---|---|
| `openspec list` | `add-role-first-review-routing 24/41`; `add-codex-skill-update 14/40` |
| `openspec list --specs` | `skill-workflow-governance requirements 30` |
| `openspec validate add-role-first-review-routing --strict` | exit 0; valid |
| `openspec validate --all --strict --no-interactive` | exit 0; 3 passed, 0 failed |
| Router core validator | exit 0; `Core gates valid` |
| Companion template validator | exit 0; compliant |

These results did not prove Conda create, quick validation, unit suites, source
correctness/delta, Pi/runtime parity, or completion.

## 12. Verdict

`BLOCKED`

Actionable P1 `F-R5-001` remained. Immutable SHA and path bindings passed, but
the exact Task 6 Step 2 command did not mechanically guarantee immediate stop
after a guard/create/assertion failure.

## 13. Exact next action

The original bound Codex control-plane must:

1. revise only Task 6 Step 2 to add reliable fail-fast and split the occupied/
   symlink guards;
2. make Step 3 mechanically stop on its first nonzero result;
3. refresh the amendment input, Plan hash, bindings, partial-source snapshot,
   and Review prompt while preserving R4/source-start/backups;
4. obtain a fresh complete independent Conda amendment Preflight from another
   new Codex window.

Until that Review is accepted as `PASS`, do not create/activate Conda, rerun or
rewrite Tasks 1–5, resume quick validation, modify source, decide source PASS,
or perform Pi/runtime/Git/canonical/archive/publication/completion/cleanup work.
