# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
### Added
- **Official Eval Assets**: Added `clarify-first/evals/evals.json` and `benchmarks/trigger-evals/clarify-first.json` so the repository ships official-style skill test prompts and trigger benchmark prompts.
- **Benchmark Wrapper**: Added `tooling/run_trigger_benchmarks.py` and `npm run benchmark:trigger` for Anthropic-style trigger evaluation with the installed `skill-creator` scripts.
- **Description A/B Runner**: Added `tooling/run_trigger_ab.py`, `npm run benchmark:ab`, and `benchmarks/description-variants/clarify-first.json` for description-only benchmark comparison.
- **Portable Skill Validation Wrapper**: Added `tooling/validate_skill.py` so repository validation no longer depends on one machine-specific validator path.
- **CI Validation Workflow**: Added `.github/workflows/validate-skill.yml` to run version checks and skill validation on pushes and pull requests.
- **Benchmark Notes**: Added `benchmarks/README.md` to document runner settings, pass criteria, and the current benchmark baseline.
- **Documentation (third-round)**: Eval schema (`clarify-first/evals/README.md`), repository structure in README and README.zh-CN, official test/measure/refine blog link, and "Next phase: trigger quality" execution discipline in `benchmarks/README.md`.
- **Human-Friendly Confirmation Format**: Added a simpler default clarification layout emphasizing confirmed facts, missing inputs, options, and next step.
- **Readable Chinese Example Set**: Added user-friendly Chinese clarification examples for broad product requests, non-technical phrasing, and compact high-risk escalation.
- **Plain-Language Question Shortcuts**: Added simpler Chinese blocking-question patterns so the skill can ask answerable questions without protocol-heavy wording.
- **Language-Mirroring Eval Coverage**: Expanded `clarify-first/evals/evals.json` with Chinese non-technical and English compact-format expectations.
- **Compact Reply Guardrail**: The default clarification reply now explicitly forbids internal audit labels, protocol meta narration, and tables unless a detailed view is actually needed.
- **Non-Negotiable Clarification Gate**: If intent/scope/criteria remain unclear, the agent must stop immediately and ask blocking questions before any MEDIUM/HIGH-risk execution.
- **Progressive Execution Rule**: Multi-step plans with 2+ dependent HIGH-risk actions now require step-by-step execution with confirmation between steps.
- **Plan Signature Anchor**: Approved plans now include a short `Plan-ID` anchor for deterministic step tracking during progressive execution.
- **Strict Execution Boundary**: Phase 2 now blocks plan-external file changes and requires explicit Plan Amendment before expanding scope.
- **State Checkpoint Recall**: Before execution after long planning threads, the agent must restate `[Recalling Execution Plan Summary: ...]` to prevent context drift.
- **Security & Privacy Guardrail**: Added mandatory redaction rule for secrets, tokens, credentials, and PII in audits/snapshots (`***` masking).
- **No Bypass Clarification Policy**: Added explicit rule that "Skip triage/Don't ask" cannot bypass unresolved ambiguity checks or HIGH-risk confirmation gates.
- **Pathfinder Mode**: Added deadlock fallback to run safe read-only diagnostics or verification demos when users cannot answer blockers.
- **Trigger Attribution**: Risk output now supports explicit trigger source labeling (threshold/rule/assumption source).
- **Reasoning Model Awareness**: Added guidance for native reasoning models to run internal audit and output only structured results.
- **Shift-Left Manifest Validation**: Added mandatory manifest self-check before asking stack/dependency questions.
- **Structured Risk Header**: Standardized parse-friendly risk header format including `RISK`, `TRIGGER`, `CONFIDENCE`, and `PLAN-ID`.
- **Optional Handoff Payload**: Added machine-readable approved payload schema for multi-agent/sub-agent transfer.
- **Meta-Skill Conflict Precedence**: Added terminal guardrail precedence rule for ambiguity/high-risk conflicts with other execution-oriented skills.
- **Plan Amendment Boundary Classification**: Added explicit split between Derivative Adaptation and Logic Expansion before amendment decisions.
- **Sandbox Validation Pathfinder Option**: Added isolated validation probe path for deadlocks when read-only diagnostics are insufficient.
- **Scoped Handoff Payload**: Added optional `scopeTag`, `intentVector`, and `contextPointers` fields for context compression in downstream handoff.
- **Contextual Risk Modifier**: Added dynamic risk escalation/de-escalation guidance based on file centrality and isolation context.
- **Architectural Anti-Pattern Assertion**: Added hard-stop rule for requests violating foundational security/architecture constraints.
- **Confidence Calibration Matrix**: Added explicit confidence scoring rubric tied to verified facts vs unverified assumptions.
- **Final Reconciliation Phase**: Added post-execution plan-vs-actual audit output requirement for MEDIUM/HIGH tasks.

