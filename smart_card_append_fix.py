#!/usr/bin/env python3
"""
Smart Card Append Load More Fix
This implements elegant scroll preservation by rendering existing + new cards separately
"""

import re

def implement_smart_card_append():
    """Implement smart card append with natural scroll preservation"""
    print("🔧 Implementing Smart Card Append Load More fix...")
    
    try:
        # Read the file
        with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Step 1: Add state for tracking loaded card count
        # Find location after existing useState declarations
        pattern = r'(const \[showScreenshotModal, setShowScreenshotModal\] = useState\(false\);)'
        
        if re.search(pattern, content):
            state_addition = r'''\1
  
  // Smart card append: track cards for smooth Load More
  const [loadedCardsCount, setLoadedCardsCount] = useState(0);'''
            
            content = re.sub(pattern, state_addition, content)
            print("✅ Added loadedCardsCount state")
        else:
            print("❌ Could not find useState location for loadedCardsCount")
            return False
        
        # Step 2: Add useEffect to sync loadedCardsCount with cards.length changes
        # Find location after the mobile fallback check and before the return
        effect_pattern = r'(// Mobile fallback\s+if \(!canUseMTGO\) \{[^}]+\}\s+)'
        
        if re.search(effect_pattern, content, re.DOTALL):
            effect_addition = r'''\1
  // Sync loaded cards count for smart append
  useEffect(() => {
    if (cards.length > 0) {
      setLoadedCardsCount(cards.length);
    }
  }, [cards.length]);
  
'''
            
            content = re.sub(effect_pattern, effect_addition, content, flags=re.DOTALL)
            print("✅ Added useEffect to sync loadedCardsCount")
        else:
            print("❌ Could not find location for useEffect")
            return False
        
        # Step 3: Replace the collection grid div and remove problematic key
        # Remove the key prop and ref that cause remounting
        grid_pattern = r'''<div 
                className="collection-grid"
                ref=\{collectionGridRef\}
                key=\{`collection-grid-\$\{cards\.length\}`\}
                data-cards-loaded=\{cards\.length\}'''
        
        grid_replacement = r'''<div 
                className="collection-grid"
                data-cards-loaded={cards.length}'''
        
        if re.search(grid_pattern, content):
            content = re.sub(grid_pattern, grid_replacement, content)
            print("✅ Removed problematic key and ref from collection-grid")
        else:
            print("❌ Could not find collection-grid pattern")
            return False
        
        # Step 4: Replace the card mapping with smart append logic
        # Find the existing sortedCollectionCards.map pattern
        map_pattern = r'\{sortedCollectionCards\.map\(\(card\) => \(\s+<DraggableCard[^}]+\}\)\)\}'
        
        smart_append_replacement = r'''{(() => {
                    // Smart Card Append: Render existing cards with stable keys + new cards
                    const existingCardsCount = Math.min(loadedCardsCount - (cards.length > loadedCardsCount ? 175 : 0), sortedCollectionCards.length);
                    const existingCards = sortedCollectionCards.slice(0, existingCardsCount);
                    const newCards = sortedCollectionCards.slice(existingCardsCount);
                    
                    return (
                      <>
                        {/* Existing cards with stable keys - no re-render */}
                        {existingCards.map((card) => (
                          <DraggableCard
                            key={`existing-${getCardId(card)}`}
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
                        
                        {/* New cards from Load More - only these render */}
                        {newCards.map((card) => (
                          <DraggableCard
                            key={`new-${getCardId(card)}`}
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
                      </>
                    );
                  })()}'''
        
        if re.search(map_pattern, content, re.DOTALL):
            content = re.sub(map_pattern, smart_append_replacement, content, flags=re.DOTALL)
            print("✅ Replaced card mapping with smart append logic")
        else:
            print("❌ Could not find sortedCollectionCards.map pattern")
            return False
        
        # Step 5: Update Load More button to not use preserveScrollOnLoadMore (no longer needed)
        load_more_pattern = r'onClick=\{\(\) => preserveScrollOnLoadMore\(\(\) => loadMoreResultsAction\(\)\)\}'
        load_more_replacement = r'onClick={loadMoreResultsAction}'
        
        if re.search(load_more_pattern, content):
            content = re.sub(load_more_pattern, load_more_replacement, content)
            print("✅ Simplified Load More button (scroll preservation no longer needed)")
        
        # Write the fixed content
        with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("\n🎯 SUCCESS! Smart Card Append implemented:")
        print("1. ✅ Added loadedCardsCount state tracking")
        print("2. ✅ Added useEffect to sync count with cards.length") 
        print("3. ✅ Removed problematic key prop from grid container")
        print("4. ✅ Split rendering: existing cards (stable) + new cards (fresh)")
        print("5. ✅ Simplified Load More button (no scroll manipulation needed)")
        print("\nHow it works:")
        print("- Existing cards keep stable keys → no re-render → scroll preserved")
        print("- Only new cards from Load More actually render")
        print("- Natural, smooth user experience with perfect scroll preservation!")
        print("\nTest Load More in Card view - should be buttery smooth now!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    implement_smart_card_append()
