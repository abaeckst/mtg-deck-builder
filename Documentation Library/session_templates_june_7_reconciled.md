# Development Session Templates

**Purpose:** Stable workflow templates for efficient development sessions with session log workflow and smart regression testing  
**Usage:** Choose appropriate template based on type of work, create session logs during active work  
**Last Updated:** June 7, 2025  

## 🚀 Session Startup Checklist

### Every Session Begins With:
```markdown
## Session Setup (5 minutes)
- [ ] Open VS Code to project folder: `C:\Users\carol\mtg-deck-builder`
- [ ] Run `npm start` to verify project compiles and loads correctly
- [ ] Check GitHub sync status: `git status`
- [ ] Review project_status.md for current state
- [ ] Check for previous session logs on related work for context
- [ ] Confirm session goal and success criteria
- [ ] **SMART IMPACT ANALYSIS** (2-3 minutes)
- [ ] Create new session log: session_log_YYYY-MM-DD_session[N]_[description].md
```

## 🎯 Smart Impact Analysis Protocol

### Pre-Session Analysis (2-3 minutes)
```markdown
## Smart Integration Analysis
**Systems being modified this session:**
- [ ] Hooks: [List specific hooks that will be changed]
- [ ] State: [What state objects/properties will change]  
- [ ] Components: [Which components will be modified]

**Features that use these systems:**
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

### Smart Testing Heuristics
```markdown
## High Risk Indicators (Always Test)
- Features using the same hooks you're modifying
- Features with complex state management (subscriptions, events)
- Features that have broken before from similar changes
- Features sharing data objects with your changes
- Features that integrate with modified architecture (validated in useCards overhaul)

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

## 📋 Template Types Available

1. **Enhancement Development** - Adding new features or capabilities
2. **Issue Resolution** - Fixing bugs or improving user experience
3. **Documentation Reconciliation** - Converting session logs to permanent documentation
4. **Environment Setup** - Development tool configuration or troubleshooting

---

## 📋 Template 1: Enhancement Development Session

### Session Goal Template:
```markdown
# Session Goal: [Enhancement Name] - [Brief Description]

## Pre-Session Information Gathering
**MANDATORY FIRST STEP - Request these files:**
- [ ] [List specific files needed for integration]
- [ ] [Related component files that might be affected]
- [ ] [Type definitions and interfaces to extend]
- [ ] [Hook files for state management patterns]
- [ ] [Previous session logs if this is multi-session work]

## Smart Impact Analysis (2-3 minutes)
**Systems being modified:**
- Hooks: [List specific hooks]
- State: [State objects/properties changing]
- Components: [Components being modified]

**Risk Assessment & Test Plan:**
- **HIGH RISK (Must test):** [1-3 features with complex dependencies]
- **MEDIUM RISK (Quick check):** [1-2 features with simpler integration]
- **SKIP:** [Independent features we won't test]

## Enhancement Implementation Goals
1. **[Primary Goal]** - [Description]
2. **[Secondary Goal]** - [Description]
3. **[Integration Goal]** - [Description]

## Implementation Plan
1. **Information Analysis** (15-30 min)
   - Review current implementation for integration points
   - Understand existing patterns and architecture
   - Map out enhancement requirements and dependencies
   
2. **Core Implementation** (60-180 min)
   - [Implementation step 1]
   - [Implementation step 2]
   - [Implementation step 3]
   - **Document progress in session log throughout**
   
3. **Integration & Testing** (30-60 min)
   - Integrate with existing components and systems
   - Test enhancement functionality thoroughly
   - **SMART REGRESSION TESTING (5 minutes max)**
   
4. **Session Documentation** (15-30 min)
   - Complete comprehensive session log with debugging details
   - Document technical discoveries and integration patterns
   - Note current status and next steps for potential continuation
   - **DO NOT update core project docs - use session log only**

## Session Success Criteria
- [ ] [Primary functionality working as designed]
- [ ] [Integration with existing system seamless]
- [ ] **[HIGH RISK features verified working - no regressions]**
- [ ] [TypeScript compilation succeeds with no errors]
- [ ] [Professional appearance matching existing standards]
- [ ] [Comprehensive session log created with all context]

## Files Expected to be Modified/Created
- [List of files that will be changed or created]

## Session Log Focus Areas
- **Smart Testing Results:** What HIGH/MEDIUM risk features were tested and results
- **Debugging Steps:** Detailed record of all debugging attempts and results
- **Technical Discoveries:** Integration patterns and architecture insights learned
- **Decision Rationale:** Why specific implementation approaches were chosen
- **Next Session Preparation:** Context needed if work continues across sessions
```

---

## 📋 Template 2: Issue Resolution Session

