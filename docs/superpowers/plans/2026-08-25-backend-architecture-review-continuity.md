# Backend Architecture Review and Continuity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILLS: Use
> `superpowers:executing-plans` for inline execution,
> `superpowers:test-driven-development` for behavior changes,
> `superpowers:writing-skills` for Skill RED/GREEN,
> `superpowers:requesting-code-review` for the standard independent Review, and
> `superpowers:verification-before-completion` before any success claim.
> Checkboxes are static executable steps only. For this change, canonical progress is read only from active OpenSpec tasks.md. Never infer pending work from an unchecked Plan step.

**Goal:** Create one independent lightweight backend architecture Review Skill,
route only explicit specialty requests to it, keep authorized pending work
executing until an existing legal stop applies, and stop non-converging
Review/Fix loops before they widen a minimal approved need.

**Architecture:** `../backend-architecture-review` remains an independent
four-file source and Git repository. Four local runtime discovery symlinks point
to that source. Router integration changes one routing surface; execution
continuity, conditional minimal implementation, and Review/Fix convergence live
in the existing approved-implementation reference and reuse existing canonical
state, `BLOCKED`, control-plane, Review, and Completion rules. No new reference,
state, gate, or authority is introduced.

**Tech Stack:** Markdown Skill contracts, Python standard-library unittest,
OpenSpec CLI, existing cross-CLI synchronization tooling, local Git metadata.

## Execution assignment

- Executor: current Pi session, direct inline assignment under the user's exact
  scoped authorization; profile `cohesive-medium` with escalation on ambiguity.
- External Handoff: none; no external batch is dispatched.
- Proposal/Preflight/implementation/final reviewer: product `codex`, role
  `independent-reviewer`, profile `control-plane-high`, fresh ephemeral instance
  distinct from the proposal/Plan artifact author and Pi executor, authority
  `governed-review-evidence` only.
- Evidence profile: `standard` Major Self-Evolution.
- Workspace decision: the user explicitly targeted the existing local
  `openspec-superpower-change` checkout and authorized immediate implementation;
  that direct instruction is bound to the currently clean `main` checkout.
  Creating a Router worktree would require unauthorized branch/worktree Git
  mutation, so implementation stays here and stops on unrelated pre-existing
  dirt or branch drift.
- Git authority: only `git init -b main` in the new sibling is authorized. No
  staging, commit, remote, push, reset, clean, Router branch/worktree mutation,
  or publication.

## Allowed files and runtime entries

**Create in Router repository:**

- `openspec/changes/add-backend-architecture-review-continuity/**`
- `docs/superpowers/plans/2026-08-25-backend-architecture-review-continuity.md`

**Modify in Router repository:**

- `SKILL.md`
- `references/approved-implementation-workflow.md`
- `tests/test_workflow_rules.py`
- Checklist markers in
  `openspec/changes/add-backend-architecture-review-continuity/tasks.md`
- On successful archive only: update
  `openspec/specs/skill-workflow-governance/spec.md` and move the exact active
  change tree to the collision-free UTC-date path bound immediately before
  archive:
  `openspec/changes/archive/${ARCHIVE_DATE}-add-backend-architecture-review-continuity/**`

**Create in independent sibling:**

- `../backend-architecture-review/SKILL.md`
- `../backend-architecture-review/README.md`
- `../backend-architecture-review/references/review-dimensions.md`
- `../backend-architecture-review/tests-or-examples/trigger-cases.md`
- `../backend-architecture-review/.git/` via authorized `git init -b main`

**Local runtime entries:**

- `${CODEX_HOME:-$HOME/.codex}/skills/backend-architecture-review`
- `${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}/skills/backend-architecture-review`
- `${ANTIGRAVITY_CLI_HOME:-$HOME/.gemini/antigravity-cli}/skills/backend-architecture-review`
- `${GROK_HOME:-$HOME/.grok}/skills/backend-architecture-review`

Each entry must be absent before apply and become a symlink resolving exactly to
`../backend-architecture-review`. Router runtime apply may replace only the two
approved portable instruction files and must bind destination pre-state. The
current full-manifest sync transaction rewrites additional unchanged files, so
it is not authorized by this Plan; absent separately reviewed targeted tooling,
runtime sync is `BLOCKED` rather than expanded here.

---

## Implementation prestate gate

Immediately before the first RED test edit, bind the exact reviewed checkout and
source preimages. Only the five reviewed untracked contract/Plan files are
allowed; any other status entry, branch, HEAD, or target-file hash is `BLOCKED`:

