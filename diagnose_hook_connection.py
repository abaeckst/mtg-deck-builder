#!/usr/bin/env python3

import os
import sys

def diagnose_hook_connection(filename):
    """Add diagnostics to useSorting.ts to verify hook initialization"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add initialization logging to the main hook function
    old_hook_start = '''export const useSorting = () => {
  const [sortState, setSortState] = useState<AreaSortState>(() => {'''

    new_hook_start = '''export const useSorting = () => {
  console.log('🔴 USESORTING HOOK CALLED - INITIALIZING');
  
  const [sortState, setSortState] = useState<AreaSortState>(() => {'''

    if old_hook_start in content:
        content = content.replace(old_hook_start, new_hook_start)
        print("✅ Added hook initialization logging")
    else:
        print("❌ Could not find hook start to add logging")
        return False

    # Add return value logging
    old_return = '''  return {
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
  };'''

    new_return = '''  console.log('🔴 USESORTING HOOK RETURNING FUNCTIONS:', {
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
  };'''

    if old_return in content:
        content = content.replace(old_return, new_return)
        print("✅ Added return value logging")
    else:
        print("❌ Could not find return statement to add logging")
        return False

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully added diagnostics to {filename}")
    return True

if __name__ == "__main__":
    success = diagnose_hook_connection("src/hooks/useSorting.ts")
    sys.exit(0 if success else 1)
