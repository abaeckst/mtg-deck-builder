# MTG Deck Builder - Code Organization Guide

**Created:** June 7, 2025 | **Performance Optimized:** June 9, 2025 | **Enhanced:** June 12, 2025 | **3D Integration:** January 13, 2025 | **Progressive Loading:** January 14, 2025  
**Purpose:** Streamlined reference for codebase organization, integration points, proven development patterns, 3D animation architecture, progressive loading system, and technical debt awareness  
**Repository:** https://github.com/abaeckst/mtg-deck-builder  

## 🎯 Quick Reference - Development Decision Tree

### Adding Search Features
**Spec:** Request Search & Filtering System specification for design intent and performance standards  
**Files:** `useSearch.ts` (extracted hook + performance optimized) → `scryfallApi.ts` (API + Load More) → `SearchAutocomplete.tsx` → `search.ts` (types)  
**Pattern:** API changes → useSearch updates → useCards coordination → component integration  
**Performance:** Apply timing analysis, clean parameter management, wildcard optimization

### Adding Filter Features  
**Spec:** Request Search & Filtering System specification for coordination patterns and UX standards  
**Files:** `useFilters.ts` (excellent example) → `FilterPanel.tsx` → `CollapsibleSection.tsx` → `scryfallApi.ts`  
**Pattern:** Filter state → UI components → API integration → useCards coordination  
**Reactivity:** Clean search triggers on filter changes

### Adding Card Display Features
**Spec:** Request Card Display & Loading System specification for progressive loading, display standards, and 3D flip integration  
**Files:** `MagicCard.tsx` (base + LazyImage integration) → `FlipCard.tsx` (3D animation wrapper) → `LazyImage.tsx` (progressive loading) → `DraggableCard.tsx` (enhanced UX) → `card.ts` (types)  
**Pattern:** Base component → LazyImage progressive loading → 3D animation wrapper (conditional) → interactive wrapper → type support  
**Performance:** Intersection Observer, viewport-based progressive loading, 3x preview scaling, hardware-accelerated 3D transforms  
**3D Integration:** FlipCard wrapper for double-faced cards with container stabilization and event isolation

### Adding Progressive Loading Features
**Spec:** Request Card Display & Loading System specification for progressive loading patterns and performance optimization  
**Files:** `LazyImage.tsx` (Intersection Observer) → `MagicCard.tsx` (integration) → view components (coordination) → `card.ts` (utilities)  
**Pattern:** LazyImage component → viewport detection → progressive rendering → performance optimization  
**Performance:** Viewport-based loading, 50px rootMargin, crisp-edges rendering, loading states

### Adding Pagination Features
**Spec:** Request Search & Filtering System specification for pagination coordination patterns  
**Files:** `usePagination.ts` (extracted) → `useSearch.ts` (state coordination) → `scryfallApi.ts` (422 prevention)  
**Pattern:** Pagination state → search coordination → API decision logic  
**Performance:** Stored pagination state, Smart Card Append for scroll preservation

### Adding Hook Features
**Files:** Review `useCards.ts` (250 lines coordinator) → assess if new hook needed → extract if growing large  
**Pattern:** Assess responsibility → extract focused hooks → maintain clean APIs  
**Performance:** Monitor re-render loops, stable dependencies, proper memoization

### Adding Layout/State Features
**Spec:** Request Layout & State Management System specification for unified state patterns and responsive design  
**Files:** `useLayout.ts` (unified state) → `DeckArea.tsx`/`SideboardArea.tsx` → `MTGOLayout.tsx` (coordinator)  
**Pattern:** Single state source → component synchronization → coordinator integration  
**Advanced:** Automatic migration, constraint systems, responsive overflow  
**Technical Debt:** CSS coordination patterns established, resize handle coordination functional

### Adding Export Features
**Spec:** Request Export & Formatting System specification for format standards and quality requirements  
**Files:** `deckFormatting.ts` → `screenshotUtils.ts` (850 lines - complex) → modal components  
**Pattern:** Utility functions → modal components → main layout integration

### Adding Drag & Drop Features
**Spec:** Request Drag & Drop System specification for visual feedback standards and interaction patterns  
**Files:** `useDragAndDrop.ts` (445 lines - complex) → `DraggableCard.tsx` → `DropZone.tsx`  
**Pattern:** Drag logic → card behavior → drop targets  
**Enhanced:** 3x transform scaling, zone-relative centering, component isolation  
**3D Integration:** FlipCard coordination with drag system through advanced event handling

