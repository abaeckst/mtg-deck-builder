# MTG Deck Builder - Complete Development Guide

**Status:** Phase 4B+ Complete | **Path:** `C:\Users\carol\mtg-deck-builder` | **GitHub:** https://github.com/abaeckst/mtg-deck-builder

# 🚨 STOP - READ THIS FIRST - MANDATORY SESSION STARTUP

## EVERY SESSION MUST START WITH THIS EXACT SEQUENCE:

### 1. ASK FOR FILES (ALWAYS FIRST)

**Say exactly:** "What files should I examine for this work?"

- **DO NOT** use analysis tool to "investigate files"
- **DO NOT** assume what files are needed
- **DO NOT** start coding without seeing current state
- **WAIT** for user to provide specific files
  
  ### 2. EXAMINE PROVIDED FILES
- Read the actual current code state
- Understand what exists before suggesting changes
- Apply Code Organization Guide patterns to understand structure
  
  ### 3. THEN PROCEED WITH DEVELOPMENT
- Use proper protocols after understanding current state
- Create session log artifact
- Follow development workflow
  
  ## ❌ NEVER START A SESSION BY:
- Using analysis tool to "investigate" or "examine files"
- Writing code without seeing current implementation
- Making assumptions about what needs fixing
- Trying to "help" before understanding current code state
- Jumping straight into solutions

---

## 🚨 Critical Technical Limitations

**File Updates:**

- Claude cannot modify local files directly
- Provide complete content OR Python scripts for user to run
- **Python scripts ONLY for PROJECT SOURCE CODE** (components, hooks, utilities, CSS)
- **PROJECT KNOWLEDGE DOCUMENTS cannot be modified** - wait for reconciliation signal
- Python scripts: Artifact filename must match command filename exactly
- Large files (500+ lines): Create update scripts vs full content
  **Required Process:**
1. Choose script filename FIRST: `update_[component]_[feature].py`
2. Use exact same name in artifact title AND command
3. **Verify file type:** Project source code (scriptable) vs project knowledge (wait for reconciliation)
4. Small files: Provide complete updated content
   **File Type Classification:**
- **Project Source Code (Can Script):** All files in `/src/` directory, CSS files, config files
- **Project Knowledge (Cannot Modify):** Documentation files, session templates, project status, code organization guide
  
  ## 🎯 Enhanced Development Workflow
  
  **Foundation:** Code Organization Guide + Session Logs + Smart Testing = Maximum efficiency
  
  ### Universal Session Startup (MANDATORY)
  
  ```markdown
  
  ## Session Setup - NEVER SKIP THESE STEPS
1. [ ] **ASK FOR FILES:** "What files should I examine for this work?" (ALWAYS FIRST)
2. [ ] **WAIT FOR FILES:** Do not proceed until user provides specific files
3. [ ] **EXAMINE PROVIDED CODE:** Understand current state using Code Organization Guide
4. [ ] **Session Goal:** [Clear objective with success criteria]
5. [ ] **CREATE SESSION LOG ARTIFACT:** `session_log_YYYY-MM-DD_[description].md` (MANDATORY)
6. [ ] **Impact Analysis:** HIGH/MEDIUM/LOW risk features using guide integration points
   ```
   
   ### Mandatory Implementation Checklist:
   
   **Session Logs:**
- [ ] **ALWAYS create session log artifacts** (never text-only summaries)
- [ ] Document progress, decisions, and guide validation
- [ ] Include smart testing results and next steps
  **Python Scripts:**
- [ ] **State filename FIRST:** "Creating update_search_performance.py"
- [ ] **Verify file type:** Confirm target is project source code, not project knowledge
- [ ] **Create artifact with EXACT filename stated**
- [ ] **Verify match before sending:** "✅ Filename verified: update_search_performance.py"
- [ ] **Provide command with EXACT same filename**
  **Development Process:**
- [ ] **Reference Code Organization Guide** for file identification and patterns
- [ ] **Apply proven patterns** (component extraction, performance optimization, unified state)
- [ ] **Smart testing only HIGH risk features** (5min max)
- [ ] **Step back after 2-3 failed attempts** - request additional context
  
  ### Essential Steps:
1. **ASK FOR FILES FIRST** - Never assume what code to examine
2. **File Identification:** Use Code Organization Guide decision tree for instant location
3. **Pattern Application:** Apply documented integration points and proven methodologies 
4. **Session Documentation:** Create artifact-based session logs during work
5. **Quality Assurance:** Risk-based testing using guide impact analysis
   
   ### Debugging Protocol:
