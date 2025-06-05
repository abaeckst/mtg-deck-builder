# Development Session Templates

**Purpose:** Stable workflow templates for efficient development sessions  
**Usage:** Choose appropriate template based on type of work, customize with specific goals  
**Last Updated:** June 5, 2025  

## 🚀 Session Startup Checklist

### Every Session Begins With:
```markdown
## Session Setup (5 minutes)
- [ ] Open VS Code to project folder: `C:\Users\carol\mtg-deck-builder`
- [ ] Run `npm start` to verify project compiles and loads correctly
- [ ] Check GitHub sync status: `git status`
- [ ] Review project_status.md for current state
- [ ] Confirm session goal and success criteria
```

## 📋 Template Types Available

1. **Enhancement Development** - Adding new features or capabilities
2. **Issue Resolution** - Fixing bugs or improving user experience
3. **Documentation Work** - Archiving, organizing, or updating documentation
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
   
3. **Integration & Testing** (30-60 min)
   - Integrate with existing components and systems
   - Test enhancement functionality thoroughly
   - Verify no regressions in existing features
   
4. **Polish & Documentation** (15-30 min)
   - Final styling and user experience improvements
   - Update project status with completion
   - Create completion document for archive

## Session Success Criteria
- [ ] [Primary functionality working as designed]
- [ ] [Integration with existing system seamless]
- [ ] [No regressions in existing functionality]
- [ ] [TypeScript compilation succeeds with no errors]
- [ ] [Professional appearance matching existing standards]

## Files Expected to be Modified/Created
- [List of files that will be changed or created]
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

## Pre-Session Information Gathering
**MANDATORY FIRST STEP - Request these files:**
- [ ] [Files related to the bug area]
- [ ] [Integration points that might be affected]
- [ ] [Recent changes that might be related]

## Debugging Plan
1. **Issue Reproduction** (15-30 min)
   - Confirm exact reproduction steps
   - Identify root cause through systematic testing
   - Check TypeScript errors and browser console
   
2. **Fix Implementation** (30-90 min)
   - Address root cause directly
   - Test fix in isolation first
   - Verify fix doesn't create new issues
   
3. **Regression Testing** (20-30 min)
   - Test all related functionality
   - Verify complete user workflows still work
   - Check for any side effects of the fix

4. **Documentation** (10 min)
   - Update project status with issue resolution
   - Document any insights or preventive measures

## Session Success Criteria
- [ ] Original issue completely resolved
- [ ] No new issues introduced by fix
- [ ] All related functionality tested and working
- [ ] Clean TypeScript compilation
- [ ] Professional user experience maintained

## Files Expected to be Modified
- [List of files that will likely need changes]
```

---

## 📋 Template 3: Documentation Work Session

### Session Goal Template:
```markdown
# Session Goal: [Documentation Task]

## Documentation Goals
- **Primary Objective:** [Main documentation task]
- **Archive Objective:** [What to archive, if applicable]
- **Organization Objective:** [How to improve documentation structure]

## Pre-Session Information Gathering
**MANDATORY FIRST STEP - Review these resources:**
- [ ] Current project_status.md for context
- [ ] Documentation_catalog.md for existing archive structure
- [ ] [Any completion documents that need to be created]

## Documentation Plan
1. **Review and Analysis** (15-30 min)
   - Review current documentation state
   - Identify what needs to be archived vs. kept active
   - Plan organization improvements
   
2. **Archive Creation** (30-90 min)
   - Create completion documents for finished work
   - Move planning documents to archive
   - Update archive organization structure
   
3. **Active Knowledge Update** (20-40 min)
   - Update project_status.md with current state
   - Update documentation_catalog.md with new archives
   - Clean obsolete information from active documents
   
4. **Verification** (10 min)
   - Verify all information is accessible via catalog
   - Ensure active documents focus on current state
   - Test that archived information can be found easily

