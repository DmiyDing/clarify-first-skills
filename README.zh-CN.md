# Clarify First Skills（先澄清再执行）

[English README](./README.md)

这是一个面向 AI / AI 编程工具的“风险分级澄清闸门”：当需求模糊、不完整或存在冲突时，AI 必须先**暂停执行**，梳理上下文、提出最少但关键的澄清问题，并在进行中/高风险操作前获得用户确认。

- Skill：`skills/clarify-first/SKILL.md`
- Skill 名称：`clarify-first`
- 协议：Apache-2.0

## 为什么需要它

很多 AI 助手会在信息不足时“猜着做”，带来返工、误解和信任成本。

这个技能的目标：
- 不确定性高：先对齐再行动
- 不确定性低：在明确假设下小步快跑
- 不可逆动作：必须先确认

## 它做什么（B：风险分级）

- **低风险**：允许继续，但必须声明假设、保持最小改动与可逆；出现新歧义立刻停下追问
- **中风险**：先只读检查，再给 2–3 个选项与权衡，问阻塞问题，确认后再做较大改动
- **高风险**：必须显式确认后才执行（跑有副作用命令、删除/覆盖、迁移、部署/发布、改配置/密钥、花钱、联系他人等）

## 安装

### 1）推荐：`skills` CLI（多客户端安装器）

如果你的工具支持 Agent Skills，这是最省心的方式：

```bash
npx -y skills add DmiyDing/clarify-first-skills --skill clarify-first
```

提示：
- `add-skill` 已更名为 `skills`（旧命令可能会提示 deprecated 并自动转发）。
- 安装后可能需要重启客户端。
- 自动触发不稳定时，建议在对话里显式说“使用 `clarify-first` skill”。

### 2）OpenAI Codex CLI

OpenAI Codex CLI 会可靠加载 `AGENTS.md / AGENTS.override.md`（仓库内或 `~/.codex/` 下的全局默认）。想“默认生效”，建议把规则放在：

- 仓库级：`<repo>/AGENTS.override.md`（优先）或 `<repo>/AGENTS.md`
- 全局级：`~/.codex/AGENTS.override.md`（优先）或 `~/.codex/AGENTS.md`

可直接粘贴的最小片段（英文优先，便于模型稳定执行）：

```markdown
# Clarify First (risk-based)

When a request is ambiguous, underspecified, conflicting, or high-impact, do not guess.

Risk triage:
- Low: proceed with explicit assumptions and minimal reversible steps; stop if new ambiguity appears.
- Medium: inspect read-only first; propose 2–3 options; ask only blocking questions; wait for confirmation before larger edits or running commands.
- High: require explicit confirmation ("Yes, proceed") before any irreversible action (side-effect commands, deletion/overwrite, migrations, deploy/publish, secrets/config changes, spending money, contacting people).

If you see a better approach than requested, present it as an option and ask the user to choose.
```

你告诉我你想全局生效还是某个仓库生效，我也可以帮你把措辞压到更短、更适合你日常工作流的版本。

## 使用方式

最可靠（显式调用）：
- “Use the `clarify-first` skill. If anything is ambiguous or high-impact, ask me the blocking questions first.”
- “使用 `clarify-first` 技能。中/高风险操作先问我确认，不要猜。”
