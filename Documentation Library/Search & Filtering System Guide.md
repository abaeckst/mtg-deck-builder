# Search & Filtering System Guide

**Last Updated:** January 24, 2025 
**Status:** Production-ready with search mode toggles, performance optimizations (<1s search), timer system fixes 
**Complexity:** High - 6-hook coordination, search mode toggles, dual sort system, API integration, timer system migration

## 🎯 System Definition

### Purpose

**What this system does:** Comprehensive search and filtering with multi-field search (names, oracle text, type lines), search mode toggles (Name/Card Text), progressive loading, sophisticated filter coordination, dual sort system (client vs server-side), and performance optimization achieving <1 second search responses 
**Why it exists:** Provides fast, responsive card search with advanced filtering capabilities, progressive loading for large datasets, professional search mode controls, and optimized performance through re-render elimination, timer system fixes, and intelligent sorting decisions 
**System boundaries:** Handles all search input, filter management, search mode coordination, API coordination, pagination state, and results display; integrates with card display system, selection system, and layout system

### Core Files (Always Work Together)

#### **Central Coordination Hub:**

- `useCards.ts` (8,678 bytes) - **CRITICAL:** 6-hook coordinator hub with effect-based reactivity, pass-through functions, clean separation of concerns
  
  #### **Search Engine Core:**
- `useSearch.ts` (23,409 bytes) - **COMPLEX:** Core search logic, API coordination, stored pagination state, dual sort system, clean search principle, performance optimization, search mode integration
- `usePagination.ts` (1,846 bytes) - **SIMPLE:** Lightweight state management wrapper, callback coordination bridge
- `useSearchSuggestions.ts` (1,994 bytes) - Autocomplete functionality, search history management
  
  #### **Filter Management:**
- `useFilters.ts` (5,878 bytes) - **EXCELLENT EXAMPLE:** Clean filter state, section management, auto-expansion logic, standard format defaults, search mode toggle coordination
  
  #### **Selection & Support:**
- `useCardSelection.ts` (1,689 bytes) - Card selection state for search results
- `useSorting.ts` (5,069 bytes) - Sort criteria coordination with dual sort system integration
  
  ### Secondary Files
  
  **UI Components (Analyzed - Batch 2):**
- `SearchAutocomplete.tsx` (4,583 bytes) - **SIMPLE:** Search input with keyboard navigation, suggestion selection, 200ms delay coordination, search mode toggle integration
- `FilterPanel.css` (large) - Professional MTGO styling foundation, color button gradients, collapsible section animations, search mode chip styling
- `CollectionArea.tsx` (18,584 bytes) - **COMPLEX:** Search results display integration, sort menu state, view mode switching, Load More UI coordination
  **API Integration (Analyzed - Batch 3):**
- `scryfallApi.ts` (31,333 bytes) - **EXTREMELY COMPLEX:** API abstraction with wildcard optimization, stored pagination state management, enhanced query building with search mode support, comprehensive filter coordination, rate limiting, timer system migration (performance.now), extensive debugging
- `search.ts` (3,178 bytes) - **SIMPLE:** Type definitions for enhanced search features, search operators, common Magic terms for autocomplete
- `useSearchSuggestions.ts` (1,994 bytes) - **SIMPLE:** Autocomplete hook with search history management, API suggestion coordination
  
  ### Integration Points
  
  **Receives data from:**
- **Card Display System:** View mode preferences, card sizing requirements, display context for search results
- **Layout System:** Container dimensions, responsive behavior triggers, view mode coordination for search results display
- **Selection System:** Selected card tracking for search results, selection state coordination across search operations
  **Provides data to:**
- **Card Display System:** Filtered card collections, search results, pagination state for progressive rendering
- **Export System:** Search result collections, filter metadata, card groupings for export functionality
- **Layout System:** Search state for responsive behavior, loading states for UI adaptation
  **Coordinates with:**
