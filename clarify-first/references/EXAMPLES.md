# Clarify First — Examples

> **Version**: 1.3.0  
> **Last Updated**: 2026-03-11  
> **Compatibility**: Matches clarify-first/SKILL.md v1.3.0 (includes non-negotiable clarification gate, progressive execution, plan-amendment boundary classification, anti-pattern hard stop, and final reconciliation)

## 1. Ambiguous Request (Medium Risk) - v1.3.0 Format
**User**: "Optimize the code."
**Agent**:
> **[RISK: MEDIUM | TRIGGER: ambiguity-goal | CONFIDENCE: 70% | PLAN-ID: pending]** - "Optimize" is subjective (speed vs. readability vs. memory).
>
> **CONTEXT AUDIT**:
> *   **Verified**: [Current file in context]
> *   **Manifest Check**: `package.json` found and reviewed (dependencies inferred before asking)
> *   **Must Access But Not Visible**: [Need to analyze codebase structure to identify optimization targets]
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
> *   **Option A (Recommended)**: Refactor for readability and strict typing. *(Tradeoff: Speed = Medium / Cost = Low / Safety = High)*
> *   **Option B**: Aggressive performance optimization. *(Tradeoff: Speed = High / Cost = Medium / Safety = Medium)*
>
> **NEXT STEP**: Please confirm Option A or clarify the goal. I will proceed only after your explicit confirmation.

## 2. Conflicting Constraints (Medium Risk) - v1.3.0 Format
**User**: "Refactor this to be generic, but don't change any interfaces."
**Agent**:
> **[RISK: MEDIUM | TRIGGER: constraint-conflict | CONFIDENCE: 74% | PLAN-ID: pending]** - Making code "generic" usually implies changing signatures (interfaces).
>
> **CONTEXT AUDIT**:
> *   **Verified**: [Current file in context]
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

## 3. High Risk / Destructive (High Risk) - v1.3.0 Format with Execution Plan
**User**: "Delete all users older than 1 year."
**Agent**:
> **[RISK: HIGH | TRIGGER: env-assumption+destructive-op | CONFIDENCE: 55% | PLAN-ID: pending]** - Critical assumption (Environment weight=2) + destructive operation.
>
> **CONTEXT AUDIT**:
> *   **Verified**: [Database schema knowledge assumed, config reviewed with secrets redacted: `DB_PASSWORD=***`]
> *   **Audit & Search Log** (Self-Rescue Attempts):
>     *   [Migration scripts]: Attempted [file search tool] with pattern "**/migrations/*.sql" → Not found
>     *   [Backup scripts]: Attempted [regex search tool] with pattern "backup" → Not found
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
> *   **Git Status**: If shell/terminal tools are available, check current branch and uncommitted changes; otherwise ask user to confirm working tree status
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
> *   **Option A (Recommended)**: Generate a `SELECT` count query first to verify scope, then soft delete script. *(Tradeoff: Speed = Medium / Cost = Low / Safety = High)*
> *   **Option B**: Generate a Soft Delete script with transaction wrapper. *(Tradeoff: Speed = Medium / Cost = Medium / Safety = High)*
> *   **Option C**: Generate Hard Delete script (Dangerous - requires explicit confirmation). *(Tradeoff: Speed = High / Cost = Low / Safety = Low)*
>
> **NEXT STEP**: Please confirm Q1, Q2, Q3, and review the Execution Plan above. I will NOT generate delete code until you confirm the plan.
> **Plan Signature (after approval)**: `Plan-ID: 7A2F`

## 4a. "Just Do It" Override (High Risk - Step 1) - v1.3.0 Format
**User**: "Yes, this is prod. Just do it, I don't care."
**Agent**:
> **[RISK: HIGH | TRIGGER: high-risk-override | CONFIDENCE: 68% | PLAN-ID: 7A2F]** - User attempted to bypass safety checks for a production operation.
>
> **CONTEXT AUDIT**:
> *   **Verified**: [Environment confirmed as Production]
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

## 4c. Progressive Execution for Dependent HIGH-Risk Actions (v1.3.0)
**User**: "Proceed with delete -> migrate -> deploy."
**Agent**:
> **[Recalling Execution Plan Summary: Delete stale users, run migration v42, deploy to production | Plan-ID: 7A2F]**
>
> **PROGRESSIVE EXECUTION ([Executing Step 1/3 of Plan 7A2F])**:
> I will execute only Step 1 now: generate and validate delete script (no deploy yet).
>
> **NEXT STEP**: Confirm "Proceed Step 1" to continue. After Step 1 result, I will pause for Step 2 confirmation.

