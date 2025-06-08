#!/usr/bin/env python3
"""
Phase 4A Session 2: UI Integration for Server-Side Sorting
Integrates MTGOLayout.tsx with enhanced sorting system from Session 1

IMPORTANT: SortCriteria type excludes 'type' for Scryfall API compatibility
- Collection: Support name, mana, color, rarity (no type)
- Deck/Sideboard: Keep existing behavior, handle type gracefully
"""

import os
import sys

def update_mtgo_layout():
    """Update MTGOLayout.tsx to use enhanced sorting system"""
    
    filename = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filename):
        print(f"❌ Error: {filename} not found")
        print("Please run this script from the project root directory (mtg-deck-builder/)")
        return False
    
    print(f"🔧 Updating {filename} with enhanced sorting integration...")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Define all replacements
    updates = [
        # 1. Add enhanced useSorting hook import
        (
            "import { useCards } from '../hooks/useCards';",
            "import { useCards } from '../hooks/useCards';\nimport { useSorting } from '../hooks/useSorting';"
        ),
        
        # 2. Remove old local sort state declarations (lines 132-138)
        (
            """  // Universal sort state for all areas and view modes
  const [collectionSortCriteria, setCollectionSortCriteria] = useState<SortCriteria>('name');
  const [collectionSortDirection, setCollectionSortDirection] = useState<'asc' | 'desc'>('asc');
  const [deckSortCriteria, setDeckSortCriteria] = useState<SortCriteria>('mana');
  const [deckSortDirection, setDeckSortDirection] = useState<'asc' | 'desc'>('asc');
  const [sideboardSortCriteria, setSideboardSortCriteria] = useState<SortCriteria>('mana');
  const [sideboardSortDirection, setSideboardSortDirection] = useState<'asc' | 'desc'>('asc');""",
            """  // Enhanced sorting system - replaces local sort state
  const { updateSort, getSortState } = useSorting();
  
  // Get current sort states from enhanced hook
  const collectionSort = getSortState('collection');
  const deckSort = getSortState('deck');
  const sideboardSort = getSortState('sideboard');"""
        ),
        
        # 3. Update Collection Sort Menu - Name button
        (
            """                    <button 
                      className={collectionSortCriteria === 'name' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSortCriteria === 'name') {
                          setCollectionSortDirection(collectionSortDirection === 'asc' ? 'desc' : 'asc');
                        } else {
                          setCollectionSortCriteria('name'); 
                          setCollectionSortDirection('asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Name {collectionSortCriteria === 'name' ? (collectionSortDirection === 'asc' ? '↑' : '↓') : ''}
                    </button>""",
            """                    <button 
                      className={collectionSort.criteria === 'name' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSort.criteria === 'name') {
                          updateSort('collection', 'name', collectionSort.direction === 'asc' ? 'desc' : 'asc');
                        } else {
                          updateSort('collection', 'name', 'asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Name {collectionSort.criteria === 'name' ? (collectionSort.direction === 'asc' ? '↑' : '↓') : ''}
                    </button>"""
        ),
        
        # 4. Update Collection Sort Menu - Mana button
        (
            """                    <button 
                      className={collectionSortCriteria === 'mana' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSortCriteria === 'mana') {
                          setCollectionSortDirection(collectionSortDirection === 'asc' ? 'desc' : 'asc');
                        } else {
                          setCollectionSortCriteria('mana'); 
                          setCollectionSortDirection('asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Mana Value {collectionSortCriteria === 'mana' ? (collectionSortDirection === 'asc' ? '↑' : '↓') : ''}
                    </button>""",
            """                    <button 
                      className={collectionSort.criteria === 'mana' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSort.criteria === 'mana') {
                          updateSort('collection', 'mana', collectionSort.direction === 'asc' ? 'desc' : 'asc');
                        } else {
                          updateSort('collection', 'mana', 'asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Mana Value {collectionSort.criteria === 'mana' ? (collectionSort.direction === 'asc' ? '↑' : '↓') : ''}
                    </button>"""
        ),
        
        # 5. Update Collection Sort Menu - Color button
        (
            """                    <button 
                      className={collectionSortCriteria === 'color' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSortCriteria === 'color') {
                          setCollectionSortDirection(collectionSortDirection === 'asc' ? 'desc' : 'asc');
                        } else {
                          setCollectionSortCriteria('color'); 
                          setCollectionSortDirection('asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Color {collectionSortCriteria === 'color' ? (collectionSortDirection === 'asc' ? '↑' : '↓') : ''}
                    </button>""",
            """                    <button 
                      className={collectionSort.criteria === 'color' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSort.criteria === 'color') {
                          updateSort('collection', 'color', collectionSort.direction === 'asc' ? 'desc' : 'asc');
                        } else {
                          updateSort('collection', 'color', 'asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Color {collectionSort.criteria === 'color' ? (collectionSort.direction === 'asc' ? '↑' : '↓') : ''}
                    </button>"""
        ),
        
        # 6. Update Collection Sort Menu - Rarity button
        (
            """                    <button 
                      className={collectionSortCriteria === 'rarity' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSortCriteria === 'rarity') {
                          setCollectionSortDirection(collectionSortDirection === 'asc' ? 'desc' : 'asc');
                        } else {
                          setCollectionSortCriteria('rarity'); 
                          setCollectionSortDirection('asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Rarity {collectionSortCriteria === 'rarity' ? (collectionSortDirection === 'asc' ? '↑' : '↓') : ''}
                    </button>""",
            """                    <button 
                      className={collectionSort.criteria === 'rarity' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSort.criteria === 'rarity') {
                          updateSort('collection', 'rarity', collectionSort.direction === 'asc' ? 'desc' : 'asc');
                        } else {
                          updateSort('collection', 'rarity', 'asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Rarity {collectionSort.criteria === 'rarity' ? (collectionSort.direction === 'asc' ? '↑' : '↓') : ''}
                    </button>"""
        ),
        
        # 7. REMOVE Collection Sort Menu - Type button (not supported by enhanced sorting)
        (
            """                    <button 
                      className={collectionSortCriteria === 'type' ? 'active' : ''}
                      onClick={() => { 
                        if (collectionSortCriteria === 'type') {
                          setCollectionSortDirection(collectionSortDirection === 'asc' ? 'desc' : 'asc');
                        } else {
                          setCollectionSortCriteria('type'); 
                          setCollectionSortDirection('asc');
                        }
                        setShowCollectionSortMenu(false); 
                      }}
                    >
                      Card Type {collectionSortCriteria === 'type' ? (collectionSortDirection === 'asc' ? '↑' : '↓') : ''}
                    </button>""",
            """                    {/* Card Type sorting removed - not supported by Scryfall API for server-side sorting */}"""
        ),
        
        # 8. Update sortedCollectionCards useMemo
        (
            """  const sortedCollectionCards = useMemo(() => {
    return sortCards(cards, collectionSortCriteria, collectionSortDirection);
  }, [cards, collectionSortCriteria, collectionSortDirection, sortCards]);""",
            """  const sortedCollectionCards = useMemo(() => {
    return sortCards(cards, collectionSort.criteria, collectionSort.direction);
  }, [cards, collectionSort.criteria, collectionSort.direction, sortCards]);"""
        ),
        
        # 9. Update sortedMainDeck useMemo  
        (
            """  const sortedMainDeck = useMemo((): DeckCardInstance[] => {
    return layout.viewModes.deck === 'pile' ? mainDeck : sortCards(mainDeck as any, deckSortCriteria, deckSortDirection) as DeckCardInstance[];
  }, [mainDeck, deckSortCriteria, deckSortDirection, layout.viewModes.deck, sortCards]);""",
            """  const sortedMainDeck = useMemo((): DeckCardInstance[] => {
    return layout.viewModes.deck === 'pile' ? mainDeck : sortCards(mainDeck as any, deckSort.criteria, deckSort.direction) as DeckCardInstance[];
  }, [mainDeck, deckSort.criteria, deckSort.direction, layout.viewModes.deck, sortCards]);"""
        ),
        
        # 10. Update sortedSideboard useMemo
        (
            """  const sortedSideboard = useMemo((): DeckCardInstance[] => {
    return layout.viewModes.sideboard === 'pile' ? sideboard : sortCards(sideboard as any, sideboardSortCriteria, sideboardSortDirection) as DeckCardInstance[];
  }, [sideboard, sideboardSortCriteria, sideboardSortDirection, layout.viewModes.sideboard, sortCards]);""",
            """  const sortedSideboard = useMemo((): DeckCardInstance[] => {
    return layout.viewModes.sideboard === 'pile' ? sideboard : sortCards(sideboard as any, sideboardSort.criteria, sideboardSort.direction) as DeckCardInstance[];
  }, [sideboard, sideboardSort.criteria, sideboardSort.direction, layout.viewModes.sideboard, sortCards]);"""
        )
    ]
    
    # Apply all updates
    original_content = content
    success_count = 0
    
    for i, (old_str, new_str) in enumerate(updates, 1):
        if old_str in content:
            content = content.replace(old_str, new_str)
            success_count += 1
            print(f"✅ Update {i}: Successfully updated")
        else:
            print(f"❌ Update {i}: Could not find target text")
            print(f"   Looking for: {old_str[:100]}...")
            return False
    
    # Verify we made all expected changes
    if success_count != len(updates):
        print(f"❌ Only {success_count}/{len(updates)} updates succeeded")
        return False
    
    # Write updated content
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False
    
    print(f"✅ Successfully updated {filename}")
    print(f"📊 Applied {success_count} updates for enhanced sorting integration")
    
    return True

