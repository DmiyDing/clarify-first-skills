# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-02-12
### Added
- **Context & Confidence Audit**: Mandatory check for missing code context before acting.
- **Assumption Threshold**: Forced pause when more than 2 technical assumptions are made.
- **Enhanced Triage**: Elevated "Creating new files" and "Refactoring" to MEDIUM risk to prevent silent errors.
- **Context Loss Handling**: Added specific instructions for when the AI loses track of entities.
- **Trigger Examples Section**: Added 7 "should trigger" and 4 "should not trigger" scenarios to help agents recognize edge cases.
- **Default Stance**: Added "When in doubt, PAUSE and CLARIFY" to shift bias from "proceed" to "trigger".
- **Confidence Check**: Added quantifiable threshold (confidence < 80% → MUST trigger clarification).
- **Negative Constraint Check (P0)**: Added detection for when user says "don't do X" but implementation would require X. MUST trigger to resolve contradiction.
- **Assumption Weight Classification (P1)**: Introduced weighted system where Environment and Dependencies assumptions have weight=2 (immediately trigger), while Framework/Location/Naming have weight=1. If ANY assumption has weight=2, trigger immediately.
- **Missing Files Checklist (P1)**: Mandatory requirement to list all files/entities that must be accessed but are NOT currently visible in the conversation context during Alignment Snapshot.
- **Atomic Step Enforcement (P2)**: For MEDIUM/HIGH risk tasks, requires two-phase approach: Phase 1 (Execution Plan) must be confirmed before Phase 2 (Code Generation). Prevents premature code generation.
- **Context Erasure Warning (P2)**: Added explicit warning when conversation is very long (approaching context window limits) to remind user that earlier constraints may have been forgotten.
- **Search-First Self-Rescue (P1)**: Enhanced Context Audit to require AI to attempt self-rescue using `grep_search`, `glob_file_search`, or `codebase_search` before pausing to ask for file location. Reduces unnecessary interruptions.
- **Cross-File Coupling Weight (P2)**: Added weight classification for cross-file modifications. If modifying more than 3 files across different modules, add +2 to assumption weight (even without environment/deps assumptions). Covers complex refactoring scenarios.
- **Fast Track Mechanism (P2)**: Added exception for MEDIUM risk tasks with explicitly scoped requests (file paths, clear criteria, no ambiguous verbs). Allows skipping Execution Plan when user explicitly requests "Skip Plan" or "Fast Track", but requires `[FAST-TRACKED MEDIUM RISK]` header comment.
- **Kanban-Style Table Display (Gold Standard)**: For Execution Plans involving 3+ files, MANDATORY use of Markdown table format with columns: Path | Action (Edit/Create) | Risk. Provides clear visual overview of changes.
- **"Rollback First" Principle (Gold Standard)**: For HIGH risk Execution Plans, MANDATORY first item must be "Rollback Preparation" (Git status check, backup confirmation, rollback script location). Ensures safety-first approach.
- **Impact Analysis Dimension (Gold Standard)**: Added "Impact Analysis" section to Alignment Snapshot for MEDIUM/HIGH risk tasks, including: scope of impact, affected modules/components, potential side effects. Enhances professional expertise perception.
- **Quick Protocol (TL;DR) (Ultimate Polish)**: Added "Quick Protocol" section at the top of SKILL.md as "L1 Cache for AI Memory" - 3 core rules (Weight Classification, Two-Phase Execution, Search-First Self-Rescue) for instant recall in long contexts. Prevents "attention drift" in lengthy conversations.
- **Self-Rescue Log (Audit & Search Log) (Ultimate Polish)**: Enhanced Output Template with "Audit & Search Log" field, requiring AI to explicitly document all self-rescue attempts (grep_search, glob_file_search results). Increases transparency and trust by showing why AI paused.
- **Mandatory Version Declaration (Ultimate Polish)**: Upgraded `tooling/verify-version.js` to MANDATORY mode - all reference files MUST have version declaration matching main version. Ensures 100% knowledge base synchronization.
- **Confidence Score Terminology (zh-CN) (Ultimate Polish)**: Added "方案确信度评估 (Confidence Score)" section to zh-CN.md, including: current confidence percentage, threshold (80%), and confidence rationale. Helps users understand why AI paused.

