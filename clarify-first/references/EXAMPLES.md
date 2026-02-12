# Clarify First — Examples

> **Version**: 1.2.0  
> **Last Updated**: 2026-02-12  
> **Compatibility**: Matches clarify-first/SKILL.md v1.2.0 (includes Execution Plan, Weight Classification, Fast Track, Search-First Context Audit)

## 1. Ambiguous Request (Medium Risk) - v1.2.0 Format
**User**: "Optimize the code."
**Agent**:
> **[RISK: MEDIUM]** - "Optimize" is subjective (speed vs. readability vs. memory).
>
> **CONTEXT AUDIT & SEARCH LOG**:
> *   **Verified**: [Current file in context]
> *   **Audit & Search Log** (Self-Rescue Attempts):
>     *   [Target files]: Not searched yet (need to identify hot paths first)
>   **Must Access But Not Visible**: [Need to analyze codebase structure to identify optimization targets]
>
> **ALIGNMENT SNAPSHOT**:
> *   **Goal**: Improve code quality/performance.
> *   **Technical Assumptions (Weight Count)**: 
>     *   Target metric (1) - CPU vs RAM vs readability
>     *   Hot paths to focus (1) - which functions/files
>     *   **Total Weight**: 2 (not triggering yet, but close)
>   **Unknowns**: Target metric (CPU, RAM, bundle size) or maintainability?
>
> **BLOCKING QUESTIONS**:
> *   Q1: What is the primary goal? (A: **Runtime Speed**, B: **Memory Usage**, C: **Code Readability/Cleanup**)
> *   Q2: Are there specific hot-paths to focus on?
>
> **PROPOSED OPTIONS**:
> *   **Option A (Recommended)**: Refactor for readability and strict typing (safest).
> *   **Option B**: Aggressive performance optimization (might reduce readability).
>
> **NEXT STEP**: Please confirm Option A or clarify the goal.

## 2. Conflicting Constraints (Medium Risk) - v1.2.0 Format
**User**: "Refactor this to be generic, but don't change any interfaces."
**Agent**:
> **[RISK: MEDIUM]** - Making code "generic" usually implies changing signatures (interfaces).
>
> **CONTEXT AUDIT & SEARCH LOG**:
> *   **Verified**: [Current file in context]
> *   **Audit & Search Log** (Self-Rescue Attempts):
>     *   [Related interfaces]: Not searched yet (need to identify all affected interfaces)
> *   **Must Access But Not Visible**: [Need to verify all call sites of current interface]
>
> **ALIGNMENT SNAPSHOT**:
> *   **Goal**: Generalize logic.
> *   **Constraint**: Keep current interfaces identical (Backwards Compatibility).
> *   **Technical Assumptions**: None (constraint is clear)
> *   **Impact Analysis**: 
>     *   **影响范围**: 当前函数及其调用点
>     *   **受影响模块**: 所有调用此接口的模块
>     *   **潜在副作用**: 如果违反约束，可能导致破坏性变更
>
> **PROPOSED OPTIONS**:
> *   **Option A (Wrapper)**: Create a new generic function and have the old interface call it (Deprecate old).
> *   **Option B (Overload)**: Use function overloading to support both (Complex).
> *   **Option C (Strict)**: Violate the constraint to make a truly clean generic API (Breaking Change).
>
> **NEXT STEP**: I recommend **Option A** to satisfy both constraints safely. Proceed?

