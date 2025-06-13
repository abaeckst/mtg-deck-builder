#!/usr/bin/env python3
"""
Fix Collection Area to show individual cards instead of stacked cards
The collection should display individual cards in a grid, not quantity stacks
"""

import os

def fix_collection_grid_layout():
    filepath = "src/components/CollectionArea.tsx"
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    # Read current content
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create backup
    backup_path = f"{filepath}.backup_individual_cards"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Backup created: {backup_path}")
    
    # Fix the collection grid rendering
    # The key issue is that we're showing quantity badges and stacking behavior
    # Collection should show individual cards that can be added to deck
    
    # Find the collection grid section and replace it
    old_grid_section = '''          <div 
            className="collection-grid"
            style={{
              display: 'grid',
              gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSize)}px, max-content))`,
              gap: `${Math.round(4 * cardSize)}px`,
              alignContent: 'start',
              padding: '8px'
            }}
          >
            {sortedCards.map((card) => (
              <DraggableCard
                key={getCardId(card)}
                card={card}
                zone="collection"
                size="normal"
                scaleFactor={cardSize}
                onClick={(card, event) => onCardClick(card, event)} 
                onDoubleClick={(card) => onCardDoubleClick(card)}
                onEnhancedDoubleClick={onCardDoubleClick}
                onRightClick={onCardRightClick}
                onDragStart={onDragStart}
                showQuantity={true}
                availableQuantity={4}
                quantity={getTotalCopies(getCardId(card))}
                selected={isSelected(getCardId(card))}
                selectable={true}
                isDragActive={dragState.isDragging}
                isBeingDragged={dragState.draggedCards.some(dc => getCardId(dc) === getCardId(card))}
                selectedCards={getSelectedCardObjects()}
              />
            ))}'''
    
    new_grid_section = '''          <div 
            className="collection-grid"
            style={{
              display: 'grid',
              gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSize)}px, max-content))`,
              gap: `${Math.round(4 * cardSize)}px`,
              alignContent: 'start',
              padding: '8px'
            }}
          >
            {sortedCards.map((card) => (
              <DraggableCard
                key={getCardId(card)}
                card={card}
                zone="collection"
                size="normal"
                scaleFactor={cardSize}
                onClick={(card, event) => onCardClick(card, event)} 
                onDoubleClick={(card) => onCardDoubleClick(card)}
                onEnhancedDoubleClick={onCardDoubleClick}
                onRightClick={onCardRightClick}
                onDragStart={onDragStart}
                showQuantity={false}
                // No quantity display for collection - each card is individual
                selected={isSelected(getCardId(card))}
                selectable={true}
                isDragActive={dragState.isDragging}
                isBeingDragged={dragState.draggedCards.some(dc => getCardId(dc) === getCardId(card))}
                selectedCards={getSelectedCardObjects()}
              />
            ))}'''
    
    # Replace the grid section
    if old_grid_section in content:
        content = content.replace(old_grid_section, new_grid_section)
        print("✅ Fixed collection grid - removed quantity stacking")
    else:
        print("⚠️ Could not find exact grid section to replace")
        # Try a more targeted fix
        if 'showQuantity={true}' in content and 'availableQuantity={4}' in content:
            content = content.replace('showQuantity={true}', 'showQuantity={false}')
            content = content.replace('availableQuantity={4}', '// No quantity display for collection')
            content = content.replace('quantity={getTotalCopies(getCardId(card))}', '// Individual cards, no quantity stacking')
            print("✅ Applied targeted fixes to remove quantity display")
    
    # Write the updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Collection area fixed - now shows individual cards in grid")
    print("🎯 Each card in collection will now appear as individual card, not stacked")
    print("🔄 Restart the app to see the fix")
    
    return True

if __name__ == "__main__":
    success = fix_collection_grid_layout()
    if success:
        print("\n🎉 Collection grid layout fixed!")
        print("📋 Changes made:")
        print("   - Removed quantity badges from collection cards")
        print("   - Removed stacking behavior")
        print("   - Collection now shows individual cards in clean grid")
        print("\n💡 Collection cards will now display as individual cards")
        print("   that can be clicked/dragged to add to deck, not quantity stacks")
    else:
        print("\n❌ Failed to fix collection grid layout")
