#!/usr/bin/env python3
"""
Scryfall-Compatible Multi-Word Search Fix Script
Fixes multi-word searches to use proper Scryfall API syntax
"""

import os
import re

def fix_scryfall_compatible_multiword_search():
    """Fix multi-word search to use proper Scryfall syntax that actually works"""
    
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
        
        # Replace with the Scryfall-compatible fixed function
        new_function = '''function buildEnhancedSearchQuery(query: string): string {
  // FIXED: Scryfall-compatible multi-word search syntax
  console.log('🔍 Building enhanced query for:', query);
  
  // For simple queries without operators, enable full-text search
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    const words = query.trim().split(/\\s+/);
    
    if (words.length > 1) {
      // Multi-word query: Use Scryfall-compatible syntax
      // Option 1: Simple space-separated search (Scryfall handles this well)
      console.log('🔍 Multi-word query detected, using simple syntax:', query);
      return query;
    } else {
      // Single word: search across multiple fields
      const result = `(name:${query} OR oracle:${query} OR type:${query})`;
      console.log('🔍 Single word query, using field search:', result);
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
  
  // Handle field-specific searches - QUOTE multi-word values
  const fieldSearches = workingQuery.match(/(name|text|type|oracle):"[^"]+"|(?:name|text|type|oracle):[\\w\\s]+(?=\\s|$)/g) || [];
  fieldSearches.forEach(fieldSearch => {
    const colonIndex = fieldSearch.indexOf(':');
    const field = fieldSearch.substring(0, colonIndex);
    const value = fieldSearch.substring(colonIndex + 1);
    
    // If multi-word field value, add quotes
    const processedValue = value.includes(' ') && !value.startsWith('"') ? `"${value}"` : value;
    
    if (field === 'text') {
      parts.push(`oracle:${processedValue}`);
    } else {
      parts.push(`${field}:${processedValue}`);
    }
    workingQuery = workingQuery.replace(fieldSearch, '');
  });
  
  // Handle remaining terms - use simple syntax for multi-word
  const remainingTerms = workingQuery.trim().split(/\\s+/).filter(term => term.length > 0);
  if (remainingTerms.length > 0) {
    const fullTextSearch = remainingTerms.join(' ');
    
    if (parts.length > 0) {
      // If we have other operators, add as simple search
      parts.push(fullTextSearch);
    } else {
      // Simple search without field restrictions
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
        
        print("✅ Scryfall-compatible multi-word search fix applied!")
        print("\n🎯 Changes made:")
        print("- Multi-word searches now use simple Scryfall syntax: 'deal damage'")
        print("- Scryfall's default search handles multi-word queries well")
        print("- Single words still use field-specific searches: (name:flying OR oracle:flying)")
        print("- Field searches with multi-word values get quoted automatically")
        
        print("\n🧪 Test these searches:")
        print("- deal damage → simple search, Scryfall handles partial matching")
        print("- enters battlefield → simple search, finds ETB effects")
        print("- target creature → simple search, finds targeting effects")
        print("- flying → field search across name, oracle, type")
        print('- "deal damage" → exact phrase search')
        print("- name:lightning → field search for 'lightning' in names")
        
        print("\n💡 How this works:")
        print("- Multi-word queries use Scryfall's default search behavior")
        print("- Scryfall naturally searches names, oracle text, and other fields")
        print("- This avoids complex field syntax that was causing 404 errors")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing file: {e}")
        return False

if __name__ == "__main__":
    print("🔧 MTG Deck Builder - Scryfall-Compatible Multi-Word Search Fix")
    print("=" * 70)
    
    success = fix_scryfall_compatible_multiword_search()
    
    if success:
        print("\n✅ Fix completed successfully!")
        print("\n📋 Next steps:")
        print("1. Save this file if your editor shows changes")
        print("2. Test the problematic search: deal damage")
        print("3. Test other multi-word searches: enters battlefield")
        print("4. Check console logs - should see simpler query syntax")
        print("5. Verify no more 404 errors from Scryfall API")
    else:
        print("\n❌ Fix failed - please check the error messages above")
    
    print("\n" + "=" * 70)