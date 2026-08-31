# Design: optimize-closed-loop-runtime-routing

Artifact revision: `v1.15`

## Design intent

Keep the Router as the single semantic owner. Reuse the current authorization,
Confirmation Lease, canonical Plan/Status/Handoff, schema 6, validators, tests,
portable manifest, and runtime transaction. Add no second state or validation
system.

The implementation is documentation-driven and therefore uses direct semantic
assertions in existing test files. Test infrastructure must not be more complex
than the behavior it proves.

## Decisions

### 1. Bounded closed-loop continuation

`references/approved-implementation-workflow.md` owns the complete rule:

- the four continuation phrases mean continuous progress only inside the
  already-approved scope;
- accepted recommendations and implementation-detail choices are not
  reconfirmed;
- only a material product/business/architecture/security/compatibility/
  acceptance decision asks one focused question;
- status reporting is progress, not a disguised confirmation request;
- canonical state, not the last chat response, restores work after compaction,
  a new window, an agent/model switch, or “继续”;
- all existing approval, Review, verification, completion, production,
  database, external-effect, destructive, and Git boundaries remain.

`SKILL.md`, the Confirmation Lease reference, and the Companion point to or
present that rule without creating another authorization mechanism.

### 2. Non-authoritative runtime advice

`agent-capability-routing.md` owns one short default table:

| Work | Default suggestion |
|---|---|
| Ordinary OpenSpec revision, `writing-plans`, routine read-only Review | Codex high |
| Cross-Track, complex security, difficult Preflight, final gate Review | Codex xhigh |
| Closed-contract cohesive implementation | Luna Max |
| Small mechanical edit | current sufficient lower-cost mode |

Model/reasoning advice never changes `agent_product`, control-plane role,
executor/reviewer role, capability/evidence profile, approval, authority, or
PASS.

Only an actual switch produces one complete block:

```text
运行环境建议：
- 目标 Session：
- 推荐模型：
- 推理强度：
- 切换原因：
- 可复制任务提示词：
- 完成后切回：
```

If no switch occurs, omit the block. Downstream Brief/dispatch surfaces copy an
existing block verbatim and never regenerate it. The block remains outside the
machine-readable Handoff marker and canonical `status.md`.

### 3. Proportional design and test budget

The global workflow selects the smallest adequate implementation and evidence:

1. reuse an existing rule, template, validator, fixture, and test location;
2. prefer direct assertions over a new schema/registry/runner;
3. add an abstraction only when the approved behavior cannot be expressed or
   verified safely with existing mechanisms;
4. keep compact tasks compact;
5. stop and simplify when support machinery exceeds the changed behavior.

TDD scope is the current task:

- RED/GREEN targets changed behavior and credible regressions;
- a test is relevant only when it covers an acceptance scenario, a changed
  contract, or a demonstrated blast radius;
- do not create or run unrelated test matrices for ceremony;
- broader suites remain required only when an existing gate or shared-file
  blast radius makes them relevant;
- proportionality never permits skipping a relevant safety, compatibility,
  validator, Review, or completion gate.

### 4. Minimal tests

Use the existing `tests/test_workflow_rules.py` in each repository. Keep three
named focused tests that directly inspect the governing files and collectively
cover the eleven acceptance scenarios. Do not use an LLM simulator, custom
fixture schema, checker registry, sensitivity framework, or forward runner.

Implementation RED/GREEN is limited to the six focused tests. Final source
verification runs each repository's existing complete unittest suite exactly
once because the changed global Skill/template files have repository-wide
consumers. It also runs:

- Router `validate_core_gates.py`;
- Companion `validate_templates.py`;
- both existing `quick_validate.py` checks;
- strict OpenSpec validation;
- Handoff reference byte parity and unchanged schema-6 marker;
- forbidden scans for new states/profiles and Luna in `agent_product`;
- read-only `git diff --check`.

`test_cross_cli_sync.py` is not part of focused RED/GREEN. After its temporary
v1.14 additions are removed and its final diff is zero, it runs only as part of
the single existing full-suite completion gate. Existing portable sync commands
remain the deployment gate.

## Removal plan

Delete only v1.14 artifacts created for this change:

- Router closed-loop fixture/schema/output-schema, forward runner, legacy
  adapter and legacy fixtures;
- Companion closed-loop fixture/schema;
- v1.14 classifier test additions in Router
  `tests/test_cross_cli_sync.py`;
- the v1.14 addition to Companion
  `references/handed-off-external-execution.md`, restoring its existing
  governor hash contract.

Rewrite the two new workflow-test classes so they no longer import those
artifacts. Do not delete or modify pre-existing transaction residue.

## Compatibility and rollback

- Handoff schema 6, marker fields, lifecycle values, hashes, and authority
  checks remain unchanged.
- Both Handoff references are byte-identical; old Handoffs without runtime
  advice remain valid.
- The existing structured preimage backup covers every retained source/runtime
  path. Removed v1.14-only files were originally absent and can be recreated
  from retained evidence if needed.
- Runtime synchronization uses the existing portable manifest and four-target
  transaction. No sync code or transaction state changes.

## Completion boundary

Completion requires focused GREEN; one full-suite source gate; relevant
validators and strict validation; a control-plane Review of the scoped
path/hash plan and target snapshots before apply; four-target parity; and one
independent gate-bearing final Review after synchronization. Clean only this
change's temporary backup/evidence after rollback is no longer needed. Git
writes and transaction-residue cleanup remain forbidden.
