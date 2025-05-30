// src/hooks/useCardSizing.ts
// Hook for managing card sizes with persistence

import { useState, useCallback, useEffect } from 'react';

interface CardSizeState {
  collection: number;
  deck: number;
  sideboard: number;
}

interface CardSizeSettings {
  sizes: CardSizeState;
  updateCollectionSize: (size: number) => void;
  updateDeckSize: (size: number) => void;
  updateSideboardSize: (size: number) => void;
  resetToDefaults: () => void;
}

const DEFAULT_SIZES: CardSizeState = {
  collection: 1.4,  // 140% (1.4) default - consistent across all areas
  deck: 1.4,        // 140% (1.4) default - consistent across all areas  
  sideboard: 1.4    // 140% (1.4) default - consistent across all areas
};

const STORAGE_KEY = 'mtg-deck-builder-card-sizes';

/**
 * Hook for managing card sizes across different zones
 */
export const useCardSizing = (): CardSizeSettings => {
  // Initialize state from localStorage or defaults - force clear for consistency
  const [sizes, setSizes] = useState<CardSizeState>(() => {
    // Clear any existing localStorage to fix loading issues
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch (error) {
      console.warn('Failed to clear card sizes from localStorage:', error);
    }
    
    // Always start with clean defaults (140% for all areas)
    console.log('Initializing card sizes with 140% defaults:', DEFAULT_SIZES);
    return { 
      collection: 1.4,
      deck: 1.4, 
      sideboard: 1.4
    };
  });

  // Persist sizes to localStorage whenever they change
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(sizes));
    } catch (error) {
      console.warn('Failed to save card sizes to localStorage:', error);
    }
  }, [sizes]);

  // Update functions
  const updateCollectionSize = useCallback((size: number) => {
    const clampedSize = Math.max(0.7, Math.min(2.5, size));
    setSizes(prev => ({ ...prev, collection: clampedSize }));
  }, []);

  const updateDeckSize = useCallback((size: number) => {
    const clampedSize = Math.max(0.7, Math.min(2.5, size));
    setSizes(prev => ({ ...prev, deck: clampedSize }));
  }, []);

  const updateSideboardSize = useCallback((size: number) => {
    const clampedSize = Math.max(0.7, Math.min(2.5, size));
    setSizes(prev => ({ ...prev, sideboard: clampedSize }));
  }, []);

  const resetToDefaults = useCallback(() => {
    setSizes(DEFAULT_SIZES);
  }, []);

  return {
    sizes,
    updateCollectionSize,
    updateDeckSize,
    updateSideboardSize,
    resetToDefaults
  };
};

export default useCardSizing;