```bash
/usr/bin/python3 - <<'PY'
import hashlib, json, subprocess
from pathlib import Path
root = Path('/Users/elvis/file/develop/opensource/openspec-superpower-change')
backup = Path('/private/tmp/openspec-backend-architecture-20260825T155406.klwuzW')
if subprocess.check_output(['git', '-C', str(root), 'branch', '--show-current'], text=True).strip() != 'main':
    raise SystemExit('BLOCKED: Router branch drift')
if subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip() != 'c1448d60744884f23054aa0e57608f99190aee9f':
    raise SystemExit('BLOCKED: Router HEAD drift')
raw = subprocess.check_output(
    ['git', '-C', str(root), 'status', '--porcelain=v1', '--untracked-files=all', '-z']
).decode().split('\0')
observed = {entry for entry in raw if entry}
expected = {
    '?? docs/superpowers/plans/2026-08-25-backend-architecture-review-continuity.md',
    '?? openspec/changes/add-backend-architecture-review-continuity/design.md',
    '?? openspec/changes/add-backend-architecture-review-continuity/proposal.md',
    '?? openspec/changes/add-backend-architecture-review-continuity/specs/skill-workflow-governance/spec.md',
    '?? openspec/changes/add-backend-architecture-review-continuity/tasks.md',
}
if observed != expected:
    raise SystemExit(f'BLOCKED: unrelated or missing checkout paths: {sorted(observed ^ expected)}')
manifest_path = backup / 'manifest.json'
manifest_bytes = manifest_path.read_bytes()
if hashlib.sha256(manifest_bytes).hexdigest() != '6202018a22c7a253f0cbe4854b3a6f9b09f4c778dabed376b14ee456d04c4f86':
    raise SystemExit('BLOCKED: backup manifest drift')
manifest = json.loads(manifest_bytes)
for record in manifest['records']:
    if record['target'] != 'source' or record['state'] != 'file':
        continue
    path = root / record['path']
    if path.is_symlink() or not path.is_file():
        raise SystemExit(f'BLOCKED: unsafe source preimage: {path}')
    if hashlib.sha256(path.read_bytes()).hexdigest() != record['sha256']:
        raise SystemExit(f'BLOCKED: source preimage drift: {path}')
print('implementation-prestate: PASS')
PY
```

### Task 1: RED routing and continuity regressions

- [ ] Add `test_backend_architecture_review_route_is_explicit_and_narrow` and
  `test_non_backend_architecture_review_stays_router_review_only` to
  `tests/test_workflow_rules.py`. They must require the exact specialist name,
  explicit architecture triggers, ordinary Bugfix Diff/generic Plan
  non-triggers, read-only/bounded-evidence return, unchanged ordinary Review
  ownership, and the non-backend fallback to the Router.
- [ ] Add `test_authorized_execution_continuity_reuses_canonical_state` and
  `test_plan_checkboxes_are_static_and_tasks_are_canonical` to the same file.
  They must require OpenSpec-backed `tasks.md` contract progress, Direct Change
  reuse of scoped Plan/Status/Handoff/equivalent state, no continuity-created
  OpenSpec/second ledger, static-only Plan checkboxes, pending/no-blocker/no-new-
  decision continuation, exact stop categories, compaction/session/model/agent/
  `继续` recovery, actual task action, and code-written-not-Done wording.
- [ ] Add `test_material_complexity_checkpoint_is_conditional_and_ordered` and
  `test_review_fix_nonconvergence_blocks_scope_growth` to the same file. They
  must pin the exact Need -> Repository Reuse -> Stdlib -> Platform Native ->
  Existing Dependency -> Small Local Implementation -> New Abstraction order,
  restrict it to material new complexity, exempt ordinary Bugfixes from new
  ceremony/specialist routing, retain the normal first-pass Review/Fix loop, and
  require repeated findings/regressions/conflict/scope growth to use existing
  `BLOCKED` + `control-plane-high` without `ESCALATED` or another lifecycle.
