# Independent Project Learning Review R2

通过。Fresh independent Project Learning Review R2 未发现阻塞或非阻塞 finding。

Review assignment：purpose=验证 prior learning finding 已修复；product=`codex`；role=`independent-reviewer`；capability=`control-plane-high`；independence=`fresh instance`；authority=`evidence-only`。

核查结果：

- Generalization：`docs/engineering-invariants.md` 已将问题概括为“哈希校验和解析必须绑定同一组精确字节”，覆盖 pathname replacement、目录/叶节点 symlink 和 reviewer identity reuse。
- Deterministic sensitivity：probe 在首次 parent leaf `os.open` 返回绑定 FD 后立即以 forged reviewer 内容替换 pathname；eligibility 仍取原 FD 的已哈希字节并返回 `True`。
- Open count：明确断言 `parent_leaf_opens == 1`。旧式“先哈希、再按路径解析”会返回 forged 内容或产生额外打开，因此无法通过。
- Fixture restoration：probe 随后将原始 parent JSON 写回 `review`，临时目录退出时统一清理。
- Discovery：`AGENTS.md` 在 correction/Review history 的 completion 路径显式要求读取 `docs/engineering-invariants.md`。
- Runtime trigger：规范由 `references/approved-implementation-workflow.md` 的 `FOCUSED_RECHECK` eligibility 路径触发；测试覆盖 parent hash、reviewer replacement/reuse、leaf/intermediate symlink 和路径漂移。
- 静态 invariant 测试通过；`git diff --check` 通过。动态 focused probe 因当前只读沙箱没有可写临时目录而未能执行，错误发生在 `TemporaryDirectory` 创建阶段，不是测试断言失败。

LEARNING_REVIEW: PASS