### Session Goal Template:
```markdown
# Session Goal: Fix [Specific Issue Description]

## Issue Analysis
- **Bug Description:** [Exact issue and reproduction steps]
- **Impact:** [What functionality is affected]
- **Error Messages:** [Any console/TypeScript errors]
- **Suspected Cause:** [What might be causing the issue]
- **Previous Debugging:** [Check session logs for prior attempts]

## Pre-Session Information Gathering
**MANDATORY FIRST STEP - Request these files:**
- [ ] [Files related to the bug area]
- [ ] [Integration points that might be affected]
- [ ] [Recent changes that might be related]
- [ ] [Previous session logs if this is ongoing debugging]

## Smart Impact Analysis (2-3 minutes)
**Systems being debugged/modified:**
- Bug Area: [Components/hooks with the issue]
- Likely Changes: [What will probably need to be fixed]

**Risk Assessment & Test Plan:**
- **HIGH RISK (Must test):** [Features that share code with bug area]
- **MEDIUM RISK (Quick check):** [Features that might be affected by fix]
- **SKIP:** [Unrelated features we won't test]

## Debugging Plan
1. **Issue Reproduction & Context Review** (15-30 min)
   - Review any previous session logs for debugging context
   - Confirm exact reproduction steps
   - Identify root cause through systematic testing
   - Check TypeScript errors and browser console
   
2. **Fix Implementation** (30-90 min)
   - Address root cause directly
   - Test fix in isolation first
   - Verify fix doesn't create new issues
   - **Document all debugging steps in session log**
   
3. **Regression Testing** (5-10 min max)
   - **SMART REGRESSION TESTING:** Test only HIGH RISK features
   - Quick verification of MEDIUM RISK features
   - **Time-boxed:** If testing takes >5 minutes, note as "needs investigation"

4. **Session Documentation** (15 min)
   - Complete detailed session log with debugging journey
   - Document resolution approach and any insights gained
   - Note verification steps taken
   - **DO NOT update core project docs - use session log only**

## Session Success Criteria
- [ ] Original issue completely resolved
- [ ] **No regressions in HIGH RISK features**
- [ ] Clean TypeScript compilation
- [ ] Professional user experience maintained
- [ ] Comprehensive debugging session log created

## Files Expected to be Modified
- [List of files that will likely need changes]

## Session Log Focus Areas
- **Smart Testing Results:** HIGH/MEDIUM risk features tested and results
- **Debugging Journey:** Every approach tried, what worked, what didn't
- **Root Cause Analysis:** How the issue was ultimately identified
- **Resolution Details:** Exact changes made and verification steps
- **Prevention Insights:** Learnings to avoid similar issues in future
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

## Pre-Reconciliation Review
**MANDATORY FIRST STEP - Review these materials:**
- [ ] All session logs in chronological order
- [ ] Current project_status.md for baseline
- [ ] Documentation_catalog.md for archive structure
- [ ] [Any additional context needed]

## Reconciliation Plan
1. **Session Log Analysis** (20-40 min)
   - Review all session logs chronologically
   - Identify completed features vs work-in-progress
   - Extract key technical discoveries and integration patterns
   - Map out documentation updates needed
   
2. **Completion Document Creation** (30-90 min)
   - Create completion documents for finished features
   - Include technical details, integration points, architecture insights
   - Document implementation approach and final decisions
   - Preserve key debugging insights and methodology
   - **Include smart testing results and regression prevention learnings**
   
3. **Core Documentation Updates** (20-40 min)
   - Update project_status.md with new capabilities
   - Update documentation_catalog.md with new archived materials
   - Archive planning documents that are now obsolete
   - Ensure single source of truth for current state
   
4. **Session Log Cleanup** (10 min)
   - Delete session logs after information is incorporated
   - Verify all important context preserved in permanent docs
   - Confirm clean project knowledge state

## Reconciliation Success Criteria
- [ ] All completed features have comprehensive completion documents
- [ ] Project status accurately reflects current capabilities
- [ ] Documentation catalog updated with new archives
- [ ] Planning documents for finished work moved to archive
- [ ] Session logs deleted after successful incorporation
- [ ] Clean project knowledge focused on current state and future options
- [ ] **Smart testing learnings preserved in completion documents**

## Expected Outputs
- **Completion Documents:** [List expected completion docs to be created]
- **Updated Core Docs:** [List permanent documents to be updated]
- **Archived Materials:** [List planning docs to be archived]
```

---

## 📋 Template 4: Environment Setup Session

