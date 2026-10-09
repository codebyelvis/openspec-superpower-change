# S9 续跑证据分阶段审查者绑定：审查草稿

作者：elvis。日期：2026-10-09。版本：draft-v1。状态：Major／仅提案，未批准实施。
change-id：support-stage-specific-resume-review。

## Gate 0 与本轮授权

Self-Evolution／proposal-only；证据绑定、兼容及恢复生命周期属于 Major，后续
采用 strict。使用 openspec-superpower-change 的迭代、Self-Evolution、提案、
Project Session Resume 规则；材料选择按当前决策取行。因兼容和不可变上下文
的设计需要明确裁决，选择 superpowers:brainstorming（architectural），映射到
唯一 OpenSpec design，不创建第二份 Superpowers 合同。没有选择实施技能。

用户要求后续自行闭环推进、不再逐步询问；本轮据此自行完成 S8 已发现前置
问题的审查草稿、OpenSpec 待批草案及校验。推荐兼容/修订方案是供具体批准
的建议，不记成已接受决定；通用继续/编辑授权不批准尚未存在的 Major。
S8 CURRENT 与 canonical blocked 保留，本轮不是 S8 实施或第二个运行时任务。

## 已观察失败与期望行为

S8 的独立 FULL_PREFLIGHT F1 和控制面真实临时文件转换分别确认：现有
_resume_review 对 implementation-review 和 final-review 使用同一个不可变
context.reviewer_assignment；s8-review-01 能进入最终验证，s8-final-01 在
完成转换被拒。同实例控制例被接受但违反 S8 已批准的 distinct Final；替换
已有 context 被 readonly kind/context 拒绝。来源为 [独立 Preflight](2026-10-08-S8-preflight-full.json) 和
[控制面诊断](2026-10-08-S8-major-prerequisite-conflict.json)，均是
诊断/阻塞证据，不能改签为实施 PASS。

期望 strict 本地上下文能在批准时分别绑定两阶段 reviewer，在恢复、进入
最终验证和完成时按阶段核对完整七字段 assignment。保留实际 previous
revision/SHA、verified checkpoint、独立身份及控制面完成权。
旧单 assignment、standard/compact、完整外部 Handoff 和历史记录保持原义。

## 方案与推荐（待具体批准）

1. 推荐：在现有 Resume Context.reviewer_assignment 内增加 strict-local
   专用的两阶段精确映射；旧七字段 assignment 按原规则处理。另增加显式、
   经具体批准的受限 context 修订转换，解除 S8 的已绑定旧格式阻塞。
2. 仅增加新格式，不提供修订转换：代码较少，但 S8 已绑定旧 context 仍不能
   恢复；日后仍须另行批准/实现修订机制，不能称已解决当前阻塞。
3. 从 Plan/Review 输出临时选 Final、复用同实例或直接重写 context：不能保证
   批准时绑定和历史完整性，不作为可接受实现方案。

本草案推荐第 1 项，并把修订的具体 S8 路径、原合同 hash、身份和最小字段
差异纳入同一个 S9 待批合同。批准前不改兼容语义或 S8 绑定。

## 拟改文件与排除项

批准后的代码/规则只改 references/approved-implementation-workflow.md、
scripts/validate_core_gates.py、tests/test_workflow_rules.py、CHANGELOG.md。
另允许 S9 自身合同/批准/Plan/Review/脱敏验证及迭代状态工件。
唯一其他 change 的受限修订目标：新增
openspec/changes/add-project-document-ownership/resume-contract-v2.md，并通过
已验证转换更新其 canonical status；保留原 approval、proposal/design/spec、
tasks 和 S8 实施内容。S8 Plan 后续沿原批准范围恢复，不由 S9 签发 readiness。

本轮实际编辑仅本草稿、四份 S9 OpenSpec 草案、提案验证记录、BACKLOG、
CURRENT 与 S8 blocked 状态的合法同阶段元数据转换。源规则/测试不编辑。
禁止改 SKILL 触发/路由、OpenSpec 必需边界、Superpowers 选择权、外部
schema-6/schema-2、companion、共享治理、manifest、CLI 目标、分发生成物、
AGENTS/CONTEXT、其他历史、业务文档、生产、依赖和其他仓库。

## 拟议规范片段（尚未生效）

> For a new strict local Resume Context, reviewer_assignment MAY instead contain
> exactly implementation-review and final-review, each a complete existing
> seven-field assignment. Bind each Review to its named phase; validate both
> assignments on every load. The two instances SHALL be distinct from each
> other and the bound controller/executor. Malformed or mixed forms fail closed.
> Existing single assignments and all external contracts retain their rules.

