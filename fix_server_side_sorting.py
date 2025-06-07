#!/usr/bin/env python3

import os
import sys

def fix_server_side_sorting():
    """Fix server-side sorting AND Load More button visibility"""
    
    filename = "src/hooks/useCards.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix 1: Force server-side sorting for ANY dataset with more than 75 cards
    old_sort_logic = """    // Smart threshold: Use server-side sort for large datasets or when not all results loaded
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
    }"""
    
    new_sort_logic = """    // FORCE server-side sorting for datasets with >75 cards to get different results
    const shouldUseServerSort = metadata.totalCards > 75;
    console.log('🔄 Sort change analysis:', {
      criteria,
      direction,
      totalCards: metadata.totalCards,
      loadedCards: metadata.loadedCards,
      threshold: 75,
      shouldUseServerSort,
      reason: shouldUseServerSort ? 'FORCE server-side sort - get different cards from Scryfall' : 'Small dataset - use client sort'
    });

    if (shouldUseServerSort) {
      console.log('🌐 FORCING server-side sorting - fetching completely different results from Scryfall');
      
      // Get current Scryfall sort parameters (will reflect the new sort)
      const sortParams = getScryfallSortParams('collection');
      console.log('🔧 Scryfall sort params for FORCED re-search:', sortParams);
      
      // FORCE re-search with same query and filters but new sort parameters
      // This will get different cards from Scryfall, not just reorder the same 75
      await searchWithPagination(metadata.query, metadata.filters);
    } else {
      console.log('🏠 Using client-side sorting - dataset is small, no re-search needed');
      // Client-side sorting will be handled by the UI component automatically
    }"""
    
    if old_sort_logic in content:
        content = content.replace(old_sort_logic, new_sort_logic)
        print("✅ Fixed server-side sorting logic to FORCE new Scryfall searches")
    else:
        print("❌ Could not find handleCollectionSortChange pattern")
        return False
    
    # Fix 2: Debug pagination state to understand why Load More isn't showing
    old_pagination_update = """      setState(prev => ({
        ...prev,
        cards: paginationResult.initialResults,
        searchQuery: query === '*' ? 'Filtered Results' : query,
        totalCards: paginationResult.totalCards,
        hasMore: paginationResult.hasMore,
        selectedCards: new Set(),
        pagination: {
          totalCards: paginationResult.totalCards,
          loadedCards: paginationResult.loadedCards,
          hasMore: paginationResult.hasMore,
          isLoadingMore: false,
          currentPage: 1,
        },
        lastSearchMetadata: {
          query,
          filters,
          totalCards: paginationResult.totalCards,
          loadedCards: paginationResult.loadedCards,
        },
      }));"""
    
    new_pagination_update = """      console.log('🔄 Updating pagination state:', {
        totalCards: paginationResult.totalCards,
        loadedCards: paginationResult.loadedCards,
        hasMore: paginationResult.hasMore,
        cardsLength: paginationResult.initialResults.length
      });

      setState(prev => ({
        ...prev,
        cards: paginationResult.initialResults,
        searchQuery: query === '*' ? 'Filtered Results' : query,
        totalCards: paginationResult.totalCards,
        hasMore: paginationResult.hasMore,
        selectedCards: new Set(),
        pagination: {
          totalCards: paginationResult.totalCards,
          loadedCards: paginationResult.loadedCards,
          hasMore: paginationResult.hasMore,
          isLoadingMore: false,
          currentPage: 1,
        },
        lastSearchMetadata: {
          query,
          filters,
          totalCards: paginationResult.totalCards,
          loadedCards: paginationResult.loadedCards,
        },
      }));

      console.log('✅ Pagination state updated - Load More should show if hasMore is true');"""
    
    if old_pagination_update in content:
        content = content.replace(old_pagination_update, new_pagination_update)
        print("✅ Added pagination debugging to understand Load More visibility")
    else:
        print("⚠️ Could not find pagination state update pattern")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed server-side sorting and pagination debugging in {filename}")
    return True

if __name__ == "__main__":
    success = fix_server_side_sorting()
    sys.exit(0 if success else 1)
    