- **API Layer:** scryfallApi.ts for all external data communication, search parameter optimization, pagination coordination
- **Performance System:** Re-render elimination, timing analysis, device detection integration for search responsiveness
- **State Management:** Multi-hook coordination patterns, effect-based reactivity, clean state separation
  
  ## 🔄 Critical Data Flows
  
  ### Primary Flow: Multi-Hook Coordination & Effect Reactivity
  
  ```
  useCards (Coordinator Hub) → 6 hooks integration → Clean separation of concerns
  ↓
  Filter Change → useCards effect → searchWithAllFilters('*') → useSearch → API coordination
  ↓
  Search Input → useCards pass-through → useSearch engine → scryfallApi with search mode → Results state update
  ↓
  Search Mode Toggle → Auto-search trigger → buildEnhancedSearchQuery with mode preferences → API coordination
  ↓
  State Synchronization → Callback coordination → UI component updates → Progressive rendering
  ```
  
  ### New Flow: Search Mode Toggle System
  
  ```
  Search Mode Toggle → FilterPanel chip interaction → useFilters state update → Auto-search trigger
  ↓
  [Name Mode Only] → Raw query optimization → Direct name matching → Fastest search performance
  ↓
  [Card Text Mode Only] → (o:term OR type:term) → Oracle text and type line focus → Content search
  ↓
  [Both Modes Active] → (name:term OR o:term OR type:term) → Comprehensive multi-field search
  ↓
  [Both Modes Disabled] → Search disabled state → No API calls → User feedback required
  ↓
  API Query Building → buildEnhancedSearchQuery with mode preferences → Optimized Scryfall queries
  ```
  
  ### Complex Flow: Dual Sort System (Client vs Server Decision)
  
  ```
  Sort Request → useSearch handleCollectionSortChange → Decision logic (≤75 cards threshold)
  ↓
  [≤75 cards] Client-side sort → UI components handle → Instant re-rendering → useSorting coordination
  ↓
  [>75 cards] Server-side sort → New search request → scryfallApi with sort params → Fresh results
  ↓
  Sort Preservation → Metadata storage → Load More coordination → Consistent sort across pagination
  ```
  
  ### Advanced Flow: Clean Search Principle & Filter Coordination
  
  ```
  Filter Update → useFilters state change → useCards effect detection → Fresh search trigger
  ↓
  Clean Search Build → searchWithAllFilters → Build filters from scratch → Never inherit previous state
  ↓
  Standard Format Default → Explicit override detection → Filter object construction → API parameter assembly
  ↓
  Wildcard Query Strategy → User query vs filter-only detection → '*' for filter-only → Clean API calls
  ```
  
  ### Complex Flow: Stored Pagination State & Load More Coordination
  
  ```
  Initial Search → searchWithPagination → API response → Store complete pagination state → Results display
  ↓
  Load More Request → useCards coordinatedLoadMore → useSearch loadMoreCards → Stored state retrieval
  ↓
  422 Error Prevention → storedPaginationState validation → Full page data availability → API continuation
  ↓
  State Synchronization → Results appending → Pagination updates → UI coordination
  ```
  
  ### Performance Flow: Re-render Elimination & Timing Analysis
  
  ```
  Search Input → Rate limiting (150ms) → Timing analysis → API call optimization
  ↓
  Re-render Prevention → Stable dependencies → Memoized callbacks → Performance optimization
  ↓
  Device Detection Integration → Throttled updates → Responsive behavior → Smooth performance
  ```
  
  ### Integration Flow: Cross-System Coordination
  
  ```
  Search Results → Card Display System → View mode integration → Selection system coordination
  ↓
  Filter Changes → Layout System → Responsive adaptation → Priority-based control hiding
  ↓
  Export Integration → Search metadata → Filter state → Card collections → Export functionality
  ```
  
  ### UI Coordination Flow: Search Input & Suggestions (SearchAutocomplete.tsx)
  
  ```
  User Input → onChange → 200ms delay → onSuggestionsRequested → useSearchSuggestions hook
  ↓
  Keyboard Navigation → Arrow keys → Active suggestion index → Visual highlighting
  ↓
  Enter Key → Suggestion selection OR direct search → onSuggestionSelect OR onSearch → Hook coordination
  ↓
  Click Outside → Blur handling → Clear suggestions → UI state reset
  ```
  
  ### UI Coordination Flow: Collection Display & Results (CollectionArea.tsx)
  
  ```
  Search Results → sortedCards calculation → View mode conditional rendering → Grid/List display
  ↓
  Sort Menu → Local state management → Click-outside detection → handleSortButtonClick → Hook coordination
  ↓
  Load More UI → Pagination state → Progress display → loadMoreResultsAction → Hook coordination
  ↓
  View Mode Switch → clearSelection → onViewModeChange → Layout system coordination
  ↓
  Card Sizing → Range input → onCardSizeChange → Real-time grid template updates
  ```
  
  ### UI Performance Flow: Professional MTGO Styling & Responsiveness
  
  ```
  Filter Panel → CSS collapsible sections → Animation coordination → Section state management
  ↓
  Color Buttons → Gradient styling → Hover/selection feedback → Visual state coordination
  ↓
  Sort Menu → Z-index strategy (1000) → Click-outside handling → Professional dropdown behavior
  ↓
  Grid Layout → Dynamic grid-template-columns → Card size scaling → Responsive card display
  ```
  
  ### API Integration Flow: Enhanced Query Building & Search Mode Support (scryfallApi.ts)
  
  ```
  Raw Query + Search Mode → buildEnhancedSearchQuery → Wildcard optimization detection → Mode-aware query building
  ↓
  ['*' query] → Early return (prevents expensive multi-field queries) → Simple wildcard → API efficiency
  ↓
  [Name Mode Only] → Raw query (fastest) → Direct name matching or name:"phrase" → Performance optimized
  ↓
  [Card Text Mode Only] → (o:term OR type:term) → Oracle text and type line search → Content-focused
  ↓
  [Both Modes Active] → (name:term OR o:term OR type:term) → Enhanced multi-field search → Comprehensive results
  ↓
  [Operator query] → Advanced parsing → Quoted phrases, exclusions, field searches → Professional query building
  ```
  
  ### API Coordination Flow: Filter Building & Parameter Assembly
  
  ```
  Filter Object → searchCardsWithFilters → Complex filter building → Scryfall parameter assembly
  ↓
  Format Filters → legal:standard/modern/etc → Color Filters → identity:/>=2/exact logic → Type/Subtype filters
  ↓
  Range Filters → cmc>=X, power<=Y → Rarity/Set filters → Multi-value OR logic → Complex query assembly
  ↓
  Final Query → searchCardsWithSort → Rate limiting (100ms) → API call → Response processing
  ```
  
  ### API Performance Flow: Stored Pagination State & 422 Error Prevention
  
  ```
  Initial Search → searchCardsWithPagination → Store complete page data (175 cards) → Display 75 cards
  ↓
  Load More Request → loadMoreResults → Check stored pagination state → Use remaining cards OR fetch new page
  ↓
  422 Error Prevention → stored currentPageCards validation → Remaining card calculation → No unnecessary API calls
  ↓
  Progressive Loading → 75-card batches → Smart Card Append → Smooth user experience
  ```
  
  ### API Rate Limiting & Performance Monitoring Flow with Timer Migration
  
  ```
  API Call → rateLimitedFetch → 100ms rate limiting → Timing analysis (performance.now)
  ↓
  Request Coordination → lastRequestTime tracking → Delay calculation → Performance optimization
  ↓
  Timer System Migration → console.time/timeEnd REMOVED → performance.now() precision → Millisecond accuracy
  ↓
  Response Processing → JSON parsing timing → Comprehensive logging → Debug output coordination
  ↓
  Performance Achievement → 8-13 second searches ELIMINATED → <1 second consistent response → Production ready
  ↓
  Error Handling → HTTP status validation → Error message enhancement → Failure recovery
  ```
  
  ## 🐛 Problem Diagnosis
  
  ### Multi-Hook Coordination Issues
  
  **"Search not triggering when filters change"**
