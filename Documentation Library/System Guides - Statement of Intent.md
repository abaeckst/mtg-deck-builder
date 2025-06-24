# System Guides - Statement of Intent

**Purpose:** Replace generic file identification with system-specific architectural understanding 
**Created:** January 14, 2025 
**Context:** Card sizing implementation failures revealed gaps in architectural understanding and file identification consistency

## 🎯 Problem Statement

### Current Documentation Gaps

**Code Organization Guide Limitations:**

- Feature-oriented ("Adding X feature → these files") but not problem-oriented ("X is broken → check these files")
- Generic file lists without architectural flow understanding
- No system boundaries - unclear which files work together as coherent systems
- Inconsistent file identification across sessions working on same system
  **System Specification Limitations:**
- High-level system behavior documentation
- Missing internal data flow and conditional logic
- No debugging-focused architectural guidance
- Too broad for efficient file identification during active development
  **Session Log Gaps:**
- Document what was attempted, not current system reality
- Don't capture architectural understanding failures
- Limited value for file identification in subsequent sessions
  
  ### Development Breakdown Pattern
  
  **Observed in card sizing sessions:**
1. **Inconsistent file requests** - Different files requested for same system across sessions
2. **Surface-level fixes** - Targeting code branches that never execute
3. **Integration misunderstanding** - Not knowing how props flow between components
4. **Conditional logic gaps** - Missing critical "if/else" flow understanding
   
   ## 🎯 System Guides Intent
   
   ### Core Philosophy
   
   **"Give Claude the architectural mental model needed for efficient, accurate development"**
   **Replace:** Generic file lists + broad specifications 
   **With:** System-specific architectural understanding + precise file identification
   
   ### Key Principles
   
   #### 1. System Boundary Definition
   
   **Each guide defines a coherent system with:**
- Complete file list that always works together
- Clear input/output boundaries
- Integration points with other systems
- Shared state and coordination patterns
  
  #### 2. Architectural Flow Understanding
  
  **Each guide provides internal system knowledge:**
- Critical data flow paths through the system
- Conditional logic branches and when they execute
- State propagation chains from triggers to effects
- Integration patterns and coordination mechanisms
  
  #### 3. Problem-Oriented File Identification
  
  **Each guide maps problems to specific files:**
- Common failure modes and their file locations
- Debugging starting points for system issues
- File dependency chains for cross-component problems
- Integration debugging between system boundaries
  
  #### 4. Current Reality Tracking
  
  **Each guide reflects actual implementation:**
- Current state vs. intended architecture
- Known divergences and technical debt
- Recent changes and their system impact
- Working vs. broken functionality status
  
  ### Design Goals
  
  #### Efficiency
- **Instant file identification:** "Card sizing issue → these 5 specific files"
- **Architectural context:** Understand why these files work together
- **Problem diagnosis:** Map symptoms to root cause locations
  
  #### Consistency
- **Repeatable file requests:** Same system = same files across sessions
- **Predictable debugging:** Standard approaches for system-level issues
- **Integration understanding:** How systems coordinate and share state
  
  #### Accuracy
- **Deep flow understanding:** Know which code branches actually execute
- **Conditional logic clarity:** Understand "if/else" decision points
- **Integration point precision:** Exact prop flow and state coordination
  
  ## 🎯 Success Criteria
  
  ### File Identification Success
- **Consistent requests:** Same files identified for same system across sessions
- **Complete coverage:** All files needed for system work identified upfront
- **Efficient focus:** No time wasted on irrelevant files or broad exploration
  
  ### Architectural Understanding Success
- **Flow comprehension:** Understand how data moves through system components
- **Conditional logic mastery:** Know which branches execute in practice
- **Integration clarity:** Understand cross-system coordination and state sharing
  
  ### Problem Resolution Success
- **Accurate diagnosis:** Map symptoms to correct root cause files
- **Efficient debugging:** Start debugging in the right file with right context
- **Integration debugging:** Understand cross-system failure modes
  
  ### Development Quality Success
- **First-attempt accuracy:** Fixes target actual problem locations
- **Integration preservation:** Changes don't break cross-system coordination
- **Technical debt awareness:** Understand system limitations and constraints
  
  ## 🎯 Integration with Existing Documentation
  
  ### Relationship to Current Docs
  
  **System Guides:** Focused architectural understanding for active development 
  **System Specifications:** High-level behavior and design intent documentation 
  **Session Logs:** Development progress and decision tracking 
  **Documentation Catalog:** Strategic archive retrieval for complex problems
  
  ### Workflow Integration
  
  **Active Development:** System Guides (file identification + architecture) → System Specs (design intent) → Session Logs (progress tracking) 
  **Complex Problems:** System Guides → Documentation Catalog (methodology retrieval) 
  **Strategic Planning:** System Specs → System Guides (implementation context)
  
  ### Maintenance Strategy
  
  **System Guides:** Updated with current reality as systems evolve 
  **System Specifications:** Updated with design intent and architectural decisions 
  **Session Logs:** Created during development, archived after reconciliation 
  **Documentation Catalog:** Strategic archive access for methodology replication
  
  ## 🎯 Implementation Approach
  
  ### Phase 1: Core System Guides
  
  **Start with systems identified in card sizing failures:**
- Card Display System Guide
- Layout State System Guide 
- Component Integration System Guide
  
  ### Phase 2: Comprehensive Coverage
  
  **Expand to all major systems:**
- Search & Filtering System Guide
- Drag & Drop System Guide
- Export & Formatting System Guide
  
  ### Phase 3: Integration & Refinement
  
  **Optimize for development efficiency:**
- Cross-system integration patterns
- Debugging workflow optimization
- File identification accuracy validation
  
  ### Success Metrics
  
  **Quantitative:**
- Consistent file identification across sessions (0 variation for same system)
- Reduced debugging time (problems → correct files in 1 attempt)
- Faster architectural understanding (no exploration needed)
  **Qualitative:**
- Accurate first-attempt fixes
- No integration breakage from system changes
- Deep architectural confidence during development

---

**Intent Summary:** Replace generic file identification with system-specific architectural understanding that enables efficient, accurate development with consistent file identification and deep flow comprehension.
**Next Steps:** Create system guide template and identify prioritized system guides for MTG Deck Builder project.
