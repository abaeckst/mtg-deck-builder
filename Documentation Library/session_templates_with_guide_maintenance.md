# Development Session Templates

**Purpose:** Optimized workflow templates for efficient development sessions with Code Organization Guide integration and maintenance  
**Usage:** Choose appropriate template based on type of work, leverage Code Organization Guide for instant file identification, maintain guide accuracy  
**Last Updated:** June 7, 2025 (Enhanced with Code Organization Guide maintenance framework)  

## 🚀 Session Startup Checklist

### Every Session Begins With:
```markdown
## Session Setup (5 minutes)
- [ ] Open VS Code to project folder: `C:\Users\carol\mtg-deck-builder`
- [ ] Run `npm start` to verify project compiles and loads correctly
- [ ] Check GitHub sync status: `git status`
- [ ] Review project_status.md for current state
- [ ] **USE CODE ORGANIZATION GUIDE** for instant file identification (major workflow enhancement)
- [ ] Check for previous session logs on related work for context
- [ ] Confirm session goal and success criteria
- [ ] **SMART IMPACT ANALYSIS** (2-3 minutes)
- [ ] Create new session log: session_log_YYYY-MM-DD_session[N]_[description].md
```

## 🎯 Smart Impact Analysis Protocol

### Pre-Session Analysis (2-3 minutes) - Enhanced with Code Organization Guide
```markdown
## Smart Integration Analysis
**Feature/System being modified:** [Use Code Organization Guide to identify relevant files]
**Files identified from Code Organization Guide:**
- [ ] Primary files: [Files that will definitely be modified]
- [ ] Integration files: [Files that connect with primary files]
- [ ] Type/utility files: [Supporting files that might be affected]

**Systems being modified this session:**
- [ ] Hooks: [List specific hooks that will be changed]
- [ ] State: [What state objects/properties will change]  
- [ ] Components: [Which components will be modified]

**Features that use these systems:** [Reference Code Organization Guide integration points]
- [ ] Direct users: [Features that directly use modified code]
- [ ] Indirect users: [Features that share state/hooks with modified systems]

**Risk Assessment:**
- **HIGH RISK:** [Features with complex state/subscription dependencies on modified systems]
- **MEDIUM RISK:** [Features that use modified hooks but simpler integration]
- **LOW RISK:** [Independent features - will SKIP testing these]

**Smart Test Plan (5 minutes max):**
- **HIGH RISK (Must test):** [1-3 features max that MUST be verified]
- **MEDIUM RISK (Quick check):** [1-2 features for basic verification]
- **SKIP:** [List what we're consciously NOT testing - low risk features]
```

### Smart Testing Heuristics (Proven Effective)
```markdown
## High Risk Indicators (Always Test)
- Features using the same hooks you're modifying
- Features with complex state management (subscriptions, events)
- Features that have broken before from similar changes
- Features sharing data objects with your changes
- Features that integrate with modified architecture

## Medium Risk Indicators (Quick Verification)
- Features using modified components but simpler integration
- Features that might be affected by UI changes
- Features with some dependency on modified systems

## Low Risk Indicators (SKIP Testing)
- Features that are completely independent
- Features using different hooks/state entirely
- Features never affected by similar changes
- Features with no shared dependencies
```

## 🔧 Code Organization Guide Maintenance Protocol

### During Sessions - Monitor Guide Accuracy:
```markdown
## Code Organization Guide Validation (Ongoing)
- [ ] **Guide Accuracy Check:** Does reality match guide predictions for files and integration points?
- [ ] **Missing Information:** Any integration points or patterns not documented in guide?
- [ ] **File Health Changes:** Any files crossing size/complexity thresholds during session?
- [ ] **New Patterns:** Any development approaches that could enhance guide recommendations?
- [ ] **Risk Assessment Accuracy:** Did guide risk predictions match actual testing needs?
```

### Maintenance Triggers - When Guide Updates Are Needed:

