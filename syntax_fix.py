#!/usr/bin/env python3
"""
Emergency Syntax Fix for scryfallApi.ts
Fixes the broken template literal and syntax errors
"""

import os
import re

def fix_syntax_errors():
    file_path = "src/services/scryfallApi.ts"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    # Read the current file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Fixing syntax errors...")
    
    # Fix 1: The broken template literal on line 366
    # The script broke the template literal by adding a semicolon in the middle
    broken_template = 'return `oracle:"${query}";'
    fixed_template = 'return `oracle:"${query}"`'
    
    if broken_template in content:
        content = content.replace(broken_template, fixed_template)
        print("✅ Fixed broken template literal")
    
    # Fix 2: Also fix the single-word query template literal that might be broken
    # Look for broken template literals with ${...} syntax
    content = re.sub(r'`\(name:\$\{([^}]+)\} OR oracle:\$\{([^}]+)\} OR type:\$\{([^}]+)\}\)`', 
                     r'`(name:${\\1} OR oracle:${\\2} OR type:${\\3})`', content)
    
    # Fix 3: More comprehensive fix - replace the entire broken buildEnhancedSearchQuery function
    # Look for the function start
    function_start = "function buildEnhancedSearchQuery(query: string): string {"
    
    if function_start in content:
        # Find the function and replace it entirely
        # This is safer than trying to patch individual lines
        new_function = '''function buildEnhancedSearchQuery(query: string): string {
  // FIXED: Scryfall-compatible multi-word search syntax
  console.log('🔍 Building enhanced query for:', query);
  
  // For simple queries without operators, enable full-text search
  if (!query.includes('"') && !query.includes('-') && !query.includes(':')) {
    const words = query.trim().split(/\\s+/);
    
    if (words.length > 1) {
      // Multi-word query: Use oracle text search with proper Scryfall syntax
      console.log('🔍 Multi-word query detected, using oracle text syntax:', query);
      return `oracle:"${query}"`;
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
        
        # Find the end of the function (next function or end of file)
        pattern = r'function buildEnhancedSearchQuery\(query: string\): string \{.*?(?=\n\/\*\*|\nexport|\nfunction|\n$|\Z)'
        
        replacement = re.sub(pattern, new_function, content, flags=re.DOTALL)
        if replacement != content:
            content = replacement
            print("✅ Replaced entire buildEnhancedSearchQuery function")
        else:
            print("⚠️  Could not replace function automatically")
    
    # Write the updated content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Syntax fixes applied to {file_path}")
    return True

def main():
    print("🚨 Emergency syntax fix for scryfallApi.ts")
    print("📍 Current directory:", os.getcwd())
    
    if fix_syntax_errors():
        print("\n✅ Syntax errors fixed!")
        print("\nNext steps:")
        print("1. Run 'npm start' to test if compilation works")
        print("2. Test multi-word searches like 'deal damage'")
        print("3. Verify single-word searches still work")
    else:
        print("\n❌ Could not fix automatically")
        print("Manual fix needed:")
        print("1. Open src/services/scryfallApi.ts")
        print("2. Find line 366 with broken template literal")
        print("3. Change: return `oracle:\"${query}\"; → return `oracle:\"${query}\"`")
        print("4. Fix any other template literal syntax errors")

if __name__ == "__main__":
    main()
