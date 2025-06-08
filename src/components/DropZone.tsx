// src/components/DropZone.tsx - IMPROVED Drop Zone with Centered Feedback
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

export default DropZoneComponent;