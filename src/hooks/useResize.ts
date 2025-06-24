// src/hooks/useResize.ts - Clean CSS/JavaScript Coordination
// Works with ResizeHandles.css foundation and PanelResizing.css behavioral states
// Uses CSS custom properties for dynamic values while preserving CSS foundation
import { useCallback, useRef, useEffect } from 'react';
import { PanelDimensions } from './useLayout';

interface ResizeHandlers {
  onDeckAreaResize: (event: React.MouseEvent) => void;
  onSideboardResize: (event: React.MouseEvent) => void;
  onVerticalResize: (event: React.MouseEvent) => void;
}

interface UseResizeProps {
  layout: {
    panels: PanelDimensions;
  };
  updatePanelDimensions: (updates: Partial<PanelDimensions>) => void;
  updateDeckAreaHeightByPixels: (pixelHeight: number) => void; // New helper function
  constraints: {
    filterPanelWidth: { min: number; max: number };
    deckAreaHeightPercent: { min: number; max: number }; // Updated to percentage
    sideboardWidth: { min: number; max: number };
  };
}

// Clean CSS/JavaScript coordination interface
// CSS handles: Static styling, visual feedback, behavioral states (via ResizeHandles.css + PanelResizing.css)  
// JavaScript handles: Dynamic calculated values via CSS custom properties
// Result: No conflicts, maintainable architecture, functional resize handles
export const useResize = ({ 
  layout, 
  updatePanelDimensions, 
  updateDeckAreaHeightByPixels,
  constraints 
}: UseResizeProps) => {
  const resizeStateRef = useRef<{
    isResizing: boolean;
    resizeType: 'deckArea' | 'sideboard' | 'vertical' | null;
    startPosition: { x: number; y: number };
    startDimensions: PanelDimensions;
    startViewportHeight: number; // Track viewport height for percentage calculations
  }>({
    isResizing: false,
    resizeType: null,
    startPosition: { x: 0, y: 0 },
    startDimensions: layout.panels,
    startViewportHeight: window.innerHeight,
  });

  // Update CSS custom properties - coordinates with CSS foundation without conflicts
  const updateCSSVariables = useCallback((heightPercent: number) => {
    const pixelHeight = Math.round((heightPercent / 100) * window.innerHeight);
    document.documentElement.style.setProperty('--deck-area-height-percent', `${heightPercent}%`);
    document.documentElement.style.setProperty('--deck-area-height', `${pixelHeight}px`);
    document.documentElement.style.setProperty('--collection-area-height', `${window.innerHeight - pixelHeight}px`);
  }, []);

  // Enhanced mouse move with percentage-based calculations
  const handleMouseMove = useCallback((event: MouseEvent) => {
    const state = resizeStateRef.current;
    if (!state.isResizing || !state.resizeType) return;

    // Use requestAnimationFrame for smoother resize operations
    requestAnimationFrame(() => {
      const deltaX = event.clientX - state.startPosition.x;
      const deltaY = event.clientY - state.startPosition.y;

      switch (state.resizeType) {
        
        case 'deckArea':
        case 'vertical': {
          // PERCENTAGE-BASED: Calculate new height percentage
          const currentViewportHeight = window.innerHeight;
          
          // Invert the direction - dragging up should make deck area bigger
          const pixelChange = -deltaY;
          const startPixelHeight = (state.startDimensions.deckAreaHeightPercent / 100) * state.startViewportHeight;
          const newPixelHeight = startPixelHeight + pixelChange;
          
          // Convert to percentage of current viewport
          const newPercentage = (newPixelHeight / currentViewportHeight) * 100;
          
          // Apply constraints
          const constrainedPercentage = Math.max(
            constraints.deckAreaHeightPercent.min,
            Math.min(constraints.deckAreaHeightPercent.max, newPercentage)
          );
          
          // Update using the new helper function
          updateDeckAreaHeightByPixels(Math.round((constrainedPercentage / 100) * currentViewportHeight));
          updateCSSVariables(constrainedPercentage);
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
    });
  }, [updatePanelDimensions, updateDeckAreaHeightByPixels, constraints, updateCSSVariables]);

  // Enhanced mouse up with better cleanup
  const handleMouseUp = useCallback(() => {
    const state = resizeStateRef.current;
    if (state.isResizing) {
      state.isResizing = false;
      state.resizeType = null;
      
      // Enhanced cleanup with CSS coordination
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
      document.body.classList.remove('resizing');
      
      // Remove resize type classes for clean CSS coordination
      const layoutElement = document.querySelector('.mtgo-layout');
      if (layoutElement) {
        layoutElement.classList.remove('resizing', 'resizing-vertical', 'resizing-horizontal');
      }
      
      console.log('Resize operation completed');
    }
  }, []);

  // Set up global event listeners with enhanced performance
  useEffect(() => {
    // Use passive listeners where possible for better performance
    document.addEventListener('mousemove', handleMouseMove, { passive: true });
    document.addEventListener('mouseup', handleMouseUp);
    
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [handleMouseMove, handleMouseUp]);

  // Initialize CSS variables on mount and when layout changes
  // Coordinates with CSSVariables.css definitions - updates dynamic values only
  useEffect(() => {
    updateCSSVariables(layout.panels.deckAreaHeightPercent);
  }, [layout.panels.deckAreaHeightPercent, updateCSSVariables]);

  // Update CSS variables on window resize to maintain percentages
  // Preserves CSS foundation while updating calculated values
  useEffect(() => {
    const handleWindowResize = () => {
      updateCSSVariables(layout.panels.deckAreaHeightPercent);
    };
    
    window.addEventListener('resize', handleWindowResize);
    return () => window.removeEventListener('resize', handleWindowResize);
  }, [layout.panels.deckAreaHeightPercent, updateCSSVariables]);

  // Enhanced resize handler with better user feedback
  const createResizeHandler = useCallback((resizeType: 'deckArea' | 'sideboard' | 'vertical', cursorType: string) => {
    return (event: React.MouseEvent) => {
      event.preventDefault();
      event.stopPropagation();
      
      resizeStateRef.current = {
        isResizing: true,
        resizeType,
        startPosition: { x: event.clientX, y: event.clientY },
        startDimensions: { ...layout.panels },
        startViewportHeight: window.innerHeight,
      };
      
      // Enhanced cursor feedback with CSS coordination
      document.body.style.cursor = cursorType;
      document.body.style.userSelect = 'none';
      document.body.classList.add('resizing');
      
      // Add resize type class for CSS coordination
      const layoutElement = document.querySelector('.mtgo-layout');
      if (layoutElement) {
        layoutElement.classList.add('resizing');
        if (resizeType === 'deckArea' || resizeType === 'vertical') {
          layoutElement.classList.add('resizing-vertical');
        } else if (resizeType === 'sideboard') {
          layoutElement.classList.add('resizing-horizontal');
        }
      }
      
      console.log(`Started ${resizeType} resize operation`);
    };
  }, [layout.panels]);

  // Create resize handlers
  const onDeckAreaResize = useCallback(createResizeHandler('deckArea', 'ns-resize'), [createResizeHandler]);
  const onSideboardResize = useCallback(createResizeHandler('sideboard', 'ew-resize'), [createResizeHandler]);
  const onVerticalResize = useCallback(createResizeHandler('vertical', 'ns-resize'), [createResizeHandler]);

  const handlers: ResizeHandlers = {
    onDeckAreaResize,
    onSideboardResize,
    onVerticalResize,
  };

  return {
    handlers,
    isResizing: resizeStateRef.current.isResizing,
    currentResizeType: resizeStateRef.current.resizeType,
  };
};