- **Root Cause:** useCards effect reactivity failure or filter change detection issues
- **Check Files:** `useCards.ts` (effect dependency array, isInitialMount logic) → `useFilters.ts` (hasActiveFilters function) → filter change propagation
- **Debug Pattern:** Verify useCards effect triggers → check hasActiveFilters calculation → validate searchWithAllFilters call → confirm API integration
  **"Filter state not synchronized across components"**
- **Root Cause:** useCards pass-through pattern failure or hook coordination breakdown
- **Check Files:** `useCards.ts` (pass-through functions) → `useFilters.ts` (state management) → component integration
- **Debug Pattern:** Check useCards filter pass-through → verify useFilters state updates → validate component prop flow
  
  ### Search Engine Performance Issues
  
  **"Search taking 2-7+ seconds despite fast API"**
- **Root Cause:** Re-render loops in useSearch or hook dependency instability (RESOLVED via timer system migration)
- **Check Files:** `useSearch.ts` (rate limiting, memoization) → `scryfallApi.ts` (timer system) → `useSorting.ts` (stable dependencies) → hook coordination
- **Debug Pattern:** Apply timing analysis with performance.now() → identify re-render loops → fix dependency stability → verify <1 second response
  **"Timer system conflicts causing performance degradation"**
- **Root Cause:** console.time/timeEnd conflicts resolved via performance.now() migration
- **Check Files:** `scryfallApi.ts` (rateLimitedFetch, timing analysis functions) → API performance monitoring
- **Debug Pattern:** Verify performance.now() usage → check timing consistency → validate millisecond precision
  **"Load More causing 422 errors"**
- **Root Cause:** Stored pagination state missing or incomplete, API continuation failure
- **Check Files:** `useSearch.ts` (storedPaginationState management) → `scryfallApi.ts` (loadMoreResults coordination) → pagination flow
- **Debug Pattern:** Verify storedPaginationState exists → check currentPageCards data → validate API continuation parameters
  
  ### Dual Sort System Issues
  
  **"Sort not working or showing wrong results"**
- **Root Cause:** Client vs server sort decision logic failure or sort parameter mapping issues
- **Check Files:** `useSearch.ts` (handleCollectionSortChange, dual sort logic) → `useSorting.ts` (sort coordination) → API parameter mapping
- **Debug Pattern:** Check sort decision logic (≤75 threshold) → verify sort parameter mapping → validate API sort coordination
  **"Sort preferences not preserved during Load More"**
- **Root Cause:** Sort metadata not stored in lastSearchMetadata or Load More coordination failure
- **Check Files:** `useSearch.ts` (actualSortOrder/actualSortDirection storage) → Load More sort preservation → API consistency
- **Debug Pattern:** Verify sort metadata storage → check Load More sort coordination → validate API sort consistency
  
  ### Filter Reactivity Issues
  
  **"Filters not triggering fresh search"**
- **Root Cause:** Clean search principle failure or filter change effect not executing
- **Check Files:** `useCards.ts` (filter change effect) → `useSearch.ts` (searchWithAllFilters logic) → clean search building
- **Debug Pattern:** Check useCards filter effect triggers → verify searchWithAllFilters execution → validate clean filter building
  **"Standard format not working as default"**
- **Root Cause:** Format filter logic or default handling in clean search building
- **Check Files:** `useFilters.ts` (DEFAULT_FILTER_STATE, hasActiveFilters) → `useSearch.ts` (searchWithAllFilters filter building)
- **Debug Pattern:** Verify standard format default → check hasActiveFilters format logic → validate clean search filter building
  
  ### Search Mode Toggle Issues
  
  **"Search mode toggles not working or not triggering search"**
- **Root Cause:** Search mode state coordination failure or auto-search trigger not executing
- **Check Files:** `FilterPanel.tsx` (search mode chip interaction) → `useFilters.ts` (search mode state) → auto-search effect
- **Debug Pattern:** Check search mode state updates → verify auto-search effect triggers → validate API query building with modes
  **"Search disabled when both modes are off"**
- **Root Cause:** Expected behavior - both modes disabled should prevent searches
- **Check Files:** `SearchAutocomplete.tsx` (disabled state) → `useFilters.ts` (search mode validation) → user feedback
- **Debug Pattern:** Verify both modes are disabled → check disabled state UI feedback → validate no API calls when disabled
  **"Search mode not affecting query building"**
- **Root Cause:** buildEnhancedSearchQuery not receiving or processing search mode preferences
- **Check Files:** `scryfallApi.ts` (buildEnhancedSearchQuery function) → mode parameter handling → query building logic
- **Debug Pattern:** Check mode parameter passing → verify query building logic for each mode → validate API query structure
  
  ### API Integration Issues
  
  **"Search suggestions not working"**
- **Root Cause:** useSearchSuggestions coordination or API integration failure
- **Check Files:** `useSearchSuggestions.ts` (suggestion logic) → `scryfallApi.ts` (getSearchSuggestions function) → API autocomplete endpoint coordination
- **Debug Pattern:** Check suggestion hook integration → verify getSearchSuggestions API call → validate autocomplete endpoint response
  **"Pagination state getting corrupted"**
- **Root Cause:** Complex pagination state management or callback coordination failure
- **Check Files:** `usePagination.ts` (state management) → `useSearch.ts` (pagination callbacks) → `scryfallApi.ts` (loadMoreResults stored state logic)
- **Debug Pattern:** Check pagination state updates → verify callback coordination → validate stored pagination state logic
  **"Search queries not optimized or taking too long"**
- **Root Cause:** buildEnhancedSearchQuery logic failure, wildcard optimization not working, or search mode not optimizing queries
- **Check Files:** `scryfallApi.ts` (buildEnhancedSearchQuery function, wildcard optimization, search mode logic) → query building logic → API parameter assembly
- **Debug Pattern:** Check wildcard optimization logic → verify search mode query optimization → validate enhanced query building → test operator parsing → confirm mode-specific optimizations
  **"Filter building not working correctly"**
