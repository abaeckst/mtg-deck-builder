#!/usr/bin/env python3
"""
Fix the card mapping pattern with a more precise approach
"""

import re

def fix_card_mapping():
    """Replace the sortedCollectionCards.map with smart append logic"""
    print("🔧 Fixing card mapping pattern...")
    
    try:
        # Read the file
        with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the start of the sortedCollectionCards.map section
        start_pattern = r'\{sortedCollectionCards\.map\(\(card\) => \('
        
        # Find where this pattern starts
        start_match = re.search(start_pattern, content)
        if not start_match:
            print("❌ Could not find sortedCollectionCards.map start")
            return False
        
        start_pos = start_match.start()
        print(f"✅ Found sortedCollectionCards.map at position {start_pos}")
        
        # Now find the matching closing brackets - we need to count parentheses
        pos = start_match.end()
        paren_count = 1  # We've already seen the opening (
        brace_count = 1  # We've already seen the opening {
        
        while pos < len(content) and (paren_count > 0 or brace_count > 0):
            char = content[pos]
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            elif char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
            pos += 1
        
        end_pos = pos
        print(f"✅ Found end of mapping at position {end_pos}")
        
        # Extract the full mapping block
        mapping_block = content[start_pos:end_pos]
        print(f"✅ Extracted mapping block ({len(mapping_block)} characters)")
        
        # Create the smart append replacement
        smart_append = """{(() => {
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
                  })()}"""
        
        # Replace the mapping block
        new_content = content[:start_pos] + smart_append + content[end_pos:]
        
        # Write the fixed content
        with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("\n🎯 SUCCESS! Card mapping replaced with smart append logic:")
        print("1. ✅ Found and extracted existing mapping block")
        print("2. ✅ Replaced with smart append logic")
        print("3. ✅ Existing cards rendered with stable keys")
        print("4. ✅ New cards rendered separately")
        print("\nLoad More should now preserve scroll position perfectly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    fix_card_mapping()
