# Data Management System Guide

**Last Updated:** January 14, 2025 
**Status:** Working with sophisticated 6-hook coordination and comprehensive API integration 
**Complexity:** Extremely High - Central coordination hub, massive API layer, dual identity system, progressive loading, complex filter building

## 🎯 System Definition

### Purpose

**What this system does:** Complete data management ecosystem with central coordination hub (useCards), sophisticated API integration (scryfallApi.ts), dual identity architecture (Cards vs Instances), progressive loading with stored pagination state, and comprehensive search/filter coordination across all systems 
**Why it exists:** Provides efficient, coordinated data flow from Scryfall API to all UI components with performance optimization, sophisticated search capabilities, proper state management, and seamless cross-system integration 
**System boundaries:** Handles all data retrieval, state coordination, search management, selection coordination, and cross-system data distribution; integrates with every major system through central hub patterns

### Core Files (Always Work Together)

#### **Central Coordination Hub:**

- `useCards.ts` (8,678 bytes) - **CRITICAL:** 6-hook coordinator with effect-based reactivity, pass-through patterns, coordinatedLoadMore, clean separation of concerns
  
  #### **API Integration Layer (Extremely Complex):**
- `scryfallApi.ts` (31,333 bytes) - **EXTREMELY COMPLEX:** Sophisticated API abstraction with 15+ major functions, enhanced query building, wildcard optimization, complex filter building, stored pagination state management, rate limiting, performance monitoring
  
  #### **Data Foundation:**
- `card.ts` (15,478 bytes) - **COMPREHENSIVE:** Dual identity system (Cards vs Instances), conversion utilities, instance management, double-faced card support, progressive loading types, bridge utilities
  
  #### **Selection Management:**
- `useCardSelection.ts` (1,689 bytes) - **SIMPLE:** Card-based selection for collection area with Set<string> management, clean state patterns
  
  #### **Search Coordination:**
- `useSearchSuggestions.ts` (1,994 bytes) - **SIMPLE:** Autocomplete and search history management with API integration
  
  ### Integration Points
  
  **Receives data from:**
- **Scryfall API:** All card data through sophisticated scryfallApi.ts abstraction with rate limiting and performance optimization
- **User Input:** Search queries, filter selections, pagination requests through coordinated hook patterns
- **Cross-System State:** View modes, sort preferences, selection state through central coordination hub
  **Provides data to:**
- **All Display Systems:** Card collections, search results, filtered data through useCards central distribution
- **Selection Systems:** Card vs instance selection patterns with dual identity support and cross-system coordination
- **Layout Systems:** Data-driven responsive behavior, loading states, pagination states through coordinated patterns
- **Export Systems:** Selected data, deck collections, metadata through comprehensive data access patterns
  **Coordinates with:**
