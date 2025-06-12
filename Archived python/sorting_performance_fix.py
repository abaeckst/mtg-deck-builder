#!/usr/bin/env python3
"""
Performance fix for useSorting hook - Eliminates re-render loops
Based on successful useCards extraction methodology
"""

import os

def create_optimized_usesorting():
    """Create performance-optimized useSorting hook"""
    
    content = '''// src/hooks/useSorting.ts - PERFORMANCE OPTIMIZED - Eliminates re-render loops
import { useState, useEffect, useCallback, useMemo, useRef } from 'react';

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

// PERFORMANCE FIX: Stable default state object
const DEFAULT_SORT_STATE: AreaSortState = {
  collection: { criteria: 'name', direction: 'asc' },
  deck: { criteria: 'mana', direction: 'asc' },
  sideboard: { criteria: 'mana', direction: 'asc' },
};

const STORAGE_KEY = 'mtg-deckbuilder-sort-state';

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
    console.log('🎯 useSorting initialized');
    initRef.current = true;
  }
  
  // PERFORMANCE FIX: Stable state initialization
  const [sortState, setSortState] = useState<AreaSortState>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        // Merge with defaults to ensure all areas exist
        return {
          collection: parsed.collection || DEFAULT_SORT_STATE.collection,
          deck: parsed.deck || DEFAULT_SORT_STATE.deck,
          sideboard: parsed.sideboard || DEFAULT_SORT_STATE.sideboard,
        };
      }
      return DEFAULT_SORT_STATE;
    } catch {
      return DEFAULT_SORT_STATE;
    }
  });

  // PERFORMANCE FIX: Debounced localStorage updates to prevent excessive writes
  const persistStateTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  
  const persistState = useCallback((state: AreaSortState) => {
    if (persistStateTimeoutRef.current) {
      clearTimeout(persistStateTimeoutRef.current);
    }
    
    persistStateTimeoutRef.current = setTimeout(() => {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      } catch (error) {
        console.warn('Failed to save sort state:', error);
      }
    }, 100); // Debounce by 100ms
  }, []);

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
      
      // Persist state asynchronously
      persistState(newState);
      
      return newState;
    });
  }, [persistState]); // PERFORMANCE FIX: Stable dependency array

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

  // PERFORMANCE FIX: Cleanup timeout on unmount
  useEffect(() => {
    return () => {
      if (persistStateTimeoutRef.current) {
        clearTimeout(persistStateTimeoutRef.current);
      }
    };
  }, []);

  // PERFORMANCE FIX: Removed complex subscription system that was causing loops
  // PERFORMANCE FIX: Removed global test functions that were causing side effects
  
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
};'''

    return content

def main():
    """Create the performance-optimized useSorting hook"""
    print("🚀 Creating performance-optimized useSorting hook...")
    
    # Create the optimized file
    file_path = "src/hooks/useSorting.ts"
    content = create_optimized_usesorting()
    
    # Write the file
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created optimized {file_path}")
    print()
    print("🎯 PERFORMANCE IMPROVEMENTS:")
    print("• Eliminated re-render loops with stable dependencies")
    print("• Removed complex subscription system causing cascades")
    print("• Added debounced localStorage updates")
    print("• Memoized return object to prevent component re-renders")
    print("• Removed excessive console logging")
    print("• Simplified collection sorting coordination")
    print()
    print("📊 EXPECTED RESULTS:")
    print("• Search times: 2-7+ seconds → <1 second")
    print("• Console logs: Hundreds per search → Minimal logging")
    print("• Hook calls: Multiple per render → Single stable instance")
    print()
    print("🧪 TESTING:")
    print("1. Run npm start")
    print("2. Try previous slow searches: 'fear of missin', 'angel', 'damage'")
    print("3. Check console for eliminated spam")
    print("4. Verify sorting still works in all view modes")

if __name__ == "__main__":
    main()
