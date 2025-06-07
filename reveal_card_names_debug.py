#!/usr/bin/env python3

import os
import sys

def reveal_card_names_debug():
    """Modify the debug logging to show actual card names instead of Array(3)"""
    
    print("🔧 Adding card name revelation to debug output...")
    
    # Update scryfallApi.ts to show actual card names
    scryfallApi_path = "src/services/scryfallApi.ts"
    if not os.path.exists(scryfallApi_path):
        print(f"❌ {scryfallApi_path} not found")
        return False
        
    with open(scryfallApi_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the API response debug section
    old_api_response = """    console.log('🌐 FIRST 3 CARD NAMES (sort verification):', 
      data.data?.slice(0, 3).map((card: any) => ({
        name: card.name,
        cmc: card.cmc,
        colors: card.colors
      })) || []
    );"""

    new_api_response = """    const first3Cards = data.data?.slice(0, 3).map((card: any) => card.name) || [];
    console.log('🌐 FIRST 3 CARD NAMES (sort verification - ACTUAL NAMES):', first3Cards);
    console.log('🌐 SORT VERIFICATION:', {
      expectedOrder: dir === 'asc' ? 'A→Z alphabetical' : 'Z→A reverse alphabetical',
      actualFirstCard: first3Cards[0] || 'No cards',
      actualSecondCard: first3Cards[1] || 'No cards',
      actualThirdCard: first3Cards[2] || 'No cards',
      sortDirection: dir,
      sortCriteria: order,
      isCorrectOrder: first3Cards.length >= 2 ? 
        (dir === 'asc' ? first3Cards[0] <= first3Cards[1] : first3Cards[0] >= first3Cards[1]) : 
        'Cannot verify'
    });"""

    content = content.replace(old_api_response, new_api_response)
    
    with open(scryfallApi_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Enhanced scryfallApi.ts to show actual card names")
    
    # Add client-side sort debugging to MTGOLayout.tsx
    mtgoLayout_path = "src/components/MTGOLayout.tsx"
    if not os.path.exists(mtgoLayout_path):
        print(f"❌ {mtgoLayout_path} not found")
        return False
        
    with open(mtgoLayout_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add debugging to the sortedCollectionCards useMemo
    old_sortedCards = """  const sortedCollectionCards = useMemo(() => {
    return sortCards(cards, collectionSort.criteria, collectionSort.direction);
  }, [cards, collectionSort.criteria, collectionSort.direction, sortCards]);"""

    new_sortedCards = """  const sortedCollectionCards = useMemo(() => {
    console.log('🔄 ===== CLIENT-SIDE SORTING ANALYSIS =====');
    console.log('🔄 INPUT CARDS (first 3 from API):', cards.slice(0, 3).map(card => card.name));
    console.log('🔄 SORT CRITERIA:', collectionSort.criteria);
    console.log('🔄 SORT DIRECTION:', collectionSort.direction);
    
    const sorted = sortCards(cards, collectionSort.criteria, collectionSort.direction);
    
    console.log('🔄 OUTPUT CARDS (first 3 after client sort):', sorted.slice(0, 3).map(card => card.name));
    console.log('🔄 CLIENT-SIDE SORT CHANGED ORDER:', {
      before: cards.slice(0, 3).map(card => card.name),
      after: sorted.slice(0, 3).map(card => card.name),
      wasReordered: JSON.stringify(cards.slice(0, 3).map(c => c.name)) !== JSON.stringify(sorted.slice(0, 3).map(c => c.name))
    });
    console.log('🔄 ===== CLIENT-SIDE SORTING COMPLETE =====');
    
    return sorted;
  }, [cards, collectionSort.criteria, collectionSort.direction, sortCards]);"""

    content = content.replace(old_sortedCards, new_sortedCards)
    
    with open(mtgoLayout_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Enhanced MTGOLayout.tsx with client-side sort debugging")
    
    # Add debugging to the sortCards function itself
    old_sortCards = """  // Card sorting helper function for all areas
  const sortCards = useCallback((cards: (ScryfallCard | DeckCard | DeckCardInstance)[], criteria: SortCriteria, direction: 'asc' | 'desc'): (ScryfallCard | DeckCard | DeckCardInstance)[] => {
    const sorted = [...cards].sort((a, b) => {
      let comparison = 0;
      
      switch (criteria) {
        case 'name':
          comparison = a.name.localeCompare(b.name);
          break;
        case 'mana':
          comparison = (a.cmc ?? 0) - (b.cmc ?? 0);
          break;
        case 'color':
          const aColors = a.colors?.join('') || 'Z';
          const bColors = b.colors?.join('') || 'Z';
          comparison = aColors.localeCompare(bColors);
          break;
        case 'rarity':
          const rarityOrder = { common: 1, uncommon: 2, rare: 3, mythic: 4 };
          const aRarity = rarityOrder[a.rarity as keyof typeof rarityOrder] || 0;
          const bRarity = rarityOrder[b.rarity as keyof typeof rarityOrder] || 0;
          comparison = aRarity - bRarity;
          break;
        case 'type':
          const aType = a.type_line || '';
          const bType = b.type_line || '';
          comparison = aType.localeCompare(bType);
          break;
        default:
          comparison = a.name.localeCompare(b.name);
      }
      
      return direction === 'desc' ? -comparison : comparison;
    });
    
    return sorted;
  }, []);"""

    new_sortCards = """  // Card sorting helper function for all areas - ENHANCED DEBUG
  const sortCards = useCallback((cards: (ScryfallCard | DeckCard | DeckCardInstance)[], criteria: SortCriteria, direction: 'asc' | 'desc'): (ScryfallCard | DeckCard | DeckCardInstance)[] => {
    console.log('🔨 CLIENT-SIDE SORT FUNCTION CALLED:', {
      cardCount: cards.length,
      criteria: criteria,
      direction: direction,
      firstCardName: cards[0]?.name || 'No cards',
      lastCardName: cards[cards.length - 1]?.name || 'No cards'
    });
    
    const sorted = [...cards].sort((a, b) => {
      let comparison = 0;
      
      switch (criteria) {
        case 'name':
          comparison = a.name.localeCompare(b.name);
          break;
        case 'mana':
          comparison = (a.cmc ?? 0) - (b.cmc ?? 0);
          break;
        case 'color':
          const aColors = a.colors?.join('') || 'Z';
          const bColors = b.colors?.join('') || 'Z';
          comparison = aColors.localeCompare(bColors);
          break;
        case 'rarity':
          const rarityOrder = { common: 1, uncommon: 2, rare: 3, mythic: 4 };
          const aRarity = rarityOrder[a.rarity as keyof typeof rarityOrder] || 0;
          const bRarity = rarityOrder[b.rarity as keyof typeof rarityOrder] || 0;
          comparison = aRarity - bRarity;
          break;
        case 'type':
          const aType = a.type_line || '';
          const bType = b.type_line || '';
          comparison = aType.localeCompare(bType);
          break;
        default:
          comparison = a.name.localeCompare(b.name);
      }
      
      const result = direction === 'desc' ? -comparison : comparison;
      return result;
    });
    
    console.log('🔨 CLIENT-SIDE SORT RESULT:', {
      originalFirst: cards[0]?.name || 'No cards',
      sortedFirst: sorted[0]?.name || 'No cards',
      originalLast: cards[cards.length - 1]?.name || 'No cards', 
      sortedLast: sorted[sorted.length - 1]?.name || 'No cards',
      orderChanged: cards[0]?.name !== sorted[0]?.name
    });
    
    return sorted;
  }, []);"""

    content = content.replace(old_sortCards, new_sortCards)
    
    with open(mtgoLayout_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Enhanced sortCards function with detailed debugging")
    
    return True

if __name__ == "__main__":
    success = reveal_card_names_debug()
    if success:
        print("\n🎯 CARD NAME DEBUGGING ADDED SUCCESSFULLY!")
        print("\n📋 NEXT STEPS:")
        print("1. Run `npm start` to test the application")
        print("2. Click any collection sort button")
        print("3. Watch for these NEW debug messages:")
        print("   - 🌐 FIRST 3 CARD NAMES (sort verification - ACTUAL NAMES)")
        print("   - 🌐 SORT VERIFICATION (shows if order is correct)")
        print("   - 🔄 CLIENT-SIDE SORTING ANALYSIS")
        print("   - 🔨 CLIENT-SIDE SORT FUNCTION debug")
        print("\n🔍 THIS WILL REVEAL:")
        print("- Exact card names returned by Scryfall API")
        print("- Whether Scryfall returns correct A→Z or wrong Z→A")
        print("- Whether client-side sorting changes the API order")
        print("- Which step causes the Z→A reversal")
    else:
        print("❌ Failed to add card name debugging")
    
    sys.exit(0 if success else 1)