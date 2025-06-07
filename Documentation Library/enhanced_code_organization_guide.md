# MTG Deck Builder - Code Organization Guide

**Created:** June 7, 2025  
**Enhanced:** June 7, 2025 (Post-Reconciliation with Proven Patterns)  
**Purpose:** Comprehensive reference for codebase organization, integration points, development patterns, and proven methodologies  
**Source:** Architecture review synthesis + useCards architecture overhaul experience + proven pattern validation  
**Repository:** https://github.com/abaeckst/mtg-deck-builder  

## 🎯 Quick Reference - Development Decision Tree

### Adding Search Features
**Files to Modify:**
- `src/hooks/useSearch.ts` - Core search logic and API integration (**EXTRACTED HOOK**)
- `src/services/scryfallApi.ts` - API query building and enhanced search
- `src/components/SearchAutocomplete.tsx` - Search UI and suggestions
- `src/types/search.ts` - Search type definitions

**Pattern:** Enhance query building in scryfallApi → Update useSearch hook → Modify search components
**Proven Pattern:** Use hook extraction methodology if useSearch grows too large

### Adding Filter Features
**Files to Modify:**
- `src/hooks/useFilters.ts` - Filter state management (extracted hook - **EXCELLENT EXAMPLE**)
- `src/components/FilterPanel.tsx` - Filter UI and controls
- `src/components/CollapsibleSection.tsx` - Reusable filter sections
- `src/services/scryfallApi.ts` - Filter parameter integration

**Pattern:** Add filter state to useFilters → Create UI in FilterPanel → Integrate with search API
**Proven Pattern:** useFilters is excellent example of focused hook responsibility

### Adding Card Display Features
**Files to Modify:**
- `src/components/MagicCard.tsx` - Base card display component
- `src/components/DraggableCard.tsx` - Interactive card wrapper
- `src/types/card.ts` - Card type definitions and utilities

**Pattern:** Enhance base card component → Update interactive wrapper → Add type support

### Adding View Modes
**Files to Modify:**
- `src/components/ListView.tsx` OR `src/components/PileView.tsx` - Specific view logic
- `src/hooks/useLayout.ts` - View mode state management
- `src/components/MTGOLayout.tsx` - View mode integration

**Pattern:** Implement view-specific logic → Update layout state → Integrate with main layout
**Smart Card Append Pattern:** For pagination scenarios requiring scroll preservation

### Adding Hook Features
**Files to Review First:**
- `src/hooks/useCards.ts` - Primary coordination hub (**REFACTORED** - now 250 lines)
- `src/hooks/useFilters.ts` - Filter state management (**EXCELLENT EXAMPLE** - clean separation)
- Integration pattern depends on feature type

**Pattern:** Assess if new hook needed → Extract if growing too large → Maintain clean APIs
**Proven Pattern:** Hook extraction methodology available for large hooks (580→250 line success)

### Adding Export Features
**Files to Modify:**
- `src/utils/deckFormatting.ts` - Text formatting utilities
- `src/utils/screenshotUtils.ts` - Image generation (⚠️ 850 lines - complex)
- `src/components/TextExportModal.tsx` OR `src/components/ScreenshotModal.tsx`

**Pattern:** Add utility functions → Create/enhance modal components → Integrate with main layout

### Adding Drag & Drop Features
**Files to Modify:**
- `src/hooks/useDragAndDrop.ts` - Drag interaction logic (⚠️ 445 lines - complex but focused)
- `src/components/DraggableCard.tsx` - Card drag behavior
- `src/components/DropZone.tsx` - Drop target behavior

**Pattern:** Enhance drag hook logic → Update card components → Modify drop zones

### Adding Pagination Features
**Files to Modify:**
- `src/hooks/usePagination.ts` - Pagination state management (**EXTRACTED HOOK**)
- `src/hooks/useSearch.ts` - Search integration with pagination (**EXTRACTED HOOK**)
- `src/services/scryfallApi.ts` - Load More API logic

**Pattern:** Update pagination state → Coordinate with search → API integration
**Smart Card Append Pattern:** For scroll preservation during Load More operations

## 📁 Complete File Organization Matrix

### 🎨 Components Layer (`src/components/`) - 18 Files

#### Core Layout & Infrastructure
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `MTGOLayout.tsx` | 925 lines | **Main application orchestrator** | ALL hooks, ALL components, **Smart Card Append implementation** | ⚠️ **NEEDS REFACTORING** |
| `FilterPanel.tsx` | 368 lines | Professional filter interface | useCards, CollapsibleSection, GoldButton, SubtypeInput | ✅ GOOD |
| `AdaptiveHeader.tsx` | 201 lines | Responsive header controls | Standalone utility | ✅ EXCELLENT |
| `CollapsibleSection.tsx` | 52 lines | Reusable collapsible UI | Used by FilterPanel | ✅ EXCELLENT |

