// src/components/DragPreview.tsx
import React from 'react';
import { getCardId } from '../types/card';
import { DragState } from '../hooks/useDragAndDrop';
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

export default DragPreview;