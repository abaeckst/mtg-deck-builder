#!/usr/bin/env python3
"""
Comprehensive Multi-Word Search Fix Script
Fixes multi-word searches to work in both card names AND oracle text
"""

import os
import re

def fix_comprehensive_multiword_search():
    """Fix multi-word search to work in both names and oracle text"""
    
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
        
        # Replace with the comprehensive fixed function
        new_function = '''function buildEnhancedSearchQuery(query: string): string {
  // FIXED: Comprehensive multi-word search for names AND oracle text
  console.log('🔍 Building enhanced query for:', query);
  
  // For simple queries without operators, enable full-text search
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    // Check if query contains multiple words
    const words = query.trim().split(/\\s+/);
    
    if (words.length > 1) {
      // Multi-word query: search as exact phrase in BOTH name and oracle fields
      const quotedQuery = `"${query}"`;
      const result = `(name:${quotedQuery} OR oracle:${quotedQuery})`;
      console.log('🔍 Multi-word query detected, using:', result);
      return result;
    } else {
      // Single word: search across multiple fields
      const result = `(name:${query} OR oracle:${query} OR type:${query})`;
      console.log('🔍 Single word query, using broad search:', result);
      return result;
    }
  }
  
  // Advanced parsing for queries with operators (unchanged)
  const parts: string[] = [];
  let workingQuery = query;
  
  // Handle quoted phrases
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
  
  // Handle remaining terms
  const remainingTerms = workingQuery.trim().split(/\\s+/).filter(term => term.length > 0);
  if (remainingTerms.length > 0) {
    const fullTextSearch = remainingTerms.join(' ');
    const searchTerm = remainingTerms.length > 1 ? `"${fullTextSearch}"` : fullTextSearch;
    
    if (parts.length > 0) {
      parts.push(`(name:${searchTerm} OR oracle:${searchTerm} OR type:${searchTerm})`);
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
        
        print("✅ Comprehensive multi-word search fix applied successfully!")
        print("\n🎯 Changes made:")
        print("- Multi-word searches now use: (name:\"phrase\" OR oracle:\"phrase\")")
        print("- Searches BOTH card names AND oracle text for multi-word phrases")
        print("- Single word searches still use broad field search")
        print("- Added comprehensive debug logging")
        
        print("\n🧪 Test these searches:")
        print('- "Lightning Bolt" → should find Lightning Bolt cards by NAME')
        print('- "deal damage" → should find cards with that phrase in TEXT')
        print('- "enters the battlefield" → should find cards with that phrase in TEXT')
        print('- "flying" → should search across name, oracle, and type fields')
        print('- "draw a card" → should find cards with that phrase in TEXT')
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing file: {e}")
        return False

if __name__ == "__main__":
    print("🔧 MTG Deck Builder - Comprehensive Multi-Word Search Fix")
    print("=" * 60)
    
    success = fix_comprehensive_multiword_search()
    
    if success:
        print("\n✅ Fix completed successfully!")
        print("\n📋 Next steps:")
        print("1. Save this file if your editor shows changes")
        print('2. Test card name search: "Lightning Bolt"')
        print('3. Test oracle text search: "deal damage"')
        print('4. Test oracle text search: "enters the battlefield"')
        print("5. Check browser console for debug logs")
        print("6. Verify single-word searches still work")
    else:
        print("\n❌ Fix failed - please check the error messages above")
    
    print("\n" + "=" * 60)