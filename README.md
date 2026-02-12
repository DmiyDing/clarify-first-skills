# Clarify First: The "Ask-Before-Act" Protocol

[![License](https://img.shields.io/github/license/DmiyDing/clarify-first)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/DmiyDing/clarify-first/pulls)
[![Spec](https://img.shields.io/badge/Spec-Agent--Skills-blueviolet)](https://agentskills.io/specification)
[![Cursor Compatible](https://img.shields.io/badge/Cursor-Compatible-blue)](https://cursor.com)

**Stop AI from guessing. Force your Agent to ask the right questions before touching your code.**

Clarify First is a skill designed for one purpose: **Clarification**. It stops AI agents from blindly executing when requirements are vague, conflicting, or high-risk. It transforms the AI from a reckless executor into a thoughtful partner that aligns on scope *before* acting.

[中文](./README.zh-CN.md) · **License:** [Apache-2.0](./LICENSE)

---

## The Problem: "Guess-and-Run"
Most AI coding assistants try to be too helpful. When you give a vague instruction like *"Optimize this,"* they start refactoring immediately without knowing if you care about speed, readability, or memory.

**Clarify First** flips the script: **Clarify First, Code Second.**

## Core Features
*   ❓ **Proactive Clarification:** If the goal is 1% ambiguous, the AI must ask for missing context.
*   🤝 **Scope Alignment:** Proposes options (A/B/C) to make sure you are on the same page.
*   🛑 **Execution Gate:** Stops the AI from running destructive or high-impact commands until you say "Yes".

## Example: The Power of a Question

| Blind Execution (Standard) | Clarified Execution (With This Skill) |
|-----------------------|--------------------|
| You: *"Optimize the app."* | You: *"Optimize the app."* |
| Agent starts massive refactors. | Agent: **"Risk: Medium. I need to clarify: are we optimizing for runtime speed, bundle size, or code readability?"** |
| Result: Broken code, wrong focus. | Result: The AI does exactly what you needed. |

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

Details and workflows are in the skill body: `clarify-first/SKILL.md`.

## Compatibility

- **Agent Skills**: This repo follows the [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) convention (Anthropic). The skill lives in the `clarify-first/` directory: `clarify-first/SKILL.md` (YAML frontmatter + Markdown).
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
├── clarify-first/
│   ├── SKILL.md          # Core skill definition (Markdown)
│   └── references/       # Context files loaded on demand
├── tooling/              # Maintenance scripts
├── .cursorrules          # Cursor rule template (condensed)
├── CHANGELOG.md          # Version history
└── CONTRIBUTING.md       # Contribution guide
```

## Standards & Compliance
This skill follows the [Agent Skills specification](https://agentskills.io/specification) and is compatible with:
*   [Claude Code](https://claude.ai)
*   [Cursor](https://cursor.com)

The skill uses progressive disclosure: the agent loads `clarify-first/SKILL.md` when the skill triggers, and only opens `references/*` when needed.

## Future Roadmap

See [`docs/FUTURE_OPTIMIZATIONS.md`](./docs/FUTURE_OPTIMIZATIONS.md) for planned enhancements in v1.3.0+:
- **Adaptive Confidence Threshold**: Dynamic threshold adjustment based on user behavior (beginner: 90%, expert: 70%)
- Enhanced multilingual support
- Context memory improvements
- Collaboration features

## Contributing and license

Contributions are welcome. This project is licensed under [Apache-2.0](./LICENSE).