> Context remains immutable on ordinary transitions. A specifically approved,
> explicit strict-local reviewer-binding amendment MAY change only the hashed
> context reference and the required revision increment while both actual prior
> and proposed states are blocked, unverified and otherwise identical. Preserve
> the old approved contract and evidence. No amendment advances readiness or
> grants execution/completion authority.

完整格式、批准绑定、S8 唯一修订与负例验收写在同 change 的 design/spec。

## 验证、前向证明与审查计划

本轮：new-change strict、quick_validate、core 双解析、现有 resume/iteration
相关测试双解析、相对链接/工件范围与 44 个无关文件检查。均只检验提案和
现有行为，不构成新规则 GREEN、Preflight 或独立实施/Final PASS。

批准后：先对旧 validator 执行阶段映射/修订的 RED，再实现并 GREEN；在
私有临时项目实际创建批准上下文、执行验证命令、持久化状态和双阶段审查，
跨窗口读回；另验证显式受限修订，实际旧上下文/hash 不变，修订后仍 blocked。
确定性负例覆盖混合/缺字段/额外字段/错误阶段/身份复用/降级/陈旧证据、
无批准的 context 旋转、越权修订/非 blocked/已 verified/非实际 previous、
授权作用域/hash 漂移、atomic verify-review-complete 和外部路径。

运行 quick/core 与完整现有 unittest（PyYAML 和无依赖解析器）、严格 change
验证。独立 Plan Preflight、Implementation Review、Final Review 分阶段保留；
S9 自身可按现有单 assignment bootstrap，两个审查阶段分开且 reviewer 与
作者/执行者独立，不强行把 S8 的额外 distinct-Final 条款施加于旧 S9 context。
模型均为 gpt-6.1-sol/high。S8 原 Preflight BLOCKED 不复用为 PASS。

仅两份已在 manifest 的便携文件（approved-implementation-workflow 和
validate_core_gates）变化时，按既有四端 scoped plan/apply/verify-all 同步；
不添加 selector/目标或改共享治理。Gate PASS 后才使用该具体轮的 Git 租约。

## 备份与回滚

结构化 proposal 备份：
/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/openspec-S9-proposal-m7fgte0p。
manifest 保留源/运行时快照、HEAD、44 个无关文件 hash、全部 S8 当前工件。
保留此前 S8 备份。尚未实施/同步/push，备份保留至批准或回滚决策完成。

仅提案回滚应按 manifest 恢复 CURRENT/BACKLOG 并在恢复后用实际 previous
验证合法 S8 blocked 转换，不直接倒退 revision/覆盖 canonical；删除本轮
新草案。不得 reset/clean、恢复无关文件或改运行时。实施前另建新备份；
需要运行时回滚时使用既有 sync 事务，已经持久化的新 context 不自动倒转。


## Specific Approval Record

The earlier proposal-only labels above record the drafting phase. Current
specific decision: approved for draft-v1 scoped implementation. Actual user
message: “：迭代优化skill：已批准 support-stage-specific-resume-review”.
This decision approves the four OpenSpec artifacts below, not a second design.
Their exact approved bytes are preserved in the structured implementation backup.
Only tasks checkbox progress may change without changing the approved contract.

The existing review draft is the stable scoped approval-record location for
factual Resume Context metadata, remaining resolvable after the OpenSpec change
archives. It does not replace the OpenSpec contract or add an approval workflow.
After this factual append it is frozen and hash-bound; no later Review/closure
result is appended to this file. Separate evidence files own those later results.

| Approved artifact | SHA-256 at approval |
|---|---|
| openspec/changes/support-stage-specific-resume-review/proposal.md | e56402cee634a79af67fd062aee28c8e27d45c8e8bdc4ea9de0412f21f773b14 |
| openspec/changes/support-stage-specific-resume-review/design.md | e2206d3f0bef80a635c4102eee94a3bcd86af80894a2d8fdd69f525664f472bb |
| openspec/changes/support-stage-specific-resume-review/tasks.md | 4744c41bd1f79e9bb6f85e22651547a042e7aa18849094b0417380af5b443d0a |
| openspec/changes/support-stage-specific-resume-review/specs/skill-workflow-governance/spec.md | 4151536cbdd3cb668bfc1b2a5af2b6e00a11a197890db1694f27b3c13b9ac1f0 |

