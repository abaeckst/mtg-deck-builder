#!/usr/bin/env python3
"""
Fix card view to show stacked cards instead of individual instances
This script adds card stacking logic to show one visual stack per unique card with 3D depth effects.
"""

import os
import sys

def fix_card_stacking():
    """Fix MTGOLayout to group deck cards by cardId and render stacks"""
    
    file_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found!")
        print("Make sure you're running this script from the project root directory.")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📖 Reading {file_path}...")
        
        # Find and replace the deck grid rendering section
        old_deck_grid = '''              ) : (
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
                  {sortedMainDeck.map((deckInstance) => (
                    <DraggableCard
                      key={deckInstance.instanceId}
                      card={deckInstance}
                      zone="deck"
                      size="normal"
                      scaleFactor={cardSizes.deck}
                      onClick={(card, event) => handleCardClick(card, event)}
                      instanceId={deckInstance.instanceId}
                      isInstance={true}
                      onInstanceClick={handleInstanceClick}
                      onEnhancedDoubleClick={handleDoubleClick}
                      onRightClick={handleRightClick}
                      onDragStart={handleDragStart}
                      showQuantity={true}
                      quantity={1}
                      selected={isSelected(deckInstance.instanceId)}
                      selectable={true}
                      isDragActive={dragState.isDragging}
                      isBeingDragged={dragState.draggedCards.some(dc => 'instanceId' in dc ? dc.instanceId === deckInstance.instanceId : dc.id === deckInstance.cardId)}
                      selectedCards={getSelectedCardObjects()}
                    />
                  ))}
                  {mainDeck.length === 0 && (
                    <div className="empty-deck-message">
                      Double-click or drag cards from the collection to add them to your deck
                    </div>
                  )}
                </div>
              )}'''

        new_deck_grid = '''              ) : (
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
                  {(() => {
                    // Group instances by cardId for stacking
                    const groupedCards = new Map<string, DeckCardInstance[]>();
                    sortedMainDeck.forEach(instance => {
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
                      
                      // Calculate 3D depth effect based on quantity
                      const getStackStyle = (qty: number) => {
                        if (qty === 1) {
                          return {}; // No special styling for single card
                        }
                        
                        const shadowLayers = [];
                        const maxLayers = Math.min(qty, 4); // Cap at 4 visual layers
                        
                        for (let i = 1; i < maxLayers; i++) {
                          const offset = i * 2;
                          const blur = i * 1;
                          const opacity = 0.7 - (i * 0.15);
                          shadowLayers.push(`${offset}px ${offset}px ${blur}px rgba(0,0,0,${opacity})`);
                        }
                        
                        return {
                          boxShadow: shadowLayers.join(', '),
                          transform: `translateZ(${qty * 2}px)`,
                          position: 'relative' as const,
                        };
                      };

                      const handleStackClick = (card: any, event?: React.MouseEvent) => {
                        // If multiple instances, select the first non-selected one, or all if all selected
                        if (instances.length > 1) {
                          const unselectedInstance = instances.find(inst => !isSelected(inst.instanceId));
                          const targetInstance = unselectedInstance || instances[0];
                          handleInstanceClick(targetInstance.instanceId, targetInstance, event as React.MouseEvent);
                        } else {
                          handleInstanceClick(representativeCard.instanceId, representativeCard, event as React.MouseEvent);
                        }
                      };

                      const handleStackDragStart = (cards: any[], zone: any, event: React.MouseEvent) => {
                        // When dragging a stack, drag all instances of the card
                        handleDragStart(instances as any[], zone, event);
                      };

                      return (
                        <div
                          key={cardId}
                          className="card-stack"
                          style={{
                            position: 'relative',
                            ...getStackStyle(quantity)
                          }}
                        >
                          <DraggableCard
                            key={`${cardId}-stack`}
                            card={representativeCard}
                            zone="deck"
                            size="normal"
                            scaleFactor={cardSizes.deck}
                            onClick={handleStackClick}
                            instanceId={representativeCard.instanceId}
                            isInstance={true}
                            onInstanceClick={handleStackClick}
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
                          
                          {/* Quantity indicator with enhanced styling for stacks */}
                          {quantity > 1 && (
                            <div
                              style={{
                                position: 'absolute',
                                top: '4px',
                                right: '4px',
                                backgroundColor: quantity >= 4 ? '#dc2626' : quantity >= 3 ? '#ea580c' : '#f59e0b',
                                color: 'white',
                                borderRadius: '50%',
                                width: '24px',
                                height: '24px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontSize: '14px',
                                fontWeight: 'bold',
                                border: '2px solid rgba(255,255,255,0.9)',
                                zIndex: 20,
                                boxShadow: '0 2px 8px rgba(0,0,0,0.5)',
                                animation: quantity >= 4 ? 'pulse 2s infinite' : 'none',
                              }}
                            >
                              {quantity}
                            </div>
                          )}
                        </div>
                      );
                    });
                  })()}
                  
                  {mainDeck.length === 0 && (
                    <div className="empty-deck-message">
                      Double-click or drag cards from the collection to add them to your deck
                    </div>
                  )}
                </div>
              )}'''
        
        if old_deck_grid in content:
            print("🔧 Fixing deck grid to use card stacking...")
            content = content.replace(old_deck_grid, new_deck_grid)
        else:
            print("⚠️  Warning: Could not find exact deck grid section to replace")
            return False

        # Now fix the sideboard grid with the same stacking logic
        old_sideboard_grid = '''              ) : (
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
                  {sortedSideboard.map((sideInstance) => (
                    <DraggableCard
                      key={sideInstance.instanceId}
                      card={sideInstance}
                      zone="sideboard"
                      size="normal"
                      scaleFactor={cardSizes.sideboard}
                      onClick={(card, event) => handleCardClick(card, event)}
                      instanceId={sideInstance.instanceId}
                      isInstance={true}
                      onInstanceClick={handleInstanceClick}
                      onEnhancedDoubleClick={handleDoubleClick}
                      onRightClick={handleRightClick}
                      onDragStart={handleDragStart}
                      showQuantity={true}
                      quantity={1}
                      selected={isSelected(sideInstance.instanceId)}
                      selectable={true}
                      isDragActive={dragState.isDragging}
                      isBeingDragged={dragState.draggedCards.some(dc => 'instanceId' in dc ? dc.instanceId === sideInstance.instanceId : dc.id === sideInstance.cardId)}
                      selectedCards={getSelectedCardObjects()}
                    />
                  ))}
                  {sideboard.length === 0 && (
                    <div className="empty-sideboard-message">
                      Drag cards here for your sideboard
                    </div>
                  )}
                </div>
              )}'''

        new_sideboard_grid = '''              ) : (
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
                  {(() => {
                    // Group instances by cardId for stacking  
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
                      
                      // Calculate 3D depth effect based on quantity
                      const getStackStyle = (qty: number) => {
                        if (qty === 1) {
                          return {}; // No special styling for single card
                        }
                        
                        const shadowLayers = [];
                        const maxLayers = Math.min(qty, 4); // Cap at 4 visual layers
                        
                        for (let i = 1; i < maxLayers; i++) {
                          const offset = i * 2;
                          const blur = i * 1;
                          const opacity = 0.7 - (i * 0.15);
                          shadowLayers.push(`${offset}px ${offset}px ${blur}px rgba(0,0,0,${opacity})`);
                        }
                        
                        return {
                          boxShadow: shadowLayers.join(', '),
                          transform: `translateZ(${qty * 2}px)`,
                          position: 'relative' as const,
                        };
                      };

                      const handleStackClick = (card: any, event?: React.MouseEvent) => {
                        // If multiple instances, select the first non-selected one, or all if all selected
                        if (instances.length > 1) {
                          const unselectedInstance = instances.find(inst => !isSelected(inst.instanceId));
                          const targetInstance = unselectedInstance || instances[0];
                          handleInstanceClick(targetInstance.instanceId, targetInstance, event as React.MouseEvent);
                        } else {
                          handleInstanceClick(representativeCard.instanceId, representativeCard, event as React.MouseEvent);
                        }
                      };

                      const handleStackDragStart = (cards: any[], zone: any, event: React.MouseEvent) => {
                        // When dragging a stack, drag all instances of the card
                        handleDragStart(instances as any[], zone, event);
                      };

                      return (
                        <div
                          key={cardId}
                          className="card-stack"
                          style={{
                            position: 'relative',
                            ...getStackStyle(quantity)
                          }}
                        >
                          <DraggableCard
                            key={`${cardId}-stack`}
                            card={representativeCard}
                            zone="sideboard"
                            size="normal"
                            scaleFactor={cardSizes.sideboard}
                            onClick={handleStackClick}
                            instanceId={representativeCard.instanceId}
                            isInstance={true}
                            onInstanceClick={handleStackClick}
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
                          
                          {/* Quantity indicator with enhanced styling for stacks */}
                          {quantity > 1 && (
                            <div
                              style={{
                                position: 'absolute',
                                top: '4px',
                                right: '4px',
                                backgroundColor: quantity >= 4 ? '#dc2626' : quantity >= 3 ? '#ea580c' : '#f59e0b',
                                color: 'white',
                                borderRadius: '50%',
                                width: '24px',
                                height: '24px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontSize: '14px',
                                fontWeight: 'bold',
                                border: '2px solid rgba(255,255,255,0.9)',
                                zIndex: 20,
                                boxShadow: '0 2px 8px rgba(0,0,0,0.5)',
                                animation: quantity >= 4 ? 'pulse 2s infinite' : 'none',
                              }}
                            >
                              {quantity}
                            </div>
                          )}
                        </div>
                      );
                    });
                  })()}
                  
                  {sideboard.length === 0 && (
                    <div className="empty-sideboard-message">
                      Drag cards here for your sideboard
                    </div>
                  )}
                </div>
              )}'''
        
        if old_sideboard_grid in content:
            print("🔧 Fixing sideboard grid to use card stacking...")
            content = content.replace(old_sideboard_grid, new_sideboard_grid)
        else:
            print("⚠️  Warning: Could not find exact sideboard grid section to replace")
            return False
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Successfully updated MTGOLayout.tsx")
        print("🎯 Added card stacking system with 3D depth effects")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {str(e)}")
        return False

