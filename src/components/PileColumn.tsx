// ===== FILE: src/components/PileColumn.tsx - FINAL VERSION =====
import React, { useCallback } from 'react';
import { ScryfallCard, DeckCard } from '../types/card';
import { DropZone } from '../hooks/useDragAndDrop';
import DraggableCard from './DraggableCard';

interface PileColumnProps {
  columnId: string;
  title: string;
  cards: (ScryfallCard | DeckCard)[];
  zone: 'deck' | 'sideboard';
  scaleFactor: number;
  isEmpty?: boolean;
  // Card interaction handlers
  onClick?: (card: ScryfallCard | DeckCard, event?: React.MouseEvent) => void;
  onDoubleClick?: (card: ScryfallCard | DeckCard) => void;
  onEnhancedDoubleClick?: (card: ScryfallCard | DeckCard, zone: DropZone, event: React.MouseEvent) => void;
  onRightClick?: (card: ScryfallCard | DeckCard, zone: DropZone, event: React.MouseEvent) => void;
  onDragStart?: (cards: (ScryfallCard | DeckCard)[], zone: DropZone, event: React.MouseEvent) => void;
  // Selection and drag state
  isSelected?: (cardId: string) => boolean;
  selectedCards?: (ScryfallCard | DeckCard)[];
  isDragActive?: boolean;
  // Drop zone handlers
  onDragEnter?: (zone: DropZone, canDrop: boolean) => void;
  onDragLeave?: () => void;
  canDropInZone?: (zone: DropZone, cards: (ScryfallCard | DeckCard)[]) => boolean;
  // Manual movement
  onManualMove?: (cardId: string, fromColumn: string, toColumn: string) => void;
}

const PileColumn: React.FC<PileColumnProps> = ({
  columnId,
  title,
  cards,
  zone,
  scaleFactor,
  isEmpty = false,
  onClick,
  onDoubleClick,
  onEnhancedDoubleClick,
  onRightClick,
  onDragStart,
  isSelected = () => false,
  selectedCards = [],
  isDragActive = false,
  onDragEnter,
  onDragLeave,
  canDropInZone,
  onManualMove,
}) => {

  // Handle drop events for manual card movement between pile columns
  const handleDrop = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    // This will integrate with the existing drag system in a future enhancement
    // For now, it's a placeholder for the manual move functionality
    console.log(`Drop event in column ${columnId}`);
  }, [columnId]);

  const handleDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
  }, []);

  // MTGO-style card stacking - ALL cards stack together with proper overlap
  const renderCards = useCallback(() => {
    try {
      const renderedCards: React.ReactElement[] = [];
      let cardIndex = 0; // Track position across all cards for proper stacking
      
      cards.forEach(card => {
        // Validate card has required properties
        if (!card || !card.id) {
          console.warn('Invalid card object:', card);
          return;
        }

        // Get quantity for this card
        let cardQuantity = 1;
        if (typeof card === 'object' && card !== null) {
          if ('quantity' in card && typeof card.quantity === 'number' && card.quantity > 0) {
            cardQuantity = card.quantity;
          }
        }

        // Create individual draggable cards for each copy (MTGO-style stacking)
        for (let i = 0; i < cardQuantity; i++) {
          // MTGO-style tight stacking - show ~15% of each card (name area visible)
          // Typical card is ~180px tall, we want ~27px showing = 85% overlap
          const cardHeight = Math.round(180 * scaleFactor); // Estimated card height at current scale
          const visiblePortion = Math.round(cardHeight * 0.14); // Show 14% of card (name area)
          const stackOffset = -(cardHeight - visiblePortion); // Negative offset to stack tightly
          
          renderedCards.push(
            <div
              key={`${card.id}-${i}`}
              className="pile-card-stack-item"
              style={{
                marginTop: cardIndex > 0 ? `${stackOffset}px` : '0px', // Stack ALL cards, not just same card
                zIndex: cardIndex, // Last card has highest z-index (most visible), first card lowest
                position: 'relative',
              }}
            >
              <DraggableCard
                card={card}
                zone={zone}
                size="normal"
                scaleFactor={scaleFactor}
                onClick={onClick}
                onDoubleClick={onDoubleClick}
                onEnhancedDoubleClick={onEnhancedDoubleClick}
                onRightClick={onRightClick}
                onDragStart={onDragStart}
                showQuantity={false} // Don't show quantity on individual cards
                quantity={1} // Each rendered card represents 1 copy
                selected={isSelected ? isSelected(card.id) : false}
                selectable={true}
                isDragActive={isDragActive}
                isBeingDragged={isDragActive && selectedCards.some(sc => sc.id === card.id)}
                selectedCards={selectedCards}
              />
            </div>
          );
          
          cardIndex++; // Increment for next card in stack
        }
      });
      
      return renderedCards;
    } catch (error) {
      console.error('Error rendering cards in pile column:', error);
      return [<div key="error" className="error-message">Error rendering cards</div>];
    }
  }, [cards, zone, scaleFactor, onClick, onDoubleClick, onEnhancedDoubleClick, onRightClick, onDragStart, isSelected, selectedCards, isDragActive]);

  // Calculate proper column width - ensure cards fit within column bounds
  // Magic cards are ~115px wide - balanced sizing to contain cards while showing gaps
  const dynamicWidth = isEmpty ? 
    Math.max(80, Math.round(90 * scaleFactor)) : 
    Math.max(110, Math.round(125 * scaleFactor)); // Balanced width - contains cards but makes gap visible

  return (
    <div 
      className={`pile-column ${isEmpty ? 'empty-column' : ''}`}
      style={{ 
        width: `${dynamicWidth}px`,
        maxWidth: `${Math.max(dynamicWidth, 220)}px`
      }}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
    >
      {/* Simple centered number - no header box */}
      {!isEmpty && title && (
        <div className="pile-column-number">
          {title}
        </div>
      )}
      
      {/* Column Content */}
      <div className="pile-column-content">
        {renderCards()}
        
        {/* Empty state for non-empty columns */}
        {!isEmpty && cards.length === 0 && (
          <div className="empty-column-placeholder">
            Drop cards here
          </div>
        )}
      </div>
    </div>
  );
};

export default PileColumn;