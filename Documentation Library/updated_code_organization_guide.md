# MTG Deck Builder - Code Organization Guide

**Created:** June 7, 2025  
**Enhanced:** June 8, 2025 (Post-Reconciliation with Advanced UI/UX Patterns + Debugging Methodologies)  
**🆕 Performance Optimized:** June 9, 2025 (Post-Search Performance + Load More + Image Loading Optimization)  
**Purpose:** Comprehensive reference for codebase organization, integration points, development patterns, advanced UI/UX techniques, sophisticated debugging methodologies, and performance optimization patterns  
**Source:** Architecture review synthesis + useCards architecture overhaul experience + MTGOLayout refactoring + Header UI/UX redesign + advanced debugging methodology development + performance optimization case studies  
**Repository:** https://github.com/abaeckst/mtg-deck-builder  

## 🎯 Quick Reference - Development Decision Tree

### Adding Search Features
**Files to Modify:**
- `src/hooks/useSearch.ts` - Core search logic and API integration (**EXTRACTED HOOK** + **PERFORMANCE OPTIMIZED**)
- `src/services/scryfallApi.ts` - API query building and enhanced search + **Load More coordination**
- `src/components/SearchAutocomplete.tsx` - Search UI and suggestions
- `src/types/search.ts` - Search type definitions

**Pattern:** Enhance query building in scryfallApi → Update useSearch hook → Modify search components
**🆕 Performance Pattern:** Apply timing analysis for performance bottlenecks, implement pagination state management
**Proven Pattern:** Use hook extraction methodology if useSearch grows too large

### Adding Filter Features
**Files to Modify:**
- `src/hooks/useFilters.ts` - Filter state management (extracted hook - **EXCELLENT EXAMPLE**)
- `src/components/FilterPanel.tsx` - Filter UI and controls
- `src/components/CollapsibleSection.tsx` - Reusable filter sections
- `src/services/scryfallApi.ts` - Filter parameter integration

**Pattern:** Add filter state to useFilters → Create UI in FilterPanel → Integrate with search API
**🆕 Reactivity Pattern:** Ensure filter changes trigger clean searches with proper coordination
**Proven Pattern:** useFilters is excellent example of focused hook responsibility

### Adding Card Display Features
**Files to Modify:**
- `src/components/MagicCard.tsx` - Base card display component (**ENHANCED WITH LAZY LOADING**)
- `src/components/LazyImage.tsx` - **NEW** Progressive image loading component
- `src/components/DraggableCard.tsx` - Interactive card wrapper with **ENHANCED DRAG PREVIEW**
- `src/types/card.ts` - Card type definitions and utilities (**CONSISTENT IMAGE STRATEGY**)

**Pattern:** Enhance base card component → Update interactive wrapper → Add type support
**🆕 Performance Pattern:** Apply progressive/lazy loading for image optimization, use consistent normal-size images
**🆕 Enhanced Pattern:** Apply 3x transform scaling for previews, zone-relative positioning for feedback

### Adding Pagination Features
**Files to Modify:**
- `src/hooks/usePagination.ts` - Pagination state management (**EXTRACTED HOOK**)
- `src/hooks/useSearch.ts` - Search integration with pagination (**ENHANCED STATE MANAGEMENT**)
- `src/services/scryfallApi.ts` - Load More API logic (**COMPREHENSIVE 422 ERROR PREVENTION**)

**Pattern:** Update pagination state → Coordinate with search → API integration
**🆕 Performance Pattern:** Implement stored pagination state to prevent unnecessary API calls and 422 errors
**Smart Card Append Pattern:** For scroll preservation during Load More operations

### Adding Performance Optimization Features
**Files to Modify:**
- `src/hooks/useSorting.ts` - **PERFORMANCE OPTIMIZED** (hook re-render loops eliminated)
- `src/hooks/useSearch.ts` - Search coordination with **CLEAN PARAMETER MANAGEMENT**
- `src/services/scryfallApi.ts` - **WILDCARD OPTIMIZATION** for filter-only searches

**🆕 Pattern:** Identify performance bottlenecks → Apply timing analysis → Fix re-render loops → Optimize API calls
**🆕 Advanced Pattern:** Hook optimization with stable dependencies, debounced storage, memoized returns

### Adding Hook Features
**Files to Review First:**
- `src/hooks/useCards.ts` - Primary coordination hub (**REFACTORED** - now 250 lines)
- `src/hooks/useFilters.ts` - Filter state management (**EXCELLENT EXAMPLE** - clean separation)
- Integration pattern depends on feature type

**Pattern:** Assess if new hook needed → Extract if growing too large → Maintain clean APIs
**🆕 Performance Pattern:** Monitor for re-render loops, apply stable dependencies, implement proper memoization
**🆕 Proven Pattern:** Component extraction methodology available for large hooks (580→250 line success + 925→450 line success)

### Adding Export Features
**Files to Modify:**
- `src/utils/deckFormatting.ts` - Text formatting utilities
- `src/utils/screenshotUtils.ts` - Image generation (⚠️ 850 lines - complex)
- `src/components/TextExportModal.tsx` OR `src/components/ScreenshotModal.tsx`

**Pattern:** Add utility functions → Create/enhance modal components → Integrate with main layout

### Adding Drag & Drop Features
**Files to Modify:**
- `src/hooks/useDragAndDrop.ts` - Drag interaction logic (⚠️ 445 lines - complex but focused)
- `src/components/DraggableCard.tsx` - Card drag behavior with **ENHANCED PREVIEW**
- `src/components/DropZone.tsx` - Drop target behavior with **CENTERED FEEDBACK**

**Pattern:** Enhance drag hook logic → Update card components → Modify drop zones
**🆕 Enhanced Pattern:** Apply 3x transform scaling, zone-relative centering, component isolation

