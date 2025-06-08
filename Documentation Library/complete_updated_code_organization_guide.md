# MTG Deck Builder - Code Organization Guide

**Created:** June 7, 2025  
**Enhanced:** June 7, 2025 (Post-MTGOLayout Refactoring with Proven Component Extraction Patterns)  
**Purpose:** Comprehensive reference for codebase organization, integration points, development patterns, and proven methodologies  
**Source:** Architecture review synthesis + useCards architecture overhaul experience + MTGOLayout component refactoring + proven pattern validation  
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
- `src/components/MTGOLayout.tsx` (coordinator), area components (`CollectionArea.tsx`, `DeckArea.tsx`, `SideboardArea.tsx`)

**Pattern:** View logic → layout state → area component integration → coordinator integration
**Architecture:** Area components handle view mode rendering, coordinator manages state
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
- `src/components/CollectionArea.tsx` - Load More integration

**Pattern:** Update pagination state → Coordinate with search → API integration → CollectionArea rendering
**Smart Card Append Pattern:** For scroll preservation during Load More operations

### Modifying MTGOLayout or Area-Specific Functionality
**Files to Modify:**
- `src/components/MTGOLayout.tsx` (**REFACTORED** - 450 lines coordinator)
- `src/components/CollectionArea.tsx` - Collection logic and Load More
- `src/components/DeckArea.tsx` - Deck management and display
- `src/components/SideboardArea.tsx` - Sideboard functionality

**Pattern:** Area-specific changes → individual area components, coordination changes → MTGOLayout coordinator
**Proven Pattern:** Component extraction successful - focused area components are maintainable and testable
**Architecture:** Clean coordinator pattern with area-specific component separation

## 📁 Complete File Organization Matrix

### 🎨 Components Layer (`src/components/`) - 21 Files **ENHANCED ARCHITECTURE**

#### Core Layout & Infrastructure (**REFACTORED**)
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `MTGOLayout.tsx` | 450 lines | **Clean application coordinator** (**REFACTORED**) | ALL hooks, area components, modal management | ✅ **EXCELLENT** |
| `CollectionArea.tsx` | 200 lines | **Collection logic and Load More** (**NEW**) | useCards, sorting, view modes, Load More integration | ✅ **EXCELLENT** |
| `DeckArea.tsx` | 200 lines | **Deck management and display** (**NEW**) | useCards, view modes, export controls, instance handling | ✅ **EXCELLENT** |
| `SideboardArea.tsx` | 200 lines | **Sideboard functionality** (**NEW**) | useCards, view modes, resize handling, instance management | ✅ **EXCELLENT** |
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
API Response → useSearch (results) → useCards (coordination) → Area Components (display)
     ↓
useFilters (filter state) → useCards (coordination) → useSearch (search params) → scryfallApi
     ↓  
useSorting (sort state) → useCards (coordination) → useSearch (sort triggers) → API/client-side
```

#### Component Architecture Flow (**NEW ARCHITECTURE**)
```
MTGOLayout (coordinator) → Hook Management → State Coordination
     ↓
Area Components (CollectionArea, DeckArea, SideboardArea) → Focused UI Logic
     ↓
Base Components (MagicCard, ListView, PileView) → Shared Display Logic
```

#### Pagination Flow (**NEW ARCHITECTURE**)
```
Components (Load More) → useCards (coordinator) → usePagination (state) → useSearch (API calls)
     ↓
API Response → useSearch → usePagination (update state) → useCards → CollectionArea (Smart Card Append)
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
- ALL area components - Search results and selection data through coordinator
- Export components - Deck and sideboard data
- Layout components - Loading states and error handling

**Hook Coordination Patterns:**
- **Callback Coordination:** Load More coordination between usePagination and useSearch
- **State Synchronization:** Filter state coordination between useFilters and useSearch
- **External API Preservation:** Maintain same interface for components during refactoring

#### MTGOLayout Component (Coordinator) (**REFACTORED**)
**Incoming Dependencies:**
- ALL hooks - useCards (coordinator), useLayout, useSelection, useDragAndDrop, etc.
- Area components - CollectionArea, DeckArea, SideboardArea (**NEW ARCHITECTURE**)
- Modal components - Export modals and other dialogs

**Outgoing Dependencies:**
- Main App.tsx - Primary application interface
- CSS variables - Layout state management

**Component Coordination Patterns:**
- **Hook Management:** All hooks integrated in coordinator component
- **Prop Interface Coordination:** Clean prop passing to area components
- **State Management:** Centralized state coordination without UI responsibilities

