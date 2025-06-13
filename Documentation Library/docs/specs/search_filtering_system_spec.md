# Search & Filtering System Specification

**Status:** Implemented + Performance Optimized  
**Last Updated:** June 12, 2025  
**Primary Files:** useSearch.ts (350 lines), useFilters.ts (120 lines), scryfallApi.ts (575 lines), useSorting.ts (270 lines)  
**Dependencies:** usePagination, useSearchSuggestions, card.ts types, Scryfall API  
**Performance Targets:** <1 second search response, zero 422 pagination errors, progressive loading

## Purpose & Intent

**Core Functionality:** Multi-field card search with advanced filtering, server-side sorting, and progressive loading for large datasets  
**Design Philosophy:** Clean parameter management, dual sort system, and comprehensive filter coordination  
**MTGO Authenticity Requirements:** Professional search experience with instant responsiveness and reliable pagination

## Technical Architecture

### File Organization

**Core Files:**
- `useSearch.ts` (350 lines) - Central search coordinator with API integration and dual sort system
- `useFilters.ts` (120 lines) - Comprehensive filter state management with section collapsibility
- `scryfallApi.ts` (575 lines) - Enhanced API layer with wildcard optimization and robust pagination
- `useSorting.ts` (270 lines) - Performance-optimized sorting with stable dependencies
- `usePagination.ts` (120 lines) - Simplified pagination state management
- `useSearchSuggestions.ts` (70 lines) - Autocomplete and search history
- `search.ts` (120 lines) - Enhanced search types and operator definitions

**Integration Points:**
- **useCards Hub:** Coordinates all search hooks through clean parameter management
- **Scryfall API:** Enhanced query building with wildcard optimization and full-text search
- **UI Components:** SearchAutocomplete, FilterPanel, SubtypeInput with professional styling
- **Dual Sort System:** Client-side (≤75 cards) vs server-side (>75 cards) decision logic

### State Management Patterns

**State Architecture:** Coordinated through useCards with extracted focused hooks  
**Data Flow:** Search input → useSearch → scryfallApi → stored pagination state → progressive loading  
**Performance Optimizations:** Re-render loop elimination, stable dependencies, wildcard query optimization  
**Error Handling:** 422 prevention through stored pagination state, graceful degradation for failed searches

### Key Implementation Decisions

**Clean Parameter Management:** Build filter objects from scratch each search, never inherit from previous searches  
**Dual Sort System:** Complete datasets (≤75 cards) use client-side sorting, larger datasets trigger server-side re-search  
**Stored Pagination State:** Full page data stored to prevent 422 errors during Load More operations  
**Wildcard Optimization:** Early detection of simple wildcard queries to prevent expensive full-text enhancement

## User Experience Design

### Core Functionality

**Primary Use Cases:**
1. **Text Search:** Multi-field search across card names, oracle text, and type lines with operator support
2. **Advanced Filtering:** Comprehensive filters including colors, types, subtypes, rarity, sets, and stats
3. **Progressive Loading:** Initial 75 cards with Load More functionality for larger result sets
4. **Intelligent Sorting:** Automatic client/server sort decision based on dataset size

**Interaction Patterns:**
- **Search Input:** Enhanced autocomplete with search history and operator suggestions
- **Filter Application:** Real-time filter updates trigger fresh searches with clean parameter coordination
- **Sort Changes:** Instant client-side sorting for small datasets, server-side re-search for large datasets
- **Load More:** Seamless progressive loading with scroll position preservation

### Visual Design Standards

**MTGO Authenticity:**
- **Search Interface:** Professional dark theme with responsive autocomplete dropdown
- **Filter Panel:** Collapsible sections with active filter indicators and MTGO-style color buttons
- **Progressive Loading:** Smooth card appending with loading states and progress indication
- **Performance Feedback:** <1 second search response with immediate visual feedback

**Visual Feedback:**
- **Search States:** Loading indicators, error messages, empty state handling
- **Filter States:** Blue selection indicators, gold multicolor button, section expansion/collapse
- **Sorting States:** Clear sort direction indicators, loading during server-side sorts
- **Pagination States:** Load More button states, progress indication, smooth card appending

**Animation & Transitions:**
- **Performance Requirements:** 60fps smooth scrolling during card appending
- **Filter Interactions:** Instant visual feedback on color button selection
- **Section Management:** Smooth expand/collapse animations for filter sections
- **Search Responsiveness:** Immediate loading states with <150ms perceived delay

### Responsive Design

