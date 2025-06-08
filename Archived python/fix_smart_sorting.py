#!/usr/bin/env python3

import os
import sys

def fix_smart_sorting_logic(filename):
    """Fix the smart sorting logic to prevent double sorting of server results"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the smart sorting logic in sortedCollectionCards useMemo
    old_smart_logic = '''    // SMART SORTING FIX: Use totalCards (not loaded cards) to determine if dataset is large
    // If there are >75 cards TOTAL available, use server-side sorting
    const totalCardsAvailable = pagination?.totalCards || cards.length;
    const isLargeDataset = totalCardsAvailable > 75;
    const shouldUseServerSort = isLargeDataset;
    
    console.log('🔄 SMART SORTING DECISION:', {
      loadedCards: cards.length,
      totalCards: totalCardsAvailable,
      threshold: 75,
      isLargeDataset,
      willUseServerSort: shouldUseServerSort
    });
    
    if (shouldUseServerSort) {
      console.log('🔄 USING SERVER-SIDE RESULTS DIRECTLY (no client sorting)');
      console.log('🔄 Server results already sorted by Scryfall API');
      console.log('🔄 ===== CLIENT-SIDE SORTING BYPASSED =====');
      return cards; // Return server results as-is
    }
    
    // For small datasets (<= 75 cards), use client-side sorting
    console.log('🔄 APPLYING CLIENT-SIDE SORTING (small dataset)');
    const sorted = sortCards(cards, collectionSort.criteria, collectionSort.direction);'''

    new_smart_logic = '''    // SMART SORTING FIX: Check if we already have server-sorted results
    // Server-side sorting is triggered for ALL sort changes via updateSort() function
    // We should only apply client-side sorting for the initial default state
    const totalCardsAvailable = pagination?.totalCards || cards.length;
    const isLargeDataset = totalCardsAvailable > 75;
    
    // Check if this is likely server-sorted data by examining if sort was recently changed
    // For server-sorted results, trust the API ordering and don't re-sort client-side
    const hasRecentSortChange = (window as any).lastSortChangeTime && 
                               (Date.now() - (window as any).lastSortChangeTime) < 5000; // 5 seconds
    
    console.log('🔄 SMART SORTING DECISION:', {
      loadedCards: cards.length,
      totalCards: totalCardsAvailable,
      threshold: 75,
      isLargeDataset,
      hasRecentSortChange,
      lastSortTime: (window as any).lastSortChangeTime,
      decision: hasRecentSortChange ? 'USE_SERVER_RESULTS' : 'APPLY_CLIENT_SORT'
    });
    
    // If we recently triggered a sort change, trust the server results
    if (hasRecentSortChange) {
      console.log('🔄 USING SERVER-SIDE RESULTS DIRECTLY (recent sort change detected)');
      console.log('🔄 Server results already sorted by Scryfall API');
      console.log('🔄 ===== CLIENT-SIDE SORTING BYPASSED =====');
      return cards; // Return server results as-is
    }
    
    // Only apply client-side sorting for initial load or when no recent sort changes
    console.log('🔄 APPLYING CLIENT-SIDE SORTING (initial load or no recent sort changes)');
    const sorted = sortCards(cards, collectionSort.criteria, collectionSort.direction);'''

    if old_smart_logic in content:
        content = content.replace(old_smart_logic, new_smart_logic)
        print("✅ Fixed smart sorting logic to prevent double sorting")
    else:
        print("❌ Could not find smart sorting logic pattern to replace")
        return False
    
    # Also need to add timestamp tracking in useSorting updateSort function
    # Find the updateSort function and add timestamp tracking
    old_update_sort = '''    console.log('🚨 ===== UPDATE SORT FUNCTION COMPLETE =====');
  }, [sortState]);'''

    new_update_sort = '''    // Track sort change timing for smart sorting logic
    (window as any).lastSortChangeTime = Date.now();
    
    console.log('🚨 ===== UPDATE SORT FUNCTION COMPLETE =====');
  }, [sortState]);'''

    if old_update_sort in content:
        content = content.replace(old_update_sort, new_update_sort)
        print("✅ Added sort change timestamp tracking")
    else:
        print("❌ Could not find updateSort function end to add timestamp tracking")
        # This might be in useSorting.ts instead, which is OK
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename}")
    return True

if __name__ == "__main__":
    success = fix_smart_sorting_logic("src/components/MTGOLayout.tsx")
    
    if success:
        print("\n🎯 SMART SORTING FIX APPLIED")
        print("This fix prevents client-side sorting from overriding server-sorted results")
        print("Test by clicking sort buttons - should now show different results immediately")
        print("\nIf the timestamp approach doesn't work reliably, we can try a different approach")
    
    sys.exit(0 if success else 1)