// src/hooks/useFilters.ts - Extracted filter management from useCards
import { useState, useCallback } from 'react';

// Phase 4B: Enhanced filter state interface
export interface FilterState {
  format: string;
  colors: string[];
  colorIdentity: 'subset' | 'exact' | 'include';
  types: string[];
  rarity: string[];
  sets: string[];
  cmc: { min: number | null; max: number | null };
  power: { min: number | null; max: number | null };
  toughness: { min: number | null; max: number | null };
  subtypes: string[];
  isGoldMode: boolean;
  sectionStates: {
    colors: boolean;
    cmc: boolean;
    types: boolean;
    subtypes: boolean;
    sets: boolean;
    rarity: boolean;
    stats: boolean;
  };
}

export interface UseFiltersState {
  activeFilters: FilterState;
  isFiltersCollapsed: boolean;
}

export interface UseFiltersActions {
  updateFilter: (filterType: string, value: any) => void;
  clearAllFilters: () => void;
  toggleFiltersCollapsed: () => void;
  hasActiveFilters: () => boolean;
  updateSectionState: (section: string, isExpanded: boolean) => void;
  getSectionState: (section: string) => boolean;
  autoExpandSection: (section: string) => void;
}

const DEFAULT_FILTER_STATE: FilterState = {
  format: 'custom-standard',
  colors: [],
  colorIdentity: 'subset',
  types: [],
  rarity: [],
  sets: [],
  cmc: { min: null, max: null },
  power: { min: null, max: null },
  toughness: { min: null, max: null },
  subtypes: [],
  isGoldMode: false,
  sectionStates: {
    colors: true,      // Default sections expanded
    cmc: true,
    types: true,
    subtypes: false,   // Advanced sections collapsed
    sets: false,
    rarity: false,
    stats: false,
  },
};

export const useFilters = (): UseFiltersState & UseFiltersActions => {
  const [state, setState] = useState<UseFiltersState>({
    activeFilters: DEFAULT_FILTER_STATE,
    isFiltersCollapsed: false,
  });

  // Update individual filter
  const updateFilter = useCallback((filterType: string, value: any) => {
    console.log('🎛️ Filter update:', filterType, '=', value);
    setState(prev => {
      const newFilters = {
        ...prev.activeFilters,
        [filterType]: value,
      };
      console.log('🎛️ New filter state:', newFilters);
      return {
        ...prev,
        activeFilters: newFilters,
      };
    });
  }, []);

  // Clear all filters and reset to defaults
  const clearAllFilters = useCallback(() => {
    console.log('🧹 Clearing all filters');
    setState(prev => ({
      ...prev,
      activeFilters: { ...DEFAULT_FILTER_STATE },
    }));
  }, []);

  // Toggle filter panel collapsed state
  const toggleFiltersCollapsed = useCallback(() => {
    setState(prev => ({
      ...prev,
      isFiltersCollapsed: !prev.isFiltersCollapsed,
    }));
  }, []);

  // Check if any filters are active
  const hasActiveFilters = useCallback((): boolean => {
    const filters = state.activeFilters;
    return (
      filters.format !== '' &&
      filters.format !== 'custom-standard' || // Don't count default format as active
      filters.colors.length > 0 ||
      filters.types.length > 0 ||
      filters.rarity.length > 0 ||
      filters.sets.length > 0 ||
      filters.cmc.min !== null ||
      filters.cmc.max !== null ||
      filters.power.min !== null ||
      filters.power.max !== null ||
      filters.toughness.min !== null ||
      filters.toughness.max !== null ||
      filters.subtypes.length > 0 ||
      filters.isGoldMode
    );
  }, [state.activeFilters]);

  // Phase 4B: Section state management
  const updateSectionState = useCallback((section: string, isExpanded: boolean) => {
    setState(prev => ({
      ...prev,
      activeFilters: {
        ...prev.activeFilters,
        sectionStates: {
          ...prev.activeFilters.sectionStates,
          [section]: isExpanded,
        },
      },
    }));
  }, []);

  const getSectionState = useCallback((section: string): boolean => {
    return state.activeFilters.sectionStates[section as keyof typeof state.activeFilters.sectionStates] ?? true;
  }, [state.activeFilters.sectionStates]);

  const autoExpandSection = useCallback((section: string) => {
    // Auto-expand sections that have active filters
    const filters = state.activeFilters;
    let shouldExpand = false;
    
    switch (section) {
      case 'colors':
        shouldExpand = filters.colors.length > 0 || filters.isGoldMode;
        break;
      case 'types':
        shouldExpand = filters.types.length > 0;
        break;
      case 'subtypes':
        shouldExpand = filters.subtypes.length > 0;
        break;
      case 'rarity':
        shouldExpand = filters.rarity.length > 0;
        break;
      case 'stats':
        shouldExpand = filters.power.min !== null || filters.power.max !== null || 
                     filters.toughness.min !== null || filters.toughness.max !== null;
        break;
      case 'cmc':
        shouldExpand = filters.cmc.min !== null || filters.cmc.max !== null;
        break;
      case 'sets':
        shouldExpand = filters.sets.length > 0;
        break;
    }
    
    if (shouldExpand && !getSectionState(section)) {
      updateSectionState(section, true);
    }
  }, [state.activeFilters, getSectionState, updateSectionState]);

  return {
    ...state,
    updateFilter,
    clearAllFilters,
    toggleFiltersCollapsed,
    hasActiveFilters,
    updateSectionState,
    getSectionState,
    autoExpandSection,
  };
};