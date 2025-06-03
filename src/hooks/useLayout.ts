// src/hooks/useLayout.ts - PERCENTAGE-BASED LAYOUT SYSTEM
import { useState, useEffect, useCallback } from 'react';

export interface PanelDimensions {
  filterPanelWidth: number;
  deckAreaHeightPercent: number; // Changed to percentage
  sideboardWidth: number;
}

export interface PreviewPaneState {
  visible: boolean;
  position: { x: number; y: number };
  size: { width: number; height: number };
}

export interface LayoutState {
  panels: PanelDimensions;
  previewPane: PreviewPaneState;
  viewModes: {
    collection: 'grid' | 'list';
    deck: 'pile' | 'card' | 'list';
    sideboard: 'pile' | 'card' | 'list';
  };
  cardSizes: {
    collection: number;
    deck: number;
    sideboard: number;
  };
}

// PERCENTAGE-BASED DEFAULTS
const DEFAULT_LAYOUT: LayoutState = {
  panels: {
    filterPanelWidth: 280,
    deckAreaHeightPercent: 30, // 30% of screen height for deck/sideboard
    sideboardWidth: 300,
  },
  previewPane: {
    visible: true,
    position: { x: 20, y: 20 },
    size: { width: 350, height: 490 },
  },
  viewModes: {
    collection: 'grid',
    deck: 'card',
    sideboard: 'card',
  },
  cardSizes: {
    collection: 1, // 0 = small, 1 = normal, 2 = large
    deck: 1,
    sideboard: 0,
  },
};

const STORAGE_KEY = 'mtg-deckbuilder-layout';

// PERCENTAGE-BASED CONSTRAINTS
const CONSTRAINTS = {
  filterPanelWidth: { min: 180, max: 500 },    // Keep search bar accessible (180px minimum)
  deckAreaHeightPercent: { min: 8, max: 75 },  // Allow much smaller/larger ranges
  sideboardWidth: { min: 20, max: 1000 },      // Allow near-invisible (20px = resize handle only)
  previewPane: {
    size: { minWidth: 250, maxWidth: 500, minHeight: 350, maxHeight: 700 },
    position: { minX: 0, minY: 0 },
  },
};