**Filter Panel Behavior:**
- **Desktop (1200px+):** Full filter panel with all options visible
- **Tablet (768-1199px):** Collapsible filter sections with priority ordering
- **Mobile (767px-):** Collapsed filter panel with essential filters only

**Search Interface:**
- **All Breakpoints:** Maintained search functionality with responsive autocomplete
- **Mobile Optimization:** Touch-friendly filter buttons and inputs

## Performance & Quality Standards

### Performance Benchmarks

**Search Response Times:**
- **Simple Queries:** <500ms including network latency
- **Complex Multi-Filter:** <1 second with full enhancement
- **Server-Side Sorts:** <2 seconds with loading indication
- **Progressive Loading:** <1 second per 75-card batch

**Resource Usage:**
- **Memory:** Efficient card data structures with cleanup during search changes
- **Network:** Optimized query building with wildcard optimization
- **Rendering:** Re-render loop elimination through stable hook dependencies

### Quality Assurance

**Testing Priorities:**
- **HIGH Risk:** Search parameter coordination, pagination state management, dual sort system
- **MEDIUM Risk:** Filter reactivity, autocomplete functionality, error handling
- **LOW Risk:** Visual feedback, section management, search history

**Regression Prevention:**
- **Core Search:** Parameter building, API integration, result handling
- **Performance:** <1 second response times, stable pagination, clean re-renders
- **State Management:** Filter coordination, sort system, progressive loading

## Evolution & Context

### Design Evolution

**Initial Implementation:** Basic search with simple filtering  
**Enhancement Phase:** Multi-field search, advanced filters, autocomplete system  
**Performance Optimization Phase:** Re-render elimination, wildcard optimization, 422 error prevention

**Key Changes & Rationale:**
- **useSearch Extraction:** Separated from monolithic useCards for focused responsibility
- **Dual Sort System:** Optimal performance for both small and large datasets
- **Stored Pagination State:** Eliminated 422 errors during Load More operations
- **Clean Parameter Management:** Prevents search parameter accumulation and filter inheritance issues

### Current Challenges & Future Considerations

**Known Limitations:** 
- Server-side sorting requires full re-search for large datasets
- Complex filter combinations may slow query building
- Mobile filter interface could be further optimized

**Future Enhancement Opportunities:**
- Real-time search suggestions with debouncing
- Saved search presets and favorites
- Advanced query syntax help and examples
- Filter preset sharing between users

**Architectural Considerations:**
- Progressive Web App offline search capabilities
- Search analytics and performance monitoring
- Advanced faceted search with dynamic filter suggestions

### Decision Context

**Why Dual Sort System:** Provides optimal performance for both small datasets (instant client-side) and large datasets (comprehensive server-side)  
**Why Clean Parameter Management:** Prevents complex filter inheritance bugs and ensures predictable search behavior  
**Why Stored Pagination State:** Eliminates 422 pagination errors by maintaining full page context during progressive loading  
**Why Wildcard Optimization:** Prevents expensive full-text enhancement for simple queries, improving response times

## Technical Implementation Details

### Search Query Building

**Enhanced Query Construction:**
- **Simple Queries:** Automatic multi-field search (name, oracle text, type)
- **Multi-word Queries:** Each word searches across all fields with OR logic
- **Operator Support:** Quoted phrases, exclusions, field-specific searches
- **Wildcard Optimization:** Early detection prevents expensive enhancement for simple wildcards

### Filter Coordination

**State Management:**
- **Section Collapsibility:** Per-section expanded/collapsed state with active filter indicators
- **Gold Mode:** Special handling for multicolor filtering with enhanced visual feedback
- **Auto-Expansion:** Sections automatically expand when filters are applied
- **Clean Inheritance:** Each search builds filters from scratch without inheritance

### Performance Patterns

**Re-render Elimination:**
- **Stable Dependencies:** useSorting hook optimized with proper memoization
- **Clean Coordination:** useSearch prevents accumulation through parameter management
- **Timing Analysis:** Console timing for performance debugging and optimization

### API Integration

**Scryfall Optimization:**
- **Rate Limiting:** 100ms delays with request coordination
- **Query Enhancement:** Smart field-based searches with operator support
- **Pagination Management:** Stored state prevents 422 errors during Load More
- **Error Handling:** Graceful degradation with user-friendly error messages

---

**Current Achievement:** Complete professional search system with <1 second response times and comprehensive filtering capabilities  
**Architecture Status:** Performance-optimized with proven patterns for complex search coordination  
**Development Readiness:** Stable foundation for advanced search features and mobile optimization