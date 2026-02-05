# Clarify First Skills (Agent Skill) / 先澄清再执行（技能）

**EN:** A risk-based clarification gate for AI agents and AI coding tools. When a request is ambiguous, underspecified, or conflicting, the agent must *pause*, summarize context, ask targeted clarification questions, and obtain confirmation before taking medium/high-risk actions.  
**中文：** 面向 AI / AI 编程工具的“风险分级澄清闸门”。当需求模糊、不完整或存在冲突时，AI 必须先暂停执行，梳理上下文、列出不确定点并提问澄清，在进行中/高风险操作前获得用户确认。

- Skill: `skills/clarify-first/SKILL.md`
- Skill name: `clarify-first`

---

## Why / 为什么要做这个

- Avoid “guess-and-run” (wrong work, rework, trust loss) / 避免“猜着做”，减少返工与误解
- Make assumptions explicit (fast alignment) / 把隐含假设显式化，快速对齐
- Add a safety layer for irreversible actions / 对不可逆操作加一道安全阀
- Improve throughput in real-world engineering / 提升真实工程场景的交付效率

---

## What it does / 它做什么

**Risk-based (Mode B) / 风险分级（B 模式）**

- **Low risk / 低风险**：允许继续，但必须声明假设、保持可逆、最小改动；遇到新歧义立即停下追问
- **Medium risk / 中风险**：先做只读检查 + 给 2–3 个方案 + 问关键问题；确认后再进行较大改动
- **High risk / 高风险**：必须先确认（尤其是运行有副作用命令、删除/覆盖、迁移、发布/部署、改配置/密钥、花钱、联系他人等）

**Output discipline / 输出纪律**

- 先“对齐快照” → 再“阻塞问题” → 再“可选问题” → 再“选项与权衡” → 再“下一步需要你确认什么”
- 尽量只问 1–5 个问题，每个问题给 2–3 个选项（含推荐项）
- 用户中文就中文问；用户英文就英文问

---

## What are “Agent Skills”? / Agent Skills 是什么（实用定义）

This repo follows the “Agent Skills” convention used by Anthropic examples:

- A skill is a folder that contains a required `SKILL.md`
- `SKILL.md` starts with YAML frontmatter (at minimum `name` + `description`)
- The agent uses `description` to decide when to activate the skill; the body is the workflow once activated

---

## Installation / 安装

### Option A — Skills CLI ecosystem (recommended) / 推荐：Skills CLI 生态

Many agentic coding tools support installing Agent Skills via a `skills` CLI and an agent selector. The exact `--agent` name varies by tool.

```bash
# Install from a GitHub repo URL (recommended for open-source distribution)
npx skills add https://github.com/DmiyDing/clarify-first-skills@clarify-first --agent <agent-name>
```

Examples (adjust `--agent` to your tool):

```bash
npx skills add https://github.com/DmiyDing/clarify-first-skills@clarify-first --agent claude-code
npx skills add https://github.com/DmiyDing/clarify-first-skills@clarify-first --agent cursor
npx skills add https://github.com/DmiyDing/clarify-first-skills@clarify-first --agent codex
npx skills add https://github.com/DmiyDing/clarify-first-skills@clarify-first --agent windsurf
npx skills add https://github.com/DmiyDing/clarify-first-skills@clarify-first --agent github-copilot
npx skills add https://github.com/DmiyDing/clarify-first-skills@clarify-first --agent gemini-cli
```

Notes / 注意：
- Some tools require restart after installing skills / 有些工具安装后需要重启
- If auto-trigger is flaky, explicitly say: “Use the `clarify-first` skill.” / 若自动触发不稳定，建议显式点名

### Option B — Manual copy / 手动复制

If your agent/tool has a “skills directory”, copy the folder:

- Copy `skills/clarify-first/` into your agent’s skills directory
- Ensure `SKILL.md` remains at the root of the skill folder

---

## Usage / 使用方式

### 1) Explicit invocation / 显式调用（最可靠）

- EN: “Use the `clarify-first` skill and ask me any blocking questions before making changes.”
- 中文：“使用 `clarify-first` 技能。对中/高风险操作先问我确认，不要猜。”

### 2) Natural trigger / 自然触发（取决于工具的技能发现能力）

The skill should activate when the user request is ambiguous, underspecified, or conflicting.

---

## Design principles / 设计理念（追求卓越）

- **Alignment > action** when uncertainty is high / 不确定性高时，对齐优先于行动
- **Ask fewer, better questions** / 少问但问到点子上
- **Provide options with tradeoffs** / 给方案与权衡，而不是替用户“擅自决定”
- **Progressive disclosure** / 必要时才展开细节，避免提示词臃肿
- **Reversible by default** / 默认可逆：先小步、再确认、再扩展

---

## Repository layout / 仓库结构

```
skills/
  clarify-first/
    SKILL.md
```

---

## License / 许可证

Apache-2.0. See `LICENSE`.

---

## Suggested GitHub description / GitHub 项目描述（中英文）

Use one of these as your repo “Description”:

- EN: `Risk-based clarification gate for AI agents: ask before acting on ambiguous or high-impact requests.`
- 中文：`面向 AI 编程工具的风险分级澄清闸门：需求不清先澄清再执行，避免误解与返工。`
- EN + 中文（合并版）：`Risk-based clarification gate for AI agents — 需求不清先澄清再执行。`

---

## Roadmap / 路线图（可选）

- Add a compact “compatibility matrix” once you confirm exact clients and install paths
- Add “conflict resolution” mini-framework (priority rules + examples)
- Add canned question sets per domain (backend, frontend, data, devops) as small reference files