### 🆕 Adding Unified State Features
**Files to Modify:**
- `src/hooks/useLayout.ts` - Unified state management with **ADVANCED COORDINATION PATTERNS**
- `src/components/DeckArea.tsx` - Control components with **MTGO STYLING**
- `src/components/SideboardArea.tsx` - State inheritance with **SIMPLIFIED HEADERS**

**🆕 Pattern:** Single source of truth → Coordination functions → Component synchronization → Migration support
**🆕 Advanced Pattern:** Unified deck/sideboard state with automatic migration and constraint systems

### 🆕 Adding Responsive Features
**Files to Modify:**
- `src/components/DeckArea.tsx` - **RESPONSIVE OVERFLOW SYSTEM** with priority-based hiding
- `src/components/ViewModeDropdown.tsx` - **CONTEXT-AWARE DROPDOWN** with z-index adaptation
- `src/components/MTGOLayout.css` - **MTGO STYLING FOUNDATION** with responsive hierarchy

**🆕 Pattern:** Priority ordering → Space detection → Dynamic hiding → Overflow menu → Context preservation
**🆕 Advanced Pattern:** ResizeObserver monitoring, context-aware components, professional overflow systems

### 🆕 Adding Advanced UI Features
**Files to Modify:**
- `src/components/MTGOLayout.css` - **PROFESSIONAL MTGO STYLING** with dark theme foundation
- Components requiring **CONTEXT-AWARE BEHAVIOR** and **RESPONSIVE DESIGN**
- Integration with **UNIFIED STATE MANAGEMENT** and **COMPONENT EXTRACTION** patterns

**🆕 Pattern:** MTGO styling foundation → Context awareness → Responsive adaptation → Advanced coordination
**🆕 Advanced Pattern:** Dark gradient panels, priority-based hiding, context-aware z-index, professional polish

## 📁 Complete File Organization Matrix

### 🎨 Components Layer (`src/components/`) - 20 Files **ENHANCED ARCHITECTURE**

#### Core Layout & Infrastructure (**ENHANCED WITH EXTRACTION + MTGO STYLING**)
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `MTGOLayout.tsx` | **450 lines** | **Simplified coordinator** (**REFACTORED** from 925 lines) | ALL hooks, area components, **Clean orchestration** | ✅ **EXCELLENT** |
| `CollectionArea.tsx` | **~200 lines** | **Collection-specific logic** (**EXTRACTED** from MTGOLayout) | useCards, Load More, **MTGO styling** | ✅ **GOOD** |
| `DeckArea.tsx` | **~200 lines** | **Deck management with unified controls** (**EXTRACTED** + **ENHANCED**) | useLayout, ViewModeDropdown, **Responsive overflow** | ✅ **GOOD** |
| `SideboardArea.tsx` | **~200 lines** | **Simplified header with unified state** (**EXTRACTED** + **ENHANCED**) | useLayout inheritance, **MTGO styling** | ✅ **EXCELLENT** |
| `FilterPanel.tsx` | 368 lines | Professional filter interface | useCards, CollapsibleSection, GoldButton, SubtypeInput | ✅ GOOD |
| `AdaptiveHeader.tsx` | 201 lines | Responsive header controls | Standalone utility | ✅ EXCELLENT |
| `CollapsibleSection.tsx` | 52 lines | Reusable collapsible UI | Used by FilterPanel | ✅ EXCELLENT |

#### Card Display & Interaction (**ENHANCED WITH UX IMPROVEMENTS + PERFORMANCE**)
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `MagicCard.tsx` | 312 lines | **Base card display foundation** (**ENHANCED WITH LAZY LOADING**) | Used by DraggableCard, ListView, PileView, export modals | ✅ **ENHANCED** |
| `LazyImage.tsx` | **~100 lines** | **Progressive/lazy image loading** (**NEW PERFORMANCE COMPONENT**) | MagicCard, **Intersection Observer**, **Performance optimization** | ✅ **EXCELLENT** |
| `DraggableCard.tsx` | 276 lines | **Interactive card with enhanced drag** (**3x PREVIEW**) | MagicCard, drag/drop system, **Component isolation** | ✅ **ENHANCED** |
| `ListView.tsx` | 318 lines | Universal tabular view | Card data types, sorting system, quantity management | ✅ GOOD |
| `PileView.tsx` | 289 lines | MTGO-style pile organization | PileColumn, card sorting, selection system | ✅ GOOD |
| `PileColumn.tsx` | 156 lines | Individual pile column | DraggableCard, selection, manual arrangement | ✅ GOOD |
| `PileSortControls.tsx` | 45 lines | Pile sort controls | PileView sort state | ✅ EXCELLENT |

#### Search & Filter Components
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `SearchAutocomplete.tsx` | 114 lines | Enhanced search input | **useSearch hook**, Search suggestions, keyboard navigation | ✅ GOOD |
| `SubtypeInput.tsx` | 191 lines | Autocomplete multi-select | Subtype database, filter state | ✅ GOOD |
| `GoldButton.tsx` | 25 lines | Multicolor filtering button | Filter state management | ✅ EXCELLENT |

#### 🆕 Advanced UI Components (**NEW + ENHANCED**)
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `ViewModeDropdown.tsx` | **~150 lines** | **Professional MTGO dropdown** (**NEW** with **CONTEXT-AWARE Z-INDEX**) | useLayout, **Context detection**, **Responsive overflow** | ✅ **EXCELLENT** |
| `DropZone.tsx` | 203 lines | **Enhanced drop zone with centered feedback** (**ENHANCED**) | Drag system, **Zone-relative positioning** | ✅ **ENHANCED** |
| `DragPreview.tsx` | 84 lines | **3x larger visual drag preview** (**ENHANCED**) | Drag state, **Transform scaling**, **Cursor offset** | ✅ **ENHANCED** |

