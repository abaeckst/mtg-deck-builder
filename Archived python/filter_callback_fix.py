# Fix for Phase 3C Filter Callbacks
# The filters are updating state but not triggering searches

import os
import re

def fix_filter_callback():
    """Fix the handleFilterChange function to actually trigger searches"""
    
    # Read the current MTGOLayout.tsx file
    with open('src/components/MTGOLayout.tsx', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the handleFilterChange function
    old_handler = '''  // Handle any filter change by triggering new search
  const handleFilterChange = useCallback((filterType: string, value: any) => {
    updateFilter(filterType, value);
    // Trigger search after filter update
    setTimeout(() => {
      if (searchText.trim() || hasActiveFilters()) {
        searchWithAllFilters(searchText);
      }
    }, 50);
  }, [updateFilter, searchWithAllFilters, searchText, hasActiveFilters]);'''
    
    new_handler = '''  // Handle any filter change by triggering new search - FIXED
  const handleFilterChange = useCallback((filterType: string, value: any) => {
    updateFilter(filterType, value);
    // Trigger search after filter update - use setTimeout to ensure state updates first
    setTimeout(() => {
      console.log('🔧 Filter changed:', filterType, '=', value);
      // Always trigger search when filters change, even with empty search text
      searchWithAllFilters(searchText);
    }, 100);
  }, [updateFilter, searchWithAllFilters, searchText]);'''
    
    content = content.replace(old_handler, new_handler)
    
    # Also need to fix the search handler to work better with filters
    old_search_handler = '''  // Enhanced search handling with comprehensive filters
  const handleSearch = useCallback((text: string) => {
    setSearchText(text);
    if (text.trim() || hasActiveFilters()) {
      searchWithAllFilters(text);
    } else {
      loadPopularCards();
    }
  }, [searchWithAllFilters, loadPopularCards, hasActiveFilters]);'''
    
    new_search_handler = '''  // Enhanced search handling with comprehensive filters - FIXED
  const handleSearch = useCallback((text: string) => {
    setSearchText(text);
    console.log('🔍 Search triggered:', { text, hasFilters: hasActiveFilters() });
    // Always search when there's text OR filters are active
    if (text.trim()) {
      searchWithAllFilters(text);
    } else if (hasActiveFilters()) {
      searchWithAllFilters('');
    } else {
      loadPopularCards();
    }
  }, [searchWithAllFilters, loadPopularCards, hasActiveFilters]);'''
    
    content = content.replace(old_search_handler, new_search_handler)
    
    # Write the updated file
    with open('src/components/MTGOLayout.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed handleFilterChange to actually trigger searches")

def fix_search_with_all_filters():
    """Fix the searchWithAllFilters function to handle empty queries better"""
    
    # Read the current useCards.ts file
    with open('src/hooks/useCards.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the searchWithAllFilters function and improve its query handling
    old_function_start = '''  // Enhanced search function that uses all active filters
  const searchWithAllFilters = useCallback(async (query: string) => {
    const filters = state.activeFilters;
    
    // Build comprehensive filter object
    const searchFilters: any = {};'''
    
    new_function_start = '''  // Enhanced search function that uses all active filters - FIXED
  const searchWithAllFilters = useCallback(async (query: string) => {
    const filters = state.activeFilters;
    
    console.log('🚀 searchWithAllFilters called:', { query, filters });
    
    // Build comprehensive filter object
    const searchFilters: any = {};'''
    
    content = content.replace(old_function_start, new_function_start)
    
    # Find the query handling part and improve it
    old_query_handling = '''    // Use the same race-condition-safe logic as searchForCards
    const searchId = Date.now() + Math.random();
    (window as any).currentSearchId = searchId;

    console.log('🔍 ENHANCED SEARCH:', { 
      searchId: searchId.toFixed(3), 
      query, 
      filters: searchFilters 
    });'''
    
    new_query_handling = '''    // Use the same race-condition-safe logic as searchForCards
    const searchId = Date.now() + Math.random();
    (window as any).currentSearchId = searchId;

    // If no query provided but we have filters, use a wildcard
    const actualQuery = query || (Object.keys(searchFilters).length > 0 ? '*' : '');
    
    console.log('🔍 ENHANCED SEARCH:', { 
      searchId: searchId.toFixed(3), 
      originalQuery: query,
      actualQuery: actualQuery,
      filters: searchFilters,
      filterCount: Object.keys(searchFilters).length
    });'''
    
    content = content.replace(old_query_handling, new_query_handling)
    
    # Fix the API call to use actualQuery
    old_api_call = '''      const response = await searchCardsWithFilters(query || '*', searchFilters);'''
    new_api_call = '''      const response = await searchCardsWithFilters(actualQuery, searchFilters);'''
    
    content = content.replace(old_api_call, new_api_call)
    
    # Write the updated file
    with open('src/hooks/useCards.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed searchWithAllFilters query handling")

def add_debug_logging():
    """Add some debug logging to help troubleshoot"""
    
    # Read the current useCards.ts file
    with open('src/hooks/useCards.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add debug logging to updateFilter function
    old_update_filter = '''  const updateFilter = useCallback((filterType: string, value: any) => {
    setState(prev => ({
      ...prev,
      activeFilters: {
        ...prev.activeFilters,
        [filterType]: value,
      },
    }));
  }, []);'''
    
    new_update_filter = '''  const updateFilter = useCallback((filterType: string, value: any) => {
    console.log('🎛️ Updating filter:', filterType, '=', value);
    setState(prev => {
      const newFilters = {
        ...prev.activeFilters,
        [filterType]: value,
      };
      console.log('🎛️ New filter state:', newFilters);
      return {
        ...prev,
        activeFilters: newFilters,
      };
    });
  }, []);'''
    
    content = content.replace(old_update_filter, new_update_filter)
    
    # Write the updated file
    with open('src/hooks/useCards.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added debug logging to filter updates")

def main():
    """Execute all fixes for filter callback issues"""
    try:
        print("🔧 Fixing Phase 3C Filter Callback Issues")
        print("=" * 50)
        
        print("\n📋 Fix 1: Making handleFilterChange actually trigger searches...")
        fix_filter_callback()
        
        print("\n📋 Fix 2: Improving searchWithAllFilters query handling...")
        fix_search_with_all_filters()
        
        print("\n📋 Fix 3: Adding debug logging...")
        add_debug_logging()
        
        print("\n" + "=" * 50)
        print("✅ Filter Callback Fixes Complete!")
        print("\n🧪 Test Again:")
        print("   1. Run 'npm start'")
        print("   2. Click 'R' (Red) button")
        print("   3. Check console for '🎛️ Updating filter' and '🔍 ENHANCED SEARCH' logs")
        print("   4. Results should change to show red cards")
        print("\n🔍 You should now see:")
        print("   • Filter update logs when clicking buttons")
        print("   • Enhanced search logs when filters trigger")
        print("   • Actual card results changing")
        
        print("\n💡 If still not working, the issue is likely in the API query building")
        
    except Exception as e:
        print(f"\n❌ Error during fixes: {e}")
        print("Please check the file paths and try again.")

if __name__ == "__main__":
    main()