- **Search & Filtering System:** Complete integration through useCards hub with 6-hook coordination and effect-based reactivity
- **Performance System:** Wildcard optimization, rate limiting, progressive loading, device detection integration for data loading efficiency
- **All UI Systems:** Through MTGOLayout prop distribution receiving data state and actions from central coordinator
  
  ## 🔄 Critical Data Flows
  
  ### Primary Flow: Central 6-Hook Coordination & Effect-Based Reactivity
  
  ```
  useCards (Central Coordinator Hub) → 6-hook integration → Clean separation of concerns
  ↓
  Hook Integration: useFilters + useSearch + usePagination + useCardSelection + useSearchSuggestions + useSorting
  ↓
  Effect-Based Reactivity: Filter changes → searchWithAllFilters('*') trigger → Fresh search coordination
  ↓
  Pass-Through Pattern: Expose sub-hook functions without duplication → Clean API to components
  ↓
  Coordination Functions: coordinatedLoadMore manages pagination + search state together → Error handling
  ```
  
  ### Complex Flow: API Integration & Enhanced Query Building
  
  ```
  User Query → buildEnhancedSearchQuery (scryfallApi.ts) → Query optimization → API efficiency
  ↓
  [Wildcard '*'] → Early return (prevents 80+ second expensive multi-field searches) → Performance optimization
  ↓
  [Multi-word] → (name:word1 OR o:word1 OR type:word1) comprehensive field search → Enhanced search capability
  ↓
  [Advanced operators] → Quoted phrases, exclusions, field searches → Professional query building
  ↓
  Complex Filter Building → Format, colors (gold mode), types, subtypes, ranges → Scryfall parameter assembly
  ```
  
  ### Sophisticated Flow: Progressive Loading & Stored Pagination State Management
  
  ```
  Initial Search → searchCardsWithPagination → 75 cards from 175-card Scryfall page → Display optimization
  ↓
  Stored State Creation → currentPageCards (full page), cardsConsumedFromCurrentPage (75) → 422 error prevention
  ↓
  Load More Request → loadMoreResults decision logic → Use remaining cards vs fetch new page
  ↓
  [Remaining cards available] → Slice from currentPageCards → No API call → Instant results
  ↓
  [No remaining cards] → Fetch next Scryfall page → Store new currentPageCards → Continue coordination
  ```
  
  ### Advanced Flow: Dual Identity System & Type Management
  
  ```
  API Response (ScryfallCard[]) → Collection display → Card-based selection (card.id)
  ↓
  Add to Deck → scryfallToDeckInstance conversion → DeckCardInstance creation (unique instanceId)
  ↓
  Instance Management → groupInstancesByCardId, quantity tracking, removal coordination → Deck building
  ↓
  Bridge Utilities → getCardId(), getSelectionId() → Context-aware ID handling → Cross-system compatibility
  ```
  
  ### Performance Flow: Wildcard Optimization & Rate Limiting
  
  ```
  Query Analysis → buildEnhancedSearchQuery → Early wildcard detection → Performance optimization
  ↓
  [Query === '*'] → Simple wildcard return → Leverage Scryfall optimizations → Avoid 80+ second responses
  ↓
  Rate Limiting → 100ms delays between requests → Comprehensive timing analysis → API compliance
  ↓
  Performance Monitoring → console.time/timeEnd throughout → API timing, JSON parsing, query building → Optimization data
  ```
  
  ### Integration Flow: Cross-System Data Distribution
  
  ```
  useCards State → MTGOLayout prop distribution → 30+ props to area components
  ↓
  Search Results → CollectionArea display → Card selection coordination → Export integration
  ↓
  Selection State → Dual selection (cards vs instances) → Drag & drop coordination → Context menu integration
  ↓
  Filter Changes → Effect reactivity → Fresh search triggers → Cross-system state synchronization
  ```
  
  ### Advanced Flow: Search Suggestion & History Coordination
  
  ```
  Search Input → useSearchSuggestions coordination → getSearchSuggestions API call → Autocomplete display
  ↓
  Search History → addToSearchHistory (10 items max) → Recent search tracking → User experience enhancement
  ↓
  API Suggestions → Card names, Magic terms, operators → Comprehensive suggestion building → Professional search UX
  ```
  
  ## 🐛 Problem Diagnosis
  
  ### Central Coordination Issues
  
  **"Hook coordination not working or effects not triggering"**
- **Root Cause:** useCards effect dependencies or 6-hook integration failure
- **Check Files:** `useCards.ts` (effect dependency arrays, isInitialMount logic) → hook integration patterns → pass-through function coordination
- **Debug Pattern:** Verify useCards effect triggers → check 6-hook integration → validate pass-through pattern → confirm coordination functions
  **"Filter changes not triggering fresh search"**
- **Root Cause:** Effect-based reactivity failure or filter change detection issues
- **Check Files:** `useCards.ts` (filter change effect, hasActiveFilters integration) → `useFilters.ts` coordination → searchWithAllFilters execution
- **Debug Pattern:** Check filter change effect triggers → verify hasActiveFilters calculation → validate searchWithAllFilters call → confirm API integration
  **"coordinatedLoadMore not working correctly"**
- **Root Cause:** Pagination + search hook coordination failure or state synchronization issues
- **Check Files:** `useCards.ts` (coordinatedLoadMore function) → `usePagination.ts` coordination → `useSearch.ts` loadMoreCards integration
- **Debug Pattern:** Verify pagination state → check search hook coordination → validate error handling → confirm state synchronization
  
  ### API Integration Issues
  
  **"Search queries taking 80+ seconds or timing out"**
- **Root Cause:** Wildcard optimization not working or expensive multi-field query building
- **Check Files:** `scryfallApi.ts` (buildEnhancedSearchQuery, wildcard optimization) → query building logic → early return validation
- **Debug Pattern:** Check wildcard optimization (query === '*') → verify early return logic → validate multi-field query building → confirm performance optimization
  **"Enhanced query building not working correctly"**
- **Root Cause:** Query parsing logic failure or operator handling issues
- **Check Files:** `scryfallApi.ts` (buildEnhancedSearchQuery function) → multi-word field search → operator parsing logic
- **Debug Pattern:** Check multi-word query handling → verify operator parsing (quotes, exclusions, field searches) → validate Scryfall syntax → confirm enhanced search capability
  **"Complex filter building failing or wrong results"**
