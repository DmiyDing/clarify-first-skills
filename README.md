# Clarify First Skills (Agent Skill)

[Chinese README](./README.zh-CN.md)

A risk-based clarification gate for AI agents and AI coding tools. When a request is ambiguous, underspecified, or conflicting, the agent must **pause**, summarize context, ask targeted clarification questions, and obtain confirmation before taking medium/high-risk actions.

- Skill: `skills/clarify-first/SKILL.md`
- Skill name: `clarify-first`
- License: Apache-2.0

## Why

AI assistants fail in a predictable way: **they guess** and proceed. That creates wrong work, rework, and trust loss.

This skill enforces:
- Clear alignment when uncertainty is high
- Explicit assumptions when uncertainty is low
- A safety valve before irreversible actions

## What it does (Mode B: risk-based)

- **Low risk**: proceed with explicit assumptions + minimal, reversible steps; stop if new ambiguity appears
- **Medium risk**: inspect first, propose 2–3 options, ask only the blocking questions, then wait for confirmation before larger edits
- **High risk**: require explicit confirmation before any irreversible action (running side-effect commands, deletion/overwrite, migrations, deploy/publish, secrets/config changes, spending money, contacting people)

## What are “Agent Skills” (practical)

This repo follows the Agent Skills convention (as used in Anthropic examples):
- A skill is a folder containing a required `SKILL.md`
- `SKILL.md` starts with YAML frontmatter (at minimum `name` + `description`)
- The agent uses `description` to decide when to activate the skill; the body is the workflow once activated

## Install

### 1) Recommended: `skills` CLI (multi-client installer)

If your agent/client supports Agent Skills, install from GitHub:

```bash
npx -y skills add DmiyDing/clarify-first-skills --skill clarify-first
```

Notes:
- `add-skill` was renamed to `skills` (the old name may print a deprecation warning and forward automatically).
- You may need to restart your client after installation.
- If auto-trigger is flaky, explicitly say: “Use the `clarify-first` skill.”

Troubleshooting:
- **Cursor doesn’t show the skill**: verify a real folder exists at `~/.cursor/skills/clarify-first/` with `SKILL.md`. Some Cursor builds may not discover **symlinked** skill folders; reinstall choosing “Copy” instead of “Symlink”, or manually replace the symlink with a real directory.

### 2) OpenAI Codex CLI (recommended integration)

OpenAI Codex CLI reliably loads instruction files named `AGENTS.md` / `AGENTS.override.md` (and the same under `~/.codex/` for global defaults). To make this behavior “always on”, add it to either:

- Repo scope: `<your-repo>/AGENTS.override.md` (preferred), or `<your-repo>/AGENTS.md`
- Global scope: `~/.codex/AGENTS.override.md` (preferred), or `~/.codex/AGENTS.md`

Suggested snippet (paste as-is, keep it short):

```markdown
# Clarify First (risk-based)

When a request is ambiguous, underspecified, conflicting, or high-impact, do not guess.

Risk triage:
- Low: proceed with explicit assumptions and minimal reversible steps; stop if new ambiguity appears.
- Medium: inspect read-only first; propose 2–3 options; ask only blocking questions; wait for confirmation before larger edits or running commands.
- High: require explicit confirmation ("Yes, proceed") before any irreversible action (side-effect commands, deletion/overwrite, migrations, deploy/publish, secrets/config changes, spending money, contacting people).

If you see a better approach than requested, present it as an option and ask the user to choose.
```

If you tell me whether you prefer repo-scope or global-scope, I can tailor the snippet to your workflow and risk tolerance.

## Use

Most reliable:
- “Use the `clarify-first` skill. If anything is ambiguous or high-impact, ask me the blocking questions first.”

## Design principles

- Alignment before action when uncertainty is high
- Ask fewer, better questions (prefer choices; 1–5 questions)
- Provide options with tradeoffs (don’t silently override user intent)
- Progressive disclosure: keep the core workflow compact; move long examples into references
- Reversible by default: small steps → confirm → expand

## Repo layout

```
skills/
  clarify-first/
    SKILL.md
    references/
      zh-CN.md
```

## Publishing to Smithery (later)

Once you’ve validated the repo in real usage:
- Create a release/tag (e.g. `v0.1.0`)
- Publish the GitHub URL on Smithery as a Skill listing (so users can install via a `smithery.ai/skills/<namespace>/<slug>` URL)
- Add a short “Install” section in the Smithery listing that mirrors the install command above
- Ask early users to submit reviews (Smithery supports reviews on skill pages)
 - Add one “before/after” usage example (a short chat transcript) to make the value obvious in 10 seconds

## GitHub Description (copy/paste)

`Risk-based clarification gate for AI agents — ask before acting on ambiguous or high-impact requests.`
