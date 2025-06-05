// src/hooks/useSorting.ts - Enhanced with server-side integration and subscription system
import { useState, useEffect, useCallback } from 'react';

// Removed 'type' as it doesn't map well to Scryfall API
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

// Subscription system for cross-component communication
interface SortSubscriber {
  id: string;
  callback: (area: AreaType, sortState: SortState) => void;
}

interface SortChangeEvent {
  area: AreaType;
  sortState: SortState;
  requiresServerSearch: boolean;
}

const DEFAULT_SORT_STATE: AreaSortState = {
  collection: { criteria: 'name', direction: 'asc' },
  deck: { criteria: 'mana', direction: 'asc' },
  sideboard: { criteria: 'mana', direction: 'asc' },
};

const STORAGE_KEY = 'mtg-deckbuilder-sort-state';

// Scryfall API mapping for server-side sorting
const SCRYFALL_SORT_MAPPING: Record<SortCriteria, string> = {
  mana: 'cmc',
  color: 'color',
  rarity: 'rarity',
  name: 'name',
  type: 'type', // Note: Scryfall doesn't support type sorting well, will fall back to name
};

// Global subscription system
let subscribers: SortSubscriber[] = [];
let currentSortState: AreaSortState = DEFAULT_SORT_STATE;

// Event emitter for sort changes
const emitSortChange = (event: SortChangeEvent) => {
  subscribers.forEach(subscriber => {
    try {
      subscriber.callback(event.area, event.sortState);
    } catch (error) {
      console.error('Error in sort subscriber callback:', error);
    }
  });
};

export const useSorting = () => {
  const [sortState, setSortState] = useState<AreaSortState>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      const loadedState = saved ? { ...DEFAULT_SORT_STATE, ...JSON.parse(saved) } : DEFAULT_SORT_STATE;
      currentSortState = loadedState;
      return loadedState;
    } catch {
      currentSortState = DEFAULT_SORT_STATE;
      return DEFAULT_SORT_STATE;
    }
  });

  // Persist to localStorage whenever sort state changes
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(sortState));
      currentSortState = sortState;
    } catch (error) {
      console.warn('Failed to save sort state to localStorage:', error);
    }
  }, [sortState]);

  // Subscribe to sort changes from other hook instances
  const subscribe = useCallback((callback: (area: AreaType, sortState: SortState) => void): string => {
    const subscriberId = `sort_subscriber_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    subscribers.push({
      id: subscriberId,
      callback,
    });
    console.log('🔔 Sort subscriber added:', subscriberId);
    return subscriberId;
  }, []);

  // Unsubscribe from sort changes
  const unsubscribe = useCallback((subscriberId: string) => {
    const index = subscribers.findIndex(sub => sub.id === subscriberId);
    if (index !== -1) {
      subscribers.splice(index, 1);
      console.log('🔕 Sort subscriber removed:', subscriberId);
    }
  }, []);

  // Enhanced update sort with subscription notification
  const updateSort = useCallback((area: AreaType, criteria: SortCriteria, direction?: SortDirection) => {
    const newSortState = {
      criteria,
      direction: direction ?? sortState[area].direction,
    };

    setSortState(prev => ({
      ...prev,
      [area]: newSortState,
    }));

    // Determine if this change requires server-side re-search
    const requiresServerSearch = area === 'collection';

    // Emit sort change event to subscribers
    const event: SortChangeEvent = {
      area,
      sortState: newSortState,
      requiresServerSearch,
    };

    console.log('📢 Sort change event:', event);
    emitSortChange(event);
  }, [sortState]);

  const toggleDirection = useCallback((area: AreaType) => {
    const currentState = sortState[area];
    const newDirection = currentState.direction === 'asc' ? 'desc' : 'asc';
    updateSort(area, currentState.criteria, newDirection);
  }, [sortState, updateSort]);

  const getSortState = useCallback((area: AreaType): SortState => {
    return sortState[area];
  }, [sortState]);

  // Get Scryfall API parameters for server-side sorting
  const getScryfallSortParams = useCallback((area: AreaType) => {
    const state = sortState[area];
    const scryfallOrder = SCRYFALL_SORT_MAPPING[state.criteria];
    
    return {
      order: scryfallOrder,
      dir: state.direction,
    };
  }, [sortState]);

  // Check if sorting criteria is supported by Scryfall API
  const isServerSideSupported = useCallback((criteria: SortCriteria): boolean => {
    return criteria in SCRYFALL_SORT_MAPPING;
  }, []);

  // Get current global sort state (useful for subscribers)
  const getGlobalSortState = useCallback((): AreaSortState => {
    return currentSortState;
  }, []);

  return {
    // Original API
    updateSort,
    toggleDirection,
    getSortState,
    sortState,
    
    // Enhanced API for server-side integration
    subscribe,
    unsubscribe,
    getScryfallSortParams,
    isServerSideSupported,
    getGlobalSortState,
    
    // Utilities
    availableCriteria: ['name', 'mana', 'color', 'rarity'] as SortCriteria[],
    scryfallMapping: SCRYFALL_SORT_MAPPING,
  };
};