#### UI Infrastructure
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `Modal.tsx` | 85 lines | Reusable modal dialog | Export modals | ✅ EXCELLENT |
| `ContextMenu.tsx` | 75 lines | Right-click context menu | Context actions, card operations | ✅ EXCELLENT |

#### Export & Utilities
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `TextExportModal.tsx` | 132 lines | Text export interface | Modal, deck formatting | ✅ GOOD |
| `ScreenshotModal.tsx` | 298 lines | Visual deck export | Modal, card display, layout utils | ⚠️ COMPLEX |

### 🔧 Hooks Layer (`src/hooks/`) - 11 Files **ENHANCED ARCHITECTURE + PERFORMANCE OPTIMIZED**

#### Core Data Management (**REFACTORED + ENHANCED + PERFORMANCE OPTIMIZED**)
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `useCards.ts` | **250 lines** | **Coordination hub** (**REFACTORED** from 580 lines) | useFilters, useSearch, usePagination, useCardSelection, useSearchSuggestions | ✅ **EXCELLENT** |
| `useSearch.ts` | **350 lines** | **Core search and API communication** (**ENHANCED STATE MANAGEMENT**) | scryfallApi, SearchAutocomplete, **Stored pagination state** | ✅ **ENHANCED** |
| `usePagination.ts` | **120 lines** | **Progressive loading and Load More** (**EXTRACTED** from useCards) | useSearch coordination, **Smart Card Append** | ✅ **EXCELLENT** |
| `useCardSelection.ts` | **50 lines** | **Card selection state management** (**EXTRACTED** from useCards) | DraggableCard, ListView, PileView | ✅ **EXCELLENT** |
| `useSearchSuggestions.ts` | **70 lines** | **Search autocomplete and history** (**EXTRACTED** from useCards) | SearchAutocomplete, search state | ✅ **EXCELLENT** |
| `useFilters.ts` | 120 lines | Filter state management (**PRE-EXISTING EXCELLENT EXAMPLE**) | Used by useCards, FilterPanel | ✅ **EXCELLENT** |

#### 🆕 UI State Management (**ENHANCED WITH UNIFIED PATTERNS**)
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `useLayout.ts` | **305 lines** | **Unified deck/sideboard state management** (**ENHANCED**) | DeckArea, SideboardArea, **Automatic migration**, **Constraint systems** | ✅ **ENHANCED** |
| `useSelection.ts` | 310 lines | Dual selection system | DraggableCard, ListView, PileView | ⚠️ COMPLEX |
| `useDragAndDrop.ts` | 445 lines | Complete drag & drop | DraggableCard, DropZone, context menu | ⚠️ VERY COMPLEX |
| `useSorting.ts` | 270 lines | **Sorting state + dual logic** (**PERFORMANCE OPTIMIZED**) | Card components, useCards, **Fixed re-render loops** | ✅ **ENHANCED** |

#### UI Utilities
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `useContextMenu.ts` | 165 lines | Context menu state | ContextMenu component, card operations | ✅ GOOD |
| `useCardSizing.ts` | 85 lines | Card size management | Card components, size sliders | ✅ **EXCELLENT** |
| `useResize.ts` | 215 lines | Panel resizing handlers | useLayout, resize handles | ✅ GOOD |

### 🛠️ Services & Utils Layer (`src/services/`, `src/utils/`, `src/types/`) - 7 Files **PERFORMANCE ENHANCED**

#### Service Layer (**PERFORMANCE OPTIMIZED**)
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `scryfallApi.ts` | **575 lines** | **Complete Scryfall abstraction** (**ENHANCED WITH LOAD MORE LOGIC**) | **useSearch hook**, search suggestions, **422 error prevention** | ✅ **ENHANCED** |

#### Utility Layer
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `deckFormatting.ts` | 180 lines | Deck export utilities | Export modals, DeckCardInstance types | ✅ GOOD |
| `screenshotUtils.ts` | **850 lines** | Advanced screenshot generation | ScreenshotModal, html2canvas | ⚠️ **EXTREMELY COMPLEX** |
| `deviceDetection.ts` | 145 lines | Device capability detection | Standalone utility (ready for integration) | ✅ EXCELLENT |

#### Type System (**ENHANCED WITH IMAGE STRATEGY**)
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `card.ts` | **520 lines** | **Foundation type system** (**ENHANCED WITH CONSISTENT IMAGE URLS**) | ALL components, hooks, services | ✅ **ENHANCED** |
| `search.ts` | 120 lines | Enhanced search types | SearchAutocomplete, enhanced search | ✅ GOOD |

#### 🆕 Styling Infrastructure (**ENHANCED WITH MTGO FOUNDATION**)
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `MTGOLayout.css` | **1,450+ lines** | **Complete application styling foundation** (**CRITICAL + MODERNIZATION PLAN READY**) | ALL components, **MTGO styling**, **Responsive systems** | ⚠️ **TECHNICAL DEBT** |

## 🔗 Integration Point Reference

### 🆕 Primary Data Flow Patterns (**ENHANCED ARCHITECTURE + PERFORMANCE**)

#### Search & Display Flow (**REFACTORED + PERFORMANCE OPTIMIZED**)
```
Components (user input) → useCards (coordinator) → useSearch → scryfallApi → Scryfall API
     ↓
API Response → useSearch (results + stored state) → useCards (coordination) → Components (display)
     ↓
useFilters (filter state) → useCards (coordination) → useSearch (clean search params) → scryfallApi
     ↓  
useSorting (sort state) → useCards (coordination) → useSearch (performance optimized) → API/client-side
```

#### 🆕 Performance-Optimized Search Flow (**NEW ARCHITECTURE**)
```
Filter changes → useCards (clean search trigger) → useSearch (fresh parameters) → scryfallApi (wildcard optimization)
     ↓
useSorting (stable dependencies) → No re-render loops → Fast search response (<1 second)
     ↓
Search coordination → Clean parameter management → No parameter accumulation
```