#### Card Display & Interaction
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `MagicCard.tsx` | 312 lines | **Base card display foundation** | Used by DraggableCard, ListView, PileView, export modals | ✅ GOOD |
| `DraggableCard.tsx` | 276 lines | Interactive card with drag/click | MagicCard, drag/drop system, selection system | ⚠️ COMPLEX |
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

#### UI Infrastructure
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `Modal.tsx` | 85 lines | Reusable modal dialog | Export modals | ✅ EXCELLENT |
| `DropZone.tsx` | 203 lines | Enhanced drop zone overlay | Drag system, visual feedback | ✅ GOOD |
| `DragPreview.tsx` | 84 lines | Visual drag preview | Drag state, card display | ✅ EXCELLENT |
| `ContextMenu.tsx` | 75 lines | Right-click context menu | Context actions, card operations | ✅ EXCELLENT |

#### Export & Utilities
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `TextExportModal.tsx` | 132 lines | Text export interface | Modal, deck formatting | ✅ GOOD |
| `ScreenshotModal.tsx` | 298 lines | Visual deck export | Modal, card display, layout utils | ⚠️ COMPLEX |

### 🔧 Hooks Layer (`src/hooks/`) - 8 Files **ENHANCED ARCHITECTURE**

#### Core Data Management (**REFACTORED**)
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `useCards.ts` | **250 lines** | **Coordination hub** (**REFACTORED** from 580 lines) | useFilters, useSearch, usePagination, useCardSelection, useSearchSuggestions | ✅ **EXCELLENT** |
| `useSearch.ts` | **350 lines** | **Core search and API communication** (**EXTRACTED** from useCards) | scryfallApi, SearchAutocomplete, filter coordination | ✅ **GOOD** |
| `usePagination.ts` | **120 lines** | **Progressive loading and Load More** (**EXTRACTED** from useCards) | useSearch coordination, Load More state | ✅ **EXCELLENT** |
| `useCardSelection.ts` | **50 lines** | **Card selection state management** (**EXTRACTED** from useCards) | DraggableCard, ListView, PileView | ✅ **EXCELLENT** |
| `useSearchSuggestions.ts` | **70 lines** | **Search autocomplete and history** (**EXTRACTED** from useCards) | SearchAutocomplete, search state | ✅ **EXCELLENT** |
| `useFilters.ts` | 120 lines | Filter state management (**PRE-EXISTING EXCELLENT EXAMPLE**) | Used by useCards, FilterPanel | ✅ **EXCELLENT** |

#### UI State Management
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `useSelection.ts` | 310 lines | Dual selection system | DraggableCard, ListView, PileView | ⚠️ COMPLEX |
| `useLayout.ts` | 305 lines | Panel layout management | MTGOLayout, panel components, CSS variables | ✅ GOOD |
| `useDragAndDrop.ts` | 445 lines | Complete drag & drop | DraggableCard, DropZone, context menu | ⚠️ VERY COMPLEX |

#### UI Utilities
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `useContextMenu.ts` | 165 lines | Context menu state | ContextMenu component, card operations | ✅ GOOD |
| `useCardSizing.ts` | 85 lines | Card size management | Card components, size sliders | ✅ **EXCELLENT** |
| `useResize.ts` | 215 lines | Panel resizing handlers | useLayout, resize handles | ✅ GOOD |
| `useSorting.ts` | 270 lines | Sorting state + dual logic | Card components, useCards | ⚠️ COMPLEX |

### 🛠️ Services & Utils Layer (`src/services/`, `src/utils/`, `src/types/`) - 7 Files

#### Service Layer
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `scryfallApi.ts` | **575 lines** | **Complete Scryfall abstraction** | **useSearch hook**, search suggestions | ⚠️ **CRITICAL SIZE** |

#### Utility Layer
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `deckFormatting.ts` | 180 lines | Deck export utilities | Export modals, DeckCardInstance types | ✅ GOOD |
| `screenshotUtils.ts` | **850 lines** | Advanced screenshot generation | ScreenshotModal, html2canvas | ⚠️ **EXTREMELY COMPLEX** |
| `deviceDetection.ts` | 145 lines | Device capability detection | Standalone utility (ready for integration) | ✅ EXCELLENT |

#### Type System
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `card.ts` | **520 lines** | **Foundation type system** | ALL components, hooks, services | ⚠️ **CRITICAL SIZE** |
| `search.ts` | 120 lines | Enhanced search types | SearchAutocomplete, enhanced search | ✅ GOOD |