### Session Goal Template:
```markdown
# Session Goal: [Environment Setup Task]

## Environment Goals
- **Primary Objective:** [Main setup or configuration task]
- **Verification Objective:** [How to confirm setup is working]
- **Documentation Objective:** [How to document the setup]

## Pre-Session Information Gathering
**MANDATORY FIRST STEP - Check current state:**
- [ ] Current development_environment.md for baseline
- [ ] Any error messages or issues encountered
- [ ] Required tools or extensions that need installation

## Setup Plan
1. **Current State Assessment** (10-20 min)
   - Verify current tool installations and configurations
   - Identify what needs to be installed, updated, or configured
   - Document any current issues or limitations
   
2. **Installation/Configuration** (30-90 min)
   - Install or update required tools
   - Configure development environment settings
   - Test that all tools work together properly
   - **Document process in session log**
   
3. **Verification & Testing** (20-30 min)
   - Test complete development workflow
   - Verify all extensions and tools function correctly
   - Test project compilation and development server
   - **Basic functionality verification (not full regression testing)**
   
4. **Session Documentation** (10-15 min)
   - Complete session log with setup details and any issues
   - Document verification steps and results
   - Note any troubleshooting discoveries
   - **Update development_environment.md if setup is complete**

## Session Success Criteria
- [ ] All required development tools installed and working
- [ ] Development workflow functions smoothly end-to-end
- [ ] Project compiles and runs without environment issues
- [ ] Setup process documented for future reference
- [ ] Any issues resolved with clear resolution steps
- [ ] Session log created with setup details

## Tools/Components to be Configured
- [List of development tools, extensions, or configurations to be handled]
```

---

## 🎯 Session Completion Checklist

### End-of-Session Protocol (Every Session):
```markdown
## Session Wrap-Up (10-15 minutes)
- [ ] All new code compiles without TypeScript errors
- [ ] Run `npm start` - application loads and all features work
- [ ] **SMART REGRESSION TESTING (5 minutes max):**
  - [ ] Test HIGH RISK features identified in pre-session analysis
  - [ ] Quick verification of MEDIUM RISK features
  - [ ] Log any issues found (don't debug during wrap-up)
- [ ] Complete comprehensive session log with:
  - [ ] Smart testing results and any regressions found
  - [ ] Detailed debugging steps and results
  - [ ] Technical discoveries and integration insights
  - [ ] Current work status (complete/in-progress/blocked)
  - [ ] Next steps needed if work continues
  - [ ] Files modified/created with descriptions
- [ ] Commit changes: `git add . && git commit -m "[descriptive message]"`
- [ ] Push to GitHub: `git push origin main`
- [ ] **DO NOT update core project docs** - session log captures all context
- [ ] Wait for explicit reconciliation signal from user
```

### Smart Regression Testing (5 minutes max)
```markdown
## Targeted Regression Verification
**HIGH RISK (Must test):** [Test the 1-3 features identified in pre-session analysis]
**MEDIUM RISK (Quick check):** [Basic verification of 1-2 medium-risk features]
**Time-boxed rule:** If any test takes >2 minutes, note as "needs investigation" and move on
**Issues found:** [Any regressions - don't debug, just log for separate session]
**Status:** ✅ No regressions / ⚠️ Minor issues noted / 🚨 Major regression found
```

### Session Log Completion Template:
```markdown
# Session Log: [Date] - Session [N] - [Brief Description]

## Session Overview
- **Goal:** [What we set out to accomplish this session]
- **Status:** [Complete/In Progress/Blocked/Debugging]
- **Next Steps:** [What needs to happen next]

## Smart Impact Analysis Results
- **Systems Modified:** [Hooks/components/state actually changed]
- **Integration Risk Assessment:** [HIGH/MEDIUM/LOW risk features identified]
- **Smart Testing Plan:** [What we planned to test and why]

## Work Accomplished This Session
- [Specific achievements, decisions made, code changes]
- [Debugging steps taken and results]
- [Technical patterns discovered or confirmed]

## Smart Regression Testing Results
- **HIGH RISK Features Tested:** [Results of critical feature testing]
- **MEDIUM RISK Features Verified:** [Results of quick verification]
- **Issues Found:** [Any regressions discovered during testing]
- **Testing Time:** [How long testing took - should be ≤5 minutes]
- **Status:** ✅ No regressions / ⚠️ Minor issues / 🚨 Major regression

## Files Modified/Created This Session
- `src/[path]/[filename]` - [description of changes]
- `docs/[path]/[filename]` - [description of changes]

## Technical Discoveries & Integration Insights
- [Integration patterns learned, architecture insights]
- [Method signatures, interfaces, data flow understanding]
- [How new code connects with existing systems]

## Debugging Journey (Detailed)
- [Problems encountered and debugging approaches tried]
- [Error messages and their resolution attempts]
- [What worked, what didn't work, and why]
- [Context preservation for multi-session debugging]

## Information for Future Reconciliation
- **Project Status Changes:** [What capabilities are new/different]
- **Completion Documents Needed:** [If any features finished this session]
- **Archive Candidates:** [Planning docs that are now obsolete]
- **Documentation Updates:** [What needs to be updated in core docs]
- **Smart Testing Learnings:** [Any insights about feature dependencies]

## Handoff Notes for Next Session
- [Specific context needed if work continues]
- [Current debugging state and next approaches to try]
- [Integration points that still need investigation]
- [Any regression issues that need separate debugging session]

## Current Status After Session
- **Application State:** [What's working now]
- **Next Recommended Action:** [What should be tackled next]

## Notes for Future Work
- [Important insights or reminders]
- [Opportunities identified for future development]
- [Any discoveries or lessons learned]
- [Feature dependency insights for future integration work]
```

