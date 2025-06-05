# Development Session Templates - Future Phases

**Purpose:** Standardized templates for efficient development sessions  
**Goal:** Every session starts with clear objectives and ends with working, tested features  
**Current Status:** Phase 3H Complete - Ready for Phase 4+ Implementation  

## 🚀 Session Startup Checklist

### Every Session Begins With:
```markdown
## Session Setup (5 minutes)
- [ ] Open VS Code to project folder: `c:\Users\carol\mtg-deck-builder`
- [ ] Run `npm start` to verify project compiles and loads
- [ ] Check GitHub sync status: `git status`
- [ ] Review updated_project_status.md for current state
- [ ] Confirm session goal and success criteria
```

### Available Session Types:
1. **Phase 4 Implementation** - Import/Export & File Management (NEXT PRIORITY)
2. **Phase 5 Implementation** - Advanced Analysis & Preview
3. **Phase 6 Implementation** - Performance & Polish
4. **Bug Fix & Polish** - Resolve issues and improve UX
5. **Feature Enhancement** - Extend existing functionality

## 📋 Template 1: Phase 4 - Import/Export & File Management (NEXT PRIORITY)

### Session Goal Template:
```markdown
# Session Goal: Phase 4 - Import/Export & File Management

## Pre-Session Information Gathering
**MANDATORY FIRST STEP - Request these files:**
- [ ] `src/hooks/useCards.ts` - Current deck state management
- [ ] `src/components/MTGOLayout.tsx` - UI integration points for import/export
- [ ] `src/types/card.ts` - Type definitions for deck structure
- [ ] `src/services/scryfallApi.ts` - Card lookup and validation patterns
- [ ] Current deck management patterns for integration

## Phase 4 Implementation Goals
1. **Deck Import System** - Support .txt, .dec, .dek file formats
2. **Deck Export System** - Export to multiple standard formats
3. **File Management** - Save/load deck configurations
4. **Format Validation** - Import validation and error handling
5. **UI Integration** - Import/export controls in main interface

## Implementation Plan
1. **Information Analysis** (20 min)
   - Review current deck state structure in useCards.ts
   - Understand UI integration points in MTGOLayout
   - Map out file format specifications for import/export
   - Identify TypeScript interfaces needed for deck files
   
2. **Core Implementation** (120-150 min)
   - Create deck import service with format parsers
   - Create deck export service with format generators
   - Implement file validation and error handling
   - Add card name resolution for imported decks
   - Create import/export UI components
   
3. **UI Integration** (30 min)
   - Add import/export buttons to main interface
   - Integrate file drop zone functionality
   - Add import/export modal dialogs
   - Connect with existing deck management system
   
4. **Testing & Polish** (30 min)
   - Test import of various deck file formats
   - Test export to multiple formats
   - Verify file validation and error messages
   - Test integration with existing deck functionality
   
5. **Documentation** (15 min)
   - Update updated_project_status.md with Phase 4 completion
   - Document supported file formats for users
   - Commit and push all changes

## Session Success Criteria
- [ ] Import .txt, .dec, .dek files successfully
- [ ] Export to multiple standard formats
- [ ] File validation provides clear error messages
- [ ] Integration with existing deck management works
- [ ] File drag-and-drop functionality works
- [ ] All existing functionality continues working
- [ ] TypeScript compilation succeeds with no errors
- [ ] Professional appearance matching existing MTGO styling

## Files Expected to be Modified/Created
- `src/services/deckImport.ts` - New import service
- `src/services/deckExport.ts` - New export service
- `src/components/ImportExportModal.tsx` - New UI component
- `src/components/MTGOLayout.tsx` - Import/export button integration
- `src/hooks/useCards.ts` - Deck loading/saving state management
- `src/types/deck.ts` - New deck file type definitions
```

## 📋 Template 2: Phase 5 - Advanced Analysis & Preview

