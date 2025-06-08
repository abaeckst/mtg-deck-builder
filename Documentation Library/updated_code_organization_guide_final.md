# MTG Deck Builder - Code Organization Guide

**Created:** June 7, 2025  
**Enhanced:** June 8, 2025 (Post-Reconciliation with Advanced UI/UX Patterns + Debugging Methodologies)  
**Purpose:** Comprehensive reference for codebase organization, integration points, development patterns, advanced UI/UX techniques, and sophisticated debugging methodologies  
**Source:** Architecture review synthesis + useCards architecture overhaul experience + MTGOLayout refactoring + Header UI/UX redesign + advanced debugging methodology development  
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
- `src/components/DraggableCard.tsx` - Interactive card wrapper with **ENHANCED DRAG PREVIEW**
- `src/types/card.ts` - Card type definitions and utilities

**Pattern:** Enhance base card component → Update interactive wrapper → Add type support
**🆕 Enhanced Pattern:** Apply 3x transform scaling for previews, zone-relative positioning for feedback

### Adding View Modes
**Files to Modify:**
- `src/components/ListView.tsx` OR `src/components/PileView.tsx` - Specific view logic
- `src/hooks/useLayout.ts` - View mode state management with **UNIFIED STATE PATTERNS**
- `src/components/DeckArea.tsx` OR `src/components/SideboardArea.tsx` - View mode integration with **MTGO STYLING**

**Pattern:** Implement view-specific logic → Update layout state → Integrate with area components
**🆕 Advanced Pattern:** Apply unified state management for multi-component coordination
**Smart Card Append Pattern:** For pagination scenarios requiring scroll preservation

### Adding Hook Features
**Files to Review First:**
- `src/hooks/useCards.ts` - Primary coordination hub (**REFACTORED** - now 250 lines)
- `src/hooks/useFilters.ts` - Filter state management (**EXCELLENT EXAMPLE** - clean separation)
- Integration pattern depends on feature type

**Pattern:** Assess if new hook needed → Extract if growing too large → Maintain clean APIs
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

### Adding Pagination Features
**Files to Modify:**
- `src/hooks/usePagination.ts` - Pagination state management (**EXTRACTED HOOK**)
- `src/hooks/useSearch.ts` - Search integration with pagination (**EXTRACTED HOOK**)
- `src/services/scryfallApi.ts` - Load More API logic

**Pattern:** Update pagination state → Coordinate with search → API integration
**Smart Card Append Pattern:** For scroll preservation during Load More operations

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

### 🎨 Components Layer (`src/components/`) - 19 Files **ENHANCED ARCHITECTURE**

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

#### Card Display & Interaction (**ENHANCED WITH UX IMPROVEMENTS**)
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `MagicCard.tsx` | 312 lines | **Base card display foundation** | Used by DraggableCard, ListView, PileView, export modals | ✅ GOOD |
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

### 🔧 Hooks Layer (`src/hooks/`) - 11 Files **ENHANCED ARCHITECTURE**

#### Core Data Management (**REFACTORED + ENHANCED**)
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `useCards.ts` | **250 lines** | **Coordination hub** (**REFACTORED** from 580 lines) | useFilters, useSearch, usePagination, useCardSelection, useSearchSuggestions | ✅ **EXCELLENT** |
| `useSearch.ts` | **350 lines** | **Core search and API communication** (**EXTRACTED** from useCards) | scryfallApi, SearchAutocomplete, filter coordination | ✅ **GOOD** |
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

#### 🆕 Styling Infrastructure (**ENHANCED WITH MTGO FOUNDATION**)
| File | Size | Responsibility | Integration Points | Health |
|------|------|----------------|-------------------|---------|
| `MTGOLayout.css` | **1,450+ lines** | **Complete application styling foundation** (**RESTORED**) | ALL components, **MTGO styling**, **Responsive systems** | ✅ **CRITICAL** |

## 🔗 Integration Point Reference

### 🆕 Primary Data Flow Patterns (**ENHANCED ARCHITECTURE**)

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

#### 🆕 Unified State Flow (**NEW ARCHITECTURE**)
```
DeckArea (user input) → useLayout (unified state) → SideboardArea (automatic inheritance)
     ↓
Single controls → Unified state updates → Both areas re-render simultaneously
     ↓
State migration → Legacy state detection → Automatic upgrade → User preference preservation
```

