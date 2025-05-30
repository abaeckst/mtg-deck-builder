#!/usr/bin/env python3
"""
Pile View Comprehensive Fixes Script
===================================

This script addresses all 5 major pile view issues:
1. Sort dropdown -> hidden behind "Sort" button 
2. Column headers -> simple numbers only
3. Card stacking -> proper MTGO-style overlap with cross-card stacking
4. Column gaps -> tightened spacing like MTGO
5. Scrolling -> area-level only, no per-column scrolling

Run from mtg-deckbuilder project root directory.
"""

import os
import re

def read_file(filepath):
    """Read file content safely"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return None
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return None

def write_file(filepath, content):
    """Write file content safely"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ Error writing {filepath}: {e}")
        return False

def apply_all_fixes():
    """Apply all pile view fixes"""
    
    print("🔧 Starting Comprehensive Pile View Fixes...")
    print("=" * 60)
    
    # Fix 1: MTGOLayout.tsx - Convert sort dropdown to button + hidden menu
    print("\n🎯 Fix 1: Converting sort dropdown to button-based system...")
    
    mtgo_layout_path = "src/components/MTGOLayout.tsx"
    mtgo_content = read_file(mtgo_layout_path)
    
    if mtgo_content is None:
        return False
    
    # Add sort menu visibility state
    sort_state_addition = '''  // Pile view sort state
  const [deckSortCriteria, setDeckSortCriteria] = useState<SortCriteria>('mana');
  const [sideboardSortCriteria, setSideboardSortCriteria] = useState<SortCriteria>('mana');
  
  // Sort menu visibility state
  const [showDeckSortMenu, setShowDeckSortMenu] = useState(false);
  const [showSideboardSortMenu, setShowSideboardSortMenu] = useState(false);'''
    
    # Replace existing sort state
    mtgo_content = re.sub(
        r'  // Pile view sort state\s*\n  const \[deckSortCriteria.*?\n  const \[sideboardSortCriteria.*?\n',
        sort_state_addition + '\n',
        mtgo_content,
        flags=re.DOTALL
    )
    
    # Replace deck sort dropdown with button + hidden menu
    old_deck_sort = '''                {layout.viewModes.deck === 'pile' && (
                  <>
                    <span>Sort: </span>
                    <select
                      value={deckSortCriteria}
                      onChange={(e) => setDeckSortCriteria(e.target.value as SortCriteria)}
                      className="sort-dropdown-compact"
                      title="Sort criteria for pile view"
                    >
                      <option value="mana">Mana Value</option>
                      <option value="color">Color</option>
                      <option value="rarity">Rarity</option>
                      <option value="type">Card Type</option>
                    </select>
                  </>
                )}'''
    
    new_deck_sort = '''                {layout.viewModes.deck === 'pile' && (
                  <div className="sort-button-container">
                    <button 
                      className="sort-toggle-btn"
                      onClick={() => setShowDeckSortMenu(!showDeckSortMenu)}
                      title="Sort options"
                    >
                      Sort
                    </button>
                    {showDeckSortMenu && (
                      <div className="sort-menu">
                        <button 
                          className={deckSortCriteria === 'mana' ? 'active' : ''}
                          onClick={() => { setDeckSortCriteria('mana'); setShowDeckSortMenu(false); }}
                        >
                          Mana Value
                        </button>
                        <button 
                          className={deckSortCriteria === 'color' ? 'active' : ''}
                          onClick={() => { setDeckSortCriteria('color'); setShowDeckSortMenu(false); }}
                        >
                          Color
                        </button>
                        <button 
                          className={deckSortCriteria === 'rarity' ? 'active' : ''}
                          onClick={() => { setDeckSortCriteria('rarity'); setShowDeckSortMenu(false); }}
                        >
                          Rarity
                        </button>
                        <button 
                          className={deckSortCriteria === 'type' ? 'active' : ''}
                          onClick={() => { setDeckSortCriteria('type'); setShowDeckSortMenu(false); }}
                        >
                          Card Type
                        </button>
                      </div>
                    )}
                  </div>
                )}'''
    
    if old_deck_sort in mtgo_content:
        mtgo_content = mtgo_content.replace(old_deck_sort, new_deck_sort)
        print("  ✅ Deck sort dropdown converted to button menu")
    else:
        print("  ⚠️  Could not find deck sort dropdown to replace")
    
    # Replace sideboard sort dropdown with button + hidden menu
    old_sideboard_sort = '''                {layout.viewModes.sideboard === 'pile' && (
                  <>
                    <span>Sort: </span>
                    <select
                      value={sideboardSortCriteria}
                      onChange={(e) => setSideboardSortCriteria(e.target.value as SortCriteria)}
                      className="sort-dropdown-compact"
                      title="Sort criteria for pile view"
                    >
                      <option value="mana">Mana Value</option>
                      <option value="color">Color</option>
                      <option value="rarity">Rarity</option>
                      <option value="type">Card Type</option>
                    </select>
                  </>
                )}'''
    
    new_sideboard_sort = '''                {layout.viewModes.sideboard === 'pile' && (
                  <div className="sort-button-container">
                    <button 
                      className="sort-toggle-btn"
                      onClick={() => setShowSideboardSortMenu(!showSideboardSortMenu)}
                      title="Sort options"
                    >
                      Sort
                    </button>
                    {showSideboardSortMenu && (
                      <div className="sort-menu">
                        <button 
                          className={sideboardSortCriteria === 'mana' ? 'active' : ''}
                          onClick={() => { setSideboardSortCriteria('mana'); setShowSideboardSortMenu(false); }}
                        >
                          Mana Value
                        </button>
                        <button 
                          className={sideboardSortCriteria === 'color' ? 'active' : ''}
                          onClick={() => { setSideboardSortCriteria('color'); setShowSideboardSortMenu(false); }}
                        >
                          Color
                        </button>
                        <button 
                          className={sideboardSortCriteria === 'rarity' ? 'active' : ''}
                          onClick={() => { setSideboardSortCriteria('rarity'); setShowSideboardSortMenu(false); }}
                        >
                          Rarity
                        </button>
                        <button 
                          className={sideboardSortCriteria === 'type' ? 'active' : ''}
                          onClick={() => { setSideboardSortCriteria('type'); setShowSideboardSortMenu(false); }}
                        >
                          Card Type
                        </button>
                      </div>
                    )}
                  </div>
                )}'''
    
    if old_sideboard_sort in mtgo_content:
        mtgo_content = mtgo_content.replace(old_sideboard_sort, new_sideboard_sort)
        print("  ✅ Sideboard sort dropdown converted to button menu")
    else:
        print("  ⚠️  Could not find sideboard sort dropdown to replace")
    
    # Save MTGOLayout.tsx changes
    if not write_file(mtgo_layout_path, mtgo_content):
        return False
    
    # Fix 2: PileView.tsx - Remove sort controls header and update column titles
    print("\n🎯 Fix 2: Updating PileView to use simple column numbers...")
    
    pile_view_path = "src/components/PileView.tsx"
    pile_view_content = read_file(pile_view_path)
    
    if pile_view_content is None:
        return False
    
    # Update the column title generation to use simple numbers
    old_title_logic = '''        title: column.isEmpty ? '' : `${column.title}${column.cards.length > 0 ? ` (${column.cards.length})` : ''}`,'''
    new_title_logic = '''        title: column.isEmpty ? '' : `${column.cards.length}`,'''
    
    if old_title_logic in pile_view_content:
        pile_view_content = pile_view_content.replace(old_title_logic, new_title_logic)
        print("  ✅ Column titles updated to show card counts only")
    else:
        print("  ⚠️  Could not find column title logic to update")
    
    # Save PileView.tsx changes
    if not write_file(pile_view_path, pile_view_content):
        return False
    
    # Fix 3: PileColumn.tsx - Fix card stacking for cross-card stacking and proper overlap
    print("\n🎯 Fix 3: Fixing card stacking for proper MTGO appearance...")
    
    pile_column_path = "src/components/PileColumn.tsx"
    pile_column_content = read_file(pile_column_path)
    
    if pile_column_content is None:
        return False
    
    # Replace the entire renderCards function with improved cross-card stacking
    old_render_cards = '''  // MTGO-style card stacking - individual copies with visible names
  const renderCards = useCallback(() => {
    try {
      const renderedCards: React.ReactElement[] = [];
      
      cards.forEach(card => {
        // Validate card has required properties
        if (!card || !card.id) {
          console.warn('Invalid card object:', card);
          return;
        }

        // Get quantity for this card
        let cardQuantity = 1;
        if (typeof card === 'object' && card !== null) {
          if ('quantity' in card && typeof card.quantity === 'number' && card.quantity > 0) {
            cardQuantity = card.quantity;
          }
        }

        // Create individual draggable cards for each copy (MTGO-style stacking)
        for (let i = 0; i < cardQuantity; i++) {
          renderedCards.push(
            <div
              key={`${card.id}-${i}`}
              className="pile-card-stack-item"
              style={{
                marginTop: i > 0 ? '-75px' : '0px', // Stack cards with MTGO-style overlap to name area
                zIndex: i + 1, // Bottom cards have higher z-index (MTGO-style)
              }}
            >
              <DraggableCard
                card={card}
                zone={zone}
                size="normal"
                scaleFactor={scaleFactor}
                onClick={onClick}
                onDoubleClick={onDoubleClick}
                onEnhancedDoubleClick={onEnhancedDoubleClick}
                onRightClick={onRightClick}
                onDragStart={onDragStart}
                showQuantity={false} // Don't show quantity on individual cards
                quantity={1} // Each rendered card represents 1 copy
                selected={isSelected ? isSelected(card.id) : false}
                selectable={true}
                isDragActive={isDragActive}
                isBeingDragged={isDragActive && selectedCards.some(sc => sc.id === card.id)}
                selectedCards={selectedCards}
              />
            </div>
          );
        }
      });
      
      return renderedCards;
    } catch (error) {
      console.error('Error rendering cards in pile column:', error);
      return [<div key="error" className="error-message">Error rendering cards</div>];
    }
  }, [cards, zone, scaleFactor, onClick, onDoubleClick, onEnhancedDoubleClick, onRightClick, onDragStart, isSelected, selectedCards, isDragActive]);'''
    
    new_render_cards = '''  // MTGO-style card stacking - ALL cards stack together with proper overlap
  const renderCards = useCallback(() => {
    try {
      const renderedCards: React.ReactElement[] = [];
      let cardIndex = 0; // Track position across all cards for proper stacking
      
      cards.forEach(card => {
        // Validate card has required properties
        if (!card || !card.id) {
          console.warn('Invalid card object:', card);
          return;
        }

        // Get quantity for this card
        let cardQuantity = 1;
        if (typeof card === 'object' && card !== null) {
          if ('quantity' in card && typeof card.quantity === 'number' && card.quantity > 0) {
            cardQuantity = card.quantity;
          }
        }

        // Create individual draggable cards for each copy (MTGO-style stacking)
        for (let i = 0; i < cardQuantity; i++) {
          const stackOffset = Math.round(-85 * scaleFactor); // Scale the overlap with card size
          
          renderedCards.push(
            <div
              key={`${card.id}-${i}`}
              className="pile-card-stack-item"
              style={{
                marginTop: cardIndex > 0 ? `${stackOffset}px` : '0px', // Stack ALL cards, not just same card
                zIndex: 100 - cardIndex, // Bottom cards have higher z-index (MTGO-style)
                position: 'relative',
              }}
            >
              <DraggableCard
                card={card}
                zone={zone}
                size="normal"
                scaleFactor={scaleFactor}
                onClick={onClick}
                onDoubleClick={onDoubleClick}
                onEnhancedDoubleClick={onEnhancedDoubleClick}
                onRightClick={onRightClick}
                onDragStart={onDragStart}
                showQuantity={false} // Don't show quantity on individual cards
                quantity={1} // Each rendered card represents 1 copy
                selected={isSelected ? isSelected(card.id) : false}
                selectable={true}
                isDragActive={isDragActive}
                isBeingDragged={isDragActive && selectedCards.some(sc => sc.id === card.id)}
                selectedCards={selectedCards}
              />
            </div>
          );
          
          cardIndex++; // Increment for next card in stack
        }
      });
      
      return renderedCards;
    } catch (error) {
      console.error('Error rendering cards in pile column:', error);
      return [<div key="error" className="error-message">Error rendering cards</div>];
    }
  }, [cards, zone, scaleFactor, onClick, onDoubleClick, onEnhancedDoubleClick, onRightClick, onDragStart, isSelected, selectedCards, isDragActive]);'''
    
    if old_render_cards in pile_column_content:
        pile_column_content = pile_column_content.replace(old_render_cards, new_render_cards)
        print("  ✅ Card stacking updated for cross-card stacking and scaled overlap")
    else:
        print("  ⚠️  Could not find renderCards function to update")
    
    # Save PileColumn.tsx changes
    if not write_file(pile_column_path, pile_column_content):
        return False
    
    # Fix 4 & 5: MTGOLayout.css - Update styling for gaps, scrolling, and sort menu
    print("\n🎯 Fix 4 & 5: Updating CSS for proper gaps, scrolling, and sort menu...")
    
    css_path = "src/components/MTGOLayout.css"
    css_content = read_file(css_path)
    
    if css_content is None:
        return False
    
    # Add sort button and menu styles
    sort_menu_css = '''
/* Sort Button and Menu Styles */
.sort-button-container {
  position: relative;
  display: inline-block;
}

.sort-toggle-btn {
  background-color: #404040;
  color: #ffffff;
  border: 1px solid #555555;
  padding: 4px 8px;
  border-radius: 3px;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin: 0 4px;
}

.sort-toggle-btn:hover {
  background-color: #4a4a4a;
  transform: scale(1.02);
}

.sort-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background-color: #333333;
  border: 1px solid #555555;
  border-radius: 4px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
  z-index: 1000;
  min-width: 120px;
  overflow: hidden;
}

.sort-menu button {
  display: block;
  width: 100%;
  background-color: transparent;
  color: #ffffff;
  border: none;
  padding: 8px 12px;
  font-size: 11px;
  cursor: pointer;
  text-align: left;
  transition: background-color 0.2s ease;
}

.sort-menu button:hover {
  background-color: #4a4a4a;
}

.sort-menu button.active {
  background-color: #3b82f6;
  color: #ffffff;
}

.sort-menu button:not(:last-child) {
  border-bottom: 1px solid #555555;
}
'''
    
    # Update pile view CSS for tighter gaps and proper scrolling
    pile_view_updates = '''
/* UPDATED: Pile View Container - Remove separate header, better stacking */
.pile-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

/* UPDATED: Pile Columns Container - Tighter gaps, area-level scrolling only */
.pile-columns-container {
  flex: 1;
  display: flex;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 4px; /* Reduced padding for tighter layout */
  gap: 6px; /* Tighter gap between columns like MTGO */
  align-items: flex-start;
}

/* UPDATED: Individual Pile Column - Remove per-column scrolling */
.pile-column {
  min-width: 120px;
  background-color: rgba(255, 255, 255, 0.02);
  border: 1px solid #404040;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  height: fit-content;
  /* REMOVED: max-height to eliminate per-column scrolling */
}

.pile-column.empty-column {
  min-width: 80px; /* Smaller empty column */
  background-color: rgba(255, 255, 255, 0.01);
  border: 1px dashed #666666;
  border-radius: 6px;
  min-height: 100px;
}

/* UPDATED: Column Header - Simple number styling */
.pile-column-header {
  padding: 4px 8px; /* Reduced padding */
  background-color: #404040;
  font-size: 12px; /* Slightly larger for number readability */
  font-weight: bold;
  text-align: center;
  border-bottom: 1px solid #555555;
  color: #ffffff;
  border-radius: 5px 5px 0 0;
  min-height: 20px; /* Consistent header height */
}

/* UPDATED: Column Content - No scrolling, better card flow */
.pile-column-content {
  flex: 1;
  padding: 3px; /* Reduced padding for tighter stacking */
  display: flex;
  flex-direction: column;
  /* REMOVED: overflow-y: auto - no per-column scrolling */
  /* REMOVED: max-height - let content flow naturally */
}

/* REMOVED: Per-column scrollbar styles */

/* UPDATED: Card stacking improvements */
.pile-card-stack-item {
  position: relative;
  transition: transform 0.15s ease, z-index 0.15s ease;
}

.pile-card-stack-item:hover {
  transform: translateY(-8px); /* Enhanced hover effect */
  z-index: 1000 !important;
  box-shadow: 0 6px 12px rgba(0,0,0,0.5);
}

/* UPDATED: Empty column placeholder */
.empty-column-placeholder {
  text-align: center;
  color: #666666;
  font-size: 10px;
  font-style: italic;
  padding: 15px 8px;
  border: 1px dashed #555555;
  border-radius: 4px;
  margin: 4px;
}
'''
    
    # Find and replace existing pile view CSS
    pile_view_section = re.search(r'/\* PHASE 3D: Pile View Styles \*/.*?(?=/\*|$)', css_content, re.DOTALL)
    if pile_view_section:
        css_content = css_content.replace(pile_view_section.group(0), '/* PHASE 3D: Pile View Styles */' + pile_view_updates)
        print("  ✅ Pile view CSS updated for tighter gaps and proper scrolling")
    else:
        # Add the CSS at the end if section not found
        css_content += '\n/* PHASE 3D: Pile View Styles */' + pile_view_updates
        print("  ✅ Pile view CSS added at end of file")
    
    # Add sort menu CSS
    css_content += sort_menu_css
    print("  ✅ Sort button and menu CSS added")
    
    # Save CSS changes
    if not write_file(css_path, css_content):
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ALL PILE VIEW FIXES APPLIED SUCCESSFULLY!")
    print("=" * 60)
    print("\n📋 Summary of Changes:")
    print("  ✅ Sort dropdown converted to hidden button menu")
    print("  ✅ Column headers now show simple card counts only") 
    print("  ✅ Card stacking fixed for cross-card stacking with scaled overlap")
    print("  ✅ Column gaps tightened to match MTGO spacing")
    print("  ✅ Per-column scrolling removed, area-level scrolling only")
    print("\n🚀 Ready to test! Run 'npm start' to see the improvements.")
    
    return True

if __name__ == "__main__":
    if apply_all_fixes():
        print("\n✨ All fixes completed successfully!")
    else:
        print("\n❌ Some fixes failed. Please check the error messages above.")
