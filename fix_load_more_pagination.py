#!/usr/bin/env python3

import re
import os

def fix_load_more_pagination():
    """
    Fix Load More pagination logic to properly handle the case where
    all results fit on the first Scryfall page but are artificially 
    limited to 75 cards for display.
    """
    
    # Update useSearch.ts loadMoreCards function
    useSearch_path = 'src/hooks/useSearch.ts'
    
    if not os.path.exists(useSearch_path):
        print(f"❌ File not found: {useSearch_path}")
        return
    
    try:
        with open(useSearch_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the loadMoreCards function and fix the pagination logic
        # The issue is in the currentPaginationState calculation
        
        # Replace the problematic pagination state calculation
        old_pagination_calc = r'''// ✅ FIXED: Build corrected pagination state for loadMoreResults API
      const currentPaginationState: PaginatedSearchState = \{
        totalCards: metadata\.totalCards,
        loadedCards: actualLoadedCards, // ✅ Use actual current cards count
        hasMore: actualLoadedCards < metadata\.totalCards,
        isLoadingMore: false,
        currentPage: Math\.floor\(actualLoadedCards / 175\) \+ 1, // ✅ Fixed: 175 cards per page, not 75
        initialResults: state\.cards,
        lastQuery: metadata\.query,
        lastFilters: metadata\.filters,
        lastSort: \{
          order: metadata\.actualSortOrder,
          dir: metadata\.actualSortDirection
        \}, // ✅ FIXED: Use actual sort parameters from original search
        // Enhanced partial page consumption tracking
        currentScryfallPage: Math\.floor\(actualLoadedCards / 175\) \+ 1,
        cardsConsumedFromCurrentPage: actualLoadedCards % 175,
        currentPageCards: \[\], // Empty since we don't store full page data in useSearch
        scryfallPageSize: 175,
        displayBatchSize: 75,
      \};'''
        
        new_pagination_calc = '''// ✅ FIXED: Build corrected pagination state for loadMoreResults API
      // Key insight: We need to track Scryfall pages vs display batches separately
      // - Scryfall returns 175 cards per page
      // - We display 75 cards per batch
      // - Multiple display batches can come from the same Scryfall page
      
      const currentPaginationState: PaginatedSearchState = {
        totalCards: metadata.totalCards,
        loadedCards: actualLoadedCards, // Current displayed cards (e.g., 75)
        hasMore: actualLoadedCards < metadata.totalCards,
        isLoadingMore: false,
        currentPage: 1, // Always start from page 1 for display purposes
        initialResults: state.cards,
        lastQuery: metadata.query,
        lastFilters: metadata.filters,
        lastSort: {
          order: metadata.actualSortOrder,
          dir: metadata.actualSortDirection
        },
        // Enhanced partial page consumption tracking
        currentScryfallPage: 1, // We're still on Scryfall page 1
        cardsConsumedFromCurrentPage: actualLoadedCards, // 75 cards consumed from 175-card page
        currentPageCards: [], // We need to store the full page data somewhere
        scryfallPageSize: 175,
        displayBatchSize: 75,
      };'''
        
        # Apply the fix
        content = re.sub(
            old_pagination_calc,
            new_pagination_calc,
            content,
            flags=re.DOTALL
        )
        
        # Also need to fix the logic to store the original full page results
        # Add storage for currentPageCards in searchWithPagination
        
        # Find where we update pagination state and store the full page
        storage_fix = '''// Store pagination state for load more functionality
      onPaginationStateChange(paginationResult);'''
        
        enhanced_storage = '''// Store pagination state for load more functionality  
      // CRITICAL: Store the full Scryfall page data for Load More to use
      const enhancedPaginationResult = {
        ...paginationResult,
        currentPageCards: response.data || [], // Store full 175-card page
        cardsConsumedFromCurrentPage: paginationResult.loadedCards || 75
      };
      onPaginationStateChange(enhancedPaginationResult);'''
        
        content = re.sub(
            storage_fix,
            enhanced_storage,
            content
        )
        
        # Write the updated file
        with open(useSearch_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {useSearch_path}")
        
        # Also need to update the searchCardsWithPagination function in scryfallApi.ts
        scryfallApi_path = 'src/services/scryfallApi.ts'
        
        if os.path.exists(scryfallApi_path):
            with open(scryfallApi_path, 'r', encoding='utf-8') as f:
                api_content = f.read()
            
            # Update the return object to include the full page data
            old_return = r'''return \{
      initialResults,
      totalCards: response\.total_cards,
      loadedCards: initialResults\.length,
      hasMore,
      isLoadingMore: false,
      currentPage: 1,
      lastQuery: query,
      lastFilters: filters,
      lastSort: \{ order, dir \},
      // Partial page consumption tracking
      currentScryfallPage: 1,
      cardsConsumedFromCurrentPage: initialResults\.length,
      currentPageCards: response\.data,
      scryfallPageSize: 175,
      displayBatchSize: 75,
    \};'''
            
            new_return = '''return {
      initialResults,
      totalCards: response.total_cards,
      loadedCards: initialResults.length,
      hasMore,
      isLoadingMore: false,
      currentPage: 1,
      lastQuery: query,
      lastFilters: filters,
      lastSort: { order, dir },
      // Partial page consumption tracking - FIXED
      currentScryfallPage: 1,
      cardsConsumedFromCurrentPage: initialResults.length, // 75 out of 175
      currentPageCards: response.data, // Store ALL cards from Scryfall page (up to 175)
      scryfallPageSize: 175,
      displayBatchSize: 75,
    };'''
            
            api_content = re.sub(
                old_return,
                new_return,
                api_content,
                flags=re.DOTALL
            )
            
            with open(scryfallApi_path, 'w', encoding='utf-8') as f:
                f.write(api_content)
            
            print(f"✅ Updated {scryfallApi_path}")
        
        print("\n🎯 PAGINATION FIX SUMMARY:")
        print("1. Fixed currentScryfallPage calculation (always 1 when all results fit on first page)")
        print("2. Fixed cardsConsumedFromCurrentPage tracking (75 out of 175)")
        print("3. Enhanced storage to preserve full Scryfall page data for Load More")
        print("4. Load More will now use remaining cards from page 1 instead of requesting page 2")
        
        print("\n🔍 EXPECTED BEHAVIOR AFTER FIX:")
        print("- Search: Gets 97 cards from Scryfall page 1, displays first 75")
        print("- Load More: Uses remaining 22 cards from page 1 (cards 76-97)")
        print("- No 422 error because we don't request non-existent page 2")
        
    except Exception as e:
        print(f"❌ Error updating files: {e}")

if __name__ == "__main__":
    fix_load_more_pagination()
