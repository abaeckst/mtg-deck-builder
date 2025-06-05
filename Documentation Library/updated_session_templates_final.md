# Development Session Templates - Issue-Driven Development

**Purpose:** Standardized templates for efficient development sessions focused on user issues  
**Goal:** Every session starts with clear objectives and ends with working, tested features  
**Current Status:** Phase 3H Complete - Ready for Issue Resolution (Phase 4A-4E)  
**Updated:** June 5, 2025 - Prioritizing user-reported critical issues  

## 🚀 Session Startup Checklist

### Every Session Begins With:
```markdown
## Session Setup (5 minutes)
- [ ] Open VS Code to project folder: `c:\Users\carol\mtg-deck-builder`
- [ ] Run `npm start` to verify project compiles and loads correctly
- [ ] Check GitHub sync status: `git status`
- [ ] Review updated_project_status.md for current state
- [ ] Confirm session goal and success criteria for issue resolution
```

### Available Session Types:
1. **Phase 4A Implementation** - Search System Overhaul (IMMEDIATE PRIORITY)
2. **Phase 4B Implementation** - Filter System Redesign (HIGH PRIORITY)
3. **Phase 4C Implementation** - Card Display & Preview System (MEDIUM PRIORITY)
4. **Phase 4D Implementation** - UI & Interaction Improvements (MEDIUM PRIORITY)
5. **Phase 4E Implementation** - Screenshot System Rebuild (LOW PRIORITY)
6. **Bug Fix & Polish** - Resolve issues and improve UX
7. **Future Enhancement** - Original Phase 5+ development (after issues resolved)

---

## 📋 Template 1: Phase 4A - Search System Overhaul (IMMEDIATE PRIORITY)

### Session Goal Template:
```markdown
# Session Goal: Phase 4A - Search System Overhaul

## Pre-Session Information Gathering
**MANDATORY FIRST STEP - Request these files:**
- [ ] `src/services/scryfallApi.ts` - Current API integration and pagination handling
- [ ] `src/hooks/useCards.ts` - Current search result management and filtering logic
- [ ] `src/components/SearchAutocomplete.tsx` - Search UI and query construction
- [ ] Current filter components - Color filter logic and behavior
- [ ] Search-related type definitions for understanding current interfaces

## Phase 4A Critical Issues to Resolve
1. **Pagination Limitation Crisis** - Only first 175 results fetched, breaking sort accuracy
2. **Multi-Word Search Failure** - Natural language search broken without quotes
3. **Multi-Color Filter Confusion** - Unclear "at most" vs "exactly" behavior
4. **Missing Gold Button** - No way to filter multicolor cards specifically

## Implementation Plan
1. **Information Analysis** (20 min)
   - Review current API pagination handling in scryfallApi.ts
   - Understand search result processing in useCards.ts
   - Analyze query construction for multi-word searches
   - Map out color filter logic and UI integration points
   
2. **API Enhancement** (90-120 min)
   - Implement complete pagination handling with progressive loading
   - Add search progress tracking and cancellation support
   - Enhance query construction for natural language phrases
   - Add rate limiting for large searches
   
3. **Search Logic Updates** (60-90 min)
   - Update useCards.ts to handle paginated results properly
   - Implement sorting across ALL fetched results (not just first page)
   - Add color filter mode handling with clear behavior
   - Integrate search progress state management
   
4. **UI Enhancements** (30-45 min)
   - Add search progress indicator for large searches
   - Create color filter mode selector with visual indicators
   - Add "gold button" for multicolor-only filtering
   - Implement search cancellation UI
   
5. **Testing & Verification** (30 min)
   - Test large searches (500+ results) with proper sorting
   - Verify multi-word search works without quotes
   - Test color filter modes with clear behavior indication
   - Verify gold button correctly filters multicolor cards only
   
6. **Documentation** (15 min)
   - Update project status with Phase 4A completion
   - Document any discovered edge cases or limitations
   - Commit and push all changes with descriptive messages

## Session Success Criteria
- [ ] Search fetches ALL matching cards regardless of quantity (handles 1000+ card results)
- [ ] Multi-word search works naturally without requiring quotes ("a killer" finds "A Killer Among Us")
- [ ] Color filters have clear "at most these colors" default with mode indicators
- [ ] Gold button correctly shows only multi-colored cards
- [ ] Large searches show progress and can be cancelled if needed
- [ ] Sorting works correctly across all fetched results, not just first page
- [ ] All existing functionality continues working without regressions
- [ ] TypeScript compilation succeeds with no errors

## Files Expected to be Modified/Created
- `src/services/scryfallApi.ts` - Complete pagination and enhanced query construction
- `src/hooks/useCards.ts` - Paginated result handling and sorting across all results
- `src/components/SearchAutocomplete.tsx` - Progress indicators and enhanced UI
- `src/components/ColorFilterMode.tsx` - New color filter mode selector (if needed)
- `src/components/GoldButton.tsx` - New multicolor filter button
- Search-related type definitions - Enhanced interfaces for pagination and progress
```

