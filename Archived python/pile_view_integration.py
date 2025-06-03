#!/usr/bin/env python3
"""
Phase 3D Integration Script: Add Pile View to MTGOLayout.tsx
Integrates the ready-to-use pile view components into the existing layout system.
"""

import os
import sys

def integrate_pile_view():
    """Integrate pile view components into MTGOLayout.tsx"""
    
    # File path
    file_path = r'C:\Users\carol\mtg-deckbuilder\src\components\MTGOLayout.tsx'
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found at {file_path}")
        return False
    
    try:
        # Read the current file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Reading MTGOLayout.tsx ({len(content)} characters)")
        
        # Step 1: Add PileView import to existing imports
        old_import = """// Import components
import { useCards } from '../hooks/useCards';
import { useCardSizing } from '../hooks/useCardSizing';
import DraggableCard from './DraggableCard';
import DropZoneComponent from './DropZone';
import DragPreview from './DragPreview';
import ContextMenu from './ContextMenu';"""

        new_import = """// Import components
import { useCards } from '../hooks/useCards';
import { useCardSizing } from '../hooks/useCardSizing';
import DraggableCard from './DraggableCard';
import DropZoneComponent from './DropZone';
import DragPreview from './DragPreview';
import ContextMenu from './ContextMenu';
import PileView from './PileView';"""

        if old_import in content:
            content = content.replace(old_import, new_import)
            print("✅ Step 1: Added PileView import")
        else:
            print("⚠️ Step 1: Import section not found exactly - manual check needed")
        
        # Step 2: Add Pile button to deck panel header
        old_deck_header = """            <div className="view-controls">
              <span>Size: </span>
              <input
                type="range"
                min="0.7"
                max="2.5"
                step="0.1"
                value={cardSizes.deck}
                onChange={(e) => updateDeckSize(parseFloat(e.target.value))}
                className="size-slider"
                title={`Card size: ${Math.round(cardSizes.deck * 100)}%`}
              />
              <button>Save Deck</button>
              <button onClick={handleClearDeck} title="Clear all cards from deck">
                Clear Deck
              </button>
            </div>"""

        new_deck_header = """            <div className="view-controls">
              <span>Size: </span>
              <input
                type="range"
                min="0.7"
                max="2.5"
                step="0.1"
                value={cardSizes.deck}
                onChange={(e) => updateDeckSize(parseFloat(e.target.value))}
                className="size-slider"
                title={`Card size: ${Math.round(cardSizes.deck * 100)}%`}
              />
              <span>View: </span>
              <button 
                className={layout.viewModes.deck === 'card' ? 'active' : ''}
                onClick={() => updateViewMode('deck', 'card')}
              >
                Card
              </button>
              <button 
                className={layout.viewModes.deck === 'pile' ? 'active' : ''}
                onClick={() => updateViewMode('deck', 'pile')}
              >
                Pile
              </button>
              <button>Save Deck</button>
              <button onClick={handleClearDeck} title="Clear all cards from deck">
                Clear Deck
              </button>
            </div>"""

        if old_deck_header in content:
            content = content.replace(old_deck_header, new_deck_header)
            print("✅ Step 2: Added Pile button to deck header")
        else:
            print("⚠️ Step 2: Deck header controls not found exactly - manual check needed")
            
        # Step 3: Add Pile button to sideboard panel header  
        old_sideboard_header = """            <div className="sideboard-controls">
              <span>Size: </span>
              <input
                type="range"
                min="0.7"
                max="2.5"
                step="0.1"
                value={cardSizes.sideboard}
                onChange={(e) => updateSideboardSize(parseFloat(e.target.value))}
                className="size-slider"
                title={`Card size: ${Math.round(cardSizes.sideboard * 100)}%`}
              />
              <button onClick={handleClearSideboard} title="Clear all cards from sideboard">
                Clear
              </button>
            </div>"""

        new_sideboard_header = """            <div className="sideboard-controls">
              <span>Size: </span>
              <input
                type="range"
                min="0.7"
                max="2.5"
                step="0.1"
                value={cardSizes.sideboard}
                onChange={(e) => updateSideboardSize(parseFloat(e.target.value))}
                className="size-slider"
                title={`Card size: ${Math.round(cardSizes.sideboard * 100)}%`}
              />
              <span>View: </span>
              <button 
                className={layout.viewModes.sideboard === 'card' ? 'active' : ''}
                onClick={() => updateViewMode('sideboard', 'card')}
              >
                Card
              </button>
              <button 
                className={layout.viewModes.sideboard === 'pile' ? 'active' : ''}
                onClick={() => updateViewMode('sideboard', 'pile')}
              >
                Pile
              </button>
              <button onClick={handleClearSideboard} title="Clear all cards from sideboard">
                Clear
              </button>
            </div>"""

        if old_sideboard_header in content:
            content = content.replace(old_sideboard_header, new_sideboard_header)
            print("✅ Step 3: Added Pile button to sideboard header")
        else:
            print("⚠️ Step 3: Sideboard header controls not found exactly - manual check needed")
            
        # Step 4: Add conditional rendering for deck area
        old_deck_content = """            <div className="deck-content">
              <div 
                className="deck-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.deck)}px, 1fr))`,
                  gap: `${Math.round(4 * cardSizes.deck)}px`,
                  alignContent: 'start',
                  minHeight: '150px',
                  paddingBottom: '40px'
                }}
              >
                {mainDeck.map((deckCard: any) => (
                  <DraggableCard
                    key={deckCard.id}
                    card={deckCard}
                    zone="deck"
                    size="normal"
                    scaleFactor={cardSizes.deck}
                    onClick={(card, event) => handleCardClick(card, event)}
                    onEnhancedDoubleClick={handleDoubleClick}
                    onRightClick={handleRightClick}
                    onDragStart={handleDragStart}
                    showQuantity={true}
                    quantity={deckCard.quantity}
                    selected={isSelected(deckCard.id)}
                    selectable={true}
                    isDragActive={dragState.isDragging}
                    isBeingDragged={dragState.draggedCards.some(dc => dc.id === deckCard.id)}
                    selectedCards={getSelectedCardObjects()}
                  />
                ))}
                {mainDeck.length === 0 && (
                  <div className="empty-deck-message">
                    Double-click or drag cards from the collection to add them to your deck
                  </div>
                )}
              </div>
            </div>"""

        new_deck_content = """            <div className="deck-content">
              {layout.viewModes.deck === 'pile' ? (
                <PileView
                  cards={mainDeck}
                  zone="deck"
                  scaleFactor={cardSizes.deck}
                  onClick={(card, event) => handleCardClick(card, event)}
                  onDoubleClick={handleAddToDeck}
                  onEnhancedDoubleClick={handleDoubleClick}
                  onRightClick={handleRightClick}
                  onDragStart={handleDragStart}
                  isSelected={isSelected}
                  selectedCards={getSelectedCardObjects()}
                  isDragActive={dragState.isDragging}
                  onDragEnter={handleDragEnter}
                  onDragLeave={handleDragLeave}
                  canDropInZone={canDropInZone}
                />
              ) : (
                <div 
                  className="deck-grid"
                  style={{
                    display: 'grid',
                    gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.deck)}px, 1fr))`,
                    gap: `${Math.round(4 * cardSizes.deck)}px`,
                    alignContent: 'start',
                    minHeight: '150px',
                    paddingBottom: '40px'
                  }}
                >
                  {mainDeck.map((deckCard: any) => (
                    <DraggableCard
                      key={deckCard.id}
                      card={deckCard}
                      zone="deck"
                      size="normal"
                      scaleFactor={cardSizes.deck}
                      onClick={(card, event) => handleCardClick(card, event)}
                      onEnhancedDoubleClick={handleDoubleClick}
                      onRightClick={handleRightClick}
                      onDragStart={handleDragStart}
                      showQuantity={true}
                      quantity={deckCard.quantity}
                      selected={isSelected(deckCard.id)}
                      selectable={true}
                      isDragActive={dragState.isDragging}
                      isBeingDragged={dragState.draggedCards.some(dc => dc.id === deckCard.id)}
                      selectedCards={getSelectedCardObjects()}
                    />
                  ))}
                  {mainDeck.length === 0 && (
                    <div className="empty-deck-message">
                      Double-click or drag cards from the collection to add them to your deck
                    </div>
                  )}
                </div>
              )}
            </div>"""

        if old_deck_content in content:
            content = content.replace(old_deck_content, new_deck_content)
            print("✅ Step 4: Added conditional rendering for deck area")
        else:
            print("⚠️ Step 4: Deck content area not found exactly - manual check needed")
            
        # Step 5: Add conditional rendering for sideboard area
        old_sideboard_content = """            <div className="sideboard-content">
              <div 
                className="sideboard-grid"
                style={{
                  display: 'grid',
                  gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.sideboard)}px, 1fr))`,
                  gap: `${Math.round(4 * cardSizes.sideboard)}px`,
                  alignContent: 'start',
                  minHeight: '150px',
                  paddingBottom: '40px'
                }}
              >
                {sideboard.map((sideCard: any) => (
                  <DraggableCard
                    key={sideCard.id}
                    card={sideCard}
                    zone="sideboard"
                    size="normal"
                    scaleFactor={cardSizes.sideboard}
                    onClick={(card, event) => handleCardClick(card, event)}
                    onEnhancedDoubleClick={handleDoubleClick}
                    onRightClick={handleRightClick}
                    onDragStart={handleDragStart}
                    showQuantity={true}
                    quantity={sideCard.quantity}
                    selected={isSelected(sideCard.id)}
                    selectable={true}
                    isDragActive={dragState.isDragging}
                    isBeingDragged={dragState.draggedCards.some(dc => dc.id === sideCard.id)}
                    selectedCards={getSelectedCardObjects()}
                  />
                ))}
                {sideboard.length === 0 && (
                  <div className="empty-sideboard-message">
                    Drag cards here for your sideboard
                  </div>
                )}
              </div>
            </div>"""

        new_sideboard_content = """            <div className="sideboard-content">
              {layout.viewModes.sideboard === 'pile' ? (
                <PileView
                  cards={sideboard}
                  zone="sideboard"
                  scaleFactor={cardSizes.sideboard}
                  onClick={(card, event) => handleCardClick(card, event)}
                  onDoubleClick={handleAddToDeck}
                  onEnhancedDoubleClick={handleDoubleClick}
                  onRightClick={handleRightClick}
                  onDragStart={handleDragStart}
                  isSelected={isSelected}
                  selectedCards={getSelectedCardObjects()}
                  isDragActive={dragState.isDragging}
                  onDragEnter={handleDragEnter}
                  onDragLeave={handleDragLeave}
                  canDropInZone={canDropInZone}
                />
              ) : (
                <div 
                  className="sideboard-grid"
                  style={{
                    display: 'grid',
                    gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.sideboard)}px, 1fr))`,
                    gap: `${Math.round(4 * cardSizes.sideboard)}px`,
                    alignContent: 'start',
                    minHeight: '150px',
                    paddingBottom: '40px'
                  }}
                >
                  {sideboard.map((sideCard: any) => (
                    <DraggableCard
                      key={sideCard.id}
                      card={sideCard}
                      zone="sideboard"
                      size="normal"
                      scaleFactor={cardSizes.sideboard}
                      onClick={(card, event) => handleCardClick(card, event)}
                      onEnhancedDoubleClick={handleDoubleClick}
                      onRightClick={handleRightClick}
                      onDragStart={handleDragStart}
                      showQuantity={true}
                      quantity={sideCard.quantity}
                      selected={isSelected(sideCard.id)}
                      selectable={true}
                      isDragActive={dragState.isDragging}
                      isBeingDragged={dragState.draggedCards.some(dc => dc.id === sideCard.id)}
                      selectedCards={getSelectedCardObjects()}
                    />
                  ))}
                  {sideboard.length === 0 && (
                    <div className="empty-sideboard-message">
                      Drag cards here for your sideboard
                    </div>
                  )}
                </div>
              )}
            </div>"""

        if old_sideboard_content in content:
            content = content.replace(old_sideboard_content, new_sideboard_content)
            print("✅ Step 5: Added conditional rendering for sideboard area")
        else:
            print("⚠️ Step 5: Sideboard content area not found exactly - manual check needed")
            
        # Step 6: Add updateViewMode to the layout destructuring
        old_layout_destructure = "  const { layout, updatePanelDimensions, updateDeckAreaHeightByPixels, constraints } = useLayout();"
        new_layout_destructure = "  const { layout, updatePanelDimensions, updateDeckAreaHeightByPixels, updateViewMode, constraints } = useLayout();"
        
        if old_layout_destructure in content:
            content = content.replace(old_layout_destructure, new_layout_destructure)
            print("✅ Step 6: Added updateViewMode to layout destructuring")
        else:
            print("⚠️ Step 6: Layout destructuring not found exactly - manual check needed")
        
        # Write the updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Integration complete! Updated MTGOLayout.tsx ({len(content)} characters)")
        print("\n🎯 Next steps:")
        print("1. Add CSS styles for pile view components")
        print("2. Test the pile view toggle functionality")
        print("3. Verify all interactions work correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during integration: {e}")
        return False

