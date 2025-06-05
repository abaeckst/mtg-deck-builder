#!/usr/bin/env python3

import os
import sys
from datetime import datetime

def fix_scryfall_api():
    """Fix syntax errors in scryfallApi.ts"""
    
    scryfall_file = "src/services/scryfallApi.ts"
    backup_file = f"src/services/scryfallApi.ts.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if not os.path.exists(scryfall_file):
        print(f"❌ Error: {scryfall_file} not found")
        return False
    
    # Read the current file
    try:
        with open(scryfall_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ Read scryfallApi.ts ({len(content)} characters)")
    except Exception as e:
        print(f"❌ Error reading {scryfall_file}: {e}")
        return False
    
    # Create backup
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created backup: {backup_file}")
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return False
    
    # Fix the loadMoreResults function - add missing return and closing brace
    if "}: Promise<ScryfallCard[]> => {" in content and "return newCards;" not in content:
        # Find the position after the console.log and add the missing return and closing brace
        progress_report_pos = content.find("onProgress(paginationState.loadedCards + newCards.length, paginationState.totalCards);")
        if progress_report_pos != -1:
            # Find the end of that line
            line_end = content.find("\n", progress_report_pos)
            if line_end != -1:
                # Insert the missing return statement and closing brace
                missing_code = """
    
    return newCards;
  } catch (error) {
    console.error('❌ Load more results failed:', error);
    throw error;
  }
};"""
                content = content[:line_end + 1] + missing_code + content[line_end + 1:]
                print("✅ Fixed loadMoreResults function - added missing return and closing brace")
    
    # Move buildEnhancedSearchQuery function declaration to top level (before it's used)
    function_declaration = """/**
 * Build enhanced search query with operator support
 */
function buildEnhancedSearchQuery(query: string): string {
  // FIXED: Scryfall-compatible multi-word search syntax
  console.log('🔍 Building enhanced query for:', query);
  
  // For simple queries without operators, enable full-text search
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    const words = query.trim().split(/\\s+/);
    
    if (words.length > 1) {
      // Multi-word query: Each word should match name, oracle text, OR type
      // Format: (name:word1 OR o:word1 OR type:word1) (name:word2 OR o:word2 OR type:word2)
      console.log('🔍 Multi-word query detected, using comprehensive field search:', query);
      const wordQueries = words.map(word => `(name:${word} OR o:${word} OR type:${word})`);
      const result = wordQueries.join(' ');
      console.log('🔍 Multi-word result:', result);
      return result;
    } else {
      // Single word: search across multiple fields
      const result = `(name:${query} OR o:${query} OR type:${query})`;
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
      parts.push(`o:${processedValue}`);
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
}"""
    
    # Remove the function declaration from its current location
    if "function buildEnhancedSearchQuery(query: string): string {" in content:
        # Find the start of the function
        func_start = content.find("/**\n * Build enhanced search query with operator support\n */\nfunction buildEnhancedSearchQuery")
        if func_start == -1:
            func_start = content.find("function buildEnhancedSearchQuery(query: string): string {")
        
        if func_start != -1:
            # Find the end of the function (looking for the closing brace and newline)
            brace_count = 0
            func_end = func_start
            found_opening = False
            
            while func_end < len(content):
                if content[func_end] == '{':
                    found_opening = True
                    brace_count += 1
                elif content[func_end] == '}':
                    brace_count -= 1
                    if found_opening and brace_count == 0:
                        func_end += 1  # Include the closing brace
                        break
                func_end += 1
            
            # Remove the function from its current location
            content = content[:func_start] + content[func_end:]
            print("✅ Removed buildEnhancedSearchQuery from its current location")
    
    # Add the function declaration after the interfaces but before searchCardsWithPagination
    insertion_point = content.find("export const searchCardsWithPagination")
    if insertion_point != -1:
        content = content[:insertion_point] + function_declaration + "\n\n" + content[insertion_point:]
        print("✅ Added buildEnhancedSearchQuery function at top level")
    
    # Write the fixed content
    try:
        with open(scryfall_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully fixed {scryfall_file}")
    except Exception as e:
        print(f"❌ Error writing fixed file: {e}")
        return False
    
    print("\n🎉 scryfallApi.ts Fix Complete!")
    print("\nNext steps:")
    print("1. Test compilation: npm start")
    print("2. If successful, the Load More functionality should work")
    print("3. If any issues occur, restore from backup:")
    print(f"   cp {backup_file} {scryfall_file}")
    
    return True

if __name__ == "__main__":
    print("🔧 MTG Deck Builder - Fix scryfallApi.ts Script")
    print("=" * 50)
    
    if not os.path.exists("package.json"):
        print("❌ Error: This doesn't appear to be the project root directory")
        print("Please run this script from C:/Users/abaec/Development/mtg-deck-builder/")
        sys.exit(1)
    
    success = fix_scryfall_api()
    sys.exit(0 if success else 1)