#### **MAJOR UPDATES (Required):**
- New files added (components, hooks, services) to core architecture
- Files deleted or significantly refactored during session
- Architecture patterns change (new integration approaches discovered)
- File health status changes (size, complexity, responsibilities crossing thresholds)
- New development patterns established that should be documented

#### **MINOR UPDATES (Recommended):**
- Integration points discovered that weren't documented in guide
- Risk assessment accuracy issues found during testing
- Development patterns refined through usage
- Method signatures or dependency flows changed

#### **VALIDATION UPDATES (Periodic):**
- Guide accuracy verification after major development phases
- Integration point validation after refactoring sessions
- Health status review after multiple development sessions

### Update Process Framework:
```markdown
## Code Organization Guide Update Process
1. **Session Documentation:** Note all guide-related findings in session log
2. **Reconciliation Assessment:** Evaluate if updates needed during reconciliation
3. **Update Categorization:**
   - **Minor Updates:** Incorporate immediately during reconciliation
   - **Major Updates:** Plan separate "Code Organization Guide Maintenance" session
   - **Validation Updates:** Schedule periodic review sessions
4. **Update Execution:** User signals "update Code Organization Guide" when ready
5. **Validation:** User reviews and validates updated guide before deployment
```

## 📋 Template Types Available

1. **Enhancement Development** - Adding new features or capabilities (Code Organization Guide accelerated)
2. **Issue Resolution** - Fixing bugs or improving user experience (Code Organization Guide guided)
3. **Documentation Reconciliation** - Converting session logs to permanent documentation
4. **Architecture Maintenance** - Following refactoring roadmap from Code Organization Guide
5. **Code Organization Guide Maintenance** - Updating guide based on accumulated findings (NEW)

---

## 📋 Template 1: Enhancement Development Session (Code Organization Guide Enhanced)

### Session Goal Template:
```markdown
# Session Goal: [Enhancement Name] - [Brief Description]

## Pre-Session File Identification (ENHANCED WORKFLOW)
**CODE ORGANIZATION GUIDE REFERENCE:**
- [ ] Use "Quick Reference Decision Tree" for instant file identification
- [ ] Reference relevant development pattern: [Search/Filter/Card Display/View Mode/etc.]
- [ ] Review integration points for identified files
- [ ] **Check guide accuracy:** Do file descriptions match current reality?

**Files identified from Code Organization Guide:**
- [ ] Primary files: [Files that will definitely need modification]
- [ ] Integration files: [Files with documented dependencies]
- [ ] Type/utility files: [Supporting files that might be affected]
- [ ] Related completion documents: [If building on previous work]

## Smart Impact Analysis (2-3 minutes) - Code Organization Guide Informed
**Systems being modified:** [Based on Code Organization Guide analysis]
- Hooks: [List specific hooks from guide]
- State: [State objects/properties changing]
- Components: [Components being modified]

**Risk Assessment & Test Plan:** [Reference Code Organization Guide integration points]
- **HIGH RISK (Must test):** [1-3 features with complex dependencies per guide]
- **MEDIUM RISK (Quick check):** [1-2 features with simpler integration per guide]
- **SKIP:** [Independent features identified in guide we won't test]

## Enhancement Implementation Goals
1. **[Primary Goal]** - [Description]
2. **[Secondary Goal]** - [Description]
3. **[Integration Goal]** - [Description per Code Organization Guide patterns]

## Implementation Plan (Accelerated with Code Organization Guide)
1. **Information Analysis** (REDUCED TIME: 5-15 min)
   - Review Code Organization Guide for relevant files and integration points
   - **Validate guide accuracy** against current implementation
   - Confirm current implementation details for integration
   - Map out enhancement requirements using documented patterns
   
2. **Core Implementation** (60-180 min)
   - [Implementation step 1 - following documented patterns]
   - [Implementation step 2 - using established integration points]
   - [Implementation step 3 - applying architecture guidelines]
   - **Monitor guide accuracy** during implementation
   - **Document progress in session log throughout**
   
3. **Integration & Testing** (30-60 min)
   - Integrate using documented integration points and method signatures
   - Test enhancement functionality thoroughly
   - **SMART REGRESSION TESTING (5 minutes max)**
   - **Validate guide risk assessment accuracy**
   
4. **Session Documentation** (10-20 min - REDUCED with better context)
   - Complete comprehensive session log referencing Code Organization Guide usage
   - **Document Code Organization Guide accuracy and any discrepancies found**
   - Document any discoveries not covered in the guide
   - Note current status and next steps for potential continuation
   - **DO NOT update core project docs - use session log only**

## Session Success Criteria
- [ ] [Primary functionality working as designed]
- [ ] [Integration following documented patterns from Code Organization Guide]
- [ ] **[HIGH RISK features verified working - no regressions]**
- [ ] [TypeScript compilation succeeds with no errors]
- [ ] [Professional appearance matching existing standards]
- [ ] [Session log created documenting Code Organization Guide usage and accuracy]
- [ ] **[Code Organization Guide maintenance needs identified and documented]**

## Files Expected to be Modified/Created (Pre-identified)
- [List from Code Organization Guide analysis]

## Session Log Focus Areas
- **Code Organization Guide Usage:** How the guide accelerated development and file identification
- **Code Organization Guide Accuracy:** Any discrepancies between guide and reality
- **Smart Testing Results:** What HIGH/MEDIUM risk features were tested and results
- **Integration Success:** How documented patterns worked for new feature integration
- **New Discoveries:** Any insights not covered in the existing guide
- **Guide Enhancement Opportunities:** Specific improvements needed for guide
- **Next Session Preparation:** Context needed if work continues across sessions
```

