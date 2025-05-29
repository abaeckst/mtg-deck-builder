// src/components/DraggableCard.tsx - Updated with context menu support
import React, { useCallback } from 'react';
import MagicCard from './MagicCard';
import { ScryfallCard, DeckCard } from '../types/card';
import { DropZone } from '../hooks/useDragAndDrop';

interface DraggableCardProps {
  card: ScryfallCard | DeckCard;
  zone: DropZone;
  size?: 'small' | 'normal' | 'large';
  onClick?: (card: ScryfallCard | DeckCard, event?: React.MouseEvent) => void;
  onDoubleClick?: (card: ScryfallCard | DeckCard) => void;
  onRightClick?: (card: ScryfallCard | DeckCard, zone: DropZone, event: React.MouseEvent) => void;
  onDragStart?: (cards: (ScryfallCard | DeckCard)[], zone: DropZone, event: React.MouseEvent) => void;
  showQuantity?: boolean;
  quantity?: number;
  availableQuantity?: number;
  className?: string;
  style?: React.CSSProperties;
  selectable?: boolean;
  selected?: boolean;
  disabled?: boolean;
  isDragActive?: boolean;
  isBeingDragged?: boolean;
  selectedCards?: (ScryfallCard | DeckCard)[];
}

const DraggableCard: React.FC<DraggableCardProps> = ({
  card,
  zone,
  size = 'normal',
  onClick,
  onDoubleClick,
  onRightClick,
  onDragStart,
  showQuantity = false,
  quantity,
  availableQuantity,
  className = '',
  style,
  selectable = false,
  selected = false,
  disabled = false,
  isDragActive = false,
  isBeingDragged = false,
  selectedCards = [],
}) => {
  // Handle drag start
  const handleMouseDown = useCallback((event: React.MouseEvent) => {
    // Only handle left mouse button for drag
    if (event.button !== 0 || disabled) return;

    // Don't start drag on double-click
    if (event.detail === 2) return;

    // Determine which cards to drag
    let cardsToDrag: (ScryfallCard | DeckCard)[];
    
    if (selected && selectedCards.length > 0) {
      // If this card is selected and there are multiple selected cards, drag all selected
      cardsToDrag = selectedCards;
    } else {
      // Otherwise, just drag this card
      cardsToDrag = [card];
    }

    // Start drag operation
    onDragStart?.(cardsToDrag, zone, event);
  }, [card, zone, selected, selectedCards, onDragStart, disabled]);

  // Handle regular click (for selection)
  const handleClick = useCallback((e: React.MouseEvent) => {
    // Don't trigger click during drag operations
    if (isDragActive) return;
    
    if (disabled) return;
    e.preventDefault();
    onClick?.(card, e); // Pass the event for Ctrl+click detection
  }, [card, onClick, disabled, isDragActive]);

  // Handle double-click
  const handleDoubleClick = useCallback((event: React.MouseEvent) => {
    // Don't trigger double-click during drag operations
    if (isDragActive) return;
    
    if (disabled) return;
    onDoubleClick?.(card);
  }, [card, onDoubleClick, isDragActive, disabled]);

  // Handle right-click for context menu
  const handleContextMenu = useCallback((event: React.MouseEvent) => {
    // Prevent browser context menu
    event.preventDefault();
    event.stopPropagation();
    
    if (disabled || isDragActive) return;
    
    // Call the right-click handler
    onRightClick?.(card, zone, event);
  }, [card, zone, onRightClick, disabled, isDragActive]);

  // Get drag-specific styles
  const getDragStyles = (): React.CSSProperties => {
    if (isBeingDragged) {
      return {
        opacity: 0.3,
        transform: 'scale(0.95)',
        transition: 'opacity 0.2s ease, transform 0.2s ease',
      };
    }

    if (isDragActive && !selected) {
      return {
        opacity: 0.6,
        transition: 'opacity 0.2s ease',
      };
    }

    return {};
  };

  return (
    <div
      className={`draggable-card ${className}`}
      style={{
        ...style,
        ...getDragStyles(),
        cursor: disabled ? 'default' : (isDragActive ? 'grabbing' : 'grab'),
      }}
      onMouseDown={handleMouseDown}
      onClick={handleClick}
      onDoubleClick={handleDoubleClick}
      onContextMenu={handleContextMenu}
    >
      <MagicCard
        card={card}
        size={size}
        showQuantity={showQuantity}
        quantity={quantity}
        availableQuantity={availableQuantity}
        selected={selected}
        selectable={selectable}
        disabled={disabled}
      />
      
      {/* Multi-selection indicator */}
      {selected && selectedCards.length > 1 && (
        <div
          style={{
            position: 'absolute',
            top: -4,
            right: -4,
            backgroundColor: '#3b82f6',
            color: 'white',
            borderRadius: '50%',
            width: '20px',
            height: '20px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '10px',
            fontWeight: 'bold',
            border: '2px solid white',
            boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
            zIndex: 10,
          }}
        >
          {selectedCards.length}
        </div>
      )}
    </div>
  );
};

export default DraggableCard;