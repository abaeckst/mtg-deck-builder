#!/usr/bin/env python3

import os
import sys

def fix_sorting_hook_defaults(filename):
    """Fix the useSorting.ts hook to have correct defaults and state updating"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Issue 1: Check and fix DEFAULT_SORT_STATE
    # The console shows 'desc' so something is wrong here
    old_default_state = '''const DEFAULT_SORT_STATE: AreaSortState = {
  collection: { criteria: 'name', direction: 'asc' },
  deck: { criteria: 'mana', direction: 'asc' },
  sideboard: { criteria: 'mana', direction: 'asc' },
};'''

    # Check if it's already correct
    if "direction: 'asc'" in content and "collection: { criteria: 'name', direction: 'asc' }" in content:
        print("✅ DEFAULT_SORT_STATE looks correct - issue must be elsewhere")
    else:
        print("❌ DEFAULT_SORT_STATE may have wrong direction")

    # Issue 2: Add debugging to see what's actually happening with sort state
    # Add debugging right after sort state is set
    old_setstate = '''    setSortState(prev => ({
      ...prev,
      [area]: newSortState,
    }));'''

    new_setstate = '''    setSortState(prev => {
      const updatedState = {
        ...prev,
        [area]: newSortState,
      };
      console.log('🔧 SORT STATE UPDATED:', {
        area,
        oldState: prev[area],
        newState: newSortState,
        fullUpdatedState: updatedState
      });
      return updatedState;
    });'''

    if old_setstate in content:
        content = content.replace(old_setstate, new_setstate)
        print("✅ Added sort state update debugging")
    else:
        print("❌ Could not find setSortState pattern")
        return False

    # Issue 3: Add debugging to getScryfallSortParams to see what it returns
    old_getparams = '''  // Get Scryfall API parameters for server-side sorting
  const getScryfallSortParams = useCallback((area: AreaType) => {
    const state = sortState[area];
    const scryfallOrder = SCRYFALL_SORT_MAPPING[state.criteria];
    
    return {
      order: scryfallOrder,
      dir: state.direction,
    };
  }, [sortState]);'''

    new_getparams = '''  // Get Scryfall API parameters for server-side sorting
  const getScryfallSortParams = useCallback((area: AreaType) => {
    const state = sortState[area];
    const scryfallOrder = SCRYFALL_SORT_MAPPING[state.criteria];
    
    const params = {
      order: scryfallOrder,
      dir: state.direction,
    };
    
    console.log('🔧 GET SCRYFALL SORT PARAMS:', {
      area,
      currentSortState: state,
      returnedParams: params,
      fullSortState: sortState
    });
    
    return params;
  }, [sortState]);'''

    if old_getparams in content:
        content = content.replace(old_getparams, new_getparams)
        print("✅ Added getScryfallSortParams debugging")
    else:
        print("❌ Could not find getScryfallSortParams pattern")
        return False

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully added debugging to {filename}")
    return True

if __name__ == "__main__":
    success = fix_sorting_hook_defaults("src/hooks/useSorting.ts")
    sys.exit(0 if success else 1)