- **Root Cause:** searchCardsWithFilters complex filter logic or Scryfall parameter assembly failure
- **Check Files:** `scryfallApi.ts` (searchCardsWithFilters function, filter building logic) → filter parameter mapping → API query assembly
- **Debug Pattern:** Check filter building logic → verify parameter mapping → validate complex filter coordination (colors, ranges, types)
  **"Load More causing 422 errors despite fixes"**
- **Root Cause:** Stored pagination state management failure or currentPageCards not preserved correctly
- **Check Files:** `scryfallApi.ts` (loadMoreResults function, stored state validation) → pagination state coordination → API continuation logic
- **Debug Pattern:** Check currentPageCards preservation → verify cardsConsumedFromCurrentPage calculation → validate Load More decision logic
  **"Rate limiting not working or API calls too frequent"**
- **Root Cause:** rateLimitedFetch logic failure or timing coordination issues
- **Check Files:** `scryfallApi.ts` (rateLimitedFetch function, rate limiting logic) → timing analysis → API call coordination
- **Debug Pattern:** Check rate limiting timing → verify delay calculation → validate API call frequency
  
  ### UI Coordination Issues
  
  **"Search autocomplete not responding to input"**
- **Root Cause:** SearchAutocomplete input handling or 200ms delay coordination failure
- **Check Files:** `SearchAutocomplete.tsx` (handleInputChange, suggestion delay) → hook coordination → suggestion state management
- **Debug Pattern:** Check input change handling → verify 200ms delay logic → validate suggestion request coordination
  **"Sort menu not opening or staying open"**
- **Root Cause:** CollectionArea sort menu state or click-outside detection failure
- **Check Files:** `CollectionArea.tsx` (showSortMenu state, click-outside effect) → sort menu rendering → state coordination
- **Debug Pattern:** Check sort menu state management → verify click-outside event handling → validate menu positioning
  **"Load More button not working in grid/list view"**
- **Root Cause:** CollectionArea Load More integration or pagination UI state synchronization failure
- **Check Files:** `CollectionArea.tsx` (Load More integration in both views) → pagination state coordination → loadMoreResultsAction coordination
- **Debug Pattern:** Check pagination.hasMore state → verify loadMoreResultsAction integration → validate UI state synchronization
  **"View mode switching not working or clearing selection"**
- **Root Cause:** CollectionArea view mode coordination or selection clearing logic failure
- **Check Files:** `CollectionArea.tsx` (onViewModeChange integration, clearSelection calls) → view mode state coordination → selection system integration
- **Debug Pattern:** Check view mode change handling → verify selection clearing logic → validate state coordination with layout system
  **"Card sizing not updating grid layout"**
- **Root Cause:** CollectionArea dynamic grid template calculation or card scaling coordination failure
- **Check Files:** `CollectionArea.tsx` (grid-template-columns calculation, cardSize scaling) → CSS coordination → responsive layout
- **Debug Pattern:** Check cardSize prop flow → verify grid template calculation → validate CSS variable coordination
  **"Filter panel styling or sections not working"**