## 🔗 Integration Point Reference

### Primary Data Flow Patterns (**ENHANCED ARCHITECTURE**)

#### Search & Display Flow (**REFACTORED**)
```
Components (user input) → useCards (coordinator) → useSearch → scryfallApi → Scryfall API
     ↓
API Response → useSearch (results) → useCards (coordination) → Components (display)
     ↓
useFilters (filter state) → useCards (coordination) → useSearch (search params) → scryfallApi
     ↓  
useSorting (sort state) → useCards (coordination) → useSearch (sort triggers) → API/client-side
```

#### Pagination Flow (**NEW ARCHITECTURE**)
```
Components (Load More) → useCards (coordinator) → usePagination (state) → useSearch (API calls)
     ↓
API Response → useSearch → usePagination (update state) → useCards → Components (Smart Card Append)
```

#### User Interaction Flow
```
Components (user actions) → useSelection (selection state) → useContextMenu (actions)
     ↓
useDragAndDrop (interactions) → Components (callbacks) → useCards (deck updates)
     ↓
useLayout (layout state) ← useResize (interactions) ← Components (handles)
```

### Critical Integration Points (**UPDATED**)

#### useCards Hook (Coordination Hub) (**REFACTORED**)
**Incoming Dependencies:**
- `useFilters.ts` - Filter state for search parameters
- `useSearch.ts` - Core search functionality and API communication (**NEW EXTRACTED HOOK**)
- `usePagination.ts` - Load More state and progressive loading (**NEW EXTRACTED HOOK**)
- `useCardSelection.ts` - Card selection state management (**NEW EXTRACTED HOOK**)
- `useSearchSuggestions.ts` - Search autocomplete and history (**NEW EXTRACTED HOOK**)
- Components - Search input, filter controls, Load More triggers

**Outgoing Dependencies:**
- ALL card display components - Search results and selection data
- Export components - Deck and sideboard data
- Layout components - Loading states and error handling

**Hook Coordination Patterns:**
- **Callback Coordination:** Load More coordination between usePagination and useSearch
- **State Synchronization:** Filter state coordination between useFilters and useSearch
- **External API Preservation:** Maintain same interface for components during refactoring

#### MTGOLayout Component (Orchestrator)
**Incoming Dependencies:**
- ALL hooks - useCards (coordinator), useLayout, useSelection, useDragAndDrop, etc.
- ALL major components - FilterPanel, card views, modals
- **Smart Card Append:** Scroll preservation during Load More (**NEW PATTERN**)

**Outgoing Dependencies:**
- Main App.tsx - Primary application interface
- CSS variables - Layout state management

#### Type System Bridge (card.ts)
**Architectural Bridge Functions:**
- `getCardId()` - ScryfallCard → unique ID for collections
- `getSelectionId()` - DeckCardInstance → unique ID for deck/sideboard
- `isCardInstance()` - Type guard for instance vs card
- `createCardInstance()` - ScryfallCard → DeckCardInstance conversion
- `groupInstancesByCard()` - Instance management for display

### Method Signature Reference (**UPDATED**)

#### useCards Hook API (**REFACTORED**)
```typescript
const {
  searchResults,           // PaginatedSearchState<ScryfallCard>
  deckCards,              // DeckCardInstance[]
  sideboardCards,         // DeckCardInstance[]
  isLoading,              // boolean
  error,                  // string | null
  hasMore,                // boolean
  searchCards,            // (query: string) => Promise<void>
  loadMore,               // () => Promise<void> - **SMART CARD APPEND INTEGRATION**
  addToDeck,              // (card: ScryfallCard, quantity?: number) => void
  removeFromDeck,         // (instanceId: string, quantity?: number) => void
  // ... additional coordination methods
} = useCards();
```

#### useSearch Hook API (**NEW EXTRACTED HOOK**)
```typescript
const {
  searchResults,           // PaginatedSearchState<ScryfallCard>
  isLoading,              // boolean
  error,                  // string | null
  hasMore,                // boolean
  searchCards,            // (query: string, filters?: FilterState) => Promise<void>
  loadMoreCards,          // () => Promise<void>
  clearResults,           // () => void
  // ... search-specific methods
} = useSearch();
```

#### usePagination Hook API (**NEW EXTRACTED HOOK**)
```typescript
const {
  currentPage,            // number
  hasMore,                // boolean
  isLoadingMore,          // boolean
  totalCards,             // number
  loadedCards,            // number
  triggerLoadMore,        // () => Promise<void>
  resetPagination,        // () => void
  // ... pagination-specific methods
} = usePagination();
```

