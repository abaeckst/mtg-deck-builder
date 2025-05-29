// src/components/DropZone.tsx
import React, { useRef, useEffect, useState } from 'react';
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

  // Handle mouse enter - immediate response
  const handleMouseEnter = () => {
    if (!isDragActive) return;
    
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    
    setIsHovered(true);
    onDragEnter(zone, canDrop);
  };

  // Handle mouse leave - immediate response for drag operations
  const handleMouseLeave = () => {
    if (!isDragActive) return;
    
    // Clear any pending timeout
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    
    setIsHovered(false);
    onDragLeave();
  };

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
    }
  }, [isDragActive]);

  // Get zone-specific styling
  const getZoneStyles = (): React.CSSProperties => {
    if (!isDragActive) return {};

    const baseStyles: React.CSSProperties = {
      transition: 'all 0.2s ease',
      position: 'relative',
    };

    if (isHovered) {
      if (canDrop) {
        return {
          ...baseStyles,
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          border: '2px dashed #10b981',
          boxShadow: 'inset 0 0 20px rgba(16, 185, 129, 0.2)',
        };
      } else {
        return {
          ...baseStyles,
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          border: '2px dashed #ef4444',
          boxShadow: 'inset 0 0 20px rgba(239, 68, 68, 0.2)',
        };
      }
    }

    // Default drag active styling
    return {
      ...baseStyles,
      border: '2px dashed rgba(156, 163, 175, 0.5)',
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
      }}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {children}
      
      {/* Drop indicator overlay */}
      {isDragActive && isHovered && (
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            backgroundColor: canDrop ? '#10b981' : '#ef4444',
            color: 'white',
            padding: '8px 16px',
            borderRadius: '8px',
            fontSize: '14px',
            fontWeight: 'bold',
            boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
            zIndex: 1000,
            pointerEvents: 'none',
            animation: 'dropIndicatorPulse 1s ease-in-out infinite',
          }}
        >
          {canDrop ? (
            <>
              ✓ Drop in {getZoneName(zone)}
            </>
          ) : (
            <>
              ✗ Cannot drop in {getZoneName(zone)}
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default DropZoneComponent;