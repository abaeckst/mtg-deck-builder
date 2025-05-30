#!/usr/bin/env python3
"""
Phase 3F Quick Fix Script
Fixes the missing useMemo import and TypeScript errors
"""

import os

def read_file(filepath):
    """Read file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return None

def write_file(filepath, content):
    """Write content to file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_mtgo_layout():
    """Fix the MTGOLayout.tsx import and TypeScript issues"""
    filepath = 'src/components/MTGOLayout.tsx'
    print(f"🔧 Fixing {filepath}...")
    
    content = read_file(filepath)
    if not content:
        return False

    # 1. Add useMemo to the React imports
    old_import = "import React, { useState, useCallback, useEffect, useRef } from 'react';"
    new_import = "import React, { useState, useCallback, useEffect, useRef, useMemo } from 'react';"
    
    content = content.replace(old_import, new_import)

    # 2. Fix the TypeScript error for the collection map function
    old_collection_map = """{sortedCollectionCards.map(card => (
              <DraggableCard
                key={card.id}
                card={card}"""

    new_collection_map = """{sortedCollectionCards.map((card: ScryfallCard | DeckCard) => (
              <DraggableCard
                key={card.id}
                card={card}"""

    content = content.replace(old_collection_map, new_collection_map)

    # 3. Fix the sorted deck memoization to ensure proper typing
    old_deck_memo = """  const sortedMainDeck = useMemo(() => {
    return layout.viewModes.deck === 'pile' ? mainDeck : sortCards(mainDeck, deckSortCriteria, deckSortDirection);
  }, [mainDeck, deckSortCriteria, deckSortDirection, layout.viewModes.deck, sortCards]);"""

    new_deck_memo = """  const sortedMainDeck = useMemo((): DeckCard[] => {
    return layout.viewModes.deck === 'pile' ? mainDeck : sortCards(mainDeck, deckSortCriteria, deckSortDirection) as DeckCard[];
  }, [mainDeck, deckSortCriteria, deckSortDirection, layout.viewModes.deck, sortCards]);"""

    content = content.replace(old_deck_memo, new_deck_memo)

    # 4. Fix the sorted sideboard memoization to ensure proper typing
    old_sideboard_memo = """  const sortedSideboard = useMemo(() => {
    return layout.viewModes.sideboard === 'pile' ? sideboard : sortCards(sideboard, sideboardSortCriteria, sideboardSortDirection);
  }, [sideboard, sideboardSortCriteria, sideboardSortDirection, layout.viewModes.sideboard, sortCards]);"""

    new_sideboard_memo = """  const sortedSideboard = useMemo((): DeckCard[] => {
    return layout.viewModes.sideboard === 'pile' ? sideboard : sortCards(sideboard, sideboardSortCriteria, sideboardSortDirection) as DeckCard[];
  }, [sideboard, sideboardSortCriteria, sideboardSortDirection, layout.viewModes.sideboard, sortCards]);"""

    content = content.replace(old_sideboard_memo, new_sideboard_memo)

    # 5. Fix the deck map function parameter typing
    old_deck_map = """{sortedMainDeck.map((deckCard: DeckCard) => ("""
    new_deck_map = """{sortedMainDeck.map((deckCard) => ("""

    content = content.replace(old_deck_map, new_deck_map)

    # 6. Fix the sideboard map function parameter typing
    old_sideboard_map = """{sortedSideboard.map((sideCard: DeckCard) => ("""
    new_sideboard_map = """{sortedSideboard.map((sideCard) => ("""

    content = content.replace(old_sideboard_map, new_sideboard_map)

    write_file(filepath, content)
    print(f"✅ Fixed {filepath}")
    return True

def main():
    """Main execution function"""
    print("🔧 Fixing Phase 3F TypeScript errors...")
    print("=" * 50)
    
    # Verify we're in the correct directory
    if not os.path.exists('src/components/MTGOLayout.tsx'):
        print("❌ Error: Please run this script from the project root directory (mtg-deckbuilder)")
        return False
    
    success = fix_mtgo_layout()
    
    print("=" * 50)
    if success:
        print("✅ Phase 3F fixes applied successfully!")
        print("\n🧪 Now test with: npm start")
        print("   The compilation errors should be resolved.")
    else:
        print("❌ Fix operation failed.")
    
    return success

if __name__ == "__main__":
    main()