#### 🆕 Load More Flow (**COMPREHENSIVE 422 ERROR PREVENTION**)
```
Load More trigger → useSearch (stored pagination state) → scryfallApi (decision logic) → API/stored cards
     ↓
Comprehensive analysis: Total cards, current page data, remaining cards availability
     ↓
Decision: Use stored cards OR fetch next page → No 422 errors → Seamless user experience
```

#### 🆕 Image Loading Flow (**PROGRESSIVE OPTIMIZATION**)
```
Search results → MagicCard (consistent normal images) → LazyImage (Intersection Observer) → Progressive loading
     ↓
Viewport detection → Load only visible cards → Eliminate simultaneous loading → Better perceived performance
```

#### 🆕 Unified State Flow (**NEW ARCHITECTURE**)
```
DeckArea (user input) → useLayout (unified state) → SideboardArea (automatic inheritance)
     ↓
Single controls → Unified state updates → Both areas re-render simultaneously
     ↓
State migration → Legacy state detection → Automatic upgrade → User preference preservation
```

#### Pagination Flow (**ENHANCED STATE MANAGEMENT**)
```
Components (Load More) → useCards (coordinator) → usePagination (state) → useSearch (stored state + API calls)
     ↓
API Response → useSearch → usePagination (update state) → useCards → Components (Smart Card Append)
```

#### 🆕 Responsive Design Flow (**NEW ARCHITECTURE**)
```
Window resize → ResizeObserver → DeckArea (space detection) → Priority-based hiding → Overflow menu
     ↓
Context detection → ViewModeDropdown (z-index adaptation) → Professional overflow functionality
```

#### User Interaction Flow
```
Components (user actions) → useSelection (selection state) → useContextMenu (actions)
     ↓
useDragAndDrop (interactions) → Components (callbacks) → useCards (deck updates)
     ↓
useLayout (layout state) ← useResize (interactions) ← Components (handles)
```

### 🆕 Critical Integration Points (**UPDATED + ENHANCED + PERFORMANCE**)

#### useCards Hook (Coordination Hub) (**REFACTORED + PERFORMANCE ENHANCED**)
**Incoming Dependencies:**
- `useFilters.ts` - Filter state for search parameters (**ENHANCED REACTIVITY**)
- `useSearch.ts` - Core search functionality and API communication (**PERFORMANCE OPTIMIZED**)
- `usePagination.ts` - Load More state and progressive loading (**422 ERROR PREVENTION**)
- `useCardSelection.ts` - Card selection state management (**EXTRACTED HOOK**)
- `useSearchSuggestions.ts` - Search autocomplete and history (**EXTRACTED HOOK**)
- Components - Search input, filter controls, Load More triggers

**Outgoing Dependencies:**
- ALL card display components - Search results and selection data
- Export components - Deck and sideboard data
- Layout components - Loading states and error handling

**🆕 Performance Coordination Patterns:**
- **Clean Search Triggers:** Filter changes trigger immediate fresh searches with clean parameters
- **Timing Optimization:** Sub-second search response through useSorting performance fixes
- **State Preservation:** Proper coordination between hooks prevents parameter accumulation

#### 🆕 useSearch Hook (API Communication Hub) (**ENHANCED STATE MANAGEMENT**)
**Incoming Dependencies:**
- `useCards.ts` - Search coordination and clean parameter management
- `usePagination.ts` - Load More state coordination
- `useFilters.ts` - Filter state for clean search triggers
- `useSorting.ts` - Sort parameters (performance optimized)

**Outgoing Dependencies:**
- `scryfallApi.ts` - API calls with stored pagination state
- Components - Search results and loading states
- Load More functionality - 422 error prevention through stored state

**🆕 Enhanced Coordination Patterns:**
- **Stored Pagination State:** Preserves full page data for Load More operations
- **Clean Parameter Management:** Prevents accumulation from previous searches
- **Performance Optimization:** Coordinates with wildcard optimization in scryfallApi

#### 🆕 useLayout Hook (Unified State Management) (**NEW ENHANCED ARCHITECTURE**)
**Incoming Dependencies:**
- `DeckArea.tsx` - Control inputs affecting both deck and sideboard
- `SideboardArea.tsx` - State inheritance from unified management
- Legacy state migration - Automatic detection and upgrade

**Outgoing Dependencies:**
- `DeckArea.tsx` - Unified view mode and size state
- `SideboardArea.tsx` - Inherited state for synchronized behavior
- Panel resizing system - Constraint management and persistence

**🆕 Unified State Coordination Patterns:**
- **Single Source of Truth:** One state controlling multiple component areas
- **Automatic Migration:** Legacy state detection and seamless upgrade
- **Constraint Systems:** Different validation rules for different component contexts
- **State Synchronization:** Multi-component coordination with real-time updates

#### MTGOLayout Component (Simplified Orchestrator) (**REFACTORED**)
**Incoming Dependencies:**
- Area components - CollectionArea, DeckArea, SideboardArea (**NEW EXTRACTED COMPONENTS**)
- ALL hooks - useCards (coordinator), useLayout, useSelection, useDragAndDrop, etc.
- **Smart Card Append:** Scroll preservation during Load More (**PROVEN PATTERN**)

**Outgoing Dependencies:**
- Main App.tsx - Primary application interface
- CSS variables - Layout state management

**🆕 Component Orchestration Patterns:**
- **Simplified Coordination:** Focus on hook integration and area component coordination
- **Clean Interfaces:** Well-defined prop interfaces between coordinator and area components
- **State Distribution:** Unified state management with proper component synchronization