---

## 📋 Template 2: Issue Resolution Session (Code Organization Guide Guided)

### Session Goal Template:
```markdown
# Session Goal: Fix [Specific Issue Description]

## Issue Analysis with Code Organization Guide
- **Bug Description:** [Exact issue and reproduction steps]
- **Impact:** [What functionality is affected]
- **Error Messages:** [Any console/TypeScript errors]
- **Code Organization Guide Analysis:** [Which files likely contain the issue]
- **Previous Debugging:** [Check session logs for prior attempts]

## Pre-Session File Identification (ENHANCED WORKFLOW)
**CODE ORGANIZATION GUIDE REFERENCE:**
- [ ] Use file matrix to identify files related to bug area
- [ ] Review integration points that might be affected
- [ ] Check health status of identified files in guide
- [ ] Reference similar issue patterns from guide
- [ ] **Validate guide accuracy:** Do descriptions match current file state?

**Files identified from Code Organization Guide:**
- [ ] Bug area files: [Files most likely containing the issue]
- [ ] Integration files: [Files that connect with bug area]
- [ ] Related dependencies: [Files that might be indirectly affected]
- [ ] Previous session logs: [If this is ongoing debugging]

## Smart Impact Analysis (2-3 minutes) - Code Organization Guide Informed
**Systems being debugged/modified:** [Based on guide analysis]
- Bug Area: [Components/hooks with the issue]
- Likely Changes: [What will probably need to be fixed]

**Risk Assessment & Test Plan:** [Reference guide integration points]
- **HIGH RISK (Must test):** [Features that share code with bug area per guide]
- **MEDIUM RISK (Quick check):** [Features that might be affected by fix per guide]
- **SKIP:** [Unrelated features identified in guide we won't test]

## Debugging Plan (Accelerated with Code Organization Guide)
1. **Issue Reproduction & Context Review** (REDUCED TIME: 5-20 min)
   - Use Code Organization Guide to quickly identify relevant files
   - **Validate guide predictions** against actual file contents and structure
   - Review any previous session logs for debugging context
   - Confirm exact reproduction steps and root cause area
   - Check TypeScript errors and browser console
   
2. **Fix Implementation** (30-90 min)
   - Address root cause using documented integration patterns
   - **Monitor guide accuracy** during debugging and implementation
   - Test fix in isolation first using guide recommendations
   - Verify fix doesn't create new issues in dependent areas
   - **Document all debugging steps in session log**
   
3. **Regression Testing** (5-10 min max)
   - **SMART REGRESSION TESTING:** Test only HIGH RISK features per guide analysis
   - Quick verification of MEDIUM RISK features identified in guide
   - **Validate guide risk assessment accuracy**
   - **Time-boxed:** If testing takes >5 minutes, note as "needs investigation"

4. **Session Documentation** (10-15 min - REDUCED with better context)
   - Complete detailed session log with debugging journey
   - **Document Code Organization Guide usage effectiveness and accuracy**
   - Note verification steps taken and resolution approach
   - **Document any guide discrepancies or enhancement opportunities**
   - **DO NOT update core project docs - use session log only**

## Session Success Criteria
- [ ] Original issue completely resolved
- [ ] **No regressions in HIGH RISK features identified by guide**
- [ ] Clean TypeScript compilation
- [ ] Professional user experience maintained
- [ ] Session log documenting Code Organization Guide effectiveness for debugging
- [ ] **Code Organization Guide accuracy validated and maintenance needs documented**

## Files Expected to be Modified (Pre-identified)
- [List from Code Organization Guide analysis]

## Session Log Focus Areas
- **Code Organization Guide Effectiveness:** How the guide accelerated issue identification
- **Code Organization Guide Accuracy:** How well guide predictions matched debugging reality
- **Smart Testing Results:** HIGH/MEDIUM risk features tested per guide and results
- **Debugging Journey:** Every approach tried, guided by file organization knowledge
- **Resolution Details:** Exact changes made using documented patterns
- **Guide Enhancement Opportunities:** Any insights that could improve the guide accuracy or coverage
```

