#!/usr/bin/env python3
"""
Fix critical MTGOLayout.tsx issues for instance-based architecture
"""

import os
import re

def fix_mtgo_layout():
    file_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    print(f"🔧 Fixing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add getCardId to imports
    if "getCardId" not in content:
        content = re.sub(
            r"(import\s+{[^}]+})\s+from\s+'\.\./types/card';",
            r"\1, getCardId } from '../types/card';",
            content
        )
    
    # Fix the handleCardClick function
    old_handle_card_click = """  const handleCardClick = (card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => {
    if (contextMenuState.visible) {
      hideContextMenu();
    }
    selectCard(card.id, card as any, event?.ctrlKey);
  };"""
    
    new_handle_card_click = """  const handleCardClick = (card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => {
    if (contextMenuState.visible) {
      hideContextMenu();
    }
    selectCard(getCardId(card), card as any, event?.ctrlKey);
  };"""
    
    content = content.replace(old_handle_card_click, new_handle_card_click)
    
    # Fix drag callback signatures and update to handle instances
    content = re.sub(
        r'moveDeckToSideboard: useCallback\(\(cards: \(ScryfallCard \| DeckCard\)\[\]',
        r'moveDeckToSideboard: useCallback((cards: (ScryfallCard | DeckCard | DeckCardInstance)[]',
        content
    )
    
    content = re.sub(
        r'moveSideboardToDeck: useCallback\(\(cards: \(ScryfallCard \| DeckCard\)\[\]',
        r'moveSideboardToDeck: useCallback((cards: (ScryfallCard | DeckCard | DeckCardInstance)[]',
        content
    )
    
    # Replace legacy double-click handler with instance-aware version
    old_handle_add_to_deck = """  // Legacy double-click handler for fallback
  const handleAddToDeck = (card: ScryfallCard | DeckCard) => {
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
    
    new_handle_add_to_deck = """  // Updated double-click handler for instance-based system
  const handleAddToDeck = (card: ScryfallCard | DeckCard | DeckCardInstance) => {
    const cardId = getCardId(card);
    const totalCopies = getTotalCopies(cardId);
    const isBasic = isBasicLand(card);
    const maxAllowed = isBasic ? Infinity : 4;
    
    if (totalCopies < maxAllowed) {
      // Create new instance for deck
      const newInstance = scryfallToDeckInstance(card as ScryfallCard, 'deck');
      setMainDeck(prev => [...prev, newInstance]);
    }
  };"""
    
    content = content.replace(old_handle_add_to_deck, new_handle_add_to_deck)
    
    # Fix console.log statements that access .quantity
    content = re.sub(
        r"console\.log\('📊 BEFORE - MainDeck:', mainDeck\.map\(c => `\${c\.name}\(\${c\.quantity}\)`\)\);",
        r"console.log('📊 BEFORE - MainDeck:', mainDeck.map(c => `${c.name}(1)`));",
        content
    )
    
    content = re.sub(
        r"console\.log\('📊 BEFORE - Sideboard:', sideboard\.map\(c => `\${c\.name}\(\${c\.quantity}\)`\)\);",
        r"console.log('📊 BEFORE - Sideboard:', sideboard.map(c => `${c.name}(1)`));",
        content
    )
    
    content = re.sub(
        r"console\.log\('📊 AFTER - MainDeck:', mainDeck\.map\(c => `\${c\.name}\(\${c\.quantity}\)`\)\);",
        r"console.log('📊 AFTER - MainDeck:', mainDeck.map(c => `${c.name}(1)`));",
        content
    )
    
    content = re.sub(
        r"console\.log\('📊 AFTER - Sideboard:', sideboard\.map\(c => `\${c\.name}\(\${c\.quantity}\)`\)\);",
        r"console.log('📊 AFTER - Sideboard:', sideboard.map(c => `${c.name}(1)`));",
        content
    )
    
    # Fix sortCards function to handle instances
    old_sort_cards = """  const sortCards = useCallback((cards: (ScryfallCard | DeckCard)[], criteria: SortCriteria, direction: 'asc' | 'desc'): (ScryfallCard | DeckCard)[] => {"""
    
    new_sort_cards = """  const sortCards = useCallback((cards: (ScryfallCard | DeckCard | DeckCardInstance)[], criteria: SortCriteria, direction: 'asc' | 'desc'): (ScryfallCard | DeckCard | DeckCardInstance)[] => {"""
    
    content = content.replace(old_sort_cards, new_sort_cards)
    
    # Fix sorted deck memos to not cast types
    content = re.sub(
        r'return layout\.viewModes\.deck === \'pile\' \? mainDeck : sortCards\(mainDeck, deckSortCriteria, deckSortDirection\) as DeckCardInstance\[\];',
        r'return layout.viewModes.deck === \'pile\' ? mainDeck : sortCards(mainDeck, deckSortCriteria, deckSortDirection) as DeckCardInstance[];',
        content
    )
    
    content = re.sub(
        r'return layout\.viewModes\.sideboard === \'pile\' \? sideboard : sortCards\(sideboard, sideboardSortCriteria, sideboardSortDirection\) as DeckCardInstance\[\];',
        r'return layout.viewModes.sideboard === \'pile\' ? sideboard : sortCards(sideboard, sideboardSortCriteria, sideboardSortDirection) as DeckCardInstance[];',
        content
    )
    
    # Fix isBeingDragged check
    content = re.sub(
        r'isBeingDragged=\{dragState\.draggedCards\.some\(dc => dc\.id === card\.id\)\}',
        r'isBeingDragged={dragState.draggedCards.some(dc => getCardId(dc) === getCardId(card))}',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed {file_path}")
    return True

if __name__ == "__main__":
    success = fix_mtgo_layout()
    if success:
        print("🎉 MTGOLayout.tsx critical fixes completed!")
    else:
        print("❌ MTGOLayout fixes failed!")
