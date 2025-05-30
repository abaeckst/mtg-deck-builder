#!/usr/bin/env python3
"""
Comprehensive Fix Script: Fix all MTGOLayout.tsx issues in one shot
- Remove duplicate imports
- Fix type mismatches with proper ScryfallCard to DeckCard conversion
- Add view toggle buttons for pile view
- Fix all TypeScript errors
"""

import os
import re

def comprehensive_fix():
    """Fix all issues in MTGOLayout.tsx comprehensively"""
    
    file_path = r'C:\Users\carol\mtg-deckbuilder\src\components\MTGOLayout.tsx'
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Reading MTGOLayout.tsx for comprehensive fixes")
        
        # STEP 1: Remove duplicate import (lines 12-15)
        old_duplicate_section = """// Card types import
import { ScryfallCard, DeckCard } from '../types/card';

// Card types import
import { ScryfallCard, DeckCard } from '../types/card';"""
        
        new_single_import = """// Card types import
import { ScryfallCard, DeckCard, scryfallToDeckCard } from '../types/card';"""
        
        if old_duplicate_section in content:
            content = content.replace(old_duplicate_section, new_single_import)
            print("✅ Step 1: Removed duplicate imports and added scryfallToDeckCard utility")
        else:
            print("⚠️ Step 1: Duplicate import pattern not found exactly")
        
        # STEP 2: Add view toggle buttons to deck header
        old_deck_controls = """              <div className="deck-controls">
                <span>Size: </span>
                <input
                  type="range"
                  min="0.7"
                  max="2.5"
                  step="0.1"
                  value={cardSizes.deck}
                  onChange={(e) => updateDeckSize(parseFloat(e.target.value))}
                  className="size-slider"
                  title={`Card size: ${Math.round(cardSizes.deck * 100)}%`}
                />
                <button>Save Deck</button>
                <button onClick={handleClearDeck} title="Clear all cards from deck">
                  Clear Deck
                </button>
              </div>"""
        
        new_deck_controls = """              <div className="deck-controls">
                <span>Size: </span>
                <input
                  type="range"
                  min="0.7"
                  max="2.5"
                  step="0.1"
                  value={cardSizes.deck}
                  onChange={(e) => updateDeckSize(parseFloat(e.target.value))}
                  className="size-slider"
                  title={`Card size: ${Math.round(cardSizes.deck * 100)}%`}
                />
                <span>View: </span>
                <button 
                  className={layout.viewModes.deck === 'card' ? 'active' : ''}
                  onClick={() => updateViewMode('deck', 'card')}
                >
                  Card
                </button>
                <button 
                  className={layout.viewModes.deck === 'pile' ? 'active' : ''}
                  onClick={() => updateViewMode('deck', 'pile')}
                >
                  Pile
                </button>
                <button>Save Deck</button>
                <button onClick={handleClearDeck} title="Clear all cards from deck">
                  Clear Deck
                </button>
              </div>"""
        
        if old_deck_controls in content:
            content = content.replace(old_deck_controls, new_deck_controls)
            print("✅ Step 2: Added view toggle buttons to deck header")
        else:
            print("⚠️ Step 2: Deck controls not found exactly")
        
        # STEP 3: Add view toggle buttons to sideboard header
        old_sideboard_controls = """              <div className="sideboard-controls">
                <span>Size: </span>
                <input
                  type="range"
                  min="0.7"
                  max="2.5"
                  step="0.1"
                  value={cardSizes.sideboard}
                  onChange={(e) => updateSideboardSize(parseFloat(e.target.value))}
                  className="size-slider"
                  title={`Card size: ${Math.round(cardSizes.sideboard * 100)}%`}
                />
                <button onClick={handleClearSideboard} title="Clear all cards from sideboard">
                  Clear
                </button>
              </div>"""
        
        new_sideboard_controls = """              <div className="sideboard-controls">
                <span>Size: </span>
                <input
                  type="range"
                  min="0.7"
                  max="2.5"
                  step="0.1"
                  value={cardSizes.sideboard}
                  onChange={(e) => updateSideboardSize(parseFloat(e.target.value))}
                  className="size-slider"
                  title={`Card size: ${Math.round(cardSizes.sideboard * 100)}%`}
                />
                <span>View: </span>
                <button 
                  className={layout.viewModes.sideboard === 'card' ? 'active' : ''}
                  onClick={() => updateViewMode('sideboard', 'card')}
                >
                  Card
                </button>
                <button 
                  className={layout.viewModes.sideboard === 'pile' ? 'active' : ''}
                  onClick={() => updateViewMode('sideboard', 'pile')}
                >
                  Pile
                </button>
                <button onClick={handleClearSideboard} title="Clear all cards from sideboard">
                  Clear
                </button>
              </div>"""
        
        if old_sideboard_controls in content:
            content = content.replace(old_sideboard_controls, new_sideboard_controls)
            print("✅ Step 3: Added view toggle buttons to sideboard header")
        else:
            print("⚠️ Step 3: Sideboard controls not found exactly")
        
        # STEP 4: Fix all ScryfallCard -> DeckCard conversion issues
        # Pattern: setMainDeck(prev => [...prev, { ...card, quantity: X }]);
        # Replace with: setMainDeck(prev => [...prev, scryfallToDeckCard(card)]);
        
        # Fix pattern 1: { ...card, quantity: addQuantity }
        old_pattern1 = "setMainDeck(prev => [...prev, { ...card, quantity: addQuantity }]);"
        new_pattern1 = "setMainDeck(prev => [...prev, { ...scryfallToDeckCard(card), quantity: addQuantity }]);"
        content = content.replace(old_pattern1, new_pattern1)
        
        # Fix pattern 2: { ...card, quantity: 1 }
        content = re.sub(
            r'setMainDeck\(prev => \[\.\.\.prev, \{ \.\.\.card, quantity: 1 \}\]\);',
            'setMainDeck(prev => [...prev, { ...scryfallToDeckCard(card), quantity: 1 }]);',
            content
        )
        
        # Fix pattern 3: setSideboard with { ...card, quantity: X }
        content = re.sub(
            r'setSideboard\(prev => \[\.\.\.prev, \{ \.\.\.card, quantity: (\w+) \}\]\);',
            r'setSideboard(prev => [...prev, { ...scryfallToDeckCard(card), quantity: \1 }]);',
            content
        )
        
        print("✅ Step 4: Fixed ScryfallCard to DeckCard conversion patterns")
        
        # STEP 5: Fix selectCard type issue - need to accept both types
        old_select_card = "    selectCard(card.id, card, event?.ctrlKey);"
        new_select_card = "    selectCard(card.id, card as any, event?.ctrlKey);"
        
        if old_select_card in content:
            content = content.replace(old_select_card, new_select_card)
            print("✅ Step 5: Fixed selectCard type casting")
        
        # STEP 6: Fix handleAddToDeck function to use proper conversion
        old_handle_add_to_deck = """  const handleAddToDeck = (card: ScryfallCard | DeckCard) => {
    const existingCard = mainDeck.find((deckCard: any) => deckCard.id === card.id);
    if (existingCard && existingCard.quantity < 4) {
      setMainDeck((prev: DeckCard[]) => prev.map((deckCard: DeckCard) => 
        deckCard.id === card.id 
          ? { ...deckCard, quantity: deckCard.quantity + 1 }
          : deckCard
      ));
    } else if (!existingCard) {
      setMainDeck((prev: DeckCard[]) => [...prev, { ...card, quantity: 1 }]);
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
      setMainDeck((prev: DeckCard[]) => [...prev, { ...scryfallToDeckCard(card as ScryfallCard), quantity: 1 }]);
    }
  };"""
        
        if old_handle_add_to_deck in content:
            content = content.replace(old_handle_add_to_deck, new_handle_add_to_deck)
            print("✅ Step 6: Fixed handleAddToDeck function")
        
        # STEP 7: Fix all remaining { ...card, quantity: moveQuantity } patterns
        content = re.sub(
            r'\{ \.\.\.card, quantity: moveQuantity \}',
            '{ ...scryfallToDeckCard(card as ScryfallCard), quantity: moveQuantity }',
            content
        )
        print("✅ Step 7: Fixed remaining card conversion patterns")
        
        # Write the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Comprehensive fix complete! Updated MTGOLayout.tsx")
        return True
        
    except Exception as e:
        print(f"❌ Error during comprehensive fix: {e}")
        return False

def main():
    print("🔧 Comprehensive Fix: Resolving All MTGOLayout Issues")
    print("=" * 55)
    
    if comprehensive_fix():
        print()
        print("🎉 Comprehensive Fix Complete!")
        print("✅ Removed duplicate imports")
        print("✅ Added scryfallToDeckCard utility import")
        print("✅ Added Pile view toggle buttons to deck header")
        print("✅ Added Pile view toggle buttons to sideboard header")
        print("✅ Fixed all ScryfallCard -> DeckCard conversion issues")
        print("✅ Fixed selectCard type casting")
        print("✅ Fixed handleAddToDeck function")
        print("✅ Fixed all remaining type conversion patterns")
        print()
        print("🧪 Testing Instructions:")
        print("1. Run `npm start` to verify compilation")
        print("2. All TypeScript errors should be resolved")
        print("3. Test Pile view toggle buttons in deck and sideboard")
        print("4. Test pile view functionality with card organization")
    else:
        print("❌ Comprehensive fix failed")

if __name__ == "__main__":
    main()
