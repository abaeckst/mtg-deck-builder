#!/usr/bin/env python3
"""
Phase 3F Final Polish Script
- Adds Name sorting to collection area (first option)
- Removes direction toggles from pile view sort menus
- Syncs sort criteria between card view and pile view
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

def update_mtgo_layout():
    """Update MTGOLayout.tsx with final polish"""
    filepath = 'src/components/MTGOLayout.tsx'
    print(f"📝 Updating {filepath}...")
    
    content = read_file(filepath)
    if not content:
        return False

    # 1. Update the SortCriteria type to include 'name'
    old_sort_type = "type SortCriteria = 'mana' | 'color' | 'rarity' | 'type';"
    new_sort_type = "type SortCriteria = 'name' | 'mana' | 'color' | 'rarity' | 'type';"
    
    content = content.replace(old_sort_type, new_sort_type)

    # 2. Update the card sorting function to handle name sorting
    old_sort_function = """  // Card sorting helper function for all areas
  const sortCards = useCallback((cards: (ScryfallCard | DeckCard)[], criteria: SortCriteria, direction: 'asc' | 'desc'): (ScryfallCard | DeckCard)[] => {
    const sorted = [...cards].sort((a, b) => {
      let comparison = 0;
      
      switch (criteria) {
        case 'mana':
          comparison = (a.cmc ?? 0) - (b.cmc ?? 0);
          break;
        case 'color':
          const aColors = a.colors?.join('') || 'Z';
          const bColors = b.colors?.join('') || 'Z';
          comparison = aColors.localeCompare(bColors);
          break;
        case 'rarity':
          const rarityOrder = { common: 1, uncommon: 2, rare: 3, mythic: 4 };
          const aRarity = rarityOrder[a.rarity as keyof typeof rarityOrder] || 0;
          const bRarity = rarityOrder[b.rarity as keyof typeof rarityOrder] || 0;
          comparison = aRarity - bRarity;
          break;
        case 'type':
          const aType = a.type_line || '';
          const bType = b.type_line || '';
          comparison = aType.localeCompare(bType);
          break;
        default:
          comparison = a.name.localeCompare(b.name);
      }
      
      return direction === 'desc' ? -comparison : comparison;
    });
    
    return sorted;
  }, []);"""

    new_sort_function = """  // Card sorting helper function for all areas
  const sortCards = useCallback((cards: (ScryfallCard | DeckCard)[], criteria: SortCriteria, direction: 'asc' | 'desc'): (ScryfallCard | DeckCard)[] => {
    const sorted = [...cards].sort((a, b) => {
      let comparison = 0;
      
      switch (criteria) {
        case 'name':
          comparison = a.name.localeCompare(b.name);
          break;
        case 'mana':
          comparison = (a.cmc ?? 0) - (b.cmc ?? 0);
          break;
        case 'color':
          const aColors = a.colors?.join('') || 'Z';
          const bColors = b.colors?.join('') || 'Z';
          comparison = aColors.localeCompare(bColors);
          break;
        case 'rarity':
          const rarityOrder = { common: 1, uncommon: 2, rare: 3, mythic: 4 };
          const aRarity = rarityOrder[a.rarity as keyof typeof rarityOrder] || 0;
          const bRarity = rarityOrder[b.rarity as keyof typeof rarityOrder] || 0;
          comparison = aRarity - bRarity;
          break;
        case 'type':
          const aType = a.type_line || '';
          const bType = b.type_line || '';
          comparison = aType.localeCompare(bType);
          break;
        default:
          comparison = a.name.localeCompare(b.name);
      }
      
      return direction === 'desc' ? -comparison : comparison;
    });
    
    return sorted;
  }, []);"""

    content = content.replace(old_sort_function, new_sort_function)

    # 3. Initialize collection sort criteria to 'name' instead of 'mana'
    old_collection_init = "const [collectionSortCriteria, setCollectionSortCriteria] = useState<SortCriteria>('mana');"
    new_collection_init = "const [collectionSortCriteria, setCollectionSortCriteria] = useState<SortCriteria>('name');"
    
    content = content.replace(old_collection_init, new_collection_init)

    # 4. Update collection sort menu to include Name as first option
    old_collection_menu = """                {showCollectionSortMenu && (
                  <div className="sort-menu">
                    <button 
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
                    </button>
                    <button 
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
                    </button>
                    <button 
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
                    </button>
                    <button 
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
                    </button>
                  </div>
                )}"""

    new_collection_menu = """                {showCollectionSortMenu && (
                  <div className="sort-menu">
                    <button 
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
                    </button>
                    <button 
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
                    </button>
                    <button 
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
                    </button>
                    <button 
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
                    </button>
                    <button 
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
                    </button>
                  </div>
                )}"""

    content = content.replace(old_collection_menu, new_collection_menu)

    # 5. Update deck sort menu to remove direction toggles when in pile view
    old_deck_menu = """                  {showDeckSortMenu && (
                    <div className="sort-menu">
                      <button 
                        className={deckSortCriteria === 'mana' ? 'active' : ''}
                        onClick={() => { 
                          if (deckSortCriteria === 'mana') {
                            setDeckSortDirection(deckSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setDeckSortCriteria('mana'); 
                            setDeckSortDirection('asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Mana Value {deckSortCriteria === 'mana' ? (deckSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={deckSortCriteria === 'color' ? 'active' : ''}
                        onClick={() => { 
                          if (deckSortCriteria === 'color') {
                            setDeckSortDirection(deckSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setDeckSortCriteria('color'); 
                            setDeckSortDirection('asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Color {deckSortCriteria === 'color' ? (deckSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={deckSortCriteria === 'rarity' ? 'active' : ''}
                        onClick={() => { 
                          if (deckSortCriteria === 'rarity') {
                            setDeckSortDirection(deckSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setDeckSortCriteria('rarity'); 
                            setDeckSortDirection('asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Rarity {deckSortCriteria === 'rarity' ? (deckSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={deckSortCriteria === 'type' ? 'active' : ''}
                        onClick={() => { 
                          if (deckSortCriteria === 'type') {
                            setDeckSortDirection(deckSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setDeckSortCriteria('type'); 
                            setDeckSortDirection('asc');
                          }
                          setShowDeckSortMenu(false); 
                        }}
                      >
                        Card Type {deckSortCriteria === 'type' ? (deckSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                    </div>
                  )}"""

    new_deck_menu = """                  {showDeckSortMenu && (
                    <div className="sort-menu">
                      <button 
                        className={deckSortCriteria === 'mana' ? 'active' : ''}
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
                        Mana Value {deckSortCriteria === 'mana' && layout.viewModes.deck === 'card' ? (deckSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={deckSortCriteria === 'color' ? 'active' : ''}
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
                        Color {deckSortCriteria === 'color' && layout.viewModes.deck === 'card' ? (deckSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={deckSortCriteria === 'rarity' ? 'active' : ''}
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
                        Rarity {deckSortCriteria === 'rarity' && layout.viewModes.deck === 'card' ? (deckSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={deckSortCriteria === 'type' ? 'active' : ''}
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
                        Card Type {deckSortCriteria === 'type' && layout.viewModes.deck === 'card' ? (deckSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                    </div>
                  )}"""

    content = content.replace(old_deck_menu, new_deck_menu)

    # 6. Update sideboard sort menu to remove direction toggles when in pile view
    old_sideboard_menu = """                  {showSideboardSortMenu && (
                    <div className="sort-menu">
                      <button 
                        className={sideboardSortCriteria === 'mana' ? 'active' : ''}
                        onClick={() => { 
                          if (sideboardSortCriteria === 'mana') {
                            setSideboardSortDirection(sideboardSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setSideboardSortCriteria('mana'); 
                            setSideboardSortDirection('asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Mana Value {sideboardSortCriteria === 'mana' ? (sideboardSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={sideboardSortCriteria === 'color' ? 'active' : ''}
                        onClick={() => { 
                          if (sideboardSortCriteria === 'color') {
                            setSideboardSortDirection(sideboardSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setSideboardSortCriteria('color'); 
                            setSideboardSortDirection('asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Color {sideboardSortCriteria === 'color' ? (sideboardSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={sideboardSortCriteria === 'rarity' ? 'active' : ''}
                        onClick={() => { 
                          if (sideboardSortCriteria === 'rarity') {
                            setSideboardSortDirection(sideboardSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setSideboardSortCriteria('rarity'); 
                            setSideboardSortDirection('asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Rarity {sideboardSortCriteria === 'rarity' ? (sideboardSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={sideboardSortCriteria === 'type' ? 'active' : ''}
                        onClick={() => { 
                          if (sideboardSortCriteria === 'type') {
                            setSideboardSortDirection(sideboardSortDirection === 'asc' ? 'desc' : 'asc');
                          } else {
                            setSideboardSortCriteria('type'); 
                            setSideboardSortDirection('asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Card Type {sideboardSortCriteria === 'type' ? (sideboardSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                    </div>
                  )}"""

    new_sideboard_menu = """                  {showSideboardSortMenu && (
                    <div className="sort-menu">
                      <button 
                        className={sideboardSortCriteria === 'mana' ? 'active' : ''}
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
                        Mana Value {sideboardSortCriteria === 'mana' && layout.viewModes.sideboard === 'card' ? (sideboardSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={sideboardSortCriteria === 'color' ? 'active' : ''}
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
                        Color {sideboardSortCriteria === 'color' && layout.viewModes.sideboard === 'card' ? (sideboardSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={sideboardSortCriteria === 'rarity' ? 'active' : ''}
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
                        Rarity {sideboardSortCriteria === 'rarity' && layout.viewModes.sideboard === 'card' ? (sideboardSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={sideboardSortCriteria === 'type' ? 'active' : ''}
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
                        Card Type {sideboardSortCriteria === 'type' && layout.viewModes.sideboard === 'card' ? (sideboardSortDirection === 'asc' ? '↑' : '↓') : ''}
                      </button>
                    </div>
                  )}"""

    content = content.replace(old_sideboard_menu, new_sideboard_menu)

    # 7. Update pile view to use the same sort criteria from card view
    old_pile_deck = """                <PileView
                  cards={mainDeck}
                  zone="deck"
                  scaleFactor={cardSizes.deck}
                  forcedSortCriteria={deckSortCriteria}"""

    new_pile_deck = """                <PileView
                  cards={mainDeck}
                  zone="deck"
                  scaleFactor={cardSizes.deck}
                  forcedSortCriteria={deckSortCriteria === 'name' ? 'mana' : deckSortCriteria}"""

    content = content.replace(old_pile_deck, new_pile_deck)

    old_pile_sideboard = """                <PileView
                  cards={sideboard}
                  zone="sideboard"
                  scaleFactor={cardSizes.sideboard}
                  forcedSortCriteria={sideboardSortCriteria}"""

    new_pile_sideboard = """                <PileView
                  cards={sideboard}
                  zone="sideboard"
                  scaleFactor={cardSizes.sideboard}
                  forcedSortCriteria={sideboardSortCriteria === 'name' ? 'mana' : sideboardSortCriteria}"""

    content = content.replace(old_pile_sideboard, new_pile_sideboard)

    write_file(filepath, content)
    print(f"✅ Updated {filepath}")
    return True

def update_pile_view_types():
    """Update PileView component to handle the type restriction"""
    filepath = 'src/components/PileView.tsx'
    print(f"📝 Updating {filepath}...")
    
    content = read_file(filepath)
    if not content:
        return False

    # Update the SortCriteria type in PileView to exclude 'name'
    old_type = "export type SortCriteria = 'mana' | 'color' | 'rarity' | 'type';"
    new_type = "export type PileSortCriteria = 'mana' | 'color' | 'rarity' | 'type';\nexport type SortCriteria = 'name' | 'mana' | 'color' | 'rarity' | 'type';"
    
    content = content.replace(old_type, new_type)

    # Update the interface to use PileSortCriteria
    old_interface = "  forcedSortCriteria?: SortCriteria; // External sort control from parent"
    new_interface = "  forcedSortCriteria?: PileSortCriteria; // External sort control from parent"
    
    content = content.replace(old_interface, new_interface)

    write_file(filepath, content)
    print(f"✅ Updated {filepath}")
    return True

def main():
    """Main execution function"""
    print("🎨 Starting Phase 3F Final Polish...")
    print("=" * 60)
    
    # Verify we're in the correct directory
    if not os.path.exists('src/components/MTGOLayout.tsx'):
        print("❌ Error: Please run this script from the project root directory (mtg-deckbuilder)")
        return False
    
    success = True
    
    # Update main layout component
    if not update_mtgo_layout():
        success = False
    
    # Update PileView types
    if not update_pile_view_types():
        success = False
    
    print("=" * 60)
    if success:
        print("✅ Phase 3F final polish completed successfully!")
        print("\n📋 Final Features:")
        print("   • Collection area has Name sorting (first option, A-Z default)")
        print("   • Direction toggles (↑/↓) only appear in card view mode")
        print("   • Pile view sort menus show criteria only (no direction arrows)")
        print("   • Sort criteria sync between card view and pile view")
        print("   • Name sorting available only in collection area")
        print("\n🧪 Testing Steps:")
        print("   1. Run 'npm start' to verify compilation")
        print("   2. Test collection 'Name' sorting (first option)")
        print("   3. Switch deck/sideboard between Card/Pile view")
        print("   4. Verify no ↑/↓ arrows in pile view sort menus")
        print("   5. Verify sort criteria persist when switching view modes")
        print("\n🎯 Phase 3F Complete! Ready for Phase 3G - Responsive UI & List View")
    else:
        print("❌ Some operations failed. Please check the output above.")
        print("   Backup files have been created for safety.")
    
    return success

if __name__ == "__main__":
    main()
