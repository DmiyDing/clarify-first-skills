# Clarify First: 先澄清，再执行

[![License](https://img.shields.io/github/license/DmiyDing/clarify-first)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/DmiyDing/clarify-first/pulls)
[![Spec](https://img.shields.io/badge/Spec-Agent--Skills-blueviolet)](https://agentskills.io/specification)
[![Cursor Compatible](https://img.shields.io/badge/Cursor-Compatible-blue)](https://cursor.com)

**拒绝盲目猜测。让 AI 在触碰你的代码前，先学会提问。**

Clarify First 核心目标只有一个：**澄清 (Clarification)**。它强制 AI Agent 在需求模糊、存在冲突或涉及高风险时停下来。它将 AI 从一个鲁莽的执行者，转变为一个在行动前先对齐目标、明确范围的“深度思考合伙人”。

[English](./README.md) · **协议：** [Apache-2.0](./LICENSE)

---

## 核心痛点：盲目执行 (Guess-and-Run)
大多数 AI 编程助手都“太想帮忙了”。当你给出一个模糊指令（如“优化这段代码”）时，它们会立即开始重构，而完全不知道你真正关心的是运行速度、包体积，还是代码的可读性。

**Clarify First 彻底改变这种模式：先澄清，后代码。**

## 核心价值
*   ❓ **主动澄清**：只要目标有 1% 的不确定，AI 必须开口询问缺失的上下文。
*   🤝 **方案对齐**：主动提供选项（A/B/C），确保你们在同一个频道上。
*   🛑 **安全关卡**：在执行破坏性或高影响命令前，必须获得你的明确授权。

## 效果对比：提问的力量

| 盲目执行（标准模式） | 深度澄清（启用本技能） |
|----------------------|--------------------|
| 你：「优化一下应用。」 | 你：「优化一下应用。」 |
| Agent 直接开始大规模重构代码。 | Agent：**「风险：中。我需要先澄清：我们是优化运行速度、内存占用，还是代码可读性？」** |
| 结果：代码坏了，优化的不是地方。 | 结果：AI 做了你真正需要的事情。 |

## 安装

**支持 Agent Skills 的 Cursor、Claude Code 等：**

```bash
npx -y skills add DmiyDing/clarify-first
```

安装后重启客户端。若未自动触发，可在对话中说：「使用 clarify-first 技能」。

**Codex（AGENTS.md）：** 若希望在某仓库或全局固定该行为，可将 [下方片段](#codex-agentsmd-片段) 写入 `AGENTS.override.md` 或 `AGENTS.md`。

## 使用方式

安装后，当 agent 识别到模糊或高风险请求时会自动启用。也可显式调用：

- 「使用 clarify-first 技能。有模糊或高风险的地方先问我确认，不要猜。」

Agent 会先对齐范围、提出 1–5 个关键问题（尽量给选项），并在你确认后再改代码或执行命令。

## 工作原理

- **低风险**（只读、小范围可逆改动）：agent 可在声明假设后继续，一旦出现新歧义会停下追问。
- **中风险**（重构、改接口等）：agent 先只读检查，给出 2–3 个选项、问清阻塞问题，确认后再做较大改动。
- **高风险**（删除、部署、改密钥等）：agent 会要求你显式确认（如「可以，执行」）后再执行。

详细流程见技能本体：`clarify-first/SKILL.md`。

## 兼容性

- **Agent Skills**：本仓库遵循 [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) 约定（Anthropic）。技能核心位于 `clarify-first/` 目录下的 `clarify-first/SKILL.md`。
- **客户端**：Cursor、Claude Code、Codex 以及任何支持从 GitHub 或本地路径加载 Agent Skills 的客户端。

### Codex AGENTS.md 片段

在 Codex 中，将以下内容写入 `AGENTS.override.md` 或 `AGENTS.md`（仓库内或 `~/.codex/`）：

```markdown
# Clarify First (risk-based)

When a request is ambiguous, underspecified, conflicting, or high-impact, do not guess.

Risk triage:
- Low: proceed with explicit assumptions and minimal reversible steps; stop if new ambiguity appears.
- Medium: inspect read-only first; propose 2–3 options; ask only blocking questions; wait for confirmation before larger edits or running commands.
- High: require explicit confirmation ("Yes, proceed") before any irreversible action (side-effect commands, deletion/overwrite, migrations, deploy/publish, secrets/config changes, spending money, contacting people).

If you see a better approach than requested, present it as an option and ask the user to choose.
```

## 仓库结构

```
.
├── clarify-first/
│   ├── SKILL.md          # 技能定义（Markdown）
│   └── references/       # 按需加载的上下文文件
├── tooling/              # 维护脚本
├── .cursorrules          # Cursor 规则模板（精简版）
├── CHANGELOG.md          # 版本历史
└── CONTRIBUTING.md       # 贡献指南
```

技能采用渐进式披露：agent 在触发时加载 `clarify-first/SKILL.md`，仅在需要时打开 `references/*`。

## 参与与协议

欢迎贡献。本项目采用 [Apache-2.0](./LICENSE) 许可。
