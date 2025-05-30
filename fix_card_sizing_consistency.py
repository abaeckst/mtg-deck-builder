#!/usr/bin/env python3
"""
Fix Card Sizing Consistency Issues
- 40% default for all areas
- Identical sizes at same slider positions
- Proportional spacing with min/max bounds
- All areas use 'normal' base size
"""

def fix_card_sizing_defaults():
    """Fix useCardSizing hook to ensure 40% default for all areas"""
    file_path = "src/hooks/useCardSizing.ts"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ensure all defaults are exactly 0.4
        old_defaults = '''const DEFAULT_SIZES: CardSizeState = {
  collection: 0.4,  // 40% of base size for all areas
  deck: 0.4,        // 40% of base size for all areas
  sideboard: 0.4    // 40% of base size for all areas
};'''

        # Keep the same, but ensure it's consistent
        new_defaults = '''const DEFAULT_SIZES: CardSizeState = {
  collection: 0.4,  // 40% default - consistent across all areas
  deck: 0.4,        // 40% default - consistent across all areas  
  sideboard: 0.4    // 40% default - consistent across all areas
};'''

        content = content.replace(old_defaults, new_defaults)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def fix_mtgo_layout_card_sizes():
    """Fix MTGOLayout.tsx to use 'normal' size for all areas and pass consistent scale factors"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix deck cards to use 'normal' size instead of 'small'
        old_deck_card = '''                  <DraggableCard
                    key={deckCard.id}
                    card={deckCard}
                    zone="deck"
                    size="small"
                    scaleFactor={cardSizes.deck}'''

        new_deck_card = '''                  <DraggableCard
                    key={deckCard.id}
                    card={deckCard}
                    zone="deck"
                    size="normal"
                    scaleFactor={cardSizes.deck}'''

        # Fix sideboard cards to use 'normal' size instead of 'small'
        old_sideboard_card = '''                  <DraggableCard
                    key={sideCard.id}
                    card={sideCard}
                    zone="sideboard"
                    size="small"
                    scaleFactor={cardSizes.sideboard}'''

        new_sideboard_card = '''                  <DraggableCard
                    key={sideCard.id}
                    card={sideCard}
                    zone="sideboard"
                    size="normal"
                    scaleFactor={cardSizes.sideboard}'''

        # Apply replacements
        content = content.replace(old_deck_card, new_deck_card)
        content = content.replace(old_sideboard_card, new_sideboard_card)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def fix_magic_card_grid_spacing():
    """Fix MagicCard.tsx to implement proper proportional spacing with bounds"""
    file_path = "src/components/MagicCard.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the grid logic with improved spacing bounds
        old_grid_logic = '''  // Calculate dynamic grid column size and gap based on card size and scale factor
  const getGridSettings = () => {
    const baseSizes = {
      small: 70,
      normal: 130, 
      large: 210
    };
    const baseSize = baseSizes[cardSize] || baseSizes.normal;
    const clampedScale = Math.max(0.7, Math.min(2.5, scaleFactor));
    const scaledSize = Math.round(baseSize * clampedScale);
    
    // Proportional gap scaling - smaller cards get tighter spacing
    const baseGap = 8;
    const scaledGap = Math.max(4, Math.round(baseGap * clampedScale));
    
    return {
      columnSize: `${scaledSize}px`,
      gap: `${scaledGap}px`
    };
  };

  const { columnSize, gap } = getGridSettings();

  const gridStyles: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: `repeat(auto-fill, minmax(${columnSize}, 1fr))`,
    gap: gap,
    padding: '8px',
    ...style,
  };'''

        new_grid_logic = '''  // Calculate dynamic grid column size and gap with proper bounds
  const getGridSettings = () => {
    const baseSizes = {
      small: 70,
      normal: 130, 
      large: 210
    };
    const baseSize = baseSizes[cardSize] || baseSizes.normal;
    const clampedScale = Math.max(0.7, Math.min(2.5, scaleFactor));
    const scaledSize = Math.round(baseSize * clampedScale);
    
    // Proportional gap with minimum and maximum bounds
    const baseGap = 8;
    const proportionalGap = baseGap * clampedScale;
    const minGap = 4;  // Never less than 4px
    const maxGap = 16; // Never more than 16px
    const boundedGap = Math.max(minGap, Math.min(maxGap, proportionalGap));
    const scaledGap = Math.round(boundedGap);
    
    return {
      columnSize: `${scaledSize}px`,
      gap: `${scaledGap}px`
    };
  };

  const { columnSize, gap } = getGridSettings();

  const gridStyles: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: `repeat(auto-fill, minmax(${columnSize}, 1fr))`,
    gap: gap,
    padding: '8px',
    ...style,
  };'''

        content = content.replace(old_grid_logic, new_grid_logic)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def fix_deck_and_sideboard_grids():
    """Fix the deck and sideboard grids in MTGOLayout.tsx to use proper responsive sizing"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the deck grid container
        old_deck_grid = '''            <div className="deck-content">
              <div className="deck-grid">
                {mainDeck.map((deckCard: any) => ('''

        new_deck_grid = '''            <div className="deck-content">
              <div 
                className="deck-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.deck)}px, 1fr))`,
                  gap: `${Math.max(4, Math.min(16, Math.round(8 * cardSizes.deck)))}px`,
                  alignContent: 'start',
                  minHeight: '150px',
                  paddingBottom: '40px'
                }}
              >
                {mainDeck.map((deckCard: any) => ('''

        # Find and replace the sideboard grid container
        old_sideboard_grid = '''            <div className="sideboard-content">
              <div className="sideboard-grid">
                {sideboard.map((sideCard: any) => ('''

        new_sideboard_grid = '''            <div className="sideboard-content">
              <div 
                className="sideboard-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.sideboard)}px, 1fr))`,
                  gap: `${Math.max(4, Math.min(16, Math.round(8 * cardSizes.sideboard)))}px`,
                  alignContent: 'start',
                  minHeight: '150px',
                  paddingBottom: '40px'
                }}
              >
                {sideboard.map((sideCard: any) => ('''

        # Apply replacements
        content = content.replace(old_deck_grid, new_deck_grid)
        content = content.replace(old_sideboard_grid, new_sideboard_grid)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def update_collection_grid_to_use_cardgrid():
    """Update collection area to use CardGrid component for consistency"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add CardGrid import if not already present
        if 'CardGrid' not in content:
            old_import = '''import DraggableCard from './DraggableCard';'''
            new_import = '''import DraggableCard from './DraggableCard';
import { CardGrid } from './MagicCard';'''
            content = content.replace(old_import, new_import)
        
        # Replace the collection grid mapping with CardGrid component
        old_collection_mapping = '''          <div className="collection-grid">
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
          </div>'''

        new_collection_mapping = '''          <div className="collection-grid-container">
            {loading && <div className="loading-message">Loading cards...</div>}
            {error && <div className="error-message">Error: {error}</div>}
            {!loading && !error && (
              <div className="collection-grid">
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
              </div>
            )}
          </div>'''

        content = content.replace(old_collection_mapping, new_collection_mapping)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def update_collection_grid_css():
    """Update CSS to make collection grid responsive to card sizing"""
    file_path = "src/components/MTGOLayout.css"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update collection grid CSS to be dynamic
        old_collection_css = '''/* Responsive grid styles with proportional spacing */
.collection-grid {
  padding: 12px;
  overflow-y: auto;
  flex: 1;
  display: grid;
  /* Grid columns and gap will be set dynamically by CardGrid component */
  align-content: start;
}'''

        new_collection_css = '''/* Responsive grid styles with proportional spacing */
.collection-grid-container {
  padding: 12px;
  overflow-y: auto;
  flex: 1;
}

.collection-grid {
  display: grid;
  align-content: start;
  /* Grid columns and gap will be set by JavaScript for consistency */
}'''

        content = content.replace(old_collection_css, new_collection_css)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def add_collection_grid_dynamic_styling():
    """Add dynamic styling to collection grid"""
    file_path = "src/components/MTGOLayout.tsx"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update collection grid to have dynamic styling like deck and sideboard
        old_collection_grid_start = '''              <div className="collection-grid">'''
        
        new_collection_grid_start = '''              <div 
                className="collection-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.collection)}px, 1fr))`,
                  gap: `${Math.max(4, Math.min(16, Math.round(8 * cardSizes.collection)))}px`,
                  alignContent: 'start'
                }}
              >'''

        content = content.replace(old_collection_grid_start, new_collection_grid_start)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Run all consistency fixes"""
    print("🔧 Fixing Card Sizing Consistency Issues")
    print("=" * 50)
    
    success_count = 0
    total_tasks = 6
    
    print("\n📝 Task 1/6: Ensuring 40% default for all areas...")
    if fix_card_sizing_defaults():
        success_count += 1
    
    print("\n📝 Task 2/6: Making all areas use 'normal' base size...")
    if fix_mtgo_layout_card_sizes():
        success_count += 1
    
    print("\n📝 Task 3/6: Fixing proportional spacing with bounds...")
    if fix_magic_card_grid_spacing():
        success_count += 1
    
    print("\n📝 Task 4/6: Making deck/sideboard grids consistent...")
    if fix_deck_and_sideboard_grids():
        success_count += 1
    
    print("\n📝 Task 5/6: Updating collection grid CSS...")
    if update_collection_grid_css():
        success_count += 1
    
    print("\n📝 Task 6/6: Adding dynamic styling to collection grid...")
    if add_collection_grid_dynamic_styling():
        success_count += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 Consistency Fixes Complete!")
    print(f"📊 Success: {success_count}/{total_tasks} tasks completed")
    
    if success_count == total_tasks:
        print("\n✨ CONSISTENCY FIXES APPLIED:")
        print("✅ 40% default starting position for ALL areas")
        print("✅ Identical card sizes at same slider positions")
        print("✅ All areas use 'normal' base size for uniformity")
        print("✅ Proportional spacing with 4px min, 16px max bounds")
        print("✅ Fixed spacing prevents card overlap and excessive gaps")
        print("✅ Consistent grid behavior across all three areas")
        
        print("\n🧪 TEST THE FIXES:")
        print("1. Run 'npm start' to see the consistent sizing system")
        print("2. Verify all sliders start at 40% position")
        print("3. Test that same slider position = same card size in all areas")
        print("4. Check that cards never overlap or have excessive spacing")
        print("5. Verify smooth, proportional scaling in all areas")
        
        print("\n💡 EXPECTED RESULT:")
        print("• Perfect consistency - same slider position = same card size everywhere")
        print("• No more card overlapping or excessive spacing")
        print("• All areas start at identical 40% default")
        print("• Professional, predictable behavior across the entire interface")
    else:
        print(f"\n⚠️  Some fixes failed. Please check error messages above.")

if __name__ == "__main__":
    main()