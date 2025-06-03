# Fix for API Query Building - Phase 3C
# The filters are updating but not being applied to the API query

import os
import re

def fix_search_with_all_filters():
    """Fix the searchWithAllFilters function to properly build filter objects"""
    
    # Read the current useCards.ts file
    with open('src/hooks/useCards.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the entire searchWithAllFilters function with a working version
    old_function_start = '''  // Enhanced search function that uses all active filters - FIXED
  const searchWithAllFilters = useCallback(async (query: string) => {
    const filters = state.activeFilters;
    
    console.log('🚀 searchWithAllFilters called:', { query, filters });
    
    // Build comprehensive filter object
    const searchFilters: any = {};
    
    if (filters.format) searchFilters.format = filters.format;
    if (filters.colors.length > 0) {
      searchFilters.colors = filters.colors;
      searchFilters.colorIdentity = filters.colorIdentity;
    }
    if (filters.types.length > 0) searchFilters.types = filters.types;
    if (filters.rarity.length > 0) searchFilters.rarity = filters.rarity;
    if (filters.sets.length > 0) searchFilters.sets = filters.sets;
    if (filters.cmc.min !== null || filters.cmc.max !== null) {
      searchFilters.cmc = {};
      if (filters.cmc.min !== null) searchFilters.cmc.min = filters.cmc.min;
      if (filters.cmc.max !== null) searchFilters.cmc.max = filters.cmc.max;
    }
    if (filters.power.min !== null || filters.power.max !== null) {
      searchFilters.power = {};
      if (filters.power.min !== null) searchFilters.power.min = filters.power.min;
      if (filters.power.max !== null) searchFilters.power.max = filters.power.max;
    }
    if (filters.toughness.min !== null || filters.toughness.max !== null) {
      searchFilters.toughness = {};
      if (filters.toughness.min !== null) searchFilters.toughness.min = filters.toughness.min;
      if (filters.toughness.max !== null) searchFilters.toughness.max = filters.toughness.max;
    }

    // Use the same race-condition-safe logic as searchForCards
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
    
    new_function_start = '''  // Enhanced search function that uses all active filters - FIXED v2
  const searchWithAllFilters = useCallback(async (query: string) => {
    const filters = state.activeFilters;
    
    console.log('🚀 searchWithAllFilters called:', { query, filters });
    
    // Build comprehensive filter object - FIXED to properly check filter values
    const searchFilters: any = {};
    
    if (filters.format && filters.format !== '') {
      searchFilters.format = filters.format;
      console.log('✅ Adding format filter:', filters.format);
    }
    if (filters.colors && filters.colors.length > 0) {
      searchFilters.colors = filters.colors;
      searchFilters.colorIdentity = filters.colorIdentity;
      console.log('✅ Adding color filter:', filters.colors, filters.colorIdentity);
    }
    if (filters.types && filters.types.length > 0) {
      searchFilters.types = filters.types;
      console.log('✅ Adding type filter:', filters.types);
    }
    if (filters.rarity && filters.rarity.length > 0) {
      searchFilters.rarity = filters.rarity;
      console.log('✅ Adding rarity filter:', filters.rarity);
    }
    if (filters.sets && filters.sets.length > 0) {
      searchFilters.sets = filters.sets;
      console.log('✅ Adding sets filter:', filters.sets);
    }
    if (filters.cmc && (filters.cmc.min !== null || filters.cmc.max !== null)) {
      searchFilters.cmc = {};
      if (filters.cmc.min !== null) searchFilters.cmc.min = filters.cmc.min;
      if (filters.cmc.max !== null) searchFilters.cmc.max = filters.cmc.max;
      console.log('✅ Adding CMC filter:', searchFilters.cmc);
    }
    if (filters.power && (filters.power.min !== null || filters.power.max !== null)) {
      searchFilters.power = {};
      if (filters.power.min !== null) searchFilters.power.min = filters.power.min;
      if (filters.power.max !== null) searchFilters.power.max = filters.power.max;
      console.log('✅ Adding power filter:', searchFilters.power);
    }
    if (filters.toughness && (filters.toughness.min !== null || filters.toughness.max !== null)) {
      searchFilters.toughness = {};
      if (filters.toughness.min !== null) searchFilters.toughness.min = filters.toughness.min;
      if (filters.toughness.max !== null) searchFilters.toughness.max = filters.toughness.max;
      console.log('✅ Adding toughness filter:', searchFilters.toughness);
    }

    // Use the same race-condition-safe logic as searchForCards
    const searchId = Date.now() + Math.random();
    (window as any).currentSearchId = searchId;

    // Determine query strategy
    const hasFilters = Object.keys(searchFilters).length > 0;
    const hasQuery = query && query.trim() !== '';
    
    let actualQuery: string;
    if (hasQuery) {
      actualQuery = query.trim();
    } else if (hasFilters) {
      // Use wildcard when we have filters but no search text
      actualQuery = '*';
    } else {
      // No query and no filters - this should not happen, but fallback to popular cards
      console.log('❌ No query and no filters - falling back to popular cards');
      loadPopularCards();
      return;
    }
    
    console.log('🔍 ENHANCED SEARCH:', { 
      searchId: searchId.toFixed(3), 
      originalQuery: query,
      actualQuery: actualQuery,
      filters: searchFilters,
      filterCount: Object.keys(searchFilters).length,
      hasQuery,
      hasFilters
    });'''
    
    # Replace the function start
    content = content.replace(old_function_start, new_function_start)
    
    # Write the updated file
    with open('src/hooks/useCards.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed searchWithAllFilters filter building logic")

def fix_scryfall_api_empty_query():
    """Fix the Scryfall API to handle empty queries better"""
    
    # Read the current scryfallApi.ts file
    with open('src/services/scryfallApi.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and fix the searchCards function to handle empty queries
    old_search_cards = '''export const searchCards = async (
  query: string,
  page = 1,
  unique = 'cards',
  order = 'name'
): Promise<ScryfallSearchResponse> => {
  try {
    const params = new URLSearchParams({
      q: query,
      page: page.toString(),
      unique,
      order,
    });
    
    const url = `${SCRYFALL_API_BASE}/cards/search?${params.toString()}`;
    const response = await rateLimitedFetch(url);
    const data = await response.json();
    
    return data as ScryfallSearchResponse;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to search cards: ${error.message}`);
    } else {
      throw new Error('Failed to search cards: Unknown error');
    }
  }
};'''
    
    new_search_cards = '''export const searchCards = async (
  query: string,
  page = 1,
  unique = 'cards',
  order = 'name'
): Promise<ScryfallSearchResponse> => {
  try {
    // Handle empty queries - Scryfall doesn't accept empty q parameter
    if (!query || query.trim() === '') {
      throw new Error('Search query cannot be empty');
    }
    
    const params = new URLSearchParams({
      q: query.trim(),
      page: page.toString(),
      unique,
      order,
    });
    
    const url = `${SCRYFALL_API_BASE}/cards/search?${params.toString()}`;
    console.log('🌐 API Request:', url);
    const response = await rateLimitedFetch(url);
    const data = await response.json();
    
    return data as ScryfallSearchResponse;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to search cards: ${error.message}`);
    } else {
      throw new Error('Failed to search cards: Unknown error');
    }
  }
};'''
    
    content = content.replace(old_search_cards, new_search_cards)
    
    # Also fix searchCardsWithFilters to ensure it never passes empty queries
    old_filters_function = '''export const searchCardsWithFilters = async (
  query: string,
  filters: SearchFilters = {},
  page = 1
): Promise<ScryfallSearchResponse> => {
  let searchQuery = query;'''
    
    new_filters_function = '''export const searchCardsWithFilters = async (
  query: string,
  filters: SearchFilters = {},
  page = 1
): Promise<ScryfallSearchResponse> => {
  // Start with base query - ensure we never have empty query
  let searchQuery = query || '*';
  
  console.log('🔧 Building search query from:', { baseQuery: query, filters });'''
    
    content = content.replace(old_filters_function, new_filters_function)
    
    # Write the updated file
    with open('src/services/scryfallApi.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed Scryfall API empty query handling")

def main():
    """Execute fixes for API query building issues"""
    try:
        print("🔧 Fixing Phase 3C API Query Building Issues")
        print("=" * 55)
        
        print("\n📋 Fix 1: Improving filter object building...")
        fix_search_with_all_filters()
        
        print("\n📋 Fix 2: Fixing empty query handling in API...")
        fix_scryfall_api_empty_query()
        
        print("\n" + "=" * 55)
        print("✅ API Query Building Fixes Complete!")
        print("\n🧪 Test Again:")
        print("   1. Run 'npm start'")
        print("   2. Select 'Standard' format")
        print("   3. You should see:")
        print("      • '✅ Adding format filter: standard' in console")
        print("      • 'filterCount: 1' in enhanced search log")
        print("      • '🌐 API Request: https://api.scryfall.com/cards/search?q=*+legal%3Astandard'")
        print("      • Actual Standard cards in results")
        print("\n🔍 Key Changes:")
        print("   • Fixed filter object building to properly detect non-empty values")
        print("   • Added detailed logging for each filter type")
        print("   • Fixed empty query handling (uses '*' wildcard)")
        print("   • Added API request URL logging")
        
        print("\n💡 Debug tip: Watch for '✅ Adding [filter] filter:' messages")
        
    except Exception as e:
        print(f"\n❌ Error during fixes: {e}")
        print("Please check the file paths and try again.")

if __name__ == "__main__":
    main()
