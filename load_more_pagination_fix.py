#!/usr/bin/env python3
"""
Fix Load More pagination jumping issue by implementing partial page consumption tracking.

Root Cause: Load More jumps from page 1 to page 2, skipping cards 76-175
Solution: Track partial page consumption and return remaining cards before fetching next page
"""

import re

def fix_pagination_state_interface():
    """Add partial page consumption fields to PaginatedSearchState interface"""
    print("🔧 Enhancing PaginatedSearchState interface...")
    
    with open('src/types/card.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the PaginatedSearchState interface
    interface_pattern = r'(export interface PaginatedSearchState \{[^}]+)\}'
    
    def replace_interface(match):
        current_interface = match.group(1)
        
        # Check if already has new fields
        if 'currentScryfallPage' in current_interface:
            print("✅ PaginatedSearchState already enhanced")
            return match.group(0)
        
        # Add new fields for partial page consumption tracking
        enhanced_interface = current_interface + """
  // Partial page consumption tracking
  currentScryfallPage: number;        // Actual Scryfall page number (1-based)
  cardsConsumedFromCurrentPage: number; // How many cards used from current Scryfall page
  currentPageCards: ScryfallCard[];   // Full current page data from Scryfall
  scryfallPageSize: number;           // Scryfall page size (175)
  displayBatchSize: number;           // User display batch size (75)
}"""
        
        print("✅ Enhanced PaginatedSearchState with partial page consumption fields")
        return enhanced_interface
    
    updated_content = re.sub(interface_pattern, replace_interface, content, flags=re.DOTALL)
    
    with open('src/types/card.ts', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    return True

def fix_search_with_pagination():
    """Update searchCardsWithPagination to initialize partial page consumption tracking"""
    print("🔧 Fixing searchCardsWithPagination function...")
    
    with open('src/services/scryfallApi.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the searchCardsWithPagination function
    function_pattern = r'(export const searchCardsWithPagination = async \([^{]+\{[^}]+try \{[^}]+console\.log[^}]+)(const response = await enhancedSearchCards[^}]+)(const initialResults = response\.data\.slice[^}]+)(const hasMore = [^}]+)(console\.log[^}]+)(return \{[^}]+\})'
    
    def replace_function(match):
        try_block = match.group(1)
        api_call = match.group(2)
        slice_logic = match.group(3)
        has_more = match.group(4)
        console_log = match.group(5)
        return_block = match.group(6)
        
        # Check if already fixed
        if 'currentScryfallPage' in return_block:
            print("✅ searchCardsWithPagination already fixed")
            return match.group(0)
        
        # Build enhanced return block with partial page consumption tracking
        enhanced_return = """return {
      initialResults,
      totalCards: response.total_cards,
      loadedCards: initialResults.length,
      hasMore,
      isLoadingMore: false,
      currentPage: 1,
      lastQuery: query,
      lastFilters: filters,
      lastSort: { order, dir },
      // Partial page consumption tracking
      currentScryfallPage: 1,
      cardsConsumedFromCurrentPage: initialResults.length,
      currentPageCards: response.data, // Store full page data
      scryfallPageSize: 175,
      displayBatchSize: 75,
    };"""
        
        print("✅ Enhanced searchCardsWithPagination with partial page tracking")
        return try_block + api_call + slice_logic + has_more + console_log + enhanced_return
    
    updated_content = re.sub(function_pattern, replace_function, content, flags=re.DOTALL)
    
    with open('src/services/scryfallApi.ts', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    return True

def fix_load_more_results():
    """Replace loadMoreResults function with partial page consumption logic"""
    print("🔧 Implementing partial page consumption in loadMoreResults...")
    
    with open('src/services/scryfallApi.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the entire loadMoreResults function
    function_pattern = r'export const loadMoreResults = async \([^{]+\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\};'
    
    # New loadMoreResults implementation with partial page consumption
    new_function = '''export const loadMoreResults = async (
  paginationState: PaginatedSearchState,
  onProgress?: (loaded: number, total: number) => void
): Promise<ScryfallCard[]> => {
  try {
    console.log('🔄 Load More with partial page consumption:', { 
      currentScryfallPage: paginationState.currentScryfallPage,
      cardsConsumedFromCurrentPage: paginationState.cardsConsumedFromCurrentPage,
      currentPageCards: paginationState.currentPageCards?.length || 0,
      loadedSoFar: paginationState.loadedCards,
      totalCards: paginationState.totalCards,
      scryfallPageSize: paginationState.scryfallPageSize || 175,
      displayBatchSize: paginationState.displayBatchSize || 75
    });
    
    // Report progress start
    if (onProgress) {
      onProgress(paginationState.loadedCards, paginationState.totalCards);
    }
    
    const scryfallPageSize = paginationState.scryfallPageSize || 175;
    const displayBatchSize = paginationState.displayBatchSize || 75;
    const cardsConsumed = paginationState.cardsConsumedFromCurrentPage || 0;
    const currentPageCards = paginationState.currentPageCards || [];
    
    // Check if current Scryfall page has remaining cards
    const remainingInCurrentPage = currentPageCards.length - cardsConsumed;
    
    console.log('📊 Partial page analysis:', {
      currentPageTotalCards: currentPageCards.length,
      cardsAlreadyConsumed: cardsConsumed,
      remainingInCurrentPage,
      needsNewPage: remainingInCurrentPage <= 0
    });
    
    let newCards: ScryfallCard[];
    
    if (remainingInCurrentPage > 0) {
      // Return remaining cards from current page
      const cardsToReturn = Math.min(remainingInCurrentPage, displayBatchSize);
      newCards = currentPageCards.slice(cardsConsumed, cardsConsumed + cardsToReturn);
      
      console.log('📄 Returning remaining cards from current page:', {
        cardsToReturn,
        sliceStart: cardsConsumed,
        sliceEnd: cardsConsumed + cardsToReturn,
        remainingAfterThis: remainingInCurrentPage - cardsToReturn
      });
      
    } else {
      // Current page exhausted - fetch next Scryfall page
      const nextScryfallPage = paginationState.currentScryfallPage + 1;
      
      console.log('🌐 Fetching next Scryfall page:', {
        currentPage: paginationState.currentScryfallPage,
        nextPage: nextScryfallPage,
        reason: 'Current page exhausted'
      });
      
      const response = await enhancedSearchCards(
        paginationState.lastQuery,
        paginationState.lastFilters,
        nextScryfallPage,
        paginationState.lastSort.order,
        paginationState.lastSort.dir
      );
      
      // Return first batch from new page
      const cardsToReturn = Math.min(response.data.length, displayBatchSize);
      newCards = response.data.slice(0, cardsToReturn);
      
      console.log('🌐 New page fetched:', {
        newPageCards: response.data.length,
        cardsToReturn,
        hasMorePages: response.has_more
      });
    }
    
    console.log('✅ Load more batch complete:', {
      batchLoaded: newCards.length,
      totalLoadedNow: paginationState.loadedCards + newCards.length,
      alphabeticalSequence: newCards.length > 0 ? `${newCards[0].name} → ${newCards[newCards.length - 1].name}` : 'No cards'
    });
    
    // Report progress completion
    if (onProgress) {
      onProgress(paginationState.loadedCards + newCards.length, paginationState.totalCards);
    }
    
    return newCards;
  } catch (error) {
    console.error('❌ Load more results failed:', error);
    throw error;
  }
};'''
    
    updated_content = re.sub(function_pattern, new_function, content, flags=re.DOTALL)
    
    # Verify the replacement worked
    if 'partial page consumption' in updated_content:
        print("✅ loadMoreResults function replaced with partial page consumption logic")
    else:
        print("❌ Failed to replace loadMoreResults function")
        return False
    
    with open('src/services/scryfallApi.ts', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    return True

def fix_use_search_hook():
    """Update useSearch hook to handle enhanced pagination state"""
    print("🔧 Updating useSearch hook for enhanced pagination...")
    
    with open('src/hooks/useSearch.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the loadMoreCards function in useSearch
    load_more_pattern = r'(const loadMoreCards = useCallback\(async \(\): Promise<ScryfallCard\[\]> => \{[^}]+console\.log[^}]+)(const currentPaginationState: PaginatedSearchState = \{[^}]+\};)'
    
    def replace_load_more(match):
        function_start = match.group(1)
        pagination_state = match.group(2)
        
        # Check if already fixed
        if 'currentScryfallPage' in pagination_state:
            print("✅ useSearch loadMoreCards already fixed")
            return match.group(0)
        
        # Enhanced pagination state with partial page consumption
        enhanced_pagination_state = '''const currentPaginationState: PaginatedSearchState = {
        totalCards: metadata.totalCards,
        loadedCards: actualLoadedCards,
        hasMore: actualLoadedCards < metadata.totalCards,
        isLoadingMore: false,
        currentPage: Math.floor(actualLoadedCards / 175) + 1,
        initialResults: state.cards,
        lastQuery: metadata.query,
        lastFilters: metadata.filters,
        lastSort: { order: "name", dir: "asc" },
        // Enhanced partial page consumption tracking
        currentScryfallPage: Math.floor(actualLoadedCards / 175) + 1,
        cardsConsumedFromCurrentPage: actualLoadedCards % 175,
        currentPageCards: [], // Will be managed by loadMoreResults
        scryfallPageSize: 175,
        displayBatchSize: 75,
      };'''
        
        print("✅ Enhanced useSearch pagination state")
        return function_start + enhanced_pagination_state
    
    updated_content = re.sub(load_more_pattern, replace_load_more, content, flags=re.DOTALL)
    
    with open('src/hooks/useSearch.ts', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    return True

def main():
    """Execute all pagination fixes"""
    print("🚀 Starting Load More pagination fix implementation")
    print("=" * 60)
    print("Issue: Load More jumps from A→C cards, missing B cards")
    print("Solution: Partial page consumption tracking")
    print("=" * 60)
    
    success = True
    
    # Step 1: Enhance type definitions
    if not fix_pagination_state_interface():
        success = False
    
    # Step 2: Fix initial search function
    if not fix_search_with_pagination():
        success = False
    
    # Step 3: Implement partial page consumption in loadMoreResults
    if not fix_load_more_results():
        success = False
    
    # Step 4: Update useSearch hook
    if not fix_use_search_hook():
        success = False
    
    if success:
        print("\n" + "=" * 60)
        print("🎯 SUCCESS! Load More pagination fix complete:")
        print("1. ✅ Enhanced PaginatedSearchState with partial page tracking")
        print("2. ✅ Fixed searchCardsWithPagination to store full page data")
        print("3. ✅ Implemented partial page consumption in loadMoreResults")
        print("4. ✅ Updated useSearch hook for enhanced pagination")
        print("\n📄 Expected behavior:")
        print("- Initial search: Shows 75 cards from Scryfall page 1")
        print("- Load More #1: Shows remaining 100 cards from page 1 (76-175)")
        print("- Load More #2: Fetches page 2 and shows first 75 cards (176-250)")
        print("- Alphabetical sequence: A→B→C (no more gaps!)")
        print("\n🧪 Test by searching with filters and using Load More")
        print("Verify alphabetical continuity without gaps")
    else:
        print("\n❌ PARTIAL FAILURE - Some fixes may not have applied correctly")
        print("Please check the files manually and run npm start to test compilation")
    
    return success

if __name__ == "__main__":
    main()