#### Pagination Flow (**NEW ARCHITECTURE**)
```
Components (Load More) → useCards (coordinator) → usePagination (state) → useSearch (API calls)
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

### 🆕 Critical Integration Points (**UPDATED + ENHANCED**)

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

**🆕 Hook Coordination Patterns:**
- **Callback Coordination:** Load More coordination between usePagination and useSearch
- **State Synchronization:** Filter state coordination between useFilters and useSearch
- **External API Preservation:** Maintain same interface for components during refactoring

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

#### Type System Bridge (card.ts)
**Architectural Bridge Functions:**
- `getCardId()` - ScryfallCard → unique ID for collections
- `getSelectionId()` - DeckCardInstance → unique ID for deck/sideboard
- `isCardInstance()` - Type guard for instance vs card
- `createCardInstance()` - ScryfallCard → DeckCardInstance conversion
- `groupInstancesByCard()` - Instance management for display

### 🆕 Method Signature Reference (**UPDATED + ENHANCED**)

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

#### 🆕 useLayout Hook API (**NEW UNIFIED STATE MANAGEMENT**)
```typescript
const {
  // Unified Deck/Sideboard State
  viewModes: {
    deckSideboard,         // 'card' | 'pile' | 'list'
    collection,            // 'card' | 'pile' | 'list' (separate)
  },
  cardSizes: {
    deckSideboard,         // number (1.3-2.5 range)
    collection,            // number (0-2 range)
  },
  
  // Unified Coordination Functions
  updateDeckSideboardViewMode,    // (mode: string) => void
  updateDeckSideboardCardSize,    // (size: number) => void
  updateCollectionViewMode,       // (mode: string) => void
  updateCollectionCardSize,       // (size: number) => void
  
  // State Migration
  migrateLegacyState,            // () => void (automatic)
  
  // ... layout-specific methods
} = useLayout();
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

#### 🆕 Smart Card Append Pattern (**UX INNOVATION**)
```typescript
// Implementation in area components (CollectionArea, etc.)
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

#### 🆕 ViewModeDropdown Component API (**NEW COMPONENT**)
```typescript
const ViewModeDropdown = ({
  currentView,             // 'card' | 'pile' | 'list'
  onViewChange,           // (mode: string) => void
  isInOverflow,           // boolean (context awareness)
  className,              // string (optional)
}) => {
  // Context-aware z-index: 2000000 (overflow) vs 600000 (normal)
  // Professional MTGO styling with proper animations
  // Fixed positioning with dynamic coordinate calculation
};
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

## 🎯 🆕 Advanced Development Patterns (**NEW SECTION**)

### 🆕 Component Extraction Methodology (**PROVEN EFFECTIVE**)

#### When to Apply Component Extraction
- **Size Threshold:** Components exceeding 800-900 lines with multiple major responsibilities
- **Complexity Indicators:** Mixed concerns, difficult maintenance, too many integration points
- **Success Example:** MTGOLayout.tsx (925 lines → 450 line coordinator + 3 focused area components)

#### Component Extraction Process (**VALIDATED**)
1. **Identify Distinct Areas:** Collection, deck, sideboard responsibilities clearly separable
2. **Create Focused Components:** Each component handles one cohesive area of functionality
3. **Maintain Coordinator:** Preserve external API compatibility and hook integration
4. **Implement Clean Interfaces:** Props-based communication between coordinator and areas
5. **Apply Smart Testing:** Validate zero regressions during extraction

#### Component Coordination Patterns (**LEARNED FROM EXPERIENCE**)
```typescript
// Area Component Pattern
const CollectionArea = ({ cards, onLoadMore, viewMode, cardSize, ...props }) => {
  // Area-specific rendering and interaction logic
  // All state management through props from coordinator
  return <div className="collection-area">{/* Area-specific UI */}</div>;
};

// Coordinator Pattern
const MTGOLayout = () => {
  const cards = useCards();
  const layout = useLayout();
  
  return (
    <>
      <CollectionArea cards={cards} {...layout.collection} />
      <DeckArea cards={cards} {...layout.deckSideboard} />
      <SideboardArea cards={cards} {...layout.deckSideboard} />
    </>
  );
};
```

