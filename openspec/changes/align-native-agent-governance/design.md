# Native Agent Governance Consumption Design

Author: elvis. Status: proposed draft-v1. Date: 2026-10-10.

## Decisions

### 1. Reuse content without expanding formal identity

Keep one editable source for each existing skill and the shared governance
body. Preserve current portable copies and consumer links. A shared body does
not share instance identity, sessions, credentials, permissions or completion
authority. `claudex` and `claudeg` are Claude Code launchers, regardless of model
backend. Claude Code and Cursor remain content consumers/advisory reviewers;
schema 6 continues to accept only the existing four products.

An actual-entry record must distinguish product, launcher, active config root,
native instruction sources, discovered skill paths, dependency path/hash,
review delivery policy, and inspected evidence. A session's catalog may prove
shared discovery even when its private skills directory is empty. Neither that
catalog nor another account's hashes proves body execution or native loading.
Owner authority still comes from the existing bound instance and contract.

### 2. Keep the existing installer

Rulesync is a potential rules-format generator, Vercel Skills a skill installer,
and Ruler a broader rule/config generator. None is adopted: the existing
manifest transaction already binds allowlisted files, reviewed hashes, target
prestates, backups, receipts and recovery. A second live installer would have
two owners for the same outputs without addressing the observed conflicts.

Any later generator experiment must have a demonstrated missing capability,
an exact pinned version, isolated input/output roots, rules-only scope,
untouched native bytes and rollback proof. It is outside this contract.

Keep managed-rule version 6 and existing exact bodies for CCG-001, CCG-002,
CCG-010 and CCG-016. This is a hash-bound content revision within the current
format, not a target/schema/version migration. Add specific checks for the new
CCG-004/014 consumption boundaries without relaxing the existing checks.

### 3. Exact shared-rule revisions

Replace only CCG-004 with:

```text
- [CCG-004] Governed implementation outside the compact local Direct Change
  exception follows Preflight Review -> Implement -> Verify -> Review, and every
  actionable finding returns to Fix -> Verify -> Review. Compact local Direct
  Change follows `references/direct-change-rule.md`: inline readiness, required
  verification and inline self-review suffice when its bounded conditions hold.
  This exception does not waive required behavioral evidence or apply to compact
  external execution, standard/strict work, multi-slice work or protected effects.
```

Keep CCG-014's entire existing paragraph and append:

```text
  Ordinary questions and standalone read-only advisory review do not enter the
  Router or the Superpowers meta-entry merely because native defaults request
  planning or saved reports. Explicitly requested file persistence returns to
  Router classification before writing.
```

The existing Router already owns these distinctions. Do not add a blanket
"compact skips Preflight" rule, bypass selected methods, or weaken Major,
external, independent-review, evidence or completion gates.

The spec delta also modifies the existing Mandatory review correction loop
requirement's generic opening sentence with this same compact-local boundary.
It retains the full existing requirement and scenarios; that section was
verified unchanged between HEAD and the dirty main spec before drafting.
This avoids leaving a universal Preflight sentence in conflict with the new
managed rule. Main-spec integration happens only during separately authorized
archival, with all unrelated existing edits preserved.

### 4. Artifact placement and delivery

Add this canonical native-consumption rule to
`references/local-instruction-checkpoint.md`:

```text
When a plan is required, form or reuse the applicable reviewed plan before
execution. Resolve its destination from the user's authorized scope, project
conventions and existing contract. A native `docs/design/` default is only a
fallback; it cannot relocate or duplicate an already-bound plan or evidence.
An incompatible request to change an immutable binding requires a newly
approved contract, never silent path replacement.

Standalone read-only advisory output defaults to chat. Explicitly requested
persistence returns to Router classification and then respects the user's
destination and the native publisher, when that publisher applies. Saving an
advisory does not make it gate-bearing. A governed external batch writes only
its bound project-relative attempt artifacts with the assigned real product,
instance, role and evidence format. Native publisher names and batch paths
cannot substitute for each other or rewrite already-bound evidence.
```

Publisher applicability is checked before constructing a save path. If a
required native publisher cannot represent the authorized path/format, report
the conflict rather than bypassing its guard or claiming publication. The
Claude publisher's origin prefix is not integrated into formal schema-6 Review:
Claude is not a formal schema-6 product in this change. The observed header
tension is not a reproduced validator failure.