### Adding 3D Animation Features
**Spec:** Request Card Display & Loading System specification for 3D animation standards and integration patterns  
**Files:** `FlipCard.tsx` (3D wrapper) → `MagicCard.tsx` (display) → `card.ts` (utilities) → `DraggableCard.tsx` (integration)  
**Pattern:** Double-faced detection → 3D animation wrapper → face-specific rendering → interaction coordination  
**Performance:** Hardware acceleration, 60fps animations, container stabilization for CSS Grid compatibility  
**Integration:** Event isolation, state preservation, seamless coordination with existing systems

### Adding CSS/Styling Features
**Spec:** Request CSS Architecture & Styling System specification for coordination patterns and professional standards  
**Files:** Target component CSS files → `MTGOLayout.css` (foundation) → `CSSVariables.css` → `useResize.ts` (coordination)  
**Pattern:** Component-specific styling → foundation integration → JavaScript coordination → clean separation  
**Coordination:** CSS classes for static styling, JavaScript for dynamic values, established separation patterns

### Adding Performance Optimization Features
**Spec:** Request relevant system specification for performance context and optimization patterns  
**Files:** Target component → performance analysis → optimization implementation → validation  
**Pattern:** Timing analysis → bottleneck identification → systematic optimization → performance validation  
**Examples:** LazyImage progressive loading, ViewModeDropdown React.memo, device detection throttling, re-render elimination

### Debugging Visual/Functional Integration Issues
**Spec:** Request relevant system specifications for debugging methodologies and technical context  
**Files:** Target components → DevTools investigation → CSS coordination analysis  
**Pattern:** Systematic DOM investigation → style conflict detection → cross-system impact analysis  
**3D Debugging:** Hardware acceleration verification, transform calculation analysis, positioning context validation  
**CSS Coordination:** Clean separation patterns, avoid conflicts, systematic resolution approaches  
**Methodology:** Element existence → CSS class application → computed styles → visual appearance → functional behavior

## 📁 Complete File Organization Matrix

### 🎨 Components Layer (`src/components/`) - 22 Files

#### Core Layout (Extracted Architecture)
| File | Size | Responsibility | Status | Technical Debt |
|------|------|----------------|--------|----------------|
| `MTGOLayout.tsx` | 450 lines | **Simplified coordinator** (refactored from 925) | ✅ Excellent | Clean CSS coordination |
| `MTGOLayout.css` | 1,450 lines | **Complete styling foundation** | ✅ Working | P3 - Size approaching maintainability limits |
| `CollectionArea.tsx` | ~200 lines | Collection logic + Load More (extracted) | ✅ Good | - |
| `DeckArea.tsx` | ~200 lines | Unified controls + responsive overflow (extracted) | ✅ Good | - |
| `SideboardArea.tsx` | ~200 lines | Simplified header + unified state (extracted) | ✅ Excellent | - |
| `FilterPanel.tsx` | 368 lines | Professional filter interface | ✅ Good | - |
| `AdaptiveHeader.tsx` | 201 lines | Responsive header controls | ✅ Excellent | - |
| `CollapsibleSection.tsx` | 52 lines | Reusable collapsible UI | ✅ Excellent | - |

#### Card Display & Progressive Loading (Performance Enhanced + 3D Integration)
| File | Size | Responsibility | Status | Technical Debt |
|------|------|----------------|--------|----------------|
| `MagicCard.tsx` | 312 lines | Base card display + LazyImage integration | ✅ Enhanced | - |
| `LazyImage.tsx` | ~100 lines | **Progressive loading with Intersection Observer** (new) | ✅ Excellent | - |
| `FlipCard.tsx` | ~350 lines | **3D flip animation wrapper** (new) | ✅ Excellent | - |
| `DraggableCard.tsx` | 276 lines | Interactive cards + 3x preview + FlipCard integration | ✅ Enhanced | - |
| `ListView.tsx` | 318 lines | Universal tabular view | ✅ Good | - |
| `PileView.tsx` | 289 lines | MTGO-style pile organization | ✅ Good | - |
| `PileColumn.tsx` | 156 lines | Individual pile column | ✅ Good | - |