#### Smart Card Append Pattern (**NEW INNOVATION**)
```typescript
// Implementation in MTGOLayout.tsx
const existingCardsCount = Math.min(loadedCardsCount, sortedCollectionCards.length);
const existingCards = sortedCollectionCards.slice(0, existingCardsCount);
const newCards = sortedCollectionCards.slice(existingCardsCount);

// Render existing cards with stable keys + new cards with fresh keys
```

#### useFilters Hook API (**EXCELLENT EXAMPLE**)
```typescript
const {
  filters,                // FilterState
  updateFilters,          // (updates: Partial<FilterState>) => void
  resetFilters,           // () => void
  isGoldMode,            // boolean
  activeFilterCount,      // number
  // ... filter-specific methods
} = useFilters();
```

#### scryfallApi Key Functions
```typescript
// Core search functions
searchCards(query: string, options?: SearchOptions): Promise<ScryfallSearchResponse>
searchCardsWithFilters(query: string, filters: FilterState): Promise<ScryfallSearchResponse>
searchCardsWithPagination(query: string, page?: string): Promise<ScryfallSearchResponse>

// Enhanced search
enhancedSearchCards(query: string, filters?: FilterState): Promise<ScryfallSearchResponse>
buildEnhancedSearchQuery(query: string): string

// Progressive loading
loadMoreResults(currentState: PaginatedSearchState): Promise<PaginatedSearchState>

// Autocomplete
autocompleteCardNames(query: string): Promise<string[]>
getSearchSuggestions(query: string): Promise<SearchSuggestion[]>
```

## 🎯 Proven Development Patterns (**NEW SECTION**)

### Hook Extraction Methodology (**PROVEN EFFECTIVE**)

#### When to Apply Hook Extraction
- **Size Threshold:** Hooks exceeding 400-500 lines with multiple major responsibilities
- **Complexity Indicators:** Mixed concerns, difficult maintenance, too many integration points
- **Success Example:** useCards.ts (580 lines → 250 line coordinator + 4 focused hooks)

#### Hook Extraction Process (**VALIDATED**)
1. **Identify Distinct Responsibilities:** Search, pagination, selection, suggestions, etc.
2. **Create Focused Hooks:** Each hook handles one cohesive area of functionality
3. **Maintain Coordinator Hook:** Preserve external API compatibility for components
4. **Implement Coordination Patterns:** Callback coordination, state synchronization
5. **Apply Smart Testing:** Validate zero regressions during extraction

#### Hook Coordination Patterns (**LEARNED FROM EXPERIENCE**)
```typescript
// Callback Coordination Pattern (Load More)
const loadMore = useCallback(async () => {
  await usePagination.triggerLoadMore(); // State management
  await useSearch.loadMoreCards();       // API call
}, [usePagination.triggerLoadMore, useSearch.loadMoreCards]);

// State Synchronization Pattern (Filters)
const searchWithFilters = useCallback((query: string) => {
  const currentFilters = useFilters.filters;
  return useSearch.searchCards(query, currentFilters);
}, [useFilters.filters, useSearch.searchCards]);
```

#### External API Preservation (**CRITICAL SUCCESS FACTOR**)
- **Principle:** Components should not need changes during hook refactoring
- **Implementation:** Coordinator hook maintains exact same external interface
- **Benefit:** Enables large-scale refactoring without component integration work

### Smart Card Append Pattern (**UX INNOVATION**)

#### When to Apply Smart Card Append
- **Scenario:** Load More or pagination operations where scroll position preservation critical
- **Problem Solved:** Eliminates jarring scroll reset to top during data loading
- **Success Example:** Load More in Card view with natural scroll preservation

#### Smart Card Append Implementation (**PROVEN TECHNIQUE**)
```typescript
// Track loaded cards for splitting existing vs new
const [loadedCardsCount, setLoadedCardsCount] = useState(75);

// Split cards for stable vs fresh rendering
const existingCardsCount = Math.min(loadedCardsCount, sortedCollectionCards.length);
const existingCards = sortedCollectionCards.slice(0, existingCardsCount);
const newCards = sortedCollectionCards.slice(existingCardsCount);

// Render separately with appropriate keys
{existingCards.map((card, index) => (
  <DraggableCard key={`existing-${index}`} ... />
))}
{newCards.map((card, index) => (
  <DraggableCard key={`new-${existingCardsCount + index}`} ... />
))}

// Update loaded count on successful Load More
useEffect(() => {
  if (cards.length > loadedCardsCount) {
    setLoadedCardsCount(cards.length);
  }
}, [cards.length, loadedCardsCount]);
```

#### Performance Benefits (**VALIDATED**)
- **Existing Cards:** Maintain stable React keys, no re-rendering
- **New Cards:** Fresh React keys, efficient initial rendering
- **Scroll Position:** Naturally preserved without manual scroll management
- **User Experience:** Smooth, natural pagination without jarring interface resets

