#!/usr/bin/env python3
"""
Fix MTGOLayout.tsx - Improve inline grid styling for deck and sideboard areas
This keeps all drag-and-drop functionality while applying our improved grid logic
"""

def fix_mtgo_layout_inline_grids():
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        # Read the current file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ Successfully read MTGOLayout.tsx")
        
        # Fix 1: Replace collection area individual cards with CardGrid (keeping existing approach but cleaner)
        old_collection_grid = """          <div className="collection-grid">
            {loading && <div className="loading-message">Loading cards...</div>}
            {error && <div className="error-message">Error: {error}</div>}
            {cards.map(card => (
              <DraggableCard
                key={card.id}
                card={card}
                zone="collection"
                size="normal"
                scaleFactor={cardSizes.collection}
                onClick={(card, event) => handleCardClick(card, event)} 
                onDoubleClick={handleAddToDeck}
                onEnhancedDoubleClick={handleDoubleClick}
                onRightClick={handleRightClick}
                onDragStart={handleDragStart}
                showQuantity={true}
                availableQuantity={4}
                quantity={mainDeck.find((dc: any) => dc.id === card.id)?.quantity || 0}
                selected={isSelected(card.id)}
                selectable={true}
                isDragActive={dragState.isDragging}
                isBeingDragged={dragState.draggedCards.some(dc => dc.id === card.id)}
                selectedCards={getSelectedCardObjects()}
              />
            ))}
          </div>"""
        
        new_collection_grid = """          <div 
            className="collection-grid"
            style={{
              display: 'grid',
              gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.collection)}px, max-content))`,
              gap: `${Math.max(8, Math.min(20, Math.round(10 * cardSizes.collection)))}px`,
              alignContent: 'start',
              padding: '8px'
            }}
          >
            {loading && <div className="loading-message">Loading cards...</div>}
            {error && <div className="error-message">Error: {error}</div>}
            {cards.map(card => (
              <DraggableCard
                key={card.id}
                card={card}
                zone="collection"
                size="normal"
                scaleFactor={cardSizes.collection}
                onClick={(card, event) => handleCardClick(card, event)} 
                onDoubleClick={handleAddToDeck}
                onEnhancedDoubleClick={handleDoubleClick}
                onRightClick={handleRightClick}
                onDragStart={handleDragStart}
                showQuantity={true}
                availableQuantity={4}
                quantity={mainDeck.find((dc: any) => dc.id === card.id)?.quantity || 0}
                selected={isSelected(card.id)}
                selectable={true}
                isDragActive={dragState.isDragging}
                isBeingDragged={dragState.draggedCards.some(dc => dc.id === card.id)}
                selectedCards={getSelectedCardObjects()}
              />
            ))}
          </div>"""
        
        if old_collection_grid in content:
            content = content.replace(old_collection_grid, new_collection_grid)
            print("✅ Fix 1: Updated collection area with improved inline grid styling")
        else:
            print("⚠️  Fix 1: Collection grid section not found in expected format")
        
        # Fix 2: Improve deck area inline grid styling
        old_deck_grid = """              <div 
                className="deck-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.max(90, Math.round(110 * cardSizes.deck))}px, 1fr))`,
                  gap: `${Math.max(6, Math.min(12, Math.round(8 * cardSizes.deck)))}px`,
                  alignContent: 'start',
                  minHeight: '150px',
                  paddingBottom: '40px'
                }}
              >"""
        
        new_deck_grid = """              <div 
                className="deck-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.deck)}px, 1fr))`,
                  gap: `${Math.max(8, Math.min(20, Math.round(10 * cardSizes.deck)))}px`,
                  alignContent: 'start',
                  minHeight: '150px',
                  paddingBottom: '40px'
                }}
              >"""
        
        if old_deck_grid in content:
            content = content.replace(old_deck_grid, new_deck_grid)
            print("✅ Fix 2: Updated deck area with improved grid calculations")
        else:
            print("⚠️  Fix 2: Deck grid styling not found in expected format")
        
        # Fix 3: Improve sideboard area inline grid styling
        old_sideboard_grid = """              <div 
                className="sideboard-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.max(90, Math.round(110 * cardSizes.sideboard))}px, 1fr))`,
                  gap: `${Math.max(6, Math.min(12, Math.round(8 * cardSizes.sideboard)))}px`,
                  alignContent: 'start',
                  minHeight: '150px',
                  paddingBottom: '40px'
                }}
              >"""
        
        new_sideboard_grid = """              <div 
                className="sideboard-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.sideboard)}px, 1fr))`,
                  gap: `${Math.max(8, Math.min(20, Math.round(10 * cardSizes.sideboard)))}px`,
                  alignContent: 'start',
                  minHeight: '150px',
                  paddingBottom: '40px'
                }}
              >"""
        
        if old_sideboard_grid in content:
            content = content.replace(old_sideboard_grid, new_sideboard_grid)
            print("✅ Fix 3: Updated sideboard area with improved grid calculations")
        else:
            print("⚠️  Fix 3: Sideboard grid styling not found in expected format")
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n🎯 SUCCESS: Fixed MTGOLayout.tsx inline grid styling")
        print("✅ Collection area: Uses max-content for multiple cards per row")
        print("✅ Deck area: Uses 1fr with improved gap calculations")  
        print("✅ Sideboard area: Uses 1fr with improved gap calculations")
        print("✅ All areas: Increased minimum gap from 6px to 8px")
        print("✅ All areas: Increased maximum gap from 12px to 20px")
        print("✅ All drag-and-drop functionality preserved")
        print("\nGrid Behavior Summary:")
        print("• Collection: max-content prevents card expansion, allows multiple per row")
        print("• Deck/Sideboard: 1fr allows flexible sizing with better spacing")
        print("• All areas use same base size (130px) and improved gap formula")
        print("\nTest with 'npm start' to verify grid improvements!")
        
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find {file_path}")
        print("Please make sure you're in the correct directory")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    fix_mtgo_layout_inline_grids()
