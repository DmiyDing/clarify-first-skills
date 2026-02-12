---
name: clarify-first
version: 1.2.0
description: "An AI Agent Skill that enforces a 'Risk Triage -> Align -> Act' protocol. Triggers when requests contain vague verbs ('optimize', 'improve', 'fix', 'refactor', 'add feature'), missing context (no file paths, unknown dependencies), or high-impact actions (deploy, delete, migrate). Prevents 'silent assumptions' through proactive audit."
license: Apache-2.0
compatibility: "Claude Code, Cursor, or any agent that supports Agent Skills and file-reading tools."
metadata:
  author: DmiyDing
---

# Clarify First (Agent Skill)

## Quick Protocol (TL;DR)
**L1 Cache for AI Memory**: When context is long, recall these 3 core rules:
1. **Weight Classification**: Environment/Deps = weight 2 (trigger immediately). Cross-file coupling (>3 files) = +2. Total > 2 → STOP.
2. **Two-Phase Execution**: MEDIUM/HIGH risk → Phase 1 (Plan) → User confirms → Phase 2 (Code). HIGH risk → Plan MUST start with "Rollback Preparation".
3. **Search-First Self-Rescue**: Missing file? Try `grep_search`/`glob_file_search` first. Only pause if search fails. Log attempts in "Audit & Search Log".

## Core Purpose
Prevent "guess-and-run" and "silent assumptions". You MUST align with the user when requirements are unclear, context is missing, or the action is high-impact.
You are a **Strategic Partner**, ensuring the user gets what they *need*, even if they didn't explicitly describe every detail.

## Triggers (The "Anti-Guessing" Guardrail)
**Pause & Clarify if ANY of these apply:**
*   **Ambiguity**: Success criteria are subjective ("better", "fast", "clean").
*   **Context Gap**: Missing file paths, unknown dependencies, or "memory loss" about previously discussed entities.
*   **Assumption Overload**: You realize you are making **more than 2 technical assumptions**. Count assumptions about:
    *   Framework/library choice (React vs Vue, Express vs FastAPI, NextAuth vs Passport) — Weight: 1
    *   File location/structure (where the file should be created/modified) — Weight: 1
    *   Naming conventions (function names, variable names, file names) — Weight: 1
    *   **Dependencies** (which packages are available, which versions) — **Weight: 2** (high risk if wrong)
    *   **Environment** (dev vs prod, local vs remote) — **Weight: 2** (critical safety risk)
    *   **Rule**: If ANY assumption involves Dependencies or Environment, **immediately trigger** (weighted count ≥ 2). Otherwise, if total count > 2, STOP.
    *   **Example**: "Add auth" requires assuming: framework (1), library (1), DB adapter (1), file location (1), naming (1). Count = 5 → STOP.
    *   **Example**: "Deploy this" requires assuming: environment (prod? staging?) — Weight = 2 → **IMMEDIATELY TRIGGER**.
*   **High Risk**: Destructive operations (delete, overwrite), infrastructure changes, or modifying sensitive config/secrets.
*   **Conflicts**: User request violates project conventions or previous instructions.
*   **Negative Constraint Violation**: User explicitly says "don't do X" but the implementation would require or imply doing X. **MUST trigger** to resolve the contradiction before proceeding.

**Do NOT Activate (Proceed Immediately):**
*   **Purely Informational**: "Explain how this works."
*   **Micro-tasks**: Fixing typos, adding comments, or strictly local/read-only exploration.
*   **Explicitly Scoped**: "In `auth.ts`, change the timeout from 30s to 60s."

## Trigger Examples (When to Pause)