#### External API Preservation (**CRITICAL SUCCESS FACTOR**)
- **Principle:** Other components should not need changes during component refactoring
- **Implementation:** Coordinator maintains exact same external interface for App.tsx
- **Benefit:** Enables large-scale refactoring without affecting external integrations

### 🆕 Unified State Management Patterns (**ADVANCED COORDINATION**)

#### When to Apply Unified State Management
- **Scenario:** Multiple components requiring synchronized behavior (deck + sideboard)
- **Problem Solved:** Eliminates interface duplication and user confusion
- **Success Example:** Single view/size controls affecting both deck and sideboard areas

#### Unified State Implementation (**PROVEN TECHNIQUE**)
```typescript
// Unified State Architecture
const useLayout = () => {
  // Single state for related components
  const [deckSideboardView, setDeckSideboardView] = useState('card');
  const [deckSideboardSize, setDeckSideboardSize] = useState(1.3);
  
  // Separate state for independent components
  const [collectionView, setCollectionView] = useState('card');
  const [collectionSize, setCollectionSize] = useState(1);
  
  // Coordination functions
  const updateDeckSideboardViewMode = (mode) => {
    setDeckSideboardView(mode);
    // Automatically applies to both deck and sideboard
  };
  
  // Automatic migration support
  useEffect(() => {
    migrateLegacyState();
  }, []);
};
```

#### State Migration Patterns (**USER EXPERIENCE PRESERVATION**)
```typescript
// Legacy State Migration
const migrateLegacyState = () => {
  const legacyDeckView = localStorage.getItem('deckViewMode');
  const legacySideboardView = localStorage.getItem('sideboardViewMode');
  
  if (legacyDeckView && !localStorage.getItem('deckSideboardViewMode')) {
    // Use deck preference for unified state
    localStorage.setItem('deckSideboardViewMode', legacyDeckView);
    localStorage.removeItem('deckViewMode');
    localStorage.removeItem('sideboardViewMode');
  }
};
```

### 🆕 Responsive Design Systems (**PRIORITY-BASED ADAPTATION**)

#### When to Apply Responsive Design Systems
- **Scenario:** Complex interfaces requiring intelligent space adaptation
- **Problem Solved:** Professional responsive behavior with priority-based control management
- **Success Example:** Header controls with overflow menu and dynamic hiding

#### Responsive Implementation (**PROVEN TECHNIQUE**)
```typescript
// Priority-Based Control Management
const useDynamicControls = () => {
  const [hiddenControls, setHiddenControls] = useState([]);
  const priorityOrder = ['actions', 'size', 'sort', 'view']; // Hide in reverse
  
  // ResizeObserver for dynamic space detection
  useEffect(() => {
    const observer = new ResizeObserver(entries => {
      const { width } = entries[0].contentRect;
      const controlsToHide = calculateHiddenControls(width);
      setHiddenControls(controlsToHide);
    });
    
    observer.observe(headerRef.current);
    return () => observer.disconnect();
  }, []);
  
  const showOverflowMenu = hiddenControls.length > 0;
  return { hiddenControls, showOverflowMenu };
};
```

#### Context-Aware Component Pattern (**SOPHISTICATED BEHAVIOR**)
```typescript
// Context-Aware Z-Index Management
const ViewModeDropdown = ({ isInOverflow, ...props }) => {
  const zIndex = isInOverflow ? 2000000 : 600000;
  const positioning = isInOverflow ? 'fixed' : 'absolute';
  
  const style = {
    zIndex,
    position: positioning,
    ...calculateDynamicPosition(isInOverflow)
  };
  
  return <div style={style}>{/* Dropdown content */}</div>;
};
```

### 🆕 MTGO Styling Foundation (**PROFESSIONAL THEME SYSTEM**)

#### When to Apply MTGO Styling
- **Scenario:** Professional dark theme interfaces requiring authentic appearance
- **Achievement:** Consistent dark gradient styling with proper visual hierarchy
- **Success Example:** All header areas with unified MTGO appearance

