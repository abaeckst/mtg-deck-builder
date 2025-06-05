#!/usr/bin/env python3

import os
import sys

def fix_url_encoding_root_cause():
    """Fix the URL encoding issue that's causing 404 errors"""
    
    filename = "src/services/scryfallApi.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # The issue is in the searchCards function - find the current implementation
    # and replace it with proper URL building
    
    old_search_function = '''export const searchCards = async (
  query: string,
  page = 1,
  unique = 'cards',
  order = 'name',
  dir: 'asc' | 'desc' = 'asc'
): Promise<ScryfallSearchResponse> => {
  try {
    // Handle empty queries - Scryfall doesn't accept empty q parameter
    if (!query || query.trim() === '') {
      throw new Error('Search query cannot be empty');
    }
    
    // Build URL manually to avoid double-encoding issues
    const encodedQuery = encodeURIComponent(query.trim());
    const url = `${SCRYFALL_API_BASE}/cards/search?q=${encodedQuery}&page=${page}&unique=${unique}&order=${order}&dir=${dir}`;
    console.log('🌐 API Request with sort:', { url, order, dir, originalQuery: query.trim() });
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
    
    new_search_function = '''export const searchCards = async (
  query: string,
  page = 1,
  unique = 'cards',
  order = 'name',
  dir: 'asc' | 'desc' = 'asc'
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
      dir,
    });
    
    const url = `${SCRYFALL_API_BASE}/cards/search?${params.toString()}`;
    console.log('🌐 API Request with sort:', { url, order, dir, originalQuery: query.trim() });
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
    
    if old_search_function in content:
        content = content.replace(old_search_function, new_search_function)
        print("✅ Fixed URL encoding in searchCards function")
    else:
        print("❌ Could not find exact searchCards function to fix")
        
        # Try to find and fix just the URL building part
        old_url_building = '''    // Build URL manually to avoid double-encoding issues
    const encodedQuery = encodeURIComponent(query.trim());
    const url = `${SCRYFALL_API_BASE}/cards/search?q=${encodedQuery}&page=${page}&unique=${unique}&order=${order}&dir=${dir}`;'''
    
        new_url_building = '''    const params = new URLSearchParams({
      q: query.trim(),
      page: page.toString(),
      unique,
      order,
      dir,
    });
    
    const url = `${SCRYFALL_API_BASE}/cards/search?${params.toString()}`;'''
    
        if old_url_building in content:
            content = content.replace(old_url_building, new_url_building)
            print("✅ Fixed URL building method")
        else:
            print("❌ Could not find URL building code to fix")
            return False
    
    # Also check for any issues in format filter handling that might be causing double legal: filters
    
    # Write the fixed content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed URL encoding issues")
    return True

def remove_default_format_filter():
    """Remove the automatic legal:standard filter that's being added"""
    
    filename = "src/hooks/useCards.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if there's a default format filter being applied
    old_default_format = '''      activeFilters: {
        format: 'custom-standard',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },'''
    
    new_default_format = '''      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },'''
    
    if old_default_format in content:
        content = content.replace(old_default_format, new_default_format)
        print("✅ Removed default 'custom-standard' format filter")
    else:
        print("ℹ️  No default format filter found to remove")
    
    # Also check the clearAllFilters function
    old_clear_filters = '''      activeFilters: {
        format: 'custom-standard',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },'''
    
    new_clear_filters = '''      activeFilters: {
        format: '',
        colors: [],
        colorIdentity: 'exact',
        types: [],
        rarity: [],
        sets: [],
        cmc: { min: null, max: null },
        power: { min: null, max: null },
        toughness: { min: null, max: null },
      },'''
    
    if old_clear_filters in content:
        content = content.replace(old_clear_filters, new_clear_filters)
        print("✅ Fixed clearAllFilters to not default to custom-standard")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

if __name__ == "__main__":
    print("🔧 FIXING URL ENCODING ROOT CAUSE")
    print("=" * 50)
    
    success1 = fix_url_encoding_root_cause()
    success2 = remove_default_format_filter()
    
    if success1 and success2:
        print("\n✅ ROOT CAUSE FIXES APPLIED")
        print("\n📋 What was fixed:")
        print("1. ✅ URL encoding now uses URLSearchParams properly")
        print("2. ✅ Removed automatic 'custom-standard' format filter")
        print("3. ✅ Search queries should work without legal: being added")
        print("\n📱 Test steps:")
        print("1. Refresh browser")
        print("2. Search for 'creature' - should work without legal:standard")
        print("3. Should find cards with 'creature' in name, text, or type")
        print("4. Load More button should still work")
    else:
        print("\n❌ Some fixes failed")
    
    sys.exit(0 if success1 and success2 else 1)