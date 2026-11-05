# Design: Narrow skill autoload

## Decisions

1. 区分自动加载条件和加载后的治理边界。Router description 采用显式触发白名单（含用户后续授权的明确 archive/distillation 请求）；普通文件或行为变更本身不再触发。已经进入门禁的任务仍保留全部批准、证据、完成和权限约束。
2. 诊断停顿按当前请求分支：同时点名缺陷并要求修复，且现有授权覆盖该修复时，诊断后继续一次单假设修复；只要求诊断或没有授权该修复时，报告并停。此分支不绕过任何现有停止条件或尚未满足的批准门槛。
3. 将 Companion 主入口中完整的 `Role-first Review assignment` 段（包括 `ROLE_FIRST_REVIEW_CLASSIFICATION` 和附属角色声明）移至现有 `references/handed-off-external-execution.md`，仅在选择 Handed-off External Execution 后读取。主入口保留该条件引用及完整 Handoff 治理入口。轻量审阅不加载或输出这段角色分配协议。

## Scope and compatibility

契约只有上述三项。Companion 没有独立 OpenSpec 目录，采用主仓库单一 delta，并在其中固定目标绝对路径。不得以本提案授权修改安装副本、全局规则、其他活动 change 或其他 CLI 副本。

现有 `Deterministic skill routing`、`Diagnosis checkpoint before a single-hypothesis fix` 和 `Evidence-gated Companion route isolation` 由本 delta 修改。其他条款保留；已经存在的 control-plane 所有权不因不自动加载 Router 而转移。

活动 change `add-role-first-review-routing` 的全 Review 角色分配要求与本提案的轻量分支范围存在重叠。`optimize-closed-loop-runtime-routing` 也涉及继续执行语义。它们不由本轮修改；实施前应核对当时的有效契约，防止旧文本重新引入被收窄的轻量要求。主入口中的无条件回跳措辞也只能按本提案显式触发范围对齐，不能扩大为治理改造。

## Validation and approval

本步只运行 `openspec validate narrow-skill-autoload --strict`，并核对仅新增四个提案文件、两边 `SKILL.md` 未变。文本场景用于定义后续验收，不代表已经验证运行时自动加载或 token 节省。

未来获批实施须核对显式/非显式触发、诊断/修复两种请求、原有停止条件、Standalone/Handoff 两条路径，并履行适用的现有验证要求。本轮不运行实施闭环，也不因 proposal 校验通过而推进实施。

## Approved implementation scope

用户已明确批准本 change，随后授权闭环处理本契约的校验对齐。实施范围为两个仓库的 `SKILL.md`、Companion 的 `references/handed-off-external-execution.md`、主仓库 `scripts/validate_core_gates.py`、双方 `tests/test_workflow_rules.py` 与 Companion `scripts/validate_templates.py`，以及角色分类前向测试调用方 `tests/run_role_first_review_forward_tests.py` 的来源路径。校验修改只覆盖新 description、迁移后的角色正文位置与 reference 完整性哈希。原 YAML 注释夹具、GOVERNED_CAVEMAN_LITE 义务、README、完成契约、schema-6、批准与证据门禁保持不变。

以上作为一个文本契约切片实施。现有定向测试先 RED 后 GREEN；运行双方 quick_validate、主仓库 validate_core_gates、Companion validate_templates、双方全量 unittest，以及本 change 的 OpenSpec strict 校验。Pi 只读审阅只提供证据，不能扩大授权或授予完成权。不安装、不跨端同步、不提交或推送。源码验证不代表当前安装副本或实际运行时加载已生效。