#### Advanced UI Components
| File | Size | Responsibility | Status | Technical Debt |
|------|------|----------------|--------|----------------|
| `ViewModeDropdown.tsx` | ~150 lines | Context-aware MTGO dropdown + React.memo optimization | ✅ Excellent | Nuclear z-index strategy |
| `DropZone.tsx` | 203 lines | Enhanced drop zones + centered feedback | ✅ Enhanced | - |
| `DragPreview.tsx` | 84 lines | 3x larger visual drag preview | ✅ Enhanced | - |
| `SearchAutocomplete.tsx` | 114 lines | Enhanced search input | ✅ Good | - |
| `SubtypeInput.tsx` | 191 lines | Autocomplete multi-select | ✅ Good | - |

### 🔧 Hooks Layer (`src/hooks/`) - 11 Files

#### Core Data Management (Refactored + Performance Optimized)
| File | Size | Responsibility | Status | Technical Debt |
|------|------|----------------|--------|----------------|
| `useCards.ts` | 250 lines | **Coordination hub** (refactored from 580) | ✅ Excellent | - |
| `useSearch.ts` | 350 lines | Core search + API + stored state | ✅ Enhanced | - |
| `usePagination.ts` | 120 lines | Progressive loading (extracted) | ✅ Excellent | - |
| `useCardSelection.ts` | 50 lines | Selection state (extracted) | ✅ Excellent | - |
| `useSearchSuggestions.ts` | 70 lines | Autocomplete + history (extracted) | ✅ Excellent | - |
| `useFilters.ts` | 120 lines | Filter state (pre-existing excellent example) | ✅ Excellent | - |

#### UI State Management
| File | Size | Responsibility | Status | Technical Debt |
|------|------|----------------|--------|----------------|
| `useLayout.ts` | 305 lines | Unified deck/sideboard state | ✅ Enhanced | Clean CSS coordination |
| `useSelection.ts` | 310 lines | Dual selection system | ⚠️ Complex | P3 - Complex hook pattern |
| `useDragAndDrop.ts` | 445 lines | Complete drag & drop | ⚠️ Very Complex | P3 - Complex hook pattern |
| `useSorting.ts` | 270 lines | **Sorting + performance optimized** | ✅ Enhanced | - |
| `useContextMenu.ts` | 165 lines | Context menu state | ✅ Good | - |

### 🛠️ Services & Utils Layer - 8 Files

| File | Size | Responsibility | Status | Technical Debt |
|------|------|----------------|--------|----------------|
| `scryfallApi.ts` | 575 lines | **Complete Scryfall abstraction + Load More** | ✅ Enhanced | P2 - Size for future extraction |
| `deckFormatting.ts` | 180 lines | Deck export utilities | ✅ Good | - |
| `screenshotUtils.ts` | 850 lines | Advanced screenshot generation | ⚠️ Extremely Complex | P2 - Large utility file |
| `deviceDetection.ts` | 145 lines | **Device capability detection + throttled** | ✅ Enhanced | - |
| `card.ts` | 520 lines | **Foundation types + 3D utilities** | ✅ Enhanced | P2 - Size for future extraction |
| `search.ts` | 120 lines | Enhanced search types | ✅ Good | - |

### 🎨 CSS & Styling Layer (`src/components/`) - 8 Files ✅ COORDINATION RESOLVED

| File | Size | Responsibility | Status | Technical Debt |
|------|------|----------------|--------|----------------|
| `MTGOLayout.css` | 1,450 lines | **Complete styling foundation** | ✅ Working | P3 - Size for modularization |
| `ResizeHandles.css` | ~60 lines | **Resize handle styling** (completed) | ✅ Complete | - |
| `PanelResizing.css` | ~50 lines | **Clean behavioral coordination** | ✅ Enhanced | - |
| `CSSVariables.css` | ~20 lines | CSS custom property definitions | ✅ Good | - |
| `FilterPanel.css` | 368 lines | Professional filter styling | ✅ Good | - |
| `modal.css` | 180 lines | Modal system styling | ✅ Good | - |
| `ComponentStyles.css` | 120 lines | Professional component patterns | ✅ Good | - |
| `ResponsiveDesign.css` | 80 lines | Extracted responsive patterns | ✅ Good | - |

## 🔗 Critical Integration Points

### Primary Data Flow (Performance Optimized)
```
Search Input → useCards (coordinator) → useSearch (clean params) → scryfallApi (wildcard opt) → API
     ↓
API Response → useSearch (stored state) → useCards → Components (Smart Card Append)
     ↓
Progressive Loading → LazyImage (Intersection Observer) → Viewport detection → Image loading
     ↓
Filter Changes → useCards (clean triggers) → useSearch (fresh params) → <1 second response
     ↓
Load More → usePagination → useSearch (stored state) → scryfallApi (422 prevention) → Success
```