### Architecture-Informed Testing (**PROVEN METHODOLOGY**)

#### Risk Assessment Using Architecture Understanding
```typescript
// HIGH RISK (Test Always) - Architecture-informed
- Features using the same hooks being modified (per integration analysis)
- Features with complex state management identified in architecture
- Features sharing data objects (per integration point documentation)
- Features that have broken before from similar changes

// MEDIUM RISK (Quick Verification) - Architecture-informed  
- Features using modified components but simpler integration
- Features that might be affected by UI changes (per dependency flow)
- Features with some dependency on modified systems

// LOW RISK (Skip Testing) - Architecture-informed
- Features that are completely independent (per architecture analysis)
- Features using different hooks/state entirely (per separation analysis)
- Features with no shared dependencies (per integration documentation)
```

#### Testing Workflow Integration (**EFFICIENT APPROACH**)
- **Pre-Session Analysis (2-3 minutes):** Use architecture understanding for risk assessment
- **During Development:** Focus on HIGH risk features only during active work
- **End-of-Session Testing (5 minutes max):** Test HIGH risk + quick MEDIUM risk verification
- **Regression Logging:** Document issues for separate debugging sessions, don't debug during wrap-up

## 🚨 Troubleshooting Patterns (**NEW SECTION**)

### React Hook Rules Troubleshooting (**LEARNED FROM EXPERIENCE**)

#### Common Hook Rules Violations
- **Conditional Hook Calls:** useEffect placed inside conditional logic
- **Hook Order Changes:** Hooks called in different order between renders
- **Loop/Function Hook Calls:** Hooks called inside loops or nested functions

#### Resolution Patterns (**PROVEN FIXES**)
```typescript
// WRONG: Conditional useEffect
if (someCondition) {
  useEffect(() => { ... }, []);
}

// RIGHT: Conditional logic inside useEffect
useEffect(() => {
  if (someCondition) {
    // conditional logic here
  }
}, [someCondition]);

// WRONG: Hook order changes
if (isLoading) {
  const [state, setState] = useState(defaultValue);
}

// RIGHT: Always call hooks, conditional rendering
const [state, setState] = useState(defaultValue);
if (isLoading) {
  return <LoadingSpinner />;
}
```

### Pagination Debugging Methodology (**SERVICE LAYER PATTERNS**)

#### Load More Sequence Issues
**Problem Pattern:** Cards jumping alphabetically (A→C, missing B cards)
**Root Cause Pattern:** Page consumption mismatch between user display and API pagination

#### Investigation Approach (**PROVEN EFFECTIVE**)
1. **Console Log Validation:** Verify API calls, state updates, data flow
2. **Pagination State Analysis:** Check currentPage, loadedCards, totalCards
3. **Data Continuity Check:** Verify alphabetical sequence in loaded results
4. **Service Layer Investigation:** Review loadMoreResults function logic
5. **State Coordination Check:** Verify pagination state flows between hooks

#### Service Layer Debug Patterns
```typescript
// Debug pagination state coordination
console.log('Pagination State:', {
  currentPage: paginationState.currentPage,
  totalCards: paginationState.totalCards,
  loadedCards: paginationState.loadedCards,
  hasMore: paginationState.hasMore
});

// Debug Load More API calls
console.log('Load More Request:', {
  nextPage: paginationState.currentPage + 1,
  query: paginationState.lastQuery,
  filters: paginationState.lastFilters
});

// Debug result continuity
console.log('Card Sequence:', {
  firstCard: results.data[0]?.name,
  lastCard: results.data[results.data.length - 1]?.name,
  totalReturned: results.data.length
});
```

### React Rendering Troubleshooting (**VIEW-SPECIFIC PATTERNS**)

#### Card View vs List View Differences
**Problem Pattern:** Load More works in List view but not Card view
**Root Cause Pattern:** Different rendering approaches (ListView component vs direct JSX mapping)

#### React Virtual DOM Issues (**RENDERING OPTIMIZATION**)
```typescript
// Problem: React not detecting need to re-render
{sortedCollectionCards.map((card) => <DraggableCard ... />)}

// Solution 1: Force re-render with container key
<div key={`collection-grid-${cards.length}`}>
  {sortedCollectionCards.map((card) => <DraggableCard ... />)}
</div>

// Solution 2: Smart Card Append (preferred for UX)
{existingCards.map((card, index) => (
  <DraggableCard key={`existing-${index}`} ... />
))}
{newCards.map((card, index) => (
  <DraggableCard key={`new-${existingCardsCount + index}`} ... />
))}
```