def update_deck_sort_buttons():
    """Update deck sort button handlers"""
    
    filename = "src/components/MTGOLayout.tsx"
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Deck sort button updates
    deck_updates = [
        # Deck Sort - Mana button
        (
            """                        className={deckSortCriteria === 'mana' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.deck === 'card' && deckSortCriteria === 'mana') {
                            setDeckSortDirection(deckSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setDeckSortCriteria('mana'); 
                            if (layout.viewModes.deck === 'card') setDeckSortDirection('asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Mana Value {deckSortCriteria === 'mana' && layout.viewModes.deck === 'card' ? (deckSortDirection === 'asc' ? '↑' : '↓') : ''}""",
            """                        className={deckSort.criteria === 'mana' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.deck === 'card' && deckSort.criteria === 'mana') {
                            updateSort('deck', 'mana', deckSort.direction === 'asc' ? 'desc' : 'asc');
                          } else {
                            updateSort('deck', 'mana', 'asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Mana Value {deckSort.criteria === 'mana' && layout.viewModes.deck === 'card' ? (deckSort.direction === 'asc' ? '↑' : '↓') : ''}"""
        ),
        
        # Deck Sort - Color button
        (
            """                        className={deckSortCriteria === 'color' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.deck === 'card' && deckSortCriteria === 'color') {
                            setDeckSortDirection(deckSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setDeckSortCriteria('color'); 
                            if (layout.viewModes.deck === 'card') setDeckSortDirection('asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Color {deckSortCriteria === 'color' && layout.viewModes.deck === 'card' ? (deckSortDirection === 'asc' ? '↑' : '↓') : ''}""",
            """                        className={deckSort.criteria === 'color' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.deck === 'card' && deckSort.criteria === 'color') {
                            updateSort('deck', 'color', deckSort.direction === 'asc' ? 'desc' : 'asc');
                          } else {
                            updateSort('deck', 'color', 'asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Color {deckSort.criteria === 'color' && layout.viewModes.deck === 'card' ? (deckSort.direction === 'asc' ? '↑' : '↓') : ''}"""
        ),
        
        # Deck Sort - Rarity button
        (
            """                        className={deckSortCriteria === 'rarity' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.deck === 'card' && deckSortCriteria === 'rarity') {
                            setDeckSortDirection(deckSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setDeckSortCriteria('rarity'); 
                            if (layout.viewModes.deck === 'card') setDeckSortDirection('asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Rarity {deckSortCriteria === 'rarity' && layout.viewModes.deck === 'card' ? (deckSortDirection === 'asc' ? '↑' : '↓') : ''}""",
            """                        className={deckSort.criteria === 'rarity' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.deck === 'card' && deckSort.criteria === 'rarity') {
                            updateSort('deck', 'rarity', deckSort.direction === 'asc' ? 'desc' : 'asc');
                          } else {
                            updateSort('deck', 'rarity', 'asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Rarity {deckSort.criteria === 'rarity' && layout.viewModes.deck === 'card' ? (deckSort.direction === 'asc' ? '↑' : '↓') : ''}"""
        ),
        
        # Deck Sort - Type button
        (
            """                        className={deckSortCriteria === 'type' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.deck === 'card' && deckSortCriteria === 'type') {
                            setDeckSortDirection(deckSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setDeckSortCriteria('type'); 
                            if (layout.viewModes.deck === 'card') setDeckSortDirection('asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Card Type {deckSortCriteria === 'type' && layout.viewModes.deck === 'card' ? (deckSortDirection === 'asc' ? '↑' : '↓') : ''}""",
            """                        className={deckSort.criteria === 'type' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.deck === 'card' && deckSort.criteria === 'type') {
                            updateSort('deck', 'type', deckSort.direction === 'asc' ? 'desc' : 'asc');
                          } else {
                            updateSort('deck', 'type', 'asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Card Type {deckSort.criteria === 'type' && layout.viewModes.deck === 'card' ? (deckSort.direction === 'asc' ? '↑' : '↓') : ''}"""
        )
    ]
    
    # Apply deck updates
    success_count = 0
    for i, (old_str, new_str) in enumerate(deck_updates, 1):
        if old_str in content:
            content = content.replace(old_str, new_str)
            success_count += 1
            print(f"✅ Deck Update {i}: Successfully updated")
        else:
            print(f"❌ Deck Update {i}: Could not find target text")
            return False
    
    # Write updated content
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False
    
    print(f"✅ Successfully updated deck sort buttons ({success_count} updates)")
    return True