- **Root Cause:** SearchFilters logic failure or Scryfall parameter assembly issues
- **Check Files:** `scryfallApi.ts` (searchCardsWithFilters function) → filter building logic → parameter assembly
- **Debug Pattern:** Check filter building logic → verify gold mode coordination → validate range filters → confirm Scryfall parameter assembly
  **"Load More causing 422 errors"**
- **Root Cause:** Stored pagination state failure or Load More decision logic issues
- **Check Files:** `scryfallApi.ts` (loadMoreResults function) → stored pagination state management → decision logic validation
- **Debug Pattern:** Check currentPageCards preservation → verify cardsConsumedFromCurrentPage calculation → validate Load More decision logic → confirm 422 error prevention
  **"Rate limiting not working or API calls too frequent"**
- **Root Cause:** rateLimitedFetch logic failure or timing coordination issues
- **Check Files:** `scryfallApi.ts` (rateLimitedFetch function) → rate limiting logic → timing analysis
- **Debug Pattern:** Check 100ms rate limiting → verify timing analysis (console.time/timeEnd) → validate delay calculation → confirm API compliance
  
  ### Data Type & Identity Issues
  
  **"Card vs instance selection not working correctly"**
- **Root Cause:** Dual identity system failure or bridge utility issues
- **Check Files:** `card.ts` (getCardId, getSelectionId utilities) → dual identity patterns → `useCardSelection.ts` coordination
- **Debug Pattern:** Check dual identity utilities → verify card vs instance detection → validate selection ID routing → confirm cross-system compatibility
  **"Instance management not working (quantities, grouping)"**
- **Root Cause:** Instance utility functions or deck building coordination failure
- **Check Files:** `card.ts` (instance management utilities) → groupInstancesByCardId, quantity functions → deck building integration
- **Debug Pattern:** Check instance utility functions → verify grouping logic → validate quantity calculations → confirm deck building coordination
  **"Double-faced card support not working"**
- **Root Cause:** CardFace integration or face-specific utility failure
- **Check Files:** `card.ts` (CardFace interface, card_faces support) → face-specific utilities → image handling coordination
- **Debug Pattern:** Check CardFace interface usage → verify face-specific utilities → validate image handling → confirm 3D flip integration
  
  ### Progressive Loading Issues
  
  **"Initial search not limiting to 75 cards correctly"**
- **Root Cause:** searchCardsWithPagination logic or INITIAL_PAGE_SIZE coordination failure
- **Check Files:** `scryfallApi.ts` (searchCardsWithPagination function) → INITIAL_PAGE_SIZE application → stored state creation
- **Debug Pattern:** Check 75-card limiting logic → verify stored pagination state creation → validate currentPageCards storage → confirm display optimization
  **"Stored pagination state getting corrupted"**
- **Root Cause:** PaginatedSearchState management or Load More coordination failure
- **Check Files:** `card.ts` (PaginatedSearchState interface) → `scryfallApi.ts` (stored state management) → coordination patterns
- **Debug Pattern:** Check PaginatedSearchState structure → verify stored state updates → validate Load More coordination → confirm state preservation
  
  ### Selection & Suggestion Issues
  
  **"Card selection not working in collection area"**
- **Root Cause:** useCardSelection simple state management or useCards coordination failure
- **Check Files:** `useCardSelection.ts` (Set<string> management) → `useCards.ts` (pass-through coordination) → component integration
- **Debug Pattern:** Check Set<string> state management → verify useCards pass-through → validate component integration → confirm selection coordination
  **"Search suggestions not appearing or wrong suggestions"**
