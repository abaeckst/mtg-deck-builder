#!/usr/bin/env python3

import os
import sys

def fix_popular_cards_pagination():
    """Fix loadPopularCards to show real total count and enable Load More button"""
    
    filename = "src/hooks/useCards.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the loadPopularCards function
    old_function = """  // Load popular/example cards
  const loadPopularCards = useCallback(async () => {
    clearError();
    setLoading(true);
    resetPagination();

    try {
      const response = await searchCards(POPULAR_CARDS_QUERY);
      
      // Limit to 75 cards for consistency
      const limitedCards = response.data.slice(0, 75);
      
      setState(prev => ({
        ...prev,
        cards: limitedCards,
        searchQuery: 'Popular Cards',
        totalCards: limitedCards.length,
        hasMore: false,
        selectedCards: new Set(),
        pagination: {
          totalCards: limitedCards.length,
          loadedCards: limitedCards.length,
          hasMore: false,
          isLoadingMore: false,
          currentPage: 1,
        },
      }));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to load popular cards';
      setState(prev => ({
        ...prev,
        error: errorMessage,
        cards: [],
        totalCards: 0,
        hasMore: false,
        pagination: {
          totalCards: 0,
          loadedCards: 0,
          hasMore: false,
          isLoadingMore: false,
          currentPage: 1,
        },
      }));
    } finally {
      setLoading(false);
    }
  }, [clearError, setLoading, resetPagination]);"""
    
    new_function = """  // Load popular/example cards with proper pagination
  const loadPopularCards = useCallback(async () => {
    console.log('🎯 Loading popular cards with pagination support...');
    
    // Use the same pagination system as searches
    await searchWithPagination(POPULAR_CARDS_QUERY, {});
    
    // Update the search query display
    setState(prev => ({
      ...prev,
      searchQuery: 'Popular Cards',
    }));
  }, [searchWithPagination]);"""
    
    if old_function in content:
        content = content.replace(old_function, new_function)
        print("✅ Fixed loadPopularCards to use proper pagination")
    else:
        print("❌ Could not find loadPopularCards function")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed popular cards pagination in {filename}")
    return True

if __name__ == "__main__":
    success = fix_popular_cards_pagination()
    sys.exit(0 if success else 1)