#!/usr/bin/env python3
"""
Fix 3D flip animation with CONTINUOUS rotation - no wiggle
- Problem: -90° creates discontinuous wiggle effect
- Solution: Single continuous rotation 0° → 180° with proper image change
- FIXED: Variable name issue
"""

import os
import shutil

def fix_continuous_flip_rotation():
    """Fix the discontinuous wiggle with continuous rotation"""
    
    # File path
    file_path = "src/components/FlipCard.tsx"
    backup_path = f"{file_path}.backup4"
    
    # Create backup
    if os.path.exists(file_path):
        shutil.copy2(file_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
    
    # FlipCard.tsx with continuous rotation - no wiggle
    continuous_content = '''// src/components/FlipCard.tsx
// Wrapper component for 3D flip animation on double-faced Magic cards
// FIXED: Continuous rotation - no wiggle or discontinuity

import React, { useState, useCallback, useMemo } from 'react';
import MagicCard from './MagicCard';
import { ScryfallCard, DeckCard, DeckCardInstance, getCardImageUri } from '../types/card';

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
 * Simple animation states for continuous rotation
 */
type FlipPhase = 'idle' | 'flipping';

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
 * Get image URI for a specific card face with proper type handling
 */
const getCardFaceImageUri = (
  card: ScryfallCard | DeckCard | DeckCardInstance, 
  faceIndex: number = 0, 
  size: 'small' | 'normal' | 'large' = 'normal'
): string => {
  // Handle double-faced cards
  if ('card_faces' in card && card.card_faces && card.card_faces[faceIndex]) {
    const face = card.card_faces[faceIndex];
    if (face.image_uris) {
      // Use PNG format for highest quality, fallback to requested size
      return face.image_uris.png || face.image_uris[size] || face.image_uris.normal || '';
    }
  }
  
  // Handle single-faced cards with image_uris
  if ('image_uris' in card && card.image_uris) {
    return card.image_uris.png || card.image_uris[size] || card.image_uris.normal || '';
  }
  
  // Handle cards with direct image_uri
  if ('image_uri' in card && card.image_uri) {
    return card.image_uri;
  }
  
  // Fallback to getCardImageUri utility for ScryfallCard
  if ('oracle_id' in card) {
    return getCardImageUri(card as ScryfallCard, size);
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
 * FlipCard wrapper component with CONTINUOUS 3D flip animation
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
  // Continuous flip state management
  const [showBackFace, setShowBackFace] = useState(false);
  const [flipPhase, setFlipPhase] = useState<FlipPhase>('idle');

  // Check if this card supports flipping
  const isDoubleFaced = isDoubleFacedCard(card);
  
  // Create face-specific card object for MagicCard with proper type conversion
  const faceCard = useMemo((): ScryfallCard | DeckCard => {
    if (!isDoubleFaced) {
      // For non-double-faced cards, convert DeckCardInstance to compatible format
      if ('instanceId' in card) {
        // Convert DeckCardInstance to DeckCard format
        return {
          id: card.cardId,
          name: card.name,
          image_uri: card.image_uri || '',
          mana_cost: card.mana_cost || '',
          cmc: card.cmc || 0,
          type_line: card.type_line || '',
          colors: card.colors || [],
          color_identity: card.color_identity || [],
          set: card.set || '',
          rarity: card.rarity,
          oracle_text: card.oracle_text || '',
          power: card.power,
          toughness: card.toughness,
          loyalty: card.loyalty,
          quantity: 1,
          maxQuantity: 4,
        } as DeckCard;
      }
      return card as ScryfallCard | DeckCard;
    }

    const faceIndex = showBackFace ? 1 : 0;
    const currentFaceImageUri = getCardFaceImageUri(card, faceIndex, size === 'small' ? 'small' : 'normal');
    
    // Create a card object with the current face's image and data
    if ('card_faces' in card && card.card_faces && card.card_faces[faceIndex]) {
      const currentFace = card.card_faces[faceIndex];
      
      // Convert to ScryfallCard format for MagicCard compatibility
      if ('oracle_id' in card) {
        return {
          ...card,
          image_uri: currentFaceImageUri,
          name: currentFace.name,
          mana_cost: currentFace.mana_cost || card.mana_cost || '',
          type_line: currentFace.type_line || card.type_line || '',
          oracle_text: currentFace.oracle_text || '',
          power: currentFace.power || card.power,
          toughness: currentFace.toughness || card.toughness,
        } as ScryfallCard;
      } else if ('instanceId' in card) {
        // Convert DeckCardInstance with face data to DeckCard
        return {
          id: card.cardId,
          name: currentFace.name,
          image_uri: currentFaceImageUri,
          mana_cost: currentFace.mana_cost || card.mana_cost || '',
          cmc: card.cmc || 0,
          type_line: currentFace.type_line || card.type_line || '',
          colors: card.colors || [],
          color_identity: card.color_identity || [],
          set: card.set || '',
          rarity: card.rarity,
          oracle_text: currentFace.oracle_text || '',
          power: currentFace.power || card.power,
          toughness: currentFace.toughness || card.toughness,
          loyalty: currentFace.loyalty || card.loyalty,
          quantity: 1,
          maxQuantity: 4,
        } as DeckCard;
      } else {
        // DeckCard with face data - explicit type assertion
        const deckCard = card as DeckCard;
        return {
          ...deckCard,
          image_uri: currentFaceImageUri,
          name: currentFace.name,
          mana_cost: currentFace.mana_cost || deckCard.mana_cost || '',
          type_line: currentFace.type_line || deckCard.type_line || '',
          oracle_text: currentFace.oracle_text || '',
          power: currentFace.power || deckCard.power,
          toughness: currentFace.toughness || deckCard.toughness,
        };
      }
    }
    
    // Fallback: return original card with updated image
    if ('instanceId' in card) {
      return {
        id: card.cardId,
        name: card.name,
        image_uri: currentFaceImageUri,
        mana_cost: card.mana_cost || '',
        cmc: card.cmc || 0,
        type_line: card.type_line || '',
        colors: card.colors || [],
        color_identity: card.color_identity || [],
        set: card.set || '',
        rarity: card.rarity,
        oracle_text: card.oracle_text || '',
        power: card.power,
        toughness: card.toughness,
        loyalty: card.loyalty,
        quantity: 1,
        maxQuantity: 4,
      } as DeckCard;
    }
    
    return {
      ...card as ScryfallCard | DeckCard,
      image_uri: currentFaceImageUri,
    };
  }, [card, showBackFace, isDoubleFaced, size]);

  /**
   * Continuous 3D flip handler - single smooth rotation
   */
  const handleFlip = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (flipPhase !== 'idle' || !isDoubleFaced) return; // Prevent multiple flips
    
    console.log(`🎪 Starting continuous flip for ${card.name}`);
    
    // Start continuous rotation
    setFlipPhase('flipping');
    
    // At midpoint (200ms), change the face while card is edge-on (invisible)
    setTimeout(() => {
      const newFaceState = !showBackFace;
      setShowBackFace(newFaceState);
      
      const newFaceName = getCardFaceName(card, newFaceState ? 1 : 0);
      console.log(`🔄 Face changed to: ${newFaceName} (at 90° invisible moment)`);
    }, 200); // Midpoint of 400ms animation
    
    // Complete the animation
    setTimeout(() => {
      setFlipPhase('idle');
      console.log(`✅ Continuous flip complete for ${card.name}`);
    }, 400); // Total animation duration
  }, [card, showBackFace, flipPhase, isDoubleFaced]);

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

  // Continuous animation container styles - SIMPLE AND SMOOTH
  const containerStyles: React.CSSProperties = {
    ...style,
    position: 'relative',
    transformStyle: 'preserve-3d',
    // CONTINUOUS ROTATION: 0° → 180° when flipping, back to 0° when idle
    transform: `perspective(1000px) rotateY(${flipPhase === 'flipping' ? '180deg' : '0deg'})`,
    transition: flipPhase === 'flipping' ? 'transform 0.4s ease-in-out' : 'none',
    // Performance optimization
    willChange: flipPhase === 'flipping' ? 'transform' : 'auto',
    backfaceVisibility: 'hidden',
  };

  // Debug logging
  if (flipPhase !== 'idle') {
    console.log(`🎭 Continuous rotation: ${flipPhase === 'flipping' ? '180deg' : '0deg'} (Phase: ${flipPhase})`);
  }

  return (
    <div className={`flip-card ${className}`} style={containerStyles}>
      {/* Continuous 3D Card Display */}
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
            cursor: flipPhase === 'idle' ? 'pointer' : 'not-allowed',
            border: '1px solid rgba(85, 85, 85, 0.8)',
            zIndex: 50,
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
            // Button stays properly oriented
            transform: 'rotateY(0deg)',
            transformStyle: 'preserve-3d',
            opacity: flipPhase === 'idle' ? 1 : 0.7,
          }}
          onClick={handleFlip}
          onMouseEnter={(e) => {
            if (flipPhase === 'idle') {
              e.currentTarget.style.backgroundColor = 'rgba(74, 74, 74, 0.95)';
              e.currentTarget.style.transform = 'rotateY(0deg) scale(1.05)';
              e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.6)';
              e.currentTarget.style.boxShadow = '0 2px 6px rgba(0, 0, 0, 0.5)';
            }
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = 'rgba(64, 64, 64, 0.9)';
            e.currentTarget.style.transform = 'rotateY(0deg) scale(1)';
            e.currentTarget.style.borderColor = 'rgba(85, 85, 85, 0.8)';
            e.currentTarget.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.4)';
          }}
          title={`Flip to ${showBackFace ? 'front' : 'back'} face ${flipPhase !== 'idle' ? '(flipping...)' : ''}`}
        >
          ↻
        </div>
      )}
    </div>
  );
};

export default FlipCard;'''
    
    # Write the continuous content (FIXED VARIABLE NAME)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(continuous_content)
    
    print(f"✅ Fixed with CONTINUOUS rotation - no wiggle:")
    print(f"   - Simple animation: 0° → 180° (continuous single direction)")
    print(f"   - Face changes at 200ms (90° invisible moment)")
    print(f"   - No discontinuous -90° jump that caused wiggle")
    print(f"   - Single smooth 400ms transition with ease-in-out")
    print(f"   - Natural card flip motion like real physical card")

if __name__ == "__main__":
    fix_continuous_flip_rotation()