- **Root Cause:** useSearchSuggestions coordination or API integration failure
- **Check Files:** `useSearchSuggestions.ts` (suggestion management) → `scryfallApi.ts` (getSearchSuggestions function) → API suggestion coordination
- **Debug Pattern:** Check suggestion state management → verify API suggestion calls → validate suggestion building → confirm autocomplete integration
  
  ### Debugging Starting Points
  
  **Central coordination issues:** Start with `useCards.ts` effect dependencies → 6-hook integration verification → pass-through pattern validation 
  **API integration problems:** Start with `scryfallApi.ts` specific function → query building/filter building/pagination logic → rate limiting verification 
  **Data type issues:** Start with `card.ts` utility functions → dual identity patterns → bridge utility validation 
  **Progressive loading issues:** Start with `scryfallApi.ts` pagination functions → stored state management → Load More decision logic 
  **Selection/suggestion issues:** Start with specific hook → useCards coordination → API integration verification 
  **Performance issues:** Start with `scryfallApi.ts` wildcard optimization → rate limiting → timing analysis validation 
  **Cross-system integration:** Start with `useCards.ts` coordination → MTGOLayout prop distribution → component integration patterns
  
  ## 🔧 Architecture Details
  
  ### State Management Pattern
  
  **How state is organized:** Central coordination through useCards hub managing 6 specialized hooks (useFilters, useSearch, usePagination, useCardSelection, useSearchSuggestions, useSorting) with sophisticated API integration through scryfallApi.ts and comprehensive data type management through card.ts dual identity system 
  **State flow:** API responses → useSearch processing → useCards coordination → 6-hook integration → effect-based reactivity → MTGOLayout prop distribution → component rendering 
  **Key state variables:** Search results (useSearch), active filters (useFilters), pagination state (usePagination), card selection (useCardSelection), search suggestions (useSearchSuggestions), sort criteria (useSorting), stored pagination state (scryfallApi.ts), dual identity management (card.ts)
  
  ### Critical Functions & Hooks
  
  #### **Central Coordination Hub (useCards.ts):**
  
  **6-hook integration:** useFilters + useSearch + usePagination + useCardSelection + useSearchSuggestions + useSorting with clean separation of concerns 
  **Effect-based reactivity:** Filter change detection → searchWithAllFilters('*') trigger → fresh search coordination with initial mount skip (isInitialMount.current) 
  **Pass-through pattern:** Expose sub-hook functions without duplication → clean API to components with proper coordination 
  **coordinatedLoadMore:** Sophisticated Load More coordination between pagination state and search engine with comprehensive error handling 
  **Sort coordination:** getCollectionSortParams callback integration with useSorting for dual sort system support
  
  #### **Extremely Complex API Layer (scryfallApi.ts):**
  
  **buildEnhancedSearchQuery:** Complex query building with wildcard optimization (early return for '*'), multi-word field search, operator parsing (quotes, exclusions, field searches) 
  **Multiple Search Variants:** searchCards (core), searchCardsWithSort (sort wrapper), searchCardsWithFilters (complex filter building), searchCardsWithPagination (75-card initial), enhancedSearchCards (enhanced query + filters), loadMoreResults (sophisticated Load More) 
  **Complex Filter Building:** searchCardsWithFilters with format filters, color coordination (gold mode), type/subtype filters, range filters (CMC, power, toughness), comprehensive Scryfall parameter assembly 
  **Stored Pagination Management:** loadMoreResults with decision logic (use remaining cards vs fetch new page), currentPageCards storage, cardsConsumedFromCurrentPage tracking, 422 error prevention 
  **Rate Limiting & Performance:** rateLimitedFetch with 100ms delays, comprehensive timing analysis (console.time/timeEnd), performance monitoring throughout, wildcard optimization preventing 80+ second responses 
  **Search Suggestions:** getSearchSuggestions with card names, Magic terms, operators for comprehensive autocomplete support
  
  #### **Comprehensive Data Foundation (card.ts):**
  
  **Dual Identity System:** ScryfallCard (collection context, card.id selection) vs DeckCardInstance (deck context, instanceId selection) with complete bridge utilities 
  **Conversion Utilities:** scryfallToDeckInstance (primary conversion), generateInstanceId/parseInstanceId (unique instance tracking), getCardId/getSelectionId (context-aware ID handling) 
  **Instance Management:** groupInstancesByCardId, getCardQuantityInZone, getTotalCardQuantity, removeInstancesForCard, removeSpecificInstances for comprehensive deck building support 
  **Double-Faced Support:** CardFace interface, card_faces array support, face-specific image utilities (getCardImageUri with PNG preference), 3D flip integration 
  **Progressive Loading Types:** PaginatedSearchState interface with sophisticated pagination state management, ProgressiveLoadingConfig for loading coordination 
  **Image Handling:** PNG preference (745×1040), double-faced card face selection, fallback strategies for consistent display quality
  
  #### **Selection & Suggestion Coordination:**
  
  **useCardSelection (simple):** Set<string> management for card-based selection (collection area), selectCard/deselectCard/clearSelection/isCardSelected patterns, getSelectedCardsData filtering 
  **useSearchSuggestions (simple):** Search suggestion state management, search history (10 items max), API suggestion coordination through getSearchSuggestions, autocomplete display coordination
  
  ### Component Hierarchy
  
  ```
  scryfallApi.ts (Extremely Complex API Layer - 31,333 bytes)
  ├── Enhanced Query Building:
  │ ├── buildEnhancedSearchQuery (wildcard optimization + multi-word field search + operator parsing)
  │ ├── Wildcard Optimization (early return for '*' preventing 80+ second responses)
  │ ├── Multi-Word Enhancement ((name:word1 OR o:word1 OR type:word1) comprehensive field search)
  │ └── Operator Parsing (quoted phrases, exclusions, field searches with Scryfall syntax)
  ├── Multiple Search Variants:
  │ ├── searchCards (core search with sort parameters)
  │ ├── searchCardsWithSort (sort coordination wrapper)
  │ ├── searchCardsWithFilters (complex filter building with gold mode support)
  │ ├── searchCardsWithPagination (75-card initial + stored pagination state)
  │ ├── enhancedSearchCards (enhanced query building + filter coordination)
  │ └── loadMoreResults (sophisticated Load More with 422 error prevention)
  ├── Complex Filter Building:
  │ ├── Format Filters (legal:standard/modern/etc with custom format support)
  │ ├── Color Coordination (gold mode color>=2 vs standard color identity filters)
  │ ├── Type/Subtype Filters (OR logic coordination for multiple selections)
  │ ├── Range Filters (CMC, power, toughness with proper Scryfall syntax)
  │ └── Comprehensive Parameter Assembly (SearchFilters → Scryfall query string)
  ├── Sophisticated Pagination Management:
  │ ├── Initial Load (75 cards from 175-card Scryfall page with stored state creation)
  │ ├── Stored State Tracking (currentPageCards, cardsConsumedFromCurrentPage, remainingInCurrentPage)
  │ ├── Load More Decision Logic (use remaining cards vs fetch new page for 422 error prevention)
  │ └── Progressive Loading Coordination (PaginatedSearchState comprehensive management)
  ├── Rate Limiting & Performance:
  │ ├── rateLimitedFetch (100ms delays + comprehensive timing analysis)
  │ ├── Performance Monitoring (console.time/timeEnd for API, JSON parsing, query building)
  │ ├── Wildcard Optimization (prevents expensive multi-field searches)
  │ └── API Compliance (proper headers, error handling, response validation)
  └── Search Suggestions & Utilities:
  ├── getSearchSuggestions (card names + Magic terms + operators)
  ├── Autocomplete coordination (10-item suggestions with term matching)
  ├── Common query constants (POPULAR_CARDS, BASIC_LANDS, etc.)
  └── Utility functions (getRandomCard, getCardById, getSets, etc.)
  ↓
  useCards (Central Coordination Hub - 8,678 bytes)
  ├── 6-Hook Integration (Clean Separation of Concerns):
  │ ├── useFilters (filter state + pass-through functions)
  │ ├── useSearch (search engine + API coordination with callback patterns)
  │ ├── usePagination (pagination state bridge + coordination callbacks)
  │ ├── useCardSelection (simple Set<string> management for collection area)
  │ ├── useSearchSuggestions (autocomplete + history with API integration)
  │ └── useSorting (sort parameter coordination with dual sort system)
  ├── Effect-Based Reactivity:
  │ ├── Filter Change Detection (activeFilters dependency → searchWithAllFilters('*') trigger)
  │ ├── Initial Mount Skip (isInitialMount.current prevents loadPopularCards interference)
  │ └── Clean Search Coordination (fresh search on filter changes with hasActiveFilters validation)
  ├── Pass-Through Pattern:
  │ ├── Filter Functions (updateFilter, clearAllFilters, etc. → useFilters coordination)
  │ ├── Search Functions (searchForCards, enhancedSearch, etc. → useSearch coordination)
  │ ├── Selection Functions (selectCard, clearSelection, etc. → useCardSelection coordination)
  │ └── Suggestion Functions (getSearchSuggestions, addToSearchHistory → useSearchSuggestions coordination)
  ├── Coordination Functions:
  │ ├── coordinatedLoadMore (pagination + search state coordination with error handling)
  │ ├── getCollectionSortParams (sort coordination callback with useSorting integration)
  │ ├── clearAllFilters (enhanced filter clearing + loadPopularCards coordination)
  │ └── getSelectedCardsData (current cards filtering based on selection state)
  └── State Composition & API:
  ├── Complete State Interface (UseCardsState with all hook state integration)
  ├── Complete Actions Interface (UseCardsActions with all coordination functions)
  └── Clean Component API (comprehensive state + actions for MTGOLayout distribution)
  ↓
  card.ts (Comprehensive Data Foundation - 15,478 bytes)
  ├── Dual Identity System:
  │ ├── ScryfallCard (collection context with card.id selection for search results)
  │ ├── DeckCardInstance (deck context with instanceId selection for deck building)
  │ ├── Bridge Utilities (getCardId, getSelectionId for context-aware ID handling)
  │ └── Legacy DeckCard (backward compatibility with deprecation path)
  ├── Type Definitions & Interfaces:
  │ ├── Core Card Types (ScryfallCard, CardFace, DeckCardInstance with comprehensive properties)
  │ ├── API Response Types (ScryfallSearchResponse, ScryfallError, SearchParams)
  │ ├── Progressive Loading Types (PaginatedSearchState, ProgressiveLoadingConfig)
  │ └── Utility Types (MagicFormat, MagicColor, LegalityStatus, RateLimitInfo)
  ├── Conversion & Bridge Utilities:
  │ ├── scryfallToDeckInstance (primary conversion for deck building)
  │ ├── generateInstanceId/parseInstanceId (unique instance tracking with zone info)
  │ ├── getCardId/getSelectionId (context-aware ID handling for dual identity)
  │ └── isCardInstance/isScryfallCard (type detection utilities)
  ├── Instance Management:
  │ ├── groupInstancesByCardId (Map<string, DeckCardInstance[]> organization)
  │ ├── Quantity Management (getCardQuantityInZone, getTotalCardQuantity)
  │ ├── Instance Removal (removeInstancesForCard, removeSpecificInstances)
  │ └── Deck Building Support (getInstancesForCard, quantity tracking)
  ├── Double-Faced Card Support:
  │ ├── CardFace Interface (complete face properties for transform cards)
  │ ├── Image Handling (getCardImageUri with PNG preference, face selection)
  │ ├── Face-Specific Utilities (face detection, image resolution, 3D flip support)
  │ └── Integration Support (card_faces array preservation, conversion coordination)
  └── Utility Functions:
  ├── Image Optimization (PNG preference 745×1040, fallback strategies)
  ├── Basic Land Detection (comprehensive basic land recognition)
  ├── Conversion Functions (scryfallToDeckCard for legacy compatibility)
  └── Constants & Helpers (MAGIC_COLORS, format definitions, utility constants)
  ↓
  Component Integration Layer
  ├── MTGOLayout.tsx (Central Prop Distribution)
  │ ├── useCards State Consumption (complete state + actions integration)
  │ ├── 30+ Props Distribution (cards, loading, actions, selection state, etc.)
  │ ├── Cross-System Coordination (data + selection + layout + context integration)
  │ └── Component Orchestration (CollectionArea, DeckArea, SideboardArea coordination)
  ├── CollectionArea.tsx (Search Results Display)
  │ ├── Data Consumption (cards, loading, pagination state from useCards)
  │ ├── Selection Integration (card selection coordination with dual selection system)
  │ ├── View Mode Coordination (grid/list display with data optimization)
  │ └── Load More Integration (coordinatedLoadMore with progress display)
  ├── DeckArea.tsx & SideboardArea.tsx (Instance Management)
  │ ├── Instance Data (DeckCardInstance arrays from deck state)
  │ ├── Quantity Display (instance counting and grouping for deck building)
  │ ├── Instance Selection (instanceId-based selection for deck management)
  │ └── Cross-System Integration (drag, selection, context menu with data coordination)
  └── Search & Filter Components:
  ├── SearchAutocomplete.tsx (search input with suggestion integration)
  ├── FilterPanel.tsx (filter controls with useCards pass-through functions)
  └── Various Controls (sort, pagination, view mode with data state coordination)
  ```
  
  ### Performance Considerations
  
  **Critical paths:** Central 6-hook coordination (useCards), API integration complexity (scryfallApi.ts 15+ functions), dual identity system management (card.ts), progressive loading coordination (stored pagination state), complex filter building (SearchFilters), effect-based reactivity (filter changes), wildcard optimization (query building), rate limiting (100ms API delays) 
  **Optimization patterns:** Wildcard optimization prevents 80+ second queries, rate limiting with timing analysis, progressive loading (75-card initial + smart Load More), stored pagination state prevents 422 errors, dual identity bridge utilities, 6-hook clean separation of concerns, effect-based reactivity with initial mount skip, comprehensive data type management 
  **Known bottlenecks:** scryfallApi.ts extreme complexity (31,333 bytes), buildEnhancedSearchQuery parsing overhead, complex filter building logic, stored pagination state management complexity, 6-hook coordination overhead in useCards, dual identity conversion performance, progressive loading decision logic complexity
  
  ## ⚠️ Current System Status
  
  ### Working Functionality