#### MTGO Foundation Implementation (**PROVEN TECHNIQUE**)
```css
/* MTGO Foundation Pattern */
.mtgo-header {
  background: linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 100%);
  border: 1px solid #444;
  border-top: 1px solid #666;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
  color: #ffffff;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

.mtgo-button {
  background: linear-gradient(180deg, #333333 0%, #222222 100%);
  border: 1px solid #555555;
  color: #ffffff;
  border-radius: 2px;
  padding: 4px 8px;
}

.mtgo-button:hover {
  background: linear-gradient(180deg, #4a4a4a 0%, #333333 100%);
}
```

#### Visual Hierarchy System (**PROFESSIONAL DESIGN**)
```css
/* MTGO Typography Hierarchy */
.mtgo-title {
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

.mtgo-subtitle {
  font-size: 14px;
  color: #cccccc;
  margin-left: 8px;
}

.mtgo-controls {
  font-size: 12px;
  color: #ffffff;
}
```

### 🆕 Enhanced UX Patterns (**TRANSFORM-BASED IMPROVEMENTS**)

#### Transform-Based Enhancement Pattern
**When to Apply:** UI elements requiring enhanced visibility and professional feedback
```css
/* 3x Transform Scaling Pattern */
.drag-preview {
  transform: scale(3);
  transform-origin: top left;
  /* More flexible than size-based scaling */
}

/* Zone-Relative Centering Pattern */
.drop-zone-feedback {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  /* Perfect centering for any zone size */
}
```

#### Component Isolation Pattern (**MULTI-INSTANCE MANAGEMENT**)
```typescript
// Component State Isolation
const DraggableCard = ({ isBeingDragged, isDragActive }) => {
  // Use specific props (isBeingDragged) vs global state (isDragActive)
  // Prevents unintended visual side effects on other instances
  const cardStyle = isBeingDragged ? {
    transform: 'rotate(5deg)',
    cursor: 'grabbing'
  } : {};
  
  return <div style={cardStyle}>{/* Card content */}</div>;
};
```

## 🚨 🆕 Advanced Debugging Patterns (**NEW SECTION**)

### 🆕 Browser Diagnostic Methodology (**SYSTEMATIC PROBLEM RESOLUTION**)

#### When to Apply Browser Diagnostics
- **Scenario:** User interaction issues where elements appear correct but don't respond
- **Problem Types:** Element interception, CSS property verification, DOM layout analysis
- **Success Example:** Resize handle accessibility debugging with element interception detection

#### Browser Diagnostic Implementation (**PROVEN TECHNIQUE**)
```javascript
// Systematic DOM Investigation Pattern
const diagnosticScript = () => {
  // Element Detection at Problem Area
  const element = document.elementFromPoint(x, y);
  console.log('Element at interaction point:', element);
  
  // Property Verification
  const computedStyle = getComputedStyle(element);
  console.log('Element properties:', {
    cursor: computedStyle.cursor,
    zIndex: computedStyle.zIndex,
    pointerEvents: computedStyle.pointerEvents,
    width: element.offsetWidth,
    height: element.offsetHeight
  });
  
  // Layer Analysis
  const elementsAtPoint = document.elementsFromPoint(x, y);
  elementsAtPoint.forEach((el, index) => {
    console.log(`Layer ${index}:`, {
      element: el.className,
      zIndex: getComputedStyle(el).zIndex
    });
  });
};
```

### 🆕 CSS Cascade Analysis (**CONFLICT RESOLUTION**)

#### When to Apply CSS Cascade Analysis
- **Scenario:** Styling issues where properties appear correct but behavior is wrong
- **Problem Types:** Specificity conflicts, cascade order issues, !important overrides
- **Success Example:** Z-index hierarchy resolution and styling conflict management

#### CSS Conflict Resolution Process (**SYSTEMATIC APPROACH**)
```css
/* Systematic CSS Hierarchy Management */
:root {
  --z-base: 1;
  --z-headers: 100;
  --z-resize-handles: 500;
  --z-dropdowns: 1000;
  --z-overflow-menu: 3000;
  --z-overflow-dropdown: 3001;
}

/* Avoid nuclear z-index values - use systematic hierarchy */
.dropdown-menu {
  z-index: var(--z-dropdowns);
}

.overflow-menu {
  z-index: var(--z-overflow-menu);
}
```