---

## 📋 Template 2: Phase 4B - Filter System Redesign (HIGH PRIORITY)

### Session Goal Template:
```markdown
# Session Goal: Phase 4B - Filter System Redesign

## Pre-Session Information Gathering
**MANDATORY FIRST STEP - Request these files:**
- [ ] `src/components/MTGOLayout.tsx` - Current filter panel integration and layout
- [ ] Current filter component files - All existing filter implementations
- [ ] `src/hooks/useCards.ts` - Current filtering logic and state management
- [ ] MTGOLayout.css or related styling - Current filter styling
- [ ] Filter-related type definitions and interfaces

## Phase 4B Critical Issues to Resolve
1. **Filter Panel Appearance** - Current panel is "ugly" and unprofessional
2. **Filter Organization** - All filters expanded, overwhelming interface
3. **Missing Subtype Filters** - No way to filter by creature types, spell types, etc.
4. **Multi-Color Gold Button** - Integration with redesigned color filters

## Implementation Plan
1. **Architecture Planning** (30 min)
   - Review current filter integration in MTGOLayout
   - Plan collapsible section architecture with state management
   - Design professional MTGO-style visual system
   - Plan subtype filter UI with autocomplete system
   
2. **Professional Filter Panel Creation** (120-150 min)
   - Create new FilterPanel component with MTGO-style design
   - Implement collapsible sections (only format/colors/type/rarity expanded by default)
   - Add professional styling with proper spacing, colors, and typography
   - Implement state persistence for section expand/collapse
   
3. **Subtype Filter System** (90-120 min)
   - Create SubtypeFilter component with autocomplete search
   - Implement grouped subtype display (Creature Types, Spell Types, etc.)
   - Add popular subtypes quick-select functionality
   - Integrate subtype filtering logic with search system
   
4. **Enhanced Color Filters** (45-60 min)
   - Redesign color filter section with professional appearance
   - Integrate gold button for multicolor-only filtering
   - Add clear visual indicators for filter behavior
   - Ensure seamless integration with Phase 4A color filter modes
   
5. **Integration & Testing** (45 min)
   - Integrate new filter panel into MTGOLayout
   - Test all filter combinations with enhanced search system
   - Verify collapsible sections work with state persistence
   - Test subtype filtering with autocomplete functionality
   
6. **Polish & Documentation** (15 min)
   - Final styling adjustments for professional appearance
   - Update project status with Phase 4B completion
   - Commit and push all changes

## Session Success Criteria
- [ ] Filter panel matches MTGO professional appearance standards exactly
- [ ] Only essential filters (format/colors/type/rarity) visible by default
- [ ] Other filters properly collapsed with smooth expand/collapse animations
- [ ] Subtype filtering works with autocomplete and intelligent grouping
- [ ] Gold button integrates seamlessly with existing color filters
- [ ] All filter combinations work correctly with enhanced search system
- [ ] Filter state persists appropriately across browser sessions
- [ ] Professional visual hierarchy and styling throughout

## Files Expected to be Modified/Created
- `src/components/FilterPanel.tsx` - New professional filter panel component
- `src/components/SubtypeFilter.tsx` - New subtype filtering with autocomplete
- `src/hooks/useFilters.ts` - Enhanced filter state management
- `src/components/MTGOLayout.tsx` - Integration of new filter panel
- Filter styling files - Professional MTGO-themed CSS system
- Filter-related type definitions - Enhanced interfaces for new functionality
```

---

## 📋 Template 3: Phase 4C - Card Display & Preview System (MEDIUM PRIORITY)