def update_sideboard_sort_buttons():
    """Update sideboard sort button handlers"""
    
    filename = "src/components/MTGOLayout.tsx"
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Sideboard sort button updates
    sideboard_updates = [
        # Sideboard Sort - Mana button
        (
            """                        className={sideboardSortCriteria === 'mana' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSortCriteria === 'mana') {
                            setSideboardSortDirection(sideboardSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setSideboardSortCriteria('mana'); 
                            if (layout.viewModes.sideboard === 'card') setSideboardSortDirection('asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Mana Value {sideboardSortCriteria === 'mana' && layout.viewModes.sideboard === 'card' ? (sideboardSortDirection === 'asc' ? '↑' : '↓') : ''}""",
            """                        className={sideboardSort.criteria === 'mana' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSort.criteria === 'mana') {
                            updateSort('sideboard', 'mana', sideboardSort.direction === 'asc' ? 'desc' : 'asc');
                          } else {
                            updateSort('sideboard', 'mana', 'asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Mana Value {sideboardSort.criteria === 'mana' && layout.viewModes.sideboard === 'card' ? (sideboardSort.direction === 'asc' ? '↑' : '↓') : ''}"""
        ),
        
        # Sideboard Sort - Color button
        (
            """                        className={sideboardSortCriteria === 'color' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSortCriteria === 'color') {
                            setSideboardSortDirection(sideboardSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setSideboardSortCriteria('color'); 
                            if (layout.viewModes.sideboard === 'card') setSideboardSortDirection('asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Color {sideboardSortCriteria === 'color' && layout.viewModes.sideboard === 'card' ? (sideboardSortDirection === 'asc' ? '↑' : '↓') : ''}""",
            """                        className={sideboardSort.criteria === 'color' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSort.criteria === 'color') {
                            updateSort('sideboard', 'color', sideboardSort.direction === 'asc' ? 'desc' : 'asc');
                          } else {
                            updateSort('sideboard', 'color', 'asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Color {sideboardSort.criteria === 'color' && layout.viewModes.sideboard === 'card' ? (sideboardSort.direction === 'asc' ? '↑' : '↓') : ''}"""
        ),
        
        # Sideboard Sort - Rarity button
        (
            """                        className={sideboardSortCriteria === 'rarity' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSortCriteria === 'rarity') {
                            setSideboardSortDirection(sideboardSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setSideboardSortCriteria('rarity'); 
                            if (layout.viewModes.sideboard === 'card') setSideboardSortDirection('asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Rarity {sideboardSortCriteria === 'rarity' && layout.viewModes.sideboard === 'card' ? (sideboardSortDirection === 'asc' ? '↑' : '↓') : ''}""",
            """                        className={sideboardSort.criteria === 'rarity' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSort.criteria === 'rarity') {
                            updateSort('sideboard', 'rarity', sideboardSort.direction === 'asc' ? 'desc' : 'asc');
                          } else {
                            updateSort('sideboard', 'rarity', 'asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Rarity {sideboardSort.criteria === 'rarity' && layout.viewModes.sideboard === 'card' ? (sideboardSort.direction === 'asc' ? '↑' : '↓') : ''}"""
        ),
        
        # Sideboard Sort - Type button
        (
            """                        className={sideboardSortCriteria === 'type' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSortCriteria === 'type') {
                            setSideboardSortDirection(sideboardSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setSideboardSortCriteria('type'); 
                            if (layout.viewModes.sideboard === 'card') setSideboardSortDirection('asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Card Type {sideboardSortCriteria === 'type' && layout.viewModes.sideboard === 'card' ? (sideboardSortDirection === 'asc' ? '↑' : '↓') : ''}""",
            """                        className={sideboardSort.criteria === 'type' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSort.criteria === 'type') {
                            updateSort('sideboard', 'type', sideboardSort.direction === 'asc' ? 'desc' : 'asc');
                          } else {
                            updateSort('sideboard', 'type', 'asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Card Type {sideboardSort.criteria === 'type' && layout.viewModes.sideboard === 'card' ? (sideboardSort.direction === 'asc' ? '↑' : '↓') : ''}"""
        )
    ]
    
    # Apply sideboard updates
    success_count = 0
    for i, (old_str, new_str) in enumerate(sideboard_updates, 1):
        if old_str in content:
            content = content.replace(old_str, new_str)
            success_count += 1
            print(f"✅ Sideboard Update {i}: Successfully updated")
        else:
            print(f"❌ Sideboard Update {i}: Could not find target text")
            return False
    
    # Write updated content
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False
    
    print(f"✅ Successfully updated sideboard sort buttons ({success_count} updates)")
    return True

