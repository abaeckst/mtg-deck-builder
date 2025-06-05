#!/usr/bin/env python3

import os
import sys

def enhance_search_debugging(filename):
    """Add detailed search debugging to scryfallApi.ts for easy diagnosis"""
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Enhanced logging for buildEnhancedSearchQuery function
    old_build_query_start = '''function buildEnhancedSearchQuery(query: string): string {
  // FIXED: Scryfall-compatible multi-word search syntax
  console.log('🔍 Building enhanced query for:', query);'''

    new_build_query_start = '''function buildEnhancedSearchQuery(query: string): string {
  // FIXED: Scryfall-compatible multi-word search syntax
  console.log('🔍 Building enhanced query for:', query);
  console.log('🔍 INPUT ANALYSIS:', {
    originalQuery: query,
    hasQuotes: query.includes('"'),
    hasDashes: query.includes('-'),
    hasColons: query.includes(':'),
    wordCount: query.trim().split(/\s+/).length
  });'''

    # Enhanced logging for final result
    old_build_query_end = '''  const result = parts.join(' ').trim() || query;
  console.log('🔍 Final enhanced query:', result);
  return result;'''

    new_build_query_end = '''  const result = parts.join(' ').trim() || query;
  console.log('🔍 ENHANCED QUERY RESULT:', {
    originalInput: query,
    processedOutput: result,
    parts: parts,
    isMultiWord: query.trim().split(/\s+/).length > 1,
    hasOperators: query.includes('"') || query.includes('-') || query.includes(':')
  });
  return result;'''

    # Enhanced logging for searchCardsWithFilters
    old_search_filters_log = '''  console.log('🔧 Building search query from:', { 
    baseQuery: query, 
    filters, 
    sort: { order, dir },
    formatFilter: filters.format,
    hasFormatFilter: !!filters.format && filters.format.trim() !== ''
  });'''

    new_search_filters_log = '''  console.log('🔧 SEARCH FILTERS INPUT:', { 
    baseQuery: query, 
    filters: JSON.stringify(filters, null, 2),
    sort: { order, dir },
    formatFilter: filters.format,
    hasFormatFilter: !!filters.format && filters.format.trim() !== ''
  });'''

    # Enhanced logging for final search query
    old_final_query_log = '''  console.log('🔧 Final search query built:', { 
    originalQuery: query, 
    finalQuery: searchQuery.trim(),
    activeFilters: activeFilters,
    filterDetails: filterDetails
  });'''

    new_final_query_log = '''  console.log('🔧 FINAL SEARCH QUERY:', { 
    step1_originalQuery: query, 
    step2_finalQuery: searchQuery.trim(),
    step3_activeFilters: activeFilters,
    step4_filterDetails: JSON.stringify(filterDetails, null, 2),
    step5_willCallSearchCardsWithSort: true
  });'''

    # Enhanced logging for API request
    old_api_request_log = '''    console.log('🌐 API Request with sort:', { url, order, dir });'''

    new_api_request_log = '''    console.log('🌐 SCRYFALL API REQUEST:', { 
      fullURL: url,
      queryParam: query.trim(),
      sortOrder: order,
      sortDirection: dir,
      parsedParams: Object.fromEntries(new URLSearchParams(url.split('?')[1] || ''))
    });'''

    # Apply all replacements
    updates = [
        (old_build_query_start, new_build_query_start, "Enhanced buildEnhancedSearchQuery input logging"),
        (old_build_query_end, new_build_query_end, "Enhanced buildEnhancedSearchQuery output logging"),
        (old_search_filters_log, new_search_filters_log, "Enhanced searchCardsWithFilters input logging"),
        (old_final_query_log, new_final_query_log, "Enhanced final query logging"),
        (old_api_request_log, new_api_request_log, "Enhanced API request logging")
    ]
    
    for old_str, new_str, desc in updates:
        if old_str in content:
            content = content.replace(old_str, new_str)
            print(f"✅ {desc}")
        else:
            print(f"❌ Could not find: {desc}")
            print(f"   Looking for: {old_str[:50]}...")
            return False
    
    # Add a console helper function at the top of the file
    helper_function = '''
// DEBUGGING HELPER: Copy this function to browser console for easy output capture
function captureSearchDebug() {
  console.log('='.repeat(80));
  console.log('SEARCH DEBUG CAPTURE - Ready for copy/paste');
  console.log('='.repeat(80));
  console.log('Instructions: Now perform your search, then scroll up to copy all the debug output');
  console.log('='.repeat(80));
}

'''
    
    # Insert helper at the top after imports
    import_end = content.find('\n\nconst SCRYFALL_API_BASE')
    if import_end != -1:
        content = content[:import_end] + helper_function + content[import_end:]
        print("✅ Added console helper function")
    else:
        print("❌ Could not add console helper function")
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Successfully enhanced debugging in {filename}")
    print("\n🎯 NEXT STEPS:")
    print("1. Run this script to update the file")
    print("2. Start your development server: npm start")
    print("3. Open browser console")
    print("4. Type: captureSearchDebug()")
    print("5. Search for 'lightning'")
    print("6. Copy all the detailed debug output")
    print("7. Share the complete output")
    
    return True

if __name__ == "__main__":
    success = enhance_search_debugging("src/services/scryfallApi.ts")
    sys.exit(0 if success else 1)