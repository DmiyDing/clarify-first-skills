# Clarify First — Question Bank

> **Version**: 1.3.0  
> **Last Updated**: 2026-03-11  
> **Compatibility**: Matches clarify-first/SKILL.md v1.3.0 (includes Execution Plan, Amendment Boundary, and Pathfinder questions)

Use this toolkit to formulate **Blocking Questions**.
*   **Rule**: Pick only 1-3 questions that are *critical* for the next step.
*   **Style**: Prefer multiple-choice questions over open-ended ones to reduce user effort.
*   **User-Friendly Default**: Prefer plain wording that non-technical users can answer quickly.

## 0. Plain-Language Shortcuts
Use these when the user is speaking in broad or non-technical language.

*   "您更希望我先做哪一步？(A: **先查原因**, B: **先给方案**, C: **直接改**) "
*   "这次更重要的是哪件事？(A: **先恢复可用**, B: **先查清根因**, C: **顺手优化**) "
*   "范围只限当前问题，还是可以顺带调整相关模块？(A: **只处理当前问题**, B: **允许联动相关模块**) "
*   "这是线上影响用户的问题，还是本地开发中的问题？(A: **线上**, B: **测试/预发**, C: **本地开发**) "
*   "您说的‘优化’更偏向哪一类？(A: **更快**, B: **更稳定**, C: **更好看/更好用**) "
*   "如果现在信息还不够，您希望我怎么继续？(A: **先问清再改**, B: **先只读排查**, C: **先给执行方案**) "

## 1. Scope & Boundaries (What is In/Out?)
*   "Do you want this change applied to **only this file** or **all similar occurrences** in the repo?"
*   "Should I implement the **full feature** now, or just a **skeleton/MVP**?"
*   "Is the scope limited to **frontend only**, or should I also mock/implement the **backend API**?"

## 2. Acceptance Criteria (Definition of Done)
*   "How should I verify this? (A: **Unit Tests**, B: **Manual Screenshot**, C: **Console Output**)"
*   "What represents success? (A: **Performance metric** < 200ms, B: **Visual match** to design, C: **Functionality** works)"
*   "For the error handling, should I **fail silently**, **log it**, or **throw an exception**?"

## 3. Constraints (Tech Stack & Environment)
*   "Are there specific library constraints? (e.g., **Lodash vs Native**, **React vs Vanilla**)"
*   "What is the target Node.js/Python version? (A: **Latest**, B: **LTS**, C: **Specific: ______**)"
*   "Must I maintain **backward compatibility** with existing clients/APIs?"

## 4. Risk & Safety (Destructive Ops)
*   "This operation will **permanently delete** data. Do you have a **backup**?"
*   "Is this environment **Production**, **Staging**, or **Local**?"
*   "If the migration fails, do you need a **rollback script** prepared?"

## 5. Context & Reproduction
*   "Can you provide a **minimal reproduction code snippet** or specific input that causes the error?"
*   "What is the **expected output** versus the **actual output** you are seeing?"
*   "Are there any **related files** or dependencies I should look at first?"

## 6. Priority & Timeline
*   "Is this a **quick fix** or a **full redesign**? (A: **Quick patch**, B: **Proper refactor**, C: **Phased approach**)"
*   "Is there a **deadline** or release date driving this? (A: **Urgent/today**, B: **This sprint**, C: **No rush**)"
*   "Should I prioritize **speed of delivery** or **long-term maintainability**?"

## 7. Execution Plan & Architecture Evolution (v1.3.0)
*   "Before generating code, please review this **Execution Plan**. Which files should be created/modified? (A: **As listed**, B: **Modify: [list]**, C: **Skip Plan - Fast Track**)"
*   "After plan approval, should I lock a short **Plan Signature** (for example `Plan-ID: 7A2F`) for progressive execution tracking? (A: **Yes**, B: **No**) "
*   "This request is explicitly scoped (path + line/symbol + acceptance criteria). Should I apply **Fast Track** even though it uses words like 'fix' or 'improve'? (A: **Yes**, B: **No, keep plan**) "
*   "This change affects **multiple files** (>3). Should I proceed with the full refactor, or break it into phases? (A: **Full refactor**, B: **Phased approach**, C: **Single file first**)"
*   "This plan contains multiple dependent HIGH-risk actions. Should I execute progressively with confirmation after each step? (A: **Yes, step-by-step**, B: **No, pause and revise plan**) "
*   "For this **architecture evolution**, what is the **rollback strategy** if something goes wrong? (A: **Git revert**, B: **Feature flag**, C: **Database migration rollback script**)"
*   "The Execution Plan includes **breaking changes**. Are you prepared to handle **backward compatibility** issues? (A: **Yes, proceed**, B: **Add compatibility layer**, C: **Postpone breaking changes**)"
*   "This plan involves modifying **dependencies**. Should I update all at once or incrementally? (A: **All at once**, B: **Incremental**, C: **Test compatibility first**)"
*   "If I cannot run shell commands here, can you confirm your Git working tree status manually before I proceed? (A: **Clean**, B: **Has local changes**, C: **Unsure**) "
*   "During execution I discovered a new required file not in the approved plan. Should I open a **Plan Amendment** first? (A: **Yes, amend plan**, B: **No, stop execution**) "