- ✅ **Central 6-Hook Coordination:** useCards successfully coordinates all data hooks with clean separation of concerns and pass-through patterns
- ✅ **Effect-Based Reactivity:** Filter changes trigger fresh searches with initial mount skip preventing loadPopularCards interference
- ✅ **Sophisticated API Integration:** scryfallApi.ts provides comprehensive search capabilities with enhanced query building and complex filter coordination
- ✅ **Wildcard Optimization:** Early return for '*' queries prevents expensive 80+ second multi-field searches with significant performance improvement
- ✅ **Progressive Loading:** 75-card initial display with sophisticated Load More using stored pagination state preventing 422 errors
- ✅ **Complex Filter Building:** SearchFilters with format, colors (gold mode), types, subtypes, ranges providing comprehensive search capabilities
- ✅ **Dual Identity System:** Cards vs Instances with bridge utilities supporting collection display and deck building contexts seamlessly
- ✅ **Rate Limiting & Performance:** 100ms API delays with comprehensive timing analysis ensuring API compliance and performance monitoring
- ✅ **Enhanced Query Building:** Multi-word field searches, operator parsing, advanced query enhancement for professional search capabilities
- ✅ **Search Suggestions:** Autocomplete with card names, Magic terms, operators, and search history (10 items) for enhanced user experience
- ✅ **Instance Management:** Complete deck building support with quantity tracking, grouping, removal functions for deck management
- ✅ **Double-Faced Card Support:** CardFace interface, face-specific utilities, PNG image optimization for 3D flip integration
- ✅ **Stored Pagination State:** Comprehensive management preventing API errors with sophisticated Load More decision logic
- ✅ **Cross-System Integration:** Complete data flow from API → useCards → MTGOLayout → Components with proper state distribution
  
  ### Known Issues
