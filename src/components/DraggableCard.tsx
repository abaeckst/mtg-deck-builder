// src/components/DraggableCard.tsx - ENHANCED: FlipCard Integration
import React, { useCallback, useRef } from 'react';
import FlipCard from './FlipCard';
import MagicCard from './MagicCard';
import { ScryfallCard, DeckCard, DeckCardInstance, getCardId, getSelectionId, isCardInstance } from '../types/card';
import { DropZone } from '../hooks/useDragAndDrop';

interface DraggableCardProps {
  card: ScryfallCard | DeckCard | DeckCardInstance;
  zone: DropZone;
  size?: 'small' | 'normal' | 'large';
  scaleFactor?: number;
  onClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => void;
  onRightClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, zone: DropZone, event: React.MouseEvent) => void;
  onDragStart?: (cards: (ScryfallCard | DeckCard | DeckCardInstance)[], zone: DropZone, event: React.MouseEvent) => void;
  // Enhanced double-click handler
  onEnhancedDoubleClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, zone: DropZone, event: React.MouseEvent) => void;
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
  selectedCards?: (ScryfallCard | DeckCard | DeckCardInstance)[];
  // Instance-specific props
  instanceId?: string;  // For deck/sideboard cards
  isInstance?: boolean; // Flag to determine behavior
  onInstanceClick?: (instanceId: string, instance: DeckCardInstance, event: React.MouseEvent) => void;
}

