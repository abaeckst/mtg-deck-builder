# MTG Deck Builder - Technical Debt Documentation

**Last Updated:** June 12, 2025  
**Repository:** https://github.com/abaeckst/mtg-deck-builder  
**Storage Location:** `C:\Users\abaec\Development\mtg-deck-builder\Documentation Library\docs\reference\`

## 🎯 Purpose & Scope

This document tracks known technical debt, architectural limitations, and areas requiring future improvement. Technical debt items are categorized by priority and system impact to guide future development decisions.

## 📊 Priority Classification

**P1 - Critical:** Affects core functionality or user experience  
**P2 - High:** Impacts maintainability or performance  
**P3 - Medium:** Architectural improvements for long-term health  
**P4 - Low:** Nice-to-have optimizations

## 🔍 Current Technical Debt Inventory

### Layout & State Management System

#### P2 - Resize Handle CSS Coordination Issues
**Issue:** CSS class vs inline style conflicts causing resize handles to be functionally unusable  
**Details:**
- CSS classes define intended 30px handle width with proper cursor styling
- Inline styles override with 6px width, making handles too small to interact with
- DevTools investigation shows elements exist in DOM but are visually/functionally inadequate
- Affects filter panel horizontal resizing and deck/sideboard vertical resizing

**Root Cause:** Inconsistent styling approach between CSS class definitions and React inline styles  
**Impact:** Resize functionality appears broken to users, poor UX for layout customization  
**Solution Path:** Systematic CSS class vs inline style coordination strategy  
**Files Affected:** `MTGOLayout.tsx`, `MTGOLayout.css`, `ResizeHandles.css`, `useResize.ts`

**Session Context:** June 12, 2025 - Investigation revealed fundamental styling conflicts, session ended with JSX syntax errors requiring git restore

#### P3 - Nuclear Z-Index Strategy
**Issue:** Extreme z-index values (500,000-2,000,000) for dropdown reliability  
**Details:** Current approach uses extremely high z-index values to ensure dropdown menus appear above all content, including resize handles  
**Impact:** Potential conflicts with future third-party components, non-systematic approach  
**Solution Path:** Implement systematic z-index management with proper layering hierarchy

#### P3 - CSS Architecture Size
**Issue:** MTGOLayout.css approaching maintainability limits at 1,450 lines  
**Details:** Single monolithic CSS file handles all layout styling with complex responsive patterns  
**Impact:** Difficult to maintain, understand, and modify styling  
**Solution Path:** Consider CSS-in-JS, CSS modules, or systematic file splitting

### Component Architecture & Integration System

#### P2 - Callback Complexity
**Issue:** 30+ callback functions create intricate dependency web  
**Details:** MTGOLayout coordinator manages complex callback patterns for cross-system communication  
**Impact:** Difficult to debug, understand data flow, and maintain integrations  
**Solution Path:** Event-driven architecture or systematic callback management patterns

#### P3 - Style Coordination Patterns
**Issue:** Lack of systematic approach for CSS class vs inline style management  
**Details:** Inconsistent patterns across components for when to use CSS classes vs inline styles  
**Impact:** Styling conflicts, maintenance difficulty, integration problems  
**Solution Path:** Establish and document consistent styling coordination patterns

### File Size & Architecture

#### P2 - Large Utility Files
**Issue:** Several files approaching or exceeding maintainability thresholds  
**Files:**
- `screenshotUtils.ts` (850 lines) - Complex mathematical optimization algorithms
- `scryfallApi.ts` (575 lines) - Complete Scryfall API abstraction
- `card.ts` (520 lines) - Foundation types and utilities

**Impact:** Difficult to maintain, understand, and modify  
**Solution Path:** Apply extraction methodology when maintenance needs arise

#### P3 - Complex Hook Patterns
**Issue:** Some hooks managing complex state and interaction patterns  
**Files:**
- `useDragAndDrop.ts` (445 lines) - Sophisticated drag & drop with timing systems
- `useSelection.ts` (310 lines) - Dual selection system coordination

**Impact:** Complex debugging, integration challenges  
**Solution Path:** Monitor for extraction opportunities as requirements evolve

## 🛠️ Systematic Debugging Methodologies

### CSS Integration Debugging
**Pattern Identified:** June 12, 2025 resize handle investigation  
**Methodology:**
1. **DOM Element Verification:** Confirm element exists in DOM with expected structure
2. **CSS Class Application:** Verify CSS classes are applied to elements
3. **Computed Style Analysis:** Check DevTools computed styles vs intended styles
4. **Visual Appearance Validation:** Confirm elements are visually present and appropriately sized
5. **Functional Interaction Testing:** Verify elements respond to user interaction
6. **Integration Impact Assessment:** Test how fixes affect cross-system functionality

### Performance Investigation
**Pattern Documented:** Search performance optimization (June 9, 2025)  
**Methodology:**
1. **Timing Analysis:** Measure actual vs expected performance
2. **Re-render Loop Detection:** Identify unnecessary component updates
3. **Hook Dependency Analysis:** Verify stable dependencies and memoization
4. **Integration Point Validation:** Test how optimizations affect system coordination

## 📈 Resolution Tracking

### Resolved Technical Debt

#### ✅ Hook Architecture Optimization (June 2025)
**Issue:** useCards monolithic hook (580 lines) with complex responsibilities  
**Solution:** Extracted 5 focused hooks + coordinator pattern  
**Result:** useCards (250 lines) + useSearch, usePagination, useCardSelection, useSearchSuggestions, useFilters  
**Impact:** Improved maintainability, clear responsibilities, better performance

#### ✅ Component Extraction Success (June 2025)
**Issue:** MTGOLayout monolithic component (925 lines)  
**Solution:** Extracted 3 area components with coordinator pattern  
**Result:** MTGOLayout (450 lines) + CollectionArea, DeckArea, SideboardArea  
**Impact:** Cleaner architecture, better maintainability, preserved functionality

#### ✅ Search Performance Optimization (June 9, 2025)
**Issue:** 2-7+ second search times despite fast API  
**Solution:** Fixed useSorting hook re-render loops  
**Result:** <1 second search response times  
**Impact:** Dramatically improved user experience

#### ✅ Load More Reliability (June 9, 2025)
**Issue:** 422 errors during pagination  
**Solution:** Stored pagination state management  
**Result:** Zero pagination errors, reliable Load More functionality  
**Impact:** Consistent user experience, no data loading failures

## 🔄 Management Process

### Adding New Technical Debt
1. **Document Issue:** Clear description of problem and impact
2. **Assign Priority:** Based on user impact and system health
3. **Identify Solution Path:** High-level approach for resolution
4. **Track Context:** Session information, investigation results, decision rationale

### Resolving Technical Debt
1. **Update Status:** Move from active to resolved section
2. **Document Solution:** Approach taken and results achieved
3. **Record Impact:** Measurable improvements and user experience changes
4. **Archive Context:** Preserve investigation and resolution details for future reference

### Regular Review Process
- **Monthly Review:** Assess priority changes based on system evolution
- **Quarterly Planning:** Select high-priority items for resolution
- **Release Planning:** Consider technical debt impact on new features
- **Post-Resolution Analysis:** Validate solutions and document lessons learned

## 📚 Related Documentation

- **System Specifications:** Reference for intended architecture and performance standards
- **Code Organization Guide:** File identification and proven patterns for resolution approaches
- **Session Logs:** Detailed investigation and resolution attempts with methodologies used
- **Strategic Archives:** Historical context and successful resolution patterns

---

**Maintenance Note:** This document should be updated as technical debt is identified, investigated, and resolved. Priority levels may change as system requirements evolve and user impact becomes clearer.