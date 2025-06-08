#!/usr/bin/env python3

"""
Drag & Drop Improvements Script
- Increase drag preview size to 3x with offset positioning
- Center green drop feedback in zones  
- Fix "Cannot Drop" logic for valid zones
- Prevent other card instances from changing appearance
"""

import os
import sys

def update_drag_preview():
    """Update DragPreview.tsx for 3x size and proper cursor offset"""
    
    content = """// src/components/DragPreview.tsx
import React from 'react';
import { ScryfallCard, DeckCard, DeckCardInstance, getCardId } from '../types/card';
import { DragState, DraggedCard } from '../hooks/useDragAndDrop';
import MagicCard from './MagicCard';

interface DragPreviewProps {
  dragState: DragState;
}

const DragPreview: React.FC<DragPreviewProps> = ({ dragState }) => {
  if (!dragState.isDragging || !dragState.dragPreview.visible) {
    return null;
  }

  const { draggedCards, dragPreview, canDrop } = dragState;
  const maxPreviewCards = 3; // Show max 3 cards in preview
  const cardsToShow = draggedCards.slice(0, maxPreviewCards);
  const additionalCount = draggedCards.length - maxPreviewCards;

  return (
    <div
      style={{
        position: 'fixed',
        // IMPROVED: Slight offset from cursor (not centered)
        left: dragPreview.x + 10,
        top: dragPreview.y - 20,
        pointerEvents: 'none',
        zIndex: 10000,
        transform: 'rotate(-5deg) scale(3)', // IMPROVED: 3x larger size
        transformOrigin: 'top left', // IMPROVED: Scale from top-left for better positioning
        filter: canDrop ? 'none' : 'grayscale(50%)',
        opacity: canDrop ? 0.9 : 0.5,
        transition: 'filter 0.2s ease, opacity 0.2s ease',
      }}
    >
      {/* Main card stack */}
      <div style={{ position: 'relative' }}>
        {cardsToShow.map((card, index) => (
          <div
            key={`${getCardId(card)}-${index}`}
            style={{
              position: index === 0 ? 'relative' : 'absolute',
              top: index * 2,
              left: index * 2,
              transform: `rotate(${index * 2}deg)`,
            }}
          >
            <MagicCard
              card={card as any}
              size="small" // Keep base size small, use scale transform for 3x
              style={{
                boxShadow: '0 4px 12px rgba(0,0,0,0.4)',
                border: `2px solid ${canDrop ? '#10b981' : '#ef4444'}`,
              }}
            />
          </div>
        ))}
        
        {/* Count indicator for multiple cards */}
        {draggedCards.length > 1 && (
          <div
            style={{
              position: 'absolute',
              top: -8,
              right: -8,
              backgroundColor: canDrop ? '#10b981' : '#ef4444',
              color: 'white',
              borderRadius: '50%',
              width: '24px',
              height: '24px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '12px',
              fontWeight: 'bold',
              border: '2px solid white',
              boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
            }}
          >
            {draggedCards.length}
          </div>
        )}

        {/* Additional count indicator */}
        {additionalCount > 0 && (
          <div
            style={{
              position: 'absolute',
              bottom: -12,
              left: '50%',
              transform: 'translateX(-50%)',
              backgroundColor: 'rgba(0,0,0,0.8)',
              color: 'white',
              padding: '2px 6px',
              borderRadius: '4px',
              fontSize: '10px',
              whiteSpace: 'nowrap',
            }}
          >
            +{additionalCount} more
          </div>
        )}
      </div>

      {/* REMOVED: Drop zone indicator under preview to reduce visual clutter */}
    </div>
  );
};

export default DragPreview;"""
    
    with open('src/components/DragPreview.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Updated DragPreview.tsx - 3x size with cursor offset")

def update_drop_zone():
    """Update DropZone.tsx for centered feedback and better logic"""
    
    content = """// src/components/DropZone.tsx - IMPROVED Drop Zone with Centered Feedback
import React, { useRef, useEffect, useState, useCallback } from 'react';
import { DropZone as DropZoneType, DraggedCard } from '../hooks/useDragAndDrop';

interface DropZoneProps {
  zone: DropZoneType;
  onDragEnter: (zone: DropZoneType, canDrop: boolean) => void;
  onDragLeave: () => void;
  canDrop: boolean;
  isDragActive: boolean;
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
}

const DropZoneComponent: React.FC<DropZoneProps> = ({
  zone,
  onDragEnter,
  onDragLeave,
  canDrop,
  isDragActive,
  children,
  className = '',
  style,
}) => {
  const [isHovered, setIsHovered] = useState(false);
  const dropZoneRef = useRef<HTMLDivElement>(null);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const mouseTrackingRef = useRef<{
    isInside: boolean;
    lastEvent: MouseEvent | null;
  }>({
    isInside: false,
    lastEvent: null,
  });

  // Enhanced mouse enter - more aggressive detection for fast drags
  const handleMouseEnter = useCallback((event: React.MouseEvent) => {
    if (!isDragActive) return;
    
    console.log(`🎯 Mouse entered ${zone} zone`);
    
    // Clear any pending leave timeout
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    
    mouseTrackingRef.current.isInside = true;
    setIsHovered(true);
    onDragEnter(zone, canDrop);
  }, [isDragActive, zone, canDrop, onDragEnter]);

  // Enhanced mouse leave - with delay for fast movements
  const handleMouseLeave = useCallback((event: React.MouseEvent) => {
    if (!isDragActive) return;
    
    console.log(`📤 Mouse leaving ${zone} zone`);
    
    // Clear any existing timeout
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    
    // Short delay before actually leaving - helps with fast movements
    timeoutRef.current = setTimeout(() => {
      if (!mouseTrackingRef.current.isInside) {
        console.log(`✅ Confirmed mouse left ${zone} zone`);
        setIsHovered(false);
        onDragLeave();
      }
    }, 50); // 50ms delay for fast drag tolerance
    
    mouseTrackingRef.current.isInside = false;
  }, [isDragActive, zone, onDragLeave]);

  // Enhanced global mouse tracking for fast drag detection
  useEffect(() => {
    if (!isDragActive || !dropZoneRef.current) return;

    const handleGlobalMouseMove = (event: MouseEvent) => {
      if (!dropZoneRef.current) return;
      
      const rect = dropZoneRef.current.getBoundingClientRect();
      const buffer = 10; // 10px buffer for easier targeting
      
      // Check if mouse is within drop zone boundaries (with buffer)
      const isInBounds = (
        event.clientX >= rect.left - buffer &&
        event.clientX <= rect.right + buffer &&
        event.clientY >= rect.top - buffer &&
        event.clientY <= rect.bottom + buffer
      );
      
      const wasInside = mouseTrackingRef.current.isInside;
      mouseTrackingRef.current.lastEvent = event;
      
      if (isInBounds && !wasInside) {
        // Fast entry detection
        console.log(`⚡ Fast entry detected for ${zone} zone`);
        
        // Clear any pending leave timeout
        if (timeoutRef.current) {
          clearTimeout(timeoutRef.current);
          timeoutRef.current = null;
        }
        
        mouseTrackingRef.current.isInside = true;
        setIsHovered(true);
        onDragEnter(zone, canDrop);
      } else if (!isInBounds && wasInside) {
        // Fast exit detection with delay
        console.log(`⚡ Fast exit detected for ${zone} zone`);
        
        if (timeoutRef.current) {
          clearTimeout(timeoutRef.current);
        }
        
        timeoutRef.current = setTimeout(() => {
          // Double-check the mouse is still outside
          if (mouseTrackingRef.current.lastEvent) {
            const currentRect = dropZoneRef.current?.getBoundingClientRect();
            if (currentRect) {
              const stillOutside = (
                mouseTrackingRef.current.lastEvent.clientX < currentRect.left - buffer ||
                mouseTrackingRef.current.lastEvent.clientX > currentRect.right + buffer ||
                mouseTrackingRef.current.lastEvent.clientY < currentRect.top - buffer ||
                mouseTrackingRef.current.lastEvent.clientY > currentRect.bottom + buffer
              );
              
              if (stillOutside) {
                console.log(`✅ Confirmed fast exit from ${zone} zone`);
                mouseTrackingRef.current.isInside = false;
                setIsHovered(false);
                onDragLeave();
              }
            }
          }
        }, 30); // Shorter delay for fast drags
      }
    };

    // Add global mouse move listener for fast drag detection
    document.addEventListener('mousemove', handleGlobalMouseMove, { passive: true });

    return () => {
      document.removeEventListener('mousemove', handleGlobalMouseMove);
    };
  }, [isDragActive, zone, canDrop, onDragEnter, onDragLeave]);

  // Cleanup timeout on unmount
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  // Reset hover state when drag ends
  useEffect(() => {
    if (!isDragActive) {
      setIsHovered(false);
      mouseTrackingRef.current.isInside = false;
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
        timeoutRef.current = null;
      }
    }
  }, [isDragActive]);

  // IMPROVED: Enhanced zone-specific styling - NO RED for origin zone
  const getZoneStyles = (): React.CSSProperties => {
    if (!isDragActive) return {};

    const baseStyles: React.CSSProperties = {
      transition: 'all 0.15s ease', // Faster transitions for responsiveness
      position: 'relative',
      minHeight: '100%', // Ensure full height coverage
    };

    // IMPROVED: Only show green for valid drop zones, no red styling for origin zones
    if (isHovered && canDrop) {
      return {
        ...baseStyles,
        backgroundColor: 'rgba(16, 185, 129, 0.15)', // Green for valid drops
        border: '2px dashed #10b981',
        boxShadow: 'inset 0 0 25px rgba(16, 185, 129, 0.25)',
        transform: 'scale(1.002)', // Subtle scale for feedback
      };
    }

    // REMOVED: Red styling for invalid zones - just use subtle neutral styling
    return {
      ...baseStyles,
      border: '1px dashed rgba(156, 163, 175, 0.2)', // Very subtle
      backgroundColor: 'rgba(156, 163, 175, 0.01)', // Nearly transparent
    };
  };

  // Get zone display name
  const getZoneName = (zone: DropZoneType): string => {
    switch (zone) {
      case 'collection': return 'Collection';
      case 'deck': return 'Main Deck';
      case 'sideboard': return 'Sideboard';
      default: return 'Unknown';
    }
  };

  return (
    <div
      ref={dropZoneRef}
      className={`drop-zone drop-zone-${zone} ${className}`}
      style={{
        ...style,
        ...getZoneStyles(),
        // CRITICAL: Ensure drop zone has proper containment
        position: 'relative',
        overflow: 'hidden', // Contain overlays within bounds
      }}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {children}
      
      {/* IMPROVED: Drop indicator overlay - CENTERED and only for valid drops */}
      {isDragActive && isHovered && canDrop && (
        <div
          style={{
            // IMPROVED: Centered both horizontally and vertically
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            backgroundColor: '#10b981', // Always green for valid drops
            color: 'white',
            padding: '12px 20px',
            borderRadius: '8px',
            fontSize: '16px',
            fontWeight: 'bold',
            boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
            zIndex: 1000,
            pointerEvents: 'none',
            border: '2px solid rgba(255,255,255,0.3)',
            whiteSpace: 'nowrap',
            // IMPROVED: Subtle animation
            animation: 'subtle-pulse 1.5s ease-in-out infinite',
          }}
        >
          ✓ Drop here
        </div>
      )}
      
      {/* Add CSS animation for subtle pulse */}
      <style>{`
        @keyframes subtle-pulse {
          0%, 100% { transform: translate(-50%, -50%) scale(1); }
          50% { transform: translate(-50%, -50%) scale(1.05); }
        }
      `}</style>
    </div>
  );
};

export default DropZoneComponent;"""
    
    with open('src/components/DropZone.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Updated DropZone.tsx - Centered feedback, no red zones")

def update_draggable_card():
    """Update DraggableCard.tsx to prevent other instances from changing"""
    
    content = """// src/components/DraggableCard.tsx - IMPROVED: Prevent Other Instances from Changing
import React, { useCallback, useRef } from 'react';
import MagicCard from './MagicCard';
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

  // IMPROVED: Enhanced drag styles - prevent other instances from changing
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

    // REMOVED: Global isDragActive styling that affected other instances
    // This prevents other cards of the same name from changing appearance

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

  // Create a card-compatible object for MagicCard component
  const cardForMagicCard = React.useMemo(() => {
    if (isCardInstance(card)) {
      // Convert DeckCardInstance to card-like object for MagicCard
      // Include all required ScryfallCard properties with sensible defaults
      return {
        id: card.cardId, // Use original card ID for MagicCard
        oracle_id: card.cardId, // Use cardId as fallback for oracle_id
        name: card.name,
        image_uris: undefined, // Will be handled by image_uri
        image_uri: card.image_uri,
        mana_cost: card.mana_cost,
        cmc: card.cmc,
        type_line: card.type_line,
        colors: card.colors,
        color_identity: card.color_identity,
        set: card.set,
        set_name: card.set, // Use set as fallback for set_name
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
        card_faces: undefined,
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
        card={cardForMagicCard}
        size={size}
        scaleFactor={scaleFactor}
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
      

    </div>
  );
};

export default DraggableCard;"""
    
    with open('src/components/DraggableCard.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Updated DraggableCard.tsx - Prevented other instances from changing")

def main():
    """Execute all drag and drop improvements"""
    
    print("🚀 Starting Drag & Drop Improvements...")
    print("")
    
    try:
        update_drag_preview()
        update_drop_zone() 
        update_draggable_card()
        
        print("")
        print("🎉 All drag & drop improvements completed successfully!")
        print("")
        print("📋 Changes made:")
        print("   1. ✅ Drag preview now 3x larger with cursor offset")
        print("   2. ✅ Drop zone feedback centered horizontally and vertically")
        print("   3. ✅ Removed red 'Cannot Drop' feedback for valid zones")
        print("   4. ✅ Prevented other card instances from changing appearance")
        print("")
        print("🧪 Test the improvements:")
        print("   • Drag preview should be much larger and positioned near cursor")
        print("   • Green 'Drop here' should appear centered in valid zones")
        print("   • No more red zone styling or 'Cannot Drop' on valid zones")
        print("   • Other instances of dragged cards should stay normal")
        print("")
        print("💡 Run 'npm start' to test the enhanced drag & drop experience!")
        
    except Exception as e:
        print(f"❌ Error during update: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