## 4d. Plan Amendment Required for Out-of-Plan Discovery (v1.3.0)
**User**: "Proceed Step 2."
**Agent**:
> **[RISK: HIGH | TRIGGER: strict-execution-boundary | CONFIDENCE: 82% | PLAN-ID: 7A2F]** - New required file discovered outside approved Impact Matrix.
>
> **DISCOVERY**: Migration step requires editing `config/feature-flags.ts`, which is NOT in approved files for Plan `7A2F`.
>
> **ACTION**: Stopping execution and requesting **Plan Amendment** before continuing.
>
> **NEXT STEP**: Approve amendment to include `config/feature-flags.ts` (A: Approve, B: Reject, C: Revise plan).

## 4e. Plan Amendment Boundary Classification (v1.3.0)
**User**: "Continue execution."
**Agent**:
> **[RISK: MEDIUM | TRIGGER: plan-amendment-boundary | CONFIDENCE: 79% | PLAN-ID: 7A2F]** - New changes discovered; classified before amendment.
>
> **DISCOVERY CLASSIFICATION**:
> *   **Derivative Adaptation**: `src/types/auth.ts` (interface sync for compile pass)
> *   **Logic Expansion**: add dependency `zod` for new runtime validation
>
> **ACTION**:
> *   Derivative adaptation can be batched in one amendment request.
> *   Logic expansion requires hard-stop amendment approval before continuing.
>
> **NEXT STEP**: Choose (A) Approve both amendments, (B) Approve derivative only and stop, (C) Cancel and re-plan.

## 5. Fast Track Example (Medium Risk with Explicit Scope) - v1.3.0 Format
**User**: "Fix timeout bug in `src/utils/auth.ts` line 42: change the JWT timeout from 30s to 60s. Skip Plan."
**Agent**:
> **[RISK: MEDIUM | TRIGGER: explicit-scope-fast-track | CONFIDENCE: 92% | PLAN-ID: N/A]** - Configuration change, but explicitly scoped.
>
> **CONTEXT AUDIT**:
> *   **Verified**: [File path and line number specified]
> *   **Must Access But Not Visible**: [None - all context available]
>
> **ALIGNMENT SNAPSHOT**:
> *   **Goal**: Update JWT timeout configuration.
>   **Technical Assumptions**: None (file path, line number, and change specified)
>   **Weight Count**: 0 (no assumptions needed)
>
> **FAST TRACK APPROVED**: Explicit scope overrides vague verb ("fix"): request includes file path, line number, and clear change. Skipping Execution Plan per user request.
>
> ```typescript
> // [FAST-TRACKED MEDIUM RISK] - Explicitly scoped request, plan skipped per user request
> // Line 42: Updated JWT timeout from 30s to 60s
> const JWT_TIMEOUT = 60; // Changed from 30
> ```

## 6. Cross-File Coupling Weight Example with Impact Matrix Table (v1.3.0)
**User**: "Refactor the authentication logic across the codebase."
**Agent**:
> **[RISK: MEDIUM | TRIGGER: cross-file-coupling | CONFIDENCE: 72% | PLAN-ID: pending]** - Refactoring with potential cross-file coupling.
>
> **CONTEXT AUDIT**:
> *   **Verified**: [Current file in context]
> *   **Must Access But Not Visible**: [Need to load all 5 files for refactoring]
>
> **ALIGNMENT SNAPSHOT**:
> *   **Goal**: Refactor authentication logic.

## 7. Human-Friendly Chinese Confirmation (v1.3.0)
**User**: "帮我把这个页面优化一下。"
**Agent**:
> **[风险：中 | 触发：goal-ambiguity | 确信度：71% | 计划ID：pending]** - 我知道您要“优化”，但现在还不够确定要优化哪一部分。
>
> **我已确认**
> *   您希望把当前页面做得更好。
> *   您希望我先对齐，再开始改。
>
> **还需确认**
> *   您更在意哪一项：加载速度、页面样式，还是转化效果？
> *   范围是只改当前页面，还是允许联动相关组件？
>
> **可选方案**
> *   **方案 A（推荐）**：先确定目标和范围，再实施。取舍：多一次确认，但结果更稳。
> *   **方案 B**：我先做只读检查，给您一份问题清单。取舍：更快，但这一步不改代码。
>
> **下一步**：请回复：`A + 加载速度 + 只改当前页面`。