---

## 📋 Template 3: Documentation Reconciliation Session

### Session Goal Template:
```markdown
# Session Goal: Reconcile Session Logs and Update Core Documentation

## Reconciliation Scope
- **Session Logs to Process:** [List all session logs from recent work]
- **Features Completed:** [Features that are finished and need completion docs]
- **Core Docs to Update:** [Which permanent documents need updates]
- **Code Organization Guide Updates:** [Any architecture changes affecting the guide]

## Pre-Reconciliation Review
**MANDATORY FIRST STEP - Review these materials:**
- [ ] All session logs in chronological order
- [ ] Current project_status.md for baseline
- [ ] Documentation_catalog.md for archive structure
- [ ] Code Organization Guide for any needed updates
- [ ] **Code Organization Guide maintenance findings** from session logs
- [ ] [Any additional context needed]

## Code Organization Guide Maintenance Assessment
**Review accumulated maintenance needs:**
- [ ] **Guide Accuracy Issues:** Any discrepancies found during sessions
- [ ] **Missing Information:** Integration points or patterns not documented
- [ ] **File Health Changes:** Files crossing size/complexity thresholds
- [ ] **New Patterns:** Development approaches that should be documented
- [ ] **Architecture Changes:** New files, deleted files, refactored structure

**Maintenance Decision:**
- [ ] **No Updates Needed:** Guide remains accurate
- [ ] **Minor Updates:** Incorporate during this reconciliation
- [ ] **Major Updates:** Schedule separate Code Organization Guide Maintenance session

## Reconciliation Plan
1. **Session Log Analysis** (20-40 min)
   - Review all session logs chronologically
   - Identify completed features vs work-in-progress
   - Extract key technical discoveries and integration patterns
   - **Compile Code Organization Guide maintenance findings**
   
2. **Code Organization Guide Maintenance** (0-30 min - if minor updates needed)
   - Address guide accuracy issues found during sessions
   - Update file health status if changed
   - Add missing integration points or patterns discovered
   - **Skip if major updates needed - schedule separate session**
   
3. **Completion Document Creation** (30-90 min)
   - Create completion documents for finished features
   - Include technical details, integration points, architecture insights
   - Document implementation approach and final decisions
   - Preserve key debugging insights and methodology
   - **Include smart testing results and regression prevention learnings**
   - **Document Code Organization Guide usage effectiveness**
   
4. **Core Documentation Updates** (20-40 min)
   - Update project_status.md with new capabilities
   - Update documentation_catalog.md with new archived materials
   - Update Code Organization Guide if minor changes were made
   - Archive planning documents that are now obsolete
   - Ensure single source of truth for current state
   
5. **Session Log Cleanup** (10 min)
   - Delete session logs after information is incorporated
   - Verify all important context preserved in permanent docs
   - Confirm clean project knowledge state

## Reconciliation Success Criteria
- [ ] All completed features have comprehensive completion documents
- [ ] Project status accurately reflects current capabilities including any architecture changes
- [ ] Documentation catalog updated with new archives
- [ ] **Code Organization Guide maintenance needs addressed or scheduled**
- [ ] Planning documents for finished work moved to archive
- [ ] Session logs deleted after successful incorporation
- [ ] Clean project knowledge focused on current state and future options
- [ ] **Code Organization Guide accuracy maintained for optimal workflow efficiency**

## Expected Outputs
- **Completion Documents:** [List expected completion docs to be created]
- **Updated Core Docs:** [List permanent documents to be updated]
- **Archived Materials:** [List planning docs to be archived]
- **Code Organization Guide Updates:** [Minor updates completed or major updates scheduled]
```