- ⚠️ **scryfallApi.ts Extreme Complexity:** 31,333 bytes with 15+ major functions creating significant maintenance complexity and learning curve
- ⚠️ **Multiple API Search Variants:** 5+ different search functions (searchCards, searchCardsWithSort, etc.) creating maintenance overhead and complexity
- ⚠️ **Enhanced Query Building Complexity:** buildEnhancedSearchQuery parsing logic complex and could benefit from simplification or extraction
- ⚠️ **Complex Filter Building:** searchCardsWithFilters extensive logic could benefit from extraction to dedicated filter building service
- ⚠️ **Stored Pagination State Complexity:** Sophisticated state management for Load More requires careful coordination and understanding
- ⚠️ **6-Hook Coordination Overhead:** Central coordination through useCards creates complexity requiring careful dependency management
- ⚠️ **Dual Identity System Complexity:** Cards vs Instances with bridge utilities adds architectural complexity requiring consistent usage patterns
- ⚠️ **API Function Proliferation:** Multiple search variants and utility functions creating API surface area management challenges
- ⚠️ **Progressive Loading Decision Logic:** Complex Load More coordination requiring sophisticated state management and error handling
  
  ### Technical Debt
  
  **Priority Items:**
- **P2:** scryfallApi.ts size and complexity (31,333 bytes) - consider extraction of query building, filter logic, or pagination management into separate services
- **P2:** Multiple API search variants (5+ functions) - consider consolidation or better organization to reduce maintenance complexity
- **P2:** Enhanced query building complexity (buildEnhancedSearchQuery) - consider extraction or simplification of parsing logic
- **P2:** Complex filter building logic (searchCardsWithFilters) - consider extraction to dedicated filter service for better maintainability
- **P3:** 6-hook coordination complexity in useCards - monitor for performance impact and consider optimization if needed
- **P3:** Stored pagination state management - sophisticated but necessary complexity requiring careful documentation and testing
- **P3:** Dual identity system maintenance - Cards vs Instances pattern requires consistent usage and bridge utility maintenance
- **P3:** API function proliferation - multiple search variants and utilities creating surface area management challenges
- **P4:** Progressive loading decision logic - complex but working Load More coordination with comprehensive error handling
- **P4:** Card.ts size (15,478 bytes) - comprehensive type foundation but approaching maintainability limits with many utility functions
  
  ### Recent Changes
  
  **API integration enhancement:** Wildcard optimization, enhanced query building, complex filter coordination, stored pagination state management 
  **Central coordination optimization:** 6-hook integration with effect-based reactivity, pass-through patterns, coordinatedLoadMore function 
  **Data type foundation:** Dual identity system implementation, comprehensive instance management, double-faced card support
  
  ## 🚀 Development Patterns
  
  ### Common Change Patterns
  
  #### **Adding Central Coordination Features:**