#### 🆕 Area Components (NEW EXTRACTED ARCHITECTURE)
**CollectionArea.tsx:**
- **Responsibility:** Collection-specific logic, Load More integration, MTGO styling
- **Integration:** useCards, search/filter coordination, Smart Card Append implementation
- **Pattern:** Focused area logic with clean prop interfaces

**DeckArea.tsx:**
- **Responsibility:** Deck management, unified controls, responsive overflow system
- **Integration:** useLayout, ViewModeDropdown, ResizeObserver, professional MTGO styling
- **Pattern:** Control center with unified state management and responsive adaptation

**SideboardArea.tsx:**
- **Responsibility:** Simplified header, state inheritance, MTGO styling consistency
- **Integration:** useLayout inheritance, automatic state synchronization
- **Pattern:** Clean state inheritance with minimal control duplication

#### Type System Bridge (card.ts) (**ENHANCED WITH IMAGE STRATEGY**)
**Architectural Bridge Functions:**
- `getCardId()` - ScryfallCard → unique ID for collections
- `getSelectionId()` - DeckCardInstance → unique ID for deck/sideboard
- `isCardInstance()` - Type guard for instance vs card
- `createCardInstance()` - ScryfallCard → DeckCardInstance conversion
- `groupInstancesByCard()` - Instance management for display
- `getCardImageUri()` - **ENHANCED** Consistent normal-size image strategy

**🆕 Image Strategy Bridge:**
- **Consistent Quality:** Always prefer normal → large → small fallback
- **Performance Optimization:** Balanced quality vs file size for lazy loading
- **Visual Consistency:** Better experience across all card sizes

## 🚨 🆕 Advanced Performance Optimization Patterns (**NEW SECTION**)

### 🆕 Search Performance Debugging Methodology (**PROVEN EFFECTIVE**)

#### When to Apply Search Performance Analysis
- **Symptoms:** Search operations taking 2+ seconds despite fast API responses
- **Indicators:** Console showing excessive hook initialization logs
- **Success Example:** useSorting optimization reducing search time from 2-7+ seconds to <1 second

#### Search Performance Debug Process (**VALIDATED**)
```typescript
// 1. Add API timing measurements
console.log('API_REQUEST_TIME:', apiEndTime - apiStartTime);
console.log('JSON_PARSING_TIME:', parseEndTime - parseStartTime);

// 2. Add total operation timing
console.log('TOTAL_SEARCH_TIME:', totalEndTime - totalStartTime);

// 3. Identify bottlenecks
if (totalTime >> apiTime) {
  // App processing bottleneck - likely hook re-render loops
  // Check for excessive hook initialization logs
}

// 4. Apply hook optimization patterns
const optimizedCallback = useCallback(
  (param) => {
    // Function logic
  },
  [stableDependency] // Fix: stable dependencies, not derived state
);
```

#### Hook Re-render Loop Elimination (**PROVEN TECHNIQUE**)
```typescript
// Problem Pattern (causes infinite re-renders)
const updateSort = useCallback(
  (newSort) => {
    setSortState(newSort);
  },
  [sortState] // ❌ Unstable dependency causing re-renders
);

// Solution Pattern (stable dependencies)
const updateSort = useCallback(
  (newSort) => {
    setSortState(newSort);
  },
  [] // ✅ Stable dependencies prevent re-renders
);

// Advanced Pattern (memoized return object)
return useMemo(() => ({
  sortState,
  updateSort,
  // ... other values
}), [sortState]); // ✅ Prevents component re-renders when object hasn't changed
```

### 🆕 Load More Debugging Methodology (**COMPREHENSIVE APPROACH**)

#### When to Apply Load More Analysis
- **Symptoms:** 422 errors during Load More operations
- **Indicators:** API logs showing "page 2" requests when all results fit on page 1
- **Success Example:** Fixed 422 errors through comprehensive pagination state management

#### Load More Debug Process (**SYSTEMATIC INVESTIGATION**)
```typescript
// 1. API Response Analysis
console.log('🌐 TOTAL CARDS:', response.total_cards);
console.log('🌐 RETURNED COUNT:', response.data.length); 
console.log('🌐 HAS MORE:', response.has_more);

// 2. Pagination State Analysis
console.log('📊 ENHANCED DEBUG - Load More Decision Analysis:', {
  totalCardsFromSearch: paginationState.totalCards,
  currentPageTotalCards: currentPageCards.length,
  allResultsFitOnCurrentPage: totalCards <= currentPageCards.length,
  shouldUseRemainingCards: /* decision logic */
});

// 3. Decision Logic Implementation
if (allResultsFitOnCurrentPage && hasRemainingCards) {
  // Use stored page data
  return useRemainingCardsFromCurrentPage();
} else {
  // Fetch next page
  return fetchNextPageFromAPI();
}
```

#### Stored Pagination State Pattern (**PROVEN SOLUTION**)
```typescript
// Enhanced SearchState with stored pagination
interface SearchState {
  searchResults: PaginatedSearchState<ScryfallCard>;
  storedPaginationState: PaginatedSearchState | null; // NEW: Store full page data
  // ... other state
}

// Store during initial search
const searchResult = await searchCardsWithPagination(query, filters);
setState(prev => ({
  ...prev,
  searchResults: searchResult,
  storedPaginationState: searchResult // Store complete pagination state
}));

// Use during Load More
if (state.storedPaginationState?.currentPageCards?.length > 0) {
  // Use stored data with full page information
  currentPaginationState = {
    ...state.storedPaginationState,
    loadedCards: actualLoadedCards,
    cardsConsumedFromCurrentPage: actualLoadedCards
  };
}
```

### 🆕 Image Loading Performance Patterns (**PROGRESSIVE OPTIMIZATION**)

#### When to Apply Image Loading Optimization
- **Symptoms:** 75 cards loading simultaneously in random order
- **Performance Impact:** Poor perceived performance, mobile issues
- **Success Example:** Progressive/lazy loading with consistent normal-size images

