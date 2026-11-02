# Approval

Author: elvis

Status: user approved for implementation. Not final acceptance.

change-id: `add-verify-anti-drift-round-budget`

Verbatim user approval:

> 批准 change-id add-verify-anti-drift-round-budget。文件 A diff 逐字接受。文件 B 接受上一份 diff，并在 evidence. 后换行。两句澄清保留。G3 为 40 次、30 分钟、80%、新增测试 5。只改运行时 SKILL.md，开源仓根副本留在待同步清单。

Scope:

- File A append only: `~/.codex/AGENTS.md`
- File B only: runtime `~/.codex/skills/openspec-superpower-change/SKILL.md` (symlink from `~/.agents/skills/openspec-superpower-change`)
- File B line break after `evidence.`
- Both clarifying sentences retained
- G3: 40 tool calls, 30 minutes, 80 percent checkpoint, new-test limit 5
- Open-source root `SKILL.md` and other CLI copies stay on the pending-sync list
- No Git mutation and no cross-CLI sync
