# Phase 1 continuation — current runtime evidence

状态：`BLOCKED`。本轮新增1次AGY模型/CLI探针（没有重试或续接），没有启用后台；此前6次R1/R2结果未重跑。用户重贴的方案Review仍是advisory，不能覆盖当前运行证据。

## 当前实测

- AGY 1.5.2：`--mode plan --sandbox --print-timeout 5s --output-format stream-json`，新native session `a19743ad-d19a-42f3-869c-c9d512e2589d`。
- 宿主耗时 `13.542` 秒（包含启动耗时，不等于5秒计时器失效）；exit `3`，宿主45秒截止未触发，进程组已结束，fixture未变。
- CLI明确返回 `status: ERROR`、`finished_reason: print_timeout`，stderr含 `AGY_ERROR` / `DEADLINE_EXCEEDED` / `retryable:false`。这是预期超时反例证据，不是业务通过，也不证明后端任务已停止。
- 同一真实init事件公布 `60` 个工具，`permission_mode: request-review`。其中包括 `call_mcp_tool, run_command, write_to_file, replace_file_content, multi_replace_file_content, notebook_execution, send_message, schedule`。因此该参数组不满足本change“只读Review仅暴露读取能力”的验收条件；没有据此宣称这些工具实际越权成功。
- AGY公开help没有no-mcp/no-extensions/工具白名单开关；`--settings`虽为会话级，但没有已核实的权限键schema。本轮不猜键、不修改全局配置或放宽权限。

## 重贴Review的机制校正

1. 实际CLI为 `agent-autoloop stop <run-id>`，不是cancel；内部调用cancel只表示发出请求，仍需核实进程结束。来源：安装引擎 `cli/main.ts:676`、命令表745；获批design.md:67与spec delta:142已写对，无需重立项。
2. 短内层超时只能覆盖宿主仍存活且可终止、落盘、交付的路径。worker timeout仍返回failed，内核retryLater仍最多10次；封装被杀及unknown没有因此被证明安全。来源：`worker/worker.ts:329-341`、`kernel/decide.ts:43,318,435`。这项限制已在获批design.md:50及spec delta:80。
3. 旧Review“不读输出直返failed”的字面描述不符合当前安装版本：现在先调用read，再由timeout分支在业务回执解析前返回failed。后果仍是不能靠业务Prompt或read输出阻断外层重试。

## 版本来源与解释边界

本机 `agy changelog`：1.1.28曾将print-timeout改为成功退出；1.2.9记录daemon清理修复；1.4.11新增finished_reason；1.5.0改为timeout exit3。不得将旧条目当1.5.2当前事实。本轮实际exit3/print_timeout与较新条目一致。changelog不是全部后端停机的运行证据。

## 停止与后续条件

阶段1的AGY只读暴露契约未满足，因此不进入阶段2–4。按用户G2：“VERIFY过程中出现失败……严禁在同轮中做 profiling、改业务代码、新增测试或调用顾问。”本轮只完成其余独立核查并落盘事实；不修AGY、不再复调Pi。此前Pi PASS仅覆盖旧报告，不能扩展为本补充材料已独立Review。

恢复所需的具体材料：AGY当前版本可验证的会话级只读工具/MCP限制schema或受支持等价机制，以及对应实际工具清单。没有这些材料，不以单次write_file被拒代替整个工具边界；也不把新外层监督/引擎修改混入当前授权。

## 文件与现场

所有新写入仅在本change evidence/tasks与原已批准临时目录的 continuation-20261106；两个主SKILL、插件、规则、全局配置、引擎和业务源码均未改。原始stdout/stderr、精确命令、进程数据、前后仓库快照及SHA-256见同目录facts/manifest。三个仓库的探针前后完整Git文件哈希及status一致。原主仓库既有改动保留，Companion保持原现场；独立worktree的change制品保持未提交，无Git提交/推送授权。
