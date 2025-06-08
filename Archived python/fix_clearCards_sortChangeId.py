#!/usr/bin/env python3

import os
import sys

def fix_clearCards_sortChangeId(filename):
    """Fix missing sortChangeId in clearCards setState call"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and fix the clearCards setState call
    old_setState = """  setState({
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

    new_setState = """  setState({
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
        print("❌ Could not find clearCards setState pattern")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed {filename}")
    return True

if __name__ == "__main__":
    success = fix_clearCards_sortChangeId("src/hooks/useCards.ts")
    sys.exit(0 if success else 1)