- [ ] Run:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 -m unittest \
    tests.test_workflow_rules.WorkflowRulesTest.test_backend_architecture_review_route_is_explicit_and_narrow \
    tests.test_workflow_rules.WorkflowRulesTest.test_non_backend_architecture_review_stays_router_review_only \
    tests.test_workflow_rules.WorkflowRulesTest.test_authorized_execution_continuity_reuses_canonical_state \
    tests.test_workflow_rules.WorkflowRulesTest.test_plan_checkboxes_are_static_and_tasks_are_canonical \
    tests.test_workflow_rules.WorkflowRulesTest.test_material_complexity_checkpoint_is_conditional_and_ordered \
    tests.test_workflow_rules.WorkflowRulesTest.test_review_fix_nonconvergence_blocks_scope_growth -v
  ```

  Historical first-run RED came from the absent specialist route and continuity
  section. For the current correction, the existing four tests stay GREEN while
  the two new assertions fail because proportionality/convergence rules are
  absent. Import/setup errors are not valid RED.

### Task 2: Skill pressure baseline and independent source

- [ ] Before candidate creation, freeze four answer-free prompts and one runner
  outside every repository. Each case launches a separate `--ephemeral` process;
  raw JSONL/final output stays mode `0600`, and the sanitized phase summary binds
  prompt-set SHA-256, distinct `thread_id` values, command result, and output
  hashes. The isolated root contains no project instruction file. RED checks all
  candidate discovery paths are absent; GREEN checks every link resolves to the
  candidate source. Create the fixture exactly:

  ```bash
  set -euo pipefail
  umask 077
  RUN_ROOT=/private/tmp/backend-architecture-skill-forward-20260825
  test ! -e "$RUN_ROOT"
  mkdir -m 700 "$RUN_ROOT" "$RUN_ROOT/isolated-root"
  cat > "$RUN_ROOT/cases.json" <<'JSON'
  [
    {"id":"explicit-simple-pass","prompt":"从后端架构设计、性能和稳定性角度 Review 当前接口方案。方案：在现有订单模块新增 POST /orders/{id}/confirm；Controller 只校验并调用现有 OrderService；Service 在一个本地事务中更新订单与审计表；无远程调用；沿用项目统一 DTO 和异常格式。只做 Review，不修改文件。"},
    {"id":"ordinary-bugfix-diff","prompt":"Review 一下这个 Bugfix 的 Diff：现有 OrderService 对可空备注调用 trim 导致异常，本次只增加 null guard 和对应回归测试。"},
    {"id":"overdesign-pressure","prompt":"从后端架构角度检查是否过度设计。现有单体内一个 QPS 20 的内部 CRUD，团队 3 人；方案拟拆 6 个微服务，引入 Kafka、服务网格、独立数据库和三层通用抽象。负责人要求至少给 5 个高阶改造建议。只做 Review。"},
    {"id":"transaction-rpc-defect","prompt":"做一次架构级方案 Review。Controller 同时负责订单、库存和通知；数据库事务开启后循环 500 条明细逐条调用库存 RPC，两次重复查询同一远程状态，异常后无上限立即重试，最后提交本地事务。指出真实关键问题和最小调整。"}
  ]
  JSON
  chmod 600 "$RUN_ROOT/cases.json"
  cat > "$RUN_ROOT/run-phase.py" <<'PY'
  import hashlib, json, os, stat, subprocess, sys
  from pathlib import Path
  os.umask(0o077)
  run_root = Path('/private/tmp/backend-architecture-skill-forward-20260825')
  source = Path('/Users/elvis/file/develop/opensource/backend-architecture-review')
  links = [
      Path('/Users/elvis/.codex/skills/backend-architecture-review'),
      Path('/Users/elvis/.pi/agent/skills/backend-architecture-review'),
      Path('/Users/elvis/.gemini/antigravity-cli/skills/backend-architecture-review'),
      Path('/Users/elvis/.grok/skills/backend-architecture-review'),
  ]
  if len(sys.argv) != 3:
      raise SystemExit('usage: run-phase.py <red|green> <positive-attempt>')
  phase, attempt_text = sys.argv[1:]
  attempt = int(attempt_text)
  if phase not in {'red', 'green'} or attempt < 1 or (phase == 'red' and attempt != 1):
      raise SystemExit('invalid phase/attempt')
  if phase == 'red' and any(os.path.lexists(path) for path in [source, *links]):
      raise SystemExit('RED contaminated by candidate source or discovery link')
  if phase == 'green':
      resolved = source.resolve(strict=True)
      if any(not path.is_symlink() or path.resolve(strict=True) != resolved for path in links):
          raise SystemExit('GREEN lacks exact candidate discovery')
  isolated_root = run_root / 'isolated-root'
  if any(isolated_root.rglob('*')):
      raise SystemExit('isolated root gained project/context files')
  cases_bytes = (run_root / 'cases.json').read_bytes()
  runner_bytes = Path(__file__).read_bytes()
  cases = json.loads(cases_bytes)
  command_contract = [
      '/opt/homebrew/bin/codex', 'exec', '--ignore-user-config', '--ephemeral',
      '--sandbox', 'read-only', '--skip-git-repo-check',
      '--cd', str(isolated_root), '--json',
      '--output-last-message', '<OUTPUT>', '<PROMPT>',
  ]
  digest = lambda value: hashlib.sha256(value).hexdigest()
  contract_sha = digest(json.dumps(command_contract, ensure_ascii=False, separators=(',', ':')).encode())
  out_dir = run_root / f'{phase}-{attempt}'
  out_dir.mkdir(mode=0o700)
  records, thread_ids = [], []
  for case in cases:
      raw = out_dir / f"{case['id']}.jsonl"
      err = out_dir / f"{case['id']}.stderr"
      final = out_dir / f"{case['id']}.final.md"
      input_argv = command_contract[:-1] + [case['prompt']]
      input_argv_sha = digest(json.dumps(input_argv, ensure_ascii=False, separators=(',', ':')).encode())
      command = command_contract[:-2] + [str(final), case['prompt']]
      with raw.open('xb') as stdout, err.open('xb') as stderr:
          result = subprocess.run(command, stdout=stdout, stderr=stderr, timeout=600)
      if result.returncode != 0 or not final.is_file():
          raise SystemExit(f"{phase}-{attempt}:{case['id']} failed; inspect private trace")
      for private_path in (raw, err, final):
          if stat.S_IMODE(private_path.stat().st_mode) != 0o600:
              raise SystemExit(f'unsafe output mode: {private_path}')
      events = [json.loads(line) for line in raw.read_text().splitlines() if line.strip()]
      ids = [event.get('thread_id') for event in events if event.get('type') == 'thread.started']
      if len(ids) != 1 or not ids[0]:
          raise SystemExit(f"{phase}-{attempt}:{case['id']} lacks one fresh thread identity")
      thread_ids.append(ids[0])
      records.append({
          'id': case['id'], 'thread_id': ids[0], 'returncode': result.returncode,
          'input_argv_sha256': input_argv_sha,
          'final_sha256': digest(final.read_bytes()),
          'raw_sha256': digest(raw.read_bytes()),
      })
  if len(set(thread_ids)) != len(thread_ids):
      raise SystemExit(f'{phase}-{attempt} reused a thread identity')
  prior_summaries = [json.loads(path.read_text()) for path in sorted(run_root.glob('*-summary.json'))]
  prior_ids = {item['thread_id'] for summary in prior_summaries for item in summary['records']}
  if set(thread_ids) & prior_ids:
      raise SystemExit(f'{phase}-{attempt} reused a prior thread identity')
  red_path = run_root / 'red-1-summary.json'
  if phase == 'green':
      if not red_path.is_file():
          raise SystemExit('GREEN lacks RED summary')
      red = json.loads(red_path.read_text())
      expected_inputs = {item['id']: item['input_argv_sha256'] for item in red['records']}
      observed_inputs = {item['id']: item['input_argv_sha256'] for item in records}
      for key, value in {
          'cases_sha256': digest(cases_bytes),
          'runner_sha256': digest(runner_bytes),
          'command_contract_sha256': contract_sha,
      }.items():
          if red[key] != value:
              raise SystemExit(f'GREEN changed RED contract: {key}')
      if expected_inputs != observed_inputs:
          raise SystemExit('GREEN changed exact case command arguments')
  summary = {
      'phase': phase, 'attempt': attempt,
      'cases_sha256': digest(cases_bytes),
      'runner_sha256': digest(runner_bytes),
      'command_contract_sha256': contract_sha,
      'isolated_root_inventory': [],
      'records': records,
  }
  target = run_root / f'{phase}-{attempt}-summary.json'
  with target.open('x') as handle:
      json.dump(summary, handle, indent=2, sort_keys=True); handle.write('\n')
  if stat.S_IMODE(target.stat().st_mode) != 0o600:
      raise SystemExit(f'unsafe summary mode: {target}')
  print(json.dumps({'phase': phase, 'attempt': attempt, 'result': 'captured', 'case_count': len(records)}))
  PY
  chmod 700 "$RUN_ROOT/run-phase.py"
  /usr/bin/python3 "$RUN_ROOT/run-phase.py" red 1
  ```

  Inspect only the four private final messages, then record actual failures and
  rationalizations (over-design, implementation/governance drift, missed defect,
  or verbose non-findings) in a sanitized inline RED note. A hypothetical
  baseline is invalid; raw traces remain temporary until their last Review use.
- [ ] Create `SKILL.md` with frontmatter containing only `name` and
  `description`; description starts `Use when` and limits activation to explicit
  backend architecture Review intent.
- [ ] Add sections for trigger/non-trigger boundary, seven-dimension procedure,
  verdict semantics, findings-first output, quick PASS, minimal adjustments,
  project-first evidence, and hard exclusions.
- [ ] Put detailed judgment prompts only in
  `references/review-dimensions.md`; keep governance workflows out.
- [ ] Add concise usage/source notes to `README.md` and executable behavior cases
  to `tests-or-examples/trigger-cases.md`.
- [ ] Validate the candidate and initialize its independent local Git repository:

  ```bash
  /opt/anaconda3/bin/python3 \
    "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" \
    ../backend-architecture-review
  git -C ../backend-architecture-review init -b main
  ```

  Verify no index entries, commits, or remotes were created.
- [ ] Before GREEN, create and validate each absent discovery link with this
  exact transaction. A failed candidate validator removes only the current
  exact link before stopping; a present/replaced destination is `BLOCKED` and
  is never overwritten or unlinked:

  ```bash
  set -euo pipefail
  umask 077
  SOURCE=/Users/elvis/file/develop/opensource/backend-architecture-review
  QUICK=/Users/elvis/.codex/skills/.system/skill-creator/scripts/quick_validate.py
  for DEST in \
    /Users/elvis/.codex/skills/backend-architecture-review \
    /Users/elvis/.pi/agent/skills/backend-architecture-review \
    /Users/elvis/.gemini/antigravity-cli/skills/backend-architecture-review \
    /Users/elvis/.grok/skills/backend-architecture-review
  do
    SOURCE="$SOURCE" DEST="$DEST" /usr/bin/python3 - <<'PY'
  import os
  from pathlib import Path
  source = Path(os.environ["SOURCE"]).resolve(strict=True)
  dest = Path(os.environ["DEST"])
  if os.path.lexists(dest):
      raise SystemExit(f"BLOCKED: discovery destination exists: {dest}")
  if dest.parent.resolve(strict=True) != dest.parent:
      raise SystemExit(f"BLOCKED: unsafe discovery parent: {dest.parent}")
  os.symlink(str(source), str(dest), target_is_directory=True)
  if not dest.is_symlink() or dest.resolve(strict=True) != source:
      raise SystemExit(f"BLOCKED: wrong discovery target: {dest}")
  PY
    if ! /opt/anaconda3/bin/python3 "$QUICK" "$DEST"; then
      SOURCE="$SOURCE" DEST="$DEST" /usr/bin/python3 - <<'PY'
  import os
  from pathlib import Path
  source = Path(os.environ["SOURCE"]).resolve(strict=True)
  dest = Path(os.environ["DEST"])
  if not dest.is_symlink() or Path(os.readlink(dest)) != source:
      raise SystemExit(f"BLOCKED: refusing to unlink changed destination: {dest}")
  dest.unlink()
  PY
      exit 1
    fi
  done
  ```

- [ ] Reuse the unchanged fixture and exact runner for GREEN:

  ```bash
  /usr/bin/python3 /private/tmp/backend-architecture-skill-forward-20260825/run-phase.py green 1
  ```

  Verify the RED/GREEN summaries carry the same `cases_sha256`,
  `runner_sha256`, `command_contract_sha256`, and per-case
  `input_argv_sha256`; all eight `thread_id` values are distinct, and private
  final messages show explicit trigger, ordinary non-trigger, quick PASS,
  over-design restraint, real defect, and read-only/minimal-output behavior.
  Any new rationalization returns to Skill correction and `green 2`, `green 3`,
  and later no-overwrite attempts using the same frozen runner and cases.

### Task 2A: Accepted minimal convergence RED evidence

- [ ] Preserve `/private/tmp/backend-review-convergence-forward-20260825-r1`
  as the existing answer-free behavioral RED. Sanitized inspection established
  one fresh thread, five successful source/state/target reads, a real pending
  target action, a non-`BLOCKED` final response, mode-`0600` files, and no source
  mutation. The initial post-processor rejected only the observed `/bin/zsh -c`
  wrapper; that post-processor failure does not erase the underlying behavioral
  baseline.
- [ ] Preserve the incomplete `r2` timeout evidence for audit only. Do not create
  `r3`, `r4`, another custom runner, another event lifecycle, or another state
  artifact. The user's boundary decision accepts static GREEN plus the required
  independent Source High Review adversarial convergence probe as the minimal
  forward evidence.

### Task 3: Minimal Router and continuity implementation

- [ ] In `SKILL.md`, split the broad architecture row so explicit backend
  architecture Review selects `backend-architecture-review`, while OpenSpec,
  implementation authorization, Completion, and ordinary Review stay on their
  current routes.
- [ ] Add one short boundary paragraph: generic Bugfix/Diff/Plan/acceptance Review
  does not select the specialist; specialist output is read-only bounded evidence
  and cannot mutate or decide Router canonical state.
- [ ] In `references/approved-implementation-workflow.md`, add one
  `Authorized Execution Continuity` section before inline implementation. It
  must encode:

  ```text
  approved pending task + no blocker + no new human decision -> perform next task action
  legal stop -> complete scope | BLOCKED | new decision | missing resource/authority |
                high-risk/irreversible/out-of-scope | user pause/cancel
  resume/继续 -> recover existing canonical state -> execute next approved task
  code written -> progress only; existing Acceptance/Test/Build/Verification/Evidence decide Done
  ```

- [ ] In the same existing reference, add one short conditional minimality block
  and one convergence block. Apply the ordered proportionality judgment only
  when a proposal/fix materially adds abstraction, component, layer, dependency,
  or scope; ordinary localized Bugfixes keep their current path. Preserve
  `Review FAIL -> Fix -> Verify -> Review`, but when retries repeat findings or
  regressions, fail to converge, conflict on the core boundary, widen scope, or
  accumulate complexity, stop before another widening fix and use existing
  `BLOCKED`, blocker owner/resume condition, and `control-plane-high`. Add no
  `ESCALATED`, Finding lifecycle, Quality Gate, Task Contract, second state,
  mandatory specialist Review, or new authority.
- [ ] Add one short Router-level sentence after the existing Review loop so a
  fresh implementation route cannot interpret non-convergence as an unlimited
  automatic retry. Keep detailed judgment in the existing reference.

- [ ] Run this exact six-test command; expected GREEN:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 -m unittest \
    tests.test_workflow_rules.WorkflowRulesTest.test_backend_architecture_review_route_is_explicit_and_narrow \
    tests.test_workflow_rules.WorkflowRulesTest.test_non_backend_architecture_review_stays_router_review_only \
    tests.test_workflow_rules.WorkflowRulesTest.test_authorized_execution_continuity_reuses_canonical_state \
    tests.test_workflow_rules.WorkflowRulesTest.test_plan_checkboxes_are_static_and_tasks_are_canonical \
    tests.test_workflow_rules.WorkflowRulesTest.test_material_complexity_checkpoint_is_conditional_and_ordered \
    tests.test_workflow_rules.WorkflowRulesTest.test_review_fix_nonconvergence_blocks_scope_growth -v
  ```

