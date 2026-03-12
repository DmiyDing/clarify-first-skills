# Clarify First: The "Ask-Before-Act" Protocol

[![License](https://img.shields.io/github/license/DmiyDing/clarify-first)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/DmiyDing/clarify-first/pulls)
[![CI](https://github.com/DmiyDing/clarify-first/actions/workflows/validate-skill.yml/badge.svg)](https://github.com/DmiyDing/clarify-first/actions/workflows/validate-skill.yml)
[![Spec](https://img.shields.io/badge/Spec-Agent--Skills-blueviolet)](https://agentskills.io/specification)
[![Cursor Compatible](https://img.shields.io/badge/Cursor-Compatible-blue)](https://cursor.com)

**Stop your AI from guessing. Clarify First is a deterministic state-machine and safety middleware that forces agents to ask before acting on ambiguous or high-risk tasks.**

Clarify First is a protocol-first skill focused on one thing: **alignment before execution**. It blocks silent assumptions, enforces explicit confirmation, and keeps plan vs execution auditable.

[中文](./README.zh-CN.md) · **License:** [Apache-2.0](./LICENSE)

---

## Why You Need This
Most coding agents optimize for immediacy, not certainty. In ambiguous or high-impact requests, this creates hidden assumptions and expensive mistakes.

**Clarify First** flips the default to: **Clarify First, Code Second**.

## What You Get

With Clarify First, the agent is much more likely to:

1. Stop before guessing on vague requests like "optimize", "fix", or "improve".
2. Ask only the blocking questions, instead of dumping a wall of protocol text.
3. Require explicit confirmation before destructive actions such as delete, deploy, migrate, or overwrite.
4. Keep medium/high-risk work auditable with a plan-first workflow.
5. Mirror the user's language and present confirmation in a compact, readable format.

## Without vs With

| Without Clarify First | With Clarify First |
|-----------------------|--------------------|
| User: "Delete old files." | User: "Delete old files." |
| Agent runs destructive command with assumptions. | Agent emits risk header, asks target scope + rollback, waits for confirmation. |
| Result: Wrong scope / hard recovery. | Result: Intent-aligned, reversible execution path. |

## Core Capabilities

| Capability | Included |
|------------|----------|
| Non-bypass clarification gate | ✅ |
| Weighted assumption triage | ✅ |
| Two-phase plan lock (Plan -> Confirm -> Execute) | ✅ |
| Strict execution boundary + amendment protocol | ✅ |
| Progressive execution for dependent high-risk actions | ✅ |
| Plan-ID anchoring + long-thread checkpoint recall | ✅ |
| Security redaction in audit outputs | ✅ |
| Architectural anti-pattern hard stop | ✅ |
| Contextual risk modifier (file centrality aware) | ✅ |
| Final reconciliation (plan vs actual) | ✅ |
| Multi-agent handoff payload (scoped pointers) | ✅ |
| Adversarial trigger tests in tooling | ✅ |
| Official-style eval assets (`evals/evals.json`) | ✅ |
| Official-style trigger benchmark wrapper | ✅ |

## Example: The Power of a Question

| Blind Execution (Standard) | Clarified Execution (With This Skill) |
|-----------------------|--------------------|
| You: *"Optimize the app."* | You: *"Optimize the app."* |
| Agent starts massive refactors. | Agent: **"Risk: Medium. I need to clarify: are we optimizing for runtime speed, bundle size, or code readability?"** |
| Result: Broken code, wrong focus. | Result: The AI does exactly what you needed. |

## Quick Start

### 1) Cursor / Windsurf style clients
- Copy [`/.cursorrules`](./.cursorrules) into your project root (or merge into your existing rules file).

### 2) Agent Skills compatible clients
- Install from registry/repo:

```bash
npx -y skills add DmiyDing/clarify-first
```

Restart your client after installation. If auto-trigger is weak, explicitly invoke: *"Use the clarify-first skill."*

### 3) Codex / AGENTS.md environments
- Add the [snippet below](#codex-agentsmd-snippet) to `AGENTS.override.md` or `AGENTS.md`.

### 4) Framework orchestration (LangChain / Dify / custom agent runtime)
- Inject core protocol as system policy from [`clarify-first/SKILL.md`](./clarify-first/SKILL.md).
- Keep references (`references/*`) as on-demand context files, not always-on prompt payload.

## What It Looks Like

After install, the skill activates when the agent detects ambiguous or high-impact requests. You can also invoke it explicitly:

- *"Use the clarify-first skill. If anything is ambiguous or high-impact, ask me the blocking questions first."*

The agent will then align on scope, ask 1–5 targeted questions (with choices when possible), and wait for your confirmation before making changes or running commands.

Default confirmation shape:
1. Risk
2. Confirmed
3. Need From You
4. Options
5. Next Step

## Verification

Version and reference consistency can be checked with:
- [`tooling/verify-version.js`](./tooling/verify-version.js)

Skill validation and trigger measurement can be checked with:
- `skills-ref validate ./clarify-first`
- `npm run validate:skill`
- `npm run benchmark:trigger`

The npm-based commands auto-discover a local Anthropic `skill-creator` install from:
- `SKILL_CREATOR_ROOT`
- `SKILL_CREATOR_SCRIPTS`
- `~/.claude/skills/skill-creator`
- `~/.codex/skills/.system/skill-creator`

The repository also ships starter eval cases in:
- [`clarify-first/evals/evals.json`](./clarify-first/evals/evals.json)
- [`clarify-first/evals/README.md`](./clarify-first/evals/README.md)
- [`benchmarks/trigger-evals/clarify-first.json`](./benchmarks/trigger-evals/clarify-first.json)
- [`benchmarks/README.md`](./benchmarks/README.md)

CI runs validation on every push and pull request.

**Local CI rehearsal** (same steps as GitHub Actions, before your first push):

```bash
git clone --depth=1 https://github.com/anthropics/skills.git /tmp/anthropic-skills
export SKILL_CREATOR_ROOT=/tmp/anthropic-skills/skills/skill-creator
npm run verify-version
npm run validate:skill
```

If both commands pass, the workflow is very likely to pass on the remote.

## Risk Model

- **Low risk** (read-only, small reversible edits): the agent may proceed with explicit assumptions and will stop if new ambiguity appears.
- **Medium risk** (refactors, API changes, etc.): the agent inspects first, proposes 2–3 options, asks blocking questions, and waits for confirmation before larger edits.
- **High risk** (deletes, deploy, secrets, etc.): the agent requires explicit confirmation (e.g. *"Yes, proceed"*) before taking action.

Details and workflows are in [`clarify-first/SKILL.md`](./clarify-first/SKILL.md).

## Human-Friendly Confirmation Output

Clarify First is opinionated about the *format* of clarification, not only the trigger logic.

The default user-facing confirmation format is intentionally simple:
1. Risk header
2. Confirmed facts
3. What is still needed
4. Two options with tradeoffs
5. Next step

For Chinese prompts, headings should stay in Chinese. For English prompts, headings should stay in English. The full protocol can still expand for HIGH-risk or multi-step cases, but the default experience should remain readable.

Reference examples live here:
- [`clarify-first/references/CONFIRMATION_FORMATS.md`](./clarify-first/references/CONFIRMATION_FORMATS.md)
- [`clarify-first/references/EXAMPLES.md`](./clarify-first/references/EXAMPLES.md)
- [`clarify-first/references/QUESTION_BANK.md`](./clarify-first/references/QUESTION_BANK.md)

References overview:
- [`clarify-first/references/CONFIRMATION_FORMATS.md`](./clarify-first/references/CONFIRMATION_FORMATS.md) - compact clarification output patterns and language variants
- [`clarify-first/references/EXAMPLES.md`](./clarify-first/references/EXAMPLES.md) - end-to-end example interactions across risk levels
- [`clarify-first/references/QUESTION_BANK.md`](./clarify-first/references/QUESTION_BANK.md) - blocking-question toolkit for common ambiguity types
- [`clarify-first/references/SCENARIOS.md`](./clarify-first/references/SCENARIOS.md) - scenario coverage and trigger guidance
- [`clarify-first/references/zh-CN.md`](./clarify-first/references/zh-CN.md) - Chinese phrasing and response style notes
- [`clarify-first/references/NFR.md`](./clarify-first/references/NFR.md) - non-functional requirements for maintainability and safety

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

## Repository Structure

```
.
├── clarify-first/
│   ├── SKILL.md          # Core skill definition (Markdown)
│   ├── evals/            # Behavioral eval prompts and schema notes
│   └── references/       # Context files loaded on demand
├── benchmarks/           # Trigger benchmark sets and benchmark notes
├── tooling/              # Maintenance scripts
├── .github/workflows/    # CI validation workflow
├── .cursorrules          # Cursor rule template (condensed)
├── CHANGELOG.md          # Version history
└── CONTRIBUTING.md       # Contribution guide
```

## Standards & Compliance
This skill follows the [Agent Skills specification](https://agentskills.io/specification) and is compatible with:
*   [Claude Code](https://claude.ai)
*   [Cursor](https://cursor.com)

The skill uses progressive disclosure: the agent loads `clarify-first/SKILL.md` when the skill triggers, and only opens `references/*` when needed.

For the official test/measure/refine workflow behind this repo's benchmark and eval setup, see [Improving skill creator: test, measure, and refine agent skills](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills).

## Contributing and license

Contributions are welcome. This project is licensed under [Apache-2.0](./LICENSE).
