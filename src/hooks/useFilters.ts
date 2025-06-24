// src/hooks/useFilters.ts - Extracted filter management from useCards
import { useState, useCallback, useMemo } from 'react';

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
  searchMode: {
    name: boolean;
    cardText: boolean;
  };
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
  toggleSearchMode: (mode: 'name' | 'cardText') => void;
  getSearchModeText: () => string;
}

const DEFAULT_FILTER_STATE: FilterState = {
  format: 'standard', // CHANGED: Default format to standard instead of custom-standard
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
  searchMode: {
    name: true,      // Default: Name search ON
    cardText: false, // Default: Card text search OFF
  },
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

  // PERFORMANCE FIX: Memoize activeFilters to prevent unnecessary re-renders
  const memoizedActiveFilters = useMemo(() => state.activeFilters, [
    state.activeFilters.format,
    state.activeFilters.colors,
    state.activeFilters.colorIdentity,
    state.activeFilters.types,
    state.activeFilters.rarity,
    state.activeFilters.sets,
    state.activeFilters.cmc.min,
    state.activeFilters.cmc.max,
    state.activeFilters.power.min,
    state.activeFilters.power.max,
    state.activeFilters.toughness.min,
    state.activeFilters.toughness.max,
    state.activeFilters.subtypes,
    state.activeFilters.isGoldMode,
    state.activeFilters.searchMode.name,
    state.activeFilters.searchMode.cardText,
    state.activeFilters.sectionStates,
  ]);

  // PERFORMANCE FIX: Memoize hasActiveFilters function
  const memoizedHasActiveFilters = useCallback((): boolean => {
    const filters = memoizedActiveFilters;
    return (
      // Format filter: only active if NOT standard (since standard is default)
      (filters.format !== '' && filters.format !== 'standard') ||
      // Color filters
      filters.colors.length > 0 ||
      filters.isGoldMode ||
      // Type filters  
      filters.types.length > 0 ||
      filters.subtypes.length > 0 ||
      // Property filters
      filters.rarity.length > 0 ||
      filters.sets.length > 0 ||
      // Range filters
      filters.cmc.min !== null ||
      filters.cmc.max !== null ||
      filters.power.min !== null ||
      filters.power.max !== null ||
      filters.toughness.min !== null ||
      filters.toughness.max !== null
    );
  }, [memoizedActiveFilters]);

  // Toggle search mode functions
  const toggleSearchMode = useCallback((mode: 'name' | 'cardText') => {
    console.log('🔍 Toggle search mode:', mode);
    setState(prev => ({
      ...prev,
      activeFilters: {
        ...prev.activeFilters,
        searchMode: {
          ...prev.activeFilters.searchMode,
          [mode]: !prev.activeFilters.searchMode[mode],
        },
      },
    }));
  }, []);

  const getSearchModeText = useCallback((): string => {
    const { name, cardText } = state.activeFilters.searchMode;
    if (name && cardText) {
      return 'Searching names and text...';
    } else if (name && !cardText) {
      return 'Searching names...';
    } else if (!name && cardText) {
      return 'Searching card text...';
    } else {
      return 'Select search mode';
    }
  }, [state.activeFilters.searchMode]);

  return {
    ...state,
    activeFilters: memoizedActiveFilters,
    updateFilter,
    clearAllFilters,
    toggleFiltersCollapsed,
    hasActiveFilters: memoizedHasActiveFilters,
    updateSectionState,
    getSectionState,
    autoExpandSection,
    toggleSearchMode,
    getSearchModeText,
  };
};