### Enhanced Progressive Loading Flow
```
Card Rendering → LazyImage component → Intersection Observer (50px rootMargin) → Viewport detection
     ↓
Image entering viewport → Progressive loading trigger → onLoad/onError coordination → Loading states
     ↓
Performance optimization → Crisp-edges rendering → Memory efficient loading → Smooth scrolling
     ↓
View coordination → Grid/pile/list display → Responsive loading → Professional UX
```

### Enhanced 3D Card Display Flow
```
Card Rendering → isDoubleFacedCard() detection → Conditional FlipCard wrapper → MagicCard display
     ↓
Double-Faced Card → Professional flip button (↻) → 3D animation (400ms) → Face-specific image
     ↓
Event Isolation → stopPropagation() → Preserves drag/selection → Hardware acceleration (60fps)
     ↓
CSS Grid → Container stabilization → Reliable positioning → Professional integration
```

### Clean CSS/JavaScript Coordination Flow ✅ RESOLVED
```
Static Styling → CSS classes (ResizeHandles.css, PanelResizing.css) → Foundation patterns
     ↓
Dynamic Values → JavaScript (useResize.ts) → CSS custom properties → Real-time updates
     ↓
Clean Separation → No conflicts → Maintainable architecture → Professional functionality
```

### Key Coordination Patterns

**useCards Hub (250 lines):**
- Coordinates 5 extracted hooks: useSearch, usePagination, useCardSelection, useSearchSuggestions, useFilters
- Clean parameter management prevents search accumulation
- Performance optimized through stable hook dependencies

**useSearch Enhanced (350 lines):**
- Stored pagination state for Load More 422 prevention
- Clean parameter coordination with useCards
- Wildcard optimization with scryfallApi

**LazyImage Integration (100 lines):**
- Intersection Observer with 0.1 threshold and 50px rootMargin
- Progressive loading states (Preparing → Loading → Loaded/Error)
- Performance optimization with crisp-edges rendering
- Professional integration with MagicCard component

**FlipCard Integration (~350 lines):**
- Conditional rendering for double-faced cards only
- 3D animation with hardware acceleration and perspective
- Container stabilization for CSS Grid compatibility
- Advanced event isolation preventing interaction conflicts
- Face-specific image resolution with `getCardFaceImageUri()`

**useLayout Unified (305 lines):**
- Single state controlling deck + sideboard
- Automatic legacy state migration
- Constraint systems for different contexts
- **Clean CSS Coordination:** Established patterns with useResize.ts

**MTGOLayout Simplified (450 lines):**
- Orchestrates extracted area components
- Clean hook integration patterns
- Responsive design coordination
- **CSS Coordination:** Clean separation with styling layers

## 🚀 Performance Optimization Patterns

### Progressive Loading Performance (January 14, 2025) ✅ IMPLEMENTED
**Problem:** 75+ cards loading images simultaneously causing performance degradation  
**Solution:** LazyImage component with Intersection Observer  
**Pattern:** Viewport detection → progressive loading → smooth scrolling → memory efficiency

### ViewModeDropdown Optimization (January 14, 2025) ✅ IMPLEMENTED
**Problem:** Render storms during search operations interfering with performance  
**Solution:** React.memo wrapper optimization  
**Pattern:** Component memoization → render elimination → clean performance → professional UX

### Search Performance (Proven Effective)
**Problem:** 2-7+ second searches despite fast API  
**Solution:** Hook re-render loop elimination in useSorting  
**Pattern:** Timing analysis → stable dependencies → memoized returns → <1 second response

### Device Detection Optimization (January 13, 2025)
**Problem:** Hundreds of re-renders during resize operations  
**Solution:** 250ms throttling + change detection  
**Pattern:** Throttle function → change detection → 95% re-render reduction → smooth performance

### Load More Reliability (Comprehensive Fix)
**Problem:** 422 errors during pagination  
**Solution:** Stored pagination state management  
**Pattern:** Store full page data → comprehensive decision logic → use stored vs fetch → zero errors

### 3D Animation Performance (Hardware Acceleration)
**Problem:** Smooth 60fps 3D card flip animations  
**Solution:** Hardware acceleration with proper optimization  
**Pattern:** `will-change: transform` → GPU rendering → 3D perspective → 400ms smooth rotation

### API Efficiency (Wildcard Optimization)
**Problem:** Expensive enhancement for simple queries  
**Solution:** Early wildcard detection in scryfallApi  
**Pattern:** Query analysis → bypass enhancement → let Scryfall handle efficiently

