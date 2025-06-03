#!/usr/bin/env python3
"""
Script to update MTGOLayout.tsx for instance-based architecture
Converts from quantity-based DeckCard arrays to instance-based DeckCardInstance arrays
"""

import re
import os

def update_mtgo_layout():
    file_path = 'src/components/MTGOLayout.tsx'
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Reading {file_path} ({len(content)} characters)")
        
        # 1. Update imports to include new types and utilities
        old_imports = """// Card types import
import { ScryfallCard, DeckCard, scryfallToDeckCard, isBasicLand } from '../types/card';"""
        
        new_imports = """// Card types import
import { ScryfallCard, DeckCard, DeckCardInstance, scryfallToDeckCard, scryfallToDeckInstance, 
         deckCardToDeckInstance, isBasicLand, getTotalCardQuantity, getCardQuantityInZone, 
         removeInstancesForCard } from '../types/card';"""
        
        content = content.replace(old_imports, new_imports)
        print("✅ Updated imports")
        
        # 2. Update state declarations from DeckCard[] to DeckCardInstance[]
        old_state_deck = "const [mainDeck, setMainDeck] = useState<DeckCard[]>([]);"
        new_state_deck = "const [mainDeck, setMainDeck] = useState<DeckCardInstance[]>([]);"
        content = content.replace(old_state_deck, new_state_deck)
        
        old_state_sideboard = "const [sideboard, setSideboard] = useState<DeckCard[]>([]);"
        new_state_sideboard = "const [sideboard, setSideboard] = useState<DeckCardInstance[]>([]);"
        content = content.replace(old_state_sideboard, new_state_sideboard)
        print("✅ Updated state declarations")
        
        # 3. Update getTotalCopies helper to use instance arrays
        old_get_total = """  // Helper function to get total copies across deck and sideboard
  const getTotalCopies = useCallback((cardId: string): number => {
    const deckCopies = mainDeck.find(card => card.id === cardId)?.quantity || 0;
    const sideboardCopies = sideboard.find(card => card.id === cardId)?.quantity || 0;
    return deckCopies + sideboardCopies;
  }, [mainDeck, sideboard]);"""
        
        new_get_total = """  // Helper function to get total copies across deck and sideboard
  const getTotalCopies = useCallback((cardId: string): number => {
    return getTotalCardQuantity(mainDeck, sideboard, cardId);
  }, [mainDeck, sideboard]);
  
  // Helper functions for individual zone quantities
  const getDeckQuantity = useCallback((cardId: string): number => {
    return getCardQuantityInZone(mainDeck, cardId);
  }, [mainDeck]);

  const getSideboardQuantity = useCallback((cardId: string): number => {
    return getCardQuantityInZone(sideboard, cardId);
  }, [sideboard]);"""
        
        content = content.replace(old_get_total, new_get_total)
        print("✅ Updated helper functions")
        
        # 4. Update the main deck management callbacks
        old_add_to_deck = """    addToDeck: useCallback((cards: (ScryfallCard | DeckCard)[], quantity = 1) => {
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
    }, [mainDeck, getTotalCopies]),"""
        
        new_add_to_deck = """    addToDeck: useCallback((cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity = 1) => {
      cards.forEach(card => {
        const cardId = 'cardId' in card ? card.cardId : card.id;
        const totalCopies = getTotalCopies(cardId);
        const isBasic = isBasicLand(card);
        
        // Basic lands have unlimited copies, others limited to 4 total
        const maxAllowed = isBasic ? Infinity : 4;
        const canAdd = Math.max(0, maxAllowed - totalCopies);
        const actualQuantity = Math.min(quantity, canAdd);
        
        if (actualQuantity > 0) {
          // Create individual instances
          const newInstances: DeckCardInstance[] = [];
          for (let i = 0; i < actualQuantity; i++) {
            if ('cardId' in card) {
              // Already a DeckCardInstance
              newInstances.push(deckCardToDeckInstance(card as any, 'deck'));
            } else {
              // ScryfallCard or DeckCard
              newInstances.push(scryfallToDeckInstance(card as ScryfallCard, 'deck'));
            }
          }
          
          setMainDeck(prev => [...prev, ...newInstances]);
        }
      });
    }, [getTotalCopies]),"""
        
        content = content.replace(old_add_to_deck, new_add_to_deck)
        print("✅ Updated addToDeck callback")
        
        # 5. Update removeFromDeck callback
        old_remove_from_deck = """    removeFromDeck: useCallback((cards: (ScryfallCard | DeckCard)[], quantity = 1) => {
      cards.forEach(card => {
        const existingCard = mainDeck.find(deckCard => deckCard.id === card.id);
        if (existingCard) {
          const newQuantity = Math.max(0, existingCard.quantity - quantity);
          if (newQuantity === 0) {
            setMainDeck(prev => prev.filter(deckCard => deckCard.id !== card.id));
          } else {
            setMainDeck(prev => prev.map(deckCard => 
              deckCard.id === card.id 
                ? { ...deckCard, quantity: newQuantity }
                : deckCard
            ));
          }
        }
      });
    }, [mainDeck]),"""
        
        new_remove_from_deck = """    removeFromDeck: useCallback((cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity = 1) => {
      cards.forEach(card => {
        const cardId = 'cardId' in card ? card.cardId : card.id;
        setMainDeck(prev => removeInstancesForCard(prev, cardId, quantity));
      });
    }, []),"""
        
        content = content.replace(old_remove_from_deck, new_remove_from_deck)
        print("✅ Updated removeFromDeck callback")
        
        # 6. Update addToSideboard callback
        old_add_to_sideboard = """    addToSideboard: useCallback((cards: (ScryfallCard | DeckCard)[], quantity = 1) => {
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
    }, [sideboard, getTotalCopies]),"""
        
        new_add_to_sideboard = """    addToSideboard: useCallback((cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity = 1) => {
      cards.forEach(card => {
        const cardId = 'cardId' in card ? card.cardId : card.id;
        const totalCopies = getTotalCopies(cardId);
        const isBasic = isBasicLand(card);
        
        // Basic lands have unlimited copies, others limited to 4 total
        const maxAllowed = isBasic ? Infinity : 4;
        const canAdd = Math.max(0, maxAllowed - totalCopies);
        const actualQuantity = Math.min(quantity, canAdd);
        
        if (actualQuantity > 0) {
          // Create individual instances
          const newInstances: DeckCardInstance[] = [];
          for (let i = 0; i < actualQuantity; i++) {
            if ('cardId' in card) {
              // Already a DeckCardInstance
              newInstances.push(deckCardToDeckInstance(card as any, 'sideboard'));
            } else {
              // ScryfallCard or DeckCard
              newInstances.push(scryfallToDeckInstance(card as ScryfallCard, 'sideboard'));
            }
          }
          
          setSideboard(prev => [...prev, ...newInstances]);
        }
      });
    }, [getTotalCopies]),"""
        
        content = content.replace(old_add_to_sideboard, new_add_to_sideboard)
        print("✅ Updated addToSideboard callback")
        
        # 7. Update removeFromSideboard callback
        old_remove_from_sideboard = """    removeFromSideboard: useCallback((cards: (ScryfallCard | DeckCard)[], quantity = 1) => {
      cards.forEach(card => {
        const existingCard = sideboard.find(sideCard => sideCard.id === card.id);
        if (existingCard) {
          const newQuantity = Math.max(0, existingCard.quantity - quantity);
          if (newQuantity === 0) {
            setSideboard(prev => prev.filter(sideCard => sideCard.id !== card.id));
          } else {
            setSideboard(prev => prev.map(sideCard => 
              sideCard.id === card.id 
                ? { ...sideCard, quantity: newQuantity }
                : sideCard
            ));
          }
        }
      });
    }, [sideboard]),"""
        
        new_remove_from_sideboard = """    removeFromSideboard: useCallback((cards: (ScryfallCard | DeckCard | DeckCardInstance)[], quantity = 1) => {
      cards.forEach(card => {
        const cardId = 'cardId' in card ? card.cardId : card.id;
        setSideboard(prev => removeInstancesForCard(prev, cardId, quantity));
      });
    }, []),"""
        
        content = content.replace(old_remove_from_sideboard, new_remove_from_sideboard)
        print("✅ Updated removeFromSideboard callback")
        
        # 8. Update getDeckQuantity callback to use helper
        old_get_deck_qty = """    getDeckQuantity: useCallback((cardId: string) => {
      return mainDeck.find(card => card.id === cardId)?.quantity || 0;
    }, [mainDeck]),"""
        
        new_get_deck_qty = """    getDeckQuantity: useCallback((cardId: string) => {
      return getDeckQuantity(cardId);
    }, [getDeckQuantity]),"""
        
        content = content.replace(old_get_deck_qty, new_get_deck_qty)
        
        # 9. Update getSideboardQuantity callback to use helper
        old_get_side_qty = """    getSideboardQuantity: useCallback((cardId: string) => {
      return sideboard.find(card => card.id === cardId)?.quantity || 0;
    }, [sideboard]),"""
        
        new_get_side_qty = """    getSideboardQuantity: useCallback((cardId: string) => {
      return getSideboardQuantity(cardId);
    }, [getSideboardQuantity]),"""
        
        content = content.replace(old_get_side_qty, new_get_side_qty)
        print("✅ Updated quantity getter callbacks")
        
        # 10. Update deck/sideboard header quantities to count instances
        old_deck_header = """<h3>Main Deck ({mainDeck.reduce((sum: number, card: any) => sum + card.quantity, 0)} cards)</h3>"""
        new_deck_header = """<h3>Main Deck ({mainDeck.length} cards)</h3>"""
        content = content.replace(old_deck_header, new_deck_header)
        
        old_sideboard_header = """<h3>Sideboard ({sideboard.reduce((sum: number, card: any) => sum + card.quantity, 0)})</h3>"""
        new_sideboard_header = """<h3>Sideboard ({sideboard.length})</h3>"""
        content = content.replace(old_sideboard_header, new_sideboard_header)
        print("✅ Updated header quantity displays")
        
        # 11. Update deck rendering to use instance IDs as keys
        old_deck_render = """{sortedMainDeck.map((deckCard) => (
                    <DraggableCard
                      key={deckCard.id}
                      card={deckCard}"""
        
        new_deck_render = """{sortedMainDeck.map((deckInstance) => (
                    <DraggableCard
                      key={deckInstance.instanceId}
                      card={deckInstance}"""
        
        content = content.replace(old_deck_render, new_deck_render)
        
        # Update the rest of the deck rendering props
        old_deck_props = """                      quantity={deckCard.quantity}
                      selected={isSelected(deckCard.id)}
                      selectable={true}
                      isDragActive={dragState.isDragging}
                      isBeingDragged={dragState.draggedCards.some(dc => dc.id === deckCard.id)}"""
        
        new_deck_props = """                      quantity={1}
                      selected={isSelected(deckInstance.instanceId)}
                      selectable={true}
                      isDragActive={dragState.isDragging}
                      isBeingDragged={dragState.draggedCards.some(dc => 'instanceId' in dc ? dc.instanceId === deckInstance.instanceId : dc.id === deckInstance.cardId)}"""
        
        content = content.replace(old_deck_props, new_deck_props)
        print("✅ Updated deck rendering")
        
        # 12. Update sideboard rendering similarly
        old_side_render = """{sortedSideboard.map((sideCard) => (
                    <DraggableCard
                      key={sideCard.id}
                      card={sideCard}"""
        
        new_side_render = """{sortedSideboard.map((sideInstance) => (
                    <DraggableCard
                      key={sideInstance.instanceId}
                      card={sideInstance}"""
        
        content = content.replace(old_side_render, new_side_render)
        
        old_side_props = """                      quantity={sideCard.quantity}
                      selected={isSelected(sideCard.id)}
                      selectable={true}
                      isDragActive={dragState.isDragging}
                      isBeingDragged={dragState.draggedCards.some(dc => dc.id === sideCard.id)}"""
        
        new_side_props = """                      quantity={1}
                      selected={isSelected(sideInstance.instanceId)}
                      selectable={true}
                      isDragActive={dragState.isDragging}
                      isBeingDragged={dragState.draggedCards.some(dc => 'instanceId' in dc ? dc.instanceId === sideInstance.instanceId : dc.id === sideInstance.cardId)}"""
        
        content = content.replace(old_side_props, new_side_props)
        print("✅ Updated sideboard rendering")
        
        # 13. Update sortedMainDeck and sortedSideboard types
        old_sorted_deck = """  const sortedMainDeck = useMemo((): DeckCard[] => {
    return layout.viewModes.deck === 'pile' ? mainDeck : sortCards(mainDeck, deckSortCriteria, deckSortDirection) as DeckCard[];
  }, [mainDeck, deckSortCriteria, deckSortDirection, layout.viewModes.deck, sortCards]);

  const sortedSideboard = useMemo((): DeckCard[] => {
    return layout.viewModes.sideboard === 'pile' ? sideboard : sortCards(sideboard, sideboardSortCriteria, sideboardSortDirection) as DeckCard[];
  }, [sideboard, sideboardSortCriteria, sideboardSortDirection, layout.viewModes.sideboard, sortCards]);"""
        
        new_sorted_deck = """  const sortedMainDeck = useMemo((): DeckCardInstance[] => {
    return layout.viewModes.deck === 'pile' ? mainDeck : sortCards(mainDeck, deckSortCriteria, deckSortDirection) as DeckCardInstance[];
  }, [mainDeck, deckSortCriteria, deckSortDirection, layout.viewModes.deck, sortCards]);

  const sortedSideboard = useMemo((): DeckCardInstance[] => {
    return layout.viewModes.sideboard === 'pile' ? sideboard : sortCards(sideboard, sideboardSortCriteria, sideboardSortDirection) as DeckCardInstance[];
  }, [sideboard, sideboardSortCriteria, sideboardSortDirection, layout.viewModes.sideboard, sortCards]);"""
        
        content = content.replace(old_sorted_deck, new_sorted_deck)
        print("✅ Updated sorted deck types")
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Successfully updated {file_path}")
        print(f"📄 New file size: {len(content)} characters")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting MTGOLayout.tsx update for instance-based architecture...")
    success = update_mtgo_layout()
    if success:
        print("🎉 Update completed successfully!")
        print("\n📋 Next steps:")
        print("1. Update DraggableCard.tsx to handle instance IDs")
        print("2. Update ListView.tsx and PileView.tsx for instances")
        print("3. Update context menus and drag operations")
        print("4. Test the individual card selection functionality")
    else:
        print("💥 Update failed - please check the errors above")
