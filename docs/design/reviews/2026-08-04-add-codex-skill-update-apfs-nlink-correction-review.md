# APFS parent-link correction independent Review

## Review identity and verdict

- Change: `add-codex-skill-update`
- Reviewer: `/root/recovery_proposal_review`
- Review profile: independent, read-only, adversarial High/Proposal Review
- Date: `2026-08-04`
- Final verdict: **PASS**

This PASS covers the APFS parent-link fail-closed correction and its current
proposal evidence only. It does not approve implementation and does not replace
a new exact user approval or a new immutable authorization manifest.

## Reviewed scope

- `CONTEXT.md`
- `openspec/changes/add-codex-skill-update/proposal.md`
- `openspec/changes/add-codex-skill-update/design.md`
- `openspec/changes/add-codex-skill-update/tasks.md`
- `openspec/changes/add-codex-skill-update/specs/skill-update-governance/spec.md`
- `docs/design/2026-07-30-governed-skill-update-review-draft.md`
- `docs/design/evidence/add-codex-skill-update/source-bootstrap-v2-helper.py`
- `docs/design/evidence/add-codex-skill-update/source-bootstrap-v2-prestate.json`
- `docs/design/evidence/add-codex-skill-update/test_source_bootstrap_v2_helper.py`
- `docs/design/evidence/add-codex-skill-update/2026-08-04-task-2.1-apfs-nlink-fail-closed.md`
- immutable failed authorization manifest
  `7df5c5ee0d3022dbed1f19c5de9e16855982b06c20fca49b99ffc742e9c3c0ff`
  and its four raw snapshots

## Root cause and no-source-write boundary

The failed exact v2 authorization used a schema-2 prestate captured before its
new immutable manifest existed. On the bound APFS volume, creating that regular
manifest file increased `approvals/` `st_nlink` from `7` to `8`. The old helper
incorrectly compared the post-decision directory against the unadjusted
pre-decision value and returned `BLOCKED_SOURCE_WORKTREE_RECOVERY`.

The failure occurred before the helper created its operation lock or journal
and before any replacement source or Git state. Read-only evidence confirmed
that the v2 ref, reflog, worktree-admin directory, replacement worktree, lock,
journal, and sibling source remained absent. The prior quarantined worktree,
ref, admin identity, manifest evidence, and missing-evidence closure remained
unchanged.

The corrected helper uses one closed phase table for both lexical `lstat` and
retained-descriptor `fstat` validation:

- `approval-recorded`: pre-decision baseline plus the new manifest;
- `journal-ready`: that manifest plus the held approval-directory lock and the
  source-bootstrap journal;
- `post-bootstrap`: those entries plus exactly the final ref, reflog,
  worktree-admin directory, and replacement worktree in their respective
  parents.

Every unlisted delta and every unknown phase remains blocking. The current
canonical prestate contains 23 parent-closure entries and matches the live
device, inode, owner, mode, and baseline link counts exactly, including
`approvals/ = 8` and `source-bootstrap/ = 3`. A newly recorded manifest must
therefore produce `approvals/ = 9`; lock and journal readiness requires
`approvals/ = 10` and `source-bootstrap/ = 4`; final ref, reflog, admin, and
worktree parents each admit only their declared `+1`.

## Initial findings and corrections

### High 1: prior-profile wording contradicted the mechanism

The first reviewed correction still prohibited copying or adopting any
prior-attempt profile, while the current helper intentionally expects the same
content-addressed `eb8ddf6e...` profile bytes previously bound by the failed
`7df5...` decision.

Correction: proposal, design, tasks, spec, and review evidence now distinguish
authority from immutable mechanism content. Existing profile bytes may be used
only when the current helper independently verifies exact expected bytes, a new
manifest binds the hash, and a new exact user decision approves it. The old
manifest grants no authority. The quarantined `892aec1c...` profile remains
rejected by the current expected-bytes/hash check.

### High 2: the focused regression sampled rather than closed the phase table

The first focused test used the historical `7 -> 8` example and sampled only
some paths, so an undeclared delta on an untested parent could have escaped the
test despite the contract requiring every allowed phase delta to be bound.

Correction: the five-test suite now asserts exact equality of the complete
`PARENT_NLINK_DELTAS` map, reads the current canonical prestate baseline
(`8 -> 9 -> 10` for the approval directory), checks all 23 closure paths across
all three phases, verifies every `validate_prestate`, retained-binding, and
post-only phase call through AST inspection with no default phase, proves an
unlisted parent has zero delta, and proves an unknown phase blocks.