def update_listview_sort_props():
    """Update ListView sort props to use enhanced sorting"""
    
    filename = "src/components/MTGOLayout.tsx"
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # ListView prop updates
    listview_updates = [
        # Collection ListView props
        (
            """                sortCriteria={collectionSortCriteria}
                sortDirection={collectionSortDirection}
                onSortChange={(criteria, direction) => {
                  setCollectionSortCriteria(criteria);
                  setCollectionSortDirection(direction);
                }}""",
            """                sortCriteria={collectionSort.criteria}
                sortDirection={collectionSort.direction}
                onSortChange={(criteria, direction) => {
                  updateSort('collection', criteria, direction);
                }}"""
        ),
        
        # Deck ListView props
        (
            """                sortCriteria={deckSortCriteria}
                sortDirection={deckSortDirection}
                onSortChange={(criteria, direction) => {
                  setDeckSortCriteria(criteria);
                  setDeckSortDirection(direction);
                }}""",
            """                sortCriteria={deckSort.criteria}
                sortDirection={deckSort.direction}
                onSortChange={(criteria, direction) => {
                  updateSort('deck', criteria, direction);
                }}"""
        ),
        
        # Sideboard ListView props
        (
            """                sortCriteria={sideboardSortCriteria}
                sortDirection={sideboardSortDirection}
                onSortChange={(criteria, direction) => {
                  setSideboardSortCriteria(criteria);
                  setSideboardSortDirection(direction);
                }}""",
            """                sortCriteria={sideboardSort.criteria}
                sortDirection={sideboardSort.direction}
                onSortChange={(criteria, direction) => {
                  updateSort('sideboard', criteria, direction);
                }}"""
        )
    ]
    
    # Apply ListView updates
    success_count = 0
    for i, (old_str, new_str) in enumerate(listview_updates, 1):
        if old_str in content:
            content = content.replace(old_str, new_str)
            success_count += 1
            print(f"✅ ListView Update {i}: Successfully updated")
        else:
            print(f"❌ ListView Update {i}: Could not find target text")
            return False
    
    # Write updated content
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False
    
    print(f"✅ Successfully updated ListView sort props ({success_count} updates)")
    return True

