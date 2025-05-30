// src/hooks/useSorting.ts - Universal sorting with persistence
import { useState, useEffect, useCallback } from 'react';

export type SortCriteria = 'mana' | 'color' | 'rarity' | 'type';
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

const DEFAULT_SORT_STATE: AreaSortState = {
  collection: { criteria: 'mana', direction: 'asc' },
  deck: { criteria: 'mana', direction: 'asc' },
  sideboard: { criteria: 'mana', direction: 'asc' },
};

const STORAGE_KEY = 'mtg-deckbuilder-sort-state';

export const useSorting = () => {
  const [sortState, setSortState] = useState<AreaSortState>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      return saved ? { ...DEFAULT_SORT_STATE, ...JSON.parse(saved) } : DEFAULT_SORT_STATE;
    } catch {
      return DEFAULT_SORT_STATE;
    }
  });

  // Persist to localStorage whenever sort state changes
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(sortState));
    } catch (error) {
      console.warn('Failed to save sort state to localStorage:', error);
    }
  }, [sortState]);

  const updateSort = useCallback((area: AreaType, criteria: SortCriteria, direction?: SortDirection) => {
    setSortState(prev => ({
      ...prev,
      [area]: {
        criteria,
        direction: direction ?? prev[area].direction,
      },
    }));
  }, []);

  const toggleDirection = useCallback((area: AreaType) => {
    setSortState(prev => ({
      ...prev,
      [area]: {
        ...prev[area],
        direction: prev[area].direction === 'asc' ? 'desc' : 'asc',
      },
    }));
  }, []);

  const getSortState = useCallback((area: AreaType): SortState => {
    return sortState[area];
  }, [sortState]);

  return {
    updateSort,
    toggleDirection,
    getSortState,
    sortState,
  };
};
