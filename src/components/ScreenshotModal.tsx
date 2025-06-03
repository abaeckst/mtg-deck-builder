import React, { useState, useMemo, useEffect, useCallback } from 'react';
import { Modal } from './Modal';
import MagicCard from './MagicCard';
import { DeckCardInstance, groupInstancesByCardId } from '../types/card';
import { 
  arrangeCardsForScreenshot, 
  getCardQuantityInGroup,
  measureAvailableSpace,
  calculateOptimalCardSize,
  determineScrollingNeeded,
  ViewportDimensions,
  CardLayoutCalculation,
  SIZE_OVERRIDES
} from '../utils/screenshotUtils';

interface ScreenshotModalProps {
  isOpen: boolean;
  onClose: () => void;
  mainDeck: DeckCardInstance[];
  sideboard: DeckCardInstance[];
  deckName?: string;
}

export const ScreenshotModal: React.FC<ScreenshotModalProps> = ({
  isOpen,
  onClose,
  mainDeck,
  sideboard,
  deckName = 'Untitled Deck'
}) => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Dynamic sizing state
  const [sizeMode, setSizeMode] = useState<'auto' | 'small' | 'medium' | 'large'>('auto');
  const [viewportDimensions, setViewportDimensions] = useState<ViewportDimensions | null>(null);
  const [cardLayout, setCardLayout] = useState<(CardLayoutCalculation & { 
    mainDeckColumns: number; 
    sideboardColumns: number;
    mainDeckAbsoluteHeight: number;
    sideboardAbsoluteHeight: number;
  }) | null>(null);
  
  // Arrange cards for screenshot layout with dynamic columns
  const layout = useMemo(() => {
    if (!cardLayout) {
      return arrangeCardsForScreenshot(mainDeck, sideboard, 12, 6);
    }
    return arrangeCardsForScreenshot(mainDeck, sideboard, cardLayout.mainDeckColumns, cardLayout.sideboardColumns);
  }, [mainDeck, sideboard, cardLayout]);
  
  // Simple calculation effect with DOM verification
  useEffect(() => {
    const handleCalculation = () => {
      const dimensions = measureAvailableSpace();
      
      // Calculate layout based on current size mode
      let layout;
      if (sizeMode === 'auto') {
        // Use mathematical optimization
        layout = calculateOptimalCardSize(mainDeck.length, sideboard.length, dimensions);
      } else {
        // For manual size modes, calculate with forced scale
        layout = calculateOptimalCardSize(mainDeck.length, sideboard.length, dimensions, SIZE_OVERRIDES[sizeMode]);
      }
      
      console.log('Layout calculated:', layout);
      setViewportDimensions(dimensions);
      setCardLayout(layout);
      
      // Add DOM verification after a short delay to allow rendering
      setTimeout(() => {
        verifyLayoutFits();
      }, 100);
    };
    
    if (isOpen) {
      // Calculate immediately when modal opens
      handleCalculation();
      
      // Recalculate on window resize
      window.addEventListener('resize', handleCalculation);
      return () => window.removeEventListener('resize', handleCalculation);
    }
  }, [isOpen, mainDeck.length, sideboard.length, sizeMode]);
  
  // DOM verification function
  const verifyLayoutFits = useCallback(() => {
    const previewElement = document.getElementById('screenshot-preview');
    if (!previewElement) return;
    
    const isOverflowing = previewElement.scrollHeight > previewElement.clientHeight || 
                         previewElement.scrollWidth > previewElement.clientWidth;
    
    if (isOverflowing && cardLayout && sizeMode === 'auto') {
      console.warn('DOM verification: Layout is overflowing, reducing scale');
      const reducedScale = cardLayout.calculatedScale * 0.9; // Reduce by 10%
      const correctedLayout = calculateOptimalCardSize(
        mainDeck.length, 
        sideboard.length, 
        viewportDimensions!, 
        reducedScale
      );
      setCardLayout(correctedLayout);
    } else if (isOverflowing) {
      console.warn('DOM verification: Layout overflowing but not in auto mode');
    } else {
      console.log('DOM verification: Layout fits correctly');
    }
  }, [cardLayout, sizeMode, mainDeck.length, sideboard.length, viewportDimensions]);
  
  // Group cards for quantity calculation
  const mainDeckGroups = useMemo(() => {
    return groupInstancesByCardId(mainDeck);
  }, [mainDeck]);
  
  const sideboardGroups = useMemo(() => {
    return groupInstancesByCardId(sideboard);
  }, [sideboard]);
  
  // Calculate final card props based on calculated layout
  const getFinalCardProps = useCallback(() => {
    if (!cardLayout) return { size: 'normal' as const, scaleFactor: 1.0 };
    
    let finalScale = cardLayout.calculatedScale;
    
    if (sizeMode !== 'auto') {
      finalScale = SIZE_OVERRIDES[sizeMode];
    }
    
    return {
      size: finalScale > 0.8 ? 'normal' as const : 'small' as const,
      scaleFactor: finalScale
    };
  }, [cardLayout, sizeMode]);
  
  const cardProps = getFinalCardProps();
  const needsScrolling = cardLayout ? determineScrollingNeeded(
    cardLayout.calculatedScale, 
    sizeMode !== 'auto' ? SIZE_OVERRIDES[sizeMode] : null
  ) : false;

  const handleSaveImage = async () => {
    // Removed download functionality - focusing on layout optimization
    console.log('Screenshot view optimized for full-screen display');
  };
  
  // Handle overlay click to prevent closing when clicking inside modal
  const handleOverlayClick = (event: React.MouseEvent) => {
    // Only close if clicking directly on the overlay, not inside the modal content
    if (event.target === event.currentTarget) {
      onClose();
    }
  };
  
  // Convert DeckCardInstance to ScryfallCard-like object for MagicCard component
  const convertInstanceToCard = (instance: DeckCardInstance) => {
    return {
      id: instance.cardId,
      oracle_id: instance.cardId,
      name: instance.name,
      image_uris: undefined,
      image_uri: instance.image_uri,
      mana_cost: instance.mana_cost,
      cmc: instance.cmc,
      type_line: instance.type_line,
      colors: instance.colors,
      color_identity: instance.color_identity,
      set: instance.set,
      set_name: instance.set,
      rarity: instance.rarity,
      oracle_text: instance.oracle_text,
      power: instance.power,
      toughness: instance.toughness,
      loyalty: instance.loyalty,
      legalities: {
        standard: 'legal' as const,
        pioneer: 'legal' as const,
        modern: 'legal' as const,
        legacy: 'legal' as const,
        vintage: 'legal' as const,
        commander: 'legal' as const,
        brawl: 'legal' as const,
        historic: 'legal' as const,
        timeless: 'legal' as const,
        pauper: 'legal' as const
      },
      keywords: [],
      layout: 'normal' as const,
      card_faces: undefined,
    };
  };
  
  const renderCardWithQuantity = (card: DeckCardInstance, groups: Map<string, DeckCardInstance[]>) => {
    const quantity = getCardQuantityInGroup(groups, card.cardId);
    const cardForMagicCard = convertInstanceToCard(card);
    
    return (
      <div key={card.cardId} className="screenshot-card-wrapper">
        <MagicCard
          card={cardForMagicCard}
          size={cardProps.size}
          scaleFactor={cardProps.scaleFactor}
          showQuantity={quantity > 1}
          quantity={quantity}
          // Use undefined for availableQuantity to only show orange deck quantity badges
          availableQuantity={undefined}
          selectable={false}
          selected={false}
          disabled={false}
        />
      </div>
    );
  };
  
  if (!isOpen) return null;
  
  return (
    // Full viewport overlay
    <div 
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0, 0, 0, 0.95)',
        zIndex: 2000,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}
      onClick={handleOverlayClick}
    >
      {/* Modal content taking full viewport */}
      <div
        style={{
          width: '100vw',
          height: '100vh',
          background: '#1a1a1a',
          position: 'relative',
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        {/* Close button - top right */}
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            background: 'rgba(60, 60, 60, 0.8)',
            border: '1px solid #666',
            borderRadius: '6px',
            color: '#fff',
            fontSize: '20px',
            width: '40px',
            height: '40px',
            cursor: 'pointer',
            zIndex: 2001,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backdropFilter: 'blur(8px)'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = 'rgba(80, 80, 80, 0.9)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'rgba(60, 60, 60, 0.8)';
          }}
        >
          ×
        </button>
        
        {/* Main content area with full space utilization */}
        <div 
          id="screenshot-preview" 
          style={{
            flex: 1,
            overflow: 'auto',
            padding: '20px',
            background: '#1a1a1a',
            display: 'flex',
            flexDirection: 'column'
          }}
        >
          {/* Main Deck Layout with absolute height */}
          {layout.mainDeckColumns.some((column: DeckCardInstance[]) => column.length > 0) && (
            <div style={{
              height: cardLayout?.mainDeckAbsoluteHeight ? `${cardLayout.mainDeckAbsoluteHeight}px` : 'auto',
              display: 'flex',
              flexDirection: 'column',
              flexShrink: 0, // Don't shrink from calculated size
              marginBottom: '16px'
            }}>
              <div style={{ 
                color: '#e0e0e0', 
                fontSize: '16px', 
                marginBottom: '8px',
                fontWeight: '600',
                textAlign: 'center',
                flexShrink: 0
              }}>
                Main Deck ({mainDeck.length} cards)
              </div>
              
              <div className="screenshot-deck-layout" style={{
                display: 'grid',
                gridTemplateColumns: `repeat(${cardLayout?.mainDeckColumns || 12}, 1fr)`,
                gap: '2px',
                padding: '4px',
                flex: 1,
                alignContent: 'start',
                overflow: 'hidden'
              }}>
                {layout.mainDeckColumns.map((column: DeckCardInstance[], columnIndex: number) => (
                  <div key={columnIndex} className="screenshot-column" style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '2px',
                    alignItems: 'center'
                  }}>
                    {column.map((card: DeckCardInstance) => renderCardWithQuantity(card, mainDeckGroups))}
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {/* Sideboard Layout with absolute height */}
          {layout.sideboardColumns.some((column: DeckCardInstance[]) => column.length > 0) && (
            <div style={{
              height: cardLayout?.sideboardAbsoluteHeight ? `${cardLayout.sideboardAbsoluteHeight}px` : 'auto',
              display: 'flex',
              flexDirection: 'column',
              flexShrink: 0 // Don't shrink from calculated size
            }}>
              <div style={{ 
                color: '#e0e0e0', 
                fontSize: '16px', 
                marginBottom: '8px',
                fontWeight: '600',
                textAlign: 'center',
                flexShrink: 0
              }}>
                Sideboard ({sideboard.length} cards)
              </div>
              
              <div className="screenshot-sideboard-layout" style={{
                display: 'grid',
                gridTemplateColumns: `repeat(${cardLayout?.sideboardColumns || 6}, 1fr)`,
                gap: '2px',
                padding: '4px',
                flex: 1,
                alignContent: 'start',
                overflow: 'hidden'
              }}>
                {layout.sideboardColumns.map((column: DeckCardInstance[], columnIndex: number) => (
                  <div key={columnIndex} className="screenshot-column" style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '2px',
                    alignItems: 'center'
                  }}>
                    {column.map((card: DeckCardInstance) => renderCardWithQuantity(card, sideboardGroups))}
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {/* Empty state */}
          {mainDeck.length === 0 && sideboard.length === 0 && (
            <div style={{ 
              textAlign: 'center', 
              color: '#888', 
              fontSize: '20px',
              padding: '60px',
              borderRadius: '8px'
            }}>
              No cards in deck
            </div>
          )}
        </div>
        
        {error && (
          <div style={{ 
            position: 'absolute',
            bottom: '20px',
            left: '50%',
            transform: 'translateX(-50%)',
            color: '#dc3545', 
            fontSize: '14px', 
            padding: '12px',
            backgroundColor: 'rgba(220, 53, 69, 0.1)',
            border: '1px solid rgba(220, 53, 69, 0.3)',
            borderRadius: '6px',
            zIndex: 2001
          }}>
            {error}
          </div>
        )}
      </div>
      
      {/* CSS for spinner animation */}
      <style>
        {`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}
      </style>
    </div>
  );
};