- **Performance Issues:** Apply timing analysis → identify bottlenecks → fix re-render loops
- **Integration Problems:** Use systematic debugging methodology from archives
- **After 2-3 attempts:** "I may be missing fundamental context about how [system] works"
- **Destructive changes:** Get explicit permission before removing functionality
  
  ## 📋 Session Type Templates
  
  ### Enhancement Development
  
  ```markdown
  **FIRST STEP:** Ask "What files should I examine for this work?"
  **Goal:** [Enhancement name and description]
  **Files:** [WAIT FOR USER TO PROVIDE - do not assume]
  **Pattern:** [Development pattern from guide after examining files]
  **Implementation:** [1-3 key steps after understanding current state]
  **Success Criteria:** [Specific deliverables]
  ```
  
  ### Issue Resolution
  
  ```markdown
  **FIRST STEP:** Ask "What files should I examine for this work?"
  **Issue:** [Exact problem and reproduction]
  **Files:** [WAIT FOR USER TO PROVIDE - do not assume]
  **Debugging Plan:** [Systematic approach after examining current code]
  **Success Criteria:** [Issue resolved + no regressions]
  ```
  
  ### Technical Debt Resolution
  
  ```markdown
  **FIRST STEP:** Ask "What files should I examine for this work?"
  **Goal:** [Technical debt item]
  **Files:** [WAIT FOR USER TO PROVIDE - do not assume]
  **Resolution Approach:** [After examining current implementation]
  **Success Criteria:** [Technical debt resolved + functionality maintained]
  ```
  
  ### Architecture Work
  
  ```markdown
  **FIRST STEP:** Ask "What files should I examine for this work?"
  **Goal:** [Refactoring objective]
  **Files:** [WAIT FOR USER TO PROVIDE - do not assume]
  **Pattern:** [Extraction/improvement methodology after examining code]
  **Success Criteria:** [Improved architecture + maintained functionality]
  ```
  
  ### Performance Optimization
  
  ```markdown
  **FIRST STEP:** Ask "What files should I examine for this work?"
  **Goal:** [Performance improvement objective]
  **Files:** [WAIT FOR USER TO PROVIDE - do not assume]
  **Pattern:** [Hook optimization patterns after examining current implementation]
  **Success Criteria:** [Measurable performance improvement]
  ```
  
  ### Cross-System Integration
  
  ```markdown
  **FIRST STEP:** Ask "What files should I examine for this work?"
  **Goal:** [Integration objective involving multiple systems]
  **Files:** [WAIT FOR USER TO PROVIDE - do not assume]
  **Pattern:** [Cross-system coordination after examining current state]
  **Success Criteria:** [Successful integration + maintained system boundaries]
  ```
  
  ## 🎯 Session Execution Protocol
  
  ### Pre-Development Checklist:
- **ASK FOR FILES FIRST:** "What files should I examine for this work?" (NEVER SKIP)
- **Python Scripts:** State filename FIRST: "Creating update_[component]_[feature].py" (PROJECT SOURCE CODE ONLY)
- **Enhanced Guide Reference:** Apply Code Organization Guide patterns after examining files
- **Session Log:** Create MANDATORY artifact (never text-only summary)
  
  ### During Development:
- **Apply proven patterns** after understanding current implementation
- **File size awareness** - If modifying 400+ line files, note size and suggest extraction when relevant
- **Document progress** - Key decisions, pattern usage in session log artifact
- **Step back trigger** - After 2-3 failed attempts, request additional context
- **Performance focus** - Apply timing analysis when relevant
  
  ### Smart Testing (5 minutes max):
- **HIGH Risk:** Test 1-3 features with complex dependencies
- **MEDIUM Risk:** Quick verification of 1-2 simpler integrations 
- **SKIP:** Independent features identified in guide
- **Time-box strictly** - Log issues, don't debug during wrap-up
  
  ### Python Script Protocol:
