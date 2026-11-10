# Phase 1 continuation: actual AGY deadline observation

Gate 0: approved implementation / FIX；本单项 probe 为 VERIFY，仅记录事实；evidence strict。沿用已读 Router、approved-implementation-workflow、已批准 design/spec 及 phase-1-plan。superpowers 方法复用现行 executing-plans；不重新开启已终结的 Preflight，不读 adapter/iteration-loop。用户现有批准覆盖阶段1真实CLI超时；不需要重复批准。

本项属于获批五组验收中的第3组，不添加业务模块/测试矩阵或产品接口。此前睡眠子进程的证据不替代它。唯一新模型调用使用新AGY fixture会话：
`/Users/elvis/.local/bin/agy --mode plan --sandbox --effort high --print-timeout 5s --output-format stream-json -p <fixed prompt>`
固定Prompt：`Isolated VERIFY timeout probe. Reply exactly TIMEOUT_PROBE_READY. Do not use any tool, read or write any file, invoke agents, access network or start background work. This is not an implementation task.`
进程 cwd 为本目录下 agy-timeout，PATH 前置既有 Node24。宿主上限45秒；届时 TERM 本次进程组，最多5秒后 KILL 尚存的本组进程；不触及其他CLI/服务。记录stdout/stderr/exit、实际耗时、进程组结束与fixture前后哈希。宿主不因exit0或JSON SUCCESS接受部分结果；超时warning、缺少有效终态分别报告，任何未知会话不续接/重试。无法证明后端停机时保留未知，不启动新的治理批次。

本次仅观察已安装行为，不修 AGY 或 Autoloop。命令/版本/公开help与本地内嵌文档作为来源；工具权限仍保留NOT_PROVEN。证据保存在此前批准临时目录的 continuation-20261106 与本change evidence/tasks，旧报告历史不改写。完成后对新事实证据用Pi独立只读Review；此Review不能授权后续阶段。运行 openspec validate integrate-governed-cli-autoloop --strict；保留全部现场，无Git/安装/同步操作。