#### Debugging React Rendering Issues (**SYSTEMATIC APPROACH**)
1. **Data Flow Verification:** Confirm state updates working correctly
2. **Component Isolation:** Test rendering in isolation vs integrated
3. **Key Prop Analysis:** Verify React keys for efficient re-rendering
4. **Virtual DOM Investigation:** Use React DevTools to analyze render cycles
5. **Pattern Comparison:** Compare working vs non-working implementations

## ⚠️ Critical Refactoring Priorities (**UPDATED WITH RECENT EXPERIENCE**)

### High Priority - Large File Issues

#### 1. MTGOLayout.tsx (925 lines) - Application Orchestrator
**Status:** Contains Smart Card Append implementation - **PROCEED WITH CAUTION**
**Problems:**
- Mixed responsibilities: layout + state + events + business logic + Smart Card Append
- Difficult to maintain and test due to size
- Too many integration points in single component

**Recommended Refactoring (**UPDATED WITH SMART CARD APPEND CONSIDERATION**):**
```
MTGOLayout.tsx (simplified coordinator)
├── CollectionArea.tsx (collection-specific logic + Smart Card Append)
├── DeckArea.tsx (deck-specific logic)  
├── SideboardArea.tsx (sideboard-specific logic)
└── LayoutOrchestrator.tsx (pure layout management)
```

**Special Consideration:** Smart Card Append implementation must be preserved during extraction

#### 2. scryfallApi.ts (575 lines) - Service Layer (**LOWER PRIORITY AFTER HOOK SUCCESS**)
**Status:** Working well with extracted hooks, refactor when needed
**Problems:**
- Multiple major responsibilities but hooks extraction reduced pressure
- Can be addressed using proven hook extraction patterns if needed

**Recommended Approach:** Apply hook extraction methodology if service layer becomes problematic

#### 3. card.ts (520 lines) - Type System Foundation (**STABLE, LOWER PRIORITY**)
**Status:** Working well, refactor only if growth continues
**Problems:**
- Types mixed with utilities but foundation is solid
- Can be addressed using proven separation patterns

#### 4. screenshotUtils.ts (850 lines) - Algorithm Complexity (**LOWEST PRIORITY**)
**Status:** Complex but focused, working well
**Problems:**
- Very complex but properly isolated
- Can use extraction patterns if maintenance becomes difficult

### Medium Priority - Architecture Improvements (**ENHANCED WITH PATTERNS**)

#### Service Layer Abstraction
- Apply hook extraction patterns to service layer if needed
- Implement caching and optimization layers using proven approaches
- Better separation using documented coordination patterns

#### Component Consolidation Opportunities
- Apply Smart Card Append pattern to other pagination scenarios
- Extract shared utilities using proven component patterns
- Use established patterns for input and layout components

### Low Priority - Performance & Polish (**ENHANCED WITH PROVEN PATTERNS**)

#### Performance Optimizations
- Apply Smart Card Append pattern to other scenarios requiring scroll preservation
- Consider hook extraction methodology for other large components
- Optimize re-render triggers using documented patterns

#### Code Quality Enhancements
- Apply proven patterns and guidelines for new development
- Enhanced type safety using established patterns
- Better error handling using documented approaches

## 📋 Development Guidelines (**ENHANCED WITH PROVEN PATTERNS**)

### Component Size & Responsibility (**UPDATED WITH EXPERIENCE**)
- **Target Size:** Keep components under 200 lines when possible
- **Single Responsibility:** New components should have clear, focused purposes
- **Smart Card Append:** Apply pattern when pagination scenarios require scroll preservation
- **Composition Over Complexity:** Build complex features through component composition
- **Integration Interfaces:** Hide internal complexity behind simple, clean prop interfaces

### Hook Development (**ENHANCED WITH EXTRACTION EXPERIENCE**)
- **Size Guidelines:** Keep hooks under 200 lines when possible, 300 lines acceptable for focused features, 400+ lines indicates need for extraction
- **Extraction Methodology:** Apply proven hook extraction patterns when size threshold exceeded
- **Responsibility Guidelines:** Each hook should manage one cohesive area of functionality
- **Coordination Patterns:** Use callback coordination and state synchronization patterns for multi-hook scenarios
- **Integration Guidelines:** Clean APIs, minimal dependencies, service abstraction for complex external interactions
- **Performance Guidelines:** Constraint enforcement, persistence strategy, optimization patterns

### Service & Utility Development (**ENHANCED WITH PROVEN APPROACHES**)
- **File Size Target:** Keep service files under 300 lines when possible
- **Hook Integration:** Design for clean integration with extracted hooks
- **Single Responsibility:** Each service should handle one major area of functionality
- **Clean APIs:** Hide internal complexity behind simple, focused interfaces
- **Error Handling:** Comprehensive error handling with meaningful messages

