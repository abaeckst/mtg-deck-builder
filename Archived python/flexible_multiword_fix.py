#!/usr/bin/env python3
"""
Flexible Multi-Word Search Fix Script
Fixes multi-word searches to allow partial matching (no forced quotes)
"""

import os
import re

def fix_flexible_multiword_search():
    """Fix multi-word search to allow partial matching without forced quotes"""
    
    file_path = "src/services/scryfallApi.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found!")
        print("Make sure you're running this script from your project root directory.")
        return False
    
    try:
        # Read the current file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the buildEnhancedSearchQuery function
        function_start = content.find('function buildEnhancedSearchQuery(query: string): string {')
        if function_start == -1:
            print("❌ Error: buildEnhancedSearchQuery function not found!")
            return False
        
        # Find the end of the function
        function_end = content.find('\n/**', function_start)
        if function_end == -1:
            function_end = content.find('\nexport const', function_start)
        if function_end == -1:
            function_end = len(content)
        
        # Replace with the flexible fixed function
        new_function = '''function buildEnhancedSearchQuery(query: string): string {
  // FIXED: Flexible multi-word search that allows partial matching
  console.log('🔍 Building enhanced query for:', query);
  
  // For simple queries without operators, enable full-text search
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    // For multi-word queries, use unquoted search to allow partial matching
    // This lets "deal damage" match "deal 3 damage", "deal damage to", etc.
    const words = query.trim().split(/\\s+/);
    
    if (words.length > 1) {
      // Multi-word query: search WITHOUT quotes for flexible matching
      const result = `(name:${query} OR oracle:${query})`;
      console.log('🔍 Multi-word query detected, using flexible search:', result);
      return result;
    } else {
      // Single word: search across multiple fields
      const result = `(name:${query} OR oracle:${query} OR type:${query})`;
      console.log('🔍 Single word query, using broad search:', result);
      return result;
    }
  }
  
  // Advanced parsing for queries with explicit operators
  const parts: string[] = [];
  let workingQuery = query;
  
  // Handle quoted phrases (user explicitly wants exact match)
  const quotedPhrases = query.match(/"[^"]+"/g) || [];
  quotedPhrases.forEach(phrase => {
    parts.push(phrase);
    workingQuery = workingQuery.replace(phrase, '');
  });
  
  // Handle exclusions
  const exclusions = workingQuery.match(/-"[^"]+"|--?[\\w\\s]+/g) || [];
  exclusions.forEach(exclusion => {
    parts.push(exclusion);
    workingQuery = workingQuery.replace(exclusion, '');
  });
  
  // Handle field-specific searches
  const fieldSearches = workingQuery.match(/(name|text|type|oracle):"[^"]+"|(?:name|text|type|oracle):[\\w\\s]+(?=\\s|$)/g) || [];
  fieldSearches.forEach(fieldSearch => {
    const colonIndex = fieldSearch.indexOf(':');
    const field = fieldSearch.substring(0, colonIndex);
    const value = fieldSearch.substring(colonIndex + 1);
    
    if (field === 'text') {
      parts.push(`oracle:${value}`);
    } else {
      parts.push(fieldSearch);
    }
    workingQuery = workingQuery.replace(fieldSearch, '');
  });
  
  // Handle remaining terms - use flexible matching for multi-word
  const remainingTerms = workingQuery.trim().split(/\\s+/).filter(term => term.length > 0);
  if (remainingTerms.length > 0) {
    const fullTextSearch = remainingTerms.join(' ');
    
    // Don't force quotes unless user explicitly added them
    if (parts.length > 0) {
      parts.push(`(name:${fullTextSearch} OR oracle:${fullTextSearch} OR type:${fullTextSearch})`);
    } else {
      parts.push(fullTextSearch);
    }
  }
  
  const result = parts.join(' ').trim() || query;
  console.log('🔍 Final enhanced query:', result);
  return result;
}'''
        
        # Replace the function in the content
        new_content = content[:function_start] + new_function + content[function_end:]
        
        # Write the fixed content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Flexible multi-word search fix applied successfully!")
        print("\n🎯 Changes made:")
        print("- Multi-word searches now use: (name:deal damage OR oracle:deal damage)")
        print("- NO forced quotes for flexible partial matching")
        print("- 'deal damage' will match 'deal 3 damage', 'deal damage to', etc.")
        print("- User can still use quotes for exact matching: \"deal damage\"")
        
        print("\n🧪 Test these searches:")
        print('- "Lightning Bolt" → should find Lightning Bolt cards by NAME')
        print('- deal damage → should find cards with "deal 3 damage", "deal damage to", etc.')
        print('- enters battlefield → should find "enters the battlefield" cards')
        print('- target creature → should find "target creature you control", etc.')
        print('- "deal damage" → exact phrase match (user explicitly quoted)')
        print('- flying → should search across name, oracle, and type fields')
        
        print("\n💡 Key improvement:")
        print("- Unquoted multi-word searches are now FLEXIBLE")
        print("- Quoted searches are EXACT (when user wants precision)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing file: {e}")
        return False

if __name__ == "__main__":
    print("🔧 MTG Deck Builder - Flexible Multi-Word Search Fix")
    print("=" * 60)
    
    success = fix_flexible_multiword_search()
    
    if success:
        print("\n✅ Fix completed successfully!")
        print("\n📋 Next steps:")
        print("1. Save this file if your editor shows changes")
        print("2. Test flexible search: deal damage")
        print("3. Test flexible search: enters battlefield") 
        print("4. Test exact search: \"deal damage\" (with quotes)")
        print("5. Check browser console for debug logs")
        print("6. Verify the difference between quoted and unquoted searches")
    else:
        print("\n❌ Fix failed - please check the error messages above")
    
    print("\n" + "=" * 60)