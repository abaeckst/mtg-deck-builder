// src/components/DraggableCard.tsx - Phase 3A: Perfect Click/Drag Separation
import React, { useCallback, useRef } from 'react';
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
  // Enhanced double-click handler
  onEnhancedDoubleClick?: (card: ScryfallCard | DeckCard, zone: DropZone, event: React.MouseEvent) => void;
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
  onEnhancedDoubleClick,
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
  // Interaction state tracking
  const interactionRef = useRef<{
    mouseDownTime: number;
    mouseDownPosition: { x: number; y: number };
    hasMoved: boolean;
    isDoubleClick: boolean;
    preventNextClick: boolean;
  }>({
    mouseDownTime: 0,
    mouseDownPosition: { x: 0, y: 0 },
    hasMoved: false,
    isDoubleClick: false,
    preventNextClick: false,
  });

  // Enhanced mouse down handler - detects all double-clicks
  const handleMouseDown = useCallback((event: React.MouseEvent) => {
    // Only handle left mouse button
    if (event.button !== 0 || disabled) return;

    const now = Date.now();
    
    // Detect double-click immediately - ANY click with detail >= 2
    interactionRef.current.isDoubleClick = event.detail >= 2;
    
    if (interactionRef.current.isDoubleClick) {
      console.log(`🔥 Double-click detected on ${card.name} in ${zone} (detail: ${event.detail})`);
      
      // CRITICAL: Call enhanced double-click handler for ALL rapid clicks
      if (onEnhancedDoubleClick) {
        onEnhancedDoubleClick(card, zone, event);
      } else {
        // Fallback to original handler
        onDoubleClick?.(card);
      }
      
      // Prevent any further processing of this interaction
      interactionRef.current.preventNextClick = true;
      event.preventDefault();
      event.stopPropagation();
      return;
    }

    // Record mouse down for single click/drag detection
    interactionRef.current.mouseDownTime = now;
    interactionRef.current.mouseDownPosition = { x: event.clientX, y: event.clientY };
    interactionRef.current.hasMoved = false;
    interactionRef.current.preventNextClick = false;

    console.log(`Mouse down on ${card.name} at (${event.clientX}, ${event.clientY})`);

    // Determine which cards would be dragged
    let cardsToDrag: (ScryfallCard | DeckCard)[];
    if (selected && selectedCards.length > 0) {
      cardsToDrag = selectedCards;
    } else {
      cardsToDrag = [card];
    }

    // Pass to drag system (it will handle timing and movement detection)
    onDragStart?.(cardsToDrag, zone, event);
  }, [card, zone, selected, selectedCards, onDragStart, onEnhancedDoubleClick, onDoubleClick, disabled]);

  // Enhanced click handler - only for single clicks
  const handleClick = useCallback((event: React.MouseEvent) => {
    // Skip if this was part of a double-click or drag operation
    if (interactionRef.current.preventNextClick || 
        interactionRef.current.isDoubleClick || 
        isDragActive) {
      console.log(`Click prevented on ${card.name}: preventNext=${interactionRef.current.preventNextClick}, isDouble=${interactionRef.current.isDoubleClick}, isDragActive=${isDragActive}`);
      return;
    }
    
    if (disabled) return;
    
    console.log(`Single click on ${card.name}, ctrlKey=${event.ctrlKey}`);
    
    // Execute single click action
    onClick?.(card, event);
  }, [card, onClick, disabled, isDragActive]);

  // Simplified double-click handler (mainly for fallback)
  const handleDoubleClick = useCallback((event: React.MouseEvent) => {
    // Double-click is already handled in mouseDown for better timing
    // This is just a safety net and preventDefault
    event.preventDefault();
    event.stopPropagation();
    
    console.log(`Double-click event (fallback) on ${card.name}`);
  }, [card]);

  // Enhanced right-click handling
  const handleContextMenu = useCallback((event: React.MouseEvent) => {
    event.preventDefault();
    event.stopPropagation();
    
    if (disabled) {
      console.log(`Right-click prevented on ${card.name}: disabled`);
      return;
    }
    
    console.log(`Right-click on ${card.name} in ${zone}`);
    onRightClick?.(card, zone, event);
  }, [card, zone, onRightClick, disabled]);

  // Mouse move detection for interaction refinement
  const handleMouseMove = useCallback((event: React.MouseEvent) => {
    if (interactionRef.current.mouseDownTime > 0) {
      const deltaX = Math.abs(event.clientX - interactionRef.current.mouseDownPosition.x);
      const deltaY = Math.abs(event.clientY - interactionRef.current.mouseDownPosition.y);
      const movement = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
      
      // Track if significant movement occurred
      if (movement > 3) {
        interactionRef.current.hasMoved = true;
      }
    }
  }, []);

  // Mouse up handler for click detection
  const handleMouseUp = useCallback((event: React.MouseEvent) => {
    // Only process if this was a potential single click
    if (interactionRef.current.mouseDownTime > 0 && 
        !interactionRef.current.isDoubleClick && 
        !interactionRef.current.hasMoved &&
        !isDragActive) {
      
      const holdTime = Date.now() - interactionRef.current.mouseDownTime;
      
      // If it was a quick release without movement, treat as click
      if (holdTime < 200) {
        console.log(`Quick click detected on ${card.name} (${holdTime}ms hold)`);
        // Click will be handled by onClick event
      }
    }
    
    // Reset interaction state
    interactionRef.current.mouseDownTime = 0;
    interactionRef.current.hasMoved = false;
    interactionRef.current.isDoubleClick = false;
  }, [card, isDragActive]);

  // Enhanced drag styles with smooth transitions
  const getDragStyles = (): React.CSSProperties => {
    if (isBeingDragged) {
      return {
        opacity: 0.4,
        transform: 'scale(0.95) rotate(2deg)',
        transition: 'all 0.2s ease',
        zIndex: 1000,
        filter: 'brightness(1.1)',
      };
    }

    if (isDragActive && !selected) {
      return {
        opacity: 0.7,
        transition: 'opacity 0.2s ease',
      };
    }

    return {
      transition: 'all 0.2s ease',
      transform: 'scale(1) rotate(0deg)',
    };
  };

  // Enhanced cursor management
  const getCursor = (): string => {
    if (disabled) return 'default';
    if (isDragActive) return 'grabbing';
    if (isBeingDragged) return 'grabbing';
    return 'grab';
  };

  return (
    <div
      className={`draggable-card ${className}`}
      style={{
        ...style,
        ...getDragStyles(),
        cursor: getCursor(),
        position: 'relative',
        userSelect: 'none', // Prevent text selection during interactions
      }}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
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
      
      {/* Enhanced multi-selection indicator with animation */}
      {selected && selectedCards.length > 1 && (
        <div
          style={{
            position: 'absolute',
            top: -6,
            right: -6,
            backgroundColor: '#3b82f6',
            color: 'white',
            borderRadius: '50%',
            width: '24px',
            height: '24px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '11px',
            fontWeight: 'bold',
            border: '3px solid white',
            boxShadow: '0 3px 6px rgba(0,0,0,0.4)',
            zIndex: 15,
            transition: 'all 0.3s ease',
            animation: selectedCards.length > 3 ? 'pulse 2s infinite' : 'none',
          }}
        >
          {selectedCards.length}
        </div>
      )}
      
      {/* Visual feedback for interaction states */}
      {selected && !isBeingDragged && (
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            border: '2px solid #3b82f6',
            borderRadius: '8px',
            pointerEvents: 'none',
            transition: 'all 0.2s ease',
            boxShadow: '0 0 0 1px rgba(59, 130, 246, 0.3)',
          }}
        />
      )}
    </div>
  );
};

export default DraggableCard;