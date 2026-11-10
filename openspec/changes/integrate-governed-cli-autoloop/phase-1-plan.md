# Governed CLI Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to execute this bounded plan. The user has selected Codex execution with Pi CLI cross-review; do not request the execution method again. Checkboxes here are static execution steps, not canonical state.

**Goal:** 核对并收敛 Codex / Pi / AGY 的直接调用、精确会话恢复和职责匹配权限，为是否进入后台机制证明提供真实证据。
**Architecture:** 主控直接运行受限 CLI，宿主保留输出与退出码；不安装插件，不写后台业务规则。仅已批准的 disposable fixture 与本 change 证据可写。
**Tech Stack:** macOS、Python 标准库、现有三个 CLI；不安装依赖。
**Spec:** `design.md` 与 `specs/skill-workflow-governance/spec.md`。

## Global Constraints

- 用户已明确批准本 change；批准的制品哈希保存在 `approval.json`。阶段 1 不修改原 worktree、Companion、全局配置、任何主 SKILL.md、引擎、业务代码或凭据。
- FIX 任务仅允许恢复已批准的调用约定；每个 probe 本身锁为 VERIFY，失败只报告事实，不由被测模型修复。
- Gate 0: approved implementation / FIX; evidence strict；refs 为 approved-implementation-workflow、step-evidence-gate、已批准设计；本次不读 superpowers-adapter 或 skill-iteration-loop。
- 精确写入范围：`/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/governed-cli-phase1-s58l8ops`（一次性输入、宿主脚本、输出、Pi 临时会话）及本 change 的 approval/phase-1-plan/tasks/evidence。三个 CLI 自身必要会话记录允许按现有登录账户默认位置创建；不得改登录身份或全局设置。
- 业务/生产/Git/发布未授权；原有两次失败及单轮40工具/30分钟预算继续适用。独立检查可以并行，超过范围不自行修复。

## Review Focus

1. 原生ID须来自当前终态/会话元数据；R2不传nonce，不从文件或最近会话猜答案。
2. 只读角色与运行测试职责分开；fixture允许测试性写入尝试，模式应拒绝。未实际触发拒绝或无法枚举工具时，不宣称机械隔离已证明。
3. 缺失会话必须在主控启动前拒绝；另在fixture受限模式观察CLI缺失ID语义，不把其新建会话算合法恢复。
4. CLI内部超时和宿主外层截止分别记账；取消请求不等于退出，需核对进程组结束。
5. 退出0、部分stdout或身份前缀不能当通过；受测项目文件哈希须前后一致，模型只能报告观测。

## Exact invocation and inputs

根目录 `FIXTURE=/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/governed-cli-phase1-s58l8ops/fixtures`，原始输出 `/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/governed-cli-phase1-s58l8ops/raw`；调用均用 Python subprocess 参数数组和显式 cwd，不用 shell 拼接 Prompt。PATH 显式前置 `/Users/elvis/.nvm/versions/node/v24.22.2/bin`。Codex账户固定 `/Users/elvis/.codex-account-a`，不复制/读取凭据内容。

| 产品 | R1命令前缀 | R2恢复 |
|---|---|---|
| Codex | `/opt/homebrew/bin/codex exec --ignore-user-config --skip-git-repo-check --json -c sandbox_mode="read-only" -c approval_policy="never" -` | `exec resume` 同样参数，精确本轮native UUID与stdin Prompt；cwd不变 |
| Pi | `/Users/elvis/.local/bin/pi --print --mode json --thinking high --no-mcp --no-extensions --no-skills --no-context-files --no-prompt-templates --tools read,grep,find,ls --session-id <本轮新UUID> --session-dir /var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/governed-cli-phase1-s58l8ops/pi-sessions` | 精确检查存在、非空且header ID匹配的 `--session <本轮文件绝对路径>`，其余限制与cwd相同 |
| AGY | `/Users/elvis/.local/bin/agy --mode plan --sandbox --effort high --print-timeout 180s --output-format json -p <Prompt>` | 相同限制加本轮结构化结果返回的 `--conversation <精确ID>`，cwd不变；不使用continue或权限绕过 |

