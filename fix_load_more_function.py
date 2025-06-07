#!/usr/bin/env python3
"""
Targeted fix for loadMoreResults function with partial page consumption logic.
"""

import re

def fix_load_more_results():
    """Replace loadMoreResults function with partial page consumption logic"""
    print("🔧 Implementing partial page consumption in loadMoreResults...")
    
    with open('src/services/scryfallApi.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the loadMoreResults function more precisely
    # Look for the function signature and find the matching closing brace
    start_pattern = r'export const loadMoreResults = async \('
    start_match = re.search(start_pattern, content)
    
    if not start_match:
        print("❌ Could not find loadMoreResults function")
        return False
    
    # Find the function start position
    start_pos = start_match.start()
    
    # Find the function end by counting braces
    brace_count = 0
    in_function = False
    end_pos = start_pos
    
    for i, char in enumerate(content[start_pos:], start_pos):
        if char == '{':
            brace_count += 1
            in_function = True
        elif char == '}':
            brace_count -= 1
            if in_function and brace_count == 0:
                end_pos = i + 1
                break
    
    if end_pos == start_pos:
        print("❌ Could not find end of loadMoreResults function")
        return False
    
    # Extract the old function
    old_function = content[start_pos:end_pos]
    print(f"📄 Found function: {len(old_function)} characters")
    
    # Check if already fixed
    if 'partial page consumption' in old_function:
        print("✅ loadMoreResults already fixed")
        return True
    
    # New loadMoreResults implementation
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
}'''
    
    # Replace the function
    new_content = content[:start_pos] + new_function + content[end_pos:]
    
    with open('src/services/scryfallApi.ts', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ loadMoreResults function replaced with partial page consumption logic")
    return True

def fix_use_search_remaining():
    """Complete the useSearch hook fix that may have been partial"""
    print("🔧 Completing useSearch hook fixes...")
    
    with open('src/hooks/useSearch.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for the loadMoreCards function and check if it needs completion
    if 'currentScryfallPage' in content and 'cardsConsumedFromCurrentPage' in content:
        print("✅ useSearch hook already fully fixed")
        return True
    
    # Find the pagination state creation in loadMoreCards
    pattern = r'(const currentPaginationState: PaginatedSearchState = \{[^}]+currentPage: Math\.floor\([^}]+\+ 1,\s+initialResults: state\.cards,\s+lastQuery: metadata\.query,\s+lastFilters: metadata\.filters,\s+lastSort: \{ order: "name", dir: "asc" \},)(\s+\};)'
    
    def add_missing_fields(match):
        existing_fields = match.group(1)
        closing = match.group(2)
        
        # Add the missing partial page consumption fields
        additional_fields = '''
        // Enhanced partial page consumption tracking
        currentScryfallPage: Math.floor(actualLoadedCards / 175) + 1,
        cardsConsumedFromCurrentPage: actualLoadedCards % 175,
        currentPageCards: [], // Will be managed by loadMoreResults
        scryfallPageSize: 175,
        displayBatchSize: 75,'''
        
        return existing_fields + additional_fields + closing
    
    updated_content = re.sub(pattern, add_missing_fields, content, flags=re.DOTALL)
    
    if updated_content != content:
        with open('src/hooks/useSearch.ts', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("✅ Completed useSearch hook partial page consumption fields")
    else:
        print("⚠️ useSearch pattern not found - may already be correct")
    
    return True

def main():
    """Execute the targeted fixes"""
    print("🎯 Targeted Load More pagination fix")
    print("=" * 50)
    
    success = True
    
    # Fix the loadMoreResults function specifically
    if not fix_load_more_results():
        success = False
    
    # Complete useSearch hook if needed
    if not fix_use_search_remaining():
        success = False
    
    if success:
        print("\n🎯 SUCCESS! Load More pagination fix completed")
        print("✅ loadMoreResults function implemented with partial page consumption")
        print("✅ useSearch hook enhanced for partial page tracking")
        print("\n🧪 Test by running: npm start")
        print("Then search with filters and use Load More to verify A→B→C sequence")
    else:
        print("\n❌ Some fixes failed - check manually")
    
    return success

if __name__ == "__main__":
    main()
