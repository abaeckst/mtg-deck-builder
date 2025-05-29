// src/components/MagicCard.tsx
// React component for displaying Magic: The Gathering cards

import React, { useState, useCallback } from 'react';
import { ScryfallCard, DeckCard, getCardImageUri } from '../types/card';

/**
 * Props for the MagicCard component
 */
interface MagicCardProps {
  card: ScryfallCard | DeckCard;
  size?: 'small' | 'normal' | 'large';
  onClick?: (card: ScryfallCard | DeckCard) => void;
  onDoubleClick?: (card: ScryfallCard | DeckCard) => void;
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
 * Rarity colors for card borders
 */
const rarityColors = {
  common: '#1e1e1e',
  uncommon: '#c0c0c0',
  rare: '#ffd700',
  mythic: '#ff8c00',
  special: '#d946ef',
  bonus: '#14b8a6',
};

/**
 * Get size styles for different card sizes
 */
const getSizeStyles = (size: 'small' | 'normal' | 'large') => {
  switch (size) {
    case 'small':
      return {
        width: '60px',
        height: '84px',
        fontSize: '10px',
      };
    case 'large':
      return {
        width: '200px',
        height: '279px',
        fontSize: '14px',
      };
    case 'normal':
    default:
      return {
        width: '120px',
        height: '168px',
        fontSize: '12px',
      };
  }
};

/**
 * Magic card component with realistic appearance
 */
export const MagicCard: React.FC<MagicCardProps> = ({
  card,
  size = 'normal',
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
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);

  const sizeStyles = getSizeStyles(size);
  const imageUri = 'image_uri' in card 
    ? card.image_uri 
    : getCardImageUri(card as ScryfallCard, size === 'small' ? 'small' : 'normal');

  /**
   * Handle image loading
   */
  const handleImageLoad = useCallback(() => {
    setImageLoaded(true);
    setImageError(false);
  }, []);

  const handleImageError = useCallback(() => {
    setImageLoaded(false);
    setImageError(true);
  }, []);

  /**
   * Handle click events
   */
  const handleClick = useCallback((e: React.MouseEvent) => {
    if (disabled) return;
    e.preventDefault();
    onClick?.(card);
  }, [card, onClick, disabled]);

  const handleDoubleClick = useCallback((e: React.MouseEvent) => {
    if (disabled) return;
    e.preventDefault();
    onDoubleClick?.(card);
  }, [card, onDoubleClick, disabled]);

  /**
   * Get rarity border color
   */
  const rarityColor = rarityColors[card.rarity] || rarityColors.common;

  /**
   * Card container styles
   */
  const cardStyles: React.CSSProperties = {
    ...sizeStyles,
    ...style,
    position: 'relative',
    borderRadius: '8px',
    border: `2px solid ${selected ? '#3b82f6' : rarityColor}`,
    backgroundColor: '#1a1a1a',
    cursor: selectable || onClick ? 'pointer' : 'default',
    opacity: disabled ? 0.5 : 1,
    transition: 'all 0.2s ease-in-out',
    overflow: 'hidden',
    boxShadow: selected 
      ? '0 0 0 2px #3b82f6, 0 4px 8px rgba(0,0,0,0.3)' 
      : '0 2px 4px rgba(0,0,0,0.3)',
  };

  return (
    <div
      className={`magic-card ${className}`}
      style={cardStyles}
      onClick={handleClick}
      onDoubleClick={handleDoubleClick}
      title={card.name}
    >
      {/* Card Image */}
      <div style={{ 
        width: '100%', 
        height: '100%', 
        position: 'relative',
        overflow: 'hidden',
        borderRadius: '6px',
      }}>
        {!imageError && imageUri ? (
          <img
            src={imageUri}
            alt={card.name}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              display: imageLoaded ? 'block' : 'none',
            }}
            onLoad={handleImageLoad}
            onError={handleImageError}
          />
        ) : null}