### Session Goal Template:
```markdown
# Session Goal: Phase 4C - Card Display & Preview System

## Pre-Session Information Gathering
**MANDATORY FIRST STEP - Request these files:**
- [ ] `src/components/MagicCard.tsx` - Current card display and sizing implementation
- [ ] `src/components/DraggableCard.tsx` - Card interaction patterns
- [ ] Card sizing and scaling logic - Current image handling
- [ ] Any existing preview or modal components
- [ ] Image-related utilities and type definitions

## Phase 4C Critical Issues to Resolve
1. **Low Resolution at Small Sizes** - Cards unreadable when sizing slider is low
2. **Missing Large Card Preview** - No way to examine card details without changing global slider
3. **Image Quality Investigation** - Research vector images or better scaling algorithms

## Implementation Plan
1. **Image Quality Investigation** (45-60 min)
   - Research vector image alternatives for Magic cards
   - Test different scaling algorithms for small size readability
   - Investigate high-resolution image sources and formats
   - Determine feasibility of vector implementation vs. improved scaling
   
2. **Card Preview System Creation** (120-150 min)
   - Create CardPreview component with high-resolution display
   - Implement smart positioning logic to avoid screen edges
   - Add hover preview with proper timing and positioning
   - Implement click-to-pin functionality for detailed examination
   
3. **MagicCard Enhancement** (60-90 min)
   - Integrate preview trigger with hover and click events
   - Implement improved scaling algorithms for better small-size readability
   - Add high-resolution image loading with fallback options
   - Optimize image handling across all scale factors
   
4. **Preview Integration** (45-60 min)
   - Create useCardPreview hook for state management
   - Integrate preview system with all view modes (card, pile, list)
   - Add keyboard navigation support (arrow keys, escape)
   - Ensure mobile-friendly preview behavior
   
5. **Testing & Optimization** (30 min)
   - Test card readability at all scale factors
   - Verify preview positioning works correctly across screen sizes
   - Test preview system in all view modes
   - Verify high-resolution images load efficiently
   
6. **Documentation** (15 min)
   - Update project status with Phase 4C completion
   - Document image quality improvements and preview functionality
   - Commit and push all changes

## Session Success Criteria
- [ ] Cards remain readable and crisp at all scale factors (down to smallest size)
- [ ] Large preview appears on hover with proper positioning (never off-screen)
- [ ] Click-to-pin preview works for detailed card examination
- [ ] Preview system works seamlessly in all view modes (card, pile, list)
- [ ] High-resolution images load efficiently without performance impact
- [ ] Vector images implemented if feasible for significant quality improvement
- [ ] Keyboard navigation works for preview system
- [ ] Mobile-friendly preview behavior on touch devices

## Files Expected to be Modified/Created
- `src/components/CardPreview.tsx` - New large card preview component
- `src/hooks/useCardPreview.ts` - Preview state management and positioning
- `src/components/MagicCard.tsx` - Preview integration and improved scaling
- `src/utils/imageUtils.ts` - Enhanced image loading and scaling utilities
- Image quality utilities - Vector investigation and scaling optimization
- Preview-related type definitions - Interfaces for preview system
```

---

## 📋 Template 4: Phase 4D - UI & Interaction Improvements (MEDIUM PRIORITY)

