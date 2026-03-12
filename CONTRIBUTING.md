# Contributing to Clarify First

We welcome contributions! This project aims to define a standard for AI Agent behavior when facing ambiguity.

## Repository Structure
*   `clarify-first/SKILL.md`: The core skill definition (Markdown).
*   `clarify-first/references/`: Context files loaded on demand.
*   `tooling/`: Maintenance scripts (not agent-executable).

## How to Contribute
1.  **Fork** the repo.
2.  **Create a branch** for your feature/fix.
3.  **Update `clarify-first/SKILL.md`** if you are changing core logic.
4.  **Sync References**: If you add a new concept, update `clarify-first/references/` accordingly.
5.  **Update `CHANGELOG.md`**: Add your change under an `[Unreleased]` section.
6.  **Bump version** in `package.json`, `CHANGELOG.md`, and all versioned files under `clarify-first/references/`.
7.  **Verify Version**: Run `npm run verify-version` to ensure all versions match.
8.  **Validate Skill**: Run `skills-ref validate ./clarify-first` if available, or `npm run validate:skill` after configuring `SKILL_CREATOR_ROOT` or `SKILL_CREATOR_SCRIPTS`.
9.  **Measure Trigger Quality**: Run `npm run benchmark:trigger` after configuring `SKILL_CREATOR_ROOT` or `SKILL_CREATOR_SCRIPTS` to compare trigger behavior against the current benchmark set.
10. **Sync `.cursorrules`**: Ensure `.cursorrules` remains a strict, condensed subset of `clarify-first/SKILL.md`.
    *   Rubric levels (Low/Medium/High) match?
    *   Protocol (Assess -> Align -> Act) matches?
    *   Anti-Patterns (especially High-risk "Just do it") included?
    *   Output Template structure matches?
11. **Submit a PR**.

## Scope
*   **In Scope**: New high-risk scenarios, better phrasing, additional languages.
*   **Out of Scope**: Framework-specific code (this is a Prompt/Skill, not a library).

## Versioning
We follow Semantic Versioning.
*   Major: Breaking changes to the protocol.
*   Minor: New features/scenarios.
*   Patch: Typos, phrasing tweaks.

## Verification Checklist

Validation should remain portable:

1.  Preferred: `skills-ref validate ./clarify-first`
2.  Alternative: `npm run validate:skill`
3.  Benchmark: `npm run benchmark:trigger`

The npm-based commands auto-discover a local Anthropic `skill-creator` install from:
*   `SKILL_CREATOR_ROOT`
*   `SKILL_CREATOR_SCRIPTS`
*   `~/.claude/skills/skill-creator`
*   `~/.codex/skills/.system/skill-creator`

When editing the frontmatter description:
*   Treat it as the primary trigger surface for the skill.
*   Keep it under 1024 characters.
*   Preserve the current trigger keywords unless you have benchmark evidence for changing them.

After modifying `SKILL.md` or `references/`, manually verify these scenarios still behave correctly:

1.  **Ambiguous request** (e.g., "optimize this") → Agent triggers MEDIUM risk, proposes options.
2.  **High-risk destructive** (e.g., "delete all users") → Agent triggers HIGH risk, requires explicit confirmation.
3.  **"Just do it" on HIGH risk** → Agent performs one final safety check before executing.
4.  **Low-risk precise request** (e.g., "add a comment to this line") → Agent proceeds immediately, no clarification.
5.  **Chinese input** → Agent responds using phrasing from `references/zh-CN.md`.

These scenarios are documented in `references/EXAMPLES.md`. If your change alters expected behavior, update the examples accordingly.
