#!/usr/bin/env python3

import os
import sys

def fix_multi_word_search():
    """Fix buildEnhancedSearchQuery function to properly handle multi-word searches"""
    
    filename = "src/services/scryfallApi.ts"
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found")
        return False
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the old multi-word search logic to replace
    old_multiword_logic = '''  // For simple queries without operators, enable full-text search
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    const words = query.trim().split(/\s+/);
    
    if (words.length > 1) {
  // Multi-word query: Search for individual words with AND logic
  console.log('🔍 Multi-word query detected, using individual word search:', query);
  const words = query.trim().split(/\s+/);
  const oracleTerms = words.map(word => `o:${word}`).join(' ');
  return oracleTerms;
} else {
      // Single word: search across multiple fields
      const result = `(name:${query} OR o:${query} OR type:${query})`;
      console.log('🔍 Single word query, using field search:', result);
      return result;
    }
  }'''

    # Define the new improved multi-word search logic
    new_multiword_logic = '''  // For simple queries without operators, enable full-text search
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    const words = query.trim().split(/\s+/);
    
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
  }'''

    # Make the replacement
    if old_multiword_logic in content:
        content = content.replace(old_multiword_logic, new_multiword_logic)
        print("✅ Fixed multi-word search logic in buildEnhancedSearchQuery function")
        
        # Write the updated content back to the file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Successfully updated scryfallApi.ts")
        print("")
        print("🎯 MULTI-WORD SEARCH FIX APPLIED:")
        print("   Before: 'lightning bolt' → o:lightning o:bolt (restrictive AND)")
        print("   After:  'lightning bolt' → (name:lightning OR o:lightning OR type:lightning) (name:bolt OR o:bolt OR type:bolt)")
        print("")
        print("✅ This fix will:")
        print("   • Find 'Lightning Bolt' when searching 'lightning bolt'")
        print("   • Find 'flying creature' matches creatures with flying ability")
        print("   • Preserve exact phrase search with quotes: \"lightning bolt\"")
        print("   • Keep single word searches working across name/text/type")
        print("")
        print("🚀 Next steps:")
        print("   1. Test in browser: npm start")
        print("   2. Search for 'lightning bolt' (should find Lightning Bolt)")
        print("   3. Search for 'flying creature' (should find flying creatures)")
        print("   4. Search for '\"lightning bolt\"' (should find exact phrase)")
        print("")
        return True
    else:
        print("❌ Could not find the expected multi-word search logic to replace")
        print("📄 The function may have already been updated or the structure changed")
        return False

if __name__ == "__main__":
    success = fix_multi_word_search()
    sys.exit(0 if success else 1)