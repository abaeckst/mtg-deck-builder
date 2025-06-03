#!/usr/bin/env python3
"""
Fix DeckCard Conversion to Include Missing Properties
The issue is that scryfallToDeckCard function doesn't copy oracle_text, power, toughness
Run from project root: python fix_deckcard_conversion.py
"""

import os
import sys

def fix_deckcard_conversion():
    """Fix the scryfallToDeckCard function to include missing properties"""
    
    # Verify we're in the correct directory
    if not os.path.exists('src/types/card.ts'):
        print("❌ Error: Please run this script from the project root directory (mtg-deckbuilder)")
        return False
    
    print("🔧 Fixing DeckCard conversion function...")
    
    try:
        with open('src/types/card.ts', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and fix the DeckCard interface to include missing properties
        old_deckcard_interface = """export interface DeckCard {
  // Card identification
  id: string;
  name: string;
  
  // Display information
  image_uri: string;
  mana_cost?: string;
  cmc: number;
  type_line: string;
  
  // Colors for filtering
  colors: string[];
  color_identity: string[];
  
  // Set and rarity for display
  set: string;
  rarity: 'common' | 'uncommon' | 'rare' | 'mythic' | 'special' | 'bonus';
  
  // Deck building
  quantity: number; // How many copies in deck/sideboard
  maxQuantity: number; // Usually 4, unlimited for basic lands
  
  // Format legality
  legal_in_format?: boolean; // Will be set based on selected format

  oracle_text?: string;
  power?: string;
  toughness?: string;
}"""
        
        new_deckcard_interface = """export interface DeckCard {
  // Card identification
  id: string;
  name: string;
  
  // Display information
  image_uri: string;
  mana_cost?: string;
  cmc: number;
  type_line: string;
  
  // Colors for filtering
  colors: string[];
  color_identity: string[];
  
  // Set and rarity for display
  set: string;
  rarity: 'common' | 'uncommon' | 'rare' | 'mythic' | 'special' | 'bonus';
  
  // Deck building
  quantity: number; // How many copies in deck/sideboard
  maxQuantity: number; // Usually 4, unlimited for basic lands
  
  // Format legality
  legal_in_format?: boolean; // Will be set based on selected format
  
  // Card text and stats (from Scryfall)
  oracle_text?: string;
  power?: string;
  toughness?: string;
  loyalty?: string;
}"""
        
        # Find and fix the scryfallToDeckCard function
        old_conversion_function = """export const scryfallToDeckCard = (scryfallCard: ScryfallCard): DeckCard => {
  return {
    id: scryfallCard.id,
    name: scryfallCard.name,
    image_uri: getCardImageUri(scryfallCard),
    mana_cost: scryfallCard.mana_cost,
    cmc: scryfallCard.cmc,
    type_line: scryfallCard.type_line,
    colors: scryfallCard.colors,
    color_identity: scryfallCard.color_identity,
    set: scryfallCard.set,
    rarity: scryfallCard.rarity,
    quantity: 0, // Initially not in deck
    maxQuantity: isBasicLand(scryfallCard) ? Infinity : 4,
  };
};"""
        
        new_conversion_function = """export const scryfallToDeckCard = (scryfallCard: ScryfallCard): DeckCard => {
  return {
    id: scryfallCard.id,
    name: scryfallCard.name,
    image_uri: getCardImageUri(scryfallCard),
    mana_cost: scryfallCard.mana_cost,
    cmc: scryfallCard.cmc,
    type_line: scryfallCard.type_line,
    colors: scryfallCard.colors,
    color_identity: scryfallCard.color_identity,
    set: scryfallCard.set,
    rarity: scryfallCard.rarity,
    quantity: 0, // Initially not in deck
    maxQuantity: isBasicLand(scryfallCard) ? Infinity : 4,
    // Copy card text and stats
    oracle_text: scryfallCard.oracle_text,
    power: scryfallCard.power,
    toughness: scryfallCard.toughness,
    loyalty: scryfallCard.loyalty,
  };
};"""
        
        fixes_applied = 0
        
        if old_deckcard_interface in content:
            content = content.replace(old_deckcard_interface, new_deckcard_interface)
            fixes_applied += 1
            print("   ✅ Enhanced DeckCard interface with missing properties")
        
        if old_conversion_function in content:
            content = content.replace(old_conversion_function, new_conversion_function)
            fixes_applied += 1
            print("   ✅ Fixed scryfallToDeckCard conversion function")
        
        if fixes_applied == 0:
            print("   ⚠️  No conversion patterns found to fix")
            return False
        
        with open('src/types/card.ts', 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"   ❌ Error fixing card.ts: {e}")
        return False
    
    print(f"\n🎯 Fixed {fixes_applied} patterns in card conversion!")
    print("\nNext steps:")
    print("1. Run 'npm start' to test the fixes")
    print("2. Switch to List view")
    print("3. Check if power, toughness, and text columns now show data")
    print("4. The cards will now have all the Scryfall properties!")
    
    return True

if __name__ == "__main__":
    success = fix_deckcard_conversion()
    if success:
        print("\n✅ DeckCard conversion should now include all card properties!")
        print("\n💡 NOTE: You may need to search for new cards to see the fix take effect")
        print("   (The current cards in memory are already converted without these properties)")
    else:
        print("\n❌ Could not fix the conversion function")
        sys.exit(1)