#### Progressive Loading Implementation (**PROVEN TECHNIQUE**)
```typescript
// LazyImage Component with Intersection Observer
const LazyImage = ({ src, alt, className }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [imageSrc, setImageSrc] = useState(null);
  const imgRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            setImageSrc(src); // Start loading when visible
            observer.unobserve(entry.target);
          }
        });
      },
      { 
        rootMargin: '100px', // Start loading before fully visible
        threshold: 0.1 
      }
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, [src]);

  return (
    <div ref={imgRef} className={className}>
      {imageSrc ? (
        <img 
          src={imageSrc} 
          alt={alt}
          onLoad={() => setIsLoading(false)}
        />
      ) : (
        <div>Preparing...</div>
      )}
    </div>
  );
};
```

#### Consistent Image Strategy (**QUALITY OPTIMIZATION**)
```typescript
// Enhanced getCardImageUri with consistent quality
export const getCardImageUri = (card: ScryfallCard, size: string = 'normal') => {
  // Always use 'normal' for consistent quality (~488×680px, ~150KB)
  // Good balance of quality vs file size for progressive loading
  return card.image_uris?.normal || 
         card.image_uris?.large || 
         card.image_uris?.small || 
         '';
};
```

### 🆕 API Performance Optimization Patterns (**EFFICIENCY IMPROVEMENTS**)

#### Wildcard Query Optimization (**SCRYFALL API EFFICIENCY**)
```typescript
// buildEnhancedSearchQuery optimization
const buildEnhancedSearchQuery = (query: string): string => {
  // Early return for wildcard queries - avoid expensive enhancement
  if (query.trim() === '*') {
    console.log('🔍 WILDCARD OPTIMIZATION: Returning simple wildcard');
    return '*'; // Let Scryfall handle wildcard efficiently
  }
  
  // Complex enhancement only for specific queries
  return `(name:${query} OR o:${query} OR type:${query})`;
};
```

#### Clean Search Parameter Management (**COORDINATION OPTIMIZATION**)
```typescript
// Filter reactivity with clean searches
useEffect(() => {
  if (!isInitialMount && hasActiveFilters) {
    console.log('🔄 CLEAN SEARCH triggered by filter change');
    searchWithAllFilters('*'); // Clean search with only current filters
  }
}, [activeFilters]); // React to filter changes

// Clean filter building
const searchWithAllFilters = useCallback(async (query: string) => {
  // Build filter object from scratch (no accumulation)
  const filterObject = {
    colors: filters.colors,
    types: filters.types,
    // ... other current filters only
  };
  
  await searchCardsWithFilters(query, filterObject);
}, [filters]); // Clean dependencies
```

## ⚠️ Critical Refactoring Priorities (**UPDATED WITH RECENT EXPERIENCE + PERFORMANCE INSIGHTS**)

### High Priority - Performance and Architecture Issues

#### 1. CSS Architecture Modernization (**COMPREHENSIVE PLAN READY**)
**Status:** Complete modernization plan developed with automated migration scripts
**Files:** `src/components/MTGOLayout.css` (1,450+ lines monolithic structure)
**Impact:** 3-6x faster style modifications, industry-standard architecture
**Approach:** 4-phase systematic migration with design token system and component-based structure

#### 2. Performance Optimization Expansion (**APPLY PROVEN PATTERNS**)
**Status:** Successful patterns identified through search/pagination optimization
**Opportunities:** Apply timing analysis and hook optimization to other performance bottlenecks
**Pattern:** Identify bottlenecks → Apply timing analysis → Fix re-render loops → Optimize coordination

#### 3. scryfallApi.ts (575 lines) - Service Layer (**ENHANCED BUT LARGE**)
**Status:** Working well with Load More enhancements, apply extraction methodology if continues growing
**Recommended Approach:** Use proven hook extraction methodology for service layer if problematic
**Pattern:** Apply extraction patterns: Identify responsibilities → Extract focused services → Maintain coordinator

### Medium Priority - Large File Issues

#### 4. card.ts (520 lines) - Type System Foundation (**ENHANCED AND STABLE**)
**Status:** Working well with image strategy enhancements, apply separation when growth continues
**Recommended Approach:** Separate types from utilities using documented separation patterns
**Pattern:** Apply type/utility separation using proven component extraction methodology

#### 5. screenshotUtils.ts (850 lines) - Algorithm Complexity (**LOWEST PRIORITY**)
**Status:** Complex but focused, apply extraction patterns if maintenance becomes difficult
**Recommended Approach:** Extract algorithm modules using proven extraction methodology

### 🆕 Excellent Architecture Examples (**POST-PERFORMANCE OPTIMIZATION**)

#### ✅ Perfect Performance Optimization Examples
- **useSorting.ts** (270 lines) - **EXCELLENT PERFORMANCE FIX** - Eliminated re-render loops reducing search time 2-7+ seconds → <1 second
- **useSearch.ts** (350 lines) - **EXCELLENT STATE MANAGEMENT** - Stored pagination state preventing 422 errors
- **scryfallApi.ts** (575 lines) - **EXCELLENT COORDINATION** - Comprehensive Load More logic with wildcard optimization
- **LazyImage.tsx** (~100 lines) - **EXCELLENT PERFORMANCE COMPONENT** - Progressive loading eliminating simultaneous image loading

#### ✅ Perfect Component Extraction Examples
- **MTGOLayout.tsx** (450 lines) - **EXCELLENT COORDINATOR** - Clean hook integration with extracted area components
- **CollectionArea.tsx** (~200 lines) - **EXCELLENT FOCUSED COMPONENT** - Collection-specific logic with MTGO styling
- **DeckArea.tsx** (~200 lines) - **EXCELLENT UNIFIED CONTROLS** - Deck management with responsive overflow system
- **SideboardArea.tsx** (~200 lines) - **EXCELLENT STATE INHERITANCE** - Simplified header with unified state

