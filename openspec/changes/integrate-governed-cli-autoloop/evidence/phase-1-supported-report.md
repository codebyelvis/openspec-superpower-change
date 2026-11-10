# Phase 1 supported-subset acceptance

当前：运行证据已完成，独立 Pi 审查实例（`01a1afbe-e61b-768b-896d-8a743ed83565`）已完成阶段 1 支持子集最终验收审查并给出 `REVIEW: PASS`（0 阻塞发现，见 `evidence/phase-1-supported-review.md` 与 `evidence/pi-phase-1-supported-review-receipt.json`）；阶段 1（Codex + Pi 支持子集）收口通过（`PASS_SUPPORTED_SUBSET`），AGY 保持受限直调/手动回退，后台治理入口仍未启用。

用户2026-11-09授权路径A，选取Codex+Pi自动入口支持子集，AGY仅受限直调/手动回退。旧报告/Review保持历史，Pi对continuation的真实PASS及修改前11/11哈希已保存，不外推到新版AGY。

本轮8次真实CLI探针：Codex0.167.0-alpha.3.2（App绝对路径）和Pi1.5.0各R1/R2/写边界/宿主deadline。R1/R2共4/4正常完成，native ID、随机nonce、规范化cwd与原生会话文件匹配。每次续接检查前轮终态/退出/进程组及精确文件；无最近会话或自动新建恢复。

权限2/2：Codex实际tool call/output关联，单次本地写被系统拒绝(exit1, operation not permitted)，原生记录read-only/never；Pi实际工具集只有read/grep/find/ls，无MCP或扩展写工具。所有fixture前后SHA一致。仅声明本次明确账户/fixture/flags的受限入口证据，不声称任意账号/插件设置全局只读。Codex模型目录刷新出现非致命超时日志，但本轮业务turn均正常完成；保留stderr，不把它当业务失败重跑。

宿主截止2/2：新鲜CLI进程在1秒host deadline终止，两个进程组均结束，没有续接或接受部分输出。这不是CLI内部或后端取消证明，也不能满足阶段2的worker/unknown/retry门槛。

续接守卫反例5/5：空身份、身份不符、前轮unknown、原生文件缺失、cwd不符，均在模型启动前拒绝。负面夹具在Pi分支运行，共用宿主入口；未编辑真实session文件，原Pi输出保持同哈希。不存在跨产品完整笛卡尔故障矩阵或通用监管实现。

原始命令/输出/退出/身份/哈希：closure-20261109原始证据与phase-1-supported-facts/manifest。独立Pi审查实例（`01a1afbe-e61b-768b-896d-8a743ed83565`，独立于原主控Codex `01a1aa6c-c4c8-7111-812f-02e1396290e7` 与收口执行者Pi `01a1bec5-45cb-76cc-9766-4c191329bdec`，且不宣称与前次210s超时会话 `20804c85-aefd-4743-9848-b2f17d9f61cf` 为 `same_reviewer_instance`）独立复核61/61 manifest文件哈希、3/3合同哈希、8/8源文件及24/24关键事件行哈希、以及3项内存逆向调用拦截全部通过（`REVIEW: PASS`，原始事件行148 `event_id=3d0c120b` SHA-256 `6a8e66d3d9e7359fbb16fedbf2451be963455daa2b1475b3730a6a4dbc56222e`）。宿主临时脚本未安装；两个SKILL、全局规则、引擎、插件、rules、业务代码与Git均未改。OpenSpec strict是本次制品检查，没有治理运行源码修改，不以未运行完整unittest宣称通过。后台授权/身份/重试/schema-6/schema-2/control-plane/完成门禁原样保持。
