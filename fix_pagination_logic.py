#!/usr/bin/env python3
"""
Fix Load More pagination logic in useSearch.ts
The issue is that loadMoreCards is reconstructing pagination state instead of using stored state
"""

import re

def fix_load_more_logic():
    """Fix the loadMoreCards function to use stored pagination state"""
    
    print("🔧 Fixing Load More pagination logic in useSearch.ts...")
    
    try:
        with open('src/hooks/useSearch.ts', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ useSearch.ts not found")
        return False
    
    # Find the loadMoreCards function and replace the problematic logic
    old_pattern = r'''// Load more cards for progressive loading
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
      const currentPaginationState: PaginatedSearchState = \{
        totalCards: metadata\.totalCards,
        loadedCards: metadata\.loadedCards,
        hasMore: metadata\.loadedCards < metadata\.totalCards,
        isLoadingMore: false,
        currentPage: Math\.floor\(metadata\.loadedCards / 75\) \+ 1,
        initialResults: state\.cards,
        lastQuery: metadata\.query,
        lastFilters: metadata\.filters,
        lastSort: \{ order: "name", dir: "asc" \},
      \};'''
    
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
      
      // Build proper pagination parameters for next page
      const nextPage = Math.floor(metadata.loadedCards / 75) + 1;
      console.log('📄 Requesting page:', {
        nextPage,
        currentLoadedCards: metadata.loadedCards,
        calculation: `Math.floor(${metadata.loadedCards} / 75) + 1 = ${nextPage}`
      });
      
      // Use searchCardsWithPagination directly with proper page parameter
      const { searchCardsWithPagination } = await import('../services/scryfallApi');
      const nextResults = await searchCardsWithPagination(
        metadata.query,
        metadata.filters,
        'name', // Sort order
        'asc',  // Sort direction
        nextPage // Pass the page number directly
      );
      
      console.log('✅ Next page API successful:', {
        newCardsCount: nextResults.initialResults.length,
        pageRequested: nextPage,
        totalAvailable: nextResults.totalCards
      });

      const newCards = nextResults.initialResults;'''
    
    if old_pattern in content:
        content = content.replace(old_pattern, new_implementation)
        print("✅ Fixed loadMoreCards pagination logic")
    else:
        print("⚠️ Could not find exact loadMoreCards pattern, trying alternative approach...")
        
        # Try to find and replace just the problematic currentPaginationState construction
        alt_pattern = r'''const currentPaginationState: PaginatedSearchState = \{
        totalCards: metadata\.totalCards,
        loadedCards: metadata\.loadedCards,
        hasMore: metadata\.loadedCards < metadata\.totalCards,
        isLoadingMore: false,
        currentPage: Math\.floor\(metadata\.loadedCards / 75\) \+ 1,
        initialResults: state\.cards,
        lastQuery: metadata\.query,
        lastFilters: metadata\.filters,
        lastSort: \{ order: "name", dir: "asc" \},
      \};

      const \{ loadMoreResults \} = await import\('\.\.\/services\/scryfallApi'\);
      const newCards = await loadMoreResults\(currentPaginationState\);'''
      
        alt_replacement = '''// Build proper pagination parameters for next page
      const nextPage = Math.floor(metadata.loadedCards / 75) + 1;
      console.log('📄 Requesting page:', {
        nextPage,
        currentLoadedCards: metadata.loadedCards,
        calculation: `Math.floor(${metadata.loadedCards} / 75) + 1 = ${nextPage}`
      });
      
      // Use searchCardsWithPagination directly with proper page parameter
      const { searchCardsWithPagination } = await import('../services/scryfallApi');
      const nextResults = await searchCardsWithPagination(
        metadata.query,
        metadata.filters,
        'name', // Sort order
        'asc',  // Sort direction
        nextPage // Pass the page number directly
      );
      
      console.log('✅ Next page API successful:', {
        newCardsCount: nextResults.initialResults.length,
        pageRequested: nextPage,
        totalAvailable: nextResults.totalCards
      });

      const newCards = nextResults.initialResults;'''
      
        if re.search(alt_pattern, content, re.DOTALL):
            content = re.sub(alt_pattern, alt_replacement, content, flags=re.DOTALL)
            print("✅ Fixed pagination logic using alternative pattern")
        else:
            print("❌ Could not find pagination state construction pattern")
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
    print("🚀 Fixing Load More pagination logic")
    print("=" * 50)
    
    if fix_load_more_logic():
        print("\n🎯 SUCCESS! Load More pagination logic fixed:")
        print("1. ✅ Removed problematic pagination state reconstruction")
        print("2. ✅ Using direct API call with proper page number")
        print("3. ✅ Added detailed logging for debugging")
        print("\nThe Load More should now request the correct next page")
        print("instead of jumping ahead in the alphabetical sequence.")
        print("\nTest by searching for cards and clicking Load More in Card view.")
        print("Check console logs to verify correct page calculation.")
    else:
        print("\n❌ MANUAL ACTION REQUIRED:")
        print("Could not automatically fix the pagination logic.")
        print("Please manually update the loadMoreCards function in src/hooks/useSearch.ts")
        print("to use direct API calls instead of reconstructing pagination state.")

if __name__ == "__main__":
    main()
