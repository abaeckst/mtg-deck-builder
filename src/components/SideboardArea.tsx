import React, { useState, useCallback, useRef, useEffect } from 'react';
import { ScryfallCard, DeckCard, DeckCardInstance, getCardId } from '../types/card';
import { SortCriteria, SortDirection } from '../hooks/useSorting';
import { DropZone as DropZoneType, DraggedCard } from '../hooks/useDragAndDrop';
import DraggableCard from './DraggableCard';
import DropZoneComponent from './DropZone';
import ListView from './ListView';
import PileView from './PileView';

interface SideboardAreaProps {
  sideboard: DeckCardInstance[];
  sideboardWidth: number;
  
  // Sorting (internal state, no UI controls)
  sortState: {
    criteria: SortCriteria;
    direction: SortDirection;
  };
  onSortChange: (criteria: SortCriteria, direction: SortDirection) => void;
  
  // View and sizing - INHERITED FROM UNIFIED STATE (no controls shown)
  viewMode: 'card' | 'pile' | 'list';
  onViewModeChange: (mode: 'card' | 'pile' | 'list') => void;
  cardSize: number;
  onCardSizeChange: (size: number) => void;
  
  // Card interactions
  onCardClick: (card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => void;
  onInstanceClick: (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => void;
  onEnhancedDoubleClick: (card: any, zone: DropZoneType, event: React.MouseEvent) => void;
  onCardRightClick: (card: any, zone: DropZoneType, event: React.MouseEvent) => void;
  onDragStart: (cards: DraggedCard[], zone: DropZoneType, event: React.MouseEvent) => void;
  
  // Drag and drop
  onDragEnter: (zone: DropZoneType, canDrop: boolean) => void;
  onDragLeave: () => void;
  canDropInZone: (zone: DropZoneType, cards: DraggedCard[]) => boolean;
  dragState: {
    isDragging: boolean;
    draggedCards: DraggedCard[];
  };
  
  // Selection
  isSelected: (cardId: string) => boolean;
  getSelectedCardObjects: () => any[];
  clearSelection: () => void;
  
  // Sideboard management
  onClearSideboard: () => void;
  getSideboardQuantity: (cardId: string) => number;
  onQuantityChange: (cardId: string, newQuantity: number) => void;
  
  // Resize
  onSideboardResize: (event: React.MouseEvent) => void;
  
  // Utility
  sortCards: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], criteria: SortCriteria, direction: 'asc' | 'desc') => (ScryfallCard | DeckCard | DeckCardInstance)[];
}

const SideboardArea: React.FC<SideboardAreaProps> = ({
  sideboard,
  sideboardWidth,
  sortState,
  onSortChange,
  viewMode, // Inherited from unified state
  onViewModeChange,
  cardSize, // Inherited from unified state
  onCardSizeChange,
  onCardClick,
  onInstanceClick,
  onEnhancedDoubleClick,
  onCardRightClick,
  onDragStart,
  onDragEnter,
  onDragLeave,
  canDropInZone,
  dragState,
  isSelected,
  getSelectedCardObjects,
  clearSelection,
  onClearSideboard,
  getSideboardQuantity,
  onQuantityChange,
  onSideboardResize,
  sortCards
}) => {
  // Get sorted cards (same sorting logic as deck area, but no UI controls)
  const sortedSideboard = viewMode === 'pile' ? sideboard : sortCards(sideboard as any, sortState.criteria, sortState.direction) as DeckCardInstance[];

  return (
    <DropZoneComponent
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
      
      <div className="sideboard-content">
        {/* View mode is inherited from unified state - uses same rendering logic */}
        {viewMode === 'pile' ? (
          <PileView
            cards={sideboard}
            zone="sideboard"
            scaleFactor={cardSize} // Inherited from unified state
            forcedSortCriteria={sortState.criteria === 'name' || sortState.criteria === 'type' ? 'mana' : sortState.criteria as any}
            onClick={(card, event) => onCardClick(card, event)}
            onInstanceClick={onInstanceClick}
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
                  onDragStart(cards, zone, event);
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
    </DropZoneComponent>
  );
};

export default SideboardArea;