### 🆕 React Event Coordination (**TIMING ISSUE RESOLUTION**)

#### When to Apply React Event Coordination
- **Scenario:** Interactive components with timing-dependent behavior
- **Problem Types:** Click-outside handlers, event bubbling, state synchronization
- **Success Example:** Overflow menu timing fixes and click-outside handler coordination

#### Event Timing Resolution (**PROVEN PATTERNS**)
```typescript
// Timing-Safe Click-Outside Handler
const useClickOutside = (ref, handler, enabled = true) => {
  useEffect(() => {
    if (!enabled) return;
    
    // Delay adding listener to prevent same-click interference
    const timeoutId = setTimeout(() => {
      const handleClickOutside = (event) => {
        if (ref.current && !ref.current.contains(event.target)) {
          handler(event);
        }
      };
      
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }, 10);
    
    return () => clearTimeout(timeoutId);
  }, [ref, handler, enabled]);
};

// Event Bubbling Prevention
const handleInteractiveElement = (event, callback) => {
  event.stopPropagation(); // Prevent bubbling
  console.log('Event handled:', event.target);
  callback(event);
};
```

### 🆕 Component Integration Debug (**STATE COORDINATION ANALYSIS**)

#### When to Apply Component Integration Debug
- **Scenario:** Issues with component state coordination and prop flow
- **Problem Types:** State updates not propagating, callback timing, integration mismatches
- **Success Example:** ViewModeDropdown integration and unified state coordination

#### Integration Debug Pattern (**COMPREHENSIVE ANALYSIS**)
```typescript
// Component Integration Debug Pattern
const useComponentIntegrationDebug = (componentName, props) => {
  useEffect(() => {
    console.log(`${componentName} props updated:`, props);
  }, [props]);
  
  useEffect(() => {
    console.log(`${componentName} mounted`);
    return () => console.log(`${componentName} unmounting`);
  }, []);
  
  // Debug callback executions
  const debugCallbacks = Object.keys(props)
    .filter(key => typeof props[key] === 'function')
    .reduce((acc, key) => {
      acc[key] = (...args) => {
        console.log(`${componentName}.${key} called with:`, args);
        return props[key](...args);
      };
      return acc;
    }, {});
    
  return { ...props, ...debugCallbacks };
};
```

## ⚠️ Critical Refactoring Priorities (**UPDATED WITH RECENT EXPERIENCE**)

### High Priority - Large File Issues

#### 1. scryfallApi.ts (575 lines) - Service Layer (**APPLY EXTRACTION METHODOLOGY**)
**Status:** Working well with extracted hooks, apply component extraction patterns if needed
**Recommended Approach:** Use proven hook extraction methodology for service layer if problematic
**Pattern:** Apply extraction patterns: Identify responsibilities → Extract focused services → Maintain coordinator → Apply coordination patterns

#### 2. card.ts (520 lines) - Type System Foundation (**STABLE, APPLY SEPARATION WHEN NEEDED**)
**Status:** Working well, apply proven separation patterns when growth continues
**Recommended Approach:** Separate types from utilities using documented separation patterns
**Pattern:** Apply type/utility separation using proven component extraction methodology

#### 3. screenshotUtils.ts (850 lines) - Algorithm Complexity (**LOWEST PRIORITY**)
**Status:** Complex but focused, apply extraction patterns if maintenance becomes difficult
**Recommended Approach:** Extract algorithm modules using proven extraction methodology

### 🆕 Excellent Architecture Examples (**POST-REFACTORING**)

#### ✅ Perfect Component Extraction Examples
- **MTGOLayout.tsx** (450 lines) - **EXCELLENT COORDINATOR** - Clean hook integration with extracted area components
- **CollectionArea.tsx** (~200 lines) - **EXCELLENT FOCUSED COMPONENT** - Collection-specific logic with MTGO styling
- **DeckArea.tsx** (~200 lines) - **EXCELLENT UNIFIED CONTROLS** - Deck management with responsive overflow system
- **SideboardArea.tsx** (~200 lines) - **EXCELLENT STATE INHERITANCE** - Simplified header with unified state

#### ✅ Perfect Hook Architecture Examples  
- **useCards.ts** (250 lines) - **EXCELLENT COORDINATOR** - Successfully coordinates 5 extracted hooks
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