---

## 📋 Template 4: Architecture Maintenance Session (Code Organization Guide Roadmap)

### Session Goal Template:
```markdown
# Session Goal: [Architecture Maintenance Task]

## Architecture Goals (Following Code Organization Guide Roadmap)
- **Primary Objective:** [Specific refactoring task from guide roadmap]
- **Verification Objective:** [How to confirm refactoring success]
- **Quality Objective:** [Ensure no regressions during maintenance]

## Pre-Session Planning (Code Organization Guide Informed)
**MANDATORY FIRST STEP - Reference established roadmap:**
- [ ] Review Code Organization Guide refactoring roadmap for specific task
- [ ] Check refactoring priorities and established recommendations
- [ ] Identify files marked for refactoring in guide health assessment
- [ ] Review excellent pattern examples to follow

**Code Organization Guide Analysis:**
- [ ] Current file health status for refactoring target
- [ ] Recommended extraction patterns from guide
- [ ] Integration points that will be affected
- [ ] Success patterns to emulate from guide examples

## Refactoring Plan (Following Established Guidelines)
1. **Current State Assessment** (10-20 min)
   - Review Code Organization Guide assessment of target files
   - **Validate guide accuracy** against current file state
   - Confirm current architecture matches guide documentation
   - Plan refactoring approach following guide recommendations
   
2. **Architecture Refactoring** (60-180 min)
   - Follow specific extraction patterns documented in guide
   - Apply established architecture guidelines and patterns
   - Maintain integration points documented in guide
   - **Monitor how refactoring affects guide accuracy**
   - **Document refactoring process in session log**
   
3. **Verification & Testing** (30-45 min)
   - Test refactored architecture maintains all functionality
   - Verify integration points work as documented
   - **SMART REGRESSION TESTING following guide risk assessment**
   - **Validate guide predictions about refactoring impact**
   
4. **Session Documentation** (15-20 min)
   - Complete session log with refactoring details
   - Document refactoring success and any discovered improvements
   - **Note extensive Code Organization Guide updates needed**
   - **Plan major guide update for new architecture**

## Session Success Criteria
- [ ] Refactoring completed following Code Organization Guide recommendations
- [ ] All integration points maintained as documented
- [ ] **No regressions in features identified as HIGH RISK in guide**
- [ ] TypeScript compilation clean with improved architecture
- [ ] **Major Code Organization Guide update needs documented for separate session**
- [ ] Session log documenting refactoring success and guide update requirements

## Architecture Files to be Refactored
- [List from Code Organization Guide refactoring roadmap]

## Code Organization Guide Impact Assessment
- [ ] **New Files Created:** [List files that will need guide documentation]
- [ ] **Files Modified:** [List files with changed health status or responsibilities]
- [ ] **Integration Changes:** [New or modified integration points]
- [ ] **Pattern Updates:** [New development patterns established]
- [ ] **Health Status Changes:** [Files crossing size/complexity thresholds]
```