### CSS Coordination Optimization (January 14, 2025) ✅ RESOLVED
**Problem:** CSS class vs inline style conflicts causing resize handle issues  
**Solution:** Clean separation patterns with systematic resolution  
**Pattern:** CSS foundation → JavaScript dynamics → clean coordination → conflict prevention

## ⚠️ Current Technical Debt & Refactoring Priorities

### Priority 1 (Critical)
*No P1 items currently - all critical functionality working including progressive loading and CSS coordination*

### Priority 2 (High)
1. **Large Utility Files** - scryfallApi.ts (575 lines), card.ts (520 lines), screenshotUtils.ts (850 lines)
2. **Callback Complexity** - 30+ callbacks in MTGOLayout requiring systematic management

### Priority 3 (Medium)
3. **Nuclear Z-Index Strategy** - Extreme values (2,000,000) need systematic approach
4. **CSS Architecture Size** - MTGOLayout.css (1,450 lines) approaching maintainability limits
5. **Complex Hook Patterns** - useDragAndDrop (445 lines), useSelection (310 lines)

### Priority 4 (Low)
6. **Style Coordination Patterns** - Continue establishing consistent CSS class vs inline style management
7. **3D Animation Browser Compatibility** - Enhanced fallback support for older browsers

### Technical Debt Resolution Examples ✅ MAJOR PROGRESS
- **✅ CSS Coordination Conflicts Resolution:** Systematic approach with clean CSS/JavaScript separation patterns
- **✅ Progressive Loading Implementation:** LazyImage system eliminating simultaneous loading performance issues
- **✅ ViewModeDropdown Performance:** React.memo optimization eliminating render storms
- **✅ Hook Extraction Success:** useCards (580→250) + 5 focused hooks
- **✅ Component Extraction Success:** MTGOLayout (925→450) + 3 area components  
- **✅ Performance Optimization Success:** useSorting re-render elimination, device detection throttling, progressive loading
- **✅ State Management Success:** useLayout unified deck/sideboard with migration
- **✅ 3D Integration Success:** FlipCard component with CSS Grid compatibility
- **✅ CSS Positioning Solutions:** Container stabilization patterns for absolute positioning reliability

## 🔍 Debugging Methodologies

### Visual/Functional Integration Issues
**Pattern:** Systematic DOM investigation from resize handle debugging (June 12, 2025) + CSS Grid positioning (January 13, 2025) + CSS coordination resolution (January 14, 2025)  
**Workflow:**
1. **Element Existence:** Verify DOM element exists with expected structure
2. **CSS Class Application:** Confirm CSS classes are applied correctly  
3. **Computed Style Analysis:** Use DevTools to check computed vs intended styles
4. **Visual Appearance:** Validate elements are visually present and appropriately sized
5. **Functional Interaction:** Test elements respond to user interaction properly
6. **Integration Impact:** Assess how fixes affect cross-system functionality

### CSS Coordination Debugging ✅ ENHANCED PATTERNS
**Pattern:** Clean CSS/JavaScript separation debugging with systematic conflict resolution  
**Workflow:**
1. **Separation Verification:** Check CSS foundation vs JavaScript dynamics
2. **Coordination Analysis:** Verify CSS custom property integration
3. **Conflict Detection:** Identify style conflicts and resolution patterns
4. **Clean Pattern Application:** Apply established coordination approaches
5. **Performance Impact:** Assess coordination efficiency and optimization
6. **Systematic Resolution:** Apply proven conflict resolution methodologies

### Progressive Loading Debugging ✅ NEW
**Pattern:** LazyImage performance and viewport detection debugging  
**Workflow:**
1. **Intersection Observer Verification:** Check viewport detection accuracy
2. **Loading State Analysis:** Verify progressive loading state transitions
3. **Performance Monitoring:** Assess memory usage and loading efficiency
4. **Viewport Coordination:** Test responsive loading across different screen sizes
5. **Error Handling:** Validate fallback patterns and error states
6. **Integration Testing:** Confirm coordination with other display systems

### 3D Animation Debugging (January 13, 2025)
**Pattern:** Hardware acceleration and positioning context debugging methodology  
**Workflow:**
1. **Hardware Acceleration Verification:** Check `will-change` and GPU rendering
2. **Transform Calculation Analysis:** Verify 3D transform values and perspective
3. **Positioning Context Validation:** Ensure container stabilization is working
4. **Event Isolation Testing:** Confirm stopPropagation() prevents conflicts
5. **Performance Monitoring:** Verify 60fps animation performance
6. **Cross-System Integration:** Test interaction with drag/selection/context systems

