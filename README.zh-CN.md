# Clarify First: 先澄清，再执行

[![License](https://img.shields.io/github/license/DmiyDing/clarify-first)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/DmiyDing/clarify-first/pulls)
[![CI](https://github.com/DmiyDing/clarify-first/actions/workflows/validate-skill.yml/badge.svg)](https://github.com/DmiyDing/clarify-first/actions/workflows/validate-skill.yml)
[![Spec](https://img.shields.io/badge/Spec-Agent--Skills-blueviolet)](https://agentskills.io/specification)
[![Cursor Compatible](https://img.shields.io/badge/Cursor-Compatible-blue)](https://cursor.com)

**拒绝盲目猜测。Clarify First 是一个确定性状态机与安全中间层，让 Agent 在模糊或高风险任务上先问清再执行。**

Clarify First 的核心是：**先对齐，再落地**。它阻断静默假设，要求显式确认，并让“计划 vs 实际执行”可对账。

[English](./README.md) · **协议：** [Apache-2.0](./LICENSE)

---

## 为什么需要它
大多数 Agent 默认追求“马上做”，而不是“先确认”。在模糊或高影响场景下，这会把隐藏假设直接变成代价。

**Clarify First 彻底改变这种模式：先澄清，后代码。**

## 它真正带来的价值

启用 Clarify First 后，Agent 更有可能做到：

1. 遇到“优化一下”“修一下”“改好它”这类模糊请求时先停下来确认，而不是直接猜。
2. 只问真正阻塞下一步的问题，而不是丢一大段协议术语。
3. 在删除、部署、迁移、覆盖等高风险动作前要求显式确认。
4. 在中高风险任务上先给计划，再执行，过程可对账。
5. 根据用户语言输出更易读的确认内容，中文用中文标题，英文用英文标题。

## 无防护 vs 启用后

| 无 Clarify First | 启用 Clarify First |
|------------------|--------------------|
| 用户：「删掉旧文件。」 | 用户：「删掉旧文件。」 |
| Agent 可能按猜测直接执行破坏性命令。 | Agent 输出风险头，先确认范围与回滚，再等待明确确认。 |
| 结果：范围错误、恢复困难。 | 结果：意图一致、可控可回滚。 |

## 核心能力

| 能力 | 支持 |
|------|------|
| 不可绕过的澄清门禁 | ✅ |
| 假设加权风险分级 | ✅ |
| 两阶段执行（计划 -> 确认 -> 执行） | ✅ |
| 严格执行边界与计划修订 | ✅ |
| 高风险渐进式执行 | ✅ |
| Plan-ID 锚定与长会话检查点 | ✅ |
| 敏感信息脱敏 | ✅ |
| 架构反模式硬中断 | ✅ |
| 文件核心度动态风险修正 | ✅ |
| 执行后最终对账 | ✅ |
| 多智能体交接载荷（细粒度） | ✅ |
| 对抗场景测试覆盖 | ✅ |
| 官方风格 eval 资产（`evals/evals.json`） | ✅ |
| 官方风格触发基准封装 | ✅ |

## 快速开始

### 1) Cursor / Windsurf 类客户端
- 复制 [`/.cursorrules`](./.cursorrules) 到项目根目录（或并入现有规则）。

### 2) 支持 Agent Skills 的客户端
- 通过命令安装：

```bash
npx -y skills add DmiyDing/clarify-first
```

安装后重启客户端。若未自动触发，可显式说：「使用 clarify-first 技能」。

### 3) Codex / AGENTS.md 环境
- 若希望在仓库或全局固定行为，可将 [下方片段](#codex-agentsmd-片段) 写入 `AGENTS.override.md` 或 `AGENTS.md`。

### 4) 框架编排（LangChain / Dify / 自研 Agent Runtime）
- 将 [`clarify-first/SKILL.md`](./clarify-first/SKILL.md) 作为系统策略注入。
- `references/*` 作为按需加载上下文，而不是常驻大 Prompt。

## 实际体验会是什么样

安装后，当 agent 识别到模糊或高风险请求时会自动启用。也可显式调用：

- 「使用 clarify-first 技能。有模糊或高风险的地方先问我确认，不要猜。」

Agent 会先对齐范围、提出 1–5 个关键问题（尽量给选项），并在你确认后再改代码或执行命令。

默认确认结构通常是：
1. 风险头
2. 我已确认
3. 还需确认
4. 可选方案
5. 下一步

## 校验

可使用以下脚本检查版本与引用一致性：
- [`tooling/verify-version.js`](./tooling/verify-version.js)

也可以使用以下命令检查 skill 结构与触发表现：
- `skills-ref validate ./clarify-first`
- `npm run validate:skill`
- `npm run benchmark:trigger`

`npm` 命令会自动发现本机 Anthropic `skill-creator` 安装位置，查找顺序为：
- `SKILL_CREATOR_ROOT`
- `SKILL_CREATOR_SCRIPTS`
- `~/.claude/skills/skill-creator`
- `~/.codex/skills/.system/skill-creator`

仓库内已提供基础 eval 资产：
- [`clarify-first/evals/evals.json`](./clarify-first/evals/evals.json)
- [`clarify-first/evals/README.md`](./clarify-first/evals/README.md)
- [`benchmarks/trigger-evals/clarify-first.json`](./benchmarks/trigger-evals/clarify-first.json)
- [`benchmarks/README.md`](./benchmarks/README.md)

CI 会在每次 push 和 pull request 上自动执行校验。

**本地 CI 预演**（与 GitHub Actions 步骤一致，可在首次 push 前自检）：

```bash
git clone --depth=1 https://github.com/anthropics/skills.git /tmp/anthropic-skills
export SKILL_CREATOR_ROOT=/tmp/anthropic-skills/skills/skill-creator
npm run verify-version
npm run validate:skill
```

若两条命令均通过，远端 workflow 通过概率很高。

## 风险模型

- **低风险**（只读、小范围可逆改动）：agent 可在声明假设后继续，一旦出现新歧义会停下追问。
- **中风险**（重构、改接口等）：agent 先只读检查，给出 2–3 个选项、问清阻塞问题，确认后再做较大改动。
- **高风险**（删除、部署、改密钥等）：agent 会要求你显式确认（如「可以，执行」）后再执行。

详细流程见技能本体：[`clarify-first/SKILL.md`](./clarify-first/SKILL.md)。

## 更易读的确认输出

Clarify First 不只是决定“该不该暂停”，还约束“暂停时怎么说”。

默认对齐输出应尽量简单：
1. 风险头
2. 我已确认
3. 还需确认
4. 可选方案
5. 下一步

中文请求默认用中文标题，英文请求默认用英文标题。只有在高风险、多步骤或用户明确要求详细版时，才展开完整协议结构。

可直接参考这些示例文件：
- [`clarify-first/references/CONFIRMATION_FORMATS.md`](./clarify-first/references/CONFIRMATION_FORMATS.md)
- [`clarify-first/references/EXAMPLES.md`](./clarify-first/references/EXAMPLES.md)
- [`clarify-first/references/QUESTION_BANK.md`](./clarify-first/references/QUESTION_BANK.md)

References 用途说明：
- [`clarify-first/references/CONFIRMATION_FORMATS.md`](./clarify-first/references/CONFIRMATION_FORMATS.md) - 紧凑确认格式与中英文变体
- [`clarify-first/references/EXAMPLES.md`](./clarify-first/references/EXAMPLES.md) - 不同风险等级下的完整示例
- [`clarify-first/references/QUESTION_BANK.md`](./clarify-first/references/QUESTION_BANK.md) - 常见歧义场景的问题模板
- [`clarify-first/references/SCENARIOS.md`](./clarify-first/references/SCENARIOS.md) - 触发场景与边界说明
- [`clarify-first/references/zh-CN.md`](./clarify-first/references/zh-CN.md) - 中文措辞与输出风格说明
- [`clarify-first/references/NFR.md`](./clarify-first/references/NFR.md) - 可维护性与安全等非功能要求

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
│   ├── evals/            # 行为评测样例与字段说明
│   └── references/       # 按需加载的上下文文件
├── benchmarks/           # 触发基准集与基准说明
├── tooling/              # 维护脚本
├── .github/workflows/    # CI 校验工作流
├── .cursorrules          # Cursor 规则模板（精简版）
├── CHANGELOG.md          # 版本历史
└── CONTRIBUTING.md       # 贡献指南
```

技能采用渐进式披露：agent 在触发时加载 `clarify-first/SKILL.md`，仅在需要时打开 `references/*`。

如果你想看这个仓库采用的官方 “test / measure / refine” 思路，可参考：[Improving skill creator: test, measure, and refine agent skills](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills)。

## 参与与协议

欢迎贡献。本项目采用 [Apache-2.0](./LICENSE) 许可。