Bound controller/author/executor: Codex /root, existing contract instance
s8-control-01, control-plane/control-plane-high. No identity transfer occurs.
Plan Preflight: Codex s9-preflight-01, independent-reviewer/control-plane-high,
distinct from controller/author/executor, governed-review-evidence.
Implementation and Final use Codex s9-review-01 through separate dispatches/gates,
distinct from author/executor. This unchanged-format bootstrap is expressly
allowed by S9 design; S8 still requires its own distinct Final instance.
All actual reviewers and native proof instances use gpt-6.1-sol/high.

The fixed command grants this one S9 round's authorized main-workspace edits,
validation, existing four-target two-file sync and scoped repository
add/commit/current-branch push after all required gates. No target/manifest,
companion/shared governance, other repository, production/release, destructive
Git or S8 implementation authority. S8 amendment is the exact metadata-only
scope below, subject to source proof, Implementation Review and sync first.

Git publishes S9 source/contracts/own status and immutable sanitized amendment
proof. The original uncommitted S8 graph and its new context/status stay locally
pending the already-approved S8 round; no incomplete S8 graph is staged here.
Historical S8 amendment facts in S9 proof do not grant S8 readiness or completion.
This is a narrower use of the permitted S9 Git lease, not omission of source work.

## Resume Context

```json
{
  "change_id": "support-stage-specific-resume-review",
  "record_kind": "local",
  "mode": "self-evolution",
  "approval_status": "approved",
  "risk_profile": "strict",
  "control_plane_owner": {
    "agent_product": "codex",
    "agent_instance_id": "s8-control-01",
    "agent_role": "control-plane",
    "capability_profile": "control-plane-high"
  },
  "allowed_actions": {
    "wait": "none",
    "implement": "local-edit",
    "verify": "local-read",
    "review": "local-read",
    "sync": "local-runtime-sync",
    "amend-review-binding": "local-edit",
    "commit-push": "source-git-lease"
  },
  "verification_commands": [
    "PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 /Users/elvis/.codex-account-a/skills/.system/skill-creator/scripts/quick_validate.py .",
    "PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_core_gates.py .",
    "PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 scripts/validate_core_gates.py .",
    "PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v",
    "PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 -m unittest discover -s tests -v"
  ],
  "reviewer_assignment": {
    "review_purpose": {
      "object": "S9 stage-specific resume implementation and separate final gates",
      "decision": "decide pass, fail or blocked at the independently reviewed implementation or final gate"
    },
    "agent_product": "codex",
    "agent_instance_id": "s9-review-01",
    "agent_role": "independent-reviewer",
    "capability_profile": "control-plane-high",
    "independence_requirement": {
      "kind": "distinct-contract-instance",
      "distinct_from": [
        "control_plane_owner",
        "executor_assignment"
      ]
    },
    "result_authority": "governed-review-evidence"
  }
}
```

## Resume Amendment Authorization

```json
{
  "amendment_kind": "strict-local-reviewer-binding",
  "change_id": "add-project-document-ownership",
  "previous_contract": {
    "path": "openspec/changes/add-project-document-ownership/approval.md",
    "sha256": "233d318470241a5eb22eea9186bb372d72db6b65bf9556f6ffa818318e924873"
  },
  "next_contract_path": "openspec/changes/add-project-document-ownership/resume-contract-v2.md",
  "reviewer_assignment": {
    "implementation-review": {
      "review_purpose": {
        "object": "S8 scoped implementation and its bound evidence",
        "decision": "decide pass, fail or blocked for the independent implementation gate"
      },
      "agent_product": "codex",
      "agent_instance_id": "s8-review-01",
      "agent_role": "independent-reviewer",
      "capability_profile": "control-plane-high",
      "independence_requirement": {
        "kind": "distinct-contract-instance",
        "distinct_from": [
          "control_plane_owner",
          "executor_assignment"
        ]
      },
      "result_authority": "governed-review-evidence"
    },
    "final-review": {
      "review_purpose": {
        "object": "S8 final verification and closure",
        "decision": "decide pass, fail or blocked for the independent final gate"
      },
      "agent_product": "codex",
      "agent_instance_id": "s8-final-01",
      "agent_role": "independent-reviewer",
      "capability_profile": "control-plane-high",
      "independence_requirement": {
        "kind": "distinct-contract-instance",
        "distinct_from": [
          "control_plane_owner",
          "executor_assignment",
          "implementation_reviewer"
        ]
      },
      "result_authority": "governed-review-evidence"
    }
  }
}
```
