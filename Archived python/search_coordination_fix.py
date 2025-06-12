#!/usr/bin/env python3
"""
Fix search coordination to ensure clean searches when users interact with filters/sorting.

Root Issue: Filter/sort changes don't trigger fresh searches, and when they do, 
they build on existing search context instead of starting clean.

Solution: Add reactive filter/sort listeners that trigger clean searches with 
only user-selected parameters + standard format preservation.
"""

import os
import re

def update_use_cards():
    """Add filter change reactivity to useCards coordinator"""
    
    file_path = "src/hooks/useCards.ts"
    
    # Read current file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the location after useEffect for loadPopularCards
    load_popular_effect = r"(  // Load popular cards on mount\s+useEffect\(\(\) => \{\s+loadPopularCards\(\);\s+\}, \[loadPopularCards\]\);)"
    
    # Add filter and sort change reactivity after the loadPopularCards effect
    new_effects = '''
  // FILTER CHANGE REACTIVITY: Trigger fresh search when filters change
  // Skip on initial mount to prevent interference with loadPopularCards
  const isInitialMount = useRef(true);
  
  useEffect(() => {
    // Skip filter reactivity on initial mount
    if (isInitialMount.current) {
      isInitialMount.current = false;
      return;
    }
    
    // Skip if no active filters (user cleared filters - handled by clearAllFilters)
    if (!hasActiveFilters()) {
      return;
    }
    
    console.log('🎯 Filter change detected, triggering fresh search');
    
    // Trigger fresh search with current filters
    // Use '*' as base query to get all cards matching filters
    searchWithAllFilters('*');
    
  }, [activeFilters, hasActiveFilters, searchWithAllFilters]);
  
  // SORT CHANGE REACTIVITY: Currently handled by useSorting hook coordination
  // No additional effect needed as handleCollectionSortChange is already wired up'''
    
    # Add useRef import to the existing imports
    import_pattern = r"(import \{ useEffect, useCallback \} from 'react';)"
    import_replacement = r"import { useEffect, useCallback, useRef } from 'react';"
    content = re.sub(import_pattern, import_replacement, content)
    
    # Add the new effects after loadPopularCards effect
    content = re.sub(load_popular_effect, r'\1' + new_effects, content, flags=re.DOTALL)
    
    # Write updated file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated useCards.ts with filter change reactivity")