### Task 3A: Minimal convergence GREEN evidence

- [ ] Use the exact six-test GREEN command above as deterministic enforcement.
  Do not add or rerun a dedicated convergence runner. In the required Source
  High Review, assign a fresh independent Codex reviewer one neutral adversarial
  canonical-state scenario: repeated same finding/regression, widening scope,
  and proposed abstraction/dependency with no predeclared expected answer. The
  reviewer must confirm the implemented rules stop the widening retry through
  existing `BLOCKED` / `control-plane-high`, while an ordinary first-pass
  finding remains on the normal same-scope Fix -> Verify -> Review loop.
- [ ] Any contrary adversarial result returns to the same minimal source scope
  for fix, six-test verification, and fresh Review. It does not authorize a new
  runner, state, gate, or abstraction.

### Task 4: Router source validation and discovery recheck

- [ ] Confirm `/opt/anaconda3/bin/python3` imports PyYAML and
  `/opt/homebrew/bin/python3` remains the modern dependency-free fallback for
  project validators/tests. Revalidate the
  independent source and all four already-created exact links; a missing,
  replaced, or non-symlink entry is `BLOCKED`:

  ```bash
  /opt/anaconda3/bin/python3 -c 'import yaml; print(yaml.__version__)'
  /opt/anaconda3/bin/python3 \
    "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" \
    ../backend-architecture-review
  SOURCE=/Users/elvis/file/develop/opensource/backend-architecture-review \
    /usr/bin/python3 - <<'PY'
  import os
  from pathlib import Path
  source = Path(os.environ['SOURCE']).resolve(strict=True)
  for dest in map(Path, (
      '/Users/elvis/.codex/skills/backend-architecture-review',
      '/Users/elvis/.pi/agent/skills/backend-architecture-review',
      '/Users/elvis/.gemini/antigravity-cli/skills/backend-architecture-review',
      '/Users/elvis/.grok/skills/backend-architecture-review',
  )):
      if not dest.is_symlink() or dest.resolve(strict=True) != source:
          raise SystemExit(f'BLOCKED: discovery drift: {dest}')
  print('specialist-discovery: PASS')
  PY
  ```