- **Root Cause:** FilterPanel.css styling conflicts or section management coordination failure
- **Check Files:** `FilterPanel.css` (collapsible section styles, color button gradients) → section state coordination → visual feedback
- **Debug Pattern:** Check CSS class application → verify section animation coordination → validate visual state feedback
  
  ### Debugging Starting Points
  
  **Multi-hook coordination issues:** Start with `useCards.ts` pass-through functions → hook integration verification → effect reactivity validation 
  **Search performance problems:** Start with `useSearch.ts` timing analysis → `scryfallApi.ts` wildcard optimization → buildEnhancedSearchQuery logic verification 
  **Load More issues:** Start with `useSearch.ts` storedPaginationState → `scryfallApi.ts` loadMoreResults → stored state validation → API continuation logic 
  **Filter reactivity problems:** Start with `useCards.ts` filter effect → `useFilters.ts` state management → `scryfallApi.ts` searchCardsWithFilters → filter building verification 
  **Sort system issues:** Start with `useSearch.ts` dual sort logic → `scryfallApi.ts` API parameter coordination → sort preservation validation 
  **API integration problems:** Start with `scryfallApi.ts` API functions → query building → filter coordination → rate limiting verification 
  **Search autocomplete issues:** Start with `SearchAutocomplete.tsx` input handling → `useSearchSuggestions.ts` coordination → `scryfallApi.ts` getSearchSuggestions 
  **UI coordination problems:** Start with `CollectionArea.tsx` state management → view mode/sizing coordination → visual feedback validation 
  **Filter UI issues:** Start with FilterPanel.css styling → section management → visual state coordination 
  **Query optimization issues:** Start with `scryfallApi.ts` buildEnhancedSearchQuery → wildcard optimization → enhanced parsing logic 
  **Pagination API issues:** Start with `scryfallApi.ts` loadMoreResults → stored pagination state validation → 422 error prevention verification
  
  ## 🔧 Architecture Details
  
  ### State Management Pattern
  
  **How state is organized:** Multi-hook coordination through useCards hub with clean separation of concerns - useFilters (filter state), useSearch (search engine), usePagination (pagination state), useCardSelection (selection), useSearchSuggestions (autocomplete), useSorting (sort coordination) 
  **State flow:** useCards coordinates all hooks → effect-based reactivity → pass-through functions → callback coordination → API integration → state synchronization 
  **Key state variables:** activeFilters (useFilters), search results + metadata (useSearch), pagination state (usePagination), selectedCards (useCardSelection), searchSuggestions (useSearchSuggestions), sort criteria (useSorting)
  
  ### Critical Functions & Hooks
  
  #### **Central Coordination (useCards.ts):**
  
  **6-hook integration:** useFilters + useSearch + usePagination + useCardSelection + useSearchSuggestions + useSorting coordination 
  **Effect-based reactivity:** Filter change detection → searchWithAllFilters('*') trigger → fresh search execution 
  **Pass-through pattern:** Filter functions, selection functions, search functions → clean API to components 
  **coordinatedLoadMore:** Load More coordination between pagination state and search engine with error handling
  
  #### **Search Engine Core (useSearch.ts):**
  
  **searchWithPagination:** Core search function with rate limiting, API coordination, stored pagination state management 
  **handleCollectionSortChange:** Dual sort system - client-side (≤75 cards) vs server-side (>75 cards) decision logic 
  **loadMoreCards:** Complex Load More with stored pagination state, 422 error prevention, state coordination 
  **Clean Search Principle:** searchWithAllFilters builds filter objects from scratch, never inherits previous state 
  **Performance optimization:** Rate limiting (150ms), re-render prevention, timing analysis integration
  
  #### **Filter Management (useFilters.ts):**
  
  **hasActiveFilters:** Excludes standard format as default, detects all active filter categories 
  **updateFilter:** Clean filter state updates with automatic section expansion integration 
  **autoExpandSection:** Auto-expands sections with active filters for better UX 
  **Section state management:** Collapsible section coordination with expanded/collapsed state persistence
  
  #### **UI Coordination (SearchAutocomplete.tsx):**
  
  **Input handling:** handleInputChange with 200ms delay for suggestion requests, keyboard navigation (arrow keys, enter, escape) 
  **Suggestion coordination:** onSuggestionSelect vs onSearch coordination, click-outside detection, blur handling with 200ms delay 
  **State management:** activeSuggestionIndex for keyboard navigation, visual highlighting coordination 
  **Event coordination:** Prevent default on navigation keys, suggestion click vs input blur timing
  
  #### **Results Display Coordination (CollectionArea.tsx):**
  
  **Sort menu management:** showSortMenu local state, click-outside detection via useEffect, handleSortButtonClick coordination with dual sort system 
  **View mode coordination:** Grid vs List conditional rendering, clearSelection integration with view mode switching 
  **Load More UI:** Integrated Load More for both grid and list views, pagination state display, progress visualization 
  **Dynamic layout:** Grid template columns calculation based on cardSize, responsive card scaling, professional MTGO header styling 
  **Card sizing:** Range input coordination with onCardSizeChange, real-time grid template updates
  
  #### **Professional Styling (FilterPanel.css):**
  
  **MTGO authenticity:** Color button gradients, professional hover effects, collapsible section animations 
  **Section management:** Auto-expand animations, active filter indication, visual state feedback 
  **Responsive design:** Media queries for mobile adaptation, scrollbar styling, overflow management
  
  #### **API Integration Core (scryfallApi.ts):**
  
  **buildEnhancedSearchQuery:** Complex query building with wildcard optimization, multi-word field search, operator parsing (quotes, exclusions, field searches) 
  **searchCardsWithFilters:** Extensive filter building logic - format, colors (with gold mode), types, subtypes, rarity, sets, CMC ranges, power/toughness ranges 
  **searchCardsWithPagination:** Initial search with 75-card limit, stored pagination state creation, progressive loading foundation 
  **loadMoreResults:** Sophisticated Load More with stored pagination state validation, 422 error prevention, remaining card calculation vs new page fetching 
  **rateLimitedFetch:** 100ms rate limiting with timing analysis, comprehensive logging, performance monitoring integration 
  **enhancedSearchCards:** Full-text search capabilities with enhanced query building and complete filter coordination
  
  #### **Search Suggestions (useSearchSuggestions.ts):**
  
  **getSearchSuggestions:** API coordination for autocomplete with card names, operators, Magic terms integration 
  **addToSearchHistory:** Search history management with 10-item limit, duplicate filtering 
  **clearSearchSuggestions:** UI state coordination for suggestion hiding
  
  ### Component Hierarchy
  
  ```
  useCards (Central Coordination Hub)
  ├── Multi-Hook Integration:
  │ ├── useFilters (filter state + section management)
  │ ├── useSearch (search engine + API + stored pagination)
  │ ├── usePagination (pagination state bridge)
  │ ├── useCardSelection (selection state)
  │ ├── useSearchSuggestions (autocomplete + history)
  │ └── useSorting (sort criteria coordination)
  ├── Effect-Based Reactivity:
  │ ├── Filter Change Detection → searchWithAllFilters('*') trigger
  │ ├── Initial Mount Skip → loadPopularCards on mount only
  │ └── Clean Search Coordination → fresh search on filter changes
  ├── Pass-Through Functions:
  │ ├── Filter functions → useFilters coordination
  │ ├── Search functions → useSearch coordination
  │ ├── Selection functions → useCardSelection coordination
  │ └── Suggestion functions → useSearchSuggestions coordination
  ├── UI Coordination Layer:
  │ ├── SearchAutocomplete.tsx (search input + suggestions)
  │ │ ├── Input handling (200ms delay → suggestion requests)
  │ │ ├── Keyboard navigation (arrow keys, enter, escape)
  │ │ ├── Suggestion selection vs direct search coordination
  │ │ └── Click-outside detection → suggestion clearing
  │ ├── CollectionArea.tsx (results display + controls)
  │ │ ├── Sort menu state (showSortMenu + click-outside detection)
  │ │ ├── View mode switching (grid/list + clearSelection coordination)
  │ │ ├── Load More UI (integrated for both grid and list views)
  │ │ ├── Card sizing (range input → dynamic grid template calculation)
  │ │ └── Professional MTGO header styling
  │ └── FilterPanel.css (professional MTGO styling)
  │ ├── Color button gradients + hover effects
  │ ├── Collapsible section animations
  │ ├── Auto-expand visual feedback
  │ └── Responsive design patterns
  ├── API Integration Layer:
  │ ├── scryfallApi.ts (complex API coordination - 31,333 bytes)
  │ │ ├── Enhanced Query Building (buildEnhancedSearchQuery)
  │ │ │ ├── Wildcard optimization (early return for '*')
  │ │ │ ├── Multi-word field search coordination
  │ │ │ ├── Operator parsing (quotes, exclusions, field searches)
  │ │ │ └── Advanced query enhancement logic
  │ │ ├── Filter Coordination (searchCardsWithFilters)
  │ │ │ ├── Format filters (legal:standard/modern/etc)
  │ │ │ ├── Color filters (identity logic + gold mode)
  │ │ │ ├── Type/subtype filters (OR logic coordination)
  │ │ │ ├── Range filters (CMC, power, toughness)
  │ │ │ └── Complex filter building with parameter assembly
  │ │ ├── Pagination Management (searchCardsWithPagination + loadMoreResults)
  │ │ │ ├── Initial search (75-card display limit)
  │ │ │ ├── Stored pagination state (complete page data)
  │ │ │ ├── Load More decision logic (remaining cards vs new page)
  │ │ │ └── 422 error prevention through stored state validation
  │ │ ├── Performance Optimization
  │ │ │ ├── Rate limiting (100ms delays + timing analysis)
  │ │ │ ├── Comprehensive logging and debugging
  │ │ │ ├── Performance monitoring (console.time/timeEnd)
  │ │ │ └── API efficiency patterns
  │ │ └── Multiple Search Variants (searchCards, searchCardsWithSort, enhancedSearchCards)
  │ ├── search.ts (type definitions for advanced search features)
  │ └── useSearchSuggestions.ts (autocomplete coordination)
  │ ├── API suggestion integration (getSearchSuggestions)
  │ ├── Search history management (10-item limit)
  │ └── Magic terms and operators coordination
  └── Coordinated Load More:
  ├── Pagination state validation
  ├── Search engine Load More call
  ├── UI progress display coordination
  ├── Error handling coordination
  └── State synchronization management
  ```
  
  ### Performance Considerations
  
  **Critical paths:** 6-hook coordination (useCards), search engine performance (useSearch rate limiting, re-render prevention), dual sort system decision logic (≤75 threshold), stored pagination state management (Load More 422 prevention), filter change reactivity (effect coordination), API integration optimization (timing analysis), UI coordination (SearchAutocomplete 200ms delay, CollectionArea dynamic grid calculations, Load More UI state synchronization), API coordination (buildEnhancedSearchQuery complexity, filter building logic, pagination state management, rate limiting coordination) 
  **Optimization patterns:** Rate limiting (150ms useSearch + 100ms API), stable hook dependencies, memoized callbacks, clean search principle (no state inheritance), device detection integration, re-render elimination, timing analysis for performance debugging, UI delay coordination (200ms suggestion requests), dynamic grid template optimization, professional animation performance, wildcard optimization (early return for '*'), stored pagination state (prevents 422 errors), enhanced query building efficiency 
  **Known bottlenecks:** useSearch complexity (23,409 bytes), scryfallApi.ts complexity (31,333 bytes with multiple API functions), multi-hook effect coordination, stored pagination state management, dual sort system decision logic, API parameter building complexity, filter reactivity coordination across 6 hooks, CollectionArea complexity (18,584 bytes), dynamic grid template calculations, UI state synchronization complexity, buildEnhancedSearchQuery parsing overhead, complex filter building in searchCardsWithFilters, loadMoreResults decision logic complexity
  
  ## ⚠️ Current System Status
  
  ### Working Functionality