### Changed
- **Trigger Logic**: Shifted from "risk-based" to "confidence-based" triggers.
- **Output Template**: Renamed `CONTEXT AUDIT` to `CONTEXT AUDIT & SEARCH LOG` with detailed "Audit & Search Log" field documenting all self-rescue attempts. Added `TECHNICAL ASSUMPTIONS` and `Impact Analysis` sections for transparency. Added `Must Access But Not Visible` field.
- **Description**: Enhanced with specific trigger keywords ('optimize', 'improve', 'fix', 'refactor', 'add feature', 'deploy', 'delete', 'migrate') to improve recognition.
- **Assumption Overload Definition**: Clarified with explicit categories (framework, file location, naming, dependencies, environment) and concrete example. Added weight classification system.
- **Context Audit**: Made MANDATORY with explicit "NEVER edit a file you haven't verified exists" rule.
- **Workflow Steps**: Added Step 3 (Atomic Step Enforcement) before Options proposal. Renumbered subsequent steps.
- **Chinese Documentation**: Enhanced `references/zh-CN.md` with architect-level terminology ("一致性确认" instead of "对齐", "关键阻塞点" instead of "阻碍性问题"). Added Execution Plan template with **变更影响面分析 (Impact Analysis)** dimension, Kanban table examples, and "回滚第一" principle. Added Context Erasure Warning examples.
- **Scenarios Reference**: Updated `references/SCENARIOS.md` with Assumption Weight Classification, Atomic Step Enforcement, and Negative Constraint Violation examples.
- **Test Script**: Enhanced `tooling/test-triggers.js` to validate all Gemini optimizations (11 checks total: 5 from first review, 3 from second review, 3 from gold standard polish).
- **Version Verification**: Enhanced `tooling/verify-version.js` to MANDATORY mode - all reference files MUST have version declaration matching main version. Fails build if any reference file lacks version declaration or has mismatched version. Ensures 100% knowledge base synchronization.
- **References Synchronization**: Updated all `references/` files to v1.2.0 standard:
  - **EXAMPLES.md**: Added Execution Plan examples with "Rollback First" principle, Context Audit & Search Log, Weight Classification examples, Fast Track example, Cross-File Coupling example with Kanban table. All HIGH risk examples strictly follow "Rollback Preparation" as first item.
  - **QUESTION_BANK.md**: Added Execution Plan & Architecture Evolution questions section.
  - **SCENARIOS.md**: Added version declaration header (was missing).
  - **NFR.md**: Added version declaration header (was missing).
  - **zh-CN.md**: Enhanced with "架构演进计划" (Architecture Evolution Plan) terminology, "变更风险评估" (Change Risk Assessment), "方案确信度评估" (Confidence Score), Fast Track Chinese phrasing, Audit & Search Log examples.
  - All reference files now include MANDATORY version declaration headers for automated verification.

## [1.1.0] - 2026-02-09
### Added
- **Multi-Turn Protocol**: Defined how to handle iterative clarification in `skill.md`.
- **Stop Heuristic**: added guidance on when to stop asking questions.
- **Question Bank**: Expanded `references/QUESTION_BANK.md` with concrete examples.
- **Scenarios**: Added high-risk scenarios (Deployment, Migration, Incident) to `references/SCENARIOS.md`.
- **NFRs**: Added Observability checklist to `references/NFR.md`.
- **Documentation**: Added `CONTRIBUTING.md` and `CHANGELOG.md`.

### Changed
- **Anti-Patterns**: Clarified "Just Do It" behavior for High vs Medium risk.
- **Project Structure**: Cleaned up `package.json` and `.gitignore`.
- **Chinese Docs**: Refactored `references/zh-CN.md` to reduce duplication.

## [1.0.0] - 2026-02-05
- Initial release.

---

## Future Considerations (v1.3.0+)

See `docs/FUTURE_OPTIMIZATIONS.md` for planned enhancements:
- **Adaptive Confidence Threshold**: Dynamic confidence threshold adjustment based on user behavior history (beginner: 90%, expert: 70%)
- Enhanced multilingual support
- Context memory improvements
- Collaboration features