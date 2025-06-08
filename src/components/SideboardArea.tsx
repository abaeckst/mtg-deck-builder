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
  
  // Sorting
  sortState: {
    criteria: SortCriteria;
    direction: SortDirection;
  };
  onSortChange: (criteria: SortCriteria, direction: SortDirection) => void;
  
  // View and sizing
  viewMode: 'card' | 'pile' | 'list';
  onViewModeChange: (mode: 'card' | 'pile' | 'list') => void;
  cardSize: number;
  onCardSizeChange: (size: number) => void;
  
  // Card interactions
  onCardClick: (card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => void;
  onInstanceClick: (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => void;
  onCardDoubleClick: (card: ScryfallCard | DeckCard | DeckCardInstance) => void;
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
  viewMode,
  onViewModeChange,
  cardSize,
  onCardSizeChange,
  onCardClick,
  onInstanceClick,
  onCardDoubleClick,
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
  // Sort menu state
  const [showSortMenu, setShowSortMenu] = useState(false);
  const sortRef = useRef<HTMLDivElement>(null);

  // Click-outside effect for sort menu
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (sortRef.current && !sortRef.current.contains(event.target as Node)) {
        setShowSortMenu(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // Sort button handlers
  const handleSortButtonClick = useCallback((criteria: SortCriteria) => {
    if (viewMode === 'card' && sortState.criteria === criteria) {
      onSortChange(criteria, sortState.direction === 'asc' ? 'desc' : 'asc');
    } else {
      onSortChange(criteria, 'asc');
    }
    setShowSortMenu(false);
  }, [viewMode, sortState.criteria, sortState.direction, onSortChange]);

  // Get sorted cards
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
      
      <div className="panel-header">
        <h3>Sideboard ({sideboard.length} cards)</h3>
        <div className="sideboard-controls">
          <span>Size: </span>
          <input
            type="range"
            min="1.3"
            max="2.5"
            step="0.1"
            value={cardSize}
            onChange={(e) => onCardSizeChange(parseFloat(e.target.value))}
            className="size-slider"
            title={`Card size: ${Math.round(cardSize * 100)}%`}
          />
          
          <div className="sort-button-container" ref={sortRef}>
            <button 
              className="sort-toggle-btn"
              onClick={() => setShowSortMenu(!showSortMenu)}
              title="Sort options"
            >
              Sort
            </button>
            {showSortMenu && (
              <div className="sort-menu">
                <button 
                  className={sortState.criteria === 'mana' ? 'active' : ''}
                  onClick={() => handleSortButtonClick('mana')}
                >
                  Mana Value {sortState.criteria === 'mana' && viewMode === 'card' ? (sortState.direction === 'asc' ? '↑' : '↓') : ''}
                </button>
                <button 
                  className={sortState.criteria === 'color' ? 'active' : ''}
                  onClick={() => handleSortButtonClick('color')}
                >
                  Color {sortState.criteria === 'color' && viewMode === 'card' ? (sortState.direction === 'asc' ? '↑' : '↓') : ''}
                </button>
                <button 
                  className={sortState.criteria === 'rarity' ? 'active' : ''}
                  onClick={() => handleSortButtonClick('rarity')}
                >
                  Rarity {sortState.criteria === 'rarity' && viewMode === 'card' ? (sortState.direction === 'asc' ? '↑' : '↓') : ''}
                </button>
              </div>
            )}
          </div>
          
          <span>View: </span>
          <button 
            className={viewMode === 'card' ? 'active' : ''}
            onClick={() => { clearSelection(); onViewModeChange('card'); }}
          >
            Card
          </button>
          <button 
            className={viewMode === 'pile' ? 'active' : ''}
            onClick={() => { clearSelection(); onViewModeChange('pile'); }}
          >
            Pile
          </button>
          <button 
            className={viewMode === 'list' ? 'active' : ''}
            onClick={() => { clearSelection(); onViewModeChange('list'); }}
          >
            List
          </button>
          
          <button onClick={onClearSideboard} title="Clear all cards from sideboard">
            Clear
          </button>
        </div>
      </div>
      
      <div className="sideboard-content">
        {viewMode === 'pile' ? (
          <PileView
            cards={sideboard}
            zone="sideboard"
            scaleFactor={cardSize}
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
            scaleFactor={cardSize}
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
              gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSize)}px, max-content))`,
              gap: `${Math.round(4 * cardSize)}px`,
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
                    scaleFactor={cardSize}
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