## Session Success Criteria
- [ ] All completed work has appropriate completion documents
- [ ] Planning documents for finished work moved to archive
- [ ] Active documents focus only on current state and immediate options
- [ ] Documentation catalog accurately reflects archive contents
- [ ] Information finding workflow is clear and efficient

## Documents to be Created/Updated
- [List of documentation files to be modified]
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
   
3. **Verification & Testing** (20-30 min)
   - Test complete development workflow
   - Verify all extensions and tools function correctly
   - Test project compilation and development server
   
4. **Documentation Update** (10-15 min)
   - Update development_environment.md with changes
   - Document any new procedures or requirements
   - Note any troubleshooting steps discovered

## Session Success Criteria
- [ ] All required development tools installed and working
- [ ] Development workflow functions smoothly end-to-end
- [ ] Project compiles and runs without environment issues
- [ ] Environment setup documented for future reference
- [ ] Any issues resolved with clear resolution steps

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
- [ ] Test complete user workflow end-to-end for affected areas
- [ ] Verify no regressions in existing functionality  
- [ ] Update project_status.md with progress and new current state
- [ ] Update documentation_catalog.md if created new archives
- [ ] Commit changes: `git add . && git commit -m "[descriptive message]"`
- [ ] Push to GitHub: `git push origin main`
- [ ] Document any issues or next steps discovered
```

### Session Summary Template:
```markdown
## Session Summary: [Date] - [Session Type and Goal]

### Accomplished:
- ✅ [Primary objective completed]
- ✅ [Secondary objectives completed]
- ✅ [Integration/testing verified]

### Files Modified/Created:
- `src/[path]/[filename]` - [description of changes]
- `docs/[path]/[filename]` - [description of changes]

### Issues Resolved/Improvements Made:
- [Specific issue] - [How it was resolved]
- [Enhancement] - [What was improved]

### Current Status After Session:
- **Application State:** [What's working now]
- **Next Recommended Action:** [What should be tackled next]

### Notes for Future Sessions:
- [Important insights or reminders]
- [Opportunities identified for future work]
- [Any discoveries or lessons learned]
```

---

## 🔧 File Update Methodology

### Method Selection Guidelines

#### For Small Files (<500 lines) or Major Rewrites:
- Provide complete updated file content in artifacts
- Use for new files, complete restructuring, or targeted small files
- User copies content and replaces local file

#### For Large Files (500+ lines) with Incremental Changes:
- Create Python script using find-and-replace operations
- Script should include all updates in single execution
- Use exact string matching with sufficient context
- Include clear success/error messages

#### When to Ask:
"This file appears to be [X] lines with [incremental/major] changes. Should I use the Python script approach or provide the complete file?"

### File Update Script Template:
```python
#!/usr/bin/env python3

import os
import sys

def update_file(filename):
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
    success = update_file("[filename]")
    sys.exit(0 if success else 1)
```

---

## 💡 Best Practices Reminders

### Information-First Methodology
- **ALWAYS** request actual source files before implementing changes
- **NEVER** guess at interfaces, method signatures, or integration patterns  
- **VERIFY** all integration points and dependencies before coding
- **UNDERSTAND** complete data flow and state management before modifying

### Quality Maintenance Standards
- Follow established project patterns and architectural decisions
- Maintain full TypeScript type safety throughout all changes
- Ensure no regressions in existing functionality
- Test each change individually and in combination with others
- Verify complete user workflows remain functional after modifications

### Documentation Hygiene
- Create completion documents for all finished work
- Archive planning documents when work is complete
- Keep active project knowledge focused on current state and immediate options
- Update documentation catalog when creating new archives
- Maintain single source of truth in project_status.md

---

**Template Usage:** Choose appropriate template, customize with specific goals, follow information-first methodology  
**Key Principle:** Templates provide structure, specific session goals provide content  
**Update Frequency:** Templates remain stable, updated only when improving workflow methodology