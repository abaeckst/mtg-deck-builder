#!/usr/bin/env python3

import os
import sys

def add_simple_card_name_debug():
    """Add simple, direct card name logging that will definitely work"""
    
    print("🔧 Adding SIMPLE card name debugging...")
    
    # Update scryfallApi.ts with ultra-simple debugging
    scryfallApi_path = "src/services/scryfallApi.ts"
    if not os.path.exists(scryfallApi_path):
        print(f"❌ {scryfallApi_path} not found")
        return False
        
    with open(scryfallApi_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the API response section and add ultra-simple logging
    old_response_section = """    const response = await rateLimitedFetch(url);
    const data = await response.json();
    
    console.log('🌐 ===== SCRYFALL API RESPONSE ANALYSIS =====');
    console.log('🌐 RESPONSE STATUS:', response.status);
    console.log('🌐 TOTAL CARDS:', data.total_cards);
    console.log('🌐 RETURNED COUNT:', data.data?.length || 0);
    console.log('🌐 HAS MORE:', data.has_more);
    const first3Cards = data.data?.slice(0, 3).map((card: any) => card.name) || [];
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
    });
    console.log('🌐 ===== API RESPONSE COMPLETE =====');"""

    new_response_section = """    const response = await rateLimitedFetch(url);
    const data = await response.json();
    
    console.log('🌐 ===== SCRYFALL API RESPONSE ANALYSIS =====');
    console.log('🌐 RESPONSE STATUS:', response.status);
    console.log('🌐 TOTAL CARDS:', data.total_cards);
    console.log('🌐 RETURNED COUNT:', data.data?.length || 0);
    console.log('🌐 HAS MORE:', data.has_more);
    
    // ULTRA-SIMPLE card name debugging
    if (data.data && data.data.length > 0) {
      console.log('🌐 CARD 1 NAME:', data.data[0].name);
      if (data.data.length > 1) console.log('🌐 CARD 2 NAME:', data.data[1].name);
      if (data.data.length > 2) console.log('🌐 CARD 3 NAME:', data.data[2].name);
      
      console.log('🌐 SORT VERIFICATION SIMPLE:', {
        direction: dir,
        expectedOrder: dir === 'asc' ? 'A→Z' : 'Z→A',
        card1: data.data[0].name,
        card2: data.data[1]?.name || 'N/A',
        card3: data.data[2]?.name || 'N/A'
      });
      
      // Simple A-Z verification
      if (data.data.length >= 2) {
        const isAscending = data.data[0].name <= data.data[1].name;
        const expectedAscending = dir === 'asc';
        console.log('🌐 SORT ORDER CHECK:', {
          actuallyAscending: isAscending,
          shouldBeAscending: expectedAscending,
          isCorrect: isAscending === expectedAscending
        });
      }
    } else {
      console.log('🌐 NO CARDS IN RESPONSE');
    }
    console.log('🌐 ===== API RESPONSE COMPLETE =====');"""

    content = content.replace(old_response_section, new_response_section)
    
    with open(scryfallApi_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added ultra-simple card name debugging to scryfallApi.ts")
    
    # Update MTGOLayout.tsx with ultra-simple client-side debugging
    mtgoLayout_path = "src/components/MTGOLayout.tsx"
    if not os.path.exists(mtgoLayout_path):
        print(f"❌ {mtgoLayout_path} not found")
        return False
        
    with open(mtgoLayout_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the client-side sorting debug
    old_client_debug = """    console.log('🔄 ===== CLIENT-SIDE SORTING ANALYSIS =====');
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
    console.log('🔄 ===== CLIENT-SIDE SORTING COMPLETE =====');"""

    new_client_debug = """    console.log('🔄 ===== CLIENT-SIDE SORTING ANALYSIS =====');
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
    console.log('🔄 ===== CLIENT-SIDE SORTING COMPLETE =====');"""

    content = content.replace(old_client_debug, new_client_debug)
    
    with open(mtgoLayout_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added ultra-simple client-side debugging to MTGOLayout.tsx")
    
    return True

if __name__ == "__main__":
    success = add_simple_card_name_debug()
    if success:
        print("\n🎯 ULTRA-SIMPLE CARD NAME DEBUGGING ADDED!")
        print("\n📋 NOW YOU WILL SEE:")
        print("🌐 CARD 1 NAME: [actual card name]")
        print("🌐 CARD 2 NAME: [actual card name]") 
        print("🌐 CARD 3 NAME: [actual card name]")
        print("🔄   Card 1: [actual card name]")
        print("🔄   Card 2: [actual card name]")
        print("🔄   Card 3: [actual card name]")
        print("\n🔍 THIS WILL FINALLY REVEAL:")
        print("- Exact card names from Scryfall API")
        print("- Whether Scryfall returns A→Z or Z→A")
        print("- Whether client-side sorting changes the order")
        print("- Which step causes any incorrect sorting")
        print("\nRun npm start and click a sort button!")
    else:
        print("❌ Failed to add simple card name debugging")
    
    sys.exit(0 if success else 1)