---

## 📋 Template 5: Code Organization Guide Maintenance Session (NEW)

### Session Goal Template:
```markdown
# Session Goal: Update Code Organization Guide Based on Accumulated Findings

## Maintenance Scope Assessment
**Accumulated maintenance needs from recent sessions:**
- [ ] **Guide Accuracy Issues:** [List discrepancies found during development]
- [ ] **Missing Information:** [Integration points or patterns not documented]
- [ ] **File Health Changes:** [Files crossing size/complexity thresholds]
- [ ] **New Architecture Elements:** [New files, deleted files, refactored structure]
- [ ] **Pattern Updates:** [New development approaches discovered]
- [ ] **Risk Assessment Improvements:** [Testing accuracy issues found]

## Pre-Maintenance Review
**MANDATORY FIRST STEP - Compile maintenance context:**
- [ ] Review recent session logs for Code Organization Guide findings
- [ ] Check current guide against actual file system state
- [ ] Validate integration points against current implementation
- [ ] Assess file health status accuracy
- [ ] Review development pattern effectiveness

## Maintenance Categories
**Categorize needed updates:**
- [ ] **File Matrix Updates:** New files, deleted files, health status changes
- [ ] **Integration Point Updates:** New or changed method signatures and dependencies
- [ ] **Development Pattern Updates:** New patterns or refined approaches
- [ ] **Risk Assessment Updates:** Improved accuracy based on testing results
- [ ] **Quick Reference Updates:** Decision tree improvements or additions

## Guide Update Plan
1. **Current State Validation** (20-30 min)
   - Compare guide against actual file system
   - Validate integration points against implementation
   - Check file health assessments for accuracy
   - Review development patterns for current effectiveness
   
2. **Guide Content Updates** (60-120 min)
   - Update file matrix with new/changed files
   - Correct integration point documentation
   - Add new development patterns discovered
   - Improve risk assessment accuracy
   - Enhance quick reference decision tree
   - Update refactoring roadmap based on changes
   
3. **Quality Assurance** (20-30 min)
   - Review updated guide for internal consistency
   - Validate new content against recent session experiences
   - Ensure integration point accuracy
   - Check development pattern completeness
   
4. **Documentation** (10-15 min)
   - Document changes made to guide
   - Note validation results
   - Update guide version/timestamp
   - Create change summary for user review

## Maintenance Success Criteria
- [ ] All identified accuracy issues resolved
- [ ] New architecture elements properly documented
- [ ] Integration points validated against implementation
- [ ] Development patterns reflect current best practices
- [ ] Risk assessment accuracy improved based on testing experience
- [ ] Guide internal consistency maintained
- [ ] Change summary created for user validation

## Guide Update Areas
- [ ] **File Organization Matrix:** [Files needing updates]
- [ ] **Integration Point Reference:** [Dependencies needing correction]
- [ ] **Development Decision Tree:** [Patterns needing addition/refinement]
- [ ] **Refactoring Roadmap:** [Priorities needing adjustment]
- [ ] **Architecture Health Assessment:** [Status changes needing documentation]

## Validation Requirements
- [ ] **User Review Required:** [Significant changes needing validation]
- [ ] **Testing Needed:** [Guide accuracy requiring verification in next session]
- [ ] **Pattern Validation:** [New approaches needing real-world testing]
```