## 3. High Risk / Destructive (High Risk) - v1.2.0 Format with Execution Plan
**User**: "Delete all users older than 1 year."
**Agent**:
> **[RISK: HIGH]** - Permanent data deletion.
>
> **CONTEXT AUDIT & SEARCH LOG**:
> *   **Verified**: [Database schema knowledge assumed]
> *   **Audit & Search Log** (Self-Rescue Attempts):
>     *   [Migration scripts]: Attempted `glob_file_search` with pattern "**/migrations/*.sql" → Not found
>     *   [Backup scripts]: Attempted `grep_search` with pattern "backup" → Not found
>     *   [Database config]: Not searched yet (need user guidance)
> *   **Must Access But Not Visible**: [Need to verify: database connection config, backup strategy, user table schema]
>
> **ALIGNMENT SNAPSHOT**:
> *   **Goal**: Prune old user records.
> *   **Technical Assumptions (Weight Count)**:
>     *   **Environment** (prod vs staging vs local) — **Weight: 2** → **IMMEDIATELY TRIGGER**
>     *   Backup strategy (1)
>     *   Delete method (soft vs hard) (1)
>     *   **Total Weight**: 4 (Environment weight=2 triggers immediately)
>
> **BLOCKING QUESTIONS**:
> *   Q1: Is this for **Production**? — **Environment assumption weight=2, MUST confirm**
> *   Q2: Do you want **Soft Delete** (`deleted_at` flag) or **Hard Delete** (SQL `DELETE`)?
> *   Q3: Do you have a **backup** or rollback strategy?
>
> **EXECUTION PLAN (Phase 1 - MANDATORY for HIGH risk)**:
> 
> **1. Rollback Preparation (MANDATORY "Rollback First" Principle)**:
> *   **Git Status**: Check current branch and uncommitted changes before proceeding
> *   **Backup Confirmation**: Verify database backup exists at `/backups/users_$(date +%Y%m%d).sql`
> *   **Rollback Script Location**: `scripts/rollback-delete-old-users.sql` (to be created)
> 
> **2. Files to Create/Modify**:
> | Path | Action | Risk |
> |------|--------|------|
> | `scripts/delete-old-users.sql` | Create | High |
> | `scripts/rollback-delete-old-users.sql` | Create | High |
> 
> **3. Dependencies**: None (SQL only)
> 
> **4. Breaking Changes**: Permanent data loss
> 
> **5. Rollback Strategy**: 
> *   If soft delete: UPDATE users SET deleted_at = NULL WHERE deleted_at = [timestamp]
> *   If hard delete: Requires backup restoration from `/backups/users_$(date +%Y%m%d).sql`
>
> **PROPOSED OPTIONS**:
> *   **Option A (Recommended)**: Generate a `SELECT` count query first to verify scope, then soft delete script.
> *   **Option B**: Generate a Soft Delete script with transaction wrapper.
> *   **Option C**: Generate Hard Delete script (Dangerous - requires explicit confirmation).
>
> **NEXT STEP**: Please confirm Q1, Q2, Q3, and review the Execution Plan above. I will NOT generate delete code until you confirm the plan.

## 4a. "Just Do It" Override (High Risk - Step 1) - v1.2.0 Format
**User**: "Yes, this is prod. Just do it, I don't care."
**Agent**:
> **[RISK: HIGH]** - User overrode safety check.
>
> **CONTEXT AUDIT & SEARCH LOG**:
> *   **Verified**: [Environment confirmed as Production]
> *   **Audit & Search Log** (Self-Rescue Attempts):
>     *   [Backup verification]: Attempted `grep_search` with pattern "backup" → Found references but need confirmation
>     *   [Rollback scripts]: Not searched yet (will create)
> *   **Must Access But Not Visible**: [Backup verification, rollback scripts]
>
> **ALIGNMENT SNAPSHOT**:
> *   **Goal**: Delete old users in Production.
>   **Technical Assumptions**: Environment confirmed (prod), but delete method and backup status still unknown.
>
> **FINAL SAFETY CHECK**: You confirmed **Production** and requested immediate execution.
> **⚠️ Context Warning**: This is a HIGH-risk operation. I am about to generate a script that **permanently removes data**. There is no undo.
>
> **EXECUTION PLAN CONFIRMATION REQUIRED**: Before generating code, please confirm:
> *   Delete method: Soft Delete (A) or Hard Delete (B)?
> *   Backup status: Do you have a recent backup?
>
> **Action**: I am pausing. Please reply with **"Yes, execute [A/B]"** and backup confirmation to generate the destructive script.

## 4b. "Just Do It" Override (High Risk - Step 2)
**User**: "Yes, execute."
**Agent**:
> **Executing Action**:
>
> ```sql
> -- PRODUCTION DELETION SCRIPT — wrapped in transaction for safety
> BEGIN;
> SELECT count(*) FROM users WHERE created_at < NOW() - INTERVAL '1 year';
> -- ↑ Verify count before proceeding
> DELETE FROM users WHERE created_at < NOW() - INTERVAL '1 year';
> -- COMMIT;   -- Uncomment after verifying the count above
> ROLLBACK;    -- Safety default: rollback until explicitly committed
> ```

