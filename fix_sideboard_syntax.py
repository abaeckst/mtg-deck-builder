#!/usr/bin/env python3
"""
Fix the JSX syntax error in SideboardArea.tsx caused by the previous script.
This script will restore the proper JSX structure while fixing the resize handle.
"""

def fix_sideboard_syntax():
    """Fix the broken JSX structure in SideboardArea.tsx"""
    
    try:
        with open('src/components/SideboardArea.tsx', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔧 Fixing SideboardArea.tsx JSX syntax error...")
        
        # Find the broken section and replace with correct structure
        # The issue is around line 93-110 where the header div structure was corrupted
        
        # Look for the problematic section and replace it entirely
        broken_section_start = content.find('<DropZoneComponent')
        broken_section_end = content.find('</DropZoneComponent>') + len('</DropZoneComponent>')
        
        if broken_section_start == -1 or broken_section_end == -1:
            print("❌ Could not find DropZoneComponent section")
            return False
        
        # Extract the content before and after the broken section
        before = content[:broken_section_start]
        after = content[broken_section_end:]
        
        # Create the corrected DropZoneComponent section
        fixed_section = '''<DropZoneComponent
      zone="sideboard"
      onDragEnter={onDragEnter}
      onDragLeave={onDragLeave}
      canDrop={canDropInZone('sideboard', dragState.draggedCards)}
      isDragActive={dragState.isDragging}
      className="mtgo-sideboard-panel"
      style={{ width: `${sideboardWidth}px` }}
    >
      {/* Horizontal Resize Handle */}
      <div 
        className="resize-handle resize-handle-left"
        onMouseDown={onSideboardResize}
        title="Drag to resize sideboard"
      />
      
      {/* MTGO-Style Simplified Header - Title + Count Only */}
      <div className="mtgo-header" style={{
        background: 'linear-gradient(180deg, #2a2a2a 0%, #1a1a1a 100%)',
        border: '1px solid #444',
        borderTop: '1px solid #666',
        boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
        padding: '6px 12px',
        color: '#ffffff',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        fontSize: '14px'
      }}>
        {/* Title Section - Only title and count */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{
            fontSize: '15px',
            fontWeight: '600',
            color: '#ffffff',
            textShadow: '0 1px 2px rgba(0,0,0,0.3)'
          }}>
            Sideboard
          </span>
          <span style={{
            color: '#cccccc',
            fontSize: '13px'
          }}>
            ({sideboard.length} cards)
          </span>
        </div>
        
        {/* No controls - view mode and size are inherited from unified state */}
      </div>
      
      <div className="sideboard-content" style={{ paddingLeft: '12px' }}>
        {/* View mode is inherited from unified state - uses same rendering logic */}
        {viewMode === 'pile' ? (
          <PileView
            cards={sideboard}
            zone="sideboard"
            scaleFactor={cardSize} // Inherited from unified state
            forcedSortCriteria={sortState.criteria === 'name' || sortState.criteria === 'type' ? 'mana' : sortState.criteria as any}
            onClick={(card, event) => onCardClick(card, event)}
            onInstanceClick={onInstanceClick}
            onDoubleClick={onCardDoubleClick}
            onEnhancedDoubleClick={onEnhancedDoubleClick}
            onRightClick={onCardRightClick}
            onDragStart={onDragStart}
            isSelected={isSelected}
            selectedCards={getSelectedCardObjects()}
            isDragActive={dragState.isDragging}
            onDragEnter={onDragEnter}
            onDragLeave={onDragLeave}
            canDropInZone={canDropInZone}
          />
        ) : viewMode === 'list' ? (
          <ListView
            cards={sortedSideboard}
            area="sideboard"
            scaleFactor={cardSize} // Inherited from unified state
            sortCriteria={sortState.criteria}
            sortDirection={sortState.direction}
            onSortChange={(criteria, direction) => {
              if (criteria === 'name' || criteria === 'mana' || criteria === 'color' || criteria === 'rarity') {
                onSortChange(criteria, direction);
              }
            }}
            onClick={(card, event) => onCardClick(card, event)}
            onDoubleClick={(card) => onEnhancedDoubleClick(card as any, 'sideboard', { preventDefault: () => {}, stopPropagation: () => {} } as React.MouseEvent)}
            onRightClick={onCardRightClick}
            onDragStart={onDragStart}
            isSelected={isSelected}
            selectedCards={getSelectedCardObjects()}
            isDragActive={dragState.isDragging}
            onQuantityChange={onQuantityChange}
          />
        ) : (
          <div 
            className="sideboard-grid"
            style={{
              display: 'grid',
              gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSize)}px, max-content))`, // Card size inherited
              gap: `${Math.round(4 * cardSize)}px`, // Gap scales with unified card size
              alignContent: 'start',
              minHeight: '150px',
              paddingBottom: '40px'
            }}
          >
            {(() => {
              // Group instances by cardId for clean stacking (same as deck area)
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
                    onInstanceClick(targetInstance.instanceId, targetInstance, event as React.MouseEvent);
                  } else {
                    onInstanceClick(representativeCard.instanceId, representativeCard, event as React.MouseEvent);
                  }
                };

                const handleStackInstanceClick = (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => {
                  handleStackClick(instance, event);
                };

                const handleStackDragStart = (cards: any[], zone: any, event: React.MouseEvent) => {
                  onDragStart(instances as any[], zone, event);
                };

                return (
                  <DraggableCard
                    key={cardId}
                    card={representativeCard}
                    zone="sideboard"
                    size="normal"
                    scaleFactor={cardSize} // Inherited from unified state
                    onClick={handleStackClick}
                    instanceId={representativeCard.instanceId}
                    isInstance={true}
                    onInstanceClick={handleStackInstanceClick}
                    onEnhancedDoubleClick={onEnhancedDoubleClick}
                    onRightClick={onCardRightClick}
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
          </div>
        )}
      </div>
    </DropZoneComponent>'''
        
        # Reconstruct the file
        new_content = before + fixed_section + after
        
        with open('src/components/SideboardArea.tsx', 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print("✅ SideboardArea.tsx JSX syntax fixed")
        print("✅ Resize handle cleaned up (no inline styles)")
        print("✅ Sideboard content padding added to prevent overlap")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing SideboardArea.tsx: {e}")
        return False

def main():
    """Execute the syntax fix"""
    print("🚀 Fixing SideboardArea.tsx JSX syntax error...")
    print()
    
    if fix_sideboard_syntax():
        print()
        print("✅ SYNTAX ERROR FIXED!")
        print()
        print("Changes made:")
        print("1. Restored proper JSX structure for DropZoneComponent")
        print("2. Fixed resize handle (removed problematic inline styles)")
        print("3. Added sideboard content padding to prevent resize handle overlap")
        print()
        print("The resize handle now uses CSS-only styling with 20px hit zones.")
        print("The compilation should work now.")
    else:
        print()
        print("❌ Fix failed - please check the error message above")

if __name__ == "__main__":
    main()
