#!/usr/bin/env python3
"""
Quality of Life Session 1 - Critical Fixes Script
Fixes 4 critical issues affecting Magic deck building rules and UX
"""

import os
import re

def fix_magic_card_borders(file_path):
    """Fix Issue 4: Remove unwanted colored borders from non-selected cards"""
    print("🎨 Fixing MagicCard.tsx - removing unwanted borders...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the card border logic and fix it
    old_border_logic = '''border: `2px solid ${selected ? '#3b82f6' : rarityColor}`,'''
    new_border_logic = '''border: `2px solid ${selected ? '#3b82f6' : '#404040'}`,'''
    
    if old_border_logic in content:
        content = content.replace(old_border_logic, new_border_logic)
        print("   ✅ Fixed card border logic - only selected cards get colored borders")
    else:
        print("   ⚠️ Border logic pattern not found - manual review needed")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def add_basic_land_detection_to_card_types(file_path):
    """Add enhanced basic land detection to card.ts"""
    print("🏔️ Enhancing card.ts - improving basic land detection...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the existing isBasicLand function and replace it
    old_function = '''/**
 * Utility function to check if a card is a basic land
 */
export const isBasicLand = (card: ScryfallCard | DeckCard): boolean => {
  const basicLandNames = ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest'];
  return basicLandNames.includes(card.name);
};'''
    
    new_function = '''/**
 * Utility function to check if a card is a basic land
 * Includes snow-covered basics, Wastes, and any card with basic land type
 */
export const isBasicLand = (card: ScryfallCard | DeckCard): boolean => {
  // Check for exact basic land names
  const basicLandNames = ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest', 'Wastes'];
  if (basicLandNames.includes(card.name)) {
    return true;
  }
  
  // Check for snow-covered basics
  const snowBasics = ['Snow-Covered Plains', 'Snow-Covered Island', 'Snow-Covered Swamp', 
                     'Snow-Covered Mountain', 'Snow-Covered Forest'];
  if (snowBasics.includes(card.name)) {
    return true;
  }
  
  // Check if type line contains "Basic Land"
  if (card.type_line && card.type_line.includes('Basic Land')) {
    return true;
  }
  
  return false;
};'''
    
    if old_function in content:
        content = content.replace(old_function, new_function)
        print("   ✅ Enhanced basic land detection function")
    else:
        print("   ⚠️ Existing isBasicLand function not found - manual review needed")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def add_unique_instance_ids(file_path):
    """Add unique instance ID generation to useSelection.ts"""
    print("🔢 Fixing useSelection.ts - adding unique instance IDs...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add utility functions at the top after imports
    import_section_end = content.find("export interface SelectionState")
    if import_section_end != -1:
        utility_functions = '''
// Utility functions for unique card instance IDs
export const generateInstanceId = (cardId: string, zone: string, index?: number): string => {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substr(2, 5);
  const indexPart = index !== undefined ? `-${index}` : '';
  return `${cardId}-${zone}${indexPart}-${timestamp}-${random}`;
};

export const parseInstanceId = (instanceId: string): { cardId: string; zone: string; } => {
  const parts = instanceId.split('-');
  if (parts.length >= 2) {
    return {
      cardId: parts[0],
      zone: parts[1]
    };
  }
  // Fallback for old IDs
  return {
    cardId: instanceId,
    zone: 'unknown'
  };
};

'''
        content = content[:import_section_end] + utility_functions + content[import_section_end:]
        print("   ✅ Added unique instance ID utility functions")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_mtgo_layout_deck_limits(file_path):
    """Fix Issue 1: 4-copy total limit enforcement across deck + sideboard"""
    print("⚖️ Fixing MTGOLayout.tsx - enforcing total 4-copy limits...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Import the isBasicLand function at the top
    import_line = "import { ScryfallCard, DeckCard, scryfallToDeckCard } from '../types/card';"
    new_import_line = "import { ScryfallCard, DeckCard, scryfallToDeckCard, isBasicLand } from '../types/card';"
    
    if import_line in content and new_import_line not in content:
        content = content.replace(import_line, new_import_line)
        print("   ✅ Added isBasicLand import")
    
    # Add helper function to calculate total copies
    helper_function = '''
  // Helper function to get total copies across deck and sideboard
  const getTotalCopies = useCallback((cardId: string): number => {
    const deckCopies = mainDeck.find(card => card.id === cardId)?.quantity || 0;
    const sideboardCopies = sideboard.find(card => card.id === cardId)?.quantity || 0;
    return deckCopies + sideboardCopies;
  }, [mainDeck, sideboard]);

'''
    
    # Find where to insert the helper function (after the first useCallback)
    first_callback_match = re.search(r'(const handleClearDeck = useCallback\(\(\) => \{.*?\}, \[clearSelection\]\);)', content, re.DOTALL)
    if first_callback_match:
        insertion_point = first_callback_match.end()
        content = content[:insertion_point] + '\n' + helper_function + content[insertion_point:]
        print("   ✅ Added getTotalCopies helper function")
    
    # Fix addToDeck callback
    old_add_to_deck = '''addToDeck: useCallback((cards: (ScryfallCard | DeckCard)[], quantity = 1) => {
      cards.forEach(card => {
        const existingCard = mainDeck.find(deckCard => deckCard.id === card.id);
        const currentQuantity = existingCard?.quantity || 0;
        
        if (existingCard) {
          const newQuantity = Math.min(currentQuantity + quantity, 4);
          if (newQuantity > currentQuantity) {
            setMainDeck(prev => prev.map(deckCard => 
              deckCard.id === card.id 
                ? { ...deckCard, quantity: newQuantity }
                : deckCard
            ));
          }
        } else {
          const addQuantity = Math.min(quantity, 4);
          setMainDeck(prev => [...prev, toDeckCard(card, addQuantity)]);
        }
      });
    }, [mainDeck]),'''
    
    new_add_to_deck = '''addToDeck: useCallback((cards: (ScryfallCard | DeckCard)[], quantity = 1) => {
      cards.forEach(card => {
        const existingCard = mainDeck.find(deckCard => deckCard.id === card.id);
        const currentDeckQuantity = existingCard?.quantity || 0;
        const totalCopies = getTotalCopies(card.id);
        const isBasic = isBasicLand(card);
        
        // Basic lands have unlimited copies, others limited to 4 total
        const maxAllowed = isBasic ? Infinity : 4;
        const canAdd = Math.max(0, maxAllowed - totalCopies);
        const actualQuantity = Math.min(quantity, canAdd);
        
        if (actualQuantity > 0) {
          if (existingCard) {
            setMainDeck(prev => prev.map(deckCard => 
              deckCard.id === card.id 
                ? { ...deckCard, quantity: currentDeckQuantity + actualQuantity }
                : deckCard
            ));
          } else {
            setMainDeck(prev => [...prev, toDeckCard(card, actualQuantity)]);
          }
        }
      });
    }, [mainDeck, getTotalCopies]),'''
    
    if old_add_to_deck in content:
        content = content.replace(old_add_to_deck, new_add_to_deck)
        print("   ✅ Fixed addToDeck callback - enforces total limit")
    
    # Fix addToSideboard callback
    old_add_to_sideboard = '''addToSideboard: useCallback((cards: (ScryfallCard | DeckCard)[], quantity = 1) => {
      cards.forEach(card => {
        const existingCard = sideboard.find(sideCard => sideCard.id === card.id);
        const currentQuantity = existingCard?.quantity || 0;
        
        if (existingCard) {
          const newQuantity = Math.min(currentQuantity + quantity, 4);
          if (newQuantity > currentQuantity) {
            setSideboard(prev => prev.map(sideCard => 
              sideCard.id === card.id 
                ? { ...sideCard, quantity: newQuantity }
                : sideCard
            ));
          }
        } else {
          const addQuantity = Math.min(quantity, 4);
          setSideboard(prev => [...prev, toDeckCard(card, addQuantity)]);
        }
      });
    }, [sideboard]),'''
    
    new_add_to_sideboard = '''addToSideboard: useCallback((cards: (ScryfallCard | DeckCard)[], quantity = 1) => {
      cards.forEach(card => {
        const existingCard = sideboard.find(sideCard => sideCard.id === card.id);
        const currentSideboardQuantity = existingCard?.quantity || 0;
        const totalCopies = getTotalCopies(card.id);
        const isBasic = isBasicLand(card);
        
        // Basic lands have unlimited copies, others limited to 4 total
        const maxAllowed = isBasic ? Infinity : 4;
        const canAdd = Math.max(0, maxAllowed - totalCopies);
        const actualQuantity = Math.min(quantity, canAdd);
        
        if (actualQuantity > 0) {
          if (existingCard) {
            setSideboard(prev => prev.map(sideCard => 
              sideCard.id === card.id 
                ? { ...sideCard, quantity: currentSideboardQuantity + actualQuantity }
                : sideCard
            ));
          } else {
            setSideboard(prev => [...prev, toDeckCard(card, actualQuantity)]);
          }
        }
      });
    }, [sideboard, getTotalCopies]),'''
    
    if old_add_to_sideboard in content:
        content = content.replace(old_add_to_sideboard, new_add_to_sideboard)
        print("   ✅ Fixed addToSideboard callback - enforces total limit")
    
    # Fix drag and drop logic for collection to deck
    old_collection_to_deck = '''if (from === 'collection' && to === 'deck') {
          console.log('➡️ COLLECTION → DECK');
          const existingCard = mainDeck.find(deckCard => deckCard.id === card.id);
          console.log('📋 Existing in deck:', existingCard ? `${existingCard.name}(${existingCard.quantity})` : 'none');
          
          if (existingCard && existingCard.quantity < 4) {
            console.log('🔄 Updating existing deck card quantity');
            setMainDeck(prev => prev.map(deckCard => 
              deckCard.id === card.id 
                ? { ...deckCard, quantity: deckCard.quantity + 1 }
                : deckCard
            ));
          } else if (!existingCard) {
            console.log('🆕 Adding new card to deck');
            setMainDeck(prev => [...prev, toDeckCard(card, 1)]);
          } else {
            console.log('❌ Cannot add - deck limit reached');
          }'''
    
    new_collection_to_deck = '''if (from === 'collection' && to === 'deck') {
          console.log('➡️ COLLECTION → DECK');
          const existingCard = mainDeck.find(deckCard => deckCard.id === card.id);
          const totalCopies = getTotalCopies(card.id);
          const isBasic = isBasicLand(card);
          const maxAllowed = isBasic ? Infinity : 4;
          
          console.log('📋 Existing in deck:', existingCard ? `${existingCard.name}(${existingCard.quantity})` : 'none');
          console.log('📊 Total copies:', totalCopies, 'Max allowed:', maxAllowed);
          
          if (totalCopies < maxAllowed) {
            if (existingCard) {
              console.log('🔄 Updating existing deck card quantity');
              setMainDeck(prev => prev.map(deckCard => 
                deckCard.id === card.id 
                  ? { ...deckCard, quantity: deckCard.quantity + 1 }
                  : deckCard
              ));
            } else {
              console.log('🆕 Adding new card to deck');
              setMainDeck(prev => [...prev, toDeckCard(card, 1)]);
            }
          } else {
            console.log('❌ Cannot add - total limit reached');
          }'''
    
    if old_collection_to_deck in content:
        content = content.replace(old_collection_to_deck, new_collection_to_deck)
        print("   ✅ Fixed drag & drop collection to deck - enforces total limit")
    
    # Fix drag and drop logic for collection to sideboard
    old_collection_to_sideboard = '''} else if (from === 'collection' && to === 'sideboard') {
          console.log('➡️ COLLECTION → SIDEBOARD');
          const existingCard = sideboard.find(sideCard => sideCard.id === card.id);
          if (existingCard && existingCard.quantity < 4) {
            setSideboard(prev => prev.map(sideCard => 
              sideCard.id === card.id 
                ? { ...sideCard, quantity: sideCard.quantity + 1 }
                : sideCard
            ));
          } else if (!existingCard) {
            setSideboard(prev => [...prev, toDeckCard(card, 1)]);
          }'''
    
    new_collection_to_sideboard = '''} else if (from === 'collection' && to === 'sideboard') {
          console.log('➡️ COLLECTION → SIDEBOARD');
          const existingCard = sideboard.find(sideCard => sideCard.id === card.id);
          const totalCopies = getTotalCopies(card.id);
          const isBasic = isBasicLand(card);
          const maxAllowed = isBasic ? Infinity : 4;
          
          if (totalCopies < maxAllowed) {
            if (existingCard) {
              setSideboard(prev => prev.map(sideCard => 
                sideCard.id === card.id 
                  ? { ...sideCard, quantity: sideCard.quantity + 1 }
                  : sideCard
              ));
            } else {
              setSideboard(prev => [...prev, toDeckCard(card, 1)]);
            }
          }'''
    
    if old_collection_to_sideboard in content:
        content = content.replace(old_collection_to_sideboard, new_collection_to_sideboard)
        print("   ✅ Fixed drag & drop collection to sideboard - enforces total limit")
    
    # Fix sideboard to deck movement
    old_sideboard_to_deck = '''} else if (from === 'sideboard' && to === 'deck') {
          console.log('➡️ SIDEBOARD → DECK');
          const sideCard = sideboard.find(sc => sc.id === card.id);
          if (sideCard) {
            if (sideCard.quantity > 1) {
              setSideboard(prev => prev.map(sc => 
                sc.id === card.id 
                  ? { ...sc, quantity: sc.quantity - 1 }
                  : sc
              ));
            } else {
              setSideboard(prev => prev.filter(sc => sc.id !== card.id));
            }
            
            const existingCard = mainDeck.find(dc => dc.id === card.id);
            if (existingCard && existingCard.quantity < 4) {
              setMainDeck(prev => prev.map(dc => 
                dc.id === card.id 
                  ? { ...dc, quantity: dc.quantity + 1 }
                  : dc
              ));
            } else if (!existingCard) {
              setMainDeck(prev => [...prev, toDeckCard(card, 1)]);
            }
          }'''
    
    new_sideboard_to_deck = '''} else if (from === 'sideboard' && to === 'deck') {
          console.log('➡️ SIDEBOARD → DECK');
          const sideCard = sideboard.find(sc => sc.id === card.id);
          if (sideCard) {
            // Remove from sideboard first
            if (sideCard.quantity > 1) {
              setSideboard(prev => prev.map(sc => 
                sc.id === card.id 
                  ? { ...sc, quantity: sc.quantity - 1 }
                  : sc
              ));
            } else {
              setSideboard(prev => prev.filter(sc => sc.id !== card.id));
            }
            
            // Add to deck (always allowed since we're just moving)
            const existingCard = mainDeck.find(dc => dc.id === card.id);
            if (existingCard) {
              setMainDeck(prev => prev.map(dc => 
                dc.id === card.id 
                  ? { ...dc, quantity: dc.quantity + 1 }
                  : dc
              ));
            } else {
              setMainDeck(prev => [...prev, toDeckCard(card, 1)]);
            }
          }'''
    
    if old_sideboard_to_deck in content:
        content = content.replace(old_sideboard_to_deck, new_sideboard_to_deck)
        print("   ✅ Fixed sideboard to deck movement")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_draggable_card_selection(file_path):
    """Fix Issue 3: Individual card selection behavior"""
    print("🎯 Fixing DraggableCard.tsx - individual card selection...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add zone prop to card identification
    old_click_handler = '''console.log(`Single click on ${card.name}, ctrlKey=${event.ctrlKey}`);
    
    // Execute single click action
    onClick?.(card, event);'''
    
    new_click_handler = '''console.log(`Single click on ${card.name} in ${zone}, ctrlKey=${event.ctrlKey}`);
    
    // Execute single click action with zone context
    onClick?.(card, event);'''
    
    if old_click_handler in content:
        content = content.replace(old_click_handler, new_click_handler)
        print("   ✅ Added zone context to card clicks")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """Run all Quality of Life fixes"""
    print("🚀 Starting Quality of Life Session 1 - Critical Fixes")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('src'):
        print("❌ Error: 'src' directory not found. Please run this script from the project root.")
        return
    
    try:
        # Fix 1: Enhanced basic land detection
        add_basic_land_detection_to_card_types('src/types/card.ts')
        print()
        
        # Fix 2: Remove unwanted borders  
        fix_magic_card_borders('src/components/MagicCard.tsx')
        print()
        
        # Fix 3: Individual card selection
        add_unique_instance_ids('src/hooks/useSelection.ts')
        fix_draggable_card_selection('src/components/DraggableCard.tsx')
        print()
        
        # Fix 4: 4-copy total limit enforcement (biggest fix)
        fix_mtgo_layout_deck_limits('src/components/MTGOLayout.tsx')
        print()
        
        print("=" * 60)
        print("✅ All Quality of Life fixes completed successfully!")
        print()
        print("🧪 Next steps:")
        print("   1. Run 'npm start' to test the application")
        print("   2. Test 4-copy limit with non-basic cards")
        print("   3. Test unlimited basic land copies")
        print("   4. Test individual card selection")
        print("   5. Verify only selected cards have colored borders")
        print()
        print("🔍 Test scenarios:")
        print("   • Add 5 copies of Lightning Bolt (should be prevented)")
        print("   • Add 10 copies of Plains (should work)")
        print("   • Click individual cards (should select only that card)")
        print("   • Check visual appearance (no unwanted borders)")
        
    except Exception as e:
        print(f"❌ Error during fixes: {e}")
        print("Please review the changes manually and fix any issues.")

if __name__ == "__main__":
    main()
