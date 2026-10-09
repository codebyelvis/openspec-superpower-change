# S8 Major 前置冲突记录

作者：elvis。change-id：`add-project-document-ownership`，draft-v1。
结果：**BLOCKED，未进入实现**。具体 S8 批准仍保留，前置治理修复未批准。

## 已完成与停止原因

已核对四份待审合同 SHA-256、记录用户具体已批准口令，创建新源/运行时
结构化备份和执行 Plan，取得独立 FULL_PREFLIGHT。提案阶段漏查的 S7
兼容限制现在已由独立 Review 与控制面分别复现；不能通过普通措辞修订解决。

`references/approved-implementation-workflow.md` 要求未完成的受治理实施
停手前持久化 canonical Session Resume。当前 `_resume_review` 将
implementation-review 与 final-review 都与一个不可变 context assignment
逐项比较。S8 已批准的 Review 明确要求 `s8-final-01` 与 `s8-review-01`
不同。当前恢复/完成机制无法同时表示两者。

控制面以既有 fixture 和实际临时文件测试完整状态转换，得到：

- 正常绑定 `s8-review-01` 的 implementation-review 可进入最终验证阶段。
- 使用 `s8-final-01` 的 final-review 被拒：identity/independent assignment mismatch。
- 同一实例承担 final 的控制例被现有验证器接受，但不满足 S8 合同。
- 用新 context 替换已有绑定被拒：readonly kind/context cannot change in place。

独立 `/root/s8_preflight` 使用另一组实际普通文件测试双阶段绑定矩阵，
同样确认两种单 assignment 各能匹配自身阶段、不能匹配另一个实际实例。
这两项只是合成隔离诊断，不是 S8 实施、行为 GREEN 或生产签发证据。

## 工件与判断

- 独立 Review：`docs/review/2026-10-08-S8-preflight-full.json`，BLOCKED，
  原 Plan SHA `d07e7388097c83dbc833278df6972ecffe70a624dacdcf6f15b5937a72904a10`。
- 控制面复现：`docs/review/2026-10-08-S8-major-prerequisite-conflict.json`。
- 现有 validator SHA：`8c0844c1ede850109965ead76831b5bceaea434482342739f53a4186198d7959`，未改。
- F2/F3 普通 Plan 缺项已补明负例与执行命令；未重开 FULL 或把作者检查
  记成独立 PASS。F1 未解决，Plan 仍不可执行。
- S9 仅按两个独立信号的窄管道收为 Major／待提案，暂不实现；因与现有
  规则冲突而 blocked。S8 scope、risk、assignment 和五项验收不变。

原 SKILL 明确要求 “Stop for scope/protected-boundary changes”，
Self-Evolution 将证据/完成规则列为 Major，且 S8 具体 scope 排除了 S7
规则修改。因此没有跳过 checkpoint、复用同一实例、替换 context、改 schema
或伪造/重标审查证据；这些都不能由当前 S8 批准自动授权。

## 当前状态、验证和清理

canonical：`docs/agent-collab/add-project-document-ownership/status.md`。
记录 approved/strict/blocked、非空 blocker/owner/resume_condition，以及
唯一 `wait` 动作；verified_revision 为 null，不宣称 S8 已通过验证或完成。
CURRENT/BACKLOG 保留相同阻塞。实际源/状态检查结果另见最终核对记录。

独立 readiness 已跑 quick、新 change strict、core 双解析和相关回归各
17 项，均通过；独立 native 单次机械写入只证明 CLI/工具审计可行，不作为
S8 三场景验收。未执行 S8 RED/GREEN、全套实施后回归、runtime sync、
archive、Git add/commit/push。44 个无关文件和 S1–S7 既有条目保持。

本轮新源/运行时备份与此前 proposal 备份保留，均位于发现目录外。
独立 Preflight 的两个自有临时目录已删除并核对不存在；原生 raw trace、
result、stderr 均未进入仓库。没有本线程的 S8 原生行为 trace。

唯一后续动作是等待用户明确选片/裁决独立前置提案；此前不改实施规则。
以后先处理具体受保护 scope 批准及前置兼容证据，再沿 S8 已批准范围恢复。
不把 BLOCKED 当 done，不自动开启候选或放宽原合同。

## 最终实际核对

- quick、新 change strict、core 双解析再次退出 0。
- `--resume-status docs/agent-collab/add-project-document-ownership/status.md
  --artifact-root .` 在两个解析器均退出 0；实际结果仍为 blocked，
  verified_revision=null、authority_granted=false，不是执行/完成 PASS。
- 14 个 S8 专属源工件/状态文件以外没有本轮改动；44 个无关文件及
  S1–S7 七行 backlog 未变；2 个批准任务完成，9 个实施/闭环任务待处理。
- SKILL/学习规则/模板/validator/tests/CHANGELOG、S7/共享治理/manifest
  及相关四份运行时文件与起轮快照保持；没有实施或同步。
- HEAD 仍为 `379667f9780a3e718f41021f8a92a82618a286e2`，index 空，
  scoped diff --check 通过；未 add/commit/push。
- 独立 Review SHA：`f68f1bd8b3d344a3dce787ac5886ea9a0a609c0365d7337d4b6b10a9611af629`。
- 修正普通细节后的 Plan SHA：`d8baab34dedc8043c857df53e62387d6a0d8b6078a27a8ddfeb7c37e3f582df6`。
- 控制面诊断 SHA：`a89dcf440f17b620168aa6b92725c0f4ad4e003ed5ce22091a3b8edbd46bba50`。

最后三项用于定位实际待处理工件，不签发批准、独立 PASS 或新完成权。
