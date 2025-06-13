#!/usr/bin/env python3
"""
Update DraggableCard.tsx to integrate FlipCard wrapper
Replaces MagicCard with FlipCard for double-faced card support
"""

import os
import shutil
from pathlib import Path

def update_draggable_card_flip_integration():
    """Update DraggableCard.tsx to use FlipCard wrapper"""
    
    # File path
    file_path = Path("src/components/DraggableCard.tsx")
    
    # Create backup
    backup_path = file_path.with_suffix('.tsx.backup')
    if file_path.exists():
        shutil.copy2(file_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
    
    # Enhanced DraggableCard.tsx with FlipCard integration
    enhanced_content = '''// src/components/DraggableCard.tsx - ENHANCED: FlipCard Integration
import React, { useCallback, useRef } from 'react';
import FlipCard from './FlipCard';
import { ScryfallCard, DeckCard, DeckCardInstance, getCardId, getSelectionId, isCardInstance } from '../types/card';
import { DropZone } from '../hooks/useDragAndDrop';

interface DraggableCardProps {
  card: ScryfallCard | DeckCard | DeckCardInstance;
  zone: DropZone;
  size?: 'small' | 'normal' | 'large';
  scaleFactor?: number;
  onClick?: (card: ScryfallCard | DeckCard | DeckCardInstance, event?: React.MouseEvent) => void;
  onDoubleClick?: (card: ScryfallCard | DeckCard | DeckCardInstance) => void;
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
    let cardsToDrag: (ScryfallCard | DeckCard | DeckCardInstance)[];
    if (selected && selectedCards.length > 0) {
      cardsToDrag = selectedCards;
    } else {
      cardsToDrag = [card];
    }

    // Pass to drag system (it will handle timing and movement detection)
    onDragStart?.(cardsToDrag, zone, event);
  }, [card, zone, selected, selectedCards, onDragStart, onEnhancedDoubleClick, onDoubleClick, disabled]);

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
    
    // Reset interaction state
    interactionRef.current.mouseDownTime = 0;
    interactionRef.current.hasMoved = false;
    interactionRef.current.isDoubleClick = false;
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
      {/* ENHANCED: FlipCard wrapper with 3D flip animation */}
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
        // Pass through all interactions to FlipCard
        onClick={onClick}
        onDoubleClick={onDoubleClick}
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
    </div>
  );
};

export default DraggableCard;'''
    
    # Write the enhanced DraggableCard component
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(enhanced_content)
    
    print(f"✅ Updated: {file_path}")
    print("🎪 DraggableCard now uses FlipCard wrapper")
    print("🔄 3D flip animation integrated with existing drag/drop system")
    print("✅ All interaction patterns preserved")

if __name__ == "__main__":
    update_draggable_card_flip_integration()