def update_pileview_sort_props():
    """Update PileView forcedSortCriteria props"""
    
    filename = "src/components/MTGOLayout.tsx"
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # PileView prop updates
    pileview_updates = [
        # Deck PileView forcedSortCriteria
        (
            """                  forcedSortCriteria={deckSortCriteria === 'name' ? 'mana' : deckSortCriteria}""",
            """                  forcedSortCriteria={deckSort.criteria === 'name' ? 'mana' : deckSort.criteria}"""
        ),
        
        # Sideboard PileView forcedSortCriteria
        (
            """                  forcedSortCriteria={sideboardSortCriteria === 'name' ? 'mana' : sideboardSortCriteria}""",
            """                  forcedSortCriteria={sideboardSort.criteria === 'name' ? 'mana' : sideboardSort.criteria}"""
        )
    ]
    
    # Apply PileView updates
    success_count = 0
    for i, (old_str, new_str) in enumerate(pileview_updates, 1):
        if old_str in content:
            content = content.replace(old_str, new_str)
            success_count += 1
            print(f"✅ PileView Update {i}: Successfully updated")
        else:
            print(f"❌ PileView Update {i}: Could not find target text")
            return False
    
    # Write updated content
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False
    
    print(f"✅ Successfully updated PileView sort props ({success_count} updates)")
    return True

