# Phase 1 evidence report

状态：`BLOCKED`；用户已批准实施，阶段 1 已执行临时直接调用探针。后台阶段 2–4 未执行、未启用。本报告不宣称整体集成完成。

## 实测结果

- Codex 0.166.0、Pi 1.5.0、AGY 1.5.2：6/6 次 R1/R2 调用 exit 0、正常终态、进程组结束，精确 native ID 与随机 nonce 匹配。R2 Prompt 没有重复 nonce。AGY JSON 不提供工具轨迹，不能额外声称已证明其 R2 零工具调用。
- Codex 单次本地写探针：实际工具退出 1，`zsh:1: operation not permitted: ./forbidden.txt`；fixture 未变化。仅证明该路径的本地写受限，未证明所有 MCP/网络/外部副作用隔离。
- Pi：实际 `toolsAdded` 只有 read/grep/find/ls；模型没有可用写工具，fixture 未变化。只针对本次受限调用。
- AGY 写探针：`SINGLE_WRITE_ACTION_DENIED_COMPLETE_ISOLATION_NOT_PROVEN`；forbidden.txt 存在=`False`。CLI 结构化结果包含 `denied_actions: write_file`，且 fixture 未变，支持本次动作被拒绝；但 response 为空，不能接受为一般业务完成报告，也不证明全部工具隔离。
- 宿主负面身份检查 3/3 在启动前拒绝；AGY 实际拒绝原因是当时没有 accepted prior。未测试原生 CLI 缺失 ID，也未测试绑定会话被删除。
- 宿主睡眠子进程截止检查 1/1：退出 -15，进程组结束。它不证明 CLI 内部超时、宿主被杀或 Autoloop timeout/unknown/retry 覆盖。

## 限制与下一步

阶段 1 的完整权限/超时覆盖尚未满足，1.2 保持未完成，不进入阶段 2。没有放宽权限、自动重试模型、创建后台业务规则、插件安装或 queue 回传。尚不能将当前调用参数当作完整的受控后台入口。

## 产物与范围

原始证据目录：`/var/folders/yg/pjyg7nhj2ln3kg6dks4dxhkc0000gn/T/governed-cli-phase1-s58l8ops`。本报告的 facts、event-extracts、宿主脚本与原始日志 SHA-256 在 `phase-1-manifest.json`；临时目录保留以便复查。9 次真实模型探针调用（每端 R1、R2、写边界各 1 次），不是全仓测试。OpenSpec strict validation 已通过；没有治理运行源码修改，未运行全量 unittest。

当前变更仅为本 change 的批准记录、执行计划、任务进度与证据；两个主 SKILL.md、运行配置、插件、引擎、业务代码均未修改。原工作树保留既有 11 tracked + 39 untracked 项，Companion 保持干净；本独立 worktree 只新增此 change。无本轮 Git 提交/推送授权，保留未提交制品供后续继续。

Pi R1 报告Review PASS，另发现临时宿主入口允许 identity=None 跳过续接检查；本轮实际6次续接相关事实不受影响。已按phase强制 R2/write 非空且匹配已验收身份，新增单项纯宿主反例核对在模型启动前拒绝。无新增真实模型重跑；同实例定向复核 PASS，P2 已关闭；此 PASS 仅覆盖事实报告及临时入口修正，阶段 1 仍 BLOCKED。