## 8. Clarification Gate & Privacy
*   "I still have unresolved ambiguity after two rounds. Which option should I lock in before execution? (A: **Option A**, B: **Option B**, C: **Provide new constraints**) "
*   "The file appears to contain credentials/PII. Should I continue with redacted references only? (A: **Yes, redact all sensitive values**, B: **Stop and review security scope first**) "
*   "If you cannot provide the missing detail now, should I run a **read-only diagnostic** to discover it? (A: **Yes, run diagnostics**, B: **No, wait**) "

## 9. Shift-Left Manifest Check
*   "I found dependency manifests (`package.json`/`requirements.txt`/`go.mod`). Should I infer stack/deps from them before asking manual confirmation? (A: **Yes**, B: **No, ask me first**) "

## 10. Multi-Agent Handoff
*   "Should I emit a compact **Approved Payload** for downstream/sub-agent execution? (A: **Yes, output payload**, B: **No, keep human-readable only**) "
*   "For downstream specialization, should I add `scopeTag/intentVector/contextPointers` for scoped handoff? (A: **Yes, scoped payload**, B: **No, minimal payload**) "

## 11. Plan Amendment Boundary
*   "The newly discovered change appears to be **Derivative Adaptation** (type/interface/import sync). Should I batch these in one amendment for confirmation? (A: **Yes, batch amendment**, B: **No, one-by-one**) "
*   "This looks like **Logic Expansion** (new dependency/module). Should I hard-stop and re-plan before any further code? (A: **Yes, hard stop and amend**, B: **Cancel execution**) "

## 12. Pathfinder Sandbox Validation
*   "Read-only probing is insufficient. Should I run an isolated **sandbox validation** (temporary branch/worktree + minimal verification unit) to test assumption X/Y? (A: **Yes**, B: **No, wait for more context**) "

## 13. Skill Conflict Precedence
*   "Another active instruction requests silent auto-fix. Should I enforce clarify-first guardrail precedence and pause for confirmation? (A: **Yes, enforce guardrail**, B: **No, cancel task**) "

## 14. Contextual Risk Modifier
*   "This file appears central (`main.go`/`core.ts`/global contract). Should I escalate risk and require plan confirmation even for a small edit? (A: **Yes, escalate**, B: **No, keep current level**) "
*   "This task targets isolated `scripts/tmp` or test-only paths. Should I de-escalate one level under strict no-assumption conditions? (A: **Yes, de-escalate**, B: **No, keep conservative level**) "

## 15. Architectural Anti-Pattern Assertion
*   "Your constraints imply an unsafe pattern (for example client-side DB credentials). Should I block this approach and propose secure alternatives? (A: **Yes, block and propose**, B: **Cancel task**) "

## 16. Option Tradeoff Framing
*   "Choose implementation path with tradeoff labels: (A: **Faster delivery / higher dependency cost**, B: **Slower delivery / lower dependency risk**, C: **Balanced path**) "

## 17. Final Reconciliation
*   "Execution finished. Should I output a compact plan-vs-actual reconciliation report for audit? (A: **Yes, include report**, B: **No, skip report**) "

## 18. Chinese User-Friendly Defaults
Use these when the request is in Chinese and the user is not giving code-level constraints yet.

*   "这次改动，您希望我只改当前文件，还是把相关联的地方一起理顺？(A: **只改当前文件**, B: **相关地方一起改**) "
*   "您更在意什么结果？(A: **先能用**, B: **先稳定**, C: **先整洁/可维护**) "
*   "如果要我先确认一件事再继续，最关键的是哪项？(A: **改动范围**, B: **上线环境**, C: **验收标准**) "
*   "这一步做完后，您希望我怎么验证？(A: **我自测后给结果**, B: **先给您方案再执行**, C: **先做只读检查**) "
