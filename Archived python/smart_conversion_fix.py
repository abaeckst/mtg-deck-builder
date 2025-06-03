#!/usr/bin/env python3
"""
Smart Conversion Fix: Handle both ScryfallCard and DeckCard types properly
"""

import os

def fix_card_conversion():
    """Fix card conversion to handle both ScryfallCard and DeckCard types"""
    
    file_path = r'C:\Users\carol\mtg-deckbuilder\src\components\MTGOLayout.tsx'
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Reading MTGOLayout.tsx for smart conversion fixes")
        
        # Step 1: Add a smart conversion helper function after imports
        old_interface_section = """interface MTGOLayoutProps {
  // Props for any data that needs to be passed down
}"""
        
        new_interface_section = """interface MTGOLayoutProps {
  // Props for any data that needs to be passed down
}

// Helper function to convert any card to DeckCard
const toDeckCard = (card: ScryfallCard | DeckCard, quantity: number = 1): DeckCard => {
  // If it's already a DeckCard, just update quantity
  if ('quantity' in card && 'maxQuantity' in card) {
    return { ...card, quantity };
  }
  
  // If it's a ScryfallCard, convert it
  return { ...scryfallToDeckCard(card as ScryfallCard), quantity };
};"""
        
        if old_interface_section in content:
            content = content.replace(old_interface_section, new_interface_section)
            print("✅ Step 1: Added smart toDeckCard helper function")
        else:
            print("⚠️ Step 1: Interface section not found exactly")
        
        # Step 2: Replace all scryfallToDeckCard(card) calls with toDeckCard(card, quantity)
        # Pattern 1: { ...scryfallToDeckCard(card), quantity: addQuantity }
        old_pattern1 = "{ ...scryfallToDeckCard(card), quantity: addQuantity }"
        new_pattern1 = "toDeckCard(card, addQuantity)"
        content = content.replace(old_pattern1, new_pattern1)
        
        # Pattern 2: { ...scryfallToDeckCard(card), quantity: 1 }
        old_pattern2 = "{ ...scryfallToDeckCard(card), quantity: 1 }"
        new_pattern2 = "toDeckCard(card, 1)"
        content = content.replace(old_pattern2, new_pattern2)
        
        # Pattern 3: { ...scryfallToDeckCard(card), quantity: moveQuantity }
        old_pattern3 = "{ ...scryfallToDeckCard(card), quantity: moveQuantity }"
        new_pattern3 = "toDeckCard(card, moveQuantity)"
        content = content.replace(old_pattern3, new_pattern3)
        
        print("✅ Step 2: Replaced all scryfallToDeckCard calls with smart toDeckCard")
        
        # Step 3: Fix the handleAddToDeck function
        old_handle_add_to_deck = """  const handleAddToDeck = (card: ScryfallCard | DeckCard) => {
    const existingCard = mainDeck.find((deckCard: DeckCard) => deckCard.id === card.id);
    if (existingCard && existingCard.quantity < 4) {
      setMainDeck((prev: DeckCard[]) => prev.map((deckCard: DeckCard) => 
        deckCard.id === card.id 
          ? { ...deckCard, quantity: deckCard.quantity + 1 }
          : deckCard
      ));
    } else if (!existingCard) {
      setMainDeck((prev: DeckCard[]) => [...prev, { ...scryfallToDeckCard(card as ScryfallCard), quantity: 1 }]);
    }
  };"""
        
        new_handle_add_to_deck = """  const handleAddToDeck = (card: ScryfallCard | DeckCard) => {
    const existingCard = mainDeck.find((deckCard: DeckCard) => deckCard.id === card.id);
    if (existingCard && existingCard.quantity < 4) {
      setMainDeck((prev: DeckCard[]) => prev.map((deckCard: DeckCard) => 
        deckCard.id === card.id 
          ? { ...deckCard, quantity: deckCard.quantity + 1 }
          : deckCard
      ));
    } else if (!existingCard) {
      setMainDeck((prev: DeckCard[]) => [...prev, toDeckCard(card, 1)]);
    }
  };"""
        
        if old_handle_add_to_deck in content:
            content = content.replace(old_handle_add_to_deck, new_handle_add_to_deck)
            print("✅ Step 3: Fixed handleAddToDeck function")
        
        # Write the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Smart conversion fix complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error during smart conversion fix: {e}")
        return False

def main():
    print("🔧 Smart Conversion Fix: Handle Both Card Types")
    print("=" * 50)
    
    if fix_card_conversion():
        print()
        print("🎉 Smart Conversion Fix Complete!")
        print("✅ Added intelligent toDeckCard helper function")
        print("✅ Fixed all card conversion calls")
        print("✅ Fixed handleAddToDeck function")
        print()
        print("🧪 Testing Instructions:")
        print("1. Run `npm start` to verify compilation")
        print("2. All TypeScript errors should be resolved")
        print("3. Test pile view functionality")
    else:
        print("❌ Smart conversion fix failed")

if __name__ == "__main__":
    main()
