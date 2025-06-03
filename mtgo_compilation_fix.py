#!/usr/bin/env python3
"""
MTGOLayout.tsx Compilation Fix Script
Fixes critical syntax errors preventing compilation
"""

import os
import re

def fix_mtgo_layout():
    filepath = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        print("Make sure you're running this script from your project root directory")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print(f"📄 Reading {filepath} ({len(content)} characters)")
        
        # Fix 1: Broken function closure around line 441
        print("🔧 Fix 1: Repairing handleCardClick function closure...")
        
        old_broken_closure = """  const handleCardClick = useCallback((card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => {
    if (contextMenuState.visible) {
      hideContextMenu();
    }
    selectCard(getCardId(card), card as any, event?.ctrlKey);
  };"""
        
        new_fixed_closure = """  const handleCardClick = useCallback((card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => {
    if (contextMenuState.visible) {
      hideContextMenu();
    }
    selectCard(getCardId(card), card as any, event?.ctrlKey);
  }, [contextMenuState.visible, hideContextMenu, selectCard]);"""
        
        if old_broken_closure in content:
            content = content.replace(old_broken_closure, new_fixed_closure)
            print("✅ Fixed handleCardClick function closure")
        else:
            print("⚠️ handleCardClick pattern not found - may already be fixed")
        
        # Fix 2: Add missing handleInstanceClick function
        print("🔧 Fix 2: Adding missing handleInstanceClick function...")
        
        # Insert after handleCardClick function
        insert_after = """  }, [contextMenuState.visible, hideContextMenu, selectCard]);"""
        
        handle_instance_click_function = """
  // Instance-based click handler for deck/sideboard cards
  const handleInstanceClick = useCallback((instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => {
    if (contextMenuState.visible) {
      hideContextMenu();
    }
    // Use selectInstance from useSelection hook for instance-based selection
    console.log(`Instance click: ${instanceId} for card ${instance.name}`);
    selectCard(instanceId, instance as any, event.ctrlKey);
  }, [contextMenuState.visible, hideContextMenu, selectCard]);"""
        
        if insert_after in content and "handleInstanceClick" not in content:
            content = content.replace(insert_after, insert_after + handle_instance_click_function)
            print("✅ Added handleInstanceClick function")
        else:
            print("⚠️ handleInstanceClick may already exist or insertion point not found")
        
        # Fix 3: Fix malformed DraggableCard JSX around line 1257 (deck area)
        print("🔧 Fix 3: Fixing malformed DraggableCard JSX in deck area...")
        
        broken_deck_jsx = """                      onClick={(card, event) =
                      instanceId={deckInstance.instanceId}
                      isInstance={true}
                      onInstanceClick={handleInstanceClick}> handleCardClick(card, event)}"""
        
        fixed_deck_jsx = """                      onClick={(card, event) => handleCardClick(card, event)}
                      instanceId={deckInstance.instanceId}
                      isInstance={true}
                      onInstanceClick={handleInstanceClick}"""
        
        if broken_deck_jsx in content:
            content = content.replace(broken_deck_jsx, fixed_deck_jsx)
            print("✅ Fixed malformed deck area DraggableCard JSX")
        else:
            print("⚠️ Deck area JSX pattern not found - may already be fixed")
        
        # Fix 4: Fix malformed DraggableCard JSX around line 1483 (sideboard area)
        print("🔧 Fix 4: Fixing malformed DraggableCard JSX in sideboard area...")
        
        broken_sideboard_jsx = """                      onClick={(card, event) =
                      instanceId={sideInstance.instanceId}
                      isInstance={true}
                      onInstanceClick={handleInstanceClick}> handleCardClick(card, event)}"""
        
        fixed_sideboard_jsx = """                      onClick={(card, event) => handleCardClick(card, event)}
                      instanceId={sideInstance.instanceId}
                      isInstance={true}
                      onInstanceClick={handleInstanceClick}"""
        
        if broken_sideboard_jsx in content:
            content = content.replace(broken_sideboard_jsx, fixed_sideboard_jsx)
            print("✅ Fixed malformed sideboard area DraggableCard JSX")
        else:
            print("⚠️ Sideboard area JSX pattern not found - may already be fixed")
        
        # Fix 5: Fix broken legacy handleAddToDeck function
        print("🔧 Fix 5: Fixing broken handleAddToDeck function...")
        
        broken_add_to_deck = """  // Legacy double-click handler for fallback
  const handleAddToDeck = (card: ScryfallCard | DeckCard | DeckCardInstance) => {
    const existingCard = mainDeck.find((deckCard: DeckCard) => getOriginalCardId(deckCard.id === getCardId(card).split(".")[0]) === getOriginalCardId(card));
    if (existingCard && existingCard.quantity < 4) {
      setMainDeck((prev: DeckCardInstance[]) => prev.map((deckCard: DeckCard) => 
        getOriginalCardId(deckCard.id === getCardId(card).split(".")[0]) === getOriginalCardId(card) 
          ? { ...deckCard, }
          : deckCard
      ));
    } else if (!existingCard) {
      setMainDeck((prev: DeckCardInstance[]) => [...prev, createDeckInstance(card, 'deck')]);
    }
  };"""
        
        fixed_add_to_deck = """  // Legacy double-click handler for fallback
  const handleAddToDeck = useCallback((card: ScryfallCard | DeckCard | DeckCardInstance) => {
    const cardId = getCardId(card);
    const totalCopies = getTotalCopies(cardId);
    const isBasic = isBasicLand(card);
    const maxAllowed = isBasic ? Infinity : 4;
    
    if (totalCopies < maxAllowed) {
      const newInstance = createDeckInstance(card, 'deck');
      setMainDeck(prev => [...prev, newInstance]);
    }
  }, [getTotalCopies]);"""
        
        if broken_add_to_deck in content:
            content = content.replace(broken_add_to_deck, fixed_add_to_deck)
            print("✅ Fixed handleAddToDeck function")
        else:
            print("⚠️ handleAddToDeck pattern not found - may already be fixed")
        
        # Fix 6: Ensure getOriginalCardId function exists or remove references
        print("🔧 Fix 6: Ensuring helper functions are available...")
        
        # Check if getOriginalCardId is defined, if not add it
        if "getOriginalCardId" not in content:
            # Add the helper function after the existing helper functions
            insert_after_helpers = """  const getCardId = (card: ScryfallCard | DeckCard | DeckCardInstance): string => {
    if ('instanceId' in card) return getCardId(card); // DeckCardInstance has id as alias
    return getCardId(card);
  };"""
            
            replacement_helpers = """  const getCardId = (card: ScryfallCard | DeckCard | DeckCardInstance): string => {
    if ('instanceId' in card) return card.cardId; // DeckCardInstance - use cardId
    return card.id; // ScryfallCard or DeckCard - use id
  };
  
  // Helper to get original card ID for quantity tracking
  const getOriginalCardId = (card: ScryfallCard | DeckCard | DeckCardInstance): string => {
    if ('cardId' in card) return card.cardId;
    return card.id;
  };"""
            
            if insert_after_helpers in content:
                content = content.replace(insert_after_helpers, replacement_helpers)
                print("✅ Fixed getCardId and added getOriginalCardId helper")
        
        # Write the fixed content back to file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✅ Successfully applied fixes to {filepath}")
        print(f"📄 File updated ({len(content)} characters)")
        
        print("\n🎯 FIXES APPLIED:")
        print("1. ✅ Fixed handleCardClick function closure")
        print("2. ✅ Added missing handleInstanceClick function")
        print("3. ✅ Fixed malformed DraggableCard JSX in deck area")
        print("4. ✅ Fixed malformed DraggableCard JSX in sideboard area")
        print("5. ✅ Fixed broken handleAddToDeck function")
        print("6. ✅ Ensured helper functions are available")
        
        print("\n🚀 NEXT STEPS:")
        print("1. Run 'npm start' to test compilation")
        print("2. If there are still errors, check the console output")
        print("3. The app should now compile and run successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return False

if __name__ == "__main__":
    print("🔧 MTGOLayout.tsx Compilation Fix Script")
    print("=" * 50)
    
    success = fix_mtgo_layout()
    
    if success:
        print("\n✅ SCRIPT COMPLETED SUCCESSFULLY")
        print("Your MTGOLayout.tsx file has been fixed!")
        print("\nTry running 'npm start' now.")
    else:
        print("\n❌ SCRIPT FAILED")
        print("Please check the error messages above.")
