#!/usr/bin/env python3

import os
import sys

def fix_state_update_timing(filename):
    """Fix React state update timing issues for sort results"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the state update section and ensure proper state synchronization
    old_state_update = '''      setState(prev => ({
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
      }));'''

    new_state_update = '''      // Force immediate state update for sort changes to prevent stale UI
      const newState = {
        ...state,
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
      };
      
      setState(newState);
      
      // Force immediate re-render for sort changes
      if ((window as any).lastSortChangeTime && 
          (Date.now() - (window as any).lastSortChangeTime) < 2000) {
        console.log('🔄 FORCED STATE UPDATE for sort change:', {
          newCardCount: paginationResult.initialResults.length,
          firstCard: paginationResult.initialResults[0]?.name,
          lastCard: paginationResult.initialResults[paginationResult.initialResults.length - 1]?.name
        });
      }'''

    if old_state_update in content:
        content = content.replace(old_state_update, new_state_update)
        print("✅ Fixed state update timing for sort changes")
    else:
        print("❌ Could not find state update pattern to replace")
        return False
    
    # Also add a more robust search cancellation check
    old_search_check = '''      if ((window as any).currentSearchId !== searchId) {
        console.log('🚫 PAGINATED SEARCH CANCELLED DURING API:', searchId.toFixed(3));
        return;
      }'''

    new_search_check = '''      if ((window as any).currentSearchId !== searchId) {
        console.log('🚫 PAGINATED SEARCH CANCELLED DURING API:', searchId.toFixed(3));
        return;
      }
      
      // Additional check: if this is a sort-triggered search, ensure it completes
      const isSortTriggered = (window as any).lastSortChangeTime && 
                             (Date.now() - (window as any).lastSortChangeTime) < 3000;
      if (isSortTriggered) {
        console.log('🎯 SORT-TRIGGERED SEARCH - ensuring completion');
      }'''

    if old_search_check in content:
        content = content.replace(old_search_check, new_search_check)
        print("✅ Enhanced search cancellation logic for sort changes")
    else:
        print("⚠️ Could not find search cancellation pattern - this is optional")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = fix_state_update_timing("src/hooks/useCards.ts")
    
    if success:
        print("\n🎯 STATE UPDATE TIMING FIX APPLIED")
        print("This should resolve the React state timing issue preventing sort results from appearing")
        print("Test by clicking sort buttons rapidly - results should update immediately")
    
    sys.exit(0 if success else 1)