- [ ] Run source checks in both parser modes:

  ```bash
  /opt/anaconda3/bin/python3 \
    "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .
  PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 scripts/validate_core_gates.py .
  PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_core_gates.py .
  PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 -m unittest discover -s tests -v
  openspec validate add-backend-architecture-review-continuity --strict
  ```

### Task 5: Review, Router runtime sync, and closeout

- [ ] Rerun continuity after the proportionality/convergence source edit as
  fresh attempt `r4`; preserve all `r1`-`r3-final` evidence and use explicit
  no-overwrite roots:

  ```bash
  set -euo pipefail
  umask 077
  RUNNER=/private/tmp/backend-architecture-continuity-agent-forward-runner-20260825-r1.py
  RUNNER_SHA256=4e3ccc8a14ec5f0559f0b3d78375b928f51f8c986ad5906f03f54c206f499fe7
  COMMAND_CONTRACT_SHA256=852dfecf0cb50c5827a3093084da8971307e736e0360654d04a75ac76d2b6227
  EVIDENCE=/private/tmp/backend-architecture-continuity-agent-forward-20260825-r4
  CWD=/private/tmp/backend-architecture-continuity-agent-cwd-20260825-r4
  test ! -e "$EVIDENCE"
  test ! -e "$CWD"
  test -e /private/tmp/backend-architecture-continuity-agent-forward-20260825-r3
  test -e /private/tmp/backend-architecture-continuity-agent-forward-20260825-r3-corrected
  test -e /private/tmp/backend-architecture-continuity-agent-forward-20260825-r3-final/summary.json
  test -e /private/tmp/backend-architecture-continuity-agent-forward-20260825-r1
  test -e /private/tmp/backend-architecture-continuity-agent-forward-20260825-r2/summary.json
  test "$(shasum -a 256 "$RUNNER" | awk '{print $1}')" = "$RUNNER_SHA256"
  /usr/bin/python3 "$RUNNER" \
    --evidence-root "$EVIDENCE" \
    --cwd-root "$CWD" >/dev/null
  EVIDENCE="$EVIDENCE" CWD="$CWD" RUNNER_SHA256="$RUNNER_SHA256" \
    COMMAND_CONTRACT_SHA256="$COMMAND_CONTRACT_SHA256" /usr/bin/python3 - <<'PY'
  import hashlib, json, os, stat
  from pathlib import Path
  evidence = Path(os.environ["EVIDENCE"])
  cwd_root = Path(os.environ["CWD"])
  runner_sha = os.environ["RUNNER_SHA256"]
  command_sha = os.environ["COMMAND_CONTRACT_SHA256"]
  summary = json.loads((evidence / "summary.json").read_text())
  assert summary["result"] == "PASS"
  assert summary["runner_sha256"] == runner_sha
  assert summary["command_contract_sha256"] == command_sha
  assert summary["baseline_scenario_count"] == 5
  assert summary["mutation_scenario_count"] == 2
  assert summary["unique_thread_ids"] is True
  assert len(set(summary["baseline_thread_ids"])) == 5
  assert len(set(summary["mutation_thread_ids"])) == 2
  assert not set(summary["baseline_thread_ids"]) & set(summary["mutation_thread_ids"])
  def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
  def mode(path): return stat.S_IMODE(path.stat().st_mode)
  def sha_json(value):
      return sha256_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())
  def sha256_bytes(value): return hashlib.sha256(value).hexdigest()
  source = {
      "/Users/elvis/file/develop/opensource/openspec-superpower-change/SKILL.md",
      "/Users/elvis/file/develop/opensource/openspec-superpower-change/references/approved-implementation-workflow.md",
  }
  bundle = b"".join(path.encode() + b"\0" + Path(path).read_bytes() + b"\0" for path in sorted(source))
  assert summary["source_sha256"] == sha256_bytes(bundle)
  for record in summary["records"]:
      assert record["runner_sha256"] == runner_sha
      assert record["input_argv_sha256"] == command_sha
      assert record["raw_mode"] == record["final_mode"] == record["stderr_mode"] == "0600"
      assert sha(evidence / "prompts" / f"{record['scenario']}.txt") == record["prompt_sha256"]
      assert sha(evidence / "raw" / f"{record['scenario']}.jsonl") == record["raw_sha256"]
      assert sha(evidence / "final" / f"{record['scenario']}.md") == record["final_sha256"]
      assert record["fixture_sha256"] == sha_json(record["fixture_files"])
      for name, digest in record["fixture_files"].items():
          assert sha(Path(record["cwd"]) / name) == digest
  for record in summary["mutation_probe"].values():
      assert record["result"] == "RED" and record["agent_trace"] == "PASS"
      assert record["contract_check_returncode"] != 0
      assert record["source_sha256"] == summary["source_sha256"]
      assert record["raw_mode"] == record["final_mode"] == record["stderr_mode"] == "0600"
      assert sha(evidence / "raw" / f"{record['scenario']}.jsonl") == record["raw_sha256"]
      assert sha(evidence / "final" / f"{record['scenario']}.md") == record["final_sha256"]
      assert sha(evidence / "prompts" / f"{record['scenario']}.txt") == record["prompt_sha256"]
      assert record["fixture_sha256"] == sha_json(record["fixture_files"])
      for name, digest in record["fixture_files"].items():
          assert sha(Path(record["cwd"]) / name) == digest
  for path in evidence.rglob("*"):
      assert mode(path) == (0o600 if path.is_file() else 0o700)
  assert cwd_root.is_dir()
  print("r4-summary/hashes/modes/threads: PASS")
  PY
  ```

  This single exact invocation was the continuity rerun. It completed seven
  real unique-thread scenarios but returned a mechanical false negative before
  summary creation because the reverse mutation read the exact isolated files
  through CWD-relative paths while the frozen post-processor required absolute
  path strings. The user explicitly accepted the r4 semantic evidence: all
  turns completed, files remained mode `0600`/directories `0700`, baseline
  pending/resume/`继续` performed target actions, BLOCKED/pause did not, both
  mutation agents read the intended files, and the reverse contract check was
  RED. Do not modify the runner or create r5. Sanitized semantic evidence is
  `/private/tmp/backend-architecture-continuity-r4-semantic-acceptance-20260826-r1.json`,
  mode `0600`, SHA-256
  `4187ca7b4e64a9d1345d43fbb950ef6533724d115fa20d9e56a217b77383ba7c`.
  Source High Review must audit this resolution and may reject it if relative
  paths do not resolve exactly inside the bound isolated CWD.

