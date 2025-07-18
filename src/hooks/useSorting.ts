// src/hooks/useSorting.ts - PERFORMANCE OPTIMIZED - No localStorage persistence
import { useState, useCallback, useMemo, useRef } from 'react';

export type SortCriteria = 'mana' | 'color' | 'rarity' | 'name' | 'type';
export type SortDirection = 'asc' | 'desc';
export type AreaType = 'collection' | 'deck' | 'sideboard';

interface SortState {
  criteria: SortCriteria;
  direction: SortDirection;
}

interface AreaSortState {
  collection: SortState;
  deck: SortState;
  sideboard: SortState;
}

// Always use these defaults - no localStorage persistence
const DEFAULT_SORT_STATE: AreaSortState = {
  collection: { criteria: 'mana', direction: 'asc' },
  deck: { criteria: 'mana', direction: 'asc' },
  sideboard: { criteria: 'mana', direction: 'asc' },
};

// PERFORMANCE FIX: Stable Scryfall mapping object
const SCRYFALL_SORT_MAPPING: Record<SortCriteria, string> = {
  mana: 'cmc',
  color: 'color',
  rarity: 'rarity',
  name: 'name',
  type: 'type',
};

export const useSorting = () => {
  // PERFORMANCE FIX: Remove excessive logging that was causing console spam
  const initRef = useRef(false);
  if (!initRef.current) {
    console.log('🎯 useSorting initialized with fresh defaults');
    initRef.current = true;
  }
  
  // Always start with fresh defaults - no localStorage loading
  const [sortState, setSortState] = useState<AreaSortState>(DEFAULT_SORT_STATE);

  // PERFORMANCE FIX: Stable updateSort function with proper dependencies
  const updateSort = useCallback((area: AreaType, criteria: SortCriteria, direction?: SortDirection) => {
    console.log('🎯 Sort update:', { area, criteria, direction });
    
    setSortState(prevState => {
      const currentAreaState = prevState[area];
      const newDirection = direction ?? currentAreaState.direction;
      
      // Don't update if values are the same (prevents unnecessary re-renders)
      if (currentAreaState.criteria === criteria && currentAreaState.direction === newDirection) {
        console.log('🎯 Sort unchanged, skipping update');
        return prevState;
      }
      
      const newAreaState = { criteria, direction: newDirection };
      const newState = { ...prevState, [area]: newAreaState };
      
      // PERFORMANCE FIX: Simplified collection sorting logic
      if (area === 'collection') {
        const triggerSearch = (window as any).triggerSearch;
        const metadata = (window as any).lastSearchMetadata;
        
        if (triggerSearch && metadata && metadata.totalCards > 75) {
          console.log('🌐 Server-side sort triggered');
          
          // Set stable override parameters
          const scryfallOrder = SCRYFALL_SORT_MAPPING[criteria];
          (window as any).overrideSortParams = {
            order: scryfallOrder,
            dir: newDirection,
          };
          
          // Trigger search without complex coordination
          setTimeout(() => {
            try {
              triggerSearch(metadata.query, metadata.filters);
            } catch (error) {
              console.error('Sort search failed:', error);
            }
          }, 0);
        }
      }
      
      // No localStorage persistence - session-only sorting
      
      return newState;
    });
  }, []); // PERFORMANCE FIX: Stable dependency array (no localStorage dependency)

  // PERFORMANCE FIX: Stable toggleDirection function
  const toggleDirection = useCallback((area: AreaType) => {
    const currentState = sortState[area];
    const newDirection = currentState.direction === 'asc' ? 'desc' : 'asc';
    updateSort(area, currentState.criteria, newDirection);
  }, [sortState, updateSort]);

  // PERFORMANCE FIX: Memoized getSortState function
  const getSortState = useCallback((area: AreaType): SortState => {
    return sortState[area];
  }, [sortState]);

  // PERFORMANCE FIX: Memoized Scryfall params
  const getScryfallSortParams = useCallback((area: AreaType) => {
    const state = sortState[area];
    return {
      order: SCRYFALL_SORT_MAPPING[state.criteria],
      dir: state.direction,
    };
  }, [sortState]);

  // PERFORMANCE FIX: Static function (no dependencies)
  const isServerSideSupported = useCallback((criteria: SortCriteria): boolean => {
    return criteria in SCRYFALL_SORT_MAPPING;
  }, []);

  // PERFORMANCE FIX: Direct state access (no complex global coordination)
  const getGlobalSortState = useCallback((): AreaSortState => {
    return sortState;
  }, [sortState]);

  // PERFORMANCE FIX: Memoized return object to prevent unnecessary re-renders
  return useMemo(() => ({
    // Core API
    updateSort,
    toggleDirection,
    getSortState,
    sortState,
    
    // Server integration
    getScryfallSortParams,
    isServerSideSupported,
    getGlobalSortState,
    
    // Static utilities
    availableCriteria: ['name', 'mana', 'color', 'rarity'] as SortCriteria[],
    scryfallMapping: SCRYFALL_SORT_MAPPING,
  }), [
    updateSort,
    toggleDirection, 
    getSortState,
    sortState,
    getScryfallSortParams,
    isServerSideSupported,
    getGlobalSortState,
  ]);
};