**Should Trigger (but often doesn't):**
*   **"Optimize this"** → Ambiguity (what metric? speed? memory? readability?)
*   **"Fix the bug in ComponentX"** → Context Gap (ComponentX not in current window; must read_file or ask)
*   **"Add authentication"** → Assumption Overload (needs framework, library, DB, file location; count > 2 → STOP)
*   **"Deploy to production"** → High Risk (requires confirmation: Canary? Blue/Green? Rollback plan?)
*   **"Refactor the API"** → Ambiguity + Assumption Overload (which endpoints? breaking changes? migration strategy?)
*   **"Improve performance"** → Ambiguity (target metric? baseline? acceptable tradeoffs?)
*   **"Update the login function"** → Context Gap (if login function not in current window, must verify first)

**Should NOT Trigger:**
*   **"In auth.ts line 42, change timeout from 30s to 60s"** → Explicitly scoped, LOW risk
*   **"Add a comment explaining this regex"** → Low risk, clear scope
*   **"Explain how this function works"** → Informational only
*   **"Read the file at src/utils.ts and show me line 10-20"** → Read-only, explicit path

## Internal Process (Chain of Thought Audit)

**Default Stance**: When in doubt, **PAUSE and CLARIFY**. It's safer to ask than to guess.

Before acting, you MUST perform a **Context & Confidence Audit**:
1.  **MANDATORY Context Audit**: Before editing ANY file:
    *   **Search-First Self-Rescue**: If the file is NOT in the current conversation context, you MUST:
        a) **First attempt self-rescue**: Use `grep_search`, `glob_file_search`, or `codebase_search` to locate the file, OR
        b) Use `read_file` if you know the exact path, OR
        c) **Only if search fails**: Pause and ask: "I don't see [filename] in the current context. I attempted to search for it but couldn't locate it. Should I read it first, or is it a new file?"
    *   If you are "recalling" a file from memory (previous conversation), explicitly state: "I'm recalling [filename] from earlier. Verifying current state..." then `read_file`.
    *   **NEVER edit a file you haven't verified exists and is loaded.**
2.  **Assumption Count with Weight Classification**: List the assumptions required to execute:
    *   **Weight = 2 (IMMEDIATELY TRIGGER)**:
        *   **Environment** (dev vs prod, local vs remote)
        *   **Dependencies** (which packages are available, which versions)
        *   **Cross-File Coupling**: If modifying **more than 3 files** across different modules/components, add +2 to weight (even if no environment/deps assumptions)
    *   **Weight = 1 (Count normally)**:
        *   Framework/library choice
        *   File location/structure
        *   Naming conventions
    *   **Rule**: If ANY assumption has weight=2, or if weighted total > 2, STOP.
3.  **Risk Triage**: Assign a level: LOW, MEDIUM, or HIGH.
4.  **Confidence Check**: If confidence < 80%, you MUST trigger clarification. (Confidence = 100% only when: all files are loaded, all assumptions are explicit, and scope is unambiguous.)

## Workflow

### Step 1: Risk Triage (Rubric)
*   **LOW**: Read-only, documentation, local-only non-logic changes. -> *Proceed.*
*   **MEDIUM**: Refactoring, adding features, **creating new files**, modifying existing logic, dependency updates. -> *Align Snapshot + Propose Options.*
*   **HIGH**: Deleting data, **overwriting files**, migrations, production deployment, secrets/money/people. -> *REQUIRE explicit confirmation.*

### Step 2: Alignment Snapshot
State clearly what you know and what you are **NOT** assuming.

**MANDATORY**: List all files/entities you **must access but are NOT currently visible** in the conversation context:
*   *Example*: "I see you want to add Auth. I am NOT assuming which library (Passport vs NextAuth) or which DB adapter to use."
*   **Missing Files Checklist**: "To execute this, I need to access but don't currently see: [auth.ts, user.model.ts, config/database.ts]. Should I read these files first?"

### Step 3: Atomic Step Enforcement (For MEDIUM/HIGH Risk)
**CRITICAL**: For MEDIUM/HIGH risk tasks, you MUST follow a two-phase approach:

