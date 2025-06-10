#!/usr/bin/env python3
"""
Fix wildcard query performance by skipping enhancement for filter-only searches.

Root Issue: buildEnhancedSearchQuery() converts '*' into '(name:* OR o:* OR type:*)'
which forces Scryfall to scan entire database multiple times.

Solution: Skip query enhancement for wildcard searches, let Scryfall handle 
'*' efficiently with its internal optimizations.
"""

import os
import re

def update_scryfall_api():
    """Fix buildEnhancedSearchQuery to handle wildcards efficiently"""
    
    file_path = "src/services/scryfallApi.ts"
    
    # Read current file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the buildEnhancedSearchQuery function and add wildcard optimization
    old_function_start = r"""(function buildEnhancedSearchQuery\(query: string\): string \{
  console\.time\("⏱️ QUERY_BUILDING_TIME"\);
  // FIXED: Scryfall-compatible multi-word search syntax
  console\.log\('🔍 Building enhanced query for:', query\);
  console\.log\('🔍 INPUT ANALYSIS:', \{
    originalQuery: query,
    hasQuotes: query\.includes\('\"'\),
    hasDashes: query\.includes\('-'\),
    hasColons: query\.includes\(':'\),
    wordCount: query\.trim\(\)\.split\(/\\s\+/\)\.length
  \}\);
  
  // For simple queries without operators, enable full-text search
  if \(!query\.includes\('\"'\) && !query\.includes\('-'\) && !query\.includes\(':'\)\) \{)"""
    
    new_function_start = r"""function buildEnhancedSearchQuery(query: string): string {
  console.time("⏱️ QUERY_BUILDING_TIME");
  
  // PERFORMANCE OPTIMIZATION: Skip enhancement for wildcard filter-only searches
  // Let Scryfall handle '*' efficiently with internal optimizations
  if (query.trim() === '*') {
    console.log('🚀 WILDCARD OPTIMIZATION: Skipping enhancement for filter-only search');
    console.timeEnd("⏱️ QUERY_BUILDING_TIME");
    return '*';
  }
  
  // FIXED: Scryfall-compatible multi-word search syntax
  console.log('🔍 Building enhanced query for:', query);
  console.log('🔍 INPUT ANALYSIS:', {
    originalQuery: query,
    hasQuotes: query.includes('"'),
    hasDashes: query.includes('-'),
    hasColons: query.includes(':'),
    wordCount: query.trim().split(/\s+/).length
  });
  
  // For simple queries without operators, enable full-text search
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {"""
    
    # Replace the function start
    content = re.sub(old_function_start, new_function_start, content, flags=re.DOTALL)
    
    # Also add a performance logging enhancement to show query optimization decisions
    old_logging_pattern = r"""(  console\.log\('🔍 ENHANCED QUERY RESULT:', \{
    originalInput: query,
    processedOutput: result,
    parts: parts,
    isMultiWord: query\.trim\(\)\.split\(/\\s\+/\)\.length > 1,
    hasOperators: query\.includes\('\"'\) \|\| query\.includes\('-'\) \|\| query\.includes\(':'\)
  \}\);
  console\.timeEnd\("⏱️ QUERY_BUILDING_TIME"\);
  return result;)"""
    
    new_logging_pattern = r"""  console.log('🔍 ENHANCED QUERY RESULT:', {
    originalInput: query,
    processedOutput: result,
    parts: parts,
    isMultiWord: query.trim().split(/\s+/).length > 1,
    hasOperators: query.includes('"') || query.includes('-') || query.includes(':'),
    optimizationApplied: 'Full enhancement (not wildcard)'
  });
  console.timeEnd("⏱️ QUERY_BUILDING_TIME");
  return result;"""
    
    # Replace the logging
    content = re.sub(old_logging_pattern, new_logging_pattern, content, flags=re.DOTALL)
    
    # Write updated file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated scryfallApi.ts with wildcard performance optimization")

def update_use_search_logging():
    """Add performance logging to track wildcard optimization impact"""
    
    file_path = "src/hooks/useSearch.ts"
    
    # Read current file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add performance tracking to searchWithAllFilters
    old_logging = r"""(    console\.log\('🚀 EXECUTING CLEAN SEARCH:', \{
      query: actualQuery,
      appliedFilters: Object\.keys\(searchFilters\),
      sortOrder: defaultSortParams\.order,
      sortDirection: defaultSortParams\.dir
    \}\);)"""
    
    new_logging = r"""    console.log('🚀 EXECUTING CLEAN SEARCH:', {
      query: actualQuery,
      appliedFilters: Object.keys(searchFilters),
      sortOrder: defaultSortParams.order,
      sortDirection: defaultSortParams.dir,
      isWildcardSearch: actualQuery === '*',
      expectedPerformance: actualQuery === '*' ? 'FAST (wildcard optimized)' : 'NORMAL (enhanced query)'
    });"""
    
    # Replace the logging
    content = re.sub(old_logging, new_logging, content, flags=re.DOTALL)
    
    # Write updated file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated useSearch.ts with performance tracking")

def main():
    """Execute wildcard performance optimization"""
    
    print("🚀 Implementing wildcard performance optimization...")
    print("📋 Performance Issue Analysis:")
    print("  🐌 SLOW: '(name:* OR o:* OR type:*) legal:standard identity<=B' (~1300ms)")
    print("  🚀 FAST: '* legal:standard identity<=B' (~100-300ms)")
    print("")
    print("🔧 Fix Strategy:")
    print("  1. Skip query enhancement for wildcard '*' searches")
    print("  2. Let Scryfall handle wildcards with internal optimizations")
    print("  3. Add performance tracking to measure improvement")
    print("")
    
    # Verify files exist
    files_to_check = [
        "src/services/scryfallApi.ts",
        "src/hooks/useSearch.ts"
    ]
    
    for file_path in files_to_check:
        if not os.path.exists(file_path):
            print(f"❌ Error: {file_path} not found")
            return
    
    try:
        update_scryfall_api()
        update_use_search_logging()
        
        print("")
        print("✅ Wildcard performance optimization implemented!")
        print("")
        print("🎯 What this achieves:")
        print("  ✓ Filter-only searches use optimized '*' query")
        print("  ✓ 3-10x faster performance for color/type filter clicks")
        print("  ✓ Scryfall's internal wildcard optimizations leveraged")
        print("  ✓ Enhanced search still works for actual search terms")
        print("")
        print("📊 Expected Performance Improvements:")
        print("  ✓ Color filter clicks: 1300ms → 100-300ms")
        print("  ✓ Type filter clicks: Similar dramatic improvement")
        print("  ✓ Any filter-only search: Much faster response")
        print("")
        print("🧪 Test Cases to Validate:")
        print("  1. Click black color button → Should see 'WILDCARD OPTIMIZATION' log")
        print("  2. Search for 'lightning bolt' → Should see 'Full enhancement' log")
        print("  3. Add any filter → Should be noticeably faster")
        print("  4. Check console for 'expectedPerformance: FAST' vs 'NORMAL'")
        print("")
        print("🚀 Run 'npm start' to test the performance improvement!")
        
    except Exception as e:
        print(f"❌ Error implementing optimization: {e}")

if __name__ == "__main__":
    main()
