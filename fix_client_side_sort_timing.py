#!/usr/bin/env python3

import os
import sys

def fix_client_side_sort_timing():
    """Fix the client-side sorting to use fresh server results instead of stale data"""
    
    print("🔧 Fixing client-side sort timing issue...")
    
    # Update MTGOLayout.tsx to disable client-side sorting for server-side sorted results
    mtgoLayout_path = "src/components/MTGOLayout.tsx"
    if not os.path.exists(mtgoLayout_path):
        print(f"❌ {mtgoLayout_path} not found")
        return False
        
    with open(mtgoLayout_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the sortedCollectionCards useMemo to disable client sorting for large datasets
    old_sorted_cards = """  const sortedCollectionCards = useMemo(() => {
    console.log('🔄 ===== CLIENT-SIDE SORTING ANALYSIS =====');
    console.log('🔄 INPUT FROM API:');
    if (cards.length >= 3) {
      console.log('🔄   Card 1:', cards[0].name);
      console.log('🔄   Card 2:', cards[1].name);
      console.log('🔄   Card 3:', cards[2].name);
    }
    console.log('🔄 SORT CRITERIA:', collectionSort.criteria);
    console.log('🔄 SORT DIRECTION:', collectionSort.direction);
    
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
  }, [cards, collectionSort.criteria, collectionSort.direction, sortCards]);"""

    new_sorted_cards = """  const sortedCollectionCards = useMemo(() => {
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
    
    // SMART SORTING FIX: For large datasets (>75 cards), server-side sorting is already applied
    // Don't re-sort on client-side - just use the server results directly
    const isLargeDataset = cards.length > 75;
    const shouldUseServerSort = isLargeDataset;
    
    if (shouldUseServerSort) {
      console.log('🔄 USING SERVER-SIDE RESULTS DIRECTLY (no client sorting)');
      console.log('🔄 Server results already sorted by Scryfall API');
      console.log('🔄 ===== CLIENT-SIDE SORTING BYPASSED =====');
      return cards; // Return server results as-is
    }
    
    // For small datasets (<= 75 cards), use client-side sorting
    console.log('🔄 APPLYING CLIENT-SIDE SORTING (small dataset)');
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
  }, [cards, collectionSort.criteria, collectionSort.direction, sortCards]);"""

    content = content.replace(old_sorted_cards, new_sorted_cards)
    
    with open(mtgoLayout_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed client-side sorting to bypass for large datasets")
    
    return True

if __name__ == "__main__":
    success = fix_client_side_sort_timing()
    if success:
        print("\n🎯 CLIENT-SIDE SORTING FIX APPLIED!")
        print("\n📋 WHAT THIS FIXES:")
        print("✅ Large datasets (>75 cards) will use server results directly")
        print("✅ No more client-side re-sorting of server-sorted results")
        print("✅ You'll now see the actual Z→A cards from Scryfall")
        print("✅ Sort button will show real server-side sorted results")
        print("\n🔍 TEST NOW:")
        print("1. Run npm start")
        print("2. Click Name sort button")
        print("3. You should see Zurgo cards (Z→A) instead of re-sorted A→Z cards")
        print("4. Console will show 'USING SERVER-SIDE RESULTS DIRECTLY'")
    else:
        print("❌ Failed to apply client-side sorting fix")
    
    sys.exit(0 if success else 1)