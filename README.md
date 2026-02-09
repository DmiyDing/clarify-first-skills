# Clarify First

[![License](https://img.shields.io/github/license/DmiyDing/clarify-first)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/DmiyDing/clarify-first/pulls)
[![Smithery](https://img.shields.io/badge/Smithery-Available-orange)](https://smithery.ai/skills/DmiyDing/clarify-first)
[![Cursor Compatible](https://img.shields.io/badge/Cursor-Compatible-blue)](https://cursor.com)

**Stop AI from guessing. Transform your Agent into a Technical Partner.**

Clarify First is a defensive [Agent Skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) that enforces a **Risk Triage** protocol. It makes Claude, Cursor, and other agents pause on vague, conflicting, or high-impact requests to align on scope and safety *before* changing files or running commands.

[中文](./README.zh-CN.md) · **License:** [Apache-2.0](./LICENSE)

---

## Why

AI coding assistants often **guess and proceed** when your request is ambiguous. The result: incorrect refactors, broken dependencies, and lost trust.

Clarify First adds a strategic gate:
*   🛑 **Prevents "Guess-and-Run":** No more undoing massive, incorrect edits.
*   🛡️ **Safety Guardrails:** Stops accidental production deployments or data deletions.
*   🤝 **Better Alignment:** Forces the agent to summarize assumptions and propose options (A/B/C) like a human senior engineer.

## Example

| Without Clarify First | With Clarify First |
|-----------------------|--------------------|
| You: *"Optimize the app and ship it."* | You: *"Optimize the app and ship it."* |
| Agent starts refactoring and changing files. | Agent pauses and asks: scope (quick wins vs full refactor?), definition of "shipped", and your preferred option. |
| You: *"I only wanted to fix one slow query…"* | You: *"Quick wins; shipped = deploy to staging with green checklist."* |
| Rework and frustration. | Agent proceeds with clear scope; no rework. |

## Install

**For Cursor, Claude Code, and other clients that support Agent Skills:**

```bash
npx -y skills add DmiyDing/clarify-first
```

Restart your client after installation. If the skill doesn’t auto-trigger, say: *"Use the clarify-first skill."*

**Codex (AGENTS.md):** To bake the behavior into a repo or global config, add the [snippet below](#codex-agentsmd-snippet) to `AGENTS.override.md` or `AGENTS.md`.

## Usage

After install, the skill activates when the agent detects ambiguous or high-impact requests. You can also invoke it explicitly:

- *"Use the clarify-first skill. If anything is ambiguous or high-impact, ask me the blocking questions first."*

The agent will then align on scope, ask 1–5 targeted questions (with choices when possible), and wait for your confirmation before making changes or running commands.

## How it works

- **Low risk** (read-only, small reversible edits): the agent may proceed with explicit assumptions and will stop if new ambiguity appears.
- **Medium risk** (refactors, API changes, etc.): the agent inspects first, proposes 2–3 options, asks blocking questions, and waits for confirmation before larger edits.
- **High risk** (deletes, deploy, secrets, etc.): the agent requires explicit confirmation (e.g. *"Yes, proceed"*) before taking action.

Details and workflows are in the skill body: `skill.md`.

## Compatibility

- **Agent Skills**: This repo follows the [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) convention (Anthropic). The skill consists of a `skill.md` (YAML frontmatter + markdown) at the root.
- **Clients**: Cursor, Claude Code, Codex, and any client that supports loading Agent Skills from a GitHub repo or local path.

### Codex AGENTS.md snippet

For Codex, paste this into `AGENTS.override.md` or `AGENTS.md` (repo or `~/.codex/`):

```markdown
# Clarify First (risk-based)

When a request is ambiguous, underspecified, conflicting, or high-impact, do not guess.

Risk triage:
- Low: proceed with explicit assumptions and minimal reversible steps; stop if new ambiguity appears.
- Medium: inspect read-only first; propose 2–3 options; ask only blocking questions; wait for confirmation before larger edits or running commands.
- High: require explicit confirmation ("Yes, proceed") before any irreversible action (side-effect commands, deletion/overwrite, migrations, deploy/publish, secrets/config changes, spending money, contacting people).

If you see a better approach than requested, present it as an option and ask the user to choose.
```

## Repository structure

```
.
├── skill.md           # Skill definition, workflow, anti-patterns
└── references/
    ├── zh-CN.md       # Chinese phrasing templates
    ├── EXAMPLES.md    # Example inputs and expected behavior
    ├── QUESTION_BANK.md
    ├── SCENARIOS.md   # Bug report, design/RFC, feature-scope scenarios
    └── NFR.md         # Non-functional requirements clarification checklist
```

The skill uses progressive disclosure: the agent loads `skill.md` when the skill triggers, and only opens `references/*` when needed.

## Contributing and license

Contributions are welcome. This project is licensed under [Apache-2.0](./LICENSE).