### Type System Management (**ENHANCED WITH BRIDGE PATTERNS**)
- **Foundation First:** Core types should be stable and comprehensive
- **Utility Separation:** Keep type definitions separate from utility implementations
- **Bridge Pattern:** Use architectural bridges to abstract complex type relationships
- **Progressive Enhancement:** Design types to support feature evolution

## 🎯 Architecture Evolution Roadmap (**UPDATED WITH PROVEN PATTERNS**)

### Phase 1: Apply Proven Patterns (Ongoing)
1. **Hook Extraction Pattern:** Available for other large hooks as needed
2. **Smart Card Append Pattern:** Apply to other pagination scenarios requiring scroll preservation
3. **Coordination Patterns:** Use proven callback coordination and state synchronization approaches
4. **Testing Methodology:** Apply architecture-informed testing for all development

### Phase 2: Targeted Refactoring (When Needed)
1. **MTGOLayout Refactoring** - Extract area-specific components (preserve Smart Card Append)
2. **Service Layer Enhancement** - Apply hook patterns if needed
3. **Component Consolidation** - Extract shared utilities and patterns using proven approaches
4. **Enhanced Error Handling** - Improve error boundaries using documented patterns

### Phase 3: Performance & Polish (Future)
1. **Performance Optimization** - Apply Smart Card Append and hook extraction patterns
2. **Code Quality Enhancement** - Additional refactoring using proven methodologies
3. **Testing Infrastructure** - Comprehensive testing coverage using established approaches
4. **Documentation Enhancement** - Update guides with newly proven patterns

### Phase 4: Advanced Features (Future)
1. **Pattern Library Expansion** - Document additional proven patterns as they emerge
2. **Performance Monitoring** - Performance tracking and optimization using established approaches
3. **Architecture Monitoring** - Automated checks for file size and complexity
4. **Advanced Type Safety** - More sophisticated type system features using proven patterns

## 🏆 Architecture Success Patterns (**ENHANCED WITH PROVEN EXAMPLES**)

### Excellent Examples to Follow

#### Perfect Utility Components
- **CollapsibleSection.tsx** (52 lines) - Single responsibility, accessibility, reusable
- **GoldButton.tsx** (25 lines) - Perfect micro-component with clear purpose
- **Modal.tsx** (85 lines) - Clean, reusable with proper accessibility

#### Successful Hook Extraction (**PROVEN EXAMPLES**)
- **useFilters.ts** (120 lines) - **ORIGINAL EXCELLENT EXAMPLE** - Perfect separation and clean API
- **usePagination.ts** (120 lines) - **NEW EXCELLENT EXAMPLE** - Extracted from useCards, focused responsibility
- **useCardSelection.ts** (50 lines) - **NEW EXCELLENT EXAMPLE** - Clean state management, minimal API
- **useSearchSuggestions.ts** (70 lines) - **NEW EXCELLENT EXAMPLE** - Focused autocomplete functionality
- **useCardSizing.ts** (85 lines) - Simple state with constraints and persistence

#### Hook Coordination Success (**PROVEN COORDINATION**)
- **useCards.ts** (250 lines) - **COORDINATION EXAMPLE** - Successfully coordinates 4 extracted hooks
- **Load More Coordination** - Proven callback coordination between usePagination and useSearch
- **Filter Integration** - Proven state synchronization between useFilters and useSearch

#### UX Innovation Success (**PROVEN PATTERN**)
- **Smart Card Append** - **UX INNOVATION EXAMPLE** - Scroll preservation during Load More operations
- **Performance Optimization** - Only new cards re-render, existing cards maintain stable React keys
- **Natural User Experience** - No jarring scroll resets, smooth pagination workflow

#### Clean Service Design
- **deckFormatting.ts** (180 lines) - Focused utilities for specific purpose
- **deviceDetection.ts** (145 lines) - Comprehensive detection with clear API
- **search.ts** (120 lines) - Well-organized type definitions

### Patterns to Avoid (**ANTI-PATTERNS FROM EXPERIENCE**)

#### Size & Complexity Issues
- **Monolithic Hooks:** Single hooks with multiple major responsibilities (useCards.ts before refactoring)
- **Mixed Concerns:** Types mixed with utilities, layout mixed with business logic
- **Complex Dependencies:** Too many integration points in single component/hook

#### Hook Coordination Anti-Patterns
- **Tight Coupling:** Hooks knowing too much about each other's internals
- **State Leakage:** Complex state management patterns exposed externally
- **Missing Coordination:** Extracted hooks not properly coordinated for complex workflows like Load More