## 5. Fast Track Example (Medium Risk with Explicit Scope) - v1.2.0 Format
**User**: "In `src/utils/auth.ts` line 42, change the JWT timeout from 30s to 60s. Skip Plan."
**Agent**:
> **[RISK: MEDIUM]** - Configuration change, but explicitly scoped.
>
> **CONTEXT AUDIT & SEARCH LOG**:
> *   **Verified**: [File path and line number specified]
> *   **Audit & Search Log** (Self-Rescue Attempts):
>     *   [`src/utils/auth.ts`]: Located via `glob_file_search` → Found and loaded
> *   **Must Access But Not Visible**: [None - all context available]
>
> **ALIGNMENT SNAPSHOT**:
> *   **Goal**: Update JWT timeout configuration.
>   **Technical Assumptions**: None (file path, line number, and change specified)
>   **Weight Count**: 0 (no assumptions needed)
>
> **FAST TRACK APPROVED**: Request is explicitly scoped with file path, line number, and clear change. Skipping Execution Plan per user request.
>
> ```typescript
> // [FAST-TRACKED MEDIUM RISK] - Explicitly scoped request, plan skipped per user request
> // Line 42: Updated JWT timeout from 30s to 60s
> const JWT_TIMEOUT = 60; // Changed from 30
> ```

## 6. Cross-File Coupling Weight Example with Kanban Table (v1.2.0)
**User**: "Refactor the authentication logic across the codebase."
**Agent**:
> **[RISK: MEDIUM]** - Refactoring with potential cross-file coupling.
>
> **CONTEXT AUDIT & SEARCH LOG**:
> *   **Verified**: [Current file in context]
> *   **Audit & Search Log** (Self-Rescue Attempts):
>     *   [auth.ts]: Attempted `grep_search` with pattern "auth" → Found 5 files
>     *   [user.model.ts]: Located via search → Found
>     *   [middleware/auth.ts]: Located via search → Found
>     *   [routes/auth.ts]: Located via search → Found
>     *   [config/auth.ts]: Located via search → Found
>   **Must Access But Not Visible**: [Need to load all 5 files for refactoring]
>
> **ALIGNMENT SNAPSHOT**:
> *   **Goal**: Refactor authentication logic.
>   **Technical Assumptions (Weight Count)**:
>     *   Framework/library choice (1)
>     *   File locations (1)
>     *   **Cross-File Coupling**: Modifying 5 files across different modules — **Weight: +2**
>     *   **Total Weight**: 4 (Cross-file coupling weight=2 triggers immediately)
>   **Impact Analysis**: 
>     *   **Scope**: Authentication module refactoring affects 5 files across models, middleware, routes, and config
>     *   **Affected Modules**: User authentication, session management, route protection
>     *   **Potential Side Effects**: Breaking changes to API endpoints, session handling, middleware chain
>
> **BLOCKING QUESTIONS**:
> *   Q1: Which files should be modified? (Found 5 auth-related files)
>     *   Q2: Should I maintain backward compatibility?
>
> **EXECUTION PLAN (Phase 1 - MANDATORY)**:
> 
> **1. Rollback Preparation**:
> *   **Git Status**: Check current branch (`main`) and create feature branch `refactor/auth-logic`
> *   **Backup**: Current implementation is in Git history (commit hash: `abc123`)
> *   **Rollback Strategy**: Git revert to `abc123` or merge rollback via feature branch
> 
> **2. Files to Modify (Kanban Table - 5 files > 3, MANDATORY)**:
> | Path | Action | Risk |
> |------|--------|------|
> | `src/auth.ts` | Edit | High |
> | `src/models/user.model.ts` | Edit | Medium |
> | `src/middleware/auth.ts` | Edit | High |
> | `src/routes/auth.ts` | Edit | Medium |
> | `src/config/auth.ts` | Edit | Medium |
> 
> **3. Dependencies**: None (refactoring only)
> 
> **4. Breaking Changes**: Potentially breaking if interfaces change (auth middleware signature, route handlers)
> 
> **5. Rollback Strategy**: Git revert to commit `abc123` or feature branch rollback
>
> **NEXT STEP**: Please review the Execution Plan and confirm which files to modify, or provide specific scope.

## 7. Low Risk (Proceed Immediately) - v1.2.0 Format
**User**: "Add a comment to explain this regex."
**Agent**:
> **[RISK: LOW]** - Documentation only.
>
> **CONTEXT AUDIT & SEARCH LOG**:
> *   **Verified**: [Regex pattern in current context]
> *   **Audit & Search Log**: [None - all context available, no search needed]
>
> I've added the explanation comment to the regex pattern.
>
> ```javascript
> // Matches email addresses (User + @ + Domain + . + TLD)
> const emailRegex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
> ```