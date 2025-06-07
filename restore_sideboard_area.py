#!/usr/bin/env python3

import os
import sys

def restore_sideboard_area(filename):
    """Restore missing sideboard area to MTGOLayout component"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the insertion point - after the deck area's resize handle
    insertion_point = '''            {/* Resize Handle */}
            <div 
              className="resize-handle resize-handle-left"
              onMouseDown={resizeHandlers.onSideboardResize}
              title="Drag to resize sideboard"
              style={{
                position: 'absolute',
                top: 0,
                left: -3,
                width: 6,
                height: '100%',
                cursor: 'ew-resize',
                background: 'linear-gradient(90deg, transparent 0%, #555555 50%, transparent 100%)',
                zIndex: 1001,
                opacity: 0.7,
                transition: 'opacity 0.2s ease'
              }}
              onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
              onMouseLeave={(e) => e.currentTarget.style.opacity = '0.7'}
            />
          </DropZoneComponent>
        </div>
      </div>'''

    # The complete sideboard area to insert
    sideboard_area = '''            {/* Resize Handle */}
            <div 
              className="resize-handle resize-handle-left"
              onMouseDown={resizeHandlers.onSideboardResize}
              title="Drag to resize sideboard"
              style={{
                position: 'absolute',
                top: 0,
                left: -3,
                width: 6,
                height: '100%',
                cursor: 'ew-resize',
                background: 'linear-gradient(90deg, transparent 0%, #555555 50%, transparent 100%)',
                zIndex: 1001,
                opacity: 0.7,
                transition: 'opacity 0.2s ease'
              }}
              onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
              onMouseLeave={(e) => e.currentTarget.style.opacity = '0.7'}
            />
          </DropZoneComponent>
          
          {/* Sideboard Area */}
          <DropZoneComponent
            zone="sideboard"
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            canDrop={canDropInZone('sideboard', dragState.draggedCards)}
            isDragActive={dragState.isDragging}
            className="mtgo-sideboard-area"
          >
            <div className="panel-header">
              <h3>Sideboard ({sideboard.length} cards)</h3>
              <div className="sideboard-controls">
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
                <div className="sort-button-container" ref={sideboardSortRef}>
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
                        className={sideboardSort.criteria === 'mana' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSort.criteria === 'mana') {
                            updateSort('sideboard', 'mana', sideboardSort.direction === 'asc' ? 'desc' : 'asc');
                          } else {
                            updateSort('sideboard', 'mana', 'asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Mana Value {sideboardSort.criteria === 'mana' && layout.viewModes.sideboard === 'card' ? (sideboardSort.direction === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={sideboardSort.criteria === 'color' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSort.criteria === 'color') {
                            updateSort('sideboard', 'color', sideboardSort.direction === 'asc' ? 'desc' : 'asc');
                          } else {
                            updateSort('sideboard', 'color', 'asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Color {sideboardSort.criteria === 'color' && layout.viewModes.sideboard === 'card' ? (sideboardSort.direction === 'asc' ? '↑' : '↓') : ''}
                      </button>
                      <button 
                        className={sideboardSort.criteria === 'rarity' ? 'active' : ''}
                        onClick={() => { 
                          if (layout.viewModes.sideboard === 'card' && sideboardSort.criteria === 'rarity') {
                            updateSort('sideboard', 'rarity', sideboardSort.direction === 'asc' ? 'desc' : 'asc');
                          } else {
                            updateSort('sideboard', 'rarity', 'asc');
                          }
                          setShowSideboardSortMenu(false); 
                        }}
                      >
                        Rarity {sideboardSort.criteria === 'rarity' && layout.viewModes.sideboard === 'card' ? (sideboardSort.direction === 'asc' ? '↑' : '↓') : ''}
                      </button>
                    </div>
                  )}
                </div>
                <span>View: </span>
                <button 
                  className={layout.viewModes.sideboard === 'card' ? 'active' : ''}
                  onClick={() => { clearSelection(); updateViewMode('sideboard', 'card'); }}
                >
                  Card
                </button>
                <button 
                  className={layout.viewModes.sideboard === 'pile' ? 'active' : ''}
                  onClick={() => { clearSelection(); updateViewMode('sideboard', 'pile'); }}
                >
                  Pile
                </button>
                <button 
                  className={layout.viewModes.sideboard === 'list' ? 'active' : ''}
                  onClick={() => { clearSelection(); updateViewMode('sideboard', 'list'); }}
                >
                  List
                </button>
                <button onClick={handleClearSideboard} title="Clear all cards from sideboard">
                  Clear
                </button>
              </div>
            </div>
            
            <div className="sideboard-content">
              {layout.viewModes.sideboard === 'pile' ? (
                <PileView
                  cards={sideboard}
                  zone="sideboard"
                  scaleFactor={cardSizes.sideboard}
                  forcedSortCriteria={sideboardSort.criteria === 'name' || sideboardSort.criteria === 'type' ? 'mana' : sideboardSort.criteria as any}
                  onClick={(card, event) => handleCardClick(card, event)}
                  onInstanceClick={handleInstanceClick}
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
                  sortCriteria={sideboardSort.criteria}
                  sortDirection={sideboardSort.direction}
                  onSortChange={(criteria, direction) => {
                    if (criteria === 'name' || criteria === 'mana' || criteria === 'color' || criteria === 'rarity') {
                      updateSort('sideboard', criteria, direction);
                    }
                  }}
                  onClick={(card, event) => handleCardClick(card, event)}
                  onDoubleClick={(card) => handleDoubleClick(card as any, 'sideboard', { preventDefault: () => {}, stopPropagation: () => {} } as React.MouseEvent)}
                  onRightClick={handleRightClick}
                  onDragStart={handleDragStart}
                  isSelected={isSelected}
                  selectedCards={getSelectedCardObjects()}
                  isDragActive={dragState.isDragging}
                  onQuantityChange={(cardId, newQuantity) => {
                    if (newQuantity === 0) {
                      setSideboard(prev => prev.filter(instance => instance.cardId !== cardId));
                    } else {
                      const currentQuantity = getSideboardQuantity(cardId);
                      const diff = newQuantity - currentQuantity;
                      
                      if (diff > 0) {
                        const cardData = cards.find(c => c.id === cardId);
                        if (cardData) {
                          const newInstances: DeckCardInstance[] = [];
                          for (let i = 0; i < diff; i++) {
                            newInstances.push(createDeckInstance(cardData, 'sideboard'));
                          }
                          setSideboard(prev => [...prev, ...newInstances]);
                        }
                      } else if (diff < 0) {
                        setSideboard(prev => removeInstancesForCard(prev, cardId, Math.abs(diff)));
                      }
                    }
                  }}
                />
              ) : (
                <div 
                  className="sideboard-grid"
                  style={{
                    display: 'grid',
                    gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.sideboard)}px, max-content))`,
                    gap: `${Math.round(4 * cardSizes.sideboard)}px`,
                    alignContent: 'start',
                    minHeight: '150px',
                    paddingBottom: '40px'
                  }}
                >
                  {(() => {
                    // Group instances by cardId for clean stacking
                    const groupedCards = new Map<string, DeckCardInstance[]>();
                    sortedSideboard.forEach(instance => {
                      const cardId = instance.cardId;
                      if (!groupedCards.has(cardId)) {
                        groupedCards.set(cardId, []);
                      }
                      groupedCards.get(cardId)!.push(instance);
                    });

                    return Array.from(groupedCards.entries()).map(([cardId, instances]) => {
                      const representativeCard = instances[0];
                      const quantity = instances.length;
                      const isAnySelected = instances.some(instance => isSelected(instance.instanceId));

                      const handleStackClick = (card: any, event?: React.MouseEvent) => {
                        if (instances.length > 1) {
                          const unselectedInstance = instances.find(inst => !isSelected(inst.instanceId));
                          const targetInstance = unselectedInstance || instances[0];
                          handleInstanceClick(targetInstance.instanceId, targetInstance, event as React.MouseEvent);
                        } else {
                          handleInstanceClick(representativeCard.instanceId, representativeCard, event as React.MouseEvent);
                        }
                      };

                      const handleStackInstanceClick = (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => {
                        handleStackClick(instance, event);
                      };

                      const handleStackDragStart = (cards: any[], zone: any, event: React.MouseEvent) => {
                        handleDragStart(instances as any[], zone, event);
                      };

                      return (
                        <DraggableCard
                          key={cardId}
                          card={representativeCard}
                          zone="sideboard"
                          size="normal"
                          scaleFactor={cardSizes.sideboard}
                          onClick={handleStackClick}
                          instanceId={representativeCard.instanceId}
                          isInstance={true}
                          onInstanceClick={handleStackInstanceClick}
                          onEnhancedDoubleClick={handleDoubleClick}
                          onRightClick={handleRightClick}
                          onDragStart={handleStackDragStart}
                          showQuantity={true}
                          quantity={quantity}
                          selected={isAnySelected}
                          selectable={true}
                          isDragActive={dragState.isDragging}
                          isBeingDragged={dragState.draggedCards.some(dc => 
                            instances.some(inst => 
                              'instanceId' in dc ? dc.instanceId === inst.instanceId : dc.id === inst.cardId
                            )
                          )}
                          selectedCards={getSelectedCardObjects()}
                        />
                      );
                    });
                  })()}
                  
                  {sideboard.length === 0 && (
                    <div className="empty-sideboard-message">
                      Drag cards here for your sideboard
                    </div>
                  )}
                </div>
              )}
            </div>
          </DropZoneComponent>
        </div>
      </div>'''

    # Make the replacement
    if insertion_point in content:
        content = content.replace(insertion_point, sideboard_area)
        print("✅ Added complete sideboard area with all view modes and controls")
    else:
        print("❌ Could not find insertion point for sideboard area")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully restored sideboard area to {filename}")
    return True

if __name__ == "__main__":
    success = restore_sideboard_area("src/components/MTGOLayout.tsx")
    sys.exit(0 if success else 1)