#### ✅ Perfect Hook Architecture Examples  
- **useCards.ts** (250 lines) - **EXCELLENT COORDINATOR** - Successfully coordinates 5 extracted hooks with performance enhancements
- **usePagination.ts** (120 lines) - **EXCELLENT EXTRACTION** - Focused responsibility, clean API
- **useCardSelection.ts** (50 lines) - **EXCELLENT EXTRACTION** - Minimal, focused state management
- **useSearchSuggestions.ts** (70 lines) - **EXCELLENT EXTRACTION** - Clean autocomplete functionality
- **useFilters.ts** (120 lines) - **ORIGINAL EXCELLENT EXAMPLE** - Perfect separation and clean API

#### ✅ Perfect UI Component Examples
- **ViewModeDropdown.tsx** (~150 lines) - **EXCELLENT CONTEXT-AWARE** - Professional MTGO dropdown with context detection
- **DragPreview.tsx** (84 lines) - **EXCELLENT ENHANCED** - 3x transform scaling with cursor offset
- **DropZone.tsx** (203 lines) - **EXCELLENT ENHANCED** - Zone-relative centering with professional feedback

#### ✅ Perfect Utility Examples
- **CollapsibleSection.tsx** (52 lines) - Single responsibility, accessibility, reusable
- **GoldButton.tsx** (25 lines) - Perfect micro-component with clear purpose
- **Modal.tsx** (85 lines) - Clean, reusable with proper accessibility

### 🆕 Architecture Success Patterns (**ENHANCED WITH PERFORMANCE EXAMPLES**)

#### 🆕 Performance Optimization Success (**PROVEN PATTERNS**)
- **Search Performance Fix:** useSorting re-render loop elimination (2-7+ seconds → <1 second)
- **Load More 422 Prevention:** Comprehensive pagination state management with stored data
- **Image Loading Optimization:** Progressive/lazy loading eliminating 75-card simultaneous loading
- **API Efficiency:** Wildcard optimization reducing unnecessary database scans

#### 🆕 Component Extraction Success (**PROVEN PATTERNS**)
- **MTGOLayout Refactoring:** 925 lines → 450 line coordinator + 3 focused area components
- **Coordinator Pattern:** Clean hook integration with extracted area-specific logic
- **External API Preservation:** All existing integrations maintained during major refactoring
- **Zero Regressions:** All functionality preserved during architectural enhancement

#### 🆕 Unified State Management Success (**ADVANCED COORDINATION**)
- **useLayout Enhancement:** Single controls affecting both deck and sideboard with state migration
- **Automatic Migration:** Legacy state detection and seamless upgrade without user impact
- **Constraint Systems:** Different validation rules for collection vs deck/sideboard contexts
- **Multi-Component Synchronization:** Real-time updates across multiple component areas

#### 🆕 Responsive Design Success (**PRIORITY-BASED SYSTEMS**)
- **Dynamic Control Management:** Priority-based hiding with professional overflow menus
- **Context-Aware Components:** ViewModeDropdown with z-index adaptation based on rendering context
- **Professional Polish:** MTGO styling with sophisticated visual hierarchy and animations

#### 🆕 Enhanced UX Success (**TRANSFORM-BASED IMPROVEMENTS**)
- **Drag & Drop Enhancement:** 3x larger previews with zone-relative centering and component isolation
- **Smart Card Append:** Scroll preservation during Load More with performance optimization
- **Professional Interactions:** Enhanced visual feedback with authentic MTGO styling

### Patterns to Avoid (**ANTI-PATTERNS FROM EXPERIENCE + PERFORMANCE**)

#### Size & Complexity Issues
- **Monolithic Components:** Single components with multiple major responsibilities (MTGOLayout before refactoring)
- **Mixed Concerns:** Types mixed with utilities, layout mixed with business logic
- **Complex Dependencies:** Too many integration points in single component

#### 🆕 Performance Anti-Patterns (**VALIDATED THROUGH OPTIMIZATION**)
- **Hook Re-render Loops:** Unstable dependencies causing infinite re-renders (useSorting before fix)
- **Simultaneous Resource Loading:** All images/data loading at once overwhelming browser queues
- **Parameter Accumulation:** Search parameters building on previous context instead of clean state
- **Missing State Storage:** Forcing API calls instead of using stored data for pagination

#### 🆕 UI/UX Anti-Patterns
- **Nuclear Z-Index:** Extremely high values (9999999+) creating more conflicts than solutions
- **Global State Leakage:** Component state affecting unrelated instances
- **Missing Context Awareness:** Components not adapting to rendering environment

#### 🆕 State Management Anti-Patterns
- **State Duplication:** Multiple similar states instead of unified management
- **Missing Migration:** Breaking user preferences during state architecture changes
- **Tight Component Coupling:** Components knowing too much about each other's internals

## 📚 🆕 Quick Reference Cards (**ENHANCED WITH PERFORMANCE PATTERNS**)

### "I want to optimize search performance"
**Primary Files:** `src/hooks/useSorting.ts` (**PERFORMANCE OPTIMIZED**), `src/hooks/useSearch.ts` (**ENHANCED**), `src/hooks/useCards.ts` (coordinator)  
**🆕 Pattern:** Timing analysis → Identify re-render loops → Fix dependencies → Apply memoization → Validate improvements  
**🆕 Proven Pattern:** useSorting optimization (2-7+ seconds → <1 second) through stable dependencies and memoized returns

### "I want to fix Load More functionality"  
**Primary Files:** `src/hooks/useSearch.ts` (**STORED STATE**), `src/services/scryfallApi.ts` (**DECISION LOGIC**)  
**Secondary Files:** `src/hooks/usePagination.ts` (state coordination)  
**🆕 Pattern:** Store pagination state → Comprehensive decision logic → Use stored data when possible → Prevent 422 errors  
**🆕 Success Example:** Complete Load More fix with stored pagination state management