- [ ] Ask a fresh ephemeral read-only Codex reviewer to inspect actual files,
  both repository states, complete Router diff, sibling contents, source-to-route
  discovery wiring, tests, docs/contracts, one adversarial trigger probe, and
  the neutral non-converging Review/Fix scenario defined in Task 3A. Every
  finding returns to fix -> focused verification -> Review; do not add a
  dedicated convergence runner.

- [ ] After source Review PASS, audit the current full-manifest planner without
  applying it. It is eligible only if each runtime mutation set contains exactly
  the two approved Router destinations and no Companion/global-rule/unchanged
  entry. Current tooling is expected to fail that eligibility check; preserve a
  sanitized mode-`0600` blocker and stop Task 5.4:

  ```bash
  set -euo pipefail
  umask 077
  SYNC_ROOT=/private/tmp/add-backend-architecture-review-continuity-20260825-sync-audit-r2
  FAILED_ROOT=/private/tmp/add-backend-architecture-review-continuity-20260825-sync-audit
  test -d "$FAILED_ROOT"
  test ! -e "$FAILED_ROOT/full-plan.json"
  test ! -e "$FAILED_ROOT/runtime-backups"
  test ! -e "$FAILED_ROOT/runtime-transactions"
  test ! -e "$SYNC_ROOT"
  mkdir -m 700 "$SYNC_ROOT"
  PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_cross_cli_sync.py plan \
    --manifest references/cross-cli-portable-manifest.json \
    --openspec-source /Users/elvis/file/develop/opensource/openspec-superpower-change \
    --brief-source /Users/elvis/file/develop/opensource/codex-brief-antigravity-review \
    --codex-skills-root /Users/elvis/.codex/skills \
    --codex-rule-file /Users/elvis/.codex/AGENTS.md \
    --pi-skills-root /Users/elvis/.pi/agent/skills \
    --pi-rule-file /Users/elvis/.pi/agent/APPEND_SYSTEM.md \
    --antigravity-skills-root /Users/elvis/.gemini/antigravity-cli/skills \
    --antigravity-rule-file /Users/elvis/.gemini/GEMINI.md \
    --grok-skills-root /Users/elvis/.grok/skills \
    --grok-rule-file /Users/elvis/.grok/AGENTS.md \
    --output "$SYNC_ROOT/full-plan.json" >/dev/null
  PLAN="$SYNC_ROOT/full-plan.json" BLOCKER="$SYNC_ROOT/blocked-targeted-sync.json" \
    /opt/homebrew/bin/python3 - <<'PY'
  import json, os, stat
  from pathlib import Path
  plan = json.loads(Path(os.environ["PLAN"]).read_text())
  expected = {"SKILL.md", "references/approved-implementation-workflow.md"}
  targets = {}
  eligible = True
  for target_id, target in plan["targets"].items():
      router = [item for item in target["files"] if item["skill"] == "openspec-superpower-change"]
      companion = [item for item in target["files"] if item["skill"] == "codex-brief-antigravity-review"]
      router_paths = {item["path"] for item in router}
      target_ok = router_paths == expected and len(router) == 2 and not companion and not target.get("rule_file")
      eligible = eligible and target_ok
      targets[target_id] = {
          "eligible": target_ok,
          "router_candidate_count": len(router),
          "companion_candidate_count": len(companion),
          "global_rule_candidate_count": 1 if target.get("rule_file") else 0,
      }
  value = {
      "result": "PASS" if eligible else "BLOCKED",
      "blocker_owner": "control-plane-high",
      "reason": "current transaction is not an exact two-Router-file mutation set",
      "resume_condition": "provide a separately approved and reviewed prestate-bound exact two-path sync mechanism",
      "targets": targets,
  }
  blocker = Path(os.environ["BLOCKER"])
  with blocker.open("x") as handle:
      json.dump(value, handle, indent=2, sort_keys=True); handle.write("\n")
  os.chmod(blocker, 0o600)
  assert stat.S_IMODE(blocker.stat().st_mode) == 0o600
  assert not eligible, "unexpected eligible targeted transaction requires fresh Sync-plan Review"
  print("runtime-sync: BLOCKED_TARGETED_TOOLING")
  PY
  test ! -e "$SYNC_ROOT/runtime-backups"
  test ! -e "$SYNC_ROOT/runtime-transactions"
  ```

  Attempt `sync-audit` is preserved empty: `/usr/bin/python3` 3.9 rejected the
  modern validator before plan creation. `sync-audit-r2` uses the project
  baseline `/opt/homebrew/bin/python3`; this interpreter correction does not
  authorize runtime mutation. Do not call `apply`, manually copy files, or modify
  `scripts/validate_cross_cli_sync.py` in this change. A later exact targeted
  mechanism requires its own approved scope, prestate-bound plan, independent
  Sync-plan Review, per-target rollback/verification, and fresh source/runtime
  Review. Platform permission cannot waive this blocker.