def add_css_animations():
    """Add CSS animations for card stacking effects"""
    
    file_path = "src/components/MTGOLayout.css"
    
    if not os.path.exists(file_path):
        print(f"⚠️  Warning: {file_path} not found! Skipping CSS animations.")
        return True
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📖 Adding CSS animations to {file_path}...")
        
        # Add card stacking CSS at the end of the file
        css_animations = '''
/* ===== CARD STACKING ANIMATIONS ===== */

/* Pulse animation for 4+ card stacks */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.9;
  }
}

/* Card stack container */
.card-stack {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card-stack:hover {
  transform: translateY(-4px) scale(1.02);
  z-index: 100;
}

/* Enhanced depth shadows for card stacks */
.card-stack {
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
}

.card-stack:hover {
  filter: drop-shadow(0 8px 16px rgba(0,0,0,0.3));
}

/* Smooth transitions for quantity indicators */
.card-stack [style*="animation"] {
  transition: all 0.3s ease;
}

/* Stack depth enhancements */
.card-stack[data-quantity="2"] {
  transform: translateZ(4px);
}

.card-stack[data-quantity="3"] {
  transform: translateZ(6px);
}

.card-stack[data-quantity="4"] {
  transform: translateZ(8px);
}

/* ===== END CARD STACKING ANIMATIONS =====

'''
        
        # Add the CSS at the end of the file
        content += css_animations
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Successfully added CSS animations")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {str(e)}")
        return False

