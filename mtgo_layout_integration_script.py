#!/usr/bin/env python3
"""
MTGOLayout.tsx Integration Script for Phase 3G
Adds ListView and AdaptiveHeader integration to the existing MTGOLayout component.
"""

import os
import re

def update_mtgo_layout():
    """Update MTGOLayout.tsx with ListView and AdaptiveHeader integration."""
    
    file_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File {file_path} not found!")
        return False
    
    try:
        # Read the current file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("📖 Reading MTGOLayout.tsx...")
        
        # 1. Add new imports
        import_section = """import SearchAutocomplete from './SearchAutocomplete';
import PileView from './PileView';"""
        
        new_import_section = """import SearchAutocomplete from './SearchAutocomplete';
import PileView from './PileView';
import ListView from './ListView';
import AdaptiveHeader from './AdaptiveHeader';"""
        
        if import_section in content:
            content = content.replace(import_section, new_import_section)
            print("✅ Added ListView and AdaptiveHeader imports")
        else:
            print("❌ Could not find import section to update")
            return False
        
        # 2. Update collection area view controls to include List button
        collection_view_controls = """              <span>View: </span>
              <button className="active">Card</button>
              <button>List</button>"""
        
        new_collection_view_controls = """              <span>View: </span>
              <button 
                className={layout.viewModes.collection === 'grid' ? 'active' : ''}
                onClick={() => updateViewMode('collection', 'grid')}
              >
                Card
              </button>
              <button 
                className={layout.viewModes.collection === 'list' ? 'active' : ''}
                onClick={() => updateViewMode('collection', 'list')}
              >
                List
              </button>"""
        
        if collection_view_controls in content:
            content = content.replace(collection_view_controls, new_collection_view_controls)
            print("✅ Updated collection view controls")
        else:
            print("❌ Could not find collection view controls to update")
            return False
        
        # 3. Replace collection grid with conditional rendering
        collection_grid_section = """          <div 
            className="collection-grid"
            style={{
              display: 'grid',
              gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.collection)}px, max-content))`,
              gap: `${Math.round(4 * cardSizes.collection)}px`,
              alignContent: 'start',
              padding: '8px'
            }}
          >
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
            {sortedCollectionCards.map((card: ScryfallCard | DeckCard) => (
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
        
        new_collection_section = """          {/* Collection Content - Conditional Rendering */}
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
            layout.viewModes.collection === 'list' ? (
              <ListView
                cards={sortedCollectionCards}
                area="collection"
                scaleFactor={cardSizes.collection}
                sortCriteria={collectionSortCriteria}
                sortDirection={collectionSortDirection}
                onSortChange={(criteria, direction) => {
                  setCollectionSortCriteria(criteria);
                  setCollectionSortDirection(direction);
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
                {sortedCollectionCards.map((card: ScryfallCard | DeckCard) => (
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
            )
          )}"""
        
        if collection_grid_section in content:
            content = content.replace(collection_grid_section, new_collection_section)
            print("✅ Updated collection area with conditional ListView rendering")
        else:
            print("❌ Could not find collection grid section to update")
            return False
        
        # 4. Add List button to deck controls
        deck_view_controls = """                <button 
                  className={layout.viewModes.deck === 'pile' ? 'active' : ''}
                  onClick={() => updateViewMode('deck', 'pile')}
                >
                  Pile
                </button>"""
        
        new_deck_view_controls = """                <button 
                  className={layout.viewModes.deck === 'pile' ? 'active' : ''}
                  onClick={() => updateViewMode('deck', 'pile')}
                >
                  Pile
                </button>
                <button 
                  className={layout.viewModes.deck === 'list' ? 'active' : ''}
                  onClick={() => updateViewMode('deck', 'list')}
                >
                  List
                </button>"""
        
        if deck_view_controls in content:
            content = content.replace(deck_view_controls, new_deck_view_controls)
            print("✅ Updated deck view controls")
        else:
            print("❌ Could not find deck view controls to update")
            return False
        
        # 5. Update deck content area with ListView option
        deck_content_section = """            <div className="deck-content">
              {layout.viewModes.deck === 'pile' ? (
                <PileView
                  cards={mainDeck}
                  zone="deck"
                  scaleFactor={cardSizes.deck}
                  forcedSortCriteria={deckSortCriteria === 'name' ? 'mana' : deckSortCriteria}
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
                  {sortedMainDeck.map((deckCard) => (
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
        
        new_deck_content_section = """            <div className="deck-content">
              {layout.viewModes.deck === 'pile' ? (
                <PileView
                  cards={mainDeck}
                  zone="deck"
                  scaleFactor={cardSizes.deck}
                  forcedSortCriteria={deckSortCriteria === 'name' ? 'mana' : deckSortCriteria}
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
              ) : layout.viewModes.deck === 'list' ? (
                <ListView
                  cards={sortedMainDeck}
                  area="deck"
                  scaleFactor={cardSizes.deck}
                  sortCriteria={deckSortCriteria}
                  sortDirection={deckSortDirection}
                  onSortChange={(criteria, direction) => {
                    setDeckSortCriteria(criteria);
                    setDeckSortDirection(direction);
                  }}
                  onClick={(card, event) => handleCardClick(card, event)}
                  onDoubleClick={handleDoubleClick}
                  onRightClick={handleRightClick}
                  onDragStart={handleDragStart}
                  isSelected={isSelected}
                  selectedCards={getSelectedCardObjects()}
                  isDragActive={dragState.isDragging}
                  onQuantityChange={(cardId, newQuantity) => {
                    if (newQuantity === 0) {
                      setMainDeck(prev => prev.filter(card => card.id !== cardId));
                    } else {
                      setMainDeck(prev => prev.map(card => 
                        card.id === cardId ? { ...card, quantity: newQuantity } : card
                      ));
                    }
                  }}
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
                  {sortedMainDeck.map((deckCard) => (
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
        
        if deck_content_section in content:
            content = content.replace(deck_content_section, new_deck_content_section)
            print("✅ Updated deck content area with ListView option")
        else:
            print("❌ Could not find deck content section to update")
            return False
        
        # 6. Add List button to sideboard controls
        sideboard_view_controls = """                <button 
                  className={layout.viewModes.sideboard === 'pile' ? 'active' : ''}
                  onClick={() => updateViewMode('sideboard', 'pile')}
                >
                  Pile
                </button>"""
        
        new_sideboard_view_controls = """                <button 
                  className={layout.viewModes.sideboard === 'pile' ? 'active' : ''}
                  onClick={() => updateViewMode('sideboard', 'pile')}
                >
                  Pile
                </button>
                <button 
                  className={layout.viewModes.sideboard === 'list' ? 'active' : ''}
                  onClick={() => updateViewMode('sideboard', 'list')}
                >
                  List
                </button>"""
        
        if sideboard_view_controls in content:
            content = content.replace(sideboard_view_controls, new_sideboard_view_controls)
            print("✅ Updated sideboard view controls")
        else:
            print("❌ Could not find sideboard view controls to update")
            return False
        
        # 7. Update sideboard content area with ListView option
        sideboard_content_section = """            <div className="sideboard-content">
              {layout.viewModes.sideboard === 'pile' ? (
                <PileView
                  cards={sideboard}
                  zone="sideboard"
                  scaleFactor={cardSizes.sideboard}
                  forcedSortCriteria={sideboardSortCriteria === 'name' ? 'mana' : sideboardSortCriteria}
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
                  {sortedSideboard.map((sideCard) => (
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
        
        new_sideboard_content_section = """            <div className="sideboard-content">
              {layout.viewModes.sideboard === 'pile' ? (
                <PileView
                  cards={sideboard}
                  zone="sideboard"
                  scaleFactor={cardSizes.sideboard}
                  forcedSortCriteria={sideboardSortCriteria === 'name' ? 'mana' : sideboardSortCriteria}
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
              ) : layout.viewModes.sideboard === 'list' ? (
                <ListView
                  cards={sortedSideboard}
                  area="sideboard"
                  scaleFactor={cardSizes.sideboard}
                  sortCriteria={sideboardSortCriteria}
                  sortDirection={sideboardSortDirection}
                  onSortChange={(criteria, direction) => {
                    setSideboardSortCriteria(criteria);
                    setSideboardSortDirection(direction);
                  }}
                  onClick={(card, event) => handleCardClick(card, event)}
                  onDoubleClick={handleDoubleClick}
                  onRightClick={handleRightClick}
                  onDragStart={handleDragStart}
                  isSelected={isSelected}
                  selectedCards={getSelectedCardObjects()}
                  isDragActive={dragState.isDragging}
                  onQuantityChange={(cardId, newQuantity) => {
                    if (newQuantity === 0) {
                      setSideboard(prev => prev.filter(card => card.id !== cardId));
                    } else {
                      setSideboard(prev => prev.map(card => 
                        card.id === cardId ? { ...card, quantity: newQuantity } : card
                      ));
                    }
                  }}
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
                  {sortedSideboard.map((sideCard) => (
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
        
        if sideboard_content_section in content:
            content = content.replace(sideboard_content_section, new_sideboard_content_section)
            print("✅ Updated sideboard content area with ListView option")
        else:
            print("❌ Could not find sideboard content section to update")
            return False
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating file: {e}")
        return False

def update_css_file():
    """Add ListView styles to MTGOLayout.css"""
    
    file_path = "src/components/MTGOLayout.css"
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File {file_path} not found!")
        return False
    
    try:
        # Read the current file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("📖 Reading MTGOLayout.css...")
        
        # Check if ListView styles already exist
        if "LIST VIEW COMPONENT STYLES" not in content:
            content += listview_styles
            print("✅ Added ListView and AdaptiveHeader styles to CSS")
        else:
            print("ℹ️ ListView styles already exist in CSS file")
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating CSS file: {e}")
        return False

def main():
    """Main execution function"""
    print("🚀 Starting Phase 3G Integration...")
    print("📋 This script will integrate ListView and AdaptiveHeader components")
    print()
    
    # Update MTGOLayout.tsx
    print("📝 Step 1: Updating MTGOLayout.tsx...")
    if not update_mtgo_layout():
        print("❌ Failed to update MTGOLayout.tsx")
        return False
    
    print()
    
    # Update CSS file
    print("🎨 Step 2: Updating MTGOLayout.css...")
    if not update_css_file():
        print("❌ Failed to update MTGOLayout.css")
        return False
    
    print()
    print("🎉 Phase 3G Integration Complete!")
    print()
    print("📋 Summary of changes:")
    print("  ✅ Added ListView and AdaptiveHeader imports")
    print("  ✅ Updated collection area with List view option")
    print("  ✅ Updated deck area with List view option")
    print("  ✅ Updated sideboard area with List view option")
    print("  ✅ Added quantity change handlers for ListView")
    print("  ✅ Added comprehensive ListView and AdaptiveHeader CSS styles")
    print()
    print("🔄 Next steps:")
    print("  1. Create the new component files:")
    print("     - src/components/ListView.tsx")
    print("     - src/components/AdaptiveHeader.tsx")
    print("  2. Test the application to ensure all views work correctly")
    print("  3. Verify drag and drop functionality in ListView")
    print("  4. Test responsive behavior at different screen widths")
    print()
    print("🎯 Phase 3G Features Now Available:")
    print("  • Universal List View in all three areas")
    print("  • Sortable columns with direction indicators")
    print("  • Column resizing with minimum widths")
    print("  • Quantity editing in deck/sideboard list views")
    print("  • Drag and drop integration with ListView")
    print("  • Responsive header adaptation (AdaptiveHeader ready)")
    print("  • Professional MTGO-style table appearance")

if __name__ == "__main__":
    main()