---

## 🔧 File Update Methodology with Python Script Consistency

### Method Selection Guidelines

#### For Small Files (<500 lines) or Major Rewrites:
- Provide complete updated file content in artifacts
- Use for new files, complete restructuring, or targeted small files
- User copies content and replaces local file

#### For Large Files (500+ lines) with Incremental Changes:
- Create Python script using find-and-replace operations
- **CRITICAL: Follow Python Script Filename Consistency Protocol**
- Script should include all updates in single execution
- Use exact string matching with sufficient context
- Include clear success/error messages

#### Python Script Filename Consistency Protocol (MANDATORY):
```markdown
1. **Choose Script Filename FIRST** before creating artifact
2. **Standard Naming Pattern:** update_[component]_[feature].py
   - Examples: update_search_multifield.py, update_layout_resizing.py
3. **Use EXACT Filename** in both artifact title AND command
4. **Verify Consistency** before providing command to user
5. **Command Format:** python update_[component]_[feature].py
```

#### When to Ask:
"This file appears to be [X] lines with [incremental/major] changes. Should I use the Python script approach (with consistent filename) or provide the complete file?"

### File Update Script Template:
```python
#!/usr/bin/env python3

import os
import sys

def update_[component]_[feature](filename):
    """Update [filename] with [description of changes]"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make replacements with exact string matching
    updates = [
        # (old_string, new_string, description)
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"❌ Could not find: {desc}")
            return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = update_[component]_[feature]("[filename]")
    sys.exit(0 if success else 1)
```

---

## 💡 Best Practices Reminders

### Information-First Methodology
- **ALWAYS** request actual source files before implementing changes
- **NEVER** guess at interfaces, method signatures, or integration patterns  
- **VERIFY** all integration points and dependencies before coding
- **UNDERSTAND** complete data flow and state management before modifying
- **CHECK** previous session logs for context on ongoing work

### Smart Impact Analysis & Testing
- **ANALYZE** what systems you're modifying before coding (2-3 minutes)
- **IDENTIFY** HIGH and MEDIUM risk features that might be affected
- **TEST** only the features most likely to have regressions (5 minutes max)
- **TIME-BOX** testing - don't debug regressions during active development
- **LOG** any issues found for separate debugging sessions

### Session Log Workflow
- **CREATE** comprehensive session log for every development session
- **CAPTURE** detailed debugging steps, decisions, and technical discoveries
- **PRESERVE** context for multi-session features and debugging work
- **INCLUDE** smart testing results and any regression findings
- **ENABLE** smooth handoff between sessions with detailed notes
- **WAIT** for user's explicit reconciliation signal before updating core docs

### Quality Maintenance Standards
- Follow established project patterns and architectural decisions
- Maintain full TypeScript type safety throughout all changes
- Ensure no regressions in HIGH RISK existing functionality
- Test each change individually and in combination with others
- Verify complete user workflows remain functional after modifications

### Python Script Consistency
- Choose script filename FIRST before creating artifact
- Use standard naming pattern: update_[component]_[feature].py
- Ensure artifact filename matches command exactly
- Verify consistency before providing command to user
- Never use generic script names

### Documentation Hygiene with Session Logs
- Create session logs for all active work instead of updating core docs
- Capture comprehensive debugging context for multi-session work
- Include smart testing results and regression prevention insights
- Wait for user's reconciliation signal before creating completion documents
- Archive planning documents only during reconciliation process
- Maintain single source of truth through reconciliation workflow

---

**Template Usage:** Choose appropriate template, create session logs during work, reconcile when user signals  
**Key Principle:** Session logs capture context during active work, reconciliation updates permanent docs  
**Workflow:** Smart impact analysis → Information first → Session logs during work → Smart regression testing → Reconciliation on user signal  
**Testing Philosophy:** Intelligent, targeted regression testing focused on actual risk areas (validated across major architecture changes)  
**Update Frequency:** Templates remain stable, session logs created per session, reconciliation user-triggered