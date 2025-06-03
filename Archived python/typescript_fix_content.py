#!/usr/bin/env python3
"""
TypeScript Fix Script: Fix deck card type declarations in MTGOLayout.tsx
Resolves the type mismatch between deck arrays and PileView expected types.
"""

import os

def fix_typescript_deck_types():
    """Fix TypeScript type declarations for mainDeck and sideboard arrays"""
    
    file_path = r'C:\Users\carol\mtg-deckbuilder\src\components\MTGOLayout.tsx'
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Reading MTGOLayout.tsx for TypeScript fixes")
        
        # Step 1: Add DeckCard import to the existing types import
        old_types_import = "import { ScryfallCard, DeckCard } from '../types/card';"
        
        # Check if we need to add the import (it might already be there)
        if "import { ScryfallCard, DeckCard } from '../types/card';" not in content:
            # Find the existing card type import and update it
            if "import { ScryfallCard } from '../types/card';" in content:
                content = content.replace(
                    "import { ScryfallCard } from '../types/card';",
                    "import { ScryfallCard, DeckCard } from '../types/card';"
                )
                print("✅ Step 1: Added DeckCard to types import")
            else:
                print("⚠️ Step 1: Could not find card types import - may need manual addition")
        else:
            print("✅ Step 1: DeckCard import already present")
        
        # Step 2: Fix mainDeck type declaration
        old_main_deck = "  const [mainDeck, setMainDeck] = useState<Array<{ id: string; name: string; quantity: number; [key: string]: any }>>([]);"
        new_main_deck = "  const [mainDeck, setMainDeck] = useState<DeckCard[]>([]);"
        
        if old_main_deck in content:
            content = content.replace(old_main_deck, new_main_deck)
            print("✅ Step 2: Fixed mainDeck type declaration")
        else:
            print("⚠️ Step 2: mainDeck declaration not found exactly - manual check needed")
        
        # Step 3: Fix sideboard type declaration  
        old_sideboard = "  const [sideboard, setSideboard] = useState<Array<{ id: string; name: string; quantity: number; [key: string]: any }>>([]);"
        new_sideboard = "  const [sideboard, setSideboard] = useState<DeckCard[]>([]);"
        
        if old_sideboard in content:
            content = content.replace(old_sideboard, new_sideboard)
            print("✅ Step 3: Fixed sideboard type declaration")
        else:
            print("⚠️ Step 3: sideboard declaration not found exactly - manual check needed")
            
        # Step 4: Fix callback parameter types (there are many 'any' types that can be DeckCard)
        # Fix addToDeck callback
        old_add_to_deck = "    addToDeck: useCallback((cards: (any)[], quantity = 1) => {"
        new_add_to_deck = "    addToDeck: useCallback((cards: (ScryfallCard | DeckCard)[], quantity = 1) => {"
        
        if old_add_to_deck in content:
            content = content.replace(old_add_to_deck, new_add_to_deck)
            print("✅ Step 4a: Fixed addToDeck callback types")
        
        # Fix removeFromDeck callback
        old_remove_from_deck = "    removeFromDeck: useCallback((cards: (any)[], quantity = 1) => {"
        new_remove_from_deck = "    removeFromDeck: useCallback((cards: (ScryfallCard | DeckCard)[], quantity = 1) => {"
        
        if old_remove_from_deck in content:
            content = content.replace(old_remove_from_deck, new_remove_from_deck)
            print("✅ Step 4b: Fixed removeFromDeck callback types")
        
        # Fix addToSideboard callback
        old_add_to_sideboard = "    addToSideboard: useCallback((cards: (any)[], quantity = 1) => {"  
        new_add_to_sideboard = "    addToSideboard: useCallback((cards: (ScryfallCard | DeckCard)[], quantity = 1) => {"
        
        if old_add_to_sideboard in content:
            content = content.replace(old_add_to_sideboard, new_add_to_sideboard)
            print("✅ Step 4c: Fixed addToSideboard callback types")
        
        # Fix removeFromSideboard callback
        old_remove_from_sideboard = "    removeFromSideboard: useCallback((cards: (any)[], quantity = 1) => {"
        new_remove_from_sideboard = "    removeFromSideboard: useCallback((cards: (ScryfallCard | DeckCard)[], quantity = 1) => {"
        
        if old_remove_from_sideboard in content:
            content = content.replace(old_remove_from_sideboard, new_remove_from_sideboard)
            print("✅ Step 4d: Fixed removeFromSideboard callback types")
        
        # Fix moveDeckToSideboard callback
        old_move_deck_to_sideboard = "    moveDeckToSideboard: useCallback((cards: (any)[], quantity = 1) => {"
        new_move_deck_to_sideboard = "    moveDeckToSideboard: useCallback((cards: (ScryfallCard | DeckCard)[], quantity = 1) => {"
        
        if old_move_deck_to_sideboard in content:
            content = content.replace(old_move_deck_to_sideboard, new_move_deck_to_sideboard)
            print("✅ Step 4e: Fixed moveDeckToSideboard callback types")
        
        # Fix moveSideboardToDeck callback
        old_move_sideboard_to_deck = "    moveSideboardToDeck: useCallback((cards: (any)[], quantity = 1) => {"
        new_move_sideboard_to_deck = "    moveSideboardToDeck: useCallback((cards: (ScryfallCard | DeckCard)[], quantity = 1) => {"
        
        if old_move_sideboard_to_deck in content:
            content = content.replace(old_move_sideboard_to_deck, new_move_sideboard_to_deck)
            print("✅ Step 4f: Fixed moveSideboardToDeck callback types")
        
        # Step 5: Fix the legacy handleAddToDeck function
        old_handle_add_to_deck = "  const handleAddToDeck = (card: any) => {"
        new_handle_add_to_deck = "  const handleAddToDeck = (card: ScryfallCard | DeckCard) => {"
        
        if old_handle_add_to_deck in content:
            content = content.replace(old_handle_add_to_deck, new_handle_add_to_deck)
            print("✅ Step 5: Fixed handleAddToDeck function types")
        
        # Step 6: Fix card interaction handlers
        old_handle_card_click = "  const handleCardClick = (card: any, event?: React.MouseEvent) => {"
        new_handle_card_click = "  const handleCardClick = (card: ScryfallCard | DeckCard, event?: React.MouseEvent) => {"
        
        if old_handle_card_click in content:
            content = content.replace(old_handle_card_click, new_handle_card_click)
            print("✅ Step 6: Fixed handleCardClick function types")
        
        # Step 7: Fix map function types in JSX (these are causing the main errors)
        # Fix mainDeck.map type casting
        old_main_deck_map = "                {mainDeck.map((deckCard: any) => ("
        new_main_deck_map = "                {mainDeck.map((deckCard: DeckCard) => ("
        
        if old_main_deck_map in content:
            content = content.replace(old_main_deck_map, new_main_deck_map)
            print("✅ Step 7a: Fixed mainDeck.map type casting")
        
        # Fix sideboard.map type casting
        old_sideboard_map = "                {sideboard.map((sideCard: any) => ("
        new_sideboard_map = "                {sideboard.map((sideCard: DeckCard) => ("
        
        if old_sideboard_map in content:
            content = content.replace(old_sideboard_map, new_sideboard_map)
            print("✅ Step 7b: Fixed sideboard.map type casting")
        
        # Step 8: Fix other 'any' references that should be DeckCard
        # Fix the setMainDeck/setSideboard prev parameters
        old_set_main_deck_prev = "      setMainDeck((prev: any) => prev.map((deckCard: any) =>"
        new_set_main_deck_prev = "      setMainDeck((prev: DeckCard[]) => prev.map((deckCard: DeckCard) =>"
        
        if old_set_main_deck_prev in content:
            content = content.replace(old_set_main_deck_prev, new_set_main_deck_prev)
            print("✅ Step 8a: Fixed setMainDeck prev parameter types")
        
        old_set_main_deck_prev2 = "      setMainDeck((prev: any) => [...prev, { ...card, quantity: 1 }]);"
        new_set_main_deck_prev2 = "      setMainDeck((prev: DeckCard[]) => [...prev, { ...card, quantity: 1 }]);"
        
        if old_set_main_deck_prev2 in content:
            content = content.replace(old_set_main_deck_prev2, new_set_main_deck_prev2)
            print("✅ Step 8b: Fixed setMainDeck spread parameter types")
        
        # Write the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ TypeScript fixes complete! Updated MTGOLayout.tsx")
        return True
        
    except Exception as e:
        print(f"❌ Error during TypeScript fixes: {e}")
        return False

def main():
    print("🔧 TypeScript Fix: Resolving Deck Card Type Issues")
    print("=" * 50)
    
    if fix_typescript_deck_types():
        print()
        print("🎉 TypeScript Fixes Complete!")  
        print("✅ Fixed mainDeck and sideboard type declarations")
        print("✅ Fixed callback function parameter types")
        print("✅ Fixed map function type casting")
        print("✅ Fixed card interaction handler types")
        print()
        print("🧪 Testing Instructions:")
        print("1. Run `npm start` to verify compilation")
        print("2. Check that TypeScript errors are resolved")
        print("3. Test pile view functionality")
    else:
        print("❌ TypeScript fixes failed")

if __name__ == "__main__":
    main()