### Session Goal Template:
```markdown
# Session Goal: Phase 4D - UI & Interaction Improvements

## Pre-Session Information Gathering
**MANDATORY FIRST STEP - Request these files:**
- [ ] `src/components/DraggableCard.tsx` - Current right-click and drag implementation
- [ ] `src/hooks/useContextMenu.ts` - Context menu behavior and integration
- [ ] `src/hooks/useSelection.ts` - Selection state management
- [ ] `src/hooks/useDragAndDrop.ts` - Current drag preview positioning and visual feedback
- [ ] Drag-related styling and visual feedback components

## Phase 4D Critical Issues to Resolve
1. **Right-Click Context Menu Selection** - Right-click doesn't select clicked card first
2. **Drag Preview Distance** - Preview appears too far from cursor
3. **Drag Visual Feedback** - Unwanted visual feedback on zones during drag operations

## Implementation Plan
1. **Right-Click Selection Integration** (30-45 min)
   - Modify DraggableCard to select card on right-click before showing context menu
   - Coordinate selection timing with context menu display
   - Maintain proper multi-selection behavior when appropriate
   - Test selection integration across all areas (collection, deck, sideboard)
   
2. **Drag Preview Positioning** (45-60 min)
   - Adjust drag preview positioning to appear close to cursor (5-10 pixels)
   - Modify useDragAndDrop hook for better cursor tracking
   - Test drag preview positioning across different screen sizes
   - Ensure drag preview remains visible and doesn't interfere with dropping
   
3. **Drag Visual Feedback Elimination** (30-45 min)
   - Remove visual feedback on existing zones during drag operations
   - Eliminate drop validation visual feedback per user request
   - Simplify drag experience with minimal visual distractions
   - Maintain drag functionality while removing unwanted feedback
   
4. **Selection Coordination** (30 min)
   - Update useContextMenu to coordinate with selection system
   - Ensure proper card selection state before menu display
   - Test multi-selection preservation during right-click operations
   - Verify selection behavior consistency across all interaction modes
   
5. **Testing & Polish** (30 min)
   - Test right-click selection across all view modes
   - Verify drag preview positioning feels natural and responsive
   - Confirm elimination of unwanted visual feedback during drag
   - Test all interaction combinations for smooth user experience
   
6. **Documentation** (15 min)
   - Update project status with Phase 4D completion
   - Document interaction improvements and behavior changes
   - Commit and push all changes

## Session Success Criteria
- [ ] Right-click automatically selects clicked card before showing context menu
- [ ] Drag preview appears very close to cursor (within 5-10 pixels)
- [ ] No visual changes occur to zones during drag operations
- [ ] No drop validation feedback shown during drag (cleaner experience)
- [ ] Multi-selection behavior preserved when appropriate
- [ ] All drag interactions feel smooth, responsive, and intuitive
- [ ] Selection behavior consistent across all view modes and areas

## Files Expected to be Modified/Created
- `src/components/DraggableCard.tsx` - Right-click selection integration
- `src/hooks/useContextMenu.ts` - Selection coordination with context menu
- `src/hooks/useDragAndDrop.ts` - Improved drag preview positioning
- `src/hooks/useSelection.ts` - Enhanced selection coordination if needed
- Drag styling components - Removal of unwanted visual feedback
```

---

## 📋 Template 5: Phase 4E - Screenshot System Rebuild (LOW PRIORITY)

### Session Goal Template:
```markdown
# Session Goal: Phase 4E - Screenshot System Rebuild

## Pre-Session Information Gathering
**MANDATORY FIRST STEP - Request these files:**
- [ ] `src/components/ScreenshotModal.tsx` - Current screenshot modal implementation
- [ ] `src/utils/screenshotUtils.ts` - Current screenshot generation utilities
- [ ] Screenshot-related type definitions and interfaces
- [ ] Any existing image generation or canvas utilities
- [ ] Current screenshot generation workflow and error handling

## Phase 4E Critical Issues to Resolve
1. **Screenshot System Robustness** - More reliable image generation across browsers
2. **Enhanced Generation Options** - Multiple layouts and quality settings
3. **Better User Experience** - Progress indication and error handling

## Implementation Plan
1. **Current System Analysis** (30 min)
   - Review existing screenshot generation approach
   - Identify reliability issues and browser compatibility problems
   - Analyze current error handling and user feedback
   - Plan multiple generation strategies for better reliability
   
2. **Enhanced Generation System** (120-150 min)
   - Implement multiple generation strategies for cross-browser reliability
   - Add comprehensive error handling with fallback options
   - Create progress tracking and cancellation support
   - Optimize generation performance for large decks
   
3. **Improved User Interface** (60-90 min)
   - Enhance ScreenshotModal with progress indication
   - Add multiple layout options for different sharing needs
   - Implement quality settings and format options
   - Add better error messages and user guidance
   
4. **Generation Options** (45-60 min)
   - Add multiple screenshot layouts (compact, detailed, custom)
   - Implement quality and resolution settings
   - Add metadata inclusion options
   - Create export format options (PNG, JPG, WebP)
   
5. **Testing & Reliability** (45 min)
   - Test screenshot generation across different browsers
   - Verify generation works with various deck sizes
   - Test error handling and fallback scenarios
   - Verify progress indication and cancellation functionality
   
6. **Documentation** (15 min)
   - Update project status with Phase 4E completion
   - Document screenshot system improvements and options
   - Commit and push all changes

## Session Success Criteria
- [ ] Screenshot generation works reliably across all major browsers
- [ ] Multiple layout and quality options available for different use cases
- [ ] Progress indication during generation with cancellation option
- [ ] Clear error handling with user-friendly error messages
- [ ] Fast generation times even for large decks (60+ cards)
- [ ] Multiple export formats and quality settings work correctly
- [ ] Improved user experience with better feedback and guidance

## Files Expected to be Modified/Created
- `src/components/ScreenshotModal.tsx` - Enhanced UI with options and progress
- `src/utils/screenshotUtils.ts` - Robust generation with multiple strategies
- Screenshot generation utilities - Enhanced reliability and browser compatibility
- Progress and error handling components
- Screenshot-related type definitions - Enhanced interfaces for new options
```

