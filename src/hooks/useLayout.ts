// src/hooks/useLayout.ts
import { useState, useEffect, useCallback } from 'react';

export interface PanelDimensions {
  filterPanelWidth: number;
  deckAreaHeight: number;
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

const DEFAULT_LAYOUT: LayoutState = {
  panels: {
    filterPanelWidth: 280,
    deckAreaHeight: 300,
    sideboardWidth: 250,
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

// Constraints for panel sizing
const CONSTRAINTS = {
  filterPanelWidth: { min: 200, max: 500 },
  deckAreaHeight: { min: 200, max: 600 },
  sideboardWidth: { min: 180, max: 400 },
  previewPane: {
    size: { minWidth: 250, maxWidth: 500, minHeight: 350, maxHeight: 700 },
    position: { minX: 0, minY: 0 }, // maxX and maxY calculated based on window size
  },
};

export const useLayout = () => {
  const [layout, setLayout] = useState<LayoutState>(DEFAULT_LAYOUT);

  // Load layout from localStorage on mount
  useEffect(() => {
    try {
      const savedLayout = localStorage.getItem(STORAGE_KEY);
      if (savedLayout) {
        const parsed = JSON.parse(savedLayout);
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
      
      if (updates.deckAreaHeight !== undefined) {
        newPanels.deckAreaHeight = Math.max(
          CONSTRAINTS.deckAreaHeight.min,
          Math.min(CONSTRAINTS.deckAreaHeight.max, updates.deckAreaHeight)
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
    updatePreviewPane,
    updateViewMode,
    updateCardSize,
    resetLayout,
    togglePreviewPane,
    constraints: CONSTRAINTS,
  };
};