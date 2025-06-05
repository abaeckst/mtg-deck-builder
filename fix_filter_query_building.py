#!/usr/bin/env python3

import os
import sys

def fix_filter_query_building():
    """Fix the filter query building that's causing 404 errors"""
    
    filename = "src/services/scryfallApi.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # The issue is likely in searchCardsWithFilters where it adds legal:standard
    # Let's look for where the format filter is being added
    old_format_filter = '''  // Add format filter with proper Scryfall syntax
  if (filters.format) {
    if (filters.format === 'custom-standard') {
      // Custom Standard: Use standard format (Final Fantasy set is standard-legal)
      searchQuery += ` legal:standard`;
    } else {
      searchQuery += ` legal:${filters.format}`;
    }
  }'''
    
    new_format_filter = '''  // Add format filter with proper Scryfall syntax
  if (filters.format) {
    if (filters.format === 'custom-standard') {
      // Custom Standard: Use standard format
      searchQuery += ` legal:standard`;
    } else {
      searchQuery += ` legal:${filters.format}`;
    }
  }'''
    
    # More importantly, let's check if the issue is in the base query building
    # Find the searchCardsWithFilters function and see how it builds the query
    
    # First, let's try a simpler fix - bypass the complex filtering for now
    old_enhanced_search = '''export const enhancedSearchCards = async (
  query: string,
  filters: SearchFilters = {},
  page = 1,
  order = 'name',
  dir: 'asc' | 'desc' = 'asc'
): Promise<ScryfallSearchResponse> => {
  // Handle empty queries
  if (!query || query.trim() === '') {
    // If we have filters, use wildcard search
    if (Object.keys(filters).length > 0) {
      return searchCardsWithFilters('*', filters, page, order, dir);
    }
    throw new Error('Search query cannot be empty');
  }
  
  // Build enhanced query for full-text search
  const searchQuery = buildEnhancedSearchQuery(query.trim());
  
  console.log('🔍 Enhanced search query:', { 
    original: query, 
    enhanced: searchQuery,
    filters: Object.keys(filters),
    sort: { order, dir }
  });
  
  // Use existing searchCardsWithFilters with enhanced query and sort
  return searchCardsWithFilters(searchQuery, filters, page, order, dir);
};'''
    
    new_enhanced_search = '''export const enhancedSearchCards = async (
  query: string,
  filters: SearchFilters = {},
  page = 1,
  order = 'name',
  dir: 'asc' | 'desc' = 'asc'
): Promise<ScryfallSearchResponse> => {
  // Handle empty queries
  if (!query || query.trim() === '') {
    // If we have filters, use wildcard search
    if (Object.keys(filters).length > 0) {
      return searchCardsWithFilters('*', filters, page, order, dir);
    }
    throw new Error('Search query cannot be empty');
  }
  
  // For debugging, try simple search first without complex filtering
  if (query.trim() === 'creature') {
    console.log('🔍 Using simple creature search for debugging');
    return searchCards('type:creature', page, 'cards', order, dir);
  }
  
  // Build enhanced query for full-text search
  const searchQuery = buildEnhancedSearchQuery(query.trim());
  
  console.log('🔍 Enhanced search query:', { 
    original: query, 
    enhanced: searchQuery,
    filters: Object.keys(filters),
    sort: { order, dir }
  });
  
  // Use existing searchCardsWithFilters with enhanced query and sort
  return searchCardsWithFilters(searchQuery, filters, page, order, dir);
};'''
    
    if old_enhanced_search in content:
        content = content.replace(old_enhanced_search, new_enhanced_search)
        print("✅ Added debugging bypass for 'creature' search")
    else:
        print("❌ Could not find enhancedSearchCards function")
        return False
    
    # Also fix the searchCardsWithPagination to use simple searchCards for debugging
    old_pagination_search = '''    // Execute paginated search
    const paginationResult = await searchCardsWithPagination(
      query, 
      filters, 
      sortParams.order, 
      sortParams.dir
    );'''
    
    new_pagination_search = '''    // Execute paginated search - use simple search for debugging
    console.log('🔍 About to call searchCardsWithPagination with:', { query, filters, sort: sortParams });
    const paginationResult = await searchCardsWithPagination(
      query, 
      filters, 
      sortParams.order, 
      sortParams.dir
    );'''
    
    # This might be in useCards.ts, let's also create a separate fix for that
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added debugging for search functions")
    return True

def fix_useCards_search():
    """Fix the useCards search to bypass complex filtering"""
    
    filename = "src/hooks/useCards.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the enhancedSearch function call and add debugging
    old_enhanced_search_call = '''  const enhancedSearch = useCallback(async (query: string, filtersOverride?: any) => {
    const filters = filtersOverride || state.activeFilters;
    
    // Handle empty query cases
    if (!query.trim()) {
      if (Object.keys(filters).some(key => {
        const value = filters[key];
        return value && (Array.isArray(value) ? value.length > 0 : 
                        typeof value === 'object' ? Object.values(value).some(v => v !== null) :
                        value !== '');
      })) {
        query = '*';
      } else {
        loadPopularCards();
        return;
      }
    }

    await searchWithPagination(query, filters);
    addToSearchHistory(query);
  }, [state.activeFilters, searchWithPagination, loadPopularCards]);'''
    
    new_enhanced_search_call = '''  const enhancedSearch = useCallback(async (query: string, filtersOverride?: any) => {
    const filters = filtersOverride || state.activeFilters;
    
    console.log('🔍 enhancedSearch called with:', { query, filters, hasFilters: Object.keys(filters).length });
    
    // Handle empty query cases
    if (!query.trim()) {
      if (Object.keys(filters).some(key => {
        const value = filters[key];
        return value && (Array.isArray(value) ? value.length > 0 : 
                        typeof value === 'object' ? Object.values(value).some(v => v !== null) :
                        value !== '');
      })) {
        query = '*';
      } else {
        loadPopularCards();
        return;
      }
    }

    // For debugging: try simple search without filters for 'creature'
    if (query.trim() === 'creature') {
      console.log('🔍 Using simple creature search - bypassing filters');
      await searchWithPagination(query, {});
    } else {
      await searchWithPagination(query, filters);
    }
    addToSearchHistory(query);
  }, [state.activeFilters, searchWithPagination, loadPopularCards]);'''
    
    if old_enhanced_search_call in content:
        content = content.replace(old_enhanced_search_call, new_enhanced_search_call)
        print("✅ Added debugging to enhancedSearch in useCards")
    else:
        print("❌ Could not find enhancedSearch in useCards")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

if __name__ == "__main__":
    print("🔧 Fixing filter query building issues...")
    
    success1 = fix_filter_query_building()
    success2 = fix_useCards_search()
    
    if success1 and success2:
        print("\n✅ DEBUGGING FIXES APPLIED")
        print("\n📋 Test steps:")
        print("1. Refresh browser")
        print("2. Search for 'creature' (this will use simple search)")
        print("3. Check console for detailed debugging info")
        print("4. Look for pagination debug values")
        print("5. Report back what you see in console")
    else:
        print("\n❌ Some fixes failed")
    
    sys.exit(0 if success1 and success2 else 1)