---

## 🎯 Session Completion Checklist

### End-of-Session Protocol (Every Session):
```markdown
## Session Wrap-Up (10-15 minutes)
- [ ] All new code compiles without TypeScript errors
- [ ] Run `npm start` - application loads and all features work
- [ ] **SMART REGRESSION TESTING (5 minutes max):**
  - [ ] Test HIGH RISK features identified in pre-session analysis using Code Organization Guide
  - [ ] Quick verification of MEDIUM RISK features per guide integration points
  - [ ] **Validate guide risk assessment accuracy**
  - [ ] Log any issues found (don't debug during wrap-up)
- [ ] Complete comprehensive session log with:
  - [ ] Code Organization Guide usage effectiveness and workflow acceleration
  - [ ] **Code Organization Guide accuracy validation and any discrepancies found**
  - [ ] Smart testing results and any regressions found
  - [ ] Detailed debugging steps and results
  - [ ] Technical discoveries and integration insights
  - [ ] Current work status (complete/in-progress/blocked)
  - [ ] Next steps needed if work continues
  - [ ] Files modified/created with descriptions
  - [ ] **Code Organization Guide maintenance needs identified**
- [ ] Commit changes: `git add . && git commit -m "[descriptive message]"`
- [ ] Push to GitHub: `git push origin main`
- [ ] **DO NOT update core project docs** - session log captures all context
- [ ] Wait for explicit reconciliation signal from user
```

### Smart Regression Testing (5 minutes max) - Code Organization Guide Enhanced
```markdown
## Targeted Regression Verification
**HIGH RISK (Must test):** [Test the 1-3 features identified using Code Organization Guide integration analysis]
**MEDIUM RISK (Quick check):** [Basic verification of 1-2 medium-risk features per guide]
**Time-boxed rule:** If any test takes >2 minutes, note as "needs investigation" and move on
**Issues found:** [Any regressions - don't debug, just log for separate session]
**Status:** ✅ No regressions / ⚠️ Minor issues noted / 🚨 Major regression found
**Code Organization Guide Effectiveness:** [How well the guide identified risk areas]
**Guide Accuracy Validation:** [Did guide predictions match development reality?]
```