#### React Rendering Anti-Patterns
- **Missing Key Props:** Causing unnecessary re-renders or preventing necessary updates
- **Full Component Remount:** Using container key props that reset scroll position
- **Hook Rules Violations:** Conditional hook calls, changing hook order

#### Integration Anti-Patterns
- **Tight Coupling:** Components knowing too much about hook internals
- **State Leakage:** Complex state management patterns exposed to components
- **API Exposure:** Direct API dependencies in multiple components
- **Coordination Gaps:** Missing state synchronization between related hooks

## 📚 Quick Reference Cards (**ENHANCED WITH PROVEN PATTERNS**)

### "I want to modify search functionality"
**Primary Files:** `useSearch.ts` (**EXTRACTED HOOK**), `scryfallApi.ts`, `SearchAutocomplete.tsx`  
**Secondary Files:** `search.ts`, `useFilters.ts`, `useCards.ts` (coordinator)  
**Pattern:** API changes → useSearch updates → useCards coordination → component integration  
**Proven Pattern:** Hook extraction successful - useSearch is focused and maintainable

### "I want to add filter functionality"  
**Primary Files:** `useFilters.ts` (**EXCELLENT EXAMPLE**), `FilterPanel.tsx`, `scryfallApi.ts`  
**Secondary Files:** `CollapsibleSection.tsx`, specific filter components  
**Pattern:** Filter state → UI components → API integration via useSearch  
**Success Example:** useFilters.ts is perfect example of focused hook responsibility

### "I want to modify card display"
**Primary Files:** `MagicCard.tsx`, `DraggableCard.tsx`  
**Secondary Files:** `ListView.tsx`, `PileView.tsx`, `card.ts`  
**Pattern:** Base component → interactive wrapper → view integration  
**Smart Card Append:** Apply pattern if pagination scenarios need scroll preservation

### "I want to add view modes"
**Primary Files:** `ListView.tsx` OR `PileView.tsx`, `useLayout.ts`  
**Secondary Files:** `MTGOLayout.tsx` (**contains Smart Card Append**), view-specific components  
**Pattern:** View logic → layout state → orchestrator integration  
**Caution:** MTGOLayout contains Smart Card Append implementation - coordinate changes carefully

### "I want to modify pagination"
**Primary Files:** `usePagination.ts` (**EXTRACTED HOOK**), `useSearch.ts` (**EXTRACTED HOOK**), `MTGOLayout.tsx` (**Smart Card Append**)  
**Secondary Files:** `scryfallApi.ts`, `useCards.ts` (coordinator)  
**Pattern:** Pagination state → search coordination → API integration → Smart Card Append rendering  
**Proven Pattern:** Hook coordination working well, Smart Card Append provides excellent UX

### "I want to modify drag & drop"
**Primary Files:** `useDragAndDrop.ts`, `DraggableCard.tsx`, `DropZone.tsx`  
**Secondary Files:** Context menu integration, selection system  
**Pattern:** Interaction logic → component behavior → integration  
**Caution:** useDragAndDrop is 445 lines but necessarily complex - consider extraction if grows

### "I want to add export functionality"
**Primary Files:** `deckFormatting.ts` OR `screenshotUtils.ts`, export modals  
**Secondary Files:** `Modal.tsx`, layout components  
**Pattern:** Utility functions → modal components → main integration  
**Caution:** screenshotUtils is 850 lines with complex algorithms - consider extraction methodology

### "I want to extract a large hook"
**Primary Files:** Identify target hook, create focused extracted hooks  
**Proven Pattern:** Hook extraction methodology validated through useCards success  
**Process:** Identify responsibilities → Create focused hooks → Implement coordinator → Apply coordination patterns → Smart testing  
**Success Example:** useCards.ts (580→250 lines) + 4 focused hooks with zero regressions

### "I want to add pagination with scroll preservation"
**Primary Files:** Component with pagination, implement Smart Card Append pattern  
**Proven Pattern:** Smart Card Append for natural scroll preservation  
**Process:** Track loaded count → Split existing/new cards → Render with stable/fresh keys → Update state appropriately  
**Success Example:** MTGOLayout.tsx Smart Card Append eliminates scroll reset during Load More

---

**Created:** June 7, 2025 from comprehensive architecture review  
**Enhanced:** June 7, 2025 with proven patterns from useCards architecture overhaul  
**Status:** Complete reference guide with validated methodologies for MTG Deck Builder development  
**Proven Patterns:** Hook extraction, Smart Card Append, coordination approaches, testing methodology  
**Usage:** Reference before any development work to understand integration points and apply proven patterns  
**Maintenance:** Update as architecture evolves and new patterns are proven through development experience