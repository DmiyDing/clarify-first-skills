# Clarify First (先澄清，再执行)

[![License](https://img.shields.io/github/license/DmiyDing/clarify-first)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/DmiyDing/clarify-first/pulls)
[![Smithery](https://img.shields.io/badge/Smithery-Available-orange)](https://smithery.ai/skills/DmiyDing/clarify-first)
[![Cursor Compatible](https://img.shields.io/badge/Cursor-Compatible-blue)](https://cursor.com)

**拒绝盲目猜测，让 AI 成为你的技术合伙人。**

Clarify First 是一个防御性的 [Agent Skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)，它引入了一套 **风险分类协议 (Risk Triage)**。它让 Claude、Cursor 等 Agent 在面对模糊、冲突或高风险请求时，先停下来与你对齐目标和方案，避免在执行错误后再去返工。

[English](./README.md) · **协议：** [Apache-2.0](./LICENSE)

---

## 为什么需要

AI 编程助手在需求不清时常常 **“猜着做”**，结果就是改错、返工和信任损耗。

Clarify First 增加了一个战略性关卡：
*   🛑 **防止“盲目执行”**：不再需要撤回大规模的错误修改。
*   🛡️ **安全护栏**：防止误删生产数据或误触发部署流程。
*   🤝 **深度对齐**：强制 Agent 像资深工程师一样总结假设并提供多套方案（A/B/C）供你选择。

## 效果对比

| 未使用 Clarify First | 使用 Clarify First |
|----------------------|--------------------|
| 你：「把应用优化一下然后上线。」 | 你：「把应用优化一下然后上线。」 |
| Agent 直接开始改代码、重构。 | Agent 先暂停，问：范围（小优化还是大重构？）、「上线」的定义、你倾向的选项。 |
| 你：「其实我只想修一个慢查询……」 | 你：「小优化；上线=部署到 staging 且检查单全绿。」 |
| 返工、心累。 | Agent 在明确范围内执行，无返工。 |

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

详细流程见技能本体：`skill.md`。

## 兼容性

- **Agent Skills**：本仓库遵循 [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) 约定（Anthropic）。技能核心位于根目录的 `skill.md`。
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
├── skill.md           # 技能定义、工作流、反模式
└── references/
    ├── zh-CN.md       # 中文措辞参考
    ├── EXAMPLES.md    # 示例输入与预期行为
    ├── QUESTION_BANK.md
    ├── SCENARIOS.md   # Bug 报告、设计/RFC、需求范围等场景
    └── NFR.md         # 非功能性需求澄清清单
```

技能采用渐进式披露：agent 在触发时加载 `skill.md`，仅在需要时打开 `references/*`。

## 参与与协议

欢迎贡献。本项目采用 [Apache-2.0](./LICENSE) 许可。
