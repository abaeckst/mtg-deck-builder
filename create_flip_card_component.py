#!/usr/bin/env python3
"""
Create FlipCard.tsx component for 3D flip animation
Wraps MagicCard with double-faced card flip functionality
"""

import os
from pathlib import Path

def create_flip_card_component():
    """Create FlipCard.tsx component with 3D flip animation"""
    
    # Create the FlipCard component
    flip_card_content = '''// src/components/FlipCard.tsx
// Wrapper component for 3D flip animation on double-faced Magic cards

import React, { useState, useCallback, useMemo } from 'react';
import MagicCard from './MagicCard';
import { ScryfallCard, DeckCard, DeckCardInstance } from '../types/card';

interface FlipCardProps {
  card: ScryfallCard | DeckCard | DeckCardInstance;
  size?: 'small' | 'normal' | 'large';
  scaleFactor?: number;
  onClick?: (card: ScryfallCard | DeckCard | DeckCardInstance) => void;
  onDoubleClick?: (card: ScryfallCard | DeckCard | DeckCardInstance) => void;
  showQuantity?: boolean;
  quantity?: number;
  availableQuantity?: number;
  className?: string;
  style?: React.CSSProperties;
  selectable?: boolean;
  selected?: boolean;
  disabled?: boolean;
}

/**
 * Utility function to detect double-faced cards
 */
const isDoubleFacedCard = (card: ScryfallCard | DeckCard | DeckCardInstance): boolean => {
  return 'card_faces' in card && 
         card.card_faces !== undefined && 
         Array.isArray(card.card_faces) && 
         card.card_faces.length >= 2;
};

/**
 * Get image URI for a specific card face
 */
const getCardFaceImageUri = (
  card: ScryfallCard, 
  faceIndex: number = 0, 
  size: 'small' | 'normal' | 'large' = 'normal'
): string => {
  // Handle double-faced cards
  if (card.card_faces && card.card_faces[faceIndex]) {
    const face = card.card_faces[faceIndex];
    if (face.image_uris) {
      // Use PNG format for highest quality, fallback to requested size
      return face.image_uris.png || face.image_uris[size];
    }
  }
  
  // Fallback for single-faced cards or missing face data
  if ('image_uris' in card && card.image_uris) {
    return card.image_uris.png || card.image_uris[size] || card.image_uris.normal;
  }
  
  if ('image_uri' in card && card.image_uri) {
    return card.image_uri;
  }
  
  return '';
};

/**
 * Get card name for a specific face
 */
const getCardFaceName = (card: ScryfallCard | DeckCard | DeckCardInstance, faceIndex: number = 0): string => {
  if (isDoubleFacedCard(card) && 'card_faces' in card && card.card_faces?.[faceIndex]) {
    return card.card_faces[faceIndex].name;
  }
  return card.name;
};

/**
 * FlipCard wrapper component with 3D flip animation
 */
export const FlipCard: React.FC<FlipCardProps> = ({
  card,
  size = 'normal',
  scaleFactor = 1,
  onClick,
  onDoubleClick,
  showQuantity = false,
  quantity,
  availableQuantity,
  className = '',
  style,
  selectable = false,
  selected = false,
  disabled = false,
}) => {
  // 3D Flip state management
  const [showBackFace, setShowBackFace] = useState(false);
  const [isFlipping, setIsFlipping] = useState(false);

  // Check if this card supports flipping
  const isDoubleFaced = isDoubleFacedCard(card);
  
  // Create face-specific card object for MagicCard
  const faceCard = useMemo(() => {
    if (!isDoubleFaced) {
      return card;
    }

    const faceIndex = showBackFace ? 1 : 0;
    const currentFaceImageUri = getCardFaceImageUri(card as ScryfallCard, faceIndex, size === 'small' ? 'small' : 'normal');
    
    // Create a card object with the current face's image
    if ('card_faces' in card && card.card_faces) {
      const currentFace = card.card_faces[faceIndex];
      return {
        ...card,
        image_uri: currentFaceImageUri,
        name: currentFace.name,
        mana_cost: currentFace.mana_cost || card.mana_cost,
        type_line: currentFace.type_line || card.type_line,
        oracle_text: currentFace.oracle_text || '',
        power: currentFace.power || card.power,
        toughness: currentFace.toughness || card.toughness,
      };
    }
    
    return {
      ...card,
      image_uri: currentFaceImageUri,
    };
  }, [card, showBackFace, isDoubleFaced, size]);

  /**
   * Enhanced 3D flip handler
   */
  const handleFlip = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (isFlipping || !isDoubleFaced) return; // Prevent multiple flips
    
    console.log(`🎪 Starting 3D flip for ${card.name}`);
    setIsFlipping(true);
    
    // Start first half of rotation (0° → 90°)
    setTimeout(() => {
      // At 90°, change face (invisible moment)
      const newFaceState = !showBackFace;
      setShowBackFace(newFaceState);
      
      const newFaceName = getCardFaceName(card, newFaceState ? 1 : 0);
      console.log(`🔄 Face changed to: ${newFaceName}`);
    }, 200); // Mid-flip timing
    
    // Complete animation cleanup
    setTimeout(() => {
      setIsFlipping(false);
      console.log(`✅ 3D flip complete for ${card.name}`);
    }, 400); // Total flip duration
  }, [card, showBackFace, isFlipping, isDoubleFaced]);

  /**
   * Get 3D transform rotation value
   */
  const getRotationDegrees = (): number => {
    if (!isFlipping) {
      return showBackFace ? 180 : 0;
    }
    
    // During flip animation, interpolate between states
    return showBackFace ? 90 : 90; // Mid-flip position
  };

  /**
   * Professional flip button sizing based on card size
   */
  const getFlipButtonSize = () => {
    const baseSize = size === 'small' ? 16 : size === 'large' ? 24 : 20;
    const fontSize = size === 'small' ? 12 : size === 'large' ? 16 : 14;
    const clampedScale = Math.max(0.7, Math.min(2.0, scaleFactor));
    
    return {
      buttonSize: Math.round(baseSize * clampedScale),
      fontSize: Math.round(fontSize * clampedScale),
    };
  };

  const { buttonSize, fontSize } = getFlipButtonSize();

  // Container styles with 3D transforms
  const containerStyles: React.CSSProperties = {
    ...style,
    position: 'relative',
    transformStyle: 'preserve-3d',
    transform: `perspective(1000px) rotateY(${getRotationDegrees()}deg)`,
    transition: isFlipping ? 'transform 0.2s ease-in-out' : 'none',
    // Performance optimization
    willChange: isFlipping ? 'transform' : 'auto',
  };

  return (
    <div className={`flip-card ${className}`} style={containerStyles}>
      {/* Enhanced 3D Card Display */}
      <MagicCard
        card={faceCard}
        size={size}
        scaleFactor={scaleFactor}
        onClick={onClick}
        onDoubleClick={onDoubleClick}
        showQuantity={showQuantity}
        quantity={quantity}
        availableQuantity={availableQuantity}
        selectable={selectable}
        selected={selected}
        disabled={disabled}
      />
      
      {/* 3D Flip Button - Only for double-faced cards */}
      {isDoubleFaced && (
        <div
          style={{
            position: 'absolute',
            bottom: '4px',
            right: '4px',
            backgroundColor: 'rgba(64, 64, 64, 0.9)',
            color: '#ffffff',
            borderRadius: '4px',
            padding: `${Math.round(buttonSize / 5)}px`,
            fontSize: `${fontSize}px`,
            cursor: 'pointer',
            border: '1px solid rgba(85, 85, 85, 0.8)',
            zIndex: 50, // Higher than MagicCard elements
            userSelect: 'none',
            transition: 'all 0.2s ease',
            width: `${buttonSize}px`,
            height: `${buttonSize}px`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontFamily: 'monospace',
            fontWeight: 'bold',
            boxShadow: '0 1px 3px rgba(0, 0, 0, 0.4)',
            // Prevent flip during button interactions
            transform: 'rotateY(0deg)',
            transformStyle: 'preserve-3d',
          }}
          onClick={handleFlip}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = 'rgba(74, 74, 74, 0.95)';
            e.currentTarget.style.transform = 'rotateY(0deg) scale(1.05)';
            e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.6)';
            e.currentTarget.style.boxShadow = '0 2px 6px rgba(0, 0, 0, 0.5)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = 'rgba(64, 64, 64, 0.9)';
            e.currentTarget.style.transform = 'rotateY(0deg) scale(1)';
            e.currentTarget.style.borderColor = 'rgba(85, 85, 85, 0.8)';
            e.currentTarget.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.4)';
          }}
          title={`3D Flip to ${showBackFace ? 'front' : 'back'} face`}
        >
          ↻
        </div>
      )}
    </div>
  );
};

export default FlipCard;'''
    
    # Write the FlipCard component
    file_path = Path("src/components/FlipCard.tsx")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(flip_card_content)
    
    print(f"✅ Created: {file_path}")
    print("🎪 FlipCard component created with 3D flip animation")
    print("📁 Next: Update DraggableCard.tsx to use FlipCard wrapper")

if __name__ == "__main__":
    create_flip_card_component()