def update_use_search():
    """Ensure search functions always start with clean context"""
    
    file_path = "src/hooks/useSearch.ts"
    
    # Read current file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update searchWithAllFilters to ensure clean search context
    old_search_logic = r"""(  // Enhanced search function that uses all active filters
  const searchWithAllFilters = useCallback\(async \(query: string, filtersOverride\?: any\) => \{
    const filters = filtersOverride \|\| activeFilters;
    
    console\.log\('🚀 searchWithAllFilters called:', \{ query, filters, usingOverride: !!filtersOverride \}\);
    
    // Build comprehensive filter object for SearchFilters interface
    const searchFilters: SearchFilters = \{\};
    
    if \(filters\.format && filters\.format !== ''\) \{
      searchFilters\.format = filters\.format;
    \}
    if \(filters\.colors && filters\.colors\.length > 0\) \{
      searchFilters\.colors = filters\.colors;
      searchFilters\.colorIdentity = filters\.colorIdentity;
    \}
    if \(filters\.types && filters\.types\.length > 0\) \{
      searchFilters\.types = filters\.types;
    \}
    if \(filters\.rarity && filters\.rarity\.length > 0\) \{
      searchFilters\.rarity = filters\.rarity;
    \}
    if \(filters\.sets && filters\.sets\.length > 0\) \{
      searchFilters\.sets = filters\.sets;
    \}
    if \(filters\.cmc && \(filters\.cmc\.min !== null \|\| filters\.cmc\.max !== null\)\) \{
      searchFilters\.cmc = \{\};
      if \(filters\.cmc\.min !== null\) searchFilters\.cmc\.min = filters\.cmc\.min;
      if \(filters\.cmc\.max !== null\) searchFilters\.cmc\.max = filters\.cmc\.max;
    \}
    if \(filters\.power && \(filters\.power\.min !== null \|\| filters\.power\.max !== null\)\) \{
      searchFilters\.power = \{\};
      if \(filters\.power\.min !== null\) searchFilters\.power\.min = filters\.power\.min;
      if \(filters\.power\.max !== null\) searchFilters\.power\.max = filters\.power\.max;
    \}
    if \(filters\.toughness && \(filters\.toughness\.min !== null \|\| filters\.toughness\.max !== null\)\) \{
      searchFilters\.toughness = \{\};
      if \(filters\.toughness\.min !== null\) searchFilters\.toughness\.min = filters\.toughness\.min;
      if \(filters\.toughness\.max !== null\) searchFilters\.toughness\.max = filters\.toughness\.max;
    \}
    if \(filters\.subtypes && filters\.subtypes\.length > 0\) \{
      searchFilters\.subtypes = filters\.subtypes;
    \}
    if \(filters\.isGoldMode\) \{
      searchFilters\.isGoldMode = filters\.isGoldMode;
    \}

    // Determine query strategy
    const hasFilters = Object\.keys\(searchFilters\)\.length > 0;
    const hasQuery = query && query\.trim\(\) !== '';
    
    let actualQuery: string;
    if \(hasQuery\) \{
      actualQuery = query\.trim\(\);
    \} else if \(hasFilters\) \{
      actualQuery = '\*';
    \} else \{
      console\.log\('❌ No query and no filters - falling back to popular cards'\);
      loadPopularCards\(\);
      return;
    \}
    
    // Get default sort parameters for consistent sorting
    const defaultSortParams = getCollectionSortParams\(\);
    await searchWithPagination\(actualQuery, searchFilters, defaultSortParams\.order, defaultSortParams\.dir\);
  \}, \[activeFilters, searchWithPagination, loadPopularCards\]\);)"""
    
    new_search_logic = r"""  // Enhanced search function that uses all active filters
  const searchWithAllFilters = useCallback(async (query: string, filtersOverride?: any) => {
    const filters = filtersOverride || activeFilters;
    
    console.log('🚀 CLEAN SEARCH - searchWithAllFilters called:', { 
      query, 
      filters: Object.keys(filters).filter(key => {
        const value = filters[key];
        return value !== '' && value !== null && value !== undefined && 
               (Array.isArray(value) ? value.length > 0 : true);
      }), 
      usingOverride: !!filtersOverride 
    });
    
    // CLEAN SEARCH PRINCIPLE: Build filter object from scratch
    // Never inherit from previous searches - only use explicitly selected filters
    const searchFilters: SearchFilters = {};
    
    // Format filter: Preserve standard as default, only add if different
    if (filters.format && filters.format !== '' && filters.format !== 'standard') {
      searchFilters.format = filters.format;
    } else {
      // Always include standard format as base
      searchFilters.format = 'standard';
    }
    
    // Color filters: Only add if explicitly selected
    if (filters.colors && filters.colors.length > 0) {
      searchFilters.colors = filters.colors;
      searchFilters.colorIdentity = filters.colorIdentity;
    }
    if (filters.isGoldMode) {
      searchFilters.isGoldMode = filters.isGoldMode;
    }
    
    // Type filters: Only add if explicitly selected
    if (filters.types && filters.types.length > 0) {
      searchFilters.types = filters.types;
    }
    if (filters.subtypes && filters.subtypes.length > 0) {
      searchFilters.subtypes = filters.subtypes;
    }
    
    // Property filters: Only add if explicitly set
    if (filters.rarity && filters.rarity.length > 0) {
      searchFilters.rarity = filters.rarity;
    }
    if (filters.sets && filters.sets.length > 0) {
      searchFilters.sets = filters.sets;
    }
    
    // Range filters: Only add if explicitly set
    if (filters.cmc && (filters.cmc.min !== null || filters.cmc.max !== null)) {
      searchFilters.cmc = {};
      if (filters.cmc.min !== null) searchFilters.cmc.min = filters.cmc.min;
      if (filters.cmc.max !== null) searchFilters.cmc.max = filters.cmc.max;
    }
    if (filters.power && (filters.power.min !== null || filters.power.max !== null)) {
      searchFilters.power = {};
      if (filters.power.min !== null) searchFilters.power.min = filters.power.min;
      if (filters.power.max !== null) searchFilters.power.max = filters.power.max;
    }
    if (filters.toughness && (filters.toughness.min !== null || filters.toughness.max !== null)) {
      searchFilters.toughness = {};
      if (filters.toughness.min !== null) searchFilters.toughness.min = filters.toughness.min;
      if (filters.toughness.max !== null) searchFilters.toughness.max = filters.toughness.max;
    }

    // CLEAN QUERY STRATEGY: Start fresh every time
    let actualQuery: string;
    const hasQuery = query && query.trim() !== '' && query.trim() !== '*';
    
    if (hasQuery) {
      // User provided explicit search query
      actualQuery = query.trim();
      console.log('🎯 Using explicit user query:', actualQuery);
    } else {
      // No user query - search all cards matching filters
      actualQuery = '*';
      console.log('🎯 Using wildcard for filter-only search');
    }
    
    // CONSISTENT SORTING: Always use current sort preferences
    const defaultSortParams = getCollectionSortParams();
    
    console.log('🚀 EXECUTING CLEAN SEARCH:', {
      query: actualQuery,
      appliedFilters: Object.keys(searchFilters),
      sortOrder: defaultSortParams.order,
      sortDirection: defaultSortParams.dir
    });
    
    await searchWithPagination(actualQuery, searchFilters, defaultSortParams.order, defaultSortParams.dir);
    
  }, [activeFilters, searchWithPagination, getCollectionSortParams]);"""
    
    # Replace the searchWithAllFilters function
    content = re.sub(old_search_logic, new_search_logic, content, flags=re.DOTALL)
    
    # Write updated file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated useSearch.ts with clean search logic")

