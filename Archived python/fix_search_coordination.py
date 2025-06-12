#!/usr/bin/env python3

# Fix the search coordination to properly use mana value sorting by default
# The issue: enhancedSearch and related functions don't respect the sort coordination

import re

def fix_search_coordination():
    print("🔧 Fixing search coordination to use mana value sorting by default...")
    
    # Read current useSearch.ts file
    try:
        with open('src/hooks/useSearch.ts', 'r', encoding='utf-8') as f:
            use_search_content = f.read()
    except FileNotFoundError:
        print("❌ useSearch.ts not found")
        return False
    
    # Read current scryfallApi.ts file  
    try:
        with open('src/services/scryfallApi.ts', 'r', encoding='utf-8') as f:
            api_content = f.read()
    except FileNotFoundError:
        print("❌ scryfallApi.ts not found")
        return False

    print("📝 Files read successfully, applying fixes...")
    
    # Fix 1: Update enhancedSearch to pass sort parameters properly
    enhanced_search_pattern = r'(const enhancedSearch = useCallback\(async \(query: string, filtersOverride\?: any\) => \{[\s\S]*?)await searchWithPagination\(query, filters as SearchFilters\);'
    
    enhanced_search_replacement = r'''\1// Get default sort parameters for consistent sorting
    const defaultSortParams = getCollectionSortParams();
    await searchWithPagination(query, filters as SearchFilters, defaultSortParams.order, defaultSortParams.dir);'''
    
    if re.search(enhanced_search_pattern, use_search_content):
        use_search_content = re.sub(enhanced_search_pattern, enhanced_search_replacement, use_search_content)
        print("✅ Fixed enhancedSearch to use sort coordination")
    else:
        print("⚠️ Could not find enhancedSearch pattern in useSearch.ts")
    
    # Fix 2: Update searchWithAllFilters to pass sort parameters
    search_with_filters_pattern = r'(await searchWithPagination\(actualQuery, searchFilters\);)'
    search_with_filters_replacement = r'''// Get default sort parameters for consistent sorting
    const defaultSortParams = getCollectionSortParams();
    await searchWithPagination(actualQuery, searchFilters, defaultSortParams.order, defaultSortParams.dir);'''
    
    if re.search(search_with_filters_pattern, use_search_content):
        use_search_content = re.sub(search_with_filters_pattern, search_with_filters_replacement, use_search_content)
        print("✅ Fixed searchWithAllFilters to use sort coordination")
    else:
        print("⚠️ Could not find searchWithAllFilters pattern")
    
    # Fix 3: Update enhancedSearchCards in scryfallApi.ts to default to 'cmc' order
    api_function_pattern = r'(export const enhancedSearchCards = async \(\s*query: string,\s*filters: SearchFilters = \{\},\s*page = 1,\s*)order = \'name\'(,\s*dir: \'asc\' \| \'desc\' = \'asc\')'
    api_function_replacement = r"\1order = 'cmc'\2"
    
    if re.search(api_function_pattern, api_content):
        api_content = re.sub(api_function_pattern, api_function_replacement, api_content)
        print("✅ Fixed enhancedSearchCards to default to 'cmc' order")
    else:
        print("⚠️ Could not find enhancedSearchCards pattern in scryfallApi.ts")
    
    # Fix 4: Update searchCardsWithPagination to default to 'cmc' order
    pagination_pattern = r'(export const searchCardsWithPagination = async \(\s*query: string,\s*filters: SearchFilters = \{\},\s*)order = \'name\'(,\s*dir: \'asc\' \| \'desc\' = \'asc\')'
    pagination_replacement = r"\1order = 'cmc'\2"
    
    if re.search(pagination_pattern, api_content):
        api_content = re.sub(pagination_pattern, pagination_replacement, api_content)
        print("✅ Fixed searchCardsWithPagination to default to 'cmc' order")
    else:
        print("⚠️ Could not find searchCardsWithPagination pattern")
    
    # Write updated files
    try:
        with open('src/hooks/useSearch.ts', 'w', encoding='utf-8') as f:
            f.write(use_search_content)
        print("✅ Updated useSearch.ts successfully")
    except Exception as e:
        print(f"❌ Failed to write useSearch.ts: {e}")
        return False
    
    try:
        with open('src/services/scryfallApi.ts', 'w', encoding='utf-8') as f:
            f.write(api_content)
        print("✅ Updated scryfallApi.ts successfully")
    except Exception as e:
        print(f"❌ Failed to write scryfallApi.ts: {e}")
        return False
    
    print("\n🎯 COORDINATION FIX SUMMARY:")
    print("1. enhancedSearch now gets sort params from useSorting via getCollectionSortParams")
    print("2. searchWithAllFilters now uses coordinated sort parameters")
    print("3. enhancedSearchCards defaults to 'cmc' (mana value) instead of 'name'")
    print("4. searchCardsWithPagination defaults to 'cmc' instead of 'name'")
    print("\n✨ Expected result: Initial searches should now be sorted by mana value!")
    print("🧪 Test with: Search 'lightning bolt' and verify console shows 'cmc' order")
    
    return True

if __name__ == "__main__":
    success = fix_search_coordination()
    if success:
        print("\n🚀 Search coordination fix complete! Test the application now.")
    else:
        print("\n❌ Search coordination fix failed. Check error messages above.")