- [ ] Only after a separately authorized targeted sync resolves Task 5.4 with
  PASS, verify all four Router copies and all four specialist links, run Project
  Learning Closeout, reconcile tasks, and archive before fresh final validation
  and final independent Review. While `BLOCKED_TARGETED_TOOLING` remains, do not
  enter this step, reconcile the change, archive, clean backups, or claim
  Completion. Archive exactly:

  ```bash
  ARCHIVE_DATE=$(date -u +%F)
  ARCHIVE_DEST="openspec/changes/archive/${ARCHIVE_DATE}-add-backend-architecture-review-continuity"
  test ! -e "$ARCHIVE_DEST"
  test -d openspec/changes/add-backend-architecture-review-continuity
  openspec archive -y add-backend-architecture-review-continuity
  test -f "$ARCHIVE_DEST/proposal.md"
  test ! -e openspec/changes/add-backend-architecture-review-continuity
  count=$(find openspec/changes/archive -maxdepth 1 -type d \
    -name '*-add-backend-architecture-review-continuity' | wc -l | tr -d ' ')
  test "$count" = 1
  openspec validate --all --strict --no-interactive
  ```

  Bind the UTC destination and collision-free prestate immediately before the
  archive command; do not reuse the obsolete review-draft date. Archive may
  update only `openspec/specs/skill-workflow-governance/spec.md` and move the
  exact active change tree to the bound archive path. Any other path is scope
  drift. After archive and strict validation, run fresh final whole-task
  verification and independent Review; pre-archive evidence cannot authorize
  Completion. Remove only this task's validated temporary backup after that
  final Review and rollback needs all resolve.

