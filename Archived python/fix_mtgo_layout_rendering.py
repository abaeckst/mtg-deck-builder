#!/usr/bin/env python3

import os
import sys

def fix_mtgo_layout_rendering():
    """Fix MTGOLayout component to properly detect and render card changes"""
    
    filename = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the sortedCollectionCards useMemo to properly detect changes
    old_sorted_cards = """  // Get sorted cards for each area
  const sortedCollectionCards = useMemo(() => {
    console.log('🔄 ===== CLIENT-SIDE SORTING ANALYSIS =====');
    console.log('🔄 INPUT FROM API:');
    if (cards.length >= 3) {
      console.log('🔄   Card 1:', cards[0].name);
      console.log('🔄   Card 2:', cards[1].name);
      console.log('🔄   Card 3:', cards[2].name);
    }
    console.log('🔄 SORT CRITERIA:', collectionSort.criteria);
    console.log('🔄 SORT DIRECTION:', collectionSort.direction);
    console.log('🔄 TOTAL CARDS:', cards.length);
    
    // SMART SORTING FIX: Check if we already have server-sorted results
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
    const sorted = sortCards(cards, collectionSort.criteria, collectionSort.direction);
    
    console.log('🔄 OUTPUT AFTER CLIENT SORT:');
    if (sorted.length >= 3) {
      console.log('🔄   Card 1:', sorted[0].name);
      console.log('🔄   Card 2:', sorted[1].name);
      console.log('🔄   Card 3:', sorted[2].name);
    }
    
    console.log('🔄 ORDER CHANGE ANALYSIS:', {
      apiFirst: cards[0]?.name || 'none',
      clientFirst: sorted[0]?.name || 'none',
      orderChanged: cards[0]?.name !== sorted[0]?.name
    });
    console.log('🔄 ===== CLIENT-SIDE SORTING COMPLETE =====');
    
    return sorted;
  }, [cards, collectionSort.criteria, collectionSort.direction, sortCards, pagination]);"""

    new_sorted_cards = """  // Get sorted cards for each area - FIXED FOR PROPER REACT UPDATES
  const sortedCollectionCards = useMemo(() => {
    // Add update tracking for debugging
    const updateTracker = (window as any).lastSuccessfulSortUpdate || 0;
    
    console.log('🔄 ===== COLLECTION CARDS MEMO RECALCULATION =====');
    console.log('🔄 MEMO DEPENDENCIES CHECK:', {
      cardsLength: cards.length,
      cardsFirstCard: cards[0]?.name || 'None',
      sortCriteria: collectionSort.criteria,
      sortDirection: collectionSort.direction,
      updateTracker: updateTracker,
      cardsReference: cards === (window as any).lastCardsReference ? 'SAME' : 'DIFFERENT'
    });
    
    // Store cards reference for tracking
    (window as any).lastCardsReference = cards;
    
    if (cards.length >= 3) {
      console.log('🔄 CURRENT CARDS:', {
        card1: cards[0].name,
        card2: cards[1].name,
        card3: cards[2].name,
        totalCards: cards.length
      });
    }
    
    // Check if we have server-sorted results (reduced time window for faster response)
    const hasRecentSortChange = (window as any).lastSortChangeTime && 
                               (Date.now() - (window as any).lastSortChangeTime) < 3000; // Reduced to 3 seconds
    
    const totalCardsAvailable = pagination?.totalCards || cards.length;
    
    console.log('🔄 SORTING DECISION ANALYSIS:', {
      hasRecentSortChange,
      lastSortTime: (window as any).lastSortChangeTime,
      timeSinceSort: (window as any).lastSortChangeTime ? Date.now() - (window as any).lastSortChangeTime : 'N/A',
      totalCards: totalCardsAvailable,
      threshold: 75,
      shouldUseServerResults: hasRecentSortChange
    });
    
    // If we recently triggered a sort change, use server results directly
    if (hasRecentSortChange) {
      console.log('🔄 USING SERVER-SIDE RESULTS DIRECTLY (recent sort change detected)');
      console.log('🔄 Server results already sorted by Scryfall API');
      console.log('🔄 ===== CLIENT-SIDE SORTING BYPASSED =====');
      // Return a new array reference to ensure React detects the change
      return [...cards];
    }
    
    // Apply client-side sorting for initial load or when no recent sort changes
    console.log('🔄 APPLYING CLIENT-SIDE SORTING');
    const sorted = sortCards([...cards], collectionSort.criteria, collectionSort.direction);
    
    console.log('🔄 CLIENT SORT RESULT:', {
      inputFirst: cards[0]?.name || 'None',
      outputFirst: sorted[0]?.name || 'None',
      orderChanged: cards[0]?.name !== sorted[0]?.name,
      sortedLength: sorted.length
    });
    console.log('🔄 ===== CLIENT-SIDE SORTING COMPLETE =====');
    
    return sorted;
  }, [cards, collectionSort.criteria, collectionSort.direction, sortCards, pagination, (window as any).lastSuccessfulSortUpdate]);"""

    if old_sorted_cards in content:
        content = content.replace(old_sorted_cards, new_sorted_cards)
        print("✅ Fixed sortedCollectionCards useMemo with better React change detection")
    else:
        print("❌ Could not find sortedCollectionCards useMemo")
        return False

    # Add a debug effect to track when cards change
    debug_effect = """  // Debug effect to track card changes
  useEffect(() => {
    if (cards.length > 0) {
      console.log('🎯 CARDS STATE CHANGED IN MTGO LAYOUT:', {
        cardsLength: cards.length,
        firstCard: cards[0]?.name || 'None',
        lastCard: cards[cards.length - 1]?.name || 'None',
        timestamp: Date.now(),
        isAfterSort: (window as any).lastSortChangeTime && 
                     (Date.now() - (window as any).lastSortChangeTime) < 3000
      });
    }
  }, [cards]);

"""

    # Insert the debug effect after the other hooks
    insert_point = "  // Clear both deck and sideboard functionality"
    if insert_point in content:
        content = content.replace(insert_point, debug_effect + insert_point)
        print("✅ Added cards change tracking effect")
    else:
        print("❌ Could not find insertion point for debug effect")

    # Write the updated content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename} with rendering fixes")
    return True

if __name__ == "__main__":
    success = fix_mtgo_layout_rendering()
    sys.exit(0 if success else 1)