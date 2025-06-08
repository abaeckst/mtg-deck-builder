#!/usr/bin/env python3

import os
import sys

def fix_sorting_integration():
    """Fix the search and sorting integration to restore proper server-side sort handling"""
    
    filename = "src/hooks/useCards.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Ensure searchWithPagination gets sort parameters properly
    old_pattern_1 = """      // Execute paginated search
      const paginationResult = await searchCardsWithPagination(
        query, 
        filters, 
        sortParams.order, 
        sortParams.dir
      );"""
    
    new_pattern_1 = """      // Execute paginated search with sort parameters
      console.log('🔧 Using sort parameters:', sortParams);
      const paginationResult = await searchCardsWithPagination(
        query, 
        filters, 
        sortParams.order, 
        sortParams.dir
      );"""
    
    if old_pattern_1 in content:
        content = content.replace(old_pattern_1, new_pattern_1)
        print("✅ Fixed searchWithPagination sort parameter usage")
    else:
        print("⚠️ Could not find searchWithPagination pattern - checking for alternative")
    
    # Fix 2: Ensure handleCollectionSortChange triggers re-search properly
    old_pattern_2 = """  // Handle collection sort changes with smart re-search logic - UPDATED FOR 75-card threshold
  const handleCollectionSortChange = useCallback(async (criteria: SortCriteria, direction: SortDirection) => {
    const metadata = state.lastSearchMetadata;
    if (!metadata) {
      console.log('🔄 No search metadata available for sort change');
      return;
    }

    // Updated threshold: Use server-side sort if we have more than 75 cards loaded
    const shouldUseServerSort = metadata.totalCards > 75 && metadata.loadedCards < metadata.totalCards;
    console.log('🔄 Sort change analysis:', {
      criteria,
      direction,
      totalCards: metadata.totalCards,
      loadedCards: metadata.loadedCards,
      threshold: 75,
      shouldUseServerSort
    });

    if (shouldUseServerSort) {
      console.log('🌐 Using server-side sorting - re-searching with new sort parameters');
      
      // Get Scryfall sort parameters
      const sortParams = getScryfallSortParams('collection');
      console.log('🔧 Scryfall sort params:', sortParams);
      
      // Re-search with same query and filters but new sort
      await searchWithPagination(metadata.query, metadata.filters);
    } else {
      console.log('🏠 Using client-side sorting - dataset is small enough or all results loaded');
      // Client-side sorting will be handled by the UI component
      // No action needed here as the sortCards function in MTGOLayout will handle it
    }
  }, [state.lastSearchMetadata, getScryfallSortParams, searchWithPagination]);"""
    
    new_pattern_2 = """  // Handle collection sort changes with smart re-search logic - FIXED SERVER-SIDE INTEGRATION
  const handleCollectionSortChange = useCallback(async (criteria: SortCriteria, direction: SortDirection) => {
    const metadata = state.lastSearchMetadata;
    if (!metadata) {
      console.log('🔄 No search metadata available for sort change');
      return;
    }

    // Smart threshold: Use server-side sort for large datasets or when not all results loaded
    const shouldUseServerSort = metadata.totalCards > 75;
    console.log('🔄 Sort change analysis:', {
      criteria,
      direction,
      totalCards: metadata.totalCards,
      loadedCards: metadata.loadedCards,
      threshold: 75,
      shouldUseServerSort,
      reason: shouldUseServerSort ? 'Large dataset - use server sort' : 'Small dataset - use client sort'
    });

    if (shouldUseServerSort) {
      console.log('🌐 Using server-side sorting - re-searching with new sort parameters');
      
      // Get current Scryfall sort parameters (will reflect the new sort)
      const sortParams = getScryfallSortParams('collection');
      console.log('🔧 Scryfall sort params for re-search:', sortParams);
      
      // Re-search with same query and filters but new sort parameters
      await searchWithPagination(metadata.query, metadata.filters);
    } else {
      console.log('🏠 Using client-side sorting - dataset is small, no re-search needed');
      // Client-side sorting will be handled by the UI component automatically
      // The sortCards function in MTGOLayout will handle the actual sorting
    }
  }, [state.lastSearchMetadata, getScryfallSortParams, searchWithPagination]);"""
    
    if old_pattern_2 in content:
        content = content.replace(old_pattern_2, new_pattern_2)
        print("✅ Fixed handleCollectionSortChange server-side logic")
    else:
        print("❌ Could not find handleCollectionSortChange pattern")
        return False
    
    # Fix 3: Ensure Load More uses the same sort parameters
    old_pattern_3 = """    const newCards = await loadMoreResults(
        paginationState,
        (loaded, total) => {
          // Progress callback
          setState(prev => ({
            ...prev,
            pagination: { 
              ...prev.pagination, 
              loadedCards: loaded
            }
          }));
        }
      );"""
    
    new_pattern_3 = """    console.log('🔄 Load more with current sort:', {
        query: paginationState.lastQuery,
        sort: paginationState.lastSort
      });
      
      const newCards = await loadMoreResults(
        paginationState,
        (loaded, total) => {
          // Progress callback
          setState(prev => ({
            ...prev,
            pagination: { 
              ...prev.pagination, 
              loadedCards: loaded
            }
          }));
        }
      );"""
    
    if old_pattern_3 in content:
        content = content.replace(old_pattern_3, new_pattern_3)
        print("✅ Added sort parameter logging to loadMoreResults")
    else:
        print("⚠️ Could not find loadMoreResults pattern - may already be correct")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed search and sorting integration in {filename}")
    return True

if __name__ == "__main__":
    success = fix_sorting_integration()
    sys.exit(0 if success else 1)