        {/* Loading/Error State */}
        {(!imageLoaded && !imageError) || imageError ? (
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: '#2a2a2a',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '8px',
            textAlign: 'center',
          }}>
            {imageError ? (
              <>
                <div style={{
                  fontSize: sizeStyles.fontSize,
                  color: '#ffffff',
                  fontWeight: 'bold',
                  marginBottom: '4px',
                  lineHeight: '1.2',
                  wordBreak: 'break-word',
                }}>
                  {card.name}
                </div>
                <div style={{
                  fontSize: Math.max(8, parseInt(sizeStyles.fontSize) - 2),
                  color: '#888888',
                  lineHeight: '1.1',
                }}>
                  {card.type_line}
                </div>
                {card.mana_cost && (
                  <div style={{
                    fontSize: Math.max(8, parseInt(sizeStyles.fontSize) - 2),
                    color: '#cccccc',
                    marginTop: '2px',
                  }}>
                    {card.mana_cost}
                  </div>
                )}
              </>
            ) : (
              <div style={{
                fontSize: sizeStyles.fontSize,
                color: '#888888',
              }}>
                Loading...
              </div>
            )}
          </div>
        ) : null}

        {/* Quantity Indicators */}
        {showQuantity && (
          <>
            {/* Available Quantity (Collection) */}
            {availableQuantity !== undefined && (
              <div style={{
                position: 'absolute',
                top: '4px',
                right: '4px',
                backgroundColor: '#1e40af',
                color: 'white',
                borderRadius: '50%',
                width: size === 'small' ? '16px' : '20px',
                height: size === 'small' ? '16px' : '20px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: size === 'small' ? '10px' : '12px',
                fontWeight: 'bold',
                border: '1px solid rgba(255,255,255,0.3)',
              }}>
                {availableQuantity}
              </div>
            )}

            {/* Deck Quantity */}
            {quantity !== undefined && quantity > 0 && (
              <div style={{
                position: 'absolute',
                top: availableQuantity !== undefined ? '26px' : '4px',
                right: '4px',
                backgroundColor: '#ca8a04',
                color: 'white',
                borderRadius: '50%',
                width: size === 'small' ? '16px' : '20px',
                height: size === 'small' ? '16px' : '20px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: size === 'small' ? '10px' : '12px',
                fontWeight: 'bold',
                border: '1px solid rgba(255,255,255,0.3)',
              }}>
                {quantity}
              </div>
            )}
          </>
        )}

        {/* Selection Indicator */}
        {selected && (
          <div style={{
            position: 'absolute',
            top: '4px',
            left: '4px',
            backgroundColor: '#3b82f6',
            color: 'white',
            borderRadius: '50%',
            width: size === 'small' ? '16px' : '20px',
            height: size === 'small' ? '16px' : '20px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: size === 'small' ? '10px' : '12px',
            fontWeight: 'bold',
          }}>
            ✓
          </div>
        )}

        {/* Hover Effect */}
        {(selectable || onClick) && !disabled && (
          <div
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundColor: 'rgba(255,255,255,0.1)',
              opacity: 0,
              transition: 'opacity 0.2s ease-in-out',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.opacity = '1';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.opacity = '0';
            }}
          />
        )}
      </div>
    </div>
  );
};

/**
 * Card placeholder component for loading states
 */
export const CardPlaceholder: React.FC<{
  size?: 'small' | 'normal' | 'large';
  className?: string;
  style?: React.CSSProperties;
}> = ({ size = 'normal', className = '', style }) => {
  const sizeStyles = getSizeStyles(size);

  return (
    <div
      className={`card-placeholder ${className}`}
      style={{
        ...sizeStyles,
        ...style,
        backgroundColor: '#2a2a2a',
        border: '2px solid #404040',
        borderRadius: '8px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        animation: 'pulse 2s infinite',
      }}
    >
      <div style={{
        fontSize: sizeStyles.fontSize,
        color: '#666666',
      }}>
        Loading...
      </div>
    </div>
  );
};

/**
 * Grid of Magic cards
 */
export const CardGrid: React.FC<{
  cards: (ScryfallCard | DeckCard)[];
  cardSize?: 'small' | 'normal' | 'large';
  onCardClick?: (card: ScryfallCard | DeckCard) => void;
  onCardDoubleClick?: (card: ScryfallCard | DeckCard) => void;
  showQuantities?: boolean;
  selectedCards?: Set<string>;
  className?: string;
  style?: React.CSSProperties;
}> = ({
  cards,
  cardSize = 'normal',
  onCardClick,
  onCardDoubleClick,
  showQuantities = false,
  selectedCards = new Set(),
  className = '',
  style,
}) => {
  const gridStyles: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: `repeat(auto-fill, minmax(${
      cardSize === 'small' ? '70px' : 
      cardSize === 'large' ? '210px' : '130px'
    }, 1fr))`,
    gap: '8px',
    padding: '8px',
    ...style,
  };

  return (
    <div className={`card-grid ${className}`} style={gridStyles}>
      {cards.map((card) => (
        <MagicCard
          key={card.id}
          card={card}
          size={cardSize}
          onClick={onCardClick}
          onDoubleClick={onCardDoubleClick}
          showQuantity={showQuantities}
          quantity={'quantity' in card ? card.quantity : undefined}
          availableQuantity={showQuantities ? 4 : undefined} // Simulate full collection
          selected={selectedCards.has(card.id)}
          selectable={true}
        />
      ))}
    </div>
  );
};

export default MagicCard;