- ✅ **6-Hook Coordination:** useCards successfully coordinates all hooks with clean separation of concerns and pass-through patterns
- ✅ **Search Performance:** Re-render elimination and timing analysis providing <1 second search response (previously optimized)
- ✅ **Dual Sort System:** Client-side sort (≤75 cards) vs server-side sort (>75 cards) decision logic working correctly
- ✅ **Load More Functionality:** Stored pagination state management preventing 422 errors with proper API continuation
- ✅ **Filter Reactivity:** Effect-based filter change detection triggering fresh searches with clean search principle
- ✅ **Clean Search Building:** searchWithAllFilters builds filter objects from scratch without state inheritance
- ✅ **Standard Format Default:** Standard format as default with explicit override detection and hasActiveFilters logic
- ✅ **Rate Limiting:** 150ms rate limiting preventing API overload with timing analysis integration
- ✅ **Progressive Loading:** 75-card initial + Load More with Smart Card Append and scroll preservation
- ✅ **Search Suggestions:** Autocomplete functionality with search history management and useCards coordination
- ✅ **Section Management:** Filter panel sections with auto-expansion and state persistence
- ✅ **UI Coordination:** SearchAutocomplete input handling with 200ms delay, keyboard navigation, suggestion selection
- ✅ **Results Display:** CollectionArea sort menu, view mode switching, Load More UI integration for both grid and list views
- ✅ **Dynamic Layout:** Real-time grid template calculation based on card sizing, responsive professional MTGO styling
- ✅ **Professional Styling:** FilterPanel.css MTGO-authentic color gradients, collapsible animations, responsive design
- ✅ **API Integration:** Complete scryfallApi.ts with enhanced query building, complex filter coordination, stored pagination state management
- ✅ **Wildcard Optimization:** buildEnhancedSearchQuery early return for '*' queries preventing expensive multi-field searches
- ✅ **Enhanced Query Building:** Multi-word field searches, operator parsing, advanced query enhancement for professional search capabilities
- ✅ **Complex Filter Building:** searchCardsWithFilters handling all filter types with proper Scryfall parameter assembly
- ✅ **Pagination API Management:** loadMoreResults with sophisticated stored state validation preventing 422 errors
- ✅ **API Rate Limiting:** 100ms API delays with comprehensive timing analysis and performance monitoring
  
  ### Known Issues
