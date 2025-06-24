// src/hooks/useCardSizing.ts
// Hook for managing card sizes with button-based controls

import { useState, useCallback } from 'react';
import { CardSizeMode, getSizeConfig } from '../types/card';

interface CardSizeState {
  collection: CardSizeMode;
  deck: CardSizeMode;
  sideboard: CardSizeMode;
}

interface CardSizeSettings {
  modes: CardSizeState;
  sizes: {
    collection: number;
    deck: number;
    sideboard: number;
  };
  updateCollectionSize: (mode: CardSizeMode) => void;
  updateDeckSize: (mode: CardSizeMode) => void;
  updateSideboardSize: (mode: CardSizeMode) => void;
  resetToDefaults: () => void;
}

const DEFAULT_MODES: CardSizeState = {
  collection: 'normal',  // Start with Normal as default
  deck: 'normal',        // Start with Normal as default
  sideboard: 'normal'    // Start with Normal as default
};

/**
 * Hook for managing card sizes across different zones
 */
export const useCardSizing = (): CardSizeSettings => {
  // No persistence for button-based sizing as specified
  const [modes, setModes] = useState<CardSizeState>(DEFAULT_MODES);

  // Convert modes to scale values for backward compatibility
  const sizes = {
    collection: getSizeConfig(modes.collection).scale,
    deck: getSizeConfig(modes.deck).scale,
    sideboard: getSizeConfig(modes.sideboard).scale
  };

  // Update functions
  const updateCollectionSize = useCallback((mode: CardSizeMode) => {
    setModes(prev => ({ ...prev, collection: mode }));
  }, []);

  const updateDeckSize = useCallback((mode: CardSizeMode) => {
    setModes(prev => ({ ...prev, deck: mode }));
  }, []);

  const updateSideboardSize = useCallback((mode: CardSizeMode) => {
    setModes(prev => ({ ...prev, sideboard: mode }));
  }, []);

  const resetToDefaults = useCallback(() => {
    setModes(DEFAULT_MODES);
  }, []);

  return {
    modes,
    sizes,
    updateCollectionSize,
    updateDeckSize,
    updateSideboardSize,
    resetToDefaults
  };
};

export default useCardSizing;