#!/usr/bin/env python3

import os
import sys

def fix_sorting_race_conditions():
    """Fix race conditions in smart sorting system that prevent UI updates"""
    
    filename = "src/hooks/useCards.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the searchWithPagination function to fix race conditions
    old_search_start = """  // Enhanced search with pagination support
  const searchWithPagination = useCallback(async (query: string, filters: SearchFilters = {}) => {
    const searchId = Date.now() + Math.random();
    (window as any).currentSearchId = searchId;

    console.log('🔍 PAGINATED SEARCH STARTED:', { 
      searchId: searchId.toFixed(3), 
      query, 
      filters,
      initialPageSize: 75
    });

    try {
      clearError();
      setLoading(true);
      resetPagination();

      // Rate limiting
      const now = Date.now();
      const lastSearch = (window as any).lastSearchTime || 0;
      const timeSinceLastSearch = now - lastSearch;
      
      if (timeSinceLastSearch < 150) {
        await new Promise(resolve => setTimeout(resolve, 150 - timeSinceLastSearch));
      }
      
      // Enhanced cancellation check - preserve sort-triggered searches
      const isSortTriggered = (window as any).lastSortChangeTime && 
                             (Date.now() - (window as any).lastSortChangeTime) < 5000;
      
      if ((window as any).currentSearchId !== searchId) {
        // Don't cancel sort-triggered searches
        if (isSortTriggered) {
          console.log('🎯 CONTINUING SORT-TRIGGERED SEARCH despite ID change:', searchId.toFixed(3));
        } else {
          console.log('🚫 PAGINATED SEARCH CANCELLED:', searchId.toFixed(3));
          return;
        }
      }
      
      (window as any).lastSearchTime = Date.now()"""

    new_search_start = """  // Enhanced search with pagination support - FIXED RACE CONDITIONS
  const searchWithPagination = useCallback(async (query: string, filters: SearchFilters = {}) => {
    const searchId = Date.now() + Math.random();
    const isSortTriggered = (window as any).lastSortChangeTime && 
                           (Date.now() - (window as any).lastSortChangeTime) < 3000; // Reduced window
    
    // CRITICAL FIX: Sort-triggered searches take priority
    if (isSortTriggered) {
      (window as any).currentSearchId = searchId;
      (window as any).prioritySearchId = searchId;
      console.log('🎯 PRIORITY SORT SEARCH STARTED:', searchId.toFixed(3));
    } else {
      // Only set as current if no priority search is running
      if (!(window as any).prioritySearchId || (Date.now() - (window as any).lastSortChangeTime) > 3000) {
        (window as any).currentSearchId = searchId;
      }
    }

    console.log('🔍 PAGINATED SEARCH STARTED:', { 
      searchId: searchId.toFixed(3), 
      query, 
      filters,
      isPriority: isSortTriggered,
      currentSearchId: (window as any).currentSearchId,
      prioritySearchId: (window as any).prioritySearchId
    });

    try {
      clearError();
      setLoading(true);
      resetPagination();

      // Rate limiting
      const now = Date.now();
      const lastSearch = (window as any).lastSearchTime || 0;
      const timeSinceLastSearch = now - lastSearch;
      
      if (timeSinceLastSearch < 150) {
        await new Promise(resolve => setTimeout(resolve, 150 - timeSinceLastSearch));
      }
      
      // SIMPLIFIED CANCELLATION: Only cancel if not current and not priority
      const isPrioritySearch = (window as any).prioritySearchId === searchId;
      const isCurrentSearch = (window as any).currentSearchId === searchId;
      
      if (!isPrioritySearch && !isCurrentSearch) {
        console.log('🚫 SEARCH CANCELLED - Not current/priority:', searchId.toFixed(3));
        return;
      }
      
      (window as any).lastSearchTime = Date.now()"""

    if old_search_start in content:
        content = content.replace(old_search_start, new_search_start)
        print("✅ Fixed search function start with race condition protection")
    else:
        print("❌ Could not find search function start")
        return False

    # Fix the state update section to ensure React detects changes
    old_state_update = """      // Update state with initial results
      console.log('🔄 Updating pagination state:', {
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
        selectedCards: new Set<string>(),
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
      
      // Force immediate re-render for sort changes
      if ((window as any).lastSortChangeTime && 
          (Date.now() - (window as any).lastSortChangeTime) < 2000) {
        console.log('🔄 FORCED STATE UPDATE for sort change:', {
          newCardCount: paginationResult.initialResults.length,
          firstCard: paginationResult.initialResults[0]?.name,
          lastCard: paginationResult.initialResults[paginationResult.initialResults.length - 1]?.name
        });
      }"""

    new_state_update = """      // CRITICAL FIX: Only update state if this search should win
      const shouldUpdateState = isPrioritySearch || 
                               (isCurrentSearch && !(window as any).prioritySearchId);
      
      if (!shouldUpdateState) {
        console.log('🚫 STATE UPDATE BLOCKED - Priority search in progress:', searchId.toFixed(3));
        return;
      }

      // Create new array reference to ensure React detects change
      const newCards = [...paginationResult.initialResults];
      const updateTimestamp = Date.now();
      
      console.log('🔄 UPDATING STATE WITH NEW CARDS:', {
        searchId: searchId.toFixed(3),
        cardsLength: newCards.length,
        firstCard: newCards[0]?.name || 'None',
        lastCard: newCards[newCards.length - 1]?.name || 'None',
        isPriority: isPrioritySearch,
        updateTimestamp
      });

      setState(prev => ({
        ...prev,
        cards: newCards, // New array reference
        searchQuery: query === '*' ? 'Filtered Results' : query,
        totalCards: paginationResult.totalCards,
        hasMore: paginationResult.hasMore,
        selectedCards: new Set<string>(),
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
      
      // Clear priority status after successful update
      if (isPrioritySearch) {
        setTimeout(() => {
          delete (window as any).prioritySearchId;
          console.log('🔄 PRIORITY SEARCH COMPLETED - Status cleared');
        }, 100);
      }
      
      // Force component re-render by updating a tracking value
      if (isSortTriggered) {
        (window as any).lastSuccessfulSortUpdate = updateTimestamp;
        console.log('🔄 SORT UPDATE COMPLETED:', {
          updateTimestamp,
          newCardCount: newCards.length,
          firstCard: newCards[0]?.name,
          lastCard: newCards[newCards.length - 1]?.name
        });
      }"""

    if old_state_update in content:
        content = content.replace(old_state_update, new_state_update)
        print("✅ Fixed state update with race condition protection and React change detection")
    else:
        print("❌ Could not find state update section")
        return False

    # Fix the post-API cancellation check
    old_post_api = """      // Enhanced post-API cancellation check for sort searches
      const isSortTriggeredPost = (window as any).lastSortChangeTime && 
                                 (Date.now() - (window as any).lastSortChangeTime) < 5000;
      
      if ((window as any).currentSearchId !== searchId) {
        // For sort-triggered searches, allow completion even with ID mismatch
        if (isSortTriggeredPost) {
          console.log('🎯 ALLOWING SORT-TRIGGERED SEARCH completion despite ID mismatch:', searchId.toFixed(3));
          // Continue with state update
        } else {
          console.log('🚫 PAGINATED SEARCH CANCELLED DURING API:', searchId.toFixed(3));
          return;
        }
      } else if (isSortTriggeredPost) {
        console.log('🎯 SORT-TRIGGERED SEARCH - ensuring completion');
      }"""

    new_post_api = """      // SIMPLIFIED POST-API CHECK: Only validate if this search should complete
      const stillShouldComplete = isPrioritySearch || 
                                 (isCurrentSearch && !(window as any).prioritySearchId);
      
      if (!stillShouldComplete) {
        console.log('🚫 SEARCH COMPLETION BLOCKED - Priority changed during API call:', searchId.toFixed(3));
        return;
      }
      
      console.log('✅ SEARCH READY TO COMPLETE:', {
        searchId: searchId.toFixed(3),
        isPriority: isPrioritySearch,
        isCurrent: isCurrentSearch
      });"""

    if old_post_api in content:
        content = content.replace(old_post_api, new_post_api)
        print("✅ Fixed post-API cancellation check")
    else:
        print("❌ Could not find post-API section")
        return False

    # Write the updated content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename} with race condition fixes")
    return True

if __name__ == "__main__":
    success = fix_sorting_race_conditions()
    sys.exit(0 if success else 1)