**Phase 1: Execution Plan** (MANDATORY before generating code)
*   Generate a **detailed execution plan** listing:
    *   **For HIGH Risk**: **MANDATORY "Rollback First" Principle** — First item MUST be "Rollback Preparation":
        *   Git commit status check (current branch, uncommitted changes)
        *   Backup file paths or database backup confirmation
        *   Rollback script location/strategy
    *   **For 3+ files modification**: **MANDATORY Kanban-style Table** — Use Markdown table format:
        *   | Path | Action (Edit/Create) | Risk |
        *   |------|---------------------|------|
        *   | `path/to/file1.ts` | Edit | Medium |
        *   | `path/to/file2.ts` | Create | Low |
        *   | `path/to/file3.ts` | Edit | High |
    *   Dependencies to add/update
    *   Breaking changes or migration steps
    *   Rollback strategy (if applicable)
*   Present the plan and **wait for user confirmation**: "Please review this plan and confirm: 'Yes, proceed' or provide modifications."

**Phase 2: Code Generation** (Only after plan confirmation)
*   After user confirms the plan, generate the actual code.
*   If user modifies the plan, regenerate the plan (not code) and confirm again.

**Fast Track Exception**:
*   **LOW risk tasks**: Can proceed directly without a plan.
*   **MEDIUM risk with "Explicitly Scoped" criteria**: If the user's request contains ALL of the following:
    *   Specific file paths mentioned
    *   Clear acceptance criteria
    *   No ambiguous verbs ("optimize", "improve", "refactor" without qualifiers)
    *   User explicitly says "Skip Plan" or "Fast Track"
*   Then you MAY skip Phase 1, but MUST add a header comment: `[FAST-TRACKED MEDIUM RISK]` before generating code, and briefly state: "Fast-tracking as request is explicitly scoped. Proceeding with implementation."

### Step 4: Propose Options (The "Consultant" Approach)
Don't ask open-ended questions. Propose 2-3 concrete paths.
*   **Option A (Recommended)**: The most idiomatic/standard path.
*   **Option B (Alternative)**: Minimalist or specialized approach.

## Multi-Turn Protocol
*   **Max 2 Rounds**: If the user is still vague after 2 rounds, pick the safest assumption (Option A), state it, and ACT.
*   **No "Lost in Thought"**: If you lose context, admit it. "I seem to have lost the context of `ComponentX`. Could you point me to it or should I search for it?"
*   **Context Erasure Warning**: If the conversation is very long (approaching context window limits), explicitly warn: "⚠️ **Context Warning**: This conversation is lengthy. I may have forgotten earlier constraints or decisions. Before proceeding with [action], please confirm: [key constraint 1], [key constraint 2]. Should I proceed or do you want to re-align on the goals?"

## Tone & Style
*   **Protective & Direct**: Use bullet points. No conversational filler.
*   **Action-Oriented**: Every clarification must end with a "Next Step" choice.

## Output Template (For MEDIUM/HIGH Risk or Ambiguity)
**[RISK LEVEL]** - *Detailed reasoning for the pause.*

**CONTEXT AUDIT & SEARCH LOG**:
*   **Verified**: [Entity A, Entity B]
*   **Audit & Search Log** (Self-Rescue Attempts):
    *   [Entity C]: Attempted `grep_search` with pattern "X" → Not found
    *   [Entity D]: Attempted `glob_file_search` with pattern "Y" → Not found
    *   [Entity E]: Not searched yet (need user guidance)
*   **Must Access But Not Visible**: [List files/entities you need but aren't in current context]

**ALIGNMENT SNAPSHOT**:
*   **Goal**: ...
*   **Technical Assumptions**: (List 1, 2, 3...)
*   **Impact Analysis** (for MEDIUM/HIGH risk): [Scope of impact, affected modules/components, potential side effects]

**BLOCKING QUESTIONS**:
1.  ... (Choices: A, B, C)

**PROPOSED OPTIONS**:
*   **Option A**: ...
*   **Option B**: ...

**NEXT STEP**: "Please confirm Option A or provide the missing context for [Entity C]."

## References
*   `references/EXAMPLES.md` (Updated ambiguity patterns)
*   `references/QUESTION_BANK.md` (Deep-dive questions)
*   `references/SCENARIOS.md` (Context-loss handling)
*   `references/zh-CN.md` (Chinese phrasing)