const DraggableCard: React.FC<DraggableCardProps> = ({
  card,
  zone,
  size = 'normal',
  scaleFactor = 1,
  onClick,
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
  instanceId,
  isInstance = false,
  onInstanceClick,
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

  // Determine if this is an instance card and get appropriate IDs
  const cardIsInstance = isCardInstance(card) || isInstance;
  const cardInstanceId = isCardInstance(card) ? card.instanceId : instanceId;
  const cardId = getCardId(card);
  const selectionId = getSelectionId(card);

  // Enhanced mouse down handler - detects all double-clicks
  const handleMouseDown = useCallback((event: React.MouseEvent) => {
    // Only handle left mouse button
    if (event.button !== 0 || disabled) return;

    const now = Date.now();
    
    // Detect double-click immediately - ANY click with detail >= 2
    interactionRef.current.isDoubleClick = event.detail >= 2;
    
    if (interactionRef.current.isDoubleClick) {
      console.log(`🔥 Double-click detected on ${card.name} in ${zone} (detail: ${event.detail})`);
      
      // Single enhanced handler - no fallback needed
      if (onEnhancedDoubleClick) {
        console.log(`🔧 Calling enhanced double-click handler for ${card.name}`);
        onEnhancedDoubleClick(card, zone, event);
      } else {
        console.warn(`⚠️ No enhanced double-click handler provided for ${card.name}`);
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

    // FIXED: Always drag single card being interacted with, not entire selection
    // This preserves selection visual state while ensuring only the dragged card moves
    const cardsToDrag: (ScryfallCard | DeckCard | DeckCardInstance)[] = [card];

    console.log(`🔧 DraggableCard drag logic: selected=${selected}, selectedCards.length=${selectedCards.length}, cardsToDrag.length=${cardsToDrag.length}`);
    console.log(`🔧 Card being dragged: ${card.name}`);
    console.log(`🔧 Cards that would have been dragged in old logic:`, selected && selectedCards.length > 0 ? selectedCards.map(c => c.name) : [card.name]);

    // Pass to drag system (it will handle timing and movement detection)
    console.log(`🔧 DraggableCard calling onDragStart with ${cardsToDrag.length} cards:`, cardsToDrag.map(c => c.name));
    console.log(`🔧 onDragStart function:`, onDragStart?.toString().substring(0, 200));
    onDragStart?.(cardsToDrag, zone, event);
  }, [card, zone, selected, selectedCards, onDragStart, onEnhancedDoubleClick, disabled]);

  // Enhanced click handler - handles both card and instance clicks
  const handleClick = useCallback((event: React.MouseEvent) => {
    // Skip if this was part of a double-click or drag operation
    if (interactionRef.current.preventNextClick || 
        interactionRef.current.isDoubleClick || 
        isDragActive) {
      console.log(`Click prevented on ${card.name}: preventNext=${interactionRef.current.preventNextClick}, isDouble=${interactionRef.current.isDoubleClick}, isDragActive=${isDragActive}`);
      return;
    }
    
    if (disabled) return;
    
    console.log(`Single click on ${card.name} in ${zone}, ctrlKey=${event.ctrlKey}, isInstance=${cardIsInstance}, selectionId=${selectionId}`);
    
    // Execute appropriate click action based on card type
    if (cardIsInstance && cardInstanceId && onInstanceClick) {
      // Instance-based click for deck/sideboard cards
      onInstanceClick(cardInstanceId, card as DeckCardInstance, event);
    } else {
      // Card-based click for collection cards
      onClick?.(card, event);
    }
  }, [card, onClick, onInstanceClick, disabled, isDragActive, cardIsInstance, cardInstanceId, zone, selectionId]);

  // Simplified double-click handler (preventDefault only)
  const handleDoubleClick = useCallback((event: React.MouseEvent) => {
    // All double-click logic is handled in mouseDown with enhanced timing system
    event.preventDefault();
    event.stopPropagation();
  }, []);

  // Enhanced right-click handling
  const handleContextMenu = useCallback((event: React.MouseEvent) => {
    event.preventDefault();
    event.stopPropagation();
    
    if (disabled) {
      console.log(`Right-click prevented on ${card.name}: disabled`);
      return;
    }
    
    console.log(`Right-click on ${card.name} in ${zone} - triggering selection`);
    
    // Right-click should select the card
    if (cardIsInstance && cardInstanceId && onInstanceClick) {
      // Instance-based selection for deck/sideboard cards
      onInstanceClick(cardInstanceId, card as DeckCardInstance, event);
    } else {
      // Card-based selection for collection cards
      onClick?.(card, event);
    }
    
    // Then show context menu
    onRightClick?.(card, zone, event);
  }, [card, zone, onRightClick, disabled, cardIsInstance, cardInstanceId, onInstanceClick, onClick]);

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
    
    // Reset interaction state (but preserve double-click flag for a moment)
    interactionRef.current.mouseDownTime = 0;
    interactionRef.current.hasMoved = false;
    // Don't reset isDoubleClick immediately - let the fallback handler check it first
    setTimeout(() => {
      interactionRef.current.isDoubleClick = false;
    }, 50); // Small delay to let fallback handler run
  }, [card, isDragActive]);

  // Enhanced drag styles - prevent other instances from changing
  const getDragStyles = (): React.CSSProperties => {
    // ONLY apply drag styles if THIS specific card is being dragged
    if (isBeingDragged) {
      return {
        opacity: 0.4,
        transform: 'scale(0.95) rotate(2deg)',
        transition: 'all 0.2s ease',
        zIndex: 1000,
        filter: 'brightness(1.1)',
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
    if (isDragActive && isBeingDragged) return 'grabbing'; // Only for THIS card being dragged
    if (isBeingDragged) return 'grabbing';
    return 'grab';
  };

  // Create a card-compatible object for FlipCard component
  const cardForFlipCard = React.useMemo(() => {
    if (isCardInstance(card)) {
      // Convert DeckCardInstance to card-like object for FlipCard
      return {
        id: card.cardId,
        oracle_id: card.cardId,
        name: card.name,
        image_uris: undefined,
        image_uri: card.image_uri,
        mana_cost: card.mana_cost,
        cmc: card.cmc,
        type_line: card.type_line,
        colors: card.colors,
        color_identity: card.color_identity,
        set: card.set,
        set_name: card.set,
        rarity: card.rarity,
        oracle_text: card.oracle_text,
        power: card.power,
        toughness: card.toughness,
        loyalty: card.loyalty,
        legalities: {
          standard: 'legal',
          pioneer: 'legal',
          modern: 'legal',
          legacy: 'legal',
          vintage: 'legal',
          commander: 'legal',
          brawl: 'legal',
          historic: 'legal',
          timeless: 'legal',
          pauper: 'legal'
        },
        keywords: [],
        layout: 'normal',
        // CRITICAL: Preserve card_faces for double-faced card support
        card_faces: card.card_faces,
      } as ScryfallCard;
    }
    return card as ScryfallCard | DeckCard;
  }, [card]);

  return (
    <div
      className={`draggable-card ${className}`}
      style={{
        ...style,
        ...getDragStyles(),
        cursor: getCursor(),
        position: 'relative',
        userSelect: 'none',
      }}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onClick={handleClick}
      onDoubleClick={handleDoubleClick}
      onContextMenu={handleContextMenu}
    >
      {/* CONDITIONAL: FlipCard only for double-faced cards, MagicCard for others */}
      {(() => {
        // Check if this is actually a double-faced card
        const isActuallyDoubleFaced = 'card_faces' in cardForFlipCard && 
                                     cardForFlipCard.card_faces && 
                                     Array.isArray(cardForFlipCard.card_faces) && 
                                     cardForFlipCard.card_faces.length >= 2;
        
        if (isActuallyDoubleFaced) {
          // Use FlipCard for actual double-faced cards
          return (
            <FlipCard
              card={cardForFlipCard}
              size={size}
              scaleFactor={scaleFactor}
              showQuantity={showQuantity}
              quantity={quantity}
              availableQuantity={availableQuantity}
              selected={selected}
              selectable={selectable}
              disabled={disabled}
            />
          );
        } else {
          // Use MagicCard directly for single-faced cards
          return (
            <MagicCard
              card={cardForFlipCard}
              size={size}
              scaleFactor={scaleFactor}
              showQuantity={showQuantity}
              quantity={quantity}
              availableQuantity={availableQuantity}
              selected={selected}
              selectable={selectable}
              disabled={disabled}
            />
          );
        }
      })()}
      
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
    </div>
  );
};

export default DraggableCard;