## Rollback and stop conditions

After an explicit rollback decision, restore only the three exact Router source
preimages from the bound backup. Keep OpenSpec/Plan audit artifacts and sibling
source for user disposition; do not delete them implicitly:

```bash
/usr/bin/python3 - <<'PY'
import hashlib, json, os, stat, tempfile
from pathlib import Path
root = Path('/Users/elvis/file/develop/opensource/openspec-superpower-change')
backup = Path('/private/tmp/openspec-backend-architecture-20260825T155406.klwuzW')
manifest_path = backup / 'manifest.json'
manifest_bytes = manifest_path.read_bytes()
if hashlib.sha256(manifest_bytes).hexdigest() != '6202018a22c7a253f0cbe4854b3a6f9b09f4c778dabed376b14ee456d04c4f86':
    raise SystemExit('BLOCKED: backup manifest drift')
manifest = json.loads(manifest_bytes)
records = {
    record['path']: record for record in manifest['records']
    if record['target'] == 'source' and record['state'] == 'file'
}
expected = {
    'SKILL.md',
    'references/approved-implementation-workflow.md',
    'tests/test_workflow_rules.py',
}
if set(records) != expected:
    raise SystemExit('BLOCKED: unexpected source backup closure')
for rel in sorted(expected):
    source = backup / 'source' / rel
    target = root / rel
    record = records[rel]
    if source.is_symlink() or not source.is_file() or target.is_symlink() or not target.is_file():
        raise SystemExit(f'BLOCKED: unsafe restore path: {rel}')
    data = source.read_bytes()
    if hashlib.sha256(data).hexdigest() != record['sha256']:
        raise SystemExit(f'BLOCKED: backup content drift: {rel}')
    fd, tmp_name = tempfile.mkstemp(prefix=f'.{target.name}.rollback.', dir=target.parent)
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(data); handle.flush(); os.fsync(handle.fileno())
        os.chmod(tmp_name, int(record['mode'], 8))
        os.replace(tmp_name, target)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
print('source-restore: PASS')
PY
/opt/anaconda3/bin/python3 \
  "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .
PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 scripts/validate_core_gates.py .
PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3 -m unittest discover -s tests -v
```

For specialist-link rollback, unlink only entries whose `lstat` type is symlink
and whose raw absolute target plus resolved target still equal the independent
source; any changed object is `BLOCKED` and preserved. Runtime Router rollback
uses only the current target's reviewed `restore-target` receipt before later
targets run.

Stop on preimage drift, present specialist destination, validator/test/Review
failure, unresolved finding, missing independent reviewer, scope expansion,
credential/resource requirement, unsafe path, or unauthorized Git/publication
action. Do not stop after a successful subtask while approved pending tasks
remain and no stop condition applies.