1. **Start with:** `useCards.ts` → 6-hook integration → effect-based reactivity → pass-through pattern implementation
2. **Consider complexity:** Hook coordination overhead → effect dependency management → callback coordination patterns
3. **Test by:** Multi-hook integration verification → effect reactivity testing → cross-system coordination validation
   
   #### **Adding API Integration Features:**
4. **Start with:** `scryfallApi.ts` → specific function implementation → query building or filter coordination → rate limiting integration
5. **Consider complexity:** API variant consolidation → function organization → maintenance overhead assessment
6. **Test by:** API integration testing → query building validation → filter coordination verification → rate limiting effectiveness
   
   #### **Adding Data Type Features:**
7. **Start with:** `card.ts` → dual identity system → conversion utilities → instance management patterns
8. **Consider integration:** Bridge utility usage → type detection patterns → cross-system compatibility verification
9. **Test by:** Dual identity validation → conversion accuracy testing → instance management functionality verification
   
   #### **Adding Progressive Loading Features:**
10. **Start with:** `scryfallApi.ts` → pagination functions → stored state management → Load More coordination
11. **Consider complexity:** Stored state tracking → decision logic coordination → 422 error prevention validation
12. **Test by:** Progressive loading accuracy → Load More functionality → stored state persistence → error handling validation
    
    #### **Adding Selection Features:**