def main():
    """Run all integration updates"""
    
    print("🚀 Phase 4A Session 2: UI Integration for Server-Side Sorting")
    print("=" * 60)
    print("⚠️  NOTE: 'Card Type' sorting removed from Collection (Scryfall API limitation)")
    print("✅ Collection supports: Name, Mana Value, Color, Rarity")
    print("✅ Deck/Sideboard: Keep all existing sort options")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("src/components/MTGOLayout.tsx"):
        print("❌ MTGOLayout.tsx not found!")
        print("Please run this script from the project root directory:")
        print("cd C:\\Users\\carol\\mtg-deck-builder")
        print("python phase4a_session2_ui_integration.py")
        return False
    
    # Run all updates in sequence
    success = True
    
    print("\n📋 Step 1: Core integration and Collection sort buttons...")
    success &= update_mtgo_layout()
    
    print("\n📋 Step 2: Deck sort buttons...")
    success &= update_deck_sort_buttons()
    
    print("\n📋 Step 3: Sideboard sort buttons...")
    success &= update_sideboard_sort_buttons()
    
    print("\n📋 Step 4: ListView sort props...")
    success &= update_listview_sort_props()
    
    print("\n📋 Step 5: PileView sort props...")
    success &= update_pileview_sort_props()
    
    print("\n" + "=" * 60)
    
    if success:
        print("🎉 UI INTEGRATION COMPLETE!")
        print("\n🔬 TESTING INSTRUCTIONS:")
        print("1. Start the development server: npm start")
        print("2. Search for 'creature' (large result set)")
        print("3. Change collection sort to 'Color' - should see:")
        print("   🔄 Collection sort changed: {criteria: 'color', direction: 'asc'}")
        print("   🔄 Sort change analysis: {shouldUseServerSort: true}")
        print("   🌐 Using server-side sorting - re-searching with new sort parameters")
        print("\n4. Search for 'lightning bolt' (small result set)")
        print("5. Change collection sort to 'Mana Value' - should see:")
        print("   🔄 Collection sort changed: {criteria: 'mana', direction: 'asc'}")
        print("   🔄 Sort change analysis: {shouldUseServerSort: false}")
        print("   🏠 Using client-side sorting - all results already loaded")
        print("\n📋 CHANGES MADE:")
        print("✅ Collection sorting now uses enhanced system (Name, Mana, Color, Rarity)")
        print("❌ Collection 'Card Type' sorting removed (API limitation)")
        print("✅ Deck/Sideboard sorting unchanged (all options preserved)")
        print("✅ Server-side vs client-side logic now active")
        print("✅ Sort state persistence enabled")
        print("\n✅ Enhanced sorting system is now ACTIVE!")
        print("📊 Collection sort changes will now trigger smart re-search logic")
        print("⚡ Large searches use server-side sorting, small searches use client-side")
    else:
        print("❌ Integration failed!")
        print("Please check the error messages above and resolve any issues")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)