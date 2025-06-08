#!/usr/bin/env python3

import os
import sys

def fix_clearCards_exact(filename):
    """Fix missing sortChangeId in clearCards setState call - exact pattern from provided file"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Exact pattern from the provided useCards.ts file
    old_setState = """    setState({
      cards: [],
      loading: false,
      error: null,
      hasMore: false,
      selectedCards: new Set(),
      searchQuery: '',
      totalCards: 0,
      searchSuggestions: [],
      showSuggestions: false,
      recentSearches: [],
      pagination: {
        totalCards: 0,
        loadedCards: 0,
        hasMore: false,
        isLoadingMore: false,
        currentPage: 1,
      },
      lastSearchMetadata: null,
      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'subset',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
        // Phase 4B: Enhanced filter reset
        subtypes: [],
        isGoldMode: false,
        sectionStates: {
          colors: true,
          cmc: true,
          types: true,
          subtypes: false,
          sets: false,
          rarity: false,
          stats: false,
        },
      },
      isFiltersCollapsed: false,
    });"""

    new_setState = """    setState({
      cards: [],
      loading: false,
      error: null,
      hasMore: false,
      selectedCards: new Set(),
      searchQuery: '',
      totalCards: 0,
      searchSuggestions: [],
      showSuggestions: false,
      recentSearches: [],
      pagination: {
        totalCards: 0,
        loadedCards: 0,
        hasMore: false,
        isLoadingMore: false,
        currentPage: 1,
      },
      lastSearchMetadata: null,
      sortChangeId: 0, // Add missing sortChangeId property
      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'subset',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
        // Phase 4B: Enhanced filter reset
        subtypes: [],
        isGoldMode: false,
        sectionStates: {
          colors: true,
          cmc: true,
          types: true,
          subtypes: false,
          sets: false,
          rarity: false,
          stats: false,
        },
      },
      isFiltersCollapsed: false,
    });"""
    
    if old_setState in content:
        content = content.replace(old_setState, new_setState)
        print("✅ Added missing sortChangeId to clearCards setState")
    else:
        print("❌ Could not find exact clearCards setState pattern")
        # Debug: show what we're looking for vs what might be there
        if "clearCards = useCallback" in content:
            print("ℹ️  Found clearCards function but setState pattern doesn't match exactly")
            print("ℹ️  This might be due to formatting differences")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed {filename}")
    return True

if __name__ == "__main__":
    success = fix_clearCards_exact("src/hooks/useCards.ts")
    sys.exit(0 if success else 1)