### Changed
- **Portable Validation & Benchmarking**: `npm run validate:skill` and `npm run benchmark:trigger` now discover Anthropic `skill-creator` via environment variables or common install locations instead of hardcoded local paths.
- **Benchmark Workflow Notes**: Added a first-pass A/B result note showing the current baseline (`5/11`) and that three aggressive description candidates did not improve recall.
- **Description Alignment**: Rewrote the skill frontmatter description in third-person style and added an explicit "when not to use" boundary for informational and explicitly scoped low-risk requests.
- **Benchmark Output Hygiene**: Benchmark summaries now write repository-relative paths, and benchmark result directories are ignored from source control.
- **Contribution Guide Consistency**: Updated README / README.zh-CN / CONTRIBUTING so versioning and validation instructions match the current frontmatter schema and portable validation flow.
- **SKILL Structure Tightening**: Reduced duplication in `clarify-first/SKILL.md`, moved detailed confirmation variants to references, and added a short "Common Edge Cases" section.
- **Eval & Benchmark Coverage**: Added machine-checkable eval metadata and expanded the trigger benchmark set for stronger regression coverage.
- **README Discoverability**: Added CI badge, validation wording, benchmark notes link, and one-line descriptions for each reference file.
- **Frontmatter Schema Compliance**: Removed unsupported `version` and `compatibility` keys from `clarify-first/SKILL.md` frontmatter to match the latest official validator rules.
- **Description Hardening**: Rewrote the skill description to fit the latest schema restrictions and to be more trigger-forward without unsupported angle brackets.
- **Chinese Guidance UX**: Updated `references/zh-CN.md` and `.cursorrules` so normal clarification output defaults to a compact, easier-to-read four-block structure.
- **Open-Source Validation Flow**: Updated README / README.zh-CN / CONTRIBUTING with official-style validation and benchmark commands.
- **Multi-Turn Protocol**: Replaced "ambiguous after 2 rounds -> auto-act" with hard confirmation gate for MEDIUM/HIGH-risk execution.
- **Fast Track Boundary**: Fast Track now requires zero unresolved ambiguity after audit, not just explicit scope markers.
- **Tone Guidance**: Added "Senior Pair Programmer" phrasing standard to keep strict protocol while reducing adversarial tone.
- **Output Modes**: Added optional `MODE=EXPERT` compact output mode while preserving all safety gates.
- **References & Examples**: Updated references for progressive execution, checkpoint recall, no-bypass behavior, and redaction language.
- **Validation Coverage**: Expanded validation rules for strict execution boundary, manifest validation, structured risk headers, handoff payloads, and adversarial prompts.
- **Cursor Rule Parity**: Aligned `.cursorrules` risk rubric with `SKILL.md` so "creating new files" is consistently MEDIUM risk.
- **Example Header Consistency**: Normalized legacy `[RISK: X]` examples to structured risk headers with `TRIGGER`, `CONFIDENCE`, and `PLAN-ID`.
- **Roadmap Wording**: Reframed roadmap headings to "Post-1.3.0" to avoid premature version signaling.
- **Reference Synchronization**: Synced scenarios/examples/question bank/Chinese phrasing with precedence, amendment boundary classification, sandbox validation, and scoped handoff payload semantics.
- **Decision Framing UX**: Updated option prompts to include concise `Speed/Cost/Safety` tradeoff annotations.
- **Open-Source Hygiene**: Replaced provider-specific conflict notes with a vendor-neutral conflict guide and removed machine-specific absolute path instructions from docs.
- **Validation Terminology**: Renamed provider-specific test labels to neutral hardening-set labels and added adversarial trigger cases (prompt injection, anti-pattern, destructive command variants).
- **README Onboarding Upgrade**: Reworked first impression, added feature matrix, and added frictionless onboarding paths for multiple client/runtime types.

### Removed
- **Non-Essential Open-Source Artifacts**: Removed `docs/` and `tooling/test-triggers.js` from public repository scope.

## [1.3.0] - 2026-02-26
### Added
- **Threshold Precision Rule**: Unified assumption trigger logic to `STOP if weighted total >= 3 OR any critical assumption has weight=2` (Environment/Dependencies/Cross-File Coupling).
- **Fast Track Priority Rule**: Added explicit override rule: precise scope (path + anchor + criteria) can still fast-track even when request contains vague verbs like "fix".
- **Language Mirroring**: Added explicit instruction to mirror user language for template headers while preserving structure.
- **Tool Availability Fallback**: HIGH-risk rollback preparation now includes fallback guidance when shell/terminal tools are unavailable (ask user to confirm Git working tree state).
- **Conditional Search Log**: `Audit & Search Log` is now conditional and should only be included when file search fails and blocks progress.

### Changed
- **Tool Name Agnosticism**: Replaced hardcoded tool names (`grep_search`, `glob_file_search`, `codebase_search`) with capability-based wording (regex/file/content search tools).
- **Execution Plan Terminology**: Renamed "Kanban-style Table" to **Impact Matrix Table (File Change Ledger)** for clearer semantics.
- **References Synchronization**: Updated examples, scenarios, and Chinese phrasing docs to match the new threshold, terminology, fallback, and fast-track priority rules.
- **Validation Script**: Updated `tooling/test-triggers.js` checks for Impact Matrix, tool-agnostic search naming, conditional search log, and fast-track priority logic.

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

## Future Considerations (Post-1.3.0)

Future roadmap items are tracked in project discussions and issue planning.