#### Area Components (New Architecture) (**NEW INTEGRATION POINTS**)
**CollectionArea.tsx:**
- **Incoming:** Search results, Load More state, view mode state from coordinator
- **Outgoing:** User interactions, Load More triggers back to coordinator
- **Special Features:** Load More integration, Smart Card Append capability

**DeckArea.tsx:**
- **Incoming:** Deck cards, export state, view mode state from coordinator
- **Outgoing:** Deck modifications, export triggers back to coordinator
- **Special Features:** Export control integration, instance-based card handling

**SideboardArea.tsx:**
- **Incoming:** Sideboard cards, resize state, view mode state from coordinator
- **Outgoing:** Sideboard modifications, resize events back to coordinator
- **Special Features:** Resize handling, instance management

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
  loadMore,               // () => Promise<void> - **COORDINATOR INTEGRATION**
  addToDeck,              // (card: ScryfallCard, quantity?: number) => void
  removeFromDeck,         // (instanceId: string, quantity?: number) => void
  // ... additional coordination methods
} = useCards();
```

#### Area Component APIs (**NEW ARCHITECTURE**)
```typescript
// CollectionArea.tsx
interface CollectionAreaProps {
  searchResults: PaginatedSearchState<ScryfallCard>;
  isLoading: boolean;
  hasMore: boolean;
  onLoadMore: () => Promise<void>;
  onCardSelect: (card: ScryfallCard) => void;
  // ... focused collection props
}

// DeckArea.tsx  
interface DeckAreaProps {
  deckCards: DeckCardInstance[];
  onCardMove: (instanceId: string, destination: string) => void;
  onExport: (format: string) => void;
  // ... focused deck props
}

// SideboardArea.tsx
interface SideboardAreaProps {
  sideboardCards: DeckCardInstance[];
  onResize: (size: number) => void;
  // ... focused sideboard props
}
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

#### Smart Card Append Pattern (**UX INNOVATION**)
```typescript
// Implementation in CollectionArea.tsx
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

## 🎯 Proven Development Patterns (**ENHANCED SECTION**)

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

### Component Extraction Methodology (**PROVEN EFFECTIVE**)

#### When to Apply Component Extraction
- **Size Threshold:** Components exceeding 800-900 lines with multiple UI areas
- **Complexity Indicators:** Mixed UI responsibilities, difficult maintenance, too many integration points
- **Success Example:** MTGOLayout.tsx (925 lines → 450 line coordinator + 3 focused area components)

#### Component Extraction Process (**VALIDATED**)
1. **Identify UI Areas:** Collection, deck, sideboard, or other distinct interface areas
2. **Create Area-Specific Components:** Each component handles one cohesive UI area
3. **Maintain Coordinator Component:** Preserve hook integration and external API compatibility
4. **Implement Integration Patterns:** Clean prop interfaces and callback coordination
5. **Apply Smart Testing:** Validate zero regressions during extraction

#### Component Coordination Patterns (**LEARNED FROM EXPERIENCE**)
```typescript
// Coordinator Component Pattern (MTGOLayout)
const MTGOLayout = () => {
  // All hook integration in coordinator
  const cardsState = useCards();
  const selectionState = useSelection();
  const dragDropState = useDragAndDrop();
  
  // Pass focused props to area components
  return (
    <div className="mtgo-layout">
      <CollectionArea 
        cards={cardsState.searchResults}
        onLoadMore={cardsState.loadMore}
        // ... focused props only
      />
      <DeckArea 
        deckCards={cardsState.deckCards}
        onCardMove={cardsState.moveCard}
        // ... focused props only
      />
      <SideboardArea 
        sideboardCards={cardsState.sideboardCards}
        // ... focused props only
      />
    </div>
  );
};

// Area Component Pattern (CollectionArea, DeckArea, SideboardArea)
const CollectionArea = ({ cards, onLoadMore, ... }) => {
  // Area-specific logic only
  // No direct hook access, clean prop interface
  // Focused responsibilities for collection area
};
```

#### External API Preservation (**CRITICAL SUCCESS FACTOR**)
- **Principle:** Other components should not need changes during component refactoring
- **Implementation:** Coordinator component maintains exact same hook integration
- **Benefit:** Enables large-scale refactoring without integration work across the application

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
- Area components when coordinator or shared hooks modified

// MEDIUM RISK (Quick Verification) - Architecture-informed  
- Features using modified components but simpler integration
- Features that might be affected by UI changes (per dependency flow)
- Features with some dependency on modified systems
- Independent area components when other ar