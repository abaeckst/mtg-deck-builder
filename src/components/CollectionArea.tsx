import React, { useState, useCallback, useRef, useEffect } from 'react';
import { ScryfallCard, DeckCard, DeckCardInstance, getCardId } from '../types/card';
import { SortCriteria, SortDirection } from '../hooks/useSorting';
import { DropZone as DropZoneType, DraggedCard } from '../hooks/useDragAndDrop';
import DraggableCard from './DraggableCard';
import DropZoneComponent from './DropZone';
import ListView from './ListView';

interface CollectionAreaProps {
  cards: ScryfallCard[];
  loading: boolean;
  error: string | null;
  
  // Pagination
  pagination: {
    hasMore: boolean;
    isLoadingMore: boolean;
    loadedCards: number;
    totalCards: number;
  };
  loadMoreResultsAction: () => Promise<void>;
  
  // Sorting
  sortState: {
    criteria: SortCriteria;
    direction: SortDirection;
  };
  onSortChange: (criteria: SortCriteria, direction: SortDirection) => Promise<void>;
  
  // View and sizing
  viewMode: 'grid' | 'list';
  onViewModeChange: (mode: 'grid' | 'list') => void;
  cardSize: number;
  onCardSizeChange: (size: number) => void;
  
  // Card interactions
  onCardClick: (card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => void;
  onEnhancedDoubleClick: (card: ScryfallCard | DeckCard | DeckCardInstance, zone: DropZoneType, event: React.MouseEvent) => void;
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
  
  // Utility
  getTotalCopies: (cardId: string) => number;
  sortCards: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], criteria: SortCriteria, direction: 'asc' | 'desc') => (ScryfallCard | DeckCard | DeckCardInstance)[];
}

