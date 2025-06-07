#!/usr/bin/env python3
"""
Fix Load More function in useSearch.ts
Fix both the API call error and the pagination calculation
"""

import re

def fix_load_more_function():
    """Fix the loadMoreCards function in useSearch.ts"""
    
    print("🔧 Fixing loadMoreCards function...")
    
    try:
        with open('src/hooks/useSearch.ts', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ useSearch.ts not found")
        return False
    
    # Find and replace the problematic loadMoreCards implementation
    old_implementation = r'''// Load more cards for progressive loading
  const loadMoreCards = useCallback\(async \(\): Promise<ScryfallCard\[\]> => \{
    console\.log\('🔄 useSearch\.loadMoreCards called'\);
    
    const metadata = state\.lastSearchMetadata;
    if \(!metadata\) \{
      console\.log\('❌ No search metadata available for load more'\);
      throw new Error\('No search metadata available'\);
    \}

    try \{
      console\.log\('📡 Loading more cards via API\.\.\.'\);
      
      // Use the existing pagination state to load more
      // Build proper pagination parameters for next page
      const nextPage = Math\.floor\(metadata\.loadedCards / 75\) \+ 1;
      console\.log\('📄 Requesting page:', \{
        nextPage,
        currentLoadedCards: metadata\.loadedCards,
        calculation: `Math\.floor\(\$\{metadata\.loadedCards\} / 75\) \+ 1 = \$\{nextPage\}`
      \}\);
      
      // Use searchCardsWithPagination directly with proper page parameter
      const \{ searchCardsWithPagination \} = await import\('\.\.\/services\/scryfallApi'\);
      const nextResults = await searchCardsWithPagination\(
        metadata\.query,
        metadata\.filters,
        'name', // Sort order
        'asc',  // Sort direction
        nextPage // Pass the page number directly
      \);
      
      console\.log\('✅ Next page API successful:', \{
        newCardsCount: nextResults\.initialResults\.length,
        pageRequested: nextPage,
        totalAvailable: nextResults\.totalCards
      \}\);

      const newCards = nextResults\.initialResults;'''
    
    new_implementation = '''// Load more cards for progressive loading
  const loadMoreCards = useCallback(async (): Promise<ScryfallCard[]> => {
    console.log('🔄 useSearch.loadMoreCards called');
    
    const metadata = state.lastSearchMetadata;
    if (!metadata) {
      console.log('❌ No search metadata available for load more');
      throw new Error('No search metadata available');
    }

    try {
      console.log('📡 Loading more cards via API...');
      
      // ✅ FIXED: Use actual current cards count instead of metadata
      const actualLoadedCards = state.cards.length;
      console.log('📄 Pagination calculation:', {
        actualLoadedCards,
        metadataLoadedCards: metadata.loadedCards,
        totalCards: metadata.totalCards,
        nextPage: Math.floor(actualLoadedCards / 75) + 1
      });
      
      // ✅ FIXED: Build corrected pagination state for loadMoreResults API
      const currentPaginationState: PaginatedSearchState = {
        totalCards: metadata.totalCards,
        loadedCards: actualLoadedCards, // ✅ Use actual current cards count
        hasMore: actualLoadedCards < metadata.totalCards,
        isLoadingMore: false,
        currentPage: Math.floor(actualLoadedCards / 75) + 1, // ✅ Calculate from actual cards
        initialResults: state.cards,
        lastQuery: metadata.query,
        lastFilters: metadata.filters,
        lastSort: { order: "name", dir: "asc" },
      };
      
      console.log('📄 Using pagination state:', {
        loadedCards: currentPaginationState.loadedCards,
        currentPage: currentPaginationState.currentPage,
        hasMore: currentPaginationState.hasMore
      });

      // ✅ FIXED: Use loadMoreResults API instead of searchCardsWithPagination
      const { loadMoreResults } = await import('../services/scryfallApi');
      const newCards = await loadMoreResults(currentPaginationState);'''
    
    # Apply the fix
    if re.search(old_implementation, content, re.DOTALL):
        content = re.sub(old_implementation, new_implementation, content, flags=re.DOTALL)
        print("✅ Fixed loadMoreCards function")
    else:
        print("❌ Could not find loadMoreCards function pattern")
        return False
    
    # Write the fixed content back
    try:
        with open('src/hooks/useSearch.ts', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ useSearch.ts updated successfully")
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

def main():
    """Main execution"""
    print("🚀 Fixing Load More function")
    print("=" * 40)
    
    if fix_load_more_function():
        print("\n🎯 SUCCESS! Load More function fixed:")
        print("1. ✅ Using state.cards.length instead of metadata.loadedCards")
        print("2. ✅ Using loadMoreResults API instead of searchCardsWithPagination")
        print("3. ✅ Fixed TypeScript compilation error (5 vs 4 parameters)")
        print("4. ✅ Added detailed logging for debugging pagination calculation")
        print("\nKey fixes:")
        print("- metadata.loadedCards → state.cards.length (accurate count)")
        print("- searchCardsWithPagination() → loadMoreResults() (correct API)")
        print("- Proper pagination state construction")
        print("\nTest: Search for cards and click Load More in Card view.")
        print("Should now continue alphabetically A → B → C without jumping.")
    else:
        print("\n❌ Fix failed - manual action required")

if __name__ == "__main__":
    main()
