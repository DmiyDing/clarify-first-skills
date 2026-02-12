# Clarify First — Scenarios

> **Version**: 1.2.0  
> **Last Updated**: 2026-02-12  
> **Compatibility**: Matches clarify-first/SKILL.md v1.2.0 (includes Assumption Weight Classification, Atomic Step Enforcement, Rollback First Principle)

## 1. Bug Reports
*   **Missing Repro**: User says "It crashes" but gives no logs/code. -> **Ask for logs.**
*   **Environment Mismatch**: User says "It works on my machine" but fails in CI. -> **Ask for diffs.**
*   **Vague Error**: "500 Error". -> **Ask for stack trace.**

## 2. Feature Requests (RFCs)
*   **XY Problem**: User asks for "A" (Solution) but really needs "B" (Problem Solved). -> **Clarify the underlying need.**
*   **Scope Creep**: Request grows vague ("also add auth"). -> **Ask to separate tasks.**
*   **Design Choice**: "Add a chart." -> **Ask: Bar? Line? Pie? Library?**

## 3. NFRs (Non-Functional Requirements)
*   **Performance**: "Make it fast." -> **Define "fast" (ms/RPS).**
*   **Scale**: "It needs to scale." -> **100 users or 1M users?**
*   **Security**: "Make it secure." -> **Auth? Encryption? Compliance?**

## 4. High-Risk Operations (Critical)
*   **Deployment**: "Deploy this to prod." -> **Clarify: Canary? Blue/Green? Downtime allowed?** (Environment assumption weight=2 → IMMEDIATELY TRIGGER)
*   **Data Migration**: "Migrate the schema." -> **Clarify: Backwards compat? Data loss acceptable during migration? Rollback plan?** (Requires Atomic Step Enforcement: Plan first, then code)
*   **Incident Response**: "System is down! Fix it!" -> **Time-pressure scenario. Bias toward read-only investigation first. Ask only 1 blocking question: Rollback to last known good, or fix forward? Then act.**
*   **Secrets**: "Update the API keys." -> **Clarify: Storage location? Rotation policy?** (Environment assumption weight=2 → IMMEDIATELY TRIGGER)
*   **Negative Constraint Violation**: User says "Don't modify the database" but the task requires DB changes. -> **MUST trigger to resolve contradiction.**

## 5. Assumption Weight Classification
*   **Weight = 2 (IMMEDIATELY TRIGGER)**:
    *   **Environment** (dev vs prod, local vs remote)
    *   **Dependencies** (which packages are available, which versions)
*   **Weight = 1 (Count normally)**:
    *   Framework/library choice
    *   File location/structure
    *   Naming conventions
*   **Rule**: If ANY assumption has weight=2, trigger immediately. Otherwise, if total count > 2, trigger.

## 6. Atomic Step Enforcement (MEDIUM/HIGH Risk)
For MEDIUM/HIGH risk tasks, follow two-phase approach:
1.   **Phase 1: Execution Plan** (MANDATORY)
    *   List files to create/modify
    *   List dependencies to add/update
    *   List breaking changes
    *   Provide rollback strategy
    *   **Wait for user confirmation** before proceeding
2.   **Phase 2: Code Generation** (Only after plan confirmation)
    *   Generate actual code
    *   If user modifies plan, regenerate plan (not code) and confirm again