#!/usr/bin/env python3

import os
import sys

def fix_collection_card_view():
    """Fix the collection view mode so card view works correctly instead of defaulting to list"""
    
    # First, fix useLayout.ts to ensure proper default
    layout_file = "src/hooks/useLayout.ts"
    
    if not os.path.exists(layout_file):
        print(f"Error: {layout_file} not found")
        return False
    
    print("🔧 Step 1: Fixing useLayout.ts default view mode...")
    
    with open(layout_file, 'r', encoding='utf-8') as f:
        layout_content = f.read()
    
    # Ensure default collection view is 'grid' (card view)
    old_default = """const DEFAULT_LAYOUT: LayoutState = {
  panels: {
    filterPanelWidth: 280,
    deckAreaHeightPercent: 30, // 30% of screen height for deck/sideboard
    sideboardWidth: 300,
  },
  previewPane: {
    visible: true,
    position: { x: 20, y: 20 },
    size: { width: 350, height: 490 },
  },
  viewModes: {
    collection: 'grid',
    deck: 'card',
    sideboard: 'card',
  },"""
    
    # This should already be correct, but let's make sure
    if 'collection: \'grid\'' in layout_content:
        print("✅ Default collection view mode is already 'grid'")
    else:
        print("❌ Default collection view mode needs fixing")
        # Try to fix if needed
        layout_content = layout_content.replace("collection: 'list'", "collection: 'grid'")
    
    # Remove the debugging localStorage override that forces list view
    old_debug_code = """  // Clear problematic localStorage for collection view mode (debugging)
  useEffect(() => {
    const savedLayout = localStorage.getItem(STORAGE_KEY);
    if (savedLayout) {
      try {
        const parsed = JSON.parse(savedLayout);
        if (parsed.viewModes && parsed.viewModes.collection === 'list') {
          console.warn('Found collection view mode set to list in localStorage, forcing to grid');
          parsed.viewModes.collection = 'grid';
          localStorage.setItem(STORAGE_KEY, JSON.stringify(parsed));
          setLayout(prev => ({
            ...prev,
            viewModes: { ...prev.viewModes, collection: 'grid' }
          }));
        }
      } catch (error) {
        console.warn('Error processing saved layout:', error);
      }
    }
  }, []);"""
    
    if old_debug_code in layout_content:
        layout_content = layout_content.replace(old_debug_code, """  // Force collection to grid view if localStorage has wrong value
  useEffect(() => {
    const savedLayout = localStorage.getItem(STORAGE_KEY);
    if (savedLayout) {
      try {
        const parsed = JSON.parse(savedLayout);
        if (parsed.viewModes && parsed.viewModes.collection !== 'grid') {
          console.log('🔧 Forcing collection view to grid mode');
          parsed.viewModes.collection = 'grid';
          localStorage.setItem(STORAGE_KEY, JSON.stringify(parsed));
        }
      } catch (error) {
        console.warn('Error processing saved layout:', error);
      }
    }
  }, []);""")
        print("✅ Updated localStorage debugging code to force grid view")
    
    with open(layout_file, 'w', encoding='utf-8') as f:
        f.write(layout_content)
    
    # Now fix MTGOLayout.tsx view mode conditional logic
    mtgo_file = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(mtgo_file):
        print(f"Error: {mtgo_file} not found")
        return False
    
    print("🔧 Step 2: Fixing MTGOLayout.tsx view mode logic...")
    
    with open(mtgo_file, 'r', encoding='utf-8') as f:
        mtgo_content = f.read()
    
    # Find the problematic conditional rendering section
    old_conditional = """          {!loading && !error && cards.length > 0 && (
            <div key={`collection-${sortChangeId}-${cardsChangeTracker.timestamp}-${cardsChangeTracker.firstCard}`}>
              {(() => {
                console.log('🎨 COLLECTION CONTENT CONTAINER RENDER:', {
                  containerKey: `collection-${sortChangeId}-${cardsChangeTracker.timestamp}-${cardsChangeTracker.firstCard}`,
                  sortChangeId: sortChangeId,
                  viewMode: layout.viewModes.collection,
                  cardsLength: cards.length,
                  sortedCardsLength: sortedCollectionCards.length
                });
                return null;
              })()}
            layout.viewModes.collection === 'list' ? ("""
    
    new_conditional = """          {!loading && !error && cards.length > 0 && (
            layout.viewModes.collection === 'list' ? ("""
    
    if old_conditional in mtgo_content:
        mtgo_content = mtgo_content.replace(old_conditional, new_conditional)
        print("✅ Simplified collection rendering logic")
    else:
        print("⚠️ Could not find exact conditional pattern - checking for simpler fix")
        
        # Alternative fix: look for the container div with complex key
        old_div_pattern = """            <div key={`collection-${sortChangeId}-${cardsChangeTracker.timestamp}-${cardsChangeTracker.firstCard}`}>"""
        
        if old_div_pattern in mtgo_content:
            # Remove the complex container div and its debug code
            debug_section = """            <div key={`collection-${sortChangeId}-${cardsChangeTracker.timestamp}-${cardsChangeTracker.firstCard}`}>
              {(() => {
                console.log('🎨 COLLECTION CONTENT CONTAINER RENDER:', {
                  containerKey: `collection-${sortChangeId}-${cardsChangeTracker.timestamp}-${cardsChangeTracker.firstCard}`,
                  sortChangeId: sortChangeId,
                  viewMode: layout.viewModes.collection,
                  cardsLength: cards.length,
                  sortedCardsLength: sortedCollectionCards.length
                });
                return null;
              })()}"""
            
            # Find the end of this debug section
            debug_end = """            </div>
          )}"""
            
            # Replace with clean conditional
            if debug_section in mtgo_content and debug_end in mtgo_content:
                # Remove the debug container entirely
                start_index = mtgo_content.find(debug_section)
                end_index = mtgo_content.find(debug_end, start_index) + len(debug_end)
                
                before = mtgo_content[:start_index]
                after = mtgo_content[end_index:]
                
                # Clean replacement
                clean_conditional = """            layout.viewModes.collection === 'list' ? (
              <ListView
                cards={sortedCollectionCards}
                area="collection"
                scaleFactor={cardSizes.collection}
                sortCriteria={collectionSort.criteria}
                sortDirection={collectionSort.direction}
                onSortChange={(criteria, direction) => {
                  updateSort('collection', criteria, direction);
                }}
                onClick={handleCardClick}
                onDoubleClick={handleAddToDeck}
                onRightClick={handleRightClick}
                onDragStart={handleDragStart}
                isSelected={isSelected}
                selectedCards={getSelectedCardObjects()}
                isDragActive={dragState.isDragging}
              />
            ) : (
              <div 
                className="collection-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.collection)}px, max-content))`,
                  gap: `${Math.round(4 * cardSizes.collection)}px`,
                  alignContent: 'start',
                  padding: '8px'
                }}
              >
                {sortedCollectionCards.map((card, index) => (
                  <DraggableCard
                    key={getCardId(card)}
                    card={card}
                    zone="collection"
                    size="normal"
                    scaleFactor={cardSizes.collection}
                    onClick={(card, event) => handleCardClick(card, event)} 
                    onDoubleClick={(card) => handleAddToDeck(card)}
                    onEnhancedDoubleClick={handleDoubleClick}
                    onRightClick={handleRightClick}
                    onDragStart={handleDragStart}
                    showQuantity={true}
                    availableQuantity={4}
                    quantity={getTotalCopies(getCardId(card))}
                    selected={isSelected(getCardId(card))}
                    selectable={true}
                    isDragActive={dragState.isDragging}
                    isBeingDragged={dragState.draggedCards.some(dc => getCardId(dc) === getCardId(card))}
                    selectedCards={getSelectedCardObjects()}
                  />
                ))}
              </div>
            )
          )}"""
                
                mtgo_content = before + clean_conditional
                print("✅ Completely cleaned collection view conditional logic")
            else:
                print("❌ Could not find complete debug section pattern")
                return False
        else:
            print("❌ Could not find any recognized pattern to fix")
            return False
    
    # Remove excessive debugging console logs from rendering
    debug_logs_to_remove = [
        """                {(() => {
                  console.log('🎨 RENDERING COLLECTION GRID:', {
                    cardsToRender: sortedCollectionCards.length,
                    firstCard: sortedCollectionCards[0]?.name || 'None',
                    lastCard: sortedCollectionCards[sortedCollectionCards.length - 1]?.name || 'None',
                    renderTimestamp: Date.now(),
                    gridColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.collection)}px, max-content))`
                  });
                  return null;
                })()}""",
        """                  if (index < 5) {
                    console.log(`🎨 RENDERING CARD ${index + 1}:`, card.name);
                  }"""
    ]
    
    for debug_log in debug_logs_to_remove:
        if debug_log in mtgo_content:
            mtgo_content = mtgo_content.replace(debug_log, "")
            print("✅ Removed excessive debug logging from card rendering")
    
    with open(mtgo_file, 'w', encoding='utf-8') as f:
        f.write(mtgo_content)
    
    print("✅ Successfully fixed collection card view mode logic")
    return True

if __name__ == "__main__":
    success = fix_collection_card_view()
    sys.exit(0 if success else 1)