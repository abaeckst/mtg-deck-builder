#!/usr/bin/env python3

import os
import sys

def fix_search_cancellation(filename):
    """Fix search cancellation issues preventing sort results from updating UI"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and fix the search cancellation logic to preserve sort-triggered searches
    old_cancellation_check = '''    if ((window as any).currentSearchId !== searchId) {
      console.log('🚫 PAGINATED SEARCH CANCELLED:', searchId.toFixed(3));
      return;
    }'''

    new_cancellation_check = '''    // Enhanced cancellation check - preserve sort-triggered searches
    const isSortTriggered = (window as any).lastSortChangeTime && 
                           (Date.now() - (window as any).lastSortChangeTime) < 5000;
    
    if ((window as any).currentSearchId !== searchId) {
      // Don't cancel sort-triggered searches that are close to completion
      if (isSortTriggered && response) {
        console.log('🎯 PRESERVING SORT-TRIGGERED SEARCH despite ID mismatch:', searchId.toFixed(3));
        // Continue with the search result processing
      } else {
        console.log('🚫 PAGINATED SEARCH CANCELLED:', searchId.toFixed(3));
        return;
      }
    }'''

    if old_cancellation_check in content:
        content = content.replace(old_cancellation_check, new_cancellation_check)
        print("✅ Enhanced search cancellation logic to preserve sort results")
    else:
        print("❌ Could not find cancellation check pattern")
        return False
    
    # Also enhance the earlier cancellation check
    old_early_check = '''      if ((window as any).currentSearchId !== searchId) {
        console.log('🚫 PAGINATED SEARCH CANCELLED DURING API:', searchId.toFixed(3));
        return;
      }
      
      // Additional check: if this is a sort-triggered search, ensure it completes
      const isSortTriggered = (window as any).lastSortChangeTime && 
                             (Date.now() - (window as any).lastSortChangeTime) < 3000;
      if (isSortTriggered) {
        console.log('🎯 SORT-TRIGGERED SEARCH - ensuring completion');
      }'''

    new_early_check = '''      // Enhanced cancellation check for sort-triggered searches
      const isSortTriggered = (window as any).lastSortChangeTime && 
                             (Date.now() - (window as any).lastSortChangeTime) < 5000;
      
      if ((window as any).currentSearchId !== searchId) {
        // For sort-triggered searches, be more lenient about cancellation
        if (isSortTriggered) {
          console.log('🎯 CONTINUING SORT-TRIGGERED SEARCH despite ID change:', searchId.toFixed(3));
          // Continue processing - don't cancel sort searches
        } else {
          console.log('🚫 PAGINATED SEARCH CANCELLED DURING API:', searchId.toFixed(3));
          return;
        }
      } else if (isSortTriggered) {
        console.log('🎯 SORT-TRIGGERED SEARCH - ensuring completion');
      }'''

    if old_early_check in content:
        content = content.replace(old_early_check, new_early_check)
        print("✅ Enhanced early cancellation logic for sort searches")
    else:
        print("⚠️ Could not find early cancellation pattern - this is optional")
    
    # Also ensure the state update happens regardless of timing
    old_state_section = '''      setState(prev => ({
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
      }'''

    new_state_section = '''      // Force immediate state update for sort changes
      const isSortTriggered = (window as any).lastSortChangeTime && 
                             (Date.now() - (window as any).lastSortChangeTime) < 3000;
      
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
      
      // Enhanced logging for sort changes
      if (isSortTriggered) {
        console.log('🔄 FORCED STATE UPDATE for sort change:', {
          searchId: searchId.toFixed(3),
          newCardCount: paginationResult.initialResults.length,
          firstCard: paginationResult.initialResults[0]?.name,
          lastCard: paginationResult.initialResults[paginationResult.initialResults.length - 1]?.name,
          sortDirection: sortParams?.dir || 'unknown'
        });
        
        // Force re-render by updating a timestamp
        (window as any).lastStateUpdate = Date.now();
      }'''

    if old_state_section in content:
        content = content.replace(old_state_section, new_state_section)
        print("✅ Enhanced state update logic for sort changes")
    else:
        print("⚠️ Could not find state update section - this is optional")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = fix_search_cancellation("src/hooks/useCards.ts")
    
    if success:
        print("\n🎯 SEARCH CANCELLATION FIX APPLIED")
        print("This prevents sort-triggered searches from being cancelled prematurely")
        print("Sort results should now actually update the UI immediately")
        print("\nTest by clicking sort buttons - the new results should appear immediately")
    
    sys.exit(0 if success else 1)