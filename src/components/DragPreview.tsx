// src/components/DragPreview.tsx
import React from 'react';
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
        left: dragPreview.x,
        top: dragPreview.y,
        pointerEvents: 'none',
        zIndex: 10000,
        transform: 'rotate(-5deg)',
        filter: canDrop ? 'none' : 'grayscale(50%)',
        opacity: canDrop ? 0.9 : 0.5,
        transition: 'filter 0.2s ease, opacity 0.2s ease',
      }}
    >
      {/* Main card stack */}
      <div style={{ position: 'relative' }}>
        {cardsToShow.map((card, index) => (
          <div
            key={`${card.id}-${index}`}
            style={{
              position: index === 0 ? 'relative' : 'absolute',
              top: index * 2,
              left: index * 2,
              transform: `rotate(${index * 2}deg)`,
            }}
          >
            <MagicCard
              card={card}
              size="small"
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

      {/* Drop zone indicator */}
      <div
        style={{
          position: 'absolute',
          top: '100%',
          left: '50%',
          transform: 'translateX(-50%)',
          marginTop: '8px',
          padding: '4px 8px',
          backgroundColor: canDrop ? '#10b981' : '#ef4444',
          color: 'white',
          borderRadius: '4px',
          fontSize: '12px',
          fontWeight: 'bold',
          boxShadow: '0 2px 4px rgba(0,0,0,0.3)',
          whiteSpace: 'nowrap',
        }}
      >
        {canDrop ? '✓ Can Drop' : '✗ Cannot Drop'}
      </div>
    </div>
  );
};

export default DragPreview;