After these corrections, no actionable finding remained.

## Final reviewed hashes

| Artifact | SHA-256 |
|---|---|
| `CONTEXT.md` | `cc89523a5b5bf720c9221a8c8f96ef254eedf085276175f508f21b1aa1166229` |
| `proposal.md` | `a028040388bff09a12f9debcb7a426c9f560d62765a3e9447a4e9f7a06c01a72` |
| `design.md` | `242b4fa1a6ba9f90d3e61712a286d77d2033934194153b8b02cb6edac88ff02c` |
| `tasks.md` | `a08f1a678dcd602848ee5b123313b2a2c47fa2d790d26489b3a55dbf1f7486ef` |
| `specs/skill-update-governance/spec.md` | `e894076dd8a16cea72d1aee480937f8180aadfd6baffdd9bfc57dffd6fe172a8` |
| `docs/design/2026-07-30-governed-skill-update-review-draft.md` | `d8823e7fb47dd4d6a2f42495d0d88183ae45911d41b4b9ada92579b86e3d5659` |
| `source-bootstrap-v2-helper.py` | `a0fc43a8420ec13c0131330d0e52cbe369425f6f9b6920462dab731ad4773e72` |
| `source-bootstrap-v2-prestate.json` | `6a8a2117be05a04891cbf42a6c3710eff035ac940b98e4ebdce5cbf932a34cdf` |
| `test_source_bootstrap_v2_helper.py` | `3da212b333b9dca862f7f0d47f8e841d46f352a02ef542d8d47e5c93ad7cf9b2` |
| `2026-08-04-task-2.1-apfs-nlink-fail-closed.md` | `5cc282615d7597ef54c3065f6f57b61fefb4acdc5eed06f057708ab76c7d6ae3` |

The source-bootstrap prestate domain digest, computed as SHA-256 over the exact
UTF-8 prefix `source-worktree-bootstrap-prestate-v2`, one NUL, and the canonical
prestate bytes with their single final LF removed, is:

`ade026b7146ad39dcd665c0268267625df1b4f1cbbe5ccd63a0c9ac058f70454`

## Verification evidence

The reviewer ran these commands against the final reviewed artifact bytes:

```bash
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3.11 -m unittest -v \
  docs/design/evidence/add-codex-skill-update/test_source_bootstrap_v2_helper.py
DO_NOT_TRACK=1 openspec validate add-codex-skill-update --strict --no-interactive
PYTHON_BIN=/opt/anaconda3/bin/python3.11 \
  /opt/anaconda3/bin/python3.11 \
  /Users/elvis/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Results:

- focused APFS regression: `5/5 PASS`;
- strict OpenSpec validation: `PASS`;
- Skill quick validation: `PASS`;
- core gates: `PASS`;
- project tests: `142/142 PASS`.

Additional read-only checks established:

- all 23 prestate parent-closure device/inode/uid/mode/`nlink` tuples match;
- the immutable `7df5...` manifest remains canonical and hashes to its filename;
- all four snapshots bound by `7df5...` remain present and hash to their names;
- `7df5...` still binds the prior helper hash
  `2823d197a8faa73c19766103ca64926dedcc670b1dcc816942075ccaa929ee43`
  and prior prestate domain digest
  `41c5747beef62fb666200730139a0195e34eab078d97b88ce2128420c522506d`;
- the corrected helper's fixed `--launch` returns exit `70` with zero current
  authorization-manifest matches;
- `refs/heads/add-codex-skill-update-v2`, its reflog,
  `.git/worktrees/add-codex-skill-update-v2`, the replacement worktree,
  `approvals/source-bootstrap.lock`,
  `approvals/source-bootstrap/recovery-v2-journal.jsonl`, and
  `/Users/elvis/file/develop/opensource/codex-skill-update` remain absent.

## Authority boundary

The failed `7df5...` manifest and its snapshots are immutable historical
evidence only and are neither rewritten nor reused as current authority. The
content-addressed `eb8ddf6e...` profile is authority-neutral mechanism content:
it requires independent expected-byte verification, binding by a new manifest,
and inclusion in a new exact user decision. No previous manifest or profile use
can authorize the corrected helper.

Accordingly, this Review PASS permits the control plane to present the exact
corrected revision for approval. It does not itself authorize task 2.1, create a
manifest, or permit any source, Git, runtime, registry, schedule, Bootstrap
Control Root, publication, or cleanup mutation.
