#!/usr/bin/env python3
"""
Fix FlipCard layout and button positioning issues while preserving smooth 3D animation
- Fix grid layout disruption in collection area
- Fix flip button positioning to be on the card, not floating above
- Maintain working 3D flip animation
"""

import os

def fix_flip_card_layout():
    filepath = "src/components/FlipCard.tsx"
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    # Create backup
    backup_path = f"{filepath}.backup_layout_fix"
    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original_content)
    
    print(f"✅ Backup created: {backup_path}")
    
    # Fixed FlipCard implementation with proper layout and button positioning
    new_content = '''// src/components/FlipCard.tsx
// Wrapper component for 3D flip animation on double-faced Magic cards
// LAYOUT FIXED: Proper grid compatibility + button positioning

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
 * Animation states for 3D rotation
 */
type FlipState = 'idle' | 'flipping';

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
 * Create a face-specific card object for MagicCard rendering
 */
const createFaceCard = (
  originalCard: ScryfallCard | DeckCard | DeckCardInstance,
  faceIndex: number,
  size: 'small' | 'normal' | 'large'
): ScryfallCard | DeckCard => {
  const faceImageUri = getCardFaceImageUri(originalCard, faceIndex, size === 'small' ? 'small' : 'normal');
  
  // Handle double-faced cards with face-specific data
  if (isDoubleFacedCard(originalCard) && 'card_faces' in originalCard && originalCard.card_faces?.[faceIndex]) {
    const currentFace = originalCard.card_faces[faceIndex];
    
    // Convert to ScryfallCard format for MagicCard compatibility
    if ('oracle_id' in originalCard) {
      return {
        ...originalCard,
        image_uri: faceImageUri,
        name: currentFace.name,
        mana_cost: currentFace.mana_cost || originalCard.mana_cost || '',
        type_line: currentFace.type_line || originalCard.type_line || '',
        oracle_text: currentFace.oracle_text || '',
        power: currentFace.power || originalCard.power,
        toughness: currentFace.toughness || originalCard.toughness,
      } as ScryfallCard;
    } else if ('instanceId' in originalCard) {
      // Convert DeckCardInstance with face data to DeckCard
      return {
        id: originalCard.cardId,
        name: currentFace.name,
        image_uri: faceImageUri,
        mana_cost: currentFace.mana_cost || originalCard.mana_cost || '',
        cmc: originalCard.cmc || 0,
        type_line: currentFace.type_line || originalCard.type_line || '',
        colors: originalCard.colors || [],
        color_identity: originalCard.color_identity || [],
        set: originalCard.set || '',
        rarity: originalCard.rarity,
        oracle_text: currentFace.oracle_text || '',
        power: currentFace.power || originalCard.power,
        toughness: currentFace.toughness || originalCard.toughness,
        loyalty: currentFace.loyalty || originalCard.loyalty,
        quantity: 1,
        maxQuantity: 4,
      } as DeckCard;
    } else {
      // DeckCard with face data
      const deckCard = originalCard as DeckCard;
      return {
        ...deckCard,
        image_uri: faceImageUri,
        name: currentFace.name,
        mana_cost: currentFace.mana_cost || deckCard.mana_cost || '',
        type_line: currentFace.type_line || deckCard.type_line || '',
        oracle_text: currentFace.oracle_text || '',
        power: currentFace.power || deckCard.power,
        toughness: currentFace.toughness || deckCard.toughness,
      };
    }
  }
  
  // Handle single-faced cards or fallback
  if ('instanceId' in originalCard) {
    return {
      id: originalCard.cardId,
      name: originalCard.name,
      image_uri: faceImageUri,
      mana_cost: originalCard.mana_cost || '',
      cmc: originalCard.cmc || 0,
      type_line: originalCard.type_line || '',
      colors: originalCard.colors || [],
      color_identity: originalCard.color_identity || [],
      set: originalCard.set || '',
      rarity: originalCard.rarity,
      oracle_text: originalCard.oracle_text || '',
      power: originalCard.power,
      toughness: originalCard.toughness,
      loyalty: originalCard.loyalty,
      quantity: 1,
      maxQuantity: 4,
    } as DeckCard;
  }
  
  return {
    ...originalCard as ScryfallCard | DeckCard,
    image_uri: faceImageUri,
  };
};

/**
 * FlipCard wrapper component with FIXED layout and button positioning
 * Maintains smooth 3D animation while fixing grid compatibility
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
  // 3D rotation state - tracks total rotation of the card object
  const [rotation, setRotation] = useState(0);
  const [flipState, setFlipState] = useState<FlipState>('idle');

  // Check if this card supports flipping
  const isDoubleFaced = isDoubleFacedCard(card);
  
  // Create both face cards for 3D rendering
  const frontFaceCard = useMemo(() => createFaceCard(card, 0, size), [card, size]);
  const backFaceCard = useMemo(() => createFaceCard(card, 1, size), [card, size]);

  /**
   * True 3D flip handler - rotates the entire card object
   */
  const handleFlip = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (flipState !== 'idle' || !isDoubleFaced) return;
    
    console.log(`🎪 Starting true 3D flip for ${card.name} (current rotation: ${rotation}°)`);
    
    setFlipState('flipping');
    
    // Rotate the entire card object 180° in 3D space
    // Both faces rotate together as a single physical object
    setRotation(prev => prev + 180);
    
    setTimeout(() => {
      setFlipState('idle');
      console.log(`✅ True 3D flip complete for ${card.name} (new rotation: ${rotation + 180}°)`);
    }, 400); // Animation duration
  }, [card, rotation, flipState, isDoubleFaced]);

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

  // FIXED: Minimal container that doesn't disrupt grid layout
  const containerStyles: React.CSSProperties = {
    ...style,
    position: 'relative',
    // REMOVED: perspective moved to inner container
    // REMOVED: width/height that broke grid layout
  };

  // 3D inner card object styles - this rotates as a single unit
  const cardObjectStyles: React.CSSProperties = {
    position: 'relative',
    width: '100%',
    height: '100%',
    perspective: '1000px', // MOVED: perspective here for proper 3D rendering
    transformStyle: 'preserve-3d',
  };

  // 3D rotating inner content
  const rotatingContentStyles: React.CSSProperties = {
    position: 'relative',
    width: '100%',
    height: '100%',
    transformStyle: 'preserve-3d',
    transform: `rotateY(${rotation}deg)`,
    transition: flipState === 'flipping' ? 'transform 0.4s ease-in-out' : 'none',
    // Performance optimization
    willChange: flipState === 'flipping' ? 'transform' : 'auto',
  };

  // Face positioning styles
  const faceStyles: React.CSSProperties = {
    position: 'absolute',
    width: '100%',
    height: '100%',
    backfaceVisibility: 'hidden',
    WebkitBackfaceVisibility: 'hidden',
  };

  const frontFaceStyles: React.CSSProperties = {
    ...faceStyles,
    transform: 'rotateY(0deg)',
  };

  const backFaceStyles: React.CSSProperties = {
    ...faceStyles,
    transform: 'rotateY(180deg)',
  };

  // Determine which face should be "primary" for current rotation
  const normalizedRotation = ((rotation % 360) + 360) % 360;
  const isShowingBack = normalizedRotation > 90 && normalizedRotation < 270;

  // Debug logging during animation
  if (flipState !== 'idle') {
    console.log(`🎭 3D card rotation: ${rotation}° (showing ${isShowingBack ? 'back' : 'front'} face)`);
  }

  return (
    <div className={`flip-card ${className}`} style={containerStyles}>
      {/* 3D Card Object - proper perspective container */}
      <div className="flip-card-3d-container" style={cardObjectStyles}>
        
        {/* Rotating content - both faces positioned back-to-back */}
        <div className="flip-card-3d-content" style={rotatingContentStyles}>
          
          {/* Front Face - positioned at rotateY(0deg) */}
          <div className="flip-card-front-face" style={frontFaceStyles}>
            <MagicCard
              card={frontFaceCard}
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
          </div>
          
          {/* Back Face - positioned at rotateY(180deg) */}
          {isDoubleFaced && (
            <div className="flip-card-back-face" style={backFaceStyles}>
              <MagicCard
                card={backFaceCard}
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
            </div>
          )}
          
        </div>
        
        {/* FIXED: Flip Button positioned properly within card bounds */}
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
              cursor: flipState === 'idle' ? 'pointer' : 'not-allowed',
              border: '1px solid rgba(85, 85, 85, 0.8)',
              zIndex: 50, // FIXED: Lower z-index, positioned within card
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
              opacity: flipState === 'idle' ? 1 : 0.7,
              // CRITICAL: Transform to stay oriented during rotation
              transform: `rotateY(${-rotation}deg)`,
              transformStyle: 'preserve-3d',
            }}
            onClick={handleFlip}
            onMouseEnter={(e) => {
              if (flipState === 'idle') {
                e.currentTarget.style.backgroundColor = 'rgba(74, 74, 74, 0.95)';
                e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.6)';
                e.currentTarget.style.boxShadow = '0 2px 6px rgba(0, 0, 0, 0.5)';
                // Keep counter-rotation during hover
                e.currentTarget.style.transform = `rotateY(${-rotation}deg) scale(1.05)`;
              }
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = 'rgba(64, 64, 64, 0.9)';
              e.currentTarget.style.borderColor = 'rgba(85, 85, 85, 0.8)';
              e.currentTarget.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.4)';
              // Restore counter-rotation
              e.currentTarget.style.transform = `rotateY(${-rotation}deg)`;
            }}
            title={`Flip to ${isShowingBack ? 'front' : 'back'} face ${flipState !== 'idle' ? '(flipping...)' : ''}`}
          >
            ↻
          </div>
        )}
        
      </div>
    </div>
  );
};

export default FlipCard;
'''

    # Write the new content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Successfully updated {filepath}")
    print("\n🔧 LAYOUT AND POSITIONING FIXES:")
    print("   • Fixed grid layout compatibility - removed disruptive container styles")
    print("   • Fixed flip button positioning - now properly positioned on card")  
    print("   • Maintained smooth 3D animation - dual-face physics preserved")
    print("   • Enhanced button behavior - counter-rotates to stay oriented")
    print("   • Proper z-index management - button within card bounds")
    
    return True

if __name__ == "__main__":
    print("🔧 Fixing FlipCard layout and button positioning...")
    success = fix_flip_card_layout()
    if success:
        print("\n🚀 Layout fixes applied!")
        print("   Expected results:")
        print("   • Collection area: Cards in proper grid layout (no stacking)")
        print("   • Flip button: Positioned on card bottom-right corner")
        print("   • Animation: Still smooth 3D rotation (preserved)")
        print("   • Integration: All existing functionality maintained")
    else:
        print("\n❌ Update failed - check file paths and try again")
