#!/usr/bin/env python3

import os
import sys

def debug_react_rendering():
    """Add comprehensive debugging to see exactly what React is rendering"""
    
    filename = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add debugging to the collection grid rendering
    old_collection_grid = """              <div 
                className="collection-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.collection)}px, max-content))`,
                  gap: `${Math.round(4 * cardSizes.collection)}px`,
                  alignContent: 'start',
                  padding: '8px'
                }}
              >
                {sortedCollectionCards.map((card) => ("""

    new_collection_grid = """              <div 
                className="collection-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.collection)}px, max-content))`,
                  gap: `${Math.round(4 * cardSizes.collection)}px`,
                  alignContent: 'start',
                  padding: '8px'
                }}
              >
                {(() => {
                  console.log('🎨 RENDERING COLLECTION GRID:', {
                    cardsToRender: sortedCollectionCards.length,
                    firstCard: sortedCollectionCards[0]?.name || 'None',
                    lastCard: sortedCollectionCards[sortedCollectionCards.length - 1]?.name || 'None',
                    renderTimestamp: Date.now(),
                    gridColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.collection)}px, max-content))`
                  });
                  return null;
                })()}
                {sortedCollectionCards.map((card, index) => {
                  if (index < 5) {
                    console.log(`🎨 RENDERING CARD ${index + 1}:`, card.name);
                  }
                  return ("""

    if old_collection_grid in content:
        content = content.replace(old_collection_grid, new_collection_grid)
        print("✅ Added collection grid rendering debug")
    else:
        print("❌ Could not find collection grid")
        return False

    # Close the map function properly
    old_draggable_card = """                  <DraggableCard
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
                ))}"""

    new_draggable_card = """                    <DraggableCard
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
                  );
                })}"""

    if old_draggable_card in content:
        content = content.replace(old_draggable_card, new_draggable_card)
        print("✅ Fixed collection grid map function")
    else:
        print("❌ Could not find draggable card section")
        return False

    # Add a key to the collection content to force React to re-render when cards change
    old_collection_content = """          {/* Collection Content - Conditional Rendering */}
          {loading && <div className="loading-message">Loading cards...</div>}
          {error && <div className="error-message">Error: {error}</div>}
          {!loading && !error && cards.length === 0 && (
            <div className="no-results-message">
              <div className="no-results-icon">🔍</div>
              <h3>No cards found</h3>
              <p>No cards match your current search and filter criteria.</p>
              <div className="no-results-suggestions">
                <p><strong>Try:</strong></p>
                <ul>
                  <li>Adjusting your search terms</li>
                  <li>Changing filter settings</li>
                  <li>Using broader criteria</li>
                  <li>Clearing some filters</li>
                </ul>
              </div>
            </div>
          )}
          
          {!loading && !error && cards.length > 0 && ("""

    new_collection_content = """          {/* Collection Content - Conditional Rendering */}
          {loading && <div className="loading-message">Loading cards...</div>}
          {error && <div className="error-message">Error: {error}</div>}
          {!loading && !error && cards.length === 0 && (
            <div className="no-results-message">
              <div className="no-results-icon">🔍</div>
              <h3>No cards found</h3>
              <p>No cards match your current search and filter criteria.</p>
              <div className="no-results-suggestions">
                <p><strong>Try:</strong></p>
                <ul>
                  <li>Adjusting your search terms</li>
                  <li>Changing filter settings</li>
                  <li>Using broader criteria</li>
                  <li>Clearing some filters</li>
                </ul>
              </div>
            </div>
          )}
          
          {!loading && !error && cards.length > 0 && (
            <div key={`collection-${cardsChangeTracker.timestamp}-${cardsChangeTracker.firstCard}`}>
              {(() => {
                console.log('🎨 COLLECTION CONTENT CONTAINER RENDER:', {
                  containerKey: `collection-${cardsChangeTracker.timestamp}-${cardsChangeTracker.firstCard}`,
                  viewMode: layout.viewModes.collection,
                  cardsLength: cards.length,
                  sortedCardsLength: sortedCollectionCards.length
                });
                return null;
              })()}"""

    if old_collection_content in content:
        content = content.replace(old_collection_content, new_collection_content)
        print("✅ Added collection content container with key")
    else:
        print("❌ Could not find collection content")
        return False

    # Close the container div
    old_load_more = """          )}
          
          {/* Load More Results Section - DEBUGGING */}"""

    new_load_more = """            </div>
          )}
          
          {/* Load More Results Section - DEBUGGING */}"""

    if old_load_more in content:
        content = content.replace(old_load_more, new_load_more)
        print("✅ Closed collection content container")
    else:
        print("❌ Could not find load more section")
        return False

    # Add a global debug function to manually trigger renders
    debug_function = """  // Global debug function for manual testing
  useEffect(() => {
    const debugRender = () => {
      console.log('🧪 MANUAL RENDER DEBUG:', {
        cardsLength: cards.length,
        sortedCardsLength: sortedCollectionCards.length,
        firstCard: cards[0]?.name || 'None',
        sortedFirstCard: sortedCollectionCards[0]?.name || 'None',
        changeTracker: cardsChangeTracker,
        viewMode: layout.viewModes.collection
      });
      
      // Force a manual re-render by updating a dummy state
      setSearchText(prev => prev === '' ? ' ' : prev === ' ' ? '' : prev);
    };
    
    (window as any).debugRender = debugRender;
    console.log('🧪 Global debug function available: window.debugRender()');
    
    return () => {
      delete (window as any).debugRender;
    };
  }, [cards, sortedCollectionCards, cardsChangeTracker, layout.viewModes.collection]);

"""

    # Insert the debug function after the other effects
    insert_point = "  // Clear both deck and sideboard functionality"
    if insert_point in content:
        content = content.replace(insert_point, debug_function + insert_point)
        print("✅ Added global debug function")
    else:
        print("❌ Could not find insertion point for debug function")

    # Write the updated content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully updated {filename} with comprehensive React rendering debug")
    return True

if __name__ == "__main__":
    success = debug_react_rendering()
    sys.exit(0 if success else 1)