- ⚠️ **useSearch Complexity:** 23,409 bytes with multiple responsibilities could benefit from extraction (search logic, pagination management, sort coordination)
- ⚠️ **scryfallApi.ts Complexity:** 31,333 bytes with extensive API functions could benefit from extraction (query building, filter logic, pagination management)
- ⚠️ **CollectionArea Complexity:** 18,584 bytes with multiple UI responsibilities (sort menu, view mode, Load More, card sizing, dynamic layout)
- ⚠️ **Stored Pagination State Complexity:** Complex state management for Load More functionality requires careful coordination
- ⚠️ **Multi-Hook Effect Coordination:** 6-hook coordination through useCards effects requires careful dependency management
- ⚠️ **API Parameter Building:** Complex filter building logic in searchCardsWithFilters could benefit from extraction
- ⚠️ **Dual Sort System Complexity:** Client vs server sort decision logic adds architectural complexity
- ⚠️ **Search Metadata Management:** lastSearchMetadata storage and coordination across sort operations requires careful state management
- ⚠️ **UI State Synchronization:** Complex coordination between hook state and UI components (SearchAutocomplete, CollectionArea)
- ⚠️ **Dynamic Grid Performance:** Real-time grid template calculation based on card sizing may impact performance with large result sets
- ⚠️ **Enhanced Query Building Complexity:** buildEnhancedSearchQuery parsing logic could benefit from simplification or extraction
- ⚠️ **API Function Proliferation:** Multiple search variants (searchCards, searchCardsWithSort, searchCardsWithFilters, searchCardsWithPagination, enhancedSearchCards) create maintenance complexity
  
  ### Technical Debt
  
  **Priority Items:**
- **P2:** useSearch.ts size and complexity (23,409 bytes) - consider extraction of pagination logic, sort coordination, or API integration
- **P2:** scryfallApi.ts size and complexity (31,333 bytes) - consider extraction of query building logic, filter coordination, or pagination management
- **P2:** CollectionArea.tsx size and complexity (18,584 bytes) - consider extraction of sort menu, view mode management, or Load More coordination
- **P2:** Stored pagination state management complexity - could benefit from dedicated pagination service
- **P3:** Multi-hook coordination complexity - 6 hooks coordinated through useCards with effect dependencies
- **P3:** API parameter building complexity - searchCardsWithFilters filter building logic could be extracted
- **P3:** Enhanced query building complexity - buildEnhancedSearchQuery parsing logic could be simplified or extracted
- **P3:** Dual sort system complexity - client vs server decision logic adds maintenance overhead
- **P3:** UI state synchronization complexity - coordination between hooks and UI components could be simplified
- **P3:** API function proliferation - multiple search variants create maintenance complexity
- **P4:** Search metadata coordination - lastSearchMetadata storage across operations could be simplified
- **P4:** Dynamic grid performance optimization - real-time grid template calculations with large datasets
  
  ### Recent Changes
  
  **Performance optimization:** Search re-render elimination providing <1 second response, Load More 422 error prevention with stored pagination state 
  **Architecture enhancement:** Clean search principle implementation, dual sort system integration, filter reactivity coordination 
  **API integration:** Rate limiting optimization, wildcard optimization, timing analysis integration
  
  ## 🚀 Development Patterns
  
  ### Common Change Patterns
  
  #### **Adding Search Features:**
1. **Start with:** `useSearch.ts` → search logic implementation → API integration patterns
2. **Consider coordination:** `useCards.ts` → pass-through function addition → hook coordination verification
3. **Test by:** Search functionality verification, performance validation, multi-hook coordination testing
   
   #### **Adding Search Mode Features:**
4. **Start with:** `useFilters.ts` → search mode state management → auto-search effect coordination
5. **Then modify:** `scryfallApi.ts` → buildEnhancedSearchQuery → mode-aware query building → optimization patterns
6. **UI integration:** `FilterPanel.tsx` → search mode chips → visual feedback → `SearchAutocomplete.tsx` disabled state coordination
7. **Test by:** Search mode toggle functionality, query optimization validation, UI state coordination, auto-search trigger verification
   
   #### **Adding Filter Features:**
8. **Start with:** `useFilters.ts` → filter state management → section management integration
9. **Then modify:** `useCards.ts` → pass-through coordination → `useSearch.ts` → clean search building
10. **Test by:** Filter reactivity verification, clean search validation, section management testing
   
   #### **Adding Performance Features:**
11. **Start with:** `useSearch.ts` → timing analysis → re-render detection → optimization implementation
12. **Consider integration:** Hook dependency stability, memoization patterns, effect coordination, timer system migration (performance.now)
13. **Test by:** Performance measurement, re-render monitoring, timing analysis validation, <1 second response verification
   
   #### **Adding API Integration Features:**
14. **Start with:** `useSearch.ts` → API parameter building → `scryfallApi.ts` integration → response handling
15. **Consider coordination:** Search mode parameter passing, pagination state management, error handling, state synchronization
16. **Test by:** API integration testing, search mode query validation, error handling validation, state coordination verification
    
    #### **Adding UI Coordination Features:**
17. **Start with:** `SearchAutocomplete.tsx` → input handling and suggestion coordination → 200ms delay timing
18. **Consider integration:** Hook coordination through useCards pass-through functions → search mode disabled state → state synchronization validation
19. **Test by:** Search input responsiveness, suggestion accuracy, keyboard navigation functionality, search mode UI feedback
    
    #### **Adding Results Display Features:**
20. **Start with:** `CollectionArea.tsx` → sort menu, view mode, or Load More integration → UI state management
21. **Consider coordination:** Hook state synchronization → dynamic layout calculations → performance impact assessment
22. **Test by:** Sort menu functionality, view mode switching accuracy, Load More UI integration, card sizing responsiveness
    
    #### **Adding Professional Styling:**
23. **Start with:** `FilterPanel.css` → MTGO-authentic styling patterns → search mode chip styling → animation coordination
24. **Consider integration:** Section management coordination → search mode visual feedback → visual state feedback → responsive design patterns
25. **Test by:** Professional appearance validation, search mode chip styling, animation smoothness, responsive behavior across screen sizes
    
    #### **Adding API Integration Features:**
22. **Start with:** `scryfallApi.ts` → query building, filter coordination, or pagination management → API parameter assembly
23. **Consider coordination:** Hook integration through useSearch → response handling → state synchronization
24. **Test by:** API call accuracy, filter parameter building, pagination state management, rate limiting effectiveness
    
    #### **Adding Query Optimization Features:**