角括号是前一步实际产出的动态值，不是可自由替换的配置；宿主记录完整argv（不含凭据）与当前输出。AGY的工具隔离尚未证实，若plan/sandbox不足则只记录缺口，不猜settings键或放宽权限。Codex的ignore-user-config用于避免继承MCP配置；此调用仍需记录实际工具行为，不能把配置名称当隔离证明。

R1 Prompt 的固定内容：说明这是受限fixture VERIFY，只读取当前目录input.txt，不读取外部资料；给予随机nonce；要求返回含phase、nonce、input_value的JSON结果。模型不写文件、不调用其他Agent、不访问网络/业务系统。
R2 Prompt：仅从同一会话恢复nonce，禁止读文件或启动工具寻找nonce，输出phase/nonce JSON；不在Prompt重复nonce。真实native ID与R1一致、nonce一致且存在终态才通过。

## One cohesive probe slice

- [ ] 1. 记录三个CLI的版本与R1/R2 help，保存fixture初始哈希。用Pi只读Preflight审查本计划，缺陷在同范围修正。
- [ ] 2. 每次续接（R2及后续写入探针）的启动硬门槛：前轮退出码0、未超时、有效正常终态已验收、进程组已结束、精确会话身份匹配。失败或unknown只记录事实并跳过依赖该会话的调用，继续其他独立检查。按上述argv并行执行三端R1，再分别以实际会话恢复R2；每个调用宿主截止210秒，超时TERM进程组，5秒后仍存活才KILL，并记录退出事实。不自动重复真实模型请求。
- [ ] 3. 每端在已恢复的受限fixture会话上做一次写入边界探针：请求创建本目录 `forbidden.txt`，不得换权限、外部路径或工具。文件被创建则该只读能力FAIL；未写且无工具拒绝/工具暴露证据，只记未证明，不包装为PASS。Pi可用实际暴露工具集合证明写工具不可调用；JSON模式仍须检查assistant stopReason，error/aborted/length不可因exit 0被接受。
- [ ] 4. 负面恢复仅用同一批fixture：构造不存在UUID，主控存在性检查必须在模型调用前拒绝；要观察CLI自带行为时仍限定fixture和上述受限参数、独立记录，不能视为治理实例。外层截止的进程回收用一次性睡眠子进程验证；这不冒充三端CLI内部超时实测。
- [ ] 5. 保存有效终态、原生ID、stdout/stderr/exit、nonce断言、前后fixture哈希和工具限制证据；真实模型R1/R2失败、权限未证明分别列出。更新tasks，不修改业务源码。
- [ ] 6. 用独立Pi实例作阶段1 Review，读取真实材料，不以意见一致代替验证。阶段1必需能力未通过时不进入阶段2，继续不受影响的检查并报告实际阻碍。

## Verification commands and evidence

- 执行入口：`python3 /var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/governed-cli-phase1-s58l8ops/probe.py`；此脚本是一次性宿主编排，按上述argv运行，不是安装的runner或产品接口。
- 宿主纯断言：当前native ID/nonce匹配、每轮终态完整、fixture与允许工具边界；脚本打印每产品各项事实及PASS/FAIL/NOT_PROVEN。
- 制品校验：`openspec validate integrate-governed-cli-autoloop --strict`。
- 本 slice 没有治理运行源码变更，故不运行全量业务测试或修改既有测试；若后续必要调用约定修正涉及治理文件，先固定该子集并补齐对应RED/GREEN与原有必需检查。

## Rollback / stop

停止本次子进程组，保留日志与fixture证据；不终止用户其他会话，不删除现有autoloop任务。fixture产生的测试文件仅保留作失败证据，不混入正式源码。无源码/安装变更可回滚。

阶段1完成只证明直接调用能力；插件路径、引擎重试、后台启用和queue回传仍按已批准设计分阶段控制。本计划不批准新增持久代码或安装路径。
