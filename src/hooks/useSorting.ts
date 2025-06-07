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
  console.log('🔴 USESORTING HOOK CALLED - INITIALIZING');
  
  const [sortState, setSortState] = useState<AreaSortState>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      const loadedState = saved ? { ...DEFAULT_SORT_STATE, ...JSON.parse(saved) } : DEFAULT_SORT_STATE;
      currentSortState = loadedState;
      
      console.log('🎯 SORTING HOOK INITIALIZED:', {
        defaultState: DEFAULT_SORT_STATE,
        loadedState: loadedState,
        collectionSort: loadedState.collection
      });
      
      return loadedState;
    } catch {
      currentSortState = DEFAULT_SORT_STATE;
      console.log('🎯 SORTING HOOK - Using default state due to error');
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

  // Simplified and reliable updateSort function
  const updateSort = useCallback((area: AreaType, criteria: SortCriteria, direction?: SortDirection) => {
    console.log('🎯 SORT UPDATE:', { area, criteria, direction });
    
    const newSortState = {
      criteria,
      direction: direction ?? sortState[area].direction,
    };

    // Update sort state
    setSortState(prev => ({
      ...prev,
      [area]: newSortState,
    }));

    // Handle collection sorting with simplified logic
    if (area === 'collection') {
      const triggerSearch = (window as any).triggerSearch;
      const metadata = (window as any).lastSearchMetadata;
      
      if (triggerSearch && metadata && metadata.totalCards > 75) {
        console.log('🌐 TRIGGERING SERVER-SIDE SORT:', {
          criteria: newSortState.criteria,
          direction: newSortState.direction,
          totalCards: metadata.totalCards
        });
        
        // Set override parameters for the search
        const scryfallOrder = SCRYFALL_SORT_MAPPING[newSortState.criteria];
        (window as any).overrideSortParams = {
          order: scryfallOrder,
          dir: newSortState.direction,
        };
        
        // Track sort timing
        (window as any).lastSortChangeTime = Date.now();
        
        // Trigger new search with sort parameters
        try {
          triggerSearch(metadata.query, metadata.filters);
          console.log('✅ Server-side sort search triggered');
        } catch (error) {
          console.error('❌ Failed to trigger sort search:', error);
        }
      } else {
        console.log('🏠 Client-side sort will be applied by UI components');
        (window as any).lastSortChangeTime = Date.now();
      }
    }

    // Emit subscription event for any remaining subscribers
    emitSortChange({
      area,
      sortState: newSortState,
      requiresServerSearch: area === 'collection',
    });
  }, [sortState]);

  // Add global test function after updateSort is defined
  useEffect(() => {
    const testUpdateSort = () => {
      console.log('🧪 MANUAL TEST: Calling updateSort directly');
      updateSort('collection', 'name', 'desc');
    };
    
    (window as any).testUpdateSort = testUpdateSort;
    console.log('🧪 Global test function available: window.testUpdateSort()');
    
    return () => {
      delete (window as any).testUpdateSort;
    };
  }, [updateSort]);

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
    
    const params = {
      order: scryfallOrder,
      dir: state.direction,
    };
    
    console.log('🔧 Sort params for', area + ':', params);
    return params;
  }, [sortState]);

  // Check if sorting criteria is supported by Scryfall API
  const isServerSideSupported = useCallback((criteria: SortCriteria): boolean => {
    return criteria in SCRYFALL_SORT_MAPPING;
  }, []);

  // Get current global sort state (useful for subscribers)
  const getGlobalSortState = useCallback((): AreaSortState => {
    return currentSortState;
  }, []);

  console.log('🔴 USESORTING HOOK RETURNING FUNCTIONS:', {
    hasUpdateSort: typeof updateSort,
    hasGetSortState: typeof getSortState,
    currentSortState: sortState
  });

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