- **Filename verification:** "✅ Filename verified: update_[component]_[feature].py"
- **Command match:** Provide exact same filename in command
- **PROJECT SOURCE CODE ONLY:** Components, hooks, utilities - NOT project knowledge documents
- **Large files:** Use update scripts vs full content for 500+ line files
  
  ## 📝 Session Log Template (MANDATORY ARTIFACT)
  
  ```markdown
  
  # Session Log: [Date] - [Brief Description]
  
  ## Goal & Status
  
  **Objective:** [What we set out to accomplish]
  **Status:** [Complete/In Progress/Blocked]
  **Files Examined:** [List files user provided for examination]
  **Files Modified:** [List with brief descriptions]
  
  ## Enhanced Code Organization Guide Usage
  
  **Files Identified:** [How guide accelerated development after examining code]
  **Patterns Applied:** [Which documented patterns used]
  **Guide Accuracy:** [Discrepancies found, maintenance needs]
  
  ## Key Decisions & Technical Insights
- [Major technical decisions made after examining current implementation]
- [Integration patterns discovered/confirmed]
- [File size considerations - extraction suggestions if relevant]
  
  ## Smart Testing Results
  
  **HIGH Risk Features:** [Results of critical testing]
  **Issues Found:** [Any regressions - separate debugging needed]
  **Testing Time:** [Should be ≤5 minutes]
  
  ## Python Script Verification (if applicable)
  
  **Filename Stated:** [Exact filename declared at start]
  **Artifact Created:** [Confirmation of exact match]
  **Command Provided:** [Verification of exact filename match]
  **File Type:** [Confirmed as project source code, not project knowledge]
  
  ## Next Steps & Context
  
  **Current Status:** [What's working now]
  **Next Action:** [What should happen next]
  **Important Context:** [Key info if work continues]
  ```
  
  ## 🔄 Session Completion Protocol
  
  ```markdown
  
  ## End-of-Session Protocol (10 minutes)

- [ ] **Smart Testing:** HIGH risk features (5min max)
- [ ] **Session Log Artifact:** Complete with guide validation
- [ ] **Python Script Verification:** If applicable, confirm filename match and source code target
- [ ] **Git Commit:** `git add . && git commit -m "[descriptive message]"`
- [ ] **Push Changes:** `git push origin main`
- [ ] **No Core Doc Updates** - Wait for reconciliation signal
  ```
  
  ## 📚 Documentation Strategy
  
  ### Active Project Knowledge (Claude's Memory):

- **Code Organization Guide** - Streamlined file identification and integration patterns
- **Project Status** - Current capabilities and development options
- **Development Session Templates** - Efficient workflow methodology
- **Documentation Catalog** - Archive retrieval guide
  
  ### Strategic Archive System:
- **When Needed:** Similar problems to past solutions, methodology replication, architectural decisions
- **Categories:** Implementation case studies, methodology patterns, technical deep dives, session archives
- **Access Pattern:** Problem-based retrieval using catalog guide
  
  ### Workflow:
  
  **Active Development:** ASK FOR FILES FIRST → Code Org Guide → Session artifacts → Smart testing 
  **Strategic Retrieval:** Documentation catalog for proven methodologies and implementation details 
  **Reconciliation:** User signals → Update active docs → Archive detailed session materials
  
  ## ❌ Critical Anti-Patterns
  
  **Session Startup Violations (NEVER DO THESE):**
- Starting with analysis tool to "investigate files"
- Writing code without examining current state first
- Making assumptions about what files are needed
- Jumping straight into solutions without understanding current implementation
- Skipping the "What files should I examine?" question
  **Workflow Violations:**
- Session logs as text responses (must be artifacts)
- Python filename mismatches (choose name FIRST)
- Attempting to script project knowledge documents (only source code)
- Skipping Code Organization Guide reference (efficiency loss)
- Testing everything instead of risk-based approach
  **Development Anti-Patterns:**
- Update `project_status.md` during active work (wait for reconciliation)
- Make destructive changes without permission
- Continue debugging >3 attempts without requesting context
- Skip proven pattern application when relevant
  
  ## 🔄 Session Flow
  
  ### **Development Sessions:**
  
  **Start:** 
1. **ASK FOR FILES:** "What files should I examine for this work?" (MANDATORY FIRST STEP)
2. **WAIT FOR FILES:** Do not proceed until provided
3. **EXAMINE FILES:** Understand current state before suggesting changes
4. State filename if creating Python scripts (verify source code target)
5. Code Organization Guide → Impact analysis → Pattern identification
   **During:** 
6. Create session log artifact documenting progress
7. Apply patterns after understanding current implementation
8. Step back if stuck after 2-3 attempts
   **End:** 
9. Smart testing (HIGH risk only) → Session log completion
10. Verify Python script filename matches and targets source code
11. Wait for reconciliation signal before updating core docs
    
    ## 🚀 Ready for Development
    
    **Optimized Setup:**
- **Streamlined Code Organization Guide** - 40% more efficient, maintains full utility
- **Strategic Documentation Catalog** - Archive retrieval for complex problems
- **Enhanced Session Workflow** - Artifact-based logs with proven pattern application
  **Next Session Protocol:**
  **MANDATORY FIRST STEP:**
1. **ASK:** "What files should I examine for this work?"
2. **WAIT:** For user to provide specific files
3. **EXAMINE:** Current code state using Code Organization Guide
4. **THEN:** Apply proven patterns and create session log artifact
   **For Development Work:**
5. **Smart testing** HIGH risk features only (5min max)
6. **Filename verification** for Python scripts (state name FIRST, verify source code target)

---

**Achievement:** Streamlined development workflow with mandatory file examination protocol and maximum efficiency 
**Status:** Ready for continued development with optimized productivity and proven methodologies 
**CRITICAL:** Every session must start by asking for files to examine - never assume or investigate independently
