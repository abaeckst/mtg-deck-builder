#!/usr/bin/env python3
"""
Fix card stacking to be clean and simple like collection area
This script removes shadows, fixes centering, and eliminates duplicate quantity indicators.
"""

import os
import sys

def fix_clean_card_stacking():
    """Fix deck/sideboard card stacking to mimic clean collection style"""
    
    file_path = "src/components/MTGOLayout.tsx"
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found!")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📖 Reading {file_path}...")
        
        # Find and replace the deck grid with clean stacking (no shadows, centered, single quantity indicator)
        old_deck_section = '''                <div 
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

                      const handleStackInstanceClick = (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => {
                        // For stacks, use the same logic but with proper signature
                        handleStackClick(instance, event);
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
                  })()}'''

        new_deck_section = '''                <div 
                  className="deck-grid"
                  style={{
                    display: 'grid',
                    gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSizes.deck)}px, max-content))`,
                    gap: `${Math.round(4 * cardSizes.deck)}px`,
                    alignContent: 'start',
                    minHeight: '150px',
                    paddingBottom: '40px'
                  }}
                >
                  {(() => {
                    // Group instances by cardId for clean stacking (collection style)
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

                      const handleStackInstanceClick = (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => {
                        // For stacks, use the same logic but with proper signature
                        handleStackClick(instance, event);
                      };

                      const handleStackDragStart = (cards: any[], zone: any, event: React.MouseEvent) => {
                        // When dragging a stack, drag all instances of the card
                        handleDragStart(instances as any[], zone, event);
                      };

                      return (
                        <DraggableCard
                          key={cardId}
                          card={representativeCard}
                          zone="deck"
                          size="normal"
                          scaleFactor={cardSizes.deck}
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
                  })()}'''

        if old_deck_section in content:
            print("🔧 Fixing deck grid to use clean collection-style stacking...")
            content = content.replace(old_deck_section, new_deck_section)
        else:
            print("⚠️  Warning: Could not find exact deck section to replace")
            return False

        # Now fix the sideboard grid with the same clean approach
        old_sideboard_section = '''                <div 
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

                      const handleStackInstanceClick = (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => {
                        // For stacks, use the same logic but with proper signature
                        handleStackClick(instance, event);
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
                  })()}'''

        new_sideboard_section = '''                <div 
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
                    // Group instances by cardId for clean stacking (collection style)
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
                        // If multiple instances, select the first non-selected one, or all if all selected
                        if (instances.length > 1) {
                          const unselectedInstance = instances.find(inst => !isSelected(inst.instanceId));
                          const targetInstance = unselectedInstance || instances[0];
                          handleInstanceClick(targetInstance.instanceId, targetInstance, event as React.MouseEvent);
                        } else {
                          handleInstanceClick(representativeCard.instanceId, representativeCard, event as React.MouseEvent);
                        }
                      };

                      const handleStackInstanceClick = (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => {
                        // For stacks, use the same logic but with proper signature
                        handleStackClick(instance, event);
                      };

                      const handleStackDragStart = (cards: any[], zone: any, event: React.MouseEvent) => {
                        // When dragging a stack, drag all instances of the card
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
                  })()}'''

        if old_sideboard_section in content:
            print("🔧 Fixing sideboard grid to use clean collection-style stacking...")
            content = content.replace(old_sideboard_section, new_sideboard_section)
        else:
            print("⚠️  Warning: Could not find exact sideboard section to replace")
            return False

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Successfully updated MTGOLayout.tsx with clean card stacking")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {str(e)}")
        return False

def remove_css_animations():
    """Remove the 3D CSS animations we added earlier"""
    
    file_path = "src/components/MTGOLayout.css"
    
    if not os.path.exists(file_path):
        print(f"⚠️  {file_path} not found, skipping CSS cleanup")
        return True
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📖 Removing 3D CSS animations from {file_path}...")
        
        # Remove the card stacking animations section we added
        css_to_remove = '''
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

/* ===== END CARD STACKING ANIMATIONS ===== */'''

        if css_to_remove in content:
            content = content.replace(css_to_remove, '')
            print("🔧 Removed 3D CSS animations")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Successfully cleaned up CSS animations")
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning CSS: {str(e)}")
        return False

def main():
    """Main function"""
    print("🔧 MTG Deck Builder - Fix Clean Card Stacking")
    print("=" * 55)
    
    success = True
    
    if fix_clean_card_stacking():
        print("✅ Clean card stacking implemented!")
    else:
        print("❌ Card stacking fix failed!")
        success = False
    
    if remove_css_animations():
        print("✅ CSS animations cleaned up!")
    else:
        print("⚠️  CSS cleanup had issues (non-critical)")
    
    if success:
        print("\n🎉 All fixes applied successfully!")
        print("\n📋 Changes made:")
        print("   • Removed all 3D shadows and depth effects")
        print("   • Fixed card centering: 1fr → max-content (like collection)")
        print("   • Eliminated duplicate quantity indicators")
        print("   • Simplified card stacking - clean collection style")
        print("   • Removed card-stack wrapper div")
        print("   • Removed custom quantity overlay (MagicCard handles it)")
        
        print("\n🎯 Result:")
        print("   • Deck cards look exactly like collection cards")
        print("   • One visual card per unique card (no individual instances)")
        print("   • Single quantity indicator from MagicCard")
        print("   • Cards properly centered in grid columns")
        print("   • Clean, simple appearance with no shadows")
        print("   • All functionality preserved (selection, drag & drop)")
        
        print("\n🚀 Next steps:")
        print("   1. Test the application with npm start")
        print("   2. Add multiple copies of cards to deck/sideboard")
        print("   3. Verify clean appearance matching collection style")
        print("   4. Test that selection and drag & drop still work")
    else:
        print("\n❌ Some fixes failed! Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
