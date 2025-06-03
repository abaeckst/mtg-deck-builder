# Fix for React State Closure Issue - Phase 3C
# The searchWithAllFilters function is reading stale state due to closure behavior

import os
import re

def fix_state_closure_issue():
    """Fix the React closure issue by restructuring how filters are passed"""
    
    # Read the current useCards.ts file
    with open('src/hooks/useCards.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the searchWithAllFilters function signature and implementation
    old_search_function = '''  // Enhanced search function that uses all active filters - FIXED v2
  const searchWithAllFilters = useCallback(async (query: string) => {
    const filters = state.activeFilters;
    
    console.log('🚀 searchWithAllFilters called:', { query, filters });'''
    
    new_search_function = '''  // Enhanced search function that uses all active filters - FIXED v3 (State Closure)
  const searchWithAllFilters = useCallback(async (query: string, filtersOverride?: any) => {
    // Use provided filters or current state - this fixes the closure issue
    const filters = filtersOverride || state.activeFilters;
    
    console.log('🚀 searchWithAllFilters called:', { query, filters, usingOverride: !!filtersOverride });'''
    
    content = content.replace(old_search_function, new_search_function)
    
    # Update the actions interface to include the new parameter
    old_search_action = '''  searchWithAllFilters: (query: string) => Promise<void>;'''
    new_search_action = '''  searchWithAllFilters: (query: string, filtersOverride?: any) => Promise<void>;'''
    
    content = content.replace(old_search_action, new_search_action)
    
    # Write the updated file
    with open('src/hooks/useCards.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed React state closure issue in searchWithAllFilters")

def fix_filter_change_handler():
    """Fix the handleFilterChange to pass current filters directly"""
    
    # Read the current MTGOLayout.tsx file
    with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the handleFilterChange function to pass the updated filters
    old_handler = '''  // Handle any filter change by triggering new search - FIXED
  const handleFilterChange = useCallback((filterType: string, value: any) => {
    updateFilter(filterType, value);
    // Trigger search after filter update - use setTimeout to ensure state updates first
    setTimeout(() => {
      console.log('🔧 Filter changed:', filterType, '=', value);
      // Always trigger search when filters change, even with empty search text
      searchWithAllFilters(searchText);
    }, 100);
  }, [updateFilter, searchWithAllFilters, searchText]);'''
    
    new_handler = '''  // Handle any filter change by triggering new search - FIXED v2 (State Closure)
  const handleFilterChange = useCallback((filterType: string, value: any) => {
    console.log('🔧 Filter changing:', filterType, '=', value);
    
    // Build the new filter state manually to avoid closure issues
    const newFilters = {
      ...activeFilters,
      [filterType]: value,
    };
    
    console.log('🔧 New filters will be:', newFilters);
    
    // Update the filter state
    updateFilter(filterType, value);
    
    // Trigger search immediately with the new filters (don't wait for state update)
    setTimeout(() => {
      console.log('🔧 Triggering search with new filters');
      searchWithAllFilters(searchText, newFilters);
    }, 50);
  }, [updateFilter, searchWithAllFilters, searchText, activeFilters]);'''
    
    content = content.replace(old_handler, new_handler)
    
    # Write the updated file
    with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed handleFilterChange to pass current filters directly")

def add_comprehensive_logging():
    """Add comprehensive logging to debug the state flow"""
    
    # Read the current useCards.ts file
    with open('src/hooks/useCards.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add logging to the filter building section
    old_filter_building = '''    // Build comprehensive filter object - FIXED to properly check filter values
    const searchFilters: any = {};
    
    if (filters.format && filters.format !== '') {
      searchFilters.format = filters.format;
      console.log('✅ Adding format filter:', filters.format);
    }'''
    
    new_filter_building = '''    // Build comprehensive filter object - FIXED to properly check filter values
    const searchFilters: any = {};
    
    console.log('🔍 Raw filters received:', filters);
    console.log('🔍 Checking format:', filters.format, 'isEmpty?', !filters.format || filters.format === '');
    
    if (filters.format && filters.format !== '') {
      searchFilters.format = filters.format;
      console.log('✅ Adding format filter:', filters.format);
    } else {
      console.log('❌ Skipping format filter - empty or undefined');
    }'''
    
    content = content.replace(old_filter_building, new_filter_building)
    
    # Add similar logging for colors
    old_color_check = '''    if (filters.colors && filters.colors.length > 0) {
      searchFilters.colors = filters.colors;
      searchFilters.colorIdentity = filters.colorIdentity;
      console.log('✅ Adding color filter:', filters.colors, filters.colorIdentity);
    }'''
    
    new_color_check = '''    console.log('🔍 Checking colors:', filters.colors, 'length:', filters.colors ? filters.colors.length : 'undefined');
    if (filters.colors && filters.colors.length > 0) {
      searchFilters.colors = filters.colors;
      searchFilters.colorIdentity = filters.colorIdentity;
      console.log('✅ Adding color filter:', filters.colors, filters.colorIdentity);
    } else {
      console.log('❌ Skipping color filter - empty or undefined');
    }'''
    
    content = content.replace(old_color_check, new_color_check)
    
    # Write the updated file
    with open('src/hooks/useCards.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added comprehensive logging for filter state debugging")

def main():
    """Execute all fixes for React state closure issues"""
    try:
        print("🔧 Fixing Phase 3C React State Closure Issues")
        print("=" * 55)
        
        print("\n📋 Fix 1: Fixing React state closure in searchWithAllFilters...")
        fix_state_closure_issue()
        
        print("\n📋 Fix 2: Fixing handleFilterChange to pass current filters...")
        fix_filter_change_handler()
        
        print("\n📋 Fix 3: Adding comprehensive logging...")
        add_comprehensive_logging()
        
        print("\n" + "=" * 55)
        print("✅ React State Closure Fixes Complete!")
        print("\n🧪 Test Again:")
        print("   1. Run 'npm start'")
        print("   2. Select 'Standard' format")
        print("   3. You should see:")
        print("      • '🔧 Filter changing: format = standard'")
        print("      • '🔧 New filters will be: {format: \"standard\", ...}'")
        print("      • '🔍 Raw filters received: {format: \"standard\", ...}'")
        print("      • '✅ Adding format filter: standard'")
        print("      • '🌐 API Request: ...legal%3Astandard'")
        print("      • Actual filtered results")
        print("\n🔍 Key Changes:")
        print("   • searchWithAllFilters now accepts filter override parameter")
        print("   • handleFilterChange passes new filters directly")
        print("   • Comprehensive logging shows exact state flow")
        print("   • No more 'No query and no filters' fallback")
        
        print("\n💡 The issue was React closure capturing old state!")
        
    except Exception as e:
        print(f"\n❌ Error during fixes: {e}")
        print("Please check the file paths and try again.")

if __name__ == "__main__":
    main()