export const useLayout = () => {
  const [layout, setLayout] = useState<LayoutState>(DEFAULT_LAYOUT);

  // Calculate actual pixel heights from percentages
  const getCalculatedHeights = useCallback(() => {
    const viewportHeight = window.innerHeight;
    const deckAreaHeight = Math.round((layout.panels.deckAreaHeightPercent / 100) * viewportHeight);
    const collectionAreaHeight = viewportHeight - deckAreaHeight;
    
    return {
      deckAreaHeight,
      collectionAreaHeight,
      deckAreaHeightPercent: layout.panels.deckAreaHeightPercent,
    };
  }, [layout.panels.deckAreaHeightPercent]);

  // Update CSS custom properties when layout changes
  const updateCSSVariables = useCallback(() => {
    const heights = getCalculatedHeights();
    document.documentElement.style.setProperty('--deck-area-height-percent', `${heights.deckAreaHeightPercent}%`);
    document.documentElement.style.setProperty('--deck-area-height', `${heights.deckAreaHeight}px`);
    document.documentElement.style.setProperty('--collection-area-height', `${heights.collectionAreaHeight}px`);
  }, [getCalculatedHeights]);

  // Load layout from localStorage on mount
  useEffect(() => {
    try {
      const savedLayout = localStorage.getItem(STORAGE_KEY);
      if (savedLayout) {
        const parsed = JSON.parse(savedLayout);
        
        // Handle migration from old pixel-based system
        if (parsed.panels && typeof parsed.panels.deckAreaHeight === 'number') {
          // Convert old pixel value to percentage (approximate)
          const oldPixelHeight = parsed.panels.deckAreaHeight;
          const estimatedPercent = Math.max(25, Math.min(60, Math.round((oldPixelHeight / window.innerHeight) * 100)));
          parsed.panels.deckAreaHeightPercent = estimatedPercent;
          delete parsed.panels.deckAreaHeight; // Remove old property
        }
        
        // Merge with defaults to handle new properties
        setLayout(prev => ({
          ...prev,
          ...parsed,
          panels: { ...prev.panels, ...parsed.panels },
          previewPane: { ...prev.previewPane, ...parsed.previewPane },
          viewModes: { ...prev.viewModes, ...parsed.viewModes },
          cardSizes: { ...prev.cardSizes, ...parsed.cardSizes },
        }));
      }
    } catch (error) {
      console.warn('Failed to load layout from localStorage:', error);
    }
  }, []);

  // Update CSS variables when layout changes or window resizes
  useEffect(() => {
    updateCSSVariables();
    
    const handleResize = () => {
      updateCSSVariables();
    };
    
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [updateCSSVariables]);

  // Save layout to localStorage whenever it changes
  const saveLayout = useCallback((newLayout: LayoutState) => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(newLayout));
    } catch (error) {
      console.warn('Failed to save layout to localStorage:', error);
    }
  }, []);

  // Update panel dimensions with constraints
  const updatePanelDimensions = useCallback((updates: Partial<PanelDimensions>) => {
    setLayout(prev => {
      const newPanels = { ...prev.panels };
      
      // Apply constraints
      if (updates.filterPanelWidth !== undefined) {
        newPanels.filterPanelWidth = Math.max(
          CONSTRAINTS.filterPanelWidth.min,
          Math.min(CONSTRAINTS.filterPanelWidth.max, updates.filterPanelWidth)
        );
      }
      
      if (updates.deckAreaHeightPercent !== undefined) {
        newPanels.deckAreaHeightPercent = Math.max(
          CONSTRAINTS.deckAreaHeightPercent.min,
          Math.min(CONSTRAINTS.deckAreaHeightPercent.max, updates.deckAreaHeightPercent)
        );
      }
      
      if (updates.sideboardWidth !== undefined) {
        newPanels.sideboardWidth = Math.max(
          CONSTRAINTS.sideboardWidth.min,
          Math.min(CONSTRAINTS.sideboardWidth.max, updates.sideboardWidth)
        );
      }

      const newLayout = { ...prev, panels: newPanels };
      saveLayout(newLayout);
      return newLayout;
    });
  }, [saveLayout]);

  // Helper function to update deck area height by pixels (for resize handlers)
  const updateDeckAreaHeightByPixels = useCallback((pixelHeight: number) => {
    const viewportHeight = window.innerHeight;
    const percentage = Math.max(25, Math.min(60, Math.round((pixelHeight / viewportHeight) * 100)));
    updatePanelDimensions({ deckAreaHeightPercent: percentage });
  }, [updatePanelDimensions]);

  // Update preview pane state
  const updatePreviewPane = useCallback((updates: Partial<PreviewPaneState>) => {
    setLayout(prev => {
      const newPreviewPane = { ...prev.previewPane, ...updates };
      
      // Apply position constraints (prevent moving off-screen)
      if (updates.position) {
        const maxX = window.innerWidth - newPreviewPane.size.width - 20;
        const maxY = window.innerHeight - newPreviewPane.size.height - 20;
        
        newPreviewPane.position.x = Math.max(
          CONSTRAINTS.previewPane.position.minX,
          Math.min(maxX, updates.position.x)
        );
        newPreviewPane.position.y = Math.max(
          CONSTRAINTS.previewPane.position.minY,
          Math.min(maxY, updates.position.y)
        );
      }
      
      // Apply size constraints
      if (updates.size) {
        newPreviewPane.size.width = Math.max(
          CONSTRAINTS.previewPane.size.minWidth,
          Math.min(CONSTRAINTS.previewPane.size.maxWidth, updates.size.width)
        );
        newPreviewPane.size.height = Math.max(
          CONSTRAINTS.previewPane.size.minHeight,
          Math.min(CONSTRAINTS.previewPane.size.maxHeight, updates.size.height)
        );
      }

      const newLayout = { ...prev, previewPane: newPreviewPane };
      saveLayout(newLayout);
      return newLayout;
    });
  }, [saveLayout]);

  // Update view modes
  const updateViewMode = useCallback((area: keyof LayoutState['viewModes'], mode: string) => {
    setLayout(prev => {
      const newLayout = {
        ...prev,
        viewModes: {
          ...prev.viewModes,
          [area]: mode,
        },
      };
      saveLayout(newLayout);
      return newLayout;
    });
  }, [saveLayout]);

  // Update card sizes
  const updateCardSize = useCallback((area: keyof LayoutState['cardSizes'], size: number) => {
    setLayout(prev => {
      const newLayout = {
        ...prev,
        cardSizes: {
          ...prev.cardSizes,
          [area]: Math.max(0, Math.min(2, size)), // Constrain to 0-2
        },
      };
      saveLayout(newLayout);
      return newLayout;
    });
  }, [saveLayout]);

  // Reset to defaults
  const resetLayout = useCallback(() => {
    setLayout(DEFAULT_LAYOUT);
    saveLayout(DEFAULT_LAYOUT);
  }, [saveLayout]);

  // Toggle preview pane visibility
  const togglePreviewPane = useCallback(() => {
    updatePreviewPane({ visible: !layout.previewPane.visible });
  }, [layout.previewPane.visible, updatePreviewPane]);

  return {
    layout,
    updatePanelDimensions,
    updateDeckAreaHeightByPixels, // New helper for resize handlers
    updatePreviewPane,
    updateViewMode,
    updateCardSize,
    resetLayout,
    togglePreviewPane,
    constraints: CONSTRAINTS,
    getCalculatedHeights, // Expose for debugging
  };
};