### 5. Native adaptation is a separate mutation boundary

The four-target transaction continues to modify only selected portable files
and managed blocks, preserving all outside native bytes. An alternate Codex
account, Claude global file, Cursor rule or Grok compatibility setting is not a
fifth portable target. Do not retarget the manifest destination or use a manual
copy to evade its safety checks.

The later local adaptation plan must bind each real path, current file/hash or
absence, authoritative input, exact edit, supported native mechanism, backup,
rollback and acceptance. It must preserve personal rules and prohibit credential,
session and model-config replication. For Grok, first establish whether its
installed version can exclude just the Claude-only report guard. A broad hook
shutdown can remove unrelated protection and needs its own reviewed policy;
neither outcome is pre-approved by this source change.

## Source And Runtime Work Sequence

1. Record exact approval. Read writing-skills/TDD/plan/isolation references
   selected by the Router. Preserve original workspace hashes; use an isolated
   working copy or approved worktree. Do not perform unapproved Git mutations.
2. Produce an executable source plan and distinct Preflight Review for this
   strict scope. Advisory reports are inputs, not gate signatures.
3. RED: mutations restoring universal CCG-004, removing the ordinary advisory
   exception, widening products, ignoring actual roots, overriding bound paths,
   or letting a publisher confer gate authority must be rejected by relevant
   artifact-owned checks. Record actual test failures before source edits.
4. GREEN: implement only the allowed source files; run required checks and
   behavioral proof. Keep unchanged authority/product/history rules enforced.
5. Separate Implementation Review, fix/reverify/review any findings, then
   generate a scoped sync plan selecting only changed portable files and the
   managed block; retain parity assertions for the unselected closure.
6. Review the exact plan; apply/verify each existing target, stopping and
   restoring the failed target before touching later targets. Explicitly bind
   the default Codex runtime rather than inferring it from the active account.
7. Final verification/Review and required learning promotion. Report source
   slice results separately from pending native-consumer adaptation and
   seven-entry behavioral acceptance. Do not declare whole-task completion.

## Verification

Proposal now:

```bash
openspec validate align-native-agent-governance --strict
```

Required source checks after approval:

```bash
"${PYTHON_BIN:-python3}" "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" .
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Choose a PyYAML-capable interpreter for quick validation; run the required
project suite/checks with PyYAML and with the supported dependency-free fallback.
Review also checks the unchanged Companion validator and source/runtime parity.
Four-target post-install checks remain those in the existing sync contract.

Behavioral forward cases cover each changed failure mechanism once:

| Case | Required result |
| --- | --- |
| Ordinary advisory despite native save default | Chat result; no write or fabricated Handoff |
| Compact local typo outside protected boundaries | Inline readiness/check/review; no redundant standalone Plan/Preflight |
| Compact external handoff | Required Preflight and bound attempt artifacts retained |
| Major workflow change before approval | Proposal only; no implementation |
| Plan with an existing bound path | Required before execution; existing path retained |
| Shared skill discovered from another config root | Record that source; do not infer missing skills or qualified runtime from private directory/parity alone |
| Claude launcher requesting formal product substitution | Reject substitution and advisory-to-canonical promotion |

Use native event evidence for native loading or no-tool claims. An isolated
fixture proves deterministic rejection only; correct prose or unchanged files
alone cannot prove native behavior. Missing runtime evidence remains pending or
blocked, with owner/resume condition. Keep raw traces temporary and sanitize
durable results according to `docs/engineering-invariants.md`.

## Rollback And Stop Conditions

Codex owns source rollback and reviewed sequential runtime recovery. Before
implementation, capture fresh whole-file prestates and backups outside skill
discovery. Restore only this change's edits, preserving original dirty content;
never reset/clean either repository. Target recovery uses the existing receipt
and backup mechanism, not ad hoc copies. Drift, unsupported loading evidence,
failed tests, stale/unresolved findings, or an excluded file change stops the
affected phase. Expand scope only with a revised approved contract.

The proposal-only backup remains temporary while approval/rollback decisions
are pending; its location is local and not a public distribution artifact.