### "I want to optimize image loading performance"
**Primary Files:** `src/components/LazyImage.tsx` (**NEW COMPONENT**), `src/components/MagicCard.tsx` (**ENHANCED**), `src/types/card.ts` (**IMAGE STRATEGY**)  
**🆕 Pattern:** Consistent image strategy → Progressive/lazy loading → Intersection Observer → Performance optimization  
**🆕 Advanced Pattern:** Normal-size images + lazy loading + viewport detection + browser queue management

### "I want to modify search functionality"
**Primary Files:** `src/hooks/useSearch.ts` (**EXTRACTED HOOK** + **PERFORMANCE OPTIMIZED**), `src/services/scryfallApi.ts`, `src/components/SearchAutocomplete.tsx`  
**Secondary Files:** `src/types/search.ts`, `src/hooks/useFilters.ts`, `src/hooks/useCards.ts` (coordinator)  
**Pattern:** API changes → useSearch updates → useCards coordination → component integration  
**🆕 Performance Pattern:** Clean parameter management → Wildcard optimization → Filter reactivity → Sub-second response times
**🆕 Proven Pattern:** Hook extraction successful - useSearch is focused and maintainable

### "I want to add unified state functionality"  
**Primary Files:** `src/hooks/useLayout.ts` (**ENHANCED WITH UNIFIED PATTERNS**), `src/components/DeckArea.tsx`, `src/components/SideboardArea.tsx`  
**Secondary Files:** `src/components/MTGOLayout.tsx` (coordinator)  
**🆕 Pattern:** Single state source → Coordination functions → Component synchronization → Migration support  
**🆕 Success Example:** useLayout unified deck/sideboard state with automatic migration

### "I want to add responsive features"
**Primary Files:** `src/components/DeckArea.tsx` (**RESPONSIVE OVERFLOW SYSTEM**), `src/components/ViewModeDropdown.tsx` (**CONTEXT-AWARE**)  
**Secondary Files:** `src/components/MTGOLayout.css` (**MTGO STYLING FOUNDATION**)  
**🆕 Pattern:** Priority ordering → Space detection → Dynamic hiding → Overflow menu → Context preservation  
**🆕 Advanced Pattern:** ResizeObserver + context-aware components + professional overflow systems

### "I want to enhance UX with transforms"
**Primary Files:** `src/components/DragPreview.tsx` (**3X SCALING**), `src/components/DropZone.tsx` (**CENTERED FEEDBACK**)  
**Secondary Files:** `src/components/DraggableCard.tsx` (**COMPONENT ISOLATION**)  
**🆕 Pattern:** Transform scaling → Zone-relative positioning → Component isolation → Professional polish  
**🆕 Proven Pattern:** 3x scale transforms + zone centering + isolated effects

### "I want to apply MTGO styling"
**Primary Files:** `src/components/MTGOLayout.css` (**FOUNDATION**), header components  
**Secondary Files:** All components requiring professional dark theme  
**🆕 Pattern:** MTGO foundation → Dark gradients → Professional typography → Visual hierarchy  
**🆕 Success Example:** All headers with consistent MTGO styling and professional polish

### "I want to extract a large component"
**Primary Files:** Identify target component, create focused extracted components  
**🆕 Proven Pattern:** Component extraction methodology validated through MTGOLayout success  
**🆕 Process:** Identify areas → Create focused components → Implement coordinator → Apply coordination patterns → Smart testing  
**🆕 Success Example:** MTGOLayout.tsx (925→450 lines) + 3 focused area components with zero regressions

### "I want to add advanced debugging"
**Primary Files:** Components with integration issues, browser diagnostic tools  
**🆕 Proven Pattern:** Browser diagnostics → CSS cascade analysis → React event coordination → Integration validation  
**🆕 Process:** Systematic DOM investigation → Property verification → Layer analysis → Conflict resolution  
**🆕 Success Example:** Resize handle accessibility, overflow menu z-index, event timing resolution

### "I want to apply performance debugging"
**Primary Files:** Hooks with performance issues, components with slow rendering  
**🆕 Proven Pattern:** Timing analysis → Hook re-render identification → Dependency optimization → State management fixes  
**🆕 Process:** API timing → Total timing → Bottleneck identification → Hook optimization → Validation  
**🆕 Success Example:** useSorting optimization, Load More fixes, image loading enhancement

### "I want to add pagination with scroll preservation"
**Primary Files:** Component with pagination, implement Smart Card Append pattern  
**🆕 Proven Pattern:** Smart Card Append for natural scroll preservation  
**🆕 Process:** Track loaded count → Split existing/new cards → Render with stable/fresh keys → Update state appropriately  
**🆕 Success Example:** Load More eliminates scroll reset, only new cards re-render

---

**Created:** June 7, 2025 from comprehensive architecture review  
**🆕 Enhanced:** June 8, 2025 with advanced patterns from MTGOLayout refactoring, Header UI/UX redesign, and debugging methodology development  
**🆕 Performance Optimized:** June 9, 2025 with proven performance optimization patterns from search, pagination, and image loading enhancements  
**Status:** Complete reference guide with validated advanced methodologies and performance optimization patterns for MTG Deck Builder development  
**🆕 Performance Patterns:** Search optimization, Load More fixes, image loading enhancement, API efficiency, hook re-render elimination  
**🆕 Advanced Patterns:** Component extraction, unified state management, responsive design, context-aware components, MTGO styling, enhanced UX, debugging methodologies, performance optimization  
**Usage:** Reference before any development work to understand integration points and apply advanced patterns  
**🆕 Maintenance:** Update as architecture evolves and new advanced patterns are proven through sophisticated development experience