### Session Log Completion Template (Enhanced with Guide Maintenance):
```markdown
# Session Log: [Date] - Session [N] - [Brief Description]

## Session Overview
- **Goal:** [What we set out to accomplish this session]
- **Status:** [Complete/In Progress/Blocked/Debugging]
- **Next Steps:** [What needs to happen next]

## Code Organization Guide Usage & Validation
- **Files Identified:** [How the guide helped identify relevant files quickly]
- **Integration Points Used:** [Which documented integration points were leveraged]
- **Patterns Applied:** [Which development patterns from guide were followed]
- **Workflow Acceleration:** [How much time saved vs traditional approach]
- **Guide Accuracy:** [How well guide predictions matched actual development needs]
- **Discrepancies Found:** [Any areas where guide was inaccurate or incomplete]

## Code Organization Guide Maintenance Findings
- **File Health Changes:** [Any files crossing size/complexity thresholds]
- **New Integration Points:** [Undocumented dependencies or method signatures discovered]
- **Missing Patterns:** [Development approaches not covered in guide]
- **Risk Assessment Accuracy:** [How well guide risk predictions matched testing results]
- **Enhancement Opportunities:** [Specific improvements needed for guide]

## Smart Impact Analysis Results
- **Systems Modified:** [Hooks/components/state actually changed - validated against guide]
- **Integration Risk Assessment:** [HIGH/MEDIUM/LOW risk features identified using guide]
- **Smart Testing Plan:** [What we planned to test based on guide integration analysis]

## Work Accomplished This Session
- [Specific achievements, decisions made, code changes]
- [Debugging steps taken and results - guided by architecture understanding]
- [Technical patterns discovered or confirmed using guide knowledge]

## Smart Regression Testing Results
- **HIGH RISK Features Tested:** [Results of critical feature testing per guide analysis]
- **MEDIUM RISK Features Verified:** [Results of quick verification per guide integration points]
- **Issues Found:** [Any regressions discovered during testing]
- **Testing Time:** [How long testing took - should be ≤5 minutes]
- **Testing Accuracy:** [How well guide risk assessment predicted actual issues]
- **Status:** ✅ No regressions / ⚠️ Minor issues / 🚨 Major regression

## Files Modified/Created This Session
- `src/[path]/[filename]` - [description of changes, reference to guide categorization]
- `docs/[path]/[filename]` - [description of changes]

## Technical Discoveries & Integration Insights
- [Integration patterns learned, architecture insights - comparison with guide documentation]
- [Method signatures, interfaces, data flow understanding - validation of guide accuracy]
- [How new code connects with existing systems using documented patterns]

## Debugging Journey (Detailed)
- [Problems encountered and debugging approaches tried - guided by architecture knowledge]
- [Error messages and their resolution attempts using guide file identification]
- [What worked, what didn't work, and why - architecture context helped/hindered]
- [Context preservation for multi-session debugging]

## Information for Future Reconciliation
- **Project Status Changes:** [What capabilities are new/different]
- **Completion Documents Needed:** [If any features finished this session]
- **Archive Candidates:** [Planning docs that are now obsolete]
- **Code Organization Guide Maintenance Needs:** [Summary of guide updates needed]
- **Smart Testing Learnings:** [Any insights about feature dependencies validated/discovered]

## Handoff Notes for Next Session
- [Specific context needed if work continues - reference guide sections]
- [Current debugging state and next approaches to try using guide knowledge]
- [Integration points that still need investigation per guide]
- [Any regression issues that need separate debugging session]

## Current Status After Session
- **Application State:** [What's working now]
- **Architecture Health:** [Any changes to file health status from guide]
- **Code Organization Guide Status:** [Any maintenance needs identified]
- **Next Recommended Action:** [What should be tackled next - reference guide roadmap]

## Notes for Future Work
- [Important insights or reminders - enhanced with architecture understanding]
- [Opportunities identified for future development using guide patterns]
- [Any discoveries or lessons learned about code organization]
- [Feature dependency insights for future integration work]
- [Code Organization Guide improvement opportunities]
```

---

## 💡 Code Organization Guide Maintenance Best Practices

### Maintenance Philosophy
- **Accuracy First:** Guide must reflect current reality to maintain workflow efficiency
- **Incremental Updates:** Small, frequent updates better than large, infrequent ones
- **Validation Required:** All updates should be validated against actual implementation
- **User Oversight:** Significant changes require user review and approval

### Maintenance Triggers Summary
- **Immediate:** New files added/deleted, major refactoring completed
- **During Reconciliation:** Guide accuracy issues, missing patterns discovered
- **Periodic:** After major features, during architecture maintenance sessions
- **Validation:** When guide predictions don't match development reality

### Quality Assurance
- **Cross-Reference Validation:** Integration points checked against implementation
- **Pattern Effectiveness:** Development approaches validated through usage
- **Health Status Accuracy:** File assessments confirmed through analysis
- **Risk Assessment Precision:** Testing accuracy verified through regression results

---

**Template Usage:** Choose appropriate template, leverage Code Organization Guide for acceleration, maintain guide accuracy, create session logs during work, reconcile when user signals  
**Key Enhancement:** Code Organization Guide maintenance framework ensures continued workflow efficiency  
**Workflow:** Guide reference → Smart impact analysis → Information gathering → Guide validation → Session logs → Smart regression testing → Guide maintenance → Reconciliation  
**Maintenance Philosophy:** Treat Code Organization Guide as critical infrastructure requiring active maintenance for sustained development efficiency