def add_pile_view_styles():
    """Add CSS styles for pile view components to MTGOLayout.css"""
    
    file_path = r'C:\Users\carol\mtg-deckbuilder\src\components\MTGOLayout.css'
    
    if not os.path.exists(file_path):
        print(f"❌ Error: CSS file not found at {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📁 Reading MTGOLayout.css ({len(content)} characters)")
        
        # Add pile view styles at the end of the file
        pile_view_styles = """

/* PHASE 3D: Pile View Styles */

/* Pile View Container */
.pile-view {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

/* Sort Controls */
.pile-sort-controls {
  padding: 8px 12px;
  background-color: #333333;
  border-bottom: 1px solid #555555;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.sort-label {
  color: #cccccc;
  font-weight: 600;
}

.sort-button {
  background-color: #404040;
  color: #ffffff;
  border: 1px solid #555555;
  padding: 4px 8px;
  border-radius: 3px;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sort-button:hover {
  background-color: #4a4a4a;
  transform: scale(1.02);
}

.sort-button.active {
  background-color: #3b82f6;
  border-color: #2563eb;
  box-shadow: 0 0 0 1px #2563eb;
}

/* Pile Columns Container */
.pile-columns-container {
  flex: 1;
  display: flex;
  overflow-x: auto;
  overflow-y: hidden;
  padding: 8px;
  gap: 12px;
  align-items: flex-start;
}

/* Individual Pile Column */
.pile-column {
  min-width: 150px;
  max-width: 200px;
  background-color: rgba(255, 255, 255, 0.02);
  border: 1px solid #404040;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  height: fit-content;
  max-height: 100%;
}

.pile-column.empty-column {
  min-width: 100px;
  background-color: rgba(255, 255, 255, 0.01);
  border: 1px dashed #555555;
  border-radius: 6px;
  min-height: 120px;
}

/* Column Header */
.pile-column-header {
  padding: 6px 10px;
  background-color: #404040;
  font-size: 11px;
  font-weight: bold;
  text-align: center;
  border-bottom: 1px solid #555555;
  color: #ffffff;
  border-radius: 5px 5px 0 0;
}

/* Column Content */
.pile-column-content {
  flex: 1;
  padding: 6px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  overflow-y: auto;
  max-height: 400px;
}

.empty-column-placeholder {
  text-align: center;
  color: #666666;
  font-size: 11px;
  font-style: italic;
  padding: 20px 10px;
  border: 1px dashed #555555;
  border-radius: 4px;
  margin: 8px;
}

/* Pile Column Scrollbar */
.pile-column-content::-webkit-scrollbar {
  width: 4px;
}

.pile-column-content::-webkit-scrollbar-track {
  background-color: #1a1a1a;
  border-radius: 2px;
}

.pile-column-content::-webkit-scrollbar-thumb {
  background-color: #404040;
  border-radius: 2px;
}

.pile-column-content::-webkit-scrollbar-thumb:hover {
  background-color: #555555;
}

/* Pile Columns Container Scrollbar */
.pile-columns-container::-webkit-scrollbar {
  height: 8px;
}

.pile-columns-container::-webkit-scrollbar-track {
  background-color: #1a1a1a;
  border-radius: 4px;
}

.pile-columns-container::-webkit-scrollbar-thumb {
  background-color: #404040;
  border-radius: 4px;
}

.pile-columns-container::-webkit-scrollbar-thumb:hover {
  background-color: #555555;
}

/* Cards in Pile View */
.pile-view .draggable-card {
  margin-bottom: 2px;
}

/* Responsive Design for Pile View */
@media (max-width: 1200px) {
  .pile-column {
    min-width: 120px;
    max-width: 150px;
  }
  
  .pile-sort-controls {
    flex-wrap: wrap;
    gap: 4px;
  }
  
  .sort-button {
    font-size: 10px;
    padding: 3px 6px;
  }
}

@media (max-width: 900px) {
  .pile-view {
    display: none; /* Hide pile view on very small screens */
  }
}
"""

        # Add the styles to the end of the file
        content += pile_view_styles
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ CSS styles added! Updated MTGOLayout.css ({len(content)} characters)")
        return True
        
    except Exception as e:
        print(f"❌ Error adding CSS styles: {e}")
        return False

def main():
    print("🚀 Phase 3D Integration: Adding Pile View to MTGOLayout")
    print("=" * 60)
    
    # Step 1: Integrate pile view into MTGOLayout.tsx
    if not integrate_pile_view():
        print("❌ Integration failed - stopping")
        return
    
    print()
    
    # Step 2: Add CSS styles for pile view
    if not add_pile_view_styles():
        print("❌ CSS integration failed")
        return
    
    print()
    print("🎉 Phase 3D Integration Complete!")
    print("✅ Pile view components integrated into MTGOLayout")
    print("✅ View toggle buttons added to deck and sideboard headers")
    print("✅ Conditional rendering implemented for both views")
    print("✅ CSS styles added for professional pile view appearance")
    print()
    print("🧪 Testing Instructions:")
    print("1. Run `npm start` to test the application")
    print("2. Try clicking 'Pile' buttons in deck and sideboard headers")
    print("3. Test drag & drop between pile columns and collection")
    print("4. Verify all 4 sort criteria work (Mana, Color, Rarity, Type)")
    print("5. Check that card sizing sliders affect pile view cards")
    print("6. Confirm view preferences persist between sessions")

if __name__ == "__main__":
    main()