## 8. Non-Technical Chinese Request (v1.3.0)
**User**: "这个问题帮我弄好就行。"
**Agent**:
> **[风险：中 | 触发：goal-ambiguity | 确信度：69% | 计划ID：pending]** - “帮我弄好”这个目标还不够具体，我现在继续会靠猜。
>
> **我已确认**
> *   您希望把问题真正处理好。
> *   您不希望我跳过确认直接动手。
>
> **还需确认**
> *   您说的“弄好”，是指修复报错、优化体验，还是补一个缺失功能？
> *   这是线上正在影响用户的问题，还是本地开发中的问题？
>
> **可选方案**
> *   **方案 A（推荐）**：您先选目标，我按目标执行。取舍：方向更稳。
> *   **方案 B**：我先做只读排查，帮您缩小范围。取舍：更省心，但暂时不改代码。
>
> **下一步**：请回复：`A + 修复报错 + 线上问题`。
>   **Technical Assumptions (Weight Count)**:
>     *   Framework/library choice (1)
>     *   File locations (1)
>     *   **Cross-File Coupling**: Modifying 5 files across different modules — **Weight: 2 (critical)**
>     *   **Total Weight**: 4 (critical assumption exists, triggers immediately)
>   **Impact Analysis**: 
>     *   **Scope**: Authentication module refactoring affects 5 files across models, middleware, routes, and config
>     *   **Affected Modules**: User authentication, session management, route protection
>     *   **Potential Side Effects**: Breaking changes to API endpoints, session handling, middleware chain
>
> **BLOCKING QUESTIONS**:
> *   Q1: Which files should be modified? (Found 5 auth-related files)
> *   Q2: Should I maintain backward compatibility?
>
> **EXECUTION PLAN (Phase 1 - MANDATORY)**:
> 
> **1. Rollback Preparation**:
> *   **Git Status**: Check current branch (`main`) and create feature branch `refactor/auth-logic`
> *   **Backup**: Current implementation is in Git history (commit hash: `abc123`)
> *   **Rollback Strategy**: Git revert to `abc123` or merge rollback via feature branch
> 
> **2. Files to Modify (Impact Matrix Table / File Change Ledger - 5 files > 3, MANDATORY)**:
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

## 7. Low Risk (Proceed Immediately) - v1.3.0 Format
**User**: "Add a comment to explain this regex."
**Agent**:
> **[RISK: LOW | TRIGGER: low-risk-readability | CONFIDENCE: 98% | PLAN-ID: N/A]** - Documentation only.
>
> **CONTEXT AUDIT**:
> *   **Verified**: [Regex pattern in current context]
>
> I've added the explanation comment to the regex pattern.
>
> ```javascript
> // Matches email addresses (User + @ + Domain + . + TLD)
> const emailRegex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
> ```

## 8. Approved Payload for Multi-Agent Handoff (v1.3.0)
**Agent**:
> **APPROVED PAYLOAD**:
> ```json
> {
>   "planId": "7A2F",
>   "risk": "HIGH",
>   "trigger": "env-assumption+destructive-op",
>   "scopeTag": "database-maintenance",
>   "intentVector": ["delete-stale-users", "preserve-rollback-path"],
>   "contextPointers": ["scripts/delete-old-users.sql", "scripts/rollback-delete-old-users.sql"],
>   "approvedFiles": ["scripts/delete-old-users.sql", "scripts/rollback-delete-old-users.sql"],
>   "rollbackStrategy": "backup restore from /backups/users_YYYYMMDD.sql",
>   "nextStep": "Execute Step 2/3 after explicit confirmation"
> }
> ```

## 9. Pathfinder Sandbox Validation (v1.3.0)
**User**: "I can't answer which allocator variant to use."
**Agent**:
> **[RISK: MEDIUM | TRIGGER: deadlock-context-gap | CONFIDENCE: 61% | PLAN-ID: pending]** - Blocked by unresolved implementation fact.
>
> **PATHFINDER OPTIONS**:
> *   **Option A (Read-only)**: continue static inspection only.
> *   **Option B (Sandbox Validation)**: run isolated validation in temp branch/worktree with minimal verification unit to test assumption A vs B.
>
> **GUARDRAIL**:
> *   No deploy/publish
> *   No production mutation
> *   Report validation result first, then request implementation confirmation
>
> **NEXT STEP**: Reply (A) or (B). I will proceed only after your explicit confirmation.

## 10. Architectural Anti-Pattern Hard Stop (v1.3.0)
**User**: "Keep it frontend-only, but connect directly to Postgres with real credentials."
**Agent**:
> **[RISK: HIGH | TRIGGER: architectural-anti-pattern | CONFIDENCE: 96% | PLAN-ID: pending]** - Requested approach violates security architecture (client-side credential exposure).
>
> **ASSERTION**:
> *   Refusing direct client-side DB credential pattern.
> *   This is a hard stop due to security baseline violation.
>
> **SAFE OPTIONS**:
> *   **Option A (Recommended)**: Add backend API proxy with server-side secrets. *(Tradeoff: Speed = Medium / Cost = Medium / Safety = High)*
> *   **Option B**: Add serverless function as thin DB gateway. *(Tradeoff: Speed = High / Cost = Medium / Safety = High)*
>
> **NEXT STEP**: Choose A or B. I will not implement client-side direct DB credentials.

## 11. Final Reconciliation Output (v1.3.0)
**Agent**:
> **FINAL RECONCILIATION**:
> *   **Plan-ID**: `7A2F`
> *   **Approved vs Actual Files**: `2` vs `2`
> *   **Plan Amendment Triggered**: No
> *   **Rollback Status**: Valid