### 🆕 Architecture Success Patterns (**ENHANCED WITH ADVANCED EXAMPLES**)

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

### Patterns to Avoid (**ANTI-PATTERNS FROM EXPERIENCE**)

#### Size & Complexity Issues
- **Monolithic Components:** Single components with multiple major responsibilities (MTGOLayout before refactoring)
- **Mixed Concerns:** Types mixed with utilities, layout mixed with business logic
- **Complex Dependencies:** Too many integration points in single component

#### 🆕 UI/UX Anti-Patterns
- **Nuclear Z-Index:** Extremely high values (9999999+) creating more conflicts than solutions
- **Global State Leakage:** Component state affecting unrelated instances
- **Missing Context Awareness:** Components not adapting to rendering environment

#### 🆕 State Management Anti-Patterns
- **State Duplication:** Multiple similar states instead of unified management
- **Missing Migration:** Breaking user preferences during state architecture changes
- **Tight Component Coupling:** Components knowing too much about each other's internals

## 📚 🆕 Quick Reference Cards (**ENHANCED WITH ADVANCED PATTERNS**)

### "I want to modify search functionality"
**Primary Files:** `useSearch.ts` (**EXTRACTED HOOK**), `scryfallApi.ts`, `SearchAutocomplete.tsx`  
**Secondary Files:** `search.ts`, `useFilters.ts`, `useCards.ts` (coordinator)  
**Pattern:** API changes → useSearch updates → useCards coordination → component integration  
**🆕 Proven Pattern:** Hook extraction successful - useSearch is focused and maintainable

### "I want to add unified state functionality"  
**Primary Files:** `useLayout.ts` (**ENHANCED WITH UNIFIED PATTERNS**), `DeckArea.tsx`, `SideboardArea.tsx`  
**Secondary Files:** `MTGOLayout.tsx` (coordinator)  
**🆕 Pattern:** Single state source → Coordination functions → Component synchronization → Migration support  
**🆕 Success Example:** useLayout unified deck/sideboard state with automatic migration

### "I want to add responsive features"
**Primary Files:** `DeckArea.tsx` (**RESPONSIVE OVERFLOW SYSTEM**), `ViewModeDropdown.tsx` (**CONTEXT-AWARE**)  
**Secondary Files:** `MTGOLayout.css` (**MTGO STYLING FOUNDATION**)  
**🆕 Pattern:** Priority ordering → Space detection → Dynamic hiding → Overflow menu → Context preservation  
**🆕 Advanced Pattern:** ResizeObserver + context-aware components + professional overflow systems

### "I want to enhance UX with transforms"
**Primary Files:** `DragPreview.tsx` (**3X SCALING**), `DropZone.tsx` (**CENTERED FEEDBACK**)  
**Secondary Files:** `DraggableCard.tsx` (**COMPONENT ISOLATION**)  
**🆕 Pattern:** Transform scaling → Zone-relative positioning → Component isolation → Professional polish  
**🆕 Proven Pattern:** 3x scale transforms + zone centering + isolated effects

### "I want to apply MTGO styling"
**Primary Files:** `MTGOLayout.css` (**FOUNDATION**), header components  
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

### "I want to add pagination with scroll preservation"
**Primary Files:** Component with pagination, implement Smart Card Append pattern  
**🆕 Proven Pattern:** Smart Card Append for natural scroll preservation  
**🆕 Process:** Track loaded count → Split existing/new cards → Render with stable/fresh keys → Update state appropriately  
**🆕 Success Example:** Load More eliminates scroll reset, only new cards re-render

---

**Created:** June 7, 2025 from comprehensive architecture review  
**🆕 Enhanced:** June 8, 2025 with advanced patterns from MTGOLayout refactoring, Header UI/UX redesign, and debugging methodology development  
**Status:** Complete reference guide with validated advanced methodologies for MTG Deck Builder development  
**🆕 Advanced Patterns:** Component extraction, unified state management, responsive design, context-aware components, MTGO styling, enhanced UX, debugging methodologies  
**Usage:** Reference before any development work to understand integration points and apply advanced patterns  
**🆕 Maintenance:** Update as architecture evolves and new advanced patterns are proven through sophisticated development experience