13. **Start with:** `useCardSelection.ts` → simple state management → `useCards.ts` → pass-through coordination
14. **Consider integration:** Dual selection coordination → cross-system selection patterns → component integration
15. **Test by:** Selection state accuracy → cross-system coordination → component integration validation
    
    #### **Adding Search Features:**
16. **Start with:** `scryfallApi.ts` → enhanced query building → `useCards.ts` → coordination integration
17. **Consider complexity:** Query optimization → search suggestion coordination → cross-system integration patterns
18. **Test by:** Search functionality accuracy → suggestion integration → cross-system search coordination
    
    ### File Modification Order
    
    #### **For central coordination changes:** `useCards.ts` (6-hook integration) → hook coordination validation → effect reactivity testing → pass-through pattern verification
    
    #### **For API integration changes:** `scryfallApi.ts` (specific function) → query building/filter coordination → rate limiting integration → API testing validation
    
    #### **For data type changes:** `card.ts` (dual identity/utilities) → conversion function testing → bridge utility validation → cross-system integration testing
    
    #### **For progressive loading changes:** `scryfallApi.ts` (pagination functions) → stored state coordination → Load More testing → 422 error prevention validation
    
    #### **For selection changes:** `useCardSelection.ts` (state management) → `useCards.ts` (coordination) → component integration → selection testing
    
    #### **For search suggestion changes:** `useSearchSuggestions.ts` (suggestion management) → `scryfallApi.ts` (API integration) → `useCards.ts` (coordination) → UI integration testing
    
    ### Testing Strategy
    
    **Critical to test:** Central 6-hook coordination (useCards), API integration accuracy (scryfallApi.ts functions), dual identity system (Cards vs Instances), progressive loading (stored pagination state), complex filter building (SearchFilters), effect-based reactivity (filter changes), wildcard optimization effectiveness, rate limiting compliance 
    **Integration tests:** Cross-hook coordination through useCards, API → useCards → component data flow, dual identity conversion accuracy, progressive loading with Load More functionality, search suggestion integration, filter coordination across systems 
    **Performance validation:** Wildcard optimization effectiveness (prevent 80+ second queries), rate limiting compliance (100ms delays), progressive loading efficiency, 6-hook coordination performance, API timing analysis, stored pagination state management efficiency

---

**System Guide Notes:**

- useCards.ts provides central coordination for 6 specialized hooks with clean separation of concerns and effect-based reactivity
- scryfallApi.ts is extremely complex (31,333 bytes) with 15+ major functions providing comprehensive API integration with sophisticated optimization
- card.ts provides comprehensive data foundation with dual identity system (Cards vs Instances) supporting all display and deck building contexts
- useCardSelection.ts provides simple card-based selection for collection area with Set<string> management patterns
- useSearchSuggestions.ts provides lightweight autocomplete coordination with search history management and API integration
- Wildcard optimization in scryfallApi.ts prevents expensive 80+ second multi-field searches with early return for '*' queries
- Progressive loading uses stored pagination state to prevent 422 errors with sophisticated Load More decision logic
- Complex filter building supports comprehensive search capabilities including gold mode, ranges, types, and format coordination
- Dual identity system enables seamless coordination between collection display (Cards) and deck building (Instances) contexts
- Effect-based reactivity in useCards coordinates filter changes with fresh search triggers while preventing initial mount interference
- Rate limiting ensures API compliance with 100ms delays and comprehensive timing analysis throughout the system
- Enhanced query building provides professional search capabilities with multi-word field searches and operator parsing
- Central coordination hub pattern enables clean data distribution to all UI systems through MTGOLayout prop distribution
