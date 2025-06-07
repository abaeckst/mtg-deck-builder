#!/usr/bin/env python3
"""
Fix Load More pagination logic in useSearch.ts - Corrected version
Work with existing API structure but fix the pagination state construction
"""

import re

def fix_load_more_logic():
    """Fix the loadMoreCards function to use proper pagination state"""
    
    print("🔧 Fixing Load More pagination logic in useSearch.ts (corrected)...")
    
    try:
        with open('src/hooks/useSearch.ts', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ useSearch.ts not found")
        return False
    
    # Find and replace the problematic pagination state construction
    old_pattern = r'''// Build proper pagination parameters for next page
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
    
    new_implementation = '''// Use the existing loadMoreResults API with corrected pagination state
      console.log('📄 Building pagination state for Load More:', {
        currentLoadedCards: metadata.loadedCards,
        totalCards: metadata.totalCards,
        currentCards: state.cards.length
      });
      
      // Build corrected pagination state - key fix: use actual loaded cards count
      const currentPaginationState: PaginatedSearchState = {
        totalCards: metadata.totalCards,
        loadedCards: state.cards.length, // ✅ Use actual current cards length
        hasMore: state.cards.length < metadata.totalCards,
        isLoadingMore: false,
        currentPage: Math.floor(state.cards.length / 75) + 1, // ✅ Calculate from actual cards
        initialResults: state.cards,
        lastQuery: metadata.query,
        lastFilters: metadata.filters,
        lastSort: { order: "name", dir: "asc" },
      };
      
      console.log('📄 Pagination state built:', {
        loadedCards: currentPaginationState.loadedCards,
        currentPage: currentPaginationState.currentPage,
        hasMore: currentPaginationState.hasMore
      });

      const { loadMoreResults } = await import('../services/scryfallApi');
      const newCards = await loadMoreResults(currentPaginationState);'''
    
    if old_pattern in content:
        content = content.replace(old_pattern, new_implementation, 1)
        print("✅ Fixed loadMoreCards pagination logic")
    else:
        print("⚠️ Trying alternative pattern match...")
        
        # Try to find the simpler pattern that might exist
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
      \};'''
      
        alt_replacement = '''const currentPaginationState: PaginatedSearchState = {
        totalCards: metadata.totalCards,
        loadedCards: state.cards.length, // ✅ Use actual current cards length
        hasMore: state.cards.length < metadata.totalCards,
        isLoadingMore: false,
        currentPage: Math.floor(state.cards.length / 75) + 1, // ✅ Calculate from actual cards
        initialResults: state.cards,
        lastQuery: metadata.query,
        lastFilters: metadata.filters,
        lastSort: { order: "name", dir: "asc" },
      };
      
      console.log('📄 Load More pagination state:', {
        actualCardsLength: state.cards.length,
        metadataLoadedCards: metadata.loadedCards,
        calculatedPage: Math.floor(state.cards.length / 75) + 1,
        hasMore: state.cards.length < metadata.totalCards
      });'''
      
        if re.search(alt_pattern, content, re.DOTALL):
            content = re.sub(alt_pattern, alt_replacement, content, flags=re.DOTALL)
            print("✅ Fixed pagination state construction")
        else:
            print("❌ Could not find pagination state pattern")
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
    print("🚀 Fixing Load More pagination logic (corrected)")
    print("=" * 50)
    
    if fix_load_more_logic():
        print("\n🎯 SUCCESS! Load More pagination logic fixed:")
        print("1. ✅ Using state.cards.length instead of metadata.loadedCards")
        print("2. ✅ Calculating page from actual cards count")
        print("3. ✅ Added detailed logging for debugging")
        print("4. ✅ Working with existing loadMoreResults API")
        print("\nThe key fix: metadata.loadedCards was out of sync with actual cards.")
        print("Now using state.cards.length for accurate pagination calculation.")
        print("\nTest by searching for cards and clicking Load More in Card view.")
        print("Should now continue alphabetically (A → B → C) without jumping.")
    else:
        print("\n❌ MANUAL ACTION REQUIRED:")
        print("Could not automatically fix the pagination logic.")
        print("Please manually update the currentPaginationState construction")
        print("to use state.cards.length instead of metadata.loadedCards.")

if __name__ == "__main__":
    main()