### Performance Investigation
**Pattern:** Search performance optimization methodology (June 9, 2025) + device detection throttling (January 13, 2025) + progressive loading optimization (January 14, 2025)  
**Workflow:**
1. **Timing Analysis:** Measure actual vs expected performance
2. **Re-render Loop Detection:** Identify unnecessary component updates
3. **Hook Dependency Analysis:** Verify stable dependencies and memoization
4. **Progressive Loading Assessment:** Evaluate viewport-based loading efficiency
5. **Throttling Implementation:** Apply rate limiting for performance-sensitive operations
6. **Integration Point Validation:** Test optimizations don't break system coordination

## 📚 Quick Reference Cards

### "Add progressive image loading"
**Spec:** Request Card Display & Loading System specification for progressive loading patterns  
**Files:** `LazyImage.tsx` (Intersection Observer component) → `MagicCard.tsx` (integration) → view components  
**Pattern:** Viewport detection → progressive loading → performance optimization → professional UX

### "Debug visual/functional integration issues"
**Spec:** Request relevant system specification for debugging context  
**Files:** Target components → DevTools analysis → CSS coordination  
**Pattern:** Systematic DOM investigation → style conflict detection → cross-system impact analysis
**3D Focus:** Hardware acceleration verification → positioning context validation → event isolation testing

### "Resolve CSS coordination issues"  
**Spec:** Request Layout & State Management System or CSS Architecture specifications  
**Files:** CSS files → component implementation → JavaScript coordination  
**Pattern:** Clean separation analysis → systematic coordination approach → conflict resolution

### "Fix CSS Grid positioning issues"
**Spec:** Request Component Architecture & Integration System specification for CSS Grid solutions  
**Files:** Target component → CSS analysis → container context  
**Pattern:** Coordinate system analysis → container stabilization → explicit dimensions → positioning reliability

### "Optimize component performance"
**Spec:** Request relevant system specification for performance context  
**Files:** Target component → performance analysis → optimization implementation  
**Pattern:** Performance profiling → React.memo/memoization → re-render elimination → validation

### "Optimize search performance"
**Spec:** Request Search & Filtering System specification for performance standards  
**Files:** `useSorting.ts` → `useSearch.ts` → `useCards.ts`  
**Pattern:** Timing analysis → fix re-render loops → stable dependencies → memoization

### "Fix device detection performance"
**Spec:** Request Component Architecture specification for integration debugging  
**Files:** `deviceDetection.ts` → `ViewModeDropdown.tsx` → components using device detection  
**Pattern:** Throttling implementation → change detection → re-render reduction → smooth performance

### "Fix Load More issues"  
**Spec:** Request Search & Filtering System specification for pagination patterns  
**Files:** `useSearch.ts` → `scryfallApi.ts` → `usePagination.ts`  
**Pattern:** Store pagination state → decision logic → use stored data → prevent 422 errors

### "Add 3D card flip functionality"
**Spec:** Request Card Display & Loading System specification for 3D animation standards  
**Files:** `FlipCard.tsx` (new) → `MagicCard.tsx` → `DraggableCard.tsx` → `card.ts`  
**Pattern:** Double-faced detection → 3D wrapper component → hardware acceleration → event isolation → CSS Grid compatibility

### "Extract large component"
**Files:** Target component → create focused components → coordinator pattern  
**Pattern:** Identify areas → extract components → implement coordinator → zero regressions  
**Success:** MTGOLayout (925→450) + CollectionArea + DeckArea + SideboardArea

### "Add unified state management"
**Spec:** Request Layout & State Management System specification for state patterns  
**Files:** `useLayout.ts` → `DeckArea.tsx` → `SideboardArea.tsx`  
**Pattern:** Single state source → coordination functions → component sync → migration support

### "Apply responsive design"
**Spec:** Request Layout & State Management System specification for responsive patterns  
**Files:** `DeckArea.tsx` → `ViewModeDropdown.tsx` → `MTGOLayout.css`  
**Pattern:** Priority ordering → space detection → dynamic hiding → overflow menu

---

**Status:** Enhanced streamlined reference with proven patterns, 3D animation integration, progressive loading system, performance optimization expertise, CSS coordination resolution, technical debt awareness, and systematic debugging methodologies  
**Usage:** Reference before development for instant file identification, integration guidance, 3D component patterns, progressive loading patterns, technical debt awareness, system specification requirements, and debugging workflow application