// src/hooks/useResize.ts
import { useCallback, useRef, useEffect } from 'react';
import { PanelDimensions } from './useLayout';

interface ResizeHandlers {
  onFilterPanelResize: (event: React.MouseEvent) => void;
  onDeckAreaResize: (event: React.MouseEvent) => void;
  onSideboardResize: (event: React.MouseEvent) => void;
}

interface UseResizeProps {
  layout: {
    panels: PanelDimensions;
  };
  updatePanelDimensions: (updates: Partial<PanelDimensions>) => void;
  constraints: {
    filterPanelWidth: { min: number; max: number };
    deckAreaHeight: { min: number; max: number };
    sideboardWidth: { min: number; max: number };
  };
}

export const useResize = ({ layout, updatePanelDimensions, constraints }: UseResizeProps) => {
  const resizeStateRef = useRef<{
    isResizing: boolean;
    resizeType: 'filterPanel' | 'deckArea' | 'sideboard' | null;
    startPosition: { x: number; y: number };
    startDimensions: PanelDimensions;
  }>({
    isResizing: false,
    resizeType: null,
    startPosition: { x: 0, y: 0 },
    startDimensions: layout.panels,
  });

  // Update CSS custom property for deck area height
  const updateDeckAreaCSSVariable = useCallback((height: number) => {
    document.documentElement.style.setProperty('--deck-area-height', `${height}px`);
  }, []);

  // Handle mouse move during resize
  const handleMouseMove = useCallback((event: MouseEvent) => {
    const state = resizeStateRef.current;
    if (!state.isResizing || !state.resizeType) return;

    const deltaX = event.clientX - state.startPosition.x;
    const deltaY = event.clientY - state.startPosition.y;

    switch (state.resizeType) {
      case 'filterPanel': {
        const newWidth = state.startDimensions.filterPanelWidth + deltaX;
        const constrainedWidth = Math.max(
          constraints.filterPanelWidth.min,
          Math.min(constraints.filterPanelWidth.max, newWidth)
        );
        updatePanelDimensions({ filterPanelWidth: constrainedWidth });
        break;
      }
      
      case 'deckArea': {
        // Invert the direction - dragging up should make deck area bigger (more intuitive)
        const newDeckHeight = state.startDimensions.deckAreaHeight - deltaY;
        const constrainedHeight = Math.max(
          constraints.deckAreaHeight.min,
          Math.min(constraints.deckAreaHeight.max, newDeckHeight)
        );
        updatePanelDimensions({ deckAreaHeight: constrainedHeight });
        updateDeckAreaCSSVariable(constrainedHeight);
        break;
      }
      
      case 'sideboard': {
        // For sideboard, we resize from the left, so subtract deltaX
        const newWidth = state.startDimensions.sideboardWidth - deltaX;
        const constrainedWidth = Math.max(
          constraints.sideboardWidth.min,
          Math.min(constraints.sideboardWidth.max, newWidth)
        );
        updatePanelDimensions({ sideboardWidth: constrainedWidth });
        break;
      }
    }
  }, [updatePanelDimensions, constraints, updateDeckAreaCSSVariable]);

  // Handle mouse up - end resize
  const handleMouseUp = useCallback(() => {
    const state = resizeStateRef.current;
    if (state.isResizing) {
      state.isResizing = false;
      state.resizeType = null;
      
      // Remove cursor override and user-select disable
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
      document.body.classList.remove('resizing');
    }
  }, []);

  // Set up global event listeners
  useEffect(() => {
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
    
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [handleMouseMove, handleMouseUp]);

  // Initialize CSS variable on mount and when deck area height changes
  useEffect(() => {
    updateDeckAreaCSSVariable(layout.panels.deckAreaHeight);
  }, [layout.panels.deckAreaHeight, updateDeckAreaCSSVariable]);

  // Create resize handler for filter panel (right edge)
  const onFilterPanelResize = useCallback((event: React.MouseEvent) => {
    event.preventDefault();
    event.stopPropagation();
    
    resizeStateRef.current = {
      isResizing: true,
      resizeType: 'filterPanel',
      startPosition: { x: event.clientX, y: event.clientY },
      startDimensions: { ...layout.panels },
    };
    
    // Set cursor and prevent text selection during resize
    document.body.style.cursor = 'ew-resize';
    document.body.style.userSelect = 'none';
    document.body.classList.add('resizing');
  }, [layout.panels]);

  // Create resize handler for deck area (bottom edge of collection)
  const onDeckAreaResize = useCallback((event: React.MouseEvent) => {
    event.preventDefault();
    event.stopPropagation();
    
    resizeStateRef.current = {
      isResizing: true,
      resizeType: 'deckArea',
      startPosition: { x: event.clientX, y: event.clientY },
      startDimensions: { ...layout.panels },
    };
    
    // Set cursor and prevent text selection during resize
    document.body.style.cursor = 'ns-resize';
    document.body.style.userSelect = 'none';
    document.body.classList.add('resizing');
  }, [layout.panels]);

  // Create resize handler for sideboard (left edge)
  const onSideboardResize = useCallback((event: React.MouseEvent) => {
    event.preventDefault();
    event.stopPropagation();
    
    resizeStateRef.current = {
      isResizing: true,
      resizeType: 'sideboard',
      startPosition: { x: event.clientX, y: event.clientY },
      startDimensions: { ...layout.panels },
    };
    
    // Set cursor and prevent text selection during resize
    document.body.style.cursor = 'ew-resize';
    document.body.style.userSelect = 'none';
    document.body.classList.add('resizing');
  }, [layout.panels]);

  const handlers: ResizeHandlers = {
    onFilterPanelResize,
    onDeckAreaResize,
    onSideboardResize,
  };

  return {
    handlers,
    isResizing: resizeStateRef.current.isResizing,
  };
};