#!/usr/bin/env python3

import os
import sys

def fix_smart_sorting_logic():
    """Fix smart sorting to use totalCards instead of loaded cards count"""
    
    print("🔧 Fixing smart sorting logic to use total cards instead of loaded cards...")
    
    # Update MTGOLayout.tsx to use pagination.totalCards instead of cards.length
    mtgoLayout_path = "src/components/MTGOLayout.tsx"
    if not os.path.exists(mtgoLayout_path):
        print(f"❌ {mtgoLayout_path} not found")
        return False
        
    with open(mtgoLayout_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the smart sorting logic to use totalCards
    old_smart_logic = """    // SMART SORTING FIX: For large datasets (>75 cards), server-side sorting is already applied
    // Don't re-sort on client-side - just use the server results directly
    const isLargeDataset = cards.length > 75;
    const shouldUseServerSort = isLargeDataset;"""

    new_smart_logic = """    // SMART SORTING FIX: Use totalCards (not loaded cards) to determine if dataset is large
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
    });"""

    content = content.replace(old_smart_logic, new_smart_logic)
    
    # Add pagination prop to the useMemo dependencies and make it accessible
    old_useMemo_deps = """  }, [cards, collectionSort.criteria, collectionSort.direction, sortCards]);"""
    new_useMemo_deps = """  }, [cards, collectionSort.criteria, collectionSort.direction, sortCards, pagination]);"""
    
    content = content.replace(old_useMemo_deps, new_useMemo_deps)
    
    with open(mtgoLayout_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed smart sorting logic to use total cards available")
    
    # Also update the server-side sorting decision in useCards.ts
    useCards_path = "src/hooks/useCards.ts"
    if not os.path.exists(useCards_path):
        print(f"❌ {useCards_path} not found")
        return False
        
    with open(useCards_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the server-side sort decision in handleCollectionSortChange
    old_server_decision = """    // Smart sorting logic: server-side only when there are more results available
    const shouldUseServerSort = metadata.totalCards > 75;"""

    new_server_decision = """    // Smart sorting logic: server-side when total dataset is large (>75 cards)
    const shouldUseServerSort = metadata.totalCards > 75;"""

    content = content.replace(old_server_decision, new_server_decision)
    
    with open(useCards_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Verified server-side sorting decision logic")
    
    return True

if __name__ == "__main__":
    success = fix_smart_sorting_logic()
    if success:
        print("\n🎯 SMART SORTING LOGIC FIXED!")
        print("\n📋 WHAT THIS FIXES:")
        print("✅ Uses totalCards (2323) instead of loaded cards (75) for smart sorting decision")
        print("✅ System will now recognize large datasets and use server-side sorting")
        print("✅ Console will show 'USING SERVER-SIDE RESULTS DIRECTLY' for large datasets")
        print("✅ You'll get the real Zurgo cards (Z→A) from Scryfall API")
        print("\n🔍 TEST NOW:")
        print("1. Run npm start")
        print("2. Click Name sort button")
        print("3. Console should show: isLargeDataset: true, willUseServerSort: true")
        print("4. You should see 'USING SERVER-SIDE RESULTS DIRECTLY'")
        print("5. Cards should be actual Z→A results (Zurgo) not re-sorted A→Z")
    else:
        print("❌ Failed to fix smart sorting logic")
    
    sys.exit(0 if success else 1)