---

## 🧹 Template 6: Bug Fix & Polish Session (AVAILABLE ANYTIME)

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

---

## 📋 Template 7: Future Enhancement Session (AFTER ISSUES RESOLVED)

### Session Goal Template:
```markdown
# Session Goal: [Original Phase 5+ Development]

**Note:** This template applies to original enhancement roadmap AFTER Phase 4A-4E issues are resolved

## Pre-Session Information Gathering
**MANDATORY FIRST STEP - Request these files:**
- [ ] Current implementation files for integration
- [ ] Existing patterns to follow for consistency
- [ ] Type definitions to extend properly
- [ ] State management patterns to enhance

## Implementation Plan
[Use original phase templates from archived documentation]

## Session Success Criteria
[Based on original enhancement goals]
```

---

## 🎯 Session Completion Templates

### End-of-Session Checklist:
```markdown
## Session Wrap-Up (10 minutes)
- [ ] All new code compiles without TypeScript errors
- [ ] Run `npm start` - application loads and all features work
- [ ] Test complete user workflow end-to-end for affected areas
- [ ] Verify no regressions in existing functionality  
- [ ] Update updated_project_status.md with progress
- [ ] Commit changes: `git add . && git commit -m "[descriptive message]"`
- [ ] Push to GitHub: `git push origin main`
- [ ] Document any issues or next steps discovered
```

### Session Summary Template:
```markdown
## Session Summary: [Date] - [Phase/Goal]

### Issues Resolved:
- ✅ [Specific user issue] - [How it was resolved]
- ✅ [Performance improvement] - [What was optimized]

### Files Modified/Created:
- `src/[path]/[filename]` - [description of changes]
- `src/[path]/[filename]` - [description of changes]

### User Experience Improvements:
- [Specific workflow improvement] - [User benefit]
- [Interface enhancement] - [Usability improvement]

### Current Status:
- **Phase:** [Current phase status after session]
- **Working Features:** [Confirmed functional features]
- **Next Priority:** [Recommended next session focus]

### Notes for Next Session:
- [Important insights or reminders]
- [Opportunities identified for future work]
- [Any user feedback or observations]
```

---

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

### Phase 4A Session (READY FOR IMMEDIATE START):
```markdown
Goal: Search System Overhaul - Fix critical pagination and multi-word search issues
Files needed first: scryfallApi.ts, useCards.ts, SearchAutocomplete.tsx
Time estimate: 6-8 hours (3-4 sessions)
Success: All cards fetchable, natural language search, clear color filter behavior
User Impact: HIGH - Fixes workflow-breaking search limitations
```

### Phase 4B Session (AFTER 4A):
```markdown
Goal: Filter System Redesign - Professional MTGO appearance with enhanced functionality
Requirements: Phase 4A completion (search system working properly)
Features: Professional styling, collapsible sections, subtype filters, gold button
```

### Phase 4C Session (AFTER 4B):
```markdown
Goal: Card Display & Preview System - Improve readability and add large previews
Requirements: Phase 4B completion (professional filter system)
Features: Better scaling, large card preview, high-resolution images
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

### User Issue Resolution Focus:
- Prioritize workflow-breaking issues first (search, filters)
- Test solutions with real user scenarios
- Verify improvements actually enhance user experience
- Document user feedback and iterate based on usage

---

**Usage Instructions:**
1. **Start each session** by choosing template based on priority (4A → 4B → 4C → 4D → 4E)
2. **Follow information-gathering step** - Critical for integration success
3. **Use appropriate file update method** - Script for large files, complete for small/new files
4. **Complete wrap-up steps** before ending any session
5. **Update master status** to reflect actual completion state

**Current Priority:** Phase 4A (Search System Overhaul) ready for immediate implementation  
**User Impact:** Directly resolves most critical workflow issues affecting daily usage