### Session Goal Template:
```markdown
# Session Goal: Phase 5 - Advanced Analysis & Preview

## Pre-Session Information Gathering
**MANDATORY FIRST STEP - Request these files:**
- [ ] `src/hooks/useCards.ts` - Current deck data for analysis
- [ ] `src/components/MTGOLayout.tsx` - UI layout for analysis panel
- [ ] `src/components/MagicCard.tsx` - Current card display for preview enhancement
- [ ] Current hover/interaction patterns for preview integration

## Phase 5 Implementation Goals
1. **Card Preview System** - Large card preview on hover
2. **Mana Curve Analysis** - Visual deck analysis charts
3. **Statistics Dashboard** - Comprehensive deck metrics
4. **Format Legality** - Real-time legality checking
5. **Analysis Integration** - Seamless UI integration

## Implementation Plan
1. **Architecture Planning** (15 min)
   - Review current deck data structure for analysis
   - Plan preview positioning and interaction system
   - Design analysis component architecture
   
2. **Preview System** (60-90 min)
   - Create large card preview component
   - Implement hover positioning logic
   - Add high-resolution image support
   - Integrate with existing card interactions
   
3. **Analysis Dashboard** (90-120 min)
   - Create mana curve visualization component
   - Implement deck statistics calculations
   - Add format legality checking system
   - Create analysis panel UI
   
4. **Integration & Testing** (45 min)
   - Integrate analysis panel into main layout
   - Test preview system in all view modes
   - Verify analysis updates with deck changes
   - Test format legality for various formats

## Session Success Criteria
- [ ] Card preview shows on hover with proper positioning
- [ ] Mana curve chart displays accurate analysis
- [ ] Format legality checking works correctly
- [ ] Statistics update in real-time
- [ ] Preview works in all view modes
- [ ] Analysis provides actionable insights
```

## 📋 Template 3: Phase 6 - Performance & Polish

### Session Goal Template:
```markdown
# Session Goal: Phase 6 - Performance & Polish

## Pre-Session Information Gathering
**MANDATORY FIRST STEP - Request these files:**
- [ ] `src/components/MTGOLayout.tsx` - Current performance bottlenecks
- [ ] `src/hooks/useCards.ts` - Large collection handling
- [ ] `src/components/ListView.tsx` - List view performance patterns
- [ ] Current performance issues or user feedback

## Phase 6 Implementation Goals
1. **Performance Optimization** - Virtual scrolling and caching
2. **Offline Capability** - Service worker and PWA features
3. **Accessibility** - WCAG compliance and keyboard navigation
4. **User Preferences** - Advanced customization system
5. **Production Polish** - Final quality improvements

## Implementation Plan
1. **Performance Analysis** (30 min)
   - Profile current performance with large datasets
   - Identify bottlenecks in rendering and state management
   - Plan optimization strategies
   
2. **Optimization Implementation** (90-120 min)
   - Implement virtual scrolling for large collections
   - Add advanced caching strategies
   - Optimize image loading and memory usage
   - Add performance monitoring
   
3. **Accessibility & PWA** (60-90 min)
   - Implement service worker for offline capability
   - Add WCAG compliance improvements
   - Enhance keyboard navigation
   - Add PWA manifest and features
   
4. **Testing & Polish** (45 min)
   - Test performance with 10,000+ card collections
   - Verify offline functionality
   - Test accessibility with screen readers
   - Verify all optimizations work correctly

## Session Success Criteria
- [ ] Smooth performance with large collections
- [ ] Offline functionality works properly
- [ ] Accessibility tools can navigate interface
- [ ] User preferences sync correctly
- [ ] Memory usage remains stable
- [ ] All interactions remain responsive
```

## 🧹 Template 4: Bug Fix & Polish Session

### Session Goal Template:
```markdown
# Session Goal: Fix [Specific Issues]

## Issue Analysis
- **Bug Description:** [Exact issue and reproduction steps]
- **Impact:** [What functionality is affected]
- **Error Messages:** [Any console/TypeScript errors]
- **Recent Changes:** [What might have caused the issue]

## Pre-Session Information Gathering
**MANDATORY FIRST STEP - Request these files:**
- [ ] Files related to the bug area
- [ ] Integration points that might be affected
- [ ] Recent changes that might be related

## Debugging Plan
1. **Issue Reproduction** (15 min)
   - Confirm exact reproduction steps
   - Identify root cause through systematic testing
   - Check TypeScript errors and browser console
   
2. **Fix Implementation** (45-60 min)
   - Address root cause directly
   - Test fix in isolation first
   - Verify fix doesn't create new issues
   
3. **Regression Testing** (20 min)
   - Test all related functionality
   - Verify complete user workflows still work
   - Check for any side effects of the fix

## Session Success Criteria
- [ ] Original issue completely resolved
- [ ] No new issues introduced by fix
- [ ] All related functionality tested and working
- [ ] Clean TypeScript compilation
- [ ] Professional user experience maintained
```