25. **Start with:** `scryfallApi.ts` → buildEnhancedSearchQuery logic → wildcard optimization → query parsing enhancement
26. **Consider integration:** useSearch coordination → search performance impact → API efficiency validation
27. **Test by:** Query building accuracy, wildcard optimization effectiveness, multi-word search capability, operator parsing functionality
    
    #### **Adding Filter Coordination Features:**
28. **Start with:** `scryfallApi.ts` → searchCardsWithFilters logic → complex filter building → parameter assembly
29. **Consider integration:** useFilters state coordination → API parameter mapping → response validation
30. **Test by:** Filter building accuracy, Scryfall parameter assembly, complex filter coordination (colors, ranges, types)
    
    ### File Modification Order
    
    #### **For search functionality changes:** `useSearch.ts` (core logic) → `scryfallApi.ts` (API coordination) → `useCards.ts` (hook coordination) → `SearchAutocomplete.tsx` (UI integration) → testing
    
    #### **For filter functionality changes:** `useFilters.ts` (state management) → `scryfallApi.ts` (filter building) → `useCards.ts` (pass-through) → `useSearch.ts` (clean search building) → FilterPanel styling → coordination testing
    
    #### **For performance optimization:** `useSearch.ts` (timing analysis) → `scryfallApi.ts` (API optimization) → hook dependency optimization → UI coordination optimization → performance validation
    
    #### **For pagination changes:** `useSearch.ts` (stored state) → `scryfallApi.ts` (pagination logic) → `usePagination.ts` (coordination) → `CollectionArea.tsx` (Load More UI) → testing
    
    #### **For sort system changes:** `useSearch.ts` (dual sort logic) → `scryfallApi.ts` (API sort coordination) → `useSorting.ts` (coordination) → `CollectionArea.tsx` (sort menu UI) → testing
    
    #### **For results display changes:** `CollectionArea.tsx` (UI logic) → hook coordination → dynamic layout calculations → visual integration → performance testing
    
    #### **For search input changes:** `SearchAutocomplete.tsx` (input handling) → `useSearchSuggestions.ts` (coordination) → `scryfallApi.ts` (suggestion API) → delay timing optimization → testing
    
    #### **For styling changes:** `FilterPanel.css` (professional styling) → visual state coordination → animation performance → responsive design validation
    
    #### **For API integration changes:** `scryfallApi.ts` (query building, filter coordination, pagination management) → `useSearch.ts` (hook integration) → response handling → UI state synchronization → testing
    
    #### **For query optimization changes:** `scryfallApi.ts` (buildEnhancedSearchQuery) → wildcard optimization → parsing logic → `useSearch.ts` integration → performance validation
    
    #### **For filter building changes:** `scryfallApi.ts` (searchCardsWithFilters) → filter parameter assembly → `useFilters.ts` integration → `useSearch.ts` coordination → testing
    
    ### Testing Strategy
    
    **Critical to test:** 6-hook coordination (useCards), search performance (<1 second response), Load More functionality (422 error prevention), filter reactivity (clean search triggering), dual sort system (client vs server decision), API integration (parameter building, response handling), UI coordination (SearchAutocomplete input/suggestions, CollectionArea sort menu/view mode/Load More), dynamic layout performance (grid template calculations), API coordination (query building, filter building, pagination management, rate limiting), wildcard optimization effectiveness, enhanced query building accuracy 
    **Integration tests:** Multi-hook coordination through useCards, effect-based reactivity validation, stored pagination state coordination, clean search principle verification, sort metadata preservation across operations, UI state synchronization between hooks and components, search input delay coordination, Load More UI integration for both grid and list views, API parameter building accuracy, filter coordination through scryfallApi.ts, enhanced query building validation, stored pagination state API coordination 
    **Performance validation:** Search timing analysis, re-render monitoring, API rate limiting effectiveness, Load More performance, filter change responsiveness, UI responsiveness (200ms suggestion delay, dynamic grid calculations), animation smoothness, professional styling performance, API optimization (100ms rate limiting, wildcard optimization, query building efficiency), pagination API performance (stored state validation, 422 error prevention)

---

**System Guide Notes:**

- useCards.ts is the central coordination hub managing 6 hooks with clean separation of concerns
- useSearch.ts is the complex search engine (23,409 bytes) handling API coordination, stored pagination state, dual sort system, and search mode integration
- useFilters.ts provides excellent example of clean filter state management with section coordination and search mode toggle state
- usePagination.ts serves as lightweight bridge between complex pagination logic and UI components
- SearchAutocomplete.tsx provides clean search input with 200ms delay coordination, keyboard navigation, and search mode disabled state handling
- CollectionArea.tsx is complex results display component (18,584 bytes) with sort menu, view mode switching, Load More UI integration
- FilterPanel.css provides professional MTGO styling with color gradients, collapsible animations, search mode chip styling, and responsive design
- Search mode toggle system provides Name/Card Text mode controls with chip-style UI and auto-search coordination
- Timer system migration from console.time/timeEnd to performance.now() resolved 8-13 second search delays achieving <1 second responses
- Dual sort system uses ≤75 card threshold to decide between client-side (instant) vs server-side (new search) sorting
- Clean search principle: searchWithAllFilters builds filter objects from scratch, never inherits previous state
- Stored pagination state management prevents 422 errors during Load More operations
- Effect-based reactivity in useCards coordinates filter changes with fresh search triggers
- Rate limiting (150ms) and performance.now() timing analysis provide performance optimization
- Multi-hook coordination requires careful dependency management and effect coordination
- UI coordination patterns include 200ms suggestion delays, search mode coordination, dynamic grid template calculations, and professional MTGO styling
- Load More UI integration works seamlessly in both grid and list view modes with progress visualization
- Real-time card sizing affects dynamic grid template calculations requiring performance consideration
- Search mode query optimization: Name-only (fastest), Card Text-only (content-focused), Both modes (comprehensive)
- buildEnhancedSearchQuery provides mode-aware query building with wildcard optimization and performance improvements