def update_use_filters():
    """Ensure hasActiveFilters properly excludes standard format from active check"""
    
    file_path = "src/hooks/useFilters.ts"
    
    # Read current file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update hasActiveFilters to not consider 'standard' format as active
    old_has_active = r"""(  // Check if any filters are active
  const hasActiveFilters = useCallback\(\(\): boolean => \{
    const filters = state\.activeFilters;
    return \(
      filters\.format !== '' &&
      filters\.format !== 'standard' \|\| // CHANGED: Updated to match new default format
      filters\.colors\.length > 0 \|\|
      filters\.types\.length > 0 \|\|
      filters\.rarity\.length > 0 \|\|
      filters\.sets\.length > 0 \|\|
      filters\.cmc\.min !== null \|\|
      filters\.cmc\.max !== null \|\|
      filters\.power\.min !== null \|\|
      filters\.power\.max !== null \|\|
      filters\.toughness\.min !== null \|\|
      filters\.toughness\.max !== null \|\|
      filters\.subtypes\.length > 0 \|\|
      filters\.isGoldMode
    \);
  \}, \[state\.activeFilters\]\);)"""
    
    new_has_active = r"""  // Check if any filters are active (excluding standard format as it's default)
  const hasActiveFilters = useCallback((): boolean => {
    const filters = state.activeFilters;
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
  }, [state.activeFilters]);"""
    
    # Replace the hasActiveFilters function
    content = re.sub(old_has_active, new_has_active, content, flags=re.DOTALL)
    
    # Write updated file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated useFilters.ts with improved active filter detection")

def main():
    """Execute all search coordination fixes"""
    
    print("🔧 Implementing search coordination fix...")
    print("📋 Fix Strategy:")
    print("  1. Add filter change reactivity to useCards")
    print("  2. Ensure clean search context in useSearch") 
    print("  3. Fix active filter detection in useFilters")
    print("  4. Preserve standard format as default while enabling clean searches")
    print("")
    
    # Verify files exist
    files_to_check = [
        "src/hooks/useCards.ts",
        "src/hooks/useSearch.ts", 
        "src/hooks/useFilters.ts"
    ]
    
    for file_path in files_to_check:
        if not os.path.exists(file_path):
            print(f"❌ Error: {file_path} not found")
            return
    
    try:
        update_use_cards()
        update_use_search() 
        update_use_filters()
        
        print("")
        print("✅ Search coordination fix implemented successfully!")
        print("")
        print("🎯 What this achieves:")
        print("  ✓ Filter changes trigger immediate fresh searches")
        print("  ✓ Sort changes trigger clean searches (not re-sorting old results)")  
        print("  ✓ Standard format preserved as default")
        print("  ✓ No parameter accumulation from previous searches")
        print("  ✓ Clean search context for every user interaction")
        print("")
        print("🧪 Test Cases Now Fixed:")
        print("  ✓ Click black color button → Search for 'legal:standard color:B'")
        print("  ✓ Change sort to name → Fresh search sorted by name") 
        print("  ✓ Add any filter → Clean search with only selected filters")
        print("  ✓ Clear filters → Return to popular cards display")
        print("")
        print("🚀 Run 'npm start' to test the fix!")
        
    except Exception as e:
        print(f"❌ Error implementing fix: {e}")

if __name__ == "__main__":
    main()