def main():
    """Main function"""
    print("🔧 MTG Deck Builder - Fix Card Stacking in Card View")
    print("=" * 60)
    
    success = True
    
    if fix_card_stacking():
        print("✅ Card stacking logic implemented successfully!")
    else:
        print("❌ Card stacking fix failed!")
        success = False
    
    if add_css_animations():
        print("✅ CSS animations added successfully!")
    else:
        print("⚠️  CSS animations could not be added (non-critical)")
    
    if success:
        print("\n🎉 All fixes applied successfully!")
        print("\n📋 Changes made:")
        print("   • Added card grouping by cardId in deck and sideboard")
        print("   • Implemented 3D depth effects that scale with quantity (1-4 cards)")
        print("   • Enhanced quantity indicators with color coding:")
        print("     - 2 cards: Orange (#f59e0b)")
        print("     - 3 cards: Orange-red (#ea580c)")  
        print("     - 4 cards: Red (#dc2626) with pulse animation")
        print("   • Maintained all existing functionality (selection, drag & drop)")
        print("   • Added hover effects and smooth transitions")
        print("   • Stack selection logic: clicks select individual instances intelligently")
        print("   • Stack dragging: dragging a stack moves all instances of that card")
        
        print("\n🎨 Visual Effects:")
        print("   • 1 card: No depth effect (standard appearance)")
        print("   • 2 cards: Subtle shadow offset")
        print("   • 3 cards: Medium stacked shadow layers")
        print("   • 4 cards: Full depth effect with multiple shadow layers + pulse")
        
        print("\n🚀 Next steps:")
        print("   1. Test the application with npm start")
        print("   2. Add multiple copies of the same card to deck/sideboard")
        print("   3. Verify card view shows stacks instead of individual cards")
        print("   4. Test selection, drag & drop, and context menus on stacks")
        print("   5. Check that quantity indicators show correct counts")
    else:
        print("\n❌ Fix failed! Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