## 🎯 Session Completion Templates

### End-of-Session Checklist:
```markdown
## Session Wrap-Up (10 minutes)
- [ ] All new code compiles without TypeScript errors
- [ ] Run `npm start` - application loads and all features work
- [ ] Test complete user workflow end-to-end
- [ ] Verify no regressions in existing functionality  
- [ ] Update updated_project_status.md with progress
- [ ] Commit changes: `git add . && git commit -m "[descriptive message]"`
- [ ] Push to GitHub: `git push origin main`
- [ ] Document any issues or next steps discovered
```

### Session Summary Template:
```markdown
## Session Summary: [Date] - [Phase/Goal]

### Accomplished:
- ✅ [Primary objective completed]
- ✅ [Secondary objectives completed]
- ✅ [Integration verified]

### Files Modified/Created:
- `src/[path]/[filename]` - [description of changes]
- `src/[path]/[filename]` - [description of changes]

### Issues Resolved:
- [Specific issue] - [How it was resolved]
- [Performance improvement] - [What was optimized]

### Current Status:
- **Phase:** [Current phase status after session]
- **Working Features:** [Confirmed functional features]
- **Next Priority:** [Recommended next session focus]

### Notes for Next Session:
- [Important insights or reminders]
- [Opportunities identified for future work]
- [Any user feedback or observations]
```

## 🔧 File Update Method Selection

### For Small Files (<500 lines) or Major Rewrites:
- Provide complete updated file content
- Use for new files, complete restructuring, or small targeted files

### For Large Files (500+ lines) with Incremental Changes:
- Create Python script using find-and-replace operations
- Script should include all updates in single execution
- Use exact string matching with sufficient context
- Include clear success/error messages

### When to Ask:
"This file appears to be [X] lines with [incremental/major] changes. Should I use the Python script approach or provide the complete file?"

## 🎯 Current Phase Quick Reference

### Phase 4 Session (READY WHEN DESIRED):
```markdown
Goal: Import/Export & File Management system
Files needed first: useCards.ts, MTGOLayout.tsx, card.ts, scryfallApi.ts
Time estimate: 4-6 hours (2-3 sessions)
Success: Import/export multiple formats, file validation working
Next step after success: Phase 5 advanced analysis implementation
```

### Phase 5 Session (AFTER 4):
```markdown
Goal: Advanced analysis tools and card preview system
Requirements: Phase 4 completion (import/export working)
Features: Card preview, mana curve, statistics, format legality
```

### Phase 6 Session (AFTER 5):
```markdown
Goal: Performance optimization and production polish
Requirements: Phase 5 completion (analysis tools working)
Features: Virtual scrolling, offline capability, accessibility, PWA
```

## 💡 Best Practices Reminders

### Information-First Methodology:
- **ALWAYS** request actual source files before coding
- **NEVER** guess at interfaces or method signatures  
- **VERIFY** integration points before implementation
- **UNDERSTAND** complete data flow and state management

### Implementation Success:
- Follow established project patterns and conventions
- Maintain TypeScript type safety throughout
- Test each change individually and in combination
- Verify no regressions in existing functionality

### Documentation Hygiene:
- Update updated_project_status.md immediately after completion
- Maintain single source of truth for project status
- Keep current documentation clean and accurate
- Archive completed phase documentation appropriately

---

**Usage Instructions:**
1. **Start each session** by choosing template based on desired enhancement
2. **Follow information-gathering step** - Critical for integration success
3. **Use appropriate file update method** - Script for large files, complete for small/new files
4. **Complete wrap-up steps** before ending any session
5. **Update master status** to reflect actual completion state

**Current Priority:** Phase 4 import/export system when additional features desired beyond current complete application.