const CollectionArea: React.FC<CollectionAreaProps> = ({
  cards,
  loading,
  error,
  pagination,
  loadMoreResultsAction,
  sortState,
  onSortChange,
  viewMode,
  onViewModeChange,
  cardSize,
  onCardSizeChange,
  onCardClick,
  onCardRightClick,
  onEnhancedDoubleClick,
  onDragStart,
  onDragEnter,
  onDragLeave,
  canDropInZone,
  dragState,
  isSelected,
  getSelectedCardObjects,
  clearSelection,
  getTotalCopies,
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
  const handleSortButtonClick = useCallback(async (criteria: SortCriteria) => {
    if (sortState.criteria === criteria) {
      const newDirection = sortState.direction === 'asc' ? 'desc' : 'asc';
      await onSortChange(criteria, newDirection);
    } else {
      await onSortChange(criteria, 'asc');
    }
    setShowSortMenu(false);
  }, [sortState.criteria, sortState.direction, onSortChange]);

  // Get sorted cards
  const sortedCards = sortCards([...cards], sortState.criteria, sortState.direction);

  return (
    <DropZoneComponent
      zone="collection"
      onDragEnter={onDragEnter}
      onDragLeave={onDragLeave}
      canDrop={canDropInZone('collection', dragState.draggedCards)}
      isDragActive={dragState.isDragging}
      className="mtgo-collection-area"
    >
      {/* MTGO-Style Header */}
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
        gap: '16px',
        fontSize: '14px'
      }}>
        <h3 style={{
          fontSize: '15px',
          fontWeight: '600',
          color: '#ffffff',
          textShadow: '0 1px 2px rgba(0,0,0,0.3)',
          margin: 0
        }}>
          Collection ({cards.length.toLocaleString()} {pagination.totalCards > pagination.loadedCards && (
            <span className="pagination-info">of {pagination.totalCards.toLocaleString()}</span>
          )} cards)
        </h3>

        <div className="view-controls" style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          fontSize: '13px'
        }}>
          <span style={{color: '#cccccc'}}>Size: </span>
          <input
            type="range"
            min="1.3"
            max="2.5"
            step="0.1"
            value={cardSize}
            onChange={(e) => onCardSizeChange(parseFloat(e.target.value))}
            className="size-slider"
            style={{
              width: '70px',
              height: '4px',
              background: '#555555',
              outline: 'none',
              borderRadius: '2px'
            }}
            title={`Card size: ${Math.round(cardSize * 100)}%`}
          />
          
          <div className="sort-button-container" ref={sortRef}>
            <button 
              className="sort-toggle-btn"
              style={{
                padding: '3px 6px',
                background: '#333333',
                border: '1px solid #555555',
                color: '#ffffff',
                fontSize: '12px',
                cursor: 'pointer',
                borderRadius: '2px'
              }}
              onClick={() => setShowSortMenu(!showSortMenu)}
              title="Sort options"
            >
              Sort
            </button>
            {showSortMenu && (
              <div className="sort-menu" style={{
                position: 'absolute',
                top: '100%',
                left: 0,
                background: '#2a2a2a',
                border: '1px solid #555555',
                borderRadius: '2px',
                boxShadow: '0 2px 8px rgba(0,0,0,0.5)',
                zIndex: 1000,
                minWidth: '120px'
              }}>
                <button 
                  className={sortState.criteria === 'name' ? 'active' : ''}
                  onClick={() => handleSortButtonClick('name')}
                  style={{
                    display: 'block',
                    width: '100%',
                    padding: '6px 10px',
                    background: sortState.criteria === 'name' ? '#4a4a4a' : 'transparent',
                    border: 'none',
                    color: '#ffffff',
                    fontSize: '12px',
                    textAlign: 'left',
                    cursor: 'pointer'
                  }}
                >
                  Name {sortState.criteria === 'name' ? (sortState.direction === 'asc' ? '↑' : '↓') : ''}
                </button>
                <button 
                  className={sortState.criteria === 'mana' ? 'active' : ''}
                  onClick={() => handleSortButtonClick('mana')}
                  style={{
                    display: 'block',
                    width: '100%',
                    padding: '6px 10px',
                    background: sortState.criteria === 'mana' ? '#4a4a4a' : 'transparent',
                    border: 'none',
                    color: '#ffffff',
                    fontSize: '12px',
                    textAlign: 'left',
                    cursor: 'pointer'
                  }}
                >
                  Mana Value {sortState.criteria === 'mana' ? (sortState.direction === 'asc' ? '↑' : '↓') : ''}
                </button>
                <button 
                  className={sortState.criteria === 'color' ? 'active' : ''}
                  onClick={() => handleSortButtonClick('color')}
                  style={{
                    display: 'block',
                    width: '100%',
                    padding: '6px 10px',
                    background: sortState.criteria === 'color' ? '#4a4a4a' : 'transparent',
                    border: 'none',
                    color: '#ffffff',
                    fontSize: '12px',
                    textAlign: 'left',
                    cursor: 'pointer'
                  }}
                >
                  Color {sortState.criteria === 'color' ? (sortState.direction === 'asc' ? '↑' : '↓') : ''}
                </button>
                <button 
                  className={sortState.criteria === 'rarity' ? 'active' : ''}
                  onClick={() => handleSortButtonClick('rarity')}
                  style={{
                    display: 'block',
                    width: '100%',
                    padding: '6px 10px',
                    background: sortState.criteria === 'rarity' ? '#4a4a4a' : 'transparent',
                    border: 'none',
                    color: '#ffffff',
                    fontSize: '12px',
                    textAlign: 'left',
                    cursor: 'pointer'
                  }}
                >
                  Rarity {sortState.criteria === 'rarity' ? (sortState.direction === 'asc' ? '↑' : '↓') : ''}
                </button>
              </div>
            )}
          </div>
          
          <span style={{color: '#cccccc'}}>View: </span>
          <button 
            className={viewMode === 'grid' ? 'active' : ''}
            style={{
              padding: '3px 6px',
              background: viewMode === 'grid' ? '#4a4a4a' : '#333333',
              border: '1px solid #555555',
              color: '#ffffff',
              fontSize: '12px',
              cursor: 'pointer',
              borderRadius: '2px'
            }}
            onClick={() => { clearSelection(); onViewModeChange('grid'); }}
          >
            Card
          </button>
          <button 
            className={viewMode === 'list' ? 'active' : ''}
            style={{
              padding: '3px 6px',
              background: viewMode === 'list' ? '#4a4a4a' : '#333333',
              border: '1px solid #555555',
              color: '#ffffff',
              fontSize: '12px',
              cursor: 'pointer',
              borderRadius: '2px'
            }}
            onClick={() => { clearSelection(); onViewModeChange('list'); }}
          >
            List
          </button>
        </div>
      </div>
      
      {/* Collection Content - Conditional Rendering */}
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
        viewMode === 'list' ? (
          <>
            <ListView
              cards={sortedCards}
              area="collection"
              scaleFactor={cardSize}
              sortCriteria={sortState.criteria}
              sortDirection={sortState.direction}
              onSortChange={onSortChange}
              onClick={onCardClick}
                onRightClick={onCardRightClick}
              onDragStart={onDragStart}
              isSelected={isSelected}
              selectedCards={getSelectedCardObjects()}
              isDragActive={dragState.isDragging}
            />
            
            {/* Load More Results integrated into List View */}
            {!loading && !error && pagination.hasMore && (
              <div className="load-more-section-integrated">
                {pagination.isLoadingMore ? (
                  <div className="loading-progress">
                    <div className="progress-bar">
                      <div 
                        className="progress-fill" 
                        style={{
                          width: `${(pagination.loadedCards / pagination.totalCards) * 100}%`
                        }}
                      />
                    </div>
                    <span className="progress-text">
                      Loading... ({pagination.loadedCards.toLocaleString()}/{pagination.totalCards.toLocaleString()} cards)
                    </span>
                  </div>
                ) : (
                  <button 
                    className="load-more-results-btn"
                    style={{
                      padding: '8px 12px',
                      background: '#333333',
                      border: '1px solid #555555',
                      color: '#ffffff',
                      fontSize: '12px',
                      cursor: 'pointer',
                      borderRadius: '2px'
                    }}
                    onClick={loadMoreResultsAction}
                    disabled={loading}
                    title={`Load 175 more cards (${pagination.totalCards - pagination.loadedCards} remaining)`}
                  >
                    Load More Results ({(pagination.totalCards - pagination.loadedCards).toLocaleString()} more cards)
                  </button>
                )}
              </div>
            )}
          </>
        ) : (
          <div 
            className="collection-grid"
            style={{
              display: 'grid',
              gridTemplateColumns: `repeat(auto-fill, minmax(${Math.round(130 * cardSize)}px, max-content))`,
              gap: `${Math.round(4 * cardSize)}px`,
              alignContent: 'start',
              padding: '8px'
            }}
          >
            {sortedCards.map((card) => (
              <DraggableCard
                key={getCardId(card)}
                card={card}
                zone="collection"
                size="normal"
                scaleFactor={cardSize}
                onClick={(card, event) => onCardClick(card, event)}
                onEnhancedDoubleClick={onEnhancedDoubleClick}                onRightClick={onCardRightClick}
                onDragStart={onDragStart}
                showQuantity={false}
                // No quantity display for collection - each card is individual
                selected={isSelected(getCardId(card))}
                selectable={true}
                isDragActive={dragState.isDragging}
                isBeingDragged={dragState.draggedCards.some(dc => getCardId(dc) === getCardId(card))}
                selectedCards={getSelectedCardObjects()}
              />
            ))}
            
            {/* Load More Results integrated into Card Grid */}
            {!loading && !error && pagination.hasMore && (
              <div className="load-more-section-integrated" style={{
                gridColumn: '1 / -1',
                display: 'flex',
                justifyContent: 'center',
                padding: '20px',
                marginTop: '10px'
              }}>
                {pagination.isLoadingMore ? (
                  <div className="loading-progress">
                    <div className="progress-bar">
                      <div 
                        className="progress-fill" 
                        style={{
                          width: `${(pagination.loadedCards / pagination.totalCards) * 100}%`
                        }}
                      />
                    </div>
                    <span className="progress-text">
                      Loading... ({pagination.loadedCards.toLocaleString()}/{pagination.totalCards.toLocaleString()} cards)
                    </span>
                  </div>
                ) : (
                  <button 
                    className="load-more-results-btn"
                    style={{
                      padding: '8px 12px',
                      background: '#333333',
                      border: '1px solid #555555',
                      color: '#ffffff',
                      fontSize: '12px',
                      cursor: 'pointer',
                      borderRadius: '2px'
                    }}
                    onClick={loadMoreResultsAction}
                    disabled={loading}
                    title={`Load 175 more cards (${pagination.totalCards - pagination.loadedCards} remaining)`}
                  >
                    Load More Results ({(pagination.totalCards - pagination.loadedCards).toLocaleString()} more cards)
                  </button>
                )}
              </div>
            )}
          </div>
        )
      )}
      
      {/* Resize Handle */}
      <div 
        className="resize-handle resize-handle-bottom"
        style={{
          position: 'absolute',
          left: 0,
          bottom: -3,
          width: '100%',
          height: 6,
          cursor: 'ns-resize',
          background: 'linear-gradient(0deg, transparent 0%, #555555 50%, transparent 100%)',
          zIndex: 1001,
          opacity: 0.7,
          transition: 'opacity 0.2s ease'
        }}
        onMouseEnter={(e) => e.currentTarget.style.opacity = '1'}
        onMouseLeave={(e) => e.currentTarget.style.opacity = '0.7'}
      />
    </DropZoneComponent>
  );
};

export default CollectionArea;